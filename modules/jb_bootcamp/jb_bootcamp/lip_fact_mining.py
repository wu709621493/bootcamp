"""Utilities for extracting lip-related factual snippets from text."""

from __future__ import annotations

import re
from typing import List

__all__ = ["lip_fact_mining"]

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_LIP_TOKEN_RE = re.compile(r"\blip[a-z]*\b", re.IGNORECASE)


def lip_fact_mining(text: str) -> List[str]:
    """Return sentence-like fragments that mention lips.

    Parameters
    ----------
    text:
        Input prose to inspect.

    Returns
    -------
    list of str
        Ordered unique fragments containing a ``lip`` word, preserving original
        sentence casing and punctuation where possible.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    stripped = text.strip()
    if not stripped:
        return []

    fragments = _SENTENCE_SPLIT_RE.split(stripped)

    seen = set()
    facts: List[str] = []
    for fragment in fragments:
        sentence = fragment.strip()
        if not sentence:
            continue
        if _LIP_TOKEN_RE.search(sentence) is None:
            continue
        if sentence in seen:
            continue
        seen.add(sentence)
        facts.append(sentence)

    return facts
