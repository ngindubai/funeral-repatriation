#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R73-R74.

   R73 (25 routes, variants B,C,D,E,A x5):
     Lithuania x5:        united-kingdom, germany, ireland, norway, sweden
     Mozambique x5:       united-kingdom, portugal, south-africa, germany, france
     Angola x5:           united-kingdom, portugal, france, germany, united-states
     Trinidad & Tobago x5: united-kingdom, united-states, canada, germany, france
     Taiwan x5:           united-kingdom, united-states, australia, japan, germany

   R74 (25 routes, variants B,C,D,E,A x5):
     Chile x5:            united-kingdom, united-states, spain, germany, france
     Eritrea x5:          united-kingdom, germany, sweden, norway, italy
     Kosovo x5:           united-kingdom, germany, switzerland, italy, united-states
     Moldova x5:          united-kingdom, germany, france, italy, united-states
     Laos x5:             united-kingdom, united-states, australia, france, germany

   Template rotation: R72 ended on A. R73 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R74 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'lithuania': {
        'name': 'Lithuania',
        'slug': 'lithuania',
        'key': 'lt',
        'reception': (
            "The Lithuanian funeral director takes custody at Vilnius "
            "International Airport (VNO) or Kaunas Airport (KUN) cargo "
            "terminal. Death registration in Lithuania is handled by the "
            "Metrikacijos skyrius (Civil Registry Division) of the local "
            "municipality under the Ministry of Justice. The mirties "
            "liudijimas (death certificate) is issued in Lithuanian; all "
            "foreign documents require certified Lithuanian translation. "
            "Lithuania joined the Hague Apostille Convention in 2001; "
            "apostille certificates from member states are accepted. "
            "Lithuania is an EU member. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Metrikacijos skyrius, Lithuania, 2025; FCDO Travel "
            "Advice: Lithuania, 2025.)"
        ),
        'consular_template': (
            "The Lithuanian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Lithuania. "
            "Lithuania joined the Hague Apostille Convention in 2001. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Metrikacijos skyrius (Civil Registry Division) in Lithuania "
            "for civil registration queries."
        ),
        'arrival_faq': (
            "The Lithuanian funeral director takes custody at Vilnius "
            "International Airport (VNO) or Kaunas Airport (KUN) cargo "
            "terminal. The Metrikacijos skyrius (Civil Registry Division) "
            "of the local municipality registers the death and issues the "
            "mirties liudijimas (death certificate) in Lithuanian. All "
            "foreign documents require certified Lithuanian translation "
            "before submission to Lithuanian authorities. Lithuania joined "
            "the Hague Apostille Convention in 2001; apostille certificates "
            "from member states are accepted. Lithuania is an EU member. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports."
        ),
        'emergency_line': 'contact the Lithuanian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-lithuania',
    },
    'mozambique': {
        'name': 'Mozambique',
        'slug': 'mozambique',
        'key': 'mz',
        'complexity_override': 'high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-5 weeks',
        'timeline_complex_override': '10-16 weeks',
        'reception': (
            "The Mozambican funeral director takes custody at Maputo "
            "International Airport (MPM) or Beira Airport (BEW) cargo "
            "terminal. Death registration in Mozambique is handled by the "
            "Conservatoria do Registo Civil under the Ministry of Justice "
            "and Constitutional Affairs. The certidao de obito (death "
            "certificate) is issued in Portuguese; all foreign documents "
            "require certified Portuguese translation. Mozambique is not a "
            "Hague Apostille Convention member; full consular authentication "
            "of all foreign documents is required. Mozambique is a "
            "Commonwealth member. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports; embalming "
            "standards and available facilities vary significantly outside "
            "Maputo. "
            "(Conservatoria do Registo Civil, Mozambique, 2025; FCDO "
            "Travel Advice: Mozambique, 2025.)"
        ),
        'consular_template': (
            "The Mozambican High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Mozambique. "
            "Mozambique is not a Hague Apostille Convention member; full "
            "consular authentication is required for all foreign documents. "
            "The High Commission cannot pay for or arrange repatriation. "
            "Contact the Conservatoria do Registo Civil in Mozambique for "
            "civil registration queries."
        ),
        'arrival_faq': (
            "The Mozambican funeral director takes custody at Maputo "
            "International Airport (MPM) or Beira Airport (BEW) cargo "
            "terminal. The Conservatoria do Registo Civil under the Ministry "
            "of Justice registers the death and issues the certidao de obito "
            "in Portuguese. All foreign documents require certified Portuguese "
            "translation before submission to Mozambican authorities. "
            "Mozambique is not a Hague Apostille Convention member; full "
            "consular authentication is required. An embalming certificate "
            "and hermetically sealed coffin are required. Families should "
            "appoint a specialist with experience of Mozambican procedures "
            "early, as administrative capacity varies significantly outside "
            "the capital."
        ),
        'emergency_line': 'contact the Mozambican High Commission or Embassy in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-mozambique',
    },
    'angola': {
        'name': 'Angola',
        'slug': 'angola',
        'key': 'ao',
        'complexity_override': 'high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-5 weeks',
        'timeline_complex_override': '10-16 weeks',
        'reception': (
            "The Angolan funeral director takes custody at Luanda Quatro "
            "de Fevereiro International Airport (LAD) cargo terminal. Death "
            "registration in Angola is handled by the Conservatoria do "
            "Registo Civil under the Ministry of Justice and Human Rights. "
            "The certidao de obito (death certificate) is issued in "
            "Portuguese; all foreign documents require certified Portuguese "
            "translation. Angola is not a Hague Apostille Convention member; "
            "full consular authentication of all foreign documents is "
            "required by Angolan authorities. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Conservatoria do Registo Civil, Angola, 2025; FCDO Travel "
            "Advice: Angola, 2025.)"
        ),
        'consular_template': (
            "The Angolan Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Angola. Angola "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required for all foreign documents. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Conservatoria do Registo Civil in Angola for civil registration "
            "queries."
        ),
        'arrival_faq': (
            "The Angolan funeral director takes custody at Luanda Quatro "
            "de Fevereiro International Airport (LAD) cargo terminal. The "
            "Conservatoria do Registo Civil under the Ministry of Justice "
            "and Human Rights registers the death and issues the certidao "
            "de obito in Portuguese. All foreign documents require certified "
            "Portuguese translation before submission to Angolan authorities. "
            "Angola is not a Hague Apostille Convention member; full consular "
            "authentication of all foreign documents is required. An "
            "embalming certificate and hermetically sealed coffin are "
            "required. A specialist is essential on this corridor."
        ),
        'emergency_line': 'contact the Angolan Embassy or Consulate in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-angola',
    },
    'trinidad-and-tobago': {
        'name': 'Trinidad and Tobago',
        'slug': 'trinidad-and-tobago',
        'key': 'tt',
        'reception': (
            "The Trinidad and Tobago funeral director takes custody at "
            "Piarco International Airport (POS) in Trinidad or A.N.R. "
            "Robinson International Airport (TAB) in Tobago cargo terminal. "
            "Deaths on Tobago may require inter-island transfer to Trinidad "
            "before international repatriation can proceed. Death "
            "registration in Trinidad and Tobago is handled by the Registrar "
            "General's Department. Death certificates are issued in English. "
            "Trinidad and Tobago joined the Hague Apostille Convention in "
            "2001; apostille certificates from member states are accepted. "
            "Trinidad and Tobago is a Commonwealth member. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Registrar General's Department, Trinidad and Tobago, 2025; "
            "FCDO Travel Advice: Trinidad and Tobago, 2025.)"
        ),
        'consular_template': (
            "The Trinidad and Tobago High Commission or Embassy in {city} "
            "can advise on documentation requirements for repatriation to "
            "Trinidad and Tobago. Trinidad and Tobago joined the Hague "
            "Apostille Convention in 2001. The High Commission cannot pay "
            "for or arrange repatriation. Contact the Registrar General's "
            "Department in Trinidad and Tobago for civil registration queries."
        ),
        'arrival_faq': (
            "The Trinidad and Tobago funeral director takes custody at "
            "Piarco International Airport (POS) in Trinidad or A.N.R. "
            "Robinson International Airport (TAB) in Tobago cargo terminal. "
            "For deaths on Tobago, inter-island transfer to Trinidad is "
            "required before international repatriation can proceed. The "
            "Registrar General's Department registers the death and issues "
            "a death certificate in English. Trinidad and Tobago joined "
            "the Hague Apostille Convention in 2001; apostille certificates "
            "from member states are accepted. Trinidad and Tobago is a "
            "Commonwealth member. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Trinidad and Tobago High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-trinidad-and-tobago',
    },
    'taiwan': {
        'name': 'Taiwan',
        'slug': 'taiwan',
        'key': 'tw',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Taiwanese funeral director takes custody at Taiwan Taoyuan "
            "International Airport (TPE) or Taipei Songshan Airport (TSA) "
            "cargo terminal. Death registration in Taiwan is handled by the "
            "Household Registration Office (huji suo) under the Ministry "
            "of the Interior. The death certificate (sijin zhengmingshu) "
            "is issued in Traditional Chinese; all foreign documents require "
            "certified Traditional Chinese translation. Taiwan is not a "
            "formal member of the Hague Apostille Convention, as most "
            "countries do not maintain formal diplomatic relations with "
            "Taiwan; document authentication follows bilateral arrangements. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Household Registration Office, Ministry of the Interior, "
            "Taiwan, 2025; FCDO Travel Advice: Taiwan, 2025.)"
        ),
        'consular_template': (
            "The Taiwan representative office or trade office in {city} "
            "can advise on documentation requirements for repatriation to "
            "Taiwan. As Taiwan is not formally represented through embassies "
            "in most countries, consular matters are handled through the "
            "Taipei Representative Office or an equivalent trade and "
            "economic office. They cannot pay for or arrange repatriation. "
            "Contact the Household Registration Office in Taiwan for "
            "civil registration queries."
        ),
        'arrival_faq': (
            "The Taiwanese funeral director takes custody at Taiwan Taoyuan "
            "International Airport (TPE) or Taipei Songshan Airport (TSA) "
            "cargo terminal. The Household Registration Office (huji suo) "
            "under the Ministry of the Interior registers the death and "
            "issues the death certificate in Traditional Chinese. All "
            "foreign documents require certified Traditional Chinese "
            "translation. Taiwan is not a formal Hague Apostille Convention "
            "member; document authentication follows bilateral arrangements "
            "through the Taipei Representative Office or equivalent trade "
            "office. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Taipei Representative Office or equivalent trade office in the origin country',
        'hub_url': 'repatriation-from-taiwan',
    },
    'chile': {
        'name': 'Chile',
        'slug': 'chile',
        'key': 'cl',
        'reception': (
            "The Chilean funeral director takes custody at Arturo Merino "
            "Benitez International Airport (SCL) in Santiago cargo terminal. "
            "Regional airports serve other areas, including El Tepual Airport "
            "(PMC) in Puerto Montt. Death registration in Chile is handled "
            "by the Servicio de Registro Civil e Identificacion (SRCEI) "
            "at the local Civil Registry Office. The certificado de defuncion "
            "(death certificate) is issued in Spanish; all foreign documents "
            "require certified Spanish translation. Chile joined the Hague "
            "Apostille Convention in 2016; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Servicio de Registro Civil e Identificacion (SRCEI), Chile, "
            "2025; FCDO Travel Advice: Chile, 2025.)"
        ),
        'consular_template': (
            "The Chilean Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Chile. Chile "
            "joined the Hague Apostille Convention in 2016. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Servicio "
            "de Registro Civil e Identificacion (SRCEI) in Chile for "
            "civil registration queries."
        ),
        'arrival_faq': (
            "The Chilean funeral director takes custody at Arturo Merino "
            "Benitez International Airport (SCL) in Santiago cargo terminal. "
            "The Servicio de Registro Civil e Identificacion (SRCEI) "
            "registers the death and issues the certificado de defuncion "
            "in Spanish. All foreign documents require certified Spanish "
            "translation before submission to SRCEI. Chile joined the Hague "
            "Apostille Convention in 2016; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Chilean Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-chile',
    },
    'eritrea': {
        'name': 'Eritrea',
        'slug': 'eritrea',
        'key': 'er',
        'complexity_override': 'high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-5 weeks',
        'timeline_complex_override': '10-16 weeks',
        'reception': (
            "The Eritrean funeral director takes custody at Asmara "
            "International Airport (ASM) cargo terminal. Death registration "
            "in Eritrea is handled by the National Statistics and Evaluation "
            "Office (NSEO) under the Ministry of Health. Death certificates "
            "are issued in Tigrinya, Arabic, or English; foreign documents "
            "require translation into one of these languages. Eritrea is "
            "not a Hague Apostille Convention member; full consular "
            "authentication of all foreign documents is required. The "
            "British Embassy in Asmara is operational but operates on a "
            "limited basis; FCDO advises against all but essential travel "
            "to Eritrea. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(National Statistics and Evaluation Office (NSEO), Eritrea, "
            "2025; FCDO Travel Advice: Eritrea, 2025.)"
        ),
        'consular_template': (
            "The Eritrean Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Eritrea. "
            "Eritrea is not a Hague Apostille Convention member; full "
            "consular authentication is required for all foreign documents. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the National Statistics and Evaluation Office (NSEO) in "
            "Eritrea for civil registration queries."
        ),
        'arrival_faq': (
            "The Eritrean funeral director takes custody at Asmara "
            "International Airport (ASM) cargo terminal. The National "
            "Statistics and Evaluation Office (NSEO) under the Ministry "
            "of Health registers the death; death certificates are issued "
            "in Tigrinya, Arabic, or English. All foreign documents require "
            "translation before submission to Eritrean authorities. Eritrea "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. The British Embassy in Asmara "
            "operates on a limited basis. An embalming certificate and "
            "hermetically sealed coffin are required. A specialist with "
            "experience of Eritrean procedures is essential."
        ),
        'emergency_line': 'contact the Eritrean Embassy or Consulate in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-eritrea',
    },
    'kosovo': {
        'name': 'Kosovo',
        'slug': 'kosovo',
        'key': 'xk',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Kosovo funeral director takes custody at Pristina "
            "International Airport Adem Jashari (PRN) cargo terminal. "
            "Death registration in Kosovo is handled by the Agency for "
            "Civil Registration (civil registry offices within local "
            "municipalities). Death certificates are issued in Albanian "
            "and Serbian; foreign documents require certified Albanian "
            "translation. Kosovo is not a member of the Hague Apostille "
            "Convention; full consular authentication of all foreign "
            "documents is required. The British Embassy in Pristina is "
            "fully operational. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Agency for Civil Registration, Kosovo, 2025; FCDO Travel "
            "Advice: Kosovo, 2025.)"
        ),
        'consular_template': (
            "The Kosovo Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Kosovo. Kosovo "
            "is not a member of the Hague Apostille Convention; full "
            "consular authentication is required for all foreign documents. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the Agency for Civil Registration in Kosovo for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Kosovo funeral director takes custody at Pristina "
            "International Airport Adem Jashari (PRN) cargo terminal. "
            "The Agency for Civil Registration, operating through local "
            "municipality offices, registers the death and issues a death "
            "certificate in Albanian and Serbian. All foreign documents "
            "require certified Albanian translation before submission to "
            "Kosovo authorities. Kosovo is not a member of the Hague "
            "Apostille Convention; full consular authentication is "
            "required. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Kosovo Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-kosovo',
    },
    'moldova': {
        'name': 'Moldova',
        'slug': 'moldova',
        'key': 'md',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Moldovan funeral director takes custody at Chisinau "
            "International Airport (KIV) cargo terminal. Death registration "
            "in Moldova is handled by the civil status offices (starea "
            "civila) under the Agency of Public Services (Agentia Servicii "
            "Publice). The act de deces (death certificate) is issued in "
            "Romanian; all foreign documents require certified Romanian "
            "translation. Moldova joined the Hague Apostille Convention "
            "in 2007; apostille certificates from member states are "
            "accepted. The British Embassy in Chisinau is operational. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Agency of Public Services (Agentia Servicii Publice), "
            "Moldova, 2025; FCDO Travel Advice: Moldova, 2025.)"
        ),
        'consular_template': (
            "The Moldovan Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Moldova. "
            "Moldova joined the Hague Apostille Convention in 2007. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Agency of Public Services (Agentia Servicii Publice) in "
            "Moldova for civil registration queries."
        ),
        'arrival_faq': (
            "The Moldovan funeral director takes custody at Chisinau "
            "International Airport (KIV) cargo terminal. The civil status "
            "offices (starea civila) under the Agency of Public Services "
            "(Agentia Servicii Publice) register the death and issue the "
            "act de deces (death certificate) in Romanian. All foreign "
            "documents require certified Romanian translation before "
            "submission to Moldovan authorities. Moldova joined the Hague "
            "Apostille Convention in 2007; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Moldovan Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-moldova',
    },
    'laos': {
        'name': 'Laos',
        'slug': 'laos',
        'key': 'la',
        'complexity_override': 'high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-5 weeks',
        'timeline_complex_override': '10-16 weeks',
        'reception': (
            "The Lao funeral director takes custody at Wattay International "
            "Airport (VTE) in Vientiane or Luang Prabang International "
            "Airport (LPQ) cargo terminal. Death registration in Laos is "
            "handled by the Department of Civil Registration under the "
            "Ministry of Home Affairs, at the village or district level. "
            "Death certificates are issued in Lao; all foreign documents "
            "require certified Lao translation. Laos is not a Hague "
            "Apostille Convention member; full consular authentication of "
            "all foreign documents is required by Lao authorities. The "
            "British Embassy in Vientiane is operational. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports; specialist expertise is essential on this "
            "corridor. "
            "(Department of Civil Registration, Ministry of Home Affairs, "
            "Lao PDR, 2025; FCDO Travel Advice: Laos, 2025.)"
        ),
        'consular_template': (
            "The Lao Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Laos. Laos "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required for all foreign documents. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Department of Civil Registration under the Ministry of Home "
            "Affairs in Laos for civil registration queries."
        ),
        'arrival_faq': (
            "The Lao funeral director takes custody at Wattay International "
            "Airport (VTE) in Vientiane or Luang Prabang International "
            "Airport (LPQ) cargo terminal. The Department of Civil "
            "Registration under the Ministry of Home Affairs registers the "
            "death at village or district level; death certificates are "
            "issued in Lao. All foreign documents require certified Lao "
            "translation before submission to Lao authorities. Laos is "
            "not a Hague Apostille Convention member; full consular "
            "authentication of all foreign documents is required. An "
            "embalming certificate and hermetically sealed coffin are "
            "required. A specialist with experience of Lao administrative "
            "procedures is essential."
        ),
        'emergency_line': 'contact the Lao Embassy or Consulate in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-laos',
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
            "complex cases."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Australia is widely available in all states and territories.",
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
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
    'ireland': {
        'name': 'Ireland',
        'emergency': '999 or 112',
        'registry': 'the General Register Office (GRO) or local registrar',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 999 or 112 for emergency services. Death is certified by a "
            "physician. The death must be registered with the General Register "
            "Office (GRO) or the local registrar as soon as possible after the "
            "death. A coroner takes jurisdiction for sudden, violent, or "
            "unexplained deaths and must issue a coroner's certificate before "
            "the body can be moved internationally. Ireland is a Hague Apostille "
            "Convention member. The Irish Embassy or Consulate at the destination "
            "can assist Irish nationals abroad. The Department of Foreign Affairs "
            "issues emergency travel documentation for deceased Irish nationals "
            "where required."
        ),
        'doc_time': '3-7 days (coroner cases longer)',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Ireland is available at several licensed crematoria. "
            "A second medical certificate is required before cremation. If the "
            "coroner is involved, the coroner's order replaces this requirement."
        ),
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
    'norway': {
        'name': 'Norway',
        'emergency': '112 (police) / 113 (ambulance)',
        'registry': 'Folkeregisteret (Norwegian National Registry), administered by Skatteetaten',
        'cert_name': 'dodsattest (death certificate)',
        'cert_lang': 'Norwegian',
        'overview': (
            "Call 112 for police or 113 for ambulance. Death is certified by a "
            "physician. The dodsattest (death certificate) is registered with "
            "Folkeregisteret (the Norwegian National Registry), administered by "
            "Skatteetaten (the Norwegian Tax Administration). Police and the "
            "Statsadvokat (public prosecutor) take jurisdiction for violent or "
            "unexplained deaths. Norway is a Hague Apostille Convention member. "
            "The British Embassy in Oslo can assist British nationals."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Norway is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Statsadvokat, public prosecutor takes jurisdiction)',
    },
    'portugal': {
        'name': 'Portugal',
        'emergency': '112',
        'registry': 'the Conservatoria do Registo Civil (civil registry)',
        'cert_name': 'certidao de obito (death certificate)',
        'cert_lang': 'Portuguese',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The certidao de obito (death certificate) is registered with the "
            "local Conservatoria do Registo Civil (civil registry). The Ministerio "
            "Publico (public prosecutor) takes jurisdiction for violent or "
            "unexplained deaths. Portugal is an EU member and Hague Apostille "
            "Convention member. The British Embassy in Lisbon can assist "
            "British nationals."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Portugal is available in major cities.",
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico, public prosecutor takes jurisdiction)',
    },
    'south-africa': {
        'name': 'South Africa',
        'emergency': '112 (mobile) / 10111 (police) / 10177 (ambulance)',
        'registry': 'the Department of Home Affairs via the local Home Affairs office',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 112 from a mobile, 10111 for police, or 10177 for ambulance. "
            "Death is certified by a medical practitioner. The death is registered "
            "with the Department of Home Affairs via the local Home Affairs office. "
            "Forensic pathology services take jurisdiction for violent or unexplained "
            "deaths. South Africa is a Hague Apostille Convention member. The British "
            "High Commission in Pretoria can assist British nationals."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in South Africa is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (forensic pathology services take jurisdiction)',
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
            "civil registry within 7 days of death. Police take jurisdiction "
            "for violent or unexplained deaths. Japan is not a member of the "
            "Hague Apostille Convention; consular authentication of documents "
            "is required. The British Embassy in Tokyo can assist British "
            "nationals."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is the near-universal method of disposition in Japan. "
            "The kotsuage ceremony of collecting ashes is integral to Japanese "
            "Buddhist tradition and is conducted before any international "
            "repatriation of cremated remains."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (police take jurisdiction; autopsy ordered by public prosecutor)',
    },
    'switzerland': {
        'name': 'Switzerland',
        'emergency': '117 (police) / 144 (ambulance) / 112 (EU emergency)',
        'registry': 'the local Zivilstandsamt (civil registry office)',
        'cert_name': 'Todesurkunde (death certificate)',
        'cert_lang': 'German, French, or Italian (depending on canton)',
        'overview': (
            "Call 117 for police, 144 for ambulance, or 112 for the EU emergency "
            "number. Death is certified by a physician. The Todesurkunde (death "
            "certificate) is registered with the local Zivilstandsamt (civil "
            "registry office). The Staatsanwaltschaft (public prosecutor) takes "
            "jurisdiction for violent or unexplained deaths. Switzerland is a "
            "Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Switzerland is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft, public prosecutor takes jurisdiction)',
    },
}

ROUTES = [
    # R73 -- Lithuania x5
    {
        'origin': 'united-kingdom', 'dest': 'lithuania',
        'embassy_city': 'London',
        'intro': (
            "Lithuania has one of the largest diaspora communities relative to "
            "population size of any European Union member state, and the United "
            "Kingdom is home to one of the biggest Lithuanian communities outside "
            "Lithuania. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Lithuania, the death must be "
            "registered at the local register office in England and Wales within "
            "5 days, or with the National Records of Scotland or GRONI in "
            "Northern Ireland. The Lithuanian Embassy in London can advise on "
            "documentation requirements for the Metrikacijos skyrius (Civil "
            "Registry Division). UK death certificates require certified "
            "Lithuanian translation. Lithuania joined the Hague Apostille "
            "Convention in 2001. "
            "(FCDO Travel Advice: Lithuania, 2025; Metrikacijos skyrius, "
            "Lithuania, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'lithuania',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to one of the largest Lithuanian diaspora "
            "communities in Western Europe, with tens of thousands of Lithuanian "
            "nationals living and working there, particularly in cities such as "
            "Hamburg, Munich, and Cologne. When a Lithuanian national dies in "
            "Germany and their family wishes to repatriate remains to Lithuania, "
            "the death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires certified "
            "Lithuanian translation for submission to the Metrikacijos skyrius "
            "(Civil Registry Division). The Lithuanian Embassy in Berlin can "
            "advise on documentation requirements. Lithuania joined the Hague "
            "Apostille Convention in 2001; German-issued apostille certificates "
            "are accepted. "
            "(FCDO Travel Advice: Lithuania, 2025; Metrikacijos skyrius, "
            "Lithuania, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'lithuania',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland has a large and long-established Lithuanian community, "
            "among the largest per capita in Europe, with roots in the post-EU "
            "accession migration of 2004. The Lithuanian-Irish community is "
            "concentrated in Dublin, Cork, and other cities. When a Lithuanian "
            "national dies in Ireland and their family wishes to repatriate "
            "remains to Lithuania, the death is registered with the General "
            "Register Office (GRO) or the local registrar. The Lithuanian "
            "Embassy in Dublin can advise on documentation requirements for "
            "the Metrikacijos skyrius (Civil Registry Division). Irish death "
            "certificates require certified Lithuanian translation. Lithuania "
            "and Ireland are both Hague Apostille Convention members. "
            "(FCDO Travel Advice: Lithuania, 2025; Metrikacijos skyrius, "
            "Lithuania, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'lithuania',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway has a substantial Lithuanian workforce, drawn by economic "
            "opportunity in the construction, maritime, and services sectors. "
            "When a Lithuanian national dies in Norway and their family wishes "
            "to repatriate remains to Lithuania, the death is registered with "
            "Folkeregisteret (the Norwegian National Registry), administered "
            "by Skatteetaten. The dodsattest (death certificate) is issued in "
            "Norwegian and requires certified Lithuanian translation for "
            "submission to the Metrikacijos skyrius (Civil Registry Division). "
            "The Lithuanian Embassy in Oslo can advise on documentation "
            "requirements. Both Norway and Lithuania are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Lithuania, 2025; Metrikacijos skyrius, "
            "Lithuania, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'lithuania',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a significant Lithuanian community, particularly in "
            "Stockholm and Gothenburg, with migration accelerating since "
            "Lithuania joined the European Union in 2004. When a Lithuanian "
            "national dies in Sweden and their family wishes to repatriate "
            "remains to Lithuania, the death is registered with Skatteverket "
            "(the Swedish Tax Agency). The dodsfallsintyg (death notification "
            "certificate) is issued in Swedish and requires certified Lithuanian "
            "translation for submission to the Metrikacijos skyrius (Civil "
            "Registry Division). The Lithuanian Embassy in Stockholm can "
            "advise on documentation requirements. Both countries are EU "
            "members and Hague Apostille Convention members. "
            "(FCDO Travel Advice: Lithuania, 2025; Metrikacijos skyrius, "
            "Lithuania, 2025.)"
        ),
    },
    # R73 -- Mozambique x5
    {
        'origin': 'united-kingdom', 'dest': 'mozambique',
        'embassy_city': 'London',
        'intro': (
            "Mozambique is a Commonwealth member and a destination for British "
            "NGO workers, development sector professionals, and tourists. When "
            "someone from the United Kingdom dies and their family wishes to "
            "repatriate remains to Mozambique, the death must be registered at "
            "the local register office in England and Wales within 5 days, or "
            "with the National Records of Scotland or GRONI in Northern Ireland. "
            "The Mozambican High Commission in London can advise on documentation "
            "requirements for the Conservatoria do Registo Civil. UK death "
            "certificates require certified Portuguese translation. Mozambique "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. A specialist is essential on this "
            "corridor. "
            "(FCDO Travel Advice: Mozambique, 2025; Conservatoria do Registo "
            "Civil, Mozambique, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'mozambique',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Mozambique share language and deep historical ties "
            "through the colonial era, which ended with Mozambican independence "
            "in 1975. A significant Mozambican community lives and works in "
            "Portugal, and families frequently need to repatriate remains between "
            "the two countries. When a Mozambican national dies in Portugal, the "
            "death is registered with the local Conservatoria do Registo Civil "
            "(civil registry). The certidao de obito is issued in Portuguese, "
            "which is the official language of both countries, and requires no "
            "translation for Mozambican authorities. The Mozambican Embassy in "
            "Lisbon can advise on documentation requirements. Mozambique is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Mozambique, 2025; Conservatoria do Registo "
            "Civil, Mozambique, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'mozambique',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa and Mozambique share a long land border, and there "
            "is significant cross-border movement for work and family purposes. "
            "The Mozambican community in South Africa is substantial, drawn "
            "particularly to the Gauteng and Mpumalanga provinces. When a "
            "Mozambican national dies in South Africa, the death is registered "
            "with the Department of Home Affairs via the local Home Affairs "
            "office. The death certificate is issued in English. The Mozambican "
            "Embassy in Pretoria can advise on documentation requirements for "
            "the Conservatoria do Registo Civil. Mozambique is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Mozambique, 2025; Conservatoria do Registo "
            "Civil, Mozambique, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'mozambique',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains a development cooperation relationship with "
            "Mozambique, and a small community of German development workers, "
            "NGO staff, and business professionals operates in Mozambique. When "
            "a Mozambican national or person with Mozambican family connections "
            "dies in Germany and their family wishes to repatriate remains to "
            "Mozambique, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde is issued in German and "
            "requires certified Portuguese translation for submission to the "
            "Conservatoria do Registo Civil. The Mozambican Embassy in Berlin "
            "can advise on documentation requirements. Mozambique is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Mozambique, 2025; Conservatoria do Registo "
            "Civil, Mozambique, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'mozambique',
        'embassy_city': 'Paris',
        'intro': (
            "France has a development and diplomatic relationship with "
            "Mozambique, and a community of French nationals works in the "
            "development, energy, and extractive sectors in Mozambique. When "
            "a Mozambican national dies in France and their family wishes to "
            "repatriate remains to Mozambique, the death is registered with "
            "the local mairie (town hall). The acte de deces is issued in "
            "French and requires certified Portuguese translation for "
            "submission to the Conservatoria do Registo Civil. The Mozambican "
            "Embassy in Paris can advise on documentation requirements. "
            "Mozambique is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(FCDO Travel Advice: Mozambique, 2025; Conservatoria do Registo "
            "Civil, Mozambique, 2025.)"
        ),
    },
    # R73 -- Angola x5
    {
        'origin': 'united-kingdom', 'dest': 'angola',
        'embassy_city': 'London',
        'intro': (
            "Angola is a significant destination for British oil and gas "
            "professionals and development sector workers, with Luanda "
            "hosting a sizeable expat community. When someone from the "
            "United Kingdom dies and their family wishes to repatriate "
            "remains to Angola, the death must be registered at the local "
            "register office in England and Wales within 5 days, or with "
            "the National Records of Scotland or GRONI in Northern Ireland. "
            "The Angolan Embassy in London can advise on documentation "
            "requirements for the Conservatoria do Registo Civil. UK "
            "death certificates require certified Portuguese translation. "
            "Angola is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(FCDO Travel Advice: Angola, 2025; Conservatoria do Registo "
            "Civil, Angola, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'angola',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Angola share language, culture, and a significant "
            "migration corridor. The Angolan community in Portugal is one of "
            "the largest African diaspora groups in the country, with deep "
            "family ties across borders. When an Angolan national dies in "
            "Portugal, the death is registered with the local Conservatoria "
            "do Registo Civil (civil registry). The certidao de obito is "
            "issued in Portuguese, which is the official language of both "
            "countries, and requires no translation for Angolan authorities. "
            "The Angolan Embassy in Lisbon can advise on documentation "
            "requirements. Angola is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(FCDO Travel Advice: Angola, 2025; Conservatoria do Registo "
            "Civil, Angola, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'angola',
        'embassy_city': 'Paris',
        'intro': (
            "France has an Angolan diaspora community, with nationals "
            "concentrated in Paris and other cities. Angola was a Portuguese "
            "colony until 1975, and French-speaking and Portuguese-speaking "
            "communities in France maintain separate ties with Angola. When "
            "an Angolan national dies in France and their family wishes to "
            "repatriate remains to Angola, the death is registered with "
            "the local mairie (town hall). The acte de deces is issued in "
            "French and requires certified Portuguese translation for "
            "submission to the Conservatoria do Registo Civil. The Angolan "
            "Embassy in Paris can advise on documentation requirements. "
            "Angola is not a Hague Apostille Convention member. "
            "(FCDO Travel Advice: Angola, 2025; Conservatoria do Registo "
            "Civil, Angola, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'angola',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a small Angolan community, with nationals living "
            "in Berlin and other cities, and Germany maintains development "
            "cooperation with Angola. When an Angolan national dies in "
            "Germany and their family wishes to repatriate remains to Angola, "
            "the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde is issued in German and requires "
            "certified Portuguese translation for submission to the "
            "Conservatoria do Registo Civil. The Angolan Embassy in Berlin "
            "can advise on documentation requirements. Angola is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Angola, 2025; Conservatoria do Registo "
            "Civil, Angola, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'angola',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a diplomatic and commercial relationship "
            "with Angola, particularly in the energy sector, and a small "
            "Angolan diaspora community is resident in the US. When an "
            "Angolan national or a person with Angolan family connections "
            "dies in the United States, the death is registered with the "
            "state civil records office where the death occurred. The "
            "Angolan Embassy in Washington DC can advise on documentation "
            "requirements for the Conservatoria do Registo Civil. US death "
            "certificates require certified Portuguese translation. Angola "
            "is not a Hague Apostille Convention member; full consular "
            "authentication of all foreign documents is required. "
            "(FCDO Travel Advice: Angola, 2025; Conservatoria do Registo "
            "Civil, Angola, 2025.)"
        ),
    },
    # R73 -- Trinidad and Tobago x5
    {
        'origin': 'united-kingdom', 'dest': 'trinidad-and-tobago',
        'embassy_city': 'London',
        'intro': (
            "Trinidad and Tobago is a Commonwealth member with strong ties "
            "to the United Kingdom, built on a long history of migration "
            "since the Windrush era and continuing family links between "
            "the two countries. When someone from the United Kingdom dies "
            "and their family wishes to repatriate remains to Trinidad and "
            "Tobago, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The Trinidad "
            "and Tobago High Commission in London can advise on documentation "
            "requirements for the Registrar General's Department. UK death "
            "certificates require no translation as English is the official "
            "language. Trinidad and Tobago joined the Hague Apostille "
            "Convention in 2001. "
            "(FCDO Travel Advice: Trinidad and Tobago, 2025; Registrar "
            "General's Department, Trinidad and Tobago, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'trinidad-and-tobago',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant Trinidadian and Tobagonian "
            "diaspora community, concentrated in New York, New Jersey, and "
            "Florida, with strong family ties to the islands. This is among "
            "the highest-volume repatriation corridors for the Caribbean. "
            "When a Trinidadian or Tobagonian national dies in the United "
            "States, the death is registered with the state civil records "
            "office where the death occurred. The Embassy of Trinidad and "
            "Tobago in Washington DC can advise on documentation requirements "
            "for the Registrar General's Department. US death certificates "
            "in English require no translation. Trinidad and Tobago joined "
            "the Hague Apostille Convention in 2001; US-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Trinidad and Tobago, 2025; Registrar "
            "General's Department, Trinidad and Tobago, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'trinidad-and-tobago',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a substantial Trinidadian and Tobagonian diaspora "
            "community, concentrated in Toronto and other Ontario cities, "
            "and strong ties within the Caribbean Community (CARICOM). "
            "When a Trinidadian or Tobagonian national dies in Canada, the "
            "death is registered with the provincial civil records registry. "
            "The High Commission of Trinidad and Tobago in Ottawa can advise "
            "on documentation requirements for the Registrar General's "
            "Department. Canadian death certificates in English require no "
            "translation. Trinidad and Tobago joined the Hague Apostille "
            "Convention in 2001; Canadian-issued apostille certificates are "
            "accepted. "
            "(FCDO Travel Advice: Trinidad and Tobago, 2025; Registrar "
            "General's Department, Trinidad and Tobago, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'trinidad-and-tobago',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a small community of Trinidadian and Tobagonian "
            "nationals, and there is a modest tourism connection through "
            "European visitors to the islands. When a Trinidadian or "
            "Tobagonian national dies in Germany and their family wishes "
            "to repatriate remains, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in "
            "German and requires certified English translation for submission "
            "to the Registrar General's Department. The High Commission or "
            "Embassy of Trinidad and Tobago in Berlin can advise on "
            "documentation requirements. Trinidad and Tobago joined the "
            "Hague Apostille Convention in 2001; German-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Trinidad and Tobago, 2025; Registrar "
            "General's Department, Trinidad and Tobago, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'trinidad-and-tobago',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains regional ties with Trinidad and Tobago through "
            "its overseas territories in the Caribbean, particularly "
            "Martinique and Guadeloupe, which are geographically close to "
            "the islands. When a Trinidadian or Tobagonian national dies "
            "in France and their family wishes to repatriate remains, the "
            "death is registered with the local mairie (town hall). The "
            "acte de deces is issued in French and requires certified English "
            "translation for submission to the Registrar General's "
            "Department. The Embassy of Trinidad and Tobago in Paris can "
            "advise on documentation requirements. Trinidad and Tobago "
            "joined the Hague Apostille Convention in 2001; French-issued "
            "apostille certificates are accepted. "
            "(FCDO Travel Advice: Trinidad and Tobago, 2025; Registrar "
            "General's Department, Trinidad and Tobago, 2025.)"
        ),
    },
    # R73 -- Taiwan x5
    {
        'origin': 'united-kingdom', 'dest': 'taiwan',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom and Taiwan maintain informal but substantive "
            "relations through the British Office Taipei (BOT) and the "
            "Taipei Representative Office in London, and there is a small "
            "but established Taiwanese community in the UK and British "
            "professionals working in Taiwan. When someone from the United "
            "Kingdom dies and their family wishes to repatriate remains to "
            "Taiwan, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The Taipei "
            "Representative Office in London can advise on documentation "
            "requirements. UK death certificates require certified Traditional "
            "Chinese translation. Taiwan is not a formal Hague Apostille "
            "Convention member. "
            "(FCDO Travel Advice: Taiwan, 2025; Household Registration Office, "
            "Ministry of the Interior, Taiwan, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'taiwan',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Taiwan maintain close unofficial relations "
            "through the American Institute in Taiwan (AIT) and the Taipei "
            "Economic and Cultural Representative Office (TECRO) in Washington "
            "DC. The Taiwanese-American community is large and well-established, "
            "concentrated in California, New York, and Texas. When a Taiwanese "
            "national or a person with Taiwanese family connections dies in "
            "the United States, the death is registered with the state civil "
            "records office. The Taipei Economic and Cultural Representative "
            "Office in Washington DC can advise on documentation requirements "
            "for the Household Registration Office. US death certificates "
            "require certified Traditional Chinese translation. Taiwan is not "
            "a formal Hague Apostille Convention member. "
            "(FCDO Travel Advice: Taiwan, 2025; Household Registration Office, "
            "Ministry of the Interior, Taiwan, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'taiwan',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Taiwan maintain relations through the Australian "
            "Office Taipei and the Taipei Economic and Cultural Office in "
            "Canberra. The Taiwanese-Australian community is growing, "
            "concentrated in Sydney and Melbourne, and Australia is a "
            "popular destination for Taiwanese students and working holiday "
            "makers. When a Taiwanese national dies in Australia and their "
            "family wishes to repatriate remains to Taiwan, the death is "
            "registered with the state or territory Births, Deaths and "
            "Marriages (BDM) registry. The Taipei Economic and Cultural "
            "Office in Canberra can advise on documentation requirements "
            "for the Household Registration Office. Australian death "
            "certificates require certified Traditional Chinese translation. "
            "Taiwan is not a formal Hague Apostille Convention member. "
            "(FCDO Travel Advice: Taiwan, 2025; Household Registration Office, "
            "Ministry of the Interior, Taiwan, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'taiwan',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japan and Taiwan share close cultural, economic, and historical "
            "ties, and the Japan-Taiwan air corridor is among the busiest in "
            "Asia. Diplomatic relations are conducted through the Japan-Taiwan "
            "Exchange Association (JTEA) in Taipei and the Association of East "
            "Asian Relations (AEAR) in Japan. When a Taiwanese national dies "
            "in Japan, the shibo todoke (death notification) is submitted "
            "to the local kuyakusho (ward office) civil registry within "
            "7 days of death. The Japan-Taiwan Exchange Association can "
            "advise on documentation requirements for the Household "
            "Registration Office in Taiwan. Death certificates require "
            "certified Traditional Chinese translation. Neither Japan nor "
            "Taiwan is a Hague Apostille Convention member in relation to "
            "each other; consular authentication is required. "
            "(FCDO Travel Advice: Taiwan, 2025; Household Registration Office, "
            "Ministry of the Interior, Taiwan, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'taiwan',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Taiwan maintain trade and economic relations through "
            "the German Institute Taipei and the Taipei Representative Office "
            "in Germany, and there is a Taiwanese community resident in "
            "major German cities. When a Taiwanese national dies in Germany "
            "and their family wishes to repatriate remains to Taiwan, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires certified "
            "Traditional Chinese translation for submission to the Household "
            "Registration Office in Taiwan. The Taipei Representative Office "
            "in Berlin can advise on documentation requirements. Taiwan is "
            "not a formal Hague Apostille Convention member; consular "
            "authentication through the Taipei Representative Office is "
            "required. "
            "(FCDO Travel Advice: Taiwan, 2025; Household Registration Office, "
            "Ministry of the Interior, Taiwan, 2025.)"
        ),
    },
    # R74 -- Chile x5
    {
        'origin': 'united-kingdom', 'dest': 'chile',
        'embassy_city': 'London',
        'intro': (
            "Chile is a popular destination for British backpackers, "
            "adventure travellers, and a small expatriate community, with "
            "Patagonia and Atacama attracting visitors year-round. The "
            "British Embassy in Santiago is fully operational. When someone "
            "from the United Kingdom dies and their family wishes to "
            "repatriate remains to Chile, the death must be registered at "
            "the local register office in England and Wales within 5 days, "
            "or with the National Records of Scotland or GRONI in Northern "
            "Ireland. The Chilean Embassy in London can advise on "
            "documentation requirements for the Servicio de Registro Civil "
            "e Identificacion (SRCEI). UK death certificates require "
            "certified Spanish translation. Chile joined the Hague Apostille "
            "Convention in 2016. "
            "(FCDO Travel Advice: Chile, 2025; Servicio de Registro Civil "
            "e Identificacion (SRCEI), Chile, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'chile',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Chilean diaspora community, concentrated "
            "in Miami, New York, and California, with migration increasing "
            "following political changes in Chile in the 1970s and 1980s. "
            "The US is also among the leading sources of visitors to Chile. "
            "When a Chilean national dies in the United States, the death "
            "is registered with the state civil records office where the "
            "death occurred. The Chilean Embassy in Washington DC can "
            "advise on documentation requirements for the Servicio de "
            "Registro Civil e Identificacion (SRCEI). US death certificates "
            "require certified Spanish translation. Chile joined the Hague "
            "Apostille Convention in 2016; US-issued apostille certificates "
            "are accepted. "
            "(FCDO Travel Advice: Chile, 2025; SRCEI, Chile, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'chile',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and Chile share language and strong historical, cultural, "
            "and migration ties. Chile received significant Spanish immigration "
            "in the 19th and 20th centuries, and the Chilean community in "
            "Spain has grown further since political changes in Chile. When "
            "a Chilean national dies in Spain, the death is registered with "
            "the local Registro Civil (civil registry). The certificado de "
            "defuncion is issued in Spanish, which is the official language "
            "of both countries, and requires no translation for Chilean "
            "authorities. The Chilean Embassy in Madrid can advise on "
            "documentation requirements for the SRCEI. Chile joined the "
            "Hague Apostille Convention in 2016; Spanish-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Chile, 2025; SRCEI, Chile, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'chile',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has historical ties to Chile through German-Chilean "
            "communities established in the 19th century, particularly in "
            "the Lake District and Patagonia. A small but established "
            "Chilean diaspora community exists in Germany. When a Chilean "
            "national dies in Germany and their family wishes to repatriate "
            "remains to Chile, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in "
            "German and requires certified Spanish translation for submission "
            "to the Servicio de Registro Civil e Identificacion (SRCEI). "
            "The Chilean Embassy in Berlin can advise on documentation "
            "requirements. Chile joined the Hague Apostille Convention in "
            "2016; German-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Chile, 2025; SRCEI, Chile, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'chile',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Chilean diaspora community with roots partly in "
            "the political exile of the 1970s and 1980s, when many "
            "Chileans sought refuge in France. Ties remain strong through "
            "cultural and political connections. When a Chilean national "
            "dies in France and their family wishes to repatriate remains "
            "to Chile, the death is registered with the local mairie (town "
            "hall). The acte de deces is issued in French and requires "
            "certified Spanish translation for submission to the Servicio "
            "de Registro Civil e Identificacion (SRCEI). The Chilean "
            "Embassy in Paris can advise on documentation requirements. "
            "Chile joined the Hague Apostille Convention in 2016; "
            "French-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Chile, 2025; SRCEI, Chile, 2025.)"
        ),
    },
    # R74 -- Eritrea x5
    {
        'origin': 'united-kingdom', 'dest': 'eritrea',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom has one of the largest Eritrean diaspora "
            "communities in Europe, concentrated in London, Birmingham, and "
            "other cities, with roots in refugees and asylum seekers who "
            "arrived during and after the independence war. When someone from "
            "the United Kingdom dies and their family wishes to repatriate "
            "remains to Eritrea, the death must be registered at the local "
            "register office in England and Wales within 5 days, or with the "
            "National Records of Scotland or GRONI in Northern Ireland. The "
            "Eritrean Embassy in London can advise on documentation "
            "requirements for the National Statistics and Evaluation Office "
            "(NSEO). UK death certificates require translation for Eritrean "
            "authorities. Eritrea is not a Hague Apostille Convention member; "
            "full consular authentication is required. FCDO advises against "
            "all but essential travel to Eritrea. "
            "(FCDO Travel Advice: Eritrea, 2025; National Statistics and "
            "Evaluation Office (NSEO), Eritrea, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'eritrea',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to one of the largest Eritrean communities in "
            "Europe, with tens of thousands of Eritrean nationals resident "
            "in cities including Frankfurt, Hamburg, and Stuttgart, many "
            "with refugee or asylum status. When an Eritrean national dies "
            "in Germany and their family wishes to repatriate remains to "
            "Eritrea, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde is issued in German and "
            "requires translation before submission to Eritrean authorities. "
            "The Eritrean Embassy in Berlin can advise on documentation "
            "requirements for the National Statistics and Evaluation Office "
            "(NSEO). Eritrea is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(FCDO Travel Advice: Eritrea, 2025; NSEO, Eritrea, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'eritrea',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a large Eritrean diaspora community, one of the "
            "largest per capita in Europe, with Eritrean nationals "
            "concentrated in Stockholm, Gothenburg, and Malmo, many "
            "arriving as refugees during and after the independence war "
            "and the subsequent conflicts. When an Eritrean national dies "
            "in Sweden and their family wishes to repatriate remains to "
            "Eritrea, the death is registered with Skatteverket (the "
            "Swedish Tax Agency). The dodsfallsintyg (death notification "
            "certificate) is issued in Swedish and requires translation "
            "for submission to Eritrean authorities. The Eritrean Embassy "
            "in Stockholm can advise on documentation requirements. Eritrea "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Eritrea, 2025; NSEO, Eritrea, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'eritrea',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway has a significant Eritrean diaspora community, with "
            "nationals settled in Oslo and other cities, many arriving "
            "through the asylum system. When an Eritrean national dies "
            "in Norway and their family wishes to repatriate remains to "
            "Eritrea, the death is registered with Folkeregisteret (the "
            "Norwegian National Registry), administered by Skatteetaten. "
            "The dodsattest (death certificate) is issued in Norwegian "
            "and requires translation for submission to Eritrean authorities. "
            "The Eritrean Embassy in Oslo can advise on documentation "
            "requirements for the National Statistics and Evaluation Office "
            "(NSEO). Eritrea is not a Hague Apostille Convention member; "
            "full consular authentication is required. FCDO advises against "
            "all but essential travel to Eritrea. "
            "(FCDO Travel Advice: Eritrea, 2025; NSEO, Eritrea, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'eritrea',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Eritrea share a colonial history: Eritrea was an "
            "Italian colony from 1890 to 1941, and some Italian cultural "
            "and architectural influence remains visible in Asmara. Italy "
            "has a small Eritrean diaspora community in Rome and other "
            "cities. When an Eritrean national dies in Italy and their "
            "family wishes to repatriate remains to Eritrea, the death is "
            "registered with the local Ufficio di Stato Civile. The atto "
            "di morte is issued in Italian and requires translation before "
            "submission to Eritrean authorities. The Eritrean Embassy in "
            "Rome can advise on documentation requirements for the National "
            "Statistics and Evaluation Office (NSEO). Eritrea is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Eritrea, 2025; NSEO, Eritrea, 2025.)"
        ),
    },
    # R74 -- Kosovo x5
    {
        'origin': 'united-kingdom', 'dest': 'kosovo',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom recognised Kosovo as an independent state "
            "in 2008 and maintains a fully operational British Embassy in "
            "Pristina. The Kosovo diaspora in the UK is significant, with "
            "communities in London, Manchester, and other cities, many of "
            "whom arrived during and after the 1998 to 1999 conflict. When "
            "someone from the United Kingdom dies and their family wishes "
            "to repatriate remains to Kosovo, the death must be registered "
            "at the local register office in England and Wales within 5 "
            "days, or with the National Records of Scotland or GRONI. The "
            "Kosovo Embassy in London can advise on documentation "
            "requirements for the Agency for Civil Registration. UK death "
            "certificates require certified Albanian translation. Kosovo is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Kosovo, 2025; Agency for Civil "
            "Registration, Kosovo, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'kosovo',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has the largest Kosovo Albanian diaspora community in "
            "Western Europe, with several hundred thousand Kosovo nationals "
            "or persons of Kosovo descent resident in Germany, particularly "
            "in Stuttgart, Duisburg, and other cities. This is one of the "
            "highest-volume repatriation corridors for Kosovo. When a "
            "Kosovo national dies in Germany and their family wishes to "
            "repatriate remains, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in "
            "German and requires certified Albanian translation for "
            "submission to the Agency for Civil Registration. The Kosovo "
            "Embassy in Berlin can advise on documentation requirements. "
            "Kosovo is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(FCDO Travel Advice: Kosovo, 2025; Agency for Civil "
            "Registration, Kosovo, 2025.)"
        ),
    },
    {
        'origin': 'switzerland', 'dest': 'kosovo',
        'embassy_city': 'Bern',
        'intro': (
            "Switzerland has a large Kosovo Albanian diaspora community, "
            "one of the largest outside the Western Balkans, with nationals "
            "concentrated in Zurich, Basel, and Bern. The Switzerland-Kosovo "
            "repatriation corridor is among the most established in Europe "
            "for this origin-destination pair. When a Kosovo national dies "
            "in Switzerland, the death is registered with the local "
            "Zivilstandsamt (civil registry office). The Todesurkunde "
            "(death certificate) is issued in German, French, or Italian "
            "and requires certified Albanian translation for submission to "
            "the Agency for Civil Registration. The Kosovo Embassy in Bern "
            "can advise on documentation requirements. Kosovo is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Kosovo, 2025; Agency for Civil "
            "Registration, Kosovo, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'kosovo',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a Kosovo Albanian community, with nationals and "
            "persons of Kosovo descent living in cities including Rome, "
            "Milan, and Turin. Italy has also contributed significantly "
            "to the NATO Kosovo Force (KFOR) mission in Kosovo, maintaining "
            "close bilateral ties. When a Kosovo national dies in Italy "
            "and their family wishes to repatriate remains, the death is "
            "registered with the local Ufficio di Stato Civile. The atto "
            "di morte is issued in Italian and requires certified Albanian "
            "translation for submission to the Agency for Civil Registration "
            "in Kosovo. The Kosovo Embassy in Rome can advise on "
            "documentation requirements. Kosovo is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Kosovo, 2025; Agency for Civil "
            "Registration, Kosovo, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'kosovo',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States played a central role in Kosovo's "
            "independence process and recognised Kosovo as an independent "
            "state in 2008. The Albanian-American community, which includes "
            "a significant Kosovo Albanian population, is concentrated in "
            "New York, New Jersey, and Michigan. When a Kosovo national "
            "dies in the United States, the death is registered with the "
            "state civil records office where the death occurred. The "
            "Kosovo Embassy in Washington DC can advise on documentation "
            "requirements for the Agency for Civil Registration. US death "
            "certificates require certified Albanian translation. Kosovo "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Kosovo, 2025; Agency for Civil "
            "Registration, Kosovo, 2025.)"
        ),
    },
    # R74 -- Moldova x5
    {
        'origin': 'united-kingdom', 'dest': 'moldova',
        'embassy_city': 'London',
        'intro': (
            "Moldova has one of the largest emigrant populations relative "
            "to its size of any country in Europe, and the United Kingdom "
            "is among the destinations for Moldovan workers and students. "
            "When someone from the United Kingdom dies and their family "
            "wishes to repatriate remains to Moldova, the death must be "
            "registered at the local register office in England and Wales "
            "within 5 days, or with the National Records of Scotland or "
            "GRONI in Northern Ireland. The Moldovan Embassy in London "
            "can advise on documentation requirements for the civil status "
            "offices (starea civila) under the Agency of Public Services. "
            "UK death certificates require certified Romanian translation. "
            "Moldova joined the Hague Apostille Convention in 2007. "
            "(FCDO Travel Advice: Moldova, 2025; Agency of Public Services "
            "(Agentia Servicii Publice), Moldova, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'moldova',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany hosts a significant Moldovan diaspora community, with "
            "nationals drawn to Germany for work in construction, healthcare, "
            "and agriculture. When a Moldovan national dies in Germany and "
            "their family wishes to repatriate remains to Moldova, the death "
            "is registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified "
            "Romanian translation for submission to the civil status offices "
            "(starea civila). The Moldovan Embassy in Berlin can advise on "
            "documentation requirements for the Agency of Public Services "
            "(Agentia Servicii Publice). Moldova joined the Hague Apostille "
            "Convention in 2007; German-issued apostille certificates are "
            "accepted. "
            "(FCDO Travel Advice: Moldova, 2025; Agency of Public Services, "
            "Moldova, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'moldova',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Moldovan diaspora community, with nationals "
            "working in Paris and other cities in catering, domestic "
            "services, and construction. Moldovan citizens also benefit "
            "from European Union free movement rules that facilitated "
            "migration to France. When a Moldovan national dies in France "
            "and their family wishes to repatriate remains to Moldova, "
            "the death is registered with the local mairie (town hall). "
            "The acte de deces is issued in French and requires certified "
            "Romanian translation for submission to Moldovan authorities. "
            "The Moldovan Embassy in Paris can advise on documentation "
            "requirements. Moldova joined the Hague Apostille Convention "
            "in 2007; French-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Moldova, 2025; Agency of Public Services, "
            "Moldova, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'moldova',
        'embassy_city': 'Rome',
        'intro': (
            "Italy is home to one of the largest Moldovan diaspora "
            "communities in Western Europe, with Moldovan nationals "
            "working predominantly in domestic care, agriculture, and "
            "the service sector. The Italy-Moldova repatriation corridor "
            "is one of the most active in Europe for this origin-destination "
            "pair. When a Moldovan national dies in Italy, the death is "
            "registered with the local Ufficio di Stato Civile. The atto "
            "di morte is issued in Italian and requires certified Romanian "
            "translation for submission to Moldovan civil status authorities. "
            "The Moldovan Embassy in Rome can advise on documentation "
            "requirements. Moldova joined the Hague Apostille Convention "
            "in 2007; Italian-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Moldova, 2025; Agency of Public Services, "
            "Moldova, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'moldova',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Moldovan diaspora community, "
            "concentrated in New York, New Jersey, and California, with "
            "migration accelerating after Moldovan independence in 1991. "
            "When a Moldovan national or a person of Moldovan heritage "
            "dies in the United States, the death is registered with "
            "the state civil records office where the death occurred. "
            "The Moldovan Embassy in Washington DC can advise on "
            "documentation requirements for the civil status offices "
            "(starea civila) under the Agency of Public Services. US "
            "death certificates require certified Romanian translation. "
            "Moldova joined the Hague Apostille Convention in 2007; "
            "US-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Moldova, 2025; Agency of Public Services, "
            "Moldova, 2025.)"
        ),
    },
    # R74 -- Laos x5
    {
        'origin': 'united-kingdom', 'dest': 'laos',
        'embassy_city': 'London',
        'intro': (
            "Laos is a destination for British backpackers and adventure "
            "travellers, with Luang Prabang, Vang Vieng, and the 4,000 "
            "Islands area among the most visited sites. The British Embassy "
            "in Vientiane is operational and provides consular assistance. "
            "When someone from the United Kingdom dies and their family "
            "wishes to repatriate remains to Laos, the death must be "
            "registered at the local register office in England and Wales "
            "within 5 days, or with the National Records of Scotland or "
            "GRONI in Northern Ireland. The Lao Embassy in London can "
            "advise on documentation requirements for the Department of "
            "Civil Registration. UK death certificates require certified "
            "Lao translation. Laos is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(FCDO Travel Advice: Laos, 2025; Department of Civil "
            "Registration, Ministry of Home Affairs, Lao PDR, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'laos',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Lao diaspora community, many with "
            "roots in the refugee resettlement that followed the 1975 "
            "political transition, concentrated in California, Minnesota, "
            "and Texas. When a Lao national or a person with Lao family "
            "connections dies in the United States, the death is registered "
            "with the state civil records office where the death occurred. "
            "The Embassy of Laos in Washington DC can advise on "
            "documentation requirements for the Department of Civil "
            "Registration under the Ministry of Home Affairs. US death "
            "certificates require certified Lao translation. Laos is not "
            "a Hague Apostille Convention member; full consular "
            "authentication of all foreign documents is required. "
            "(FCDO Travel Advice: Laos, 2025; Department of Civil "
            "Registration, Ministry of Home Affairs, Lao PDR, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'laos',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a small Lao diaspora community, with roots in "
            "the refugee resettlement of the late 1970s and 1980s, "
            "concentrated in Melbourne and Sydney. Australian tourists "
            "also visit Laos in significant numbers. The Australian Embassy "
            "in Vientiane is operational. When a Lao national dies in "
            "Australia and their family wishes to repatriate remains to "
            "Laos, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. The Embassy of "
            "Laos in Canberra can advise on documentation requirements for "
            "the Department of Civil Registration. Australian death "
            "certificates require certified Lao translation. Laos is not "
            "a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Laos, 2025; Department of Civil "
            "Registration, Ministry of Home Affairs, Lao PDR, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'laos',
        'embassy_city': 'Paris',
        'intro': (
            "France and Laos share a colonial history through French "
            "Indochina (1893 to 1954), and France retains cultural, "
            "linguistic, and institutional ties with Laos. A Lao diaspora "
            "community is settled in France, and French is still used "
            "in some Lao government and educational contexts. When a Lao "
            "national dies in France and their family wishes to repatriate "
            "remains to Laos, the death is registered with the local "
            "mairie (town hall). The acte de deces is issued in French "
            "and requires certified Lao translation for submission to "
            "Lao authorities. The Embassy of Laos in Paris can advise "
            "on documentation requirements for the Department of Civil "
            "Registration. Laos is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(FCDO Travel Advice: Laos, 2025; Department of Civil "
            "Registration, Ministry of Home Affairs, Lao PDR, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'laos',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a small Lao community and maintains development "
            "cooperation with Laos. German tourists visit Laos for "
            "cultural tourism, trekking, and the UNESCO World Heritage "
            "site of Luang Prabang. The German Embassy in Vientiane is "
            "operational. When a Lao national dies in Germany and their "
            "family wishes to repatriate remains to Laos, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Lao "
            "translation for submission to Lao authorities. The Embassy "
            "of Laos in Berlin can advise on documentation requirements "
            "for the Department of Civil Registration under the Ministry "
            "of Home Affairs. Laos is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(FCDO Travel Advice: Laos, 2025; Department of Civil "
            "Registration, Ministry of Home Affairs, Lao PDR, 2025.)"
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
