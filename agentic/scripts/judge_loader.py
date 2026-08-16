"""Load per-task judge inputs for the LLM-as-judge evaluator.

For each candidate `.extracted.lean` in a run directory, joins:
  - informal statement / optional NL proof   (from shadowbench-benchmark text.md)
  - reference formal statement with `sorry`  (from shadowbench-benchmark meta.json target_code)
  - compile-success flag                     (task_results.json `ok`)
  - BEq status                               (beq_results.json, if present)

Usage (self-test):
    python -m scripts.judge_loader --run-id <run_id> [--scope compiled|beq|all] [--max 5]
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

from scripts.beq_pair_loader import TASK_FILENAME_RE

REPO_ROOT = Path(__file__).resolve().parent.parent
NAIVE_PROMPTING_DIR = REPO_ROOT / "results" / "naive_prompting"
SHADOWBENCH_DATA = Path(
    os.environ.get("SHADOWBENCH_BENCHMARK_DATA", REPO_ROOT / "non_agentic" / "shadowbench-benchmark" / "data")
)


@dataclass
class JudgeItem:
    task_id: str            # "algebra/L1/alg_gen_L1_005"
    area: str               # "algebra"
    level: str              # "L1"
    problem_id: str         # "alg_gen_L1_005"
    informal_text: str | None
    has_nl_proof: bool
    formal_ref: str | None  # meta.target_code (statement with `sorry`)
    candidate: str | None   # content of .extracted.lean
    compile_ok: bool | None
    beq: bool | None
    beq_plus: bool | None
    skip_reason: str | None


def _problem_dir(area: str, level: str, problem_id: str) -> Path:
    return SHADOWBENCH_DATA / area / level / problem_id


def load_benchmark_problem(area: str, level: str, problem_id: str) -> dict | None:
    """Return {text_md, target_code, types, meta} or None if the problem is missing."""
    pdir = _problem_dir(area, level, problem_id)
    text_path = pdir / "text.md"
    meta_path = pdir / "meta.json"
    if not meta_path.exists():
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    text_md = text_path.read_text(encoding="utf-8") if text_path.exists() else meta.get("text")
    types = meta.get("types") or []
    if isinstance(types, str):
        types = [t.strip() for t in types.split(";") if t.strip()]
    return {
        "text_md": text_md,
        "target_code": meta.get("target_code") or meta.get("lean", {}).get("code"),
        "types": types,
        "meta": meta,
    }


def _compile_ok_from_logs(run_dir: Path) -> dict[str, bool]:
    """Derive compile-ok from per-task .log files: no 'error:' lines => ok."""
    out: dict[str, bool] = {}
    # logs may live directly under run_dir or inside a single nested subdir
    log_dirs = [run_dir]
    for sub in run_dir.iterdir():
        if sub.is_dir() and any(sub.glob("*.log")):
            log_dirs.append(sub)
    for ld in log_dirs:
        for log_path in ld.glob("*.log"):
            m = TASK_FILENAME_RE.match(log_path.stem + ".extracted.lean")
            if not m:
                continue
            tid = f"{m.group('area')}/{m.group('level')}/{m.group('basename')}"
            text = log_path.read_text(encoding="utf-8", errors="replace")
            has_error = any("error:" in line for line in text.splitlines())
            out[tid] = not has_error
    return out


def load_compile_ok(run_dir: Path) -> dict[str, bool]:
    """Return {task_id (slash form) -> ok}. Missing file -> empty dict.

    Precedence: task_results.json → result.json["problems"] → per-task .log scan.
    """
    path = run_dir / "task_results.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return {item["task_id"]: bool(item.get("ok")) for item in data}
    rpath = run_dir / "result.json"
    if rpath.exists():
        r = json.loads(rpath.read_text(encoding="utf-8"))
        problems = r.get("problems") or []
        if problems:
            return {item["task_id"]: bool(item.get("ok")) for item in problems}
    return _compile_ok_from_logs(run_dir)


def load_beq_status(run_dir: Path) -> dict[str, dict]:
    """Return {task_id (slash form) -> {beq, beq_plus, skipped}}."""
    path = run_dir / "beq_results.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for item in data.get("tasks", []):
        # beq_results uses underscore form ("algebra_L1_alg_gen_L1_005"); normalise to slash form.
        tid_underscore = item["task_id"]
        m = TASK_FILENAME_RE.match(tid_underscore + ".extracted.lean")
        if m:
            tid = f"{m.group('area')}/{m.group('level')}/{m.group('basename')}"
        else:
            tid = tid_underscore
        out[tid] = {
            "beq": bool(item.get("beq")),
            "beq_plus": bool(item.get("beq_plus")),
            "skipped": bool(item.get("skipped")),
        }
    return out


def _iter_candidate_files(run_dir: Path) -> Iterable[Path]:
    """Yield .extracted.lean files from run_dir or its single sub-layout."""
    direct = list(run_dir.glob("*.extracted.lean"))
    if direct:
        yield from direct
        return
    for sub in run_dir.iterdir():
        if sub.is_dir():
            for p in sub.glob("*.extracted.lean"):
                yield p


def load_judge_pairs(run_id: str, scope: str = "compiled") -> list[JudgeItem]:
    """Join candidate files + benchmark ground truth + compile flag + BEq status."""
    if scope not in {"compiled", "beq", "all"}:
        raise ValueError(f"unknown scope: {scope!r}")

    run_dir = NAIVE_PROMPTING_DIR / run_id
    if not run_dir.exists():
        raise FileNotFoundError(f"run directory not found: {run_dir}")

    compile_ok_map = load_compile_ok(run_dir)
    beq_map = load_beq_status(run_dir)

    items: list[JudgeItem] = []
    for cand_path in sorted(_iter_candidate_files(run_dir)):
        m = TASK_FILENAME_RE.match(cand_path.name)
        if not m:
            continue
        area, level, basename = m.group("area"), m.group("level"), m.group("basename")
        task_id = f"{area}/{level}/{basename}"
        bench = load_benchmark_problem(area, level, basename)
        beq_info = beq_map.get(task_id, {})
        compile_ok = compile_ok_map.get(task_id)
        skip_reason: str | None = None
        candidate = cand_path.read_text(encoding="utf-8")

        if bench is None:
            skip_reason = f"no benchmark data at {_problem_dir(area, level, basename)}"
        elif bench.get("target_code") is None:
            skip_reason = "benchmark meta has no target_code"

        has_nl_proof = bench is not None and any("proof" in t for t in bench["types"])
        items.append(JudgeItem(
            task_id=task_id,
            area=area,
            level=level,
            problem_id=basename,
            informal_text=(bench["text_md"] if bench else None),
            has_nl_proof=has_nl_proof,
            formal_ref=(bench["target_code"] if bench else None),
            candidate=candidate,
            compile_ok=compile_ok,
            beq=beq_info.get("beq"),
            beq_plus=beq_info.get("beq_plus"),
            skip_reason=skip_reason,
        ))

    if scope == "compiled":
        items = [i for i in items if i.skip_reason is None and i.compile_ok]
    elif scope == "beq":
        items = [i for i in items if i.skip_reason is None and i.beq]
    else:  # "all"
        items = [i for i in items if i.skip_reason is None]

    return items


def _main() -> None:
    ap = argparse.ArgumentParser(description="Self-test for judge_loader")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--scope", choices=["compiled", "beq", "all"], default="compiled")
    ap.add_argument("--max", type=int, default=5)
    args = ap.parse_args()

    items = load_judge_pairs(args.run_id, args.scope)
    print(f"run={args.run_id} scope={args.scope}  loaded={len(items)}")
    for it in items[: args.max]:
        d = asdict(it)
        # elide big strings for summary output
        for k in ("informal_text", "formal_ref", "candidate"):
            v = d.get(k)
            if isinstance(v, str):
                d[k] = f"<{len(v)} chars>"
        print(json.dumps(d, ensure_ascii=False))


if __name__ == "__main__":
    _main()
