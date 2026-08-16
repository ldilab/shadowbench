#!/bin/bash
# commands/run_naive_claude_folder.sh
# Iterate over .lean files in a folder and run run_naive_claude.sh on each.
#
# Usage: ./commands/run_naive_claude_folder.sh <FOLDER> [options]
#   --mode autoformalize|complete   (default: autoformalize)
#   --model opus|sonnet|haiku       (default: opus)
#   --effort low|medium|high|xhigh|max  (default: none)
#   --name EXPERIMENT_NAME          (default: naive_claude_code)
#   --timeout SECONDS               (default: 120)
#   --skip-existing                 Skip problems that already have results
#   --recursive                     Search .lean files recursively
#   --keep-sandbox                  Don't clean up sandboxes
#
# Examples:
#   ./commands/run_naive_claude_folder.sh leanproblems/Minif2f --mode complete --model opus
#   ./commands/run_naive_claude_folder.sh leanproblems/shadowbench_lift_text/L1 --recursive --name L1_test
#   ./commands/run_naive_claude_folder.sh leanproblems/shadowbench_lift_text/L1/algebra --skip-existing

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_SINGLE="${SCRIPT_DIR}/run_naive_claude.sh"

# Environment setup: elan (Lean toolchain) and Python venv
export PATH="$HOME/.elan/bin:$PATH"
[ -f "${REPO_DIR}/.venv/bin/activate" ] && source "${REPO_DIR}/.venv/bin/activate"

# Lean project root
LEAN_PROJECT_ROOT="${REPO_DIR}/leanproblems"

# ── Pre-flight: ensure mathlib cache is ready ─────
# Multiple concurrent lake processes writing .olean files causes SIGBUS crashes.
# Check that (1) no other lake cache processes are running, and (2) cache exists.
preflight_lean_cache() {
    local CACHE_DIR="${LEAN_PROJECT_ROOT}/.lake/packages/mathlib/.lake/build/lib"

    # Block if another lake exe cache is running (concurrent writes corrupt mmap'd .olean files)
    if pgrep -f "lake exe cache" >/dev/null 2>&1; then
        echo "⚠  Another 'lake exe cache' is running. Waiting for it to finish..."
        while pgrep -f "lake exe cache" >/dev/null 2>&1; do
            sleep 5
        done
        echo "  ✓ Other cache process finished."
    fi

    # Check if mathlib .olean files exist
    local OLEAN_COUNT
    OLEAN_COUNT=$(find "$CACHE_DIR" -name "*.olean" 2>/dev/null | wc -l)
    if [ "$OLEAN_COUNT" -lt 5000 ]; then
        echo "⚠  Mathlib cache incomplete ($OLEAN_COUNT oleans, need ~7000+). Fetching..."
        (cd "$LEAN_PROJECT_ROOT" && lake exe cache get 2>&1)
        OLEAN_COUNT=$(find "$CACHE_DIR" -name "*.olean" 2>/dev/null | wc -l)
        echo "  ✓ Cache ready ($OLEAN_COUNT oleans)."
    fi

    # Quick smoke test: compile a trivial file to catch SIGBUS from corrupted cache
    local TEST_FILE
    TEST_FILE=$(mktemp "${LEAN_PROJECT_ROOT}/smoke_test_XXXXXX.lean")
    echo 'import Mathlib.Tactic.Linarith' > "$TEST_FILE"
    if ! (cd "$LEAN_PROJECT_ROOT" && lake env lean "$TEST_FILE" >/dev/null 2>&1); then
        echo "⚠  Cache smoke test failed (possible corruption). Re-fetching..."
        rm -rf "$CACHE_DIR" 2>/dev/null
        (cd "$LEAN_PROJECT_ROOT" && lake exe cache get 2>&1)
        if ! (cd "$LEAN_PROJECT_ROOT" && lake env lean "$TEST_FILE" >/dev/null 2>&1); then
            echo "✗  Lean compilation still failing after cache re-fetch. Check your environment."
            rm -f "$TEST_FILE"
            exit 1
        fi
    fi
    rm -f "$TEST_FILE"
    echo "✓ Lean mathlib cache OK."
}

# ── Defaults ──────────────────────────────────────
MODE="autoformalize"
MODEL_CLI="opus"
EFFORT_ARG=""
EXPERIMENT_NAME="naive_claude_code"
TIMEOUT=300
SKIP_EXISTING="true"
RECURSIVE="false"
KEEP_SANDBOX="false"

# ── Usage ─────────────────────────────────────────
usage() {
    echo "Usage: $0 <FOLDER> [--mode autoformalize|complete] [--model opus|sonnet|haiku] [--name NAME] [--timeout SECONDS] [--skip-existing] [--recursive] [--keep-sandbox]"
    exit 1
}

if [ "$#" -lt 1 ]; then usage; fi

FOLDER_PATH="$1"
shift

if [ ! -d "$FOLDER_PATH" ]; then
    echo "Error: '$FOLDER_PATH' is not a directory."
    exit 1
fi

# ── Parse flags ───────────────────────────────────
while [ $# -gt 0 ]; do
    case "$1" in
        --mode)           MODE="$2"; shift 2 ;;
        --model)          MODEL_CLI="$2"; shift 2 ;;
        --effort)         EFFORT_ARG="$2"; shift 2 ;;
        --name)           EXPERIMENT_NAME="$2"; shift 2 ;;
        --timeout)        TIMEOUT="$2"; shift 2 ;;
        --skip-existing)  SKIP_EXISTING="true"; shift ;;
        --recursive)      RECURSIVE="true"; shift ;;
        --keep-sandbox)   KEEP_SANDBOX="true"; shift ;;
        -h|--help)        usage ;;
        *)                echo "Unknown flag: $1"; exit 1 ;;
    esac
done

# ── Model alias → name ───────────────────────────
case "$MODEL_CLI" in
    haiku)   MODEL_NAME="claude-haiku-4-5" ;;
    sonnet)  MODEL_NAME="claude-sonnet-4-6" ;;
    opus)    MODEL_NAME="claude-opus-4-6" ;;
    *)       MODEL_NAME="$MODEL_CLI" ;;
esac

# ── Shared output base for this experiment run ──
DATETIME=$(date +"%Y%m%d_%H%M%S")
# BENCHMARK_PATH: relative to leanproblems/ (e.g. shadowbench_lift_text/L1/algebra)
BENCHMARK_PATH="${FOLDER_PATH#leanproblems/}"
[ "$BENCHMARK_PATH" = "$FOLDER_PATH" ] && BENCHMARK_PATH="$(basename "$FOLDER_PATH")"

RESULT_BASE="${REPO_DIR}/results/${EXPERIMENT_NAME}"
mkdir -p "$RESULT_BASE"

# Save experiment config
cat <<EOF > "${RESULT_BASE}/config.json"
{
  "folder": "$FOLDER_PATH",
  "benchmark_path": "$BENCHMARK_PATH",
  "mode": "$MODE",
  "model": "$MODEL_NAME",
  "model_cli": "$MODEL_CLI",
  "experiment_name": "$EXPERIMENT_NAME",
  "timeout": $TIMEOUT,
  "recursive": $RECURSIVE,
  "datetime": "$DATETIME"
}
EOF

# ── Pre-flight check ─────────────────────────────
preflight_lean_cache

# ── Collect .lean files ──────────────────────────
if [ "$RECURSIVE" = "true" ]; then
    mapfile -t LEAN_FILES < <(find "$FOLDER_PATH" -name "*.lean" -not -path "*/sandbox_*" | sort)
else
    mapfile -t LEAN_FILES < <(find "$FOLDER_PATH" -maxdepth 1 -name "*.lean" | sort)
fi

TOTAL=${#LEAN_FILES[@]}
if [ "$TOTAL" -eq 0 ]; then
    echo "No .lean files found in '$FOLDER_PATH'."
    exit 1
fi

echo "=================================================="
echo "Naive Claude Code Folder Experiment"
echo "  Folder:     $FOLDER_PATH"
echo "  Benchmark:  $BENCHMARK_PATH"
echo "  Mode:       $MODE"
echo "  Model:      $MODEL_NAME"
echo "  Timeout:    ${TIMEOUT}s"
echo "  Total:      $TOTAL files"
echo "  Recursive:  $RECURSIVE"
echo "  Skip exist: $SKIP_EXISTING"
echo "  Output:     $RESULT_BASE/{problem}/"
echo "=================================================="

SUCCESS=0
FAILED=0
SKIPPED=0
ERROR=0
FAILED_NAMES=()
SKIPPED_NAMES=()

for i in "${!LEAN_FILES[@]}"; do
    LEAN_FILE="${LEAN_FILES[$i]}"
    PROBLEM_NAME=$(basename "$LEAN_FILE" .lean)

    echo ""
    echo "──────────────────────────────────────────────────"
    echo "[$(( i + 1 ))/$TOTAL] $PROBLEM_NAME"
    echo "──────────────────────────────────────────────────"

    # Skip if result already exists
    # Format: results/{EXPERIMENT_NAME}/{BENCHMARK_PATH}/{PROBLEM_NAME}/result.json
    PROBLEM_RESULT_DIR="${RESULT_BASE}/${BENCHMARK_PATH}/${PROBLEM_NAME}"
    if [ "$SKIP_EXISTING" = "true" ]; then
        if [ -f "${PROBLEM_RESULT_DIR}/result.json" ]; then
            echo "  → Skipping (result already exists)"
            (( SKIPPED++ )) || true
            SKIPPED_NAMES+=("$PROBLEM_NAME")
            continue
        fi
    fi

    # Build passthrough args
    PASSTHROUGH=(
        --mode "$MODE"
        --model "$MODEL_CLI"
        --name "$EXPERIMENT_NAME"
        --timeout "$TIMEOUT"
    )
    [ -n "$EFFORT_ARG" ] && PASSTHROUGH+=(--effort "$EFFORT_ARG")
    [ "$KEEP_SANDBOX" = "true" ] && PASSTHROUGH+=(--keep-sandbox)

    # Run single problem (don't exit on failure)
    if bash "$RUN_SINGLE" "$LEAN_FILE" "${PASSTHROUGH[@]}"; then
        (( SUCCESS++ )) || true
    else
        EXIT_CODE=$?
        # Check if it was skipped (exit 0 with skipped=true in result.json)
        RESULT_FILE="${PROBLEM_RESULT_DIR}/result.json"
        if [ -f "$RESULT_FILE" ]; then
            IS_SKIPPED=$(python3 -c "import json; r=json.load(open('$RESULT_FILE')); print('true' if r.get('skipped') else 'false')" 2>/dev/null || echo "false")
            if [ "$IS_SKIPPED" = "true" ]; then
                (( SKIPPED++ )) || true
                SKIPPED_NAMES+=("$PROBLEM_NAME")
                continue
            fi
        fi
        FAILED_NAMES+=("$PROBLEM_NAME")
        (( FAILED++ )) || true
    fi
done

# ── Generate summary ─────────────────────────────
TOTAL_ATTEMPTED=$(( SUCCESS + FAILED ))
if [ "$TOTAL_ATTEMPTED" -gt 0 ]; then
    PASS_RATE=$(python3 -c "print(round($SUCCESS / $TOTAL_ATTEMPTED * 100, 2))")
else
    PASS_RATE="0.0"
fi

cat <<EOF > "${RESULT_BASE}/summary.json"
{
  "total_files": $TOTAL,
  "attempted": $TOTAL_ATTEMPTED,
  "passed": $SUCCESS,
  "failed": $FAILED,
  "skipped": $SKIPPED,
  "pass_rate_percent": $PASS_RATE,
  "model": "$MODEL_NAME",
  "mode": "$MODE",
  "folder": "$FOLDER_PATH",
  "datetime": "$DATETIME"
}
EOF

echo ""
echo "=================================================="
echo "Naive Claude Code Experiment Complete"
echo "  Total:     $TOTAL"
echo "  Attempted: $TOTAL_ATTEMPTED"
echo "  Passed:    $SUCCESS (${PASS_RATE}%)"
echo "  Failed:    $FAILED"
echo "  Skipped:   $SKIPPED"
if [ ${#FAILED_NAMES[@]} -gt 0 ]; then
    echo "  Failed problems:"
    for name in "${FAILED_NAMES[@]}"; do
        echo "    - $name"
    done
fi
echo "  Results:   $RESULT_BASE/"
echo "=================================================="
