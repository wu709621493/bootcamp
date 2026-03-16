import pytest

from jb_bootcamp.temporary_visual_input_hijack import (
    HijackWindow,
    temporary_visual_input_hijack,
)


def test_hijack_window_stop_property():
    window = HijackWindow(start=3, duration=5)
    assert window.stop == 8


def test_hijack_replaces_requested_segment():
    baseline = ["a", "b", "c", "d", "e"]
    hijacked = ["x", "y"]

    result = temporary_visual_input_hijack(baseline, hijacked, start=1)

    assert result == ["a", "x", "y", "d", "e"]


def test_hijack_respects_duration_boundaries():
    baseline = [0, 1, 2, 3, 4]
    hijacked = [9, 8, 7]

    result = temporary_visual_input_hijack(baseline, hijacked, start=3, duration=5)

    assert result == [0, 1, 2, 9, 8]


def test_hijack_with_zero_duration_returns_copy():
    baseline = [1, 2, 3]

    result = temporary_visual_input_hijack(baseline, [9], start=1, duration=0)

    assert result == baseline
    assert result is not baseline


def test_hijack_raises_for_negative_start():
    with pytest.raises(ValueError, match="start must be non-negative"):
        temporary_visual_input_hijack([1], [2], start=-1)


def test_hijack_raises_for_negative_duration():
    with pytest.raises(ValueError, match="duration must be non-negative"):
        temporary_visual_input_hijack([1], [2], start=0, duration=-2)
