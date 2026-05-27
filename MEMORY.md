# Repatriate Service — Project Memory

> Attach this file at the start of every new session: `#file:MEMORY.md`
> Update the Open Questions and Session History sections at the end of each session.

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

**NEVER use Surge.** Surge has been removed from the deployment process entirely. Do not run `surge` commands. Do not reference Surge in any documentation.

---

## 2. Build Decisions

**Data-driven architecture:** Country content is driven by `site/data/countries_repatriation.json` (238 countries). Layout templates pull this data via `country_key` frontmatter. Changes to JSON field names cascade to all templates that read them — check layouts before modifying data structure.

**URL permalink design:** Defined in `hugo.toml` under `[permalinks]`. Country section uses `/repatriation-from-:slug/`. City pages use `/repatriation-from-:sections[last]/:slug/`. Route pages use `/routes/:slug/`. This is a live indexed structure — do not change.

**Slug requirement:** Every country `_index.md` must have an explicit `slug:` field set to just the country key (e.g. `brazil`). Hugo's automatic slug derivation from the long page title creates double-prefix ghost URLs (`/repatriation-from-repatriation-from-brazil-to-the-uk/`). This bug was fixed for 11 countries and 11 stub files deleted.

**--cleanDestinationDir on every build:** Regular `hugo --gc` does not remove stale output directories. Using `--cleanDestinationDir` is mandatory to prevent ghost pages persisting in `public/` after source files are deleted or renamed.

**Direct-answer frontmatter:** Key pages include `short_answer`, `direct_answer_heading`, `direct_answer_intro`, `direct_answer_points[]`, and `direct_answer_note` frontmatter fields. These are rendered by the `country-hub` layout as an above-fold structured answer block, optimised for LLM citation (ChatGPT, Perplexity, Gemini).

**YMYL content standards:** This is a death, legal, and financial content site. Every factual claim requires a named, dated source. No safety guarantees. Author attribution on substantive pages. These are non-negotiable SEO and legal liability requirements.

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

**Route pair engine (added May 2026):** New silo `/routes/` generates origin x destination pages (e.g. `/routes/spain-to-united-kingdom/`). Generator: `generate_routes.py`. QA gate: `qa_routes.py`. Template: `site/layouts/routes/single.html`. All content is frontmatter-driven — no body Markdown. Batch 1: 25 pages committed. Target: 30,000+ pages total. Run `python generate_routes.py` to add new batches. Run `python qa_routes.py` to audit existing pages.

**FTP deploy is incremental:** `dangerous-clean-slate: false` in `.github/workflows/deploy.yml`. Only changed files are uploaded on each push. Full re-upload is never done. This is intentional — do not change this setting.

**Workforce model:** Worker soul files in `workforce/` define role-specific rules for content creation, QA, and SEO. Engage the relevant worker's soul file before performing tasks in their domain.

---

## 3. Pages and Content Completed

**Phase 1:** Foundation — complete.

**Phase 2:** Core content — complete.

**Phase 3 (IN PROGRESS):** As of May 2026:

| Silo | Status |
|------|--------|
| Country hubs | 238 countries published |
| City pages (all chunks) | Complete — C1 through C22 done (220 pages) |
| Guides | All 26 P1 country guides published |
| Blog | 150 articles live |
| FAQ standalone pages | Published |
| Bringing ashes home | All 238 countries covered |
| Cremation transfer | All 238 countries covered |
| Embassy contacts | All 238 countries covered |
| Route pairs | Batch 1 (25 pages) committed May 2026 |

**CTR rescue (May 2026):** 25 highest-impression / lowest-CTR pages had title tags and meta descriptions rewritten. 14 country hubs had bare country names as titles — all replaced with descriptive titles. 7 pages had no meta description — all added.

**Route engine (May 2026):** `/routes/` silo created. 25 route pages committed. All 25 pass QA: titles ≤60 chars, descriptions ≤155 chars, 6 FAQs, 7 timeline steps, 6 internal links, no em-dashes, no prices, no banned words, 3 schema types (BreadcrumbList + Service + FAQPage + Organisation).

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
hero_image: "/images/[image].jpg"
layout: "country-hub"
date: YYYY-MM-DD
direct_answer_heading: "[Question matching primary keyword]"
direct_answer_intro: "[Opening sentence]"
direct_answer_points:
  - "[Specific fact]"
direct_answer_note: "[Caveat or edge case]"
---
```

### Route Page Frontmatter

```yaml
---
title: "[Origin] to [Dest] Repatriation: [trust signal]"
description: "[origin] to [dest] repatriation: [timeline]. [doc note]. [CTA]."
layout: route
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

### Content Voice Pattern

Short declarative sentence to open. Expand with specific detail. Cut to practical consequence.

---

## 6. Mistakes Avoided

- **Never omit `slug:` from country `_index.md` files.** Double-prefix ghost URLs.
- **Never run `hugo --gc --minify` without `--cleanDestinationDir`** after deleting content files.
- **Never edit `site/public/` directly.** Regenerated on every build.
- **Never change `[permalinks]` in `hugo.toml`** without planning a full redirect strategy.
- **Never use `fa-urn-trowel`.** Does not exist in FA6 Free. Use `fa-jar`.
- **Never use `country-card-link`.** Superseded by `country-card-cta`.
- **Never use Surge.** Deployment is GitHub Actions → Hostinger FTP only.
- **Never set `dangerous-clean-slate: true`** in the FTP deploy action. Causes timeout on large sites. Always incremental.
- **Never hardcode em-dashes in route page content.** The `esc()` function in `generate_routes.py` strips them. If editing frontmatter directly, use commas or colons instead.
- **Never generate route pages with `dangerous-clean-slate: false` off.** Always run `qa_routes.py` before committing a new batch.

---

## 7. Design System (Locked — April 2026)

### Hero Pattern for Listing Pages

```html
<section class="page-hero" style="background-image: url('/images/[image].jpg');">
    <div class="page-hero-content">
        <p class="label-sm">Repatriate Service</p>
        <h1>[H1]</h1>
        <p>[Intro]</p>
        <div class="hero-actions page-hero-actions">
            <a href="/contact/" class="btn btn-cta">Get Help Now</a>
        </div>
    </div>
</section>
```

### Hero Image Assignments

| Section | Image |
|---|---|
| Countries listing | `mrwashingt0n-ai-generated-9048740.jpg` |
| What to do abroad (guides) | `documents-desk.jpg` |
| Guidance articles (blog) | `support-conversation.jpg` |
| Cremation abroad | `airport-cargo.jpg` |
| Embassy contacts | `passport-stamp.jpg` |
| Bringing ashes home | `hero.jpg` |
| Routes | `cargo-terminal-night.jpg` |

---

## 8. Open Questions

- Phase 4 tasks (link building, schema expansion, conversion optimisation) not yet started.
- `quoteFormEndpoint` in hugo.toml is still a Formspree placeholder — real form endpoint not yet configured.
- LLM citation audit pass 2 — re-run Perplexity/ChatGPT queries once deploy is confirmed working.
- Route engine Turn B — next 25 corridors (high-value P2xP2 pairs, Ireland-origin routes).

---

## 9. Session History

| Date | Session Summary |
|------|-----------------|
| April 23, 2026 | Full site design review pass complete. 16 issues fixed. Build 269 pages, deployed. |
| April 2026 | Phase 3 major work: slug fixes, cremation-transfer silo, LLM citation upgrades. |
| April 2026 | Migration session: MEMORY.md, BUILD-PLAN.md, AGENTS.md created for VS Code. |
| 27 May 2026 | CTR Rescue Turn A: 25 pages title/desc rewritten. 14 bare country-name titles fixed. 7 missing meta descriptions added. Stage 3.CTR marked DONE. |
| 27 May 2026 | Route Engine Turn A: New /routes/ silo. generate_routes.py + qa_routes.py + routes/single.html committed. 25 route pages committed (all QA PASS). hugo.toml updated. Deploy workflow fixed (incremental FTP, security:loose, secrets-based credentials). Surge removed from all docs. MEMORY.md updated. |
