# KISS Institute Equipment Usage Application — Triple-Sign Pass

## Purpose
The **Triple-Sign Pass** is a lightweight approval workflow for using shared institute equipment safely, fairly, and traceably.

## Scope
Applies to all restricted or high-value shared equipment at KISS Institute, including:
- Wet-lab instruments
- Fabrication tools
- Imaging systems
- Field deployment kits

## Triple-Sign Roles
A request is valid only when all three signatures are present:
1. **Applicant** — confirms training completion, intended use, and risk awareness.
2. **Supervisor/PI** — confirms scientific necessity, schedule alignment, and accountability.
3. **Equipment Custodian** — confirms readiness, safety compliance, and resource availability.

## Required Application Fields
- Applicant name, ID, team, and contact
- Equipment name and asset ID
- Requested date/time window
- Usage objective and protocol reference
- Required consumables and estimated quantity
- Safety checklist acknowledgment
- Contingency and shutdown plan

## Approval Rules
- Missing any required field: **return for revision**.
- Missing any one of three signatures: **not approved**.
- Conflicting schedule with higher-priority approved task: **queue or reschedule**.
- Safety risk not mitigated: **reject until controls are documented**.

## Pass States
- **Draft**: created, not submitted
- **Submitted**: awaiting signatures
- **Triple-Signed**: all three approvals complete
- **Active**: currently using equipment
- **Closed**: session completed and logged
- **Flagged**: incident or policy deviation requires review

## Operator Commitments
Before use, operator must:
- Verify calibration status
- Inspect equipment condition
- Confirm PPE and safety controls

After use, operator must:
- Clean and reset station
- Upload run notes and output location
- Record anomalies, maintenance needs, or incidents

## Revocation Conditions
A Triple-Sign Pass may be revoked if:
- Unsafe behavior is observed
- Equipment is used outside approved scope
- Logbook/reporting is repeatedly incomplete
- Emergency maintenance is required

## Audit and Retention
- All applications and signatures are retained for **24 months**.
- Flagged sessions are retained for **60 months**.
- Monthly audit samples verify fairness, safety compliance, and utilization accuracy.

## Minimal Form Template
```text
[ ] Applicant Information Complete
[ ] Equipment + Asset ID Confirmed
[ ] Time Window + Objective Entered
[ ] Safety Checklist Completed

Signature 1 (Applicant): __________  Date: ________
Signature 2 (Supervisor/PI): ______  Date: ________
Signature 3 (Custodian): __________  Date: ________

Decision:  APPROVED / REVISE / REJECT
```
