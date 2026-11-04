---
name: match-my-writing-style
description: |-
  Use when the user asks to draft, reply to, or rewrite emails, messages, posts, memos, or docs in their voice, or to build or update their writing style profile. Infers tone, greetings, sign-offs, and channel registers from sent Gmail and Google Docs so drafts sound like them rather than generic AI prose, even without a style prompt. Do NOT trigger for factual Q&A, code, translation, other personas, content remixes (use generate-fresh-ideas), or meeting briefs (use prep-for-meetings).
version: 1.0.0
author: DracieVajko
tags: [writing, voice, email, style, workspace]
category: writing-docs
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/match-my-writing-style/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Match My Writing Style

Write, reply to, and rewrite emails, messages, posts, memos, and documents in
the user's authentic voice by learning their real phrasing and channel registers
from Workspace writing samples.

## Core Principles & Applicability

-   **Deliver the requested draft on Turn 1 — never gate writing behind an
    onboarding survey:** When the user asks to write, reply to, or rewrite
    something, always fulfill the writing request immediately in the first turn.
    If no Voice Card exists yet, scan connected Workspace sources, infer the
    user's voice silently, deliver the completed draft first, and include a
    compact **Voice Card Snapshot** below the draft, because withholding a
    requested draft to ask a multi-question style survey blocks the user's task
    and causes high drop-off on mobile.
-   **Infer from real writing rather than interrogating:** Extract greetings,
    sign-offs, sentence rhythm, contraction habits, punctuation quirks, and
    implicitly avoided buzzwords directly from the user's sent Gmail messages
    and authored Google Docs. Never require the user to fill out a questionnaire
    before drafting.
-   **Unconnected or declined apps — never loop:** Check connected **Google
    Drive** (for an existing Voice Card or user-authored Google Docs) and
    **Gmail** (recent sent messages) on Turn 1. If Gmail or Google Drive is
    unconnected, returns no authored samples, or is declined once, do NOT
    re-call the tool or re-ask the user to connect apps on subsequent turns —
    deliver the requested draft immediately in a natural, direct human voice
    (free of stiff AI clichés) and add a one-line invite to share 2–3 sample
    messages or style tweaks if they want future drafts tuned closer to their
    phrasing.
-   **Cold-start / starter prompts build the Voice Card immediately:** When the
    user invokes the skill with a bare starter prompt
    (`"Match my writing style"`, `"Build my voice card"`, or
    `@match_my_writing_style` with no specific writing task), immediately scan
    connected Gmail sent messages and user-authored Google Docs, present the
    inferred **Voice Card** in chat, and ask what they would like to draft
    first.
-   **Keep drafts clean, copy-ready, and draft-only by default:** Output
    ready-to-send text without inline warning tags or meta-commentary inside the
    draft body, because inline flags force the user to manually strip brackets
    before copying. Present drafts in chat by default; create a Gmail draft or
    save a Voice Card Google Doc only when requested or confirmed by the user
    (and never claim a Google Doc was saved unless a Drive/Docs creation tool
    call succeeded). Never send emails or messages directly.
-   **Scope to user-authored communications:** Apply the user's personal voice
    whenever drafting or rewriting text meant to be sent, published, or shared
    as the user (unless they explicitly ask for a different persona, such as
    formal legal boilerplate). Leave objective factual Q&A, code, and data
    tables in standard clear prose so this skill coexists cleanly with other
    active skills.

## Workflow

1.  **Check for an existing Voice Card or scan Workspace writing samples:**
    -   If a Voice Card was already established in the conversation or saved in
        **Google Drive** (search for `"Voice Card"` or `"Writing Style"`), apply
        it directly without re-scanning.
    -   Otherwise, scan connected **Gmail** sent messages
        (`from:me newer_than:90d`, aiming for 15–25 sent messages across varied
        recipients and thread lengths, reading threads newest-first) and
        **Google Drive / Google Docs** authored by the user (`owner:me`) to
        capture how they actually write.
    -   **Fallback (if Gmail and Drive are unconnected, empty, or declined):**
        Skip scanning without prompting to connect apps. Infer any style cues
        available from the user's prompt or pasted text, and use a crisp,
        natural human register (contractions, direct openings, zero AI filler).
2.  **Extract the user's Voice Card attributes:**
    -   **Greetings & openings:** How they start emails and messages (e.g.,
        `"Hey [Name],"`, `"Hi [Name] —"`, or jumping straight to the point; note
        whether they ever use `"I hope this finds you well"`).
    -   **Sign-offs & closings:** Signature sign-offs (`"Best,"`, `"Thanks,"`,
        `"- [Initial]"`, or no sign-off) and how they frame asks or next steps.
    -   **Sentence rhythm & paragraph structure:** Short punchy bursts vs.
        layered sentences, single-sentence paragraphs, bulleted lists, or bold
        lead-ins.
    -   **Vocabulary, contractions & formality:** Contraction frequency
        (`"don't"` vs. `"do not"`), plain vs. technical diction, and transition
        phrases (`"Quick update:"`, `"Here's the thing —"`, `"So basically"`).
    -   **Punctuation, casing & formatting quirks:** Em dashes, parentheticals,
        exclamation marks, Oxford commas, lowercase chat phrasing, or emoji.
    -   **Channel & audience registers:** How their voice shifts across external
        / executive emails, team emails, quick chat messages, and longer
        documents.
    -   **Implicitly avoided language:** Corporate clichés or AI tropes absent
        from their writing (e.g., `"delve"`, `"tapestry"`, `"synergy"`,
        `"thrilled to announce"`), plus any explicit **"Never use"** words the
        user has specified.
3.  **Select the target register and draft immediately:**
    -   Default to matching the register for the target channel and audience
        (e.g., client email, team update, LinkedIn post, doc section). If the
        channel is slightly ambiguous (e.g.,
        `"Write a note to Alex that I'm 5 minutes late"`), default to a concise,
        adaptable message rather than blocking on a clarifying question; ask
        only if the audience or core intent is genuinely unclear.
    -   Write the draft using the user's exact greeting pattern, sentence
        rhythm, transitions, punctuation habits, and sign-off, strictly
        excluding any banned or out-of-character words.
4.  **Surface or update the Voice Card non-blockingly:**
    -   **On the first writing task in a session (when newly inferred):** Below
        the completed draft, include a compact **Voice Card Snapshot** (3–5
        bullets summarizing the inferred style and sources read) and a one-line
        note that they can refine it or add banned words anytime.
    -   **On subsequent writing tasks:** Deliver the matched draft cleanly
        without repeating the Voice Card Snapshot unless the user asks to see it
        or you approximated a new format they haven't written in before (note
        any register approximation in one line below the draft).
    -   **When the user asks to view, edit, or update their Voice Card** (or
        edits a draft in a way that reveals a clear preference, such as swapping
        `"Hi"` for `"Hey"`): Update the Voice Card rules in context (and in
        their saved Voice Card Google Doc if one exists and editing is
        supported/confirmed) and confirm what changed in one sentence.

## Output Format

### Mode A: Writing or Rewriting Request (Default)

-   **Draft (top of response):** Present the clean, copy-ready draft first so
    the user can copy or use it immediately.
-   **Voice Card Snapshot (include on first scan or when requested; omit on
    routine repeat drafts):**
    -   `**Voice matched ([Sources read, e.g., Gmail sent mail, Google
        Docs]):**` 1–2 compact lines or 3–4 bullets covering **Register used**,
        **Openings & sign-offs**, **Rhythm & mechanics**, and **Avoided/banned
        phrasing**.
-   **Optional next step (one line max):** Offer to adjust the tone/length, add
    words to their "never use" list, or create a Gmail draft
    (`"Say 'create Gmail draft' if you'd like this staged in Gmail"`).

### Mode B: Standalone Voice Card Setup / Review

When the user asks to build, show, or update their Voice Card without a specific
writing task:

-   **Header:**
    `**Your Voice Card · Sources used: [Gmail, Google Docs / Pasted samples]**`
-   **Core Voice Profile:**
    -   **Sentence & Paragraph Rhythm:** [1 line]
    -   **Vocabulary & Contractions:** [1 line]
    -   **Signature Openings & Closings:** [1 line with real examples]
    -   **Punctuation & Formatting Quirks:** [1 line]
-   **Channel Registers:**
    -   **Email (External / Leadership):** [1–2 lines]
    -   **Email / Messages (Team & Peers):** [1–2 lines]
    -   **Long-Form / Docs:** [1–2 lines]
-   **Guardrails:**
    -   **Signature Phrases to Keep:** [comma-separated list]
    -   **Words to Avoid:** [inferred AI/corporate clichés + user-specified ban
        list]
-   **Closing line:** Ask what they'd like to draft first, or invite any quick
    corrections.

## Tool Usage Guide

Tool                       | When                                                                         | What to extract
:------------------------- | :--------------------------------------------------------------------------- | :--------------
Google Drive / Google Docs | First turn if connected (never loop if declined)                             | Search for an existing `"Voice Card"` doc first; if none exists, read 3–5 recent Google Docs authored by the user (`owner:me`) for long-form structure, headings, and tone.
Gmail (search & threads)   | First turn if connected and no Voice Card is loaded (never loop if declined) | Recent sent messages (`from:me newer_than:90d`); read threads (`get_thread`) newest-first across diverse recipients to extract greetings, sign-offs, sentence length, contractions, and tone shifts.
Gmail (create draft)       | Only when explicitly requested by the user or after `"yes"` confirmation     | Stage the completed email as a Gmail draft. Never send an email directly.

## Scope Boundaries & Gotchas

-   For remixing an article, transcript, or notes into 5 distinct creative
    content angles (`Contrarian`, `Personal Story`, `Data`, `Playbook`,
    `What They Missed`), route to `generate-fresh-ideas`.
-   For building a pre-meeting brief or 30-second glance card from workspace
    notes and calendar invites, route to `prep-for-meetings`.
-   For evaluating a decision across multiple simulated expert viewpoints, route
    to `get-more-perspectives`.
-   **Sent messages only — never mimic incoming mail:** When scanning Gmail
    threads or shared Google Docs, verify the message sender or document author
    is the user (`from:me` / `owner:me`) so another person's phrasing is never
    mistaken for the user's voice.
-   **Quote content without copying confidential facts into unrelated drafts:**
    Extract *stylistic patterns* (greetings, rhythm, transitions, sign-offs)
    from scanned emails and docs — never leak private details from unrelated
    threads into a new draft.
-   **Unseen formats:** If the user asks for a format not present in their
    Workspace samples (e.g., a public LinkedIn post when only internal emails
    exist), adapt their core sentence rhythm and vocabulary to the new format
    and note the approximation in one line below the draft rather than inserting
    inline warnings inside the draft text.

## Example

**User:** Help me draft an email to a realtor asking to see an open house at 742
Maple St on Sunday at noon.

**Subject:** Sunday open house at 742 Maple St — 12pm?

Hey [Realtor Name],

Quick question — is the open house at 742 Maple St this Sunday still on, and
would noon work for us to stop by and take a look?

If Sunday at 12pm requires a private slot or pre-registration, just let me know
what you need from my end.

Thanks, \
[Your Name]

--------------------------------------------------------------------------------

**Voice matched (Gmail sent mail):**

-   **Register:** External inquiry — friendly, direct, no small-talk preamble.
-   **Openings & closings:** Opens with `"Hey [Name],"` and
    `"Quick question —"`; signs off with `"Thanks,"`.
-   **Rhythm & mechanics:** Short 1–2 sentence paragraphs, natural contractions,
    and em dashes to connect clauses.

Want me to stage this as a Gmail draft, or tweak anything in your Voice Card
(like preferred sign-offs or words to avoid)?