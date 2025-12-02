from jb_bootcamp import grant_visitorships
import pytest


def test_grant_visitorships_from_mapping():
    trusted = {"Ada": 0.9, "Grace": 0.6, "Alan": 0.4}
    assert grant_visitorships(trusted, minimum_score=0.5) == ["Ada", "Grace"]


def test_grant_visitorships_from_mixed_iterable():
    entries = [
        (" ada ", 1),
        {"grace": 0.7},
        "Turing",
        ("Grace", 0.8),  # duplicate should be ignored
    ]
    assert grant_visitorships(entries, minimum_score=0.6) == ["ada", "grace", "Turing"]


@pytest.mark.parametrize("bad_entry", ["  ", ("Ada", -0.1), ("Ada", 1.1), {"Ada": 0.5, "Bob": 0.6}])
def test_invalid_entries_raise(bad_entry):
    with pytest.raises((ValueError, TypeError)):
        grant_visitorships([bad_entry])


def test_invalid_threshold():
    with pytest.raises(ValueError):
        grant_visitorships({"Ada": 1.0}, minimum_score=1.5)
