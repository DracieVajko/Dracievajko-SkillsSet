---
name: generate-fresh-ideas
description: |-
  Use when the user wants fresh content ideas, creative concepts, or new angles by remixing or repurposing articles, posts, briefs, transcripts, notes, or Google Docs. Generates 5 distinct angles (Contrarian, Personal Story, Data/Evidence, Playbook, What They Missed) rather than summarizing or rephrasing. Do NOT trigger for plain summaries, drafting in the user's voice (use match-my-writing-style), decision panels (use get-more-perspectives), or meeting briefs (use prep-for-meetings).
version: 1.0.0
author: DracieVajko
tags: [content, ideas, creativity, remix, workspace]
category: thinking-frameworks
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/generate-fresh-ideas/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Generate Fresh Ideas

Turn any piece of source material into 5 distinct derivative content concepts
using five structured creative lenses — not summaries or rewrites, but genuinely
new angles on the core topic.

## Core Principles & Applicability

-   **Deliver all 5 remixes on Turn 1 — never gate brainstorming behind intake
    questions:** When the user provides or references an article, post, product
    brief, quote, transcript, note, or **Google Doc**, generate the 5 creative
    angles immediately on Turn 1. Never withhold remixes to ask upfront
    clarifying questions about target platform, audience, or tone, because
    preliminary questionnaires stall creative momentum.
-   **Generate derivative angles, never summaries or paraphrases:** Each remix
    must stand on its own as a fresh concept spun off the source material rather
    than a restatement of what the original already said. If two lenses converge
    on a similar point, sharpen the distinction or pivot one to a different
    facet of the source.
-   **One default structure, two clearly scoped escape hatches:**
    -   **Default:** Present 5 distinct remixes across the 5 creative lenses
        (`🔥 Contrarian Take`, `📖 Personal Story Hook`,
        `📊 Data / Evidence Angle`, `✅ Practical Playbook`, and
        `🎯 What They Missed`), each with a punchy one-line pitch and a 2–3
        sentence expansion.
    -   **Escape hatch 1 (Thin source material):** If the source is a brief
        quote, single tweet, or one-liner where a lens genuinely does not apply
        (for example, the quote is already a nuanced contrarian take), skip that
        lens and state why in one sentence rather than padding with filler.
    -   **Escape hatch 2 (Immediate draft expansion):** When the user selects
        one of the 5 angles and asks to develop it into a full post, article,
        thread, or memo (or asks on Turn 1 to both remix and draft a winner),
        write the full piece immediately without re-pitching the menu.
-   **Ground the Data / Evidence lens without fabricating statistics:** Quote
    exact numbers from the user's source material when present, or cite verified
    figures only when retrieved via **Google Search** in the same turn. When
    suggesting external proof points or benchmarks that have not been verified
    in the turn, frame them explicitly as evidence to gather or use bracketed
    placeholders (e.g., `[insert team cycle-time metric]` or
    `"Look up industry benchmark on X"`) — never invent statistics, study
    citations, or customer case studies.
-   **Unconnected or declined apps — never loop:** When the user references a
    **Google Doc**, **Gmail** newsletter/thread, or web URL, check the relevant
    connected tool on Turn 1. If a Workspace app is unconnected, returns empty,
    or is declined once, do NOT re-call the tool or re-ask the user to connect
    apps on subsequent turns — ask the user to paste the text or excerpt
    directly. List connected sources read in the header (`Sources used: ...`)
    without recurring `Couldn't check:` footers.
-   **Cold-start fallback:** If the user invokes the skill with a bare starter
    prompt (`"Generate fresh ideas"` or `@generate_fresh_ideas`) and no source
    material or topic exists in the prompt or recent conversation context, ask
    one focused question: `"Paste an article, link, quote, or rough notes (or
    name a Google Doc in your Drive), and I'll spin it into 5 fresh creative
    angles."`
-   **Read-only by default:** Present remixes and follow-up drafts in chat by
    default; create a **Google Doc** only when explicitly requested or confirmed
    by the user.

## Workflow

1.  **Ingest the source material and identify its core thesis:**
    -   Accept pasted text, quotes, transcripts, rough notes, product briefs,
        web URLs, or content retrieved from connected **Google Drive / Google
        Docs** or **Gmail**.
    -   Distill the source's central claim, underlying assumptions, and unspoken
        gaps so each lens pushes beyond the original framing.
2.  **Apply the 5 remix lenses:**
    -   **1. 🔥 Contrarian Take:** Identify the strongest defensible
        counter-argument or overlooked trade-off. Where is the original premise
        incomplete, over-generalized, or missing nuance? Frame as:
        `"Everyone is saying X, but here's why Y is the real driver."` Keep the
        take genuinely defensible rather than contrarian just for clicks.
    -   **2. 📖 Personal Story Hook:** Connect the core idea to a relatable
        first-person lived experience (`"This happened to me when..."`) that a
        broad range of practitioners could adapt. Frame it as a narrative
        springboard with a clear turning point and lesson rather than an
        abstract essay.
    -   **3. 📊 Data / Evidence Angle:** Lead with empirical proof rather than
        opinion — specify what data, research, benchmark, or case study would
        make the claim undeniable (or pull underutilized numbers from the
        source). If the original source is already data-heavy, flip the lens:
        turn the headline numbers into a human operator or customer story behind
        the metrics.
    -   **4. ✅ Practical Playbook:** Strip out the theory and turn the concept
        into an actionable step-by-step guide or checklist someone can execute
        today (`"How to actually do [X] in [timeframe]"`). Include a concrete
        3–4 step tactical outline; never use vague truisms like
        `"Step 1: Get 10 years of experience."`
    -   **5. 🎯 What They Missed:** Surface the adjacent idea, second-order
        consequence, or edge case the original content didn't explore (`"The
        piece talks about X, but nobody is discussing Y — which matters more
        because..."`).
3.  **Audit for distinctiveness and expand on demand:**
    -   Verify that all 5 angles could be published as separate pieces without
        overlapping.
    -   Offer in one closing line to expand any of the 5 angles into a complete
        draft tailored to their preferred channel (such as a LinkedIn post, blog
        article, social thread, newsletter, or internal memo).

## Output Format

### Mode A: 5-Lens Content Remix (Default)

-   **Header:** `**💡 Remix: [Original Content Title or Core Topic] · Sources
    used: [Prompt / URL / Google Docs / Gmail]**`
-   **Five Lens Blocks (skip a lens with a 1-line note only if the source is too
    thin to support it):**
    -   `**1. 🔥 CONTRARIAN TAKE: [Punchy one-line pitch / headline]**`
        -   `→ **Angle:** [2–3 sentences explaining the counter-argument, why it
            holds up, and the tension it creates.]`
    -   `**2. 📖 PERSONAL STORY HOOK: [Punchy one-line pitch / headline]**`
        -   `→ **Angle:** [2–3 sentences + suggested 3-beat story structure:
            Setup → Friction moment → Lesson.]`
    -   `**3. 📊 DATA / EVIDENCE ANGLE: [Punchy one-line pitch / headline]**`
        -   `→ **Angle:** [2–3 sentences + exact metrics from the source or
            specific evidence/benchmarks to pull (using [placeholders] for
            unverified figures).]`
    -   `**4. ✅ PRACTICAL PLAYBOOK: [Punchy one-line pitch / headline]**`
        -   `→ **Angle:** [1–2 sentence setup + 3–4 tactical steps the reader
            can execute today.]`
    -   `**5. 🎯 WHAT THEY MISSED: [Punchy one-line pitch / headline]**`
        -   `→ **Angle:** [2–3 sentences unpacking the second-order consequence
            or adjacent blind spot.]`
-   **Optional closing line (one line max):** Ask which angle (`1–5`) they want
    developed into a full draft and for which channel.

### Mode B: Follow-Up Draft Expansion

When the user picks one of the 5 remixes to flesh out:

-   Deliver the complete, copy-ready draft in chat immediately, structured for
    their target channel (or a clean article/post layout if no channel was
    specified).
-   Offer in one closing line to adjust the angle or save the draft to **Google
    Docs** upon confirmation.

## Tool Usage Guide

Tool                         | When                                                                                                                   | What to extract
:--------------------------- | :--------------------------------------------------------------------------------------------------------------------- | :--------------
Google Drive / Google Docs   | First turn if connected and user names a doc or notes to remix (never loop if declined); write only after confirmation | Read source notes, transcripts, or drafts to remix. Create a new Google Doc for a selected draft only after explicit user request or confirmation.
Gmail                        | First turn if connected and user references an email or newsletter to remix (never loop if declined)                   | Read the referenced email thread or newsletter body as source material. Never send or draft emails unless requested.
Google Search / Web Browsing | When the user shares a web URL to remix or asks to look up real benchmarks for the Data / Evidence lens                | Retrieve the article content from the user-provided URL or verify public studies/statistics. Clearly label any unsearched figures as evidence to gather.

## Scope Boundaries & Gotchas

-   For drafting, replying to, or rewriting a specific email, message, post, or
    document in the user's personal voice and channel register, route to
    `match-my-writing-style` (or pair with it once the user picks one of the 5
    angles to draft).
-   For evaluating a strategic decision or dilemma across multiple simulated
    expert advisors (`Operator`, `Skeptic`, `Visionary`, `Customer`, `Finance`),
    route to `get-more-perspectives`.
-   For building a pre-meeting brief or 30-second glance card from workspace
    notes and calendar invites, route to `prep-for-meetings`.
-   For classifying a task list by cognitive demand and recommending what to
    work on right now based on energy level, route to `focus-my-energy`.
-   **Plain summarization vs. creative remixing:** If the user only asks to
    summarize, condense, or translate an article
    (`"Give me a TL;DR of this doc"`), provide a direct summary rather than
    forcing the 5 creative remix lenses.
-   **Evidence pointers vs. verified stats:** Never present illustrative numbers
    in the `📊 Data / Evidence Angle` as verified facts unless they came directly
    from the user's source text or a same-turn search result. Always distinguish
    `"evidence to gather"` or `[bracketed placeholders]` from verified source
    metrics.
-   **Defensible contrarianism:** The `🔥 Contrarian Take` is meant to surface a
    genuine blind spot or trade-off in the source's thesis — never generate
    inflammatory, unsafe, or factually false claims just to be contrarian.

## Example

**User:** Remix this article arguing that remote work is causing engineer
burnout because distributed teams miss out on in-person office camaraderie.

**💡 Remix: Remote Work & Engineer Burnout · Sources used: Prompt**

**1. 🔥 CONTRARIAN TAKE: Remote work isn't burning engineers out — synchronous
surveillance in a distributed wrapper is.**

→ **Angle:** Everyone blames isolation for remote burnout, but the real culprit
is copying broken office habits onto video calls and chat apps. When companies
replace hallway trust with green-dot status anxiety and 7 hours of daily video
check-ins, engineers get all the interruptions of an open office with none of
the deep-focus upside of working from home.

**2. 📖 PERSONAL STORY HOOK: The week I deleted 6 recurring "alignment" syncs and
watched my team ship twice as fast.**

→ **Angle:** Anchor this in a first-person turning point where trying to fix
team fatigue with virtual happy hours flopped, and the breakthrough came from
protecting uninterrupted maker time instead. **Story structure:** (1) Setup: An
exhausted remote team drowning in daily status calls → (2) Friction: Realizing
morale boosters were just adding more screen time → (3) Lesson: Replacing status
meetings with a single async Friday demo restored energy and camaraderie.

**3. 📊 DATA / EVIDENCE ANGLE: The hidden cost of context-switching: Comparing
calendar fragmentation vs. office attendance.**

→ **Angle:** Shift the debate from subjective feelings about office culture to
measurable calendar metrics. Pull internal or industry benchmarks comparing
**[average uninterrupted 2+ hour focus blocks per week]** and **[after-hours
message volume]** against self-reported burnout scores — showing that calendar
fragmentation predicts exhaustion far better than physical location.

**4. ✅ PRACTICAL PLAYBOOK: The 15-Minute Remote Energy Audit for Engineering
Leads.**

→ **Angle:** A tactical checklist a manager or tech lead can run this afternoon
to cut remote drag without waiting for an org-wide policy change:

1.  **Audit the calendar:** Cancel or convert to async any recurring status
    meeting where >50% of attendees only listen.
2.  **Core-hours window:** Define a 3-hour synchronous collaboration window and
    protect the rest of the day for heads-down work.
3.  **Kill the "quick ping":** Replace bare `"Hey"` chat messages with
    one-message context + urgency (`"Non-urgent — for tomorrow: ..."`).
4.  **Ship-show-ask:** Move routine code and doc updates to async written briefs
    with a 24-hour response norm.

**5. 🎯 WHAT THEY MISSED: Unstructured hybrid is more exhausting than either full
remote or full in-office.**

→ **Angle:** The article frames burnout as a binary between remote and in-office
work, missing the second-order reality most teams actually live in: commuting
into an office only to sit on video calls all day because half the team is still
distributed. Uncoordinated hybrid combines commute fatigue with virtual meeting
overload.

Want me to turn one of these (`1–5`) into a full LinkedIn post, blog article, or
internal memo?