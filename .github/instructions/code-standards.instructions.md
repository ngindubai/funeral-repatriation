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
