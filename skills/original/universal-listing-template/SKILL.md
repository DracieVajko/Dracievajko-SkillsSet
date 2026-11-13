---
name: universal-listing-template
description: "Generate structured lists (TODO lists, inventory, tables) using AI and file operations."
version: 1.0.0
author: DracieVajko
tags: [list, template, productivity, organize, table]
category: productivity
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/universal-listing-template/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Universal Listing Template

Generate structured lists (TODO lists, inventory, comparison tables) using AI and file operations.

## When to Use

- The user wants to generate a structured list (TODO, inventory, table) and save it as a file.

## Procedure

1. **Define list structure** — gather requirements: type of list (bullet points, table, markdown), items and format.
2. **Generate content with AI** — create the list dynamically using file write tools.
3. **Export as file** — save in the desired format: Markdown (`.md`), plain text (`.txt`) or CSV (`.csv`).
4. **Verify output** — open the generated file and check correct structure, all items present, no syntax errors.

## Pitfalls

- Missing tools (write_file, read_file).
- Incorrect formatting (tables or markdown syntax errors).
- Unclear requirements leading to wrong list structure.

## Verification

- The generated file exists.
- All items are present.
- Format matches the user's requirements.
- No syntax errors.
