"""Lightweight tools for working with notifications.

The helpers in this module keep notifications immutable and easy to reason
about.  They support common tasks such as normalizing levels, marking
notifications as read, and summarizing unread alerts.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Iterable, Sequence

__all__ = [
    "Notification",
    "normalize_level",
    "mark_read",
    "mark_unread",
    "unread_count",
    "summarize_unread",
]


_VALID_LEVELS = {"info", "warning", "error", "success"}


@dataclass(frozen=True)
class Notification:
    """Simple immutable notification record.

    Parameters
    ----------
    message:
        User-facing message; must be a non-empty string.
    level:
        Optional severity level (``info``, ``warning``, ``error``, or
        ``success``).  Case-insensitive and normalized to lowercase.
    read:
        Whether the notification has already been read.
    """

    message: str
    level: str = "info"
    read: bool = False

    def __post_init__(self) -> None:  # pragma: no cover - simple guard
        if not self.message:
            raise ValueError("Notification message must be non-empty.")
        normalized = normalize_level(self.level)
        object.__setattr__(self, "level", normalized)


def normalize_level(level: str) -> str:
    """Return a lowercase notification level after validation.

    Parameters
    ----------
    level:
        Level string to validate.

    Raises
    ------
    ValueError
        If ``level`` is empty or not one of the allowed values.
    """

    if not level:
        raise ValueError("Level must be a non-empty string.")

    normalized = level.lower()
    if normalized not in _VALID_LEVELS:
        allowed = ", ".join(sorted(_VALID_LEVELS))
        raise ValueError(f"Invalid level: {level!r}. Allowed levels: {allowed}.")
    return normalized


def mark_read(notification: Notification) -> Notification:
    """Return a copy of ``notification`` marked as read."""

    if notification.read:
        return notification
    return replace(notification, read=True)


def mark_unread(notification: Notification) -> Notification:
    """Return a copy of ``notification`` marked as unread."""

    if not notification.read:
        return notification
    return replace(notification, read=False)


def unread_count(notifications: Iterable[Notification], levels: Sequence[str] | None = None) -> int:
    """Count unread notifications, optionally filtering by levels."""

    normalized_levels = None
    if levels is not None:
        normalized_levels = {normalize_level(level) for level in levels}
    count = 0
    for notification in notifications:
        if notification.read:
            continue
        if normalized_levels is not None and notification.level not in normalized_levels:
            continue
        count += 1
    return count


def summarize_unread(notifications: Iterable[Notification]) -> Dict[str, int]:
    """Return a summary of unread notifications per level."""

    summary: Dict[str, int] = {level: 0 for level in _VALID_LEVELS}
    for notification in notifications:
        if not notification.read:
            summary[notification.level] = summary.get(notification.level, 0) + 1
    # Remove any unexpected levels that may have crept in
    return {level: count for level, count in summary.items() if count > 0}
