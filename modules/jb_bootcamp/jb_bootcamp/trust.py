"""Helpers for granting visitorships based on trust scores.

The :func:`grant_visitorships` function normalises a variety of input formats
into a clean list of people who should be granted visitorship.  Inputs can be a
mapping of names to trust scores, a sequence of ``(name, score)`` pairs, or a
simple iterable of names (treated as fully trusted).  Scores are clamped to the
``[0.0, 1.0]`` interval and entries that fall below a configurable threshold are
filtered out.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Union

__all__ = ["grant_visitorships"]


def _coerce_person(entry: object) -> tuple[str, float]:
    """Return a ``(name, score)`` tuple from *entry*.

    ``entry`` may be a string name (assumed to have a perfect score), a mapping
    with a single name/score pair, or a two-element sequence.  Whitespace is
    stripped from names and scores are converted to floats.  The function raises
    ``TypeError`` or ``ValueError`` for unsupported structures or invalid data.
    """

    if isinstance(entry, str):
        name = entry.strip()
        if not name:
            raise ValueError("Visitor names must be non-empty strings.")
        return name, 1.0

    if isinstance(entry, Mapping):
        if len(entry) != 1:
            raise ValueError("Visitor mappings must contain exactly one name/score pair.")
        (name, score), *_ = entry.items()
        return _coerce_person((name, score))

    if isinstance(entry, Sequence) and not isinstance(entry, (bytes, bytearray)):
        if len(entry) != 2:
            raise ValueError("Visitor entries must be two-item sequences of (name, score).")
        name_raw, score_raw = entry
        if not isinstance(name_raw, str):
            raise TypeError("Visitor names must be strings.")
        name = name_raw.strip()
        if not name:
            raise ValueError("Visitor names must be non-empty strings.")
        if isinstance(score_raw, bool) or not isinstance(score_raw, (int, float)):
            raise TypeError("Trust scores must be numeric.")
        score = float(score_raw)
        if score < 0.0 or score > 1.0:
            raise ValueError("Trust scores must lie between 0.0 and 1.0.")
        return name, score

    raise TypeError("Visitor entries must be strings, mappings, or (name, score) pairs.")


def grant_visitorships(
    entries: Union[Mapping[str, float], Iterable[object]], *, minimum_score: float = 0.5
) -> list[str]:
    """Return trusted visitor names meeting ``minimum_score``.

    Parameters
    ----------
    entries:
        People and their trust scores.  Accepts a mapping of names to scores or
        an iterable containing strings (implying a score of ``1.0``), mappings
        with a single name/score pair, or two-item sequences ``(name, score)``.
    minimum_score:
        Inclusive threshold a visitor must meet to be granted access.  Values
        outside the ``[0.0, 1.0]`` interval raise ``ValueError``.

    Returns
    -------
    list[str]
        Ordered list of unique visitor names whose trust score meets or
        exceeds ``minimum_score``.
    """

    if minimum_score < 0.0 or minimum_score > 1.0:
        raise ValueError("minimum_score must be between 0.0 and 1.0.")

    if isinstance(entries, Mapping):
        iterable: Iterable[object] = entries.items()
    elif isinstance(entries, Iterable) and not isinstance(entries, (str, bytes, bytearray)):
        iterable = entries
    else:
        raise TypeError("entries must be a mapping or iterable of visitor information.")

    granted: list[str] = []
    seen: set[str] = set()

    for entry in iterable:
        name, score = _coerce_person(entry)
        normalised_name = name.lower()
        if score >= minimum_score and normalised_name not in seen:
            granted.append(name)
            seen.add(normalised_name)

    return granted
