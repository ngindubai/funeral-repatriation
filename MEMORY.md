# Repatriate Service -- Project Memory

> Read this file at the start of every run, alongside CLAUDE.md and BUILD-PLAN.md.
> Update the Current State, Next Tasks, and Session History sections at the end of each run.

---

## CLAUDE WORKING RULES (autonomous routine)

**This project is built by a scheduled cloud routine with no human watching. There is no approval step.**
- Build one block per run (25 routes, or one 5-article blog batch), pass the full QA gate, commit to master, post live links to Slack, stop.
- The Slack live-link post is a record of what shipped, posted after the push. It does not pause anything. The QA gate is the safety control: it must pass before any commit. If QA fails, do not commit; post the halt message and end.
- No "wait for go". No HTML preview. No stop condition: each run picks up the next unbuilt block.
- Links in the Slack record are clickable markdown hyperlinks, never bare URLs. Use /routes/[slug]/ for route pages, /blog/[slug]/ for blog articles, /repatriation-from-[country]/ for hubs.
- Deploy is automatic on push to master. Pages live within ~60 seconds.

---

## 1. Site Overview

**What it is:** A programmatic SEO lead generation website targeting UK and Irish families needing to repatriate a loved one who died abroad. Converts grief-driven search traffic into service enquiries.

**Target audience:** UK and Irish families searching in distress immediately after a death abroad; corporate travel managers; travel insurers seeking approved supplier networks.

**Primary goal:** Capture service enquiries. Every commercial-intent page has an enquiry form or phone CTA.

**Brand:** Repatriate Service. "Bringing your loved ones home."

**Final domain:** repatriateservice.com
**Current deployment:** repatriationfuneral.com (Hostinger)
**Production branch:** master (NOT main; master triggers deploy)
**Hugo config baseURL:** `https://www.repatriationfuneral.com/` -- MUST INCLUDE WWW (canonical fix, 1 Jun 2026).

**Tech stack:** Hugo v0.160.1-extended, Markdown + YAML frontmatter, TOML config (site/hugo.toml), JSON data (site/data/), GitHub Actions to live branch, Hostinger pulls live into /public_html/. Build: `hugo --gc --minify` from `site/`.

**NEVER use Surge.** Removed entirely.

**Hostinger server-dir:** `/public_html/` (confirmed May 2026).

---

## 2. Build Decisions

**Data-driven architecture:** Country content from `site/data/countries_repatriation.json`. Route data from `data/countries_repatriation.json` (238 countries, regulatory detail), `data/countries-197.json` (canonical country and slug list), `data/keyword_matrix.json` (per-corridor search demand and tier ordering).

**Route page frontmatter rule:** Do NOT include `layout:` field. Hugo auto-selects `routes/single.html`. Adding it silently skips the build. See ERRORS.md E001.

**server-dir rule:** Always `/public_html/`. See ERRORS.md E002.

**site/data/ rule:** NEVER place .md, .txt, or non-JSON files in site/data/. Hugo parses everything there as data. See ERRORS.md E006.

**baseURL rule:** ALWAYS include www. See ERRORS.md E007.

**buildFuture rule:** buildFuture = true in hugo.toml; author content with a safely past date. See ERRORS.md E012.

**Template variants:** Five A-E in site/layouts/routes/single.html, controlled by template_variant: frontmatter. Rotate across every block, no two consecutive pages sharing a variant.

**Route slug format:** `{origin-slug}-to-{destination-slug}.md`. Destination uses the full country slug (united-kingdom, ireland, united-states), not short keys.

**YMYL standards:** No safety guarantees, no prices, named dated sources only.

**FTP deploy.yml is disabled** (no-op stub). build-and-publish.yml (live branch) is the active pipeline. Do not re-enable deploy.yml.

---

## 3. Current State (5 June 2026)

| Silo | Status |
|------|--------|
| Country hubs | 238 countries published |
| City pages | 220 pages |
| Guides | 238 country guides |
| Blog | 239 articles live (target 500+) |
| Bringing ashes home | 238 countries |
| Cremation transfer | 238 countries |
| Embassy contacts | 238 countries |
| Route pairs | 170 of 38,612 (132 to UK, 32 to Ireland, 6 pre-matrix mixed) |

**Active build:** Phase R, the route matrix. Tier A in progress (170 of 394 built). Next block: chunk R5 (Tier A, Template A). 132 origins to UK built. See BUILD-PLAN.md for the tier breakdown and chunk ledger.

---

## 4. The Route Matrix (the growth engine)

Full origin-to-destination square: 197 countries x 197, minus same-country pairs = 38,612 route pages. Four tiers, highest commercial intent first:

- **Tier A (394):** every origin to United Kingdom and to Ireland. The revenue tier. 70 built, 324 remaining.
- **Tier B (~1,100):** diaspora and cross-border corridors to the top 12 destination hubs.
- **Tier C (~7,700):** regional and secondary destinations.
- **Tier D (~29,400):** long-tail completion of the square.

25 routes per block, template A-E rotation, built in `data/keyword_matrix.json` tier order. Full detail in BUILD-PLAN.md.

---

## 5. Next Tasks -- in priority order

1. **Route matrix, Tier A, chunk R5** (default every run): next 25 unbuilt Tier A routes, UK destinations before Ireland. 132 UK routes built (chunks pre-matrix + R1-R4). Continue chunk by chunk through Tier A.
2. After Tier A: Tier B, then C, then D, same block rhythm.
3. Blog batches 27 onward (first-contact cluster, cause-specific, sector deep-dives, then open-ended country long-tail): built on any run where the next route chunk is already committed.

There is no end state for the routine. When a tier completes, move to the next. When the matrix completes, the blog long-tail continues indefinitely.

---

## 6. Author Personas

Never Gareth. James Whitfield (coordinator, route/process), Dr. Amara Osei (consular/legal/embassy), Claire Sutton (family/bereavement/FAQ), Thomas Anand (logistics/air cargo). Full table in CLAUDE.md.

---

## 7. Patterns to Follow

### Route Page Frontmatter (NO layout: field)
```yaml
---
title: "..."
description: "..."
origin_key: "..."
dest_key: "..."         # full destination slug
template_variant: "A"   # rotate A-E
date: YYYY-MM-DD         # safely past
faqs:
  - question: "..."
    answer: "..."
---
```

### Blog Article Frontmatter
```yaml
---
title: "..."
description: "..."
date: YYYY-MM-DD
slug: slug-here
author: "[persona name]"
author_title: "[persona title], Repatriate Service"
category: "[category]"
faqs:
  - question: "..."
    answer: "..."
---
```
British English, no em dashes, 2+ internal links, named persona, FAQs in frontmatter.

---

## 8. Mistakes Avoided

- Never add `layout:` to route page frontmatter.
- Never use the long Hostinger server-dir path.
- Never set `dangerous-clean-slate: true`.
- Never use Surge.
- Never place non-JSON files in site/data/.
- Never set template_variant outside A-E.
- baseURL must include www.
- Never hardcode repatriationfuneral.com URLs in layouts.
- Never commit to main; master deploys.
- **Before generating any blog batch, check site/content/blog/ for an existing slug on the same topic.** Roadmap candidate lists are not pre-checked against live content. Several earlier candidates already existed and would have cannibalised live pages.

---

## 9. Design System (Locked)

Hero image assignments: Countries `mrwashingt0n-ai-generated-9048740.jpg`, Guides `documents-desk.jpg`, Blog `support-conversation.jpg`, Cremation `airport-cargo.jpg`, Embassy `passport-stamp.jpg`, Ashes `hero.jpg`, Routes `cargo-terminal-night.jpg`.

---

## 10. Open Questions

- GSC 'Alternate page with proper canonical tag': fixed 1 Jun 2026, monitoring.
- GSC 859 not-indexed URLs: audit pending.

---

## 11. Session History

| Date | Session Summary |
|------|---------------|
| 27 May 2026 | Route Engine Turn A: /routes/ silo built, 25 route pages, deploy pipeline fixed. |
| 28 May 2026 | 7-engine install. Turn C: 23 route pages. Total 48. |
| 1 Jun 2026 | GSC canonical fix (www). GEO/LLM 4-phase. Route pages: 70. |
| 2 Jun 2026 | Engine 3 Batches 4-6: 15 articles. Deploy structural fix (deploy.yml disabled, Hostinger pulls live). |
| 5 Jun 2026 | Engine 3 Batch 26: 5 seasonal articles. Blog total 239. |
| 5 Jun 2026 | Plan rebuild to Pet Transport parity: full 197x197 route matrix (38,612 target) installed across BUILD-PLAN.md, CLAUDE.md, MEMORY.md and the HTML tracker. Approval gate removed; routine now fully autonomous (build, QA, commit, report, stop; no wait-for-go, no stop condition). Chunk R1 (Tier A, Template A) is next. No content built in this entry. |
| 5 Jun 2026 | Chunks R1-R4 (batch 1): 100 new Tier A route pages to UK. cambodia, dominican-republic, poland, china, saudi-arabia, kuwait, qatar, bahrain, malaysia, austria, croatia, czech-republic, hungary, bulgaria, netherlands, belgium, sweden, norway, switzerland, denmark, finland, romania, bangladesh, jamaica, gambia, barbados, trinidad-and-tobago, cuba, colombia, argentina, peru, chile, albania, ukraine, georgia, azerbaijan, armenia, kazakhstan, oman, nepal, myanmar, taiwan, south-korea, north-macedonia, serbia, montenegro, slovakia, slovenia, estonia, latvia, lithuania, luxembourg, iceland, malta, iran, iraq, lebanon, laos, mongolia, afghanistan, kyrgyzstan, uzbekistan, tajikistan, turkmenistan, belarus, moldova, senegal, ivory-coast, ethiopia, tanzania, uganda, zimbabwe, zambia, mozambique, botswana, namibia, malawi, rwanda, cameroon, angola, algeria, tunisia, libya, sudan, eritrea, djibouti, somalia, south-sudan, democratic-republic-of-the-congo, congo, gabon, equatorial-guinea, burundi, sierra-leone, liberia, guinea, guinea-bissau, burkina-faso, benin, togo. All QA clean. 170 total route pairs live. |
