"""Tests for pulse helpers in the TCM decoder."""

import pathlib
import sys

import pytest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp import patterns_by_pulse


def test_floating_pulse_matches_multiple_patterns():
    matches = patterns_by_pulse("floating")

    assert [pattern.code for pattern in matches] == ["WIND_COLD", "WIND_HEAT"]


def test_compound_pulse_description_requires_all_tokens():
    matches = patterns_by_pulse("floating rapid")

    assert [pattern.code for pattern in matches] == ["WIND_HEAT"]


def test_non_matching_pulse_returns_empty_list():
    assert patterns_by_pulse("slow wiry") == []


def test_non_string_input_raises_type_error():
    with pytest.raises(TypeError):
        patterns_by_pulse(42)  # type: ignore[arg-type]
