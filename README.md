# Dracievajko AI Agent Collection

[![CI](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml/badge.svg)](https://github.com/DracieVajko/Dracievajko-SkillsSet/actions/workflows/skills-tooling.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Sponsors](https://img.shields.io/github/sponsors/DracieVajko?style=for-the-badge&logo=github-sponsors&color=ea4aaa)](https://github.com/sponsors/DracieVajko)

A curated collection of reusable **AI agent skills, system prompts, personas,
agent rules and workflows**, maintained and tested on four platforms:
**Odysseus, Cindy, OpenCode and OpenDesign**.

Everything is plain Markdown and Python. There is no runtime, no service and
no dependency you have to trust: you copy what you need, read it, and adapt
it. My own work and other people's work are kept in separate categories and
are never mixed.

**No releases - `master` is the source of truth.** There are no release tags and
no versioned downloads on purpose: every push to `master` is the current state,
and the install scripts always read from `master`. If you need a fixed snapshot,
pin a commit hash in your own fork.

## Quick Navigation

| Looking for | Go to |
|-------------|-------|
| What this repository is | [Introduction](#what-this-repository-is) |
| Platforms used and tested | [Platforms](#platforms-i-use-and-test) |
| Exact contents and counts | [Repository contents](#repository-contents) |
| Install into OpenCode | [Quick Start](#quick-start) |
| The other tested platforms | [Platforms](#the-other-tested-platforms) |
| Machine sync and manifest | [Machine sync](#machine-sync) |
| Cindy plugins | [Cindy plugins](#cindy-plugins-i-track) |
| Authorship rules | [Authorship](#authorship-and-provenance) |
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

## Platforms I use and test

| Platform | How it consumes this collection |
|----------|---------------------------------|
| **OpenCode** | `scripts/install-skills.ps1` copies `skills/original/` into `~/.config/opencode/skills/`; `scripts/sync-skills.ps1` applies the shared collection from `sync/manifest.json`. |
| **Cindy** | Reads `~/.agents/skills/`. The repository keeps one installed copy there and mirrors it with directory junctions; Cindy's four built-in skills are managed by the app and never copied. |
| **Odysseus** | Consumes the plain URL lists in `catalog/links/` directly. |
| **OpenDesign** | Uses the `opendesign-trial` plugin from its marketplace plus `prompts/system/opendesign-ui-code-audit.md`; plugin files are per device and are not stored here. |

Not tested on Hermes, Claude Code, Claude, OpenAI/GPT, Codex or VS Code -
treat those as unsupported until tested.

## Repository contents

The numbers below are generated from `catalog/items.json` and the filesystem
by `scripts/update-category-index.py` - they are never maintained by hand.

<!-- counts:start -->

| What | Count | Where |
|------|------:|-------|
| Original skills | 23 | `skills/original/` - authored and maintained here |
| Bundled third-party skills | 6 | `skills/third-party/` - local copies of upstream `SKILL.md` files |
| External link-only skills | 236 | referenced by URL; no content copied |
| Stable-branch links | 191 | `catalog/links/skill-links.txt` |
| Pinned links | 45 | `catalog/links/pinned-links.txt` |
| Catalog records | 259 | `catalog/items.json` |
| System prompts | 9 | `prompts/system/` |
| Personas | 10 | `prompts/personas/` |
| Image prompts | 4 | `prompts/image/` |
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

## Machine sync

`sync/` holds one shared collection: every skill and plugin any of my
computers has, described once, so any computer can be brought to the same
state without duplicating skill content. A computer only writes its own
evidence file; the shared files are built from all of them. The current
collection has **108 enabled skills**; `sync/collection.json` is the source of
truth.

| File | Purpose |
|------|---------|
| `sync/collection.json` | **The collection**: every skill and plugin, how it installs, which agents see it, where it was seen, plus coverage gaps and hash drift. |
| `sync/manifest.json` | The same collection in the schema the installer reads. This is the only install manifest, never a per-computer snapshot. |
| `sync/cindy-plugins.json` | Plugins for Cindy, OpenCode and OpenDesign, with what each needs to be authorized again. |
| `sync/optional.json` | Disabled skills (not installed); empty when everything is enabled. |
| `sync/prune-optional.py` | Moves disabled skills out of every agent root into `~/.config/opencode/skills-disabled/`. |
| `sync/CINDY-INSTALL.md` | Ready-to-paste prompt: installs the skills, then the plugins, then reports what still needs me. |
| `sync/UPDATE.md` | Ready-to-paste prompt: updates a computer to the versions recorded in the collection. |
| `sync/verify-installed.py` | Checks every installed skill against the recorded hash; `0 differ` is the success line. |
| `sync/machines/<machineId>.json` | Raw evidence from one computer. Not a separate collection. |
| `sync/unresolved.md` | Skills with no verified upstream; they stay out of `skills/original/` until one is found. |
| `sync/generate-manifest.py` | Records this computer as `machines/<machineId>.json`. |
| `sync/build-collection.py` | Merges every evidence file into `collection.json`, `manifest.json` and `unresolved.md`. |
| `scripts/sync-skills.ps1` | Installs missing skills and recreates directory junctions. |

```powershell
.\scripts\sync-skills.ps1 -DryRun   # preview: what installs, what stays unresolved
.\scripts\sync-skills.ps1           # install and link
python sync\prune-optional.py       # move disabled skills out of every root
python sync\generate-manifest.py    # record this computer as evidence
python sync\build-collection.py     # refresh the shared collection
```

The script never overwrites an existing skill folder without `-Force`, and it
reports upstream drift, unresolved skills and failures instead of guessing.
Cindy, OpenCode and OpenDesign plugins are installed from their marketplace or
config (see `sync/CINDY-INSTALL.md`) and authorized per device; nothing
per-device is stored here.

The evidence files also inventory roots this repository does not manage,
including skills that ship inside an app, so nothing installed on a computer
silently falls out of scope. Those entries are listed, never copied.

Run git operations on one PC at a time: commit and push there, then `git pull`
on the other.

## Cindy plugins I track

These plugins are optional and installed per device from the Cindy
marketplace. Their files, tokens and OAuth grants are **not** stored in this
repository; each machine has to install and authorize them again. The
machine-readable list is `sync/cindy-plugins.json`.

| Plugin | What it does | What it needs |
|--------|--------------|---------------|
| `agent-desktop` | Read and drive the desktop GUI: click, type, snapshot windows, clipboard, notifications | nothing |
| `cindy-art` | Image and art generation; installed but disabled | nothing while disabled |
| `cindy-github` | GitHub issues, PRs, reviews, repositories, Actions, releases, search | the machine's GitHub login or a fallback PAT |
| `cindy-mermaid` | Normalize Mermaid diagram source | nothing |
| `cindy-web-search` | Web search and page fetch | optional Brave/Tavily/DeepSeek keys |
| `compact-file-browser` | Left-panel project file browser | nothing |
| `gh-market` | Search GitHub for Cindy plugins and skills | optional GitHub PAT for rate limits |
| `git-flow` | Local repository and branch panel, GitHub account switching | nothing |
| `google-calendar` | Read and change calendar events | Google OAuth, per device |
| `google-drive` | Search and manage Drive files, Docs and Slides | Google OAuth, per device |
| `google-gmail` | Read mail, drafts and send through the draft card | Google OAuth, per device |
| `my-browser` | Cindy Chrome: page translation and in-player subtitles | the Cindy Chrome extension on that machine |
| `ntfy` | Push notifications through a personal ntfy server | ntfy server URL and access token |
| `opendesign-trial` | Create and revise HTML drafts with a local editor | nothing |
| `ponytail` | Lazy-senior code review and anti-over-engineering rules | nothing |
| `prompt-optimizer` | Rewrites prompts before they are sent; installed but disabled | nothing while disabled |
| `ticktick-connector` | TickTick tasks, projects and habits through a Cindy plugin plus an OAuth MCP server; not installed here | TickTick OAuth; install from its GitHub release |
| `tuya-home` | Tuya / Smart Life devices: lights, plugs, air conditioners, sensors | local development copy, not a marketplace plugin; Tuya API key starting with `sk-` |

The separate OpenCode plugin `superpowers@git+https://github.com/obra/superpowers`
is configured in the OpenCode config on each machine
(`~/.config/opencode/opencode.jsonc`); it is not a Cindy plugin.

## Repository structure

```text
.
├── .github/
│   ├── FUNDING.yml              # GitHub Sponsors
│   ├── ISSUE_TEMPLATE/          # bug report, feature request, skill submission
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/               # skills-tooling.yml, link-check.yml
├── catalog/
│   ├── README.md
│   ├── items.json               # 259 records: 23 original + 236 link-only
│   └── links/
│       ├── README.md
│       ├── skill-links.txt      # 191 stable-branch links
│       └── pinned-links.txt     # 45 pinned commit links
├── docs/
│   ├── CATEGORY_INDEX.md        # generated index of every skill
│   ├── CONTRIBUTING.md          # how to add or update content
│   ├── INSTALL.md               # installation, updating, uninstalling, troubleshooting
│   ├── SAFETY-AND-LICENSES.md   # safety notes and license boundaries
│   ├── SKILL_SPEC.md            # the skill format specification
│   ├── SKILL-QUALITY-REVIEW.md  # prioritized improvement backlog
│   ├── THIRD-PARTY-LICENSES.md  # upstream licenses of bundled content
│   └── templates/               # project, plan, decisions, handoff, sources
├── instructions/
│   ├── modules/                 # 11 domain rule modules
│   ├── profiles/                # 9 specialized agent profiles
│   └── opencode/                # OpenCode integration + project template
├── prompts/
│   ├── system/                  # 9 system prompts
│   ├── personas/                # 10 chat personas
│   └── image/                   # 4 image prompts
├── scripts/                     # validators, index generator, link checkers, installers, sync, tests
├── sync/
│   ├── collection.json          # one collection of every skill and plugin
│   ├── manifest.json            # the collection in the installer's schema
│   ├── machines/                # raw evidence from each computer
│   ├── cindy-plugins.json       # Cindy, OpenCode and OpenDesign plugins
│   ├── CINDY-INSTALL.md         # paste-into-Cindy prompt to install everything
│   ├── unresolved.md            # skills with no verified upstream
│   ├── generate-manifest.py     # records this computer as evidence
│   ├── build-collection.py      # merges evidence into collection.json + manifest.json
│   └── README.md                # apply the collection to a computer
├── skills/
│   ├── README.md
│   ├── original/                # 23 original skills, one folder each
│   └── third-party/             # 6 bundled SKILL.md bodies + provenance, everything else linked
├── AGENTS.md                    # modular rules entry point
├── AGENTS-combined.md           # the same rules in one file
├── ATTRIBUTION.md               # authorship and license summary
├── LICENSE                      # MIT
└── README.md
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

### The other tested platforms

OpenCode is the only platform with an installer in this repository. On Cindy,
Odysseus and OpenDesign, use the routes below; nothing else is claimed as
supported.

| Platform | Practical route |
|----------|-----------------|
| Cindy | Put skills in `~/.agents/skills/`; `scripts/sync-skills.ps1` recreates the junctions from the manifest. |
| Odysseus | Feed it `catalog/links/skill-links.txt` and `catalog/links/pinned-links.txt`. |
| OpenDesign | Install the `opendesign-trial` plugin from the marketplace and use `prompts/system/opendesign-ui-code-audit.md`. |

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
| [`ticktick-tasks`](skills/original/ticktick-tasks/SKILL.md) | Manage TickTick tasks, projects, tags, habits and focus via MCP |
| [`write-research-projects`](skills/original/write-research-projects/SKILL.md) | Deep research, academic writing, source verification and complex projects |
| [`pen-testing`](skills/original/pen-testing/SKILL.md) | Authorized penetration testing methodology: scope, recon, scan, controlled testing, blast radius, report |
| [`agent-operating-rules`](skills/original/agent-operating-rules/SKILL.md) | Evidence-first project workflow: consent-gated git, verification, coverage checklists, test discipline |
| [`repository-hygiene`](skills/original/repository-hygiene/SKILL.md) | Repository cleanup: classification, temporary files, generated artifacts, secrets, commit preparation |
| [`beyond-vibe-coding-autonomous-development`](skills/original/beyond-vibe-coding-autonomous-development/SKILL.md) | Intent-driven AI-era software development: prompt engineering, the 70% problem, code review, autonomous agents |
| [`document-editing-general`](skills/original/document-editing-general/SKILL.md) | Create, read, edit and manage documents (markdown, text, code) in an editor panel |
| [`github-code-documentation`](skills/original/github-code-documentation/SKILL.md) | Detailed descriptions and high-quality READMEs for scripts and programs published to GitHub |
| [`detailed-source-rewrite-guide`](skills/original/detailed-source-rewrite-guide/SKILL.md) | Rewrite an article or paper into a structured, step-by-step guide |
| [`book-to-skill`](skills/original/book-to-skill/SKILL.md) | Convert a book or article into a reusable skill |
| [`ds-note-formatter`](skills/original/ds-note-formatter/SKILL.md) | Format content for Synology DS Note / Note Station |
| [`create-individual-calendar-events-from-earnings-dates-list`](skills/original/create-individual-calendar-events-from-earnings-dates-list/SKILL.md) | One calendar event per ticker, with company name and reminder |
| [`yfinance-ai`](skills/original/yfinance-ai/SKILL.md) | Yahoo Finance integration: stocks, crypto, forex, commodities and ETFs |
| [`enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras`](skills/original/enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras/SKILL.md) | Wake-on-LAN and auto-shutdown on network loss for a Raspberry Pi |
| [`fix-inconclusive-skills`](skills/original/fix-inconclusive-skills/SKILL.md) | Find and fix skills marked as inconclusive because of missing tools |
| [`generate-findings-report-from-pipeline-logs`](skills/original/generate-findings-report-from-pipeline-logs/SKILL.md) | Verify that generated files contain every expected section, and summarize discrepancies |
| [`testing-skills`](skills/original/testing-skills/SKILL.md) | Test skills with pressure scenarios and rationalization tables |
| [`universal-listing-template`](skills/original/universal-listing-template/SKILL.md) | Generate structured lists, inventories and tables |
| [`focus-my-energy`](skills/original/focus-my-energy/SKILL.md) | Classify tasks by cognitive demand and recommend what to work on now |
| [`generate-fresh-ideas`](skills/original/generate-fresh-ideas/SKILL.md) | Remix source material into five distinct content angles |
| [`get-more-perspectives`](skills/original/get-more-perspectives/SKILL.md) | Stress-test a decision across a five-advisor panel |
| [`match-my-writing-style`](skills/original/match-my-writing-style/SKILL.md) | Draft, reply or rewrite in your own voice, learned from your samples |
| [`prep-for-meetings`](skills/original/prep-for-meetings/SKILL.md) | Pre-meeting brief and a 30-second glance card from your Workspace sources |

### Skills by Task

| Area | Original skills | Personas, prompts and rules |
|------|-----------------|----------------------------|
| **Research** | `write-research-projects`, `detailed-source-rewrite-guide`, `book-to-skill`, `generate-findings-report-from-pipeline-logs` | `orion-researcher` persona; `deep-research-writing-long.md` / `-short.md` prompts; `research-learning` module; `research-agent` profile |
| **Software engineering** | `beyond-vibe-coding-autonomous-development`, `github-code-documentation`, `document-editing-general`, `enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras`, `fix-inconclusive-skills` | `bruno-coder` persona; `coding`, `debugging`, `testing` modules; `coding-agent`, `debugging-agent` profiles |
| **Architecture** | `get-more-perspectives` (trade-off stress tests) | `atlas-architect` persona; `planning` module; `planning-agent` profile |
| **Critical thinking** | `get-more-perspectives`, `generate-fresh-ideas` | `victor-thinker` persona; `thinking-frameworks` external skill category |
| **Writing** | `match-my-writing-style`, `detailed-source-rewrite-guide`, `ds-note-formatter` | `elias-writer` persona |
| **Decision-making** | `get-more-perspectives`, `focus-my-energy` | `marcus-advisor` persona |
| **Financial analysis** | `yfinance-ai`, `create-individual-calendar-events-from-earnings-dates-list` | `adrian-investor` persona; `investing` module; `investing-agent` profile; day-trader external skills (link-only) |
| **Security and penetration testing** | `pen-testing` | `security` module |
| **Task management and productivity** | `ticktick-tasks`, `universal-listing-template`, `focus-my-energy`, `prep-for-meetings`, `match-my-writing-style`, `ds-note-formatter`, `create-individual-calendar-events-from-earnings-dates-list` | `jericho-chef` persona for cooking and meal planning |
| **Repository upkeep** | `repository-hygiene`, `agent-operating-rules`, `testing-skills`, `fix-inconclusive-skills`, `generate-findings-report-from-pipeline-logs` | `repository-hygiene.md` system prompt |

External link-only skills extend these areas - the `deep-research` link for
research, `frontend-design-systems` for frontend work, or the day-trader suite
for trading workflows. The complete external list is in
[docs/CATEGORY_INDEX.md](docs/CATEGORY_INDEX.md).

### What the files are

- **Original skills** use the `SKILL.md` frontmatter convention (`name`,
  `description`, `version`, `author`, `authorship`, `category`). OpenCode reads
  this format directly; the other tested platforms use the routes above.
- **Bundled third-party skills** are local copies of upstream `SKILL.md` files
  with their notices preserved; authorship stays with the upstream author, and
  their companion notes are linked to the upstream repository rather than
  vendored here.
- **External skills** are URL references only. They are not tested here and may
  target a specific harness.
- **Personas, system prompts and rule modules** are plain Markdown, consumed as
  chat modes, custom instructions or rule files on the platforms listed above.
- **Installation scripts** target OpenCode's user-level skills directory
  (`~/.config/opencode/skills/`). Cindy, Odysseus and OpenDesign use the routes
  in the table above.

## Third-party skills

Two clearly separated groups. They are never counted as the same thing.

**Link-only** - upstream skills referenced by URL, with no content copied here:

- Curated table with purpose and license: [skills/third-party/README.md](skills/third-party/README.md)
- Raw URL lists: [catalog/links/](catalog/links/)
- Generated index of every entry: [docs/CATEGORY_INDEX.md](docs/CATEGORY_INDEX.md)

**Bundled** - six reverse-engineering skills copied into
`skills/third-party/` from `zhaoxuya520/reverse-skill` and `morluto/rea`.
Each file carries an upstream copyright notice. Only the six `SKILL.md`
bodies are redistributed; the companion notes they link to stay in the
upstream repository, and the full license texts are in
[docs/THIRD-PARTY-LICENSES.md](docs/THIRD-PARTY-LICENSES.md).

| Bundled skill | Upstream |
|---------------|----------|
| `apk-reverse` | `zhaoxuya520/reverse-skill` |
| `binary-diff` | `zhaoxuya520/reverse-skill` |
| `ghidra-reverse` | `zhaoxuya520/reverse-skill` |
| `js-reverse` | `zhaoxuya520/reverse-skill` |
| `mobile-reverse` | `zhaoxuya520/reverse-skill` |
| `reverse-engineer-anything` | `morluto/rea` |

A URL returning HTTP 200 proves availability only. It says nothing about the
linked content, its license, its security posture or whether it works in your
harness. Review an external skill before you install it.

## Authorship and provenance

My work and other people's work are never mixed:

- **`skills/original/` may only contain my own work.** Every skill there must
  have `author: DracieVajko` and `authorship: original`.
  `scripts/validate-frontmatter.py` fails the build when that is not true, and
  CI runs it on every push.
- **Bundled third-party skills** live in `skills/third-party/`, keep their
  upstream copyright and license notices, and are limited to the six
  reverse-engineering skills listed above.
- **Every other foreign skill is a link only.** `catalog/items.json` records the
  repository, branch or commit, the path inside the repository, the direct raw
  `SKILL.md` URL and the license when known. No content is copied.
- **`sync/collection.json`** records authorship per skill, and `sync/manifest.json`
  is generated from it. A skill is never promoted to `original` just because it
  sits on my disk; an unresolved upstream stays `unknown` in
  `sync/unresolved.md`.

The full license texts are in
[docs/THIRD-PARTY-LICENSES.md](docs/THIRD-PARTY-LICENSES.md), and
[ATTRIBUTION.md](ATTRIBUTION.md) summarizes provenance.

## Prompts and personas

System prompts in `prompts/system/` - including `opendesign-ui-code-audit.md`
for UI and code audits and the compact `deep-research-writing-short.md` -
chat personas in `prompts/personas/`, and image prompts in `prompts/image/`.
All plain Markdown - copy them in.

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

# On a machine with the skills installed:
python sync/generate-manifest.py --check         # manifest matches this machine
```

CI runs the repository checks on every push and pull request; the manifest
check needs a machine with installed skills, so it is not a CI job. A monthly
workflow checks external link availability.

The current improvement backlog for existing skills is tracked in
[docs/SKILL-QUALITY-REVIEW.md](docs/SKILL-QUALITY-REVIEW.md).

## Funding

This collection is maintained in spare time and offered for free under MIT.
If it saves you time, support the work through
[GitHub Sponsors](https://github.com/sponsors/DracieVajko).

Contributions fund new original skills, maintenance of the existing skills and
the catalog, documentation, testing and CI, work on Odysseus, Cindy, OpenCode
and OpenDesign, research methods, and help for community contributions.

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
- **Mid term** - installation examples for Cindy, Odysseus and OpenDesign, more
  worked examples in the younger skills, expanded domain rule modules.
- **Long term** - a smoother contribution flow for outside authors, per-area
  skill bundles, and a steady maintenance cadence as funding allows.

## Licensing and attribution

| Content | License |
|---------|---------|
| Original skills, prompts, personas, rules, docs and scripts | MIT (© 2026 DracieVajko) - [LICENSE](LICENSE) |
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

---

## Support this work

If you find this project useful, consider supporting its ongoing development, maintenance, and improvements.

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?logo=github)](https://github.com/sponsors/DracieVajko)
