"""Utilities for modelling a temporary visual input hijack."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class HijackWindow:
    """A time window during which visual input is hijacked."""

    start: int
    duration: int

    @property
    def stop(self) -> int:
        """Exclusive end index for the hijack period."""
        return self.start + self.duration


def temporary_visual_input_hijack(
    baseline_stream: Sequence[T],
    hijacked_stream: Iterable[T],
    start: int,
    duration: int | None = None,
) -> list[T]:
    """Return a copy of ``baseline_stream`` with a temporary hijack applied.

    Parameters
    ----------
    baseline_stream:
        Original stream of visual inputs.
    hijacked_stream:
        Replacement values to inject during hijack.
    start:
        Index in ``baseline_stream`` where hijack starts.
    duration:
        Number of slots hijacked. If omitted, the length of ``hijacked_stream``
        is used.
    """
    if start < 0:
        raise ValueError("start must be non-negative")

    replacement = list(hijacked_stream)
    if duration is None:
        duration = len(replacement)

    if duration < 0:
        raise ValueError("duration must be non-negative")

    result = list(baseline_stream)
    if not result or duration == 0 or start >= len(result):
        return result

    window = HijackWindow(start=start, duration=duration)
    if not replacement:
        return result

    for index in range(window.start, min(window.stop, len(result))):
        source_index = index - window.start
        if source_index >= len(replacement):
            break
        result[index] = replacement[source_index]

    return result


__all__ = ["HijackWindow", "temporary_visual_input_hijack"]
