"""Keyword-based disambiguation between fraud and Freud-related text."""

from __future__ import annotations

import re

__all__ = ["fraud_freud_test"]

_FRAUD_KEYWORDS = {
    "fraud",
    "scam",
    "embezzle",
    "embezzlement",
    "phishing",
    "money",
    "laundering",
    "forgery",
    "counterfeit",
}

_FREUD_KEYWORDS = {
    "freud",
    "psychoanalysis",
    "id",
    "ego",
    "superego",
    "unconscious",
    "dream",
    "libido",
}

_TOKEN_RE = re.compile(r"[a-zA-Z']+")


def fraud_freud_test(text: str) -> str:
    """Classify text as about fraud, Freud, both, or neither.

    Returns one of: ``"fraud"``, ``"freud"``, ``"both"``, or ``"neither"``.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    tokens = {token.lower() for token in _TOKEN_RE.findall(text)}
    if not tokens:
        return "neither"

    has_fraud = bool(tokens & _FRAUD_KEYWORDS)
    has_freud = bool(tokens & _FREUD_KEYWORDS)

    if has_fraud and has_freud:
        return "both"
    if has_fraud:
        return "fraud"
    if has_freud:
        return "freud"
    return "neither"
