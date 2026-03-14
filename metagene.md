# Metagene

A **metagene** is an aggregated representation of many genes aligned to a common reference point so their average behavior can be compared.

## Why it is useful

- It reduces noise from single-gene variability.
- It highlights shared trends in gene expression or epigenetic signals.
- It is commonly used in genomics and transcriptomics to visualize genome-wide patterns.

## Typical construction workflow

1. Choose a reference feature (for example: transcription start site).
2. Normalize each gene region to a common coordinate system.
3. Aggregate signal across all genes (mean, median, or quantiles).
4. Plot the resulting profile as a metagene curve or heatmap.

## Common use cases

- RNA-seq expression trends around gene bodies.
- ChIP-seq enrichment around promoters.
- DNA methylation patterns across coding regions.
