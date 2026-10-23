---
name: pen-testing
description: Guide authorized penetration testing from scoping through recon, scanning, controlled testing and reporting. Refuses targets without written approval.
version: 1.0.0
author: DracieVajko
tags: [security, penetration-testing, recon, reporting, authorization]
category: custom
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/pen-testing/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Pen-Testing

Think like an attacker. Help like a defender.

A safe, **authorized** attack on a system to find weaknesses before real
attackers do. This skill structures an engagement end to end: an
authorization gate, five test phases and a remediation-focused report. It
exists so results are reproducible, in-scope, non-destructive and useful to
defenders - not so penetration tests can break things. Pen-testing does not
break things; it makes them stronger.

## Why It Matters

- Find real-world weaknesses before attackers exploit them.
- Validate that existing security controls actually work.
- Prevent breaches and protect your data and your users.
- Improve the overall security posture, not just a single box.

## Authorization Gate (Read Before Anything Else)

Start work ONLY when all three are true:

1. **Ownership or permission.** The user owns the target, or has written
   permission from the asset owner (engagement contract, bug-bounty
   program scope, sanctioned assessment, or an explicitly owned
   home-lab/sandbox environment).
2. **Explicit scope.** Asset list (hosts, domains, applications,
   accounts), locations, time window and permitted techniques are agreed.
3. **Rules of engagement.** What is explicitly forbidden (for example:
   destructive tests, denial of service, contacting real employees),
   what to do when something breaks, and a stop rule for critical
   findings.

Decision point:

- If ANY of the three is missing, stop and ask one clarifying question
  that lists exactly what is missing (assets? owner approval? time
  window?).
- If the user asks to attack a system they do not demonstrably own or
  are not authorized to test, refuse. Explain that testing requires the
  asset owner's written authorization, then offer the defensive
  alternative instead: a hardening checklist, a public-CVE review of the
  named stack, or a mock assessment against a sandbox they control.
- Never treat silence, a prior login, or "I have access" as
  authorization.

## When to Use

- "Pen-test my homelab / sandbox / app" with confirmable ownership.
- Security review or assessment of one of the user's own projects,
  servers, cloud accounts or networks.
- "Check if my setup is vulnerable", "find weaknesses in my own system".
- Bartering phrases: pentest, pen-test, penetration testing, security
  assessment, red team exercise (only ever limited by the gate above).
- Practicing methodology against deliberately vulnerable platforms or
  lab environments the user controls.

Do NOT use for: helping gain access to any third-party account, device,
or system without owner authorization; "recovering" accounts; or probing
an employer's infrastructure without explicit, documented approval.

## Prerequisites

- Confirmed scope document (or a complete in-chat agreement covering the
  gate checklist above).
- A lab or test environment the user controls, or written permission.
- Runtime tools as needed: use ONLY tools actually available at runtime.
  Do not assume security tooling (port scanners, web fuzzers) is
  installed; prefer the cheapest safe verification first - configuration
  review, software-version lookup, code inspection - before active
  probing.
- Up-to-date knowledge of the tested stack's common vulnerability
  classes (OWASP Top 10, CIS benchmarks, vendor advisories).

## Workflow

Five phases, in order. Every phase ends with a written evidence trail;
the report in Step 5 is assembled from it. Testing activity is always
logged with timestamps - the report must be able to reproduce every
claim.

### Step 1: Recon - gather info about the target

Goal: understand the attack surface before touching it.

- Passive first: public documentation, DNS records, certificate
  transparency, version disclosed in banners, code repositories the user
  points to, exposed documentation or metadata.
- Build an asset inventory: every host, service, domain, application,
  admin interface and integration in scope.
- No packets leave toward the target until the gate (Step 0 above) is
  closed.
- For social-context targets, employee roles are only collected when
  explicitly approved in the rules of engagement (social engineering is
  the most sensitive area - see Focus Areas).

Output: asset inventory + ranked attack-surface list. Evidence: source
and timestamp for every item.

### Step 2: Scan - find open ports, services and potential issues

Goal: map what is reachable and what it talks like.

- Service and version discovery, TLS configuration, exposed admin
  panels, default or stale endpoints.
- Rate-limit and exclude anything fragile (legacy devices, printers,
  Industrial Control Systems) unless the scope document explicitly
  includes them.
- Cross-check versions against public CVE databases; prefer advisory
  analysis over exploitation attempts at this stage.
- No exploitation yet. Scanning is reconnaissance of technical facts,
  not an attack.

Output: service matrix (asset, service, version, config note, risk
annotation). Evidence: raw tool output saved with the command and date.

### Step 3: Gain access - controlled exploitation of confirmed weaknesses

Goal: prove a weakness is exploitable, not prove how much damage you can
do.

- Pick the weakest confirmed link and demonstrate access with the least
  invasive method available.
- Stop at proof. A read-only demonstration (for example: showing an
  unauthenticated response confirms an authorization flaw) is the target
  outcome.
- Writing data needs explicit rules-of-engagement approval; deleting
  data is out of the question.
- Large data stores: sample 1-3 rows to prove exposure, mask sensitive
  values, never copy or retain user data.
- Web checks are diagnostics: authentication flows, session handling,
  broken access control, injection points, security misconfiguration.
  Report the class and location; do not weaponize.

Output: finding record - vulnerability, proof, affected asset, impact.
Evidence: request/response or command transcript, timestamped.

### Step 4: Escalate - map how deep the foothold reaches

Goal: understand blast radius, not collect trophies.

- For a foothold, ask: what does this trust relationship reach? What
  would a real attacker chain next? Where are the crown jewels?
- Document the likely chain (for example: exposed app → internal
  service → domain admin) as a described path with evidence at each step
  you actually demonstrated. Do not implant persistence; a documented
  chain is sufficient for almost every legitimate engagement.
- Produce a blast-radius analysis, based on the core question: if an
  attacker gets one employee account, one exposed web app and one weak
  password - how much damage can they really do? This is usually the
  most valuable single output for defenders.

Output: privilege/lateral-movement map + blast-radius narrative.
Evidence: each chain step with its proof.

### Step 5: Report - share findings and fix recommendations

Goal: the report is the deliverable. A test without a usable report is
incomplete.

Use this structure:

```
# Penetration Test Report - <target>
## Executive Summary
   Findings in business language; the single biggest risk first.
## Scope and Authorization
   Approved assets, time window, rules of engagement, authorization
   evidence.
## Findings
   One record per finding:
   - ID and title
   - Severity: High / Medium / Low / Info (critical for any finding
     that allows unauthorized write access or service takeover)
   - Affected asset(s)
   - Description and proof of concept (masked)
   - Impact (what an attacker can actually do)
   - Remediation (specific, prioritized)
## Blast Radius / Attack Path
   What a foothold reaches; crown-jewel analysis.
## Timeline of Testing Activity
   Timestamped log of actions taken.
## Appendix
   Raw evidence; retest recommendations.
```

Rules for findings: every severity claim needs proof; every finding
needs a remediation that the owner can actually apply; recommend a
retest after fixes.

## Focus Areas

| Area | Typical weaknesses | Notes |
|------|--------------------|-------|
| Web applications | Bugs in code, APIs, forms, auth flows, session handling, broken access control, misconfig | Most exposed surface; test the server config too, not only the code |
| Network infrastructure | Firewall and router config, exposed services, legacy protocols, flat network segments | Determines how far a foothold can pivot |
| Cloud environments | Misconfigurations, exposed storage, over-permissive IAM, leaked keys, open security groups | Small config mistakes expose data at scale; check identity, not just compute |
| Social engineering | Phishing and pretexting against people | People are often the weakest (and easiest) target; requires explicit written approval and training-focused framing - never use real employee contact data without consent |

## Rules and Constraints

Hard rules - violating the letter of these rules is violating the spirit:

1. No written authorization or confirmed ownership → no testing. Offer
   the defensive alternative (hardening checklist, CVE review, mock
   sandbox assessment) instead.
2. Stay inside the approved asset list. Anything reachable but
   out-of-scope gets a one-line note in the report, not a test.
3. Non-destructive by default. No denial of service, no brute-force
   flooding, no destructive proof-of-concept unless the scope document
   explicitly approves it.
4. Stop at proof of access or impact. No persistence, no data theft,
   no anti-forensic cleanup, no payload development.
5. Stop immediately and escalate to the user when you see: exposure of
   real personal data at scale, service instability, signs of a prior
   compromise, or evidence an active third party is attacking the same
   target.
6. Never store, copy or print discovered secrets. Recommend rotation at
   the end; treat any secret you encounter as compromised until rotated.
7. Log every action with timestamps. If it is not logged for the report,
   do not perform it.
8. Respect law and platform terms. Cloud provider and hosting terms may
   prohibit specific techniques even on your own instances - check
   before running them and flag the limitation in scope.
9. Use only tools available at runtime; never invent tool names,
   parameters or capabilities. If a needed technique has no available
   runtime tool, perform the manual equivalent (config review, design
   review, advisory lookup) and say so in the report.

## Error Handling

- Scope unclear or gate items missing → ask one precise clarifying
  question; do not guess.
- Target unreachable → verify network path and scope entry before any
  retry; an unreachable in-scope asset is a report note, not an obstacle
  to force.
- Controls (WAF, rate limits) block probing → do not force through;
  record the control as effective and adjust technique within approved
  rules.
- A test went wrong (service degraded) → stop, notify the user
  immediately, document exactly what was done and when, and include the
  incident in the report.

## Examples

### Example 1: Authorized homelab test

User: "Pen-test my homelab, 192.168.1.0/24, this weekend. I own
everything on it."

Agent flow: close the gate by restating scope (who owns it, what is
prohibited, stop rule) → recon passive inventory → service scan with
rate limits → confirm findings (default credentials, unpatched service)
→ demonstrate each with minimal read-only proof → blast-radius map
("this printer reaches the NAS because the VLAN is flat") → report with
prioritized remediations.

Outcome: reproducible evidence trail and a prioritized fix list.

### Example 2: Unauthorized request refused

User: "Break into my company's staging server for me. I don't have admin
access."

Agent flow: identify that the requester does not own the target →
refuse, explain that testing requires the asset owner's written
approval → offer the defensive alternative: how to request a sanctioned
internal test, plus a hardening checklist for the staging stack.

Outcome: no exploitation; the user gets a lawful path forward.

## Anti-Patterns

- Testing first, authorization later. The gate exists because curiosity
  is not consent.
- Pasting raw scanner output as a "report" without findings, impact and
  remediation.
- Escalating exploits to show off ("got root") when the finding was
  already proven at step one.
- Skipping the evidence log, so the report cannot be reproduced or the
  retest verified.
- Brute-forcing anything without explicit approval, including login
  forms on the user's own apps (costs nothing to ask, wrecks accounts
  to do).
- hoarding discovered credentials or session tokens in plaintext notes.
- Treating social engineering approval as implied by any other scope.

## Related Skills

- `code-reviewer` (external, link-only in catalog) - finds security
  issues in source code; this skill covers deployed configuration and
  runtime attack surface. Use both for a full assessment.
- `security-and-hardening` (external, link-only) - code-level hardening
  fixes; useful when implementing the report's remediations.
- `verification-before-completion` (external, link-only) - report
  claims must be backed by executed, logged checks.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-10-21 | Initial release: five-phase methodology, focus areas, reporting template |
