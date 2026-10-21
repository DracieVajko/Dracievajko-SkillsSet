# Skills Catalog

Canonical structured catalog of this collection.

## Contents

- `items.json` - 157 records: 3 original skills and 154 external skills.
  Each record includes name, category, repository, upstream URL, authorship,
  license and verification status.
- `links/` - authoritative plain URL lists for external skills.
  - `skill-links.txt` - 142 stable-branch links.
  - `pinned-links.txt` - 12 release-branch links.
  - `README.md` - provenance and verification note.

No third-party skill code is stored in this repository. External skills are
listed by name and link only.

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
| `original` | 2 |
| `link-only` | 154 |
| **Total** | **156** |

The 154 link-only records cover the 142 stable links and 12 pinned links. The
catalog contains only the two original skills and 154 external link-only
records; no third-party code is stored locally.

## Link Verification

All 154 external URLs returned HTTP 200 on 2026-10-20. The check covers URL
availability only. It does not verify upstream content, license, security or
runtime compatibility.

## Adding an External Skill

1. Add the direct raw URL to `catalog/links/skill-links.txt` (stable branch) or
   `catalog/links/pinned-links.txt` (pinned release branch).
2. Add a matching record to `items.json`.
3. Run `python scripts/update-category-index.py`.
4. Run `python scripts/validate-frontmatter.py` and the tooling tests.
