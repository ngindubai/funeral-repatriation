# BUILD-PLAN.md -- Repatriate Service

> Session log and task tracker. Read at the start of every session.
> The 7-engine system is the build framework. CLAUDE.md is the operating law.

---

## CURRENT STATUS -- 2 June 2026

**Route pages live:** 70
**Blog articles live:** 142 (112 baseline + 30 from Engine 3 Batches 1-6)
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
**Engine 3 status:** Batches 1-6 complete (30 articles).

---

## COMPLETED

- [x] Engines 1, 2, 4, 5, 6, 7: all complete
- [x] Turn A/C/D+: 70 route pages total
- [x] GSC canonical fix: baseURL www (1 Jun 2026)
- [x] GEO/LLM 4-phase implementation (1 Jun 2026)
- [x] 10 thin blog stubs expanded (1 Jun 2026)
- [x] Fix all known issues E008-E011 (1 Jun 2026)
- [x] **Engine 3 Batch 1 (1 Jun 2026):** Cost cluster, 5 articles
  - who-pays-for-repatriation-when-someone-dies-abroad
  - repatriation-cost-without-travel-insurance
  - repatriation-quote-what-to-check
  - crowdfunding-repatriation-costs
  - airline-cargo-costs-repatriation-explained
- [x] **Engine 3 Batch 2 (1 Jun 2026):** Timeline cluster, 5 articles
  - repatriation-timeline-by-cause-of-death
  - repatriation-from-tourist-destinations-typical-timeline
  - repatriation-from-asia-timeline-realistic-expectations
  - post-mortem-extension-impact-on-repatriation-timeline
  - expedited-repatriation-when-and-how
- [x] **Engine 3 Batch 3 (1 Jun 2026):** Documents deep-dive, 5 articles
  - apostille-certification-for-international-repatriation
  - certified-translation-for-death-abroad-documents
  - death-certificate-from-abroad-using-it-in-uk
  - registering-a-death-abroad-with-uk-authorities
  - fcdo-documents-for-repatriation
- [x] **Engine 3 Batch 4 (2 Jun 2026):** Religious and cultural specifics, 5 articles
  - muslim-repatriation-requirements-and-ghusl
  - jewish-repatriation-requirements-and-tahara
  - hindu-repatriation-cremation-options-abroad
  - sikh-repatriation-considerations
  - non-religious-secular-repatriation
- [x] **Engine 3 Batch 5 (2 Jun 2026):** Special circumstances, 5 articles
  - death-of-a-child-abroad-repatriation
  - repatriation-of-uk-military-personnel
  - dual-national-deaths-which-country-process-applies
  - repatriation-when-no-family-can-be-contacted
  - death-abroad-criminal-case-how-repatriation-works
- [x] **Engine 3 Batch 6 (2 Jun 2026):** UK reception cluster, 5 articles
  - what-happens-when-body-arrives-uk-from-abroad
  - uk-coroner-and-repatriated-bodies
  - uk-port-health-and-repatriation
  - registering-a-death-in-uk-after-repatriation
  - uk-funeral-after-repatriation-what-to-expect

---

## KNOWN ISSUES

_None currently blocking._

---

## ENGINE 3 -- BLOG BATCH ROADMAP

### Batches 1-6: DONE (30 articles)

### Batch 7: Airline-policy specific articles (NEXT)
Which airlines accept human remains, IATA standards, container requirements, common airline policies for UK families.
Candidate articles:
- which-airlines-accept-human-remains-cargo
- iata-standards-for-human-remains-transport
- container-requirements-for-repatriation-cargo
- airline-cargo-vs-passenger-aircraft-for-repatriation
- cargo-delays-and-what-causes-them

### Batch 8: Insurance deep-dives
Employer schemes, policy exclusions, premium vs standard cover, claim disputes, pre-existing condition exclusions.

### Batch 9: Comparison and decision articles
Burial abroad vs repatriation, cremation abroad vs repatriation, repatriation vs memorial service, choosing between providers.

### Batch 10: Embalming and preparation deep-dives
International embalming standards, what embalming involves, religious considerations, mortuary services abroad.

### Batch 11+: Country deep-dive blog series
Country-specific blog articles beyond the existing hub pages. E.g. "repatriation from Spain: the most common questions UK families ask."

Target overall: 500+ blog articles. 142 live. 358 to go.

---

## NEXT TASKS -- IN PRIORITY ORDER

### Priority 1: Engine 3 Batch 7 -- airline-policy cluster
Generate 5 articles on airline cargo policies and standards.

### Priority 2: GSC not-indexed audit
Export 859 not-indexed URLs from GSC and categorise. Many should now be resolving from the 1 June canonical/stub fixes.

### Priority 3: Turn E -- next 50 route pages from existing origins

### Priority 4: Reverse route pages (uk-to-{country}, ireland-to-{country})

### Priority 5: Engine 2 further expansion
Needed: poland, czech-republic, hungary, austria, croatia, bulgaria, romania, bahrain, qatar, saudi-arabia, malaysia, china, hong-kong, south-korea, bangladesh, nepal

---

## ROUTE DATA ORIGINS (32 total)

australia, brazil, canada, cyprus, egypt, france, germany, ghana, greece, india, indonesia, israel, italy, japan, jordan, kenya, mexico, morocco, new-zealand, nigeria, pakistan, philippines, portugal, singapore, south-africa, spain, sri-lanka, thailand, turkey, uae, usa, vietnam

---

## ERRORS ENCOUNTERED (summary)

| Error | Status |
|---|---|
| E001-E006 | Fixed/Documented (see ERRORS.md) |
| E007: baseURL missing www | Fixed |
| E008: 70 broken sideways links | Fixed via template filter |
| E009: robots.txt/llms.txt non-www | Fixed |
| E010: Missing cremation-transfer permalink | Fixed |
| E011: Broken sameAs TODO + dead social links | Fixed |

---

*Last updated: 2 June 2026*
