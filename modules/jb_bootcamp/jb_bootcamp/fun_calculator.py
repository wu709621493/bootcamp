"""Utilities for estimating a lighthearted fun score for group activities."""

from __future__ import annotations

import math
from typing import Iterable


def _validate_fraction(value: float, name: str) -> float:
    """Return *value* if in the unit interval, otherwise raise ``ValueError``."""

    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be on the [0, 1] scale; got {value!r}.")
    return float(value)


def cal_fun(
    attendees: int,
    excitement_levels: Iterable[float],
    collaboration: float,
    chaos: float = 0.1,
    novelty: float = 0.2,
) -> float:
    """Return a fun score on a ``[0, 10]`` scale for a group activity.

    Parameters
    ----------
    attendees
        Number of people participating.  Must be positive.
    excitement_levels
        Iterable of individual excitement measurements on a ``[0, 1]`` scale.
        The geometric mean captures whether the group can sustain energy together.
    collaboration
        Perceived collaboration quality on a ``[0, 1]`` scale where ``1`` means
        everyone is eager to help one another.
    chaos
        Degree of unpredictable chaos on a ``[0, 1]`` scale.  Higher values
        reduce the fun score by applying a penalty.
    novelty
        Freshness of the activity on a ``[0, 1]`` scale.  Higher values increase
        the fun score.

    Notes
    -----
    The model gently rewards medium-sized groups, prioritises collective
    excitement, and damps the score when chaos overwhelms collaboration.

    Returns
    -------
    float
        Overall fun score clipped to the range ``[0, 10]``.
    """

    if attendees <= 0:
        raise ValueError("attendees must be positive.")

    excitement_values = list(excitement_levels)
    if not excitement_values:
        raise ValueError("At least one excitement level must be provided.")

    collaboration = _validate_fraction(collaboration, "collaboration")
    chaos = _validate_fraction(chaos, "chaos")
    novelty = _validate_fraction(novelty, "novelty")

    for idx, value in enumerate(excitement_values):
        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:  # Handles non-numeric iterables.
            raise TypeError("Excitement levels must be numeric.") from exc

        excitement_values[idx] = _validate_fraction(numeric_value, "excitement")

    group_factor = min(math.log1p(attendees) / math.log(30), 1.0)

    # Geometric mean highlights whether the group can maintain collective energy.
    log_product = sum(math.log(value or 1e-9) for value in excitement_values)
    excitement_mean = math.exp(log_product / len(excitement_values))

    synergy = 0.55 * excitement_mean + 0.35 * collaboration + 0.25 * novelty
    penalty = 0.5 * chaos * (1.0 + 0.2 * attendees)

    score = 10.0 * (0.55 * group_factor + 0.45 * synergy) - penalty
    return max(0.0, min(score, 10.0))
