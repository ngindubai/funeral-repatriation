# SEO Build Plan, 2 July 2026

Execution plan derived from `seo-audit-2026-07-02.html`, which is derived from the SEO and Search Brief dated 29 June 2026.

**Execution model:** Sonnet, unless a step is marked **OPUS REQUIRED**.
**Deploy target (updated 2 July 2026, authorised by Gareth):** every block is pushed to `master`, which is the live production branch. Pushing to `master` triggers `build-and-publish.yml`, which force-pushes to `live`, and Hostinger serves it within about 60 seconds. So every push is a live deploy of a YMYL site. Work is prepared on `claude/funeral-repatriation-seo-audit-zayex7` and fast-forwarded to `master` per block. Still never commit to `main`. Deploy discipline from CLAUDE.md holds: one push (one deploy) per block, and only push a block that builds clean and passes `check_schema.py`; do not deploy a block whose own gate fails.
**House rules that still apply to every step:** no em dashes anywhere, no banned vocabulary, British English, no prices on route pages, no invented facts on a YMYL topic. Run the QA gate before any commit.

## Standard checks (run after every code wave)

```
cd /home/user/funeral-repatriation
hugo --source site --gc --minify            # must build with no errors
python3 qa_routes.py                          # route QA gate, exit 0 required
python3 check_schema.py                        # schema check
python3 check_titles.py --routes-only          # title/description lengths
```

If any gate fails, fix before committing. Commit each wave once, with a clear message.

---

## WAVE 1, safe mechanical wins (Sonnet)

One deploy covers F1, F5, F6, F8, F9. All template-only, low risk.

### Step 1.1, F1: answer block first on all variants
- File: `site/layouts/routes/single.html`.
- In variants B, D and E, move the `answer-brief-section` block so it is the first `<section>` after the hero (before the helpline strip in B and D, before the overview in E). Variants A and C already do this; use them as the pattern.
- Keep the ordering of the sections beneath the answer block as they are per variant, so layout variety is preserved below the fold.
- Acceptance: build succeeds; view one page of each variant (B, D, E) in the built output and confirm the "Quick answer" / "Key facts" block renders directly under the hero.

### Step 1.2, F5: remove duplicate Organization schema
- File: `site/layouts/routes/single.html`, lines defining the second `Organization` JSON-LD inside the `schema` block (the thinner one, around the `contactOption:"TollFree"` block).
- Delete that block only. The site-wide Organization schema in `site/layouts/_default/baseof.html` stays and is the single source.
- Acceptance: `check_schema.py` passes; a built route page contains exactly one `"@type":"Organization"` block (the one from baseof).

### Step 1.3, F6: og:image and twitter card
- File: `site/layouts/_default/baseof.html`, in `<head>`.
- Add, after the existing og tags: a default `og:image` (absolute URL), `og:image:width`/`og:image:height`, and `twitter:card` = `summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image`.
- Image asset: use an existing calm brand image from `site/static/images/` if one is suitable (for example the cargo-terminal image already used in the route hero), or ask Gareth for one. Never a distressing photo. If no suitable asset exists, use the site logo/favicon as a fallback and note it for later replacement.
- Acceptance: built home page and a route page both output `og:image` and `twitter:card` tags with an absolute URL.

### Step 1.4, F8: shorten rendered title
- Files: `site/layouts/routes/single.html` (title block) and `site/layouts/countries/country-hub.html`.
- Drop the ` | Repatriate Service` suffix from route and country-hub `<title>` output (or shorten to ` | Repatriate`). Keep the suffix on the home page and top-level pages.
- Acceptance: `check_titles.py --routes-only` shows rendered titles inside 60 characters where the field itself was already short.

### Step 1.5, F9: trim over-length descriptions
- 33 route files have `description` over 155 characters. List them, then trim each to end with the call to action inside 155 characters. Do not change meaning.
- Find them:
```
python3 - <<'PY'
import glob,re
for f in sorted(glob.glob("site/content/routes/*.md")):
    if "_index" in f: continue
    fm=open(f,encoding="utf-8").read().split("---",2)[1]
    m=re.search(r'^description:\s*"?(.+?)"?\s*$',fm,re.M)
    if m and len(m.group(1))>155: print(len(m.group(1)),f)
PY
```
- Acceptance: `check_titles.py` reports zero descriptions over 155.

### Commit Wave 1
- Message example: `seo: answer-first layouts, dedupe org schema, og:image, title/desc length (F1,F5,F6,F8,F9)`.

---

## WAVE 2, structured-data honesty and silo (Sonnet, with one Opus sub-step)

### Step 2.1, F2: FAQ schema must match visible answers (country hubs)
- File: `site/layouts/countries/country-hub.html`.
- The visible FAQ (around lines 259 to 277) already builds real answers for questions 0 to 3 from country data. The FAQ JSON-LD (around line 53) writes the same boilerplate for every answer.
- Change the JSON-LD so each `acceptedAnswer.text` reproduces the same text the visible block shows for that index. The cleanest approach: build each answer string once (as a Hugo variable per index) and use it in both the visible HTML and the JSON-LD, so they cannot drift again.
- For question indexes with no real answer (index 4 and beyond, currently the "contact our team" fallback): either omit those questions from the JSON-LD entirely, or supply a real answer (see 2.1a).
- **Do not emit price figures into route-page schema.** On hubs, prices are a separate open decision (see Wave 4, F13); do not add new price output here, only mirror what already renders.
- Acceptance: for a built hub page, each FAQ question's schema answer text equals its visible answer text; `check_schema.py` passes.

### Step 2.1a **OPUS REQUIRED**: write real answers for trailing hub FAQ questions
- Only needed if Gareth wants the trailing questions kept in the markup rather than dropped.
- Writing new YMYL answers needs Opus: they must be factually correct, source-able against `data/countries_repatriation.json` or named FCDO/embassy sources, and free of banned words and em dashes.
- If Opus is not being used this run, take the safe path instead: drop the trailing (index 4+) questions from the JSON-LD so no unbacked answer is marked up. This still resolves the mismatch risk.

### Step 2.2, F7: link hubs down to route pages
- File: `site/layouts/countries/country-hub.html`.
- Add a "Routes from {country}" section that links to route pages whose `origin_slug` matches this country. Use `site.GetPage` or a filtered `where` over the routes section so only existing pages are linked (follow the existing link-filter pattern in `routes/single.html` that guards against 404s).
- Keep it scoped: link the main corridors for that origin plus a link to `/routes/`. Do not list every possible destination.
- Acceptance: a built hub page shows working links into `/routes/...`; no link points to a non-existent page (`hugo` build has no broken-ref warnings for these).

### Commit Wave 2
- Message example: `seo: FAQ schema matches visible answers on hubs, hub-to-route links (F2,F7)`.

---

## WAVE 3, trust and content quality (OPUS REQUIRED)

Both steps here need Opus. Do not run them on Sonnet.

### Step 3.1 **OPUS REQUIRED**, F3: author identity (E-E-A-T)
- This starts with a decision, so surface the two options to Gareth before building:
  - Option A: stand up real author bio pages (a new `/authors/` or `/about/team/` section) for the four personas, describing genuine experience only, then wire named Person schema (`name`, `jobTitle`, `url` pointing to the bio) into route, hub and blog templates. Assign a persona per content type per the CLAUDE.md persona table.
  - Option B: keep Organization as author, and instead strengthen the existing "Reviewed by the editorial team" credit and the methodology page.
- Do not invent qualifications. If real experience cannot be described truthfully, prefer Option B.
- If Option A is approved: add the bio pages, then add author frontmatter or template mapping so each page resolves to one persona deterministically, then add Person schema (upgrade blog author from Organization to Person, replace the generic "Senior Repatriation Consultant" on hubs).
- Acceptance: chosen option built and passing `check_schema.py`; if Option A, each Person in schema has a `url` to a real bio page.

### Step 3.2 **OPUS REQUIRED**, F4: thicken the thin overview prose
- Target: the 695 routes with `overview_body` under 40 words first, then the rest under 60.
- The prose is generated from the route generators (`generate_r*.py`) into frontmatter, so fix at the source: improve the sentence templates so output is grammatical and fuller (aim for 60 to 110 words), then re-generate or backfill the affected files.
- Hard constraints: no invented facts (source from `data/countries_repatriation.json` and named FCDO/embassy sources), varied sentence rhythm, no banned words, no em dashes, no prices on routes.
- Work in batches through the QA gate. Do not attempt all 2,467 in one commit; the deploy pipeline expects one push per run and small batches are safer for a YMYL site.
- Find the shortest first:
```
python3 - <<'PY'
import glob,re
rows=[]
for f in glob.glob("site/content/routes/*.md"):
    if "_index" in f: continue
    fm=open(f,encoding="utf-8").read().split("---",2)[1]
    m=re.search(r'^overview_body:\s*"(.+?)"\s*$',fm,re.M)
    if m:
        w=len(m.group(1).split())
        if w<40: rows.append((w,f))
for w,f in sorted(rows): print(w,f)
PY
```
- Acceptance per batch: QA gate green; spot-read 5 rewritten pages for grammar and factual sourcing.

### Commit Wave 3
- Commit F3 and each F4 batch separately, each with its own clear message.

---

## WAVE 4, decision and governance (no build until decided)

### Step 4.1, F13 **DECISION NEEDED from Gareth**: prices on country hubs
- The 239 hubs render price ranges (hero stat, answer brief, cost banner, cost section, two FAQ answers, ashes cards). This conflicts with CLAUDE.md content rule 9 (no prices).
- Do not change anything until Gareth decides. Present the two paths:
  - Keep prices (treat hubs as a deliberate exception; update CLAUDE.md to record the exception so it is not flagged again).
  - Remove prices (replace each price element with a qualitative "what affects the cost" explanation plus a link to the contact form; then the no-prices rule holds site-wide).
- If removal is approved, it is a Sonnet job across `site/layouts/countries/country-hub.html` and any hub data references. QA gate must pass.

### Step 4.2, F11: record the do-not
- Add a line to `MEMORY.md`: do not buy brand mentions or use PBNs for GEO; Google flags it and it does not work on AI Overviews (per 29 June brief, Story 3).

### Step 4.3, F10: note on llms.txt
- No code change. Keep `llms.txt` and `llms-full.txt`. Do not add AI-specific schema, content chunking, or further llms-specific files; Google does not read them for AI ranking (Story 2). Record this in `MEMORY.md` so future runs do not re-open it.

### Step 4.4, F12 **OPUS REQUIRED for the fact loop**: quarterly refresh spec
- Write a short spec (a new doc, for example `CONTENT-REFRESH-SPEC.md`) for a quarterly pass that re-checks dated regulatory facts (FCDO numbers, embassy status, documentation timings) against named sources and flags changes for confirmation. Edits are confirmed by Opus or a person, never applied blind, because the content is YMYL.

---

## Monitoring (operational, no code), from the brief

- Track positions for the named queries in Story 1: "repatriation of remains" and "body repatriation from UAE", plus core UK-inbound corridors.
- The GSC page indexing report is lagging (no data since 11 June per Story 6). Use the URL Inspection tool for individual pages until the bulk report resolves; do not trust the bulk report for anything launched after 11 June.

---

## Summary of model requirements

| Step | Item | Model |
|---|---|---|
| 1.1 to 1.5 | Answer-first, dedupe schema, og:image, titles, descriptions | Sonnet |
| 2.1 | FAQ schema mirrors visible answers | Sonnet |
| 2.1a | New YMYL answers for trailing FAQ questions | **Opus** (or drop questions on Sonnet) |
| 2.2 | Hub to route links | Sonnet |
| 3.1 | Author identity / E-E-A-T | **Opus** |
| 3.2 | Thicken thin overview prose | **Opus** |
| 4.1 | Prices on hubs | Decision (Gareth); Sonnet to action |
| 4.2, 4.3 | Governance notes in MEMORY.md | Sonnet |
| 4.4 | Quarterly refresh spec + fact loop | **Opus** |

---

# Execution session, 2 July 2026: block order and additions

This session runs the plan in thematic blocks in this order: **Block 1 Discoverability**, **Block 2 Trust and schema**, **Block 3 Answer-first content**, then **Block 4 On-page tidy and governance**. The findings above are re-grouped into these blocks below. Nothing in the findings changes; only the running order and two additions (llms.txt per the session rules, and a cross-cutting prices decision).

Session rules in force: ask before every decision (no default assumed); stop and request a model switch at every Opus-tagged or Opus-designed step; extend this plan in place; keep the changelog at the foot of this file; treat llms.txt as a live deliverable regardless of what the audit said about it; push every completed block to `master` for live deploy (see Deploy target above).

## Block 1: Discoverability
- **1B.1 llms.txt upgrade (NEW this session, Sonnet OK after prices decision).** The site already ships `site/static/llms.txt` and `site/static/llms-full.txt`. Upgrade, do not skip. Verify every linked page exists (all core pages confirmed present on 2 July), reflect the route matrix and country-hub coverage, and resolve the price content per the cross-cutting prices decision below. Decision raised: prices in llms.txt (see Prices decision). Do not assert a fresh verification date that has not actually been re-verified on a YMYL site.
- **1B.2 F7 hub to route links (Sonnet OK after scope decision).** Add a "Routes from {country}" block to `site/layouts/countries/country-hub.html`, filtered so only built route pages render. Decision raised: link scope (see F7 scope decision).

## Block 2: Trust and schema
- **2B.1 F5 dedupe Organization schema (Sonnet OK).**
- **2B.2 F2 FAQ schema mirrors visible answers on hubs (Sonnet OK; 2.1a new answers is Opus advised).**
- **2B.3 F3 author identity / E-E-A-T (OPUS ADVISED, and a business decision).** Raises: option A real author bio pages with Person schema, or option B keep Organization as author. Also raises the Organization-modelling decision: no postal address is set, so is the business a service-area Organization (no address) or is there a real address to add. Both are decisions for Gareth.

## Block 2 sub-plan (added 2 July after code mapping)

Reality found during Block 2: hubs use variant dispatch (variant A inline in `country-hub.html`; B/C/D/E via partials). The FAQ JSON-LD is emitted once from `country-hub.html`'s `define "schema"` for all variants, but the visible FAQ is implemented five ways. Prices reach hubs from three places: the variant-A cost sections, the `cost_guide` data in `data/countries_repatriation.json`, and free-text figures inside individual hub `_index.md` frontmatter. Only 13 hubs render a price today (bolivia, egypt, germany, india, indonesia, kyrgyzstan, malaysia, morocco, nepal, philippines, south-africa, spain, turkey).

### 2B.2a F13 hub price removal (qualitative-only; Sonnet OK; decided)
Steps:
1. `country-hub.html` inline template: remove the price outputs and replace with qualitative wording plus a contact route. Specific spots: hero "Typical cost" stat (line ~86), answer-brief cost clause and cost stat (lines ~122, ~132), process-step `typical_cost_gbp` clause (line ~151), the whole cost banner + breakdown table section (lines ~193-219) becomes a "What affects the cost" factor list (post-mortem, island or remote transfer, distance, weekend delay) with no figures, FAQ answer 1 cost line (line ~269) and FAQ answer 3 ashes figure (line ~271), and the ashes cost card figures (line ~318, keep the CTA).
2. Individual hub `_index.md` frontmatter: sweep for figures in `short_answer`, `direct_answer_intro`, `direct_answer_points`, and any faq text; rewrite qualitatively. Start with the 13 listed above; grep the rest for `GBP`, `£`, and thousands figures.
3. `data/countries_repatriation.json` `cost_guide`: leave the data in place; once the template stops rendering it, it is dormant. Not deleted, so it can feed a future qualitative "what affects cost" note if wanted.
Decision raised: none beyond the prices decision already made (qualitative only).

### 2B.2b F2 hub FAQ schema (decision required)
The FAQ JSON-LD answers are identical boilerplate and do not match the visible answers. Options:
- Option 1: make the schema answers mirror the visible answers. Most faithful to audit F2, but must reconcile five visible implementations and keep them price-free.
- Option 2: emit schema only for the questions that have real, data-backed, price-free answers (timeline, documents, ashes without a figure); drop the rest from the markup.
- Option 3: remove the FAQPage schema from hubs entirely. Google restricted FAQ rich results to government and health sites in 2023, so hubs gain little from it; removal ends the mismatch risk at effectively zero SEO cost.
Recommendation: Option 3 (lowest risk, near-zero cost), or Option 2 if we want to keep some FAQ markup. Awaiting decision.

## Block 3: Answer-first content
- **3B.1 F1 answer block to top of variants B, D, E (Sonnet OK).**
- **3B.2 F4 thicken and grammar-fix thin overview prose (OPUS ADVISED).** Opus writes the rubric and hand-checks a sample before any bulk pass.

### Block 3: Answer-first content (in progress)

**3B.1 F1 answer block to top of route variants** (done, verified; commit pending, batched with F4)
- File: `site/layouts/routes/single.html`.
- Corrected the plan's assumption after reading the live code: variant A and C already led with the answer; variant D already placed the answer above the overview (helpline, then answer, then dest, then overview), so D needed no change; only variants B and E rendered the overview narrative before the answer. B and E shared a byte-identical "overview then answer" sequence, so one swap (replace all) moved the answer block above the overview in both.
- Result: all five variants now render the `answer-brief-section` before the overview narrative. Verified on a sample route of each variant that the answer block's DOM position precedes "The process" overview. In B and D the helpline strip (a short contact bar, roughly 30 words) still sits directly under the hero, so the answer remains well inside the first 200 words.
- Why: AI Overview and featured-snippet capture favour the direct answer high in the document (brief Story 2).

## Block 4: On-page tidy and governance
- **4B.1 F8 shorten rendered title (Sonnet OK).**
- **4B.2 F9 trim 33 over-length descriptions (Sonnet OK).**
- **4B.3 F13 prices on hubs (DECISION, then Sonnet to action).** Folded into the cross-cutting Prices decision below.
- **4B.4 F11 record PBN do-not, F10 llms note superseded by session rule 5, F12 quarterly refresh spec (Opus advised).**

## Cross-cutting decision: prices
Route pages carry no prices (compliant with CLAUDE.md rule 9). Country hubs and `llms.txt` both publish GBP price ranges. This must be resolved once, because it affects Block 1 (llms.txt), Block 2 (any schema), and Block 4 (F13 hubs). Options: (a) strip all figures site-wide and direct to the contact form; (b) keep figures as a deliberate exception and record it in CLAUDE.md; (c) keep qualitative "what affects the cost" wording with no figures. Awaiting Gareth's decision before editing llms.txt or hubs.

## F7 scope decision
Options: (a) link every built route page whose origin is this country, filtered by existence so it self-scales as the matrix grows; (b) a curated set of top corridors plus a link to the routes index; (c) a full collapsible list of all destinations. Awaiting Gareth's decision.

---

## Changes made and why

Format per entry: finding ID, files and lines touched, what changed, why. Written so it can be lifted into the routine build prompts later.

### Block 1: Discoverability (built and verified 2 July 2026; commit pending)

**1B.1 llms.txt and llms-full.txt upgrade** (session rule 5; supersedes audit F10)
- Files: `site/static/llms.txt`, `site/static/llms-full.txt`.
- llms.txt: removed the two GBP price figures (Spain, Thailand) under the qualitative-only prices decision; removed two em dashes (UAE line, Sensitivity note) under the em dash ban; added a "Route Guides (country to country)" section linking /routes/.
- llms-full.txt: removed all GBP cost figures (the P1/P2 country lines and the "typical cost range (GBP)" phrase); replaced the em dash separators with colons throughout; corrected the stale "26 countries" framing to describe full country coverage plus route corridors; added a "Country-to-country route guides" section linking /routes/. Left the "verified May 2026" line unchanged, since it was not actually re-verified.
- Why: other AI systems read these files and they drive real traffic (session rule 5). Figures removed to match the site-wide qualitative-only decision and the route-page no-prices rule. Em dashes removed under the absolute ban.

**1B.2 F7 hub-to-route internal links**
- Files: new `site/layouts/partials/countries/routes-from.html`; partial call added in `site/layouts/countries/country-hub.html` (variant A inline path) and in `site/layouts/partials/countries/country-b.html`, `country-c.html`, `country-d.html`, `country-e.html` (immediately before the enquiry form).
- What: every country hub now renders a "Repatriation routes from {country}" block linking each built route page whose origin is that country, sorted by destination.
- Matching approach: normalise `origin_name` (lowercase, strip a leading "the ") and compare to the hub name, rather than joining on slug. The hub slug and route `origin_slug` diverge (hub `usa` but route `origin_slug` `united-states` and `usa`; both captured; USA hub shows 113 destinations). Only `site.RegularPages` are linked, so no link can 404 and the block self-scales as the matrix grows.
- Coverage: 189 of 238 hubs render a block; the remainder have no built outbound routes yet.
- Discovered during build: country hubs use variant dispatch. Variant A renders inline in `country-hub.html`; variants B/C/D/E render via the `partials/countries/country-{b,c,d,e}.html` partials. That is why the block was factored into one shared partial called from all five, rather than edited into a single template.
- Why: strengthens the silo and gives crawlers a path into the 2,467 route pages (audit F7; brief Story 5 silo structure, Story 6 indexing lag).

### Block 2: Trust and schema (in progress)

**2B.1 F5 dedupe Organization schema** (done, verified; commit pending, batched with the rest of Block 2)
- File: `site/layouts/routes/single.html`.
- Removed the standalone route-level Organization JSON-LD block (the one carrying `contactOption: TollFree`). The site-wide Organization schema in `_default/baseof.html` is retained as the single source.
- Verified: a built route page now has 4 JSON-LD blocks with top-level types Organization (from baseof), BreadcrumbList, Service, FAQPage; the `TollFree` block is gone; all parse as valid JSON. The Organization nested as the Service `provider` is unchanged and correct.
- Why: one Organization entity per page (audit F5).

**2B.2 F2 remove hub FAQPage schema** (decided: option 3; done, verified)
- File: `site/layouts/countries/country-hub.html`, `define "schema"` block.
- Discovered during mapping: the mismatched FAQPage schema only ever rendered for variant D hubs (47 of 238), gated by `{{ if eq $variant "D" }}`. Variant D's own visible FAQ (in `partials/countries/country-d.html`) is itself boilerplate for most of its questions, so schema and visible were both weak; removing the schema removes the mismatch risk entirely rather than trying to reconcile two weak sources.
- Verified: 0 of 238 built hub pages carry `"@type":"FAQPage"` after the change; `check_schema.py` passes 0 errors across all 2,467 route files (unaffected, hubs only).

**2B.2a F13 hub price removal** (qualitative-only, decided; done, verified)
- File: `site/layouts/countries/country-hub.html` (the only template with price code; the four B/C/D/E partials never rendered prices).
- Removed: hero "Typical cost" stat (replaced with a "24/7 support" stat); the cost clause and cost stat in the answer-brief section (replaced with qualitative timeline/availability wording); the `typical_cost_gbp` clause in the process-step cards; the entire cost banner and cost-breakdown table (replaced with a price-free "what the cost depends on" factor list plus a link to contact); the FAQ answer 1 cost figure and FAQ answer 3 ashes-return cost figure (both replaced with qualitative wording and a contact link); the ashes cost card figures (replaced with a case-specific-estimate line).
- Also stopped rendering `cost_guide.cost_notes` and `cost_guide.insurance_note` as free text, because those fields carry embedded GBP figures for some countries (confirmed in data: spain, thailand, turkey, portugal, india, egypt, philippines) and could not be shown safely without checking every country's text by hand. Replaced with static, price-free copy plus a link to `/methodology/`.
- Investigated and ruled out: swept all 238 hub `_index.md` files for `GBP`, `£`, and thousands-separator figures; the initial 34-file hit list was a false positive from a loose regex matching population and altitude figures (for example "population of around 80,000", "elevations between 2,400 and 4,500 metres"), not prices. Re-checked with a currency-anchored pattern (`GBP[0-9]`, `£[0-9]`, `$[0-9]`): zero hub frontmatter files contain a genuine price figure. No frontmatter edits were needed.
- Verified: rebuilt and scanned all 238 built hub pages for `£[0-9]`, `GBP [0-9]`, `$[0-9]{2,}`; zero matches (down from 13 hubs rendering a price before this fix). `check_schema.py` and a banned-word scan of the edited template both pass clean.
- Left in place, not deleted: the `cost_guide` data in `data/countries_repatriation.json` is now dormant (unrendered) rather than removed, so it can feed a future qualitative note if wanted.

**Also fixed while in these files (found during Block 2, not a separate audit finding):** four em dashes reaching live output were removed: a `—` escape baked into every hub's meta description (`country-hub.html`), an `&mdash;` in the cost table (removed along with the table itself), and a `—` in the WhatsApp helpline label on variant B and C hubs (96 hubs). Two em dashes in code comments (non-rendering) were also cleaned for consistency. This is the absolute em dash ban applied opportunistically to files already open for Block 2; a full site-wide em dash sweep beyond these files is not yet done and is not currently scheduled as a separate step (worth a mention if a governance pass is wanted later).

**2B.3 F3 author identity / E-E-A-T** (decided: Option B, Organization as author, service-area Organization, no reviews; Opus session; done, verified)
- Decision recorded: the four personas (James Whitfield, Dr Amara Osei, Claire Sutton, Thomas Anand) are fictional bylines defined in CLAUDE.md, there is no postal address anywhere in the site, and there are no reviews. Gareth chose Option B: keep the Organization as the author and publisher everywhere, model the business as a service-area Organization with no invented address, and add no review or rating markup. Inventing named-expert credentials, an address, or reviews on a YMYL site was rejected as an inauthentic-signal risk (audit F3 caveat; brief Story 3).
- Files and changes:
  - `_default/baseof.html`: added `areaServed` ("United Kingdom", "Ireland", "Worldwide") and `knowsAbout` (six repatriation topics) to the site-wide Organization schema. No `PostalAddress` added (service-area model). This is the honest entity-strengthening for GEO entity authority (brief Story 2).
  - `countries/country-hub.html`: variant E Article schema `author` changed from a fabricated `{"@type":"Person","name":"Senior Repatriation Consultant"}` to the Organization, and a `reviewedBy` Organization added.
  - `partials/countries/country-e.html`: the visible byline "Senior Repatriation Consultant" (a generic fabricated title, not one of the mandated personas) replaced with "By the Repatriate Service editorial team" in both the hero byline and the author-credit block. This removes the only visible fabricated author on the hubs.
  - `blog/single.html`: added a `reviewedBy` Organization to the Article schema (author and publisher were already Organization).
- Investigated and left alone: the blog `author` frontmatter (the four personas on 137 posts, plus "Senior Repatriation Consultant" on 127) is dormant. It is not rendered visibly and not used in schema (the blog schema hardcodes the Organization). So there is no visible fabricated persona byline on the blog to reconcile, and no conflict with CLAUDE.md rule 7 (the persona frontmatter is untouched). Editing 264 files of dormant metadata would be needless churn, so it was left as is.
- Verified: home Organization renders `areaServed` and `knowsAbout`; variant E hub Article renders Organization author plus `reviewedBy` and contains zero `Person` types; blog Article renders `reviewedBy`; all JSON-LD parses; `check_schema.py` passes 0 errors; edited templates are free of banned words and em dashes; 0 built hub pages still show "Senior Repatriation Consultant".
- Note for a future decision (not blocking): if the site ever wants named-expert E-E-A-T, that needs real people with truthful bios, not the current fictional personas. Until then, Organization authorship is the honest ceiling.

### Block 2 complete
F5, F2, F13 (folded in), and F3 all done and verified. F5+F2+F13 deployed to master at commit 0f844c6. F3 pending deploy (this commit).

**Pre-existing QA state noted (not caused by Block 1):** `qa_routes.py` reports 36 route files failing, and `check_titles.py` matches: descriptions over 155 characters, the banned word "vital" in 6 files, and 2 titles at 61 characters. Block 1 changed only templates and static files (no route `.md` touched), and `check_schema.py` passes with zero errors. These 36 map to Block 4 F9 (descriptions) plus a new banned-word sub-item; see Block 4.
