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
**Current deployment:** uk-funeral-repatriation.surge.sh  
**Hugo config baseURL:** `https://repatriateservice.com/`

**Tech stack:**
- Static site generator: Hugo v0.160.1 (extended)
- Content: Markdown with YAML frontmatter
- Config: TOML (`site/hugo.toml`)
- Data: JSON (`site/data/`)
- Deployment: Surge.sh
- Build: `hugo --gc --minify --cleanDestinationDir` from `site/`
- Deploy: `surge public/ uk-funeral-repatriation.surge.sh` from `site/`

---

## 2. Build Decisions

**Data-driven architecture:** Country content is driven by `site/data/countries_repatriation.json` (26 countries). Layout templates pull this data via `country_key` frontmatter. Changes to JSON field names cascade to all templates that read them — check layouts before modifying data structure.

**URL permalink design:** Defined in `hugo.toml` under `[permalinks]`. Country section uses `/repatriation-from-:slug/`. City pages use `/repatriation-from-:sections[last]/:slug/`. This is a live indexed structure — do not change.

**Slug requirement:** Every country `_index.md` must have an explicit `slug:` field set to just the country key (e.g. `brazil`). Hugo's automatic slug derivation from the long page title creates double-prefix ghost URLs (`/repatriation-from-repatriation-from-brazil-to-the-uk/`). This bug was fixed for 11 countries and 11 stub files deleted.

**--cleanDestinationDir on every build:** Regular `hugo --gc` does not remove stale output directories. Using `--cleanDestinationDir` is mandatory to prevent ghost pages persisting in `public/` after source files are deleted or renamed.

**Direct-answer frontmatter:** Key pages include `short_answer`, `direct_answer_heading`, `direct_answer_intro`, `direct_answer_points[]`, and `direct_answer_note` frontmatter fields. These are rendered by the `country-hub` layout as an above-fold structured answer block, optimised for LLM citation (ChatGPT, Perplexity, Gemini).

**YMYL content standards:** This is a death, legal, and financial content site. Every factual claim requires a named, dated source. No safety guarantees. Author attribution on substantive pages. These are non-negotiable SEO and legal liability requirements.

**8 content silos established:**
1. Country hubs (`/repatriation-from-[country]/`)
2. City pages (`/repatriation-from-[country]/[city]/`)
3. Guides (`/guides/`)
4. Blog (`/blog/`)
5. FAQ (`/faq/`)
6. Bringing ashes home (`/bringing-ashes-home/`)
7. Cremation transfer (`/cremation-transfer/`)
8. Embassy contacts (`/embassy-contacts/`)

**Workforce model:** Worker soul files in `workforce/` define role-specific rules for content creation, QA, and SEO. Engage the relevant worker's soul file before performing tasks in their domain.

---

## 3. Pages and Content Completed

**Phase 1:** Foundation — complete. Hugo site setup, data architecture, URL structure, core layouts.

**Phase 2:** Core content — complete. Original P1 country hubs, core guides, initial FAQ pages, embassy contacts.

**Phase 3 (IN PROGRESS):** As of April 2026:

| Silo | Status |
|------|--------|
| Country hubs | 26/26 published |
| P1 city pages | Complete — all P1 countries have city depth |
| P2 city pages | Complete (Stage 3.3 done) |
| Guides | Published — see HTML build plan for count |
| Blog | Core posts published |
| FAQ standalone pages | Published (Stage 3.11 done) |
| Bringing ashes home | Published (Stage 3.4 done) |
| Cremation transfer | 26/26 complete (Turkey, Egypt, Morocco added April 2026) |
| Embassy contacts | All live countries covered (Stage 3.6 done) |

**URL slug bug fixed (April 2026):** 11 country `_index.md` files had `slug:` field added; 11 conflicting stub `.md` files deleted. Countries fixed: brazil, cambodia, cyprus, dominican-republic, indonesia, kenya, mexico, morocco, philippines, sri-lanka, vietnam.

**LLM citation pass 2 (April 2026):** Direct-answer frontmatter blocks added to: Kenya hub, Philippines hub, 3 FAQ pages (costs/who-pays, ashes-in-hand-luggage, what-does-embassy-do), 2 blog pages (what-happens-when-someone-dies-abroad, documents-needed-to-repatriate-body). Payer scenario tables, CAN/CANNOT tables, and conditions tables added.

---

## 4. Build Plan Navigation

**Primary tracker:** `funeral-repatriation-build-plan.html` — visual HTML with phase/stage definitions, task tables, and badge status (DONE / IN PROGRESS / TODO).

**Session summary:** `BUILD-PLAN.md` — read at session start for current phase state. Consult the HTML for full task detail.

**Current phase:** Phase 3 — Content Depth and Optimisation, IN PROGRESS.

**Immediately next:** Check `funeral-repatriation-build-plan.html` for the next IN PROGRESS or TODO item in Phase 3.

---

## 5. Patterns to Follow

### Country Hub Frontmatter

```yaml
---
title: "Repatriation from [Country] to the UK"
description: "[keyword + CTA, 140–160 chars]"
country_key: "[key matching countries_repatriation.json]"
slug: "[country-key — MUST be explicit]"
hero_image: "/images/[image].jpg"
layout: "country-hub"
date: YYYY-MM-DD
short_answer: "[2–3 sentence direct answer]"
direct_answer_heading: "[Question matching primary keyword]"
direct_answer_intro: "[Opening sentence]"
direct_answer_points:
  - "[Specific cost range or timeline]"
  - "[Key document or process step]"
  - "[Third specific fact]"
direct_answer_note: "[Caveat or edge case]"
---
```

### FAQ Page Frontmatter

```yaml
---
title: "[Question]"
description: "[140–160 chars with keyword and CTA]"
slug: "[question-in-kebab-case]"
date: YYYY-MM-DD
short_answer: "[Direct answer, 2–3 sentences, specific facts only]"
---
```

### Markdown Tables for LLM Extraction

Use for: cost breakdowns, document checklists, payer scenarios, timelines, CAN/CANNOT lists.

```markdown
| Scenario | Who pays |
|---|---|
| Valid travel insurance | Insurer — covers repatriation to UK |
| No insurance, estate has funds | Estate or family upfront |
```

### Content Voice Pattern

Short declarative sentence to open. Then expand with specific detail. Then cut to the practical consequence.

---

## 6. Mistakes Avoided

- **Never omit `slug:` from country `_index.md` files.** Hugo will slugify the long title and apply the section prefix twice, creating double-prefix ghost URLs that pass silently through a regular build.
- **Never run `hugo --gc --minify` without `--cleanDestinationDir` after deleting content files.** Stale `public/` directories persist and get deployed, creating live ghost pages.
- **Never edit `site/public/` directly.** It is regenerated on every build.
- **Never change `[permalinks]` in `hugo.toml` without planning a full redirect strategy.** All existing indexed URLs will break.
- **Never deploy without verifying the ghost URL check:** `Get-ChildItem public -Directory | Where-Object { $_.Name -like "*repatriation-from-repatriation*" }` should return empty.
- **Never rearrange JSON data field names** without auditing every layout template that reads those fields.
- **Never use `guide-hero` for listing pages.** It is dark slate with a facts sidebar — only for single guide/country detail pages. Listing pages (`list.html`) use `page-hero` with a background image.
- **Never use `guides-grid` / `guide-card` in listing templates.** These classes are deprecated for listing use. All listing grids use `countries-grid` + `country-card`.
- **Never use `fa-urn-trowel` as a Font Awesome icon.** It does not exist in FA6 Free and renders blank. Use `fa-jar` for ashes/urn context.
- **Never use `country-card-link` in new pages.** It is superseded by `country-card-cta`.

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

### Card Grid Pattern for Listing Pages

```html
<div class="countries-grid stagger-children">
    {{ range .Pages }}
    <a href="{{ .RelPermalink }}" class="country-card reveal">
        <div class="country-card-body">
            <h3>{{ .Params.country_name }}</h3>
            <p>[description]</p>
            <p class="country-card-cta">Read guide <i class="fa-solid fa-arrow-right"></i></p>
        </div>
    </a>
    {{ end }}
</div>
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

---

## 8. Open Questions

- Live LLM scoring for pass 2 citation upgrades not yet run — Perplexity, ChatGPT, Gemini test queries pending.
- Phase 4 tasks (link building, schema expansion, conversion optimisation) not yet started — see HTML build plan.
- `quoteFormEndpoint` in hugo.toml is still a Formspree placeholder — real form endpoint not yet configured.
- `emergencyPhone` in hugo.toml is still a placeholder — real phone number not yet set.

---

## 9. Session History

| Date | Session Summary |
|------|-----------------|
| April 23, 2026 | Full site design review pass complete. 16 issues fixed across 3 prompts: transparent nav, country card CSS conflict, FAQ spacing, ashes two-col layout, homepage redesign (How it Works badges, parallax CTA, dark guides section), Resources dropdown nav, listing page heroes, blog card grid, guide-card/guides-grid CSS. Follow-up: Resources listing pages standardised (page-hero + countries-grid on all 5 listing pages), nav alignment fixed, fa-jar icon fix. Build 269 pages, deployed. All design patterns locked into code-standards.instructions.md and MEMORY.md. |
| April 2026 | Phase 3 major work session: Stage A (11 slug fixes, 11 stub deletions), Stage B (Turkey/Egypt/Morocco cremation-transfer pages completing 26/26 silo), Stage C pass 2 (Kenya + Philippines hubs + 5 FAQ/blog pages upgraded with direct-answer content). Rebuilt with --cleanDestinationDir. Deployed. Build plan HTML updated. |
| April 2026 | Migration session: Created .github/ instruction files, MEMORY.md, BUILD-PLAN.md, AGENTS.md for standalone VS Code instance. Repo copied to Desktop. Fresh git repo initialised. |
