"""Utilities for interpreting vehicle energy specifications.

This module provides helpers for parsing strings that describe a
progression of vehicles and the metadata associated with an energy chart.
The user prompt that inspired this module looked like::

    mopad->motorcycle->4-wheel-drive->.space-vessel.->
    energy.chart.localization.=propelant.type.ecological.impact.epact.dat.fly

The :func:`parse_vehicle_energy_spec` function turns an expression like
this into a structured dictionary that is easier to reason about in
Python code.  In addition, :func:`build_vehicle_energy_chart` enriches the
resulting data with qualitative information about each vehicle in the
sequence so it can be used directly in data analysis or reporting tools.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from difflib import get_close_matches
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence


@dataclass(frozen=True)
class VehicleEnergyProfile:
    """Description of the energy characteristics of a vehicle.

    Parameters
    ----------
    name:
        Human readable name of the vehicle.  The value is stored in lower
        case for easier matching.
    propellant_type:
        The primary propellant or energy source used by the vehicle.
    ecological_impact:
        A qualitative statement about the ecological footprint of the
        vehicle relative to the other entries in the chain.
    notes:
        Optional free-form description providing additional context.
    """

    name: str
    propellant_type: str
    ecological_impact: str
    notes: str = ""


DEFAULT_VEHICLE_PROFILES: Mapping[str, VehicleEnergyProfile] = {
    "mopad": VehicleEnergyProfile(
        name="moped",
        propellant_type="small gasoline engine",
        ecological_impact="low",
        notes=(
            "Lightweight two-wheel vehicle.  Impact dominated by combustion "
            "of a compact gasoline engine."
        ),
    ),
    "moped": VehicleEnergyProfile(
        name="moped",
        propellant_type="small gasoline engine",
        ecological_impact="low",
        notes=(
            "Alias for mopad to accommodate common spelling variations in "
            "energy chain specifications."
        ),
    ),
    "motorcycle": VehicleEnergyProfile(
        name="motorcycle",
        propellant_type="gasoline engine",
        ecological_impact="moderate",
        notes=(
            "Greater fuel consumption than a moped but still relatively "
            "efficient compared to larger road vehicles."
        ),
    ),
    "4-wheel-drive": VehicleEnergyProfile(
        name="4-wheel drive",
        propellant_type="diesel or gasoline engine",
        ecological_impact="high",
        notes=(
            "Heavy chassis and drivetrain reduce efficiency; emissions are "
            "significantly higher than two-wheel vehicles."
        ),
    ),
    "space-vessel": VehicleEnergyProfile(
        name="space vessel",
        propellant_type="cryogenic liquid propellant",
        ecological_impact="very high",
        notes=(
            "Orbital and deep-space launches require high-energy propellants "
            "with substantial manufacturing and launch impacts."
        ),
    ),
}


PROFILE_ALIASES: Mapping[str, Iterable[str]] = {
    "mopad": ("moped", "mopad"),
    "motorcycle": ("motorbike", "motor-cycle"),
    "4-wheel-drive": ("four-wheel-drive", "4wd", "4-wheel-drive"),
    "space-vessel": ("spacecraft", "space-vessel", "spaceship"),
}


def _normalize_token(token: str) -> str:
    """Return a normalized version of a token taken from a specification string."""

    cleaned = token.strip().strip(".").replace(" ", "-")
    return cleaned.lower()


def parse_vehicle_energy_spec(spec: str) -> Dict[str, object]:
    """Parse a vehicle energy specification into structured components.

    Parameters
    ----------
    spec:
        Raw specification string containing tokens separated by ``->``.

    Returns
    -------
    dict
        A dictionary containing the ordered ``vehicle_chain`` along with a
        nested dictionary describing the ``chart_assignment``.  The latter
        is created by interpreting the segment that contains an ``=`` sign
        as a mapping from the path on the left-hand side to the path on the
        right-hand side.
    """

    if not spec or not spec.strip():
        raise ValueError("Specification string must be a non-empty value.")

    segments = [segment for segment in spec.split("->") if segment and segment.strip()]
    if not segments:
        raise ValueError("Specification must contain at least one segment.")

    vehicle_chain: List[str] = []
    chart_assignment: MutableMapping[str, Sequence[str]] | None = None

    for segment in segments:
        normalized = _normalize_token(segment)
        if not normalized:
            continue
        if "=" in normalized:
            if chart_assignment is not None:
                raise ValueError("Specification contains multiple chart assignments.")
            lhs, rhs = normalized.split("=", 1)
            left_path = tuple(filter(None, lhs.split(".")))
            right_path = tuple(filter(None, rhs.split(".")))
            if not left_path or not right_path:
                raise ValueError("Chart assignment must include both chart and attribute paths.")
            chart_assignment = {
                "chart_path": left_path,
                "attribute_path": right_path,
            }
        else:
            vehicle_chain.append(normalized)

    if not vehicle_chain:
        raise ValueError("Specification must contain at least one vehicle token.")
    if chart_assignment is None:
        raise ValueError("Specification must include a chart assignment segment.")

    return {
        "vehicle_chain": vehicle_chain,
        "chart_assignment": chart_assignment,
    }


def build_vehicle_energy_chart(
    spec: str,
    profiles: Mapping[str, VehicleEnergyProfile] | None = None,
) -> Dict[str, object]:
    """Construct an enriched energy chart description from a specification.

    Parameters
    ----------
    spec:
        Specification string describing a sequence of vehicles followed by
        an energy chart mapping as consumed by
        :func:`parse_vehicle_energy_spec`.
    profiles:
        Optional mapping that supplies :class:`VehicleEnergyProfile`
        instances.  When omitted, :data:`DEFAULT_VEHICLE_PROFILES` is used.

    Returns
    -------
    dict
        Dictionary containing the parsed specification along with a list of
        profile dictionaries in the ``profiles`` key.  Profiles are returned
        in the order they appear in the vehicle chain.  If a vehicle is not
        present in the provided profiles mapping, a minimal profile is
        generated on-the-fly to preserve the entry in the output.
    """

    parsed = parse_vehicle_energy_spec(spec)
    profile_store = profiles or DEFAULT_VEHICLE_PROFILES

    profile_entries: List[Mapping[str, str]] = []
    for token in parsed["vehicle_chain"]:
        profile = _resolve_profile(token, profile_store)
        profile_entries.append(asdict(profile))

    enriched = dict(parsed)
    enriched["profiles"] = profile_entries
    return enriched


__all__ = [
    "VehicleEnergyProfile",
    "DEFAULT_VEHICLE_PROFILES",
    "PROFILE_ALIASES",
    "parse_vehicle_energy_spec",
    "build_vehicle_energy_chart",
]


def _resolve_profile(token: str, profile_store: Mapping[str, VehicleEnergyProfile]) -> VehicleEnergyProfile:
    """Return a profile for *token*, tolerating simple misspellings."""

    if token in profile_store:
        return profile_store[token]

    for canonical, aliases in PROFILE_ALIASES.items():
        if token == canonical:
            if canonical in profile_store:
                return profile_store[canonical]
        elif token in aliases:
            if canonical in profile_store:
                return profile_store[canonical]

    close_match = _nearest_profile_key(token, profile_store)
    if close_match is not None:
        return profile_store[close_match]

    return VehicleEnergyProfile(
        name=token.replace("-", " "),
        propellant_type="unknown",
        ecological_impact="unknown",
        notes="Auto-generated profile for unrecognized vehicle.",
    )


def _nearest_profile_key(
    token: str, profile_store: Mapping[str, VehicleEnergyProfile]
) -> str | None:
    """Return the closest matching profile key for *token* when available."""

    matches = get_close_matches(token, profile_store.keys(), n=1, cutoff=0.85)
    return matches[0] if matches else None

