"""Simple utilities for estimating drink-related happiness balance."""

from __future__ import annotations


def _validate_unit_interval(value: float, name: str) -> float:
    """Validate that ``value`` is between ``0`` and ``1`` inclusive."""

    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be numeric; got {value!r}.") from exc

    if not 0.0 <= numeric <= 1.0:
        raise ValueError(f"{name} must be on the [0, 1] scale; got {value!r}.")
    return numeric


def happiness_formula_drinks(
    hydration: float,
    flavor: float,
    social_context: float,
    *,
    caffeine: float = 0.35,
    sugar: float = 0.30,
    alcohol: float = 0.0,
) -> float:
    """Return a drink happiness score on a ``[0, 100]`` scale.

    The formula prioritizes hydration and flavor while applying moderate
    penalties for high sugar and alcohol levels.
    """

    hydration = _validate_unit_interval(hydration, "hydration")
    flavor = _validate_unit_interval(flavor, "flavor")
    social_context = _validate_unit_interval(social_context, "social_context")
    caffeine = _validate_unit_interval(caffeine, "caffeine")
    sugar = _validate_unit_interval(sugar, "sugar")
    alcohol = _validate_unit_interval(alcohol, "alcohol")

    core = 0.45 * hydration + 0.30 * flavor + 0.25 * social_context
    boost = 0.08 * caffeine * (1.0 - alcohol)
    penalty = 0.10 * sugar + 0.18 * alcohol

    score = 100.0 * (core + boost - penalty)
    return max(0.0, min(score, 100.0))
