#!/bin/bash
# commands/run_beq_eval.sh
# End-to-end BEq / BEq+ evaluation pipeline for naive_prompting results.
#
# Steps:
#   1. Select best-per-model runs
#   2. Run BEq/BEq+ evaluation for all selected runs
#   3. Generate summary table
#
# Usage:
#   ./commands/run_beq_eval.sh [--max-tasks N] [--timeout SECONDS] [--force]
#
# Options:
#   --max-tasks N     Limit tasks per run (for debugging)
#   --timeout SECONDS Per-direction proof timeout (default: 60)
#   --force           Re-run even if beq_results.json exists
#   --run-id ID       Evaluate a specific run only (skips step 1)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/.elan/bin:$PATH"
[ -f "${SCRIPT_DIR}/.venv/bin/activate" ] && source "${SCRIPT_DIR}/.venv/bin/activate"

MAX_TASKS_ARG=""
TIMEOUT_ARG=""
FORCE_ARG=""
RUN_ID_ARG=""

while [ $# -gt 0 ]; do
    case "$1" in
        --max-tasks) MAX_TASKS_ARG="--max-tasks $2"; shift 2 ;;
        --timeout)   TIMEOUT_ARG="--timeout $2"; shift 2 ;;
        --force)     FORCE_ARG="--force"; shift ;;
        --run-id)    RUN_ID_ARG="$2"; shift 2 ;;
        *) echo "Unknown flag: $1"; exit 1 ;;
    esac
done

cd "$SCRIPT_DIR"

if [ -z "$RUN_ID_ARG" ]; then
    echo "=================================================="
    echo "Step 1: Selecting best-per-model runs"
    echo "=================================================="
    python3 -m scripts.beq_select_runs

    echo ""
    echo "=================================================="
    echo "Step 2: Running BEq / BEq+ evaluation"
    echo "=================================================="
    python3 -m scripts.beq_eval --all $MAX_TASKS_ARG $TIMEOUT_ARG $FORCE_ARG
else
    echo "=================================================="
    echo "Evaluating run: $RUN_ID_ARG"
    echo "=================================================="
    python3 -m scripts.beq_eval --run-id "$RUN_ID_ARG" $MAX_TASKS_ARG $TIMEOUT_ARG $FORCE_ARG
fi

echo ""
echo "=================================================="
echo "Step 3: Generating summary tables"
echo "=================================================="
python3 -m scripts.beq_summary

echo ""
echo "Done. Results in results/naive_prompting/analysis/"
