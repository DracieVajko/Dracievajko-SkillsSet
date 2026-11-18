# Machine sync

`sync/` describes one machine's installed agent-skill layout so another Windows
PC can reproduce it. It does not duplicate skill content: every skill is
installed once and the other agents see it through a Windows directory
junction.

| File | Purpose |
|------|---------|
| `manifest.json` | Snapshot: every installed skill, its upstream source, its install root, the junctions that mirror it. |
| `cindy-plugins.json` | Cindy plugins installed on the reference machine, with what each one needs to be authorized again. |
| `unresolved.md` | Per-machine snapshot: installed skills whose upstream is not verified. They stay out of the catalog and out of `skills/original/` until the upstream is found. |
| `generate-manifest.py` | Rebuilds `manifest.json` from the local machine plus `catalog/items.json`. |

The installer is `scripts/sync-skills.ps1`; it lives with the other scripts.

## Reproduce on a new machine

```powershell
git clone https://github.com/DracieVajko/Dracievajko-SkillsSet.git
cd Dracievajko-SkillsSet

# see what would happen, touch nothing
.\scripts\sync-skills.ps1 -DryRun

# install missing skills, then create the junctions
.\scripts\sync-skills.ps1

# also reinstall runtime dependencies (playwright-skill)
.\scripts\sync-skills.ps1 -InstallNodeModules
```

The script never overwrites an existing skill folder without `-Force`, and it
reports three things instead of guessing:

* **upstream drift** — the installed `SKILL.md` no longer matches the hash in
  the manifest, usually because upstream moved on or the copy was edited;
* **unresolved** — no upstream was identified, so the folder has to be copied
  by hand;
* **failures** — the clone or copy did not finish, run again.

## What is installed where

| Root | Owner | Mirrored into |
|------|-------|---------------|
| `~/.config/opencode/skills` | OpenCode, the OpenCode superpowers plugin, `scripts/install-skills.ps1` | `~/.agents/skills` |
| `~/.agents/skills` | Agent Skills installers (gsap, transitions, impeccable, skill-creator, deep-agents-memory) | `~/.claude/skills`, `~/.pi/agent/skills` |

Pi reads `~/.agents/skills` on its own, so a junction there is enough for Pi
and Cindy to see the same folder. If another tool has already created a plain
folder in a mirror location, the script leaves it alone and reports it rather
than deleting user data. The paths above describe the filesystem layout only;
the platforms this repository is tested on are Odysseus, Cindy, OpenCode and
OpenDesign.

Cindy's own skills (`cindy-plugin-creator`, `cindy-skill-creator`,
`cindy-theme-creator`, `learn`) ship inside the Cindy app. They are listed in
the manifest for completeness and are never copied between machines.

## What is never synced

* **Cindy plugins** — installed per device from the marketplace, with secrets
  in the per-device safe storage. Install the ids from `cindy-plugins.json`
  again and re-authorize them.
* **`node_modules`** — never copied; use `-InstallNodeModules`.
* **Secrets and account authorizations** — GitHub login, Google OAuth, ntfy
  token and the Tuya API key are per machine.

## Authorship

Nothing here relabels skill ownership. The manifest records one of three
values per skill:

| `authorship` | Meaning | Where the content lives |
|---|---|---|
| `original` | Written by the repository owner | `skills/original/` in this repo |
| `third-party` | Someone else's work, installed from upstream | Upstream repository; only a link/path in this repo |
| `unknown` | Upstream not identified | Not in this repo at all |

`third-party` and `unknown` skills are installed on a machine but are never
promoted into `skills/original/`, and their frontmatter keeps the upstream
author. `scripts/validate-frontmatter.py` enforces this in CI: a skill in
`skills/original/` must have `author: DracieVajko` and `authorship: original`,
and a skill in `skills/third-party/` may not claim either.

When a skill's upstream is resolved later, add it to `catalog/items.json` as an
external entry - that updates the manifest's `third-party` classification
without copying anyone's content.

## Keeping the manifest honest

```powershell
python sync/generate-manifest.py           # rewrite after adding or removing a skill
python sync/generate-manifest.py --check    # fail when manifest.json is stale
```

Add the new skill to `catalog/items.json` first so the manifest records where it
came from; otherwise it shows up as `unresolved`.
