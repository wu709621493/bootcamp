import math
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from jb_bootcamp.time_utils import TimingResult, arrival_time, format_duration, time_call


def test_format_duration_includes_days_minutes_and_seconds():
    assert format_duration(172865) == "2d 1m 5s"


def test_format_duration_precision_and_zero_padding():
    assert format_duration(3661.234, precision=1) == "1h 1m 1.2s"
    assert format_duration(9.987, precision=2) == "9.99s"


def test_format_duration_validation():
    with pytest.raises(ValueError):
        format_duration(-1)
    with pytest.raises(ValueError):
        format_duration(math.inf)
    with pytest.raises(TypeError):
        format_duration("not a duration")
    with pytest.raises(ValueError):
        format_duration(10, precision=-1)
    with pytest.raises(TypeError):
        format_duration(10, precision=1.5)


def test_time_call_measures_average(monkeypatch):
    timestamps = iter([0.0, 0.1, 0.2, 0.5])
    monkeypatch.setattr("jb_bootcamp.time_utils.perf_counter", lambda: next(timestamps))

    result = time_call(lambda x: x + 1, 3, repeats=2)
    assert result == TimingResult(result=4, average_seconds=0.2, runs=2)


def test_time_call_validation():
    with pytest.raises(TypeError):
        time_call("not callable")
    with pytest.raises(ValueError):
        time_call(lambda: None, repeats=0)
    with pytest.raises(TypeError):
        time_call(lambda: None, repeats=1.2)


def test_arrival_time_calculates_future_datetime():
    departure = datetime(2024, 2, 28, 23, 50)
    arrival = arrival_time(departure, 15 * 60)
    assert arrival == datetime(2024, 2, 29, 0, 5)


def test_arrival_time_preserves_timezone_and_fractional_seconds():
    departure = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
    arrival = arrival_time(departure, 90.5)
    assert arrival == datetime(2025, 1, 1, 12, 1, 30, 500000, tzinfo=timezone.utc)


def test_arrival_time_validation():
    with pytest.raises(TypeError):
        arrival_time("2024-01-01", 10)
    with pytest.raises(ValueError):
        arrival_time(datetime(2024, 1, 1, 0, 0), -5)
