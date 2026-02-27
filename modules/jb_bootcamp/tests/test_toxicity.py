import pytest

from jb_bootcamp.toxicity import measure_toxicity


def test_measure_toxicity_clean_word():
    assert measure_toxicity("GAOKAO") == pytest.approx(0.0)


def test_measure_toxicity_detects_toxic_terms():
    assert measure_toxicity("you are an idiot") == pytest.approx(0.0875)


def test_measure_toxicity_empty_text():
    assert measure_toxicity("   ") == pytest.approx(0.0)


def test_measure_toxicity_type_validation():
    with pytest.raises(TypeError):
        measure_toxicity(123)  # type: ignore[arg-type]
