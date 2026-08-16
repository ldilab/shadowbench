from __future__ import annotations

import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Optional

import os
import shutil
from pathlib import Path
import math

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from .db import (
    SubmissionRow,
    create_submission,
    get_submission,
    init_db,
    list_completed_runs,
    list_submissions,
    delete_submission,
    set_submission_run,
    update_submission,
    update_submission_status,
)
from .runner import BenchmarkRunError, run_benchmark
from .settings import Settings, load_settings

SETTINGS: Settings = load_settings()
init_db(SETTINGS.db_path)

app = FastAPI(title="ShadowBench Leaderboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXECUTOR = ThreadPoolExecutor(max_workers=SETTINGS.max_workers)

DEFAULT_WHATS_NEW = [
    {"title": "v1.2 released", "desc": "Added harder theorems + stricter proof checking + timeout caps."},
    {"title": "Track separation", "desc": "Open/Closed/Academic tracks now have clearer rules + required artifacts."},
    {"title": "New metrics", "desc": "Tokens/task + $/task exposed for cost-aware ranking."},
]


def iso_date_today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


_slug_rx = re.compile(r"[^a-z0-9]+")


def slugify(s: str, *, fallback: str = "run") -> str:
    s = (s or "").strip().lower()
    s = _slug_rx.sub("-", s).strip("-")
    return s or fallback

@app.get("/health")
def health():
    return {
        "ok": True,
        "benchmarkDir": str(SETTINGS.benchmark_dir),
        "runnerCmd": SETTINGS.runner_cmd,
    }

class SubmissionIn(BaseModel):
    id: Optional[str] = Field(default=None, description="Optional stable id (slug). If omitted, generated.")
    name: str
    org: str
    track: str = "Open"
    license: str = ""
    tags: list[str] = Field(default_factory=list)
    submissionSpec: dict[str, Any] = Field(default_factory=dict)

    # metadata (optional)
    reproducible: bool = True
    openWeights: bool = False
    verified: bool = False
    releaseDate: Optional[str] = None  # ISO date
    commit: Optional[str] = None
    evidence: Optional[str] = None


class SubmissionOut(BaseModel):
    submission_id: str
    status: str


class SubmissionStatusOut(BaseModel):
    submission_id: str
    status: str
    error: Optional[str] = None
    run: Optional[dict[str, Any]] = None
    logs: Optional[str] = None


class LeaderboardOut(BaseModel):
    datasetVersion: str
    whatsNew: list[dict[str, str]]
    runs: list[dict[str, Any]]


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "datasetVersion": SETTINGS.dataset_version,
        "benchmarkDir": str(SETTINGS.benchmark_dir),
    }


@app.get("/api/leaderboard.json", response_model=LeaderboardOut)
def get_leaderboard() -> LeaderboardOut:
    runs = list_completed_runs(SETTINGS.db_path)
    return LeaderboardOut(
        datasetVersion=SETTINGS.dataset_version,
        whatsNew=DEFAULT_WHATS_NEW,
        runs=_sanitize_json(runs),
    )


# -----------------------------
# Admin auth dependency
# -----------------------------


def _check_admin_auth(request: Request) -> None:
    """FastAPI dependency that enforces the ADMIN_PASSWORD if one is configured."""
    pw = SETTINGS.admin_password
    if not pw:
        return  # no password configured — open access

    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer "):].strip()
        if token == pw:
            return

    raise HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )


_AdminAuth = Depends(_check_admin_auth)


# -----------------------------
# Admin API (protect via ADMIN_PASSWORD or Cloudflare Access)
# -----------------------------


def _admin_row_to_obj(row: SubmissionRow) -> dict[str, Any]:
    """Flatten the DB row into a single JSON object the admin UI can edit."""
    obj: dict[str, Any] = {
        "id": row.submission_id,
        "status": row.status,
        "error": row.error,
        "createdAt": row.created_at,
        "updatedAt": row.updated_at,
    }

    # Merge submission input (name/org/track/etc.).
    if isinstance(row.input_json, dict):
        for k, v in row.input_json.items():
            if k in ("id", "submission_id"):
                continue
            obj[k] = v

    # Merge completed run metrics (overall/pass1/etc.).
    if isinstance(row.run_json, dict):
        for k, v in row.run_json.items():
            if k in ("id", "submission_id"):
                continue
            obj[k] = v

    # Standardize id.
    obj["id"] = row.submission_id
    return _sanitize_json(obj)


def _sanitize_json(x: Any) -> Any:
    """Convert NaN/Inf to None so browsers can parse the JSON."""
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return None
        return x
    if isinstance(x, dict):
        return {k: _sanitize_json(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_sanitize_json(v) for v in x]
    return x


@app.get("/api/admin/submissions.json", dependencies=[_AdminAuth])
def admin_list_submissions() -> dict[str, Any]:
    """List ALL submissions (queued/running/completed/failed), newest-first."""
    rows = list_submissions(SETTINGS.db_path)
    subs = [_admin_row_to_obj(r) for r in rows]
    return {
        "datasetVersion": SETTINGS.dataset_version,
        "submissions": subs,
    }


@app.patch("/api/admin/submissions/{submission_id}", dependencies=[_AdminAuth])
def admin_patch_submission(submission_id: str, patch: dict[str, Any] = Body(...)) -> dict[str, Any]:
    row = get_submission(SETTINGS.db_path, submission_id)
    if not row:
        raise HTTPException(status_code=404, detail="submission not found")

    # Start from current.
    input_json = dict(row.input_json or {})
    run_json = dict(row.run_json or {}) if row.run_json else None
    status = row.status
    error = row.error
    logs = row.logs

    # Allow explicitly changing status/error/logs via admin.
    if "status" in patch:
        try:
            status = str(patch.get("status") or "").strip() or status
        except Exception:
            pass
    if "error" in patch:
        error = None if patch.get("error") is None else str(patch.get("error"))
    if "logs" in patch:
        logs = None if patch.get("logs") is None else str(patch.get("logs"))

    # Hidden toggle: keep in BOTH input_json + run_json (if present).
    if "hidden" in patch:
        hv = bool(patch.get("hidden"))
        input_json["hidden"] = hv
        if run_json is not None:
            run_json["hidden"] = hv

    # If the admin editor sends a full flattened object, we merge it back.
    # Some keys should never be overwritten.
    reserved = {"id", "submission_id", "createdAt", "created_at", "updatedAt", "updated_at"}

    # Fields that belong to the original submission payload.
    input_fields = {
        "name",
        "org",
        "track",
        "license",
        "tags",
        "submissionSpec",
        "reproducible",
        "openWeights",
        "verified",
        "releaseDate",
        "commit",
        "evidence",
    }

    for k, v in patch.items():
        if k in reserved:
            continue
        if k in ("status", "error", "logs"):
            continue
        if k in input_fields:
            input_json[k] = v
        # Metrics / run fields are stored on the run_json if it exists.
        if run_json is not None:
            run_json[k] = v

    if run_json is not None:
        run_json["id"] = submission_id

    try:
        update_submission(
            SETTINGS.db_path,
            submission_id,
            input_json=input_json,
            run_json=run_json,
            status=status,
            error=error,
            logs=logs,
            updated_at=iso_now(),
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="submission not found")

    # Return the updated object.
    row2 = get_submission(SETTINGS.db_path, submission_id)
    return {"ok": True, "submission": _admin_row_to_obj(row2) if row2 else None}


def _safe_read_text(p: Path, *, limit: int = 250_000) -> str:
    try:
        data = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"[error reading {p}: {e}]\n"
    if len(data) <= limit:
        return data
    return data[:limit] + "\n...\n[truncated]\n"


def _resolve_run_dir(row: SubmissionRow) -> Optional[Path]:
    """Try to find the persistent per-run directory written by score_submission.py."""
    run_dir = None
    if isinstance(row.run_json, dict):
        meta = row.run_json.get("meta") if isinstance(row.run_json.get("meta"), dict) else {}
        if meta and isinstance(meta.get("runDir"), str):
            run_dir = meta.get("runDir")
    if not run_dir:
        return None

    try:
        p = Path(str(run_dir)).expanduser().resolve()
    except Exception:
        return None

    # Safety: only allow reading inside SHADOWBENCH_LOG_DIR.
    root = Path(os.environ.get("SHADOWBENCH_LOG_DIR", "run_logs")).expanduser().resolve()
    try:
        if p == root or root in p.parents:
            return p
    except Exception:
        return None
    return None


def _compose_admin_logs(row: SubmissionRow) -> str:
    lines: list[str] = []
    lines.append(f"submission_id: {row.submission_id}")
    lines.append(f"status: {row.status}")
    lines.append(f"created_at: {row.created_at}")
    lines.append(f"updated_at: {row.updated_at}")
    if row.error:
        lines.append("")
        lines.append("--- ERROR ---")
        lines.append(str(row.error))

    run_dir = _resolve_run_dir(row)
    if run_dir:
        lines.append("")
        lines.append(f"run_dir: {run_dir}")
        try:
            files = sorted([p.name for p in run_dir.iterdir()])
            lines.append(f"files: {len(files)}")
            for name in files[:200]:
                lines.append(f"  - {name}")
            if len(files) > 200:
                lines.append("  ...")
        except Exception as e:
            lines.append(f"[error listing run_dir: {e}]")

        # Prefer run.log if present; otherwise fall back to DB-captured logs.
        run_log = run_dir / "run.log"
        if run_log.exists():
            lines.append("")
            lines.append("--- RUN.LOG ---")
            lines.append(_safe_read_text(run_log))

        result_json = run_dir / "result.json"
        if result_json.exists():
            lines.append("")
            lines.append("--- RESULT.JSON ---")
            lines.append(_safe_read_text(result_json))

    if row.logs:
        lines.append("")
        lines.append("--- BACKEND RUNNER STDOUT/STDERR ---")
        lines.append(str(row.logs))

    return "\n".join(lines).rstrip() + "\n"


@app.get("/api/admin/submissions/{submission_id}/logs", response_class=PlainTextResponse, dependencies=[_AdminAuth])
def admin_get_logs(submission_id: str) -> str:
    row = get_submission(SETTINGS.db_path, submission_id)
    if not row:
        raise HTTPException(status_code=404, detail="submission not found")
    return _compose_admin_logs(row)


@app.get("/api/admin/submissions/{submission_id}/logs.json", dependencies=[_AdminAuth])
def admin_get_logs_json(submission_id: str) -> dict[str, Any]:
    row = get_submission(SETTINGS.db_path, submission_id)
    if not row:
        raise HTTPException(status_code=404, detail="submission not found")
    return {"text": _compose_admin_logs(row)}


@app.get("/api/admin/logs.json", dependencies=[_AdminAuth])
def admin_logs(submissionId: Optional[str] = None) -> dict[str, Any]:
    """Optional: global logs feed.

    If submissionId is provided, returns that submission's logs.
    Otherwise returns a short recent activity list.
    """
    if submissionId:
        row = get_submission(SETTINGS.db_path, submissionId)
        if not row:
            raise HTTPException(status_code=404, detail="submission not found")
        return {"text": _compose_admin_logs(row)}

    rows = list_submissions(SETTINGS.db_path)[:50]
    out: list[str] = []
    for r in rows:
        out.append(f"{r.updated_at}  {r.submission_id}  {r.status}")
    return {"logs": out}


@app.delete("/api/admin/submissions/{submission_id}", dependencies=[_AdminAuth])
def admin_delete_submission(submission_id: str) -> dict[str, Any]:
    row = get_submission(SETTINGS.db_path, submission_id)
    if not row:
        raise HTTPException(status_code=404, detail="submission not found")

    # Best-effort cleanup of the run directory (only if under SHADOWBENCH_LOG_DIR).
    run_dir = _resolve_run_dir(row)
    if run_dir and run_dir.exists():
        try:
            shutil.rmtree(run_dir)
        except Exception:
            pass

    delete_submission(SETTINGS.db_path, submission_id)
    return {"ok": True}


@app.post("/api/submissions", response_model=SubmissionOut)
def submit_run(sub: SubmissionIn) -> SubmissionOut:
    base_id = slugify(sub.id or sub.name, fallback="run")
    # add a short suffix to avoid collisions for name-based ids
    if sub.id is None:
        base_id = f"{base_id}-{uuid.uuid4().hex[:6]}"

    created = iso_now()
    input_json = sub.model_dump()

    # try insert; if collision, retry with new suffix
    submission_id = base_id
    for _ in range(3):
        try:
            create_submission(SETTINGS.db_path, submission_id, "queued", input_json, created_at=created)
            break
        except Exception:
            submission_id = f"{slugify(base_id)}-{uuid.uuid4().hex[:6]}"
    else:
        raise HTTPException(status_code=500, detail="Failed to allocate submission id (db collisions)")

    # Kick off background evaluation
    EXECUTOR.submit(_evaluate_submission_job, submission_id)

    return SubmissionOut(submission_id=submission_id, status="queued")


@app.get("/api/submissions/{submission_id}", response_model=SubmissionStatusOut)
def get_submission_status(submission_id: str) -> SubmissionStatusOut:
    row = get_submission(SETTINGS.db_path, submission_id)
    if not row:
        raise HTTPException(status_code=404, detail="submission not found")

    return SubmissionStatusOut(
        submission_id=row.submission_id,
        status=row.status,
        error=row.error,
        run=row.run_json,
        logs=row.logs if row.status in ("failed", "completed") else None,
    )


def _evaluate_submission_job(submission_id: str) -> None:
    """
    Runs in a background worker thread.
    """
    row = get_submission(SETTINGS.db_path, submission_id)
    if not row:
        return

    update_submission_status(SETTINGS.db_path, submission_id, "running", updated_at=iso_now())

    try:
        spec = row.input_json.get("submissionSpec") or {}
        rr = run_benchmark(
            benchmark_dir=SETTINGS.benchmark_dir,
            runner_cmd_template=SETTINGS.runner_cmd,
            submission_spec=spec,
            timeout_sec=SETTINGS.timeout_sec,
        )

        # Build a full "run record" that matches the frontend schema.
        now = iso_date_today()
        run_record: dict[str, Any] = {
            "id": submission_id,
            "name": row.input_json.get("name"),
            "org": row.input_json.get("org"),
            "track": row.input_json.get("track"),
            "license": row.input_json.get("license") or "",
            "verified": bool(row.input_json.get("verified", False)),
            "reproducible": bool(row.input_json.get("reproducible", True)),
            "openWeights": bool(row.input_json.get("openWeights", False)),
            "isNew": True,
            "updatedAt": now,
            "releaseDate": row.input_json.get("releaseDate") or now,
            "tags": row.input_json.get("tags") or [],
            "evidence": row.input_json.get("evidence") or "—",
            "runId": f"run_{submission_id[:8]}",
            "commit": row.input_json.get("commit") or (rr.metrics.get("commit") if isinstance(rr.metrics, dict) else None) or "—",
            "envHash": rr.metrics.get("envHash", "—") if isinstance(rr.metrics, dict) else "—",
        }

        # Merge metrics: overall, pass1, etc.
        for k, v in rr.metrics.items():
            # allow any extra keys (categories, trend, etc.)
            run_record[k] = v

        # Minimal required metrics: if missing, set JSON-safe placeholders.
        # (Do NOT use NaN: browsers can't parse it as JSON.)
        for k in ("overall", "pass1", "pass5", "compileRate", "avgTimeSec", "usdPerTask", "tokensPerTask"):
            run_record.setdefault(k, None)

        set_submission_run(SETTINGS.db_path, submission_id, run_record, updated_at=iso_now(), logs=rr.logs)

    except BenchmarkRunError as e:
        update_submission_status(
            SETTINGS.db_path,
            submission_id,
            "failed",
            updated_at=iso_now(),
            error=str(e)[:8000],
            logs=str(e)[:12000],
        )
    except Exception as e:
        update_submission_status(
            SETTINGS.db_path,
            submission_id,
            "failed",
            updated_at=iso_now(),
            error=f"Unexpected error: {e}"[:8000],
        )
