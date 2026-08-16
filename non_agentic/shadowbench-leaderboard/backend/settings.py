from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Settings:
    db_path: Path
    dataset_version: str
    benchmark_dir: Path
    runner_cmd: str
    timeout_sec: int
    max_workers: int
    allow_origins: list[str]
    admin_password: Optional[str]


def load_settings() -> Settings:
    db_path = Path(os.environ.get("LEADERBOARD_DB", "./data/leaderboard.sqlite")).expanduser()
    dataset_version = os.environ.get("DATASET_VERSION", "v1.2")
    benchmark_dir = Path(os.environ.get("SHADOWBENCH_BENCHMARK_DIR", "~/shadowbench/shadowbench-benchmark")).expanduser()

    # Runner command template; must include {spec} and {out}
    runner_cmd = os.environ.get(
        "SHADOWBENCH_BENCHMARK_RUNNER",
        "python score_submission.py --spec {spec} --out {out}",
    )

    timeout_sec = int(os.environ.get("SHADOWBENCH_BENCHMARK_TIMEOUT_SEC", "3600"))
    max_workers = int(os.environ.get("LEADERBOARD_MAX_WORKERS", "1"))

    # For dev: allow all. For prod, set a specific origin list.
    allow = os.environ.get("LEADERBOARD_ALLOW_ORIGINS", "*")
    allow_origins = ["*"] if allow.strip() == "*" else [x.strip() for x in allow.split(",") if x.strip()]

    # Admin password (set ADMIN_PASSWORD env var to enable protection).
    # If unset or empty, admin endpoints are unprotected (rely on network-level auth).
    admin_password = os.environ.get("ADMIN_PASSWORD") or None

    return Settings(
        db_path=db_path,
        dataset_version=dataset_version,
        benchmark_dir=benchmark_dir,
        runner_cmd=runner_cmd,
        timeout_sec=timeout_sec,
        max_workers=max_workers,
        allow_origins=allow_origins,
        admin_password=admin_password,
    )
