#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R53-R54.

   R53 (25 routes, variants D,E,A,B,C x5):
     South Korea wave 3 x5: india, philippines, uzbekistan, australia, usa
     Bahrain wave 3 x5: jordan, iraq, iran, ghana, nigeria
     Japan wave 8 x5: singapore, canada, saudi-arabia, iraq, jordan
     New Zealand wave 6 x5: japan, thailand, singapore, ethiopia, ghana
     Oman wave 5 x5: ghana, somalia, uzbekistan, russia, saudi-arabia

   R54 (25 routes, variants D,E,A,B,C x5):
     South Korea wave 4 x5: iran, iraq, pakistan, malaysia, singapore
     Bahrain wave 4 x5: turkey, qatar, kuwait, oman, vietnam
     Japan wave 9 x5: oman, bahrain, kuwait, qatar, spain
     New Zealand wave 7 x5: iran, iraq, turkey, cambodia, laos
     Oman wave 6 x5: germany, france, australia, canada, usa

   Template rotation: R52 ended C (index 2). R53 starts D (index 3).
   Each block of 25 cycles D,E,A,B,C x5, ending on C. R54 starts D again.

   Embassy notes:
   - Bahrain-Iran: Bahrain severed ties with Iran in 2016; as of 2025
     families should verify current consular status with Bahrain MFA. Embassy
     city listed as Tehran; if suspended, contact Bahrain MFA directly.
   - NZ-Ethiopia: NZ has no resident embassy in Ethiopia; covered from Nairobi.
   - NZ-Ghana: NZ has no resident embassy in Ghana; covered from Abuja (Nigeria).
   - NZ-Laos: NZ has no resident embassy in Laos; covered from Bangkok.
   - NZ-Iraq: NZ maintains an Embassy in Baghdad.
   - Japan-Iraq: Japanese Embassy operates in Baghdad.
   - Japan-Bahrain: Japanese Embassy in Manama operational.
   - Japan-Kuwait: Japanese Embassy in Kuwait City operational.
   - Japan-Qatar: Japanese Embassy in Doha operational.
   - Oman-Somalia: Oman has an Embassy in Mogadishu.
   - SK-Iran: South Korean Embassy in Tehran operational.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 3  # D

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
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
        'emergency_line': 'contact Bahraini Embassy in origin country',
        'hub_url': 'repatriation-from-bahrain',
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
    'new-zealand': {
        'name': 'New Zealand',
        'slug': 'new-zealand',
        'key': 'nz',
        'reception': (
            "The New Zealand funeral director takes custody at Auckland (AKL), "
            "Wellington (WLG), or Christchurch (CHC) cargo terminal. Births, "
            "Deaths and Marriages New Zealand (BDM) registers the death. A "
            "burial or cremation certificate is required before final disposition. "
            "New Zealand is a Hague Apostille Convention member. Documents not in "
            "English require certified translation. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
        'consular_template': (
            "New Zealand Embassy or High Commission in {city} can advise on "
            "documentation requirements for repatriation to New Zealand. New "
            "Zealand Ministry of Foreign Affairs and Trade emergency line: "
            "+64 4 439 8000 (24 hours). The Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The New Zealand funeral director takes custody at Auckland (AKL), "
            "Wellington (WLG), or Christchurch (CHC) cargo terminal. BDM "
            "registers the death. A burial or cremation certificate is required "
            "before final disposition. New Zealand is a Hague Apostille member. "
            "Documents not in English require certified translation. The receiving "
            "funeral director coordinates with local authorities."
        ),
        'emergency_line': '+64 4 439 8000',
        'hub_url': 'repatriation-from-new-zealand',
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
        'emergency_line': 'contact Omani Embassy in origin country',
        'hub_url': 'repatriation-from-oman',
    },
}

# ---------------------------------------------------------------------------
# Origin country data
# ---------------------------------------------------------------------------

ORIGIN_DATA = {
    'india': {
        'name': 'India',
        'emergency': '112 (national emergency) / 100 (police) / 108 (ambulance)',
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
    'philippines': {
        'name': 'Philippines',
        'emergency': '911',
        'registry': 'the Local Civil Registrar',
        'cert_name': 'certificate of death (PSA-authenticated)',
        'cert_lang': 'English',
        'overview': (
            "Contact local emergency services (911). If death is unexpected, "
            "police must be notified. The certificate of death is issued by the "
            "attending physician and filed with the Local Civil Registrar. PSA "
            "authentication and DFA countersignature are then required before "
            "international use."
        ),
        'doc_time': '3-6 weeks (PSA and DFA authentication are the main delays)',
        'timeline_avg': '4-6 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in the Philippines is available and increasingly common.',
        'postmortem_trigger': 'Unexpected, violent, or medically uncertified deaths',
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
    'jordan': {
        'name': 'Jordan',
        'emergency': '911 (police) / 912 (ambulance)',
        'registry': 'the Civil Status and Passports Department',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 911 for police or 912 for ambulance. Death is certified by a "
            "physician and registered with the Civil Status and Passports Department. "
            "The public prosecutor takes jurisdiction for violent or unexplained "
            "deaths. All documentation is in Arabic and requires certified translation. "
            "Jordan's climate requires prompt embalming."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Jordan.',
        'postmortem_trigger': 'Violent or unexplained deaths (public prosecutor)',
    },
    'iraq': {
        'name': 'Iraq',
        'emergency': '104 (police) / 115 (ambulance)',
        'registry': 'the Civil Status Directorate',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 104 for police or 115 for ambulance. Death is certified by a "
            "physician and registered with the Civil Status Directorate. For "
            "violent or unexplained deaths, police and judicial procedures apply. "
            "The FCDO advises against all travel to large parts of Iraq; access "
            "to consular and civil registry services varies significantly by "
            "location. All documentation is in Arabic."
        ),
        'doc_time': '2-4 weeks (highly variable)',
        'timeline_avg': '6-12 weeks',
        'timeline_fast': '4-6 weeks',
        'timeline_complex': 'many months',
        'complexity': 'high',
        'cremation': (
            'Cremation is not available in Iraq for Muslim remains. Non-Muslim '
            'remains face very limited options.'
        ),
        'postmortem_trigger': (
            'Violent, suspicious, or unexplained deaths; security situation may '
            'further delay access'
        ),
    },
    'iran': {
        'name': 'Iran',
        'emergency': '110 (police) / 115 (ambulance)',
        'registry': 'the Sazman-e Sabt-e Ahval (Civil Registration Organization)',
        'cert_name': 'death certificate (in Farsi)',
        'cert_lang': 'Farsi (Persian)',
        'overview': (
            "Call 110 for police or 115 for ambulance. Death is certified by a "
            "physician and registered with the Sazman-e Sabt-e Ahval (Civil "
            "Registration Organization). The judiciary takes jurisdiction for "
            "violent or unexplained deaths. The FCDO advises against travel to "
            "Iran, and consular access is limited; British interests in Iran are "
            "represented by the Swedish Embassy in Tehran."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': '3-6 months',
        'complexity': 'high',
        'cremation': (
            'Cremation is not available for Muslim remains in Iran. Non-Muslim '
            'families face very limited options.'
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths (judiciary)',
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
            "for violent or unexplained deaths. Documentation is in English. "
            "Ghana's tropical climate requires prompt embalming."
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
    'canada': {
        'name': 'Canada',
        'emergency': '911',
        'registry': 'the provincial or territorial civil records authority',
        'cert_name': 'death certificate',
        'cert_lang': 'English or French',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician or "
            "medical examiner. The death is registered with the relevant provincial "
            "or territorial civil records authority. The coroner or medical examiner "
            "takes jurisdiction for sudden, violent, or unexplained deaths. Canada "
            "is a Hague Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Canada is widely available.',
        'postmortem_trigger': (
            'Sudden, violent, or unexplained deaths (coroner or medical examiner)'
        ),
    },
    'saudi-arabia': {
        'name': 'Saudi Arabia',
        'emergency': '999 (police) / 911 (ambulance)',
        'registry': 'the Ministry of Interior civil affairs department',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 999 for police or 911 for ambulance. Death is certified by a "
            "physician. The death is registered with the local Ministry of Interior "
            "civil affairs department. The Public Prosecution takes jurisdiction for "
            "violent or unexplained deaths. All documentation is in Arabic and "
            "requires certified translation. Saudi Arabia's climate requires "
            "prompt embalming."
        ),
        'doc_time': '5-14 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-10 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available in Saudi Arabia.',
        'postmortem_trigger': (
            'Violent or unexplained deaths (Public Prosecution)'
        ),
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
    'thailand': {
        'name': 'Thailand',
        'emergency': '191 (police) / 1669 (ambulance)',
        'registry': 'the local district office (amphoe)',
        'cert_name': 'death certificate (in Thai)',
        'cert_lang': 'Thai',
        'overview': (
            "Call 191 for police or 1669 for ambulance. Death is certified by a "
            "licensed physician. The death must be registered with the local "
            "district office (amphoe). Police take jurisdiction for violent, "
            "accidental, or unexplained deaths. Thailand's tropical climate "
            "requires prompt embalming, particularly outside major cities."
        ),
        'doc_time': '5-14 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Thailand is widely available and commonly used across '
            'Buddhist, Christian, and other communities.'
        ),
        'postmortem_trigger': (
            'Violent, accidental, or unexplained deaths, particularly road '
            'traffic accidents or drowning'
        ),
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
    'somalia': {
        'name': 'Somalia',
        'emergency': 'Emergency services are severely limited across Somalia',
        'registry': (
            'the relevant local authority '
            '(civil registry capacity is highly variable)'
        ),
        'cert_name': 'death certificate (in Somali or Arabic)',
        'cert_lang': 'Somali or Arabic',
        'overview': (
            "Emergency services are severely limited across Somalia. The FCDO "
            "advises against all travel to Somalia. Civil registration capacity "
            "is highly variable by region and may be entirely absent in some "
            "areas. Contact the nearest operational embassy immediately. Death "
            "certification and documentation in Somalia are complex and may "
            "involve significant delays."
        ),
        'doc_time': 'Weeks to months; highly variable by region',
        'timeline_avg': '3-6 months',
        'timeline_fast': '6-10 weeks',
        'timeline_complex': 'Many months or longer',
        'complexity': 'very-high',
        'cremation': (
            'Cremation is not available for Muslim remains in Somalia, in '
            'accordance with Islamic law.'
        ),
        'postmortem_trigger': (
            'Violent or suspicious deaths; the security situation may prevent '
            'access to authorities'
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
    'pakistan': {
        'name': 'Pakistan',
        'emergency': '15 (ambulance) / 1122 (rescue) / 115 (emergency)',
        'registry': 'the National Database and Registration Authority (NADRA)',
        'cert_name': 'death certificate',
        'cert_lang': 'Urdu and English',
        'overview': (
            "Call 115 for emergency services. Death is certified by a physician "
            "and registered with NADRA or the local Union Council. Police take "
            "jurisdiction for violent or unexplained deaths. In more remote "
            "provinces, access to civil registration may be limited. "
            "Pakistan's climate requires prompt embalming."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Pakistan.',
        'postmortem_trigger': 'Violent, accidental, or unexplained deaths',
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
    'oman': {
        'name': 'Oman',
        'emergency': '9999 (police) / 9999 (ambulance)',
        'registry': 'the Royal Oman Police civil registration section',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 9999 for emergency services. Death is certified by a physician "
            "and registered with the Royal Oman Police civil registration section. "
            "The Public Prosecution takes jurisdiction for violent or unexplained "
            "deaths. Muslim remains are handled in accordance with Islamic law. "
            "All documentation is in Arabic and requires certified translation."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Oman.',
        'postmortem_trigger': 'Violent or unexplained deaths (Public Prosecution)',
    },
    'vietnam': {
        'name': 'Vietnam',
        'emergency': '113 (police) / 115 (ambulance)',
        'registry': 'the local civil registry (nha nuoc)',
        'cert_name': 'giay chung tu (death certificate)',
        'cert_lang': 'Vietnamese',
        'overview': (
            "Call 113 for police or 115 for ambulance. A licensed physician must "
            "certify the death. Unexpected deaths trigger police notification. "
            "Death registered with the local civil registry (nha nuoc). The "
            "giay chung tu is issued in Vietnamese only."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Vietnam is available in major cities including Hanoi '
            'and Ho Chi Minh City.'
        ),
        'postmortem_trigger': 'Unexpected or accident deaths',
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
    'france': {
        'name': 'France',
        'emergency': '15 (SAMU) / 17 (police) / 18 (fire) / 112',
        'registry': 'the mairie (town hall) civil registry',
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'French',
        'overview': (
            "Call 15 (SAMU ambulance), 17 (police), or 112. Death is certified "
            "by a physician and the acte de deces is registered at the mairie "
            "(town hall). The procureur de la Republique (prosecutor) takes "
            "jurisdiction for violent or unexplained deaths. France is an EU "
            "member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in France is widely available.',
        'postmortem_trigger': (
            'Violent or unexplained deaths (procureur de la Republique)'
        ),
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
    'spain': {
        'name': 'Spain',
        'emergency': '112',
        'registry': 'the Registro Civil (civil registry)',
        'cert_name': 'Certificado de Defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician "
            "and the Certificado de Defuncion is registered with the local Registro "
            "Civil. For violent, accidental, or unexplained deaths, the Juzgado "
            "de Instruccion (examining magistrate) takes jurisdiction, which adds "
            "time before the body can be released. Spain is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '5-15 working days (Juzgado cases take longer)',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Spain is widely available.',
        'postmortem_trigger': (
            'Violent, accidental, or unexplained deaths (Juzgado de Instruccion)'
        ),
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

ROUTES = [
    # R53 -- South Korea wave 3
    {
        'origin': 'india', 'dest': 'south-korea',
        'embassy_city': 'New Delhi',
        'intro': (
            "India has a large and growing professional community in South Korea, "
            "with Indian nationals working in technology, pharmaceuticals, and "
            "international trade. South Korea is a significant destination for "
            "Indian IT professionals and students. Indian death certificates are "
            "in English, which eases initial steps, but all documents require "
            "authentication through the South Korean Embassy in New Delhi before "
            "the gu office (ward office) can register the death. South Korea is "
            "not a Hague Apostille member, so consular legalisation is required. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'philippines', 'dest': 'south-korea',
        'embassy_city': 'Manila',
        'intro': (
            "Filipino nationals form one of the largest foreign worker communities "
            "in South Korea, with approximately 70,000 Filipinos registered as "
            "residents in 2024. Many work under South Korea's Employment Permit "
            "System (EPS) in manufacturing and service sectors. The Philippines "
            "and South Korea have bilateral labour agreements covering migrant "
            "worker protections. Philippine death certificates require PSA "
            "authentication and DFA countersignature before certified Korean "
            "translation is obtained for the gu office. The South Korean "
            "Embassy in Manila handles consular matters. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'uzbekistan', 'dest': 'south-korea',
        'embassy_city': 'Tashkent',
        'intro': (
            "Uzbek nationals in South Korea include students and workers in "
            "manufacturing under the Employment Permit System (EPS) and the "
            "Specified Skilled Worker scheme. South Korea and Uzbekistan have "
            "strengthened bilateral ties through investment and labour cooperation "
            "agreements. Uzbek documentation, in the Latin-script Uzbek alphabet "
            "or Russian, requires certified Korean translation and authentication "
            "through the South Korean Embassy in Tashkent before submission to "
            "the local gu office. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'south-korea',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in South Korea include English teachers, "
            "professionals, and a community of long-term residents with Korean "
            "cultural and family connections. Australia and South Korea have "
            "a bilateral Free Trade Agreement (KAFTA, 2014) and close "
            "people-to-people ties. Australian death certificates are in English "
            "and generally straightforward for initial steps, though all documents "
            "require authentication through the South Korean Embassy in Canberra, "
            "as South Korea is not a Hague Apostille Convention member. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'usa', 'dest': 'south-korea',
        'embassy_city': 'Washington D.C.',
        'intro': (
            "American nationals in South Korea number around 130,000 residents, "
            "including military personnel and their families, English teachers, "
            "business professionals, and a large Korean-American community. The "
            "United States and South Korea have a Mutual Defense Treaty and one "
            "of the largest bilateral Free Trade Agreements in the world. American "
            "death certificates are in English and require authentication through "
            "the South Korean Embassy in Washington D.C. South Korea is not a "
            "Hague Apostille member, so consular authentication is required for "
            "all documentation. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R53 -- Bahrain wave 3
    {
        'origin': 'jordan', 'dest': 'bahrain',
        'embassy_city': 'Amman',
        'intro': (
            "Jordanian nationals in Bahrain include professionals in banking, "
            "education, and public administration. Jordan and Bahrain share close "
            "ties within the Arab League and the Gulf Cooperation Council framework. "
            "Arabic-language Jordanian death certificates are accepted directly by "
            "the Civil Status and Passports Affairs Authority (CSPA) in Bahrain, "
            "though consular authentication by the Bahraini Embassy in Amman is "
            "still required before the CSPA can register the death. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'iraq', 'dest': 'bahrain',
        'embassy_city': 'Baghdad',
        'intro': (
            "Iraqi nationals in Bahrain include professionals and workers in "
            "construction and service sectors. Iraq and Bahrain share cultural "
            "and religious ties as neighbouring Gulf states. Arabic-language "
            "Iraqi death certificates require authentication by the Bahraini "
            "Embassy in Baghdad before the Civil Status and Passports Affairs "
            "Authority (CSPA) can register the death. Families should be aware "
            "that the FCDO advises against travel to large parts of Iraq, which "
            "may complicate consular access. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'iran', 'dest': 'bahrain',
        'embassy_city': 'Tehran',
        'intro': (
            "Iranian nationals requiring repatriation to Bahrain face a complex "
            "consular situation. Bahrain severed diplomatic relations with Iran "
            "in 2016 following political tensions; families should verify the "
            "current status of the Bahraini Embassy in Tehran directly with the "
            "Bahrain Ministry of Foreign Affairs before relying on this route. "
            "If Bahraini consular services are unavailable in Tehran, documentation "
            "may need to be processed through the Bahraini Embassy in a third "
            "country. All documentation in Farsi requires certified Arabic "
            "translation for the Civil Status and Passports Affairs Authority "
            "(CSPA). (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ghana', 'dest': 'bahrain',
        'embassy_city': 'Accra',
        'intro': (
            "Ghanaian nationals in Bahrain include domestic workers, healthcare "
            "professionals, and workers in the service sector. Ghana has become "
            "an increasingly active participant in Gulf labour migration, with "
            "Bahrain among the destination countries under bilateral labour "
            "frameworks. English-language Ghanaian death certificates require "
            "consular authentication by the Bahraini Embassy in Accra before "
            "certified Arabic translation is obtained for the Civil Status and "
            "Passports Affairs Authority (CSPA). "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'nigeria', 'dest': 'bahrain',
        'embassy_city': 'Abuja',
        'intro': (
            "Nigerian nationals in Bahrain include professionals in oil and gas, "
            "healthcare, and the service sector. Nigeria and Bahrain have "
            "maintained diplomatic ties within the Organisation of Islamic "
            "Cooperation (OIC) and Gulf Cooperation Council framework. "
            "English-language Nigerian death certificates require consular "
            "authentication by the Bahraini Embassy in Abuja before certified "
            "Arabic translation is obtained for the Civil Status and Passports "
            "Affairs Authority (CSPA). "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R53 -- Japan wave 8
    {
        'origin': 'singapore', 'dest': 'japan',
        'embassy_city': 'Singapore',
        'intro': (
            "Singapore nationals in Japan include professionals, students, and a "
            "community of long-term residents with close Japan ties. Singapore "
            "and Japan have a bilateral Economic Partnership Agreement (JSEPA, "
            "2002) and strong people-to-people connections through tourism and "
            "business. Singapore death certificates are in English and Japan is "
            "a Hague Apostille Convention member, which simplifies document "
            "authentication. The Japanese Embassy in Singapore handles consular "
            "matters. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'japan',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in Japan include professionals, English teachers, "
            "and a community with Japanese family connections. Canada and Japan "
            "have a bilateral Economic Partnership Agreement (CJJEPA, 2012) and "
            "maintain close diplomatic ties. Canadian death certificates are in "
            "English or French. As Japan is a Hague Apostille member, Canadian "
            "documentation can be apostilled rather than requiring full consular "
            "legalisation. The Japanese Embassy in Ottawa handles consular matters. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'saudi-arabia', 'dest': 'japan',
        'embassy_city': 'Riyadh',
        'intro': (
            "Saudi Arabian nationals in Japan include students, professionals, "
            "and a growing community reflecting bilateral energy and investment "
            "ties. Japan imports a significant share of its oil from Saudi Arabia, "
            "and Saudi Vision 2030 has brought increased numbers of Saudi students "
            "and professionals to Japan. Arabic-language Saudi documentation "
            "requires certified Japanese translation and authentication through the "
            "Japanese Embassy in Riyadh before submission to the municipal office "
            "(shiyakusho). (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'iraq', 'dest': 'japan',
        'embassy_city': 'Baghdad',
        'intro': (
            "Iraqi nationals in Japan include students, scholars, and a small "
            "community of long-term residents. Japan and Iraq have maintained "
            "diplomatic relations and Japan's Embassy in Baghdad remains "
            "operational, though families should be aware of the FCDO's travel "
            "advice for Iraq which advises against travel to large parts of the "
            "country. Arabic-language Iraqi documentation requires certified "
            "Japanese translation and authentication through the Japanese Embassy "
            "in Baghdad. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'jordan', 'dest': 'japan',
        'embassy_city': 'Amman',
        'intro': (
            "Jordanian nationals in Japan include students and professionals, "
            "with Japan providing significant development assistance to Jordan "
            "over the decades. Japan and Jordan maintain strong bilateral ties "
            "and the Japanese Embassy in Amman covers consular matters. Arabic-"
            "language Jordanian documentation requires certified Japanese "
            "translation and authentication through the Japanese Embassy in Amman "
            "before submission to the local municipal office (shiyakusho). "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R53 -- New Zealand wave 6
    {
        'origin': 'japan', 'dest': 'new-zealand',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japanese nationals in New Zealand include students, professionals, "
            "and a well-established community on working holiday visas. New "
            "Zealand and Japan have a bilateral Economic Partnership Agreement "
            "(NZJEPA, 2009) and the New Zealand Embassy in Tokyo handles "
            "consular matters. Japanese death certificates are in Japanese and "
            "require certified English translation. Both Japan and New Zealand "
            "are Hague Apostille Convention members, which simplifies document "
            "authentication. (New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'thailand', 'dest': 'new-zealand',
        'embassy_city': 'Bangkok',
        'intro': (
            "Thai nationals in New Zealand include students, professionals, and "
            "a community of long-term residents with New Zealand family connections. "
            "New Zealand and Thailand have bilateral economic ties within ASEAN "
            "frameworks. The New Zealand Embassy in Bangkok handles consular "
            "matters for New Zealand in Thailand. Thai death certificates require "
            "certified English translation. New Zealand is a Hague Apostille "
            "member; Thai documents will need to go through the Thai Ministry "
            "of Foreign Affairs for authentication before use in New Zealand. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'singapore', 'dest': 'new-zealand',
        'embassy_city': 'Singapore',
        'intro': (
            "Singaporean nationals in New Zealand include professionals, students "
            "on working holiday visas, and a community of long-term residents. "
            "Singapore and New Zealand have a bilateral Closer Economic Partnership "
            "Agreement (NZSCEP, 2001). Both countries are Hague Apostille "
            "Convention members and Singapore issues death certificates in English, "
            "which significantly reduces document complexity. The New Zealand High "
            "Commission in Singapore handles consular matters. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'ethiopia', 'dest': 'new-zealand',
        'embassy_city': 'Nairobi',
        'intro': (
            "Ethiopian nationals in New Zealand include students and professionals, "
            "with the community growing through skilled migration pathways. New "
            "Zealand does not maintain a resident embassy in Ethiopia; consular "
            "matters for Ethiopia are covered by the New Zealand Embassy in "
            "Nairobi, Kenya. Ethiopian documentation from VERA, Ethiopia's civil "
            "events registration authority, is issued in Amharic and requires "
            "certified English translation. New Zealand is a Hague Apostille "
            "member; Ethiopian documents require appropriate authentication before "
            "use in New Zealand. (New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'ghana', 'dest': 'new-zealand',
        'embassy_city': 'Abuja',
        'intro': (
            "Ghanaian nationals in New Zealand include students, nurses, and "
            "healthcare professionals in a community that has grown through New "
            "Zealand's skilled migrant and health worker recruitment pathways. "
            "New Zealand does not maintain a resident embassy in Ghana; consular "
            "matters for West Africa are covered by the New Zealand Embassy in "
            "Abuja, Nigeria. English-language Ghanaian death certificates are "
            "generally accepted without translation, though New Zealand Hague "
            "Apostille requirements mean proper authentication is still needed. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    # R53 -- Oman wave 5
    {
        'origin': 'ghana', 'dest': 'oman',
        'embassy_city': 'Accra',
        'intro': (
            "Ghanaian nationals in Oman include domestic workers and professionals "
            "in construction and healthcare. Oman's workforce includes significant "
            "West African communities recruited through Gulf labour channels. "
            "English-language Ghanaian death certificates require authentication "
            "by the Omani Embassy in Accra before the Royal Oman Police civil "
            "registration section registers the death. Certified Arabic translation "
            "is required for the Ministry of Health burial permit. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'somalia', 'dest': 'oman',
        'embassy_city': 'Mogadishu',
        'intro': (
            "Somali nationals in Oman include workers and a small diaspora "
            "community, reflecting Gulf migration patterns across the Horn of "
            "Africa. Oman maintains an Embassy in Mogadishu. However, the FCDO "
            "advises against all travel to Somalia, and civil registration "
            "capacity is severely limited across much of the country. Families "
            "should expect significant complexity on this corridor. Documentation "
            "in Somali or Arabic requires certified Arabic translation for the "
            "Royal Oman Police. Contact the Omani Embassy in Mogadishu at the "
            "earliest opportunity. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'uzbekistan', 'dest': 'oman',
        'embassy_city': 'Tashkent',
        'intro': (
            "Uzbek nationals in Oman include workers in construction and technical "
            "sectors, reflecting the growth of Central Asian labour migration to "
            "the Gulf. Oman and Uzbekistan have maintained diplomatic relations "
            "and the Omani Embassy in Tashkent handles consular matters. Uzbek "
            "documentation, issued in Uzbek or Russian, requires certified Arabic "
            "translation for the Royal Oman Police civil registration section. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'russia', 'dest': 'oman',
        'embassy_city': 'Moscow',
        'intro': (
            "Russian nationals in Oman include tourists, investors, and a growing "
            "community of long-term residents, with Oman having become a "
            "significant destination for Russian nationals following 2022. Oman "
            "maintained a neutral diplomatic position and the Russian Embassy in "
            "Muscat and the Omani Embassy in Moscow both remain operational. "
            "Russian death certificates (svidetelstvo o smerti) require certified "
            "Arabic translation for the Royal Oman Police. Families should be "
            "aware of the FCDO's advice against travel to Russia. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'saudi-arabia', 'dest': 'oman',
        'embassy_city': 'Riyadh',
        'intro': (
            "Saudi nationals in Oman include tourists, residents with family "
            "connections, and business professionals, reflecting the close "
            "ties between the two Gulf Cooperation Council member states. The "
            "two countries share a long land border and free movement for GCC "
            "nationals simplifies some aspects of cross-border movement. Arabic-"
            "language Saudi death certificates are accepted directly by the "
            "Royal Oman Police civil registration section, though authentication "
            "by the Omani Embassy in Riyadh is still required. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R54 -- South Korea wave 4
    {
        'origin': 'iran', 'dest': 'south-korea',
        'embassy_city': 'Seoul',
        'intro': (
            "Iranian nationals in South Korea include students, academics, and "
            "professionals, with South Korea and Iran having maintained trade and "
            "diplomatic relations despite international sanctions. The South Korean "
            "Embassy in Tehran remains operational. Farsi-language Iranian "
            "documentation requires certified Korean translation and authentication "
            "through the South Korean Embassy in Tehran before the gu office "
            "(ward office) can register the death. South Korea is not a Hague "
            "Apostille member. Families should contact the South Korean Embassy "
            "in Tehran as a first step. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'iraq', 'dest': 'south-korea',
        'embassy_city': 'Baghdad',
        'intro': (
            "Iraqi nationals in South Korea include students and professionals "
            "on academic and bilateral exchange programmes. South Korea and Iraq "
            "have development and reconstruction cooperation ties. The South "
            "Korean Embassy in Baghdad handles consular matters. Arabic-language "
            "Iraqi documentation requires certified Korean translation and "
            "authentication through the South Korean Embassy in Baghdad. Families "
            "should be aware of the FCDO's advice against travel to large parts "
            "of Iraq. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'pakistan', 'dest': 'south-korea',
        'embassy_city': 'Islamabad',
        'intro': (
            "Pakistani nationals in South Korea include workers under the "
            "Employment Permit System (EPS) and students. South Korea and "
            "Pakistan have bilateral ties within the South Asian development "
            "framework, and Pakistan has been a participant country in South "
            "Korea's EPS scheme. Urdu and English Pakistani documentation requires "
            "certified Korean translation and authentication through the South "
            "Korean Embassy in Islamabad before the gu office (ward office) can "
            "register the death. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'malaysia', 'dest': 'south-korea',
        'embassy_city': 'Kuala Lumpur',
        'intro': (
            "Malaysian nationals in South Korea include students, professionals, "
            "and workers in manufacturing and technology. South Korea and Malaysia "
            "have a bilateral Economic Partnership Agreement and close trade ties "
            "within the ASEAN-Korea framework. The South Korean Embassy in Kuala "
            "Lumpur handles consular matters. Malaysian death certificates (sijil "
            "kematian) in Bahasa Malaysia require certified Korean translation and "
            "authentication. South Korea is not a Hague Apostille member, so "
            "full consular authentication is required. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'singapore', 'dest': 'south-korea',
        'embassy_city': 'Singapore',
        'intro': (
            "Singaporean nationals in South Korea include business professionals, "
            "students, and a community with strong Korea connections through trade "
            "and the Korea-Singapore Free Trade Agreement (2006). Singapore issues "
            "death certificates in English, which eases initial steps. However, "
            "South Korea is not a Hague Apostille Convention member, so all "
            "documents still require authentication through the South Korean "
            "Embassy in Singapore before the gu office (ward office) can register "
            "the death. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R54 -- Bahrain wave 4
    {
        'origin': 'turkey', 'dest': 'bahrain',
        'embassy_city': 'Ankara',
        'intro': (
            "Turkish nationals in Bahrain include professionals and workers in "
            "construction and professional services. Turkey and Bahrain have "
            "strengthened bilateral ties within the Organisation of Islamic "
            "Cooperation (OIC) and Gulf Cooperation Council engagement frameworks. "
            "Turkish death certificates (olum belgesi) require certified Arabic "
            "translation for the Civil Status and Passports Affairs Authority "
            "(CSPA) and authentication by the Bahraini Embassy in Ankara. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'qatar', 'dest': 'bahrain',
        'embassy_city': 'Doha',
        'intro': (
            "Qatari nationals in Bahrain include business people and visitors, "
            "reflecting the close ties between the two Gulf Cooperation Council "
            "member states. The Gulf diplomatic crisis (2017-2021), in which "
            "Bahrain joined the blockade of Qatar, has ended and normal diplomatic "
            "relations were restored through the Al-Ula Declaration in January 2021. "
            "Arabic-language Qatari documentation is accepted directly by the "
            "Civil Status and Passports Affairs Authority (CSPA), though "
            "authentication by the Bahraini Embassy in Doha remains required. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'kuwait', 'dest': 'bahrain',
        'embassy_city': 'Kuwait City',
        'intro': (
            "Kuwaiti nationals in Bahrain include business people, tourists, and "
            "a community of residents with family and commercial ties across the "
            "Gulf Cooperation Council. Kuwait and Bahrain are close GCC partners "
            "and normal movement between the two countries is well-established. "
            "Arabic-language Kuwaiti documentation is accepted directly by the "
            "Civil Status and Passports Affairs Authority (CSPA), though "
            "authentication by the Bahraini Embassy in Kuwait City is still "
            "required. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'oman', 'dest': 'bahrain',
        'embassy_city': 'Muscat',
        'intro': (
            "Omani nationals in Bahrain include business professionals, students, "
            "and visitors with close GCC ties. Oman and Bahrain are both members "
            "of the Gulf Cooperation Council, and movement between the two "
            "countries is straightforward for GCC nationals. Arabic-language "
            "Omani documentation is accepted by the Civil Status and Passports "
            "Affairs Authority (CSPA) without translation, though authentication "
            "by the Bahraini Embassy in Muscat is still required before "
            "registration can proceed. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'vietnam', 'dest': 'bahrain',
        'embassy_city': 'Hanoi',
        'intro': (
            "Vietnamese nationals in Bahrain include domestic workers and workers "
            "in construction and hospitality, reflecting Vietnam's active Gulf "
            "labour migration programmes. Vietnam and Bahrain have a bilateral "
            "labour cooperation framework. Vietnamese death certificates (giay "
            "chung tu) require certified Arabic translation for the Civil Status "
            "and Passports Affairs Authority (CSPA) and authentication by the "
            "Bahraini Embassy in Hanoi. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R54 -- Japan wave 9
    {
        'origin': 'oman', 'dest': 'japan',
        'embassy_city': 'Muscat',
        'intro': (
            "Omani nationals in Japan include students and professionals on "
            "academic exchanges and business visits. Japan and Oman have "
            "maintained bilateral ties through energy cooperation and diplomatic "
            "exchanges, with Japan importing significant quantities of Omani "
            "liquefied natural gas. Arabic-language Omani documentation requires "
            "certified Japanese translation and authentication through the Japanese "
            "Embassy in Muscat before submission to the municipal office "
            "(shiyakusho). (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'bahrain', 'dest': 'japan',
        'embassy_city': 'Manama',
        'intro': (
            "Bahraini nationals in Japan include students, business professionals, "
            "and visitors on academic and economic exchanges. Japan and Bahrain "
            "have maintained bilateral diplomatic relations and the Japanese "
            "Embassy in Manama handles consular matters. Arabic-language Bahraini "
            "documentation requires certified Japanese translation and "
            "authentication through the Japanese Embassy in Manama before "
            "submission to the local municipal office (shiyakusho). "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'kuwait', 'dest': 'japan',
        'embassy_city': 'Kuwait City',
        'intro': (
            "Kuwaiti nationals in Japan include students, business professionals, "
            "and tourists. Japan and Kuwait have close energy ties: Japan imports "
            "a substantial share of its oil from Kuwait, and Kuwaiti sovereign "
            "wealth investment in Japan has grown. The Japanese Embassy in Kuwait "
            "City handles consular matters. Arabic-language Kuwaiti documentation "
            "requires certified Japanese translation and authentication through "
            "the Japanese Embassy in Kuwait City. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'qatar', 'dest': 'japan',
        'embassy_city': 'Doha',
        'intro': (
            "Qatari nationals in Japan include students, investors, and business "
            "professionals reflecting the two countries' energy partnership. Japan "
            "is one of Qatar's largest LNG export markets, and Japanese "
            "infrastructure investment in Qatar has deepened bilateral ties. The "
            "Japanese Embassy in Doha handles consular matters. Arabic-language "
            "Qatari documentation requires certified Japanese translation and "
            "authentication through the Japanese Embassy in Doha before submission "
            "to the local municipal office (shiyakusho). "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'japan',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Japan include professionals, students, and a "
            "community of long-term residents with Japan connections. Spain and "
            "Japan have maintained diplomatic relations since 1868, one of the "
            "longest bilateral ties Japan holds in Europe. Spanish death "
            "certificates (Certificado de Defuncion) are in Spanish and require "
            "certified Japanese translation. Both Spain and Japan are Hague "
            "Apostille Convention members, which simplifies authentication. The "
            "Japanese Embassy in Madrid handles consular matters. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R54 -- New Zealand wave 7
    {
        'origin': 'iran', 'dest': 'new-zealand',
        'embassy_city': 'Tehran',
        'intro': (
            "Iranian nationals in New Zealand include students and professionals, "
            "with New Zealand being one of the destinations for Iranian-born "
            "skilled migrants. New Zealand maintains an Embassy in Tehran and "
            "the Iranian Embassy in Wellington covers Iranian interests. Farsi-"
            "language Iranian documentation requires certified English translation. "
            "New Zealand is a Hague Apostille member; Iranian documents will need "
            "to be authenticated before use. Families should be aware that the "
            "FCDO advises against travel to Iran. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'iraq', 'dest': 'new-zealand',
        'embassy_city': 'Baghdad',
        'intro': (
            "Iraqi nationals in New Zealand include refugees who arrived during "
            "the 1990s and 2000s and subsequent family reunification migrants, "
            "with significant Iraqi communities in Auckland and Wellington. New "
            "Zealand maintains an Embassy in Baghdad. Arabic-language Iraqi "
            "documentation requires certified English translation. Families should "
            "be aware that the FCDO advises against travel to large parts of Iraq, "
            "and that consular access varies significantly by location. New Zealand "
            "is a Hague Apostille member but Iraqi documents will need authentication "
            "through the Iraqi Ministry of Foreign Affairs. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'turkey', 'dest': 'new-zealand',
        'embassy_city': 'Ankara',
        'intro': (
            "Turkish nationals in New Zealand include students, professionals, and "
            "a community with New Zealand connections through business and family. "
            "New Zealand and Turkey have maintained diplomatic relations and the "
            "New Zealand Embassy in Ankara handles consular matters. Turkish death "
            "certificates (olum belgesi) require certified English translation. "
            "New Zealand is a Hague Apostille member; Turkish documents require "
            "authentication through the Turkish Ministry of Foreign Affairs before "
            "use in New Zealand. (New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'cambodia', 'dest': 'new-zealand',
        'embassy_city': 'Phnom Penh',
        'intro': (
            "Cambodian nationals in New Zealand include students, professionals, "
            "and a community that arrived through humanitarian and family "
            "reunification pathways. New Zealand maintains an Embassy in Phnom "
            "Penh. Khmer-language Cambodian documentation requires certified "
            "English translation. New Zealand is a Hague Apostille member; "
            "Cambodian documents require authentication through the Cambodian "
            "Ministry of Foreign Affairs before use in New Zealand. Cambodia's "
            "tropical climate requires urgent embalming on this corridor. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'laos', 'dest': 'new-zealand',
        'embassy_city': 'Bangkok',
        'intro': (
            "Lao nationals in New Zealand include students and a small community "
            "of long-term residents. New Zealand does not maintain a resident "
            "embassy in Laos; consular matters are covered by the New Zealand "
            "Embassy in Bangkok, Thailand. Lao-language documentation requires "
            "certified English translation. New Zealand is a Hague Apostille "
            "member; Lao documents require authentication through Lao authorities "
            "before use in New Zealand. Outside Vientiane, access to civil "
            "registration services and international transport is limited. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    # R54 -- Oman wave 6
    {
        'origin': 'germany', 'dest': 'oman',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Oman include professionals in engineering, "
            "energy, and construction, and a community of long-term residents. "
            "Germany and Oman have maintained bilateral economic ties and the "
            "Omani Embassy in Berlin handles consular matters. German death "
            "certificates (Sterbeurkunde) are in German and require certified "
            "Arabic translation for the Royal Oman Police civil registration "
            "section. Both Germany and Oman are not in the same Apostille "
            "framework, so consular authentication through the Omani Embassy "
            "in Berlin is required. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'oman',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Oman include professionals in oil and gas, "
            "education, and the defence sector, and a community of long-term "
            "residents. France and Oman have long-standing bilateral ties in "
            "defence, energy, and diplomacy. The Omani Embassy in Paris handles "
            "consular matters. French death certificates (actes de deces) require "
            "certified Arabic translation for the Royal Oman Police civil "
            "registration section. Authentication by the Omani Embassy in Paris "
            "is required before the Royal Oman Police can register the death. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'oman',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Oman include professionals in oil and gas, "
            "defence, and education, and a community of long-term residents. "
            "Australia and Oman maintain bilateral diplomatic relations and the "
            "Omani Embassy in Canberra handles consular matters. Australian death "
            "certificates are in English and require certified Arabic translation "
            "for the Royal Oman Police civil registration section. Australia is "
            "a Hague Apostille member; authentication through the Omani Embassy "
            "in Canberra remains required regardless. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'oman',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in Oman include professionals in oil and gas, "
            "healthcare, and engineering, and a community of long-term residents. "
            "Canada and Oman maintain bilateral diplomatic relations and the Omani "
            "Embassy in Ottawa handles consular matters. Canadian death certificates "
            "are in English or French and require certified Arabic translation for "
            "the Royal Oman Police civil registration section. Authentication by "
            "the Omani Embassy in Ottawa is required before registration proceeds. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'usa', 'dest': 'oman',
        'embassy_city': 'Washington D.C.',
        'intro': (
            "American nationals in Oman include professionals in oil and gas, "
            "defence, education, and a long-established community with strong "
            "US-Oman bilateral ties. The United States and Oman signed a bilateral "
            "Free Trade Agreement in 2006, and significant US military cooperation "
            "has deepened the relationship. American death certificates require "
            "certified Arabic translation for the Royal Oman Police civil "
            "registration section. Authentication by the Omani Embassy in "
            "Washington D.C. is required. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
]

# ---------------------------------------------------------------------------
# Generate route content
# ---------------------------------------------------------------------------

def make_dest_key(dest_slug):
    keys = {
        'south-korea': 'kr', 'bahrain': 'bh', 'japan': 'jp',
        'new-zealand': 'nz', 'oman': 'om',
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
