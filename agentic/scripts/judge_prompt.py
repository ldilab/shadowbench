"""Prompt builder + response parser for the LLM-as-judge evaluator.

The response parser is robust (handles bare JSON, fenced JSON, and lenient
fallbacks) — you should not usually need to touch it.

The PROMPT WORDING, however, shapes verdict quality more than anything else
in the pipeline. The `SYSTEM_PROMPT` and the user-message template below are
intentionally left minimal so you can refine them. See the TODO block.
"""

from __future__ import annotations

import json
import re
from typing import Literal

Verdict = Literal["correct", "incorrect", "uncertain"]

# ---------------------------------------------------------------------------
# TODO(user): tune the wording below. This is the 5–10 line part that matters.
#
# Why this prompt matters: the judge sees (informal problem, reference formal
# statement with `sorry`, candidate statement+proof). It must catch proofs
# that compile but are "cheese" — e.g. the candidate restated a weaker claim,
# dropped a hypothesis, replaced equality with a tautology, used circular
# tactics, or relied on a malformed local definition. A generic "is this
# proof correct" prompt underweights those failure modes.
#
# Guidance from the plan:
#  - Output MUST be a single JSON object: {"verdict": ..., "reason": ...}
#  - verdict ∈ {"correct", "incorrect", "uncertain"}
#  - "correct" requires BOTH: (a) candidate's stated theorem is
#    mathematically equivalent to the intended claim, AND
#    (b) the proof actually justifies that claim.
#  - "incorrect" if the statement is weaker/stronger/wrong OR the proof
#    is unsound, circular, or relies on a malformed auxiliary.
#  - "uncertain" only if the artifact is truncated or unreadable.
#
# Consider spelling out specific Lean/Mathlib failure modes you've seen in
# prior runs — models trained on general text benefit from concrete hints.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an expert in Lean 4 and Mathlib. Decide whether a candidate Lean 4 \
statement+proof semantically establishes the INTENDED mathematical theorem \
shown alongside it.

Return ONE JSON object and nothing else:
  {"verdict": "correct" | "incorrect" | "uncertain", "reason": "<1-3 sentences>"}

"correct" = (a) the candidate's stated theorem is mathematically equivalent \
to the intended claim, AND (b) its proof actually justifies that claim.
"incorrect" = statement weaker/stronger/wrong OR proof unsound, circular, \
or relies on a broken auxiliary.
"uncertain" = artifact truncated or unreadable.
"""

USER_TEMPLATE = """\
# Intended problem (informal)
{informal_block}

# Intended formal statement (reference Lean 4; proof body is `sorry`)
```lean
{formal_ref}
```

# Candidate (Lean 4; statement + attempted proof)
```lean
{candidate}
```

Return your JSON verdict now.
"""


def build_prompt(
    informal_text: str | None,
    has_nl_proof: bool,
    formal_ref: str,
    candidate: str,
) -> tuple[str, str]:
    """Return (system_message, user_message)."""
    if informal_text:
        label = "informal statement + proof" if has_nl_proof else "informal statement only"
        informal_block = f"(LaTeX, {label})\n{informal_text.strip()}"
    else:
        informal_block = "(no informal text available)"
    user = USER_TEMPLATE.format(
        informal_block=informal_block,
        formal_ref=formal_ref.strip(),
        candidate=candidate.strip(),
    )
    return SYSTEM_PROMPT, user


# --- response parsing ------------------------------------------------------

_JSON_OBJECT_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def _extract_json(text: str) -> dict | None:
    text = text.strip()
    # strip ```json ... ``` or ``` ... ``` fences
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        pass
    # fall back to first balanced {...} (no nesting)
    m = _JSON_OBJECT_RE.search(text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return None
    return None


def _normalise_verdict(raw) -> Verdict:
    if not isinstance(raw, str):
        return "uncertain"
    r = raw.strip().lower()
    if r in ("correct", "yes", "true", "right", "sound"):
        return "correct"
    if r in ("incorrect", "wrong", "no", "false", "unsound"):
        return "incorrect"
    return "uncertain"


def parse_response(text: str) -> dict:
    """Return {verdict, reason, raw}. Never raises — falls back to uncertain."""
    obj = _extract_json(text) or {}
    verdict = _normalise_verdict(obj.get("verdict"))
    reason = obj.get("reason")
    if not isinstance(reason, str):
        reason = ""
    reason = reason.strip()[:500]
    return {"verdict": verdict, "reason": reason, "raw": text[:2000]}
