# Quantitative Work and Data

Read when: planning or analysing experiments, calculations, measurements or logged data.

Part of the `write-research-projects` method (version 2.3.0). The core rules, workflow, research and writing procedure are in `../SKILL.md`.

## Calculations

- Audit chain: objective → formula → inputs with units and provenance → substitution → result → independent recomputation → dimensional check → plausibility / limiting case → justified rounding.
- Label measured vs calculated values. Distinguish precision, accuracy, resolution, repeatability, calibration error, and uncertainty.
- Percent change: state the reference value and formula. Percentages always have a baseline.
- Energy/capacity from logged data: state the integration method, sampling, sign convention, and limits.

## Data

- Keep raw data immutable; work on copies; log every cleaning step, exclusion, unit conversion, and filter.
- Never fill missing data with invented values; mark gaps. Check outliers, drift, clipping, duplicates, and timestamps.
- Recompute key results from raw data rather than copied summary values.
- Figures: purpose, labeled axes with units, legend, conditions, sample size (n), honest scale. Generate from preserved data or scripts.
- Tables: units, conditions, comparable metrics only; mark non-comparable entries instead of ranking them.

## Experiments

Write the protocol before interpreting results:

```text
Test ID / objective:
Hypothesis or requirement:
System / sample and ID:
Configuration + version:
Baseline:
Variables: independent / dependent / controlled / confounders:
Instruments, calibration, resolution, sampling, sensor placement:
Conditions, preconditioning, procedure:
Stop criteria, safety limits:
Repeats and rationale:
Metadata to record:
Analysis method, uncertainty:
Expected / observed:
Raw data location:
Deviations / failures:
Limitations:
Pass/fail, follow-up:
```

- Record actual conditions, not intended ones. Report deviations.
- Keep failed and anomalous runs; do not cherry-pick.
- Separate observation, interpretation, and limitation.
- One sample or event supports a cautious case report, not a universal claim.
- Write the method so another person could reproduce it.
