"""Basic arithmetic utilities with strict input validation."""

from __future__ import annotations

from numbers import Number

__all__ = ["add", "expo", "verify_sum"]


def _ensure_numeric(value: Number, name: str) -> Number:
    """Return ``value`` if it is numeric, otherwise raise ``TypeError``."""

    if not isinstance(value, Number):
        raise TypeError(f"{name} must be numeric; got {value!r}.")
    return value


def add(left: Number, right: Number) -> Number:
    """Return the arithmetic sum of ``left`` and ``right``.

    Both inputs must be numeric. The function preserves the numeric type of
    the operands (e.g., integers stay integers, complex numbers stay complex)
    by delegating to Python's native addition after validation.
    """

    left_numeric = _ensure_numeric(left, "left")
    right_numeric = _ensure_numeric(right, "right")
    return left_numeric + right_numeric


def expo(base: Number, exponent: Number) -> Number:
    """Return ``base`` raised to the power of ``exponent`` with validation.

    The function accepts any numeric ``base`` but restricts ``exponent`` to
    non-negative integers to avoid surprising implicit conversions. Inputs are
    validated before computing the power.

    Raises
    ------
    TypeError
        If ``base`` is not numeric or ``exponent`` is not an integer.
    ValueError
        If ``exponent`` is negative.
    """

    base_numeric = _ensure_numeric(base, "base")
    exponent_numeric = _ensure_numeric(exponent, "exponent")

    if not isinstance(exponent_numeric, int) or isinstance(exponent_numeric, bool):
        raise TypeError("exponent must be an integer.")
    if exponent_numeric < 0:
        raise ValueError("exponent must be non-negative.")

    return base_numeric**exponent_numeric


def verify_sum(left: Number, right: Number, expected: Number) -> bool:
    """Validate that ``left + right`` equals ``expected``.

    Parameters
    ----------
    left, right
        Numeric operands to add together.
    expected
        Target value that the sum should match.

    Returns
    -------
    bool
        ``True`` if the sum matches ``expected``.

    Raises
    ------
    TypeError
        If any of the inputs are not numeric.
    ValueError
        If the computed sum does not equal ``expected``.
    """

    result = add(left, right)
    if result != expected:
        raise ValueError(
            f"Expected {left!r} + {right!r} to equal {expected!r}, got {result!r}."
        )
    return True
