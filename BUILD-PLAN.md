# BUILD-PLAN.md -- Repatriate Service

> This file is the quick-reference checklist and session log for the autonomous build routine.
> Read it at the start of every run, immediately after CLAUDE.md.
> The visual master tracker is funeral-repatriation-build-plan.html (kept in sync, not load-bearing).
> CLAUDE.md is the operating law. This file says what to build next.

---

## THE BLOCK RHYTHM (read before every run)

- **One run = one batch of up to 4 blocks.** Floor is 1 block. (Changed 5 June 2026 from one block per run, to fit the 15-run routine cap; see session log.)
- **A block = 25 route pages** at the indicated tier and template, OR (when the blog roadmap shows a batch is due) one blog batch of 5 articles. A run builds up to 4 such blocks. Do not mix route and blog blocks unless the route chunks are exhausted for the run.
- Every block runs the full quality gate from CLAUDE.md: research from named dated FCDO/embassy sources, write in the wordsmith voice, rotate template_variant A to E (no two consecutive pages share a variant), humanise, QA scan. Zero em dashes. Zero banned vocab. No prices. No safety guarantees. British English. Correct persona.
- Quality first: if a run cannot finish 4 blocks cleanly, build as many as pass the gate (minimum 1), commit those, and note the shortfall in Slack.
- **The routine is fully autonomous. There is no human approval step and no wait-for-go.** Write, QA each block, commit the whole batch to master once, report the live links to Slack, stop. The Slack link post is a record of what shipped, not a gate: nothing waits on it.
- **One push per run.** Commit the whole batch in a single commit so concurrent deploys never clobber each other (see CLAUDE.md race condition warning). One push = one deploy per run.
- If the QA gate finds a failure on a block, do not commit that block (see CLAUDE.md QUALITY GATE).
- Every batch also updates BUILD-PLAN.md and MEMORY.md in the same commit (MANDATORY DOCS UPDATE in CLAUDE.md).
- **Skip rule:** skip a block whose slugs already exist; skip the whole run only if nothing is left to build (no unbuilt chunk and no blog batch due). Do NOT skip just because a build ran earlier today; this routine runs twice a day on purpose.
- Bulk-generation without the quality gate is banned. A batch is still N individually quality-gated blocks, full gate on each, every time.

**Where we are (11 June 2026):** 1,023 quality route pages live (196 to UK, 196 to Ireland, 6 pre-matrix mixed, 625 Tier B diaspora corridors). Tier A complete (394 routes). Chunks R14-R38 (Tier B, first 625 routes) committed. R35 introduced new destination hubs Greece, Austria, Denmark; R36 introduced Finland; R37-R38 added wave 2 and wave 3 corridors to Greece, Austria, Denmark, Finland, plus New Zealand wave 3 and Japan wave 3. R39 (Tier B, continued waves) is next. Blog: 239 articles live. Country hubs, guides, ashes, cremation, embassy silos all complete (238 countries each). The route engine is the growth engine from here.

---

## THE ROUTE MATRIX -- THE GROWTH ENGINE (Phase R)

This is the spine of the site, the funeral-repatriation equivalent of Pet Transport's 190x190 corridor matrix. The data already exists in `data/countries_repatriation.json` (regulatory detail for 238 countries), `data/countries-197.json` (the canonical country and slug list), and `data/keyword_matrix.json` (search demand per corridor).

**Target: the full origin to destination square. 197 countries as origins, 197 as destinations, minus same-country pairs = 38,612 route pages.** Slug format is the existing convention: `{origin-slug}-to-{destination-slug}.md` in `site/content/routes/`. Destination key uses the full country slug (united-kingdom, ireland, australia, united-states, and so on), not the short `uk`/`ireland` keys.

Routes are built in four tiers, highest commercial intent first. Within each tier, build in the order the tier lists, 25 routes per block, rotating template A to E. A single run builds up to 4 such blocks and commits them once.

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
| A | All origins to UK and Ireland | 394 | 394 | 0 |
| B | Diaspora and high-volume cross-border | ~1,100 | 625 | ~475 |
| C | Regional and secondary destinations | ~7,700 | 0 | ~7,700 |
| D | Long-tail completion of the square | ~29,400 | 0 | ~29,400 |
| **Total** | **Full 197x197 matrix** | **38,612** | **1,023** | **37,589** |

At 2 runs per day, each a batch of up to 4 blocks (up to 8 blocks per day, 25 routes per block = up to 200 routes per day), Tier A (the revenue tier) completes in under 3 weeks and the full matrix in roughly the same horizon as before.

---

## TEMPLATE ROTATION

Rotate `template_variant` A, B, C, D, E across every block so no two consecutive pages share a layout, exactly as the 70 live pages already do. The five variants are defined in CLAUDE.md (TEMPLATE VARIANTS) and implemented in `site/layouts/routes/single.html`. The rotation continues across blocks within a batch (it does not reset per block).

- Next chunk: **R39 (Tier B)**
- Next tier: **B**
- Next template lead: **D** (rotation continues from last page of R38, variant C, so next is D)

---

## CHUNK LEDGER

The routine names each route block "chunk R<N>" in its commit message so the skip-check in the routine can detect an already-built chunk. Increment R<N> by one each block. A batch covers a contiguous run of chunks (for example R1 to R4); record each chunk row in the same batch commit.

| Chunk | Tier | Template lead | Routes | Status | Notes |
|---|---|---|---|---|---|
| (pre-matrix) | A | mixed | 70 | DONE | 35 origins to UK and Ireland. Live before the matrix plan. |
| R1 | A | A | 25 | DONE | cambodia, dominican-republic, poland, china, saudi-arabia, kuwait, qatar, bahrain, malaysia, austria, croatia, czech-republic, hungary, bulgaria, netherlands, belgium, sweden, norway, switzerland, denmark, finland, romania, bangladesh, jamaica, gambia to UK. 5 Jun 2026. |
| R2 | A | A | 25 | DONE | barbados, trinidad-and-tobago, cuba, colombia, argentina, peru, chile, albania, ukraine, georgia, azerbaijan, armenia, kazakhstan, oman, nepal, myanmar, taiwan, south-korea, north-macedonia, serbia, montenegro, slovakia, slovenia, estonia, latvia to UK. 5 Jun 2026. |
| R3 | A | A | 25 | DONE | lithuania, luxembourg, iceland, malta, iran, iraq, lebanon, laos, mongolia, afghanistan, kyrgyzstan, uzbekistan, tajikistan, turkmenistan, belarus, moldova, senegal, ivory-coast, ethiopia, tanzania, uganda, zimbabwe, zambia, mozambique, botswana to UK. 5 Jun 2026. |
| R4 | A | A | 25 | DONE | namibia, malawi, rwanda, cameroon, angola, algeria, tunisia, libya, sudan, eritrea, djibouti, somalia, south-sudan, democratic-republic-of-the-congo, congo, gabon, equatorial-guinea, burundi, sierra-leone, liberia, guinea, guinea-bissau, burkina-faso, benin, togo to UK. 5 Jun 2026. |
| R5 | A | A | 25 | DONE | andorra, antigua-and-barbuda, bahamas, belize, bhutan, bolivia, bosnia-and-herzegovina, brunei, cabo-verde, central-african-republic, chad, comoros, costa-rica, dominica, ecuador, el-salvador, eswatini, fiji, grenada, guatemala, guyana, haiti, honduras, hong-kong, ireland to UK. 6 Jun 2026. |
| R6 | A | A | 25 | DONE | kiribati, liechtenstein, madagascar, maldives, mali, marshall-islands, mauritania, mauritius, micronesia, monaco, nauru, nicaragua, niger, north-korea, palau, palestine, panama, papua-new-guinea, paraguay, russia, saint-kitts-and-nevis, saint-lucia, saint-vincent-and-the-grenadines, samoa to UK (lesotho pre-existing). 6 Jun 2026. |
| R7 | A | B | 25 | DONE | san-marino, sao-tome-and-principe, seychelles, solomon-islands, suriname, syria, timor-leste, tonga, tuvalu, uruguay, vanuatu, vatican-city, venezuela, yemen to UK; afghanistan, albania, algeria, andorra, angola, antigua-and-barbuda, argentina, armenia, austria, azerbaijan, bahamas to Ireland. 6 Jun 2026. |
| R8 | A | C | 25 | DONE | barbados, belarus, belgium, belize, benin, bhutan, bolivia, bosnia-and-herzegovina, botswana, brunei, bulgaria, burkina-faso, burundi, cabo-verde, cambodia, cameroon, central-african-republic, chad, chile, china, colombia, comoros, congo to Ireland (bahrain, bangladesh pre-existing). 6 Jun 2026. |
| R9 | A | A | 25 | DONE | costa-rica, croatia, cuba, czech-republic, democratic-republic-of-the-congo, denmark, djibouti, dominica, dominican-republic, ecuador, el-salvador, equatorial-guinea, eritrea, estonia, eswatini, ethiopia, fiji, finland, gabon, gambia, georgia, grenada, guatemala, guinea, guinea-bissau to Ireland. 6 Jun 2026. |
| R10 | A | A | 25 | DONE | guyana, haiti, honduras, hungary, iceland, iran, iraq, ivory-coast, jamaica, kazakhstan, kiribati, kuwait, kyrgyzstan, laos, latvia, lebanon, lesotho, liberia, libya, liechtenstein, lithuania, luxembourg, madagascar, malawi, malaysia to Ireland. 6 Jun 2026. |
| R11 | A | A | 25 | DONE | maldives, mali, malta, marshall-islands, mauritania, mauritius, micronesia, moldova, monaco, mongolia, montenegro, mozambique, myanmar, namibia, nauru, nepal, netherlands, nicaragua, niger, north-korea, north-macedonia, norway, oman, palau, palestine to Ireland. 6 Jun 2026. |
| R12 | A | A | 25 | DONE | panama, papua-new-guinea, paraguay, peru, poland, qatar, romania, russia, rwanda, saint-kitts-and-nevis, saint-lucia, saint-vincent-and-the-grenadines, samoa, san-marino, sao-tome-and-principe, saudi-arabia, senegal, serbia, seychelles, sierra-leone, slovakia, slovenia, solomon-islands, somalia, south-sudan to Ireland. 6 Jun 2026. |
| R13 | A | A | 28 | DONE | hong-kong, south-korea, sudan, suriname, sweden, switzerland, syria, taiwan, tajikistan, tanzania, timor-leste, togo, tonga, trinidad-and-tobago, tunisia, turkmenistan, tuvalu, uganda, ukraine, united-kingdom, uruguay, uzbekistan, vanuatu, vatican-city, venezuela, yemen, zambia, zimbabwe to Ireland. Tier A complete (394 routes). 7 Jun 2026. |
| R14 | B | D | 25 | DONE | Top 25 diaspora corridors to United States: mexico, philippines, india, china, el-salvador, dominican-republic, vietnam, cuba, south-korea, guatemala, jamaica, haiti, colombia, nigeria, pakistan, brazil, honduras, ecuador, ethiopia, ghana, ukraine, iran, peru, cambodia, trinidad-and-tobago. 7 Jun 2026. |
| R15 | B | D | 25 | DONE | 12 routes to UAE (india, pakistan, bangladesh, philippines, egypt, nepal, sri-lanka, jordan, kenya, ethiopia, indonesia, morocco) and 13 routes to Saudi Arabia (pakistan, india, bangladesh, philippines, indonesia, egypt, nepal, ethiopia, jordan, kenya, sri-lanka, ghana, nigeria). 7 Jun 2026. |
| R16 | B | D | 25 | DONE | 13 routes to Germany (turkey, poland, russia, romania, italy, serbia, ukraine, iraq, morocco, ghana, nigeria, vietnam, afghanistan) and 12 routes to France (morocco, algeria, tunisia, portugal, senegal, ivory-coast, cameroon, mali, guinea, congo, madagascar, haiti). 7 Jun 2026. |
| R17 | B | D | 25 | DONE | 8 routes to Canada (india, philippines, china, pakistan, nigeria, ukraine, south-korea, iran), 9 routes to Australia (india, china, philippines, vietnam, malaysia, south-korea, new-zealand, indonesia, nepal), 8 routes to India (bangladesh, nepal, singapore, malaysia, united-states, canada, australia, united-arab-emirates). 7 Jun 2026. |
| R18 | B | D | 25 | DONE | Qatar (india, pakistan, bangladesh, philippines, nepal, egypt, sri-lanka, ethiopia, indonesia, kenya), Kuwait (india, pakistan, bangladesh, philippines, egypt, sri-lanka, nepal, ethiopia), Singapore (india, china, malaysia, philippines, bangladesh, indonesia, myanmar). 8 Jun 2026. |
| R19 | B | D | 25 | DONE | South Africa (zimbabwe, mozambique, lesotho, malawi, zambia, drc, tanzania, botswana, namibia, nigeria, ghana, kenya, ethiopia, angola, cameroon), USA second wave (bangladesh, turkey, egypt, poland, morocco, indonesia, kenya, senegal, laos, ivory-coast). 8 Jun 2026. |
| R20 | B | D | 25 | DONE | UAE second wave (turkey, ghana, nigeria, south-korea, china, vietnam, iraq, afghanistan), Germany second wave (india, bangladesh, china, spain, portugal, algeria, tunisia, pakistan), France second wave (nigeria, burkina-faso, guinea-bissau, niger, chad, mauritania, togo, benin, gabon). 8 Jun 2026. |
| R21 | B | D | 25 | DONE | Canada second wave (bangladesh, ghana, jamaica, trinidad-and-tobago, kenya, ethiopia, mexico, vietnam, iraq), Australia second wave (bangladesh, pakistan, myanmar, fiji, sri-lanka, singapore, kenya, ghana), India second wave (pakistan, china, sri-lanka, thailand, japan, kenya, nigeria, indonesia). 8 Jun 2026. |
| R22 | B | D | 25 | DONE | New Tier B hubs introduced: Italy x7 (morocco, romania, albania, china, ukraine, philippines, bangladesh), Spain x7 (morocco, romania, colombia, venezuela, ecuador, china, bolivia), Netherlands x6 (turkey, morocco, suriname, indonesia, china, india), Belgium x5 (morocco, democratic-republic-of-the-congo, turkey, rwanda, india). 8 Jun 2026. |
| R23 | B | D | 25 | DONE | Italy wave 2 x5 (egypt, india, pakistan, senegal, nigeria), Spain wave 2 x5 (ukraine, nigeria, pakistan, peru, dominican-republic), Netherlands wave 2 x5 (iraq, afghanistan, pakistan, ukraine, egypt), Belgium wave 2 x5 (cameroon, ethiopia, senegal, nigeria, pakistan), USA wave 3 x5 (somalia, venezuela, afghanistan, nepal, myanmar). 8 Jun 2026. |
| R24 | B | D | 25 | DONE | UAE wave 3 x5 (malaysia, senegal, cameroon, myanmar, tanzania), Germany wave 3 x5 (greece, iran, egypt, hungary, bulgaria), France wave 3 x5 (democratic-republic-of-the-congo, rwanda, comoros, vietnam, china), Canada wave 3 x5 (morocco, afghanistan, egypt, sri-lanka, malaysia), Australia wave 3 x5 (cambodia, laos, thailand, zimbabwe, nigeria). 8 Jun 2026. |
| R25 | B | D | 25 | DONE | India wave 3 x5 (myanmar, afghanistan, iran, south-korea, philippines), Singapore wave 2 x5 (vietnam, south-korea, thailand, pakistan, sri-lanka), Qatar wave 2 x5 (turkey, ghana, nigeria, jordan, malaysia), Kuwait wave 2 x5 (kenya, indonesia, vietnam, ghana, nigeria), South Africa wave 2 x5 (senegal, south-korea, china, india, pakistan). 8 Jun 2026. |
| R26 | B | D | 25 | DONE | Switzerland x5 (turkey, portugal, italy, germany, india), Sweden x5 (syria, somalia, iraq, poland, afghanistan), Norway x5 (poland, somalia, pakistan, india, philippines), Portugal x5 (brazil, angola, mozambique, cabo-verde, guinea-bissau), extra waves x5 (turkey-france, iraq-france, ghana-netherlands, ghana-spain, kenya-netherlands). 9 Jun 2026. |
| R27 | B | D | 25 | DONE | Switzerland wave 2 x5 (france, spain, morocco, eritrea, pakistan), Sweden wave 2 x5 (turkey, iran, eritrea, ethiopia, bosnia-and-herzegovina), Norway wave 2 x5 (iraq, iran, vietnam, eritrea, ethiopia), Portugal wave 2 x5 (france, spain, india, china, venezuela), additional Tier B x5 (eritrea-italy, ethiopia/kenya/senegal/cameroon-germany). 9 Jun 2026. |
| R28 | B | D | 25 | DONE | Spain wave 3 x5 (argentina, cuba, brazil, philippines, senegal), Netherlands wave 3 x5 (nigeria, bangladesh, vietnam, somalia, eritrea), Italy wave 3 x5 (ecuador, peru, ghana, tunisia, ivory-coast), Belgium wave 3 x5 (algeria, ivory-coast, ghana, poland, vietnam), Saudi Arabia wave 2 x5 (somalia, iraq, yemen, turkey, sudan). 9 Jun 2026. |
| R29 | B | D | 25 | DONE | Germany wave 4 x5 (syria, lebanon, jordan, indonesia, philippines), France wave 4 x5 (ghana, lebanon, pakistan, india, bangladesh), UAE wave 4 x5 (iran, lebanon, oman, eritrea, sudan), Canada wave 4 x5 (colombia, ecuador, peru, brazil, haiti), Australia wave 5 x5 (japan, south-africa, tonga, papua-new-guinea, ukraine). 10 Jun 2026. |
| R30 | B | D | 25 | DONE | Qatar wave 3 x5 (vietnam, china, iran, morocco, somalia), Kuwait wave 3 x5 (jordan, malaysia, china, turkey, iran), Singapore wave 3 x5 (japan, nepal, cambodia, hong-kong, laos), South Africa wave 3 x5 (somalia, rwanda, burundi, eritrea, ivory-coast), USA wave 4 x5 (russia, lebanon, eritrea, iraq, syria). 10 Jun 2026. |
| R31 | B | D | 25 | DONE | Switzerland wave 3 x5 (egypt, chile, colombia, brazil, china), Sweden wave 3 x5 (nigeria, kenya, morocco, tunisia, china), Norway wave 3 x5 (nigeria, kenya, morocco, turkey, china), Portugal wave 3 x5 (morocco, guinea, senegal, nigeria, turkey), Saudi Arabia wave 3 x5 (malaysia, vietnam, china, eritrea, iran). 10 Jun 2026. |
| R32 | B | D | 25 | DONE | New hub Japan x8 (china, south-korea, philippines, vietnam, india, myanmar, indonesia, brazil), new hub New Zealand x7 (india, china, philippines, fiji, samoa, tonga, south-korea), Belgium wave 4 x5 (france, kenya, eritrea, burkina-faso, lebanon), Germany wave 5 x5 (ivory-coast, mali, togo, guinea, somalia). 10 Jun 2026. |
| R33 | B | D | 25 | DONE | Japan wave 2 x5 (nepal, thailand, cambodia, malaysia, bangladesh), New Zealand wave 2 x5 (indonesia, vietnam, myanmar, pakistan, malaysia), Italy wave 4 x5 (turkey, kenya, ethiopia, cameroon, algeria), Spain wave 4 x5 (turkey, kenya, ethiopia, cameroon, algeria), Netherlands wave 4 x5 (iran, russia, poland, south-korea, colombia). 10 Jun 2026. |
| R34 | B | D | 25 | DONE | Portugal wave 4 x5 (bangladesh, kenya, pakistan, ivory-coast, cameroon), Switzerland wave 4 x5 (afghanistan, kenya, poland, algeria, russia), Sweden wave 4 x5 (india, bangladesh, south-korea, russia, vietnam), Norway wave 4 x5 (russia, bangladesh, ukraine, south-korea, cambodia), Saudi Arabia wave 4 x5 (oman, lebanon, senegal, cameroon, mali). 10 Jun 2026. |
| R35 | B | D | 25 | DONE | Greece wave 1 x5 (albania, bulgaria, romania, pakistan, india), Austria wave 1 x5 (turkey, serbia, romania, india, china), Denmark wave 1 x5 (turkey, somalia, poland, iraq, pakistan), France wave 5 x5 (egypt, indonesia, philippines, eritrea, angola), Germany wave 6 x5 (south-korea, georgia, armenia, azerbaijan, uzbekistan). 11 Jun 2026. |
| R36 | B | D | 25 | DONE | Finland wave 1 x5 (iraq, somalia, russia, india, turkey), UAE wave 5 x5 (russia, uzbekistan, algeria, somalia, angola), Canada wave 5 x5 (turkey, russia, jordan, romania, eritrea), Australia wave 5 x5 (iraq, iran, turkey, egypt, jordan), Belgium wave 5 x5 (china, indonesia, philippines, brazil, guinea). 11 Jun 2026. |
| R37 | B | D | 25 | DONE | Greece wave 2 x5 (egypt, turkey, nigeria, bangladesh, morocco), Austria wave 2 x5 (pakistan, ukraine, afghanistan, egypt, morocco), Denmark wave 2 x5 (afghanistan, india, vietnam, morocco, nigeria), Finland wave 2 x5 (afghanistan, vietnam, ethiopia, kenya, china), New Zealand wave 3 x5 (nepal, bangladesh, kenya, nigeria, sri-lanka). 11 Jun 2026. |
| R38 | B | D | 25 | DONE | Japan wave 3 x5 (iran, pakistan, hong-kong, sri-lanka, laos), Greece wave 3 x5 (ukraine, germany, russia, china, philippines), Austria wave 3 x5 (nigeria, philippines, russia, iran, bosnia-and-herzegovina), Denmark wave 3 x5 (iran, sri-lanka, lebanon, russia, ethiopia), Finland wave 3 x5 (iran, pakistan, nigeria, bangladesh, ukraine). 11 Jun 2026. |
| R39 | B | D | 25 | NEXT | Continue Tier B diaspora corridors: further waves to established hubs and new corridors as needed. |

When a chunk is committed, add its row here (date, tier, template, routes, corridors) in the same commit, mirroring the Pet Transport session log style.

---

## BLOG ROADMAP (Engine 3) -- runs in parallel, blog blocks only when route chunks are exhausted for the run

239 articles live. Target 500+. Blog batches are built only when the route matrix is not the priority for that run; the route matrix is the default. Each batch is 5 articles, distinct topics, checked against `site/content/blog/` for existing slugs first (no cannibalisation). Author personas rotate per CLAUDE.md.

### Next blog batches (build in order, 5 articles each)

- **Batch 27 -- Practical first-contact cluster:** who-to-call-when-someone-dies-abroad, contacting-the-british-embassy-after-death-abroad, what-happens-to-passport-after-death-abroad, next-of-kin-rights-when-someone-dies-abroad, funeral-director-abroad-what-they-do-and-how-to-choose.
- **Batch 28 -- Cause-specific cluster:** heart-attack-abroad-repatriation-and-post-mortem, road-accident-abroad-repatriation-process, drowning-abroad-inquest-and-repatriation, sudden-death-abroad-what-families-need-to-know, unexplained-death-abroad-what-happens-next.
- **Batch 29 -- Sector deep-dives:** death-in-hospital-abroad-release-procedure, death-in-a-hotel-room-abroad-what-happens, death-in-custody-abroad-uk-family-rights, death-at-a-sports-event-abroad, death-in-a-care-facility-abroad-repatriation.
- **Batch 30 onward -- Country deep-dive long-tail:** continue the "repatriation from {country} questions families ask" series for any country not yet covered, then "cost of repatriation from {country}" angle (no figures, directs to enquiry), then "how long does repatriation from {country} take". Generate the next country from `data/countries-197.json` order, skipping any slug already on disk.

The blog roadmap does not end. When the listed batches are exhausted, continue the country long-tail series above. The routine keeps building the next unbuilt unit every run; skip a run only when nothing is left to build.

---

## NEXT TASKS -- IN PRIORITY ORDER

1. **Route matrix, Tier A, chunks R1 onward** (default every run): a batch of up to 4 chunks, each 25 unbuilt routes in Tier A order. This is the priority until Tier A is complete.
2. After Tier A: continue to Tier B, then C, then D, same batch rhythm.
3. Blog batches 27 onward: built on a run where the route chunks are exhausted, or to fill out a batch once the next route chunk is already committed (the routine's skip-check will route it here).

---

## SESSION LOG

| Date | Chunk / Batch | Work Done | Routes/Pages | Notes |
|------|------|-----------|-------| ------|
| 5 Jun 2026 | Routine config | Switched to batch builds of up to 4 blocks per run, 2 runs/day, to fit the 15-run routine cap. One push per run (whole batch committed once) to avoid concurrent-deploy clobbering. Pointer-based skip (no same-day skip). Docs only (CLAUDE.md + this file). No content built this entry. | 70 (unchanged) | Instruction change only. |
| 5 Jun 2026 | Plan rebuild | Route matrix plan installed: full 197x197 tiered matrix (38,612 target), four tiers A to D, chunk ledger, autonomous rhythm. Replaces the previous stub plan that topped out at the blog roadmap. No content built this entry. | 70 (unchanged) | Build plan now at parity with Pet Transport. Chunk R1 (Tier A, Template A) is next. |
| 5 Jun 2026 | Chunks R1-R4 | Batch build: 100 new Tier A routes to United Kingdom. 4 blocks of 25 origins each. All QA clean (0 errors). 132 total UK routes now live. Next: R5 (continue Tier A to UK). | 170 (132 UK + 32 Ireland + 6 pre-matrix mixed) | R1-R4 committed in single batch. Deploy auto via build-and-publish.yml. |
| 6 Jun 2026 | Chunks R5-R8 | Batch build: 100 new Tier A routes (64 to UK, 36 to Ireland). 4 blocks of 25 each. All QA clean (0 errors on new files). UK Tier A complete (196 routes). 68 Ireland routes now live. Next: R9 (continue Ireland origins). | 270 (196 UK + 68 Ireland + 6 pre-matrix mixed) | R5-R8 committed in single batch. Deploy auto via build-and-publish.yml. |
| 6 Jun 2026 | Chunks R9-R12 | Batch build: 100 new Tier A routes to Ireland (origins costa-rica through south-sudan). All QA clean (0 errors on new files). 168 Ireland routes now live. 370 total route pairs. Tier A 370/394 built; 24 Ireland origins remaining. Next: R13. | 370 (196 UK + 168 Ireland + 6 pre-matrix mixed) | R9-R12 committed in single batch. Deploy auto via build-and-publish.yml. |
| 7 Jun 2026 | Chunk R13 | Batch build: 28 new Tier A routes to Ireland (hong-kong, south-korea, sudan, suriname, sweden, switzerland, syria, taiwan, tajikistan, tanzania, timor-leste, togo, tonga, trinidad-and-tobago, tunisia, turkmenistan, tuvalu, uganda, ukraine, united-kingdom, uruguay, uzbekistan, vanuatu, vatican-city, venezuela, yemen, zambia, zimbabwe). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). Tier A complete: 394 routes (196 to UK, 196 to Ireland, 6 pre-matrix). 398 total route pairs. Next: R14 Tier B. | 398 (196 UK + 196 Ireland + 6 pre-matrix mixed) | R13 committed as single chunk. Deploy auto via build-and-publish.yml. |
| 7 Jun 2026 | Chunks R14-R17 | Batch build: 100 new Tier B diaspora corridor routes. R14: 25 to USA (mexico, philippines, india, china, el-salvador, dominican-republic, vietnam, cuba, south-korea, guatemala, jamaica, haiti, colombia, nigeria, pakistan, brazil, honduras, ecuador, ethiopia, ghana, ukraine, iran, peru, cambodia, trinidad-and-tobago). R15: 25 to UAE and Saudi Arabia. R16: 25 to Germany and France (Turkish, Polish, Maghreb, West African corridors). R17: 25 to Canada, Australia, and India. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 498 total route pairs. Next: R18 Tier B. | 498 (196 UK + 196 Ireland + 6 pre-matrix + 100 Tier B) | R14-R17 committed in single batch. Deploy auto via build-and-publish.yml. |
| 8 Jun 2026 | Chunks R18-R21 | Batch build: 100 new Tier B diaspora corridor routes. R18: 25 routes to Qatar (10), Kuwait (8), Singapore (7). R19: 25 routes to South Africa (15) and USA second wave (10). R20: 25 routes UAE second wave (8), Germany second wave (8), France second wave (9). R21: 25 routes Canada second wave (9), Australia second wave (8), India second wave (8). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 598 total route pairs. Next: R22 Tier B. | 598 (196 UK + 196 Ireland + 6 pre-matrix + 200 Tier B) | R18-R21 committed in single batch. Deploy auto via build-and-publish.yml. |
| 8 Jun 2026 | Chunks R22-R25 | Batch build: 100 new Tier B diaspora corridor routes. R22: 25 routes introducing Italy x7, Spain x7, Netherlands x6, Belgium x5 as new Tier B hubs. R23: 25 routes Italy wave 2 x5, Spain wave 2 x5, Netherlands wave 2 x5, Belgium wave 2 x5, USA wave 3 x5 (somalia, venezuela, afghanistan, nepal, myanmar). R24: 25 routes UAE wave 3 x5, Germany wave 3 x5, France wave 3 x5, Canada wave 3 x5, Australia wave 3 x5. R25: 25 routes India wave 3 x5, Singapore wave 2 x5, Qatar wave 2 x5, Kuwait wave 2 x5, South Africa wave 2 x5. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 698 total route pairs. Next: R26 Tier B. | 698 (196 UK + 196 Ireland + 6 pre-matrix + 300 Tier B) | R22-R25 committed in single batch. Deploy auto via build-and-publish.yml. |

| 9 Jun 2026 | Chunk R26 | Batch build: 25 new Tier B diaspora corridor route pages. Four new Tier B hubs: Switzerland x5 (turkey, portugal, italy, germany, india), Sweden x5 (syria, somalia, iraq, poland, afghanistan), Norway x5 (poland, somalia, pakistan, india, philippines), Portugal x5 (brazil, angola, mozambique, cabo-verde, guinea-bissau). Extra waves x5 (turkey-france, iraq-france, ghana-netherlands, ghana-spain, kenya-netherlands). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 723 total route pairs. Next: R27 Tier B. | 723 (196 UK + 196 Ireland + 6 pre-matrix + 325 Tier B) | R26 committed as single chunk. Deploy auto via build-and-publish.yml. |
| 9 Jun 2026 | Chunks R27-R28 | Batch build: 50 new Tier B diaspora corridor route pages. R27 (25): Switzerland wave 2 x5 (france, spain, morocco, eritrea, pakistan), Sweden wave 2 x5 (turkey, iran, eritrea, ethiopia, bosnia-and-herzegovina), Norway wave 2 x5 (iraq, iran, vietnam, eritrea, ethiopia), Portugal wave 2 x5 (france, spain, india, china, venezuela), additional Tier B x5 (eritrea-italy, ethiopia/kenya/senegal/cameroon-germany). R28 (25): Spain wave 3 x5 (argentina, cuba, brazil, philippines, senegal), Netherlands wave 3 x5 (nigeria, bangladesh, vietnam, somalia, eritrea), Italy wave 3 x5 (ecuador, peru, ghana, tunisia, ivory-coast), Belgium wave 3 x5 (algeria, ivory-coast, ghana, poland, vietnam), Saudi Arabia wave 2 x5 (somalia, iraq, yemen, turkey, sudan). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 773 total route pairs. Next: R29 Tier B. | 773 (196 UK + 196 Ireland + 6 pre-matrix + 375 Tier B) | R27-R28 committed in single batch. Deploy auto via build-and-publish.yml. |
| 10 Jun 2026 | Chunks R29-R32 | Batch build: 100 new Tier B diaspora corridor route pages. R29 (25): Germany wave 4 x5, France wave 4 x5, UAE wave 4 x5, Canada wave 4 x5, Australia wave 5 x5. R30 (25): Qatar wave 3 x5, Kuwait wave 3 x5, Singapore wave 3 x5, South Africa wave 3 x5, USA wave 4 x5. R31 (25): Switzerland wave 3 x5, Sweden wave 3 x5, Norway wave 3 x5, Portugal wave 3 x5, Saudi Arabia wave 3 x5. R32 (25): new hub Japan x8, new hub New Zealand x7, Belgium wave 4 x5, Germany wave 5 x5. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 873 total route pairs. Next: R33 Tier B. | 873 (196 UK + 196 Ireland + 6 pre-matrix + 475 Tier B) | R29-R32 committed in single batch. Deploy auto via build-and-publish.yml. |
| 10 Jun 2026 | Chunks R33-R34 | Batch build: 50 new Tier B diaspora corridor route pages. R33 (25): Japan wave 2 x5 (nepal, thailand, cambodia, malaysia, bangladesh), New Zealand wave 2 x5 (indonesia, vietnam, myanmar, pakistan, malaysia), Italy wave 4 x5 (turkey, kenya, ethiopia, cameroon, algeria), Spain wave 4 x5 (turkey, kenya, ethiopia, cameroon, algeria), Netherlands wave 4 x5 (iran, russia, poland, south-korea, colombia). R34 (25): Portugal wave 4 x5 (bangladesh, kenya, pakistan, ivory-coast, cameroon), Switzerland wave 4 x5 (afghanistan, kenya, poland, algeria, russia), Sweden wave 4 x5 (india, bangladesh, south-korea, russia, vietnam), Norway wave 4 x5 (russia, bangladesh, ukraine, south-korea, cambodia), Saudi Arabia wave 4 x5 (oman, lebanon, senegal, cameroon, mali). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 923 total route pairs. Next: R35 Tier B. | 923 (196 UK + 196 Ireland + 6 pre-matrix + 525 Tier B) | R33-R34 committed in single batch. Deploy auto via build-and-publish.yml. |

---

| 11 Jun 2026 | Chunks R35-R36 | Batch build: 50 new Tier B diaspora corridor route pages. R35 (25): Greece wave 1 x5 (albania, bulgaria, romania, pakistan, india), Austria wave 1 x5 (turkey, serbia, romania, india, china), Denmark wave 1 x5 (turkey, somalia, poland, iraq, pakistan), France wave 5 x5 (egypt, indonesia, philippines, eritrea, angola), Germany wave 6 x5 (south-korea, georgia, armenia, azerbaijan, uzbekistan). R36 (25): Finland wave 1 x5 (iraq, somalia, russia, india, turkey), UAE wave 5 x5 (russia, uzbekistan, algeria, somalia, angola), Canada wave 5 x5 (turkey, russia, jordan, romania, eritrea), Australia wave 5 x5 (iraq, iran, turkey, egypt, jordan), Belgium wave 5 x5 (china, indonesia, philippines, brazil, guinea). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 973 total route pairs. Next: R37 Tier B. | 973 (196 UK + 196 Ireland + 6 pre-matrix + 575 Tier B) | R35-R36 committed in single batch. Deploy auto via build-and-publish.yml. |
| 11 Jun 2026 | Chunks R37-R38 | Batch build: 50 new Tier B diaspora corridor route pages. R37 (25): Greece wave 2 x5 (egypt, turkey, nigeria, bangladesh, morocco), Austria wave 2 x5 (pakistan, ukraine, afghanistan, egypt, morocco), Denmark wave 2 x5 (afghanistan, india, vietnam, morocco, nigeria), Finland wave 2 x5 (afghanistan, vietnam, ethiopia, kenya, china), New Zealand wave 3 x5 (nepal, bangladesh, kenya, nigeria, sri-lanka). R38 (25): Japan wave 3 x5 (iran, pakistan, hong-kong, sri-lanka, laos), Greece wave 3 x5 (ukraine, germany, russia, china, philippines), Austria wave 3 x5 (nigeria, philippines, russia, iran, bosnia-and-herzegovina), Denmark wave 3 x5 (iran, sri-lanka, lebanon, russia, ethiopia), Finland wave 3 x5 (iran, pakistan, nigeria, bangladesh, ukraine). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 1,023 total route pairs. Next: R39 Tier B. | 1,023 (196 UK + 196 Ireland + 6 pre-matrix + 625 Tier B) | R37-R38 committed in single batch. Deploy auto via build-and-publish.yml. |

---

*Last updated: 11 June 2026. The routine builds a batch of up to 4 blocks per run, autonomously, commits once, and reports live links to Slack. No approval step. Skip only when nothing is left to build.*
