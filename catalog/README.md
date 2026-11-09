# Skills Catalog

Canonical structured catalog of this collection.

## Contents

- `items.json` - 224 records: 25 original skills and 199 external skills.
  Each record includes name, category, repository, upstream URL, authorship,
  license and verification status.
- `links/` - authoritative plain URL lists for external skills.
  - `skill-links.txt` - 157 stable-branch links.
  - `pinned-links.txt` - 42 pinned commit/release links.
  - `README.md` - provenance and verification note.

External skills are listed by name and link only; their code is not stored
here. Seven reverse-engineering skills are additionally bundled as local copies
under `skills/third-party/` (from `zhaoxuya520/reverse-skill` and `morluto/rea`)
and are tracked separately from the link catalog.

## Authority

Exactly one authoritative input per section of `docs/CATEGORY_INDEX.md`:

| Section | Authoritative input |
|---------|---------------------|
| Original local skills | `skills/original/**/SKILL.md` |
| External skills (links only) | `catalog/links/skill-links.txt` + `pinned-links.txt` |
| Structured metadata | `catalog/items.json` |

The index generator treats a missing or malformed authoritative input as an
error. It never falls back to an empty collection.

## Counts

| Authorship | Count |
|------------|-------|
| `original` | 25 |
| `link-only` | 199 |
| **Total** | **224** |

The 199 link-only records cover the stable and pinned link files. The catalog
contains 224 records: 25 original and 199 external link-only. Seven
reverse-engineering skills are additionally bundled as local copies under
`skills/third-party/` and are tracked separately from the link catalog.

## Link Verification

All 199 external URLs returned HTTP 200: 188 were verified on 2026-11-05 and
the 11 day-trader links on 2026-11-06. The check covers URL availability only.
It does not verify upstream content, license, security or runtime compatibility.

## Adding an External Skill

1. Add the direct raw URL to `catalog/links/skill-links.txt` (stable branch) or
   `catalog/links/pinned-links.txt` (pinned commit or release branch).
2. Add a matching record to `items.json`.
3. Run `python scripts/update-category-index.py`.
4. Run `python scripts/validate-frontmatter.py` and the tooling tests.
