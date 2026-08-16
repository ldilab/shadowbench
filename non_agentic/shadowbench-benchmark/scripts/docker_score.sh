#!/usr/bin/env bash
# Optional wrapper if you want the backend runner command to be "bash scripts/docker_score.sh SPEC OUT"
# This wrapper runs score_submission.py on the host (venv python) and relies on score_submission.py
# to sandbox compilation using Docker.
set -euo pipefail
SPEC="${1:?spec path required}"
OUT="${2:?out path required}"

PY="${SHADOWBENCH_VENV_PY:-$HOME/venvs/shadowbench/bin/python}"
exec "$PY" "$(dirname "$0")/../score_submission.py" --spec "$SPEC" --out "$OUT"
