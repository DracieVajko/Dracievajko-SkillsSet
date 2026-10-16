# Dracievajko AI Agent Collection

A curated collection of AI agent skills, system prompts, personas, and agent instructions. It is structured for practical use across agent harnesses while keeping provenance and licensing honest.

## Explore

| Collection | Description |
|---|---|
| [01-my-skills](01-my-skills/) | Original skills authored by DracieVajko. |
| 02-my-modified-skills | Reserved for skills adapted from upstream sources — currently empty. |
| [03-third-party-skills](03-third-party-skills/) | Unmodified third-party skills, with provenance and license evidence. |
| [04-system-prompts](04-system-prompts/) | System prompts and personas for consistent agent behavior. |
| [05-agent-instructions](05-agent-instructions/) | Modular agent operating rules and profiles. |

## How to use

### Agent harnesses (OpenCode, Claude Code, VS Code)

This is a library layout, not an installation path. To activate a skill, copy the specific skill folder (not the surrounding collection) into the skill discovery location of your harness. Discovery locations differ per tool and per version; check the harness's own documentation. Some skills additionally need scripts, reference files, runtimes or MCP servers — follow the skill's `SKILL.md`.

### Odysseus

Link-only references for Odysseus are in [03-third-party-skills/odysseus](03-third-party-skills/odysseus/). Implementations are not bundled. See that directory's README for details.

## System prompts and personas

| Use for | Persona |
|---|---|
| General expert work, evidence-grounded decision support | [jayce-general.md](04-system-prompts/personas/jayce-general.md) |
| Broad multidisciplinary tasks needing a wider multi-section brief | [jayce-expanded-general.md](04-system-prompts/personas/jayce-expanded-general.md) |
| Coding, implementation, debugging, code review | [ekko-coding.md](04-system-prompts/personas/ekko-coding.md) |
| Software and system architecture, design trade-offs | [singed-architecture.md](04-system-prompts/personas/singed-architecture.md) |
| Technical writing, documentation, editing for clarity | [isha-writing.md](04-system-prompts/personas/isha-writing.md) |
| Investing, portfolios, long-horizon risk-adjusted returns | [mel-investing.md](04-system-prompts/personas/mel-investing.md) |
| Research, source evaluation, evidence-based conclusions | [heimerdinger-research.md](04-system-prompts/personas/heimerdinger-research.md) |
| Stress-testing an idea, challenging assumptions | [viktor-challenge.md](04-system-prompts/personas/viktor-challenge.md) |
| Making a decision, weighing trade-offs | [caitlyn-decisions.md](04-system-prompts/personas/caitlyn-decisions.md) |
| Cooking, recipes, ingredient substitution | [jericho-cooking.md](04-system-prompts/personas/jericho-cooking.md) |

Core system prompts are in [04-system-prompts/core/](04-system-prompts/core/) and image prompts in [04-system-prompts/upscale/](04-system-prompts/upscale/). Full listing: [04-system-prompts/README.md](04-system-prompts/README.md).

## Sources, attribution and licensing

- Detailed skill listings, categories and machine-readable data: [catalog/](catalog/).
- Provenance and attribution details: [ATTRIBUTION.md](ATTRIBUTION.md).
- License scope and third-party terms: [LICENSE](LICENSE).
- Verification notes: [docs/VERIFICATION.md](docs/VERIFICATION.md).

This is a curated collection. Third-party work remains attributed to its original authors. Applicable source and license information is recorded per item; unresolved verification is disclosed honestly. The root license applies to original curation and original materials in this collection and does not override third-party terms.

## Status

Structured, documented and ready for use. No completeness or universal "verification" is claimed for upstream content.
