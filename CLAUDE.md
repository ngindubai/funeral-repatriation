# CLAUDE.md -- Repatriate Service

> Single source of truth for the autonomous build routine and any AI assistant working on this project. Read this in full at the start of every run. Read MEMORY.md and BUILD-PLAN.md alongside it.

---

## THE 4 LOAD-BEARING RULES

1. **Simplest solution first.** Always implement the simplest thing that could work. Do not add abstractions or flexibility that were not explicitly requested.
2. **Don't touch unrelated code.** If a file or function is not directly part of the current task, do not modify it, even if you think it could be improved.
3. **Flag uncertainty by halting, not guessing.** Running autonomously, if a regulatory fact cannot be sourced from a named dated source, mark it for later rather than inventing it, and if the build itself is ambiguous, stop and post the halt message rather than guess. Confidence without certainty causes damage on a YMYL site.
4. **One block per run.** Build exactly one unit (25 routes or one 5-article blog batch), then commit, report, and stop.

---

## AUTONOMY -- HOW THIS PROJECT RUNS NOW

**This project is built by a scheduled cloud routine with no human watching. There is no approval step.** The old "HTML preview then wait for Gareth to approve" model is retired. The working loop is:

1. Read CLAUDE.md, BUILD-PLAN.md, MEMORY.md, ERRORS.md.
2. Determine the one next block from BUILD-PLAN.md.
3. Build it through the full quality gate.
4. If QA passes cleanly, commit to master and push. Deploy is automatic.
5. Post the live links to the Slack channel as a record of what shipped.
6. Stop.

**The Slack link post is a record, not a gate.** Nothing waits on it. It exists so a bad batch can be caught after the fact. The safety control on this auto-deploying site is the QA gate in step 3, which must pass before any commit. If QA finds any failure, do not commit: post the halt message and end.

There is no "wait for go". There is no "stop and wait for approval". Each scheduled run picks up the next unbuilt block and ships it.

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
- **Race condition warning:** Multiple concurrent deploys clobber each other. Push one commit, let it finish, then push the next. The routine builds one block per run for this reason.
- **Deploy speed:** pages are live within ~60 seconds of the push to master.

---

## CONTENT RULES -- NON-NEGOTIABLE

1. **No safety guarantees.** Never write "we guarantee" or "100% safe" or "risk-free".
2. **Named, dated sources for every regulatory claim.** FCDO guidance, Home Office, official embassy contacts only. If a fact cannot be sourced, do not state it.
3. **Calm, authoritative, compassionate tone.** The reader has just lost someone. Do not use sales language.
4. **No em dashes. Ever. Anywhere. See EM DASH BAN above.**
5. **No banned vocabulary:** delve, meticulous, comprehensive, tailored, navigate, leverage, seamless, robust, vital, crucial, utilize, intricate, paramount, pivotal, embark, foster, elevate, unleash, unlock, harness, streamline, holistic, realm, landscape (figurative), testament, moreover, furthermore, groundbreaking, transformative, synergy, reimagine, bustling, nestled, nuanced, illuminate, encompasses, proactive, ubiquitous, quintessential.
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

No page ships without passing all 6 steps. This gate runs fully inline. There is no human preview.

1. **Research** -- real regulations from `data/countries_repatriation.json` and named dated FCDO/embassy sources, plus web search for current detail. No invented facts. If web search is unavailable and a claim cannot be sourced from the data files, halt.
2. **Write** -- load workforce/the-wordsmith.md for voice rules before writing.
3. **Rotate templates** -- assign template_variant A/B/C/D/E. No two consecutive pages use the same variant.
4. **Humanise** -- apply workforce/the-humaniser.md rules. Remove all AI-pattern phrases.
5. **QA scan** -- run qa_routes.py and the SEO/title/schema checks. Zero em dashes, zero banned vocab, no prices, no safety guarantees, FAQ schema present, Service schema present, internal links present (origin hub + destination hub + 2 sideways routes). **If any check fails, do not commit. Post the halt message and end.**
6. **Commit to master, push, report.** Deploy is automatic. Post the live links to Slack as a record. Then stop.

---

## BATCH COMPLETION -- LIVE LINK RECORD

After every committed block, output a live link list. Links must be clickable markdown hyperlinks, never bare URLs (Gareth reads them on mobile). This is a record of what shipped, posted after the push, not a gate that pauses anything.

Format:

**Chunk [N] / Batch [N] -- [topic] -- [N] pages live**

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

The site's growth comes from the origin to destination route matrix: 197 countries to 197 countries, 38,612 pages, built in four tiers (A inbound to UK and Ireland, B diaspora corridors, C regional, D long-tail completion). The full tier breakdown, order, and chunk ledger live in BUILD-PLAN.md. The data exists in `data/countries_repatriation.json`, `data/countries-197.json`, and `data/keyword_matrix.json`. Build 25 routes per run, rotating templates A to E. This is the default work of every run until the matrix is complete.

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
2. From BUILD-PLAN.md, identify the one next block (the next route chunk by default; a blog batch only if the next route chunk is already committed).
3. Check the target folder (site/content/routes/ or site/content/blog/) for the slugs about to be built. If they already exist, this block is built: stop and post the SKIPPED message.
4. Build the block through the full quality gate.
5. If QA passes: commit to master with BUILD-PLAN.md and MEMORY.md updated in the same commit. Push. Deploy is automatic.
6. Post the live link list to Slack as a record.
7. Stop. One block per run.

---

## PERMANENT FACTS

- Domain: repatriationfuneral.com (Hostinger). Final domain: repatriateservice.com.
- Production branch is master. Never commit to main. Never repoint the deploy trigger.
- Deploy: push to master triggers build-and-publish.yml, which builds Hugo and force-pushes to the `live` branch; Hostinger pulls `live` into /public_html/. server-dir /public_html/ confirmed correct.
- The old FTP deploy.yml is disabled (no-op stub). Do not re-enable it.
- Slugs: lowercase, hyphen-separated, no underscores. Route slug format: {origin}-to-{destination}.
- Python generators at repo root. Hugo content in site/content/. site/public/ is gitignored, never commit build output.
- Every push to master auto-deploys within ~60 seconds.
- buildFuture = true in hugo.toml. Keep it. Author content with a safely past date.
- .github/workflows/ files cannot be edited via MCP connector (403).
- No layout: field in route page frontmatter. Hugo auto-selects routes/single.html.
- Never use Gareth's real name as author. No em dashes anywhere. No prices on any page. British English throughout.
- The routine is autonomous: build, QA, commit, report, stop. No approval step, no wait-for-go, no stop condition. See AUTONOMY section.

---

## WHAT TO DO WHEN STUCK (autonomous)

1. Re-read this file and BUILD-PLAN.md.
2. Read MEMORY.md for prior decisions and ERRORS.md for prior failures.
3. If still ambiguous, do not guess: stop and post the halt message to the Slack channel describing the ambiguity. Build nothing this run.

---

*Last updated: 5 June 2026. Autonomous build routine. Route matrix is the growth engine.*
