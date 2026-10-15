# Dracievajko AI Agent Collection

A curated collection of AI agent skills, system prompts, personas, and agent instructions for use with OpenCode, Claude Code, VS Code, and the Odysseus LLM interface.

## Structure

```
Dracievajko-AI-Agent-Collection/
â”œâ”€â”€ 01-my-skills/                    # Confirmed original skills authored by me
â”‚   â”œâ”€â”€ agent-harnesses/             # For OpenCode, Claude Code, VS Code, etc.
â”‚   â”‚   â””â”€â”€ ticktick-tasks/          # TickTick MCP task management
â”‚   â””â”€â”€ odysseus/                    # For Odysseus LLM interface
â”‚
â”œâ”€â”€ 02-my-modified-skills/           # Skills derived from others' work, modified for my needs
â”‚   â”œâ”€â”€ agent-harnesses/
â”‚   â”‚   â””â”€â”€ <skill-name>/
â”‚   â”‚       â”œâ”€â”€ SKILL.md
â”‚   â”‚       â””â”€â”€ SOURCE.md
â”‚   â””â”€â”€ odysseus/
â”‚       â””â”€â”€ <skill-name>/
â”‚           â”œâ”€â”€ SKILL.md
â”‚           â””â”€â”€ SOURCE.md
â”‚
â”œâ”€â”€ 03-third-party-skills/           # Unmodified third-party skills
â”‚   â”œâ”€â”€ agent-harnesses/
â”‚   â”‚   â”œâ”€â”€ README.md
â”‚   â”‚   â””â”€â”€ <skill-name>/
â”‚   â”‚       â”œâ”€â”€ SKILL.md
â”‚   â”‚       â””â”€â”€ SOURCE.md
â”‚   â””â”€â”€ odysseus/
â”‚       â”œâ”€â”€ README.md
â”‚       â”œâ”€â”€ skill-links.txt          # Verified raw Markdown URLs (one per line)
â”‚       â””â”€â”€ unverified-links.txt     # Candidate URLs needing verification
â”‚
â”œâ”€â”€ 04-system-prompts/               # System prompts and personas
â”‚   â”œâ”€â”€ README.md                    # This table explains each prompt's role
â”‚   â”œâ”€â”€ Jayce.md                     # Versatile expert generalist
â”‚   â”œâ”€â”€ Isha.md                      # Technical writer
â”‚   â”œâ”€â”€ Mel.md                       # Chief Investment Officer
â”‚   â”œâ”€â”€ Atlas.md                     # Systems architect
â”‚   â”œâ”€â”€ Bruno.md                     # Senior software engineer
â”‚   â”œâ”€â”€ Marcus.md                    # Decision advisor
â”‚   â”œâ”€â”€ Orion.md                     # Research analyst
â”‚   â”œâ”€â”€ Victor.md                    # Strategic challenger
â”‚   â”œâ”€â”€ Jericho.md                   # Personal chef
â”‚   â”œâ”€â”€ general.md                   # General expert consultant
â”‚   â”œâ”€â”€ coding.md                    # Concise coding assistant
â”‚   â”œâ”€â”€ cad.md                       # 3D printing copywriter (VoxelScribe)
â”‚   â”œâ”€â”€ trading.md                   # Algorithmic trading
â”‚   â”œâ”€â”€ repository-hygiene.md        # Repository cleanup & Git hygiene
â”‚   â”œâ”€â”€ upscale-basic.md             # Portrait upscale (identity preserved)
â”‚   â”œâ”€â”€ upscale-portrait.md          # Professional ID/CV headshot
â”‚   â””â”€â”€ upscale-translate.md         # 1:1 upscale + ENâ†’SK translation
â”‚
â”œâ”€â”€ 05-agent-instructions/           # Modular agent operating rules
â”‚   â”œâ”€â”€ modules/                     # Domain-specific rule modules
â”‚   â”œâ”€â”€ profiles/                    # Pre-configured agent profiles
â”‚   â””â”€â”€ combined/AGENTS.md           # Single-file alternative
â”‚
â”œâ”€â”€ catalog/                         # Canonical structured catalog
â”œâ”€â”€ templates/                       # Document templates (PLAN, HANDOFF, etc.)
â”œâ”€â”€ docs/                            # Documentation (publishing, safety, verification)
â”œâ”€â”€ scripts/                         # Utility scripts (validation, indexing)
â””â”€â”€ .github/workflows/               # CI/CD workflows (to be added)
```

## Skill Groups

### 01-my-skills
Confirmed original skills authored by me.
- **ticktick-tasks** â€” Manage TickTick tasks, projects, habits via MCP

### 02-my-modified-skills
Skills derived from someone else's work and modified for my needs. Currently empty â€” no modified skills identified.

### 03-third-party-skills
Unmodified third-party skills that I use or explicitly retain.

**Agent Harnesses (17 skills):**
- applying-themes, blender-geometry-nodes, blender-hard-surface-modeling, blender-python-integration, blender-rigging-animation, brainstorming, building-mcp-servers, code-documenter, code-reviewer, context-engineering, creating-skills, debugging-wizard, fine-tuning-expert, frontend-design-systems, idea-to-plan, using-superpowers, wordpress-pro

**Odysseus Links (158 verified + 12 unverified):**
- From: obra/superpowers, addyosmani/agent-skills, Jeffallan/claude-skills, mattpocock/skills, anthropics/skills, greensock/gsap-skills, composio-community/opencode-skills, pbakaus/impeccable, jakubkrehel/make-interfaces-feel-better, Jakubantalik/transitions.dev, vercel-labs/agent-browser, lackeyjb/playwright-skill, morluto/rea, Graphify-Labs/graphify, tjboudreaux/cc-thinking-skills, nextlevelbuilder/ui-ux-pro-max-skill
- Unverified: diegosouzapw/OmniRoute (12 skills)

## Personas (Arcane-Inspired)

Nine specialized personas with original Arcane character names restored:
- **Jayce** â€” Generalist (truth > agreement)
- **Isha** â€” Technical Writer (clarity, precision)
- **Mel** â€” CIO (long-term risk-adjusted returns)
- **Atlas** â€” Systems Architect (simplest reliable architecture)
- **Bruno** â€” Senior Software Engineer (understand first)
- **Marcus** â€” Decision Advisor (decisive trade-offs)
- **Orion** â€” Research Analyst (evidence-based)
- **Victor** â€” Strategic Challenger (stress-test ideas)
- **Jericho** â€” Personal Chef (recipe discovery)

## Quick Start

### For OpenCode / Claude Code / VS Code
```bash
# Copy skills to your local discovery directory
cp -r 01-my-skills/agent-harnesses/* ~/.config/opencode/skills/
cp -r 03-third-party-skills/agent-harnesses/* ~/.config/opencode/skills/
```

### For Odysseus
Import skills by pasting raw Markdown URLs from `03-third-party-skills/odysseus/skill-links.txt` into the Odysseus skill import dialog.

## Catalog

See `catalog/README.md` for the complete catalog with provenance tracking, reconciliation, and category/preset organization.

## License

See `LICENSE` for the collection's license. Individual third-party skills retain their original licenses (mostly MIT as claimed in frontmatter â€” verify against upstream).

## Attribution

See `ATTRIBUTION.md` for detailed source attribution of all third-party content.

## Contributing

This is a personal collection. For upstream contributions, please contribute to the original repositories listed in each skill's `SOURCE.md`.
