# Package Verification

Created/revised 2026-10-15.

## Verified (HTTP fetch + content shape)
- Unique URLs: 154 (142 in skill-links.txt, 12 in unverified-links.txt)
- HTTP status: 200 for all 154
- Content-Type: text/plain; charset=utf-8 for all 154
- Markdown with frontmatter: yes for all 154 (spot-checked samples confirmed)

## License verification
- anthropics/skills: Apache License 2.0 per-skill LICENSE.txt (verified by fetching theme-factory/mcp-builder/skill-creator LICENSE.txt)
- composio-community/opencode-skills: MIT declared in repository README (no LICENSE file)
- obra/superpowers: MIT (root LICENSE verified)
- Jeffallan/claude-skills: MIT (root LICENSE verified)
- addyosmani/agent-skills: MIT (root LICENSE verified)

## Catalog
- Reconciliation CSV/JSON consistent after local_skill_path updates; no empty directories created to force examples.
- Persona names corrected per Arcane identities.

## File integrity
- All referenced files exist; total prompt/persona files: 18 (9 personas + 1 expanded variant + 5 core + 3 image).

## Notes
- OmniRoute URLs (12) are HTTP-verified but pinned to release branch (branch/path uncertain); retained in unverified-links.txt per layout.
- SOURCE.md documents provenance; it does not prove redistribution permission.
- This is a point-in-time snapshot; upstream branches may evolve.
