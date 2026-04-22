# New Page Creation — Repatriate Service (Hugo)

Before starting, attach:
- `#file:MEMORY.md` — project history and decisions
- `#file:BUILD-PLAN.md` — current phase status

Also read:
- `funeral-repatriation-build-plan.html` — the task you are building from
- `.github/copilot-instructions.md` — auto-loaded, confirms conventions

---

## Step 1: Confirm Before Building

Answer these before writing any content:

1. **Page type?** (country hub / city page / guide / blog / FAQ / bringing-ashes-home / cremation-transfer / embassy-contacts)
2. **Primary keyword target?** (the exact phrase this page should rank for)
3. **Search intent?** (informational / commercial / transactional)
4. **Which existing pages link to this new page?** (at least 2 must exist)
5. **Which existing pages should this new page link to?** (at least 2 must be identified)
6. **For country/city pages: does the `country_key` exist in `site/data/countries_repatriation.json`?**

---

## Step 2: Frontmatter Template by Page Type

### Country Hub (`countries/[country]/_index.md`)

```yaml
---
title: "Repatriation from [Country] to the UK"
description: "[140–160 chars with keyword and CTA]"
country_key: "[key from countries_repatriation.json]"
slug: "[country-key]"
hero_image: "/images/[relevant-image].jpg"
layout: "country-hub"
date: YYYY-MM-DD
short_answer: "[2–3 sentence direct answer to the primary search query]"
direct_answer_heading: "[Question format matching primary keyword]"
direct_answer_intro: "[Opening sentence of answer]"
direct_answer_points:
  - "[Specific fact: cost range, timeline, key document]"
  - "[Second specific fact]"
  - "[Third specific fact]"
direct_answer_note: "[Caveat, edge case, or season/route variation]"
---
```

### City Page (`countries/[country]/[city].md`)

```yaml
---
title: "Repatriation from [City], [Country] to the UK"
description: "[140–160 chars]"
country_key: "[matches parent country]"
slug: "[city-name]"
date: YYYY-MM-DD
---
```

### FAQ Page (`faq/[question-slug].md`)

```yaml
---
title: "[Question as title]"
description: "[140–160 chars]"
slug: "[question-in-kebab-case]"
date: YYYY-MM-DD
short_answer: "[Direct answer, 2–3 sentences]"
---
```
Body must include FAQ JSON-LD schema.

### Blog / Guide Page

```yaml
---
title: "[Title with keyword]"
description: "[140–160 chars]"
slug: "[kebab-case]"
date: YYYY-MM-DD
author: "Senior Repatriation Consultant"
---
```
Body must include Article schema JSON-LD.

---

## Step 3: Content Rules

- Tone: senior repatriation consultant — specific, direct, authoritative
- No banned vocabulary (delve, tapestry, robust, seamless — see `.github/copilot-instructions.md`)
- No em dashes
- Every factual claim needs a named, dated source or it gets cut
- Vary sentence length — high burstiness, not uniform paragraphs
- No safety guarantees or implied certainty

---

## Step 4: After Building

Run the self-review checklist automatically.

Reference: `#file:.github/prompts/self-review.prompt.md`

Do not mark the task done until the self-review passes all checks.
