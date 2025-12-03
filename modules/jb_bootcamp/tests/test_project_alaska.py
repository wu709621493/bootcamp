import pytest

from jb_bootcamp.project_alaska import (
    AlaskaSite,
    SitePriority,
    assess_resupply_gap,
    prioritize_sites,
)


def test_assess_resupply_gap_balanced_site():
    site = AlaskaSite(
        name="Nome",
        population=2500,
        fuel_liters=32000,
        food_days=12.0,
        runway_length_m=1830,
        daylight_hours=5.5,
    )

    score, limiting = assess_resupply_gap(site)

    assert score == pytest.approx(2.46)
    assert limiting == "food"


def test_assess_resupply_gap_runway_limited():
    site = AlaskaSite(
        name="Kivalina",
        population=500,
        fuel_liters=1000,
        food_days=3.0,
        runway_length_m=600,
        daylight_hours=3.2,
    )

    score, limiting = assess_resupply_gap(site)

    assert score == pytest.approx(9.48)
    assert limiting == "runway access"


def test_prioritize_sites_respects_storm_and_daylight():
    sites = [
        AlaskaSite("Nome", 2500, 32000, 12.0, 1830, daylight_hours=5.5),
        AlaskaSite("Bethel", 1800, 14000, 7.0, 1600, daylight_hours=3.5),
        AlaskaSite("Kotzebue", 3200, 36000, 9.0, 1900, daylight_hours=7.0),
    ]

    ranked = prioritize_sites(
        sites,
        storm_risk={"Bethel": 0.6},
        daylight_overrides={"Bethel": 3.0},
    )

    assert isinstance(ranked, tuple)
    assert [entry.name for entry in ranked] == ["Bethel", "Kotzebue", "Nome"]

    bethel = ranked[0]
    assert bethel.priority_score > 7.0
    assert "daylight" in bethel.limiting_factor
    assert "heavy-lift" in bethel.recommended_action


def test_prioritize_sites_max_sites_and_validation():
    sites = [
        AlaskaSite("SiteA", 200, 2400, 5.0, 1100),
        AlaskaSite("SiteB", 300, 1000, 4.0, 700),
        AlaskaSite("SiteC", 400, 8000, 15.0, 1200),
    ]

    top_two = prioritize_sites(sites, max_sites=2)
    assert len(top_two) == 2
    assert all(isinstance(entry, SitePriority) for entry in top_two)

    with pytest.raises(ValueError):
        prioritize_sites(sites, max_sites=0)

    with pytest.raises(ValueError):
        prioritize_sites(sites + [AlaskaSite("SiteA", 50, 500, 2, 400)])
