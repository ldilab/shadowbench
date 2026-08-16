#!/usr/bin/env python3
"""
Autoformalization Benchmark runner (compile-check)

NEW (template-completion mode):
- If meta.json contains "target_code", we treat the task as code-completion:
    * Prompt includes informal statement + the target Lean template
    * Model must output a COMPLETE Lean file that compiles
    * No `sorry` allowed (warn.sorry + warningAsError)
    * We optionally enforce that the target declaration signature is unchanged

LEGACY (from-scratch mode):
- If "target_code" is missing, we fall back to the old behavior that asks the
  model to produce Lean code from the informal statement.

NEW (explicit mode override via submissionSpec):
- submissionSpec.eval.formalization_mode = "target" | "full"
    * "target" (default): use template-completion when target_code exists, else from-scratch
    * "full": always ignore target_code and formalize the NL statement from scratch

Called by backend:
  python score_submission.py --spec /tmp/submission_spec.json --out /tmp/result.json

Environment variables:
  SHADOWBENCH_BENCHMARK_DIR           default "~/shadowbench/shadowbench-benchmark"
  SHADOWBENCH_LEAN_IMAGE              (required unless set via spec.runtime.docker_image)
  SHADOWBENCH_EVAL_PROJECT_DIR        default "leanproblems"
  SHADOWBENCH_DOCKER_NETWORK          default "none"
  SHADOWBENCH_CPUS                    default "2"
  SHADOWBENCH_MEMORY                  default "8g"
  SHADOWBENCH_PIDS_LIMIT              default "256"
  SHADOWBENCH_TMPFS_SIZE              default "4g"
  SHADOWBENCH_MODEL_TIMEOUT_SEC       default "120"
  SHADOWBENCH_COMPILE_TIMEOUT_SEC     default "120"
  SHADOWBENCH_MAX_TASKS               default "" (no limit)
  SHADOWBENCH_LOG_PER_TASK            default "0" (set "1" to print per-task failure snippets)
  SHADOWBENCH_ENFORCE_TARGET_SIGNATURE default "1" (completion mode only)

Submission spec (JSON) keys supported:
  - model_cmd: string   (preferred) command to run the model, e.g. "python3 models/example/model.py"
  - model: string       (fallback) model id; resolves to ~/shadowbench/shadowbench-models/<model>/model.py
  - env: object         extra env vars for model command (e.g. VLLM_BASE_URL, VLLM_MODEL)
  - runtime: object     optional overrides:
        docker_image, eval_project_dir, docker_network, model_timeout_sec, compile_timeout_sec
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib

# Optional dependency: PyYAML (not required for meta.json tasks)
try:
    import yaml  # type: ignore
except Exception:
    yaml = None

from datetime import datetime
import uuid
# ----------------------------
# I/O + progress utilities
# ----------------------------

def _configure_io() -> None:
    """Best-effort: make stdout/stderr line-buffered so progress appears even without -u."""
    try:
        sys.stdout.reconfigure(line_buffering=True)  # type: ignore[attr-defined]
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(line_buffering=True)  # type: ignore[attr-defined]
    except Exception:
        pass


def _emit(msg: str) -> None:
    """
    Print a line and flush immediately.

    Note: In some runners only stderr is streamed live. If stdout is not a TTY,
    mirror to stderr as well (avoids double-printing in interactive shells).
    """
    print(msg, flush=True)
    if not sys.stdout.isatty():
        try:
            print(msg, file=sys.stderr, flush=True)
        except Exception:
            pass


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8", errors="replace")
    tmp.replace(path)


def _write_progress_out(out_path: Path, obj: Dict[str, Any]) -> None:
    """Best-effort progress writing for UIs that poll the output JSON."""
    try:
        _atomic_write_text(out_path, json.dumps(obj, indent=2, sort_keys=True))
    except Exception:
        # Never fail the run due to progress I/O
        pass


def _enforce_min_tasks_in_eval_spec(eval_spec: Dict[str, Any], *, min_tasks: int) -> None:
    """
    Ensure eval_spec['num_problems'] / ['max_tasks'] are not set below min_tasks.
    This must happen BEFORE apply_eval_selection(), otherwise tasks are truncated early.
    """
    if min_tasks <= 0:
        return
    for k in ("num_problems", "max_tasks"):
        if eval_spec.get(k) is None:
            continue
        try:
            v = int(eval_spec.get(k))
        except Exception:
            continue
        if v > 0 and v < min_tasks:
            eval_spec[k] = min_tasks



# ----------------------------
# Extraction utilities
# ----------------------------

_LEAN_FENCE_RE = re.compile(
    r"```(?:\s*(?:lean|lean4|l4))?\s*\n(.*?)```",
    re.IGNORECASE | re.DOTALL,
)
_GENERIC_FENCE_RE = re.compile(r"```\s*\n(.*?)```", re.DOTALL)
_LEAN_XML_RE = re.compile(r"<lean>\s*(.*?)</lean>", re.IGNORECASE | re.DOTALL)

_LEAN_START_RE = re.compile(
    r"^\s*(?:import|prelude|universe|namespace|section|open|set_option|"
    r"variable|variables|theorem|lemma|def|example|axiom|constant|constants|"
    r"structure|inductive|class|instance|notation|attribute|macro|syntax|mutual|"
    r"#check|#eval|#print|#reduce|#simp)\b"
)

_TACTIC_START_RE = re.compile(
    r"^\s*(?:by|simp|simp_all|simp_rw|aesop|exact|refine|apply|intro|intros|"
    r"cases|rcases|induction|constructor|have|show|calc|"
    r"nlinarith|linarith|omega|ring|trivial|tauto|finish)\b"
)

# MULTILINE so .search() works across the whole file
_DECL_LINE_RE = re.compile(
    r"^\s*(theorem|lemma|def|example)\s+([A-Za-z0-9_'.]+)\b",
    re.MULTILINE,
)


def _score_block(s: str) -> int:
    t = s.strip()
    if not t:
        return -10
    score = len(t)

    # Lean-y bonuses
    for kw in ("import ", "theorem ", "lemma ", "def ", "namespace ", "section ", "set_option "):
        if kw in t:
            score += 200
    if ":=" in t:
        score += 80
    if "by" in t:
        score += 40

    # Slight penalty for blocks that look like prose
    if re.search(r"\b(Explanation|Notes|Proof sketch|Here is)\b", t):
        score -= 150
    return score


def _extract_from_jsonish(raw: str) -> Optional[str]:
    """
    Best-effort extraction from JSON-like responses.
    Supports:
      {"lean_code": "..."} / {"code": "..."} / {"lean": "..."}
      OpenAI-ish: {"choices":[{"message":{"content":"..."}}]}
    """
    s = raw.strip()
    if not s or s[0] not in "{[":
        return None

    try:
        obj = json.loads(s)
    except Exception:
        if "{" in s and "}" in s:
            sub = s[s.find("{") : s.rfind("}") + 1]
            try:
                obj = json.loads(sub)
            except Exception:
                return None
        else:
            return None

    def pick(d: Any) -> Optional[str]:
        if isinstance(d, dict):
            for k in ("lean_code", "lean", "code", "content", "answer", "final"):
                v = d.get(k)
                if isinstance(v, str) and v.strip():
                    return v
            ch = d.get("choices")
            if isinstance(ch, list) and ch:
                c0 = ch[0]
                if isinstance(c0, dict):
                    msg = c0.get("message")
                    if isinstance(msg, dict):
                        c = msg.get("content")
                        if isinstance(c, str) and c.strip():
                            return c
                    c = c0.get("text")
                    if isinstance(c, str) and c.strip():
                        return c
        return None

    return pick(obj)


def _looks_leanish(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    if any(k in t for k in ("theorem", "lemma", "def", "import", ":=", "#check", "#eval", "namespace", "section")):
        return True
    if re.search(r"[∀∃→←↔∧∨⊢]", t):
        return True
    return False


def _line_is_probably_lean(line: str) -> bool:
    s = line.rstrip("\n")
    t = s.strip()

    if not t:
        return True  # blank lines are fine in Lean

    if t.startswith("```"):
        return False

    # comments
    if t.startswith("--") or t.startswith("/-") or t.endswith("-/"):
        return True

    # common Lean starts
    if _LEAN_START_RE.match(t) or _TACTIC_START_RE.match(t) or _DECL_LINE_RE.match(t):
        return True
    if t == "end" or t.startswith("end "):
        return True
    if t == "where" or t.startswith("where "):
        return True

    # indentation usually means proof/tactic continuation
    if s[:1].isspace():
        return True

    # Lean-y punctuation/symbols
    if re.search(r"[:=<>⟨⟩∀∃→←↔∧∨⊢]", t):
        return True
    if re.search(r"\b(by|simp|exact|intro|apply|refine|have|show|calc|cases|rcases|induction)\b", t):
        return True

    # Markdown-ish / prose-ish lines
    if t.startswith(("*", "- ", "• ")) or re.match(r"^\d+\.", t):
        return False
    if t.startswith("#") and not re.match(r"^#(check|eval|print|reduce|simp)\b", t):
        return False

    if re.match(r"^[A-Za-z][A-Za-z0-9 ,;:'\"()\\-]+[.!?]$", t):
        return False

    return True


def _extract_lean_code(raw: Optional[str]) -> str:
    """
    Extract Lean code from a model response. Prefers fenced blocks but will
    fall back to heuristic extraction for plain text outputs.
    """
    if not raw:
        return ""

    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    s = raw.strip()
    if not s:
        return ""

    extracted = _extract_from_jsonish(s)
    if extracted and extracted.strip():
        s = extracted.strip()

    m = _LEAN_XML_RE.search(s)
    if m:
        code = m.group(1).strip()
        return (code + "\n") if code else ""

    blocks = _LEAN_FENCE_RE.findall(s)
    if not blocks:
        blocks = _GENERIC_FENCE_RE.findall(s)

    if blocks:
        best = max(blocks, key=_score_block).strip()
        return (best + "\n") if best else ""

    # plain text heuristic: find first Lean-looking line
    lines = s.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        if _LEAN_START_RE.match(line) or _TACTIC_START_RE.match(line) or _DECL_LINE_RE.match(line):
            start_idx = i
            break

    if start_idx is None:
        return (s + "\n") if _looks_leanish(s) else ""

    kept: list[str] = []
    for line in lines[start_idx:]:
        if _line_is_probably_lean(line):
            kept.append(line.rstrip("\n"))
        else:
            continue

    code = "\n".join(kept).strip()
    return (code + "\n") if code else ""


# ----------------------------
# Completion-mode helpers
# ----------------------------

def _normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def _infer_primary_decl(code: str) -> Optional[Tuple[str, str]]:
    """
    Returns (kind, name) for the first theorem/lemma/def/example in the file.
    """
    m = _DECL_LINE_RE.search(code or "")
    if not m:
        return None
    return m.group(1), m.group(2)


def _extract_decl_signature(code: str, *, kind: str, name: str) -> Optional[str]:
    """
    Extract signature substring from:  <kind> <name> ...  up to and including ':='
    Whitespace-insensitive comparison is done elsewhere.
    """
    if not code:
        return None
    pat = re.compile(rf"(?m)^\s*{re.escape(kind)}\s+{re.escape(name)}\b")
    m = pat.search(code)
    if not m:
        return None
    idx = code.find(":=", m.end())
    if idx == -1:
        return None
    sig = code[m.start() : idx + 2]
    return sig.strip()


# ----------------------------
# Benchmark helpers
# ----------------------------

def _die(msg: str, code: int = 2) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def _get_env_int(name: str, default: int) -> int:
    v = os.environ.get(name, "")
    if not v:
        return default
    try:
        return int(v)
    except Exception:
        return default


def _get_env_str(name: str, default: str) -> str:
    v = os.environ.get(name)
    return v if v is not None and v != "" else default


def _safe_stem(s: str) -> str:
    s = (s or "").strip() or "task"
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s)


def _safe_id_piece(s: str, *, max_len: int = 32) -> str:
    """Filesystem-safe short identifier component."""
    s = (s or "").strip() or "misc"
    s = re.sub(r"[^A-Za-z0-9_.-]+", "_", s)
    s = s.strip("._-") or "misc"
    return s[:max_len]


def _make_run_id(submission_spec: Dict[str, Any]) -> str:
    """
    Create a unique run id like:
        20260318T014102Z__mymodel__a1b2c3

    This becomes the per-run log directory name.
    """
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    label = "misc"
    try:
        if isinstance(submission_spec.get("model"), str) and str(submission_spec.get("model")).strip():
            label = str(submission_spec.get("model")).strip()
        elif isinstance(submission_spec.get("model_cmd"), str) and str(submission_spec.get("model_cmd")).strip():
            cmd0 = shlex.split(str(submission_spec.get("model_cmd")).strip())[0]
            label = Path(cmd0).stem or "misc"
        else:
            # fallback to common env var used by some runners
            env_label = os.environ.get("VLLM_MODEL", "").strip() or os.environ.get("MODEL", "").strip()
            if env_label:
                label = env_label
    except Exception:
        label = "misc"

    label = _safe_id_piece(label, max_len=24)
    nonce = uuid.uuid4().hex[:6]
    return f"{ts}__{label}__{nonce}"


def _level_bucket(level: str) -> str:
    """
    Map dataset levels to HighSchool / College / Research.
    """
    level = (level or "").strip().upper()
    m = re.match(r"L(\d+)", level)
    if not m:
        return "College"
    n = int(m.group(1))
    if n <= 1:
        return "HighSchool"
    if n <= 3:
        return "College"
    return "Research"


@dataclass
class Task:
    task_id: str          # e.g. "geometry/L3/geo_gen_L3_001"
    dir: Path
    area: str
    level: str
    level_bucket: str

    # Informal statement
    text: str

    # Completion template (preferred new path)
    target_code: Optional[str] = None

    # Inferred from target_code when present
    target_kind: Optional[str] = None
    target_decl: Optional[str] = None
    target_sig: Optional[str] = None

    # Legacy metadata (optional)
    target_type: Optional[str] = None


@dataclass
class TaskResult:
    task_id: str
    ok: bool
    area: str
    level_bucket: str
    compile_sec: float
    model_sec: float
    err: str = ""


def load_tasks(benchmark_dir: Path) -> List[Task]:
    """
    Loads tasks from: <benchmark_dir>/data/**/meta.json

    Supports:
      - NL text from <prob_dir>/text.md OR meta["text"]
      - template from meta["target_code"] (new)
      - legacy fields meta["target_decl"], meta["target_type"], meta["target_kind"] (optional)
    """
    data_root = benchmark_dir / "data"
    metas = sorted(data_root.glob("**/meta.json"))
    tasks: List[Task] = []

    for meta_path in metas:
        prob_dir = meta_path.parent  # data/<area>/<level>/<problemid>/
        level = prob_dir.parent.name
        area = prob_dir.parent.parent.name
        problem_id = prob_dir.name

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        # NL text: prefer text.md, else meta["text"]
        nl_text = ""
        text_path = prob_dir / "text.md"
        if text_path.exists():
            nl_text = text_path.read_text(encoding="utf-8", errors="replace").strip()
        else:
            nl_text = (meta.get("text") or "").strip()

        if not nl_text:
            # Skip tasks with no NL prompt at all
            continue

        # New: template code
        target_code = meta.get("target_code")
        if isinstance(target_code, str):
            target_code = target_code.strip()
        else:
            target_code = None

        # Legacy: explicit target info (optional)
        target_decl = meta.get("target_decl")
        target_kind = meta.get("target_kind")
        target_type = meta.get("target_type")

        # If we have target_code, infer primary decl/kind and signature
        inferred_kind = None
        inferred_decl = None
        inferred_sig = None
        if target_code:
            inf = _infer_primary_decl(target_code)
            if inf:
                inferred_kind, inferred_decl = inf
                inferred_sig = _extract_decl_signature(
                    target_code, kind=inferred_kind, name=inferred_decl
                )

        # Prefer explicit meta fields if present, else inferred
        kind = (str(target_kind).strip() if isinstance(target_kind, str) and target_kind.strip() else inferred_kind)
        decl = (str(target_decl).strip() if isinstance(target_decl, str) and target_decl.strip() else inferred_decl)
        sig = inferred_sig if inferred_sig else None

        task_id = f"{area}/{level}/{problem_id}"
        tasks.append(Task(
            task_id=task_id,
            dir=prob_dir,
            area=area,
            level=level,
            level_bucket=_level_bucket(level),
            text=nl_text,
            target_code=target_code,
            target_kind=kind,
            target_decl=decl,
            target_sig=sig,
            target_type=(str(target_type).strip() if isinstance(target_type, str) and target_type.strip() else None),
        ))

    return tasks

def _as_str_list(x: Any) -> List[str]:
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i).strip() for i in x if str(i).strip()]
    if isinstance(x, str):
        # allow comma-separated
        return [p.strip() for p in x.split(",") if p.strip()]
    return [str(x).strip()] if str(x).strip() else []

def _task_hash_key(task_id: str, seed: int) -> str:
    s = f"{seed}|{task_id}".encode("utf-8", errors="replace")
    return hashlib.sha256(s).hexdigest()

def apply_eval_selection(
    tasks: List[Task],
    eval_spec: Dict[str, Any],
    *,
    fallback_max_tasks: Optional[int],
) -> Tuple[List[Task], Dict[str, Any]]:
    """
    Filters tasks by areas/levels and selects num_problems deterministically.

    Returns (selected_tasks, resolved_eval_dict).
    """
    # --- parse inputs ---
    areas_in = [a for a in _as_str_list(eval_spec.get("areas"))]
    levels_in = [l for l in _as_str_list(eval_spec.get("levels"))]

    seed = eval_spec.get("seed", 1337)
    try:
        seed = int(seed)
    except Exception:
        seed = 1337

    sampling = str(eval_spec.get("sampling", "hash")).strip().lower()
    if sampling not in ("hash", "first"):
        sampling = "hash"

    n = eval_spec.get("num_problems", eval_spec.get("max_tasks", None))
    if n is None:
        n = fallback_max_tasks
    try:
        n = int(n) if n is not None else None
    except Exception:
        n = fallback_max_tasks

    # --- normalize available sets for case-insensitive matching ---
    available_areas = sorted({t.area for t in tasks})
    area_map = {a.lower(): a for a in available_areas}

    available_levels = sorted({t.level for t in tasks})
    level_map = {lv.lower(): lv for lv in available_levels}

    # We also allow bucket names
    available_buckets = sorted({t.level_bucket for t in tasks})
    bucket_map = {b.lower(): b for b in available_buckets}

    # --- apply filters ---
    selected_areas: List[str] = []
    if areas_in:
        for a in areas_in:
            key = a.lower()
            if key in area_map:
                selected_areas.append(area_map[key])
        # if user provided only unknown areas, you can choose to:
        # - treat as error, or
        # - evaluate nothing
        # Here we treat unknown-only as "no match" -> empty tasks.
        area_set = set(selected_areas)
        tasks = [t for t in tasks if t.area in area_set]

    selected_levels: List[str] = []
    selected_buckets: List[str] = []
    if levels_in:
        for l in levels_in:
            key = l.lower()
            if key in level_map:
                selected_levels.append(level_map[key])
            elif key in bucket_map:
                selected_buckets.append(bucket_map[key])

        lvl_set = set(selected_levels)
        buck_set = set(selected_buckets)
        tasks = [t for t in tasks if (t.level in lvl_set) or (t.level_bucket in buck_set)]

    # --- deterministic sampling ---
    total_after_filter = len(tasks)

    # stable order before sampling
    if sampling == "first":
        tasks = sorted(tasks, key=lambda t: t.task_id)
    else:
        tasks = sorted(tasks, key=lambda t: _task_hash_key(t.task_id, seed))

    if n is not None and n >= 0:
        tasks = tasks[:n]

    resolved = {
        "num_problems": n if n is not None else total_after_filter,
        "areas": selected_areas if areas_in else "ALL",
        "levels": selected_levels if selected_levels else [],
        "levelBuckets": selected_buckets if selected_buckets else [],
        "seed": seed,
        "sampling": sampling,
        "availableAfterFilter": total_after_filter,
        "selected": len(tasks),
    }
    return tasks, resolved

def resolve_model_cmd(spec: Dict[str, Any]) -> Tuple[List[str], Dict[str, str]]:
    """
    Resolve the model command + environment.
    Returns (argv, env_overrides).
    """
    env_overrides = {str(k): str(v) for k, v in (spec.get("env") or {}).items()}

    if isinstance(spec.get("model_cmd"), str) and spec["model_cmd"].strip():
        cmd = spec["model_cmd"].strip()
        return shlex.split(cmd), env_overrides

    model_id = spec.get("model")
    if isinstance(model_id, str) and model_id.strip():
        mp = Path("~/shadowbench/shadowbench-models").expanduser() / model_id.strip() / "model.py"
        return [str(mp)], env_overrides

    _die("submissionSpec must include 'model_cmd' or 'model'", 2)
    raise RuntimeError("unreachable")


def call_model(model_argv: List[str], model_env: Dict[str, str], prompt: str, timeout_sec: int) -> Tuple[str, float, str]:
    """
    Run model command as a subprocess. Returns (stdout, elapsed, errstr).
    NOTE: In this harness, ANY stderr output is treated as an error (to keep runners clean).
    """
    env = os.environ.copy()
    env.update(model_env)

    t0 = time.time()
    try:
        proc = subprocess.run(
            model_argv + [prompt],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        return "", time.time() - t0, "MODEL_TIMEOUT"
    except FileNotFoundError:
        return "", time.time() - t0, f"MODEL_CMD_NOT_FOUND: {model_argv[0]}"
    except Exception as e:
        return "", time.time() - t0, f"MODEL_ERROR: {e}"

    out = proc.stdout or ""
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        return out, time.time() - t0, f"MODEL_EXIT_{proc.returncode}: {err[:2000]}"
    if err:
        return out, time.time() - t0, err
    return out, time.time() - t0, ""


_HEADER_IMPORT_RE = re.compile(
    r"^\s*(?:(?:public|meta)\s+)*import(?:\s+all)?\s+(.+?)\s*$"
)


def _parse_header_imports(text: str) -> List[str]:
    """Best-effort parser for top-of-file Lean imports."""
    out: List[str] = []
    seen = set()
    in_block_comment = False

    for raw in text.splitlines():
        line = raw.strip()

        if in_block_comment:
            if '-/' in line:
                in_block_comment = False
            continue

        if not line:
            continue
        if line.startswith('/-') and '-/' not in line:
            in_block_comment = True
            continue
        if line.startswith('--') or (line.startswith('/-') and line.endswith('-/')):
            continue
        if line == 'prelude' or line == 'module' or line.startswith('module '):
            continue

        m = _HEADER_IMPORT_RE.match(line)
        if m:
            rest = m.group(1).split('--', 1)[0].strip()
            if rest:
                for tok in rest.split():
                    tok = tok.strip()
                    if tok and tok not in seen:
                        seen.add(tok)
                        out.append(tok)
            continue

        break

    return out


def _find_abm_parent(benchmark_dir: Path) -> Optional[Path]:
    for parent in (benchmark_dir, benchmark_dir / 'data'):
        if (parent / 'ShadowBench').is_dir():
            return parent
    return None


def _collect_abm_import_closure(lean_file: Path, benchmark_dir: Path) -> Tuple[List[str], List[str]]:
    """
    Return ShadowBench imports needed by `lean_file` in dependency order (deps first),
    along with any missing ShadowBench modules referenced from source imports.
    """
    abm_parent = _find_abm_parent(benchmark_dir)
    if abm_parent is None:
        return [], []

    try:
        initial_imports = _parse_header_imports(lean_file.read_text(encoding='utf-8', errors='ignore'))
    except Exception:
        return [], []

    ordered: List[str] = []
    missing: List[str] = []
    seen = set()

    def visit(mod: str) -> None:
        if mod in seen:
            return
        seen.add(mod)

        if not (mod == 'ShadowBench' or mod.startswith('ShadowBench.')):
            return

        src = abm_parent / (mod.replace('.', '/') + '.lean')
        if not src.exists():
            missing.append(mod)
            return

        try:
            deps = _parse_header_imports(src.read_text(encoding='utf-8', errors='ignore'))
        except Exception:
            deps = []

        for dep in deps:
            if dep == 'ShadowBench' or dep.startswith('ShadowBench.'):
                visit(dep)

        ordered.append(mod)

    for mod in initial_imports:
        if mod == 'ShadowBench' or mod.startswith('ShadowBench.'):
            visit(mod)

    return ordered, missing


def compile_in_docker(lean_file: Path, benchmark_dir: Path, timeout_sec: int) -> Tuple[bool, float, str]:
    """
    Compile a Lean file inside a hardened Docker container.
    Uses a pre-built eval project mounted at /proj.
    """
    image = os.environ.get("SHADOWBENCH_LEAN_IMAGE", "").strip()
    if not image:
        _die("Set SHADOWBENCH_LEAN_IMAGE (or spec.runtime.docker_image) to a Lean+Mathlib docker image", 2)

    eval_proj = Path(_get_env_str("SHADOWBENCH_EVAL_PROJECT_DIR", "leanproblems")).expanduser().resolve()
    if not eval_proj.exists():
        return False, 0.0, f"EVAL_PROJECT_DIR_NOT_FOUND: {eval_proj}"

    network = _get_env_str("SHADOWBENCH_DOCKER_NETWORK", "none")
    cpus = _get_env_str("SHADOWBENCH_CPUS", "2")
    mem = _get_env_str("SHADOWBENCH_MEMORY", "8g")
    pids = _get_env_str("SHADOWBENCH_PIDS_LIMIT", "256")
    tmpfs = _get_env_str("SHADOWBENCH_TMPFS_SIZE", "4g")

    workdir = lean_file.parent.resolve()
    in_path = "/work/" + lean_file.name

    abm_modules, missing_shadowbench_modules = _collect_abm_import_closure(lean_file, benchmark_dir)
    abm_modules_block = "\n".join(abm_modules)
    missing_shadowbench_note = ""
    if missing_shadowbench_modules:
        missing_shadowbench_note = "\n[host] missing ShadowBench sources: " + ", ".join(missing_shadowbench_modules[:10])

    cmd_inside = f"""
set -eu
export HOME=/tmp
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TOOLCHAIN="$(tr -d '\\r\\n' < /proj/lean-toolchain 2>/dev/null || true)"
TAG="$(printf "%s" "$TOOLCHAIN" | sed 's/.*://')"
[ -z "$TAG" ] && TAG="$(ls -d /elan/toolchains/leanprover--lean4---* 2>/dev/null | head -n 1 | sed 's#.*/leanprover--lean4---##' || true)"

TC_DIR="/elan/toolchains/leanprover--lean4---$TAG"
if [ ! -d "$TC_DIR" ]; then
  TC_DIR="$(ls -d /elan/toolchains/leanprover--lean4---* 2>/dev/null | head -n 1 || true)"
fi

LEAN_BIN="$TC_DIR/bin/lean"
if [ ! -x "$LEAN_BIN" ]; then
  echo "[docker] ERROR: Lean binary not executable: $LEAN_BIN" >&2
  exit 81
fi

# Ensure Mathlib oleans exist
if [ ! -f /proj/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ]; then
  echo "[docker] ERROR: missing /proj/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" >&2
  exit 80
fi

BENCH_ROOT=""
if [ -d /bench/ShadowBench ]; then
  BENCH_ROOT="/bench"
elif [ -d /bench/data/ShadowBench ]; then
  BENCH_ROOT="/bench/data"
fi

SHADOWBENCH_OLEAN_ROOT="/tmp/shadowbench-oleans"
mkdir -p "$SHADOWBENCH_OLEAN_ROOT"

LP="$SHADOWBENCH_OLEAN_ROOT:/proj/.lake/build/lib/lean:/proj"
for d in /proj/.lake/packages/*/.lake/build/lib/lean; do
  [ -d "$d" ] && LP="$d:$LP"
done
if [ -n "$BENCH_ROOT" ]; then
  LP="$LP:$BENCH_ROOT"
  export LEAN_SRC_PATH="$BENCH_ROOT:/proj"
else
  export LEAN_SRC_PATH="/proj"
fi
export LEAN_PATH="$LP"

echo "[docker] BENCH_ROOT=$BENCH_ROOT" >&2
echo "[docker] LEAN_PATH=$LEAN_PATH" >&2
echo "[docker] LEAN_SRC_PATH=$LEAN_SRC_PATH" >&2

cat > /tmp/abm_modules.txt <<'EOF_SHADOWBENCH_MODULES'
{abm_modules_block}
EOF_SHADOWBENCH_MODULES

if [ -s /tmp/abm_modules.txt ]; then
  if [ -z "$BENCH_ROOT" ]; then
    echo "[docker] ERROR: target imports ShadowBench modules but no ShadowBench source root was mounted under /bench or /bench/data" >&2
    exit 82
  fi

  echo "[docker] precompiling ShadowBench source deps" >&2
  while IFS= read -r mod; do
    [ -n "$mod" ] || continue
    rel="$(printf "%s" "$mod" | tr '.' '/').lean"
    src="$BENCH_ROOT/$rel"
    out="$SHADOWBENCH_OLEAN_ROOT/${{rel%.lean}}.olean"
    if [ ! -f "$src" ]; then
      echo "[docker] ERROR: missing ShadowBench source for $mod at $src" >&2
      exit 83
    fi
    mkdir -p "$(dirname "$out")"
    echo "[docker] build $mod" >&2
    "$LEAN_BIN" -R "$BENCH_ROOT" -o "$out" "$src"
  done < /tmp/abm_modules.txt
fi

"$LEAN_BIN" -o /tmp/out.olean {shlex.quote(in_path)}
""".strip()

    docker_cmd = [
        "docker", "run", "--rm",
        "--network", network,
        "--cpus", cpus,
        "--memory", mem,
        "--pids-limit", pids,
        "--read-only",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "-u", f"{os.getuid()}:{os.getgid()}",
        "-e", "HOME=/tmp",
        "--tmpfs", f"/tmp:rw,noexec,nosuid,size={tmpfs}",
        "--tmpfs", f"/var/tmp:rw,noexec,nosuid,size={tmpfs}",
        "-v", f"{str(benchmark_dir.resolve())}:/bench:ro",
        "-v", f"{str(eval_proj)}:/proj:ro",
        "-v", f"{str(workdir)}:/work:rw",
        "-v", f"{str((Path.home() / '.elan').resolve())}:/elan:ro",
        "-w", "/work",
        "--entrypoint", "/bin/sh",
        image,
        "-c", cmd_inside,
    ]

    t0 = time.time()
    try:
        proc = subprocess.run(
            docker_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        return False, time.time() - t0, "COMPILE_TIMEOUT"
    except FileNotFoundError:
        return False, time.time() - t0, "DOCKER_NOT_FOUND"
    except Exception as e:
        return False, time.time() - t0, f"DOCKER_ERROR: {e}"

    ok = proc.returncode == 0
    out = (proc.stdout or "") + "\n" + (proc.stderr or "") + missing_shadowbench_note
    return ok, time.time() - t0, out.strip()[:6000]


def build_prompt(task: Task, *, use_target_template: bool) -> str:
    """Build a prompt for either template-completion or from-scratch formalization."""
    if use_target_template and task.target_code:
        lines: List[str] = []
        lines.append("You are an autoformalization system for Lean 4 + Mathlib.")
        lines.append("Goal: COMPLETE the given Lean file template by replacing ALL `sorry` with correct Lean code so the file compiles.")
        lines.append("Rules:")
        lines.append("- Output ONLY Lean code. No markdown, no explanation.")
        lines.append("- Do NOT leave any `sorry`.")
        if task.target_kind and task.target_decl and task.target_sig:
            lines.append(f"- Do NOT change the declaration header/signature of `{task.target_decl}` (up to `:=`).")
        lines.append("")
        lines.append("INFORMAL STATEMENT (for guidance):")
        lines.append(task.text.strip())
        lines.append("")
        lines.append("LEAN TEMPLATE (fill the sorries):")
        lines.append(task.target_code.strip())
        lines.append("")
        lines.append("Now output the FULL completed Lean file.")
        return "\n".join(lines)

    # From-scratch (NL -> Lean)
    lines = []
    lines.append("You are an autoformalization system for Lean 4 + Mathlib.")
    lines.append("Translate the following informal statement into Lean 4 code that compiles with Mathlib.")
    lines.append("Do not use `sorry` (sorry warnings are treated as errors).")
    lines.append("Output ONLY Lean code (no markdown, no explanation).")
    lines.append("")
    lines.append("INFORMAL STATEMENT:")
    lines.append(task.text.strip())
    return "\n".join(lines)


def _resolve_formalization_mode(submission_spec: Dict[str, Any]) -> str:
    """
    Resolve runner behavior for tasks that have target templates.

    Accepted values (case-insensitive):
      - "target" (default): use target template when present
      - "full": ignore target templates and formalize NL from scratch

    Also accepts common aliases.
    """
    # Order of precedence: eval -> top-level -> bench -> env
    v: Any = None
    try:
        ev = submission_spec.get("eval")
        if isinstance(ev, dict) and "formalization_mode" in ev:
            v = ev.get("formalization_mode")
    except Exception:
        v = None

    if v is None and "formalization_mode" in submission_spec:
        v = submission_spec.get("formalization_mode")

    if v is None:
        try:
            bench = submission_spec.get("bench")
            if isinstance(bench, dict) and "formalization_mode" in bench:
                v = bench.get("formalization_mode")
        except Exception:
            v = None

    if v is None:
        v = os.environ.get("SHADOWBENCH_FORMALIZATION_MODE", "")

    s = str(v or "").strip().lower()

    # full/scratch/from-scratch aliases
    if s in {"full", "scratch", "from_scratch", "from-scratch", "nl", "no_target", "ignore_target"}:
        return "full"

    # target/template/auto aliases
    if s in {"target", "template", "completion", "complete", "auto", "default", ""}:
        return "target"

    # unknown -> default
    return "target"


def wrap_for_compile(code: str, *, task: Task, completion_mode: bool) -> str:
    """
    Wraps code into a file to compile, injecting strict options.

    IMPORTANT:
    - In completion mode, we DO NOT force-add `import Mathlib` if imports already exist,
      because target templates usually have precise imports for speed.
    - If there are NO imports, we add `import Mathlib`.
    """
    options_block = "set_option warn.sorry true\nset_option warningAsError true\n\n"
    task_comment = f"/- task: {task.task_id} (area={task.area}, level={task.level}) -/\n\n"

    c = (code or "").strip() + "\n"
    m = re.match(r"(?s)\A(\s*(?:import[^\n]*\n)+)", c)

    if m:
        imports = m.group(1).rstrip() + "\n\n"
        rest = c[m.end():].lstrip()

        # Only add import Mathlib in legacy mode
        if (not completion_mode) and ("import Mathlib" not in imports):
            imports = "import Mathlib\n" + imports

        wrapped = imports + options_block + task_comment + rest.strip() + "\n"
        return wrapped

    # No imports at all -> add Mathlib import
    return "import Mathlib\n\n" + options_block + task_comment + c.strip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    # Try to make progress visible even without `PYTHONUNBUFFERED=1 python -u ...`
    _configure_io()

    # Hard floor: never evaluate fewer than this many tasks (unless filtering leaves fewer).
    MIN_TASKS = 3

    benchmark_dir = Path(os.environ.get("SHADOWBENCH_BENCHMARK_DIR", "~/shadowbench/shadowbench-benchmark")).expanduser().resolve()

    spec_obj = json.loads(args.spec.read_text(encoding="utf-8"))
    submission_spec = spec_obj if isinstance(spec_obj, dict) else {}

    # runtime config from spec (env still wins if already set)
    runtime = submission_spec.get("runtime", {}) if isinstance(submission_spec.get("runtime", {}), dict) else {}
    if "docker_image" in runtime:
        os.environ.setdefault("SHADOWBENCH_LEAN_IMAGE", str(runtime["docker_image"]))
    if "eval_project_dir" in runtime:
        os.environ.setdefault("SHADOWBENCH_EVAL_PROJECT_DIR", str(runtime["eval_project_dir"]))
    if "docker_network" in runtime:
        os.environ.setdefault("SHADOWBENCH_DOCKER_NETWORK", str(runtime["docker_network"]))
    if "compile_timeout_sec" in runtime:
        os.environ.setdefault("SHADOWBENCH_COMPILE_TIMEOUT_SEC", str(runtime["compile_timeout_sec"]))
    if "model_timeout_sec" in runtime:
        os.environ.setdefault("SHADOWBENCH_MODEL_TIMEOUT_SEC", str(runtime["model_timeout_sec"]))

    model_argv, model_env = resolve_model_cmd(submission_spec)
    model_timeout = _get_env_int("SHADOWBENCH_MODEL_TIMEOUT_SEC", 120)
    compile_timeout = _get_env_int("SHADOWBENCH_COMPILE_TIMEOUT_SEC", 120)

    log_per_task = _get_env_int("SHADOWBENCH_LOG_PER_TASK", 0) == 1
    enforce_sig = _get_env_int("SHADOWBENCH_ENFORCE_TARGET_SIGNATURE", 1) == 1

    # Global override: how we treat tasks with target templates.
    #   - "target": use template completion when target_code exists
    #   - "full": ignore target_code and always do NL->Lean from scratch
    formalization_mode = _resolve_formalization_mode(submission_spec)
    enforce_sig_effective = enforce_sig and (formalization_mode != "full")

    # Progress controls
    emit_every = _get_env_int("SHADOWBENCH_PROGRESS_EVERY", 1)
    if emit_every < 1:
        emit_every = 1
    write_progress = _get_env_int("SHADOWBENCH_WRITE_PROGRESS", 1) == 1
    write_every = _get_env_int("SHADOWBENCH_WRITE_PROGRESS_EVERY", 1)
    if write_every < 1:
        write_every = 1

    LOG_ROOT = Path(os.environ.get("SHADOWBENCH_LOG_DIR", "run_logs")).expanduser().resolve()
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    run_id = _make_run_id(submission_spec)
    LOG_DIR = LOG_ROOT / run_id
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    _emit(f"[debug] LOG_ROOT = {LOG_ROOT}")
    _emit(f"[debug] RUN_DIR = {LOG_DIR}")

    logs: List[str] = []

    # SHADOWBENCH_MAX_TASKS is a server cap (optional)
    max_tasks = os.environ.get("SHADOWBENCH_MAX_TASKS", "").strip()
    max_tasks_n = int(max_tasks) if max_tasks.isdigit() else None

    tasks = load_tasks(benchmark_dir)

    # NEW: apply eval selection from spec (num_problems / areas / levels)
    eval_spec = submission_spec.get("eval", {})
    if not isinstance(eval_spec, dict):
        eval_spec = {}

    # Enforce MIN_TASKS BEFORE selection truncates the task list
    _enforce_min_tasks_in_eval_spec(eval_spec, min_tasks=MIN_TASKS)

    tasks, resolved_eval = apply_eval_selection(
        tasks,
        eval_spec,
        fallback_max_tasks=None,
    )

    # (optional) include in logs
    logs.append(f"Eval selection: {resolved_eval}")
    logs.append("")

    # server cap (optional)
    server_cap = max_tasks_n  # SHADOWBENCH_MAX_TASKS

    # requested cap (prefer eval.num_problems, fallback to bench.limit)
    requested: Optional[int] = None
    try:
        if eval_spec.get("num_problems") is not None:
            requested = int(eval_spec.get("num_problems"))
    except Exception:
        requested = None

    if requested is None:
        bench = submission_spec.get("bench", {})
        if isinstance(bench, dict):
            try:
                if bench.get("limit") is not None:
                    requested = int(bench.get("limit"))
            except Exception:
                requested = None

    # Enforce MIN_TASKS floor on caps (once-and-for-all)
    if requested is not None and requested > 0 and requested < MIN_TASKS:
        requested = MIN_TASKS
    if server_cap is not None and server_cap > 0 and server_cap < MIN_TASKS:
        server_cap = MIN_TASKS

    cap: Optional[int] = None
    if requested is not None and requested > 0 and server_cap is not None and server_cap > 0:
        cap = min(requested, server_cap)
    elif requested is not None and requested > 0:
        cap = requested
    elif server_cap is not None and server_cap > 0:
        cap = server_cap

    if cap is not None:
        tasks = tasks[:cap]

    # Update resolved_eval so the log reflects reality
    resolved_eval = dict(resolved_eval)
    resolved_eval["requested"] = requested
    resolved_eval["serverCap_SHADOWBENCH_MAX_TASKS"] = server_cap
    resolved_eval["finalCap"] = cap
    resolved_eval["finalSelected"] = len(tasks)

    if not tasks:
        _die(f"No tasks found under {benchmark_dir}/data/**/meta.json", 2)

    if len(tasks) < MIN_TASKS:
        _emit(f"[warn] Only {len(tasks)} tasks available after filtering; cannot reach MIN_TASKS={MIN_TASKS}")

    _emit(f"[info] ShadowBench eval starting: tasks={len(tasks)} (requested={requested}, serverCap={server_cap})")
    _emit(f"[info] Eval selection: {resolved_eval}")
    _emit(f"[info] Formalization mode: {formalization_mode} (enforceTargetSignatureEffective={enforce_sig_effective})")

    logs.append(f"Loaded {len(tasks)} tasks from {benchmark_dir}/data")
    logs.append(f"Model cmd: {shlex.join(model_argv)}")
    logs.append(f"Docker image: {os.environ.get('SHADOWBENCH_LEAN_IMAGE','(unset)')}")
    logs.append(f"Docker network: {_get_env_str('SHADOWBENCH_DOCKER_NETWORK','none')}")
    logs.append(f"Formalization mode: {formalization_mode}")
    logs.append(f"Enforce target signature (env): {enforce_sig} (effective): {enforce_sig_effective}")
    logs.append("")

    logs.append(f"Benchmark dir: {benchmark_dir}")
    logs.append(f"Total tasks loaded: {len(tasks)}")
    logs.append(f"Task IDs (first 5): {[t.task_id for t in tasks[:5]]}")
    logs.append("")

    # Write an initial output file so polling UIs have *something* immediately.
    t_start = time.time()
    processed = 0
    passed = 0
    sum_compile = 0.0
    sum_model = 0.0

    if write_progress:
        init_obj: Dict[str, Any] = {
            "overall": 0.0,
            "pass1": 0.0,
            "pass5": 0.0,
            "compileRate": 0.0,
            "avgTimeSec": 0.0,
            "tokensPerTask": 0,
            "usdPerTask": 0.0,
            "categories": {},
            "levels": {},
            "meta": {
                "status": "running",
                "runId": run_id,
                "runDir": str(LOG_DIR),
                "tasks": len(tasks),
                "processed": 0,
                "passed": 0,
                "progress": 0.0,
                "elapsedSec": 0.0,
                "avgModelSecSoFar": 0.0,
                "avgCompileSecSoFar": 0.0,
                "benchmarkDir": str(benchmark_dir),
                "dockerNetwork": _get_env_str("SHADOWBENCH_DOCKER_NETWORK", "none"),
                "formalizationMode": formalization_mode,
                "enforceTargetSignature": enforce_sig,
                "enforceTargetSignatureEffective": enforce_sig_effective,
                "eval:": resolved_eval,
            },
        }
        _write_progress_out(args.out, init_obj)

    results: List[TaskResult] = []

    def _maybe_emit_progress_line(i: int, task_id: str, ok: bool, model_sec: float, comp_sec: float, mode: str) -> None:
        if i == 1 or i == len(tasks) or (emit_every > 0 and (i % emit_every == 0)) or (not ok):
            _emit(f"[{i}/{len(tasks)}] {task_id} ok={ok} model={model_sec:.2f}s compile={comp_sec:.2f}s mode={mode}")

    def _maybe_write_progress_json(i: int, last_task: str, last_ok: bool, last_err: str) -> None:
        nonlocal processed, passed, sum_compile, sum_model
        if not write_progress:
            return
        if i != len(tasks) and (write_every <= 0 or (i % write_every != 0)) and last_ok:
            # write on schedule, always write on final step, and always write on failures
            return

        prog = processed / max(len(tasks), 1)
        compile_rate_so_far = 100.0 * passed / max(processed, 1)
        avg_compile_so_far = sum_compile / max(processed, 1)
        avg_model_so_far = sum_model / max(processed, 1)

        obj: Dict[str, Any] = {
            "overall": compile_rate_so_far,
            "pass1": compile_rate_so_far,
            "pass5": compile_rate_so_far,
            "compileRate": compile_rate_so_far,
            "avgTimeSec": avg_compile_so_far,
            "tokensPerTask": 0,
            "usdPerTask": 0.0,
            "categories": {},
            "levels": {},
            "meta": {
                "status": "running",
                "runId": run_id,
                "runDir": str(LOG_DIR),
                "tasks": len(tasks),
                "processed": processed,
                "passed": passed,
                "progress": prog,
                "elapsedSec": time.time() - t_start,
                "avgModelSecSoFar": avg_model_so_far,
                "avgCompileSecSoFar": avg_compile_so_far,
                "lastTask": last_task,
                "lastOk": last_ok,
                "lastErr": last_err,
                "benchmarkDir": str(benchmark_dir),
                "dockerNetwork": _get_env_str("SHADOWBENCH_DOCKER_NETWORK", "none"),
                "formalizationMode": formalization_mode,
                "enforceTargetSignature": enforce_sig,
                "enforceTargetSignatureEffective": enforce_sig_effective,
                "eval:": resolved_eval,
            },
        }
        _write_progress_out(args.out, obj)

    with tempfile.TemporaryDirectory(prefix="abm_eval_") as td:
        tdir = Path(td)

        for i, task in enumerate(tasks, 1):
            stem = _safe_stem(task.task_id)
            use_target_template = (formalization_mode != "full") and bool(task.target_code)
            completion_mode = bool(use_target_template)

            if formalization_mode == "full":
                mode_str = "full"
            else:
                mode_str = "completion" if completion_mode else "scratch"

            prompt = build_prompt(task, use_target_template=use_target_template)

            raw, model_sec, model_err = call_model(
                model_argv, model_env, prompt, timeout_sec=model_timeout
            )

            # Always dump raw (helps debugging even on error)
            (LOG_DIR / f"{stem}.raw.txt").write_text(raw or "", encoding="utf-8", errors="replace")

            ok = False
            comp_sec = 0.0
            err_short = ""

            if model_err:
                msg = f"MODEL_ERROR: {model_err}"
                (LOG_DIR / f"{stem}.log").write_text(msg + "\n", encoding="utf-8", errors="replace")
                if log_per_task:
                    logs.append(f"[{i}/{len(tasks)}] {task.task_id} ok=False model={model_sec:.2f}s compile=0.00s mode={mode_str}")
                    logs.append(msg)
                    logs.append("")
                results.append(TaskResult(
                    task_id=task.task_id,
                    ok=False,
                    area=task.area,
                    level_bucket=task.level_bucket,
                    compile_sec=0.0,
                    model_sec=model_sec,
                    err=msg,
                ))
                ok = False
                err_short = msg[:500].replace("\n", " ")
                processed += 1
                sum_model += model_sec
                _maybe_emit_progress_line(i, task.task_id, ok, model_sec, comp_sec, mode_str)
                _maybe_write_progress_json(i, task.task_id, ok, err_short)
                continue

            code = _extract_lean_code(raw)
            (LOG_DIR / f"{stem}.extracted.lean").write_text(code or "", encoding="utf-8", errors="replace")

            if not (code or "").strip():
                msg = "EMPTY_EXTRACTED_CODE"
                (LOG_DIR / f"{stem}.log").write_text(
                    "EARLY EXIT: extracted Lean code is empty.\nSee .raw.txt and .extracted.lean\n",
                    encoding="utf-8",
                    errors="replace",
                )
                if log_per_task:
                    logs.append(f"[{i}/{len(tasks)}] {task.task_id} ok=False model={model_sec:.2f}s compile=0.00s mode={mode_str}")
                    logs.append(msg)
                    logs.append("")
                results.append(TaskResult(
                    task_id=task.task_id,
                    ok=False,
                    area=task.area,
                    level_bucket=task.level_bucket,
                    compile_sec=0.0,
                    model_sec=model_sec,
                    err=msg,
                ))
                ok = False
                err_short = msg
                processed += 1
                sum_model += model_sec
                _maybe_emit_progress_line(i, task.task_id, ok, model_sec, comp_sec, mode_str)
                _maybe_write_progress_json(i, task.task_id, ok, err_short)
                continue

            # Completion-mode guardrail: ensure target signature unchanged
            if completion_mode and enforce_sig_effective and task.target_kind and task.target_decl and task.target_sig:
                out_sig = _extract_decl_signature(code, kind=task.target_kind, name=task.target_decl)
                if not out_sig:
                    msg = f"TARGET_DECL_NOT_FOUND: expected `{task.target_kind} {task.target_decl}` in output"
                    (LOG_DIR / f"{stem}.log").write_text(msg + "\n", encoding="utf-8", errors="replace")
                    if log_per_task:
                        logs.append(f"[{i}/{len(tasks)}] {task.task_id} ok=False model={model_sec:.2f}s compile=0.00s mode={mode_str}")
                        logs.append(msg)
                        logs.append("")
                    results.append(TaskResult(
                        task_id=task.task_id,
                        ok=False,
                        area=task.area,
                        level_bucket=task.level_bucket,
                        compile_sec=0.0,
                        model_sec=model_sec,
                        err=msg,
                    ))
                    ok = False
                    err_short = msg[:500].replace("\n", " ")
                    processed += 1
                    sum_model += model_sec
                    _maybe_emit_progress_line(i, task.task_id, ok, model_sec, comp_sec, mode_str)
                    _maybe_write_progress_json(i, task.task_id, ok, err_short)
                    continue

                if _normalize_ws(out_sig) != _normalize_ws(task.target_sig):
                    msg = "TARGET_DECL_SIGNATURE_MISMATCH"
                    detail = (
                        msg + "\n\n"
                        + "EXPECTED (from target_code):\n" + task.target_sig + "\n\n"
                        + "GOT (from model output):\n" + (out_sig or "") + "\n"
                    )
                    (LOG_DIR / f"{stem}.log").write_text(detail, encoding="utf-8", errors="replace")
                    if log_per_task:
                        logs.append(f"[{i}/{len(tasks)}] {task.task_id} ok=False model={model_sec:.2f}s compile=0.00s mode={mode_str}")
                        logs.append(msg)
                        logs.append("")
                    results.append(TaskResult(
                        task_id=task.task_id,
                        ok=False,
                        area=task.area,
                        level_bucket=task.level_bucket,
                        compile_sec=0.0,
                        model_sec=model_sec,
                        err=msg,
                    ))
                    ok = False
                    err_short = msg
                    processed += 1
                    sum_model += model_sec
                    _maybe_emit_progress_line(i, task.task_id, ok, model_sec, comp_sec, mode_str)
                    _maybe_write_progress_json(i, task.task_id, ok, err_short)
                    continue

            wrapped = wrap_for_compile(code, task=task, completion_mode=completion_mode)
            (LOG_DIR / f"{stem}.wrapped.lean").write_text(wrapped, encoding="utf-8", errors="replace")

            # Compile in Docker
            lean_file = tdir / f"{stem}.lean"
            lean_file.write_text(wrapped, encoding="utf-8", errors="replace")

            ok, comp_sec, comp_log = compile_in_docker(
                lean_file, benchmark_dir=benchmark_dir, timeout_sec=compile_timeout
            )
            (LOG_DIR / f"{stem}.log").write_text(comp_log or "", encoding="utf-8", errors="replace")

            if log_per_task:
                logs.append(
                    f"[{i}/{len(tasks)}] {task.task_id} ok={ok} "
                    f"model={model_sec:.2f}s compile={comp_sec:.2f}s mode={mode_str}"
                )
                if not ok:
                    logs.append((comp_log or "")[:1200])
                    logs.append("")

            results.append(TaskResult(
                task_id=task.task_id,
                ok=ok,
                area=task.area,
                level_bucket=task.level_bucket,
                compile_sec=comp_sec,
                model_sec=model_sec,
                err=("" if ok else (comp_log or "compile failed")),
            ))

            processed += 1
            sum_model += model_sec
            sum_compile += comp_sec
            if ok:
                passed += 1

            if not ok:
                err_short = (comp_log or "compile failed")[:500].replace("\n", " ")

            _maybe_emit_progress_line(i, task.task_id, ok, model_sec, comp_sec, mode_str)
            _maybe_write_progress_json(i, task.task_id, ok, err_short)

    total = len(results)
    passed_final = sum(1 for r in results if r.ok)
    compile_rate = 100.0 * passed_final / max(total, 1)

    # Aggregate by area
    by_area: Dict[str, List[TaskResult]] = {}
    for r in results:
        by_area.setdefault(r.area, []).append(r)
    area_scores: Dict[str, float] = {}
    for a, rs in by_area.items():
        area_scores[a] = 100.0 * sum(1 for x in rs if x.ok) / max(len(rs), 1)

    # Aggregate by level bucket
    by_level: Dict[str, List[TaskResult]] = {}
    for r in results:
        by_level.setdefault(r.level_bucket, []).append(r)
    level_scores: Dict[str, float] = {}
    for lv, rs in by_level.items():
        level_scores[lv] = 100.0 * sum(1 for x in rs if x.ok) / max(len(rs), 1)

    # Timing stats
    avg_compile = sum(r.compile_sec for r in results) / max(total, 1)
    avg_model = sum(r.model_sec for r in results) / max(total, 1)

    out_obj: Dict[str, Any] = {
        "overall": compile_rate,
        "pass1": compile_rate,
        "pass5": compile_rate,
        "compileRate": compile_rate,
        "avgTimeSec": avg_compile,
        "tokensPerTask": 0,
        "usdPerTask": 0.0,
        "categories": area_scores,
        "levels": level_scores,
        "meta": {
            "status": "done",
            "runId": run_id,
            "runDir": str(LOG_DIR),
            "tasks": total,
            "passed": passed_final,
            "progress": 1.0,
            "avgModelSec": avg_model,
            "benchmarkDir": str(benchmark_dir),
            "dockerNetwork": _get_env_str("SHADOWBENCH_DOCKER_NETWORK", "none"),
            "formalizationMode": formalization_mode,
            "enforceTargetSignature": enforce_sig,
            "enforceTargetSignatureEffective": enforce_sig_effective,
            "eval:": resolved_eval,
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out_obj, indent=2, sort_keys=True), encoding="utf-8")


    # Archive a copy of the final result + spec alongside the per-task artifacts.
    try:
        _atomic_write_text(LOG_DIR / "result.json", json.dumps(out_obj, indent=2, sort_keys=True))
    except Exception as e:
        _emit(f"[warn] failed to write {LOG_DIR / 'result.json'}: {e}")

    try:
        _atomic_write_text(LOG_DIR / "submission_spec.json", json.dumps(submission_spec, indent=2, sort_keys=True))
    except Exception as e:
        _emit(f"[warn] failed to write {LOG_DIR / 'submission_spec.json'}: {e}")

    # Optional: store per-task outcomes for later inspection / admin UI.
    try:
        task_rows = [
            {
                "task_id": r.task_id,
                "ok": r.ok,
                "area": r.area,
                "level_bucket": r.level_bucket,
                "compile_sec": r.compile_sec,
                "model_sec": r.model_sec,
                "err": r.err,
            }
            for r in results
        ]
        _atomic_write_text(LOG_DIR / "task_results.json", json.dumps(task_rows, indent=2, sort_keys=True))
    except Exception:
        pass

    _emit(f"OK wrote metrics to {args.out} (overall={compile_rate:.1f}, passed={passed_final}/{total})")

    # Persist the human-readable run log output (best-effort).
    try:
        if logs:
            _atomic_write_text(LOG_DIR / "run.log", "\n".join(logs) + "\n")
    except Exception:
        pass

    if logs:
        _emit("\n--- RUN LOG ---")
        for line in logs[:2000]:
            _emit(line)


if __name__ == "__main__":
    main()
