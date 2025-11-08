"""Symmetry-aware analytics for high-speed railway networks.

This module offers a playful take on the equivariant Tamagawa number
conjecture (ETNC) by translating its language of global and local
invariants into the setting of transportation planning.  We represent a
railway network as a graph whose vertices are stations and whose edges
are high-speed track segments.  From that representation we can compute
shortest travel times as well as symmetry-respecting aggregations that
mirror the spirit of Tamagawa measures.

The design philosophy is practical despite the whimsical mathematical
inspiration.  Engineers can use :class:`RailwayNetwork` to evaluate the
connectivity of a proposed infrastructure project, and planners can
build orbit decompositions of stations to quantify how well a timetable
honours network symmetries.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
from typing import Dict, Iterable, Iterator, List, Mapping, Sequence, Tuple

__all__ = [
    "Station",
    "Track",
    "RailwayNetwork",
    "compute_equivariant_tamagawa_index",
]


@dataclass(frozen=True)
class Station:
    """Representation of a railway station.

    Parameters
    ----------
    name:
        A unique identifier for the station.
    coordinates:
        The (x, y) coordinates of the station in kilometres.  The unit
        choice is arbitrary but must be consistent with the track
        lengths to give interpretable travel times.
    weight:
        A dimensionless factor describing how important the station is
        in the global infrastructure plan.  The default weight is 1.0.
    """

    name: str
    coordinates: Tuple[float, float]
    weight: float = 1.0

    def __post_init__(self) -> None:  # pragma: no cover - simple validation
        if not self.name:
            raise ValueError("station name must be a non-empty string")
        if len(self.coordinates) != 2:
            raise ValueError("station coordinates must contain exactly two values")

    def distance_to(self, other: "Station") -> float:
        """Return the Euclidean distance to *other* in kilometres."""

        x0, y0 = self.coordinates
        x1, y1 = other.coordinates
        return math.hypot(x0 - x1, y0 - y1)


@dataclass(frozen=True)
class Track:
    """A single railway track segment connecting two stations."""

    origin: str
    destination: str
    length_km: float
    design_speed_kph: float
    bidirectional: bool = True

    def __post_init__(self) -> None:  # pragma: no cover - simple validation
        if self.length_km <= 0.0:
            raise ValueError("track length must be positive")
        if self.design_speed_kph <= 0.0:
            raise ValueError("design speed must be positive")
        if self.origin == self.destination:
            raise ValueError("tracks must connect distinct stations")

    @property
    def travel_time_hours(self) -> float:
        """Return the travel time in hours for this segment."""

        return self.length_km / self.design_speed_kph


class RailwayNetwork:
    """A railway network with high-speed track segments."""

    def __init__(self) -> None:
        self._stations: Dict[str, Station] = {}
        self._tracks: List[Track] = []
        self._adjacency: Dict[str, List[Tuple[str, float]]] = {}

    def add_station(self, station: Station) -> None:
        """Add *station* to the network."""

        if station.name in self._stations:
            raise ValueError(f"station '{station.name}' already exists")
        self._stations[station.name] = station
        self._adjacency.setdefault(station.name, [])

    def add_track(self, track: Track) -> None:
        """Add *track* to the network."""

        if track.origin not in self._stations:
            raise KeyError(f"unknown origin station '{track.origin}'")
        if track.destination not in self._stations:
            raise KeyError(f"unknown destination station '{track.destination}'")

        self._tracks.append(track)
        travel_time = track.travel_time_hours
        self._adjacency[track.origin].append((track.destination, travel_time))

        if track.bidirectional:
            self._adjacency[track.destination].append((track.origin, travel_time))

    def stations(self) -> Iterator[Station]:
        """Iterate over stations in insertion order."""

        return iter(self._stations.values())

    def travel_time(self, origin: str, destination: str) -> float:
        """Return the shortest travel time between two stations in hours."""

        if origin not in self._stations:
            raise KeyError(f"unknown origin station '{origin}'")
        if destination not in self._stations:
            raise KeyError(f"unknown destination station '{destination}'")
        if origin == destination:
            return 0.0

        queue: List[Tuple[float, str]] = [(0.0, origin)]
        visited: Dict[str, float] = {}

        while queue:
            current_time, station = heapq.heappop(queue)
            if station in visited and current_time >= visited[station]:
                continue
            visited[station] = current_time

            if station == destination:
                return current_time

            for neighbour, travel_time in self._adjacency.get(station, []):
                next_time = current_time + travel_time
                if neighbour not in visited or next_time < visited[neighbour]:
                    heapq.heappush(queue, (next_time, neighbour))

        raise ValueError(f"destination '{destination}' is not reachable from '{origin}'")

    def itinerary_time(self, stops: Sequence[str]) -> float:
        """Return the travel time for visiting *stops* in order."""

        if len(stops) < 2:
            return 0.0
        total = 0.0
        for start, end in zip(stops, stops[1:]):
            leg_time = None
            for neighbour, travel_time in self._adjacency.get(start, []):
                if neighbour == end:
                    leg_time = travel_time
                    break
            if leg_time is None:
                leg_time = self.travel_time(start, end)
            total += leg_time
        return total

    def local_tamagawa_factors(self) -> Dict[str, float]:
        """Return local invariants inspired by Tamagawa measures."""

        factors: Dict[str, float] = {
            name: station.weight for name, station in self._stations.items()
        }
        for track in self._tracks:
            contribution = track.design_speed_kph / track.length_km
            factors[track.origin] += 0.5 * contribution
            factors[track.destination] += 0.5 * contribution
        return factors

    def adjacency(self) -> Mapping[str, List[Tuple[str, float]]]:
        """Expose the adjacency mapping (read-only usage expected)."""

        return self._adjacency


def compute_equivariant_tamagawa_index(
    network: RailwayNetwork,
    orbits: Iterable[Iterable[str]],
    *,
    weight_exponent: float = 1.0,
) -> float:
    """Compute an equivariant Tamagawa index for *network*.

    Parameters
    ----------
    network:
        The :class:`RailwayNetwork` to analyse.
    orbits:
        An iterable of station-name collections describing the orbits of
        a symmetry group action.  Each orbit contributes an averaged
        local factor to the final product.
    weight_exponent:
        A scaling exponent applied to every orbit average.  Values must
        be strictly positive.
    """

    if weight_exponent <= 0.0:
        raise ValueError("weight_exponent must be positive")

    local_factors = network.local_tamagawa_factors()
    covered: set[str] = set()
    invariant = 1.0

    for orbit in orbits:
        orbit_list = list(orbit)
        if not orbit_list:
            raise ValueError("orbit collections must be non-empty")

        total = 0.0
        for station_name in orbit_list:
            if station_name not in local_factors:
                raise KeyError(f"orbit references unknown station '{station_name}'")
            if station_name in covered:
                raise ValueError(f"station '{station_name}' appears in multiple orbits")
            covered.add(station_name)
            total += local_factors[station_name]

        average = total / len(orbit_list)
        invariant *= math.pow(average, weight_exponent)

    # Include stations that were not explicitly assigned to an orbit by
    # treating them as singleton orbits.  This ensures that the measure
    # accounts for the entire network.
    for station_name, local_factor in local_factors.items():
        if station_name not in covered:
            invariant *= math.pow(local_factor, weight_exponent)

    return invariant

