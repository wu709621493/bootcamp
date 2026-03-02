# ADHD, Bipolar Disorder, and Schizophrenia: 2D-HPLC Research Concept

## Objective
Evaluate whether **two-dimensional high-performance liquid chromatography (2D-HPLC)** can separate and quantify metabolomic panels associated with ADHD, bipolar disorder, and schizophrenia in plasma/serum samples.

## Rationale
These conditions are diagnosed clinically, but biological signatures may improve stratification and treatment selection. 2D-HPLC can improve resolution of complex biological matrices by combining orthogonal separation modes (for example, ion-exchange in the first dimension and reversed-phase in the second dimension).

## Proposed Design
- **Groups:** ADHD, bipolar disorder, schizophrenia, and matched healthy controls.
- **Samples:** Fasting plasma and optional urine.
- **Dimension 1:** Fractionation by polarity/charge class.
- **Dimension 2:** High-resolution separation of target fractions.
- **Detection:** UV/fluorescence and LC-MS confirmation for peak identity.

## Candidate analyte classes
- Neurotransmitter-related metabolites (catecholamine and tryptophan pathways)
- Inflammatory lipid mediators
- Oxidative stress markers
- Kynurenine pathway metabolites
- Medication metabolites (for adjustment/covariate analysis)

## Key controls and confounders
- Medication status (stimulants, antipsychotics, mood stabilizers, antidepressants)
- Smoking/nicotine, caffeine, sleep deprivation
- Age, sex, BMI, fasting state, and circadian timing
- Comorbid substance use and metabolic disease

## Analysis plan
1. Preprocess chromatograms (retention-time alignment, baseline correction, peak normalization).
2. Compare classes using multivariate models (PCA/PLS-DA with strict cross-validation).
3. Build classifiers for pairwise and multiclass discrimination.
4. Validate on an external cohort.

## Limitations
- Psychiatric diagnoses are heterogeneous and overlapping.
- Medication effects may dominate biological signals.
- Cross-sectional designs cannot establish causality.

## Deliverables
- 2D-HPLC method parameters and QC report
- Candidate biomarker panel with effect sizes
- Replication-ready SOP for independent cohorts
