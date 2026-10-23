---
name: repository-hygiene
description: Use when cleaning a repository, preparing a commit, or removing temporary files, generated artifacts or ad-hoc fix scripts.
version: 1.0.0
author: DracieVajko
tags: [repository, hygiene, git, cleanup, temporary-files, generated-files]
category: development
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/repository-hygiene/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Repository Hygiene

Keep the repository in a state where another competent developer can clone it,
understand what is authoritative, install it, run it and verify it. Cleanup is
classification before deletion, never blind deletion.

The long-form checklist lives in `prompts/system/repository-hygiene.md` in the
collection repository. This skill is the executable short form for day-to-day
project work.

## When to Use

- Cleaning a repository or preparing it for a commit, release or handoff.
- Removing temporary diagnostics, logs, build output or generated artifacts.
- Finding `fix.py`, `fix1.py`, `patch*.py`, `*_fixed.py`, `working_version.py`
  or similar ad-hoc files.
- Deciding whether an untracked or unexpected file belongs in Git.
- Auditing a repository for secrets, local machine paths or private data.

Do not use it to delete files whose purpose is unknown. Investigate first.

## Core Principle

Preserve user work. Every file gets one classification before any action:

| Class | Action |
|-------|--------|
| Canonical source | Keep; edit the real implementation, not a copy |
| Useful documentation | Keep or move to the documented location |
| Test or fixture | Keep; make sure it is discoverable and repeatable |
| Committed configuration | Keep; remove secrets and machine-specific values |
| Generated artifact | Remove from Git; add to `.gitignore` |
| Local-only file | Keep locally; ignore it in Git |
| Temporary diagnostic | Remove after integrating anything useful |
| Secret or credential | Remove, rotate if exposed, replace with a safe example |
| Dead or duplicate code | Remove only after proving it is unused |
| Unknown | Stop and inspect; do not delete |

## Workflow

1. **Inventory.** Inspect the root tree, `git status`, current branch, recent
   commits, changed and untracked files, `.gitignore`, manifests, build/test
   configuration and CI files.
2. **Classify.** Assign every suspicious file to a class above. Read the file
   before deciding. Check references before calling code dead.
3. **Integrate.** If a temporary fix contains a real change, apply it to the
   canonical module, add or update a focused test, then delete the temporary
   file.
4. **Clean.** Remove only the classified temporary/generated files. Do not
   reformat, rename or reorganize unrelated content.
5. **Verify.** Re-run the relevant tests and checks. Inspect `git status` and
   the final diff.
6. **Report.** State what was removed, what was kept, what was moved, what was
   verified and what remains uncertain.

## Temporary Patch Rule

- Never keep a parallel implementation as the solution.
- Diagnose what the temporary file actually changes.
- Compare it with the canonical implementation and the current tests.
- Integrate the valid part into the canonical source file.
- Add or update a regression test for the behavior.
- Delete the temporary file and any generated output in the same task.
- If the file contains work you cannot verify, keep it outside the repository
  and report it as an open item.

## Before Git Operations

- Check the branch, remote, staged files and the full diff.
- Stage explicit paths; never `git add -A` or `git add .` by default.
- Do not commit secrets, local paths, logs, caches, model files or build output.
- Do not commit generated files unless the project intentionally versions them.
- Keep one canonical implementation; no `main_fixed.py` or `working_version.py`.
- Commit and push only with the user's explicit consent.

## Secrets and Privacy

- Search for API keys, tokens, passwords, private keys, cookies, session data,
  database URLs, webhook secrets and cloud credentials.
- Inspect `.env`, `.env.*`, `*.pem`, `*.key`, `credentials.*`, `secrets.*` and
  similar files.
- If a secret was committed, remove it, replace it with a sanitized example and
  tell the user to rotate it. Removing it from the current tree does not remove
  it from history.
- Keep personal data, private hostnames, LAN addresses and local filesystem
  paths out of public files.
- Never paste secrets into an issue, report, screenshot or chat.

## Generated and Local Files

- Remove build output, caches, compiled binaries, coverage reports, test
  reports, notebook checkpoints, IDE metadata, OS metadata and runtime state.
- Do not commit model weights, checkpoints, embeddings, vector databases or
  large generated datasets unless the project explicitly requires them.
- Add the correct patterns to `.gitignore`; do not rely on memory.
- Keep committed examples sanitized: `config.example.yaml`, `.env.example`.
- Keep local overrides local: `.env`, `config.local.yaml`.

## Documentation and Dead Code

- Keep README, setup, test and usage instructions accurate after cleanup.
- Delete stale generated documentation, not the source that generates it.
- Remove commented-out code, debug prints and disabled validation only after
  confirming they are not intentional.
- Mark uncertain documentation as uncertain; do not invent missing steps.
- Report unrelated technical debt instead of expanding the cleanup scope.

## Verification Checklist

- [ ] Every removed file was classified and read first.
- [ ] Temporary fixes were integrated into the canonical source.
- [ ] Tests were run after cleanup and the result is reported.
- [ ] `git status` contains only intended changes.
- [ ] The diff contains no secrets, logs, caches or generated artifacts.
- [ ] `.gitignore` covers the removed local/generated files.
- [ ] Documentation still matches the actual commands and layout.
- [ ] Remaining uncertainty and unverified items are stated.

## Anti-Patterns

- Deleting by extension or filename pattern without reading the file.
- Keeping `fix1.py` because deleting it feels risky.
- Committing generated files because they were already there.
- Adding a broad `.gitignore` rule that hides source files.
- Rewriting history or force-pushing to hide a secret.
- Cleaning unrelated parts of the repository because you are already there.
- Reporting "clean" without checking `git status` and the diff.

## Related Skills

- `agent-operating-rules` (local) - consent-gated git, evidence and verification.
- `prompts/system/repository-hygiene.md` - full cleanup checklist.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-10-23 | Initial release: classification workflow, temporary patch rule, secrets, generated files and verification checklist |
