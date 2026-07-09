#!/usr/bin/env python3
"""
generate_r111_r112.py -- Repatriate Service Route Generator
Chunk R111: 24 Tier C route pages, introducing the last three brand new
destinations available on the canonical 197-country list: Congo x8,
Vatican City x8, Yemen x8 (all 8 origins from the established pool at once,
since the destination-introduction phase of the route matrix is complete
after this chunk). This closes out Tier C new-destination coverage: of the
197 canonical countries in data/countries-197.json, only Palestine remains
without a single "*-to-palestine" route, and Palestine is deliberately
skipped here because it has no site/content/countries/palestine/ hub, no
guide, and no embassy-contacts page (the same reason Vatican City itself
was dropped from R103-R104; see MEMORY.md). Building a route with a broken
destination-hub link would violate the internal-linking rule in CLAUDE.md.
Vatican City and Congo are built here under their canonical route slugs,
"vatican-city" and "congo", matching data/countries-197.json, with a
hub_slug override (the same pattern used for cabo-verde/cape-verde in
generate_r101_r102.py) pointing to this site's existing hub pages, built
under the aliases "holy-see" and "republic-of-congo" respectively.

Chunk R112: 26 Tier C route pages, filling in previously missing
origin-pool combinations for nine destinations introduced in
generate_r97_r98.py (North Macedonia, Montenegro, Armenia, Azerbaijan,
Kazakhstan, Kyrgyzstan, Mongolia, Luxembourg, Monaco). Each of those ten
destinations was originally given only 5 of the 8 established Tier C
origins (Australia, France, Canada, Netherlands, Italy, Norway, Sweden,
Belgium); a direct file-count audit of site/content/routes/ on 9 July 2026
showed every Tier C "single wave" destination introduced since R97 is
missing exactly 3 of the 8. R112 completes all 8 origins for the first
eight of these (North Macedonia, Montenegro, Armenia, Azerbaijan,
Kazakhstan, Kyrgyzstan, Mongolia, Luxembourg) and adds 2 of Monaco's 3
missing origins (Australia, Canada; Netherlands is left for a future
chunk). No new destination research was required for R112: all facts are
reused verbatim from generate_r97_r98.py's own DEST_META, itself sourced
from the HCCH status table and national civil registry sites, checked
July 2026.

Origins (unchanged pool, both chunks): Australia, France, Canada,
Netherlands, Italy, Norway, Sweden, Belgium.

Sources for Congo, Vatican City, and Yemen facts: this site's own existing
country-hub pages (site/content/countries/republic-of-congo/_index.md,
holy-see/_index.md, yemen/_index.md), themselves sourced from FCDO travel
advice and embassy contacts when built. Apostille status for all three
verified directly against the official HCCH status table
(hcch.net/en/instruments/conventions/status-table/?cid=41) and its print
view (.../status-table/print/?cid=41), both fetched 9 July 2026: none of
the three -- Congo, the Holy See (Vatican City), or Yemen -- appear
anywhere in the current 130-contracting-party list, so all three are NOT
Hague Apostille Convention members and require standard legalisation.

Template variants: R111 starts at C (index 2), 24 routes, ending at A
(index 0). R112 continues the rotation without resetting and starts at B
(index 1), 26 routes, ending at B (index 1). The next chunk after R112
should start at C (index 2), restoring the usual alignment once 50 routes
have been added since the last confirmed C start (R109-R110).
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r109_r110.py)
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
# Destination data. Congo, Vatican City, and Yemen are brand new to the
# route matrix; the other nine are reused verbatim from
# generate_r97_r98.py, which sourced them from the HCCH status table and
# national civil registry sites.
# ---------------------------------------------------------------------------

DEST_META = {
    "congo": {
        "name": "Congo",
        "slug": "congo",
        "hub_slug": "republic-of-congo",
        "airport": "Maya-Maya Airport (BZV), Brazzaville, or Pointe-Noire Airport (PNR)",
        "reception": "The funeral director in the Republic of Congo takes custody at the cargo terminal at Maya-Maya Airport (BZV), Brazzaville, or Pointe-Noire Airport (PNR), depending on where the death occurred. Death registration runs through the Tribunal de Grande Instance in the relevant district, with Parquet clearance required before remains can be released for export and the Ministere de l'Interieur issuing the export permit. The Republic of Congo is not a Hague Apostille Convention member; documents require standard legalisation. Civil registration in Brazzaville and Pointe-Noire is well established; the Pool department and the northern Likouala and Sangha departments have far sparser infrastructure. Cremation is not available; full body repatriation is required.",
        "consular_note": "Notify the non-resident British Embassy in Kinshasa, Democratic Republic of Congo, which covers the Republic of Congo from directly across the Congo River. The FCDO advises against all but essential travel to the Pool department, south of Brazzaville.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days, longer for cases in the Pool department or the northern jungle provinces",
        "dest_key": "congo",
    },
    "vatican-city": {
        "name": "Vatican City",
        "slug": "vatican-city",
        "hub_slug": "holy-see",
        "airport": "No airport of its own. Rome Fiumicino Leonardo da Vinci International Airport (FCO), approximately 30 minutes by road",
        "reception": "The receiving funeral director takes custody following a short road transfer from Rome Fiumicino Leonardo da Vinci International Airport (FCO), since Vatican City has no airport of its own. Civil registration and death certification are handled by the Governorate of Vatican City State (Governatorato dello Stato della Citta del Vaticano); non-natural deaths are investigated by the Gendarmerie Corps of Vatican City State. Vatican City is not a Hague Apostille Convention member; documents require standard legalisation. Death certificates are issued in Italian. Where the deceased was clergy, a member of a religious order, or a Vatican employee, the relevant congregation or dicastery may have its own requirements alongside the Governorate's civil process. Cremation is not performed within Vatican City.",
        "consular_note": "Notify the British Embassy to the Holy See in Rome, a separate mission from the British Embassy to Italy. Italian transit law applies once remains leave Vatican territory for transport to Rome Fiumicino.",
        "apostille": "not a member; legalisation required",
        "timeline": "5-21 days, though genuinely rare and specialist in nature",
        "dest_key": "vatican-city",
    },
    "yemen": {
        "name": "Yemen",
        "slug": "yemen",
        "airport": "Aden International Airport (ADE) under the internationally recognised government; Sana'a International Airport (SAH), Houthi-controlled, with very limited and unpredictable service",
        "reception": "Reception depends entirely on which authority controls the area of arrival. Aden International Airport (ADE), under the internationally recognised government, is the more accessible gateway; Sana'a International Airport (SAH), Houthi-controlled, has very limited and unpredictable scheduled service. Death registration and export authorisation depend on which administration controls the location: the internationally recognised government's civil authorities in IRG areas, or Houthi-controlled authorities in the north-west. Yemen is not a Hague Apostille Convention member. Islamic burial within 24 hours is universally practised, and cremation is not available; full body repatriation is required.",
        "consular_note": "There is no UK Embassy in Yemen; it closed in Sana'a in 2015. Limited consular assistance is available through the British Embassy in Riyadh, Saudi Arabia. The FCDO advises against all travel to Yemen.",
        "apostille": "not a member; legalisation required",
        "timeline": "28-120 days where achievable at all; many locations are not accessible",
        "dest_key": "yemen",
    },
    "north-macedonia": {
        "name": "North Macedonia",
        "slug": "north-macedonia",
        "airport": "Skopje International Airport (SKP)",
        "reception": "The North Macedonian funeral director takes custody at the cargo terminal at Skopje International Airport (SKP). Death is registered with the maticna sluzba (civil registry) under the Ministry of Justice. Apostille certification is issued through the Ministry of Justice and the network of 27 First Instance Courts. Death certificates are issued in Macedonian, which uses the Cyrillic script. North Macedonia is a Hague Apostille Convention member since 1993.",
        "consular_note": "Embassy of North Macedonia in {origin_country}: contact the North Macedonian Embassy for documentation guidance. Hague Apostille applies (North Macedonia joined 1993). Certified translation of Macedonian documents is required for non-Macedonian-speaking destinations.",
        "apostille": "Hague Apostille (1993)",
        "timeline": "2-4 weeks standard",
        "dest_key": "north-macedonia",
    },
    "montenegro": {
        "name": "Montenegro",
        "slug": "montenegro",
        "airport": "Podgorica Airport (TGD) or Tivat Airport (TIV)",
        "reception": "The Montenegrin funeral director takes custody at the cargo terminal at Podgorica (TGD) or Tivat (TIV). Death is registered by the maticar (civil registry officer) in the local opstina (municipality). Montenegro has been a party to the Vienna CIEC Convention of 8 September 1976 since independence, which allows multilingual death certificate extracts between contracting states without translation. Montenegro is also a Hague Apostille Convention member since 3 July 2006.",
        "consular_note": "Embassy of Montenegro in {origin_country}: contact the Montenegrin Embassy for documentation guidance. Hague Apostille applies (Montenegro joined 2006). CIEC multilingual extracts may remove the need for translation when the destination is also a CIEC member state.",
        "apostille": "Hague Apostille (2006)",
        "timeline": "2-4 weeks standard",
        "dest_key": "montenegro",
    },
    "armenia": {
        "name": "Armenia",
        "slug": "armenia",
        "airport": "Zvartnots International Airport (EVN), Yerevan",
        "reception": "The Armenian funeral director takes custody at the cargo terminal at Zvartnots International Airport (EVN) near Yerevan. Death is registered with one of 52 Civil Status Acts Registration (CSAR) territorial bodies under the Ministry of Justice. In Yerevan, registration and certificates are handled through the Civic Status Registration Department at the municipal funeral bureau. Armenia is a Hague Apostille Convention member since 1993. Death certificates are issued in Armenian.",
        "consular_note": "Embassy of Armenia in {origin_country}: contact the Armenian Embassy for documentation guidance. Hague Apostille applies (Armenia joined 1993). Certified translation into Armenian is required for foreign-language documentation.",
        "apostille": "Hague Apostille (1993)",
        "timeline": "2-4 weeks standard",
        "dest_key": "armenia",
    },
    "azerbaijan": {
        "name": "Azerbaijan",
        "slug": "azerbaijan",
        "airport": "Heydar Aliyev International Airport (GYD), Baku",
        "reception": "The Azerbaijani funeral director takes custody at the cargo terminal at Heydar Aliyev International Airport (GYD) in Baku. Death is registered at a district Civil Registry Office (VVAQ) or through an ASAN Xidmet (ASAN Service) one-stop centre. Azerbaijan is a Hague Apostille Convention member since 1 March 2005. Death certificates are issued in Azerbaijani.",
        "consular_note": "Embassy of Azerbaijan in {origin_country}: contact the Azerbaijani Embassy for documentation guidance. Hague Apostille applies (Azerbaijan joined 2005). Certified translation into Azerbaijani is required for foreign-language documentation.",
        "apostille": "Hague Apostille (2005)",
        "timeline": "2-4 weeks standard",
        "dest_key": "azerbaijan",
    },
    "kazakhstan": {
        "name": "Kazakhstan",
        "slug": "kazakhstan",
        "airport": "Almaty International Airport (ALA) or Astana International Airport (NQZ)",
        "reception": "The Kazakhstani funeral director takes custody at the cargo terminal at Almaty (ALA) or Astana (NQZ). Death is registered with a local RAGS civil registry office. Apostille certification of civil registry documents, including death certificates, is issued by the Ministry of Justice. Kazakhstan is a Hague Apostille Convention member since 30 January 2001. Death certificates are issued in Kazakh and Russian.",
        "consular_note": "Embassy of Kazakhstan in {origin_country}: contact the Kazakhstani Embassy for documentation guidance. Hague Apostille applies (Kazakhstan joined 2001). Certified translation may be required depending on the destination language.",
        "apostille": "Hague Apostille (2001)",
        "timeline": "2-4 weeks standard",
        "dest_key": "kazakhstan",
    },
    "kyrgyzstan": {
        "name": "Kyrgyzstan",
        "slug": "kyrgyzstan",
        "airport": "Manas International Airport (FRU), Bishkek",
        "reception": "The Kyrgyzstani funeral director takes custody at the cargo terminal at Manas International Airport (FRU) near Bishkek. Death is registered with the local civil registry office (civil status acts registration). Kyrgyzstan is a Hague Apostille Convention member since 31 July 2011. Death certificates are issued in Kyrgyz and Russian.",
        "consular_note": "Embassy of Kyrgyzstan in {origin_country}: contact the Kyrgyzstani Embassy for documentation guidance. Hague Apostille applies (Kyrgyzstan joined 2011). Certified translation may be required depending on the destination language.",
        "apostille": "Hague Apostille (2011)",
        "timeline": "3-5 weeks standard",
        "dest_key": "kyrgyzstan",
    },
    "mongolia": {
        "name": "Mongolia",
        "slug": "mongolia",
        "airport": "Chinggis Khaan International Airport (ULN), Ulaanbaatar",
        "reception": "The Mongolian funeral director takes custody at the cargo terminal at Chinggis Khaan International Airport (ULN) in Ulaanbaatar. Death must be reported to the local civil registration office within 28 days; the Civil Registration Department of the General Authority for Intellectual Property and State Registration, under the Ministry of Justice and Home Affairs, issues the certificate. Apostille certification is handled separately by the Ministry of Foreign Affairs and Trade. Mongolia is a Hague Apostille Convention member since 31 December 2009. Death certificates are issued in Mongolian.",
        "consular_note": "Embassy of Mongolia in {origin_country}: contact the Mongolian Embassy for documentation guidance. Hague Apostille applies (Mongolia joined 2009). Certified translation into Mongolian is required for foreign-language documentation.",
        "apostille": "Hague Apostille (2009)",
        "timeline": "4-6 weeks standard",
        "dest_key": "mongolia",
    },
    "luxembourg": {
        "name": "Luxembourg",
        "slug": "luxembourg",
        "airport": "Luxembourg Findel Airport (LUX)",
        "reception": "The Luxembourgish funeral director takes custody at the cargo terminal at Luxembourg Findel Airport (LUX). Death is registered at the local commune, where the acte de deces (death certificate) is issued. Legalisation and apostille of the acte de deces is handled by the legalisation service of the Ministry of Foreign and European Affairs. Luxembourg is a Hague Apostille Convention member since 3 June 1979.",
        "consular_note": "Embassy of Luxembourg in {origin_country}: contact the Luxembourgish Embassy for documentation guidance. Hague Apostille applies (Luxembourg joined 1979).",
        "apostille": "Hague Apostille (1979)",
        "timeline": "2-3 weeks standard",
        "dest_key": "luxembourg",
    },
    "monaco": {
        "name": "Monaco",
        "slug": "monaco",
        "airport": "No commercial airport. The nearest international gateway is Nice Cote d'Azur Airport (NCE) in France, with onward transfer by road",
        "reception": "The Monegasque funeral director takes custody following arrival via Nice Cote d'Azur Airport (NCE), since Monaco has no commercial airport of its own. Death is registered with the Etat Civil (Civil Registry) at the Mairie de Monaco (Monaco City Hall). Apostille certification is issued by Monaco's Department of Justice. Monaco is a Hague Apostille Convention member since 31 December 2002. Death certificates are issued in French.",
        "consular_note": "Consulate of Monaco in {origin_country}: contact the Monegasque Consulate for documentation guidance. Hague Apostille applies (Monaco joined 2002). Because Monaco has no international airport, every air cargo route runs via Nice, France, followed by a short road transfer.",
        "apostille": "Hague Apostille (2002)",
        "timeline": "2-3 weeks standard",
        "dest_key": "monaco",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R111: starts at template C (index 2). 24 routes (3 brand new destinations,
# all 8 origins each -- the destination-introduction phase of the matrix
# closes with this chunk).
R111_ROUTES = [
    # Congo x8
    ("australia", "congo"),
    ("france", "congo"),
    ("canada", "congo"),
    ("netherlands", "congo"),
    ("italy", "congo"),
    ("norway", "congo"),
    ("sweden", "congo"),
    ("belgium", "congo"),
    # Vatican City x8
    ("australia", "vatican-city"),
    ("france", "vatican-city"),
    ("canada", "vatican-city"),
    ("netherlands", "vatican-city"),
    ("italy", "vatican-city"),
    ("norway", "vatican-city"),
    ("sweden", "vatican-city"),
    ("belgium", "vatican-city"),
    # Yemen x8
    ("australia", "yemen"),
    ("france", "yemen"),
    ("canada", "yemen"),
    ("netherlands", "yemen"),
    ("italy", "yemen"),
    ("norway", "yemen"),
    ("sweden", "yemen"),
    ("belgium", "yemen"),
]

# R112: starts at template B (index 1), continuing the rotation from R111's
# final page (index 0, variant A) without resetting. 26 routes, completing
# 8/8 origin coverage for eight R97-R98 destinations and adding 2 of
# Monaco's 3 missing origins.
R112_ROUTES = [
    # North Macedonia -- missing origins (france, norway, belgium)
    ("france", "north-macedonia"),
    ("norway", "north-macedonia"),
    ("belgium", "north-macedonia"),
    # Montenegro -- missing origins (australia, sweden, belgium)
    ("australia", "montenegro"),
    ("sweden", "montenegro"),
    ("belgium", "montenegro"),
    # Armenia -- missing origins (canada, norway, belgium)
    ("canada", "armenia"),
    ("norway", "armenia"),
    ("belgium", "armenia"),
    # Azerbaijan -- missing origins (australia, france, belgium)
    ("australia", "azerbaijan"),
    ("france", "azerbaijan"),
    ("belgium", "azerbaijan"),
    # Kazakhstan -- missing origins (italy, netherlands, belgium)
    ("italy", "kazakhstan"),
    ("netherlands", "kazakhstan"),
    ("belgium", "kazakhstan"),
    # Kyrgyzstan -- missing origins (france, norway, belgium)
    ("france", "kyrgyzstan"),
    ("norway", "kyrgyzstan"),
    ("belgium", "kyrgyzstan"),
    # Mongolia -- missing origins (australia, sweden, belgium)
    ("australia", "mongolia"),
    ("sweden", "mongolia"),
    ("belgium", "mongolia"),
    # Luxembourg -- missing origins (australia, italy, norway)
    ("australia", "luxembourg"),
    ("italy", "luxembourg"),
    ("norway", "luxembourg"),
    # Monaco -- 2 of 3 missing origins (australia, canada); netherlands left for a future chunk
    ("australia", "monaco"),
    ("canada", "monaco"),
]

# ---------------------------------------------------------------------------
# Varied title shapes, description openings, intro texts (burstiness and
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

INTRO_VARS = {
    0: "The process starts the moment the death is reported.",
    1: "Repatriation from {origin} takes {timeline_avg} in most cases.",
    2: "Getting a loved one home from {origin} is possible. The process has clear steps.",
    3: "A death in {origin} brings specific documentation and consular procedures.",
    4: "Families in {dest_name} waiting for news from {origin} face a defined process.",
}

OVERVIEW_SUFFIX = {
    0: "Appoint a repatriation specialist on day one.",
    1: "Contact us at any hour on +44 7703 577246.",
    2: "The earlier a specialist is involved, the faster the process moves.",
    3: "Do not sign anything locally without specialist advice.",
    4: "Our team is available 24 hours a day, every day of the year.",
}

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
    "congo": lambda origin: "Notify the non-resident British Embassy in Kinshasa, Democratic Republic of Congo, directly across the Congo River from Brazzaville. The Republic of Congo is not a Hague Apostille Convention member; documents require standard legalisation. The FCDO advises against all but essential travel to the Pool department.",
    "vatican-city": lambda origin: "Notify the British Embassy to the Holy See in Rome, a separate mission from the British Embassy to Italy. Vatican City is not a Hague Apostille Convention member; documents require standard legalisation.",
    "yemen": lambda origin: "Call the FCDO immediately; there is no UK Embassy in Yemen since it closed in Sana'a in 2015. Limited consular assistance comes from the British Embassy in Riyadh, Saudi Arabia. Yemen is not a Hague Apostille Convention member, and the FCDO advises against all travel.",
    "north-macedonia": lambda origin: f"Notify the Embassy of North Macedonia in {origin}. Hague Apostille applies (1993).",
    "montenegro": lambda origin: f"Notify the Embassy of Montenegro in {origin}. Hague Apostille applies (2006). Vienna CIEC Convention (1976) may apply for multilingual extracts.",
    "armenia": lambda origin: f"Notify the Embassy of Armenia in {origin}. Hague Apostille applies (1993).",
    "azerbaijan": lambda origin: f"Notify the Embassy of Azerbaijan in {origin}. Hague Apostille applies (2005).",
    "kazakhstan": lambda origin: f"Notify the Embassy of Kazakhstan in {origin}. Hague Apostille applies (2001).",
    "kyrgyzstan": lambda origin: f"Notify the Embassy of Kyrgyzstan in {origin}. Hague Apostille applies (2011).",
    "mongolia": lambda origin: f"Notify the Embassy of Mongolia in {origin}. Hague Apostille applies (2009). Allow extra time given Mongolia's size and low population density.",
    "luxembourg": lambda origin: f"Notify the Embassy of Luxembourg in {origin}. Hague Apostille applies (1979).",
    "monaco": lambda origin: f"Notify the Consulate of Monaco in {origin}. Hague Apostille applies (2002). Route via Nice, France, since Monaco has no commercial airport.",
}

DEST_RECEPTION_STEPS = {
    "congo": "Funeral director in the Republic of Congo takes custody at the cargo terminal at Maya-Maya Airport (BZV), Brazzaville, or Pointe-Noire Airport (PNR). Tribunal de Grande Instance notified; Parquet clearance confirmed before export.",
    "vatican-city": "Receiving funeral director takes custody following a short road transfer from Rome Fiumicino Leonardo da Vinci International Airport (FCO). Governorate of Vatican City State notified; Gendarmerie Corps clearance confirmed for any non-natural death.",
    "yemen": "Reception depends on which authority controls the arrival point: Aden International Airport (ADE) under the internationally recognised government, or the far less predictable Sana'a International Airport (SAH) under Houthi control. Islamic burial timing considerations apply throughout.",
    "north-macedonia": "North Macedonian funeral director takes custody at cargo terminal at Skopje International Airport (SKP). Maticna sluzba (civil registry) notified. Apostille issued through the Ministry of Justice and First Instance Courts. Death certificate issued in Macedonian (Cyrillic script).",
    "montenegro": "Montenegrin funeral director takes custody at cargo terminal at Podgorica (TGD) or Tivat (TIV). Maticar (civil registry officer) at the local opstina notified. Hague Apostille applies (Montenegro joined 2006).",
    "armenia": "Armenian funeral director takes custody at cargo terminal at Zvartnots International Airport (EVN), Yerevan. Civil Status Acts Registration (CSAR) territorial body notified. Death certificate issued in Armenian. Certified translation required for foreign documentation.",
    "azerbaijan": "Azerbaijani funeral director takes custody at cargo terminal at Heydar Aliyev International Airport (GYD), Baku. District Civil Registry Office (VVAQ) or ASAN Xidmet centre notified. Death certificate issued in Azerbaijani.",
    "kazakhstan": "Kazakhstani funeral director takes custody at cargo terminal at Almaty (ALA) or Astana (NQZ). RAGS civil registry office notified. Apostille issued by the Ministry of Justice. Death certificate issued in Kazakh and Russian.",
    "kyrgyzstan": "Kyrgyzstani funeral director takes custody at cargo terminal at Manas International Airport (FRU), Bishkek. Local civil registry office notified. Death certificate issued in Kyrgyz and Russian.",
    "mongolia": "Mongolian funeral director takes custody at cargo terminal at Chinggis Khaan International Airport (ULN), Ulaanbaatar. Civil Registration Department (Ministry of Justice and Home Affairs) notified within the 28-day reporting window. Apostille issued separately by the Ministry of Foreign Affairs and Trade. Death certificate issued in Mongolian.",
    "luxembourg": "Luxembourgish funeral director takes custody at cargo terminal at Luxembourg Findel Airport (LUX). Local commune civil registry notified. Acte de deces legalised or apostilled by the Ministry of Foreign and European Affairs.",
    "monaco": "Monegasque funeral director takes custody following arrival via Nice Cote d'Azur Airport (NCE) and a short road transfer, since Monaco has no commercial airport of its own. Etat Civil at the Mairie de Monaco notified. Death certificate issued in French.",
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
    "congo": lambda origin: {
        "question": f"Why is repatriation from {origin} to Congo covered by an embassy in a different country?",
        "answer": (
            "The British Embassy in Kinshasa, Democratic Republic of Congo, provides non-resident consular cover for the Republic of Congo, "
            "even though the two countries are entirely separate: different governments, different legal systems, sharing only the Congo River as a border. "
            "Brazzaville sits directly across that river from Kinshasa, so the arrangement is a practical one rather than a sign the two countries are connected administratively. "
            f"The Republic of Congo is not a Hague Apostille Convention member, so documents from {origin} require standard legalisation rather than a simpler apostille stamp."
        ),
    },
    "vatican-city": lambda origin: {
        "question": f"Does the British Embassy to Italy handle a repatriation from {origin} to Vatican City?",
        "answer": (
            "No. Vatican City has its own separate mission, the British Embassy to the Holy See, distinct from the British Embassy to Italy, even though both are based in Rome. "
            "Contacting the wrong one wastes time on a case that is already unusual: deaths of non-Vatican citizens within the 0.44 square kilometre city-state are rare. "
            f"Vatican City is not a Hague Apostille Convention member, and any document arriving from {origin} needs standard legalisation rather than an apostille."
        ),
    },
    "yemen": lambda origin: {
        "question": f"Does it make a difference to a family in {origin} which part of Yemen the death occurred in?",
        "answer": (
            "Yes, fundamentally. Yemen has been split since 2014-15 between the internationally recognised government, based in Aden, and the Houthi movement, which controls Sana'a and much of the north-west. "
            "Documentation, and even whether repatriation is achievable at all, depends on which authority controls the location of death. "
            "Aden International Airport under the internationally recognised government is the more accessible gateway; Sana'a's airport has very limited, unpredictable service under Houthi control. "
            "The FCDO advises against all travel to Yemen, and any case here should begin with a call to the FCDO emergency line before contacting a specialist firm."
        ),
    },
    "north-macedonia": lambda origin: {
        "question": f"Is North Macedonia a Hague Apostille member and how does this affect repatriation from {origin}?",
        "answer": (
            "North Macedonia is a Hague Apostille Convention member since 1993. "
            "Apostille certification is issued through the Ministry of Justice and a network of 27 First Instance Courts rather than a single national office. "
            "Death certificates are issued in Macedonian, which uses the Cyrillic script. "
            f"Certified translation of documents from {origin} into Macedonian is typically required by the receiving civil registry."
        ),
    },
    "montenegro": lambda origin: {
        "question": f"Does repatriation to Montenegro from {origin} require translated documents?",
        "answer": (
            "It depends. Montenegro is a party to the Vienna CIEC Convention of 1976, which allows multilingual civil status extracts, including death certificates, "
            "to be used between contracting states without translation. "
            "Montenegro is also a Hague Apostille member since 2006. "
            f"Whether translation is needed for a document from {origin} depends on whether {origin} is also a CIEC member. Your specialist will confirm this for your case."
        ),
    },
    "armenia": lambda origin: {
        "question": f"How is a death registered when repatriating from {origin} to Armenia?",
        "answer": (
            "Armenia's civil registration system runs through 52 Civil Status Acts Registration (CSAR) territorial bodies under the Ministry of Justice. "
            "In Yerevan specifically, death registration and certificates are handled through the Civic Status Registration Department at the municipal funeral bureau. "
            "Armenia is a Hague Apostille member since 1993. "
            f"Certified translation of documents from {origin} into Armenian is required before the receiving registry will accept them."
        ),
    },
    "azerbaijan": lambda origin: {
        "question": f"What is ASAN Xidmet and how does it affect repatriation from {origin} to Azerbaijan?",
        "answer": (
            "ASAN Xidmet (ASAN Service) is a network of one-stop government service centres in Azerbaijan that can issue civil registry documents, including death certificates, "
            "alongside the traditional district Civil Registry Offices (VVAQ). "
            "Azerbaijan is a Hague Apostille member since 2005. "
            f"Certified translation of documents from {origin} into Azerbaijani is required as part of the repatriation process."
        ),
    },
    "kazakhstan": lambda origin: {
        "question": f"Which cities handle international arrivals when repatriating from {origin} to Kazakhstan?",
        "answer": (
            "Kazakhstan has two major reception points: Almaty International Airport (ALA), the country's largest city, and Astana International Airport (NQZ), the capital. "
            "Which one applies depends on where the family and receiving funeral director are based. "
            "Kazakhstan is a Hague Apostille member since 30 January 2001, and death certificates are issued in Kazakh and Russian by RAGS civil registry offices."
        ),
    },
    "kyrgyzstan": lambda origin: {
        "question": f"What is the realistic timeline for repatriation from {origin} to Kyrgyzstan?",
        "answer": (
            "In a straightforward case, repatriation to Kyrgyzstan takes 3-5 weeks. "
            "Kyrgyzstan is a Hague Apostille member since 31 July 2011, which simplifies authentication of origin-country documents. "
            "All international arrivals route through Manas International Airport near Bishkek. "
            "Delays are more likely when the death is sudden or unexplained and requires local investigation before the body is released."
        ),
    },
    "mongolia": lambda origin: {
        "question": f"Why does repatriation from {origin} to Mongolia typically take longer than to other Tier C destinations?",
        "answer": (
            "Repatriation to Mongolia takes 4-6 weeks, longer than many comparable corridors. "
            "Mongolia's civil registration and its Hague Apostille certification are handled by two separate authorities, the Ministry of Justice and Home Affairs and the Ministry of Foreign Affairs and Trade, "
            "which adds a coordination step. "
            "Ulaanbaatar's Chinggis Khaan International Airport is the only realistic reception point given the country's size and low population density."
        ),
    },
    "luxembourg": lambda origin: {
        "question": f"Which authority handles apostille certification for repatriation from {origin} to Luxembourg?",
        "answer": (
            "The legalisation service of Luxembourg's Ministry of Foreign and European Affairs issues apostille certification for the acte de deces (death certificate), "
            "which is first obtained from the local commune where the death is registered. "
            "Luxembourg is a Hague Apostille member since 3 June 1979, so this is generally a straightforward process for documents arriving from other Hague member states."
        ),
    },
    "monaco": lambda origin: {
        "question": f"How does a repatriation from {origin} actually reach Monaco, given it has no airport?",
        "answer": (
            "Monaco has no commercial airport of its own. "
            "Every air cargo repatriation to Monaco lands at Nice Cote d'Azur Airport (NCE) in neighbouring France, followed by a short road transfer across the border. "
            "Monaco is a Hague Apostille member since 31 December 2002, and death is registered with the Etat Civil at the Mairie de Monaco once the body arrives."
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

    # Every destination in this batch either is brand new to the matrix
    # (R111) or already existed alongside these origins (R112), so sideways
    # links point to the two Tier A routes guaranteed to exist for every
    # origin in the pool: origin-to-UK and origin-to-Ireland.
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
    lines.append(f'date: 2026-07-09')
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
        ("R111", R111_ROUTES, 2),  # Start at C (index 2), 24 routes, ends at A (index 0)
        ("R112", R112_ROUTES, 1),  # Start at B (index 1), continuing seamlessly from R111
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
