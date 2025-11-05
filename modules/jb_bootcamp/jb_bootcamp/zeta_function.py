"""Numerical helpers for evaluating the Riemann zeta function."""

from __future__ import annotations

import cmath
import math

__all__ = ["riemann_zeta"]


def _complex_power(base: int, exponent: complex) -> complex:
    """Return ``base`` raised to ``exponent`` for complex ``exponent``."""

    return cmath.exp(exponent * cmath.log(float(base)))


def riemann_zeta(
    s: complex,
    *,
    tolerance: float = 1e-12,
    max_terms: int = 64,
) -> complex:
    """Approximate ``ζ(s)`` using the globally convergent Hasse series.

    Parameters
    ----------
    s:
        Complex argument of the zeta function.  The implementation supports
        values with ``Re(s) > 0``.  Arguments extremely close to the simple pole
        at ``s = 1`` raise a :class:`ValueError` because the quotient becomes
        numerically unstable.
    tolerance:
        Absolute tolerance used to truncate the series.
    max_terms:
        Maximum number of terms from the outer Hasse summation to evaluate.
    """

    if tolerance <= 0:
        raise ValueError("tolerance must be a positive real number.")
    if max_terms <= 0:
        raise ValueError("max_terms must be a positive integer.")

    s = complex(s)
    if s.real <= 0:
        raise ValueError("riemann_zeta is implemented for arguments with Re(s) > 0.")

    denominator = 1 - _complex_power(2, 1 - s)
    if abs(denominator) < 10 * tolerance:
        raise ValueError("s is too close to the pole at 1 for a stable evaluation.")

    total = 0j
    for n in range(max_terms):
        inner = 0j
        for k in range(n + 1):
            coefficient = (-1) ** k * math.comb(n, k)
            inner += coefficient * _complex_power(k + 1, -s)

        term = inner / (2 ** (n + 1))
        total += term
        if abs(term) < tolerance:
            break
    else:
        raise ValueError("Series did not converge within the allotted terms.")

    return total / denominator

