# Repatriate Service — Copilot Instructions

## Site Identity

- This is a lead generation website for UK funeral repatriation services.
- Target audience: UK families needing to bring a loved one home from abroad, plus corporate travel managers and insurers.
- Primary goal: capture service enquiries from bereaved families searching for repatriation help.
- Brand: Repatriate Service
- Tagline: "Bringing your loved ones home"
- Final domain: repatriateservice.com
- Current deployment: uk-funeral-repatriation.surge.sh
- Tech stack: Hugo v0.160.1 (extended), Markdown content, YAML frontmatter, TOML config, JSON data files
- Build: `hugo --gc --minify --cleanDestinationDir` (run from `site/` directory)
- Deploy: `surge public/ uk-funeral-repatriation.surge.sh` (run from `site/` directory)

## Project Status

- Phase 3: Content Depth and Optimisation — IN PROGRESS
- Pages live: 269 (as of April 2026) across 26 countries
- Do NOT suggest restructuring existing files, renaming pages, reorganising directories, or changing established conventions unless explicitly asked.
- Always read `funeral-repatriation-build-plan.html` AND `BUILD-PLAN.md` before suggesting what to work on next.
- When completing a task, update `BUILD-PLAN.md` AND update `funeral-repatriation-build-plan.html` stage badges and notes.

## File and Directory Map

```
funeral-repatriation/
├── site/                        ← Hugo project root (run all Hugo commands here)
│   ├── content/                 ← Markdown content files
│   ├── layouts/                 ← Hugo templates (.html)
│   ├── data/                    ← JSON data files Hugo reads at build time
│   ├── static/                  ← Static assets (images, fonts, etc.)
│   ├── hugo.toml                ← Hugo configuration
│   └── public/                  ← Generated output (never edit directly)
├── data/                        ← Source research data (JSON, CSV, MD reports)
├── content/                     ← Raw content research documents
├── scripts/                     ← Utility scripts (e.g. citation audit Python)
├── workforce/                   ← Worker soul files (role-specific rules)
├── templates/                   ← Page template references
├── funeral-repatriation-build-plan.html  ← PRIMARY build plan (visual, with badges)
├── BUILD-PLAN.md                ← Session-start summary (updated each session)
├── MEMORY.md                    ← Project memory (attach at session start)
└── AGENTS.md                    ← Workforce map and engagement rules
```

## Hugo Conventions

- Content file naming: kebab-case (`repatriation-from-spain.md`, `what-happens-when-someone-dies-abroad.md`)
- Section hub files: `_index.md` inside a named directory, not a root-level `.md`
- Country hub pages: `site/content/countries/[country]/_index.md`
- CRITICAL: every country `_index.md` MUST have an explicit `slug: "[country]"` field. Omitting this causes Hugo to slugify the title and generate double-prefix ghost URLs (`/repatriation-from-repatriation-from-brazil-to-the-uk/`).
- Permalink config in `hugo.toml`: sections use `/repatriation-from-:slug/` — the slug must be just the country key (e.g. `brazil`, not `repatriation-from-brazil`).
- Do not edit files in `site/public/` — it is generated output, not source.
- When cleaning a build, always use `--cleanDestinationDir` to remove stale output files.

## Country Hub Frontmatter (Required Fields)

```yaml
---
title: "Repatriation from [Country] to the UK"
description: "..."
country_key: "[key matching countries_repatriation.json]"
slug: "[country-key]"
hero_image: "/images/[image].jpg"
layout: "country-hub"
---
```

## Direct Answer Frontmatter Pattern (LLM Citation)

For country hubs and high-value FAQ/blog pages, include these fields for LLM citation visibility:

```yaml
short_answer: "Plain prose direct answer to the primary search query, 2–3 sentences."
direct_answer_heading: "How long does repatriation from [Country] to the UK take?"
direct_answer_intro: "..."
direct_answer_points:
  - "First key fact..."
  - "Second key fact..."
direct_answer_note: "Caveat or edge case..."
```

## Content Silos (URL Structure)

| Silo | Path | URL Pattern |
|------|------|-------------|
| Country hubs | `countries/[country]/_index.md` | `/repatriation-from-[country]/` |
| City pages | `countries/[country]/[city].md` | `/repatriation-from-[country]/[city]/` |
| Guides | `guides/[guide].md` | `/guides/[guide]/` |
| Blog | `blog/[post].md` | `/blog/[post]/` |
| FAQ | `faq/[question].md` | `/faq/[question]/` |
| Bringing ashes home | `bringing-ashes-home/[country].md` | `/bringing-ashes-home/[country]/` |
| Cremation transfer | `cremation-transfer/[country].md` | `/cremation-transfer/[country]/` |
| Embassy contacts | `embassy-contacts/[country].md` | `/embassy-contacts/[country]/` |

## Data Architecture

- `site/data/countries_repatriation.json` — 26-country dataset. Every country page reads from this via `country_key` frontmatter.
- `site/data/cities_p1.json` and `cities_p2.json` — City data for city-level pages.
- Changes to data files affect all pages that reference them. Check the layout templates before modifying data structure.

## SEO Requirements (Non-Negotiable)

- Every page: unique title (50–60 characters) + meta description (140–160 characters) with keyword and CTA
- H1: exactly one per page, contains primary keyword
- First 100 words of body copy must contain the target keyword
- Images: descriptive alt text always — never empty, never "image of..."
- Internal links: minimum 2 per new page, descriptive anchor text (never "click here" or "read more")
- FAQ schema JSON-LD: all FAQ and informational pages
- This is a YMYL site (death, legal, financial). Google holds it to the highest E-E-A-T standards.

## Content Hard Rules

1. **YMYL compliance** — E-E-A-T signals mandatory. Author attribution, trust signals, and named+dated source citations required.
2. **No safety guarantees** — Never imply guaranteed outcomes. "Reduce risk" and "trained professionals" are fine. "Stay safe" and "guaranteed" are not. Legal liability issue.
3. **No banned vocabulary** — Never use: delve, tapestry, robust, seamless, elevate, foster, navigate (metaphorical), empower, revolutionise, game-changer, or any AI cliché patterns.
4. **No em dashes** — Use other punctuation.
5. **Authority voice** — Every page sounds like a senior repatriation consultant wrote it. Not a travel blog, not a marketing brochure, not a military briefing.
6. **Source attribution** — Every factual claim (cost, timeline, legal requirement, country regulation) has a named, dated source or it gets cut.
7. **High burstiness** — Vary sentence length. Mix very short sentences with longer ones. Never uniform paragraph length.

## Worker Soul Files

The `workforce/` directory contains role-specific rules that expand on these instructions. Read the relevant soul file before performing tasks in that worker's domain. See `AGENTS.md` for the full workforce map.

## Quality Self-Check (Run Before Finishing Any Task)

1. Does the Hugo build complete without errors? (`hugo --gc --minify --cleanDestinationDir` from `site/`)
2. Page count equal to or greater than before the session?
3. No ghost/double-prefix URLs in built output?
4. All new country `_index.md` files have explicit `slug:` field?
5. SEO requirements met? (title, description, H1, internal links, schema)
6. Content hard rules followed? (no banned vocab, no em dashes, source citations present)
7. At least 2 internal links with descriptive anchor text?
8. `BUILD-PLAN.md` updated?
9. `funeral-repatriation-build-plan.html` badges and notes updated?

Report any failures before marking done.

## Communication Rules

- State what you are about to do before doing it.
- If a task is ambiguous, ask one clarifying question before proceeding.
- When completing a task: list files changed, summarise what was done, and state the next recommended task.
- Flag any deviation from these instructions.
- Never restructure existing files, change URL structures, or rename established frontmatter fields without explicit instruction.
