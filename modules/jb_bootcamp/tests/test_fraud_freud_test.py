import pytest

from jb_bootcamp.fraud_freud_test import fraud_freud_test


def test_fraud_freud_test_detects_fraud_text():
    assert fraud_freud_test("This scam used phishing and forgery.") == "fraud"


def test_fraud_freud_test_detects_freud_text():
    assert fraud_freud_test("Freud wrote about ego and unconscious drives.") == "freud"


def test_fraud_freud_test_detects_both_domains():
    assert fraud_freud_test("A fraud case discussed ego and dream analysis.") == "both"


def test_fraud_freud_test_returns_neither_for_unrelated_text():
    assert fraud_freud_test("Clouds drift over the mountain.") == "neither"


def test_fraud_freud_test_type_validation():
    with pytest.raises(TypeError):
        fraud_freud_test(3.14)  # type: ignore[arg-type]
