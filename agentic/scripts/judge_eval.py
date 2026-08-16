"""LLM-as-Judge evaluator for proof semantic correctness.

Complements `scripts/beq_eval.py` (which only judges STATEMENT equivalence).
For each (compile-successful) candidate we ask M judge models × K samples
whether the candidate's statement+proof actually establishes the intended
theorem, then majority-vote.

Usage:
    # dry run (smallest-per-family models, 1 sample, 5 tasks)
    python -m scripts.judge_eval --run-id <id> --dry-run --max-tasks 5

    # real run (defaults: best-per-family, 3 samples, compile-success scope)
    python -m scripts.judge_eval --run-id <id>

    # custom
    python -m scripts.judge_eval --run-id <id> \
        --models op/gemini-pro,op/claude-opus-4.6,op/gpt-mini \
        --samples 5 --temperature 0.6 --scope compiled --concurrency 8

Writes results/naive_prompting/<run_id>/judge_results.json.

Environment: set LITELLM_API_KEY (or pass via litellm config).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from openai import APIError, AsyncOpenAI, RateLimitError
from rich.console import Console
from tqdm.asyncio import tqdm_asyncio

from scripts.judge_loader import JudgeItem, NAIVE_PROMPTING_DIR, load_judge_pairs
from scripts.judge_prompt import build_prompt, parse_response

# Defaults
BEST_PER_FAMILY = ["op/gemini-pro", "op/claude-opus-4.6", "op/gpt-mini"]
SMALLEST_PER_FAMILY = ["op/gemini-flash", "op/claude-haiku-4.5", "op/gpt-nano"]
LITELLM_BASE_URL = "http://127.0.0.1:1235/v1"

console = Console()


@dataclass
class Vote:
    model: str
    sample: int
    verdict: str
    reason: str
    error: str | None = None
    latency_s: float | None = None


def _make_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        base_url=os.environ.get("LITELLM_BASE_URL", LITELLM_BASE_URL),
        api_key=os.environ.get("LITELLM_API_KEY", "sk-dummy"),
    )


async def _call_judge(
    client: AsyncOpenAI,
    model: str,
    system: str,
    user: str,
    temperature: float,
    max_tokens: int = 512,
    max_retries: int = 3,
) -> tuple[str, str | None, float]:
    """Return (response_text, error_message, latency_s). Retries on transient errors."""
    t0 = time.time()
    last_err: str | None = None
    for attempt in range(max_retries):
        try:
            resp = await client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return resp.choices[0].message.content or "", None, time.time() - t0
        except (RateLimitError, APIError) as e:
            last_err = f"{type(e).__name__}: {e}"
            # exponential backoff with jitter
            await asyncio.sleep(2 ** attempt + random.uniform(0, 0.5))
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            break
    return "", last_err, time.time() - t0


async def _vote_for_task(
    client: AsyncOpenAI,
    item: JudgeItem,
    models: list[str],
    samples: int,
    temperature: float,
    sem: asyncio.Semaphore,
) -> list[Vote]:
    system, user = build_prompt(
        informal_text=item.informal_text,
        has_nl_proof=item.has_nl_proof,
        formal_ref=item.formal_ref or "",
        candidate=item.candidate or "",
    )

    async def one(model: str, sample: int) -> Vote:
        async with sem:
            text, err, latency = await _call_judge(
                client, model, system, user, temperature
            )
        if err:
            return Vote(model=model, sample=sample, verdict="uncertain",
                        reason="", error=err, latency_s=round(latency, 2))
        parsed = parse_response(text)
        return Vote(model=model, sample=sample, verdict=parsed["verdict"],
                    reason=parsed["reason"], error=None, latency_s=round(latency, 2))

    tasks = [one(m, s) for m in models for s in range(samples)]
    return await asyncio.gather(*tasks)


def _aggregate(votes: list[Vote], models: list[str]) -> dict:
    verdicts = [v.verdict for v in votes]
    c = Counter(verdicts)
    correct = c.get("correct", 0)
    incorrect = c.get("incorrect", 0)
    if correct > incorrect:
        majority = "correct"
    elif incorrect > correct:
        majority = "incorrect"
    else:
        majority = "uncertain"

    per_model: dict[str, str] = {}
    for m in models:
        mv = [v.verdict for v in votes if v.model == m]
        mc = Counter(mv)
        if mc.get("correct", 0) > mc.get("incorrect", 0):
            per_model[m] = "correct"
        elif mc.get("incorrect", 0) > mc.get("correct", 0):
            per_model[m] = "incorrect"
        else:
            per_model[m] = "uncertain"

    agreement = (
        sum(1 for v in verdicts if v == majority) / len(verdicts)
        if verdicts else 0.0
    )
    return {
        "correct": correct,
        "incorrect": incorrect,
        "uncertain": c.get("uncertain", 0),
        "majority": majority,
        "per_model": per_model,
        "agreement": round(agreement, 3),
    }


async def evaluate_run(
    run_id: str,
    models: list[str],
    samples: int,
    temperature: float,
    scope: str,
    max_tasks: int | None,
    concurrency: int,
    force: bool,
    verbose: bool,
) -> dict:
    run_dir = NAIVE_PROMPTING_DIR / run_id
    out_path = run_dir / "judge_results.json"
    existing: dict[str, dict] = {}
    if out_path.exists() and not force:
        try:
            prior = json.loads(out_path.read_text(encoding="utf-8"))
            # allow resume only when config matches
            same_config = (
                prior.get("models") == models
                and prior.get("samples_per_model") == samples
                and prior.get("scope") == scope
            )
            if same_config:
                existing = {t["task_id"]: t for t in prior.get("tasks", [])}
                console.print(
                    f"[cyan]Resuming: {len(existing)} tasks already judged.[/]"
                )
            else:
                console.print(
                    "[yellow]Existing judge_results.json has different config; "
                    "use --force to overwrite.[/]"
                )
                return prior
        except Exception as e:
            console.print(f"[yellow]Could not read existing {out_path}: {e}[/]")

    items = load_judge_pairs(run_id, scope)
    if max_tasks is not None:
        items = items[:max_tasks]
    console.print(
        f"[bold]{run_id}[/]  scope={scope}  tasks={len(items)}  "
        f"models={len(models)}×{samples}"
    )

    client = _make_client()
    sem = asyncio.Semaphore(concurrency)

    tasks_out: list[dict] = list(existing.values())
    remaining = [i for i in items if i.task_id not in existing]

    async def grade(item: JudgeItem) -> dict:
        votes = await _vote_for_task(client, item, models, samples, temperature, sem)
        agg = _aggregate(votes, models)
        rec = {
            "task_id": item.task_id,
            "area": item.area, "level": item.level,
            "compile_ok": item.compile_ok,
            "beq": item.beq, "beq_plus": item.beq_plus,
            "informal_has_nl_proof": item.has_nl_proof,
            "votes": [asdict(v) for v in votes],
            "per_model_majority": agg["per_model"],
            "majority": agg["majority"],
            "agreement": agg["agreement"],
            "counts": {"correct": agg["correct"], "incorrect": agg["incorrect"],
                       "uncertain": agg["uncertain"]},
        }
        if verbose:
            console.log(
                f"  [{agg['majority']}] {item.task_id}  "
                f"c={agg['correct']} i={agg['incorrect']} u={agg['uncertain']}  "
                f"agree={agg['agreement']}"
            )
        return rec

    # gather with progress bar; await_all tolerates individual failures inside grade()
    if remaining:
        results = await tqdm_asyncio.gather(
            *[grade(it) for it in remaining], desc=f"{run_id}", unit="task"
        )
        tasks_out.extend(results)

    # summary
    n_correct = sum(1 for t in tasks_out if t["majority"] == "correct")
    n_incorrect = sum(1 for t in tasks_out if t["majority"] == "incorrect")
    n_uncertain = sum(1 for t in tasks_out if t["majority"] == "uncertain")
    judged = len(tasks_out)
    result = {
        "run_id": run_id,
        "scope": scope,
        "models": models,
        "samples_per_model": samples,
        "temperature": temperature,
        "base_url": os.environ.get("LITELLM_BASE_URL", LITELLM_BASE_URL),
        "n_total_candidates": len(items) + sum(
            1 for t in existing.values() if t["task_id"] not in {i.task_id for i in items}
        ),
        "n_judged": judged,
        "n_majority_correct": n_correct,
        "n_majority_incorrect": n_incorrect,
        "n_majority_uncertain": n_uncertain,
        "proof_correct_rate": round(n_correct / judged * 100, 2) if judged else 0.0,
        "tasks": tasks_out,
    }
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(
        f"[green]{run_id}: correct={n_correct}/{judged} "
        f"= {result['proof_correct_rate']}%  (incorrect={n_incorrect}, "
        f"uncertain={n_uncertain})[/]"
    )
    console.print(f"  saved → {out_path}")
    return result


def _parse_models(s: str | None) -> list[str] | None:
    if not s:
        return None
    return [x.strip() for x in s.split(",") if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser(description="LLM-as-Judge evaluator for proofs")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--run-id", type=str)
    group.add_argument("--all", action="store_true",
                       help="Evaluate runs listed in analysis/beq_runs.json")
    ap.add_argument("--models", type=str, default=None,
                    help="Comma-separated judge models (default: best-per-family)")
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=0.5)
    ap.add_argument("--scope", choices=["compiled", "beq", "all"], default="compiled")
    ap.add_argument("--max-tasks", type=int, default=None)
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true",
                    help="Shortcut: smallest-per-family models × 1 sample")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if args.dry_run:
        models = _parse_models(args.models) or SMALLEST_PER_FAMILY
        samples = 1 if args.samples == 3 else args.samples
    else:
        models = _parse_models(args.models) or BEST_PER_FAMILY
        samples = args.samples

    async def _run_all():
        if args.run_id:
            await evaluate_run(
                args.run_id, models, samples, args.temperature, args.scope,
                args.max_tasks, args.concurrency, args.force, args.verbose,
            )
        else:
            runs_path = NAIVE_PROMPTING_DIR / "analysis" / "beq_runs.json"
            if not runs_path.exists():
                console.print(f"[red]{runs_path} not found. Run beq_select_runs first.[/]")
                return
            selected = json.loads(runs_path.read_text(encoding="utf-8"))["selected_runs"]
            console.print(f"Evaluating {len(selected)} runs…")
            for info in selected:
                try:
                    await evaluate_run(
                        info["run_id"], models, samples, args.temperature,
                        args.scope, args.max_tasks, args.concurrency,
                        args.force, args.verbose,
                    )
                except Exception as e:
                    console.print(f"[red]failed on {info['run_id']}: {e}[/]")

    asyncio.run(_run_all())


if __name__ == "__main__":
    main()
