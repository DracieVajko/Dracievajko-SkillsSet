# OpenCode

## Modular Variant

Copy the contents of `project-template/` into the root of your project. The
template `AGENTS.md` loads the relevant file from `agent-rules/` on demand.

## Single-File Variant

Use [`AGENTS-combined.md`](../../AGENTS-combined.md) as the project `AGENTS.md`.
Do not use it together with the full modular rule set.

The files in `project-template/agent-rules/` are self-contained copies of
`instructions/modules/`. Keep them in sync when the rules change; the
`scripts/check-sync.py` check fails on drift.

## Skills

This repository bundles twenty-five original skills under `skills/original/`:

- [`ticktick-tasks`](../../skills/original/ticktick-tasks/SKILL.md) - manage
  TickTick tasks, projects, habits and focus via MCP
- [`write-research-projects`](../../skills/original/write-research-projects/SKILL.md) -
  deep research, academic writing, source verification and complex projects
- [`pen-testing`](../../skills/original/pen-testing/SKILL.md) - authorized
  penetration testing methodology: scope gate, recon, scan, controlled
  testing, blast radius, report
- [`agent-operating-rules`](../../skills/original/agent-operating-rules/SKILL.md) -
  evidence-first project workflow: consent-gated git, root-cause fixes,
  verification, coverage checklists and test discipline
- [`repository-hygiene`](../../skills/original/repository-hygiene/SKILL.md) -
  repository cleanup, temporary files, generated artifacts and commit
  preparation
- [`beyond-vibe-coding-autonomous-development`](../../skills/original/beyond-vibe-coding-autonomous-development/SKILL.md) - Practical skill for AI-era software development based on Addy Osmani's 'Beyond Vibe Coding' — intent-driven workflows, prompt engineering, the 70% problem, code review/refinement, AI prototyping, autonomous agents, and production-ready AI-assisted engineering.
- [`document-editing-general`](../../skills/original/document-editing-general/SKILL.md) - General-purpose skill for creating, reading, editing and managing documents (markdown, text, code, etc.) in an editor panel.
- [`github-code-documentation`](../../skills/original/github-code-documentation/SKILL.md) - Skill for creating detailed descriptions and high-quality README.md files for scripts and programs intended for GitHub upload, push and commit. Includes coding and 'vibe-coding' rules to maximize efficiency and minimize errors.
- [`penetration-testing-guide`](../../skills/original/penetration-testing-guide/SKILL.md) - Penetration testing guide and methodology covering 5 phases: Recon, Scan, Gain Access, Escalate and Report.
- [`generate-markdown-and-docx-documents`](../../skills/original/generate-markdown-and-docx-documents/SKILL.md) - Create a new document from a user-provided outline and content, output both a Markdown file and a Word (DOCX) file for download.
- [`create-individual-calendar-events-from-earnings-dates-list`](../../skills/original/create-individual-calendar-events-from-earnings-dates-list/SKILL.md) - Create individual calendar events from an earnings dates list, one event per ticker with company name and reminder.
- [`ds-note-formatter`](../../skills/original/ds-note-formatter/SKILL.md) - Format content for Synology DS Note / Note Station so it pastes cleanly and preserves structure, readability and checklist usability.
- [`fix-inconclusive-skills`](../../skills/original/fix-inconclusive-skills/SKILL.md) - Identify and fix skills marked as inconclusive due to missing tools or other issues.
- [`generate-findings-report-from-pipeline-logs`](../../skills/original/generate-findings-report-from-pipeline-logs/SKILL.md) - Verify that all expected sections and data are present in generated files by comparing logs and output artifacts, and summarize discrepancies.
- [`testing-skills`](../../skills/original/testing-skills/SKILL.md) - Test skills that enforce discipline, compliance and verification using pressure scenarios and rationalization tables.
- [`yfinance-ai`](../../skills/original/yfinance-ai/SKILL.md) - World-class AI-powered Yahoo Finance integration: 56+ tools for stocks, crypto, forex, commodities and ETFs.
- [`book-to-skill`](../../skills/original/book-to-skill/SKILL.md) - Convert a book or article into a reusable skill using AI and web data.
- [`universal-listing-template`](../../skills/original/universal-listing-template/SKILL.md) - Generate structured lists (TODO lists, inventory, tables) using AI and file operations.
- [`enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras`](../../skills/original/enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras/SKILL.md) - Enable Wake-on-LAN and auto-shutdown on network loss for Raspberry Pi.
- [`detailed-source-rewrite-guide`](../../skills/original/detailed-source-rewrite-guide/SKILL.md) - Rewrite a source document (e.g., article, research paper) into a structured, step-by-step guide using AI.
- [`focus-my-energy`](../../skills/original/focus-my-energy/SKILL.md) - classify
  tasks by cognitive demand and recommend what to work on now based on energy level
- [`generate-fresh-ideas`](../../skills/original/generate-fresh-ideas/SKILL.md) -
  remix source material into five distinct creative content angles
- [`get-more-perspectives`](../../skills/original/get-more-perspectives/SKILL.md) -
  stress-test decisions across a five-advisor panel
- [`match-my-writing-style`](../../skills/original/match-my-writing-style/SKILL.md) -
  draft, reply or rewrite in the user's authentic voice from Gmail/Docs samples
- [`prep-for-meetings`](../../skills/original/prep-for-meetings/SKILL.md) -
  pre-meeting brief and 30-second glance card from Workspace sources

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
