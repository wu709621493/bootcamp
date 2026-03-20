"""Tests for factorial cell-count variance summaries."""

import pytest

from jb_bootcamp.cell_count_variance import CellCountObservation, summarize_cell_count_variance


@pytest.fixture
def additive_dataset():
    observations = []
    researchers = {
        "R1": -10,
        "R2": -5,
        "R3": 0,
        "R4": 5,
        "R5": 10,
    }
    techniques = {
        "T1": -4,
        "T2": -2,
        "T3": 0,
        "T4": 2,
        "T5": 4,
    }
    counters = {
        "C1": -8,
        "C2": -4,
        "C3": 0,
        "C4": 4,
        "C5": 8,
    }

    for researcher, researcher_effect in researchers.items():
        for technique, technique_effect in techniques.items():
            for counter, counter_effect in counters.items():
                observations.append(
                    CellCountObservation(
                        researcher=researcher,
                        suspension_technique=technique,
                        counter=counter,
                        cell_count=100 + researcher_effect + technique_effect + counter_effect,
                    )
                )
    return observations


def test_summary_reports_expected_overall_values(additive_dataset):
    summary = summarize_cell_count_variance(additive_dataset)

    assert summary["observation_count"] == 125
    assert summary["grand_mean"] == pytest.approx(100.0)
    assert summary["overall_variance"] == pytest.approx(90.7258064516129)


def test_summary_reports_factor_level_stats(additive_dataset):
    summary = summarize_cell_count_variance(additive_dataset)

    assert summary["by_factor"]["researcher"]["R1"]["mean"] == pytest.approx(90.0)
    assert summary["by_factor"]["researcher"]["R1"]["variance"] == pytest.approx(41.666666666666664)
    assert summary["by_factor"]["suspension_technique"]["T5"]["mean"] == pytest.approx(104.0)
    assert summary["by_factor"]["counter"]["C5"]["mean"] == pytest.approx(108.0)


def test_sum_of_squares_decomposition_matches_additive_design(additive_dataset):
    summary = summarize_cell_count_variance(additive_dataset)

    assert summary["sum_of_squares"]["total"] == pytest.approx(11250.0)
    assert summary["sum_of_squares"]["researcher"] == pytest.approx(6250.0)
    assert summary["sum_of_squares"]["suspension_technique"] == pytest.approx(1000.0)
    assert summary["sum_of_squares"]["counter"] == pytest.approx(4000.0)
    assert summary["sum_of_squares"]["residual"] == pytest.approx(0.0)

    assert summary["variance_fraction"]["researcher"] == pytest.approx(0.5555555555555556)
    assert summary["variance_fraction"]["suspension_technique"] == pytest.approx(0.08888888888888889)
    assert summary["variance_fraction"]["counter"] == pytest.approx(0.35555555555555557)
    assert summary["variance_fraction"]["residual"] == pytest.approx(0.0)


def test_summary_accepts_mapping_inputs():
    summary = summarize_cell_count_variance(
        [
            {
                "researcher": "R1",
                "suspension_technique": "T1",
                "counter": "budget",
                "cell_count": 98,
            },
            {
                "researcher": "R2",
                "suspension_technique": "T1",
                "counter": "budget",
                "cell_count": 102,
            },
        ]
    )

    assert summary["grand_mean"] == pytest.approx(100.0)
    assert summary["overall_variance"] == pytest.approx(8.0)



def test_summary_requires_observations():
    with pytest.raises(ValueError):
        summarize_cell_count_variance([])
