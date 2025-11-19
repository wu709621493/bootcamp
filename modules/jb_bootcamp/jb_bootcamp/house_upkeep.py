"""House upkeep planning tools tailored for sprawling villas (大别野).

The goal of the module is to provide light-weight primitives that let a user
describe the footprint of a large home, generate a tailored set of upkeep
tasks, and distribute the work evenly across a team of caretakers.  The
functions are intentionally deterministic, making it straightforward to unit
test different scenarios or plug the logic into a larger workflow.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Dict, Iterable, List, Sequence


@dataclass(frozen=True)
class VillaProfile:
    """Description of a 大别野 (villa) that needs upkeep."""

    name: str
    floor_count: int
    area_m2: float
    resident_count: int
    has_garden: bool = True
    has_pool: bool = False
    has_guesthouse: bool = False

    def __post_init__(self) -> None:  # pragma: no cover - trivial validation
        if not self.name:
            raise ValueError("The villa must have a name.")
        if self.floor_count <= 0:
            raise ValueError("floor_count must be positive.")
        if self.area_m2 <= 0:
            raise ValueError("area_m2 must be positive.")
        if self.resident_count < 0:
            raise ValueError("resident_count cannot be negative.")


@dataclass(frozen=True)
class UpkeepTask:
    """Repeated task needed to keep a villa pristine."""

    name: str
    frequency_days: int
    duration_hours: float
    priority: int = 1
    zone: str = "general"
    notes: str = ""

    def __post_init__(self) -> None:  # pragma: no cover - trivial validation
        if not self.name:
            raise ValueError("Tasks must be named.")
        if self.frequency_days <= 0:
            raise ValueError("frequency_days must be positive.")
        if self.duration_hours <= 0:
            raise ValueError("duration_hours must be positive.")
        if self.priority <= 0:
            raise ValueError("priority must be positive.")


@dataclass(frozen=True)
class TaskProjection:
    """Result of expanding a task over a planning horizon."""

    task: UpkeepTask
    occurrences: int
    total_hours: float

    def __post_init__(self) -> None:  # pragma: no cover - trivial validation
        if self.occurrences <= 0:
            raise ValueError("occurrences must be positive.")
        if self.total_hours <= 0:
            raise ValueError("total_hours must be positive.")


def _effort_multiplier(profile: VillaProfile) -> float:
    """Return a multiplier derived from area, floors, and residents."""

    area_factor = max(1.0, profile.area_m2 / 200.0)
    floor_factor = 1.0 + 0.2 * (profile.floor_count - 1)
    resident_factor = 1.0 + 0.1 * max(0, profile.resident_count - 2)
    return area_factor * floor_factor * resident_factor


def suggest_upkeep_tasks(profile: VillaProfile) -> List[UpkeepTask]:
    """Generate a deterministic task list tailored to *profile*."""

    multiplier = _effort_multiplier(profile)

    def hours(base: float) -> float:
        return round(base * multiplier, 2)

    tasks: List[UpkeepTask] = [
        UpkeepTask(
            name="interior detailing",
            frequency_days=3,
            duration_hours=hours(1.8),
            priority=3,
            zone="interior",
            notes="Deep dusting and vacuuming across all levels.",
        ),
        UpkeepTask(
            name="laundry and linens",
            frequency_days=2,
            duration_hours=hours(1.2),
            priority=2,
            zone="service wing",
        ),
        UpkeepTask(
            name="air circulation check",
            frequency_days=7,
            duration_hours=hours(0.8),
            priority=1,
            zone="interior",
        ),
        UpkeepTask(
            name="security perimeter walk",
            frequency_days=1,
            duration_hours=hours(0.6),
            priority=4,
            zone="exterior",
        ),
    ]

    if profile.has_garden:
        tasks.append(
            UpkeepTask(
                name="garden grooming",
                frequency_days=3,
                duration_hours=hours(1.5),
                priority=3,
                zone="garden",
                notes="Pruning of courtyards and bamboo screens.",
            )
        )
    if profile.has_pool:
        tasks.append(
            UpkeepTask(
                name="pool care",
                frequency_days=2,
                duration_hours=hours(1.0),
                priority=3,
                zone="spa",
                notes="Skimming, chemistry check, and pump purge.",
            )
        )
    if profile.has_guesthouse:
        tasks.append(
            UpkeepTask(
                name="guesthouse refresh",
                frequency_days=7,
                duration_hours=hours(2.0),
                priority=2,
                zone="guest wing",
            )
        )

    tasks.sort(key=lambda task: task.name)
    return tasks


class UpkeepPlanner:
    """Roll a villa profile and associated tasks into actionable plans."""

    def __init__(self, profile: VillaProfile, tasks: Iterable[UpkeepTask]):
        self.profile = profile
        self.tasks = list(tasks)
        if not self.tasks:
            raise ValueError("At least one task is required to plan upkeep.")

    def project_cycle(self, days: int) -> List[TaskProjection]:
        """Return task projections needed to cover *days* days."""

        if days <= 0:
            raise ValueError("days must be positive.")

        projections: List[TaskProjection] = []
        for task in self.tasks:
            occurrences = math.ceil(days / task.frequency_days)
            total_hours = round(occurrences * task.duration_hours, 2)
            projections.append(
                TaskProjection(task=task, occurrences=occurrences, total_hours=total_hours)
            )

        projections.sort(key=lambda proj: proj.task.name)
        return projections

    def total_hours(self, days: int) -> float:
        """Convenience helper returning the aggregate projected hours."""

        return round(sum(proj.total_hours for proj in self.project_cycle(days)), 2)

    def assign_staff(
        self, staff: Sequence[str], days: int
    ) -> Dict[str, List[TaskProjection]]:
        """Distribute projected tasks to *staff* balancing total hours."""

        members = [member for member in staff if member]
        if not members:
            raise ValueError("At least one staff member must be provided.")

        projections = sorted(
            self.project_cycle(days),
            key=lambda proj: (-proj.task.priority, -proj.total_hours, proj.task.name),
        )

        assignments: Dict[str, List[TaskProjection]] = {member: [] for member in members}
        load_tracker: Dict[str, float] = {member: 0.0 for member in members}

        for projection in projections:
            assignee = min(load_tracker, key=load_tracker.get)
            assignments[assignee].append(projection)
            load_tracker[assignee] += projection.total_hours

        return assignments

