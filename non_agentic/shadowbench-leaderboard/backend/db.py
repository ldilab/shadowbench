from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class SubmissionRow:
    submission_id: str
    status: str
    error: Optional[str]
    input_json: dict[str, Any]
    run_json: Optional[dict[str, Any]]
    logs: Optional[str]
    created_at: str
    updated_at: str


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), timeout=30, isolation_level=None)  # autocommit
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
              submission_id TEXT PRIMARY KEY,
              status TEXT NOT NULL,
              error TEXT,
              input_json TEXT NOT NULL,
              run_json TEXT,
              logs TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status)")
    finally:
        conn.close()


def create_submission(
    db_path: Path,
    submission_id: str,
    status: str,
    input_json: dict[str, Any],
    created_at: str,
) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO submissions(submission_id, status, error, input_json, run_json, logs, created_at, updated_at)
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (submission_id, status, None, json.dumps(input_json), None, None, created_at, created_at),
        )
    finally:
        conn.close()


def update_submission_status(
    db_path: Path,
    submission_id: str,
    status: str,
    updated_at: str,
    *,
    error: Optional[str] = None,
    logs: Optional[str] = None,
) -> None:
    conn = _connect(db_path)
    try:
        if logs is None:
            conn.execute(
                "UPDATE submissions SET status=?, error=?, updated_at=? WHERE submission_id=?",
                (status, error, updated_at, submission_id),
            )
        else:
            conn.execute(
                "UPDATE submissions SET status=?, error=?, logs=?, updated_at=? WHERE submission_id=?",
                (status, error, logs, updated_at, submission_id),
            )
    finally:
        conn.close()


def set_submission_run(
    db_path: Path,
    submission_id: str,
    run_json: dict[str, Any],
    updated_at: str,
    *,
    logs: Optional[str] = None,
) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(
            "UPDATE submissions SET run_json=?, status=?, updated_at=?, logs=? WHERE submission_id=?",
            (json.dumps(run_json), "completed", updated_at, logs, submission_id),
        )
    finally:
        conn.close()


def _row_to_submission(row: sqlite3.Row) -> SubmissionRow:
    return SubmissionRow(
        submission_id=row["submission_id"],
        status=row["status"],
        error=row["error"],
        input_json=json.loads(row["input_json"]),
        run_json=json.loads(row["run_json"]) if row["run_json"] else None,
        logs=row["logs"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def get_submission(db_path: Path, submission_id: str) -> Optional[SubmissionRow]:
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT * FROM submissions WHERE submission_id=?",
            (submission_id,),
        )
        row = cur.fetchone()
        return _row_to_submission(row) if row else None
    finally:
        conn.close()


def list_completed_runs(db_path: Path) -> list[dict[str, Any]]:
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT run_json FROM submissions WHERE status='completed' AND run_json IS NOT NULL"
        )
        runs: list[dict[str, Any]] = []
        for r in cur.fetchall():
            try:
                run = json.loads(r["run_json"])
                # Allow admins to hide runs from the public leaderboard.
                # We keep the data in the DB, but filter it out here.
                if isinstance(run, dict):
                    hidden = bool(
                        run.get("hidden") is True
                        or run.get("isHidden") is True
                        or run.get("published") is False
                        or run.get("isPublic") is False
                    )
                    if hidden:
                        continue
                runs.append(run)
            except Exception:
                continue
        return runs
    finally:
        conn.close()


def list_submissions(db_path: Path) -> list[SubmissionRow]:
    """Admin helper: return ALL submissions (queued/running/completed/failed)."""
    conn = _connect(db_path)
    try:
        cur = conn.execute("SELECT * FROM submissions ORDER BY created_at DESC")
        out: list[SubmissionRow] = []
        for row in cur.fetchall():
            try:
                out.append(_row_to_submission(row))
            except Exception:
                continue
        return out
    finally:
        conn.close()


def delete_submission(db_path: Path, submission_id: str) -> None:
    """Admin helper: delete a submission row."""
    conn = _connect(db_path)
    try:
        conn.execute("DELETE FROM submissions WHERE submission_id=?", (submission_id,))
    finally:
        conn.close()


def update_submission(
    db_path: Path,
    submission_id: str,
    *,
    input_json: Optional[dict[str, Any]] = None,
    run_json: Optional[dict[str, Any]] = None,
    status: Optional[str] = None,
    error: Optional[str] = None,
    logs: Optional[str] = None,
    updated_at: str,
) -> None:
    """Admin helper: update one or more fields on a submission row."""
    conn = _connect(db_path)
    try:
        cur = conn.execute("SELECT * FROM submissions WHERE submission_id=?", (submission_id,))
        row = cur.fetchone()
        if not row:
            raise KeyError(f"submission not found: {submission_id}")

        cur_input = json.loads(row["input_json"]) if row["input_json"] else {}
        cur_run = json.loads(row["run_json"]) if row["run_json"] else None
        cur_status = row["status"]
        cur_error = row["error"]
        cur_logs = row["logs"]

        new_input = input_json if input_json is not None else cur_input
        new_run = run_json if run_json is not None else cur_run
        new_status = status if status is not None else cur_status
        new_error = error if error is not None else cur_error
        new_logs = logs if logs is not None else cur_logs

        conn.execute(
            "UPDATE submissions SET input_json=?, run_json=?, status=?, error=?, logs=?, updated_at=? WHERE submission_id=?",
            (
                json.dumps(new_input),
                json.dumps(new_run) if new_run is not None else None,
                new_status,
                new_error,
                new_logs,
                updated_at,
                submission_id,
            ),
        )
    finally:
        conn.close()
