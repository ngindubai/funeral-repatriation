# Repatriate Service -- Project Memory

> Attach this file at the start of every new session: `#file:MEMORY.md`
> Update the Open Questions and Session History sections at the end of each session.

---

## CLAUDE WORKING RULES

**When providing code or file content to the user:**
- ALWAYS paste the COMPLETE file content in full so the user can overwrite the entire file.
- NEVER provide partial snippets, diffs, or "change this line" instructions when the user needs to edit a file manually.
- If a file needs editing and Claude cannot do it directly (e.g. `.github/workflows/` permission error), paste the entire file content in a code block so the user can select-all and replace.

**After every completed batch:**
- Output a live link list for every article or page published in that batch before stopping or updating BUILD-PLAN.
- Format: one URL per line, using https://www.repatriationfuneral.com/blog/[slug]/ for blog articles, /routes/[slug]/ for route pages.
- Deploy is automatic on push to master. Pages are live within ~60 seconds of commit.
- This is non-negotiable. No batch is complete until Gareth has the links.

---

## 1. Site Overview

**What it is:** A programmatic SEO lead generation website targeting UK and Irish families needing to repatriate a loved one who died abroad. The site converts grief-driven search traffic into service enquiries.

**Niche:** Funeral repatriation, international body transfer, ashes transport, consular support for bereaved UK and Irish families.

**Target audience:**
- UK and Irish families searching in distress immediately after a death abroad
- Corporate travel managers arranging repatriation after employee deaths
- Travel insurers looking for approved supplier networks

**Primary goal:** Capture service enquiries. Every commercial-intent page has an enquiry form or phone CTA.

**Brand:** Repatriate Service | "Bringing your loved ones home"

**Final domain:** repatriateservice.com
**Current deployment:** repatriationfuneral.com (Hostinger)
**Hugo config baseURL:** `https://www.repatriationfuneral.com/` -- MUST INCLUDE WWW. Changed 1 Jun 2026 to fix canonical mismatch.

**Tech stack:**
- Static site generator: Hugo v0.160.1 (extended)
- Content: Markdown with YAML frontmatter
- Config: TOML (`site/hugo.toml`)
- Data: JSON (`site/data/`)
- Deployment: GitHub Actions to Hostinger FTP (automatic on push to master)
- Build: `hugo --gc --minify` from `site/`
- Deploy: push to git. GitHub Actions builds and deploys automatically.

**NEVER use Surge.** Surge has been removed from the deployment process entirely.

**Hostinger FTP server-dir:** `/public_html/`
This is the confirmed correct path (confirmed May 2026 via Hostinger File Manager).
Do NOT use the long path with username. FTP chroots to account home.

---

## 2. Build Decisions

**Data-driven architecture:** Country content driven by `site/data/countries_repatriation.json` (238 countries). Route page data driven by `site/data/route_data/*.json` (per-origin JSON, Engine 2).

**URL permalink design:** Defined in `hugo.toml` under `[permalinks]`. Route pages use `/routes/:slug/`. Do not change.

**Route page frontmatter rule:** Do NOT include `layout:` field in route page frontmatter. Hugo auto-selects `routes/single.html`. Adding `layout: route` causes Hugo to silently skip building the page. See ERRORS.md E001.

**server-dir rule:** Always `/public_html/`. Never the long Hostinger path. See ERRORS.md E002.

**site/data/ rule:** NEVER place .md, .txt, or any non-JSON files inside site/data/ or any subdirectory. Hugo tries to parse everything in site/data/ as structured data. See ERRORS.md E006.

**baseURL rule:** ALWAYS include www: `https://www.repatriationfuneral.com/`. Without www, Google crawls www. version but canonical tags output non-www, causing 'Alternate page with proper canonical tag' for every page. See ERRORS.md E007.

**Template variants:** Five variants A-E implemented in site/layouts/routes/single.html. Controlled by template_variant: frontmatter field. All 70 live pages have variants assigned. Rotate across every batch.

**Direct-answer frontmatter:** Key pages include `direct_answer_heading`, `direct_answer_intro`, `direct_answer_points[]` frontmatter fields for LLM citation optimisation.

**YMYL content standards:** Death, legal, and financial content site. No safety guarantees. No prices. Named sources only.

**9 content silos established:**
1. Country hubs (`/repatriation-from-[country]/`)
2. City pages (`/repatriation-from-[country]/[city]/`)
3. Guides (`/guides/`)
4. Blog (`/blog/`)
5. FAQ (`/faq/`)
6. Bringing ashes home (`/bringing-ashes-home/`)
7. Cremation transfer (`/cremation-transfer/`)
8. Embassy contacts (`/embassy-contacts/`)
9. Route pairs (`/routes/`) -- 70 pages live, 30,000+ target

**FTP deploy is incremental:** `dangerous-clean-slate: false`. Only changed files uploaded on each push. Never change this.

**Live link rule (added 2 June 2026):** After every completed batch, output a live link list in the format:
```
https://www.repatriationfuneral.com/blog/[slug]/
```
One URL per line. Do this before updating BUILD-PLAN.md. Do not stop a session without outputting links for every batch completed that session.

---

## 3. Pages and Content Completed

**As of 2 June 2026:**

| Silo | Status |
|------|--------|
| Country hubs | 238 countries published |
| City pages | 220 pages complete |
| Guides | 238 country guides published |
| Blog | 142 articles live (Engine 3 Batches 1-6 complete) |
| FAQ standalone pages | Published |
| Bringing ashes home | All 238 countries covered |
| Cremation transfer | All 238 countries covered |
| Embassy contacts | All 238 countries covered |
| Route pairs | 70 pages live |

**Engine 3 blog batches complete:**
- Batch 1: Cost cluster (5 articles)
- Batch 2: Timeline cluster (5 articles)
- Batch 3: Documents deep-dive (5 articles)
- Batch 4: Religious and cultural specifics (5 articles)
- Batch 5: Special circumstances (5 articles)
- Batch 6: UK reception cluster (5 articles)
- Total new articles from Engine 3: 30

---

## 4. 7-Engine Status

| Engine | Status | Files |
|---|---|---|
| 1 -- Route generator | INSTALLED v2 | generate_routes.py |
| 2 -- Data layer | INSTALLED | site/data/route_data/ (32 origins) |
| 3 -- Blog factory | IN PROGRESS | 142 articles live. Batches 1-6 done. Batch 7 next. |
| 4 -- Link graph | INSTALLED | rebuild_link_graph.py, diagnose_links.py |
| 5 -- QA gate | INSTALLED | qa_routes.py, check_titles.py, check_schema.py, seo_pass.py |
| 6 -- Deploy pipeline | WORKING | .github/workflows/deploy.yml |
| 7 -- Operating system | INSTALLED | CLAUDE.md, AGENTS.md, workforce/, MEMORY.md, ERRORS.md |

---

## 5. Build Plan Navigation

**Next tasks in priority order:**
1. Engine 3 Batch 7 -- airline-policy cluster (5 articles)
2. GSC not-indexed audit -- export and categorise 859 URLs
3. Turn E -- next 50 route pages from existing 32 origins
4. Reverse route pages (uk-to-{country})
5. Engine 2 further expansion -- eastern Europe + more Asia origins

---

## 6. Route Pages -- Current Inventory (70 total)

### Turn A (25 pages)
australia-to-ireland, australia-to-united-kingdom, cyprus-to-united-kingdom, egypt-to-united-kingdom, france-to-united-kingdom, germany-to-united-kingdom, greece-to-united-kingdom, india-to-united-kingdom, italy-to-united-kingdom, kenya-to-united-kingdom, morocco-to-united-kingdom, philippines-to-united-kingdom, portugal-to-united-kingdom, south-africa-to-united-kingdom, spain-to-ireland, spain-to-united-kingdom, sri-lanka-to-united-kingdom, thailand-to-ireland, thailand-to-united-kingdom, turkey-to-united-kingdom, uae-to-ireland, uae-to-united-kingdom, usa-to-ireland, usa-to-united-kingdom, vietnam-to-united-kingdom

### Turn C (23 pages)
greece-to-ireland, cyprus-to-ireland, turkey-to-ireland, philippines-to-ireland, india-to-ireland, france-to-ireland, germany-to-ireland, portugal-to-ireland, italy-to-ireland, egypt-to-ireland, morocco-to-ireland, kenya-to-ireland, south-africa-to-ireland, vietnam-to-ireland, sri-lanka-to-ireland, canada-to-united-kingdom, new-zealand-to-united-kingdom, mexico-to-united-kingdom, nigeria-to-united-kingdom, ghana-to-united-kingdom, jordan-to-united-kingdom, indonesia-to-united-kingdom, brazil-to-united-kingdom

### Turn D+ (22 pages)
brazil-to-ireland, canada-to-ireland, ghana-to-ireland, indonesia-to-ireland, israel-to-ireland, israel-to-united-kingdom, japan-to-ireland, japan-to-united-kingdom, jordan-to-ireland, mexico-to-ireland, new-zealand-to-ireland, nigeria-to-ireland, pakistan-to-ireland, pakistan-to-united-kingdom, singapore-to-ireland, singapore-to-united-kingdom, south-africa-to-ireland (check duplicate), vietnam-to-ireland (check duplicate)

---

## 7. Patterns to Follow

### Blog Article Frontmatter (Engine 3 standard)

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

All articles: British English, no em dashes, 2+ internal links, named author persona, FAQs in frontmatter.

### Route Page Frontmatter (NO layout: field)

```yaml
---
title: "..."
description: "..."
origin_key: "..."
dest_key: "uk" or "ireland"
...
---
```

---

## 8. Mistakes Avoided

- Never add `layout:` field to route page frontmatter.
- Never use `server-dir: /home/u356263466/...` in deploy workflow.
- Never set `dangerous-clean-slate: true` in FTP deploy.
- Never provide partial code snippets when user needs to edit a file manually.
- Never use Surge.
- Never place .md or non-JSON files inside site/data/ subdirectories.
- Never set template_variant to anything outside A-E.
- baseURL must include www.
- Never hardcode repatriationfuneral.com URLs in layouts.
- **Never complete a batch without outputting live links for Gareth.**

---

## 9. Design System (Locked)

### Hero Image Assignments

| Section | Image |
|---|---|
| Countries listing | `mrwashingt0n-ai-generated-9048740.jpg` |
| Guides | `documents-desk.jpg` |
| Blog | `support-conversation.jpg` |
| Cremation abroad | `airport-cargo.jpg` |
| Embassy contacts | `passport-stamp.jpg` |
| Bringing ashes home | `hero.jpg` |
| Routes | `cargo-terminal-night.jpg` |

---

## 10. Open Questions

- GSC 'Alternate page with proper canonical tag': fixed 1 Jun 2026. Monitor over 7-14 days.
- GSC 859 not-indexed URLs: audit pending.
- seo_pass.py not yet run on Turn D+ pages.
- rebuild_link_graph.py --fix not yet run on 70-page set.

---

## 11. Session History

| Date | Session Summary |
|------|---------------|
| April 23, 2026 | Full site design review pass complete. 16 issues fixed. |
| April 2026 | Phase 3 major work: slug fixes, cremation-transfer silo, LLM citation upgrades. |
| April 2026 | Migration session: MEMORY.md, BUILD-PLAN.md, AGENTS.md created for VS Code. |
| 27 May 2026 | CTR Rescue Turn A: 25 pages title/desc rewritten. Stage 3.CTR marked DONE. |
| 27 May 2026 | Route Engine Turn A: /routes/ silo built. 25 route pages committed. Deploy pipeline fixed. |
| 28 May 2026 | 7-engine install: Engine 7, 5, 2, 1 upgrade, 4. Turn C: 23 route pages. Total: 48. |
| 29 May 2026 | GSC indexing audit: fixed empty city pages, thin country hubs, Guatemala encoding bug. |
| 1 Jun 2026 | GSC canonical fix: baseURL changed to www. Fixed non-www URLs in baseof.html. |
| 1 Jun 2026 | GEO/LLM implementation: 4-phase playbook. FAQPage schema, llms.txt, methodology page. |
| 1 Jun 2026 | Docs sync: BUILD-PLAN.md and MEMORY.md updated. Route pages: 70. Origins: 32. |
| 1 Jun 2026 | Fix all known issues: E008-E011 resolved (sideways links, robots.txt, permalink, schema). |
| 1 Jun 2026 | Engine 3 Batches 1-3: 15 articles (cost cluster, timeline cluster, documents deep-dive). |
| 2 Jun 2026 | Engine 3 Batches 4-6: 15 articles (religious/cultural, special circumstances, UK reception). Total blog: 142. Added live link output rule to CLAUDE.md and MEMORY.md. |
