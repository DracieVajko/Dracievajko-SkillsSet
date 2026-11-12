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

<!-- counts:start -->

| What | Count | Where |
|------|------:|-------|
| Catalog records | 224 | `catalog/items.json` |
| Catalog records with `authorship: original` | 25 |  |
| Catalog records with `authorship: link-only` | 199 |  |
| Stable-branch links | 157 | `catalog/links/skill-links.txt` |
| Pinned links | 42 | `catalog/links/pinned-links.txt` |
| Bundled third-party skills | 7 | `skills/third-party/` - local copies of upstream `SKILL.md` files |

<!-- counts:end -->

The link-only records cover the stable and the pinned link files. The
reverse-engineering skills that are bundled as local copies under
`skills/third-party/` are tracked separately from the link catalog and are not
part of the link-only count.

## Link Verification

All 199 external URLs returned HTTP 200 when checked on 2026-11-12. The check
covers URL availability only. It does not verify upstream content, license,
security or runtime compatibility.

## Adding an External Skill

1. Add the direct raw URL to `catalog/links/skill-links.txt` (stable branch) or
   `catalog/links/pinned-links.txt` (pinned commit or release branch).
2. Add a matching record to `items.json`.
3. Run `python scripts/update-category-index.py`.
4. Run `python scripts/validate-frontmatter.py` and the tooling tests.
