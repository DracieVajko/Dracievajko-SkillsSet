---
name: generate-markdown-and-docx-documents
description: "Create a new document from a user-provided outline and content, output both a Markdown file and a Word (DOCX) file for download."
version: 1.1.0
author: DracieVajko
tags: [document-creation, markdown-docx-generation]
category: documents
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/generate-markdown-and-docx-documents/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Generate Markdown and DOCX Documents

Create a new document from a user-provided outline and content, outputting both a Markdown file and a Word (DOCX) file (or their base-64 strings) for download.

## When to Use

- The user wants to create a new document from an outline and content, delivered as Markdown and DOCX.

## Procedure

1. **Gather the document specification** — title and a list of top-level sections, each with heading text and body content (plain text, markdown tables, fenced code blocks, bullet/numbered lists). Store in a `content_spec`.
2. **Assemble the Markdown text** — build `# {title}` followed by `## {heading}` and `{body}` for each section.
3. **Write the Markdown file** — create `document.md` with the assembled content.
4. **Verify the Markdown file** — confirm creation and optionally read the first bytes.
5. **Convert Markdown → DOCX** — prefer Pandoc (`pandoc document.md -o document.docx --standalone`); if unavailable, fall back to a pure-Python conversion using `python-docx`, `markdown` and `beautifulsoup4`.
6. **Validate the DOCX file** — confirm it exists and is non-empty; verify file type.
7. **Prepare files for delivery** — upload both files if an upload tool is available; otherwise encode them as base-64 and return with decoding instructions.
8. **Communicate the result** — inform the user that Markdown and DOCX were generated; ask if further edits are needed.

## Pitfalls

- Creating duplicate documents instead of editing an existing one.
- Using a converter that is not installed.
- Forgetting to validate the DOCX output.

## Verification

- Both `document.md` and `document.docx` exist and are non-empty.
- DOCX opens correctly in a word processor.
- Content matches the provided outline.
