---
name: book-to-skill
description: "Convert a book or article into a reusable skill using AI and web data."
version: 1.0.0
author: DracieVajko
tags: [book, skill, research, learning, extraction]
category: knowledge
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/book-to-skill/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Book-to-Skill Converter

Extract knowledge from a book or article and convert it into a reusable skill.

## When to Use

- Converting a book or article into a reusable skill using AI and web data.

## Procedure

1. **Fetch book content** — use a web browser to download the book or article as a PDF or text file; save to a known location.
2. **Extract key sections** — use AI to summarize chapters or key points; prompt with "Summarize these chapters into bullet points:" followed by the copied content.
3. **Generate skill template** — structure the summarized content into a `SKILL.md` with frontmatter (name, description, when_to_use) and sections (When to Use, Procedure, Pitfalls, Verification).
4. **Save as skill** — create a new file named `extracted_skill.md` (or appropriate name) with the structured content; save to a known location.
5. **Verify output** — open the generated `SKILL.md` and check completeness and correct structure.

## Pitfalls

- Incorrect or inaccessible URL.
- Poor summarization missing key details.
- Manual copy-paste errors.
- Incomplete or malformed skill structure.

## Verification

- All key points from the source are included.
- The skill is usable as intended.
- Structure follows When to Use, Procedure, Pitfalls, Verification.
