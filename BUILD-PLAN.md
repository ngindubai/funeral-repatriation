# BUILD-PLAN.md -- Repatriate Service

> This file is the quick-reference checklist and session log for the autonomous build routine.
> Read it at the start of every run, immediately after CLAUDE.md.
> The visual master tracker is funeral-repatriation-build-plan.html (kept in sync, not load-bearing).
> CLAUDE.md is the operating law. This file says what to build next.

---

## THE BLOCK RHYTHM (read before every run)

- **One run = one block. Never more.**
- **A block = 25 route pages** at the indicated tier and template, OR (when the blog roadmap shows a batch is due) one blog batch of 5 articles. Never both in one run.
- Every block runs the full quality gate from CLAUDE.md: research from named dated FCDO/embassy sources, write in the wordsmith voice, rotate template_variant A to E (no two consecutive pages share a variant), humanise, QA scan. Zero em dashes. Zero banned vocab. No prices. No safety guarantees. British English. Correct persona.
- **The routine is fully autonomous. There is no human approval step and no wait-for-go.** Write, QA, commit to master, report the live links to Slack, stop. The Slack link post is a record of what shipped, not a gate: nothing waits on it.
- If the QA gate finds any failure, do not commit. Post the halt message and end (see CLAUDE.md QUALITY GATE).
- Every block also updates BUILD-PLAN.md and MEMORY.md in the same commit (MANDATORY DOCS UPDATE in CLAUDE.md).
- Bulk-generation without the quality gate is banned. One block, full gate, every time.

**Where we are (reconciled from disk 5 June 2026):** 70 quality route pages live (35 origins, each to United Kingdom and Ireland). The full route matrix below is now the active build. Chunk R1 is next (Tier A, Template A). Blog: 239 articles live. Country hubs, guides, ashes, cremation, embassy silos all complete (238 countries each). The route engine is the growth engine from here.

---

## THE ROUTE MATRIX -- THE GROWTH ENGINE (Phase R)

This is the spine of the site, the funeral-repatriation equivalent of Pet Transport's 190x190 corridor matrix. The data already exists in `data/countries_repatriation.json` (regulatory detail for 238 countries), `data/countries-197.json` (the canonical country and slug list), and `data/keyword_matrix.json` (search demand per corridor).

**Target: the full origin to destination square. 197 countries as origins, 197 as destinations, minus same-country pairs = 38,612 route pages.** Slug format is the existing convention: `{origin-slug}-to-{destination-slug}.md` in `site/content/routes/`. Destination key uses the full country slug (united-kingdom, ireland, australia, united-states, and so on), not the short `uk`/`ireland` keys.

Routes are built in four tiers, highest commercial intent first. Within each tier, build in the order the tier lists, 25 routes per block, rotating template A to E.

### Tier A -- Inbound to the two core markets (the money tier)

Every country in the world, repatriated to the United Kingdom and to Ireland. This is where the demand is: British and Irish families bringing someone home.

- 197 origins to United Kingdom, plus 197 origins to Ireland = **394 routes.**
- 70 already live (35 origins x UK and Ireland). **324 remaining in Tier A.**
- Build the remaining 162 origins to United Kingdom first, then the remaining 162 to Ireland.
- Order origins by Tier A priority list in `data/keyword_matrix.json` (highest search volume first: Spain, France, Turkey, Greece, USA, Thailand, Cyprus, Portugal, Italy, Germany, then down the list). If a corridor slug already exists on disk, skip it and take the next.

### Tier B -- Diaspora and high-volume cross-border corridors

The corridors where a death abroad most often needs repatriating between two non-UK/Ireland countries, driven by migration and expat patterns. Source the pairs from the `tier_b_corridors` block in `data/keyword_matrix.json` (for example: Pakistan to Saudi Arabia, India to UAE, Philippines to USA, Mexico to USA, Morocco to France, Bangladesh to UAE, Nigeria to USA, Poland to Germany, Portugal to France, Turkey to Germany, and the rest of the diaspora set).

- Approximately **1,100 routes.** Build origins to the top 12 destination hubs (USA, UAE, Saudi Arabia, Germany, France, Canada, Australia, Qatar, Kuwait, Singapore, South Africa, India) excluding pairs already built in Tier A.

### Tier C -- Regional and secondary destination corridors

Every origin to the next band of destination countries (the remaining EU states, Gulf states, major Commonwealth and Anglophone destinations) not covered in A or B. Approximately **7,700 routes.** Source order from `data/keyword_matrix.json` `tier_c` ranking.

### Tier D -- The long-tail completion of the square

All remaining origin to destination pairs to complete the 38,612 matrix. Approximately **29,400 routes.** Built last, lowest individual volume, but this is the long-tail layer that captures the exact-match "{country} to {country} repatriation" queries competitors do not cover. Build in `data/keyword_matrix.json` `tier_d` order.

### Tier totals

| Tier | Description | Routes | Built | Remaining |
|---|---|---|---|---|
| A | All origins to UK and Ireland | 394 | 70 | 324 |
| B | Diaspora and high-volume cross-border | ~1,100 | 0 | ~1,100 |
| C | Regional and secondary destinations | ~7,700 | 0 | ~7,700 |
| D | Long-tail completion of the square | ~29,400 | 0 | ~29,400 |
| **Total** | **Full 197x197 matrix** | **38,612** | **70** | **38,542** |

At 8 blocks per day, 7 days per week (56 blocks per week, 25 routes per block = 1,400 routes per week), the full matrix completes in approximately 28 weeks. Tier A alone (the revenue tier) completes in under 3 weeks.

---

## TEMPLATE ROTATION

Rotate `template_variant` A, B, C, D, E across every block so no two consecutive pages share a layout, exactly as the 70 live pages already do. The five variants are defined in CLAUDE.md (TEMPLATE VARIANTS) and implemented in `site/layouts/routes/single.html`.

- Next chunk: **R1**
- Next tier: **A**
- Next template lead: **A** (rotation continues A, B, C, D, E across the 25 routes in the block)

---

## CHUNK LEDGER

The routine names each route block "chunk R<N>" in its commit message so the skip-check in the routine can detect an already-built chunk. Increment R<N> by one each block.

| Chunk | Tier | Template lead | Routes | Status | Notes |
|---|---|---|---|---|---|
| (pre-matrix) | A | mixed | 70 | DONE | 35 origins to UK and Ireland. Live before the matrix plan. |
| R1 | A | A | 25 | NEXT | Remaining highest-volume origins to United Kingdom. |

When a chunk is committed, add its row here (date, tier, template, routes, corridors) in the same commit, mirroring the Pet Transport session log style.

---

## BLOG ROADMAP (Engine 3) -- runs in parallel, one batch when a route block is not due

239 articles live. Target 500+. Blog batches are built only when the route matrix is not the priority for that run; the route matrix is the default. Each batch is 5 articles, distinct topics, checked against `site/content/blog/` for existing slugs first (no cannibalisation). Author personas rotate per CLAUDE.md.

### Next blog batches (build in order, 5 articles each)

- **Batch 27 -- Practical first-contact cluster:** who-to-call-when-someone-dies-abroad, contacting-the-british-embassy-after-death-abroad, what-happens-to-passport-after-death-abroad, next-of-kin-rights-when-someone-dies-abroad, funeral-director-abroad-what-they-do-and-how-to-choose.
- **Batch 28 -- Cause-specific cluster:** heart-attack-abroad-repatriation-and-post-mortem, road-accident-abroad-repatriation-process, drowning-abroad-inquest-and-repatriation, sudden-death-abroad-what-families-need-to-know, unexplained-death-abroad-what-happens-next.
- **Batch 29 -- Sector deep-dives:** death-in-hospital-abroad-release-procedure, death-in-a-hotel-room-abroad-what-happens, death-in-custody-abroad-uk-family-rights, death-at-a-sports-event-abroad, death-in-a-care-facility-abroad-repatriation.
- **Batch 30 onward -- Country deep-dive long-tail:** continue the "repatriation from {country} questions families ask" series for any country not yet covered, then "cost of repatriation from {country}" angle (no figures, directs to enquiry), then "how long does repatriation from {country} take". Generate the next country from `data/countries-197.json` order, skipping any slug already on disk.

The blog roadmap does not end. When the listed batches are exhausted, continue the country long-tail series above. There is no stop condition: the routine keeps building the next unbuilt unit every run, indefinitely.

---

## NEXT TASKS -- IN PRIORITY ORDER

1. **Route matrix, Tier A, chunk R1** (default every run): next 25 unbuilt routes in Tier A order. This is the priority until Tier A is complete.
2. After Tier A: continue to Tier B, then C, then D, same block rhythm.
3. Blog batches 27 onward: built on any run where a route block has just been built by a concurrent run and the next route chunk is already committed (the routine's skip-check will route it here).

---

## SESSION LOG

| Date | Chunk / Batch | Work Done | Routes/Pages | Notes |
|------|------|-----------|-------| ------|
| 5 Jun 2026 | Plan rebuild | Route matrix plan installed: full 197x197 tiered matrix (38,612 target), four tiers A to D, chunk ledger, autonomous rhythm. Replaces the previous stub plan that topped out at the blog roadmap. No content built this entry. | 70 (unchanged) | Build plan now at parity with Pet Transport. Chunk R1 (Tier A, Template A) is next. |

---

*Last updated: 5 June 2026. The routine builds one block per run, autonomously, and reports live links to Slack. No approval step. No stop condition.*
