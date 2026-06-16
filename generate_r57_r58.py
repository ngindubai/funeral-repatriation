#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R57-R58.

   R57 (25 routes, variants D,E,A,B,C x5):
     Indonesia wave 3 x5: vietnam, bangladesh, saudi-arabia, taiwan, france
     Bahrain wave 7 x5: south-korea, japan, singapore, morocco, algeria
     South Korea wave 7 x5: canada, germany, france, italy, new-zealand
     Japan wave 12 x5: mexico, colombia, peru, morocco, algeria
     Oman wave 9 x5: yemen, singapore, japan, afghanistan, tanzania

   R58 (25 routes, variants D,E,A,B,C x5):
     Turkey wave 6 x5: france, italy, spain, netherlands, belgium
     Malaysia wave 7 x5: turkey, egypt, iran, germany, france
     Indonesia wave 4 x5: south-africa, canada, norway, sweden, hong-kong
     South Korea wave 8 x5: spain, netherlands, belgium, switzerland, sweden
     Japan wave 13 x5: venezuela, chile, tanzania, ivory-coast, cameroon

   Template rotation: R56 ended C (index 2). R57 starts D (index 3).
   Each block of 25 cycles D,E,A,B,C x5, ending on C. R58 starts D again.

   Embassy notes:
   - Taiwan: not a Hague Apostille member. Indonesian representative in
     Taiwan is the Indonesia Economic and Trade Office Taipei.
   - Yemen: FCDO advises against all travel; civil registration severely
     disrupted. Omani Embassy in Sana'a has limited operations; families
     should contact Omani MFA directly.
   - Afghanistan to Oman: Omani Embassy in Islamabad covers Afghanistan.
   - Turkey as destination: no cremation for Muslim remains; burial required.
     Istanbul Airport (IST) and Istanbul Sabiha Gokcen Airport (SAW).
   - Malaysia as destination: KLIA (KUL) cargo terminal; Islamic law for
     Muslim remains; Jabatan Agama Islam burial permit required.
   - Iran: British Embassy not operational in Tehran since 2011; many
     Western embassies have limited or no consular presence.
   - Ivory Coast and Cameroon: not Hague Apostille members; full
     consular authentication through Japanese Embassy required.
   - Algeria: not a Hague Apostille member.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 3  # D

DEST_META = {
    'bahrain': {
        'name': 'Bahrain',
        'slug': 'bahrain',
        'key': 'bh',
        'reception': (
            "The Bahraini funeral director takes custody at Bahrain International "
            "Airport (BAH) cargo terminal. The Civil Status and Passports Affairs "
            "Authority (CSPA) under the Ministry of Interior registers deaths in "
            "Bahrain. For Muslim remains, Islamic law requires prompt preparation "
            "and burial; a special authorisation from the CSPA is required for "
            "international repatriation to delay disposition. All foreign documents "
            "not in Arabic require certified Arabic translation. Authentication by "
            "the Bahraini Embassy or Consulate in the country of origin is required. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Bahraini Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Bahrain. Contact the Embassy during "
            "business hours. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Bahraini funeral director takes custody at Bahrain International "
            "Airport (BAH) cargo terminal. The CSPA registers the death. For Muslim "
            "remains, Islamic law procedures apply and the CSPA authorises the final "
            "disposition. All foreign documents require certified Arabic translation "
            "and authentication by the Bahraini Embassy in the origin country. The "
            "receiving funeral director coordinates with the CSPA."
        ),
        'emergency_line': 'contact the Bahraini Embassy in the origin country',
        'hub_url': 'repatriation-from-bahrain',
    },
    'south-korea': {
        'name': 'South Korea',
        'slug': 'south-korea',
        'key': 'kr',
        'reception': (
            "The Korean funeral director (jang-ye-jido-sa) takes custody at "
            "Incheon International Airport (ICN) cargo terminal. The local gu "
            "office (ward office) registers the death and issues the Korean death "
            "certificate. A burial or cremation certificate (jang-ui-hwakinjung) "
            "is required before final disposition. South Korea is not a member of "
            "the Hague Apostille Convention; all foreign documents require "
            "authentication through Korean embassy channels and certified Korean "
            "translation. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Embassy of the Republic of Korea in {city} can advise on "
            "documentation requirements for repatriation to South Korea. Korean "
            "Ministry of Foreign Affairs 24-hour emergency line: +82 2 3210 0404. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Korean funeral director (jang-ye-jido-sa) takes custody at "
            "Incheon International Airport (ICN) cargo terminal. The local gu "
            "office (ward office) registers the death. A jang-ui-hwakinjung "
            "(burial or cremation certificate) is required before final "
            "disposition. South Korea is not a Hague Apostille member; all "
            "foreign documents require authentication through Korean embassy "
            "channels and certified Korean translation."
        ),
        'emergency_line': '+82 2 3210 0404',
        'hub_url': 'repatriation-from-south-korea',
    },
    'japan': {
        'name': 'Japan',
        'slug': 'japan',
        'key': 'jp',
        'reception': (
            "The Japanese funeral director (sogisha) takes custody at Tokyo "
            "Narita (NRT), Tokyo Haneda (HND), or Kansai (KIX) cargo terminal. "
            "The shibo todoke (death notification) must be submitted to the local "
            "municipal office (shiyakusho or kuyakusho) within seven days of "
            "arrival. A burial permit is required before final disposition. Japan "
            "has near-universal cremation; the remains (kotsuage) are presented to "
            "the family after cremation. All foreign documents not in Japanese "
            "require certified Japanese translation. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Japanese Embassy in {city} can advise on documentation requirements "
            "for repatriation to Japan. Japanese Ministry of Foreign Affairs "
            "emergency line: +81 3 3580 3311 (24 hours). The Japanese Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Japanese funeral director takes custody at Tokyo Narita (NRT) or "
            "Kansai (KIX) cargo terminal. The shibo todoke must be submitted to "
            "the local municipal office within seven days. A burial permit is "
            "required. Japan has near-universal cremation; remains are presented "
            "as kotsuage after the ceremony. All foreign documents require "
            "certified Japanese translation. The receiving funeral director "
            "coordinates with local authorities."
        ),
        'emergency_line': '+81 3 3580 3311',
        'hub_url': 'repatriation-from-japan',
    },
    'oman': {
        'name': 'Oman',
        'slug': 'oman',
        'key': 'om',
        'reception': (
            "The Omani funeral director takes custody at Muscat International Airport "
            "(MCT) cargo terminal. The Royal Oman Police registers the death and a "
            "burial permit from the Ministry of Health is required before any final "
            "disposition. Muslim remains are handled in accordance with Islamic law. "
            "All foreign documents not in Arabic require certified Arabic translation. "
            "Authentication by the Omani Embassy in the country of origin is required. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Omani Embassy in {city} can advise on documentation requirements for "
            "repatriation to Oman. Oman Ministry of Foreign Affairs can be reached "
            "via the Omani Embassy during business hours. The Omani Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Omani funeral director takes custody at Muscat International Airport "
            "(MCT) cargo terminal. The Royal Oman Police registers the death. A burial "
            "permit from the Ministry of Health is required. Muslim remains are handled "
            "in accordance with Islamic law. All foreign documents require certified "
            "Arabic translation and authentication by the Omani Embassy in the origin "
            "country."
        ),
        'emergency_line': 'contact the Omani Embassy in the origin country',
        'hub_url': 'repatriation-from-oman',
    },
    'indonesia': {
        'name': 'Indonesia',
        'slug': 'indonesia',
        'key': 'id',
        'reception': (
            "The Indonesian funeral director takes custody at Soekarno-Hatta "
            "International Airport (CGK) in Jakarta, or at I Gusti Ngurah Rai "
            "International Airport (DPS) for Bali arrivals. The Dinas Kependudukan "
            "dan Pencatatan Sipil (Disdukcapil), Indonesia's civil registration "
            "authority, registers the death. A burial or cremation permit from the "
            "local health authority is required before final disposition. For Muslim "
            "remains, Islamic law procedures apply. All foreign documents not in "
            "Bahasa Indonesia require certified Indonesian translation. Authentication "
            "by the Indonesian Embassy in the country of origin is required. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Indonesian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Indonesia. Contact the Embassy during "
            "business hours. The Indonesian Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Indonesian funeral director takes custody at Soekarno-Hatta "
            "International Airport (CGK) or Ngurah Rai Airport (DPS) for Bali. "
            "The Disdukcapil registers the death. A burial or cremation permit is "
            "required from the local health authority. For Muslim remains, Islamic "
            "law procedures apply. All foreign documents require certified Indonesian "
            "translation and authentication by the Indonesian Embassy in the origin "
            "country. The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': 'contact the Indonesian Embassy in the origin country',
        'hub_url': 'repatriation-from-indonesia',
    },
    'turkey': {
        'name': 'Turkey',
        'slug': 'turkey',
        'key': 'tr',
        'reception': (
            "The Turkish funeral director takes custody at Istanbul Airport (IST) "
            "or Istanbul Sabiha Gokcen Airport (SAW) cargo terminal. The receiving "
            "nufus mudurlugu (population directorate) registers the incoming death "
            "documentation. A burial permit is required before final disposition. "
            "Cremation is not available for Muslim remains in Turkey; burial is "
            "required. All foreign documents not in Turkish require certified Turkish "
            "translation. Authentication by the Turkish Embassy or Consulate in the "
            "country of origin is required. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Turkish Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Turkey. Turkish Ministry of Foreign "
            "Affairs emergency line: +90 312 292 2000 (24 hours). The Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Turkish funeral director takes custody at Istanbul Airport (IST) "
            "or Istanbul Sabiha Gokcen Airport (SAW) cargo terminal. The nufus "
            "mudurlugu (population directorate) registers the incoming documentation. "
            "A burial permit is required before final disposition. Cremation is not "
            "available for Muslim remains; burial is required. All foreign documents "
            "require certified Turkish translation and authentication by the Turkish "
            "Embassy in the origin country. The receiving funeral director coordinates "
            "with local authorities."
        ),
        'emergency_line': '+90 312 292 2000',
        'hub_url': 'repatriation-from-turkey',
    },
    'malaysia': {
        'name': 'Malaysia',
        'slug': 'malaysia',
        'key': 'my',
        'reception': (
            "The Malaysian funeral director takes custody at Kuala Lumpur "
            "International Airport (KLIA, KUL) cargo terminal. The National "
            "Registration Department (Jabatan Pendaftaran Negara) registers the "
            "death documentation. For Muslim remains, a burial permit from the "
            "local Islamic Religious Department (Jabatan Agama Islam) is required "
            "before final disposition, and Islamic law procedures apply. All foreign "
            "documents not in Bahasa Malaysia or English require certified translation. "
            "Authentication by the Malaysian Embassy or High Commission in the country "
            "of origin is required. (Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Malaysian Embassy or High Commission in {city} can advise on "
            "documentation requirements for repatriation to Malaysia. Contact the "
            "Malaysian Embassy during business hours. The Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Malaysian funeral director takes custody at Kuala Lumpur "
            "International Airport (KLIA, KUL) cargo terminal. The National "
            "Registration Department (Jabatan Pendaftaran Negara) registers the "
            "death documentation. For Muslim remains, a burial permit from the "
            "Jabatan Agama Islam (Islamic Religious Department) is required, and "
            "Islamic law procedures apply. All foreign documents require certified "
            "translation and authentication by the Malaysian Embassy in the origin "
            "country. The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': 'contact the Malaysian Embassy in the origin country',
        'hub_url': 'repatriation-from-malaysia',
    },
}

ORIGIN_DATA = {
    'vietnam': {
        'name': 'Vietnam',
        'emergency': '113 (police) / 115 (ambulance)',
        'registry': "the local People's Committee (Uy ban Nhan dan) civil status office",
        'cert_name': 'giay chung tu khai tu (death notification)',
        'cert_lang': 'Vietnamese',
        'overview': (
            "Call 113 for police or 115 for ambulance. Death is certified by a "
            "physician. The giay chung tu khai tu is registered with the local "
            "People's Committee (Uy ban Nhan dan) civil status office. Police take "
            "jurisdiction for violent or unexplained deaths. Documentation is in "
            "Vietnamese and requires certified translation. Vietnam's tropical "
            "climate in the south requires urgent embalming."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation in Vietnam is widely available in major cities including "
            "Ho Chi Minh City and Hanoi."
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
    'bangladesh': {
        'name': 'Bangladesh',
        'emergency': '999 (police) / 199 (fire and ambulance)',
        'registry': 'the local Union Parishad or Municipality (Pourashava) civil registration office',
        'cert_name': 'death certificate',
        'cert_lang': 'Bengali',
        'overview': (
            "Call 999 for police or 199 for fire and ambulance. Death is certified "
            "by a physician. Death is registered with the local Union Parishad or "
            "Municipality (Pourashava) under the national registration system. "
            "Police take jurisdiction for violent or unexplained deaths. "
            "Bangladesh's tropical climate requires urgent embalming. Documentation "
            "is in Bengali and requires certified translation."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not widely available for Muslim remains in Bangladesh. "
            "Hindu communities may use cremation facilities."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
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
        'timeline_avg': '2-3 weeks',
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
    'taiwan': {
        'name': 'Taiwan',
        'emergency': '110 (police) / 119 (ambulance)',
        'registry': 'the local Household Registration Office (huji dengji)',
        'cert_name': 'si wang zheng ming shu (death certificate)',
        'cert_lang': 'Traditional Chinese',
        'overview': (
            "Call 110 for police or 119 for ambulance. Death is certified by a "
            "physician. The death is registered with the local Household "
            "Registration Office (huji dengji). Police and the Prosecutor's Office "
            "take jurisdiction for violent or unexplained deaths. All documentation "
            "is in Traditional Chinese and requires certified translation. Taiwan is "
            "not a member of the Hague Apostille Convention; documents require "
            "authentication through the relevant Taipei Representative Office."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-10 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'moderate',
        'cremation': "Cremation in Taiwan is widely available and commonly used.",
        'postmortem_trigger': "Violent or unexplained deaths (Prosecutor's Office)",
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': "Cremation in France is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Procureur de la Republique)',
    },
    'morocco': {
        'name': 'Morocco',
        'emergency': '19 (police) / 15 (ambulance)',
        'registry': 'the local bureau d\'etat civil (civil registry office)',
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'Arabic and French',
        'overview': (
            "Call 19 for police or 15 for ambulance. Death is certified by a "
            "physician. The acte de deces is registered with the local bureau "
            "d'etat civil. Police and the Parquet (public prosecutor) take "
            "jurisdiction for violent or unexplained deaths. Documentation is in "
            "Arabic and French; certified translation is required for destination "
            "country authorities."
        ),
        'doc_time': '5-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available for Muslim remains in Morocco. "
            "Non-Muslim remains may be repatriated for cremation."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Parquet)',
    },
    'algeria': {
        'name': 'Algeria',
        'emergency': '17 (police) / 21 (ambulance)',
        'registry': "the local etat civil (civil registry office)",
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 17 for police or 21 for ambulance. Death is certified by a "
            "physician. The acte de deces is registered with the local etat civil. "
            "Police take jurisdiction for violent or unexplained deaths. "
            "Documentation is primarily in Arabic, with some offices also issuing "
            "French-language versions. Certified translation is required for "
            "destination country authorities. Algeria is not a Hague Apostille "
            "Convention member; full consular authentication is required."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available for Muslim remains in Algeria. "
            "Non-Muslim remains may be repatriated for cremation."
        ),
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
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Canada is widely available.",
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Germany is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft)',
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Italy is available, though less prevalent than in "
            "northern Europe; facilities exist in major cities."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Procura della Repubblica)',
    },
    'new-zealand': {
        'name': 'New Zealand',
        'emergency': '111',
        'registry': 'Births, Deaths and Marriages New Zealand (BDM)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 111 for emergency services. Death is certified by a registered "
            "medical practitioner or Coroner. The death is registered with Births, "
            "Deaths and Marriages New Zealand (BDM). The Coroner takes jurisdiction "
            "for sudden, unexpected, or unnatural deaths. New Zealand is a Hague "
            "Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': "Cremation in New Zealand is widely available.",
        'postmortem_trigger': 'Sudden, unexpected, or unnatural deaths (Coroner takes jurisdiction)',
    },
    'mexico': {
        'name': 'Mexico',
        'emergency': '911',
        'registry': 'the Registro Civil (civil registry)',
        'cert_name': 'acta de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician. "
            "The acta de defuncion is registered with the local Registro Civil. "
            "The Ministerio Publico (public prosecutor) takes jurisdiction for "
            "violent or unexplained deaths. Mexico is a Hague Apostille Convention "
            "member. Families should be aware that consular conditions vary "
            "significantly across Mexico's regions; the FCDO advises against "
            "all but essential travel in certain areas."
        ),
        'doc_time': '5-14 days',
        'timeline_avg': '14-28 days',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': "Cremation in Mexico is available in major cities.",
        'postmortem_trigger': 'Violent, accidental, or unexplained deaths (Ministerio Publico)',
    },
    'colombia': {
        'name': 'Colombia',
        'emergency': '112',
        'registry': 'the Registraduria Nacional del Estado Civil',
        'cert_name': 'acta de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The acta de defuncion is registered with the Registraduria Nacional "
            "del Estado Civil. Police and the Fiscalia (public prosecutor) take "
            "jurisdiction for violent or unexplained deaths. Colombia is a Hague "
            "Apostille Convention member. Safety conditions vary significantly by "
            "region; families should check FCDO travel advice."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': "Cremation in Colombia is available in major cities.",
        'postmortem_trigger': 'Violent or unexplained deaths (Fiscalia)',
    },
    'peru': {
        'name': 'Peru',
        'emergency': '105 (police) / 117 (ambulance)',
        'registry': 'the Registro Nacional de Identificacion y Estado Civil (RENIEC)',
        'cert_name': 'acta de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 105 for police or 117 for ambulance. Death is certified by a "
            "physician. The acta de defuncion is registered with RENIEC (Registro "
            "Nacional de Identificacion y Estado Civil). The Fiscalia (public "
            "prosecutor) takes jurisdiction for violent or unexplained deaths. "
            "Peru is a Hague Apostille Convention member."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': "Cremation in Peru is available in major cities including Lima.",
        'postmortem_trigger': 'Violent or unexplained deaths (Fiscalia)',
    },
    'yemen': {
        'name': 'Yemen',
        'emergency': '194 (police, severely limited) / 191 (ambulance, severely limited)',
        'registry': 'the local civil registry (very limited capacity due to the conflict)',
        'cert_name': 'death certificate',
        'cert_lang': 'Arabic',
        'overview': (
            "Emergency services and civil registration are severely disrupted across "
            "most of Yemen due to the ongoing conflict. The FCDO advises against all "
            "travel to Yemen. Consular access is extremely limited. Families should "
            "contact the nearest operational embassy as a first step and seek "
            "specialist support immediately. Documentation is in Arabic and requires "
            "certified translation."
        ),
        'doc_time': 'Weeks to many months; highly variable due to the conflict',
        'timeline_avg': '3-6 months',
        'timeline_fast': '6-12 weeks in accessible areas',
        'timeline_complex': 'Many months or longer',
        'complexity': 'very-high',
        'cremation': "Cremation is not available for Muslim remains in Yemen.",
        'postmortem_trigger': (
            'Violent or unexplained deaths; the conflict and security conditions '
            'may prevent or delay access to authorities'
        ),
    },
    'singapore': {
        'name': 'Singapore',
        'emergency': '999 (police) / 995 (ambulance)',
        'registry': 'the Registry of Births and Deaths (Immigration and Checkpoints Authority)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 999 for police or 995 for ambulance. Death must be certified by "
            "a registered medical practitioner within 24 hours. The death is "
            "registered with the Registry of Births and Deaths, administered by "
            "the Immigration and Checkpoints Authority (ICA). The coroner takes "
            "jurisdiction for sudden or unexplained deaths. Singapore is a Hague "
            "Apostille Convention member and English is the official language."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '7-10 days',
        'timeline_fast': '3-5 days',
        'timeline_complex': '2-4 weeks (coroner cases)',
        'complexity': 'low',
        'cremation': "Cremation in Singapore is widely available and commonly used.",
        'postmortem_trigger': 'Sudden or unexplained deaths (coroner takes jurisdiction)',
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
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation is the standard final disposition in Japan (over 99%).',
        'postmortem_trigger': 'Violent or unexplained deaths (public prosecutor, Kenji)',
    },
    'afghanistan': {
        'name': 'Afghanistan',
        'emergency': '119 (police, severely limited)',
        'registry': 'the relevant local authority (civil registry capacity is very limited)',
        'cert_name': 'death certificate',
        'cert_lang': 'Dari or Pashto',
        'overview': (
            "Emergency services are severely limited across Afghanistan. The FCDO "
            "advises against all travel to Afghanistan. Civil registration capacity "
            "is very limited and consular access has been significantly curtailed "
            "since August 2021. Families should contact the nearest operational "
            "embassy as a first step. Documentation complexity on this corridor "
            "is very high."
        ),
        'doc_time': 'Weeks to months; highly variable',
        'timeline_avg': '3-6 months',
        'timeline_fast': '6-12 weeks',
        'timeline_complex': 'Many months or longer',
        'complexity': 'very-high',
        'cremation': 'Cremation is not available for Muslim remains in Afghanistan.',
        'postmortem_trigger': (
            'Violent or unexplained deaths; the security situation may prevent '
            'access to authorities'
        ),
    },
    'tanzania': {
        'name': 'Tanzania',
        'emergency': '112 (police) / 115 (ambulance)',
        'registry': 'the Registration, Insolvency and Trusteeship Agency (RITA)',
        'cert_name': 'death certificate',
        'cert_lang': 'Swahili and English',
        'overview': (
            "Call 112 for police or 115 for ambulance. Death is certified by a "
            "physician. The death is registered with RITA (Registration, Insolvency "
            "and Trusteeship Agency) at the local registration office. Police take "
            "jurisdiction for violent or unexplained deaths. Tanzania's tropical "
            "climate requires urgent embalming."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is available in major cities in Tanzania, though burial "
            "is more common."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'turkey': {
        'name': 'Turkey',
        'emergency': '155 (police) / 112 (ambulance)',
        'registry': 'the nufus mudurlugu (population directorate)',
        'cert_name': 'olum belgesi (death certificate)',
        'cert_lang': 'Turkish',
        'overview': (
            "Call 155 for police or 112 for ambulance. Death is certified by a "
            "physician. The olum belgesi (death certificate) is registered with "
            "the local nufus mudurlugu (population directorate). Police and the "
            "Cumhuriyet Savcilik (public prosecutor's office) take jurisdiction "
            "for violent or unexplained deaths. All documentation is in Turkish "
            "and requires certified translation."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available in Turkey. Burial is the required "
            "final disposition."
        ),
        'postmortem_trigger': (
            'Violent, sudden, or unexplained deaths (Cumhuriyet Savcilik)'
        ),
    },
    'egypt': {
        'name': 'Egypt',
        'emergency': '122 (police) / 123 (ambulance)',
        'registry': 'the local health office (through the niyaba, public prosecutor)',
        'cert_name': 'death certificate',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 122 for police or 123 for ambulance. All deaths of foreign "
            "nationals require police attendance. The niyaba (public prosecutor) "
            "takes jurisdiction for unexpected or violent deaths. Death is "
            "registered at the local health office. In tourist areas such as "
            "Hurghada and Sharm el-Sheikh, local health offices tend to process "
            "registrations faster than in Cairo. All documentation is in Arabic "
            "and requires certified translation."
        ),
        'doc_time': '7-14 days (tourist areas); longer elsewhere',
        'timeline_avg': '14-28 days',
        'timeline_fast': '7-14 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not available in Egypt. All repatriations must be "
            "of the full body."
        ),
        'postmortem_trigger': (
            'All unnatural, sudden, or suspicious deaths (niyaba takes jurisdiction)'
        ),
    },
    'iran': {
        'name': 'Iran',
        'emergency': '110 (police) / 115 (ambulance)',
        'registry': 'the National Civil Registration Organisation (NCRO)',
        'cert_name': 'death certificate',
        'cert_lang': 'Farsi (Persian)',
        'overview': (
            "Call 110 for police or 115 for ambulance. Death is certified by a "
            "physician and registered with the National Civil Registration "
            "Organisation (NCRO). Police and the public prosecutor take "
            "jurisdiction for violent or unexplained deaths. All documentation "
            "is in Farsi and requires certified translation. The FCDO advises "
            "against all travel to Iran. The British Embassy in Tehran has been "
            "closed since 2011; British nationals should contact the nearest "
            "operational embassy. Consular access is limited for many Western "
            "countries. Families should seek specialist support at the earliest "
            "opportunity."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': '3-6 months',
        'complexity': 'high',
        'cremation': "Cremation is not available for Muslim remains in Iran.",
        'postmortem_trigger': 'Violent or unexplained deaths (public prosecutor)',
    },
    'south-africa': {
        'name': 'South Africa',
        'emergency': '10111 (police) / 10177 (ambulance)',
        'registry': 'the Department of Home Affairs',
        'cert_name': 'death certificate',
        'cert_lang': 'English or Afrikaans',
        'overview': (
            "Call 10111 for police or 10177 for ambulance. Death is certified by "
            "a medical practitioner. The death is registered with the Department "
            "of Home Affairs. Police and the magistrate's court take jurisdiction "
            "for violent or unexplained deaths. South Africa is a member of the "
            "Hague Apostille Convention."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation in South Africa is widely available in major cities "
            "including Johannesburg, Cape Town, and Durban."
        ),
        'postmortem_trigger': "Violent or unexplained deaths (magistrate's court)",
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Sweden is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'hong-kong': {
        'name': 'Hong Kong',
        'emergency': '999',
        'registry': 'the Registry of Births and Deaths (Immigration Department)',
        'cert_name': 'death certificate',
        'cert_lang': 'English and Chinese',
        'overview': (
            "Call 999 for police or ambulance. Death is certified by a registered "
            "medical practitioner. The death is registered with the Registry of "
            "Births and Deaths (Immigration Department). The Coroner's Court takes "
            "jurisdiction for sudden, violent, or unexplained deaths. Hong Kong "
            "is a common law jurisdiction with well-established administrative "
            "procedures."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks (Coroner cases)',
        'complexity': 'low',
        'cremation': "Cremation in Hong Kong is widely available and commonly used.",
        'postmortem_trigger': "Sudden, violent, or unexplained deaths (Coroner's Court)",
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Spain is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Juzgado de Guardia)',
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
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
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Belgium is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Parquet)',
    },
    'switzerland': {
        'name': 'Switzerland',
        'emergency': '117 (police) / 144 (ambulance)',
        'registry': 'the Zivilstandsamt (civil registry office)',
        'cert_name': 'Todesschein (death certificate)',
        'cert_lang': 'German, French, or Italian',
        'overview': (
            "Call 117 for police or 144 for ambulance. A physician certifies the "
            "death. The Todesschein is registered with the local Zivilstandsamt. "
            "Police and the Staatsanwaltschaft (public prosecutor) take jurisdiction "
            "for violent or unexplained deaths. Switzerland is a Hague Apostille "
            "Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Switzerland is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft)',
    },
    'venezuela': {
        'name': 'Venezuela',
        'emergency': '911',
        'registry': 'the Registro Civil under SAREN (Servicio Autonomo de Registros y Notarias)',
        'cert_name': 'acta de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician. "
            "The acta de defuncion is registered with the Registro Civil under "
            "SAREN (Servicio Autonomo de Registros y Notarias). Police and the "
            "Ministerio Publico take jurisdiction for violent or unexplained deaths. "
            "Civil registration capacity varies given the current humanitarian "
            "situation. Families should contact the nearest operational embassy "
            "as a first step. Venezuela is a Hague Apostille Convention member, "
            "though practical application may be limited."
        ),
        'doc_time': 'Weeks to months; variable due to infrastructure constraints',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': 'Several months',
        'complexity': 'high',
        'cremation': (
            "Cremation in Venezuela is available in major cities, though access "
            "may be limited."
        ),
        'postmortem_trigger': (
            'Violent or unexplained deaths (Ministerio Publico); '
            'infrastructure constraints may compound delays'
        ),
    },
    'chile': {
        'name': 'Chile',
        'emergency': '133 (police) / 131 (ambulance)',
        'registry': 'the Servicio de Registro Civil e Identificacion (SRCEI)',
        'cert_name': 'certificado de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 133 for police or 131 for ambulance. Death is certified by a "
            "physician. The certificado de defuncion is registered with the "
            "Servicio de Registro Civil e Identificacion (SRCEI). The Ministerio "
            "Publico takes jurisdiction for violent or unexplained deaths. Chile "
            "is a Hague Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '14-21 days',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Chile is available and increasingly used.",
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico)',
    },
    'ivory-coast': {
        'name': 'Ivory Coast',
        'emergency': '110 (police) / 185 (SAMU ambulance)',
        'registry': "the local Centre d'etat civil",
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'French',
        'overview': (
            "Call 110 for police or 185 for SAMU (ambulance). Death is certified "
            "by a physician. The acte de deces is registered with the local Centre "
            "d'etat civil. Police take jurisdiction for violent or unexplained "
            "deaths. Documentation is in French and requires certified translation. "
            "Ivory Coast's tropical climate requires urgent embalming."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not widely available in Ivory Coast. Most families "
            "opt for full body repatriation."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'cameroon': {
        'name': 'Cameroon',
        'emergency': '117 (police) / 15 (ambulance)',
        'registry': "the local Centre d'etat civil",
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'French or English (Anglophone region)',
        'overview': (
            "Call 117 for police or 15 for ambulance. Death is certified by a "
            "physician. The acte de deces is registered with the local Centre "
            "d'etat civil. Police take jurisdiction for violent or unexplained "
            "deaths. Documentation is primarily in French, with English used "
            "in the Anglophone North-West and South-West regions."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not widely available in Cameroon. Most families "
            "opt for full body repatriation."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
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
    # R57 -- Indonesia wave 3
    {
        'origin': 'vietnam', 'dest': 'indonesia',
        'embassy_city': 'Hanoi',
        'intro': (
            "Vietnamese nationals in Indonesia include workers in manufacturing, "
            "construction, and business, reflecting growing bilateral trade ties. "
            "Vietnam and Indonesia are both ASEAN member states with strong "
            "bilateral trade ties and a growing economic partnership within the "
            "ASEAN regional framework. Vietnamese death certificates (giay chung tu "
            "khai tu, in Vietnamese) require certified Indonesian translation for "
            "the Disdukcapil (Dinas Kependudukan dan Pencatatan Sipil) and "
            "authentication by the Indonesian Embassy in Hanoi. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'bangladesh', 'dest': 'indonesia',
        'embassy_city': 'Dhaka',
        'intro': (
            "Bangladeshi nationals in Indonesia include workers in manufacturing "
            "and construction, reflecting Bangladesh's growing labour export to "
            "Southeast Asia. Bangladesh and Indonesia are both Organisation of "
            "Islamic Cooperation (OIC) member states with bilateral economic ties "
            "within ASEAN-South Asian frameworks. Bangladeshi death certificates "
            "(in Bengali) require certified Indonesian translation for the "
            "Disdukcapil and authentication by the Indonesian Embassy in Dhaka. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'saudi-arabia', 'dest': 'indonesia',
        'embassy_city': 'Riyadh',
        'intro': (
            "Saudi nationals in Indonesia include business professionals and "
            "individuals with religious and cultural ties, reflecting the long-standing "
            "relationship between the two OIC member states. Indonesia is the "
            "world's largest Muslim-majority country and has strong trade and "
            "religious links with Saudi Arabia. Arabic-language Saudi death "
            "certificates require certified Indonesian translation for the "
            "Disdukcapil and authentication by the Indonesian Embassy in Riyadh. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'taiwan', 'dest': 'indonesia',
        'embassy_city': 'Taipei',
        'intro': (
            "Taiwanese nationals in Indonesia include business investors, "
            "manufacturing professionals, and expatriates. Taiwan is among the "
            "significant foreign investors in Indonesian manufacturing and industry. "
            "Taiwan's representative office in Indonesia is the Taipei Economic "
            "and Cultural Office (TECO) in Jakarta; the Indonesian representative "
            "in Taiwan is the Indonesia Economic and Trade Office Taipei. "
            "Taiwanese death certificates (si wang zheng ming shu, in Traditional "
            "Chinese) require certified Indonesian translation for the Disdukcapil. "
            "Taiwan is not a member of the Hague Apostille Convention; families "
            "should contact the Indonesia Economic and Trade Office Taipei to "
            "verify current authentication requirements. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'indonesia',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Indonesia include professionals in the energy, "
            "mining, and tourism sectors, development workers, and expatriates. "
            "France and Indonesia maintain bilateral diplomatic relations and France "
            "has an active Embassy in Jakarta. French death certificates (acte de "
            "deces, in French) require certified Indonesian translation for the "
            "Disdukcapil and authentication by the Indonesian Embassy in Paris. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R57 -- Bahrain wave 7
    {
        'origin': 'south-korea', 'dest': 'bahrain',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korean nationals in Bahrain include engineers, construction "
            "professionals, and technical specialists, reflecting South Korea's "
            "significant presence in Gulf infrastructure projects through major "
            "Korean construction firms. South Korea and Bahrain have bilateral "
            "economic cooperation agreements. South Korean death certificates "
            "(in Korean) require certified Arabic translation for the Civil Status "
            "and Passports Affairs Authority (CSPA) and authentication by the "
            "Bahraini Embassy in Seoul. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'bahrain',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japanese nationals in Bahrain include engineers, construction "
            "professionals, and business executives reflecting Japan's bilateral "
            "trade and investment ties with Bahrain. Japan and Bahrain have "
            "maintained diplomatic relations since 1971. Japanese death "
            "certificates (shibo todoke, in Japanese) require certified Arabic "
            "translation for the Civil Status and Passports Affairs Authority "
            "(CSPA) and authentication by the Bahraini Embassy in Tokyo. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'singapore', 'dest': 'bahrain',
        'embassy_city': 'Singapore',
        'intro': (
            "Singaporean nationals in Bahrain include finance professionals, "
            "business executives, and technical specialists. Singapore and Bahrain "
            "have bilateral ties through Gulf-Southeast Asian financial and economic "
            "frameworks. English-language Singapore death certificates require "
            "certified Arabic translation for the Civil Status and Passports "
            "Affairs Authority (CSPA). The Bahraini Embassy in Singapore handles "
            "consular matters. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'morocco', 'dest': 'bahrain',
        'embassy_city': 'Rabat',
        'intro': (
            "Moroccan nationals in Bahrain include workers in construction, "
            "domestic service, and the hospitality sector, reflecting Morocco's "
            "labour migration to the Gulf. Morocco and Bahrain are both members "
            "of the Arab League and the Organisation of Islamic Cooperation (OIC). "
            "Moroccan death certificates (acte de deces, in Arabic and French) "
            "require certified Arabic translation for sections not already in "
            "Arabic, plus authentication by the Bahraini Embassy in Rabat. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'algeria', 'dest': 'bahrain',
        'embassy_city': 'Algiers',
        'intro': (
            "Algerian nationals in Bahrain include workers and professionals in "
            "construction and technical sectors. Algeria and Bahrain are both "
            "members of the Arab League and the Organisation of Islamic Cooperation "
            "(OIC). Arabic-language Algerian death certificates (acte de deces) "
            "require authentication by the Bahraini Embassy in Algiers before "
            "submission to the Civil Status and Passports Affairs Authority (CSPA). "
            "Algeria is not a Hague Apostille Convention member; full consular "
            "authentication is required. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R57 -- South Korea wave 7
    {
        'origin': 'canada', 'dest': 'south-korea',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in South Korea include English teachers, business "
            "professionals, students, and a well-established expatriate community. "
            "Canada and South Korea have a bilateral Free Trade Agreement "
            "(CKFTA, 2015) and strong people-to-people ties. Canadian death "
            "certificates (in English or French, depending on province) require "
            "certified Korean translation and authentication through the South "
            "Korean Embassy in Ottawa before the gu office (ward office) can "
            "register the death. South Korea is not a Hague Apostille Convention "
            "member. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'south-korea',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in South Korea include professionals in automotive, "
            "manufacturing, and trade sectors, and a business community reflecting "
            "significant German investment in the Korean market. German death "
            "certificates (Sterbeurkunde, in German) require certified Korean "
            "translation and authentication through the South Korean Embassy in "
            "Berlin before the gu office (ward office) can register the death. "
            "South Korea is not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'south-korea',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in South Korea include professionals, students, and "
            "a community with France-Korea cultural and business ties. France and "
            "South Korea have bilateral diplomatic relations and active cultural "
            "exchange. French death certificates (acte de deces, in French) require "
            "certified Korean translation and authentication through the South "
            "Korean Embassy in Paris before the gu office (ward office) can "
            "register the death. South Korea is not a Hague Apostille Convention "
            "member. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'south-korea',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in South Korea include professionals in design, "
            "fashion, and manufacturing sectors, and a community with Italy-Korea "
            "connections through the EU-Korea Free Trade Agreement (2011). Italian "
            "death certificates (atto di morte, in Italian) require certified "
            "Korean translation and authentication through the South Korean Embassy "
            "in Rome before the gu office (ward office) can register the death. "
            "South Korea is not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'new-zealand', 'dest': 'south-korea',
        'embassy_city': 'Wellington',
        'intro': (
            "New Zealand nationals in South Korea include English teachers, "
            "students, and professionals on bilateral exchange. New Zealand and "
            "South Korea have a bilateral Free Trade Agreement (NZKFTA, 2015) "
            "and growing people-to-people connections. New Zealand death "
            "certificates (in English) require certified Korean translation and "
            "authentication through the South Korean Embassy in Wellington before "
            "the gu office (ward office) can register the death. South Korea is "
            "not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R57 -- Japan wave 12
    {
        'origin': 'mexico', 'dest': 'japan',
        'embassy_city': 'Mexico City',
        'intro': (
            "Mexican nationals in Japan include students, academics, and "
            "professionals. Mexico and Japan have a bilateral Economic Partnership "
            "Agreement (MexJEPA, 2005) and cultural connections through the Nikkei "
            "Japanese-Mexican community, one of the larger Nikkei communities in "
            "Latin America. Spanish-language Mexican death certificates (acta de "
            "defuncion) require certified Japanese translation and authentication "
            "through the Japanese Embassy in Mexico City. Both Mexico and Japan "
            "are Hague Apostille Convention members, which simplifies document "
            "authentication. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'colombia', 'dest': 'japan',
        'embassy_city': 'Bogota',
        'intro': (
            "Colombian nationals in Japan include students, professionals, and "
            "a growing community with bilateral ties. Colombia and Japan maintain "
            "diplomatic relations and bilateral economic cooperation. Spanish-language "
            "Colombian death certificates (acta de defuncion) require certified "
            "Japanese translation and authentication through the Japanese Embassy "
            "in Bogota. Both Colombia and Japan are Hague Apostille Convention "
            "members. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'peru', 'dest': 'japan',
        'embassy_city': 'Lima',
        'intro': (
            "Peruvian nationals in Japan include a significant and long-established "
            "Nikkei (Japanese-Peruvian) community, one of the largest Nikkei "
            "populations worldwide. Peru and Japan have strong bilateral ties "
            "through migration history, with diplomatic relations maintained since "
            "1873. Spanish-language Peruvian death certificates (acta de defuncion) "
            "require certified Japanese translation and authentication through the "
            "Japanese Embassy in Lima. Both Peru and Japan are Hague Apostille "
            "Convention members. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'morocco', 'dest': 'japan',
        'embassy_city': 'Rabat',
        'intro': (
            "Moroccan nationals in Japan include students, academics, and "
            "professionals on bilateral cultural and academic exchange. Morocco "
            "and Japan have maintained bilateral diplomatic relations and economic "
            "ties. Moroccan death certificates (in Arabic and French) require "
            "certified Japanese translation and authentication through the Japanese "
            "Embassy in Rabat. Both Morocco and Japan are Hague Apostille "
            "Convention members. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'algeria', 'dest': 'japan',
        'embassy_city': 'Algiers',
        'intro': (
            "Algerian nationals in Japan include students and academics on "
            "scientific and cultural exchange programmes. Algeria and Japan have "
            "maintained bilateral diplomatic relations and cooperation through "
            "bilateral agreements. Arabic-language Algerian death certificates "
            "require certified Japanese translation and authentication through "
            "the Japanese Embassy in Algiers. Japan is a Hague Apostille "
            "Convention member; Algeria is not, so full consular authentication "
            "through the Japanese Embassy in Algiers is required. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R57 -- Oman wave 9
    {
        'origin': 'yemen', 'dest': 'oman',
        'embassy_city': "Sana'a",
        'intro': (
            "Yemeni nationals form one of the largest foreign communities in Oman, "
            "with many Yemeni workers in construction, services, and agriculture. "
            "Yemen and Oman share a border and have historically close ties. The "
            "ongoing conflict in Yemen means the FCDO advises against all travel "
            "and civil registration services are severely disrupted in most areas. "
            "Families should seek specialist support at the earliest opportunity "
            "and contact the Omani Ministry of Foreign Affairs directly, as the "
            "Omani Embassy in Sana'a has limited operations. Documentation is "
            "in Arabic. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'singapore', 'dest': 'oman',
        'embassy_city': 'Singapore',
        'intro': (
            "Singaporean nationals in Oman include finance professionals, engineers, "
            "and technical specialists. Singapore and Oman have bilateral trade and "
            "investment ties through Gulf-Southeast Asian economic frameworks. "
            "English-language Singapore death certificates require certified Arabic "
            "translation for the Royal Oman Police civil registration section and "
            "authentication by the Omani Embassy in Singapore. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'oman',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japanese nationals in Oman include engineers, construction professionals, "
            "and business executives in infrastructure and energy projects. Japan "
            "and Oman have maintained strong bilateral energy cooperation, with Oman "
            "supplying a portion of Japan's liquefied natural gas imports. Japanese "
            "death certificates (shibo todoke, in Japanese) require certified Arabic "
            "translation for the Royal Oman Police civil registration section and "
            "authentication by the Omani Embassy in Tokyo. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'afghanistan', 'dest': 'oman',
        'embassy_city': 'Islamabad',
        'intro': (
            "Afghan nationals in Oman include workers in construction and domestic "
            "service sectors. Afghanistan and Oman maintain diplomatic relations, "
            "though the situation in Afghanistan since August 2021 means consular "
            "access is severely curtailed. The FCDO advises against all travel to "
            "Afghanistan. The Omani Embassy in Islamabad covers consular matters "
            "for Afghanistan. All documentation in Dari or Pashto requires "
            "certified Arabic translation for the Royal Oman Police civil "
            "registration section. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'tanzania', 'dest': 'oman',
        'embassy_city': 'Dar es Salaam',
        'intro': (
            "Tanzanian nationals in Oman include workers in construction and "
            "domestic service sectors, reflecting East African labour migration "
            "to the Gulf. Tanzania and Oman maintain diplomatic relations and the "
            "Omani Embassy in Dar es Salaam handles consular matters. Tanzanian "
            "death certificates (in Swahili and English) require certified Arabic "
            "translation for the Royal Oman Police civil registration section. "
            "Families should contact the Omani Embassy in Dar es Salaam at the "
            "earliest opportunity. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R58 -- Turkey wave 6
    {
        'origin': 'france', 'dest': 'turkey',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Turkey include tourists, students, professionals, "
            "and a community with close bilateral ties through NATO membership and "
            "long-standing diplomatic relations. France and Turkey have maintained "
            "bilateral economic and diplomatic relations since Ottoman times. French "
            "death certificates (acte de deces, in French) require certified Turkish "
            "translation for the local nufus mudurlugu (population directorate) and "
            "authentication by the Turkish Embassy in Paris. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'turkey',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Turkey include tourists, professionals, and a "
            "business community reflecting Turkey-Italy trade ties. Italy and Turkey "
            "have significant bilateral trade and investment relations, with Italy "
            "among Turkey's largest trading partners in the EU. Italian death "
            "certificates (atto di morte, in Italian) require certified Turkish "
            "translation for the local nufus mudurlugu and authentication by the "
            "Turkish Embassy in Rome. (Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'turkey',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Turkey include tourists, students, and "
            "professionals. Spain and Turkey have bilateral diplomatic and trade "
            "relations within NATO and EU-Turkey frameworks. Spanish death "
            "certificates (certificado de defuncion, in Spanish) require certified "
            "Turkish translation for the local nufus mudurlugu and authentication "
            "by the Turkish Embassy in Madrid. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'turkey',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in Turkey include tourists, professionals, and a "
            "community with bilateral ties linked to the large Turkish-Dutch "
            "diaspora. The Netherlands has one of the largest Turkish diaspora "
            "communities in Europe, and bilateral people-to-people ties are "
            "substantial. Dutch death certificates (akte van overlijden, in Dutch) "
            "require certified Turkish translation for the local nufus mudurlugu "
            "and authentication by the Turkish Embassy in The Hague. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'turkey',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgian nationals in Turkey include tourists, professionals, and a "
            "community with bilateral ties through Belgium's Turkish diaspora, "
            "particularly in Brussels and Liege. Belgium and Turkey have bilateral "
            "diplomatic relations within NATO. Belgian death certificates (acte de "
            "deces or akte van overlijden, in French or Dutch depending on region) "
            "require certified Turkish translation for the local nufus mudurlugu "
            "and authentication by the Turkish Embassy in Brussels. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R58 -- Malaysia wave 7
    {
        'origin': 'turkey', 'dest': 'malaysia',
        'embassy_city': 'Ankara',
        'intro': (
            "Turkish nationals in Malaysia include business professionals, students, "
            "and a community with bilateral ties through OIC membership and "
            "expanding trade. Turkey and Malaysia have maintained bilateral economic "
            "ties within the D-8 Organisation for Economic Cooperation framework. "
            "Turkish death certificates (olum belgesi, in Turkish) require certified "
            "translation for the National Registration Department (Jabatan "
            "Pendaftaran Negara). The Malaysian High Commission in Ankara handles "
            "consular matters for Turkey. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'egypt', 'dest': 'malaysia',
        'embassy_city': 'Cairo',
        'intro': (
            "Egyptian nationals in Malaysia include students at Malaysian "
            "universities, academics, and a community with Islamic educational "
            "and cultural ties. Egypt and Malaysia have bilateral ties within the "
            "OIC and through academic exchange. Arabic-language Egyptian death "
            "certificates require certified translation for the National "
            "Registration Department (Jabatan Pendaftaran Negara). For Muslim "
            "remains, a burial permit from the Jabatan Agama Islam is required. "
            "The Malaysian Embassy in Cairo handles consular matters. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'iran', 'dest': 'malaysia',
        'embassy_city': 'Tehran',
        'intro': (
            "Iranian nationals in Malaysia include students at Malaysian "
            "universities, business professionals, and a community with OIC ties. "
            "Malaysia and Iran have maintained bilateral diplomatic relations within "
            "the OIC, and Kuala Lumpur has historically welcomed Iranian students "
            "seeking education abroad. Farsi-language Iranian death certificates "
            "require certified translation for the National Registration Department "
            "(Jabatan Pendaftaran Negara). Families should be aware that the FCDO "
            "advises against all travel to Iran and that the British Embassy in "
            "Tehran has been closed since 2011. The Malaysian Embassy in Tehran "
            "handles consular matters. (Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'malaysia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Malaysia include professionals in manufacturing, "
            "automotive, and engineering sectors, expatriates, and tourists. "
            "Germany and Malaysia have bilateral investment ties through ASEAN-EU "
            "frameworks and significant German manufacturing investment in Malaysia. "
            "German death certificates (Sterbeurkunde, in German) require certified "
            "translation for the National Registration Department (Jabatan "
            "Pendaftaran Negara). The Malaysian High Commission in Berlin handles "
            "consular matters. (Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'malaysia',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Malaysia include professionals, expatriates in "
            "the energy and technology sectors, and tourists. France and Malaysia "
            "have bilateral diplomatic and economic ties through ASEAN-EU frameworks "
            "and French investment in Malaysian industry. French death certificates "
            "(acte de deces, in French) require certified translation for the "
            "National Registration Department (Jabatan Pendaftaran Negara). The "
            "Malaysian High Commission in Paris handles consular matters. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R58 -- Indonesia wave 4
    {
        'origin': 'south-africa', 'dest': 'indonesia',
        'embassy_city': 'Pretoria',
        'intro': (
            "South African nationals in Indonesia include business professionals, "
            "resources sector workers, and tourists, particularly in Bali. South "
            "Africa and Indonesia have bilateral ties through the Indian Ocean Rim "
            "Association (IORA) and bilateral cooperation frameworks. South African "
            "death certificates (in English or Afrikaans) require certified "
            "Indonesian translation for the Disdukcapil and authentication by the "
            "Indonesian Embassy in Pretoria. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'indonesia',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in Indonesia include business professionals in "
            "resources and energy, tourists, and expatriates, particularly in Bali. "
            "Canada and Indonesia have bilateral diplomatic ties and cooperation "
            "through ASEAN-Canada frameworks. Canadian death certificates (in "
            "English or French) require certified Indonesian translation for the "
            "Disdukcapil and authentication by the Indonesian Embassy in Ottawa. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'indonesia',
        'embassy_city': 'Oslo',
        'intro': (
            "Norwegian nationals in Indonesia include professionals in oil, gas, "
            "and maritime industries, and tourists, particularly in Bali. Norway "
            "and Indonesia have bilateral ties through energy sector cooperation "
            "and Norwegian investment in Indonesian resources. Norwegian death "
            "certificates (in Norwegian) require certified Indonesian translation "
            "for the Disdukcapil and authentication by the Indonesian Embassy in "
            "Oslo. (Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'indonesia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in Indonesia include business professionals, "
            "expatriates, and tourists, particularly in Bali. Sweden and Indonesia "
            "have bilateral diplomatic ties and cooperation through ASEAN-EU "
            "frameworks, with Swedish investment in Indonesian manufacturing and "
            "sustainability sectors. Swedish death certificates (in Swedish) require "
            "certified Indonesian translation for the Disdukcapil and authentication "
            "by the Indonesian Embassy in Stockholm. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'hong-kong', 'dest': 'indonesia',
        'embassy_city': 'Hong Kong',
        'intro': (
            "Hong Kong residents in Indonesia include business professionals in "
            "finance and trade, and tourists, particularly in Bali. Hong Kong "
            "and Indonesia have significant commercial ties, with Hong Kong serving "
            "as a major financial intermediary for Indonesian trade and investment. "
            "Hong Kong death certificates (in English and Chinese) require certified "
            "Indonesian translation for the Disdukcapil and authentication by the "
            "Indonesian Consulate-General in Hong Kong. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R58 -- South Korea wave 8
    {
        'origin': 'spain', 'dest': 'south-korea',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in South Korea include students, academics, and "
            "professionals on cultural and bilateral exchange. Spain and South Korea "
            "have maintained diplomatic relations and cultural exchange through "
            "bilateral cooperation. Spanish death certificates (certificado de "
            "defuncion, in Spanish) require certified Korean translation and "
            "authentication through the South Korean Embassy in Madrid before the "
            "gu office (ward office) can register the death. South Korea is not a "
            "Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'south-korea',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in South Korea include business professionals in "
            "trade, logistics, and technology sectors, and a community with "
            "bilateral ties through significant Dutch-Korean business links. The "
            "Netherlands has active trade and investment ties with South Korea "
            "through EU-Korea cooperation. Dutch death certificates (akte van "
            "overlijden, in Dutch) require certified Korean translation and "
            "authentication through the South Korean Embassy in The Hague before "
            "the gu office (ward office) can register the death. South Korea is "
            "not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'south-korea',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgian nationals in South Korea include business professionals, "
            "students, and professionals in the automotive and technology sectors. "
            "Belgium and South Korea have bilateral ties through EU-Korea economic "
            "cooperation. Belgian death certificates (acte de deces or akte van "
            "overlijden, in French or Dutch depending on region) require certified "
            "Korean translation and authentication through the South Korean Embassy "
            "in Brussels before the gu office (ward office) can register the death. "
            "South Korea is not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'south-korea',
        'embassy_city': 'Bern',
        'intro': (
            "Swiss nationals in South Korea include professionals in finance, "
            "pharmaceuticals, and technology sectors. Switzerland and South Korea "
            "have a bilateral free trade agreement (EFTA-Korea FTA, 2006) and "
            "active investment ties. Swiss death certificates (Todesschein, in "
            "German, French, or Italian depending on the canton) require certified "
            "Korean translation and authentication through the South Korean Embassy "
            "in Bern before the gu office (ward office) can register the death. "
            "South Korea is not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'south-korea',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in South Korea include professionals in technology, "
            "automotive, and manufacturing sectors, and a community with bilateral "
            "ties. Sweden and South Korea have maintained bilateral diplomatic "
            "relations and bilateral trade links. Swedish death certificates "
            "(in Swedish) require certified Korean translation and authentication "
            "through the South Korean Embassy in Stockholm before the gu office "
            "(ward office) can register the death. South Korea is not a Hague "
            "Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R58 -- Japan wave 13
    {
        'origin': 'venezuela', 'dest': 'japan',
        'embassy_city': 'Caracas',
        'intro': (
            "Venezuelan nationals in Japan include students, professionals, and "
            "a small community. Venezuela and Japan have maintained bilateral "
            "diplomatic relations. Spanish-language Venezuelan death certificates "
            "(acta de defuncion) require certified Japanese translation and "
            "authentication through the Japanese Embassy in Caracas. Both "
            "Venezuela and Japan are Hague Apostille Convention members, which "
            "simplifies document authentication. Families should be aware that "
            "civil registration capacity in Venezuela may be affected by "
            "infrastructure constraints. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'chile', 'dest': 'japan',
        'embassy_city': 'Santiago',
        'intro': (
            "Chilean nationals in Japan include professionals, students, and a "
            "Nikkei (Japanese-Chilean) community with long-established bilateral "
            "ties. Chile and Japan have strong trade connections through Japan's "
            "imports of Chilean copper and agricultural products, and bilateral "
            "diplomatic relations since 1897. Spanish-language Chilean death "
            "certificates (certificado de defuncion) require certified Japanese "
            "translation and authentication through the Japanese Embassy in "
            "Santiago. Both Chile and Japan are Hague Apostille Convention members. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'tanzania', 'dest': 'japan',
        'embassy_city': 'Dar es Salaam',
        'intro': (
            "Tanzanian nationals in Japan include students on academic scholarships "
            "and a small community of professionals. Tanzania and Japan have "
            "bilateral ties through Japan's Official Development Assistance (ODA) "
            "programmes, with Japan among Tanzania's long-standing development "
            "partners. Tanzanian death certificates (in Swahili and English) require "
            "certified Japanese translation and authentication through the Japanese "
            "Embassy in Dar es Salaam. Families should confirm current authentication "
            "requirements with the Embassy. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ivory-coast', 'dest': 'japan',
        'embassy_city': 'Abidjan',
        'intro': (
            "Ivorian nationals in Japan include students and academics on "
            "scholarship programmes and a small professional community. Ivory Coast "
            "and Japan have bilateral ties through Japan's development cooperation "
            "in West Africa and the TICAD (Tokyo International Conference on African "
            "Development) frameworks. French-language Ivorian death certificates "
            "(acte de deces) require certified Japanese translation and "
            "authentication through the Japanese Embassy in Abidjan. Japan is a "
            "Hague Apostille Convention member; Ivory Coast is not, so full "
            "consular authentication through the Japanese Embassy in Abidjan is "
            "required. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'cameroon', 'dest': 'japan',
        'embassy_city': 'Yaounde',
        'intro': (
            "Cameroonian nationals in Japan include students, particularly those "
            "on Japanese Government (MEXT) scholarship programmes, and a small "
            "professional community. Cameroon and Japan have bilateral ties through "
            "Japan's TICAD development cooperation framework and development "
            "assistance to Cameroon. French-language Cameroonian death certificates "
            "(acte de deces) require certified Japanese translation and "
            "authentication through the Japanese Embassy in Yaounde. Japan is a "
            "Hague Apostille Convention member; Cameroon is not, so full consular "
            "authentication through the Japanese Embassy in Yaounde is required. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
]


def make_dest_key(dest_slug):
    keys = {
        'south-korea': 'kr', 'bahrain': 'bh', 'japan': 'jp',
        'oman': 'om', 'indonesia': 'id', 'turkey': 'tr', 'malaysia': 'my',
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
    description = (
        f"Someone has died in {origin_name}. Repatriation to {dest_name} "
        f"takes {timeline_avg}. {desc_note} Contact us 24/7."
    )

    dest_reception = dm['reception']
    dest_consular = dm['consular_template'].format(city=embassy_city)
    arrival_faq = dm['arrival_faq']

    pts = [
        f"Key document: {od['cert_name']} (in {od['cert_lang']})",
        f"Documentation takes {doc_time}. Appoint a specialist on day one.",
        (
            f"British Embassy or High Commission in {embassy_city} registers "
            f"the death and advises. They cannot fund repatriation."
        ),
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
    timing: "Day of death. Call +44 (0)20 7008 5000 (FCDO) or {emergency_line}."
    responsible: "Family or travel insurer"
  - step: 2
    action: "{step2_action}"
    timing: "{step2_timing}"
    responsible: "Local funeral director and registry"
  - step: 3
    action: "{dest_name} Embassy in {embassy_city} notified"
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
    - url: "/routes/{origin_slug}-to-united-kingdom/"
      text: "Repatriation from {origin_name} to the UK"
    - url: "/routes/{origin_slug}-to-ireland/"
      text: "Repatriation from {origin_name} to Ireland"
"""

    content = f"""---
title: "{origin_name} to {dest_name}: Repatriation Guidance"
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

        # QA: check for em dashes
        check = content.replace('---', '').replace('--gc', '')
        if '--' in check or '—' in content:
            msg = f"ERROR em dash in {slug}"
            print(msg)
            errors.append(msg)
            continue

        # QA: banned vocab check
        lower_content = content.lower()
        found_banned = [w for w in banned if w in lower_content]
        if found_banned:
            msg = f"ERROR banned vocab in {slug}: {found_banned}"
            print(msg)
            errors.append(msg)
            continue

        # QA: no price language
        price_patterns = [
            'prices start', 'from £', 'from $', 'cost from',
            'price from', 'prices from',
        ]
        if any(p in lower_content for p in price_patterns):
            msg = f"ERROR price language in {slug}"
            print(msg)
            errors.append(msg)
            continue

        # QA: no safety guarantees
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
