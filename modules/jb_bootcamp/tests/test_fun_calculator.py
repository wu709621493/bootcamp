"""Tests for the fun score calculator."""

import math

import pytest

from jb_bootcamp.fun_calculator import cal_fun


def test_balanced_group_reaches_high_score():
    score = cal_fun(attendees=18, excitement_levels=[0.9, 0.95, 0.92], collaboration=0.88, chaos=0.05, novelty=0.7)
    assert math.isclose(score, 9.11, rel_tol=1e-3)


def test_penalty_from_chaos():
    calm_score = cal_fun(attendees=6, excitement_levels=[0.8, 0.76], collaboration=0.65, chaos=0.0, novelty=0.4)
    chaotic_score = cal_fun(attendees=6, excitement_levels=[0.8, 0.76], collaboration=0.65, chaos=0.6, novelty=0.4)
    assert chaotic_score < calm_score


def test_invalid_inputs_raise_errors():
    with pytest.raises(ValueError):
        cal_fun(attendees=0, excitement_levels=[0.8], collaboration=0.5)

    with pytest.raises(ValueError):
        cal_fun(attendees=5, excitement_levels=[], collaboration=0.5)

    with pytest.raises(ValueError):
        cal_fun(attendees=5, excitement_levels=[1.2], collaboration=0.5)

    with pytest.raises(TypeError):
        cal_fun(attendees=5, excitement_levels=["very"], collaboration=0.5)
