---
applyTo: "site/**/*.md, site/**/*.html, site/**/*.toml"
---

# Code Standards — Repatriate Service (Hugo)

## Content Files (Markdown)

- File naming: kebab-case (`bangkok.md`, `what-happens-when-someone-dies-abroad.md`)
- Section hub files: `_index.md` inside a named directory — not a root-level `.md` file alongside the directory
- Frontmatter format: YAML with `---` delimiters
- Date format: `2025-04-20` (ISO 8601)

### Minimum Required Frontmatter

```yaml
---
title: "..."
description: "..."
date: YYYY-MM-DD
slug: "[kebab-case-matches-filename]"
---
```

### Country Hub Additional Fields

```yaml
country_key: "[key matching countries_repatriation.json]"
layout: "country-hub"
hero_image: "/images/[image].jpg"
```

### CRITICAL: Slug Rule

Every country `_index.md` MUST include an explicit `slug:` field set to just the country key.
Omitting it causes Hugo to slugify the full title and apply the section permalink prefix twice,
creating ghost URLs like `/repatriation-from-repatriation-from-brazil-to-the-uk/`.

Correct: `slug: "brazil"`
Wrong: `slug: "repatriation-from-brazil"` or missing entirely.

## Hugo Templates (layouts/)

- Follow existing template structure and naming conventions — do not introduce new template logic patterns unless explicitly asked.
- Access site-level data: `{{ .Site.Data.countries_repatriation }}`
- Country hub data lookup: templates use `.Params.country_key` to look up the country in the JSON data.
- Partials live in `layouts/partials/` — reference existing partials, do not duplicate functionality.
- Schema markup (JSON-LD): goes inside `{{ define "schema" }}` blocks or equivalent in the relevant layout.

## Configuration (hugo.toml)

- URL permalink structure is defined in `hugo.toml` under `[permalinks]` — do not change this without explicit instruction. It affects all existing indexed URLs.
- `baseURL = "https://repatriateservice.com/"` — do not change.

## Build and Deploy Commands (run from `site/` directory)

```powershell
# Full clean build (always use this — prevents stale output files creating ghost URLs)
hugo --gc --minify --cleanDestinationDir

# Local development server
hugo server

# Deploy to Surge
surge public/ uk-funeral-repatriation.surge.sh
```

## Data Files

- `site/data/countries_repatriation.json` — 26 countries, used by country hubs, bringing-ashes, cremation-transfer, embassy-contacts layouts.
- `site/data/cities_p1.json` and `site/data/cities_p2.json` — city data for city-level pages.
- `data/countries_repatriation.json` at project root — source research copy (not read by Hugo). Hugo reads from `site/data/`.
- Do not restructure JSON data field names without checking every layout template that reads those fields.

## No Restructuring Rule

Do not rename existing content files, reorganise directory structure, change permalink patterns, rename frontmatter fields, or modify existing layout template filenames without explicit instruction. This is a 269-page live site with established indexed URLs.

## Output Directory

`site/public/` is generated output. Never edit files there directly. Always rebuild after content changes.

---

## Design System — Locked Conventions (April 2026)

These patterns were established during the Phase 3 design review and must be followed on all new and modified pages.

### Hero Pattern — Listing / Hub Pages

All section listing pages (`list.html`) use the `page-hero` pattern — NOT `guide-hero`. This gives a full-width dark image hero consistent with the Countries page.

```html
<section class="page-hero" style="background-image: url('/images/[image].jpg');">
    <div class="page-hero-content">
        <p class="label-sm">Repatriate Service</p>
        <h1>[Page H1]</h1>
        <p>[Intro sentence]</p>
        <div class="hero-actions page-hero-actions">
            <a href="/contact/" class="btn btn-cta">Get Help Now</a>
        </div>
    </div>
</section>
```

**`guide-hero` (dark slate, two-column with facts sidebar) is ONLY for individual guide/country single pages**, not listing pages.

### Card Grid Pattern — Country/Guide Listing Pages

All listing pages that show a grid of country or topic cards use the `countries-grid` + `country-card` pattern. Do NOT use `guides-grid` / `guide-card` on listing pages — these are deprecated for listing use.

```html
<div class="countries-grid stagger-children">
    {{ range .Pages }}
    <a href="{{ .RelPermalink }}" class="country-card reveal">
        <div class="country-card-body">
            <h3>{{ .Params.country_name }}</h3>
            <p>[short description]</p>
            <p class="country-card-cta">Read guide <i class="fa-solid fa-arrow-right"></i></p>
        </div>
    </a>
    {{ end }}
</div>
```

### CTA Link Style in Cards

Use `country-card-cta` for the link label inside `country-card-body`. Do NOT use `country-card-link` — that class is superseded.

```html
<p class="country-card-cta">Read guide <i class="fa-solid fa-arrow-right"></i></p>
```

### Available Hero Images (site/static/images/)

| Image file | Best used for |
|---|---|
| `mrwashingt0n-ai-generated-9048740.jpg` | Countries listing (default hero) |
| `hero.jpg` | Homepage / generic |
| `documents-desk.jpg` | Guides / What to do abroad |
| `support-conversation.jpg` | Blog / Guidance articles |
| `airport-cargo.jpg` | Cremation abroad |
| `passport-stamp.jpg` | Embassy contacts |
| `airport-terminal.jpg` | General repatriation |
| `cargo-terminal-night.jpg` | Logistics / repatriation |
| `consultation-office.jpg` | Services / About |
| `document-checklist.jpg` | FAQs / legal guides |

### Nav Dropdown Icon Requirements

The Resources dropdown in `header.html` requires a Font Awesome icon before every item label. Use **only icons that exist in FA6 Free** (solid set). Current assignments:

| Item | Icon class |
|---|---|
| What to do abroad | `fa-solid fa-circle-info` |
| Cremation abroad | `fa-solid fa-fire` |
| Embassy contacts | `fa-solid fa-building-columns` |
| Bringing ashes home | `fa-solid fa-jar` |
| Guidance articles | `fa-solid fa-book-open` |

Do NOT use `fa-urn-trowel` — it does not exist in FA6 Free and renders as a broken icon.

### CSS Variables Available (defined in :root)

```css
--gold, --charcoal, --slate (#16222E), --white, --muted, --light
--surface (= --white), --surface-2 (#F5F4F2)
--border (#E9E9E9), --border-light
--accent (= --gold = #D5A021)
--text (= --charcoal = #050D15), --text-primary, --text-muted (#7A7A7A), --text-secondary
--bg-card (#FFFFFF), --bg-alt (#F8F6F3), --blue-mid (= --gold)
--warm-white, --radius, --transition
```

### Nav Vertical Alignment

`.nav-list li` has `display: flex; align-items: center;` — this keeps the Resources `<span>` toggle vertically aligned with `<a>` items. Do not remove this rule.
