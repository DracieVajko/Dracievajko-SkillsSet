# Skills Catalog

This directory contains the canonical structured catalog of all skills, prompts, and agent instructions in this collection.

## Files

- **skills-catalog.json** — Machine-readable catalog with full provenance
- **items.csv** — Flat CSV view of all catalog items
- **items.json** — JSON view of all catalog items
- **catalog-reconciliation.csv** — Reconciliation of original 154-record catalog with current state
- **provenance-tracking.json** — Detailed provenance tracking for each item
- **source-mapping.md** — Mapping of local files to upstream sources
- **custom-or-unresolved.json** — Items that are custom-created or have unresolved sources
- **custom-skills.json** — Custom/original skills only
- **unresolved-sources.json** — Items with unresolved attribution
- **unresolved.md** — Human-readable unresolved items
- **categories/** — Category-specific catalogs
- **presets/** — Skill presets for different workflows

## Catalog Authority

Exactly one authoritative input per generated `docs/CATEGORY_INDEX.md` section:

| Index section | Authoritative input |
|---------------|---------------------|
| Original local skills | local tree, `01-my-skills/**/SKILL.md` |
| Modified local skills | local tree, `02-my-modified-skills/**/SKILL.md` |
| Third-party local skills | local tree, `03-third-party-skills/**/SKILL.md` |
| Link-only references | `03-third-party-skills/odysseus/skill-links.txt` + `unverified-links.txt` |
| Unresolved inventory entries | `items.json` where `authorship` is `unresolved` |
| Notes / catalog-vs-tree drift | `items.json` (`local_skill_path` column) |

The generators treat a missing or malformed authoritative input as an error and
exit nonzero; they never fall back to an empty collection.

Historical / derived views — **not** authoritative and not read by any generator:
`custom-skills.json`, `custom-or-unresolved.json`, `unresolved-sources.json`,
`unresolved.md`, `items.csv`, `catalog-reconciliation.csv`,
`provenance-tracking.json`, `skills-catalog.json`, `categories/`, `presets/`.
They record how the catalog evolved and may use older sets, scopes or labels.
See the scope note in `unresolved.md` for the documented differences.

## Catalog Statistics

Derived from `items.json` (`authorship`) and the local tree. The derived numbers
are asserted by `scripts/test_skills_tooling.py` (`CatalogDataTests`).

| Category | Count | Source |
|----------|-------|--------|
| Original local skills (`01-my-skills`) | 1 | local tree, `items.json` |
| Modified local skills (`02-my-modified-skills`) | 0 | local tree |
| Third-party skills with local copies (`03-third-party-skills/agent-harnesses`) | 17 | local tree (`items.json`: 18 records) |
| Third-party link-only records | 136 | `items.json` `authorship: link-only` |
| Third-party link-only URLs | 154 (142 + 12) | `odysseus/skill-links.txt` + `unverified-links.txt` |
| Unresolved inventory records | 23 | `items.json` `authorship: unresolved` |
| Candidate-upstream records | 6 | `items.json` `authorship: candidate_upstream` |
| Prompts and personas (04-system-prompts) | 18 | `04-system-prompts/` (`core/` 5, `personas/` 10, `upscale/` 3) |
| Agent instructions (05-agent-instructions) | 10 modules + 9 profiles | `05-agent-instructions/` |

## Reconciliation Summary

- **Original catalog records**: 154 (Odysseus-derived list, preserved as the 154
  URLs under `03-third-party-skills/odysseus/` and in `categories/skills.json`)
- **Current records**: 184 rows in `items.json` and `items.csv`
  (1 original + 18 third-party local + 136 link-only + 6 candidate-upstream + 23 unresolved)
- **Promoted to local copies**: 18 records now have a local `SKILL.md`
  (`categories/skills.json` ids = the 136 link-only ids plus those 18)
- **Link-only records**: 136 (`items.json`); the Odysseus URL list holds 154
- **Unresolved inventory**: 23 (`items.json`); `unresolved-sources.json` tracks a
  wider scope of 28 (22 custom-or-unverified + 6 candidate-upstream) — see
  `unresolved.md` for the scope definitions
- **Exclusions**: None — all original records mapped

## Categories

See `categories/` for topic-based organization:
- animation, browser, coding, community, documents, frontend, knowledge, learning, omniroute, planning, platforms-and-tools, reverse-engineering, specialists, thinking, workflow

## Presets

See `presets/` for workflow-specific skill bundles:
- coding, debugging, documents, engineering-3d, frontend, investing, local-ai-infra, planning, research-learning