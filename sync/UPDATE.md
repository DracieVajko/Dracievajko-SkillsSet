# Update a computer to the newest versions

Every skill version lives in this repository. This prompt makes a computer match
it: it reinstalls from the collection, so old local copies are replaced and
nothing is taken from the machine's own leftovers.

Run it in `MySkillInstructionPromptsPresets` after `git pull`. Paste the block
below into Cindy on the computer you want to update.

---

```text
Bring this computer to the newest versions in this repository. Work only from
files in the repository; do not invent skill names or compare against old local
copies.

STEP 1 - newest collection
  git pull --rebase origin master
  git status --short        (must be empty; if not, stop and report)
Show the last three commit subjects so I can see which version I am installing.

STEP 2 - reinstall every skill from the collection
  .\scripts\sync-skills.ps1 -Manifest sync\manifest.json -DryRun
  .\scripts\sync-skills.ps1 -Manifest sync\manifest.json -Force
-Force is required: it replaces older local copies with the recorded versions.
The script prints "installed", "already present", "differs" and "unresolved";
unresolved skills are reported and never guessed.

STEP 3 - prove it
  python sync\verify-installed.py
Success means "0 differ". Skills listed as missing exist only on another
computer; say which ones, do not install anything extra.

STEP 4 - Cindy plugins
Read sync\cindy-plugins.json, compare with ghost_list, and install the missing
ones through the marketplace (ghost_market_search, then ghost_market_install
with the exact plugin_id and release_id). The entry with namespace "local"
(tuya-home) has no marketplace release: install it from its GitHub repository
if it is not present. Never authorize accounts, keys or OAuth yourself.

STEP 5 - record this computer
  python sync\generate-manifest.py
  python sync\build-collection.py
  git status --short
Commit only sync\machines\<this machine>.json, sync\manifest.json,
sync\collection.json and sync\unresolved.md, with the message
"Refresh this computer's snapshot", then push.

Answer with:
  1. which commit is installed,
  2. verify-installed output (counts only),
  3. plugins installed, skipped and still needing authorization,
  4. anything you could not do.
```

## What this does not cover

| Item | Why |
|---|---|
| The 13 skills without a verified upstream | They are reported, never installed from a guess. See `sync/research/README.md`. |
| Plugin authorization (Gmail, Drive, Calendar, ntfy, Tuya) | Secrets are per device; you approve them yourself. |
| `tuya-home` | Local development copy, no marketplace release; install from its repository. |
| Skills that only exist on the other computer | `verify-installed.py` lists them as missing instead of installing unknown content. |
