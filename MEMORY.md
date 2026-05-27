# Repatriate Service — Project Memory

> Attach this file at the start of every new session: `#file:MEMORY.md`
> Update the Open Questions and Session History sections at the end of each session.

---

## CLAUDE WORKING RULES

**When providing code or file content to the user:**
- ALWAYS paste the COMPLETE file content in full so the user can overwrite the entire file.
- NEVER provide partial snippets, diffs, or "change this line" instructions when the user needs to edit a file manually.
- If a file needs editing and Claude cannot do it directly (e.g. `.github/workflows/` permission error), paste the entire file content in a code block so the user can select-all and replace.

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
**Hugo config baseURL:** `https://repatriationfuneral.com/`

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

**Template variants:** Five variants A-E implemented in site/layouts/routes/single.html. Controlled by template_variant: frontmatter field. All 48 live pages have variants assigned. Rotate across every batch.

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
9. Route pairs (`/routes/`) -- 48 pages live, 30,000+ target

**FTP deploy is incremental:** `dangerous-clean-slate: false`. Only changed files uploaded on each push. Never change this.

---

## 3. Pages and Content Completed

**Phase 3 (IN PROGRESS):** As of 28 May 2026:

| Silo | Status |
|------|--------|
| Country hubs | 238 countries published |
| City pages | Complete -- C1 through C22 done (220 pages) |
| Guides | All 26 P1 country guides published |
| Blog | 150 articles live |
| FAQ standalone pages | Published |
| Bringing ashes home | All 238 countries covered |
| Cremation transfer | All 238 countries covered |
| Embassy contacts | All 238 countries covered |
| Route pairs | 48 pages live (Turn A: 25, Turn C: 23) |

---

## 4. 7-Engine Status

| Engine | Status | Files |
|---|---|---|
| 1 -- Route generator | INSTALLED v2 | generate_routes.py |
| 2 -- Data layer | INSTALLED | site/data/route_data/ (11 origins, 22 corridors) |
| 3 -- Blog factory | PARTIAL | 150 articles live. Batch scripts pending. |
| 4 -- Link graph | INSTALLED | rebuild_link_graph.py, diagnose_links.py |
| 5 -- QA gate | INSTALLED | qa_routes.py, check_titles.py, check_schema.py, seo_pass.py |
| 6 -- Deploy pipeline | WORKING | .github/workflows/deploy.yml |
| 7 -- Operating system | INSTALLED | CLAUDE.md, AGENTS.md, workforce/, MEMORY.md, ERRORS.md |

---

## 5. Build Plan Navigation

**Next tasks in priority order:**
1. Engine 2 expansion -- add more origins to site/data/route_data/ (currently 11, need 50+)
2. Turn D -- next batch of 25 route pages using new origins
3. Engine 3 -- blog batch scripts for topical authority
4. MEMORY.md / BUILD-PLAN.md -- keep updated each session
5. Scale target: 30,000+ route pages

---

## 6. Route Pages -- Current Inventory (48 total)

### Turn A (25 pages -- manually written, full content, all variants assigned)
australia-to-ireland(A), australia-to-united-kingdom(E), cyprus-to-united-kingdom(C), egypt-to-united-kingdom(E), france-to-united-kingdom(C), germany-to-united-kingdom(D), greece-to-united-kingdom(B), india-to-united-kingdom(A), italy-to-united-kingdom(B), kenya-to-united-kingdom(B), morocco-to-united-kingdom(A), philippines-to-united-kingdom(E), portugal-to-united-kingdom(C), south-africa-to-united-kingdom(C), spain-to-ireland(B), spain-to-united-kingdom(A), sri-lanka-to-united-kingdom(E), thailand-to-ireland(E), thailand-to-united-kingdom(D), turkey-to-united-kingdom(D), uae-to-ireland(B), uae-to-united-kingdom(A), usa-to-ireland(D), usa-to-united-kingdom(C), vietnam-to-united-kingdom(D)

### Turn C (23 pages -- generated through full quality gate)
greece-to-ireland(B), cyprus-to-ireland(D), turkey-to-ireland(A), philippines-to-ireland(C), india-to-ireland(E), france-to-ireland(B), germany-to-ireland(C), portugal-to-ireland(D), italy-to-ireland(E), egypt-to-ireland(A), morocco-to-ireland(B), kenya-to-ireland(C), south-africa-to-ireland(D), vietnam-to-ireland(E), sri-lanka-to-ireland(A), canada-to-united-kingdom(B), new-zealand-to-united-kingdom(C), mexico-to-united-kingdom(D), nigeria-to-united-kingdom(E), ghana-to-united-kingdom(A), jordan-to-united-kingdom(B), indonesia-to-united-kingdom(C), brazil-to-united-kingdom(D)

**Template variant distribution:** A x10, B x10, C x10, D x9, E x9

---

## 7. Patterns to Follow

### Route Page Frontmatter (NO layout: field)

```yaml
---
title: "..."
description: "..."
origin_key: "..."
dest_key: "uk" or "ireland"
origin_name: "..."
dest_name: "United Kingdom" or "Ireland"
origin_slug: "..."
dest_slug: "united-kingdom" or "ireland"
slug: "{origin-slug}-to-{dest-slug}"
template_variant: "A" through "E" -- rotate across batch
route_complexity: "low|moderate|high"
timeline_avg: "..."
timeline_fast: "..."
timeline_complex: "..."
embassy_city: "..."
doc_processing_time: "..."
direct_answer_heading: "..."
direct_answer_intro: "..."
direct_answer_points:
  - "..."
overview_heading: "..."
overview_body: "..."
dest_reception: "..."
dest_consular: "..."
timeline_steps:
  - step: 1
    action: "..."
    timing: "..."
    responsible: "..."
faqs:
  - question: "..."
    answer: "..."
links:
  upward:
    - url: "/repatriation-from-{origin}/"
      text: "Full {Origin} repatriation guide"
    - url: "/guides/death-abroad-{origin}/"
      text: "What to do if someone dies in {Origin}"
    - url: "/embassy-contacts/{origin}/"
      text: "British Embassy in {Origin}"
    - url: "/contact/"
      text: "Send an enquiry to our team"
  sideways:
    - url: "/routes/{dest}-to-{origin}/"
      text: "Repatriation from {Dest} to {Origin}"
    - url: "/routes/{origin}-to-{alt-dest}/"
      text: "Repatriation from {Origin} to {AltDest}"
---
```

---

## 8. Mistakes Avoided

- **Never add `layout:` field to route page frontmatter.** Hugo silently skips pages with unresolvable layouts.
- **Never use `server-dir: /home/u356263466/...`** in deploy workflow. Correct path is `/public_html/`.
- **Never set `dangerous-clean-slate: true`** in FTP deploy. Causes timeout.
- **Never provide partial code snippets when user needs to edit a file manually.** Always paste the complete file content.
- **Never use Surge.** GitHub Actions to Hostinger FTP only.
- **Never place .md or non-JSON files inside site/data/ subdirectories.** Hugo tries to parse them as data.
- **Never set template_variant to anything outside A-E.** Hugo template conditionals only handle those five.

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

- Engine 2 expansion: need 50+ origins in route_data to enable Turn D and beyond.
- Engine 3: blog batch scripts not yet built.
- quoteFormEndpoint in hugo.toml is still a placeholder.
- LLM citation audit pass 2 pending.
- ERRORS.md E003 (stale sync-state) still possible; document the curl-delete fix.

---

## 11. Session History

| Date | Session Summary |
|------|---------------|
| April 23, 2026 | Full site design review pass complete. 16 issues fixed. |
| April 2026 | Phase 3 major work: slug fixes, cremation-transfer silo, LLM citation upgrades. |
| April 2026 | Migration session: MEMORY.md, BUILD-PLAN.md, AGENTS.md created for VS Code. |
| 27 May 2026 | CTR Rescue Turn A: 25 pages title/desc rewritten. Stage 3.CTR marked DONE. |
| 27 May 2026 | Route Engine Turn A: /routes/ silo built. 25 route pages committed. Deploy pipeline fixed. Discovered server-dir error (E002). Route page layout: frontmatter removed (E001). |
| 28 May 2026 | 7-engine install session: Engine 7 (CLAUDE.md, AGENTS.md, workforce), Engine 5 (full QA gate), Engine 2 (route_data layer, 11 origins), Engine 1 upgrade (reads route_data), Engine 4 (link graph tools). Turn C: 23 new route pages committed. Template rotation: all 48 pages now have A-E variants, single.html implements all 5 variants. Total route pages: 48. |
