"""Helpers for simple rotational dynamics calculations."""

from __future__ import annotations


def _validate_positive(value: float, name: str) -> float:
    """Ensure ``value`` is positive.

    Parameters
    ----------
    value
        Numeric quantity to check.
    name
        Parameter name for error messages.

    Returns
    -------
    float
        The validated value as a float.

    Raises
    ------
    ValueError
        If ``value`` is not strictly positive.
    """

    value = float(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive; got {value!r}.")
    return value


def _validate_non_negative(value: float, name: str) -> float:
    """Ensure ``value`` is non-negative, returning it as a float."""

    value = float(value)
    if value < 0:
        raise ValueError(f"{name} must be non-negative; got {value!r}.")
    return value


def angular_momentum(moment_of_inertia: float, angular_velocity: float) -> float:
    """Return angular momentum for a spinning body.

    Parameters
    ----------
    moment_of_inertia
        Resistance to rotational acceleration. Must be positive.
    angular_velocity
        Current angular velocity.
    """

    inertia = _validate_positive(moment_of_inertia, "moment_of_inertia")
    return inertia * float(angular_velocity)


def rotational_energy(moment_of_inertia: float, angular_velocity: float) -> float:
    """Return the kinetic energy of rotation."""

    inertia = _validate_positive(moment_of_inertia, "moment_of_inertia")
    omega = float(angular_velocity)
    return 0.5 * inertia * omega**2


def spin_up(
    initial_omega: float,
    torque: float,
    moment_of_inertia: float,
    duration: float,
) -> float:
    """Return the final angular velocity after applying constant ``torque``.

    The update assumes the torque is applied for the entire ``duration``.
    ``duration`` must be non-negative, and ``moment_of_inertia`` must be
    positive. Units are left to the caller but must be consistent.
    """

    inertia = _validate_positive(moment_of_inertia, "moment_of_inertia")
    delta_t = _validate_non_negative(duration, "duration")

    alpha = float(torque) / inertia
    return float(initial_omega) + alpha * delta_t
