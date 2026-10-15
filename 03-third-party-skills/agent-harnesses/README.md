# Third-Party Skills — Agent Harnesses Branch

Local copies of unmodified third-party skills for agent harnesses
(OpenCode, Claude Code, VS Code, and similar). Each skill folder contains:

- `SKILL.md` — the skill definition
- `SOURCE.md` — provenance, license evidence, verification status

## Skills Included (17)

| Skill | Upstream repository | Branch | License | License evidence |
|-------|---------------------|--------|---------|------------------|
| applying-themes | anthropics/skills | main | Apache-2.0 | Per-skill `LICENSE.txt` (Copyright 2026 Anthropic, PBC) |
| blender-geometry-nodes | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| blender-hard-surface-modeling | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| blender-python-integration | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| blender-rigging-animation | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| brainstorming | obra/superpowers | main | MIT | Root LICENSE file verified |
| building-mcp-servers | anthropics/skills | main | Apache-2.0 | Per-skill `LICENSE.txt` (Copyright 2026 Anthropic, PBC) |
| code-documenter | Jeffallan/claude-skills | main | MIT | Root LICENSE file verified |
| code-reviewer | Jeffallan/claude-skills | main | MIT | Root LICENSE file verified |
| context-engineering | addyosmani/agent-skills | main | MIT | Root LICENSE file verified |
| creating-skills | anthropics/skills | main | Apache-2.0 | Per-skill `LICENSE.txt` (Copyright 2026 Anthropic, PBC) |
| debugging-wizard | Jeffallan/claude-skills | main | MIT | Root LICENSE file verified |
| fine-tuning-expert | Jeffallan/claude-skills | main | MIT | Root LICENSE file verified |
| frontend-design-systems | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| idea-to-plan | composio-community/opencode-skills | master | MIT | Declared in repo README (no LICENSE file) |
| using-superpowers | obra/superpowers | main | MIT | Root LICENSE file verified |
| wordpress-pro | Jeffallan/claude-skills | main | MIT | Root LICENSE file verified |

`applying-themes`, `building-mcp-servers` and `creating-skills` were renamed
locally from `theme-factory`, `mcp-builder` and `skill-creator`; the instruction
bodies are unchanged.

## License Notes

- A `SOURCE.md` documents provenance; it does **not** by itself grant or prove
  redistribution permission.
- The license column records evidence actually checked on 2026-10-15:
  - "Root LICENSE file verified" = a LICENSE file was fetched from the upstream
    repository root and read (MIT).
  - "Per-skill `LICENSE.txt`" = the upstream skill folder ships its own
    `LICENSE.txt` (Apache-2.0, Copyright 2026 Anthropic, PBC).
  - "Declared in repo README" = the repository README states `## License` / `MIT`
    but contains no LICENSE file. Recorded as declared, not as a verified file.
- Do not assume a local `license:` frontmatter field is authoritative.

## Installation

These folders use an archive/library layout; this branch is not itself a skill
discovery directory. To use one skill:

1. Read that skill's `SKILL.md` and `SOURCE.md` (dependencies, sidecar files and
   license).
2. Copy only that skill folder into the skill discovery directory of your
   harness. Discovery locations differ per tool and per version — check the
   harness's own documentation rather than assuming a path.
3. Do not copy this `agent-harnesses/` branch (or this README) into a discovery
   directory; doing so can import unrelated files or overwrite existing skills.
4. Some skills need additional components — scripts, reference files, runtimes or
   MCP servers. Installing those is separate from copying the folder; follow the
   skill's `SKILL.md`.

## Verification

On 2026-10-15 the upstream raw `SKILL.md` for each of the 17 skills was fetched
successfully (HTTP 200, Markdown content) and each upstream license was checked.
See `../../docs/VERIFICATION.md` and the `SOURCE.md` inside each skill folder.
