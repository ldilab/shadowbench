#!/bin/bash
# commands/run_experiment.sh
# Usage: ./commands/run_experiment.sh <TARGET_PATH> <MAX_ROUNDS> [PROMPT_FILE] [--name EXPERIMENT_NAME] [--model MODEL] [--effort LEVEL] [--failure-memory] [--no-guard]

set -e

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <TARGET_PATH> <MAX_ROUNDS> [PROMPT_FILE] [--name EXPERIMENT_NAME] [--model MODEL] [--effort LEVEL] [--failure-memory] [--no-guard]"
    echo "Example: $0 leanproblems/Minif2f/imo_1964_p1.lean 3"
    echo "Example: $0 leanproblems/Minif2f/imo_1964_p1.lean 3 --name ablation_full --failure-memory"
    exit 1
fi

TARGET_PATH="$1"
MAX_ROUNDS="$2"
shift 2

# Parse remaining arguments: first non-flag arg is PROMPT_FILE, rest are flags
PROMPT_FILE="prompts/prompt_medium_mode.txt"
USE_FAILURE_MEMORY="false"
DISABLE_GUARD="1"
EXPERIMENT_NAME=""
MODEL_ARG=""
EFFORT_ARG=""
while [ $# -gt 0 ]; do
    case "$1" in
        --failure-memory) USE_FAILURE_MEMORY="true"; shift ;;
        --no-guard) DISABLE_GUARD="1"; shift ;;
        --name) EXPERIMENT_NAME="$2"; shift 2 ;;
        --model) MODEL_ARG="$2"; shift 2 ;;
        --effort) EFFORT_ARG="$2"; shift 2 ;;
        --*) echo "Unknown flag: $1"; exit 1 ;;
        *) PROMPT_FILE="$1"; shift ;;
    esac
done

# Model selection: default to opus, map aliases to directory names
MODEL_ARG="${MODEL_ARG:-opus}"
case "$MODEL_ARG" in
    haiku)   MODEL_NAME="claude-haiku-4-5";  MODEL_CLI="haiku" ;;
    sonnet)  MODEL_NAME="claude-sonnet-4-6"; MODEL_CLI="sonnet" ;;
    opus)    MODEL_NAME="claude-opus-4-6";   MODEL_CLI="opus" ;;
    *)       MODEL_NAME="$MODEL_ARG";        MODEL_CLI="$MODEL_ARG" ;;
esac

# Ensure max_rounds is a valid number, default to 3 if not
if ! [[ "$MAX_ROUNDS" =~ ^[0-9]+$ ]]; then
    echo "Error: MAX_ROUNDS must be a number."
    exit 1
fi

# ==========================================
# Important Argument Settings for Experiment
# ==========================================
PERMISSION_MODE="bypassPermissions"   # Set to bypass permissions for Claude tools by default
ALLOW_SORRY="false"                   # Strict correctness (treats sorry as an error)
OUTPUT_FORMAT="json"                  # Forces Claude stdout output format to structural JSON
TRACK_STATEMENTS="true"               # Tracks theorem/lemma modifications using StatementTracker across rounds
GIT_COMMIT="true"                     # Automatically creates a git commit after each round for step-by-step history tracking
CHECK_AFTER_COMPLETE="true"           # Verify files via compilation after Claude finishes round
# USE_FAILURE_MEMORY               — set via --failure-memory flag (training-free RL)
# DISABLE_GUARD                    — set via --no-guard flag (disable mathlib tool guard hook)

# ==========================================
# MCP Isolation: Only load research MCP servers (lean-lsp, gemini)
# Uses --strict-mcp-config to block personal MCP servers (Figma, Gmail, Calendar, Notion, plugins)
# ==========================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_CONFIG="${SCRIPT_DIR}/configs/experiment_mcp.json"
LEAN_PROJECT_ROOT="${SCRIPT_DIR}/leanproblems"
SANDBOXES_DIR="${SCRIPT_DIR}/sandboxes"

# Extract BENCHMARK_PATH and PROBLEM_NAME from TARGET_PATH
# BENCHMARK_PATH is relative to leanproblems/ (e.g. shadowbench_lift_wo_nl_proof/L1/algebra)
PROBLEM_DIR="$(dirname "$TARGET_PATH")"
BENCHMARK_PATH="${PROBLEM_DIR#leanproblems/}"
[ "$BENCHMARK_PATH" = "$PROBLEM_DIR" ] && BENCHMARK_PATH="$(basename "$PROBLEM_DIR")"
BENCHMARK="$BENCHMARK_PATH"  # kept for reference in echo output

if [ -f "$TARGET_PATH" ]; then
    PROBLEM_NAME=$(basename "$TARGET_PATH" .lean)
    TASK_TYPE="file"
else
    PROBLEM_NAME=$(basename "$TARGET_PATH")
    TASK_TYPE="folder"
fi

DATETIME=$(date +"%Y%m%d_%H%M%S")
# Default experiment name to model+datetime when --name is not supplied
EXPERIMENT_NAME="${EXPERIMENT_NAME:-${MODEL_CLI}_${DATETIME}}"

# Format: results/{EXPERIMENT_NAME}/{BENCHMARK_PATH}/{PROBLEM_NAME}/
# Must be absolute — MCP servers are spawned with a different cwd and need absolute paths.
OUT_DIR="${SCRIPT_DIR}/results/${EXPERIMENT_NAME}/${BENCHMARK_PATH}/${PROBLEM_NAME}"
mkdir -p "$OUT_DIR"

# Create sandbox in dedicated sandboxes/ directory (isolated from leanproblems/)
# Symlinks provide Lean project infrastructure so compilation works without exposing other problem files
mkdir -p "$SANDBOXES_DIR"
SANDBOX_NAME="${PROBLEM_NAME}_${DATETIME}_${EXPERIMENT_NAME}"
sandbox_target="${SANDBOXES_DIR}/${SANDBOX_NAME}"

echo "Creating isolated sandbox at ${sandbox_target}..."
mkdir -p "${sandbox_target}"
cp -r "$TARGET_PATH" "${sandbox_target}/"

# Symlink Lean project infrastructure so compilation and lean-lsp work from the sandbox.
# .lake/packages/ (pre-compiled mathlib oleans) is shared read-only via symlink.
# .lake/build/ is a fresh per-sandbox directory so parallel Lean LSP processes
# don't write to the same mmap'd .olean files (which causes SIGBUS / hangs).
mkdir -p "${sandbox_target}/.lake/build"
ln -sf "${LEAN_PROJECT_ROOT}/.lake/packages"     "${sandbox_target}/.lake/packages"
ln -sf "${LEAN_PROJECT_ROOT}/lakefile.toml"      "${sandbox_target}/lakefile.toml"
ln -sf "${LEAN_PROJECT_ROOT}/lean-toolchain"     "${sandbox_target}/lean-toolchain"
ln -sf "${LEAN_PROJECT_ROOT}/lake-manifest.json" "${sandbox_target}/lake-manifest.json"

if [ "$TASK_TYPE" = "file" ]; then
    RUN_TARGET="${sandbox_target}/${PROBLEM_NAME}.lean"
else
    RUN_TARGET="${sandbox_target}/${PROBLEM_NAME}"
fi

# Cleanup trap: copy final solution to OUT_DIR and remove sandbox on exit (success or failure)
_cleanup_sandbox() {
    local _exit=$?
    if [ -d "${sandbox_target}" ]; then
        echo "→ Saving final answer to ${OUT_DIR}/ ..."
        if [ "$TASK_TYPE" = "file" ] && [ -f "${RUN_TARGET}" ]; then
            cp "${RUN_TARGET}" "${OUT_DIR}/final_answer.lean"
        elif [ "$TASK_TYPE" = "folder" ] && [ -d "${RUN_TARGET}" ]; then
            mkdir -p "${OUT_DIR}/final_answer"
            cp -r "${RUN_TARGET}/." "${OUT_DIR}/final_answer/"
        fi
        echo "→ Removing sandbox ${sandbox_target} ..."
        rm -f "${OUT_DIR}/sandbox"
        rm -rf "${sandbox_target}"
        echo "  ✓ Sandbox cleaned up."
    fi
    exit $_exit
}
trap _cleanup_sandbox EXIT

# Symlink sandbox into OUT_DIR for easy access from results (removed after experiment)
ln -sfn "$(cd "${sandbox_target}" && pwd)" "${OUT_DIR}/sandbox"

CONFIG_FILE="${OUT_DIR}/config.yaml"

# Generate per-experiment MCP config with a unique server name.
# Claude Code identifies MCP servers by name and may reuse background processes
# across invocations with the same name — giving each experiment a unique name
# (lean-lsp-<sandbox>) guarantees a fresh, independent server process per experiment.
EXP_MCP_CONFIG="${OUT_DIR}/mcp_config.json"
cat <<MCPEOF > "$EXP_MCP_CONFIG"
{
  "mcpServers": {
    "lean-lsp-${SANDBOX_NAME}": {
      "command": "lean-lsp-mcp/numina-lean-mcp.sh",
      "args": [],
      "env": {
        "MCP_LOG_NAME": "${PROBLEM_NAME}_mcp",
        "MCP_LOG_DIR": "${OUT_DIR}/mcp_logs"
      }
    }
  }
}
MCPEOF

# Generate YAML Configuration
cat <<EOF > "$CONFIG_FILE"
defaults:
  task_type: "${TASK_TYPE}"
  prompt_file: "${PROMPT_FILE}"
  cwd: "${sandbox_target}"
  max_rounds: ${MAX_ROUNDS}
  check_after_complete: ${CHECK_AFTER_COMPLETE}
  permission_mode: "${PERMISSION_MODE}"

  # ==========================================
  # Maximal Logging & Dumping Configurations
  # ==========================================
  result_dir: "${OUT_DIR}/results"       # Dumps detailed JSON results including line counts, duration, round details
  mcp_log_dir: "${OUT_DIR}/mcp_logs"     # Dumps raw MCP traffic logs and generates mcp_stats.json tool execution summary
  output_format: stream-json             # Streams JSON for runN.log dump while python wrapper parses live text output
  track_statements: ${TRACK_STATEMENTS}  # Statement tracking
  git_commit: ${GIT_COMMIT}              # Git commits
  allow_sorry: ${ALLOW_SORRY}            # Sorry allowances
  use_failure_memory: ${USE_FAILURE_MEMORY}  # Training-free RL via failure memory
  mcp_config: "${EXP_MCP_CONFIG}"            # Per-experiment MCP config (unique server name for isolation)
  model: "${MODEL_CLI}"                        # Claude model (alias or full name)
  effort: "${EFFORT_ARG}"                      # Effort level (extended thinking: low/medium/high/xhigh/max)
  disallowed_tools:                            # Hard deny list: block results/ access even with bypassPermissions
    - "Read(${SCRIPT_DIR}/results/**)"
    - "Write(${SCRIPT_DIR}/results/**)"
    - "Edit(${SCRIPT_DIR}/results/**)"
    - "Bash(*${SCRIPT_DIR}/results*)"

tasks:
  - target_path: "${RUN_TARGET}"
    mcp_log_name: "${PROBLEM_NAME}_mcp"
EOF

echo "=================================================="
echo "Experiment Configuration Generated"
echo "Experiment: ${EXPERIMENT_NAME}"
echo "Target: $TARGET_PATH ($TASK_TYPE)"
echo "Model: $MODEL_NAME"
[ -n "$EFFORT_ARG" ] && echo "Effort: $EFFORT_ARG"
echo "Max Rounds: $MAX_ROUNDS"
echo "Failure Memory: $USE_FAILURE_MEMORY"
echo "Mathlib Guard: $([ -n "$DISABLE_GUARD" ] && echo 'disabled' || echo 'enabled')"
echo "MCP Config: $MCP_CONFIG (strict isolation)"
echo "Output Directory: $OUT_DIR"
echo "Config File: $CONFIG_FILE"
echo "=================================================="

# Run the experiment using the batch sequence which reads our config mapping
source ./.venv/bin/activate

# Disable mathlib tool guard hook if --no-guard flag is set
if [ -n "$DISABLE_GUARD" ]; then
    export DISABLE_MATHLIB_GUARD=1
fi

python3 -m scripts.run_claude batch "$CONFIG_FILE"

# If run by root, change ownership of the results to anonymous so they can read/edit them
if [ "$(id -u)" -eq 0 ] && id -u anonymous >/dev/null 2>&1; then
    echo "Transferring ownership of results to anonymous..."
    chown -R anonymous:anonymous "$OUT_DIR"
fi
