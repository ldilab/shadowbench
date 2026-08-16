#!/usr/bin/env python3
"""
sync_runs.py — runs hourly: download new experiments + execute analysis pipeline
  - target: org=anonymous-org, created_at >= 2026-04-16
  - skip runs that already exist locally
"""

import json
import os
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL  = os.environ.get("SHADOWBENCH_DOWNLOAD_BASE_URL", "https://leaderboard.example.org/api/downloads")
PASSWORD  = os.environ.get("SHADOWBENCH_DOWNLOAD_PASSWORD") or os.environ.get("SHADOWBENCH_API_KEY")
CUTOFF    = datetime(2026, 4, 16, tzinfo=timezone.utc)
TARGET_ORG = os.environ.get("SHADOWBENCH_TARGET_ORG", "anonymous-org")

RESULTS_DIR  = Path(os.environ.get("SHADOWBENCH_RESULTS_DIR", "results/naive_prompting"))
RUNS_JSON    = RESULTS_DIR / "runs.json"
ANALYSIS_DIR = RESULTS_DIR / "analysis"
RUN_ALL_SH   = ANALYSIS_DIR / "src" / "run_all.sh"

def curl_json(url: str) -> dict:
    result = subprocess.run(
        ["curl", "-s", "--max-time", "30", url],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)

def fetch_remote_runs() -> list:
    url = f"{BASE_URL}/runs.json?password={PASSWORD}"
    return curl_json(url)["runs"]

def load_local_runs() -> dict:
    if not RUNS_JSON.exists():
        return {}
    return {r["id"]: r for r in json.load(open(RUNS_JSON)).get("runs", [])}

def save_local_runs(runs: dict):
    with open(RUNS_JSON, "w") as f:
        json.dump({"runs": list(runs.values())}, f, indent=2, default=str)

def download_run(run_id: str) -> bool:
    run_dir = RESULTS_DIR / run_id
    if run_dir.exists():
        return False  # already exists

    url = f"{BASE_URL}/runs/{run_id}.tar.gz?password={PASSWORD}"
    tgz = RESULTS_DIR / f"{run_id}.tar.gz"
    print(f"  ↓ {run_id}")
    try:
        # -f: fail on HTTP error (4xx/5xx) → non-zero exit code
        r = subprocess.run(
            ["curl", "-sf", "--max-time", "120", "-o", str(tgz), "-w", "%{http_code}", url],
            capture_output=True, text=True,
        )
        http_code = r.stdout.strip()
        if r.returncode != 0 or http_code == "404":
            print(f"  ⏳ not ready yet (HTTP {http_code}) — will retry next cycle")
            if tgz.exists():
                tgz.unlink()
            return False
        with tarfile.open(tgz) as t:
            t.extractall(RESULTS_DIR)
        tgz.unlink()
        return True
    except Exception as e:
        print(f"  ✗ download failed: {e}")
        if tgz.exists():
            tgz.unlink()
        return False

def run_analysis():
    print("\n[analysis] running pipeline...")
    result = subprocess.run(["bash", str(RUN_ALL_SH)], capture_output=True, text=True,
                            cwd=str(ANALYSIS_DIR))
    if result.returncode == 0:
        print("[analysis] done")
    else:
        print("[analysis] FAILED")
        print(result.stderr[-2000:])

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not PASSWORD:
        print("Set SHADOWBENCH_DOWNLOAD_PASSWORD or SHADOWBENCH_API_KEY before syncing runs.", file=sys.stderr)
        sys.exit(2)

    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[sync] {now}")

    remote = fetch_remote_runs()
    local  = load_local_runs()

    # Filter: our org + after cutoff
    target = [
        r for r in remote
        if r.get("org") == TARGET_ORG
        and datetime.fromisoformat(r["created_at"]) >= CUTOFF
    ]
    print(f"[sync] remote target runs: {len(target)}  (local: {len(local)})")

    new_runs = [r for r in target if r["id"] not in local]
    if not new_runs:
        print("[sync] no new runs")
        return

    print(f"[sync] {len(new_runs)} new run(s) to download:")
    downloaded = []
    for r in new_runs:
        if download_run(r["id"]):
            downloaded.append(r)
            local[r["id"]] = r  # also add to runs.json

    if downloaded:
        save_local_runs(local)
        print(f"[sync] downloaded {len(downloaded)} run(s): "
              + ", ".join(r["id"] for r in downloaded))
        run_analysis()
    else:
        print("[sync] nothing new to download")

if __name__ == "__main__":
    main()
