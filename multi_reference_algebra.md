# Multi-reference Algebra

**Multi-reference algebra** is a practical way to reason about the *same quantity* across multiple reference systems at once.

A “reference” can be any frame you use to describe objects:

- coordinate basis (standard basis, rotated basis)
- unit system (meters vs. feet)
- indexing scheme (0-based vs. 1-based)
- representation domain (time domain vs. frequency domain)

The core idea is simple:

> Keep one underlying mathematical object, but allow many equivalent descriptions linked by explicit transformations.

## 1) Core objects

A compact multi-reference algebra setup usually includes:

- an abstract object space \(\mathcal{X}\) (vectors, functions, tensors, signals)
- a family of reference maps \(R_i: \mathcal{X} \to \mathcal{D}_i\), where each \(\mathcal{D}_i\) is a concrete representation
- conversion maps \(T_{ij}: \mathcal{D}_i \to \mathcal{D}_j\) satisfying
  - \(T_{ii} = I\) (identity)
  - \(T_{jk} \circ T_{ij} = T_{ik}\) (composition consistency)

This guarantees that switching references is coherent.

## 2) Operations and invariants

Given an operation \(\star\) on the abstract space, a good reference system preserves it through commuting diagrams:

\[
R_j(x \star y) = T_{ij}(R_i(x) \star_i R_i(y))
\]

In plain language:

- compute in reference \(i\)
- map to reference \(j\)
- get the same result as computing directly in \(j\)

Quantities unchanged by all valid reference changes are **invariants** (e.g., vector norm under orthonormal basis changes, determinant under similarity-class interpretation, physical laws under unit-consistent scaling).

## 3) Minimal linear example

Let \(x \in \mathbb{R}^n\) be an abstract vector.

- In basis \(B\): coordinates \([x]_B\)
- In basis \(C\): coordinates \([x]_C\)

If \(P_{C\leftarrow B}\) is the change-of-basis matrix,

\[
[x]_C = P_{C\leftarrow B}[x]_B
\]

A linear operator \(A\) transforms as

\[
[A]_C = P_{C\leftarrow B}[A]_B P_{B\leftarrow C}
\]

The operator is the same abstract map; only the reference description changes.

## 4) Why use multi-reference algebra?

- **Numerical stability:** pick a reference that improves conditioning.
- **Interpretability:** pick a reference where structure is obvious.
- **Efficiency:** compute where operations are cheap (e.g., convolution in Fourier space).
- **Interoperability:** translate correctly between teams, tools, or data formats.

## 5) Typical pitfalls

1. Mixing objects from different references without conversion.
2. Forgetting scale factors in unit or normalization changes.
3. Applying transformation matrices in the wrong direction.
4. Assuming a quantity is invariant when it is merely covariant.

## 6) One-line summary

Multi-reference algebra is the discipline of doing algebra with explicit, composable transformations between equivalent representations—so results are correct regardless of viewpoint.
