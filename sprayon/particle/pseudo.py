"""Construct whimsical spray-on pseudo particles that can "fly" through space."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["PseudoParticle", "spray_on"]


@dataclass(frozen=True)
class PseudoParticle:
    """Representation of an imaginative spray-on particle."""

    surface: str
    thrust: float

    def fly(self) -> str:
        """Describe the particle's flight across the universe."""

        return (
            f"The spray-on pseudo particle launched from {self.surface} "
            f"rides cosmic currents with thrust {self.thrust:.2f}."
        )


def spray_on(surface: str, *, thrust: float = 1.0) -> PseudoParticle:
    """Create a pseudo particle ready to explore the universe."""

    if not isinstance(surface, str) or not surface.strip():
        raise ValueError("surface must be a non-empty string describing the launch point.")

    if not isinstance(thrust, (int, float)):
        raise TypeError("thrust must be a numeric value.")

    if thrust <= 0:
        raise ValueError("thrust must be positive to propel the particle through the universe.")

    return PseudoParticle(surface=surface.strip(), thrust=float(thrust))
