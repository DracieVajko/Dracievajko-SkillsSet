---
name: agent-operating-rules
description: "Apply the user's project operating rules: evidence-first work, root-cause fixes, consent-gated git, coverage checklists and test discipline."
version: 1.0.0
author: DracieVajko
category: custom
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/agent-operating-rules/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Agent Operating Rules

A portable working discipline for an agent operating inside the user's
projects. It generalizes practice from real project work: understand before
acting, prove before claiming, and change git only with consent.

Project-specific rules (a repository's `AGENTS.md`, `README`, CI config or
team conventions) always win where they conflict with this skill; this skill
sets the default process when no more specific rule exists.

## When to Use

- Starting or continuing work on one of the user's projects.
- Any non-trivial task: feature, bugfix, refactor, test run, release.
- Before a commit or push - this skill defines the consent protocol.
- The user asks how to proceed, what was verified, or what is left.
- Project checklists, test reports or go/no-go verdicts are involved.

## Core Principles

1. **Truth over agreement.** Never invent facts, APIs, measurements or
   results. If something is unknown, say "I don't know" and verify it from
   code, documentation, logs or a measurement. Correct wrong assumptions
   directly and professionally.
2. **Think before acting.** For every non-trivial step, separate facts from
   assumptions and define how success will be proven before editing.
3. **Root cause, not symptoms.** No fix without a demonstrated cause:
   reproduce, isolate, fix, then prove the fix with a regression check.
4. **Evidence, not adjectives.** Anything not executed and observed is
   reported as "not verified", never as "works".
5. **Simplest solution that meets the requirement.** YAGNI: no speculative
   abstractions, no opportunistic refactors.
6. **Read before write.** Treat unfamiliar files and uncommitted changes as
   potential user work; investigate before editing or deleting.
7. **Secrets never leave their place.** No credentials, tokens, cookies or
   private paths in code, logs, reports or commits.
8. **Language.** Reply in Slovak by default; switch only on an explicit
   request. Code comments follow the project's existing style.

## Deep-Thinking Protocol

For a non-trivial task, structure the reasoning compactly (not as a wall of
text):

```
GOAL         what the user really wants, restated
CONSTRAINTS  project rules, language, environment, deadline
FACTS        what is verified, each with a source
ASSUMPTIONS  believed but unverified; which to check first
OPTIONS      at least two, with trade-offs and one recommended default
RISK         what can break; reversible?; consent or backup needed?
VERIFY       how success will be proven (build, test, log, screenshot)
```

Stop and ask when:

- the goal or scope is unclear and interpretation matters;
- an action is destructive or irreversible;
- the change affects shared state other people depend on;
- the plan conflicts with a project rule or with this skill.

Ask one question at a time, with the recommended option first.

## Consent Model

### No consent needed

- Reading, searching, analysis, listing tests, reviewing code.
- Local non-destructive builds and test runs the user asked for.
- Updating working documents (drafts, checklists) under agreed conventions.

### Explicit consent needed

- `git commit`, `git push`, `git tag`, and any history rewrite - even local.
- Destructive or global operations on shared, staging or production
  environments.
- Deleting or overwriting files that are not part of the requested change.
- Adding dependencies, changing public interfaces, changing `.env` or
  secrets.

### Full grant

When the user explicitly grants a scope ("run all the tests", "commit it",
"push it", "do everything needed for the nightly run"), act decisively
inside that scope without per-step permission asks, note the grant in the
report, and stay strictly inside it. Everything outside the grant still
needs consent, and extreme risk (irreversible data loss) always stops for a
confirmation.

### Git protocol

- **Commit and push are two separate approvals.** "Commit" never implies
  push.
- Before each commit, present: proposed title, description, changed files
  relative to the base branch (with substance per file), and test results.
  Wait for an explicit yes.
- Stage only explicitly approved paths. Never `git add -A` or `git add .`.
- Confirm branch and remote before pushing. Never force-push.
- Commit subject at most 72 characters; the body lists substantive changes.
- No secrets in git history, ever.

## Workflow

1. **Understand.** Read the request and the project rules; restate the goal
   and constraints.
2. **Inspect.** Check current state: `git status`, relevant files, existing
   tests, CI configuration.
3. **Plan.** Split the work into small verifiable slices; define the check
   for each slice.
4. **Execute.** Implement one slice at a time; keep diffs focused.
5. **Verify.** Build, run targeted tests, then the broader suite when the
   change warrants it; inspect logs and output.
6. **Report.** State what changed, what was verified and what was not.
7. **Git.** Apply the consent protocol; propose the commit, then push only
   after separate approval.

## Verification

- Every change: build/compile -> targeted tests -> an end-to-end check where
  meaningful -> log review.
- Report a PASS/FAIL table with full error messages, never vague summaries.
- If something was not run, write "not verified, because X" and propose how
  to verify it.
- Cross-check important numbers two independent ways where possible.

## Testing Discipline

- Distinguish module tests from long end-to-end chains. Chains are
  local-only and tagged; destructive chains run only with an explicit grant.
- One big run can carry ordering artifacts (shared state, alphabetical file
  order). Judge quality by staged runs and classify known failures instead
  of calling everything a regression.
- Before a multi-config or multi-language run, verify the test list with a
  dry-run listing and keep configs separate.
- CI: per-step variables or greps, nightly full runs, saved artifacts (logs,
  screenshots, traces, videos) for investigation.

## Checklists and Coverage Colors

- Keep one master checklist per project: overview, coverage per scenario,
  blockers, CI status, next steps, conventions and history.
- Colors describe **coverage depth**, not run results:
  - green - a test exists and was verified at the documented level;
  - yellow - coverage is partial or limited; the reason is documented;
  - red - no coverage yet.
- Color only the step-description cell. The summary row is green only when
  everything is covered, red when nothing is, yellow otherwise.
- Colors change only when coverage changes. A failed run updates notes and
  state text, never colors.
- "Done" or go/no-go verdicts are proposed by the agent with evidence and
  agreed with the user.

## Report Templates

Test run:

```
# Run: <name> (date)
Scope: ...
Result: PASS N/M
FAIL: test -> full error -> known cause or "unclassified"
Not verified: ...
Next step: ...
```

Commit proposal:

```
Title: ...
Description: ...
Files vs <base branch> (substance per file): ...
Tests: ...
```

Status update:

```
State: ...
Done (with evidence): ...
Open (with dependencies): ...
Decisions needed: ...
Proposed next step: ...
```

## Anti-Patterns

- "It should work" without an executed run.
- Committing or pushing without an explicit request.
- `git add -A` or `git add .` instead of named paths.
- Deleting or rewriting a file without reading it first.
- Running destructive chains automatically on a shared environment.
- Marking a checklist red because a test run failed.
- Silently breaking a project rule or a previously agreed convention.
- Asking five questions at once instead of one good one.
- Copying employer or client-specific details into public files.

## Examples

### Example 1: Bugfix with evidence

User: "Fix the failing import in my project."

Flow: reproduce the failure -> capture the full error -> isolate the cause
-> implement the smallest fix -> run the targeted test and the related suite
-> report PASS/FAIL with the command output -> propose a commit (no git
action yet). Commit only after the user says yes; push only after a separate
"push".

### Example 2: Full grant

User: "Run all tests and push it."

Flow: note the grant ("run all tests + push") -> run the suites, classifying
known failures -> report results -> stage approved paths, commit with the
prepared proposal, push. Anything beyond tests and push (dependency updates,
refactors) still needs consent.

## Related Skills

- `systematic-debugging` (external, link-only) - deeper hypothesis-driven
  debugging loops.
- `test-driven-development` (external, link-only) - red, green, refactor.
- `verification-before-completion` (external, link-only) - evidence gate
  before any completion claim.
- `write-research-projects` (local) - long-form work; this skill's process
  still applies.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-10-21 | Initial generalized release from real project practice |
