"""Generate BEq / BEq+ summary tables from beq_results.json files.

Usage:
    python -m scripts.beq_summary

Reads:
    results/naive_prompting/analysis/beq_runs.json        (which runs to include)
    results/naive_prompting/{run_id}/beq_results.json     (per-run BEq results)
    results/naive_prompting/runs.json                     (model metadata)

Writes:
    results/naive_prompting/analysis/beq_summary_table.md
    results/naive_prompting/analysis/beq_summary_table.csv
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
NAIVE_DIR = REPO_ROOT / "results" / "naive_prompting"
BEQ_RUNS_JSON = NAIVE_DIR / "analysis" / "beq_runs.json"
RUNS_JSON = NAIVE_DIR / "runs.json"
OUT_MD = NAIVE_DIR / "analysis" / "beq_summary_table.md"
OUT_CSV = NAIVE_DIR / "analysis" / "beq_summary_table.csv"

AREAS = ["algebra", "analysis", "college-math-competition", "geometry", "topology"]
LEVELS = ["L1", "L2", "L3"]

AREA_DISPLAY = {
    "algebra": "algebra",
    "analysis": "analysis",
    "college-math-competition": "cmc",
    "geometry": "geometry",
    "topology": "topology",
}


def load_runs_meta() -> dict[str, dict]:
    with open(RUNS_JSON) as f:
        data = json.load(f)
    return {r["id"]: r for r in data["runs"]}


def compute_area_level_rates(tasks: list[dict]) -> dict[tuple[str, str], dict]:
    """Compute BEq and BEq+ pass rates per (area, level)."""
    buckets: dict[tuple[str, str], dict] = defaultdict(lambda: {"beq": 0, "beq_plus": 0, "attempted": 0})

    for t in tasks:
        if t.get("skipped"):
            continue
        area = t.get("area", "unknown")
        level = t.get("level", "unknown")
        key = (area, level)
        buckets[key]["attempted"] += 1
        if t.get("beq"):
            buckets[key]["beq"] += 1
        if t.get("beq_plus"):
            buckets[key]["beq_plus"] += 1

    rates = {}
    for key, counts in buckets.items():
        n = counts["attempted"]
        rates[key] = {
            "beq_rate": round(counts["beq"] / n * 100, 1) if n else None,
            "beq_plus_rate": round(counts["beq_plus"] / n * 100, 1) if n else None,
            "n": n,
        }
    return rates


def fmt_rate(val, n) -> str:
    if val is None or n == 0:
        return "—"
    return f"{val:.0f}%"


def build_table(selected_runs: list[dict], runs_meta: dict) -> tuple[list[list[str]], list[list[str]]]:
    """
    Build header rows and data rows.

    Returns (header_rows, data_rows) both as list of list of strings.
    The table has two rows of column headers (area / level) then one data row per run.
    Each run row has two sub-rows: BEq and BEq+.
    """
    # Column structure: [Run info cols] + [area_L1, area_L2, area_L3 for each area] + [overall]
    run_info_cols = ["Model", "MaxTok", "Temp", "PassRate(compile)"]

    # Build area×level columns
    area_level_cols = []
    for area in AREAS:
        for level in LEVELS:
            area_level_cols.append((area, level))
    area_level_cols.append(("overall", "all"))

    # Header row 1: area names
    header1 = run_info_cols[:]
    for area, level in area_level_cols:
        header1.append(AREA_DISPLAY.get(area, area) if level == LEVELS[0] else "")
    header1.append("")  # for metric col

    # Header row 2: level names + n (filled per-run)
    header2 = ["" for _ in run_info_cols] + [level for area, level in area_level_cols] + ["Metric"]

    rows = []
    for run_info in selected_runs:
        run_id = run_info["run_id"]
        beq_file = NAIVE_DIR / run_id / "beq_results.json"
        if not beq_file.exists():
            continue

        with open(beq_file) as f:
            beq_data = json.load(f)

        meta = runs_meta.get(run_id, {})
        env = meta.get("env", {})
        model_raw = env.get("VLLM_MODEL", run_info.get("model_raw", ""))
        # Strip proxy prefix
        model_display = model_raw.split("/", 1)[-1] if "/" in model_raw else model_raw

        compile_rate = run_info.get("pass_rate", 0.0)
        row_prefix = [
            model_display,
            str(env.get("VLLM_MAX_TOKENS", "?")),
            str(env.get("VLLM_TEMPERATURE", "?")),
            f"{compile_rate:.1f}%",
        ]

        rates = compute_area_level_rates(beq_data.get("tasks", []))
        total_attempted = beq_data.get("attempted_tasks", 0)
        total_beq = beq_data.get("beq_passed", 0)
        total_beq_plus = beq_data.get("beq_plus_passed", 0)
        overall_beq = round(total_beq / total_attempted * 100, 1) if total_attempted else None
        overall_beq_plus = round(total_beq_plus / total_attempted * 100, 1) if total_attempted else None

        for metric_name, metric_key, overall_val in [
            ("BEq", "beq_rate", overall_beq),
            ("BEq+", "beq_plus_rate", overall_beq_plus),
        ]:
            row = row_prefix[:]
            for area, level in area_level_cols:
                if area == "overall":
                    row.append(fmt_rate(overall_val, total_attempted))
                else:
                    r = rates.get((area, level), {})
                    row.append(fmt_rate(r.get(metric_key), r.get("n", 0)))
            row.append(metric_name)
            rows.append(row)

    return [header1, header2], rows


def to_markdown(header_rows: list[list[str]], data_rows: list[list[str]]) -> str:
    all_rows = header_rows + data_rows
    widths = [max(len(r[i]) for r in all_rows) for i in range(len(all_rows[0]))]

    def fmt_row(row):
        return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)) + " |"

    lines = []
    lines.append(fmt_row(header_rows[0]))
    # Separator after first header
    lines.append("| " + " | ".join("-" * w for w in widths) + " |")
    lines.append(fmt_row(header_rows[1]))
    lines.append("| " + " | ".join("-" * w for w in widths) + " |")
    for row in data_rows:
        lines.append(fmt_row(row))
    return "\n".join(lines)


def main():
    if not BEQ_RUNS_JSON.exists():
        print(f"beq_runs.json not found: {BEQ_RUNS_JSON}")
        print("Run: python -m scripts.beq_select_runs")
        sys.exit(1)

    with open(BEQ_RUNS_JSON) as f:
        selected_runs = json.load(f)["selected_runs"]

    runs_meta = load_runs_meta()
    header_rows, data_rows = build_table(selected_runs, runs_meta)

    if not data_rows:
        print("No beq_results.json files found. Run python -m scripts.beq_eval --all first.")
        sys.exit(1)

    md = to_markdown(header_rows, data_rows)
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Saved: {OUT_MD}")

    all_rows = header_rows + data_rows
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)
    print(f"Saved: {OUT_CSV}")

    print("\n" + md)


if __name__ == "__main__":
    main()
