# Math Depicts Physics: An Entry-Level Calculus Textbook

## Preface
Calculus is the language of change, and physics is the science of change in the physical world. This textbook introduces limits, derivatives, and integrals through everyday physical ideas: motion, force, energy, and accumulation.

---

## Chapter 1: Why Calculus?
### 1.1 From Arithmetic to Change
- Arithmetic describes totals.
- Algebra describes relationships.
- Calculus describes how relationships change.

### 1.2 Physics Questions That Need Calculus
- How fast is an object moving *right now*?
- How far has it traveled after a changing speed?
- How does force relate to changing motion?

### 1.3 Mathematical Toolkit Review
- Real numbers, variables, and functions
- Coordinate plane and graph reading
- Exponents and basic trigonometric functions

**Checkpoint problems**
1. Sketch the graph of position vs. time for a person walking, stopping, then walking faster.
2. Explain in words the difference between average speed and instantaneous speed.

---

## Chapter 2: Functions and Models
### 2.1 Functions as Input-Output Machines
A function assigns one output to each input. In physics, examples include:
- Position: \(x(t)\)
- Velocity: \(v(t)\)
- Temperature: \(T(t)\)

### 2.2 Common Function Types
- Linear: constant rate changes
- Quadratic: uniformly accelerated motion
- Exponential: growth/decay
- Trigonometric: periodic motion

### 2.3 Dimensional Meaning
Always attach units:
- \(x\): meters
- \(t\): seconds
- \(v\): meters/second

**Physics connection**
If \(x(t)=3t^2\), then as time increases, position grows faster and faster—suggesting acceleration.

---

## Chapter 3: Limits — Approaching Without Reaching
### 3.1 Idea of a Limit
A limit asks what value a function approaches as input approaches some point.

\[
\lim_{t\to 2} x(t)
\]

### 3.2 Graphical and Numerical Limits
- Read behavior from a graph near a point.
- Build value tables approaching from left and right.

### 3.3 Continuity and Physical Realism
Continuous models fit many physical systems where sudden jumps are unlikely.

### 3.4 Infinite Limits and Asymptotes
Useful in extreme behavior models (e.g., idealized forces at short distance).

**Checkpoint problems**
1. Estimate \(\lim_{t\to 1} \frac{t^2-1}{t-1}\) from a table.
2. Determine where a given graph is not continuous.

---

## Chapter 4: Derivatives — Instantaneous Change
### 4.1 From Average to Instantaneous Rate
Average velocity on \([t, t+h]\):
\[
\frac{x(t+h)-x(t)}{h}
\]
Derivative (instantaneous velocity):
\[
v(t)=x'(t)=\lim_{h\to 0}\frac{x(t+h)-x(t)}{h}
\]

### 4.2 Geometric Meaning
The derivative is the slope of the tangent line.

### 4.3 Basic Rules
- Power rule
- Constant multiple and sum rules
- Product and quotient rules
- Chain rule

### 4.4 Physics Meanings
- \(x'(t)=v(t)\): velocity
- \(v'(t)=a(t)\): acceleration
- If \(F=ma\), then force drives derivative changes in velocity.

**Worked example**
If \(x(t)=5t^2+2t\), then
\[
v(t)=10t+2,\quad a(t)=10
\]
Constant acceleration model.

---

## Chapter 5: Applications of Derivatives in Physics
### 5.1 Motion Analysis
- Increasing/decreasing position
- Turning points (when \(v=0\))

### 5.2 Optimization
Minimize travel time, maximize projectile range (under model assumptions).

### 5.3 Related Rates
How fast does one physical quantity change when another changes?

### 5.4 Linear Approximation
Near a point:
\[
f(x)\approx f(a)+f'(a)(x-a)
\]
Useful in measurement and small-error physics approximations.

---

## Chapter 6: Integrals — Accumulation and Area
### 6.1 Area as Accumulated Quantity
The integral adds infinitely many tiny pieces.

### 6.2 Riemann Sums
Approximate area or accumulation with rectangles:
\[
\sum f(x_i^*)\Delta x
\]

### 6.3 Definite Integral
\[
\int_a^b f(x)\,dx
\]
Represents net accumulation from \(a\) to \(b\).

### 6.4 Physical Interpretations
- Area under velocity-time curve = displacement
- Area under acceleration-time curve = change in velocity

---

## Chapter 7: Fundamental Theorem of Calculus
### 7.1 Part I
If
\[
F(x)=\int_a^x f(t)\,dt,
\]
then
\[
F'(x)=f(x).
\]

### 7.2 Part II
\[
\int_a^b f(x)\,dx=F(b)-F(a)
\]
where \(F' = f\).

### 7.3 Big Picture
Derivatives and integrals are inverse processes:
- Differentiate to find instantaneous change.
- Integrate to recover accumulated total.

---

## Chapter 8: Antiderivatives and Techniques
### 8.1 Basic Antiderivatives
- \(\int x^n dx = \frac{x^{n+1}}{n+1}+C\) for \(n\neq -1\)
- \(\int \cos x\,dx=\sin x + C\)

### 8.2 Substitution (u-sub)
Reverse chain rule for composite functions.

### 8.3 Initial Value Problems in Physics
Given acceleration and initial velocity, recover velocity and position by integration.

---

## Chapter 9: First-Order Differential Equations (Preview)
### 9.1 Why Differential Equations?
Many laws of physics are naturally written using derivatives.

### 9.2 Exponential Decay Example
\[
\frac{dN}{dt}=-kN
\]
Solution:
\[
N(t)=N_0e^{-kt}
\]
Used in cooling, radioactive decay, and damping models.

---

## Chapter 10: Modeling Projects
1. **Free-fall model** with constant gravitational acceleration.
2. **Braking distance model** from velocity and deceleration.
3. **Spring oscillation model** using sine/cosine behavior.
4. **Energy and work** using force-position integrals.

Each project includes:
- Assumptions
- Variables and units
- Derivation
- Interpretation limits

---

## Appendix A: Formula Sheet
- Derivative rules
- Integral rules
- Trigonometric identities
- Common physical constants and unit conversions

## Appendix B: Study Strategy
- Draw graphs before computing.
- Write units at every step.
- Explain results in words after solving.
- Check if answers are physically reasonable.

## Appendix C: Suggested Problem Set Structure
- Concept checks
- Computation drills
- Mixed word problems
- Model critique questions

---

## Closing Note
Mathematics does not replace physics; it clarifies it. Physics supplies meaning, experiments, and constraints, while calculus provides precision and predictive power. When studied together, they reveal how the world changes—and why.
