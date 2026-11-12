# Dracievajko AI Agent Collection

[![CI](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml/badge.svg)](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Sponsors](https://img.shields.io/github/sponsors/DracieVajko?style=for-the-badge&logo=github-sponsors&color=ea4aaa)](https://github.com/sponsors/DracieVajko)

A curated collection of reusable **AI agent skills, system prompts, personas,
agent rules and workflows** for OpenCode and compatible agent frameworks.

Everything is plain Markdown and Python. There is no runtime, no service and
no dependency you have to trust: you copy what you need, read it, and adapt
it.

## Quick Navigation

| Looking for | Go to |
|-------------|-------|
| What this repository is | [Introduction](#what-this-repository-is) |
| Exact contents and counts | [Repository contents](#repository-contents) |
| Install into OpenCode | [Quick Start](#quick-start) |
| Install somewhere else | [Other agent platforms](#other-agent-platforms) |
| The skills themselves | [Original skills](#original-skills) |
| Which skill for which task | [Skills by Task](#skills-by-task) |
| External and bundled skills | [Third-party skills](#third-party-skills) |
| Prompts and personas | [Prompts and personas](#prompts-and-personas) |
| Reusable agent rules | [Agent instructions](#agent-instructions) |
| Machine-readable metadata | [Catalog](#catalog) |
| Add or update a skill | [Contributing](#contributing) |
| Licensing and attribution | [Licensing and attribution](#licensing-and-attribution) |
| Full install guide and troubleshooting | [docs/INSTALL.md](docs/INSTALL.md) |
| Skill format specification | [docs/SKILL_SPEC.md](docs/SKILL_SPEC.md) |
| Open improvement backlog | [docs/SKILL-QUALITY-REVIEW.md](docs/SKILL-QUALITY-REVIEW.md) |

## What this repository is

Three kinds of content live here, and they are **never** the same category:

1. **Original content** - skills, prompts, personas, rules and tooling written
   and maintained here. MIT licensed.
2. **External skills referenced by URL** - upstream skills you can open and
   install yourself. No content is copied; their licenses stay with their
   authors.
3. **Third-party skills physically bundled** - a small, explicit set of
   upstream skills copied into `skills/third-party/`, each with its upstream
   copyright notice and license text preserved.

Read [docs/THIRD-PARTY-LICENSES.md](docs/THIRD-PARTY-LICENSES.md) before
copying anything from this repository into your own project.

## Repository contents

The numbers below are generated from `catalog/items.json` and the filesystem
by `scripts/update-category-index.py` - they are never maintained by hand.

<!-- counts:start -->

| What | Count | Where |
|------|------:|-------|
| Original skills | 25 | `skills/original/` - authored and maintained here |
| Bundled third-party skills | 7 | `skills/third-party/` - local copies of upstream `SKILL.md` files |
| External link-only skills | 199 | referenced by URL; no content copied |
| Stable-branch links | 157 | `catalog/links/skill-links.txt` |
| Pinned links | 42 | `catalog/links/pinned-links.txt` |
| Catalog records | 224 | `catalog/items.json` |
| System prompts | 8 | `prompts/system/` |
| Personas | 10 | `prompts/personas/` |
| Image prompts | 3 | `prompts/image/` |
| Instruction modules | 11 | `instructions/modules/` |
| Agent profiles | 9 | `instructions/profiles/` |

<!-- counts:end -->

### What you can install

| Content | Install it? | How |
|---------|-------------|-----|
| Original skills | Yes | `scripts/install-skills.ps1` / `scripts/install-skills.sh` |
| Bundled third-party skills | Optional | Copy the folder from `skills/third-party/` |
| External link-only skills | By reference | Open the upstream link and copy it yourself |
| System prompts, personas | Yes | Copy the Markdown file |
| Agent rules and profiles | Yes | Copy `AGENTS.md` + `instructions/`, or `AGENTS-combined.md` |
| Catalog and tooling | Yes | Read `catalog/`, run `scripts/` |

## Repository structure

```text
.
â”œâ”€â”€ .github/
â”‚   â”œâ”€â”€ FUNDING.yml              # GitHub Sponsors
â”‚   â”œâ”€â”€ ISSUE_TEMPLATE/          # bug report, feature request, skill submission
â”‚   â”œâ”€â”€ PULL_REQUEST_TEMPLATE.md
â”‚   â””â”€â”€ workflows/               # skills-tooling.yml, link-check.yml
â”œâ”€â”€ catalog/
â”‚   â”œâ”€â”€ items.json               # machine-readable catalog: every skill record
â”‚   â””â”€â”€ links/                   # authoritative URL lists (stable + pinned)
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ CATEGORY_INDEX.md        # generated index of every skill
â”‚   â”œâ”€â”€ CONTRIBUTING.md          # how to add or update content
â”‚   â”œâ”€â”€ INSTALL.md               # installation, updating, uninstalling, troubleshooting
â”‚   â”œâ”€â”€ SAFETY-AND-LICENSES.md   # safety notes and license boundaries
â”‚   â”œâ”€â”€ SKILL_SPEC.md            # the skill format specification
â”‚   â”œâ”€â”€ SKILL-QUALITY-REVIEW.md  # prioritized improvement backlog
â”‚   â”œâ”€â”€ THIRD-PARTY-LICENSES.md  # upstream licenses of bundled content
â”‚   â””â”€â”€ templates/               # project, plan, decisions, handoff, sources
â”œâ”€â”€ instructions/
â”‚   â”œâ”€â”€ modules/                 # domain rule modules
â”‚   â”œâ”€â”€ profiles/                # specialized agent profiles
â”‚   â””â”€â”€ opencode/                # OpenCode integration + project template
â”œâ”€â”€ prompts/
â”‚   â”œâ”€â”€ system/                  # system prompts
â”‚   â”œâ”€â”€ personas/                # chat personas
â”‚   â””â”€â”€ image/                   # image prompts
â”œâ”€â”€ scripts/                     # validators, index generator, link checker, installers, tests
â”œâ”€â”€ skills/
â”‚   â”œâ”€â”€ original/                # original skills, one folder each
â”‚   â””â”€â”€ third-party/             # bundled upstream copies + provenance
â”œâ”€â”€ AGENTS.md                    # modular rules entry point
â”œâ”€â”€ AGENTS-combined.md           # the same rules in one file
â”œâ”€â”€ ATTRIBUTION.md               # authorship and license summary
â”œâ”€â”€ LICENSE                      # MIT
â””â”€â”€ README.md
```

## Quick Start

```bash
git clone https://github.com/DracieVajko/Dracievajko-SkillsSet.git
cd Dracievajko-SkillsSet
```

### OpenCode installation

Install every original skill into your user-level skills directory:

```powershell
# Windows
.\scripts\install-skills.ps1
```

```bash
# Linux / macOS
./scripts/install-skills.sh
```

Preview first, install later:

```bash
./scripts/install-skills.sh --dry-run
```

Other options: `--target <dir>` to install elsewhere, `--uninstall` to remove
this collection's skills again. The installer backs up any folder it replaces
into `~/.config/opencode/skill-backups/<timestamp>/` - it never overwrites an
existing skill in place.

Full guide, including project-local installs, agent rules, updating,
uninstalling and troubleshooting: **[docs/INSTALL.md](docs/INSTALL.md)**.

### Other agent platforms

The skills use the `SKILL.md` frontmatter convention, so they load in any agent
that reads that format. Copy the folders you want into the directory your
agent expects:

```bash
# project-local, works for most agents
cp -r skills/original/* .agents/skills/
```

For agent rules, use the modular `AGENTS.md` plus `instructions/modules/`, or
the single-file `AGENTS-combined.md` - not both in the same project.

| You want | Use |
|----------|-----|
| Project rules for OpenCode | `instructions/opencode/project-template/` |
| A single rules file | `AGENTS-combined.md` |
| Modular rules | `AGENTS.md` + `instructions/modules/` |
| A specialist agent | `instructions/profiles/` |

## Original skills

| Skill | Purpose |
|-------|---------|
| [`ticktick-tasks](skills/original/ticktick-tasks/SKILL.md) | Manage TickTick tasks, projects, tags, habits and focus via MCP |
| [`write-research-projects](skills/original/write-research-projects/SKILL.md) | Deep research, academic writing, source verification and complex projects |
| [`pen-testing](skills/original/pen-testing/SKILL.md) | Authorized penetration testing methodology: scope, recon, scan, controlled testing, blast radius, report |
| [`penetration-testing-guide](skills/original/penetration-testing-guide/SKILL.md) | Penetration testing guide and methodology covering 5 phases |
| [`agent-operating-rules](skills/original/agent-operating-rules/SKILL.md) | Evidence-first project workflow: consent-gated git, verification, coverage checklists, test discipline |
| [`repository-hygiene](skills/original/repository-hygiene/SKILL.md) | Repository cleanup: classification, temporary files, generated artifacts, secrets, commit preparation |
| [`beyond-vibe-coding-autonomous-development](skills/original/beyond-vibe-coding-autonomous-development/SKILL.md) | Intent-driven AI-era software development: prompt engineering, the 70% problem, code review, autonomous agents |
| [`document-editing-general](skills/original/document-editing-general/SKILL.md) | Create, read, edit and manage documents (markdown, text, code) in an editor panel |
| [`github-code-documentation](skills/original/github-code-documentation/SKILL.md) | Detailed descriptions and high-quality READMEs for scripts and programs published to GitHub |
| [`generate-markdown-and-docx-documents](skills/original/generate-markdown-and-docx-documents/SKILL.md) | Produce a Markdown file and a Word (DOCX) file from an outline |
| [`detailed-source-rewrite-guide](skills/original/detailed-source-rewrite-guide/SKILL.md) | Rewrite an article or paper into a structured, step-by-step guide |
| [`book-to-skill](skills/original/book-to-skill/SKILL.md) | Convert a book or article into a reusable skill |
| [`ds-note-formatter](skills/original/ds-note-formatter/SKILL.md) | Format content for Synology DS Note / Note Station |
| [`create-individual-calendar-events-from-earnings-dates-list](skills/original/create-individual-calendar-events-from-earnings-dates-list/SKILL.md) | One calendar event per ticker, with company name and reminder |
| [`yfinance-ai](skills/original/yfinance-ai/SKILL.md) | Yahoo Finance integration: stocks, crypto, forex, commodities and ETFs |
| [`enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras](skills/original/enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras/SKILL.md) | Wake-on-LAN and auto-shutdown on network loss for a Raspberry Pi |
| [`fix-inconclusive-skills](skills/original/fix-inconclusive-skills/SKILL.md) | Find and fix skills marked as inconclusive because of missing tools |
| [`generate-findings-report-from-pipeline-logs](skills/original/generate-findings-report-from-pipeline-logs/SKILL.md) | Verify that generated files contain every expected section, and summarize discrepancies |
| [`testing-skills](skills/original/testing-skills/SKILL.md) | Test skills with pressure scenarios and rationalization tables |
| [`universal-listing-template](skills/original/universal-listing-template/SKILL.md) | Generate structured lists, inventories and tables |
| [`focus-my-energy](skills/original/focus-my-energy/SKILL.md) | Classify tasks by cognitive demand and recommend what to work on now |
| [`generate-fresh-ideas](skills/original/generate-fresh-ideas/SKILL.md) | Remix source material into five distinct content angles |
| [`get-more-perspectives](skills/original/get-more-perspectives/SKILL.md) | Stress-test a decision across a five-advisor panel |
| [`match-my-writing-style](skills/original/match-my-writing-style/SKILL.md) | Draft, reply or rewrite in your own voice, learned from your samples |
| [`prep-for-meetings](skills/original/prep-for-meetings/SKILL.md) | Pre-meeting brief and a 30-second glance card from your Workspace sources |

### Skills by Task

| Area | Original skills | Personas, prompts and rules |
|------|-----------------|----------------------------|
| **Research** | `write-research-projects`, `detailed-source-rewrite-guide`, `book-to-skill`, `generate-findings-report-from-pipeline-logs` | `orion-researcher` persona; `deep-research-writing-long.md` / `-short.md` prompts; `research-learning` module; `research-agent` profile |
| **Software engineering** | `beyond-vibe-coding-autonomous-development`, `github-code-documentation`, `document-editing-general`, `generate-markdown-and-docx-documents`, `enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras`, `fix-inconclusive-skills` | `bruno-coder` persona; `coding`, `debugging`, `testing` modules; `coding-agent`, `debugging-agent` profiles |
| **Architecture** | `get-more-perspectives` (trade-off stress tests) | `atlas-architect` persona; `planning` module; `planning-agent` profile |
| **Critical thinking** | `get-more-perspectives`, `generate-fresh-ideas` | `victor-thinker` persona; `thinking-frameworks` external skill category |
| **Writing** | `match-my-writing-style`, `detailed-source-rewrite-guide`, `ds-note-formatter`, `generate-markdown-and-docx-documents` | `elias-writer` persona |
| **Decision-making** | `get-more-perspectives`, `focus-my-energy` | `marcus-advisor` persona |
| **Financial analysis** | `yfinance-ai`, `create-individual-calendar-events-from-earnings-dates-list` | `adrian-investor` persona; `investing` module; `investing-agent` profile; day-trader external skills (link-only) |
| **Security and penetration testing** | `pen-testing`, `penetration-testing-guide` | `security` module |
| **Task management and productivity** | `ticktick-tasks`, `universal-listing-template`, `focus-my-energy`, `prep-for-meetings`, `match-my-writing-style`, `ds-note-formatter`, `create-individual-calendar-events-from-earnings-dates-list` | `jericho-chef` persona for cooking and meal planning |
| **Repository upkeep** | `repository-hygiene`, `agent-operating-rules`, `testing-skills`, `fix-inconclusive-skills`, `generate-findings-report-from-pipeline-logs` | `repository-hygiene.md` system prompt |

External link-only skills extend these areas - the `deep-research` and
`web-research` links for research, `frontend-design-systems` for frontend
work, or the day-trader suite for trading workflows. The complete external
list is in [docs/CATEGORY_INDEX.md](docs/CATEGORY_INDEX.md).

### Compatibility

- **Original skills** use the `SKILL.md` frontmatter convention
  (`name`, `description`, `version`, `author`, `category`) and load in OpenCode
  and in any agent that reads that format.
- **Bundled third-party skills** are local copies of upstream `SKILL.md` files
  with provenance recorded; they load like original files.
- **External skills** are URL references. They are platform-neutral but are not
  tested by this repository and may target a specific harness.
- **Personas, system prompts and rule modules** are plain Markdown and work as
  chat modes, custom instructions or rule files in most agent tools.
- **Installation scripts** target OpenCode's user-level skills directory
  (`~/.config/opencode/skills/`). Other agents need a manual copy step.

## Third-party skills

Two clearly separated groups. They are never counted as the same thing.

**Link-only** - upstream skills referenced by URL, with no content copied here:

- Curated table with purpose and license: [skills/third-party/README.md](skills/third-party/README.md)
- Raw URL lists: [catalog/links/](catalog/links/)
- Generated index of every entry: [docs/CATEGORY_INDEX.md](docs/CATEGORY_INDEX.md)

**Bundled** - seven reverse-engineering skills copied into
`skills/third-party/` from `zhaoxuya520/reverse-skill` and `morluto/rea`.
Each file carries an upstream copyright notice, and the companion files a
skill links to inside its own directory are bundled with it; the full license
texts are in [docs/THIRD-PARTY-LICENSES.md](docs/THIRD-PARTY-LICENSES.md).

| Bundled skill | Upstream |
|---------------|----------|
| `apk-reverse` | `zhaoxuya520/reverse-skill` |
| `binary-diff` | `zhaoxuya520/reverse-skill` |
| `ghidra-reverse` | `zhaoxuya520/reverse-skill` |
| `js-reverse` | `zhaoxuya520/reverse-skill` |
| `mobile-reverse` | `zhaoxuya520/reverse-skill` |
| `reverse-engineering` | `zhaoxuya520/reverse-skill` |
| `reverse-engineer-anything` | `morluto/rea` |

A URL returning HTTP 200 proves availability only. It says nothing about the
linked content, its license, its security posture or whether it works in your
harness. Review an external skill before you install it.

## Prompts and personas

System prompts in `prompts/system/` (including the compact
`deep-research-writing-short.md`), chat personas in `prompts/personas/`, and
image prompts in `prompts/image/`. All plain Markdown - copy them in.

| Persona | Role |
|---------|------|
| `jayce-generalist` | Versatile expert, truth over agreement |
| `jayce-generalist-expanded` | Multidisciplinary generalist, expanded brief |
| `bruno-coder` | Senior software engineer, understand first |
| `atlas-architect` | Systems architect, simplest reliable architecture |
| `elias-writer` | Technical writer, clarity and precision |
| `adrian-investor` | CIO, long-term risk-adjusted returns |
| `orion-researcher` | Research analyst, evidence-based conclusions |
| `victor-thinker` | Strategic challenger, stress-test ideas |
| `marcus-advisor` | Decision advisor, decisive trade-off analysis |
| `jericho-chef` | Personal chef, recipe discovery and cooking |

## Agent instructions

| File | Use |
|------|-----|
| `AGENTS.md` | Modular entry point - loads rule files on demand |
| `AGENTS-combined.md` | The same rules inline in one file |
| `instructions/modules/` | Domain modules: coding, debugging, planning, frontend, documents, research, local AI infrastructure, investing, engineering/3D, security, testing |
| `instructions/profiles/` | Preconfigured profiles for specialized agents |
| `instructions/opencode/project-template/` | Ready-to-copy project scaffold for OpenCode |

Use `AGENTS.md` or `AGENTS-combined.md`, never both in the same project.

## Catalog

`catalog/items.json` holds one record per skill: name, category, repository,
upstream URL, authorship (`original` or `link-only`), license and verification
status. The URL lists in `catalog/links/` are authoritative for external
skills, and `docs/CATEGORY_INDEX.md` is generated from them.

The catalog and the index are regenerated by a single command; CI fails if
either is stale:

```bash
python scripts/update-category-index.py          # write the index and count blocks
python scripts/update-category-index.py --check  # verify only
```

## Contributing

Adding content is welcome - see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)
for the process and [docs/SKILL_SPEC.md](docs/SKILL_SPEC.md) for the format. A
copy-ready skeleton lives in `docs/templates/SKILL-TEMPLATE.md`.

**Add a skill:** create `skills/original/<skill-name>/SKILL.md` from the
template, add a catalog record, regenerate the index, run the validation.

**Improve a skill:** edit the file, bump the version, update the version
history table, run the validation.

**Validate everything:**

```bash
python scripts/validate-frontmatter.py            # skill metadata
python scripts/check-sync.py                      # rule copies are in sync
python scripts/update-category-index.py --check   # generated files are current
python scripts/check-markdown-links.py           # relative Markdown links resolve
python -m unittest discover -s scripts -p "test_*.py"  # tooling tests
```

CI runs the same checks on every push and pull request. A monthly workflow
checks external link availability.

The current improvement backlog for existing skills is tracked in
[docs/SKILL-QUALITY-REVIEW.md](docs/SKILL-QUALITY-REVIEW.md).

## Funding

This collection is maintained in spare time and offered for free under MIT.
If it saves you time, support the work through
[GitHub Sponsors](https://github.com/sponsors/DracieVajko).

Contributions fund new original skills, maintenance of the existing skills and
the catalog, documentation, testing and CI, compatibility work with current AI
coding agents, research methods, and help for community contributions.

The tier amounts are configured on the
[Sponsors page](https://github.com/sponsors/DracieVajko); the levels below
describe what each level funds.

| Level | Typical amount | What it funds |
|-------|----------------|---------------|
| Tip | one-time | A thank-you that helps cover hosting for the docs |
| Supporter | monthly | Recurring upkeep: external link checks and catalog maintenance |
| Sustainer | monthly | Documentation refreshes, new skills, testing and CI work |
| Patron | monthly | Priority triage of feature requests, and early public review drafts of new skills |

No skill is paywalled, and there is no guaranteed access to commercial
services or exclusive AI capabilities. Sponsorship speeds the work up; it
does not gate content. All original material stays public under the MIT
license, and GitHub shows sponsor status on your own profile as a public
badge.

## Roadmap

A living list, not a promise of dates. Inputs come from
[docs/SKILL-QUALITY-REVIEW.md](docs/SKILL-QUALITY-REVIEW.md) and everyday use.

- **Near term** - trim over-length skill descriptions for picker display, align
  the skill heading vocabulary with `docs/SKILL_SPEC.md`, add version history
  sections to older skills.
- **Mid term** - installation examples for agents other than OpenCode, more
  worked examples in the younger skills, expanded domain rule modules.
- **Long term** - a smoother contribution flow for outside authors, per-area
  skill bundles, and a steady maintenance cadence as funding allows.

## Licensing and attribution

| Content | License |
|---------|---------|
| Original skills, prompts, personas, rules, docs and scripts | MIT (Â© 2026 DracieVajko) - [LICENSE](LICENSE) |
| External skills (link-only) | Upstream licenses; no content copied here |
| Bundled third-party skills | Upstream MIT licenses - [docs/THIRD-PARTY-LICENSES.md](docs/THIRD-PARTY-LICENSES.md) |

[ATTRIBUTION.md](ATTRIBUTION.md) records authorship and provenance for every
item, and [docs/SAFETY-AND-LICENSES.md](docs/SAFETY-AND-LICENSES.md) covers the
safety boundaries. Upstream copyright notices are never removed.

## Related repositories

- [OpenCode](https://github.com/anomalyco/opencode) - the agent this collection targets first
- [Superpowers](https://github.com/obra/superpowers) - upstream skill framework referenced here
- [Odysseus](https://github.com/DracieVajko/odysseus) - consume the plain URL lists directly

---

Maintained by [@DracieVajko](https://github.com/DracieVajko).
