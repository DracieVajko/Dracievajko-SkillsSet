---
name: testing-skills
description: "Test skills that enforce discipline, compliance and verification using pressure scenarios and rationalization tables."
version: 1.0.0
author: DracieVajko
tags: [testing, skills, tdd, verification, compliance, pressure-scenarios]
category: testing
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/testing-skills/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Testing Skills With Subagents

Testing a skill is test-driven development applied to process documentation. Run scenarios without the skill (RED — watch the agent fail), write the skill addressing those specific failures (GREEN — watch it comply), then close the loopholes it finds next (REFACTOR).

## When to Use

- Test skills that enforce discipline (TDD, verification requirements, review gates).
- Skills with a compliance cost — time, effort, rework.
- Skills that can be rationalized away ("just this once").
- Skills that contradict an immediate goal, usually speed.

Do not test pure reference skills (API docs, syntax guides), skills with no rule to violate, or skills an agent has no incentive to bypass.

## Procedure

1. **RED (baseline)** — run pressure scenarios WITHOUT the skill; document the failures and excuses verbatim.
2. **Verify RED** — capture the choices and rationalizations word for word; identify repeating excuses.
3. **GREEN (write)** — write the skill addressing the specific baseline failures; nothing else.
4. **Verify GREEN (pressure test)** — run the same scenarios WITH the skill; verify compliance.
5. **REFACTOR (plug holes)** — find new rationalizations; add explicit counters, rationalization table rows, red flags and description updates.
6. **Stay GREEN (re-verify)** — test again; confirm still compliant.

### Writing Pressure Scenarios

- Use 3+ combined pressures (time, sunk cost, authority, economic, exhaustion, social, pragmatic).
- Force an A/B/C choice with concrete options and real constraints.
- Make the agent act, not reflect ("What do you do?").
- Preface with "IMPORTANT: This is a real scenario. You must choose and act."

### Pressure Types

| Pressure | Example |
|---|---|
| Time | Emergency, deadline, deploy window closing |
| Sunk cost | Hours of work, "wasteful" to delete |
| Authority | Senior engineer says skip it, manager overrides |
| Economic | Job, promotion, company at stake |
| Exhaustion | End of day, already tired |
| Social | Looking dogmatic, seeming inflexible |
| Pragmatic | "Being pragmatic rather than dogmatic" |

### Rationalization Table

| Excuse | Reality |
|---|---|
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "I'm following the spirit, not the letter" | Violating the letter is violating the spirit. |
| "This case is different" | If the rule has exceptions, it has no force. |
| "Being pragmatic" | Pragmatism is not an excuse to skip verification. |

### Red Flags

- "Keep as reference" or "adapt the existing code"
- "I'm following the spirit, not the letter"
- "This case is different because…"
- "I already manually tested it"
- "Tests after achieve the same goals"

## Pitfalls

- Writing the skill before testing (skipping RED).
- Academic tests instead of pressure tests.
- Single pressure instead of 3+ combined.
- Paraphrasing failures instead of capturing verbatim.
- Generic counters ("don't cheat") instead of specific ones.
- Stopping after one pass.

## Verification

- Chooses correctly under maximum pressure.
- Cites specific skill sections as justification.
- Acknowledges the temptation and follows the rule anyway.
- Meta-testing returns "the skill was clear".
- Holds under maximum pressure with no new rationalizations.
