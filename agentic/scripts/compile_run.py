"""Compile every *.wrapped.lean in a naive_prompting run dir via lean_interact.

Useful for runs produced by `scripts/two_stage_eval.py` that don't compile
in-line — and for any run dir that lacks per-task compile flags. Updates
`task_results.json` (sets `ok`, `compile_sec`, `err`) and recomputes
`result.json` headline metrics (`compileRate`, `overall`, `pass1`).

Usage:
    python -m scripts.compile_run --run-id <run_id>
    python -m scripts.compile_run --run-id <run_id> --max-tasks 5 --force
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

os.environ.setdefault("PATH", "")
os.environ["PATH"] = os.path.expanduser("~/.elan/bin") + ":" + os.environ["PATH"]

from lean_interact import AutoLeanServer, Command, LeanREPLConfig
from lean_interact.interface import LeanError
from lean_interact.project import LocalProject
from rich.console import Console
from tqdm import tqdm

REPO_ROOT = Path(__file__).resolve().parent.parent
NAIVE_PROMPTING_DIR = REPO_ROOT / "results" / "naive_prompting"
LEAN_PROJECT_DIR = REPO_ROOT / "leanproblems"
LAKE_PATH = os.path.expanduser("~/.elan/bin/lake")

console = Console()


def make_server() -> AutoLeanServer:
    config = LeanREPLConfig(
        project=LocalProject(
            directory=str(LEAN_PROJECT_DIR), lake_path=LAKE_PATH, auto_build=False
        ),
        lake_path=LAKE_PATH,
    )
    return AutoLeanServer(config=config)


def _is_error(resp) -> tuple[bool, str]:
    """Return (has_error, error_text). Looks at LeanError + diagnostics severity."""
    if isinstance(resp, LeanError):
        return True, str(resp)
    msgs = getattr(resp, "messages", None) or []
    errs = []
    for m in msgs:
        sev = getattr(m, "severity", None)
        # lean_interact severity: "error" / "warning" / "info"; warningAsError makes both error
        if str(sev).lower() == "error":
            errs.append(getattr(m, "data", str(m)))
    if errs:
        return True, "\n".join(errs)
    # sorries are also fail under set_option warningAsError; lean_interact may report .sorries
    sorries = getattr(resp, "sorries", None) or []
    if sorries:
        return True, f"sorry remains in proof ({len(sorries)} site(s))"
    return False, ""


def discover_wrapped(run_dir: Path) -> list[Path]:
    out = sorted(run_dir.glob("*.wrapped.lean"))
    if out:
        return out
    for sub in run_dir.iterdir():
        if sub.is_dir():
            out.extend(sub.glob("*.wrapped.lean"))
    return sorted(out)


def parse_task_id(stem: str) -> tuple[str, str, str] | None:
    """`algebra_L1_alg_gen_L1_005` → ('algebra', 'L1', 'alg_gen_L1_005'). Falls back to None."""
    import re
    m = re.match(r"^(?P<area>[^_]+(?:-[^_]+)*)_(?P<level>L[1-4])_(?P<basename>.+)$", stem)
    if not m:
        return None
    return m.group("area"), m.group("level"), m.group("basename")


def load_existing_task_results(run_dir: Path) -> dict[str, dict]:
    p = run_dir / "task_results.json"
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {item["task_id"]: item for item in data}


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile *.wrapped.lean in a run dir")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--max-tasks", type=int, default=None)
    ap.add_argument("--timeout", type=int, default=180,
                    help="Per-file compile timeout (seconds)")
    ap.add_argument("--force", action="store_true",
                    help="Recompile tasks that already have ok set in task_results.json")
    args = ap.parse_args()

    run_dir = NAIVE_PROMPTING_DIR / args.run_id
    if not run_dir.exists():
        raise FileNotFoundError(run_dir)

    wrapped = discover_wrapped(run_dir)
    if args.max_tasks is not None:
        wrapped = wrapped[: args.max_tasks]
    if not wrapped:
        console.print(f"[red]No *.wrapped.lean files in {run_dir}[/]")
        return

    existing = load_existing_task_results(run_dir)

    server = make_server()
    console.print(f"  Warming up Mathlib (~30s)...")
    warm = server.run(Command(cmd="import Mathlib"), timeout=300, add_to_session_cache=True)
    if isinstance(warm, LeanError):
        raise RuntimeError(f"Failed to load Mathlib: {warm}")
    mathlib_env = warm.env
    console.print(f"  Lean server initialised (env={mathlib_env}).")

    new_results: list[dict] = []
    n_ok = 0
    for wp in tqdm(wrapped, desc=args.run_id, unit="task"):
        stem = wp.name.removesuffix(".wrapped.lean")
        parsed = parse_task_id(stem)
        if parsed is None:
            continue
        area, level, basename = parsed
        task_id = f"{area}/{level}/{basename}"

        prior = existing.get(task_id)
        if prior is not None and prior.get("ok") is not None and not args.force:
            new_results.append(prior)
            if prior.get("ok"):
                n_ok += 1
            continue

        code = wp.read_text(encoding="utf-8")
        # strip leading `import ...` lines — Mathlib already pre-warmed
        lines = code.splitlines()
        body_start = 0
        for i, ln in enumerate(lines):
            if ln.strip().startswith("import "):
                body_start = i + 1
            elif ln.strip() == "":
                continue
            else:
                break
        cmd_body = "\n".join(lines[body_start:])

        t0 = time.time()
        try:
            resp = server.run(
                Command(cmd=cmd_body, env=mathlib_env),
                timeout=args.timeout,
            )
            has_err, err_text = _is_error(resp)
        except Exception as e:
            has_err, err_text = True, f"{type(e).__name__}: {e}"
        elapsed = round(time.time() - t0, 2)
        ok = not has_err

        # write log
        log_path = wp.parent / f"{stem}.log"
        log_path.write_text(err_text if err_text else "", encoding="utf-8")

        rec = {
            "task_id": task_id,
            "area": area,
            "level_bucket": level,
            "ok": ok,
            "compile_sec": elapsed,
            "model_sec": (prior or {}).get("model_sec"),
            "err": err_text[:500] if err_text else "",
        }
        new_results.append(rec)
        if ok:
            n_ok += 1

    # write task_results
    (run_dir / "task_results.json").write_text(
        json.dumps(new_results, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    n = len(new_results)
    rate = round(n_ok / n * 100, 2) if n else 0.0
    # update result.json (preserve any other fields)
    rj_path = run_dir / "result.json"
    result = json.loads(rj_path.read_text(encoding="utf-8")) if rj_path.exists() else {}
    result["compileRate"] = rate
    result["overall"] = rate
    result["pass1"] = rate
    result["compiled_tasks"] = n
    result["compiled_passed"] = n_ok
    result["problems"] = [{"task_id": r["task_id"], "ok": r["ok"],
                            "area": r["area"], "level": r["level_bucket"],
                            "compile_sec": r["compile_sec"]} for r in new_results]
    rj_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    console.print(f"\n[green]{args.run_id}: {n_ok}/{n} = {rate}% compile-ok[/]")


if __name__ == "__main__":
    main()
