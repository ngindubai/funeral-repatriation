#!/usr/bin/env python3
"""
generate_r103_r104.py -- Repatriate Service Route Generator
Chunks R103 and R104: 50 Tier C route pages, introducing ten new destinations
not previously covered anywhere in the route matrix.
R103: Andorra x5, Bhutan x5, Brunei x5, Haiti x5, Madagascar x5
R104: Eswatini x5, Mauritania x5, Comoros x5, Sao Tome and Principe x5, Togo x5
Origins: Australia, France, Canada, Netherlands, Italy, Norway, Sweden, Belgium
(established Tier C origin pool, reused verbatim from generate_r101_r102.py).
Template variants: both chunks start at C (index 2), continuing rotation from R102
(ended on B, netherlands-to-grenada).
Note: Vatican City was researched for this batch but dropped before generation.
It has no site/content/countries/vatican-city/ hub, guide, or embassy-contacts
page built yet, so a route page there would carry a broken destination-hub link.
Togo was substituted (hub, guide, and embassy pages all confirmed present).
Sources for new destination facts: HCCH Apostille status table (hcch.net, checked
July 2026), GOV.UK "British Embassy/High Commission" world-organisation pages and
GOV.UK bereavement/travel-advice pages (checked July 2026), Govern d'Andorra civil
registry pages, Bhutan Department of Civil Registration and Census, U.S. Embassy
Togo "Disposition of Remains" report (August 2019), Eswatini Ministry of Home
Affairs civil registration guidance as cited on GOV.UK, Mauritania and Haiti civil
registry detail via U.S. Department of State Visa Reciprocity and Civil Documents
pages, Sao Tome and Principe Direccao-Geral dos Registos e do Notariado.
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r97_r98.py / generate_r99_r100.py / generate_r101_r102.py)
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
# anywhere in the route matrix. Facts sourced from HCCH Apostille status
# table (hcch.net, checked July 2026), GOV.UK "British Embassy/High
# Commission" world-organisation pages and GOV.UK travel-advice pages (checked
# July 2026), and named national civil-registry sources per country. Where a
# fact could not be independently verified during research (for example, a
# specific local certificate language for some island states), it has been
# left out of the page rather than stated as fact, per CLAUDE.md rule 3.
# ---------------------------------------------------------------------------

DEST_META = {
    "andorra": {
        "name": "Andorra",
        "slug": "andorra",
        "display_name": "Andorra",
        "airport": "Barcelona-El Prat (BCN) or Toulouse-Blagnac (TLS), followed by a road transfer across the border",
        "reception": "The funeral director in Andorra takes custody after air cargo clears Barcelona-El Prat or Toulouse-Blagnac, followed by a road transfer across the border into Andorra. Death is registered with the Registre Civil (Civil Registry) of the Govern d'Andorra in Andorra la Vella. Andorra has been a Hague Apostille Convention member since 31 December 1996. The death certificate, the certificat de defuncio, is issued in Catalan.",
        "consular_note": "There is no British embassy or consulate in Andorra. Consular support comes from the British Consulate-General in Barcelona, under the British Embassy in Madrid.",
        "apostille": "Hague Apostille (1996)",
        "timeline": "2-4 weeks standard",
        "dest_key": "andorra",
    },
    "bhutan": {
        "name": "Bhutan",
        "slug": "bhutan",
        "display_name": "Bhutan",
        "airport": "Paro International Airport (PBH), Bhutan's only international airport",
        "reception": "The funeral director in Bhutan takes custody after air cargo clears Paro International Airport (PBH), the country's only international gateway, where landings are restricted to daylight hours and a small number of specially certified pilots. Death is registered with the Department of Civil Registration and Census (DCRC), Ministry of Home and Cultural Affairs, through the Bhutan Civil Registration System. Bhutan is not a Hague Apostille Convention member; documents require legalisation through Bhutan's Ministry of Foreign Affairs instead.",
        "consular_note": "There is no resident British embassy or consulate in Bhutan. Consular assistance comes from the British Deputy High Commission in Kolkata, India.",
        "apostille": "not a member; Ministry of Foreign Affairs legalisation required",
        "timeline": "3-6 weeks standard",
        "dest_key": "bhutan",
    },
    "brunei": {
        "name": "Brunei",
        "slug": "brunei",
        "display_name": "Brunei",
        "airport": "Brunei International Airport (BWN), Bandar Seri Begawan",
        "reception": "The funeral director in Brunei takes custody at the cargo terminal at Brunei International Airport (BWN), Bandar Seri Begawan. Death is registered with the Birth, Death and Adoption Section of the Immigration and National Registration Department, Ministry of Home Affairs. Brunei has been a Hague Apostille Convention member since 3 December 1987.",
        "consular_note": "The British High Commission in Bandar Seri Begawan is resident in Brunei and can register the death with UK authorities and advise on local funeral directors.",
        "apostille": "Hague Apostille (1987)",
        "timeline": "2-4 weeks standard",
        "dest_key": "brunei",
    },
    "haiti": {
        "name": "Haiti",
        "slug": "haiti",
        "display_name": "Haiti",
        "airport": "Toussaint Louverture International Airport (PAP), Port-au-Prince, which has faced repeated security-related flight suspensions",
        "reception": "The funeral director in Haiti takes custody after air cargo clears Toussaint Louverture International Airport (PAP), Port-au-Prince, though the airport has faced repeated flight suspensions linked to unrest. Death is registered with the local bureau d'etat civil (civil registry office); records are forwarded to the National Archives of Haiti. Haiti is not a Hague Apostille Convention member; documents require consular legalisation. The death certificate, the acte de deces, is issued in French.",
        "consular_note": "There is no resident British consular presence in Haiti. British nationals are covered by the British Embassy in Santo Domingo, Dominican Republic. The FCDO currently advises against all travel to Haiti.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "variable, often longer than 4-8 weeks given the current security situation",
        "dest_key": "haiti",
    },
    "madagascar": {
        "name": "Madagascar",
        "slug": "madagascar",
        "display_name": "Madagascar",
        "airport": "Ivato International Airport (TNR), Antananarivo",
        "reception": "The funeral director in Madagascar takes custody at the cargo terminal at Ivato International Airport (TNR), Antananarivo. Death is registered with the local commune's civil status officer, within 30 days, under Madagascar's 2018 civil registration law. Madagascar is not a Hague Apostille Convention member; documents require consular legalisation. The death certificate, the acte de deces, is issued in French.",
        "consular_note": "The British Embassy in Antananarivo is resident in Madagascar and can register the death with UK authorities and advise on local funeral directors.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "3-6 weeks standard",
        "dest_key": "madagascar",
    },
    "eswatini": {
        "name": "Eswatini",
        "slug": "eswatini",
        "display_name": "Eswatini",
        "airport": "King Mswati III International Airport (SHO), in the Lubombo region, Eswatini's sole international airport",
        "reception": "The funeral director in Eswatini takes custody at the cargo terminal at King Mswati III International Airport (SHO). Death is registered with the Ministry of Home Affairs' civil registration department within 60 days; a death outside hospital is certified instead by a stamped letter from the local Umphakatsi (traditional council) chief. Eswatini has been a Hague Apostille Convention member since its 1968 independence, through succession to an earlier UK extension of the Convention.",
        "consular_note": "A resident British High Commission is based in Mbabane, but it has no consular office. Consular support for British nationals comes from the British High Commission in Pretoria, South Africa.",
        "apostille": "Hague Apostille (1968, by succession)",
        "timeline": "2-4 weeks standard",
        "dest_key": "eswatini",
    },
    "mauritania": {
        "name": "Mauritania",
        "slug": "mauritania",
        "display_name": "Mauritania",
        "airport": "Nouakchott-Oumtounsy International Airport (NKC), opened in 2016",
        "reception": "The funeral director in Mauritania takes custody at the cargo terminal at Nouakchott-Oumtounsy International Airport (NKC). Death is registered at the Centre d'accueil des citoyens (citizen reception centre) of the commune where the death occurred, under the Agence Nationale du Registre des Populations et des Titres Securises. Mauritania is not a Hague Apostille Convention member; documents require consular legalisation. The death certificate, the Extrait d'acte de deces, is issued in French and Arabic.",
        "consular_note": "The British Embassy building in Nouakchott has no consular office. Consular support for British nationals comes from the British Embassy in Dakar, Senegal.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "3-6 weeks standard",
        "dest_key": "mauritania",
    },
    "comoros": {
        "name": "Comoros",
        "slug": "comoros",
        "display_name": "Comoros",
        "airport": "Prince Said Ibrahim International Airport (HAH), near Moroni, Comoros' only airport equipped for international flights",
        "reception": "The funeral director in Comoros takes custody at the cargo terminal at Prince Said Ibrahim International Airport (HAH), near Moroni. A death on the outer islands of Anjouan or Moheli requires an inter-island transfer to Grande Comore before an international departure or arrival can take place. Death is registered locally with the prefecture's civil registry (etat civil) where the death occurred. Comoros is not a Hague Apostille Convention member; documents require consular legalisation.",
        "consular_note": "There is no resident British embassy in Comoros. British nationals are covered by the British Embassy in Antananarivo, Madagascar, whose ambassador is also accredited to Comoros.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "3-6 weeks standard",
        "dest_key": "comoros",
    },
    "sao-tome-and-principe": {
        "name": "Sao Tome and Principe",
        "slug": "sao-tome-and-principe",
        "display_name": "Sao Tome and Principe",
        "airport": "Sao Tome International Airport (TMS), on Sao Tome island; Principe has its own smaller airport around 150km away",
        "reception": "The funeral director in Sao Tome and Principe takes custody at the cargo terminal at Sao Tome International Airport (TMS), the country's main gateway on Sao Tome island. Principe, roughly 150km away, has its own smaller airport, so a death there needs an inter-island transfer before international departure or arrival. Death is registered with the Conservatoria do Registo Civil, under the Direccao-Geral dos Registos e do Notariado. Sao Tome and Principe has been a Hague Apostille Convention member since 13 September 2008.",
        "consular_note": "There is no resident British embassy in Sao Tome and Principe. British nationals are covered by the British Embassy in Luanda, Angola, accredited to Sao Tome and Principe since 1980.",
        "apostille": "Hague Apostille (2008)",
        "timeline": "3-6 weeks standard",
        "dest_key": "sao-tome-and-principe",
    },
    "togo": {
        "name": "Togo",
        "slug": "togo",
        "display_name": "Togo",
        "airport": "Gnassingbe Eyadema International Airport (LFW), Lome",
        "reception": "The funeral director in Togo takes custody at the cargo terminal at Gnassingbe Eyadema International Airport (LFW), Lome. Death is registered through Togo's etat civil (civil registry) system. Togo is not a Hague Apostille Convention member; documents require consular legalisation. The death certificate, the acte de deces, is issued in French.",
        "consular_note": "There is no British embassy or consulate in Togo. Consular support for British nationals comes from the British Embassy in Abidjan, Cote d'Ivoire.",
        "apostille": "not a member; consular legalisation required",
        "timeline": "3-6 weeks standard",
        "dest_key": "togo",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R103: starts at template C (index 2). 25 routes.
R103_ROUTES = [
    # Andorra x5
    ("australia", "andorra"),
    ("france", "andorra"),
    ("canada", "andorra"),
    ("netherlands", "andorra"),
    ("italy", "andorra"),
    # Bhutan x5
    ("netherlands", "bhutan"),
    ("italy", "bhutan"),
    ("norway", "bhutan"),
    ("sweden", "bhutan"),
    ("belgium", "bhutan"),
    # Brunei x5
    ("sweden", "brunei"),
    ("belgium", "brunei"),
    ("australia", "brunei"),
    ("france", "brunei"),
    ("canada", "brunei"),
    # Haiti x5
    ("france", "haiti"),
    ("canada", "haiti"),
    ("netherlands", "haiti"),
    ("italy", "haiti"),
    ("norway", "haiti"),
    # Madagascar x5
    ("italy", "madagascar"),
    ("norway", "madagascar"),
    ("sweden", "madagascar"),
    ("belgium", "madagascar"),
    ("australia", "madagascar"),
]

# R104: starts at template C (index 2). 25 routes.
R104_ROUTES = [
    # Eswatini x5
    ("belgium", "eswatini"),
    ("australia", "eswatini"),
    ("france", "eswatini"),
    ("canada", "eswatini"),
    ("netherlands", "eswatini"),
    # Mauritania x5
    ("canada", "mauritania"),
    ("netherlands", "mauritania"),
    ("italy", "mauritania"),
    ("norway", "mauritania"),
    ("sweden", "mauritania"),
    # Comoros x5
    ("norway", "comoros"),
    ("sweden", "comoros"),
    ("belgium", "comoros"),
    ("australia", "comoros"),
    ("france", "comoros"),
    # Sao Tome and Principe x5
    ("australia", "sao-tome-and-principe"),
    ("france", "sao-tome-and-principe"),
    ("canada", "sao-tome-and-principe"),
    ("netherlands", "sao-tome-and-principe"),
    ("italy", "sao-tome-and-principe"),
    # Togo x5
    ("netherlands", "togo"),
    ("italy", "togo"),
    ("norway", "togo"),
    ("sweden", "togo"),
    ("belgium", "togo"),
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
    return dest_data["consular_note"]


DEST_CONSULAR_LINES = {
    "andorra": "Notify the British Consulate-General in Barcelona, under the British Embassy in Madrid (no British post in Andorra itself). Hague Apostille applies (Andorra joined 1996).",
    "bhutan": "Notify the British Deputy High Commission in Kolkata, India (no resident British post in Bhutan). Bhutan is not a Hague Apostille member; documents need Ministry of Foreign Affairs legalisation.",
    "brunei": "Notify the British High Commission in Bandar Seri Begawan, which is resident in Brunei. Hague Apostille applies (Brunei joined 1987).",
    "haiti": "Notify the British Embassy in Santo Domingo, Dominican Republic (no resident British post in Haiti). Haiti is not a Hague Apostille member; documents need consular legalisation.",
    "madagascar": "Notify the British Embassy in Antananarivo, which is resident in Madagascar. Madagascar is not a Hague Apostille member; documents need consular legalisation.",
    "eswatini": "Notify the British High Commission in Pretoria, South Africa (the Mbabane office has no consular function). Hague Apostille applies (Eswatini, member since 1968 independence).",
    "mauritania": "Notify the British Embassy in Dakar, Senegal (the Nouakchott office has no consular function). Mauritania is not a Hague Apostille member; documents need consular legalisation.",
    "comoros": "Notify the British Embassy in Antananarivo, Madagascar, which is also accredited to Comoros (no resident British post in Comoros itself). Comoros is not a Hague Apostille member; documents need consular legalisation.",
    "sao-tome-and-principe": "Notify the British Embassy in Luanda, Angola, accredited to Sao Tome and Principe since 1980 (no resident British post locally). Hague Apostille applies (Sao Tome and Principe joined 2008).",
    "togo": "Notify the British Embassy in Abidjan, Cote d'Ivoire (there is no British post in Togo). Togo is not a Hague Apostille member; documents need consular legalisation.",
}

DEST_RECEPTION_STEPS = {
    "andorra": "Funeral director in Andorra takes custody after air cargo clears Barcelona-El Prat or Toulouse-Blagnac, then a road transfer across the border. Registre Civil (Govern d'Andorra) notified. Death certificate (certificat de defuncio) issued in Catalan.",
    "bhutan": "Funeral director in Bhutan takes custody after air cargo clears Paro International Airport (PBH), Bhutan's only international gateway. Department of Civil Registration and Census (DCRC) notified via the Bhutan Civil Registration System.",
    "brunei": "Funeral director in Brunei takes custody at the cargo terminal at Brunei International Airport (BWN), Bandar Seri Begawan. Immigration and National Registration Department notified.",
    "haiti": "Funeral director in Haiti takes custody after air cargo clears Toussaint Louverture International Airport (PAP), Port-au-Prince. Local bureau d'etat civil notified; death certificate (acte de deces) issued in French.",
    "madagascar": "Funeral director in Madagascar takes custody at the cargo terminal at Ivato International Airport (TNR), Antananarivo. Local commune's civil status officer notified; death certificate (acte de deces) issued in French, within 30 days.",
    "eswatini": "Funeral director in Eswatini takes custody at the cargo terminal at King Mswati III International Airport (SHO). Ministry of Home Affairs civil registration department notified, within 60 days.",
    "mauritania": "Funeral director in Mauritania takes custody at the cargo terminal at Nouakchott-Oumtounsy International Airport (NKC). Centre d'accueil des citoyens notified; death certificate (Extrait d'acte de deces) issued in French and Arabic.",
    "comoros": "Funeral director in Comoros takes custody at the cargo terminal at Prince Said Ibrahim International Airport (HAH), near Moroni. Local prefecture's civil registry (etat civil) notified.",
    "sao-tome-and-principe": "Funeral director in Sao Tome and Principe takes custody at the cargo terminal at Sao Tome International Airport (TMS). Conservatoria do Registo Civil notified.",
    "togo": "Funeral director in Togo takes custody at the cargo terminal at Gnassingbe Eyadema International Airport (LFW), Lome. Togo's etat civil system notified; death certificate (acte de deces) issued in French.",
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
    "andorra": lambda origin: {
        "question": f"Why might a death certificate for someone repatriated to Andorra look different to what a {origin} family has seen before?",
        "answer": (
            "Since 2 January 2019, Andorra's Civil Registry, the Registre Civil, has been the sole issuer of every civil-status certificate, including death certificates. "
            "Parish and church registries that once recorded these events no longer issue certificates at all. "
            "The certificate itself, the certificat de defuncio, is issued in Catalan, so certified translation is required for UK use."
        ),
    },
    "bhutan": lambda origin: {
        "question": f"Are there any entry costs a family travelling from {origin} to Bhutan should know about?",
        "answer": (
            "Yes. Every visitor to Bhutan who is not a national of India, Bangladesh, or the Maldives pays a Sustainable Development Fee of 100 US dollars per person per night, "
            "plus a 40 US dollar visa fee, confirmed by the FCDO's Bhutan entry requirements guidance. "
            "This applies to any family member travelling to escort a repatriation or attend a funeral, on top of the funeral director's own logistics costs."
        ),
    },
    "brunei": lambda origin: {
        "question": f"Does Islamic law affect a repatriation from {origin} to Brunei?",
        "answer": (
            "Brunei applies Sharia law alongside its civil legal system, and Islamic funeral practice, which calls for prompt burial rather than cremation, "
            "governs local funeral arrangements. "
            "A family repatriating a non-Muslim relative should discuss the specific arrangements with a local funeral director in advance, "
            "since burial customs and timelines are shaped by this wider legal framework."
        ),
    },
    "haiti": lambda origin: {
        "question": f"Does the current security situation in Haiti affect a repatriation from {origin}?",
        "answer": (
            "Yes, significantly. The FCDO currently advises against all travel to Haiti, and Toussaint Louverture International Airport has faced repeated flight suspensions during periods of unrest. "
            "In areas under armed group control, families have sometimes had to submit a signed statement of unavailability in place of a death certificate that could not safely be collected. "
            "Speak to a specialist early. Timelines here are far less predictable than in most other corridors on this site."
        ),
    },
    "madagascar": lambda origin: {
        "question": f"Why does Madagascar's Apostille status matter for a repatriation from {origin}?",
        "answer": (
            "Madagascar has not joined the Hague Apostille Convention. "
            "Documents needing recognition in Madagascar, or Malagasy documents needing recognition back in the UK, require full consular legalisation rather than a single apostille stamp. "
            "This adds a legalisation step that most Tier A and Tier B corridors on this site do not need."
        ),
    },
    "eswatini": lambda origin: {
        "question": f"How is a death registered in Eswatini if it happens outside a hospital, for a family arranging repatriation from {origin}?",
        "answer": (
            "Differently to most corridors on this site. A hospital death produces a standard medical certificate. "
            "A death at home instead gets an officially stamped letter from the chief of the local Umphakatsi, the traditional council, standing in for the medical certificate. "
            "Registration with the Ministry of Home Affairs must happen within 60 days; late registration needs a sworn affidavit from a notary public."
        ),
    },
    "mauritania": lambda origin: {
        "question": f"Does Mauritanian law affect how a repatriation from {origin} is handled?",
        "answer": (
            "It can. Mauritania's 2001 Personal Status Code directs that matters the code does not directly address, which can include aspects of death and burial, "
            "are resolved by reference to Sharia, with the Moughataa Court holding competence over personal status and death-related civil matters. "
            "A specialist familiar with this framework should be involved from the outset."
        ),
    },
    "comoros": lambda origin: {
        "question": f"Does Comoros' island geography affect a repatriation from {origin}?",
        "answer": (
            "It can. Comoros is an archipelago, and Prince Said Ibrahim International Airport, near Moroni on Grande Comore, is the only airport equipped for international flights. "
            "A death on Anjouan or Moheli means an inter-island transfer to Grande Comore is needed before the case can proceed internationally, "
            "a step most single-island corridors on this site do not have."
        ),
    },
    "sao-tome-and-principe": lambda origin: {
        "question": f"Does the two-island geography of Sao Tome and Principe affect a repatriation from {origin}?",
        "answer": (
            "It can. Sao Tome and Principe is made up of two main islands around 150km apart. "
            "Sao Tome International Airport, on the larger island, is the country's main international gateway; Principe has its own smaller airport. "
            "A death on Principe needs an inter-island transfer before the case can proceed internationally."
        ),
    },
    "togo": lambda origin: {
        "question": f"Is cremation an option in Togo for a family repatriating from {origin}?",
        "answer": (
            "Yes, unusually for the region. Togo has one cremation facility, at the Hindu cemetery in Lome, though Togolese law requires a written expression of the deceased's wish to be cremated, "
            "or a written family statement in its place, and remains must be partially embalmed before the crematorium will accept them. "
            "Burial timelines are also tied to embalming status: unembalmed remains must be buried within 72 hours."
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
    lines.append(f'date: 2026-07-07')
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

def main():
    all_batches = [
        ("R103", R103_ROUTES, 2),  # Start at C (index 2)
        ("R104", R104_ROUTES, 2),  # Start at C (index 2)
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
