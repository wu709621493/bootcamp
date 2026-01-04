import pytest

from jb_bootcamp.notification import (
    Notification,
    mark_read,
    mark_unread,
    normalize_level,
    summarize_unread,
    unread_count,
)


def test_notification_normalizes_level_and_validates_message():
    note = Notification("Hello", level="WARNING")
    assert note.level == "warning"
    assert note.message == "Hello"
    assert note.read is False

    with pytest.raises(ValueError):
        Notification("", level="info")

    with pytest.raises(ValueError):
        Notification("Hi", level="urgent")


def test_normalize_level_validates_input():
    assert normalize_level("Info") == "info"
    with pytest.raises(ValueError):
        normalize_level("")


def test_mark_read_and_unread_are_idempotent():
    unread = Notification("Ping")
    read = mark_read(unread)
    assert read.read is True
    # idempotent
    assert mark_read(read) is read

    unread_again = mark_unread(read)
    assert unread_again.read is False
    assert mark_unread(unread_again) is unread_again


def test_unread_count_with_filtering():
    notifications = [
        Notification("Ping"),
        Notification("Warning", level="warning", read=True),
        Notification("Error", level="error"),
    ]

    assert unread_count(notifications) == 2
    assert unread_count(notifications, levels=["warning"]) == 0
    assert unread_count(notifications, levels=["error"]) == 1


def test_summarize_unread_counts_by_level():
    notifications = [
        Notification("Info"),
        Notification("Warning", level="warning"),
        Notification("Error", level="error", read=True),
    ]
    assert summarize_unread(notifications) == {"info": 1, "warning": 1}
