"""Simple vertical rocket launch and landing simulation."""

from __future__ import annotations

from dataclasses import dataclass

from typing import Callable


GRAVITY = 9.81  # m / s**2


@dataclass(frozen=True)
class RocketState:
    """Snapshot of a rocket's motion state.

    Parameters
    ----------
    time
        Simulation time stamp in seconds.
    altitude
        Altitude above the launch / landing pad in metres.
    velocity
        Vertical velocity in metres per second (positive upward).
    throttle
        Normalised throttle command between 0 (no thrust) and 1 (maximum thrust).
    """

    time: float
    altitude: float
    velocity: float
    throttle: float


@dataclass(frozen=True)
class RocketSimulationResult:
    """Summary of a rocket launch-to-landing simulation."""

    states: tuple[RocketState, ...]
    landed: bool
    touchdown_velocity: float
    max_altitude: float


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    """Clamp ``value`` within ``[lower, upper]``."""

    return max(lower, min(upper, value))


def _landing_controller(
    altitude: float,
    velocity: float,
    *,
    mass: float,
    max_thrust: float,
    descent_gain: float,
    damping_gain: float,
    max_descent_rate: float,
) -> float:
    """Compute a throttle command that brakes the rocket toward rest at ground level."""

    altitude = max(altitude, 0.0)
    desired_velocity = -min(max_descent_rate, descent_gain * altitude)
    velocity_error = desired_velocity - velocity
    desired_acceleration = velocity_error * damping_gain

    acceleration_command = desired_acceleration + GRAVITY
    throttle = acceleration_command * mass / max_thrust
    return _clamp(throttle)


def simulate_vertical_landing(
    *,
    mass: float = 2000.0,
    max_thrust: float = 45000.0,
    burn_time: float = 20.0,
    controller_activation_altitude: float = 200.0,
    descent_gain: float = 0.3,
    damping_gain: float = 1.2,
    max_descent_rate: float = 60.0,
    dt: float = 0.05,
    max_time: float = 400.0,
    landing_altitude_tolerance: float = 0.5,
    landing_velocity_tolerance: float = 0.5,
    throttle_modifier: Callable[[float, float, float], float] | None = None,
) -> RocketSimulationResult:
    """Launch a single-stage rocket vertically and guide it back to a gentle landing.

    Parameters
    ----------
    mass
        Mass of the rocket in kilograms.
    max_thrust
        Maximum thrust produced by the engine in Newtons.
    burn_time
        Duration (seconds) of the initial ascent burn at full throttle.
    controller_activation_altitude
        Additional altitude margin (metres) added to the stopping distance criterion
        before initiating the landing burn.
    descent_gain
        Gain (1/s) linking altitude to a target downward velocity during landing.
    damping_gain
        Gain converting velocity error to an acceleration command.
    max_descent_rate
        Maximum magnitude (m/s) for the desired downward velocity profile.
    dt
        Simulation timestep in seconds.
    max_time
        Maximum simulated duration in seconds before the routine aborts.
    landing_altitude_tolerance
        Maximum altitude above the pad regarded as a successful landing.
    landing_velocity_tolerance
        Maximum absolute vertical velocity (m/s) regarded as a soft landing.
    throttle_modifier
        Optional callable ``f(time, altitude, velocity)`` returning a throttle
        multiplier in ``[0, 1]``. This may be used to explore thrust limits.

    Returns
    -------
    RocketSimulationResult
        Simulation history and landing outcome summary.
    """

    if burn_time <= 0:
        raise ValueError("burn_time must be positive.")
    if dt <= 0:
        raise ValueError("dt must be positive.")
    if mass <= 0:
        raise ValueError("mass must be positive.")
    if max_thrust <= 0:
        raise ValueError("max_thrust must be positive.")

    time = 0.0
    altitude = 0.0
    velocity = 0.0
    states: list[RocketState] = [RocketState(time, altitude, velocity, throttle=0.0)]
    max_altitude = altitude
    landed = False
    touchdown_velocity = 0.0
    landing_burn_active = False

    upward_acceleration_available = max_thrust / mass - GRAVITY
    if upward_acceleration_available <= 0:
        raise ValueError(
            "The rocket cannot hover; increase max_thrust or reduce mass to allow landing burns.")

    def apply_throttle_modifier(throttle: float) -> float:
        if throttle_modifier is None:
            return throttle
        return _clamp(throttle * _clamp(throttle_modifier(time, altitude, velocity)))

    while time < max_time:
        if time < burn_time:
            throttle = 1.0
        else:
            if not landing_burn_active and velocity < 0.0:
                required_stop_distance = (velocity ** 2) / (
                    2.0 * max(upward_acceleration_available, 1e-6)
                )
                if altitude <= required_stop_distance + controller_activation_altitude:
                    landing_burn_active = True

            if landing_burn_active:
                throttle = _landing_controller(
                    altitude,
                    velocity,
                    mass=mass,
                    max_thrust=max_thrust,
                    descent_gain=descent_gain,
                    damping_gain=damping_gain,
                    max_descent_rate=max_descent_rate,
                )
            else:
                throttle = 0.0

        throttle = apply_throttle_modifier(throttle)

        acceleration = (throttle * max_thrust) / mass - GRAVITY

        prev_altitude = altitude
        prev_velocity = velocity

        velocity = prev_velocity + acceleration * dt
        altitude = prev_altitude + velocity * dt
        next_time = time + dt

        if altitude <= 0.0 and next_time > burn_time:
            # Interpolate touchdown to refine the landing assessment.
            if prev_altitude <= 0.0:
                touchdown_time = next_time
                touchdown_velocity = velocity
            else:
                altitude_drop = prev_altitude - altitude
                if altitude_drop == 0:
                    touchdown_fraction = 1.0
                else:
                    touchdown_fraction = prev_altitude / altitude_drop
                touchdown_time = time + dt * touchdown_fraction
                touchdown_velocity = prev_velocity + acceleration * dt * touchdown_fraction

            altitude_before_touchdown = max(prev_altitude, 0.0)
            max_altitude = max(max_altitude, altitude_before_touchdown)
            landed = (
                altitude_before_touchdown <= landing_altitude_tolerance
                and abs(touchdown_velocity) <= landing_velocity_tolerance
            )
            altitude = 0.0
            velocity = touchdown_velocity
            time = touchdown_time
            states.append(RocketState(time, altitude, velocity, throttle))
            break

        time = next_time
        max_altitude = max(max_altitude, altitude)
        states.append(RocketState(time, altitude, velocity, throttle))

    if not landed:
        raise RuntimeError("Rocket did not achieve a soft landing within the simulation window.")

    return RocketSimulationResult(
        states=tuple(states),
        landed=landed,
        touchdown_velocity=touchdown_velocity,
        max_altitude=max_altitude,
    )


def main() -> None:
    """Run the rocket simulation and print a concise mission report."""

    result = simulate_vertical_landing()
    final_state = result.states[-1]
    print("Rocket launch and landing sequence complete.")
    print(f"Time elapsed: {final_state.time:0.1f} s")
    print(f"Maximum altitude: {result.max_altitude:0.1f} m")
    print(f"Touchdown velocity: {result.touchdown_velocity:0.2f} m/s")
    print(f"Soft landing: {'yes' if result.landed else 'no'}")


if __name__ == "__main__":
    main()
