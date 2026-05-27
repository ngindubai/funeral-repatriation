# BUILD-PLAN.md -- Repatriate Service

> Session log and task tracker. Read at the start of every session.
> The 7-engine system is the build framework. CLAUDE.md is the operating law.

---

## CURRENT STATUS -- 28 May 2026

**Route pages live:** 48
**Target:** 30,000+
**Engines complete:** 1, 2 (partial), 4, 5, 6, 7
**Engines pending:** 3 (blog), 2 expansion (more origins)

---

## COMPLETED THIS SESSION

- [x] Engine 7: CLAUDE.md, AGENTS.md, workforce/ installed
- [x] Engine 5: qa_routes.py, check_titles.py, check_schema.py, seo_pass.py
- [x] Engine 2: site/data/route_data/ with 11 origins (22 corridors)
- [x] Engine 1: generate_routes.py upgraded to read route_data, apply wordsmith voice, QA gate
- [x] Engine 4: rebuild_link_graph.py, diagnose_links.py installed
- [x] Template rotation: single.html implements all A-E variants; all 48 pages have template_variant
- [x] Turn C: 23 new route pages committed (Ireland-destination + new UK-destination origins)
- [x] ERRORS.md updated with E006 (.md files in site/data/ break Hugo build)
- [x] MEMORY.md and BUILD-PLAN.md updated

---

## NEXT TASKS -- IN PRIORITY ORDER

### Priority 1: Engine 2 expansion
Add more origins to site/data/route_data/ to enable Turn D generation.
Currently: 11 origins (spain, thailand, uae, usa, australia, greece, cyprus, turkey, philippines, india, france)
Need to add: japan, italy, portugal, germany, south-africa, kenya, morocco, vietnam, sri-lanka, egypt, indonesia, brazil, nigeria, ghana, jordan, new-zealand, canada, mexico
plus: poland, czech-republic, hungary, austria, croatia, bulgaria, romania, israel, bahrain, qatar, saudi-arabia, singapore, malaysia, china, hong-kong, south-korea, pakistan, bangladesh, nepal

Target: 50+ origins covering all UK search volume corridors.

### Priority 2: Turn D -- next 25 route pages
Once route_data files exist, run generate_routes.py to produce Turn D.
Next corridors to generate:
- All existing origins x ireland (where not yet done)
- New origins x uk and ireland
Rotate templates continuing from last assigned variant.

### Priority 3: Engine 3 -- blog batch factory
Build generate_blog_batch1.py through generate_blog_batch5.py.
Modelled on pet-transport repo batch system.
Content: topical authority articles around repatriation, what to do guides, country-specific deep dives.
150 articles already live. Target: 500+.

### Priority 4: Engine 2 -- country hubs for new origins
As route pages are added for new countries (Japan, Italy, Poland etc.), ensure country hub pages exist at /repatriation-from-{country}/.
Audit what hubs are missing for current 48 route origins.

### Priority 5: seo_pass.py audit on all 48 pages
Run the full Engine 5 audit on the complete route page set.
Fix any errors before proceeding to Turn D.

### Priority 6: rebuild_link_graph.py --fix
Run Engine 4 with --fix to patch any missing links across all 48 pages.
Then run diagnose_links.py to confirm no orphans.

---

## SCALE ROADMAP

| Batch | Pages | Cumulative |
|---|---|---|
| Turn A | 25 | 25 |
| Turn C | 23 | 48 |
| Turn D | 25 | 73 |
| Turn E | 50 | 123 |
| Turn F | 100 | 223 |
| ... | ... | ... |
| Target | 30,000+ | 30,000+ |

To reach 30,000: need ~200 origins x 150 destinations.
Immediate next step: expand Engine 2 to 50+ origins, generate 2 destinations each = 100 new pages per Engine 1 run.

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

---

*Last updated: 28 May 2026*
