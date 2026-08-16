#!/usr/bin/env bash
# submit_all.sh — submit every experiment defined in the YAML file
#
# Usage:
#   ./submit_all.sh <experiments.yaml>
#
# Example:
#   ./submit_all.sh submit/experiments/naive_prompting.yaml

set -euo pipefail

YAML="${1:?Usage: $0 <experiments.yaml>}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBMIT="$SCRIPT_DIR/submit_one.sh"

if [[ ! -f "$YAML" ]]; then
    echo "File not found: $YAML" >&2
    exit 1
fi

python3 - "$YAML" "$SUBMIT" <<'EOF'
import sys, subprocess, itertools, json, yaml

yaml_path = sys.argv[1]
submit_sh = sys.argv[2]

from pathlib import Path
yaml_stem = Path(yaml_path).stem   # e.g. "naive_prompting"

with open(yaml_path) as f:
    data = yaml.safe_load(f)

# ── Sweep axes ────────────────────────────────────────────────────────────────
models       = data.get("models", [])
max_tokens   = [int(t)   for t in data.get("max_tokens",   [])]
temperatures = [float(t) for t in data.get("temperatures", [])]

if not models or not max_tokens or not temperatures:
    print("YAML must define all of: models, max_tokens, temperatures")
    sys.exit(1)

# ── Shared config (defaults) ──────────────────────────────────────────────────
default_org = data.get("org", "anonymous-org")

default_areas = data.get("areas", [
    "algebra", "topology", "analysis", "number-theory",
    "logic", "category-theory", "probability",
    "geometry", "college-math-competition",
])
default_levels = data.get("levels", ["L1", "L2", "L3", "L4"])

default_prompt = {
    "informal_statement":  True,
    "informal_proof":      True,
    "formalization_rules": True,
    "imports":             True,
    "aux_theorems":        True,
    "formal_statement":    False,
    "dpp":                 False,
}
default_prompt.update(data.get("prompt_components", {}))

# ── New eval / bench fields (with payload defaults) ───────────────────────────
default_two_phase           = data.get("two_phase_evaluation", True)
default_lean_version        = data.get("lean_version", "v4.27.0-rc1")
default_hidden_checker_only = data.get("hidden_checker_only", True)
default_hidden_checker_sets = data.get("hidden_checker_sets", [1, 2])

# ── Build all combinations ────────────────────────────────────────────────────
combos = list(itertools.product(models, max_tokens, temperatures))
print(f"Total {len(combos)} combinations  "
      f"({len(models)} models × {len(max_tokens)} tokens × {len(temperatures)} temps)")
print(f"areas  : {default_areas}")
print(f"levels : {default_levels}")
print(f"prompts: {default_prompt}\n")

failed = []
for i, (model, tokens, temp) in enumerate(combos, 1):
    model_short = model.removeprefix("op/").removesuffix(":floor")
    name = f"{model_short};l={tokens};t={temp} ({yaml_stem})"

    cfg = json.dumps({
        "name":                  name,
        "org":                   default_org,
        "model":                 model,
        "max_tokens":            tokens,
        "temperature":           temp,
        "areas":                 default_areas,
        "levels":                default_levels,
        "prompt_components":     default_prompt,
        "two_phase_evaluation":  default_two_phase,
        "lean_version":          default_lean_version,
        "hidden_checker_only":   default_hidden_checker_only,
        "hidden_checker_sets":   default_hidden_checker_sets,
    })

    print(f"[{i}/{len(combos)}] {name}")
    result = subprocess.run(["bash", submit_sh, cfg], capture_output=True, text=True)
    if result.returncode == 0:
        print("  " + result.stdout.strip())
    else:
        print("  FAILED: " + result.stderr.strip())
        failed.append(name)

print(f"\nDone. {len(combos) - len(failed)}/{len(combos)} succeeded.")
if failed:
    print("Failed:")
    for name in failed:
        print(f"  {name}")
    sys.exit(1)
EOF
