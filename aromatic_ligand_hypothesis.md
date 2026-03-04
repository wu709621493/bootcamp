# Aromatic Ligand Hypothesis

## Core hypothesis
Aromatic ligands with tunable electron density and ring substitution patterns can improve target selectivity by simultaneously optimizing three interactions in a binding pocket:

1. **π-stacking geometry** with aromatic amino acids (Phe, Tyr, Trp),
2. **cation–π stabilization** near Lys/Arg-rich motifs, and
3. **shape complementarity** in hydrophobic subpockets.

If this is correct, ligand series that preserve a common aromatic scaffold but vary substituent electronics and steric bulk should display predictable shifts in affinity and selectivity across related protein targets.

## Rationale
- Aromatic systems are structurally rigid, reducing conformational entropy penalties upon binding.
- Substituents can modulate polarizability and quadrupole moments, altering π-contact strength.
- Ortho/meta/para substitution provides a practical way to steer binding poses without changing the core scaffold.

## Testable predictions
1. **Electron-rich aromatic variants** should increase affinity in pockets dominated by π-stacking and cation–π contacts.
2. **Electron-poor variants** may reduce off-target binding where aromatic contacts are weaker or geometrically misaligned.
3. **Bulky para substituents** should increase selectivity when a target pocket has a unique distal cavity.
4. Binding free energy trends should correlate with computed interaction energies from docking + short MD refinement.

## Experimental plan
1. Design a focused library (20–40 compounds) around one aromatic core.
2. Measure binding (SPR/ITC or enzyme IC50/Ki) across target and close homologs.
3. Solve 1–2 co-crystal or cryo-EM structures to verify ring orientation and contact maps.
4. Fit a simple QSAR model using Hammett constants, steric descriptors, and measured potency.

## Falsification criteria
The hypothesis is weakened if:
- affinity trends are not explained by electronic/steric aromatic descriptors,
- structural data show inconsistent aromatic engagement,
- or selectivity gains require non-aromatic features outside the modeled scaffold.

## Practical impact
A validated aromatic ligand hypothesis would provide a compact medicinal chemistry strategy for rapidly tuning potency/selectivity before broader scaffold exploration.
