from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple


@dataclass
class RunnerResult:
    metrics: dict[str, Any]
    logs: str


class BenchmarkRunError(RuntimeError):
    pass


def _truncate(s: str, limit: int = 12000) -> str:
    if len(s) <= limit:
        return s
    return s[:limit] + "\n...\n[truncated]\n"


def run_benchmark(
    benchmark_dir: Path,
    runner_cmd_template: str,
    submission_spec: dict[str, Any],
    timeout_sec: int,
) -> RunnerResult:
    """
    Writes submission_spec to a temp file, calls the benchmark runner command in benchmark_dir,
    expects the runner to write JSON metrics to the output file.

    runner_cmd_template MUST contain '{spec}' and '{out}' placeholders.
    """
    benchmark_dir = benchmark_dir.expanduser().resolve()
    if not benchmark_dir.exists():
        raise BenchmarkRunError(f"Benchmark dir not found: {benchmark_dir}")

    if "{spec}" not in runner_cmd_template or "{out}" not in runner_cmd_template:
        raise BenchmarkRunError("SHADOWBENCH_BENCHMARK_RUNNER must include '{spec}' and '{out}' placeholders")

    with tempfile.TemporaryDirectory(prefix="abm_eval_") as td:
        td_path = Path(td)
        spec_path = td_path / "submission_spec.json"
        out_path = td_path / "result.json"

        spec_path.write_text(json.dumps(submission_spec, indent=2))

        cmd = runner_cmd_template.format(spec=str(spec_path), out=str(out_path))

        # Use shell=True so you can set SHADOWBENCH_BENCHMARK_RUNNER as a single string with args.
        # If you want stricter parsing, set it to a simple python command.
        proc = subprocess.run(
            cmd,
            cwd=str(benchmark_dir),
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=os.environ.copy(),
        )

        logs = _truncate(
            f"$ {cmd}\n\n--- STDOUT ---\n{proc.stdout}\n\n--- STDERR ---\n{proc.stderr}\n"
        )

        if proc.returncode != 0:
            raise BenchmarkRunError(f"Benchmark runner failed (exit {proc.returncode}).\n\n{logs}")

        if not out_path.exists():
            raise BenchmarkRunError(
                f"Benchmark runner did not write output JSON at: {out_path}\n\n{logs}"
            )

        try:
            metrics = json.loads(out_path.read_text())
        except Exception as e:
            raise BenchmarkRunError(f"Failed to parse output JSON: {e}\n\n{logs}") from e

        if not isinstance(metrics, dict):
            raise BenchmarkRunError(f"Output JSON must be an object/dict.\n\n{logs}")

        return RunnerResult(metrics=metrics, logs=logs)
