# Unresolved skills: research notes

These are the skills that remain without a verified public upstream after the
2026-11-18 pass. A record is only added to `catalog/items.json` when a public
`SKILL.md` matches the recorded hash exactly (line endings normalised).

Method: the hash in `sync/machines/*.json` was compared byte-for-byte against
candidates found by GitHub code search, repository search, hub inventory walks
and web search. A hash match proves the file, not the original author; entries
whose only match is a redistribution are labelled as a copy in
`compatibility_notes`.

| Skill | Candidate upstreams found | Why it is still unresolved |
|---|---|---|
| `editor-v1` | `HenokCodez/Motion-Studio` (`workflow4-editor-v1`) | hash differs; the public file is a derivative, not the installed version |
| `orchestrate` | `AtifAssari/MCP-Skills-Universe` (two copies) | hash differs; the public copies are older or edited |

## Resolved in this pass

Exact hash match and a link-only catalog record:

| Skill | Upstream |
|---|---|
| `browser-automation` | `FNOSP/fnos-dsh` |
| `design-taste-frontend` | `compozy/compozy` |
| `doc` | `letta-ai/skills` |
| `gws-gmail` | `JetBrains/skills` (v1.0.0 installed) |
| `home-assistant` | `balloob/llm-skills` |
| `knowledge-base` | `inkeep/open-knowledge-skills` |
| `meal-plan` | `ianseddon/cookbook` |
| `multi-agent-orchestration` | `qodex-ai/ai-agent-skills` |
| `spreadsheet` | `jasonkneen/openclicky` (hash-verified copy) |
| `desloppify` | `peteromallet/desloppify` (public data file may lag the installed v7 build) |
| `humanizer` | `blader/humanizer` (v4.0.0 installed) |

`meeting-notes` (`claude-office-skills/skills`) and `higgsfield`
(`OSideMedia/higgsfield-ai-prompt-skill`) were resolved by the other computer in
the same pass. The raw search evidence is in `unresolved-matches*.json`.

## Final state

- 117 skills installed; 115 have a verified source, 2 remain unresolved.
- `sync/verify-installed.py` reports `117 match, 0 differ, 0 missing`.
- Local copies agree with their source in every install root; cross-computer
  `drift` is empty after both computers reinstall from `sync/manifest.json`.
- Old copies replaced during this pass are under
  `~/.config/opencode/skill-backups/20261118-*-verify|upstream|drift/`.
