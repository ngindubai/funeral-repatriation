#!/usr/bin/env python3
"""
generate_r95_r96.py -- Repatriate Service Route Generator
Chunks R95 and R96: 50 Tier C route pages
R95: Ukraine x5, Bosnia x5, Serbia x5, Malta x5, Hungary x5
R96: Bulgaria x5, Czech Republic x5, Croatia x5, Iceland x5, Georgia x5
Origins: Australia, France, Canada, Netherlands, Italy, Norway, Sweden (and others from R93/R94 pool)
Template variants: Both R95 and R96 start at C (index 2)
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data
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
    "portugal": {
        "name": "Portugal",
        "slug": "portugal",
        "airport": "Lisbon Humberto Delgado (LIS), Porto Francisco Sa Carneiro (OPO), or Faro (FAO)",
        "emergency": "112",
        "death_cert": "certidao de obito (death certificate from the Conservatoria do Registo Civil)",
        "registry": "Conservatoria do Registo Civil (Civil Registry), Instituto dos Registos e do Notariado (IRN)",
        "language": "Portuguese",
        "apostille": True,
        "apostille_year": "1968",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Lisbon",
        "embassy_note": "The British Embassy in Lisbon can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 for emergency services. Death is registered at the local Conservatoria do Registo Civil within 48 hours. The official death certificate is the certidao de obito. The Ministerio Publico (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths. Portugal is a Hague Apostille Convention member since 1968. The British Embassy in Lisbon can assist British nationals. (FCDO Travel Advice Portugal 2025; Portuguese IRN civil registration procedures 2025.)",
        "police_note": "The Ministerio Publico takes jurisdiction for violent or suspicious deaths. Body release requires formal clearance before repatriation can proceed.",
        "source": "FCDO Travel Advice Portugal 2025; Portuguese IRN civil registration procedures 2025; Hague Conference Portugal profile 1968",
        "translation_note": "The certidao de obito is issued in Portuguese. Certified translation is required for non-Portuguese-speaking destinations.",
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
    "spain": {
        "name": "Spain",
        "slug": "spain",
        "airport": "Madrid Barajas (MAD), Barcelona El Prat (BCN), or other major Spanish airport",
        "emergency": "112",
        "death_cert": "certificado de defuncion (death certificate from the Registro Civil)",
        "registry": "Registro Civil (Civil Registry), Ministerio de Justicia",
        "language": "Spanish",
        "apostille": True,
        "apostille_year": "1978",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Madrid",
        "embassy_note": "The British Embassy in Madrid can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 for emergency services. Death must be declared at the local Registro Civil (Civil Registry, Ministerio de Justicia) within 24 hours. The official death certificate is the certificado de defuncion. The Fiscal (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths; a levantamiento del cadaver (judicial clearance) is required before the body can be moved. Spain is a Hague Apostille Convention member since 1978. The British Embassy in Madrid can assist British nationals. (FCDO Travel Advice Spain 2025; Spanish Ministerio de Justicia Registro Civil procedures 2025.)",
        "police_note": "The Fiscal investigates violent or suspicious deaths. A levantamiento del cadaver (judicial clearance) is required before the body can be released for repatriation.",
        "source": "FCDO Travel Advice Spain 2025; Spanish Ministerio de Justicia Registro Civil procedures 2025; Hague Conference Spain profile 1978",
        "translation_note": "The certificado de defuncion is issued in Spanish. Certified translation is required for non-Spanish-speaking destinations.",
    },
}

# ---------------------------------------------------------------------------
# Destination data
# ---------------------------------------------------------------------------

DEST_META = {
    "ukraine": {
        "name": "Ukraine",
        "slug": "ukraine",
        "display_name": "Ukraine",
        "airport": "Lviv Danylo Halytsky Airport (LWO) for limited international services; Kyiv Boryspil International Airport (KBP) suspended commercial operations in February 2022",
        "reception": "The Ukrainian funeral director takes custody at the cargo terminal. Death is registered with the State Registry of Civil Status Acts (DRACS, Derzhavnyi Reiestr Aktiv Tsyvilnoho Stanu), administered by the Ministry of Justice of Ukraine. Death certificates are issued in Ukrainian. Ukraine is a Hague Apostille Convention member since 2003, which simplifies document authentication. Kyiv Boryspil Airport (KBP) suspended commercial operations in February 2022; repatriation currently routes via Lviv (LWO) or through third countries such as Poland and Romania. Allow significantly extended timelines due to the ongoing armed conflict. FCDO advises against all travel to Ukraine.",
        "consular_note": "Ukrainian Embassy or Consulate in {origin_country}: contact the Ukrainian Embassy for documentation guidance. FCDO advises against all travel to Ukraine. Hague Apostille applies (Ukraine joined 2003). Transit routing via Poland or Romania is typically required.",
        "apostille": "Hague Apostille (2003). Direct flights are severely restricted since February 2022; transit via Poland or Romania is required.",
        "timeline": "8-16 weeks standard",
        "dest_key": "ukraine",
        "country_note": "FCDO advises against all travel to Ukraine since February 2022. Repatriation to Ukraine is possible but logistics are severely disrupted. Allow extended timelines and engage a specialist with Ukraine experience.",
    },
    "bosnia-and-herzegovina": {
        "name": "Bosnia",
        "slug": "bosnia-and-herzegovina",
        "display_name": "Bosnia and Herzegovina",
        "airport": "Sarajevo International Airport Butmir (SJJ), Mostar Airport (OMO), or Banja Luka Airport (BNX)",
        "reception": "The funeral director in Bosnia and Herzegovina takes custody at the cargo terminal. Death is registered with the maticna sluzba (civil registry department) within the relevant opstina (municipality). Death certificates are issued in Bosnian, Croatian, and Serbian. Bosnia and Herzegovina is a Hague Apostille Convention member since 2008, which simplifies document authentication for most Western documentation.",
        "consular_note": "Embassy of Bosnia and Herzegovina in {origin_country}: contact the Bosnian Embassy or Consulate for documentation guidance. Hague Apostille applies (Bosnia and Herzegovina joined 2008).",
        "apostille": "Hague Apostille (2008)",
        "timeline": "3-6 weeks standard",
        "dest_key": "bosnia-and-herzegovina",
        "country_note": "Bosnia and Herzegovina is a Hague Apostille member since 2008. Death certificates are trilingual (Bosnian, Croatian, Serbian). Certified translation may be required for non-regional language destinations.",
    },
    "serbia": {
        "name": "Serbia",
        "slug": "serbia",
        "display_name": "Serbia",
        "airport": "Belgrade Nikola Tesla Airport (BEG)",
        "reception": "The Serbian funeral director takes custody at the cargo terminal at Belgrade Nikola Tesla Airport (BEG). Death is registered with the opstina (municipal) civil status records office (Maticna knjiga umrlih). Death certificates are issued in Serbian in both Latin and Cyrillic scripts. Serbia is a Hague Apostille Convention member since 2001, which simplifies document authentication for Western documentation.",
        "consular_note": "Serbian Embassy in {origin_country}: contact the Serbian Embassy for documentation guidance. Hague Apostille applies (Serbia joined 2001 as successor state).",
        "apostille": "Hague Apostille (2001)",
        "timeline": "2-4 weeks standard",
        "dest_key": "serbia",
        "country_note": "Serbia is a Hague Apostille member since 2001. Death certificates are issued in Serbian in both Latin and Cyrillic scripts. Certified translation is required for non-Serbian-speaking destinations.",
    },
    "malta": {
        "name": "Malta",
        "slug": "malta",
        "display_name": "Malta",
        "airport": "Malta International Airport (MLA)",
        "reception": "The Maltese funeral director takes custody at the cargo terminal at Malta International Airport (MLA). Death is registered with the Public Registry Division (Identity Malta). Death certificates are issued in Maltese and English. Malta is a Hague Apostille Convention member since 1968 and an EU member state. Most Western documentation is accepted without additional legalisation, and the English-language process makes coordination straightforward.",
        "consular_note": "Maltese High Commission or Embassy in {origin_country}: contact the Maltese Embassy for documentation guidance. Hague Apostille applies (Malta joined 1968). Malta is an EU member state and a Commonwealth member.",
        "apostille": "Hague Apostille (1968)",
        "timeline": "2-4 weeks standard",
        "dest_key": "malta",
        "country_note": "Malta is a Hague Apostille member since 1968 and a Commonwealth member. Death certificates are bilingual (Maltese and English). This makes Malta one of the more straightforward European repatriation destinations.",
    },
    "hungary": {
        "name": "Hungary",
        "slug": "hungary",
        "display_name": "Hungary",
        "airport": "Budapest Ferenc Liszt International Airport (BUD)",
        "reception": "The Hungarian funeral director takes custody at the cargo terminal at Budapest Ferenc Liszt International Airport (BUD). Death is registered with the anyakonyvi hivatal (civil registry office), under the Belugyminiszterium (Ministry of Interior). Death certificates are issued in Hungarian. Hungary is a Hague Apostille Convention member since 1973 and an EU member state. Certified translation into Hungarian may be required for origin-country documentation.",
        "consular_note": "Hungarian Embassy in {origin_country}: contact the Hungarian Embassy for documentation guidance. Hague Apostille applies (Hungary joined 1973). Hungary is an EU member state.",
        "apostille": "Hague Apostille (1973)",
        "timeline": "2-4 weeks standard",
        "dest_key": "hungary",
        "country_note": "Hungary is a Hague Apostille member since 1973 and an EU member state. Death certificates are issued in Hungarian; certified translation of origin documents into Hungarian may be required.",
    },
    "bulgaria": {
        "name": "Bulgaria",
        "slug": "bulgaria",
        "display_name": "Bulgaria",
        "airport": "Sofia Airport (SOF), Varna International Airport (VAR), or Burgas Airport (BOJ)",
        "reception": "The Bulgarian funeral director takes custody at the cargo terminal at Sofia (SOF), Varna (VAR), or Burgas (BOJ). Death is registered with ESGRAON (civil registration system), administered by GRAO (Civil Registration and Administrative Services Directorate). Death certificates are issued in Bulgarian, which uses the Cyrillic script. Bulgaria is a Hague Apostille Convention member since 2001 and an EU member state. Certified translation into Bulgarian is required for all foreign-language documentation.",
        "consular_note": "Bulgarian Embassy in {origin_country}: contact the Bulgarian Embassy for documentation guidance. Hague Apostille applies (Bulgaria joined 2001). Bulgaria is an EU member state. Certified translation into Bulgarian is required.",
        "apostille": "Hague Apostille (2001)",
        "timeline": "2-4 weeks standard",
        "dest_key": "bulgaria",
        "country_note": "Bulgaria is a Hague Apostille member since 2001 and an EU member state. Death certificates use the Cyrillic script. Certified translation of all foreign documents into Bulgarian is required.",
    },
    "czech-republic": {
        "name": "Czech Republic",
        "slug": "czech-republic",
        "display_name": "Czech Republic",
        "airport": "Vaclav Havel Airport Prague (PRG)",
        "reception": "The Czech funeral director takes custody at the cargo terminal at Vaclav Havel Airport Prague (PRG). Death is registered with the matrika (civil registry) at the local magistrat or obecni urad (municipal office). Death certificates are issued in Czech. The Czech Republic is a Hague Apostille Convention member since 1998 and an EU member state. Certified translation into Czech is required for all foreign-language documentation.",
        "consular_note": "Czech Embassy in {origin_country}: contact the Czech Embassy for documentation guidance. Hague Apostille applies (Czech Republic joined 1998). Czech Republic is an EU member state.",
        "apostille": "Hague Apostille (1998)",
        "timeline": "2-4 weeks standard",
        "dest_key": "czech-republic",
        "country_note": "Czech Republic is a Hague Apostille member since 1998 and an EU member state. Death certificates are issued in Czech; certified translation of origin documentation into Czech is required.",
    },
    "croatia": {
        "name": "Croatia",
        "slug": "croatia",
        "display_name": "Croatia",
        "airport": "Zagreb Franjo Tudman Airport (ZAG), Split Airport (SPU), or Dubrovnik Airport (DBV)",
        "reception": "The Croatian funeral director takes custody at the cargo terminal at Zagreb (ZAG), Split (SPU), or Dubrovnik (DBV). Death is registered with the maticni ured (civil registry) within the local ured drzavne uprave (state administration office). Death certificates are issued in Croatian. Croatia is a Hague Apostille Convention member since 1991 and an EU member state (since 2013).",
        "consular_note": "Croatian Embassy in {origin_country}: contact the Croatian Embassy for documentation guidance. Hague Apostille applies (Croatia joined 1991). Croatia is an EU member state.",
        "apostille": "Hague Apostille (1991)",
        "timeline": "2-3 weeks standard",
        "dest_key": "croatia",
        "country_note": "Croatia is a Hague Apostille member since 1991 and an EU member state. The process is well-established for Western repatriations. Certified translation into Croatian may be required for documentation.",
    },
    "iceland": {
        "name": "Iceland",
        "slug": "iceland",
        "display_name": "Iceland",
        "airport": "Keflavik International Airport (KEF)",
        "reception": "The Icelandic funeral director takes custody at the cargo terminal at Keflavik International Airport (KEF). Death is registered with Thjodskra Islendinga (Registers Iceland, also known as the National Registry). Death certificates are issued in Icelandic. Iceland is a Hague Apostille Convention member since 1996. Certified translation into Icelandic may be required for non-Icelandic documentation.",
        "consular_note": "Icelandic Embassy or Ministry for Foreign Affairs in {origin_country}: contact the Icelandic Embassy for documentation guidance. Hague Apostille applies (Iceland joined 1996).",
        "apostille": "Hague Apostille (1996)",
        "timeline": "2-3 weeks standard",
        "dest_key": "iceland",
        "country_note": "Iceland is a Hague Apostille member since 1996. The process is straightforward for Western repatriations. Death certificates are issued in Icelandic; certified translation may be required.",
    },
    "georgia": {
        "name": "Georgia",
        "slug": "georgia",
        "display_name": "Georgia",
        "airport": "Tbilisi International Airport (TBS) or Batumi International Airport (BUS)",
        "reception": "The Georgian funeral director takes custody at the cargo terminal at Tbilisi (TBS) or Batumi (BUS). Death is registered with the Public Service Development Agency (PSDA) through its Justice Houses (Iusticiis Sakhli). Death certificates are issued in Georgian, which uses the Mkhedruli (Georgian) script. Georgia is a Hague Apostille Convention member since 2007. Certified translation of all foreign-language documentation into Georgian is required.",
        "consular_note": "Georgian Embassy in {origin_country}: contact the Georgian Embassy for documentation guidance. Hague Apostille applies (Georgia joined 2007). Certified translation of Georgian documents is required.",
        "apostille": "Hague Apostille (2007)",
        "timeline": "3-5 weeks standard",
        "dest_key": "georgia",
        "country_note": "Georgia is a Hague Apostille member since 2007. Death certificates use the Mkhedruli (Georgian) script. Certified translation of all foreign documents into Georgian is required.",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R95: starts at template C (index 2). 25 routes.
R95_ROUTES = [
    # Ukraine x5: Wave 2, Western and Scandinavian origins
    ("australia", "ukraine"),
    ("netherlands", "ukraine"),
    ("canada", "ukraine"),
    ("sweden", "ukraine"),
    ("italy", "ukraine"),
    # Bosnia x5: Wave 2, Western and Scandinavian origins
    ("australia", "bosnia-and-herzegovina"),
    ("italy", "bosnia-and-herzegovina"),
    ("netherlands", "bosnia-and-herzegovina"),
    ("canada", "bosnia-and-herzegovina"),
    ("norway", "bosnia-and-herzegovina"),
    # Serbia x5: Wave 2, Western and Scandinavian origins
    ("australia", "serbia"),
    ("italy", "serbia"),
    ("netherlands", "serbia"),
    ("canada", "serbia"),
    ("sweden", "serbia"),
    # Malta x5: Wave 2, Western European origins
    ("france", "malta"),
    ("canada", "malta"),
    ("norway", "malta"),
    ("sweden", "malta"),
    ("netherlands", "malta"),
    # Hungary x5: Wave 2, Western and Scandinavian origins
    ("australia", "hungary"),
    ("italy", "hungary"),
    ("netherlands", "hungary"),
    ("sweden", "hungary"),
    ("norway", "hungary"),
]

# R96: starts at template C (index 2). 25 routes.
R96_ROUTES = [
    # Bulgaria x5: Wave 2, Western and Scandinavian origins
    ("australia", "bulgaria"),
    ("italy", "bulgaria"),
    ("sweden", "bulgaria"),
    ("norway", "bulgaria"),
    ("canada", "bulgaria"),
    # Czech Republic x5: Wave 2, Western and Scandinavian origins
    ("australia", "czech-republic"),
    ("netherlands", "czech-republic"),
    ("italy", "czech-republic"),
    ("sweden", "czech-republic"),
    ("canada", "czech-republic"),
    # Croatia x5: Wave 2, Western and Scandinavian origins
    ("australia", "croatia"),
    ("france", "croatia"),
    ("netherlands", "croatia"),
    ("sweden", "croatia"),
    ("canada", "croatia"),
    # Iceland x5: Wave 2, Scandinavian and Western origins
    ("sweden", "iceland"),
    ("norway", "iceland"),
    ("australia", "iceland"),
    ("netherlands", "iceland"),
    ("canada", "iceland"),
    # Georgia x5: Wave 2, Western and Scandinavian origins
    ("australia", "georgia"),
    ("italy", "georgia"),
    ("canada", "georgia"),
    ("sweden", "georgia"),
    ("norway", "georgia"),
]

# ---------------------------------------------------------------------------
# Sideways link helpers
# ---------------------------------------------------------------------------

SIDEWAYS = {
    # Ukraine routes
    ("australia", "ukraine"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-ukraine/", "Repatriation from Germany to Ukraine",
    ),
    ("netherlands", "ukraine"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/france-to-ukraine/", "Repatriation from France to Ukraine",
    ),
    ("canada", "ukraine"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-ukraine/", "Repatriation from Germany to Ukraine",
    ),
    ("sweden", "ukraine"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/france-to-ukraine/", "Repatriation from France to Ukraine",
    ),
    ("italy", "ukraine"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/france-to-ukraine/", "Repatriation from France to Ukraine",
    ),
    # Bosnia routes
    ("australia", "bosnia-and-herzegovina"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-bosnia-and-herzegovina/", "Repatriation from Germany to Bosnia",
    ),
    ("italy", "bosnia-and-herzegovina"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/austria-to-bosnia-and-herzegovina/", "Repatriation from Austria to Bosnia",
    ),
    ("netherlands", "bosnia-and-herzegovina"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-bosnia-and-herzegovina/", "Repatriation from Germany to Bosnia",
    ),
    ("canada", "bosnia-and-herzegovina"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/france-to-bosnia-and-herzegovina/", "Repatriation from France to Bosnia",
    ),
    ("norway", "bosnia-and-herzegovina"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/sweden-to-bosnia-and-herzegovina/", "Repatriation from Sweden to Bosnia",
    ),
    # Serbia routes
    ("australia", "serbia"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-serbia/", "Repatriation from Germany to Serbia",
    ),
    ("italy", "serbia"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/austria-to-serbia/", "Repatriation from Austria to Serbia",
    ),
    ("netherlands", "serbia"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-serbia/", "Repatriation from Germany to Serbia",
    ),
    ("canada", "serbia"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/france-to-serbia/", "Repatriation from France to Serbia",
    ),
    ("sweden", "serbia"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/austria-to-serbia/", "Repatriation from Austria to Serbia",
    ),
    # Malta routes
    ("france", "malta"): (
        "/routes/france-to-united-kingdom/", "Repatriation from France to the UK",
        "/routes/italy-to-malta/", "Repatriation from Italy to Malta",
    ),
    ("canada", "malta"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-malta/", "Repatriation from Germany to Malta",
    ),
    ("norway", "malta"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/italy-to-malta/", "Repatriation from Italy to Malta",
    ),
    ("sweden", "malta"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/germany-to-malta/", "Repatriation from Germany to Malta",
    ),
    ("netherlands", "malta"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/australia-to-malta/", "Repatriation from Australia to Malta",
    ),
    # Hungary routes
    ("australia", "hungary"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-hungary/", "Repatriation from Germany to Hungary",
    ),
    ("italy", "hungary"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/austria-to-hungary/", "Repatriation from Austria to Hungary",
    ),
    ("netherlands", "hungary"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-hungary/", "Repatriation from Germany to Hungary",
    ),
    ("sweden", "hungary"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/france-to-hungary/", "Repatriation from France to Hungary",
    ),
    ("norway", "hungary"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/germany-to-hungary/", "Repatriation from Germany to Hungary",
    ),
    # Bulgaria routes
    ("australia", "bulgaria"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-bulgaria/", "Repatriation from Germany to Bulgaria",
    ),
    ("italy", "bulgaria"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/france-to-bulgaria/", "Repatriation from France to Bulgaria",
    ),
    ("sweden", "bulgaria"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/germany-to-bulgaria/", "Repatriation from Germany to Bulgaria",
    ),
    ("norway", "bulgaria"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/france-to-bulgaria/", "Repatriation from France to Bulgaria",
    ),
    ("canada", "bulgaria"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-bulgaria/", "Repatriation from Germany to Bulgaria",
    ),
    # Czech Republic routes
    ("australia", "czech-republic"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-czech-republic/", "Repatriation from Germany to the Czech Republic",
    ),
    ("netherlands", "czech-republic"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/austria-to-czech-republic/", "Repatriation from Austria to the Czech Republic",
    ),
    ("italy", "czech-republic"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/germany-to-czech-republic/", "Repatriation from Germany to the Czech Republic",
    ),
    ("sweden", "czech-republic"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/france-to-czech-republic/", "Repatriation from France to the Czech Republic",
    ),
    ("canada", "czech-republic"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-czech-republic/", "Repatriation from Germany to the Czech Republic",
    ),
    # Croatia routes
    ("australia", "croatia"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-croatia/", "Repatriation from Germany to Croatia",
    ),
    ("france", "croatia"): (
        "/routes/france-to-united-kingdom/", "Repatriation from France to the UK",
        "/routes/italy-to-croatia/", "Repatriation from Italy to Croatia",
    ),
    ("netherlands", "croatia"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-croatia/", "Repatriation from Germany to Croatia",
    ),
    ("sweden", "croatia"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/italy-to-croatia/", "Repatriation from Italy to Croatia",
    ),
    ("canada", "croatia"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-croatia/", "Repatriation from Germany to Croatia",
    ),
    # Iceland routes
    ("sweden", "iceland"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/france-to-iceland/", "Repatriation from France to Iceland",
    ),
    ("norway", "iceland"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/denmark-to-iceland/", "Repatriation from Denmark to Iceland",
    ),
    ("australia", "iceland"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-iceland/", "Repatriation from Germany to Iceland",
    ),
    ("netherlands", "iceland"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-iceland/", "Repatriation from Germany to Iceland",
    ),
    ("canada", "iceland"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/france-to-iceland/", "Repatriation from France to Iceland",
    ),
    # Georgia routes
    ("australia", "georgia"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-georgia/", "Repatriation from Germany to Georgia",
    ),
    ("italy", "georgia"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/france-to-georgia/", "Repatriation from France to Georgia",
    ),
    ("canada", "georgia"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-georgia/", "Repatriation from Germany to Georgia",
    ),
    ("sweden", "georgia"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/netherlands-to-georgia/", "Repatriation from the Netherlands to Georgia",
    ),
    ("norway", "georgia"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/germany-to-georgia/", "Repatriation from Germany to Georgia",
    ),
}

# ---------------------------------------------------------------------------
# Varied intro texts (to avoid repetitive patterns)
# ---------------------------------------------------------------------------

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

def make_title(origin_data, dest_data):
    """Generate an SEO-optimised title under 60 characters."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    title = f"{origin} to {dest}: Funeral Repatriation Guidance"
    if len(title) > 60:
        title = f"{origin} to {dest} Repatriation Guide"
    if len(title) > 60:
        title = f"{origin} to {dest} Repatriation"
    return title


def make_description(origin_data, dest_data):
    """Generate an SEO description under 155 characters with CTA."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    timeline = origin_data["timeline_avg"]
    desc = f"Death in {origin}, coming home to {dest}. Repatriation takes {timeline}. Consular support, all documentation handled. Contact us 24/7."
    if len(desc) > 155:
        desc = f"Death in {origin}. Repatriation to {dest} takes {timeline}. All documentation handled. Contact us 24/7."
    return desc


def make_embassy_note(dest_data, origin_name):
    """Generate destination consular note."""
    note = dest_data["consular_note"].replace("{origin_country}", origin_name)
    return note


def make_timeline_steps(origin_data, dest_data):
    """Generate 7 timeline steps appropriate to the corridor."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    dest_airport = dest_data["airport"]
    cert = origin_data["death_cert"]
    doc_time = origin_data["doc_processing"]
    dest_key = dest_data["dest_key"]

    if dest_key == "ukraine":
        consular = (
            f"Notify the Ukrainian Embassy or Consulate in {origin}. "
            "FCDO advises against all travel to Ukraine. Hague Apostille applies (2003). "
            "Engage a specialist with Ukraine repatriation experience."
        )
        reception_step = (
            "Ukrainian funeral director takes custody at cargo terminal. "
            "DRACS (State Registry of Civil Status Acts) notified. "
            "Hague Apostille applies (Ukraine joined 2003). "
            "Allow extended timelines due to ongoing armed conflict. "
            "Transit via Poland or Romania typically required."
        )
    elif dest_key == "bosnia-and-herzegovina":
        consular = f"Notify the Embassy of Bosnia and Herzegovina in {origin}. Hague Apostille applies (2008)."
        reception_step = (
            "Funeral director in Bosnia and Herzegovina takes custody at cargo terminal. "
            "Maticna sluzba (civil registry) at local opstina notified. "
            "Hague Apostille applies (Bosnia and Herzegovina joined 2008)."
        )
    elif dest_key == "serbia":
        consular = f"Notify the Serbian Embassy in {origin}. Hague Apostille applies (2001)."
        reception_step = (
            "Serbian funeral director takes custody at cargo terminal at Belgrade Nikola Tesla Airport (BEG). "
            "Opstina civil status records office (Maticna knjiga umrlih) notified. "
            "Hague Apostille applies (Serbia joined 2001). "
            "Death certificate issued in Serbian (Latin and Cyrillic scripts)."
        )
    elif dest_key == "malta":
        consular = (
            f"Notify the Maltese High Commission or Embassy in {origin}. "
            "Hague Apostille applies (Malta joined 1968). Malta is an EU member state."
        )
        reception_step = (
            "Maltese funeral director takes custody at cargo terminal at Malta International Airport (MLA). "
            "Public Registry Division (Identity Malta) notified. "
            "Hague Apostille applies (Malta joined 1968). "
            "Death certificate issued in Maltese and English."
        )
    elif dest_key == "hungary":
        consular = (
            f"Notify the Hungarian Embassy in {origin}. "
            "Hague Apostille applies (Hungary joined 1973). Hungary is an EU member state."
        )
        reception_step = (
            "Hungarian funeral director takes custody at cargo terminal at Budapest Ferenc Liszt Airport (BUD). "
            "Anyakonyvi hivatal (civil registry office) notified. "
            "Hague Apostille applies (Hungary joined 1973). "
            "Death certificate issued in Hungarian."
        )
    elif dest_key == "bulgaria":
        consular = (
            f"Notify the Bulgarian Embassy in {origin}. "
            "Hague Apostille applies (Bulgaria joined 2001). Bulgaria is an EU member state. "
            "Certified translation into Bulgarian is required."
        )
        reception_step = (
            "Bulgarian funeral director takes custody at cargo terminal at Sofia (SOF), Varna (VAR), or Burgas (BOJ). "
            "ESGRAON civil registration authority notified via GRAO. "
            "Hague Apostille applies (Bulgaria joined 2001). "
            "Death certificate issued in Bulgarian (Cyrillic script)."
        )
    elif dest_key == "czech-republic":
        consular = (
            f"Notify the Czech Embassy in {origin}. "
            "Hague Apostille applies (Czech Republic joined 1998). Czech Republic is an EU member state."
        )
        reception_step = (
            "Czech funeral director takes custody at cargo terminal at Vaclav Havel Airport Prague (PRG). "
            "Matrika (civil registry) at local magistrat or obecni urad notified. "
            "Hague Apostille applies (Czech Republic joined 1998). "
            "Death certificate issued in Czech."
        )
    elif dest_key == "croatia":
        consular = (
            f"Notify the Croatian Embassy in {origin}. "
            "Hague Apostille applies (Croatia joined 1991). Croatia is an EU member state."
        )
        reception_step = (
            "Croatian funeral director takes custody at cargo terminal at Zagreb (ZAG), Split (SPU), or Dubrovnik (DBV). "
            "Maticni ured (civil registry) within local ured drzavne uprave notified. "
            "Hague Apostille applies (Croatia joined 1991). "
            "Death certificate issued in Croatian."
        )
    elif dest_key == "iceland":
        consular = (
            f"Notify the Icelandic Embassy or Ministry for Foreign Affairs in {origin}. "
            "Hague Apostille applies (Iceland joined 1996)."
        )
        reception_step = (
            "Icelandic funeral director takes custody at cargo terminal at Keflavik International Airport (KEF). "
            "Thjodskra Islendinga (Registers Iceland) notified. "
            "Hague Apostille applies (Iceland joined 1996). "
            "Death certificate issued in Icelandic."
        )
    elif dest_key == "georgia":
        consular = (
            f"Notify the Georgian Embassy in {origin}. "
            "Hague Apostille applies (Georgia joined 2007). "
            "Certified translation of Georgian-language documents is required."
        )
        reception_step = (
            "Georgian funeral director takes custody at cargo terminal at Tbilisi (TBS) or Batumi (BUS). "
            "PSDA Justice House civil registry notified. "
            "Hague Apostille applies (Georgia joined 2007). "
            "Death certificate issued in Georgian (Mkhedruli script). "
            "Certified translation of all foreign documents into Georgian required."
        )
    else:
        consular = f"Notify the {dest} Embassy in {origin}."
        reception_step = f"{dest} funeral director takes custody at cargo terminal."

    # FCDO or DFA line
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
    dest = dest_data["name"]
    dest_key = dest_data["dest_key"]

    if dest_key == "ukraine":
        return {
            "question": f"What is the FCDO position on travel to Ukraine and how does it affect repatriation from {origin}?",
            "answer": (
                "FCDO advises against all travel to Ukraine since February 2022. "
                "Direct flights between most Western countries and Ukraine are suspended. "
                "Repatriation to Ukraine is possible but requires routing via third countries such as Poland or Romania. "
                "Ukraine is a Hague Apostille member since 2003, which helps with documentation. "
                "A specialist with Ukraine repatriation experience is essential for this corridor."
            ),
        }
    elif dest_key == "bosnia-and-herzegovina":
        return {
            "question": f"Does repatriation to Bosnia and Herzegovina require certified translation of documents from {origin}?",
            "answer": (
                "Bosnia and Herzegovina is a Hague Apostille Convention member since 2008. "
                "Documents from Hague member countries are generally accepted with an Apostille stamp rather than full legalisation. "
                "However, the civil registry in Bosnia and Herzegovina works in Bosnian, Croatian, and Serbian. "
                "Certified translation of any foreign-language documentation into one of these languages is required. "
                "A specialist will confirm exactly which documents need translating for your specific case."
            ),
        }
    elif dest_key == "serbia":
        return {
            "question": f"Is Serbia a Hague Apostille member and how does this affect repatriation from {origin}?",
            "answer": (
                "Serbia is a Hague Apostille Convention member since 2001 as a successor state of the former Federal Republic of Yugoslavia. "
                f"Documents issued in {origin}, which is also a Hague member, can be authenticated with an Apostille stamp rather than full consular legalisation. "
                "Death certificates in Serbia are issued in Serbian in both Latin and Cyrillic scripts. "
                "Certified translation of origin-country documents into Serbian may still be required by the receiving opstina."
            ),
        }
    elif dest_key == "malta":
        return {
            "question": f"Why is Malta considered one of the simpler European repatriation destinations from {origin}?",
            "answer": (
                "Malta combines three factors that simplify repatriation. "
                "It is a Hague Apostille member since 1968, an EU member state, and a Commonwealth member. "
                "Death certificates are issued in both Maltese and English, which reduces translation requirements. "
                "The Public Registry Division processes repatriation documentation efficiently. "
                f"{origin} is also a Hague member, so document authentication is straightforward on both ends."
            ),
        }
    elif dest_key == "hungary":
        return {
            "question": f"How does EU membership affect the repatriation process when bringing someone home to Hungary from {origin}?",
            "answer": (
                "Hungary is an EU member state and a Hague Apostille member since 1973. "
                "EU membership means Hungarian authorities are familiar with Western European documentation standards. "
                "The anyakonyvi hivatal (civil registry office) processes incoming repatriations through established procedures. "
                "Death certificates in Hungary are issued in Hungarian; certified translation of origin-country documents into Hungarian is typically required. "
                "The process is well-understood by Hungarian funeral directors who handle repatriations regularly."
            ),
        }
    elif dest_key == "bulgaria":
        return {
            "question": f"Do documents need to be translated into Bulgarian for repatriation from {origin} to Bulgaria?",
            "answer": (
                "Yes. Bulgarian death certificates use the Cyrillic script and all official civil registration is conducted in Bulgarian. "
                f"Documents from {origin} require certified translation into Bulgarian before they are accepted by ESGRAON (the civil registration authority). "
                "Bulgaria is a Hague Apostille member since 2001, so Apostille-stamped documents from other Hague members are accepted. "
                "Your repatriation specialist will arrange certified translation as part of the documentation process."
            ),
        }
    elif dest_key == "czech-republic":
        return {
            "question": f"How does EU membership simplify repatriation from {origin} to the Czech Republic?",
            "answer": (
                "The Czech Republic is an EU member state and a Hague Apostille member since 1998. "
                "EU membership means Czech funeral directors and civil registry officials are familiar with Western European documentation. "
                "Hague Apostille membership removes the need for full consular legalisation of documents. "
                "Death certificates are issued in Czech; certified translation of origin-country documents is required. "
                "The matrika (civil registry) at the local obecni urad processes incoming repatriations promptly once documentation is in order."
            ),
        }
    elif dest_key == "croatia":
        return {
            "question": f"What is the realistic timeline for repatriation from {origin} to Croatia?",
            "answer": (
                f"In a straightforward case, repatriation from {origin} to Croatia takes {dest_data['timeline']}. "
                "Croatia is a Hague Apostille member since 1991 and an EU member state, which means documentation processing is efficient. "
                "The maticni ured (civil registry) within the local ured drzavne uprave registers the death promptly on arrival. "
                "Delays occur when deaths are sudden or unexplained, requiring Croatian authorities to open an investigation before releasing the body for funeral arrangements."
            ),
        }
    elif dest_key == "iceland":
        return {
            "question": f"How does the Hague Apostille apply to repatriation from {origin} to Iceland?",
            "answer": (
                "Iceland is a Hague Apostille Convention member since 1996. "
                f"{origin} is also a Hague member, so documents can be authenticated with an Apostille stamp on both ends. "
                "This removes the need for full consular legalisation and speeds up the documentation process. "
                "Death certificates in Iceland are issued in Icelandic by Thjodskra Islendinga (Registers Iceland). "
                "Certified translation of Icelandic documents into the destination language is required when used abroad."
            ),
        }
    elif dest_key == "georgia":
        return {
            "question": f"What translation requirements apply when repatriating to Georgia from {origin}?",
            "answer": (
                "Georgia is a Hague Apostille member since 2007. "
                "However, the Georgian civil registry (PSDA Justice Houses) works exclusively in Georgian, which uses the Mkhedruli (Georgian) script. "
                f"All documentation from {origin} requires certified translation into Georgian before it is accepted. "
                "Your repatriation specialist will arrange this translation as part of the documentation process. "
                "Hague Apostille stamping applies to origin documents, but Georgian translation remains a firm requirement."
            ),
        }
    else:
        return {
            "question": f"What specialist support is available for repatriation from {origin} to {dest}?",
            "answer": (
                f"A specialist repatriation company can coordinate the full process from {origin} to {dest}, "
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
    title = make_title(o, d)
    description = make_description(o, d)
    sideways = SIDEWAYS.get((origin_key, dest_key), (
        f"/routes/{origin_key}-to-united-kingdom/", f"Repatriation from {o['name']} to the UK",
        f"/routes/germany-to-{dest_key}/", f"Repatriation from Germany to {d['name']}",
    ))

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
    lines.append(f'date: 2026-06-27')
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
    lines.append(f'  - "All {o["language"]}-language documentation requires certified translation where needed."')
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
        ("R95", R95_ROUTES, 2),   # Start at C (index 2)
        ("R96", R96_ROUTES, 2),   # Start at C (index 2)
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
