#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R63-R64.

   R63 (25 routes, variants B,C,D,E,A x5):
     Turkey x5: united-kingdom, united-states, australia, canada, japan
     Poland x5: united-kingdom, germany, united-states, france, netherlands
     Romania x5: united-kingdom, italy, spain, germany, france
     Iraq x5: united-kingdom, united-states, germany, australia, france
     Lebanon x5: united-kingdom, united-states, france, germany, australia

   R64 (25 routes, variants B,C,D,E,A x5):
     Peru x5: united-kingdom, united-states, spain, germany, italy
     Ecuador x5: united-kingdom, united-states, spain, germany, italy
     Tanzania x5: united-kingdom, united-states, germany, australia, france
     Senegal x5: france, united-kingdom, united-states, germany, spain
     Cameroon x5: france, united-kingdom, united-states, germany, belgium

   Template rotation: R62 ended A (index 0). R63 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R64 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'turkey': {
        'name': 'Turkey',
        'slug': 'turkey',
        'key': 'tr',
        'reception': (
            "The Turkish funeral director takes custody at Istanbul Airport (IST) "
            "or Istanbul Sabiha Gokcen Airport (SAW) cargo terminal, or the "
            "relevant regional airport serving the destination city. Civil "
            "registration of deaths in Turkey is handled by the local Nufus "
            "Mudurlugu (Directorate of Civil Registration) under the Directorate "
            "General of Civil Registration and Nationality (NUFUS). An olum "
            "belgesi (death certificate) is issued in Turkish. For Muslim remains, "
            "which account for the large majority of the Turkish population, "
            "Islamic law procedures apply and families expect prompt burial. "
            "Turkey is a member of the Hague Apostille Convention; apostille "
            "certificates are accepted for documents from member states. All "
            "other foreign documents require certified Turkish translation. An "
            "embalming certificate and hermetically sealed coffin are required "
            "for all air imports. "
            "(Turkish Ministry of Interior, Directorate General of Civil "
            "Registration and Nationality, 2025; FCDO Travel Advice: Turkey, 2025.)"
        ),
        'consular_template': (
            "Turkish Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Turkey. Turkey is a Hague Apostille "
            "Convention member. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Turkish funeral director takes custody at Istanbul Airport (IST) "
            "or Istanbul Sabiha Gokcen Airport (SAW) cargo terminal. The local "
            "Nufus Mudurlugu registers the death; an olum belgesi is issued in "
            "Turkish. For Muslim remains, Islamic law procedures apply and "
            "families expect prompt burial. Turkey is a Hague Apostille Convention "
            "member; apostille certificates from member states are accepted. All "
            "other documents require certified Turkish translation. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Turkish Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-turkey',
    },
    'poland': {
        'name': 'Poland',
        'slug': 'poland',
        'key': 'pl',
        'reception': (
            "The Polish funeral director takes custody at Warsaw Chopin Airport "
            "(WAW) or Krakow John Paul II International Airport (KRK) cargo "
            "terminal, or the relevant regional airport. Death registration is "
            "handled by the local Urzad Stanu Cywilnego (USC, Civil Status "
            "Office), which issues an akt zgonu (death certificate) in Polish. "
            "Poland is an EU member state and a member of the Hague Apostille "
            "Convention; apostille certificates are accepted for documents from "
            "member states. All foreign documents in languages other than Polish "
            "require a certified sworn translation by a sworn translator registered "
            "in Poland. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Polish Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Poland. Poland is an EU member and "
            "Hague Apostille Convention member. The Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Polish funeral director takes custody at Warsaw Chopin Airport "
            "(WAW) or Krakow John Paul II International Airport (KRK) cargo "
            "terminal. The local Urzad Stanu Cywilnego (USC) registers the death "
            "and issues an akt zgonu in Polish. Poland is an EU member and Hague "
            "Apostille Convention member; apostille certificates from member "
            "states are accepted. Foreign documents in other languages require a "
            "certified sworn translation. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Polish Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-poland',
    },
    'romania': {
        'name': 'Romania',
        'slug': 'romania',
        'key': 'ro',
        'reception': (
            "The Romanian funeral director takes custody at Bucharest Henri "
            "Coanda International Airport (OTP) cargo terminal or the relevant "
            "regional airport. Death registration is handled by the local Starea "
            "Civila (civil status office) under the local council, which issues "
            "a certificat de deces (death certificate) in Romanian. Romania is "
            "an EU member state and a member of the Hague Apostille Convention; "
            "apostille certificates are accepted for documents from member states. "
            "All foreign documents in languages other than Romanian require "
            "certified Romanian translation authorised by a Romanian court or "
            "notary. An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Romanian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Romania. Romania is an EU member "
            "and Hague Apostille Convention member. The Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Romanian funeral director takes custody at Bucharest Henri "
            "Coanda International Airport (OTP) cargo terminal. The local Starea "
            "Civila registers the death and issues a certificat de deces in "
            "Romanian. Romania is an EU member and Hague Apostille Convention "
            "member; apostille certificates from member states are accepted. "
            "Foreign documents in other languages require certified Romanian "
            "translation. An embalming certificate and hermetically sealed coffin "
            "are required."
        ),
        'emergency_line': 'contact the Romanian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-romania',
    },
    'iraq': {
        'name': 'Iraq',
        'slug': 'iraq',
        'key': 'iq',
        'reception': (
            "The Iraqi funeral director takes custody at Baghdad International "
            "Airport (BGW) cargo terminal. For destinations in the Kurdistan "
            "Region of Iraq, Erbil International Airport (EBL) is the relevant "
            "gateway. Death registration is handled by the Civil Status "
            "Directorate under the Iraqi Ministry of Interior; all certificates "
            "are issued in Arabic. The FCDO advises against all travel to Iraq "
            "except the Kurdistan Region of Iraq, where it advises against all "
            "but essential travel. Families repatriating remains to Iraq should "
            "work with a specialist who maintains current contacts on the ground. "
            "Iraq is not a member of the Hague Apostille Convention; full "
            "consular authentication through the Iraqi Embassy or Consulate in "
            "the country of origin is required. All foreign documents require "
            "certified Arabic translation. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(FCDO Travel Advice: Iraq, 2025; Iraqi Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Iraqi Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Iraq. Iraq is not a Hague Apostille "
            "Convention member; full consular authentication is required. The "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Iraqi funeral director takes custody at Baghdad International "
            "Airport (BGW) cargo terminal. For the Kurdistan Region, Erbil "
            "International Airport (EBL) is the main gateway. The Civil Status "
            "Directorate registers the death; all certificates are in Arabic. "
            "Iraq is not a Hague Apostille member; full consular authentication "
            "through the Iraqi Embassy or Consulate in the origin country is "
            "required. All foreign documents require certified Arabic translation. "
            "An embalming certificate and hermetically sealed coffin are required. "
            "Families should work with a specialist given current conditions."
        ),
        'emergency_line': 'contact the Iraqi Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-iraq',
    },
    'lebanon': {
        'name': 'Lebanon',
        'slug': 'lebanon',
        'key': 'lb',
        'reception': (
            "The Lebanese funeral director takes custody at Beirut Rafic Hariri "
            "International Airport (BEY) cargo terminal. Death registration is "
            "handled by the Civil Registry Directorate (Sijill Madani) under the "
            "Lebanese Ministry of Interior; certificates are issued in Arabic, "
            "with French widely used in Lebanese administrative practice. The "
            "FCDO advises against travel to Lebanon; families should verify "
            "current airline operations and consular access before arranging "
            "repatriation. Lebanon is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Lebanese Embassy "
            "or Consulate in the country of origin is required. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(FCDO Travel Advice: Lebanon, 2025; Lebanese Ministry of Foreign "
            "Affairs and Emigrants, 2025.)"
        ),
        'consular_template': (
            "Lebanese Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Lebanon. Lebanon is not a Hague "
            "Apostille Convention member; full consular authentication is required. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Lebanese funeral director takes custody at Beirut Rafic Hariri "
            "International Airport (BEY) cargo terminal. The Civil Registry "
            "Directorate (Sijill Madani) registers the death; certificates are "
            "in Arabic, with French widely accepted. Lebanon is not a Hague "
            "Apostille member; full consular authentication through the Lebanese "
            "Embassy or Consulate in the origin country is required. Families "
            "should verify current airline operations and consular access. An "
            "embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Lebanese Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-lebanon',
    },
    'peru': {
        'name': 'Peru',
        'slug': 'peru',
        'key': 'pe',
        'reception': (
            "The Peruvian funeral director takes custody at Jorge Chavez "
            "International Airport Lima (LIM) cargo terminal or the relevant "
            "regional airport. Death registration is handled by RENIEC (Registro "
            "Nacional de Identificacion y Estado Civil), Peru's national civil "
            "registry. Peru is a member of the Hague Apostille Convention; "
            "apostille certificates are accepted for documents from member states. "
            "All other foreign documents require certified Spanish translation and "
            "full consular authentication through the Peruvian Embassy or "
            "Consulate in the country of origin. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
        'consular_template': (
            "Peruvian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Peru. Peru is a Hague Apostille "
            "Convention member. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Peruvian funeral director takes custody at Jorge Chavez "
            "International Airport Lima (LIM) cargo terminal. RENIEC (Registro "
            "Nacional de Identificacion y Estado Civil) registers the death. "
            "Peru is a Hague Apostille Convention member; apostille certificates "
            "from member states are accepted. All other documents require "
            "certified Spanish translation and full consular authentication. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Peruvian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-peru',
    },
    'ecuador': {
        'name': 'Ecuador',
        'slug': 'ecuador',
        'key': 'ec',
        'reception': (
            "The Ecuadorian funeral director takes custody at Quito Mariscal Sucre "
            "International Airport (UIO) or Guayaquil Jose Joaquin de Olmedo "
            "International Airport (GYE) cargo terminal, depending on the "
            "family's destination. Death registration is handled by DIGERCIC "
            "(Direccion General de Registro Civil, Identificacion y Cedulacion), "
            "Ecuador's civil registry directorate. Ecuador is a member of the "
            "Hague Apostille Convention; apostille certificates are accepted for "
            "documents from member states. All other foreign documents require "
            "certified Spanish translation and full consular authentication through "
            "the Ecuadorian Embassy or Consulate in the country of origin. An "
            "embalming certificate and hermetically sealed coffin are required "
            "for all air imports. "
            "(Ecuadorian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Ecuadorian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Ecuador. Ecuador is "
            "a Hague Apostille Convention member. The Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Ecuadorian funeral director takes custody at Quito Mariscal "
            "Sucre International Airport (UIO) or Guayaquil Jose Joaquin de "
            "Olmedo International Airport (GYE) cargo terminal. DIGERCIC "
            "(Direccion General de Registro Civil, Identificacion y Cedulacion) "
            "registers the death. Ecuador is a Hague Apostille Convention member; "
            "apostille certificates from member states are accepted. All other "
            "documents require certified Spanish translation and full consular "
            "authentication. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Ecuadorian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-ecuador',
    },
    'tanzania': {
        'name': 'Tanzania',
        'slug': 'tanzania',
        'key': 'tz',
        'reception': (
            "The Tanzanian funeral director takes custody at Julius Nyerere "
            "International Airport Dar es Salaam (DAR) or Kilimanjaro "
            "International Airport (JRO) cargo terminal, depending on the "
            "destination region. Death registration is handled by RITA "
            "(Registration, Insolvency and Trusteeship Agency), Tanzania's "
            "civil registration authority. Death certificates are issued in "
            "English and Swahili, both official languages of Tanzania. Tanzania "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication through the Tanzanian High Commission or Embassy in "
            "the country of origin is required. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Tanzanian Ministry of Foreign Affairs and East African Cooperation, 2025.)"
        ),
        'consular_template': (
            "Tanzanian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Tanzania. Tanzania "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. The High Commission cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Tanzanian funeral director takes custody at Julius Nyerere "
            "International Airport Dar es Salaam (DAR) or Kilimanjaro "
            "International Airport (JRO) cargo terminal. RITA (Registration, "
            "Insolvency and Trusteeship Agency) registers the death; certificates "
            "are issued in English and Swahili. Tanzania is not a Hague Apostille "
            "member; full consular authentication through the Tanzanian High "
            "Commission or Embassy in the origin country is required. An "
            "embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Tanzanian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-tanzania',
    },
    'senegal': {
        'name': 'Senegal',
        'slug': 'senegal',
        'key': 'sn',
        'reception': (
            "The Senegalese funeral director takes custody at Blaise Diagne "
            "International Airport Dakar (DSS) cargo terminal. Death registration "
            "is handled by the local Centre d'Etat Civil (civil status centre) at "
            "commune level. Death certificates (actes de deces) are issued in "
            "French, the official language. For Muslim remains, which account for "
            "the large majority of the Senegalese population, Islamic law "
            "procedures apply and prompt burial is expected. Senegal is not a "
            "member of the Hague Apostille Convention; full consular authentication "
            "through the Senegalese Embassy or Consulate in the country of origin "
            "is required. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. "
            "(Senegalese Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Senegalese Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Senegal. Senegal "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. The Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Senegalese funeral director takes custody at Blaise Diagne "
            "International Airport Dakar (DSS) cargo terminal. The local Centre "
            "d'Etat Civil registers the death and issues an acte de deces in "
            "French. For Muslim remains, Islamic law procedures apply and prompt "
            "burial is expected. Senegal is not a Hague Apostille member; full "
            "consular authentication through the Senegalese Embassy or Consulate "
            "in the origin country is required. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Senegalese Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-senegal',
    },
    'cameroon': {
        'name': 'Cameroon',
        'slug': 'cameroon',
        'key': 'cm',
        'reception': (
            "The Cameroonian funeral director takes custody at Douala International "
            "Airport (DLA) or Yaounde Nsimalen International Airport (NSI) cargo "
            "terminal. Death registration is handled by the local Centre d'Etat "
            "Civil at arrondissement level. Cameroon is bilingual; death "
            "certificates are issued in French or English depending on the "
            "region. Cameroon is not a member of the Hague Apostille Convention; "
            "full consular authentication through the Cameroonian High Commission "
            "or Embassy in the country of origin is required. Documents from "
            "English-speaking origins may be accepted in Anglophone regions "
            "without translation; French documents are accepted in Francophone "
            "regions. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. "
            "(Cameroonian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Cameroonian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Cameroon. Cameroon "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. The High Commission cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Cameroonian funeral director takes custody at Douala "
            "International Airport (DLA) or Yaounde Nsimalen International "
            "Airport (NSI) cargo terminal. The local Centre d'Etat Civil at "
            "arrondissement level registers the death. Cameroon is bilingual; "
            "certificates are in French or English by region. Cameroon is not "
            "a Hague Apostille member; full consular authentication through the "
            "Cameroonian High Commission or Embassy in the origin country is "
            "required. An embalming certificate and hermetically sealed coffin "
            "are required."
        ),
        'emergency_line': 'contact the Cameroonian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-cameroon',
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
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Spain is widely available.",
        'postmortem_trigger': "Violent or unexplained deaths (Juzgado de Guardia)",
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
    'japan': {
        'name': 'Japan',
        'emergency': '110 (police) / 119 (fire and ambulance)',
        'registry': 'the local municipal office (kuyakusho or shiyakusho) civil registration section',
        'cert_name': 'shibo todoke-juri shomeisho (death registration receipt) and koseki (family register)',
        'cert_lang': 'Japanese',
        'overview': (
            "Call 110 for police or 119 for fire and ambulance. Death is certified "
            "by a physician, who issues a shindansho (medical certificate). The "
            "family files a shibo todoke (death notification) with the local "
            "municipal office (kuyakusho or shiyakusho) within 7 days. The koseki "
            "(family register) is updated to reflect the death. Police (keisatsu) "
            "and the public prosecutor (kensatsu) take jurisdiction for violent or "
            "unexplained deaths. Japan is a Hague Apostille Convention member. All "
            "Japanese-language documents require certified translation before "
            "submission to foreign authorities; allow additional time for "
            "translation. The British Embassy in Tokyo can assist British nationals."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is the predominant funeral practice in Japan and is widely "
            "available. A cremation certificate is required for export of ashes. "
            "For families of faiths that require burial, specialist coordination "
            "is needed as burial plots in Japan are limited."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (keisatsu and kensatsu take jurisdiction)',
    },
}

ROUTES = [
    # R63 -- Turkey wave 1
    {
        'origin': 'united-kingdom', 'dest': 'turkey',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Turkey include one of the largest expat "
            "communities in the country, comprising retirees, property owners, "
            "tourism and hospitality workers, and a substantial community in "
            "coastal resorts such as Antalya, Bodrum, Fethiye, and Dalaman. "
            "Turkey and the United Kingdom maintain bilateral diplomatic relations. "
            "British death certificates are issued by the relevant register office "
            "and require authentication by the Turkish Embassy in London. Turkey "
            "is a member of the Hague Apostille Convention; apostille certificates "
            "are accepted for UK-issued documents. For British nationals, the "
            "British Consulate in Istanbul or the British Embassy in Ankara assists "
            "with registration and document verification. "
            "(FCDO Travel Advice: Turkey, 2025; Turkish Ministry of Interior, "
            "Directorate General of Civil Registration and Nationality, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'turkey',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Turkey include business professionals, academics, "
            "tourists, and a community with bilateral ties reflecting US-Turkey "
            "relations within NATO. English-language US death certificates require "
            "authentication by the Turkish Embassy in Washington DC. Turkey is a "
            "member of the Hague Apostille Convention; apostille certificates are "
            "accepted for US-issued documents. The US Embassy in Ankara or the "
            "US Consulate in Istanbul handles consular matters for US nationals "
            "in Turkey. "
            "(Turkish Ministry of Interior, Directorate General of Civil "
            "Registration and Nationality, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'turkey',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Turkey include tourists, backpackers, and "
            "individuals with bilateral ties, including those visiting Gallipoli "
            "and ANZAC memorial sites. Australia and Turkey maintain bilateral "
            "diplomatic relations with shared historical significance at Gallipoli. "
            "Australian death certificates require authentication by the Turkish "
            "Embassy in Canberra. Turkey is a member of the Hague Apostille "
            "Convention; apostille certificates are accepted for Australian "
            "documents. The British Embassy in Ankara and the British Consulate "
            "in Istanbul can assist Australian nationals under the Canada-Australia "
            "CANBERRA Pact arrangement in countries without an Australian post, "
            "though Australia maintains its own Embassy in Ankara. "
            "(Turkish Ministry of Interior, Directorate General of Civil "
            "Registration and Nationality, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'turkey',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in Turkey include tourists, business professionals, "
            "and a community with bilateral ties reflecting the large Turkish-Canadian "
            "diaspora. Canada and Turkey maintain bilateral diplomatic relations "
            "within NATO and G20 frameworks. Canadian death certificates (in "
            "English or French) require authentication by the Turkish Embassy in "
            "Ottawa. Turkey is a member of the Hague Apostille Convention; "
            "apostille certificates are accepted for Canadian documents. The "
            "Canadian Embassy in Ankara handles consular matters for Canadian "
            "nationals in Turkey. "
            "(Turkish Ministry of Interior, Directorate General of Civil "
            "Registration and Nationality, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'turkey',
        'embassy_city': 'Tokyo',
        'intro': (
            "Japanese nationals in Turkey include tourists, business professionals, "
            "and researchers. Japan and Turkey maintain bilateral diplomatic "
            "relations reflecting historical ties. Japanese documents (shibo todoke "
            "and koseki, in Japanese) require certified translation and "
            "authentication by the Turkish Embassy in Tokyo. Turkey is a member "
            "of the Hague Apostille Convention; apostille certificates are accepted "
            "for Japanese documents once translated. The Japanese Embassy in Ankara "
            "handles consular matters for Japanese nationals in Turkey. Allow "
            "additional time for Japanese-language document translation. "
            "(Turkish Ministry of Interior, Directorate General of Civil "
            "Registration and Nationality, 2025.)"
        ),
    },
    # R63 -- Poland wave 1
    {
        'origin': 'united-kingdom', 'dest': 'poland',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Poland include business professionals, students, "
            "and individuals with bilateral ties including the large Polish community "
            "resident in the United Kingdom. Poland and the UK maintain bilateral "
            "diplomatic relations as NATO allies, with close people-to-people ties "
            "through the Polish community in Britain. British death certificates "
            "require a certified sworn translation into Polish and authentication "
            "by the Polish Embassy in London. Poland is an EU member and Hague "
            "Apostille Convention member; apostille certificates are accepted for "
            "UK-issued documents. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'poland',
        'embassy_city': 'Berlin',
        'intro': (
            "Polish nationals in Germany form one of the largest diaspora "
            "communities in Germany, reflecting close bilateral ties as EU and "
            "NATO neighbours. When a Polish national dies in Germany, the death "
            "is registered at the local Standesamt (civil registry) and a "
            "Sterbeurkunde is issued in German. German death certificates require "
            "a certified sworn translation into Polish. Poland and Germany are "
            "both EU members and Hague Apostille Convention members; apostille "
            "certificates are accepted for German documents. The Polish Embassy "
            "in Berlin advises on documentation. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'poland',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Poland include business professionals, military "
            "personnel, and a community with bilateral ties reflecting the "
            "large Polish-American diaspora. Poland and the United States "
            "maintain close bilateral relations as NATO allies. English-language "
            "US death certificates require a certified sworn translation into "
            "Polish and authentication by the Polish Embassy in Washington DC. "
            "Poland is a Hague Apostille Convention member; apostille certificates "
            "are accepted for US-issued documents. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'poland',
        'embassy_city': 'Paris',
        'intro': (
            "Polish nationals in France include a community of workers, students, "
            "and professionals, reflecting the movement of people within the EU "
            "single market. France and Poland maintain bilateral EU and NATO "
            "relations. French death certificates (acte de deces, in French) "
            "require a certified sworn translation into Polish and authentication "
            "by the Polish Embassy in Paris. Poland and France are both EU "
            "members and Hague Apostille Convention members; apostille "
            "certificates are accepted for French documents. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'poland',
        'embassy_city': 'The Hague',
        'intro': (
            "Polish nationals in the Netherlands form a significant community "
            "of workers and professionals, reflecting labour migration within the "
            "EU single market. The Netherlands and Poland maintain bilateral EU "
            "and NATO relations. Dutch death certificates (akte van overlijden, "
            "in Dutch) require a certified sworn translation into Polish and "
            "authentication by the Polish Embassy in The Hague. Both countries "
            "are EU members and Hague Apostille Convention members; apostille "
            "certificates are accepted for Dutch documents. "
            "(Polish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R63 -- Romania wave 1
    {
        'origin': 'united-kingdom', 'dest': 'romania',
        'embassy_city': 'London',
        'intro': (
            "Romanian nationals in the United Kingdom form one of the largest "
            "diaspora communities in the country, with a substantial presence in "
            "the workforce across agriculture, construction, health and social "
            "care, and hospitality. When a Romanian national dies in the UK, the "
            "death is registered at the relevant register office. British death "
            "certificates require certified Romanian translation and authentication "
            "by the Romanian Embassy in London. Romania is an EU member and Hague "
            "Apostille Convention member; apostille certificates are accepted for "
            "UK-issued documents. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'romania',
        'embassy_city': 'Rome',
        'intro': (
            "Romanian nationals in Italy form one of the largest immigrant "
            "communities in the country, with a long-established presence in "
            "agriculture, domestic care, construction, and industry. When a "
            "Romanian national dies in Italy, the death is registered at the "
            "local Ufficio di Stato Civile. Italian death certificates (atto di "
            "morte, in Italian) require certified Romanian translation and "
            "authentication by the Romanian Embassy in Rome. Both countries are "
            "EU members and Hague Apostille Convention members; apostille "
            "certificates are accepted. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'romania',
        'embassy_city': 'Madrid',
        'intro': (
            "Romanian nationals in Spain form a substantial community, with a "
            "significant presence in agriculture, construction, and domestic care "
            "sectors. When a Romanian national dies in Spain, the death is "
            "registered at the local Registro Civil. Spanish death certificates "
            "(certificado de defuncion, in Spanish) require certified Romanian "
            "translation and authentication by the Romanian Embassy in Madrid. "
            "Both countries are EU members and Hague Apostille Convention members; "
            "apostille certificates are accepted. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'romania',
        'embassy_city': 'Berlin',
        'intro': (
            "Romanian nationals in Germany include a growing community of workers "
            "and professionals, reflecting EU free movement. Germany and Romania "
            "maintain bilateral EU and NATO relations. German death certificates "
            "(Sterbeurkunde, in German) require certified Romanian translation and "
            "authentication by the Romanian Embassy in Berlin. Both countries are "
            "EU members and Hague Apostille Convention members; apostille "
            "certificates are accepted for German documents. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'romania',
        'embassy_city': 'Paris',
        'intro': (
            "Romanian nationals in France include a community of workers and "
            "professionals, reflecting EU free movement and bilateral ties. "
            "France and Romania maintain bilateral EU and NATO relations. French "
            "death certificates (acte de deces, in French) require certified "
            "Romanian translation and authentication by the Romanian Embassy in "
            "Paris. Both countries are EU members and Hague Apostille Convention "
            "members; apostille certificates are accepted for French documents. "
            "(Romanian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R63 -- Iraq wave 1
    {
        'origin': 'united-kingdom', 'dest': 'iraq',
        'embassy_city': 'London',
        'intro': (
            "Iraqi nationals in the United Kingdom include one of the largest "
            "Iraqi diaspora communities in Europe, with a substantial presence "
            "in London and other cities. When an Iraqi national dies in the UK, "
            "the death is registered at the relevant register office. British "
            "death certificates require certified Arabic translation and "
            "authentication by the Iraqi Embassy in London. Iraq is not a member "
            "of the Hague Apostille Convention; full consular authentication is "
            "required. The FCDO advises against all travel to Iraq except the "
            "Kurdistan Region; families should use a repatriation specialist with "
            "current ground contacts. "
            "(FCDO Travel Advice: Iraq, 2025; Iraqi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'iraq',
        'embassy_city': 'Washington DC',
        'intro': (
            "Iraqi nationals in the United States include a substantial diaspora "
            "community, particularly in Michigan, California, and Tennessee. "
            "English-language US death certificates require certified Arabic "
            "translation and authentication by the Iraqi Embassy in Washington DC. "
            "Iraq is not a Hague Apostille Convention member; full consular "
            "authentication is required. The FCDO advises against all travel "
            "to Iraq except the Kurdistan Region; families should work with a "
            "specialist who maintains current contacts on the ground. "
            "(FCDO Travel Advice: Iraq, 2025; Iraqi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'iraq',
        'embassy_city': 'Berlin',
        'intro': (
            "Iraqi nationals in Germany include a significant diaspora community "
            "with bilateral ties reflecting decades of migration. German death "
            "certificates (Sterbeurkunde, in German) require certified Arabic "
            "translation and authentication by the Iraqi Embassy in Berlin. Iraq "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. The FCDO advises against all travel "
            "to Iraq except the Kurdistan Region; families should use a "
            "specialist with current ground knowledge. "
            "(FCDO Travel Advice: Iraq, 2025; Iraqi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'iraq',
        'embassy_city': 'Canberra',
        'intro': (
            "Iraqi nationals in Australia include a diaspora community with a "
            "presence across Melbourne, Sydney, and Adelaide. Australian death "
            "certificates require certified Arabic translation and authentication "
            "by the Iraqi Embassy in Canberra. Iraq is not a Hague Apostille "
            "Convention member; full consular authentication is required. The "
            "FCDO advises against all travel to Iraq except the Kurdistan Region; "
            "families should work with a specialist who has current contacts "
            "on the ground. "
            "(FCDO Travel Advice: Iraq, 2025; Iraqi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'iraq',
        'embassy_city': 'Paris',
        'intro': (
            "Iraqi nationals in France include a diaspora community with bilateral "
            "ties. French death certificates (acte de deces, in French) require "
            "certified Arabic translation and authentication by the Iraqi Embassy "
            "in Paris. Iraq is not a Hague Apostille Convention member; full "
            "consular authentication is required. The FCDO advises against all "
            "travel to Iraq except the Kurdistan Region; families should engage "
            "a specialist with current operational knowledge. "
            "(FCDO Travel Advice: Iraq, 2025; Iraqi Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R63 -- Lebanon wave 1
    {
        'origin': 'united-kingdom', 'dest': 'lebanon',
        'embassy_city': 'London',
        'intro': (
            "Lebanese nationals in the United Kingdom include one of the largest "
            "Lebanese diaspora communities in Europe, with long-established "
            "businesses, academic, and professional ties. When a Lebanese national "
            "dies in the UK, the death is registered at the relevant register "
            "office. British death certificates require certified Arabic translation "
            "and authentication by the Lebanese Embassy in London. Lebanon is not "
            "a member of the Hague Apostille Convention; full consular "
            "authentication is required. The FCDO advises against travel to "
            "Lebanon; families should verify current airline services and consular "
            "access before proceeding. "
            "(FCDO Travel Advice: Lebanon, 2025; Lebanese Ministry of Foreign "
            "Affairs and Emigrants, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'lebanon',
        'embassy_city': 'Washington DC',
        'intro': (
            "Lebanese nationals in the United States include a substantial diaspora "
            "community with long-established presence across Dearborn, Michigan, "
            "New York, and other cities. English-language US death certificates "
            "require certified Arabic translation and authentication by the "
            "Lebanese Embassy in Washington DC. Lebanon is not a Hague Apostille "
            "Convention member; full consular authentication is required. The FCDO "
            "advises against travel to Lebanon; families should verify current "
            "airline operations and consular access. "
            "(FCDO Travel Advice: Lebanon, 2025; Lebanese Ministry of Foreign "
            "Affairs and Emigrants, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'lebanon',
        'embassy_city': 'Paris',
        'intro': (
            "Lebanese nationals in France include a large and long-established "
            "diaspora with deep cultural and linguistic ties, reflecting the "
            "French-Lebanese bilateral relationship and the use of French in "
            "Lebanese administration. French death certificates (acte de deces, "
            "in French) are widely accepted in Lebanese administrative practice. "
            "Lebanon is not a Hague Apostille Convention member; full consular "
            "authentication through the Lebanese Embassy in Paris is required. "
            "The FCDO advises against travel to Lebanon; families should verify "
            "current airline operations and consular access. "
            "(FCDO Travel Advice: Lebanon, 2025; Lebanese Ministry of Foreign "
            "Affairs and Emigrants, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'lebanon',
        'embassy_city': 'Berlin',
        'intro': (
            "Lebanese nationals in Germany include a diaspora community with "
            "bilateral ties. German death certificates (Sterbeurkunde, in German) "
            "require certified Arabic translation and authentication by the "
            "Lebanese Embassy in Berlin. Lebanon is not a Hague Apostille "
            "Convention member; full consular authentication is required. The FCDO "
            "advises against travel to Lebanon; families should verify current "
            "airline services and consular access before proceeding. "
            "(FCDO Travel Advice: Lebanon, 2025; Lebanese Ministry of Foreign "
            "Affairs and Emigrants, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'lebanon',
        'embassy_city': 'Canberra',
        'intro': (
            "Lebanese nationals in Australia include one of the largest Lebanese "
            "diaspora communities in the world, with a long-established presence "
            "in Sydney, Melbourne, and other cities. Australian death certificates "
            "require certified Arabic translation and authentication by the "
            "Lebanese Embassy in Canberra. Lebanon is not a Hague Apostille "
            "Convention member; full consular authentication is required. The "
            "FCDO advises against travel to Lebanon; families should verify "
            "current airline services and consular access before proceeding. "
            "(FCDO Travel Advice: Lebanon, 2025; Lebanese Ministry of Foreign "
            "Affairs and Emigrants, 2025.)"
        ),
    },
    # R64 -- Peru wave 1
    {
        'origin': 'united-kingdom', 'dest': 'peru',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Peru include tourists, trekkers, researchers, "
            "and a small expat community. Peru is one of South America's most "
            "visited destinations, with the Inca Trail and Machu Picchu attracting "
            "significant numbers of British visitors each year. British death "
            "certificates require certified Spanish translation and authentication "
            "by the Peruvian Embassy in London. Peru is a member of the Hague "
            "Apostille Convention; apostille certificates are accepted for "
            "UK-issued documents. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'peru',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Peru include tourists, business professionals, and "
            "a community with bilateral ties reflecting significant US investment "
            "in the Peruvian mining, energy, and technology sectors. English-language "
            "US death certificates require certified Spanish translation and "
            "authentication by the Peruvian Embassy in Washington DC. Peru is a "
            "Hague Apostille Convention member; apostille certificates are "
            "accepted for US-issued documents. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'peru',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Peru include business professionals and "
            "individuals with bilateral ties reflecting the long-standing "
            "Spain-Peru historical relationship and shared Spanish language. "
            "Spanish death certificates (certificado de defuncion) are accepted "
            "directly in Peru without translation. Peru is a member of the Hague "
            "Apostille Convention; apostille certificates are accepted for "
            "Spanish-issued documents. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'peru',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Peru include tourists, trekkers, researchers, "
            "and business professionals. Germany and Peru maintain bilateral "
            "diplomatic and development cooperation. German death certificates "
            "(Sterbeurkunde, in German) require certified Spanish translation "
            "and authentication by the Peruvian Embassy in Berlin. Peru is a "
            "Hague Apostille Convention member; apostille certificates are "
            "accepted for German documents. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'peru',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Peru include business professionals and a "
            "community with bilateral ties. Italy and Peru maintain bilateral "
            "diplomatic relations. Italian death certificates (atto di morte, "
            "in Italian) require certified Spanish translation and authentication "
            "by the Peruvian Embassy in Rome. Peru is a member of the Hague "
            "Apostille Convention; apostille certificates are accepted for "
            "Italian documents. "
            "(Peruvian Ministry of Foreign Affairs, MRE, 2025.)"
        ),
    },
    # R64 -- Ecuador wave 1
    {
        'origin': 'united-kingdom', 'dest': 'ecuador',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Ecuador include tourists, researchers, and a "
            "small expat community. Ecuador's Galapagos Islands attract significant "
            "international visitor numbers, including British tourists and "
            "naturalists. British death certificates require certified Spanish "
            "translation and authentication by the Ecuadorian Embassy in London. "
            "Ecuador is a member of the Hague Apostille Convention; apostille "
            "certificates are accepted for UK-issued documents. "
            "(Ecuadorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'ecuador',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Ecuador include retirees, business professionals, "
            "and tourists, reflecting the use of the US dollar as Ecuador's "
            "official currency and the resulting accessibility for US nationals. "
            "English-language US death certificates require certified Spanish "
            "translation and authentication by the Ecuadorian Embassy in "
            "Washington DC. Ecuador is a Hague Apostille Convention member; "
            "apostille certificates are accepted for US-issued documents. "
            "(Ecuadorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'ecuador',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Ecuador include a community with long-standing "
            "cultural and linguistic ties, as well as business professionals. "
            "Ecuador has a significant Spanish-heritage population. Spanish death "
            "certificates (certificado de defuncion) are accepted directly in "
            "Ecuador without translation. Ecuador is a Hague Apostille Convention "
            "member; apostille certificates are accepted for Spanish-issued "
            "documents. "
            "(Ecuadorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'ecuador',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Ecuador include researchers, tourists, and "
            "business professionals. Germany and Ecuador maintain bilateral "
            "diplomatic and development cooperation. German death certificates "
            "(Sterbeurkunde, in German) require certified Spanish translation "
            "and authentication by the Ecuadorian Embassy in Berlin. Ecuador "
            "is a Hague Apostille Convention member; apostille certificates "
            "are accepted for German documents. "
            "(Ecuadorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'ecuador',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Ecuador include a small business and expat "
            "community. Italy and Ecuador maintain bilateral diplomatic relations. "
            "Italian death certificates (atto di morte, in Italian) require "
            "certified Spanish translation and authentication by the Ecuadorian "
            "Embassy in Rome. Ecuador is a member of the Hague Apostille "
            "Convention; apostille certificates are accepted for Italian documents. "
            "(Ecuadorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R64 -- Tanzania wave 1
    {
        'origin': 'united-kingdom', 'dest': 'tanzania',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Tanzania include a significant community with "
            "historical ties, NGO workers, development professionals, and tourists "
            "visiting the Serengeti, Kilimanjaro, and Zanzibar. The UK and Tanzania "
            "maintain bilateral relations as Commonwealth members. British death "
            "certificates are issued by the relevant register office and require "
            "authentication by the Tanzanian High Commission in London. Tanzania "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication is required. English is widely used in Tanzanian "
            "administration alongside Swahili. "
            "(Tanzanian Ministry of Foreign Affairs and East African Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'tanzania',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Tanzania include development workers, NGO professionals, "
            "wildlife researchers, and tourists visiting national parks and the "
            "Zanzibar coast. The US maintains development cooperation with Tanzania "
            "through USAID programmes across health and agriculture. English-language "
            "US death certificates require authentication by the Tanzanian Embassy "
            "in Washington DC. Tanzania is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(Tanzanian Ministry of Foreign Affairs and East African Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'tanzania',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Tanzania include development workers, researchers, "
            "NGO professionals, and tourists. Germany and Tanzania maintain "
            "bilateral development cooperation through GIZ programmes. German "
            "death certificates (Sterbeurkunde, in German) require certified "
            "English or Swahili translation and authentication by the Tanzanian "
            "Embassy in Berlin. Tanzania is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Tanzanian Ministry of Foreign Affairs and East African Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'tanzania',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Tanzania include development workers, "
            "researchers, and tourists visiting the Serengeti and Kilimanjaro. "
            "Australia and Tanzania maintain bilateral Commonwealth ties. "
            "Australian death certificates (in English) require authentication "
            "by the Tanzanian High Commission in Canberra. Tanzania is not a "
            "Hague Apostille Convention member; full consular authentication is "
            "required. English-language documents are widely accepted in "
            "Tanzanian administration. "
            "(Tanzanian Ministry of Foreign Affairs and East African Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'tanzania',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Tanzania include development workers, researchers, "
            "and tourists. France and Tanzania maintain bilateral development "
            "cooperation and diplomatic relations. French death certificates "
            "(acte de deces, in French) require certified English or Swahili "
            "translation and authentication by the Tanzanian Embassy in Paris. "
            "Tanzania is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(Tanzanian Ministry of Foreign Affairs and East African Cooperation, 2025.)"
        ),
    },
    # R64 -- Senegal wave 1
    {
        'origin': 'france', 'dest': 'senegal',
        'embassy_city': 'Paris',
        'intro': (
            "Senegalese nationals in France form one of the largest Senegalese "
            "diaspora communities globally, with deep cultural, linguistic, and "
            "bilateral ties reflecting the France-Senegal historical relationship. "
            "Senegal and France maintain bilateral diplomatic and development "
            "cooperation. French death certificates (acte de deces, in French) "
            "are widely accepted in Senegalese administrative practice. Senegal "
            "is not a Hague Apostille Convention member; full consular "
            "authentication through the Senegalese Embassy in Paris is required. "
            "(Senegalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'senegal',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Senegal include development workers, NGO "
            "professionals, researchers, and tourists. The UK and Senegal "
            "maintain bilateral diplomatic and development relations. British "
            "death certificates require certified French translation and "
            "authentication by the Senegalese Embassy in London. Senegal is "
            "not a member of the Hague Apostille Convention; full consular "
            "authentication is required. For Muslim remains, which account for "
            "the large majority of the Senegalese population, Islamic law "
            "procedures apply and prompt burial is expected. "
            "(Senegalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'senegal',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Senegal include development workers, NGO professionals, "
            "Peace Corps volunteers, and a community with bilateral ties. The US "
            "maintains development cooperation with Senegal through USAID and "
            "other programmes. English-language US death certificates require "
            "certified French translation and authentication by the Senegalese "
            "Embassy in Washington DC. Senegal is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Senegalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'senegal',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Senegal include development workers, NGO "
            "professionals, and researchers. Germany and Senegal maintain "
            "bilateral development cooperation through GIZ programmes. German "
            "death certificates (Sterbeurkunde, in German) require certified "
            "French translation and authentication by the Senegalese Embassy "
            "in Berlin. Senegal is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(Senegalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'senegal',
        'embassy_city': 'Madrid',
        'intro': (
            "Senegalese nationals in Spain form a significant community, "
            "reflecting migration along the Spain-Senegal corridor and bilateral "
            "ties as neighbouring Atlantic countries. Spain and Senegal maintain "
            "bilateral diplomatic and migration cooperation. Spanish death "
            "certificates (certificado de defuncion, in Spanish) require "
            "certified French translation and authentication by the Senegalese "
            "Embassy in Madrid. Senegal is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Senegalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R64 -- Cameroon wave 1
    {
        'origin': 'france', 'dest': 'cameroon',
        'embassy_city': 'Paris',
        'intro': (
            "Cameroonian nationals in France include one of the largest "
            "Cameroonian diaspora communities globally, with deep cultural, "
            "linguistic, and bilateral ties reflecting the France-Cameroon "
            "historical relationship. Cameroon and France maintain close "
            "bilateral diplomatic and development cooperation. French death "
            "certificates (acte de deces, in French) are accepted in "
            "Francophone regions of Cameroon. Cameroon is not a Hague Apostille "
            "Convention member; full consular authentication through the "
            "Cameroonian Embassy in Paris is required. "
            "(Cameroonian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'cameroon',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Cameroon include development workers, NGO "
            "professionals, researchers, and business contacts. The UK and "
            "Cameroon maintain bilateral Commonwealth and diplomatic relations. "
            "British death certificates require authentication by the Cameroonian "
            "High Commission in London. Cameroon is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "English-language documents are accepted in Anglophone regions "
            "of Cameroon without translation. "
            "(Cameroonian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'cameroon',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Cameroon include development workers, NGO "
            "professionals, and researchers. The US maintains development "
            "cooperation with Cameroon through USAID programmes. English-language "
            "US death certificates require authentication by the Cameroonian "
            "Embassy in Washington DC. Cameroon is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "English-language documents are accepted in Anglophone regions "
            "of Cameroon. "
            "(Cameroonian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'cameroon',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Cameroon include development workers, NGO "
            "professionals, and researchers. Germany and Cameroon maintain "
            "bilateral development cooperation through GIZ programmes. German "
            "death certificates (Sterbeurkunde, in German) require certified "
            "French or English translation and authentication by the Cameroonian "
            "Embassy in Berlin. Cameroon is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Cameroonian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'cameroon',
        'embassy_city': 'Brussels',
        'intro': (
            "Cameroonian nationals in Belgium include a significant diaspora "
            "community with bilateral ties. Belgium and Cameroon maintain "
            "bilateral diplomatic relations. Belgian death certificates (in "
            "French or Dutch depending on region) require certified French or "
            "English translation and authentication by the Cameroonian Embassy "
            "in Brussels. Cameroon is not a Hague Apostille Convention member; "
            "full consular authentication is required. French-language Belgian "
            "documents are accepted directly in Francophone regions of Cameroon. "
            "(Cameroonian Ministry of Foreign Affairs, 2025.)"
        ),
    },
]


def make_dest_key(dest_slug):
    keys = {
        'turkey': 'tr', 'poland': 'pl', 'romania': 'ro', 'iraq': 'iq',
        'lebanon': 'lb', 'peru': 'pe', 'ecuador': 'ec', 'tanzania': 'tz',
        'senegal': 'sn', 'cameroon': 'cm',
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

    complexity = od['complexity']
    timeline_avg = od['timeline_avg']
    timeline_fast = od['timeline_fast']
    timeline_complex = od['timeline_complex']
    doc_time = od['doc_time']
    dest_key = dm['key']
    emergency_line = dm['emergency_line']

    desc_note = complexity_to_desc(complexity)
    t_origin = title_name(origin_name)
    t_dest = title_name(dest_name)
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
