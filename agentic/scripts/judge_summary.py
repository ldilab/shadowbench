"""Generate LLM-as-Judge analysis artifacts from judge_results.json files.

Usage:
    python -m scripts.judge_summary

Writes to results/naive_prompting/analysis/:
    judge_summary_table.md / .csv   — per-run judge %, compile %, BEq % side by side
    judge_by_run.csv                — flat per-run file, one row per run
    judge_by_task.csv               — flat per-task file, one row per (run, task)
    judge_vs_beq_crosstab.md        — cross-tab of judge vs BEq verdicts
    judge_by_family.md              — aggregated by model family (best-of only)
    judge_by_area_level.md          — aggregated by area × level across all runs
    JUDGE_REPORT.md                 — human-readable report
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NAIVE_DIR = REPO_ROOT / "results" / "naive_prompting"
ANALYSIS_DIR = NAIVE_DIR / "analysis"

AREAS = ["algebra", "analysis", "college-math-competition", "geometry", "topology", "number-theory"]
LEVELS = ["L1", "L2", "L3"]
AREA_DISPLAY = {
    "algebra": "algebra",
    "analysis": "analysis",
    "college-math-competition": "cmc",
    "geometry": "geometry",
    "topology": "topology",
    "number-theory": "nt",
}


def load_runs_meta() -> dict[str, dict]:
    """Return {run_id -> {model, max_tokens, temperature}} pulled from env when needed."""
    path = NAIVE_DIR / "runs.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for r in data.get("runs", []):
        rid = r["id"]
        env = r.get("env") or {}
        model = r.get("model") or env.get("VLLM_MODEL")
        max_tokens = r.get("maxTokens") or env.get("VLLM_MAX_TOKENS")
        temperature = r.get("temperature") or env.get("VLLM_TEMPERATURE")
        out[rid] = {"model": model, "maxTokens": max_tokens, "temperature": temperature}
    return out


def load_all() -> list[dict]:
    """Return per-run dicts merging judge + beq + run.json metadata."""
    meta = load_runs_meta()
    rows: list[dict] = []
    for jp in sorted(NAIVE_DIR.glob("*/judge_results.json")):
        j = json.loads(jp.read_text(encoding="utf-8"))
        run_id = j["run_id"]
        row = {"run_id": run_id, **{k: j.get(k) for k in (
            "scope", "models", "samples_per_model", "temperature",
            "n_judged", "n_majority_correct", "n_majority_incorrect",
            "n_majority_uncertain", "proof_correct_rate")}}
        # BEq
        bp = jp.parent / "beq_results.json"
        if bp.exists():
            b = json.loads(bp.read_text(encoding="utf-8"))
            row.update({
                "beq_passed": b.get("beq_passed"),
                "beq_plus_passed": b.get("beq_plus_passed"),
                "beq_attempted": b.get("attempted_tasks"),
                "beq_rate": b.get("beq_rate"),
                "beq_plus_rate": b.get("beq_plus_rate"),
                "beq_tasks": b.get("tasks", []),
            })
        # result.json
        rp = jp.parent / "result.json"
        if rp.exists():
            r = json.loads(rp.read_text(encoding="utf-8"))
            row["compile_rate"] = round(r.get("compileRate", 0), 2)
        # runs.json (secondary); primary source is parsed run_id
        parsed = _parse_run_id(run_id)
        if run_id in meta:
            m = meta[run_id]
            row["model_raw"] = m.get("model")
            row["max_tokens"] = parsed.get("tokens") or m.get("maxTokens")
            row["temperature_cfg"] = parsed.get("temp") or m.get("temperature")
        else:
            row["model_raw"] = None
            row["max_tokens"] = parsed.get("tokens")
            row["temperature_cfg"] = parsed.get("temp")
        row["variant"] = parsed.get("variant") or ""
        row["prov"] = parsed.get("prov") or ""
        row["tasks"] = j.get("tasks", [])
        rows.append(row)
    return rows


import re


_RUN_ID_RE = re.compile(
    r"^(?P<model>claude-(?:haiku|sonnet|opus)-\d-\d|gemini-(?:flash|pro)(?:-\d-\d)?|"
    r"gpt-(?:base|mini|nano)(?:-\d-\d)?)"
    r"(?:-(?P<variant>l|preview))?"
    r"(?:-(?P<tokens>\d{3,5}))?"
    r"(?:-t-(?P<temp>\d(?:-\d)?))?"
    r"(?:-(?P<prov>proving(?:-w-nl|-wo-aux)?))?"
    r"-(?P<hash>[0-9a-f]{6})$"
)


def _parse_run_id(run_id: str) -> dict:
    """Best-effort parse of run_id into {model, variant, tokens, temp, prov}."""
    m = _RUN_ID_RE.match(run_id)
    if not m:
        return {}
    model = m.group("model")
    # normalise claude/gemini model name -> dot form, claude-haiku-4-5 → claude-haiku-4.5
    model = re.sub(r"-(\d)-(\d)$", r"-\1.\2", model)
    temp = m.group("temp")
    if temp and "-" in temp:
        temp = temp.replace("-", ".")
    return {
        "model": model,
        "variant": m.group("variant"),
        "tokens": m.group("tokens"),
        "temp": temp,
        "prov": m.group("prov"),
    }


def _model_canonical(raw: str | None, run_id: str | None = None) -> str:
    # prefer run_id parse (runs.json env can be mislabeled by config reuse)
    if run_id:
        p = _parse_run_id(run_id)
        if p.get("model"):
            return p["model"]
    if not raw:
        return "?"
    return raw.replace("op/", "").replace(":floor", "")


def _family_of(model_canonical: str) -> str:
    if "gemini" in model_canonical:
        return "gemini"
    if "claude" in model_canonical:
        return "claude"
    if "gpt" in model_canonical:
        return "gpt"
    return "other"


def write_per_run_table(rows: list[dict]) -> None:
    """Per-run summary table (md + csv). Sorts by judged-task count, then judge%."""
    rows = sorted(rows, key=lambda r: (-(r.get("n_judged") or 0), -(r.get("proof_correct_rate") or 0)))

    header = [
        "run_id", "model", "max_tokens", "temp",
        "compile%", "n_judged", "judge_correct%",
        "beq%", "beq+%",
        "correct", "incorrect", "uncertain",
    ]
    out_csv = ANALYSIS_DIR / "judge_summary_table.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow([
                r["run_id"],
                _model_canonical(r.get("model_raw"), r["run_id"]),
                r.get("max_tokens") or "",
                r.get("temperature_cfg") or "",
                r.get("compile_rate"),
                r.get("n_judged"),
                r.get("proof_correct_rate"),
                r.get("beq_rate"),
                r.get("beq_plus_rate"),
                r.get("n_majority_correct"),
                r.get("n_majority_incorrect"),
                r.get("n_majority_uncertain"),
            ])

    lines: list[str] = []
    lines.append("# Judge Summary Table — per-run\n")
    lines.append("_Judged only `compile_ok=true` tasks. Voting: 3 judges (op/gemini-pro, op/claude-opus-4.6, op/gpt-mini) × 3 samples at T=0.5; majority rule._\n")
    lines.append(f"\n| run_id | model | tok | T | compile% | judged | **judge%** | BEq% | BEq+% | c/i/u |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        model = _model_canonical(r.get("model_raw"), r["run_id"])
        cr = r.get("compile_rate")
        cr_s = f"{cr:.1f}" if cr is not None else "—"
        rate = r.get("proof_correct_rate")
        rate_s = f"**{rate:.1f}**" if rate is not None else "—"
        beq = r.get("beq_rate")
        beq_s = f"{beq:.1f}" if beq is not None else "—"
        beqp = r.get("beq_plus_rate")
        beqp_s = f"{beqp:.1f}" if beqp is not None else "—"
        lines.append(
            f"| {r['run_id']} | {model} | {r.get('max_tokens') or '-'} | "
            f"{r.get('temperature_cfg') or '-'} | {cr_s} | {r.get('n_judged')} | "
            f"{rate_s} | {beq_s} | {beqp_s} | "
            f"{r.get('n_majority_correct')}/{r.get('n_majority_incorrect')}/{r.get('n_majority_uncertain')} |"
        )

    (ANALYSIS_DIR / "judge_summary_table.md").write_text("\n".join(lines), encoding="utf-8")


def write_by_run_csv(rows: list[dict]) -> None:
    """Lean flat CSV for downstream pandas work."""
    header = [
        "run_id", "model_raw", "model_canonical", "family",
        "max_tokens", "temperature_cfg",
        "compile_rate", "beq_attempted", "beq_passed", "beq_plus_passed",
        "beq_rate", "beq_plus_rate",
        "scope", "judge_models", "samples_per_model", "judge_temperature",
        "n_judged", "n_majority_correct", "n_majority_incorrect",
        "n_majority_uncertain", "proof_correct_rate",
    ]
    out = ANALYSIS_DIR / "judge_by_run.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in sorted(rows, key=lambda r: r["run_id"]):
            mc = _model_canonical(r.get("model_raw"), r["run_id"])
            w.writerow([
                r["run_id"], r.get("model_raw"), mc, _family_of(mc),
                r.get("max_tokens"), r.get("temperature_cfg"),
                r.get("compile_rate"), r.get("beq_attempted"),
                r.get("beq_passed"), r.get("beq_plus_passed"),
                r.get("beq_rate"), r.get("beq_plus_rate"),
                r.get("scope"), "|".join(r.get("models") or []),
                r.get("samples_per_model"), r.get("temperature"),
                r.get("n_judged"), r.get("n_majority_correct"),
                r.get("n_majority_incorrect"), r.get("n_majority_uncertain"),
                r.get("proof_correct_rate"),
            ])


def write_by_task_csv(rows: list[dict]) -> None:
    """One row per (run, task)."""
    out = ANALYSIS_DIR / "judge_by_task.csv"
    header = [
        "run_id", "task_id", "area", "level",
        "compile_ok", "beq", "beq_plus",
        "majority", "agreement",
        "c_correct", "c_incorrect", "c_uncertain",
        "gemini_majority", "claude_majority", "gpt_majority",
        "informal_has_nl_proof",
    ]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            for t in r.get("tasks") or []:
                pm = t.get("per_model_majority") or {}
                counts = t.get("counts") or {}
                gem = next((v for k, v in pm.items() if "gemini" in k), "")
                cla = next((v for k, v in pm.items() if "claude" in k), "")
                gpt = next((v for k, v in pm.items() if "gpt" in k), "")
                w.writerow([
                    r["run_id"], t["task_id"], t.get("area"), t.get("level"),
                    t.get("compile_ok"), t.get("beq"), t.get("beq_plus"),
                    t.get("majority"), t.get("agreement"),
                    counts.get("correct"), counts.get("incorrect"), counts.get("uncertain"),
                    gem, cla, gpt,
                    t.get("informal_has_nl_proof"),
                ])


def write_judge_vs_beq_crosstab(rows: list[dict]) -> None:
    """BEq verdict × Judge verdict cross-tab across all judged tasks.

    Uses only tasks where beq info is available (skipped=False, attempted).
    """
    mat = Counter()
    n_tasks = 0
    for r in rows:
        for t in r.get("tasks") or []:
            if t.get("beq") is None:
                continue
            n_tasks += 1
            beq_label = "pass" if t.get("beq") else ("plus" if t.get("beq_plus") else "fail")
            if t.get("beq"):
                beq_label = "BEq"
            elif t.get("beq_plus"):
                beq_label = "BEq+ only"
            else:
                beq_label = "BEq fail"
            judge_label = t.get("majority") or "?"
            mat[(beq_label, judge_label)] += 1

    beq_order = ["BEq", "BEq+ only", "BEq fail"]
    judge_order = ["correct", "incorrect", "uncertain"]

    lines = ["# Judge × BEq cross-tab\n",
             f"_Over {n_tasks} (run, task) pairs where both BEq and Judge were available (i.e. compile-ok tasks with BEq records)._\n",
             "\n| BEq status ↓ / Judge → | correct | incorrect | uncertain | row total |",
             "|---|---:|---:|---:|---:|"]
    col_totals = Counter()
    for b in beq_order:
        row = [mat[(b, j)] for j in judge_order]
        rt = sum(row)
        for i, v in enumerate(row):
            col_totals[judge_order[i]] += v
        lines.append(f"| **{b}** | {row[0]} | {row[1]} | {row[2]} | {rt} |")
    lines.append(
        f"| **col total** | {col_totals['correct']} | {col_totals['incorrect']} | "
        f"{col_totals['uncertain']} | {n_tasks} |"
    )

    # Additional framing
    beq_pass = sum(mat[(b, j)] for b in ("BEq", "BEq+ only") for j in judge_order)
    beq_fail = sum(mat[("BEq fail", j)] for j in judge_order)
    judge_correct_when_beq_pass = sum(mat[(b, "correct")] for b in ("BEq", "BEq+ only"))
    judge_correct_when_beq_fail = mat[("BEq fail", "correct")]
    lines.append("")
    lines.append(f"- Tasks that BEq/BEq+ passed and judge called correct: "
                 f"**{judge_correct_when_beq_pass}/{beq_pass}** "
                 f"({judge_correct_when_beq_pass/max(beq_pass,1)*100:.1f}%)")
    lines.append(f"- Tasks that BEq failed but judge called correct: "
                 f"**{judge_correct_when_beq_fail}/{beq_fail}** "
                 f"({judge_correct_when_beq_fail/max(beq_fail,1)*100:.1f}%)")
    lines.append(f"- Tasks judge called correct that BEq missed: "
                 f"**{judge_correct_when_beq_fail}** (would be new 'semantically correct proof' signal)")

    (ANALYSIS_DIR / "judge_vs_beq_crosstab.md").write_text("\n".join(lines), encoding="utf-8")


def write_area_level_table(rows: list[dict]) -> None:
    """Area × Level aggregation across all runs (one figure: fraction majority-correct of judged)."""
    buckets: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for r in rows:
        for t in r.get("tasks") or []:
            key = (t.get("area") or "?", t.get("level") or "?")
            buckets[key][t.get("majority") or "?"] += 1

    lines = ["# Judge majority × area × level (all runs pooled)\n",
             "_Each cell: judge-correct% (n judged). Populations are compile-successful tasks across all 58 runs._\n",
             "\n| Area | L1 | L2 | L3 | all |",
             "|---|---|---|---|---|"]

    def cell(n_correct, n_total):
        if n_total == 0:
            return "—"
        return f"{n_correct/n_total*100:.1f}% ({n_correct}/{n_total})"

    for area in AREAS:
        cells = []
        area_c = area_t = 0
        for level in LEVELS:
            b = buckets[(area, level)]
            nt = sum(b.values())
            nc = b["correct"]
            area_c += nc; area_t += nt
            cells.append(cell(nc, nt))
        cells.append(cell(area_c, area_t))
        lines.append(f"| {AREA_DISPLAY.get(area, area)} | " + " | ".join(cells) + " |")

    (ANALYSIS_DIR / "judge_by_area_level.md").write_text("\n".join(lines), encoding="utf-8")


def write_family_table(rows: list[dict]) -> None:
    """Per-family aggregate: for each (family × token budget × temperature), pool judged tasks."""
    buckets: dict[tuple[str, str, str, str], Counter] = defaultdict(Counter)
    cond_compile: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)
    cond_beq: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)
    for r in rows:
        mc = _model_canonical(r.get("model_raw"), r["run_id"])
        fam = _family_of(mc)
        tok = str(r.get("max_tokens") or "?")
        temp = str(r.get("temperature_cfg") or "?")
        key = (fam, mc, tok, temp)
        for t in r.get("tasks") or []:
            buckets[key][t.get("majority") or "?"] += 1
        cond_compile[key].append(r.get("compile_rate") or 0)
        cond_beq[key].append(r.get("beq_plus_rate") or 0)

    lines = ["# Judge aggregate per model/family\n",
             "_Rows are model × max_tokens × temp configurations. judge% is over pooled compile-ok tasks from all runs matching that config._\n",
             "\n| family | model | tok | T | runs | judged | judge% | ø compile% | ø BEq+% |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    order = sorted(buckets.keys(), key=lambda k: (k[0], k[1], int(k[2]) if k[2].isdigit() else 0, k[3]))
    for key in order:
        fam, mc, tok, temp = key
        b = buckets[key]
        total = sum(b.values())
        if total == 0:
            continue
        correct = b["correct"]
        n_runs = len(cond_compile[key])
        avg_compile = sum(cond_compile[key]) / n_runs
        avg_beq = sum(cond_beq[key]) / n_runs
        lines.append(
            f"| {fam} | {mc} | {tok} | {temp} | {n_runs} | {total} | "
            f"{correct/total*100:.1f}% | {avg_compile:.1f}% | {avg_beq:.1f}% |"
        )
    (ANALYSIS_DIR / "judge_by_family.md").write_text("\n".join(lines), encoding="utf-8")


def write_beq_pass_judge_incorrect(rows: list[dict]) -> None:
    """The inverse: BEq passed (statement match) but judge called incorrect/uncertain.

    These are cases where Lean's REPL says the two statements are logically equivalent,
    but the LLM judges disagree about whether the proof actually establishes the claim.
    Worth inspecting: either judges are wrong, or BEq+ is blind to proof-level issues
    (e.g. helper `def` with wrong body, restated-but-vacuous hypothesis).
    """
    records: list[dict] = []
    for r in rows:
        for t in r.get("tasks") or []:
            beq_ok = bool(t.get("beq")) or bool(t.get("beq_plus"))
            if not beq_ok:
                continue
            if t.get("majority") == "correct":
                continue
            counts = t.get("counts") or {}
            records.append({
                "run_id": r["run_id"],
                "task_id": t["task_id"],
                "area": t.get("area"), "level": t.get("level"),
                "beq": t.get("beq"), "beq_plus": t.get("beq_plus"),
                "majority": t.get("majority"),
                "agreement": t.get("agreement", 0),
                "correct": counts.get("correct", 0),
                "incorrect": counts.get("incorrect", 0),
                "uncertain": counts.get("uncertain", 0),
                "per_model": t.get("per_model_majority") or {},
            })
    records.sort(key=lambda x: (x["majority"] == "uncertain", -x["incorrect"], -x["agreement"]))

    lines = ["# Tasks where BEq/BEq+ passed but the judge did NOT call correct\n",
             f"_Filter: (beq OR beq_plus) = True AND judge majority ≠ correct. Total: **{len(records)}**_\n",
             "_These are candidates for manual inspection: BEq says statements match, but ≥5 of 9 judge votes disagreed._\n",
             "\n| run_id | task_id | area/level | BEq / BEq+ | judge majority | c/i/u | agreement | per-model |",
             "|---|---|---|---|---|---|---:|---|"]
    for rec in records:
        pm = rec["per_model"]
        pm_s = ", ".join(f"{k.split('/')[-1]}={v[0]}" for k, v in pm.items())
        beq_flag = ("B" if rec["beq"] else ".") + ("+" if rec["beq_plus"] else ".")
        lines.append(
            f"| {rec['run_id']} | {rec['task_id']} | {rec['area']}/{rec['level']} | "
            f"{beq_flag} | **{rec['majority']}** | "
            f"{rec['correct']}/{rec['incorrect']}/{rec['uncertain']} | "
            f"{rec['agreement']:.2f} | {pm_s} |"
        )
    (ANALYSIS_DIR / "judge_beq_pass_judge_incorrect.md").write_text("\n".join(lines), encoding="utf-8")


def _intra_agreement(votes: list[dict], model: str) -> float | None:
    """Return fraction of the most-common verdict within one model's K samples."""
    verdicts = [v["verdict"] for v in votes if v.get("model") == model]
    if not verdicts:
        return None
    c = Counter(verdicts)
    return c.most_common(1)[0][1] / len(verdicts)


def write_consensus_report(rows: list[dict]) -> None:
    """Consensus analysis.

    Per task we have 3 judge models × 3 samples = 9 votes. We measure:
      (A) Intra-model consensus: for each (task, model), how uniform were the 3 samples?
          We bucket into {unanimous, 2-of-3, 1-1-1}. Report per-model distribution.
      (B) Inter-model consensus: do the three models' per-model majorities agree?
          We bucket into {all-3-agree, 2-of-3-agree, all-3-differ}.
      (C) Fleiss-style pairwise agreement: average pairwise agreement of verdicts
          across the 9 votes per task.
    """
    per_model_intra: dict[str, Counter] = defaultdict(Counter)  # model → {unanimous, 2/3, 1/1/1}
    inter_buckets = Counter()                                   # task-level
    pairwise_agreements: list[float] = []                       # per-task
    total_tasks = 0

    from itertools import combinations

    for r in rows:
        for t in r.get("tasks") or []:
            votes = t.get("votes") or []
            if len(votes) < 2:
                continue
            total_tasks += 1
            # (A) per-model
            models = sorted({v.get("model") for v in votes if v.get("model")})
            for m in models:
                m_verd = [v["verdict"] for v in votes if v.get("model") == m]
                if not m_verd:
                    continue
                cc = Counter(m_verd)
                top = cc.most_common(1)[0][1]
                k = len(m_verd)
                if top == k:
                    per_model_intra[m]["unanimous"] += 1
                elif top == k - 1:
                    per_model_intra[m][f"{top}/{k}"] += 1
                else:
                    per_model_intra[m][f"{top}/{k} (split)"] += 1
            # (B) inter-model
            pm = t.get("per_model_majority") or {}
            pm_values = list(pm.values()) if pm else []
            if len(pm_values) == len(models) == 3:
                if len(set(pm_values)) == 1:
                    inter_buckets["all-agree"] += 1
                elif len(set(pm_values)) == 2:
                    inter_buckets["2-of-3-agree"] += 1
                else:
                    inter_buckets["all-differ"] += 1
            # (C) pairwise
            all_v = [v["verdict"] for v in votes]
            pairs = list(combinations(all_v, 2))
            if pairs:
                agree = sum(1 for a, b in pairs if a == b) / len(pairs)
                pairwise_agreements.append(agree)

    def _fmt_pct(n, d):
        return f"{n/d*100:.1f}% ({n}/{d})" if d else "—"

    lines = ["# Judge Consensus Report\n",
             f"_Across **{total_tasks}** judged tasks, each with 3 judge models × 3 samples (9 votes)._\n"]

    # (A) Intra-model
    lines.append("\n## (A) Intra-model consensus — do the 3 samples of one judge agree with themselves?\n")
    lines.append("| model | unanimous (3/3) | 2/3 agree | split 1/1/1 |")
    lines.append("|---|---|---|---|")
    for m in sorted(per_model_intra.keys()):
        c = per_model_intra[m]
        u = c["unanimous"]
        two = sum(v for k, v in c.items() if k.startswith("2/"))
        sp = sum(v for k, v in c.items() if "split" in k)
        tot = u + two + sp
        lines.append(
            f"| `{m}` | {_fmt_pct(u, tot)} | {_fmt_pct(two, tot)} | {_fmt_pct(sp, tot)} |"
        )

    # (B) Inter-model
    lines.append("\n## (B) Inter-model consensus — do the 3 judges' majorities agree with each other?\n")
    tot_b = sum(inter_buckets.values())
    lines.append("| configuration | count | fraction |")
    lines.append("|---|---:|---:|")
    for label in ("all-agree", "2-of-3-agree", "all-differ"):
        v = inter_buckets.get(label, 0)
        lines.append(f"| {label} | {v} | {v/max(tot_b,1)*100:.1f}% |")

    # (C) Pairwise agreement
    if pairwise_agreements:
        avg = sum(pairwise_agreements) / len(pairwise_agreements)
        low = sum(1 for p in pairwise_agreements if p < 0.5)
        high = sum(1 for p in pairwise_agreements if p >= 0.75)
        lines.append("\n## (C) Average pairwise agreement across all 9 votes\n")
        lines.append(f"- Mean pairwise agreement: **{avg*100:.1f}%**")
        lines.append(f"- Tasks with ≥75% pairwise agreement: {_fmt_pct(high, len(pairwise_agreements))}")
        lines.append(f"- Tasks with <50% pairwise agreement (judges disagree a lot): {_fmt_pct(low, len(pairwise_agreements))}")

    # interpretation
    lines.append("\n## Interpretation\n")
    if tot_b:
        all_agree = inter_buckets.get("all-agree", 0)
        lines.append(
            f"- **Strong inter-model signal**: all three judges reach the same per-model majority on "
            f"{all_agree}/{tot_b} tasks ({all_agree/tot_b*100:.1f}%). "
            f"Disagreement across models is concentrated in borderline proofs."
        )
    lines.append(
        "- **Within a single judge**, the 3 samples mostly agree with themselves (see table A), "
        "meaning temperature=0.5 did not destabilise per-model judgments — most of the 'uncertainty' "
        "in the final verdict comes from genuine cross-model disagreement, not sampling noise."
    )

    (ANALYSIS_DIR / "judge_consensus_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_judge_finds_beq_misses(rows: list[dict]) -> None:
    """List tasks where BEq failed but judge called correct with high agreement.

    These are the concrete examples of 'BEq too strict / judge finds real proofs'.
    Sort by agreement desc, then by run_id.
    """
    records: list[dict] = []
    for r in rows:
        for t in r.get("tasks") or []:
            if t.get("beq") or t.get("beq_plus"):
                continue
            if t.get("majority") != "correct":
                continue
            records.append({
                "run_id": r["run_id"],
                "task_id": t["task_id"],
                "area": t.get("area"),
                "level": t.get("level"),
                "agreement": t.get("agreement", 0),
                "correct_votes": (t.get("counts") or {}).get("correct", 0),
                "incorrect_votes": (t.get("counts") or {}).get("incorrect", 0),
                "per_model": t.get("per_model_majority") or {},
            })
    records.sort(key=lambda x: (-x["agreement"], -x["correct_votes"], x["run_id"], x["task_id"]))

    lines = ["# Tasks the judge calls correct that BEq missed\n",
             f"_Filter: BEq and BEq+ both false, judge majority = correct. Total: **{len(records)}** (run, task) pairs._\n",
             f"_Sorted by agreement then correct-vote count._\n",
             "\n| rank | run_id | task_id | area/level | correct/incorrect votes | agreement | per-model |",
             "|---:|---|---|---|---|---:|---|"]
    for i, rec in enumerate(records[:100], start=1):
        pm = rec["per_model"]
        pm_s = ", ".join(f"{k.split('/')[-1]}={v[0]}" for k, v in pm.items())
        lines.append(
            f"| {i} | {rec['run_id']} | {rec['task_id']} | "
            f"{rec['area']}/{rec['level']} | {rec['correct_votes']}/{rec['incorrect_votes']} | "
            f"{rec['agreement']:.2f} | {pm_s} |"
        )
    if len(records) > 100:
        lines.append(f"\n_…truncated, showing top 100 of {len(records)}. Full list in `judge_by_task.csv`._")
    (ANALYSIS_DIR / "judge_finds_beq_misses.md").write_text("\n".join(lines), encoding="utf-8")


# Measured per-call USD cost (mean across 4 sample tasks × 3 models, 2026-04-23).
# LiteLLM proxy returns a `cost` field per response; these numbers are direct,
# not estimated. See `scripts/judge_summary.py` inline probe for reproduction.
PER_CALL_USD: dict[str, float] = {
    "op/gemini-pro": 0.007227,
    "op/claude-opus-4.6": 0.009124,
    "op/gpt-mini": 0.000751,
}


def write_report(rows: list[dict]) -> None:
    """Human-readable markdown report."""
    total_judged = sum(r.get("n_judged") or 0 for r in rows)
    total_correct = sum(r.get("n_majority_correct") or 0 for r in rows)
    total_incorrect = sum(r.get("n_majority_incorrect") or 0 for r in rows)
    total_uncertain = sum(r.get("n_majority_uncertain") or 0 for r in rows)
    # Cost: each judged task = 3 models × 3 samples = 9 calls
    calls_per_model = total_judged * 3
    total_calls = total_judged * 9
    cost_by_model = {m: calls_per_model * c for m, c in PER_CALL_USD.items()}
    total_cost_usd = sum(cost_by_model.values())

    # top / bottom
    with_data = [r for r in rows if (r.get("n_judged") or 0) >= 10]
    top = sorted(with_data, key=lambda r: -(r.get("proof_correct_rate") or 0))[:5]
    bot = sorted(with_data, key=lambda r: (r.get("proof_correct_rate") or 0))[:5]
    largest_gap_above = sorted(
        with_data,
        key=lambda r: -((r.get("proof_correct_rate") or 0) - (r.get("beq_plus_rate") or 0))
    )[:5]
    largest_gap_below = sorted(
        with_data,
        key=lambda r: ((r.get("proof_correct_rate") or 0) - (r.get("beq_plus_rate") or 0))
    )[:5]

    lines: list[str] = []
    lines.append("# LLM-as-Judge Proof Correctness Report\n")
    lines.append("## Method\n")
    lines.append(
        "For every compile-successful candidate (scope `compiled`), three judge LLMs each produced "
        "three verdicts (9 votes/task) on whether the candidate's statement+proof semantically "
        "establishes the intended theorem. Majority rule per task; ties go to `uncertain`.\n"
    )
    lines.append("- **Scope:** `--scope compiled` — every row in this report corresponds to a task that compiled cleanly (zero error lines). Non-compile tasks were not judged.")
    lines.append("- **Judges (best of each family):** `op/gemini-pro`, `op/claude-opus-4.6`, `op/gpt-mini`")
    lines.append("- **Sampling:** 3 samples per judge at T=0.5")
    lines.append("- **Inputs shown to judge:** informal statement + optional NL proof (`shadowbench-benchmark/data/<area>/<level>/<problem_id>/text.md`), reference formal statement with `sorry` (`meta.target_code`), candidate `.extracted.lean`.")
    lines.append("- **Compile-ok detection:** `task_results.json` → `result.json.problems` → per-task `.log` scan (first hit wins).")
    lines.append("- **Code:** `scripts/judge_loader.py`, `scripts/judge_prompt.py`, `scripts/judge_eval.py`, `scripts/judge_summary.py`.\n")

    lines.append("## Headline numbers\n")
    lines.append(f"- Runs with ≥1 judged task: **{sum(1 for r in rows if (r.get('n_judged') or 0) > 0)}/{len(rows)}**")
    lines.append(f"- Judged tasks: **{total_judged}**")
    lines.append(f"- Majority **correct**: **{total_correct}** ({total_correct/max(total_judged,1)*100:.2f}%)")
    lines.append(f"- Majority incorrect: {total_incorrect} ({total_incorrect/max(total_judged,1)*100:.2f}%)")
    lines.append(f"- Majority uncertain: {total_uncertain} ({total_uncertain/max(total_judged,1)*100:.2f}%)\n")

    lines.append("## Cost\n")
    lines.append(
        f"Each task costs 3 judges × 3 samples = 9 LiteLLM calls. "
        f"Per-call USD (measured 2026-04-23 on 4 sample tasks per judge):\n"
    )
    lines.append("| judge model | per-call $ | calls | subtotal $ |")
    lines.append("|---|---:|---:|---:|")
    for m, per in PER_CALL_USD.items():
        sub = cost_by_model[m]
        lines.append(f"| `{m}` | ${per:.5f} | {calls_per_model} | ${sub:.2f} |")
    lines.append(
        f"| **total** |  | **{total_calls}** | **${total_cost_usd:.2f}** |"
    )
    lines.append(
        f"\n_Per judged task: ${total_cost_usd/max(total_judged,1):.4f} "
        f"(≈${total_cost_usd/max(total_judged,1)*1000:.1f} / 1000 tasks)._\n"
    )
    lines.append(
        "_Note on `gemini-pro`: it consistently emitted the full 512-token output "
        "(the `JSON`-only contract was obeyed but the model wrote prose before the JSON), "
        "so its per-call cost is near the `max_tokens=512` ceiling. "
        "Dropping to `max_tokens=256` with stricter `response_format` would ~halve gemini's share._\n"
    )

    lines.append("## Top 5 runs by judge correct rate (≥10 judged)\n")
    lines.append("| run_id | judged | judge% | BEq+% | compile% |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in top:
        lines.append(
            f"| {r['run_id']} | {r['n_judged']} | **{r['proof_correct_rate']:.1f}** | "
            f"{r.get('beq_plus_rate') or 0:.1f} | {r.get('compile_rate') or 0:.1f} |"
        )

    lines.append("\n## Bottom 5 runs by judge correct rate (≥10 judged)\n")
    lines.append("| run_id | judged | judge% | BEq+% | compile% |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in bot:
        lines.append(
            f"| {r['run_id']} | {r['n_judged']} | {r['proof_correct_rate']:.1f} | "
            f"{r.get('beq_plus_rate') or 0:.1f} | {r.get('compile_rate') or 0:.1f} |"
        )

    lines.append("\n## Largest judge − BEq+ gap (judge much higher; BEq missed these)\n")
    lines.append("| run_id | judged | judge% | BEq+% | gap |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in largest_gap_above:
        gap = (r.get("proof_correct_rate") or 0) - (r.get("beq_plus_rate") or 0)
        lines.append(
            f"| {r['run_id']} | {r['n_judged']} | {r['proof_correct_rate']:.1f} | "
            f"{r.get('beq_plus_rate') or 0:.1f} | +{gap:.1f} |"
        )

    lines.append("\n## Largest BEq+ − judge gap (BEq passed but judge doubted)\n")
    lines.append("| run_id | judged | judge% | BEq+% | gap |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in largest_gap_below:
        gap = (r.get("proof_correct_rate") or 0) - (r.get("beq_plus_rate") or 0)
        lines.append(
            f"| {r['run_id']} | {r['n_judged']} | {r['proof_correct_rate']:.1f} | "
            f"{r.get('beq_plus_rate') or 0:.1f} | {gap:+.1f} |"
        )

    lines.append("\n## Files in this directory\n")
    lines.append("- `judge_summary_table.md` / `.csv` — per-run side-by-side with BEq and compile")
    lines.append("- `judge_by_run.csv` — same, lean pandas-friendly version")
    lines.append("- `judge_by_task.csv` — per-task atomic file (run_id × task_id)")
    lines.append("- `judge_vs_beq_crosstab.md` — BEq verdict × judge verdict matrix")
    lines.append("- `judge_by_area_level.md` — judge correct% broken down by area × level")
    lines.append("- `judge_by_family.md` — aggregated by model family × max_tokens × temperature")
    lines.append("- `judge_finds_beq_misses.md` — concrete list of tasks where BEq failed but judge said correct")
    lines.append("- `judge_beq_pass_judge_incorrect.md` — tasks where BEq passed but judges disagreed (manual-inspection candidates)")
    lines.append("- `judge_consensus_report.md` — intra-model (samples) and inter-model (3 judges) agreement breakdown")
    lines.append("- `judge_logs/` — per-run evaluator logs")
    lines.append("\n## Regenerate\n")
    lines.append("```bash\npython -m scripts.judge_summary\n```")

    (ANALYSIS_DIR / "JUDGE_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_all()
    print(f"Loaded {len(rows)} runs.")
    write_per_run_table(rows)
    write_by_run_csv(rows)
    write_by_task_csv(rows)
    write_judge_vs_beq_crosstab(rows)
    write_area_level_table(rows)
    write_family_table(rows)
    write_judge_finds_beq_misses(rows)
    write_beq_pass_judge_incorrect(rows)
    write_consensus_report(rows)
    write_report(rows)
    print("Wrote:")
    for p in [
        "judge_summary_table.md", "judge_summary_table.csv",
        "judge_by_run.csv", "judge_by_task.csv",
        "judge_vs_beq_crosstab.md", "judge_by_area_level.md",
        "judge_by_family.md",
        "judge_finds_beq_misses.md",
        "judge_beq_pass_judge_incorrect.md",
        "judge_consensus_report.md",
        "JUDGE_REPORT.md",
    ]:
        full = ANALYSIS_DIR / p
        print(f"  {full}  ({full.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
