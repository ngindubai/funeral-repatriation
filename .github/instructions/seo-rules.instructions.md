---
applyTo: "site/content/**/*.md, site/layouts/**/*.html"
---

# SEO Rules — Repatriate Service

This is a YMYL lead generation website. SEO is the primary acquisition channel. Every rule below is non-negotiable.

## Page-Level Requirements

- **Title**: unique, 50–60 characters, contains primary keyword
- **Meta description**: 140–160 characters, emotionally resonant, contains CTA (e.g. "Get expert guidance today")
- **H1**: exactly one per page, contains primary keyword, appears above the fold
- **First 100 words**: target keyword must appear naturally within the first 100 words of body copy
- **Images**: descriptive alt text always — never empty, never "image of X", never the filename

## Internal Linking

- Minimum 2 internal links per new page
- Anchor text must be descriptive — never "click here", "read more", or "this page"
- Country hub pages must link to: at least 2 city pages, the relevant embassy contact page, and at least one guide
- City pages must link back to their country hub and to at least one adjacent city page
- FAQ pages must link to relevant country hubs or guides

## Schema Markup

- FAQ pages: `FAQPage` JSON-LD schema with `Question` and `AcceptedAnswer` entities
- Country hub pages: `Service` or `Article` schema with `author` entity
- Blog pages: `Article` schema with `author`, `datePublished`, `dateModified`
- Embassy contact pages: `GovernmentService` or `LocalBusiness` schema

## LLM Citation (Direct-Answer Optimisation)

For country hubs and high-priority FAQ/blog pages that target informational queries:

- Include `short_answer` frontmatter: a plain-prose direct answer to the primary search query, 2–3 sentences, factual and specific (costs, timelines, key steps).
- Include `direct_answer_*` frontmatter block (heading, intro, points[], note) — rendered by the country-hub layout as a citation-friendly answer block.
- Use markdown tables with `| Header | Column |` format for scannable data: costs by category, timelines, document checklists. LLMs extract tabular data reliably.
- Never pad the direct-answer block with filler. Every sentence must contain a specific, extractable fact.

## YMYL Rules

- Every factual claim involving cost, timeline, legal requirement, or country regulation must have a named, dated source — or it gets cut.
- Never imply guaranteed outcomes: "can help reduce risk" not "will protect you". "Typically takes 14–28 days" not "repatriation is quick".
- Author attribution required on all substantive pages (guides, country hubs, blog posts).
- Trust signals required: professional context for any quoted advice, named sources for statistics.

## Content Quality for SEO

- **No banned vocabulary**: delve, tapestry, robust, seamless, elevate, foster, navigate (metaphorical), empower, revolutionise, game-changer, cutting-edge, comprehensive (unless it genuinely is). These signal AI-generated content to ranking systems.
- **No em dashes** — use commas, colons, or a new sentence instead.
- **Sentence rhythm**: vary length deliberately. Short declarative sentences alongside longer explanatory ones. Never uniform paragraph length. High burstiness score.
- **Tone**: senior repatriation consultant. Not travel blog. Not marketing brochure. Not government leaflet. Authoritative, specific, and direct.
- **No safety guarantees**: this is a legal liability issue as well as an E-E-A-T issue.

## Page Types and Their SEO Priority

| Page Type | Primary Intent | Key SEO Signal |
|-----------|---------------|----------------|
| Country hub | Commercial/transactional | Cost table, process steps, direct-answer block |
| City page | Commercial/local | City-specific risk and logistics details |
| FAQ page | Informational | FAQ schema, direct answer, short_answer field |
| Guide | Informational | Long-form depth, internal links to hubs |
| Blog | Informational | Article schema, author attribution |
| Embassy contacts | Navigational | Structured contact data |
| Bringing ashes home | Commercial | Country-specific cremation/ashes rules |
| Cremation transfer | Commercial | Cremation availability status, costs |

## Lead Generation Integration

- Every country hub and city page must have a visible enquiry form or CTA above the fold
- CTA copy: specific and outcome-focused ("Get a repatriation quote within 2 hours") not generic ("Contact us")
- Phone number must be visible on mobile without scrolling on all commercial-intent pages
