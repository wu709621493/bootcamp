# Polynomial Time Complexity

Polynomial time describes algorithms whose running time grows no faster than a polynomial function of the input size \(n\). This means there exists a constant \(k\) such that the worst-case runtime can be bounded by \(O(n^k)\).

## Why it matters
- **Predictable growth:** Polynomial functions increase more slowly than exponential functions, so algorithms in polynomial time generally remain practical as input sizes scale.
- **Complexity classes:** The class **P** contains decision problems solvable in deterministic polynomial time; **NP** contains problems verifiable in polynomial time. Whether P = NP is a central open question in computer science.

## Common polynomial-time runtimes
- **Linear:** \(O(n)\) – scanning a list to find its maximum.
- **Log-linear:** \(O(n \log n)\) – efficient sorting algorithms like mergesort.
- **Quadratic:** \(O(n^2)\) – simple graph algorithms like checking all pairs of vertices for an edge.

## Comparing to exponential time
Exponential-time algorithms (e.g., \(O(2^n)\)) become infeasible even for moderate \(n\). If a problem admits a polynomial-time algorithm, it is generally considered efficiently solvable, while exponential-time solutions are typically impractical except for very small inputs.
