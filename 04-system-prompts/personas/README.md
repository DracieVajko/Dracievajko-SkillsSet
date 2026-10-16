# Personas

Task-specific behavioural profiles with Arcane-inspired display names. Each file is a standalone system prompt: use its content as a system message, or reference the file from your agent configuration.

The display name is the intended identity. Where a source filename combined a personal alias with the Arcane-inspired name, the Arcane-inspired name is used as the display name. The file name encodes the intended use, for example `ekko-coding.md` is Ekko, used for coding.

## Which persona is good for what

| Use for | Persona | File |
|---------|---------|------|
| General expert work, evidence-grounded decision support | Jayce | [`jayce-general.md`](jayce-general.md) |
| Broad multidisciplinary tasks needing a wider, multi-section brief | Jayce (expanded) | [`jayce-expanded-general.md`](jayce-expanded-general.md) |
| Coding, implementation, debugging, code review | Ekko | [`ekko-coding.md`](ekko-coding.md) |
| Software and system architecture, design trade-offs | Singed | [`singed-architecture.md`](singed-architecture.md) |
| Technical writing, documentation, editing for clarity | Isha | [`isha-writing.md`](isha-writing.md) |
| Investing, portfolios, long-horizon risk-adjusted returns | Mel | [`mel-investing.md`](mel-investing.md) |
| Research, source evaluation, evidence-based conclusions | Heimerdinger | [`heimerdinger-research.md`](heimerdinger-research.md) |
| Stress-testing an idea, challenging assumptions | Viktor | [`viktor-challenge.md`](viktor-challenge.md) |
| Making a decision, weighing trade-offs | Caitlyn | [`caitlyn-decisions.md`](caitlyn-decisions.md) |
| Cooking, recipes, ingredient substitution | Jericho | [`jericho-cooking.md`](jericho-cooking.md) |

## Details and provenance

| File | Persona | Role | Source/Provenance | Notes |
|------|---------|------|-------------------|-------|
| `jayce-general.md` | Jayce | Versatile expert generalist — truth > agreement | SystemPrompts/Personas/Odysseus_Jayce_Generalist.txt | Primary generalist persona |
| `jayce-expanded-general.md` | Jayce | Multidisciplinary generalist — expanded multi-section variant | SystemPrompts/Personas/Odysseus_Jayce_Generalist_Expanded.txt | Meaningful expanded variant of Jayce, preserved |
| `isha-writing.md` | Isha | Technical writer — clarity and precision | SystemPrompts/Personas/Elias_Isha_Writer.txt | Source filename combined alias "Elias" with Arcane-inspired "Isha" |
| `mel-investing.md` | Mel | Chief Investment Officer — long-term risk-adjusted returns | SystemPrompts/Personas/Adrian_Mel_GeneralInvestor.txt | Source filename combined alias "Adrian" with Arcane-inspired "Mel" |
| `singed-architecture.md` | Singed | Systems architect — simplest reliable architecture | SystemPrompts/Personas/Atlas_Singed_SystemArchitect.txt | Source filename combined alias "Atlas" with Arcane-inspired "Singed" |
| `ekko-coding.md` | Ekko | Senior software engineer — understand first, implement second | SystemPrompts/Personas/Brono_Ekko_Coder.txt | Source filename combined alias "Brono"/"Bruno" with Arcane-inspired "Ekko" |
| `caitlyn-decisions.md` | Caitlyn | Decision advisor — decisive trade-off analysis | SystemPrompts/Personas/Markus_Caithlyn_DecisionAdvisor.txt | Source filename combined alias "Markus"/"Marcus" with Arcane-inspired "Caithlyn" |
| `heimerdinger-research.md` | Heimerdinger | Research analyst — evidence-based conclusions | SystemPrompts/Personas/Orion_Heimerdinger_Researcher.txt | Source filename combined alias "Orion" with Arcane-inspired "Heimerdinger" |
| `viktor-challenge.md` | Viktor | Strategic challenger — stress-test ideas | SystemPrompts/Personas/Victor_Thinker.txt | Content confirms Arcane-inspired thinker persona; filename spelling "Victor" |
| `jericho-cooking.md` | Jericho | Personal chef — recipe discovery and cooking | SystemPrompts/Personas/Jericho_PersonalChef.txt | Existing chosen persona name; no lore interpretation added |

See [`../README.md`](../README.md) for the directory map and [`../core/README.md`](../core/README.md) for the non-persona prompts.
