"""Run frequency blinking + coloring on simulated gravitational-wave strain."""

from pathlib import Path

from modules.jb_bootcamp.jb_bootcamp.gravitational_wave_frequency_coloring import (
    FrequencyBlinkConfig,
    apply_frequency_blinking_coloring,
    save_frequency_coloring_figure,
    simulate_gravitational_wave_strain,
    summarize_top_frequency_events,
)


def main() -> None:
    config = FrequencyBlinkConfig()
    _, strain = simulate_gravitational_wave_strain(sample_rate_hz=config.sample_rate_hz)
    result = apply_frequency_blinking_coloring(strain, config)

    output = save_frequency_coloring_figure(
        result, Path("artifacts/gravitational_wave_frequency_coloring.ppm")
    )
    events = summarize_top_frequency_events(result, top_n=6)

    print(f"Saved visualization to: {output}")
    print("Top dynamic events:")
    for i, event in enumerate(events, 1):
        print(
            f"{i}. t={event['time_s']:.3f}s, "
            f"f={event['frequency_hz']:.1f}Hz, "
            f"score={event['event_score']:.5f}, "
            f"I={event['intensity']:.3f}"
        )


if __name__ == "__main__":
    main()
