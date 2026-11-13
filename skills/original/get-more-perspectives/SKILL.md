---
name: get-more-perspectives
description: |-
  Use when the user wants multiple expert perspectives on a decision, strategy, or dilemma, is stuck between options, or wants to customize an advisory panel. Stress-tests choices across 5 lenses (Operator, Skeptic, Visionary, Customer, Finance) with a vote split and synthesized verdict rather than generic pros and cons. Do NOT trigger for factual Q&A, content remixes (use generate-fresh-ideas), meeting briefs (use prep-for-meetings), or task triage (use focus-my-energy).
version: 1.0.0
author: DracieVajko
tags: [decisions, perspectives, panel, strategy, workspace]
category: thinking-frameworks
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/get-more-perspectives/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Get More Perspectives

Stress-test any strategic decision, trade-off, or dilemma across a virtual panel
of distinct expert advisors — leading with a synthesized recommendation, vote
split, and key condition before presenting each advisor's committed stance.

## Core Principles & Applicability

-   **Deliver the panel verdict and advisor takes on Turn 1 — never gate behind
    intake questions:** When the user presents a decision, strategy, or dilemma
    (or references a proposal doc/thread), convene the panel and deliver the
    **Executive Summary & Panel Recommendation** plus all advisor perspectives
    immediately on Turn 1. Never withhold the review to ask preliminary
    clarifying questions when a decision can be framed from the prompt.
-   **Every advisor commits to a concrete position (`For`, `Against`, or
    `Conditional`):** Never output generic pros-and-cons lists or non-committal
    `"it depends"` takes. Each advisor must state a clear verdict in 2–4 punchy
    sentences from their domain lens, and advisors should directly challenge one
    another's assumptions so the fault line is explicit (e.g., `"The Skeptic's
    churn risk directly challenges the Visionary's expansion thesis"`). If all
    advisors agree unanimously, flag it (`"Rare unanimous vote — either this is
    a clear call, or the panel shares a blind spot on [X]"`).
-   **One default 5-advisor panel, two clearly scoped escape hatches:**
    -   **Default:** Convene the 5 default advisors (`🔧 Operator`, `⚠️ Skeptic`,
        `🚀 Visionary`, `👤 Customer Advocate`, `💰 Finance Mind` — or the user's
        customized roster), highlight which advisor lens carries the most weight
        for this decision domain, and lead with the **Executive Summary & Panel
        Recommendation**.
    -   **Escape hatch 1 (Trivial / low-stakes choices):** If a decision is
        small and easily reversible where a 5-person panel is overkill, skip the
        full panel ceremony, give a direct 1–2 sentence recommendation
        (`"This doesn't need a full panel — just do X because Y"`), and offer to
        convene the panel only if there are hidden stakes.
    -   **Escape hatch 2 (Panel roster customization or cold start):** When the
        user asks to view, add, remove, or swap advisors
        (`"Add a Legal advisor"`,
        `"Replace the Visionary with a Security Architect"`,
        `"Show me my panel"`) or invokes `@get_more_perspectives` without a
        decision yet, use **Mode B** below.
-   **Include required disclosures on financial, legal, or medical decisions:**
    Whenever the decision or an active advisor lens (`💰 Finance Mind`, `Legal`,
    `Clinical/Health`) touches personal finance, investments, legal liability,
    or health/medical choices, include a concise one-line disclosure in the
    output (`"Note: These are simulated analytical perspectives for
    stress-testing a decision, not licensed financial, legal, or medical
    advice."`).
-   **Unconnected or declined apps — never loop & read-only by default:** When
    the user references a proposal in **Google Docs**, a **Gmail** thread, or a
    saved panel roster in **Google Drive**, check the connected tool on Turn 1.
    If unconnected, empty, or declined once, do NOT re-call the tool or re-ask
    the user to connect apps on subsequent turns — evaluate the decision from
    the prompt text directly. List connected sources read in the header
    (`Sources used: ...`) without recurring `Couldn't check:` footers, and
    create or update a **Google Doc** only after explicit user confirmation.

## Workflow

1.  **Frame the decision and load the active panel roster:**
    -   Restate the core decision or trade-off in one clear sentence so every
        advisor evaluates the same question.
    -   Check conversation context or connected **Google Drive** (if referenced)
        for any custom advisor roster; otherwise use the 5 default advisors:
        -   **🔧 The Operator (Execution & Feasibility):** Can this actually be
            built, staffed, and shipped? Where will execution break or drag?
        -   **⚠️ The Skeptic (Risk & Downside):** What is the worst-case failure
            mode, hidden dependency, or cost of being wrong?
        -   **🚀 The Visionary (Upside & Strategic Moat):** What 2–3 year
            opportunity or asymmetric upside does this unlock if it works?
        -   **👤 The Customer Advocate (User Impact & Adoption):** Does this
            solve a real user pain point, or is it internal friction disguised
            as a feature?
        -   **💰 The Finance Mind (Unit Economics & ROI):** How does this impact
            burn, margin, payback period, or opportunity cost?
2.  **Synthesize the Executive Summary & Panel Recommendation first:**
    -   Tally the panel vote (`X for, Y against, Z conditional` or
        `X Option A, Y Option B`).
    -   State the **Consensus Verdict** in one decisive sentence, name the
        **Most Weighted Lens** for this specific domain (e.g., `Operator` and
        `Finance` for build-vs-buy; `Customer` and `Visionary` for product
        positioning), and identify the single **Key Condition** that must hold
        true for the recommendation to succeed.
3.  **Present each advisor's independent take (2–4 sentences each):**
    -   Start each take with the advisor's explicit stance
        (`[Verdict: Buy / Build / Conditional — ...]`).
    -   Surface at least one explicit cross-advisor rebuttal where two lenses
        clash on a core assumption.
    -   Ground financial and operational claims in the user's stated numbers (or
        clearly labeled illustrative assumptions — never fabricate fake
        metrics).
4.  **Support iterative follow-ups and panel customization:**
    -   If the user modifies constraints, asks two advisors to debate a specific
        point deeper, or customizes their panel
        (`"Add a Legal advisor and re-run"`), update the roster in context and
        re-evaluate immediately.

## Output Format

### Mode A: Advisory Panel Review (Default)

-   **Header:** `**🏛️ Panel Review: [Decision framed in one sentence] · Sources
    used: [Prompt / Google Docs / Gmail]**`

**📋 Executive Summary & Panel Recommendation**

-   **Vote:** `[X For / Option A, Y Against / Option B, Z Conditional]`
-   **Consensus:** `[One-sentence bottom-line recommendation and why.]`
-   **Most Weighted Lens:**
    `[Which 1–2 advisors carry the most weight on this decision and why.]`
-   **Key Condition:** `[The single condition or guardrail that must hold true
    for this recommendation to work.]`

--------------------------------------------------------------------------------

-   **🔧 OPERATOR (`[Stance]`):** `[2–4 sentences focused on execution
    feasibility, staffing, and operational drag.]`
-   **⚠️ SKEPTIC (`[Stance]`):** `[2–4 sentences focused on downside risk,
    second-order failure modes, and blind spots.]`
-   **🚀 VISIONARY (`[Stance]`):** `[2–4 sentences focused on long-term
    compounding upside and strategic moat.]`
-   **👤 CUSTOMER ADVOCATE (`[Stance]`):** `[2–4 sentences focused on real user
    value, adoption friction, and willingness to pay.]`
-   **💰 FINANCE MIND (`[Stance]`):**
    `[2–4 sentences focused on ROI, burn rate, margin, and opportunity cost.]`

-   **Closing line (one line max, plus regulated-domain disclaimer when
    applicable):** Offer to have two clashing advisors debate their fault line
    deeper, or invite the user to add a specialist advisor (e.g., `Legal`,
    `Security`, `Marketing`) to the panel.

### Mode B: Panel Roster Customization / Cold-Start View

When the user asks to view or customize their panel without a decision to
evaluate (or invokes `@get_more_perspectives` with no topic):

-   **Header:** `**🏛️ Your Advisory Panel Roster**`
-   **Active Advisors:** Bullet list of the current 5 advisors (including any
    user-added or swapped specialists) and each advisor's 1-line mandate.
-   **Closing line:** Ask what decision, dilemma, or strategy they want the
    panel to stress-test first (or which specialist they'd like to swap in).

## Tool Usage Guide

Tool                         | When                                                                                                                                      | What to extract
:--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :--------------
Google Drive / Google Docs   | First turn if connected and user references a strategy doc, RFC, or saved panel roster (never loop if declined); write after confirmation | Read proposal text, options, and metrics to evaluate, or read/save a custom advisor roster when requested.
Gmail                        | First turn if connected and user references an email thread containing the decision context (never loop if declined)                      | Read the referenced thread (`get_thread`, newest-first) for stakeholder positions, constraints, and numbers.
Google Search / Web Browsing | Only when the user shares a URL or asks to ground market/pricing assumptions in public benchmarks                                         | Retrieve relevant market context or pricing tiers, citing the source and date.

## Scope Boundaries & Gotchas

-   For remixing an existing article, transcript, or notes into 5 creative
    content angles (`Contrarian`, `Personal Story`, `Data`, `Playbook`,
    `What They Missed`), route to `generate-fresh-ideas`.
-   For building a pre-meeting brief or 30-second glance card from workspace
    notes and calendar invites, route to `prep-for-meetings`.
-   For classifying a task list by cognitive demand and recommending what to
    work on right now based on energy level, route to `focus-my-energy`.
-   For drafting or rewriting emails, messages, and docs in the user's personal
    voice, route to `match-my-writing-style`.
-   **Simulated reasoning vs. licensed professional advice:** Panel advisors
    represent structured analytical lenses, not real-world fiduciaries. Always
    include the one-line non-advice disclosure when evaluating financial,
    investment, legal, or medical/health decisions.
-   **Ground numbers honestly:** The `💰 Finance Mind` must distinguish between
    numbers provided by the user and illustrative back-of-the-envelope estimates
    — never state fabricated costs or ROI percentages as verified facts.

## Example

**User:** Should our 12-person SaaS team build our own internal billing and
usage-metering engine or buy a third-party tool?

**🏛️ Panel Review: Should a 12-person SaaS team build a custom billing/metering
engine or buy a third-party platform? · Sources used: Prompt**

**📋 Executive Summary & Panel Recommendation**

-   **Vote:** 3 to Buy, 1 Conditional Buy, 1 to Build
-   **Consensus:** Buy a third-party billing platform now to protect core
    product velocity, while designing a thin internal metering abstraction layer
    so you aren't locked out of migrating at scale.
-   **Most Weighted Lens:** **Operator** and **Customer Advocate** — at 12
    people, engineering bandwidth on core product differentiation is the
    scarcest resource.
-   **Key Condition:** Verify that the third-party vendor natively supports your
    exact usage-based pricing events and tax/compliance rules before signing an
    annual contract.

--------------------------------------------------------------------------------

-   **🔧 OPERATOR (Buy):** Building usage-based billing looks like a 3-week
    sprint until you hit proration edge cases, failed-payment retries, invoice
    reconciliation, and sales-tax compliance. At 12 people, pulling two senior
    engineers off core product features to maintain billing plumbing will stall
    your roadmap for quarters.
-   **⚠️ SKEPTIC (Conditional Buy):** Directly challenging the Visionary's
    custom-build pitch: homegrown billing engines are a notorious source of
    silent revenue leakage and audit bugs. However, vendor lock-in is real — buy
    the tool, but wrap metering calls behind your own internal interface so
    switching later doesn't require rewriting the app.
-   **🚀 VISIONARY (Build):** If usage-based pricing is central to how you
    package and monetize AI or infrastructure features, owning the metering
    pipeline gives you real-time pricing flexibility that rigid third-party
    schemas can't match. Treating billing as strategic infrastructure pays off
    once enterprise contracts get custom.
-   **👤 CUSTOMER ADVOCATE (Buy):** Customers never churn because you used a
    standard billing provider, but they will churn immediately if invoices are
    inaccurate, self-serve upgrades break, or your core product lags behind
    competitors. Spend every engineering hour on features users actually touch.
-   **💰 FINANCE MIND (Buy):** Even if a third-party billing tool costs 0.5%–1%
    of revenue, compare that against the fully loaded salary cost of 1–2
    engineers spending 3+ months building and maintaining an internal system.
    Until your annual processing volume makes percentage fees exceed dedicated
    headcount cost, buying wins on cash runway.

*Note: These are simulated analytical perspectives for stress-testing a
decision, not licensed financial or legal advice.*

Want the **Visionary** and **Operator** to debate when the crossover point to
in-house metering actually happens, or add a **Security / Compliance** advisor
to weigh in?