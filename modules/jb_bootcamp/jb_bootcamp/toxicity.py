"""Simple lexical toxicity scoring utilities.

The scorer implemented here is intentionally lightweight and deterministic so it
can run in offline teaching environments.  It is *not* a replacement for modern
moderation models, but it provides a quick signal for obviously abusive terms.
"""

from __future__ import annotations

import re

__all__ = ["measure_toxicity"]

# Core toxic terms weighted by severity on a 0..1 scale.
_TOXIC_TERM_WEIGHTS: dict[str, float] = {
    "idiot": 0.35,
    "stupid": 0.25,
    "moron": 0.35,
    "hate": 0.25,
    "kill": 0.5,
    "trash": 0.2,
    "damn": 0.1,
}

_TOKEN_RE = re.compile(r"[a-zA-Z']+")


def measure_toxicity(text: str) -> float:
    """Return a lexical toxicity score between 0.0 and 1.0.

    Parameters
    ----------
    text:
        Input string to score.

    Returns
    -------
    float
        Toxicity score in ``[0.0, 1.0]``.  The score is the mean per-token toxic
        weight and is clipped to ``1.0``.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    tokens = [token.lower() for token in _TOKEN_RE.findall(text)]
    if not tokens:
        return 0.0

    weighted_sum = sum(_TOXIC_TERM_WEIGHTS.get(token, 0.0) for token in tokens)
    return min(1.0, weighted_sum / len(tokens))
