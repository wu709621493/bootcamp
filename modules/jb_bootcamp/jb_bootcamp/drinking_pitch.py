"""Lightweight helpers to match drink toasting pitch to intended emotion.

The functions in this module turn a whimsical idea—choosing the vocal pitch of
cheers to convey a mood—into deterministic helpers.  They map high-level
emotions to recommended fundamental frequencies (in hertz) and provide a simple
validator that checks whether a measured pitch lands close enough to the
recommendation for the desired mood.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

__all__ = ["EMOTION_PITCH_MAP", "recommended_pitch", "PitchAssessment", "drinking_pitch_test"]


EMOTION_PITCH_MAP: Dict[str, float] = {
    "joy": 330.0,
    "celebration": 310.0,
    "gratitude": 270.0,
    "calm": 200.0,
    "reflection": 180.0,
    "melancholy": 160.0,
}


@dataclass(frozen=True)
class PitchAssessment:
    """Result of comparing a pitch to the target for an emotion."""

    emotion: str
    measured_pitch_hz: float
    target_pitch_hz: float
    difference_hz: float
    match: bool
    message: str


def _normalise_emotion(emotion: str) -> str:
    if not isinstance(emotion, str) or not emotion.strip():
        raise ValueError("emotion must be a non-empty string.")
    return emotion.strip().lower()


def recommended_pitch(emotion: str) -> float:
    """Return the target pitch in hertz for the given *emotion*.

    Parameters
    ----------
    emotion:
        Name of the emotion to express; matching is case-insensitive.

    Raises
    ------
    KeyError
        If the emotion is unknown.
    ValueError
        If *emotion* is empty or whitespace.
    """

    emotion_key = _normalise_emotion(emotion)
    if emotion_key not in EMOTION_PITCH_MAP:
        raise KeyError(
            f"Unknown emotion '{emotion}'. Known options: {', '.join(sorted(EMOTION_PITCH_MAP))}."
        )
    return EMOTION_PITCH_MAP[emotion_key]


def drinking_pitch_test(emotion: str, pitch_hz: float, *, tolerance_hz: float = 12.0) -> PitchAssessment:
    """Assess whether ``pitch_hz`` conveys ``emotion`` within ``tolerance_hz``.

    The helper returns a :class:`PitchAssessment` that records the measured and
    recommended pitch along with a boolean flag indicating whether the measured
    value falls within the specified tolerance.
    """

    if not isinstance(pitch_hz, (int, float)):
        raise TypeError("pitch_hz must be numeric.")
    measured = float(pitch_hz)
    if measured <= 0:
        raise ValueError("pitch_hz must be positive.")

    if not isinstance(tolerance_hz, (int, float)):
        raise TypeError("tolerance_hz must be numeric.")
    tolerance = float(tolerance_hz)
    if tolerance < 0:
        raise ValueError("tolerance_hz cannot be negative.")

    emotion_key = _normalise_emotion(emotion)
    target = recommended_pitch(emotion_key)
    diff = abs(measured - target)
    within = diff <= tolerance

    verb = "matches" if within else "misses"
    message = (
        f"Pitch {measured:.1f} Hz {verb} the {emotion_key} target of {target:.1f} Hz "
        f"by {diff:.1f} Hz (tolerance {tolerance:.1f} Hz)."
    )
    return PitchAssessment(
        emotion=emotion_key,
        measured_pitch_hz=measured,
        target_pitch_hz=target,
        difference_hz=diff,
        match=within,
        message=message,
    )
