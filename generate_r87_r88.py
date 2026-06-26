#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R87-R88.

   R87 (25 routes, START_VARIANT=2=C):
     Philippines x5: netherlands, spain, portugal, norway, sweden
     Nepal x5:       netherlands, norway, sweden, south-africa, united-arab-emirates
     Ethiopia x5:    netherlands, ireland, india, spain, portugal
     Sri Lanka x5:   united-states, ireland, portugal, spain, united-arab-emirates
     Brazil x5:      ireland, norway, sweden, switzerland, belgium

   R88 (25 routes, continues from R87):
     Mexico x5:      norway, sweden, switzerland, belgium, portugal
     Jordan x5:      ireland, south-africa, norway, switzerland, spain
     Colombia x5:    ireland, norway, sweden, switzerland, belgium
     Algeria x5:     ireland, norway, sweden, portugal, south-africa
     Argentina x5:   ireland, norway, sweden, switzerland, belgium

   Template rotation: R86 ended on variant B (idx=1). R87 starts at C (idx=2).
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
    'spain': {
        'name': 'Spain',
        'emergency': '112',
        'registry': 'the Registro Civil (civil registry office) under the Ministry of Justice',
        'cert_name': 'acta de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The acta de defuncion is registered with the local Registro Civil "
            "(civil registry office). The Fiscal (public prosecutor) takes "
            "jurisdiction for violent or unexplained deaths. Spain is an EU "
            "member and Hague Apostille Convention member (joined 1978)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Spain is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Fiscal)',
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
    'switzerland': {
        'name': 'Switzerland',
        'emergency': '117 (police) / 144 (ambulance) / 112',
        'registry': 'the local Zivilstandsamt (civil registry office, cantonal level)',
        'cert_name': 'Todesurkunde (death certificate)',
        'cert_lang': 'German, French, or Italian (depending on canton)',
        'overview': (
            "Call 117 for police, 144 for ambulance, or 112 for emergency services. "
            "Death is certified by a physician. The Todesurkunde is registered with "
            "the local Zivilstandsamt (civil registry office, cantonal level). The "
            "cantonal police or investigating magistrate take jurisdiction for violent "
            "or unexplained deaths. Switzerland is a Hague Apostille Convention "
            "member (joined 1972)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Switzerland is widely available at authorised facilities "
            "across all major cantons."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (cantonal police or investigating magistrate)',
    },
    'belgium': {
        'name': 'Belgium',
        'emergency': '112 (emergency) / 101 (police)',
        'registry': 'the local commune or gemeenten (civil registry)',
        'cert_name': 'acte de deces or overlijdensakte (death certificate)',
        'cert_lang': 'French or Dutch (depending on region)',
        'overview': (
            "Call 112 for emergency services or 101 for police. Death is certified "
            "by a physician. The acte de deces or overlijdensakte is registered "
            "with the local commune or gemeenten (civil registry). The Procureur "
            "du Roi or Procureur des Konings (public prosecutor) takes jurisdiction "
            "for violent or unexplained deaths. Belgium is an EU member and Hague "
            "Apostille Convention member (joined 1975)."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Belgium is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Procureur du Roi or Procureur des Konings)',
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
    'united-arab-emirates': {
        'name': 'the United Arab Emirates',
        'emergency': '999 (police and ambulance) / 998 (ambulance in some emirates)',
        'registry': (
            'the relevant emirate health authority (Dubai Health Authority in '
            'Dubai, Department of Health in Abu Dhabi)'
        ),
        'cert_name': 'death certificate',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 999 for police and ambulance, or 998 for ambulance in some "
            "emirates. Death is certified by a hospital physician. The death is "
            "registered with the relevant emirate health authority (Dubai Health "
            "Authority in Dubai, Department of Health in Abu Dhabi). Foreign "
            "nationals must have deaths reported by their employer or sponsor; "
            "the deceased's embassy must be notified on the day of death. All "
            "documents are in Arabic and require certified translation. The UAE "
            "is not a Hague Apostille Convention member; full UAE Ministry of "
            "Foreign Affairs authentication is required for all documents. The "
            "public prosecutor takes jurisdiction for violent or unexplained "
            "deaths. Cremation is not available in the UAE for most nationalities."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available in the United Arab Emirates. Repatriation "
            "of the full body is the only option for most families. Contact the "
            "relevant embassy on the day of death to begin the repatriation process."
        ),
        'postmortem_trigger': 'Violent, suspicious, or unexplained deaths (public prosecutor takes jurisdiction)',
    },
}

ROUTES = [
    # R87 -- Philippines x5
    {
        'origin': 'netherlands', 'dest': 'philippines',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has an established Filipino community, with nationals "
            "working in Amsterdam, Rotterdam, and The Hague in healthcare, domestic "
            "services, and international trade. The Philippine Embassy in The Hague "
            "is fully operational. When a Filipino national dies in the Netherlands "
            "and their family wishes to repatriate remains to the Philippines, the "
            "death is registered with the local gemeente (municipal civil registry). "
            "The Philippine Statistics Authority (PSA) requires a Report of Death "
            "(ROD) issued by the Philippine Embassy in The Hague. The akte van "
            "overlijden must be included in all repatriation documentation. The "
            "Philippines is not a Hague Apostille Convention member; Dutch documents "
            "require full consular authentication through the Philippine Embassy in "
            "The Hague. "
            "(Philippine Department of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'philippines',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain has a Filipino community, with nationals working in Madrid and "
            "Barcelona in domestic services, healthcare, and hospitality. The "
            "Philippine Embassy in Madrid is fully operational. When a Filipino "
            "national dies in Spain and their family wishes to repatriate remains "
            "to the Philippines, the death is registered with the local Registro "
            "Civil (civil registry). The Philippine Statistics Authority (PSA) "
            "requires a Report of Death (ROD) issued by the Philippine Embassy in "
            "Madrid. The acta de defuncion must be included in all repatriation "
            "documentation. The Philippines is not a Hague Apostille Convention "
            "member; Spanish documents require full consular authentication through "
            "the Philippine Embassy in Madrid. "
            "(Philippine Department of Foreign Affairs, 2025; Spanish Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'philippines',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal has a Filipino community, with nationals working in Lisbon "
            "and Porto in domestic services and healthcare. The Philippine Embassy "
            "in Lisbon is fully operational. When a Filipino national dies in "
            "Portugal and their family wishes to repatriate remains to the "
            "Philippines, the death is registered with the local Conservatoria do "
            "Registo Civil. The Philippine Statistics Authority (PSA) requires a "
            "Report of Death (ROD) issued by the Philippine Embassy in Lisbon. "
            "The assento de obito must be included in all repatriation documentation. "
            "The Philippines is not a Hague Apostille Convention member; Portuguese "
            "documents require full consular authentication through the Philippine "
            "Embassy in Lisbon. "
            "(Philippine Department of Foreign Affairs, 2025; Portuguese Ministry "
            "of Justice, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'philippines',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway has a Filipino community, with nationals working in Oslo and "
            "other Norwegian cities in healthcare, domestic services, and the "
            "offshore energy sector. The Philippine Embassy in Oslo is fully "
            "operational. When a Filipino national dies in Norway and their family "
            "wishes to repatriate remains to the Philippines, the death is "
            "registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). The Philippine Statistics Authority "
            "(PSA) requires a Report of Death (ROD) issued by the Philippine "
            "Embassy in Oslo. The dodsattest must be included in all repatriation "
            "documentation. The Philippines is not a Hague Apostille Convention "
            "member; Norwegian documents require full consular authentication "
            "through the Philippine Embassy in Oslo. "
            "(Philippine Department of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'philippines',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a Filipino community, with nationals working in Stockholm "
            "and other Swedish cities in healthcare and domestic services. The "
            "Philippine Embassy in Stockholm is fully operational. When a Filipino "
            "national dies in Sweden and their family wishes to repatriate remains "
            "to the Philippines, the death is registered with the Swedish Tax Agency "
            "(Skatteverket) Population Register. The Philippine Statistics Authority "
            "(PSA) requires a Report of Death (ROD) issued by the Philippine Embassy "
            "in Stockholm. The dodsfallsintyg must be included in all repatriation "
            "documentation. The Philippines is not a Hague Apostille Convention "
            "member; Swedish documents require full consular authentication through "
            "the Philippine Embassy in Stockholm. "
            "(Philippine Department of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    # R87 -- Nepal x5
    {
        'origin': 'netherlands', 'dest': 'nepal',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a Nepali community, with nationals working in "
            "The Hague, Amsterdam, and Rotterdam in professional services and "
            "hospitality. The Embassy of Nepal in The Hague is fully operational. "
            "When a Nepali national dies in the Netherlands and their family "
            "wishes to repatriate remains to Nepal, the death is registered with "
            "the local gemeente (municipal civil registry). Tribhuvan International "
            "Airport (KTM) in Kathmandu is Nepal's only international airport; all "
            "repatriated remains arrive there. Nepal is not a Hague Apostille "
            "Convention member; full consular authentication through the Embassy "
            "of Nepal in The Hague is required. A certified Nepali translation of "
            "all documents is required by the Ward Office on arrival. "
            "(Embassy of Nepal, The Hague; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'nepal',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway has a Nepali community, with nationals working in Oslo and "
            "other Norwegian cities, and Norwegian development organisations have "
            "maintained long-standing ties with Nepal. The Embassy of Nepal in "
            "Oslo is fully operational. When a Nepali national dies in Norway and "
            "their family wishes to repatriate remains to Nepal, the death is "
            "registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). Tribhuvan International Airport (KTM) "
            "in Kathmandu is Nepal's only international airport. The dodsattest "
            "requires certified Nepali translation for the Ward Office in Nepal. "
            "Nepal is not a Hague Apostille Convention member; full consular "
            "authentication through the Embassy of Nepal in Oslo is required. "
            "(Embassy of Nepal, Oslo; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'nepal',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a Nepali community, with nationals working in Stockholm "
            "and Gothenburg, and Swedish development partnerships with Nepal have "
            "created ongoing bilateral connections. The Embassy of Nepal in "
            "Stockholm is fully operational. When a Nepali national dies in Sweden "
            "and their family wishes to repatriate remains to Nepal, the death is "
            "registered with the Swedish Tax Agency (Skatteverket) Population "
            "Register. Tribhuvan International Airport (KTM) in Kathmandu is "
            "Nepal's only international airport. The dodsfallsintyg requires "
            "certified Nepali translation for the Ward Office in Nepal. Nepal is "
            "not a Hague Apostille Convention member; full consular authentication "
            "through the Embassy of Nepal in Stockholm is required. "
            "(Embassy of Nepal, Stockholm; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'nepal',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa and Nepal have connections through the United Nations "
            "and humanitarian organisations, and a Nepali community is established "
            "in Johannesburg and Pretoria. The Embassy of Nepal in Pretoria is "
            "fully operational. When a Nepali national dies in South Africa and "
            "their family wishes to repatriate remains to Nepal, the death is "
            "registered with the Department of Home Affairs under the Births, "
            "Deaths and Marriages Act. Tribhuvan International Airport (KTM) in "
            "Kathmandu is Nepal's only international airport. South Africa is a "
            "Hague Apostille Convention member; Nepal is not, so full consular "
            "authentication through the Embassy of Nepal in Pretoria is required "
            "for South African documents. All documents require certified Nepali "
            "translation for the Ward Office. "
            "(Embassy of Nepal, Pretoria; Government of Nepal Ministry of Home "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-arab-emirates', 'dest': 'nepal',
        'embassy_city': 'Abu Dhabi',
        'intro': (
            "The UAE hosts one of the largest Nepali migrant worker communities in "
            "the world, with Nepali nationals working across construction, "
            "hospitality, and domestic services throughout Dubai, Abu Dhabi, and "
            "the other emirates. When a Nepali national dies in the UAE, the "
            "sponsoring employer (under the kafala system) must notify the relevant "
            "emirate health authority and the Embassy of Nepal in Abu Dhabi. The "
            "Embassy of Nepal in Abu Dhabi coordinates the repatriation process and "
            "issues a No Objection Certificate for repatriation. The UAE is not a "
            "Hague Apostille Convention member; full UAE Ministry of Foreign Affairs "
            "authentication is required for all documents. All documents are in "
            "Arabic and require certified Nepali translation. Tribhuvan International "
            "Airport (KTM) in Kathmandu receives all repatriated remains. "
            "(Embassy of Nepal, Abu Dhabi; Government of Nepal Ministry of Home "
            "Affairs, 2025; UAE Ministry of Human Resources, 2025.)"
        ),
    },
    # R87 -- Ethiopia x5
    {
        'origin': 'netherlands', 'dest': 'ethiopia',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Ethiopia have active development cooperation ties, "
            "and an Ethiopian community is established in Amsterdam and The Hague. "
            "The Ethiopian Embassy in The Hague is fully operational. When an "
            "Ethiopian national dies in the Netherlands and their family wishes to "
            "repatriate remains to Ethiopia, the death is registered with the local "
            "gemeente (municipal civil registry). Addis Ababa Bole International "
            "Airport (ADD) receives all repatriated remains. Ethiopia is not a "
            "Hague Apostille Convention member; full consular authentication through "
            "the Ethiopian Embassy in The Hague is required. All documents require "
            "certified Amharic translation for VERA, Ethiopia's civil events "
            "registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'ethiopia',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Ethiopia maintain diplomatic relations, and an Ethiopian "
            "community is established in Dublin and other Irish cities. The Ethiopian "
            "Embassy in Dublin is fully operational. When an Ethiopian national dies "
            "in Ireland and their family wishes to repatriate remains to Ethiopia, "
            "the death is registered with the local registrar's office, which "
            "reports to the General Register Office (GRO). Addis Ababa Bole "
            "International Airport (ADD) receives all repatriated remains. Ireland "
            "is a Hague Apostille Convention member; Ethiopia is not, so full "
            "consular authentication through the Ethiopian Embassy in Dublin is "
            "required for Irish documents. All documents require certified Amharic "
            "translation for VERA, Ethiopia's civil events registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Irish Department of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'india', 'dest': 'ethiopia',
        'embassy_city': 'New Delhi',
        'intro': (
            "India and Ethiopia have bilateral trade and diplomatic ties, and Indian "
            "nationals travel to Ethiopia for business, development work, and "
            "investment. The Ethiopian Embassy in New Delhi is fully operational. "
            "When an Indian national dies in Ethiopia and the family wishes to "
            "repatriate remains to India, or when an Ethiopian national dies in "
            "India, the death is registered with the relevant civil registration "
            "authority. Addis Ababa Bole International Airport (ADD) handles cargo "
            "departures for the India route. Ethiopia is not a Hague Apostille "
            "Convention member; Indian documents require full consular authentication "
            "through the Ethiopian Embassy in New Delhi. All documents require "
            "certified Amharic translation for VERA, Ethiopia's civil events "
            "registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Indian Ministry of "
            "External Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'ethiopia',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and Ethiopia have diplomatic and development cooperation ties, "
            "and an Ethiopian community is established in Madrid and Barcelona. "
            "The Ethiopian Embassy in Madrid is fully operational. When an Ethiopian "
            "national dies in Spain and their family wishes to repatriate remains "
            "to Ethiopia, the death is registered with the local Registro Civil "
            "(civil registry). Addis Ababa Bole International Airport (ADD) receives "
            "all repatriated remains. Ethiopia is not a Hague Apostille Convention "
            "member; full consular authentication through the Ethiopian Embassy in "
            "Madrid is required for Spanish documents. All documents require "
            "certified Amharic translation for VERA, Ethiopia's civil events "
            "registration authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Spanish Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'ethiopia',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Ethiopia have diplomatic and historical ties, and an "
            "Ethiopian community is established in Lisbon. The Ethiopian Embassy "
            "in Lisbon is fully operational. When an Ethiopian national dies in "
            "Portugal and their family wishes to repatriate remains to Ethiopia, "
            "the death is registered with the local Conservatoria do Registo Civil. "
            "Addis Ababa Bole International Airport (ADD) receives all repatriated "
            "remains. Ethiopia is not a Hague Apostille Convention member; full "
            "consular authentication through the Ethiopian Embassy in Lisbon is "
            "required for Portuguese documents. All documents require certified "
            "Amharic translation for VERA, Ethiopia's civil events registration "
            "authority. "
            "(Ethiopian Ministry of Foreign Affairs, 2025; Portuguese Ministry "
            "of Justice, 2025.)"
        ),
    },
    # R87 -- Sri Lanka x5
    {
        'origin': 'united-states', 'dest': 'sri-lanka',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Sri Lankan-American community, concentrated "
            "in New York, New Jersey, and Los Angeles. The Sri Lanka Embassy in "
            "Washington DC is fully operational. When a Sri Lankan national dies "
            "in the United States and their family wishes to repatriate remains "
            "to Sri Lanka, the death is registered with the state civil records "
            "office. Bandaranaike International Airport (CMB) in Colombo receives "
            "most repatriated remains. Sri Lanka is not a Hague Apostille Convention "
            "member; full consular authentication through the Sri Lanka Embassy in "
            "Washington DC is required. All documents require certified Sinhala or "
            "Tamil translation for the Registrar General's Department. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; US Department of "
            "State, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'sri-lanka',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland has a Sri Lankan community, with nationals working in Dublin "
            "and other Irish cities in healthcare and professional services. The "
            "Sri Lanka High Commission in Dublin is fully operational. When a Sri "
            "Lankan national dies in Ireland and their family wishes to repatriate "
            "remains to Sri Lanka, the death is registered with the local "
            "registrar's office, which reports to the General Register Office "
            "(GRO). Bandaranaike International Airport (CMB) in Colombo receives "
            "all repatriated remains. Sri Lanka is not a Hague Apostille Convention "
            "member; full consular authentication through the Sri Lanka High "
            "Commission in Dublin is required. All documents require certified "
            "Sinhala or Tamil translation for the Registrar General's Department. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Irish Department of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'sri-lanka',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal has a Sri Lankan community, with nationals working in Lisbon "
            "in hospitality and services. The Sri Lanka Embassy in Lisbon is fully "
            "operational. When a Sri Lankan national dies in Portugal and their "
            "family wishes to repatriate remains to Sri Lanka, the death is "
            "registered with the local Conservatoria do Registo Civil. Bandaranaike "
            "International Airport (CMB) in Colombo receives all repatriated "
            "remains. Sri Lanka is not a Hague Apostille Convention member; full "
            "consular authentication through the Sri Lanka Embassy in Lisbon is "
            "required for Portuguese documents. All documents require certified "
            "Sinhala or Tamil translation for the Registrar General's Department. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Portuguese Ministry "
            "of Justice, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'sri-lanka',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain has a Sri Lankan community, with nationals established in Madrid "
            "and Barcelona in hospitality and trade. The Sri Lanka Embassy in Madrid "
            "is fully operational. When a Sri Lankan national dies in Spain and their "
            "family wishes to repatriate remains to Sri Lanka, the death is registered "
            "with the local Registro Civil (civil registry). Bandaranaike International "
            "Airport (CMB) in Colombo receives all repatriated remains. Sri Lanka is "
            "not a Hague Apostille Convention member; full consular authentication "
            "through the Sri Lanka Embassy in Madrid is required for Spanish documents. "
            "All documents require certified Sinhala or Tamil translation for the "
            "Registrar General's Department. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Spanish Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-arab-emirates', 'dest': 'sri-lanka',
        'embassy_city': 'Abu Dhabi',
        'intro': (
            "The UAE hosts a large Sri Lankan community, with nationals working "
            "across Dubai, Abu Dhabi, and the other emirates in construction, "
            "domestic services, and hospitality. When a Sri Lankan national dies "
            "in the UAE, the sponsoring employer (under the kafala system) notifies "
            "the relevant emirate health authority and the Sri Lanka Embassy in "
            "Abu Dhabi. The Sri Lanka Embassy in Abu Dhabi coordinates the "
            "repatriation process and documentation. The UAE is not a Hague "
            "Apostille Convention member; full UAE Ministry of Foreign Affairs "
            "authentication is required for all documents. All documents are in "
            "Arabic and require certified Sinhala or Tamil translation for the "
            "Registrar General's Department in Sri Lanka. Bandaranaike International "
            "Airport (CMB) in Colombo receives all repatriated remains. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; UAE Ministry of "
            "Human Resources, 2025.)"
        ),
    },
    # R87 -- Brazil x5
    {
        'origin': 'ireland', 'dest': 'brazil',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Brazil maintain bilateral diplomatic relations, with "
            "Brazilian nationals working in Dublin and other Irish cities in "
            "hospitality, technology, and services. The Brazilian Embassy in Dublin "
            "is fully operational. When a Brazilian national dies in Ireland and "
            "their family wishes to repatriate remains to Brazil, the death is "
            "registered with the local registrar's office, which reports to the "
            "General Register Office (GRO). Guarulhos International Airport (GRU) "
            "in Sao Paulo or Galeao International Airport (GIG) in Rio de Janeiro "
            "receives the remains. Ireland joined the Hague Apostille Convention "
            "in 1967; Brazil joined in 2016. Both countries are Hague members, "
            "which simplifies document authentication. ANVISA (the Brazilian "
            "National Health Surveillance Agency) clearance is required for all "
            "incoming remains. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Irish Department of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'brazil',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Brazil have active trade ties, with Norwegian companies "
            "investing in Brazil's offshore energy and maritime sectors, and a "
            "Brazilian community is established in Oslo. The Brazilian Embassy in "
            "Oslo is fully operational. When a Brazilian national dies in Norway "
            "and their family wishes to repatriate remains to Brazil, the death "
            "is registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). Guarulhos International Airport (GRU) "
            "in Sao Paulo or Galeao (GIG) in Rio de Janeiro receives the remains. "
            "Norway is a Hague Apostille Convention member; Brazil joined in 2016. "
            "Both countries are Hague members, which simplifies document "
            "authentication. ANVISA clearance is required for all incoming remains. "
            "The dodsattest requires certified Portuguese translation for Brazilian "
            "authorities. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'brazil',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Brazil have active bilateral ties through trade and "
            "investment, and a Brazilian community is established in Stockholm and "
            "Gothenburg. The Brazilian Embassy in Stockholm is fully operational. "
            "When a Brazilian national dies in Sweden and their family wishes to "
            "repatriate remains to Brazil, the death is registered with the Swedish "
            "Tax Agency (Skatteverket) Population Register. Guarulhos International "
            "Airport (GRU) in Sao Paulo or Galeao (GIG) in Rio de Janeiro receives "
            "the remains. Sweden joined the Hague Apostille Convention in 1999; "
            "Brazil joined in 2016. Both countries are Hague members, which "
            "simplifies document authentication. ANVISA clearance is required for "
            "all incoming remains. The dodsfallsintyg requires certified Portuguese "
            "translation for Brazilian authorities. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'brazil',
        'embassy_city': 'Bern',
        'intro': (
            "Switzerland and Brazil have close bilateral ties through trade, "
            "finance, and the pharmaceutical sector, and a Brazilian community is "
            "established in Zurich and Geneva. The Brazilian Embassy in Bern is "
            "fully operational. When a Brazilian national dies in Switzerland and "
            "their family wishes to repatriate remains to Brazil, the death is "
            "registered with the local Zivilstandsamt (civil registry office, "
            "cantonal level). Guarulhos International Airport (GRU) in Sao Paulo "
            "or Galeao (GIG) in Rio de Janeiro receives the remains. Switzerland "
            "joined the Hague Apostille Convention in 1972; Brazil joined in 2016. "
            "Both countries are Hague members, which simplifies document "
            "authentication. ANVISA clearance is required for all incoming remains. "
            "The Todesurkunde requires certified Portuguese translation for "
            "Brazilian authorities. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Swiss Federal "
            "Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'brazil',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgium has a Brazilian community, with nationals working in Brussels "
            "and Antwerp in services and trade. The Brazilian Embassy in Brussels "
            "is fully operational. When a Brazilian national dies in Belgium and "
            "their family wishes to repatriate remains to Brazil, the death is "
            "registered with the local commune or gemeenten (civil registry). "
            "Guarulhos International Airport (GRU) in Sao Paulo or Galeao (GIG) "
            "in Rio de Janeiro receives the remains. Belgium joined the Hague "
            "Apostille Convention in 1975; Brazil joined in 2016. Both countries "
            "are Hague members, which simplifies document authentication. ANVISA "
            "clearance is required for all incoming remains. The acte de deces or "
            "overlijdensakte requires certified Portuguese translation for Brazilian "
            "authorities. "
            "(Brazilian Ministry of Foreign Affairs, 2025; Belgian Federal "
            "Public Service Foreign Affairs, 2025.)"
        ),
    },
    # R88 -- Mexico x5
    {
        'origin': 'norway', 'dest': 'mexico',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Mexico maintain bilateral diplomatic relations, with "
            "Norwegian maritime and energy companies active in Mexico, and Mexican "
            "nationals living and working in Oslo. The Mexican Embassy in Oslo is "
            "fully operational. When a Mexican national dies in Norway and their "
            "family wishes to repatriate remains to Mexico, the death is registered "
            "with Folkeregisteret (the civil registration system administered by "
            "Skatteetaten). Benito Juarez International Airport (MEX) in Mexico "
            "City, Guadalajara International Airport (GDL), or Monterrey "
            "International Airport (MTY) receives the remains. Norway is a Hague "
            "Apostille Convention member; Mexico joined in 1995. Both countries are "
            "Hague members, which simplifies document authentication. The dodsattest "
            "requires certified Spanish translation for Mexican authorities. "
            "(Norwegian Ministry of Foreign Affairs, 2025; Mexican Secretariat "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'mexico',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Mexico have active bilateral relations, with Swedish "
            "companies established in Mexico's automotive and energy sectors, and "
            "Mexican nationals living and working in Stockholm. The Mexican Embassy "
            "in Stockholm is fully operational. When a Mexican national dies in "
            "Sweden and their family wishes to repatriate remains to Mexico, the "
            "death is registered with the Swedish Tax Agency (Skatteverket) "
            "Population Register. Benito Juarez International Airport (MEX), "
            "Guadalajara (GDL), or Monterrey (MTY) receives the remains. Sweden "
            "joined the Hague Apostille Convention in 1999; Mexico joined in 1995. "
            "Both countries are Hague members, which simplifies document "
            "authentication. The dodsfallsintyg requires certified Spanish "
            "translation for Mexican authorities. "
            "(Swedish Ministry of Foreign Affairs, 2025; Mexican Secretariat "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'mexico',
        'embassy_city': 'Bern',
        'intro': (
            "Switzerland and Mexico have established trade and diplomatic ties, "
            "with Swiss pharmaceutical and financial companies active in Mexico, "
            "and a Mexican community working in Zurich and Geneva. The Mexican "
            "Embassy in Bern is fully operational. When a Mexican national dies "
            "in Switzerland and their family wishes to repatriate remains to Mexico, "
            "the death is registered with the local Zivilstandsamt (civil registry "
            "office, cantonal level). Benito Juarez International Airport (MEX), "
            "Guadalajara (GDL), or Monterrey (MTY) receives the remains. "
            "Switzerland joined the Hague Apostille Convention in 1972; Mexico "
            "joined in 1995. Both countries are Hague members, which simplifies "
            "document authentication. The Todesurkunde requires certified Spanish "
            "translation for Mexican authorities. "
            "(Swiss Federal Department of Foreign Affairs, 2025; Mexican "
            "Secretariat of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'mexico',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgium and Mexico maintain bilateral diplomatic relations, and Belgian "
            "nationals visit Mexico for business and tourism. The Mexican Embassy in "
            "Brussels is fully operational. When a Mexican national dies in Belgium "
            "and their family wishes to repatriate remains to Mexico, the death is "
            "registered with the local commune or gemeenten (civil registry). Benito "
            "Juarez International Airport (MEX), Guadalajara (GDL), or Monterrey "
            "(MTY) receives the remains. Belgium joined the Hague Apostille "
            "Convention in 1975; Mexico joined in 1995. Both countries are Hague "
            "members, which simplifies document authentication. The acte de deces "
            "or overlijdensakte requires certified Spanish translation for Mexican "
            "authorities. "
            "(Belgian Federal Public Service Foreign Affairs, 2025; Mexican "
            "Secretariat of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'mexico',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Mexico share Iberian heritage and cultural connections, "
            "and a Portuguese community is established in Mexico City. The Mexican "
            "Embassy in Lisbon is fully operational. When a Mexican national dies "
            "in Portugal and their family wishes to repatriate remains to Mexico, "
            "the death is registered with the local Conservatoria do Registo Civil. "
            "Benito Juarez International Airport (MEX), Guadalajara (GDL), or "
            "Monterrey (MTY) receives the remains. Portugal joined the Hague "
            "Apostille Convention in 1970; Mexico joined in 1995. Both countries "
            "are Hague members, which simplifies document authentication. The "
            "assento de obito is accepted in Portuguese by Mexican authorities. "
            "(Portuguese Ministry of Justice, 2025; Mexican Secretariat of "
            "Foreign Affairs, 2025.)"
        ),
    },
    # R88 -- Jordan x5
    {
        'origin': 'ireland', 'dest': 'jordan',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Jordan maintain bilateral diplomatic relations, with Irish "
            "nationals visiting Jordan for tourism and development work, and a "
            "Jordanian community established in Dublin. The Jordanian Embassy in "
            "Dublin is fully operational. When a Jordanian national dies in Ireland "
            "and their family wishes to repatriate remains to Jordan, the death is "
            "registered with the local registrar's office, which reports to the "
            "General Register Office (GRO). Queen Alia International Airport (AMM) "
            "in Amman receives the remains. Ireland is a Hague Apostille Convention "
            "member; Jordan is not, so full consular authentication through the "
            "Jordanian Embassy in Dublin is required for Irish documents. All "
            "documents require certified Arabic translation for the Civil Status "
            "Department in Jordan. Islamic law procedures apply for Muslim remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Irish Department of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'jordan',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa and Jordan have bilateral ties through trade and "
            "diplomatic engagement, and a Jordanian community is established in "
            "Johannesburg and Pretoria. The Jordanian Embassy in Pretoria is fully "
            "operational. When a Jordanian national dies in South Africa and their "
            "family wishes to repatriate remains to Jordan, the death is registered "
            "with the Department of Home Affairs under the Births, Deaths and "
            "Marriages Act. Queen Alia International Airport (AMM) in Amman "
            "receives the remains. South Africa is a Hague Apostille Convention "
            "member; Jordan is not, so full consular authentication through the "
            "Jordanian Embassy in Pretoria is required for South African documents. "
            "All documents require certified Arabic translation for the Civil Status "
            "Department in Jordan. Islamic law procedures apply for Muslim remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025; South African "
            "Department of Home Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'jordan',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Jordan have bilateral ties through development cooperation "
            "and trade, with Norwegian aid organisations active in the region. A "
            "Jordanian community is established in Oslo. The Jordanian Embassy in "
            "Oslo is fully operational. When a Jordanian national dies in Norway "
            "and their family wishes to repatriate remains to Jordan, the death is "
            "registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). Queen Alia International Airport (AMM) "
            "in Amman receives the remains. Norway is a Hague Apostille Convention "
            "member; Jordan is not, so full consular authentication through the "
            "Jordanian Embassy in Oslo is required for Norwegian documents. All "
            "documents require certified Arabic translation for the Civil Status "
            "Department in Jordan. Islamic law procedures apply for Muslim remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'jordan',
        'embassy_city': 'Bern',
        'intro': (
            "Switzerland and Jordan have bilateral ties through trade and diplomatic "
            "engagement at the United Nations in Geneva, with Swiss development "
            "organisations active in the region. A Jordanian community is "
            "established in Geneva and Zurich. The Jordanian Embassy in Bern is "
            "fully operational. When a Jordanian national dies in Switzerland and "
            "their family wishes to repatriate remains to Jordan, the death is "
            "registered with the local Zivilstandsamt (civil registry office, "
            "cantonal level). Queen Alia International Airport (AMM) in Amman "
            "receives the remains. Switzerland is a Hague Apostille Convention "
            "member; Jordan is not, so full consular authentication through the "
            "Jordanian Embassy in Bern is required for Swiss documents. All "
            "documents require certified Arabic translation for the Civil Status "
            "Department in Jordan. Islamic law procedures apply for Muslim remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Swiss Federal "
            "Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'jordan',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and Jordan maintain bilateral diplomatic relations, and a "
            "Jordanian community is established in Madrid and other Spanish cities. "
            "The Jordanian Embassy in Madrid is fully operational. When a Jordanian "
            "national dies in Spain and their family wishes to repatriate remains "
            "to Jordan, the death is registered with the local Registro Civil "
            "(civil registry). Queen Alia International Airport (AMM) in Amman "
            "receives the remains. Spain is a Hague Apostille Convention member; "
            "Jordan is not, so full consular authentication through the Jordanian "
            "Embassy in Madrid is required for Spanish documents. All documents "
            "require certified Arabic translation for the Civil Status Department "
            "in Jordan. Islamic law procedures apply for Muslim remains. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Spanish Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    # R88 -- Colombia x5
    {
        'origin': 'ireland', 'dest': 'colombia',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Colombia maintain bilateral diplomatic relations, with "
            "Colombian nationals living and working in Dublin and other Irish "
            "cities. The Colombian Embassy in Dublin is fully operational. When a "
            "Colombian national dies in Ireland and their family wishes to "
            "repatriate remains to Colombia, the death is registered with the local "
            "registrar's office, which reports to the General Register Office "
            "(GRO). El Dorado International Airport (BOG) in Bogota is the main "
            "receiving airport. Both Ireland and Colombia are Hague Apostille "
            "Convention members, which simplifies document authentication. The "
            "Instituto Nacional de Medicina Legal (Medicina Legal) takes "
            "jurisdiction for violent or unexplained deaths in Colombia. "
            "(Colombian Ministry of Foreign Affairs, 2025; Irish Department of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'colombia',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Colombia have bilateral ties through trade and development "
            "cooperation, and a Colombian community is established in Oslo. The "
            "Colombian Embassy in Oslo is fully operational. When a Colombian "
            "national dies in Norway and their family wishes to repatriate remains "
            "to Colombia, the death is registered with Folkeregisteret (the civil "
            "registration system administered by Skatteetaten). El Dorado "
            "International Airport (BOG) in Bogota is the main receiving airport. "
            "Both Norway and Colombia are Hague Apostille Convention members, which "
            "simplifies document authentication. The dodsattest requires certified "
            "Spanish translation for Colombian authorities. "
            "(Colombian Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'colombia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Colombia have active bilateral ties through trade and "
            "development cooperation, and a Colombian community is established in "
            "Stockholm. The Colombian Embassy in Stockholm is fully operational. "
            "When a Colombian national dies in Sweden and their family wishes to "
            "repatriate remains to Colombia, the death is registered with the "
            "Swedish Tax Agency (Skatteverket) Population Register. El Dorado "
            "International Airport (BOG) in Bogota is the main receiving airport. "
            "Both Sweden and Colombia are Hague Apostille Convention members, which "
            "simplifies document authentication. The dodsfallsintyg requires "
            "certified Spanish translation for Colombian authorities. "
            "(Colombian Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'colombia',
        'embassy_city': 'Bern',
        'intro': (
            "Switzerland and Colombia maintain bilateral relations through trade "
            "and investment, and a Colombian community is established in Geneva "
            "and Zurich. The Colombian Embassy in Bern is fully operational. When "
            "a Colombian national dies in Switzerland and their family wishes to "
            "repatriate remains to Colombia, the death is registered with the local "
            "Zivilstandsamt (civil registry office, cantonal level). El Dorado "
            "International Airport (BOG) in Bogota is the main receiving airport. "
            "Both Switzerland and Colombia are Hague Apostille Convention members, "
            "which simplifies document authentication. The Todesurkunde requires "
            "certified Spanish translation for Colombian authorities. "
            "(Colombian Ministry of Foreign Affairs, 2025; Swiss Federal "
            "Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'colombia',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgium and Colombia maintain bilateral relations through trade and "
            "European Union partnerships, and a Colombian community is established "
            "in Brussels and Antwerp. The Colombian Embassy in Brussels is fully "
            "operational. When a Colombian national dies in Belgium and their family "
            "wishes to repatriate remains to Colombia, the death is registered with "
            "the local commune or gemeenten (civil registry). El Dorado "
            "International Airport (BOG) in Bogota is the main receiving airport. "
            "Both Belgium and Colombia are Hague Apostille Convention members, "
            "which simplifies document authentication. The acte de deces or "
            "overlijdensakte requires certified Spanish translation for Colombian "
            "authorities. "
            "(Colombian Ministry of Foreign Affairs, 2025; Belgian Federal "
            "Public Service Foreign Affairs, 2025.)"
        ),
    },
    # R88 -- Algeria x5
    {
        'origin': 'ireland', 'dest': 'algeria',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Algeria maintain diplomatic relations, and an Algerian "
            "community is established in Dublin and other Irish cities. The Algerian "
            "Embassy in Dublin is fully operational. When an Algerian national dies "
            "in Ireland and their family wishes to repatriate remains to Algeria, "
            "the death is registered with the local registrar's office, which "
            "reports to the General Register Office (GRO). Houari Boumediene "
            "International Airport (ALG) in Algiers is the main receiving airport. "
            "Ireland is a Hague Apostille Convention member; Algeria is not, so "
            "full consular authentication through the Algerian Embassy in Dublin "
            "is required for Irish documents. All documents require certified Arabic "
            "translation for the Algerian etat civil (civil registry). Remains must "
            "arrive in a hermetically sealed coffin. "
            "(Algerian Ministry of Foreign Affairs, 2025; Irish Department of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'algeria',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Algeria have bilateral ties through the oil and gas sector, "
            "and an Algerian community is established in Oslo. The Algerian Embassy "
            "in Oslo is fully operational. When an Algerian national dies in Norway "
            "and their family wishes to repatriate remains to Algeria, the death "
            "is registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). Houari Boumediene International Airport "
            "(ALG) in Algiers is the main receiving airport. Norway is a Hague "
            "Apostille Convention member; Algeria is not, so full consular "
            "authentication through the Algerian Embassy in Oslo is required for "
            "Norwegian documents. All documents require certified Arabic translation "
            "for the Algerian etat civil. "
            "(Algerian Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'algeria',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has an Algerian community, with nationals established in "
            "Stockholm, Gothenburg, and Malmo. The Algerian Embassy in Stockholm "
            "is fully operational. When an Algerian national dies in Sweden and "
            "their family wishes to repatriate remains to Algeria, the death is "
            "registered with the Swedish Tax Agency (Skatteverket) Population "
            "Register. Houari Boumediene International Airport (ALG) in Algiers "
            "is the main receiving airport. Sweden joined the Hague Apostille "
            "Convention in 1999; Algeria is not a member, so full consular "
            "authentication through the Algerian Embassy in Stockholm is required "
            "for Swedish documents. All documents require certified Arabic "
            "translation for the Algerian etat civil. "
            "(Algerian Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'algeria',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Algeria have diplomatic and historical ties, and an "
            "Algerian community is established in Lisbon and Porto. The Algerian "
            "Embassy in Lisbon is fully operational. When an Algerian national dies "
            "in Portugal and their family wishes to repatriate remains to Algeria, "
            "the death is registered with the local Conservatoria do Registo Civil. "
            "Houari Boumediene International Airport (ALG) in Algiers is the main "
            "receiving airport. Portugal joined the Hague Apostille Convention in "
            "1970; Algeria is not a member, so full consular authentication through "
            "the Algerian Embassy in Lisbon is required for Portuguese documents. "
            "All documents require certified Arabic translation for the Algerian "
            "etat civil. "
            "(Algerian Ministry of Foreign Affairs, 2025; Portuguese Ministry "
            "of Justice, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'algeria',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa and Algeria have bilateral ties as two of Africa's largest "
            "economies, both active in African Union frameworks. An Algerian "
            "community is established in Johannesburg and Cape Town. The Algerian "
            "Embassy in Pretoria is fully operational. When an Algerian national "
            "dies in South Africa and their family wishes to repatriate remains to "
            "Algeria, the death is registered with the Department of Home Affairs "
            "under the Births, Deaths and Marriages Act. Houari Boumediene "
            "International Airport (ALG) in Algiers is the main receiving airport. "
            "South Africa is a Hague Apostille Convention member; Algeria is not, "
            "so full consular authentication through the Algerian Embassy in "
            "Pretoria is required for South African documents. All documents require "
            "certified Arabic translation for the Algerian etat civil. "
            "(Algerian Ministry of Foreign Affairs, 2025; South African "
            "Department of Home Affairs, 2025.)"
        ),
    },
    # R88 -- Argentina x5
    {
        'origin': 'ireland', 'dest': 'argentina',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Argentina have historical connections through Irish "
            "emigration to South America, and an Irish-Argentine community maintains "
            "bilateral ties. The Argentine Embassy in Dublin is fully operational. "
            "When an Argentine national dies in Ireland and their family wishes to "
            "repatriate remains to Argentina, the death is registered with the local "
            "registrar's office, which reports to the General Register Office (GRO). "
            "Ministro Pistarini International Airport (EZE) in Buenos Aires is the "
            "main receiving airport. Both Ireland and Argentina are Hague Apostille "
            "Convention members (Ireland joined 1967, Argentina joined 1987), which "
            "simplifies document authentication. The Cuerpo Medico Forense (Forensic "
            "Medical Corps) takes jurisdiction for violent or unexplained deaths. "
            "(Argentine Ministry of Foreign Affairs, 2025; Irish Department of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'argentina',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Argentina maintain bilateral relations through trade and "
            "Norwegian investment in Argentina's offshore oil sector. An "
            "Argentine community is established in Oslo. The Argentine Embassy in "
            "Oslo is fully operational. When an Argentine national dies in Norway "
            "and their family wishes to repatriate remains to Argentina, the death "
            "is registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). Ministro Pistarini International "
            "Airport (EZE) in Buenos Aires is the main receiving airport. Both "
            "Norway and Argentina are Hague Apostille Convention members, which "
            "simplifies document authentication. The dodsattest requires certified "
            "Spanish translation for Argentine authorities. The Cuerpo Medico "
            "Forense takes jurisdiction for violent or unexplained deaths. "
            "(Argentine Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'argentina',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Argentina have active bilateral ties through trade and a "
            "Swedish-Argentine community with historical roots. The Argentine "
            "Embassy in Stockholm is fully operational. When an Argentine national "
            "dies in Sweden and their family wishes to repatriate remains to "
            "Argentina, the death is registered with the Swedish Tax Agency "
            "(Skatteverket) Population Register. Ministro Pistarini International "
            "Airport (EZE) in Buenos Aires is the main receiving airport. Both "
            "Sweden and Argentina are Hague Apostille Convention members, which "
            "simplifies document authentication. The dodsfallsintyg requires "
            "certified Spanish translation for Argentine authorities. The Cuerpo "
            "Medico Forense takes jurisdiction for violent or unexplained deaths. "
            "(Argentine Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'argentina',
        'embassy_city': 'Bern',
        'intro': (
            "Switzerland and Argentina have close bilateral ties through trade, "
            "finance, and a Swiss-Argentine community with historical roots in "
            "Buenos Aires and Cordoba. The Argentine Embassy in Bern is fully "
            "operational. When an Argentine national dies in Switzerland and their "
            "family wishes to repatriate remains to Argentina, the death is "
            "registered with the local Zivilstandsamt (civil registry office, "
            "cantonal level). Ministro Pistarini International Airport (EZE) in "
            "Buenos Aires is the main receiving airport. Both Switzerland and "
            "Argentina are Hague Apostille Convention members (Switzerland joined "
            "1972, Argentina joined 1987), which simplifies document authentication. "
            "The Todesurkunde requires certified Spanish translation for Argentine "
            "authorities. The Cuerpo Medico Forense takes jurisdiction for violent "
            "or unexplained deaths. "
            "(Argentine Ministry of Foreign Affairs, 2025; Swiss Federal "
            "Department of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'argentina',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgium and Argentina maintain bilateral diplomatic relations, and a "
            "Belgian-Argentine community maintains connections through historical "
            "ties. The Argentine Embassy in Brussels is fully operational. When an "
            "Argentine national dies in Belgium and their family wishes to repatriate "
            "remains to Argentina, the death is registered with the local commune "
            "or gemeenten (civil registry). Ministro Pistarini International Airport "
            "(EZE) in Buenos Aires is the main receiving airport. Both Belgium and "
            "Argentina are Hague Apostille Convention members (Belgium joined 1975, "
            "Argentina joined 1987), which simplifies document authentication. The "
            "acte de deces or overlijdensakte requires certified Spanish translation "
            "for Argentine authorities. The Cuerpo Medico Forense takes jurisdiction "
            "for violent or unexplained deaths. "
            "(Argentine Ministry of Foreign Affairs, 2025; Belgian Federal "
            "Public Service Foreign Affairs, 2025.)"
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
