# System Prompts and Personas

System prompts and personas organized by purpose. Every file is a standalone prompt: use its content as a system message, or reference the file from your agent configuration.

| Directory | Contents | Count |
|-----------|----------|-------|
| [`core/`](core/README.md) | General-purpose system prompts | 5 |
| [`personas/`](personas/README.md) | Task-specific personas (Arcane-inspired names) | 10 |
| [`upscale/`](upscale/README.md) | Image generation and upscale prompts | 3 |
|  | **Total** | **18** |

## Which persona is good for what

| Use for | Persona | File |
|---------|---------|------|
| General expert work, evidence-grounded decision support | Jayce | [`personas/jayce-general.md`](personas/jayce-general.md) |
| Broad multidisciplinary tasks needing a wider multi-section brief | Jayce (expanded) | [`personas/jayce-expanded-general.md`](personas/jayce-expanded-general.md) |
| Coding, implementation, debugging, code review | Ekko | [`personas/ekko-coding.md`](personas/ekko-coding.md) |
| Software and system architecture, design trade-offs | Singed | [`personas/singed-architecture.md`](personas/singed-architecture.md) |
| Technical writing, documentation, editing for clarity | Isha | [`personas/isha-writing.md`](personas/isha-writing.md) |
| Investing, portfolios, long-horizon risk-adjusted returns | Mel | [`personas/mel-investing.md`](personas/mel-investing.md) |
| Research, source evaluation, evidence-based conclusions | Heimerdinger | [`personas/heimerdinger-research.md`](personas/heimerdinger-research.md) |
| Stress-testing an idea, challenging assumptions | Viktor | [`personas/viktor-challenge.md`](personas/viktor-challenge.md) |
| Making a decision, weighing trade-offs | Caitlyn | [`personas/caitlyn-decisions.md`](personas/caitlyn-decisions.md) |
| Cooking, recipes, ingredient substitution | Jericho | [`personas/jericho-cooking.md`](personas/jericho-cooking.md) |

Display names are the intended identity. Where a source filename combined a personal alias with the Arcane-inspired name, the Arcane-inspired name is used as the display name. Full provenance is in [`personas/README.md`](personas/README.md).

## Core system prompts and image prompts

Not persona-specific: [`core/`](core/README.md) holds general behavioural presets (general, coding, cults3d-listing, trading, repository-hygiene) and [`upscale/`](upscale/README.md) holds the image upscaling prompts (upscale-basic, upscale-portrait, upscale-translate).

## Notes

- All maintained prompt content is translated into English without changing behavioral meaning
- Instructions to respond in the user's language (Slovak default) remain intact
- Arcane-inspired display names recovered from source filenames and content
- No invented names for prompts that never had Arcane associations
- Jayce-Expanded is retained as a meaningful variant (not demonstrably redundant)
