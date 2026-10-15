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

## Catalog Statistics

| Category | Count |
|----------|-------|
| Original local skills (01-my-skills) | 1 |
| Modified local skills (02-my-modified-skills) | 0 |
| Unmodified third-party local skills (03-third-party-skills/agent-harnesses) | 17 |
| Third-party link-only resources (03-third-party-skills/odysseus) | 158 |
| Prompts and personas (04-system-prompts) | 17 |
| Agent instructions (05-agent-instructions) | 10 modules + 9 profiles |
| Unresolved inventory records | 24 |

## Reconciliation Summary

- **Original catalog records**: 154
- **Retained current records**: 17 (local) + 158 (link-only) = 175
- **Merged records**: Multiple entries from same upstream repo consolidated
- **Link-only records**: 158 (Odysseus branch)
- **Unresolved records**: 24 (planned/custom items)
- **Exclusions**: None — all original records mapped

## Categories

See `categories/` for topic-based organization:
- animation, browser, coding, community, documents, frontend, knowledge, learning, omniroute, planning, platforms-and-tools, reverse-engineering, specialists, thinking, workflow

## Presets

See `presets/` for workflow-specific skill bundles:
- coding, debugging, documents, engineering-3d, frontend, investing, local-ai-infra, planning, research-learning