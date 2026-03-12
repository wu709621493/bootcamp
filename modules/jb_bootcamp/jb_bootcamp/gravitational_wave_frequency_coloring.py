"""Frequency blinking + real-time frequency coloring for gravitational-wave signals."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

__all__ = [
    "FrequencyBlinkConfig",
    "FrequencyColoringResult",
    "simulate_gravitational_wave_strain",
    "apply_frequency_blinking_coloring",
    "save_frequency_coloring_figure",
    "summarize_top_frequency_events",
]


@dataclass(frozen=True)
class FrequencyBlinkConfig:
    """Configuration for STFT, blink, and coloring settings."""

    sample_rate_hz: float = 4096.0
    window_size: int = 512
    overlap: float = 0.75
    smoothing_lambda: float = 0.85
    db_min: float = -120.0
    db_max: float = -30.0
    blink_base_rate_hz: float = 2.0
    blink_alpha: float = 80.0
    blink_beta: float = 0.65
    duty_base: float = 0.35
    duty_gamma: float = 2.5


@dataclass(frozen=True)
class FrequencyColoringResult:
    """Container for derived frequency-coloring channels."""

    times: np.ndarray
    frequencies_hz: np.ndarray
    amplitude: np.ndarray
    delta_amplitude: np.ndarray
    phase_velocity: np.ndarray
    saturation: np.ndarray
    value: np.ndarray
    blink_gate: np.ndarray
    intensity: np.ndarray
    rgb: np.ndarray


def simulate_gravitational_wave_strain(
    duration_s: float = 4.0,
    sample_rate_hz: float = 4096.0,
    chirp_start_hz: float = 30.0,
    chirp_end_hz: float = 320.0,
    seed: int = 7,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a simple inspiral-like chirp strain series with detector-like noise."""

    rng = np.random.default_rng(seed)
    n_samples = int(duration_s * sample_rate_hz)
    times = np.arange(n_samples, dtype=float) / sample_rate_hz

    ramp = np.clip(times / duration_s, 0.0, 1.0)
    instantaneous_frequency = chirp_start_hz + (chirp_end_hz - chirp_start_hz) * ramp**3
    phase = 2.0 * np.pi * np.cumsum(instantaneous_frequency) / sample_rate_hz

    envelope = 0.08 * ramp**2
    chirp = envelope * np.sin(phase)

    white = rng.normal(0.0, 0.015, size=n_samples)
    coloring = np.convolve(white, np.ones(16) / 16.0, mode="same")
    strain = chirp + coloring

    return times, strain


def apply_frequency_blinking_coloring(
    strain: np.ndarray,
    config: FrequencyBlinkConfig,
) -> FrequencyColoringResult:
    """Apply the frequency blinking + coloring pipeline on a strain signal."""

    hop_size = max(1, int(config.window_size * (1.0 - config.overlap)))
    window = np.hanning(config.window_size)

    frames: list[np.ndarray] = []
    frame_times: list[float] = []
    for start in range(0, len(strain) - config.window_size + 1, hop_size):
        chunk = strain[start : start + config.window_size] * window
        frames.append(np.fft.rfft(chunk))
        frame_times.append((start + config.window_size / 2.0) / config.sample_rate_hz)

    stft = np.asarray(frames)
    amplitude = np.abs(stft)
    phase = np.angle(stft)

    smoothed_amplitude = np.zeros_like(amplitude)
    smoothed_amplitude[0] = amplitude[0]
    for i in range(1, amplitude.shape[0]):
        smoothed_amplitude[i] = (
            config.smoothing_lambda * smoothed_amplitude[i - 1]
            + (1.0 - config.smoothing_lambda) * amplitude[i]
        )

    delta_amplitude = np.zeros_like(amplitude)
    delta_amplitude[1:] = np.diff(smoothed_amplitude, axis=0)

    phase_unwrapped = np.unwrap(phase, axis=0)
    delta_phase = np.zeros_like(phase_unwrapped)
    delta_phase[1:] = np.diff(phase_unwrapped, axis=0)
    delta_t = hop_size / config.sample_rate_hz
    phase_velocity = delta_phase / max(delta_t, np.finfo(float).eps)

    amplitude_db = 20.0 * np.log10(amplitude + 1e-12)
    value = np.clip(
        (amplitude_db - config.db_min) / (config.db_max - config.db_min),
        0.0,
        1.0,
    )

    noise_floor = np.percentile(amplitude, 20, axis=0, keepdims=True) + 1e-9
    snr = amplitude / noise_floor
    saturation = np.clip((snr - 1.0) / 10.0, 0.0, 1.0)

    delta_norm = np.abs(delta_amplitude)
    scale = np.percentile(delta_norm, 95) + 1e-12
    delta_norm = np.clip(delta_norm / scale, 0.0, 1.0)

    blink_rate = config.blink_base_rate_hz + config.blink_alpha * delta_norm
    duty = np.clip(config.duty_base + config.duty_gamma * delta_norm, 0.05, 0.95)

    t = np.asarray(frame_times)[:, None]
    phase_cycle = (t * blink_rate) % 1.0
    blink_gate = (phase_cycle < duty).astype(float)
    intensity = value * (1.0 - config.blink_beta + config.blink_beta * blink_gate)

    nyquist = config.sample_rate_hz / 2.0
    frequencies_hz = np.fft.rfftfreq(config.window_size, d=1.0 / config.sample_rate_hz)
    hue = np.clip(frequencies_hz / nyquist, 0.0, 1.0)[None, :]

    hsv = np.stack([np.broadcast_to(hue, intensity.shape), saturation, intensity], axis=-1)
    rgb = _hsv_to_rgb(hsv)

    return FrequencyColoringResult(
        times=np.asarray(frame_times),
        frequencies_hz=frequencies_hz,
        amplitude=amplitude,
        delta_amplitude=delta_amplitude,
        phase_velocity=phase_velocity,
        saturation=saturation,
        value=value,
        blink_gate=blink_gate,
        intensity=intensity,
        rgb=rgb,
    )


def summarize_top_frequency_events(
    result: FrequencyColoringResult,
    top_n: int = 6,
) -> tuple[dict[str, float], ...]:
    """Return the strongest dynamic frequency events based on blink intensity."""

    event_score = np.abs(result.delta_amplitude) * result.intensity
    flat_indices = np.argpartition(event_score.ravel(), -top_n)[-top_n:]
    ordered = flat_indices[np.argsort(event_score.ravel()[flat_indices])[::-1]]

    n_bins = event_score.shape[1]
    rows = []
    for flat in ordered:
        frame, freq_idx = divmod(int(flat), n_bins)
        rows.append(
            {
                "time_s": float(result.times[frame]),
                "frequency_hz": float(result.frequencies_hz[freq_idx]),
                "event_score": float(event_score[frame, freq_idx]),
                "intensity": float(result.intensity[frame, freq_idx]),
            }
        )

    return tuple(rows)


def save_frequency_coloring_figure(
    result: FrequencyColoringResult,
    output_path: str | Path,
) -> Path:
    """Persist a simple RGB image showing blink gate and frequency coloring."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    blink = np.repeat(result.blink_gate[..., None], 3, axis=-1)
    colored = np.clip(result.rgb, 0.0, 1.0)

    blink_img = np.flipud(np.swapaxes(blink, 0, 1))
    color_img = np.flipud(np.swapaxes(colored, 0, 1))

    separator = np.ones((8, color_img.shape[1], 3), dtype=float) * 0.2
    stacked = np.vstack([blink_img, separator, color_img])
    rgb8 = np.clip(stacked * 255.0, 0, 255).astype(np.uint8)

    _write_ppm(output, rgb8)
    return output


def _write_ppm(path: Path, rgb8: np.ndarray) -> None:
    """Write an 8-bit RGB image as binary PPM (P6)."""

    if rgb8.ndim != 3 or rgb8.shape[2] != 3:
        raise ValueError("rgb8 must be an array with shape (height, width, 3).")

    header = f"P6\n{rgb8.shape[1]} {rgb8.shape[0]}\n255\n".encode("ascii")
    with path.open("wb") as handle:
        handle.write(header)
        handle.write(rgb8.tobytes())


def _hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    """Vectorised HSV-to-RGB conversion for arrays in [0, 1]."""

    h = hsv[..., 0]
    s = hsv[..., 1]
    v = hsv[..., 2]

    i = np.floor(h * 6.0).astype(int)
    f = h * 6.0 - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)

    i_mod = i % 6
    rgb = np.zeros_like(hsv)

    choices = [
        np.stack([v, t, p], axis=-1),
        np.stack([q, v, p], axis=-1),
        np.stack([p, v, t], axis=-1),
        np.stack([p, q, v], axis=-1),
        np.stack([t, p, v], axis=-1),
        np.stack([v, p, q], axis=-1),
    ]

    for idx, choice in enumerate(choices):
        rgb[i_mod == idx] = choice[i_mod == idx]

    return rgb
