# Skill Specification — How to Write Skills

This document defines the standard structure, conventions, and best practices for creating skills in this repository.

## Skill File Structure

Each original skill lives in its own directory under `skills/original/`:

```
skills/
└── original/
    └── skill-name/
        ├── SKILL.md          # Main skill definition (required)
        ├── README.md         # Optional: human-readable overview
        ├── scripts/          # Optional: helper scripts
        ├── templates/        # Optional: template files
        └── assets/           # Optional: images, data files
```

External skills are not copied into this repository. They are recorded as links
in `catalog/links/`, `catalog/items.json` and `skills/third-party/README.md`.

## SKILL.md Format

The `SKILL.md` file is the canonical definition. It uses frontmatter + Markdown:

```markdown
---
name: skill-name
description: One-line description for the skill picker. When to invoke, triggers, scope.
version: 1.0.0
author: github-username
tags: [tag1, tag2, tag3]
category: category-name
---

# Skill Title

Brief intro: what this skill does, when to use it.

## When to Use

Explicit triggers — phrases, situations, task types that should invoke this skill.

## Prerequisites

- Required tools, accounts, configurations
- Expected environment setup

## Workflow

Step-by-step process the agent should follow.

### Step 1: Name

Details, commands, tools, decisions.

### Step 2: Name

...

## Rules & Constraints

- Hard rules (never do X)
- Preferences (prefer Y over Z)
- Edge case handling

## Examples

### Example 1: Scenario

User request → Agent actions → Outcome

### Example 2: Scenario

...

## Anti-Patterns

What NOT to do. Common mistakes.

## Related Skills

- `other-skill` — How it complements this one
- `another-skill` — When to use instead

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case, matches folder name) |
| `description` | Yes | Summary for the skill picker; aim for 160 characters or less |
| `version` | Yes | Semantic version (MAJOR.MINOR.PATCH) |
| `author` | Yes | GitHub username or "community" |
| `tags` | No | Array of searchable tags |
| `category` | Yes | Category label, for example `core`, `development` or `writing-docs` |
| `requires` | No | Array of skill dependencies |
| `conflicts` | No | Array of incompatible skills |

## Writing Principles

### 1. Be Explicit About Triggers
Don't make the agent guess. List exact phrases, keywords, and situations.

```markdown
## When to Use
- "Manage my TickTick tasks" → invoke ticktick-tasks
- "Deep research this topic" → invoke write-research-projects
- "Clean this repository" → use the repository-hygiene prompt
```

### 2. Prescribe, Don't Suggest
Use imperative language. The agent follows instructions literally.

```markdown
## Workflow
1. FIRST: Read the user's full request
2. THEN: Identify the core objective
3. NEXT: Check for existing solutions
```

### 3. Include Decision Points
Where the agent must choose, give clear criteria.

```markdown
## Step 3: Choose Approach
- If X: use Method A
- If Y: use Method B
- If unclear: ask user
```

### 4. Handle Failure Modes
Tell the agent what to do when things go wrong.

```markdown
## Error Handling
- If tool fails: retry with modified params
- If ambiguity: ask clarifying question
- If blocked: escalate to user with specific question
```

### 5. Reference Runtime Schemas
Never invent tool names or parameters. Always defer to runtime.

```markdown
## Tool Usage
- Use only tools available at runtime
- Treat runtime schema as source of truth
- Never assume tool capabilities
```

## Category Labels

Use these labels in the `category` frontmatter field. They are metadata, not
directory names; all original skills live directly under `skills/original/`.

| Category | Focus |
|----------|-------|
| `core` | Essential, always-available skills |
| `development` | Code, engineering, DevOps |
| `design` | UI/UX, visual, frontend |
| `ai-ml` | Model training, data, inference |
| `3d-blender` | Blender-specific workflows |
| `productivity` | Personal task management |
| `custom` | User-specific or cross-domain workflows |
| `web-automation` | Browser, testing, scraping |
| `thinking-frameworks` | Mental models, decision tools |
| `writing-docs` | Content, documentation, publishing |

## Naming Conventions

- **Skill folder**: `kebab-case` (e.g., `building-mcp-servers`)
- **Skill name (frontmatter)**: Same as folder
- **Display name**: Title Case (e.g., "Building MCP Servers")
- **Tags**: lowercase, hyphenated (e.g., `mcp`, `server-development`, `typescript`)

## Quality Checklist

Before submitting a skill, verify:

- [ ] `SKILL.md` exists with valid frontmatter
- [ ] `name` matches folder name exactly
- [ ] `category` is one of the documented labels
- [ ] Description is one line, ideally under 160 characters
- [ ] Triggers are explicit and specific
- [ ] Workflow steps are numbered and actionable
- [ ] No invented tool names or parameters
- [ ] Error/failure handling included
- [ ] Examples show real usage
- [ ] Related skills referenced
- [ ] Version starts at 1.0.0

## External Skills

Do not copy third-party skill code into this repository. To add an external
reference:

1. Add the direct raw URL to `catalog/links/skill-links.txt` or
   `catalog/links/pinned-links.txt`.
2. Add a matching record to `catalog/items.json` with `authorship: link-only`.
3. Add name, purpose, license and original link to
   `skills/third-party/README.md` when it belongs in the curated list.
4. Run `python scripts/update-category-index.py` and the tests.

A link is not a license grant. Verify the upstream license before copying or
redistributing any external content.

## Testing Skills

1. **Syntax**: Validate frontmatter YAML
2. **Load**: Test in OpenCode with `/skill load skill-name`
3. **Invoke**: Trigger via natural language
4. **Edge cases**: Ambiguous requests, missing tools, failures

## Updating Skills

- Increment version per semver
- Update `Version History` table
- Maintain backward compatibility when possible
- Document breaking changes clearly

---

*See [CONTRIBUTING.md](CONTRIBUTING.md) for submission process.*
