#!/usr/bin/env python3
"""
PreToolUse hook: intercept Grep/Bash/Read/Glob calls targeting mathlib.

When the agent tries to search mathlib via file system tools,
this hook blocks the call and returns a message redirecting it
to use lean_leandex, lean_loogle, or lean_hover_info instead.

Protocol:
  - Reads tool call JSON from stdin (tool_name, tool_input)
  - Outputs JSON to stdout with decision
  - Always exits 0
"""

import json
import os
import sys

MATHLIB_INDICATORS = (
    ".lake/packages",
    "/mathlib/",
    "Mathlib/",
    "packages/batteries",
    "packages/aesop",
    "packages/proofwidgets",
)

BASH_SEARCH_COMMANDS = ("grep", "find", "rg", "ag", "xargs")

# Environment variable to disable this hook (for ablation experiments)
DISABLED = os.environ.get("DISABLE_MATHLIB_GUARD", "").lower() in ("1", "true", "yes")


def is_mathlib_path(path: str) -> bool:
    return any(ind in path for ind in MATHLIB_INDICATORS)


def check_tool_call(tool_name: str, tool_input: dict) -> str | None:
    """Return a warning message if this tool call targets mathlib, else None."""

    if tool_name == "Grep":
        path = tool_input.get("path", "")
        pattern = tool_input.get("pattern", "")
        if is_mathlib_path(path):
            return (
                f"Do not use Grep to search mathlib. "
                f"You tried to grep for '{pattern}' in '{path}'.\n\n"
                f"Use these MCP tools instead:\n"
                f"  - lean_leandex(\"{pattern}\") — natural language theorem search\n"
                f"  - lean_loogle(\"{pattern}\") — search by type pattern or name\n"
                f"  - lean_leanfinder(\"{pattern}\") — semantic theorem search\n"
                f"  - lean_hover_info — check type signatures of specific terms\n\n"
                f"These tools search mathlib's full index and are far more effective than grep."
            )

    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if is_mathlib_path(cmd) and any(c in cmd for c in BASH_SEARCH_COMMANDS):
            return (
                f"Do not use Bash to search mathlib. "
                f"Command: {cmd[:150]}\n\n"
                f"Use these MCP tools instead:\n"
                f"  - lean_leandex(\"your query\") — natural language theorem search\n"
                f"  - lean_loogle(\"type pattern\") — search by type or name\n"
                f"  - lean_leanfinder(\"query\") — semantic theorem search\n"
                f"  - lean_local_search(\"name\") — search declarations by name\n\n"
                f"These tools search mathlib's full index and are far more effective."
            )

    if tool_name == "Read":
        path = tool_input.get("file_path", "")
        if is_mathlib_path(path) and any(d in path for d in ("/Mathlib/", "/batteries/")):
            return (
                f"Do not read mathlib source files directly. "
                f"File: {path}\n\n"
                f"Use these MCP tools instead:\n"
                f"  - lean_hover_info — get type info and docstrings for any term\n"
                f"  - lean_leandex(\"description\") — find related theorems\n"
                f"  - lean_loogle(\"type pattern\") — search by type signature\n"
                f"  - lean_declaration_file — find where a declaration is defined"
            )

    if tool_name == "Glob":
        pattern = tool_input.get("pattern", "")
        if is_mathlib_path(pattern):
            return (
                f"Do not use Glob to search mathlib. "
                f"Pattern: {pattern}\n\n"
                f"Use these MCP tools instead:\n"
                f"  - lean_leandex(\"your query\") — natural language theorem search\n"
                f"  - lean_loogle(\"type pattern\") — search by type or name\n"
                f"  - lean_local_search(\"name\") — search declarations by name"
            )

    return None


def main():
    if DISABLED:
        print(json.dumps({}), file=sys.stdout)
        sys.exit(0)

    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}), file=sys.stdout)
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    warning = check_tool_call(tool_name, tool_input)

    if warning:
        # Block the tool call and redirect to MCP tools
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
            },
            "systemMessage": warning,
        }
        print(json.dumps(result), file=sys.stdout)
    else:
        print(json.dumps({}), file=sys.stdout)

    sys.exit(0)


if __name__ == "__main__":
    main()
