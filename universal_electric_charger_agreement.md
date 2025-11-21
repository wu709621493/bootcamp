# Universal Electric Charger Agreement

## 1. Parties and Purpose
This Universal Electric Charger Agreement ("Agreement") is entered into by and between the undersigned manufacturers, distributors, platform operators, and related stakeholders (each, a "Party"). The purpose of this Agreement is to establish common technical, safety, and commercial terms for interoperable electric chargers and power adapters that reduce e-waste, improve user convenience, and enable a consistent customer experience across devices.

## 2. Definitions
- **Universal Charger**: A charger compliant with the technical and safety requirements set forth in this Agreement.
- **Device**: Any hardware product designed to receive power from the Universal Charger.
- **Reference Design**: A charger design shared among Parties for manufacturing, testing, and certification purposes.
- **Firmware**: Embedded software controlling charging behavior, safety monitoring, and communication with Devices.

## 3. Technical Standards
1. **Connector and Cabling**: USB Type-C receptacle on the charger and cable compliant with USB-C specifications; cable assemblies must meet USB-IF standards for current capacity and e-marker requirements where applicable.
2. **Power Delivery Profiles**: Compliance with the latest published USB Power Delivery (USB-PD) specification, supporting at minimum 5 V/3 A, 9 V/3 A, 15 V/3 A, and 20 V/3.25 A (65 W) profiles; optional Extended Power Range (EPR) profiles (28–48 V) where supported by components.
3. **Communication and Negotiation**: Chargers must negotiate power using USB-PD; proprietary fast-charge schemes are allowed only if they remain backward-compatible with USB-PD and do not degrade baseline PD interoperability.
4. **Electrical Protections**: Mandatory over-voltage, over-current, over-temperature, short-circuit, and surge protections; default safe state is power-off with auto-recovery where safe.
5. **EMC and Safety Compliance**: Conformance with IEC/EN 62368-1 for safety and applicable EMI/EMC standards (e.g., EN 55032/55035, FCC Part 15B). Region-specific certifications (CE, UKCA, UL, PSE, KC, CCC) must be obtained prior to market release.
6. **Energy Efficiency**: External Power Supply (EPS) efficiency requirements must meet or exceed ENERGY STAR EPS 3.0 and regional mandates (DOE Level VI, EU CoC Tier 2, or successor standards).
7. **Mechanical and Environmental**: Housings rated minimum IP20; optional higher ingress protection for outdoor use; operating range 0–40°C; storage range -20–60°C; enclosures must meet flammability rating UL94 V-0 or equivalent.
8. **Sustainability**: Design for disassembly where practical, avoidance of hazardous substances per RoHS/REACH, and use of post-consumer recycled plastics where feasible.
9. **Quality and Reliability**: Mean Time Between Failure (MTBF) target ≥ 100,000 hours at 25°C; chargers must pass HALT/HASS where required and 500+ insertion cycles for connectors.

## 4. Testing, Certification, and Audit
1. Parties shall submit Universal Chargers for pre-compliance testing against USB-IF PD CTS, safety, EMC, and efficiency requirements.
2. Certification lab results must be shared with signatory Parties; major failures must be remediated before market shipment.
3. Parties grant each other audit rights (with reasonable notice) to review production quality control, component traceability, and firmware versioning.
4. Non-conformities must be corrected within mutually agreed remediation timelines; sustained non-compliance may trigger suspension of certification under this Agreement.

## 5. Firmware and Security
1. Firmware must enforce negotiated voltage/current limits, include watchdogs for thermal and fault conditions, and log critical events.
2. Firmware updates (if supported) must be authenticated, signed, and integrity-checked before installation; rollback to a known-good image must be supported.
3. Parties shall disclose and remediate security vulnerabilities consistent with coordinated disclosure practices.

## 6. Supply Chain and Components
1. Parties shall maintain Approved Vendor Lists (AVL) for critical components (PD controllers, power MOSFETs, magnetics, capacitors) with dual sourcing where practicable.
2. Critical safety components must have valid safety certificates and be traceable by lot and date code.
3. Parties shall notify others within five business days of material changes to design, firmware, or manufacturing location that could affect compliance or interoperability.

## 7. Packaging, Labeling, and Documentation
1. Chargers must be labeled with output profiles, certifications, serial/lot identifiers, and recycling marks.
2. Packaging must clearly state compatibility with USB-C and USB-PD, and include safety warnings and operating temperature range.
3. User documentation shall include safe use guidelines, fault indicator meanings, and instructions for obtaining firmware/security updates (if applicable).

## 8. Interoperability and Backward Compatibility
1. Parties commit to verifying interoperability with a representative matrix of Devices across major platforms and power levels.
2. Legacy support: chargers must safely power non-PD USB devices at default USB current limits.
3. Fast-charge extensions must gracefully fall back to PD defaults when unsupported by a Device.

## 9. Environmental and Take-Back
1. Parties shall operate take-back/recycling programs where legally required and work toward voluntary programs where absent.
2. E-waste reduction targets: Parties will review annual targets to increase adoption of Universal Chargers and reduce bundled chargers where permitted by law and customer acceptance.

## 10. Commercial Terms
1. **Pricing and Royalties**: Except as separately agreed, Parties will not charge royalties for baseline USB-PD interoperability; optional proprietary fast-charge licensing, if any, must be FRAND and documented.
2. **Reference Designs**: Non-exclusive reference designs may be shared under reciprocal, non-sublicensable licenses for the purpose of manufacturing Universal Chargers.
3. **Orders and Forecasts**: Parties will provide non-binding rolling 90-day forecasts and firm purchase orders consistent with standard lead times; allocation policies during constraints will be fair and non-discriminatory.
4. **Warranty**: Minimum one-year limited warranty against defects in materials and workmanship; remedies limited to repair, replacement, or refund.

## 11. Confidentiality
All non-public information exchanged under this Agreement shall be treated as confidential, used solely for purposes of this collaboration, and protected with at least reasonable care. Confidentiality obligations survive for five years after termination.

## 12. Intellectual Property
1. Each Party retains ownership of its pre-existing IP. No Party grants any license except as expressly provided for reference designs, interoperability, or certification.
2. Contributions to shared specifications are licensed to other Parties on a non-exclusive, worldwide, royalty-free basis to the extent necessary to implement the Universal Charger requirements.
3. Any essential patents covering baseline USB-PD compliance shall be offered on FRAND terms.

## 13. Term, Suspension, and Termination
1. This Agreement commences on the Effective Date and remains in force for three years, automatically renewing annually unless a Party provides 60 days’ notice.
2. A Party may be suspended for material non-compliance after failure to cure within 30 days of written notice; suspension can be lifted upon verified remediation.
3. Termination for cause may occur upon insolvency, repeated safety violations, or material breach; accrued obligations survive termination.

## 14. Liability
Liability of each Party is limited to direct damages capped at fees paid or payable under the applicable purchase orders in the prior 12 months. Neither Party is liable for consequential, incidental, or special damages, except for breaches of confidentiality or IP indemnity obligations.

## 15. Indemnification
Each Party shall indemnify, defend, and hold harmless the others from third-party claims alleging (a) bodily injury or property damage caused by defective chargers supplied by the indemnifying Party, or (b) IP infringement arising from the indemnifying Party’s designs, except to the extent caused by modifications by the indemnified Parties.

## 16. Governance and Change Management
1. Establish a Technical Steering Committee (TSC) with representatives from each Party to maintain the technical baseline, approve changes, and review interoperability issues.
2. The TSC will publish versioned revisions of the Universal Charger Requirements, maintain test plans, and track compliance metrics.
3. Substantive changes require majority vote of the TSC and 45 days’ notice before enforcement.

## 17. Dispute Resolution
Parties will first attempt to resolve disputes through good-faith negotiation, then mediation. If unresolved, disputes shall be settled by binding arbitration under the rules of the International Chamber of Commerce (ICC) with one arbitrator, in English, and seated in a mutually agreed neutral location.

## 18. Governing Law
This Agreement is governed by the laws of [Jurisdiction], excluding conflicts-of-law principles. The U.N. Convention on Contracts for the International Sale of Goods does not apply.

## 19. Notices
Notices shall be in writing and delivered by email with confirmation, or by courier to the addresses designated by the Parties.

## 20. Miscellaneous
- No assignment without consent, except to affiliates or in connection with a merger or sale of substantially all assets.
- Independent contractors; no partnership or agency is created.
- Entire Agreement; amendments must be in writing and signed by authorized representatives.
- Severability; waiver of a provision does not waive future enforcement.

## 21. Signatures
Authorized representatives of the Parties may sign in counterparts and via electronic signature. The Effective Date is the date of the last signature below.

---

**Party A:** ______________________   Date: _____________

**Party B:** ______________________   Date: _____________

**Additional Parties (if any):** ______________________   Date: _____________
