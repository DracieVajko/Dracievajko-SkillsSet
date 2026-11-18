# Installation and Usage

Everything in this page was verified against the installer scripts in
[`scripts/`](../scripts/). If a step here disagrees with the scripts, the
scripts are the truth - please open an issue.

## What gets installed

The installer copies the **original skills** from `skills/original/` into an
agent's skills directory. It does not install:

- external skills that are referenced by URL only (see
  [docs/CATEGORY_INDEX.md](CATEGORY_INDEX.md)),
- the bundled third-party copies under `skills/third-party/` (copy those
  manually if you want them),
- personas, system prompts or rule modules (they are files you reference
  directly).

## Requirements

| Requirement | Why |
|-------------|-----|
| Git | to clone the repository |
| PowerShell 5.1+ (Windows) or bash (Linux/macOS) | to run the installer |
| Python 3.9+ with PyYAML | only for the validation scripts, not for installing |

Install Python dependencies for the tooling with:

```bash
pip install --requirement scripts/requirements.txt
```

## Install into OpenCode (user level)

This installs every original skill into `~/.config/opencode/skills/` so it is
available in all your projects.

```powershell
# Windows
.\scripts\install-skills.ps1
```

```bash
# Linux / macOS
./scripts/install-skills.sh
```

### Options

| Windows | Linux/macOS | Meaning |
|---------|-------------|---------|
| `-Target <dir>` | `--target <dir>` | Install into a different directory, e.g. `.agents\skills` |
| `-BackupRoot <dir>` | `--backup-root <dir>` | Where replaced or removed folders are kept (default `~/.config/opencode/skill-backups`) |
| `-Uninstall` | `--uninstall` | Remove this collection's skills from the target directory |
| `-WhatIf` | `--dry-run` | Print the planned actions and change nothing |

Always try the dry run first if you are unsure:

```bash
./scripts/install-skills.sh --dry-run
```

### Backup behaviour

The installer **never overwrites an existing skill in place**. If a folder with
the same name already exists in the target directory, it is moved to a
timestamped backup first:

```
~/.config/opencode/skill-backups/20261112-104746/<skill-name>/
```

The same happens on every re-run, so each install leaves a dated snapshot of
what it replaced. Backups are yours to keep or delete.

## Install into a single project (project level)

Copy the skills you want into the project instead of the user directory:

```bash
# Linux / macOS
cp -r skills/original/* .agents/skills/
```

```powershell
# Windows
Copy-Item -Path skills\original\* -Destination .agents\skills\ -Recurse
```

Or point the installer at the project directory:

```bash
./scripts/install-skills.sh --target .agents/skills
```

## Updating installed skills

Re-run the installer. Each skill that is already installed is backed up to a
new timestamped folder and then replaced with the current version:

```bash
./scripts/install-skills.sh
```

## Uninstalling

The installer can remove this collection's skills without deleting anything:

```bash
./scripts/install-skills.sh --uninstall
```

```powershell
.\scripts\install-skills.ps1 -Uninstall
```

- Only folders whose names match the skills in `skills/original/` are touched.
  Other skills in the same directory stay where they are.
- Removed folders are **moved** into the backup directory, not deleted, so a
  mistaken uninstall can be undone by copying them back.

To restore a single skill from a backup:

```bash
cp -r ~/.config/opencode/skill-backups/20261112-104746/<skill-name> ~/.config/opencode/skills/
```

## Agent rules, prompts and personas

These are plain Markdown files - there is nothing to install.

| You want | Use |
|----------|-----|
| Project rules for OpenCode | Copy `instructions/opencode/project-template/` into the project root |
| A single rules file | Copy `AGENTS-combined.md` into the project root |
| Modular rules | Copy `AGENTS.md` and the `instructions/modules/` tree |
| Chat personas | Copy `prompts/personas/*.md` into your agent's persona folder |
| System prompts | Copy `prompts/system/*.md` and use them as custom instructions |

Do not use `AGENTS.md` and `AGENTS-combined.md` in the same project - they are
two formats of the same rules.

## Using the collection with other agent frameworks

The skills use the `SKILL.md` frontmatter convention, so they load in any
agent that reads that format. Copy the skill folders into the directory your
agent expects (commonly `.agents/skills/`, `.claude/skills/` or
`~/.config/opencode/skills/`) and make sure the frontmatter keeps `name`,
`description`, `version`, `author` and `category`.

External skills are URL references: open the link, read the upstream file and
place it wherever your agent expects it. Compatibility of an external skill
with a specific agent is not guaranteed by this repository.

## Verifying the installation

After installing, you can check the collection itself:

```bash
python scripts/validate-frontmatter.py        # skill metadata
python scripts/check-sync.py                  # rule copies are in sync
python scripts/update-category-index.py --check  # the generated index is current
python scripts/check-markdown-links.py        # relative Markdown links resolve
python -m unittest discover -s scripts -p "test_*.py"  # the tooling tests
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `opencode` does not list the skills | The agent loaded its config before the install | Restart the agent, or reload its configuration |
| The installer fails on Windows | Execution policy blocks the script | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `No skills found under: ...` | Running the script from the wrong directory | Run it from the repository root; the script resolves paths relative to itself |
| `ERROR: Missing link file` | A catalog link file was deleted | Restore `catalog/links/skill-links.txt` and `catalog/links/pinned-links.txt` |
| A skill does not appear after install | The folder name does not match the frontmatter `name` | The validator reports this; see [docs/SKILL_SPEC.md](SKILL_SPEC.md) |
| Validation fails with `ModuleNotFoundError: yaml` | PyYAML is missing | `pip install --requirement scripts/requirements.txt` |
| `Permission denied` when writing to the target directory | The target needs elevated rights | Use a project-local target with `--target .agents/skills` |

---

*Verified 2026-11-12 on Windows (PowerShell) and in bash: dry run, install,
re-install with backup, and uninstall.*
