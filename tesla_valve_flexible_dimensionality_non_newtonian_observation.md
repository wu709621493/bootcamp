# Tesla Valve with Flexible Dimensionality for Non-Newtonian Fluid Parameter Observation

## Purpose
Design a Tesla-valve-based experimental platform that can switch between quasi-1D, 2D, and 3D flow dominance to observe non-Newtonian parameters (shear-thinning, yield stress, viscoelastic relaxation, thixotropy) using a single modular test article.

## Concept Summary
A classical Tesla valve is a no-moving-parts check-valve geometry that creates directional asymmetry in pressure drop. By embedding scalable branch loops and variable depth layers, the same platform can emulate:
- **1D-like channel flow** (depth-constrained, negligible cross-stream effects),
- **2D planar recirculation flow** (moderate depth, visible vortical structures),
- **3D secondary-flow-rich behavior** (stacked or deep channels with vertical transport).

This **flexible dimensionality** enables parameter identification under multiple stress histories without changing pump infrastructure.

## Why Tesla Valve Geometry Helps
- **Directional pressure-loss asymmetry** creates natural loading/unloading paths useful for hysteresis measurement.
- **Recirculation pockets and branch junctions** amplify shear-rate gradients, improving sensitivity to shear-dependent viscosity.
- **Pulsatile compatibility** allows extraction of viscoelastic phase lag from periodic forcing.
- **No active parts** reduces confounding mechanical compliance.

## Modular Architecture
1. **Base manifold**
   - Inlet plenum, outlet plenum, flow straightener, pressure tap rails.
2. **Interchangeable Tesla cartridges**
   - Same footprint, varied channel depth and branch angle.
3. **Dimensionality inserts**
   - **D1 insert**: shallow ceiling spacer to enforce quasi-1D behavior.
   - **D2 insert**: nominal depth for planar flow visualization.
   - **D3 insert**: deep or multilayer spacer for out-of-plane transport.
4. **Sensing layer**
   - Differential pressure sensors across each stage.
   - Optional inline Coriolis or gravimetric flow validation.
   - Optical window for particle image velocimetry (PIV) or dye streaks.

## Parameter Observation Targets
### 1) Shear-thinning / shear-thickening index
Use generalized power-law form:
\[
\mu_{app} = K\,\dot\gamma^{n-1}
\]
- Estimate **n** from pressure-drop vs flow-rate sweeps in forward/reverse directions.
- Use D1 mode first for robust bulk fitting, then D2/D3 for geometry-coupled refinement.

### 2) Yield stress (Bingham / Herschel-Bulkley behavior)
\[
\tau = \tau_y + K\dot\gamma^n
\]
- Identify onset flow condition (critical pressure) where stagnant pockets begin to mobilize.
- Tesla side loops provide spatially distributed yielding thresholds.

### 3) Viscoelastic relaxation time
- Apply sinusoidal or square-wave flow excitation.
- Measure phase lag between inlet flow waveform and stage pressure response.
- Fit relaxation spectrum (single-mode or multi-mode approximation).

### 4) Thixotropy and structural rebuild
- Run high-shear conditioning in reverse direction.
- Pause or reduce shear in forward direction.
- Track time-dependent pressure recovery at fixed flow.

## Flexible Dimensionality Protocol
1. **Calibration (Newtonian reference)**
   - Run water/glycerol standards to derive hydraulic baseline by mode (D1, D2, D3).
2. **D1 mode identification**
   - Fit first-pass rheology with minimal geometric complexity.
3. **D2 mode enrichment**
   - Add recirculation-sensitive metrics (vortex residence, branch activation).
4. **D3 mode validation**
   - Confirm parameter portability under out-of-plane flow structures.
5. **Cross-mode consistency check**
   - Accept parameter set only if prediction error stays below tolerance across all modes.

## Recommended Measured Outputs
- Stage-wise pressure drop \(\Delta P_i\)
- Total pressure drop \(\Delta P_{tot}\)
- Forward/reverse diodicity ratio
  \[
  Di = \frac{\Delta P_{reverse}}{\Delta P_{forward}}\bigg|_{Q}
  \]
- Flow-rate waveform and harmonic content
- Optional image-derived metrics: recirculation area fraction, interface curvature, vortex persistence

## Data Reduction Workflow
1. Preprocess sensor drift and temperature correction.
2. Compute apparent hydraulic resistance for each stage and direction.
3. Perform global optimization of rheological parameters using all dimensionality modes jointly.
4. Report parameter covariance and mode-specific residuals.
5. Flag non-identifiable parameters where sensitivity matrix is rank-deficient.

## Design Envelope (Example Starting Point)
- Channel width: 0.8–2.0 mm
- Depth options: 0.15 mm (D1), 0.8 mm (D2), 2.5 mm or dual-layer (D3)
- Tesla stage count: 6–12
- Working flow rate: 0.1–20 mL/min (microfluidic scale)
- Pressure range: up to 200 kPa differential

## Practical Notes
- Keep Reynolds number in range appropriate for targeted rheology regime; inertial effects can mask constitutive behavior.
- Use temperature control (±0.2 °C) because many non-Newtonian fluids are thermo-sensitive.
- For opaque fluids, rely on pressure-only identification plus occasional transparent analog calibration.
- If wall slip is likely, include surface treatments or roughness-controlled cartridges.

## Deliverables
- CAD set of the base manifold and three dimensionality inserts.
- Test matrix defining forward/reverse steady and pulsatile runs.
- Parameter estimation notebook (with uncertainty quantification).
- Comparative report: single-mode vs multi-mode identification performance.
