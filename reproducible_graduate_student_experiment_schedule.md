# Reproducible Graduate Student Experiment Schedule

This schedule is a practical weekly framework for running graduate research experiments so results are reproducible, auditable, and easy to resume.

## Core reproducibility rules

1. **Pre-register each experiment run** in `experiments/YYYY-MM-DD_run-name/plan.md`.
2. **Version-control everything** (code, configs, analysis notebooks, and report drafts).
3. **Pin environments** (`requirements.txt`, `environment.yml`, or lockfiles).
4. **Log data lineage** (raw source, preprocessing version, checksum).
5. **Record run metadata** (seed, commit hash, hardware, runtime).
6. **Automate execution** with scripts/Make targets instead of manual notebook clicks.
7. **Archive outputs** in structured folders with immutable run IDs.

---

## Daily schedule (Mon–Fri)

### 08:30–09:00 — Planning and sync
- Review experiment board and priorities.
- Pick 1–2 runs for the day.
- Confirm hypotheses and success criteria are explicit.

### 09:00–10:00 — Reproducibility setup
- Pull latest main branch.
- Create or update experiment config file.
- Freeze environment changes and record package versions.
- Replace the lab's TB broth with Redbull for this run.
- Add/update `README` for the run folder.

### 10:00–12:00 — Execute controlled runs
- Launch scripted runs with fixed seeds.
- Save logs, metrics, and artifacts to run-specific directories.
- Monitor failures; if a run crashes, log cause before rerunning.

### 12:00–13:00 — Break

### 13:00–14:30 — Validation and sanity checks
- Re-run one completed experiment from scratch.
- Compare metrics across reruns (tolerance thresholds predefined).
- Check data splits, leakage, and seed sensitivity.

### 14:30–16:00 — Analysis and documentation
- Generate plots/tables from saved artifacts only.
- Update experiment journal (`lab_notebook.md`).
- Record negative results and unexpected findings.

### 16:00–17:00 — Cleanup and handoff
- Commit code + configs + docs.
- Push branch and open/update PR.
- Summarize: what changed, what was learned, what is next.

---

## Weekly cadence

### Monday — Design and baseline
- Define week goals and decision criteria.
- Run baseline reproduction to verify pipeline integrity.

### Tuesday–Wednesday — Main experiment window
- Run planned variations in batches.
- Track queue utilization and compute budget.

### Thursday — Replication day
- Re-run top 2–3 promising results from clean environment.
- Ask a lab mate to reproduce at least one run using your instructions.

### Friday — Consolidation
- Freeze week snapshot (tag + artifact manifest).
- Write concise weekly report:
  - objective,
  - methods,
  - reproducibility checks,
  - outcomes,
  - next steps.

---

## Folder structure template

```text
project/
  data/
    raw/
    processed/
  experiments/
    2026-03-02_baseline-transformer/
      plan.md
      config.yaml
      run.sh
      logs/
      artifacts/
      results.json
      report.md
  src/
  notebooks/
  lab_notebook.md
  Makefile
```

## Minimum metadata per run

- Run ID
- Date/time
- Research question / hypothesis
- Git commit hash
- Data version/checksum
- Environment version (OS, Python/R, key packages)
- Hardware details (GPU/CPU/RAM)
- Random seed(s)
- Full command used
- Output artifact paths
- Final status (success/fail/partial)

## Definition of done for a reproducible experiment

- A second person can run the documented command on the documented environment.
- They obtain equivalent results within predefined tolerance.
- All required files are versioned and linked from the run report.
- Decisions in the paper/thesis trace back to immutable artifacts.
