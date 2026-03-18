# jb_bootcamp

Utilities for use in the Introduction to Programming in the Biological Sciences Bootcamp.

## Installation

Install the package in editable mode from the repository root:

```bash
pip install -e modules/jb_bootcamp
```

## Running tests

From within the `modules/jb_bootcamp` directory, run the test suite with:

```bash
pytest
```

## Shell usage

You can query the demographics helper directly from a shell with:

```bash
jb-demographics --age 25 --reference-year 2024
jb-demographics --birth-year 1985
```

## Contents

The package bundles small, self-contained utilities that accompany bootcamp lessons, ranging from simple arithmetic helpers to domain-focused examples like `bioinfo_dicts` and `fermented_foods`. Each module mirrors a practice exercise so learners can explore Python syntax and testing workflows.
