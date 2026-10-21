# Skills

This directory separates what this repository authors from what it
references. Two kinds live here, always clearly labeled:

- `original/` - skills authored and maintained in this repository (**4**)
- `third-party/` - upstream skills referenced by link only (**154**). No
  upstream code is bundled; see [`third-party/README.md`](third-party/README.md).

## Original Skills (authored by DracieVajko)

These are the skills written and versioned in this repository. To use one,
copy its folder into your agent's skill directory.

| Skill | Purpose | Path |
|-------|---------|------|
| `ticktick-tasks` | Manage TickTick tasks, projects, habits and focus via MCP | [`SKILL.md`](original/ticktick-tasks/SKILL.md) |
| `write-research-projects` | Deep research, academic writing, source verification and complex projects | [`SKILL.md`](original/write-research-projects/SKILL.md) |
| `pen-testing` | Authorized penetration testing methodology: scope gate, recon, scan, controlled testing, blast radius, report | [`SKILL.md`](original/pen-testing/SKILL.md) |
| `agent-operating-rules` | Evidence-first project workflow: consent-gated git, root-cause fixes, verification, coverage checklists and test discipline | [`SKILL.md`](original/agent-operating-rules/SKILL.md) |

Install example (OpenCode):

```bash
cp -r skills/original/pen-testing ~/.config/opencode/skills/
```

## Third-Party Skills (links only)

154 upstream skills are referenced by URL only. Their content is never
copied here, so licenses and provenance stay with the upstream owners.

- Curated list with purpose and license: [`third-party/README.md`](third-party/README.md)
- Complete generated list: [`docs/CATEGORY_INDEX.md`](../docs/CATEGORY_INDEX.md)
- Raw URL lists: [`catalog/links/`](../catalog/links/)
- Safety notes before installing external skills: [`docs/SAFETY-AND-LICENSES.md`](../docs/SAFETY-AND-LICENSES.md)

A link is not a license grant; check the upstream license before reusing
external content.

## Find Skills by Platform

| Platform | How it consumes this collection |
|----------|--------------------------------|
| OpenCode | Copy an original skill folder to `.agents/skills/` (project) or `~/.config/opencode/skills/` (user) |
| Odysseus | Read `catalog/links/skill-links.txt` and `catalog/links/pinned-links.txt` directly |
| VS Code / other agents | Use `prompts/system/*.md` as custom instructions and `instructions/modules/*.md` as domain rules |

The machine-readable catalog for every skill (original and link-only) is
[`catalog/items.json`](../catalog/items.json).
