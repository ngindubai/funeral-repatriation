#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R85-R86.

   R85 (25 routes, START_VARIANT=2=C):
     Philippines x5: united-kingdom, germany, france, italy, south-korea
     Nepal x5:       canada, france, italy, qatar, kuwait
     Ethiopia x5:    australia, canada, norway, sweden, south-africa
     Sri Lanka x5:   australia, canada, france, india, italy
     Brazil x5:      australia, canada, france, portugal, netherlands

   R86 (25 routes, continues from R85):
     Mexico x5:     australia, france, italy, ireland, netherlands
     Colombia x5:   australia, canada, france, netherlands, portugal
     Jordan x5:     australia, germany, netherlands, sweden, india
     Algeria x5:    united-kingdom, united-states, australia, canada, italy
     Argentina x5:  australia, canada, france, netherlands, portugal

   Template rotation: R84 ended on variant B (idx=1). R85 starts at C (idx=2).
   START_VARIANT=2 applies across all 50 routes as one continuous cycle.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 2  # C

DEST_META = {
    'philippines': {
        'name': 'the Philippines',
        'slug': 'philippines',
        'key': 'ph',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Philippine funeral director takes custody at Ninoy Aquino "
            "International Airport (MNL) in Manila, Mactan-Cebu International "
            "Airport (CEB), or Francisco Bangoy International Airport (DVO) in "
            "Davao, depending on the final destination. The Philippine Statistics "
            "Authority (PSA) handles civil registration of deaths abroad through "
            "the Philippine Overseas Labor Office (POLO) or the relevant Philippine "
            "Embassy or Consulate. The Embassy or Consulate in the origin country "
            "must issue a Report of Death (ROD) before repatriation can proceed; "
            "the ROD is a required document. The Philippines is not a member of "
            "the Hague Apostille Convention; all foreign documents require full "
            "consular authentication through the Philippine Embassy or Consulate in "
            "the country of origin. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. Burial or cremation permit "
            "from the Local Civil Registry Office (LCRO) is required before final "
            "disposition. (Philippine Department of Foreign Affairs/PSA, 2025.)"
        ),
        'consular_template': (
            "The Philippine Embassy or Consulate in {city} can advise on "
            "documentation requirements and must issue a Report of Death (ROD) "
            "before repatriation can proceed. The Philippines is not a Hague "
            "Apostille Convention member; all documents require full consular "
            "authentication. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Philippine funeral director takes custody at Ninoy Aquino "
            "International Airport (MNL), Mactan-Cebu (CEB), or Francisco Bangoy "
            "(DVO) cargo terminal. The Philippine Statistics Authority (PSA) "
            "handles civil registration. A Report of Death (ROD) issued by the "
            "Philippine Embassy in the origin country must accompany the remains. "
            "The Philippines is not a Hague Apostille member; full consular "
            "authentication is required for all foreign documents. An embalming "
            "certificate and hermetically sealed coffin are required. A burial or "
            "cremation permit from the Local Civil Registry Office (LCRO) is "
            "required before final disposition."
        ),
        'emergency_line': 'contact the Philippine Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-philippines',
    },
    'nepal': {
        'name': 'Nepal',
        'slug': 'nepal',
        'key': 'np',
        'complexity_override': 'moderate-high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-14 weeks',
        'reception': (
            "The Nepali funeral director takes custody at Tribhuvan International "
            "Airport (KTM) in Kathmandu, Nepal's only international airport. All "
            "repatriated remains arrive via KTM regardless of the final destination "
            "within Nepal. Death registration of overseas Nepalis is handled by "
            "the local Ward Office (formerly the Village Development Committee or "
            "Municipality) under the Ministry of Home Affairs, upon receipt of "
            "the overseas documentation. Nepal is not a member of the Hague "
            "Apostille Convention; all foreign documents require full consular "
            "authentication through the Embassy of Nepal in the country of origin. "
            "All documents require certified Nepali translation for submission to "
            "the Ward Office. A hermetically sealed zinc-lined coffin is required "
            "for all air imports. The Embassy of Nepal in the origin country "
            "coordinates the overseas death registration process. "
            "(Embassy of Nepal, London; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
        'consular_template': (
            "The Embassy of Nepal in {city} can advise on documentation "
            "requirements and coordinates the overseas death registration process. "
            "Nepal is not a Hague Apostille Convention member; full consular "
            "authentication through the Embassy in {city} is required. The "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Nepali funeral director takes custody at Tribhuvan International "
            "Airport (KTM) in Kathmandu, Nepal's only international airport. The "
            "local Ward Office under the Ministry of Home Affairs handles death "
            "registration on receipt of overseas documentation. Nepal is not a "
            "Hague Apostille Convention member; full consular authentication "
            "through the Embassy of Nepal in the origin country is required. "
            "All foreign documents require certified Nepali translation for "
            "the Ward Office. A hermetically sealed zinc-lined coffin is required. "
            "The Embassy of Nepal coordinates the overseas death registration."
        ),
        'emergency_line': 'contact the Embassy of Nepal in the origin country',
        'hub_url': 'repatriation-from-nepal',
    },
    'ethiopia': {
        'name': 'Ethiopia',
        'slug': 'ethiopia',
        'key': 'et',
        'complexity_override': 'moderate-high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-14 weeks',
        'reception': (
            "The Ethiopian funeral director takes custody at Addis Ababa Bole "
            "International Airport (ADD) cargo terminal. Civil registration of "
            "overseas deaths is handled at the local kebele level through VERA, "
            "Ethiopia's civil events registration authority, upon receipt of "
            "the overseas documentation. The Ethiopian Embassy or Consulate in "
            "the country of origin must authenticate all foreign documents. "
            "All documents require certified Amharic translation for submission "
            "to VERA. Ethiopia is not a member of the Hague Apostille Convention; "
            "full consular authentication is required for all foreign documents. "
            "A hermetically sealed zinc-lined coffin is required for all air "
            "imports. A burial or cremation permit from the relevant local "
            "authority is required before final disposition. Ethiopian Airlines "
            "operates the main cargo route from most international hubs to ADD. "
            "(Ethiopian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Ethiopian Embassy or Consulate in {city} can advise on "
            "documentation requirements and must authenticate all foreign "
            "documents. Ethiopia is not a Hague Apostille Convention member; "
            "full consular authentication through the Embassy in {city} is "
            "required. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Ethiopian funeral director takes custody at Addis Ababa Bole "
            "International Airport (ADD) cargo terminal. Civil registration is "
            "handled at kebele level through VERA, Ethiopia's civil events "
            "registration authority. All foreign documents require certified "
            "Amharic translation and full consular authentication through the "
            "Ethiopian Embassy in the origin country. Ethiopia is not a Hague "
            "Apostille Convention member. A hermetically sealed zinc-lined coffin "
            "is required. A burial or cremation permit from the relevant local "
            "authority is required before final disposition."
        ),
        'emergency_line': 'contact the Ethiopian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-ethiopia',
    },
    'sri-lanka': {
        'name': 'Sri Lanka',
        'slug': 'sri-lanka',
        'key': 'lk',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) in Colombo, which handles the majority "
            "of repatriated remains. Mattala Rajapaksa International Airport (HRI) "
            "in Hambantota may be used for arrivals in southern Sri Lanka. The "
            "Registrar General's Department handles civil registration of deaths "
            "abroad on receipt of overseas documentation authenticated by the "
            "Sri Lanka High Commission or Embassy in the country of origin. "
            "Sri Lanka is not a member of the Hague Apostille Convention; full "
            "consular authentication is required for all foreign documents. All "
            "documents require certified Sinhala or Tamil translation for "
            "submission to the Registrar General's Department. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. A burial or cremation permit is required from the "
            "relevant local authority before final disposition. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Sri Lanka High Commission or Embassy in {city} can advise on "
            "documentation requirements and must authenticate all foreign documents. "
            "Sri Lanka is not a Hague Apostille Convention member; full consular "
            "authentication through the High Commission in {city} is required. "
            "The High Commission cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) in Colombo, or Mattala Rajapaksa (HRI) "
            "for southern arrivals. The Registrar General's Department handles "
            "civil registration on receipt of authenticated overseas documentation. "
            "Sri Lanka is not a Hague Apostille Convention member; full consular "
            "authentication through the Sri Lanka High Commission or Embassy in "
            "the origin country is required. All foreign documents require "
            "certified Sinhala or Tamil translation. An embalming certificate "
            "and hermetically sealed coffin are required. A burial or cremation "
            "permit is required before final disposition."
        ),
        'emergency_line': 'contact the Sri Lanka High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-sri-lanka',
    },
    'brazil': {
        'name': 'Brazil',
        'slug': 'brazil',
        'key': 'br',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Brazilian funeral director takes custody at Guarulhos "
            "International Airport (GRU) in Sao Paulo, Galeao International "
            "Airport (GIG) in Rio de Janeiro, or Brasilia International Airport "
            "(BSB), depending on the final destination. The local Cartorio de "
            "Registro Civil (Civil Registry Notary) handles death registration. "
            "ANVISA (the Brazilian National Health Surveillance Agency) must "
            "clear all incoming human remains; an ANVISA-compliant health "
            "certificate from the origin country is required. For violent or "
            "unexplained deaths, the Instituto Medico Legal (IML) takes "
            "jurisdiction before final disposition. Brazil joined the Hague "
            "Apostille Convention in 2016; apostille certificates from member "
            "states are accepted, which reduces authentication requirements "
            "compared with non-Hague routes. An embalming certificate and "
            "hermetically sealed coffin are required. All documents must be "
            "in Portuguese or accompanied by a certified Portuguese translation. "
            "(Brazilian Ministry of Foreign Affairs/ANVISA, 2025.)"
        ),
        'consular_template': (
            "The Brazilian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Brazil. Brazil "
            "joined the Hague Apostille Convention in 2016; apostille certificates "
            "from member states are accepted. The Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Brazilian funeral director takes custody at Guarulhos (GRU) "
            "in Sao Paulo, Galeao (GIG) in Rio de Janeiro, or Brasilia (BSB) "
            "cargo terminal. The local Cartorio de Registro Civil handles death "
            "registration. ANVISA must clear all incoming remains; a health "
            "certificate from the origin country is required. Brazil joined "
            "the Hague Apostille Convention in 2016; apostille certificates "
            "are accepted from member states. For violent or unexplained deaths, "
            "the Instituto Medico Legal (IML) takes jurisdiction. An embalming "
            "certificate and hermetically sealed coffin are required. All "
            "documents must be in Portuguese or with certified Portuguese "
            "translation."
        ),
        'emergency_line': 'contact the Brazilian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-brazil',
    },
    'mexico': {
        'name': 'Mexico',
        'slug': 'mexico',
        'key': 'mx',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Mexican funeral director takes custody at Benito Juarez "
            "International Airport (MEX) in Mexico City, Guadalajara International "
            "Airport (GDL), or Monterrey International Airport (MTY), depending "
            "on the final destination. The local Registro Civil (Civil Registry "
            "Office) handles death registration of foreign nationals. For violent "
            "or unexplained deaths, SEMEFO (Servicio Medico Forense, the Forensic "
            "Medical Service) takes jurisdiction before the body can be released "
            "for final disposition; this adds time. Mexico is a Hague Apostille "
            "Convention member; apostille certificates from member states are "
            "accepted. All documents must be in Spanish or accompanied by a "
            "certified Spanish translation. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Mexican Secretariat of Foreign Affairs/Registro Civil, 2025.)"
        ),
        'consular_template': (
            "The Mexican Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Mexico. Mexico is "
            "a Hague Apostille Convention member; apostille certificates from "
            "member states are accepted. The Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Mexican funeral director takes custody at Benito Juarez "
            "International Airport (MEX), Guadalajara (GDL), or Monterrey "
            "(MTY) cargo terminal. The local Registro Civil handles death "
            "registration. For violent or unexplained deaths, SEMEFO "
            "(Forensic Medical Service) takes jurisdiction before the body "
            "can be released; this adds time. Mexico is a Hague Apostille "
            "Convention member; apostille certificates from member states are "
            "accepted. All documents must be in Spanish or with certified "
            "Spanish translation. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Mexican Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-mexico',
    },
    'colombia': {
        'name': 'Colombia',
        'slug': 'colombia',
        'key': 'co',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport (BOG) in Bogota, Jose Maria Cordova "
            "International Airport (MDE) near Medellin, or Alfonso Bonilla "
            "Aragon International Airport (CLO) in Cali, depending on the "
            "final destination. The Registraduria Nacional del Estado Civil "
            "handles civil registration. For violent or unexplained deaths, "
            "the Instituto Nacional de Medicina Legal y Ciencias Forenses "
            "(National Institute of Legal Medicine, commonly called Medicina "
            "Legal) takes jurisdiction before the body can be released; this "
            "adds time. Colombia is a Hague Apostille Convention member; "
            "apostille certificates from member states are accepted. All "
            "documents must be in Spanish or accompanied by a certified "
            "Spanish translation. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Colombian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Colombian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Colombia. Colombia "
            "is a Hague Apostille Convention member; apostille certificates "
            "from member states are accepted. The Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport (BOG) in Bogota, Jose Maria Cordova (MDE) "
            "near Medellin, or Alfonso Bonilla Aragon (CLO) in Cali. The "
            "Registraduria Nacional del Estado Civil handles civil registration. "
            "For violent or unexplained deaths, Medicina Legal (National Institute "
            "of Legal Medicine) takes jurisdiction. Colombia is a Hague Apostille "
            "Convention member; apostille certificates from member states are "
            "accepted. All documents must be in Spanish or with certified "
            "Spanish translation. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Colombian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-colombia',
    },
    'jordan': {
        'name': 'Jordan',
        'slug': 'jordan',
        'key': 'jo',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Jordanian funeral director takes custody at Queen Alia "
            "International Airport (AMM) in Amman. The Civil Status Department "
            "of the Ministry of Interior handles death registration. For Muslim "
            "remains, Islamic law procedures apply and prompt burial is expected; "
            "a burial permit from the Ministry of Interior is required before "
            "final disposition. All foreign documents require certified Arabic "
            "translation. Jordan is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Jordanian "
            "Embassy or Consulate in the country of origin is required. An "
            "embalming certificate and hermetically sealed coffin are required "
            "for all air imports. A health clearance certificate is required "
            "for all incoming human remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Jordanian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Jordan. Jordan is "
            "not a Hague Apostille Convention member; full consular authentication "
            "through the Jordanian Embassy in {city} is required. The Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Jordanian funeral director takes custody at Queen Alia "
            "International Airport (AMM) cargo terminal. The Civil Status "
            "Department of the Ministry of Interior handles death registration. "
            "For Muslim remains, Islamic law procedures apply and a burial "
            "permit from the Ministry of Interior is required; prompt burial "
            "is expected. All foreign documents require certified Arabic "
            "translation. Jordan is not a Hague Apostille Convention member; "
            "full consular authentication through the Jordanian Embassy in the "
            "origin country is required. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Jordanian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-jordan',
    },
    'algeria': {
        'name': 'Algeria',
        'slug': 'algeria',
        'key': 'dz',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Algerian funeral director takes custody at Houari Boumediene "
            "International Airport (ALG) in Algiers. The local etat civil "
            "(Municipal Civil Registry, commune level) handles death registration. "
            "For Muslim remains, Islamic law procedures apply and prompt burial "
            "is expected; a burial permit from the relevant local authority is "
            "required before final disposition. Algeria has a predominantly "
            "Muslim population (approximately 99 per cent), and Islamic law "
            "procedures apply in the large majority of cases. All foreign "
            "documents require certified Arabic translation; French-language "
            "documents are also accepted in Algeria. Algeria is not a member of "
            "the Hague Apostille Convention; full consular authentication through "
            "the Algerian Embassy or Consulate in the country of origin is "
            "required for all documents. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Algerian Ministry of Foreign Affairs/MICLAT, 2025.)"
        ),
        'consular_template': (
            "The Algerian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Algeria. Algeria is "
            "not a Hague Apostille Convention member; full consular authentication "
            "through the Algerian Embassy in {city} is required. The Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Algerian funeral director takes custody at Houari Boumediene "
            "International Airport (ALG) cargo terminal. The local etat civil "
            "(commune-level civil registry) registers the death on receipt of "
            "authenticated overseas documentation. For Muslim remains, Islamic "
            "law procedures apply; a burial permit from the local authority is "
            "required and prompt burial is expected. All foreign documents "
            "require certified Arabic translation. Algeria is not a Hague "
            "Apostille Convention member; full consular authentication through "
            "the Algerian Embassy in the origin country is required. An "
            "embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Algerian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-algeria',
    },
    'argentina': {
        'name': 'Argentina',
        'slug': 'argentina',
        'key': 'ar',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Argentine funeral director takes custody at Ministro Pistarini "
            "International Airport (EZE) in Ezeiza, Buenos Aires. The local "
            "Registro Civil Provincial handles death registration. For violent "
            "or unexplained deaths, the Cuerpo Medico Forense (Forensic Medical "
            "Corps) takes jurisdiction before the body can be released for final "
            "disposition; this adds time. Argentina joined the Hague Apostille "
            "Convention in 1987; apostille certificates from member states are "
            "accepted, which reduces authentication requirements compared with "
            "non-Hague routes. All documents must be in Spanish or accompanied "
            "by a certified Spanish translation. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Argentine Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Argentine Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Argentina. Argentina "
            "joined the Hague Apostille Convention in 1987; apostille certificates "
            "from member states are accepted. The Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Argentine funeral director takes custody at Ministro Pistarini "
            "International Airport (EZE) in Ezeiza, Buenos Aires. The local "
            "Registro Civil Provincial handles death registration. For violent "
            "or unexplained deaths, the Cuerpo Medico Forense (Forensic Medical "
            "Corps) takes jurisdiction. Argentina joined the Hague Apostille "
            "Convention in 1987; apostille certificates from member states are "
            "accepted. All documents must be in Spanish or with certified "
            "Spanish translation. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Argentine Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-argentina',
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
    'south-korea': {
        'name': 'South Korea',
        'emergency': '112 (police) / 119 (fire and ambulance)',
        'registry': 'the local gu office (ward office) under the Act on the Registration of Family Relations',
        'cert_name': 'samang jindan-seo (death certificate)',
        'cert_lang': 'Korean',
        'overview': (
            "Call 112 for police or 119 for fire and ambulance. Death is certified "
            "by a physician. The samang jindan-seo is registered with the local gu "
            "office (ward office) under the Act on the Registration of Family "
            "Relations. Police take jurisdiction for violent or unexplained deaths. "
            "Documentation is in Korean and requires certified translation. South "
            "Korea is a member of the Hague Apostille Convention."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '6-10 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation in South Korea is widely available at registered crematoriums "
            "across major cities including Seoul and Busan."
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
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
    'norway': {
        'name': 'Norway',
        'emergency': '112 (police 02800 / ambulance 113)',
        'registry': 'Folkeregisteret (the civil registration system / Skatteetaten)',
        'cert_name': 'dodsattest (death certificate)',
        'cert_lang': 'Norwegian',
        'overview': (
            "Call 112 for emergency services (or 02800 for police, 113 for "
            "ambulance). Death is certified by a physician. The dodsattest is "
            "registered with Folkeregisteret (the civil registration system, "
            "administered by the Norwegian Tax Administration / Skatteetaten). "
            "The police take jurisdiction for violent or unexplained deaths. "
            "Note that deaths occurring in Svalbard require transfer to mainland "
            "Norway before any international cargo flight can depart. Norway "
            "is a Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Norway is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (police take jurisdiction)',
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
    'south-africa': {
        'name': 'South Africa',
        'emergency': '112 / 10111 (police) / 10177 (ambulance)',
        'registry': 'the Department of Home Affairs under the Births, Deaths and Marriages Act',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 112 for emergency services, 10111 for police, or 10177 for "
            "ambulance. Death is certified by a physician and registered with the "
            "Department of Home Affairs under the Births, Deaths and Marriages Act. "
            "The South African Police Service (SAPS) takes jurisdiction for violent "
            "or unexplained deaths; these cases require a pathologist's report "
            "before the body can be released. South Africa is a Hague Apostille "
            "Convention member. Processing times can vary; Johannesburg and Cape "
            "Town process faster than rural areas."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation in South Africa is available at licensed facilities in "
            "major cities including Johannesburg, Cape Town, and Durban. A death "
            "certificate and authority to cremate are required before cremation "
            "can proceed."
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths (SAPS and pathologist take jurisdiction)',
    },
    'ireland': {
        'name': 'Ireland',
        'emergency': '999 or 112',
        'registry': "the local registrar's office (reporting to the General Register Office / GRO)",
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 999 or 112 for emergency services. Death is certified by a "
            "registered medical practitioner. The death is registered with the "
            "local registrar's office, which reports to the General Register "
            "Office (GRO). The coroner takes jurisdiction for sudden, violent, "
            "or unexplained deaths. Ireland is a Hague Apostille Convention "
            "member (joined 1967)."
        ),
        'doc_time': '3-7 days (coroner cases longer)',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Ireland is available at licensed facilities. A cremation "
            "order from the coroner is required where the coroner has taken "
            "jurisdiction."
        ),
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
    'qatar': {
        'name': 'Qatar',
        'emergency': '999',
        'registry': 'the Ministry of Interior Civil Status Affairs Department',
        'cert_name': 'death certificate (shahadat wafah)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 999 for emergency services. Death is certified by a hospital "
            "physician. The death is registered with the Ministry of Interior "
            "Civil Status Affairs Department. Foreign nationals in Qatar are "
            "under the kafala (sponsorship) system; the sponsoring employer is "
            "responsible for notifying the Civil Status Department and the "
            "deceased's embassy. All documents are in Arabic and require "
            "certified translation. The public prosecutor takes jurisdiction for "
            "violent, suspicious, or unexplained deaths. Qatar is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required for all foreign documents. Contact the relevant embassy "
            "on the day of death."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available in Qatar. Repatriation of the full body "
            "is the only option for most families. Contact the relevant embassy "
            "on the day of death to begin the repatriation process."
        ),
        'postmortem_trigger': 'Violent, suspicious, or unexplained deaths (public prosecutor takes jurisdiction)',
    },
    'kuwait': {
        'name': 'Kuwait',
        'emergency': '112 / 777 (police) / 180 (ambulance)',
        'registry': 'the Civil Affairs Department of the Ministry of Interior',
        'cert_name': 'death certificate',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 112 for emergency services, 777 for police, or 180 for "
            "ambulance. Death is certified by a hospital physician. The death "
            "is registered with the Civil Affairs Department of the Ministry "
            "of Interior. Foreign nationals must have deaths reported by their "
            "employer or sponsor; the deceased's embassy must be notified on "
            "the day of death. All documents are in Arabic and require "
            "certified translation. Kuwait is not a Hague Apostille Convention "
            "member; full consular authentication is required. The public "
            "prosecutor takes jurisdiction for violent or unexplained deaths."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available in Kuwait. Repatriation of the full "
            "body is the only option. Under Islamic law, burial should occur as "
            "soon as possible; prompt notification of the relevant embassy "
            "is important to avoid delay."
        ),
        'postmortem_trigger': 'Violent, suspicious, or unexplained deaths (public prosecutor takes jurisdiction)',
    },
}

ROUTES = [
    # R85 -- Philippines x5
    {
        'origin': 'united-kingdom', 'dest': 'philippines',
        'embassy_city': 'London',
        'intro': (
            "The Philippines has one of the largest diaspora communities in the "
            "United Kingdom, with Filipino nationals prominent in the NHS, care "
            "sector, and merchant navy. When a Filipino national dies in the "
            "United Kingdom and their family wishes to repatriate remains to the "
            "Philippines, the death must be registered within 5 days at the local "
            "register office. The Philippine Statistics Authority (PSA) handles "
            "civil registration of the death abroad through the Philippine Embassy "
            "in London. The Philippine Embassy in London must issue a Report of "
            "Death (ROD) before repatriation can proceed; this is a required "
            "document alongside the UK death certificate. The Philippines is not "
            "a Hague Apostille Convention member; full consular authentication "
            "through the Philippine Embassy in London is required for UK documents. "
            "(FCDO Travel Advice, 2025; Philippine Department of Foreign Affairs "
            "and PSA, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'philippines',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has an active Filipino community, with nationals working in "
            "healthcare, services, and information technology across Berlin, "
            "Frankfurt, and Cologne. The Philippine Embassy in Berlin is fully "
            "operational. When a Filipino national dies in Germany and their family "
            "wishes to repatriate remains to the Philippines, the death is "
            "registered with the local Standesamt (civil registry). The Philippine "
            "Statistics Authority (PSA) requires a Report of Death (ROD) issued "
            "by the Philippine Embassy in Berlin for all overseas Filipinos. The "
            "Sterbeurkunde must accompany the ROD and all repatriation "
            "documentation. The Philippines is not a Hague Apostille Convention "
            "member; German documents require full consular authentication through "
            "the Philippine Embassy in Berlin. "
            "(Philippine Department of Foreign Affairs, 2025; German Federal "
            "Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'philippines',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Filipino community, with nationals working in Paris and "
            "other French cities in healthcare, hospitality, and domestic services. "
            "The Philippine Embassy in Paris is fully operational. When a Filipino "
            "national dies in France and their family wishes to repatriate remains "
            "to the Philippines, the death is registered with the local mairie "
            "(town hall). The Philippine Statistics Authority (PSA) requires a "
            "Report of Death (ROD) issued by the Philippine Embassy in Paris. The "
            "acte de deces must be included in all repatriation documentation. "
            "The Philippines is not a Hague Apostille Convention member; French "
            "documents require full consular authentication through the Philippine "
            "Embassy in Paris. "
            "(Philippine Department of Foreign Affairs, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'philippines',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a significant Filipino community, with nationals working "
            "across Rome, Milan, and other major cities in domestic services, "
            "healthcare, and hospitality. The Philippine Embassy in Rome is fully "
            "operational. When a Filipino national dies in Italy and their family "
            "wishes to repatriate remains to the Philippines, the death is "
            "registered with the local comune (civil registry). The Philippine "
            "Statistics Authority (PSA) requires a Report of Death (ROD) issued "
            "by the Philippine Embassy in Rome. The atto di morte must be included "
            "in all repatriation documentation. The Philippines is not a Hague "
            "Apostille Convention member; Italian documents require full consular "
            "authentication through the Philippine Embassy in Rome. "
            "(Philippine Department of Foreign Affairs, 2025; Italian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-korea', 'dest': 'philippines',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korea and the Philippines maintain active bilateral ties, with "
            "a substantial Filipino community working in Seoul and Busan in "
            "manufacturing, services, and domestic roles. South Korea's Employment "
            "Permit System (EPS) has brought Filipino workers to Korea, and "
            "bilateral migration is ongoing. The Philippine Embassy in Seoul is "
            "fully operational. When a Filipino national dies in South Korea and "
            "their family wishes to repatriate remains to the Philippines, the "
            "death is registered with the local gu office (ward office). The "
            "Philippine Statistics Authority (PSA) requires a Report of Death "
            "(ROD) issued by the Philippine Embassy in Seoul. The Philippines is "
            "not a Hague Apostille Convention member; South Korean documents "
            "require full authentication through the Philippine Embassy in Seoul. "
            "(Philippine Department of Foreign Affairs, 2025; South Korean "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R85 -- Nepal x5
    {
        'origin': 'canada', 'dest': 'nepal',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts an established Nepali-Canadian community, with nationals "
            "concentrated in Toronto, Vancouver, and Calgary working in healthcare, "
            "hospitality, and professional services. The Embassy of Nepal in Ottawa "
            "is fully operational. When a Nepali national dies in Canada and their "
            "family wishes to repatriate remains to Nepal, the death is registered "
            "with the provincial civil registration authority. Tribhuvan International "
            "Airport (KTM) in Kathmandu is Nepal's only international airport; all "
            "repatriated remains arrive there. Nepal is not a Hague Apostille "
            "Convention member; full consular authentication through the Embassy "
            "of Nepal in Ottawa is required. A certified Nepali translation of all "
            "documents is required by the Ward Office on arrival. "
            "(Embassy of Nepal, Ottawa; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'nepal',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Nepali community, with nationals working in Paris and "
            "other French cities in restaurants, hospitality, and services. The "
            "Embassy of Nepal in Paris is fully operational. When a Nepali national "
            "dies in France and their family wishes to repatriate remains to Nepal, "
            "the death is registered with the local mairie (town hall). Tribhuvan "
            "International Airport (KTM) in Kathmandu is Nepal's only international "
            "airport; all remains arrive there. The acte de deces requires certified "
            "Nepali translation for the Ward Office in Nepal. Nepal is not a Hague "
            "Apostille Convention member; full consular authentication through the "
            "Embassy of Nepal in Paris is required. "
            "(Embassy of Nepal, Paris; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'nepal',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a Nepali community, with nationals working in Rome, Milan, "
            "and northern Italian cities in hospitality and services. The Embassy "
            "of Nepal in Rome is fully operational. When a Nepali national dies in "
            "Italy and their family wishes to repatriate remains to Nepal, the death "
            "is registered with the local comune (civil registry). Tribhuvan "
            "International Airport (KTM) in Kathmandu is Nepal's only international "
            "airport. The atto di morte requires certified Nepali translation for "
            "the Ward Office in Nepal. Nepal is not a Hague Apostille Convention "
            "member; full consular authentication through the Embassy of Nepal in "
            "Rome is required for Italian documents. "
            "(Embassy of Nepal, Rome; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'qatar', 'dest': 'nepal',
        'embassy_city': 'Doha',
        'intro': (
            "Nepal is one of the largest sources of migrant workers in Qatar, "
            "with Nepali nationals throughout construction, hospitality, and "
            "domestic services. Deaths of Nepali nationals in Qatar trigger a "
            "specific overseas worker repatriation process. The Embassy of Nepal "
            "in Doha handles all such cases. When a Nepali national dies in Qatar, "
            "the sponsoring employer (under the kafala system) notifies both the "
            "Ministry of Interior Civil Status Affairs Department and the Embassy "
            "of Nepal in Doha. Qatar is not a Hague Apostille Convention member; "
            "the Embassy of Nepal in Doha coordinates the overseas death "
            "registration and issues a No Objection Certificate for repatriation. "
            "All documents are in Arabic and require certified Nepali translation. "
            "Tribhuvan International Airport (KTM) in Kathmandu is Nepal's only "
            "international airport. "
            "(Embassy of Nepal, Doha; Government of Nepal Ministry of Home "
            "Affairs, 2025; Qatar Ministry of Interior, 2025.)"
        ),
    },
    {
        'origin': 'kuwait', 'dest': 'nepal',
        'embassy_city': 'Kuwait City',
        'intro': (
            "Nepal provides a significant proportion of Kuwait's migrant labour "
            "force, with Nepali nationals working across construction, hospitality, "
            "and domestic services. When a Nepali national dies in Kuwait, the "
            "sponsoring employer notifies the Civil Affairs Department of the "
            "Ministry of Interior and the Embassy of Nepal in Kuwait City. The "
            "Embassy of Nepal in Kuwait City coordinates the repatriation process "
            "with the family. Kuwait is not a Hague Apostille Convention member; "
            "full consular authentication through the Embassy of Nepal in Kuwait "
            "City is required. All documents are in Arabic and require certified "
            "Nepali translation. Tribhuvan International Airport (KTM) in "
            "Kathmandu is Nepal's only international airport for repatriated "
            "remains. "
            "(Embassy of Nepal, Kuwait; Government of Nepal Ministry of Home "
            "Affairs, 2025; Kuwait Ministry of Interior, 2025.)"
        ),
    },
    # R85 -- Ethiopia x5
    {
        'origin': 'australia', 'dest': 'ethiopia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has development partnership ties with Ethiopia and an "
            "established Ethiopian-Australian community concentrated in Melbourne "
            "and Sydney. The Ethiopian Embassy in Canberra is fully operational. "
            "When an Ethiopian national dies in Australia and their family wishes "
            "to repatriate remains to Ethiopia, the death is registered with the "
            "state or territory Births, Deaths and Marriages (BDM) registry. "
            "Addis Ababa Bole International Airport (ADD) receives all repatriated "
            "remains. Ethiopia is not a Hague Apostille Convention member; full "
            "consular authentication through the Ethiopian Embassy in Canberra is "
            "required. All documents require certified Amharic translation for "
            "VERA, Ethiopia's civil events registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'ethiopia',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts one of the world's largest Ethiopian diaspora communities, "
            "concentrated in Toronto, Ottawa, and Calgary. The Ethiopian Embassy "
            "in Ottawa is fully operational. When an Ethiopian national dies in "
            "Canada and their family wishes to repatriate remains to Ethiopia, the "
            "death is registered with the provincial civil registration authority. "
            "Addis Ababa Bole International Airport (ADD) receives all repatriated "
            "remains. Ethiopia is not a Hague Apostille Convention member; full "
            "consular authentication through the Ethiopian Embassy in Ottawa is "
            "required. All documents require certified Amharic translation for "
            "VERA, Ethiopia's civil events registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'ethiopia',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Ethiopia have long-standing development cooperation ties, "
            "with Norwegian NGOs and aid organisations active in Ethiopia. An "
            "Ethiopian community is established in Oslo. The Ethiopian Embassy in "
            "Oslo is fully operational. When an Ethiopian national dies in Norway "
            "and their family wishes to repatriate remains to Ethiopia, the death "
            "is registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). Addis Ababa Bole International Airport "
            "(ADD) receives all repatriated remains. Ethiopia is not a Hague "
            "Apostille Convention member; full consular authentication through the "
            "Ethiopian Embassy in Oslo is required. All documents require certified "
            "Amharic translation for VERA, Ethiopia's civil events registration "
            "authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'ethiopia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Ethiopia have active development cooperation ties, and an "
            "Ethiopian community is established in Stockholm, Gothenburg, and "
            "Malmo. The Ethiopian Embassy in Stockholm is fully operational. When "
            "an Ethiopian national dies in Sweden and their family wishes to "
            "repatriate remains to Ethiopia, the death is registered with the "
            "Swedish Tax Agency (Skatteverket) Population Register. Addis Ababa "
            "Bole International Airport (ADD) receives all repatriated remains. "
            "Ethiopia is not a Hague Apostille Convention member; full consular "
            "authentication through the Ethiopian Embassy in Stockholm is required. "
            "All documents require certified Amharic translation for VERA, "
            "Ethiopia's civil events registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'ethiopia',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa and Ethiopia have significant bilateral ties as two of "
            "Africa's major economies, and an Ethiopian community is established "
            "in Johannesburg and Cape Town. The Ethiopian Embassy in Pretoria is "
            "fully operational. When an Ethiopian national dies in South Africa "
            "and their family wishes to repatriate remains to Ethiopia, the death "
            "is registered with the Department of Home Affairs under the Births, "
            "Deaths and Marriages Act. Addis Ababa Bole International Airport "
            "(ADD) receives all repatriated remains. South Africa is a Hague "
            "Apostille Convention member; Ethiopia is not, so full consular "
            "authentication through the Ethiopian Embassy in Pretoria is required "
            "for South African documents. All documents require certified Amharic "
            "translation for VERA, Ethiopia's civil events registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; South African "
            "Department of Home Affairs, 2025.)"
        ),
    },
    # R85 -- Sri Lanka x5
    {
        'origin': 'australia', 'dest': 'sri-lanka',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Sri Lankan-Australian community, with nationals "
            "concentrated in Sydney and Melbourne working in healthcare, "
            "professional services, and trade. The Sri Lanka High Commission in "
            "Canberra is fully operational. When a Sri Lankan national dies in "
            "Australia and their family wishes to repatriate remains to Sri Lanka, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Bandaranaike International Airport "
            "(CMB) in Colombo receives all repatriated remains. Sri Lanka is not "
            "a Hague Apostille Convention member; full consular authentication "
            "through the Sri Lanka High Commission in Canberra is required. All "
            "documents require certified Sinhala or Tamil translation for the "
            "Registrar General's Department. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'sri-lanka',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a substantial Sri Lankan-Canadian community, concentrated "
            "in Toronto, Ottawa, and Vancouver working in professional services and "
            "healthcare. The Sri Lanka High Commission in Ottawa is fully "
            "operational. When a Sri Lankan national dies in Canada and their "
            "family wishes to repatriate remains to Sri Lanka, the death is "
            "registered with the provincial civil registration authority. "
            "Bandaranaike International Airport (CMB) in Colombo receives all "
            "repatriated remains. Sri Lanka is not a Hague Apostille Convention "
            "member; full consular authentication through the Sri Lanka High "
            "Commission in Ottawa is required. All documents require certified "
            "Sinhala or Tamil translation for the Registrar General's Department. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'sri-lanka',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Sri Lankan community, with nationals established in "
            "Paris in services and trade. The Sri Lanka Embassy in Paris is fully "
            "operational. When a Sri Lankan national dies in France and their "
            "family wishes to repatriate remains to Sri Lanka, the death is "
            "registered with the local mairie (town hall). Bandaranaike "
            "International Airport (CMB) in Colombo receives all repatriated "
            "remains. The acte de deces requires certified Sinhala or Tamil "
            "translation for the Registrar General's Department in Sri Lanka. "
            "Sri Lanka is not a Hague Apostille Convention member; full consular "
            "authentication through the Sri Lanka Embassy in Paris is required "
            "for French documents. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'india', 'dest': 'sri-lanka',
        'embassy_city': 'New Delhi',
        'intro': (
            "India and Sri Lanka are close neighbours with deep historical, "
            "cultural, and diaspora ties, particularly between Tamil communities "
            "in Tamil Nadu and Sri Lanka's Northern Province. When a Sri Lankan "
            "national dies in India and their family wishes to repatriate remains "
            "to Sri Lanka, the death is registered with the local Registrar of "
            "Births and Deaths under the state civil registration system. "
            "Bandaranaike International Airport (CMB) in Colombo receives most "
            "repatriated remains. Sri Lanka is not a Hague Apostille Convention "
            "member; full consular authentication through the Sri Lanka High "
            "Commission in New Delhi is required. All documents require certified "
            "Sinhala or Tamil translation for the Registrar General's Department. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'sri-lanka',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a Sri Lankan community, with nationals established across "
            "Rome and Milan in hospitality, catering, and domestic services. The "
            "Sri Lanka Embassy in Rome is fully operational. When a Sri Lankan "
            "national dies in Italy and their family wishes to repatriate remains "
            "to Sri Lanka, the death is registered with the local comune (civil "
            "registry). Bandaranaike International Airport (CMB) in Colombo "
            "receives all repatriated remains. The atto di morte requires certified "
            "Sinhala or Tamil translation for the Registrar General's Department "
            "in Sri Lanka. Sri Lanka is not a Hague Apostille Convention member; "
            "full consular authentication through the Sri Lanka Embassy in Rome "
            "is required for Italian documents. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Italian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    # R85 -- Brazil x5
    {
        'origin': 'australia', 'dest': 'brazil',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Brazil maintain bilateral diplomatic ties and a growing "
            "Brazilian-Australian community is established in Sydney and Melbourne. "
            "The Brazilian Embassy in Canberra is fully operational. When a "
            "Brazilian national dies in Australia and their family wishes to "
            "repatriate remains to Brazil, the death is registered with the state "
            "or territory Births, Deaths and Marriages (BDM) registry. Guarulhos "
            "International Airport (GRU) in Sao Paulo or Galeao International "
            "Airport (GIG) in Rio de Janeiro receives repatriated remains. Brazil "
            "joined the Hague Apostille Convention in 2016; Australia joined in "
            "1995. Both countries are Hague members, which simplifies document "
            "authentication. ANVISA (the Brazilian National Health Surveillance "
            "Agency) clearance is required for all incoming human remains. "
            "(Brazilian Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'brazil',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a growing Brazilian-Canadian community, with nationals "
            "concentrated in Toronto and Vancouver working in professional services "
            "and technology. The Brazilian Consulate in Toronto and Embassy in "
            "Ottawa are fully operational. When a Brazilian national dies in Canada "
            "and their family wishes to repatriate remains to Brazil, the death is "
            "registered with the provincial civil registration authority. Guarulhos "
            "International Airport (GRU) in Sao Paulo or Galeao (GIG) in Rio de "
            "Janeiro receives the remains. Brazil joined the Hague Apostille "
            "Convention in 2016; Canada joined in November 2024. Both countries "
            "are now Hague members, simplifying document authentication. ANVISA "
            "clearance is required for all incoming remains. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'brazil',
        'embassy_city': 'Paris',
        'intro': (
            "France and Brazil share close historical and cultural ties, and a "
            "significant Brazilian community is established in Paris. The Brazilian "
            "Embassy in Paris is fully operational. When a Brazilian national dies "
            "in France and their family wishes to repatriate remains to Brazil, the "
            "death is registered with the local mairie (town hall). Guarulhos "
            "International Airport (GRU) in Sao Paulo or Galeao (GIG) in Rio de "
            "Janeiro receives the remains. Both countries are Hague Apostille "
            "members; apostille certificates are accepted, which reduces "
            "authentication requirements. ANVISA clearance is required for all "
            "incoming remains. The acte de deces requires certified Portuguese "
            "translation for Brazilian authorities. "
            "(Brazilian Ministry of Foreign Affairs, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'brazil',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Brazil share a language and deep historical ties; "
            "nationals travel frequently between the two countries, and family "
            "connections are common. The Brazilian Embassy in Lisbon is fully "
            "operational. When a Brazilian national dies in Portugal and their "
            "family wishes to repatriate remains to Brazil, the death is registered "
            "with the local Conservatoria do Registo Civil. Guarulhos International "
            "Airport (GRU) in Sao Paulo or Galeao (GIG) in Rio de Janeiro receives "
            "the remains. Portugal joined the Hague Apostille Convention in 1970; "
            "Brazil joined in 2016. Both are Hague members. ANVISA clearance is "
            "required for all incoming remains. The assento de obito is accepted "
            "in Portuguese by Brazilian authorities. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Portuguese Ministry "
            "of Justice, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'brazil',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a Brazilian community, with nationals working in "
            "Amsterdam and Rotterdam in technology and services. The Brazilian "
            "Consulate General in Amsterdam is fully operational. When a Brazilian "
            "national dies in the Netherlands and their family wishes to repatriate "
            "remains to Brazil, the death is registered with the local gemeente "
            "(municipal civil registry). Both countries are Hague Apostille members; "
            "the Netherlands joined in 1960, Brazil in 2016. ANVISA clearance is "
            "required for all incoming remains. The akte van overlijden requires "
            "certified Portuguese translation for Brazilian authorities. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    # R86 -- Mexico x5
    {
        'origin': 'australia', 'dest': 'mexico',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Mexico maintain bilateral diplomatic ties, with Australian "
            "nationals visiting Mexico for tourism, business, and academic exchange. "
            "The Mexican Embassy in Canberra is fully operational. When an Australian "
            "national dies in Mexico and their family wishes to repatriate remains "
            "to Australia, the death is registered with the local Registro Civil "
            "(Civil Registry Office). SEMEFO (Forensic Medical Service) takes "
            "jurisdiction for violent or unexplained deaths. Benito Juarez "
            "International Airport (MEX) in Mexico City is the main cargo gateway. "
            "Mexico is a Hague Apostille Convention member; Australia joined in "
            "1995. Both are Hague members, which simplifies document authentication. "
            "(DFAT Travel Advice: Mexico, 2025; Mexican Secretariat of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'mexico',
        'embassy_city': 'Paris',
        'intro': (
            "France and Mexico share close diplomatic and cultural ties, with French "
            "nationals established in Mexico City and Guadalajara in business and "
            "cultural roles. The French Embassy in Mexico City is fully operational. "
            "When a French national dies in Mexico and their family wishes to "
            "repatriate remains to France, the death is registered with the local "
            "Registro Civil (Civil Registry). SEMEFO (Forensic Medical Service) "
            "takes jurisdiction for violent or unexplained deaths. Benito Juarez "
            "International Airport (MEX) or Guadalajara International Airport "
            "(GDL) handles cargo departures. Mexico is a Hague Apostille Convention "
            "member; France joined in 1960. Both are Hague members. "
            "(French Ministry of Foreign Affairs, 2025; Mexican Secretariat "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'mexico',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Mexico have cultural and historical ties, with an "
            "Italian-Mexican community established in Mexico City and Guadalajara. "
            "The Italian Embassy in Mexico City is fully operational. When an "
            "Italian national dies in Mexico and their family wishes to repatriate "
            "remains to Italy, the death is registered with the local Registro "
            "Civil (Civil Registry). SEMEFO (Forensic Medical Service) takes "
            "jurisdiction for violent or unexplained deaths. Benito Juarez "
            "International Airport (MEX) or Guadalajara International Airport "
            "(GDL) handles cargo departures. Both Mexico and Italy are Hague "
            "Apostille Convention members, which simplifies document authentication. "
            "All documents in Spanish require certified Italian translation for "
            "Italian authorities. "
            "(Italian Ministry of Foreign Affairs, 2025; Mexican Secretariat "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'mexico',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Mexico maintain bilateral diplomatic relations, with Irish "
            "nationals visiting Mexico for tourism and business. The Irish Embassy "
            "in Mexico City is fully operational. When an Irish national dies in "
            "Mexico and their family wishes to repatriate remains to Ireland, the "
            "death is registered with the local Registro Civil (Civil Registry). "
            "SEMEFO (Forensic Medical Service) takes jurisdiction for violent or "
            "unexplained deaths. Benito Juarez International Airport (MEX) handles "
            "most cargo departures. Both Ireland and Mexico are Hague Apostille "
            "Convention members, which reduces authentication requirements. The "
            "Irish Embassy in Mexico City is the primary contact for Irish families; "
            "the FCDO can also provide consular assistance if required. "
            "(Irish Department of Foreign Affairs, 2025; Mexican Secretariat "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'mexico',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Mexico maintain active trade relations, with Dutch "
            "nationals working in Mexico in agribusiness, logistics, and financial "
            "services. The Dutch Embassy in Mexico City is fully operational. When "
            "a Dutch national dies in Mexico and their family wishes to repatriate "
            "remains to the Netherlands, the death is registered with the local "
            "Registro Civil (Civil Registry). SEMEFO (Forensic Medical Service) "
            "takes jurisdiction for violent or unexplained deaths. Benito Juarez "
            "International Airport (MEX) handles most cargo departures. Both the "
            "Netherlands and Mexico are Hague Apostille Convention members, which "
            "simplifies document authentication. The akte van overlijden requires "
            "certified Spanish translation for Mexican authorities. "
            "(Netherlands Ministry of Foreign Affairs, 2025; Mexican Secretariat "
            "of Foreign Affairs, 2025.)"
        ),
    },
    # R86 -- Colombia x5
    {
        'origin': 'australia', 'dest': 'colombia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Colombian-Australian community, with nationals "
            "concentrated in Sydney and Melbourne. The Colombian Embassy in "
            "Canberra is fully operational. When a Colombian national dies in "
            "Australia and their family wishes to repatriate remains to Colombia, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. El Dorado International Airport (BOG) "
            "in Bogota is the main receiving airport. Colombia is a Hague Apostille "
            "Convention member; Australia joined in 1995. Both are Hague members, "
            "simplifying document authentication. The Instituto Nacional de Medicina "
            "Legal (Medicina Legal) takes jurisdiction for violent or unexplained "
            "deaths. "
            "(Colombian Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'colombia',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada is home to one of the largest Colombian diaspora communities, "
            "concentrated in Toronto and Vancouver. The Colombian Consulate in "
            "Toronto and Embassy in Ottawa are fully operational. When a Colombian "
            "national dies in Canada and their family wishes to repatriate remains "
            "to Colombia, the death is registered with the provincial civil "
            "registration authority. El Dorado International Airport (BOG) in "
            "Bogota is the main receiving airport. Colombia is a Hague Apostille "
            "Convention member; Canada joined in November 2024. Both countries "
            "are now Hague members, which simplifies document authentication. "
            "(Colombian Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'colombia',
        'embassy_city': 'Paris',
        'intro': (
            "France and Colombia maintain bilateral ties through trade and cultural "
            "partnerships, and a Colombian community is established in Paris. The "
            "Colombian Embassy in Paris is fully operational. When a Colombian "
            "national dies in France and their family wishes to repatriate remains "
            "to Colombia, the death is registered with the local mairie (town "
            "hall). El Dorado International Airport (BOG) in Bogota is the main "
            "receiving airport. Both France and Colombia are Hague Apostille "
            "Convention members, which simplifies document authentication. The "
            "acte de deces requires certified Spanish translation for Colombian "
            "authorities. "
            "(Colombian Ministry of Foreign Affairs, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'colombia',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has an active Colombian community, with nationals "
            "working in Rotterdam and Amsterdam in trade, logistics, and services. "
            "The Colombian Embassy in The Hague is fully operational. When a "
            "Colombian national dies in the Netherlands and their family wishes "
            "to repatriate remains to Colombia, the death is registered with the "
            "local gemeente (municipal civil registry). El Dorado International "
            "Airport (BOG) in Bogota is the main receiving airport. Both the "
            "Netherlands and Colombia are Hague Apostille Convention members, "
            "which simplifies document authentication. The akte van overlijden "
            "requires certified Spanish translation for Colombian authorities. "
            "(Colombian Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'colombia',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Colombia share Iberian heritage and cultural connections, "
            "and an active Portuguese-Colombian community maintains bilateral ties. "
            "The Colombian Embassy in Lisbon is fully operational. When a Colombian "
            "national dies in Portugal and their family wishes to repatriate remains "
            "to Colombia, the death is registered with the local Conservatoria do "
            "Registo Civil. El Dorado International Airport (BOG) in Bogota is "
            "the main receiving airport. Both Portugal and Colombia are Hague "
            "Apostille Convention members, which simplifies document authentication. "
            "The assento de obito requires certified Spanish translation for "
            "Colombian authorities. "
            "(Colombian Ministry of Foreign Affairs, 2025; Portuguese Ministry "
            "of Justice, 2025.)"
        ),
    },
    # R86 -- Jordan x5
    {
        'origin': 'australia', 'dest': 'jordan',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals travel to Jordan for tourism, to visit Petra "
            "and Wadi Rum, and for academic and development work. A "
            "Jordanian-Australian community is established across Sydney and "
            "Melbourne. The Australian Embassy in Amman is fully operational. "
            "When an Australian national dies in Jordan and their family wishes "
            "to repatriate remains to Australia, the death is registered with "
            "the Civil Status Department of the Ministry of Interior. Queen Alia "
            "International Airport (AMM) handles cargo departures. Jordan is not "
            "a Hague Apostille Convention member; Australian documents require "
            "full authentication by the Jordanian Embassy in Canberra. All "
            "documents require certified Arabic translation. Islamic law procedures "
            "apply for Muslim remains. "
            "(DFAT Travel Advice: Jordan, 2025; Jordanian Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'jordan',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has an established Jordanian community, with nationals and "
            "their families settled across Berlin, Cologne, and Hamburg. The "
            "Jordanian Embassy in Berlin is fully operational. When a Jordanian "
            "national dies in Germany and their family wishes to repatriate remains "
            "to Jordan, the death is registered with the local Standesamt (civil "
            "registry). Queen Alia International Airport (AMM) receives the remains. "
            "The Sterbeurkunde requires certified Arabic translation for the Civil "
            "Status Department in Jordan. Jordan is not a Hague Apostille Convention "
            "member; German documents require full consular authentication through "
            "the Jordanian Embassy in Berlin. Islamic law procedures apply for "
            "Muslim remains; prompt burial is expected. "
            "(Jordanian Ministry of Foreign Affairs, 2025; German Federal "
            "Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'jordan',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a Jordanian community, with nationals working "
            "in Amsterdam and The Hague in trade and services. The Jordanian "
            "Embassy in The Hague is fully operational. When a Jordanian national "
            "dies in the Netherlands and their family wishes to repatriate remains "
            "to Jordan, the death is registered with the local gemeente (municipal "
            "civil registry). Queen Alia International Airport (AMM) receives the "
            "remains. The akte van overlijden requires certified Arabic translation "
            "for the Civil Status Department in Jordan. Jordan is not a Hague "
            "Apostille Convention member; Dutch documents require full consular "
            "authentication through the Jordanian Embassy in The Hague. Islamic "
            "law procedures apply for Muslim remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'jordan',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a Jordanian community, with nationals established in "
            "Stockholm and other Swedish cities. The Jordanian Embassy in "
            "Stockholm is fully operational. When a Jordanian national dies in "
            "Sweden and their family wishes to repatriate remains to Jordan, the "
            "death is registered with the Swedish Tax Agency (Skatteverket) "
            "Population Register. Queen Alia International Airport (AMM) receives "
            "the remains. The dodsfallsintyg requires certified Arabic translation "
            "for the Civil Status Department in Jordan. Jordan is not a Hague "
            "Apostille Convention member; Swedish documents require full consular "
            "authentication through the Jordanian Embassy in Stockholm. Islamic "
            "law procedures apply for Muslim remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'india', 'dest': 'jordan',
        'embassy_city': 'New Delhi',
        'intro': (
            "India and Jordan have bilateral ties through trade, development "
            "cooperation, and a sizeable Indian community working in Amman in "
            "information technology, engineering, and commerce. The Jordanian "
            "Embassy in New Delhi is fully operational. When an Indian national "
            "dies in Jordan and their family wishes to repatriate remains to India, "
            "the death is registered with the Civil Status Department of the "
            "Ministry of Interior. Queen Alia International Airport (AMM) handles "
            "cargo departures for Indian routes. Jordan is not a Hague Apostille "
            "Convention member; Indian documents require full consular authentication "
            "by the Jordanian Embassy in New Delhi. All documents require certified "
            "Arabic translation. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Indian Ministry "
            "of External Affairs, 2025.)"
        ),
    },
    # R86 -- Algeria x5
    {
        'origin': 'united-kingdom', 'dest': 'algeria',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom has an Algerian-British community, and Algeria "
            "is a significant origin country for families settled in Britain. "
            "The British Embassy in Algiers is fully operational. When an Algerian "
            "national dies in the United Kingdom and their family wishes to "
            "repatriate remains to Algeria, the death must be registered at the "
            "local register office within 5 days. Houari Boumediene International "
            "Airport (ALG) in Algiers handles most repatriated remains. The United "
            "Kingdom is a Hague Apostille Convention member; Algeria is not, so "
            "the Algerian Consulate General in London must authenticate UK documents. "
            "All documents require certified Arabic translation for the Algerian "
            "etat civil (civil registry). Remains must arrive in a hermetically "
            "sealed coffin. "
            "(FCDO Travel Advice: Algeria, 2025; Algerian Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'algeria',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has an Algerian-American community, with nationals "
            "established across New York, Los Angeles, and other major cities. "
            "The Algerian Embassy in Washington DC is fully operational. When an "
            "Algerian national dies in the United States and their family wishes "
            "to repatriate remains to Algeria, the death is registered with the "
            "state civil records office. Houari Boumediene International Airport "
            "(ALG) in Algiers is the main receiving airport. The United States "
            "is a Hague Apostille Convention member; Algeria is not, so full "
            "consular authentication by the Algerian Embassy in Washington DC is "
            "required for US documents. All documents require certified Arabic "
            "translation for the Algerian etat civil. "
            "(Algerian Ministry of Foreign Affairs, 2025; US Department of "
            "State, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'algeria',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has an Algerian community, with nationals established in "
            "Sydney and Melbourne. The Algerian Embassy in Canberra is fully "
            "operational. When an Algerian national dies in Australia and their "
            "family wishes to repatriate remains to Algeria, the death is "
            "registered with the state or territory Births, Deaths and Marriages "
            "(BDM) registry. Houari Boumediene International Airport (ALG) in "
            "Algiers is the main receiving airport. Australia is a Hague Apostille "
            "Convention member; Algeria is not, so full consular authentication "
            "by the Algerian Embassy in Canberra is required for Australian "
            "documents. All documents require certified Arabic translation for "
            "the Algerian etat civil. Remains must arrive in a hermetically "
            "sealed coffin. "
            "(Algerian Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'algeria',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has an active Algerian-Canadian community, concentrated in "
            "Montreal and other Quebec cities where French-language ties are "
            "strong. The Algerian Consulate in Montreal and Embassy in Ottawa "
            "are fully operational. When an Algerian national dies in Canada "
            "and their family wishes to repatriate remains to Algeria, the death "
            "is registered with the provincial civil registration authority. "
            "Houari Boumediene International Airport (ALG) in Algiers is the "
            "main receiving airport. Canada joined the Hague Apostille Convention "
            "in November 2024; Algeria is not a member, so full consular "
            "authentication by the Algerian Embassy in Ottawa is required. All "
            "documents require certified Arabic translation for the Algerian "
            "etat civil. "
            "(Algerian Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'algeria',
        'embassy_city': 'Rome',
        'intro': (
            "Italy is home to a significant Algerian community, with nationals "
            "working across northern Italian cities including Milan and Turin in "
            "manufacturing, construction, and services. The Algerian Embassy in "
            "Rome is fully operational. When an Algerian national dies in Italy "
            "and their family wishes to repatriate remains to Algeria, the death "
            "is registered with the local comune (civil registry). Houari "
            "Boumediene International Airport (ALG) in Algiers is the main "
            "receiving airport. Italy is a Hague Apostille Convention member; "
            "Algeria is not, so full consular authentication by the Algerian "
            "Embassy in Rome is required for Italian documents. The atto di morte "
            "requires certified Arabic translation for the Algerian etat civil. "
            "(Algerian Ministry of Foreign Affairs, 2025; Italian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    # R86 -- Argentina x5
    {
        'origin': 'australia', 'dest': 'argentina',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has an Argentine-Australian community, with nationals "
            "established in Sydney and Melbourne. The Argentine Embassy in "
            "Canberra is fully operational. When an Argentine national dies in "
            "Australia and their family wishes to repatriate remains to Argentina, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Ministro Pistarini International "
            "Airport (EZE) in Buenos Aires is the main receiving airport. "
            "Argentina joined the Hague Apostille Convention in 1987; Australia "
            "joined in 1995. Both are Hague members, which simplifies document "
            "authentication. The Cuerpo Medico Forense (Forensic Medical Corps) "
            "takes jurisdiction for violent or unexplained deaths. "
            "(Argentine Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'argentina',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has an Argentine-Canadian community, with nationals working "
            "in Toronto and Vancouver. The Argentine Embassy in Ottawa is fully "
            "operational. When an Argentine national dies in Canada and their "
            "family wishes to repatriate remains to Argentina, the death is "
            "registered with the provincial civil registration authority. "
            "Ministro Pistarini International Airport (EZE) in Buenos Aires is "
            "the main receiving airport. Argentina joined the Hague Apostille "
            "Convention in 1987; Canada joined in November 2024. Both are now "
            "Hague members, which simplifies document authentication. The Cuerpo "
            "Medico Forense (Forensic Medical Corps) takes jurisdiction for "
            "violent or unexplained deaths. "
            "(Argentine Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'argentina',
        'embassy_city': 'Paris',
        'intro': (
            "France and Argentina share close cultural and historical ties, with "
            "a significant French-Argentine community and France among the leading "
            "European investors in Argentina. The French Embassy in Buenos Aires "
            "is fully operational. When a French national dies in Argentina and "
            "their family wishes to repatriate remains to France, the death is "
            "registered with the local Registro Civil Provincial. Ministro "
            "Pistarini International Airport (EZE) in Buenos Aires handles cargo "
            "departures. Both France and Argentina are Hague Apostille Convention "
            "members, which simplifies document authentication. The Cuerpo Medico "
            "Forense (Forensic Medical Corps) takes jurisdiction for violent or "
            "unexplained deaths. "
            "(French Ministry of Foreign Affairs, 2025; Argentine Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'argentina',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Argentina maintain bilateral trade relations, "
            "with Dutch agribusiness investment significant in the Argentine "
            "agricultural sector. The Dutch Embassy in Buenos Aires is fully "
            "operational. When a Dutch national dies in Argentina and their "
            "family wishes to repatriate remains to the Netherlands, the death "
            "is registered with the local Registro Civil Provincial. Ministro "
            "Pistarini International Airport (EZE) in Buenos Aires handles cargo "
            "departures. Both the Netherlands and Argentina are Hague Apostille "
            "Convention members, which simplifies document authentication. Spanish "
            "documents require certified Dutch translation for Dutch authorities. "
            "The Cuerpo Medico Forense takes jurisdiction for violent or "
            "unexplained deaths. "
            "(Netherlands Ministry of Foreign Affairs, 2025; Argentine Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'argentina',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Argentina share Iberian heritage and historical ties, "
            "with historical migration creating connections between the two "
            "communities. The Portuguese Embassy in Buenos Aires is fully "
            "operational. When a Portuguese national dies in Argentina and their "
            "family wishes to repatriate remains to Portugal, the death is "
            "registered with the local Registro Civil Provincial. Ministro "
            "Pistarini International Airport (EZE) in Buenos Aires handles cargo "
            "departures. Both Portugal and Argentina are Hague Apostille Convention "
            "members, which simplifies document authentication. The Cuerpo Medico "
            "Forense takes jurisdiction for violent or unexplained deaths. "
            "(Portuguese Ministry of Justice, 2025; Argentine Ministry of Foreign "
            "Affairs, 2025.)"
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
            f"Contact the {dest_name} Embassy in Dublin "
            f"for documentation requirements. They cannot fund repatriation."
        )
        step1_timing = (
            "Day of death. Call 999 or 112 for emergency services. "
            f"Contact the {dest_name} Embassy in Dublin."
        )
        step3_action = f"{dest_name} Embassy in Dublin notified"
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
