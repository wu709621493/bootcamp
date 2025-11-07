"""Numerical helpers for evaluating the Riemann zeta function."""

from __future__ import annotations

import cmath
import math

__all__ = ["riemann_zeta", "find_first_riemann_zero"]


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


def find_first_riemann_zero(
    *,
    t_lower: float = 13.0,
    t_upper: float = 15.0,
    tolerance: float = 1e-10,
    max_iterations: int = 64,
    zeta_tolerance: float = 1e-14,
    zeta_max_terms: int = 256,
) -> complex:
    """Locate the first nontrivial zero of ``ζ(s)`` on the critical line.

    The function performs a golden-section search on ``|ζ(1/2 + it)|`` within the
    provided interval ``[t_lower, t_upper]``.  The default bounds bracket the
    first nontrivial zero near ``t ≈ 14.1347``.  The search terminates when the
    interval width falls below ``tolerance`` or once ``max_iterations`` have
    elapsed.

    Parameters
    ----------
    t_lower, t_upper:
        Bounds for the search along the imaginary axis.  ``t_lower`` must be
        strictly less than ``t_upper``.
    tolerance:
        Desired precision of the imaginary component of the zero.
    max_iterations:
        Maximum number of refinement steps performed by the search.
    zeta_tolerance, zeta_max_terms:
        Parameters forwarded to :func:`riemann_zeta` for each function
        evaluation.

    Returns
    -------
    complex
        Approximation to the first nontrivial zero ``1/2 + it``.

    Raises
    ------
    ValueError
        If ``t_lower`` is not strictly less than ``t_upper`` or if the search
        fails to converge within ``max_iterations``.
    """

    if t_lower >= t_upper:
        raise ValueError("t_lower must be strictly less than t_upper.")
    if tolerance <= 0:
        raise ValueError("tolerance must be a positive real number.")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be a positive integer.")

    phi = (1 + math.sqrt(5)) / 2
    inv_phi = 1 / phi

    lower = float(t_lower)
    upper = float(t_upper)

    def evaluate(t: float) -> complex:
        return riemann_zeta(
            0.5 + 1j * t,
            tolerance=zeta_tolerance,
            max_terms=zeta_max_terms,
        )

    def magnitude(t: float) -> float:
        return abs(evaluate(t))

    width = upper - lower
    c = upper - inv_phi * width
    d = lower + inv_phi * width
    f_c = magnitude(c)
    f_d = magnitude(d)

    for _ in range(max_iterations):
        if upper - lower < tolerance:
            break
        if f_c < f_d:
            upper = d
            d = c
            f_d = f_c
            width = upper - lower
            c = upper - inv_phi * width
            f_c = magnitude(c)
        else:
            lower = c
            c = d
            f_c = f_d
            width = upper - lower
            d = lower + inv_phi * width
            f_d = magnitude(d)
    else:
        raise ValueError("Search did not converge within max_iterations.")

    t = 0.5 * (lower + upper)
    return 0.5 + 1j * t

