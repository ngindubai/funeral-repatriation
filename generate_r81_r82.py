#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R81-R82.

   R81 (25 routes, START_VARIANT=2=C):
     United States x5:   united-kingdom, ireland, australia, canada, germany
     UAE x5:             united-kingdom, ireland, australia, canada, germany
     Saudi Arabia x5:    united-kingdom, ireland, australia, canada, germany
     India x5:           united-kingdom, ireland, italy, spain, netherlands
     Japan x5:           united-kingdom, ireland, united-states, czech-republic, hungary

   R82 (25 routes, continues from R81):
     Malaysia x5:        united-kingdom, ireland, canada, italy, spain
     Indonesia x5:       united-kingdom, ireland, italy, spain, portugal
     Qatar x5:           united-kingdom, ireland, australia, canada, germany
     South Africa x5:    united-kingdom, ireland, canada, belgium, sweden
     Kuwait x5:          united-kingdom, ireland, australia, canada, germany

   Template rotation: R80 ended on variant B (idx=1). R81 starts at C (idx=2).
   START_VARIANT=2 applies across all 50 routes as one continuous cycle.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 2  # C

DEST_META = {
    'united-states': {
        'name': 'the United States',
        'slug': 'united-states',
        'key': 'us',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The US funeral director takes custody at the cargo terminal at the "
            "receiving city's international airport. Major cargo gateways include "
            "John F Kennedy (JFK), Los Angeles (LAX), Chicago O'Hare (ORD), Dallas "
            "Fort Worth (DFW), and Miami (MIA), depending on the final destination. "
            "Each US state operates its own civil registration system. The death is "
            "registered with the state civil records office in the state where the "
            "remains are received. The medical examiner or coroner "
            "takes jurisdiction for violent, sudden, or unexplained deaths; processes "
            "vary by state and county. The United States joined the Hague Apostille "
            "Convention in 1981; apostille certificates from member states are accepted. "
            "All imported human remains must comply with the US Centers for Disease "
            "Control and Prevention (CDC) importation rules and be accompanied by an "
            "embalming certificate and hermetically sealed coffin. "
            "(US Centers for Disease Control and Prevention, 2025; FCDO Travel "
            "Advice: USA, 2025.)"
        ),
        'consular_template': (
            "The US Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to the United States. The United States "
            "joined the Hague Apostille Convention in 1981. The Embassy cannot pay "
            "for or arrange repatriation. Contact the state civil records office in "
            "the receiving state for civil registration queries. The CDC importation "
            "rules apply to all human remains entering the United States."
        ),
        'arrival_faq': (
            "The US funeral director takes custody at the receiving airport cargo "
            "terminal. The death is registered with the relevant state civil records "
            "office. Foreign death certificates must be apostilled and, where not in "
            "English, accompanied by a certified English translation. The medical "
            "examiner or coroner handles violent or unexplained deaths. The United "
            "States joined the Hague Apostille Convention in 1981. All imported human "
            "remains must comply with CDC importation rules and be accompanied by an "
            "embalming certificate and hermetically sealed coffin."
        ),
        'emergency_line': 'contact the US Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-united-states',
    },
    'united-arab-emirates': {
        'name': 'the United Arab Emirates',
        'slug': 'united-arab-emirates',
        'key': 'ae',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The UAE funeral director takes custody at Dubai International Airport "
            "(DXB) or Abu Dhabi International Airport (AUH) cargo terminal, depending "
            "on the emirate of final destination. Sharjah International Airport (SHJ) "
            "is also used for cargo. Death registration in the UAE is handled by the "
            "relevant emirate health authority: the Dubai Health Authority (DHA) for "
            "Dubai, the Health Authority Abu Dhabi (HAAD) for Abu Dhabi, and equivalent "
            "authorities in other emirates. The death certificate is issued by the "
            "relevant emirate health authority. Police are involved in all deaths in "
            "the UAE as part of the death registration process. The UAE is not a member "
            "of the Hague Apostille Convention. All foreign documents for use in the "
            "UAE must be attested by the UAE Embassy in the country of origin and then "
            "by the UAE Ministry of Foreign Affairs (MoFA) in Abu Dhabi. "
            "(UAE Ministry of Health and Prevention, 2025; FCDO Travel Advice: UAE, 2025.)"
        ),
        'consular_template': (
            "The UAE Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to the UAE. The UAE is not a Hague Apostille "
            "Convention member; foreign documents must be attested by the UAE Embassy "
            "in {city} and then by UAE Ministry of Foreign Affairs in Abu Dhabi. "
            "The Embassy cannot pay for or arrange repatriation. Contact the relevant "
            "emirate health authority for civil registration queries."
        ),
        'arrival_faq': (
            "The UAE funeral director takes custody at Dubai (DXB) or Abu Dhabi (AUH) "
            "cargo terminal. Death registration is handled by the relevant emirate "
            "health authority (DHA for Dubai, HAAD for Abu Dhabi). The UAE is not a "
            "Hague Apostille Convention member; all foreign documents must be attested "
            "by the UAE Embassy in the origin country and then by the UAE Ministry of "
            "Foreign Affairs in Abu Dhabi. Police are involved in all UAE deaths. An "
            "embalming certificate and hermetically sealed coffin are required for "
            "all air imports."
        ),
        'emergency_line': 'contact the UAE Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-united-arab-emirates',
    },
    'saudi-arabia': {
        'name': 'Saudi Arabia',
        'slug': 'saudi-arabia',
        'key': 'sa',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Saudi funeral director takes custody at King Abdulaziz International "
            "Airport Jeddah (JED), King Khalid International Airport Riyadh (RUH), or "
            "King Fahd International Airport Dammam (DMM) cargo terminal, depending on "
            "the final destination. Death registration in Saudi Arabia is handled by the "
            "General Directorate of Civil Affairs (GDCA) under the Ministry of Interior. "
            "The death certificate is issued by the relevant civil affairs authority. "
            "The Public Prosecution (Al-Niyaba Al-Ammah) takes jurisdiction for violent "
            "or unexplained deaths and must authorise release before repatriation can "
            "proceed. Saudi Arabia is not a member of the Hague Apostille Convention. "
            "All foreign documents for use in Saudi Arabia must be attested by the Saudi "
            "Embassy in the country of origin and then by the Saudi Ministry of Foreign "
            "Affairs in Riyadh. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. "
            "(Saudi Arabia Ministry of Interior / GDCA, 2025; FCDO Travel Advice: "
            "Saudi Arabia, 2025.)"
        ),
        'consular_template': (
            "The Saudi Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Saudi Arabia. Saudi Arabia is not a Hague "
            "Apostille Convention member; foreign documents must be attested by the "
            "Saudi Embassy in {city} and then by the Saudi Ministry of Foreign Affairs "
            "in Riyadh. The Embassy cannot pay for or arrange repatriation. Contact the "
            "General Directorate of Civil Affairs (GDCA) for civil registration queries."
        ),
        'arrival_faq': (
            "The Saudi funeral director takes custody at Jeddah (JED), Riyadh (RUH), "
            "or Dammam (DMM) cargo terminal. The General Directorate of Civil Affairs "
            "(GDCA) under the Ministry of Interior handles death registration. Saudi "
            "Arabia is not a Hague Apostille Convention member; all foreign documents "
            "must be attested by the Saudi Embassy in the origin country and then by "
            "the Saudi Ministry of Foreign Affairs in Riyadh. The Public Prosecution "
            "handles violent or unexplained deaths. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Saudi Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-saudi-arabia',
    },
    'india': {
        'name': 'India',
        'slug': 'india',
        'key': 'in',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Indian funeral director takes custody at the cargo terminal of the "
            "receiving airport. Major international cargo gateways include Indira Gandhi "
            "International Airport Delhi (DEL), Chhatrapati Shivaji Maharaj International "
            "Airport Mumbai (BOM), Kempegowda International Airport Bangalore (BLR), "
            "Chennai International Airport (MAA), Netaji Subhas Chandra Bose International "
            "Airport Kolkata (CCU), and Rajiv Gandhi International Airport Hyderabad (HYD). "
            "Death registration in India is handled by the state civil registrar under "
            "the Registration of Births and Deaths Act 1969. The death certificate is "
            "issued by the municipal corporation or local body. Police and the judicial "
            "magistrate take jurisdiction for violent or unexplained deaths. India joined "
            "the Hague Apostille Convention in 2005; apostille certificates from member "
            "states are accepted. Foreign death certificates must be apostilled and, "
            "where not in English, accompanied by a certified translation. An embalming "
            "certificate and hermetically sealed coffin are required for all air imports. "
            "(Registrar General of India, Ministry of Home Affairs, India, 2025; FCDO "
            "Travel Advice: India, 2025.)"
        ),
        'consular_template': (
            "The Indian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to India. India joined the "
            "Hague Apostille Convention in 2005. The High Commission cannot pay for "
            "or arrange repatriation. Contact the state civil registrar in the "
            "receiving state for civil registration queries."
        ),
        'arrival_faq': (
            "The Indian funeral director takes custody at the cargo terminal of the "
            "receiving international airport (Delhi, Mumbai, Bangalore, Chennai, Kolkata, "
            "or Hyderabad depending on the final destination). The state civil registrar "
            "handles death registration under the Registration of Births and Deaths Act "
            "1969. Police and judicial magistrate handle violent or unexplained deaths. "
            "India joined the Hague Apostille Convention in 2005; foreign documents must "
            "be apostilled and, where not in English, accompanied by a certified "
            "translation. An embalming certificate and hermetically sealed coffin are "
            "required for all air imports."
        ),
        'emergency_line': 'contact the Indian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-india',
    },
    'japan': {
        'name': 'Japan',
        'slug': 'japan',
        'key': 'jp',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Japanese funeral director takes custody at the cargo terminal of the "
            "receiving airport. Major international cargo gateways include Narita "
            "International Airport (NRT), Tokyo Haneda (HND), Kansai International "
            "Airport Osaka (KIX), Chubu Centrair International Airport Nagoya (NGO), "
            "and Fukuoka Airport (FUK). Death registration in Japan is handled by the "
            "local municipal office (shiyakusho or kuyakusho) where the death occurred "
            "or where the deceased was registered. The shibo todoke (death notification) "
            "must be filed within seven days of death under the Family Register Act. "
            "Police take jurisdiction for violent or unexplained deaths and must complete "
            "their investigation before the body is released. Japan joined the Hague "
            "Apostille Convention in 1970; apostille certificates from member states are "
            "accepted. Foreign death certificates must be apostilled and accompanied by "
            "a certified Japanese translation for the municipal office. An embalming "
            "certificate and hermetically sealed coffin are required for all air imports. "
            "(Japan Ministry of Justice, 2025; Japan Ministry of Health, Labour and "
            "Welfare, 2025; FCDO Travel Advice: Japan, 2025.)"
        ),
        'consular_template': (
            "The Embassy of Japan in {city} can advise on documentation requirements "
            "for repatriation to Japan. Japan joined the Hague Apostille Convention "
            "in 1970. The Embassy cannot pay for or arrange repatriation. Contact "
            "the local municipal office (shiyakusho or kuyakusho) in the receiving "
            "area for civil registration queries."
        ),
        'arrival_faq': (
            "The Japanese funeral director takes custody at Narita (NRT), Haneda (HND), "
            "Kansai (KIX), Nagoya (NGO), Fukuoka (FUK), or another cargo terminal "
            "depending on the final destination. The local municipal office (shiyakusho "
            "or kuyakusho) handles death registration; the shibo todoke must be filed "
            "within seven days under the Family Register Act. Police handle violent or "
            "unexplained deaths. Japan joined the Hague Apostille Convention in 1970; "
            "foreign documents must be apostilled and accompanied by a certified "
            "Japanese translation. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Japanese Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-japan',
    },
    'malaysia': {
        'name': 'Malaysia',
        'slug': 'malaysia',
        'key': 'my',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Malaysian funeral director takes custody at Kuala Lumpur International "
            "Airport (KUL) cargo terminal, or at Penang International Airport (PEN) or "
            "Kota Kinabalu International Airport (BKI) depending on the final destination. "
            "Death registration in Malaysia is handled by the National Registration "
            "Department (Jabatan Pendaftaran Negara, JPN). The death certificate is "
            "issued in Bahasa Malaysia. Police and the forensic pathologist take "
            "jurisdiction for violent or unexplained deaths. Malaysia is not a member "
            "of the Hague Apostille Convention. All foreign documents for use in "
            "Malaysia must be attested by the Malaysian Embassy or High Commission in "
            "the country of origin and then by the Malaysian Ministry of Foreign Affairs "
            "(Wisma Putra) in Kuala Lumpur. Foreign death certificates must be "
            "accompanied by a certified Bahasa Malaysia translation where required. "
            "An embalming certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(National Registration Department (JPN), Malaysia, 2025; FCDO Travel "
            "Advice: Malaysia, 2025.)"
        ),
        'consular_template': (
            "The Malaysian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Malaysia. Malaysia is not "
            "a Hague Apostille Convention member; foreign documents must be attested "
            "by the Malaysian High Commission or Embassy in {city} and then by the "
            "Malaysian Ministry of Foreign Affairs (Wisma Putra) in Kuala Lumpur. "
            "The High Commission cannot pay for or arrange repatriation. Contact "
            "the National Registration Department (JPN) for civil registration queries."
        ),
        'arrival_faq': (
            "The Malaysian funeral director takes custody at Kuala Lumpur (KUL), "
            "Penang (PEN), Kota Kinabalu (BKI), or another cargo terminal depending "
            "on the final destination. The National Registration Department (JPN) "
            "handles death registration. Malaysia is not a Hague Apostille Convention "
            "member; all foreign documents must be attested by the Malaysian High "
            "Commission or Embassy in the origin country and then by the Malaysian "
            "Ministry of Foreign Affairs (Wisma Putra) in Kuala Lumpur. A certified "
            "Bahasa Malaysia translation may be required. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Malaysian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-malaysia',
    },
    'indonesia': {
        'name': 'Indonesia',
        'slug': 'indonesia',
        'key': 'id',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Indonesian funeral director takes custody at Soekarno-Hatta "
            "International Airport Jakarta (CGK), Ngurah Rai International Airport "
            "Bali (DPS), or Juanda International Airport Surabaya (SUB) cargo "
            "terminal, depending on the final destination. Death registration in "
            "Indonesia is handled by the Dinas Kependudukan dan Pencatatan Sipil "
            "(Disdukcapil, the civil registration service) in the relevant regency "
            "or city. The death certificate (akta kematian) is issued in Indonesian. "
            "Police take jurisdiction for violent or unexplained deaths. Indonesia "
            "is not a member of the Hague Apostille Convention. All foreign documents "
            "for use in Indonesia must be attested by the Indonesian Embassy or "
            "Consulate in the country of origin and then by the Indonesian Ministry "
            "of Foreign Affairs (Kementerian Luar Negeri) in Jakarta. A certified "
            "Indonesian translation is required for all non-Indonesian documentation. "
            "An embalming certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Disdukcapil / Directorate General of Population and Civil Registration, "
            "Indonesia, 2025; FCDO Travel Advice: Indonesia, 2025.)"
        ),
        'consular_template': (
            "The Indonesian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Indonesia. Indonesia "
            "is not a Hague Apostille Convention member; foreign documents must "
            "be attested by the Indonesian Embassy in {city} and then by the "
            "Indonesian Ministry of Foreign Affairs (Kementerian Luar Negeri) "
            "in Jakarta. A certified Indonesian translation is required. The "
            "Embassy cannot pay for or arrange repatriation. Contact the local "
            "Disdukcapil for civil registration queries."
        ),
        'arrival_faq': (
            "The Indonesian funeral director takes custody at Jakarta (CGK), "
            "Bali (DPS), Surabaya (SUB), or another cargo terminal depending on "
            "the final destination. The Disdukcapil (civil registration service) "
            "handles civil registration. Indonesia is not a Hague Apostille "
            "Convention member; all foreign documents must be attested by the "
            "Indonesian Embassy in the origin country and then by the Ministry "
            "of Foreign Affairs in Jakarta. A certified Indonesian translation is "
            "required for all non-Indonesian documentation. Police handle violent "
            "or unexplained deaths. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Indonesian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-indonesia',
    },
    'qatar': {
        'name': 'Qatar',
        'slug': 'qatar',
        'key': 'qa',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Qatari funeral director takes custody at Hamad International Airport "
            "Doha (DOH) cargo terminal. Death registration in Qatar is handled by the "
            "Civil Affairs Section of the Ministry of Interior. A death certificate is "
            "issued after medical and police clearance. The police and forensic medicine "
            "department take jurisdiction for violent or unexplained deaths and must "
            "complete their process before the body is released. Qatar is not a member "
            "of the Hague Apostille Convention. All foreign documents for use in Qatar "
            "must follow the Qatari attestation process through the Qatari Embassy in "
            "the country of origin and then through the Qatari Ministry of Foreign "
            "Affairs. An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Qatar Ministry of Interior Civil Affairs, 2025; FCDO Travel Advice: "
            "Qatar, 2025.)"
        ),
        'consular_template': (
            "The Qatari Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Qatar. Qatar is not a Hague Apostille "
            "Convention member; foreign documents must follow the Qatari attestation "
            "process through the Qatari Embassy in {city} and then through the Qatari "
            "Ministry of Foreign Affairs. The Embassy cannot pay for or arrange "
            "repatriation. Contact the Civil Affairs Section of the Ministry of "
            "Interior for civil registration queries."
        ),
        'arrival_faq': (
            "The Qatari funeral director takes custody at Hamad International Airport "
            "(DOH) cargo terminal. The Civil Affairs Section of the Ministry of "
            "Interior handles death registration. Qatar is not a Hague Apostille "
            "Convention member; all foreign documents must follow the Qatari "
            "attestation process through the Qatari Embassy in the origin country "
            "and then through the Ministry of Foreign Affairs. Police and forensic "
            "medicine handle violent or unexplained deaths. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Qatari Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-qatar',
    },
    'south-africa': {
        'name': 'South Africa',
        'slug': 'south-africa',
        'key': 'za',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The South African funeral director takes custody at OR Tambo International "
            "Airport Johannesburg (JNB), Cape Town International Airport (CPT), or King "
            "Shaka International Airport Durban (DUR) cargo terminal, depending on the "
            "final destination. Death registration in South Africa is handled by the "
            "Department of Home Affairs (DHA) under the Births and Deaths Registration "
            "Act 51 of 1992. The death certificate is issued in English. The South "
            "African Police Service (SAPS) takes jurisdiction for violent or unexplained "
            "deaths and must complete their investigation before the body is released. "
            "South Africa joined the Hague Apostille Convention in 1995; apostille "
            "certificates from member states are accepted. Foreign death certificates "
            "must be apostilled and, where not in English, accompanied by a certified "
            "English translation for the DHA. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(South African Department of Home Affairs, 2025; FCDO Travel Advice: "
            "South Africa, 2025.)"
        ),
        'consular_template': (
            "The South African High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to South Africa. South Africa "
            "joined the Hague Apostille Convention in 1995. The High Commission cannot "
            "pay for or arrange repatriation. Contact the Department of Home Affairs "
            "(DHA) for civil registration queries."
        ),
        'arrival_faq': (
            "The South African funeral director takes custody at OR Tambo (JNB), "
            "Cape Town (CPT), or King Shaka (DUR) cargo terminal. The Department of "
            "Home Affairs (DHA) handles death registration under the Births and Deaths "
            "Registration Act 51 of 1992. South Africa joined the Hague Apostille "
            "Convention in 1995; foreign documents must be apostilled and, where not "
            "in English, accompanied by a certified English translation. The South "
            "African Police Service (SAPS) handles violent or unexplained deaths. "
            "An embalming certificate and hermetically sealed coffin are required "
            "for all air imports."
        ),
        'emergency_line': 'contact the South African High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-south-africa',
    },
    'kuwait': {
        'name': 'Kuwait',
        'slug': 'kuwait',
        'key': 'kw',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Kuwaiti funeral director takes custody at Kuwait International "
            "Airport (KWI) cargo terminal. Death registration in Kuwait is handled "
            "by the Civil Affairs Division of the Ministry of Interior. The death "
            "certificate is issued in Arabic. Police and the Ministry of Health "
            "forensic department take jurisdiction for violent or unexplained deaths "
            "and must complete their process before the body can be released. Kuwait "
            "is not a member of the Hague Apostille Convention. All foreign documents "
            "for use in Kuwait must be attested by the Kuwaiti Embassy or Consulate "
            "in the country of origin and then by the Kuwaiti Ministry of Foreign "
            "Affairs. A certified Arabic translation is required for all "
            "non-Arabic documentation. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Kuwait Ministry of Interior Civil Affairs, 2025; FCDO Travel Advice: "
            "Kuwait, 2025.)"
        ),
        'consular_template': (
            "The Kuwaiti Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Kuwait. Kuwait is not a Hague Apostille "
            "Convention member; foreign documents must be attested by the Kuwaiti "
            "Embassy in {city} and then by the Kuwaiti Ministry of Foreign Affairs. "
            "A certified Arabic translation is required. The Embassy cannot pay for "
            "or arrange repatriation. Contact the Civil Affairs Division of the "
            "Ministry of Interior for civil registration queries."
        ),
        'arrival_faq': (
            "The Kuwaiti funeral director takes custody at Kuwait International "
            "Airport (KWI) cargo terminal. The Civil Affairs Division of the Ministry "
            "of Interior handles death registration. Kuwait is not a Hague Apostille "
            "Convention member; all foreign documents must be attested by the Kuwaiti "
            "Embassy in the origin country and then by the Kuwaiti Ministry of Foreign "
            "Affairs. A certified Arabic translation is required. Police and forensic "
            "medicine handle violent or unexplained deaths. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Kuwaiti Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-kuwait',
    },
}

ORIGIN_DATA = {
    'united-kingdom': {
        'name': 'the United Kingdom',
        'emergency': '999',
        'registry': 'the local register office (or National Records of Scotland / GRONI)',
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
    'ireland': {
        'name': 'Ireland',
        'emergency': '999 or 112',
        'registry': 'the local civil registration service (General Register Office)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 999 or 112 for emergency services. Death is certified by a "
            "physician or, where necessary, the coroner. The death must be "
            "registered with the local civil registration service. The coroner "
            "takes jurisdiction for sudden, violent, or unexplained deaths and "
            "must issue a burial or cremation order before the body can be "
            "released. Ireland is a Hague Apostille Convention member. In "
            "complex cases, the coroner's investigation can take several weeks "
            "before the body is released."
        ),
        'doc_time': '3-7 days (coroner cases longer)',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '6-10 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Ireland is available at a number of approved "
            "locations, including facilities in Dublin and other cities."
        ),
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
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
            "straightforward; the coroner's release is the main cause of delay "
            "in complex cases."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Australia is widely available in all states and territories.",
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
    'canada': {
        'name': 'Canada',
        'emergency': '911',
        'registry': 'the provincial civil registration authority',
        'cert_name': 'death certificate',
        'cert_lang': 'English or French',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician "
            "or medical examiner. The death is registered with the provincial "
            "civil registration authority. The coroner or medical examiner takes "
            "jurisdiction for sudden, violent, or unexplained deaths. Canada "
            "joined the Hague Apostille Convention; it entered into force in "
            "November 2024."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Canada is widely available in all provinces.",
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner or medical examiner)',
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
            "The United States is a Hague Apostille Convention member. The relevant "
            "Embassy or Consulate of the destination country can assist with "
            "documentation requirements."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in the United States is widely available in all states.",
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths (medical examiner or coroner, varies by state)',
    },
    'italy': {
        'name': 'Italy',
        'emergency': '112 (EU emergency) or 118 (ambulance) or 113 (police)',
        'registry': 'the comune (civil registry office)',
        'cert_name': 'atto di morte (death certificate)',
        'cert_lang': 'Italian',
        'overview': (
            "Call 112 for the EU emergency number, 118 for ambulance, or 113 for "
            "police. Death is certified by a physician. The atto di morte is "
            "registered with the local comune (civil registry office). The Procura "
            "della Repubblica (public prosecutor) takes jurisdiction for violent "
            "or unexplained deaths. Italy is an EU member and Hague Apostille "
            "Convention member (joined 1978)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Italy is available at approved facilities in major cities.",
        'postmortem_trigger': 'Violent or unexplained deaths (Procura della Repubblica)',
    },
    'spain': {
        'name': 'Spain',
        'emergency': '112',
        'registry': 'the Registro Civil (civil registry)',
        'cert_name': 'certificado de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The certificado de defuncion is registered with the local Registro "
            "Civil (civil registry). The Juzgado de Instruccion (investigating "
            "magistrate) and Medico Forense (forensic physician) take jurisdiction "
            "for violent or unexplained deaths. Spain is an EU member and Hague "
            "Apostille Convention member (joined 1978)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Spain is available at approved facilities across the country.",
        'postmortem_trigger': 'Violent or unexplained deaths (Juzgado de Instruccion and Medico Forense)',
    },
    'netherlands': {
        'name': 'the Netherlands',
        'emergency': '112',
        'registry': 'the gemeente (municipal civil registry)',
        'cert_name': 'akte van overlijden (death certificate)',
        'cert_lang': 'Dutch',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The akte van overlijden is registered with the local gemeente "
            "(municipal civil registry office). The officier van justitie "
            "(public prosecutor) takes jurisdiction for violent or unexplained "
            "deaths. The Netherlands is an EU member and Hague Apostille "
            "Convention member (joined 1960)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in the Netherlands is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (officier van justitie)',
    },
    'portugal': {
        'name': 'Portugal',
        'emergency': '112',
        'registry': 'the Conservatoria do Registo Civil (civil registry office)',
        'cert_name': 'assento de obito (death certificate)',
        'cert_lang': 'Portuguese',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The assento de obito is registered with the local Conservatoria do "
            "Registo Civil (civil registry office). The Ministerio Publico "
            "(public prosecutor) takes jurisdiction for violent or unexplained "
            "deaths. Portugal is an EU member and Hague Apostille Convention "
            "member (joined 1970)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Portugal is available at approved facilities.",
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico)',
    },
    'czech-republic': {
        'name': 'the Czech Republic',
        'emergency': '112 or 158 (police)',
        'registry': 'the matrika (civil registry office) in the relevant municipality',
        'cert_name': 'umrtni list (death certificate)',
        'cert_lang': 'Czech',
        'overview': (
            "Call 112 for the EU emergency number or 158 for police. Death is "
            "certified by a physician. The umrtni list is registered with the "
            "local matrika (civil registry office). The police and Prokuratura "
            "(state prosecutor) take jurisdiction for violent or unexplained "
            "deaths. The Czech Republic is an EU member and Hague Apostille "
            "Convention member (joined 1998)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in the Czech Republic is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (police and Prokuratura)',
    },
    'hungary': {
        'name': 'Hungary',
        'emergency': '112 or 107 (police) or 104 (ambulance)',
        'registry': 'the anyakonyvi hivatal (civil registry office)',
        'cert_name': 'halotti anyakonyvi kivonat (death certificate)',
        'cert_lang': 'Hungarian',
        'overview': (
            "Call 112 for the EU emergency number, 107 for police, or 104 for "
            "ambulance. Death is certified by a physician. The halotti anyakonyvi "
            "kivonat is registered with the local anyakonyvi hivatal (civil registry "
            "office). The rendorseg (police) take jurisdiction for violent or "
            "unexplained deaths. Hungary is an EU member and Hague Apostille "
            "Convention member (joined 1973)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Hungary is available at approved facilities.",
        'postmortem_trigger': 'Violent or unexplained deaths (rendorseg / police)',
    },
    'belgium': {
        'name': 'Belgium',
        'emergency': '112 (ambulance/fire) or 101 (police)',
        'registry': 'the local commune or gemeenten civil registry (etat civil / burgerlijke stand)',
        'cert_name': 'acte de deces / overlijdensakte (death certificate)',
        'cert_lang': 'French or Dutch',
        'overview': (
            "Call 112 for ambulance or fire, or 101 for police. Death is certified "
            "by a physician. The acte de deces (in French regions) or overlijdensakte "
            "(in Dutch-speaking regions) is registered with the local commune or "
            "gemeenten civil registry. The parquet (public prosecutor) takes "
            "jurisdiction for violent or unexplained deaths. Belgium is an EU member "
            "and Hague Apostille Convention member (joined 1975)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Belgium is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (parquet / public prosecutor)',
    },
    'sweden': {
        'name': 'Sweden',
        'emergency': '112',
        'registry': 'the Swedish Tax Agency (Skatteverket) Population Register',
        'cert_name': 'dodsfallsintyg (death certificate)',
        'cert_lang': 'Swedish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The dodsfallsintyg is registered with the Swedish Tax Agency "
            "(Skatteverket) in the Population Register. The police and medical "
            "examiner take jurisdiction for violent or unexplained deaths. Sweden "
            "is an EU member and Hague Apostille Convention member (joined 1999)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Sweden is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (police and medical examiner)',
    },
}

ROUTES = [
    # R81 -- United States x5
    {
        'origin': 'united-kingdom', 'dest': 'united-states',
        'embassy_city': 'London',
        'intro': (
            "The United States is one of the most popular destinations for British "
            "nationals, with millions of UK citizens visiting each year for tourism, "
            "business, education, and to visit family. A substantial British expat "
            "community lives across the United States, concentrated in New York, "
            "California, Texas, and Florida. The US Embassy in London is fully "
            "operational. When someone from the United Kingdom dies in the United "
            "States and their family wishes to repatriate remains home, the death is "
            "registered with the state civil records office in the state where the "
            "death occurred. The UK death certificate is apostilled; both the United "
            "Kingdom and the United States are Hague Apostille Convention members. "
            "The US Embassy in London can advise on documentation requirements. "
            "(FCDO Travel Advice: USA, 2025; US Department of State, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'united-states',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and the United States share one of the world's strongest "
            "bilateral bonds, rooted in the Irish diaspora of the 19th and 20th "
            "centuries. More than 30 million Americans claim Irish heritage, and "
            "Irish nationals continue to emigrate to and work across the United "
            "States. The US Embassy in Dublin is fully operational. When someone "
            "from Ireland dies in the United States and their family wishes to "
            "repatriate remains home, the death is registered with the state civil "
            "records office where the death occurred. Both Ireland and the United "
            "States are Hague Apostille Convention members. The US Embassy in "
            "Dublin can advise on documentation requirements for repatriation. "
            "(FCDO Travel Advice: USA, 2025; US Department of State, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'united-states',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and the United States maintain close bilateral ties as "
            "longstanding allies, with a substantial movement of nationals "
            "between the two countries for tourism, work, and education. Australian "
            "nationals travel widely across the United States, and an Australian "
            "expat community is established in cities including Los Angeles, New "
            "York, and San Francisco. The US Embassy in Canberra is fully "
            "operational. When an Australian national dies in the United States "
            "and their family wishes to repatriate remains to Australia, the death "
            "is registered with the state civil records office. Both Australia and "
            "the United States are Hague Apostille Convention members. "
            "(FCDO Travel Advice: USA, 2025; US Department of State, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'united-states',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada and the United States share the world's longest land border "
            "and one of the most interconnected bilateral relationships in the "
            "world. Canadian nationals cross into the United States regularly for "
            "tourism, business, medical care, and to visit family; cross-border "
            "families are extremely common. The US Embassy in Ottawa is fully "
            "operational. When a Canadian national dies in the United States and "
            "their family wishes to repatriate remains to Canada, the death is "
            "registered with the state civil records office. Canada joined the "
            "Hague Apostille Convention (in force November 2024); the United "
            "States joined in 1981. "
            "(FCDO Travel Advice: USA, 2025; US Department of State, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'united-states',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and the United States maintain close bilateral ties as NATO "
            "allies and major trade partners. A large German-American heritage "
            "community exists across the United States, and German nationals "
            "regularly travel to or work in the US in manufacturing, automotive, "
            "finance, and technology sectors. The US Embassy in Berlin is fully "
            "operational. When a German national dies in the United States and "
            "their family wishes to repatriate remains to Germany, the death is "
            "registered with the state civil records office. Both Germany and the "
            "United States are Hague Apostille Convention members. "
            "(FCDO Travel Advice: USA, 2025; US Department of State, 2025.)"
        ),
    },
    # R81 -- United Arab Emirates x5
    {
        'origin': 'united-kingdom', 'dest': 'united-arab-emirates',
        'embassy_city': 'London',
        'intro': (
            "The United Arab Emirates is home to one of the largest British expat "
            "communities outside Europe, concentrated in Dubai and Abu Dhabi across "
            "finance, oil and gas, property, hospitality, and professional services. "
            "The British Embassy in Abu Dhabi and the British Consulate-General in "
            "Dubai are fully operational. When someone from the United Kingdom dies "
            "in the UAE and their family wishes to repatriate remains, the death is "
            "registered with the relevant emirate health authority. The UAE is not a "
            "member of the Hague Apostille Convention; UK documents must be attested "
            "by the UAE Embassy in London and then by UAE Ministry of Foreign Affairs. "
            "Appoint a specialist on the day of death. "
            "(FCDO Travel Advice: UAE, 2025; UAE Ministry of Health and Prevention, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'united-arab-emirates',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals work across the UAE in aviation, finance, technology, "
            "and professional services, with Dublin-Dubai a busy bilateral air route. "
            "Ireland maintains an Embassy in Abu Dhabi. When an Irish national dies "
            "in the UAE and their family wishes to repatriate remains to Ireland, "
            "the death is registered with the relevant emirate health authority. "
            "The UAE is not a member of the Hague Apostille Convention; Irish "
            "documents for use in the UAE must be attested by the UAE Embassy in "
            "Dublin and then by the UAE Ministry of Foreign Affairs. Appoint a "
            "specialist immediately. "
            "(FCDO Travel Advice: UAE, 2025; UAE Ministry of Health and Prevention, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'united-arab-emirates',
        'embassy_city': 'Canberra',
        'intro': (
            "The UAE is a significant bilateral partner for Australia, with Dubai "
            "serving as a major transit hub for Australian travellers and a "
            "destination for Australian expats in finance, mining, and property. "
            "The Australian Embassy in Abu Dhabi is fully operational. When an "
            "Australian national dies in the UAE and their family wishes to "
            "repatriate remains to Australia, the death is registered with the "
            "relevant emirate health authority. The UAE is not a member of the "
            "Hague Apostille Convention; Australian documents must be attested "
            "by the UAE Embassy in Canberra and then by the UAE Ministry of "
            "Foreign Affairs. "
            "(FCDO Travel Advice: UAE, 2025; UAE Ministry of Health and Prevention, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'united-arab-emirates',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals work across the UAE in oil and gas, engineering, "
            "finance, and professional services, and Dubai is a regular transit "
            "point for Canadian travellers. The Canadian Embassy in Abu Dhabi "
            "is fully operational. When a Canadian national dies in the UAE and "
            "their family wishes to repatriate remains to Canada, the death is "
            "registered with the relevant emirate health authority. The UAE is "
            "not a member of the Hague Apostille Convention; Canadian documents "
            "must be attested by the UAE Embassy in Ottawa and then by the UAE "
            "Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: UAE, 2025; UAE Ministry of Health and Prevention, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'united-arab-emirates',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and the UAE maintain strong bilateral trade ties, with German "
            "nationals working in engineering, construction, and manufacturing "
            "sectors across Dubai and Abu Dhabi. Germany maintains an Embassy "
            "in Abu Dhabi. When a German national dies in the UAE and their "
            "family wishes to repatriate remains to Germany, the death is "
            "registered with the relevant emirate health authority. The UAE is "
            "not a member of the Hague Apostille Convention; German documents "
            "must be attested by the UAE Embassy in Berlin and then by the UAE "
            "Ministry of Foreign Affairs. The Sterbeurkunde requires certified "
            "translation for UAE authorities. "
            "(FCDO Travel Advice: UAE, 2025; UAE Ministry of Health and Prevention, 2025.)"
        ),
    },
    # R81 -- Saudi Arabia x5
    {
        'origin': 'united-kingdom', 'dest': 'saudi-arabia',
        'embassy_city': 'London',
        'intro': (
            "Saudi Arabia has long hosted one of the most established British "
            "expat communities in the Gulf, working across oil and gas, defence, "
            "engineering, healthcare, and education. The British Embassy in Riyadh "
            "and British Consulate-General in Jeddah are fully operational. When "
            "someone from the United Kingdom dies in Saudi Arabia and their family "
            "wishes to repatriate remains, the death is registered with the General "
            "Directorate of Civil Affairs under the Ministry of Interior. Saudi "
            "Arabia is not a Hague Apostille Convention member; all documents must "
            "be attested by the Saudi Embassy in London and then by the Saudi "
            "Ministry of Foreign Affairs. Appoint a specialist on the day of death. "
            "(FCDO Travel Advice: Saudi Arabia, 2025; Saudi Ministry of Interior, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'saudi-arabia',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals work in Saudi Arabia in healthcare, construction, "
            "engineering, and professional services. Ireland maintains an Embassy "
            "in Riyadh. When an Irish national dies in Saudi Arabia and their "
            "family wishes to repatriate remains to Ireland, the death is "
            "registered with the General Directorate of Civil Affairs under "
            "the Ministry of Interior. Saudi Arabia is not a Hague Apostille "
            "Convention member; Irish documents must be attested by the Saudi "
            "Embassy in Dublin and then by the Saudi Ministry of Foreign "
            "Affairs in Riyadh. Engage a specialist immediately. "
            "(FCDO Travel Advice: Saudi Arabia, 2025; Saudi Ministry of Interior, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'saudi-arabia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals work in Saudi Arabia in oil and gas, mining, "
            "engineering, and project management. Australia maintains an Embassy "
            "in Riyadh. When an Australian national dies in Saudi Arabia and "
            "their family wishes to repatriate remains to Australia, the death "
            "is registered with the General Directorate of Civil Affairs under "
            "the Ministry of Interior. Saudi Arabia is not a Hague Apostille "
            "Convention member; Australian documents must be attested by the "
            "Saudi Embassy in Canberra and then by the Saudi Ministry of "
            "Foreign Affairs. "
            "(FCDO Travel Advice: Saudi Arabia, 2025; Saudi Ministry of Interior, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'saudi-arabia',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals work in Saudi Arabia in engineering, oil and "
            "gas, healthcare, and professional services. Canada maintains an "
            "Embassy in Riyadh. When a Canadian national dies in Saudi Arabia "
            "and their family wishes to repatriate remains to Canada, the death "
            "is registered with the General Directorate of Civil Affairs under "
            "the Ministry of Interior. Saudi Arabia is not a Hague Apostille "
            "Convention member; Canadian documents must be attested by the "
            "Saudi Embassy in Ottawa and then by the Saudi Ministry of Foreign "
            "Affairs. "
            "(FCDO Travel Advice: Saudi Arabia, 2025; Saudi Ministry of Interior, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'saudi-arabia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Saudi Arabia maintain strong bilateral economic ties, "
            "with German nationals working in Saudi Arabia in industrial, "
            "engineering, and construction sectors. Germany maintains an Embassy "
            "in Riyadh. When a German national dies in Saudi Arabia and their "
            "family wishes to repatriate remains to Germany, the death is "
            "registered with the General Directorate of Civil Affairs under "
            "the Ministry of Interior. Saudi Arabia is not a Hague Apostille "
            "Convention member; German documents must be attested by the Saudi "
            "Embassy in Berlin and then by the Saudi Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: Saudi Arabia, 2025; Saudi Ministry of Interior, 2025.)"
        ),
    },
    # R81 -- India x5
    {
        'origin': 'united-kingdom', 'dest': 'india',
        'embassy_city': 'London',
        'intro': (
            "India and the United Kingdom share deep historical, cultural, and "
            "diaspora ties. The British-Indian community is one of the largest "
            "diaspora groups in the UK, and a significant number of British "
            "nationals of Indian heritage maintain strong family connections in "
            "India. British nationals also travel to India for tourism, business, "
            "and family visits in large numbers each year. The Indian High "
            "Commission in London is fully operational. When someone from the "
            "United Kingdom dies in India and their family wishes to repatriate "
            "remains, the death is registered with the state civil registrar "
            "under the Registration of Births and Deaths Act 1969. India joined "
            "the Hague Apostille Convention in 2005; UK documents are apostilled. "
            "(FCDO Travel Advice: India, 2025; Registrar General of India, "
            "Ministry of Home Affairs, India, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'india',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals travel to India for tourism, business, and to visit "
            "family, and Ireland has a growing Indian diaspora community whose "
            "members maintain family connections in India. Ireland maintains an "
            "Embassy in New Delhi. When an Irish national dies in India and their "
            "family wishes to repatriate remains to Ireland, the death is registered "
            "with the state civil registrar under the Registration of Births and "
            "Deaths Act 1969. India joined the Hague Apostille Convention in 2005; "
            "the Indian High Commission or Embassy in Dublin can advise on "
            "documentation requirements. "
            "(FCDO Travel Advice: India, 2025; Registrar General of India, "
            "Ministry of Home Affairs, India, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'india',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and India have bilateral diplomatic and trade relations, with "
            "a growing Indian community in Italian cities including Milan and Rome. "
            "Italian nationals travel to India for tourism and business. The Indian "
            "Embassy in Rome is fully operational. When a person with Indian family "
            "connections dies in Italy and their family wishes to repatriate remains "
            "to India, the death is registered with the local comune (civil registry "
            "office). The atto di morte requires apostilling for Indian authorities; "
            "both Italy and India are Hague Apostille Convention members. A certified "
            "translation may be required for the state civil registrar. "
            "(FCDO Travel Advice: India, 2025; Registrar General of India, "
            "Ministry of Home Affairs, India, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'india',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and India maintain bilateral diplomatic ties, with an Indian "
            "community established across Barcelona, Madrid, and other Spanish "
            "cities. Spanish nationals visit India for tourism, yoga, and spiritual "
            "travel in increasing numbers. The Indian Embassy in Madrid is fully "
            "operational. When a person with Indian family connections dies in Spain "
            "and their family wishes to repatriate remains to India, the death is "
            "registered with the local Registro Civil. The certificado de defuncion "
            "requires apostilling; both Spain and India are Hague Apostille "
            "Convention members. A certified translation may be required for "
            "the state civil registrar. "
            "(FCDO Travel Advice: India, 2025; Registrar General of India, "
            "Ministry of Home Affairs, India, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'india',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and India have longstanding bilateral ties rooted in "
            "trade history and the modern Indian diaspora in the Netherlands, "
            "which is one of Europe's larger Indian communities. Dutch nationals "
            "travel to India for business, technology, and tourism. The Indian "
            "Embassy in The Hague is fully operational. When a person with Indian "
            "family connections dies in the Netherlands and their family wishes to "
            "repatriate remains to India, the death is registered with the local "
            "gemeente (municipal civil registry). The akte van overlijden requires "
            "apostilling; both the Netherlands and India are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: India, 2025; Registrar General of India, "
            "Ministry of Home Affairs, India, 2025.)"
        ),
    },
    # R81 -- Japan x5
    {
        'origin': 'united-kingdom', 'dest': 'japan',
        'embassy_city': 'London',
        'intro': (
            "Japan and the United Kingdom maintain a close bilateral partnership, "
            "with British nationals working in Japan across finance, education, "
            "technology, and creative industries, particularly in Tokyo. Japan "
            "is also a popular destination for British tourists and travellers "
            "on cultural and language exchange programmes. The Japanese Embassy "
            "in London is fully operational. When someone from the United Kingdom "
            "dies in Japan and their family wishes to repatriate remains, the "
            "death must be registered with the local municipal office within "
            "seven days under the Family Register Act. Both the United Kingdom "
            "and Japan are Hague Apostille Convention members; Japan joined in "
            "1970. A certified Japanese translation of the UK documents may be "
            "required by the local municipal office. "
            "(FCDO Travel Advice: Japan, 2025; Japan Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'japan',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Japan have maintained bilateral relations since 1957, "
            "with Irish nationals working in Japan in education (particularly "
            "English-language teaching), technology, and professional services. "
            "Japan is an increasingly popular destination for Irish tourists. "
            "The Japanese Embassy in Dublin is fully operational. When an Irish "
            "national dies in Japan and their family wishes to repatriate remains "
            "to Ireland, the death must be registered with the local municipal "
            "office within seven days under the Family Register Act. Both "
            "Ireland and Japan are Hague Apostille Convention members; Japan "
            "joined in 1970. "
            "(FCDO Travel Advice: Japan, 2025; Japan Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'japan',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Japan maintain one of the world's most "
            "important bilateral alliances, with a large American expat "
            "community in Japan working in finance, technology, military, and "
            "education. Hundreds of thousands of American nationals visit Japan "
            "each year for tourism and cultural exchange. The Japanese Embassy "
            "in Washington DC is fully operational. When an American national "
            "dies in Japan and their family wishes to repatriate remains to "
            "the United States, the death must be registered with the local "
            "municipal office within seven days under the Family Register Act. "
            "Both countries are Hague Apostille Convention members; Japan "
            "joined in 1970, the United States in 1981. "
            "(FCDO Travel Advice: Japan, 2025; Japan Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'czech-republic', 'dest': 'japan',
        'embassy_city': 'Prague',
        'intro': (
            "The Czech Republic and Japan maintain bilateral diplomatic relations, "
            "with Czech nationals visiting Japan for tourism, technology exchange, "
            "and cultural travel. Japan is a growing destination for Czech tourists "
            "attracted by Japanese culture and traditions. The Japanese Embassy "
            "in Prague is fully operational. When a Czech national dies in Japan "
            "and their family wishes to repatriate remains to the Czech Republic, "
            "the death must be registered with the local municipal office within "
            "seven days under the Family Register Act. Both the Czech Republic "
            "and Japan are Hague Apostille Convention members; Japan joined in "
            "1970. A certified Japanese translation of the Czech documents may "
            "be required. "
            "(FCDO Travel Advice: Japan, 2025; Japan Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'hungary', 'dest': 'japan',
        'embassy_city': 'Budapest',
        'intro': (
            "Hungary and Japan maintain diplomatic relations, with Hungarian "
            "nationals visiting Japan for tourism, technology, and cultural "
            "exchange. Japan has attracted growing interest from Hungarian "
            "travellers in recent years. The Japanese Embassy in Budapest is "
            "fully operational. When a Hungarian national dies in Japan and "
            "their family wishes to repatriate remains to Hungary, the death "
            "must be registered with the local municipal office within seven "
            "days under the Family Register Act. Both Hungary and Japan are "
            "Hague Apostille Convention members; Japan joined in 1970, Hungary "
            "in 1973. A certified Japanese translation of the Hungarian documents "
            "may be required. "
            "(FCDO Travel Advice: Japan, 2025; Japan Ministry of Justice, 2025.)"
        ),
    },
    # R82 -- Malaysia x5
    {
        'origin': 'united-kingdom', 'dest': 'malaysia',
        'embassy_city': 'London',
        'intro': (
            "Malaysia and the United Kingdom share longstanding ties through "
            "Commonwealth membership and a shared legal heritage. British nationals "
            "live and work in Malaysia in finance, oil and gas, education, and "
            "professional services, and Kuala Lumpur attracts British expats through "
            "the Malaysia My Second Home (MM2H) programme. The Malaysian High "
            "Commission in London is fully operational. When someone from the "
            "United Kingdom dies in Malaysia and their family wishes to repatriate "
            "remains, the death is registered with the National Registration "
            "Department (JPN). Malaysia is not a member of the Hague Apostille "
            "Convention; UK documents must be attested by the Malaysian High "
            "Commission in London and then by the Malaysian Ministry of Foreign "
            "Affairs (Wisma Putra). "
            "(FCDO Travel Advice: Malaysia, 2025; National Registration Department "
            "(JPN), Malaysia, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'malaysia',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals travel to Malaysia for business and tourism, with "
            "Kuala Lumpur and Penang among the most popular destinations. Ireland "
            "maintains an Embassy in Kuala Lumpur. When an Irish national dies "
            "in Malaysia and their family wishes to repatriate remains to Ireland, "
            "the death is registered with the National Registration Department "
            "(JPN). Malaysia is not a member of the Hague Apostille Convention; "
            "Irish documents must be attested by the Malaysian Embassy in Dublin "
            "and then by the Malaysian Ministry of Foreign Affairs (Wisma Putra) "
            "in Kuala Lumpur. Appoint a specialist on the day of death. "
            "(FCDO Travel Advice: Malaysia, 2025; National Registration Department "
            "(JPN), Malaysia, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'malaysia',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals travel to Malaysia for tourism, business, and "
            "family visits, with a Malaysian-Canadian diaspora maintaining "
            "connections between the two countries. Canada maintains a High "
            "Commission in Kuala Lumpur. When a Canadian national dies in "
            "Malaysia and their family wishes to repatriate remains to Canada, "
            "the death is registered with the National Registration Department "
            "(JPN). Malaysia is not a member of the Hague Apostille Convention; "
            "Canadian documents must be attested by the Malaysian High Commission "
            "in Ottawa and then by the Malaysian Ministry of Foreign Affairs "
            "(Wisma Putra). "
            "(FCDO Travel Advice: Malaysia, 2025; National Registration Department "
            "(JPN), Malaysia, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'malaysia',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals travel to Malaysia for tourism, business, and "
            "as part of Asian travel itineraries. Kuala Lumpur and Langkawi are "
            "popular destinations for Italian visitors. The Malaysian Embassy in "
            "Rome is operational. When a person with Malaysian family connections "
            "dies in Italy and their family wishes to repatriate remains to Malaysia, "
            "the death is registered with the local comune (civil registry office). "
            "Malaysia is not a member of the Hague Apostille Convention; Italian "
            "documents must be attested by the Malaysian Embassy in Rome and then "
            "by the Malaysian Ministry of Foreign Affairs (Wisma Putra). "
            "(FCDO Travel Advice: Malaysia, 2025; National Registration Department "
            "(JPN), Malaysia, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'malaysia',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals travel to Malaysia for tourism, with Kuala Lumpur "
            "and Borneo among destinations on Asian itineraries. A small Spanish "
            "professional community is present in Malaysia. The Malaysian Embassy "
            "in Madrid is operational. When a person with Malaysian family "
            "connections dies in Spain and their family wishes to repatriate "
            "remains to Malaysia, the death is registered with the local Registro "
            "Civil. Malaysia is not a member of the Hague Apostille Convention; "
            "Spanish documents must be attested by the Malaysian Embassy in Madrid "
            "and then by the Malaysian Ministry of Foreign Affairs (Wisma Putra). "
            "(FCDO Travel Advice: Malaysia, 2025; National Registration Department "
            "(JPN), Malaysia, 2025.)"
        ),
    },
    # R82 -- Indonesia x5
    {
        'origin': 'united-kingdom', 'dest': 'indonesia',
        'embassy_city': 'London',
        'intro': (
            "Indonesia is a significant destination for British nationals, "
            "particularly Bali, which attracts large numbers of UK tourists and "
            "long-term visitors. British nationals also work in Indonesia in oil "
            "and gas, natural resources, and NGO sectors. The Indonesian Embassy "
            "in London is fully operational. When someone from the United Kingdom "
            "dies in Indonesia and their family wishes to repatriate remains, the "
            "death is registered with the Disdukcapil (civil registration service) "
            "in the relevant area. Indonesia is not a member of the Hague Apostille "
            "Convention; UK documents must be attested by the Indonesian Embassy "
            "in London and then by the Indonesian Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: Indonesia, 2025; Disdukcapil / Directorate "
            "General of Population and Civil Registration, Indonesia, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'indonesia',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals travel to Indonesia, particularly to Bali and "
            "Lombok, for tourism and wellness retreats. Ireland maintains "
            "consular assistance for Irish nationals in Indonesia through the "
            "Irish Embassy in Singapore. When an Irish national dies in Indonesia "
            "and their family wishes to repatriate remains to Ireland, the death "
            "is registered with the Disdukcapil (civil registration service). "
            "Indonesia is not a member of the Hague Apostille Convention; "
            "Irish documents must be attested by the Indonesian Embassy in Dublin "
            "and then by the Indonesian Ministry of Foreign Affairs. Appoint a "
            "specialist as soon as possible. "
            "(FCDO Travel Advice: Indonesia, 2025; Disdukcapil / Directorate "
            "General of Population and Civil Registration, Indonesia, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'indonesia',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals are regular visitors to Indonesia, particularly "
            "to Bali, which attracts Italian tourists and expatriates seeking "
            "longer stays. The Indonesian Embassy in Rome is operational. When "
            "a person with Indonesian family connections dies in Italy and their "
            "family wishes to repatriate remains to Indonesia, the death is "
            "registered with the local comune. Indonesia is not a member of "
            "the Hague Apostille Convention; Italian documents must be attested "
            "by the Indonesian Embassy in Rome and then by the Indonesian "
            "Ministry of Foreign Affairs in Jakarta. A certified Indonesian "
            "translation is required. "
            "(FCDO Travel Advice: Indonesia, 2025; Disdukcapil / Directorate "
            "General of Population and Civil Registration, Indonesia, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'indonesia',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals travel to Indonesia, particularly to Bali, as "
            "part of Asian travel itineraries. The Indonesian Embassy in Madrid "
            "is operational. When a person with Indonesian family connections "
            "dies in Spain and their family wishes to repatriate remains to "
            "Indonesia, the death is registered with the local Registro Civil. "
            "Indonesia is not a member of the Hague Apostille Convention; "
            "Spanish documents must be attested by the Indonesian Embassy in "
            "Madrid and then by the Indonesian Ministry of Foreign Affairs "
            "in Jakarta. A certified Indonesian translation is required. "
            "(FCDO Travel Advice: Indonesia, 2025; Disdukcapil / Directorate "
            "General of Population and Civil Registration, Indonesia, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'indonesia',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Indonesia share historical ties through the Portuguese "
            "colonial presence in Timor-Leste (now independent) and older "
            "connections across the Indonesian archipelago. Portuguese nationals "
            "visit Indonesia for tourism and as part of Asia-Pacific travel. "
            "The Indonesian Embassy in Lisbon is operational. When a person "
            "with Indonesian family connections dies in Portugal and their "
            "family wishes to repatriate remains to Indonesia, the death is "
            "registered with the local Conservatoria do Registo Civil. "
            "Indonesia is not a member of the Hague Apostille Convention; "
            "Portuguese documents must be attested by the Indonesian Embassy "
            "in Lisbon and then by the Indonesian Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: Indonesia, 2025; Disdukcapil / Directorate "
            "General of Population and Civil Registration, Indonesia, 2025.)"
        ),
    },
    # R82 -- Qatar x5
    {
        'origin': 'united-kingdom', 'dest': 'qatar',
        'embassy_city': 'London',
        'intro': (
            "Qatar has a significant British expatriate community working in "
            "energy, finance, construction, education, and the aviation sector "
            "through Qatar Airways and Hamad International Airport. The "
            "British Embassy in Doha is fully operational. When someone from "
            "the United Kingdom dies in Qatar and their family wishes to "
            "repatriate remains, the death is registered with the Civil Affairs "
            "Section of the Ministry of Interior. Qatar is not a member of the "
            "Hague Apostille Convention; UK documents must be attested by the "
            "Qatari Embassy in London and then by the Qatari Ministry of "
            "Foreign Affairs. Appoint a specialist on the day of death. "
            "(FCDO Travel Advice: Qatar, 2025; Qatar Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'qatar',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals work in Qatar in construction, engineering, aviation, "
            "and professional services. Ireland maintains an Embassy in Doha. "
            "When an Irish national dies in Qatar and their family wishes to "
            "repatriate remains to Ireland, the death is registered with the "
            "Civil Affairs Section of the Ministry of Interior. Qatar is not "
            "a member of the Hague Apostille Convention; Irish documents must "
            "be attested by the Qatari Embassy in Dublin and then by the Qatari "
            "Ministry of Foreign Affairs. Engage a specialist immediately. "
            "(FCDO Travel Advice: Qatar, 2025; Qatar Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'qatar',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals work in Qatar in oil and gas, engineering, "
            "sports management, and professional services. Qatar Airways operates "
            "direct flights to Australia and is a common transit route. Australia "
            "maintains an Embassy in Doha. When an Australian national dies in "
            "Qatar and their family wishes to repatriate remains to Australia, "
            "the death is registered with the Civil Affairs Section of the "
            "Ministry of Interior. Qatar is not a Hague Apostille Convention "
            "member; Australian documents must be attested by the Qatari Embassy "
            "in Canberra and then by the Qatari Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: Qatar, 2025; Qatar Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'qatar',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals work in Qatar in energy, project management, "
            "and professional services. Canada maintains an Embassy in Doha. "
            "When a Canadian national dies in Qatar and their family wishes "
            "to repatriate remains to Canada, the death is registered with "
            "the Civil Affairs Section of the Ministry of Interior. Qatar "
            "is not a Hague Apostille Convention member; Canadian documents "
            "must be attested by the Qatari Embassy in Ottawa and then by "
            "the Qatari Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: Qatar, 2025; Qatar Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'qatar',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Qatar maintain strong economic ties, with German nationals "
            "working in Qatar in industrial, engineering, and technology projects. "
            "Germany has an Embassy in Doha. When a German national dies in Qatar "
            "and their family wishes to repatriate remains to Germany, the death "
            "is registered with the Civil Affairs Section of the Ministry of "
            "Interior. Qatar is not a Hague Apostille Convention member; German "
            "documents must be attested by the Qatari Embassy in Berlin and "
            "then by the Qatari Ministry of Foreign Affairs. The Sterbeurkunde "
            "requires certified translation for Qatari authorities. "
            "(FCDO Travel Advice: Qatar, 2025; Qatar Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    # R82 -- South Africa x5
    {
        'origin': 'united-kingdom', 'dest': 'south-africa',
        'embassy_city': 'London',
        'intro': (
            "South Africa and the United Kingdom share deep Commonwealth ties, "
            "with a large British expat community living in South Africa and a "
            "significant South African diaspora in the UK. British nationals "
            "travel to South Africa for tourism, wildlife safaris, and to visit "
            "family. The South African High Commission in London is fully "
            "operational. When someone from the United Kingdom dies in South "
            "Africa and their family wishes to repatriate remains, the death "
            "is registered with the Department of Home Affairs (DHA) under the "
            "Births and Deaths Registration Act 51 of 1992. South Africa joined "
            "the Hague Apostille Convention in 1995; UK documents are apostilled. "
            "(FCDO Travel Advice: South Africa, 2025; South African Department "
            "of Home Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'south-africa',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals travel to South Africa for tourism, wildlife, and "
            "business, and an Irish-South African community maintains bilateral "
            "ties. Ireland maintains an Embassy in Pretoria. When an Irish "
            "national dies in South Africa and their family wishes to repatriate "
            "remains to Ireland, the death is registered with the Department of "
            "Home Affairs (DHA) under the Births and Deaths Registration Act "
            "51 of 1992. South Africa joined the Hague Apostille Convention in "
            "1995; the South African Embassy in Dublin can advise on "
            "documentation requirements. "
            "(FCDO Travel Advice: South Africa, 2025; South African Department "
            "of Home Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'south-africa',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals travel to South Africa for tourism and wildlife, "
            "and a South African-Canadian community maintains connections between "
            "the two countries. Canada maintains a High Commission in Pretoria. "
            "When a Canadian national dies in South Africa and their family "
            "wishes to repatriate remains to Canada, the death is registered "
            "with the Department of Home Affairs (DHA) under the Births and "
            "Deaths Registration Act 51 of 1992. South Africa joined the Hague "
            "Apostille Convention in 1995; Canada joined in November 2024. "
            "(FCDO Travel Advice: South Africa, 2025; South African Department "
            "of Home Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'south-africa',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgian nationals travel to South Africa for tourism, wildlife "
            "safaris, and business, and Belgian companies are active in the "
            "South African mining and technology sectors. The South African "
            "Embassy in Brussels is operational. When a person with South "
            "African family connections dies in Belgium and their family "
            "wishes to repatriate remains to South Africa, the death is "
            "registered with the local commune or gemeenten civil registry. "
            "Both Belgium and South Africa are Hague Apostille Convention "
            "members; the acte de deces or overlijdensakte requires apostilling "
            "for South African Department of Home Affairs. "
            "(FCDO Travel Advice: South Africa, 2025; South African Department "
            "of Home Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'south-africa',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals travel to South Africa for wildlife tourism and "
            "volunteers work across NGO and development sectors in the country. "
            "The South African Embassy in Stockholm is operational. When a "
            "person with South African family connections dies in Sweden and "
            "their family wishes to repatriate remains to South Africa, the "
            "death is registered with the Swedish Tax Agency (Skatteverket) "
            "Population Register. Both Sweden and South Africa are Hague "
            "Apostille Convention members; the dodsfallsintyg requires "
            "apostilling and, where required by the Department of Home Affairs, "
            "a certified English translation. "
            "(FCDO Travel Advice: South Africa, 2025; South African Department "
            "of Home Affairs, 2025.)"
        ),
    },
    # R82 -- Kuwait x5
    {
        'origin': 'united-kingdom', 'dest': 'kuwait',
        'embassy_city': 'London',
        'intro': (
            "Kuwait has a British expat community working in oil and gas, finance, "
            "engineering, and healthcare, with the United Kingdom and Kuwait "
            "maintaining close bilateral ties since the Gulf War. The British "
            "Embassy in Kuwait City is fully operational. When someone from the "
            "United Kingdom dies in Kuwait and their family wishes to repatriate "
            "remains, the death is registered with the Civil Affairs Division of "
            "the Ministry of Interior. Kuwait is not a member of the Hague "
            "Apostille Convention; UK documents must be attested by the Kuwaiti "
            "Embassy in London and then by the Kuwaiti Ministry of Foreign "
            "Affairs. Appoint a specialist on the day of death. "
            "(FCDO Travel Advice: Kuwait, 2025; Kuwait Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'kuwait',
        'embassy_city': 'Dublin',
        'intro': (
            "Irish nationals work in Kuwait in engineering, oil and gas, and "
            "professional services. Ireland provides consular assistance for "
            "Irish nationals in Kuwait through the Irish Embassy in Riyadh. "
            "When an Irish national dies in Kuwait and their family wishes to "
            "repatriate remains to Ireland, the death is registered with the "
            "Civil Affairs Division of the Ministry of Interior. Kuwait is "
            "not a member of the Hague Apostille Convention; Irish documents "
            "must be attested by the Kuwaiti Embassy in Dublin and then by "
            "the Kuwaiti Ministry of Foreign Affairs. Engage a specialist "
            "immediately. "
            "(FCDO Travel Advice: Kuwait, 2025; Kuwait Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'kuwait',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals work in Kuwait in oil and gas, project "
            "management, and engineering. Australia provides consular assistance "
            "for Australian nationals in Kuwait through the Australian Embassy "
            "in Riyadh. When an Australian national dies in Kuwait and their "
            "family wishes to repatriate remains to Australia, the death is "
            "registered with the Civil Affairs Division of the Ministry of "
            "Interior. Kuwait is not a Hague Apostille Convention member; "
            "Australian documents must be attested by the Kuwaiti Embassy "
            "in Canberra and then by the Kuwaiti Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: Kuwait, 2025; Kuwait Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'kuwait',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals work in Kuwait in oil and gas, engineering, "
            "and project management. Canada maintains an Embassy in Kuwait City. "
            "When a Canadian national dies in Kuwait and their family wishes "
            "to repatriate remains to Canada, the death is registered with "
            "the Civil Affairs Division of the Ministry of Interior. Kuwait "
            "is not a Hague Apostille Convention member; Canadian documents "
            "must be attested by the Kuwaiti Embassy in Ottawa and then by "
            "the Kuwaiti Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: Kuwait, 2025; Kuwait Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'kuwait',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals work in Kuwait in engineering, construction, "
            "and oil and gas sectors. Germany maintains an Embassy in Kuwait City. "
            "When a German national dies in Kuwait and their family wishes "
            "to repatriate remains to Germany, the death is registered with "
            "the Civil Affairs Division of the Ministry of Interior. Kuwait "
            "is not a Hague Apostille Convention member; German documents "
            "must be attested by the Kuwaiti Embassy in Berlin and then by "
            "the Kuwaiti Ministry of Foreign Affairs. The Sterbeurkunde "
            "requires certified Arabic translation for Kuwaiti authorities. "
            "(FCDO Travel Advice: Kuwait, 2025; Kuwait Ministry of Interior "
            "Civil Affairs, 2025.)"
        ),
    },
]


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

    complexity = dm.get('complexity_override', od['complexity'])
    timeline_avg = dm.get('timeline_avg_override', od['timeline_avg'])
    timeline_fast = dm.get('timeline_fast_override', od['timeline_fast'])
    timeline_complex = dm.get('timeline_complex_override', od['timeline_complex'])
    doc_time = od['doc_time']
    dest_key = dm['key']

    desc_note = complexity_to_desc(complexity)
    t_origin = title_name(origin_name)
    t_dest = dm.get('short_title', title_name(dest_name))
    description = (
        f"Someone has died in {origin_name}. Repatriation to {dest_name} "
        f"takes {timeline_avg}. {desc_note} Contact us 24/7."
    )

    dest_reception = dm['reception']
    dest_consular = dm['consular_template'].format(city=embassy_city)
    arrival_faq = dm['arrival_faq']

    if origin_slug == 'united-kingdom':
        pt3 = (
            f"Contact the {dest_name} High Commission or Embassy in London "
            f"for documentation requirements. They cannot fund repatriation."
        )
        step1_timing = (
            "Day of death. Call 999 for emergency services. "
            f"Contact the {dest_name} High Commission or Embassy in London."
        )
        step3_action = f"{dest_name} High Commission or Embassy in London notified"
    elif origin_slug == 'ireland':
        pt3 = (
            f"Contact the {dest_name} High Commission or Embassy in Dublin "
            f"for documentation requirements. They cannot fund repatriation."
        )
        step1_timing = (
            "Day of death. Call 999 or 112 for emergency services. "
            f"Contact the {dest_name} High Commission or Embassy in Dublin."
        )
        step3_action = f"{dest_name} High Commission or Embassy in Dublin notified"
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
    elif origin_slug == 'ireland':
        sideways = f"""    - url: "/routes/{dest_slug}-to-ireland/"
      text: "Repatriation from {dest_name} to Ireland"
    - url: "/routes/ireland-to-united-kingdom/"
      text: "Repatriation from Ireland to the UK"
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
    exit(main())
