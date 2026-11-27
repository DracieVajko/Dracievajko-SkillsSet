---
name: frontend-design-resources
description: "Use when building or refining React UI: animated components/backgrounds from React Bits, or 12k+ shadcn/Tailwind components, templates and themes from 21st.dev."
version: 1.0.0
author: DracieVajko
tags: [react, ui, components, design, tailwind, shadcn, websites, resources]
category: design
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/frontend-design-resources/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Frontend Design Resources

Two curated, high-quality reference sites for React UI work. Use them to avoid
generic "AI average" output and to ship components with taste: React Bits for
animated/interactive React pieces, 21st.dev for a large catalog of
shadcn/Tailwind components, templates and themes.

This skill is a lookup aid, not a dependency. It tells the agent where to find
real, designed components and how to bring them into a project safely.

## When to Use

- The user asks for a React component, page, hero, pricing table, background,
  text animation, micro-interaction or visual polish.
- The current UI looks generic and needs a stronger, designed starting point.
- You need a ready-made component instead of hand-rolling one from scratch.
- The task mentions React, Tailwind, shadcn/ui, Next.js, Vite, Remix or Astro.
- The user explicitly names `reactbits.dev` or `21st.dev`.

Do NOT use this skill for backend, non-React or purely logic tasks.

## Resource 1 — React Bits (https://reactbits.dev/)

**What it is:** Animated React components and backgrounds that install as source
you own. Tune every value. Choose JavaScript or TypeScript, with plain CSS or
Tailwind. Copy the source or install a component with the CLI.

**Categories (browse by):**
- Text Animations
- Animations
- Components
- Backgrounds
- Micro Interactions

**Best for:** hero text reveals, animated backgrounds, hover micro-interactions,
loading/transition effects, decorative motion.

**How to use:**
1. Browse the category that matches the need (e.g. `/c/text-animations`).
2. Read the component source on the page (JS/TS, CSS/Tailwind variants).
3. Either copy the source into the project or install via the documented CLI.
4. Adapt tokens (colors, spacing, timing) to the project's design system.
5. Respect `prefers-reduced-motion` and accessibility (see frontend rules).

**Source of truth:** https://github.com/DavidHDev/react-bits
**Docs/install:** https://reactbits.dev/get-started/installation

## Resource 2 — 21st.dev (https://21st.dev/)

**What it is:** A community catalog of 12,000+ hand-crafted React + Tailwind +
shadcn/ui components, full templates and themes by real design engineers. Preview
live, install with one command. Components are copied into your repo (you own
them), no runtime dependency on 21st.

**Browse:**
- Components: https://21st.dev/community/components
- Templates: https://21st.dev/community/templates
- Themes: https://21st.dev/community/themes
- Component libraries: https://21st.dev/community/libraries

**Best for:** heroes, pricing sections, testimonials, buttons, inputs, dialogs,
marketing blocks, full page templates, shadcn themes, shaders/gradients.

**How to use:**
1. Search/browse the shelf that matches the need.
2. Preview live on the component page; read the full source.
3. Install via the shadcn CLI command shown on the page, OR use "Copy prompt"
   and paste into the coding agent so it rebuilds the component wired to the
   project stack.
4. Adapt to the project's design tokens (components use your tokens).
5. Verify accessibility, responsiveness and reduced-motion.

**Agent support:**
- Product summary: https://21st.dev/llms.txt
- MCP + CLI setup for coding agents: https://21st.dev/mcp.md
- Generate UI with 21st AI: https://21st.dev/ai.md
- Agent skills index: https://21st.dev/.well-known/skills/index.json
- Auth for agents: https://21st.dev/auth.md
- REST/OpenAPI: https://21st.dev/openapi.json

**CLI init (one-time):**
```bash
npx @21st-dev/cli@latest init --client <cursor|claude|codex|vscode|devin>
```

**Pricing note:** Browsing is free; 2 free component copies/day. Unlimited
copies and premium templates require membership. 21st AI is a paid add-on.

## Selection Guide

| Need | Prefer |
|------|--------|
| Animated text, backgrounds, micro-interactions, motion | React Bits |
| Static UI blocks (hero, pricing, testimonials, forms) | 21st.dev |
| Full page template / starter app | 21st.dev templates |
| Theme / color system / shadcn theme | 21st.dev themes |
| shadcn/ui-compatible primitive | 21st.dev (shadcn format) |

## Rules & Constraints

- Never copy a component verbatim without adapting tokens to the project.
- Never add a runtime dependency on either site; both ship source you own.
- Verify license/terms before redistributing copied code; 21st has free/paid
  tiers and per-author terms.
- Always check accessibility, keyboard paths, focus, contrast and
  `prefers-reduced-motion` after integrating.
- Prefer the project's existing components/tokens before importing new ones.
- Do not invent component APIs; use only what the site documents.

## Verification

- Confirm the chosen component renders and matches the project's theme.
- Run the project's build/lint/tests after integration.
- Check responsive layout (mobile + desktop) and reduced-motion.

## Related Skills

- `frontend-design` (external) — distinctive UI design direction.
- `ui-styling` (external) — shadcn/ui + Tailwind styling patterns.
- `avoid-ai-design` (external) — remove generic AI design tells.
- `make-interfaces-feel-better` (external) — polish details.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-11-27 | Initial release: React Bits + 21st.dev reference |
