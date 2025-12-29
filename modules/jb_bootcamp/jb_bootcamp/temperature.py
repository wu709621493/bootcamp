"""Utilities for working with basic temperature readings."""
from __future__ import annotations

from numbers import Real
from typing import Iterable, List

__all__ = [
    "celsius_to_fahrenheit",
    "fahrenheit_to_celsius",
    "mean_temperature",
    "temperature_range",
]


def _validate_number(value: Real, name: str) -> float:
    """Return ``value`` as a float after validating it is numeric.

    Boolean values are rejected even though they subclass :class:`int`.
    """

    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    return float(value)


def _validate_series(readings: Iterable[Real]) -> List[float]:
    """Validate a series of temperature readings and return them as floats."""

    validated: List[float] = []
    for index, reading in enumerate(readings):
        validated.append(_validate_number(reading, f"reading {index}"))

    if not validated:
        raise ValueError("readings must contain at least one value.")

    return validated


def celsius_to_fahrenheit(celsius: Real) -> float:
    """Convert a Celsius temperature to Fahrenheit."""

    value = _validate_number(celsius, "celsius")
    return (value * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit: Real) -> float:
    """Convert a Fahrenheit temperature to Celsius."""

    value = _validate_number(fahrenheit, "fahrenheit")
    return (value - 32) * 5 / 9


def mean_temperature(readings: Iterable[Real]) -> float:
    """Return the arithmetic mean of provided temperature readings."""

    values = _validate_series(readings)
    return sum(values) / len(values)


def temperature_range(readings: Iterable[Real]) -> float:
    """Return the difference between the highest and lowest readings."""

    values = _validate_series(readings)
    return max(values) - min(values)
