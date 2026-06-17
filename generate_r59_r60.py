#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R59-R60.

   R59 (25 routes, variants D,E,A,B,C x5):
     Egypt x5: india, pakistan, germany, france, italy
     Pakistan (dest) x5: united-kingdom, germany, united-states, norway, sweden
     Philippines x5: united-states, saudi-arabia, australia, canada, japan
     Vietnam x5: united-states, australia, france, germany, canada
     Bangladesh x5: united-kingdom, italy, germany, sweden, norway

   R60 (25 routes, variants D,E,A,B,C x5):
     Thailand x5: united-kingdom, united-states, sweden, norway, france
     China x5: united-states, australia, canada, united-kingdom, sweden
     Morocco x5: france, spain, belgium, netherlands, united-kingdom
     Jordan x5: united-kingdom, united-states, canada, france, italy
     Sri Lanka x5: united-kingdom, germany, sweden, norway, netherlands

   Template rotation: R58 ended C (index 2). R59 starts D (index 3).
   Each block of 25 cycles D,E,A,B,C x5, ending on C. R60 starts D again.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 3  # D

DEST_META = {
    'egypt': {
        'name': 'Egypt',
        'slug': 'egypt',
        'key': 'eg',
        'reception': (
            "The Egyptian funeral director takes custody at Cairo International "
            "Airport (CAI) cargo terminal. The Civil Status Authority (Maslahat "
            "al-Ahwal al-Madaniyya) processes death registration for foreign "
            "nationals. The niyaba (public prosecutor) takes jurisdiction for any "
            "case with an unclear cause of death. All foreign documents must be in "
            "Arabic or accompanied by a certified Arabic translation. An embalming "
            "certificate and hermetically sealed coffin are required for all air "
            "imports. Cremation is not available in Egypt; all repatriations must "
            "be of the full body. Authentication by the Egyptian Embassy or Consulate "
            "in the country of origin is required for all documents. "
            "(Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Egyptian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Egypt. The Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Egyptian funeral director takes custody at Cairo International "
            "Airport (CAI) cargo terminal. The Civil Status Authority (Maslahat "
            "al-Ahwal al-Madaniyya) registers the death. The niyaba (public "
            "prosecutor) may be involved where the cause of death is unclear. All "
            "foreign documents require certified Arabic translation and authentication "
            "by the Egyptian Embassy in the origin country. An embalming certificate "
            "and hermetically sealed coffin are required. Cremation is not available; "
            "burial is the only option. The receiving funeral director coordinates "
            "with the Civil Status Authority."
        ),
        'emergency_line': 'contact the Egyptian Embassy in the origin country',
        'hub_url': 'repatriation-from-egypt',
    },
    'pakistan': {
        'name': 'Pakistan',
        'slug': 'pakistan',
        'key': 'pk',
        'reception': (
            "The Pakistani funeral director takes custody at the receiving airport: "
            "Islamabad International Airport (ISB), Jinnah International Airport "
            "Karachi (KHI), or Allama Iqbal International Airport Lahore (LHE), "
            "depending on the final destination. NADRA (National Database and "
            "Registration Authority) processes civil registration. For Muslim remains, "
            "Islamic law procedures apply and prompt burial is required; a burial "
            "permit from the relevant health authority is needed before final "
            "disposition. All foreign documents require certified translation. "
            "Pakistan is not a member of the Hague Apostille Convention; full "
            "consular authentication is required. Authentication by the Pakistani "
            "High Commission or Embassy in the country of origin is required. "
            "(Pakistan Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Pakistani High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Pakistan. The High "
            "Commission cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Pakistani funeral director takes custody at Islamabad International "
            "(ISB), Jinnah International Karachi (KHI), or Allama Iqbal Lahore (LHE) "
            "cargo terminal. NADRA processes civil registration. For Muslim remains, "
            "Islamic law procedures apply and prompt burial is required. A burial "
            "permit from the relevant health authority is needed before final "
            "disposition. All foreign documents require certified translation. Pakistan "
            "is not a Hague Apostille member; full consular authentication through "
            "the Pakistani High Commission or Embassy in the origin country is required."
        ),
        'emergency_line': 'contact the Pakistani High Commission in the origin country',
        'hub_url': 'repatriation-from-pakistan',
    },
    'philippines': {
        'name': 'the Philippines',
        'slug': 'philippines',
        'key': 'ph',
        'reception': (
            "The Philippine funeral director takes custody at Ninoy Aquino "
            "International Airport (NAIA) cargo terminal in Manila, or at the "
            "relevant regional airport for other destinations. The Bureau of "
            "Quarantine must clear all incoming remains. The Philippine Statistics "
            "Authority (PSA) is notified of the death. English is an official "
            "language in the Philippines, which simplifies documentation from "
            "English-speaking origin countries. The Philippines is a member of "
            "the Hague Apostille Convention; apostille certificates are accepted "
            "for documents from member states. All other documents require full "
            "consular authentication. An embalming certificate and hermetically "
            "sealed coffin are required. (Philippine Department of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Philippine Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to the Philippines. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Philippine funeral director takes custody at Ninoy Aquino "
            "International Airport (NAIA) cargo terminal in Manila. The Bureau of "
            "Quarantine clears the consignment. The Philippine Statistics Authority "
            "(PSA) is notified of the death. Documents from Hague Apostille member "
            "countries are accepted with an apostille certificate; all others require "
            "full consular authentication. An embalming certificate and hermetically "
            "sealed coffin are required. The receiving funeral director coordinates "
            "with PSA and the Bureau of Quarantine."
        ),
        'emergency_line': 'contact the Philippine Embassy in the origin country',
        'hub_url': 'repatriation-from-philippines',
    },
    'vietnam': {
        'name': 'Vietnam',
        'slug': 'vietnam',
        'key': 'vn',
        'reception': (
            "The Vietnamese funeral director takes custody at Noi Bai International "
            "Airport (HAN) in Hanoi or Tan Son Nhat International Airport (SGN) in "
            "Ho Chi Minh City. The local People's Committee civil status office "
            "handles death registration. A Ministry of Health import permit is "
            "required for all incoming remains. All foreign documents must be "
            "accompanied by certified Vietnamese translation and legalised through "
            "the Vietnamese Embassy in the country of origin. Vietnam is not a "
            "member of the Hague Apostille Convention; full consular legalisation "
            "is required for all documents. An embalming certificate and "
            "hermetically sealed coffin are required. "
            "(Vietnamese Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Vietnamese Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Vietnam. Legalisation of origin country "
            "documents must go through the Vietnamese Embassy. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Vietnamese funeral director takes custody at Noi Bai International "
            "Airport (HAN) in Hanoi or Tan Son Nhat International Airport (SGN) in "
            "Ho Chi Minh City. The local People's Committee civil status office "
            "handles death registration. A Ministry of Health import permit is "
            "required. All foreign documents require certified Vietnamese translation "
            "and legalisation through the Vietnamese Embassy in the origin country. "
            "Vietnam is not a Hague Apostille member; full consular legalisation "
            "is required. The receiving funeral director coordinates with the "
            "People's Committee civil status office."
        ),
        'emergency_line': 'contact the Vietnamese Embassy in the origin country',
        'hub_url': 'repatriation-from-vietnam',
    },
    'bangladesh': {
        'name': 'Bangladesh',
        'slug': 'bangladesh',
        'key': 'bd',
        'reception': (
            "The Bangladeshi funeral director takes custody at Hazrat Shahjalal "
            "International Airport (DAC) cargo terminal in Dhaka. Bangladesh Civil "
            "Aviation Authority (BCAA) clearance is required for all cargo "
            "shipments. The Registrar General of Birth and Death (RGBD) registers "
            "the death. For Muslim remains, Islamic law procedures apply and prompt "
            "burial is required; a burial permit from the relevant health authority "
            "is needed. All foreign documents require certified translation into "
            "Bengali or English. Bangladesh is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Bangladeshi High "
            "Commission or Embassy in the country of origin is required. A sealed "
            "zinc-lined coffin is required for all repatriations. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Bangladeshi High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Bangladesh. The High "
            "Commission cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Bangladeshi funeral director takes custody at Hazrat Shahjalal "
            "International Airport (DAC) cargo terminal in Dhaka. Bangladesh Civil "
            "Aviation Authority (BCAA) clearance is required. The RGBD registers "
            "the death. For Muslim remains, Islamic law procedures apply and a "
            "burial permit from the relevant health authority is required. All "
            "foreign documents require certified Bengali or English translation. "
            "Bangladesh is not a Hague Apostille member; full consular authentication "
            "through the Bangladeshi High Commission or Embassy in the origin "
            "country is required. A sealed zinc-lined coffin is required."
        ),
        'emergency_line': 'contact the Bangladeshi High Commission in the origin country',
        'hub_url': 'repatriation-from-bangladesh',
    },
    'thailand': {
        'name': 'Thailand',
        'slug': 'thailand',
        'key': 'th',
        'reception': (
            "The Thai funeral director takes custody at Suvarnabhumi Airport (BKK) "
            "or Don Mueang International Airport (DMK) cargo terminal. The "
            "Department of Provincial Administration (DOPA) Civil Registration "
            "Division handles death registration. A Ministry of Public Health "
            "inspection of the remains is required on arrival. All foreign documents "
            "require certified Thai translation. Thailand is not a member of the "
            "Hague Apostille Convention; full consular legalisation through the "
            "Thai Embassy or Consulate in the country of origin is required. An "
            "embalming certificate and hermetically sealed coffin are required for "
            "all air imports. A burial or cremation permit from DOPA is required "
            "before final disposition. (Thai Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Thai Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Thailand. The Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Thai funeral director takes custody at Suvarnabhumi Airport (BKK) "
            "or Don Mueang (DMK) cargo terminal. The Department of Provincial "
            "Administration (DOPA) Civil Registration Division registers the death. "
            "A Ministry of Public Health inspection is required on arrival. All "
            "foreign documents require certified Thai translation. Thailand is not "
            "a Hague Apostille member; full consular legalisation through the Thai "
            "Embassy in the origin country is required. An embalming certificate "
            "and hermetically sealed coffin are required. A burial or cremation "
            "permit from DOPA is required before final disposition."
        ),
        'emergency_line': 'contact the Thai Embassy in the origin country',
        'hub_url': 'repatriation-from-thailand',
    },
    'china': {
        'name': 'China',
        'slug': 'china',
        'key': 'cn',
        'reception': (
            "The Chinese funeral director takes custody at the receiving airport: "
            "Beijing Capital International Airport (PEK), Shanghai Pudong "
            "International Airport (PVG), or Guangzhou Baiyun International Airport "
            "(CAN) cargo terminal, depending on the destination city. The General "
            "Administration of Customs carries out quarantine inspection of all "
            "incoming remains. The Ministry of Civil Affairs (MCA) oversees "
            "mortuary standards and civil registration. All foreign documents "
            "require certified simplified Chinese translation. China is not a "
            "member of the Hague Apostille Convention; full consular legalisation "
            "through the Chinese Embassy or Consulate in the country of origin is "
            "required for all documents. An embalming certificate, health certificate, "
            "and hermetically sealed coffin are required. Quarantine clearance "
            "procedures are strict and documentation must be complete before the "
            "body is released for final disposition. "
            "(Chinese Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Chinese Embassy or Consulate in {city} can advise on documentation "
            "requirements and legalisation for repatriation to China. China is not "
            "a Hague Apostille member; all documents must be legalised through the "
            "Chinese Embassy. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Chinese funeral director takes custody at Beijing Capital (PEK), "
            "Shanghai Pudong (PVG), or Guangzhou Baiyun (CAN) cargo terminal. "
            "The General Administration of Customs carries out quarantine inspection. "
            "The Ministry of Civil Affairs (MCA) oversees mortuary standards. All "
            "foreign documents require certified simplified Chinese translation and "
            "full consular legalisation through the Chinese Embassy in the origin "
            "country. China is not a Hague Apostille member. Quarantine clearance "
            "procedures are strict and all documentation must be complete before "
            "the body is released for final disposition."
        ),
        'emergency_line': 'contact the Chinese Embassy in the origin country',
        'hub_url': 'repatriation-from-china',
    },
    'morocco': {
        'name': 'Morocco',
        'slug': 'morocco',
        'key': 'ma',
        'reception': (
            "The Moroccan funeral director takes custody at Mohammed V International "
            "Airport (CMN) in Casablanca, or Marrakech Menara Airport (RAK) for "
            "arrivals in the south. Civil registration is handled by the local "
            "etat civil (civil registry). For Muslim remains, documentation from "
            "the Adoul (notarial authority) confirming Islamic identity may be "
            "required before burial; Islamic law procedures apply and prompt burial "
            "is expected. All foreign documents require certified Arabic translation; "
            "French-language documents are also accepted in Morocco. Morocco joined "
            "the Hague Apostille Convention in 2021. Authentication by the Moroccan "
            "Embassy or Consulate in the country of origin is required for documents "
            "not covered by the apostille process. A hermetically sealed coffin "
            "is required. (Moroccan Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Moroccan Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Morocco. Morocco joined the Hague "
            "Apostille Convention in 2021. The Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Moroccan funeral director takes custody at Mohammed V International "
            "Airport (CMN) or Marrakech Menara (RAK) cargo terminal. The local "
            "etat civil (civil registry) registers the death. For Muslim remains, "
            "Adoul documentation and Islamic law procedures apply; prompt burial is "
            "expected. All foreign documents require certified Arabic translation. "
            "Morocco joined the Hague Apostille Convention in 2021; apostille "
            "certificates are accepted from member states. A hermetically sealed "
            "coffin is required. The receiving funeral director coordinates with "
            "the etat civil and relevant religious authorities."
        ),
        'emergency_line': 'contact the Moroccan Embassy in the origin country',
        'hub_url': 'repatriation-from-morocco',
    },
    'jordan': {
        'name': 'Jordan',
        'slug': 'jordan',
        'key': 'jo',
        'reception': (
            "The Jordanian funeral director takes custody at Queen Alia International "
            "Airport (AMM) cargo terminal in Amman. The Ministry of Interior civil "
            "registration department processes death documentation. Ministry of "
            "Health clearance is required before final disposition. For Muslim "
            "remains, Islamic law procedures apply and prompt burial is expected. "
            "All foreign documents require certified Arabic translation and "
            "authentication by the Jordanian Embassy or Consulate in the country "
            "of origin. An embalming certificate and hermetically sealed coffin "
            "are required. A burial permit from the Ministry of Health must be "
            "obtained before the body is released. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Jordanian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Jordan. The Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Jordanian funeral director takes custody at Queen Alia International "
            "Airport (AMM) cargo terminal in Amman. The Ministry of Interior civil "
            "registration department processes the death documentation. Ministry of "
            "Health clearance is required before final disposition. For Muslim "
            "remains, Islamic law procedures apply and prompt burial is expected. "
            "All foreign documents require certified Arabic translation and "
            "authentication by the Jordanian Embassy in the origin country. A "
            "burial permit from the Ministry of Health must be obtained."
        ),
        'emergency_line': 'contact the Jordanian Embassy in the origin country',
        'hub_url': 'repatriation-from-jordan',
    },
    'sri-lanka': {
        'name': 'Sri Lanka',
        'slug': 'sri-lanka',
        'key': 'lk',
        'reception': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) cargo terminal in Colombo. The Registrar "
            "General's Department registers the death. Ministry of Health clearance "
            "is required before final disposition. Sri Lanka is not a member of "
            "the Hague Apostille Convention; full consular authentication through "
            "the Sri Lankan High Commission or Embassy in the country of origin is "
            "required for all documents. All foreign documents require certified "
            "translation. A sealed zinc-lined coffin and embalming certificate "
            "are required for all air imports. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Sri Lankan High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Sri Lanka. Sri Lanka "
            "is not a Hague Apostille member; all documents must be authenticated "
            "through the Sri Lankan High Commission. The High Commission cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) cargo terminal in Colombo. The Registrar "
            "General's Department registers the death. Ministry of Health clearance "
            "is required before final disposition. Sri Lanka is not a Hague "
            "Apostille member; full consular authentication through the Sri Lankan "
            "High Commission or Embassy in the origin country is required. A sealed "
            "zinc-lined coffin and embalming certificate are required. The receiving "
            "funeral director coordinates with the Registrar General's Department."
        ),
        'emergency_line': 'contact the Sri Lankan High Commission in the origin country',
        'hub_url': 'repatriation-from-sri-lanka',
    },
}

ORIGIN_DATA = {
    'india': {
        'name': 'India',
        'emergency': '112 (unified) / 100 (police) / 108 (ambulance)',
        'registry': 'the local Registrar of Births and Deaths under the state civil registration system',
        'cert_name': 'death certificate',
        'cert_lang': 'English or regional language (varies by state)',
        'overview': (
            "Call 112 for emergency services, 100 for police, or 108 for ambulance. "
            "Death is certified by a physician. The death is registered with the "
            "local Registrar of Births and Deaths under the state civil registration "
            "system. Documentation language varies by state; English-language "
            "certificates are issued in most urban areas. Police take jurisdiction "
            "for violent or unexplained deaths. India is a Hague Apostille "
            "Convention member. Processing times vary by state; large cities "
            "process faster than rural areas. Tropical conditions in many regions "
            "require prompt embalming."
        ),
        'doc_time': '5-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is widely available in India and is the traditional rite "
            "for Hindu and Sikh communities. Muslim remains require burial. "
            "A cremation certificate is required for export of ashes."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'pakistan': {
        'name': 'Pakistan',
        'emergency': '15 (emergency) / 1122 (rescue)',
        'registry': 'the NADRA (National Database and Registration Authority) system via the Union Council or hospital',
        'cert_name': 'death certificate',
        'cert_lang': 'Urdu and English',
        'overview': (
            "Call 15 for emergency services or 1122 for rescue services. Death is "
            "certified by a physician. The death is registered through the NADRA "
            "(National Database and Registration Authority) system via the relevant "
            "Union Council or hospital. Documentation is in Urdu and English. "
            "Police take jurisdiction for violent or unexplained deaths. Pakistan "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication is required for international documentation. The "
            "tropical climate in Karachi and other cities requires prompt embalming."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available for Muslim remains in Pakistan. Non-Muslim "
            "remains may be repatriated for cremation in the destination country."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'united-kingdom': {
        'name': 'the United Kingdom',
        'emergency': '999 (police, fire, ambulance)',
        'registry': (
            'the register office in England and Wales, National Records of Scotland, '
            'or the General Register Office Northern Ireland (GRONI)'
        ),
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 999 for emergency services. Death is certified by a physician or, "
            "where necessary, the coroner. The death must be registered at the local "
            "register office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The coroner takes "
            "jurisdiction for sudden, violent, or unexplained deaths and must issue "
            "a removal order before the body can leave England and Wales. The United "
            "Kingdom is a Hague Apostille Convention member. Coroner cases add time: "
            "the coroner must be satisfied the body may leave before issuing the "
            "order for removal out of England and Wales."
        ),
        'doc_time': '3-7 days (coroner cases longer)',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in the United Kingdom is widely available. A second medical "
            "certificate is required for cremation before the body can be removed. "
            "If the coroner is involved, a coroner's certificate replaces the second "
            "medical certificate."
        ),
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
    'united-states': {
        'name': 'the United States',
        'emergency': '911',
        'registry': 'the state civil records office where the death occurred',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician or "
            "medical examiner. The death is registered with the state civil records "
            "office where the death occurred. Each US state operates its own civil "
            "records system. The coroner or medical examiner takes jurisdiction for "
            "violent, sudden, or unexplained deaths, with processes varying by state. "
            "The United States is a Hague Apostille Convention member. The British "
            "Embassy in Washington DC or the relevant British Consulate can assist "
            "British nationals."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in the United States is widely available in all states.",
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths (medical examiner or coroner, varies by state)',
    },
    'australia': {
        'name': 'Australia',
        'emergency': '000 (police, fire, ambulance)',
        'registry': 'the state or territory Births, Deaths and Marriages (BDM) registry',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 000 for emergency services. Death is certified by a registered "
            "medical practitioner. The death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. The coroner takes "
            "jurisdiction for sudden, violent, or unexplained deaths. Australia is "
            "a Hague Apostille Convention member. The registration process is "
            "straightforward; the coroner's release is the main cause of delay in "
            "complex cases. The British High Commission in Canberra or the relevant "
            "Consulate can assist British nationals."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Australia is widely available in all states and territories.",
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
    'germany': {
        'name': 'Germany',
        'emergency': '112',
        'registry': 'the local Standesamt (civil registry)',
        'cert_name': 'Sterbeurkunde (death certificate)',
        'cert_lang': 'German',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician "
            "and registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German. Police and the Staatsanwaltschaft "
            "(public prosecutor) take jurisdiction for violent or unexplained "
            "deaths. Germany is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Germany is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft)',
    },
    'france': {
        'name': 'France',
        'emergency': '17 (police) / 15 (ambulance) / 112 (EU emergency)',
        'registry': 'the local mairie (town hall) civil registry',
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'French',
        'overview': (
            "Call 17 for police, 15 for ambulance, or 112 for the EU emergency "
            "number. Death is certified by a physician. The acte de deces is "
            "registered with the local mairie (town hall). The Procureur de la "
            "Republique (public prosecutor) takes jurisdiction for violent or "
            "unexplained deaths. France is an EU member and Hague Apostille "
            "Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in France is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Procureur de la Republique)',
    },
    'italy': {
        'name': 'Italy',
        'emergency': '112 (unified) / 113 (police) / 118 (ambulance)',
        'registry': 'the local Ufficio di Stato Civile (civil registry) of the Comune',
        'cert_name': 'atto di morte (death certificate)',
        'cert_lang': 'Italian',
        'overview': (
            "Call 112 for the unified emergency number, 113 for police, or 118 "
            "for ambulance. Death is certified by a physician. The atto di morte "
            "is registered with the local Ufficio di Stato Civile of the Comune "
            "(municipality). The Procura della Repubblica (public prosecutor) takes "
            "jurisdiction for violent or unexplained deaths. Italy is an EU member "
            "and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Italy is available, though less common than in northern "
            "Europe; facilities exist in major cities."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Procura della Repubblica)',
    },
    'norway': {
        'name': 'Norway',
        'emergency': '112 (police) / 113 (ambulance)',
        'registry': 'the Norwegian National Population Register (Folkeregisteret)',
        'cert_name': 'death certificate',
        'cert_lang': 'Norwegian',
        'overview': (
            "Call 112 for police or 113 for ambulance. Death is certified by a "
            "physician. The death is registered with the Norwegian National "
            "Population Register (Folkeregisteret). Police take jurisdiction for "
            "violent or unexplained deaths. Norway is a Hague Apostille Convention "
            "member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Norway is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'sweden': {
        'name': 'Sweden',
        'emergency': '112',
        'registry': 'the Swedish Tax Agency (Skatteverket)',
        'cert_name': 'death certificate',
        'cert_lang': 'Swedish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The death is registered with the Swedish Tax Agency (Skatteverket), "
            "which manages the population register. Police take jurisdiction for "
            "violent or unexplained deaths. Sweden is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Sweden is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'canada': {
        'name': 'Canada',
        'emergency': '911',
        'registry': 'the provincial civil records registry',
        'cert_name': 'death certificate',
        'cert_lang': 'English or French',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician "
            "or medical examiner. The death is registered with the provincial "
            "civil records registry. The coroner or medical examiner takes "
            "jurisdiction for sudden, violent, or unexplained deaths. Canada is "
            "a Hague Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Canada is widely available.",
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner or medical examiner)',
    },
    'japan': {
        'name': 'Japan',
        'emergency': '110 (police) / 119 (ambulance)',
        'registry': 'the local municipal office (shiyakusho or kuyakusho)',
        'cert_name': 'shibo todoke (death notification)',
        'cert_lang': 'Japanese',
        'overview': (
            "Call 110 for police or 119 for ambulance. The shibo todoke (death "
            "notification) must be submitted to the local municipal office "
            "(shiyakusho or kuyakusho) within seven days. A physician must certify "
            "the death. Police and the public prosecutor (Kenji) take jurisdiction "
            "for violent or unexplained deaths. All documentation is in Japanese "
            "and requires certified translation."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': 'Cremation is the standard final disposition in Japan (over 99%).',
        'postmortem_trigger': 'Violent or unexplained deaths (public prosecutor, Kenji)',
    },
    'netherlands': {
        'name': 'the Netherlands',
        'emergency': '112',
        'registry': 'the gemeente (municipality) civil registry',
        'cert_name': 'akte van overlijden (death certificate)',
        'cert_lang': 'Dutch',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The akte van overlijden is registered with the local gemeente "
            "(municipality). Police and the Officier van Justitie (public "
            "prosecutor) take jurisdiction for violent or unexplained deaths. "
            "The Netherlands is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in the Netherlands is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Officier van Justitie)',
    },
    'belgium': {
        'name': 'Belgium',
        'emergency': '112 (ambulance) / 101 (police)',
        'registry': 'the commune (local authority) civil registry',
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'French, Dutch, or German',
        'overview': (
            "Call 112 for ambulance or 101 for police. Death is certified by a "
            "physician. The acte de deces is registered with the local commune "
            "civil registry. The Parquet (public prosecutor) takes jurisdiction "
            "for violent or unexplained deaths. Belgium is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Belgium is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Parquet)',
    },
    'spain': {
        'name': 'Spain',
        'emergency': '112 (unified) / 091 (national police)',
        'registry': 'the Registro Civil (civil registry)',
        'cert_name': 'certificado de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for the unified emergency number or 091 for the national "
            "police. Death is certified by a physician. The certificado de defuncion "
            "is registered with the local Registro Civil. The Juzgado de Guardia "
            "(duty magistrate's court) takes jurisdiction for violent or unexplained "
            "deaths. Spain is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Spain is widely available.",
        'postmortem_trigger': "Violent or unexplained deaths (Juzgado de Guardia)",
    },
    'saudi-arabia': {
        'name': 'Saudi Arabia',
        'emergency': '911',
        'registry': 'the Ministry of Interior civil registration system',
        'cert_name': 'death certificate',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician "
            "and registered through the Ministry of Interior civil registration "
            "system. The Public Prosecution takes jurisdiction for violent or "
            "unexplained deaths. All documentation is in Arabic. Saudi Arabia's "
            "climate requires prompt embalming. Muslim remains are handled in "
            "accordance with Islamic law."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available for Muslim remains in Saudi Arabia. "
            "Non-Muslim remains may be repatriated for cremation in the country "
            "of destination."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Public Prosecution)',
    },
}

ROUTES = [
    # R59 -- Egypt wave 1
    {
        'origin': 'india', 'dest': 'egypt',
        'embassy_city': 'New Delhi',
        'intro': (
            "Indian nationals in Egypt include business professionals, traders, "
            "and tourists, reflecting India-Egypt bilateral diplomatic ties dating "
            "to 1947. Both countries are founding members of the Non-Aligned "
            "Movement. Indian death certificates are issued by the local Registrar "
            "of Births and Deaths; the language varies by state. The death "
            "certificate requires certified Arabic translation and authentication "
            "by the Egyptian Embassy in New Delhi for the civil registration "
            "process in Egypt. Egypt joined the Hague Apostille Convention in 2022; "
            "families should confirm current authentication requirements with the "
            "Egyptian Embassy in New Delhi. (Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'pakistan', 'dest': 'egypt',
        'embassy_city': 'Islamabad',
        'intro': (
            "Pakistani nationals in Egypt include students at Al-Azhar University "
            "and other institutions, business professionals, and a community with "
            "close cultural and religious ties. Pakistan and Egypt have maintained "
            "bilateral diplomatic relations within the Organisation of Islamic "
            "Cooperation (OIC). Urdu and English-language Pakistani death "
            "certificates require certified Arabic translation and authentication "
            "by the Egyptian Embassy in Islamabad before civil registration in "
            "Egypt can proceed. (Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'egypt',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Egypt include tourists at Red Sea resorts and "
            "Nile destinations, business professionals, and a small expat community "
            "reflecting Germany-Egypt bilateral trade ties. Germany is among Egypt's "
            "significant European trading partners and both maintain active bilateral "
            "diplomatic relations. German death certificates (Sterbeurkunde, in "
            "German) require certified Arabic translation and authentication by the "
            "Egyptian Embassy in Berlin before civil registration in Egypt can "
            "proceed. Egypt joined the Hague Apostille Convention in 2022; families "
            "should confirm current authentication requirements with the Egyptian "
            "Embassy in Berlin. (Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'egypt',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Egypt include tourists at Red Sea and Nile "
            "destinations, academics, and business professionals. France and Egypt "
            "have maintained close bilateral economic and cultural ties, with France "
            "among Egypt's leading European trading partners. French death "
            "certificates (acte de deces, in French) require certified Arabic "
            "translation and authentication by the Egyptian Embassy in Paris. Egypt "
            "joined the Hague Apostille Convention in 2022; families should confirm "
            "whether apostille authentication applies to their documentation with "
            "the Egyptian Embassy in Paris. (Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'egypt',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Egypt include tourists at Red Sea and Mediterranean "
            "coastal destinations, academics, and business professionals. Italy and "
            "Egypt have bilateral diplomatic and economic ties, with Italy among "
            "Egypt's significant European trading partners. Italian death certificates "
            "(atto di morte, in Italian) require certified Arabic translation and "
            "authentication by the Egyptian Embassy in Rome. Egypt joined the Hague "
            "Apostille Convention in 2022; families should confirm current "
            "authentication requirements with the Egyptian Embassy in Rome. "
            "(Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R59 -- Pakistan (dest) wave 1
    {
        'origin': 'united-kingdom', 'dest': 'pakistan',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Pakistan include dual nationals, individuals with "
            "close family ties reflecting the large British-Pakistani community, "
            "development workers, and business professionals. The UK and Pakistan "
            "have substantial bilateral people-to-people ties. British death "
            "certificates are issued by the relevant register office in England "
            "and Wales, Scotland, or Northern Ireland. The Pakistani High Commission "
            "in London can advise on documentation requirements for repatriation "
            "to Pakistan. Pakistan is not a member of the Hague Apostille "
            "Convention; full consular authentication is required. "
            "(Pakistan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'pakistan',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Pakistan include business professionals, "
            "development workers, and a small community with bilateral ties. "
            "Germany and Pakistan maintain bilateral diplomatic relations and "
            "Germany provides development assistance to Pakistan. German death "
            "certificates (Sterbeurkunde, in German) require certified Urdu or "
            "English translation and authentication by the Pakistani Embassy in "
            "Berlin. Pakistan is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(Pakistan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'pakistan',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Pakistan include dual nationals, business professionals, "
            "development workers, and individuals with family ties to the large "
            "Pakistani-American community. The US and Pakistan have close bilateral "
            "relations. English-language US death certificates are issued by the "
            "state civil records office where the death occurred. The Pakistani "
            "Embassy in Washington DC can advise on documentation requirements "
            "for repatriation to Pakistan. Pakistan is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(Pakistan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'pakistan',
        'embassy_city': 'Oslo',
        'intro': (
            "Norwegian nationals in Pakistan include development workers, academics, "
            "and a small community with bilateral ties. Norway maintains bilateral "
            "development cooperation with Pakistan, with Norwegian funding across "
            "health and education programmes. Norwegian death certificates require "
            "certified Urdu or English translation and authentication by the "
            "Pakistani Embassy in Oslo. Pakistan is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(Pakistan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'pakistan',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in Pakistan include development workers and a small "
            "community with bilateral ties through Sida (Swedish International "
            "Development Cooperation Agency) programmes in Pakistan. Swedish death "
            "certificates require certified Urdu or English translation and "
            "authentication by the Pakistani Embassy in Stockholm. Pakistan is "
            "not a Hague Apostille Convention member; full consular authentication "
            "is required. (Pakistan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R59 -- Philippines wave 1
    {
        'origin': 'united-states', 'dest': 'philippines',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in the Philippines include a significant dual-national "
            "population, business professionals, retirees, and a community "
            "reflecting deep bilateral ties since 1946. English is an official "
            "language in the Philippines, which simplifies documentation. US death "
            "certificates are issued by the state civil records office where "
            "the death occurred. The Philippine Embassy in Washington DC handles "
            "consular matters. Both the US and the Philippines are Hague Apostille "
            "Convention members. (Philippine Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'saudi-arabia', 'dest': 'philippines',
        'embassy_city': 'Riyadh',
        'intro': (
            "This corridor primarily covers repatriation of Filipino overseas "
            "workers (OFWs) and other Filipino nationals who die in Saudi Arabia. "
            "The Philippines maintains an Overseas Workers Welfare Administration "
            "(OWWA) office and Philippine Overseas Labor Office (POLO) in Riyadh "
            "to assist with OFW repatriation. Arabic-language Saudi death "
            "certificates require certified English translation for registration "
            "with the Philippine Statistics Authority (PSA). The Philippine "
            "Consulate General in Riyadh handles consular matters for Filipino "
            "nationals. (Philippine Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'philippines',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in the Philippines include business professionals, "
            "retirees, and individuals with bilateral family ties, reflecting the "
            "large Filipino-Australian community. Australia and the Philippines "
            "maintain bilateral diplomatic relations through ASEAN-Australia "
            "frameworks. Australian death certificates (in English) are issued by "
            "the state or territory Births, Deaths and Marriages office. The "
            "Philippine Embassy in Canberra can advise on documentation requirements. "
            "Both Australia and the Philippines are Hague Apostille Convention "
            "members. (Philippine Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'philippines',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in the Philippines include business professionals, "
            "retirees, and a community with bilateral ties reflecting the large "
            "Filipino-Canadian diaspora in Canada. Canada has one of the largest "
            "Filipino communities globally. Canadian death certificates (in English "
            "or French) are issued by the relevant provincial civil records "
            "office. The Philippine Embassy in Ottawa can advise on documentation "
            "requirements. Both Canada and the Philippines are Hague Apostille "
            "Convention members. (Philippine Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'philippines',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japanese nationals in the Philippines include business professionals, "
            "retirees, investors, and a Nikkei-Filipino community with historical "
            "ties. Japan is among the Philippines' most significant bilateral "
            "economic partners and provides development assistance through ODA "
            "programmes. Japanese death certificates (shibo todoke, in Japanese) "
            "require certified English translation for the Philippine Statistics "
            "Authority (PSA). The Philippine Embassy in Tokyo handles consular "
            "matters. The Philippines is a Hague Apostille Convention member; "
            "Japan is not a member, so documents require consular authentication "
            "through the Philippine Embassy in Tokyo. "
            "(Philippine Department of Foreign Affairs, 2025.)"
        ),
    },
    # R59 -- Vietnam wave 1
    {
        'origin': 'united-states', 'dest': 'vietnam',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Vietnam include business professionals, students, "
            "tourists, and a growing expat community, reflecting Vietnam-US "
            "diplomatic normalisation since 1995. English-language US death "
            "certificates require certified Vietnamese translation and legalisation "
            "for Vietnamese authorities. The Vietnamese Embassy in Washington DC "
            "can advise on documentation requirements. Vietnam is not a member of "
            "the Hague Apostille Convention; full consular legalisation through "
            "the Vietnamese Embassy is required. "
            "(Vietnamese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'vietnam',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Vietnam include business professionals, "
            "students, and tourists, with a growing expat community. Australia-Vietnam "
            "bilateral trade and investment ties have grown substantially within "
            "ASEAN-Australia frameworks. Australian death certificates (in English) "
            "require certified Vietnamese translation and legalisation by the "
            "Vietnamese Embassy in Canberra. Vietnam is not a member of the Hague "
            "Apostille Convention; full consular legalisation is required. "
            "(Vietnamese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'vietnam',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Vietnam include business professionals, students, "
            "tourists, and a community with historical and cultural ties reflecting "
            "the former French colonial presence. France and Vietnam maintain active "
            "bilateral diplomatic and cultural relations through the Francophonie. "
            "French death certificates (acte de deces, in French) require certified "
            "Vietnamese translation and legalisation by the Vietnamese Embassy in "
            "Paris. Vietnam is not a member of the Hague Apostille Convention; "
            "full consular legalisation is required. "
            "(Vietnamese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'vietnam',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Vietnam include business professionals in "
            "manufacturing and technology sectors, students, and tourists. Germany "
            "is among Vietnam's significant European trading partners, with German "
            "investment in Vietnamese industry. German death certificates "
            "(Sterbeurkunde, in German) require certified Vietnamese translation "
            "and legalisation by the Vietnamese Embassy in Berlin. Vietnam is not "
            "a member of the Hague Apostille Convention; full consular legalisation "
            "is required. (Vietnamese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'vietnam',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in Vietnam include business professionals, tourists, "
            "and a community with bilateral ties through Canada's development "
            "partnerships in Vietnam. Canadian death certificates (in English or "
            "French) require certified Vietnamese translation and legalisation by "
            "the Vietnamese Embassy in Ottawa. Vietnam is not a member of the "
            "Hague Apostille Convention; full consular legalisation is required. "
            "(Vietnamese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R59 -- Bangladesh wave 1
    {
        'origin': 'united-kingdom', 'dest': 'bangladesh',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Bangladesh include dual nationals with close "
            "family ties to the large British-Bangladeshi community, development "
            "workers, and business professionals. The UK and Bangladesh have "
            "significant bilateral people-to-people ties. British death certificates "
            "are issued by the relevant register office in England and Wales, "
            "Scotland, or Northern Ireland. The Bangladeshi High Commission in "
            "London can advise on documentation requirements for repatriation "
            "to Bangladesh. Bangladesh is not a member of the Hague Apostille "
            "Convention; full consular authentication is required. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'bangladesh',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Bangladesh include development workers, NGO "
            "professionals, and business contacts in the garment and textile "
            "supply chain. Bangladesh is a major supplier of garments to European "
            "markets including Italy, creating bilateral commercial ties and a "
            "small professional community of Italian nationals in country. Italian "
            "death certificates (atto di morte, in Italian) require certified "
            "Bengali or English translation and authentication by the Bangladeshi "
            "Embassy in Rome. Bangladesh is not a Hague Apostille Convention "
            "member. (Bangladeshi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'bangladesh',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Bangladesh include development sector workers, "
            "NGO professionals, and business contacts in the garment supply chain. "
            "Germany is among the largest importers of Bangladeshi readymade "
            "garments, creating bilateral commercial ties and a small professional "
            "community. German death certificates (Sterbeurkunde, in German) "
            "require certified Bengali or English translation and authentication "
            "by the Bangladeshi Embassy in Berlin. Bangladesh is not a Hague "
            "Apostille Convention member. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'bangladesh',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in Bangladesh include development workers, "
            "humanitarian professionals, and NGO staff. Sweden maintains "
            "significant development cooperation with Bangladesh through Sida "
            "(Swedish International Development Cooperation Agency), with "
            "Swedish funding across health, climate, and poverty programmes. "
            "Swedish death certificates require certified Bengali or English "
            "translation and authentication by the Bangladeshi Embassy in "
            "Stockholm. Bangladesh is not a Hague Apostille Convention member. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'bangladesh',
        'embassy_city': 'Oslo',
        'intro': (
            "Norwegian nationals in Bangladesh include development and humanitarian "
            "workers and a small professional community. Norway maintains bilateral "
            "development cooperation with Bangladesh, with Norwegian funding across "
            "health and climate resilience programmes. Norwegian death certificates "
            "require certified Bengali or English translation and authentication "
            "by the Bangladeshi Embassy in Oslo. Bangladesh is not a Hague "
            "Apostille Convention member. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R60 -- Thailand wave 1
    {
        'origin': 'united-kingdom', 'dest': 'thailand',
        'embassy_city': 'London',
        'intro': (
            "Thai nationals in the United Kingdom include students, professionals, "
            "and a community including Thai spouses of British nationals, built over "
            "decades of bilateral people-to-people contact. When a Thai national "
            "dies in the UK, the death must be registered with the relevant register "
            "office in England and Wales, Scotland, or Northern Ireland. The Thai "
            "Embassy in London can advise on documentation requirements for "
            "repatriation to Thailand. Thailand is not a member of the Hague "
            "Apostille Convention; full consular legalisation through the Thai "
            "Embassy in London is required. "
            "(Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'thailand',
        'embassy_city': 'Washington DC',
        'intro': (
            "Thai nationals in the United States include students, professionals, "
            "and a community with bilateral ties. When a Thai national dies in the "
            "US, the death must be registered with the state civil records office "
            "where the death occurred. English-language US death certificates require "
            "certified Thai translation for Thai authorities. The Thai Embassy in "
            "Washington DC can advise on documentation requirements. Thailand is "
            "not a member of the Hague Apostille Convention; full consular "
            "legalisation through the Thai Embassy is required. "
            "(Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'thailand',
        'embassy_city': 'Stockholm',
        'intro': (
            "Thai nationals in Sweden include students, professionals, and Thai "
            "spouses of Swedish nationals, a community established over decades "
            "of bilateral people-to-people contact. Sweden has an established "
            "Thai community. Swedish death certificates require certified Thai "
            "translation for Thai authorities. The Thai Embassy in Stockholm "
            "handles consular matters. Thailand is not a Hague Apostille Convention "
            "member; full consular legalisation through the Thai Embassy in "
            "Stockholm is required. (Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'thailand',
        'embassy_city': 'Oslo',
        'intro': (
            "Thai nationals in Norway include individuals with bilateral family "
            "ties, particularly Thai spouses of Norwegian nationals. Norway has "
            "a small but established Thai community. Norwegian death certificates "
            "require certified Thai translation for Thai authorities. The Thai "
            "Embassy in Oslo handles consular matters. Thailand is not a Hague "
            "Apostille Convention member; full consular legalisation through the "
            "Thai Embassy in Oslo is required. "
            "(Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'thailand',
        'embassy_city': 'Paris',
        'intro': (
            "Thai nationals in France include students, professionals, and a small "
            "community with bilateral ties. France and Thailand have maintained "
            "diplomatic relations since 1862, one of the oldest bilateral "
            "relationships in Southeast Asia. French death certificates (acte de "
            "deces, in French) require certified Thai translation for Thai "
            "authorities. The Thai Embassy in Paris handles consular matters. "
            "Thailand is not a Hague Apostille Convention member; full consular "
            "legalisation through the Thai Embassy in Paris is required. "
            "(Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R60 -- China wave 1
    {
        'origin': 'united-states', 'dest': 'china',
        'embassy_city': 'Washington DC',
        'intro': (
            "Chinese nationals in the United States include one of the largest "
            "overseas Chinese communities globally, encompassing students, "
            "professionals, business people, and permanent residents. English-language "
            "US death certificates require certified simplified Chinese translation "
            "and legalisation through the Chinese Embassy in Washington DC. China "
            "is not a member of the Hague Apostille Convention; full consular "
            "legalisation is required for all US-issued documents. "
            "(Chinese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'china',
        'embassy_city': 'Canberra',
        'intro': (
            "Chinese nationals in Australia include one of the largest overseas "
            "Chinese communities globally, encompassing students, business "
            "professionals, and permanent residents. Australian death certificates "
            "(in English) require certified simplified Chinese translation and "
            "legalisation through the Chinese Embassy in Canberra. China is not "
            "a member of the Hague Apostille Convention; full consular legalisation "
            "is required for all Australian-issued documents. "
            "(Chinese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'china',
        'embassy_city': 'Ottawa',
        'intro': (
            "Chinese nationals in Canada include a large overseas Chinese community "
            "encompassing students, business professionals, and permanent residents "
            "with strong bilateral ties. Canadian death certificates (in English or "
            "French) require certified simplified Chinese translation and legalisation "
            "through the Chinese Embassy in Ottawa. China is not a member of the "
            "Hague Apostille Convention; full consular legalisation is required "
            "for all Canadian-issued documents. "
            "(Chinese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'china',
        'embassy_city': 'London',
        'intro': (
            "Chinese nationals in the United Kingdom include students, business "
            "professionals, and a community with bilateral ties, forming one of "
            "the largest overseas Chinese populations in Europe. British death "
            "certificates require certified simplified Chinese translation and "
            "legalisation through the Chinese Embassy in London. China is not a "
            "member of the Hague Apostille Convention; full consular legalisation "
            "is required for all UK-issued documents. "
            "(Chinese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'china',
        'embassy_city': 'Stockholm',
        'intro': (
            "Chinese nationals in Sweden include students, business professionals, "
            "and a small community with bilateral ties through Sweden-China trade "
            "and academic cooperation. Swedish death certificates require certified "
            "simplified Chinese translation and legalisation through the Chinese "
            "Embassy in Stockholm. China is not a member of the Hague Apostille "
            "Convention; full consular legalisation is required for all "
            "Swedish-issued documents. (Chinese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R60 -- Morocco wave 1
    {
        'origin': 'france', 'dest': 'morocco',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Morocco include tourists, business professionals, "
            "and a large community with historical and cultural ties reflecting "
            "France's former protectorate period (1912 to 1956). France is among "
            "Morocco's most significant bilateral partners and there is substantial "
            "movement of French nationals to and from Morocco. French death "
            "certificates (acte de deces, in French) are accepted in Morocco "
            "alongside Arabic translation. Morocco joined the Hague Apostille "
            "Convention in 2021. The Moroccan Embassy in Paris can advise on "
            "current documentation requirements. "
            "(Moroccan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'morocco',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Morocco include tourists, business professionals, "
            "and a significant community reflecting Spain-Morocco geographical "
            "proximity and historical ties. Spain and Morocco share land borders "
            "at Ceuta and Melilla. Spanish death certificates (certificado de "
            "defuncion, in Spanish) require certified Arabic translation for "
            "Moroccan civil registration. Morocco joined the Hague Apostille "
            "Convention in 2021. The Moroccan Embassy in Madrid can advise on "
            "current documentation requirements. "
            "(Moroccan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'morocco',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgian nationals in Morocco include tourists, business professionals, "
            "and a community with bilateral ties through Belgium's large Moroccan "
            "diaspora. Belgium has one of the largest Moroccan communities in "
            "Europe, reflecting decades of migration from the 1960s onward. Belgian "
            "death certificates (in French or Dutch depending on region) require "
            "certified Arabic translation for Moroccan civil registration. Morocco "
            "joined the Hague Apostille Convention in 2021. The Moroccan Embassy "
            "in Brussels can advise on current documentation requirements. "
            "(Moroccan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'morocco',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in Morocco include tourists, business professionals, "
            "and a community with bilateral ties through the Netherlands' large "
            "Moroccan diaspora, one of the largest in Europe. Dutch death "
            "certificates (akte van overlijden, in Dutch) require certified Arabic "
            "translation for Moroccan civil registration. Morocco joined the Hague "
            "Apostille Convention in 2021. The Moroccan Embassy in The Hague can "
            "advise on current documentation requirements. "
            "(Moroccan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'morocco',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Morocco include tourists, business professionals, "
            "and retirees who have settled in cities such as Marrakech. British "
            "death certificates require certified Arabic translation for Moroccan "
            "civil registration. Morocco joined the Hague Apostille Convention in "
            "2021. The Moroccan Embassy in London can advise on current "
            "documentation requirements for repatriation to Morocco. "
            "(Moroccan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R60 -- Jordan wave 1
    {
        'origin': 'united-kingdom', 'dest': 'jordan',
        'embassy_city': 'London',
        'intro': (
            "Jordanian nationals in the United Kingdom include students, "
            "professionals, and a community with bilateral ties. Jordan and the "
            "UK have maintained close diplomatic relations and the Jordanian "
            "community in the UK includes professionals in academia, medicine, "
            "and business. British death certificates require certified Arabic "
            "translation and authentication by the Jordanian Embassy in London "
            "for Jordanian civil registration. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'jordan',
        'embassy_city': 'Washington DC',
        'intro': (
            "Jordanian nationals in the United States include students, "
            "professionals, and a community with bilateral ties reflecting close "
            "US-Jordan strategic relations. English-language US death certificates "
            "require certified Arabic translation and authentication by the "
            "Jordanian Embassy in Washington DC for Jordanian civil registration. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'jordan',
        'embassy_city': 'Ottawa',
        'intro': (
            "Jordanian nationals in Canada include students, professionals, and "
            "a community with bilateral ties. Canada and Jordan maintain bilateral "
            "diplomatic relations. Canadian death certificates (in English or "
            "French) require certified Arabic translation and authentication by "
            "the Jordanian Embassy in Ottawa for Jordanian civil registration. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'jordan',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Jordan include development workers, archaeologists "
            "working at sites such as Petra, business professionals, and a small "
            "expat community. France and Jordan maintain bilateral diplomatic "
            "relations and France provides development assistance to Jordan. French "
            "death certificates (acte de deces, in French) require certified Arabic "
            "translation and authentication by the Jordanian Embassy in Paris. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'jordan',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Jordan include development workers, archaeologists, "
            "and business professionals. Italy and Jordan maintain bilateral "
            "diplomatic relations and Italy has long-standing archaeological "
            "involvement at Jordanian historical sites. Italian death certificates "
            "(atto di morte, in Italian) require certified Arabic translation and "
            "authentication by the Jordanian Embassy in Rome. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R60 -- Sri Lanka wave 1
    {
        'origin': 'united-kingdom', 'dest': 'sri-lanka',
        'embassy_city': 'London',
        'intro': (
            "Sri Lankan nationals in the United Kingdom include a significant "
            "diaspora community, particularly in London. The UK has one of the "
            "largest Sri Lankan communities globally, reflecting decades of "
            "migration. British death certificates require certified translation "
            "and authentication by the Sri Lankan High Commission in London. "
            "Sri Lanka is not a member of the Hague Apostille Convention; full "
            "consular authentication through the Sri Lankan High Commission is "
            "required. (Sri Lankan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'sri-lanka',
        'embassy_city': 'Berlin',
        'intro': (
            "Sri Lankan nationals in Germany include students, professionals, and "
            "a small diaspora community with bilateral ties. German death "
            "certificates (Sterbeurkunde, in German) require certified translation "
            "and authentication by the Sri Lankan Embassy in Berlin. Sri Lanka is "
            "not a member of the Hague Apostille Convention; full consular "
            "authentication through the Sri Lankan Embassy in Berlin is required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'sri-lanka',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sri Lankan nationals in Sweden include a community with bilateral ties "
            "established in part through asylum migration during the civil conflict "
            "period (1983 to 2009) and their families. Swedish death certificates "
            "require certified translation and authentication by the Sri Lankan "
            "Embassy in Stockholm. Sri Lanka is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Sri Lankan "
            "Embassy in Stockholm is required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'sri-lanka',
        'embassy_city': 'Oslo',
        'intro': (
            "Sri Lankan nationals in Norway include a small community with "
            "bilateral ties, including individuals who sought asylum during the "
            "civil conflict period and their families. Norway played a role as a "
            "peace facilitator during the Sri Lankan conflict (2000 to 2006). "
            "Norwegian death certificates require certified translation and "
            "authentication by the Sri Lankan Embassy in Oslo. Sri Lanka is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. (Sri Lankan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'sri-lanka',
        'embassy_city': 'The Hague',
        'intro': (
            "Sri Lankan nationals in the Netherlands include a small community "
            "with bilateral ties. Dutch death certificates (akte van overlijden, "
            "in Dutch) require certified translation and authentication by the "
            "Sri Lankan Embassy in The Hague. Sri Lanka is not a member of the "
            "Hague Apostille Convention; full consular authentication through the "
            "Sri Lankan Embassy in The Hague is required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025.)"
        ),
    },
]


def make_dest_key(dest_slug):
    keys = {
        'egypt': 'eg', 'pakistan': 'pk', 'philippines': 'ph',
        'vietnam': 'vn', 'bangladesh': 'bd', 'thailand': 'th',
        'china': 'cn', 'morocco': 'ma', 'jordan': 'jo', 'sri-lanka': 'lk',
    }
    return keys.get(dest_slug, dest_slug[:2])


def complexity_to_desc(c):
    labels = {
        'low': 'Established process.',
        'moderate': 'Specialist support recommended.',
        'moderate-high': 'Complex route. Specialist required.',
        'high': 'Complex process. A specialist is essential.',
        'very-high': 'A specialist is essential on this complex route.',
    }
    return labels.get(c, 'Specialist support recommended.')


def title_name(name):
    if name.lower().startswith('the '):
        return name[4:]
    return name


def render_route(route, variant):
    origin_slug = route['origin']
    dest_slug = route['dest']
    embassy_city = route['embassy_city']
    intro = route['intro']

    od = ORIGIN_DATA[origin_slug]
    dm = DEST_META[dest_slug]

    origin_name = od['name']
    dest_name = dm['name']
    slug = f"{origin_slug}-to-{dest_slug}"

    complexity = od['complexity']
    timeline_avg = od['timeline_avg']
    timeline_fast = od['timeline_fast']
    timeline_complex = od['timeline_complex']
    doc_time = od['doc_time']
    dest_key = dm['key']
    emergency_line = dm['emergency_line']

    desc_note = complexity_to_desc(complexity)
    t_origin = title_name(origin_name)
    t_dest = title_name(dest_name)
    description = (
        f"Someone has died in {origin_name}. Repatriation to {dest_name} "
        f"takes {timeline_avg}. {desc_note} Contact us 24/7."
    )

    dest_reception = dm['reception']
    dest_consular = dm['consular_template'].format(city=embassy_city)
    arrival_faq = dm['arrival_faq']

    if origin_slug == 'united-kingdom':
        pt3 = (
            f"Contact the {dest_name} Embassy or High Commission in London "
            f"for documentation requirements. They cannot fund repatriation."
        )
        step1_timing = (
            "Day of death. Call 999 for emergency services. "
            f"Contact the {dest_name} Embassy or High Commission in London."
        )
        step3_action = f"{dest_name} Embassy or High Commission in London notified"
    else:
        pt3 = (
            f"British Embassy or High Commission in {embassy_city} registers "
            f"the death and advises. They cannot fund repatriation."
        )
        step1_timing = (
            f"Day of death. Call +44 (0)20 7008 5000 (FCDO) or {od['emergency']} "
            f"for local emergency services."
        )
        step3_action = f"{dest_name} Embassy in {embassy_city} notified"

    pts = [
        f"Key document: {od['cert_name']} (in {od['cert_lang']})",
        f"Documentation takes {doc_time}. Appoint a specialist on day one.",
        pt3,
        f"Death must be registered with {od['registry']} promptly.",
        (
            f"{dest_name} Embassy in {embassy_city} can advise on "
            f"documentation. They cannot fund repatriation."
        ),
    ]

    overview_body = od['overview']
    pts_yaml = "\n".join(f'  - "{p}"' for p in pts)

    step2_action = f"Death registered. {od['cert_name'].capitalize()} obtained."
    step2_timing = (
        f"Death must be registered with {od['registry']}. "
        f"{od['postmortem_trigger']} may delay this step."
    )

    timeline_steps = f"""  - step: 1
    action: "Immediate steps after death"
    timing: "{step1_timing}"
    responsible: "Family or travel insurer"
  - step: 2
    action: "{step2_action}"
    timing: "{step2_timing}"
    responsible: "Local funeral director and registry"
  - step: 3
    action: "{step3_action}"
    timing: "Simultaneous with Step 1. Embassy provides a list of local funeral directors."
    responsible: "Family or repatriation specialist"
  - step: 4
    action: "Embalming and preparation."
    timing: "After body released by authorities."
    responsible: "Licensed local funeral director"
  - step: 5
    action: "All export documentation and permits obtained."
    timing: "Allow {doc_time}. Cannot begin until death certificate issued."
    responsible: "Local funeral director and authorities"
  - step: 6
    action: "Air cargo to {dest_name}"
    timing: "Once all documentation complete."
    responsible: "Repatriation specialist and airline cargo"
  - step: 7
    action: "{dest_name} funeral director takes custody. Receiving funeral director coordinates with local authorities."
    timing: "Within 24 hours of arrival."
    responsible: "Receiving funeral director"
"""

    faqs = f"""  - question: "How long does repatriation from {origin_name} to {dest_name} take?"
    answer: "In a straightforward case, repatriation from {origin_name} to {dest_name} takes {timeline_avg}. The fastest cases complete in {timeline_fast}. Complex cases can take {timeline_complex} or longer."
  - question: "What should I know first about repatriation from {origin_name}?"
    answer: "Death must be registered with {od['registry']} promptly. {od['postmortem_trigger']} may add time before the body can be released."
  - question: "What documents are required for repatriation from {origin_name} to {dest_name}?"
    answer: "The core documents are: {od['cert_name']} with certified translation where required, embalming certificate, export permit, freedom from infection certificate, and passport of the deceased. Your repatriation coordinator handles obtaining these on your behalf."
  - question: "Does the {dest_name} Embassy in {origin_name} help with repatriation?"
    answer: "The {dest_name} Embassy in {embassy_city} can assist with document authentication and advise on repatriation requirements. They cannot pay for or arrange repatriation. Contact the {dest_name} Embassy in {embassy_city} as soon as possible after the death."
  - question: "Is a post-mortem required when someone dies in {origin_name}?"
    answer: "{od['postmortem_trigger']} may trigger a post-mortem examination. This adds time: the body cannot be released until the authorities authorise it."
  - question: "What happens when the body arrives in {dest_name}?"
    answer: "{arrival_faq}"
  - question: "Can I bring ashes home from {origin_name} instead of repatriating the body?"
    answer: "{od['cremation']} You will need the local death certificate, cremation certificate, and relevant export documentation. Your repatriation specialist can advise on the current position."
"""

    if origin_slug == 'united-kingdom':
        sideways = f"""    - url: "/routes/{dest_slug}-to-united-kingdom/"
      text: "Repatriation from {dest_name} to the UK"
    - url: "/routes/united-kingdom-to-ireland/"
      text: "Repatriation from the UK to Ireland"
"""
    else:
        sideways = f"""    - url: "/routes/{origin_slug}-to-united-kingdom/"
      text: "Repatriation from {origin_name} to the UK"
    - url: "/routes/{origin_slug}-to-ireland/"
      text: "Repatriation from {origin_name} to Ireland"
"""

    links = f"""  upward:
    - url: "/repatriation-from-{origin_slug}/"
      text: "Full {origin_name} repatriation guide"
    - url: "/guides/death-abroad-{origin_slug}/"
      text: "What to do if someone dies in {origin_name}"
    - url: "/{dm['hub_url']}/"
      text: "Repatriation to {dest_name}: overview"
    - url: "/contact/"
      text: "Send an enquiry to our team"
  sideways:
{sideways}"""

    content = f"""---
title: "{t_origin} to {t_dest}: Repatriation Guidance"
description: "{description}"
origin_key: "{origin_slug}"
dest_key: "{dest_key}"
origin_name: "{origin_name}"
dest_name: "{dest_name}"
origin_slug: "{origin_slug}"
dest_slug: "{dest_slug}"
slug: "{slug}"
template_variant: "{variant}"
route_complexity: "{complexity}"
timeline_avg: "{timeline_avg}"
timeline_fast: "{timeline_fast}"
timeline_complex: "{timeline_complex}"
embassy_city: "{embassy_city}"
doc_processing_time: "{doc_time}"
date: 2026-05-01
direct_answer_heading: "Repatriation from {origin_name} to {dest_name}: what to expect"
direct_answer_intro: "{intro}"
direct_answer_points:
{pts_yaml}
overview_heading: "What happens after a death in {origin_name}"
overview_body: "{overview_body}"
dest_reception: "{dest_reception}"
dest_consular: "{dest_consular}"
timeline_steps:
{timeline_steps}faqs:
{faqs}links:
{links}---
"""
    return content


def main():
    os.makedirs(ROUTES_DIR, exist_ok=True)
    variant_idx = START_VARIANT
    created = []
    errors = []

    banned = [
        'delve', 'meticulous', 'comprehensive', 'tailored', 'navigate',
        'leverage', 'seamless', 'robust', 'vital', 'crucial', 'utilize',
        'intricate', 'paramount', 'pivotal', 'embark', 'foster', 'elevate',
        'unleash', 'unlock', 'harness', 'streamline', 'holistic', 'realm',
        'testament', 'groundbreaking', 'transformative', 'synergy', 'reimagine',
        'bustling', 'nestled', 'nuanced', 'illuminate', 'encompasses',
        'proactive', 'ubiquitous', 'quintessential', 'moreover', 'furthermore',
    ]

    for route in ROUTES:
        variant = VARIANTS[variant_idx % 5]
        slug = f"{route['origin']}-to-{route['dest']}"
        path = os.path.join(ROUTES_DIR, f"{slug}.md")

        if os.path.exists(path):
            print(f"SKIP (exists): {slug}")
            variant_idx += 1
            continue

        content = render_route(route, variant)

        check = content.replace('---', '').replace('--gc', '')
        if '--' in check or '—' in content:
            msg = f"ERROR em dash in {slug}"
            print(msg)
            errors.append(msg)
            continue

        lower_content = content.lower()
        found_banned = [w for w in banned if w in lower_content]
        if found_banned:
            msg = f"ERROR banned vocab in {slug}: {found_banned}"
            print(msg)
            errors.append(msg)
            continue

        price_patterns = [
            'prices start', 'from \xa3', 'from $', 'cost from',
            'price from', 'prices from',
        ]
        if any(p in lower_content for p in price_patterns):
            msg = f"ERROR price language in {slug}"
            print(msg)
            errors.append(msg)
            continue

        safety_patterns = ['guarantee', '100% safe', 'risk-free', 'risk free']
        if any(p in lower_content for p in safety_patterns):
            msg = f"ERROR safety guarantee language in {slug}"
            print(msg)
            errors.append(msg)
            continue

        with open(path, 'w') as f:
            f.write(content)

        print(f"CREATED ({variant}): {slug}")
        created.append((slug, variant))
        variant_idx += 1

    print(f"\nTotal created: {len(created)}")
    for s, v in created:
        print(f"  [{v}] {s}")
    if errors:
        print(f"\nErrors: {len(errors)}")
        for e in errors:
            print(f"  {e}")
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
