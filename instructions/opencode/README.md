# OpenCode

## Modular Variant

Copy the contents of `project-template/` into the root of your project. The
template `AGENTS.md` loads the relevant file from `agent-rules/` on demand.

## Single-File Variant

Use [`AGENTS-combined.md`](../../AGENTS-combined.md) as the project `AGENTS.md`.
Do not use it together with the full modular rule set.

The files in `project-template/agent-rules/` are self-contained copies of
`instructions/modules/`. Keep them in sync when the rules change.

## Skills

This repository bundles three original skills under `skills/original/`:

- [`ticktick-tasks`](../../skills/original/ticktick-tasks/SKILL.md) - manage
  TickTick tasks, projects, habits and focus via MCP
- [`write-research-projects`](../../skills/original/write-research-projects/SKILL.md) -
  deep research, academic writing, source verification and complex projects
- [`pen-testing`](../../skills/original/pen-testing/SKILL.md) - authorized
  penetration testing methodology: scope gate, recon, scan, controlled
  testing, blast radius, report

External skills are links only; use the catalog and the generated index:

- [`catalog/links/`](../../catalog/links/)
- [`docs/CATEGORY_INDEX.md`](../../docs/CATEGORY_INDEX.md)
- [`skills/third-party/README.md`](../../skills/third-party/README.md)

No upstream skill implementation is installed by this repository. If you want to
use an external skill, install it from its original repository and keep the
complete upstream folder, including dependencies. Do not install different
skills with the same `name` without resolving the collision.

Official documentation:

- https://opencode.ai/docs/skills/
- https://opencode.ai/docs/rules/
- https://code.visualstudio.com/docs/copilot/customization/agent-skills
