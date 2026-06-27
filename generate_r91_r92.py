#!/usr/bin/env python3
"""
generate_r91_r92.py -- Repatriate Service Route Generator
Chunks R91 and R92: 50 Tier C route pages
R91: Iraq x5, Zambia x5, Rwanda x5, Somalia x5, Sudan x5
R92: Jamaica x5, Barbados x5, Cyprus x5, Hong Kong x5, Myanmar x5
Template variants: R91 and R92 both start at C (index 2)
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
    "iraq": {
        "name": "Iraq",
        "slug": "iraq",
        "airport": "Baghdad International Airport (BGW); Erbil International Airport (EBL) in the Kurdistan Region",
        "emergency": "104 (emergency operator), 115 (police), 122 (ambulance)",
        "death_cert": "shahada wafah (death certificate from the Civil Status Directorate)",
        "registry": "Civil Status Directorate (Mudiriyyat al-Ahwal al-Madaniyya)",
        "language": "Arabic",
        "apostille": False,
        "complexity": "very-high",
        "timeline_avg": "6-12 weeks",
        "timeline_fast": "4-6 weeks",
        "timeline_complex": "12-24 weeks",
        "doc_processing": "3-8 weeks",
        "embassy_city": "Baghdad",
        "embassy_note": "The British Embassy in Baghdad can register the death and provide a list of approved local funeral directors. The British Consulate-General in Erbil covers the Kurdistan Region. FCDO advises against all travel to Iraq. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (104). Death must be registered with the Civil Status Directorate. The Iraqi security services take jurisdiction for violent, suspicious, or unexplained deaths, which can cause significant delays. All documentation is in Arabic and requires certified English translation. Iraq is not a Hague Apostille Convention member; documents must be authenticated through the Iraqi Ministry of Foreign Affairs and the destination country's embassy. FCDO advises against all travel to Iraq; consular capacity is limited in many areas.",
        "police_note": "The Iraqi security services investigate violent or suspicious deaths. Political and security conditions can extend timelines considerably.",
        "source": "FCDO Travel Advice Iraq 2025; Iraqi Civil Status Directorate procedures; British Embassy Baghdad consular guidance 2025",
        "translation_note": "All Iraqi documents are in Arabic. Certified English translation is required for all Western destinations. Ministry of Foreign Affairs authentication is required as Iraq is not a Hague Apostille member.",
        "consular_faq": "The British Embassy in Baghdad handles consular matters for most of Iraq, and the British Consulate-General in Erbil covers the Kurdistan Region. FCDO advises against all travel to Iraq; consular capacity is limited. The Embassy can register the death and advise on approved local funeral directors, but cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
    },
    "zambia": {
        "name": "Zambia",
        "slug": "zambia",
        "airport": "Kenneth Kaunda International Airport Lusaka (LUN) or Simon Mwansa Kapwepwe Airport Ndola (NLA)",
        "emergency": "999 or 112",
        "death_cert": "death certificate (Registrar of Births Marriages and Deaths)",
        "registry": "Registrar of Births Marriages and Deaths, Ministry of Home Affairs",
        "language": "English",
        "apostille": False,
        "complexity": "moderate",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "7-14 days",
        "embassy_city": "Lusaka",
        "embassy_note": "The British High Commission in Lusaka can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (999 or 112). Death must be registered with the Registrar of Births Marriages and Deaths within 30 days. The Zambia Police Service takes jurisdiction for violent, suspicious, or unexplained deaths. Death certificates are issued in English. Zambia is not a Hague Apostille Convention member; documents must be authenticated through the Ministry of Foreign Affairs.",
        "police_note": "The Zambia Police Service investigates violent or sudden deaths. Clearance is required before the body is released for repatriation.",
        "source": "FCDO Travel Advice Zambia 2025; Zambia Registrar of Births Marriages and Deaths procedures 2025",
        "translation_note": "Death certificates are issued in English. No translation is required for English-speaking destination countries.",
    },
    "rwanda": {
        "name": "Rwanda",
        "slug": "rwanda",
        "airport": "Kigali International Airport (KGL)",
        "emergency": "112",
        "death_cert": "death certificate (National Identification Agency/NIDA, sector-level civil registration)",
        "registry": "National Identification Agency (NIDA), sector-level civil registrars",
        "language": "English, French, and Kinyarwanda",
        "apostille": True,
        "apostille_year": "2019",
        "complexity": "moderate",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "7-14 days",
        "embassy_city": "Kigali",
        "embassy_note": "The British High Commission in Kigali can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (112). Death must be registered with the local sector civil registrar through the National Identification Agency (NIDA) system. The Rwanda Investigation Bureau (RIB) takes jurisdiction for violent, suspicious, or unexplained deaths. Death certificates are issued in English, French, or Kinyarwanda. Rwanda joined the Hague Apostille Convention in 2019, which simplifies document authentication.",
        "police_note": "The Rwanda Investigation Bureau (RIB) investigates violent or suspicious deaths. Clearance is required before the body is released for repatriation.",
        "source": "FCDO Travel Advice Rwanda 2025; NIDA civil registration procedures 2025; Hague Conference Rwanda profile 2019",
        "translation_note": "Death certificates in Kinyarwanda require certified English or French translation. English and French certificates are accepted without translation at most Western destinations.",
    },
    "somalia": {
        "name": "Somalia",
        "slug": "somalia",
        "airport": "Aden Adde International Airport Mogadishu (MGQ) or Hargeisa Airport (HGA) for Somaliland",
        "emergency": "Emergency services are very limited in Somalia. Contact international assistance lines at once.",
        "death_cert": "death certificate from local authority where available; civil registration infrastructure is severely limited in many areas",
        "registry": "Federal Government civil registration (very limited capacity); Somaliland Civil Registration Authority for the Somaliland region",
        "language": "Somali and Arabic",
        "apostille": False,
        "complexity": "very-high",
        "timeline_avg": "8-16 weeks",
        "timeline_fast": "6-8 weeks",
        "timeline_complex": "16+ weeks",
        "doc_processing": "4-10 weeks",
        "embassy_city": "Nairobi",
        "embassy_note": "There is no resident British diplomatic mission in Mogadishu. The British High Commission in Nairobi handles consular matters for Somalia. FCDO advises against all travel to southern and central Somalia and all but essential travel to Somaliland. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Somalia has very limited civil registration infrastructure in many regions. Local authority, tribal leadership, or Islamic courts may be involved in certifying the death depending on location. Contact the British High Commission in Nairobi at once; they can advise on documentation and specialist repatriation companies that operate in Somalia. FCDO advises against all travel to much of the country. A specialist repatriation company with Somalia experience is not optional in most cases.",
        "police_note": "Formal police investigation capacity is very limited in most of Somalia. Timelines for body release vary based on location and local conditions.",
        "source": "FCDO Travel Advice Somalia 2025; British High Commission Nairobi consular guidance for Somalia 2025",
        "translation_note": "All Somali and Arabic documents require certified English translation. Notarial authentication through the Federal Government Ministry of Foreign Affairs may be required.",
        "consular_faq": "There is no resident British diplomatic mission in Mogadishu. The British High Commission in Nairobi handles consular matters for Somalia. FCDO advises against all travel to southern and central Somalia. The Nairobi High Commission can register the death and advise on specialist companies able to operate locally, but cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
    },
    "sudan": {
        "name": "Sudan",
        "slug": "sudan",
        "airport": "Khartoum Civil Aviation Authority Airport (KRT, severely damaged since April 2023); Port Sudan Airport (PZU) is the primary operational gateway",
        "emergency": "999",
        "death_cert": "civil registration certificate (Civil Registration General Directorate, CRGD)",
        "registry": "Civil Registration General Directorate (CRGD), Ministry of Interior",
        "language": "Arabic",
        "apostille": False,
        "complexity": "very-high",
        "timeline_avg": "8-16 weeks",
        "timeline_fast": "6-10 weeks",
        "timeline_complex": "16+ weeks",
        "doc_processing": "4-10 weeks",
        "embassy_city": "London",
        "embassy_note": "The British Embassy in Khartoum suspended operations in May 2023 due to the conflict. Consular assistance for Sudan is handled by FCDO directly from London. FCDO advises against all travel to Sudan. Contact FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "The British Embassy in Khartoum suspended operations in May 2023. All consular matters are handled by FCDO in London. Contact the FCDO 24-hour emergency line at once. Khartoum airport is largely non-operational; the primary departure point is Port Sudan (PZU). Civil registration is through the Civil Registration General Directorate, but capacity is severely disrupted by the conflict. All documents are in Arabic and require certified English translation. A specialist repatriation company with Sudan experience is essential.",
        "police_note": "Formal security and police capacity is severely limited due to the ongoing conflict. Body release may depend on the authorities controlling the area.",
        "source": "FCDO Travel Advice Sudan 2025; FCDO Sudan crisis guidance 2025; Sudan Civil Registration General Directorate procedures (pre-conflict reference)",
        "translation_note": "All Sudanese documents are in Arabic. Certified English translation is required for all Western destinations.",
        "consular_faq": "The British Embassy in Khartoum suspended operations in May 2023. FCDO in London now handles all consular matters for Sudan. They can advise on documentation requirements and specialist companies able to operate in the country, but cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
    },
    "jamaica": {
        "name": "Jamaica",
        "slug": "jamaica",
        "airport": "Norman Manley International Airport Kingston (KIN) or Sangster International Airport Montego Bay (MBJ)",
        "emergency": "119 (police) or 110 (ambulance)",
        "death_cert": "death certificate (Registrar General's Department, RGD)",
        "registry": "Registrar General's Department (RGD)",
        "language": "English",
        "apostille": True,
        "apostille_year": "1964",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "3-6 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Kingston",
        "embassy_note": "The British High Commission in Kingston can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (119 or 110). Death must be registered with the Registrar General's Department within 10 days of the medical certificate being issued. The Jamaica Constabulary Force takes jurisdiction for violent, suspicious, or unexplained deaths. Death certificates are issued in English. Jamaica has been a Hague Apostille Convention member since 1964, which simplifies document authentication.",
        "police_note": "The Jamaica Constabulary Force investigates violent or sudden deaths. Clearance is required before the body is released for repatriation.",
        "source": "FCDO Travel Advice Jamaica 2025; Registrar General's Department Jamaica procedures 2025; Hague Conference Jamaica profile",
        "translation_note": "Death certificates are issued in English. No translation is required for English-speaking destination countries.",
    },
    "barbados": {
        "name": "Barbados",
        "slug": "barbados",
        "airport": "Grantley Adams International Airport Bridgetown (BGI)",
        "emergency": "211 (police) or 511 (ambulance)",
        "death_cert": "death certificate (Barbados Registration Department)",
        "registry": "Barbados Registration Department",
        "language": "English",
        "apostille": True,
        "apostille_year": "2001",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "3-5 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Bridgetown",
        "embassy_note": "The British High Commission in Bridgetown can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (211 police / 511 ambulance). Death must be registered with the Barbados Registration Department promptly. The Royal Barbados Police Force takes jurisdiction for violent, suspicious, or unexplained deaths. Death certificates are issued in English. Barbados has been a Hague Apostille Convention member since 2001.",
        "police_note": "The Royal Barbados Police Force investigates violent or suspicious deaths. Clearance is required before the body is released for repatriation.",
        "source": "FCDO Travel Advice Barbados 2025; Barbados Registration Department procedures 2025; Hague Conference Barbados profile",
        "translation_note": "Death certificates are issued in English. No translation is required for English-speaking destination countries.",
    },
    "cyprus": {
        "name": "Cyprus",
        "slug": "cyprus",
        "airport": "Larnaca International Airport (LCA) or Paphos International Airport (PFO)",
        "emergency": "112",
        "death_cert": "death certificate (Civil Registry and Migration Department, CRMD)",
        "registry": "Civil Registry and Migration Department (CRMD), Ministry of Interior",
        "language": "Greek (English widely used; Cyprus is a former British colony)",
        "apostille": True,
        "apostille_year": "2003",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "3-6 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Nicosia",
        "embassy_note": "The British High Commission in Nicosia can register the death and advise on local funeral directors. FCDO advises caution for travel to the northern areas of Cyprus (held by Turkish Cypriot authorities since 1974). FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (112). Death must be registered with the Civil Registry and Migration Department (CRMD). The Cyprus Police takes jurisdiction for violent, suspicious, or unexplained deaths. Death certificates are issued in Greek; English-language translations are available from the CRMD. Cyprus joined the Hague Apostille Convention in 2003. Deaths in the northern area require separate guidance; contact the FCDO for current advice.",
        "police_note": "The Cyprus Police investigates violent or suspicious deaths. Clearance is required before the body is released for repatriation.",
        "source": "FCDO Travel Advice Cyprus 2025; Civil Registry and Migration Department CRMD procedures 2025; Hague Conference Cyprus profile",
        "translation_note": "Death certificates are in Greek. Certified English translation is required for most non-Cypriot destinations. Hague Apostille authentication applies for member countries (since 2003).",
    },
    "hong-kong": {
        "name": "Hong Kong",
        "slug": "hong-kong",
        "airport": "Hong Kong International Airport (HKG)",
        "emergency": "999",
        "death_cert": "death certificate (Births and Deaths Registry, Immigration Department of Hong Kong)",
        "registry": "Births and Deaths Registry, Immigration Department",
        "language": "English and Cantonese (both official languages)",
        "apostille": False,
        "complexity": "moderate",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "7-14 days",
        "embassy_city": "Hong Kong",
        "embassy_note": "The British Consulate-General in Hong Kong can register the death and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (999). Death must be reported to the Births and Deaths Registry within 24 hours of the medical certificate of cause of death being issued. The Hong Kong Police Force takes jurisdiction for violent, suspicious, or unexplained deaths; a coroner may be appointed. Death certificates are issued in English and Chinese. Hong Kong is not a Hague Apostille Convention member, as China has not ratified the convention; documents must be authenticated through the Chinese Ministry of Foreign Affairs Consular Legalisation process.",
        "police_note": "The Hong Kong Police Force investigates violent or suspicious deaths. A coroner may be involved, which can add several weeks to the process.",
        "source": "FCDO Travel Advice Hong Kong 2025; Births and Deaths Registry Hong Kong Immigration Department 2025",
        "translation_note": "Death certificates are issued in English and Chinese. English-language certificates are accepted without translation in most English-speaking destinations. Chinese-only documents require certified translation.",
    },
    "myanmar": {
        "name": "Myanmar",
        "slug": "myanmar",
        "airport": "Yangon International Airport (RGN) or Mandalay International Airport (MDL)",
        "emergency": "199 (police) or 192 (fire and ambulance)",
        "death_cert": "death certificate from the GAD (General Administration Department), township level",
        "registry": "General Administration Department (GAD), township level; operating under military administration since the February 2021 coup",
        "language": "Burmese",
        "apostille": False,
        "complexity": "high",
        "timeline_avg": "4-10 weeks",
        "timeline_fast": "3-5 weeks",
        "timeline_complex": "10-20 weeks",
        "doc_processing": "2-6 weeks",
        "embassy_city": "Yangon",
        "embassy_note": "The British Embassy in Yangon can register the death and advise on local funeral directors. FCDO advises against all travel to most of Myanmar, including border regions and multiple states. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Contact emergency services (199). Death must be registered with the General Administration Department at township level. Since the February 2021 military coup, civil administration capacity has been disrupted across much of Myanmar. The death certificate is issued in Burmese and requires certified English translation. Myanmar is not a Hague Apostille Convention member; documents must be authenticated through the Myanmar Ministry of Foreign Affairs. A specialist repatriation company with Myanmar experience is strongly advised.",
        "police_note": "Township-level authorities investigate violent or suspicious deaths. The security situation in many areas of Myanmar can significantly extend timelines.",
        "source": "FCDO Travel Advice Myanmar 2025; Myanmar General Administration Department procedures; FCDO Myanmar consular guidance 2025",
        "translation_note": "All Myanmar documents are in Burmese. Certified English translation is required for all Western destinations. Ministry of Foreign Affairs authentication is required as Myanmar is not a Hague Apostille member.",
    },
}

# ---------------------------------------------------------------------------
# Destination data
# ---------------------------------------------------------------------------

DEST_META = {
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
    "belgium": {
        "name": "Belgium",
        "slug": "belgium",
        "display_name": "Belgium",
        "airport": "Brussels Airport (BRU) or Brussels South Charleroi (CRL)",
        "reception": "The Belgian funeral director takes custody at the cargo terminal. Death is registered with the local commune/gemeenten (municipal authority). The acte de deces or overlijdensakte (Belgian death certificate) is issued in French, Dutch, or German depending on region. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Belgian Embassy in {origin_country}: contact the Belgian Ministry of Foreign Affairs at +32 2 501 8111 for consular guidance.",
        "apostille": "Hague Apostille (1975)",
        "timeline": "2-4 weeks standard",
        "dest_key": "belgium",
    },
    "jordan": {
        "name": "Jordan",
        "slug": "jordan",
        "display_name": "Jordan",
        "airport": "Queen Alia International Airport Amman (AMM) or King Hussein International Airport Aqaba (AQJ)",
        "reception": "The Jordanian funeral director takes custody at the cargo terminal. Death is registered with the National Civil Status and Passports Department (NCSPC). Islamic law procedures apply for Muslim remains. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Jordanian Embassy in {origin_country}: contact the Jordanian Ministry of Foreign Affairs at +962 6 567 8311 for consular guidance.",
        "apostille": "Jordan is not a Hague Apostille Convention member. Documents require authentication through the Jordanian Ministry of Foreign Affairs.",
        "timeline": "3-5 weeks standard",
        "dest_key": "jordan",
    },
    "malaysia": {
        "name": "Malaysia",
        "slug": "malaysia",
        "display_name": "Malaysia",
        "airport": "Kuala Lumpur International Airport (KUL), Kota Kinabalu (BKI), or Penang (PEN)",
        "reception": "The Malaysian funeral director takes custody at the cargo terminal. Death is registered with Jabatan Pendaftaran Negara (JPN, National Registration Department). Documents require Malaysian High Commission attestation and Wisma Putra (Ministry of Foreign Affairs) authentication before acceptance. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Malaysian High Commission in {origin_country}: contact Wisma Putra (Ministry of Foreign Affairs Malaysia) at +60 3 8000 8000 for consular guidance.",
        "apostille": "Malaysia is not a Hague Apostille Convention member. Documents require Malaysian High Commission attestation and Ministry of Foreign Affairs authentication.",
        "timeline": "3-5 weeks standard",
        "dest_key": "malaysia",
    },
    "switzerland": {
        "name": "Switzerland",
        "slug": "switzerland",
        "display_name": "Switzerland",
        "airport": "Zurich (ZRH), Geneva (GVA), or Basel EuroAirport (BSL)",
        "reception": "The Swiss funeral director takes custody at the cargo terminal. Death is registered with the local Zivilstandsamt (Civil Status Office). The Todesurkunde (Swiss death certificate) is issued in German, French, or Italian depending on canton. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Swiss Embassy in {origin_country}: contact the FDFA Helpline on +41 800 24-7-365 for consular guidance.",
        "apostille": "Hague Apostille (1972)",
        "timeline": "2-4 weeks standard",
        "dest_key": "switzerland",
    },
    "india": {
        "name": "India",
        "slug": "india",
        "display_name": "India",
        "airport": "Delhi Indira Gandhi International (DEL), Mumbai Chhatrapati Shivaji Maharaj International (BOM), Chennai (MAA), or other major Indian airport",
        "reception": "The Indian funeral director takes custody at the cargo terminal. Death is registered with the state civil registrar under the Registration of Births and Deaths Act 1969. Customs clearance is required on arrival. Straightforward cases proceed to funeral arrangements without delay.",
        "consular_note": "Indian High Commission or Embassy in {origin_country}: contact the Ministry of External Affairs India Consular Services at +91 11 2301 2113 for guidance.",
        "apostille": "Hague Apostille (2005)",
        "timeline": "2-4 weeks standard",
        "dest_key": "india",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R91: starts at template C (index 2). 25 routes.
R91_ROUTES = [
    # Iraq x5: high-diaspora destinations not yet built
    ("iraq", "spain"),
    ("iraq", "italy"),
    ("iraq", "belgium"),
    ("iraq", "jordan"),
    ("iraq", "malaysia"),
    # Zambia x5: Commonwealth and European destinations
    ("zambia", "australia"),
    ("zambia", "canada"),
    ("zambia", "germany"),
    ("zambia", "france"),
    ("zambia", "netherlands"),
    # Rwanda x5: Europe and Commonwealth destinations
    ("rwanda", "australia"),
    ("rwanda", "canada"),
    ("rwanda", "italy"),
    ("rwanda", "netherlands"),
    ("rwanda", "sweden"),
    # Somalia x5: Western Europe and Commonwealth destinations
    ("somalia", "france"),
    ("somalia", "australia"),
    ("somalia", "italy"),
    ("somalia", "spain"),
    ("somalia", "switzerland"),
    # Sudan x5: Western Europe and North America
    ("sudan", "canada"),
    ("sudan", "france"),
    ("sudan", "germany"),
    ("sudan", "italy"),
    ("sudan", "netherlands"),
]

# R92: starts at template C (index 2). 25 routes.
R92_ROUTES = [
    # Jamaica x5: Commonwealth and European destinations
    ("jamaica", "australia"),
    ("jamaica", "germany"),
    ("jamaica", "france"),
    ("jamaica", "italy"),
    ("jamaica", "netherlands"),
    # Barbados x5: North America and Europe
    ("barbados", "canada"),
    ("barbados", "france"),
    ("barbados", "germany"),
    ("barbados", "australia"),
    ("barbados", "netherlands"),
    # Cyprus x5: Western Europe and North America
    ("cyprus", "france"),
    ("cyprus", "italy"),
    ("cyprus", "australia"),
    ("cyprus", "netherlands"),
    ("cyprus", "canada"),
    # Hong Kong x5: Commonwealth and Europe
    ("hong-kong", "australia"),
    ("hong-kong", "canada"),
    ("hong-kong", "germany"),
    ("hong-kong", "france"),
    ("hong-kong", "india"),
    # Myanmar x5: Europe
    ("myanmar", "italy"),
    ("myanmar", "spain"),
    ("myanmar", "netherlands"),
    ("myanmar", "sweden"),
    ("myanmar", "norway"),
]

# ---------------------------------------------------------------------------
# Sideways link helpers
# ---------------------------------------------------------------------------

SIDEWAYS = {
    # Iraq routes -- sideways: same origin different dest + related origin same dest
    ("iraq", "spain"): (
        "/routes/iraq-to-united-kingdom/", "Repatriation from Iraq to the UK",
        "/routes/jordan-to-spain/", "Repatriation from Jordan to Spain",
    ),
    ("iraq", "italy"): (
        "/routes/iraq-to-united-kingdom/", "Repatriation from Iraq to the UK",
        "/routes/lebanon-to-italy/", "Repatriation from Lebanon to Italy",
    ),
    ("iraq", "belgium"): (
        "/routes/iraq-to-united-kingdom/", "Repatriation from Iraq to the UK",
        "/routes/morocco-to-belgium/", "Repatriation from Morocco to Belgium",
    ),
    ("iraq", "jordan"): (
        "/routes/iraq-to-united-kingdom/", "Repatriation from Iraq to the UK",
        "/routes/lebanon-to-jordan/", "Repatriation from Lebanon to Jordan",
    ),
    ("iraq", "malaysia"): (
        "/routes/iraq-to-united-kingdom/", "Repatriation from Iraq to the UK",
        "/routes/bangladesh-to-malaysia/", "Repatriation from Bangladesh to Malaysia",
    ),
    # Zambia routes
    ("zambia", "australia"): (
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
        "/routes/kenya-to-australia/", "Repatriation from Kenya to Australia",
    ),
    ("zambia", "canada"): (
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
        "/routes/kenya-to-canada/", "Repatriation from Kenya to Canada",
    ),
    ("zambia", "germany"): (
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
        "/routes/kenya-to-germany/", "Repatriation from Kenya to Germany",
    ),
    ("zambia", "france"): (
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
        "/routes/kenya-to-france/", "Repatriation from Kenya to France",
    ),
    ("zambia", "netherlands"): (
        "/routes/zambia-to-united-kingdom/", "Repatriation from Zambia to the UK",
        "/routes/kenya-to-netherlands/", "Repatriation from Kenya to the Netherlands",
    ),
    # Rwanda routes
    ("rwanda", "australia"): (
        "/routes/rwanda-to-united-kingdom/", "Repatriation from Rwanda to the UK",
        "/routes/kenya-to-australia/", "Repatriation from Kenya to Australia",
    ),
    ("rwanda", "canada"): (
        "/routes/rwanda-to-united-kingdom/", "Repatriation from Rwanda to the UK",
        "/routes/kenya-to-canada/", "Repatriation from Kenya to Canada",
    ),
    ("rwanda", "italy"): (
        "/routes/rwanda-to-united-kingdom/", "Repatriation from Rwanda to the UK",
        "/routes/kenya-to-italy/", "Repatriation from Kenya to Italy",
    ),
    ("rwanda", "netherlands"): (
        "/routes/rwanda-to-united-kingdom/", "Repatriation from Rwanda to the UK",
        "/routes/kenya-to-netherlands/", "Repatriation from Kenya to the Netherlands",
    ),
    ("rwanda", "sweden"): (
        "/routes/rwanda-to-united-kingdom/", "Repatriation from Rwanda to the UK",
        "/routes/kenya-to-sweden/", "Repatriation from Kenya to Sweden",
    ),
    # Somalia routes
    ("somalia", "france"): (
        "/routes/somalia-to-united-kingdom/", "Repatriation from Somalia to the UK",
        "/routes/ethiopia-to-france/", "Repatriation from Ethiopia to France",
    ),
    ("somalia", "australia"): (
        "/routes/somalia-to-united-kingdom/", "Repatriation from Somalia to the UK",
        "/routes/ethiopia-to-australia/", "Repatriation from Ethiopia to Australia",
    ),
    ("somalia", "italy"): (
        "/routes/somalia-to-united-kingdom/", "Repatriation from Somalia to the UK",
        "/routes/ethiopia-to-italy/", "Repatriation from Ethiopia to Italy",
    ),
    ("somalia", "spain"): (
        "/routes/somalia-to-united-kingdom/", "Repatriation from Somalia to the UK",
        "/routes/nigeria-to-spain/", "Repatriation from Nigeria to Spain",
    ),
    ("somalia", "switzerland"): (
        "/routes/somalia-to-united-kingdom/", "Repatriation from Somalia to the UK",
        "/routes/ethiopia-to-switzerland/", "Repatriation from Ethiopia to Switzerland",
    ),
    # Sudan routes
    ("sudan", "canada"): (
        "/routes/sudan-to-united-kingdom/", "Repatriation from Sudan to the UK",
        "/routes/ethiopia-to-canada/", "Repatriation from Ethiopia to Canada",
    ),
    ("sudan", "france"): (
        "/routes/sudan-to-united-kingdom/", "Repatriation from Sudan to the UK",
        "/routes/ethiopia-to-france/", "Repatriation from Ethiopia to France",
    ),
    ("sudan", "germany"): (
        "/routes/sudan-to-united-kingdom/", "Repatriation from Sudan to the UK",
        "/routes/ethiopia-to-germany/", "Repatriation from Ethiopia to Germany",
    ),
    ("sudan", "italy"): (
        "/routes/sudan-to-united-kingdom/", "Repatriation from Sudan to the UK",
        "/routes/ethiopia-to-italy/", "Repatriation from Ethiopia to Italy",
    ),
    ("sudan", "netherlands"): (
        "/routes/sudan-to-united-kingdom/", "Repatriation from Sudan to the UK",
        "/routes/ethiopia-to-netherlands/", "Repatriation from Ethiopia to the Netherlands",
    ),
    # Jamaica routes
    ("jamaica", "australia"): (
        "/routes/jamaica-to-united-kingdom/", "Repatriation from Jamaica to the UK",
        "/routes/barbados-to-australia/", "Repatriation from Barbados to Australia",
    ),
    ("jamaica", "germany"): (
        "/routes/jamaica-to-united-kingdom/", "Repatriation from Jamaica to the UK",
        "/routes/barbados-to-germany/", "Repatriation from Barbados to Germany",
    ),
    ("jamaica", "france"): (
        "/routes/jamaica-to-united-kingdom/", "Repatriation from Jamaica to the UK",
        "/routes/barbados-to-france/", "Repatriation from Barbados to France",
    ),
    ("jamaica", "italy"): (
        "/routes/jamaica-to-united-kingdom/", "Repatriation from Jamaica to the UK",
        "/routes/trinidad-and-tobago-to-italy/", "Repatriation from Trinidad and Tobago to Italy",
    ),
    ("jamaica", "netherlands"): (
        "/routes/jamaica-to-united-kingdom/", "Repatriation from Jamaica to the UK",
        "/routes/trinidad-and-tobago-to-netherlands/", "Repatriation from Trinidad and Tobago to the Netherlands",
    ),
    # Barbados routes
    ("barbados", "canada"): (
        "/routes/barbados-to-united-kingdom/", "Repatriation from Barbados to the UK",
        "/routes/jamaica-to-canada/", "Repatriation from Jamaica to Canada",
    ),
    ("barbados", "france"): (
        "/routes/barbados-to-united-kingdom/", "Repatriation from Barbados to the UK",
        "/routes/jamaica-to-france/", "Repatriation from Jamaica to France",
    ),
    ("barbados", "germany"): (
        "/routes/barbados-to-united-kingdom/", "Repatriation from Barbados to the UK",
        "/routes/jamaica-to-germany/", "Repatriation from Jamaica to Germany",
    ),
    ("barbados", "australia"): (
        "/routes/barbados-to-united-kingdom/", "Repatriation from Barbados to the UK",
        "/routes/jamaica-to-australia/", "Repatriation from Jamaica to Australia",
    ),
    ("barbados", "netherlands"): (
        "/routes/barbados-to-united-kingdom/", "Repatriation from Barbados to the UK",
        "/routes/jamaica-to-netherlands/", "Repatriation from Jamaica to the Netherlands",
    ),
    # Cyprus routes
    ("cyprus", "france"): (
        "/routes/cyprus-to-united-kingdom/", "Repatriation from Cyprus to the UK",
        "/routes/greece-to-france/", "Repatriation from Greece to France",
    ),
    ("cyprus", "italy"): (
        "/routes/cyprus-to-united-kingdom/", "Repatriation from Cyprus to the UK",
        "/routes/greece-to-italy/", "Repatriation from Greece to Italy",
    ),
    ("cyprus", "australia"): (
        "/routes/cyprus-to-united-kingdom/", "Repatriation from Cyprus to the UK",
        "/routes/greece-to-australia/", "Repatriation from Greece to Australia",
    ),
    ("cyprus", "netherlands"): (
        "/routes/cyprus-to-united-kingdom/", "Repatriation from Cyprus to the UK",
        "/routes/greece-to-netherlands/", "Repatriation from Greece to the Netherlands",
    ),
    ("cyprus", "canada"): (
        "/routes/cyprus-to-united-kingdom/", "Repatriation from Cyprus to the UK",
        "/routes/greece-to-canada/", "Repatriation from Greece to Canada",
    ),
    # Hong Kong routes
    ("hong-kong", "australia"): (
        "/routes/hong-kong-to-united-kingdom/", "Repatriation from Hong Kong to the UK",
        "/routes/singapore-to-australia/", "Repatriation from Singapore to Australia",
    ),
    ("hong-kong", "canada"): (
        "/routes/hong-kong-to-united-kingdom/", "Repatriation from Hong Kong to the UK",
        "/routes/singapore-to-canada/", "Repatriation from Singapore to Canada",
    ),
    ("hong-kong", "germany"): (
        "/routes/hong-kong-to-united-kingdom/", "Repatriation from Hong Kong to the UK",
        "/routes/singapore-to-germany/", "Repatriation from Singapore to Germany",
    ),
    ("hong-kong", "france"): (
        "/routes/hong-kong-to-united-kingdom/", "Repatriation from Hong Kong to the UK",
        "/routes/singapore-to-france/", "Repatriation from Singapore to France",
    ),
    ("hong-kong", "india"): (
        "/routes/hong-kong-to-united-kingdom/", "Repatriation from Hong Kong to the UK",
        "/routes/singapore-to-india/", "Repatriation from Singapore to India",
    ),
    # Myanmar routes
    ("myanmar", "italy"): (
        "/routes/myanmar-to-united-kingdom/", "Repatriation from Myanmar to the UK",
        "/routes/thailand-to-italy/", "Repatriation from Thailand to Italy",
    ),
    ("myanmar", "spain"): (
        "/routes/myanmar-to-united-kingdom/", "Repatriation from Myanmar to the UK",
        "/routes/thailand-to-spain/", "Repatriation from Thailand to Spain",
    ),
    ("myanmar", "netherlands"): (
        "/routes/myanmar-to-united-kingdom/", "Repatriation from Myanmar to the UK",
        "/routes/thailand-to-netherlands/", "Repatriation from Thailand to the Netherlands",
    ),
    ("myanmar", "sweden"): (
        "/routes/myanmar-to-united-kingdom/", "Repatriation from Myanmar to the UK",
        "/routes/thailand-to-sweden/", "Repatriation from Thailand to Sweden",
    ),
    ("myanmar", "norway"): (
        "/routes/myanmar-to-united-kingdom/", "Repatriation from Myanmar to the UK",
        "/routes/thailand-to-norway/", "Repatriation from Thailand to Norway",
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

    if dest_key == "germany":
        consular = f"Notify the German Embassy in {origin}."
        reception_step = "German funeral director takes custody at cargo terminal. Standesamt notified."
    elif dest_key == "france":
        consular = f"Notify the French Embassy in {origin}."
        reception_step = "French funeral director takes custody at cargo terminal. Mairie notified."
    elif dest_key == "australia":
        consular = "Notify Australian High Commission or Embassy. DFAT emergency: +61 2 6261 3305."
        reception_step = "Australian funeral director takes custody. ABF clearance completed. State BDM notified."
    elif dest_key == "netherlands":
        consular = f"Notify the Netherlands Embassy in {origin}."
        reception_step = "Dutch funeral director takes custody at cargo terminal. Gemeente BRP notified."
    elif dest_key == "canada":
        consular = "Notify Canadian High Commission or Embassy. Global Affairs Canada emergency: +1-613-996-8885."
        reception_step = "Canadian funeral director takes custody at cargo terminal. Provincial BDM notified."
    elif dest_key == "sweden":
        consular = f"Notify the Swedish Embassy in {origin}."
        reception_step = "Swedish funeral director takes custody at cargo terminal. Skatteverket notified."
    elif dest_key == "norway":
        consular = f"Notify the Norwegian Embassy in {origin}."
        reception_step = "Norwegian funeral director takes custody at cargo terminal. Folkeregisteret notified."
    elif dest_key == "spain":
        consular = f"Notify the Spanish Embassy in {origin}."
        reception_step = "Spanish funeral director takes custody at cargo terminal. Registro Civil notified."
    elif dest_key == "italy":
        consular = f"Notify the Italian Embassy in {origin}."
        reception_step = "Italian funeral director takes custody at cargo terminal. Comune notified."
    elif dest_key == "portugal":
        consular = f"Notify the Portuguese Embassy in {origin}."
        reception_step = "Portuguese funeral director takes custody at cargo terminal. Conservatoria do Registo Civil notified."
    elif dest_key == "belgium":
        consular = f"Notify the Belgian Embassy in {origin}."
        reception_step = "Belgian funeral director takes custody at cargo terminal. Commune/gemeenten notified."
    elif dest_key == "jordan":
        consular = f"Notify the Jordanian Embassy in {origin}. Jordanian Ministry of Foreign Affairs: +962 6 567 8311."
        reception_step = "Jordanian funeral director takes custody at cargo terminal. NCSPC notified."
    elif dest_key == "malaysia":
        consular = f"Notify the Malaysian High Commission in {origin}. Wisma Putra: +60 3 8000 8000."
        reception_step = "Malaysian funeral director takes custody at cargo terminal. JPN notified. Documents authenticated by Wisma Putra."
    elif dest_key == "switzerland":
        consular = f"Notify the Swiss Embassy in {origin}. FDFA Helpline: +41 800 24-7-365."
        reception_step = "Swiss funeral director takes custody at cargo terminal. Zivilstandsamt notified."
    elif dest_key == "india":
        consular = "Notify Indian High Commission or Embassy. Ministry of External Affairs India: +91 11 2301 2113."
        reception_step = "Indian funeral director takes custody at cargo terminal. Customs clearance completed. State civil registrar notified."
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

    # Use override consular FAQ if set (e.g. for Somalia, Sudan, Iraq)
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
        f"/routes/india-to-{dest_key}/", f"Repatriation from India to {d['name']}",
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
        ("R91", R91_ROUTES, 2),   # Start at C (index 2)
        ("R92", R92_ROUTES, 2),   # Start at C (index 2)
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
