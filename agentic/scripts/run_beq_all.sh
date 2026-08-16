#!/bin/bash
# run_beq_all.sh — Run BEq evaluation on all remaining runs
# Each run takes ~30-90 minutes depending on task count
set -e

cd .

LOG_DIR="results/naive_prompting/analysis/beq_logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
MAIN_LOG="$LOG_DIR/beq_batch_${TIMESTAMP}.log"

echo "BEq batch evaluation started at $(date)" | tee "$MAIN_LOG"
echo "==========================================" | tee -a "$MAIN_LOG"

run_beq() {
    local run_id="$1"
    local n="$2"
    local total="$3"
    echo "" | tee -a "$MAIN_LOG"
    echo "[$n/$total] Evaluating: $run_id ($(date))" | tee -a "$MAIN_LOG"

    # Skip if already done
    if [ -f "results/naive_prompting/$run_id/beq_results.json" ]; then
        echo "  SKIP — beq_results.json already exists" | tee -a "$MAIN_LOG"
        return 0
    fi

    local run_log="$LOG_DIR/beq_${run_id}.log"
    if python -m scripts.beq_eval --run-id "$run_id" 2>&1 | tee "$run_log"; then
        echo "  DONE — $(date)" | tee -a "$MAIN_LOG"
    else
        echo "  FAILED — see $run_log" | tee -a "$MAIN_LOG"
    fi
}

# Non-ablation runs (token length variations)
NON_ABLATION=(
    claude-haiku-4-5-2048-t-0-6-8fab78
    claude-haiku-4-5-4096-t-0-6-7adf4f
    claude-haiku-4-5-l-16384-t-0-6-04a942
    claude-haiku-4-5-l-8192-t-0-6-36bfca
    claude-opus-4-6-4096-1c5014
    claude-opus-4-6-4096-22b2d7
    claude-opus-4-6-4096-2edc79
    claude-opus-4-6-ef2f0d
    claude-opus-4-6-l-16384-t-0-6-3156ea
    claude-opus-4-6-l-8192-t-0-6-7bc3f4
    claude-sonnet-4-6-2048-t-0-6-0246b1
    claude-sonnet-4-6-l-16384-t-0-6-faef30
    claude-sonnet-4-6-l-8192-t-0-6-e02169
    gemini-3-1-pro-l-16384-t-0-6-1034bf
    gemini-3-1-pro-l-8192-t-0-6-d5d564
    gemini-flash-3-1-2048-t-0-6-e6b1e4
    gemini-flash-3-1-4096-t-0-6-825c37
    gemini-flash-3-preview-6f9f3e
    gemini-flash-l-16384-t-0-6-b7b966
    gemini-flash-l-8192-t-0-6-d4171f
    gemini-pro-3-1-2048-t-0-6-ab6ddd
    gemini-pro-3-1-e77466
    gpt-5-4-l-16384-t-0-6-48aeb1
    gpt-5-4-l-8192-t-0-6-c6f2b0
    gpt-base-5-4-4096-t-0-6-095e2f
    gpt-base-5-4-9bac9e
    gpt-mini-5-4-2048-t-0-6-6c0d1a
    gpt-mini-5-4-4096-t-0-6-17f8ab
    gpt-mini-l-16384-t-0-6-58cad5
    gpt-mini-l-8192-t-0-6-657ae3
    gpt-nano-5-4-4096-t-0-6-e6a7a2
    gpt-nano-5-4-b73155
    gpt-nano-l-16384-t-0-6-a8668b
    gpt-nano-l-8192-t-0-6-c3c571
)

# Ablation runs
ABLATION=(
    claude-haiku-4-5-l-8192-t-0-6-proving-e2a64b
    claude-haiku-4-5-l-8192-t-0-6-proving-w-nl-5a1005
    claude-haiku-4-5-l-8192-t-0-6-proving-wo-aux-f80ce4
    claude-opus-4-6-l-8192-t-0-6-proving-d99891
    claude-opus-4-6-l-8192-t-0-6-proving-w-nl-983039
    claude-opus-4-6-l-8192-t-0-6-proving-wo-aux-2c4e37
    claude-sonnet-4-6-l-8192-t-0-6-proving-db03b1
    claude-sonnet-4-6-l-8192-t-0-6-proving-w-nl-98b784
    claude-sonnet-4-6-l-8192-t-0-6-proving-wo-aux-374ad6
    gemini-flash-l-8192-t-0-6-proving-2c0b4e
    gemini-flash-l-8192-t-0-6-proving-w-nl-4a6164
    gemini-flash-l-8192-t-0-6-proving-wo-aux-a9a714
    gemini-pro-l-8192-t-0-6-proving-89dba4
    gemini-pro-l-8192-t-0-6-proving-w-nl-fc3aae
    gemini-pro-l-8192-t-0-6-proving-wo-aux-5ca274
    gpt-base-l-8192-t-0-6-proving-d1521b
    gpt-base-l-8192-t-0-6-proving-w-nl-edf732
    gpt-base-l-8192-t-0-6-proving-wo-aux-2ffa18
    gpt-mini-l-8192-t-0-6-proving-5e4b9d
    gpt-mini-l-8192-t-0-6-proving-w-nl-6be6f5
    gpt-mini-l-8192-t-0-6-proving-wo-aux-5e5935
    gpt-nano-l-8192-t-0-6-proving-6ff0c5
    gpt-nano-l-8192-t-0-6-proving-w-nl-b1adca
    gpt-nano-l-8192-t-0-6-proving-wo-aux-f5b2d3
)

ALL=("${NON_ABLATION[@]}" "${ABLATION[@]}")
TOTAL=${#ALL[@]}

echo "Total runs to evaluate: $TOTAL" | tee -a "$MAIN_LOG"
echo "  Non-ablation: ${#NON_ABLATION[@]}" | tee -a "$MAIN_LOG"
echo "  Ablation: ${#ABLATION[@]}" | tee -a "$MAIN_LOG"

N=0
for run_id in "${ALL[@]}"; do
    N=$((N + 1))
    run_beq "$run_id" "$N" "$TOTAL"
done

echo "" | tee -a "$MAIN_LOG"
echo "==========================================" | tee -a "$MAIN_LOG"
echo "BEq batch evaluation completed at $(date)" | tee -a "$MAIN_LOG"

# Count results
DONE=$(find results/naive_prompting -name "beq_results.json" | wc -l)
echo "Total runs with beq_results.json: $DONE" | tee -a "$MAIN_LOG"
