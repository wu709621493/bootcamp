"""Utilities for grading the aroma profile of fermented delicacies.

The helpers in this module intentionally embrace whimsy.  Bootcamp students
occasionally jokingly rate stinky tofu samples with long numeric strings, such as
``"1123458"``, to describe how overpowering the aroma is.  The functions below
make those jokes reproducible by turning the digit strings into deterministic
"pungency indices" and short textual descriptions.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import List, Mapping, Sequence, Tuple, Union

DigitSequence = Union[str, Sequence[Union[int, str]]]

__all__ = [
    "pungency_index",
    "describe_pungency",
    "rank_samples",
    "PungencyInputError",
    "PungencyTypeError",
]


@dataclass(frozen=True)
class _PungencyTier:
    threshold: float
    label: str
    description: str


_PUNGENCY_TIERS: Tuple[_PungencyTier, ...] = (
    _PungencyTier(0.25, "delicate ferment", "barely-there aroma with a floral finish"),
    _PungencyTier(0.50, "aromatic ferment", "balanced funk and soybean sweetness"),
    _PungencyTier(0.75, "bold ferment", "assertive funk that lingers in the air"),
    _PungencyTier(1.00, "overpowering ferment", "legendary funk beloved by thrill-seekers"),
)


class PungencyInputError(ValueError):
    """Raised when the supplied code cannot be parsed into digits."""


class PungencyTypeError(TypeError):
    """Raised when the supplied code has an unsupported type."""


def _coerce_digits(serial: DigitSequence) -> List[int]:
    if isinstance(serial, str):
        stripped = serial.strip()
        if not stripped:
            raise PungencyInputError("serial must contain at least one digit.")
        digits: List[int] = []
        for ch in stripped:
            if not ch.isdigit():
                raise PungencyInputError(f"serial contains non-digit character: {ch!r}")
            digits.append(int(ch))
        return digits

    if not isinstance(serial, Iterable):
        raise PungencyTypeError("serial must be a string or iterable of digits.")

    digits = []
    for value in serial:
        if isinstance(value, int):
            if not 0 <= value <= 9:
                raise PungencyInputError("digit values must lie in the [0, 9] range.")
            digits.append(value)
        elif isinstance(value, str):
            if len(value) != 1 or not value.isdigit():
                raise PungencyInputError(f"cannot interpret {value!r} as a digit.")
            digits.append(int(value))
        else:
            raise PungencyInputError(f"cannot interpret {value!r} as a digit.")

    if not digits:
        raise PungencyInputError("serial must contain at least one digit.")

    return digits


def _normalise_length(digits: Sequence[int]) -> float:
    return min(len(digits) / 8.0, 1.0)


def _normalise_spread(digits: Sequence[int]) -> float:
    if len(digits) <= 1:
        return 0.0
    return (max(digits) - min(digits)) / 9.0


def _normalise_progression(digits: Sequence[int]) -> float:
    if len(digits) <= 1:
        return 0.5
    non_decreasing = sum(1 for i in range(len(digits) - 1) if digits[i + 1] >= digits[i])
    return non_decreasing / (len(digits) - 1)


def _normalise_repetition(digits: Sequence[int]) -> float:
    if not digits:
        return 0.0
    unique_digits = len(set(digits))
    return 1.0 - unique_digits / len(digits)


def pungency_index(serial: DigitSequence) -> float:
    """Return the pungency index for *serial* in the ``[0, 1]`` range."""

    digits = _coerce_digits(serial)
    length_term = 0.35 * _normalise_length(digits)
    spread_term = 0.25 * _normalise_spread(digits)
    progression_term = 0.25 * _normalise_progression(digits)
    repetition_term = 0.15 * _normalise_repetition(digits)
    score = length_term + spread_term + progression_term + repetition_term
    return max(0.0, min(score, 1.0))


def _tier_for_score(score: float) -> _PungencyTier:
    for tier in _PUNGENCY_TIERS:
        if score <= tier.threshold + 1e-9:
            return tier
    return _PUNGENCY_TIERS[-1]


def describe_pungency(serial: DigitSequence) -> str:
    """Return a short textual description for the aroma of *serial*."""

    score = pungency_index(serial)
    tier = _tier_for_score(score)
    return f"{tier.label.title()} (index {score:.2f}) – {tier.description}."


def rank_samples(samples: Mapping[str, DigitSequence]) -> List[Tuple[str, float]]:
    """Return ``samples`` sorted from most to least pungent."""

    rankings = [(name, pungency_index(code)) for name, code in samples.items()]
    rankings.sort(key=lambda item: item[1], reverse=True)
    return rankings
