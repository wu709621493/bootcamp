# Applying Frequency Blinking + Real-Time Frequency Coloring to Gravitational-Wave Data

This document applies the method in
`frequency_blinking_real_time_frequency_coloring_for_fourier_transform_operation.md`
to gravitational-wave style strain data.

## What was applied

The implementation follows the requested pipeline:

1. Simulate detector strain with an inspiral-like chirp + colored noise.
2. Run STFT (Hann window, 75% overlap).
3. Compute per-bin features (`A`, `ΔA`, phase velocity).
4. Build visual channels:
   - Hue from frequency,
   - Saturation from SNR-like confidence,
   - Value from log-amplitude,
   - Blink gate from `|ΔA|` (dynamic bins pulse more).
5. Render combined blink + RGB frequency map.

## Run

```bash
python apply_frequency_coloring_to_gravitational_wave.py
```

## Sample output (from this repo run)

- Saved visualization: `artifacts/gravitational_wave_frequency_coloring.ppm`
- Top dynamic events cluster near late-time high-frequency bins:
  - around `t ≈ 3.72–3.91 s`
  - around `f ≈ 264–304 Hz`

This behavior matches the expected inspiral chirp trend where frequency and amplitude ramp up toward merger.
