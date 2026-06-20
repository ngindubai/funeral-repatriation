#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R71-R72.

   R71 (25 routes, variants B,C,D,E,A x5):
     Mauritius x5:         united-kingdom, france, germany, australia, italy
     Georgia x5:           united-kingdom, united-states, germany, france, netherlands
     Albania x5:           united-kingdom, germany, italy, united-states, france
     Dominican Republic x5: united-kingdom, united-states, germany, canada, spain
     Maldives x5:          united-kingdom, united-states, germany, france, australia

   R72 (25 routes, variants B,C,D,E,A x5):
     Cambodia x5:   united-kingdom, united-states, australia, france, germany
     Estonia x5:    united-kingdom, germany, finland, sweden, united-states
     Latvia x5:     united-kingdom, germany, sweden, finland, united-states
     Slovakia x5:   united-kingdom, germany, austria, united-states, france
     Slovenia x5:   united-kingdom, germany, italy, austria, united-states

   Template rotation: R70 ended A (index 0). R71 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R72 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'mauritius': {
        'name': 'Mauritius',
        'slug': 'mauritius',
        'key': 'mu',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-4 weeks',
        'timeline_complex_override': '8-14 weeks',
        'reception': (
            "The Mauritian funeral director takes custody at Sir Seewoosagur "
            "Ramgoolam International Airport (MRU) cargo terminal at Plaisance. "
            "Death registration in Mauritius is handled by the Civil Status "
            "Division, which falls under the Ministry of Health and Wellness. "
            "Death certificates are issued in English and French, both official "
            "languages. Mauritius joined the Hague Apostille Convention in 2006; "
            "apostille certificates from member states are accepted for relevant "
            "documents. Mauritius is a Commonwealth member. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(Civil Status Division, Mauritius, 2025; FCDO Travel "
            "Advice: Mauritius, 2025.)"
        ),
        'consular_template': (
            "The Mauritius High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Mauritius. Mauritius "
            "joined the Hague Apostille Convention in 2006. The High Commission "
            "cannot pay for or arrange repatriation. Contact the Civil Status "
            "Division in Mauritius for civil registration queries."
        ),
        'arrival_faq': (
            "The Mauritian funeral director takes custody at Sir Seewoosagur "
            "Ramgoolam International Airport (MRU) cargo terminal. The Civil "
            "Status Division, under the Ministry of Health and Wellness, "
            "registers the death and issues a death certificate in English "
            "and French. Mauritius joined the Hague Apostille Convention in "
            "2006; apostille certificates from member states are accepted. "
            "Mauritius is a Commonwealth member; English is used throughout "
            "the administration process. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Mauritius High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-mauritius',
    },
    'georgia': {
        'name': 'Georgia',
        'slug': 'georgia',
        'key': 'ge',
        'reception': (
            "The Georgian funeral director takes custody at Tbilisi "
            "International Airport (TBS) or Batumi International Airport "
            "(BUS) cargo terminal. Death registration in Georgia is handled "
            "by the Public Services Development Agency (PSDA), which operates "
            "Justice House civil registry offices across the country. The "
            "death certificate (sikvdilis sabuTi) is issued in Georgian "
            "(Mkhedruli script); foreign documents require certified Georgian "
            "translation. Georgia joined the Hague Apostille Convention in "
            "2007; apostille certificates from member states are accepted. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Public Services Development Agency (PSDA), Georgia, 2025; "
            "FCDO Travel Advice: Georgia, 2025.)"
        ),
        'consular_template': (
            "The Georgian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Georgia. Georgia "
            "joined the Hague Apostille Convention in 2007. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Public "
            "Services Development Agency (PSDA) in Georgia for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Georgian funeral director takes custody at Tbilisi "
            "International Airport (TBS) or Batumi International Airport "
            "(BUS) cargo terminal. The Public Services Development Agency "
            "(PSDA) operates Justice House civil registry offices, which "
            "register the death and issue the sikvdilis sabuTi (death "
            "certificate) in Georgian. Foreign documents require certified "
            "Georgian translation before submission to the PSDA. Georgia "
            "joined the Hague Apostille Convention in 2007; apostille "
            "certificates from member states are accepted. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Georgian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-georgia',
    },
    'albania': {
        'name': 'Albania',
        'slug': 'albania',
        'key': 'al',
        'reception': (
            "The Albanian funeral director takes custody at Tirana "
            "International Airport Nene Tereza (TIA) cargo terminal. "
            "Death registration in Albania is handled by the Zyrja e "
            "Gjendjes Civile (Office of Civil Status) within the local "
            "bashkia (municipality), under the Directorate of Civil Status "
            "(DSHC). Death certificates are issued in Albanian; all foreign "
            "documents require certified Albanian translation. Albania joined "
            "the Hague Apostille Convention in 2007; apostille certificates "
            "from member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Directorate of Civil Status (DSHC), Albania, 2025; FCDO "
            "Travel Advice: Albania, 2025.)"
        ),
        'consular_template': (
            "The Albanian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Albania. Albania "
            "joined the Hague Apostille Convention in 2007. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Directorate "
            "of Civil Status (DSHC) in Albania for civil registration queries."
        ),
        'arrival_faq': (
            "The Albanian funeral director takes custody at Tirana "
            "International Airport Nene Tereza (TIA) cargo terminal. The "
            "Zyrja e Gjendjes Civile (Office of Civil Status) within the "
            "local bashkia (municipality) registers the death and issues the "
            "death certificate in Albanian. All foreign documents require "
            "certified Albanian translation before submission to Albanian "
            "authorities. Albania joined the Hague Apostille Convention in "
            "2007; apostille certificates from member states are accepted. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports."
        ),
        'emergency_line': 'contact the Albanian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-albania',
    },
    'dominican-republic': {
        'name': 'the Dominican Republic',
        'slug': 'dominican-republic',
        'key': 'do',
        'short_title': 'Dominican Republic',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-14 weeks',
        'reception': (
            "The Dominican funeral director takes custody at Las Americas "
            "International Airport (SDQ) in Santo Domingo or Punta Cana "
            "International Airport (PUJ) cargo terminal. Death registration "
            "in the Dominican Republic is handled by the Junta Central "
            "Electoral (JCE), the civil registry authority. Death certificates "
            "are issued in Spanish; foreign documents require certified "
            "Spanish translation. The Dominican Republic joined the Hague "
            "Apostille Convention in 2009; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Junta Central Electoral (JCE), Dominican Republic, 2025; "
            "FCDO Travel Advice: Dominican Republic, 2025.)"
        ),
        'consular_template': (
            "The Dominican Republic Embassy or Consulate in {city} can "
            "advise on documentation requirements for repatriation to the "
            "Dominican Republic. The Dominican Republic joined the Hague "
            "Apostille Convention in 2009. The Embassy cannot pay for or "
            "arrange repatriation. Contact the Junta Central Electoral "
            "(JCE) for civil registration queries."
        ),
        'arrival_faq': (
            "The Dominican funeral director takes custody at Las Americas "
            "International Airport (SDQ) or Punta Cana International "
            "Airport (PUJ) cargo terminal. The Junta Central Electoral "
            "(JCE) is the civil registry authority; it registers the death "
            "and issues the death certificate in Spanish. Foreign documents "
            "require certified Spanish translation. The Dominican Republic "
            "joined the Hague Apostille Convention in 2009; apostille "
            "certificates from member states are accepted. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Dominican Republic Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-dominican-republic',
    },
    'maldives': {
        'name': 'the Maldives',
        'slug': 'maldives',
        'key': 'mv',
        'short_title': 'Maldives',
        'complexity_override': 'high',
        'timeline_avg_override': '3-7 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '10-16 weeks',
        'reception': (
            "The Maldivian funeral director or island authority takes "
            "custody at Velana International Airport (MLE) in Male cargo "
            "terminal. Deaths on outer island resorts require inter-island "
            "transfer to Male by speedboat or seaplane before any air "
            "repatriation can begin. Death registration is handled by the "
            "National Registration Authority (NRA); deaths on outer atolls "
            "are registered with the Atoll Council. Death certificates are "
            "issued in Dhivehi (Thaana script); English translations are "
            "widely available but must be certified. The Maldives is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required for all foreign documents. Islamic law applies for "
            "Muslim remains; embalming and burial must respect religious "
            "requirements. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(National Registration Authority (NRA), Maldives, 2025; FCDO "
            "Travel Advice: Maldives, 2025.)"
        ),
        'consular_template': (
            "The Maldivian High Commission or Embassy nearest to {city} "
            "can advise on documentation requirements for repatriation to "
            "the Maldives. The Maldives is not a Hague Apostille Convention "
            "member; full consular authentication is required. The High "
            "Commission cannot pay for or arrange repatriation. Contact "
            "the National Registration Authority (NRA) in Maldives for "
            "civil registration queries."
        ),
        'arrival_faq': (
            "The Maldivian funeral director takes custody at Velana "
            "International Airport (MLE) cargo terminal in Male. For "
            "deaths on outer atolls, inter-island transfer to Male is "
            "required before international repatriation can proceed. "
            "The National Registration Authority (NRA) registers the "
            "death; deaths on outer atolls are initially registered with "
            "the Atoll Council. Death certificates are issued in Dhivehi; "
            "certified English translations are obtainable but take time. "
            "The Maldives is not a Hague Apostille Convention member; "
            "full consular authentication is required. Islamic law applies "
            "for Muslim remains. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Maldivian High Commission or Embassy in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-maldives',
    },
    'cambodia': {
        'name': 'Cambodia',
        'slug': 'cambodia',
        'key': 'kh',
        'complexity_override': 'high',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-14 weeks',
        'reception': (
            "The Cambodian funeral director takes custody at Phnom Penh "
            "International Airport (PNH) or Siem Reap International "
            "Airport (REP) cargo terminal. Death registration in Cambodia "
            "is handled by the Ministry of Interior via the commune or "
            "sangkat (sub-district) civil registry. Death certificates are "
            "issued in Khmer; all foreign documents require certified Khmer "
            "translation. Cambodia is not a Hague Apostille Convention "
            "member; full consular authentication of all foreign documents "
            "is required by Cambodian authorities. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(Ministry of Interior, Kingdom of Cambodia, 2025; FCDO "
            "Travel Advice: Cambodia, 2025.)"
        ),
        'consular_template': (
            "The Royal Embassy of Cambodia in {city} can advise on "
            "documentation requirements for repatriation to Cambodia. "
            "Cambodia is not a Hague Apostille Convention member; full "
            "consular authentication is required. The Embassy cannot pay "
            "for or arrange repatriation. Contact the Ministry of Interior "
            "commune registry in Cambodia for civil registration queries."
        ),
        'arrival_faq': (
            "The Cambodian funeral director takes custody at Phnom Penh "
            "International Airport (PNH) or Siem Reap International "
            "Airport (REP) cargo terminal. The Ministry of Interior handles "
            "civil registration through the commune or sangkat (sub-district) "
            "civil registry; death certificates are issued in Khmer. All "
            "foreign documents require certified Khmer translation before "
            "submission to Cambodian authorities. Cambodia is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Royal Embassy of Cambodia in the origin country',
        'hub_url': 'repatriation-from-cambodia',
    },
    'estonia': {
        'name': 'Estonia',
        'slug': 'estonia',
        'key': 'ee',
        'reception': (
            "The Estonian funeral director takes custody at Lennart Meri "
            "Tallinn Airport (TLL) cargo terminal. Death registration in "
            "Estonia is handled by the Population Register Centre "
            "(Rahvastikuregister), which is administered by the Ministry "
            "of the Interior; deaths are registered at the local "
            "omavalitsus (local government office). Death certificates "
            "are issued in Estonian; foreign documents require certified "
            "Estonian translation. Estonia joined the Hague Apostille "
            "Convention in 2001; apostille certificates from member states "
            "are accepted. Estonia is an EU member. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Population Register Centre (Rahvastikuregister), Estonia, "
            "2025; FCDO Travel Advice: Estonia, 2025.)"
        ),
        'consular_template': (
            "The Estonian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Estonia. "
            "Estonia joined the Hague Apostille Convention in 2001. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the Population Register Centre (Rahvastikuregister) in "
            "Estonia for civil registration queries."
        ),
        'arrival_faq': (
            "The Estonian funeral director takes custody at Lennart Meri "
            "Tallinn Airport (TLL) cargo terminal. The Population Register "
            "Centre (Rahvastikuregister), administered by the Ministry of "
            "the Interior, registers the death; deaths are handled at the "
            "local omavalitsus (local government office) and the certificate "
            "is issued in Estonian. Foreign documents require certified "
            "Estonian translation. Estonia joined the Hague Apostille "
            "Convention in 2001; apostille certificates from member states "
            "are accepted. Estonia is an EU member. An embalming certificate "
            "and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Estonian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-estonia',
    },
    'latvia': {
        'name': 'Latvia',
        'slug': 'latvia',
        'key': 'lv',
        'reception': (
            "The Latvian funeral director takes custody at Riga "
            "International Airport (RIX) cargo terminal. Death "
            "registration in Latvia is handled by the local dzimtsarakstu "
            "nodala (civil registry department), administered by the "
            "Office of Citizenship and Migration Affairs (PMLP) under "
            "the Ministry of the Interior. Death certificates are issued "
            "in Latvian; foreign documents require certified Latvian "
            "translation. Latvia joined the Hague Apostille Convention "
            "in 1996; apostille certificates from member states are "
            "accepted. Latvia is an EU member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(Office of Citizenship and Migration Affairs (PMLP), "
            "Latvia, 2025; FCDO Travel Advice: Latvia, 2025.)"
        ),
        'consular_template': (
            "The Latvian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Latvia. "
            "Latvia joined the Hague Apostille Convention in 1996. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the Office of Citizenship and Migration Affairs (PMLP) in "
            "Latvia for civil registration queries."
        ),
        'arrival_faq': (
            "The Latvian funeral director takes custody at Riga "
            "International Airport (RIX) cargo terminal. The local "
            "dzimtsarakstu nodala (civil registry department), "
            "administered by the Office of Citizenship and Migration "
            "Affairs (PMLP), registers the death and issues a "
            "death certificate in Latvian. Foreign documents require "
            "certified Latvian translation. Latvia joined the Hague "
            "Apostille Convention in 1996; apostille certificates from "
            "member states are accepted. Latvia is an EU member. "
            "An embalming certificate and hermetically sealed coffin "
            "are required."
        ),
        'emergency_line': 'contact the Latvian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-latvia',
    },
    'slovakia': {
        'name': 'Slovakia',
        'slug': 'slovakia',
        'key': 'sk',
        'reception': (
            "The Slovak funeral director takes custody at Milan Rastislav "
            "Stefanik Airport Bratislava (BTS) cargo terminal; some "
            "families also route via Vienna International Airport (VIE), "
            "approximately 60 kilometres from Bratislava. Death "
            "registration in Slovakia is handled by the local matrika "
            "(civil registry office) at the obecny urad (municipal "
            "office) or mestsky urad (city office). Death certificates "
            "are issued in Slovak; foreign documents require certified "
            "Slovak translation. Slovakia joined the Hague Apostille "
            "Convention in 2002; apostille certificates from member "
            "states are accepted. Slovakia is an EU member. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Ministry of Interior Civil Registry Division (Matriky), "
            "Slovakia, 2025; FCDO Travel Advice: Slovakia, 2025.)"
        ),
        'consular_template': (
            "The Slovak Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Slovakia. "
            "Slovakia joined the Hague Apostille Convention in 2002. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the Ministry of Interior Civil Registry Division (Matriky) "
            "in Slovakia for civil registration queries."
        ),
        'arrival_faq': (
            "The Slovak funeral director takes custody at Milan Rastislav "
            "Stefanik Airport Bratislava (BTS) cargo terminal, or via "
            "Vienna International Airport (VIE) for families travelling "
            "through Austria. The local matrika (civil registry office) "
            "at the obecny urad or mestsky urad registers the death and "
            "issues a certificate in Slovak. Foreign documents require "
            "certified Slovak translation. Slovakia joined the Hague "
            "Apostille Convention in 2002; apostille certificates from "
            "member states are accepted. Slovakia is an EU member. "
            "An embalming certificate and hermetically sealed coffin "
            "are required."
        ),
        'emergency_line': 'contact the Slovak Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-slovakia',
    },
    'slovenia': {
        'name': 'Slovenia',
        'slug': 'slovenia',
        'key': 'si',
        'reception': (
            "The Slovenian funeral director takes custody at Ljubljana "
            "Joze Pucnik Airport (LJU) cargo terminal. Death registration "
            "in Slovenia is handled by the local maticni urad (civil "
            "registry office) at the upravna enota (administrative unit). "
            "Death certificates are issued in Slovenian; foreign documents "
            "require certified Slovenian translation. Slovenia joined the "
            "Hague Apostille Convention in 1992; apostille certificates "
            "from member states are accepted. Slovenia is an EU member. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Administrative Unit (Upravna enota), Slovenia, 2025; FCDO "
            "Travel Advice: Slovenia, 2025.)"
        ),
        'consular_template': (
            "The Slovenian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Slovenia. "
            "Slovenia joined the Hague Apostille Convention in 1992. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the local maticni urad (civil registry) via the upravna "
            "enota (administrative unit) in Slovenia for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Slovenian funeral director takes custody at Ljubljana "
            "Joze Pucnik Airport (LJU) cargo terminal. The local "
            "maticni urad (civil registry office) at the upravna enota "
            "(administrative unit) registers the death and issues a "
            "death certificate in Slovenian. Foreign documents require "
            "certified Slovenian translation. Slovenia joined the Hague "
            "Apostille Convention in 1992; apostille certificates from "
            "member states are accepted. Slovenia is an EU member. "
            "An embalming certificate and hermetically sealed coffin "
            "are required."
        ),
        'emergency_line': 'contact the Slovenian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-slovenia',
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
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
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
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Italy is available, though less common than in northern "
            "Europe; facilities exist in major cities."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Procura della Repubblica)',
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
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in the Netherlands is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Officier van Justitie)',
    },
    'spain': {
        'name': 'Spain',
        'emergency': '112',
        'registry': 'the local Registro Civil (civil registry)',
        'cert_name': 'certificado de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The certificado de defuncion is registered with the local Registro "
            "Civil (civil registry). The Fiscal (public prosecutor) takes "
            "jurisdiction for violent or unexplained deaths. Spain is an EU "
            "member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Spain is available, with facilities in major cities "
            "and tourist areas."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Fiscal, public prosecutor takes jurisdiction)',
    },
    'sweden': {
        'name': 'Sweden',
        'emergency': '112',
        'registry': 'Skatteverket (the Swedish Tax Agency)',
        'cert_name': 'dodsfallsintyg (death notification certificate)',
        'cert_lang': 'Swedish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The dodsfallsintyg (death notification certificate) is issued by "
            "Skatteverket (the Swedish Tax Agency), which maintains the population "
            "register. Police and the Riksaklagaren (public prosecutor) take "
            "jurisdiction for violent or unexplained deaths. Sweden is an EU "
            "member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Sweden is widely available and is the most common "
            "method of disposition."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (police and Riksaklagaren, public prosecutor takes jurisdiction)',
    },
    'finland': {
        'name': 'Finland',
        'emergency': '112',
        'registry': 'the Digi- and Population Data Services Agency (DVV)',
        'cert_name': 'kuolintodistus (death certificate)',
        'cert_lang': 'Finnish or Swedish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The kuolintodistus (death certificate) is registered with the Digi- "
            "and Population Data Services Agency (DVV). Police and the syyttaja "
            "(public prosecutor) take jurisdiction for violent or unexplained "
            "deaths. Finland is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Finland is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (syyttaja, public prosecutor takes jurisdiction)',
    },
}

ROUTES = [
    # R71 -- Mauritius x5
    {
        'origin': 'united-kingdom', 'dest': 'mauritius',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom and Mauritius share a history stretching from "
            "British Crown Colony status until Mauritian independence in 1968. "
            "Mauritius has remained a Commonwealth member and a popular destination "
            "for British honeymooners, retirees, and business travellers. When "
            "someone from the United Kingdom dies and their family wishes to "
            "repatriate remains to Mauritius, the death must be registered at the "
            "local register office in England and Wales within 5 days, or with "
            "the National Records of Scotland or GRONI in Northern Ireland. The "
            "Mauritius High Commission in London can authenticate documents for "
            "the Civil Status Division. UK death certificates require no translation "
            "as English is an official language in Mauritius. Mauritius joined the "
            "Hague Apostille Convention in 2006. "
            "(FCDO Travel Advice: Mauritius, 2025; Civil Status Division, "
            "Mauritius, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'mauritius',
        'embassy_city': 'Paris',
        'intro': (
            "Mauritius was a French colony from 1715 until 1810, and French "
            "remains a language of culture and commerce alongside English. The "
            "Franco-Mauritian community maintains close ties with France. When a "
            "Mauritian national or a person with Mauritian family connections dies "
            "in France, the death is registered with the local mairie (town hall). "
            "The acte de deces is issued in French and requires no translation for "
            "submission to Mauritian authorities, as French is an official language. "
            "The Embassy of Mauritius in Paris can advise on documentation "
            "requirements for the Civil Status Division. Mauritius joined the "
            "Hague Apostille Convention in 2006; French-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Mauritius, 2025; Civil Status Division, "
            "Mauritius, 2025; French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'mauritius',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a small but growing expat and business community in "
            "Mauritius, attracted by the island's offshore financial sector and "
            "business environment. When a German national with Mauritian connections "
            "dies in Germany and their family wishes to repatriate remains to "
            "Mauritius, the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde is issued in German and requires certified "
            "English or French translation for Mauritian authorities. The Embassy "
            "of Mauritius in Berlin can advise on documentation requirements for "
            "the Civil Status Division. Mauritius joined the Hague Apostille "
            "Convention in 2006; German-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Mauritius, 2025; Civil Status Division, "
            "Mauritius, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'mauritius',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Mauritius share Commonwealth ties, and the "
            "Mauritian-Australian community is concentrated in Melbourne and "
            "Sydney. When a Mauritian national or a person with Mauritian "
            "connections dies in Australia and their family wishes to repatriate "
            "remains to Mauritius, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. The death "
            "certificate is issued in English and requires no translation for "
            "Mauritian authorities. The Mauritius High Commission in Canberra "
            "can advise on documentation requirements for the Civil Status "
            "Division. Mauritius joined the Hague Apostille Convention in 2006; "
            "Australian-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Mauritius, 2025; Civil Status Division, "
            "Mauritius, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'mauritius',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a small community of nationals working in Mauritius, "
            "particularly in the hospitality and luxury tourism sectors. When an "
            "Italian national with Mauritian connections dies in Italy and their "
            "family wishes to repatriate remains to Mauritius, the death is "
            "registered with the local Ufficio di Stato Civile (civil registry). "
            "The atto di morte is issued in Italian and requires certified English "
            "or French translation for submission to Mauritian authorities. The "
            "Embassy of Mauritius in Rome can advise on documentation requirements "
            "for the Civil Status Division. Mauritius joined the Hague Apostille "
            "Convention in 2006; Italian-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Mauritius, 2025; Civil Status Division, "
            "Mauritius, 2025.)"
        ),
    },
    # R71 -- Georgia x5
    {
        'origin': 'united-kingdom', 'dest': 'georgia',
        'embassy_city': 'London',
        'intro': (
            "Georgia has become an increasingly popular destination for British "
            "travellers, and a growing hub for British entrepreneurs drawn by "
            "the country's liberal visa policy and emerging business culture. "
            "When someone from the United Kingdom dies and their family wishes "
            "to repatriate remains to Georgia, the death must be registered at "
            "the local register office in England and Wales within 5 days, or "
            "with the National Records of Scotland or GRONI in Northern Ireland. "
            "The Georgian Embassy in London can advise on documentation "
            "requirements for the Public Services Development Agency (PSDA). "
            "UK death certificates require certified Georgian translation. Georgia "
            "joined the Hague Apostille Convention in 2007. "
            "(FCDO Travel Advice: Georgia, 2025; Public Services Development "
            "Agency (PSDA), Georgia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'georgia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a sizeable Georgian diaspora community, "
            "concentrated in New York, New Jersey, and California, with cultural "
            "ties maintained through the Georgian Orthodox Church and community "
            "associations. When a Georgian national or a person of Georgian "
            "heritage dies in the United States, the death is registered with "
            "the state civil records office where the death occurred. The Embassy "
            "of Georgia in Washington DC can advise on documentation requirements "
            "for the Public Services Development Agency (PSDA). US death "
            "certificates require certified Georgian translation. Georgia joined "
            "the Hague Apostille Convention in 2007; US-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Georgia, 2025; Public Services Development "
            "Agency (PSDA), Georgia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'georgia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to one of the largest Georgian diaspora communities "
            "in Western Europe, with tens of thousands of Georgian nationals "
            "living and working there. When a Georgian national dies in Germany "
            "and their family wishes to repatriate remains to Georgia, the death "
            "is registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Georgian "
            "translation for submission to the Public Services Development Agency "
            "(PSDA). The Embassy of Georgia in Berlin can advise on documentation "
            "requirements. Georgia joined the Hague Apostille Convention in 2007; "
            "German-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Georgia, 2025; Public Services Development "
            "Agency (PSDA), Georgia, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'georgia',
        'embassy_city': 'Paris',
        'intro': (
            "France hosts a growing Georgian community, with several thousand "
            "Georgian nationals resident in Paris and other cities. When a "
            "Georgian national dies in France and their family wishes to "
            "repatriate remains to Georgia, the death is registered with the "
            "local mairie (town hall) civil registry. The acte de deces is "
            "issued in French and requires certified Georgian translation for "
            "submission to the Public Services Development Agency (PSDA). "
            "The Embassy of Georgia in Paris can advise on documentation "
            "requirements. Georgia joined the Hague Apostille Convention in "
            "2007; French-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Georgia, 2025; Public Services Development "
            "Agency (PSDA), Georgia, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'georgia',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a small Georgian community, with nationals "
            "working in logistics, hospitality, and the service sector. When "
            "a Georgian national dies in the Netherlands and their family "
            "wishes to repatriate remains to Georgia, the death is registered "
            "with the local gemeente (municipality) civil registry. The akte "
            "van overlijden is issued in Dutch and requires certified Georgian "
            "translation for submission to Tbilisi authorities. The Embassy "
            "of Georgia in The Hague can advise on documentation requirements "
            "for the Public Services Development Agency (PSDA). Georgia joined "
            "the Hague Apostille Convention in 2007; Dutch-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Georgia, 2025; Public Services Development "
            "Agency (PSDA), Georgia, 2025.)"
        ),
    },
    # R71 -- Albania x5
    {
        'origin': 'united-kingdom', 'dest': 'albania',
        'embassy_city': 'London',
        'intro': (
            "Albania has the largest diaspora community in the United Kingdom "
            "among Western Balkan countries. The Albanian-British community has "
            "grown substantially since the 1990s and maintains strong cultural "
            "and family ties. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Albania, the death must be "
            "registered at the local register office in England and Wales within "
            "5 days, or with the National Records of Scotland or GRONI. The "
            "Albanian Embassy in London can advise on documentation requirements "
            "for the Zyrja e Gjendjes Civile (Office of Civil Status). UK death "
            "certificates require certified Albanian translation. Albania joined "
            "the Hague Apostille Convention in 2007. "
            "(FCDO Travel Advice: Albania, 2025; Directorate of Civil Status "
            "(DSHC), Albania, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'albania',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to one of the largest Albanian diaspora communities "
            "outside Albania itself, with hundreds of thousands of Albanian "
            "nationals living and working there. When an Albanian national dies "
            "in Germany and their family wishes to repatriate remains to Albania, "
            "the death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires certified Albanian "
            "translation for submission to the Zyrja e Gjendjes Civile (Office "
            "of Civil Status). The Embassy of Albania in Berlin can advise on "
            "documentation requirements. Albania joined the Hague Apostille "
            "Convention in 2007; German-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Albania, 2025; Directorate of Civil Status "
            "(DSHC), Albania, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'albania',
        'embassy_city': 'Rome',
        'intro': (
            "Italy is home to one of the largest Albanian diaspora communities "
            "in the world, with over 400,000 Albanian nationals resident in "
            "Italy. The geographic proximity between the two countries and regular "
            "ferry services between Vlore or Durres and Bari or Ancona make this "
            "a well-established corridor. When an Albanian national dies in Italy, "
            "the death is registered with the local Ufficio di Stato Civile. The "
            "atto di morte is issued in Italian and requires certified Albanian "
            "translation for submission to the Zyrja e Gjendjes Civile. The "
            "Embassy of Albania in Rome can advise on documentation requirements. "
            "Albania joined the Hague Apostille Convention in 2007. "
            "(FCDO Travel Advice: Albania, 2025; Directorate of Civil Status "
            "(DSHC), Albania, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'albania',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant Albanian diaspora community, "
            "concentrated in New York, New Jersey, and Michigan. When an Albanian "
            "national or a person of Albanian heritage dies in the United States, "
            "the death is registered with the state civil records office where "
            "the death occurred. The Embassy of Albania in Washington DC can "
            "advise on documentation requirements for the Zyrja e Gjendjes "
            "Civile (Office of Civil Status). US death certificates require "
            "certified Albanian translation. Albania joined the Hague Apostille "
            "Convention in 2007; US-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Albania, 2025; Directorate of Civil Status "
            "(DSHC), Albania, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'albania',
        'embassy_city': 'Paris',
        'intro': (
            "France has a growing Albanian diaspora community, with nationals "
            "living and working in Paris and other cities. When an Albanian "
            "national dies in France and their family wishes to repatriate "
            "remains to Albania, the death is registered with the local mairie "
            "(town hall) civil registry. The acte de deces is issued in French "
            "and requires certified Albanian translation for submission to the "
            "Zyrja e Gjendjes Civile (Office of Civil Status). The Embassy "
            "of Albania in Paris can advise on documentation requirements. "
            "Albania joined the Hague Apostille Convention in 2007; "
            "French-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Albania, 2025; Directorate of Civil Status "
            "(DSHC), Albania, 2025.)"
        ),
    },
    # R71 -- Dominican Republic x5
    {
        'origin': 'united-kingdom', 'dest': 'dominican-republic',
        'embassy_city': 'London',
        'intro': (
            "The Dominican Republic is one of the most popular long-haul "
            "holiday destinations for British travellers, with Punta Cana "
            "in particular attracting large numbers of package tourists. When "
            "someone from the United Kingdom dies and their family wishes to "
            "repatriate remains to the Dominican Republic, the death must be "
            "registered at the local register office in England and Wales within "
            "5 days, or with the National Records of Scotland or GRONI. The "
            "Dominican Republic Embassy in London can advise on documentation "
            "requirements for the Junta Central Electoral (JCE) civil registry. "
            "UK death certificates require certified Spanish translation. The "
            "Dominican Republic joined the Hague Apostille Convention in 2009. "
            "(FCDO Travel Advice: Dominican Republic, 2025; Junta Central "
            "Electoral (JCE), Dominican Republic, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'dominican-republic',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has the largest Dominican diaspora community "
            "outside the Dominican Republic itself, concentrated in New York, "
            "New Jersey, and Massachusetts. This is one of the highest-volume "
            "repatriation corridors in the Americas. When a Dominican national "
            "dies in the United States, the death is registered with the state "
            "civil records office where the death occurred. The Embassy of the "
            "Dominican Republic in Washington DC can advise on documentation "
            "requirements for the Junta Central Electoral (JCE). US death "
            "certificates require certified Spanish translation. The Dominican "
            "Republic joined the Hague Apostille Convention in 2009; US-issued "
            "apostille certificates are accepted. "
            "(FCDO Travel Advice: Dominican Republic, 2025; Junta Central "
            "Electoral (JCE), Dominican Republic, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'dominican-republic',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a small Dominican community, with nationals living in "
            "Frankfurt, Hamburg, and other cities. When a Dominican national "
            "dies in Germany and their family wishes to repatriate remains to "
            "the Dominican Republic, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in German "
            "and requires certified Spanish translation for submission to the "
            "Junta Central Electoral (JCE). The Embassy of the Dominican "
            "Republic in Berlin can advise on documentation requirements. The "
            "Dominican Republic joined the Hague Apostille Convention in 2009; "
            "German-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Dominican Republic, 2025; Junta Central "
            "Electoral (JCE), Dominican Republic, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'dominican-republic',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a substantial Dominican diaspora community, particularly "
            "in Toronto and Montreal. The Dominican Republic is also a popular "
            "winter holiday destination for Canadian travellers. When a Dominican "
            "national dies in Canada, the death is registered with the provincial "
            "civil records registry. The Embassy of the Dominican Republic in "
            "Ottawa can advise on documentation requirements for the Junta Central "
            "Electoral (JCE). Canadian death certificates in English or French "
            "require certified Spanish translation. The Dominican Republic joined "
            "the Hague Apostille Convention in 2009; Canadian-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Dominican Republic, 2025; Junta Central "
            "Electoral (JCE), Dominican Republic, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'dominican-republic',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and the Dominican Republic share language, cultural ties, "
            "and historical connections, and the Dominican-Spanish community is "
            "among the largest Latin American diaspora groups in Spain. When a "
            "Dominican national dies in Spain, the death is registered with the "
            "local Registro Civil (civil registry). The certificado de defuncion "
            "is issued in Spanish, which is the official language of both "
            "countries, and requires no translation for Dominican authorities. "
            "The Embassy of the Dominican Republic in Madrid can advise on the "
            "Junta Central Electoral (JCE). The Dominican Republic joined the "
            "Hague Apostille Convention in 2009; Spanish-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Dominican Republic, 2025; Junta Central "
            "Electoral (JCE), Dominican Republic, 2025.)"
        ),
    },
    # R71 -- Maldives x5
    {
        'origin': 'united-kingdom', 'dest': 'maldives',
        'embassy_city': 'London',
        'intro': (
            "The Maldives is one of the United Kingdom's most popular long-haul "
            "destinations, particularly for honeymooners and luxury travellers, "
            "with over 200,000 British visitors annually. The remote island "
            "geography of the country, spanning 26 atolls and over 1,000 coral "
            "islands, creates particular challenges for repatriation. When "
            "someone from the United Kingdom dies and their family wishes to "
            "repatriate remains to the Maldives, the death must be registered "
            "at the local register office in England and Wales within 5 days, "
            "or with the National Records of Scotland or GRONI. The Maldives "
            "High Commission in London can advise on documentation requirements "
            "for the National Registration Authority (NRA). UK death certificates "
            "require certified Dhivehi translation. The Maldives is not a Hague "
            "Apostille Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Maldives, 2025; National Registration "
            "Authority (NRA), Maldives, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'maldives',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Maldives is an increasingly popular destination for American "
            "travellers, particularly for luxury travel and honeymoons. When a "
            "Maldivian national or a person with Maldivian family connections "
            "dies in the United States, the death is registered with the state "
            "civil records office where the death occurred. The Embassy of the "
            "Maldives in Washington DC can advise on documentation requirements "
            "for the National Registration Authority (NRA). US death certificates "
            "require certified Dhivehi translation. The Maldives is not a Hague "
            "Apostille Convention member; full consular authentication of all "
            "documents is required by Maldivian authorities. "
            "(FCDO Travel Advice: Maldives, 2025; National Registration "
            "Authority (NRA), Maldives, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'maldives',
        'embassy_city': 'Brussels',
        'intro': (
            "The Maldives is a popular tourism destination for German visitors, "
            "and a small community of German nationals work in the islands' "
            "hospitality sector. When a Maldivian national dies in Germany and "
            "their family wishes to repatriate remains to the Maldives, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires certified Dhivehi "
            "and English translation for submission to the National Registration "
            "Authority (NRA). The Maldives is not represented by a resident "
            "embassy in Germany; families should contact the Embassy of the "
            "Maldives in Brussels. The Maldives is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Maldives, 2025; National Registration "
            "Authority (NRA), Maldives, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'maldives',
        'embassy_city': 'Paris',
        'intro': (
            "The Maldives is a popular destination for French tourists, "
            "particularly for diving and luxury holidays. When a Maldivian "
            "national or a person with Maldivian connections dies in France "
            "and their family wishes to repatriate remains to the Maldives, "
            "the death is registered with the local mairie (town hall). The "
            "acte de deces is issued in French and requires certified Dhivehi "
            "translation for submission to Maldivian authorities. The Embassy "
            "of the Maldives in Paris can advise on documentation requirements "
            "for the National Registration Authority (NRA). The Maldives is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Maldives, 2025; National Registration "
            "Authority (NRA), Maldives, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'maldives',
        'embassy_city': 'Colombo',
        'intro': (
            "Australian tourists visit the Maldives in significant numbers, "
            "and Australia and the Maldives maintain diplomatic relations "
            "through the Australian High Commission in Colombo, Sri Lanka. "
            "When a Maldivian national or a person with Maldivian connections "
            "dies in Australia and their family wishes to repatriate remains "
            "to the Maldives, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. The death "
            "certificate is issued in English. The Maldives is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required even for English-language documents. The Australian "
            "High Commission in Colombo handles Maldivian consular matters "
            "for Australians in the Maldives. "
            "(FCDO Travel Advice: Maldives, 2025; National Registration "
            "Authority (NRA), Maldives, 2025.)"
        ),
    },
    # R72 -- Cambodia x5
    {
        'origin': 'united-kingdom', 'dest': 'cambodia',
        'embassy_city': 'London',
        'intro': (
            "Cambodia is a growing destination for British backpackers, tourists, "
            "and a small but established expat community, drawn by Angkor Wat "
            "and the country's cultural heritage. When someone from the United "
            "Kingdom dies and their family wishes to repatriate remains to "
            "Cambodia, the death must be registered at the local register office "
            "in England and Wales within 5 days, or with the National Records "
            "of Scotland or GRONI. The Royal Embassy of Cambodia in London can "
            "advise on documentation requirements for the Ministry of Interior "
            "commune-level civil registry (sangkat). UK death certificates "
            "require certified Khmer translation. Cambodia is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Cambodia, 2025; Ministry of Interior, "
            "Kingdom of Cambodia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'cambodia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant Cambodian diaspora community, "
            "concentrated in California, Massachusetts, and Washington State, "
            "with roots in the refugee resettlement following the Khmer Rouge "
            "period. When a Cambodian national or a person of Cambodian heritage "
            "dies in the United States, the death is registered with the state "
            "civil records office. The Embassy of Cambodia in Washington DC "
            "can advise on documentation requirements for the Ministry of "
            "Interior commune registry. US death certificates require certified "
            "Khmer translation. Cambodia is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(FCDO Travel Advice: Cambodia, 2025; Ministry of Interior, "
            "Kingdom of Cambodia, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'cambodia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Cambodian diaspora community of around 50,000, "
            "concentrated in Melbourne and Sydney, with origins in the refugee "
            "resettlement of the 1980s. When a Cambodian national dies in "
            "Australia and their family wishes to repatriate remains to Cambodia, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. The Royal Embassy of Cambodia in "
            "Canberra can advise on documentation requirements. Australian death "
            "certificates require certified Khmer translation for submission to "
            "Cambodian authorities. Cambodia is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(FCDO Travel Advice: Cambodia, 2025; Ministry of Interior, "
            "Kingdom of Cambodia, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'cambodia',
        'embassy_city': 'Paris',
        'intro': (
            "France and Cambodia share a colonial and cultural history through "
            "the French Protectorate of Cambodia (1863 to 1953), and France "
            "hosts a significant Cambodian diaspora community in Paris and Lyon. "
            "When a Cambodian national dies in France and their family wishes to "
            "repatriate remains to Cambodia, the death is registered with the "
            "local mairie (town hall). The acte de deces is issued in French "
            "and requires certified Khmer translation for submission to "
            "Cambodian authorities. The Royal Embassy of Cambodia in Paris "
            "can advise on documentation requirements for the Ministry of "
            "Interior commune registry. Cambodia is not a Hague Apostille "
            "Convention member. "
            "(FCDO Travel Advice: Cambodia, 2025; Ministry of Interior, "
            "Kingdom of Cambodia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'cambodia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a small Cambodian community, with nationals living "
            "in Berlin, Cologne, and other cities. When a Cambodian national "
            "dies in Germany and their family wishes to repatriate remains to "
            "Cambodia, the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde is issued in German and requires "
            "certified Khmer translation for submission to Cambodian authorities. "
            "The Royal Embassy of Cambodia in Berlin can advise on documentation "
            "requirements for the Ministry of Interior commune registry. Cambodia "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Cambodia, 2025; Ministry of Interior, "
            "Kingdom of Cambodia, 2025.)"
        ),
    },
    # R72 -- Estonia x5
    {
        'origin': 'united-kingdom', 'dest': 'estonia',
        'embassy_city': 'London',
        'intro': (
            "Estonia is a popular destination for British tourists, particularly "
            "Tallinn, which draws visitors for city breaks, Christmas markets, "
            "and cultural tourism. The Estonian community in the United Kingdom "
            "has grown considerably since EU accession in 2004. When someone "
            "from the United Kingdom dies and their family wishes to repatriate "
            "remains to Estonia, the death must be registered at the local "
            "register office in England and Wales within 5 days, or with the "
            "National Records of Scotland or GRONI. The Estonian Embassy in "
            "London can advise on documentation requirements for the Population "
            "Register Centre (Rahvastikuregister). UK death certificates require "
            "certified Estonian translation. Estonia joined the Hague Apostille "
            "Convention in 2001. "
            "(FCDO Travel Advice: Estonia, 2025; Population Register Centre "
            "(Rahvastikuregister), Estonia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'estonia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a significant Estonian diaspora community, with nationals "
            "drawn to Berlin and other cities since Estonia joined the European "
            "Union in 2004. When an Estonian national dies in Germany and their "
            "family wishes to repatriate remains to Estonia, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Estonian "
            "translation for submission to the Population Register Centre "
            "(Rahvastikuregister). The Estonian Embassy in Berlin can advise "
            "on documentation requirements. Estonia joined the Hague Apostille "
            "Convention in 2001; German-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Estonia, 2025; Population Register Centre "
            "(Rahvastikuregister), Estonia, 2025.)"
        ),
    },
    {
        'origin': 'finland', 'dest': 'estonia',
        'embassy_city': 'Helsinki',
        'intro': (
            "Finland and Estonia share close historical, cultural, and linguistic "
            "ties, and the ferry route across the Gulf of Finland between Helsinki "
            "and Tallinn is one of the busiest in Europe. The Estonian community "
            "in Finland is large, and many Estonians commute across the Gulf for "
            "work. When an Estonian national dies in Finland, the death is "
            "registered with the Digi- and Population Data Services Agency (DVV). "
            "The kuolintodistus is issued in Finnish or Swedish and requires "
            "certified Estonian translation for submission to the Population "
            "Register Centre. The Estonian Embassy in Helsinki can advise on "
            "documentation requirements. Both countries are EU members and Hague "
            "Apostille Convention members. "
            "(FCDO Travel Advice: Estonia, 2025; Population Register Centre "
            "(Rahvastikuregister), Estonia, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'estonia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a long-established Estonian diaspora community, with roots "
            "stretching back to wartime refugees who fled to Sweden during the "
            "Second World War, and later supplemented by migration since EU "
            "accession. When an Estonian national dies in Sweden, the death is "
            "registered with Skatteverket (the Swedish Tax Agency), which "
            "maintains the population register. The dodsfallsintyg (death "
            "notification certificate) is issued in Swedish and requires "
            "certified Estonian translation. The Estonian Embassy in Stockholm "
            "can advise on documentation requirements for the Population "
            "Register Centre (Rahvastikuregister). Both countries are EU "
            "members and Hague Apostille Convention members. "
            "(FCDO Travel Advice: Estonia, 2025; Population Register Centre "
            "(Rahvastikuregister), Estonia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'estonia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has an Estonian diaspora community with roots in "
            "the post-Second World War refugee resettlement, concentrated in "
            "New York, New Jersey, and the Midwest. When an Estonian national "
            "or a person of Estonian heritage dies in the United States, the "
            "death is registered with the state civil records office where the "
            "death occurred. The Estonian Embassy in Washington DC can advise "
            "on documentation requirements for the Population Register Centre "
            "(Rahvastikuregister). US death certificates require certified "
            "Estonian translation. Estonia joined the Hague Apostille Convention "
            "in 2001; US-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Estonia, 2025; Population Register Centre "
            "(Rahvastikuregister), Estonia, 2025.)"
        ),
    },
    # R72 -- Latvia x5
    {
        'origin': 'united-kingdom', 'dest': 'latvia',
        'embassy_city': 'London',
        'intro': (
            "Latvia has one of the largest diaspora communities relative to "
            "population size in the European Union, with a substantial Latvian "
            "community in the United Kingdom, particularly in London and "
            "Peterborough. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Latvia, the death must be "
            "registered at the local register office in England and Wales within "
            "5 days, or with the National Records of Scotland or GRONI. The "
            "Latvian Embassy in London can advise on documentation requirements "
            "for the Office of Citizenship and Migration Affairs (PMLP) and "
            "local dzimtsarakstu nodala (civil registry). UK death certificates "
            "require certified Latvian translation. Latvia joined the Hague "
            "Apostille Convention in 1996. "
            "(FCDO Travel Advice: Latvia, 2025; Office of Citizenship and "
            "Migration Affairs (PMLP), Latvia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'latvia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to a significant Latvian diaspora, with nationals "
            "attracted to Berlin, Frankfurt, and other cities following EU "
            "accession in 2004. When a Latvian national dies in Germany and "
            "their family wishes to repatriate remains to Latvia, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Latvian "
            "translation for submission to the dzimtsarakstu nodala (civil "
            "registry department). The Latvian Embassy in Berlin can advise on "
            "documentation requirements. Latvia joined the Hague Apostille "
            "Convention in 1996; German-issued apostille certificates are "
            "accepted. "
            "(FCDO Travel Advice: Latvia, 2025; Office of Citizenship and "
            "Migration Affairs (PMLP), Latvia, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'latvia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a long-established Latvian diaspora community, with "
            "roots in the wartime refugee settlement of 1944 to 1945, when "
            "tens of thousands of Latvians fled to Sweden. This community has "
            "since grown through newer migration since EU accession. When a "
            "Latvian national dies in Sweden, the death is registered with "
            "Skatteverket (the Swedish Tax Agency). The dodsfallsintyg (death "
            "notification certificate) is issued in Swedish and requires "
            "certified Latvian translation. The Latvian Embassy in Stockholm "
            "can advise on documentation requirements for the Office of "
            "Citizenship and Migration Affairs (PMLP). Both countries are "
            "Hague Apostille Convention members. "
            "(FCDO Travel Advice: Latvia, 2025; Office of Citizenship and "
            "Migration Affairs (PMLP), Latvia, 2025.)"
        ),
    },
    {
        'origin': 'finland', 'dest': 'latvia',
        'embassy_city': 'Helsinki',
        'intro': (
            "Finland and Latvia are fellow Baltic Sea neighbours and both joined "
            "the European Union in 2004. The Latvian community in Finland has "
            "grown since EU accession. When a Latvian national dies in Finland, "
            "the death is registered with the Digi- and Population Data Services "
            "Agency (DVV). The kuolintodistus (death certificate) is issued in "
            "Finnish or Swedish and requires certified Latvian translation for "
            "submission to Latvian civil registry authorities. The Latvian "
            "Embassy in Helsinki can advise on documentation requirements for "
            "the Office of Citizenship and Migration Affairs. Both countries "
            "are EU members and Hague Apostille Convention members. "
            "(FCDO Travel Advice: Latvia, 2025; Office of Citizenship and "
            "Migration Affairs (PMLP), Latvia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'latvia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant Latvian diaspora community "
            "with roots in the Second World War refugee settlement, concentrated "
            "in New York, Massachusetts, and Ohio. Latvian-American cultural "
            "organisations remain active across the country. When a Latvian "
            "national or a person of Latvian heritage dies in the United States, "
            "the death is registered with the state civil records office. The "
            "Latvian Embassy in Washington DC can advise on documentation "
            "requirements for the Office of Citizenship and Migration Affairs "
            "(PMLP). US death certificates require certified Latvian translation. "
            "Latvia joined the Hague Apostille Convention in 1996; US-issued "
            "apostille certificates are accepted. "
            "(FCDO Travel Advice: Latvia, 2025; Office of Citizenship and "
            "Migration Affairs (PMLP), Latvia, 2025.)"
        ),
    },
    # R72 -- Slovakia x5
    {
        'origin': 'united-kingdom', 'dest': 'slovakia',
        'embassy_city': 'London',
        'intro': (
            "Slovakia has a substantial diaspora community in the United Kingdom, "
            "with nationals drawn particularly to London, Coventry, and other "
            "cities since EU accession in 2004. When someone from the United "
            "Kingdom dies and their family wishes to repatriate remains to "
            "Slovakia, the death must be registered at the local register office "
            "in England and Wales within 5 days, or with the National Records "
            "of Scotland or GRONI. The Slovak Embassy in London can advise on "
            "documentation requirements for the local matrika (civil registry "
            "office). UK death certificates require certified Slovak translation. "
            "Slovakia joined the Hague Apostille Convention in 2002. "
            "(FCDO Travel Advice: Slovakia, 2025; Ministry of Interior Civil "
            "Registry Division (Matriky), Slovakia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'slovakia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to one of the largest Slovak diaspora communities "
            "outside Slovakia, with nationals working in industry, healthcare, "
            "and the service sector. When a Slovak national dies in Germany and "
            "their family wishes to repatriate remains to Slovakia, the death "
            "is registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Slovak "
            "translation for submission to the local matrika (civil registry "
            "office). The Slovak Embassy in Berlin can advise on documentation "
            "requirements. Slovakia joined the Hague Apostille Convention in "
            "2002; German-issued apostille certificates are accepted. Both "
            "countries are EU members. "
            "(FCDO Travel Advice: Slovakia, 2025; Ministry of Interior Civil "
            "Registry Division (Matriky), Slovakia, 2025.)"
        ),
    },
    {
        'origin': 'austria', 'dest': 'slovakia',
        'embassy_city': 'Vienna',
        'intro': (
            "Austria and Slovakia share a border and long historical ties through "
            "the former Habsburg Empire. The Slovak community in Vienna and "
            "eastern Austria is well established, and the two capitals are among "
            "the closest in Europe at around 60 kilometres apart. When a Slovak "
            "national dies in Austria, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in German; "
            "certified Slovak translation will still be required for Slovak "
            "authorities even though both countries share German as an "
            "administrative language on the Austrian side. The Slovak Embassy "
            "in Vienna can advise on documentation requirements for the local "
            "matrika. Both countries are EU members and Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Slovakia, 2025; Ministry of Interior Civil "
            "Registry Division (Matriky), Slovakia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'slovakia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Slovak-American community with roots "
            "stretching back to the late 19th-century migration to Pennsylvania, "
            "Ohio, and Illinois. When a Slovak national or a person of Slovak "
            "heritage dies in the United States, the death is registered with "
            "the state civil records office where the death occurred. The Slovak "
            "Embassy in Washington DC can advise on documentation requirements "
            "for the local matrika (civil registry office). US death certificates "
            "require certified Slovak translation. Slovakia joined the Hague "
            "Apostille Convention in 2002; US-issued apostille certificates "
            "are accepted. "
            "(FCDO Travel Advice: Slovakia, 2025; Ministry of Interior Civil "
            "Registry Division (Matriky), Slovakia, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'slovakia',
        'embassy_city': 'Paris',
        'intro': (
            "France has a modest Slovak diaspora community, with nationals "
            "living and working in Paris and the wider Ile-de-France region. "
            "When a Slovak national dies in France and their family wishes to "
            "repatriate remains to Slovakia, the death is registered with the "
            "local mairie (town hall). The acte de deces is issued in French "
            "and requires certified Slovak translation for submission to the "
            "local matrika (civil registry office). The Slovak Embassy in Paris "
            "can advise on documentation requirements. Slovakia joined the "
            "Hague Apostille Convention in 2002; French-issued apostille "
            "certificates are accepted. Both countries are EU members. "
            "(FCDO Travel Advice: Slovakia, 2025; Ministry of Interior Civil "
            "Registry Division (Matriky), Slovakia, 2025.)"
        ),
    },
    # R72 -- Slovenia x5
    {
        'origin': 'united-kingdom', 'dest': 'slovenia',
        'embassy_city': 'London',
        'intro': (
            "Slovenia is a popular destination for British ski tourists, "
            "drawn to Kranjska Gora and the Julian Alps, and for cultural "
            "visits to Ljubljana. The Slovenian community in the United Kingdom "
            "has been established since EU accession in 2004. When someone from "
            "the United Kingdom dies and their family wishes to repatriate "
            "remains to Slovenia, the death must be registered at the local "
            "register office in England and Wales within 5 days, or with the "
            "National Records of Scotland or GRONI. The Slovenian Embassy in "
            "London can advise on documentation requirements for the local "
            "maticni urad (civil registry office) at the upravna enota "
            "(administrative unit). UK death certificates require certified "
            "Slovenian translation. Slovenia joined the Hague Apostille "
            "Convention in 1992. "
            "(FCDO Travel Advice: Slovenia, 2025; Administrative Unit "
            "(Upravna enota), Slovenia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'slovenia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Slovenia are both EU members with strong economic "
            "ties, and a significant Slovenian community lives and works in "
            "Germany, particularly in Bavaria and Baden-Wurttemberg. When a "
            "Slovenian national dies in Germany and their family wishes to "
            "repatriate remains to Slovenia, the death is registered with the "
            "local Standesamt (civil registry). The Sterbeurkunde is issued "
            "in German and requires certified Slovenian translation for "
            "submission to the local maticni urad (civil registry). The "
            "Slovenian Embassy in Berlin can advise on documentation "
            "requirements. Slovenia joined the Hague Apostille Convention "
            "in 1992; German-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Slovenia, 2025; Administrative Unit "
            "(Upravna enota), Slovenia, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'slovenia',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Slovenia share a border and deep historical ties "
            "through Trieste and the Karst region. The Slovenian community "
            "in Trieste and Udine is long established, dating to before "
            "Slovenian independence in 1991. When a Slovenian national dies "
            "in Italy, the death is registered with the local Ufficio di "
            "Stato Civile. The atto di morte is issued in Italian and requires "
            "certified Slovenian translation for submission to the maticni "
            "urad (civil registry). The Slovenian Embassy in Rome can advise "
            "on documentation requirements. Both countries are EU members and "
            "Hague Apostille Convention members. "
            "(FCDO Travel Advice: Slovenia, 2025; Administrative Unit "
            "(Upravna enota), Slovenia, 2025.)"
        ),
    },
    {
        'origin': 'austria', 'dest': 'slovenia',
        'embassy_city': 'Vienna',
        'intro': (
            "Austria and Slovenia share a border and a history within the "
            "Habsburg Empire, with close cultural and economic ties. Austrian "
            "tourists visit Slovenia regularly for ski holidays and lake "
            "breaks. When a Slovenian national dies in Austria, the death "
            "is registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Slovenian "
            "translation for submission to the local maticni urad (civil "
            "registry at the upravna enota). The Slovenian Embassy in Vienna "
            "can advise on documentation requirements. Both countries are EU "
            "members and Hague Apostille Convention members. "
            "(FCDO Travel Advice: Slovenia, 2025; Administrative Unit "
            "(Upravna enota), Slovenia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'slovenia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a small Slovenian-American community with "
            "roots in the early 20th-century migration to the Midwest, "
            "concentrated in Ohio and Pennsylvania. When a Slovenian national "
            "or a person of Slovenian heritage dies in the United States, "
            "the death is registered with the state civil records office "
            "where the death occurred. The Slovenian Embassy in Washington "
            "DC can advise on documentation requirements for the local "
            "maticni urad (civil registry office). US death certificates "
            "require certified Slovenian translation. Slovenia joined the "
            "Hague Apostille Convention in 1992; US-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Slovenia, 2025; Administrative Unit "
            "(Upravna enota), Slovenia, 2025.)"
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
    exit(main())
