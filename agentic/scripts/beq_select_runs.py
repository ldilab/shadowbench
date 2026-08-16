"""Select the best-performing run per model from naive_prompting results.

Usage:
    python -m scripts.beq_select_runs [--out PATH]

Reads results/naive_prompting/runs.json and the directories on disk, then
picks the run with the highest compile-pass rate per model family.

Output: results/naive_prompting/analysis/beq_runs.json
"""

import argparse
import json
import os
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
NAIVE_PROMPTING_DIR = REPO_ROOT / "results" / "naive_prompting"
RUNS_JSON = NAIVE_PROMPTING_DIR / "runs.json"
OUTPUT_JSON = NAIVE_PROMPTING_DIR / "analysis" / "beq_runs.json"


def normalize_model_name(model: str) -> str:
    """Collapse variant suffixes to a canonical model key."""
    # Strip proxy prefix (op/, openai/, etc.)
    if "/" in model:
        model = model.split("/", 1)[1]
    # Strip suffix variants like :floor, :latest
    if ":" in model:
        model = model.rsplit(":", 1)[0]
    return model


def _run_has_data(run_dir: Path, run_id: str) -> bool:
    """Check if a run has extracted lean files (tar.gz or directory)."""
    tar_gz = run_dir / f"{run_id}.tar.gz"
    if tar_gz.exists():
        return True
    # Check for .extracted.lean files directly or in subdirectory
    if list(run_dir.glob("*.extracted.lean")):
        return True
    for sub in run_dir.iterdir():
        if sub.is_dir() and list(sub.glob("*.extracted.lean")):
            return True
    return False


def select_best_runs(runs_json_path: Path, naive_dir: Path) -> list[dict]:
    with open(runs_json_path) as f:
        data = json.load(f)

    runs = data["runs"]
    best: dict[str, dict] = {}  # canonical_model -> best run entry

    for run in runs:
        run_id = run["id"]
        run_dir = naive_dir / run_id
        if not run_dir.exists() or not _run_has_data(run_dir, run_id):
            continue

        model_raw = run.get("env", {}).get("VLLM_MODEL", "")
        canonical = normalize_model_name(model_raw)

        meta = run.get("meta", {})
        passed = meta.get("passed", 0)
        tasks = meta.get("tasks", 1) or 1
        pass_rate = passed / tasks

        env = run.get("env", {})
        entry = {
            "run_id": run_id,
            "model_raw": model_raw,
            "model_canonical": canonical,
            "max_tokens": env.get("VLLM_MAX_TOKENS"),
            "temperature": env.get("VLLM_TEMPERATURE"),
            "passed": passed,
            "tasks": tasks,
            "pass_rate": round(pass_rate * 100, 2),
        }

        if canonical not in best or pass_rate > best[canonical]["pass_rate"] / 100:
            best[canonical] = entry

    selected = sorted(best.values(), key=lambda x: x["model_canonical"])
    return selected


def main():
    parser = argparse.ArgumentParser(description="Select best-per-model runs for BEq evaluation")
    parser.add_argument("--out", type=str, default=str(OUTPUT_JSON))
    args = parser.parse_args()

    selected = select_best_runs(RUNS_JSON, NAIVE_PROMPTING_DIR)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({"selected_runs": selected}, f, indent=2, ensure_ascii=False)

    print(f"Selected {len(selected)} runs:")
    for r in selected:
        print(f"  {r['model_canonical']:40} {r['pass_rate']:5.1f}%  {r['run_id']}")
    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()
