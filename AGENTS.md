# Repatriate Service — Workforce

The `workforce/` directory contains worker soul files. Each defines a role, domain rules, quality gates, and engagement protocol. Read the relevant soul file before performing tasks in that worker's domain.

---

## Leadership

| Worker | File | Role | Engage When |
|--------|------|------|-------------|
| The Architect | `workforce/leadership/the-architect.md` | Phase orchestration, planning, stage gate decisions | Starting a new phase, making structural decisions, resolving ambiguity about scope |
| The Auditor | `workforce/leadership/the-auditor.md` | Legal accuracy, regulatory compliance, YMYL QA | Any claim involving law, country regulation, cost, process steps, or official requirements |

## Content

| Worker | File | Role | Engage When |
|--------|------|------|-------------|
| The Wordsmith | `workforce/content/the-wordsmith.md` | Copywriting, editorial voice, authority tone | Writing or rewriting any page content |
| The Chameleon | `workforce/content/the-chameleon.md` | Anti-AI humaniser, authenticity and burstiness pass | Content that needs to sound human-authored — apply after The Wordsmith |
| The Interrogator | `workforce/content/the-interrogator.md` | FAQ generation, entity question research | Building FAQ pages, question clusters, or researching what users actually ask |

## Intelligence

| Worker | File | Role | Engage When |
|--------|------|------|-------------|
| The Geographer | `workforce/intelligence/the-geographer.md` | Country-specific risk, geography, logistics analysis | Writing country or city pages requiring local knowledge |
| The Scout | `workforce/intelligence/the-scout.md` | Keyword research, SERP analysis, market reconnaissance | Keyword targeting decisions, competitor analysis |
| The Spider | `workforce/intelligence/the-spider.md` | Data extraction, web research | Gathering source data, researching factual claims |

## Development

| Worker | File | Role | Engage When |
|--------|------|------|-------------|
| The Builder | `workforce/development/the-builder.md` | Template creation, page generation, deployment | Building new page types, creating Hugo templates, deployment tasks |
| The Librarian | `workforce/development/the-librarian.md` | Data management, JSON schema, data files | Modifying countries_repatriation.json, adding data fields, data architecture decisions |

## SEO

| Worker | File | Role | Engage When |
|--------|------|------|-------------|
| The Optimiser | `workforce/seo/the-optimiser.md` | On-page SEO, schema markup, E-E-A-T signals | SEO review of any page, schema implementation, meta tag optimisation |
| The Connector | `workforce/seo/the-connector.md` | Internal linking strategy, backlink planning | Internal linking audits, anchor text decisions, link building tasks |

## Monitoring

| Worker | File | Role | Engage When |
|--------|------|------|-------------|
| The Analyst | `workforce/monitoring/the-analyst.md` | Performance tracking, LLM citation audits, analytics | Running citation audits, reviewing performance data, deciding what to optimise |
| The Watchdog | `workforce/monitoring/the-watchdog.md` | Site health, uptime, build verification | Post-deployment checks, broken link audits, build verification |

---

## Engagement Rule

When a task requires domain-specific judgment — writing country content, checking a regulation, generating FAQ questions, running a citation audit — read the relevant soul file in full before proceeding. The soul files contain quality gates, banned patterns, and domain knowledge that is not repeated in the main instructions.
