# Calculus Overview

Calculus studies change and accumulation through the twin pillars of **differential calculus** (rates of change) and **integral calculus** (accumulating quantities). Core techniques revolve around limits, derivatives, integrals, and infinite series.

## Limits
- A limit \(\lim_{x \to a} f(x) = L\) means values of \(f(x)\) approach \(L\) as \(x\) approaches \(a\).
- Important patterns: \(\lim_{x \to 0} \frac{\sin x}{x} = 1\) and \(\lim_{x \to \infty} (1 + \tfrac{r}{n})^{n} = e^{r}\).
- Continuity requires the limit to exist and equal the function value at the point.

## Derivatives
- The derivative measures instantaneous rate of change: \(f'(x) = \lim_{h \to 0} \tfrac{f(x+h) - f(x)}{h}\).
- Common rules:
  - Power rule: \(\tfrac{d}{dx} x^{n} = n x^{n-1}\).
  - Product rule: \((fg)' = f'g + fg'\).
  - Chain rule: \(\tfrac{d}{dx} f(g(x)) = f'(g(x)) g'(x)\).
- Applications: tangent lines, velocity/acceleration, optimization via critical points, and modeling growth/decay.

## Integrals
- A definite integral accumulates signed area: \(\int_{a}^{b} f(x)\,dx\).
- Fundamental techniques: substitution, integration by parts, partial fractions, and numerical integration (trapezoidal, Simpson's).
- Improper integrals extend limits of integration to infinities or discontinuities.

## Fundamental Theorem of Calculus (FTC)
- Part 1: If \(F(x) = \int_{a}^{x} f(t)\,dt\) and \(f\) is continuous, then \(F'(x) = f(x)\).
- Part 2: \(\int_{a}^{b} f(x)\,dx = F(b) - F(a)\) for any antiderivative \(F\) of \(f\).

## Series and Convergence
- A series \(\sum_{n=1}^{\infty} a_n\) converges when its partial sums approach a finite limit.
- Tests: comparison, ratio, root, and alternating series tests help determine convergence.
- Taylor series approximate smooth functions near a point: \(f(x) \approx \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!} (x-a)^{n}\).

## Multivariable Calculus Snapshot
- Partial derivatives measure change along individual variables; the gradient \(\nabla f\) points toward steepest ascent.
- Multiple integrals compute volume and mass over regions; change of variables uses Jacobians.
- Vector calculus connects fields and flux through identities like Green's, Stokes', and the Divergence theorems.

## Problem-Solving Tips
- Sketch functions and regions to visualize behavior and domains.
- Track units in applied problems (physics, economics) to catch errors.
- For optimization: check endpoints, critical points, and constraint boundaries.
- Use series expansions for local approximations when derivatives are messy.

## Key Applications
- Physics: motion under forces (kinematics, energy), electromagnetism, and thermodynamics.
- Engineering: signal processing, control systems, and fluid flow.
- Data and finance: gradient-based optimization, probability densities, and continuous compounding.

## Practice Checklist
- Differentiate products, quotients, and composites accurately.
- Evaluate definite integrals with substitution or parts; set up Riemann sums.
- Decide convergence of common series and compute radius of convergence for power series.
- Translate word problems into equations, paying attention to constraints and units.
