"""BEq / BEq+ evaluator for naive_prompting results.

Usage:
    # Evaluate a specific run
    python -m scripts.beq_eval --run-id claude-sonnet-4-6-4096-6edc4b

    # Evaluate all best-per-model runs (requires beq_select_runs to have been run first)
    python -m scripts.beq_eval --all

    # Smoke test: only process first N tasks
    python -m scripts.beq_eval --run-id <ID> --max-tasks 5

    # Verbose per-task proof output
    python -m scripts.beq_eval --run-id <ID> --verbose

Results are written to:
    results/naive_prompting/{run_id}/beq_results.json
"""

import argparse
import json
import os
import time
from pathlib import Path

# Ensure elan/lean toolchain is on PATH
os.environ.setdefault("PATH", "")
os.environ["PATH"] = os.path.expanduser("~/.elan/bin") + ":" + os.environ["PATH"]

from lean_interact import AutoLeanServer, Command, LeanREPLConfig
from lean_interact.interface import LeanError
from lean_interact.project import LocalProject
from rich.console import Console
from tqdm import tqdm

from lean_interact.utils import extract_last_theorem
from scripts._beq_plus_vendored import DEFAULT_TIMEOUT, beql, beq_plus
from scripts.beq_pair_loader import load_pairs_for_run

REPO_ROOT = Path(__file__).parent.parent
NAIVE_PROMPTING_DIR = REPO_ROOT / "results" / "naive_prompting"
LEAN_PROJECT_DIR = REPO_ROOT / "leanproblems"
BEQ_RUNS_JSON = NAIVE_PROMPTING_DIR / "analysis" / "beq_runs.json"

console = Console()


LAKE_PATH = os.path.expanduser("~/.elan/bin/lake")


def make_lean_server() -> AutoLeanServer:
    """Create a LeanServer using the local leanproblems project (Lean 4.26 + Mathlib)."""
    config = LeanREPLConfig(
        project=LocalProject(directory=str(LEAN_PROJECT_DIR), lake_path=LAKE_PATH, auto_build=False),
        lake_path=LAKE_PATH,
    )
    return AutoLeanServer(config=config)


def evaluate_run(
    run_id: str,
    max_tasks: int | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    verbose: bool = False,
    force: bool = False,
) -> dict:
    """
    Run BEq / BEq+ evaluation for a single run.

    Returns the aggregated result dict (also saved to disk).
    """
    run_dir = NAIVE_PROMPTING_DIR / run_id
    out_path = run_dir / "beq_results.json"

    if not force and out_path.exists():
        console.print(f"[yellow]Skipping {run_id} — beq_results.json already exists. Use --force to rerun.[/]")
        with open(out_path) as f:
            return json.load(f)

    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    console.rule(f"[bold]{run_id}")
    console.print(f"Loading pairs from {run_dir.name}...")

    pairs = load_pairs_for_run(run_id)
    if max_tasks is not None:
        pairs = pairs[:max_tasks]

    matchable = [p for p in pairs if p["skip_reason"] is None]
    console.print(f"  Total tasks: {len(pairs)}, matchable: {len(matchable)}, "
                  f"skipped: {len(pairs) - len(matchable)}")

    server = make_lean_server()

    # Pre-warm Mathlib: import once, cache the env with a stable negative ID.
    # The session cache persists the env across REPL restarts (e.g. OOM kills).
    # This avoids re-loading all Mathlib oleans on each REPL call (~30s overhead).
    console.print("  Warming up Mathlib (may take ~30s)...")
    _warmup = server.run(Command(cmd="import Mathlib"), timeout=300, add_to_session_cache=True)
    if isinstance(_warmup, LeanError):
        raise RuntimeError(f"Failed to load Mathlib in REPL: {_warmup}")
    mathlib_env = _warmup.env  # negative stable ID from session cache
    console.print(f"  Lean server initialised (Mathlib env={mathlib_env}).")

    task_results = []
    stats = {"compile_both": 0, "beq": 0, "beq_plus": 0, "skipped": 0, "total": len(pairs)}

    for pair in tqdm(pairs, desc=run_id, unit="task"):
        task_id = pair["task_id"]
        if pair["skip_reason"]:
            task_results.append({
                "task_id": task_id,
                "area": pair["area"],
                "level": pair["level"],
                "skipped": True,
                "skip_reason": pair["skip_reason"],
                "beq": False,
                "beq_plus": False,
            })
            stats["skipped"] += 1
            continue

        ref_full = pair["ref_content"]
        cand_full = pair["cand_content"]

        # Split reference into preamble (opens, variables, defs) and theorem statement.
        # Use the preamble as src_header for both theorems, passing only the theorem statements
        # to beql/beq_plus. This prevents duplicate-import errors when harness concatenates.
        # NOTE: We use mathlib_env (pre-loaded) so NO import statements are needed here.
        # All imports are stripped; Mathlib is available via the pre-warmed env.
        try:
            ref_thm_idx = extract_last_theorem(ref_full)
            raw_preamble = ref_full[:ref_thm_idx]
            # Strip import lines — Mathlib is already in the pre-warmed env (mathlib_env)
            preamble_lines = [
                ln for ln in raw_preamble.splitlines()
                if not ln.strip().startswith("import ")
            ]
            src_header = "\n".join(preamble_lines).rstrip()
            ref = ref_full[ref_thm_idx:]
        except Exception:
            src_header = ""
            ref = ref_full

        try:
            cand_thm_idx = extract_last_theorem(cand_full)
            cand = cand_full[cand_thm_idx:]
        except Exception:
            cand = cand_full

        t0 = time.time()
        beq_result = False
        beq_plus_result = False
        error = None

        try:
            beq_result = beql(ref, cand, src_header, server, timeout_per_proof=timeout, verbose=verbose, mathlib_env=mathlib_env)
            if beq_result:
                beq_plus_result = True  # BEqL implies BEq+
            else:
                beq_plus_result = beq_plus(ref, cand, src_header, server, timeout_per_proof=timeout, verbose=verbose, mathlib_env=mathlib_env)
        except Exception as e:
            error = str(e)
            console.log(f"[red]Error on {task_id}: {e}[/]")

        elapsed = round(time.time() - t0, 1)

        if beq_result:
            stats["beq"] += 1
        if beq_plus_result:
            stats["beq_plus"] += 1

        task_results.append({
            "task_id": task_id,
            "area": pair["area"],
            "level": pair["level"],
            "skipped": False,
            "skip_reason": None,
            "beq": beq_result,
            "beq_plus": beq_plus_result,
            "duration_seconds": elapsed,
            "error": error,
        })

        if verbose:
            status = "BEq" if beq_result else ("BEq+" if beq_plus_result else "FAIL")
            console.print(f"  [{status}] {task_id} ({elapsed}s)")

    attempted = stats["total"] - stats["skipped"]
    result = {
        "run_id": run_id,
        "total_tasks": stats["total"],
        "skipped_tasks": stats["skipped"],
        "attempted_tasks": attempted,
        "beq_passed": stats["beq"],
        "beq_plus_passed": stats["beq_plus"],
        "beq_rate": round(stats["beq"] / attempted * 100, 2) if attempted else 0.0,
        "beq_plus_rate": round(stats["beq_plus"] / attempted * 100, 2) if attempted else 0.0,
        "tasks": task_results,
    }

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    console.print(f"\n  BEq:  {stats['beq']}/{attempted} = {result['beq_rate']}%")
    console.print(f"  BEq+: {stats['beq_plus']}/{attempted} = {result['beq_plus_rate']}%")
    console.print(f"  Saved to {out_path}")

    return result


def main():
    parser = argparse.ArgumentParser(description="BEq / BEq+ evaluation for naive_prompting runs")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run-id", type=str, help="Evaluate a specific run")
    group.add_argument("--all", action="store_true", help="Evaluate all best-per-model runs from beq_runs.json")
    parser.add_argument("--max-tasks", type=int, default=None, help="Limit number of tasks per run (for debugging)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Per-direction proof timeout (seconds)")
    parser.add_argument("--verbose", action="store_true", help="Print per-task proof details")
    parser.add_argument("--force", action="store_true", help="Re-evaluate even if beq_results.json exists")
    args = parser.parse_args()

    if args.run_id:
        evaluate_run(args.run_id, args.max_tasks, args.timeout, args.verbose, args.force)

    elif args.all:
        if not BEQ_RUNS_JSON.exists():
            console.print(f"[red]beq_runs.json not found: {BEQ_RUNS_JSON}[/]")
            console.print("Run: python -m scripts.beq_select_runs")
            return

        with open(BEQ_RUNS_JSON) as f:
            selected = json.load(f)["selected_runs"]

        console.print(f"Evaluating {len(selected)} runs...")
        for run_info in selected:
            try:
                evaluate_run(
                    run_info["run_id"], args.max_tasks, args.timeout, args.verbose, args.force
                )
            except Exception as e:
                console.print(f"[red]Failed on {run_info['run_id']}: {e}[/]")


if __name__ == "__main__":
    main()
