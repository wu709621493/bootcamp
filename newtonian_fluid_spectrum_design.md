# Newtonian Fluid Spectrum Design

## Purpose
Design a compact, teachable spectrum that places everyday Newtonian fluids along a continuum of viscosity and temperature, showing how density, viscosity, and flow regime interact. The spectrum is meant for quick selection of working fluids in laboratory, art, and industrial prototypes.

## Spectrum Axes
- **Primary axis: dynamic viscosity (μ)** measured in Pa·s, spanning water-like to syrup-like Newtonian fluids.
- **Secondary axis: operational temperature (T)** in °C, because viscosity varies strongly with temperature.
- **Overlay: density (ρ)** in kg/m³ to anticipate inertia vs. gravity effects.
- **Overlay: typical Reynolds number (Re)** ranges for a reference tube flow or stirring setup.

## Reference Conditions
- **Reference geometry**: 10 mm diameter tube, 0.2 m/s mean velocity.
- **Re formula**: Re = ρVD/μ.
- **Reference temperature**: 20 °C unless stated.

## Spectrum Bands
1. **Low viscosity (μ: 0.3–2 mPa·s)**
   - Examples: water (1 mPa·s), acetone, light alcohols.
   - Behavior: turbulent at modest velocities, high diffusion of momentum.
   - Use cases: heat transfer loops, rinsing, fast mixing.

2. **Medium viscosity (μ: 2–20 mPa·s)**
   - Examples: light oils, glycerol-water blends (10–30% glycerol).
   - Behavior: transition region in small channels; laminar in microfluidics.
   - Use cases: controlled laminar experiments, lubrication.

3. **High viscosity (μ: 20–200 mPa·s)**
   - Examples: heavy oils, pure glycerol (~1,500 mPa·s at 20 °C but can be lowered with heat).
   - Behavior: laminar for most lab-scale geometries; strong temperature sensitivity.
   - Use cases: damping, slow flow visualization, low-Re experiments.

4. **Very high viscosity (μ: 0.2–2 Pa·s)**
   - Examples: corn syrup, honey (variable by moisture).
   - Behavior: creeping flow; stratification depends strongly on density differences.
   - Use cases: sedimentation demonstrations, slow dynamics.

5. **Ultra high viscosity (μ: 2–20 Pa·s)**
   - Examples: silicone oils (high viscosity grades), pitch-like fluids (if Newtonian over small shear rates).
   - Behavior: quasi-static flow; inertia negligible.
   - Use cases: time-scale stretching for visualizations and education.

## Temperature Mapping
Viscosity drops roughly exponentially with temperature for most Newtonian liquids. Design the spectrum with temperature “rails”:
- **Cold rail (0–5 °C)**: shifts fluids one band higher (more viscous).
- **Ambient rail (20–25 °C)**: base mapping.
- **Warm rail (40–60 °C)**: shifts fluids one band lower (less viscous).

## Selection Procedure
1. Choose target Re for your experiment.
2. Fix geometry and flow rate (or mixing speed).
3. Pick density range (e.g., 800–1,200 kg/m³).
4. Read viscosity from the band that delivers the target Re.
5. Adjust temperature to fine-tune within the band.

## Example Mapping (20 °C)
| Fluid | μ (mPa·s) | ρ (kg/m³) | Re (ref) | Band |
| --- | --- | --- | --- | --- |
| Water | 1 | 998 | ~2,000 | Low |
| Ethanol | 1.2 | 789 | ~1,300 | Low |
| Light mineral oil | 10 | 850 | ~170 | Medium |
| Glycerol (50%) | 6 | 1,130 | ~380 | Medium |
| Glycerol (100%) | 1,500 | 1,260 | ~1.7 | Very high |
| Corn syrup | 2,000 | 1,350 | ~1 | Very high |

## Design Notes
- Keep the spectrum Newtonian by avoiding shear-thinning or viscoelastic fluids (e.g., polymer solutions, ketchup).
- Specify the measurement method (capillary viscometer, rotational viscometer) to avoid confusion.
- The spectrum is a practical heuristic, not a substitute for measured data.

## Deliverables
- Poster-sized chart with color-banded viscosity zones.
- A small lookup card listing common fluids and their viscosity at 20 °C and 40 °C.
- A spreadsheet that recalculates Re for different geometries.
