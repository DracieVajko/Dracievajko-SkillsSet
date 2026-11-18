# Unresolved skills: research notes

These skills are installed on the other computer but no public file matched the
recorded `SKILL.md` hash, so they stay out of the catalog and out of
`skills/original/`. This page records the leads so the next pass starts from
evidence instead of a blank search.

Method: the hash in `sync/machines/*.json` was compared byte-for-byte (line
endings normalised) against `SKILL.md` candidates found by GitHub code search,
repository search, hub inventory walks and web search. A record is only added to
`catalog/items.json` when a file matches exactly.

| Skill | Candidate upstreams found | Why it is still unresolved |
|---|---|---|
| `browser-automation` | `danielsuguimoto/skills`, `xicv/browser-automation-skill`, `ssrjkk/agent-skills`, `Jinhong270/AI-Agent`, `shahfarzane/claude-code-browser-skills` | no file matches the recorded hash; several independent skills share this name |
| `design-taste-frontend` | none found | no public `SKILL.md` with this name |
| `desloppify` | `peteromallet/desloppify`, `Parcha-ai/parcha-skills`, `docxology/codomyrmex`, `databuddy-analytics/databuddy` | hash differs; the tool has many re-packaged variants |
| `doc` | none found | name too generic to search; no frontmatter match |
| `editor-v1` | none found | no public `SKILL.md` with this name |
| `gws-gmail` | `aiskillstore/marketplace` (`skills/googleworkspace/gws-gmail`), `omriariav/workspace-cli`, `kcchien/skills` | hash differs; the file exists upstream under `aiskillstore/marketplace` |
| `home-assistant` | `homeassistant-ai/skills` (`home-assistant-best-practices`), `nolte/claude-home-assistant` | hash differs, and the name may be a local rename |
| `humanizer` | `blader/humanizer`, `Aboudjem/humanizer-skill`, `ugudlado/agent-skills` | hash differs; at least three separate humanizers exist |
| `knowledge-base` | `inkeep/open-knowledge-skills` (declared in frontmatter) | the declared repository has no file with this hash |
| `meal-plan` | `caseyWebb/groceries-agent-data`, `St0nefish/agent-toolkit`, `brandonmartinez/meal-planner` | hash differs |
| `multi-agent-orchestration` | `composio-community/opencode-skills` (`skills/multi-agent-orchestration`) | hash differs, so the installed copy was edited or is older |
| `orchestrate` | none found | no public `SKILL.md` with this name |
| `spreadsheet` | none found | name too generic; no frontmatter match |

A hash mismatch does not prove the candidate is wrong: the installed copy may be
an older or locally edited version. To promote one of these, either find the
commit whose `SKILL.md` matches the hash, or decide that the candidate is the
intended upstream and reinstall from it, accepting the newer content.

## Resolved in this pass

Matched exactly and recorded as link-only: `meeting-notes`
(`claude-office-skills/skills`) and `higgsfield`
(`OSideMedia/higgsfield-ai-prompt-skill`). Earlier passes resolved 15 more; see
`unresolved-matches*.json` in this directory for the raw evidence.

## Version alignment (2026-11-18)

Every skill installed on this computer was compared against its recorded source
and the twelve that had drifted were reinstalled from it: `brainstorming`,
`code-documenter`, `code-reviewer`, `context-engineering`, `debugging-wizard`,
`fine-tuning-expert`, `impeccable`, `reverse-engineer-anything`,
`skill-creator`, `transitions-dev`, `using-superpowers`, `wordpress-pro`.

All 42 installed skills now match their source byte for byte. The previous
copies are in `~/.config/opencode/skill-backups/20261118-align/`. The ten
remaining differences are between computers, not against upstream: they are
listed as `drift` in `sync/collection.json` and disappear once the other
computer reinstalls from the same manifest.
