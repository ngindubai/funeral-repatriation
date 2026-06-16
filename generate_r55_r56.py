#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R55-R56.

   R55 (25 routes, variants D,E,A,B,C x5):
     Bahrain wave 5 x5: malaysia, myanmar, cambodia, china, uzbekistan
     South Korea wave 5 x5: japan, hong-kong, turkey, egypt, sri-lanka
     Japan wave 10 x5: austria, denmark, finland, norway, sweden
     Oman wave 7 x5: south-africa, eritrea, laos, myanmar, south-korea
     Indonesia NEW HUB wave 1 x5: india, malaysia, netherlands, china, australia

   R56 (25 routes, variants D,E,A,B,C x5):
     Indonesia wave 2 x5: singapore, japan, germany, usa, south-korea
     Bahrain wave 6 x5: laos, russia, senegal, cameroon, afghanistan
     Japan wave 11 x5: portugal, switzerland, belgium, poland, greece
     South Korea wave 6 x5: ghana, nigeria, kenya, ethiopia, jordan
     Oman wave 8 x5: bahrain, kuwait, qatar, new-zealand, djibouti

   Template rotation: R54 ended C (index 2). R55 starts D (index 3).
   Each block of 25 cycles D,E,A,B,C x5, ending on C. R56 starts D again.

   Embassy notes:
   - Bahrain-Myanmar: Bahrain Embassy in Bangkok covers Myanmar.
   - Bahrain-Cambodia: Bahrain Embassy in Bangkok covers Cambodia.
   - Bahrain-Uzbekistan: families should verify current Bahraini consular
     arrangements for Uzbekistan; may be covered from Riyadh or Amman.
   - Bahrain-Senegal/Cameroon: Bahraini Embassy in Paris or nearest post.
   - Bahrain-Afghanistan: Bahraini Embassy in Islamabad covers Afghanistan.
   - Bahrain-Laos: Bahraini Embassy in Bangkok covers Laos.
   - Oman-Eritrea: families should verify Omani consular arrangements for
     Eritrea; Oman maintains an Embassy in Asmara.
   - Oman-Laos: Omani Embassy in Bangkok covers Laos.
   - Oman-Myanmar: Omani Embassy in Yangon handles Myanmar.
   - Oman-Djibouti: Omani Embassy in Djibouti.
   - NZ-Oman: Omani Embassy in Canberra covers New Zealand.
   - Indonesia hub: Soekarno-Hatta (CGK) Jakarta and Ngurah Rai (DPS) Bali.
   - Japan-Denmark/Finland/Norway/Sweden: Hague Apostille simplifies auth.
   - Japan-Austria: Austrian Standesamt; Hague Apostille applies.
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
}

ORIGIN_DATA = {
    # --- countries already established in prior generators ---
    'india': {
        'name': 'India',
        'emergency': '112 (national) / 100 (police) / 108 (ambulance)',
        'registry': 'the local municipal authority',
        'cert_name': 'death certificate',
        'cert_lang': 'English and local language',
        'overview': (
            "Contact local emergency services (112, or 100 for police, 108 for "
            "ambulance). If death occurs outside hospital, police must be notified. "
            "Death must be registered with the local municipal authority within "
            "21 days. India's tropical climate requires urgent embalming."
        ),
        'doc_time': '14-30 days minimum. Post-mortem cases take longer.',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '8-16 weeks or longer',
        'complexity': 'high',
        'cremation': 'Cremation in India is well established and widely available.',
        'postmortem_trigger': (
            'Indian police routinely order post-mortem examinations for unexpected '
            'deaths of foreign nationals'
        ),
    },
    'malaysia': {
        'name': 'Malaysia',
        'emergency': '999',
        'registry': 'the National Registration Department (Jabatan Pendaftaran Negara)',
        'cert_name': 'death certificate (sijil kematian)',
        'cert_lang': 'Bahasa Malaysia',
        'overview': (
            "Call 999 for emergency services. Death is certified by a registered "
            "medical practitioner. The death is registered with the National "
            "Registration Department (Jabatan Pendaftaran Negara). Police take "
            "jurisdiction for violent or unexplained deaths. Documentation is "
            "in Bahasa Malaysia and requires certified translation."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Malaysia is available and widely used by non-Muslim '
            'communities. Muslim remains must be buried in accordance with '
            'Islamic law.'
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'myanmar': {
        'name': 'Myanmar',
        'emergency': '199 (police) / 192 (fire)',
        'registry': 'the General Administration Department (GAD)',
        'cert_name': 'death certificate (in Burmese)',
        'cert_lang': 'Burmese (Myanmar)',
        'overview': (
            "Call 199 for police. A physician must certify the death. The death "
            "is registered with the General Administration Department (GAD). "
            "Police take jurisdiction for violent or unexplained deaths. The FCDO "
            "advises against all travel to Myanmar; consular access is severely "
            "limited. Families should contact the nearest operational embassy "
            "immediately. Documentation is in Burmese and requires certified "
            "translation."
        ),
        'doc_time': 'Weeks to months; highly variable given current conditions',
        'timeline_avg': '6-12 weeks',
        'timeline_fast': '4-6 weeks',
        'timeline_complex': 'Several months or longer',
        'complexity': 'high',
        'cremation': 'Cremation in Myanmar is available and commonly used in Buddhist communities.',
        'postmortem_trigger': (
            'Violent or unexplained deaths; the security situation may further '
            'restrict access to authorities'
        ),
    },
    'cambodia': {
        'name': 'Cambodia',
        'emergency': '117 (police) / 119 (ambulance)',
        'registry': 'the Ministry of Interior civil registry',
        'cert_name': 'death certificate (in Khmer)',
        'cert_lang': 'Khmer',
        'overview': (
            "Call 117 for police or 119 for ambulance. Death is certified by a "
            "licensed physician. Registration is required with the local Ministry "
            "of Interior civil registry office. Police take jurisdiction for violent "
            "or unexplained deaths. Cambodia's tropical climate requires urgent "
            "embalming. Documentation in Khmer requires certified translation."
        ),
        'doc_time': '10-21 days',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': '10-16 weeks',
        'complexity': 'high',
        'cremation': (
            'Cremation in Cambodia is available and commonly used in Buddhist '
            'communities.'
        ),
        'postmortem_trigger': (
            'Violent, accidental, or unexplained deaths, particularly drowning '
            'and road traffic accidents'
        ),
    },
    'uzbekistan': {
        'name': 'Uzbekistan',
        'emergency': '102 (police) / 103 (ambulance)',
        'registry': 'the local Hukumati (civil administration) registration office',
        'cert_name': 'death certificate',
        'cert_lang': 'Uzbek or Russian',
        'overview': (
            "Contact emergency services (102 for police, 103 for ambulance). Death "
            "must be registered with the Hukumati (local civil administration) "
            "registration office. The Prosecutor's Office takes jurisdiction for "
            "violent, suspicious, or unexplained deaths."
        ),
        'doc_time': '7-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is available in Uzbekistan.',
        'postmortem_trigger': 'Violent, suspicious, or unexplained deaths',
    },
    'japan': {
        'name': 'Japan',
        'emergency': '110 (police) / 119 (ambulance)',
        'registry': 'the local municipal office (shiyakusho or kuyakusho)',
        'cert_name': 'shibo todoke (death notification, in Japanese)',
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
        'postmortem_trigger': (
            'Violent or unexplained deaths (public prosecutor, Kenji)'
        ),
    },
    'turkey': {
        'name': 'Turkey',
        'emergency': '155 (police) / 112 (ambulance)',
        'registry': 'the nufus mudurlugu (population directorate)',
        'cert_name': 'olum belgesi (death certificate, in Turkish)',
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
            'Cremation is not available in Turkey. Burial is the required '
            'final disposition.'
        ),
        'postmortem_trigger': (
            'Violent, sudden, or unexplained deaths '
            '(Cumhuriyet Savcilik)'
        ),
    },
    'russia': {
        'name': 'Russia',
        'emergency': '112 / 102 (police) / 103 (ambulance)',
        'registry': 'the local ZAGS (Registry Office)',
        'cert_name': 'svidetelstvo o smerti (death certificate, in Russian)',
        'cert_lang': 'Russian',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician "
            "and the svidetelstvo o smerti is registered with the local ZAGS "
            "(Registry Office). Police and the Sledstvenny Komitet (Investigative "
            "Committee) take jurisdiction for violent or unexplained deaths. "
            "Families should be aware that the FCDO advises against travel to "
            "Russia, and consular access by some Western embassies has been "
            "significantly reduced since 2022."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': '3 months or longer',
        'complexity': 'high',
        'cremation': 'Cremation in Russia is widely available in major cities.',
        'postmortem_trigger': (
            'Violent, sudden, or unexplained deaths '
            '(Sledstvenny Komitet)'
        ),
    },
    'laos': {
        'name': 'Laos',
        'emergency': '191 (police) / 195 (ambulance)',
        'registry': 'the Ministry of Home Affairs civil registry',
        'cert_name': 'death certificate (in Lao)',
        'cert_lang': 'Lao',
        'overview': (
            "Call 191 for police or 195 for ambulance. Death is certified by a "
            "licensed physician. Registration is required with the local Ministry "
            "of Home Affairs civil registry. Police take jurisdiction for violent "
            "or unexplained deaths. Outside Vientiane, access to civil registry "
            "services and international transport links is limited. Documentation "
            "is in Lao and requires certified translation."
        ),
        'doc_time': '14-30 days',
        'timeline_avg': '5-8 weeks',
        'timeline_fast': '3-5 weeks',
        'timeline_complex': '10-16 weeks',
        'complexity': 'high',
        'cremation': (
            'Cremation in Laos is available and common in Buddhist communities.'
        ),
        'postmortem_trigger': 'Violent, accidental, or unexplained deaths',
    },
    'bahrain': {
        'name': 'Bahrain',
        'emergency': '999',
        'registry': 'the Civil Status and Passports Affairs Authority (CSPA)',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 999 for emergency services. Death is certified by a physician "
            "and registered with the Civil Status and Passports Affairs Authority "
            "(CSPA) under the Ministry of Interior. For Muslim remains, Islamic "
            "law requires prompt preparation and burial; a special CSPA "
            "authorisation is required to delay disposition for international "
            "repatriation. All documentation is in Arabic and requires certified "
            "translation. Bahrain's climate requires prompt embalming."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Bahrain.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'kuwait': {
        'name': 'Kuwait',
        'emergency': '112 (police) / 112 (ambulance)',
        'registry': 'the Civil Registration Affairs Authority',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician "
            "and registered with the Civil Registration Affairs Authority. The "
            "Public Prosecution takes jurisdiction for violent or unexplained "
            "deaths. All documentation is in Arabic and requires certified "
            "translation. Kuwait's climate requires prompt embalming."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Kuwait.',
        'postmortem_trigger': (
            'Violent or unexplained deaths (Public Prosecution)'
        ),
    },
    'qatar': {
        'name': 'Qatar',
        'emergency': '999 (police) / 999 (ambulance)',
        'registry': 'the Ministry of Interior civil registration system',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 999 for emergency services. Death is certified by a physician "
            "and registered through the Ministry of Interior civil registration "
            "system. The Public Prosecution takes jurisdiction for violent or "
            "unexplained deaths. All documentation is in Arabic and requires "
            "certified translation. Qatar's climate requires prompt embalming."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Qatar.',
        'postmortem_trigger': (
            'Violent or unexplained deaths (Public Prosecution)'
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
        'cremation': 'Cremation in Singapore is widely available and commonly used.',
        'postmortem_trigger': 'Sudden or unexplained deaths (coroner takes jurisdiction)',
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
        'cremation': 'Cremation in Germany is widely available.',
        'postmortem_trigger': (
            'Violent or unexplained deaths (Staatsanwaltschaft)'
        ),
    },
    'usa': {
        'name': 'the United States',
        'emergency': '911',
        'registry': 'the state civil records office',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician or "
            "medical examiner. The death is registered with the state civil records "
            "office. The county medical examiner or coroner takes jurisdiction for "
            "sudden, violent, or unexplained deaths. The United States is a Hague "
            "Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks (longer if medical examiner involved)',
        'complexity': 'low',
        'cremation': 'Cremation in the United States is widely available.',
        'postmortem_trigger': (
            'Sudden, violent, or unexplained deaths (county medical examiner or coroner)'
        ),
    },
    'australia': {
        'name': 'Australia',
        'emergency': '000',
        'registry': 'the state or territory Registry of Births, Deaths and Marriages',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 000 for emergency services. Death is certified by a registered "
            "medical practitioner. The death is registered with the relevant state "
            "or territory Registry of Births, Deaths and Marriages. The coroner "
            "takes jurisdiction for sudden, unexpected, or unnatural deaths. "
            "Australia is a Hague Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks (longer if coroner involved)',
        'complexity': 'low',
        'cremation': 'Cremation in Australia is widely available and commonly used.',
        'postmortem_trigger': (
            'Sudden, unexpected, or violent deaths (coroner takes jurisdiction)'
        ),
    },
    # --- new origin countries for R55-R56 ---
    'china': {
        'name': 'China',
        'emergency': '120 (ambulance) / 110 (police)',
        'registry': 'the local civil affairs bureau (minzhengju)',
        'cert_name': 'si wang zheng ming shu (death certificate)',
        'cert_lang': 'Mandarin Chinese',
        'overview': (
            "Call 120 for ambulance or 110 for police. A physician must certify "
            "the death at a recognised medical facility. The si wang zheng ming "
            "shu is registered with the local civil affairs bureau (minzhengju). "
            "Police and the judiciary take jurisdiction for violent or unexplained "
            "deaths. All documentation is in Mandarin Chinese and requires "
            "certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in China is widely available and commonly used.',
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
    'egypt': {
        'name': 'Egypt',
        'emergency': '122 (police) / 123 (ambulance)',
        'registry': 'the local health office (through the niyaba, public prosecutor)',
        'cert_name': 'death certificate (in Arabic)',
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
        'cremation': 'Cremation is not available in Egypt. All repatriations must be of the full body.',
        'postmortem_trigger': 'All unnatural, sudden, or suspicious deaths (niyaba takes jurisdiction)',
    },
    'sri-lanka': {
        'name': 'Sri Lanka',
        'emergency': '119 (police) / 110 (ambulance)',
        'registry': 'the Registrar General\'s Department',
        'cert_name': 'death certificate (in Sinhala and English)',
        'cert_lang': 'Sinhala and English',
        'overview': (
            "Call 119 for police or 110 for ambulance. Death is certified by a "
            "physician. Registration is with the Registrar General's Department. "
            "Police take jurisdiction for violent or unexplained deaths. "
            "Sri Lanka's tropical climate requires urgent embalming."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Sri Lanka is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'hong-kong': {
        'name': 'Hong Kong',
        'emergency': '999',
        'registry': 'the Registry of Births and Deaths (Immigration Department)',
        'cert_name': 'death certificate (in English and Chinese)',
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
        'cremation': 'Cremation in Hong Kong is widely available and commonly used.',
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (Coroner\'s Court)',
    },
    'austria': {
        'name': 'Austria',
        'emergency': '133 (police) / 144 (ambulance)',
        'registry': 'the local Standesamt (civil registry)',
        'cert_name': 'Sterbeurkunde (death certificate, in German)',
        'cert_lang': 'German',
        'overview': (
            "Call 133 for police or 144 for ambulance. A physician certifies the "
            "death. The Sterbeurkunde is registered with the local Standesamt. "
            "The Staatsanwaltschaft (public prosecutor) takes jurisdiction for "
            "violent or unexplained deaths. Austria is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Austria is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft)',
    },
    'denmark': {
        'name': 'Denmark',
        'emergency': '112',
        'registry': 'the local civil registration office',
        'cert_name': 'death certificate (in Danish)',
        'cert_lang': 'Danish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The death is registered with the local civil registration office. "
            "Police take jurisdiction for violent or unexplained deaths. Denmark "
            "is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Denmark is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'finland': {
        'name': 'Finland',
        'emergency': '112',
        'registry': 'the Digital and Population Data Services Agency (DVV)',
        'cert_name': 'death certificate (in Finnish or Swedish)',
        'cert_lang': 'Finnish or Swedish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The death is registered with the Digital and Population Data Services "
            "Agency (DVV). Police take jurisdiction for violent or unexplained "
            "deaths. Finland is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Finland is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'norway': {
        'name': 'Norway',
        'emergency': '112 (police) / 113 (ambulance)',
        'registry': 'the Norwegian National Population Register (Folkeregisteret)',
        'cert_name': 'death certificate (in Norwegian)',
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
        'cremation': 'Cremation in Norway is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'sweden': {
        'name': 'Sweden',
        'emergency': '112',
        'registry': 'the Swedish Tax Agency (Skatteverket)',
        'cert_name': 'death certificate (in Swedish)',
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
        'cremation': 'Cremation in Sweden is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'south-africa': {
        'name': 'South Africa',
        'emergency': '10111 (police) / 10177 (ambulance)',
        'registry': 'the Department of Home Affairs',
        'cert_name': 'death certificate (in English or Afrikaans)',
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
            'Cremation in South Africa is widely available in major cities '
            'including Johannesburg, Cape Town, and Durban.'
        ),
        'postmortem_trigger': "Violent or unexplained deaths (magistrate's court)",
    },
    'eritrea': {
        'name': 'Eritrea',
        'emergency': '122 (police) / 123 (ambulance)',
        'registry': 'the civil registration authority (limited capacity)',
        'cert_name': 'death certificate (in Tigrinya or Arabic)',
        'cert_lang': 'Tigrinya or Arabic',
        'overview': (
            "Call 122 for police or 123 for ambulance. Civil registration capacity "
            "is limited across Eritrea. The FCDO advises against all travel to "
            "Eritrea and consular access is restricted. Families should contact "
            "the nearest operational embassy immediately. All documentation is "
            "in Tigrinya or Arabic and requires certified translation."
        ),
        'doc_time': '2-6 weeks (highly variable)',
        'timeline_avg': '6-12 weeks',
        'timeline_fast': '3-6 weeks',
        'timeline_complex': 'Several months or longer',
        'complexity': 'high',
        'cremation': 'Cremation is not widely available in Eritrea.',
        'postmortem_trigger': (
            'Violent or unexplained deaths; security and access limitations '
            'may compound delays'
        ),
    },
    'netherlands': {
        'name': 'the Netherlands',
        'emergency': '112',
        'registry': 'the gemeente (municipality) civil registry',
        'cert_name': 'akte van overlijden (death certificate, in Dutch)',
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
        'cremation': 'Cremation in the Netherlands is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (Officier van Justitie)',
    },
    'south-korea': {
        'name': 'South Korea',
        'emergency': '112 (police) / 119 (ambulance)',
        'registry': 'the local gu office (ward office)',
        'cert_name': 'death certificate (in Korean)',
        'cert_lang': 'Korean',
        'overview': (
            "Call 112 for police or 119 for ambulance. Death is certified by a "
            "physician. The death is registered with the local gu office (ward "
            "office), which issues the Korean death certificate. A jang-ui-hwakinjung "
            "(burial or cremation certificate) is required before final disposition. "
            "Police take jurisdiction for violent or unexplained deaths. South Korea "
            "is not a Hague Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation is widely used in South Korea.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'new-zealand': {
        'name': 'New Zealand',
        'emergency': '111',
        'registry': 'Births, Deaths and Marriages New Zealand (BDM)',
        'cert_name': 'death certificate (in English)',
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
        'timeline_complex': '3-6 weeks (longer if Coroner involved)',
        'complexity': 'low',
        'cremation': 'Cremation in New Zealand is widely available.',
        'postmortem_trigger': 'Sudden, unexpected, or unnatural deaths (Coroner takes jurisdiction)',
    },
    'portugal': {
        'name': 'Portugal',
        'emergency': '112',
        'registry': 'the Conservatoria do Registo Civil (civil registry)',
        'cert_name': 'certidao de obito (death certificate, in Portuguese)',
        'cert_lang': 'Portuguese',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The certidao de obito is registered with the Conservatoria do Registo "
            "Civil. The Ministerio Publico (public prosecutor) takes jurisdiction "
            "for violent or unexplained deaths. Portugal is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Portugal is available and increasingly used.',
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico)',
    },
    'switzerland': {
        'name': 'Switzerland',
        'emergency': '117 (police) / 144 (ambulance)',
        'registry': 'the Zivilstandsamt (civil registry office)',
        'cert_name': 'Todesschein (death certificate, in German, French, or Italian)',
        'cert_lang': 'German, French, or Italian (depending on canton)',
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
        'cremation': 'Cremation in Switzerland is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft)',
    },
    'belgium': {
        'name': 'Belgium',
        'emergency': '112 (ambulance) / 101 (police)',
        'registry': 'the commune (local authority) civil registry',
        'cert_name': 'acte de deces (death certificate, in French, Dutch, or German)',
        'cert_lang': 'French, Dutch, or German (depending on region)',
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
        'cremation': 'Cremation in Belgium is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (Parquet)',
    },
    'poland': {
        'name': 'Poland',
        'emergency': '112',
        'registry': 'the Urzad Stanu Cywilnego (USC, civil status office)',
        'cert_name': 'akt zgonu (death certificate, in Polish)',
        'cert_lang': 'Polish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The akt zgonu is registered with the local Urzad Stanu Cywilnego "
            "(USC). Police and the Prokuratura (public prosecutor) take jurisdiction "
            "for violent or unexplained deaths. Poland is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Poland is available in major cities.',
        'postmortem_trigger': 'Violent or unexplained deaths (Prokuratura)',
    },
    'greece': {
        'name': 'Greece',
        'emergency': '100 (police) / 166 (ambulance)',
        'registry': 'the local civil registry (Lixiarcheio)',
        'cert_name': 'death certificate (in Greek)',
        'cert_lang': 'Greek',
        'overview': (
            "Call 100 for police or 166 for ambulance. Death is certified by a "
            "physician. The death is registered with the local Lixiarcheio (civil "
            "registry). Police and the Eisangelia (public prosecutor's office) "
            "take jurisdiction for violent or unexplained deaths. Greece is an EU "
            "member and Hague Apostille Convention member. On islands, ferry or "
            "light aircraft transfer to the mainland may be needed before "
            "international cargo arrangements can begin."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '2-6 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation became legal in Greece in 2006. Facilities are limited; '
            'the nearest crematoria are in Athens. Most families opt for full '
            'body repatriation.'
        ),
        'postmortem_trigger': "Violent or unexplained deaths (Eisangelia)",
    },
    'kenya': {
        'name': 'Kenya',
        'emergency': '999 (police and ambulance)',
        'registry': 'the Civil Registration Department',
        'cert_name': 'death certificate (in English)',
        'cert_lang': 'English',
        'overview': (
            "Call 999 for emergency services. Death is certified by a registered "
            "medical practitioner. The death is registered with the Civil "
            "Registration Department. Police take jurisdiction for violent or "
            "unexplained deaths. Kenya's tropical climate requires urgent embalming."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Kenya is available in Nairobi and some major cities, '
            'though burial remains more common.'
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
    'ethiopia': {
        'name': 'Ethiopia',
        'emergency': '911',
        'registry': 'VERA, the civil events registration authority',
        'cert_name': 'death certificate (in Amharic)',
        'cert_lang': 'Amharic',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician "
            "or health officer and registered with VERA, Ethiopia's civil events "
            "registration authority. Police take jurisdiction for violent or "
            "unexplained deaths. Documentation is in Amharic and requires "
            "certified translation."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is limited in Ethiopia and not widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'ghana': {
        'name': 'Ghana',
        'emergency': '191 (police) / 193 (fire and ambulance)',
        'registry': 'the Births and Deaths Registry (Ghana Statistical Service)',
        'cert_name': 'death certificate (in English)',
        'cert_lang': 'English',
        'overview': (
            "Call 191 for police or 193 for fire and ambulance. Death is certified "
            "by a medical practitioner and registered with the Births and Deaths "
            "Registry under the Ghana Statistical Service. Police take jurisdiction "
            "for violent or unexplained deaths. Ghana's tropical climate requires "
            "prompt embalming."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Ghana is available in Accra and some major cities, '
            'though burial remains more common.'
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
    'nigeria': {
        'name': 'Nigeria',
        'emergency': '112 / 199 (police)',
        'registry': 'the National Population Commission (NPC)',
        'cert_name': 'death certificate (in English)',
        'cert_lang': 'English',
        'overview': (
            "Call 112 or 199 for emergency services. Death is certified by a "
            "registered medical practitioner. Death registration is handled by "
            "the National Population Commission (NPC). Police take jurisdiction "
            "for violent or unexplained deaths. Access to civil registration "
            "services varies considerably between Lagos and rural states. "
            "Nigeria's tropical climate requires urgent embalming."
        ),
        'doc_time': '7-21 days; longer in more remote states',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Nigeria is available in Lagos and Abuja, though burial '
            'is the predominant practice across most communities.'
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
    'jordan': {
        'name': 'Jordan',
        'emergency': '911 (police) / 912 (ambulance)',
        'registry': 'the Civil Status and Passports Department',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 911 for police or 912 for ambulance. Death is certified by a "
            "physician and registered with the Civil Status and Passports "
            "Department. The public prosecutor takes jurisdiction for violent or "
            "unexplained deaths. All documentation is in Arabic and requires "
            "certified translation. Jordan's climate requires prompt embalming."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Jordan.',
        'postmortem_trigger': 'Violent or unexplained deaths (public prosecutor)',
    },
    'senegal': {
        'name': 'Senegal',
        'emergency': '17 (police) / 15 (ambulance)',
        'registry': 'the local Centre d\'etat civil',
        'cert_name': 'acte de deces (death certificate, in French)',
        'cert_lang': 'French',
        'overview': (
            "Call 17 for police or 15 for ambulance. Death is certified by a "
            "physician. The acte de deces is registered with the local Centre "
            "d'etat civil. Police take jurisdiction for violent or unexplained "
            "deaths. Documentation is in French and requires certified translation."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not widely available in Senegal. Most families opt for full body repatriation.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'cameroon': {
        'name': 'Cameroon',
        'emergency': '117 (police) / 15 (ambulance)',
        'registry': 'the local Centre d\'etat civil',
        'cert_name': 'acte de deces (death certificate, in French)',
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
        'cremation': 'Cremation is not widely available in Cameroon. Most families opt for full body repatriation.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'afghanistan': {
        'name': 'Afghanistan',
        'emergency': '119 (police) (severely limited)',
        'registry': 'the relevant local authority (civil registry capacity is very limited)',
        'cert_name': 'death certificate (in Dari or Pashto)',
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
    'djibouti': {
        'name': 'Djibouti',
        'emergency': '17 (police) / 15 (ambulance)',
        'registry': 'the local etat civil (civil registry)',
        'cert_name': 'acte de deces (death certificate, in French or Arabic)',
        'cert_lang': 'French or Arabic',
        'overview': (
            "Call 17 for police or 15 for ambulance. Death is certified by a "
            "physician. The acte de deces is registered with the local etat "
            "civil. Police take jurisdiction for violent or unexplained deaths. "
            "Djibouti's climate requires prompt embalming. Documentation is in "
            "French or Arabic."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not widely available in Djibouti. Most families opt for full body repatriation.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
}

ROUTES = [
    # R55 -- Bahrain wave 5
    {
        'origin': 'malaysia', 'dest': 'bahrain',
        'embassy_city': 'Kuala Lumpur',
        'intro': (
            "Malaysian nationals in Bahrain include professionals in construction, "
            "engineering, and the hospitality sector. Malaysia and Bahrain maintain "
            "bilateral relations within the Organisation of Islamic Cooperation (OIC). "
            "Malaysian death certificates (sijil kematian, in Bahasa Malaysia) require "
            "certified Arabic translation for the Civil Status and Passports Affairs "
            "Authority (CSPA) and authentication by the Bahraini Embassy in Kuala "
            "Lumpur. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'myanmar', 'dest': 'bahrain',
        'embassy_city': 'Bangkok',
        'intro': (
            "Myanmar nationals in Bahrain include domestic workers and workers in "
            "construction and hospitality. Myanmar's labour migration to the Gulf "
            "has grown through government bilateral labour frameworks. Myanmar death "
            "certificates (in Burmese) require certified Arabic translation for the "
            "Civil Status and Passports Affairs Authority (CSPA). Bahrain does not "
            "maintain a resident Embassy in Myanmar; consular matters are covered by "
            "the Bahraini Embassy in Bangkok, Thailand. Families should contact the "
            "Bahraini Embassy in Bangkok as a first step. Families should also be "
            "aware that the FCDO advises against travel to Myanmar. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'cambodia', 'dest': 'bahrain',
        'embassy_city': 'Bangkok',
        'intro': (
            "Cambodian nationals in Bahrain include domestic workers and workers in "
            "the hospitality sector, reflecting Cambodia's growing Gulf labour "
            "migration under bilateral labour frameworks. Cambodian death certificates "
            "(in Khmer) require certified Arabic translation for the Civil Status and "
            "Passports Affairs Authority (CSPA). Bahrain does not maintain a resident "
            "Embassy in Cambodia; consular matters are covered by the Bahraini Embassy "
            "in Bangkok, Thailand. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'china', 'dest': 'bahrain',
        'embassy_city': 'Beijing',
        'intro': (
            "Chinese nationals in Bahrain include professionals and workers in "
            "construction and infrastructure projects, reflecting growing bilateral "
            "economic ties. Bahrain and China have strengthened investment and trade "
            "links in recent years. Mandarin-language Chinese death certificates "
            "(si wang zheng ming shu) require certified Arabic translation for the "
            "Civil Status and Passports Affairs Authority (CSPA) and authentication "
            "by the Bahraini Embassy in Beijing. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'uzbekistan', 'dest': 'bahrain',
        'embassy_city': 'Riyadh',
        'intro': (
            "Uzbek nationals in Bahrain include workers in construction and technical "
            "sectors, reflecting Central Asian labour migration to the Gulf. "
            "Uzbekistan and Bahrain have maintained diplomatic relations within Gulf "
            "cooperation frameworks. Uzbek documentation (in Uzbek or Russian) "
            "requires certified Arabic translation for the Civil Status and Passports "
            "Affairs Authority (CSPA). Bahrain does not maintain a resident Embassy "
            "in Uzbekistan; families should contact the Bahraini Embassy in Riyadh, "
            "which covers consular matters for Central Asia, to verify current "
            "arrangements. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R55 -- South Korea wave 5
    {
        'origin': 'japan', 'dest': 'south-korea',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japanese nationals in South Korea include a well-established community "
            "of business professionals, students, and long-term residents, reflecting "
            "the close but historically complex bilateral relationship between the two "
            "countries. Japan and South Korea have significant economic and "
            "people-to-people ties. Japanese death certificates (shibo todoke) are "
            "in Japanese and require certified Korean translation and authentication "
            "through the South Korean Embassy in Tokyo. South Korea is not a Hague "
            "Apostille Convention member; consular authentication is required for "
            "all documentation. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'hong-kong', 'dest': 'south-korea',
        'embassy_city': 'Hong Kong',
        'intro': (
            "Hong Kong residents in South Korea include business professionals and "
            "students, reflecting significant trade and financial ties between the "
            "two places. Hong Kong functions as a major regional financial hub with "
            "close economic links to South Korea. Hong Kong death certificates are "
            "issued in English and Chinese by the Registry of Births and Deaths. "
            "The South Korean Consulate-General in Hong Kong handles consular "
            "matters. All documents require authentication through the South Korean "
            "Consulate-General, as South Korea is not a Hague Apostille Convention "
            "member. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'turkey', 'dest': 'south-korea',
        'embassy_city': 'Ankara',
        'intro': (
            "Turkish nationals in South Korea include students, professionals, and "
            "a small but established community. Turkey and South Korea have "
            "maintained bilateral ties since the Korean War, in which Turkey "
            "contributed troops under the United Nations Command, a bond that "
            "continues to underpin diplomatic relations. Turkish death certificates "
            "(olum belgesi, in Turkish) require certified Korean translation and "
            "authentication through the South Korean Embassy in Ankara before the "
            "gu office (ward office) can register the death. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'egypt', 'dest': 'south-korea',
        'embassy_city': 'Cairo',
        'intro': (
            "Egyptian nationals in South Korea include students and professionals "
            "on academic and business exchange programmes. Egypt and South Korea "
            "have maintained bilateral diplomatic relations and economic ties. "
            "Arabic-language Egyptian death certificates require certified Korean "
            "translation and authentication through the South Korean Embassy in "
            "Cairo before the gu office (ward office) can register the death. "
            "South Korea is not a Hague Apostille Convention member; full consular "
            "authentication is required. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sri-lanka', 'dest': 'south-korea',
        'embassy_city': 'Colombo',
        'intro': (
            "Sri Lankan nationals in South Korea include workers under the Employment "
            "Permit System (EPS) and students. Sri Lanka has been a participant "
            "country in South Korea's EPS scheme, with Sri Lankan workers in "
            "manufacturing and technical sectors. Sri Lankan death certificates, "
            "issued by the Registrar General's Department in Sinhala and English, "
            "require certified Korean translation and authentication through the "
            "South Korean Embassy in Colombo. South Korea is not a Hague Apostille "
            "Convention member. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R55 -- Japan wave 10
    {
        'origin': 'austria', 'dest': 'japan',
        'embassy_city': 'Vienna',
        'intro': (
            "Austrian nationals in Japan include professionals, students, and a "
            "community with Japan connections through business and cultural exchange. "
            "Austria and Japan have maintained bilateral diplomatic relations and "
            "close ties through the EU-Japan Economic Partnership Agreement (JEEPA, "
            "2019). Austrian death certificates (Sterbeurkunde, in German) require "
            "certified Japanese translation and authentication through the Japanese "
            "Embassy in Vienna. Both Austria and Japan are Hague Apostille Convention "
            "members, which simplifies document authentication. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'denmark', 'dest': 'japan',
        'embassy_city': 'Copenhagen',
        'intro': (
            "Danish nationals in Japan include professionals, students, and a "
            "community with Japan connections through business and cultural exchange. "
            "Denmark and Japan maintain bilateral diplomatic relations, and Denmark "
            "benefits from the EU-Japan Economic Partnership Agreement (JEEPA, "
            "2019) as an EU member. Danish death certificates (in Danish) require "
            "certified Japanese translation and authentication through the Japanese "
            "Embassy in Copenhagen. Both Denmark and Japan are Hague Apostille "
            "Convention members. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'finland', 'dest': 'japan',
        'embassy_city': 'Helsinki',
        'intro': (
            "Finnish nationals in Japan include professionals, students, and a "
            "community with Japan connections through technology, design, and "
            "business. Finland and Japan maintain bilateral diplomatic relations, "
            "and Finland benefits from the EU-Japan Economic Partnership Agreement "
            "(JEEPA, 2019). Finnish death certificates (in Finnish or Swedish) "
            "require certified Japanese translation and authentication through the "
            "Japanese Embassy in Helsinki. Both Finland and Japan are Hague "
            "Apostille Convention members. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'japan',
        'embassy_city': 'Oslo',
        'intro': (
            "Norwegian nationals in Japan include professionals in energy, shipping, "
            "and maritime industries, and a small community of long-term residents. "
            "Norway and Japan maintain bilateral diplomatic relations, with the "
            "Norwegian Embassy in Tokyo and the Japanese Embassy in Oslo both "
            "operational. Norwegian death certificates (in Norwegian) require "
            "certified Japanese translation and authentication through the Japanese "
            "Embassy in Oslo. Both Norway and Japan are Hague Apostille Convention "
            "members. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'japan',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in Japan include professionals, students, and a "
            "community with close cultural and business connections. Sweden and Japan "
            "have maintained bilateral diplomatic relations since 1868. Swedish death "
            "certificates (in Swedish) require certified Japanese translation and "
            "authentication through the Japanese Embassy in Stockholm. Both Sweden "
            "and Japan are Hague Apostille Convention members, which simplifies "
            "document authentication. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R55 -- Oman wave 7
    {
        'origin': 'south-africa', 'dest': 'oman',
        'embassy_city': 'Pretoria',
        'intro': (
            "South African nationals in Oman include professionals in oil and gas, "
            "engineering, and construction, and a growing community of residents "
            "reflecting Gulf recruitment of Southern African technical specialists. "
            "South Africa and Oman maintain bilateral diplomatic relations and the "
            "Omani Embassy in Pretoria handles consular matters. South African death "
            "certificates (in English or Afrikaans) require certified Arabic "
            "translation for the Royal Oman Police civil registration section. "
            "South Africa is a Hague Apostille member; authentication through the "
            "Omani Embassy in Pretoria is still required. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'eritrea', 'dest': 'oman',
        'embassy_city': 'Asmara',
        'intro': (
            "Eritrean nationals in Oman include workers in construction and "
            "domestic service sectors. Eritrea and Oman maintain diplomatic "
            "relations and the Omani Embassy in Asmara handles consular matters. "
            "Families should be aware that the FCDO advises against all travel "
            "to Eritrea and that civil registration capacity is limited. "
            "Documentation in Tigrinya or Arabic requires certified Arabic "
            "translation for the Royal Oman Police civil registration section. "
            "Contact the Omani Embassy in Asmara at the earliest opportunity. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'laos', 'dest': 'oman',
        'embassy_city': 'Bangkok',
        'intro': (
            "Lao nationals in Oman include workers in construction and hospitality, "
            "reflecting Laos's growing participation in Gulf labour migration. Oman "
            "does not maintain a resident Embassy in Laos; consular matters are "
            "covered by the Omani Embassy in Bangkok, Thailand. Lao-language "
            "documentation requires certified Arabic translation for the Royal Oman "
            "Police civil registration section. Families should contact the Omani "
            "Embassy in Bangkok as a first step. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'myanmar', 'dest': 'oman',
        'embassy_city': 'Yangon',
        'intro': (
            "Myanmar nationals in Oman include domestic workers and workers in "
            "construction, reflecting Myanmar's labour migration to the Gulf. "
            "The Omani Embassy in Yangon handles consular matters for Myanmar. "
            "Myanmar death certificates (in Burmese) require certified Arabic "
            "translation for the Royal Oman Police civil registration section. "
            "Families should be aware that the FCDO advises against all travel "
            "to Myanmar and that consular access may be limited given the "
            "current situation. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-korea', 'dest': 'oman',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korean nationals in Oman include engineers and construction "
            "professionals involved in major infrastructure projects, reflecting "
            "South Korea's significant presence in Gulf construction through "
            "firms including Hyundai Engineering and Construction. South Korea "
            "and Oman have maintained strong bilateral economic ties through "
            "energy cooperation agreements. The Omani Embassy in Seoul handles "
            "consular matters. South Korean death certificates require certified "
            "Arabic translation for the Royal Oman Police civil registration "
            "section. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R55 -- Indonesia NEW HUB wave 1
    {
        'origin': 'india', 'dest': 'indonesia',
        'embassy_city': 'New Delhi',
        'intro': (
            "Indian nationals in Indonesia include business professionals in trade, "
            "manufacturing, and the financial sector, and a community with historical "
            "links through Indian Ocean trade routes. India and Indonesia have a "
            "bilateral Strategic Partnership and strong economic ties reinforced "
            "through ASEAN-India cooperation frameworks. Indian death certificates "
            "require certified Indonesian translation for the Disdukcapil "
            "(Dinas Kependudukan dan Pencatatan Sipil) and authentication by the "
            "Indonesian Embassy in New Delhi. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'malaysia', 'dest': 'indonesia',
        'embassy_city': 'Kuala Lumpur',
        'intro': (
            "Malaysian nationals in Indonesia include a significant community of "
            "workers, students, and residents reflecting the close cultural, "
            "linguistic, and historical ties between the two countries. Malaysia "
            "and Indonesia share closely related national languages and bilateral "
            "migration is substantial within the ASEAN framework. Malaysian death "
            "certificates (sijil kematian, in Bahasa Malaysia) require certified "
            "Indonesian translation for the Disdukcapil and authentication by the "
            "Indonesian Embassy in Kuala Lumpur. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'indonesia',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in Indonesia include business professionals, "
            "development workers, and expatriates with deep historical ties "
            "reflecting the centuries-long Netherlands-Indonesia relationship. "
            "The Netherlands and Indonesia have strong bilateral diplomatic and "
            "economic ties. Dutch death certificates (akte van overlijden, in "
            "Dutch) require certified Indonesian translation for the Disdukcapil "
            "and authentication by the Indonesian Embassy in The Hague. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'china', 'dest': 'indonesia',
        'embassy_city': 'Beijing',
        'intro': (
            "Chinese nationals in Indonesia include a long-established ethnic "
            "Chinese-Indonesian community and business professionals in investment "
            "and infrastructure projects. China is one of Indonesia's largest "
            "trade and investment partners, with ties deepened through bilateral "
            "cooperation frameworks. Mandarin-language Chinese death certificates "
            "(si wang zheng ming shu) require certified Indonesian translation "
            "for the Disdukcapil and authentication by the Indonesian Embassy "
            "in Beijing. (Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'indonesia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Indonesia include tourists, expatriates "
            "working in resources and energy, and a community with significant "
            "ties reflecting Australia's close neighbour relationship. Australians "
            "constitute one of the largest groups of foreign visitors in Bali, "
            "with a high volume of arrivals through Ngurah Rai International "
            "Airport (DPS). Australian death certificates (in English) require "
            "certified Indonesian translation for the Disdukcapil and "
            "authentication by the Indonesian Embassy in Canberra. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R56 -- Indonesia wave 2
    {
        'origin': 'singapore', 'dest': 'indonesia',
        'embassy_city': 'Singapore',
        'intro': (
            "Singaporean nationals in Indonesia include business professionals and "
            "investors reflecting the substantial Singapore-Indonesia economic "
            "relationship. Singapore is among the largest foreign investors in "
            "Indonesia and the two countries operate the Batam-Bintan-Karimun "
            "Special Economic Zone framework. Singapore death certificates (in "
            "English) require certified Indonesian translation for the Disdukcapil "
            "and authentication by the Indonesian Embassy in Singapore. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'indonesia',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japanese nationals in Indonesia include a large and long-established "
            "community of business professionals and manufacturing executives, "
            "reflecting Japan's significant investment in Indonesian industry. "
            "Japan and Indonesia have a bilateral Economic Partnership Agreement "
            "(JIEPA, 2008) and Japan is one of Indonesia's largest investors. "
            "Japanese death certificates (shibo todoke, in Japanese) require "
            "certified Indonesian translation for the Disdukcapil and "
            "authentication by the Indonesian Embassy in Tokyo. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'indonesia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Indonesia include business professionals, "
            "development workers, and expatriates in manufacturing and engineering. "
            "Germany and Indonesia have bilateral economic ties and the German "
            "Embassy in Jakarta maintains an active presence. German death "
            "certificates (Sterbeurkunde, in German) require certified Indonesian "
            "translation for the Disdukcapil and authentication by the Indonesian "
            "Embassy in Berlin. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'usa', 'dest': 'indonesia',
        'embassy_city': 'Washington D.C.',
        'intro': (
            "American nationals in Indonesia include business professionals in "
            "energy, mining, and technology, expatriates, and tourists across "
            "Indonesia's many islands, particularly Bali. The United States and "
            "Indonesia maintain a bilateral Strategic Partnership and close "
            "investment ties. American death certificates, issued by the state "
            "civil records office, require certified Indonesian translation for "
            "the Disdukcapil and authentication by the Indonesian Embassy in "
            "Washington D.C. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'south-korea', 'dest': 'indonesia',
        'embassy_city': 'Seoul',
        'intro': (
            "South Korean nationals in Indonesia include business professionals, "
            "manufacturing executives, and a growing community reflecting South "
            "Korea's significant investment in Indonesian manufacturing and "
            "infrastructure through a bilateral Economic Partnership Agreement. "
            "South Korean death certificates (in Korean) require certified "
            "Indonesian translation for the Disdukcapil and authentication by "
            "the Indonesian Embassy in Seoul. "
            "(Indonesian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R56 -- Bahrain wave 6
    {
        'origin': 'laos', 'dest': 'bahrain',
        'embassy_city': 'Bangkok',
        'intro': (
            "Lao nationals in Bahrain include workers in construction and "
            "hospitality, reflecting Laos's growing participation in Gulf labour "
            "migration. Lao-language documentation requires certified Arabic "
            "translation for the Civil Status and Passports Affairs Authority "
            "(CSPA). Bahrain does not maintain a resident Embassy in Laos; "
            "consular matters are covered by the Bahraini Embassy in Bangkok, "
            "Thailand. Families should contact the Bahraini Embassy in Bangkok "
            "as a first step. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'russia', 'dest': 'bahrain',
        'embassy_city': 'Moscow',
        'intro': (
            "Russian nationals in Bahrain include tourists, business professionals, "
            "and a growing community of residents. Bahrain maintained a neutral "
            "diplomatic position following 2022 and the Bahraini Embassy in "
            "Moscow remains operational. Russian death certificates (svidetelstvo "
            "o smerti, in Russian) require certified Arabic translation for the "
            "Civil Status and Passports Affairs Authority (CSPA) and "
            "authentication by the Bahraini Embassy in Moscow. Families should "
            "be aware of the FCDO's advice against travel to Russia. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'senegal', 'dest': 'bahrain',
        'embassy_city': 'Paris',
        'intro': (
            "Senegalese nationals in Bahrain include domestic workers and workers "
            "in the service sector, reflecting West African labour migration to "
            "the Gulf. Senegal and Bahrain maintain ties within the Organisation "
            "of Islamic Cooperation (OIC). French-language Senegalese death "
            "certificates require certified Arabic translation for the Civil "
            "Status and Passports Affairs Authority (CSPA). Bahrain does not "
            "maintain a resident Embassy in Senegal; consular matters for "
            "Senegal are covered by the Bahraini Embassy in Paris. Families "
            "should contact the Bahraini Embassy in Paris to initiate "
            "documentation. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'cameroon', 'dest': 'bahrain',
        'embassy_city': 'Paris',
        'intro': (
            "Cameroonian nationals in Bahrain include domestic workers and "
            "workers in construction and the service sector. Cameroon and "
            "Bahrain maintain diplomatic ties within the Organisation of "
            "Islamic Cooperation (OIC). French-language Cameroonian death "
            "certificates require certified Arabic translation for the Civil "
            "Status and Passports Affairs Authority (CSPA). Bahrain does not "
            "maintain a resident Embassy in Cameroon; consular matters are "
            "covered by the Bahraini Embassy in Paris. Families should contact "
            "the Bahraini Embassy in Paris to initiate documentation. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'afghanistan', 'dest': 'bahrain',
        'embassy_city': 'Islamabad',
        'intro': (
            "Afghan nationals requiring repatriation to Bahrain face significant "
            "consular complexity. The FCDO advises against all travel to "
            "Afghanistan and consular access has been severely curtailed since "
            "August 2021. The Bahraini Embassy in Islamabad covers consular "
            "matters for Afghanistan. All documentation in Dari or Pashto "
            "requires certified Arabic translation for the Civil Status and "
            "Passports Affairs Authority (CSPA). Families should contact the "
            "Bahraini Embassy in Islamabad as early as possible. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R56 -- Japan wave 11
    {
        'origin': 'portugal', 'dest': 'japan',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portuguese nationals in Japan include professionals, students, and "
            "a community with cultural and historical connections. Portugal and "
            "Japan have maintained bilateral diplomatic relations since the 16th "
            "century, one of the longest bilateral ties Japan holds with a "
            "European nation. Portuguese death certificates (certidao de obito, "
            "in Portuguese) require certified Japanese translation and "
            "authentication through the Japanese Embassy in Lisbon. Both "
            "Portugal and Japan are Hague Apostille Convention members, which "
            "simplifies the authentication process. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'japan',
        'embassy_city': 'Bern',
        'intro': (
            "Swiss nationals in Japan include professionals in finance, "
            "pharmaceuticals, and business, and a long-established community "
            "with bilateral ties through investment and cultural exchange. "
            "Switzerland and Japan have a bilateral Free Trade Agreement "
            "(EFTA-Japan EPA, 2009). Swiss death certificates (Todesschein, "
            "in German, French, or Italian depending on the canton) require "
            "certified Japanese translation and authentication through the "
            "Japanese Embassy in Bern. Both Switzerland and Japan are Hague "
            "Apostille Convention members. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'japan',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgian nationals in Japan include professionals, students, and "
            "a community with Belgium-Japan ties through business and diplomacy. "
            "Belgium and Japan have maintained bilateral diplomatic relations "
            "since 1866, and Belgium benefits from the EU-Japan Economic "
            "Partnership Agreement (JEEPA, 2019) as an EU member. Belgian "
            "death certificates (acte de deces or akte van overlijden, in "
            "French or Dutch depending on the region) require certified Japanese "
            "translation and authentication through the Japanese Embassy in "
            "Brussels. Both Belgium and Japan are Hague Apostille Convention "
            "members. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'poland', 'dest': 'japan',
        'embassy_city': 'Warsaw',
        'intro': (
            "Polish nationals in Japan include students, professionals, and a "
            "growing community with Japan connections through cultural exchange "
            "and business. Poland and Japan have maintained bilateral diplomatic "
            "relations and Poland benefits from the EU-Japan Economic Partnership "
            "Agreement (JEEPA, 2019). Polish death certificates (akt zgonu, in "
            "Polish) require certified Japanese translation and authentication "
            "through the Japanese Embassy in Warsaw. Both Poland and Japan are "
            "Hague Apostille Convention members. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'greece', 'dest': 'japan',
        'embassy_city': 'Athens',
        'intro': (
            "Greek nationals in Japan include students, professionals, and a "
            "small community of long-term residents. Greece and Japan have "
            "maintained bilateral diplomatic relations, and Greece benefits from "
            "the EU-Japan Economic Partnership Agreement (JEEPA, 2019) as an "
            "EU member. Greek death certificates (in Greek) require certified "
            "Japanese translation and authentication through the Japanese Embassy "
            "in Athens. Both Greece and Japan are Hague Apostille Convention "
            "members. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R56 -- South Korea wave 6
    {
        'origin': 'ghana', 'dest': 'south-korea',
        'embassy_city': 'Accra',
        'intro': (
            "Ghanaian nationals in South Korea include students, professionals, "
            "and a growing community of residents. Ghana and South Korea have "
            "maintained bilateral ties through development assistance and trade "
            "cooperation within Africa-Korea economic frameworks. English-language "
            "Ghanaian death certificates require certified Korean translation and "
            "authentication through the South Korean Embassy in Accra before the "
            "gu office (ward office) can register the death. South Korea is not "
            "a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'nigeria', 'dest': 'south-korea',
        'embassy_city': 'Abuja',
        'intro': (
            "Nigerian nationals in South Korea include students, professionals, "
            "and a community of long-term residents. Nigeria and South Korea have "
            "maintained bilateral diplomatic ties and economic cooperation within "
            "Africa-Korea engagement frameworks. English-language Nigerian death "
            "certificates require certified Korean translation and authentication "
            "through the South Korean Embassy in Abuja before the gu office "
            "(ward office) can register the death. South Korea is not a Hague "
            "Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'kenya', 'dest': 'south-korea',
        'embassy_city': 'Nairobi',
        'intro': (
            "Kenyan nationals in South Korea include students, academics, and "
            "professionals on bilateral exchange and development cooperation "
            "programmes. Kenya and South Korea have maintained ties through the "
            "Africa-Korea Forum and development cooperation agreements. "
            "English-language Kenyan death certificates require certified Korean "
            "translation and authentication through the South Korean Embassy in "
            "Nairobi before the gu office (ward office) can register the death. "
            "South Korea is not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ethiopia', 'dest': 'south-korea',
        'embassy_city': 'Addis Ababa',
        'intro': (
            "Ethiopian nationals in South Korea include students and professionals "
            "on academic and development exchange programmes. Ethiopia and South "
            "Korea have maintained bilateral ties through South Korea's Official "
            "Development Assistance (ODA) programmes and the Korea-Ethiopia "
            "bilateral cooperation framework. Documentation from VERA, Ethiopia's "
            "civil events registration authority, is in Amharic and requires "
            "certified Korean translation and authentication through the South "
            "Korean Embassy in Addis Ababa. South Korea is not a Hague Apostille "
            "Convention member. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'jordan', 'dest': 'south-korea',
        'embassy_city': 'Amman',
        'intro': (
            "Jordanian nationals in South Korea include students, academics, "
            "and professionals on bilateral exchange programmes. Jordan and "
            "South Korea have maintained diplomatic relations and South Korea "
            "has provided development assistance to Jordan. Arabic-language "
            "Jordanian death certificates require certified Korean translation "
            "and authentication through the South Korean Embassy in Amman "
            "before the gu office (ward office) can register the death. South "
            "Korea is not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R56 -- Oman wave 8
    {
        'origin': 'bahrain', 'dest': 'oman',
        'embassy_city': 'Manama',
        'intro': (
            "Bahraini nationals in Oman include business professionals, tourists, "
            "and residents with close Gulf Cooperation Council connections. Bahrain "
            "and Oman are both GCC member states, and movement between the two "
            "countries is well-established for GCC nationals. Arabic-language "
            "Bahraini death certificates are accepted by the Royal Oman Police "
            "civil registration section without translation, though authentication "
            "by the Omani Embassy in Manama is still required before registration "
            "can proceed. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'kuwait', 'dest': 'oman',
        'embassy_city': 'Kuwait City',
        'intro': (
            "Kuwaiti nationals in Oman include business professionals, tourists, "
            "and residents with close Gulf Cooperation Council connections. Kuwait "
            "and Oman are both GCC member states, and movement between the two "
            "countries is straightforward for GCC nationals. Arabic-language "
            "Kuwaiti death certificates are accepted by the Royal Oman Police "
            "civil registration section without translation, though authentication "
            "by the Omani Embassy in Kuwait City is still required before "
            "registration proceeds. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'qatar', 'dest': 'oman',
        'embassy_city': 'Doha',
        'intro': (
            "Qatari nationals in Oman include business professionals, tourists, "
            "and residents with close Gulf Cooperation Council ties. Qatar and "
            "Oman are both GCC member states and normal diplomatic relations were "
            "fully restored through the Al-Ula Declaration in January 2021. "
            "Arabic-language Qatari death certificates are accepted by the Royal "
            "Oman Police civil registration section without translation, though "
            "authentication by the Omani Embassy in Doha is still required. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'new-zealand', 'dest': 'oman',
        'embassy_city': 'Canberra',
        'intro': (
            "New Zealand nationals in Oman include professionals in oil and gas, "
            "engineering, and construction, reflecting New Zealand's participation "
            "in Gulf technical recruitment. New Zealand and Oman maintain bilateral "
            "diplomatic relations. The Omani Embassy in Canberra handles consular "
            "matters for New Zealand. New Zealand death certificates (in English) "
            "require certified Arabic translation for the Royal Oman Police civil "
            "registration section. New Zealand is a Hague Apostille member; "
            "authentication through the Omani Embassy in Canberra is still "
            "required regardless. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'djibouti', 'dest': 'oman',
        'embassy_city': 'Djibouti',
        'intro': (
            "Djiboutian nationals in Oman include workers and a small community "
            "with Horn of Africa connections in the Gulf. Djibouti and Oman "
            "maintain diplomatic relations within the Arab League framework. "
            "The Omani Embassy in Djibouti handles consular matters. French or "
            "Arabic-language Djiboutian documentation requires certified Arabic "
            "translation for the Royal Oman Police civil registration section "
            "where not already in Arabic. Families should contact the Omani "
            "Embassy in Djibouti as the first point of contact. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
]


def make_dest_key(dest_slug):
    keys = {
        'south-korea': 'kr', 'bahrain': 'bh', 'japan': 'jp',
        'oman': 'om', 'indonesia': 'id',
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
            print(f"ERROR em dash in {slug}")
            continue

        # QA: banned vocab check
        lower_content = content.lower()
        found_banned = [w for w in banned if w in lower_content]
        if found_banned:
            print(f"ERROR banned vocab in {slug}: {found_banned}")
            continue

        # QA: no price language
        price_patterns = [
            'prices start', 'from £', 'from $', 'cost from',
            'price from', 'prices from',
        ]
        if any(p in lower_content for p in price_patterns):
            print(f"ERROR price language in {slug}")
            continue

        # QA: no safety guarantees
        safety_patterns = ['guarantee', '100% safe', 'risk-free', 'risk free']
        if any(p in lower_content for p in safety_patterns):
            print(f"ERROR safety guarantee language in {slug}")
            continue

        with open(path, 'w') as f:
            f.write(content)

        print(f"CREATED ({variant}): {slug}")
        created.append((slug, variant))
        variant_idx += 1

    print(f"\nTotal created: {len(created)}")
    for s, v in created:
        print(f"  [{v}] {s}")


if __name__ == '__main__':
    main()
