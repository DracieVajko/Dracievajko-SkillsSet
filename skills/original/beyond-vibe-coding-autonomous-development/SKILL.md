---
name: beyond-vibe-coding-autonomous-development
description: "Practical skill for AI-era software development based on Addy Osmani's 'Beyond Vibe Coding' — intent-driven workflows, prompt engineering, the 70% problem, code review/refinement, AI prototyping, autonomous agents, and production-ready AI-assisted engineering."
version: 1.0.0
author: DracieVajko
tags: [ai-assisted-development, vibe-coding, autonomous-agents, prompt-engineering, software-engineering, github-copilot, cursor, claude-code]
category: dev
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/beyond-vibe-coding-autonomous-development/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Beyond Vibe Coding: Autonomous Development

A practical skill for adopting AI coding assistants (GitHub Copilot, Cursor, Claude Code, etc.) in real production work.

## When to Use

- Starting new projects with AI scaffolding.
- Reviewing, debugging, or hardening AI-generated code.
- Moving from prototype to production.
- Setting up autonomous background agents.
- Establishing team workflows for AI-assisted development.

## Procedure

1. **Assess your position on the AI coding spectrum.** Choose deliberately per task: vibe coding for spikes, prototypes and learning; AI-assisted engineering for production code, security-sensitive areas and long-lived systems.
2. **Formulate clear intent before prompting.** Write a short spec first: problem, constraints (stack, performance, security, compliance), acceptance criteria, non-goals. Feed this as context, not a one-line prompt.
3. **Apply structured prompting.** Use role + context + task + constraints + output format; few-shot examples; chain-of-thought ("think step by step"); iterative refinement; negative constraints ("no external dependencies").
4. **Solve the 70% problem.** AI gets you ~70% there; the remaining 30% (edge cases, integration, testing, hardening) is human engineering. Never commit code you have not read and understood. Run the code before accepting. Write tests first (TDD with AI). Integrate incrementally.
5. **Review, refactor and own generated code.** Trace implementation to intent; check the majority-problem (AI defaults to common patterns — are they right for your context?); audit readability; use reproduce → isolate → hypothesize → verify → fix for debugging; refactor for maintainability; test at unit, integration and E2E levels.
6. **Prototype workflow.** Concept → spec (1 page), scaffold with AI, build one vertical slice end-to-end, iterate on feedback, then run a hardening checklist before production (error handling, validation, auth, logging, monitoring, performance budgets, accessibility).
7. **Production web apps with AI.** Scaffold repo/CI/lint/types/tests; design schema (AI suggests, you decide); define API contracts first (OpenAPI), then generate stubs; AI generates unit tests for business logic, you write integration/E2E; validate with load tests, security scans, accessibility audits.
8. **Security, maintainability, reliability.** Audit AI code for SQL injection, XSS, path traversal, auth bypass, secrets, insecure defaults, supply-chain risks; run SAST/DAST. Use property-based and mutation testing. Enforce architectural boundaries, document decisions (ADRs), track AI-generated tech debt. Treat AI as a junior developer; you are the senior reviewer.
9. **Deploy autonomous background agents.** Use for long-running refactors, test generation, dependency upgrades, documentation sync, codebase analysis. Define goal, scope, constraints, success criteria and rollback plan. Use multiple models (planner + coder + reviewer) with human-in-the-loop approval for merges, deletions, external API calls and schema changes. Log all actions; alert on failures; track cost.
10. **Prepare for the future.** Adopt AI-generated test suites, automated bug reproduction, root-cause analysis; AI-driven UX iteration and accessibility audits; AI for sprint planning and risk identification; express requirements as executable specs. Shift from "code writer" to "intent architect".

## Pitfalls

- Treating vibe coding as a replacement for engineering judgment.
- Accepting AI output without reading — subtle bugs, security holes, unmaintainable code.
- Skipping the intent/spec phase — "prompt and pray" yields prototype quality.
- Letting AI choose architecture by default (majority problem).
- No testing strategy — AI generates happy-path code; you must define edge cases.
- Over-relying on autonomous agents without guardrails.
- Ignoring IP/licensing — AI may reproduce copyrighted code.
- No rollback plan for agent actions.
- Skill atrophy — if you stop writing code, you lose the ability to review AI output.

## Verification

- You can articulate the difference between vibe coding and AI-assisted engineering and choose per task.
- Every AI-generated commit passes human read-through, test suite, security scan, lint/type check.
- You have a documented prompting template (role, context, task, constraints, output format).
- Prototypes have a hardening checklist before production deployment.
- Autonomous agents run with defined scope, approval gates, monitoring and cost limits.
- Team has shared AI usage policy, review standards and sign-off rules.
- You can debug AI-generated code without asking AI to fix it.
<!-- END SKILL CONTENT (cleaned) -->
