# Two-Layer Bose-Einstein Condensate Model

## Overview
We consider two quasi-2D condensate layers coupled by interlayer tunneling. Each layer hosts a dilute gas of bosons confined by identical in-plane harmonic traps but separated along \(z\) by a barrier that suppresses direct contact interactions across layers. The coupled system is described by two order parameters \(\psi_1(\mathbf{r},t)\) and \(\psi_2(\mathbf{r},t)\) interacting via mean-field contact terms and a Josephson-like tunneling energy \(J\).

## Coupled Gross-Pitaevskii Equations
The dynamics follow
\[
 i\hbar \partial_t \psi_1 = \left[-\frac{\hbar^2}{2m}\nabla^2 + V(r) + g_{11}|\psi_1|^2 + g_{12}|\psi_2|^2 \right]\psi_1 - J\,\psi_2,
\]
\[
 i\hbar \partial_t \psi_2 = \left[-\frac{\hbar^2}{2m}\nabla^2 + V(r) + g_{22}|\psi_2|^2 + g_{21}|\psi_1|^2 \right]\psi_2 - J\,\psi_1.
\]
Here \(V(r)=\tfrac{1}{2}m(\omega_x^2 x^2+\omega_y^2 y^2)\) is the in-plane trap, \(g_{ij}=\sqrt{8\pi}\hbar^2 a_{ij}/(m\ell_z)\) are effective 2D couplings set by scattering lengths \(a_{ij}\) and layer thickness \(\ell_z\), and \(J\) captures tunneling through the barrier. We normalize each field such that \(\int |\psi_i|^2 d^2r = N_i\).

## Dimensionless Form
Rescaling time by \(\omega_\perp^{-1}\), length by \(a_\perp=\sqrt{\hbar/(m\omega_\perp)}\), and wavefunctions by \(\sqrt{N}/a_\perp\), we obtain
\[
 i \partial_\tau \phi_1 = \left[-\tfrac{1}{2}\nabla^2 + \tfrac{1}{2}(\lambda_x^2 x^2 + \lambda_y^2 y^2) + u_{11}|\phi_1|^2 + u_{12}|\phi_2|^2\right]\phi_1 - k\,\phi_2,
\]
\[
 i \partial_\tau \phi_2 = \left[-\tfrac{1}{2}\nabla^2 + \tfrac{1}{2}(\lambda_x^2 x^2 + \lambda_y^2 y^2) + u_{22}|\phi_2|^2 + u_{21}|\phi_1|^2\right]\phi_2 - k\,\phi_1,
\]
with \(k=J/\hbar\omega_\perp\) and \(u_{ij}=g_{ij}N/(\hbar\omega_\perp a_\perp^2)\).

## Parameter Choices for a Trial Run
* **Species**: \(^{87}\mathrm{Rb}\) with \(a_{11}=a_{22}=100\,a_0\), \(a_{12}=95\,a_0\); atom number per layer \(N_1=N_2=2\times10^4\).
* **Trap**: \(\omega_x=2\pi\times50\,\mathrm{Hz}\), \(\omega_y=2\pi\times60\,\mathrm{Hz}\); layer separation \(d=1.5\,\mu\mathrm{m}\), axial confinement \(\omega_z=2\pi\times3\,\mathrm{kHz}\) giving \(\ell_z\approx0.2\,\mu\mathrm{m}\).
* **Tunneling**: \(J/h\approx5\,\mathrm{Hz}\) (adjust barrier height to scan \(k\in[0,0.2]\)).
* **Temperature**: Start at \(T<50\,\mathrm{nK}\) to maintain condensate fraction >80%.

## Numerical Experiment Outline
1. **Ground state**: Use imaginary-time propagation on both fields with shared chemical potential until convergence of energy and overlap between successive steps (<1e-6 relative change).
2. **Population imbalance**: Impose an initial phase difference \(\Delta\varphi\) or number difference \(\Delta N/N\approx0.1\) to seed Josephson oscillations.
3. **Dynamical evolution**: Propagate real time using split-step Fourier with time step \(\Delta\tau\approx10^{-3}\) and grid resolving \(\xi=\hbar/\sqrt{2mgn}\) to capture healing length physics.
4. **Observables**:
   * Population dynamics: \(z(t)=(N_1-N_2)/(N_1+N_2)\), phase difference \(\Delta\varphi(t)\).
   * Phase-coherence: fringe contrast after time-of-flight expansion.
   * Vortex dynamics: track phase singularities per layer to identify vortex-pair nucleation when \(k\) competes with interactions.
5. **Scan variables**: vary \(k\), \(a_{12}\), and trap anisotropy to map regimes of Josephson plasma oscillations vs. macroscopic self-trapping.

## Expected Outcomes
* For weak coupling (\(k\lesssim0.02\)), nonlinear interactions dominate and macroscopic self-trapping appears when \(z(0)\) or \(\Delta\varphi\) exceeds critical values predicted by the two-mode model.
* For intermediate \(k\), coherent Josephson oscillations of population and phase persist with frequency \(\omega_J\approx\sqrt{2k(2k+u)}/\hbar\), modulated by trap anisotropy.
* At strong coupling and near miscibility, phase locking suppresses vortex nucleation; reducing \(a_{12}\) or increasing \(d\) should restore layer-specific vortices and domain-wall excitations.

## Diagnostic Extensions
* **Noise seeding**: Add small-amplitude complex noise to \(\psi_{1,2}\) before real-time evolution to study spontaneous symmetry breaking and domain patterns.
* **Finite temperature**: Couple to a stochastic Gross-Pitaevskii term with damping \(\gamma\sim10^{-3}\) to model thermal cloud effects on interlayer coherence.
* **Spinor generalization**: Promote each layer to a two-component spinor and include spin-dependent scattering lengths to explore coupled spin-charge Josephson dynamics.
