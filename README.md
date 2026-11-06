# Dracievajko AI Agent Collection

[![CI](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml/badge.svg)](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A personal collection of agent skills, system prompts, personas, agent rules and
supporting resources for OpenCode, Odysseus, VS Code and compatible agent
frameworks.

## Quick Navigation

| Looking for | Where |
|-------------|-------|
| **My skills (5, original)** | [`skills/original/`](skills/original) - details in the [Original Skills](#original-skills) table below |
| **Third-party skills (199, links only)** | [`skills/third-party/README.md`](skills/third-party/README.md) or the complete [category index](docs/CATEGORY_INDEX.md) |
| **Machine-readable catalog** | [`catalog/items.json`](catalog/items.json) |
| **Platform usage (OpenCode / Odysseus / VS Code)** | [Quick Start](#quick-start) below |

## What Is in the Repository

- **25 original skills** - `ticktick-tasks`, `write-research-projects`, `pen-testing`, `agent-operating-rules`, `repository-hygiene`, `focus-my-energy`, `generate-fresh-ideas`, `get-more-perspectives`, `match-my-writing-style`, `prep-for-meetings`, `beyond-vibe-coding-autonomous-development`, `document-editing-general`, `github-code-documentation`, `penetration-testing-guide`, `generate-markdown-and-docx-documents`, `create-individual-calendar-events-from-earnings-dates-list`, `ds-note-formatter`, `fix-inconclusive-skills`, `generate-findings-report-from-pipeline-logs`, `testing-skills`, `yfinance-ai`, `book-to-skill`, `universal-listing-template`, `enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras`, `detailed-source-rewrite-guide`
- **199 external skills** - links to original upstream files only; no third-party
  code is bundled
- **7 system prompts**, **10 personas** and **3 image prompts**
- **11 modular rule files** and **9 specialized agent profiles**
- **OpenCode integration** - modular project template and single-file rules
- **Catalog and tooling** - machine-readable metadata, link lists, validation and CI

There are no local copies of third-party skills, no archives, no backups and no
historical catalog views in this repository.

## Repository Structure

```text
.
├── .github/workflows/          # CI: tests, sync, frontmatter validation, index check
├── catalog/
│   ├── README.md
│   ├── items.json              # 224 records: 25 original + 199 external links
│   └── links/
│       ├── README.md
│       ├── skill-links.txt     # 157 stable-branch links
│       └── pinned-links.txt    # 42 pinned commit/release links
├── docs/
│   ├── CATEGORY_INDEX.md       # Generated list of original + external skills
│   ├── CONTRIBUTING.md
│   ├── SAFETY-AND-LICENSES.md
│   ├── SKILL_SPEC.md
│   └── templates/              # Project, plan, decisions, handoff, sources
├── instructions/
│   ├── modules/                # 11 domain rule modules
│   ├── profiles/               # 9 specialized agent profiles
│   └── opencode/               # OpenCode README + modular project template
├── prompts/
│   ├── system/                 # 7 system prompts
│   ├── personas/               # 10 personas
│   └── image/                  # 3 image prompts
├── scripts/                    # Validator, sync check, index generator, link checker, installers, tests
├── skills/
│   ├── README.md
│   ├── original/               # 25 original skills
│   └── third-party/README.md   # External skills: name, purpose, link
├── AGENTS.md                   # Modular entry point
├── AGENTS-combined.md          # Single-file rules variant
├── ATTRIBUTION.md
├── LICENSE
└── README.md
```

## Quick Start

### OpenCode

Install all original skills into the user-level OpenCode directory:

```powershell
# Windows
.\scripts\install-skills.ps1
```

```bash
# Linux / macOS
./scripts/install-skills.sh
```

Both scripts back up an existing skill folder before replacing it. For a manual
install, copy the folders you need:

```bash
# Project-local
cp -r skills/original/* .agents/skills/

# User-level
cp -r skills/original/* ~/.config/opencode/skills/
```

For project rules, copy `instructions/opencode/project-template/` into the
project root. For a single-file variant, use `AGENTS-combined.md`.

### External Skills

External skills are not installed or copied by this repository. Use the links to
open the original files:

- [Complete list - `docs/CATEGORY_INDEX.md`](docs/CATEGORY_INDEX.md)
- [Curated list with purpose and license - `skills/third-party/README.md`](skills/third-party/README.md)
- [Raw URL lists - `catalog/links/`](catalog/links/)

All 199 URLs returned HTTP 200: 188 were verified on 2026-11-05 and the 11
day-trader links on 2026-11-06. Availability does not imply license, security
or runtime compatibility.

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
| `repository-hygiene` | Repository cleanup: classification, temporary files, generated artifacts, secrets and commit preparation | [`SKILL.md`](skills/original/repository-hygiene/SKILL.md) |
| `beyond-vibe-coding-autonomous-development` | Practical skill for AI-era software development based on Addy Osmani's 'Beyond Vibe Coding' — intent-driven workflows, prompt engineering, the 70% problem, code review/refinement, AI prototyping, autonomous agents, and production-ready AI-assisted engineering. | [`SKILL.md`](skills/original/beyond-vibe-coding-autonomous-development/SKILL.md) |
| `document-editing-general` | General-purpose skill for creating, reading, editing and managing documents (markdown, text, code, etc.) in an editor panel. | [`SKILL.md`](skills/original/document-editing-general/SKILL.md) |
| `github-code-documentation` | Skill for creating detailed descriptions and high-quality README.md files for scripts and programs intended for GitHub upload, push and commit. Includes coding and 'vibe-coding' rules to maximize efficiency and minimize errors. | [`SKILL.md`](skills/original/github-code-documentation/SKILL.md) |
| `penetration-testing-guide` | Penetration testing guide and methodology covering 5 phases: Recon, Scan, Gain Access, Escalate and Report. | [`SKILL.md`](skills/original/penetration-testing-guide/SKILL.md) |
| `generate-markdown-and-docx-documents` | Create a new document from a user-provided outline and content, output both a Markdown file and a Word (DOCX) file for download. | [`SKILL.md`](skills/original/generate-markdown-and-docx-documents/SKILL.md) |
| `create-individual-calendar-events-from-earnings-dates-list` | Create individual calendar events from an earnings dates list, one event per ticker with company name and reminder. | [`SKILL.md`](skills/original/create-individual-calendar-events-from-earnings-dates-list/SKILL.md) |
| `ds-note-formatter` | Format content for Synology DS Note / Note Station so it pastes cleanly and preserves structure, readability and checklist usability. | [`SKILL.md`](skills/original/ds-note-formatter/SKILL.md) |
| `fix-inconclusive-skills` | Identify and fix skills marked as inconclusive due to missing tools or other issues. | [`SKILL.md`](skills/original/fix-inconclusive-skills/SKILL.md) |
| `generate-findings-report-from-pipeline-logs` | Verify that all expected sections and data are present in generated files by comparing logs and output artifacts, and summarize discrepancies. | [`SKILL.md`](skills/original/generate-findings-report-from-pipeline-logs/SKILL.md) |
| `testing-skills` | Test skills that enforce discipline, compliance and verification using pressure scenarios and rationalization tables. | [`SKILL.md`](skills/original/testing-skills/SKILL.md) |
| `yfinance-ai` | World-class AI-powered Yahoo Finance integration: 56+ tools for stocks, crypto, forex, commodities and ETFs. | [`SKILL.md`](skills/original/yfinance-ai/SKILL.md) |
| `book-to-skill` | Convert a book or article into a reusable skill using AI and web data. | [`SKILL.md`](skills/original/book-to-skill/SKILL.md) |
| `universal-listing-template` | Generate structured lists (TODO lists, inventory, tables) using AI and file operations. | [`SKILL.md`](skills/original/universal-listing-template/SKILL.md) |
| `enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras` | Enable Wake-on-LAN and auto-shutdown on network loss for Raspberry Pi. | [`SKILL.md`](skills/original/enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras/SKILL.md) |
| `detailed-source-rewrite-guide` | Rewrite a source document (e.g., article, research paper) into a structured, step-by-step guide using AI. | [`SKILL.md`](skills/original/detailed-source-rewrite-guide/SKILL.md) |
| `focus-my-energy` | Classify tasks by cognitive demand and recommend what to work on now based on energy level | [`SKILL.md`](skills/original/focus-my-energy/SKILL.md) |
| `generate-fresh-ideas` | Remix source material into five distinct creative content angles | [`SKILL.md`](skills/original/generate-fresh-ideas/SKILL.md) |
| `get-more-perspectives` | Stress-test decisions across a five-advisor panel | [`SKILL.md`](skills/original/get-more-perspectives/SKILL.md) |
| `match-my-writing-style` | Draft, reply or rewrite in the user's authentic voice from Gmail/Docs samples | [`SKILL.md`](skills/original/match-my-writing-style/SKILL.md) |
| `prep-for-meetings` | Pre-meeting brief and 30-second glance card from Workspace sources | [`SKILL.md`](skills/original/prep-for-meetings/SKILL.md) |

The research skill has two companion system prompts:

- [`deep-research-writing-long.md`](prompts/system/deep-research-writing-long.md) - self-contained long prompt
- [`deep-research-writing-short.md`](prompts/system/deep-research-writing-short.md) - compact prompt (under 1500 characters)

## External Skills

The collection references 199 upstream skills:

- 157 stable-branch links in `catalog/links/skill-links.txt`
- 42 pinned commit/release links in `catalog/links/pinned-links.txt`

The 30 curated skill links are pinned to upstream commit SHAs; the 12 OmniRoute
links remain pinned to its release branch.

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

- `instructions/modules/` - eleven domain rule files: coding, debugging,
  planning, frontend, documents, research and learning, local AI
  infrastructure, investing, engineering/3D, security, and testing.
- `instructions/profiles/` - nine preconfigured profiles for specialized agents.
- `instructions/opencode/` - OpenCode integration and a self-contained project
  template.

`AGENTS.md` is the modular entry point and loads rule files on demand.
`AGENTS-combined.md` is the single-file alternative with all rules inlined. Do
not use both in the same project.

## Catalog

| File | Purpose |
|------|---------|
| [`catalog/items.json`](catalog/items.json) | 224 structured records: 25 original + 199 external links |
| [`catalog/links/skill-links.txt`](catalog/links/skill-links.txt) | 157 stable upstream URLs |
| [`catalog/links/pinned-links.txt`](catalog/links/pinned-links.txt) | 42 pinned upstream URLs |
| [`docs/CATEGORY_INDEX.md`](docs/CATEGORY_INDEX.md) | Generated human-readable skill index |

## Validation

```bash
python scripts/validate-frontmatter.py
python scripts/check-sync.py
python scripts/update-category-index.py
python scripts/update-category-index.py --check
python -m unittest discover -s scripts -p "test_*.py"

# Optional: network check for external links
python scripts/check-links.py
```

CI runs the validation, sync, index and test checks on every push and pull
request in `.github/workflows/skills-tooling.yml`. A separate scheduled workflow
checks external link availability.

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
