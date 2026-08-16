"""Repo-root pytest config: make src/ importable as top-level packages.

Without this, `from sa_pass.scorer import score_one` fails because pytest's
default rootdir discovery does not add ``src`` to ``sys.path``. Putting a
conftest at the repo root runs before any test module is imported, so we
can adjust ``sys.path`` once and let everything below resolve normally.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC_ROOT  = REPO_ROOT / "src"

for p in (SRC_ROOT, REPO_ROOT):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)
