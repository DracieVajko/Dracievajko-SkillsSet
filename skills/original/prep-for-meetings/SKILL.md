---
name: prep-for-meetings
description: |-
  Use when the user asks to prep for an upcoming meeting, call, or 1:1, or wants to know what they owe or need to know before walking in. Scans connected Calendar, Gmail, Docs, and Tasks for mentions of the user to build a 30-second glance card and TL;DR brief (Must Do, Must Know, Watch Out). Do NOT trigger when an active plugin meeting skill is available in the turn (use plugin:prepare-for-meetings, plugin:meeting-context-builder, or plugin:meeting-prep instead), or for booking calendar events, energy-based task triage (use focus-my-energy), voice-matched drafting (use match-my-writing-style), or decision panels (use get-more-perspectives).
version: 1.0.0
author: DracieVajko
tags: [meetings, prep, workspace, calendar]
category: productivity
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/prep-for-meetings/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Prep for Meetings

Deliver a tight, user-centric pre-meeting brief — combining a **30-Second Glance
Card** and a **TL;DR Brief** (`Must Do`, `Must Know`, `Watch Out`) — by scanning
connected Workspace sources for what the user owes, what changed since last
time, and what could catch them off guard.

## Core Principles & Applicability

-   **Deliver the brief on Turn 1 — starter prompts invoke live data
    immediately:** When the user invokes `"Prep for meetings"`,
    `"Prep me for my next meeting"`, `@prep_for_meetings`, or names a specific
    session (`"Prep me for my 2pm"` or `"Prep me for my 1:1 with Sarah"`),
    immediately query connected **Google Calendar**, **Gmail**, **Google Drive /
    Google Docs**, and **Google Tasks** on Turn 1. Never reply with generic
    meeting-prep tips or block on upfront clarifying questions when calendar,
    email, or document context is available.
-   **One default two-part structure, one imminent-meeting escape hatch:**
    -   **Default:** Produce a **30-Second Glance Card** (`Context`,
        `Your Goal & Move`, `Danger Zones`) followed by a **TL;DR Brief**
        (`🔴 Must Do Before`, `🧠 Must Know`, `⚠️ Watch Out`), plus an optional
        **What Matters to You** filter when a multi-topic agenda has items that
        do not involve the user. Keep the entire brief scannable in under 90
        seconds; if a section has nothing to flag, write
        `None found — you're clear` rather than padding.
    -   **Escape hatch (Meeting starting in <30 minutes or user is walking
        in):** Lead with the **30-Second Glance Card** and scope
        `🔴 Must Do Before` strictly to the 1–2 numbers, updates, or decisions
        the user must have ready to say out loud in the room (skipping
        multi-hour prep tasks they no longer have time to complete).
-   **Thread recency ("latest reply wins"), strict date anchoring, and true
    ownership:**
    -   **Latest reply wins:** Read full **Gmail** threads (`get_thread`) and
        recent meeting notes newest-first so a blocker or question resolved in a
        later reply is reported under `🧠 Must Know` (settled context), never
        flagged as an open `🔴 Must Do Before` or `⚠️ Watch Out`.
    -   **Strict date anchoring:** Cite the source and date for every surfaced
        fact or commitment. Preserve explicit dates verbatim (`"October 9"`
        stays `Oct 9`) and resolve relative dates (`"by Friday"`, `"tomorrow"`)
        strictly from the source message or note timestamp
        (`source_date + offset`).
    -   **True ownership:** Being `@mentioned` or CC'd in a doc or email thread
        does not automatically mean the user owns the task — verify that the
        user agreed to or was assigned the deliverable before placing it under
        `🔴 Must Do Before`.
-   **Unconnected or declined apps — never loop:** Check connected **Google
    Calendar**, **Gmail**, **Google Drive / Google Docs**, and **Google Tasks**
    on Turn 1. If any app is unconnected, returns empty, or is declined once, do
    NOT re-call the tool or re-ask the user to connect apps on subsequent turns
    — build the brief directly from any notes, agenda, or emails the user
    pasted, or ask one focused question (`"Which meeting are you prepping for,
    and what did you commit to or leave open last time?"`). List connected
    sources read in the header (`Sources used: ...`) without recurring
    `Couldn't check:` footers.
-   **Read-only by default & zero generic dossiers:** Never modify calendar
    events, mutate tasks, or send emails unless explicitly requested and
    confirmed. Do not write career bios of recurring teammates — focus on what
    attendees need from the user in this session.

## Workflow

1.  **Identify the target meeting and check connected Workspace sources:**
    -   Locate the requested meeting in **Google Calendar** (for
        `"my next meeting"` or a bare starter prompt, select the next upcoming
        event with ≥1 other attendee). Extract the title, start time, time zone,
        attendee list, description, and any linked agenda docs.
    -   If multiple upcoming events plausibly match (e.g., two meetings with
        different people named Sarah), either provide a compact brief for each
        or list the matching titles/times and ask which one they want.
    -   **Fallback (if Calendar/Gmail/Drive are unconnected or declined):** Skip
        tool retries and build the brief from user-provided context, or ask one
        question to identify the meeting and open items.
2.  **Scan for mentions of the user, commitments, and latest thread state:**
    -   **Google Drive / Google Docs:** Read attached agenda docs and search
        recent shared meeting notes for the meeting topic, attendee names, and
        mentions of the user's name (`"[User] will..."`,
        `"Assigned to [User]"`).
    -   **Gmail:** Search recent threads involving the attendees or meeting
        topic and read full threads (`get_thread`) newest-first to capture
        latest numbers, unanswered questions directed at the user, and promises
        made.
    -   **Google Tasks:** Check open or overdue tasks tied to the meeting topic
        or attendees.
3.  **Synthesize the three core prep dimensions:**
    -   **🔴 Must Do Before (What the user owes):** Incomplete action items,
        documents to review, or metrics/updates the user promised to bring.
    -   **🧠 Must Know (Context & settled updates):** Key facts, revised numbers,
        or decisions settled since the last sync that shape how the user should
        show up.
    -   **⚠️ Watch Out (Danger zones):** Overdue deliverables, repeated nudges
        waiting on the user, conflicting timelines/numbers across emails and
        docs, or sensitive stakeholder dynamics (2–3 bullets max).
4.  **Format and deliver the brief:**
    -   Present the **30-Second Glance Card** and **TL;DR Brief** using the
        structure below. If the meeting has a long agenda where only a subset
        impacts the user, include **What Matters to You** filtered strictly to
        the 2–3 items that affect the user's work.

## Output Format

-   **Header:** `**📋 [Meeting Title] · [Day, Date, Time, Time Zone] · [Attendees
    (first names or roles)] · Sources used: [Google Calendar, Gmail, Google
    Docs, Google Tasks]**`

**30-Second Glance Card**

-   **🎯 Context & Goal:** [One sentence on where things stand and what needs to
    be decided or aligned on in this session, with source/date.]
-   **⚡ Your Move:** [The single most important update, decision, or question
    the user needs to drive.]
-   **⚠️ Top Watch-Out:** [One sentence on the main blind spot, overdue ask, or
    trap to avoid, with source/date.]

**TL;DR Brief**

-   **🔴 Must Do Before:**
    -   `[ ] [Specific action item or number to have ready — cite source &
        date]` (or `No open items found — you're clear.`)
-   **🧠 Must Know:**
    -   `[Key fact, revised metric, or settled decision since last meeting —
        cite source & date]`
-   **⚠️ Watch Out:**
    -   `[Hard question, conflicting date/number, or unanswered nudge — cite
        source & date]` (or `Nothing flagged.`)

**What Matters to You (include only when filtering a multi-item agenda)**

-   `**[Agenda Item]**: [Why it impacts your work in 1 sentence] · **Your
    position:** [Recommended stance or question to ask]`

-   **Optional closing line (one line max):** Offer to draft a pre-meeting
    update message or pull a deeper history on a specific thread or attendee.

## Tool Usage Guide

Tool                       | When                                             | What to extract
:------------------------- | :----------------------------------------------- | :--------------
Google Calendar            | First turn if connected (never loop if declined) | Target event title, start/end time, user's time zone, attendee list and RSVP status, invite description, and attached doc links. Never modify events on Turn 1.
Gmail                      | First turn if connected (never loop if declined) | Recent threads with attendees or on the meeting topic (`get_thread`, read newest-first); unanswered questions directed at the user, revised figures, and promised deliverables.
Google Drive / Google Docs | First turn if connected (never loop if declined) | Attached agenda docs and prior meeting notes mentioning the user's name, action items, or open comments/questions.
Google Tasks               | First turn if connected (never loop if declined) | Open or overdue tasks matching the meeting topic, project, or attendees.

## Scope Boundaries & Gotchas

-   When a plugin is invoked in the turn (such as `@Productivity suite` or
    `@Business`), defer to that plugin's meeting skill
    (`plugin:prepare-for-meetings`, `plugin:meeting-context-builder`, or
    `plugin:meeting-prep`) so the plugin's connected 3P apps and vertical
    workflow are used.
-   For classifying a task list by cognitive demand and deciding what to work on
    right now based on mental bandwidth, route to `focus-my-energy`.
-   For drafting or rewriting emails, messages, and docs in the user's personal
    voice, route to `match-my-writing-style`.
-   For stress-testing a strategic decision across multiple simulated expert
    advisors (`Operator`, `Skeptic`, `Visionary`, `Customer`, `Finance`), route
    to `get-more-perspectives`.
-   For remixing an article, transcript, or notes into 5 new creative content
    angles, route to `generate-fresh-ideas`.
-   **Mentions vs. ownership:** Verify whether the user actually committed to or
    was assigned an action item before listing it in `🔴 Must Do Before` — do not
    treat passive `@mentions` or CC'd threads as user obligations.
-   **Stale thread state:** Always check the newest message in a thread so an
    issue resolved yesterday is summarized under `🧠 Must Know` rather than
    flagged as an active `⚠️ Watch Out`.
-   **Never fabricate prior commitments:** If Workspace sources are unconnected
    or contain no prior notes for the meeting, state that no prior notes were
    found rather than inventing action items or attendee positions.

## Example

**User:** Prep me for my 2pm Q4 launch sync.

**📋 Q4 Launch Sync · Wed, Oct 7, 2:00 PM PT · Maya, Sam, +2 · Sources used:
Google Calendar, Gmail, Google Docs, Google Tasks**

**30-Second Glance Card**

-   **🎯 Context & Goal:** Weekly checkpoint ahead of the Oct 19 launch; staging
    cutover slipped two days, so today's goal is locking the revised QA sign-off
    schedule (Gmail thread, Oct 5).
-   **⚡ Your Move:** Confirm whether Legal signed off on the updated terms
    banner and share the final support staffing numbers you committed to last
    week.
-   **⚠️ Top Watch-Out:** Sam pinged you twice in the launch checklist doc
    asking if the terms banner is approved — walking in without that answer will
    block QA sign-off (Google Doc comment, Oct 5).

**TL;DR Brief**

-   **🔴 Must Do Before:**
    -   `[ ]` Confirm Legal's sign-off status on the terms banner (Sam's comment
        in *Q4 Launch Checklist*, Oct 5).
    -   `[ ]` Bring the updated Tier-1 support staffing table you promised at
        last Wednesday's sync (*Q4 Launch Notes*, Sep 30; overdue in Google
        Tasks).
-   **🧠 Must Know:**
    -   Engineering pushed staging cutover from Oct 5 to Oct 7 due to API rate
        limits, which Maya confirmed is now resolved in staging (Gmail thread,
        Oct 6).
    -   The security review blocker flagged last week was cleared on Monday — no
        need to reopen it (Gmail thread, Oct 5).
-   **⚠️ Watch Out:**
    -   Marketing's announcement email is still locked for Oct 19 — any further
        QA slip today puts that send date at risk (*Q4 Launch Checklist*, Oct
        4).

Want me to draft a quick reply to Sam's doc comment before you head in, or pull
up the support staffing numbers from your recent threads?