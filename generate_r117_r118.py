#!/usr/bin/env python3
"""
generate_r117_r118.py -- Repatriate Service Route Generator
Chunks R117-R118: 50 Tier C route pages, continuing the origin-pool
fill-out phase begun in R112. Every Tier C "single wave" destination
introduced between R97 and R110 was originally given only 5 of the 8
established origins (Australia, France, Canada, Netherlands, Italy,
Norway, Sweden, Belgium), missing exactly 3 each. R116 completed
Uzbekistan's remaining 3 origins, confirmed 8/8 by a direct filesystem
check before this chunk was written. This chunk continues with
Tajikistan (the next destination in the R105-R106 introduction order)
onward through the R105-R110 destination list, in the order those
destinations were introduced.

R117 (25 routes, template start C): Tajikistan, Mali, Niger, Chad,
Burkina Faso, Guinea, Guinea-Bissau, Liberia (all R105-R106
destinations) completed to full 8/8 origin coverage, plus Benin (the
first R107-R108 destination) given 1 of its 3 missing origins (Norway).

R118 (25 routes, template start C, continuing seamlessly): Benin's
remaining 2 origins (Sweden, Belgium), then Burundi, Central African
Republic, Djibouti, Equatorial Guinea, Gabon, South Sudan, Kiribati
completed to full 8/8, then Samoa given 2 of its 3 missing origins
(Norway, Sweden), leaving Belgium and all of Tonga for R119.

No new destination research was required for this chunk: every fact
below is reused verbatim from the generator that originally introduced
that destination (generate_r105_r106.py for Tajikistan through Liberia,
generate_r107_r108.py for Benin through Samoa), each itself sourced
from the HCCH Apostille status table, national civil registry sites,
and GOV.UK British Embassy/High Commission pages, checked July 2026.

Origins (unchanged pool): Australia, France, Canada, Netherlands, Italy,
Norway, Sweden, Belgium.

Missing-origin combinations for every destination in this chunk were
confirmed by a direct filesystem check of site/content/routes/ against
the 8-origin pool immediately before this generator was written.

Template variants: R116 ended at index 1 (B), 25 routes from a start of
2. R117 starts at C (index 2), 25 routes, ending at index 1 (B). R118
continues seamlessly from index 2 (C) since 25 is a multiple of 5,
ending at index 1 (B) again. No two consecutive pages share a variant.
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r115_r116.py)
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
    "tajikistan": {
        "name": "Tajikistan",
        "slug": "tajikistan",
        "airport": "Dushanbe Airport (DYU)",
        "reception": "The funeral director in Tajikistan takes custody at the cargo terminal at Dushanbe Airport (DYU). Death is registered with the Civil Status Registration Agency; for non-natural deaths the Ministry of Internal Affairs also becomes involved. Tajikistan has been a Hague Apostille Convention member since 31 October 2015, though Austria, Belgium, and Germany objected to its accession, so the Convention does not apply between Tajikistan and those three states specifically. Documentation is issued in Tajik, using Cyrillic script, and often Russian.",
        "consular_note": "The British Embassy in Dushanbe is resident in Tajikistan and provides direct consular support, though capacity is limited.",
        "apostille": "Hague Apostille (2015; does not apply between Tajikistan and Austria, Belgium, or Germany)",
        "timeline": "2-6 weeks standard",
        "dest_key": "tajikistan",
    },
    "mali": {
        "name": "Mali",
        "slug": "mali",
        "airport": "Bamako-Senou International Airport (BKO)",
        "reception": "The funeral director in Mali takes custody at the cargo terminal at Bamako-Senou International Airport (BKO). Death is registered through the etat civil (civil status office); the acte de deces is issued in French. Mali is not a Hague Apostille Convention member; documents require consular legalisation. The country has been under military rule since the coup of May 2021.",
        "consular_note": "There is no resident British Embassy in Mali. Consular support comes from the British Embassy in Dakar, Senegal, which provides non-resident coverage.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "4-13 weeks standard, longer in northern regions",
        "dest_key": "mali",
    },
    "niger": {
        "name": "Niger",
        "slug": "niger",
        "airport": "Diori Hamani International Airport (NIM), Niamey",
        "reception": "The funeral director in Niger takes custody at the cargo terminal at Diori Hamani International Airport (NIM), Niamey. Death is registered through local civil status offices, with police clearance issued through the Police Nationale. Niger is not a Hague Apostille Convention member; documents require consular legalisation. A military junta, the CNSP, has governed since the coup of July 2023.",
        "consular_note": "There is no resident British Embassy in Niger. Consular support comes from the British Embassy in Abuja, Nigeria, which holds non-resident accreditation.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "4-13 weeks standard, post-coup conditions",
        "dest_key": "niger",
    },
    "chad": {
        "name": "Chad",
        "slug": "chad",
        "airport": "Hassan Djamous N'Djamena International Airport (NDJ)",
        "reception": "The funeral director in Chad takes custody at the cargo terminal at Hassan Djamous N'Djamena International Airport (NDJ). Death is registered through the etat civil (civil status office); the acte de deces is issued in French. Chad is not a Hague Apostille Convention member; documents require consular legalisation. The country has been governed by a Transitional Military Council since April 2021.",
        "consular_note": "There is no resident British Embassy in Chad. Consular support comes from the British Embassy in Yaounde, Cameroon, which provides non-resident coverage.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "4-12 weeks standard, longer near conflict-affected border regions",
        "dest_key": "chad",
    },
    "burkina-faso": {
        "name": "Burkina Faso",
        "slug": "burkina-faso",
        "airport": "Ouagadougou Airport (OUA)",
        "reception": "The funeral director in Burkina Faso takes custody at the cargo terminal at Ouagadougou Airport (OUA). Death is registered through the etat civil (civil status office); for non-natural deaths the Tribunal de Grande Instance must issue an order before the death certificate is released. Burkina Faso is not a Hague Apostille Convention member; documents require consular legalisation. A military junta has governed since September 2022.",
        "consular_note": "There is no resident British Embassy in Burkina Faso. Consular support comes from the British High Commission in Accra, Ghana, which provides non-resident coverage.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "4-13 weeks standard, post-coup conditions",
        "dest_key": "burkina-faso",
    },
    "guinea": {
        "name": "Guinea",
        "slug": "guinea",
        "airport": "Conakry-Gbessia International Airport (CKY)",
        "reception": "The funeral director in Guinea takes custody at the cargo terminal at Conakry-Gbessia International Airport (CKY). Death is registered through the etat civil (civil status office); the acte de deces is issued in French, and Gendarmerie clearance is required alongside civil registration. Guinea is not a Hague Apostille Convention member; documents require consular legalisation. A military junta has governed since September 2021.",
        "consular_note": "There is no resident British Embassy in Guinea. Consular support comes from the British High Commission in Freetown, Sierra Leone, which provides non-resident coverage.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "2-6 weeks standard",
        "dest_key": "guinea",
    },
    "guinea-bissau": {
        "name": "Guinea-Bissau",
        "slug": "guinea-bissau",
        "airport": "Osvaldo Vieira International Airport (OXB), Bissau, with limited international cargo frequency",
        "reception": "The funeral director in Guinea-Bissau takes custody at the cargo terminal at Osvaldo Vieira International Airport (OXB), Bissau. Death is registered through the Conservatoria do Registo Civil under Portuguese civil law, and the Ministerio da Administracao Territorial issues the export permit. Guinea-Bissau is not a Hague Apostille Convention member; documents require consular legalisation.",
        "consular_note": "There is no resident British Embassy in Guinea-Bissau. Consular support comes from the British Embassy in Dakar, Senegal, which provides non-resident coverage.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "2-6 weeks standard, longer outside Bissau",
        "dest_key": "guinea-bissau",
    },
    "liberia": {
        "name": "Liberia",
        "slug": "liberia",
        "airport": "Roberts International Airport (ROB), around 60km from Monrovia",
        "reception": "The funeral director in Liberia takes custody at the cargo terminal at Roberts International Airport (ROB), around 60km from Monrovia, requiring a road transfer to the capital. Death is registered through Liberia's English-language civil registration system, with the Liberia National Police issuing clearance where required. Liberia is not a Hague Apostille Convention member; documents require consular legalisation.",
        "consular_note": "The British Embassy in Monrovia is resident in Liberia and provides direct consular support.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "2-5 weeks standard",
        "dest_key": "liberia",
    },
    "benin": {
        "name": "Benin",
        "slug": "benin",
        "airport": "Cadjehoun Airport (COO), Cotonou",
        "reception": "The funeral director in Benin takes custody at the cargo terminal at Cadjehoun Airport (COO), Cotonou. Death is registered at the Tribunal de Premiere Instance, and Parquet clearance is required before remains can be exported. Benin is not a Hague Apostille Convention member; documents require legalisation. Documentation is issued in French.",
        "consular_note": "There is no resident British High Commission in Benin. Consular support comes from the British High Commission in Accra, Ghana, which provides non-resident coverage.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-35 days standard, longer from northern departments near the Burkina Faso border",
        "dest_key": "benin",
    },
    "burundi": {
        "name": "Burundi",
        "slug": "burundi",
        "airport": "Melchior Ndadaye International Airport (BJM), Bujumbura",
        "reception": "The funeral director in Burundi takes custody at the cargo terminal at Melchior Ndadaye International Airport (BJM), Bujumbura. Death is registered with the civil registry (registrar des actes de l'etat civil); the Parquet must authorise release for non-natural deaths. Burundi has been a Hague Apostille Convention member since 13 February 2015. Documentation is issued in Kirundi and French.",
        "consular_note": "There is no resident British High Commission in Burundi. Consular support comes from the British High Commission in Kampala, Uganda, which provides non-resident coverage.",
        "apostille": "Hague Apostille (2015)",
        "timeline": "14-42 days standard",
        "dest_key": "burundi",
    },
    "central-african-republic": {
        "name": "Central African Republic",
        "slug": "central-african-republic",
        "airport": "Bangui M'Poko International Airport (BGF)",
        "reception": "The funeral director in the Central African Republic takes custody at the cargo terminal at Bangui M'Poko International Airport (BGF). Death is registered through the etat civil in Bangui; the Forces Armees Centrafricaines or police, and in some cases the UN MINUSCA peacekeeping chain, must clear non-natural deaths. Central African Republic is not a Hague Apostille Convention member; documents require legalisation. Armed groups and the Russian Wagner Group (Africa Corps) hold significant influence outside the capital.",
        "consular_note": "There is no resident British Embassy in the Central African Republic. Consular support comes from the British Embassy in Yaounde, Cameroon, which provides non-resident coverage.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "28-90 days for cases in Bangui; areas outside Bangui are not achievable by civilian means",
        "dest_key": "central-african-republic",
    },
    "djibouti": {
        "name": "Djibouti",
        "slug": "djibouti",
        "airport": "Djibouti-Ambouli International Airport (JIB)",
        "reception": "The funeral director in Djibouti takes custody at the cargo terminal at Djibouti-Ambouli International Airport (JIB). Death is registered through the etat civil; the Tribunal de Premiere Instance must issue an order for non-natural deaths before the Ministry of Health export permit can be granted. Djibouti is not a Hague Apostille Convention member; documents require legalisation. Documentation is issued in French and Arabic.",
        "consular_note": "There is no resident British Embassy in Djibouti. Consular support comes from the British Embassy in Addis Ababa, Ethiopia, which provides non-resident coverage.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days standard",
        "dest_key": "djibouti",
    },
    "equatorial-guinea": {
        "name": "Equatorial Guinea",
        "slug": "equatorial-guinea",
        "airport": "Malabo Airport (SSG), Bioko Island",
        "reception": "The funeral director in Equatorial Guinea takes custody at the cargo terminal at Malabo Airport (SSG) on Bioko Island. Death is registered at the Registro Civil, and the Ministerio del Interior y Corporaciones Locales issues the export permit. Equatorial Guinea is not a Hague Apostille Convention member; documents require legalisation. Documentation is issued in Spanish. Deaths on the Rio Muni mainland require internal transfer to Malabo before international repatriation can proceed.",
        "consular_note": "There is no resident British High Commission in Equatorial Guinea. Consular support comes from the British High Commission in Yaounde, Cameroon, which provides non-resident coverage.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days standard, longer for mainland Rio Muni cases",
        "dest_key": "equatorial-guinea",
    },
    "gabon": {
        "name": "Gabon",
        "slug": "gabon",
        "airport": "Leon M'ba International Airport (LBV), Libreville",
        "reception": "The funeral director in Gabon takes custody at the cargo terminal at Leon M'ba International Airport (LBV), Libreville. Death is registered at the Tribunal de Premiere Instance, and Parquet clearance is required before the Ministere de l'Interieur issues the export permit. Gabon is not a Hague Apostille Convention member; documents require legalisation. Documentation is issued in French. A transitional military government (CTRI) has governed since the August 2023 coup.",
        "consular_note": "There is no resident British High Commission in Gabon. Consular support comes from the British High Commission in Yaounde, Cameroon, which provides non-resident coverage.",
        "apostille": "not a member; legalisation required",
        "timeline": "14-42 days standard, longer for remote forest provinces outside Libreville",
        "dest_key": "gabon",
    },
    "south-sudan": {
        "name": "South Sudan",
        "slug": "south-sudan",
        "airport": "Juba International Airport (JUB)",
        "reception": "The funeral director in South Sudan takes custody at the cargo terminal at Juba International Airport (JUB). Death is registered with the Office of the Registrar General, a system in place only since independence in 2011; the South Sudan National Police Service clears non-natural deaths before the Ministry of Health issues the export permit. South Sudan is not a Hague Apostille Convention member; documents require legalisation. Mortuary infrastructure exists in Juba but almost nowhere else.",
        "consular_note": "The British Embassy in Juba is resident in South Sudan and provides direct consular support, though its reach into conflict-affected states is limited.",
        "apostille": "not a member; legalisation required",
        "timeline": "21-90 days for Juba and accessible areas; Unity State, Upper Nile, and Equatoria conflict zones are not achievable by standard civilian means",
        "dest_key": "south-sudan",
    },
    "kiribati": {
        "name": "Kiribati",
        "slug": "kiribati",
        "airport": "Bonriki International Airport (TRW), South Tarawa, Gilbert Islands",
        "reception": "The funeral director in Kiribati takes custody at the cargo terminal at Bonriki International Airport (TRW), South Tarawa. Death is registered with the Kiribati Registration of Births, Deaths and Marriages, with the Kiribati Police Service clearing non-natural deaths. Kiribati is not a Hague Apostille Convention member; documents require legalisation. Kiribati's three island groups span roughly 3.5 million square kilometres of ocean; a death in the Phoenix Islands or the Line Islands (Kiritimati) requires transfer to South Tarawa or, for Kiritimati, may route via Honolulu instead.",
        "consular_note": "There is no resident British High Commission in Kiribati. Consular support comes from the British High Commission in Suva, Fiji, which provides non-resident coverage.",
        "apostille": "not a member; legalisation required",
        "timeline": "21-56 days standard, longer from the Phoenix or Line Islands groups",
        "dest_key": "kiribati",
    },
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
}

# ---------------------------------------------------------------------------
# Route definitions -- exact missing origin/destination combinations,
# confirmed by a direct filesystem check of site/content/routes/ against
# the 8-origin pool before this chunk was generated.
# ---------------------------------------------------------------------------

# R117: starts at template C (index 2). 25 routes.
R117_ROUTES = [
    ("netherlands", "tajikistan"),
    ("italy", "tajikistan"),
    ("norway", "tajikistan"),
    ("australia", "mali"),
    ("sweden", "mali"),
    ("belgium", "mali"),
    ("france", "niger"),
    ("canada", "niger"),
    ("netherlands", "niger"),
    ("italy", "chad"),
    ("norway", "chad"),
    ("sweden", "chad"),
    ("australia", "burkina-faso"),
    ("france", "burkina-faso"),
    ("belgium", "burkina-faso"),
    ("canada", "guinea"),
    ("netherlands", "guinea"),
    ("italy", "guinea"),
    ("norway", "guinea-bissau"),
    ("sweden", "guinea-bissau"),
    ("belgium", "guinea-bissau"),
    ("australia", "liberia"),
    ("france", "liberia"),
    ("canada", "liberia"),
    ("norway", "benin"),
]

# R118: starts at template C (index 2), continuing seamlessly from R117
# (25 is a multiple of 5, so the rotation index does not shift). 25 routes.
R118_ROUTES = [
    ("sweden", "benin"),
    ("belgium", "benin"),
    ("australia", "burundi"),
    ("france", "burundi"),
    ("canada", "burundi"),
    ("netherlands", "central-african-republic"),
    ("italy", "central-african-republic"),
    ("norway", "central-african-republic"),
    ("australia", "djibouti"),
    ("sweden", "djibouti"),
    ("belgium", "djibouti"),
    ("france", "equatorial-guinea"),
    ("canada", "equatorial-guinea"),
    ("netherlands", "equatorial-guinea"),
    ("italy", "gabon"),
    ("norway", "gabon"),
    ("sweden", "gabon"),
    ("australia", "south-sudan"),
    ("france", "south-sudan"),
    ("belgium", "south-sudan"),
    ("canada", "kiribati"),
    ("netherlands", "kiribati"),
    ("italy", "kiribati"),
    ("norway", "samoa"),
    ("sweden", "samoa"),
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
    "tajikistan": lambda origin: "Notify the British Embassy in Dushanbe, which is resident in Tajikistan though Embassy capacity is limited. Hague Apostille applies (Tajikistan joined 2015, though it does not apply between Tajikistan and Austria, Belgium, or Germany).",
    "mali": lambda origin: "Notify the British Embassy in Dakar, Senegal (no resident British post in Mali). Mali is not a Hague Apostille member; documents need consular legalisation, and the post-coup administrative environment can delay processing without explanation.",
    "niger": lambda origin: "Notify the British Embassy in Abuja, Nigeria (no resident British post in Niger). Niger is not a Hague Apostille member; documents need consular legalisation under the CNSP military junta administration.",
    "chad": lambda origin: "Notify the British Embassy in Yaounde, Cameroon (no resident British post in Chad). Chad is not a Hague Apostille member; documents need consular legalisation under the Transitional Military Council.",
    "burkina-faso": lambda origin: "Notify the British High Commission in Accra, Ghana (no resident British post in Burkina Faso). Burkina Faso is not a Hague Apostille member; documents need consular legalisation under the current military junta.",
    "guinea": lambda origin: "Notify the British High Commission in Freetown, Sierra Leone (no resident British post in Guinea). Guinea is not a Hague Apostille member; documents need consular legalisation, and Gendarmerie clearance is required alongside civil registration.",
    "guinea-bissau": lambda origin: "Notify the British Embassy in Dakar, Senegal (no resident British post in Guinea-Bissau). Guinea-Bissau is not a Hague Apostille member; documents need consular legalisation under the Portuguese civil law system.",
    "liberia": lambda origin: "Notify the British Embassy in Monrovia, which is resident in Liberia. Liberia is not a Hague Apostille member; documents need consular legalisation, though all documentation is in English, avoiding the translation step most West African corridors require.",
    "benin": lambda origin: "Notify the British High Commission in Accra, Ghana (no resident British post in Benin). Benin is not a Hague Apostille member; documents need legalisation, and the FCDO advises against all travel within 5km of the Burkina Faso border, which can affect deaths in the northern departments.",
    "burundi": lambda origin: "Notify the British High Commission in Kampala, Uganda (no resident British post in Burundi). Hague Apostille applies (Burundi joined 13 February 2015). Documentation in Kirundi or French requires certified English translation.",
    "central-african-republic": lambda origin: "Notify the British Embassy in Yaounde, Cameroon (no resident British post in the Central African Republic). The Central African Republic is not a Hague Apostille member; documents need legalisation, and armed groups including the Russian Wagner Group (Africa Corps) control most areas outside Bangui.",
    "djibouti": lambda origin: "Notify the British Embassy in Addis Ababa, Ethiopia (no resident British post in Djibouti). Djibouti is not a Hague Apostille member; documents need legalisation, and all documentation is issued in French and Arabic.",
    "equatorial-guinea": lambda origin: "Notify the British High Commission in Yaounde, Cameroon (no resident British post in Equatorial Guinea). Equatorial Guinea is not a Hague Apostille member; documents need legalisation, and mainland Rio Muni cases require internal transfer to Malabo on Bioko Island first.",
    "gabon": lambda origin: "Notify the British High Commission in Yaounde, Cameroon (no resident British post in Gabon). Gabon is not a Hague Apostille member; documents need legalisation, under the transitional military government (CTRI) that has governed since August 2023.",
    "south-sudan": lambda origin: "Notify the British Embassy in Juba, which is resident in South Sudan. South Sudan is not a Hague Apostille member; documents need legalisation, and the FCDO advises against all travel to Unity State, Upper Nile, and Equatoria conflict areas outside Juba.",
    "kiribati": lambda origin: "Notify the British High Commission in Suva, Fiji (no resident British post in Kiribati). Kiribati is not a Hague Apostille member; documents need legalisation, and the routing depends heavily on which of the three island groups the death occurred in.",
    "samoa": lambda origin: "Notify the New Zealand High Commission in Apia under the UK-New Zealand Consular Sharing Agreement (no resident British post in Samoa). Hague Apostille applies (Samoa joined 1999). English is an official language, so translation is rarely needed.",
}

DEST_RECEPTION_STEPS = {
    "tajikistan": "Funeral director in Tajikistan takes custody at the cargo terminal at Dushanbe Airport (DYU). Civil Status Registration Agency notified; no cremation facilities exist in Tajikistan.",
    "mali": "Funeral director in Mali takes custody at the cargo terminal at Bamako-Senou International Airport (BKO). Etat civil notified; death certificate (acte de deces) issued in French.",
    "niger": "Funeral director in Niger takes custody at the cargo terminal at Diori Hamani International Airport (NIM), Niamey. Local civil status office notified; Police Nationale issues clearance.",
    "chad": "Funeral director in Chad takes custody at the cargo terminal at Hassan Djamous N'Djamena International Airport (NDJ). Etat civil notified; death certificate (acte de deces) issued in French.",
    "burkina-faso": "Funeral director in Burkina Faso takes custody at the cargo terminal at Ouagadougou Airport (OUA). Etat civil notified; Tribunal de Grande Instance order required for non-natural deaths.",
    "guinea": "Funeral director in Guinea takes custody at the cargo terminal at Conakry-Gbessia International Airport (CKY). Etat civil notified alongside Gendarmerie clearance; death certificate (acte de deces) issued in French.",
    "guinea-bissau": "Funeral director in Guinea-Bissau takes custody at the cargo terminal at Osvaldo Vieira International Airport (OXB), Bissau. Conservatoria do Registo Civil notified; Ministerio da Administracao Territorial issues the export permit.",
    "liberia": "Funeral director in Liberia takes custody at the cargo terminal at Roberts International Airport (ROB), around 60km from Monrovia. Liberia National Police issues clearance where required; documentation is in English throughout.",
    "benin": "Funeral director in Benin takes custody at the cargo terminal at Cadjehoun Airport (COO), Cotonou. Tribunal de Premiere Instance notified; Parquet clearance confirmed before release.",
    "burundi": "Funeral director in Burundi takes custody at the cargo terminal at Melchior Ndadaye International Airport (BJM), Bujumbura. Civil registry notified; documentation in Kirundi or French.",
    "central-african-republic": "Funeral director in the Central African Republic takes custody at the cargo terminal at Bangui M'Poko International Airport (BGF). Etat civil notified; FACA or police clearance confirmed, with MINUSCA coordination where relevant.",
    "djibouti": "Funeral director in Djibouti takes custody at the cargo terminal at Djibouti-Ambouli International Airport (JIB). Etat civil notified; documentation issued in French and Arabic.",
    "equatorial-guinea": "Funeral director in Equatorial Guinea takes custody at the cargo terminal at Malabo Airport (SSG), Bioko Island. Registro Civil notified; mainland Rio Muni cases transfer to Malabo first.",
    "gabon": "Funeral director in Gabon takes custody at the cargo terminal at Leon M'ba International Airport (LBV), Libreville. Tribunal de Premiere Instance notified; Parquet clearance confirmed before release.",
    "south-sudan": "Funeral director in South Sudan takes custody at the cargo terminal at Juba International Airport (JUB). Office of the Registrar General notified; South Sudan National Police Service clearance confirmed for non-natural deaths.",
    "kiribati": "Funeral director in Kiribati takes custody at the cargo terminal at Bonriki International Airport (TRW), South Tarawa. Kiribati Registration of Births, Deaths and Marriages notified; Kiribati Police Service clearance confirmed for non-natural deaths.",
    "samoa": "Funeral director in Samoa takes custody at the cargo terminal at Faleolo International Airport (APW). Samoa Births, Deaths and Marriages Registration notified; documentation issued in English throughout.",
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
    "tajikistan": lambda origin: {
        "question": f"Is cremation available in Tajikistan for a family repatriating from {origin}?",
        "answer": (
            "No. Tajikistan has no cremation facilities at all, so full body repatriation to Tajikistan is the only option for families choosing "
            "this destination. Documents are issued in Tajik, using Cyrillic script, and often Russian, so certified English translation is required "
            "throughout for any documents that also need to be recognised in the UK."
        ),
    },
    "mali": lambda origin: {
        "question": f"Does the political situation in Mali affect a repatriation from {origin}?",
        "answer": (
            "Yes. Mali has been under military rule since the coup of May 2021, and the Transition government controls all civil administration, "
            "which can mean delays without explanation. Air France suspended its Bamako service in 2023, so cargo now routes via Addis Ababa, "
            "Casablanca, or Abidjan instead. There is no resident British Embassy; consular support comes from Dakar, Senegal."
        ),
    },
    "niger": lambda origin: {
        "question": f"How has the 2023 coup in Niger changed repatriation logistics from {origin}?",
        "answer": (
            "Significantly. A military junta, the CNSP, has governed Niger since the Presidential Guard's takeover in July 2023, and Air France "
            "suspended its Niamey service in the aftermath. Cargo now routes via Addis Ababa with Ethiopian Airlines or via Casablanca with Royal "
            "Air Maroc. There is no resident British Embassy; consular support comes from Abuja, Nigeria."
        ),
    },
    "chad": lambda origin: {
        "question": f"Are all areas of Chad accessible for a repatriation arranged from {origin}?",
        "answer": (
            "No. Chad's north, including the Tibesti and Borkou regions, and its eastern border areas facing spillover from the Sudan conflict, "
            "are not accessible by civilian means. Cases in N'Djamena and other accessible areas proceed through the etat civil under French civil "
            "law, with the British Embassy in Yaounde, Cameroon providing non-resident consular coverage."
        ),
    },
    "burkina-faso": lambda origin: {
        "question": f"What additional legal step applies to a non-natural death in Burkina Faso for a family in {origin}?",
        "answer": (
            "For any non-natural death, the Tribunal de Grande Instance, Burkina Faso's court of first instance, must issue a formal order before "
            "the death certificate can be released, a step most straightforward corridors on this site do not require. Northern, eastern, and western "
            "border regions are not achievable given current armed group activity; cases in Ouagadougou and accessible central areas proceed under "
            "the current military junta administration."
        ),
    },
    "guinea": lambda origin: {
        "question": f"Is Guinea the same country as Guinea-Bissau or Equatorial Guinea for a family arranging repatriation from {origin}?",
        "answer": (
            "No, these are three separate countries. This route is to the Republic of Guinea, capital Conakry, which operates French civil law and "
            "requires Gendarmerie clearance alongside the standard etat civil registration. Guinea-Bissau uses Portuguese civil law and Equatorial "
            "Guinea is a separate Central African state; confirm the correct country with your repatriation provider before booking."
        ),
    },
    "guinea-bissau": lambda origin: {
        "question": f"Does location within Guinea-Bissau affect how long a repatriation from {origin} takes?",
        "answer": (
            "Yes, considerably. Outside the capital, Bissau, civil registry offices, mortuaries, and health authorities have limited capacity, so "
            "documentation that takes days in the capital can take significantly longer in provincial or border areas. Osvaldo Vieira International "
            "Airport also has limited international cargo frequency, so routing options are narrower than in most Tier C corridors on this site."
        ),
    },
    "liberia": lambda origin: {
        "question": f"Does documentation from {origin} need translation for a repatriation to Liberia?",
        "answer": (
            "No, and this sets Liberia apart from most West African destinations on this site. Liberia was founded by freed American and Caribbean "
            "settlers in the 1820s and uses an English-language legal and administrative system throughout, so no certified translation step is "
            "needed for English-language documents. Roberts International Airport is around 60km from Monrovia, so a road transfer to the capital "
            "is still required."
        ),
    },
    "benin": lambda origin: {
        "question": f"Why does the Burkina Faso border matter for a repatriation from {origin} to Benin?",
        "answer": (
            "The FCDO advises against all travel within 5km of the Burkina Faso border, an area that has seen jihadist activity spill over "
            "from the Sahel since 2022. A death in the northern Alibori or Atacora departments can face access restrictions that a straightforward "
            "case in Cotonou would not, so a specialist should confirm the exact location before setting expectations on timing."
        ),
    },
    "burundi": lambda origin: {
        "question": f"Does Burundi's Hague Apostille membership speed up documents for a family in {origin}?",
        "answer": (
            "It helps, but it does not remove every step. Burundi joined the Hague Apostille Convention on 13 February 2015, which simplifies "
            "authentication compared to a non-member country. Documents are still issued in Kirundi or French, though, so certified English "
            "translation is required regardless of the Apostille stamp before UK authorities will accept them."
        ),
    },
    "central-african-republic": lambda origin: {
        "question": f"Is a repatriation from {origin} to the Central African Republic achievable outside Bangui?",
        "answer": (
            "No. The FCDO advises against all travel to every area of the Central African Republic outside Bangui, where armed groups and the "
            "Russian Wagner Group, now known as Africa Corps, hold significant territory. Even within Bangui itself the advisory is all but "
            "essential travel. A case is only workable where the death has occurred in the capital, and even then it can involve MINUSCA, the "
            "UN peacekeeping mission, alongside national authorities."
        ),
    },
    "djibouti": lambda origin: {
        "question": f"Why is Djibouti's documentation different from most other Horn of Africa corridors for a family in {origin}?",
        "answer": (
            "Djibouti issues civil documents in both French and Arabic, a legacy of its French colonial administration and its position at "
            "the Red Sea's southern entrance. Certified English translation is required for both languages. Natural deaths in Djibouti city "
            "typically clear in 14 to 21 days, but a Tribunal de Premiere Instance referral for a non-natural death adds a further 10 to 21 days."
        ),
    },
    "equatorial-guinea": lambda origin: {
        "question": f"Does it matter whether the death in Equatorial Guinea happened on the island or the mainland, for a repatriation from {origin}?",
        "answer": (
            "Yes, considerably. All international repatriation flights leave from Malabo Airport on Bioko Island. A death on the Rio Muni "
            "mainland, the enclave between Cameroon and Gabon, needs an internal transfer to Malabo first, over limited road infrastructure "
            "in some districts, before the international leg of the journey can even begin."
        ),
    },
    "gabon": lambda origin: {
        "question": f"Has the 2023 coup in Gabon affected repatriation processing for a family in {origin}?",
        "answer": (
            "The transitional military government, the CTRI under General Brice Clotaire Oligui Nguema, took power on 30 August 2023 and "
            "removed President Ali Bongo Ondimba after more than a decade in office. Courts and civil registry offices in Libreville continue "
            "to function, but processing times at government ministries can fluctuate during periods of political change, so build in some "
            "margin rather than assuming the fastest end of the range."
        ),
    },
    "south-sudan": lambda origin: {
        "question": f"Which parts of South Sudan can a specialist actually reach for a repatriation from {origin}?",
        "answer": (
            "Juba and the immediately accessible surrounding area are workable, with a resident British Embassy providing direct consular "
            "backing, a genuine advantage this route has over most others in this batch. Unity State, Upper Nile State, and Western and Central "
            "Equatoria outside Juba are under an FCDO advisory against all travel, and mortuary infrastructure barely exists once you leave the "
            "capital, so recovery from those areas is not something a civilian repatriation firm can promise."
        ),
    },
    "kiribati": lambda origin: {
        "question": f"Does it matter which of Kiribati's island groups the death occurred in, for a family in {origin}?",
        "answer": (
            "It changes the case completely. Kiribati's three groups, Gilbert, Phoenix, and Line Islands, are spread across roughly 3.5 million "
            "square kilometres of the Pacific. A death in the Gilbert Islands, where most people live, routes fairly directly through South "
            "Tarawa. A death in the remote Phoenix Islands can add weeks, and the Line Islands, including Kiritimati, sit over 3,500km east, "
            "close enough to route via Honolulu instead of back through South Tarawa. There is no political travel advisory here; the complexity "
            "is purely a function of geography."
        ),
    },
    "samoa": lambda origin: {
        "question": f"Does Samoa's Sunday observance actually delay a repatriation case from {origin}?",
        "answer": (
            "Yes, and it is worth planning around. Samoa observes Sunday strictly: government offices close, and official documentation does "
            "not move that day. A case reaching the Ministry of Health on a Saturday afternoon will typically wait until Monday to progress. "
            "On the plus side, English is an official language alongside Samoan, so death certificates and most paperwork need no translation, "
            "which is not the case for most Pacific destinations on this site."
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
        ("R117", R117_ROUTES, 2),  # Start at C (index 2), 25 routes
        ("R118", R118_ROUTES, 2),  # Start at C (index 2), continues seamlessly (25 is a multiple of 5)
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
