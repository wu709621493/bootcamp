"""Helpers for rebuilding educational HIV regimen "cocktails".

These utilities are designed for bootcamp exercises and are not a
substitute for clinical guidance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

__all__ = [
    "HIVCocktail",
    "classify_antiretroviral",
    "rebuild_hiv_cocktail",
    "format_hiv_cocktail_summary",
]


_DRUG_CLASSES: dict[str, tuple[str, ...]] = {
    "nrtis": (
        "abacavir",
        "emtricitabine",
        "lamivudine",
        "tenofovir alafenamide",
        "tenofovir disoproxil fumarate",
        "zidovudine",
    ),
    "nnrtis": (
        "doravirine",
        "efavirenz",
        "etravirine",
        "nevirapine",
        "rilpivirine",
    ),
    "instis": (
        "bictegravir",
        "dolutegravir",
        "elvitegravir",
        "raltegravir",
    ),
    "pis": (
        "atazanavir",
        "darunavir",
        "lopinavir",
    ),
}

_ANCHOR_PRIORITY: tuple[str, ...] = ("instis", "nnrtis", "pis")
_DISCOURAGED_PI_AGENTS: tuple[str, ...] = ("lopinavir",)


@dataclass(frozen=True)
class HIVCocktail:
    """Structured representation of a simplified HIV regimen."""

    backbone: tuple[str, ...]
    anchor: str | None
    extras: tuple[str, ...] = ()
    unknown: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


def _normalise_drug_name(drug: str) -> str:
    return " ".join(drug.strip().lower().split())


def classify_antiretroviral(drug: str) -> str | None:
    """Return the antiretroviral class for *drug*, if known."""

    if not drug or drug.strip() == "":
        raise ValueError("drug must be a non-empty string.")

    normalised = _normalise_drug_name(drug)
    for class_name, drugs in _DRUG_CLASSES.items():
        if normalised in drugs:
            return class_name
    return None


def _dedupe(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def rebuild_hiv_cocktail(drugs: Sequence[str]) -> HIVCocktail:
    """Rebuild a simplified HIV cocktail from a list of drug names."""

    if not drugs:
        raise ValueError("drugs must contain at least one entry.")

    normalised = [_normalise_drug_name(drug) for drug in drugs if drug and drug.strip()]
    if not normalised:
        raise ValueError("drugs must contain at least one non-empty entry.")

    classified: dict[str, list[str]] = {key: [] for key in _DRUG_CLASSES}
    unknown: list[str] = []
    filtered_discouraged_pis: list[str] = []

    for drug in normalised:
        class_name = classify_antiretroviral(drug)
        if class_name is None:
            unknown.append(drug)
        elif class_name == "pis" and drug in _DISCOURAGED_PI_AGENTS:
            filtered_discouraged_pis.append(drug)
        else:
            classified[class_name].append(drug)

    backbone = _dedupe(classified["nrtis"])
    anchor = None
    extras: list[str] = []
    for class_name in _ANCHOR_PRIORITY:
        if classified[class_name]:
            anchor = classified[class_name][0]
            extras.extend(classified[class_name][1:])
            break

    for class_name in _ANCHOR_PRIORITY:
        if class_name in classified and classified[class_name]:
            if classified[class_name][0] != anchor:
                extras.extend(classified[class_name])

    if len(backbone) > 2:
        extras.extend(backbone[2:])
        backbone = backbone[:2]

    notes: list[str] = []
    if len(backbone) < 2:
        notes.append("Backbone incomplete: expect two NRTIs for the core pair.")
    if anchor is None:
        notes.append("No anchor agent detected (INSTI/NNRTI/PI).")
    if unknown:
        notes.append("Unknown agents were provided and are listed separately.")
    if filtered_discouraged_pis:
        notes.append(
            "Discouraged PI agents were filtered out: "
            + ", ".join(_dedupe(filtered_discouraged_pis))
            + "."
        )

    return HIVCocktail(
        backbone=backbone,
        anchor=anchor,
        extras=_dedupe(extras),
        unknown=_dedupe(unknown),
        notes=tuple(notes),
    )


def format_hiv_cocktail_summary(cocktail: HIVCocktail) -> str:
    """Return a human-readable summary for a rebuilt cocktail."""

    backbone = ", ".join(cocktail.backbone) if cocktail.backbone else "none"
    anchor = cocktail.anchor or "none"
    extras = ", ".join(cocktail.extras) if cocktail.extras else "none"
    unknown = ", ".join(cocktail.unknown) if cocktail.unknown else "none"

    summary = (
        f"Backbone: {backbone}. Anchor: {anchor}. "
        f"Extras: {extras}. Unknown: {unknown}."
    )

    if cocktail.notes:
        notes = " ".join(cocktail.notes)
        return f"{summary} Notes: {notes}"
    return summary
