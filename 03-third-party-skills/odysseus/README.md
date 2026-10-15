# Third-Party Skills — Odysseus Branch (Link-Only)

This branch references **unmodified third-party Odysseus skills by upstream
link only**. Their implementations are **not** bundled here.

- `skill-links.txt` — one complete raw Markdown URL per line. Stable-branch
  sources. No headings, descriptions, bullets, tags, or comments inside.
- `unverified-links.txt` — candidate URLs whose branch/path stability is
  uncertain (pinned to a release branch). Same plain one-URL-per-line format.

## Counts (from actual files, 2026-10-15)

| File | URLs | Note |
|------|------|------|
| `skill-links.txt` | 142 | Stable `main`/`master` branch sources |
| `unverified-links.txt` | 12 | `diegosouzapw/OmniRoute` pinned to `release/v3.8.52` |
| **Total unique** | **154** | No overlap between the two files |

## Verification Status (2026-10-15)

All 154 unique URLs were fetched:

| Check | Result |
|-------|--------|
| HTTP status | 200 for all 154 |
| Content-Type | `text/plain; charset=utf-8` for all 154 |
| Content shape | Markdown with frontmatter for all 154 |

Status taxonomy used:

- **HTTP verified** — fetched successfully with real Markdown content. Applies
  to all 142 `skill-links.txt` URLs.
- **Branch/path uncertain** — HTTP verified now, but the URL is pinned to a
  release branch that may move or be deleted. Applies to the 12 OmniRoute URLs
  in `unverified-links.txt`; they are kept separate for this reason, not
  because they are unchecked.
- **catalog-derived, unchecked** — derived from the original catalog without an
  HTTP check. None remain in these files after the 2026-10-15 pass.

This verifies reachability and content type at a point in time. It does **not**
guarantee the URLs remain available, and it does **not** grant redistribution
rights.

## Sources by repository (`skill-links.txt`, 142)

| Repository | Links |
|------------|-------|
| tjboudreaux/cc-thinking-skills | 28 |
| addyosmani/agent-skills | 25 |
| mattpocock/skills | 16 |
| obra/superpowers | 15 |
| Jeffallan/claude-skills | 14 |
| composio-community/opencode-skills | 13 |
| anthropics/skills | 11 |
| greensock/gsap-skills | 8 |
| Jakubantalik/transitions.dev | 3 |
| DietrichGebert/ponytail | 1 |
| Graphify-Labs/graphify | 1 |
| jakubkrehel/make-interfaces-feel-better | 1 |
| lackeyjb/playwright-skill | 1 |
| morluto/rea | 1 |
| multica-ai/andrej-karpathy-skills | 1 |
| nextlevelbuilder/ui-ux-pro-max-skill | 1 |
| pbakaus/impeccable | 1 |
| vercel-labs/agent-browser | 1 |

`unverified-links.txt` (12): `diegosouzapw/OmniRoute`.

## Notes

- Link-only references carry no redistribution obligation for the linked
  content; they point to the upstream file and do not copy it.
- Dependencies and limitations are documented here, not inside the plain
  link files.
