# Cigarette Conjecture (Cigarette-Butt Exchange Puzzle)

A common "cigarette conjecture" in puzzle circles is:

> If one new cigarette can be made from `k` cigarette butts, and you start with `n` cigarettes,
> then the total number you can smoke is
>
> `n + floor((n - 1) / (k - 1))` for `k > 1`.

## Why this works

- Every smoked cigarette produces one butt.
- Creating a new cigarette consumes `k` butts but eventually returns one butt when smoked.
- So each extra cigarette effectively reduces your butt balance by `k - 1`.
- Starting from `n` butts over time, the number of extra cigarettes is therefore bounded by how many
  times you can subtract `k - 1` before dropping below `k`.

Equivalent expression for extras:

`extras = floor((n - 1) / (k - 1))`

Total:

`total = n + extras`

## Example

If `n = 10` and `k = 3`:

- Extras = `floor((10 - 1) / (3 - 1)) = floor(9 / 2) = 4`
- Total smoked = `10 + 4 = 14`
