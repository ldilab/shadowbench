#!/usr/bin/env python3
"""
Example scorer stub.

Copy this file into your benchmark repo root as `score_submission.py` (or change SHADOWBENCH_BENCHMARK_RUNNER),
then replace `score(spec)` with your real benchmark invocation.

Contract:
- Read JSON from --spec (submission spec)
- Write JSON metrics to --out
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from typing import Any


def score(spec: dict[str, Any]) -> dict[str, Any]:
    # TODO: Replace with your real benchmark execution.
    #
    # This stub returns "valid-looking" metrics so you can test the plumbing end-to-end.
    seed = int(spec.get("seed", 0))
    rng = random.Random(seed)

    overall = 50.0 + 40.0 * rng.random()
    pass1 = overall - 3.0 + 3.0 * rng.random()
    pass5 = min(100.0, pass1 + 5.0 + 5.0 * rng.random())
    compile_rate = 90.0 + 9.0 * rng.random()
    avg_time = 1.0 + 4.0 * rng.random()
    usd_per_task = 0.0
    tokens_per_task = 800 + int(2000 * rng.random())

    return {
        "overall": float(round(overall, 1)),
        "pass1": float(round(pass1, 1)),
        "pass5": float(round(pass5, 1)),
        "compileRate": float(round(compile_rate, 1)),
        "avgTimeSec": float(round(avg_time, 2)),
        "usdPerTask": float(round(usd_per_task, 3)),
        "tokensPerTask": int(tokens_per_task),
        "trend": [float(round(overall - 6.0, 1)), float(round(overall - 2.0, 1)), float(round(overall, 1))],
        "categories": {
            "Lean4": float(round(overall + rng.uniform(-3, 3), 1)),
            "Coq": float(round(overall + rng.uniform(-3, 3), 1)),
            "Isabelle": float(round(overall + rng.uniform(-3, 3), 1)),
            "HOL4": float(round(overall + rng.uniform(-3, 3), 1)),
        },
        "envHash": spec.get("envHash", "sha256:demo"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="Path to JSON submission spec")
    ap.add_argument("--out", required=True, help="Path to JSON metrics output")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    out_path = Path(args.out)

    spec = json.loads(spec_path.read_text())
    metrics = score(spec)

    out_path.write_text(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
