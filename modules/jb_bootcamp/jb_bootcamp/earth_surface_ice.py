"""Earth surface ice intervention planning utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

__all__ = [
    "IceField",
    "InterventionPlan",
    "assess_melt_risk",
    "plan_interventions",
]


@dataclass(frozen=True)
class IceField:
    """Description of a managed ice field on Earth's surface.

    Parameters
    ----------
    name:
        Human readable identifier for the ice field.
    area_km2:
        Surface area covered by the field.
    thickness_m:
        Mean thickness of the ice column.
    albedo:
        Fraction of sunlight reflected by the surface.  Values must lie in the
        ``(0, 1]`` interval.
    ocean_influence:
        Positive values indicate additional warming from nearby oceans while
        negative values correspond to inland buffers.  The value is constrained
        to the ``[-1, 1]`` interval to keep risk computations bounded.
    """

    name: str
    area_km2: float
    thickness_m: float
    albedo: float = 0.62
    ocean_influence: float = 0.0

    def __post_init__(self) -> None:  # pragma: no cover - trivial validation
        if not self.name:
            raise ValueError("IceField requires a non-empty name.")
        if self.area_km2 <= 0:
            raise ValueError("area_km2 must be positive.")
        if self.thickness_m <= 0:
            raise ValueError("thickness_m must be positive.")
        if not 0.0 < self.albedo <= 1.0:
            raise ValueError("albedo must lie in the (0, 1] interval.")
        if not -1.0 <= self.ocean_influence <= 1.0:
            raise ValueError("ocean_influence must be between -1 and 1.")


@dataclass(frozen=True)
class InterventionPlan:
    """Recommended action for an ice field."""

    name: str
    risk_score: float
    recommended_action: str
    expected_stability_gain: float
    area_km2: float


def assess_melt_risk(
    field: IceField,
    temperature_anomaly: float,
    *,
    dust_index: float = 0.0,
    solar_radiation: float = 320.0,
) -> float:
    """Return a melt risk score for ``field`` on a ``[0, 10]`` scale.

    The risk metric combines radiative forcing, dust loading and structural
    buffering from the ice thickness.  Values above ``10`` are clamped to keep
    interpretation simple for ranking and planning tasks.
    """

    if dust_index < 0.0:
        raise ValueError("dust_index must be non-negative.")
    if solar_radiation <= 0.0:
        raise ValueError("solar_radiation must be positive.")

    temp_term = max(0.0, temperature_anomaly)
    dust_term = 1.0 + dust_index * 0.4
    albedo_term = 1.0 + (1.0 - field.albedo) * 0.6
    thickness_term = 1.0 / (1.0 + field.thickness_m / 40.0)
    ocean_term = 1.0 + max(0.0, field.ocean_influence) * 0.5
    radiation_term = solar_radiation / 400.0

    base_load = (0.5 + temp_term) * radiation_term * albedo_term
    risk = base_load * dust_term * thickness_term * ocean_term * 4.2
    if risk > 10.0:
        return 10.0
    if risk < 0.0:
        return 0.0
    return risk


def plan_interventions(
    fields: Sequence[IceField],
    temperature_anomalies: Mapping[str, float],
    *,
    dust_alerts: Mapping[str, float] | None = None,
    solar_radiation: float = 320.0,
    max_total_area: float | None = None,
    top_n: int | None = None,
) -> tuple[InterventionPlan, ...]:
    """Rank fields by risk and return intervention recommendations."""

    if max_total_area is not None and max_total_area <= 0:
        raise ValueError("max_total_area must be positive when provided.")
    if top_n is not None and top_n <= 0:
        raise ValueError("top_n must be positive when provided.")

    _ensure_unique_fields(fields)

    dust_alerts = dust_alerts or {}
    for name, value in dust_alerts.items():
        if value < 0.0:
            raise ValueError(f"dust_alerts for {name} must be non-negative.")

    plans = [
        _build_plan(
            field,
            temperature_anomalies,
            dust_alerts,
            solar_radiation,
        )
        for field in fields
    ]

    plans.sort(key=lambda plan: (-plan.risk_score, plan.name))

    selected: list[InterventionPlan] = []
    accumulated_area = 0.0
    for plan in plans:
        if max_total_area is not None and accumulated_area + plan.area_km2 > max_total_area:
            continue
        selected.append(plan)
        accumulated_area += plan.area_km2
        if top_n is not None and len(selected) >= top_n:
            break

    return tuple(selected)


def _build_plan(
    field: IceField,
    temperature_anomalies: Mapping[str, float],
    dust_alerts: Mapping[str, float],
    solar_radiation: float,
) -> InterventionPlan:
    try:
        anomaly = temperature_anomalies[field.name]
    except KeyError as error:  # pragma: no cover - covered via plan_interventions
        raise KeyError(f"Missing temperature anomaly for {field.name}.") from error

    dust_index = dust_alerts.get(field.name, 0.0)
    risk = assess_melt_risk(
        field,
        anomaly,
        dust_index=dust_index,
        solar_radiation=solar_radiation,
    )
    action, gain = _action_for_risk(risk)
    return InterventionPlan(
        name=field.name,
        risk_score=risk,
        recommended_action=action,
        expected_stability_gain=gain,
        area_km2=field.area_km2,
    )


def _action_for_risk(risk: float) -> tuple[str, float]:
    if risk >= 6.5:
        action = "deploy brine curtains and shade canopies"
        gain = min(0.35 + risk * 0.08, 0.95)
    elif risk >= 3.5:
        action = "install reflective mesh and dust fences"
        gain = min(0.22 + risk * 0.06, 0.7)
    else:
        action = "monitor albedo and reroute meltwater"
        gain = min(0.1 + risk * 0.04, 0.45)
    return action, round(gain, 3)


def _ensure_unique_fields(fields: Sequence[IceField]) -> None:
    names: set[str] = set()
    for field in fields:
        if field.name in names:
            raise ValueError("IceField names must be unique.")
        names.add(field.name)
