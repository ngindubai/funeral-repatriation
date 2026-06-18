#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R61-R62.

   R61 (25 routes, variants B,C,D,E,A x5):
     Nigeria x5: united-kingdom, united-states, germany, france, italy
     Kenya x5: united-kingdom, united-states, germany, australia, france
     Ghana x5: united-kingdom, united-states, germany, italy, netherlands
     Nepal x5: united-kingdom, united-states, germany, india, australia
     Ethiopia x5: united-kingdom, united-states, germany, france, italy

   R62 (25 routes, variants B,C,D,E,A x5):
     Brazil x5: united-kingdom, united-states, germany, spain, italy
     Mexico x5: united-kingdom, united-states, germany, spain, canada
     Colombia x5: united-kingdom, united-states, spain, germany, italy
     Argentina x5: united-kingdom, united-states, spain, italy, germany
     Algeria x5: france, spain, belgium, netherlands, germany

   Template rotation: R60 ended A (index 0). R61 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'nigeria': {
        'name': 'Nigeria',
        'slug': 'nigeria',
        'key': 'ng',
        'reception': (
            "The Nigerian funeral director takes custody at Murtala Muhammed "
            "International Airport Lagos (LOS) or Nnamdi Azikiwe International "
            "Airport Abuja (ABV) cargo terminal, depending on the family's "
            "destination. The National Population Commission (NPC) handles civil "
            "registration of deaths. Ministry of Health clearance is required "
            "before final disposition. For Muslim remains, Islamic law procedures "
            "apply and prompt burial is expected. All foreign documents require "
            "certified English translation where applicable; English is Nigeria's "
            "official language, which simplifies documentation from "
            "English-speaking origin countries. Nigeria is not a member of the "
            "Hague Apostille Convention; full consular authentication through the "
            "Nigerian High Commission or Embassy in the country of origin is "
            "required. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Nigerian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Nigeria. The High "
            "Commission cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Nigerian funeral director takes custody at Murtala Muhammed "
            "International Airport Lagos (LOS) or Nnamdi Azikiwe International "
            "Airport Abuja (ABV) cargo terminal. The National Population "
            "Commission (NPC) handles civil registration. Ministry of Health "
            "clearance is required before final disposition. For Muslim remains, "
            "Islamic law procedures apply and prompt burial is expected. Nigeria "
            "is not a Hague Apostille member; full consular authentication "
            "through the Nigerian High Commission or Embassy in the origin "
            "country is required. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Nigerian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-nigeria',
    },
    'kenya': {
        'name': 'Kenya',
        'slug': 'kenya',
        'key': 'ke',
        'reception': (
            "The Kenyan funeral director takes custody at Jomo Kenyatta "
            "International Airport Nairobi (NBO) cargo terminal. The Civil "
            "Registration Department (CRD) under the Registrar General handles "
            "death registration. Ministry of Health clearance is required before "
            "final disposition. Kenya joined the Hague Apostille Convention in "
            "2021; apostille certificates are accepted for documents from member "
            "states. All other foreign documents require full consular "
            "authentication through the Kenyan High Commission or Embassy in "
            "the country of origin. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. English is Kenya's "
            "official language, which simplifies documentation from "
            "English-speaking origin countries. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025.)"
        ),
        'consular_template': (
            "Kenyan High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Kenya. Kenya joined "
            "the Hague Apostille Convention in 2021. The High Commission cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Kenyan funeral director takes custody at Jomo Kenyatta "
            "International Airport Nairobi (NBO) cargo terminal. The Civil "
            "Registration Department (CRD) registers the death. Ministry of "
            "Health clearance is required before final disposition. Kenya joined "
            "the Hague Apostille Convention in 2021; apostille certificates are "
            "accepted from member states. All other documents require full "
            "consular authentication through the Kenyan High Commission or "
            "Embassy in the origin country. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Kenyan High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-kenya',
    },
    'ghana': {
        'name': 'Ghana',
        'slug': 'ghana',
        'key': 'gh',
        'reception': (
            "The Ghanaian funeral director takes custody at Kotoka International "
            "Airport Accra (ACC) cargo terminal. The Births and Deaths Registry "
            "(BDR) under the Registrar General's Department handles death "
            "registration. Ministry of Health clearance is required before final "
            "disposition. Ghana is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Ghanaian High "
            "Commission or Embassy in the country of origin is required. English "
            "is Ghana's official language, which simplifies documentation from "
            "English-speaking origin countries. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Ghanaian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Ghanaian High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Ghana. Ghana is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. The High Commission cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Ghanaian funeral director takes custody at Kotoka International "
            "Airport Accra (ACC) cargo terminal. The Births and Deaths Registry "
            "(BDR) under the Registrar General's Department registers the death. "
            "Ministry of Health clearance is required before final disposition. "
            "Ghana is not a Hague Apostille member; full consular authentication "
            "through the Ghanaian High Commission or Embassy in the origin "
            "country is required. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Ghanaian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-ghana',
    },
    'nepal': {
        'name': 'Nepal',
        'slug': 'nepal',
        'key': 'np',
        'reception': (
            "The Nepalese funeral director takes custody at Tribhuvan "
            "International Airport Kathmandu (KTM) cargo terminal. Death "
            "registration is handled by the local Ward Office under Nepal's "
            "civil registration system. Ministry of Health clearance is required "
            "before final disposition. For Hindu remains, traditional funeral "
            "rites at the ghats of the Bagmati or Gandaki rivers are observed "
            "by many families. Nepal is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Nepalese "
            "Embassy in the country of origin is required. All foreign documents "
            "require certified Nepali or English translation. An embalming "
            "certificate and hermetically sealed coffin are required for all air "
            "imports. (Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Nepalese Embassy in {city} can advise on documentation requirements "
            "for repatriation to Nepal. Nepal is not a Hague Apostille Convention "
            "member; full consular authentication is required. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Nepalese funeral director takes custody at Tribhuvan "
            "International Airport Kathmandu (KTM) cargo terminal. Death "
            "registration is handled by the local Ward Office under Nepal's "
            "civil registration system. Ministry of Health clearance is required "
            "before final disposition. For Hindu remains, traditional funeral "
            "rites at the river ghats are observed by many families. Nepal is "
            "not a Hague Apostille member; full consular authentication through "
            "the Nepalese Embassy in the origin country is required. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Nepalese Embassy in the origin country',
        'hub_url': 'repatriation-from-nepal',
    },
    'ethiopia': {
        'name': 'Ethiopia',
        'slug': 'ethiopia',
        'key': 'et',
        'reception': (
            "The Ethiopian funeral director takes custody at Addis Ababa Bole "
            "International Airport (ADD) cargo terminal. VERA, Ethiopia's civil "
            "events registration authority, handles death registration. Ministry "
            "of Health clearance is required before final disposition. Ethiopia "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication through the Ethiopian Embassy in the country of "
            "origin is required. Amharic is the official language; all foreign "
            "documents require certified Amharic or English translation. An "
            "embalming certificate and hermetically sealed coffin are required "
            "for all air imports. "
            "(Ethiopian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Ethiopian Embassy in {city} can advise on documentation requirements "
            "for repatriation to Ethiopia. Ethiopia is not a Hague Apostille "
            "Convention member; full consular authentication is required. The "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Ethiopian funeral director takes custody at Addis Ababa Bole "
            "International Airport (ADD) cargo terminal. VERA, Ethiopia's civil "
            "events registration authority, handles death registration. Ministry "
            "of Health clearance is required before final disposition. Ethiopia "
            "is not a Hague Apostille member; full consular authentication "
            "through the Ethiopian Embassy in the origin country is required. "
            "All foreign documents require certified Amharic or English "
            "translation. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Ethiopian Embassy in the origin country',
        'hub_url': 'repatriation-from-ethiopia',
    },
    'brazil': {
        'name': 'Brazil',
        'slug': 'brazil',
        'key': 'br',
        'reception': (
            "The Brazilian funeral director takes custody at Guarulhos "
            "International Airport Sao Paulo (GRU) or Rio de Janeiro "
            "International Airport (GIG) cargo terminal, depending on the "
            "family's destination. The Cartorio de Registro Civil (Civil "
            "Registry) registers the death locally. ANVISA (Brazilian Health "
            "Regulatory Agency) clearance is required for all imported human "
            "remains. Brazil joined the Hague Apostille Convention in 2016; "
            "apostille certificates are accepted for documents from member "
            "states. All other foreign documents require full consular "
            "authentication through the Brazilian Embassy or Consulate in the "
            "country of origin. All documents in languages other than Portuguese "
            "require certified Portuguese translation. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
        'consular_template': (
            "Brazilian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Brazil. Brazil joined "
            "the Hague Apostille Convention in 2016. The Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Brazilian funeral director takes custody at Guarulhos "
            "International Airport Sao Paulo (GRU) or Rio de Janeiro "
            "International Airport (GIG) cargo terminal. The Cartorio de "
            "Registro Civil registers the death locally. ANVISA clearance is "
            "required for all imported remains. Brazil joined the Hague Apostille "
            "Convention in 2016; apostille certificates are accepted from member "
            "states. Documents not in Portuguese require certified Portuguese "
            "translation. An embalming certificate and hermetically sealed "
            "coffin are required. The receiving funeral director coordinates "
            "with the Cartorio and the relevant state health authority."
        ),
        'emergency_line': 'contact the Brazilian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-brazil',
    },
    'mexico': {
        'name': 'Mexico',
        'slug': 'mexico',
        'key': 'mx',
        'reception': (
            "The Mexican funeral director takes custody at Benito Juarez "
            "International Airport Mexico City (MEX) or the relevant regional "
            "airport cargo terminal. The Registro Civil (Civil Registry) in the "
            "relevant state processes death registration. The Servicio Medico "
            "Forense (SEMEFO) may take jurisdiction for deaths from violent or "
            "unclear causes. Mexico is a member of the Hague Apostille "
            "Convention; apostille certificates are accepted for documents from "
            "member states. All other foreign documents require certified Spanish "
            "translation and full consular authentication through the Mexican "
            "Embassy or Consulate in the country of origin. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
        'consular_template': (
            "Mexican Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Mexico. Mexico is a Hague Apostille "
            "Convention member. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Mexican funeral director takes custody at Benito Juarez "
            "International Airport Mexico City (MEX) or the relevant regional "
            "airport cargo terminal. The Registro Civil in the relevant state "
            "registers the death. SEMEFO may take jurisdiction for violent or "
            "unclear deaths. Mexico is a Hague Apostille Convention member; "
            "apostille certificates are accepted from member states. All other "
            "documents require certified Spanish translation and full consular "
            "authentication. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Mexican Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-mexico',
    },
    'colombia': {
        'name': 'Colombia',
        'slug': 'colombia',
        'key': 'co',
        'reception': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport Bogota (BOG) or the relevant regional airport "
            "cargo terminal. The Notaria or Registraduria Nacional del Estado "
            "Civil handles civil registration of the death. The Instituto "
            "Nacional de Medicina Legal y Ciencias Forenses (Medicina Legal) "
            "takes jurisdiction for deaths from violent or unclear causes. "
            "Colombia is a member of the Hague Apostille Convention; apostille "
            "certificates are accepted for documents from member states. All "
            "other foreign documents require certified Spanish translation and "
            "full consular authentication through the Colombian Embassy or "
            "Consulate in the country of origin. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
        'consular_template': (
            "Colombian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Colombia. Colombia "
            "is a Hague Apostille Convention member. The Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Colombian funeral director takes custody at El Dorado "
            "International Airport Bogota (BOG) or the relevant regional airport "
            "cargo terminal. The Notaria or Registraduria Nacional del Estado "
            "Civil registers the death. Medicina Legal (Instituto Nacional de "
            "Medicina Legal y Ciencias Forenses) takes jurisdiction for violent "
            "or unclear deaths. Colombia is a Hague Apostille Convention member; "
            "apostille certificates are accepted from member states. All other "
            "documents require certified Spanish translation and full consular "
            "authentication. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Colombian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-colombia',
    },
    'argentina': {
        'name': 'Argentina',
        'slug': 'argentina',
        'key': 'ar',
        'reception': (
            "The Argentine funeral director takes custody at Ministro Pistarini "
            "International Airport Buenos Aires (EZE) cargo terminal. The "
            "Registro Civil at provincial level handles civil registration of "
            "the death. The Cuerpo Medico Forense (forensic medical unit) takes "
            "jurisdiction for deaths from violent or unclear causes. Argentina "
            "is a member of the Hague Apostille Convention; apostille "
            "certificates are accepted for documents from member states. All "
            "other foreign documents require certified Spanish translation and "
            "full consular authentication through the Argentine Embassy or "
            "Consulate in the country of origin. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Argentine Ministry of Foreign Affairs, International Trade and "
            "Worship, Cancilleria, 2025.)"
        ),
        'consular_template': (
            "Argentine Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Argentina. Argentina "
            "is a Hague Apostille Convention member. The Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Argentine funeral director takes custody at Ministro Pistarini "
            "International Airport Buenos Aires (EZE) cargo terminal. The "
            "Registro Civil at provincial level registers the death. The Cuerpo "
            "Medico Forense takes jurisdiction for violent or unclear deaths. "
            "Argentina is a Hague Apostille Convention member; apostille "
            "certificates are accepted from member states. All other documents "
            "require certified Spanish translation and full consular "
            "authentication. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Argentine Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-argentina',
    },
    'algeria': {
        'name': 'Algeria',
        'slug': 'algeria',
        'key': 'dz',
        'reception': (
            "The Algerian funeral director takes custody at Houari Boumediene "
            "Airport Algiers (ALG) cargo terminal or the relevant regional "
            "airport. Civil registration is handled by the local Etat Civil "
            "(civil registry) in the commune. For Muslim remains, Islamic law "
            "procedures apply and prompt burial is expected. All foreign "
            "documents require certified Arabic translation; French-language "
            "documents are also widely understood in Algerian administrative "
            "practice. Algeria is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Algerian "
            "Embassy or Consulate in the country of origin is required. A "
            "hermetically sealed coffin is required for all air imports. "
            "(Algerian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Algerian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Algeria. Algeria "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. The Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Algerian funeral director takes custody at Houari Boumediene "
            "Airport Algiers (ALG) cargo terminal. The local Etat Civil (civil "
            "registry) in the commune registers the death. For Muslim remains, "
            "Islamic law procedures apply and prompt burial is expected. All "
            "foreign documents require certified Arabic translation. Algeria is "
            "not a Hague Apostille member; full consular authentication through "
            "the Algerian Embassy or Consulate in the origin country is required. "
            "A hermetically sealed coffin is required."
        ),
        'emergency_line': 'contact the Algerian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-algeria',
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
    'india': {
        'name': 'India',
        'emergency': '112 (unified) / 100 (police) / 108 (ambulance)',
        'registry': 'the local Registrar of Births and Deaths under the state civil registration system',
        'cert_name': 'death certificate',
        'cert_lang': 'English or regional language (varies by state)',
        'overview': (
            "Call 112 for emergency services, 100 for police, or 108 for ambulance. "
            "Death is certified by a physician. The death is registered with the "
            "local Registrar of Births and Deaths under the state civil registration "
            "system. Documentation language varies by state; English-language "
            "certificates are issued in most urban areas. Police take jurisdiction "
            "for violent or unexplained deaths. India is a Hague Apostille "
            "Convention member. Processing times vary by state; large cities "
            "process faster than rural areas. Tropical conditions in many regions "
            "require prompt embalming."
        ),
        'doc_time': '5-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '2-3 weeks',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': (
            "Cremation is widely available in India and is the traditional rite "
            "for Hindu and Sikh communities. Muslim remains require burial. "
            "A cremation certificate is required for export of ashes."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths',
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
}

ROUTES = [
    # R61 -- Nigeria wave 1
    {
        'origin': 'united-kingdom', 'dest': 'nigeria',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Nigeria include oil and gas sector professionals, "
            "development workers, NGO staff, and a community with bilateral ties "
            "built across decades of close UK-Nigeria relations within the "
            "Commonwealth. When a British national dies in Nigeria, the death must "
            "be registered with the relevant register office in England and Wales, "
            "Scotland, or Northern Ireland. The Nigerian High Commission in London "
            "can advise on documentation requirements for repatriation to Nigeria. "
            "Nigeria is not a member of the Hague Apostille Convention; full "
            "consular authentication is required. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'nigeria',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Nigeria include business professionals in the oil, "
            "gas, and technology sectors, NGO staff, and a community with bilateral "
            "ties reflecting the large Nigerian-American diaspora in the United "
            "States. The US Embassy in Abuja handles consular matters for US "
            "nationals in Nigeria. English-language US death certificates require "
            "authentication by the Nigerian Embassy in Washington DC. Nigeria is "
            "not a member of the Hague Apostille Convention; full consular "
            "authentication is required. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'nigeria',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Nigeria include development sector workers, NGO "
            "professionals, and business contacts in the energy and technology "
            "sectors. Germany and Nigeria maintain bilateral diplomatic relations "
            "and Germany is a significant development partner. German death "
            "certificates (Sterbeurkunde, in German) require certified English "
            "translation and authentication by the Nigerian Embassy in Berlin. "
            "Nigeria is not a member of the Hague Apostille Convention; full "
            "consular authentication is required. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'nigeria',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Nigeria include business professionals in the "
            "oil and energy sectors, development workers, and a small expat "
            "community. France and Nigeria maintain bilateral diplomatic relations, "
            "with France among Nigeria's European trading partners. French death "
            "certificates (acte de deces, in French) require certified English "
            "translation and authentication by the Nigerian Embassy in Paris. "
            "Nigeria is not a member of the Hague Apostille Convention; full "
            "consular authentication is required. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'nigeria',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Nigeria include business professionals and a "
            "small expat community. Italy and Nigeria maintain bilateral diplomatic "
            "relations, with Italian firms active in the Nigerian energy and "
            "construction sectors. Italian death certificates (atto di morte, in "
            "Italian) require certified English translation and authentication by "
            "the Nigerian Embassy in Rome. Nigeria is not a member of the Hague "
            "Apostille Convention; full consular authentication is required. "
            "(Nigerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R61 -- Kenya wave 1
    {
        'origin': 'united-kingdom', 'dest': 'kenya',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Kenya include a significant community with "
            "historical ties, retirees, NGO workers, development professionals, "
            "and business people in tourism and agriculture. The UK and Kenya "
            "maintain close bilateral relations as Commonwealth members. British "
            "death certificates are issued by the relevant register office and "
            "require authentication by the Kenyan High Commission in London. "
            "Kenya joined the Hague Apostille Convention in 2021; apostille "
            "certificates are accepted for UK-issued documents. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'kenya',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Kenya include development workers, NGO professionals, "
            "business people, and tourists. The US maintains a substantial "
            "development presence in Kenya through USAID programmes across health, "
            "agriculture, and governance. English-language US death certificates "
            "require authentication by the Kenyan Embassy in Washington DC. Kenya "
            "joined the Hague Apostille Convention in 2021; apostille certificates "
            "are accepted for US-issued documents. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'kenya',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Kenya include development workers, NGO "
            "professionals, researchers, and tourists visiting Kenyan national "
            "parks. Germany and Kenya maintain bilateral development cooperation. "
            "German death certificates (Sterbeurkunde, in German) require "
            "certified English translation and authentication by the Kenyan "
            "Embassy in Berlin. Kenya joined the Hague Apostille Convention in "
            "2021; apostille certificates are accepted for German documents. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'kenya',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Kenya include development workers, "
            "researchers, and tourists visiting Kenyan national parks and "
            "coastal areas. Australia and Kenya maintain bilateral diplomatic "
            "relations within Commonwealth frameworks. Australian death "
            "certificates (in English) require authentication by the Kenyan "
            "High Commission in Canberra. Kenya joined the Hague Apostille "
            "Convention in 2021; apostille certificates are accepted for "
            "Australian-issued documents. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'kenya',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Kenya include development workers, researchers, "
            "business professionals, and tourists visiting national parks and "
            "coastal resorts. France maintains bilateral development cooperation "
            "with Kenya. French death certificates (acte de deces, in French) "
            "require certified English translation and authentication by the "
            "Kenyan Embassy in Paris. Kenya joined the Hague Apostille Convention "
            "in 2021; apostille certificates are accepted for French documents. "
            "(Kenyan Ministry of Foreign Affairs and Diaspora Affairs, 2025.)"
        ),
    },
    # R61 -- Ghana wave 1
    {
        'origin': 'united-kingdom', 'dest': 'ghana',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Ghana include a community with historical ties, "
            "development workers, NGO staff, and business professionals. The UK "
            "and Ghana maintain close bilateral relations as Commonwealth members. "
            "British death certificates are issued by the relevant register office "
            "and require authentication by the Ghanaian High Commission in London. "
            "Ghana is not a member of the Hague Apostille Convention; full "
            "consular authentication is required. "
            "(Ghanaian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'ghana',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Ghana include development workers, academics, and "
            "a community with bilateral ties reflecting the large Ghanaian-American "
            "diaspora. The US maintains a development presence through USAID "
            "programmes in Ghana. English-language US death certificates require "
            "authentication by the Ghanaian Embassy in Washington DC. Ghana is "
            "not a Hague Apostille Convention member; full consular authentication "
            "is required. (Ghanaian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'ghana',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Ghana include development workers, NGO "
            "professionals, and business contacts. Germany and Ghana maintain "
            "bilateral development cooperation through GIZ (Deutsche Gesellschaft "
            "fuer Internationale Zusammenarbeit). German death certificates "
            "(Sterbeurkunde, in German) require certified English translation and "
            "authentication by the Ghanaian Embassy in Berlin. Ghana is not a "
            "Hague Apostille Convention member; full consular authentication is "
            "required. (Ghanaian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'ghana',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Ghana include business professionals and a "
            "small expat community. Italy and Ghana maintain bilateral diplomatic "
            "relations. Italian death certificates (atto di morte, in Italian) "
            "require certified English translation and authentication by the "
            "Ghanaian Embassy in Rome. Ghana is not a member of the Hague "
            "Apostille Convention; full consular authentication is required. "
            "(Ghanaian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'ghana',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in Ghana include development workers, NGO "
            "professionals, and business contacts. The Netherlands and Ghana "
            "maintain bilateral development cooperation. Dutch death certificates "
            "(akte van overlijden, in Dutch) require certified English translation "
            "and authentication by the Ghanaian Embassy in The Hague. Ghana is "
            "not a member of the Hague Apostille Convention; full consular "
            "authentication is required. "
            "(Ghanaian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R61 -- Nepal wave 1
    {
        'origin': 'united-kingdom', 'dest': 'nepal',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Nepal include trekkers, mountaineers, volunteers, "
            "development workers, and a community including British Gurkha veterans "
            "and their families. Nepal has a long historical connection with the "
            "United Kingdom through the Brigade of Gurkhas, with Gurkha settlement "
            "communities in garrison towns across the UK. British death certificates "
            "are issued by the relevant register office. The Nepalese Embassy in "
            "London can advise on documentation requirements for repatriation to "
            "Nepal. Nepal is not a member of the Hague Apostille Convention; full "
            "consular authentication is required. "
            "(Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'nepal',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Nepal include trekkers, mountaineers, volunteers, "
            "development workers, and a community including Nepali-American "
            "families. The US maintains bilateral development cooperation with "
            "Nepal. English-language US death certificates require authentication "
            "by the Nepalese Embassy in Washington DC. Nepal is not a member of "
            "the Hague Apostille Convention; full consular authentication is "
            "required. (Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'nepal',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Nepal include trekkers, mountaineers, development "
            "workers, and researchers. Germany and Nepal maintain bilateral "
            "development cooperation through GIZ programmes. German death "
            "certificates (Sterbeurkunde, in German) require certified Nepali "
            "or English translation and authentication by the Nepalese Embassy "
            "in Berlin. Nepal is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'india', 'dest': 'nepal',
        'embassy_city': 'New Delhi',
        'intro': (
            "Nepalese nationals in India include a large community of migrant "
            "workers, students, and professionals, reflecting the open border "
            "and deep bilateral ties between India and Nepal under the Treaty of "
            "Peace and Friendship (1950), which allows free movement of nationals "
            "between the two countries. Indian death certificates are issued by "
            "the local Registrar of Births and Deaths. Documentation requires "
            "certified Nepali translation where issued in a regional Indian "
            "language. Nepal is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'nepal',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Nepal include trekkers, mountaineers, "
            "volunteers, and development workers. Australia and Nepal maintain "
            "bilateral diplomatic relations. Australian death certificates "
            "(in English) require authentication by the Nepalese Embassy in "
            "Canberra. Nepal is not a member of the Hague Apostille Convention; "
            "full consular authentication is required. "
            "(Nepalese Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R61 -- Ethiopia wave 1
    {
        'origin': 'united-kingdom', 'dest': 'ethiopia',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Ethiopia include development workers, NGO "
            "professionals, diplomats, and a community with bilateral ties. The "
            "UK and Ethiopia maintain bilateral diplomatic relations, with the UK "
            "providing development assistance across health and food security "
            "programmes. British death certificates are issued by the relevant "
            "register office. The Ethiopian Embassy in London can advise on "
            "documentation requirements for repatriation to Ethiopia. Ethiopia "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication is required. "
            "(Ethiopian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'ethiopia',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Ethiopia include development workers, NGO "
            "professionals, diplomats, and a community including "
            "Ethiopian-American families. The US maintains a substantial "
            "development presence in Ethiopia through USAID. English-language "
            "US death certificates require authentication by the Ethiopian "
            "Embassy in Washington DC. Ethiopia is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(Ethiopian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'ethiopia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Ethiopia include development workers, NGO "
            "professionals, and researchers. Germany and Ethiopia maintain "
            "bilateral development cooperation through GIZ programmes. German "
            "death certificates (Sterbeurkunde, in German) require certified "
            "Amharic or English translation and authentication by the Ethiopian "
            "Embassy in Berlin. Ethiopia is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Ethiopian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'ethiopia',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Ethiopia include development workers, NGO "
            "professionals, and diplomats. France and Ethiopia maintain bilateral "
            "diplomatic relations, with France active in development cooperation "
            "in the region. French death certificates (acte de deces, in French) "
            "require certified Amharic or English translation and authentication "
            "by the Ethiopian Embassy in Paris. Ethiopia is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(Ethiopian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'ethiopia',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Ethiopia include development workers, business "
            "professionals, and a small community with historical ties reflecting "
            "the Italy-Ethiopia bilateral diplomatic relationship. Italy and "
            "Ethiopia maintain bilateral diplomatic relations. Italian death "
            "certificates (atto di morte, in Italian) require certified Amharic "
            "or English translation and authentication by the Ethiopian Embassy "
            "in Rome. Ethiopia is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(Ethiopian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R62 -- Brazil wave 1
    {
        'origin': 'united-kingdom', 'dest': 'brazil',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Brazil include business professionals, "
            "researchers, students, and individuals with bilateral ties including "
            "the large Brazilian community in the UK. Brazil and the UK maintain "
            "bilateral diplomatic relations. British death certificates require "
            "certified Portuguese translation for Brazilian civil registration. "
            "The Brazilian Embassy in London can advise on documentation "
            "requirements. Brazil is a member of the Hague Apostille Convention; "
            "apostille certificates are accepted for UK-issued documents. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'brazil',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Brazil include a significant community of business "
            "professionals, investors, and individuals with bilateral ties. Brazil "
            "and the United States are major bilateral economic partners. "
            "English-language US death certificates require certified Portuguese "
            "translation for Brazilian civil registration. The Brazilian Embassy "
            "in Washington DC can advise on documentation requirements. Brazil "
            "is a member of the Hague Apostille Convention; apostille certificates "
            "are accepted for US-issued documents. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'brazil',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Brazil include a significant community reflecting "
            "historical German migration to southern Brazil, as well as business "
            "professionals and investors. Brazil has a large German-heritage "
            "population, particularly in Rio Grande do Sul, Santa Catarina, and "
            "Parana states. German death certificates (Sterbeurkunde, in German) "
            "require certified Portuguese translation for Brazilian civil "
            "registration. Brazil is a member of the Hague Apostille Convention; "
            "apostille certificates are accepted for German documents. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'brazil',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Brazil include business professionals and a "
            "community with historical ties reflecting the long-standing "
            "Spain-Brazil bilateral relationship and shared Iberian heritage. "
            "Spanish death certificates (certificado de defuncion, in Spanish) "
            "require certified Portuguese translation for Brazilian civil "
            "registration. The Brazilian Embassy in Madrid can advise on "
            "documentation requirements. Brazil is a member of the Hague "
            "Apostille Convention; apostille certificates are accepted for "
            "Spanish-issued documents. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'brazil',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Brazil include a community reflecting significant "
            "historical Italian migration to Brazil, particularly to Sao Paulo "
            "state, as well as business professionals. Brazil has one of the "
            "largest Italian-heritage populations outside Italy. Italian death "
            "certificates (atto di morte, in Italian) require certified Portuguese "
            "translation for Brazilian civil registration. Brazil is a member of "
            "the Hague Apostille Convention; apostille certificates are accepted "
            "for Italian documents. "
            "(Brazilian Ministry of Foreign Affairs, Itamaraty, 2025.)"
        ),
    },
    # R62 -- Mexico wave 1
    {
        'origin': 'united-kingdom', 'dest': 'mexico',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Mexico include tourists, retirees, business "
            "professionals, and a small expat community. Mexico and the UK "
            "maintain bilateral diplomatic relations. British death certificates "
            "require certified Spanish translation for Mexican civil registration. "
            "The Mexican Embassy in London can advise on documentation requirements. "
            "Mexico is a member of the Hague Apostille Convention; apostille "
            "certificates are accepted for UK-issued documents. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'mexico',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Mexico include one of the largest expat communities "
            "globally, comprising retirees, business professionals, dual nationals, "
            "and tourists. Mexico and the United States share a long bilateral "
            "relationship within the Canada-United States-Mexico Agreement (CUSMA). "
            "English-language US death certificates require certified Spanish "
            "translation for Mexican civil registration. Mexico is a member of "
            "the Hague Apostille Convention; apostille certificates are accepted "
            "for US-issued documents. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'mexico',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Mexico include business professionals, "
            "researchers, and tourists. Germany and Mexico maintain bilateral "
            "diplomatic relations, with Germany among Mexico's European trading "
            "partners. German death certificates (Sterbeurkunde, in German) "
            "require certified Spanish translation for Mexican civil registration. "
            "Mexico is a member of the Hague Apostille Convention; apostille "
            "certificates are accepted for German documents. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'mexico',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Mexico include business professionals, academics, "
            "and a community with close cultural and linguistic ties. Mexico and "
            "Spain share language and deep cultural heritage. Spanish death "
            "certificates (certificado de defuncion, in Spanish) are accepted "
            "directly in Mexico. Mexico is a member of the Hague Apostille "
            "Convention; apostille certificates are accepted for Spanish documents. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'mexico',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in Mexico include retirees, snowbirds, business "
            "professionals, and tourists. Canada is one of Mexico's most "
            "significant bilateral partners within the Canada-United "
            "States-Mexico Agreement (CUSMA). Canadian death certificates "
            "(in English or French) require certified Spanish translation for "
            "Mexican civil registration. Mexico is a member of the Hague "
            "Apostille Convention; apostille certificates are accepted for "
            "Canadian-issued documents. "
            "(Mexican Secretariat of Foreign Affairs, SRE, 2025.)"
        ),
    },
    # R62 -- Colombia wave 1
    {
        'origin': 'united-kingdom', 'dest': 'colombia',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Colombia include business professionals, "
            "tourists, English-language teachers, and development workers. The "
            "UK and Colombia maintain bilateral diplomatic relations. British "
            "death certificates require certified Spanish translation for "
            "Colombian civil registration. The Colombian Embassy in London can "
            "advise on documentation requirements. Colombia is a member of the "
            "Hague Apostille Convention; apostille certificates are accepted for "
            "UK-issued documents. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'colombia',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Colombia include business professionals, dual "
            "nationals, retirees, and tourists, reflecting the large "
            "Colombian-American community and close bilateral relations. "
            "English-language US death certificates require certified Spanish "
            "translation for Colombian civil registration. Colombia is a member "
            "of the Hague Apostille Convention; apostille certificates are "
            "accepted for US-issued documents. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'colombia',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Colombia include business professionals, "
            "academics, and a community with close cultural and linguistic ties. "
            "Colombia and Spain maintain bilateral diplomatic and cultural "
            "relations, with Spain among Colombia's most significant bilateral "
            "partners. Spanish death certificates (certificado de defuncion) "
            "are accepted directly in Colombia. Colombia is a Hague Apostille "
            "Convention member; apostille certificates are accepted for Spanish "
            "documents. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'colombia',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Colombia include development workers, business "
            "professionals, and researchers. Germany and Colombia maintain "
            "bilateral diplomatic relations and development cooperation. German "
            "death certificates (Sterbeurkunde, in German) require certified "
            "Spanish translation for Colombian civil registration. Colombia is "
            "a Hague Apostille Convention member; apostille certificates are "
            "accepted for German-issued documents. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'colombia',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Colombia include business professionals and a "
            "community with bilateral ties. Italy and Colombia maintain bilateral "
            "diplomatic relations. Italian death certificates (atto di morte, in "
            "Italian) require certified Spanish translation for Colombian civil "
            "registration. Colombia is a Hague Apostille Convention member; "
            "apostille certificates are accepted for Italian-issued documents. "
            "(Colombian Ministry of Foreign Affairs, Cancilleria, 2025.)"
        ),
    },
    # R62 -- Argentina wave 1
    {
        'origin': 'united-kingdom', 'dest': 'argentina',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Argentina include a significant community with "
            "historical ties, business professionals, and individuals with "
            "bilateral family connections. Argentina has a long-established "
            "Anglo-Argentine community. British death certificates require "
            "certified Spanish translation for Argentine civil registration. "
            "The Argentine Embassy in London can advise on documentation "
            "requirements. Argentina is a member of the Hague Apostille "
            "Convention; apostille certificates are accepted for UK-issued "
            "documents. (Argentine Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'argentina',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Argentina include business professionals, students, "
            "dual nationals, and tourists. Argentina and the United States "
            "maintain bilateral diplomatic relations. English-language US death "
            "certificates require certified Spanish translation for Argentine "
            "civil registration. Argentina is a member of the Hague Apostille "
            "Convention; apostille certificates are accepted for US-issued "
            "documents. (Argentine Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'argentina',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Argentina include a significant community "
            "reflecting historical Spanish migration to Argentina from the late "
            "nineteenth and early twentieth centuries. Argentina has a large "
            "Spanish-heritage population. Spanish death certificates (certificado "
            "de defuncion, in Spanish) are accepted directly in Argentina. "
            "Argentina is a member of the Hague Apostille Convention; apostille "
            "certificates are accepted for Spanish documents. "
            "(Argentine Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'argentina',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Argentina include a community reflecting "
            "significant historical Italian migration to Argentina, with Argentina "
            "having one of the largest Italian-heritage populations outside Italy. "
            "Italian death certificates (atto di morte, in Italian) require "
            "certified Spanish translation for Argentine civil registration. "
            "Argentina is a Hague Apostille Convention member; apostille "
            "certificates are accepted for Italian documents. "
            "(Argentine Cancilleria, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'argentina',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Argentina include business professionals and a "
            "community with historical ties, including German-Argentine communities "
            "in Buenos Aires and Patagonia. German death certificates (Sterbeurkunde, "
            "in German) require certified Spanish translation for Argentine civil "
            "registration. Argentina is a member of the Hague Apostille Convention; "
            "apostille certificates are accepted for German documents. "
            "(Argentine Cancilleria, 2025.)"
        ),
    },
    # R62 -- Algeria wave 1
    {
        'origin': 'france', 'dest': 'algeria',
        'embassy_city': 'Paris',
        'intro': (
            "Algerian nationals in France form one of the largest diaspora "
            "communities in France, reflecting deep historical and cultural ties "
            "from the French colonial period (1830 to 1962) and subsequent "
            "migration. France has the largest Algerian diaspora outside Algeria. "
            "French death certificates (acte de deces, in French) are widely "
            "understood in Algerian administrative practice; Arabic translation "
            "may be required for formal registration. Algeria is not a member "
            "of the Hague Apostille Convention; full consular authentication "
            "through the Algerian Embassy in Paris is required. "
            "(Algerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'algeria',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Algeria include business professionals and a "
            "small community with bilateral ties. Algeria and Spain maintain "
            "bilateral relations as neighbouring Mediterranean states, with Spain "
            "among Algeria's significant European trading partners. Spanish death "
            "certificates (certificado de defuncion, in Spanish) require certified "
            "Arabic translation and authentication by the Algerian Embassy in "
            "Madrid. Algeria is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(Algerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'algeria',
        'embassy_city': 'Brussels',
        'intro': (
            "Belgian nationals in Algeria include business professionals, "
            "particularly in the energy sector, and a community with bilateral "
            "ties through Belgium's Algerian diaspora. Belgium has a significant "
            "Algerian community reflecting post-war migration patterns. Belgian "
            "death certificates (in French or Dutch depending on region) require "
            "certified Arabic translation and authentication by the Algerian "
            "Embassy in Brussels. Algeria is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Algerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'algeria',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in Algeria include business professionals, "
            "particularly in the energy and construction sectors. The Netherlands "
            "and Algeria maintain bilateral economic relations, with Dutch firms "
            "active in Algerian infrastructure. Dutch death certificates (akte "
            "van overlijden, in Dutch) require certified Arabic translation and "
            "authentication by the Algerian Embassy in The Hague. Algeria is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. (Algerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'algeria',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Algeria include business professionals in the "
            "energy, construction, and manufacturing sectors. Germany and Algeria "
            "maintain bilateral economic relations, with Germany among Algeria's "
            "significant European trading partners. German death certificates "
            "(Sterbeurkunde, in German) require certified Arabic translation and "
            "authentication by the Algerian Embassy in Berlin. Algeria is not a "
            "Hague Apostille Convention member; full consular authentication is "
            "required. (Algerian Ministry of Foreign Affairs, 2025.)"
        ),
    },
]


def make_dest_key(dest_slug):
    keys = {
        'nigeria': 'ng', 'kenya': 'ke', 'ghana': 'gh', 'nepal': 'np',
        'ethiopia': 'et', 'brazil': 'br', 'mexico': 'mx', 'colombia': 'co',
        'argentina': 'ar', 'algeria': 'dz',
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
