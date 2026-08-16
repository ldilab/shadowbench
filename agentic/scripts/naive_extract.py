"""
Utilities for naive Claude Code experiments.

Extracts natural language descriptions from Lean files and
strips markdown fencing from Claude's output.
"""

import re
import sys
from pathlib import Path


def extract_nl(lean_file: str | Path) -> str | None:
    """
    Extract natural language descriptions from /- ... -/ and /-- ... -/ block comments.

    Args:
        lean_file: Path to a .lean file

    Returns:
        Concatenated NL text, or None if no block comments found
    """
    content = Path(lean_file).read_text(encoding="utf-8")

    # Match both /- ... -/ (block comments) and /-- ... -/ (doc comments)
    # Lean block comments: /- ... -/ where the content is between /- and -/
    # Doc comments: /-- ... -/ (a special case of block comments)
    pattern = r"/--?\s*(.*?)\s*-/"
    matches = re.findall(pattern, content, re.DOTALL)

    if not matches:
        return None

    # Filter out very short matches (likely just code comments like /- by claude -/)
    nl_blocks = [m.strip() for m in matches if len(m.strip()) > 20]

    if not nl_blocks:
        return None

    return "\n\n".join(nl_blocks)


def extract_lean_code(raw_output: str) -> str:
    """
    Extract Lean code from Claude's output, stripping markdown fencing if present.

    Handles:
    - ```lean ... ``` blocks
    - ```lean4 ... ``` blocks
    - ``` ... ``` blocks (no language tag)
    - Raw output (no fencing)

    Args:
        raw_output: Raw text output from Claude

    Returns:
        Extracted Lean code
    """
    # Try to find fenced code blocks (```lean ... ``` or ```lean4 ... ``` or ``` ... ```)
    pattern = r"```(?:lean4?|)\s*\n(.*?)```"
    matches = re.findall(pattern, raw_output, re.DOTALL)

    if matches:
        # If multiple code blocks, concatenate them (unusual but handle it)
        return "\n\n".join(m.strip() for m in matches)

    # No fencing found - use the raw output, but strip common conversational prefixes/suffixes
    text = raw_output.strip()

    # Remove common Claude prefixes like "Here's the Lean 4 code:" etc.
    lines = text.split("\n")
    # Skip leading non-code lines (heuristic: Lean code starts with import, open, set_option, theorem, etc.)
    lean_starts = (
        "import ", "open ", "set_option ", "theorem ", "lemma ", "def ",
        "example ", "instance ", "class ", "structure ", "namespace ",
        "section ", "variable ", "noncomputable ", "#check ", "--",
        "/-", "universe ", "axiom ", "abbrev ", "inductive ", "private ",
        "protected ", "mutual ",
    )
    start_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and any(stripped.startswith(s) for s in lean_starts):
            start_idx = i
            break

    return "\n".join(lines[start_idx:]).strip()


def main():
    """CLI interface for bash integration."""
    if len(sys.argv) < 2:
        print("Usage:", file=sys.stderr)
        print("  python -m scripts.naive_extract extract-nl <file.lean>", file=sys.stderr)
        print("  python -m scripts.naive_extract strip-markdown < raw_output.txt", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "extract-nl":
        if len(sys.argv) < 3:
            print("Error: missing file path", file=sys.stderr)
            sys.exit(1)
        result = extract_nl(sys.argv[2])
        if result is None:
            sys.exit(1)  # No NL found - exit with error code
        print(result)

    elif command == "strip-markdown":
        raw = sys.stdin.read()
        print(extract_lean_code(raw))

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
