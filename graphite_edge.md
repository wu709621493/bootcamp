# Graphite Edge

Graphite Edge is a conceptual platform for modular carbon-based composites that combine the lightness of graphene sheets with the machinability of graphite. The intent is to produce panels, struts, and conductive layers that can be fabricated with standard CNC workflows while retaining exceptional thermal stability and strength-to-weight ratios.

## Material architecture
- **Layered hybrid stack:** Alternating graphene-rich films and resin-infused graphite fibers create anisotropic strength, allowing edges to be milled without fraying.
- **Thermal vias:** Embedded boron nitride microtubes conduct heat laterally, giving the composite an edge-cooled profile suitable for electronics enclosures and drone airframes.
- **Surface tuning:** Plasma treatments add hydrophobic or hydrophilic finishes, while vapor-deposited metals provide selective conductivity for antennas or grounding grids.

## Manufacturing approach
- Start from roll-to-roll graphene-coated foil, stack with graphite fiber mats, and cure under low-pressure autoclave cycles to minimize voids.
- Use waterjet pre-cuts for internal cavities, then finish with diamond-coated end mills; the composite’s graphite shell tolerates standard cutting fluids.
- Integrate recycled graphite powder into the resin to lower cost and boost machinability without compromising tensile performance.

## Application sketches
- **Aerospace brackets:** Edge-cooled mounts that dissipate heat from avionics boards while holding tight tolerances after repeated thermal cycling.
- **Battery housings:** Rigid shells that wick heat to external fins, reducing hot spots in high-density battery arrays.
- **RF panels:** Conformal structures with selective metallization for antennas on small satellites or high-altitude platforms.

## Validation checkpoints
- Characterize flexural modulus and interlaminar shear strength against aluminum 6061-T6 benchmarks.
- Run thermal shock tests from −50°C to 120°C to verify edge integrity after CNC finishing.
- Evaluate EMI shielding effectiveness before and after plasma surface treatments.

## Roadmap
1. Prototype 300 mm × 300 mm panels with three layup variations and document machinability metrics.
2. Build finite element models for bracket geometries, incorporating orthotropic properties from coupon testing.
3. Partner with a CNC shop to validate tool wear, chip evacuation, and tolerance retention over a 50-part run.
4. Package findings into an open data set with fabrication parameters, test rigs, and recommended workflows.
