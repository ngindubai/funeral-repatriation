#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R51-R52.

   R51 (25 routes, variants D,E,A,B,C x5):
     Bahrain NEW HUB x5: india, pakistan, bangladesh, philippines, nepal
     South Korea NEW HUB x5: china, vietnam, thailand, indonesia, myanmar
     Japan wave 6 x5: taiwan, mongolia, uzbekistan, russia, ukraine
     Canada wave 7 x5: nepal, cambodia, laos, somalia, taiwan
     New Zealand wave 5 x5: russia, ukraine, germany, france, netherlands

   R52 (25 routes, variants D,E,A,B,C x5):
     Bahrain wave 2 x5: sri-lanka, kenya, ethiopia, egypt, indonesia
     South Korea wave 2 x5: cambodia, mongolia, bangladesh, russia, nepal
     Japan wave 7 x5: new-zealand, turkey, egypt, argentina, netherlands
     South Africa wave 8 x5: poland, hungary, iraq, iran, argentina
     Switzerland wave 6 x5: ukraine, philippines, ghana, senegal, iraq

   Template rotation: R50 ended C (index 2). R51 starts D (index 3).
   Each block of 25 cycles D,E,A,B,C x5, ending on C. R52 starts D again.

   Embassy notes:
   - Japan-Taiwan: Japan-Taiwan Exchange Association (JTEA) handles consular
     matters; no formal Japanese Embassy in Taiwan.
   - Japan-Ukraine: Japanese Embassy relocated from Kyiv to Warsaw, Feb 2022.
   - Japan-Russia: Japanese Embassy in Moscow operational with reduced capacity.
   - Canada-Nepal: Canada has no resident embassy in Nepal; covered from
     High Commission in New Delhi.
   - Canada-Laos: Canada has no resident embassy in Laos; covered from Bangkok.
   - Canada-Somalia: Canada has no resident embassy in Somalia; covered from Nairobi.
   - Canada-Taiwan: Canadian Trade Office in Taipei handles consular matters.
   - NZ-Russia: NZ suspended Moscow Embassy March 2022; covered from Warsaw.
   - NZ-Ukraine: NZ has no resident embassy in Ukraine; covered from Warsaw.
   - South Africa-Iraq: South Africa has no resident embassy in Iraq; covered
     from Amman, Jordan.
   - Switzerland-Iraq: Swiss Embassy in Baghdad handles consular matters.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 3  # D

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

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
        'emergency_line': 'contact Bahraini Embassy in origin country',
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
    'canada': {
        'name': 'Canada',
        'slug': 'canada',
        'key': 'ca',
        'reception': (
            "The Canadian funeral director takes custody at Toronto Pearson (YYZ), "
            "Vancouver (YVR), or another major Canadian airport cargo terminal. "
            "The provincial or territorial civil records authority "
            "registers the death. A burial permit is required before "
            "final disposition. Canada is a Hague Apostille Convention member. "
            "Documents not in English or French require certified translation. "
            "(Global Affairs Canada, 2025.)"
        ),
        'consular_template': (
            "Canadian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Canada. Global Affairs "
            "Canada 24-hour emergency line: +1 613 996 8885. The High Commission "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Canadian funeral director takes custody at Toronto Pearson (YYZ) "
            "or Vancouver (YVR) cargo terminal. The provincial civil records "
            "authority registers the death. A burial permit is required before "
            "final disposition. Canada is a Hague Apostille member. Documents not "
            "in English or French require certified translation. The receiving "
            "funeral director coordinates with local authorities."
        ),
        'emergency_line': '+1 613 996 8885',
        'hub_url': 'repatriation-from-canada',
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
    'south-africa': {
        'name': 'South Africa',
        'slug': 'south-africa',
        'key': 'za',
        'reception': (
            "The South African funeral director takes custody at O.R. Tambo "
            "International Airport (JNB) or Cape Town International (CPT) cargo "
            "terminal. The Department of Home Affairs registers the death and "
            "issues the South African death certificate. A burial order is required "
            "before final disposition. All foreign documents not in English require "
            "certified translation. (South African Department of International "
            "Relations and Cooperation, DIRCO, 2025.)"
        ),
        'consular_template': (
            "South African Embassy or High Commission in {city} can advise on "
            "documentation requirements for repatriation to South Africa. South "
            "African Department of International Relations and Cooperation (DIRCO) "
            "can be reached via the South African Embassy in origin country. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The South African funeral director takes custody at O.R. Tambo "
            "International Airport (JNB) cargo terminal. The Department of Home "
            "Affairs registers the death and issues the death certificate. A burial "
            "order is required before final disposition. All foreign documents not "
            "in English require certified translation. The receiving funeral "
            "director coordinates with the Department of Home Affairs."
        ),
        'emergency_line': 'contact South African Embassy in origin country',
        'hub_url': 'repatriation-from-south-africa',
    },
    'switzerland': {
        'name': 'Switzerland',
        'slug': 'switzerland',
        'key': 'ch',
        'reception': (
            "The Swiss funeral director (Bestattungsunternehmen) takes custody at "
            "Zurich (ZRH) or Geneva (GVA) cargo terminal. The local "
            "Zivilstandsamt (civil registry office) registers the death. A "
            "Bestattungsbewilligung (burial authorisation) is required before "
            "final disposition. Switzerland is a Hague Apostille Convention "
            "member. Documents not in German, French, or Italian require certified "
            "translation. (Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
        'consular_template': (
            "Swiss Embassy in {city} can advise on documentation requirements for "
            "repatriation to Switzerland. Swiss Federal Department of Foreign "
            "Affairs (FDFA) 24-hour helpline: +41 800 24 7 365. The Swiss Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Swiss funeral director takes custody at Zurich (ZRH) or Geneva "
            "(GVA) cargo terminal. The Zivilstandsamt registers the death. A "
            "Bestattungsbewilligung is required before final disposition. "
            "Switzerland is a Hague Apostille member. Documents not in German, "
            "French, or Italian require certified translation. The receiving "
            "funeral director coordinates with the Zivilstandsamt."
        ),
        'emergency_line': '+41 800 24 7 365',
        'hub_url': 'repatriation-from-switzerland',
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
    'bangladesh': {
        'name': 'Bangladesh',
        'emergency': '999',
        'registry': 'the local registration office',
        'cert_name': 'death certificate (in Bengali)',
        'cert_lang': 'Bengali',
        'overview': (
            "Call 999 for emergency services. Death is certified by a physician "
            "and registered with the local registration office. Police take "
            "jurisdiction for violent or unexplained deaths. Documentation is "
            "in Bengali and requires certified translation."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Bangladesh is available for non-Muslim remains.',
        'postmortem_trigger': 'Violent or unexplained deaths',
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
    'nepal': {
        'name': 'Nepal',
        'emergency': '100 (police) / 102 (ambulance)',
        'registry': 'the relevant ward or municipality office',
        'cert_name': 'death certificate (in Nepali)',
        'cert_lang': 'Nepali',
        'overview': (
            "Call 100 for police or 102 for ambulance. Death is certified by a "
            "registered medical practitioner. Registration is required with the "
            "relevant ward or municipality office. For deaths in remote or "
            "high-altitude areas, access to medical facilities and civil registry "
            "offices may be severely limited. Police take jurisdiction for violent, "
            "accidental, or unexplained deaths."
        ),
        'doc_time': '10-21 days; mountain or remote area deaths take longer',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '8-16 weeks',
        'complexity': 'high',
        'cremation': (
            'Cremation in Nepal is the traditional Hindu and Buddhist practice, '
            'widely carried out at cremation ghats. Non-Hindu and non-Buddhist '
            'cremation facilities are limited.'
        ),
        'postmortem_trigger': (
            'Violent, accidental, or unexplained deaths, particularly those in '
            'mountain areas or involving foreign nationals'
        ),
    },
    'sri-lanka': {
        'name': 'Sri Lanka',
        'emergency': '119 (police) / 110 (ambulance)',
        'registry': 'the local Divisional Secretariat',
        'cert_name': 'death certificate',
        'cert_lang': 'Sinhala, Tamil, and English',
        'overview': (
            "Call 119 for police or 110 for ambulance. Death is certified by a "
            "physician and registered with the local Divisional Secretariat. Police "
            "take jurisdiction for violent or unexplained deaths. Documentation is "
            "issued in Sinhala, Tamil, and English."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Sri Lanka is available and commonly used.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'kenya': {
        'name': 'Kenya',
        'emergency': '999 / 112',
        'registry': 'the Births, Deaths and Marriages Registry',
        'cert_name': 'death certificate (in English)',
        'cert_lang': 'English',
        'overview': (
            "Call 999 or 112 for emergency services. Death is certified by a "
            "registered medical practitioner. Registration is required with the "
            "local Births, Deaths and Marriages Registry. Police take jurisdiction "
            "for violent or unexplained deaths. Kenya's tropical climate means "
            "embalming should be arranged without delay."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-10 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Kenya is available in Nairobi and some major cities, '
            'though burial remains the more common practice.'
        ),
        'postmortem_trigger': 'Violent, accidental, or unexplained deaths',
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
    'egypt': {
        'name': 'Egypt',
        'emergency': '122 (police) / 123 (ambulance)',
        'registry': 'the Ministry of Interior civil registry',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 122 for police or 123 for ambulance. Death is certified by a "
            "physician and registered with the local Ministry of Interior civil "
            "registry. Police take jurisdiction for violent or unexplained deaths. "
            "All documentation is in Arabic and requires certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Egypt.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'indonesia': {
        'name': 'Indonesia',
        'emergency': '112',
        'registry': 'the local civil registry (catatan sipil)',
        'cert_name': 'surat keterangan kematian (death certificate)',
        'cert_lang': 'Bahasa Indonesia',
        'overview': (
            "Call 112 for emergency services. Unexpected deaths require police "
            "attendance. Death registered with the local civil registry (catatan "
            "sipil). The surat keterangan kematian is issued in Bahasa Indonesia. "
            "Deaths in Bali require internal transfer to Jakarta (CGK) for "
            "international cargo departure."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Indonesia (including Bali, where Hindu cremation is '
            'traditional) is available.'
        ),
        'postmortem_trigger': 'Unexpected and unnatural deaths',
    },
    'china': {
        'name': 'China',
        'emergency': '120 (ambulance) / 110 (police)',
        'registry': 'the local civil affairs bureau (minzhengju)',
        'cert_name': 'si wang zheng ming shu (death certificate)',
        'cert_lang': 'Mandarin Chinese',
        'overview': (
            "Call 120 for ambulance or 110 for police. Death must be certified by "
            "a physician at a recognised medical facility. The death is registered "
            "with the local civil affairs bureau (minzhengju). Police take "
            "jurisdiction for sudden, violent, or unexplained deaths. All "
            "documentation is in Mandarin Chinese and requires certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in China is the standard and in most cities the legally '
            'required method of disposition.'
        ),
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths',
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
    'myanmar': {
        'name': 'Myanmar',
        'emergency': '199 (police) / 192 (ambulance)',
        'registry': 'the General Administration Department',
        'cert_name': 'death certificate (in Burmese)',
        'cert_lang': 'Burmese (Myanmar)',
        'overview': (
            "Call 199 for police or 192 for ambulance. Death is certified by a "
            "physician and registered with the General Administration Department. "
            "The FCDO advises against all travel to Myanmar due to ongoing "
            "political instability. Access to civil registry services, medical "
            "facilities, and international transport links is severely disrupted "
            "in many areas. Contact the nearest operational embassy immediately."
        ),
        'doc_time': '2-4 weeks; significantly longer in conflict-affected areas',
        'timeline_avg': '6-12 weeks',
        'timeline_fast': '4-6 weeks',
        'timeline_complex': 'many months in unstable areas',
        'complexity': 'high',
        'cremation': (
            'Cremation in Myanmar is available in major cities and is common in '
            'Buddhist communities.'
        ),
        'postmortem_trigger': (
            'Violent, unexplained, or conflict-related deaths; the security '
            'situation may prevent access to authorities'
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
    'mongolia': {
        'name': 'Mongolia',
        'emergency': '102 (police) / 103 (ambulance)',
        'registry': 'the State Registration Authority (SRA)',
        'cert_name': 'death certificate (in Mongolian)',
        'cert_lang': 'Mongolian',
        'overview': (
            "Call 102 for police or 103 for ambulance. Death is certified by a "
            "licensed physician. Registration is required with the State "
            "Registration Authority (SRA). Police take jurisdiction for violent "
            "or unexplained deaths. In rural areas of Mongolia, access to medical "
            "facilities and civil registry services may be limited."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Mongolia is available in Ulaanbaatar, though traditional '
            'burial is more common in rural areas.'
        ),
        'postmortem_trigger': 'Violent, accidental, or unexplained deaths',
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
    'ukraine': {
        'name': 'Ukraine',
        'emergency': '102 (police) / 103 (ambulance)',
        'registry': 'the civil registry office (DRACS)',
        'cert_name': 'death certificate (in Ukrainian)',
        'cert_lang': 'Ukrainian',
        'overview': (
            "Call 102 for police or 103 for ambulance. In areas not affected by "
            "hostilities, death is certified by a physician and registered with the "
            "civil registry office (DRACS). In areas affected by the ongoing "
            "conflict, access to civil registry services and the ability to "
            "transport remains may be severely limited or impossible. The FCDO "
            "advises against all travel to Ukraine."
        ),
        'doc_time': '7-14 days (stable areas); highly variable in conflict zones',
        'timeline_avg': '3-6 weeks (stable areas)',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': 'many months or impossible in conflict zones',
        'complexity': 'high',
        'cremation': (
            'Cremation in Ukraine is available in major cities in non-conflict areas.'
        ),
        'postmortem_trigger': 'Violent, unexplained, or conflict-related deaths',
    },
    'taiwan': {
        'name': 'Taiwan',
        'emergency': '110 (police) / 119 (fire and ambulance)',
        'registry': 'the Household Registration Office (Huji Shiwusuo)',
        'cert_name': 'death certificate (in Traditional Chinese)',
        'cert_lang': 'Traditional Chinese',
        'overview': (
            "Call 110 for police or 119 for fire and ambulance. Death is certified "
            "by a licensed physician. The death notification and certificate are "
            "registered with the Household Registration Office (Huji Shiwusuo). "
            "The prosecutor's office takes jurisdiction for violent or unexplained "
            "deaths. Taiwan is not a member of the Hague Apostille Convention; "
            "documents require authentication through designated channels."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Taiwan is widely available and the most common final '
            'disposition, particularly in urban areas.'
        ),
        'postmortem_trigger': (
            'Violent, sudden, or unexplained deaths (prosecutor\'s office)'
        ),
    },
    'new-zealand': {
        'name': 'New Zealand',
        'emergency': '111',
        'registry': 'Births, Deaths and Marriages New Zealand (BDM)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 111 for emergency services. A registered medical practitioner "
            "certifies the death. The death is registered with Births, Deaths and "
            "Marriages New Zealand (BDM). The coroner takes jurisdiction for sudden, "
            "unexpected, or violent deaths."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in New Zealand is widely available.',
        'postmortem_trigger': (
            'Sudden, unexpected, or violent deaths (coroner takes jurisdiction)'
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
    'argentina': {
        'name': 'Argentina',
        'emergency': '101 (police) / 107 (ambulance)',
        'registry': 'the Registro Civil y Capacidad de las Personas',
        'cert_name': 'Acta de Defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 101 for police or 107 for ambulance. Death is certified by a "
            "physician and registered with the Registro Civil y Capacidad de las "
            "Personas. The Acta de Defuncion is issued in Spanish. Police and "
            "the judicial system take jurisdiction for violent or unexplained deaths."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Argentina is available in major cities.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'netherlands': {
        'name': 'Netherlands',
        'emergency': '112',
        'registry': 'the gemeente (municipality) Burgerlijke Stand (civil registry)',
        'cert_name': 'overlijdensakte (death certificate, in Dutch)',
        'cert_lang': 'Dutch',
        'overview': (
            "Call 112 for emergency services. Death is certified by a registered "
            "physician. The overlijdensakte (death certificate) is registered with "
            "the local gemeente (municipality) Burgerlijke Stand (civil registry). "
            "The Officier van Justitie (public prosecutor) takes jurisdiction for "
            "violent or unexplained deaths. The Netherlands is an EU member and "
            "Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in the Netherlands is widely available.',
        'postmortem_trigger': (
            'Violent or unexplained deaths '
            '(Officier van Justitie)'
        ),
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
    'somalia': {
        'name': 'Somalia',
        'emergency': 'Emergency services are severely limited across Somalia',
        'registry': 'the relevant local authority (civil registry capacity is highly variable)',
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
    'poland': {
        'name': 'Poland',
        'emergency': '112 / 997 (police) / 999 (ambulance)',
        'registry': 'the Urzad Stanu Cywilnego (USC, civil registry)',
        'cert_name': 'akt zgonu (death certificate, in Polish)',
        'cert_lang': 'Polish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The akt zgonu (death certificate) is registered with the local Urzad "
            "Stanu Cywilnego (USC). The prokuratura (public prosecutor's office) "
            "takes jurisdiction for violent or unexplained deaths. Poland is an "
            "EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Poland is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (prokuratura)',
    },
    'hungary': {
        'name': 'Hungary',
        'emergency': '112 / 107 (police) / 104 (ambulance)',
        'registry': 'the anyakonyvvezeto (civil registrar, local government office)',
        'cert_name': 'halotti anyakonyvi kivonat (death certificate, in Hungarian)',
        'cert_lang': 'Hungarian',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The halotti anyakonyvi kivonat (death certificate) is issued by the "
            "local anyakonyvvezeto (civil registrar). The ugyeszseg (prosecutor's "
            "office) takes jurisdiction for violent or unexplained deaths. Hungary "
            "is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Hungary is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (ugyeszseg)',
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
    'senegal': {
        'name': 'Senegal',
        'emergency': '17 (police) / 15 (SAMU ambulance)',
        'registry': 'the Direction de l\'Etat Civil (civil registry)',
        'cert_name': 'acte de deces (death certificate, in French)',
        'cert_lang': 'French',
        'overview': (
            "Call 17 for police or 15 for SAMU ambulance. Death is certified by a "
            "physician and the acte de deces is registered with the local Direction "
            "de l'Etat Civil. Police take jurisdiction for violent or unexplained "
            "deaths. Documentation is in French. Senegal's tropical climate requires "
            "prompt embalming."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-10 weeks',
        'complexity': 'moderate',
        'cremation': (
            'Cremation in Senegal is limited. Burial is the standard practice for '
            'Muslim families, who make up the majority of the population.'
        ),
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

ROUTES = [
    # R51 -- Bahrain NEW HUB wave 1
    {
        'origin': 'india', 'dest': 'bahrain',
        'embassy_city': 'New Delhi',
        'intro': (
            "India has one of the largest foreign national communities in Bahrain, "
            "with an estimated 350,000 Indian nationals working across construction, "
            "finance, healthcare, and hospitality sectors. India and Bahrain have "
            "longstanding diplomatic ties strengthened through the Gulf Cooperation "
            "Council framework, and Bahrain has maintained an Indian Embassy since "
            "1971. English-language Indian death certificates are accepted by "
            "Bahraini authorities, though consular legalisation is required. The "
            "Bahraini Embassy in New Delhi handles repatriation documentation enquiries. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'pakistan', 'dest': 'bahrain',
        'embassy_city': 'Islamabad',
        'intro': (
            "Pakistani nationals form one of Bahrain's largest foreign worker "
            "communities, with hundreds of thousands employed in construction, "
            "manufacturing, domestic service, and professional sectors. Pakistan "
            "and Bahrain share close bilateral ties within the Organisation of "
            "Islamic Cooperation (OIC) and the Gulf Cooperation Council framework. "
            "Urdu and English documentation from Pakistan requires consular "
            "authentication by the Bahraini Embassy before certified Arabic "
            "translation for the Civil Status and Passports Affairs Authority "
            "(CSPA). The Bahraini Embassy in Islamabad handles consular matters. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'bangladesh', 'dest': 'bahrain',
        'embassy_city': 'Dhaka',
        'intro': (
            "Bangladeshi nationals are among the most significant migrant worker "
            "communities in Bahrain, with tens of thousands employed in "
            "construction, domestic service, and general labour sectors. Bangladesh "
            "and Bahrain have bilateral agreements on labour migration within the "
            "Gulf Cooperation Council framework. Bengali documentation requires "
            "certified Arabic translation for the Civil Status and Passports "
            "Affairs Authority (CSPA). The Bahraini Embassy in Dhaka handles "
            "consular matters. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'philippines', 'dest': 'bahrain',
        'embassy_city': 'Manila',
        'intro': (
            "Filipino nationals in Bahrain number in the tens of thousands, "
            "working in domestic service, healthcare, hospitality, and professional "
            "sectors. The Philippines and Bahrain have a memorandum of understanding "
            "on the deployment of overseas Filipino workers. Philippine death "
            "certificates require PSA authentication and DFA countersignature "
            "before certified Arabic translation is obtained for the Civil Status "
            "and Passports Affairs Authority (CSPA). The Bahraini Embassy in "
            "Manila handles consular matters. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'nepal', 'dest': 'bahrain',
        'embassy_city': 'New Delhi',
        'intro': (
            "Nepali nationals in Bahrain include significant numbers of construction "
            "and domestic workers, reflecting wider South Asian migration patterns "
            "to the Gulf. Bahrain does not have a resident embassy in Nepal; the "
            "nearest Bahraini Embassy is in New Delhi, which covers consular "
            "matters for Nepali nationals in Bahrain. Nepali death certificates "
            "require certified Arabic translation for the Civil Status and Passports "
            "Affairs Authority (CSPA). Families in Nepal should contact the "
            "Bahraini Embassy in New Delhi directly. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R51 -- South Korea NEW HUB wave 1
    {
        'origin': 'china', 'dest': 'south-korea',
        'embassy_city': 'Beijing',
        'intro': (
            "Chinese nationals form the largest foreign community in South Korea, "
            "with around 800,000 residents in 2024, including a significant "
            "Korean-Chinese (Joseonjok) population. China and South Korea have "
            "major trade and cultural ties: South Korea is one of China's largest "
            "trading partners, and millions of people move between the two countries "
            "annually. Chinese documentation (si wang zheng ming shu) requires "
            "certified Korean translation and authentication through the South "
            "Korean Embassy in Beijing before the gu office (ward office) can "
            "register the death. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'vietnam', 'dest': 'south-korea',
        'embassy_city': 'Hanoi',
        'intro': (
            "Vietnamese nationals form the second-largest foreign community in "
            "South Korea, with approximately 250,000 residents in 2024, including "
            "workers under the Employment Permit System (EPS) and marriage migrants. "
            "South Korea and Vietnam signed a strategic partnership in 2001, and "
            "bilateral trade and migration have grown significantly since. Vietnamese "
            "documentation (giay chung tu) requires certified Korean translation "
            "and authentication through the South Korean Embassy in Hanoi. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'thailand', 'dest': 'south-korea',
        'embassy_city': 'Bangkok',
        'intro': (
            "Thai nationals in South Korea include workers under the Employment "
            "Permit System (EPS) and visitors. South Korea and Thailand have "
            "bilateral ties within the ASEAN-Republic of Korea framework, with "
            "people-to-people connections growing through tourism and professional "
            "exchanges. Thai documentation requires certified Korean translation "
            "and authentication through the South Korean Embassy in Bangkok. "
            "The South Korean Embassy in Bangkok handles consular matters. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'indonesia', 'dest': 'south-korea',
        'embassy_city': 'Jakarta',
        'intro': (
            "Indonesian nationals in South Korea include workers under the "
            "Employment Permit System (EPS) and students, with Indonesia a "
            "significant participant in South Korea's bilateral labour agreements. "
            "South Korea and Indonesia have a bilateral Economic Partnership "
            "Agreement and longstanding trade ties. Indonesian documentation "
            "(surat keterangan kematian) requires certified Korean translation "
            "and authentication through the South Korean Embassy in Jakarta. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'myanmar', 'dest': 'south-korea',
        'embassy_city': 'Yangon',
        'intro': (
            "Myanmar nationals in South Korea include workers under the Employment "
            "Permit System (EPS), with South Korea one of the principal "
            "destinations for Myanmar migrant workers. South Korean authorities "
            "maintain the EPS programme for Myanmar despite the political situation "
            "there, as many Myanmar workers have settled in South Korea for extended "
            "periods. Myanmar documentation requires certified Korean translation "
            "and authentication through the South Korean Embassy in Yangon. "
            "Families should be aware of the FCDO's advice against travel to "
            "Myanmar. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R51 -- Japan wave 6
    {
        'origin': 'taiwan', 'dest': 'japan',
        'embassy_city': 'Taipei',
        'intro': (
            "Taiwan and Japan have a close relationship managed through unofficial "
            "channels: Japan does not maintain a formal embassy in Taiwan, with "
            "consular services handled through the Japan-Taiwan Exchange Association "
            "(JTEA) offices in Taipei and Kaohsiung. Tens of thousands of Taiwanese "
            "nationals live and work in Japan, and Japan is one of Taiwan's most "
            "significant trading and cultural partners. Traditional Chinese "
            "documentation requires certified Japanese translation. Families should "
            "contact the Japan-Taiwan Exchange Association (JTEA) in Taipei for "
            "documentation assistance. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'mongolia', 'dest': 'japan',
        'embassy_city': 'Ulaanbaatar',
        'intro': (
            "Mongolia has one of the fastest-growing migrant communities in Japan, "
            "with over 20,000 Mongolian nationals registered as residents in 2024. "
            "Many Mongolians work in Japan's manufacturing, construction, and "
            "service sectors, and a significant number are engaged in professional "
            "and academic roles. Japan and Mongolia have maintained bilateral "
            "diplomatic relations since 1972, and cultural exchanges have grown "
            "steadily. Mongolian documentation requires certified Japanese "
            "translation. The Japanese Embassy in Ulaanbaatar handles consular "
            "matters. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'uzbekistan', 'dest': 'japan',
        'embassy_city': 'Tashkent',
        'intro': (
            "Uzbek nationals in Japan include students and workers in manufacturing "
            "and technical training programmes, reflecting the growth in Japan's "
            "Specified Skilled Worker visa scheme. Japan and Uzbekistan have "
            "strengthened bilateral ties through the Central Asia plus Japan "
            "Dialogue framework and cooperation on infrastructure and energy. "
            "Uzbek documentation in the Latin-script Uzbek alphabet requires "
            "certified Japanese translation for the municipal office (shiyakusho). "
            "The Japanese Embassy in Tashkent handles consular matters. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'russia', 'dest': 'japan',
        'embassy_city': 'Moscow',
        'intro': (
            "Russian nationals in Japan number around 8,000 residents, including "
            "professionals, students, and families with Japanese-Russian ties. "
            "Japan-Russia relations have been significantly strained since 2022, "
            "and the Japanese Embassy in Moscow continues to operate with a reduced "
            "staff following the mutual expulsions of diplomats. Families in Russia "
            "requiring repatriation to Japan should contact the Japanese Embassy "
            "in Moscow directly. Russian documentation requires certified Japanese "
            "translation for the municipal office (shiyakusho). "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ukraine', 'dest': 'japan',
        'embassy_city': 'Warsaw',
        'intro': (
            "Ukrainian nationals in Japan include students, professionals, and a "
            "growing community of those who relocated following the February 2022 "
            "invasion. Japan granted temporary protection status to Ukrainian "
            "displaced persons, and the Ukrainian community in Japan grew "
            "significantly from 2022. The Japanese Embassy suspended operations "
            "in Kyiv in February 2022 and relocated to Warsaw, Poland; Ukrainian "
            "families requiring repatriation to Japan should contact the Japanese "
            "Embassy in Warsaw. Ukrainian documentation requires certified Japanese "
            "translation. (Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R51 -- Canada wave 7
    {
        'origin': 'nepal', 'dest': 'canada',
        'embassy_city': 'New Delhi',
        'intro': (
            "Nepal's community in Canada has grown rapidly, with significant "
            "Nepali populations in Toronto, Calgary, and Vancouver, driven by "
            "international student migration and skilled worker streams. Canada "
            "does not maintain a resident embassy in Nepal; consular matters are "
            "handled by the Canadian High Commission in New Delhi. Nepali "
            "documentation requires certified English or French translation. "
            "The Canadian High Commission in New Delhi handles documentation "
            "enquiries for Nepali families in Canada. "
            "(Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'cambodia', 'dest': 'canada',
        'embassy_city': 'Phnom Penh',
        'intro': (
            "Cambodia's community in Canada is concentrated in Montreal, Toronto, "
            "and Vancouver, with many families arriving as refugees following the "
            "Khmer Rouge period and through subsequent family reunification. Canada "
            "and Cambodia maintain diplomatic relations, and the Canadian Embassy "
            "in Phnom Penh handles consular matters. Khmer documentation requires "
            "certified English or French translation. Families should be aware "
            "that Cambodia's tropical climate requires prompt embalming before "
            "repatriation can proceed. (Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'laos', 'dest': 'canada',
        'embassy_city': 'Bangkok',
        'intro': (
            "The Lao community in Canada includes refugees who arrived in the late "
            "1970s and 1980s and subsequent family reunifications, concentrated "
            "in Quebec, Ontario, and Alberta. Canada does not maintain a resident "
            "embassy in Laos; consular matters are handled by the Canadian Embassy "
            "in Bangkok, Thailand. Lao documentation requires certified English or "
            "French translation. Families requiring repatriation of a loved one "
            "who has died in Laos should contact the Canadian Embassy in Bangkok "
            "as a first step. (Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'somalia', 'dest': 'canada',
        'embassy_city': 'Nairobi',
        'intro': (
            "Canada hosts one of the world's largest Somali diaspora communities, "
            "with an estimated 150,000 or more Somali Canadians concentrated "
            "primarily in Toronto and Ottawa. Many Somali Canadians maintain close "
            "family connections to Somalia and travel there regularly. Canada "
            "does not maintain a resident embassy in Somalia; the Canadian High "
            "Commission in Nairobi handles consular matters for Somalia. Given "
            "the FCDO's advice against all travel to Somalia and the highly "
            "variable civil registration situation, specialist support is essential "
            "on this corridor. (Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'taiwan', 'dest': 'canada',
        'embassy_city': 'Taipei',
        'intro': (
            "The Taiwanese community in Canada has grown steadily, with significant "
            "populations in Toronto and Vancouver drawn by education and professional "
            "opportunities. Canada does not maintain a formal embassy in Taiwan; "
            "the Canadian Trade Office in Taipei handles consular matters. "
            "Traditional Chinese documentation from Taiwan requires certified "
            "English or French translation. Taiwan is not a member of the Hague "
            "Apostille Convention; documents require authentication through "
            "the Canadian Trade Office in Taipei before use in Canada. "
            "(Global Affairs Canada, 2025.)"
        ),
    },
    # R51 -- New Zealand wave 5
    {
        'origin': 'russia', 'dest': 'new-zealand',
        'embassy_city': 'Warsaw',
        'intro': (
            "Russian nationals in New Zealand include professionals, students, "
            "and a small community of long-term residents with New Zealand "
            "connections. New Zealand suspended the operations of its Moscow "
            "Embassy in March 2022 following Russia's invasion of Ukraine; Russian "
            "matters are now handled by the New Zealand Embassy in Warsaw, Poland. "
            "Russian documentation requires certified English translation. Families "
            "in Russia requiring consular assistance for repatriation to New "
            "Zealand should contact the New Zealand Embassy in Warsaw. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'ukraine', 'dest': 'new-zealand',
        'embassy_city': 'Warsaw',
        'intro': (
            "New Zealand accepted Ukrainian displaced persons following the "
            "February 2022 invasion, and a growing Ukrainian community has settled "
            "in Auckland and Wellington. New Zealand does not maintain a resident "
            "embassy in Ukraine; matters are handled by the New Zealand Embassy "
            "in Warsaw, Poland. In conflict-affected parts of Ukraine, access to "
            "civil registry services and international transport is severely "
            "limited. Ukrainian documentation requires certified English "
            "translation. (New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'new-zealand',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in New Zealand include professionals on working "
            "holiday visas, long-term residents, and retirees drawn by New "
            "Zealand's lifestyle and landscape. Germany and New Zealand have "
            "maintained bilateral diplomatic relations through their respective "
            "embassies, with the German Embassy in Wellington and the New Zealand "
            "Embassy in Berlin covering consular matters. German documentation "
            "(Sterbeurkunde) is accepted by New Zealand authorities without "
            "further translation in most cases, as New Zealand and Germany both "
            "belong to the Hague Apostille Convention. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'new-zealand',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in New Zealand include professionals on working "
            "holiday visas and a community of long-term residents, with New "
            "Caledonia and French Polynesia creating additional France-Pacific "
            "connections. The French Embassy in Wellington handles consular "
            "matters in New Zealand; the New Zealand Embassy in Paris covers "
            "New Zealand interests in France. French documentation (acte de "
            "deces) is accepted by New Zealand authorities without further "
            "translation in most cases, as both countries belong to the Hague "
            "Apostille Convention. "
            "(New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'new-zealand',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in New Zealand include professionals, students on "
            "working holiday visas, and a long-established community of Dutch "
            "immigrants who arrived from the 1950s onwards. The Netherlands "
            "and New Zealand have maintained diplomatic relations through the "
            "Dutch Embassy in Wellington and the New Zealand Embassy in The "
            "Hague. Dutch documentation (overlijdensakte) is accepted by New "
            "Zealand authorities; both countries belong to the Hague Apostille "
            "Convention. (New Zealand Ministry of Foreign Affairs and Trade, 2025.)"
        ),
    },
    # R52 -- Bahrain wave 2
    {
        'origin': 'sri-lanka', 'dest': 'bahrain',
        'embassy_city': 'Colombo',
        'intro': (
            "Sri Lankan nationals in Bahrain include domestic workers, healthcare "
            "professionals, and workers in the hospitality sector. Sri Lanka and "
            "Bahrain have a bilateral labour agreement covering migrant worker "
            "protections within the Gulf Cooperation Council framework. Sri Lankan "
            "documentation (in Sinhala, Tamil, and English) requires consular "
            "authentication by the Bahraini Embassy before certified Arabic "
            "translation for the Civil Status and Passports Affairs Authority "
            "(CSPA). The Bahraini Embassy in Colombo handles consular matters. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'kenya', 'dest': 'bahrain',
        'embassy_city': 'Nairobi',
        'intro': (
            "Kenyan nationals in Bahrain include domestic workers, healthcare "
            "professionals, and workers in the service sector. Kenya has become "
            "an increasingly active participant in Gulf labour migration, with "
            "Bahrain among the destination countries. English-language Kenyan "
            "death certificates require consular authentication by the Bahraini "
            "Embassy before certified Arabic translation is obtained for the "
            "Civil Status and Passports Affairs Authority (CSPA). The Bahraini "
            "Embassy in Nairobi handles consular matters. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ethiopia', 'dest': 'bahrain',
        'embassy_city': 'Addis Ababa',
        'intro': (
            "Ethiopian nationals in Bahrain include domestic workers, who form "
            "a significant part of the Gulf's Ethiopian diaspora. Ethiopia and "
            "Bahrain have maintained diplomatic relations, and the Ethiopian "
            "community in Bahrain has grown alongside Gulf-wide Ethiopian "
            "labour migration. Documentation from VERA, Ethiopia's civil events "
            "registration authority, is issued in Amharic and requires certified "
            "Arabic translation for the Civil Status and Passports Affairs "
            "Authority (CSPA). The Bahraini Embassy in Addis Ababa handles "
            "consular matters. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'egypt', 'dest': 'bahrain',
        'embassy_city': 'Cairo',
        'intro': (
            "Egyptian nationals form one of Bahrain's significant Arab expatriate "
            "communities, with Egyptians working across professional, academic, "
            "and service sectors. Egypt and Bahrain share strong bilateral ties "
            "within the Arab League and the Gulf Cooperation Council framework. "
            "Arabic documentation from Egypt is generally accepted by Bahraini "
            "authorities, though consular authentication by the Bahraini Embassy "
            "in Cairo may still be required. The Bahraini Embassy in Cairo "
            "handles consular matters. (Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'indonesia', 'dest': 'bahrain',
        'embassy_city': 'Jakarta',
        'intro': (
            "Indonesian nationals in Bahrain include domestic workers and "
            "professionals, reflecting Indonesia's significant Gulf labour "
            "migration. Indonesia and Bahrain have bilateral ties within the "
            "Organisation of Islamic Cooperation (OIC), and Indonesia is one of "
            "Bahrain's source countries for migrant workers. Indonesian "
            "documentation (surat keterangan kematian) requires certified Arabic "
            "translation for the Civil Status and Passports Affairs Authority "
            "(CSPA). The Bahraini Embassy in Jakarta handles consular matters. "
            "(Bahrain Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R52 -- South Korea wave 2
    {
        'origin': 'cambodia', 'dest': 'south-korea',
        'embassy_city': 'Phnom Penh',
        'intro': (
            "Cambodian nationals in South Korea include workers under the "
            "Employment Permit System (EPS) and students. South Korea and "
            "Cambodia signed a bilateral labour agreement in 2004, making Cambodia "
            "one of the original EPS-partner countries. Khmer documentation "
            "requires certified Korean translation and authentication through "
            "the South Korean Embassy in Phnom Penh before the gu office "
            "(ward office) can register the death. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'mongolia', 'dest': 'south-korea',
        'embassy_city': 'Ulaanbaatar',
        'intro': (
            "Mongolian nationals form one of the fastest-growing foreign "
            "communities in South Korea, with over 50,000 registered residents "
            "in 2024. Many Mongolians work in South Korea under the Employment "
            "Permit System (EPS) and other visa categories. South Korea and "
            "Mongolia have maintained diplomatic relations since 1990, with "
            "growing trade and people-to-people ties. Mongolian documentation "
            "requires certified Korean translation and authentication through the "
            "South Korean Embassy in Ulaanbaatar. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'bangladesh', 'dest': 'south-korea',
        'embassy_city': 'Dhaka',
        'intro': (
            "Bangladeshi nationals in South Korea include workers under the "
            "Employment Permit System (EPS) and students. South Korea and "
            "Bangladesh signed a bilateral labour agreement, and Bangladesh "
            "has been an active EPS-partner country. Bengali documentation "
            "requires certified Korean translation and authentication through "
            "the South Korean Embassy in Dhaka before the gu office can "
            "register the death in South Korea. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'russia', 'dest': 'south-korea',
        'embassy_city': 'Moscow',
        'intro': (
            "Russian nationals in South Korea include professionals, students, "
            "and members of Sakhalin Korean heritage communities who maintain "
            "family ties to Russia. South Korea and Russia have had diplomatic "
            "relations since 1990, though relations have been strained since "
            "2022. The South Korean Embassy in Moscow continues to handle "
            "consular matters. Russian documentation requires certified Korean "
            "translation and authentication through the South Korean Embassy "
            "in Moscow. (Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'nepal', 'dest': 'south-korea',
        'embassy_city': 'Kathmandu',
        'intro': (
            "Nepali nationals in South Korea include workers under the Employment "
            "Permit System (EPS) and students. Nepal has been one of the most "
            "active EPS-partner countries, and South Korea is among Nepal's "
            "principal labour destinations. South Korea maintains a resident "
            "embassy in Kathmandu. Nepali documentation requires certified Korean "
            "translation and authentication through the South Korean Embassy in "
            "Kathmandu before the gu office can register the death. "
            "(Korean Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R52 -- Japan wave 7
    {
        'origin': 'new-zealand', 'dest': 'japan',
        'embassy_city': 'Wellington',
        'intro': (
            "New Zealand and Japan share close bilateral ties through the "
            "Japan-New Zealand Economic Partnership Agreement and growing "
            "people-to-people connections. New Zealanders in Japan include "
            "teachers, students, and professionals, and a small community of "
            "long-term residents. The Japanese Embassy in Wellington handles "
            "consular matters in New Zealand. English-language New Zealand "
            "death certificates require certified Japanese translation for the "
            "municipal office (shiyakusho) in Japan. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'turkey', 'dest': 'japan',
        'embassy_city': 'Ankara',
        'intro': (
            "Turkish nationals in Japan include students, professionals, and a "
            "small community of long-term residents. Japan and Turkey established "
            "diplomatic relations in 1924, and bilateral ties have grown through "
            "trade, cultural exchanges, and growing tourism flows. Turkish "
            "documentation (olum belgesi) requires certified Japanese translation "
            "for the municipal office (shiyakusho) in Japan. The Japanese Embassy "
            "in Ankara handles consular matters. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'egypt', 'dest': 'japan',
        'embassy_city': 'Cairo',
        'intro': (
            "Egyptian nationals in Japan include students, academics, and "
            "professionals in trade and engineering sectors. Japan and Egypt "
            "have maintained diplomatic relations since 1955, and bilateral "
            "ties have grown through Japanese investment in Egyptian "
            "infrastructure projects. Arabic documentation requires certified "
            "Japanese translation for the municipal office (shiyakusho) in "
            "Japan. The Japanese Embassy in Cairo handles consular matters. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'argentina', 'dest': 'japan',
        'embassy_city': 'Buenos Aires',
        'intro': (
            "Argentina has one of the largest Japanese diaspora (Nikkeijin) "
            "communities in South America, with an estimated 65,000 residents "
            "of Japanese descent. Japanese-Argentine nationals and their "
            "descendants sometimes seek repatriation to Japan, and Japan has "
            "had bilateral agreements facilitating Nikkeijin return migration. "
            "Spanish documentation (Acta de Defuncion) requires certified "
            "Japanese translation for the municipal office (shiyakusho). "
            "The Japanese Embassy in Buenos Aires handles consular matters. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'japan',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in Japan include business professionals, "
            "academics, and representatives of the longstanding Netherlands-Japan "
            "commercial relationship, one of the oldest bilateral ties in Japan's "
            "modern history. Japan and the Netherlands have maintained diplomatic "
            "relations since 1858, when the Treaty of Amity and Commerce was "
            "signed. Dutch documentation (overlijdensakte) requires certified "
            "Japanese translation for the municipal office (shiyakusho). "
            "The Japanese Embassy in The Hague handles consular matters. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R52 -- South Africa wave 8
    {
        'origin': 'poland', 'dest': 'south-africa',
        'embassy_city': 'Warsaw',
        'intro': (
            "Polish nationals in South Africa include professionals, business "
            "people, and a community of long-term residents with South African "
            "connections. Poland and South Africa have maintained diplomatic "
            "relations since the 1990s, with the South African Embassy in Warsaw "
            "handling consular matters for Polish nationals. Polish documentation "
            "(akt zgonu) requires certified English translation for the South "
            "African Department of Home Affairs. Poland is an EU and Hague "
            "Apostille Convention member. "
            "(South African Department of International Relations and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'hungary', 'dest': 'south-africa',
        'embassy_city': 'Budapest',
        'intro': (
            "Hungarian nationals in South Africa include professionals, students, "
            "and a small community of long-term residents. Hungary and South "
            "Africa have maintained diplomatic relations since the post-apartheid "
            "era, with the South African Embassy in Budapest handling consular "
            "matters. Hungarian documentation (halotti anyakonyvi kivonat) "
            "requires certified English translation for the South African "
            "Department of Home Affairs. Hungary is an EU and Hague Apostille "
            "Convention member. "
            "(South African Department of International Relations and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'iraq', 'dest': 'south-africa',
        'embassy_city': 'Amman',
        'intro': (
            "Iraqi nationals in South Africa include asylum seekers, refugees, "
            "and professionals who have settled since the 1990s and 2000s. "
            "South Africa does not maintain a resident embassy in Iraq; "
            "repatriation documentation for South Africa is handled through the "
            "South African Embassy in Amman, Jordan, which covers Iraq. Arabic "
            "documentation requires certified English translation for the South "
            "African Department of Home Affairs. Families should also be aware "
            "of the FCDO's travel advice for Iraq, which advises against travel "
            "to large parts of the country. "
            "(South African Department of International Relations and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'iran', 'dest': 'south-africa',
        'embassy_city': 'Tehran',
        'intro': (
            "Iranian nationals in South Africa include professionals, students, "
            "and a community of asylum seekers and refugees who have settled "
            "since the 1980s. South Africa maintains an Embassy in Tehran, "
            "which handles consular matters for South Africa in Iran. Farsi "
            "documentation requires certified English translation for the "
            "South African Department of Home Affairs. Families should be "
            "aware that the FCDO advises against travel to Iran and that "
            "British consular access in Iran is provided through the Swedish "
            "Embassy in Tehran. "
            "(South African Department of International Relations and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'argentina', 'dest': 'south-africa',
        'embassy_city': 'Buenos Aires',
        'intro': (
            "Argentine nationals in South Africa include professionals, business "
            "people, and a community of long-term residents. Argentina and South "
            "Africa share longstanding diplomatic ties as major Southern Hemisphere "
            "economies, and bilateral trade and cultural exchanges have grown. "
            "The South African Embassy in Buenos Aires handles consular matters. "
            "Spanish documentation (Acta de Defuncion) requires certified English "
            "translation for the South African Department of Home Affairs. "
            "(South African Department of International Relations and Cooperation, 2025.)"
        ),
    },
    # R52 -- Switzerland wave 6
    {
        'origin': 'ukraine', 'dest': 'switzerland',
        'embassy_city': 'Kyiv',
        'intro': (
            "Switzerland granted temporary protection status (S permit) to "
            "Ukrainian displaced persons following February 2022, with over "
            "70,000 Ukrainians living in Switzerland by 2024. Switzerland "
            "maintained its Embassy in Kyiv throughout the conflict, as a "
            "neutral state with ongoing diplomatic engagement in Ukraine. "
            "Ukrainian documentation (in Ukrainian) requires certified German, "
            "French, or Italian translation for the Swiss Zivilstandsamt. "
            "The Swiss Embassy in Kyiv handles consular matters. "
            "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
    },
    {
        'origin': 'philippines', 'dest': 'switzerland',
        'embassy_city': 'Manila',
        'intro': (
            "Filipino nationals in Switzerland include domestic workers, "
            "healthcare professionals, and a community of long-term residents. "
            "Switzerland and the Philippines have maintained diplomatic ties "
            "since 1956, and Filipinos are among Switzerland's significant "
            "non-European migrant communities. Philippine documentation requires "
            "PSA authentication and DFA countersignature before certified German, "
            "French, or Italian translation is obtained for the Swiss "
            "Zivilstandsamt. The Swiss Embassy in Manila handles consular matters. "
            "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
    },
    {
        'origin': 'ghana', 'dest': 'switzerland',
        'embassy_city': 'Accra',
        'intro': (
            "Ghanaian nationals in Switzerland include students, professionals, "
            "and a community of long-term residents. Switzerland and Ghana have "
            "maintained diplomatic relations, and the Swiss Embassy in Accra "
            "handles consular matters. English-language Ghanaian death "
            "certificates are generally accepted by Swiss authorities without "
            "further translation, as English is a recognised working language in "
            "Swiss international administrative practice. Certified translation "
            "into German, French, or Italian may still be required for formal "
            "registration. (Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
    },
    {
        'origin': 'senegal', 'dest': 'switzerland',
        'embassy_city': 'Dakar',
        'intro': (
            "Senegalese nationals in Switzerland include students, professionals, "
            "and a long-established Francophone African community. Switzerland "
            "and Senegal have maintained diplomatic and development cooperation "
            "ties for decades, and the Swiss Embassy in Dakar handles consular "
            "matters. French-language Senegalese documentation (acte de deces) "
            "is generally accepted by Swiss authorities without further translation, "
            "as French is one of Switzerland's official languages. "
            "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
    },
    {
        'origin': 'iraq', 'dest': 'switzerland',
        'embassy_city': 'Baghdad',
        'intro': (
            "Iraqi nationals in Switzerland include a significant community of "
            "asylum seekers and refugees who have settled since the 1990s and "
            "2000s. Switzerland has been a principal destination for Iraqi "
            "asylum seekers in Europe. The Swiss Embassy in Baghdad handles "
            "consular matters in Iraq. Arabic documentation requires certified "
            "German, French, or Italian translation for the Swiss Zivilstandsamt. "
            "Families should be aware of the FCDO's travel advice for Iraq, "
            "which advises against travel to large parts of the country. "
            "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
    },
]

# ---------------------------------------------------------------------------
# Generate route content
# ---------------------------------------------------------------------------

def make_dest_key(dest_slug):
    keys = {
        'bahrain': 'bh', 'south-korea': 'kr', 'japan': 'jp',
        'canada': 'ca', 'new-zealand': 'nz', 'south-africa': 'za',
        'switzerland': 'ch',
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
