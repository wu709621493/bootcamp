"""Tests for the drug safety profile helper."""

import pathlib
import sys

import pytest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp import DrugSafetyProfile, drug_safety_profile_check


def test_acetaminophen_second_trimester_is_supported():
    profile = drug_safety_profile_check("Acetaminophen", species="human", pregnancy_stage="Second")

    assert isinstance(profile, DrugSafetyProfile)
    assert profile.status == "compatible"
    assert profile.pregnancy_stage == "second"
    assert "preferred analgesic" in profile.summary.lower()


def test_ibuprofen_third_trimester_contraindicated():
    profile = drug_safety_profile_check("ibuprofen", species="HUMAN", pregnancy_stage="third")

    assert profile.status == "contraindicated"
    assert "ductus arteriosus" in profile.summary.lower()


def test_fly_profiles_are_not_applicable():
    profile = drug_safety_profile_check("caffeine", species="fly")

    assert profile.status == "not_applicable"
    assert profile.pregnancy_stage is None
    assert "oviparous" in profile.summary.lower()


def test_unknown_stage_alias_raises_value_error():
    with pytest.raises(ValueError):
        drug_safety_profile_check("acetaminophen", species="human", pregnancy_stage="late")
