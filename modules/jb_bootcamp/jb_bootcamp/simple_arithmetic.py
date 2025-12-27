"""Basic arithmetic utilities with strict input validation."""

from __future__ import annotations

import re
from numbers import Number

__all__ = ["add", "expo", "parse_sum_expression", "verify_sum"]


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


def parse_sum_expression(expression: str) -> Number:
    """Compute the sum expressed as a simple ``"A+B"`` string.

    The parser accepts optional whitespace around the operator and unary plus or
    minus signs on each operand, allowing inputs such as ``"1++1"`` or
    ``"10 + -3"``. Only numeric literals are permitted; any other characters or
    additional operators raise ``ValueError``.

    Parameters
    ----------
    expression
        String representing a single addition expression.

    Returns
    -------
    Number
        The computed sum of the two operands.

    Raises
    ------
    TypeError
        If ``expression`` is not a string.
    ValueError
        If the expression does not match the supported ``A+B`` pattern.
    """

    if not isinstance(expression, str):
        raise TypeError("expression must be a string.")

    match = re.fullmatch(
        r"\s*([+-]?\d+(?:\.\d+)?)\s*\+\s*([+-]?\d+(?:\.\d+)?)\s*",
        expression,
    )
    if not match:
        raise ValueError(
            "expression must be in the form 'A+B' with optional unary signs and whitespace."
        )

    left_literal, right_literal = match.groups()
    left_number = float(left_literal) if "." in left_literal else int(left_literal)
    right_number = float(right_literal) if "." in right_literal else int(right_literal)

    return add(left_number, right_number)
