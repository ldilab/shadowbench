#!/bin/bash
# commands/run_naive_claude.sh
# Run a single naive Claude Code experiment — no tools, no MCP, single-shot.
#
# Usage: ./commands/run_naive_claude.sh <PROBLEM.lean> [options]
#   --mode autoformalize|complete   (default: autoformalize)
#   --model opus|sonnet|haiku       (default: opus)
#   --effort low|medium|high|xhigh|max  (default: none)
#   --name EXPERIMENT_NAME          (default: naive_claude_code)
#   --timeout SECONDS               (default: 300)
#   --keep-sandbox                  Don't clean up sandbox on success
#
# Examples:
#   ./commands/run_naive_claude.sh leanproblems/shadowbench_lift_text/L1/algebra/alg_gen_L1_001.lean
#   ./commands/run_naive_claude.sh leanproblems/Minif2f/amc12a_2021_p7.lean --mode complete --model sonnet
#
# Output: results/{EXPERIMENT_NAME}/{BENCHMARK_PATH}/{PROBLEM_NAME}/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EMPTY_MCP="${SCRIPT_DIR}/configs/empty_mcp.json"

# Environment setup: elan (Lean toolchain) and Python venv
export PATH="$HOME/.elan/bin:$PATH"
[ -f "${SCRIPT_DIR}/.venv/bin/activate" ] && source "${SCRIPT_DIR}/.venv/bin/activate"

# Lean project root (where lean-toolchain lives)
LEAN_PROJECT_ROOT="${SCRIPT_DIR}/leanproblems"

# ── Defaults ──────────────────────────────────────
MODE="autoformalize"
MODEL_CLI="opus"
EFFORT_ARG=""
EXPERIMENT_NAME="naive_claude_code"
TIMEOUT=300
KEEP_SANDBOX="false"

# ── Usage ─────────────────────────────────────────
usage() {
    echo "Usage: $0 <PROBLEM.lean> [--mode autoformalize|complete] [--model opus|sonnet|haiku] [--name NAME] [--timeout SECONDS] [--keep-sandbox]"
    exit 1
}

if [ "$#" -lt 1 ]; then usage; fi
[[ "$1" == "-h" || "$1" == "--help" ]] && usage

TARGET_PATH="$1"
shift

if [ ! -f "$TARGET_PATH" ]; then
    echo "Error: '$TARGET_PATH' is not a file."
    exit 1
fi

# ── Parse flags ───────────────────────────────────
while [ $# -gt 0 ]; do
    case "$1" in
        --mode)         MODE="$2"; shift 2 ;;
        --model)        MODEL_CLI="$2"; shift 2 ;;
        --effort)       EFFORT_ARG="$2"; shift 2 ;;
        --name)         EXPERIMENT_NAME="$2"; shift 2 ;;
        --timeout)      TIMEOUT="$2"; shift 2 ;;
        --keep-sandbox) KEEP_SANDBOX="true"; shift ;;
        -h|--help)      usage ;;
        *)              echo "Unknown flag: $1"; exit 1 ;;
    esac
done

# ── Model alias → name ───────────────────────────
case "$MODEL_CLI" in
    haiku)   MODEL_NAME="claude-haiku-4-5" ;;
    sonnet)  MODEL_NAME="claude-sonnet-4-6" ;;
    opus)    MODEL_NAME="claude-opus-4-6" ;;
    *)       MODEL_NAME="$MODEL_CLI" ;;
esac

# ── Validate mode ────────────────────────────────
if [[ "$MODE" != "autoformalize" && "$MODE" != "complete" ]]; then
    echo "Error: --mode must be 'autoformalize' or 'complete'"
    exit 1
fi

# ── Paths ─────────────────────────────────────────
PROBLEM_NAME=$(basename "$TARGET_PATH" .lean)
# BENCHMARK_PATH: relative to leanproblems/ (e.g. shadowbench_lift_text/L1/algebra)
PROBLEM_DIR="$(dirname "$TARGET_PATH")"
BENCHMARK_PATH="${PROBLEM_DIR#leanproblems/}"
[ "$BENCHMARK_PATH" = "$PROBLEM_DIR" ] && BENCHMARK_PATH="$(basename "$PROBLEM_DIR")"

DATETIME=$(date +"%Y%m%d_%H%M%S")

# Format: results/{EXPERIMENT_NAME}/{BENCHMARK_PATH}/{PROBLEM_NAME}/
PROBLEM_OUT="${SCRIPT_DIR}/results/${EXPERIMENT_NAME}/${BENCHMARK_PATH}/${PROBLEM_NAME}"
OUT_DIR="$PROBLEM_OUT"

mkdir -p "$PROBLEM_OUT"

# ── Prompt template ──────────────────────────────
if [ "$MODE" = "autoformalize" ]; then
    PROMPT_TEMPLATE="${SCRIPT_DIR}/prompts/prompt_naive_autoformalize.txt"
else
    PROMPT_TEMPLATE="${SCRIPT_DIR}/prompts/prompt_naive_complete.txt"
fi

if [ ! -f "$PROMPT_TEMPLATE" ]; then
    echo "Error: prompt template not found: $PROMPT_TEMPLATE"
    exit 1
fi

# ── Step 1: Extract input ────────────────────────
if [ "$MODE" = "autoformalize" ]; then
    # Extract NL description from block comments
    NL_INPUT=$(python3 -m scripts.naive_extract extract-nl "$TARGET_PATH" 2>/dev/null) || true
    if [ -z "$NL_INPUT" ]; then
        echo "  ⊘ No NL description found in $PROBLEM_NAME — skipping"
        cat <<EOF > "${PROBLEM_OUT}/result.json"
{"problem": "$PROBLEM_NAME", "model": "$MODEL_NAME", "mode": "$MODE", "success": false, "skipped": true, "reason": "no_nl_description"}
EOF
        exit 0
    fi
    echo "$NL_INPUT" > "${PROBLEM_OUT}/input_nl.txt"
    INPUT_CONTENT="$NL_INPUT"
else
    # Use full file content
    INPUT_CONTENT=$(cat "$TARGET_PATH")
    cp "$TARGET_PATH" "${PROBLEM_OUT}/input_original.lean"
fi

# ── Step 2: Build prompt ─────────────────────────
PROMPT_BASE=$(cat "$PROMPT_TEMPLATE")
FULL_PROMPT="${PROMPT_BASE}
${INPUT_CONTENT}"

# ── Step 3: Run Claude (no tools, no MCP, single-shot) ──
echo "  ▶ Running Claude ($MODEL_CLI, mode=$MODE) on $PROBLEM_NAME ..."
START_TIME=$(date +%s)

RAW_OUTPUT=""
CLAUDE_EXIT=0
# Disable hooks via env vars; --tools "" disables all built-in tools;
# --strict-mcp-config with empty config disables all MCP servers.
# Use --bare if ANTHROPIC_API_KEY is set (cleanest), otherwise rely on normal auth.
CLAUDE_EXTRA_FLAGS=()
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    CLAUDE_EXTRA_FLAGS+=(--bare)
fi
if [ -n "$EFFORT_ARG" ]; then
    CLAUDE_EXTRA_FLAGS+=(--effort "$EFFORT_ARG")
fi
RAW_OUTPUT=$(DISABLE_OMC=1 DISABLE_MATHLIB_GUARD=1 \
    timeout "$TIMEOUT" claude -p \
    "${CLAUDE_EXTRA_FLAGS[@]}" \
    --tools "" \
    --strict-mcp-config --mcp-config "$EMPTY_MCP" \
    --permission-mode bypassPermissions \
    --model "$MODEL_CLI" \
    --no-session-persistence \
    "$FULL_PROMPT" 2>&1) || CLAUDE_EXIT=$?

END_TIME=$(date +%s)
DURATION=$(( END_TIME - START_TIME ))

# Save raw output
echo "$RAW_OUTPUT" > "${PROBLEM_OUT}/raw_output.txt"

# Handle timeout or crash
if [ "$CLAUDE_EXIT" -eq 124 ]; then
    echo "  ✗ TIMEOUT after ${TIMEOUT}s"
    cat <<EOF > "${PROBLEM_OUT}/result.json"
{"problem": "$PROBLEM_NAME", "model": "$MODEL_NAME", "mode": "$MODE", "success": false, "skipped": false, "has_error": true, "has_sorry": false, "duration_seconds": $DURATION, "error": "timeout"}
EOF
    exit 1
fi

if [ -z "$RAW_OUTPUT" ]; then
    echo "  ✗ Empty output from Claude"
    cat <<EOF > "${PROBLEM_OUT}/result.json"
{"problem": "$PROBLEM_NAME", "model": "$MODEL_NAME", "mode": "$MODE", "success": false, "skipped": false, "has_error": true, "has_sorry": false, "duration_seconds": $DURATION, "error": "empty_output"}
EOF
    exit 1
fi

# ── Step 4: Extract Lean code ────────────────────
LEAN_CODE=$(echo "$RAW_OUTPUT" | python3 -m scripts.naive_extract strip-markdown)
echo "$LEAN_CODE" > "${PROBLEM_OUT}/extracted.lean"

# ── Step 5: Create sandbox & save for compilation ──
# Sandbox lives in sandboxes/ (separate from leanproblems/) to avoid exposing other problem files
SANDBOXES_DIR="${SCRIPT_DIR}/sandboxes"
mkdir -p "$SANDBOXES_DIR"
SANDBOX_NAME="naive_${PROBLEM_NAME}_${DATETIME}"
SANDBOX_DIR="${SANDBOXES_DIR}/${SANDBOX_NAME}"
mkdir -p "$SANDBOX_DIR"

# Cleanup trap: ensure sandbox is removed even on early exit
_cleanup_sandbox() {
    [ -d "$SANDBOX_DIR" ] && rm -rf "$SANDBOX_DIR"
}
trap _cleanup_sandbox EXIT

SANDBOX_FILE="${SANDBOX_DIR}/${PROBLEM_NAME}.lean"
SANDBOX_FILE_ABS="$(cd "$SANDBOX_DIR" && pwd)/${PROBLEM_NAME}.lean"
echo "$LEAN_CODE" > "$SANDBOX_FILE"

# ── Step 6: Verify compilation ───────────────────
# Run lake env lean directly from the Lean project root to avoid PATH/cwd issues.
echo "  ⏳ Verifying compilation..."
COMPILE_STDOUT=""
COMPILE_STDERR=""
COMPILE_EXIT=0
COMPILE_STDOUT=$(cd "$LEAN_PROJECT_ROOT" && timeout 300 lake env lean "$SANDBOX_FILE_ABS" 2>"${PROBLEM_OUT}/compile_stderr.tmp") || COMPILE_EXIT=$?
COMPILE_STDERR=$(cat "${PROBLEM_OUT}/compile_stderr.tmp" 2>/dev/null || true)
rm -f "${PROBLEM_OUT}/compile_stderr.tmp"

# Detect errors and sorry
HAS_ERROR="false"
HAS_SORRY="false"
if [ "$COMPILE_EXIT" -ne 0 ] || echo "$COMPILE_STDOUT$COMPILE_STDERR" | grep -qi "error"; then
    HAS_ERROR="true"
fi
if echo "$COMPILE_STDOUT$COMPILE_STDERR" | grep -qi "sorry"; then
    HAS_SORRY="true"
fi

if [ "$HAS_ERROR" = "false" ] && [ "$HAS_SORRY" = "false" ]; then
    IS_SUCCESS="true"
else
    IS_SUCCESS="false"
fi

# Save compile log
cat <<LOGEOF > "${PROBLEM_OUT}/compile_log.txt"
=== exit_code: $COMPILE_EXIT ===
=== stdout ===
$COMPILE_STDOUT
=== stderr ===
$COMPILE_STDERR
LOGEOF

# Escape JSON strings safely
VERIFY_OUTPUT=$(python3 -c "
import json, sys
result = {
    'problem': '$PROBLEM_NAME',
    'model': '$MODEL_NAME',
    'mode': '$MODE',
    'success': $( [ "$IS_SUCCESS" = "true" ] && echo "True" || echo "False" ),
    'skipped': False,
    'has_error': $( [ "$HAS_ERROR" = "true" ] && echo "True" || echo "False" ),
    'has_sorry': $( [ "$HAS_SORRY" = "true" ] && echo "True" || echo "False" ),
    'duration_seconds': $DURATION,
    'compile_exit_code': $COMPILE_EXIT,
    'compile_stdout': open('${PROBLEM_OUT}/compile_log.txt').read()[:2000],
}
print(json.dumps(result, ensure_ascii=False))
" 2>&1)

echo "$VERIFY_OUTPUT" > "${PROBLEM_OUT}/result.json"

# ── Step 7: Report result ────────────────────────
if [ "$IS_SUCCESS" = "true" ]; then
    echo "  ✓ PASSED ($PROBLEM_NAME) in ${DURATION}s"
elif [ "$HAS_SORRY" = "true" ]; then
    echo "  ✗ FAILED ($PROBLEM_NAME) — sorry detected (${DURATION}s)"
else
    echo "  ✗ FAILED ($PROBLEM_NAME) — compilation error [exit $COMPILE_EXIT] (${DURATION}s)"
fi

# ── Step 8: Cleanup sandbox ─────────────────────
if [ "$KEEP_SANDBOX" = "false" ]; then
    rm -rf "$SANDBOX_DIR"
else
    echo "  📁 Sandbox kept at: $SANDBOX_DIR"
fi

# Return exit code based on success
[ "$IS_SUCCESS" = "true" ] && exit 0 || exit 1
