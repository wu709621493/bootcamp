"""Lightweight utilities for reasoning about drug safety in pregnancy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

__all__ = ["DrugSafetyProfile", "drug_safety_profile_check"]


@dataclass(frozen=True)
class DrugSafetyProfile:
    """Structured safety recommendation for a drug/species combination."""

    drug: str
    species: str
    pregnancy_stage: str | None
    status: str
    summary: str
    notes: Tuple[str, ...] = ()


def _profile(status: str, summary: str, notes: Iterable[str] | None = None) -> Tuple[str, str, Tuple[str, ...]]:
    """Return a normalised tuple representing a safety profile entry."""

    return status, summary, tuple(notes or ())


# Internal reference data used for exercises and unit tests.
_SAFETY_DATA: Dict[str, Dict[str, Dict[str | None, Tuple[str, str, Tuple[str, ...]]]]] = {}


def _register(
    drug: str,
    species: str,
    profiles: Dict[str | None, Tuple[str, str, Tuple[str, ...]]],
) -> None:
    drug_key = drug.strip().lower()
    species_key = species.strip().lower()
    _SAFETY_DATA.setdefault(drug_key, {})[species_key] = profiles


# Populate structured entries used by the bootcamp exercises.
_acetaminophen_default = _profile(
    "compatible",
    "Acetaminophen is the preferred analgesic during pregnancy when used at therapeutic doses.",
    (
        "Limit cumulative daily dose to avoid hepatotoxicity.",
        "Pair with non-pharmacological pain strategies where possible.",
    ),
)
_register(
    "acetaminophen",
    "human",
    {
        None: _acetaminophen_default,
        "first": _acetaminophen_default,
        "second": _acetaminophen_default,
        "third": _acetaminophen_default,
    },
)

_ibuprofen_pre_third = _profile(
    "caution",
    "Ibuprofen may be used cautiously before the third trimester when benefits outweigh risks.",
    (
        "Limit to short courses and monitor for gastrointestinal side-effects.",
        "Consider acetaminophen as the first-line alternative.",
    ),
)
_ibuprofen_third = _profile(
    "contraindicated",
    "Third-trimester ibuprofen increases the risk of premature ductus arteriosus closure and oligohydramnios.",
    (
        "Switch to acetaminophen or consult a maternal-fetal specialist for alternatives.",
    ),
)
_register(
    "ibuprofen",
    "human",
    {
        None: _ibuprofen_pre_third,
        "first": _ibuprofen_pre_third,
        "second": _ibuprofen_pre_third,
        "third": _ibuprofen_third,
    },
)

_caffeine_fly = _profile(
    "not_applicable",
    "Drosophila melanogaster are oviparous; pregnancy-specific safety categories do not apply.",
    (
        "Report exposure in terms of dietary concentration or larval medium instead of maternal trimester.",
    ),
)
_register(
    "caffeine",
    "fly",
    {
        None: _caffeine_fly,
    },
)


def _normalise_stage(stage: str | None) -> str | None:
    if stage is None:
        return None

    value = stage.strip().lower()
    if not value:
        return None

    aliases = {
        "1": "first",
        "1st": "first",
        "first": "first",
        "2": "second",
        "2nd": "second",
        "second": "second",
        "3": "third",
        "3rd": "third",
        "third": "third",
    }

    value = value.replace("trimester", "").strip()
    normalised = aliases.get(value)
    if normalised is None:
        raise ValueError(
            "pregnancy_stage must be one of 'first', 'second', or 'third' when provided."
        )
    return normalised


def drug_safety_profile_check(
    drug: str,
    *,
    species: str = "human",
    pregnancy_stage: str | None = None,
) -> DrugSafetyProfile:
    """Look up safety guidance for a drug during pregnancy."""

    if not drug or drug.strip() == "":
        raise ValueError("drug must be a non-empty string.")

    drug_key = drug.strip().lower()
    species_key = species.strip().lower()
    stage_key = _normalise_stage(pregnancy_stage)

    try:
        species_map = _SAFETY_DATA[drug_key]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise KeyError(f"No safety data available for drug {drug!r}.") from exc

    try:
        stage_map = species_map[species_key]
    except KeyError as exc:
        raise KeyError(
            f"No pregnancy safety data for drug {drug!r} in species {species!r}."
        ) from exc

    profile_tuple = stage_map.get(stage_key)
    if profile_tuple is None and stage_key is not None:
        profile_tuple = stage_map.get(None)
        if profile_tuple is None:
            available = sorted(k for k in stage_map.keys() if k is not None)
            available_str = ", ".join(available) if available else ""
            raise KeyError(
                "No safety data for the requested pregnancy stage." +
                (f" Available stages: {available_str}." if available_str else "")
            )

    if profile_tuple is None:
        raise KeyError("No default pregnancy safety data for the requested combination.")

    status, summary, notes = profile_tuple
    return DrugSafetyProfile(
        drug=drug_key,
        species=species_key,
        pregnancy_stage=stage_key,
        status=status,
        summary=summary,
        notes=notes,
    )
