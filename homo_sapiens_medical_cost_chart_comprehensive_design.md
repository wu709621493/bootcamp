# Homo sapiens medical cost chart: comprehensive design

## Purpose
Design a medical cost chart that explains how costs accumulate across a human lifetime, balances clinical clarity with financial transparency, and supports decisions by patients, clinicians, insurers, employers, and policy teams.

## Audience and use cases
- **Patients & caregivers:** understand what is billed, why, and how choices affect out-of-pocket cost.
- **Clinicians:** visualize cost tradeoffs alongside outcomes for shared decision-making.
- **Finance & ops teams:** identify high-cost pathways, avoidable spend, and prevention ROI.
- **Policy makers & researchers:** compare cohorts, highlight inequities, and model interventions.

## Core chart concept
A **layered, timeline-based cost stack** that follows a person from birth to late life, with **care domains as bands**, **events as spikes**, and **out-of-pocket vs. covered amounts** as split shading. The design allows both **macro (lifecycle)** and **micro (episode)** analysis.

## Data model (minimum viable)
- **Time axis:** age in years (0–100), with optional monthly granularity during early life and end-of-life.
- **Cost axis:** annual spend (inflation-adjusted, e.g., USD 2024).
- **Cost categories:**
  - Preventive & primary care
  - Acute care (ED, inpatient)
  - Chronic disease management
  - Mental health & substance use
  - Maternal & reproductive health
  - Pediatric care & immunizations
  - Long-term care & home health
  - Pharmaceuticals
  - Diagnostics & imaging
  - Rehabilitation & assistive devices
- **Payer split:** patient out-of-pocket, private insurance, public insurance, employer contributions, and charity/other.
- **Outcome overlays:** quality of life index, survival probability, and disability-adjusted life years (DALYs).

## Visual layout
### 1) Primary lifecycle stack
- **X-axis:** age bands (0–5, 6–17, 18–35, 36–50, 51–65, 66–80, 81+).
- **Y-axis:** annual cost per person.
- **Stacked areas:** categories above, normalized to total cost per age.
- **Split fill:** top portion indicates out-of-pocket share; bottom indicates covered share.
- **Key events overlay:** thin vertical markers (e.g., childbirth, major surgery, diagnosis).

### 2) Episode zoom-in panel
- Small multiples for high-cost episodes (e.g., myocardial infarction, hip fracture, cancer).
- Show **pre-event, event, post-event** phases with cost distribution and recovery timeline.

### 3) Cost drivers table
- A compact table next to the chart listing **top 5 drivers** by age band with percent contribution.

### 4) Equity overlay
- A toggle to compare cohorts (gender, income, geography, race/ethnicity) using color-coded outlines.

## Design rules
- **Color palette:** muted base colors for categories; bright accent for out-of-pocket.
- **Hierarchy:** thick axis labels; event markers are thin to avoid dominating the lifecycle view.
- **Legibility:** avoid more than 10 categories in the primary stack; group smaller items into “Other.”
- **Accessibility:** colorblind-safe palette; texture for payer split; minimum 4.5:1 contrast.

## Sample annotation copy
- “Preventive care costs are low but steady; each 1% increase in preventive utilization reduces acute cost spikes by ~3%.”
- “Out-of-pocket share rises sharply in early retirement before Medicare eligibility.”
- “Chronic disease management dominates spend after age 50.”

## Data sources (suggested)
- National health expenditure accounts (NHEA)
- Claims data (commercial + Medicare/Medicaid)
- Hospital cost reports
- Population surveys (e.g., MEPS)

## Validation checklist
- Costs are inflation-adjusted and consistent across sources.
- Category definitions match billing codes (ICD/CPT/DRG).
- Payer split percentages sum to 100% per age band.
- High-cost outliers are annotated with context.

## Deliverables
- Static infographic (PDF/PNG)
- Interactive dashboard (filters for cohort and time window)
- Data dictionary (definitions, inclusion/exclusion criteria)

## Success metrics
- Stakeholders can identify top cost drivers within 60 seconds.
- Users correctly interpret out-of-pocket share vs. covered share.
- Chart supports actionable decisions (e.g., preventive investment, policy design).
