"""Utilities for formatting and measuring durations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from time import perf_counter
from typing import Callable, Iterable, Tuple

__all__ = ["format_duration", "time_call", "TimingResult", "arrival_time"]


@dataclass(frozen=True)
class TimingResult:
    """Outcome and average runtime of a callable."""

    result: object
    average_seconds: float
    runs: int


def _validate_seconds(seconds: object) -> float:
    if not isinstance(seconds, (int, float)) or isinstance(seconds, bool):
        raise TypeError("Duration must be a numeric value in seconds.")

    value = float(seconds)
    if value < 0:
        raise ValueError("Duration cannot be negative.")
    if value == float("inf") or value != value:
        raise ValueError("Duration must be finite.")
    return value


def format_duration(seconds: object, *, precision: int = 1) -> str:
    """Return ``seconds`` as a human-readable string.

    Parameters
    ----------
    seconds
        A numeric quantity representing seconds; must be finite and non-negative.
    precision
        Number of decimal places to display for the seconds component.
    """

    value = _validate_seconds(seconds)
    if not isinstance(precision, int):
        raise TypeError("precision must be an integer.")
    if precision < 0:
        raise ValueError("precision must be non-negative.")

    units: Iterable[Tuple[str, float]] = (
        ("d", 86400.0),
        ("h", 3600.0),
        ("m", 60.0),
    )
    remaining = value
    parts: list[str] = []

    for label, unit_seconds in units:
        if remaining >= unit_seconds or parts:
            unit_value = int(remaining // unit_seconds)
            if unit_value:
                parts.append(f"{unit_value}{label}")
            remaining -= unit_value * unit_seconds

    seconds_formatted = f"{remaining:.{precision}f}" if precision else str(int(round(remaining)))
    parts.append(f"{seconds_formatted.rstrip('0').rstrip('.') if precision else seconds_formatted}s")
    return " ".join(parts)


def arrival_time(departure: datetime, travel_seconds: object) -> datetime:
    """Return the arrival time after travelling for ``travel_seconds``.

    ``travel_seconds`` must be a finite, non-negative numeric duration. The
    returned :class:`~datetime.datetime` preserves the timezone information of
    the ``departure`` instance.
    """

    if not isinstance(departure, datetime):
        raise TypeError("departure must be a datetime.")

    duration = timedelta(seconds=_validate_seconds(travel_seconds))
    return departure + duration


def time_call(func: Callable, *args, repeats: int = 1, **kwargs) -> TimingResult:
    """Measure the average runtime of ``func``.

    The callable is executed ``repeats`` times with the provided arguments. The
    result from the final run is returned alongside the average duration.
    """

    if not callable(func):
        raise TypeError("func must be callable.")
    if not isinstance(repeats, int):
        raise TypeError("repeats must be an integer.")
    if repeats < 1:
        raise ValueError("repeats must be at least 1.")

    total = 0.0
    result = None
    for _ in range(repeats):
        start = perf_counter()
        result = func(*args, **kwargs)
        total += perf_counter() - start

    average = total / repeats
    return TimingResult(result=result, average_seconds=average, runs=repeats)
