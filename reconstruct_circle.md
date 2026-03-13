# Reconstruct Circle

To **reconstruct a circle**, you only need enough constraints to recover its center and radius.

## Minimal geometric constructions

- **Center + radius**: If the center point \(O\) and a distance \(r\) are known, draw all points at distance \(r\) from \(O\).
- **Diameter endpoints**: If points \(A\) and \(B\) are opposite ends of a diameter, the center is the midpoint of \(AB\), and radius is \(|AB|/2\).
- **Three non-collinear points**: If points \(A, B, C\) lie on the circle and are not collinear, the circle is unique. Construct perpendicular bisectors of \(AB\) and \(BC\); their intersection is the center.

## Coordinate form (from three points)

For points \((x_i, y_i)\), solve for \((h, k, r)\) in:

\[
(x-h)^2 + (y-k)^2 = r^2.
\]

Subtracting equations pairwise removes \(r^2\), giving a linear system in \(h\) and \(k\). Once the center is found, compute \(r\) using any point.

## Practical checks

- Verify all source points are at the same distance from the recovered center (within tolerance if measured data is noisy).
- Reject degenerate input: identical points or three collinear points cannot define a unique circle.

In short: reconstructing a circle means recovering its **center** and **radius** from sufficient, non-degenerate information.
