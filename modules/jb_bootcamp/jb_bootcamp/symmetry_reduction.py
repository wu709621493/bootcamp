"""Symmetry-aware dimensionality reduction for folding energy landscapes.

This module provides helper functions that perform a lightweight principal
component analysis (PCA) on complex barrier sequences produced by
``InfiniteSequenceFly``.  By studying the covariance of the real and
imaginary components we obtain the dominant axes that describe the spiral-like
geometry of the fly's energy landscape.

The implementation avoids external dependencies so that it can be imported in
minimal environments.  Only the Python standard library is used to construct
the covariance matrix and to compute the closed-form eigen-decomposition of a
2x2 symmetric matrix.  The resulting axes describe how symmetric the
landscape is in the complex plane and yield a natural, low-dimensional summary
of its structure.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from .folding_energy import imaginary_potential_barriers

Point = Tuple[float, float]


@dataclass(frozen=True)
class PrincipalAxis:
    """Description of a principal axis in the complex plane."""

    eigenvalue: float
    direction: Point


@dataclass(frozen=True)
class SymmetryResult:
    """Summary statistics describing the dimensionality of a sequence."""

    centroid: Point
    principal_axes: Tuple[PrincipalAxis, PrincipalAxis]
    axis_ratio: float

    def variance_explained(self) -> Tuple[float, float]:
        """Return the fraction of variance captured by the two axes."""

        leading, trailing = self.principal_axes
        total = leading.eigenvalue + trailing.eigenvalue
        if total <= 0.0:
            return (0.0, 0.0)
        return (leading.eigenvalue / total, trailing.eigenvalue / total)


def _mean(points: Sequence[Point]) -> Point:
    if not points:
        raise ValueError("At least one point is required to compute the mean.")
    total_x = sum(x for x, _ in points)
    total_y = sum(y for _, y in points)
    n = len(points)
    return (total_x / n, total_y / n)


def _covariance_matrix(points: Sequence[Point]) -> Tuple[float, float, float]:
    if len(points) < 2:
        raise ValueError("At least two points are required to compute covariance.")

    mean_x, mean_y = _mean(points)
    sum_xx = 0.0
    sum_xy = 0.0
    sum_yy = 0.0
    for x, y in points:
        dx = x - mean_x
        dy = y - mean_y
        sum_xx += dx * dx
        sum_xy += dx * dy
        sum_yy += dy * dy

    scale = 1.0 / (len(points) - 1)
    return (sum_xx * scale, sum_xy * scale, sum_yy * scale)


def _normalize_vector(vector: Point) -> Point:
    vx, vy = vector
    length = math.hypot(vx, vy)
    if length == 0.0:
        return (1.0, 0.0)
    return (vx / length, vy / length)


def _principal_axes_from_covariance(
    a: float, b: float, c: float
) -> Tuple[PrincipalAxis, PrincipalAxis]:
    trace = a + c
    determinant = a * c - b * b
    discriminant_sq = max(trace * trace - 4.0 * determinant, 0.0)
    discriminant = math.sqrt(discriminant_sq)

    eigenvalue1 = 0.5 * (trace + discriminant)
    eigenvalue2 = 0.5 * (trace - discriminant)

    def eigenvector(eigenvalue: float) -> Point:
        if abs(b) > 1e-12 or abs(a - eigenvalue) > abs(c - eigenvalue):
            vx = b
            vy = eigenvalue - a
        else:
            vx = eigenvalue - c
            vy = b
        vector = _normalize_vector((vx, vy))
        if vector[0] < 0:
            vector = (-vector[0], -vector[1])
        return vector

    axis1 = PrincipalAxis(eigenvalue1, eigenvector(eigenvalue1))
    axis2 = PrincipalAxis(eigenvalue2, eigenvector(eigenvalue2))

    if axis1.eigenvalue < axis2.eigenvalue:
        axis1, axis2 = axis2, axis1

    return axis1, axis2


def _axis_ratio(axes: Tuple[PrincipalAxis, PrincipalAxis]) -> float:
    leading, trailing = axes
    if trailing.eigenvalue <= 0.0:
        return math.inf
    return math.sqrt(leading.eigenvalue / trailing.eigenvalue)


def analyze_complex_symmetry(sequence: Sequence[complex]) -> SymmetryResult:
    """Perform a PCA-like analysis on a complex sequence.

    Parameters
    ----------
    sequence:
        Iterable of complex numbers to analyse.  The real and imaginary
        components are treated as coordinates in the plane.
    """

    points = [(z.real, z.imag) for z in sequence]
    if len(points) < 2:
        raise ValueError("At least two complex points are required for analysis.")

    covariance = _covariance_matrix(points)
    axes = _principal_axes_from_covariance(*covariance)
    centroid = _mean(points)
    return SymmetryResult(centroid=centroid, principal_axes=axes, axis_ratio=_axis_ratio(axes))


def analyze_fly_landscape(
    levels: int, *, parameters: Iterable[float] | None = None, **kwargs: float
) -> SymmetryResult:
    """Analyse the symmetry of the fly's energy landscape.

    Parameters
    ----------
    levels:
        Number of folding levels to include in the landscape.  Must be at least
        two to produce a meaningful covariance estimate.
    parameters:
        Deprecated placeholder for compatibility with earlier drafts.  If
        supplied it is ignored; keyword arguments should be used instead.
    kwargs:
        Additional keyword arguments forwarded to
        :func:`imaginary_potential_barriers` to customise the fly behaviour.
    """

    if levels < 2:
        raise ValueError("levels must be at least 2 to analyse symmetry.")

    barriers = imaginary_potential_barriers(levels, **kwargs)
    return analyze_complex_symmetry(barriers)


def project_landscape(
    sequence: Sequence[complex], axes: Tuple[PrincipalAxis, PrincipalAxis]
) -> List[float]:
    """Project a complex sequence onto the leading principal axis.

    Returns a list of scalar coordinates representing the trajectory in the
    reduced one-dimensional subspace defined by the dominant axis.  This helps
    visualise how the folding pattern evolves while respecting its inherent
    symmetries.
    """

    leading_axis = axes[0].direction
    projections: List[float] = []
    lx, ly = leading_axis
    for value in sequence:
        projections.append(value.real * lx + value.imag * ly)
    return projections

