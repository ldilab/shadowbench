#!/usr/bin/env bash
set -euo pipefail

SPEC=""
OUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --spec) SPEC="$2"; shift 2;;
    --out)  OUT="$2";  shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

[[ -n "$SPEC" ]] || { echo "--spec required" >&2; exit 2; }
[[ -n "$OUT"  ]] || { echo "--out required" >&2; exit 2; }
[[ -f "$SPEC" ]] || { echo "spec file not found: $SPEC" >&2; exit 2; }

# Default model command (relative to repo root)
MODEL_CMD="./submissions/dummy_model.sh"

# If jq exists, let spec override model.command
if command -v jq >/dev/null 2>&1; then
  OVERRIDE="$(jq -r '.model.command // empty' "$SPEC" 2>/dev/null || true)"
  if [[ -n "${OVERRIDE:-}" && "${OVERRIDE:-}" != "null" ]]; then
    MODEL_CMD="$OVERRIDE"
  fi
fi

# If command is relative, resolve relative to repo root (current working directory)
if [[ "$MODEL_CMD" != /* ]]; then
  MODEL_CMD="$PWD/$MODEL_CMD"
fi

[[ -x "$MODEL_CMD" ]] || { echo "model command not executable: $MODEL_CMD" >&2; exit 2; }

PROMPT="Give a Lean proof of True."
# Timing (nanoseconds if supported; falls back to 0.01)
START_NS="$(date +%s%N 2>/dev/null || echo "")"
ANS="$("$MODEL_CMD" "$PROMPT" 2>/dev/null || true)"
END_NS="$(date +%s%N 2>/dev/null || echo "")"

ELAPSED_SEC="0.01"
if [[ -n "${START_NS:-}" && -n "${END_NS:-}" ]]; then
  # Guard: ensure both are integers
  if [[ "$START_NS" =~ ^[0-9]+$ && "$END_NS" =~ ^[0-9]+$ && "$END_NS" -ge "$START_NS" ]]; then
    DIFF_NS=$((END_NS - START_NS))
    # awk is ubiquitous; convert ns -> seconds as float
    ELAPSED_SEC="$(awk -v ns="$DIFF_NS" 'BEGIN { printf "%.6f", ns/1000000000 }')"
  fi
fi


# Toy scoring: "by trivial" => success
OVERALL="0.0"
if echo "$ANS" | grep -qi "by trivial"; then
  OVERALL="10.0"
fi

cat > "$OUT" <<JSON
{
  "overall": $OVERALL,
  "pass1": $OVERALL,
  "pass5": $OVERALL,
  "compileRate": 0.0,
  "avgTimeSec": $ELAPSED_SEC,
  "usdPerTask": 0.0,
  "tokensPerTask": 0,
  "categories": { "smoke": $OVERALL },
  "envHash": "run_benchmark.sh"
}
JSON

echo "OK wrote metrics to $OUT (overall=$OVERALL)" >&2
