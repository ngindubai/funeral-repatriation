# BUILD-PLAN.md -- Repatriate Service

> Session log and task tracker. Read at the start of every session.
> The 7-engine system is the build framework. CLAUDE.md is the operating law.

---

## CURRENT STATUS -- 1 June 2026

**Route pages live:** 70
**Blog articles live:** 117 (112 + 5 from Engine 3 Batch 1)
**Country hubs:** 238
**Guides:** 238 (one per country)
**Bringing ashes home pages:** 238
**Cremation transfer pages:** 238
**Embassy contact pages:** 238
**City pages:** 220
**Total indexable pages (approx):** 1,400+
**GSC known pages:** ~2,740
**GSC indexed:** 1,880
**GSC not indexed:** 859 (expected to drop after recent fixes)
**Target route pages:** 30,000+
**Engines complete:** 1, 2 (32 origins), 4, 5, 6, 7
**Engine 3 status:** Started 1 Jun 2026. Batch 1 complete (5 articles).

---

## COMPLETED

- [x] Engine 7: CLAUDE.md, AGENTS.md, workforce/ installed
- [x] Engine 5: qa_routes.py, check_titles.py, check_schema.py, seo_pass.py
- [x] Engine 2: site/data/route_data/ with 32 origins
- [x] Engine 1: generate_routes.py upgraded
- [x] Engine 4: rebuild_link_graph.py, diagnose_links.py installed
- [x] Template rotation: all 70 route pages have A-E variants
- [x] Turn A/C/D+: 70 route pages total
- [x] GSC canonical fix: baseURL changed to www (1 Jun 2026)
- [x] GEO/LLM 4-phase implementation complete (1 Jun 2026)
- [x] 10 thin blog stubs expanded to full articles (1 Jun 2026)
- [x] Country hub audit: all 4 newer origins confirmed (1 Jun 2026)
- [x] Fix all known issues pass (1 Jun 2026): E008-E011 all resolved
- [x] **Engine 3 Batch 1 (1 Jun 2026):** Commercial-intent cost cluster, 5 articles
  - who-pays-for-repatriation-when-someone-dies-abroad
  - repatriation-cost-without-travel-insurance
  - repatriation-quote-what-to-check
  - crowdfunding-repatriation-costs
  - airline-cargo-costs-repatriation-explained
  - Manifest script: scripts/generate_blog_batch1.py

---

## KNOWN ISSUES

_None currently blocking. All issues identified during 1 June audit have been fixed._

---

## ENGINE 3 -- BLOG BATCH ROADMAP

### Batch 1: Cost cluster (DONE, 1 Jun 2026)
Commercial-intent payer/quote/funding articles. 5 articles. Live.

### Batch 2: Timeline cluster (NEXT)
Timeline articles by scenario, country, and case type. Covers high-search-volume "how long does X take" queries that the single existing generic timeline article does not address.
Candidate articles:
- repatriation-timeline-by-cause-of-death
- repatriation-from-tourist-destinations-typical-timeline
- repatriation-from-asia-timeline-realistic-expectations
- post-mortem-extension-impact-on-repatriation-timeline
- expedited-repatriation-when-and-how

### Batch 3: Documents deep-dive cluster
Apostille, legalisation, notarisation, translation, FCDO documents. Each merits its own page.
Candidate articles:
- apostille-certification-for-international-repatriation
- certified-translation-for-death-abroad-documents
- death-certificate-from-abroad-using-it-in-uk
- registering-a-death-abroad-with-uk-authorities
- fcdo-documents-for-repatriation

### Batch 4: Religious and cultural specifics
Faith-specific repatriation requirements. Existing general piece doesn't cover the granularity.
Candidate articles:
- muslim-repatriation-requirements-and-ghusl
- jewish-repatriation-requirements-and-tahara
- hindu-repatriation-cremation-options-abroad
- sikh-repatriation-considerations
- humanist-and-secular-repatriation

### Batch 5: Special-circumstance cluster
Child deaths, military, dual nationals, unidentified remains. High-stakes long-tail.
Candidate articles:
- death-of-a-child-abroad-repatriation
- repatriation-of-uk-military-personnel
- dual-national-deaths-which-country-process-applies
- unidentified-remains-repatriation-process
- mass-casualty-events-and-repatriation

### Beyond Batch 5
- UK reception cluster (coroner, registration, port health)
- Airline-policy specific articles
- Insurance deep-dives (employer schemes, exclusions, premium vs standard)
- Comparison/decision articles
- Embalming/preparation deep-dives

Target overall: 500+ blog articles. 117 live. 383 to go.

---

## NEXT TASKS -- IN PRIORITY ORDER

### Priority 1: Engine 3 Batch 2 -- timeline cluster
Generate 5 timeline-themed articles (see roadmap above). Same pattern: manifest script + content via MCP.

### Priority 2: GSC not-indexed audit
Export the 859 not-indexed URLs from GSC and categorise by reason.
Many of these should self-resolve over the next 7-14 days as Google re-crawls the canonical/stub/template fixes from 1 June.

### Priority 3: Turn E -- next 50 route pages from existing origins
Identify missing corridors from the 32 existing origins (some have only UK or only Ireland page).
Generate the missing direction for each.

### Priority 4: Reverse route pages (uk-to-{country}, ireland-to-{country})
Building these would activate the now-filtered sideways links (E008 fix means they currently don't render; building reverse routes makes them auto-restore).
Requires a new destination key pattern in the data layer.

### Priority 5: Engine 2 further expansion
Add new origins to enable Turn F.
Needed: poland, czech-republic, hungary, austria, croatia, bulgaria, romania, bahrain, qatar, saudi-arabia, malaysia, china, hong-kong, south-korea, bangladesh, nepal

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
| E008: 70 broken sideways links | Fixed via template filter (site.GetPage check) |
| E009: robots.txt/llms.txt non-www URLs | Fixed. Both rewritten with www. |
| E010: Missing cremation-transfer permalink | Fixed. Added to hugo.toml. |
| E011: Broken sameAs TODO + dead social links | Fixed. Removed until real URLs exist. |

---

*Last updated: 1 June 2026*
