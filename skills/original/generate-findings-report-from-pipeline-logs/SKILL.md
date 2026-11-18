---
name: generate-findings-report-from-pipeline-logs
description: "Verify that all expected sections and data are present in generated files by comparing logs and output artifacts, and summarize discrepancies."
version: 1.0.0
author: DracieVajko
tags: [log-analysis, report-generation, markdown, file-comparison, automation]
category: development
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/generate-findings-report-from-pipeline-logs/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Generate Findings Report from Pipeline Logs

Verify that all expected sections and data are present in generated files by comparing logs and output artifacts, and summarize any discrepancies.

## When to Use

- Need to verify that all expected sections and data are present in generated files by comparing logs and output artifacts, and summarize any discrepancies.

## Procedure

1. Identify and list the relevant log and output files (JSON run metadata, generated `*.md` reports).
2. Load each file's contents into memory using a JSON or text parser.
3. Compare expected keys/sections (run_id, file sizes, section headings) against actual values; record mismatches or missing items.
4. Organize discovered issues into priority categories (Critical, High, Medium, Low).
5. Compose a Markdown report with an executive summary, a table of issues by priority and detailed descriptions for each finding.
6. Write the report to a known path in the workspace.

## Pitfalls

- Missing or inaccessible log/output files.
- Incomplete comparison (skipping sections).
- Writing the report to the wrong path.

## Verification

- The report exists at the expected path.
- All mismatches and missing items are documented.
- Findings are categorized by priority.
