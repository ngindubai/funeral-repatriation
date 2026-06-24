#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R83-R84.

   R83 (25 routes, START_VARIANT=2=C):
     Egypt x5:    united-kingdom, united-states, australia, netherlands, canada
     Pakistan x5: india, italy, australia, canada, netherlands
     Thailand x5: australia, germany, canada, italy, netherlands
     China x5:    germany, france, italy, japan, south-korea
     Morocco x5:  germany, italy, united-states, canada, portugal

   R84 (25 routes, continues from R83):
     Bangladesh x5: united-states, canada, france, australia, india
     Nigeria x5:    canada, australia, spain, netherlands, sweden
     Kenya x5:      canada, italy, netherlands, sweden, norway
     Ghana x5:      france, canada, australia, sweden, norway
     Vietnam x5:    united-kingdom, italy, south-korea, japan, netherlands

   Template rotation: R82 ended on variant B (idx=1). R83 starts at C (idx=2).
   START_VARIANT=2 applies across all 50 routes as one continuous cycle.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 2  # C

DEST_META = {
    'egypt': {
        'name': 'Egypt',
        'slug': 'egypt',
        'key': 'eg',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
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
            "The Egyptian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Egypt. The Embassy cannot pay for "
            "or arrange repatriation. Egypt is not a Hague Apostille Convention "
            "member; all foreign documents require full consular authentication."
        ),
        'arrival_faq': (
            "The Egyptian funeral director takes custody at Cairo International "
            "Airport (CAI) cargo terminal. The Civil Status Authority (Maslahat "
            "al-Ahwal al-Madaniyya) registers the death. The niyaba (public "
            "prosecutor) may be involved where the cause of death is unclear. All "
            "foreign documents require certified Arabic translation and authentication "
            "by the Egyptian Embassy in the origin country. An embalming certificate "
            "and hermetically sealed coffin are required. Cremation is not available "
            "in Egypt; burial is the only option."
        ),
        'emergency_line': 'contact the Egyptian Embassy in the origin country',
        'hub_url': 'repatriation-from-egypt',
    },
    'pakistan': {
        'name': 'Pakistan',
        'slug': 'pakistan',
        'key': 'pk',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
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
            "The Pakistani High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Pakistan. Pakistan is "
            "not a Hague Apostille Convention member; full consular authentication "
            "is required. The High Commission cannot pay for or arrange repatriation."
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
    'thailand': {
        'name': 'Thailand',
        'slug': 'thailand',
        'key': 'th',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
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
            "The Thai Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Thailand. Thailand is not a Hague "
            "Apostille Convention member; full consular legalisation through the "
            "Thai Embassy in {city} is required. The Embassy cannot pay for or "
            "arrange repatriation."
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
        'complexity_override': 'moderate-high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-16 weeks',
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
            "The Chinese Embassy or Consulate in {city} can advise on documentation "
            "requirements and legalisation for repatriation to China. China is not "
            "a Hague Apostille member; all documents must be legalised through the "
            "Chinese Embassy in {city}. The Embassy cannot pay for or arrange "
            "repatriation."
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
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
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
            "The Moroccan Embassy or Consulate in {city} can advise on documentation "
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
    'bangladesh': {
        'name': 'Bangladesh',
        'slug': 'bangladesh',
        'key': 'bd',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
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
            "The Bangladeshi High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Bangladesh. Bangladesh "
            "is not a Hague Apostille Convention member; full consular authentication "
            "through the High Commission in {city} is required. The High Commission "
            "cannot pay for or arrange repatriation."
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
    'nigeria': {
        'name': 'Nigeria',
        'slug': 'nigeria',
        'key': 'ng',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Nigerian funeral director takes custody at Murtala Muhammed "
            "International Airport Lagos (LOS) or Nnamdi Azikiwe International "
            "Airport Abuja (ABV) cargo terminal, depending on the family's "
            "destination. The National Population Commission (NPC) handles civil "
            "registration of deaths. Ministry of Health clearance is required "
            "before final disposition. For Muslim remains, Islamic law procedures "
            "apply and prompt burial is expected. All foreign documents require "
            "certified English translation where applicable; English is Nigeria's "
            "official language, which simplifies documentation from "
            "English-speaking origin countries. Nigeria is not a member of the "
            "Hague Apostille Convention; full consular authentication through the "
            "Nigerian High Commission or Embassy in the country of origin is "
            "required. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Nigerian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Nigeria. Nigeria is not "
            "a Hague Apostille Convention member; full consular authentication "
            "through the High Commission in {city} is required. The High Commission "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Nigerian funeral director takes custody at Murtala Muhammed "
            "International Airport Lagos (LOS) or Nnamdi Azikiwe International "
            "Airport Abuja (ABV) cargo terminal. The National Population "
            "Commission (NPC) handles civil registration. Ministry of Health "
            "clearance is required before final disposition. For Muslim remains, "
            "Islamic law procedures apply and prompt burial is expected. Nigeria "
            "is not a Hague Apostille member; full consular authentication "
            "through the Nigerian High Commission or Embassy in the origin "
            "country is required. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Nigerian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-nigeria',
    },
    'kenya': {
        'name': 'Kenya',
        'slug': 'kenya',
        'key': 'ke',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Kenyan funeral director takes custody at Jomo Kenyatta "
            "International Airport Nairobi (NBO) cargo terminal. The Civil "
            "Registration Department (CRD) under the Registrar General handles "
            "death registration. Ministry of Health clearance is required before "
            "final disposition. Kenya joined the Hague Apostille Convention in "
            "2021; apostille certificates are accepted for documents from member "
            "states. All other foreign documents require full consular "
            "authentication through the Kenyan High Commission or Embassy in "
            "the country of origin. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. English is Kenya's "
            "official language, which simplifies documentation from "
            "English-speaking origin countries. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025.)"
        ),
        'consular_template': (
            "The Kenyan High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Kenya. Kenya joined "
            "the Hague Apostille Convention in 2021; apostille certificates from "
            "member states are accepted. The High Commission cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Kenyan funeral director takes custody at Jomo Kenyatta "
            "International Airport Nairobi (NBO) cargo terminal. The Civil "
            "Registration Department (CRD) registers the death. Ministry of "
            "Health clearance is required before final disposition. Kenya joined "
            "the Hague Apostille Convention in 2021; apostille certificates are "
            "accepted from member states. All other documents require full "
            "consular authentication through the Kenyan High Commission or "
            "Embassy in the origin country. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Kenyan High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-kenya',
    },
    'ghana': {
        'name': 'Ghana',
        'slug': 'ghana',
        'key': 'gh',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Ghanaian funeral director takes custody at Kotoka International "
            "Airport Accra (ACC) cargo terminal. The Births and Deaths Registry "
            "(BDR) under the Registrar General's Department handles death "
            "registration. Ministry of Health clearance is required before final "
            "disposition. Ghana is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Ghanaian High "
            "Commission or Embassy in the country of origin is required. English "
            "is Ghana's official language, which simplifies documentation from "
            "English-speaking origin countries. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Ghanaian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Ghanaian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Ghana. Ghana is not "
            "a Hague Apostille Convention member; full consular authentication "
            "through the High Commission in {city} is required. The High Commission "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Ghanaian funeral director takes custody at Kotoka International "
            "Airport Accra (ACC) cargo terminal. The Births and Deaths Registry "
            "(BDR) under the Registrar General's Department registers the death. "
            "Ministry of Health clearance is required before final disposition. "
            "Ghana is not a Hague Apostille member; full consular authentication "
            "through the Ghanaian High Commission or Embassy in the origin "
            "country is required. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Ghanaian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-ghana',
    },
    'vietnam': {
        'name': 'Vietnam',
        'slug': 'vietnam',
        'key': 'vn',
        'complexity_override': 'moderate-high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-16 weeks',
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
            "The Vietnamese Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Vietnam. Vietnam is "
            "not a Hague Apostille Convention member; legalisation of origin "
            "country documents must go through the Vietnamese Embassy in {city}. "
            "The Embassy cannot pay for or arrange repatriation."
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
    'japan': {
        'name': 'Japan',
        'emergency': '110 (police) / 119 (fire and ambulance)',
        'registry': 'the local kuyakusho (ward office) or town hall civil registry',
        'cert_name': 'shibo todoke (death notification)',
        'cert_lang': 'Japanese',
        'overview': (
            "Call 110 for police or 119 for fire and ambulance. Death is "
            "certified by a physician. The shibo todoke (death notification) "
            "is submitted to the local kuyakusho (ward office) or town hall "
            "civil registry within 7 days of death under the Family Register Act. "
            "Police take jurisdiction for violent or unexplained deaths; the public "
            "prosecutor orders an autopsy where required. Japan joined the Hague "
            "Apostille Convention in 1970; apostille certificates are accepted. "
            "The British Embassy in Tokyo can assist British nationals."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation is the near-universal method of disposition in Japan. "
            "The kotsuage ceremony of collecting ashes is integral to Japanese "
            "Buddhist tradition and is conducted before any international "
            "repatriation of cremated remains."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (police take jurisdiction; autopsy ordered by public prosecutor)',
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
}

ROUTES = [
    # R83 -- Egypt x5
    {
        'origin': 'united-kingdom', 'dest': 'egypt',
        'embassy_city': 'London',
        'intro': (
            "Egypt is a significant destination for British nationals, attracting "
            "large numbers of tourists to the Red Sea resorts, the Nile valley, "
            "and historic sites. A small British expat community lives and works "
            "in Cairo and Alexandria. The Egyptian Embassy in London is fully "
            "operational. When someone from the United Kingdom dies in Egypt and "
            "their family wishes to repatriate remains, the death is registered "
            "with the Civil Status Authority (Maslahat al-Ahwal al-Madaniyya). "
            "Egypt is not a Hague Apostille Convention member; UK documents require "
            "full consular authentication. The British Embassy in Cairo can assist. "
            "Cremation is not available in Egypt; full body repatriation is required. "
            "(FCDO Travel Advice: Egypt, 2025; Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'egypt',
        'embassy_city': 'Washington DC',
        'intro': (
            "Egypt is a destination for American tourists and a country with "
            "historical ties to the United States through diplomatic engagement "
            "and archaeological research partnerships. American nationals visit "
            "for tourism, academic study, and work in international organisations. "
            "The Egyptian Embassy in Washington DC is fully operational. When an "
            "American national dies in Egypt and their family wishes to repatriate "
            "remains, the death is registered with the Civil Status Authority "
            "(Maslahat al-Ahwal al-Madaniyya). Egypt is not a Hague Apostille "
            "member; US documents require full consular authentication. Cremation "
            "is not available in Egypt; full body repatriation is the only option. "
            "(US Department of State Egypt Travel Advisory, 2025; Egyptian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'egypt',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals travel to Egypt for tourism, diving in the Red "
            "Sea, and visits to historical sites including the pyramids and Luxor. "
            "Australia maintains an Embassy in Cairo. When an Australian national "
            "dies in Egypt and their family wishes to repatriate remains to "
            "Australia, the death is registered with the Civil Status Authority "
            "(Maslahat al-Ahwal al-Madaniyya). Egypt is not a Hague Apostille "
            "Convention member; Australian documents require full consular "
            "authentication by the Egyptian Embassy in Canberra. Cremation is "
            "not available in Egypt; full body repatriation is required. "
            "(DFAT Travel Advice: Egypt, 2025; Egyptian Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'egypt',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals travel to Egypt for tourism, particularly to Red Sea "
            "resorts, and the Netherlands has active archaeological research ties "
            "with Egypt. The Netherlands maintains an Embassy in Cairo. When a "
            "Dutch national dies in Egypt and their family wishes to repatriate "
            "remains to the Netherlands, the death is registered with the Civil "
            "Status Authority (Maslahat al-Ahwal al-Madaniyya). The akte van "
            "overlijden issued in the Netherlands requires certified Arabic "
            "translation for Egyptian authorities. Egypt is not a Hague Apostille "
            "member; Dutch documents require full consular authentication by the "
            "Egyptian Embassy in The Hague. Cremation is not available in Egypt. "
            "(Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'egypt',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals travel to Egypt for tourism and the country has "
            "an active Egyptian-Canadian diaspora community. Canada maintains an "
            "Embassy in Cairo. When a Canadian national dies in Egypt and their "
            "family wishes to repatriate remains to Canada, the death is registered "
            "with the Civil Status Authority (Maslahat al-Ahwal al-Madaniyya). "
            "Egypt is not a Hague Apostille Convention member; Canadian documents "
            "require full consular authentication by the Egyptian Embassy in Ottawa. "
            "Canada joined the Hague Apostille Convention in November 2024. "
            "Cremation is not available in Egypt; full body repatriation is required. "
            "(Global Affairs Canada Egypt Travel Advice, 2025; Egyptian Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    # R83 -- Pakistan x5
    {
        'origin': 'india', 'dest': 'pakistan',
        'embassy_city': 'New Delhi',
        'intro': (
            "India and Pakistan share the longest land border between any two "
            "predominantly Muslim and Hindu nations, and family ties across the "
            "partition divide remain significant for many British and Indian "
            "diaspora families. The Pakistan High Commission in New Delhi handles "
            "consular matters. When an Indian national dies and their family "
            "wishes to repatriate remains to Pakistan, or where cross-border family "
            "connections exist, the death is registered with the local Registrar "
            "of Births and Deaths under the Indian state civil registration system. "
            "Pakistan is not a Hague Apostille Convention member; full consular "
            "authentication is required. The Pakistan High Commission in New Delhi "
            "can advise on documentation. "
            "(Pakistan Ministry of Foreign Affairs, 2025; FCDO guidance on South "
            "Asia repatriation, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'pakistan',
        'embassy_city': 'Rome',
        'intro': (
            "Italy hosts one of the largest Pakistani diaspora communities in "
            "southern Europe, concentrated in cities including Rome, Milan, Turin, "
            "and Brescia. Pakistani nationals work across agriculture, hospitality, "
            "textiles, and manufacturing. The Pakistani Embassy in Rome is fully "
            "operational. When a Pakistani national dies in Italy and their family "
            "wishes to repatriate remains to Pakistan, the death is registered "
            "with the local comune (civil registry). The atto di morte requires "
            "certified Urdu or English translation. Pakistan is not a Hague "
            "Apostille member; Italian documents require full authentication by the "
            "Pakistani Embassy in Rome. "
            "(Pakistan Ministry of Foreign Affairs, 2025; Italian Ministry of "
            "Interior, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'pakistan',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia hosts a significant Pakistani-Australian community, with "
            "families concentrated in Sydney, Melbourne, and Brisbane. Pakistani "
            "nationals travel to Australia for education, work, and family visits. "
            "The Pakistani High Commission in Canberra is fully operational. "
            "When a Pakistani national dies in Australia and their family "
            "wishes to repatriate remains to Pakistan, the death is registered "
            "with the state or territory Births, Deaths and Marriages (BDM) "
            "registry. Australia is a Hague Apostille Convention member; Pakistan "
            "is not, so full consular authentication by the Pakistani High "
            "Commission in Canberra is required for Australian documents. "
            "(Pakistan Ministry of Foreign Affairs, 2025; DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'pakistan',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts one of the world's largest Pakistani diaspora communities, "
            "concentrated in Toronto, Mississauga, and Vancouver. Pakistani-Canadians "
            "maintain strong family and cultural connections to Pakistan, and "
            "bilateral travel is regular. The Pakistani High Commission in Ottawa "
            "is fully operational. When a Pakistani national dies in Canada and "
            "their family wishes to repatriate remains to Pakistan, the death is "
            "registered with the provincial civil registration authority. Canada "
            "joined the Hague Apostille Convention in November 2024; Pakistan is "
            "not a member, so full consular authentication by the Pakistani High "
            "Commission in Ottawa is required. "
            "(Pakistan Ministry of Foreign Affairs, 2025; Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'pakistan',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a significant Pakistani community, with families "
            "settled across Rotterdam, Amsterdam, and The Hague in textile, "
            "catering, and services sectors. The Pakistani Embassy in The Hague "
            "is fully operational. When a Pakistani national dies in the Netherlands "
            "and their family wishes to repatriate remains to Pakistan, the death "
            "is registered with the local gemeente (municipal civil registry). "
            "The akte van overlijden requires certified Urdu or English translation. "
            "Pakistan is not a Hague Apostille member; Dutch documents require full "
            "authentication by the Pakistani Embassy in The Hague. "
            "(Pakistan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R83 -- Thailand x5
    {
        'origin': 'australia', 'dest': 'thailand',
        'embassy_city': 'Canberra',
        'intro': (
            "Thailand is one of Australia's most popular international tourism "
            "destinations, with millions of Australian visitors each year to "
            "Bangkok, Phuket, Chiang Mai, and Koh Samui. An established "
            "Australian expat community also lives in Thailand, particularly "
            "in Bangkok and Pattaya. The Australian Embassy in Bangkok is "
            "fully operational. When an Australian national dies in Thailand "
            "and their family wishes to repatriate remains to Australia, the "
            "death is registered with DOPA (Department of Provincial Administration) "
            "Civil Registration Division. Thailand is not a Hague Apostille member; "
            "the Thai Embassy in Canberra can advise on consular legalisation. "
            "(DFAT Travel Advice: Thailand, 2025; Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'thailand',
        'embassy_city': 'Berlin',
        'intro': (
            "Thailand is a major tourism and retirement destination for German "
            "nationals, with a substantial German community living long-term in "
            "Bangkok, Phuket, and Pattaya. Germany maintains an Embassy in Bangkok. "
            "When a German national dies in Thailand and their family wishes to "
            "repatriate remains to Germany, the death is registered with the DOPA "
            "(Department of Provincial Administration) Civil Registration Division. "
            "The Sterbeurkunde issued in Germany requires certified Thai translation "
            "for Thai authorities. Thailand is not a Hague Apostille member; "
            "the Thai Embassy in Berlin can advise on consular legalisation. "
            "(FCDO Travel Advice: Thailand, 2025; Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'thailand',
        'embassy_city': 'Ottawa',
        'intro': (
            "Thailand is a popular destination for Canadian tourists, retirees, "
            "and Canadians teaching English abroad. A Canadian expat community is "
            "established in Bangkok and in the northern cities. The Canadian Embassy "
            "in Bangkok is fully operational. When a Canadian national dies in "
            "Thailand and their family wishes to repatriate remains to Canada, "
            "the death is registered with the DOPA Civil Registration Division. "
            "Thailand is not a Hague Apostille Convention member; the Thai Embassy "
            "in Ottawa can advise on consular legalisation requirements for "
            "Canadian documents. Canada joined the Hague Apostille Convention in "
            "November 2024. "
            "(Global Affairs Canada Thailand Travel Advice, 2025; Thai Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'thailand',
        'embassy_city': 'Rome',
        'intro': (
            "Thailand is a growing destination for Italian tourists and retirees, "
            "with Bangkok and Koh Samui popular on Italian itineraries. Italy "
            "maintains an Embassy in Bangkok. When an Italian national dies in "
            "Thailand and their family wishes to repatriate remains to Italy, the "
            "death is registered with the DOPA (Department of Provincial "
            "Administration) Civil Registration Division. The atto di morte requires "
            "certified Thai translation for Thai authorities. Thailand is not a "
            "Hague Apostille member; the Thai Embassy in Rome can advise on "
            "consular legalisation requirements. "
            "(Italian Ministry of Foreign Affairs, 2025; Thai Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'thailand',
        'embassy_city': 'The Hague',
        'intro': (
            "Thailand is popular with Dutch tourists and long-term residents, "
            "particularly in Bangkok, Phuket, and Chiang Mai. The Netherlands "
            "maintains an Embassy in Bangkok. When a Dutch national dies in "
            "Thailand and their family wishes to repatriate remains to the "
            "Netherlands, the death is registered with the DOPA Civil Registration "
            "Division. The akte van overlijden requires certified Thai translation "
            "for Thai authorities. Thailand is not a Hague Apostille member; "
            "the Thai Embassy in The Hague can advise on consular legalisation. "
            "(Netherlands Ministry of Foreign Affairs, 2025; Thai Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    # R83 -- China x5
    {
        'origin': 'germany', 'dest': 'china',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and China maintain significant bilateral economic ties, "
            "with Germany one of China's largest European trading partners. "
            "German nationals work in China in automotive, engineering, chemicals, "
            "and finance, and Chinese students and professionals are present in "
            "Germany. Germany maintains an Embassy in Beijing and Consulates in "
            "Shanghai, Guangzhou, and Chengdu. When a German national dies in "
            "China and their family wishes to repatriate remains to Germany, "
            "the death must be registered and quarantine clearance obtained through "
            "the General Administration of Customs. China is not a Hague Apostille "
            "member; the Chinese Embassy in Berlin can advise on document legalisation. "
            "(FCDO Travel Advice: China, 2025; Chinese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'china',
        'embassy_city': 'Paris',
        'intro': (
            "France and China maintain strong bilateral trade and cultural ties, "
            "with French nationals working in China in luxury goods, aerospace, "
            "pharmaceuticals, and financial services. A French expat community "
            "is established in Shanghai and Beijing. France maintains an Embassy "
            "in Beijing and Consulates in Shanghai and Guangzhou. When a French "
            "national dies in China and their family wishes to repatriate remains "
            "to France, the death must be registered and quarantine clearance "
            "obtained through the General Administration of Customs. China is "
            "not a Hague Apostille member; the Chinese Embassy in Paris can "
            "advise on document legalisation. "
            "(French Ministry of Foreign Affairs, 2025; Chinese Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'china',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and China share significant bilateral ties, including a large "
            "Chinese community in Italian cities such as Prato, Milan, and Rome, "
            "and Italian nationals working in China in fashion, luxury goods, and "
            "manufacturing. Italy maintains an Embassy in Beijing and Consulates "
            "in Shanghai and Guangzhou. When an Italian national dies in China "
            "and their family wishes to repatriate remains to Italy, the death "
            "must be registered and quarantine clearance obtained through the "
            "General Administration of Customs. China is not a Hague Apostille "
            "member; the Chinese Embassy in Rome can advise on document legalisation. "
            "(Italian Ministry of Foreign Affairs, 2025; Chinese Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'china',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japan and China are close geographic neighbours with deeply intertwined "
            "trade and cultural histories. Japanese nationals work extensively in "
            "China in manufacturing, automotive, electronics, and finance, and "
            "a substantial Japanese expat community is established in Shanghai, "
            "Beijing, and Guangzhou. Japan maintains an Embassy in Beijing and "
            "Consulates in major Chinese cities. When a Japanese national dies in "
            "China and their family wishes to repatriate remains to Japan, the "
            "death must be registered and quarantine clearance obtained through "
            "the General Administration of Customs. China is not a Hague Apostille "
            "member; the Chinese Embassy in Tokyo can advise on document legalisation. "
            "Japan joined the Hague Apostille Convention in 1970. "
            "(Japan Ministry of Foreign Affairs, 2025; Chinese Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-korea', 'dest': 'china',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korea and China share an active bilateral economic relationship, "
            "with South Korean nationals working and studying in China in technology, "
            "manufacturing, and financial services. A large Korean-Chinese (joseonjok) "
            "community also maintains cross-border connections. South Korea "
            "maintains an Embassy in Beijing and Consulates in Shanghai, Qingdao, "
            "Guangzhou, and Shenyang. When a South Korean national dies in China "
            "and their family wishes to repatriate remains to South Korea, the "
            "death must be registered and quarantine clearance obtained through "
            "the General Administration of Customs. China is not a Hague Apostille "
            "member; the Chinese Embassy in Seoul can advise on document legalisation. "
            "(South Korean Ministry of Foreign Affairs, 2025; Chinese Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    # R83 -- Morocco x5
    {
        'origin': 'germany', 'dest': 'morocco',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to one of the largest Moroccan diaspora communities "
            "in Europe, with Moroccan-Germans concentrated in cities including "
            "Berlin, Cologne, Frankfurt, and Munich. Bilateral ties between the "
            "two countries include strong trade and cultural links. Germany "
            "maintains an Embassy in Rabat. When a Moroccan national dies in "
            "Germany and their family wishes to repatriate remains to Morocco, "
            "the death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde requires certified Arabic translation for Moroccan "
            "authorities. Morocco joined the Hague Apostille Convention in 2021; "
            "German documents can be apostilled. "
            "(Moroccan Ministry of Foreign Affairs, 2025; German Federal Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'morocco',
        'embassy_city': 'Rome',
        'intro': (
            "Italy is home to a significant Moroccan community, one of the largest "
            "migrant groups in Italy, concentrated in northern cities including "
            "Milan, Turin, and Brescia, and in the south. Italy maintains an "
            "Embassy in Rabat. When a Moroccan national dies in Italy and their "
            "family wishes to repatriate remains to Morocco, the death is registered "
            "with the local comune (civil registry). The atto di morte requires "
            "certified Arabic translation for Moroccan authorities. Morocco joined "
            "the Hague Apostille Convention in 2021; Italian documents can be "
            "apostilled, simplifying the process compared with non-Hague routes. "
            "(Moroccan Ministry of Foreign Affairs, 2025; Italian Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'morocco',
        'embassy_city': 'Washington DC',
        'intro': (
            "Morocco and the United States maintain close bilateral ties, including "
            "a long-standing friendship treaty and active trade, military, and "
            "cultural partnerships. American nationals travel to Morocco for tourism, "
            "academic programmes, and business. The Moroccan Embassy in Washington "
            "DC is fully operational. When an American national dies in Morocco "
            "and their family wishes to repatriate remains to the United States, "
            "the death is registered with the local etat civil (civil registry). "
            "Morocco joined the Hague Apostille Convention in 2021; the United "
            "States joined in 1981. Both countries are now Hague members, "
            "simplifying document authentication. "
            "(Moroccan Ministry of Foreign Affairs, 2025; US Department of State, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'morocco',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has an active Moroccan-Canadian community, with families settled "
            "in Montreal, Toronto, and other major cities. Canada maintains an "
            "Embassy in Rabat. When a Moroccan national dies in Canada and their "
            "family wishes to repatriate remains to Morocco, the death is registered "
            "with the provincial civil registration authority. Morocco joined the "
            "Hague Apostille Convention in 2021; Canada joined in November 2024. "
            "Both countries are now Hague members, which simplifies document "
            "authentication for this corridor. "
            "(Moroccan Ministry of Foreign Affairs, 2025; Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'morocco',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Morocco are close Atlantic neighbours with historical "
            "and cultural ties dating to the Moorish period and the Reconquista. "
            "Moroccan nationals live and work in Portugal, and Portugal maintains "
            "an Embassy in Rabat. When a Moroccan national dies in Portugal and "
            "their family wishes to repatriate remains to Morocco, the death is "
            "registered with the local Conservatoria do Registo Civil. The assento "
            "de obito requires certified Arabic translation for Moroccan authorities. "
            "Morocco joined the Hague Apostille Convention in 2021; Portugal "
            "joined in 1970. Both are Hague members, simplifying document "
            "authentication. "
            "(Moroccan Ministry of Foreign Affairs, 2025; Portuguese Ministry of "
            "Justice, 2025.)"
        ),
    },
    # R84 -- Bangladesh x5
    {
        'origin': 'united-states', 'dest': 'bangladesh',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States is home to one of the world's largest Bangladeshi "
            "diaspora communities, with families concentrated in New York City "
            "(particularly the Bronx and Queens), Los Angeles, and Washington DC. "
            "The Bangladeshi Embassy in Washington DC is fully operational. When "
            "a Bangladeshi national dies in the United States and their family "
            "wishes to repatriate remains to Bangladesh, the death is registered "
            "with the state civil records office. Bangladesh is not a Hague "
            "Apostille Convention member; full consular authentication through "
            "the Bangladeshi Embassy in Washington DC is required. A sealed "
            "zinc-lined coffin is required for all repatriations. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025; US Department of "
            "State, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'bangladesh',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a substantial Bangladeshi-Canadian community, with "
            "families concentrated in Toronto, Vancouver, and Calgary. The "
            "Bangladeshi High Commission in Ottawa is fully operational. When "
            "a Bangladeshi national dies in Canada and their family wishes to "
            "repatriate remains to Bangladesh, the death is registered with "
            "the provincial civil registration authority. Bangladesh is not a "
            "Hague Apostille Convention member; full consular authentication "
            "through the Bangladeshi High Commission in Ottawa is required. "
            "Canada joined the Hague Apostille Convention in November 2024. "
            "A sealed zinc-lined coffin is required for all repatriations. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'bangladesh',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Bangladeshi community concentrated in Paris, with "
            "nationals working in hospitality, retail, and services. The "
            "Bangladeshi Embassy in Paris is fully operational. When a "
            "Bangladeshi national dies in France and their family wishes to "
            "repatriate remains to Bangladesh, the death is registered with "
            "the local mairie (town hall). The acte de deces requires certified "
            "Bengali or English translation for Bangladeshi authorities. "
            "Bangladesh is not a Hague Apostille Convention member; full "
            "consular authentication through the Bangladeshi Embassy in Paris "
            "is required. A sealed zinc-lined coffin is required. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'bangladesh',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia hosts a growing Bangladeshi-Australian community, with "
            "nationals concentrated in Sydney and Melbourne. Bangladesh maintains "
            "a High Commission in Canberra. When a Bangladeshi national dies in "
            "Australia and their family wishes to repatriate remains to Bangladesh, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Bangladesh is not a Hague Apostille "
            "Convention member; full consular authentication through the Bangladeshi "
            "High Commission in Canberra is required for Australian documents. "
            "A sealed zinc-lined coffin is required for all repatriations. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025; DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'india', 'dest': 'bangladesh',
        'embassy_city': 'New Delhi',
        'intro': (
            "India and Bangladesh share a long border and deep historical, "
            "cultural, and migration ties, particularly between West Bengal "
            "and Bangladesh. Cross-border family connections are common among "
            "communities on both sides. The Bangladeshi High Commission in "
            "New Delhi is fully operational. When an Indian national with "
            "Bangladeshi family connections dies and their family wishes to "
            "repatriate remains to Bangladesh, or for Bangladeshi nationals "
            "who die in India, the death is registered with the local Registrar "
            "of Births and Deaths in India. Bangladesh is not a Hague Apostille "
            "member; full consular authentication through the Bangladeshi High "
            "Commission in New Delhi is required. A sealed zinc-lined coffin "
            "is required. "
            "(Bangladeshi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R84 -- Nigeria x5
    {
        'origin': 'canada', 'dest': 'nigeria',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada is home to a growing Nigerian-Canadian community, with "
            "nationals concentrated in Toronto, Calgary, and Edmonton in "
            "healthcare, technology, and professional services. The Nigerian "
            "High Commission in Ottawa is fully operational. When a Nigerian "
            "national dies in Canada and their family wishes to repatriate "
            "remains to Nigeria, the death is registered with the provincial "
            "civil registration authority. Nigeria is not a Hague Apostille "
            "Convention member; full consular authentication through the Nigerian "
            "High Commission in Ottawa is required. Canada joined the Hague "
            "Apostille Convention in November 2024. "
            "(Nigerian Ministry of Foreign Affairs, 2025; Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'nigeria',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has an established Nigerian-Australian community, with "
            "nationals working in healthcare, education, and information technology. "
            "Nigeria maintains a High Commission in Canberra. When a Nigerian "
            "national dies in Australia and their family wishes to repatriate "
            "remains to Nigeria, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. Nigeria is "
            "not a Hague Apostille Convention member; full consular authentication "
            "through the Nigerian High Commission in Canberra is required for "
            "Australian documents. "
            "(Nigerian Ministry of Foreign Affairs, 2025; DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'nigeria',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain is home to a Nigerian community concentrated in Madrid, "
            "Valencia, and Barcelona, working in hospitality, construction, "
            "and services. Nigeria maintains an Embassy in Madrid. When a "
            "Nigerian national dies in Spain and their family wishes to "
            "repatriate remains to Nigeria, the death is registered with the "
            "local Registro Civil (civil registry). The certificado de defuncion "
            "requires certified English translation where needed for the Nigerian "
            "National Population Commission. Nigeria is not a Hague Apostille "
            "member; Spanish documents require full consular authentication through "
            "the Nigerian Embassy in Madrid. "
            "(Nigerian Ministry of Foreign Affairs, 2025; Spanish Ministry of "
            "Justice, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'nigeria',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has an active Nigerian-Dutch community, with nationals "
            "working across Rotterdam, Amsterdam, and The Hague in trade, "
            "logistics, and services. Nigeria maintains an Embassy in The Hague. "
            "When a Nigerian national dies in the Netherlands and their family "
            "wishes to repatriate remains to Nigeria, the death is registered "
            "with the local gemeente (municipal civil registry). The akte van "
            "overlijden requires certified English translation for the Nigerian "
            "National Population Commission. Nigeria is not a Hague Apostille "
            "member; Dutch documents require full authentication through the "
            "Nigerian Embassy in The Hague. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'nigeria',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a Nigerian community, with nationals working in Stockholm "
            "and other major cities in healthcare, academia, and information "
            "technology. Nigeria maintains an Embassy in Stockholm. When a "
            "Nigerian national dies in Sweden and their family wishes to repatriate "
            "remains to Nigeria, the death is registered with the Swedish Tax "
            "Agency (Skatteverket) Population Register. The dodsfallsintyg requires "
            "certified English translation for Nigerian authorities. Nigeria is not "
            "a Hague Apostille member; Swedish documents require full authentication "
            "through the Nigerian Embassy in Stockholm. "
            "(Nigerian Ministry of Foreign Affairs, 2025; Skatteverket, Sweden, 2025.)"
        ),
    },
    # R84 -- Kenya x5
    {
        'origin': 'canada', 'dest': 'kenya',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has an established Kenyan-Canadian community, with nationals "
            "working in Toronto, Ottawa, and Vancouver in healthcare, education, "
            "and technology. Kenya maintains a High Commission in Ottawa. When "
            "a Kenyan national dies in Canada and their family wishes to repatriate "
            "remains to Kenya, the death is registered with the provincial civil "
            "registration authority. Kenya joined the Hague Apostille Convention "
            "in 2021; Canada joined in November 2024. Both countries are now "
            "Hague members, which simplifies document authentication for this "
            "corridor. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025; "
            "Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'kenya',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has bilateral ties with Kenya through trade, tourism, and "
            "development cooperation, and Italian nationals travel to Kenya for "
            "safari tourism and conservation work. A Kenyan community is established "
            "in Italy. Kenya maintains an Embassy in Rome. When a Kenyan national "
            "dies in Italy and their family wishes to repatriate remains to Kenya, "
            "the death is registered with the local comune (civil registry). "
            "Kenya joined the Hague Apostille Convention in 2021; Italy joined in "
            "1978. Both countries are Hague members, which simplifies document "
            "authentication. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025; "
            "Italian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'kenya',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Kenya maintain active bilateral ties through "
            "trade, development cooperation, and horticulture exports, with Dutch "
            "investment significant in Kenya's flower and vegetable export sectors. "
            "The Netherlands maintains an Embassy in Nairobi. When a Kenyan "
            "national dies in the Netherlands and their family wishes to repatriate "
            "remains to Kenya, the death is registered with the local gemeente "
            "(municipal civil registry). Kenya joined the Hague Apostille Convention "
            "in 2021; the Netherlands joined in 1960. Both are Hague members. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025; "
            "Netherlands Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'kenya',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Kenya have development cooperation ties, and Swedish "
            "nationals travel to Kenya for safari tourism and NGO work. A Kenyan "
            "community is established in Sweden. Kenya maintains an Embassy in "
            "Stockholm. When a Kenyan national dies in Sweden and their family "
            "wishes to repatriate remains to Kenya, the death is registered with "
            "the Swedish Tax Agency (Skatteverket) Population Register. Kenya "
            "joined the Hague Apostille Convention in 2021; Sweden joined in "
            "1999. Both are Hague members, which simplifies document authentication. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025; "
            "Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'kenya',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Kenya have long-standing development cooperation and "
            "conservation partnerships, with Norwegian NGOs active in Kenya's "
            "conservation and humanitarian sectors. Norwegian nationals travel "
            "to Kenya for tourism and voluntary work. The Norwegian Embassy in "
            "Nairobi is fully operational. When a Kenyan national dies in Norway "
            "and their family wishes to repatriate remains to Kenya, the death "
            "is registered with Folkeregisteret (the civil registration system "
            "administered by Skatteetaten). Kenya joined the Hague Apostille "
            "Convention in 2021; Norway joined in 1980. Both are Hague members. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025; "
            "Skatteetaten, Norway, 2025.)"
        ),
    },
    # R84 -- Ghana x5
    {
        'origin': 'france', 'dest': 'ghana',
        'embassy_city': 'Paris',
        'intro': (
            "France has bilateral ties with Ghana through trade, Francophone "
            "West African regional networks, and development cooperation. A "
            "Ghanaian community is established in Paris and other French cities. "
            "Ghana maintains an Embassy in Paris. When a Ghanaian national dies "
            "in France and their family wishes to repatriate remains to Ghana, "
            "the death is registered with the local mairie (town hall). The acte "
            "de deces requires certified English translation for the Births and "
            "Deaths Registry (BDR) in Ghana. Ghana is not a Hague Apostille "
            "member; French documents require full consular authentication through "
            "the Ghanaian Embassy in Paris. "
            "(Ghanaian Ministry of Foreign Affairs, 2025; French Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'ghana',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts a substantial Ghanaian-Canadian community, with nationals "
            "concentrated in Toronto, Ottawa, and Calgary working in healthcare, "
            "construction, and professional services. The Ghanaian High Commission "
            "in Ottawa is fully operational. When a Ghanaian national dies in "
            "Canada and their family wishes to repatriate remains to Ghana, the "
            "death is registered with the provincial civil registration authority. "
            "Ghana is not a Hague Apostille Convention member; full consular "
            "authentication through the Ghanaian High Commission in Ottawa is "
            "required. Canada joined the Hague Apostille Convention in November "
            "2024. "
            "(Ghanaian Ministry of Foreign Affairs, 2025; Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'ghana',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Ghanaian-Australian community, with nationals "
            "working in mining, healthcare, and professional services across "
            "Perth, Sydney, and Melbourne. Ghana maintains a High Commission "
            "in Canberra. When a Ghanaian national dies in Australia and their "
            "family wishes to repatriate remains to Ghana, the death is registered "
            "with the state or territory Births, Deaths and Marriages (BDM) "
            "registry. Ghana is not a Hague Apostille Convention member; full "
            "consular authentication through the Ghanaian High Commission in "
            "Canberra is required for Australian documents. "
            "(Ghanaian Ministry of Foreign Affairs, 2025; DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'ghana',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a Ghanaian community, with nationals working in Stockholm "
            "and other Swedish cities. Ghana maintains an Embassy in Stockholm. "
            "When a Ghanaian national dies in Sweden and their family wishes to "
            "repatriate remains to Ghana, the death is registered with the "
            "Swedish Tax Agency (Skatteverket) Population Register. The "
            "dodsfallsintyg requires certified English translation for the Births "
            "and Deaths Registry (BDR) in Ghana. Ghana is not a Hague Apostille "
            "member; Swedish documents require full consular authentication through "
            "the Ghanaian Embassy in Stockholm. "
            "(Ghanaian Ministry of Foreign Affairs, 2025; Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'ghana',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Ghana maintain bilateral ties through development "
            "cooperation, oil sector partnerships, and the Ghanaian community "
            "established in Oslo and Bergen. Ghana maintains an Embassy in Oslo. "
            "When a Ghanaian national dies in Norway and their family wishes to "
            "repatriate remains to Ghana, the death is registered with "
            "Folkeregisteret (the Norwegian civil registration system). The "
            "dodsattest requires certified English translation for the Births "
            "and Deaths Registry (BDR) in Ghana. Ghana is not a Hague Apostille "
            "member; Norwegian documents require full consular authentication "
            "through the Ghanaian Embassy in Oslo. "
            "(Ghanaian Ministry of Foreign Affairs, 2025; Skatteetaten, Norway, 2025.)"
        ),
    },
    # R84 -- Vietnam x5
    {
        'origin': 'united-kingdom', 'dest': 'vietnam',
        'embassy_city': 'London',
        'intro': (
            "Vietnam is a growing destination for British tourists and business "
            "travellers, with Ho Chi Minh City and Hanoi popular on Southeast "
            "Asian itineraries. A small British expat and business community is "
            "established in Vietnam's major cities. The British Embassy in Hanoi "
            "is fully operational. When someone from the United Kingdom dies in "
            "Vietnam and their family wishes to repatriate remains, the death is "
            "registered with the local People's Committee civil status office. "
            "A Ministry of Health import permit is required for the receiving "
            "country. Vietnam is not a Hague Apostille Convention member; the "
            "Vietnamese Embassy in London can advise on consular legalisation "
            "requirements. Appoint a specialist on the day of death. "
            "(FCDO Travel Advice: Vietnam, 2025; Vietnamese Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'vietnam',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Vietnam maintain bilateral trade ties, and Italian nationals "
            "travel to Vietnam for tourism and business in manufacturing and "
            "fashion sectors. Vietnam maintains an Embassy in Rome. When an Italian "
            "national dies in Vietnam and their family wishes to repatriate remains "
            "to Italy, the death is registered with the local People's Committee "
            "civil status office. A Ministry of Health import permit is required. "
            "Vietnam is not a Hague Apostille Convention member; the Vietnamese "
            "Embassy in Rome can advise on consular legalisation for Italian "
            "documents. The atto di morte requires certified Vietnamese translation. "
            "(Italian Ministry of Foreign Affairs, 2025; Vietnamese Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-korea', 'dest': 'vietnam',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korea and Vietnam maintain one of the most active bilateral "
            "relationships in Southeast Asia, with South Korean investment "
            "significant in Vietnamese manufacturing, electronics, and construction. "
            "A substantial South Korean expat community lives and works in Hanoi "
            "and Ho Chi Minh City. South Korea maintains an Embassy in Hanoi "
            "and Consulates in Ho Chi Minh City. When a South Korean national "
            "dies in Vietnam and their family wishes to repatriate remains to "
            "South Korea, the death is registered with the local People's Committee "
            "civil status office. Vietnam is not a Hague Apostille member; the "
            "Vietnamese Embassy in Seoul can advise on consular legalisation. "
            "(South Korean Ministry of Foreign Affairs, 2025; Vietnamese Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'vietnam',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japan and Vietnam have a strong bilateral relationship, with Japanese "
            "investment among the largest in Vietnam across manufacturing, "
            "infrastructure, and services. A substantial Japanese business community "
            "is established in Ho Chi Minh City and Hanoi. Japan maintains an "
            "Embassy in Hanoi and Consulates in Ho Chi Minh City and Da Nang. "
            "When a Japanese national dies in Vietnam and their family wishes to "
            "repatriate remains to Japan, the death is registered with the local "
            "People's Committee civil status office. Vietnam is not a Hague "
            "Apostille member; the Vietnamese Embassy in Tokyo can advise on "
            "consular legalisation. Japan joined the Hague Apostille Convention "
            "in 1970. "
            "(Japan Ministry of Foreign Affairs, 2025; Vietnamese Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'vietnam',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Vietnam have bilateral ties through trade, "
            "development cooperation, and agricultural expertise partnerships. "
            "Dutch nationals travel to Vietnam for business and tourism. The "
            "Netherlands maintains an Embassy in Hanoi. When a Dutch national "
            "dies in Vietnam and their family wishes to repatriate remains to "
            "the Netherlands, the death is registered with the local People's "
            "Committee civil status office. A Ministry of Health import permit "
            "is required. Vietnam is not a Hague Apostille Convention member; "
            "the Vietnamese Embassy in The Hague can advise on consular "
            "legalisation for Dutch documents. "
            "(Netherlands Ministry of Foreign Affairs, 2025; Vietnamese Ministry "
            "of Foreign Affairs, 2025.)"
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
