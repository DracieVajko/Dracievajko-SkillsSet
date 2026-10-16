# Unresolved Sources and Licensing Issues

This document tracks items with unresolved provenance, licensing, or redistribution permission.

## Scope Definitions

The totals in this directory differ on purpose; each file tracks a different scope.

| Count | Scope | Source of truth |
|-------|-------|-----------------|
| 23 | Unresolved inventory records (no local content, no confirmed upstream) | `items.json` where `authorship` is `unresolved` |
| 22 | Custom-or-unverified entries | `unresolved-sources.json` where `source_type` is `custom-or-unverified` |
| 6 | Candidate-upstream records | `items.json` where `authorship` is `candidate_upstream` (same ids as the `third-party-candidate` rows in `unresolved-sources.json`) |
| 28 | Unresolved-sources total (22 + 6) | `unresolved-sources.json` |
| 26 | Historical "custom or unresolved" lists | `custom-or-unresolved.json` and `custom-skills.json` — pre-date the promotion of `applying-themes`, `building-mcp-servers`, `creating-skills` and `ticktick-tasks` to resolved local skills, and disagree on `writing-great-skills` vs `ticktick-tasks` |

`23` differs from `22` by exactly one record: `writing-great-skills` is unresolved in
`items.json` but is not listed in `unresolved-sources.json`. That gap is recorded here
rather than hidden by deleting or re-labelling records.

## Skills Requiring Content Export (28)

**Policy:** These items are retained as inventory entries only. Local content has not been exported. Original source remains unresolved. Not included as installable skills.

The table combines 22 custom-or-unverified entries with the 6 candidate-upstream
entries repeated in the next section (see Scope Definitions).

These skills are listed in the Odysseus inventory but have no local content or identified upstream source:

| Skill | Category | Status |
|-------|----------|--------|
| beyond-vibe-coding-autonomous-development | development | needs-content-export |
| generate-markdown-and-docx-documents | writing-docs | needs-content-export |
| enable-wake-on-lan-and-auto-shutdown-on-network-loss-for-ras | local-ai-infra | needs-content-export |
| create-individual-calendar-events-from-earnings-dates-list | productivity | needs-content-export |
| fix-inconclusive-skills | development | needs-content-export |
| smart-email-reading | productivity | needs-content-export |
| stock-picking-by-common-stocks-uncommon-profits-4 | investing | needs-content-export |
| generate-findings-report-from-pipeline-logs | development | needs-content-export |
| book-to-skill | writing-docs | needs-content-export |
| common-sense-index-investing-bogle-4 | investing | needs-content-export |
| create-professional-email-signature | writing-docs | needs-content-export |
| detailed-source-rewrite-guide | writing-docs | needs-content-export |
| document-editing-general | writing-docs | needs-content-export |
| drawio-skill | design | needs-content-export |
| firecrawl-deep-research-4 | research | needs-content-export |
| generate-markdown-document-via-file-tool | writing-docs | needs-content-export |
| github-code-documentation | development | needs-content-export |
| import-ics-events-into-google-calendar | productivity | needs-content-export |
| investing-from-darwin-4 | investing | needs-content-export |
| penetration-testing-guide | development | needs-content-export |
| save-long-opencode-prompts-as-markdown-documents | writing-docs | needs-content-export |
| universal-listing-template | writing-docs | needs-content-export |
| writing-great-skills | development | needs-content-export |
| banner-design | design | needs-verification (candidate: nextlevelbuilder/ui-ux-pro-max-skill) |
| make-interfaces-feel-better | design | needs-verification (candidate: jakubkrehel/make-interfaces-feel-better) |
| transitions-dev | design | needs-verification (candidate: Jakubantalik/transitions.dev) |
| transitions-polish | design | needs-verification (candidate: Jakubantalik/transitions.dev) |
| agent-browser-6 | web-automation | needs-verification (candidate: vercel-labs/agent-browser) |
| pptx-6 | writing-docs | needs-verification (candidate: anthropics/skills) |

**Handling:**
- Kept as inventory entries in `catalog/items.json` with `status: "needs-content-export"`
- **No local SKILL.md files created**
- **No skill directories created under `skills/`**
- Original source remains unresolved
- Not included as installable skills
- Listed here for tracking and future resolution

## Third-Party Skills with Candidate Upstreams (6)

These have candidate upstream repositories identified but content not verified:

| Skill | Category | Candidate Upstream |
|-------|----------|-------------------|
| banner-design | design | nextlevelbuilder/ui-ux-pro-max-skill |
| make-interfaces-feel-better | design | jakubkrehel/make-interfaces-feel-better |
| transitions-dev | design | Jakubantalik/transitions.dev |
| transitions-polish | design | Jakubantalik/transitions.dev |
| agent-browser-6 | web-automation | vercel-labs/agent-browser |
| pptx-6 | writing-docs | anthropics/skills |

**Handling:** Same as above — inventory only, no local content, not installable.

## Third-Party Skills with Unverified Content (17)

The following 17 skills have local copies with provenance metadata but have not been content-verified against their upstream sources:

| Skill | Upstream | Verification Needed |
|-------|----------|---------------------|
| using-superpowers | obra/superpowers | Content comparison |
| brainstorming | obra/superpowers | Content comparison |
| idea-to-plan | composio-community/opencode-skills | Content comparison |
| context-engineering | addyosmani/agent-skills | Content comparison |
| building-mcp-servers | anthropics/skills | Content comparison |
| code-reviewer | Jeffallan/claude-skills | Content comparison |
| debugging-wizard | Jeffallan/claude-skills | Content comparison |
| code-documenter | Jeffallan/claude-skills | Content comparison |
| creating-skills | anthropics/skills | Content comparison |
| wordpress-pro | Jeffallan/claude-skills | Content comparison |
| applying-themes | anthropics/skills | Content comparison |
| frontend-design-systems | composio-community/opencode-skills | Content comparison |
| fine-tuning-expert | Jeffallan/claude-skills | Content comparison |
| blender-geometry-nodes | composio-community/opencode-skills | Content comparison |
| blender-hard-surface-modeling | composio-community/opencode-skills | Content comparison |
| blender-python-integration | composio-community/opencode-skills | Content comparison |
| blender-rigging-animation | composio-community/opencode-skills | Content comparison |

**Status:** Local SKILL.md exists with provenance metadata. Marked `verification_status: unverified`. Included as installable skills but with unverified warning.

## Link Verification Status

The third-party link-only URLs in `03-third-party-skills/odysseus/` (`skill-links.txt`, `unverified-links.txt`) were cataloged from the prior Odysseus collection. Their HTTP reachability was checked on 2026-10-15 — see that directory's README and `docs/VERIFICATION.md`.

## Licensing Uncertainties

| Issue | Affected Items | Status |
|-------|----------------|--------|
| No explicit license file in some upstream repos | Several third-party skills | Evidence recorded per item (root `LICENSE`, README, or per-skill `LICENSE.txt`) |
| Redistribution permission unclear for adapted skills | All third-party skills | Only link-only for cataloged skills |
| Upstream licenses for local copies | 17 third-party skills | Recorded per item — MIT or Apache-2.0; see `docs/VERIFICATION.md` |

## Action Items

- [x] HTTP validate all Odysseus skill URLs (2026-10-15 — 154/154 returned HTTP 200)
- [ ] Content-compare local third-party skills against upstreams
- [ ] Resolve the outstanding inventory in `items.json` (23 `unresolved` + 6 `candidate_upstream` = 29 records): create content, find the upstream, or remove from inventory
- [x] Verify license evidence for all upstream repositories (recorded per item in each `SOURCE.md`)
- [ ] Confirm redistribution permission for adapted skills

---

*Last updated: 2026-10-15*