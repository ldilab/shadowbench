#!/usr/bin/env bash
# submit_one.sh — Submit a single experiment to the ShadowBench leaderboard
#
# Usage (internal — invoked by submit_all.sh):
#   ./submit_one.sh <json_config_string>
#
# json_config fields:
#   name, org, model, max_tokens, temperature,
#   areas, levels, prompt_components

set -euo pipefail

JSON_CONFIG="${1:?json config required}"

API_URL="${SHADOWBENCH_SUBMIT_URL:-https://api.leaderboard.example.org/api/submissions}"
API_KEY="${SHADOWBENCH_API_KEY:?Set SHADOWBENCH_API_KEY before submitting}"

BODY=$(python3 -c "
import json, os, sys

cfg = json.loads(sys.argv[1])

body = {
    'name': cfg['name'],
    'org':  cfg.get('org', 'anonymous-org'),
    'track': 'Open',
    'license': '—',
    'tags': ['test'],
    'submissionSpec': {
        'model_cmd': cfg.get('model_cmd') or os.environ.get('SHADOWBENCH_MODEL_CMD', 'models/qwen235b_remote/model.py'),
        'env': {
            'VLLM_BASE_URL':        cfg.get('vllm_base_url') or os.environ.get('VLLM_BASE_URL', 'http://127.0.0.1:1235/v1'),
            'VLLM_MODEL':           cfg['model'],
            'VLLM_MAX_TOKENS':      str(cfg['max_tokens']),
            'VLLM_TEMPERATURE':     str(cfg['temperature']),
            'VLLM_CONNECT_TIMEOUT': '3.0',
            'VLLM_READ_TIMEOUT':    '540.0',
            'SHADOWBENCH_MAX_TASKS':        '22',
        },
        'eval': {
            'num_problems': 500,
            'areas':    cfg['areas'],
            'levels':   cfg['levels'],
            'seed':     1337,
            'sampling': 'hash',
            'prompt_components': cfg['prompt_components'],
            'two_phase_evaluation': cfg.get('two_phase_evaluation', True),
            'lean_version':         cfg.get('lean_version', 'v4.27.0-rc1'),
            'hidden_checker_only':  cfg.get('hidden_checker_only', True),
            'hidden_checker_sets':  cfg.get('hidden_checker_sets', [1, 2]),
        },
        'runtime': {
            'docker_image':     'shadowbench/lean-eval:lean4.26.0-data',
            'eval_project_dir': cfg.get('eval_project_dir') or os.environ.get('SHADOWBENCH_EVAL_PROJECT_DIR', 'leanproblems'),
            'docker_network':   'none',
            'model_timeout_sec':   600,
            'compile_timeout_sec': 180,
        },
        'bench': {
            'prompt_components': cfg['prompt_components'],
            'limit':    500,
            'seed':     1337,
            'sampling': 'hash',
            'areas':    cfg['areas'],
            'levels':   cfg['levels'],
            'two_phase_evaluation': cfg.get('two_phase_evaluation', True),
            'hidden_checker_only':  cfg.get('hidden_checker_only', True),
            'hidden_checker_sets':  cfg.get('hidden_checker_sets', [1, 2]),
        },
    },
}
print(json.dumps(body))
" "$JSON_CONFIG")

CURL_ARGS=(
    -s -X POST "$API_URL"
    -H "Content-Type: application/json"
    -H "Authorization: Bearer $API_KEY"
    -d "$BODY"
)

RESPONSE=$(curl "${CURL_ARGS[@]}")
STATUS=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null || echo "")

if [[ "$STATUS" == "queued" ]]; then
    SUBMISSION_ID=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('submission_id',''))")
    echo "✓ Queued: $SUBMISSION_ID"
else
    echo "✗ Unexpected response:" >&2
    echo "$RESPONSE" | python3 -m json.tool >&2
    exit 1
fi
