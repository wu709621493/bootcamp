"""Tests for the high-speed railway Tamagawa utilities."""

from __future__ import annotations

import pytest

from jb_bootcamp.tamagawa_network import (
    RailwayNetwork,
    Station,
    Track,
    compute_equivariant_tamagawa_index,
)


def build_sample_network() -> RailwayNetwork:
    network = RailwayNetwork()
    network.add_station(Station("A", (0.0, 0.0)))
    network.add_station(Station("B", (1.0, 0.0)))
    network.add_station(Station("C", (2.0, 0.0)))

    network.add_track(Track("A", "B", length_km=10.0, design_speed_kph=300.0))
    network.add_track(Track("B", "C", length_km=10.0, design_speed_kph=200.0))
    network.add_track(Track("A", "C", length_km=30.0, design_speed_kph=300.0))
    return network


def test_travel_time_chooses_fastest_path():
    network = build_sample_network()
    travel_time = network.travel_time("A", "C")
    # A -> B -> C is faster than the direct A -> C track.
    expected = (10.0 / 300.0) + (10.0 / 200.0)
    assert travel_time == pytest.approx(expected)


def test_itinerary_time_accumulates_segments():
    network = build_sample_network()
    itinerary = ["A", "B", "C", "A"]
    time = network.itinerary_time(itinerary)
    expected = (10.0 / 300.0) + (10.0 / 200.0) + (30.0 / 300.0)
    assert time == pytest.approx(expected)


def test_local_tamagawa_factors_and_equivariant_index():
    network = build_sample_network()
    local = network.local_tamagawa_factors()
    assert local == {
        "A": pytest.approx(21.0),
        "B": pytest.approx(26.0),
        "C": pytest.approx(16.0),
    }

    invariant = compute_equivariant_tamagawa_index(network, [["A", "C"], ["B"]])
    expected_orbit_mean = (21.0 + 16.0) / 2.0
    expected = expected_orbit_mean * 26.0
    assert invariant == pytest.approx(expected)


def test_unreachable_station_raises_error():
    network = RailwayNetwork()
    network.add_station(Station("A", (0.0, 0.0)))
    network.add_station(Station("B", (1.0, 0.0)))
    network.add_station(Station("C", (2.0, 0.0)))
    network.add_track(Track("A", "B", length_km=10.0, design_speed_kph=250.0, bidirectional=False))

    with pytest.raises(ValueError):
        network.travel_time("B", "A")


def test_invalid_orbit_configuration():
    network = build_sample_network()
    with pytest.raises(ValueError):
        compute_equivariant_tamagawa_index(network, [["A", "A"]])
    with pytest.raises(KeyError):
        compute_equivariant_tamagawa_index(network, [["A", "D"]])
    with pytest.raises(ValueError):
        compute_equivariant_tamagawa_index(network, [[]])

