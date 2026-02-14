# The Art of CRISPR Editing — Lecture Notes

## 1) Why people call CRISPR an “art”
CRISPR is often taught as a tool, but in practice it behaves like both engineering **and** craft. You can know the rules and still need judgment in design, timing, delivery, and validation. The “art” is balancing efficiency, specificity, ethics, and biological context.

---

## 2) Fast conceptual refresher
- **CRISPR-Cas system:** A programmable nuclease (often Cas9) guided by RNA to a DNA sequence.
- **Cut location control:** Determined by guide RNA complementarity and PAM constraints.
- **Repair outcome:** The cell’s repair machinery determines edit type:
  - **NHEJ** → small insertions/deletions (often knockouts)
  - **HDR** → precise changes with donor template (typically lower efficiency)

Think of Cas as scissors, gRNA as the address label, and DNA repair as the unpredictable “tailor” that finishes the job.

---

## 3) The design layer (where art begins)
### A. Defining the biological objective
Before sequence design, ask:
1. What phenotype matters most?
2. Is full knockout required, or partial modulation enough?
3. Is permanent editing necessary, or would CRISPRi/CRISPRa be safer?

### B. Guide RNA strategy
- Prioritize guides with strong on-target score and low off-target risk.
- Avoid problematic genomic regions (repeats, copy-number complexity, inaccessible chromatin where possible).
- Design multiple guides in parallel to reduce single-guide failure.

### C. Choosing the editor platform
- **Cas9 nuclease:** strong for knockouts
- **Nickase pairs / high-fidelity variants:** lower off-target risk in some contexts
- **Base editors:** single-base changes without double-strand breaks
- **Prime editors:** flexible edits with potentially cleaner outcomes (often more optimization required)

The art is selecting the *least disruptive tool* that still answers the biological question.

---

## 4) Delivery is destiny
Even perfect guide design fails if delivery is poor.

- **Transient RNP delivery:** fast, often lower prolonged off-target activity.
- **Plasmid delivery:** simple, but longer editor expression can increase risk.
- **Viral delivery (e.g., AAV/lenti):** useful in hard-to-transfect cells, with packaging and safety tradeoffs.

Cell type, cycle state, and viability often dominate outcomes more than theoretical guide score.

---

## 5) Validation: don’t trust a single readout
A disciplined validation stack usually includes:
1. **Genotyping** (amplicon sequencing/Sanger + decomposition)
2. **Off-target checks** (in silico + targeted or unbiased methods depending on risk)
3. **Functional readout** (protein, pathway, phenotype)
4. **Clonal vs pooled logic** (depends on experimental question)

Good CRISPR work is not “I got an indel.” It is “I can defend mechanism and consequence.”

---

## 6) Common failure modes
- Chasing high edit percentage without biological relevance
- Underestimating mosaicism and allele complexity
- Ignoring p53/stress responses in sensitive systems
- Over-claiming causality from one clone or one guide

A practical rule: if your story depends on one construct and one assay, it is probably incomplete.

---

## 7) Ethics and governance
CRISPR power demands proportional responsibility.

- Distinguish **somatic therapy research** from **germline editing**.
- Build consent, transparency, and risk communication into project design.
- Use independent review and red-team thinking for ecological or heritable interventions.

Technical success does not automatically justify deployment.

---

## 8) Closing takeaway
The art of CRISPR editing is not just cutting DNA—it is choosing the right biological question, the right editor, the right delivery path, and the right evidence threshold, while respecting ethical boundaries.

When done well, CRISPR is less like pressing a button and more like composing: design, timing, harmony, and revision.
