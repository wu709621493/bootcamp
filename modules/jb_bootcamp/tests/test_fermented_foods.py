import pytest

from jb_bootcamp.fermented_foods import describe_pungency, pungency_index, rank_samples
from jb_bootcamp.fermented_foods import PungencyInputError, PungencyTypeError


def test_reference_serial_is_overpowering():
    score = pungency_index("1123458")
    assert score == pytest.approx(0.7721, rel=1e-3)
    description = describe_pungency("1123458")
    assert description.startswith("Overpowering Ferment")


def test_short_code_is_delicate():
    assert pungency_index("5") < 0.25
    assert describe_pungency("5").startswith("Delicate Ferment")


def test_invalid_inputs_raise():
    with pytest.raises(PungencyInputError):
        pungency_index("12a5")
    with pytest.raises(PungencyInputError):
        pungency_index([])
    with pytest.raises(PungencyTypeError):
        pungency_index(12345)  # type: ignore[arg-type]


def test_rank_samples_orders_highest_first():
    samples = {"market": "1123458", "kitchen": "346", "lab": [4, 2, 1]}
    ranked = rank_samples(samples)
    assert ranked[0][0] == "market"
    assert ranked[-1][0] == "lab"
