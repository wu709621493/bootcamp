"""Utilities for classifying natural numbers by divisor sums."""
from __future__ import annotations

from typing import List

__all__ = [
    "proper_divisors",
    "aliquot_sum",
    "is_perfect_number",
    "classify_number",
    "is_abundant_number",
    "abundant_numbers",
]


def _validate_positive_int(value: int, name: str) -> int:
    """Ensure ``value`` is a positive integer and return it.

    Booleans are rejected even though they are instances of ``int``.
    """

    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
    return value


def proper_divisors(value: int) -> List[int]:
    """Return the proper divisors of ``value`` in ascending order.

    Proper divisors are positive integers less than ``value`` that divide the
    number evenly. ``1`` is always included for valid inputs greater than one.
    """

    validated = _validate_positive_int(value, "value")
    if validated == 1:
        return []

    divisors: List[int] = [1]
    for candidate in range(2, validated):
        if validated % candidate == 0:
            divisors.append(candidate)
    return divisors


def aliquot_sum(value: int) -> int:
    """Return the sum of the proper divisors of ``value``.

    This helper wraps :func:`proper_divisors` and provides consistent input
    validation for consumers that only need the divisor sum.
    """

    validated = _validate_positive_int(value, "value")
    return sum(proper_divisors(validated))


def is_perfect_number(value: int) -> bool:
    """Return ``True`` if ``value`` is a perfect number.

    A perfect number equals the sum of its proper divisors. Only positive
    integers can be perfect numbers; invalid inputs raise appropriate errors.
    """

    validated = _validate_positive_int(value, "value")
    return sum(proper_divisors(validated)) == validated


def classify_number(value: int) -> str:
    """Classify ``value`` as ``"perfect"``, ``"abundant"``, or ``"deficient"``.

    The classification compares the sum of proper divisors against the number
    itself. It raises if the input is not a positive integer.
    """

    validated = _validate_positive_int(value, "value")
    divisor_sum = sum(proper_divisors(validated))
    if divisor_sum == validated:
        return "perfect"
    if divisor_sum > validated:
        return "abundant"
    return "deficient"


def is_abundant_number(value: int) -> bool:
    """Return ``True`` if ``value`` is an abundant number."""

    validated = _validate_positive_int(value, "value")
    return sum(proper_divisors(validated)) > validated


def abundant_numbers(limit: int) -> List[int]:
    """Return abundant numbers up to and including ``limit``.

    The search begins at ``12``, the smallest abundant number, and returns
    results in ascending order. Inputs are validated as positive integers.
    """

    validated = _validate_positive_int(limit, "limit")
    if validated < 12:
        return []

    return [candidate for candidate in range(12, validated + 1) if classify_number(candidate) == "abundant"]
