"""Tools for designing a perfume formula from aromatic notes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

__all__ = [
    "PerfumeNote",
    "PerfumeBlend",
    "concentration_label",
    "build_perfume",
    "estimate_longevity_hours",
]


@dataclass(frozen=True)
class PerfumeNote:
    """Single aromatic ingredient used in a blend."""

    name: str
    family: str
    intensity: float
    volatility: float

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Note name cannot be empty.")
        if not self.family:
            raise ValueError("Note family cannot be empty.")
        if not 0.0 <= self.intensity <= 1.0:
            raise ValueError("intensity must be between 0 and 1.")
        if not 0.0 <= self.volatility <= 1.0:
            raise ValueError("volatility must be between 0 and 1.")


@dataclass(frozen=True)
class PerfumeBlend:
    """Computed blend details for a perfume recipe."""

    concentration: str
    note_volumes_ml: dict[str, float]
    top_heart_base_ratio: tuple[float, float, float]


def concentration_label(oil_fraction: float) -> str:
    """Return standard perfume naming for aromatic oil fraction."""

    if not 0 < oil_fraction <= 1:
        raise ValueError("oil_fraction must be in the (0, 1] range.")
    if oil_fraction >= 0.30:
        return "parfum"
    if oil_fraction >= 0.20:
        return "eau de parfum"
    if oil_fraction >= 0.10:
        return "eau de toilette"
    return "eau de cologne"


def build_perfume(
    notes: Sequence[PerfumeNote],
    ratios: Mapping[str, float],
    *,
    total_volume_ml: float,
    oil_fraction: float,
) -> PerfumeBlend:
    """Create a blend by distributing aromatic oil over selected notes."""

    if not notes:
        raise ValueError("At least one note is required.")
    if total_volume_ml <= 0:
        raise ValueError("total_volume_ml must be positive.")

    note_map = {note.name: note for note in notes}
    if len(note_map) != len(notes):
        raise ValueError("Note names must be unique.")

    total_ratio = 0.0
    for name, ratio in ratios.items():
        if name not in note_map:
            raise KeyError(f"Unknown note in ratios: {name}.")
        if ratio < 0:
            raise ValueError("Ratios must be non-negative.")
        total_ratio += ratio

    if total_ratio <= 0:
        raise ValueError("Ratios must include at least one positive value.")

    aromatic_oil_ml = total_volume_ml * oil_fraction
    volumes: dict[str, float] = {}
    for name, ratio in ratios.items():
        volumes[name] = aromatic_oil_ml * ratio / total_ratio

    top, heart, base = _accord_breakdown(note_map, volumes)
    return PerfumeBlend(
        concentration=concentration_label(oil_fraction),
        note_volumes_ml=volumes,
        top_heart_base_ratio=(top, heart, base),
    )


def estimate_longevity_hours(notes: Sequence[PerfumeNote], oil_fraction: float) -> float:
    """Estimate wear time in hours based on volatility and concentration."""

    if not notes:
        raise ValueError("At least one note is required.")

    concentration = max(0.05, min(oil_fraction, 0.4))
    avg_fixative = sum(1.0 - note.volatility for note in notes) / len(notes)
    avg_intensity = sum(note.intensity for note in notes) / len(notes)
    return round(2.0 + 18.0 * concentration * (0.6 * avg_fixative + 0.4 * avg_intensity), 2)


def _accord_breakdown(
    note_map: Mapping[str, PerfumeNote],
    volumes: Mapping[str, float],
) -> tuple[float, float, float]:
    top = 0.0
    heart = 0.0
    base = 0.0
    total = sum(volumes.values())
    for name, volume in volumes.items():
        volatility = note_map[name].volatility
        if volatility >= 0.66:
            top += volume
        elif volatility >= 0.33:
            heart += volume
        else:
            base += volume

    if total <= 0:
        return (0.0, 0.0, 0.0)
    return (top / total, heart / total, base / total)
