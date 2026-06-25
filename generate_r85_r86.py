#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R85-R86.

   R85 (25 routes, START_VARIANT=2=C):
     Jordan x5:    france, italy, netherlands, sweden, norway
     Sri Lanka x5: germany, netherlands, sweden, norway, spain
     Nepal x5:     germany, italy, netherlands, sweden, norway
     Mexico x5:    australia, france, germany, spain, italy
     Brazil x5:    australia, france, netherlands, sweden, norway

   R86 (25 routes, continues from R85):
     Colombia x5:  australia, france, sweden, norway, portugal
     Argentina x5: australia, canada, france, germany, netherlands
     Poland x5:    australia, canada, italy, spain, sweden
     Romania x5:   united-states, australia, canada, netherlands, sweden
     Cuba x5:      australia, france, italy, netherlands, sweden

   Template rotation: R84 ended on variant B (idx=1). R85 starts at C (idx=2).
   START_VARIANT=2 applies across all 50 routes as one continuous cycle.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 2  # C

DEST_META = {
    'jordan': {
        'name': 'Jordan',
        'slug': 'jordan',
        'key': 'jo',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Jordanian funeral director takes custody at Queen Alia "
            "International Airport (AMM) cargo terminal in Amman. The Civil "
            "Status and Passports Department (CSPA) handles civil registration "
            "for foreign nationals. The public prosecutor (an-Niyaba al-Amma) "
            "takes jurisdiction for any case with an unclear cause of death. "
            "All foreign documents require certified Arabic translation. Jordan "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication by the Jordanian Embassy or Consulate in the country "
            "of origin is required for all documents. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. For "
            "Muslim remains, Islamic burial law applies and prompt burial is "
            "expected. (Jordanian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Jordanian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Jordan. Jordan is "
            "not a Hague Apostille Convention member; all foreign documents "
            "require full consular authentication. The Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Jordanian funeral director takes custody at Queen Alia "
            "International Airport (AMM) cargo terminal in Amman. The Civil "
            "Status and Passports Department (CSPA) registers the death. The "
            "public prosecutor (an-Niyaba al-Amma) takes jurisdiction where "
            "the cause of death is unclear. All foreign documents require "
            "certified Arabic translation and full consular authentication. "
            "Jordan is not a Hague Apostille member. For Muslim remains, "
            "Islamic burial law applies and prompt burial is expected. An "
            "embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Jordanian Embassy in the origin country',
        'hub_url': 'repatriation-from-jordan',
    },
    'sri-lanka': {
        'name': 'Sri Lanka',
        'slug': 'sri-lanka',
        'key': 'lk',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) cargo terminal near Colombo. The "
            "Registrar General's Department handles civil registration for "
            "foreign nationals. Police and the Magistrate's Court take "
            "jurisdiction for violent or unexplained deaths. All foreign "
            "documents require certified Sinhala, Tamil, or English translation. "
            "Sri Lanka is not a member of the Hague Apostille Convention; full "
            "consular authentication by the Sri Lankan Embassy or High Commission "
            "in the country of origin is required. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "Cremation is available at approved facilities; Muslim remains "
            "require burial. (Sri Lanka Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Sri Lankan Embassy or High Commission in {city} can advise "
            "on documentation requirements for repatriation to Sri Lanka. "
            "Sri Lanka is not a Hague Apostille Convention member; full "
            "consular authentication through the Embassy in {city} is required. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Sri Lankan funeral director takes custody at Bandaranaike "
            "International Airport (CMB) cargo terminal. The Registrar "
            "General's Department registers the death. Police and the "
            "Magistrate's Court take jurisdiction for violent or unexplained "
            "deaths. All foreign documents require certified Sinhala, Tamil, "
            "or English translation. Sri Lanka is not a Hague Apostille member; "
            "full consular authentication is required. An embalming certificate "
            "and hermetically sealed coffin are required. Cremation is available "
            "at approved facilities; Muslim remains require burial."
        ),
        'emergency_line': 'contact the Sri Lankan Embassy or High Commission in the origin country',
        'hub_url': 'repatriation-from-sri-lanka',
    },
    'nepal': {
        'name': 'Nepal',
        'slug': 'nepal',
        'key': 'np',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Nepalese funeral director takes custody at Tribhuvan "
            "International Airport (KTM) cargo terminal in Kathmandu. The "
            "Ward Office under the Department of Civil Registration (DCR) "
            "handles civil registration. Nepal Police and the District "
            "Administration Office (DAO) take jurisdiction for violent or "
            "unexplained deaths. All foreign documents require certified Nepali "
            "translation. Nepal is not a member of the Hague Apostille "
            "Convention; full consular authentication by the Nepalese Embassy "
            "or Consulate in the country of origin is required. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. Hindu cremation traditions are predominant in Nepal; "
            "for Hindu remains, prompt repatriation is expected. Buddhist and "
            "other religious traditions also apply. "
            "(Nepal Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Nepalese Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Nepal. Nepal is "
            "not a Hague Apostille Convention member; full consular "
            "authentication through the Embassy in {city} is required. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Nepalese funeral director takes custody at Tribhuvan "
            "International Airport (KTM) cargo terminal in Kathmandu. The "
            "Ward Office under the Department of Civil Registration (DCR) "
            "registers the death. Nepal Police and the District Administration "
            "Office (DAO) take jurisdiction for violent or unexplained deaths. "
            "All foreign documents require certified Nepali translation. Nepal "
            "is not a Hague Apostille member; full consular authentication is "
            "required. Hindu cremation traditions are predominant; for Hindu "
            "remains, prompt repatriation is expected. An embalming certificate "
            "and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Nepalese Embassy in the origin country',
        'hub_url': 'repatriation-from-nepal',
    },
    'mexico': {
        'name': 'Mexico',
        'slug': 'mexico',
        'key': 'mx',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Mexican funeral director takes custody at Benito Juarez "
            "International Airport Mexico City (MEX) or Guadalajara "
            "International Airport (GDL) cargo terminal, depending on the "
            "family's destination. The Registro Civil registers the death. "
            "SEMEFO (Servicio Medico Forense) takes jurisdiction for violent "
            "or unexplained deaths; this adds 1 to 3 weeks to the process. "
            "Mexico joined the Hague Apostille Convention in 1995; apostille "
            "certificates from member states are accepted. COFEPRIS (health "
            "authority) clearance is required for all incoming remains. A "
            "hermetically sealed coffin and embalming certificate are required "
            "for all air imports. "
            "(Mexico Secretaria de Relaciones Exteriores, 2025.)"
        ),
        'consular_template': (
            "The Mexican Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Mexico. Mexico "
            "is a Hague Apostille Convention member (joined 1995); apostille "
            "certificates from member states are accepted. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Mexican funeral director takes custody at Benito Juarez "
            "International Airport Mexico City (MEX) or Guadalajara (GDL) "
            "cargo terminal. The Registro Civil registers the death. SEMEFO "
            "(Servicio Medico Forense) takes jurisdiction where the cause of "
            "death is violent or unclear; this adds 1 to 3 weeks. Mexico "
            "joined the Hague Apostille Convention in 1995; apostille "
            "certificates from member states are accepted. COFEPRIS clearance "
            "is required for all incoming remains. A hermetically sealed coffin "
            "and embalming certificate are required."
        ),
        'emergency_line': 'contact the Mexican Embassy in the origin country',
        'hub_url': 'repatriation-from-mexico',
    },
    'brazil': {
        'name': 'Brazil',
        'slug': 'brazil',
        'key': 'br',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '6-12 weeks',
        'reception': (
            "The Brazilian funeral director takes custody at Guarulhos "
            "International Airport Sao Paulo (GRU) or Galeao International "
            "Airport Rio de Janeiro (GIG) cargo terminal, depending on the "
            "family's destination. The Cartorio de Registro Civil (civil "
            "registry) registers the death. The Instituto Medico Legal (IML) "
            "takes jurisdiction for violent or unexplained deaths. ANVISA "
            "(Agencia Nacional de Vigilancia Sanitaria) clearance is required "
            "for all incoming human remains before final disposition. Brazil "
            "joined the Hague Apostille Convention in 2016; apostille "
            "certificates from member states are accepted. A hermetically "
            "sealed coffin and embalming certificate are required for all "
            "air imports. (Brazil Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Brazilian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Brazil. Brazil "
            "is a Hague Apostille Convention member (joined 2016); apostille "
            "certificates from member states are accepted. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Brazilian funeral director takes custody at Guarulhos "
            "International Airport Sao Paulo (GRU) or Galeao International "
            "Airport Rio de Janeiro (GIG) cargo terminal. The Cartorio de "
            "Registro Civil registers the death. The Instituto Medico Legal "
            "(IML) takes jurisdiction where the cause of death is violent or "
            "unclear. ANVISA (Agencia Nacional de Vigilancia Sanitaria) "
            "clearance is required for all incoming remains. Brazil joined "
            "the Hague Apostille Convention in 2016; apostille certificates "
            "from member states are accepted. A hermetically sealed coffin "
            "and embalming certificate are required."
        ),
        'emergency_line': 'contact the Brazilian Embassy in the origin country',
        'hub_url': 'repatriation-from-brazil',
    },
    'colombia': {
        'name': 'Colombia',
        'slug': 'colombia',
        'key': 'co',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport Bogota (BOG) cargo terminal. The "
            "Registraduria Nacional del Estado Civil handles civil registration "
            "through local registraduria offices. The Instituto Nacional de "
            "Medicina Legal y Ciencias Forenses (Medicina Legal) takes "
            "jurisdiction for violent or unexplained deaths; this adds 1 to "
            "3 weeks to the process. Colombia joined the Hague Apostille "
            "Convention in 1991; apostille certificates from member states "
            "are accepted. A hermetically sealed coffin and embalming "
            "certificate are required for all air imports. "
            "(Colombia Cancilleria, 2025.)"
        ),
        'consular_template': (
            "The Colombian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Colombia. "
            "Colombia is a Hague Apostille Convention member (joined 1991); "
            "apostille certificates from member states are accepted. The "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport Bogota (BOG) cargo terminal. The "
            "Registraduria Nacional del Estado Civil registers the death. "
            "The Instituto Nacional de Medicina Legal y Ciencias Forenses "
            "(Medicina Legal) takes jurisdiction for violent or unexplained "
            "deaths; this adds 1 to 3 weeks. Colombia joined the Hague "
            "Apostille Convention in 1991; apostille certificates from member "
            "states are accepted. A hermetically sealed coffin and embalming "
            "certificate are required."
        ),
        'emergency_line': 'contact the Colombian Embassy in the origin country',
        'hub_url': 'repatriation-from-colombia',
    },
    'argentina': {
        'name': 'Argentina',
        'slug': 'argentina',
        'key': 'ar',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Argentine funeral director takes custody at Ministro Pistarini "
            "International Airport Buenos Aires (EZE) cargo terminal. The "
            "provincial Registro Civil registers the death. The Cuerpo Medico "
            "Forense and judicial authorities take jurisdiction for violent or "
            "unexplained deaths. Argentina joined the Hague Apostille Convention "
            "in 1988; apostille certificates from member states are accepted. "
            "All foreign documents require certified Spanish translation where "
            "applicable. A hermetically sealed coffin and embalming certificate "
            "are required for all air imports. "
            "(Argentina Cancilleria, 2025.)"
        ),
        'consular_template': (
            "The Argentine Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Argentina. "
            "Argentina is a Hague Apostille Convention member (joined 1988); "
            "apostille certificates from member states are accepted. The "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Argentine funeral director takes custody at Ministro Pistarini "
            "International Airport Buenos Aires (EZE) cargo terminal. The "
            "provincial Registro Civil registers the death. The Cuerpo Medico "
            "Forense and judicial authorities take jurisdiction for violent or "
            "unexplained deaths. Argentina joined the Hague Apostille Convention "
            "in 1988; apostille certificates from member states are accepted. "
            "All foreign documents require certified Spanish translation where "
            "applicable. A hermetically sealed coffin and embalming certificate "
            "are required."
        ),
        'emergency_line': 'contact the Argentine Embassy in the origin country',
        'hub_url': 'repatriation-from-argentina',
    },
    'poland': {
        'name': 'Poland',
        'slug': 'poland',
        'key': 'pl',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Polish funeral director takes custody at Warsaw Chopin Airport "
            "(WAW) or Krakow John Paul II International Airport (KRK) cargo "
            "terminal, depending on the family's destination. The Urzad Stanu "
            "Cywilnego (USC - Civil Registry Office) registers the death. The "
            "prokuratura (public prosecutor) takes jurisdiction for violent or "
            "unexplained deaths. Poland joined the Hague Apostille Convention "
            "in 2005; apostille certificates from member states are accepted. "
            "Poland is an EU member state; documents from EU member countries "
            "benefit from simplified procedures under EU regulations. A "
            "hermetically sealed coffin and embalming certificate are required "
            "for all air imports. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Polish Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Poland. Poland "
            "is a Hague Apostille Convention member (joined 2005); apostille "
            "certificates from member states are accepted. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Polish funeral director takes custody at Warsaw Chopin "
            "Airport (WAW) or Krakow International Airport (KRK) cargo "
            "terminal. The Urzad Stanu Cywilnego (USC - Civil Registry "
            "Office) registers the death. The prokuratura (public prosecutor) "
            "takes jurisdiction for violent or unexplained deaths. Poland "
            "joined the Hague Apostille Convention in 2005; apostille "
            "certificates from member states are accepted. A hermetically "
            "sealed coffin and embalming certificate are required."
        ),
        'emergency_line': 'contact the Polish Embassy in the origin country',
        'hub_url': 'repatriation-from-poland',
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
            "The Romanian funeral director takes custody at Henri Coanda "
            "International Airport Bucharest (OTP) or Cluj-Napoca International "
            "Airport (CLJ) cargo terminal, depending on the family's destination. "
            "The Starea Civila (Civil Status Department) registers the death. "
            "The parchet (public prosecutor) takes jurisdiction for violent or "
            "unexplained deaths. Romania joined the Hague Apostille Convention "
            "in 2001; apostille certificates from member states are accepted. "
            "Romania is an EU member state; documents from EU member countries "
            "benefit from simplified procedures under EU regulations. A "
            "hermetically sealed coffin and embalming certificate are required "
            "for all air imports. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Romanian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Romania. Romania "
            "is a Hague Apostille Convention member (joined 2001); apostille "
            "certificates from member states are accepted. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Romanian funeral director takes custody at Henri Coanda "
            "International Airport Bucharest (OTP) or Cluj-Napoca International "
            "Airport (CLJ) cargo terminal. The Starea Civila (Civil Status "
            "Department) registers the death. The parchet (public prosecutor) "
            "takes jurisdiction for violent or unexplained deaths. Romania "
            "joined the Hague Apostille Convention in 2001; apostille "
            "certificates from member states are accepted. A hermetically "
            "sealed coffin and embalming certificate are required."
        ),
        'emergency_line': 'contact the Romanian Embassy in the origin country',
        'hub_url': 'repatriation-from-romania',
    },
    'cuba': {
        'name': 'Cuba',
        'slug': 'cuba',
        'key': 'cu',
        'complexity_override': 'high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-4 weeks',
        'timeline_complex_override': '8-16 weeks',
        'reception': (
            "The Cuban funeral director takes custody at Jose Marti "
            "International Airport Havana (HAV) cargo terminal. The Registro "
            "del Estado Civil under the Ministerio de Justicia (MINJUS) "
            "registers the death. Cuban National Revolutionary Police (MININT) "
            "are involved in all deaths of foreign nationals. Cuba is not a "
            "member of the Hague Apostille Convention; full consular "
            "authentication is required for all foreign documents. The Ministry "
            "of Foreign Affairs (MINREX) must authorise all international "
            "repatriations; this authorisation step adds 1 to 3 weeks to the "
            "process. A hermetically sealed coffin and embalming certificate "
            "are required for all air imports. "
            "(Cuba Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "The Cuban Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Cuba. Cuba is not "
            "a Hague Apostille Convention member; all foreign documents require "
            "full consular authentication. All repatriations require "
            "authorisation from Cuba's Ministry of Foreign Affairs (MINREX). "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Cuban funeral director takes custody at Jose Marti "
            "International Airport Havana (HAV) cargo terminal. The Registro "
            "del Estado Civil under MINJUS registers the death. Cuban National "
            "Revolutionary Police (MININT) are involved in all deaths of foreign "
            "nationals. Cuba is not a Hague Apostille member; full consular "
            "authentication is required for all foreign documents. MINREX "
            "(Ministry of Foreign Affairs) must authorise all repatriations; "
            "this adds 1 to 3 weeks. A hermetically sealed coffin and embalming "
            "certificate are required."
        ),
        'emergency_line': 'contact the Cuban Embassy in the origin country',
        'hub_url': 'repatriation-from-cuba',
    },
}

ORIGIN_DATA = {
    'united-states': {
        'name': 'the United States',
        'emergency': '911',
        'registry': 'the state civil records office where the death occurred',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician "
            "or medical examiner. The death is registered with the state civil "
            "records office where the death occurred. Each US state operates its "
            "own civil records system. The coroner or medical examiner takes "
            "jurisdiction for violent, sudden, or unexplained deaths, with "
            "processes varying by state. The United States is a Hague Apostille "
            "Convention member. The relevant Embassy or Consulate of the "
            "destination country can assist with documentation requirements."
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
            "medical practitioner. The death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. The coroner "
            "takes jurisdiction for sudden, violent, or unexplained deaths. "
            "Australia is a Hague Apostille Convention member. The registration "
            "process is straightforward; the coroner's release is the main cause "
            "of delay in complex cases."
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
}

ROUTES = [
    # R85 -- Jordan x5
    {
        'origin': 'france', 'dest': 'jordan',
        'embassy_city': 'Paris',
        'intro': (
            "France has an established Jordanian community, with nationals "
            "working in Paris and Lyon in trade, commerce, and hospitality. "
            "Jordan and France maintain active bilateral ties through political "
            "dialogue and development cooperation. The Jordanian Embassy in "
            "Paris is fully operational. When a Jordanian national dies in "
            "France and their family wishes to repatriate remains to Jordan, "
            "the death is registered with the local mairie (town hall). The "
            "acte de deces requires certified Arabic translation for the Civil "
            "Status and Passports Department (CSPA) in Jordan. Jordan is not "
            "a Hague Apostille Convention member; French documents require full "
            "consular authentication through the Jordanian Embassy in Paris. "
            "For Muslim remains, Islamic burial traditions apply and prompt "
            "repatriation is expected. "
            "(Jordanian Ministry of Foreign Affairs, 2025; French Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'jordan',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a Jordanian community, with nationals working in Rome "
            "and Milan in hospitality, trade, and academic sectors. Jordan and "
            "Italy maintain bilateral ties including development cooperation and "
            "tourism links. The Jordanian Embassy in Rome is fully operational. "
            "When a Jordanian national dies in Italy and their family wishes to "
            "repatriate remains to Jordan, the death is registered with the "
            "local comune (civil registry). The atto di morte requires certified "
            "Arabic translation for the Civil Status and Passports Department "
            "(CSPA) in Jordan. Jordan is not a Hague Apostille Convention member; "
            "Italian documents require full consular authentication through the "
            "Jordanian Embassy in Rome. For Muslim remains, Islamic burial "
            "traditions apply and prompt repatriation is expected. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Italian Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'jordan',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Jordan maintain bilateral relations through "
            "trade and development cooperation, and a Jordanian community is "
            "established in the Netherlands. The Jordanian Embassy is located "
            "in The Hague. When a Jordanian national dies in the Netherlands "
            "and their family wishes to repatriate remains to Jordan, the death "
            "is registered with the local gemeente (municipal civil registry). "
            "The akte van overlijden requires certified Arabic translation for "
            "the Civil Status and Passports Department (CSPA) in Jordan. Jordan "
            "is not a Hague Apostille Convention member; Dutch documents require "
            "full consular authentication through the Jordanian Embassy in "
            "The Hague. For Muslim remains, Islamic burial traditions apply and "
            "prompt repatriation is expected. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'jordan',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Jordan maintain bilateral diplomatic relations, and a "
            "Jordanian community is established in Sweden. The Jordanian Embassy "
            "in Stockholm is fully operational. When a Jordanian national dies "
            "in Sweden and their family wishes to repatriate remains to Jordan, "
            "the death is registered with the Swedish Tax Agency (Skatteverket) "
            "Population Register. The dodsfallsintyg requires certified Arabic "
            "translation for the Civil Status and Passports Department (CSPA) "
            "in Jordan. Jordan is not a Hague Apostille Convention member; "
            "Swedish documents require full consular authentication through the "
            "Jordanian Embassy in Stockholm. For Muslim remains, Islamic burial "
            "traditions apply and prompt repatriation is expected. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'jordan',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Jordan maintain bilateral diplomatic relations, and a "
            "Jordanian community is established in Norway. The Jordanian Embassy "
            "in Oslo is fully operational. When a Jordanian national dies in "
            "Norway and their family wishes to repatriate remains to Jordan, "
            "the death is registered with Folkeregisteret (the civil registration "
            "system administered by Skatteetaten). The dodsattest requires "
            "certified Arabic translation for the Civil Status and Passports "
            "Department (CSPA) in Jordan. Jordan is not a Hague Apostille "
            "Convention member; Norwegian documents require full consular "
            "authentication through the Jordanian Embassy in Oslo. For Muslim "
            "remains, Islamic burial traditions apply and prompt repatriation "
            "is expected. "
            "(Jordanian Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    # R85 -- Sri Lanka x5
    {
        'origin': 'germany', 'dest': 'sri-lanka',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has an established Sri Lankan community, with nationals "
            "working in Berlin, Frankfurt, and Cologne in healthcare, engineering, "
            "and catering. Sri Lanka maintains an Embassy in Berlin. When a Sri "
            "Lankan national dies in Germany and their family wishes to repatriate "
            "remains to Sri Lanka, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde requires certified "
            "Sinhala, Tamil, or English translation for Sri Lankan authorities. "
            "Sri Lanka is not a Hague Apostille Convention member; German "
            "documents require full consular authentication through the Sri "
            "Lankan Embassy in Berlin. A hermetically sealed coffin and "
            "embalming certificate are required for all air imports. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; German Federal "
            "Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'sri-lanka',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a Sri Lankan community, with nationals working "
            "in The Hague, Amsterdam, and Rotterdam in hospitality and professional "
            "services. Sri Lanka maintains an Embassy in The Hague. When a Sri "
            "Lankan national dies in the Netherlands and their family wishes to "
            "repatriate remains to Sri Lanka, the death is registered with the "
            "local gemeente (municipal civil registry). The akte van overlijden "
            "requires certified Sinhala, Tamil, or English translation for Sri "
            "Lankan authorities. Sri Lanka is not a Hague Apostille Convention "
            "member; Dutch documents require full consular authentication through "
            "the Sri Lankan Embassy in The Hague. A hermetically sealed coffin "
            "and embalming certificate are required. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'sri-lanka',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a Sri Lankan community concentrated in Stockholm and "
            "Gothenburg, with many families who arrived during the civil conflict "
            "period now well established. Sri Lanka maintains an Embassy in "
            "Stockholm. When a Sri Lankan national dies in Sweden and their "
            "family wishes to repatriate remains to Sri Lanka, the death is "
            "registered with the Swedish Tax Agency (Skatteverket) Population "
            "Register. The dodsfallsintyg requires certified Sinhala, Tamil, or "
            "English translation for Sri Lankan authorities. Sri Lanka is not a "
            "Hague Apostille Convention member; Swedish documents require full "
            "consular authentication through the Sri Lankan Embassy in Stockholm. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'sri-lanka',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway has a Sri Lankan community established through refugee "
            "settlement during the civil conflict period and subsequent family "
            "reunification. Sri Lanka maintains an Embassy in Oslo. When a Sri "
            "Lankan national dies in Norway and their family wishes to repatriate "
            "remains to Sri Lanka, the death is registered with Folkeregisteret "
            "(the civil registration system administered by Skatteetaten). The "
            "dodsattest requires certified Sinhala, Tamil, or English translation "
            "for Sri Lankan authorities. Sri Lanka is not a Hague Apostille "
            "Convention member; Norwegian documents require full consular "
            "authentication through the Sri Lankan Embassy in Oslo. A "
            "hermetically sealed coffin and embalming certificate are required. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'sri-lanka',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain has a growing Sri Lankan community, with nationals working "
            "in Madrid and Barcelona in hospitality, retail, and domestic "
            "services. Sri Lanka maintains an Embassy in Madrid. When a Sri "
            "Lankan national dies in Spain and their family wishes to repatriate "
            "remains to Sri Lanka, the death is registered with the local "
            "Registro Civil (civil registry). The certificado de defuncion "
            "requires certified Sinhala, Tamil, or English translation for "
            "Sri Lankan authorities. Sri Lanka is not a Hague Apostille "
            "Convention member; Spanish documents require full consular "
            "authentication through the Sri Lankan Embassy in Madrid. A "
            "hermetically sealed coffin and embalming certificate are required "
            "for all air imports. "
            "(Sri Lanka Ministry of Foreign Affairs, 2025; Spanish Ministry "
            "of Justice, 2025.)"
        ),
    },
    # R85 -- Nepal x5
    {
        'origin': 'germany', 'dest': 'nepal',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Nepal maintain bilateral ties through development "
            "cooperation, and Nepalese nationals work in Germany in healthcare "
            "under bilateral recruitment agreements. Nepal maintains an Embassy "
            "in Berlin. When a Nepalese national dies in Germany and their "
            "family wishes to repatriate remains to Nepal, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde requires certified Nepali translation for the Ward "
            "Office civil registration in Nepal. Nepal is not a Hague Apostille "
            "Convention member; German documents require full consular "
            "authentication through the Nepalese Embassy in Berlin. Hindu "
            "funeral traditions are predominant; for Hindu remains, prompt "
            "repatriation is expected. "
            "(Nepal Ministry of Foreign Affairs, 2025; German Federal "
            "Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'nepal',
        'embassy_city': 'Rome',
        'intro': (
            "Italy has a Nepalese community, with nationals working in Rome "
            "and other Italian cities in hospitality, construction, and domestic "
            "services. Nepal maintains an Embassy in Rome. When a Nepalese "
            "national dies in Italy and their family wishes to repatriate remains "
            "to Nepal, the death is registered with the local comune (civil "
            "registry). The atto di morte requires certified Nepali translation "
            "for the Ward Office civil registration in Nepal. Nepal is not a "
            "Hague Apostille Convention member; Italian documents require full "
            "consular authentication through the Nepalese Embassy in Rome. "
            "Hindu funeral traditions are predominant; for Hindu remains, prompt "
            "repatriation is expected. "
            "(Nepal Ministry of Foreign Affairs, 2025; Italian Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'nepal',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Nepal maintain bilateral ties through "
            "development cooperation, and a Nepalese community is established "
            "in the Netherlands. Nepal maintains an Embassy in The Hague. When "
            "a Nepalese national dies in the Netherlands and their family wishes "
            "to repatriate remains to Nepal, the death is registered with the "
            "local gemeente (municipal civil registry). The akte van overlijden "
            "requires certified Nepali translation for the Ward Office civil "
            "registration in Nepal. Nepal is not a Hague Apostille Convention "
            "member; Dutch documents require full consular authentication through "
            "the Nepalese Embassy in The Hague. Hindu funeral traditions are "
            "predominant in Nepal. "
            "(Nepal Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'nepal',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Nepal maintain bilateral diplomatic relations, and a "
            "Nepalese community is established in Sweden. Nepal maintains an "
            "Embassy in Stockholm. When a Nepalese national dies in Sweden and "
            "their family wishes to repatriate remains to Nepal, the death is "
            "registered with the Swedish Tax Agency (Skatteverket) Population "
            "Register. The dodsfallsintyg requires certified Nepali translation "
            "for the Ward Office civil registration in Nepal. Nepal is not a "
            "Hague Apostille Convention member; Swedish documents require full "
            "consular authentication through the Nepalese Embassy in Stockholm. "
            "Hindu funeral traditions are predominant in Nepal; for Hindu "
            "remains, prompt repatriation is expected. "
            "(Nepal Ministry of Foreign Affairs, 2025; Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'nepal',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Nepal maintain bilateral diplomatic ties through "
            "development cooperation, and a Nepalese community is established "
            "in Norway. Nepal maintains an Embassy in Oslo. When a Nepalese "
            "national dies in Norway and their family wishes to repatriate "
            "remains to Nepal, the death is registered with Folkeregisteret "
            "(the civil registration system administered by Skatteetaten). The "
            "dodsattest requires certified Nepali translation for the Ward "
            "Office civil registration in Nepal. Nepal is not a Hague Apostille "
            "Convention member; Norwegian documents require full consular "
            "authentication through the Nepalese Embassy in Oslo. Hindu funeral "
            "traditions are predominant. "
            "(Nepal Ministry of Foreign Affairs, 2025; Skatteetaten, Norway, 2025.)"
        ),
    },
    # R85 -- Mexico x5
    {
        'origin': 'australia', 'dest': 'mexico',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Mexico maintain bilateral diplomatic relations, and "
            "Australian nationals travel to Mexico for tourism, academic "
            "exchanges, and business. Mexico maintains an Embassy in Canberra. "
            "When an Australian national dies in Mexico and their family wishes "
            "to repatriate remains to Australia, the death is registered with "
            "the local Registro Civil. SEMEFO (Servicio Medico Forense) takes "
            "jurisdiction for violent or unexplained deaths. Mexico is a Hague "
            "Apostille Convention member (joined 1995); Australia is also a "
            "Hague member, which simplifies document authentication for this "
            "corridor. A hermetically sealed coffin and embalming certificate "
            "are required for all air cargo. "
            "(Mexico Secretaria de Relaciones Exteriores, 2025; DFAT Travel "
            "Advice: Mexico, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'mexico',
        'embassy_city': 'Paris',
        'intro': (
            "France and Mexico maintain active bilateral ties through trade, "
            "culture, and diplomatic engagement, and French nationals travel to "
            "Mexico for tourism, academic research, and business. The Mexican "
            "Embassy in Paris is fully operational. When a French national dies "
            "in Mexico and their family wishes to repatriate remains to France, "
            "the death is registered with the local Registro Civil. SEMEFO "
            "(Servicio Medico Forense) takes jurisdiction for violent or "
            "unexplained deaths. Mexico joined the Hague Apostille Convention "
            "in 1995; France is a Hague member. Both countries are Hague members, "
            "which simplifies document authentication for this corridor. A "
            "hermetically sealed coffin and embalming certificate are required "
            "for air cargo. "
            "(Mexico Secretaria de Relaciones Exteriores, 2025; French Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'mexico',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Mexico maintain strong bilateral ties through trade, "
            "automotive and manufacturing investment, and cultural exchanges. "
            "German nationals travel to Mexico for business and tourism. The "
            "Mexican Embassy in Berlin is fully operational. When a German "
            "national dies in Mexico and their family wishes to repatriate "
            "remains to Germany, the death is registered with the local "
            "Registro Civil. SEMEFO (Servicio Medico Forense) takes jurisdiction "
            "for violent or unexplained deaths. Mexico joined the Hague Apostille "
            "Convention in 1995; Germany is a Hague member. Both countries are "
            "Hague members, which simplifies document authentication. A "
            "hermetically sealed coffin and embalming certificate are required. "
            "(Mexico Secretaria de Relaciones Exteriores, 2025; German Federal "
            "Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'mexico',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain and Mexico share deep cultural, linguistic, and historical "
            "ties, and significant bilateral community flows exist in both "
            "directions. Spanish nationals travel to Mexico for business, "
            "tourism, and family visits. The Mexican Embassy in Madrid is fully "
            "operational. When a Spanish national dies in Mexico and their "
            "family wishes to repatriate remains to Spain, the death is "
            "registered with the local Registro Civil. SEMEFO (Servicio Medico "
            "Forense) takes jurisdiction for violent or unexplained deaths. "
            "Mexico joined the Hague Apostille Convention in 1995; Spain "
            "joined in 1978. Both countries are Hague members. "
            "(Mexico Secretaria de Relaciones Exteriores, 2025; Spanish "
            "Ministry of Justice, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'mexico',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Mexico maintain bilateral ties through trade, cultural "
            "links, and a significant Italian-Mexican community. Italian "
            "nationals travel to Mexico for tourism and business. The Mexican "
            "Embassy in Rome is fully operational. When an Italian national "
            "dies in Mexico and their family wishes to repatriate remains to "
            "Italy, the death is registered with the local Registro Civil. "
            "SEMEFO (Servicio Medico Forense) takes jurisdiction for violent "
            "or unexplained deaths. Mexico joined the Hague Apostille Convention "
            "in 1995; Italy joined in 1978. Both countries are Hague members, "
            "which simplifies document authentication. A hermetically sealed "
            "coffin and embalming certificate are required for air cargo. "
            "(Mexico Secretaria de Relaciones Exteriores, 2025; Italian "
            "Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R85 -- Brazil x5
    {
        'origin': 'australia', 'dest': 'brazil',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Brazil maintain bilateral diplomatic relations, and "
            "Australian nationals travel to Brazil for tourism and business in "
            "mining and agriculture sectors. Brazil maintains an Embassy in "
            "Canberra. When an Australian national dies in Brazil and their "
            "family wishes to repatriate remains to Australia, the death is "
            "registered with the local Cartorio de Registro Civil. The Instituto "
            "Medico Legal (IML) takes jurisdiction for violent or unexplained "
            "deaths. ANVISA (Agencia Nacional de Vigilancia Sanitaria) clearance "
            "is required before remains can be released for international "
            "transport. Brazil joined the Hague Apostille Convention in 2016; "
            "Australia is a Hague member, which simplifies document "
            "authentication. "
            "(Brazil Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice: Brazil, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'brazil',
        'embassy_city': 'Paris',
        'intro': (
            "France and Brazil maintain one of the most active bilateral "
            "relationships in Europe-Latin America, with strong trade, "
            "investment, and cultural ties. French nationals travel extensively "
            "to Brazil for business and tourism. The Brazilian Embassy in Paris "
            "is fully operational. When a French national dies in Brazil and "
            "their family wishes to repatriate remains to France, the death is "
            "registered with the local Cartorio de Registro Civil. The Instituto "
            "Medico Legal (IML) takes jurisdiction for violent or unexplained "
            "deaths. ANVISA clearance is required before remains can be released "
            "for international transport. Brazil joined the Hague Apostille "
            "Convention in 2016; France is a Hague member. "
            "(Brazil Ministry of Foreign Affairs, 2025; French Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'brazil',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Brazil maintain bilateral ties through trade "
            "and investment, with Dutch agricultural and energy interests "
            "present in Brazil. The Netherlands maintains an Embassy in "
            "Brasilia and Consulates in Sao Paulo and Rio de Janeiro. When a "
            "Dutch national dies in Brazil and their family wishes to repatriate "
            "remains to the Netherlands, the death is registered with the local "
            "Cartorio de Registro Civil. The Instituto Medico Legal (IML) takes "
            "jurisdiction for violent or unexplained deaths. ANVISA clearance "
            "is required before remains can be released. Brazil joined the "
            "Hague Apostille Convention in 2016; the Netherlands joined in 1960. "
            "Both are Hague members. "
            "(Brazil Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'brazil',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Brazil maintain bilateral ties through trade, investment, "
            "and development cooperation, with Swedish companies active in the "
            "Brazilian market. Swedish nationals travel to Brazil for business "
            "and tourism. The Brazilian Embassy in Stockholm is fully operational. "
            "When a Swedish national dies in Brazil and their family wishes to "
            "repatriate remains to Sweden, the death is registered with the "
            "local Cartorio de Registro Civil. The Instituto Medico Legal (IML) "
            "takes jurisdiction for violent or unexplained deaths. ANVISA "
            "clearance is required before remains can be released. Brazil joined "
            "the Hague Apostille Convention in 2016; Sweden joined in 1999. "
            "Both are Hague members. "
            "(Brazil Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'brazil',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Brazil maintain bilateral diplomatic relations through "
            "trade and energy sector cooperation, with Norwegian shipping and "
            "energy interests active in Brazil. Norwegian nationals travel to "
            "Brazil for business and tourism. The Brazilian Embassy in Oslo is "
            "fully operational. When a Norwegian national dies in Brazil and "
            "their family wishes to repatriate remains to Norway, the death is "
            "registered with the local Cartorio de Registro Civil. The Instituto "
            "Medico Legal (IML) takes jurisdiction for violent or unexplained "
            "deaths. ANVISA clearance is required before remains can be released "
            "for international transport. Brazil joined the Hague Apostille "
            "Convention in 2016; Norway is a Hague member. "
            "(Brazil Ministry of Foreign Affairs, 2025; Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    # R86 -- Colombia x5
    {
        'origin': 'australia', 'dest': 'colombia',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Colombia maintain bilateral diplomatic relations, "
            "and Australian nationals travel to Colombia for tourism and "
            "business. Colombia maintains an Embassy in Canberra. When an "
            "Australian national dies in Colombia and their family wishes to "
            "repatriate remains to Australia, the death is registered with "
            "the local Registraduria Nacional del Estado Civil. The Instituto "
            "Nacional de Medicina Legal y Ciencias Forenses (Medicina Legal) "
            "takes jurisdiction for violent or unexplained deaths. Colombia "
            "joined the Hague Apostille Convention in 1991; Australia is a "
            "Hague member, which simplifies document authentication. A "
            "hermetically sealed coffin and embalming certificate are required "
            "for all air cargo. "
            "(Colombia Cancilleria, 2025; DFAT Travel Advice: Colombia, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'colombia',
        'embassy_city': 'Paris',
        'intro': (
            "France and Colombia maintain active bilateral ties through trade, "
            "cultural exchanges, and diplomatic engagement. French nationals "
            "travel to Colombia for tourism and business, particularly in "
            "Cartagena and Bogota. The Colombian Embassy in Paris is fully "
            "operational. When a French national dies in Colombia and their "
            "family wishes to repatriate remains to France, the death is "
            "registered with the local Registraduria Nacional del Estado Civil. "
            "The Instituto Nacional de Medicina Legal y Ciencias Forenses "
            "(Medicina Legal) takes jurisdiction for violent or unexplained "
            "deaths. Colombia joined the Hague Apostille Convention in 1991; "
            "France is a Hague member. Both countries are Hague members, which "
            "simplifies document authentication. "
            "(Colombia Cancilleria, 2025; French Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'colombia',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Colombia maintain bilateral diplomatic relations, with "
            "Swedish development cooperation active in Colombia. Swedish "
            "nationals travel to Colombia for tourism and voluntary work. The "
            "Colombian Embassy in Stockholm is fully operational. When a Swedish "
            "national dies in Colombia and their family wishes to repatriate "
            "remains to Sweden, the death is registered with the local "
            "Registraduria Nacional del Estado Civil. Medicina Legal takes "
            "jurisdiction for violent or unexplained deaths. Colombia joined "
            "the Hague Apostille Convention in 1991; Sweden joined in 1999. "
            "Both are Hague members, which simplifies document authentication. "
            "(Colombia Cancilleria, 2025; Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'colombia',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and Colombia maintain bilateral diplomatic relations through "
            "development cooperation and peace process support, with Norway "
            "playing a role in Colombian peace negotiations. Norwegian nationals "
            "travel to Colombia for diplomatic and voluntary work. The Colombian "
            "Embassy in Oslo is fully operational. When a Norwegian national "
            "dies in Colombia and their family wishes to repatriate remains to "
            "Norway, the death is registered with the local Registraduria "
            "Nacional del Estado Civil. Medicina Legal takes jurisdiction for "
            "violent or unexplained deaths. Colombia joined the Hague Apostille "
            "Convention in 1991; Norway is a Hague member. Both are Hague "
            "members. "
            "(Colombia Cancilleria, 2025; Skatteetaten, Norway, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'colombia',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Colombia maintain bilateral ties through shared "
            "Iberian linguistic heritage, trade partnerships, and cultural "
            "exchanges. The Colombian Embassy in Lisbon is fully operational. "
            "When a Portuguese national dies in Colombia and their family wishes "
            "to repatriate remains to Portugal, the death is registered with "
            "the local Registraduria Nacional del Estado Civil. The Instituto "
            "Nacional de Medicina Legal y Ciencias Forenses (Medicina Legal) "
            "takes jurisdiction for violent or unexplained deaths. Colombia "
            "joined the Hague Apostille Convention in 1991; Portugal joined "
            "in 1970. Both countries are Hague members, which simplifies "
            "document authentication. "
            "(Colombia Cancilleria, 2025; Portuguese Ministry of Justice, 2025.)"
        ),
    },
    # R86 -- Argentina x5
    {
        'origin': 'australia', 'dest': 'argentina',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Argentina maintain bilateral diplomatic relations, "
            "and Australian nationals travel to Argentina for tourism, "
            "particularly to Buenos Aires and Patagonia. Argentina maintains "
            "an Embassy in Canberra. When an Australian national dies in "
            "Argentina and their family wishes to repatriate remains to "
            "Australia, the death is registered with the provincial Registro "
            "Civil. The Cuerpo Medico Forense and judicial authorities take "
            "jurisdiction for violent or unexplained deaths. Argentina joined "
            "the Hague Apostille Convention in 1988; Australia is a Hague "
            "member, which simplifies document authentication for this "
            "corridor. A hermetically sealed coffin and embalming certificate "
            "are required for all air imports. "
            "(Argentina Cancilleria, 2025; DFAT Travel Advice: Argentina, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'argentina',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada and Argentina maintain bilateral diplomatic relations, "
            "with a significant Argentine-Canadian community established in "
            "Toronto and other cities. Argentine nationals travel to Canada "
            "for study and work, and bilateral cultural ties are active. The "
            "Argentine Embassy in Ottawa is fully operational. When an "
            "Argentine national dies in Canada and their family wishes to "
            "repatriate remains to Argentina, the death is registered with "
            "the provincial civil registration authority. Argentina joined the "
            "Hague Apostille Convention in 1988; Canada joined in November "
            "2024. Both countries are now Hague members, which simplifies "
            "document authentication. "
            "(Argentina Cancilleria, 2025; Global Affairs Canada, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'argentina',
        'embassy_city': 'Paris',
        'intro': (
            "France and Argentina share deep historical and cultural ties, "
            "including a significant French-Argentine heritage community. "
            "Argentine nationals travel to France for academic study, culture, "
            "and family visits, and there is a substantial Argentine community "
            "in Paris. The Argentine Embassy in Paris is fully operational. "
            "When an Argentine national dies in France and their family wishes "
            "to repatriate remains to Argentina, the death is registered with "
            "the local mairie (town hall). The acte de deces requires certified "
            "Spanish translation for the provincial Registro Civil in Argentina. "
            "Argentina joined the Hague Apostille Convention in 1988; France "
            "is a Hague member. Both countries are Hague members. "
            "(Argentina Cancilleria, 2025; French Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'argentina',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Argentina share significant bilateral ties, including "
            "a large German-Argentine heritage community, trade and investment "
            "links, and active diplomatic engagement. Argentine nationals travel "
            "to Germany for academic study, business, and tourism. The Argentine "
            "Embassy in Berlin is fully operational. When an Argentine national "
            "dies in Germany and their family wishes to repatriate remains to "
            "Argentina, the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde requires certified Spanish translation "
            "for the provincial Registro Civil in Argentina. Argentina joined "
            "the Hague Apostille Convention in 1988; Germany is a Hague member. "
            "Both countries are Hague members, which simplifies document "
            "authentication. "
            "(Argentina Cancilleria, 2025; German Federal Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'argentina',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Argentina maintain bilateral ties through "
            "trade and investment, with Dutch agricultural and food technology "
            "interests active in Argentina. Argentine nationals travel to the "
            "Netherlands for academic study and business. The Argentine Embassy "
            "is in The Hague. When an Argentine national dies in the Netherlands "
            "and their family wishes to repatriate remains to Argentina, the "
            "death is registered with the local gemeente (municipal civil "
            "registry). The akte van overlijden requires certified Spanish "
            "translation for the provincial Registro Civil in Argentina. "
            "Argentina joined the Hague Apostille Convention in 1988; the "
            "Netherlands joined in 1960. Both are Hague members. "
            "(Argentina Cancilleria, 2025; Netherlands Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    # R86 -- Poland x5
    {
        'origin': 'australia', 'dest': 'poland',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a significant Polish-Australian community, with "
            "families established across Sydney, Melbourne, and other major "
            "cities, many arriving during and after the Second World War and "
            "through the Solidarity period. Poland maintains an Embassy in "
            "Canberra. When a Polish national dies in Australia and their "
            "family wishes to repatriate remains to Poland, the death is "
            "registered with the state or territory Births, Deaths and "
            "Marriages (BDM) registry. Poland joined the Hague Apostille "
            "Convention in 2005; Australia is a Hague member. Both countries "
            "are Hague members, which simplifies document authentication. A "
            "hermetically sealed coffin and embalming certificate are required "
            "for all repatriations. "
            "(Polish Ministry of Foreign Affairs, 2025; DFAT Travel Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'poland',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has one of the world's largest Polish diaspora communities, "
            "concentrated in Toronto, Montreal, and Edmonton. Polish-Canadians "
            "maintain strong cultural and family connections to Poland, and "
            "bilateral travel is regular. The Polish Embassy in Ottawa is fully "
            "operational. When a Polish national dies in Canada and their family "
            "wishes to repatriate remains to Poland, the death is registered "
            "with the provincial civil registration authority. Poland joined "
            "the Hague Apostille Convention in 2005; Canada joined in November "
            "2024. Both countries are now Hague members, which simplifies "
            "document authentication. "
            "(Polish Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'poland',
        'embassy_city': 'Rome',
        'intro': (
            "Italy is a significant destination for Polish workers, with a "
            "large Polish community concentrated in Rome, Milan, and Florence "
            "working in domestic services, construction, and hospitality. "
            "Poland maintains an Embassy in Rome. When a Polish national dies "
            "in Italy and their family wishes to repatriate remains to Poland, "
            "the death is registered with the local comune (civil registry). "
            "The atto di morte requires certified Polish translation for the "
            "Urzad Stanu Cywilnego (USC) in Poland. Poland joined the Hague "
            "Apostille Convention in 2005; Italy joined in 1978. Both countries "
            "are EU members and Hague members, which simplifies document "
            "authentication. "
            "(Polish Ministry of Foreign Affairs, 2025; Italian Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'poland',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain is a significant European destination for Polish workers "
            "and tourists, with a Polish community established in Madrid and "
            "Barcelona. Poland maintains an Embassy in Madrid. When a Polish "
            "national dies in Spain and their family wishes to repatriate "
            "remains to Poland, the death is registered with the local Registro "
            "Civil (civil registry). The certificado de defuncion requires "
            "certified Polish translation for the Urzad Stanu Cywilnego (USC) "
            "in Poland. Poland joined the Hague Apostille Convention in 2005; "
            "Spain joined in 1978. Both are EU members and Hague members. "
            "(Polish Ministry of Foreign Affairs, 2025; Spanish Ministry of "
            "Justice, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'poland',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Poland maintain active bilateral relations as EU member "
            "states, with a Polish community established in Stockholm and other "
            "Swedish cities working in construction, healthcare, and services. "
            "Poland maintains an Embassy in Stockholm. When a Polish national "
            "dies in Sweden and their family wishes to repatriate remains to "
            "Poland, the death is registered with the Swedish Tax Agency "
            "(Skatteverket) Population Register. The dodsfallsintyg requires "
            "certified Polish translation for the Urzad Stanu Cywilnego (USC) "
            "in Poland. Poland joined the Hague Apostille Convention in 2005; "
            "Sweden joined in 1999. Both are EU members and Hague members. "
            "(Polish Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    # R86 -- Romania x5
    {
        'origin': 'united-states', 'dest': 'romania',
        'embassy_city': 'Washington DC',
        'intro': (
            "Romania and the United States maintain close bilateral ties as "
            "NATO allies, with a significant Romanian-American community "
            "established in cities including Chicago, Detroit, New York, and "
            "Los Angeles. The Romanian Embassy in Washington DC is fully "
            "operational. When a Romanian national dies in the United States "
            "and their family wishes to repatriate remains to Romania, the "
            "death is registered with the state civil records office. Romania "
            "joined the Hague Apostille Convention in 2001; the United States "
            "joined in 1981. Both countries are Hague members, which simplifies "
            "document authentication. "
            "(Romania Ministry of Foreign Affairs, 2025; US Department of "
            "State, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'romania',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has an established Romanian-Australian community, with "
            "nationals who settled in the post-communist period and through "
            "subsequent migration working in Melbourne, Sydney, and other "
            "cities. Romania maintains an Embassy in Canberra. When a Romanian "
            "national dies in Australia and their family wishes to repatriate "
            "remains to Romania, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. Romania "
            "joined the Hague Apostille Convention in 2001; Australia is a "
            "Hague member. Both countries are Hague members, which simplifies "
            "document authentication. "
            "(Romania Ministry of Foreign Affairs, 2025; DFAT Travel "
            "Advice, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'romania',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a Romanian-Canadian community concentrated in Toronto "
            "and Montreal, with families who settled during the communist and "
            "post-communist periods. The Romanian Embassy in Ottawa is fully "
            "operational. When a Romanian national dies in Canada and their "
            "family wishes to repatriate remains to Romania, the death is "
            "registered with the provincial civil registration authority. "
            "Romania joined the Hague Apostille Convention in 2001; Canada "
            "joined in November 2024. Both countries are now Hague members, "
            "which simplifies document authentication. "
            "(Romania Ministry of Foreign Affairs, 2025; Global Affairs "
            "Canada, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'romania',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands is a major destination for Romanian workers, with "
            "a large Romanian community established in The Hague, Amsterdam, "
            "Rotterdam, and other Dutch cities working across agriculture, "
            "logistics, and construction. Romania maintains an Embassy in "
            "The Hague. When a Romanian national dies in the Netherlands and "
            "their family wishes to repatriate remains to Romania, the death "
            "is registered with the local gemeente (municipal civil registry). "
            "Romania joined the Hague Apostille Convention in 2001; the "
            "Netherlands joined in 1960. Both are EU members and Hague members. "
            "(Romania Ministry of Foreign Affairs, 2025; Netherlands Ministry "
            "of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'romania',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden has a Romanian community established through the EU freedom "
            "of movement framework, with nationals working in Stockholm and "
            "other Swedish cities in construction, healthcare, and services. "
            "Romania maintains an Embassy in Stockholm. When a Romanian national "
            "dies in Sweden and their family wishes to repatriate remains to "
            "Romania, the death is registered with the Swedish Tax Agency "
            "(Skatteverket) Population Register. The dodsfallsintyg requires "
            "certified Romanian translation for the Starea Civila (Civil Status "
            "Department) in Romania. Romania joined the Hague Apostille "
            "Convention in 2001; Sweden joined in 1999. Both are EU members "
            "and Hague members. "
            "(Romania Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
        ),
    },
    # R86 -- Cuba x5
    {
        'origin': 'australia', 'dest': 'cuba',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Cuba maintain bilateral diplomatic relations, and "
            "Australian nationals travel to Cuba for tourism and educational "
            "visits. Cuba maintains an Embassy in Canberra. When an Australian "
            "national dies in Cuba and their family wishes to repatriate remains "
            "to Australia, the death is registered with the local Registro del "
            "Estado Civil. Cuban National Revolutionary Police (MININT) are "
            "involved in all deaths of foreign nationals. Cuba is not a Hague "
            "Apostille Convention member; all foreign documents require consular "
            "authentication. The Cuban Ministry of Foreign Affairs (MINREX) "
            "must authorise all repatriations, adding 1 to 3 weeks to the "
            "process. A hermetically sealed coffin and embalming certificate "
            "are required for all air imports. "
            "(DFAT Travel Advice: Cuba, 2025; Cuba Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'cuba',
        'embassy_city': 'Paris',
        'intro': (
            "France and Cuba maintain bilateral diplomatic relations, with "
            "France among the European countries with active trade and cultural "
            "ties to Cuba. French nationals travel to Cuba for tourism and "
            "cultural visits. The Cuban Embassy in Paris is fully operational. "
            "When a French national dies in Cuba and their family wishes to "
            "repatriate remains to France, the death is registered with the "
            "local Registro del Estado Civil. Cuban authorities are involved "
            "in all deaths of foreign nationals. Cuba is not a Hague Apostille "
            "Convention member; French documents require consular authentication. "
            "The Cuban Ministry of Foreign Affairs (MINREX) must authorise all "
            "repatriations. A hermetically sealed coffin and embalming "
            "certificate are required. "
            "(Cuba Ministry of Foreign Affairs, 2025; French Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'cuba',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Cuba maintain bilateral diplomatic relations, with Italian "
            "nationals travelling to Cuba for tourism and cultural visits. The "
            "Cuban Embassy in Rome is fully operational. When an Italian national "
            "dies in Cuba and their family wishes to repatriate remains to Italy, "
            "the death is registered with the local Registro del Estado Civil. "
            "Cuban authorities are involved in all deaths of foreign nationals. "
            "Cuba is not a Hague Apostille Convention member; Italian documents "
            "require consular authentication. The Cuban Ministry of Foreign "
            "Affairs (MINREX) must authorise all repatriations; this adds 1 to "
            "3 weeks compared with other Caribbean routes. A hermetically sealed "
            "coffin and embalming certificate are required. "
            "(Cuba Ministry of Foreign Affairs, 2025; Italian Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'cuba',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands and Cuba maintain bilateral diplomatic relations, "
            "and Dutch nationals travel to Cuba for tourism. The Cuban Embassy "
            "is located in The Hague. When a Dutch national dies in Cuba and "
            "their family wishes to repatriate remains to the Netherlands, the "
            "death is registered with the local Registro del Estado Civil. "
            "Cuban authorities are involved in all deaths of foreign nationals. "
            "Cuba is not a Hague Apostille Convention member; Dutch documents "
            "require consular authentication. The MINREX authorisation step "
            "adds time to this process compared with other Caribbean routes. "
            "A hermetically sealed coffin and embalming certificate are "
            "required. "
            "(Cuba Ministry of Foreign Affairs, 2025; Netherlands Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'sweden', 'dest': 'cuba',
        'embassy_city': 'Stockholm',
        'intro': (
            "Sweden and Cuba maintain bilateral diplomatic relations, and "
            "Swedish nationals travel to Cuba for tourism. The Cuban Embassy "
            "in Stockholm is fully operational. When a Swedish national dies "
            "in Cuba and their family wishes to repatriate remains to Sweden, "
            "the death is registered with the local Registro del Estado Civil. "
            "Cuban authorities are involved in all deaths of foreign nationals. "
            "Cuba is not a Hague Apostille Convention member; Swedish documents "
            "require consular authentication. The Cuban Ministry of Foreign "
            "Affairs (MINREX) must authorise all repatriations; allow extra "
            "time for this step. A hermetically sealed coffin and embalming "
            "certificate are required. "
            "(Cuba Ministry of Foreign Affairs, 2025; Skatteverket, "
            "Sweden, 2025.)"
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
