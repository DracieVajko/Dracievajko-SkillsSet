# Shared skill and plugin collection

`sync/` is one collection for every computer, not one collection per machine.
A skill is installed once from its source on each computer, and the other
agents see it through a Windows directory junction. No third-party content is
copied into this repository.

A computer only writes its own evidence file, `machines/<machineId>.json`.
The shared files are built from all evidence files, so two computers cannot
overwrite each other's inventory:

```powershell
python sync\generate-manifest.py    # this computer -> machines\<machineId>.json
python sync\build-collection.py     # all evidence -> collection.json, manifest.json, unresolved.md
```

| File | Purpose |
|------|---------|
| `collection.json` | **The collection**: every skill and plugin, how it installs, which agents see it, where it was seen, coverage gaps and hash drift. |
| `manifest.json` | The same collection in the schema `scripts/sync-skills.ps1` installs from. This is the only install manifest. |
| `machines/<machineId>.json` | Raw evidence from one computer: installed skills, harness roots, app-managed skills, junctions, drift. Never edited by hand. |
| `cindy-plugins.json` | Plugins for Cindy, OpenCode and OpenDesign, with what each one needs to be authorized again. |
| `optional.json` | Disabled skills (not installed); empty when everything is enabled. |
| `prune-optional.py` | Moves disabled skills out of every agent root into `~/.config/opencode/skills-disabled/`. |
| `CINDY-INSTALL.md` | Ready-to-paste prompt that installs the skills, then the plugins, then reports what still needs the owner. |
| `UPDATE.md` | Ready-to-paste prompt that updates a computer to the newest versions in the collection. |
| `verify-installed.py` | Checks every installed skill against the recorded hash; `0 differ` is the success line. |
| `unresolved.md` | Skills with no verified upstream. They stay out of the catalog and out of `skills/original/`. |
| `generate-manifest.py` | Writes this computer's evidence file. |
| `build-collection.py` | Merges every evidence file into the shared collection. The merge is monotonic: a skill is never dropped because one snapshot is missing. |

## Apply the collection to a computer

```powershell
git pull
.\scripts\sync-skills.ps1 -DryRun    # preview: what installs, what is unresolved
.\scripts\sync-skills.ps1            # install missing skills and create junctions
python sync\prune-optional.py        # move disabled skills out of every root
python sync\generate-manifest.py     # record this computer as evidence
python sync\build-collection.py      # refresh the shared collection
```

`sync-skills.ps1` never overwrites an existing skill folder without `-Force`.
It reports upstream drift, unresolved skills and failures instead of guessing.
`-InstallNodeModules` also runs `npm install` for skills that declare
`needsNodeModules`.

A skill that exists in a mirror location as a real folder is left alone and
reported. Deleting user data is never automatic.

## What is installed where

| Root | Owner | Mirrored into |
|------|-------|---------------|
| `~/.config/opencode/skills` | OpenCode, the OpenCode superpowers plugin, `scripts/install-skills.ps1` | `~/.agents/skills`, `~/.claude/skills`, `~/.qwen/skills` |
| `~/.agents/skills` | Agent Skills installers, Cindy | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.qwen/skills` |

`~/.pi/agent/skills` is in the mirror list only when Pi is installed; the
installer skips the rule when the parent directory does not exist. The same
applies to any other agent root that is not present.

These paths describe the filesystem layout only. The platforms this repository
is tested on are Odysseus, Cindy, OpenCode and OpenDesign. Other agent folders
are mirrored for convenience when they exist; that is not a support claim.

Cindy's own skills (`cindy-plugin-creator`, `cindy-skill-creator`,
`cindy-theme-creator`, `learn`) ship inside the Cindy app. Codex's five system
skills ship inside Codex. Both groups are listed in the evidence files for
completeness and are never copied between computers.

## Plugins

`cindy-plugins.json` is the single plugin inventory:

* `plugins[]` — Cindy plugins, installed from the marketplace and authorized
  per device. `opendesign-trial` is the OpenDesign plugin.
* `opencodePlugins[]` — plugins kept in `opencode.jsonc`.
* `platforms` — which platform each group belongs to.

Plugin folders, tokens and OAuth grants are per device and are never stored
here. Each computer installs the ids again and authorizes them there.

## What is never synced

* **Cindy, OpenDesign and OpenCode plugins** — installed per device, with
  secrets in the per-device safe storage. Install the ids from
  `cindy-plugins.json` again and re-authorize them.
* **`node_modules`** — never copied; use `-InstallNodeModules`.
* **Secrets and account authorizations** — GitHub login, Google OAuth, ntfy
  token and the Tuya API key are per machine.

## Authorship

Nothing here relabels skill ownership. The collection records one of three
values per skill:

| `authorship` | Meaning | Where the content lives |
|---|---|---|
| `original` | Written by the repository owner | `skills/original/` in this repo |
| `third-party` | Someone else's work, installed from upstream | Upstream repository; only a link/path in this repo |
| `unknown` | Upstream not identified | Not in this repo at all |

`third-party` and `unknown` skills are installed on a computer but are never
promoted into `skills/original/`, and their frontmatter keeps the upstream
author. `scripts/validate-frontmatter.py` enforces this in CI: a skill in
`skills/original/` must have `author: DracieVajko` and `authorship: original`,
and a skill in `skills/third-party/` may not claim either.

When a skill's upstream is resolved later, add it to `catalog/items.json` as an
external entry. That updates the collection's `third-party` classification
without copying anyone's content.

## Keeping the shared files honest

```powershell
python sync\generate-manifest.py --check   # this computer's evidence is current
python sync\build-collection.py --check    # collection.json, manifest.json, unresolved.md are current
```

`build-collection.py --check` runs in CI. It is deterministic: the same
evidence files always produce the same collection.

The merge is monotonic. If a computer's evidence file is missing, its skills
stay in `collection.json`; the correct fix is to restore the evidence, not to
delete the skill. `gaps` is a coverage checklist, not a separate collection.
