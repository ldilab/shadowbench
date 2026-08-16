# ShadowBench

**An autoformalization benchmark and agentic theorem-proving harness in Lean 4.**

ShadowBench packages two complementary contributions in a single repository:

1. **An agentic solver** (`agentic/`) — *ShadowBench Agent*, a Claude Code-based system for
   formal theorem proving. The four shell entrypoints under `agentic/commands/` reproduce both
   the agentic and the single-shot baseline experiments reported in the paper.
2. **A non-agentic leaderboard benchmark** (`non_agentic/`) — *ShadowBench*: a curated suite
   of Lean 4 problems, a containerized evaluator, and a FastAPI leaderboard server. Participants
   submit jobs to a hosted instance via the `non_agentic/submit/` client.

This repository ships the **public split** of the benchmark: the informal theorems and the
formalization rules for all 179 problems (`data/`). The gold formalizations and the hidden
shadow checkers used for scoring are kept private and live only on the evaluation server.

---

## Repository layout

```
shadowbench/
├── agentic/                      # Track A — ShadowBench Agent (Claude Code)
│   ├── commands/                 #   four shell entrypoints (single / folder × agentic / naive)
│   ├── scripts/                  #   Python orchestration, judges, BEQ scoring, statement tracker
│   ├── prompts/                  #   prompt templates (medium / hard / naive_*)
│   ├── configs/                  #   MCP server configs (experiment_mcp.json, empty_mcp.json)
│   ├── config/                   #   YAML examples (config_minif2f.yaml)
│   ├── conftest.py, pytest.ini   #   pytest plumbing
│   └── leanproblems → <your Lean project>  #   ← symlink created during setup (see Track A)
│
├── non_agentic/                  # Track B — Hosted ShadowBench leaderboard
│   ├── shadowbench-leaderboard/          #   FastAPI backend + static frontend (the host)
│   │   ├── backend/              #     app.py, runner.py, db.py, settings.py, requirements.txt
│   │   └── frontend/             #     leaderboard.html, submit.test-run.html, admin UI, assets
│   ├── shadowbench-benchmark/            #   the evaluator (benchmark data kept private)
│   │   ├── score_submission.py   #     evaluator entrypoint
│   │   ├── run_benchmark.sh      #     local-run wrapper
│   │   ├── scripts/              #     docker_score.sh (optional runner wrapper)
│   │   ├── lean-toolchain        #     pinned Lean version
│   │   ├── sample_submission_spec.json, sample_result.json
│   │   └── lean-benchmark-guideline.md
│   └── submit/                   #   participant-side submission client
│       ├── submit_one.sh         #     POST a single submission to the leaderboard
│       ├── submit_all.sh         #     batch sweep over experiments/*.yaml
│       ├── sync_runs.py          #     pull completed runs back from the leaderboard
│       ├── models.yaml           #     model registry
│       └── experiments/          #     YAML sweep configs (shadow.yaml, proving*.yaml, ...)
│
├── data/                         # public split of the 179 ShadowBench problems
└── README.md                     # ← you are here
```

---

## Dataset

`data/` contains the public split of all 179 ShadowBench problems, laid out as
`data/<area>/<level>/<problem_id>/`:

- `text.md` — the informal source document: the theorem to formalize, with the
  surrounding definitions and the informal proof.
- `meta.json` — the task specification: problem identifiers, area, level,
  `formalization_rules` (required preamble, target declaration name, and constraints),
  `target_decl` / `target_kind`, custom modules, toolchain pin, and source references.

The gold Lean formalizations and the hidden shadow checkers used for scoring are **not**
included. Evaluation against them runs on the hosted leaderboard (Track B below).

Directory levels and problem identifiers use the paper's difficulty scale `L1`–`L3`
(for example, `analysis/L1/ana_gen_L1_003`).

| Area | L1 | L2 | L3 | Total |
| --- | ---: | ---: | ---: | ---: |
| algebra | 19 | 4 | 3 | 26 |
| algebraic-geometry | 2 | 16 | 4 | 22 |
| analysis | 14 | 10 | 4 | 28 |
| combinatorics | 8 | 6 | 0 | 14 |
| geometry | 18 | 6 | 0 | 24 |
| number-theory | 17 | 0 | 2 | 19 |
| probability | 19 | 1 | 0 | 20 |
| topology | 17 | 9 | 0 | 26 |
| **Total** | **114** | **52** | **13** | **179** |

---

## Agentic

A Claude Code-based agent that drives a Lean 4 toolchain (via `lean-lsp-mcp`) to produce and
verify formal proofs over multiple rounds.

### Prerequisites

- **Lean 4** via `elan` (the toolchain version is pinned by
  `non_agentic/shadowbench-benchmark/lean-toolchain`).
- **Python 3.10+** with `venv`.
- **Claude Code CLI** (`claude`) on your `PATH`. See
  https://github.com/anthropics/claude-code for installation.
- **`lean-lsp-mcp`** — the MCP server used by `run_experiment.sh` is invoked as
  `lean-lsp-mcp/numina-lean-mcp.sh`. Clone or install it as a sibling so this relative path
  resolves from the experiment sandbox. (The companion implementation is *ShadowBench Lean LSP MCP*.)

### Setup

```bash
cd agentic

# 1. Bridge a Lean 4 project of problem files into agentic/leanproblems/
#    (all four scripts reference leanproblems/). The public data/ split ships
#    informal statements only, so point this at your own Lean project of
#    problem .lean files.
ln -s <path-to-your-lean-project> leanproblems

# 2. Python environment (the scripts source agentic/.venv/bin/activate)
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install pyyaml      # plus any further deps used by scripts/run_claude.py
```

### The four entrypoints

All commands are run **from inside `agentic/`** so that `leanproblems/...` paths resolve.

| Script | What it does |
| --- | --- |
| `commands/run_experiment.sh <PROBLEM.lean> <MAX_ROUNDS> [flags]`           | Agentic run on a single problem. Spawns an isolated sandbox with a per-experiment MCP server, multi-round agent loop, statement tracking, and per-round git commits. |
| `commands/run_folder_experiment.sh <FOLDER> <MAX_ROUNDS> [flags]`          | Sequentially calls `run_experiment.sh` over every `.lean` file in `<FOLDER>`. Tracks success / failed / skipped counts. |
| `commands/run_naive_claude.sh <PROBLEM.lean> [flags]`                      | Single-shot baseline. Calls Claude with no tools and no MCP servers, then compiles the response with `lake env lean`. Two modes: `--mode autoformalize` (extract NL from comments) or `--mode complete` (full Lean file). |
| `commands/run_naive_claude_folder.sh <FOLDER> [flags]`                     | Batch baseline runner. Performs a Mathlib cache pre-flight (SIGBUS detection, cache repair) before sweeping a folder. |

#### Common flags

| Flag                              | Default     | Where           |
| --------------------------------- | ----------- | --------------- |
| `--model {opus\|sonnet\|haiku}`   | `opus`      | all             |
| `--effort {low\|medium\|high\|xhigh\|max}` | unset | all             |
| `--name <EXPERIMENT_NAME>`        | `<model>_<datetime>` (agentic) / `naive_claude_code` (baseline) | all |
| `--failure-memory`                | off         | agentic only    |
| `--no-guard`                      | on (guard disabled by default in scripts) | agentic only |
| `--mode {autoformalize\|complete}` | `autoformalize` | naive only |
| `--timeout <SECONDS>`             | `300`       | naive only      |
| `--skip-existing`                 | on          | folder runners  |
| `--recursive`                     | off         | naive folder    |
| `--keep-sandbox`                  | off         | naive only      |

#### Examples

```bash
# Agentic, single problem, 3 rounds, default model (opus)
./commands/run_experiment.sh leanproblems/<dataset>/<problem>.lean 3

# Agentic, full subfolder with failure-memory RL and a custom name
./commands/run_folder_experiment.sh leanproblems/<dataset>/<subfolder> 3 \
    --name ablation_full --failure-memory

# Naive baseline, single problem, "complete" mode
./commands/run_naive_claude.sh leanproblems/<dataset>/<problem>.lean \
    --mode complete --model sonnet

# Naive baseline, recursive folder
./commands/run_naive_claude_folder.sh leanproblems/<dataset> \
    --recursive --name L1_naive
```

Outputs land in `agentic/results/<EXPERIMENT_NAME>/<BENCHMARK_PATH>/<PROBLEM_NAME>/` —
streaming logs (`run<N>.log`), per-round JSON, MCP traffic (`mcp_logs/`),
`final_answer.lean`, and a generated `config.yaml`.

#### Known issues

- `agentic/scripts/statement_tracker.py:9` imports `extract_sublemmas`. The corresponding
  `agentic/scripts/extract_sublemmas.py` is not part of this snapshot; the import fails when
  `python3 -m scripts.run_claude` is invoked. If you hit `ModuleNotFoundError: extract_sublemmas`,
  stub the module (`pass`-only) or remove the import in `statement_tracker.py` for runs that do
  not exercise sub-lemma extraction.

---

## Non-agentic ShadowBench

Three pieces — all coordinated by environment variables, no hard-coded paths:

```
   participant                 hosted leaderboard               evaluator
┌─────────────────┐          ┌────────────────────┐          ┌────────────────────┐
│ submit/         │  HTTPS   │ shadowbench-leaderboard/   │  subproc │ shadowbench-benchmark/     │
│ submit_one.sh   │ ───────▶ │  backend/app.py    │ ───────▶ │  score_submission  │
│ submit_all.sh   │  POST    │   /api/submissions │          │   .py + data/      │
│ sync_runs.py    │ ◀─────── │   /api/leaderboard │          │  Dockerfile.shadowbench-… │
└─────────────────┘   GET    └────────────────────┘          └────────────────────┘
```

### B.1 Run the leaderboard server

```bash
cd non_agentic/shadowbench-leaderboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt

export SHADOWBENCH_BENCHMARK_DIR="$(pwd)/../shadowbench-benchmark"
export SHADOWBENCH_BENCHMARK_RUNNER="python score_submission.py --spec {spec} --out {out}"
export ADMIN_PASSWORD="<long-random-secret>"   # optional; protects /api/admin/*
# optional tuning:
#   LEADERBOARD_DB=./data/leaderboard.sqlite
#   SHADOWBENCH_BENCHMARK_TIMEOUT_SEC=3600
#   LEADERBOARD_MAX_WORKERS=1
#   LEADERBOARD_ALLOW_ORIGINS="https://your.host"

uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

Routes:

- `POST /api/submissions` — accept a `SubmissionIn` JSON, queue an evaluator subprocess.
- `GET  /api/leaderboard.json` — ranked runs for the static frontend.
- `GET  /api/downloads/...`   — completed-run artifacts (used by `submit/sync_runs.py`).
- `*    /api/admin/...`       — admin-only endpoints, gated by `ADMIN_PASSWORD`.

The static frontend lives under `frontend/` (`leaderboard.html`,
`leaderboard.admin.html`, `submit.test-run.html`). Serve it behind any reverse proxy that
forwards `/api/*` to uvicorn (a sample systemd unit lives at
`shadowbench-leaderboard/README_systemd.md`).

### B.2 Run the evaluator locally (sanity check)

```bash
cd non_agentic/shadowbench-benchmark
python score_submission.py \
    --spec sample_submission_spec.json \
    --out  /tmp/abm_result.json
```

Or via the optional Docker wrapper:

```bash
bash scripts/docker_score.sh sample_submission_spec.json /tmp/abm_result.json
```

`Dockerfile.shadowbench-eval` builds the container image referenced from a submission spec's
`runtime.docker_image` field.

### B.3 Submit a job (participant client)

`non_agentic/submit/submit_one.sh` POSTs a single submission. `submit_all.sh` reads a YAML sweep
config (Cartesian product over models × tokens × temperatures × areas × levels) and calls
`submit_one.sh` once per combination. `sync_runs.py` pulls completed runs from the leaderboard
back to a local results tree.

```bash
cd non_agentic/submit

export SHADOWBENCH_SUBMIT_URL="https://<your-leaderboard-host>/api/submissions"
export SHADOWBENCH_API_KEY="<your-token>"
# (optional) override download endpoint used by sync_runs.py:
# export SHADOWBENCH_DOWNLOAD_BASE_URL="https://<your-leaderboard-host>/api/downloads"

# Single submission:
./submit_one.sh "$(cat <<'EOF'
{
  "name": "my-run-001",
  "org":  "my-team",
  "model": "claude-sonnet-4-6",
  "max_tokens": 8192,
  "temperature": 0.6,
  "areas":  ["algebra", "topology"],
  "levels": ["L1", "L2"],
  "prompt_components": {"informal_statement": true}
}
EOF
)"

# Sweep from a YAML config (see experiments/shadow.yaml for the full schema):
./submit_all.sh experiments/shadow.yaml

# Pull completed runs:
python sync_runs.py
```

The submission body sent on the wire wraps the user's config inside a `submissionSpec` envelope
(`model_cmd`, `env`, `eval`, `runtime`, `bench`) — see `submit_one.sh` for the exact schema and
how environment variables (`VLLM_BASE_URL`, `VLLM_MODEL`, `SHADOWBENCH_EVAL_PROJECT_DIR`, ...) are
threaded through.

---

## Reproducing paper results

| Sweep                            | Config                                  | Notes |
| -------------------------------- | --------------------------------------- | ----- |
| Main non-agentic table           | `non_agentic/submit/experiments/shadow.yaml` | Full ShadowBench sweep, hidden checker enabled |
| "Proving" ablation               | `non_agentic/submit/experiments/proving.yaml` | Without auxiliary-lemma exposure |
| "Proving (with NL)"              | `non_agentic/submit/experiments/proving_w_nl.yaml` | Adds informal statement |
| "Proving (no aux)"               | `non_agentic/submit/experiments/proving_wo_aux.yaml` | Drops auxiliary lemmas |
| Agentic numbers                  | `agentic/commands/run_folder_experiment.sh leanproblems/<dataset> <ROUNDS> --model <opus\|sonnet\|haiku>` | One folder per row |
| Single-shot Claude baseline      | `agentic/commands/run_naive_claude_folder.sh leanproblems/<dataset> --mode {autoformalize\|complete}` | |

Result post-processing scripts live under `agentic/scripts/` (judges, BEQ scoring, MCP stats).

---

## Quick start at a glance

```bash
git clone <this-repo> && cd shadowbench

# Track A — agentic
cd agentic
ln -s <path-to-your-lean-project> leanproblems
python3 -m venv .venv && source .venv/bin/activate && pip install pyyaml
./commands/run_naive_claude.sh leanproblems/<dataset>/<problem>.lean --mode complete

# Track B — leaderboard (in another shell)
cd ../non_agentic/shadowbench-leaderboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
SHADOWBENCH_BENCHMARK_DIR="$(pwd)/../shadowbench-benchmark" \
    uvicorn backend.app:app --port 8000

# Track B — submit a job (yet another shell)
cd ../submit
SHADOWBENCH_SUBMIT_URL="http://localhost:8000/api/submissions" \
SHADOWBENCH_API_KEY="dev" \
    ./submit_all.sh experiments/shadow.yaml
```

---

