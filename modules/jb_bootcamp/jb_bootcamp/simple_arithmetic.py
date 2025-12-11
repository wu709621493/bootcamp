"""Basic arithmetic utilities with strict input validation."""

from __future__ import annotations

from numbers import Number

__all__ = ["add", "verify_sum"]


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
