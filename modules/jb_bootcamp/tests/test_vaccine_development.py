import pytest

from jb_bootcamp.vaccine_development import (
    normalize_curve,
    normalize_vaccine_development_curves,
)


def test_normalize_curve_basic():
    assert normalize_curve([2.0, 4.0, 6.0]) == (0.0, 0.5, 1.0)


def test_normalize_curve_constant():
    assert normalize_curve([3.0, 3.0, 3.0, 3.0]) == (0.0, 0.0, 0.0, 0.0)


def test_normalize_curve_raises_on_empty():
    with pytest.raises(ValueError):
        normalize_curve([])


def test_normalize_vaccine_development_curves_mapping():
    curves = {
        "candidate_alpha": [0, 10, 20, 30],
        "candidate_beta": [5, 5, 10],
    }

    normalised = normalize_vaccine_development_curves(curves)

    assert normalised["candidate_alpha"] == (0.0, 0.3333333333333333, 0.6666666666666666, 1.0)
    assert normalised["candidate_beta"] == (0.0, 0.0, 1.0)


def test_normalize_vaccine_development_curves_rejects_blank_name():
    with pytest.raises(ValueError):
        normalize_vaccine_development_curves({"": [1, 2, 3]})
