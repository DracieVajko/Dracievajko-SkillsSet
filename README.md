# Dracievajko AI Agent Collection

[![CI](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml/badge.svg)](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A personal collection of agent skills, system prompts, personas, agent rules and
supporting resources for OpenCode, Odysseus, VS Code and compatible agent
frameworks.

## Quick Navigation

| Looking for | Where |
|-------------|-------|
| **My skills (4, original)** | [`skills/original/`](skills/original) - details in the [Original Skills](#original-skills) table below |
| **Third-party skills (154, links only)** | [`skills/third-party/README.md`](skills/third-party/README.md) or the complete [category index](docs/CATEGORY_INDEX.md) |
| **Machine-readable catalog** | [`catalog/items.json`](catalog/items.json) |
| **Platform usage (OpenCode / Odysseus / VS Code)** | [Quick Start](#quick-start) below |

## What Is in the Repository

- **4 original skills** - `ticktick-tasks`, `write-research-projects`, `pen-testing`, `agent-operating-rules`
- **154 external skills** - links to original upstream files only; no third-party
  code is bundled
- **7 system prompts**, **10 personas** and **3 image prompts**
- **9 modular rule files** and **9 specialized agent profiles**
- **OpenCode integration** - modular project template and single-file rules
- **Catalog and tooling** - machine-readable metadata, link lists, validation and CI

There are no local copies of third-party skills, no archives, no backups and no
historical catalog views in this repository.

## Repository Structure

```text
.
├── .github/workflows/          # CI: tests, frontmatter validation, index check
├── catalog/
│   ├── README.md
│   ├── items.json              # 158 records: 4 original + 154 external links
│   └── links/
│       ├── README.md
│       ├── skill-links.txt     # 142 stable-branch links
│       └── pinned-links.txt    # 12 pinned release links
├── docs/
│   ├── CATEGORY_INDEX.md       # Generated list of original + external skills
│   ├── CONTRIBUTING.md
│   ├── SAFETY-AND-LICENSES.md
│   ├── SKILL_SPEC.md
│   └── templates/              # Project, plan, decisions, handoff, sources
├── instructions/
│   ├── modules/                # 9 domain rule modules
│   ├── profiles/               # 9 specialized agent profiles
│   └── opencode/               # OpenCode README + modular project template
├── prompts/
│   ├── system/                 # 7 system prompts
│   ├── personas/               # 10 personas
│   └── image/                  # 3 image prompts
├── scripts/                    # Validator, index generator, tests
├── skills/
│   ├── README.md
│   ├── original/               # 4 original skills
│   └── third-party/README.md   # External skills: name, purpose, link
├── AGENTS.md                   # Modular entry point
├── AGENTS-combined.md          # Single-file rules variant
├── ATTRIBUTION.md
├── LICENSE
└── README.md
```

## Quick Start

### OpenCode

Copy an original skill into a supported discovery directory:

```bash
# Project-local
cp -r skills/original/write-research-projects .agents/skills/

# User-level
cp -r skills/original/write-research-projects ~/.config/opencode/skills/
```

For project rules, copy `instructions/opencode/project-template/` into the
project root. For a single-file variant, use `AGENTS-combined.md`.

### External Skills

External skills are not installed or copied by this repository. Use the links to
open the original files:

- [Complete list - `docs/CATEGORY_INDEX.md`](docs/CATEGORY_INDEX.md)
- [Curated list with purpose and license - `skills/third-party/README.md`](skills/third-party/README.md)
- [Raw URL lists - `catalog/links/`](catalog/links/)

All 154 URLs returned HTTP 200 on 2026-10-20. Availability does not imply
license, security or runtime compatibility.

### Odysseus

Odysseus can consume the plain URL lists directly:

```bash
cat catalog/links/skill-links.txt
cat catalog/links/pinned-links.txt
```

### VS Code and Other Agents

- Use `prompts/system/*.md` as custom instructions.
- Use `prompts/personas/*.md` as chat modes or role definitions.
- Reference `instructions/modules/*.md` for domain-specific rules.

## Original Skills

| Skill | Purpose | Path |
|-------|---------|------|
| `ticktick-tasks` | Manage TickTick tasks, projects, tags, habits and focus via MCP | [`SKILL.md`](skills/original/ticktick-tasks/SKILL.md) |
| `write-research-projects` | Deep research, academic writing, source verification and complex projects | [`SKILL.md`](skills/original/write-research-projects/SKILL.md) |
| `pen-testing` | Authorized penetration testing methodology: scope, recon, scan, controlled testing, blast radius and report | [`SKILL.md`](skills/original/pen-testing/SKILL.md) |
| `agent-operating-rules` | Evidence-first project workflow: consent-gated git, verification, coverage checklists and test discipline | [`SKILL.md`](skills/original/agent-operating-rules/SKILL.md) |

The research skill has two companion system prompts:

- [`deep-research-writing-long.md`](prompts/system/deep-research-writing-long.md) - self-contained long prompt
- [`deep-research-writing-short.md`](prompts/system/deep-research-writing-short.md) - compact prompt (under 1500 characters)

## External Skills

The collection references 154 upstream skills:

- 142 stable-branch links in `catalog/links/skill-links.txt`
- 12 pinned release links in `catalog/links/pinned-links.txt`

No upstream implementation is stored here. The 17 upstream skills that were
previously bundled locally are now link-only; see
[`skills/third-party/README.md`](skills/third-party/README.md) for their name,
purpose, license and original link.

## System Prompts

| Prompt | Purpose |
|--------|---------|
| [`general.md`](prompts/system/general.md) | General expert consultant behaviour |
| [`coding.md`](prompts/system/coding.md) | Concise coding assistant |
| [`cad.md`](prompts/system/cad.md) | 3D printing copywriter (VoxelScribe) |
| [`trading.md`](prompts/system/trading.md) | Algorithmic trading |
| [`deep-research-writing-long.md`](prompts/system/deep-research-writing-long.md) | Deep research, academic writing and complex projects |
| [`deep-research-writing-short.md`](prompts/system/deep-research-writing-short.md) | Short companion prompt |
| [`repository-hygiene.md`](prompts/system/repository-hygiene.md) | Repository cleanup and Git hygiene |

## Personas

| Persona | Role | Best For |
|---------|------|----------|
| `jayce-generalist` | Versatile expert | General problem-solving |
| `jayce-generalist-expanded` | Multidisciplinary generalist | Broad tasks needing a wider brief |
| `bruno-coder` | Senior software engineer | Implementation, debugging, review |
| `atlas-architect` | Systems architect | Architecture and trade-off analysis |
| `elias-writer` | Technical writer | Documentation, rewriting, clarity |
| `adrian-investor` | Chief Investment Officer | Investment analysis and portfolio decisions |
| `orion-researcher` | Research analyst | Deep research and evidence synthesis |
| `victor-thinker` | Strategic challenger | Stress-testing ideas and blind spots |
| `marcus-advisor` | Decision advisor | Trade-off analysis and recommendations |
| `jericho-chef` | Personal chef | Recipe discovery and meal planning |

## Agent Rules and Profiles

- `instructions/modules/` - nine domain rule files: coding, debugging, planning,
  frontend, documents, research and learning, local AI infrastructure,
  investing, and engineering/3D.
- `instructions/profiles/` - nine preconfigured profiles for specialized agents.
- `instructions/opencode/` - OpenCode integration and a self-contained project
  template.

`AGENTS.md` is the modular entry point and loads rule files on demand.
`AGENTS-combined.md` is the single-file alternative with all rules inlined. Do
not use both in the same project.

## Catalog

| File | Purpose |
|------|---------|
| [`catalog/items.json`](catalog/items.json) | 158 structured records: 4 original + 154 external links |
| [`catalog/links/skill-links.txt`](catalog/links/skill-links.txt) | 142 stable upstream URLs |
| [`catalog/links/pinned-links.txt`](catalog/links/pinned-links.txt) | 12 pinned upstream URLs |
| [`docs/CATEGORY_INDEX.md`](docs/CATEGORY_INDEX.md) | Generated human-readable skill index |

## Validation

```bash
python scripts/validate-frontmatter.py
python scripts/update-category-index.py
python scripts/update-category-index.py --check
python -m unittest discover -s scripts -p "test_*.py"
```

CI runs the same checks on every push and pull request in
`.github/workflows/skills-tooling.yml`.

## Licensing

The root [MIT license](LICENSE) applies to original content authored by the
collection maintainer. External skills are links only; their licenses remain
with their upstream authors. See [ATTRIBUTION.md](ATTRIBUTION.md).

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for adding original skills or
external links, and [docs/SKILL_SPEC.md](docs/SKILL_SPEC.md) for the skill format.

## Related Repositories

- [OpenCode](https://github.com/anomalyco/opencode)
- [Superpowers](https://github.com/obra/superpowers)
- [Odysseus](https://github.com/DracieVajko/odysseus)

---

Maintained by [@DracieVajko](https://github.com/DracieVajko).
