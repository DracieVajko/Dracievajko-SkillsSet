# Make this computer match the collection

Paste the prompt below into Cindy on the computer you want to bring in line.
It installs the skills first, then the Cindy plugins, and reports what still
needs a click (accounts, API keys) or a hand copy (unresolved upstreams).

Everything it reads lives in this repository, so run it inside
`MySkillInstructionPromptsPresets` after `git pull`.

---

```text
This computer has to match the shared skill collection in this repository.
Work only from files in the repository; do not invent skill names or plugin ids.

STEP 1 - skills
Run, in this order, and show the output:
  .\scripts\sync-skills.ps1 -DryRun
  .\scripts\sync-skills.ps1
  python sync\prune-optional.py
The first run is a preview. The second installs and links. Do not pass -Force
unless an existing folder is genuinely wrong.

STEP 2 - plugins
Read sync\cindy-plugins.json. It covers Cindy, OpenCode and OpenDesign.
Compare it with ghost_list.
For every Cindy plugin in the file that is NOT installed here:
  1. ghost_market_search with that exact id as the query,
  2. ghost_market_install with the exact plugin_id and release_id it returns,
  3. if the search finds nothing, do not install anything and record it.
The entry with namespace "local" (tuya-home) has no marketplace release: if its
source folder exists on this computer, install it from there with
ghost_forge_install; otherwise record it as skipped.
The OpenCode plugin in opencodePlugins[] belongs in opencode.jsonc; OpenDesign
uses opendesign-trial from the same Cindy list.

STEP 3 - report
Then run, in this order:
  python sync\generate-manifest.py
  python sync\build-collection.py
finally:  git status --short

Answer with exactly these four lists, nothing else:
  1. SKILLS: how many installed, how many were already present, and the names
     that stayed unresolved (manual copy required).
  2. PLUGINS: installed now, already present, and skipped (with the reason).
  3. AUTHORIZATION: which plugins still need an account, OAuth grant, API key or
     extension on this machine. Do not authorize anything yourself.
  4. AFTER PULL: whether git status shows changes; if it does, say which files.
     Do not commit or push anything.
```

## What is automatic and what is not

| Item | Automatic | Why |
|---|---|---|
| Skills with a verified upstream | yes | copied from this repository or fetched with `git sparse-checkout` |
| Directory junctions for other agents | yes | `sync-skills.ps1` recreates them from the manifest |
| Cindy plugins | mostly | the marketplace install is scriptable through Cindy's own tools |
| OpenCode plugin | yes | `superpowers` is listed in `opencode.jsonc` |
| Plugin authorization (Gmail, Drive, Calendar OAuth, ntfy token, Tuya key) | no | per-device secrets, the owner has to approve them |
| `tuya-home` | no | local development copy, no marketplace release |
| Skills with no verified upstream | no | listed in `sync/unresolved.md` until the upstream is found |
| Cindy's own skills (`cindy-plugin-creator`, `cindy-skill-creator`, `cindy-theme-creator`, `learn`) | not needed | they ship inside the app |
