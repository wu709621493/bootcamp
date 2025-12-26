# Atomic Unit

Atomic units simplify physical calculations by normalizing fundamental constants to 1. They are especially useful in quantum chemistry and atomic physics, where electron behavior dominates system dynamics. Working in atomic units avoids repetitive constants in equations and clarifies how magnitudes compare across systems.

## Core definitions
- **Bohr radius (a0)**: Unit of length, roughly \(5.29 \times 10^{-11}\) meters. In atomic units, \(a_0 = 1\) by definition.
- **Hartree energy (Eh)**: Unit of energy, about \(4.36 \times 10^{-18}\) joules. It sets the scale for electron orbital energies; \(E_h = 1\) in atomic units.
- **Electron mass (me)** and **elementary charge (e)**: Both set to 1 in atomic units, streamlining equations involving kinetic terms and Coulomb interactions.
- **Reduced Planck constant (ℏ)**: Also equals 1, eliminating explicit constants in angular momentum expressions.

## Benefits of using atomic units
1. **Cleaner equations**: Schrödinger’s equation and related operators shed constant factors, making analytic and numerical work more transparent.
2. **Stable numerics**: Values are closer to order-unity, reducing floating-point underflow or overflow in simulation code.
3. **Comparability**: Results from different calculations can be compared without conversion, as long as all parties use the same atomic unit system (usually Hartree atomic units).

## Converting to and from SI
- Multiply distances in atomic units by \(a_0\) to obtain meters.
- Multiply energies in atomic units by \(E_h\) to obtain joules or by 27.2114 to obtain electronvolts.
- Frequencies expressed in atomic units of energy can be converted using \(E = h \nu\), where \(h = 2\pi\hbar\) and \(\hbar = 1\) in atomic units.

## Practical tips
- Always state the unit system at the start of a calculation to avoid ambiguity, especially when mixing data from literature or software packages.
- When coding, keep conversion constants in a single module so that switching between SI and atomic units is safe and auditable.
- For spectroscopy or condensed matter applications, double-check whether authors use Hartree or Rydberg atomic units; the latter scales energies by a factor of 1/2.

Atomic units are not just a convenience—they reflect the natural scales of electrons bound to nuclei, which is why they remain a workhorse for computational chemistry and atomic physics.
