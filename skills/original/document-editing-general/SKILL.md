---
name: document-editing-general
description: "General-purpose skill for creating, reading, editing and managing documents (markdown, text, code, etc.) in an editor panel."
version: 1.0.0
author: DracieVajko
tags: [document, editing, markdown, editor, create, update, general]
category: dev
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/document-editing-general/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Document Editing (General)

General-purpose skill for creating, reading, editing and managing documents (markdown, text, code, config, reports, notes) in an editor panel. Not for Word/PDF/PPTX (use docx/pdf/pptx skills).

## When to Use

- The user wants to create, edit, read or manage any document in an editor panel.
- Applies to markdown, code, text, config files, reports, notes or any structured content.

## Procedure

1. **Check the active document** before any edit — verify which document is currently open (content with line numbers is provided each turn).
2. **Edit in place (preferred)** — if a relevant document is already open, use edit with exact FIND/REPLACE pairs. Match text exactly (no line numbers, no tabs). Make the smallest possible change.
3. **Create a new document** only when no relevant document exists or the user explicitly asks for a new file. Set title, language and content.
4. **Full rewrite** only when more than 50% of content changes — use update with complete new content.
5. **Suggest changes** when the user asks for review/improvements without direct edits — use inline comments.
6. **Verify after edit** — re-read the changed section to confirm the edit applied correctly.
7. **Language tagging** — always set the correct language (markdown, python, javascript, json, yaml, text, etc.) for syntax highlighting and tooling.

## Pitfalls

- Creating duplicate documents instead of editing the active one.
- Using FIND text that does not match exactly (including whitespace).
- Including line numbers or tabs in FIND/REPLACE text.
- Using full rewrite for small edits (wasteful).
- Forgetting to set the language parameter on create.
- Editing the wrong document when multiple are open.

## Verification

- After edit, the changed section reads as intended.
- No duplicate documents created.
- Language tag matches content type.
- FIND text matched exactly once.
