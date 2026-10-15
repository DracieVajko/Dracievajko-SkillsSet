# Third-Party Skills â€” Agent Harnesses Branch

Local copies of unmodified third-party skills for agent harnesses
(OpenCode, Claude Code, VS Code, and similar). Each skill folder contains:

- `SKILL.md` â€” the skill definition
- `SOURCE.md` â€” provenance, license evidence, verification status

## Skills Included (14)

| Skill | Upstream repository | Branch | License | License evidence |
|-------|---------------------|--------|---------|------------------|
| blender-geometry-nodes | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| blender-hard-surface-modeling | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| blender-python-integration | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| blender-rigging-animation | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| frontend-design-systems | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| idea-to-plan | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| brainstorming | obra/superpowers | main | MIT | LICENSE file verified |
| using-superpowers | obra/superpowers | main | MIT | LICENSE file verified |
| code-documenter | Jeffallan/claude-skills | main | MIT | LICENSE file verified |
| code-reviewer | Jeffallan/claude-skills | main | MIT | LICENSE file verified |
| debugging-wizard | Jeffallan/claude-skills | main | MIT | LICENSE file verified |
| fine-tuning-expert | Jeffallan/claude-skills | main | MIT | LICENSE file verified |
| wordpress-pro | Jeffallan/claude-skills | main | MIT | LICENSE file verified |
| context-engineering | addyosmani/agent-skills | main | MIT | LICENSE file verified |

## Excluded â€” Redistribution Terms Unresolved (3)

The following copies were removed from this public-ready branch and preserved
outside the publication tree, because the upstream source grants no
established license and no LICENSE file exists:

| Skill | Upstream | Preserved location |
|-------|----------|--------------------|
| applying-themes (was theme-factory) | anthropics/skills | `_private-review/excluded-third-party-redistribution/anthropics-skills/` |
| building-mcp-servers (was mcp-builder) | anthropics/skills | same |
| creating-skills (was skill-creator) | anthropics/skills | same |

`anthropics/skills` reports no license (GitHub API `license: NONE`), has no
LICENSE file, and its `README.md` contains no license terms. Its individual
upstream `SKILL.md` files reference `LICENSE.txt`, which does not exist in the
repository. Redistribution terms are therefore unresolved.

## License Notes

- A `SOURCE.md` documents provenance; it does **not** by itself grant or prove
  redistribution permission.
- The license column records evidence actually checked on 2026-10-15:
  - "LICENSE file verified" = a LICENSE file was fetched from the upstream repo
    and read (MIT).
  - "Declared in repo README" = the repository README states `## License` / `MIT`
    but contains no LICENSE file. Treated as MIT per the repository's declaration.
- Do not assume a local `license: MIT` frontmatter field is authoritative.

## Installation

These folders use an archive/library layout, not a native discovery path.
To use a skill with a harness, copy the skill folder into that harness's
skill discovery directory, for example:

- OpenCode: `~/.config/opencode/skills/<skill>/SKILL.md`
- Claude Code: `~/.claude/skills/<skill>/SKILL.md`
- VS Code / other: the extension's configured skills directory

Review a skill's dependencies and sidecar files before activating it.

## Verification

All 14 files were fetched successfully (HTTP 200, Markdown content) on
2026-10-15. See `../../docs/VERIFICATION.md`.

