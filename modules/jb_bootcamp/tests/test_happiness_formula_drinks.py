"""Tests for drink happiness formula."""

import math

import pytest

from jb_bootcamp.happiness_formula_drinks import happiness_formula_drinks


def test_balanced_drink_scores_high():
    score = happiness_formula_drinks(
        hydration=0.9,
        flavor=0.85,
        social_context=0.8,
        caffeine=0.4,
        sugar=0.1,
        alcohol=0.0,
    )
    assert math.isclose(score, 88.2, rel_tol=1e-3)


def test_penalties_reduce_score():
    light = happiness_formula_drinks(0.75, 0.75, 0.75, sugar=0.05, alcohol=0.0)
    heavy = happiness_formula_drinks(0.75, 0.75, 0.75, sugar=0.8, alcohol=0.7)
    assert heavy < light


def test_input_validation():
    with pytest.raises(ValueError):
        happiness_formula_drinks(1.1, 0.8, 0.9)

    with pytest.raises(TypeError):
        happiness_formula_drinks("high", 0.8, 0.9)
