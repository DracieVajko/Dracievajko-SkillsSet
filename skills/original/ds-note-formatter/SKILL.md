---
name: ds-note-formatter
description: "Format content for Synology DS Note / Note Station so it pastes cleanly and preserves structure, readability and checklist usability."
version: 1.0.0
author: DracieVajko
tags: [ds-note, formatting, checklist, synology, note-station]
category: productivity
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/ds-note-formatter/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# DS Note Formatter

Format content for Synology DS Note / Note Station so it pastes cleanly and preserves structure, readability and checklist usability.

## When to Use

- The user wants content formatted for DS Note / Synology Note Station.
- Applies to checklists, inspection notes, service notes, shopping lists, work logs, quick structured notes, copy-paste templates.

## Procedure

1. Output only the final note unless the user asks for explanation.
2. Prefer plain text with lightweight structure; keep one blank line between major sections.
3. Keep each actionable item on its own line; avoid deep nesting.
4. Avoid tables and decorative Markdown that may paste inconsistently.
5. Use short section titles on their own lines.
6. Group items by location, function or status when the source is messy.
7. Split overloaded lines into separate task lines when useful; preserve meaning, do not invent missing details.
8. Support modes: checklist-ready (one item per line), visible checkbox (`☐`/`☑`), plain structured note, mixed work-log (`TO CHECK`/`TO BUY`/`DONE`/`NOTES`).
9. For electrical/field-service notes, group by room, floor, zone or customer area; keep sockets, switches, lights, tightening, replacement and inspection as separate lines; use `TO BUY` for missing parts and `DONE` for completed interventions.

## Pitfalls

- Adding useless intro text.
- Over-explaining formatting decisions.
- Converting into formal business prose.
- Using large Markdown heading stacks when not requested.
- Using tables for simple task notes.
- Inventing missing context.
- Merging multiple actionable tasks into one long line.

## Verification

- The note is readable in the editor, plain-text copy and PDF export.
- Structure survives paste into DS Note's rich-text editor.
- No syntax errors or fragile formatting.
