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

| Persona | Purpose |
|---|---|
| [Jayce.md](04-system-prompts/Jayce.md) | Versatile generalist; prioritizes truth and evidence. |
| [Jayce-Expanded.md](04-system-prompts/Jayce-Expanded.md) | Expanded multi-section variant of Jayce. |
| [Ekko.md](04-system-prompts/Ekko.md) | Senior software engineer; understand first, implement second. |
| [Singed.md](04-system-prompts/Singed.md) | Systems architect; simplest reliable architecture. |
| [Isha.md](04-system-prompts/Isha.md) | Technical writer; clarity and precision. |
| [Mel.md](04-system-prompts/Mel.md) | Chief investment officer style; long-term, risk-adjusted returns. |
| [Heimerdinger.md](04-system-prompts/Heimerdinger.md) | Research analyst; evidence-based conclusions. |
| [Viktor.md](04-system-prompts/Viktor.md) | Strategic challenger; stress-tests ideas and assumptions. |
| [Caitlyn.md](04-system-prompts/Caitlyn.md) | Decision advisor; clear trade-off analysis. |
| [Jericho.md](04-system-prompts/Jericho.md) | Personal chef; recipe discovery and cooking. |

Additional system prompts are listed in [04-system-prompts/README.md](04-system-prompts/README.md).

## Sources, attribution and licensing

- Detailed skill listings, categories and machine-readable data: [catalog/](catalog/).
- Provenance and attribution details: [ATTRIBUTION.md](ATTRIBUTION.md).
- License scope and third-party terms: [LICENSE](LICENSE).
- Verification notes: [docs/VERIFICATION.md](docs/VERIFICATION.md).

This is a curated collection. Third-party work remains attributed to its original authors. Applicable source and license information is recorded per item; unresolved verification is disclosed honestly. The root license applies to original curation and original materials in this collection and does not override third-party terms.

## Status

Structured, documented and ready for use. No completeness or universal "verification" is claimed for upstream content.
