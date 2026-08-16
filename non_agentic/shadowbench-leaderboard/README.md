# Multiple tunnel forwarding without running a remote shell

ssh -N \
  -L 8100:127.0.0.1:8100 \
  -L 8000:127.0.0.1:8000 \
  -L 5000:127.0.0.1:5000 \
  user@example.org -p 41705



# ShadowBench Leaderboard + Benchmark Runner (scaffold)

This folder wires the provided leaderboard UI to a small FastAPI backend that:

1) Accepts a **submission** (`POST /api/submissions`)
2) Runs your benchmark harness in `~/shadowbench/shadowbench-benchmark` (or wherever you point it)
3) Stores the resulting metrics
4) Serves `GET /api/leaderboard.json` for the page to render

> ✅ You only need to adapt **one thing**: the command that actually runs your benchmark and writes a JSON result.

---

## Quick start (host runner)

### 1) Install deps

```bash
python -m venv .venv
source .venv/bin/activate

source ~/venvs/shadowbench/bin/activate
pip install -r backend/requirements.txt
```

### 2) Configure how to run your benchmark

By default the server expects a script at:

```
$SHADOWBENCH_BENCHMARK_DIR/score_submission.py
```

and will run:

```
python score_submission.py --spec <spec.json> --out <result.json>
```

Set these environment variables to match your real harness:

```bash
export SHADOWBENCH_BENCHMARK_DIR="$HOME/shadowbench/shadowbench-benchmark"
export SHADOWBENCH_BENCHMARK_RUNNER='python score_submission.py --spec {spec} --out {out}'
export SHADOWBENCH_BENCHMARK_TIMEOUT_SEC=7200
```

**Placeholders:** `{spec}` is the JSON submission spec file path, `{out}` is where your runner must write result JSON.

A minimal example scorer stub is provided at `backend/example_score_submission.py` for you to copy into your benchmark repo.

### 3) Run the API

Run from the folder that contains `backend/`:

```bash
uvicorn backend.app:app --port 8000
```

**Dev reload:** If `--reload` hits an OS file-watch limit, restrict the watched directory:

```bash
uvicorn backend.app:app --reload --reload-dir backend --port 8000
```

### 4) Serve the frontend

3) Créer le fichier de config Nginx pour leaderboard.example.org

Crée un “server block” :

sudo nano /etc/nginx/sites-available/leaderboard.example.org

Colle ceci (adapte seulement root et le port backend si besoin) :

server {
    listen 80;
    server_name leaderboard.example.org;

    # Frontend statique
    root non_agentic/shadowbench-leaderboard/frontend;

    # Autoriser uniquement leaderboard.html
    location = /leaderboard.html {
        try_files $uri =404;
    }

    # Autoriser uniquement leaderboard.html
    location = /submit.test-run.html {
        try_files $uri =404;
    }

    # Autoriser uniquement tes assets (adapte si ton dossier s'appelle autrement)
    location /assets/ {
        try_files $uri =404;
    }

    # Backend API (CHANGE LE PORT si ton backend n’est pas 8200)
    location /api/ {
        proxy_pass http://127.0.0.1:8200/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
    }

    # Bloquer tout le reste
    location / {
        return 403;
    }
}
Activer le site
sudo ln -s /etc/nginx/sites-available/leaderboard.example.org /etc/nginx/sites-enabled/

Désactiver le default (sinon conflit possible) :

sudo rm -f /etc/nginx/sites-enabled/default

Tester + recharger :

sudo nginx -t
sudo systemctl reload nginx