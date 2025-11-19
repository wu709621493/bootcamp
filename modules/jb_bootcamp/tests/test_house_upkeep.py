import math
import pathlib
import sys

import pytest


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))


from jb_bootcamp.house_upkeep import TaskProjection, UpkeepPlanner, VillaProfile, suggest_upkeep_tasks


def test_villa_profile_and_suggestion_scaling():
    compact = VillaProfile(
        name="梅园",
        floor_count=2,
        area_m2=220,
        resident_count=3,
        has_garden=False,
    )
    estate = VillaProfile(
        name="大别野",
        floor_count=4,
        area_m2=620,
        resident_count=8,
        has_garden=True,
        has_pool=True,
        has_guesthouse=True,
    )

    compact_tasks = suggest_upkeep_tasks(compact)
    estate_tasks = suggest_upkeep_tasks(estate)

    assert len(estate_tasks) == len(compact_tasks) + 3

    compact_by_name = {task.name: task for task in compact_tasks}
    estate_by_name = {task.name: task for task in estate_tasks}

    for key in {"interior detailing", "laundry and linens"}:
        assert estate_by_name[key].duration_hours > compact_by_name[key].duration_hours


def test_planner_projects_and_balances_staff():
    profile = VillaProfile(name="大别野", floor_count=3, area_m2=480, resident_count=6)
    tasks = suggest_upkeep_tasks(profile)
    planner = UpkeepPlanner(profile, tasks)

    projections = planner.project_cycle(7)
    assert all(isinstance(item, TaskProjection) for item in projections)

    laundry = next(proj for proj in projections if proj.task.name == "laundry and linens")
    assert laundry.occurrences == math.ceil(7 / laundry.task.frequency_days)
    assert pytest.approx(laundry.total_hours, rel=1e-6) == laundry.occurrences * laundry.task.duration_hours

    staff = ["阿福", "Lena", "Bo"]
    assignments = planner.assign_staff(staff, days=7)

    assert set(assignments) == set(staff)
    assert sum(len(bucket) for bucket in assignments.values()) == len(projections)

    staff_hours = {name: sum(item.total_hours for item in bucket) for name, bucket in assignments.items()}
    assert max(staff_hours.values()) - min(staff_hours.values()) <= max(item.total_hours for item in projections)


def test_planner_requires_tasks_and_staff():
    profile = VillaProfile(name="晓院", floor_count=1, area_m2=120, resident_count=2)

    with pytest.raises(ValueError):
        UpkeepPlanner(profile, [])

    planner = UpkeepPlanner(profile, suggest_upkeep_tasks(profile))

    with pytest.raises(ValueError):
        planner.assign_staff([], days=3)

