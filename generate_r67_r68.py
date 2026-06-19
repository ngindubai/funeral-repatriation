#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R67-R68.

   R67 (25 routes, variants B,C,D,E,A x5):
     Syria x5:   united-kingdom, germany, sweden, france, united-states
     Russia x5:  united-kingdom, germany, france, united-states, finland
     Ukraine x5: united-kingdom, germany, poland, france, united-states
     Myanmar x5: united-kingdom, australia, thailand, singapore, united-states
     Rwanda x5:  united-kingdom, united-states, france, belgium, germany

   R68 (25 routes, variants B,C,D,E,A x5):
     Zambia x5:  united-kingdom, united-states, germany, australia, france
     Sudan x5:   united-kingdom, united-states, germany, egypt, france
     Somalia x5: united-kingdom, germany, sweden, norway, united-states
     Bosnia x5:  united-kingdom, germany, austria, sweden, france
     Serbia x5:  united-kingdom, germany, austria, france, united-states

   Template rotation: R66 ended A (index 0). R67 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R68 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'syria': {
        'name': 'Syria',
        'slug': 'syria',
        'key': 'sy',
        'timeline_avg_override': '8-16 weeks',
        'timeline_fast_override': '8 weeks',
        'timeline_complex_override': '6 months or longer',
        'complexity_override': 'very-high',
        'reception': (
            "Death registration in Syria is handled by the Civil Status "
            "Directorate (Mudiriyyat al-Ahwal al-Madaniyyah) at local "
            "government level. Death certificates are issued in Arabic. "
            "Syria is not a member of the Hague Apostille Convention; full "
            "consular authentication through the relevant Syrian consular "
            "representation is required for all foreign-issued documents. "
            "All foreign documents require certified Arabic translation. "
            "Damascus International Airport (DAM) has had limited operations "
            "during the conflict period; access and routing should be confirmed "
            "with a specialist before proceeding. Repatriation to Syria "
            "requires a specialist with current operational contacts and "
            "up-to-date knowledge of the transitional authorities as of 2025. "
            "For Muslim remains, which account for the large majority of "
            "Syria's population, Islamic law procedures apply and prompt burial "
            "is expected. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(FCDO Travel Advice: Syria, 2025.)"
        ),
        'consular_template': (
            "The Syrian consular representation in {city} can advise on "
            "current documentation requirements for repatriation to Syria. "
            "Syria is not a Hague Apostille Convention member; full consular "
            "authentication is required. Consular arrangements are subject "
            "to change given ongoing political transition. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Civil Status Directorate (Mudiriyyat al-Ahwal al-Madaniyyah) "
            "handles death registration in Syria; certificates are issued in "
            "Arabic. Syria is not a Hague Apostille member; full consular "
            "authentication of all foreign documents is required along with "
            "certified Arabic translation. Damascus International Airport (DAM) "
            "has had limited operations since the conflict; routing must be "
            "confirmed with a specialist. For Muslim remains, Islamic law "
            "procedures apply and prompt burial is expected. Repatriation to "
            "Syria requires a specialist with current operational contacts. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the FCDO on +44 (0)20 7008 5000 for current Syria guidance',
        'hub_url': 'repatriation-from-syria',
    },
    'russia': {
        'name': 'Russia',
        'slug': 'russia',
        'key': 'ru',
        'reception': (
            "The Russian funeral director takes custody at Sheremetyevo "
            "International Airport Moscow (SVO), Domodedovo International "
            "Airport Moscow (DME), or Vnukovo International Airport Moscow "
            "(VKO) cargo terminal, depending on the airline routing. For "
            "other regions, the relevant regional airport cargo terminal "
            "handles arrivals. Death registration is handled by the local "
            "ZAGS office (Zapis Aktov Grazhdanskogo Sostoyaniya, the civil "
            "registration office). Death certificates are issued in Russian. "
            "Russia has been a member of the Hague Apostille Convention since "
            "1992; apostille certificates from member states are accepted for "
            "relevant documents. All foreign documents require certified Russian "
            "translation. Families should verify current airline routes given "
            "aviation disruption since February 2022. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports. "
            "(FCDO Travel Advice: Russia, 2025; Russian Ministry of Justice, 2025.)"
        ),
        'consular_template': (
            "Russian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Russia. Russia has been a Hague "
            "Apostille Convention member since 1992. The Embassy cannot pay "
            "for or arrange repatriation. Families should verify current "
            "diplomatic arrangements before proceeding."
        ),
        'arrival_faq': (
            "The Russian funeral director takes custody at the cargo terminal "
            "of the relevant airport: Sheremetyevo (SVO), Domodedovo (DME), "
            "or Vnukovo (VKO) in Moscow, or the relevant regional airport. "
            "The local ZAGS office (civil registration office) registers the "
            "death; certificates are issued in Russian. Russia has been a "
            "Hague Apostille Convention member since 1992; apostille certificates "
            "from member states are accepted. All foreign documents require "
            "certified Russian translation. Families should verify current "
            "airline routes given aviation disruption since February 2022. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Russian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-russia',
    },
    'ukraine': {
        'name': 'Ukraine',
        'slug': 'ukraine',
        'key': 'ua',
        'timeline_avg_override': '4-12 weeks',
        'timeline_fast_override': '4 weeks',
        'timeline_complex_override': '6 months or longer',
        'complexity_override': 'very-high',
        'reception': (
            "Death registration in Ukraine is handled by the State Registry "
            "of Acts of Civil Status (DRACS) under the Ministry of Justice "
            "of Ukraine. Death certificates are issued in Ukrainian. Ukraine "
            "has been a member of the Hague Apostille Convention since 2003; "
            "apostille certificates from member states are accepted. "
            "Kyiv Boryspil International Airport (KBP) has been closed since "
            "February 2022 due to the ongoing armed conflict. Repatriation "
            "into Ukraine requires routing through neighbouring countries, "
            "primarily Poland via Warsaw (WAW) or Romania. All foreign documents "
            "require certified Ukrainian translation. A specialist with current "
            "operational contacts is required. An embalming certificate and "
            "hermetically sealed coffin are required for all imports. "
            "(FCDO Travel Advice: Ukraine, 2025; Ukrainian Ministry of "
            "Justice, 2025.)"
        ),
        'consular_template': (
            "Ukrainian Embassy or Consulate in {city} can advise on current "
            "documentation requirements for repatriation to Ukraine. Ukraine "
            "has been a Hague Apostille Convention member since 2003. "
            "The Embassy cannot pay for or arrange repatriation. Access "
            "constraints due to the ongoing armed conflict may significantly "
            "affect timelines."
        ),
        'arrival_faq': (
            "Death registration in Ukraine is handled by the State Registry "
            "of Acts of Civil Status (DRACS); certificates are issued in "
            "Ukrainian. Ukraine has been a Hague Apostille Convention member "
            "since 2003; apostille certificates are accepted. Kyiv Boryspil "
            "Airport (KBP) has been closed since February 2022; access must "
            "be arranged via Poland or Romania. All foreign documents require "
            "certified Ukrainian translation. Access constraints due to the "
            "ongoing armed conflict mean timelines are unpredictable. A "
            "specialist with current operational contacts is required. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the FCDO on +44 (0)20 7008 5000 or the Ukrainian Embassy in the origin country',
        'hub_url': 'repatriation-from-ukraine',
    },
    'myanmar': {
        'name': 'Myanmar',
        'slug': 'myanmar',
        'key': 'mm',
        'timeline_avg_override': '4-10 weeks',
        'timeline_fast_override': '4 weeks',
        'timeline_complex_override': '3 months or longer',
        'complexity_override': 'high',
        'reception': (
            "The Myanmar funeral director takes custody at Yangon "
            "International Airport (RGN) cargo terminal, or Mandalay "
            "International Airport (MDL) for central Myanmar. Death "
            "registration is handled by the General Administration "
            "Department (GAD) at township level under the State "
            "Administration Council. Death certificates are issued in "
            "Burmese. Myanmar is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Myanmar "
            "Embassy or Consulate in the country of origin is required. "
            "All foreign documents require certified Burmese translation. "
            "The political situation following the February 2021 military "
            "coup has created additional bureaucratic complexity in death "
            "registration and export procedures. A specialist with current "
            "Myanmar operational contacts is required. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(FCDO Travel Advice: Myanmar, 2025.)"
        ),
        'consular_template': (
            "Myanmar Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Myanmar. "
            "Myanmar is not a Hague Apostille Convention member; full "
            "consular authentication is required. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Myanmar funeral director takes custody at Yangon "
            "International Airport (RGN) or Mandalay International "
            "Airport (MDL) cargo terminal. The General Administration "
            "Department (GAD) at township level registers the death; "
            "certificates are issued in Burmese. Myanmar is not a Hague "
            "Apostille member; full consular authentication through the "
            "Myanmar Embassy in the origin country is required. All foreign "
            "documents require certified Burmese translation. The political "
            "situation since the February 2021 coup has created additional "
            "procedural complexity; a specialist with current operational "
            "contacts is required. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Myanmar Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-myanmar',
    },
    'rwanda': {
        'name': 'Rwanda',
        'slug': 'rwanda',
        'key': 'rw',
        'reception': (
            "The Rwandan funeral director takes custody at Kigali "
            "International Airport (KGL) cargo terminal. Death registration "
            "is handled by the Rwanda Governance Board (RGB) civil "
            "registration directorate. Death certificates are issued in "
            "English, French, or Kinyarwanda, the three official languages "
            "of Rwanda. Rwanda joined the Hague Apostille Convention in "
            "2019; apostille certificates from member states are accepted. "
            "Rwanda is a Commonwealth member; English is widely used in "
            "administration. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(Rwanda Governance Board (RGB), 2025; FCDO Travel Advice: "
            "Rwanda, 2025.)"
        ),
        'consular_template': (
            "Rwandan High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Rwanda. Rwanda "
            "joined the Hague Apostille Convention in 2019. The High "
            "Commission cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Rwandan funeral director takes custody at Kigali "
            "International Airport (KGL) cargo terminal. The Rwanda "
            "Governance Board (RGB) civil registration directorate registers "
            "the death; certificates are issued in English, French, or "
            "Kinyarwanda. Rwanda joined the Hague Apostille Convention in "
            "2019; apostille certificates from member states are accepted. "
            "Rwanda is a Commonwealth member; English is widely used in "
            "administration. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Rwandan High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-rwanda',
    },
    'zambia': {
        'name': 'Zambia',
        'slug': 'zambia',
        'key': 'zm',
        'reception': (
            "The Zambian funeral director takes custody at Kenneth Kaunda "
            "International Airport Lusaka (LUN) cargo terminal, or Simon "
            "Mwansa Kapwepwe International Airport Ndola (NLA) for the "
            "Copperbelt region. Death registration is handled by the "
            "Registrar of Births Marriages and Deaths, under the Ministry "
            "of Home Affairs and Internal Security. Death certificates "
            "are issued in English, the official language of Zambia. "
            "Zambia is not a member of the Hague Apostille Convention; "
            "full consular authentication through the Zambian High "
            "Commission or Embassy in the country of origin is required. "
            "Foreign documents in languages other than English require "
            "certified English translation. Zambia is a Commonwealth member. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Zambia Registrar General's Office, 2025; FCDO Travel "
            "Advice: Zambia, 2025.)"
        ),
        'consular_template': (
            "Zambian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Zambia. Zambia "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. The High Commission cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Zambian funeral director takes custody at Kenneth Kaunda "
            "International Airport Lusaka (LUN) or Simon Mwansa Kapwepwe "
            "International Airport Ndola (NLA) cargo terminal. The Registrar "
            "of Births Marriages and Deaths registers the death and issues "
            "a death certificate in English. Zambia is not a Hague Apostille "
            "member; full consular authentication through the Zambian High "
            "Commission or Embassy in the origin country is required. Foreign "
            "documents in other languages require certified English translation. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Zambian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-zambia',
    },
    'sudan': {
        'name': 'Sudan',
        'slug': 'sudan',
        'key': 'sd',
        'timeline_avg_override': '8-16 weeks',
        'timeline_fast_override': '8 weeks',
        'timeline_complex_override': '6 months or longer',
        'complexity_override': 'very-high',
        'reception': (
            "Death registration in Sudan is handled by the Civil Registration "
            "General Directorate under the Ministry of Interior. Death "
            "certificates are issued in Arabic, the official language. Sudan "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication is required for all foreign-issued documents. All "
            "foreign documents require certified Arabic translation. Khartoum "
            "International Airport (KRT) suffered severe damage in the April "
            "2023 armed conflict and has had extremely limited operations since. "
            "Port Sudan Airport (PZU) is the main functioning gateway as of "
            "2025. The British Embassy in Khartoum suspended operations in "
            "April 2023; British consular assistance is provided through the "
            "British Embassy in Nairobi, Kenya. Repatriation to Sudan requires "
            "a specialist with current operational contacts. For Muslim remains, "
            "which account for the large majority of Sudan's population, Islamic "
            "law procedures apply and prompt burial is expected. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(FCDO Travel Advice: Sudan, 2025.)"
        ),
        'consular_template': (
            "The relevant Sudanese consular representation in {city} can advise "
            "on current documentation requirements for repatriation to Sudan. "
            "Sudan is not a Hague Apostille Convention member; full consular "
            "authentication is required. The Embassy cannot pay for or arrange "
            "repatriation. Arrangements are subject to change given the "
            "ongoing conflict situation."
        ),
        'arrival_faq': (
            "Death registration in Sudan is handled by the Civil Registration "
            "General Directorate; certificates are issued in Arabic. Sudan is "
            "not a Hague Apostille member; full consular authentication of all "
            "foreign documents is required along with certified Arabic "
            "translation. Khartoum Airport (KRT) has had extremely limited "
            "operations since April 2023; Port Sudan Airport (PZU) is the "
            "main functioning gateway. For Muslim remains, Islamic law "
            "procedures apply and prompt burial is expected. Repatriation to "
            "Sudan requires a specialist with current operational contacts. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the FCDO on +44 (0)20 7008 5000 for current Sudan guidance',
        'hub_url': 'repatriation-from-sudan',
    },
    'somalia': {
        'name': 'Somalia',
        'slug': 'somalia',
        'key': 'so',
        'timeline_avg_override': '8-16 weeks',
        'timeline_fast_override': '8 weeks',
        'timeline_complex_override': '6 months or longer',
        'complexity_override': 'very-high',
        'reception': (
            "The funeral director or family representative takes custody at "
            "Mogadishu Aden Adde International Airport (MGQ) cargo terminal, "
            "or Hargeisa Egal International Airport (HGA) for Somaliland. "
            "Civil registration capacity in Somalia is limited; death "
            "registration is handled through local administrative structures "
            "under the Federal Government of Somalia. Death certificates are "
            "issued in Somali or Arabic. Somalia is not a member of the Hague "
            "Apostille Convention; full consular authentication is required "
            "for all foreign documents. No Western embassies maintain a "
            "permanent resident presence in Mogadishu; consular assistance "
            "is provided through regional embassies in Nairobi, Kenya. All "
            "foreign documents require certified Somali or Arabic translation. "
            "Repatriation to Somalia requires a specialist with current "
            "operational contacts. For Muslim remains, which account for the "
            "large majority of Somalia's population, Islamic law procedures "
            "apply and prompt burial is expected. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports. "
            "(FCDO Travel Advice: Somalia, 2025.)"
        ),
        'consular_template': (
            "Somali consular representation in {city} can advise on current "
            "documentation requirements for repatriation to Somalia. Somalia "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required where possible. Repatriation to "
            "Somalia requires specialist coordination. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "Civil registration in Somalia has limited capacity; death "
            "registration is handled through local administrative structures "
            "under the Federal Government of Somalia. Certificates are issued "
            "in Somali or Arabic. Somalia is not a Hague Apostille member. "
            "No Western embassies maintain a permanent resident presence in "
            "Mogadishu; consular assistance is provided through regional "
            "embassies in Nairobi. Mogadishu Aden Adde International Airport "
            "(MGQ) serves as the main gateway. For Muslim remains, Islamic law "
            "procedures apply and prompt burial is expected. Repatriation to "
            "Somalia requires a specialist with current operational contacts. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the FCDO on +44 (0)20 7008 5000 for current Somalia guidance',
        'hub_url': 'repatriation-from-somalia',
    },
    'bosnia-and-herzegovina': {
        'name': 'Bosnia and Herzegovina',
        'short_title': 'Bosnia',
        'slug': 'bosnia-and-herzegovina',
        'key': 'ba',
        'reception': (
            "The Bosnian funeral director takes custody at Sarajevo "
            "International Airport (SJJ) cargo terminal, Mostar "
            "International Airport (OMO), or Banja Luka International "
            "Airport (BNX) for regional arrivals. Death registration is "
            "handled by the maticna sluzba (civil registration service) "
            "at municipality level, operated separately in the Federation "
            "of Bosnia and Herzegovina and Republika Srpska entities. "
            "Death certificates are issued in Bosnian, Croatian, or "
            "Serbian, the three official languages. Bosnia and Herzegovina "
            "joined the Hague Apostille Convention in 2008; apostille "
            "certificates from member states are accepted. Foreign documents "
            "in other languages require certified translation into one of "
            "the official languages. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Bosnia and Herzegovina Ministry of Foreign Affairs, 2025; "
            "FCDO Travel Advice: Bosnia and Herzegovina, 2025.)"
        ),
        'consular_template': (
            "Bosnia and Herzegovina Embassy or Consulate in {city} can "
            "advise on documentation requirements for repatriation to "
            "Bosnia and Herzegovina. Bosnia and Herzegovina joined the "
            "Hague Apostille Convention in 2008. The Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Bosnian funeral director takes custody at Sarajevo "
            "International Airport (SJJ), Mostar International Airport "
            "(OMO), or Banja Luka International Airport (BNX) cargo "
            "terminal. The maticna sluzba (civil registration service) "
            "at municipality level registers the death; certificates are "
            "issued in Bosnian, Croatian, or Serbian. Bosnia and Herzegovina "
            "joined the Hague Apostille Convention in 2008; apostille "
            "certificates from member states are accepted. Foreign documents "
            "in other languages require certified translation. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Bosnia and Herzegovina Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-bosnia-and-herzegovina',
    },
    'serbia': {
        'name': 'Serbia',
        'slug': 'serbia',
        'key': 'rs',
        'reception': (
            "The Serbian funeral director takes custody at Belgrade Nikola "
            "Tesla Airport (BEG) cargo terminal. Death registration is "
            "handled by the opstina (municipality) civil status office. "
            "Death certificates are issued in Serbian, written in both "
            "Cyrillic and Latin scripts. Serbia has been a member of the "
            "Hague Apostille Convention since 2001; apostille certificates "
            "from member states are accepted. Foreign documents in other "
            "languages require certified Serbian translation. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Serbian Ministry of Foreign Affairs, 2025; FCDO Travel "
            "Advice: Serbia, 2025.)"
        ),
        'consular_template': (
            "Serbian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Serbia. Serbia "
            "has been a Hague Apostille Convention member since 2001. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Serbian funeral director takes custody at Belgrade Nikola "
            "Tesla Airport (BEG) cargo terminal. The opstina (municipality) "
            "civil status office registers the death; certificates are "
            "issued in Serbian (Cyrillic and Latin scripts). Serbia has "
            "been a Hague Apostille Convention member since 2001; apostille "
            "certificates from member states are accepted. Foreign documents "
            "in other languages require certified Serbian translation. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Serbian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-serbia',
    },
}

ORIGIN_DATA = {
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
    'sweden': {
        'name': 'Sweden',
        'emergency': '112',
        'registry': 'Skatteverket (Swedish Tax Agency), which manages civil registration',
        'cert_name': 'dodsfallsintyg (death certificate)',
        'cert_lang': 'Swedish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The dodsfallsintyg is issued by the treating physician and civil "
            "registration is updated with Skatteverket (Swedish Tax Agency). "
            "Police and the prosecutor take jurisdiction for violent or unexplained "
            "deaths. Sweden is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Sweden is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (police and prosecutor take jurisdiction)',
    },
    'finland': {
        'name': 'Finland',
        'emergency': '112',
        'registry': 'the Digital and Population Data Services Agency (DVV)',
        'cert_name': 'kuolintodistus (death certificate)',
        'cert_lang': 'Finnish or Swedish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The kuolintodistus is registered with the Digital and Population Data "
            "Services Agency (DVV). Police take jurisdiction for violent or "
            "unexplained deaths. Finland is an EU member and Hague Apostille "
            "Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Finland is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (police take jurisdiction)',
    },
    'poland': {
        'name': 'Poland',
        'emergency': '112 (unified) / 997 (police) / 999 (ambulance)',
        'registry': 'the Urzad Stanu Cywilnego (USC, civil status office) in the district of death',
        'cert_name': 'akt zgonu (death certificate)',
        'cert_lang': 'Polish',
        'overview': (
            "Call 112 for the unified emergency number, 997 for police, or 999 for "
            "ambulance. Death is certified by a physician. The akt zgonu is registered "
            "with the local Urzad Stanu Cywilnego (USC, civil status office). Police "
            "and the prokuratura (public prosecutor) take jurisdiction for violent or "
            "unexplained deaths. Poland is an EU member and Hague Apostille "
            "Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Poland is available; facilities exist in major cities.",
        'postmortem_trigger': 'Violent or unexplained deaths (prokuratura, public prosecutor)',
    },
    'thailand': {
        'name': 'Thailand',
        'emergency': '191 (police) / 1669 (ambulance) / 1155 (tourist police)',
        'registry': 'the local district office (amphoe) or, in Bangkok, the khet office',
        'cert_name': 'death certificate (bai morn sia, issued in Thai)',
        'cert_lang': 'Thai',
        'overview': (
            "Call 191 for police, 1669 for ambulance, or 1155 for the tourist police. "
            "Death is certified by a physician. The death certificate (bai morn sia) "
            "is registered with the local district office (amphoe) or khet in Bangkok, "
            "under the Ministry of Interior. Police take jurisdiction for violent or "
            "unexplained deaths. Thailand is not a member of the Hague Apostille "
            "Convention; full consular authentication is required for Thai-issued "
            "documents intended for use abroad."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation in Thailand is widely available; Buddhist tradition makes "
            "cremation the most common practice."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (police investigation required)',
    },
    'singapore': {
        'name': 'Singapore',
        'emergency': '999 (police) / 995 (fire and ambulance)',
        'registry': 'the Immigration and Checkpoints Authority (ICA), Registry of Births and Deaths',
        'cert_name': 'Certificate of Death',
        'cert_lang': 'English',
        'overview': (
            "Call 999 for police or 995 for fire and ambulance. Death is certified "
            "by a registered medical practitioner. The Certificate of Death is issued "
            "by the Immigration and Checkpoints Authority (ICA), Registry of Births "
            "and Deaths. The Coroner's Court takes jurisdiction for sudden, unnatural, "
            "or violent deaths. Singapore is not a member of the Hague Apostille "
            "Convention, but the process is well-established and English is the "
            "primary administrative language."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Singapore is widely available; it is the most common "
            "form of final disposition."
        ),
        'postmortem_trigger': "Sudden, unnatural, or violent deaths (Coroner's Court takes jurisdiction)",
    },
    'egypt': {
        'name': 'Egypt',
        'emergency': '122 (police) / 123 (ambulance)',
        'registry': (
            'the local civil registration office under the Ministry of Interior, '
            'with statistics coordinated by CAPMAS (Central Agency for Public '
            'Mobilization and Statistics)'
        ),
        'cert_name': 'shahadat al-wafah (death certificate)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 122 for police or 123 for ambulance. Death is certified by a "
            "physician. The shahadat al-wafah (death certificate) is registered "
            "with the local civil registration office under the Ministry of "
            "Interior. Police take jurisdiction for violent or unexplained deaths. "
            "Egypt is not a member of the Hague Apostille Convention; full consular "
            "authentication is required for Egyptian documents intended for use "
            "abroad. Death certificates are issued in Arabic."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is not widely available in Egypt. The large majority of "
            "the population is Muslim, for whom Islamic law prohibits cremation; "
            "Christian communities follow burial practice. Specialist guidance "
            "is required if cremation is sought."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (police investigation required)',
    },
    'norway': {
        'name': 'Norway',
        'emergency': '112 (police) / 113 (ambulance)',
        'registry': (
            'the Folkeregisteret (Norwegian Population Register), '
            'administered by the Norwegian Tax Administration (Skatteetaten)'
        ),
        'cert_name': 'dodsattest (death certificate)',
        'cert_lang': 'Norwegian',
        'overview': (
            "Call 112 for police or 113 for ambulance. Death is certified by a "
            "physician. The dodsattest is issued by the treating physician and "
            "the Folkeregisteret (Norwegian Population Register), administered "
            "by Skatteetaten (Norwegian Tax Administration), is updated. Police "
            "and the statsadvokat (public prosecutor) take jurisdiction for "
            "violent or unexplained deaths. Norway is a Hague Apostille "
            "Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Norway is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (police and public prosecutor take jurisdiction)',
    },
    'austria': {
        'name': 'Austria',
        'emergency': '112 (unified) / 133 (police) / 144 (ambulance)',
        'registry': 'the Standesamt (civil registry) of the local authority',
        'cert_name': 'Sterbeurkunde (death certificate)',
        'cert_lang': 'German',
        'overview': (
            "Call 112 for the unified emergency number, 133 for police, or 144 "
            "for ambulance. Death is certified by a physician. The Sterbeurkunde "
            "is registered with the local Standesamt (civil registry). The "
            "Staatsanwaltschaft (public prosecutor) takes jurisdiction for "
            "violent or unexplained deaths. Austria is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Austria is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft)',
    },
}

ROUTES = [
    # R67 -- Syria x5
    {
        'origin': 'united-kingdom', 'dest': 'syria',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Syria include individuals with family ties and "
            "journalists. The British Embassy in Damascus closed in March 2012. "
            "Consular assistance for British nationals in Syria is provided "
            "through the British Embassy in Beirut, Lebanon, or the FCDO on "
            "+44 (0)20 7008 5000. British death certificates require certified "
            "Arabic translation. Syria is not a Hague Apostille Convention member. "
            "Following the fall of the Assad government in December 2024, "
            "consular arrangements are subject to change; contact the FCDO for "
            "the current position before proceeding. Repatriation to Syria "
            "requires a specialist with current operational contacts. "
            "(FCDO Travel Advice: Syria, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'syria',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Syria include individuals with family ties and "
            "dual nationals. The German Embassy in Damascus suspended operations "
            "in 2012. Consular assistance for German nationals in Syria is "
            "provided through the German Embassy in Beirut. German death "
            "certificates (Sterbeurkunde, in German) require certified Arabic "
            "translation. Syria is not a Hague Apostille Convention member; "
            "full consular authentication is required. The German Foreign "
            "Office advises against all travel to Syria; consular arrangements "
            "are subject to change following the December 2024 political "
            "transition. "
            "(German Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'syria',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in Syria include individuals with family ties "
            "and dual nationals, reflecting a significant Swedish-Syrian diaspora "
            "community. Sweden closed its Embassy in Damascus in 2012. Consular "
            "assistance for Swedish nationals in Syria is provided through the "
            "Swedish Embassy in Beirut or the Swedish Ministry for Foreign "
            "Affairs crisis line. Swedish death certificates (dodsfallsintyg, "
            "in Swedish) require certified Arabic translation. Syria is not a "
            "Hague Apostille Convention member; full consular authentication is "
            "required. Consular arrangements are subject to change following "
            "the December 2024 political transition. "
            "(Swedish Ministry for Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'syria',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Syria include individuals with family ties and "
            "journalists. The French Embassy in Damascus suspended operations "
            "in 2012. Consular assistance for French nationals in Syria is "
            "provided through the French Embassy in Beirut or the French "
            "Ministry of Foreign Affairs crisis line on +33 1 43 17 67 67. "
            "French death certificates (acte de deces, in French) require "
            "certified Arabic translation. Syria is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "Consular arrangements are subject to change following the "
            "December 2024 political transition. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'syria',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Syria include individuals with family ties, "
            "dual nationals, and journalists. The United States closed its "
            "Embassy in Damascus in 2012. Consular assistance for US nationals "
            "in Syria is provided through the US Embassy in Amman, Jordan, or "
            "the US State Department emergency line on +1 888 407 4747. "
            "English-language US death certificates require certified Arabic "
            "translation. Syria is not a Hague Apostille Convention member. "
            "Consular arrangements are subject to change following the "
            "December 2024 political transition in Syria. "
            "(US State Department, 2025.)"
        ),
    },
    # R67 -- Russia x5
    {
        'origin': 'united-kingdom', 'dest': 'russia',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Russia include business professionals, "
            "academics, journalists, and individuals with family ties. The "
            "British Embassy in Moscow remains open but operates with reduced "
            "staffing following the deterioration in UK-Russia relations since "
            "February 2022. Families should contact the British Embassy in "
            "Moscow and the FCDO on +44 (0)20 7008 5000 immediately after a "
            "death. British death certificates require certified Russian "
            "translation and authentication by the Russian Embassy in London. "
            "Russia has been a Hague Apostille Convention member since 1992. "
            "Families should verify current airline routes before proceeding. "
            "(FCDO Travel Advice: Russia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'russia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Russia include business professionals and "
            "individuals with family ties. The German Embassy in Moscow remains "
            "operational. German death certificates (Sterbeurkunde, in German) "
            "require certified Russian translation and authentication by the "
            "Russian Embassy in Berlin. Russia has been a Hague Apostille "
            "Convention member since 1992; apostille certificates are accepted "
            "for German documents. The German Foreign Office advises against "
            "all travel to Russia; families should verify current airline "
            "routes before proceeding. "
            "(German Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'russia',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Russia include business professionals, academics, "
            "and individuals with family ties. The French Embassy in Moscow "
            "remains operational. French death certificates (acte de deces, in "
            "French) require certified Russian translation and authentication by "
            "the Russian Embassy in Paris. Russia has been a Hague Apostille "
            "Convention member since 1992; apostille certificates are accepted "
            "for French documents. The French Ministry of Foreign Affairs advises "
            "against all travel to Russia; families should verify current airline "
            "routes. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'russia',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Russia include business professionals, dual nationals, "
            "and individuals with family ties. The US Embassy in Moscow operates "
            "with significantly reduced staffing but remains open. Families should "
            "contact the US Embassy in Moscow and the US State Department on "
            "+1 888 407 4747 immediately after a death. English-language US death "
            "certificates require certified Russian translation and authentication "
            "by the Russian Embassy in Washington DC. Russia has been a Hague "
            "Apostille Convention member since 1992. Families should verify current "
            "airline routes before proceeding. "
            "(US State Department, 2025.)"
        ),
    },
    {
        'origin': 'finland', 'dest': 'russia',
        'embassy_city': 'Helsinki',
        'intro': (
            "Finnish nationals in Russia include business professionals and "
            "individuals with family ties, reflecting Finland's shared border "
            "with Russia. The Finnish Embassy in Moscow remains operational. "
            "Finnish death certificates (kuolintodistus, in Finnish or Swedish) "
            "require certified Russian translation and authentication by the "
            "Russian Embassy in Helsinki. Russia has been a Hague Apostille "
            "Convention member since 1992; apostille certificates are accepted "
            "for Finnish documents. The Finnish Ministry for Foreign Affairs "
            "advises against all travel to Russia; families should verify "
            "current border and airline arrangements. "
            "(Finnish Ministry for Foreign Affairs, 2025.)"
        ),
    },
    # R67 -- Ukraine x5
    {
        'origin': 'united-kingdom', 'dest': 'ukraine',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Ukraine include individuals with family ties, "
            "aid workers, and journalists. Kyiv Boryspil International Airport "
            "(KBP) has been closed since February 2022 due to the ongoing armed "
            "conflict. Repatriation from Ukraine requires routing through "
            "neighbouring countries, primarily Poland or Romania. The British "
            "Embassy in Kyiv can provide consular assistance where access is "
            "possible; contact the FCDO on +44 (0)20 7008 5000 immediately. "
            "British death certificates require certified Ukrainian translation "
            "and authentication by the Ukrainian Embassy in London. Ukraine has "
            "been a Hague Apostille Convention member since 2003. "
            "(FCDO Travel Advice: Ukraine, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'ukraine',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Ukraine include aid workers and individuals "
            "with family ties. Kyiv Boryspil International Airport (KBP) has "
            "been closed since February 2022. Repatriation requires routing "
            "through Poland, Romania, or Slovakia. The German Embassy in Kyiv "
            "can provide consular assistance where access is possible. German "
            "death certificates (Sterbeurkunde, in German) require certified "
            "Ukrainian translation and authentication by the Ukrainian Embassy "
            "in Berlin. Ukraine has been a Hague Apostille Convention member "
            "since 2003. "
            "(German Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'poland', 'dest': 'ukraine',
        'embassy_city': 'Warsaw',
        'intro': (
            "Polish nationals in Ukraine include individuals with family ties "
            "reflecting Poland's close community connections with Ukraine. "
            "Poland and Ukraine share a border; Warsaw Chopin Airport (WAW) "
            "is a key routing hub for repatriation from Ukraine during the "
            "ongoing conflict. The Polish Embassy in Kyiv can provide consular "
            "assistance where access is possible. Polish death certificates "
            "(akt zgonu, in Polish) require certified Ukrainian translation "
            "and authentication by the Ukrainian Embassy in Warsaw. Ukraine "
            "has been a Hague Apostille Convention member since 2003. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'ukraine',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Ukraine include individuals with family ties "
            "and aid workers. Kyiv Boryspil International Airport (KBP) has "
            "been closed since February 2022. Repatriation requires routing "
            "through Poland, Romania, or Slovakia. The French Embassy in Kyiv "
            "can provide consular assistance where access is possible. French "
            "death certificates (acte de deces, in French) require certified "
            "Ukrainian translation and authentication by the Ukrainian Embassy "
            "in Paris. Ukraine has been a Hague Apostille Convention member "
            "since 2003. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'ukraine',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Ukraine include individuals with family ties, "
            "journalists, and aid workers. The US Embassy in Kyiv relocated "
            "temporarily in February 2022 but has since resumed limited "
            "operations; contact the US State Department on +1 888 407 4747. "
            "Kyiv Boryspil International Airport (KBP) has been closed since "
            "February 2022; repatriation requires routing through Poland or "
            "Romania. English-language US death certificates require certified "
            "Ukrainian translation and authentication by the Ukrainian Embassy "
            "in Washington DC. Ukraine has been a Hague Apostille Convention "
            "member since 2003. "
            "(US State Department, 2025.)"
        ),
    },
    # R67 -- Myanmar x5
    {
        'origin': 'united-kingdom', 'dest': 'myanmar',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Myanmar include business professionals, aid "
            "workers, and tourists. The British Embassy in Yangon can provide "
            "consular assistance; contact the FCDO on +44 (0)20 7008 5000. "
            "Death registration is handled by the General Administration "
            "Department (GAD) at township level under the State Administration "
            "Council, following the February 2021 military coup. British death "
            "certificates require certified Burmese translation and authentication "
            "by the Myanmar Embassy in London. Myanmar is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "Repatriation from Myanmar requires a specialist with current "
            "operational contacts. "
            "(FCDO Travel Advice: Myanmar, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'myanmar',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Myanmar include aid workers, tourists, and "
            "business professionals. The Australian Embassy in Yangon can provide "
            "consular assistance; contact DFAT on 1300 555 135 (Australia) or "
            "+61 2 6261 3305 (overseas). Death registration is handled by the "
            "General Administration Department (GAD) at township level; death "
            "certificates are issued in Burmese. Myanmar is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "Repatriation requires a specialist with current Myanmar contacts "
            "given the ongoing political situation. "
            "(DFAT Smartraveller: Myanmar, 2025.)"
        ),
    },
    {
        'origin': 'thailand', 'dest': 'myanmar',
        'embassy_city': 'Bangkok',
        'intro': (
            "Thai nationals in Myanmar include business professionals and "
            "individuals with family ties, reflecting Thailand's shared border "
            "with Myanmar. The Thai Embassy in Yangon can provide consular "
            "assistance. Thai death certificates (bai morn sia, in Thai) require "
            "certified Burmese translation and authentication by the Myanmar "
            "Embassy in Bangkok. Myanmar is not a Hague Apostille Convention "
            "member; full consular authentication is required. Families should "
            "verify current airline routes between Bangkok and Yangon given "
            "disruption since the February 2021 coup. "
            "(Thai Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'singapore', 'dest': 'myanmar',
        'embassy_city': 'Singapore',
        'intro': (
            "Singapore nationals in Myanmar include business professionals "
            "and individuals with bilateral ties reflecting Singapore's "
            "significant investment presence in Myanmar. The Singapore Embassy "
            "in Yangon can provide consular assistance. Singapore death "
            "certificates (Certificate of Death, in English) require certified "
            "Burmese translation and authentication by the Myanmar Embassy in "
            "Singapore. Myanmar is not a Hague Apostille Convention member; "
            "full consular authentication is required. Families should verify "
            "current airline connections given disruption since the February "
            "2021 coup. "
            "(Singapore Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'myanmar',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Myanmar include aid workers, business professionals, "
            "and journalists. The US Embassy in Yangon can provide consular "
            "assistance; contact the US State Department on +1 888 407 4747. "
            "English-language US death certificates require certified Burmese "
            "translation and authentication by the Myanmar Embassy in Washington "
            "DC. Myanmar is not a Hague Apostille Convention member; full "
            "consular authentication is required. The US State Department "
            "advises against travel to Myanmar. Repatriation requires a "
            "specialist with current operational contacts. "
            "(US State Department, 2025.)"
        ),
    },
    # R67 -- Rwanda x5
    {
        'origin': 'united-kingdom', 'dest': 'rwanda',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Rwanda include development workers, business "
            "professionals, and tourists visiting Volcanoes National Park and "
            "Kigali. The UK and Rwanda maintain close bilateral relations as "
            "Commonwealth members. The British High Commission in Kigali can "
            "assist British nationals after a death. British death certificates "
            "require authentication by the Rwandan High Commission in London. "
            "Rwanda joined the Hague Apostille Convention in 2019; apostille "
            "certificates are accepted for UK-issued documents. English is an "
            "official language of Rwanda and widely used in administration. "
            "(FCDO Travel Advice: Rwanda, 2025; Rwanda Governance Board, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'rwanda',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Rwanda include development workers, aid "
            "professionals, and tourists. The US Embassy in Kigali can assist "
            "US nationals after a death. English-language US death certificates "
            "require authentication by the Rwandan Embassy in Washington DC. "
            "Rwanda joined the Hague Apostille Convention in 2019; apostille "
            "certificates are accepted for US-issued documents. English is an "
            "official language of Rwanda. "
            "(Rwanda Governance Board, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'rwanda',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Rwanda include development workers and "
            "individuals with bilateral ties. France and Rwanda restored "
            "diplomatic relations in 2023 following a reconciliation process. "
            "The French Embassy in Kigali is operational. French death "
            "certificates (acte de deces, in French) are accepted in Rwanda "
            "alongside English; French is a co-official language. "
            "Authentication by the Rwandan Embassy in Paris is required. "
            "Rwanda joined the Hague Apostille Convention in 2019; apostille "
            "certificates are accepted for French documents. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'rwanda',
        'embassy_city': 'Brussels',
        'intro': (
            "Rwandan nationals in Belgium include a significant diaspora "
            "community reflecting the Belgium-Rwanda historical relationship. "
            "Belgium and Rwanda maintain bilateral diplomatic relations and the "
            "Belgian Embassy in Kigali is operational. Belgian death certificates "
            "(in French, Dutch, or German depending on region) require "
            "authentication by the Rwandan Embassy in Brussels. French-language "
            "Belgian certificates are accepted in Rwandan administration alongside "
            "English. Rwanda joined the Hague Apostille Convention in 2019; "
            "apostille certificates are accepted for Belgian documents. "
            "(Rwanda Governance Board, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'rwanda',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Rwanda include development workers and "
            "researchers. Germany and Rwanda maintain bilateral development "
            "cooperation through GIZ programmes. German death certificates "
            "(Sterbeurkunde, in German) require certified English or French "
            "translation and authentication by the Rwandan Embassy in Berlin. "
            "Rwanda joined the Hague Apostille Convention in 2019; apostille "
            "certificates are accepted for German documents. English and French "
            "are official languages of Rwanda. "
            "(Rwanda Governance Board, 2025.)"
        ),
    },
    # R68 -- Zambia x5
    {
        'origin': 'united-kingdom', 'dest': 'zambia',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Zambia include development workers, mining "
            "sector professionals, conservation workers, and tourists visiting "
            "Victoria Falls and national parks. The UK and Zambia maintain "
            "bilateral relations as Commonwealth members. The British High "
            "Commission in Lusaka can assist British nationals after a death. "
            "British death certificates require authentication by the Zambian "
            "High Commission in London. Zambia is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "English is Zambia's official language and widely used in "
            "administration. "
            "(FCDO Travel Advice: Zambia, 2025; Zambia Registrar General's "
            "Office, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'zambia',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Zambia include development workers, NGO "
            "professionals, and researchers. The US Embassy in Lusaka can "
            "assist US nationals after a death. English-language US death "
            "certificates require authentication by the Zambian Embassy in "
            "Washington DC. Zambia is not a Hague Apostille Convention member; "
            "full consular authentication is required. English is Zambia's "
            "official language. "
            "(Zambia Registrar General's Office, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'zambia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Zambia include development workers and "
            "researchers. Germany and Zambia maintain bilateral development "
            "cooperation through GIZ programmes. German death certificates "
            "(Sterbeurkunde, in German) require certified English translation "
            "and authentication by the Zambian Embassy in Berlin. Zambia is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(Zambia Registrar General's Office, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'zambia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Zambia include development workers, "
            "conservation professionals, and tourists. Australian consular "
            "matters in Zambia are handled by the High Commission of Canada "
            "in Lusaka under a consular services sharing arrangement, as "
            "Australia does not maintain a resident High Commission in Zambia. "
            "Australian death certificates (in English) require authentication "
            "by the Zambian High Commission in Canberra. Zambia is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(DFAT Smartraveller: Zambia, 2025; Zambia Registrar General's "
            "Office, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'zambia',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Zambia include development workers and "
            "researchers. France and Zambia maintain bilateral diplomatic "
            "relations. French death certificates (acte de deces, in French) "
            "require certified English translation and authentication by the "
            "Zambian Embassy in Paris. Zambia is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "English is Zambia's official language. "
            "(Zambia Registrar General's Office, 2025.)"
        ),
    },
    # R68 -- Sudan x5
    {
        'origin': 'united-kingdom', 'dest': 'sudan',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Sudan include individuals with family ties, "
            "aid workers, and journalists. The British Embassy in Khartoum "
            "suspended operations in April 2023 following the outbreak of "
            "armed conflict. Consular assistance for British nationals in "
            "Sudan is provided through the British Embassy in Nairobi, Kenya, "
            "or the FCDO on +44 (0)20 7008 5000. Khartoum International "
            "Airport (KRT) has had extremely limited operations since April "
            "2023; Port Sudan Airport (PZU) is the main functioning gateway. "
            "British death certificates require certified Arabic translation. "
            "Sudan is not a Hague Apostille Convention member. Repatriation "
            "from Sudan requires a specialist with current operational contacts. "
            "(FCDO Travel Advice: Sudan, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'sudan',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Sudan include individuals with family ties, aid "
            "workers, and journalists. The US Embassy in Khartoum suspended "
            "operations in April 2023. Consular assistance for US nationals "
            "in Sudan is provided through the US Embassy in Nairobi or the "
            "US State Department emergency line on +1 888 407 4747. Khartoum "
            "International Airport (KRT) has had extremely limited operations "
            "since April 2023; Port Sudan Airport (PZU) is the main functioning "
            "gateway. English-language US death certificates require certified "
            "Arabic translation. Sudan is not a Hague Apostille Convention "
            "member. Repatriation requires a specialist with current operational "
            "contacts. "
            "(US State Department, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'sudan',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Sudan include development workers and "
            "individuals with bilateral ties. The German Embassy in Khartoum "
            "suspended operations in April 2023. Consular assistance for "
            "German nationals in Sudan is provided through the German Embassy "
            "in Nairobi or the German Foreign Office on +49 30 5000 2000. "
            "Port Sudan Airport (PZU) is the main functioning entry and exit "
            "point. German death certificates (Sterbeurkunde, in German) "
            "require certified Arabic translation. Sudan is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. Repatriation from Sudan requires a specialist with "
            "current operational contacts. "
            "(German Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'egypt', 'dest': 'sudan',
        'embassy_city': 'Cairo',
        'intro': (
            "Egyptian nationals in Sudan include business professionals and "
            "individuals with close bilateral ties reflecting Egypt's shared "
            "border with Sudan. The Egyptian Embassy in Khartoum has had "
            "limited operations since April 2023. Repatriation between Sudan "
            "and Egypt can be arranged via Port Sudan and overland or via "
            "regional airports as conditions allow. Arabic is the official "
            "language of both countries; Egyptian death certificates (shahadat "
            "al-wafah, in Arabic) may be accepted with authentication by the "
            "Sudanese Embassy in Cairo. Sudan is not a Hague Apostille "
            "Convention member. Families should contact the Egyptian Ministry "
            "of Foreign Affairs for current guidance. "
            "(Egyptian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'sudan',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Sudan include development workers and "
            "individuals with bilateral ties. The French Embassy in Khartoum "
            "suspended operations in April 2023. Consular assistance for "
            "French nationals in Sudan is provided through the French Embassy "
            "in Nairobi or the French Ministry of Foreign Affairs crisis line "
            "on +33 1 43 17 67 67. Port Sudan Airport (PZU) is the main "
            "functioning exit point. French death certificates (acte de deces, "
            "in French) require certified Arabic translation. Sudan is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. Repatriation from Sudan requires a specialist with "
            "current operational contacts. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R68 -- Somalia x5
    {
        'origin': 'united-kingdom', 'dest': 'somalia',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Somalia include individuals with family ties, "
            "aid workers, and a small number of journalists. The FCDO advises "
            "against all travel to Somalia. There is no permanent British Embassy "
            "in Mogadishu; limited consular support is provided through the "
            "British Embassy in Nairobi, Kenya. Families should contact the FCDO "
            "on +44 (0)20 7008 5000 immediately after a death. British death "
            "certificates require certified Somali or Arabic translation. Somalia "
            "is not a Hague Apostille Convention member. Repatriation from "
            "Somalia requires a specialist with current operational contacts. "
            "(FCDO Travel Advice: Somalia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'somalia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Somalia include individuals with family ties "
            "and a small number of aid workers. The German Embassy does not "
            "maintain a permanent presence in Mogadishu; consular matters are "
            "handled through the German Embassy in Nairobi. German death "
            "certificates (Sterbeurkunde, in German) require certified Somali "
            "or Arabic translation. Somalia is not a Hague Apostille Convention "
            "member; full consular authentication is required. Repatriation "
            "from Somalia requires a specialist with current operational contacts; "
            "the German Foreign Office advises against all travel to Somalia. "
            "(German Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'somalia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in Somalia include a significant Somali-Swedish "
            "diaspora community visiting relatives, particularly in Mogadishu "
            "and Hargeisa. Sweden does not maintain a resident Embassy in "
            "Mogadishu; consular matters are handled through the Swedish Embassy "
            "in Nairobi. Swedish death certificates (dodsfallsintyg, in Swedish) "
            "require certified Somali or Arabic translation. Somalia is not a "
            "Hague Apostille Convention member; full consular authentication is "
            "required. Repatriation from Somalia requires a specialist with "
            "current operational contacts. "
            "(Swedish Ministry for Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'somalia',
        'embassy_city': 'Oslo',
        'intro': (
            "Norwegian nationals in Somalia include individuals with family "
            "ties and a small number of aid workers. Norway does not maintain "
            "a resident Embassy in Mogadishu; consular matters are handled "
            "through the Norwegian Embassy in Nairobi. Norwegian death "
            "certificates (dodsattest, in Norwegian) require certified Somali "
            "or Arabic translation. Somalia is not a Hague Apostille Convention "
            "member; full consular authentication is required. Repatriation "
            "from Somalia requires a specialist with current operational contacts. "
            "(Norwegian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'somalia',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Somalia include individuals with family ties and "
            "a small number of aid workers. The US Embassy in Mogadishu "
            "operates with significant security restrictions; contact the US "
            "State Department on +1 888 407 4747 immediately after a death. "
            "English-language US death certificates require certified Somali "
            "or Arabic translation. Somalia is not a Hague Apostille Convention "
            "member. Repatriation from Somalia requires a specialist with "
            "current operational contacts; the US State Department advises "
            "against all travel to Somalia. "
            "(US State Department, 2025.)"
        ),
    },
    # R68 -- Bosnia x5
    {
        'origin': 'united-kingdom', 'dest': 'bosnia-and-herzegovina',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Bosnia and Herzegovina include tourists, "
            "development workers, and individuals with connections from the "
            "1990s Balkan conflicts. The British Embassy in Sarajevo can "
            "assist British nationals after a death. British death certificates "
            "require certified translation into Bosnian, Croatian, or Serbian "
            "and authentication by the Bosnian Embassy in London. Bosnia and "
            "Herzegovina joined the Hague Apostille Convention in 2008; "
            "apostille certificates are accepted for UK-issued documents. "
            "(FCDO Travel Advice: Bosnia and Herzegovina, 2025; Bosnia and "
            "Herzegovina Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'bosnia-and-herzegovina',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Bosnia and Herzegovina include a substantial "
            "diaspora community and business professionals, reflecting decades "
            "of bilateral ties. The German Embassy in Sarajevo is operational. "
            "German death certificates (Sterbeurkunde, in German) require "
            "certified translation into Bosnian, Croatian, or Serbian and "
            "authentication by the Bosnian Embassy in Berlin. Bosnia and "
            "Herzegovina joined the Hague Apostille Convention in 2008; "
            "apostille certificates are accepted for German documents. "
            "(Bosnia and Herzegovina Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'austria', 'dest': 'bosnia-and-herzegovina',
        'embassy_city': 'Vienna',
        'intro': (
            "Austrian nationals in Bosnia and Herzegovina include a significant "
            "diaspora community and business professionals, reflecting Austria's "
            "geographical proximity and historical relationship with the Western "
            "Balkans. The Austrian Embassy in Sarajevo is operational. Austrian "
            "death certificates (Sterbeurkunde, in German) require certified "
            "translation into Bosnian, Croatian, or Serbian and authentication "
            "by the Bosnian Embassy in Vienna. Bosnia and Herzegovina joined "
            "the Hague Apostille Convention in 2008; apostille certificates "
            "are accepted for Austrian documents. "
            "(Bosnia and Herzegovina Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'bosnia-and-herzegovina',
        'embassy_city': 'Stockholm',
        'intro': (
            "Swedish nationals in Bosnia and Herzegovina include a significant "
            "Bosnian diaspora community, particularly following the 1990s "
            "conflict. Sweden does not maintain a resident Embassy in Sarajevo; "
            "consular matters for Swedish nationals in Bosnia and Herzegovina "
            "are handled through the Swedish Embassy in Zagreb, Croatia. "
            "Swedish death certificates (dodsfallsintyg, in Swedish) require "
            "certified translation into Bosnian, Croatian, or Serbian and "
            "authentication by the Bosnian Embassy in Stockholm. Bosnia and "
            "Herzegovina joined the Hague Apostille Convention in 2008. "
            "(Swedish Ministry for Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'bosnia-and-herzegovina',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Bosnia and Herzegovina include individuals "
            "with bilateral ties and development workers. The French Embassy "
            "in Sarajevo is operational. French death certificates (acte de "
            "deces, in French) require certified translation into Bosnian, "
            "Croatian, or Serbian and authentication by the Bosnian Embassy "
            "in Paris. Bosnia and Herzegovina joined the Hague Apostille "
            "Convention in 2008; apostille certificates are accepted for "
            "French documents. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R68 -- Serbia x5
    {
        'origin': 'united-kingdom', 'dest': 'serbia',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Serbia include tourists, business "
            "professionals, and individuals with bilateral ties. The British "
            "Embassy in Belgrade can assist British nationals after a death. "
            "British death certificates require certified Serbian translation "
            "and authentication by the Serbian Embassy in London. Serbia has "
            "been a Hague Apostille Convention member since 2001; apostille "
            "certificates are accepted for UK-issued documents. Serbian, "
            "written in Cyrillic and Latin scripts, is the official language. "
            "(FCDO Travel Advice: Serbia, 2025; Serbian Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'serbia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Serbia include business professionals and "
            "a significant Serbian diaspora community reflecting decades of "
            "migration. The German Embassy in Belgrade is operational. German "
            "death certificates (Sterbeurkunde, in German) require certified "
            "Serbian translation and authentication by the Serbian Embassy in "
            "Berlin. Serbia has been a Hague Apostille Convention member since "
            "2001; apostille certificates are accepted for German documents. "
            "(Serbian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'austria', 'dest': 'serbia',
        'embassy_city': 'Vienna',
        'intro': (
            "Austrian nationals in Serbia include business professionals and "
            "a Serbian diaspora community with close bilateral ties reflecting "
            "Austria's geographical proximity and historical relationship with "
            "Serbia. The Austrian Embassy in Belgrade is operational. Austrian "
            "death certificates (Sterbeurkunde, in German) require certified "
            "Serbian translation and authentication by the Serbian Embassy in "
            "Vienna. Serbia has been a Hague Apostille Convention member since "
            "2001; apostille certificates are accepted for Austrian documents. "
            "(Serbian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'serbia',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Serbia include business professionals and "
            "individuals with bilateral ties. The French Embassy in Belgrade "
            "is operational. French death certificates (acte de deces, in "
            "French) require certified Serbian translation and authentication "
            "by the Serbian Embassy in Paris. Serbia has been a Hague Apostille "
            "Convention member since 2001; apostille certificates are accepted "
            "for French documents. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'serbia',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Serbia include business professionals, researchers, "
            "and tourists. The US Embassy in Belgrade can assist US nationals "
            "after a death. English-language US death certificates require "
            "certified Serbian translation and authentication by the Serbian "
            "Embassy in Washington DC. Serbia has been a Hague Apostille "
            "Convention member since 2001; apostille certificates are accepted "
            "for US-issued documents. "
            "(Serbian Ministry of Foreign Affairs, 2025.)"
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
    emergency_line = dm['emergency_line']

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
