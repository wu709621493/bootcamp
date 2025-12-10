"""Utilities for working with prime number series.

This module includes helper functions to generate prime numbers and
identify twin prime pairs (pairs of primes that differ by two).
"""
from __future__ import annotations

from math import isqrt
from typing import List, Tuple

__all__ = [
    "is_prime",
    "prime_series",
    "twin_prime_pairs",
    "is_armstrong_number",
    "armstrong_numbers",
    "prime_factorization",
    "nth_prime",
]


def is_prime(value: int) -> bool:
    """Return ``True`` when *value* is a prime number.

    The implementation uses trial division up to the square root of the
    value. Negative integers and zero are not considered prime.
    """
    if value <= 1:
        return False
    if value <= 3:
        return True
    if value % 2 == 0 or value % 3 == 0:
        return False

    limit = isqrt(value)
    step = 2
    candidate = 5
    while candidate <= limit:
        if value % candidate == 0:
            return False
        candidate += step
        step = 6 - step  # alternate between checking numbers +/- 1 from multiples of 6
    return True


def prime_series(limit: int) -> List[int]:
    """Generate the sequence of prime numbers less than or equal to *limit*.

    Parameters
    ----------
    limit:
        The inclusive upper bound for the generated primes.
    """
    if limit < 2:
        return []

    primes: List[int] = [2]
    for candidate in range(3, limit + 1, 2):
        if is_prime(candidate):
            primes.append(candidate)
    return primes


def twin_prime_pairs(limit: int) -> List[Tuple[int, int]]:
    """Return twin prime pairs whose elements do not exceed *limit*.

    A twin prime pair consists of two prime numbers where the second is exactly
    two greater than the first (``p`` and ``p + 2``). The upper bound applies to
    the second element of the pair so that every returned value satisfies
    ``p + 2 <= limit``.
    """
    primes = prime_series(limit)
    twin_pairs: List[Tuple[int, int]] = []
    for first, second in zip(primes, primes[1:]):
        if second - first == 2:
            twin_pairs.append((first, second))
    return twin_pairs


def is_armstrong_number(value: int) -> bool:
    """Return ``True`` when ``value`` is an Armstrong (narcissistic) number.

    The check raises each digit to the power of the total digit count and
    compares the resulting sum to the original number. Only non-negative
    integers can satisfy the property; negative inputs always return ``False``.
    """

    if value < 0:
        return False

    digits = [int(digit) for digit in str(value)]
    power = len(digits)
    return value == sum(digit**power for digit in digits)


def armstrong_numbers(limit: int) -> List[int]:
    """Return Armstrong numbers less than or equal to ``limit``.

    The search starts at zero and stops at ``limit``; negative limits yield an
    empty list. Results are ordered from smallest to largest.
    """

    if limit < 0:
        return []

    return [candidate for candidate in range(limit + 1) if is_armstrong_number(candidate)]


def prime_factorization(value: int) -> List[int]:
    """Return the prime factors of ``value`` in non-decreasing order.

    Only integers greater than or equal to ``2`` can be factorized into primes.
    Providing a smaller value raises a :class:`ValueError` to signal invalid
    input. The implementation performs trial division while reusing the
    :func:`is_prime` helper to minimize redundant work when testing larger
    factors.
    """

    if value < 2:
        raise ValueError("Prime factorization is only defined for integers >= 2.")

    remaining = value
    factors: List[int] = []

    # Handle the smallest prime explicitly to enable a consistent odd-step loop
    while remaining % 2 == 0:
        factors.append(2)
        remaining //= 2

    candidate = 3
    limit = isqrt(remaining)
    while candidate <= limit and remaining > 1:
        if remaining % candidate == 0:
            factors.append(candidate)
            remaining //= candidate
            limit = isqrt(remaining)
        else:
            candidate += 2

    if remaining > 1:
        factors.append(remaining)

    return factors


def nth_prime(n: int) -> int:
    """Return the ``n`` th prime number using a straightforward search."""

    if not isinstance(n, int):
        raise TypeError("n must be an integer.")
    if n <= 0:
        raise ValueError("n must be a positive integer.")

    count = 0
    candidate = 2
    while True:  # pragma: no branch - loop exits via return
        if is_prime(candidate):
            count += 1
            if count == n:
                return candidate

        if candidate == 2:
            candidate = 3
        else:
            candidate += 2
