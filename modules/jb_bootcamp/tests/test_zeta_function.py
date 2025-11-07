"""Tests for the numerical Riemann zeta approximation."""

from __future__ import annotations

import math
import pathlib
import sys

import pytest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp.zeta_function import find_first_riemann_zero, riemann_zeta


def test_riemann_zeta_matches_known_even_values():
    # ζ(2) = π^2 / 6 and ζ(4) = π^4 / 90
    assert riemann_zeta(2, tolerance=1e-14, max_terms=512) == pytest.approx(
        (math.pi ** 2) / 6,
        rel=1e-12,
    )
    assert riemann_zeta(4, tolerance=1e-14, max_terms=128) == pytest.approx(
        (math.pi ** 4) / 90,
        rel=1e-12,
    )


def test_complex_argument_is_supported():
    value = riemann_zeta(0.75 + 2.0j, tolerance=1e-14, max_terms=64)
    # Reference value computed with high precision using ``mpmath``.
    expected = 0.5170887213140056 - 0.33863252815887j
    assert value == pytest.approx(expected, rel=1e-9, abs=1e-9)


def test_invalid_parameters_raise_value_error():
    with pytest.raises(ValueError):
        riemann_zeta(0.0)
    with pytest.raises(ValueError):
        riemann_zeta(2, tolerance=-1.0)
    with pytest.raises(ValueError):
        riemann_zeta(2, max_terms=0)


def test_first_riemann_zero_search():
    zero = find_first_riemann_zero()
    assert zero.real == pytest.approx(0.5, abs=1e-12)
    assert zero.imag == pytest.approx(14.134725141, rel=1e-6)
    zeta_value = riemann_zeta(zero, tolerance=1e-14, max_terms=512)
    assert abs(zeta_value) < 5e-9

