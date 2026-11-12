# Skill Quality Review — Prioritized Improvements

*Review date: 2026-11-12. Scope: all 25 original skills under `skills/original/`, plus the skill tooling.*

## Method

What was actually run and observed:

| Check | Command | Result |
|-------|---------|--------|
| Frontmatter validation | `python scripts/validate-frontmatter.py` | OK: 0 errors, 19 warnings |
| Rule-copy sync | `python scripts/check-sync.py` | OK: 11 modules, 9 profiles, combined copy |
| Index freshness | `python scripts/update-category-index.py --check` | OK: up to date |
| Tooling tests | `python -m unittest discover -s scripts -p "test_*.py"` | 34 tests, OK |

In addition, a section-coverage scan of all 25 `SKILL.md` files (heading census,
calibrated by manual spot reads) informed the structural findings below.

## Summary

The collection is in good shape: every skill has valid frontmatter, the
required fields are complete, the name/folder convention holds, and the whole
tooling suite passes. The findings below are quality and consistency work, not
repairs. Per the review policy, no skill was mass-rewritten; each item lists
the affected files so follow-ups can be small and deliberate.

## Priority table

| # | Priority | Finding | Affected | Status |
|---|----------|---------|----------|--------|
| 1 | P1 | Six skill `category` labels are in use but absent from the documented category table and the validator's known set | 11 skills | **Fixed in this branch** (see [Category alignment](#1-category-alignment)) |
| 2 | P2 | Skill descriptions exceed the picker-length guidance | 7 skills | Open |
| 3 | P2 | Section vocabulary in most skills diverges from the `SKILL_SPEC.md` template | 20 skills | Open (decision needed) |
| 4 | P3 | `Version History` section missing in most skills | 20 skills | Open, incremental |
| 5 | P3 | `write-research-projects/SKILL.md` exceeds the 500-line guidance (731 lines) | 1 skill | Open, low urgency |
| 6 | P3 | Two penetration-testing skills overlap in scope | `pen-testing`, `penetration-testing-guide` | Open, keep both or consolidate |
| 7 | P3 | Bundled third-party `SKILL.md` files are outside frontmatter validation | 7 skills | Documented as intentional |

## Details

### 1. Category alignment

The validator warned `Unknown category` for eleven skills because these labels
are used in frontmatter but were missing from both the validator's
`KNOWN_CATEGORIES` set and the category table in `docs/SKILL_SPEC.md`:

| In-use label | Skills | Notes |
|--------------|--------|-------|
| `dev` | `beyond-vibe-coding-autonomous-development`, `document-editing-general`, `fix-inconclusive-skills`, `generate-findings-report-from-pipeline-logs`, `github-code-documentation` | Legacy shorthand for the documented `development` |
| `documents` | `detailed-source-rewrite-guide`, `generate-markdown-and-docx-documents` | Mirrors `instructions/modules/documents.md` |
| `knowledge` | `book-to-skill` | No module equivalent |
| `engineering-3d` | `enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras` | Mirrors `instructions/modules/engineering-3d.md` |
| `security` | `penetration-testing-guide` | Mirrors `instructions/modules/security.md` |
| `testing` | `testing-skills` | Mirrors `instructions/modules/testing.md` |

Resolution applied in this branch:

- `KNOWN_CATEGORIES` extended with `documents`, `engineering-3d`, `security`,
  `testing`, `knowledge` so the validator and the spec describe the same
  vocabulary.
- `docs/SKILL_SPEC.md` category table extended with the same labels.
- Frontmatter `dev` normalized to the documented `development` label
  (frontmatter + matching `catalog/items.json` records + regenerated index).

Remaining follow-up: decide whether `knowledge` stays as a label or migrates
to `research`. Kept as-is for now because it is a single, working record.

### 2. Description length (P2)

The repository style advisory is a 160-character description for skill-picker
display; documented authoring guidance is 500. Current offenders:

| Skill | Description length | Above |
|-------|-------------------:|-------|
| `prep-for-meetings` | 647 | 500-char guidance |
| `focus-my-energy` | 506 | 500-char guidance |
| `match-my-writing-style` | 488 | 160-char advisory |
| `generate-fresh-ideas` | 487 | 160-char advisory |
| `get-more-perspectives` | 474 | 160-char advisory |
| `beyond-vibe-coding-autonomous-development` | 260 | 160-char advisory |
| `github-code-documentation` | 227 | 160-char advisory |

Recommendation: rewrite each frontmatter `description` to one line of at most
160 characters that still carries the trigger ("Use when..."), and move the
long rationale into the skill body where it already mostly lives. Not done
automatically because descriptions are activation cues; wording changes affect
skill triggering.

### 3. Section vocabulary vs `SKILL_SPEC.md` (P2)

The spec template prescribes `Workflow`, `Rules & Constraints`, `Examples`,
`Anti-Patterns`, `Related Skills`, `Version History`. The de-facto structure in
20 of 25 skills is leaner: `When to Use`, `Procedure`, `Pitfalls`,
`Verification` (calibrated manually; the census below is the raw scan). The
content the spec asks for is present, but under different names — so the spec
and the skills disagree about vocabulary, not substance.

Recommendation: update `docs/SKILL_SPEC.md` to document the de-facto lean
structure as the standard (mapping `Procedure`→workflow, `Pitfalls`→rules and
anti-patterns, `Verification`→examples/evidence), instead of renaming headings
in twenty files. Decision is open; the review records both options.

Raw census (strict heading-name match; many "missing" entries exist under a
different name — see the calibrated note above):

- Full spec coverage: `pen-testing`
- Near-complete: `agent-operating-rules`, `repository-hygiene`, `write-research-projects`, `ticktick-tasks`
- Lean structure (`When to Use` / `Procedure` / `Pitfalls` / `Verification`): most of the 2026 additions, e.g. `beyond-vibe-coding-autonomous-development`, `yfinance-ai`, `testing-skills`
- Mixed: `focus-my-energy`, `generate-fresh-ideas`, `get-more-perspectives`, `match-my-writing-style`, `prep-for-meetings`

### 4. Version history (P3)

Only 5 of 25 skills carry a `Version History` section:
`agent-operating-rules`, `repository-hygiene`, `pen-testing`,
`write-research-projects`, `ticktick-tasks`. Recommendation: add the section
incrementally, the next time each skill is edited, rather than in one sweep.

### 5. Long file (P3)

`write-research-projects/SKILL.md` is 731 lines against the documented 500-line
guidance. It is the collection's flagship research workflow; splitting it (for
example, a core workflow plus a separate source-verification companion) is a
candidate, but nothing depends on it today.

### 6. Overlap between the two pentest skills (P3)

`pen-testing` (authorized-testing methodology with a scope gate) and
`penetration-testing-guide` (five-phase guide) cover overlapping ground.
Options: keep both with clearer trigger wording, or merge into one. No action
taken in this branch.

### 7. Bundled third-party skills and validation (P3)

`validate-frontmatter.py` discovers skills under `skills/original/` only; the
seven bundled third-party copies under `skills/third-party/` are checked for
existence and policy by the tooling tests, but their upstream frontmatter is
not re-validated. This is intentional — their content belongs to upstream
authors and is preserved as-is. Documented here so the decision is visible.

## Out of scope of this review

- External link-only skills: quality is owned upstream; this repository tracks
  availability (`scripts/check-links.py`) and provenance, not content.
- Personas, prompts, rule modules: separate bodies of work, not `SKILL.md`
  skills; they are covered by the sync check instead.
