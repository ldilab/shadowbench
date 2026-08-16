"""
Statement tracking utilities for detecting changes in theorem/lemma statements.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, Optional

from .extract_sublemmas import LeanCodeParser


@dataclass
class StatementSnapshot:
    """Snapshot of a single statement."""
    file_path: Path
    name: str
    statement: str  # Statement without proof


@dataclass
class StatementChange:
    """Record of a statement change."""
    file_path: Path
    name: str
    original: str
    current: str
    change_type: Literal["modified", "added", "removed"]

    def __str__(self) -> str:
        return f"[{self.change_type}] {self.file_path}:{self.name}"


def extract_statements_from_file(file_path: Path) -> Dict[str, str]:
    """
    Extract all theorem/lemma statements from a Lean file.
    Returns a dict mapping theorem/lemma names to their statements (without proofs).
    """
    try:
        if not file_path.exists():
            return {}
        code = file_path.read_text(encoding="utf-8")
        parser = LeanCodeParser(code)
        blocks = parser.extract_all_blocks(keys=["theorem", "lemma"], allow_overlap=False)

        statements = {}
        for block in blocks:
            name = block["info"]["name"]
            statement = block["info"]["statement"]
            if name:
                statements[name] = statement

        return statements
    except Exception as e:
        print(f"[warn] Failed to extract statements from {file_path}: {e}")
        return {}


def normalize_statement(statement: str) -> str:
    """Normalize whitespace for comparison."""
    return " ".join(statement.split())


class StatementTracker:
    """
    Track statement changes across Claude runs.

    Usage:
        tracker = StatementTracker(files=[Path("file.lean")])
        # ... run claude ...
        changes = tracker.check()
        if changes:
            for c in changes:
                print(f"  {c}")
    """

    def __init__(self, files: List[Path]):
        """
        Initialize tracker with files to monitor.

        Args:
            files: List of .lean files to track
        """
        self.files = [Path(f).resolve() for f in files]
        self.initial_snapshots: Dict[Path, Dict[str, str]] = {}
        self._capture_initial()

    def _capture_initial(self) -> None:
        """Capture initial state of all statements."""
        for f in self.files:
            self.initial_snapshots[f] = extract_statements_from_file(f)

    def check(self) -> List[StatementChange]:
        """
        Check current state against initial state.

        Returns:
            List of statement changes (compared to initial state)
        """
        changes = []

        for f in self.files:
            initial = self.initial_snapshots.get(f, {})
            current = extract_statements_from_file(f)

            all_names = set(initial.keys()) | set(current.keys())

            for name in all_names:
                orig = initial.get(name, "")
                curr = current.get(name, "")

                orig_norm = normalize_statement(orig)
                curr_norm = normalize_statement(curr)

                if orig_norm != curr_norm:
                    if not orig:
                        change_type = "added"
                    elif not curr:
                        change_type = "removed"
                    else:
                        change_type = "modified"

                    changes.append(StatementChange(
                        file_path=f,
                        name=name,
                        original=orig,
                        current=curr,
                        change_type=change_type,
                    ))

        return changes

    def get_initial_statements(self) -> Dict[Path, Dict[str, str]]:
        """Get the initial snapshots."""
        return self.initial_snapshots.copy()


@dataclass
class RoundResult:
    """Result of a single run_claude_once call."""
    round_number: int
    stdout: str
    end_reason: Optional[str]  # COMPLETE / LIMIT / None
    returncode: int
    statement_changes: List[StatementChange] = field(default_factory=list)
    duration_seconds: float = 0.0  # Duration of this round
    line_counts: dict = field(default_factory=dict)  # {filename: line_count}

    def has_statement_changes(self) -> bool:
        """Check if any statements were changed in this round."""
        return len(self.statement_changes) > 0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "round_number": self.round_number,
            "stdout": self.stdout,
            "end_reason": self.end_reason,
            "returncode": self.returncode,
            "duration_seconds": self.duration_seconds,
            "statement_changes": [
                {
                    "file_path": str(c.file_path),
                    "name": c.name,
                    "original": c.original,
                    "current": c.current,
                    "change_type": c.change_type,
                }
                for c in self.statement_changes
            ],
            "line_counts": self.line_counts,
        }
