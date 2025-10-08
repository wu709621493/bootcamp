"""Tests for Diceware passphrase utilities."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

MODULE_ROOT = Path(__file__).resolve().parents[1] / "modules"
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from jb_bootcamp.jb_bootcamp.diceware import estimate_diceware_entropy


def test_entropy_for_dotted_passphrase():
    passphrase = "Merlot.Hotel.Watch.Dog.fly"
    expected_bits = 5 * math.log2(7776)
    assert estimate_diceware_entropy(passphrase) == pytest.approx(expected_bits)


def test_entropy_for_iterable_passphrase():
    passphrase = ["apple", "banana", "cactus"]
    expected_bits = 3 * math.log2(7776)
    assert estimate_diceware_entropy(passphrase) == pytest.approx(expected_bits)


def test_empty_passphrase_raises():
    with pytest.raises(ValueError):
        estimate_diceware_entropy("")


def test_small_wordlist_raises():
    with pytest.raises(ValueError):
        estimate_diceware_entropy("word", wordlist_size=1)

