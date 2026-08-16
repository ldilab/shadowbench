#!/bin/bash
# run_two_stage.sh — convenience wrapper for the two-stage autoformalize→prove pipeline.
#
# Usage:
#   bash scripts/run_two_stage.sh                # full algebra L1 with defaults
#   DRY=1 bash scripts/run_two_stage.sh          # 5 algebra L1 tasks
#   AREAS="algebra topology" LEVELS="L1 L2" bash scripts/run_two_stage.sh
#   STAGE1=op/gemini-flash STAGE2=op/claude-opus-4.6 bash scripts/run_two_stage.sh
set -e

cd .

LOG_DIR="results/naive_prompting/analysis/two_stage_logs"
mkdir -p "$LOG_DIR"
TS=$(date +%Y%m%d_%H%M%S)
LOG="$LOG_DIR/two_stage_${TS}.log"

STAGE1="${STAGE1:-op/gemini-flash}"
STAGE2="${STAGE2:-op/gemini-pro}"
MAX_TOKENS="${MAX_TOKENS:-8192}"
TEMP="${TEMP:-0.6}"
AREAS_ARGS=""
LEVELS_ARGS=""
[ -n "${AREAS:-}" ] && AREAS_ARGS="--areas $AREAS"
[ -n "${LEVELS:-}" ] && LEVELS_ARGS="--levels $LEVELS"

DRY_FLAG=""
if [ "${DRY:-0}" = "1" ]; then
    DRY_FLAG="--dry-run"
fi

if [ -z "${LITELLM_API_KEY:-}" ]; then
    export LITELLM_API_KEY="sk-dummy"
fi

echo "Two-stage run started $(date)" | tee "$LOG"
echo "  stage1=$STAGE1 stage2=$STAGE2 max_tokens=$MAX_TOKENS temp=$TEMP" | tee -a "$LOG"
echo "  $AREAS_ARGS $LEVELS_ARGS $DRY_FLAG" | tee -a "$LOG"

python -m scripts.two_stage_eval \
    --stage1-model "$STAGE1" --stage2-model "$STAGE2" \
    --max-tokens "$MAX_TOKENS" --temperature "$TEMP" \
    $AREAS_ARGS $LEVELS_ARGS $DRY_FLAG ${EXTRA_ARGS:-} 2>&1 | tee -a "$LOG"

echo "Two-stage run finished $(date)" | tee -a "$LOG"
