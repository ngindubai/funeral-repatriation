# BUILD-PLAN.md -- Repatriate Service

> Session log and task tracker. Read at the start of every session.
> The 7-engine system is the build framework. CLAUDE.md is the operating law.

---

## CURRENT STATUS -- 1 June 2026

**Route pages live:** 70
**Blog articles live:** 112 (not 150 -- corrected 1 Jun 2026 after direct repo count)
**Country hubs:** 238
**Bringing ashes home pages:** 238
**Cremation transfer pages:** 238
**Embassy contact pages:** 238
**City pages:** 220
**Guides:** 26
**Total indexable pages (approx):** 1,400+
**GSC known pages:** ~2,740 (includes paginated list pages, historical URLs, city sub-pages)
**GSC indexed:** 1,880
**GSC not indexed:** 859
**Target route pages:** 30,000+
**Engines complete:** 1, 2 (32 origins), 4, 5, 6, 7
**Engines pending:** 3 (blog batch scripts), 2 further expansion

---

## COMPLETED

- [x] Engine 7: CLAUDE.md, AGENTS.md, workforce/ installed
- [x] Engine 5: qa_routes.py, check_titles.py, check_schema.py, seo_pass.py
- [x] Engine 2: site/data/route_data/ with 32 origins (64 corridors)
- [x] Engine 1: generate_routes.py upgraded to read route_data, apply wordsmith voice, QA gate
- [x] Engine 4: rebuild_link_graph.py, diagnose_links.py installed
- [x] Template rotation: single.html implements all A-E variants; all pages have template_variant
- [x] Turn A: 25 route pages (manually written)
- [x] Turn C: 23 route pages
- [x] Turn D+: 22 further route pages (israel, singapore, pakistan, japan corridors)
- [x] Total route pages: 70
- [x] ERRORS.md updated with E006, E007
- [x] GSC canonical fix: baseURL changed to www (1 Jun 2026)
- [x] GEO/LLM citation upgrades: FAQPage schema, Organization schema, llms.txt, methodology page
- [x] 4-phase GEO implementation complete (1 Jun 2026)
- [x] Page count audit: corrected blog count to 112, total site ~1,400+ indexable pages (1 Jun 2026)

---

## KNOWN ISSUES

- Several blog files are very thin (under 1.5KB): repatriation-from-brazil-guide, repatriation-from-south-africa-guide, repatriation-from-uae-guide, repatriation-from-canada-guide, bringing-ashes-through-connecting-flights, first-24-hours-after-a-death-abroad-checklist, how-to-choose-a-repatriation-funeral-director, how-airline-cargo-booking-works-for-repatriation, post-mortem-delays-and-what-families-can-control, repatriation-delays-caused-by-name-mismatch. These are likely stub pages contributing to GSC 'not indexed' count.
- 859 pages not indexed in GSC -- requires audit of 'not indexed' reasons.

---

## NEXT TASKS -- IN PRIORITY ORDER

### Priority 1: Thin blog stub audit and fix
Inspect the ~10 thin blog files (under 2KB). Expand each to full content or redirect/delete.
This directly reduces the GSC 'not indexed' count.

### Priority 2: Engine 3 -- blog batch factory
Build generate_blog_batch1.py through generate_blog_batch5.py.
Modelled on pet-transport repo batch system.
Content: topical authority articles around repatriation, what to do guides, country-specific deep dives.
112 articles live. Target: 500+.

### Priority 3: Country hubs audit for new route origins
The following origins have route pages but may lack country hub pages at /repatriation-from-{country}/:
Check: israel, singapore, pakistan, japan.
Audit all 32 route origins against the country hub silo.

### Priority 4: seo_pass.py audit on all 70 route pages
Run the full Engine 5 audit on the complete route page set.
Fix any errors before next content turn.

### Priority 5: rebuild_link_graph.py --fix
Run Engine 4 with --fix to patch any missing links across all 70 pages.
Then run diagnose_links.py to confirm no orphans.

### Priority 6: Engine 2 further expansion
Add more origins to site/data/route_data/ to enable Turn E.
Current: 32 origins.
Still needed: poland, czech-republic, hungary, austria, croatia, bulgaria, romania, bahrain, qatar, saudi-arabia, malaysia, china, hong-kong, south-korea, bangladesh, nepal

### Priority 7: Turn E -- next 50 route pages
Once additional route_data files exist, run generate_routes.py for Turn E.
Rotate templates continuing from last assigned variant.

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
