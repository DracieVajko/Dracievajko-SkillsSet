<!--
SKILL.md template for new original skills.

Copy this directory-listing structure: skills/original/<skill-name>/SKILL.md
Replace every <...> placeholder. Keep frontmatter valid; the validator
(scripts/validate-frontmatter.py) enforces it. See docs/SKILL_SPEC.md for
the full specification and docs/CONTRIBUTING.md for the submission process.
-->
---
name: <skill-name>            # kebab-case, MUST match the folder name
description: >-               # one line, <=160 chars, carries the trigger
  Use when <trigger phrases/situations>. <What the skill produces.>
version: 1.0.0                # semantic version
author: <github-username>     # or "community"
tags: [<tag1>, <tag2>]        # lowercase, hyphenated
category: <category>          # see docs/SKILL_SPEC.md category table
---

# <Skill Title>

One short paragraph: what this skill does and when to reach for it.

## When to Use

Explicit triggers — phrases, situations and task types that should invoke this
skill. Make the agent's decision mechanical, not a guess.

- "<exact user phrase>" → invoke this skill
- <situation or task type>

## Prerequisites

- Required tools, accounts, configurations (only what actually exists at runtime)
- Expected environment setup

## Procedure

Step-by-step workflow. Numbered, imperative, with decision points.

### Step 1: <Name>

Details, commands, tools, decisions. If a choice exists, give criteria:

- If <condition A>: use <approach A>
- If <condition B>: use <approach B>
- If unclear: ask the user

### Step 2: <Name>

...

## Pitfalls

What NOT to do. Common mistakes and the failure modes of each step above.

- Never <mistake>; instead <correct behavior>
- If a tool fails: <fallback>

## Verification

How to prove the skill worked. What evidence to present when done.

- Run / inspect <concrete check>
- Report what was verified and what was not

## Related Skills

- `<other-skill>` — how it complements this one
- `<another-skill>` — when to use instead

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |
