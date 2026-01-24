# Clear Calculation of Old Dues

Old dues are past-due balances that need a transparent method to compute principal, penalties, and interest. A clear calculation avoids disputes and shows exactly how the total was built.

## 1. Gather required inputs
- **Original principal**: the unpaid amount from each billing cycle.
- **Due dates**: when each amount became overdue.
- **Interest or late fee rules**: percentage rates, flat fees, and compounding rules.
- **Credits or payments**: partial payments, waivers, or adjustments already applied.
- **Cutoff date**: the date you want the total calculated through.

## 2. Build a due schedule
Create a table with one row per charge or invoice:
- Invoice ID
- Principal amount
- Due date
- Days past due (cutoff date minus due date)
- Applicable rate or fee type

## 3. Calculate interest or penalties
Use the policy that applies to each charge. Two common approaches:

### Simple interest
```
Interest = Principal × Annual Rate × (Days Past Due ÷ 365)
```

### Flat late fees
```
Late Fee = Flat Fee × Number of Missed Cycles
```

If compounding applies (e.g., monthly), compute interest per period and add it to the principal for the next period.

## 4. Apply payments and credits
Apply any payments or credits in chronological order:
1. Fees and interest (if policy requires it).
2. Principal.

Document the date and amount of every credit so the trail is clear.

## 5. Summarize the total
For each invoice, sum:
- Remaining principal
- Accrued interest
- Late fees

Then add everything together for the final balance. Provide subtotals per invoice and a grand total.

## 6. Provide a transparent summary
Include:
- The calculation method and rates used.
- The cutoff date.
- A table of each invoice with subtotals.
- Any assumptions (e.g., 365-day year, policy priorities).

## Example template
| Invoice | Principal | Due Date | Days Past Due | Interest | Late Fees | Payments | Balance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INV-001 | 1,000.00 | 2023-07-01 | 200 | 54.79 | 0.00 | 200.00 | 854.79 |

This structure keeps the calculation consistent, auditable, and easy to explain.
