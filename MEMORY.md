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

**What it is:** A programmatic SEO lead generation website targeting UK families needing to repatriate a loved one who died abroad. The site converts grief-driven search traffic into service enquiries.

**Niche:** Funeral repatriation, international body transfer, ashes transport, consular support for bereaved UK families.

**Target audience:**
- UK families searching in distress immediately after a death abroad
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
- Deployment: GitHub Actions → Hostinger FTP (automatic on push to master)
- Build: `hugo --gc --minify --cleanDestinationDir` from `site/`
- Deploy: push to git. GitHub Actions builds and deploys automatically. No manual step.

**NEVER use Surge.** Surge has been removed from the deployment process entirely.

**Hostinger FTP server-dir:** `/home/u356263466/domains/repatriationfuneral.com/public_html/`
This is the correct full path. Do NOT use `/public_html/` (wrong — goes to wrong folder).

---

## 2. Build Decisions

**Data-driven architecture:** Country content is driven by `site/data/countries_repatriation.json` (238 countries). Layout templates pull this data via `country_key` frontmatter. Changes to JSON field names cascade to all templates that read them — check layouts before modifying data structure.

**URL permalink design:** Defined in `hugo.toml` under `[permalinks]`. Country section uses `/repatriation-from-:slug/`. City pages use `/repatriation-from-:sections[last]/:slug/`. Route pages use `/routes/:slug/`. This is a live indexed structure — do not change.

**Slug requirement:** Every country `_index.md` must have an explicit `slug:` field set to just the country key (e.g. `brazil`). Hugo's automatic slug derivation from the long page title creates double-prefix ghost URLs.

**--cleanDestinationDir on every build:** Mandatory to prevent ghost pages persisting in `public/`.

**Direct-answer frontmatter:** Key pages include `direct_answer_heading`, `direct_answer_intro`, `direct_answer_points[]`, and `direct_answer_note` frontmatter fields for LLM citation optimisation.

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
9. Route pairs (`/routes/`) — added May 2026

**Route pair engine (added May 2026):** New silo `/routes/` generates origin x destination pages. Generator: `generate_routes.py`. QA gate: `qa_routes.py`. Template: `site/layouts/routes/single.html`. No `layout:` field in frontmatter — Hugo auto-selects `routes/single.html`. Batch 1: 25 pages live. Target: 30,000+ pages total.

**FTP deploy is incremental:** `dangerous-clean-slate: false`. Only changed files uploaded on each push. Never change this.

**Route page frontmatter rule:** Do NOT include `layout:` field in route page frontmatter. Hugo auto-selects `routes/single.html` for all pages in the routes section. Adding `layout: route` causes Hugo to look for a non-existent layout and silently skip building the page.

---

## 3. Pages and Content Completed

**Phase 3 (IN PROGRESS):** As of May 2026:

| Silo | Status |
|------|--------|
| Country hubs | 238 countries published |
| City pages | Complete — C1 through C22 done (220 pages) |
| Guides | All 26 P1 country guides published |
| Blog | 150 articles live |
| FAQ standalone pages | Published |
| Bringing ashes home | All 238 countries covered |
| Cremation transfer | All 238 countries covered |
| Embassy contacts | All 238 countries covered |
| Route pairs | Batch 1 (25 pages) committed May 2026 |

---

## 4. Build Plan Navigation

**Primary tracker:** `funeral-repatriation-build-plan.html`
**Session summary:** `BUILD-PLAN.md` — read at session start.
**Current phase:** Phase 3 — Content Depth and Optimisation, IN PROGRESS.

---

## 5. Patterns to Follow

### Country Hub Frontmatter

```yaml
---
title: "Repatriation from [Country] to the UK"
description: "[keyword + CTA, 140-160 chars]"
country_key: "[key matching countries_repatriation.json]"
slug: "[country-key — MUST be explicit]"
layout: "country-hub"
date: YYYY-MM-DD
direct_answer_heading: "[Question matching primary keyword]"
direct_answer_intro: "[Opening sentence]"
direct_answer_points:
  - "[Specific fact]"
direct_answer_note: "[Caveat or edge case]"
---
```

### Route Page Frontmatter (NO layout: field)

```yaml
---
title: "[Origin] to [Dest] Repatriation: [trust signal]"
description: "[origin] to [dest] repatriation: [timeline]. [CTA]."
origin_key: "[json key]"
dest_key: "uk"
origin_name: "[display name]"
dest_name: "United Kingdom"
origin_slug: "[url slug]"
dest_slug: "united-kingdom"
slug: "[origin-slug]-to-[dest-slug]"
route_complexity: "low|moderate|high"
timeline_avg: "[X-Y days/weeks]"
timeline_fast: "[X-Y days]"
timeline_complex: "[X-Y weeks]"
embassy_city: "[city]"
doc_processing_time: "[X-Y days]"
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
    - url: "/repatriation-from-[origin]/"
      text: "..."
  sideways:
    - url: "/routes/[dest]-to-[origin]/"
      text: "..."
---
```

---

## 6. Mistakes Avoided

- **Never omit `slug:` from country `_index.md` files.** Double-prefix ghost URLs.
- **Never run `hugo --gc --minify` without `--cleanDestinationDir`.**
- **Never edit `site/public/` directly.** Regenerated on every build.
- **Never change `[permalinks]` in `hugo.toml`** without planning redirects.
- **Never use `fa-urn-trowel`.** Use `fa-jar`.
- **Never use Surge.** GitHub Actions → Hostinger FTP only.
- **Never set `dangerous-clean-slate: true`** in FTP deploy. Causes timeout.
- **Never add `layout:` field to route page frontmatter.** Hugo silently skips pages with unresolvable layouts. Routes section auto-selects `routes/single.html`.
- **Never use `server-dir: /public_html/`** in deploy workflow. Correct path is `/home/u356263466/domains/repatriationfuneral.com/public_html/`.
- **Never provide partial code snippets when user needs to edit a file manually.** Always paste the complete file content.

---

## 7. Design System (Locked — April 2026)

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

## 8. Open Questions

- Phase 4 tasks (link building, schema expansion, conversion optimisation) not yet started.
- `quoteFormEndpoint` in hugo.toml is still a Formspree placeholder.
- LLM citation audit pass 2 pending.
- Route engine Turn B — next 25 corridors.

---

## 9. Session History

| Date | Session Summary |
|------|-----------------|
| April 23, 2026 | Full site design review pass complete. 16 issues fixed. |
| April 2026 | Phase 3 major work: slug fixes, cremation-transfer silo, LLM citation upgrades. |
| April 2026 | Migration session: MEMORY.md, BUILD-PLAN.md, AGENTS.md created for VS Code. |
| 27 May 2026 | CTR Rescue Turn A: 25 pages title/desc rewritten. Stage 3.CTR marked DONE. |
| 27 May 2026 | Route Engine Turn A: /routes/ silo built. 25 route pages committed. Deploy pipeline fixed. Discovered server-dir was wrong (/public_html/ instead of full Hostinger path). Route page layout: frontmatter removed (was causing Hugo to silently skip building pages). MEMORY.md updated with full working rules. |
