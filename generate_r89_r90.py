#!/usr/bin/env python3
"""
generate_r89_r90.py -- Repatriate Service Route Generator
Chunks R89 and R90: 50 Tier C route pages
R89: Uganda x5, Cuba x5, Zimbabwe x5, Venezuela x5, Ecuador x5
R90: Romania x5, Poland x5, Lebanon x5, Tanzania x5, Cameroon x5
Template variants: R89 starts at C (index 2), R90 starts at C (index 2)
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
    "uganda": {
        "name": "Uganda",
        "slug": "uganda",
        "airport": "Entebbe International Airport (EBB)",
        "emergency": "999 or 112",
        "death_cert": "death certificate from the local government civil registry",
        "registry": "URSB (Uganda Registration Services Bureau)",
        "language": "English",
        "apostille": False,
        "complexity": "moderate",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "7-10 days",
        "embassy_city": "Nairobi",
        "embassy_note": "The British High Commission in Kampala can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (999 or 112). Death must be registered with the local government civil registry within 3 days. The Uganda Police Force takes jurisdiction for violent, suspicious, or unexplained deaths. The British High Commission in Kampala provides consular support. URSB issues the death certificate, which is in English, within 7 days of registration.",
        "police_note": "The Uganda Police Force may investigate violent or sudden deaths before authorising release.",
        "source": "FCDO Travel Advice Uganda 2025; URSB registration procedures 2025",
        "translation_note": "Death certificates are issued in English. No translation is required for English-speaking destinations.",
    },
    "cuba": {
        "name": "Cuba",
        "slug": "cuba",
        "airport": "Jose Marti International Airport Havana (HAV) or Varadero (VRA)",
        "emergency": "106",
        "death_cert": "certificado de defuncion (Registro del Estado Civil)",
        "registry": "Registro del Estado Civil; Fiscalia (Prosecutor's Office) for suspicious deaths",
        "language": "Spanish",
        "apostille": False,
        "complexity": "moderate",
        "timeline_avg": "3-5 weeks",
        "timeline_fast": "2-3 weeks",
        "timeline_complex": "6-10 weeks",
        "doc_processing": "10-14 days",
        "embassy_city": "Havana",
        "embassy_note": "The British Embassy in Havana can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (106). Death must be registered with the Registro del Estado Civil. The Fiscalia takes jurisdiction for violent, suspicious, or unexplained deaths. All documentation is in Spanish and requires certified English translation before acceptance in English-speaking destinations. The state controls all funeral services, so a specialist repatriation company must coordinate locally through approved channels.",
        "police_note": "The Fiscalia (Prosecutor's Office) investigates violent or suspicious deaths. This can add 2-4 weeks to the process.",
        "source": "FCDO Travel Advice Cuba 2025; Cuban Ministry of Justice Registro del Estado Civil regulations",
        "translation_note": "All Cuban documents are in Spanish. Certified English translation is required for every document before UK, Irish, or Commonwealth destination acceptance.",
    },
    "zimbabwe": {
        "name": "Zimbabwe",
        "slug": "zimbabwe",
        "airport": "Robert Gabriel Mugabe International Airport Harare (HRE) or Joshua Mqabuko Nkomo Airport Bulawayo (BUQ)",
        "emergency": "999 or 112",
        "death_cert": "death certificate (Registrar General's Department)",
        "registry": "Registrar General of Births and Deaths",
        "language": "English",
        "apostille": True,
        "apostille_year": "2014",
        "complexity": "moderate",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "7-14 days",
        "embassy_city": "Harare",
        "embassy_note": "The British Embassy in Harare can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (999 or 112). Death must be registered with the Registrar General's Department, usually within 30 days. The Zimbabwe Republic Police takes jurisdiction for violent, suspicious, or unexplained deaths. Death certificates are issued in English. Zimbabwe joined the Hague Apostille Convention in 2014, which simplifies document authentication.",
        "police_note": "The Zimbabwe Republic Police (ZRP) investigates violent or sudden deaths. Clearance is required before release.",
        "source": "FCDO Travel Advice Zimbabwe 2025; Zimbabwe Registrar General Department procedures; Hague Conference HCCH country profile Zimbabwe",
        "translation_note": "Death certificates are in English. Hague Apostille authentication applies for member countries (since 2014).",
    },
    "venezuela": {
        "name": "Venezuela",
        "slug": "venezuela",
        "airport": "Simon Bolivar International Airport Caracas (CCS/MAI)",
        "emergency": "171",
        "death_cert": "acta de defuncion (SAREN, Registro Civil)",
        "registry": "SAREN (Servicio Autonomo de Registros y Notarias)",
        "language": "Spanish",
        "apostille": True,
        "apostille_year": "2023",
        "complexity": "high",
        "timeline_avg": "4-8 weeks",
        "timeline_fast": "3-5 weeks",
        "timeline_complex": "8-16 weeks",
        "doc_processing": "14-30 days",
        "embassy_city": "Caracas",
        "embassy_note": "The British Embassy in Caracas can register the death and advise on local funeral directors. Consular capacity is limited due to political instability. FCDO advises against all but essential travel to Venezuela. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (171). Death must be registered with SAREN at the local Registro Civil. Political and economic instability in Venezuela can cause delays at every stage. All documentation is in Spanish and requires certified English translation. Venezuela joined the Hague Apostille Convention in 2023, which simplifies document authentication, but the acta de defuncion must be authenticated by SAREN and the Ministry of Foreign Affairs before it is valid abroad.",
        "police_note": "The CICPC (investigative police) takes jurisdiction for violent or suspicious deaths. Timelines can extend significantly in cases involving criminal investigation.",
        "source": "FCDO Travel Advice Venezuela 2025; SAREN Registro Civil regulations; Hague Conference HCCH Venezuela profile 2023",
        "translation_note": "All Venezuelan documents are in Spanish. Certified English translation is required for UK, Irish, and Commonwealth destinations.",
    },
    "ecuador": {
        "name": "Ecuador",
        "slug": "ecuador",
        "airport": "Mariscal Sucre International Airport Quito (UIO) or Jose Joaquin de Olmedo Airport Guayaquil (GYE)",
        "emergency": "911",
        "death_cert": "acta de defuncion (DINARDAP, Registro Civil)",
        "registry": "DINARDAP (Direccion Nacional de Registro de Datos Publicos)",
        "language": "Spanish",
        "apostille": True,
        "apostille_year": "2005",
        "complexity": "moderate",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "7-14 days",
        "embassy_city": "Quito",
        "embassy_note": "The British Embassy in Quito can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (911). Death must be registered with the DINARDAP/Registro Civil. The Fiscalia General del Estado takes jurisdiction for violent, suspicious, or unexplained deaths. All documentation is in Spanish and requires certified English translation. Ecuador has been a Hague Apostille Convention member since 2005.",
        "police_note": "The Fiscalia General del Estado investigates violent or suspicious deaths before authorising body release.",
        "source": "FCDO Travel Advice Ecuador 2025; DINARDAP Registro Civil procedures; Hague Conference HCCH Ecuador profile",
        "translation_note": "All Ecuadorian documents are in Spanish. Certified English translation is required for UK, Irish, and Commonwealth destinations.",
    },
    "romania": {
        "name": "Romania",
        "slug": "romania",
        "airport": "Henri Coanda International Airport Bucharest (OTP)",
        "emergency": "112",
        "death_cert": "certificat de deces (Starea Civila)",
        "registry": "Serviciul de Stare Civila (Civil Status Office)",
        "language": "Romanian",
        "apostille": True,
        "apostille_year": "member",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "3-6 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Bucharest",
        "embassy_note": "The British Embassy in Bucharest can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (112). Death must be registered with the local Serviciul de Stare Civila within 3 days. The Parchet (Prosecutor's Office) takes jurisdiction for violent or suspicious deaths. The certificat de deces is issued in Romanian and requires certified English translation for UK and Irish destinations. Romania is a Hague Apostille Convention member, which simplifies document authentication.",
        "police_note": "The Parchet (Prosecutor's Office) investigates violent or sudden deaths. Clearance is needed before the body can be released for repatriation.",
        "source": "FCDO Travel Advice Romania 2025; Romanian Ministry of Internal Affairs, Directia de Evidenta a Persoanelor; Hague Conference Romania profile",
        "translation_note": "Death certificates are in Romanian. Certified English translation is required for UK, Irish, and most Anglophone destinations.",
    },
    "poland": {
        "name": "Poland",
        "slug": "poland",
        "airport": "Warsaw Chopin Airport (WAW) or Krakow John Paul II Airport (KRK)",
        "emergency": "112, 997 (police), 999 (ambulance)",
        "death_cert": "akt zgonu (USC, Urzad Stanu Cywilnego)",
        "registry": "Urzad Stanu Cywilnego (Civil Registry Office)",
        "language": "Polish",
        "apostille": True,
        "apostille_year": "1992",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "3-5 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Warsaw",
        "embassy_note": "The British Embassy in Warsaw can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (112). Death must be registered with the local USC (Urzad Stanu Cywilnego) within 3 days. The Prokuratura (Prosecutor's Office) takes jurisdiction for violent or suspicious deaths. The akt zgonu is issued in Polish and requires certified English translation for UK and Irish destinations. Poland has been a Hague Apostille Convention member since 1992.",
        "police_note": "The Prokuratura investigates violent or suspicious deaths. This typically adds 5-10 working days before the body is released.",
        "source": "FCDO Travel Advice Poland 2025; Polish Ministry of Internal Affairs USC procedures; Hague Conference Poland profile",
        "translation_note": "Death certificates are in Polish. Certified English translation is required for UK, Irish, and Anglophone destinations.",
    },
    "lebanon": {
        "name": "Lebanon",
        "slug": "lebanon",
        "airport": "Beirut Rafic Hariri International Airport (BEY)",
        "emergency": "112 or 140",
        "death_cert": "death certificate (Ministry of Interior Civil Status Department)",
        "registry": "Civil Status Directorate, Ministry of Interior",
        "language": "Arabic",
        "apostille": False,
        "complexity": "high",
        "timeline_avg": "3-6 weeks",
        "timeline_fast": "2-4 weeks",
        "timeline_complex": "6-12 weeks",
        "doc_processing": "10-21 days",
        "embassy_city": "Beirut",
        "embassy_note": "The British Embassy in Beirut can register the death and advise on local funeral directors. FCDO advises against all travel to parts of Lebanon and against all but essential travel to others. Check current FCDO Travel Advice before arranging any travel. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (112 or 140). Death must be registered with the Civil Status Directorate. The Internal Security Forces (ISF) takes jurisdiction for violent, suspicious, or unexplained deaths. All documentation is in Arabic and requires certified English translation. Lebanon is not a Hague Apostille Convention member, so documents must be authenticated through the Lebanese Ministry of Foreign Affairs and the destination country's embassy. Active conflict in parts of the country can affect timelines significantly.",
        "police_note": "The Internal Security Forces (ISF) investigates violent or suspicious deaths. Political and security conditions can affect processing times.",
        "source": "FCDO Travel Advice Lebanon 2025; Lebanese Civil Status Directorate procedures; Ministry of Foreign Affairs and Emigrants Lebanon",
        "translation_note": "All Lebanese documents are in Arabic. Certified English translation is required for UK, Irish, and most Western destinations. Ministry of Foreign Affairs legalisation is also required.",
    },
    "tanzania": {
        "name": "Tanzania",
        "slug": "tanzania",
        "airport": "Julius Nyerere International Airport Dar es Salaam (DAR) or Kilimanjaro International Airport (JRO)",
        "emergency": "112 or 999",
        "death_cert": "death certificate (RITA, Registration Insolvency and Trusteeship Agency)",
        "registry": "RITA (Registration Insolvency and Trusteeship Agency)",
        "language": "English and Swahili",
        "apostille": True,
        "apostille_year": "2015",
        "complexity": "moderate",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "7-14 days",
        "embassy_city": "Dar es Salaam",
        "embassy_note": "The British High Commission in Dar es Salaam can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (112 or 999). Death must be registered with RITA (Registration Insolvency and Trusteeship Agency) within 6 months, though prompt registration is required for repatriation. The Tanzania Police Force takes jurisdiction for violent, suspicious, or unexplained deaths. Death certificates are issued in English or Swahili. Tanzania joined the Hague Apostille Convention in 2015.",
        "police_note": "The Tanzania Police Force investigates violent or suspicious deaths. Clearance from the police and medical examiner is required before body release.",
        "source": "FCDO Travel Advice Tanzania 2025; RITA registration procedures 2025; Hague Conference Tanzania profile",
        "translation_note": "Death certificates issued in Swahili may require certified English translation. English-language certificates are accepted without translation.",
    },
    "cameroon": {
        "name": "Cameroon",
        "slug": "cameroon",
        "airport": "Douala International Airport (DLA) or Nsimalen International Airport Yaounde (NSI)",
        "emergency": "117 or 118",
        "death_cert": "acte de deces (Etat Civil, commune level)",
        "registry": "Etat Civil (commune-level civil registration authority)",
        "language": "French and English (bilingual country)",
        "apostille": False,
        "complexity": "moderate",
        "timeline_avg": "3-5 weeks",
        "timeline_fast": "2-3 weeks",
        "timeline_complex": "5-10 weeks",
        "doc_processing": "10-21 days",
        "embassy_city": "Yaounde",
        "embassy_note": "The British High Commission in Yaounde can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (117 or 118). Death must be registered at the local Etat Civil (commune-level civil registry). The Parquet (Prosecutor's Office) takes jurisdiction for violent, suspicious, or unexplained deaths. Cameroon is officially bilingual (French and English), though French predominates in most official documentation. Cameroon is not a Hague Apostille Convention member, so documents must be legalised through the Cameroonian Ministry of Foreign Affairs and the destination country's embassy.",
        "police_note": "The Gendarmerie or Police Judiciaire investigates violent or sudden deaths. Clearance is required before body release.",
        "source": "FCDO Travel Advice Cameroon 2025; Cameroon Ministry of External Relations; FCDO Cameroon consular guidance 2025",
        "translation_note": "French-language documents require certified English translation for UK, Irish, and Anglophone destinations. Cameroonian notarial legalisation and Ministry of Foreign Affairs authentication are required.",
    },
}

# ---------------------------------------------------------------------------
# Destination data
# ---------------------------------------------------------------------------

DEST_META = {
    "united-states": {
        "name": "United States",
        "slug": "united-states",
        "display_name": "the United States",
        "airport": "JFK, LAX, ORD, MIA, or the nearest major gateway",
        "reception": "The US funeral director takes custody at the cargo terminal. CDC importation requirements apply. The state records office must be notified. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "US Embassy or Consulate in {origin_country}: contact details vary by country. US Dept of State emergency: 1-888-407-4747 (from US) or +1-202-501-4444.",
        "apostille": "Hague Apostille (1981)",
        "timeline": "2-4 weeks standard",
        "dest_key": "us",
    },
    "germany": {
        "name": "Germany",
        "slug": "germany",
        "display_name": "Germany",
        "airport": "Frankfurt (FRA), Munich (MUC), Berlin (BER), or other major German airport",
        "reception": "The German funeral director takes custody at the cargo terminal. Death is registered with the local Standesamt (Civil Status Office). The Sterbeurkunde (German death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "German Embassy in {origin_country}: contact the German Embassy in the country of death for support with documentation. Germany has consular representation in most countries.",
        "apostille": "Hague Apostille (1965)",
        "timeline": "2-4 weeks standard",
        "dest_key": "germany",
    },
    "france": {
        "name": "France",
        "slug": "france",
        "display_name": "France",
        "airport": "Paris Charles de Gaulle (CDG), Paris Orly (ORY), Lyon (LYS), or other major French airport",
        "reception": "The French funeral director takes custody at the cargo terminal. Death is registered with the local mairie (town hall). The acte de deces (French death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "French Embassy in {origin_country}: contact the French Embassy in the country of death for documentation support.",
        "apostille": "Hague Apostille (1960)",
        "timeline": "2-4 weeks standard",
        "dest_key": "france",
    },
    "australia": {
        "name": "Australia",
        "slug": "australia",
        "display_name": "Australia",
        "airport": "Sydney (SYD), Melbourne (MEL), Brisbane (BNE), Perth (PER), or other major Australian airport",
        "reception": "The Australian funeral director takes custody at the cargo terminal. Australian Border Force (ABF) clearance is required on arrival. Death is registered with the relevant state BDM (Births, Deaths and Marriages). Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Australian High Commission or Embassy in {origin_country}: contact DFAT on +61 2 6261 3305 or the Consular Emergency Centre on 1300 555 135 (from Australia).",
        "apostille": "Hague Apostille (1995)",
        "timeline": "2-4 weeks standard",
        "dest_key": "australia",
    },
    "netherlands": {
        "name": "Netherlands",
        "slug": "netherlands",
        "display_name": "the Netherlands",
        "airport": "Amsterdam Schiphol (AMS), Rotterdam The Hague (RTM), or Eindhoven (EIN)",
        "reception": "The Dutch funeral director takes custody at the cargo terminal. Death is registered with the local gemeente (municipality) in the BRP (Municipal Personal Records Database). The akte van overlijden (Dutch death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Netherlands Embassy in {origin_country}: contact the Dutch Embassy in the country of death for support with documentation.",
        "apostille": "Hague Apostille (1960, founding member)",
        "timeline": "2-4 weeks standard",
        "dest_key": "netherlands",
    },
    "canada": {
        "name": "Canada",
        "slug": "canada",
        "display_name": "Canada",
        "airport": "Toronto Pearson (YYZ), Vancouver (YVR), Montreal (YUL), or other major Canadian airport",
        "reception": "The Canadian funeral director takes custody at the cargo terminal. Death is registered with the provincial civil registration authority (BDM in the relevant province). Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Canadian High Commission or Embassy in {origin_country}: contact Global Affairs Canada Emergency Watch: +1-613-996-8885 (collect calls accepted).",
        "apostille": "Hague Apostille (in force November 2024)",
        "timeline": "2-4 weeks standard",
        "dest_key": "canada",
    },
    "sweden": {
        "name": "Sweden",
        "slug": "sweden",
        "display_name": "Sweden",
        "airport": "Stockholm Arlanda (ARN), Gothenburg Landvetter (GOT), or other major Swedish airport",
        "reception": "The Swedish funeral director takes custody at the cargo terminal. Death is registered with Skatteverket (the Swedish Tax Agency population register). The dodsfallsintyg (Swedish death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Swedish Embassy in {origin_country}: contact the Swedish Embassy in the country of death for documentation support.",
        "apostille": "Hague Apostille (1999)",
        "timeline": "2-3 weeks standard",
        "dest_key": "sweden",
    },
    "norway": {
        "name": "Norway",
        "slug": "norway",
        "display_name": "Norway",
        "airport": "Oslo Gardermoen (OSL), Bergen (BGO), or Stavanger (SVG)",
        "reception": "The Norwegian funeral director takes custody at the cargo terminal. Death is registered with Folkeregisteret (Norwegian Population Register) via Skatteetaten. The dodsattest (Norwegian death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Norwegian Embassy in {origin_country}: contact the Norwegian Embassy in the country of death for documentation support.",
        "apostille": "Hague Apostille (1980)",
        "timeline": "2-3 weeks standard",
        "dest_key": "norway",
    },
    "spain": {
        "name": "Spain",
        "slug": "spain",
        "display_name": "Spain",
        "airport": "Madrid Barajas (MAD), Barcelona El Prat (BCN), or other major Spanish airport",
        "reception": "The Spanish funeral director takes custody at the cargo terminal. Death is registered with the Registro Civil (Civil Registry, Ministerio de Justicia). The certificado de defuncion (Spanish death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Spanish Embassy in {origin_country}: contact the Spanish Embassy in the country of death for documentation support.",
        "apostille": "Hague Apostille (1978)",
        "timeline": "2-4 weeks standard",
        "dest_key": "spain",
    },
    "italy": {
        "name": "Italy",
        "slug": "italy",
        "display_name": "Italy",
        "airport": "Rome Fiumicino (FCO), Milan Malpensa (MXP), Naples (NAP), or other major Italian airport",
        "reception": "The Italian funeral director takes custody at the cargo terminal. Death is registered with the local Comune (ufficio di stato civile). The atto di morte (Italian death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Italian Embassy in {origin_country}: contact the Italian Embassy in the country of death for documentation support.",
        "apostille": "Hague Apostille (1978)",
        "timeline": "2-4 weeks standard",
        "dest_key": "italy",
    },
    "austria": {
        "name": "Austria",
        "slug": "austria",
        "display_name": "Austria",
        "airport": "Vienna International Airport (VIE)",
        "reception": "The Austrian funeral director takes custody at the cargo terminal. Death is registered with the local Standesamt (Civil Status Office). The Sterbeurkunde (Austrian death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Austrian Embassy in {origin_country}: contact the Austrian Embassy in the country of death for documentation support.",
        "apostille": "Hague Apostille (1968)",
        "timeline": "2-4 weeks standard",
        "dest_key": "austria",
    },
    "portugal": {
        "name": "Portugal",
        "slug": "portugal",
        "display_name": "Portugal",
        "airport": "Lisbon Humberto Delgado (LIS), Porto Francisco Sa Carneiro (OPO), or Faro (FAO)",
        "reception": "The Portuguese funeral director takes custody at the cargo terminal. Death is registered with the Conservatoria do Registo Civil (Civil Registry, IRN). The certidao de obito (Portuguese death certificate) is issued. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Portuguese Embassy in {origin_country}: contact the Portuguese Embassy in the country of death for documentation support.",
        "apostille": "Hague Apostille (1968)",
        "timeline": "2-3 weeks standard",
        "dest_key": "portugal",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R89: starts at template C (index 2). 25 routes.
R89_ROUTES = [
    # Uganda x5: filling the R65 gap + new destinations
    ("uganda", "united-states"),
    ("uganda", "germany"),
    ("uganda", "australia"),
    ("uganda", "netherlands"),
    ("uganda", "france"),
    # Cuba x5: filling R65 gaps + new destinations
    ("cuba", "canada"),
    ("cuba", "germany"),
    ("cuba", "france"),
    ("cuba", "australia"),
    ("cuba", "netherlands"),
    # Zimbabwe x5: filling R65 gaps + new destinations
    ("zimbabwe", "united-states"),
    ("zimbabwe", "germany"),
    ("zimbabwe", "france"),
    ("zimbabwe", "canada"),
    ("zimbabwe", "netherlands"),
    # Venezuela x5: filling R65 gaps + new destinations
    ("venezuela", "germany"),
    ("venezuela", "italy"),
    ("venezuela", "france"),
    ("venezuela", "australia"),
    ("venezuela", "canada"),
    # Ecuador x5: filling R64 gap + new destinations
    ("ecuador", "germany"),
    ("ecuador", "france"),
    ("ecuador", "australia"),
    ("ecuador", "netherlands"),
    ("ecuador", "portugal"),
]

# R90: starts at template C (index 2). 25 routes.
R90_ROUTES = [
    # Romania x5: wave 2 destinations
    ("romania", "australia"),
    ("romania", "netherlands"),
    ("romania", "sweden"),
    ("romania", "norway"),
    ("romania", "united-states"),
    # Poland x5: wave 2 destinations
    ("poland", "australia"),
    ("poland", "canada"),
    ("poland", "spain"),
    ("poland", "italy"),
    ("poland", "austria"),
    # Lebanon x5: wave 2 destinations
    ("lebanon", "australia"),
    ("lebanon", "italy"),
    ("lebanon", "spain"),
    ("lebanon", "netherlands"),
    ("lebanon", "sweden"),
    # Tanzania x5: wave 2 destinations
    ("tanzania", "france"),
    ("tanzania", "australia"),
    ("tanzania", "canada"),
    ("tanzania", "italy"),
    ("tanzania", "sweden"),
    # Cameroon x5: wave 2 destinations
    ("cameroon", "australia"),
    ("cameroon", "united-states"),
    ("cameroon", "canada"),
    ("cameroon", "sweden"),
    ("cameroon", "netherlands"),
]

# ---------------------------------------------------------------------------
# Sideways link helpers
# ---------------------------------------------------------------------------

# Pre-verified existing routes for sideways references
# Format: (origin_slug, dest_slug) -> (sideways1_path, sideways1_text, sideways2_path, sideways2_text)
SIDEWAYS = {
    # Uganda routes
    ("uganda", "united-states"): (
        "/routes/uganda-to-united-kingdom/", "Repatriation from Uganda to the UK",
        "/routes/kenya-to-united-states/", "Repatriation from Kenya to the United States",
    ),
    ("uganda", "germany"): (
        "/routes/uganda-to-united-kingdom/", "Repatriation from Uganda to the UK",
        "/routes/kenya-to-germany/", "Repatriation from Kenya to Germany",
    ),
    ("uganda", "australia"): (
        "/routes/uganda-to-united-kingdom/", "Repatriation from Uganda to the UK",
        "/routes/kenya-to-australia/", "Repatriation from Kenya to Australia",
    ),
    ("uganda", "netherlands"): (
        "/routes/uganda-to-united-kingdom/", "Repatriation from Uganda to the UK",
        "/routes/kenya-to-netherlands/", "Repatriation from Kenya to the Netherlands",
    ),
    ("uganda", "france"): (
        "/routes/uganda-to-united-kingdom/", "Repatriation from Uganda to the UK",
        "/routes/kenya-to-france/", "Repatriation from Kenya to France",
    ),
    # Cuba routes
    ("cuba", "canada"): (
        "/routes/cuba-to-united-kingdom/", "Repatriation from Cuba to the UK",
        "/routes/jamaica-to-canada/", "Repatriation from Jamaica to Canada",
    ),
    ("cuba", "germany"): (
        "/routes/cuba-to-united-kingdom/", "Repatriation from Cuba to the UK",
        "/routes/jamaica-to-germany/", "Repatriation from Jamaica to Germany",
    ),
    ("cuba", "france"): (
        "/routes/cuba-to-united-kingdom/", "Repatriation from Cuba to the UK",
        "/routes/jamaica-to-france/", "Repatriation from Jamaica to France",
    ),
    ("cuba", "australia"): (
        "/routes/cuba-to-united-kingdom/", "Repatriation from Cuba to the UK",
        "/routes/jamaica-to-australia/", "Repatriation from Jamaica to Australia",
    ),
    ("cuba", "netherlands"): (
        "/routes/cuba-to-united-kingdom/", "Repatriation from Cuba to the UK",
        "/routes/barbados-to-netherlands/", "Repatriation from Barbados to the Netherlands",
    ),
    # Zimbabwe routes
    ("zimbabwe", "united-states"): (
        "/routes/zimbabwe-to-united-kingdom/", "Repatriation from Zimbabwe to the UK",
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
    ),
    ("zimbabwe", "germany"): (
        "/routes/zimbabwe-to-united-kingdom/", "Repatriation from Zimbabwe to the UK",
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
    ),
    ("zimbabwe", "france"): (
        "/routes/zimbabwe-to-united-kingdom/", "Repatriation from Zimbabwe to the UK",
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
    ),
    ("zimbabwe", "canada"): (
        "/routes/zimbabwe-to-united-kingdom/", "Repatriation from Zimbabwe to the UK",
        "/routes/zimbabwe-to-australia/", "Repatriation from Zimbabwe to Australia",
    ),
    ("zimbabwe", "netherlands"): (
        "/routes/zimbabwe-to-united-kingdom/", "Repatriation from Zimbabwe to the UK",
        "/routes/zimbabwe-to-australia/", "Repatriation from Zimbabwe to Australia",
    ),
    # Venezuela routes
    ("venezuela", "germany"): (
        "/routes/venezuela-to-united-kingdom/", "Repatriation from Venezuela to the UK",
        "/routes/colombia-to-germany/", "Repatriation from Colombia to Germany",
    ),
    ("venezuela", "italy"): (
        "/routes/venezuela-to-united-kingdom/", "Repatriation from Venezuela to the UK",
        "/routes/colombia-to-italy/", "Repatriation from Colombia to Italy",
    ),
    ("venezuela", "france"): (
        "/routes/venezuela-to-united-kingdom/", "Repatriation from Venezuela to the UK",
        "/routes/colombia-to-france/", "Repatriation from Colombia to France",
    ),
    ("venezuela", "australia"): (
        "/routes/venezuela-to-united-kingdom/", "Repatriation from Venezuela to the UK",
        "/routes/colombia-to-australia/", "Repatriation from Colombia to Australia",
    ),
    ("venezuela", "canada"): (
        "/routes/venezuela-to-united-kingdom/", "Repatriation from Venezuela to the UK",
        "/routes/colombia-to-canada/", "Repatriation from Colombia to Canada",
    ),
    # Ecuador routes
    ("ecuador", "germany"): (
        "/routes/ecuador-to-united-kingdom/", "Repatriation from Ecuador to the UK",
        "/routes/peru-to-germany/", "Repatriation from Peru to Germany",
    ),
    ("ecuador", "france"): (
        "/routes/ecuador-to-united-kingdom/", "Repatriation from Ecuador to the UK",
        "/routes/peru-to-france/", "Repatriation from Peru to France",
    ),
    ("ecuador", "australia"): (
        "/routes/ecuador-to-united-kingdom/", "Repatriation from Ecuador to the UK",
        "/routes/peru-to-australia/", "Repatriation from Peru to Australia",
    ),
    ("ecuador", "netherlands"): (
        "/routes/ecuador-to-united-kingdom/", "Repatriation from Ecuador to the UK",
        "/routes/peru-to-netherlands/", "Repatriation from Peru to the Netherlands",
    ),
    ("ecuador", "portugal"): (
        "/routes/ecuador-to-united-kingdom/", "Repatriation from Ecuador to the UK",
        "/routes/ecuador-to-spain/", "Repatriation from Ecuador to Spain",
    ),
    # Romania routes
    ("romania", "australia"): (
        "/routes/romania-to-united-kingdom/", "Repatriation from Romania to the UK",
        "/routes/romania-to-germany/", "Repatriation from Romania to Germany",
    ),
    ("romania", "netherlands"): (
        "/routes/romania-to-united-kingdom/", "Repatriation from Romania to the UK",
        "/routes/romania-to-germany/", "Repatriation from Romania to Germany",
    ),
    ("romania", "sweden"): (
        "/routes/romania-to-united-kingdom/", "Repatriation from Romania to the UK",
        "/routes/romania-to-germany/", "Repatriation from Romania to Germany",
    ),
    ("romania", "norway"): (
        "/routes/romania-to-united-kingdom/", "Repatriation from Romania to the UK",
        "/routes/romania-to-germany/", "Repatriation from Romania to Germany",
    ),
    ("romania", "united-states"): (
        "/routes/romania-to-united-kingdom/", "Repatriation from Romania to the UK",
        "/routes/romania-to-germany/", "Repatriation from Romania to Germany",
    ),
    # Poland routes
    ("poland", "australia"): (
        "/routes/poland-to-united-kingdom/", "Repatriation from Poland to the UK",
        "/routes/poland-to-germany/", "Repatriation from Poland to Germany",
    ),
    ("poland", "canada"): (
        "/routes/poland-to-united-kingdom/", "Repatriation from Poland to the UK",
        "/routes/poland-to-germany/", "Repatriation from Poland to Germany",
    ),
    ("poland", "spain"): (
        "/routes/poland-to-united-kingdom/", "Repatriation from Poland to the UK",
        "/routes/poland-to-germany/", "Repatriation from Poland to Germany",
    ),
    ("poland", "italy"): (
        "/routes/poland-to-united-kingdom/", "Repatriation from Poland to the UK",
        "/routes/poland-to-germany/", "Repatriation from Poland to Germany",
    ),
    ("poland", "austria"): (
        "/routes/poland-to-united-kingdom/", "Repatriation from Poland to the UK",
        "/routes/poland-to-germany/", "Repatriation from Poland to Germany",
    ),
    # Lebanon routes
    ("lebanon", "australia"): (
        "/routes/lebanon-to-united-kingdom/", "Repatriation from Lebanon to the UK",
        "/routes/lebanon-to-germany/", "Repatriation from Lebanon to Germany",
    ),
    ("lebanon", "italy"): (
        "/routes/lebanon-to-united-kingdom/", "Repatriation from Lebanon to the UK",
        "/routes/lebanon-to-france/", "Repatriation from Lebanon to France",
    ),
    ("lebanon", "spain"): (
        "/routes/lebanon-to-united-kingdom/", "Repatriation from Lebanon to the UK",
        "/routes/lebanon-to-france/", "Repatriation from Lebanon to France",
    ),
    ("lebanon", "netherlands"): (
        "/routes/lebanon-to-united-kingdom/", "Repatriation from Lebanon to the UK",
        "/routes/lebanon-to-germany/", "Repatriation from Lebanon to Germany",
    ),
    ("lebanon", "sweden"): (
        "/routes/lebanon-to-united-kingdom/", "Repatriation from Lebanon to the UK",
        "/routes/lebanon-to-germany/", "Repatriation from Lebanon to Germany",
    ),
    # Tanzania routes
    ("tanzania", "france"): (
        "/routes/tanzania-to-united-kingdom/", "Repatriation from Tanzania to the UK",
        "/routes/kenya-to-france/", "Repatriation from Kenya to France",
    ),
    ("tanzania", "australia"): (
        "/routes/tanzania-to-united-kingdom/", "Repatriation from Tanzania to the UK",
        "/routes/kenya-to-australia/", "Repatriation from Kenya to Australia",
    ),
    ("tanzania", "canada"): (
        "/routes/tanzania-to-united-kingdom/", "Repatriation from Tanzania to the UK",
        "/routes/kenya-to-canada/", "Repatriation from Kenya to Canada",
    ),
    ("tanzania", "italy"): (
        "/routes/tanzania-to-united-kingdom/", "Repatriation from Tanzania to the UK",
        "/routes/kenya-to-italy/", "Repatriation from Kenya to Italy",
    ),
    ("tanzania", "sweden"): (
        "/routes/tanzania-to-united-kingdom/", "Repatriation from Tanzania to the UK",
        "/routes/kenya-to-sweden/", "Repatriation from Kenya to Sweden",
    ),
    # Cameroon routes
    ("cameroon", "australia"): (
        "/routes/cameroon-to-united-kingdom/", "Repatriation from Cameroon to the UK",
        "/routes/nigeria-to-australia/", "Repatriation from Nigeria to Australia",
    ),
    ("cameroon", "united-states"): (
        "/routes/cameroon-to-united-kingdom/", "Repatriation from Cameroon to the UK",
        "/routes/nigeria-to-united-states/", "Repatriation from Nigeria to the United States",
    ),
    ("cameroon", "canada"): (
        "/routes/cameroon-to-united-kingdom/", "Repatriation from Cameroon to the UK",
        "/routes/nigeria-to-canada/", "Repatriation from Nigeria to Canada",
    ),
    ("cameroon", "sweden"): (
        "/routes/cameroon-to-united-kingdom/", "Repatriation from Cameroon to the UK",
        "/routes/nigeria-to-sweden/", "Repatriation from Nigeria to Sweden",
    ),
    ("cameroon", "netherlands"): (
        "/routes/cameroon-to-united-kingdom/", "Repatriation from Cameroon to the UK",
        "/routes/nigeria-to-netherlands/", "Repatriation from Nigeria to the Netherlands",
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
        # Try shorter version
        title = f"{origin} to {dest} Repatriation Guide"
    return title


def make_description(origin_data, dest_data):
    """Generate an SEO description under 155 characters with CTA."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    timeline = origin_data["timeline_avg"]
    # Build description
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

    if dest_key == "us":
        consular = "Notify US Embassy or Consulate. US Dept of State emergency: 1-888-407-4747."
        reception_step = f"US funeral director takes custody at cargo terminal. CDC importation checks apply."
    elif dest_key == "germany":
        consular = "Notify the German Embassy in {origin}.".format(origin=origin)
        reception_step = "German funeral director takes custody at cargo terminal. Standesamt notified."
    elif dest_key == "france":
        consular = "Notify the French Embassy in {origin}.".format(origin=origin)
        reception_step = "French funeral director takes custody at cargo terminal. Mairie notified."
    elif dest_key == "australia":
        consular = "Notify Australian High Commission or Embassy. DFAT emergency: +61 2 6261 3305."
        reception_step = "Australian funeral director takes custody. ABF clearance completed. State BDM notified."
    elif dest_key == "netherlands":
        consular = "Notify the Netherlands Embassy in {origin}.".format(origin=origin)
        reception_step = "Dutch funeral director takes custody at cargo terminal. Gemeente BRP notified."
    elif dest_key == "canada":
        consular = "Notify Canadian High Commission or Embassy. Global Affairs Canada emergency: +1-613-996-8885."
        reception_step = "Canadian funeral director takes custody at cargo terminal. Provincial BDM notified."
    elif dest_key == "sweden":
        consular = "Notify the Swedish Embassy in {origin}.".format(origin=origin)
        reception_step = "Swedish funeral director takes custody at cargo terminal. Skatteverket notified."
    elif dest_key == "norway":
        consular = "Notify the Norwegian Embassy in {origin}.".format(origin=origin)
        reception_step = "Norwegian funeral director takes custody at cargo terminal. Folkeregisteret notified."
    elif dest_key == "spain":
        consular = "Notify the Spanish Embassy in {origin}.".format(origin=origin)
        reception_step = "Spanish funeral director takes custody at cargo terminal. Registro Civil notified."
    elif dest_key == "italy":
        consular = "Notify the Italian Embassy in {origin}.".format(origin=origin)
        reception_step = "Italian funeral director takes custody at cargo terminal. Comune notified."
    elif dest_key == "austria":
        consular = "Notify the Austrian Embassy in {origin}.".format(origin=origin)
        reception_step = "Austrian funeral director takes custody at cargo terminal. Standesamt notified."
    elif dest_key == "portugal":
        consular = "Notify the Portuguese Embassy in {origin}.".format(origin=origin)
        reception_step = "Portuguese funeral director takes custody at cargo terminal. Conservatoria do Registo Civil notified."
    else:
        consular = f"Notify the {dest} Embassy in {origin}."
        reception_step = f"{dest} funeral director takes custody at cargo terminal."

    # FCDO or DFA line
    if "ireland" in dest_data["slug"]:
        emergency_line = "Department of Foreign Affairs 24-hour line: +353 1 408 2000."
    else:
        emergency_line = "FCDO 24-hour emergency line: +44 (0)20 7008 5000."

    steps = [
        {
            "step": 1,
            "action": "Immediate steps after death. Report to local emergency services and contact a specialist.",
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
            "answer": (
                f"The {origin_data['embassy_city']}-based British embassy or high commission can register the death with UK authorities, "
                f"provide a list of local funeral directors, and advise on documentation. "
                f"They cannot pay for or arrange repatriation. "
                f"FCDO 24-hour emergency line: +44 (0)20 7008 5000."
            ),
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
        f"/routes/kenya-to-{dest_key}/", f"Repatriation from Kenya to {d['name']}",
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
    lines.append(f'  - "All {o["language"]}-language documentation requires certified English translation where needed."')
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
    # Combine R89 and R90 with their start variant indices
    all_batches = [
        ("R89", R89_ROUTES, 2),   # Start at C (index 2)
        ("R90", R90_ROUTES, 2),   # Start at C (index 2)
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
