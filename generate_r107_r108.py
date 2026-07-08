#!/usr/bin/env python3
"""
generate_r107_r108.py -- Repatriate Service Route Generator
Chunks R107 and R108: 50 Tier C route pages, introducing ten new destinations
not previously covered anywhere in the route matrix. All ten already carry a
country hub, guide, and embassy-contacts page, so each has an existing
destination-hub link target.
R107: Benin x5, Burundi x5, Central African Republic x5, Djibouti x5, Equatorial Guinea x5
R108: Gabon x5, South Sudan x5, Kiribati x5, Samoa x5, Tonga x5
Origins: Australia, France, Canada, Netherlands, Italy, Norway, Sweden, Belgium
(established Tier C origin pool, reused verbatim from generate_r101_r102.py
through generate_r105_r106.py).
Template variants: both chunks start at C (index 2), continuing rotation from
R106 (ended on B, belgium-to-liberia).
Sources for destination facts: HCCH Apostille Convention status table
(hcch.net/en/instruments/conventions/status-table/?cid=41, fetched 8 July
2026) for Apostille membership and dates: Burundi (accession in force
13 February 2015), Samoa (accession in force 13 September 1999), Tonga
(succession in force 4 June 1970); Benin, Central African Republic,
Djibouti, Equatorial Guinea, Gabon, South Sudan, and Kiribati are not
listed as contracting parties. All operational detail (airports,
registration authority, embassy coverage, routing, security context) is
reused from this site's own existing country-hub pages for these ten
countries (site/content/countries/{slug}/_index.md), which were themselves
built from named FCDO travel-advice pages and embassy sources, not
invented fresh for this chunk.
"""
import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r97_r98.py / generate_r99_r100.py / generate_r101_r102.py /
# generate_r103_r104.py)
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
# Destination data -- ten new Tier C destinations, none previously covered
# anywhere in the route matrix. All ten already exist as origin countries
# (Tier A, R1-R4) with a built country hub, guide, and embassy-contacts page.
# Apostille status confirmed against the official HCCH status table
# (hcch.net/en/instruments/conventions/status-table/?cid=41, fetched 8 July
# 2026). Operational detail (airport, registry authority, embassy coverage,
# routing, security context) reused from this site's own existing
# country-hub pages, sourced there from FCDO travel advice and embassy
# contacts, not invented fresh here.
# ---------------------------------------------------------------------------

DEST_META = {
    "benin": {
        "name": "Benin",
        "slug": "benin",
        "display_name": "Benin",
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
        "display_name": "Burundi",
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
        "display_name": "Central African Republic",
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
        "display_name": "Djibouti",
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
        "display_name": "Equatorial Guinea",
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
        "display_name": "Gabon",
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
        "display_name": "South Sudan",
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
        "display_name": "Kiribati",
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
        "display_name": "Samoa",
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
        "display_name": "Tonga",
        "airport": "Fua'amotu International Airport (TBU), Tongatapu",
        "reception": "The funeral director in Tonga takes custody at the cargo terminal at Fua'amotu International Airport (TBU), Tongatapu. Death is registered with the Registrar General's Office, with a post-mortem from Vaiola Hospital where required, before the Ministry of Health issues the export permit. Tonga has been a Hague Apostille Convention member since 4 June 1970 (succession). Documentation is processed in English. Deaths in the Vava'u or Ha'apai groups need inter-island transfer first, and Vaiola Hospital has no hyperbaric decompression capacity, so diving-related incidents require medical evacuation before a repatriation case can begin.",
        "consular_note": "There is no resident British diplomatic post in Tonga. The Australian High Commission in Nuku'alofa provides consular assistance under the UK-Australia Consular Sharing Agreement, and the British High Commission in Wellington holds formal accreditation.",
        "apostille": "Hague Apostille (1970, succession)",
        "timeline": "18-30 days standard, add 1-2 days for Vava'u or Ha'apai, add 2-4 days for the Niuas",
        "dest_key": "tonga",
    },
}

# ---------------------------------------------------------------------------
# Route definitions. Origin rotation follows the same (3*i) mod 8 offset
# pattern used since generate_r97_r98.py across the 8-origin pool
# [australia, france, canada, netherlands, italy, norway, sweden, belgium].
# ---------------------------------------------------------------------------

# R107: starts at template C (index 2). 25 routes.
R107_ROUTES = [
    # Benin x5 (offset 0)
    ("australia", "benin"),
    ("france", "benin"),
    ("canada", "benin"),
    ("netherlands", "benin"),
    ("italy", "benin"),
    # Burundi x5 (offset 3)
    ("netherlands", "burundi"),
    ("italy", "burundi"),
    ("norway", "burundi"),
    ("sweden", "burundi"),
    ("belgium", "burundi"),
    # Central African Republic x5 (offset 6)
    ("sweden", "central-african-republic"),
    ("belgium", "central-african-republic"),
    ("australia", "central-african-republic"),
    ("france", "central-african-republic"),
    ("canada", "central-african-republic"),
    # Djibouti x5 (offset 1)
    ("france", "djibouti"),
    ("canada", "djibouti"),
    ("netherlands", "djibouti"),
    ("italy", "djibouti"),
    ("norway", "djibouti"),
    # Equatorial Guinea x5 (offset 4)
    ("italy", "equatorial-guinea"),
    ("norway", "equatorial-guinea"),
    ("sweden", "equatorial-guinea"),
    ("belgium", "equatorial-guinea"),
    ("australia", "equatorial-guinea"),
]

# R108: starts at template C (index 2). 25 routes.
R108_ROUTES = [
    # Gabon x5 (offset 7)
    ("belgium", "gabon"),
    ("australia", "gabon"),
    ("france", "gabon"),
    ("canada", "gabon"),
    ("netherlands", "gabon"),
    # South Sudan x5 (offset 2)
    ("canada", "south-sudan"),
    ("netherlands", "south-sudan"),
    ("italy", "south-sudan"),
    ("norway", "south-sudan"),
    ("sweden", "south-sudan"),
    # Kiribati x5 (offset 5)
    ("norway", "kiribati"),
    ("sweden", "kiribati"),
    ("belgium", "kiribati"),
    ("australia", "kiribati"),
    ("france", "kiribati"),
    # Samoa x5 (offset 0)
    ("australia", "samoa"),
    ("france", "samoa"),
    ("canada", "samoa"),
    ("netherlands", "samoa"),
    ("italy", "samoa"),
    # Tonga x5 (offset 3)
    ("netherlands", "tonga"),
    ("italy", "tonga"),
    ("norway", "tonga"),
    ("sweden", "tonga"),
    ("belgium", "tonga"),
]
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
    """Generate destination consular note."""
    return dest_data["consular_note"]


DEST_CONSULAR_LINES = {
    "benin": "Notify the British High Commission in Accra, Ghana (no resident British post in Benin). Benin is not a Hague Apostille member; documents need legalisation, and the FCDO advises against all travel within 5km of the Burkina Faso border, which can affect deaths in the northern departments.",
    "burundi": "Notify the British High Commission in Kampala, Uganda (no resident British post in Burundi). Hague Apostille applies (Burundi joined 13 February 2015). Documentation in Kirundi or French requires certified English translation.",
    "central-african-republic": "Notify the British Embassy in Yaounde, Cameroon (no resident British post in the Central African Republic). The Central African Republic is not a Hague Apostille member; documents need legalisation, and armed groups including the Russian Wagner Group (Africa Corps) control most areas outside Bangui.",
    "djibouti": "Notify the British Embassy in Addis Ababa, Ethiopia (no resident British post in Djibouti). Djibouti is not a Hague Apostille member; documents need legalisation, and all documentation is issued in French and Arabic.",
    "equatorial-guinea": "Notify the British High Commission in Yaounde, Cameroon (no resident British post in Equatorial Guinea). Equatorial Guinea is not a Hague Apostille member; documents need legalisation, and mainland Rio Muni cases require internal transfer to Malabo on Bioko Island first.",
    "gabon": "Notify the British High Commission in Yaounde, Cameroon (no resident British post in Gabon). Gabon is not a Hague Apostille member; documents need legalisation, under the transitional military government (CTRI) that has governed since August 2023.",
    "south-sudan": "Notify the British Embassy in Juba, which is resident in South Sudan. South Sudan is not a Hague Apostille member; documents need legalisation, and the FCDO advises against all travel to Unity State, Upper Nile, and Equatoria conflict areas outside Juba.",
    "kiribati": "Notify the British High Commission in Suva, Fiji (no resident British post in Kiribati). Kiribati is not a Hague Apostille member; documents need legalisation, and the routing depends heavily on which of the three island groups the death occurred in.",
    "samoa": "Notify the New Zealand High Commission in Apia under the UK-New Zealand Consular Sharing Agreement (no resident British post in Samoa). Hague Apostille applies (Samoa joined 1999). English is an official language, so translation is rarely needed.",
    "tonga": "Notify the Australian High Commission in Nuku'alofa under the UK-Australia Consular Sharing Agreement (no resident British post in Tonga). Hague Apostille applies (Tonga, succession, 1970). Documentation is processed in English throughout.",
}

DEST_RECEPTION_STEPS = {
    "benin": "Funeral director in Benin takes custody at the cargo terminal at Cadjehoun Airport (COO), Cotonou. Tribunal de Premiere Instance notified; Parquet clearance confirmed before release.",
    "burundi": "Funeral director in Burundi takes custody at the cargo terminal at Melchior Ndadaye International Airport (BJM), Bujumbura. Civil registry notified; documentation in Kirundi or French.",
    "central-african-republic": "Funeral director in the Central African Republic takes custody at the cargo terminal at Bangui M'Poko International Airport (BGF). Etat civil notified; FACA or police clearance confirmed, with MINUSCA coordination where relevant.",
    "djibouti": "Funeral director in Djibouti takes custody at the cargo terminal at Djibouti-Ambouli International Airport (JIB). Etat civil notified; documentation issued in French and Arabic.",
    "equatorial-guinea": "Funeral director in Equatorial Guinea takes custody at the cargo terminal at Malabo Airport (SSG), Bioko Island. Registro Civil notified; mainland Rio Muni cases transfer to Malabo first.",
    "gabon": "Funeral director in Gabon takes custody at the cargo terminal at Leon M'ba International Airport (LBV), Libreville. Tribunal de Premiere Instance notified; Parquet clearance confirmed before release.",
    "south-sudan": "Funeral director in South Sudan takes custody at the cargo terminal at Juba International Airport (JUB). Office of the Registrar General notified; South Sudan National Police Service clearance confirmed for non-natural deaths.",
    "kiribati": "Funeral director in Kiribati takes custody at the cargo terminal at Bonriki International Airport (TRW), South Tarawa. Kiribati Registration of Births, Deaths and Marriages notified; Kiribati Police Service clearance confirmed for non-natural deaths.",
    "samoa": "Funeral director in Samoa takes custody at the cargo terminal at Faleolo International Airport (APW). Samoa Births, Deaths and Marriages Registration notified; documentation issued in English throughout.",
    "tonga": "Funeral director in Tonga takes custody at the cargo terminal at Fua'amotu International Airport (TBU), Tongatapu. Registrar General's Office notified; documentation issued in English throughout.",
}

def make_timeline_steps(origin_data, dest_data):
    """Generate 7 timeline steps appropriate to the corridor."""
    origin = origin_data["name"]
    dest_airport = dest_data["airport"]
    cert = origin_data["death_cert"]
    doc_time = origin_data["doc_processing"]
    dest_key = dest_data["dest_key"]

    consular = DEST_CONSULAR_LINES.get(dest_key, f"Notify the {dest_data['name']} Embassy in {origin}.")
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
    "tonga": lambda origin: {
        "question": f"What happens if a death in Tonga involves diving or the Vava'u whale season, for a family in {origin}?",
        "answer": (
            "Vaiola Hospital on Tongatapu has no hyperbaric decompression capacity, so any diving-related incident, including those linked to "
            "the Vava'u whale-swimming season between July and October, requires medical evacuation before a repatriation case can properly "
            "begin. Tonga also sits in an active seismic and volcanic zone: the January 2022 Hunga Tonga eruption and tsunami cut communications "
            "and inter-island transport for weeks, so a specialist will check current conditions across the island group before confirming a timeline."
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

    # Both destinations are brand new to the matrix, so sideways links point
    # to the two Tier A routes that are guaranteed to already exist for every
    # origin in this batch (origin-to-UK and origin-to-Ireland).
    sideways = (
        f"/routes/{origin_key}-to-united-kingdom/", f"Repatriation from {o['name']} to the UK",
        f"/routes/{origin_key}-to-ireland/", f"Repatriation from {o['name']} to Ireland",
    )

    timeline_steps = make_timeline_steps(o, d)
    faqs = make_faqs(o, d)

    origin_hub_url = f"/repatriation-from-{origin_key}/"
    dest_hub_url = f"/repatriation-from-{d.get('hub_slug', dest_key)}/"
    dest_link_name = d["name"][4:] if d["name"].startswith("The ") else d["name"]

    intro_text = INTRO_VARS[page_index % 5].format(
        origin=o["name"], timeline_avg=o["timeline_avg"], dest_name=d["name"]
    )
    suffix_text = OVERVIEW_SUFFIX[page_index % 5]

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
    lines.append(f'date: 2026-07-08')
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
    lines.append(f'      text: "Full {dest_link_name} repatriation guide"')
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

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    all_batches = [
        ("R107", R107_ROUTES, 2),  # Start at C (index 2)
        ("R108", R108_ROUTES, 2),  # Start at C (index 2)
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
