#!/usr/bin/env python3
"""
generate_r93_r94.py -- Repatriate Service Route Generator
Chunks R93 and R94: 50 Tier C route pages
R93: Peru x5, Senegal x5, Iran x5, Ivory Coast x5, DRC x5
R94: Afghanistan x5, Libya x5, Tunisia x5, Syria x5, Russia x5
Origins: Australia, France, Canada, Portugal, Netherlands, Italy, Belgium, Norway, Sweden, Spain
Template variants: R93 and R94 both start at C (index 2)
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
        "police_note": "The coroner or medical examiner investigates sudden, violent, or unexplained deaths. Body release requires coroner's authorisation before repatriation can proceed.",
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
    "peru": {
        "name": "Peru",
        "slug": "peru",
        "display_name": "Peru",
        "airport": "Lima Jorge Chavez International Airport (LIM)",
        "reception": "The Peruvian funeral director takes custody at the cargo terminal. Death is registered with RENIEC (Registro Nacional de Identificacion y Estado Civil). The partida de defuncion (death certificate) is issued in Spanish. Peru joined the Hague Apostille Convention in 2011, which simplifies document authentication. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Peruvian Embassy in {origin_country}: contact the Peruvian Ministry of Foreign Affairs consular section for documentation guidance. Hague Apostille applies (Peru joined 2011).",
        "apostille": "Hague Apostille (2011)",
        "timeline": "3-5 weeks standard",
        "dest_key": "peru",
    },
    "senegal": {
        "name": "Senegal",
        "slug": "senegal",
        "display_name": "Senegal",
        "airport": "Blaise Diagne International Airport Dakar (DSS)",
        "reception": "The Senegalese funeral director takes custody at the cargo terminal. Death is registered with the Etat Civil (Centre National de l'Etat Civil, CNEC). Documents are issued in French. Senegal is not a Hague Apostille Convention member; full consular authentication through the Senegalese Embassy or Consulate in the origin country is required. All foreign-language documents require certified French translation. For Muslim remains, Islamic law procedures apply and prompt burial is expected.",
        "consular_note": "Senegalese Embassy in {origin_country}: contact the Senegalese Embassy or Consulate for documentation guidance. Senegal is not a Hague Apostille member; full consular authentication is required.",
        "apostille": "Senegal is not a Hague Apostille Convention member. Documents require authentication through the Senegalese Ministry of Foreign Affairs.",
        "timeline": "3-6 weeks standard",
        "dest_key": "senegal",
    },
    "iran": {
        "name": "Iran",
        "slug": "iran",
        "display_name": "Iran",
        "airport": "Tehran Imam Khomeini International Airport (IKA) or Mehrabad International Airport (THR)",
        "reception": "The Iranian funeral director takes custody at the cargo terminal. Death is registered with the National Organization for Civil Registration (NOCR, Sazman-e Sabt-e Ahval-e Keshvar). Death certificates are issued in Farsi (Persian). Iran is not a Hague Apostille Convention member; full consular authentication through the Iranian Embassy or Consulate in the origin country is required. All foreign documents require certified Farsi translation. For Muslim remains, Islamic law procedures apply and prompt burial is expected. The British Embassy in Tehran has not been operational since 2011; the Swiss Embassy acts as protecting power for UK interests.",
        "consular_note": "Iranian Embassy or Consulate in {origin_country}: contact the Iranian Embassy for consular guidance on repatriation documentation. Iran is not a Hague Apostille member; full consular authentication is required.",
        "apostille": "Iran is not a Hague Apostille Convention member. Full consular authentication through the Iranian Embassy or Consulate in the origin country is required.",
        "timeline": "8-16 weeks standard",
        "dest_key": "iran",
    },
    "ivory-coast": {
        "name": "Ivory Coast",
        "slug": "ivory-coast",
        "display_name": "Ivory Coast",
        "airport": "Felix Houphouet-Boigny International Airport Abidjan (ABJ)",
        "reception": "The Ivorian funeral director takes custody at the cargo terminal. Death is registered with the Etat Civil (commune-level civil registration, coordinated by the Centre National de l'Etat Civil, CNEC). Documents are issued in French. Ivory Coast is not a Hague Apostille Convention member; full consular authentication is required. All foreign-language documents require certified French translation.",
        "consular_note": "Ivory Coast Embassy in {origin_country}: contact the Ivorian Embassy or Consulate for documentation guidance. Ivory Coast is not a Hague Apostille member; full consular authentication is required.",
        "apostille": "Ivory Coast is not a Hague Apostille Convention member. Documents require authentication through the Ivorian Ministry of Foreign Affairs.",
        "timeline": "3-6 weeks standard",
        "dest_key": "ivory-coast",
    },
    "democratic-republic-of-the-congo": {
        "name": "DR Congo",
        "slug": "democratic-republic-of-the-congo",
        "display_name": "the DR Congo",
        "airport": "N'djili International Airport Kinshasa (FIH) or Lubumbashi International Airport (FBM)",
        "reception": "The Congolese funeral director takes custody at the cargo terminal at N'djili Airport Kinshasa (FIH) or Lubumbashi (FBM). Death is registered with the Office National de l'Etat Civil (ONEC). Documents are issued in French. The DRC is not a Hague Apostille Convention member; full consular authentication is required. All foreign-language documents require certified French translation. Infrastructure and security conditions vary significantly by region.",
        "consular_note": "DRC Embassy in {origin_country}: contact the Congolese Embassy or Consulate for documentation guidance. The DRC is not a Hague Apostille member; full consular authentication is required.",
        "apostille": "The DRC is not a Hague Apostille Convention member. Documents require authentication through the Congolese Ministry of Foreign Affairs.",
        "timeline": "6-12 weeks standard",
        "dest_key": "democratic-republic-of-the-congo",
    },
    "afghanistan": {
        "name": "Afghanistan",
        "slug": "afghanistan",
        "display_name": "Afghanistan",
        "airport": "Hamid Karzai International Airport Kabul (KBL)",
        "reception": "The Afghan funeral director takes custody at the cargo terminal. Civil registration and documentation are administered under Taliban-led authorities (from August 2021). All Western embassies in Kabul suspended operations in August 2021. Death certificates and export permits are issued in Dari and Pashto. Afghanistan is not a Hague Apostille Convention member. Full authentication through current Afghan authorities is required. A specialist repatriation company with Afghanistan experience is essential.",
        "consular_note": "There is no operational Western embassy in Kabul (all Western missions suspended August 2021). Contact the Afghan Embassy or Consulate in {origin_country} for guidance. A specialist repatriation company is essential.",
        "apostille": "Afghanistan is not a Hague Apostille Convention member. Full authentication through current Afghan authorities is required.",
        "timeline": "8-16 weeks standard",
        "dest_key": "afghanistan",
    },
    "libya": {
        "name": "Libya",
        "slug": "libya",
        "display_name": "Libya",
        "airport": "Mitiga International Airport Tripoli (MJI) or Benina International Airport Benghazi (BEN)",
        "reception": "The Libyan funeral director takes custody at the cargo terminal. Death is registered with the National Centre for Civil Status (NCCS). Documents are issued in Arabic. Libya is not a Hague Apostille Convention member; full consular authentication is required. The British Embassy in Tripoli suspended operations in 2014; British interests are handled by the FCDO. All foreign-language documents require certified Arabic translation.",
        "consular_note": "Libyan Embassy or Consulate in {origin_country}: contact the Libyan Embassy for documentation guidance. Note: the British Embassy in Tripoli suspended operations in 2014. Libya is not a Hague Apostille member.",
        "apostille": "Libya is not a Hague Apostille Convention member. Documents require authentication through the Libyan Ministry of Foreign Affairs.",
        "timeline": "8-16 weeks standard",
        "dest_key": "libya",
    },
    "tunisia": {
        "name": "Tunisia",
        "slug": "tunisia",
        "display_name": "Tunisia",
        "airport": "Tunis-Carthage International Airport (TUN) or Monastir Habib Bourguiba Airport (MIR)",
        "reception": "The Tunisian funeral director takes custody at the cargo terminal. Death is registered with the Bureau de l'Etat Civil (local civil status office). Documents are issued in Arabic, with French also widely used. Tunisia is not a Hague Apostille Convention member; full consular authentication through the Tunisian Embassy or Consulate in the origin country is required. For Muslim remains, Islamic law procedures apply and prompt burial is expected.",
        "consular_note": "Tunisian Embassy in {origin_country}: contact the Tunisian Embassy or Consulate for documentation guidance. Tunisia is not a Hague Apostille member; full consular authentication is required.",
        "apostille": "Tunisia is not a Hague Apostille Convention member. Documents require authentication through the Tunisian Ministry of Foreign Affairs.",
        "timeline": "3-6 weeks standard",
        "dest_key": "tunisia",
    },
    "syria": {
        "name": "Syria",
        "slug": "syria",
        "display_name": "Syria",
        "airport": "Damascus International Airport (DAM)",
        "reception": "The Syrian funeral director takes custody at the cargo terminal. Death is registered with the Civil Status Directorate. Documents are issued in Arabic. Syria is not a Hague Apostille Convention member; full consular authentication is required. The British Embassy in Damascus closed in March 2012. FCDO advises against all travel to Syria. A specialist repatriation company with Syria experience is essential.",
        "consular_note": "Syrian Embassy or Consulate in {origin_country}: contact the Syrian authorities for documentation guidance. Note: the British Embassy in Damascus closed in March 2012. Syria is not a Hague Apostille member.",
        "apostille": "Syria is not a Hague Apostille Convention member. Documents require authentication through the Syrian Ministry of Foreign Affairs.",
        "timeline": "8-16 weeks standard",
        "dest_key": "syria",
    },
    "russia": {
        "name": "Russia",
        "slug": "russia",
        "display_name": "Russia",
        "airport": "Moscow Sheremetyevo (SVO), Domodedovo (DME), or Vnukovo (VKO); or other major Russian airport",
        "reception": "The Russian funeral director takes custody at the cargo terminal. Death is registered with ZAGS (Zapis Aktov Grazhdanskogo Sostoyaniya, civil acts registration authority). Death certificates are issued in Russian. Russia is a Hague Apostille Convention member since 1992. However, since February 2022 FCDO advises against all travel to Russia. Direct flight connections between Russia and most Western countries are suspended. Repatriation routes may require transit via third countries; allow significantly longer timelines.",
        "consular_note": "Russian Embassy or Consulate in {origin_country}: contact the Russian Embassy for consular guidance. Note FCDO all-travel advisory for Russia since February 2022. Russia is a Hague Apostille member (1992) but direct flight connections from most Western countries are suspended.",
        "apostille": "Hague Apostille (1992). Note: direct air connections from most Western countries are suspended since February 2022; transit routing required.",
        "timeline": "6-16 weeks standard",
        "dest_key": "russia",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R93: starts at template C (index 2). 25 routes.
R93_ROUTES = [
    # Peru x5: Western Europe and Commonwealth origins
    ("australia", "peru"),
    ("france", "peru"),
    ("canada", "peru"),
    ("portugal", "peru"),
    ("netherlands", "peru"),
    # Senegal x5: Western Europe and Commonwealth origins
    ("italy", "senegal"),
    ("belgium", "senegal"),
    ("portugal", "senegal"),
    ("canada", "senegal"),
    ("australia", "senegal"),
    # Iran x5: Western Europe and Scandinavia
    ("canada", "iran"),
    ("italy", "iran"),
    ("norway", "iran"),
    ("sweden", "iran"),
    ("netherlands", "iran"),
    # Ivory Coast x5: Western Europe and Commonwealth
    ("italy", "ivory-coast"),
    ("portugal", "ivory-coast"),
    ("canada", "ivory-coast"),
    ("australia", "ivory-coast"),
    ("netherlands", "ivory-coast"),
    # DRC x5: Western Europe and Commonwealth
    ("australia", "democratic-republic-of-the-congo"),
    ("canada", "democratic-republic-of-the-congo"),
    ("portugal", "democratic-republic-of-the-congo"),
    ("italy", "democratic-republic-of-the-congo"),
    ("netherlands", "democratic-republic-of-the-congo"),
]

# R94: starts at template C (index 2). 25 routes.
R94_ROUTES = [
    # Afghanistan x5: Western Europe and Scandinavia
    ("france", "afghanistan"),
    ("italy", "afghanistan"),
    ("norway", "afghanistan"),
    ("sweden", "afghanistan"),
    ("netherlands", "afghanistan"),
    # Libya x5: Western Europe and Mediterranean
    ("canada", "libya"),
    ("australia", "libya"),
    ("netherlands", "libya"),
    ("belgium", "libya"),
    ("spain", "libya"),
    # Tunisia x5: Western Europe and Mediterranean
    ("canada", "tunisia"),
    ("australia", "tunisia"),
    ("netherlands", "tunisia"),
    ("spain", "tunisia"),
    ("portugal", "tunisia"),
    # Syria x5: Western Europe and Scandinavia
    ("canada", "syria"),
    ("australia", "syria"),
    ("italy", "syria"),
    ("netherlands", "syria"),
    ("norway", "syria"),
    # Russia x5: Western Europe and Scandinavia
    ("canada", "russia"),
    ("australia", "russia"),
    ("italy", "russia"),
    ("sweden", "russia"),
    ("norway", "russia"),
]

# ---------------------------------------------------------------------------
# Sideways link helpers
# ---------------------------------------------------------------------------

SIDEWAYS = {
    # Peru routes
    ("australia", "peru"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/spain-to-peru/", "Repatriation from Spain to Peru",
    ),
    ("france", "peru"): (
        "/routes/france-to-united-kingdom/", "Repatriation from France to the UK",
        "/routes/italy-to-peru/", "Repatriation from Italy to Peru",
    ),
    ("canada", "peru"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-peru/", "Repatriation from Germany to Peru",
    ),
    ("portugal", "peru"): (
        "/routes/portugal-to-united-kingdom/", "Repatriation from Portugal to the UK",
        "/routes/spain-to-peru/", "Repatriation from Spain to Peru",
    ),
    ("netherlands", "peru"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-peru/", "Repatriation from Germany to Peru",
    ),
    # Senegal routes
    ("italy", "senegal"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/france-to-senegal/", "Repatriation from France to Senegal",
    ),
    ("belgium", "senegal"): (
        "/routes/belgium-to-united-kingdom/", "Repatriation from Belgium to the UK",
        "/routes/spain-to-senegal/", "Repatriation from Spain to Senegal",
    ),
    ("portugal", "senegal"): (
        "/routes/portugal-to-united-kingdom/", "Repatriation from Portugal to the UK",
        "/routes/france-to-senegal/", "Repatriation from France to Senegal",
    ),
    ("canada", "senegal"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-senegal/", "Repatriation from Germany to Senegal",
    ),
    ("australia", "senegal"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/france-to-senegal/", "Repatriation from France to Senegal",
    ),
    # Iran routes
    ("canada", "iran"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/australia-to-iran/", "Repatriation from Australia to Iran",
    ),
    ("italy", "iran"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/france-to-iran/", "Repatriation from France to Iran",
    ),
    ("norway", "iran"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/germany-to-iran/", "Repatriation from Germany to Iran",
    ),
    ("sweden", "iran"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/france-to-iran/", "Repatriation from France to Iran",
    ),
    ("netherlands", "iran"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-iran/", "Repatriation from Germany to Iran",
    ),
    # Ivory Coast routes
    ("italy", "ivory-coast"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/france-to-ivory-coast/", "Repatriation from France to Ivory Coast",
    ),
    ("portugal", "ivory-coast"): (
        "/routes/portugal-to-united-kingdom/", "Repatriation from Portugal to the UK",
        "/routes/france-to-ivory-coast/", "Repatriation from France to Ivory Coast",
    ),
    ("canada", "ivory-coast"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/germany-to-ivory-coast/", "Repatriation from Germany to Ivory Coast",
    ),
    ("australia", "ivory-coast"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/france-to-ivory-coast/", "Repatriation from France to Ivory Coast",
    ),
    ("netherlands", "ivory-coast"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/belgium-to-ivory-coast/", "Repatriation from Belgium to Ivory Coast",
    ),
    # DRC routes
    ("australia", "democratic-republic-of-the-congo"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/france-to-democratic-republic-of-the-congo/", "Repatriation from France to the DR Congo",
    ),
    ("canada", "democratic-republic-of-the-congo"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/belgium-to-democratic-republic-of-the-congo/", "Repatriation from Belgium to the DR Congo",
    ),
    ("portugal", "democratic-republic-of-the-congo"): (
        "/routes/portugal-to-united-kingdom/", "Repatriation from Portugal to the UK",
        "/routes/france-to-democratic-republic-of-the-congo/", "Repatriation from France to the DR Congo",
    ),
    ("italy", "democratic-republic-of-the-congo"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/belgium-to-democratic-republic-of-the-congo/", "Repatriation from Belgium to the DR Congo",
    ),
    ("netherlands", "democratic-republic-of-the-congo"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/belgium-to-democratic-republic-of-the-congo/", "Repatriation from Belgium to the DR Congo",
    ),
    # Afghanistan routes
    ("france", "afghanistan"): (
        "/routes/france-to-united-kingdom/", "Repatriation from France to the UK",
        "/routes/germany-to-afghanistan/", "Repatriation from Germany to Afghanistan",
    ),
    ("italy", "afghanistan"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/germany-to-afghanistan/", "Repatriation from Germany to Afghanistan",
    ),
    ("norway", "afghanistan"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/australia-to-afghanistan/", "Repatriation from Australia to Afghanistan",
    ),
    ("sweden", "afghanistan"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/germany-to-afghanistan/", "Repatriation from Germany to Afghanistan",
    ),
    ("netherlands", "afghanistan"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/canada-to-afghanistan/", "Repatriation from Canada to Afghanistan",
    ),
    # Libya routes
    ("canada", "libya"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/france-to-libya/", "Repatriation from France to Libya",
    ),
    ("australia", "libya"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/italy-to-libya/", "Repatriation from Italy to Libya",
    ),
    ("netherlands", "libya"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-libya/", "Repatriation from Germany to Libya",
    ),
    ("belgium", "libya"): (
        "/routes/belgium-to-united-kingdom/", "Repatriation from Belgium to the UK",
        "/routes/france-to-libya/", "Repatriation from France to Libya",
    ),
    ("spain", "libya"): (
        "/routes/spain-to-united-kingdom/", "Repatriation from Spain to the UK",
        "/routes/italy-to-libya/", "Repatriation from Italy to Libya",
    ),
    # Tunisia routes
    ("canada", "tunisia"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/france-to-tunisia/", "Repatriation from France to Tunisia",
    ),
    ("australia", "tunisia"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/france-to-tunisia/", "Repatriation from France to Tunisia",
    ),
    ("netherlands", "tunisia"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-tunisia/", "Repatriation from Germany to Tunisia",
    ),
    ("spain", "tunisia"): (
        "/routes/spain-to-united-kingdom/", "Repatriation from Spain to the UK",
        "/routes/france-to-tunisia/", "Repatriation from France to Tunisia",
    ),
    ("portugal", "tunisia"): (
        "/routes/portugal-to-united-kingdom/", "Repatriation from Portugal to the UK",
        "/routes/france-to-tunisia/", "Repatriation from France to Tunisia",
    ),
    # Syria routes
    ("canada", "syria"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/france-to-syria/", "Repatriation from France to Syria",
    ),
    ("australia", "syria"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/france-to-syria/", "Repatriation from France to Syria",
    ),
    ("italy", "syria"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/germany-to-syria/", "Repatriation from Germany to Syria",
    ),
    ("netherlands", "syria"): (
        "/routes/netherlands-to-united-kingdom/", "Repatriation from the Netherlands to the UK",
        "/routes/germany-to-syria/", "Repatriation from Germany to Syria",
    ),
    ("norway", "syria"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/sweden-to-syria/", "Repatriation from Sweden to Syria",
    ),
    # Russia routes
    ("canada", "russia"): (
        "/routes/canada-to-united-kingdom/", "Repatriation from Canada to the UK",
        "/routes/france-to-russia/", "Repatriation from France to Russia",
    ),
    ("australia", "russia"): (
        "/routes/australia-to-united-kingdom/", "Repatriation from Australia to the UK",
        "/routes/germany-to-russia/", "Repatriation from Germany to Russia",
    ),
    ("italy", "russia"): (
        "/routes/italy-to-united-kingdom/", "Repatriation from Italy to the UK",
        "/routes/france-to-russia/", "Repatriation from France to Russia",
    ),
    ("sweden", "russia"): (
        "/routes/sweden-to-united-kingdom/", "Repatriation from Sweden to the UK",
        "/routes/finland-to-russia/", "Repatriation from Finland to Russia",
    ),
    ("norway", "russia"): (
        "/routes/norway-to-united-kingdom/", "Repatriation from Norway to the UK",
        "/routes/finland-to-russia/", "Repatriation from Finland to Russia",
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

    if dest_key == "peru":
        consular = f"Notify the Peruvian Embassy in {origin}."
        reception_step = "Peruvian funeral director takes custody at cargo terminal. RENIEC notified. Hague Apostille applies (Peru joined 2011)."
    elif dest_key == "senegal":
        consular = f"Notify the Senegalese Embassy in {origin}."
        reception_step = "Senegalese funeral director takes custody at cargo terminal. Etat Civil (CNEC) notified. Full consular authentication required."
    elif dest_key == "iran":
        consular = f"Notify the Iranian Embassy or Consulate in {origin}. Full consular authentication required. Iran is not a Hague Apostille member."
        reception_step = "Iranian funeral director takes custody at cargo terminal. NOCR notified. Death certificate issued in Farsi. Full consular authentication and certified Farsi translation required."
    elif dest_key == "ivory-coast":
        consular = f"Notify the Ivory Coast Embassy in {origin}."
        reception_step = "Ivorian funeral director takes custody at cargo terminal. Etat Civil (CNEC) notified. Full consular authentication required."
    elif dest_key == "democratic-republic-of-the-congo":
        consular = f"Notify the DRC Embassy in {origin}."
        reception_step = "Congolese funeral director takes custody at cargo terminal. ONEC notified. Full consular authentication required."
    elif dest_key == "afghanistan":
        consular = "No operational Western embassy in Kabul (all Western missions suspended August 2021). Contact your home country's Ministry of Foreign Affairs for current guidance on repatriation to Afghanistan."
        reception_step = "Afghan funeral director takes custody at cargo terminal. Authorities under Taliban administration (from August 2021). Death certificate in Dari and Pashto. Full authentication through Afghan authorities required."
    elif dest_key == "libya":
        consular = f"Notify the Libyan Embassy or Consulate in {origin}. FCDO 24-hour emergency line: +44 (0)20 7008 5000. The British Embassy Tripoli suspended operations in 2014."
        reception_step = "Libyan funeral director takes custody at cargo terminal. NCCS notified. Full consular authentication required."
    elif dest_key == "tunisia":
        consular = f"Notify the Tunisian Embassy in {origin}."
        reception_step = "Tunisian funeral director takes custody at cargo terminal. Bureau de l'Etat Civil notified. Full consular authentication required."
    elif dest_key == "syria":
        consular = f"Notify the Syrian Embassy or Consulate in {origin}. FCDO 24-hour emergency line: +44 (0)20 7008 5000. Note: British Embassy Damascus closed March 2012."
        reception_step = "Syrian funeral director takes custody at cargo terminal. Civil Status Directorate notified. Full consular authentication required."
    elif dest_key == "russia":
        consular = f"Notify the Russian Embassy or Consulate in {origin}. Note FCDO all-travel advisory for Russia since February 2022. Direct air connections are limited."
        reception_step = "Russian funeral director takes custody at cargo terminal. ZAGS notified. Hague Apostille applies (Russia joined 1992). Allow extended timelines due to current travel restrictions."
    else:
        consular = f"Notify the {dest} Embassy in {origin}."
        reception_step = f"{dest} funeral director takes custody at cargo terminal."

    # FCDO or DFA line
    if dest_key == "ireland":
        emergency_line = "Department of Foreign Affairs 24-hour line: +353 1 408 2000."
    else:
        emergency_line = "FCDO 24-hour emergency line: +44 (0)20 7008 5000."

    steps = [
        {
            "step": 1,
            "action": f"Immediate steps after death. Report to local emergency services and contact a specialist at once.",
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


def make_faqs(origin_data, dest_data):
    """Generate 5 FAQs for the corridor."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    timeline_avg = origin_data["timeline_avg"]
    timeline_fast = origin_data["timeline_fast"]
    timeline_complex = origin_data["timeline_complex"]
    cert = origin_data["death_cert"]

    # Use override consular FAQ if set
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


def build_page(origin_key, dest_key, variant):
    """Build the full YAML frontmatter for one route page."""
    o = ORIGIN_DATA[origin_key]
    d = DEST_META[dest_key]

    slug = f"{origin_key}-to-{dest_key}"
    title = make_title(o, d)
    description = make_description(o, d)
    sideways = SIDEWAYS.get((origin_key, dest_key), (
        f"/routes/{origin_key}-to-united-kingdom/", f"Repatriation from {o['name']} to the UK",
        f"/routes/france-to-{dest_key}/", f"Repatriation from France to {d['name']}",
    ))

    timeline_steps = make_timeline_steps(o, d)
    faqs = make_faqs(o, d)

    # Build upward links
    origin_hub_url = f"/repatriation-from-{origin_key}/"
    dest_hub_url = f"/repatriation-from-{dest_key}/"

    # Overview and direct answer
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
    lines.append(f'date: 2026-06-26')
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
        ("R93", R93_ROUTES, 2),   # Start at C (index 2)
        ("R94", R94_ROUTES, 2),   # Start at C (index 2)
    ]

    total_written = 0
    for chunk_name, routes, start_idx in all_batches:
        print(f"\n=== {chunk_name} ===")
        for i, (origin_key, dest_key) in enumerate(routes):
            variant_idx = (start_idx + i) % len(VARIANTS)
            variant = VARIANTS[variant_idx]
            slug = f"{origin_key}-to-{dest_key}"
            filepath = ROUTES_DIR / f"{slug}.md"

            if filepath.exists():
                print(f"  SKIP (exists): {slug}")
                continue

            content = build_page(origin_key, dest_key, variant)
            filepath.write_text(content, encoding="utf-8")
            print(f"  WROTE [{variant}]: {slug}")
            total_written += 1

    print(f"\nTotal pages written: {total_written}")


if __name__ == "__main__":
    main()
