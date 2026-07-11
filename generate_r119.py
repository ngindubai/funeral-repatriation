#!/usr/bin/env python3
"""
generate_r119.py -- Repatriate Service Route Generator
Chunk R119: 34 Tier C route pages, closing the origin-pool fill-out phase
begun in R112. Every Tier C "single wave" destination introduced between
R97 and R110 was originally given only 5 of the 8 established origins
(Australia, France, Canada, Netherlands, Italy, Norway, Sweden, Belgium),
missing exactly 3 each. R118 completed Benin through Kiribati to full
8/8 and gave Samoa 2 of its 3 missing origins (Norway, Sweden), leaving
Samoa's last origin (Belgium) plus all of Tonga (the last two R107-R108
destinations), and the ten R109-R110 destinations (Belarus, Marshall
Islands, Micronesia, Nauru, North Korea, Palau, Solomon Islands,
Timor-Leste, Tuvalu, Vanuatu) still at 5/8 each.

A direct filesystem audit of site/content/routes/ against the 8-origin
pool, run immediately before this generator was written, confirmed
exactly 34 routes remained across these 12 destinations: 1 for Samoa,
3 for Tonga, and 3 each for the ten R109-R110 destinations. This
generator builds all 34 in one chunk, closing the R97-R110 origin-pool
fill-out phase entirely. A fresh audit (also run before this generator,
see BUILD-PLAN.md) found no other Tier C "single wave" destination with
partial 8-pool coverage outside this list, and no other class of
missing-origin gap in the wider route matrix, so no further fill-out
chunk is needed after this one.

No new destination research was required: every fact below is reused
verbatim from the generator that originally introduced that destination
(generate_r107_r108.py for Samoa and Tonga, generate_r109_r110.py for
Belarus through Vanuatu), each itself sourced from the HCCH Apostille
status table, national civil registry sites, and GOV.UK British
Embassy/High Commission pages, checked July 2026.

Origins (unchanged pool): Australia, France, Canada, Netherlands, Italy,
Norway, Sweden, Belgium.

Template variants: R118 ended at index 1 (B), 25 routes from a start of
2. R119 starts at C (index 2), 34 routes, ending at index 0 (A). No two
consecutive pages share a variant.
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r117_r118.py)
# ---------------------------------------------------------------------------

ORIGIN_DATA = {
    "australia": {
        "name": "Australia",
        "slug": "australia",
        "airport": "Sydney (SYD), Melbourne (MEL), Brisbane (BNE), Perth (PER), or other major Australian airport",
        "emergency": "000 (police, fire, ambulance)",
        "death_cert": "death certificate (state or territory Births, Deaths and Marriages registry)",
        "registry": "state or territory Births, Deaths and Marriages (BDM) registry",
        "language": "English",
        "apostille": True,
        "apostille_year": "1995",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Canberra",
        "embassy_note": "The British High Commission in Canberra can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 000 for emergency services. Death is certified by a registered medical practitioner and registered with the state or territory Births, Deaths and Marriages (BDM) registry. The coroner takes jurisdiction for sudden, violent, or unexplained deaths. Australia is a Hague Apostille Convention member since 1995. Death certificates are issued in English. The British High Commission in Canberra can assist British nationals. (DFAT Smartraveller Australia 2025; FCDO Travel Advice Australia 2025.)",
        "police_note": "The coroner takes jurisdiction for sudden, violent, or unexplained deaths. Body release may be delayed until the coroner authorises it.",
        "source": "DFAT Smartraveller Australia 2025; state BDM registry procedures 2025; Hague Conference Australia profile 1995",
        "translation_note": "Death certificates are issued in English. No translation is required for English-speaking destinations. Certified translation may be required for non-English-speaking destinations.",
    },
    "france": {
        "name": "France",
        "slug": "france",
        "airport": "Paris Charles de Gaulle (CDG), Paris Orly (ORY), Lyon Saint-Exupery (LYS), or other major French airport",
        "emergency": "15 (SAMU medical), 17 (police), 18 (fire), 112 (Europe-wide)",
        "death_cert": "acte de deces (death certificate from the local mairie)",
        "registry": "local mairie (town hall) or commune civil registration office",
        "language": "French",
        "apostille": True,
        "apostille_year": "1960",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Paris",
        "embassy_note": "The British Embassy in Paris can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 15 (SAMU), 17 (police), or 112 for emergency services. Death is registered at the local mairie (town hall) within 24 hours. The official death certificate is the acte de deces. The Procureur de la Republique (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths. France is a Hague Apostille Convention member since 1960. Death certificates are issued in French. The British Embassy in Paris can assist British nationals. (FCDO Travel Advice France 2025; French Ministry of Justice civil registration procedures 2025.)",
        "police_note": "The Procureur de la Republique takes jurisdiction for violent or suspicious deaths. A judicial investigation can significantly delay body release.",
        "source": "FCDO Travel Advice France 2025; French Ministry of Justice civil registration procedures 2025; Hague Conference France profile 1960",
        "translation_note": "The acte de deces is issued in French. Certified translation into the destination country's language is required for all non-French-speaking destinations.",
    },
    "canada": {
        "name": "Canada",
        "slug": "canada",
        "airport": "Toronto Pearson (YYZ), Vancouver (YVR), Montreal (YUL), or other major Canadian airport",
        "emergency": "911",
        "death_cert": "death certificate (provincial civil registration authority)",
        "registry": "provincial civil registration authority (the civil records office for each province and territory)",
        "language": "English or French depending on province",
        "apostille": True,
        "apostille_year": "November 2024",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Ottawa",
        "embassy_note": "The British High Commission in Ottawa can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 911 for emergency services. Death is certified by a licensed physician and registered with the provincial civil registration authority. The coroner or medical examiner takes jurisdiction for sudden, violent, or unexplained deaths. Canada joined the Hague Apostille Convention in November 2024, simplifying document authentication. Death certificates are issued in English or French depending on the province. The British High Commission in Ottawa can assist British nationals. (Global Affairs Canada consular guidance 2025; Hague Conference Canada profile November 2024.)",
        "police_note": "The coroner or medical examiner investigates sudden, violent, or unexplained deaths. Body release requires coroner authorisation before repatriation can proceed.",
        "source": "Global Affairs Canada consular guidance 2025; provincial civil registration offices 2025; Hague Conference Canada profile November 2024",
        "translation_note": "Death certificates are issued in English. Documentation is issued in English or French depending on the province. Certified translation is required where needed.",
    },
    "netherlands": {
        "name": "Netherlands",
        "slug": "netherlands",
        "airport": "Amsterdam Schiphol (AMS), Rotterdam The Hague (RTM), or Eindhoven (EIN)",
        "emergency": "112",
        "death_cert": "akte van overlijden (death certificate from the local gemeente)",
        "registry": "local gemeente (municipality), Basisregistratie Personen (BRP)",
        "language": "Dutch",
        "apostille": True,
        "apostille_year": "1960",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "The Hague",
        "embassy_note": "The British Embassy in The Hague can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 for emergency services. Death is registered with the local gemeente (municipality) in the BRP (Municipal Personal Records Database). The official death certificate is the akte van overlijden. The Officier van Justitie (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths. The Netherlands is a founding Hague Apostille Convention member since 1960. The British Embassy in The Hague can assist British nationals. (FCDO Travel Advice Netherlands 2025; Dutch Ministry of Justice civil registration procedures 2025.)",
        "police_note": "The Officier van Justitie investigates violent or suspicious deaths. Body release requires formal clearance before repatriation can proceed.",
        "source": "FCDO Travel Advice Netherlands 2025; Dutch Ministry of Justice civil registration procedures 2025; Hague Conference Netherlands profile 1960",
        "translation_note": "The akte van overlijden is issued in Dutch. Certified translation is required for non-Dutch-speaking destinations.",
    },
    "italy": {
        "name": "Italy",
        "slug": "italy",
        "airport": "Rome Fiumicino (FCO), Milan Malpensa (MXP), Naples (NAP), or other major Italian airport",
        "emergency": "112 (general), 118 (medical), 113 (police)",
        "death_cert": "atto di morte (death certificate from the local Comune)",
        "registry": "local Comune (ufficio di stato civile, civil status office)",
        "language": "Italian",
        "apostille": True,
        "apostille_year": "1978",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Rome",
        "embassy_note": "The British Embassy in Rome can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 or 118 for emergency services. Death must be declared within 24 hours at the local Comune (ufficio di stato civile). The official death certificate is the atto di morte. The Procura della Repubblica (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths; a formal nulla osta is required before the body can be moved. Italy is a Hague Apostille Convention member since 1978. The British Embassy in Rome can assist British nationals. (FCDO Travel Advice Italy 2025; Italian Ministry of Interior civil registration procedures 2025.)",
        "police_note": "The Procura della Repubblica investigates violent or suspicious deaths. A formal nulla osta (judicial clearance) is required before the body can be released for repatriation.",
        "source": "FCDO Travel Advice Italy 2025; Italian Ministry of Interior civil registration procedures 2025; Hague Conference Italy profile 1978",
        "translation_note": "The atto di morte is issued in Italian. Certified translation is required for non-Italian-speaking destinations.",
    },
    "belgium": {
        "name": "Belgium",
        "slug": "belgium",
        "airport": "Brussels Airport (BRU) or Brussels South Charleroi (CRL)",
        "emergency": "112 (medical and fire), 101 (police)",
        "death_cert": "acte de deces or overlijdensakte (death certificate from the local commune or gemeenten)",
        "registry": "local commune (French-speaking areas) or gemeenten (Flemish areas), Registre National/Rijksregister",
        "language": "French, Dutch, or German depending on region",
        "apostille": True,
        "apostille_year": "1975",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Brussels",
        "embassy_note": "The British Embassy in Brussels can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 (ambulance and fire) or 101 (police) for emergency services. Death is registered with the local commune or gemeenten within 24 hours. The official death certificate is the acte de deces (French and German regions) or overlijdensakte (Flemish region). The Procureur du Roi takes jurisdiction for violent, suspicious, or unexplained deaths. Belgium is a Hague Apostille Convention member since 1975. The British Embassy in Brussels can assist British nationals. (FCDO Travel Advice Belgium 2025; Belgian FPS Home Affairs civil registration procedures 2025.)",
        "police_note": "The Procureur du Roi investigates violent or suspicious deaths. Formal clearance is required before the body can be released for repatriation.",
        "source": "FCDO Travel Advice Belgium 2025; Belgian FPS Home Affairs civil registration procedures 2025; Hague Conference Belgium profile 1975",
        "translation_note": "Documentation is issued in French, Dutch, or German depending on region. Certified translation is required where needed.",
    },
    "norway": {
        "name": "Norway",
        "slug": "norway",
        "airport": "Oslo Gardermoen (OSL), Bergen (BGO), or Stavanger (SVG)",
        "emergency": "112 (police), 113 (medical)",
        "death_cert": "dodsattest (death certificate from Folkeregisteret via Skatteetaten)",
        "registry": "Folkeregisteret (Norwegian Population Register), administered by Skatteetaten (Tax Administration)",
        "language": "Norwegian",
        "apostille": True,
        "apostille_year": "1980",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "3-6 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Oslo",
        "embassy_note": "The British Embassy in Oslo can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 (police) or 113 (ambulance) for emergency services. Death is registered with Folkeregisteret (Norwegian Population Register) via Skatteetaten. The official death certificate is the dodsattest. The Norwegian Police Service investigates violent, suspicious, or unexplained deaths. Norway is a Hague Apostille Convention member since 1980. The British Embassy in Oslo can assist British nationals. (FCDO Travel Advice Norway 2025; Norwegian Skatteetaten population register procedures 2025.)",
        "police_note": "The Norwegian Police Service investigates violent or suspicious deaths. Body release requires police clearance before repatriation can proceed.",
        "source": "FCDO Travel Advice Norway 2025; Norwegian Skatteetaten population register procedures 2025; Hague Conference Norway profile 1980",
        "translation_note": "The dodsattest is issued in Norwegian. Certified translation is required for non-Norwegian-speaking destinations.",
    },
    "sweden": {
        "name": "Sweden",
        "slug": "sweden",
        "airport": "Stockholm Arlanda (ARN), Gothenburg Landvetter (GOT), or other major Swedish airport",
        "emergency": "112",
        "death_cert": "dodsfallsintyg (death certificate from Skatteverket)",
        "registry": "Skatteverket (Swedish Tax Agency), which maintains the population register",
        "language": "Swedish",
        "apostille": True,
        "apostille_year": "1999",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "3-6 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Stockholm",
        "embassy_note": "The British Embassy in Stockholm can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 for emergency services. Death is registered with Skatteverket (the Swedish Tax Agency population register). The official death certificate is the dodsfallsintyg. The Swedish Police Authority investigates violent, suspicious, or unexplained deaths. Sweden is a Hague Apostille Convention member since 1999. The British Embassy in Stockholm can assist British nationals. (FCDO Travel Advice Sweden 2025; Swedish Skatteverket population register procedures 2025.)",
        "police_note": "The Swedish Police Authority investigates violent or suspicious deaths. Body release requires police clearance before repatriation can proceed.",
        "source": "FCDO Travel Advice Sweden 2025; Swedish Skatteverket population register procedures 2025; Hague Conference Sweden profile 1999",
        "translation_note": "The dodsfallsintyg is issued in Swedish. Certified translation is required for non-Swedish-speaking destinations.",
    },
}

# ---------------------------------------------------------------------------
# Destination data. All reused verbatim from the generator that originally
# introduced each destination (see module docstring for sourcing).
# ---------------------------------------------------------------------------

DEST_META = {
    "samoa": {
        "name": "Samoa",
        "slug": "samoa",
        "airport": "Faleolo International Airport (APW)",
        "reception": "The funeral director in Samoa takes custody at the cargo terminal at Faleolo International Airport (APW). Death is registered with Samoa Births, Deaths and Marriages Registration, with a post-mortem from TTM Hospital, Apia, where required, before the Ministry of Health issues the export permit. Samoa has been a Hague Apostille Convention member since 13 September 1999. English is an official language alongside Samoan, so death certificates and most documentation need no translation for a UK-bound case. Samoa observes Sunday strictly; official processing does not progress on that day.",
        "consular_note": "There is no resident British diplomatic post in Samoa. The New Zealand High Commission in Apia provides consular assistance under the UK-New Zealand Consular Sharing Agreement, and the British High Commission in Wellington holds formal accreditation.",
        "apostille": "Hague Apostille (1999)",
        "timeline": "18-30 days standard, add 1-2 days for deaths on Savai'i",
        "dest_key": "samoa",
    },
    "tonga": {
        "name": "Tonga",
        "slug": "tonga",
        "airport": "Fua'amotu International Airport (TBU), Tongatapu",
        "reception": "The funeral director in Tonga takes custody at the cargo terminal at Fua'amotu International Airport (TBU), Tongatapu. Death is registered with the Registrar General's Office, with a post-mortem from Vaiola Hospital where required, before the Ministry of Health issues the export permit. Tonga has been a Hague Apostille Convention member since 4 June 1970 (succession). Documentation is processed in English. Deaths in the Vava'u or Ha'apai groups need inter-island transfer first, and Vaiola Hospital has no hyperbaric decompression capacity, so diving-related incidents require medical evacuation before a repatriation case can begin.",
        "consular_note": "There is no resident British diplomatic post in Tonga. The Australian High Commission in Nuku'alofa provides consular assistance under the UK-Australia Consular Sharing Agreement, and the British High Commission in Wellington holds formal accreditation.",
        "apostille": "Hague Apostille (1970, succession)",
        "timeline": "18-30 days standard, add 1-2 days for Vava'u or Ha'apai, add 2-4 days for the Niuas",
        "dest_key": "tonga",
    },
    "belarus": {
        "name": "Belarus",
        "slug": "belarus",
        "airport": "Minsk National Airport (MSQ)",
        "reception": "The funeral director in Belarus takes custody at the cargo terminal at Minsk National Airport (MSQ). No direct flights connect most Western countries to Belarus; cargo typically routes via Warsaw, Vilnius, or Istanbul instead. Death registration is handled by the Civil Registry Department, with the Investigative Committee of Belarus clearing any non-natural death before release. Belarus has been a Hague Apostille Convention member since 1992 (succession, in force 31 May 1992). Documentation is issued in Belarusian and Russian.",
        "consular_note": "The British Embassy in Minsk operates with reduced staff following the diplomatic deterioration since 2020. The FCDO advises against all but essential travel to Belarus.",
        "apostille": "Hague Apostille (1992, succession)",
        "timeline": "Minsk cases typically add 10 to 20 days beyond the origin country's own processing, chiefly reduced embassy capacity and indirect flight routing",
        "dest_key": "belarus",
    },
    "marshall-islands": {
        "name": "Marshall Islands",
        "slug": "marshall-islands",
        "airport": "Amata Kabua International Airport (MAJ), Majuro",
        "reception": "The funeral director in the Marshall Islands takes custody at the cargo terminal at Amata Kabua International Airport (MAJ), Majuro. The Republic of the Marshall Islands comprises 29 atolls and 5 islands spread across roughly 1.9 million square kilometres of ocean; a death on an outer atoll requires boat or light aircraft transfer to Majuro before documentation can properly begin. Death registration goes through the national civil registration office, with the RMI Police Department investigating non-natural deaths. The Marshall Islands has been a Hague Apostille Convention member since 1991 (accession, in force 14 August 1992). Documentation is issued in English. Kwajalein Atoll, home to a US Army missile defence installation, follows separate US military coordination protocols. Cremation is not available; full body repatriation is required.",
        "consular_note": "There is no resident British Embassy in the Marshall Islands. Consular support comes from the non-resident British Embassy in Manila, Philippines.",
        "apostille": "Hague Apostille (1991, in force 1992)",
        "timeline": "21-56 days, longer for outer atoll cases",
        "dest_key": "marshall-islands",
    },
    "micronesia": {
        "name": "Micronesia",
        "slug": "micronesia",
        "airport": "Pohnpei International Airport (PNI), or Chuuk, Kosrae, or Yap, reached via the United Airlines Island Hopper through Guam",
        "reception": "The funeral director in the Federated States of Micronesia takes custody at the cargo terminal on whichever of the four states, Yap, Chuuk, Pohnpei, or Kosrae, received the case, all reached only through the United Airlines Island Hopper via Guam. Each state operates its own civil registration office; documentation is in English throughout, reflecting FSM's Compact of Free Association with the United States. Non-natural deaths require state police investigation and clearance. The Federated States of Micronesia is not a Hague Apostille Convention member; documents require standard legalisation. Cremation is not available anywhere in FSM; full body repatriation is required.",
        "consular_note": "There is no resident British Embassy in the Federated States of Micronesia. Consular support comes from the non-resident British Embassy in Manila, Philippines.",
        "apostille": "not a member; legalisation required",
        "timeline": "21-56 days, varies sharply by which of the four states is involved",
        "dest_key": "micronesia",
    },
    "nauru": {
        "name": "Nauru",
        "slug": "nauru",
        "airport": "Nauru International Airport (INU)",
        "reception": "The funeral director in Nauru takes custody at the cargo terminal at Nauru International Airport (INU). Nauru Airlines is the only carrier serving the island, and all international routing for a repatriation case runs via Brisbane, Australia. Death registration goes through Nauru's civil registration office, with the Nauru Police Force investigating non-natural deaths. Nauru is not a Hague Apostille Convention member; documents require standard legalisation. Mortuary and embalming capacity on the island is very limited; complex cases have historically been referred to Australia or Fiji. Cremation is not available; full body repatriation via Brisbane is required.",
        "consular_note": "There is no resident British High Commission in Nauru. Consular support comes from the non-resident British High Commission in Suva, Fiji.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days",
        "dest_key": "nauru",
    },
    "north-korea": {
        "name": "North Korea",
        "slug": "north-korea",
        "airport": "Pyongyang Sunan International Airport (FNJ)",
        "reception": "There is no standard reception process in North Korea. Air Koryo operates the only viable route, Pyongyang to Beijing, and all cargo for a repatriation case would move via Beijing. Death registration and any export authorisation are controlled entirely by North Korean state authorities, principally the Ministry of People's Security; no independent verification of documentation is possible. North Korea is not a Hague Apostille Convention member. The small number of foreign nationals present in North Korea, mostly diplomatic staff, accredited journalists, or supervised tour groups, are accompanied by state-assigned minders at all times, and any death becomes a matter North Korean authorities manage directly.",
        "consular_note": "The UK has no resident embassy in Pyongyang. The Swedish Embassy in Pyongyang provides limited consular assistance to British nationals by prior arrangement with North Korean authorities, and the British Embassy in Seoul handles UK-DPRK consular matters. The FCDO advises against all travel to North Korea.",
        "apostille": "not a member; state control of documentation makes the question moot",
        "timeline": "28-180 days where achievable at all, entirely dependent on North Korean state cooperation",
        "dest_key": "north-korea",
    },
    "palau": {
        "name": "Palau",
        "slug": "palau",
        "airport": "Roman Tmetuchl International Airport (ROR), near Koror",
        "reception": "The funeral director in Palau takes custody at the cargo terminal at Roman Tmetuchl International Airport (ROR), near Koror. There are no direct flights to the UK, Europe, or Australia; international connections run via Manila in the Philippines or Guam. Death registration is handled by Palau's civil registration authority, with the Palau Police Department investigating non-natural deaths. Palau has been a Hague Apostille Convention member since 17 October 2019 (in force 23 June 2020), which simplifies authentication for documents arriving from other member states. Embalming capacity exists in Koror but is limited in volume. Cremation is not available; full body repatriation is required.",
        "consular_note": "There is no resident British Embassy in Palau. Consular support comes from the non-resident British Embassy in Manila, Philippines.",
        "apostille": "Hague Apostille (2019, in force 2020)",
        "timeline": "14-42 days",
        "dest_key": "palau",
    },
    "solomon-islands": {
        "name": "Solomon Islands",
        "slug": "solomon-islands",
        "airport": "Honiara International Airport (HIR)",
        "reception": "The funeral director in Solomon Islands takes custody at the cargo terminal at Honiara International Airport (HIR). Connections to onward destinations run via Brisbane or Port Moresby. Death registration goes through the Registrar of Births, Deaths and Marriages, with the Royal Solomon Islands Police Force investigating non-natural deaths. Solomon Islands is not a Hague Apostille Convention member; documents require standard legalisation. English common law applies throughout, a legacy of British rule until 1978, so documentation is in English with no translation step. A death on any of the outer islands beyond Guadalcanal requires transfer to Honiara first. Cremation is not available; full body repatriation is required.",
        "consular_note": "There is no resident British High Commission in Solomon Islands. Consular support comes from the Australian High Commission in Honiara. The FCDO advises increased caution in parts of Honiara following the 2021 unrest, though the situation has since stabilised.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days",
        "dest_key": "solomon-islands",
    },
    "timor-leste": {
        "name": "Timor-Leste",
        "slug": "timor-leste",
        "airport": "Presidente Nicolau Lobato International Airport (DIL), Dili",
        "reception": "The funeral director in Timor-Leste takes custody at the cargo terminal at Presidente Nicolau Lobato International Airport (DIL), Dili. Onward connections run via Bali, Indonesia, or Darwin, Australia; there is no direct route to the UK or Europe. Death registration goes through the Civil Registration Service, with the National Police of Timor-Leste (PNTL) attending non-natural deaths. Timor-Leste is not a Hague Apostille Convention member; documents require standard legalisation. Documentation is issued in Portuguese and Tetum. Deaths in the Oecusse enclave, separated from the rest of the country by Indonesian territory, need a road transfer through West Timor or a charter flight from the enclave's own airstrip before the case can proceed.",
        "consular_note": "There is no resident British Embassy in Timor-Leste. The Australian Embassy in Dili provides consular assistance to British nationals under the UK-Australia consular sharing arrangement.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days, longer from the Oecusse enclave",
        "dest_key": "timor-leste",
    },
    "tuvalu": {
        "name": "Tuvalu",
        "slug": "tuvalu",
        "airport": "Funafuti International Airport (FUN)",
        "reception": "The funeral director in Tuvalu takes custody at the cargo terminal at Funafuti International Airport (FUN). Fiji Airways is the only international carrier, so all onward connections route through Nadi or Suva before continuing to Sydney, Singapore, or Hong Kong. Death registration goes through the Tuvalu Births, Deaths and Marriages Registry, with the Tuvalu Police Service investigating non-natural deaths. Tuvalu is not a Hague Apostille Convention member; documents require standard legalisation. A death on any of the eight outer atolls depends on the government vessel MV Nivaga III for transfer to Funafuti, a service that runs infrequently and is weather-dependent. Cremation is not available; full body repatriation is required.",
        "consular_note": "There is no resident British High Commission in Tuvalu. Consular support comes from the non-resident British High Commission in Suva, Fiji.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days, longer for outer atoll cases",
        "dest_key": "tuvalu",
    },
    "vanuatu": {
        "name": "Vanuatu",
        "slug": "vanuatu",
        "airport": "Bauerfield International Airport (VLI), Port Vila",
        "reception": "The funeral director in Vanuatu takes custody at the cargo terminal at Bauerfield International Airport (VLI), Port Vila. All onward cargo connections run via Brisbane or Sydney; there is no direct route to the UK or Europe. Death registration and any export authorisation go through Vanuatu's civil registration authority, with police investigating non-natural deaths; complex cases can require forensic assistance requested from Australia, which adds time. Vanuatu has been a Hague Apostille Convention member since 2008 (succession, recognised in force from 30 July 1980), which simplifies authentication for documents arriving from other member states. A death on Tanna, Malekula, Ambrym, or any of the other islands beyond Efate requires inter-island transfer to Port Vila first, and cyclone season, November to April, can delay that transfer.",
        "consular_note": "There is no resident British High Commission in Vanuatu. The Australian High Commission in Port Vila provides consular assistance to British nationals under the UK-Australia Consular Sharing Agreement; the British High Commission in Port Moresby, Papua New Guinea, holds formal accreditation.",
        "apostille": "Hague Apostille (2008 succession, retroactive to 1980)",
        "timeline": "21-35 days, longer during cyclone season or for outer island cases",
        "dest_key": "vanuatu",
    },
}

# ---------------------------------------------------------------------------
# Route definitions -- exact missing origin/destination combinations,
# confirmed by a direct filesystem check of site/content/routes/ against
# the 8-origin pool before this chunk was generated.
# ---------------------------------------------------------------------------

# R119: starts at template C (index 2). 34 routes.
R119_ROUTES = [
    ("belgium", "samoa"),
    ("australia", "tonga"),
    ("france", "tonga"),
    ("canada", "tonga"),
    ("norway", "belarus"),
    ("sweden", "belarus"),
    ("belgium", "belarus"),
    ("australia", "marshall-islands"),
    ("france", "marshall-islands"),
    ("canada", "marshall-islands"),
    ("netherlands", "micronesia"),
    ("italy", "micronesia"),
    ("norway", "micronesia"),
    ("australia", "nauru"),
    ("sweden", "nauru"),
    ("belgium", "nauru"),
    ("canada", "north-korea"),
    ("france", "north-korea"),
    ("netherlands", "north-korea"),
    ("italy", "palau"),
    ("norway", "palau"),
    ("sweden", "palau"),
    ("australia", "solomon-islands"),
    ("france", "solomon-islands"),
    ("belgium", "solomon-islands"),
    ("canada", "timor-leste"),
    ("netherlands", "timor-leste"),
    ("italy", "timor-leste"),
    ("norway", "tuvalu"),
    ("sweden", "tuvalu"),
    ("belgium", "tuvalu"),
    ("australia", "vanuatu"),
    ("france", "vanuatu"),
    ("canada", "vanuatu"),
]

# ---------------------------------------------------------------------------
# Varied title shapes, description openings (burstiness and
# anti-template-footprint measures per CLAUDE.md canonical constants)
# ---------------------------------------------------------------------------

TITLE_SHAPES = [
    lambda o, d: f"{o} to {d} Repatriation: Family Guidance",
    lambda o, d: f"Repatriation from {o} to {d}",
    lambda o, d: f"Bringing Someone Home from {o} to {d}",
    lambda o, d: f"{o} to {d}: Funeral Repatriation Guidance",
    lambda o, d: f"{o} to {d} Repatriation Guide",
]

DESCRIPTION_OPENERS = [
    lambda o, d, t: f"A death in {o} brings immediate questions. Repatriation to {d} takes {t}. Contact us 24/7.",
    lambda o, d, t: f"Bringing a loved one home from {o} to {d} takes {t} in most cases. All documentation handled. Contact us 24/7.",
    lambda o, d, t: f"Death in {o}, coming home to {d}. Repatriation takes {t}. Consular support included. Contact us 24/7.",
    lambda o, d, t: f"Arranging repatriation from {o} to {d}? Most cases complete within {t}. All documentation handled. Call us now.",
    lambda o, d, t: f"When someone dies in {o}, {d} families face a defined process taking {t}. Contact us 24/7.",
]

# ---------------------------------------------------------------------------
# Page generator
# ---------------------------------------------------------------------------

def make_title(origin_data, dest_data, page_index):
    """Generate an SEO-optimised title under 60 characters, rotating shape."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    shape = TITLE_SHAPES[page_index % len(TITLE_SHAPES)]
    title = shape(origin, dest)
    if len(title) > 60:
        title = f"{origin} to {dest} Repatriation Guide"
    if len(title) > 60:
        title = f"{origin} to {dest} Repatriation"
    return title


def make_description(origin_data, dest_data, page_index):
    """Generate an SEO description under 155 characters with CTA, rotating opener."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    timeline = origin_data["timeline_avg"]
    opener = DESCRIPTION_OPENERS[page_index % len(DESCRIPTION_OPENERS)]
    desc = opener(origin, dest, timeline)
    if len(desc) > 155:
        desc = f"Death in {origin}. Repatriation to {dest} takes {timeline}. All documentation handled. Contact us 24/7."
    if len(desc) > 155:
        desc = f"Repatriation from {origin} to {dest} takes {timeline}. Contact us 24/7."
    return desc


def make_embassy_note(dest_data, origin_name):
    """Generate destination consular note. No-op replace when the older
    {origin_country} placeholder style is not present in the string."""
    return dest_data["consular_note"].replace("{origin_country}", origin_name)


DEST_CONSULAR_LINES = {
    "samoa": lambda origin: "Notify the New Zealand High Commission in Apia under the UK-New Zealand Consular Sharing Agreement (no resident British post in Samoa). Hague Apostille applies (Samoa joined 1999). English is an official language, so translation is rarely needed.",
    "tonga": lambda origin: "Notify the Australian High Commission in Nuku'alofa under the UK-Australia Consular Sharing Agreement (no resident British post in Tonga). Hague Apostille applies (Tonga, succession, 1970). Documentation is processed in English throughout.",
    "belarus": lambda origin: "Notify the FCDO and the British Embassy in Minsk, which operates with reduced staff since the 2020 diplomatic downturn. Belarus is a Hague Apostille Convention member since 1992, and the FCDO advises against all but essential travel; no direct flights connect the UK to Belarus, so cargo routes via Warsaw, Vilnius, or Istanbul.",
    "marshall-islands": lambda origin: "Notify the British Embassy in Manila, Philippines (no resident British post in the Marshall Islands). The Marshall Islands is a Hague Apostille member since 1991, and a death on an outer atoll needs boat or light aircraft transfer to Majuro before documentation can begin.",
    "micronesia": lambda origin: "Notify the British Embassy in Manila, Philippines (no resident British post in the Federated States of Micronesia). FSM is not a Hague Apostille member, and which of its four states, Yap, Chuuk, Pohnpei, or Kosrae, the death occurred in changes the routing entirely.",
    "nauru": lambda origin: "Notify the British High Commission in Suva, Fiji (no resident British post in Nauru). Nauru is not a Hague Apostille member, and Nauru Airlines' limited service means all repatriation cargo must route via Brisbane, Australia.",
    "north-korea": lambda origin: "Call the FCDO immediately; there is no resident UK embassy in Pyongyang, so the Swedish Embassy handles what limited consular contact is possible, working alongside the British Embassy in Seoul. North Korea is not a Hague Apostille member, and North Korean state authorities control every stage of documentation.",
    "palau": lambda origin: "Notify the British Embassy in Manila, Philippines (no resident British post in Palau). Palau is a Hague Apostille member since 2019, though routing runs only via Manila or Guam, with no direct connection to the UK or Europe.",
    "solomon-islands": lambda origin: "Notify the Australian High Commission in Honiara (no resident British post in Solomon Islands). Solomon Islands is not a Hague Apostille member, though English common law and English-language documentation avoid a translation step most other Pacific corridors require.",
    "timor-leste": lambda origin: "Notify the Australian Embassy in Dili (no resident British post in Timor-Leste). Timor-Leste is not a Hague Apostille member, and documentation issued in Portuguese and Tetum requires certified English translation.",
    "tuvalu": lambda origin: "Notify the British High Commission in Suva, Fiji (no resident British post in Tuvalu). Tuvalu is not a Hague Apostille member, and a death on an outer atoll depends on the infrequent government vessel MV Nivaga III to reach Funafuti.",
    "vanuatu": lambda origin: "Notify the Australian High Commission in Port Vila (no resident British post in Vanuatu). Vanuatu is a Hague Apostille member since 2008 (succession), and a death on any of its islands beyond Efate needs inter-island transfer to Port Vila, which cyclone season can delay further.",
}

DEST_RECEPTION_STEPS = {
    "samoa": "Funeral director in Samoa takes custody at the cargo terminal at Faleolo International Airport (APW). Samoa Births, Deaths and Marriages Registration notified; documentation issued in English throughout.",
    "tonga": "Funeral director in Tonga takes custody at the cargo terminal at Fua'amotu International Airport (TBU), Tongatapu. Registrar General's Office notified; documentation issued in English throughout.",
    "belarus": "Funeral director in Belarus takes custody at the cargo terminal at Minsk National Airport (MSQ), reached via Warsaw, Vilnius, or Istanbul as no direct flights operate. Civil Registry Department notified; Investigative Committee clearance confirmed for any non-natural death.",
    "marshall-islands": "Funeral director in the Marshall Islands takes custody at the cargo terminal at Amata Kabua International Airport (MAJ), Majuro. National civil registration office notified; RMI Police Department clearance confirmed for non-natural deaths.",
    "micronesia": "Funeral director in the Federated States of Micronesia takes custody at the cargo terminal on whichever state, Yap, Chuuk, Pohnpei, or Kosrae, received the case. State civil registration office notified; documentation issued in English throughout.",
    "nauru": "Funeral director in Nauru takes custody at the cargo terminal at Nauru International Airport (INU), reached via Brisbane. Civil registration office notified; Nauru Police Force clearance confirmed for non-natural deaths.",
    "north-korea": "Funeral director access in North Korea is entirely state-controlled; any handover happens under Ministry of People's Security supervision at Pyongyang Sunan International Airport (FNJ), reached via Beijing. Swedish Embassy liaison confirmed throughout.",
    "palau": "Funeral director in Palau takes custody at the cargo terminal at Roman Tmetuchl International Airport (ROR), near Koror. Civil registration authority notified; Palau Police Department clearance confirmed for non-natural deaths.",
    "solomon-islands": "Funeral director in Solomon Islands takes custody at the cargo terminal at Honiara International Airport (HIR). Registrar of Births, Deaths and Marriages notified; documentation issued in English throughout, no translation required.",
    "timor-leste": "Funeral director in Timor-Leste takes custody at the cargo terminal at Presidente Nicolau Lobato International Airport (DIL), Dili. Civil Registration Service notified; National Police of Timor-Leste clearance confirmed for non-natural deaths.",
    "tuvalu": "Funeral director in Tuvalu takes custody at the cargo terminal at Funafuti International Airport (FUN), reached via Fiji. Tuvalu Births, Deaths and Marriages Registry notified; Tuvalu Police Service clearance confirmed for non-natural deaths.",
    "vanuatu": "Funeral director in Vanuatu takes custody at the cargo terminal at Bauerfield International Airport (VLI), Port Vila, reached via Brisbane or Sydney. Civil registration authority notified; police clearance confirmed for non-natural deaths.",
}


def make_timeline_steps(origin_data, dest_data):
    """Generate 7 timeline steps appropriate to the corridor."""
    origin = origin_data["name"]
    dest_airport = dest_data["airport"]
    cert = origin_data["death_cert"]
    doc_time = origin_data["doc_processing"]
    dest_key = dest_data["dest_key"]

    consular_fn = DEST_CONSULAR_LINES.get(dest_key, lambda o: f"Notify the {dest_data['name']} Embassy in {o}.")
    consular = consular_fn(origin)
    reception_step = DEST_RECEPTION_STEPS.get(dest_key, f"{dest_data['name']} funeral director takes custody at cargo terminal.")

    emergency_line = "FCDO 24-hour emergency line: +44 (0)20 7008 5000."

    steps = [
        {
            "step": 1,
            "action": "Immediate steps after death. Report to local emergency services and contact a specialist at once.",
            "timing": f"Day of death. {emergency_line}",
            "responsible": "Family or travel insurer",
        },
        {
            "step": 2,
            "action": f"Death registered. {cert.capitalize()} obtained from {origin_data['registry']}.",
            "timing": f"Registration must occur promptly. {origin_data.get('police_note', 'Local police clearance may be required.')}",
            "responsible": "Local funeral director and civil registry",
        },
        {
            "step": 3,
            "action": f"Embassy or consulate notified. {consular}",
            "timing": "Simultaneous with Step 1. Embassy provides list of local funeral directors.",
            "responsible": "Family or repatriation specialist",
        },
        {
            "step": 4,
            "action": "Embalming and preparation for international air transport.",
            "timing": "After body released by authorities. IATA P650 requirements apply.",
            "responsible": "Licensed local funeral director",
        },
        {
            "step": 5,
            "action": f"All export permits and authenticated documents obtained. {origin_data.get('translation_note', '')}",
            "timing": f"Allow {doc_time}. Cannot begin until death certificate issued.",
            "responsible": "Local funeral director and authorities",
        },
        {
            "step": 6,
            "action": f"Air cargo from {origin_data['airport']} to {dest_airport}.",
            "timing": "Once all documentation complete.",
            "responsible": "Repatriation specialist and airline cargo",
        },
        {
            "step": 7,
            "action": f"{reception_step}",
            "timing": "Within 24-48 hours of arrival.",
            "responsible": "Receiving funeral director",
        },
    ]
    return steps


DEST_FAQ6 = {
    "samoa": lambda origin: {
        "question": f"Does Samoa's Sunday observance actually delay a repatriation case from {origin}?",
        "answer": (
            "Yes, and it is worth planning around. Samoa observes Sunday strictly: government offices close, and official documentation does "
            "not move that day. A case reaching the Ministry of Health on a Saturday afternoon will typically wait until Monday to progress. "
            "On the plus side, English is an official language alongside Samoan, so death certificates and most paperwork need no translation, "
            "which is not the case for most Pacific destinations on this site."
        ),
    },
    "tonga": lambda origin: {
        "question": f"What happens if a death in Tonga involves diving or the Vava'u whale season, for a family in {origin}?",
        "answer": (
            "Vaiola Hospital on Tongatapu has no hyperbaric decompression capacity, so any diving-related incident, including those linked to "
            "the Vava'u whale-swimming season between July and October, requires medical evacuation before a repatriation case can properly "
            "begin. Tonga also sits in an active seismic and volcanic zone: the January 2022 Hunga Tonga eruption and tsunami cut communications "
            "and inter-island transport for weeks, so a specialist will check current conditions across the island group before confirming a timeline."
        ),
    },
    "belarus": lambda origin: {
        "question": f"Is Belarus still part of the Hague Apostille Convention for a repatriation from {origin}?",
        "answer": (
            "Yes. Belarus has been a Hague Apostille Convention member since 1992, confirmed on the official HCCH status table, "
            f"so a document apostilled in {origin} should be accepted by Belarusian authorities without further legalisation. "
            "The bigger practical constraint is diplomatic capacity: the British Embassy in Minsk has operated with reduced "
            "staff since 2020, and no direct flights connect the UK to Belarus, so cargo routes via Warsaw, Vilnius, or "
            "Istanbul instead."
        ),
    },
    "marshall-islands": lambda origin: {
        "question": f"Does it matter which atoll the death occurred on, for a repatriation from {origin} to the Marshall Islands?",
        "answer": (
            "Considerably. The Republic of the Marshall Islands spans 29 atolls and 5 islands across roughly 1.9 million "
            "square kilometres of ocean, and only Majuro has international air access. A death on an outer atoll needs "
            "boat or light aircraft transfer to Majuro first, which can take anywhere from hours to several days depending "
            "on weather and available transport. Kwajalein Atoll is a separate case again: it hosts a US Army missile "
            "defence installation, and any death there is coordinated through US military channels rather than the "
            "standard RMI civil process."
        ),
    },
    "micronesia": lambda origin: {
        "question": f"Why does it matter which FSM state a death happens in, for a family in {origin}?",
        "answer": (
            "The Federated States of Micronesia is not one place but four: Yap, Chuuk, Pohnpei, and Kosrae, spread across "
            "2,600 kilometres of the western Pacific. Each operates its own civil registration office, and the only "
            "international access is the United Airlines Island Hopper service through Guam, which serves the states on "
            "a fixed schedule. A death on Chuuk, popular for wreck diving, and a death on distant Yap involve genuinely "
            "different routing and timing, so a specialist confirms the exact island before giving any estimate."
        ),
    },
    "nauru": lambda origin: {
        "question": f"How does Nauru's single airline affect a repatriation from {origin}?",
        "answer": (
            "Nauru International Airport is served only by Nauru Airlines, and flights to Brisbane run just a few times "
            "a week with limited cargo space. Every repatriation case from Nauru depends on securing space on one of "
            "those services, since there is no alternative carrier and no other viable international gateway. The island "
            "itself is tiny, just 21 square kilometres, so once cargo space is confirmed the on-island logistics move quickly."
        ),
    },
    "north-korea": lambda origin: {
        "question": f"What actually happens if a British national dies in North Korea while travelling from {origin}?",
        "answer": (
            "There is no ordinary process to describe. The UK has no embassy in Pyongyang, so the Swedish Embassy handles "
            "whatever consular contact North Korean authorities permit, working with the British Embassy in Seoul. Every "
            "foreign national in the country, whether diplomat, journalist, or supervised tourist, is accompanied by state "
            "minders, and a death becomes a matter North Korean authorities manage directly rather than a case a "
            "repatriation firm can drive. Families should expect the FCDO to lead this case, not a private specialist."
        ),
    },
    "palau": lambda origin: {
        "question": f"Is Palau's Hague Apostille membership new, and does it help a repatriation from {origin}?",
        "answer": (
            "Yes, it is recent: Palau acceded to the Hague Apostille Convention on 17 October 2019, with the Convention "
            f"entering into force there on 23 June 2020. That means documents apostilled in {origin} are now recognised "
            "in Palau without the older, slower legalisation chain through embassies and foreign ministries. The "
            "remaining constraint is routing: there is no direct connection to the UK or Europe, so cargo travels via "
            "Manila or Guam regardless of how fast the paperwork moves."
        ),
    },
    "solomon-islands": lambda origin: {
        "question": f"Does Solomon Islands' British colonial history make a repatriation from {origin} more straightforward?",
        "answer": (
            "In some respects, yes. Solomon Islands was a British protectorate until 1978, and it retains English common "
            "law and English-language civil documentation, so a case here avoids the translation step that most Pacific "
            "corridors require. What it does not avoid is geography: the country spans roughly 900 islands, and a death "
            "outside Guadalcanal needs transfer to Honiara before the standard process can start, on top of the FCDO's "
            "advice to take increased caution in parts of Honiara since the 2021 unrest."
        ),
    },
    "timor-leste": lambda origin: {
        "question": f"What happens if the death in Timor-Leste occurs in the Oecusse enclave, for a family in {origin}?",
        "answer": (
            "Oecusse is geographically cut off from the rest of Timor-Leste, separated by a stretch of Indonesian West "
            "Timor. Reaching it by road means crossing into Indonesian territory and back out again; the alternative is "
            "a charter flight to the enclave's own small airstrip. Either way, a case in Oecusse takes noticeably longer "
            "to reach Dili, where the Civil Registration Service and the Australian Embassy's consular support are "
            "based, than a death in the capital itself."
        ),
    },
    "tuvalu": lambda origin: {
        "question": f"How does the MV Nivaga III affect a repatriation from {origin} to Tuvalu?",
        "answer": (
            "Tuvalu has nine atolls, and only Funafuti has an airport. The other eight depend on the government vessel "
            "MV Nivaga III for transport, and its schedule is infrequent and weather-dependent rather than fixed. A death "
            "on one of those outer atolls can add several days just to reach Funafuti, before the Tuvalu Births, Deaths "
            "and Marriages Registry process and the onward Fiji Airways connection even begin."
        ),
    },
    "vanuatu": lambda origin: {
        "question": f"Does cyclone season change the timeline for a repatriation from {origin} to Vanuatu?",
        "answer": (
            "It can. Vanuatu's cyclone season runs from November to April, and tropical cyclones regularly disrupt the "
            "inter-island boats and light aircraft that outer islands such as Tanna, Malekula, and Ambrym depend on to "
            "reach Port Vila. A death during that window, especially outside Efate or Espiritu Santo, may need to wait "
            "for weather to clear before transfer can even begin, on top of the standard documentation process."
        ),
    },
}


def make_dest_faq6(origin_data, dest_data):
    """Generate a destination-specific sixth FAQ."""
    origin = origin_data["name"]
    dest_key = dest_data["dest_key"]
    fn = DEST_FAQ6.get(dest_key)
    if fn:
        return fn(origin)
    return {
        "question": f"What specialist support is available for repatriation from {origin} to {dest_data['name']}?",
        "answer": (
            f"A specialist repatriation company can coordinate the full process from {origin} to {dest_data['name']}, "
            "including documentation, embalming, air cargo, and reception at the destination. "
            "Call our team on +44 7703 577246 at any hour for guidance on your specific case."
        ),
    }


def make_faqs(origin_data, dest_data):
    """Generate 6 FAQs for the corridor."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    timeline_avg = origin_data["timeline_avg"]
    timeline_fast = origin_data["timeline_fast"]
    timeline_complex = origin_data["timeline_complex"]
    cert = origin_data["death_cert"]

    consular_answer = origin_data.get("consular_faq")
    if not consular_answer:
        consular_answer = (
            f"The {origin_data['embassy_city']}-based British embassy or high commission can register the death "
            f"with UK authorities, provide a list of local funeral directors, and advise on documentation. "
            f"They cannot pay for or arrange repatriation. "
            f"FCDO 24-hour emergency line: +44 (0)20 7008 5000."
        )

    faqs = [
        {
            "question": f"How long does repatriation from {origin} to {dest} take?",
            "answer": (
                f"In a straightforward case, repatriation from {origin} to {dest} takes {timeline_avg}. "
                f"The fastest cases complete in {timeline_fast}. "
                f"Complex cases involving criminal investigation or remote locations can take {timeline_complex}."
            ),
        },
        {
            "question": f"What documents are required for repatriation from {origin} to {dest}?",
            "answer": (
                f"The core documents are: {cert}, "
                f"embalming certificate, freedom from infection certificate, passport of the deceased, "
                f"and all required export permits. "
                f"{origin_data.get('translation_note', 'Check destination requirements for translation.')} "
                f"Source: FCDO Travel Advice {origin} 2025."
            ),
        },
        {
            "question": f"Does the British Embassy in {origin} help with repatriation?",
            "answer": consular_answer,
        },
        {
            "question": f"What happens when the body arrives in {dest}?",
            "answer": (
                f"{dest_data['reception']} "
                f"All documentation from {origin} must be in order before the body is released for the funeral."
            ),
        },
        {
            "question": f"Can I bring ashes home from {origin} to {dest} instead of repatriating the body?",
            "answer": (
                f"Yes. Cremation in {origin} is an option in most cases, though local authorities must release "
                f"the body before cremation can take place. You will need the death certificate, cremation "
                f"certificate, and an export permit for the ashes. Ashes are simpler to transport than a body "
                f"and carry lower cargo costs. Ask our team for specific guidance on your case."
            ),
        },
        make_dest_faq6(origin_data, dest_data),
    ]
    return faqs


def format_step(step):
    lines = []
    lines.append(f"  - step: {step['step']}")
    lines.append(f"    action: \"{step['action']}\"")
    lines.append(f"    timing: \"{step['timing']}\"")
    lines.append(f"    responsible: \"{step['responsible']}\"")
    return "\n".join(lines)


def format_faq(faq):
    lines = []
    lines.append(f"  - question: \"{faq['question']}\"")
    lines.append(f"    answer: \"{faq['answer']}\"")
    return "\n".join(lines)


def build_page(origin_key, dest_key, variant, page_index):
    """Build the full YAML frontmatter for one route page."""
    o = ORIGIN_DATA[origin_key]
    d = DEST_META[dest_key]

    slug = f"{origin_key}-to-{dest_key}"
    title = make_title(o, d, page_index)
    description = make_description(o, d, page_index)

    # All destinations in this batch already exist in the matrix with 5 of
    # 8 origins built, so sideways links point to the two Tier A routes
    # guaranteed to exist for every origin in the pool: origin-to-UK and
    # origin-to-Ireland.
    sideways = (
        f"/routes/{origin_key}-to-united-kingdom/", f"Repatriation from {o['name']} to the UK",
        f"/routes/{origin_key}-to-ireland/", f"Repatriation from {o['name']} to Ireland",
    )

    timeline_steps = make_timeline_steps(o, d)
    faqs = make_faqs(o, d)

    origin_hub_url = f"/repatriation-from-{origin_key}/"
    dest_hub_url = f"/repatriation-from-{d.get('hub_slug', dest_key)}/"

    direct_intro = (
        f"Repatriation from {o['name']} to {d['name']} follows {o['name']}'s civil registration and export procedures. "
        f"Most cases take {o['timeline_avg']}."
    )

    lines = []
    lines.append("---")
    lines.append(f'title: "{title}"')
    lines.append(f'description: "{description}"')
    lines.append(f'origin_key: "{origin_key}"')
    lines.append(f'dest_key: "{d["dest_key"]}"')
    lines.append(f'origin_name: "{o["name"]}"')
    lines.append(f'dest_name: "{d["name"]}"')
    lines.append(f'origin_slug: "{origin_key}"')
    lines.append(f'dest_slug: "{dest_key}"')
    lines.append(f'slug: "{slug}"')
    lines.append(f'template_variant: "{variant}"')
    lines.append(f'route_complexity: "{o["complexity"]}"')
    lines.append(f'timeline_avg: "{o["timeline_avg"]}"')
    lines.append(f'timeline_fast: "{o["timeline_fast"]}"')
    lines.append(f'timeline_complex: "{o["timeline_complex"]}"')
    lines.append(f'embassy_city: "{o["embassy_city"]}"')
    lines.append(f'doc_processing_time: "{o["doc_processing"]}"')
    lines.append(f'date: 2026-07-10')
    lines.append(f'direct_answer_heading: "Repatriation from {o["name"]} to {d["name"]}: what to expect"')
    lines.append(f'direct_answer_intro: "{direct_intro}"')
    lines.append('direct_answer_points:')
    lines.append(f'  - "Key document: {o["death_cert"]}"')
    lines.append(f'  - "Documentation takes {o["doc_processing"]}. Appoint a specialist on day one."')
    lines.append(f'  - "British Embassy in {o["embassy_city"]} can advise. They cannot fund repatriation."')
    if o.get("apostille"):
        lines.append(f'  - "{o["name"]} is a Hague Apostille member ({o.get("apostille_year", "member")}). This simplifies document authentication."')
    else:
        lines.append(f'  - "{o["name"]} is not a Hague Apostille member. Documents require legalisation through the Ministry of Foreign Affairs."')
    lines.append(f'  - "Documentation is issued in {o["language"]}. Certified translation is required where needed."')
    lines.append(f'overview_heading: "What happens after a death in {o["name"]}"')
    lines.append(f'overview_body: "{o["overview"]}"')
    lines.append(f'dest_reception: "{d["reception"]}"')
    lines.append(f'dest_consular: "{make_embassy_note(d, o["name"])}"')
    lines.append("timeline_steps:")
    for step in timeline_steps:
        lines.append(format_step(step))
    lines.append("faqs:")
    for faq in faqs:
        lines.append(format_faq(faq))
    lines.append("links:")
    lines.append("  upward:")
    lines.append(f'    - url: "{origin_hub_url}"')
    lines.append(f'      text: "Full {o["name"]} repatriation guide"')
    lines.append(f'    - url: "{dest_hub_url}"')
    lines.append(f'      text: "Full {d["name"]} repatriation guide"')
    lines.append(f'    - url: "/guides/death-abroad-{origin_key}/"')
    lines.append(f'      text: "What to do if someone dies in {o["name"]}"')
    lines.append(f'    - url: "/embassy-contacts/{origin_key}/"')
    lines.append(f'      text: "British Embassy in {o["name"]}"')
    lines.append(f'    - url: "/contact/"')
    lines.append(f'      text: "Send an enquiry to our team"')
    lines.append("  sideways:")
    lines.append(f'    - url: "{sideways[0]}"')
    lines.append(f'      text: "{sideways[1]}"')
    lines.append(f'    - url: "{sideways[2]}"')
    lines.append(f'      text: "{sideways[3]}"')
    lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    all_batches = [
        ("R119", R119_ROUTES, 2),  # Start at C (index 2), 34 routes
    ]

    total_written = 0
    page_index = 0
    for chunk_name, routes, start_idx in all_batches:
        print(f"\n=== {chunk_name} ===")
        for i, (origin_key, dest_key) in enumerate(routes):
            variant_idx = (start_idx + i) % len(VARIANTS)
            variant = VARIANTS[variant_idx]
            slug = f"{origin_key}-to-{dest_key}"
            filepath = ROUTES_DIR / f"{slug}.md"

            if filepath.exists():
                print(f"  SKIP (exists): {slug}")
                page_index += 1
                continue

            content = build_page(origin_key, dest_key, variant, page_index)
            filepath.write_text(content, encoding="utf-8")
            print(f"  WROTE [{variant}]: {slug}")
            total_written += 1
            page_index += 1

    print(f"\nTotal pages written: {total_written}")


if __name__ == "__main__":
    main()
