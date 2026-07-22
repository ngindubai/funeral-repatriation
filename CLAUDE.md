# CLAUDE.md -- Repatriate Service

> Single source of truth for the autonomous build routine and any AI assistant working on this project. Read this in full at the start of every run. Read MEMORY.md and BUILD-PLAN.md alongside it.

---

## THE 4 LOAD-BEARING RULES

1. **Simplest solution first.** Always implement the simplest thing that could work. Do not add abstractions or flexibility that were not explicitly requested.
2. **Don't touch unrelated code.** If a file or function is not directly part of the current task, do not modify it, even if you think it could be improved.
3. **Flag uncertainty by halting, not guessing.** Running autonomously, if a regulatory fact cannot be sourced from a named dated source, mark it for later rather than inventing it, and if the build itself is ambiguous, stop and post the halt message rather than guess. Confidence without certainty causes damage on a YMYL site.
4. **A batch of up to 4 blocks per run.** Build up to 4 units (each unit = 25 routes or one 5-article blog batch), floor 1, each through the full quality gate. Commit the whole batch ONCE, report, and stop. (Changed 5 June 2026 from one block per run, to fit the 15-run routine cap.) **Throughput target (added 5 July 2026): 100 new pages/day across two runs, so 50 pages/run (2 blocks of 25). Ceiling stays 4 blocks (100 pages) when capacity allows; floor 1 clean block. Quality always gates volume: never ship a thin or duplicate page to hit the number.**

---

## AUTONOMY -- HOW THIS PROJECT RUNS NOW

**This project is built by a scheduled cloud routine with no human watching. There is no approval step.** The old "HTML preview then wait for Gareth to approve" model is retired. The working loop is:

1. Read CLAUDE.md, BUILD-PLAN.md, MEMORY.md, ERRORS.md.
2. Determine the next batch of up to 4 blocks from BUILD-PLAN.md.
3. Build each block through the full quality gate, advancing the build pointer after each.
4. If QA passes cleanly on the blocks built, commit the whole batch to master once and push. Deploy is automatic.
5. Post the live links to the Slack channel as a record of what shipped.
6. Stop.

**The Slack link post is a record, not a gate.** Nothing waits on it. It exists so a bad batch can be caught after the fact. The safety control on this auto-deploying site is the QA gate in step 3, which must pass before any commit. If QA fails on a block, do not commit that block: build as many of the 4 as pass cleanly (minimum 1), commit those, and note the shortfall in Slack. If nothing passes, post the halt message and end.

There is no "wait for go". There is no "stop and wait for approval". Each scheduled run picks up the next unbuilt blocks and ships them as one batch.

---

## EM DASH BAN -- ABSOLUTE, NO EXCEPTIONS

**Never use em dashes (-- or the em dash character) anywhere, ever.** This applies to:
- All site content (route pages, country guides, blog articles, FAQs)
- All internal documents (CLAUDE.md, BUILD-PLAN.md, MEMORY.md)
- All Slack messages and chat responses

Use commas, full stops, colons, brackets, or restructure the sentence instead. There are no circumstances under which an em dash is acceptable.

---

## THE PROJECT

- **Site:** repatriationfuneral.com (live, on Hostinger)
- **Final domain:** repatriateservice.com (not yet live)
- **Type:** Programmatic SEO lead-generation site for funeral repatriation
- **Goal:** Capture enquiries from British and Irish families who need to bring a loved one home after a death abroad
- **Audience:** Bereaved families in distress, searching immediately after a death. Needs calm, authoritative, compassionate tone
- **Stack:**
  - Hugo v0.160.1-extended (static site generator)
  - Python 3.11 (route/content generators at repo root)
  - GitHub Actions (auto-build, force-push to live branch, Hostinger pulls)
  - Hostinger (hosting)
- **Repository:** https://github.com/ngindubai/funeral-repatriation (private)
- **Production branch:** master (NOT main: master triggers the deploy, main does not)
- **WhatsApp:** +44 7703 577246
- **Enquiry form endpoint:** formsubmit.co/ajax/garethsomers@outlook.com

---

## ABOUT THE USER

- **Name:** Gareth
- **Role:** Founder, Repatriate Service
- **Technical level:** Non-technical. Does not read code.
- When reporting to Slack, write in plain English: what was built, what is live, what is next, with clickable live links.

---

## DEPLOY PIPELINE

```
Push to master
   |
GitHub Actions (build-and-publish.yml) triggers automatically
   |
Hugo --gc --minify builds site/public/
   |
Built HTML is force-pushed to the `live` branch
   |
Hostinger Git integration pulls `live` into /public_html/
   |
Live on repatriationfuneral.com (within ~60 seconds)
```

### Critical deploy rules

- **build-and-publish.yml is the live pipeline.** It builds Hugo and force-pushes to the `live` branch, which Hostinger pulls into /public_html/. Do not disable it. The `live` branch is load-bearing.
- **deploy.yml (FTP) is DISABLED** (2 June 2026). It is a manual-only no-op stub. Do not re-enable it with a push trigger: it fought with Hostinger's own Git pull into the same folder.
- **server-dir: /public_html/** is the correct Hostinger path. Never change it.
- **buildFuture = true** is set in hugo.toml. Keep it. Author all content with a safely past date so nothing is skipped (see E012).
- **The .github/workflows/ files cannot be edited via the MCP connector** (GitHub returns 403). Provide the complete file for manual paste if one ever needs changing.
- **Never repoint the deploy workflow trigger.** master deploys, main does not. Never commit to main.
- **Race condition warning:** Multiple concurrent deploys clobber each other. This is exactly why a run commits its whole batch ONCE: one push per run, let it finish, never overlapping pushes. Build up to 4 blocks, then push them together in a single commit so there is one deploy per run.
- **Deploy speed:** pages are live within ~60 seconds of the push to master.

---

## CONTENT RULES -- NON-NEGOTIABLE

1. **No safety guarantees.** Never write "we guarantee" or "100% safe" or "risk-free".
2. **Named, dated sources for every regulatory claim.** FCDO guidance, Home Office, official embassy contacts only. If a fact cannot be sourced, do not state it.
3. **Calm, authoritative, compassionate tone.** The reader has just lost someone. Do not use sales language.
4. **No em dashes. Ever. Anywhere. See EM DASH BAN above.**
5. **No banned vocabulary:** delve, meticulous, comprehensive, tailored, navigate, leverage, seamless, robust, vital, crucial, utilize, intricate, paramount, pivotal, embark, foster, elevate, unleash, unlock, harness, streamline, holistic, realm, landscape (figurative), testament, moreover, furthermore, groundbreaking, transformative, synergy, reimagine, bustling, nestled, nuanced, illuminate, encompasses, proactive, ubiquitous, quintessential. **AI-tell phrases also banned (added 5 July 2026):** additionally, in conclusion, it is worth noting, it is important to note, when it comes to, in today's fast-paced world, navigate the complexities, a testament to, plays a crucial role, plays a vital role, in the realm of, tapestry, underscore, myriad, plethora, dive into, ever-evolving, cutting-edge, game-changer, at the end of the day, rest assured, look no further, "whether you are a X or a Y".
6. **Vary sentence rhythm.** Avoid AI-pattern writing: lists of three, symmetrical sentence pairs, over-use of "not only...but also".
7. **Use correct author persona.** See AUTHOR PERSONAS section. Never use Gareth's name.
8. **British English throughout.** -ise not -ize. Organise, recognise, specialise.
9. **No prices.** Never state costs or price ranges, not even "from X" or "prices start at". Direct to the contact form.
10. **YMYL standard.** Death, legal, and consular content. Wrong information causes real harm. Every factual claim must be source-able.

---

## SEO RULES -- NON-NEGOTIABLE

- Unique title and description per page.
- Title: lead with primary keyword, under 60 characters.
- Description: answer the urgent question in the first 100 characters, under 155 characters, end with a CTA (Contact us 24/7, Call us now).
- One H1 per page containing the primary keyword.
- Target keyword in first 100 words, one H2, meta description.
- Internal links: route page links to origin country hub + destination country hub + relevant guides + at least 2 sideways routes.
- FAQ schema from faqs: frontmatter on all route and country pages.
- Service schema on all route pages.
- No duplicate content. Check the target folder for an existing slug before building.

---

## CANONICAL SEO, HUMANISATION AND FRESHNESS CONSTANTS (added 5 July 2026)

Durable rules distilled from the July 2026 upgrade work. Full detail and status in `docs/seo-upgrade-log.md`; the build routine that applies them is `docs/build-routine.md`. These bind every future run.

**Title and description**
- Route and country-hub titles carry NO ` | Repatriate Service` suffix (it pushed titles past 60 characters). Home and top-level pages keep it.
- Do not use one fixed title or description skeleton across pages. Rotate several genuine shapes and openings, so pages at scale do not share an identifiable pattern.

**Schema**
- Exactly one Organization entity per page, from `_default/baseof.html`. Never add a second route-level Organization.
- FAQ schema answer text MUST match the visible answer text word for word (build each answer once, use in both). No boilerplate schema answers.
- No FAQPage schema on country hubs (removed 2 July 2026; Google restricts FAQ rich results to gov/health).
- Service schema on every route page. Schema author is the Organization; visible bylines, where a template shows one, are one of the four personas, never a fabricated title, never Gareth.
- Organization is a service-area business: `areaServed` and `knowsAbout` set, no invented postal address, no invented reviews.
- Canonical is auto self-referencing from baseof; never add a canonical override in front matter.

**Content and information gain**
- Every page must state at least one specific, sourced, page-unique fact a competitor lacks (local emergency number, named registration authority, jurisdiction rule, corridor-specific transfer method, document time, timeline). A page that cannot clear this bar is thin: enrich it or set `noindex: true`, do not publish it thin.
- No prices anywhere, not even a range or "from X"; give qualitative "what affects the cost" wording and direct to the contact form.
- Never display the internal P1/P2/P3 build-tier codes in visible content.
- Never set a distressing hero image (gravestones, coffin, grief, deathbed) in front matter; use a calm image from `site/static/images/`.

**Freshness (YMYL honesty)**
- Do not present a fabricated "updated this month" date. The auto `now.Format` stamps are being replaced by a single `site.Params.lastReviewed` bumped only when a real regulatory review runs (see `CONTENT-REFRESH-SPEC.md`). Never claim a review that did not happen.

**Canonical facts**
- FCDO 24-hour emergency line: `+44 (0)20 7008 5000` (verify against gov.uk before changing anywhere; it appears in thousands of pages).
- WhatsApp: `+44 7703 577246`. Enquiry endpoint: `formsubmit.co/ajax/garethsomers@outlook.com`.

**Deploy safety**
- CI does not yet run the QA scripts before publishing. Until a QA job is added to `build-and-publish.yml` (needs a manual paste; the API returns 403 on workflow files), the inline QA gate in the routine is the only backstop. It must pass before any commit.

---

## LINK AND SLUG INTEGRITY (added 22 July 2026, after a Semrush audit found 1,474 broken internal links and 1,008 schema errors)

These rules exist because a whole class of 404s and schema faults built cleanly, passed the old QA, and only showed up in a live crawl. Every rule below is load-bearing. Root causes and the exact fixes are in `docs/semrush-fix-log.md`.

**Rule S1: every content file MUST carry an explicit `slug:` field.**
Hugo's `:slug` permalink token, when `slug` is absent from front matter, falls back to a slug derived from the page TITLE, not the filename. A guide filed as `death-abroad-venezuela.md` with no `slug` therefore went live at `/guides/what-to-do-when-someone-dies-in-venezuela-a-guide-for-uk-families/` while every internal link pointed at `/guides/death-abroad-venezuela/`, a hard 404. Five guides and nine blog posts were lost this way. The slug must equal the intended URL path. Never rely on filename or title derivation. The generator sets `slug:` on every page; the QA gate rejects any content file missing it.

**Rule S2: the canonical hub slug is the country directory name, which equals the data map key.** `site/data/countries_repatriation.json` is keyed by that slug. Every entry MUST have `slug` set equal to its key. 192 of 238 entries had `slug: null`, so any template reading `$c.slug` emitted `/repatriation-from-/` (empty). Keep `slug` populated for every country. When iterating the data, use the key, or `$c.slug` only after confirming it is filled.

**Rule S3: never hardcode an internal hub or guide link from a raw slug parameter.** Route front matter carries non-canonical identifiers (`origin_slug: "united-states"` while the hub is `usa`; `dest_key: "us"`). Building `/repatriation-from-{{ .Params.origin_slug }}/` produced 249 broken links plus the matching 4xx pages. Instead resolve the target through `site.GetPage` on the content path (`/countries/<key>`) and emit the resolved page's `.RelPermalink`. Guard every such link with `site.GetPage` so a missing or mismatched target is dropped, never served as a 404. Known origin aliases map in `routes/single.html` (`united-states` to `usa`, `united-kingdom` to `uk`, `united-arab-emirates` to `uae`, `gambia` to `the-gambia`, `cabo-verde` to `cape-verde`, `congo` to `republic-of-congo`, `democratic-republic-of-the-congo` to `democratic-republic-of-congo`, `vatican-city` to `holy-see`). Palestine has no hub, so its link is correctly suppressed.

**Rule S4: when a page slug changes, fix every inbound link in the same change.** Nine blog posts were renamed to better slugs but 31 articles still linked the old paths, all 404. If a slug must change, grep the whole repo for the old path and repoint every reference. Prefer never renaming a live, indexed slug.

**Rule S5: schema must validate.** No `reviewedBy` on `Article`: validators report it as `NOT_RECOGNIZED` (this alone caused 1,008 errors). Article schema carries `author` and `publisher` only. Any new schema block must be checked against a validator before it ships.

**Rule S6: titles stay unique and under 60 characters.** Programmatic single pages (route, country hub, guide, embassy, city, blog, ashes, cremation) carry NO ` | Repatriate Service` suffix. Only the home page, section list pages, and top-level pages keep it. Resolve the country name from the data map, never from a front-matter field that may be empty: embassy pages had no `country_name`, so every title rendered `British Embassy in : ...`, 184 identical titles. A page title that cannot be made unique from real data is a content bug, not a template default.

**Rule S7: the QA gate MUST build the site and crawl internal links before any commit.** Front-matter checks alone do not catch these faults, because the broken pages built without error. After Hugo builds, walk `public/`, collect every internal `href`, and assert each resolves to a built file (`<path>/index.html` or the file itself). Zero unresolved internal links is a hard gate. This is the single check that would have caught all of the above. `docs/semrush-fix-log.md` carries a reference link-crawl script.

**Rule S8: content files must be UTF-8.** 67 files carry stray Windows-1252 bytes (smart quotes, en and em dashes) that render as the replacement character on the live page and break stricter Hugo builds. The generator writes UTF-8 only; the QA gate rejects any file that is not valid UTF-8. (This also enforces the em dash ban at the byte level.)

**Known non-defect: `wa.me` "broken external link" warnings.** Semrush reports the WhatsApp click-to-chat links (about 9,720 of them) as broken because `wa.me` returns HTTP 429 to the Semrush crawler. The links work for real users. This is a crawler false positive, not a site fault. Do not try to "fix" it by removing or rewriting the WhatsApp links.

---

## AUTHOR PERSONAS -- NON-NEGOTIABLE

Never use Gareth's name as author. Use one of the personas below.

| Persona | Name | Title | Use for |
|---|---|---|---|
| The Senior Coordinator | James Whitfield | Senior Repatriation Coordinator, Repatriate Service | Route guides, process explainers, timeline articles, documentation guides |
| The Consular Specialist | Dr. Amara Osei | International Consular Affairs Specialist, Repatriate Service | Embassy contacts, FCDO guidance, legal and regulatory content, post-mortem procedures |
| The Family Adviser | Claire Sutton | Bereavement and Repatriation Adviser, Repatriate Service | Family guidance, what to do first, emotional support content, FAQ pages |
| The Logistics Lead | Thomas Anand | International Logistics Coordinator, Repatriate Service | Air cargo, airline procedures, island transfers, cargo terminal guidance |

---

## QUALITY GATE -- EVERY PAGE, EVERY BLOCK

No page ships without passing all 6 steps. This gate runs fully inline on every block in the batch. There is no human preview.

1. **Research** -- real regulations from `data/countries_repatriation.json` and named dated FCDO/embassy sources, plus web search for current detail. No invented facts. If web search is unavailable and a claim cannot be sourced from the data files, halt.
2. **Write** -- load workforce/the-wordsmith.md for voice rules before writing.
3. **Rotate templates** -- assign template_variant A/B/C/D/E. No two consecutive pages use the same variant.
4. **Humanise** -- apply workforce/the-humaniser.md rules. Remove all AI-pattern phrases.
5. **QA scan** -- run qa_routes.py and the SEO/title/schema checks. Zero em dashes, zero banned vocab, no prices, no safety guarantees, FAQ schema present, Service schema present, internal links present (origin hub + destination hub + 2 sideways routes). **If any check fails on a block, do not commit that block. Build as many of the batch as pass cleanly (minimum 1); if none pass, post the halt message and end.**
6. **Commit the whole batch to master once, push, report.** Run the gate on each block first, then commit all built blocks in a single commit. Deploy is automatic. Post the live links to Slack as a record. Then stop.

---

## BATCH COMPLETION -- LIVE LINK RECORD

After every committed batch, output a live link list covering every page in the batch. Links must be clickable markdown hyperlinks, never bare URLs (Gareth reads them on mobile). This is a record of what shipped, posted after the push, not a gate that pauses anything.

Format:

**Chunks [N-M] / Batches [N] -- [topic] -- [N] pages live**

- [Title of page 1](https://www.repatriationfuneral.com/routes/[slug-1]/)
- [Title of page 2](https://www.repatriationfuneral.com/routes/[slug-2]/)

Use /routes/[slug]/ for route pages, /blog/[slug]/ for blog articles, /repatriation-from-[country]/ for country hubs. Deploy is automatic; pages are live within ~60 seconds of commit.

---

## TEMPLATE VARIANTS

Five variants (A-E) exist for route pages and country hubs. Rotate them across every block so no two consecutive pages share a layout. Assign via template_variant: frontmatter field.

- **A:** Hero + direct answer box + timeline steps + FAQ + form
- **B:** Hero + overview narrative + destination section + FAQ + crosslinks + form
- **C:** Hero + helpline strip + step-by-step + consular box + FAQ + form
- **D:** Hero + quick answer sidebar + overview + timeline + crosslinks + FAQ + form
- **E:** Hero + emergency strip + overview + steps + destination + FAQ + form

All variants use site/layouts/routes/single.html as the base template. The variant field controls section ordering and emphasis via Hugo conditionals.

---

## THE ROUTE MATRIX IS THE GROWTH ENGINE

The site's growth comes from the origin to destination route matrix: 197 countries to 197 countries, 38,612 pages, built in four tiers (A inbound to UK and Ireland, B diaspora corridors, C regional, D long-tail completion). The full tier breakdown, order, and chunk ledger live in BUILD-PLAN.md. The data exists in `data/countries_repatriation.json`, `data/countries-197.json`, and `data/keyword_matrix.json`. Build up to 4 blocks of 25 routes per run, rotating templates A to E, committed once. This is the default work of every run until the matrix is complete.

---

## DIRECTORY STRUCTURE

```
funeral-repatriation/
  site/content/
    countries/         # 238 country hubs
    guides/            # 238 country guides
    routes/            # Route pair pages (70 live, 38,612 target). Slug: {origin}-to-{destination}.md
    blog/              # 239+ articles
    bringing-ashes-home/
    cremation-transfer/
    embassy-contacts/
  site/layouts/        # Hugo templates (routes/single.html holds the A-E variants)
  site/static/         # CSS, JS, images
  site/data/           # JSON consumed by Hugo at build time
  data/                # Source JSON for generators (countries_repatriation.json, countries-197.json, keyword_matrix.json)
  workforce/           # Worker soul files
  generate_routes.py   # Route generator
  qa_routes.py         # QA gate
  CLAUDE.md            # THIS FILE
  BUILD-PLAN.md        # What to build next + chunk ledger
  MEMORY.md            # Decision log
  ERRORS.md            # Failed approaches
```

---

## RUN PROTOCOL (autonomous)

1. Read CLAUDE.md, BUILD-PLAN.md, MEMORY.md, ERRORS.md.
2. From BUILD-PLAN.md, identify the next batch of up to 4 blocks (the next route chunks by default; a blog batch only where the next route chunk is already committed). Floor is 1 block.
3. Check the target folder (site/content/routes/ or site/content/blog/) for the slugs about to be built. Skip a block whose slugs already exist; skip the whole run only if nothing is left to build (no unbuilt chunk and no blog batch due). Do NOT skip just because a build ran earlier today; this routine runs twice a day on purpose.
4. Build each block in the batch through the full quality gate, advancing the build pointer after each.
5. If QA passes: commit the whole batch to master in one commit, with BUILD-PLAN.md and MEMORY.md updated in the same commit. Push once. Deploy is automatic.
6. Post the live link list to Slack as a record.
7. Stop. One batch (up to 4 blocks) per run.

---

## PERMANENT FACTS

- Domain: repatriationfuneral.com (Hostinger). Final domain: repatriateservice.com.
- Production branch is master. Never commit to main. Never repoint the deploy trigger.
- Deploy: push to master triggers build-and-publish.yml, which builds Hugo and force-pushes to the `live` branch; Hostinger pulls `live` into /public_html/. server-dir /public_html/ confirmed correct.
- The old FTP deploy.yml is disabled (no-op stub). Do not re-enable it.
- Slugs: lowercase, hyphen-separated, no underscores. Route slug format: {origin}-to-{destination}.
- Python generators at repo root. Hugo content in site/content/. site/public/ is gitignored, never commit build output.
- Every push to master auto-deploys within ~60 seconds. One push per run (the whole batch committed once) so concurrent deploys never clobber each other.
- buildFuture = true in hugo.toml. Keep it. Author content with a safely past date.
- .github/workflows/ files cannot be edited via MCP connector (403).
- No layout: field in route page frontmatter. Hugo auto-selects routes/single.html.
- Never use Gareth's real name as author. No em dashes anywhere. No prices on any page. British English throughout.
- The routine is autonomous: build a batch of up to 4 blocks, QA each, commit once, report, stop. No approval step, no wait-for-go. Bulk-generation without the quality gate is banned. See AUTONOMY section.

---

## WHAT TO DO WHEN STUCK (autonomous)

1. Re-read this file and BUILD-PLAN.md.
2. Read MEMORY.md for prior decisions and ERRORS.md for prior failures.
3. If still ambiguous, do not guess: stop and post the halt message to the Slack channel describing the ambiguity. Build nothing this run.

---

*Last updated: 5 June 2026. Autonomous build routine. Route matrix is the growth engine. Batch builds of up to 4 blocks per run, 2 runs/day, to fit the 15-run routine cap.*
