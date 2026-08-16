#!/bin/bash
# commands/run_folder_experiment.sh
# Iterates over .lean files in a folder and runs run_experiment.sh on each sequentially.
#
# Usage: ./commands/run_folder_experiment.sh <FOLDER_PATH> <MAX_ROUNDS> [PROMPT_FILE] [--name EXPERIMENT_NAME] [--model MODEL] [--effort LEVEL] [--failure-memory] [--no-guard] [--skip-existing]
# Example: ./commands/run_folder_experiment.sh leanproblems/chibench__research_papers_noprop 3
# Example: ./commands/run_folder_experiment.sh leanproblems/chibench__research_papers_noprop 3 --name my_exp --failure-memory --skip-existing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_EXPERIMENT="${SCRIPT_DIR}/run_experiment.sh"

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <FOLDER_PATH> <MAX_ROUNDS> [PROMPT_FILE] [--name EXPERIMENT_NAME] [--model MODEL] [--effort LEVEL] [--failure-memory] [--no-guard] [--skip-existing]"
    echo "Example: $0 leanproblems/chibench__research_papers_noprop 3"
    echo "Example: $0 leanproblems/chibench__research_papers_noprop 3 --model opus --effort max --name my_exp --skip-existing"
    exit 1
fi

FOLDER_PATH="$1"
MAX_ROUNDS="$2"
shift 2

if [ ! -d "$FOLDER_PATH" ]; then
    echo "Error: '$FOLDER_PATH' is not a directory."
    exit 1
fi

# Parse remaining arguments — pass them through to run_experiment.sh as-is,
# but intercept --skip-existing which is folder-level only.
PASSTHROUGH_ARGS=()
SKIP_EXISTING="true"
EXPERIMENT_NAME=""
MODEL_ARG=""

while [ $# -gt 0 ]; do
    case "$1" in
        --skip-existing) SKIP_EXISTING="true"; shift ;;
        --name) EXPERIMENT_NAME="$2"; PASSTHROUGH_ARGS+=("--name" "$2"); shift 2 ;;
        --model) MODEL_ARG="$2"; PASSTHROUGH_ARGS+=("--model" "$2"); shift 2 ;;
        --effort) PASSTHROUGH_ARGS+=("--effort" "$2"); shift 2 ;;
        *) PASSTHROUGH_ARGS+=("$1"); shift ;;
    esac
done

# Model selection: default to opus, map aliases to directory names (same as run_experiment.sh)
MODEL_ARG="${MODEL_ARG:-opus}"
case "$MODEL_ARG" in
    haiku)   MODEL_NAME="claude-haiku-4-5" ;;
    sonnet)  MODEL_NAME="claude-sonnet-4-6" ;;
    opus)    MODEL_NAME="claude-opus-4-6" ;;
    *)       MODEL_NAME="$MODEL_ARG" ;;
esac

# BENCHMARK_PATH: relative to leanproblems/ (e.g. shadowbench_lift_wo_nl_proof/L1/algebra)
BENCHMARK_PATH="${FOLDER_PATH#leanproblems/}"
[ "$BENCHMARK_PATH" = "$FOLDER_PATH" ] && BENCHMARK_PATH="$(basename "$FOLDER_PATH")"
BENCHMARK="$BENCHMARK_PATH"  # kept for echo output

# Collect all .lean files (sorted)
mapfile -t LEAN_FILES < <(find "$FOLDER_PATH" -maxdepth 1 -name "*.lean" | sort)

TOTAL=${#LEAN_FILES[@]}
if [ "$TOTAL" -eq 0 ]; then
    echo "No .lean files found in '$FOLDER_PATH'."
    exit 1
fi

echo "=================================================="
echo "Folder Experiment"
echo "Folder:      $FOLDER_PATH"
echo "Benchmark:   $BENCHMARK"
echo "Model:       $MODEL_NAME"
echo "Max Rounds:  $MAX_ROUNDS"
echo "Total Files: $TOTAL"
echo "Skip Existing: $SKIP_EXISTING"
[ -n "$EXPERIMENT_NAME" ] && echo "Experiment:  $EXPERIMENT_NAME"
echo "=================================================="

SUCCESS=0
SKIPPED=0
FAILED=0
FAILED_NAMES=()

for i in "${!LEAN_FILES[@]}"; do
    LEAN_FILE="${LEAN_FILES[$i]}"
    PROBLEM_NAME=$(basename "$LEAN_FILE" .lean)

    echo ""
    echo "──────────────────────────────────────────────────"
    echo "[$(( i + 1 ))/$TOTAL] $PROBLEM_NAME"
    echo "──────────────────────────────────────────────────"

    # --skip-existing: skip if a results directory already exists for this problem
    # New path: results/{EXPERIMENT_NAME}/{BENCHMARK_PATH}/{PROBLEM_NAME}/results/
    # Note: --skip-existing only works reliably when --name is specified.
    if [ "$SKIP_EXISTING" = "true" ] && [ -n "$EXPERIMENT_NAME" ]; then
        RESULT_DIR="${REPO_DIR}/results/${EXPERIMENT_NAME}/${BENCHMARK_PATH}/${PROBLEM_NAME}/results"
        EXISTING=$(find "$RESULT_DIR" -name "run1.log" -maxdepth 2 2>/dev/null | head -1)
        if [ -n "$EXISTING" ]; then
            echo "  → Skipping (result already exists: $RESULT_DIR)"
            (( SKIPPED++ )) || true
            continue
        fi
    fi

    if bash "$RUN_EXPERIMENT" "$LEAN_FILE" "$MAX_ROUNDS" "${PASSTHROUGH_ARGS[@]}"; then
        (( SUCCESS++ )) || true
    else
        EXIT_CODE=$?
        echo "  ✗ FAILED (exit code $EXIT_CODE): $PROBLEM_NAME"
        FAILED_NAMES+=("$PROBLEM_NAME")
        (( FAILED++ )) || true
    fi
done

echo ""
echo "=================================================="
echo "Folder Experiment Complete"
echo "  Total:   $TOTAL"
echo "  Success: $SUCCESS"
echo "  Skipped: $SKIPPED"
echo "  Failed:  $FAILED"
if [ ${#FAILED_NAMES[@]} -gt 0 ]; then
    echo "  Failed problems:"
    for name in "${FAILED_NAMES[@]}"; do
        echo "    - $name"
    done
fi
echo "=================================================="
