import pytest

from jb_bootcamp.drinking_pitch import (
    EMOTION_PITCH_MAP,
    PitchAssessment,
    drinking_pitch_test,
    recommended_pitch,
)


def test_recommended_pitch_lookup_is_case_insensitive():
    assert recommended_pitch("Joy") == EMOTION_PITCH_MAP["joy"]
    assert recommended_pitch(" reflection ") == EMOTION_PITCH_MAP["reflection"]


def test_recommended_pitch_unknown_emotion():
    with pytest.raises(KeyError):
        recommended_pitch("bewilderment")


def test_drinking_pitch_test_matches_within_tolerance():
    assessment = drinking_pitch_test("gratitude", EMOTION_PITCH_MAP["gratitude"] + 3)
    assert isinstance(assessment, PitchAssessment)
    assert assessment.match is True
    assert "matches the gratitude target" in assessment.message


def test_drinking_pitch_test_rejects_negative_pitch():
    with pytest.raises(ValueError):
        drinking_pitch_test("calm", -10.0)


def test_drinking_pitch_test_requires_known_emotion():
    with pytest.raises(KeyError):
        drinking_pitch_test("confusion", 200.0)


def test_drinking_pitch_test_respects_tolerance():
    assessment = drinking_pitch_test("melancholy", EMOTION_PITCH_MAP["melancholy"] + 15, tolerance_hz=10)
    assert assessment.match is False
    assert assessment.difference_hz == pytest.approx(15)
