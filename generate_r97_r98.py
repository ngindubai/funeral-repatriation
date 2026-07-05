#!/usr/bin/env python3
"""
generate_r97_r98.py -- Repatriate Service Route Generator
Chunks R97 and R98: 50 Tier C route pages, introducing ten new destinations.
R97: North Macedonia x5, Montenegro x5, Armenia x5, Azerbaijan x5, Kazakhstan x5
R98: Kyrgyzstan x5, Mongolia x5, Luxembourg x5, Monaco x5, Costa Rica x5
Origins: Australia, France, Canada, Netherlands, Italy, Norway, Sweden, Belgium (from the established Tier C origin pool)
Template variants: Both R97 and R98 start at C (index 2), continuing rotation from R96 (ended on B).
Sources for new destination facts: HCCH status table (hcch.net), Schmidt & Schmidt apostille country
guides, national civil registry authority sites, GOV.UK travel advice, all checked July 2026.
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused from the established Tier C origin pool, generate_r95_r96.py)
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
        "translation_note": "Death certificates are issued in English or French depending on the province. Certified translation is required for non-English and non-French-speaking destinations.",
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
        "translation_note": "Death certificates are issued in French, Dutch, or German depending on region. Certified translation is required for non-Belgian language destinations.",
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
# Destination data -- ten new Tier C destinations
# ---------------------------------------------------------------------------

DEST_META = {
    "north-macedonia": {
        "name": "North Macedonia",
        "slug": "north-macedonia",
        "display_name": "North Macedonia",
        "airport": "Skopje International Airport (SKP)",
        "reception": "The North Macedonian funeral director takes custody at the cargo terminal at Skopje International Airport (SKP). Death is registered with the maticna sluzba (civil registry) under the Ministry of Justice. Apostille certification is issued through the Ministry of Justice and the network of 27 First Instance Courts. Death certificates are issued in Macedonian, which uses the Cyrillic script. North Macedonia is a Hague Apostille Convention member since 1993.",
        "consular_note": "Embassy of North Macedonia in {origin_country}: contact the North Macedonian Embassy for documentation guidance. Hague Apostille applies (North Macedonia joined 1993). Certified translation of Macedonian documents is required for non-Macedonian-speaking destinations.",
        "apostille": "Hague Apostille (1993)",
        "timeline": "2-4 weeks standard",
        "dest_key": "north-macedonia",
        "country_note": "North Macedonia is a Hague Apostille member since 1993. Death certificates use the Cyrillic script and are apostilled through 27 First Instance Courts rather than a single national office. Certified translation is required for non-Macedonian-speaking destinations.",
    },
    "montenegro": {
        "name": "Montenegro",
        "slug": "montenegro",
        "display_name": "Montenegro",
        "airport": "Podgorica Airport (TGD) or Tivat Airport (TIV)",
        "reception": "The Montenegrin funeral director takes custody at the cargo terminal at Podgorica (TGD) or Tivat (TIV). Death is registered by the maticar (civil registry officer) in the local opstina (municipality). Montenegro has been a party to the Vienna CIEC Convention of 8 September 1976 since independence, which allows multilingual death certificate extracts between contracting states without translation. Montenegro is also a Hague Apostille Convention member since 3 July 2006.",
        "consular_note": "Embassy of Montenegro in {origin_country}: contact the Montenegrin Embassy for documentation guidance. Hague Apostille applies (Montenegro joined 2006). CIEC multilingual extracts may remove the need for translation when the destination is also a CIEC member state.",
        "apostille": "Hague Apostille (2006)",
        "timeline": "2-4 weeks standard",
        "dest_key": "montenegro",
        "country_note": "Montenegro is a Hague Apostille member since 3 July 2006 and a CIEC Convention party, meaning multilingual death certificate extracts are available and translation is not always required for use in other CIEC states.",
    },
    "armenia": {
        "name": "Armenia",
        "slug": "armenia",
        "display_name": "Armenia",
        "airport": "Zvartnots International Airport (EVN), Yerevan",
        "reception": "The Armenian funeral director takes custody at the cargo terminal at Zvartnots International Airport (EVN) near Yerevan. Death is registered with one of 52 Civil Status Acts Registration (CSAR) territorial bodies under the Ministry of Justice. In Yerevan, registration and certificates are handled through the Civic Status Registration Department at the municipal funeral bureau. Armenia is a Hague Apostille Convention member since 1993. Death certificates are issued in Armenian.",
        "consular_note": "Embassy of Armenia in {origin_country}: contact the Armenian Embassy for documentation guidance. Hague Apostille applies (Armenia joined 1993). Certified translation into Armenian is required for foreign-language documentation.",
        "apostille": "Hague Apostille (1993)",
        "timeline": "2-4 weeks standard",
        "dest_key": "armenia",
        "country_note": "Armenia is a Hague Apostille member since 1993. Death registration runs through 52 Civil Status Acts Registration (CSAR) territorial bodies; in Yerevan this is handled by the municipal funeral bureau. Certified translation into Armenian is required for foreign documentation.",
    },
    "azerbaijan": {
        "name": "Azerbaijan",
        "slug": "azerbaijan",
        "display_name": "Azerbaijan",
        "airport": "Heydar Aliyev International Airport (GYD), Baku",
        "reception": "The Azerbaijani funeral director takes custody at the cargo terminal at Heydar Aliyev International Airport (GYD) in Baku. Death is registered at a district Civil Registry Office (VVAQ) or through an ASAN Xidmet (ASAN Service) one-stop centre. Azerbaijan is a Hague Apostille Convention member since 1 March 2005. Death certificates are issued in Azerbaijani.",
        "consular_note": "Embassy of Azerbaijan in {origin_country}: contact the Azerbaijani Embassy for documentation guidance. Hague Apostille applies (Azerbaijan joined 2005). Certified translation into Azerbaijani is required for foreign-language documentation.",
        "apostille": "Hague Apostille (2005)",
        "timeline": "2-4 weeks standard",
        "dest_key": "azerbaijan",
        "country_note": "Azerbaijan is a Hague Apostille member since 1 March 2005. Civil registry documents including death certificates can be issued through ASAN Xidmet one-stop service centres as well as district Civil Registry Offices (VVAQ). Certified translation into Azerbaijani is required.",
    },
    "kazakhstan": {
        "name": "Kazakhstan",
        "slug": "kazakhstan",
        "display_name": "Kazakhstan",
        "airport": "Almaty International Airport (ALA) or Astana International Airport (NQZ)",
        "reception": "The Kazakhstani funeral director takes custody at the cargo terminal at Almaty (ALA) or Astana (NQZ). Death is registered with a local RAGS civil registry office. Apostille certification of civil registry documents, including death certificates, is issued by the Ministry of Justice. Kazakhstan is a Hague Apostille Convention member since 30 January 2001. Death certificates are issued in Kazakh and Russian.",
        "consular_note": "Embassy of Kazakhstan in {origin_country}: contact the Kazakhstani Embassy for documentation guidance. Hague Apostille applies (Kazakhstan joined 2001). Certified translation may be required depending on the destination language.",
        "apostille": "Hague Apostille (2001)",
        "timeline": "2-4 weeks standard",
        "dest_key": "kazakhstan",
        "country_note": "Kazakhstan is a Hague Apostille member since 30 January 2001. Death certificates are issued in Kazakh and Russian through RAGS civil registry offices, with apostille certification handled by the Ministry of Justice.",
    },
    "kyrgyzstan": {
        "name": "Kyrgyzstan",
        "slug": "kyrgyzstan",
        "display_name": "Kyrgyzstan",
        "airport": "Manas International Airport (FRU), Bishkek",
        "reception": "The Kyrgyzstani funeral director takes custody at the cargo terminal at Manas International Airport (FRU) near Bishkek. Death is registered with the local civil registry office (civil status acts registration). Kyrgyzstan is a Hague Apostille Convention member since 31 July 2011. Death certificates are issued in Kyrgyz and Russian.",
        "consular_note": "Embassy of Kyrgyzstan in {origin_country}: contact the Kyrgyzstani Embassy for documentation guidance. Hague Apostille applies (Kyrgyzstan joined 2011). Certified translation may be required depending on the destination language.",
        "apostille": "Hague Apostille (2011)",
        "timeline": "3-5 weeks standard",
        "dest_key": "kyrgyzstan",
        "country_note": "Kyrgyzstan is a Hague Apostille member since 31 July 2011. Every international arrival of a deceased person routes through Manas International Airport near Bishkek, the country's principal air hub.",
    },
    "mongolia": {
        "name": "Mongolia",
        "slug": "mongolia",
        "display_name": "Mongolia",
        "airport": "Chinggis Khaan International Airport (ULN), Ulaanbaatar",
        "reception": "The Mongolian funeral director takes custody at the cargo terminal at Chinggis Khaan International Airport (ULN) in Ulaanbaatar. Death must be reported to the local civil registration office within 28 days; the Civil Registration Department of the General Authority for Intellectual Property and State Registration, under the Ministry of Justice and Home Affairs, issues the certificate. Apostille certification is handled separately by the Ministry of Foreign Affairs and Trade. Mongolia is a Hague Apostille Convention member since 31 December 2009. Death certificates are issued in Mongolian.",
        "consular_note": "Embassy of Mongolia in {origin_country}: contact the Mongolian Embassy for documentation guidance. Hague Apostille applies (Mongolia joined 2009). Certified translation into Mongolian is required for foreign-language documentation.",
        "apostille": "Hague Apostille (2009)",
        "timeline": "4-6 weeks standard",
        "dest_key": "mongolia",
        "country_note": "Mongolia is a Hague Apostille member since 31 December 2009. Ulaanbaatar's Chinggis Khaan International Airport is the only realistic reception point, and the country's size and low population density mean documentation should be allowed extra time to reach the Ministry of Foreign Affairs and Trade for apostille.",
    },
    "luxembourg": {
        "name": "Luxembourg",
        "slug": "luxembourg",
        "display_name": "Luxembourg",
        "airport": "Luxembourg Findel Airport (LUX)",
        "reception": "The Luxembourgish funeral director takes custody at the cargo terminal at Luxembourg Findel Airport (LUX). Death is registered at the local commune, where the acte de deces (death certificate) is issued. Legalisation and apostille of the acte de deces is handled by the legalisation service of the Ministry of Foreign and European Affairs. Luxembourg is a Hague Apostille Convention member since 3 June 1979.",
        "consular_note": "Embassy of Luxembourg in {origin_country}: contact the Luxembourgish Embassy for documentation guidance. Hague Apostille applies (Luxembourg joined 1979).",
        "apostille": "Hague Apostille (1979)",
        "timeline": "2-3 weeks standard",
        "dest_key": "luxembourg",
        "country_note": "Luxembourg is a Hague Apostille member since 3 June 1979. The acte de deces is issued at the local commune and legalised or apostilled by the Ministry of Foreign and European Affairs.",
    },
    "monaco": {
        "name": "Monaco",
        "slug": "monaco",
        "display_name": "Monaco",
        "airport": "No commercial airport. The nearest international gateway is Nice Cote d'Azur Airport (NCE) in France, with onward transfer by road",
        "reception": "The Monegasque funeral director takes custody following arrival via Nice Cote d'Azur Airport (NCE), since Monaco has no commercial airport of its own. Death is registered with the Etat Civil (Civil Registry) at the Mairie de Monaco (Monaco City Hall). Apostille certification is issued by Monaco's Department of Justice. Monaco is a Hague Apostille Convention member since 31 December 2002. Death certificates are issued in French.",
        "consular_note": "Consulate of Monaco in {origin_country}: contact the Monegasque Consulate for documentation guidance. Hague Apostille applies (Monaco joined 2002). Because Monaco has no international airport, every air cargo route runs via Nice, France, followed by a short road transfer.",
        "apostille": "Hague Apostille (2002)",
        "timeline": "2-3 weeks standard",
        "dest_key": "monaco",
        "country_note": "Monaco is a Hague Apostille member since 31 December 2002. Monaco has no commercial airport, so every repatriation to Monaco routes through Nice Cote d'Azur Airport in France, with a short road transfer to complete the journey.",
    },
    "costa-rica": {
        "name": "Costa Rica",
        "slug": "costa-rica",
        "display_name": "Costa Rica",
        "airport": "Juan Santamaria International Airport (SJO), San Jose",
        "reception": "The Costa Rican funeral director takes custody at the cargo terminal at Juan Santamaria International Airport (SJO) near San Jose. Death is registered with the Registro Civil, part of the Tribunal Supremo de Elecciones, Costa Rica's electoral authority rather than a justice ministry. Apostille certification is issued by the Ministry of Foreign Affairs and Worship in San Jose. Costa Rica joined the Hague Apostille Convention in 2011. Death certificates are issued in Spanish.",
        "consular_note": "Embassy of Costa Rica in {origin_country}: contact the Costa Rican Embassy for documentation guidance. Hague Apostille applies (Costa Rica joined 2011).",
        "apostille": "Hague Apostille (2011)",
        "timeline": "2-4 weeks standard",
        "dest_key": "costa-rica",
        "country_note": "Costa Rica joined the Hague Apostille Convention in 2011. Unusually, civil registration runs through the Registro Civil under the Tribunal Supremo de Elecciones, the national electoral authority, rather than a justice or interior ministry.",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R97: starts at template C (index 2). 25 routes.
R97_ROUTES = [
    # North Macedonia x5
    ("australia", "north-macedonia"),
    ("italy", "north-macedonia"),
    ("netherlands", "north-macedonia"),
    ("sweden", "north-macedonia"),
    ("canada", "north-macedonia"),
    # Montenegro x5
    ("france", "montenegro"),
    ("italy", "montenegro"),
    ("norway", "montenegro"),
    ("canada", "montenegro"),
    ("netherlands", "montenegro"),
    # Armenia x5
    ("australia", "armenia"),
    ("france", "armenia"),
    ("netherlands", "armenia"),
    ("sweden", "armenia"),
    ("italy", "armenia"),
    # Azerbaijan x5
    ("canada", "azerbaijan"),
    ("italy", "azerbaijan"),
    ("norway", "azerbaijan"),
    ("sweden", "azerbaijan"),
    ("netherlands", "azerbaijan"),
    # Kazakhstan x5
    ("australia", "kazakhstan"),
    ("canada", "kazakhstan"),
    ("france", "kazakhstan"),
    ("norway", "kazakhstan"),
    ("sweden", "kazakhstan"),
]

# R98: starts at template C (index 2). 25 routes.
R98_ROUTES = [
    # Kyrgyzstan x5
    ("netherlands", "kyrgyzstan"),
    ("italy", "kyrgyzstan"),
    ("canada", "kyrgyzstan"),
    ("australia", "kyrgyzstan"),
    ("sweden", "kyrgyzstan"),
    # Mongolia x5
    ("france", "mongolia"),
    ("norway", "mongolia"),
    ("netherlands", "mongolia"),
    ("canada", "mongolia"),
    ("italy", "mongolia"),
    # Luxembourg x5
    ("belgium", "luxembourg"),
    ("france", "luxembourg"),
    ("netherlands", "luxembourg"),
    ("sweden", "luxembourg"),
    ("canada", "luxembourg"),
    # Monaco x5
    ("france", "monaco"),
    ("italy", "monaco"),
    ("belgium", "monaco"),
    ("norway", "monaco"),
    ("sweden", "monaco"),
    # Costa Rica x5
    ("canada", "costa-rica"),
    ("netherlands", "costa-rica"),
    ("australia", "costa-rica"),
    ("sweden", "costa-rica"),
    ("norway", "costa-rica"),
]

# ---------------------------------------------------------------------------
# Varied title shapes, description openings, intro texts (burstiness and
# anti-template-footprint measures per CLAUDE.md canonical constants, 5 Jul 2026)
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
    note = dest_data["consular_note"].replace("{origin_country}", origin_name)
    return note


def make_timeline_steps(origin_data, dest_data):
    """Generate 7 timeline steps appropriate to the corridor."""
    origin = origin_data["name"]
    dest_airport = dest_data["airport"]
    cert = origin_data["death_cert"]
    doc_time = origin_data["doc_processing"]
    dest_key = dest_data["dest_key"]

    if dest_key == "north-macedonia":
        consular = f"Notify the Embassy of North Macedonia in {origin}. Hague Apostille applies (1993)."
        reception_step = (
            "North Macedonian funeral director takes custody at cargo terminal at Skopje International Airport (SKP). "
            "Maticna sluzba (civil registry) notified. Apostille issued through the Ministry of Justice and First Instance Courts. "
            "Death certificate issued in Macedonian (Cyrillic script)."
        )
    elif dest_key == "montenegro":
        consular = f"Notify the Embassy of Montenegro in {origin}. Hague Apostille applies (2006). Vienna CIEC Convention (1976) may apply for multilingual extracts."
        reception_step = (
            "Montenegrin funeral director takes custody at cargo terminal at Podgorica (TGD) or Tivat (TIV). "
            "Maticar (civil registry officer) at the local opstina notified. "
            "Hague Apostille applies (Montenegro joined 2006)."
        )
    elif dest_key == "armenia":
        consular = f"Notify the Embassy of Armenia in {origin}. Hague Apostille applies (1993)."
        reception_step = (
            "Armenian funeral director takes custody at cargo terminal at Zvartnots International Airport (EVN), Yerevan. "
            "Civil Status Acts Registration (CSAR) territorial body notified. "
            "Death certificate issued in Armenian. Certified translation required for foreign documentation."
        )
    elif dest_key == "azerbaijan":
        consular = f"Notify the Embassy of Azerbaijan in {origin}. Hague Apostille applies (2005)."
        reception_step = (
            "Azerbaijani funeral director takes custody at cargo terminal at Heydar Aliyev International Airport (GYD), Baku. "
            "District Civil Registry Office (VVAQ) or ASAN Xidmet centre notified. "
            "Death certificate issued in Azerbaijani."
        )
    elif dest_key == "kazakhstan":
        consular = f"Notify the Embassy of Kazakhstan in {origin}. Hague Apostille applies (2001)."
        reception_step = (
            "Kazakhstani funeral director takes custody at cargo terminal at Almaty (ALA) or Astana (NQZ). "
            "RAGS civil registry office notified. Apostille issued by the Ministry of Justice. "
            "Death certificate issued in Kazakh and Russian."
        )
    elif dest_key == "kyrgyzstan":
        consular = f"Notify the Embassy of Kyrgyzstan in {origin}. Hague Apostille applies (2011)."
        reception_step = (
            "Kyrgyzstani funeral director takes custody at cargo terminal at Manas International Airport (FRU), Bishkek. "
            "Local civil registry office notified. "
            "Death certificate issued in Kyrgyz and Russian."
        )
    elif dest_key == "mongolia":
        consular = f"Notify the Embassy of Mongolia in {origin}. Hague Apostille applies (2009). Allow extra time given Mongolia's size and low population density."
        reception_step = (
            "Mongolian funeral director takes custody at cargo terminal at Chinggis Khaan International Airport (ULN), Ulaanbaatar. "
            "Civil Registration Department (Ministry of Justice and Home Affairs) notified within the 28-day reporting window. "
            "Apostille issued separately by the Ministry of Foreign Affairs and Trade. "
            "Death certificate issued in Mongolian."
        )
    elif dest_key == "luxembourg":
        consular = f"Notify the Embassy of Luxembourg in {origin}. Hague Apostille applies (1979)."
        reception_step = (
            "Luxembourgish funeral director takes custody at cargo terminal at Luxembourg Findel Airport (LUX). "
            "Local commune civil registry notified. Acte de deces legalised or apostilled by the Ministry of Foreign and European Affairs."
        )
    elif dest_key == "monaco":
        consular = f"Notify the Consulate of Monaco in {origin}. Hague Apostille applies (2002). Route via Nice, France, since Monaco has no commercial airport."
        reception_step = (
            "Monegasque funeral director takes custody following arrival via Nice Cote d'Azur Airport (NCE) and a short road transfer, "
            "since Monaco has no commercial airport of its own. Etat Civil at the Mairie de Monaco notified. "
            "Death certificate issued in French."
        )
    elif dest_key == "costa-rica":
        consular = f"Notify the Embassy of Costa Rica in {origin}. Hague Apostille applies (2011)."
        reception_step = (
            "Costa Rican funeral director takes custody at cargo terminal at Juan Santamaria International Airport (SJO), San Jose. "
            "Registro Civil, part of the Tribunal Supremo de Elecciones, notified. "
            "Death certificate issued in Spanish."
        )
    else:
        consular = f"Notify the {dest_data['name']} Embassy in {origin}."
        reception_step = f"{dest_data['name']} funeral director takes custody at cargo terminal."

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


def make_dest_faq6(origin_data, dest_data):
    """Generate a destination-specific sixth FAQ."""
    origin = origin_data["name"]
    dest_key = dest_data["dest_key"]

    if dest_key == "north-macedonia":
        return {
            "question": f"Is North Macedonia a Hague Apostille member and how does this affect repatriation from {origin}?",
            "answer": (
                "North Macedonia is a Hague Apostille Convention member since 1993. "
                "Apostille certification is issued through the Ministry of Justice and a network of 27 First Instance Courts rather than a single national office. "
                "Death certificates are issued in Macedonian, which uses the Cyrillic script. "
                f"Certified translation of documents from {origin} into Macedonian is typically required by the receiving civil registry."
            ),
        }
    elif dest_key == "montenegro":
        return {
            "question": f"Does repatriation to Montenegro from {origin} require translated documents?",
            "answer": (
                "It depends. Montenegro is a party to the Vienna CIEC Convention of 1976, which allows multilingual civil status extracts, including death certificates, "
                "to be used between contracting states without translation. "
                "Montenegro is also a Hague Apostille member since 2006. "
                f"Whether translation is needed for a document from {origin} depends on whether {origin} is also a CIEC member. Your specialist will confirm this for your case."
            ),
        }
    elif dest_key == "armenia":
        return {
            "question": f"How is a death registered when repatriating from {origin} to Armenia?",
            "answer": (
                "Armenia's civil registration system runs through 52 Civil Status Acts Registration (CSAR) territorial bodies under the Ministry of Justice. "
                "In Yerevan specifically, death registration and certificates are handled through the Civic Status Registration Department at the municipal funeral bureau. "
                "Armenia is a Hague Apostille member since 1993. "
                f"Certified translation of documents from {origin} into Armenian is required before the receiving registry will accept them."
            ),
        }
    elif dest_key == "azerbaijan":
        return {
            "question": f"What is ASAN Xidmet and how does it affect repatriation from {origin} to Azerbaijan?",
            "answer": (
                "ASAN Xidmet (ASAN Service) is a network of one-stop government service centres in Azerbaijan that can issue civil registry documents, including death certificates, "
                "alongside the traditional district Civil Registry Offices (VVAQ). "
                "Azerbaijan is a Hague Apostille member since 2005. "
                f"Certified translation of documents from {origin} into Azerbaijani is required as part of the repatriation process."
            ),
        }
    elif dest_key == "kazakhstan":
        return {
            "question": f"Which cities handle international arrivals when repatriating from {origin} to Kazakhstan?",
            "answer": (
                "Kazakhstan has two major reception points: Almaty International Airport (ALA), the country's largest city, and Astana International Airport (NQZ), the capital. "
                "Which one applies depends on where the family and receiving funeral director are based. "
                "Kazakhstan is a Hague Apostille member since 30 January 2001, and death certificates are issued in Kazakh and Russian by RAGS civil registry offices."
            ),
        }
    elif dest_key == "kyrgyzstan":
        return {
            "question": f"What is the realistic timeline for repatriation from {origin} to Kyrgyzstan?",
            "answer": (
                f"In a straightforward case, repatriation from {origin} to Kyrgyzstan takes {dest_data['timeline']}. "
                "Kyrgyzstan is a Hague Apostille member since 31 July 2011, which simplifies authentication of origin-country documents. "
                "All international arrivals route through Manas International Airport near Bishkek. "
                "Delays are more likely when the death is sudden or unexplained and requires local investigation before the body is released."
            ),
        }
    elif dest_key == "mongolia":
        return {
            "question": f"Why does repatriation from {origin} to Mongolia typically take longer than to other Tier C destinations?",
            "answer": (
                f"Repatriation from {origin} to Mongolia takes {dest_data['timeline']}, longer than many comparable corridors. "
                "Mongolia's civil registration and its Hague Apostille certification are handled by two separate authorities, the Ministry of Justice and Home Affairs and the Ministry of Foreign Affairs and Trade, "
                "which adds a coordination step. "
                "Ulaanbaatar's Chinggis Khaan International Airport is the only realistic reception point given the country's size and low population density."
            ),
        }
    elif dest_key == "luxembourg":
        return {
            "question": f"Which authority handles apostille certification for repatriation from {origin} to Luxembourg?",
            "answer": (
                "The legalisation service of Luxembourg's Ministry of Foreign and European Affairs issues apostille certification for the acte de deces (death certificate), "
                "which is first obtained from the local commune where the death is registered. "
                "Luxembourg is a Hague Apostille member since 3 June 1979, so this is generally a straightforward process for documents arriving from other Hague member states."
            ),
        }
    elif dest_key == "monaco":
        return {
            "question": f"How does a repatriation from {origin} actually reach Monaco, given it has no airport?",
            "answer": (
                "Monaco has no commercial airport of its own. "
                "Every air cargo repatriation to Monaco lands at Nice Cote d'Azur Airport (NCE) in neighbouring France, followed by a short road transfer across the border. "
                "Monaco is a Hague Apostille member since 31 December 2002, and death is registered with the Etat Civil at the Mairie de Monaco once the body arrives."
            ),
        }
    elif dest_key == "costa-rica":
        return {
            "question": f"Which government body registers a death for repatriation from {origin} to Costa Rica?",
            "answer": (
                "Costa Rican civil registration, including death certificates, runs through the Registro Civil, which sits under the Tribunal Supremo de Elecciones, "
                "the country's electoral authority, rather than a justice or interior ministry as in most countries. "
                "Costa Rica joined the Hague Apostille Convention in 2011, and apostille certification is issued separately by the Ministry of Foreign Affairs and Worship in San Jose."
            ),
        }
    else:
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
    dest_hub_url = f"/repatriation-from-{dest_key}/"

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
    lines.append(f'date: 2026-07-04')
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
        ("R97", R97_ROUTES, 2),   # Start at C (index 2)
        ("R98", R98_ROUTES, 2),   # Start at C (index 2)
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
