# BUILD-PLAN.md -- Repatriate Service

> Session log and task tracker. Read at the start of every session.
> The 7-engine system is the build framework. CLAUDE.md is the operating law.

---

## CURRENT STATUS -- 4 June 2026

**Route pages live:** 70
**Blog articles live:** 229 (112 baseline + 117 from Engine 3 Batches 1-24)
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
**Engine 3 status:** Batches 1-24 complete (117 articles).

---

## DEPLOY ARCHITECTURE (confirmed 2 June 2026 -- READ THIS)

Production is served as follows:

```
push to master
  -> build-and-publish.yml builds Hugo and force-pushes built HTML to the `live` branch
     -> Hostinger Git integration pulls the `live` branch into /public_html/   <- THIS serves the site
```

- **build-and-publish.yml is the production pipeline. Do not disable it.** The `live` branch is load-bearing: Hostinger pulls it.
- **deploy.yml (FTP) is DISABLED** as of 2 June 2026. It is now a manual-only no-op stub. It used to FTP-push into /public_html/, which fought with Hostinger's own Git pull into the same folder, and it deleted the FTP sync-state on every run. Do not re-enable it with a push trigger.
- FTP secrets (FTP_SERVER / FTP_USERNAME / FTP_PASSWORD) are now unused and can be deleted from GitHub repo secrets.
- buildFuture = true is set in hugo.toml. Keep it. See E012.

---

## COMPLETED

- [x] Engines 1, 2, 4, 5, 6, 7: all complete
- [x] Turn A/C/D+: 70 route pages total
- [x] GSC canonical fix: baseURL www (1 Jun 2026)
- [x] GEO/LLM 4-phase implementation (1 Jun 2026)
- [x] 10 thin blog stubs expanded (1 Jun 2026)
- [x] Fix all known issues E008-E011 (1 Jun 2026)
- [x] **E012 fix (2 Jun 2026):** buildFuture=true added to hugo.toml. Root cause of Batch 4-6 404s was future-dated content silently skipped by Hugo on a UTC build. See ERRORS.md.
- [x] **Deploy structural fix (2 Jun 2026):** Confirmed Hostinger pulls the `live` branch. Disabled the redundant FTP workflow (deploy.yml) that was double-writing to /public_html/ and deleting sync-state each run.
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
- [x] **Engine 3 Batch 7 (2 Jun 2026):** Airline and cargo cluster, 5 articles
  - which-airlines-accept-human-remains-cargo
  - iata-standards-for-human-remains-transport
  - container-requirements-for-repatriation-cargo
  - airline-cargo-vs-passenger-aircraft-for-repatriation
  - cargo-delays-and-what-causes-them
- [x] **Engine 3 Batch 8 (2 Jun 2026):** Insurance deep-dives, 5 articles
  - does-travel-insurance-cover-repatriation-of-remains
  - how-insurer-assistance-company-coordinates-repatriation
  - repatriation-and-pre-existing-medical-conditions
  - repatriation-insurance-claim-refused-what-to-do
  - credit-card-bank-travel-cover-repatriation
- [x] **Engine 3 Batch 9 (3 Jun 2026):** Comparison and decision, 2 articles
  - repatriation-vs-local-memorial-service
  - direct-repatriation-vs-full-service-what-differs
  - Note: 3 of the 5 roadmap candidates were dropped because the topics already exist live (burial-abroad-vs-repatriation = repatriation-vs-local-burial-abroad; cremation-abroad-vs-repatriation = repatriation-vs-cremation-abroad; how-to-choose-a-provider = how-to-choose-a-repatriation-company + ...-funeral-director). Duplicates avoided per no-duplicate-content rule.
- [x] **Engine 3 Batch 10 (3 Jun 2026):** Embalming and mortuary preparation, 5 articles
  - when-embalming-is-not-required-for-repatriation
  - what-happens-in-the-mortuary-before-repatriation
  - viewing-a-repatriated-body-in-the-uk
  - body-preparation-time-before-repatriation-flight
  - mortuary-standards-abroad-what-families-should-know
- [x] **Engine 3 Batch 11 (4 Jun 2026):** Country deep-dive series (questions families ask), 5 articles
  - repatriation-from-spain-questions-families-ask
  - repatriation-from-greece-questions-families-ask
  - repatriation-from-turkey-questions-families-ask
  - repatriation-from-thailand-questions-families-ask
  - repatriation-from-cyprus-questions-families-ask
  - Angle: family question (Q&A) format, distinct from the existing -guide process articles, cross-linked to them.
- [x] **Engine 3 Batch 12 (4 Jun 2026):** Country deep-dive series part 2 (questions families ask), 5 articles
  - repatriation-from-france-questions-families-ask
  - repatriation-from-portugal-questions-families-ask
  - repatriation-from-usa-questions-families-ask
  - repatriation-from-india-questions-families-ask
  - repatriation-from-uae-questions-families-ask
- [x] **Engine 3 Batch 13 (4 Jun 2026):** Country deep-dive series part 3 (questions families ask), 5 articles
  - repatriation-from-germany-questions-families-ask
  - repatriation-from-italy-questions-families-ask
  - repatriation-from-egypt-questions-families-ask
  - repatriation-from-pakistan-questions-families-ask
  - repatriation-from-australia-questions-families-ask
- [x] **Engine 3 Batch 14 (4 Jun 2026):** Country deep-dive series part 4 (questions families ask), 5 articles
  - repatriation-from-morocco-questions-families-ask
  - repatriation-from-kenya-questions-families-ask
  - repatriation-from-south-africa-questions-families-ask
  - repatriation-from-nigeria-questions-families-ask
  - repatriation-from-philippines-questions-families-ask
- [x] **Engine 3 Batch 15 (4 Jun 2026):** Country deep-dive series part 5 (questions families ask), 5 articles
  - repatriation-from-brazil-questions-families-ask
  - repatriation-from-canada-questions-families-ask
  - repatriation-from-mexico-questions-families-ask
  - repatriation-from-indonesia-questions-families-ask
  - repatriation-from-sri-lanka-questions-families-ask
- [x] **Engine 3 Batch 16 (4 Jun 2026):** Country deep-dive series part 6 (questions families ask), 5 articles
  - repatriation-from-japan-questions-families-ask
  - repatriation-from-singapore-questions-families-ask
  - repatriation-from-vietnam-questions-families-ask
  - repatriation-from-new-zealand-questions-families-ask
  - repatriation-from-israel-questions-families-ask
- [x] **Engine 3 Batch 17 (4 Jun 2026):** Country deep-dive series part 7 (questions families ask), 5 articles
  - repatriation-from-jordan-questions-families-ask
  - repatriation-from-ghana-questions-families-ask
  - repatriation-from-china-questions-families-ask
  - repatriation-from-hong-kong-questions-families-ask
  - repatriation-from-jamaica-questions-families-ask
- [x] **Engine 3 Batch 18 (4 Jun 2026):** Country deep-dive series part 8 (questions families ask), 5 articles
  - repatriation-from-bangladesh-questions-families-ask
  - repatriation-from-nepal-questions-families-ask
  - repatriation-from-south-korea-questions-families-ask
  - repatriation-from-malaysia-questions-families-ask
  - repatriation-from-saudi-arabia-questions-families-ask
- [x] **Engine 3 Batch 19 (4 Jun 2026):** Country deep-dive series part 9 (questions families ask), 5 articles
  - repatriation-from-qatar-questions-families-ask
  - repatriation-from-bahrain-questions-families-ask
  - repatriation-from-austria-questions-families-ask
  - repatriation-from-poland-questions-families-ask
  - repatriation-from-czech-republic-questions-families-ask
- [x] **Engine 3 Batch 20 (4 Jun 2026):** Country deep-dive series part 10 (questions families ask), 5 articles
  - repatriation-from-hungary-questions-families-ask
  - repatriation-from-croatia-questions-families-ask
  - repatriation-from-romania-questions-families-ask
  - repatriation-from-bulgaria-questions-families-ask
  - repatriation-from-serbia-questions-families-ask
- [x] **Engine 3 Batch 21 (4 Jun 2026):** Country deep-dive series part 11 (questions families ask), 5 articles
  - repatriation-from-albania-questions-families-ask
  - repatriation-from-montenegro-questions-families-ask
  - repatriation-from-ireland-questions-families-ask
  - repatriation-from-maldives-questions-families-ask
  - repatriation-from-tunisia-questions-families-ask
  - Note: North Macedonia, Kosovo, Bosnia dropped (no guide pages exist). Replaced with Ireland, Maldives, Tunisia.
- [x] **Engine 3 Batch 22 (4 Jun 2026):** Country deep-dive series part 12 (questions families ask), 5 articles
  - repatriation-from-iceland-questions-families-ask
  - repatriation-from-netherlands-questions-families-ask
  - repatriation-from-norway-questions-families-ask
  - repatriation-from-sweden-questions-families-ask
  - repatriation-from-switzerland-questions-families-ask
- [x] **Engine 3 Batch 23 (4 Jun 2026):** Country deep-dive series part 13 (questions families ask), 5 articles
  - repatriation-from-oman-questions-families-ask
  - repatriation-from-kuwait-questions-families-ask
  - repatriation-from-lebanon-questions-families-ask
  - repatriation-from-mauritius-questions-families-ask
  - repatriation-from-tanzania-questions-families-ask
- [x] **Engine 3 Batch 24 (4 Jun 2026):** Country deep-dive series part 14 (questions families ask), 5 articles
  - repatriation-from-uganda-questions-families-ask
  - repatriation-from-rwanda-questions-families-ask
  - repatriation-from-zimbabwe-questions-families-ask
  - repatriation-from-kazakhstan-questions-families-ask
  - repatriation-from-taiwan-questions-families-ask

---

## KNOWN ISSUES

_None currently blocking._

Tidy-up (non-blocking, manual): delete unused FTP_SERVER / FTP_USERNAME / FTP_PASSWORD secrets from GitHub now that deploy.yml is disabled.

---

## ENGINE 3 -- BLOG BATCH ROADMAP

### Batches 1-8: DONE (40 articles)

### Batch 9: Comparison and decision articles -- DONE (2 articles)
- repatriation-vs-local-memorial-service
- direct-repatriation-vs-full-service-what-differs
3 candidate slugs dropped as duplicates of existing live articles (see COMPLETED above). Before any future batch, check site/content/blog/ for an existing slug on the same topic to avoid cannibalisation.

### Batch 10: Embalming and preparation deep-dives -- DONE (5 articles)
when-embalming-is-not-required, what-happens-in-the-mortuary, viewing-a-repatriated-body-in-the-uk, body-preparation-time, mortuary-standards-abroad.

### Batch 11: Country deep-dive series (questions families ask) -- DONE (5 articles)
Spain, Greece, Turkey, Thailand, Cyprus. Q&A format, distinct from the -guide articles, cross-linked.

### Batch 12: Country deep-dive series, part 2 -- DONE (5 articles)
France, Portugal, USA, India, UAE. Q&A format, distinct from the -guide articles, cross-linked.

### Batch 13: Country deep-dive series, part 3 -- DONE (5 articles)
Germany, Italy, Egypt, Pakistan, Australia. Q&A format, distinct from the -guide articles, cross-linked.

### Batch 14: Country deep-dive series, part 4 -- DONE (5 articles)
Morocco, Kenya, South Africa, Nigeria, Philippines. Q&A format, distinct from the -guide articles, cross-linked.

### Batch 15: Country deep-dive series, part 5 -- DONE (5 articles)
Brazil, Canada, Mexico, Indonesia, Sri Lanka. Q&A format, distinct from -guide articles, cross-linked.

### Batch 16: Country deep-dive series, part 6 -- DONE (5 articles)
Japan, Singapore, Vietnam, New Zealand, Israel. Q&A format, distinct from -guide articles, cross-linked.

### Batch 17: Country deep-dive series, part 7 -- DONE (5 articles)
Jordan, Ghana, China, Hong Kong, Jamaica. Q&A format, distinct from -guide articles, cross-linked.

### Batch 18: Country deep-dive series, part 8 -- DONE (5 articles)
Bangladesh, Nepal, South Korea, Malaysia, Saudi Arabia. Q&A format, distinct from -guide articles, cross-linked.

### Batch 19: Country deep-dive series, part 9 -- DONE (5 articles)
Qatar, Bahrain, Austria, Poland, Czech Republic. Q&A format, distinct from -guide articles, cross-linked.

### Batch 20: Country deep-dive series, part 10 -- DONE (5 articles)
Hungary, Croatia, Romania, Bulgaria, Serbia. Q&A format, distinct from -guide articles, cross-linked.

### Batch 21: Country deep-dive series, part 11 -- DONE (5 articles)
Albania, Montenegro, Ireland, Maldives, Tunisia. Q&A format, distinct from -guide articles, cross-linked.

### Batch 22: Country deep-dive series, part 12 -- DONE (5 articles)
Iceland, Netherlands, Norway, Sweden, Switzerland. Q&A format, distinct from -guide articles, cross-linked.

### Batch 23: Country deep-dive series, part 13 -- DONE (5 articles)
Oman, Kuwait, Lebanon, Mauritius, Tanzania. Q&A format, distinct from -guide articles, cross-linked.

### Batch 24: Country deep-dive series, part 14 -- DONE (5 articles)
Uganda, Rwanda, Zimbabwe, Kazakhstan, Taiwan. Q&A format, distinct from -guide articles, cross-linked.

### Batch 25: Country deep-dive series, part 15 (NEXT)
Next origins. Suggested: Peru, Venezuela, Myanmar, Laos, Slovenia. Check existing -guide slugs and avoid duplicating the guide content. Note: this likely completes the available -guide country coverage; after this, pivot to a new blog cluster (e.g. practical how-to, sector deep-dives, or seasonal/awareness topics).

### Batch 15+: remaining origins and any new clusters.

Target overall: 500+ blog articles. 229 live. 271 to go.

---

## NEXT TASKS -- IN PRIORITY ORDER

### Priority 1: Engine 3 Batch 25 -- country deep-dive series part 15
Next 5 origins (Peru, Venezuela, Myanmar, Laos, Slovenia) in the questions-families-ask format. Check existing -guide slugs; complement, do not duplicate. This likely exhausts the -guide country list; plan a new cluster for Batch 26+.

### Priority 2: GSC not-indexed audit
Export 859 not-indexed URLs from GSC and categorise. Many should now be resolving from the 1 June canonical/stub fixes. Worth checking now that 7-14 days are passing since the canonical fix.

### Priority 3: Turn E -- next 50 route pages from existing origins

### Priority 4: Reverse route pages (uk-to-{country}, ireland-to-{country})
Note: building these auto-restores the E008-filtered sideways links.

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
| E012: Future-dated content skipped by Hugo | Fixed (buildFuture=true) |
| Structural: duplicate deploy workflows | Fixed (deploy.yml disabled; Hostinger pulls `live`) |

---

*Last updated: 4 June 2026 (Batch 24 complete)*
