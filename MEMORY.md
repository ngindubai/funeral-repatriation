# Repatriate Service -- Project Memory

> Read this file at the start of every run, alongside CLAUDE.md and BUILD-PLAN.md.
> Update the Current State, Next Tasks, and Session History sections at the end of each run.

---

## CLAUDE WORKING RULES (autonomous routine)

**This project is built by a scheduled cloud routine with no human watching. There is no approval step.**
- Build one block per run (25 routes, or one 5-article blog batch), pass the full QA gate, commit to master, post live links to Slack, stop.
- The Slack live-link post is a record of what shipped, posted after the push. It does not pause anything. The QA gate is the safety control: it must pass before any commit. If QA fails, do not commit; post the halt message and end.
- No "wait for go". No HTML preview. No stop condition: each run picks up the next unbuilt block.
- Links in the Slack record are clickable markdown hyperlinks, never bare URLs. Use /routes/[slug]/ for route pages, /blog/[slug]/ for blog articles, /repatriation-from-[country]/ for hubs.
- Deploy is automatic on push to master. Pages live within ~60 seconds.

---

## 1. Site Overview

**What it is:** A programmatic SEO lead generation website targeting UK and Irish families needing to repatriate a loved one who died abroad. Converts grief-driven search traffic into service enquiries.

**Target audience:** UK and Irish families searching in distress immediately after a death abroad; corporate travel managers; travel insurers seeking approved supplier networks.

**Primary goal:** Capture service enquiries. Every commercial-intent page has an enquiry form or phone CTA.

**Brand:** Repatriate Service. "Bringing your loved ones home."

**Final domain:** repatriateservice.com
**Current deployment:** repatriationfuneral.com (Hostinger)
**Production branch:** master (NOT main; master triggers deploy)
**Hugo config baseURL:** `https://www.repatriationfuneral.com/` -- MUST INCLUDE WWW (canonical fix, 1 Jun 2026).

**Tech stack:** Hugo v0.160.1-extended, Markdown + YAML frontmatter, TOML config (site/hugo.toml), JSON data (site/data/), GitHub Actions to live branch, Hostinger pulls live into /public_html/. Build: `hugo --gc --minify` from `site/`.

**NEVER use Surge.** Removed entirely.

**Hostinger server-dir:** `/public_html/` (confirmed May 2026).

---

## 2. Build Decisions

**Data-driven architecture:** Country content from `site/data/countries_repatriation.json`. Route data from `data/countries_repatriation.json` (238 countries, regulatory detail), `data/countries-197.json` (canonical country and slug list), `data/keyword_matrix.json` (per-corridor search demand and tier ordering).

**Route page frontmatter rule:** Do NOT include `layout:` field. Hugo auto-selects `routes/single.html`. Adding it silently skips the build. See ERRORS.md E001.

**server-dir rule:** Always `/public_html/`. See ERRORS.md E002.

**site/data/ rule:** NEVER place .md, .txt, or non-JSON files in site/data/. Hugo parses everything there as data. See ERRORS.md E006.

**baseURL rule:** ALWAYS include www. See ERRORS.md E007.

**buildFuture rule:** buildFuture = true in hugo.toml; author content with a safely past date. See ERRORS.md E012.

**Template variants:** Five A-E in site/layouts/routes/single.html, controlled by template_variant: frontmatter. Rotate across every block, no two consecutive pages sharing a variant.

**Route slug format:** `{origin-slug}-to-{destination-slug}.md`. Destination uses the full country slug (united-kingdom, ireland, united-states), not short keys.

**YMYL standards:** No safety guarantees, no prices, named dated sources only.

**FTP deploy.yml is disabled** (no-op stub). build-and-publish.yml (live branch) is the active pipeline. Do not re-enable deploy.yml.

---

## 3. Current State (13 June 2026)

| Silo | Status |
|------|--------|
| Country hubs | 238 countries published |
| City pages | 220 pages |
| Guides | 238 country guides |
| Blog | 239 articles live (target 500+) |
| Bringing ashes home | 238 countries |
| Cremation transfer | 238 countries |
| Embassy contacts | 238 countries |
| Route pairs | 1,223 of 38,612 (196 to UK, 196 to Ireland, 6 pre-matrix mixed, 825 Tier B diaspora corridors) |

**Active build:** Phase R, the route matrix. Tier A complete (394 routes). Chunks R14-R46 complete (825 Tier B routes: USA, UAE, Saudi Arabia, Germany, France, Canada, Australia, India, Qatar, Kuwait, Singapore, South Africa, Italy, Spain, Netherlands, Belgium, Switzerland, Sweden, Norway, Portugal, Japan, New Zealand, Greece, Austria, Denmark, Finland, Turkey, Malaysia, Oman, plus wave-2 through wave-7+ corridors for all hubs). Next block: chunk R47 (Tier B, Template D, continued waves). See BUILD-PLAN.md for the tier breakdown and chunk ledger.

**Note on Tier B:** The keyword_matrix.json does not contain a `tier_b_corridors` key. Tier B corridors are built by adapting the existing {origin}-to-united-kingdom.md source files, keeping origin-country regulatory content and replacing destination-specific fields (reception, consular, embassy city, FAQs). Generators: generate_tier_b.py (R14-R17), generate_r18_r21.py (R18-R21), generate_r22_r25.py (R22-R25), generate_r26_r29.py (R26-R28), generate_r29_r32.py (R29-R32), generate_r33_r34.py (R33-R34), generate_r35_r36.py (R35-R36), generate_r37_r38.py (R37-R38), generate_r39_r40.py (R39-R40), generate_r41_r42.py (R41-R42), generate_r43_r46.py (R43-R46) at repo root. Two pre-matrix origins used short slugs (usa, uae) not canonical slugs; these needed manual file creation for to-India routes. Important fix: the -- replacement must protect --- YAML delimiters (use placeholder swap). New hubs added in R22-R25: italy, spain, netherlands, belgium. New hubs added in R26: switzerland, sweden, norway, portugal. R29-R32 introduced two new hubs: japan (Narita/KIX, +81 3 3580 3311) and new-zealand (AKL/WLG/CHC, +64 4 439 8000). R35 introduced three new hubs: greece (ATH/SKG, +30 210 3681 000), austria (VIE, +43 1 90115 3775), denmark (CPH, +45 33 92 00 00). R36 introduced one new hub: finland (HEL, +358 9 1605 5555). R41 introduced two new hubs: turkey (IST/SAW, +90 312 292 2000) and malaysia (KUL, +603 8000 8000). R44 introduced one new hub: oman (MCT, Royal Oman Police clearance, Arabic death certificate translation required, Embassy of Oman in London +44 20 7225 0001). Embassy notes: German/US Embassy in Damascus closed 2012, covered from Beirut. Turkish Embassy in Damascus suspended since 2012; Syria-to-Turkey families directed to Turkish MFA in Ankara. South Africa and Germany have no direct embassy in Somalia, covered from Nairobi. Saudi Embassy in Tehran reopened March 2023. Swiss Embassy in Kabul suspended Aug 2021, Afghanistan covered from Islamabad. Austrian, Danish, and Finnish Embassies in Kabul suspended Aug 2021, all three covered from Islamabad. Norwegian Embassy covers Cambodia from Bangkok. Danish and Finnish Embassies cover Somalia from Nairobi. Kuwait Embassy covers Eritrea from Addis Ababa. NZ High Commission covers Bangladesh and Sri Lanka from New Delhi. Nepal-to-South-Africa covered from New Delhi (South African High Commission); Myanmar-to-South-Africa covered from Bangkok. Banned vocab: "comprehensive" triggered in corridor intro (EU-Armenia partnership); always use "Enhanced Partnership Agreement" not "Comprehensive and Enhanced Partnership Agreement". USA-origin files: usa-to-united-kingdom.md contains "state vital records" in timeline; all new USA-origin Tier B files must replace "vital records" with "civil records". For R47+, create new generator following generate_r43_r46.py pattern.

Full origin-to-destination square: 197 countries x 197, minus same-country pairs = 38,612 route pages. Four tiers, highest commercial intent first:

- **Tier A (394):** every origin to United Kingdom and to Ireland. The revenue tier. Complete.
- **Tier B (~1,100):** diaspora and cross-border corridors to the top 12 destination hubs. 825 built, ~275 remaining.
- **Tier C (~7,700):** regional and secondary destinations.
- **Tier D (~29,400):** long-tail completion of the square.

25 routes per block, template A-E rotation, built in `data/keyword_matrix.json` tier order. Full detail in BUILD-PLAN.md.

---

## 5. Next Tasks -- in priority order

1. **Route matrix, Tier B, chunk R47** (default every run): continued waves to established hubs and new corridors. Template rotation continues from D (last was C on R46). Create generate_r47_r50.py following the generate_r43_r46.py pattern.
2. After Tier B: Tier C, then D, same block rhythm.
3. Blog batches 27 onward (first-contact cluster, cause-specific, sector deep-dives, then open-ended country long-tail): built on any run where the next route chunk is already committed.

There is no end state for the routine. When a tier completes, move to the next. When the matrix completes, the blog long-tail continues indefinitely.

---

## 6. Author Personas

Never Gareth. James Whitfield (coordinator, route/process), Dr. Amara Osei (consular/legal/embassy), Claire Sutton (family/bereavement/FAQ), Thomas Anand (logistics/air cargo). Full table in CLAUDE.md.

---

## 7. Patterns to Follow

### Route Page Frontmatter (NO layout: field)
```yaml
---
title: "..."
description: "..."
origin_key: "..."
dest_key: "..."         # full destination slug
template_variant: "A"   # rotate A-E
date: YYYY-MM-DD         # safely past
faqs:
  - question: "..."
    answer: "..."
---
```

### Blog Article Frontmatter
```yaml
---
title: "..."
description: "..."
date: YYYY-MM-DD
slug: slug-here
author: "[persona name]"
author_title: "[persona title], Repatriate Service"
category: "[category]"
faqs:
  - question: "..."
    answer: "..."
---
```
British English, no em dashes, 2+ internal links, named persona, FAQs in frontmatter.

---

## 8. Mistakes Avoided

- Never add `layout:` to route page frontmatter.
- Never use the long Hostinger server-dir path.
- Never set `dangerous-clean-slate: true`.
- Never use Surge.
- Never place non-JSON files in site/data/.
- Never set template_variant outside A-E.
- baseURL must include www.
- Never hardcode repatriationfuneral.com URLs in layouts.
- Never commit to main; master deploys.
- **Before generating any blog batch, check site/content/blog/ for an existing slug on the same topic.** Roadmap candidate lists are not pre-checked against live content. Several earlier candidates already existed and would have cannibalised live pages.

---

## 9. Design System (Locked)

Hero image assignments: Countries `mrwashingt0n-ai-generated-9048740.jpg`, Guides `documents-desk.jpg`, Blog `support-conversation.jpg`, Cremation `airport-cargo.jpg`, Embassy `passport-stamp.jpg`, Ashes `hero.jpg`, Routes `cargo-terminal-night.jpg`.

---

## 10. Open Questions

- GSC 'Alternate page with proper canonical tag': fixed 1 Jun 2026, monitoring.
- GSC 859 not-indexed URLs: audit pending.

---

## 11. Session History

| Date | Session Summary |
|------|---------------|
| 27 May 2026 | Route Engine Turn A: /routes/ silo built, 25 route pages, deploy pipeline fixed. |
| 28 May 2026 | 7-engine install. Turn C: 23 route pages. Total 48. |
| 1 Jun 2026 | GSC canonical fix (www). GEO/LLM 4-phase. Route pages: 70. |
| 2 Jun 2026 | Engine 3 Batches 4-6: 15 articles. Deploy structural fix (deploy.yml disabled, Hostinger pulls live). |
| 5 Jun 2026 | Engine 3 Batch 26: 5 seasonal articles. Blog total 239. |
| 5 Jun 2026 | Plan rebuild to Pet Transport parity: full 197x197 route matrix (38,612 target) installed across BUILD-PLAN.md, CLAUDE.md, MEMORY.md and the HTML tracker. Approval gate removed; routine now fully autonomous (build, QA, commit, report, stop; no wait-for-go, no stop condition). Chunk R1 (Tier A, Template A) is next. No content built in this entry. |
| 5 Jun 2026 | Chunks R1-R4 (batch 1): 100 new Tier A route pages to UK. cambodia, dominican-republic, poland, china, saudi-arabia, kuwait, qatar, bahrain, malaysia, austria, croatia, czech-republic, hungary, bulgaria, netherlands, belgium, sweden, norway, switzerland, denmark, finland, romania, bangladesh, jamaica, gambia, barbados, trinidad-and-tobago, cuba, colombia, argentina, peru, chile, albania, ukraine, georgia, azerbaijan, armenia, kazakhstan, oman, nepal, myanmar, taiwan, south-korea, north-macedonia, serbia, montenegro, slovakia, slovenia, estonia, latvia, lithuania, luxembourg, iceland, malta, iran, iraq, lebanon, laos, mongolia, afghanistan, kyrgyzstan, uzbekistan, tajikistan, turkmenistan, belarus, moldova, senegal, ivory-coast, ethiopia, tanzania, uganda, zimbabwe, zambia, mozambique, botswana, namibia, malawi, rwanda, cameroon, angola, algeria, tunisia, libya, sudan, eritrea, djibouti, somalia, south-sudan, democratic-republic-of-the-congo, congo, gabon, equatorial-guinea, burundi, sierra-leone, liberia, guinea, guinea-bissau, burkina-faso, benin, togo. All QA clean. 170 total route pairs live. |
| 6 Jun 2026 | Chunks R5-R8 (batch 2): 100 new Tier A route pages (64 to UK, 36 to Ireland). UK Tier A complete at 196 routes. andorra, antigua-and-barbuda, bahamas, belize, bhutan, bolivia, bosnia-and-herzegovina, brunei, cabo-verde, central-african-republic, chad, comoros, costa-rica, dominica, ecuador, el-salvador, eswatini, fiji, grenada, guatemala, guyana, haiti, honduras, hong-kong, ireland, kiribati, liechtenstein, madagascar, maldives, mali, marshall-islands, mauritania, mauritius, micronesia, monaco, nauru, nicaragua, niger, north-korea, palau, palestine, panama, papua-new-guinea, paraguay, russia, saint-kitts-and-nevis, saint-lucia, saint-vincent-and-the-grenadines, samoa, san-marino, sao-tome-and-principe, seychelles, solomon-islands, suriname, syria, timor-leste, tonga, tuvalu, uruguay, vanuatu, vatican-city, venezuela, yemen to UK; afghanistan, albania, algeria, andorra, angola, antigua-and-barbuda, argentina, armenia, austria, azerbaijan, bahamas, bahrain, bangladesh, barbados, belarus, belgium, belize, benin, bhutan, bolivia, bosnia-and-herzegovina, botswana, brunei, bulgaria, burkina-faso, burundi, cabo-verde, cambodia, cameroon, central-african-republic, chad, chile, china, colombia, comoros, congo to Ireland. All QA clean. 270 total route pairs live. |
| 6 Jun 2026 | Chunks R9-R12 (batch 3): 100 new Tier A route pages to Ireland. costa-rica, croatia, cuba, czech-republic, democratic-republic-of-the-congo, denmark, djibouti, dominica, dominican-republic, ecuador, el-salvador, equatorial-guinea, eritrea, estonia, eswatini, ethiopia, fiji, finland, gabon, gambia, georgia, grenada, guatemala, guinea, guinea-bissau, guyana, haiti, honduras, hungary, iceland, iran, iraq, ivory-coast, jamaica, kazakhstan, kiribati, kuwait, kyrgyzstan, laos, latvia, lebanon, lesotho, liberia, libya, liechtenstein, lithuania, luxembourg, madagascar, malawi, malaysia, maldives, mali, malta, marshall-islands, mauritania, mauritius, micronesia, moldova, monaco, mongolia, montenegro, mozambique, myanmar, namibia, nauru, nepal, netherlands, nicaragua, niger, north-korea, north-macedonia, norway, oman, palau, palestine, panama, papua-new-guinea, paraguay, peru, poland, qatar, romania, russia, rwanda, saint-kitts-and-nevis, saint-lucia, saint-vincent-and-the-grenadines, samoa, san-marino, sao-tome-and-principe, saudi-arabia, senegal, serbia, seychelles, sierra-leone, slovakia, slovenia, solomon-islands, somalia, south-sudan to Ireland. All QA clean (0 errors on new files; 36 pre-existing route failures unchanged). 370 total route pairs live. |
| 7 Jun 2026 | Chunk R13: 28 new Tier A route pages to Ireland. hong-kong, south-korea, sudan, suriname, sweden, switzerland, syria, taiwan, tajikistan, tanzania, timor-leste, togo, tonga, trinidad-and-tobago, tunisia, turkmenistan, tuvalu, uganda, ukraine, united-kingdom, uruguay, uzbekistan, vanuatu, vatican-city, venezuela, yemen, zambia, zimbabwe to Ireland. Tier A complete (394 routes: 196 UK + 196 Ireland + 2 pre-matrix). All QA clean (0 errors on new files; 36 pre-existing route failures unchanged). 398 total route pairs live. |
| 7 Jun 2026 | Chunks R14-R17: 100 new Tier B diaspora corridor route pages. R14 (25 to USA): mexico, philippines, india, china, el-salvador, dominican-republic, vietnam, cuba, south-korea, guatemala, jamaica, haiti, colombia, nigeria, pakistan, brazil, honduras, ecuador, ethiopia, ghana, ukraine, iran, peru, cambodia, trinidad-and-tobago. R15 (25 to UAE+SA): india/pakistan/bangladesh/philippines/egypt/nepal/sri-lanka/jordan/kenya/ethiopia/indonesia/morocco to UAE; pakistan/india/bangladesh/philippines/indonesia/egypt/nepal/ethiopia/jordan/kenya/sri-lanka/ghana/nigeria to Saudi Arabia. R16 (25 to DE+FR): turkey/poland/russia/romania/italy/serbia/ukraine/iraq/morocco/ghana/nigeria/vietnam/afghanistan to Germany; morocco/algeria/tunisia/portugal/senegal/ivory-coast/cameroon/mali/guinea/congo/madagascar/haiti to France. R17 (25 to CA+AU+IN): india/philippines/china/pakistan/nigeria/ukraine/south-korea/iran to Canada; india/china/philippines/vietnam/malaysia/south-korea/new-zealand/indonesia/nepal to Australia; bangladesh/nepal/singapore/malaysia/united-states/canada/australia/united-arab-emirates to India. All QA clean (0 errors on new files; 36 pre-existing route failures unchanged). 498 total route pairs live. |
| 8 Jun 2026 | Chunks R18-R21: 100 new Tier B diaspora corridor route pages. R18 (25): Qatar x10 (india/pakistan/bangladesh/philippines/nepal/egypt/sri-lanka/ethiopia/indonesia/kenya), Kuwait x8 (india/pakistan/bangladesh/philippines/egypt/sri-lanka/nepal/ethiopia), Singapore x7 (india/china/malaysia/philippines/bangladesh/indonesia/myanmar). R19 (25): South Africa x15 (zimbabwe/mozambique/lesotho/malawi/zambia/drc/tanzania/botswana/namibia/nigeria/ghana/kenya/ethiopia/angola/cameroon), USA second wave x10 (bangladesh/turkey/egypt/poland/morocco/indonesia/kenya/senegal/laos/ivory-coast). R20 (25): UAE second wave x8 (turkey/ghana/nigeria/south-korea/china/vietnam/iraq/afghanistan), Germany second wave x8 (india/bangladesh/china/spain/portugal/algeria/tunisia/pakistan), France second wave x9 (nigeria/burkina-faso/guinea-bissau/niger/chad/mauritania/togo/benin/gabon). R21 (25): Canada second wave x9 (bangladesh/ghana/jamaica/trinidad-and-tobago/kenya/ethiopia/mexico/vietnam/iraq), Australia second wave x8 (bangladesh/pakistan/myanmar/fiji/sri-lanka/singapore/kenya/ghana), India second wave x8 (pakistan/china/sri-lanka/thailand/japan/kenya/nigeria/indonesia). All QA clean (0 errors on new files; 36 pre-existing route failures unchanged). 598 total route pairs live. |
| 8 Jun 2026 | Chunks R22-R25: 100 new Tier B diaspora corridor route pages. Introduced four new Tier B hubs: Italy, Spain, Netherlands, Belgium. R22 (25): Italy x7 (morocco/romania/albania/china/ukraine/philippines/bangladesh), Spain x7 (morocco/romania/colombia/venezuela/ecuador/china/bolivia), Netherlands x6 (turkey/morocco/suriname/indonesia/china/india), Belgium x5 (morocco/drc/turkey/rwanda/india). R23 (25): Italy wave 2 x5 (egypt/india/pakistan/senegal/nigeria), Spain wave 2 x5 (ukraine/nigeria/pakistan/peru/dominican-republic), Netherlands wave 2 x5 (iraq/afghanistan/pakistan/ukraine/egypt), Belgium wave 2 x5 (cameroon/ethiopia/senegal/nigeria/pakistan), USA wave 3 x5 (somalia/venezuela/afghanistan/nepal/myanmar). R24 (25): UAE wave 3 x5 (malaysia/senegal/cameroon/myanmar/tanzania), Germany wave 3 x5 (greece/iran/egypt/hungary/bulgaria), France wave 3 x5 (drc/rwanda/comoros/vietnam/china), Canada wave 3 x5 (morocco/afghanistan/egypt/sri-lanka/malaysia), Australia wave 3 x5 (cambodia/laos/thailand/zimbabwe/nigeria). R25 (25): India wave 3 x5 (myanmar/afghanistan/iran/south-korea/philippines), Singapore wave 2 x5 (vietnam/south-korea/thailand/pakistan/sri-lanka), Qatar wave 2 x5 (turkey/ghana/nigeria/jordan/malaysia), Kuwait wave 2 x5 (kenya/indonesia/vietnam/ghana/nigeria), South Africa wave 2 x5 (senegal/south-korea/china/india/pakistan). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 698 total route pairs live. |
| 9 Jun 2026 | Chunk R26: 25 new Tier B diaspora corridor route pages. Introduced four new Tier B hubs: Switzerland, Sweden, Norway, Portugal. Switzerland x5: turkey, portugal, italy, germany, india. Sweden x5: syria, somalia, iraq, poland, afghanistan. Norway x5: poland, somalia, pakistan, india, philippines. Portugal x5: brazil, angola, mozambique, cabo-verde, guinea-bissau. Extra waves x5: turkey-france, iraq-france, ghana-netherlands, ghana-spain, kenya-netherlands. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 723 total route pairs live. Generator: generate_r26_r29.py. |
| 9 Jun 2026 | Chunks R27-R28: 50 new Tier B diaspora corridor route pages. R27 (25): Switzerland wave 2 (france, spain, morocco, eritrea, pakistan), Sweden wave 2 (turkey, iran, eritrea, ethiopia, bosnia-and-herzegovina), Norway wave 2 (iraq, iran, vietnam, eritrea, ethiopia), Portugal wave 2 (france, spain, india, china, venezuela), additional Tier B (eritrea-italy, ethiopia/kenya/senegal/cameroon-germany). R28 (25): Spain wave 3 (argentina, cuba, brazil, philippines, senegal), Netherlands wave 3 (nigeria, bangladesh, vietnam, somalia, eritrea), Italy wave 3 (ecuador, peru, ghana, tunisia, ivory-coast), Belgium wave 3 (algeria, ivory-coast, ghana, poland, vietnam), Saudi Arabia wave 2 (somalia, iraq, yemen, turkey, sudan). New DEST_META added: germany, italy, belgium, saudi-arabia. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 773 total route pairs live. Generator: generate_r26_r29.py (extended). |
| 10 Jun 2026 | Chunks R33-R34: 50 new Tier B diaspora corridor route pages. R33 (25): Japan wave 2 x5 (nepal, thailand, cambodia, malaysia, bangladesh), New Zealand wave 2 x5 (indonesia, vietnam, myanmar, pakistan, malaysia), Italy wave 4 x5 (turkey, kenya, ethiopia, cameroon, algeria), Spain wave 4 x5 (turkey, kenya, ethiopia, cameroon, algeria), Netherlands wave 4 x5 (iran, russia, poland, south-korea, colombia). R34 (25): Portugal wave 4 x5 (bangladesh, kenya, pakistan, ivory-coast, cameroon), Switzerland wave 4 x5 (afghanistan, kenya, poland, algeria, russia), Sweden wave 4 x5 (india, bangladesh, south-korea, russia, vietnam), Norway wave 4 x5 (russia, bangladesh, ukraine, south-korea, cambodia), Saudi Arabia wave 4 x5 (oman, lebanon, senegal, cameroon, mali). Generator: generate_r33_r34.py. New embassy notes: Swiss Embassy covers Afghanistan from Islamabad; Norwegian Embassy covers Cambodia from Bangkok. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 923 total route pairs live. |
| 11 Jun 2026 | Chunks R35-R36: 50 new Tier B diaspora corridor route pages. R35 (25): Greece wave 1 x5 (albania, bulgaria, romania, pakistan, india), Austria wave 1 x5 (turkey, serbia, romania, india, china), Denmark wave 1 x5 (turkey, somalia, poland, iraq, pakistan), France wave 5 x5 (egypt, indonesia, philippines, eritrea, angola), Germany wave 6 x5 (south-korea, georgia, armenia, azerbaijan, uzbekistan). R36 (25): Finland wave 1 x5 (iraq, somalia, russia, india, turkey), UAE wave 5 x5 (russia, uzbekistan, algeria, somalia, angola), Canada wave 5 x5 (turkey, russia, jordan, romania, eritrea), Australia wave 5 x5 (iraq, iran, turkey, egypt, jordan), Belgium wave 5 x5 (china, indonesia, philippines, brazil, guinea). Generator: generate_r35_r36.py. New hubs: greece (ATH/SKG), austria (VIE), denmark (CPH), finland (HEL). Embassy notes: Danish and Finnish Embassies cover Somalia from Nairobi. Fixed: "comprehensive" banned vocab in corridor intro (EU-Armenia partnership); replaced with "Enhanced Partnership Agreement". All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 973 total route pairs live. |
| 11 Jun 2026 | Chunks R37-R38: 50 new Tier B diaspora corridor route pages. R37 (25): Greece wave 2 x5 (egypt, turkey, nigeria, bangladesh, morocco), Austria wave 2 x5 (pakistan, ukraine, afghanistan, egypt, morocco), Denmark wave 2 x5 (afghanistan, india, vietnam, morocco, nigeria), Finland wave 2 x5 (afghanistan, vietnam, ethiopia, kenya, china), New Zealand wave 3 x5 (nepal, bangladesh, kenya, nigeria, sri-lanka). R38 (25): Japan wave 3 x5 (iran, pakistan, hong-kong, sri-lanka, laos), Greece wave 3 x5 (ukraine, germany, russia, china, philippines), Austria wave 3 x5 (nigeria, philippines, russia, iran, bosnia-and-herzegovina), Denmark wave 3 x5 (iran, sri-lanka, lebanon, russia, ethiopia), Finland wave 3 x5 (iran, pakistan, nigeria, bangladesh, ukraine). Generator: generate_r37_r38.py. Embassy notes added: Austrian/Danish/Finnish Embassies cover Afghanistan from Islamabad (all suspended Kabul Aug 2021); NZ High Commission covers Bangladesh and Sri Lanka from New Delhi. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 1,023 total route pairs live. |
| 12 Jun 2026 | Chunks R39-R40: 50 new Tier B diaspora corridor route pages. R39 (25): Japan wave 4 x5 (usa, australia, france, germany, italy), New Zealand wave 4 x5 (australia, usa, south-africa, canada, hong-kong), Greece wave 4 x5 (georgia, serbia, north-macedonia, ethiopia, iran), Austria wave 4 x5 (hungary, croatia, slovakia, czech-republic, albania), Denmark wave 4 x5 (china, ghana, kenya, bangladesh, eritrea). R40 (25): Finland wave 4 x5 (ghana, eritrea, morocco, indonesia, senegal), Singapore wave 4 x5 (australia, usa, south-africa, kenya, nigeria), South Africa wave 4 x5 (france, usa, germany, australia, netherlands), Saudi Arabia wave 5 x5 (morocco, ivory-coast, burkina-faso, togo, djibouti), USA wave 5 x5 (japan, argentina, south-africa, georgia, tanzania). Generator: generate_r39_r40.py. Embassy notes: Danish/Finnish Embassies cover Eritrea from Addis Ababa. Fixed: banned word 'vital' in USA-origin files (replaced 'state vital records' with 'state civil records'). All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 1,073 total route pairs live. |
| 12 Jun 2026 | Chunks R41-R42: 50 new Tier B diaspora corridor route pages. R41 (25): Kuwait wave 4 x5 (cameroon, senegal, myanmar, iraq, eritrea), Qatar wave 4 x5 (cameroon, senegal, myanmar, iraq, oman), India wave 4 x5 (vietnam, egypt, france, germany, ghana), Turkey wave 1 NEW HUB x5 (syria, iraq, iran, azerbaijan, georgia), Malaysia wave 1 NEW HUB x5 (indonesia, bangladesh, philippines, myanmar, india). R42 (25): Turkey wave 2 x5 (pakistan, egypt, germany, morocco, ukraine), Malaysia wave 2 x5 (china, vietnam, nepal, thailand, cambodia), South Africa wave 5 x5 (japan, italy, spain, brazil, portugal), Saudi Arabia wave 6 x5 (niger, guinea, benin, gambia, liberia), UAE wave 6 x5 (djibouti, togo, mali, comoros, turkmenistan). Generator: generate_r41_r42.py. New hubs: turkey (IST/SAW, +90 312 292 2000) and malaysia (KUL, +603 8000 8000). Embassy notes: Turkish Embassy in Damascus suspended since 2012; Syria-to-Turkey families directed to Turkish MFA in Ankara. Kuwait Embassy covers Eritrea from Addis Ababa. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 1,123 total route pairs live. |
| 13 Jun 2026 | Chunks R43-R46: 100 new Tier B diaspora corridor route pages. R43 (25): Turkey wave 3 x5 (russia, saudi-arabia, jordan, algeria, china), Malaysia wave 3 x5 (sri-lanka, pakistan, south-korea, laos, hong-kong), India wave 5 x5 (iraq, russia, jordan, turkey, ethiopia), Singapore wave 5 x5 (ethiopia, ghana, morocco, turkey, iraq), Kuwait wave 5 x5 (russia, algeria, morocco, uzbekistan, ukraine). R44 (25): South Africa wave 6 x5 (ukraine, russia, indonesia, bangladesh, egypt), USA wave 6 x5 (jordan, algeria, uzbekistan, nicaragua, costa-rica), Germany wave 7 x5 (thailand, myanmar, south-africa, brazil, colombia), France wave 6 x5 (ethiopia, kenya, sri-lanka, nepal, myanmar), Oman wave 1 NEW HUB x5 (india, pakistan, bangladesh, nepal, philippines). R45 (25): Turkey wave 4 x5 (nigeria, ghana, kenya, ethiopia, bangladesh), Malaysia wave 4 x5 (nigeria, ghana, kenya, ethiopia, saudi-arabia), Oman wave 2 x5 (ethiopia, kenya, sri-lanka, indonesia, egypt), Switzerland wave 5 x5 (nigeria, iran, bangladesh, indonesia, vietnam), Sweden wave 5 x5 (ghana, senegal, pakistan, ukraine, indonesia). R46 (25): Norway wave 5 x5 (ghana, senegal, indonesia, egypt, algeria), Oman wave 3 x5 (turkey, iraq, iran, jordan, morocco), South Africa wave 7 x5 (malaysia, vietnam, philippines, nepal, myanmar), Portugal wave 5 x5 (ghana, ethiopia, iraq, egypt, algeria), Japan wave 5 x5 (south-africa, nigeria, ghana, ethiopia, kenya). Generator: generate_r43_r46.py. New hub: oman (MCT, Royal Oman Police clearance, Arabic translation required, Embassy of Oman in London +44 20 7225 0001). Embassy notes: Nepal-to-South-Africa covered from New Delhi; Myanmar-to-South-Africa covered from Bangkok. All QA clean (0 errors on new files; 36 pre-existing failures unchanged). 1,223 total route pairs live. |
