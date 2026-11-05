# Skills

This directory separates what this repository authors from what it
references. Two kinds live here, always clearly labeled:

- `original/` - skills authored and maintained in this repository (**25**)
- `third-party/` - upstream skills referenced by link only (**188**). No
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
| `repository-hygiene` | Repository cleanup: classification, temporary files, generated artifacts, secrets and commit preparation | [`SKILL.md`](original/repository-hygiene/SKILL.md) |
| `beyond-vibe-coding-autonomous-development` | Practical skill for AI-era software development based on Addy Osmani's 'Beyond Vibe Coding' — intent-driven workflows, prompt engineering, the 70% problem, code review/refinement, AI prototyping, autonomous agents, and production-ready AI-assisted engineering. | [`SKILL.md`](original/beyond-vibe-coding-autonomous-development/SKILL.md) |
| `document-editing-general` | General-purpose skill for creating, reading, editing and managing documents (markdown, text, code, etc.) in an editor panel. | [`SKILL.md`](original/document-editing-general/SKILL.md) |
| `github-code-documentation` | Skill for creating detailed descriptions and high-quality README.md files for scripts and programs intended for GitHub upload, push and commit. Includes coding and 'vibe-coding' rules to maximize efficiency and minimize errors. | [`SKILL.md`](original/github-code-documentation/SKILL.md) |
| `penetration-testing-guide` | Penetration testing guide and methodology covering 5 phases: Recon, Scan, Gain Access, Escalate and Report. | [`SKILL.md`](original/penetration-testing-guide/SKILL.md) |
| `generate-markdown-and-docx-documents` | Create a new document from a user-provided outline and content, output both a Markdown file and a Word (DOCX) file for download. | [`SKILL.md`](original/generate-markdown-and-docx-documents/SKILL.md) |
| `create-individual-calendar-events-from-earnings-dates-list` | Create individual calendar events from an earnings dates list, one event per ticker with company name and reminder. | [`SKILL.md`](original/create-individual-calendar-events-from-earnings-dates-list/SKILL.md) |
| `ds-note-formatter` | Format content for Synology DS Note / Note Station so it pastes cleanly and preserves structure, readability and checklist usability. | [`SKILL.md`](original/ds-note-formatter/SKILL.md) |
| `fix-inconclusive-skills` | Identify and fix skills marked as inconclusive due to missing tools or other issues. | [`SKILL.md`](original/fix-inconclusive-skills/SKILL.md) |
| `generate-findings-report-from-pipeline-logs` | Verify that all expected sections and data are present in generated files by comparing logs and output artifacts, and summarize discrepancies. | [`SKILL.md`](original/generate-findings-report-from-pipeline-logs/SKILL.md) |
| `testing-skills` | Test skills that enforce discipline, compliance and verification using pressure scenarios and rationalization tables. | [`SKILL.md`](original/testing-skills/SKILL.md) |
| `yfinance-ai` | World-class AI-powered Yahoo Finance integration: 56+ tools for stocks, crypto, forex, commodities and ETFs. | [`SKILL.md`](original/yfinance-ai/SKILL.md) |
| `book-to-skill` | Convert a book or article into a reusable skill using AI and web data. | [`SKILL.md`](original/book-to-skill/SKILL.md) |
| `universal-listing-template` | Generate structured lists (TODO lists, inventory, tables) using AI and file operations. | [`SKILL.md`](original/universal-listing-template/SKILL.md) |
| `enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras` | Enable Wake-on-LAN and auto-shutdown on network loss for Raspberry Pi. | [`SKILL.md`](original/enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras/SKILL.md) |
| `detailed-source-rewrite-guide` | Rewrite a source document (e.g., article, research paper) into a structured, step-by-step guide using AI. | [`SKILL.md`](original/detailed-source-rewrite-guide/SKILL.md) |
| `focus-my-energy` | Classify tasks by cognitive demand and recommend what to work on now based on energy level | [`SKILL.md`](original/focus-my-energy/SKILL.md) |
| `generate-fresh-ideas` | Remix source material into five distinct creative content angles | [`SKILL.md`](original/generate-fresh-ideas/SKILL.md) |
| `get-more-perspectives` | Stress-test decisions across a five-advisor panel | [`SKILL.md`](original/get-more-perspectives/SKILL.md) |
| `match-my-writing-style` | Draft, reply or rewrite in the user's authentic voice from Gmail/Docs samples | [`SKILL.md`](original/match-my-writing-style/SKILL.md) |
| `prep-for-meetings` | Pre-meeting brief and 30-second glance card from Workspace sources | [`SKILL.md`](original/prep-for-meetings/SKILL.md) |

Install all original skills (OpenCode):

```powershell
# Windows
.\scripts\install-skills.ps1
```

```bash
# Linux / macOS
./scripts/install-skills.sh

# Manual, one skill
cp -r skills/original/repository-hygiene ~/.config/opencode/skills/
```

## Third-Party Skills (links only)

188 upstream skills are referenced by URL only. Their content is never
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
