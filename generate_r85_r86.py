#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R85-R86.

   R85 (25 routes, START_VARIANT=2=C):
     Philippines x5: united-kingdom, germany, france, italy, south-korea
     Colombia x5:    france, australia, canada, portugal, sweden
     Argentina x5:   france, australia, canada, portugal, netherlands
     Mexico x5:      france, australia, italy, netherlands, sweden
     Nepal x5:       france, canada, italy, netherlands, sweden

   R86 (25 routes, continues from R85):
     Brazil x5:      france, australia, canada, portugal, netherlands
     Peru x5:        france, australia, canada, netherlands, sweden
     Jordan x5:      germany, australia, netherlands, sweden, norway
     Romania x5:     australia, canada, netherlands, sweden, portugal
     Sri Lanka x5:   france, australia, canada, italy, south-korea

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
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Philippine funeral director takes custody at Ninoy Aquino "
            "International Airport (NAIA) cargo terminal in Manila. The Bureau "
            "of Quarantine clears the consignment. The Philippine Statistics "
            "Authority (PSA) is notified of the death. Documents from Hague "
            "Apostille member countries are accepted with an apostille "
            "certificate; all other documents require full consular "
            "authentication through the Philippine Embassy in the origin "
            "country. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. The receiving funeral director "
            "coordinates with the PSA and the Bureau of Quarantine. "
            "(Philippine Department of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Philippine Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to the Philippines. "
            "The Philippines joined the Hague Apostille Convention in 2019. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Philippine funeral director takes custody at Ninoy Aquino "
            "International Airport (NAIA) cargo terminal in Manila. The Bureau "
            "of Quarantine clears the consignment. The Philippine Statistics "
            "Authority (PSA) is notified of the death. Documents from Hague "
            "Apostille member countries are accepted with an apostille "
            "certificate; all others require full consular authentication. An "
            "embalming certificate and hermetically sealed coffin are required. "
            "The receiving funeral director coordinates with the PSA and the "
            "Bureau of Quarantine."
        ),
        'hub_url': 'repatriation-from-philippines',
    },
    'colombia': {
        'name': 'Colombia',
        'slug': 'colombia',
        'key': 'co',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport (BOG) cargo terminal in Bogota. The "
            "Notaria or Registraduria Nacional del Estado Civil registers "
            "the death. Medicina Legal (the forensic authority) takes "
            "jurisdiction for violent or unexplained deaths. Colombia is "
            "a Hague Apostille Convention member; documents from member "
            "states are accepted with an apostille certificate. All other "
            "documents require certified Spanish translation and consular "
            "authentication. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
        'consular_template': (
            "The Colombian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Colombia. "
            "Colombia is a Hague Apostille Convention member. The Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport (BOG) cargo terminal in Bogota. The "
            "Notaria or Registraduria Nacional del Estado Civil registers "
            "the death. Medicina Legal takes jurisdiction for violent or "
            "unexplained deaths. Colombia is a Hague Apostille Convention "
            "member; documents from member states are accepted with an "
            "apostille certificate. All other documents require certified "
            "Spanish translation and consular authentication. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'hub_url': 'repatriation-from-colombia',
    },
    'argentina': {
        'name': 'Argentina',
        'slug': 'argentina',
        'key': 'ar',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Argentine funeral director takes custody at Ministro "
            "Pistarini International Airport (EZE) cargo terminal in "
            "Buenos Aires. The provincial Registro Civil registers the "
            "death. The Cuerpo Medico Forense (forensic authority) takes "
            "jurisdiction for violent or unexplained deaths. Argentina is "
            "a Hague Apostille Convention member; documents from member "
            "states are accepted with an apostille certificate. All other "
            "documents require certified Spanish translation. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Argentine Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
        'consular_template': (
            "The Argentine Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Argentina. "
            "Argentina is a Hague Apostille Convention member. The Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Argentine funeral director takes custody at Ministro "
            "Pistarini International Airport (EZE) cargo terminal in Buenos "
            "Aires. The provincial Registro Civil registers the death. The "
            "Cuerpo Medico Forense takes jurisdiction for violent or "
            "unexplained deaths. Argentina is a Hague Apostille Convention "
            "member; documents from member states are accepted with an "
            "apostille certificate. All other documents require certified "
            "Spanish translation. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'hub_url': 'repatriation-from-argentina',
    },
    'mexico': {
        'name': 'Mexico',
        'slug': 'mexico',
        'key': 'mx',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Mexican funeral director takes custody at Mexico City "
            "International Airport (MEX) or the relevant regional cargo "
            "terminal. The Registro Civil (civil registry) registers the "
            "death. SEMEFO (Servicio Medico Forense) takes jurisdiction "
            "for violent or unexplained deaths. Mexico is a Hague Apostille "
            "Convention member; documents from member states are accepted "
            "with an apostille certificate. All other documents require "
            "certified Spanish translation. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
        'consular_template': (
            "The Mexican Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Mexico. Mexico "
            "is a Hague Apostille Convention member. The Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Mexican funeral director takes custody at Mexico City "
            "International Airport (MEX) or the relevant regional cargo "
            "terminal. The Registro Civil registers the death. SEMEFO "
            "takes jurisdiction for violent or unexplained deaths. Mexico "
            "is a Hague Apostille Convention member; documents from member "
            "states are accepted with an apostille certificate. All other "
            "documents require certified Spanish translation. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'hub_url': 'repatriation-from-mexico',
    },
    'nepal': {
        'name': 'Nepal',
        'slug': 'nepal',
        'key': 'np',
        'complexity_override': 'moderate-high',
        'timeline_avg_override': '4-7 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-16 weeks',
        'reception': (
            "The Nepalese funeral director takes custody at Tribhuvan "
            "International Airport (KTM) cargo terminal in Kathmandu. "
            "The local Ward Office handles civil registration of the death. "
            "The Ministry of Health clearance is required on arrival before "
            "the body is released. Hindu remains may be received for "
            "cremation rites at the ghats; the receiving family should "
            "specify arrangements in advance. Nepal is not a member of the "
            "Hague Apostille Convention; all foreign documents require full "
            "consular authentication through the Nepalese Embassy in the "
            "country of origin. Certified translation into Nepali or "
            "English is required. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Nepalese Embassy in {city} can advise on documentation "
            "requirements for repatriation to Nepal. Nepal is not a Hague "
            "Apostille Convention member; full consular authentication "
            "through the Nepalese Embassy in {city} is required. The "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Nepalese funeral director takes custody at Tribhuvan "
            "International Airport (KTM) cargo terminal in Kathmandu. The "
            "local Ward Office handles civil registration. The Ministry of "
            "Health clearance is required on arrival. Nepal is not a Hague "
            "Apostille Convention member; all foreign documents require full "
            "consular authentication through the Nepalese Embassy in the "
            "origin country. Certified translation into Nepali or English "
            "is required. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'hub_url': 'repatriation-from-nepal',
    },
    'brazil': {
        'name': 'Brazil',
        'slug': 'brazil',
        'key': 'br',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Brazilian funeral director takes custody at Guarulhos "
            "International Airport (GRU) in Sao Paulo or Galeao "
            "International Airport (GIG) in Rio de Janeiro cargo terminal, "
            "depending on the family's destination. The local Cartorio de "
            "Registro Civil registers the death. ANVISA (Agencia Nacional "
            "de Vigilancia Sanitaria) clearance is required for all "
            "incoming remains. Brazil joined the Hague Apostille Convention "
            "in 2016; documents from member states are accepted with an "
            "apostille certificate. All other documents require certified "
            "Portuguese translation. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
        'consular_template': (
            "The Brazilian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Brazil. Brazil "
            "joined the Hague Apostille Convention in 2016. The Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Brazilian funeral director takes custody at Guarulhos "
            "International Airport (GRU) or Galeao International Airport "
            "(GIG) cargo terminal. The local Cartorio de Registro Civil "
            "registers the death. ANVISA clearance is required for all "
            "incoming remains. Brazil joined the Hague Apostille Convention "
            "in 2016; documents from member states are accepted with an "
            "apostille certificate. All other documents require certified "
            "Portuguese translation. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'hub_url': 'repatriation-from-brazil',
    },
    'peru': {
        'name': 'Peru',
        'slug': 'peru',
        'key': 'pe',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Peruvian funeral director takes custody at Jorge Chavez "
            "International Airport (LIM) cargo terminal in Lima. RENIEC "
            "(Registro Nacional de Identificacion y Estado Civil) registers "
            "the death. Peru is a Hague Apostille Convention member; "
            "documents from member states are accepted with an apostille "
            "certificate. All other documents require certified Spanish "
            "translation. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. The receiving funeral "
            "director coordinates with RENIEC and the relevant health "
            "authority. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
        'consular_template': (
            "The Peruvian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Peru. Peru is "
            "a Hague Apostille Convention member. The Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Peruvian funeral director takes custody at Jorge Chavez "
            "International Airport (LIM) cargo terminal in Lima. RENIEC "
            "registers the death. Peru is a Hague Apostille Convention "
            "member; documents from member states are accepted with an "
            "apostille certificate. All other documents require certified "
            "Spanish translation. An embalming certificate and hermetically "
            "sealed coffin are required. The receiving funeral director "
            "coordinates with RENIEC and the relevant health authority."
        ),
        'hub_url': 'repatriation-from-peru',
    },
    'jordan': {
        'name': 'Jordan',
        'slug': 'jordan',
        'key': 'jo',
        'complexity_override': 'moderate-high',
        'timeline_avg_override': '4-7 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-14 weeks',
        'reception': (
            "The Jordanian funeral director takes custody at Queen Alia "
            "International Airport (AMM) cargo terminal in Amman. The "
            "Ministry of Interior civil registration office registers the "
            "death. The Ministry of Health clearance is required before "
            "final disposition; a burial permit from the Ministry of Health "
            "is required. For Muslim remains, Islamic law procedures apply "
            "and prompt burial is expected. Jordan is not a member of the "
            "Hague Apostille Convention; all foreign documents require "
            "certified Arabic translation and full consular authentication "
            "through the Jordanian Embassy in the country of origin. An "
            "embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Jordanian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Jordan. Jordan "
            "is not a Hague Apostille Convention member; full consular "
            "authentication through the Jordanian Embassy in {city} is "
            "required. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Jordanian funeral director takes custody at Queen Alia "
            "International Airport (AMM) cargo terminal in Amman. The "
            "Ministry of Interior civil registration office registers the "
            "death. The Ministry of Health clearance and a burial permit "
            "are required before final disposition. For Muslim remains, "
            "Islamic law procedures apply and prompt burial is expected. "
            "Jordan is not a Hague Apostille Convention member; all "
            "foreign documents require certified Arabic translation and "
            "full consular authentication through the Jordanian Embassy "
            "in the origin country. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'hub_url': 'repatriation-from-jordan',
    },
    'romania': {
        'name': 'Romania',
        'slug': 'romania',
        'key': 'ro',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Romanian funeral director takes custody at Bucharest Henri "
            "Coanda International Airport (OTP) cargo terminal or the "
            "relevant regional airport. The local Starea Civila (civil "
            "status office under the local council) registers the death and "
            "issues the certificat de deces in Romanian. Romania is an EU "
            "member and Hague Apostille Convention member; documents from "
            "EU and Hague member states are accepted. Documents in other "
            "languages require certified Romanian translation. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. The receiving funeral director coordinates "
            "with the local Starea Civila. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Romanian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Romania. Romania "
            "is an EU member and Hague Apostille Convention member. The "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Romanian funeral director takes custody at Bucharest Henri "
            "Coanda International Airport (OTP) or the relevant regional "
            "airport cargo terminal. The local Starea Civila registers the "
            "death and issues the certificat de deces in Romanian. Romania "
            "is an EU member and Hague Apostille Convention member; "
            "documents from EU and Hague member states are accepted. "
            "Documents in other languages require certified Romanian "
            "translation. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'hub_url': 'repatriation-from-romania',
    },
    'sri-lanka': {
        'name': 'Sri Lanka',
        'slug': 'sri-lanka',
        'key': 'lk',
        'complexity_override': 'moderate-high',
        'timeline_avg_override': '4-7 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-14 weeks',
        'reception': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) cargo terminal in Colombo. The "
            "Registrar General's Department registers the death. The "
            "Ministry of Health clearance is required on arrival before the "
            "body is released. Sri Lanka is not a member of the Hague "
            "Apostille Convention; all foreign documents require full "
            "consular authentication through the Sri Lankan High Commission "
            "or Embassy in the country of origin. Certified translation "
            "into English or Sinhala is required. A sealed zinc-lined "
            "coffin and embalming certificate are required for all air "
            "imports. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Sri Lankan High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Sri Lanka. "
            "Sri Lanka is not a Hague Apostille Convention member; all "
            "documents must be authenticated through the Sri Lankan High "
            "Commission in {city}. The High Commission cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) cargo terminal in Colombo. The "
            "Registrar General's Department registers the death. The "
            "Ministry of Health clearance is required on arrival. Sri Lanka "
            "is not a Hague Apostille Convention member; all foreign "
            "documents require full consular authentication through the Sri "
            "Lankan High Commission or Embassy in the origin country. "
            "Certified translation into English or Sinhala is required. A "
            "sealed zinc-lined coffin and embalming certificate are required."
        ),
        'hub_url': 'repatriation-from-sri-lanka',
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
}

ROUTES = [
    # R85 -- Philippines x5
    {
        'origin': 'united-kingdom', 'dest': 'philippines',
        'embassy_city': 'London',
        'intro': (
            "The UK has one of Europe's largest Filipino communities, with over "
            "200,000 Filipinos living and working in the UK, many in healthcare, "
            "social care, and hospitality. When a Filipino national dies in the UK "
            "and their family wishes to repatriate remains to the Philippines, the "
            "death is registered at the local register office within 5 days. The UK "
            "is a Hague Apostille Convention member; the Philippines joined in 2019. "
            "Both countries are now Hague members. The Philippine Embassy in London "
            "can assist with documentation requirements. "
            "(Philippine Department of Foreign Affairs, 2025; FCDO Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'philippines',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany hosts a Filipino community, with nationals working in "
            "healthcare, IT, and engineering as part of bilateral labour "
            "agreements. Germany maintains an Embassy in Manila. When a Filipino "
            "national dies in Germany and their family wishes to repatriate "
            "remains to the Philippines, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde requires certified "
            "English or Filipino translation for Philippine authorities. The "
            "Philippines joined the Hague Apostille Convention in 2019; Germany "
            "joined in 1965. Both countries are Hague members. "
            "(Philippine Department of Foreign Affairs, 2025; German Federal "
            "Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'philippines',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Filipino community, with nationals working in domestic "
            "services, healthcare, and the maritime sector. The Philippines "
            "maintains an Embassy in Paris. When a Filipino national dies in "
            "France and their family wishes to repatriate remains to the "
            "Philippines, the death is registered with the local mairie (town "
            "hall). The acte de deces requires certified English or Filipino "
            "translation for Philippine authorities. The Philippines joined the "
            "Hague Apostille Convention in 2019; France joined in 1960. Both "
            "countries are Hague members. "
            "(Philippine Department of Foreign Affairs, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'philippines',
        'embassy_city': 'Rome',
        'intro': (
            "Italy is home to a significant Filipino community, concentrated in "
            "Rome, Milan, and other major cities, where Filipinos work "
            "predominantly in domestic care, hospitality, and services. Italy "
            "maintains an Embassy in Manila. When a Filipino national dies in "
            "Italy and their family wishes to repatriate remains to the "
            "Philippines, the death is registered with the local comune (civil "
            "registry). The atto di morte requires certified English or Filipino "
            "translation for Philippine authorities. The Philippines joined the "
            "Hague Apostille Convention in 2019; Italy joined in 1978. "
            "(Philippine Department of Foreign Affairs, 2025; Italian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-korea', 'dest': 'philippines',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korea and the Philippines maintain active bilateral ties, with "
            "Filipino nationals working in manufacturing, domestic services, and "
            "seafaring under the Philippines Overseas Employment Administration "
            "(POEA) framework. South Korea maintains an Embassy in Manila. When "
            "a Filipino national dies in South Korea and their family wishes to "
            "repatriate remains to the Philippines, the death is registered with "
            "the local gu office (ward office). The Philippines joined the Hague "
            "Apostille Convention in 2019; South Korea is also a Hague member. "
            "(Philippine Department of Foreign Affairs, 2025; South Korean "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R85 -- Colombia x5
    {
        'origin': 'france', 'dest': 'colombia',
        'embassy_city': 'Paris',
        'intro': (
            "France and Colombia maintain bilateral ties, with Colombian nationals "
            "present in Paris and other French cities, and French nationals working "
            "in Colombia in trade and development cooperation. The Colombian Embassy "
            "in Paris is fully operational. When a Colombian national dies in France "
            "and their family wishes to repatriate remains to Colombia, the death is "
            "registered with the local mairie (town hall). The acte de deces requires "
            "certified Spanish translation for Colombian authorities. Colombia is a "
            "Hague Apostille Convention member; France joined in 1960. Both countries "
            "are Hague members, which simplifies document authentication. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025; French "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'colombia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Colombia have bilateral ties through trade, mining "
            "investment, and a Colombian-Australian community established in "
            "Sydney, Melbourne, and Perth. Colombia maintains a Consulate in "
            "Sydney. When a Colombian national dies in Australia and their family "
            "wishes to repatriate remains to Colombia, the death is registered "
            "with the state or territory Births, Deaths and Marriages (BDM) "
            "registry. Australia is a Hague Apostille Convention member; Colombia "
            "is also a Hague member. Both countries are Hague members, which "
            "simplifies document authentication. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'colombia',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts one of the largest Colombian communities in North "
            "America, with families concentrated in Toronto, Mississauga, and "
            "Vancouver. The Colombian Embassy in Ottawa is fully operational. "
            "When a Colombian national dies in Canada and their family wishes "
            "to repatriate remains to Colombia, the death is registered with "
            "the provincial civil registration authority. Canada joined the "
            "Hague Apostille Convention in November 2024; Colombia is a Hague "
            "member. Both countries are now Hague members. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025; "
            "Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'colombia',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Colombia share cultural and linguistic ties through "
            "the shared Iberian heritage of Latin America, and Colombian "
            "nationals are present in Lisbon and Porto. Colombia maintains an "
            "Embassy in Lisbon. When a Colombian national dies in Portugal and "
            "their family wishes to repatriate remains to Colombia, the death "
            "is registered with the local Conservatoria do Registo Civil. The "
            "assento de obito requires certified Spanish translation for "
            "Colombian authorities. Colombia is a Hague Apostille Convention "
            "member; Portugal joined in 1970. Both are Hague members. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025; "
            "Portuguese Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'colombia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Colombia maintain bilateral ties through trade, "
            "development cooperation, and a Colombian community established "
            "in Stockholm and Gothenburg. The Colombian Embassy in Stockholm "
            "is fully operational. When a Colombian national dies in Sweden "
            "and their family wishes to repatriate remains to Colombia, the "
            "death is registered with the Swedish Tax Agency (Skatteverket) "
            "Population Register. The dodsfallsintyg requires certified Spanish "
            "translation for Colombian authorities. Colombia is a Hague "
            "Apostille Convention member; Sweden joined in 1999. Both are "
            "Hague members. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025; "
            "Skatteverket, Sweden, 2025.)"
        ),
    },
    # R85 -- Argentina x5
    {
        'origin': 'france', 'dest': 'argentina',
        'embassy_city': 'Paris',
        'intro': (
            "France and Argentina share strong historical and cultural "
            "connections, with a significant French-Argentine community and "
            "Argentine nationals present in Paris and Lyon. Argentina maintains "
            "an Embassy in Paris. When an Argentine national dies in France and "
            "their family wishes to repatriate remains to Argentina, the death "
            "is registered with the local mairie (town hall). The acte de deces "
            "requires certified Spanish translation for Argentine authorities. "
            "Argentina is a Hague Apostille Convention member; France joined "
            "in 1960. Both countries are Hague members. "
            "(Argentine Ministry of Foreign Affairs, Cancilleria, 2025; French "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'argentina',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Argentina share bilateral trade ties and an "
            "Argentine-Australian community established in Sydney and Melbourne. "
            "Argentina maintains an Embassy in Canberra. When an Argentine "
            "national dies in Australia and their family wishes to repatriate "
            "remains to Argentina, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. Argentina "
            "is a Hague Apostille Convention member; Australia joined in 1995. "
            "Both countries are Hague members, which simplifies document "
            "authentication for this corridor. "
            "(Argentine Ministry of Foreign Affairs, Cancilleria, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'argentina',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts an Argentine-Canadian community, with families "
            "concentrated in Toronto and Vancouver. Argentina maintains an "
            "Embassy in Ottawa. When an Argentine national dies in Canada and "
            "their family wishes to repatriate remains to Argentina, the death "
            "is registered with the provincial civil registration authority. "
            "Argentina is a Hague Apostille Convention member; Canada joined "
            "in November 2024. Both countries are now Hague members. "
            "(Argentine Ministry of Foreign Affairs, Cancilleria, 2025; "
            "Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'argentina',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Argentina share deep historical and linguistic ties, "
            "with a significant Portuguese-Argentine community in Buenos Aires "
            "and Argentine nationals present in Lisbon. Argentina maintains an "
            "Embassy in Lisbon. When an Argentine national dies in Portugal and "
            "their family wishes to repatriate remains to Argentina, the death "
            "is registered with the local Conservatoria do Registo Civil. The "
            "assento de obito requires certified Spanish translation for "
            "Argentine authorities. Argentina is a Hague Apostille Convention "
            "member; Portugal joined in 1970. Both are Hague members. "
            "(Argentine Ministry of Foreign Affairs, Cancilleria, 2025; "
            "Portuguese Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'argentina',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has bilateral trade and cultural ties with "
            "Argentina, and Argentine nationals are present in Amsterdam and "
            "Rotterdam. Argentina maintains an Embassy in The Hague. When an "
            "Argentine national dies in the Netherlands and their family wishes "
            "to repatriate remains to Argentina, the death is registered with "
            "the local gemeente (municipal civil registry). The akte van "
            "overlijden requires certified Spanish translation for Argentine "
            "authorities. Argentina is a Hague Apostille Convention member; "
            "the Netherlands joined in 1960. Both are Hague members. "
            "(Argentine Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
    },
    # R85 -- Mexico x5
    {
        'origin': 'france', 'dest': 'mexico',
        'embassy_city': 'Paris',
        'intro': (
            "France and Mexico maintain strong bilateral ties, with Mexican "
            "nationals present in Paris for work, study, and business, and "
            "French nationals working in Mexico in aerospace, luxury goods, "
            "and financial services. The Mexican Embassy in Paris is fully "
            "operational. When a Mexican national dies in France and their "
            "family wishes to repatriate remains to Mexico, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "requires certified Spanish translation for Mexican authorities. "
            "Mexico is a Hague Apostille Convention member; France joined "
            "in 1960. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025; French "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'mexico',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Mexico share bilateral trade ties and a growing "
            "Mexican-Australian community. Mexico maintains a Consulate in "
            "Sydney. When a Mexican national dies in Australia and their "
            "family wishes to repatriate remains to Mexico, the death is "
            "registered with the state or territory Births, Deaths and "
            "Marriages (BDM) registry. Mexico is a Hague Apostille Convention "
            "member; Australia joined in 1995. Both countries are Hague "
            "members, simplifying document authentication. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'mexico',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Mexico share significant bilateral ties through trade "
            "and a shared Italian-Mexican cultural heritage, with Mexican "
            "nationals present in Rome and Milan for study, business, and "
            "cultural exchange. Mexico maintains an Embassy in Rome. When a "
            "Mexican national dies in Italy and their family wishes to "
            "repatriate remains to Mexico, the death is registered with the "
            "local comune (civil registry). The atto di morte requires "
            "certified Spanish translation for Mexican authorities. Mexico "
            "is a Hague Apostille Convention member; Italy joined in 1978. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025; Italian "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'mexico',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Mexico maintain bilateral trade and cultural "
            "ties, with Mexican nationals present in Amsterdam and Rotterdam "
            "for business and study. Mexico maintains an Embassy in The Hague. "
            "When a Mexican national dies in the Netherlands and their family "
            "wishes to repatriate remains to Mexico, the death is registered "
            "with the local gemeente (municipal civil registry). The akte van "
            "overlijden requires certified Spanish translation for Mexican "
            "authorities. Mexico is a Hague Apostille Convention member; the "
            "Netherlands joined in 1960. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'mexico',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Mexico maintain bilateral ties, with Mexican nationals "
            "present in Stockholm for work and study, and Sweden as a trading "
            "partner for Mexican exports. The Mexican Embassy in Stockholm is "
            "fully operational. When a Mexican national dies in Sweden and their "
            "family wishes to repatriate remains to Mexico, the death is "
            "registered with the Swedish Tax Agency (Skatteverket) Population "
            "Register. The dodsfallsintyg requires certified Spanish translation "
            "for Mexican authorities. Mexico is a Hague Apostille Convention "
            "member; Sweden joined in 1999. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025; "
            "Skatteverket, Sweden, 2025.)"
        ),
    },
    # R85 -- Nepal x5
    {
        'origin': 'france', 'dest': 'nepal',
        'embassy_city': 'Paris',
        'intro': (
            "France and Nepal have bilateral ties through mountaineering, "
            "trekking tourism, and development cooperation, with a Nepalese "
            "community established in France and French nationals working in "
            "Nepal in development and exploration. The Nepalese Embassy in "
            "Paris is fully operational. When a Nepalese national dies in "
            "France and their family wishes to repatriate remains to Nepal, "
            "the death is registered with the local mairie (town hall). The "
            "acte de deces requires certified Nepali or English translation "
            "for Nepalese authorities. Nepal is not a Hague Apostille "
            "Convention member; full consular authentication through the "
            "Nepalese Embassy in Paris is required. "
            "(Nepalese Ministry of Foreign Affairs, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'nepal',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a growing Nepalese-Canadian community, with Nepalese "
            "nationals working in healthcare, engineering, and technology across "
            "Toronto, Vancouver, and Calgary. The Nepalese Embassy in Ottawa is "
            "fully operational. When a Nepalese national dies in Canada and "
            "their family wishes to repatriate remains to Nepal, the death is "
            "registered with the provincial civil registration authority. Nepal "
            "is not a Hague Apostille Convention member; full consular "
            "authentication through the Nepalese Embassy in Ottawa is required. "
            "Canada joined the Hague Apostille Convention in November 2024. "
            "(Nepalese Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'nepal',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a Nepalese community, with nationals working in "
            "agriculture, domestic services, and the textile industry in "
            "northern Italy. The Nepalese Embassy in Rome is fully operational. "
            "When a Nepalese national dies in Italy and their family wishes to "
            "repatriate remains to Nepal, the death is registered with the "
            "local comune (civil registry). The atto di morte requires certified "
            "Nepali or English translation for Nepalese authorities. Nepal is "
            "not a Hague Apostille Convention member; full consular "
            "authentication through the Nepalese Embassy in Rome is required. "
            "(Nepalese Ministry of Foreign Affairs, 2025; Italian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'nepal',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Nepal maintain bilateral ties through "
            "development cooperation, with Dutch organisations active in "
            "Nepal's education and water sectors. A Nepalese community is "
            "established in the Netherlands. Nepal maintains an Embassy in "
            "The Hague. When a Nepalese national dies in the Netherlands and "
            "their family wishes to repatriate remains to Nepal, the death is "
            "registered with the local gemeente (municipal civil registry). "
            "Nepal is not a Hague Apostille Convention member; full consular "
            "authentication through the Nepalese Embassy in The Hague is "
            "required. "
            "(Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'nepal',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Nepal have development cooperation ties, with Swedish "
            "organisations active in Nepal's health and poverty reduction "
            "programmes. A Nepalese community is established in Sweden. Nepal "
            "maintains an Embassy in Stockholm. When a Nepalese national dies "
            "in Sweden and their family wishes to repatriate remains to Nepal, "
            "the death is registered with the Swedish Tax Agency (Skatteverket) "
            "Population Register. Nepal is not a Hague Apostille Convention "
            "member; full consular authentication through the Nepalese Embassy "
            "in Stockholm is required. "
            "(Nepalese Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    # R86 -- Brazil x5
    {
        'origin': 'france', 'dest': 'brazil',
        'embassy_city': 'Paris',
        'intro': (
            "France and Brazil share strong bilateral ties through culture, "
            "trade, and science, with a significant Brazilian community in "
            "Paris and French nationals working in Brazil in luxury goods, "
            "aerospace, and energy. Brazil maintains an Embassy in Paris. "
            "When a Brazilian national dies in France and their family wishes "
            "to repatriate remains to Brazil, the death is registered with "
            "the local mairie (town hall). The acte de deces requires certified "
            "Portuguese translation for Brazilian authorities. Brazil joined "
            "the Hague Apostille Convention in 2016; France joined in 1960. "
            "Both countries are Hague members. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025; French "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'brazil',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Brazil maintain bilateral trade ties, and a "
            "Brazilian-Australian community is established in Sydney and "
            "Melbourne, working in professional services and IT. Brazil "
            "maintains an Embassy in Canberra. When a Brazilian national "
            "dies in Australia and their family wishes to repatriate remains "
            "to Brazil, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. Brazil joined the "
            "Hague Apostille Convention in 2016; Australia joined in 1995. "
            "Both countries are Hague members. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'brazil',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a significant Brazilian-Canadian community, with "
            "nationals concentrated in Toronto and Vancouver working in "
            "construction, services, and technology. Brazil maintains an "
            "Embassy in Ottawa. When a Brazilian national dies in Canada and "
            "their family wishes to repatriate remains to Brazil, the death "
            "is registered with the provincial civil registration authority. "
            "Brazil joined the Hague Apostille Convention in 2016; Canada "
            "joined in November 2024. Both countries are now Hague members. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025; "
            "Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'brazil',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Brazil share a profound historical and linguistic "
            "bond, with the largest Portuguese-speaking populations outside "
            "Brazil concentrated in Portugal. Brazilian nationals are "
            "Portugal's largest non-EU migrant group. Brazil maintains an "
            "Embassy in Lisbon. When a Brazilian national dies in Portugal "
            "and their family wishes to repatriate remains to Brazil, the "
            "death is registered with the local Conservatoria do Registo "
            "Civil. Brazil joined the Hague Apostille Convention in 2016; "
            "Portugal joined in 1970. Both countries are Hague members. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025; "
            "Portuguese Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'brazil',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Brazil have strong bilateral trade ties, "
            "with Dutch agricultural investment significant in Brazil's "
            "agri-food sector and Brazilian nationals present in Amsterdam "
            "and Rotterdam. Brazil maintains an Embassy in The Hague. When "
            "a Brazilian national dies in the Netherlands and their family "
            "wishes to repatriate remains to Brazil, the death is registered "
            "with the local gemeente (municipal civil registry). The akte "
            "van overlijden requires certified Portuguese translation for "
            "Brazilian authorities. Brazil joined the Hague Apostille "
            "Convention in 2016; the Netherlands joined in 1960. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
    },
    # R86 -- Peru x5
    {
        'origin': 'france', 'dest': 'peru',
        'embassy_city': 'Paris',
        'intro': (
            "France and Peru maintain bilateral ties through culture, trade, "
            "and archaeology, with Peruvian nationals present in Paris for "
            "study and work, and French nationals working in Peru in mining "
            "and development. The Peruvian Embassy in Paris is fully "
            "operational. When a Peruvian national dies in France and their "
            "family wishes to repatriate remains to Peru, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "requires certified Spanish translation for Peruvian authorities. "
            "Peru is a Hague Apostille Convention member; France joined in "
            "1960. Both countries are Hague members. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025; French "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'peru',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Peru have bilateral trade ties, with the mining "
            "and resources sectors creating commercial links between the two "
            "countries. A Peruvian-Australian community is established in "
            "Sydney and Melbourne. Peru maintains an Embassy in Canberra. "
            "When a Peruvian national dies in Australia and their family "
            "wishes to repatriate remains to Peru, the death is registered "
            "with the state or territory Births, Deaths and Marriages (BDM) "
            "registry. Peru is a Hague Apostille Convention member; Australia "
            "joined in 1995. Both countries are Hague members. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'peru',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a Peruvian-Canadian community, with nationals "
            "concentrated in Toronto, Ottawa, and Montreal working in "
            "hospitality, construction, and professional services. Peru "
            "maintains an Embassy in Ottawa. When a Peruvian national dies "
            "in Canada and their family wishes to repatriate remains to Peru, "
            "the death is registered with the provincial civil registration "
            "authority. Peru is a Hague Apostille Convention member; Canada "
            "joined in November 2024. Both countries are now Hague members. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025; "
            "Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'peru',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Peru maintain bilateral trade and cultural "
            "ties. A Peruvian community is established in the Netherlands, "
            "working in services and the arts. Peru maintains an Embassy in "
            "The Hague. When a Peruvian national dies in the Netherlands and "
            "their family wishes to repatriate remains to Peru, the death is "
            "registered with the local gemeente (municipal civil registry). "
            "The akte van overlijden requires certified Spanish translation "
            "for Peruvian authorities. Peru is a Hague Apostille Convention "
            "member; the Netherlands joined in 1960. Both are Hague members. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'peru',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Peru maintain bilateral ties through trade and "
            "development cooperation. A Peruvian community is established "
            "in Stockholm. Peru maintains an Embassy in Stockholm. When a "
            "Peruvian national dies in Sweden and their family wishes to "
            "repatriate remains to Peru, the death is registered with the "
            "Swedish Tax Agency (Skatteverket) Population Register. Peru is "
            "a Hague Apostille Convention member; Sweden joined in 1999. "
            "Both are Hague members. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025; "
            "Skatteverket, Sweden, 2025.)"
        ),
    },
    # R86 -- Jordan x5
    {
        'origin': 'germany', 'dest': 'jordan',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany hosts one of the largest Arab communities in Europe, "
            "with Jordanian and Palestinian-origin nationals established "
            "across Berlin, Cologne, and Hamburg. Germany maintains an "
            "Embassy in Amman. When a Jordanian national dies in Germany "
            "and their family wishes to repatriate remains to Jordan, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde requires certified Arabic translation for "
            "Jordanian authorities. Jordan is not a Hague Apostille "
            "Convention member; full consular authentication through the "
            "Jordanian Embassy in Berlin is required. For Muslim remains, "
            "Islamic law procedures apply and prompt burial is expected. "
            "(Jordanian Ministry of Foreign Affairs, 2025; German Federal "
            "Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'jordan',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Jordanian-Australian community, with nationals "
            "working across Sydney and Melbourne in professional services "
            "and business. Jordan maintains an Embassy in Canberra. When a "
            "Jordanian national dies in Australia and their family wishes "
            "to repatriate remains to Jordan, the death is registered with "
            "the state or territory Births, Deaths and Marriages (BDM) "
            "registry. Jordan is not a Hague Apostille Convention member; "
            "full consular authentication through the Jordanian Embassy in "
            "Canberra is required. For Muslim remains, Islamic law "
            "procedures apply. "
            "(Jordanian Ministry of Foreign Affairs, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'jordan',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a Jordanian and broader Arab community, "
            "and trade ties between the two countries include logistics, "
            "agriculture, and phosphate trade. Jordan maintains an Embassy "
            "in The Hague. When a Jordanian national dies in the Netherlands "
            "and their family wishes to repatriate remains to Jordan, the "
            "death is registered with the local gemeente (municipal civil "
            "registry). The akte van overlijden requires certified Arabic "
            "translation for Jordanian authorities. Jordan is not a Hague "
            "Apostille Convention member; full consular authentication "
            "through the Jordanian Embassy in The Hague is required. "
            "(Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'jordan',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden hosts a Jordanian and broader Arab-origin community, "
            "with families established in Stockholm and Malmo. Jordan "
            "maintains an Embassy in Stockholm. When a Jordanian national "
            "dies in Sweden and their family wishes to repatriate remains "
            "to Jordan, the death is registered with the Swedish Tax Agency "
            "(Skatteverket) Population Register. The dodsfallsintyg requires "
            "certified Arabic translation for Jordanian authorities. Jordan "
            "is not a Hague Apostille Convention member; full consular "
            "authentication through the Jordanian Embassy in Stockholm is "
            "required. For Muslim remains, Islamic law procedures apply. "
            "(Jordanian Ministry of Foreign Affairs, 2025; "
            "Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'jordan',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway has a Jordanian and broader Middle Eastern community, "
            "with families established in Oslo and Bergen. Jordan maintains "
            "an Embassy in Oslo. When a Jordanian national dies in Norway "
            "and their family wishes to repatriate remains to Jordan, the "
            "death is registered with Folkeregisteret (the civil registration "
            "system administered by Skatteetaten). The dodsattest requires "
            "certified Arabic translation for Jordanian authorities. Jordan "
            "is not a Hague Apostille Convention member; full consular "
            "authentication through the Jordanian Embassy in Oslo is "
            "required. For Muslim remains, Islamic law procedures apply. "
            "(Jordanian Ministry of Foreign Affairs, 2025; "
            "Skatteetaten, Norway, 2025.)"
        ),
    },
    # R86 -- Romania x5
    {
        'origin': 'australia', 'dest': 'romania',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Romanian-Australian community, with nationals "
            "working in Sydney, Melbourne, and Adelaide in construction, IT, "
            "and healthcare. Romania maintains an Embassy in Canberra. When "
            "a Romanian national dies in Australia and their family wishes "
            "to repatriate remains to Romania, the death is registered with "
            "the state or territory Births, Deaths and Marriages (BDM) "
            "registry. Romania is an EU member and Hague Apostille Convention "
            "member; Australia joined in 1995. Both countries are Hague "
            "members, which simplifies document authentication. "
            "(Romanian Ministry of Foreign Affairs, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'romania',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a significant Romanian-Canadian community, with "
            "nationals concentrated in Toronto, Montreal, and Calgary working "
            "in IT, engineering, and healthcare. The Romanian Embassy in "
            "Ottawa is fully operational. When a Romanian national dies in "
            "Canada and their family wishes to repatriate remains to Romania, "
            "the death is registered with the provincial civil registration "
            "authority. Romania is an EU member and Hague Apostille Convention "
            "member; Canada joined in November 2024. Both countries are now "
            "Hague members. "
            "(Romanian Ministry of Foreign Affairs, 2025; "
            "Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'romania',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has one of Europe's largest Romanian diaspora "
            "communities, with Romanians working predominantly in agriculture, "
            "logistics, and construction across Westland, Rotterdam, and "
            "Amsterdam. Romania maintains an Embassy in The Hague. When a "
            "Romanian national dies in the Netherlands and their family wishes "
            "to repatriate remains to Romania, the death is registered with "
            "the local gemeente (municipal civil registry). Romania is an EU "
            "member and Hague Apostille Convention member; the Netherlands "
            "joined in 1960. Both are Hague members. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'romania',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden hosts a Romanian community, with nationals working in "
            "Stockholm and other major cities in hospitality, construction, "
            "and care services. Romania maintains an Embassy in Stockholm. "
            "When a Romanian national dies in Sweden and their family wishes "
            "to repatriate remains to Romania, the death is registered with "
            "the Swedish Tax Agency (Skatteverket) Population Register. "
            "Romania is an EU member and Hague Apostille Convention member; "
            "Sweden joined in 1999. Both are Hague members. "
            "(Romanian Ministry of Foreign Affairs, 2025; "
            "Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'romania',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal has a Romanian community, with nationals working in "
            "agriculture, construction, and services across Lisbon, the "
            "Alentejo, and the Algarve. Romania maintains an Embassy in "
            "Lisbon. When a Romanian national dies in Portugal and their "
            "family wishes to repatriate remains to Romania, the death is "
            "registered with the local Conservatoria do Registo Civil. "
            "Romania is an EU member and Hague Apostille Convention member; "
            "Portugal joined in 1970. Both are EU and Hague members, "
            "facilitating straightforward document authentication. "
            "(Romanian Ministry of Foreign Affairs, 2025; Portuguese "
            "Ministry of Justice, 2025.)"
        ),
    },
    # R86 -- Sri Lanka x5
    {
        'origin': 'france', 'dest': 'sri-lanka',
        'embassy_city': 'Paris',
        'intro': (
            "France and Sri Lanka maintain bilateral ties through trade, "
            "tourism, and a Sri Lankan community established in Paris. The "
            "Sri Lankan Embassy in Paris is fully operational. When a Sri "
            "Lankan national dies in France and their family wishes to "
            "repatriate remains to Sri Lanka, the death is registered with "
            "the local mairie (town hall). The acte de deces requires "
            "certified English or Sinhala translation for Sri Lankan "
            "authorities. Sri Lanka is not a Hague Apostille Convention "
            "member; full consular authentication through the Sri Lankan "
            "Embassy in Paris is required. A sealed zinc-lined coffin and "
            "embalming certificate are required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025; French "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'sri-lanka',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a significant Sri Lankan-Australian community, "
            "with nationals concentrated in Melbourne, Sydney, and Adelaide, "
            "working in healthcare, IT, and professional services. Sri Lanka "
            "maintains a High Commission in Canberra. When a Sri Lankan "
            "national dies in Australia and their family wishes to repatriate "
            "remains to Sri Lanka, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. Sri Lanka "
            "is not a Hague Apostille Convention member; full consular "
            "authentication through the Sri Lankan High Commission in Canberra "
            "is required. A sealed zinc-lined coffin and embalming certificate "
            "are required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025; "
            "DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'sri-lanka',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a substantial Sri Lankan-Canadian community, with "
            "Tamil and Sinhalese families concentrated in Toronto's Scarborough "
            "district, as well as in Ottawa and Vancouver. Sri Lanka maintains "
            "a High Commission in Ottawa. When a Sri Lankan national dies in "
            "Canada and their family wishes to repatriate remains to Sri Lanka, "
            "the death is registered with the provincial civil registration "
            "authority. Sri Lanka is not a Hague Apostille Convention member; "
            "full consular authentication through the Sri Lankan High Commission "
            "in Ottawa is required. A sealed zinc-lined coffin and embalming "
            "certificate are required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025; "
            "Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'sri-lanka',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a Sri Lankan community, with nationals working in Rome, "
            "Milan, and other cities in domestic care, hospitality, and "
            "industry. Sri Lanka maintains an Embassy in Rome. When a Sri "
            "Lankan national dies in Italy and their family wishes to repatriate "
            "remains to Sri Lanka, the death is registered with the local comune "
            "(civil registry). The atto di morte requires certified English or "
            "Sinhala translation for Sri Lankan authorities. Sri Lanka is not "
            "a Hague Apostille Convention member; full consular authentication "
            "through the Sri Lankan Embassy in Rome is required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025; Italian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-korea', 'dest': 'sri-lanka',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korea and Sri Lanka maintain bilateral ties through trade, "
            "the Korean apparel and manufacturing sector's engagement with Sri "
            "Lankan textile industries, and bilateral labour agreements. The "
            "Sri Lankan Embassy in Seoul is fully operational. When a Sri Lankan "
            "national dies in South Korea and their family wishes to repatriate "
            "remains to Sri Lanka, the death is registered with the local gu "
            "office (ward office). Sri Lanka is not a Hague Apostille Convention "
            "member; full consular authentication through the Sri Lankan Embassy "
            "in Seoul is required. A sealed zinc-lined coffin and embalming "
            "certificate are required. "
            "(Sri Lankan Ministry of Foreign Affairs, 2025; South Korean "
            "Ministry of Foreign Affairs, 2025.)"
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
    dest_name_title = title_name(dest_name)
    slug = f"{origin_slug}-to-{dest_slug}"

    complexity = dm.get('complexity_override', od['complexity'])
    timeline_avg = dm.get('timeline_avg_override', od['timeline_avg'])
    timeline_fast = dm.get('timeline_fast_override', od['timeline_fast'])
    timeline_complex = dm.get('timeline_complex_override', od['timeline_complex'])
    doc_time = od['doc_time']
    dest_key = dm['key']

    desc_note = complexity_to_desc(complexity)
    t_origin = title_name(origin_name)
    t_dest = dm.get('short_title', dest_name_title)
    description = (
        f"Someone has died in {origin_name}. Repatriation to {dest_name} "
        f"takes {timeline_avg}. {desc_note} Contact us 24/7."
    )

    dest_reception = dm['reception']
    dest_consular = dm['consular_template'].format(city=embassy_city)
    arrival_faq = dm['arrival_faq']

    if origin_slug == 'united-kingdom':
        pt3 = (
            f"Contact the {dest_name_title} High Commission or Embassy in London "
            f"for documentation requirements. They cannot fund repatriation."
        )
        step1_timing = (
            "Day of death. Call 999 for emergency services. "
            f"Contact the {dest_name_title} High Commission or Embassy in London."
        )
        step3_action = f"{dest_name_title} High Commission or Embassy in London notified"
    elif origin_slug == 'ireland':
        pt3 = (
            f"Contact the {dest_name_title} High Commission or Embassy in Dublin "
            f"for documentation requirements. They cannot fund repatriation."
        )
        step1_timing = (
            "Day of death. Call 999 or 112 for emergency services. "
            f"Contact the {dest_name_title} High Commission or Embassy in Dublin."
        )
        step3_action = f"{dest_name_title} High Commission or Embassy in Dublin notified"
    else:
        pt3 = (
            f"British Embassy or High Commission in {embassy_city} registers "
            f"the death and advises. They cannot fund repatriation."
        )
        step1_timing = (
            f"Day of death. Call +44 (0)20 7008 5000 (FCDO) or {od['emergency']} "
            f"for local emergency services."
        )
        step3_action = f"{dest_name_title} Embassy in {embassy_city} notified"

    pts = [
        f"Key document: {od['cert_name']} (in {od['cert_lang']})",
        f"Documentation takes {doc_time}. Appoint a specialist on day one.",
        pt3,
        f"Death must be registered with {od['registry']} promptly.",
        (
            f"{dest_name_title} Embassy in {embassy_city} can advise on "
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
    action: "{dest_name_title} funeral director takes custody. Receiving funeral director coordinates with local authorities."
    timing: "Within 24 hours of arrival."
    responsible: "Receiving funeral director"
"""

    faqs = f"""  - question: "How long does repatriation from {origin_name} to {dest_name} take?"
    answer: "In a straightforward case, repatriation from {origin_name} to {dest_name} takes {timeline_avg}. The fastest cases complete in {timeline_fast}. Complex cases can take {timeline_complex} or longer."
  - question: "What should I know first about repatriation from {origin_name}?"
    answer: "Death must be registered with {od['registry']} promptly. {od['postmortem_trigger']} may add time before the body can be released."
  - question: "What documents are required for repatriation from {origin_name} to {dest_name}?"
    answer: "The core documents are: {od['cert_name']} with certified translation where required, embalming certificate, export permit, freedom from infection certificate, and passport of the deceased. Your repatriation coordinator handles obtaining these on your behalf."
  - question: "Does the {dest_name_title} Embassy in {origin_name} help with repatriation?"
    answer: "The {dest_name_title} Embassy in {embassy_city} can assist with document authentication and advise on repatriation requirements. They cannot pay for or arrange repatriation. Contact the {dest_name_title} Embassy in {embassy_city} as soon as possible after the death."
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
