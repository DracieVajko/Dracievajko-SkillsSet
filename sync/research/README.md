# Unresolved skills: research notes

Final pass, 2026-11-18. Every installed skill now has a public source that was
fetched, installed and hash-verified. A record is added to `catalog/items.json`
only after the public `SKILL.md` is byte-checked (line endings normalised).

Method: the hash in `sync/machines/*.json` was compared against candidates from
GitHub code search, repository search, hub inventory walks and web search. When
the public skill was the same skill but newer or differently packaged, the local
copy was replaced (with a backup) and the public version recorded.

## Last two, resolved by adopting the public version

| Skill | Public source | What changed |
|---|---|---|
| `editor-v1` | `HenokCodez/Motion-Studio`, `.agents/skills/workflow4-editor-v1` | Adopted the full public package (SKILL.md, WORKFLOW.md, assets, components, reference, scripts, sfx, template). The public skill is named `workflow4-editor-v1`; the installed skill keeps the `editor-v1` name through the catalog's `rename_to` field. |
| `orchestrate` | `hyperb1iss/hyperskills`, `skills/orchestrate` | Adopted the canonical MIT source (SKILL.md + references). |

Old copies are in `~/.config/opencode/skill-backups/20261118-131724-public/`
and `20261118-131759-editor-root/`.

## Earlier in the same day

`browser-automation`, `design-taste-frontend`, `doc`, `gws-gmail`,
`home-assistant`, `knowledge-base`, `meal-plan`, `multi-agent-orchestration`,
`spreadsheet`, `desloppify`, `humanizer`, `meeting-notes` and `higgsfield` were
matched exactly and recorded as link-only. Raw search evidence is in
`unresolved-matches*.json`.

## Final state

- 117 skills in the collection: **108 enabled and installed**, 9 disabled by
  `sync/optional.json` because they do the same job as a kept, better version:
  `creating-skills`, `summarize-meeting`, `code-reviewer`, `debugging-wizard`,
  `penetration-testing-guide`, `web-research`, `multi-agent-orchestration`,
  `reverse-engineering`, `generate-markdown-and-docx-documents`.
- `sync/verify-installed.py` reports `108 match, 0 differ, 0 missing`.
- No unresolved skills and no local or cross-computer `drift`.
- Disabled skills are moved to `~/.config/opencode/skills-disabled/` by
  `sync/prune-optional.py`; remove a name from `sync/optional.json` and run the
  installer to bring it back.
- `editor-v1` is the one renamed install: the source is
  `workflow4-editor-v1`, installed as `editor-v1`; the catalog carries the
  patched hash and `rename_to`, so both computers produce the same file.
