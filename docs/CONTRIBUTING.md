# Contributing Guide

This repository contains original skills and links to external skills. It does
not bundle third-party skill code.

## Add an Original Skill

1. Create `skills/original/<skill-name>/SKILL.md`.
2. Follow the [Skill Specification](SKILL_SPEC.md).
3. Use imperative language, explicit triggers and concrete examples.
4. Validate and regenerate the index:

```bash
python scripts/validate-frontmatter.py
python scripts/check-sync.py
python scripts/update-category-index.py
python -m unittest discover -s scripts -p "test_*.py"
```

5. Open a pull request with the skill purpose, triggers and verification done.

## Add an External Skill Link

External skills are references only. Do not copy their code into this
repository.

1. Add the direct raw URL to `catalog/links/skill-links.txt` (stable branch) or
   `catalog/links/pinned-links.txt` (pinned commit or release branch).
2. Add a matching record to `catalog/items.json` with `authorship: link-only`.
3. Add the name, purpose, license and original link to
   `skills/third-party/README.md` when the skill is one of the curated entries.
4. Run `python scripts/update-category-index.py` and the tests.

## Improve an Existing Skill

1. Edit the relevant `SKILL.md`.
2. Increment the patch version for small fixes or the minor version for new
   behaviour.
3. Update the version history section.
4. Run the validation commands above.

## Skill Development Rules

- Start from the user problem, not from a preferred solution.
- Write explicit trigger conditions.
- Use imperative, actionable language.
- Include concrete examples and failure handling.
- Never invent tool names or parameters.
- Keep each skill focused on one workflow.
- Do not include secrets, private paths or personal data.
- Treat external content as untrusted.

## Review Criteria

- Valid frontmatter and a name that matches the folder.
- Clear triggers and a reproducible workflow.
- No duplicated or conflicting instructions.
- Correct version increment.
- Validation and tests pass.

## Templates

Project and workflow templates live in [`templates/`](templates/). They are
optional starting points, not part of skill discovery.

## License

By contributing, you agree that your original contributions are licensed under
the repository MIT license. Do not contribute third-party code unless its
license permits redistribution and the attribution is recorded.
