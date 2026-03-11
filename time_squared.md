# Time Squared

"Time squared" (`time²`) is a compact way to emphasize **acceleration of consequences**: if one unit of delay creates one unit of cost now, repeated delay can compound into much larger downstream effects.

## Practical interpretation

- **Linear time use:** each hour invested returns roughly one hour's worth of progress.
- **Time-squared dynamics:** each hour of delay increases not only elapsed time, but also coordination, context-switching, and recovery costs.

## Where this shows up

1. **Technical debt:** postponed maintenance increases future debugging complexity.
2. **Biology experiments:** delayed calibration can invalidate multiple future runs.
3. **Team communication:** unanswered questions branch into conflicting assumptions.

## Simple heuristic

When choosing between *small action now* and *perfect action later*, bias toward the small action if it prevents compounding delay.

## Tiny formula metaphor

If immediate cost is `c` per unit time and compounding friction grows with delay `t`, then planning cost can be thought of as:

`total_cost ≈ c·t + k·t²`

where `k` captures how strongly your system penalizes delay.
