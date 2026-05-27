# CLAUDE.md — Repatriate Service

> Single source of truth for any AI assistant working on this project. Read this in full at the start of every session. Attach MEMORY.md and BUILD-PLAN.md alongside this file.

---

## THE 4 LOAD-BEARING RULES

1. **Ask, don't assume.** If anything is unclear, ask before writing a single line. Never make silent assumptions about intent, architecture, or requirements.
2. **Simplest solution first.** Always implement the simplest thing that could work. Do not add abstractions or flexibility that were not explicitly requested.
3. **Don't touch unrelated code.** If a file or function is not directly part of the current task, do not modify it, even if you think it could be improved.
4. **Flag uncertainty explicitly.** If you are not confident about an approach or technical detail, say so before proceeding. Confidence without certainty causes damage.

---

## EM DASH BAN — ABSOLUTE, NO EXCEPTIONS

**Never use em dashes (— or –) anywhere, ever.** This applies to:
- All site content (route pages, country guides, blog articles, FAQs)
- All internal documents (CLAUDE.md, BUILD-PLAN.md, MEMORY.md)
- All chat responses from Claude to Gareth

Use commas, full stops, colons, brackets, or restructure the sentence instead. There are no circumstances under which an em dash is acceptable.

---

## THE PROJECT

- **Site:** repatriationfuneral.com (live, on Hostinger)
- **Final domain:** repatriateservice.com (not yet live)
- **Type:** Programmatic SEO lead-generation site for funeral repatriation
- **Goal:** Capture enquiries from British families who need to bring a loved one home after a death abroad
- **Audience:** Bereaved families in distress, searching immediately after a death — needs calm, authoritative, compassionate tone
- **Stack:**
  - Hugo v0.160.1-extended (static site generator)
  - Python 3.11 (route/content generators at repo root)
  - GitHub Actions (auto-build + incremental FTP deploy)
  - Hostinger (hosting, FTP deploy)
- **Repository:** https://github.com/ngindubai/funeral-repatriation (private)
- **WhatsApp:** +44 7703 577246
- **Enquiry form endpoint:** formsubmit.co/ajax/garethsomers@outlook.com

---

## ABOUT THE USER

- **Name:** Gareth
- **Role:** Founder, Repatriate Service
- **Technical level:** Non-technical. Does not read code. Does not know git commands by heart.
- **What this means for you:**
  - Use plain English. No jargon without explanation.
  - For any manual task Gareth has to do (in GitHub, in Hostinger, in the Claude app), give step-by-step instructions. Number every step.
  - Never say "just run X" without showing the exact command and explaining what it does.
  - If something fails, diagnose it yourself before asking Gareth to do anything.
  - When you finish a task, summarise in plain English: what changed, what is live, what is next.
  - **When providing code or file content for manual editing, always paste the COMPLETE file so Gareth can select-all and replace.**

---

## DEPLOY PIPELINE

```
Push/merge to master
   |
GitHub Actions triggers automatically
   |
Hugo --gc --minify builds site/public/
   |
FTP Deploy Action checks .ftp-deploy-sync-state.json on Hostinger
   |
Only NEW or CHANGED files are uploaded (seconds, not hours)
   |
Live on repatriationfuneral.com
```

### Critical deploy rules

- **server-dir: /public_html/** — this is the correct Hostinger path. Never change it.
- **Never set dangerous-clean-slate: true** in the workflow.
- **Never delete .ftp-deploy-sync-state.json from Hostinger** unless diagnosing a known sync problem.
- **The .github/workflows/deploy.yml file cannot be edited via the MCP connector** (GitHub returns 403 for workflow files). Always provide the complete file and ask Gareth to paste it via the GitHub web editor.
- **Race condition warning:** Multiple concurrent deploys clobber each other. Push one commit, let it finish, then push the next.
- **Deploy speed:** Single file change: 24-33 seconds. 25 new route pages: 1-2 minutes.

---

## CONTENT RULES — NON-NEGOTIABLE

1. **No safety guarantees.** Never write "we guarantee" or "100% safe" or "risk-free".
2. **Named, dated sources for every regulatory claim.** FCDO guidance, Home Office, official embassy contacts only.
3. **Calm, authoritative, compassionate tone.** The reader has just lost someone. Do not use sales language.
4. **No em dashes. Ever. Anywhere. See EM DASH BAN above.**
5. **No banned vocabulary:** delve, meticulous, comprehensive, tailored, navigate, leverage, seamless, robust, vital, crucial, utilize, intricate, paramount, pivotal, embark, foster, elevate, unleash, unlock, harness, streamline, holistic, realm, landscape (figurative), testament, moreover, furthermore, groundbreaking, transformative, synergy, reimagine, bustling, nestled, nuanced, illuminate, encompasses, proactive, ubiquitous, quintessential.
6. **Vary sentence rhythm.** Avoid AI-pattern writing: lists of three, symmetrical sentence pairs, over-use of "not only...but also".
7. **Use correct author persona.** See AUTHOR PERSONAS section.
8. **British English throughout.** -ise not -ize. Organise, recognise, specialise.
9. **No prices.** Never state costs or price ranges. Direct to contact form.
10. **YMYL standard.** Death, legal, and consular content. Wrong information causes real harm. Every factual claim must be source-able.

---

## SEO RULES — NON-NEGOTIABLE

- Unique title and description per page.
- Title: lead with primary keyword, under 60 characters.
- Description: answer the urgent question in first 100 characters, under 155 characters, end with a CTA (Contact us 24/7, Call us now, etc.).
- One H1 per page containing primary keyword.
- Target keyword in first 100 words, one H2, meta description.
- Internal links: route page links to origin country hub + destination country hub + relevant guides + 2 sideways routes.
- FAQ schema from faqs: frontmatter on all route and country pages.
- Service schema on all route pages.
- No duplicate content.

---

## AUTHOR PERSONAS — NON-NEGOTIABLE

Never use Gareth's name as author. Use one of the personas below.

| Persona | Name | Title | Use for |
|---|---|---|---|
| The Senior Coordinator | James Whitfield | Senior Repatriation Coordinator, Repatriate Service | Route guides, process explainers, timeline articles, documentation guides |
| The Consular Specialist | Dr. Amara Osei | International Consular Affairs Specialist, Repatriate Service | Embassy contacts, FCDO guidance, legal and regulatory content, post-mortem procedures |
| The Family Adviser | Claire Sutton | Bereavement and Repatriation Adviser, Repatriate Service | Family guidance, what to do first, emotional support content, FAQ pages |
| The Logistics Lead | Thomas Anand | International Logistics Coordinator, Repatriate Service | Air cargo, airline procedures, island transfers, cargo terminal guidance |

---

## QUALITY GATE — EVERY PAGE, EVERY BATCH

No page ships without passing all 7 steps:

1. **Research** — real regulations from data files and named FCDO/embassy sources. No invented facts.
2. **Write** — load workforce/the-wordsmith.md for voice rules before writing.
3. **Rotate templates** — assign template_variant A/B/C/D/E. No two consecutive pages use the same variant.
4. **Humanise** — apply workforce/the-humaniser.md rules. Remove all AI-pattern phrases.
5. **QA scan** — run qa_routes.py. Zero errors before proceeding.
6. **HTML preview** — present rendered preview to Gareth for approval.
7. **Commit to master only after approval.** Stop and wait for next "go".

---

## TEMPLATE VARIANTS

Five variants (A-E) exist for route pages and country hubs. Rotate them across every batch so no two consecutive pages share a layout. Assign via template_variant: frontmatter field.

- **A:** Hero + direct answer box + timeline steps + FAQ + form
- **B:** Hero + overview narrative + destination section + FAQ + crosslinks + form
- **C:** Hero + helpline strip + step-by-step + consular box + FAQ + form
- **D:** Hero + quick answer sidebar + overview + timeline + crosslinks + FAQ + form
- **E:** Hero + emergency strip + overview + steps + destination + FAQ + form

All variants use site/layouts/routes/single.html as the base template. The variant field controls section ordering and emphasis via Hugo conditionals.

---

## THE 7-ENGINE BUILD SYSTEM

### Engine 1 — Combinatorial route generator
Generates origin x destination pages from structured JSON data. Target: 30,000+ route pairs.
Files: generate_routes.py, assemble_routes.py
Status: v1 generator exists (thin). Full version pending Engine 2 data.

### Engine 2 — Structured data layer
Per-country and per-route JSON: embassy contacts, timeline, key documents, airlines, special rules.
Files: site/data/countries_repatriation.json, site/data/route_data/*.json
Status: countries_repatriation.json exists (shallow). Route data files pending.

### Engine 3 — Blog factory
Batch blog article generator producing topical authority content.
Files: generate_blog_batch*.py
Status: 150 articles live. Batch system pending Engine 7 operating system.

### Engine 4 — Internal link graph
Rebuilds interlink web so every route links to origin hub, destination guide, and sideways routes.
Files: rebuild_link_graph.py
Status: Pending build.

### Engine 5 — QA and SEO quality gate
Automated checks before anything ships.
Files: qa_routes.py, check_titles.py, check_schema.py, seo_pass.py
Status: qa_routes.py exists (basic). Full suite pending.

### Engine 6 — Incremental deploy pipeline
Push to master, GitHub Actions, Hugo build, FTP sync to Hostinger.
Files: .github/workflows/deploy.yml
Status: WORKING. Confirmed 27 May 2026.

### Engine 7 — Operating system
CLAUDE.md + AGENTS.md + workforce souls + cascading build plan as law.
Files: CLAUDE.md, AGENTS.md, workforce/, BUILD-PLAN.md, MEMORY.md, ERRORS.md
Status: THIS INSTALL (27 May 2026).

---

## DIRECTORY STRUCTURE

```
funeral-repatriation/
+-- site/content/          # All page content
|   +-- countries/         # 238 country hubs
|   +-- guides/            # 26 country guides
|   +-- routes/            # Route pair pages (25 live, 30,000+ target)
|   +-- blog/              # 150+ articles
|   +-- bringing-ashes-home/
|   +-- cremation-transfer/
|   +-- embassy-contacts/
+-- site/layouts/          # Hugo templates
+-- site/static/           # CSS, JS, images
+-- site/data/             # Source JSON for generators
+-- workforce/             # Worker soul files (this install)
+-- generate_routes.py     # Route generator (v1, upgrade pending)
+-- qa_routes.py           # QA gate (basic, upgrade pending)
+-- CLAUDE.md              # THIS FILE
+-- AGENTS.md              # Agent roles
+-- BUILD-PLAN.md          # Session log and remaining tasks
+-- MEMORY.md              # Decision log
+-- ERRORS.md              # Failed approaches
```

---

## SESSION PROTOCOLS

### "go" or "next block"
1. Read BUILD-PLAN.md and MEMORY.md.
2. Write content through the full 7-step quality gate.
3. Present HTML preview, wait for approval.
4. Commit to master, provide live URL and Actions link.
5. Stop and wait.

### "session end" or "wrap up"
1. Update BUILD-PLAN.md and MEMORY.md.
2. Commit to master.
3. Summarise: what was built, what is live, what is next.

### Every content task
1. Load the-wordsmith.md before writing.
2. Load the-humaniser.md before finalising.
3. Load the-auditor.md to QA before committing.

---

## PERMANENT FACTS

- Domain: repatriationfuneral.com (Hostinger). Final domain: repatriateservice.com.
- Hostinger FTP server-dir: /public_html/ (confirmed correct 27 May 2026).
- Slugs: lowercase, hyphen-separated, no underscores.
- Python generators at repo root.
- Hugo content in site/content/.
- site/public/ is gitignored. Never commit build output.
- Every push to master auto-deploys via incremental FTP.
- Do NOT delete .ftp-deploy-sync-state.json from Hostinger.
- FTP credentials in GitHub Secrets only. Never in chat or commits.
- .github/workflows/deploy.yml cannot be edited via MCP connector (403 error). Gareth must paste via GitHub web editor.
- No layout: field in route page frontmatter. Hugo auto-selects routes/single.html.
- Never use Gareth's real name as author on published content.
- No em dashes anywhere, ever.
- No prices on any page.
- British English throughout.

---

## WHAT TO DO WHEN STUCK

1. Re-read this file.
2. Read MEMORY.md for prior decisions.
3. Read ERRORS.md for prior failures.
4. Ask Gareth one specific question.

---

*Last updated: 27 May 2026*
