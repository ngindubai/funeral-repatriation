#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R75-R76.

   R75 (25 routes, variants B,C,D,E,A x5):
     Israel x5:      united-kingdom, united-states, france, germany, russia
     Armenia x5:     france, russia, united-states, germany, united-kingdom
     Azerbaijan x5:  russia, turkey, germany, united-kingdom, united-states
     Kazakhstan x5:  russia, germany, united-kingdom, united-states, china
     Paraguay x5:    united-states, spain, argentina, germany, brazil

   R76 (25 routes, variants B,C,D,E,A x5):
     Uruguay x5:     united-states, spain, argentina, italy, germany
     Bolivia x5:     united-states, spain, argentina, germany, france
     Honduras x5:    united-states, spain, mexico, canada, germany
     Guatemala x5:   united-states, mexico, spain, canada, germany
     El Salvador x5: united-states, mexico, spain, canada, germany

   Template rotation: R74 ended on A. R75 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R76 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'israel': {
        'name': 'Israel',
        'slug': 'israel',
        'key': 'il',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Israeli funeral director takes custody at Ben Gurion "
            "International Airport (TLV) cargo terminal near Tel Aviv. "
            "Death registration in Israel is handled by the Population and "
            "Immigration Authority under the Ministry of Interior. The "
            "teudat ptirah (death certificate) is issued in Hebrew; all "
            "foreign documents require certified Hebrew translation. Israel "
            "joined the Hague Apostille Convention in 1977; apostille "
            "certificates from member states are accepted. In Jewish "
            "tradition, burial is ordinarily carried out as soon as possible "
            "after death; families should appoint a specialist with "
            "experience of Israeli religious requirements at the earliest "
            "opportunity. Muslim burials in Israel are coordinated with "
            "the relevant Islamic society. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Population and Immigration Authority, Ministry of Interior, "
            "Israel, 2025; FCDO Travel Advice: Israel, 2025.)"
        ),
        'consular_template': (
            "The Israeli Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Israel. Israel "
            "joined the Hague Apostille Convention in 1977. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Population "
            "and Immigration Authority under the Ministry of Interior in "
            "Israel for civil registration queries."
        ),
        'arrival_faq': (
            "The Israeli funeral director takes custody at Ben Gurion "
            "International Airport (TLV) cargo terminal. The Population "
            "and Immigration Authority under the Ministry of Interior "
            "registers the death and issues the teudat ptirah (death "
            "certificate) in Hebrew. All foreign documents require certified "
            "Hebrew translation before submission to Israeli authorities. "
            "Israel joined the Hague Apostille Convention in 1977; apostille "
            "certificates from member states are accepted. In Jewish "
            "tradition, burial takes place as soon as possible after death; "
            "specialist handling is required to expedite the international "
            "process. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports."
        ),
        'emergency_line': 'contact the Israeli Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-israel',
    },
    'armenia': {
        'name': 'Armenia',
        'slug': 'armenia',
        'key': 'am',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Armenian funeral director takes custody at Zvartnots "
            "International Airport (EVN) in Yerevan cargo terminal. Death "
            "registration in Armenia is handled by the Civil Status Acts "
            "Registration Agency (CSARA). The death certificate is issued "
            "in Armenian; all foreign documents require certified Armenian "
            "translation. Armenia joined the Hague Apostille Convention in "
            "2018; apostille certificates from member states are accepted. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Civil Status Acts Registration Agency (CSARA), Armenia, 2025; "
            "FCDO Travel Advice: Armenia, 2025.)"
        ),
        'consular_template': (
            "The Armenian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Armenia. Armenia "
            "joined the Hague Apostille Convention in 2018. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Civil "
            "Status Acts Registration Agency (CSARA) in Armenia for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Armenian funeral director takes custody at Zvartnots "
            "International Airport (EVN) in Yerevan cargo terminal. The "
            "Civil Status Acts Registration Agency (CSARA) registers the "
            "death and issues the death certificate in Armenian. All foreign "
            "documents require certified Armenian translation before "
            "submission to Armenian authorities. Armenia joined the Hague "
            "Apostille Convention in 2018; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Armenian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-armenia',
    },
    'azerbaijan': {
        'name': 'Azerbaijan',
        'slug': 'azerbaijan',
        'key': 'az',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Azerbaijani funeral director takes custody at Heydar "
            "Aliyev International Airport (GYD) in Baku cargo terminal. "
            "Death registration in Azerbaijan is handled by the State "
            "Registry of Civil Acts (ARCA) under the Ministry of Justice. "
            "The death certificate is issued in Azerbaijani (Latin script); "
            "all foreign documents require certified Azerbaijani translation. "
            "Azerbaijan joined the Hague Apostille Convention in 2004; "
            "apostille certificates from member states are accepted. An "
            "embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(State Registry of Civil Acts (ARCA), Ministry of Justice, "
            "Azerbaijan, 2025; FCDO Travel Advice: Azerbaijan, 2025.)"
        ),
        'consular_template': (
            "The Azerbaijani Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Azerbaijan. "
            "Azerbaijan joined the Hague Apostille Convention in 2004. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "State Registry of Civil Acts (ARCA) under the Ministry of "
            "Justice in Azerbaijan for civil registration queries."
        ),
        'arrival_faq': (
            "The Azerbaijani funeral director takes custody at Heydar "
            "Aliyev International Airport (GYD) in Baku cargo terminal. "
            "The State Registry of Civil Acts (ARCA) under the Ministry of "
            "Justice registers the death and issues the death certificate in "
            "Azerbaijani. All foreign documents require certified Azerbaijani "
            "translation before submission to Azerbaijani authorities. "
            "Azerbaijan joined the Hague Apostille Convention in 2004; "
            "apostille certificates from member states are accepted. An "
            "embalming certificate and hermetically sealed coffin are "
            "required."
        ),
        'emergency_line': 'contact the Azerbaijani Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-azerbaijan',
    },
    'kazakhstan': {
        'name': 'Kazakhstan',
        'slug': 'kazakhstan',
        'key': 'kz',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Kazakhstani funeral director takes custody at Almaty "
            "International Airport (ALA) or Astana International Airport "
            "(NQZ) cargo terminal. Death registration in Kazakhstan is "
            "handled by the Civil Registry Department under the Ministry "
            "of Justice. Death certificates are issued in Kazakh and "
            "Russian; all foreign documents require certified Kazakh or "
            "Russian translation. Kazakhstan joined the Hague Apostille "
            "Convention in 2001; apostille certificates from member states "
            "are accepted. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(Civil Registry Department, Ministry of Justice, Kazakhstan, "
            "2025; FCDO Travel Advice: Kazakhstan, 2025.)"
        ),
        'consular_template': (
            "The Kazakhstani Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Kazakhstan. "
            "Kazakhstan joined the Hague Apostille Convention in 2001. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Civil Registry Department under the Ministry of Justice in "
            "Kazakhstan for civil registration queries."
        ),
        'arrival_faq': (
            "The Kazakhstani funeral director takes custody at Almaty "
            "International Airport (ALA) or Astana International Airport "
            "(NQZ) cargo terminal. The Civil Registry Department under the "
            "Ministry of Justice registers the death and issues the death "
            "certificate in Kazakh and Russian. All foreign documents "
            "require certified Kazakh or Russian translation before "
            "submission to Kazakhstani authorities. Kazakhstan joined the "
            "Hague Apostille Convention in 2001; apostille certificates "
            "from member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Kazakhstani Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-kazakhstan',
    },
    'paraguay': {
        'name': 'Paraguay',
        'slug': 'paraguay',
        'key': 'py',
        'reception': (
            "The Paraguayan funeral director takes custody at Silvio "
            "Pettirossi International Airport (ASU) in Asuncion cargo "
            "terminal. Death registration in Paraguay is handled by the "
            "Direccion General del Registro del Estado Civil de las "
            "Personas (Registro Civil) under the Ministry of Justice. "
            "The acta de defuncion (death certificate) is issued in "
            "Spanish; all foreign documents require certified Spanish "
            "translation where required. Paraguay joined the Hague "
            "Apostille Convention in 1991; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Registro Civil, Paraguay, 2025; FCDO Travel Advice: "
            "Paraguay, 2025.)"
        ),
        'consular_template': (
            "The Paraguayan Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Paraguay. "
            "Paraguay joined the Hague Apostille Convention in 1991. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Direccion General del Registro del Estado Civil de las Personas "
            "in Paraguay for civil registration queries."
        ),
        'arrival_faq': (
            "The Paraguayan funeral director takes custody at Silvio "
            "Pettirossi International Airport (ASU) in Asuncion cargo "
            "terminal. The Direccion General del Registro del Estado Civil "
            "de las Personas (Registro Civil) under the Ministry of Justice "
            "registers the death and issues the acta de defuncion in "
            "Spanish. Foreign documents require certified Spanish translation "
            "where required. Paraguay joined the Hague Apostille Convention "
            "in 1991; apostille certificates from member states are "
            "accepted. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Paraguayan Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-paraguay',
    },
    'uruguay': {
        'name': 'Uruguay',
        'slug': 'uruguay',
        'key': 'uy',
        'reception': (
            "The Uruguayan funeral director takes custody at Carrasco "
            "International Airport (MVD) in Montevideo cargo terminal. "
            "Death registration in Uruguay is handled by the Direccion "
            "General del Registro del Estado Civil under the Ministry of "
            "Education and Culture. The acta de defuncion (death "
            "certificate) is issued in Spanish; all foreign documents "
            "require certified Spanish translation where required. Uruguay "
            "joined the Hague Apostille Convention in 2012; apostille "
            "certificates from member states are accepted. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Direccion General del Registro del Estado Civil, Uruguay, "
            "2025; FCDO Travel Advice: Uruguay, 2025.)"
        ),
        'consular_template': (
            "The Uruguayan Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Uruguay. "
            "Uruguay joined the Hague Apostille Convention in 2012. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Direccion General del Registro del Estado Civil in Uruguay "
            "for civil registration queries."
        ),
        'arrival_faq': (
            "The Uruguayan funeral director takes custody at Carrasco "
            "International Airport (MVD) in Montevideo cargo terminal. "
            "The Direccion General del Registro del Estado Civil under the "
            "Ministry of Education and Culture registers the death and "
            "issues the acta de defuncion in Spanish. Foreign documents "
            "require certified Spanish translation where required. Uruguay "
            "joined the Hague Apostille Convention in 2012; apostille "
            "certificates from member states are accepted. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Uruguayan Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-uruguay',
    },
    'bolivia': {
        'name': 'Bolivia',
        'slug': 'bolivia',
        'key': 'bo',
        'complexity_override': 'moderate',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-5 weeks',
        'timeline_complex_override': '10-16 weeks',
        'reception': (
            "The Bolivian funeral director takes custody at El Alto "
            "International Airport (LPB) in La Paz or Viru Viru "
            "International Airport (VVI) in Santa Cruz cargo terminal. "
            "Death registration in Bolivia is handled by SERECI "
            "(Servicio de Registro Civico) under the Tribunal Supremo "
            "Electoral. The certificado de defuncion (death certificate) "
            "is issued in Spanish; all foreign documents require certified "
            "Spanish translation. Bolivia joined the Hague Apostille "
            "Convention in 2009; apostille certificates from member states "
            "are accepted. Deaths at high altitude or in remote areas may "
            "require additional local procedures. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports. "
            "(SERECI, Tribunal Supremo Electoral, Bolivia, 2025; FCDO "
            "Travel Advice: Bolivia, 2025.)"
        ),
        'consular_template': (
            "The Bolivian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Bolivia. Bolivia "
            "joined the Hague Apostille Convention in 2009. The Embassy "
            "cannot pay for or arrange repatriation. Contact SERECI "
            "(Servicio de Registro Civico) in Bolivia for civil registration "
            "queries."
        ),
        'arrival_faq': (
            "The Bolivian funeral director takes custody at El Alto "
            "International Airport (LPB) in La Paz or Viru Viru "
            "International Airport (VVI) in Santa Cruz cargo terminal. "
            "SERECI (Servicio de Registro Civico) under the Tribunal Supremo "
            "Electoral registers the death and issues the certificado de "
            "defuncion in Spanish. Foreign documents require certified "
            "Spanish translation before submission to Bolivian authorities. "
            "Bolivia joined the Hague Apostille Convention in 2009; "
            "apostille certificates from member states are accepted. Deaths "
            "in high-altitude or remote areas may require additional local "
            "procedures. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Bolivian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-bolivia',
    },
    'honduras': {
        'name': 'Honduras',
        'slug': 'honduras',
        'key': 'hn',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Honduran funeral director takes custody at Toncontin "
            "International Airport (TGU) in Tegucigalpa or Ramon Villeda "
            "Morales International Airport (SAP) in San Pedro Sula cargo "
            "terminal. Death registration in Honduras is handled by the "
            "Registro Nacional de las Personas (RNP). The certificado de "
            "defuncion (death certificate) is issued in Spanish; all "
            "foreign documents require certified Spanish translation where "
            "required. Honduras joined the Hague Apostille Convention in "
            "2007; apostille certificates from member states are accepted. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Registro Nacional de las Personas (RNP), Honduras, 2025; "
            "FCDO Travel Advice: Honduras, 2025.)"
        ),
        'consular_template': (
            "The Honduran Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Honduras. "
            "Honduras joined the Hague Apostille Convention in 2007. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Registro Nacional de las Personas (RNP) in Honduras for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Honduran funeral director takes custody at Toncontin "
            "International Airport (TGU) in Tegucigalpa or Ramon Villeda "
            "Morales International Airport (SAP) in San Pedro Sula cargo "
            "terminal. The Registro Nacional de las Personas (RNP) "
            "registers the death and issues the certificado de defuncion "
            "in Spanish. Foreign documents require certified Spanish "
            "translation where required. Honduras joined the Hague "
            "Apostille Convention in 2007; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Honduran Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-honduras',
    },
    'guatemala': {
        'name': 'Guatemala',
        'slug': 'guatemala',
        'key': 'gt',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Guatemalan funeral director takes custody at La Aurora "
            "International Airport (GUA) in Guatemala City cargo terminal. "
            "Death registration in Guatemala is handled by the Registro "
            "Nacional de las Personas (RENAP). The acta de defuncion "
            "(death certificate) is issued in Spanish; all foreign documents "
            "require certified Spanish translation where required. Guatemala "
            "joined the Hague Apostille Convention in 2019; apostille "
            "certificates from member states are accepted. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Registro Nacional de las Personas (RENAP), Guatemala, 2025; "
            "FCDO Travel Advice: Guatemala, 2025.)"
        ),
        'consular_template': (
            "The Guatemalan Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Guatemala. "
            "Guatemala joined the Hague Apostille Convention in 2019. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Registro Nacional de las Personas (RENAP) in Guatemala for "
            "civil registration queries."
        ),
        'arrival_faq': (
            "The Guatemalan funeral director takes custody at La Aurora "
            "International Airport (GUA) in Guatemala City cargo terminal. "
            "The Registro Nacional de las Personas (RENAP) registers the "
            "death and issues the acta de defuncion in Spanish. Foreign "
            "documents require certified Spanish translation where required. "
            "Guatemala joined the Hague Apostille Convention in 2019; "
            "apostille certificates from member states are accepted. An "
            "embalming certificate and hermetically sealed coffin are "
            "required."
        ),
        'emergency_line': 'contact the Guatemalan Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-guatemala',
    },
    'el-salvador': {
        'name': 'El Salvador',
        'slug': 'el-salvador',
        'key': 'sv',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Salvadoran funeral director takes custody at San Oscar "
            "Arnulfo Romero International Airport (SAL) in San Salvador "
            "cargo terminal. Death registration in El Salvador is handled "
            "by the Registro Nacional de las Personas Naturales (RNPN). "
            "The certificado de defuncion (death certificate) is issued in "
            "Spanish; all foreign documents require certified Spanish "
            "translation where required. El Salvador joined the Hague "
            "Apostille Convention in 2001; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Registro Nacional de las Personas Naturales (RNPN), El "
            "Salvador, 2025; FCDO Travel Advice: El Salvador, 2025.)"
        ),
        'consular_template': (
            "The Salvadoran Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to El Salvador. "
            "El Salvador joined the Hague Apostille Convention in 2001. The "
            "Embassy cannot pay for or arrange repatriation. Contact the "
            "Registro Nacional de las Personas Naturales (RNPN) in El "
            "Salvador for civil registration queries."
        ),
        'arrival_faq': (
            "The Salvadoran funeral director takes custody at San Oscar "
            "Arnulfo Romero International Airport (SAL) in San Salvador "
            "cargo terminal. The Registro Nacional de las Personas Naturales "
            "(RNPN) registers the death and issues the certificado de "
            "defuncion in Spanish. Foreign documents require certified "
            "Spanish translation where required. El Salvador joined the "
            "Hague Apostille Convention in 2001; apostille certificates "
            "from member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Salvadoran Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-el-salvador',
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
            "can assist Irish nationals abroad."
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
            "a Hague Apostille Convention member."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Australia is widely available in all states and territories.",
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
    'russia': {
        'name': 'Russia',
        'emergency': '112',
        'registry': 'the local ZAGS (civil registry office)',
        'cert_name': 'svidetelstvo o smerti (death certificate)',
        'cert_lang': 'Russian',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The svidetelstvo o smerti (death certificate) is registered with "
            "the local ZAGS (Zapis Aktov Grazhdanskogo Sostoyaniya, civil registry "
            "office). Police take jurisdiction for violent or unexplained deaths. "
            "Russia is a Hague Apostille Convention member (accession 1992). The "
            "FCDO advises against all travel to Russia. British nationals in Russia "
            "should contact the British Embassy in Moscow, which continues to operate "
            "on a reduced basis. Consular access may be restricted in some "
            "circumstances."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation in Russia is available in major cities including Moscow "
            "and St Petersburg, though access varies significantly in more "
            "remote regions."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (police take jurisdiction; Sledstvenny Komitet may be involved)',
    },
    'turkey': {
        'name': 'Turkey',
        'emergency': '112',
        'registry': 'the local Nufus Mudurlugu (Directorate of Population)',
        'cert_name': 'olum belgesi (death certificate)',
        'cert_lang': 'Turkish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The olum belgesi (death certificate) is registered with the local "
            "Nufus Mudurlugu (Directorate of Population) under the Ministry of "
            "Interior. Police and the Cumhuriyet Bassavciligi (public prosecutor) "
            "take jurisdiction for violent or unexplained deaths. Turkey joined "
            "the Hague Apostille Convention in 2017. The British Embassy in Ankara "
            "and the British Consulates in Istanbul and Izmir can assist British "
            "nationals."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation is not available in Turkey. Remains must be prepared as "
            "a burial case or repatriated as a body for burial in the destination "
            "country."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Cumhuriyet Bassavciligi, public prosecutor takes jurisdiction)',
    },
    'china': {
        'name': 'China',
        'emergency': '110 (police) / 120 (ambulance)',
        'registry': 'the local Public Security Bureau (PSB) and civil affairs office',
        'cert_name': 'siwang zhengmingshu (death certificate)',
        'cert_lang': 'Mandarin Chinese',
        'overview': (
            "Call 110 for police or 120 for ambulance. Death is certified by a "
            "physician. The siwang zhengmingshu (death certificate) is issued "
            "by the local Public Security Bureau (PSB) and civil affairs office. "
            "Police take jurisdiction for violent or unexplained deaths. China "
            "is not a member of the Hague Apostille Convention; all foreign "
            "documents require full consular authentication by the relevant "
            "embassy or consulate in China. The British Embassy in Beijing and "
            "British Consulates in Shanghai, Guangzhou, and Chongqing can assist "
            "British nationals. All documentation is in Mandarin Chinese and "
            "requires certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': '10-16 weeks',
        'complexity': 'moderate-high',
        'cremation': (
            "Cremation is widely available in China and is required by law in "
            "many urban areas. The Chinese authorities may require local cremation "
            "before international repatriation in some circumstances. A cremation "
            "certificate is required for the export of cremated remains."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (police take jurisdiction; Public Security Bureau involved)',
    },
    'mexico': {
        'name': 'Mexico',
        'emergency': '911',
        'registry': 'the local Registro Civil (civil registry office)',
        'cert_name': 'acta de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician. "
            "The acta de defuncion (death certificate) is registered with the "
            "local Registro Civil (civil registry office). The Ministerio Publico "
            "(public prosecutor) takes jurisdiction for violent or unexplained "
            "deaths. Mexico is a Hague Apostille Convention member. The British "
            "Embassy in Mexico City and British Consulates in Cancun, Guadalajara, "
            "and Monterrey can assist British nationals."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Mexico is available in major cities and resort areas.",
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico, public prosecutor takes jurisdiction)',
    },
    'argentina': {
        'name': 'Argentina',
        'emergency': '911',
        'registry': 'the Registro Civil provincial (civil registry of the relevant province)',
        'cert_name': 'partida de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician. "
            "The partida de defuncion (death certificate) is registered with the "
            "Registro Civil provincial. The Ministerio Publico Fiscal (public "
            "prosecutor) takes jurisdiction for violent or unexplained deaths. "
            "Argentina is a Hague Apostille Convention member. The British Embassy "
            "in Buenos Aires can assist British nationals."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Argentina is available in Buenos Aires and major "
            "provincial cities."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico Fiscal, public prosecutor takes jurisdiction)',
    },
    'brazil': {
        'name': 'Brazil',
        'emergency': '190 (police) / 192 (ambulance) / 193 (fire)',
        'registry': 'the local Cartorio de Registro Civil (civil registry office)',
        'cert_name': 'certidao de obito (death certificate)',
        'cert_lang': 'Portuguese',
        'overview': (
            "Call 190 for police, 192 for ambulance, or 193 for fire. Death is "
            "certified by a physician. The certidao de obito (death certificate) "
            "is registered with the local Cartorio de Registro Civil (civil registry "
            "office). The Ministerio Publico (public prosecutor) takes jurisdiction "
            "for violent or unexplained deaths. Brazil joined the Hague Apostille "
            "Convention in 2016. The British Embassy in Brasilia and British "
            "Consulates in Sao Paulo and Rio de Janeiro can assist British nationals. "
            "ANVISA (the Brazilian Health Regulatory Agency) authorises the export "
            "of human remains; the certidao de obito and embalming certificate are "
            "required for ANVISA clearance."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Brazil is available in major cities.",
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico, public prosecutor takes jurisdiction)',
    },
}

ROUTES = [
    # R75 -- Israel x5
    {
        'origin': 'united-kingdom', 'dest': 'israel',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom has a significant Jewish community, one of the "
            "largest in Western Europe, with an estimated 292,000 Jewish "
            "residents (UK Census, 2021). British Jews maintain close family "
            "ties with Israel, and British nationals also visit Israel for "
            "tourism, business, and pilgrimages to religious sites. When someone "
            "from the United Kingdom dies and their family wishes to repatriate "
            "remains to Israel, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The Israeli Embassy "
            "in London can advise on documentation requirements for the Population "
            "and Immigration Authority (Ministry of Interior). In Jewish tradition, "
            "burial is ordinarily carried out as soon as possible after death; "
            "specialist handling is required. UK death certificates require certified "
            "Hebrew translation. Israel joined the Hague Apostille Convention in "
            "1977. (FCDO Travel Advice: Israel, 2025; Population and Immigration "
            "Authority, Ministry of Interior, Israel, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'israel',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has the largest Jewish diaspora community in the "
            "world outside Israel, with an estimated 7.6 million Jewish Americans "
            "(Jewish Virtual Library, 2023). Dual US-Israeli citizenship is common, "
            "and family connections between the United States and Israel are "
            "extensive across multiple generations. When an Israeli national or a "
            "person with Israeli family connections dies in the United States and "
            "their family wishes to repatriate remains to Israel, the death is "
            "registered with the state civil records office where the death "
            "occurred. The Israeli Embassy in Washington DC can advise on "
            "documentation requirements for the Population and Immigration "
            "Authority (Ministry of Interior). In Jewish tradition, burial is "
            "ordinarily carried out as soon as possible after death; specialist "
            "handling is required to expedite the international process. US death "
            "certificates require certified Hebrew translation. Israel joined the "
            "Hague Apostille Convention in 1977; US-issued apostille certificates "
            "are accepted. (FCDO Travel Advice: Israel, 2025; Population and "
            "Immigration Authority, Ministry of Interior, Israel, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'israel',
        'embassy_city': 'Paris',
        'intro': (
            "France has the largest Jewish community in Western Europe, estimated "
            "at around 450,000 people (Institut National d'Etudes Demographiques, "
            "2023). The France-Israel repatriation corridor is one of the most "
            "active in Europe, reflecting close family ties and significant "
            "emigration between the two countries. When an Israeli national or "
            "a person with Israeli family connections dies in France and their "
            "family wishes to repatriate remains to Israel, the death is registered "
            "with the local mairie (town hall). The acte de deces is issued in "
            "French and requires certified Hebrew translation for submission to "
            "the Population and Immigration Authority. In Jewish tradition, burial "
            "is ordinarily carried out as soon as possible after death; a specialist "
            "with experience of this corridor is recommended. Israel joined the "
            "Hague Apostille Convention in 1977; French-issued apostille "
            "certificates are accepted. (FCDO Travel Advice: Israel, 2025; "
            "Population and Immigration Authority, Ministry of Interior, "
            "Israel, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'israel',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a Jewish community partly reconstituted through "
            "post-Soviet migration from the former USSR in the 1990s and 2000s, "
            "and maintains close diplomatic and economic ties with Israel. "
            "German nationals also travel to Israel in substantial numbers. "
            "When an Israeli national or a person with Israeli family connections "
            "dies in Germany and their family wishes to repatriate remains to "
            "Israel, the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde is issued in German and requires "
            "certified Hebrew translation for submission to the Population and "
            "Immigration Authority. In Jewish tradition, burial is ordinarily "
            "carried out as soon as possible after death; a specialist with "
            "experience of Israeli burial requirements is recommended. Israel "
            "joined the Hague Apostille Convention in 1977; German-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: Israel, "
            "2025; Population and Immigration Authority, Ministry of Interior, "
            "Israel, 2025.)"
        ),
    },
    {
        'origin': 'russia', 'dest': 'israel',
        'embassy_city': 'Moscow',
        'intro': (
            "Russia was the source of significant Jewish emigration to Israel "
            "in the 1990s following the dissolution of the Soviet Union, and a "
            "large Russian-speaking community lives in Israel. Family ties between "
            "Russia and Israel remain extensive. When an Israeli national or a "
            "person with family connections in Israel dies in Russia, the death "
            "is registered with the local ZAGS (civil registry office). The "
            "svidetelstvo o smerti (death certificate) is issued in Russian and "
            "requires certified Hebrew translation for submission to the Population "
            "and Immigration Authority in Israel. The Israeli Embassy in Moscow "
            "can advise on documentation requirements. The FCDO advises against "
            "all travel to Russia. Israel joined the Hague Apostille Convention "
            "in 1977; Russian-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Russia, 2025; Population and Immigration "
            "Authority, Ministry of Interior, Israel, 2025.)"
        ),
    },
    # R75 -- Armenia x5
    {
        'origin': 'france', 'dest': 'armenia',
        'embassy_city': 'Paris',
        'intro': (
            "France has one of the largest Armenian diaspora communities in the "
            "world, with roots in the survivors of the 1915 Armenian Genocide "
            "who settled predominantly in Marseille, Lyon, and Paris. The "
            "Armenian-French community is estimated at around 500,000 people "
            "(Conseil de Coordination des Organisations Armeniennes de France, "
            "2023) and maintains strong cultural and family ties with Armenia. "
            "When an Armenian national or a person of Armenian heritage dies in "
            "France and their family wishes to repatriate remains to Armenia, "
            "the death is registered with the local mairie (town hall). The "
            "acte de deces is issued in French and requires certified Armenian "
            "translation for submission to the Civil Status Acts Registration "
            "Agency (CSARA). The Armenian Embassy in Paris can advise on "
            "documentation requirements. Armenia joined the Hague Apostille "
            "Convention in 2018; French-issued apostille certificates are "
            "accepted. (FCDO Travel Advice: Armenia, 2025; Civil Status Acts "
            "Registration Agency (CSARA), Armenia, 2025.)"
        ),
    },
    {
        'origin': 'russia', 'dest': 'armenia',
        'embassy_city': 'Moscow',
        'intro': (
            "Russia is home to one of the largest Armenian diaspora communities "
            "in the world, estimated at between one and two million people, "
            "concentrated in Moscow, Krasnodar, and other major cities. Many "
            "Armenian nationals work in Russia in construction, trade, and "
            "services. When an Armenian national dies in Russia and their family "
            "wishes to repatriate remains to Armenia, the death is registered "
            "with the local ZAGS (civil registry office). The svidetelstvo o "
            "smerti (death certificate) is issued in Russian and requires "
            "certified Armenian translation for submission to the Civil Status "
            "Acts Registration Agency (CSARA). The Armenian Embassy in Moscow "
            "can advise on documentation requirements. The FCDO advises against "
            "all travel to Russia. Armenia joined the Hague Apostille Convention "
            "in 2018; Russian-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Russia, 2025; Civil Status Acts Registration "
            "Agency (CSARA), Armenia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'armenia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant Armenian-American community, "
            "estimated at around one million people, concentrated in California "
            "(particularly the Los Angeles area), Massachusetts, and New York "
            "(Armenian National Committee of America, 2023). The community "
            "maintains close family and cultural ties with Armenia. When an "
            "Armenian national or a person of Armenian heritage dies in the "
            "United States and their family wishes to repatriate remains to "
            "Armenia, the death is registered with the state civil records "
            "office where the death occurred. The Armenian Embassy in Washington "
            "DC can advise on documentation requirements for the Civil Status "
            "Acts Registration Agency (CSARA). US death certificates require "
            "certified Armenian translation. Armenia joined the Hague Apostille "
            "Convention in 2018; US-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Armenia, 2025; Civil Status Acts Registration "
            "Agency (CSARA), Armenia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'armenia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany hosts a notable Armenian community, with nationals and "
            "persons of Armenian heritage working across various sectors in "
            "Berlin, Munich, and Cologne. Historical ties between Germany and "
            "Armenia include Germany's parliamentary recognition of the Armenian "
            "Genocide in 2016. When an Armenian national dies in Germany and "
            "their family wishes to repatriate remains to Armenia, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Armenian "
            "translation for submission to the Civil Status Acts Registration "
            "Agency (CSARA). The Armenian Embassy in Berlin can advise on "
            "documentation requirements. Armenia joined the Hague Apostille "
            "Convention in 2018; German-issued apostille certificates are "
            "accepted. (FCDO Travel Advice: Armenia, 2025; Civil Status Acts "
            "Registration Agency (CSARA), Armenia, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'armenia',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom has an Armenian community concentrated in "
            "London and the south-east, with the Armenian Apostolic Cathedral "
            "of St Sarkis in London reflecting the community's long presence "
            "in Britain. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Armenia, the death must "
            "be registered at the local register office in England and Wales "
            "within 5 days, or with the National Records of Scotland or GRONI "
            "in Northern Ireland. The Armenian Embassy in London can advise "
            "on documentation requirements for the Civil Status Acts "
            "Registration Agency (CSARA). UK death certificates require "
            "certified Armenian translation. Armenia joined the Hague Apostille "
            "Convention in 2018; UK-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Armenia, 2025; Civil Status Acts Registration "
            "Agency (CSARA), Armenia, 2025.)"
        ),
    },
    # R75 -- Azerbaijan x5
    {
        'origin': 'russia', 'dest': 'azerbaijan',
        'embassy_city': 'Moscow',
        'intro': (
            "Russia and Azerbaijan share significant ties as former Soviet "
            "republics, and the Azerbaijani diaspora in Russia is substantial, "
            "estimated at over one million people, concentrated in Moscow "
            "and other major cities. Azerbaijani nationals work across Russia "
            "in trade, construction, and agriculture. When an Azerbaijani "
            "national dies in Russia and their family wishes to repatriate "
            "remains to Azerbaijan, the death is registered with the local "
            "ZAGS (civil registry office). The svidetelstvo o smerti "
            "(death certificate) is issued in Russian and requires certified "
            "Azerbaijani translation for submission to the State Registry "
            "of Civil Acts (ARCA). The Azerbaijani Embassy in Moscow can "
            "advise on documentation requirements. The FCDO advises against "
            "all travel to Russia. Azerbaijan joined the Hague Apostille "
            "Convention in 2004; Russian-issued apostille certificates are "
            "accepted. (FCDO Travel Advice: Russia, 2025; State Registry "
            "of Civil Acts (ARCA), Azerbaijan, 2025.)"
        ),
    },
    {
        'origin': 'turkey', 'dest': 'azerbaijan',
        'embassy_city': 'Ankara',
        'intro': (
            "Turkey and Azerbaijan share close ethnic, linguistic, and cultural "
            "ties expressed in the phrase 'one nation, two states'. The two "
            "countries maintain a bilateral agreement facilitating travel and "
            "close cooperation across multiple sectors. The Turkey-Azerbaijan "
            "repatriation corridor is among the most established in the region. "
            "When a Turkish national or a person with Azerbaijani family "
            "connections dies in Turkey and their family wishes to repatriate "
            "remains to Azerbaijan, the death is registered with the local "
            "Nufus Mudurlugu (Directorate of Population). The olum belgesi "
            "(death certificate) is issued in Turkish, which is closely related "
            "to Azerbaijani, and requires certified Azerbaijani translation "
            "for submission to the State Registry of Civil Acts (ARCA). The "
            "Azerbaijani Embassy in Ankara can advise on documentation "
            "requirements. Azerbaijan joined the Hague Apostille Convention "
            "in 2004; Turkish-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Azerbaijan, 2025; State Registry of Civil "
            "Acts (ARCA), Azerbaijan, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'azerbaijan',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Azerbaijan have economic ties particularly in energy "
            "and trade, and an Azerbaijani community is present in Germany, "
            "with nationals working in medicine, academia, and business in "
            "Berlin and other cities. When an Azerbaijani national dies in "
            "Germany and their family wishes to repatriate remains to "
            "Azerbaijan, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde is issued in German and "
            "requires certified Azerbaijani translation for submission to "
            "the State Registry of Civil Acts (ARCA) under the Ministry of "
            "Justice. The Azerbaijani Embassy in Berlin can advise on "
            "documentation requirements. Azerbaijan joined the Hague Apostille "
            "Convention in 2004; German-issued apostille certificates are "
            "accepted. (FCDO Travel Advice: Azerbaijan, 2025; State Registry "
            "of Civil Acts (ARCA), Azerbaijan, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'azerbaijan',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom and Azerbaijan maintain significant economic "
            "ties, particularly in the energy sector through the Baku-Tbilisi-"
            "Ceyhan pipeline and related investments. The UK is a destination "
            "for Azerbaijani students, professionals, and business travellers. "
            "When someone from the United Kingdom dies and their family wishes "
            "to repatriate remains to Azerbaijan, the death must be registered "
            "at the local register office in England and Wales within 5 days, "
            "or with the National Records of Scotland or GRONI in Northern "
            "Ireland. The Azerbaijani Embassy in London can advise on "
            "documentation requirements for the State Registry of Civil Acts "
            "(ARCA). UK death certificates require certified Azerbaijani "
            "translation. Azerbaijan joined the Hague Apostille Convention "
            "in 2004; UK-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Azerbaijan, 2025; State Registry of Civil "
            "Acts (ARCA), Azerbaijan, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'azerbaijan',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Azerbaijan maintain diplomatic relations, "
            "and an Azerbaijani-American community is concentrated in New "
            "York, New Jersey, and California. The Azerbaijani Embassy in "
            "Washington DC handles consular matters for Azerbaijani nationals "
            "in the United States. When an Azerbaijani national dies in the "
            "United States and their family wishes to repatriate remains to "
            "Azerbaijan, the death is registered with the state civil records "
            "office where the death occurred. The Azerbaijani Embassy in "
            "Washington DC can advise on documentation requirements for the "
            "State Registry of Civil Acts (ARCA). US death certificates "
            "require certified Azerbaijani translation. Azerbaijan joined "
            "the Hague Apostille Convention in 2004; US-issued apostille "
            "certificates are accepted. (FCDO Travel Advice: Azerbaijan, "
            "2025; State Registry of Civil Acts (ARCA), Azerbaijan, 2025.)"
        ),
    },
    # R75 -- Kazakhstan x5
    {
        'origin': 'russia', 'dest': 'kazakhstan',
        'embassy_city': 'Moscow',
        'intro': (
            "Russia and Kazakhstan share the longest continuous land border "
            "between any two countries and significant historical ties as "
            "former Soviet republics. A large Russian-speaking population "
            "lives in Kazakhstan, and many Kazakhstani nationals study and "
            "work in Russia. When a Kazakhstani national dies in Russia and "
            "their family wishes to repatriate remains to Kazakhstan, the "
            "death is registered with the local ZAGS (civil registry office). "
            "The svidetelstvo o smerti (death certificate) is issued in "
            "Russian, which is also an official language in Kazakhstan, and "
            "requires certified Kazakh translation for submission to the "
            "Civil Registry Department under the Ministry of Justice. The "
            "Kazakhstani Embassy in Moscow can advise on documentation "
            "requirements. The FCDO advises against all travel to Russia. "
            "Kazakhstan joined the Hague Apostille Convention in 2001; "
            "Russian-issued apostille certificates are accepted. (FCDO Travel "
            "Advice: Russia, 2025; Civil Registry Department, Ministry of "
            "Justice, Kazakhstan, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'kazakhstan',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Kazakhstan have substantial economic ties in trade, "
            "energy, and engineering, and a community of Kazakhstani students "
            "and professionals is present in Germany. When a Kazakhstani "
            "national dies in Germany and their family wishes to repatriate "
            "remains to Kazakhstan, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in "
            "German and requires certified Kazakh or Russian translation for "
            "submission to the Civil Registry Department under the Ministry "
            "of Justice. The Kazakhstani Embassy in Berlin can advise on "
            "documentation requirements. Kazakhstan joined the Hague Apostille "
            "Convention in 2001; German-issued apostille certificates are "
            "accepted. (FCDO Travel Advice: Kazakhstan, 2025; Civil Registry "
            "Department, Ministry of Justice, Kazakhstan, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'kazakhstan',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom and Kazakhstan maintain significant economic "
            "ties through energy, mining, and trade, and there is a Kazakhstani "
            "student and professional community in the UK. The British Embassy "
            "in Astana is operational. When someone from the United Kingdom "
            "dies and their family wishes to repatriate remains to Kazakhstan, "
            "the death must be registered at the local register office in "
            "England and Wales within 5 days, or with the National Records "
            "of Scotland or GRONI in Northern Ireland. The Kazakhstani Embassy "
            "in London can advise on documentation requirements for the Civil "
            "Registry Department under the Ministry of Justice. UK death "
            "certificates require certified Kazakh or Russian translation. "
            "Kazakhstan joined the Hague Apostille Convention in 2001; "
            "UK-issued apostille certificates are accepted. (FCDO Travel "
            "Advice: Kazakhstan, 2025; Civil Registry Department, Ministry "
            "of Justice, Kazakhstan, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'kazakhstan',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Kazakhstan maintain a strategic partnership, "
            "and a Kazakhstani-American community is concentrated in New York, "
            "Washington DC, and California. The US Embassy in Astana is "
            "operational. When a Kazakhstani national dies in the United States "
            "and their family wishes to repatriate remains to Kazakhstan, the "
            "death is registered with the state civil records office where the "
            "death occurred. The Kazakhstani Embassy in Washington DC can advise "
            "on documentation requirements for the Civil Registry Department "
            "under the Ministry of Justice. US death certificates require "
            "certified Kazakh or Russian translation. Kazakhstan joined the "
            "Hague Apostille Convention in 2001; US-issued apostille certificates "
            "are accepted. (FCDO Travel Advice: Kazakhstan, 2025; Civil Registry "
            "Department, Ministry of Justice, Kazakhstan, 2025.)"
        ),
    },
    {
        'origin': 'china', 'dest': 'kazakhstan',
        'embassy_city': 'Beijing',
        'intro': (
            "China and Kazakhstan share a long border and significant economic "
            "ties through the Belt and Road Initiative and established Central "
            "Asian trade routes. Chinese nationals work in Kazakhstan in energy, "
            "construction, and trade. When a Chinese national or a person with "
            "Kazakhstani family connections dies in China and their family wishes "
            "to repatriate remains to Kazakhstan, the death is registered with "
            "the local Public Security Bureau (PSB) and civil affairs office. "
            "The siwang zhengmingshu (death certificate) is issued in Mandarin "
            "Chinese and requires certified Kazakh or Russian translation for "
            "submission to the Civil Registry Department. China is not a member "
            "of the Hague Apostille Convention; full consular authentication "
            "of all foreign documents is required by Kazakhstani authorities. "
            "The Kazakhstani Embassy in Beijing can advise on documentation "
            "requirements. (FCDO Travel Advice: Kazakhstan, 2025; Civil Registry "
            "Department, Ministry of Justice, Kazakhstan, 2025.)"
        ),
    },
    # R75 -- Paraguay x5
    {
        'origin': 'united-states', 'dest': 'paraguay',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Paraguayan-American community concentrated "
            "in New York, New Jersey, and Florida, with nationals also entering "
            "the United States for work and study. When a Paraguayan national "
            "or a person with Paraguayan family connections dies in the United "
            "States and their family wishes to repatriate remains to Paraguay, "
            "the death is registered with the state civil records office where "
            "the death occurred. The Paraguayan Embassy in Washington DC can "
            "advise on documentation requirements for the Registro Civil "
            "(Direccion General del Registro del Estado Civil de las Personas). "
            "US death certificates require certified Spanish translation. "
            "Paraguay joined the Hague Apostille Convention in 1991; US-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: Paraguay, "
            "2025; Direccion General del Registro del Estado Civil de las "
            "Personas, Paraguay, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'paraguay',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and Paraguay share the Spanish language and historical ties "
            "through the colonial era. A significant Paraguayan community lives "
            "and works in Spain, particularly in Madrid and Barcelona, with "
            "migration growing since the early 2000s. When a Paraguayan national "
            "dies in Spain and their family wishes to repatriate remains to "
            "Paraguay, the death is registered with the local Registro Civil. "
            "The certificado de defuncion is issued in Spanish, the official "
            "language of both countries, and may require no language translation "
            "for submission to the Registro Civil in Paraguay. The Paraguayan "
            "Embassy in Madrid can advise on documentation requirements for the "
            "Direccion General del Registro del Estado Civil de las Personas. "
            "Paraguay joined the Hague Apostille Convention in 1991; "
            "Spanish-issued apostille certificates are accepted. (FCDO Travel "
            "Advice: Paraguay, 2025; Direccion General del Registro del Estado "
            "Civil de las Personas, Paraguay, 2025.)"
        ),
    },
    {
        'origin': 'argentina', 'dest': 'paraguay',
        'embassy_city': 'Buenos Aires',
        'intro': (
            "Argentina and Paraguay share a land border and extensive family "
            "and economic ties. A large Paraguayan community lives and works "
            "in Argentina, particularly in Buenos Aires and the northern "
            "provinces, making this one of the most active repatriation "
            "corridors in South America for this origin-destination pair. "
            "When a Paraguayan national dies in Argentina, the death is "
            "registered with the Registro Civil provincial. The partida de "
            "defuncion is issued in Spanish and requires no language "
            "translation for submission to Paraguayan authorities. The "
            "Paraguayan Embassy in Buenos Aires can advise on documentation "
            "requirements. Both Argentina and Paraguay are Hague Apostille "
            "Convention members; Argentine-issued apostille certificates are "
            "accepted. (FCDO Travel Advice: Paraguay, 2025; Direccion General "
            "del Registro del Estado Civil de las Personas, Paraguay, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'paraguay',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has historic ties with Paraguay stemming from waves of "
            "German immigration in the 19th and 20th centuries, and communities "
            "of German-Paraguayan heritage maintain connections with Germany. "
            "When a Paraguayan national or a person of Paraguayan heritage "
            "dies in Germany and their family wishes to repatriate remains "
            "to Paraguay, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde is issued in German and "
            "requires certified Spanish translation for submission to the "
            "Registro Civil in Paraguay. The Paraguayan Embassy in Berlin "
            "can advise on documentation requirements for the Direccion "
            "General del Registro del Estado Civil de las Personas. Both "
            "Germany and Paraguay are Hague Apostille Convention members; "
            "German-issued apostille certificates are accepted. (FCDO Travel "
            "Advice: Paraguay, 2025; Direccion General del Registro del "
            "Estado Civil de las Personas, Paraguay, 2025.)"
        ),
    },
    {
        'origin': 'brazil', 'dest': 'paraguay',
        'embassy_city': 'Brasilia',
        'intro': (
            "Brazil and Paraguay share a long border and deep economic ties. "
            "Many Paraguayan nationals live and work in Brazil, and a community "
            "of Brazilian origin also resides in Paraguay. When a Paraguayan "
            "national dies in Brazil and their family wishes to repatriate "
            "remains to Paraguay, the death is registered with the local "
            "Cartorio de Registro Civil. The certidao de obito is issued in "
            "Portuguese and requires certified Spanish translation for "
            "submission to the Registro Civil in Paraguay. The Paraguayan "
            "Embassy in Brasilia can advise on documentation requirements "
            "for the Direccion General del Registro del Estado Civil de las "
            "Personas. Both Brazil and Paraguay are Hague Apostille Convention "
            "members; Brazilian-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Paraguay, 2025; Direccion General del "
            "Registro del Estado Civil de las Personas, Paraguay, 2025.)"
        ),
    },
    # R76 -- Uruguay x5
    {
        'origin': 'united-states', 'dest': 'uruguay',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Uruguayan-American community concentrated "
            "in New York, New Jersey, and Florida. When a Uruguayan national "
            "or a person with Uruguayan family connections dies in the United "
            "States and their family wishes to repatriate remains to Uruguay, "
            "the death is registered with the state civil records office where "
            "the death occurred. The Uruguayan Embassy in Washington DC can "
            "advise on documentation requirements for the Direccion General "
            "del Registro del Estado Civil. US death certificates require "
            "certified Spanish translation. Uruguay joined the Hague Apostille "
            "Convention in 2012; US-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Uruguay, 2025; Direccion General del Registro "
            "del Estado Civil, Uruguay, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'uruguay',
        'embassy_city': 'Madrid',
        'intro': (
            "Uruguay and Spain share the Spanish language and strong historical "
            "ties through the significant Spanish immigration of the 19th and "
            "20th centuries. A Uruguayan community lives and works in Spain, "
            "and many Uruguayan nationals hold Spanish citizenship. When a "
            "Uruguayan national dies in Spain and their family wishes to "
            "repatriate remains to Uruguay, the death is registered with the "
            "local Registro Civil. The certificado de defuncion is issued in "
            "Spanish, the official language of both countries, and requires "
            "no language translation for submission to Uruguayan authorities. "
            "The Uruguayan Embassy in Madrid can advise on documentation "
            "requirements for the Direccion General del Registro del Estado "
            "Civil. Both Spain and Uruguay are Hague Apostille Convention "
            "members; Spanish-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Uruguay, 2025; Direccion General del "
            "Registro del Estado Civil, Uruguay, 2025.)"
        ),
    },
    {
        'origin': 'argentina', 'dest': 'uruguay',
        'embassy_city': 'Buenos Aires',
        'intro': (
            "Argentina and Uruguay are separated by the Rio de la Plata "
            "estuary and share close cultural, economic, and family ties. "
            "Buenos Aires and Montevideo are connected by frequent ferry "
            "and air services, and movement between the two countries is "
            "constant. When a Uruguayan national dies in Argentina, the "
            "death is registered with the Registro Civil provincial. The "
            "partida de defuncion is issued in Spanish and requires no "
            "language translation for submission to Uruguayan authorities. "
            "The Uruguayan Embassy in Buenos Aires can advise on "
            "documentation requirements for the Direccion General del "
            "Registro del Estado Civil. Both countries are Hague Apostille "
            "Convention members; Argentine-issued apostille certificates "
            "are accepted. (FCDO Travel Advice: Uruguay, 2025; Direccion "
            "General del Registro del Estado Civil, Uruguay, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'uruguay',
        'embassy_city': 'Rome',
        'intro': (
            "Uruguay received significant Italian immigration in the late "
            "19th and early 20th centuries, and Italian is among the most "
            "common ancestral backgrounds for Uruguayan nationals. Family "
            "ties between Uruguay and Italy remain strong, and a Uruguayan "
            "community lives and works in Italy, many holding Italian "
            "citizenship through descent. When a Uruguayan national dies "
            "in Italy and their family wishes to repatriate remains to "
            "Uruguay, the death is registered with the local Ufficio di "
            "Stato Civile. The atto di morte is issued in Italian and "
            "requires certified Spanish translation for submission to the "
            "Direccion General del Registro del Estado Civil in Uruguay. "
            "The Uruguayan Embassy in Rome can advise on documentation "
            "requirements. Uruguay joined the Hague Apostille Convention "
            "in 2012; Italian-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Uruguay, 2025; Direccion General del "
            "Registro del Estado Civil, Uruguay, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'uruguay',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has historic ties with Uruguay through 19th-century "
            "immigration, and a community of Uruguayan nationals lives and "
            "works in Germany. When a Uruguayan national dies in Germany "
            "and their family wishes to repatriate remains to Uruguay, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires certified "
            "Spanish translation for submission to the Direccion General "
            "del Registro del Estado Civil in Uruguay. The Uruguayan Embassy "
            "in Berlin can advise on documentation requirements. Both Germany "
            "and Uruguay are Hague Apostille Convention members; German-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: Uruguay, "
            "2025; Direccion General del Registro del Estado Civil, Uruguay, "
            "2025.)"
        ),
    },
    # R76 -- Bolivia x5
    {
        'origin': 'united-states', 'dest': 'bolivia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Bolivian-American community concentrated "
            "in the Washington DC metropolitan area, Virginia, and California. "
            "When a Bolivian national or a person with Bolivian family "
            "connections dies in the United States and their family wishes "
            "to repatriate remains to Bolivia, the death is registered with "
            "the state civil records office where the death occurred. The "
            "Bolivian Embassy in Washington DC can advise on documentation "
            "requirements for SERECI (Servicio de Registro Civico). US "
            "death certificates require certified Spanish translation. Bolivia "
            "joined the Hague Apostille Convention in 2009; US-issued apostille "
            "certificates are accepted. (FCDO Travel Advice: Bolivia, 2025; "
            "SERECI (Servicio de Registro Civico), Bolivia, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'bolivia',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain has a large Bolivian community, among the largest Latin "
            "American diaspora groups in Spain, concentrated in Madrid and "
            "Barcelona following the migration wave of the early 2000s. "
            "When a Bolivian national dies in Spain and their family wishes "
            "to repatriate remains to Bolivia, the death is registered with "
            "the local Registro Civil. The certificado de defuncion is issued "
            "in Spanish, the official language of both countries, and may "
            "require no language translation for submission to SERECI. The "
            "Bolivian Embassy in Madrid can advise on documentation requirements "
            "for the Servicio de Registro Civico (SERECI). Bolivia joined "
            "the Hague Apostille Convention in 2009; Spanish-issued apostille "
            "certificates are accepted. (FCDO Travel Advice: Bolivia, 2025; "
            "SERECI (Servicio de Registro Civico), Bolivia, 2025.)"
        ),
    },
    {
        'origin': 'argentina', 'dest': 'bolivia',
        'embassy_city': 'Buenos Aires',
        'intro': (
            "Argentina and Bolivia share a land border, and a large Bolivian "
            "community lives and works in Argentina, particularly in Buenos "
            "Aires and the northern provinces of Jujuy and Salta. The "
            "Argentina-Bolivia repatriation corridor is one of the most "
            "active in South America. When a Bolivian national dies in "
            "Argentina, the death is registered with the Registro Civil "
            "provincial. The partida de defuncion is issued in Spanish "
            "and requires no language translation for submission to SERECI "
            "(Servicio de Registro Civico) in Bolivia. The Bolivian Embassy "
            "in Buenos Aires can advise on documentation requirements. Both "
            "Argentina and Bolivia are Hague Apostille Convention members; "
            "Argentine-issued apostille certificates are accepted. (FCDO "
            "Travel Advice: Bolivia, 2025; SERECI, Bolivia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'bolivia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains development cooperation ties with Bolivia "
            "and a small Bolivian community lives in Germany. German nationals "
            "also visit Bolivia for ecotourism, trekking, and cultural travel. "
            "When a Bolivian national dies in Germany and their family wishes "
            "to repatriate remains to Bolivia, the death is registered with "
            "the local Standesamt (civil registry). The Sterbeurkunde is "
            "issued in German and requires certified Spanish translation for "
            "submission to SERECI (Servicio de Registro Civico) in Bolivia. "
            "The Bolivian Embassy in Berlin can advise on documentation "
            "requirements. Bolivia joined the Hague Apostille Convention in "
            "2009; German-issued apostille certificates are accepted. Deaths "
            "in high-altitude or remote areas in Bolivia may require "
            "additional local procedures. (FCDO Travel Advice: Bolivia, "
            "2025; SERECI (Servicio de Registro Civico), Bolivia, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'bolivia',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains development ties with Bolivia and French nationals "
            "visit Bolivia for ecotourism and cultural travel to sites including "
            "Salar de Uyuni and the Amazon basin. When a Bolivian national "
            "dies in France and their family wishes to repatriate remains to "
            "Bolivia, the death is registered with the local mairie (town "
            "hall). The acte de deces is issued in French and requires "
            "certified Spanish translation for submission to SERECI (Servicio "
            "de Registro Civico) in Bolivia. The Bolivian Embassy in Paris "
            "can advise on documentation requirements. Bolivia joined the "
            "Hague Apostille Convention in 2009; French-issued apostille "
            "certificates are accepted. (FCDO Travel Advice: Bolivia, 2025; "
            "SERECI (Servicio de Registro Civico), Bolivia, 2025.)"
        ),
    },
    # R76 -- Honduras x5
    {
        'origin': 'united-states', 'dest': 'honduras',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States is home to the largest Honduran diaspora "
            "community in the world, with an estimated 1.1 million "
            "Honduran-born residents (US Census Bureau, 2023), concentrated "
            "in New York, Florida, Texas, and California. The Honduras-US "
            "repatriation corridor is one of the most active in the Americas. "
            "When a Honduran national dies in the United States and their "
            "family wishes to repatriate remains to Honduras, the death is "
            "registered with the state civil records office where the death "
            "occurred. The Honduran Embassy in Washington DC can advise on "
            "documentation requirements for the Registro Nacional de las "
            "Personas (RNP). US death certificates require certified Spanish "
            "translation. Honduras joined the Hague Apostille Convention in "
            "2007; US-issued apostille certificates are accepted. (FCDO Travel "
            "Advice: Honduras, 2025; Registro Nacional de las Personas (RNP), "
            "Honduras, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'honduras',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain has a significant Honduran community, particularly in "
            "Madrid and other major cities, with migration driven by language "
            "ties and economic opportunity. When a Honduran national dies "
            "in Spain and their family wishes to repatriate remains to "
            "Honduras, the death is registered with the local Registro Civil. "
            "The certificado de defuncion is issued in Spanish, the official "
            "language of both countries, and may require no language "
            "translation for submission to the Registro Nacional de las "
            "Personas (RNP) in Honduras. The Honduran Embassy in Madrid "
            "can advise on documentation requirements. Both Spain and "
            "Honduras are Hague Apostille Convention members; Spanish-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: "
            "Honduras, 2025; Registro Nacional de las Personas (RNP), "
            "Honduras, 2025.)"
        ),
    },
    {
        'origin': 'mexico', 'dest': 'honduras',
        'embassy_city': 'Mexico City',
        'intro': (
            "Mexico and Honduras are connected through Central American "
            "migration routes, and a significant Honduran community lives "
            "and works in Mexico, both as migrant workers and longer-term "
            "residents in cities and border regions. When a Honduran national "
            "dies in Mexico and their family wishes to repatriate remains "
            "to Honduras, the death is registered with the local Registro "
            "Civil. The acta de defuncion is issued in Spanish and requires "
            "no language translation for submission to the Registro Nacional "
            "de las Personas (RNP) in Honduras. The Honduran Embassy in "
            "Mexico City can advise on documentation requirements. Both "
            "Mexico and Honduras are Hague Apostille Convention members; "
            "Mexican-issued apostille certificates are accepted. (FCDO "
            "Travel Advice: Honduras, 2025; Registro Nacional de las "
            "Personas (RNP), Honduras, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'honduras',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a Honduran community concentrated in Ontario and "
            "Quebec, with nationals working in agriculture, construction, "
            "and services. The Canadian Embassy in Tegucigalpa is operational. "
            "When a Honduran national dies in Canada and their family wishes "
            "to repatriate remains to Honduras, the death is registered with "
            "the provincial civil records registry. The death certificate is "
            "issued in English or French and requires certified Spanish "
            "translation for submission to the Registro Nacional de las "
            "Personas (RNP) in Honduras. The Honduran Embassy in Ottawa "
            "can advise on documentation requirements. Both Canada and "
            "Honduras are Hague Apostille Convention members; Canadian-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: "
            "Honduras, 2025; Registro Nacional de las Personas (RNP), "
            "Honduras, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'honduras',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains bilateral ties with Honduras through development "
            "cooperation, and a small Honduran community lives in Germany. "
            "When a Honduran national dies in Germany and their family "
            "wishes to repatriate remains to Honduras, the death is registered "
            "with the local Standesamt (civil registry). The Sterbeurkunde "
            "is issued in German and requires certified Spanish translation "
            "for submission to the Registro Nacional de las Personas (RNP) "
            "in Honduras. The Honduran Embassy in Berlin can advise on "
            "documentation requirements. Both Germany and Honduras are Hague "
            "Apostille Convention members; German-issued apostille certificates "
            "are accepted. (FCDO Travel Advice: Honduras, 2025; Registro "
            "Nacional de las Personas (RNP), Honduras, 2025.)"
        ),
    },
    # R76 -- Guatemala x5
    {
        'origin': 'united-states', 'dest': 'guatemala',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has the largest Guatemalan diaspora community "
            "outside Guatemala, with an estimated 1.7 million Guatemalan-born "
            "residents (US Census Bureau, 2023), concentrated in California, "
            "Florida, Texas, and New York. When a Guatemalan national dies "
            "in the United States and their family wishes to repatriate "
            "remains to Guatemala, the death is registered with the state "
            "civil records office where the death occurred. The Guatemalan "
            "Embassy in Washington DC can advise on documentation requirements "
            "for the Registro Nacional de las Personas (RENAP). US death "
            "certificates require certified Spanish translation. Guatemala "
            "joined the Hague Apostille Convention in 2019; US-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: "
            "Guatemala, 2025; Registro Nacional de las Personas (RENAP), "
            "Guatemala, 2025.)"
        ),
    },
    {
        'origin': 'mexico', 'dest': 'guatemala',
        'embassy_city': 'Mexico City',
        'intro': (
            "Mexico and Guatemala share a land border, and a significant "
            "Guatemalan community lives in southern Mexico, particularly "
            "in Chiapas and Oaxaca, with nationals working in agriculture "
            "and seasonal labour. When a Guatemalan national dies in Mexico "
            "and their family wishes to repatriate remains to Guatemala, "
            "the death is registered with the local Registro Civil. The "
            "acta de defuncion is issued in Spanish and requires no language "
            "translation for submission to the Registro Nacional de las "
            "Personas (RENAP) in Guatemala. The Guatemalan Embassy in Mexico "
            "City can advise on documentation requirements. Both Mexico and "
            "Guatemala are Hague Apostille Convention members; Mexican-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: "
            "Guatemala, 2025; Registro Nacional de las Personas (RENAP), "
            "Guatemala, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'guatemala',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and Guatemala share the Spanish language and a colonial "
            "history, and a Guatemalan community lives and works in Spain, "
            "particularly in Madrid and Barcelona. When a Guatemalan national "
            "dies in Spain and their family wishes to repatriate remains to "
            "Guatemala, the death is registered with the local Registro Civil. "
            "The certificado de defuncion is issued in Spanish and may require "
            "no language translation for submission to RENAP in Guatemala. "
            "The Guatemalan Embassy in Madrid can advise on documentation "
            "requirements. Guatemala joined the Hague Apostille Convention "
            "in 2019; Spanish-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Guatemala, 2025; Registro Nacional de las "
            "Personas (RENAP), Guatemala, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'guatemala',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a Guatemalan community concentrated in Ontario and "
            "British Columbia, with roots partly in refugee resettlement "
            "following the Guatemalan Civil War of the 1980s. When a "
            "Guatemalan national dies in Canada and their family wishes to "
            "repatriate remains to Guatemala, the death is registered with "
            "the provincial civil records registry. The death certificate "
            "is issued in English or French and requires certified Spanish "
            "translation for submission to RENAP (Registro Nacional de las "
            "Personas). The Guatemalan Embassy in Ottawa can advise on "
            "documentation requirements. Guatemala joined the Hague Apostille "
            "Convention in 2019; Canadian-issued apostille certificates are "
            "accepted. (FCDO Travel Advice: Guatemala, 2025; Registro "
            "Nacional de las Personas (RENAP), Guatemala, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'guatemala',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains development cooperation ties with Guatemala "
            "and German nationals visit Guatemala for cultural heritage "
            "tourism, including Antigua and the Maya archaeological sites. "
            "A small Guatemalan community lives in Germany. When a Guatemalan "
            "national dies in Germany and their family wishes to repatriate "
            "remains to Guatemala, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in "
            "German and requires certified Spanish translation for submission "
            "to RENAP (Registro Nacional de las Personas). The Guatemalan "
            "Embassy in Berlin can advise on documentation requirements. "
            "Guatemala joined the Hague Apostille Convention in 2019; "
            "German-issued apostille certificates are accepted. (FCDO Travel "
            "Advice: Guatemala, 2025; Registro Nacional de las Personas "
            "(RENAP), Guatemala, 2025.)"
        ),
    },
    # R76 -- El Salvador x5
    {
        'origin': 'united-states', 'dest': 'el-salvador',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has the largest Salvadoran diaspora community "
            "in the world, with an estimated 1.4 million Salvadoran-born "
            "residents (US Census Bureau, 2023), concentrated in California, "
            "Texas, New York, and the Washington DC metropolitan area. The "
            "US-El Salvador repatriation corridor is one of the most active "
            "in the Americas. When a Salvadoran national dies in the United "
            "States and their family wishes to repatriate remains to El "
            "Salvador, the death is registered with the state civil records "
            "office where the death occurred. The Salvadoran Embassy in "
            "Washington DC can advise on documentation requirements for the "
            "Registro Nacional de las Personas Naturales (RNPN). US death "
            "certificates require certified Spanish translation. El Salvador "
            "joined the Hague Apostille Convention in 2001; US-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: El "
            "Salvador, 2025; Registro Nacional de las Personas Naturales "
            "(RNPN), El Salvador, 2025.)"
        ),
    },
    {
        'origin': 'mexico', 'dest': 'el-salvador',
        'embassy_city': 'Mexico City',
        'intro': (
            "Mexico and El Salvador share a Spanish-speaking cultural context "
            "and significant migration connections. Many Salvadoran nationals "
            "pass through Mexico, and a community lives in Mexican cities. "
            "When a Salvadoran national dies in Mexico and their family wishes "
            "to repatriate remains to El Salvador, the death is registered "
            "with the local Registro Civil. The acta de defuncion is issued "
            "in Spanish and requires no language translation for submission "
            "to the Registro Nacional de las Personas Naturales (RNPN) in "
            "El Salvador. The Salvadoran Embassy in Mexico City can advise "
            "on documentation requirements. Both Mexico and El Salvador are "
            "Hague Apostille Convention members; Mexican-issued apostille "
            "certificates are accepted. (FCDO Travel Advice: El Salvador, "
            "2025; Registro Nacional de las Personas Naturales (RNPN), "
            "El Salvador, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'el-salvador',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain has a Salvadoran community, particularly in Madrid, "
            "drawn by language ties and accessible migration routes. When "
            "a Salvadoran national dies in Spain and their family wishes "
            "to repatriate remains to El Salvador, the death is registered "
            "with the local Registro Civil. The certificado de defuncion "
            "is issued in Spanish and may require no language translation "
            "for submission to the Registro Nacional de las Personas "
            "Naturales (RNPN) in El Salvador. The Salvadoran Embassy in "
            "Madrid can advise on documentation requirements. El Salvador "
            "joined the Hague Apostille Convention in 2001; Spanish-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: El "
            "Salvador, 2025; Registro Nacional de las Personas Naturales "
            "(RNPN), El Salvador, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'el-salvador',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a Salvadoran community concentrated in Toronto, "
            "Montreal, and Vancouver, with roots in the refugee resettlement "
            "of the 1980s during the Salvadoran Civil War. When a Salvadoran "
            "national dies in Canada and their family wishes to repatriate "
            "remains to El Salvador, the death is registered with the "
            "provincial civil records registry. The death certificate is "
            "issued in English or French and requires certified Spanish "
            "translation for submission to the Registro Nacional de las "
            "Personas Naturales (RNPN). The Salvadoran Embassy in Ottawa "
            "can advise on documentation requirements. El Salvador joined "
            "the Hague Apostille Convention in 2001; Canadian-issued "
            "apostille certificates are accepted. (FCDO Travel Advice: "
            "El Salvador, 2025; Registro Nacional de las Personas Naturales "
            "(RNPN), El Salvador, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'el-salvador',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains development cooperation ties with El Salvador "
            "and a small Salvadoran community lives in Germany. When a "
            "Salvadoran national dies in Germany and their family wishes "
            "to repatriate remains to El Salvador, the death is registered "
            "with the local Standesamt (civil registry). The Sterbeurkunde "
            "is issued in German and requires certified Spanish translation "
            "for submission to the Registro Nacional de las Personas Naturales "
            "(RNPN) in El Salvador. The Salvadoran Embassy in Berlin can "
            "advise on documentation requirements. El Salvador joined the "
            "Hague Apostille Convention in 2001; German-issued apostille "
            "certificates are accepted. (FCDO Travel Advice: El Salvador, "
            "2025; Registro Nacional de las Personas Naturales (RNPN), "
            "El Salvador, 2025.)"
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
