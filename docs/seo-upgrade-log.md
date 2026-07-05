# SEO Upgrade Log

> Single record of every SEO, schema, content, design, and build upgrade surfaced in the build and audit work of 2 to 4 July 2026, cross-checked against the actual repository state on 4 July 2026. Each item records the problem, the fix or recommendation, why it matters, the files touched, and current status.
>
> Sources folded in: the 2 July SEO build (findings F1 to F13, plus llms.txt and the late-caught F6), the 3 July design and conversion build (D1 to D5), the 4 July sitemap split, and the ChatGPT SEO audit triage. Duplicates are recorded once at their final resolution.
>
> Status key: **Applied** (in the repo and verified), **Partially applied** (some scope done, remainder is backlog), **Outstanding** (recommended, not built), **Closed** (decided as no-change).

---

## How status was verified

Each "Applied" claim below was re-checked against the working tree on 4 July 2026, not taken on trust from the build plans. Verification commands and their results are summarised inline. The live sitemap was also fetched from the production server to confirm deployment.

---

## Category 1: Technical SEO (canonicals, robots, sitemaps, indexation)

### 1.1 Sitemap was a single flat file
- **Problem:** one `/sitemap.xml` listing all 4,262 URLs, with no per-section split. As the route matrix grows toward 38,612 pages it approaches Google's 50,000-URL and 50MB per-file limits, and a single file gives no per-section indexation visibility in Search Console.
- **Fix applied:** replaced with a sitemap index at `/sitemap.xml` referencing nine child sitemaps (one per top-level section plus a root-pages child). Verified live: index root element is `sitemapindex`, nine children resolve HTTP 200, union is exactly 4,262 URLs with zero duplicates or losses, zero orphan files, nested country sitemaps correctly return 404.
- **Why it matters:** keeps every sitemap file small and within limits, and lets Search Console report indexation per section (routes, countries, guides, blog) instead of one lumped figure.
- **Files:** `site/hugo.toml` (output formats), `site/layouts/index.sitemapindex.xml`, `site/layouts/index.rootsitemap.xml`, `site/layouts/_default/section.sectionsitemap.xml`, `site/layouts/partials/sitemap-url.html`, `site/content/countries/_index.md` (cascade), deleted `site/layouts/sitemap.xml`.
- **Status:** Applied (commit 388c999, live).

### 1.2 Canonical tags
- **Problem:** none identified; checked as part of the audit.
- **State confirmed:** `site/layouts/_default/baseof.html` line 12 emits a self-referencing `<link rel="canonical" href="{{ .Permalink }}">` on every page. Correct.
- **Status:** Applied (baseline, already correct).

### 1.3 Robots and AI-crawler policy
- **State confirmed:** `site/static/robots.txt` allows all major AI search crawlers by name (OAI-SearchBot, ChatGPT-User, PerplexityBot, Claude-SearchBot, Google-Extended, GPTBot) plus `*`, and points to the sitemap. `baseof.html` line 14 emits `<meta name="robots" content="noindex, follow">` only when a page sets `noindex` frontmatter. Correct.
- **Status:** Applied (baseline, already correct).

### 1.4 CI has no quality gate before deploy (highest-impact outstanding item)
- **Problem:** `.github/workflows/build-and-publish.yml` runs only the Hugo build and publish to the `live` branch. It does not run `qa_routes.py`, `check_schema.py`, or `check_titles.py`. A broken page (missing schema, em dash, price, over-length title) can deploy to a live YMYL site with nothing catching it. Confirmed: no python or QA step present in the workflow.
- **Recommendation:** add a QA job that runs the three scripts and fails the build on any error before the publish step.
- **Why it matters:** the audit calls this the single highest-impact fix. It is the only automated backstop on an auto-deploying site with no human approval step.
- **Files that would need touching:** `.github/workflows/build-and-publish.yml`.
- **Status:** Outstanding. Blocker: workflow files under `.github/workflows/` cannot be edited through the MCP connector (GitHub returns 403, per CLAUDE.md), so this needs a complete file provided for manual paste by Gareth. It also makes every deploy blocking, which is the intended trade-off.

### 1.5 Thin or near-duplicate route pages not flagged for noindex
- **Problem:** the audit recommends auto-flagging thin or duplicate programmatic route pages and setting `noindex` so Google does not judge 2,468-plus near-identical pages as thin content.
- **Recommendation:** a uniqueness or thinness gate that sets `noindex` on pages below an information-gain threshold. The template already supports per-page `noindex` frontmatter and honours it in both the robots meta and the sitemap, so the mechanism exists; the detection rule does not.
- **Why it matters:** thin programmatic content at scale can drag the whole domain's quality signal down.
- **Status:** Outstanding. High risk: a too-aggressive rule could deindex pages that currently rank. Deferred for its own carefully-tested piece of work, not a quick switch.

---

## Category 2: On-page (titles, meta descriptions, headings)

### 2.1 F8: rendered titles over 60 characters
- **Problem:** route and country-hub `<title>` output carried a ` | Repatriate Service` suffix that pushed rendered titles past the ~60-character SERP truncation point.
- **Fix applied:** dropped the suffix from route and hub title blocks (kept on home and top-level pages). Measured first: bare title fields were already inside 60 chars for all but 3 routes and 5 hubs, so dropping the suffix resolved truncation for ~2,030 routes and ~233 hubs without rewriting any title text.
- **Why it matters:** truncated titles lose the keyword tail and read poorly in results.
- **Files:** `site/layouts/routes/single.html`, `site/layouts/countries/country-hub.html`.
- **Status:** Applied. Residual: 5 hub titles are extreme official country names still over 60 chars (for example Saint Helena, Ascension and Tristan da Cunha); left as a small known residual.

### 2.2 F9: descriptions over 155 characters and 36 pre-existing QA failures
- **Problem:** 33 route descriptions exceeded 155 chars; `qa_routes.py` reported 36 failing route files in total (the 33 plus 2 titles at 61 chars and 6 files using the banned word "vital" in "vital statistics office").
- **Fix applied:** trimmed the 33 descriptions to end with a call to action inside 155 chars; trimmed 2 long titles; replaced "vital statistics office" with the equally accurate "civil registration office". A regression where two trims dropped the CTA was caught by re-running `check_titles.py` and fixed.
- **Why it matters:** truncated descriptions lose the CTA; banned words are an AI-tell and a house-rule breach.
- **Files:** 36 files under `site/content/routes/`.
- **Status:** Applied. `qa_routes.py` now 0 FAIL / 2,467 PASS. Residual: 27 pre-existing lower-severity "no CTA in description" warnings remain, out of scope of this task.

### 2.3 F1: direct answer buried below the overview narrative
- **Problem:** route variants B and E rendered the overview narrative before the "Quick answer / Key facts" block, pushing the direct answer down the page.
- **Fix applied:** moved the `answer-brief-section` above the overview on variants B and E (A, C, D already led with, or placed, the answer high). All five variants now render the answer before the overview.
- **Why it matters:** AI Overviews and featured snippets favour a direct answer high in the document.
- **Files:** `site/layouts/routes/single.html`.
- **Status:** Applied.

### 2.4 F6: no Open Graph image or Twitter card
- **Problem:** the site emitted zero `og:image` and zero Twitter card tags, so shared links rendered with no image.
- **Fix applied:** added `og:image` (with width, height, site_name) and a full Twitter `summary_large_image` card, placed outside the `page-meta` block so they render on every page including routes and hubs. Verified: `baseof.html` now contains 5 matching tag lines.
- **Why it matters:** social and chat previews with an image earn more clicks; several AI surfaces read og tags.
- **Files:** `site/layouts/_default/baseof.html`. Image asset: `cargo-terminal-night-card.jpg` (640x448, 30KB).
- **Status:** Applied. Optional upgrade: a purpose-built 1200x630 branded share image can replace the single default value with no other change.

### 2.5 Template footprint: titles, descriptions, and heading skeleton are near-identical at scale (new finding)
- **Problem found during this audit:** the 2,468 route pages share a small set of templated shapes. Titles reduce to about a dozen skeletons ("{Origin} to {Dest}: Repatriation Guidance for British Families", "{Origin} to {Dest}: Funeral Repatriation Guidance", and so on). Descriptions follow a strong fixed pattern ("Someone has died in {origin}. Repatriation to the {dest} takes {N} days. {one detail}. Contact us 24/7."). The route template's H2 set is a fixed skeleton across variants (Timeline, When the body arrives in {dest}, FAQs: repatriation from {origin}, More repatriation guidance); the A to E variants rotate section order but not the heading set. `overview_body` is generated from rotating sentence frames.
- **Recommendation (for the new routine):** break the skeleton at generation time. Vary the opening construction, rotate and vary the H2 set and count per page, and anchor each page to page-specific real data (local emergency number, named registration authority, jurisdiction rule, corridor-specific transfer method) so two pages in the same variant are not the same paragraphs with the nouns swapped.
- **Why it matters:** an identifiable shared skeleton across tens of thousands of pages is the classic scaled-content pattern Google penalises, humanised prose or not.
- **Status:** Outstanding. This is the central reason the routine rewrite (Stage 2) exists.

---

## Category 3: Structured data and schema

### 3.1 F5: duplicate Organization schema on route pages
- **Problem:** route pages carried a second, thinner Organization JSON-LD block (the one with `contactOption: TollFree`) in addition to the site-wide Organization in `baseof.html`.
- **Fix applied:** removed the route-level block. The site-wide Organization is the single source. Verified: a built route page has one top-level Organization plus BreadcrumbList, Service, and FAQPage; the TollFree block is gone.
- **Why it matters:** one canonical entity per page avoids conflicting Organization signals.
- **Files:** `site/layouts/routes/single.html`.
- **Status:** Applied.

### 3.2 F2: hub FAQPage schema did not match visible answers
- **Problem:** the FAQPage JSON-LD on country hubs wrote identical boilerplate answers that did not match the visible FAQ text (and only ever rendered for variant D). Mismatched FAQ schema is a manual-action risk.
- **Fix applied (decided Option 3):** removed the FAQPage schema from hubs entirely. Verified: `country-hub.html` line 53 now carries only a comment recording the removal; 0 of 238 built hubs emit `"@type":"FAQPage"`. Route-page FAQPage schema (which does match its visible answers) is unaffected and retained.
- **Why it matters:** Google restricted FAQ rich results to government and health sites in 2023, so hubs gained little from it; removal ends the mismatch risk at near-zero SEO cost.
- **Files:** `site/layouts/countries/country-hub.html`.
- **Status:** Applied.

### 3.3 F3: E-E-A-T author identity and Organization modelling
- **Problem:** hubs carried a fabricated visible byline ("Senior Repatriation Consultant") and a matching Person in schema; the site-wide Organization had no `areaServed` or `knowsAbout`; there is no real postal address and no reviews.
- **Fix applied (decided Option B):** keep Organization as author and publisher everywhere; model the business as a service-area Organization with no invented address; add no review markup. Added `areaServed` (United Kingdom, Ireland, Worldwide) and `knowsAbout` (six repatriation topics) to the site-wide Organization. Replaced the fabricated hub Person byline and schema author with the Organization and a `reviewedBy` Organization; added `reviewedBy` to blog Article schema. Verified: `baseof.html` contains `areaServed` and `knowsAbout`; 0 built hubs show "Senior Repatriation Consultant".
- **Why it matters:** honest entity signals strengthen E-E-A-T and GEO entity authority without inventing credentials, which is an inauthentic-signal risk on a YMYL site.
- **Files:** `site/layouts/_default/baseof.html`, `site/layouts/countries/country-hub.html`, `site/layouts/partials/countries/country-e.html`, `site/layouts/blog/single.html`.
- **Status:** Applied. Outstanding future option: named-expert E-E-A-T would need real people with truthful bios, not the current fictional personas. Until then, Organization authorship is the honest ceiling. The dormant persona `author` frontmatter on 264 blog posts is unrendered and was left untouched.

### 3.4 Schema inventory (confirmed present and valid)
- **State confirmed:** templates emit Organization, Service, BreadcrumbList, FAQPage (routes only), Article, HowTo/HowToStep, ContactPoint, OpeningHoursSpecification. `check_schema.py` reports 0 errors across 2,467 route files.
- **Status:** Applied (baseline healthy).

---

## Category 4: Content quality and information gain

### 4.1 F4: thin, sometimes ungrammatical route overview prose
- **Problem:** 695 route `overview_body` fields were under 40 words, and 618 carried a grammar bug ("takes jurisdiction when the death is:").
- **Fix applied (Opus-designed rubric, then bulk):** rewrote the `overview_body` of 501 routes to an 85 to 115 word, grammatical overview using only facts already in the same file (local emergency number, registration authority, document time, jurisdiction rule, standard air-cargo flow, typical timeline). No new facts. Three sentence frames rotate by slug hash. Guardrails reject banned words, em dashes, prices, and unescaped quotes.
- **Why it matters:** thin content is a scaled-content risk; grammatical, fuller pages read as human and carry more information gain.
- **Files:** `f4_thicken_overview.py`, 501 files under `site/content/routes/`.
- **Status:** Partially applied. Result: under-40-word bodies fell from 695 to 194; grammar bug from 618 to 117. The remaining ~194 thin and ~117 grammar-bug files do not match the canonical template and were deliberately left rather than risk corrupting sourced facts. **Backlog:** those files need their own pattern analysis.

### 4.2 F13: prices published on country hubs (compliance breach)
- **Problem:** 13 hubs rendered GBP price ranges (hero stat, answer brief, cost banner, breakdown table, two FAQ answers, ashes cards), breaching CLAUDE.md content rule 9 (no prices) which route pages already follow.
- **Fix applied (decided qualitative-only):** removed every price element from `country-hub.html` and replaced with qualitative "what affects the cost" wording plus a contact link. Stopped rendering `cost_guide.cost_notes` and `cost_guide.insurance_note` (which carry embedded figures). Verified: `country-hub.html` line 194 is now a comment; 0 built hubs render a price (down from 13). The `cost_guide` data is left dormant, not deleted.
- **Why it matters:** consistent no-prices compliance site-wide, and a single conversion path (the contact form) instead of anchoring expectations to a figure.
- **Files:** `site/layouts/countries/country-hub.html`; also `site/layouts/countries/list.html` (removed a price stat on the countries index).
- **Status:** Applied.

### 4.3 llms.txt price and em-dash cleanup (F10, session rule)
- **Problem:** `llms.txt` and `llms-full.txt` carried GBP figures and em dashes, and stale "26 countries" framing.
- **Fix applied:** removed all GBP figures, replaced em dashes with colons, corrected the coverage framing, and added route-guide sections. Kept both files as live deliverables (other AI systems read them and they drive traffic), overriding the audit's original suggestion to deprioritise them.
- **Files:** `site/static/llms.txt`, `site/static/llms-full.txt`.
- **Status:** Applied.

---

## Category 5: Internal linking and site architecture

### 5.1 F7: country hubs did not link down to route pages
- **Problem:** hubs did not link into the 2,467 route pages, weakening the silo and giving crawlers no path in.
- **Fix applied:** a shared `routes-from.html` partial renders a "Repatriation routes from {country}" block on every hub variant, linking each built route whose origin is that country (matched on normalised `origin_name`, filtered to existing pages so no link 404s and it self-scales). Verified the partial exists and is wired into all five variants.
- **Why it matters:** distributes link equity into the route matrix and gives crawlers a route into pages that the indexing report was lagging on.
- **Files:** `site/layouts/partials/countries/routes-from.html`, `site/layouts/countries/country-hub.html`, `site/layouts/partials/countries/country-{b,c,d,e}.html`.
- **Status:** Applied. Coverage: 189 of 238 hubs (the rest have no built outbound routes yet).

### 5.2 D1.2: /routes/ index page was blank
- **Problem:** no `routes/list.html` existed, so `/routes/` fell back to a template that only renders body content, and the index showed a hero and nothing else. None of the 2,467 routes were listed or linked.
- **Fix applied:** built `routes/list.html`, a grouped accordion index of all routes by destination (129 groups, largest first), reusing the existing FAQ accordion markup and JS. Verified the file exists and renders a usable grouped list.
- **Why it matters:** gives users and crawlers a single navigable entry point to the whole matrix.
- **Files:** `site/layouts/routes/list.html`.
- **Status:** Applied.

### 5.3 Route hub pages (/routes/from/{origin}/, /routes/to/{destination}/)
- **Problem/recommendation (ChatGPT audit):** add ~400 intermediate hub pages to strengthen internal linking.
- **Why not (recommendation):** ~400 new pages to build, QA, and keep unique is a large thin-content surface for uncertain gain, and the new `/routes/` accordion index already provides most of the linking benefit.
- **Status:** Outstanding. Recommended skip.

---

## Category 6: Design, UX and conversion (3 July design audit)

### 6.1 D1.1: navigation invisible on light-hero pages
- **Problem:** the fixed header is transparent with white text and only turns solid-dark via a `has-hero` body class or on scroll. City, cremation-transfer, and embassy-contacts pages set `hero_image` in frontmatter without rendering a dark hero, so the header stayed transparent over a light page and the white logo and nav links vanished, leaving only the gold "Service" span.
- **Fix applied:** excluded those page types from the `has-hero` gate in `baseof.html` so the header renders solid-dark and readable. Bringing-ashes-home (which does use a real background hero) left correct.
- **Files:** `site/layouts/_default/baseof.html`.
- **Status:** Applied.

### 6.2 D1.3: empty guide-card titles and stale count
- **Problem:** `/guides/` cards rendered `{{ .Params.country_name }}`, a param no guide page has, so every card heading was empty; the grid label read a stale "26 country guides" (there are 238).
- **Fix applied:** resolve the country name from `country_key` via the shared data file, fallback to `.Title`; corrected the count to a live 238.
- **Files:** `site/layouts/guides/list.html`.
- **Status:** Applied.

### 6.3 D2.1: no visible phone number on the highest-traffic pages
- **Problem:** the homepage hero and contact page linked to WhatsApp but never printed the number `+44 7703 577246` as readable, tappable text.
- **Fix applied:** added a `tel:`-linked number line to the homepage hero and the contact page, reusing the existing helpline style.
- **Files:** `site/layouts/index.html`, `site/layouts/_default/contact.html`.
- **Status:** Applied.

### 6.4 D2.2: no persistent CTA on interior pages
- **Problem:** the enquiry form sat only at the page bottom; nothing persisted except the floating WhatsApp button.
- **Fix applied:** a shared fixed-bottom mobile CTA bar (WhatsApp plus Send Enquiry to `/contact/`), shown under 600px, with the floating WhatsApp button hidden at that breakpoint to avoid collision. Verified the partial exists and is included from `baseof.html`.
- **Why it matters:** the single highest-impact mobile conversion change in the audit.
- **Files:** `site/layouts/partials/sticky-cta.html`, `site/assets/css/main.css`, `site/layouts/_default/baseof.html`.
- **Status:** Applied.

### 6.5 D2.3 and D2.4: contact form length and trust text
- **Problem:** the contact form had 7 fields including two selects; trust and response-time text under the submit button was thin.
- **Fix applied:** trimmed the contact form to 5 fields (removed `service` and `urgency` selects); added a response-time and confidentiality line. Scoped to the contact page only (route and hub forms were already short).
- **Files:** `site/layouts/_default/contact.html`.
- **Status:** Applied.

### 6.6 D3.2 and D3.4: internal jargon and stale counts shown to users
- **Problem:** homepage and country cards displayed raw internal "P1 / P2" build-tier codes; several hardcoded counts were stale.
- **Fix applied:** removed the priority-tier badges entirely (not just relabelled, since even a friendly label exposes an implied ranking of which families' deaths are prioritised); replaced stale counts with live counts.
- **Files:** `site/layouts/countries/list.html`, `site/layouts/index.html`.
- **Status:** Applied.

### 6.7 D4.1: distressing and repeated hero images
- **Problem:** a coffin-and-flowers image was hardcoded on Contact, Privacy, and generic pages; the countries index showed a figure-among-gravestones image; the routes index and generic fallback defaulted to a couple-at-deathbed image.
- **Fix applied:** reassigned calm, previously-unused images already in the repo to Contact, the generic single template, and the countries, routes, and generic section indexes (including fixing a frontmatter override in `content/countries/_index.md`). No distressing default remains in any template or index. No new images commissioned, per decision.
- **Files:** `site/layouts/_default/contact.html`, `site/layouts/_default/single.html`, `site/layouts/countries/list.html`, `site/layouts/routes/list.html`, `site/layouts/_default/list.html`, `site/content/countries/_index.md`.
- **Status:** Applied. Known limitation accepted: route heroes stay visually similar across corridors.

### 6.8 D5.1: five hub layouts inconsistent, two missing the emergency bar
- **Problem:** variants D and E rendered no emergency helpline bar at all (the most important trust and safety element), and B, D, E rendered no orientation stats.
- **Fix applied (Option 1, Opus session):** built two shared components, a single `helpline-strip.html` (now identical on all five hubs) and a `hero-stats.html` orientation strip (added to B, D, E). Replaced variant A's leftover priority-code pill with the embassy city. The five heroes deliberately still differ in arrangement (rotation variety kept); the consistency added is in the load-bearing components.
- **Files:** `site/layouts/partials/countries/helpline-strip.html`, `hero-stats.html`, plus the five variant templates and `main.css`.
- **Status:** Applied.

### 6.9 D5.2: navigation had redundant items
- **Problem:** eight top-level nav items plus a redundant "WhatsApp us" link and "Get Help Now" button (three routes to the same two actions).
- **Fix applied:** restructured to five top-level items (Home, Country Guides, Resources dropdown with About folded in, Services, Contact) plus one WhatsApp icon-button; removed the dead `.header-cta` CSS.
- **Files:** `site/layouts/partials/header.html`, `site/assets/css/main.css`.
- **Status:** Applied.

### 6.10 D3.1: green WhatsApp button
- **Decision:** keep it green (WhatsApp brand convention). No change.
- **Status:** Closed.

---

## Category 7: Accessibility

### 7.1 D3.3: overline label contrast fails AA on light backgrounds
- **Problem:** `.label-sm` in full gold (`#D5A021`) scores 8.26:1 on dark hero backgrounds (passes) but only 2.36:1 on the white section backgrounds where most instances appear. WCAG AA needs 4.5:1 for normal text.
- **Fix applied (partial):** scoped override to `--gold-dark` on light sections, raising contrast to 3.17:1, and bumped the label font-size slightly.
- **Why it matters:** low-contrast eyebrow labels are hard to read and fail accessibility.
- **Files:** `site/assets/css/main.css`.
- **Status:** Partially applied and honestly scoped: 3.17:1 clears the large-text threshold (3:1) but not full normal-text AA (4.5:1). Reaching 4.5:1 needs abandoning the gold hue for this element or enlarging it into the large-text category. **Backlog:** a genuine full-AA decision on this element.

### 7.2 Editorial image alt text
- **Recommendation (ChatGPT audit):** review hero and content image alt text for descriptive, page-specific wording.
- **Status:** Outstanding (minor).

---

## Category 8: Performance and Core Web Vitals

### 8.1 Font loading and CWV
- **Recommendation (ChatGPT audit):** review web-font loading strategy and other Core Web Vitals inputs.
- **Why it matters:** CWV is a ranking input and affects real user experience on mobile, where bereaved users often arrive.
- **Status:** Outstanding (moderate). Not yet investigated; no specific defect confirmed in-repo yet. Note: route heroes reuse a shared image, and the social card image was deliberately kept small (30KB), which helps.

---

## Category 9: Analytics and measurement

### 9.1 Two analytics packages loaded at once
- **Problem found during this audit:** `site/hugo.toml` sets both `plausibleDomain` and `googleAnalyticsID`, and `baseof.html` loads both Plausible and GA4 (gtag) on every page.
- **Recommendation:** decide which to keep. Running both adds a second blocking script and splits measurement across two tools.
- **Why it matters:** page weight and a single source of truth for conversion tracking.
- **Files:** `site/hugo.toml`, `site/layouts/_default/baseof.html`.
- **Status:** Outstanding. Decision needed (which tool to keep).

---

## Category 10: Governance, freshness, and operational

### 10.1 F12: no honest "last reviewed" mechanism
- **Problem:** eight templates stamp `{{ now.Format "January 2006" }}`, so every page always displays the current month as its review date even when nothing was reviewed; three hardcoded "May 2026" stamps also exist. Confirmed still present: 9 `now.Format` occurrences across the hub variants, hub, guides, and route templates; `lastReviewed` param not implemented (0 references); "May 2026" still in `methodology.html` and `country-hub.html`.
- **Fix specified, not applied:** `CONTENT-REFRESH-SPEC.md` specifies replacing all of these with a single `site.Params.lastReviewed` bumped only when a real review runs, so the displayed date becomes honest.
- **Why it matters:** auto-advancing review dates on YMYL content misrepresent freshness; an honest date is the defensible posture.
- **Files that would need touching:** the 9 template locations above, `methodology.html`, `hugo.toml`.
- **Status:** Outstanding. Low-risk and self-contained; recommended as the next contained fix. Trade-off: pages will show a fixed older date instead of always-current-month until the next real review.

### 10.2 F12: quarterly regulatory-fact refresh
- **Problem:** consular numbers, embassy status, travel advisories, and treaty facts go stale and cause real harm if wrong on a YMYL site.
- **Fix applied (spec):** wrote `CONTENT-REFRESH-SPEC.md`, a quarterly plus event-triggered pass with a priority-ordered volatile-fact register (FCDO 24-hour line, embassy status, travel advisories, Hague Apostille, dormant cost data), each with its named source and repo location, and a flag-never-blind-apply workflow run on Opus or with a person.
- **Status:** Applied as a spec; first run (including the lastReviewed fix in 10.1) is Outstanding.

### 10.3 F11: paid GEO mentions and PBNs
- **Fix applied:** recorded a permanent do-not in `MEMORY.md` (no buying brand mentions on low-quality domains or PBNs to influence AI Overviews or chatbot citations).
- **Status:** Applied.

### 10.4 Site-wide em dash sweep
- **Problem:** em dashes were removed opportunistically from files already open during the SEO and design blocks (hub meta descriptions, WhatsApp labels on 96 hubs, contact form, CSS comments, llms files), but no full site-wide sweep of all content and templates has been run.
- **Why it matters:** the em dash ban is absolute; a stray dash in generated content or an untouched file would breach it.
- **Status:** Outstanding. Recommended as a governance pass (and enforceable by the CI QA gate in 1.4 once that lands).

### 10.5 Monitoring (operational, no code)
- **Note from the brief:** track positions for "repatriation of remains" and "body repatriation from UAE" plus core UK-inbound corridors; the GSC page-indexing bulk report was lagging (no data since 11 June), so use URL Inspection for pages launched after that date.
- **Status:** Operational note, no code change.

---

## Summary: category counts

| Category | Applied | Partially applied | Outstanding | Closed |
|---|---|---|---|---|
| 1. Technical SEO | 3 | 0 | 2 | 0 |
| 2. On-page (titles, meta, headings) | 4 | 0 | 1 | 0 |
| 3. Structured data and schema | 4 | 0 | 0 | 0 |
| 4. Content quality and information gain | 3 | 1 | 0 | 0 |
| 5. Internal linking and architecture | 2 | 0 | 1 | 0 |
| 6. Design, UX and conversion | 9 | 0 | 0 | 1 |
| 7. Accessibility | 0 | 1 | 1 | 0 |
| 8. Performance and CWV | 0 | 0 | 1 | 0 |
| 9. Analytics | 0 | 0 | 1 | 0 |
| 10. Governance and freshness | 3 | 0 | 3 | 0 |
| **Totals** | **28** | **3** | **10** | **1** |

### The outstanding backlog, most important first
1. **CI quality gate** before deploy (Category 1.4). Highest impact; blocked on manual workflow paste.
2. **`lastReviewed` honest-date fix** (Category 10.1). Low-risk, contained, recommended next.
3. **Break the template footprint** at generation time (Category 2.5). The core reason for the routine rewrite.
4. **Finish F4 thin-content rewrite** on the remaining ~194 files (Category 4.1).
5. **Thin-content / noindex uniqueness gate** (Category 1.5). High-risk, needs careful thresholds.
6. **Analytics consolidation** decision (Category 9.1).
7. **Full-AA label contrast** decision (Category 7.1).
8. **Performance / CWV** review (Category 8.1).
9. **Site-wide em dash sweep** (Category 10.4).
10. **Editorial image alt text** review (Category 7.2). Route hub pages (Category 5.3) recommended skipped.
