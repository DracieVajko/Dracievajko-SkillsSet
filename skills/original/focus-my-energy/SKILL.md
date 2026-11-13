---
name: focus-my-energy
description: |-
  Use when the user asks what to work on next, wants to prioritize or sequence tasks by energy or mental bandwidth, feels tired, fried, or overwhelmed, or wants to set up an energy profile. Classifies tasks from their prompt or connected Workspace apps by cognitive demand and recommends one clear action matched to their state. Do NOT trigger for calendar booking, medical advice, meeting briefs (use prep-for-meetings), decision panels (use get-more-perspectives), or drafting (use match-my-writing-style).
version: 1.0.0
author: DracieVajko
tags: [energy, tasks, productivity, triage, workspace]
category: productivity
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/focus-my-energy/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Focus My Energy

Match the user's workload to their current mental bandwidth by classifying tasks
by cognitive demand (`Deep Work`, `Steady Work`, `Low Drain`) and recommending
one clear action to tackle right now.

## Core Principles & Applicability

-   **Deliver a concrete recommendation on Turn 1 — never gate prioritization
    behind an intake questionnaire:** When the user shares tasks or asks what to
    work on next, classify their tasks and deliver the `DO NOW` recommendation
    immediately on Turn 1. Never withhold a recommendation to ask an Energy
    Profile setup survey or a standalone
    `"How are you feeling — sharp, steady, or fried?"` check-in when tasks are
    available, because adding upfront questionnaires increases cognitive load
    when the user is already tired or overwhelmed.
-   **Three-tier energy precedence (Self-Report > Energy Profile > Context
    Heuristics):**
    1.  **Real-time self-report always wins:** If the user states or implies how
        they feel (`"sharp"`, `"steady"`, `"fried"`, `"brain dead"`,
        `"just got out of 3 hours of meetings"`), use that state immediately —
        even if it contradicts their saved Energy Profile.
    2.  **Saved Energy Profile fills the gaps:** If the user hasn't stated their
        current energy and an Energy Profile exists in conversation history or
        **Google Drive**, infer their state from the current time and day of
        week against their peak hours, dip window, and energy drains, showing
        your reasoning in one line (`"It's 2:15 PM, which falls in your
        2:00–3:30 PM dip window, so I'm matching for steady-to-low energy — tell
        me if that's off"`).
    3.  **Calendar and time-of-day heuristics as fallback:** If neither
        self-report nor an Energy Profile is available, infer from recent
        **Google Calendar** load (e.g., back-to-back meetings → drained; open
        morning → sharp) and time-of-day / day-of-week defaults (morning →
        `Sharp`, post-lunch 1:30–3:30 PM → `Steady / Dip`, late Friday afternoon
        → `Low Drain`), stating the assumption so the user can easily pivot.
-   **One default recommendation, one hard-deadline escape hatch:**
    -   **Default:** Recommend **one** specific task under `DO NOW` matched to
        the user's current energy tier (plus one optional `<5–10 min` item under
        `QUICK WIN` for easy momentum), and park higher-drain tasks under
        `SAVE FOR LATER`, because a multi-option menu creates decision fatigue.
    -   **Escape hatch (Hard deadline today):** If a `🔴 Deep Work` or
        `🟡 Steady Work` task is due today (or before the user's next peak
        window), surface it in `DO NOW` regardless of low energy, state the
        override plainly (`"Normally I'd save this for your peak window, but
        since it's due today, let's make it manageable"`), and break out a 10–15
        minute low-friction starter step so they can begin without feeling
        overwhelmed.
-   **Unconnected or declined apps — never loop:** Check connected **Google
    Tasks** (for open tasks and due dates), **Google Calendar** (for today's
    meeting load, time zone, and free windows), and **Google Drive** (for an
    existing `"Energy Profile"` doc) on Turn 1 when needed. If any app is
    unconnected, empty, or declined once, do NOT re-call the tool or re-ask the
    user to connect apps on subsequent turns — work directly from the tasks in
    the user's prompt or conversation history. List connected sources read in
    the header (`Sources used: ...`) without recurring `Couldn't check:`
    footers.
-   **Cold-start fallback — never invent tasks:** If the user invokes the skill
    with no tasks in their prompt, recent chat context, or connected **Google
    Tasks**, do not fabricate sample work. State any inferred energy baseline in
    one line and ask one focused question: `"Drop 2–3 things on your plate (and
    whether you're feeling sharp, steady, or fried), and I'll pick the best one
    to start with."` If they invoked the skill to configure their rhythms
    (`"Set up my energy profile"`), use **Mode B** below.
-   **Read-only by default:** Do not create **Google Calendar** events or mutate
    **Google Tasks** on Turn 1 unless explicitly confirmed by the user, and keep
    Energy Profile updates in the conversation rather than offering to create or
    update a **Google Doc**. Support low-energy choices without guilt-tripping
    (`"Good call — knock out the easy admin now and protect tomorrow's peak
    window for deep work"`).

## Workflow

1.  **Gather the task list and check connected Workspace context:**
    -   Use tasks provided in the user's message or earlier conversation turns
        first.
    -   If the user asks what to work on without listing tasks, check connected
        **Google Tasks** for open items and due dates, and check **Google
        Calendar** for today's schedule, time zone, and recent meeting blocks.
    -   Check conversation history or connected **Google Drive** (search for
        `"Energy Profile"`) for a saved Energy Profile.
2.  **Assess current energy state (`Sharp`, `Steady`, or `Fried`):**
    -   Apply the three-tier precedence: (1) explicit or implied self-report in
        the user's prompt, (2) saved Energy Profile matched against current
        local time and day of week, or (3) recent **Google Calendar** meeting
        density and time-of-day heuristics.
3.  **Classify tasks by cognitive demand:**
    -   **🔴 Deep Work:** Creative thinking, strategy, writing from scratch,
        system architecture, complex problem-solving, or high-stakes decisions.
        Requires peak mental energy (`Sharp`).
    -   **🟡 Steady Work:** Focused execution without heavy invention — code or
        document reviews, editing, substantive email replies, project planning,
        or structured analysis. Fits moderate energy (`Steady`).
    -   **🟢 Low Drain:** Routine, administrative, or mechanical tasks —
        scheduling, filing, expense reports, quick status replies, inbox
        cleanup, or organizing notes. Ideal when depleted (`Fried`).
4.  **Select the `DO NOW` match and sequence the rest:**
    -   Pick the single best-fitting task for `DO NOW`:
        -   When **Sharp**: Pick the highest-leverage `🔴 Deep Work` task so peak
            bandwidth isn't wasted on routine admin.
        -   When **Steady**: Pick a `🟡 Steady Work` task (or a well-scoped chunk
            of deep work), plus an optional `🟢 Low Drain` quick win.
        -   When **Fried**: Pick a `🟢 Low Drain` task or `<5–10 min` quick win,
            and explicitly protect `🔴 Deep Work` for their next peak window.
    -   **Hard-deadline check:** If a high-demand task is due today, promote it
        to `DO NOW` and decompose it into a concrete 10–15 minute starter action
        (e.g., outlining 3 bullet points or drafting only the rough intro).
5.  **Surface pattern refinements and Energy Profile updates non-blockingly:**
    -   On first use (when no Energy Profile exists), add a one-line optional
        invite at the bottom of the response offering to save their peak hours
        and dip window as an Energy Profile.
    -   Across repeated turns, when observed energy patterns diverge from their
        saved profile (e.g., consistently sharp during a stated dip window, or
        repeatedly fried after back-to-back meetings), note the pattern in one
        concise bullet and ask if they want to update their profile.

## Output Format

### Mode A: Energy-Matched Task Recommendation (Default)

-   **Header:** `**⚡ Energy Match: [Sharp / Steady / Fried] ([stated by you /
    from your Energy Profile / inferred from time & schedule]) · Sources used:
    [Prompt / Google Tasks, Google Calendar]**`
-   **DO NOW (single primary recommendation):**
    -   `**[Task Name]** ([🔴 Deep Work / 🟡 Steady Work / 🟢 Low Drain] · [due
        date or est. effort if known])` — 1–2 sentences explaining why this task
        matches their current bandwidth (or, if overriding for a today deadline,
        the 10–15 minute low-friction first step).
-   **QUICK WIN (include when helpful for easy momentum):**
    -   `**[Task Name]** (🟢 Low Drain · ~5–10 min)` — 1 line on how to knock it
        out quickly.
-   **SAVE FOR LATER (remaining tasks grouped by cognitive tier):**
    -   `- [🔴/🟡/🟢 Tier] **[Task Name]**: [Why to defer + target window, e.g.,
        "Save for tomorrow's 9:00–11:00 AM peak window"]`
-   **Optional closing line (one line max):** Offer to flip the recommendation
    if their energy differs from the inference
    (`"Actually feeling sharp or fried? Tell me and I'll flip the order"`) or
    invite them to set up/update their Energy Profile.

### Mode B: Standalone Energy Profile Setup / Review

When the user asks to set up, view, or update their Energy Profile without a
specific task list to prioritize:

-   **Header:** `**🔋 Your Energy Profile · Baseline rhythms**`
-   **Profile Fields (clean Markdown bullets — fill in any details already
    shared and mark remaining fields as optional):**
    -   **Peak Hours:** [When you're sharpest, e.g., `9:00–11:30 AM` or
        `After 8:00 PM`]
    -   **Dip Window:** [When you reliably crash, e.g., `2:00–3:30 PM` or
        `Post-lunch`]
    -   **Second Wind:** [Late-day surge window, or `None`]
    -   **Energy Drains:** [Triggers that deplete bandwidth, e.g.,
        `Back-to-back meetings`, `Context-switching`]
    -   **Energy Boosts:** [Quick resets that recharge you, e.g., `10-min walk`,
        `Music`, `Coffee`]
    -   **Weekly Pattern:** [Day-of-week rhythms, e.g., `Slow Monday start`,
        `Low-drain Friday afternoons`]
    -   **Chronotype:** [`Morning lark`, `Night owl`, or `In-between`]
-   **Closing line:** Invite them to share as much or as little as they want (or
    drop their current task list to match immediately) so you can apply their
    profile in the conversation.

## Tool Usage Guide

Tool                       | When                                                                                             | What to extract
:------------------------- | :----------------------------------------------------------------------------------------------- | :--------------
Google Tasks               | First turn if connected and user has not pasted a task list (never loop if declined)             | Open tasks, task notes, and due dates from the user's task lists. Do not create or complete tasks without confirmation.
Google Calendar            | First turn if connected (never loop if declined)                                                 | Today's events, user's local time zone, recent back-to-back meeting blocks (to infer energy drain), and remaining free windows today. Do not book calendar events on Turn 1.
Google Drive / Google Docs | First turn if connected to check for an existing `"Energy Profile"` doc (never loop if declined) | Read an existing `"Energy Profile"` doc for baseline peak/dip windows (read-only; keep profile updates in the conversation rather than offering to create or edit a Google Doc).

## Scope Boundaries & Gotchas

-   For estimating task durations across a week, checking capacity shortfalls,
    and booking focus blocks on **Google Calendar**, route to calendar
    scheduling (`focus-block-scheduler` when available).
-   For building a pre-meeting brief or 30-second glance card for an upcoming
    meeting, route to `prep-for-meetings`.
-   For evaluating a strategic decision across multiple simulated expert
    viewpoints, route to `get-more-perspectives`.
-   For drafting or rewriting emails, messages, and docs in the user's personal
    voice, route to `match-my-writing-style`.
-   For remixing source material into 5 new creative content angles, route to
    `generate-fresh-ideas`.
-   **Vague task descriptions:** If a task on the user's list is too vague to
    classify confidently (e.g., `"Work on Q4 project"`), assign a provisional
    tier based on context (`🔴 Deep Work` if strategic/drafting, `🟡 Steady Work`
    if review/update) and note in one line how to split it if it's actually
    quick admin.
-   **Profile drift vs. real-time override:** Treat a saved Energy Profile as a
    helpful default, never a rigid rule. Always honor the user's real-time
    energy first, and prompt to update the profile only when it misses
    repeatedly.
-   **Non-clinical scope:** Keep guidance focused on task selection and
    cognitive load. If the user describes clinical fatigue, insomnia, or medical
    symptoms, respond supportively and encourage consulting a healthcare
    professional rather than framing medical symptoms as a productivity problem.

## Example

**User:** I just got out of 3 hours of back-to-back roadmap meetings and my
brain is cooked. On my list: write the Q4 architecture RFC, review Alex's PR,
submit my travel expenses, and reply to the venue coordinator about Friday's
lunch headcount. What should I do right now?

**⚡ Energy Match: Fried (stated by you after 3 hours of back-to-back meetings) ·
Sources used: Prompt**

**DO NOW:**

-   **Reply to the venue coordinator with Friday's lunch headcount** (🟢 Low
    Drain · ~5 min) — Zero creative lift required. Sending a two-sentence
    headcount confirmation clears an open loop immediately and gives you an easy
    win without taxing your depleted focus.

**QUICK WIN (if you want one more easy check-off):**

-   **Submit travel expenses** (🟢 Low Drain · ~10–15 min) — Purely mechanical
    receipt matching you can do on autopilot before wrapping up or taking a
    break.

**SAVE FOR LATER:**

-   🔴 **Write the Q4 architecture RFC**: Needs peak strategic thinking and
    blank-page writing — protect tomorrow morning's peak window for this when
    your head is clear.
-   🟡 **Review Alex's PR**: Needs steady attention to catch logic bugs — save
    for after a break or your mid-day steady window tomorrow.

Want me to draft that quick headcount reply for you now, or save "back-to-back
meetings" as an energy drain in a personal Energy Profile?