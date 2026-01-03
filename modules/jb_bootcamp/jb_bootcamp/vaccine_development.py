"""Utilities for normalising vaccine development curves.

The helpers here standardise a collection of candidate development
trajectories so they can be compared on a common 0–1 scale regardless of
magnitude or offset. Each curve is rescaled independently by subtracting
its minimum and dividing by its range. Constant curves collapse to all
zeros, making it easy to spot candidates without meaningful change.
"""

from __future__ import annotations

from typing import Mapping, Sequence

__all__ = ["normalize_curve", "normalize_vaccine_development_curves"]


def normalize_curve(curve: Sequence[float]) -> tuple[float, ...]:
    """Return a single curve scaled to the ``[0, 1]`` interval.

    The function subtracts the minimum value from every point and divides
    by the range (max - min). Constant curves yield all zeros to avoid a
    division-by-zero error.
    """

    if not curve:
        raise ValueError("curve must contain at least one point.")

    values = tuple(float(point) for point in curve)
    min_value = min(values)
    max_value = max(values)
    span = max_value - min_value

    if span == 0.0:
        return tuple(0.0 for _ in values)

    return tuple((value - min_value) / span for value in values)


def normalize_vaccine_development_curves(
    curves: Mapping[str, Sequence[float]],
) -> dict[str, tuple[float, ...]]:
    """Normalise a mapping of vaccine development curves.

    Parameters
    ----------
    curves:
        Mapping from candidate name to a sequence of progress indicators.

    Returns
    -------
    dict
        Dictionary with the same keys as ``curves`` and values rescaled
        to the ``[0, 1]`` interval.
    """

    normalised: dict[str, tuple[float, ...]] = {}
    for name, curve in curves.items():
        if not name or name.strip() == "":
            raise ValueError("curve names must be non-empty strings.")
        normalised[name] = normalize_curve(curve)
    return normalised
