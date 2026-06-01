# BUILD-PLAN.md -- Repatriate Service

> Session log and task tracker. Read at the start of every session.
> The 7-engine system is the build framework. CLAUDE.md is the operating law.

---

## CURRENT STATUS -- 1 June 2026

**Route pages live:** 70
**Blog articles live:** 112 (all at full content -- stubs fixed 1 Jun 2026)
**Country hubs:** 238
**Guides:** 238 (one per country)
**Bringing ashes home pages:** 238
**Cremation transfer pages:** 238
**Embassy contact pages:** 238
**City pages:** 220
**Total indexable pages (approx):** 1,400+
**GSC known pages:** ~2,740
**GSC indexed:** 1,880
**GSC not indexed:** 859
**Target route pages:** 30,000+
**Engines complete:** 1, 2 (32 origins), 4, 5, 6, 7
**Engines pending:** 3 (blog batch scripts), 2 further expansion

---

## COMPLETED

- [x] Engine 7: CLAUDE.md, AGENTS.md, workforce/ installed
- [x] Engine 5: qa_routes.py, check_titles.py, check_schema.py, seo_pass.py
- [x] Engine 2: site/data/route_data/ with 32 origins
- [x] Engine 1: generate_routes.py upgraded
- [x] Engine 4: rebuild_link_graph.py, diagnose_links.py installed
- [x] Template rotation: all 70 route pages have A-E variants
- [x] Turn A: 25 route pages
- [x] Turn C: 23 route pages
- [x] Turn D+: 22 further route pages
- [x] Total route pages: 70
- [x] GSC canonical fix: baseURL changed to www (1 Jun 2026)
- [x] GEO/LLM 4-phase implementation complete (1 Jun 2026)
- [x] 10 thin blog stubs expanded to full articles (1 Jun 2026): brazil guide, south africa guide, uae guide, canada guide, connecting flights ashes, first 24 hours checklist, choosing funeral director, airline cargo booking, post-mortem delays, name mismatch
- [x] Country hub audit: israel, singapore, pakistan, japan all confirmed with full content (1 Jun 2026)
- [x] SEO link audit: all upward links to country hubs and guides confirmed valid (1 Jun 2026)
- [x] Known issue logged: sideways links to reverse routes (uk-to-{country}) will 404 until those pages are built

---

## KNOWN ISSUES

- **Reverse route 404s:** Every route page has a sideways link to `/routes/united-kingdom-to-{country}/` and `/routes/ireland-to-{country}/`. These pages do not exist yet. They will 404 until we build UK-as-origin and Ireland-as-origin route pages. This is a future Turn E/F task.
- **859 pages not indexed in GSC:** Requires a full GSC 'not indexed' reasons audit. Stub pages now fixed. Remaining causes likely include thin city pages, paginated list pages, or pages Google hasn't yet crawled since recent pushes.

---

## NEXT TASKS -- IN PRIORITY ORDER

### Priority 1: Engine 3 -- blog batch factory
Build generate_blog_batch1.py through generate_blog_batch5.py.
Modelled on pet-transport repo batch system.
Content: topical authority articles around repatriation, what to do guides, country-specific deep dives.
112 articles live. Target: 500+.

### Priority 2: GSC not-indexed audit
Export the 859 not-indexed URLs from GSC and categorise by reason.
Fix the most impactful category first.
Likely categories: thin content, crawled-not-indexed, soft 404, noindex.

### Priority 3: Turn E -- next 50 route pages
Current 32 origins x 2 destinations = 64 possible corridors. Only 70 pages exist (some corridors already have both directions).
Identify which corridors are still missing and fill them.
Then add new origins for Turn E expansion.

### Priority 4: Engine 2 further expansion
Add to site/data/route_data/ to enable more corridors.
Needed: poland, czech-republic, hungary, austria, croatia, bulgaria, romania, bahrain, qatar, saudi-arabia, malaysia, china, hong-kong, south-korea, bangladesh, nepal

### Priority 5: Reverse route pages (uk-to-{country}, ireland-to-{country})
Building UK-as-origin and Ireland-as-origin pages would fix the sideways link 404s and significantly expand the route silo. These require a new destination key in the data layer.

---

## ROUTE DATA ORIGINS (32 total)

australia, brazil, canada, cyprus, egypt, france, germany, ghana, greece, india, indonesia, israel, italy, japan, jordan, kenya, mexico, morocco, new-zealand, nigeria, pakistan, philippines, portugal, singapore, south-africa, spain, sri-lanka, thailand, turkey, uae, usa, vietnam

---

## SCALE ROADMAP

| Batch | Pages | Cumulative |
|---|---|---|
| Turn A | 25 | 25 |
| Turn C | 23 | 48 |
| Turn D+ | 22 | 70 |
| Turn E | 50 | 120 |
| Turn F | 100 | 220 |
| ... | ... | ... |
| Target | 30,000+ | 30,000+ |

---

## ERRORS ENCOUNTERED (summary)

| Error | Status |
|---|---|
| E001: layout: frontmatter | Fixed. Never add layout: field. |
| E002: Wrong server-dir | Fixed. Always /public_html/ |
| E003: Stale sync-state | Documented. Prevention: keep state file. |
| E004: YAML paste duplication | Documented. Always select-all before paste. |
| E005: MCP 403 on workflow files | Documented. Gareth must paste workflow manually. |
| E006: .md file in site/data/ | Fixed. Deleted README.md from route_data/. |
| E007: baseURL missing www | Fixed. Changed to https://www.repatriationfuneral.com/ |

---

*Last updated: 1 June 2026*
