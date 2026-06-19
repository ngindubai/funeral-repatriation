#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R65-R66.

   R65 (25 routes, variants B,C,D,E,A x5):
     Cuba x5:      united-kingdom, united-states, spain, canada, germany
     Venezuela x5: united-states, spain, united-kingdom, germany, italy
     Iran x5:      united-kingdom, united-states, germany, france, australia
     Zimbabwe x5:  united-kingdom, united-states, germany, australia, france
     Uganda x5:    united-kingdom, united-states, germany, australia, netherlands

   R66 (25 routes, variants B,C,D,E,A x5):
     Ivory Coast x5:  france, united-kingdom, belgium, germany, united-states
     DRC x5:          france, belgium, united-kingdom, united-states, germany
     Afghanistan x5:  united-kingdom, united-states, germany, australia, canada
     Libya x5:        united-kingdom, united-states, italy, germany, france
     Tunisia x5:      france, united-kingdom, germany, italy, belgium

   Template rotation: R64 ended A (index 0). R65 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R66 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'cuba': {
        'name': 'Cuba',
        'slug': 'cuba',
        'key': 'cu',
        'reception': (
            "The Cuban funeral director takes custody at Havana Jose Marti "
            "International Airport (HAV) cargo terminal, or the relevant "
            "regional airport. Death registration is handled by the local "
            "Registro del Estado Civil (civil status registry). Death "
            "certificates are issued in Spanish. Cuban authorities require "
            "all foreign-language documents to be accompanied by a certified "
            "Spanish translation approved by a Cuban sworn translator. Cuba "
            "is not a member of the Hague Apostille Convention; full consular "
            "authentication through the Cuban Embassy or Consulate in the "
            "country of origin is required. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "Cuban airline regulations and import procedures may add "
            "coordination steps; a specialist with current Cuba contacts "
            "is recommended. "
            "(Cuban Ministry of Foreign Affairs (MINREX), 2025; FCDO Travel "
            "Advice: Cuba, 2025.)"
        ),
        'consular_template': (
            "Cuban Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Cuba. Cuba is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Cuban funeral director takes custody at Havana Jose Marti "
            "International Airport (HAV) cargo terminal. The local Registro "
            "del Estado Civil registers the death; certificates are issued "
            "in Spanish. Cuba is not a Hague Apostille member; full consular "
            "authentication through the Cuban Embassy in the origin country "
            "is required. All foreign documents require certified Spanish "
            "translation by a Cuban-approved translator. An embalming "
            "certificate and hermetically sealed coffin are required. "
            "A specialist with current Cuba airline and cargo contacts "
            "is recommended."
        ),
        'emergency_line': 'contact the Cuban Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-cuba',
    },
    'venezuela': {
        'name': 'Venezuela',
        'slug': 'venezuela',
        'key': 've',
        'reception': (
            "The Venezuelan funeral director takes custody at Simon Bolivar "
            "International Airport Caracas (CCS) cargo terminal, or the "
            "relevant regional airport. Death registration is handled by the "
            "local Registro Civil (civil status office) under the Consejo "
            "Nacional Electoral. Death certificates are issued in Spanish. "
            "Venezuela acceded to the Hague Apostille Convention in November "
            "2023; apostille certificates from member states are now accepted "
            "for documents issued by signatory countries. All other foreign "
            "documents require certified Spanish translation and full consular "
            "authentication through the Venezuelan Embassy or Consulate in "
            "the country of origin. Families should verify current airline "
            "routes before arranging repatriation, as commercial aviation "
            "connections have been subject to change. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports. "
            "(Venezuelan Ministry of Foreign Affairs, 2025; Hague Conference "
            "on Private International Law, 2025.)"
        ),
        'consular_template': (
            "Venezuelan Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Venezuela. "
            "Venezuela joined the Hague Apostille Convention in November 2023. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Venezuelan funeral director takes custody at Simon Bolivar "
            "International Airport Caracas (CCS) cargo terminal. The local "
            "Registro Civil registers the death; certificates are issued in "
            "Spanish. Venezuela joined the Hague Apostille Convention in "
            "November 2023; apostille certificates from member states are "
            "accepted. All other documents require certified Spanish translation "
            "and full consular authentication through the Venezuelan Embassy "
            "in the origin country. Families should verify current airline "
            "routes before proceeding. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Venezuelan Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-venezuela',
    },
    'iran': {
        'name': 'Iran',
        'slug': 'iran',
        'key': 'ir',
        'reception': (
            "The Iranian funeral director takes custody at Tehran Imam Khomeini "
            "International Airport (IKA) or Mehrabad International Airport (THR) "
            "cargo terminal, depending on the airline routing. Death registration "
            "is handled by the National Organization for Civil Registration "
            "(NOCR, Sazman-e Sabt-e Ahval-e Keshvar). Death certificates are "
            "issued in Farsi (Persian). Iran is not a member of the Hague "
            "Apostille Convention; full consular authentication through the "
            "Iranian Embassy or Consulate in the country of origin is required. "
            "All foreign documents require certified Farsi translation. For "
            "Muslim remains, Islamic law procedures apply and prompt burial is "
            "expected. The Swiss Embassy in Tehran acts as a protecting power "
            "for British interests; the British Embassy in Tehran has not been "
            "operational since 2011. Families with UK or US connections should "
            "contact the FCDO or US State Department for current guidance. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(FCDO Travel Advice: Iran, 2025; Iranian NOCR, 2025.)"
        ),
        'consular_template': (
            "Iranian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Iran. Iran is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Iranian funeral director takes custody at Tehran Imam Khomeini "
            "International Airport (IKA) or Mehrabad International Airport (THR) "
            "cargo terminal. The National Organization for Civil Registration "
            "(NOCR) registers the death; certificates are issued in Farsi. "
            "Iran is not a Hague Apostille member; full consular authentication "
            "through the Iranian Embassy in the origin country is required. "
            "All foreign documents require certified Farsi translation. For "
            "Muslim remains, Islamic law procedures apply and prompt burial is "
            "expected. The British Embassy in Tehran has not been operational "
            "since 2011; Swiss Embassy acts as protecting power for UK interests. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Iranian Embassy or Consulate in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-iran',
    },
    'zimbabwe': {
        'name': 'Zimbabwe',
        'slug': 'zimbabwe',
        'key': 'zw',
        'reception': (
            "The Zimbabwean funeral director takes custody at Robert Gabriel "
            "Mugabe International Airport Harare (HRE) cargo terminal, or "
            "Joshua Mqabuko Nkomo International Airport Bulawayo (BUQ) for "
            "western Zimbabwe. Death registration is handled by the Registrar "
            "General of Zimbabwe. Death certificates are issued in English, "
            "one of Zimbabwe's official languages. Zimbabwe is a member of the "
            "Hague Apostille Convention; apostille certificates are accepted "
            "for documents issued by member states. Foreign documents in "
            "languages other than English require certified translation. An "
            "embalming certificate and hermetically sealed coffin are required "
            "for all air imports. "
            "(Zimbabwe Ministry of Home Affairs, Registrar General Department, "
            "2025; FCDO Travel Advice: Zimbabwe, 2025.)"
        ),
        'consular_template': (
            "Zimbabwean Embassy or High Commission in {city} can advise on "
            "documentation requirements for repatriation to Zimbabwe. Zimbabwe "
            "is a Hague Apostille Convention member. The High Commission cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Zimbabwean funeral director takes custody at Robert Gabriel "
            "Mugabe International Airport Harare (HRE) or Joshua Mqabuko "
            "Nkomo International Airport Bulawayo (BUQ) cargo terminal. The "
            "Registrar General of Zimbabwe registers the death; certificates "
            "are issued in English. Zimbabwe is a Hague Apostille Convention "
            "member; apostille certificates from member states are accepted. "
            "Foreign documents in other languages require certified translation. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Zimbabwean Embassy or High Commission in the origin country',
        'hub_url': 'repatriation-from-zimbabwe',
    },
    'uganda': {
        'name': 'Uganda',
        'slug': 'uganda',
        'key': 'ug',
        'reception': (
            "The Ugandan funeral director takes custody at Entebbe International "
            "Airport (EBB) cargo terminal. Death registration is handled by the "
            "Uganda Registration Services Bureau (URSB). Death certificates are "
            "issued in English, the official language of Uganda. Uganda is not "
            "a member of the Hague Apostille Convention; full consular "
            "authentication through the Ugandan High Commission or Embassy in "
            "the country of origin is required. For Muslim remains, which account "
            "for approximately one third of Uganda's population, Islamic law "
            "procedures apply and prompt burial is expected. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(Uganda Registration Services Bureau (URSB), 2025; FCDO Travel "
            "Advice: Uganda, 2025.)"
        ),
        'consular_template': (
            "Ugandan High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Uganda. Uganda is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. The High Commission cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Ugandan funeral director takes custody at Entebbe International "
            "Airport (EBB) cargo terminal. The Uganda Registration Services "
            "Bureau (URSB) registers the death and issues a death certificate "
            "in English. Uganda is not a Hague Apostille member; full consular "
            "authentication through the Ugandan High Commission or Embassy in "
            "the origin country is required. For Muslim remains, Islamic law "
            "procedures apply and prompt burial is expected. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Ugandan High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-uganda',
    },
    'ivory-coast': {
        'name': "Ivory Coast",
        'slug': 'ivory-coast',
        'key': 'ci',
        'reception': (
            "The Ivorian funeral director takes custody at Felix "
            "Houphouet-Boigny International Airport Abidjan (ABJ) cargo "
            "terminal. Death registration is handled by the local Centre "
            "d'Etat Civil at commune level. Death certificates (actes de "
            "deces) are issued in French, the official language. For Muslim "
            "remains, which account for approximately 40 percent of Ivory "
            "Coast's population, Islamic law procedures apply and prompt "
            "burial is expected. Ivory Coast is not a member of the Hague "
            "Apostille Convention; full consular authentication through the "
            "Ivorian Embassy or Consulate in the country of origin is "
            "required. All foreign-language documents require certified French "
            "translation. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(Ivorian Ministry of Foreign Affairs, 2025; FCDO Travel Advice: "
            "Ivory Coast, 2025.)"
        ),
        'consular_template': (
            "Ivorian Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Ivory Coast. Ivory Coast is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Ivorian funeral director takes custody at Felix "
            "Houphouet-Boigny International Airport Abidjan (ABJ) cargo "
            "terminal. The local Centre d'Etat Civil at commune level "
            "registers the death and issues an acte de deces in French. "
            "Ivory Coast is not a Hague Apostille member; full consular "
            "authentication through the Ivorian Embassy in the origin "
            "country is required. For Muslim remains, Islamic law procedures "
            "apply and prompt burial is expected. All foreign-language "
            "documents require certified French translation. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Ivorian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-ivory-coast',
    },
    'democratic-republic-of-the-congo': {
        'name': 'the Democratic Republic of the Congo',
        'slug': 'democratic-republic-of-the-congo',
        'key': 'cd',
        'reception': (
            "The Congolese funeral director takes custody at N'Djili "
            "International Airport Kinshasa (FIH) cargo terminal, or "
            "Lubumbashi International Airport (FBM) for the Katanga region. "
            "Death registration is handled by the Office National de l'Etat "
            "Civil (ONEC) at commune level. Death certificates (actes de "
            "deces) are issued in French, the official language. The "
            "Democratic Republic of the Congo is not a member of the Hague "
            "Apostille Convention; full consular authentication through the "
            "DRC Embassy or Consulate in the country of origin is required. "
            "All foreign-language documents require certified French "
            "translation. The FCDO advises against all travel to certain "
            "eastern DRC provinces; families should verify current airline "
            "routes and confirm consular access before proceeding. An "
            "embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(DRC Ministry of Foreign Affairs, 2025; FCDO Travel Advice: "
            "Democratic Republic of the Congo, 2025.)"
        ),
        'consular_template': (
            "DRC Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to the Democratic Republic of "
            "the Congo. The DRC is not a Hague Apostille Convention member; "
            "full consular authentication is required. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Congolese funeral director takes custody at N'Djili "
            "International Airport Kinshasa (FIH) or Lubumbashi "
            "International Airport (FBM) cargo terminal. The Office "
            "National de l'Etat Civil (ONEC) at commune level registers "
            "the death and issues an acte de deces in French. The DRC "
            "is not a Hague Apostille member; full consular authentication "
            "through the DRC Embassy in the origin country is required. "
            "The FCDO advises against all travel to certain eastern DRC "
            "provinces; families should verify current conditions. An "
            "embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the DRC Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-democratic-republic-of-the-congo',
    },
    'afghanistan': {
        'name': 'Afghanistan',
        'slug': 'afghanistan',
        'key': 'af',
        'reception': (
            "The funeral director or family representative takes custody at "
            "Hamid Karzai International Airport Kabul (KBL) cargo terminal. "
            "Death registration is handled by local authorities under "
            "Taliban-administered procedures, which differ significantly "
            "from pre-August 2021 civil registration systems. Death "
            "certificates are issued in Dari or Pashto, the two official "
            "languages. Afghanistan is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Afghan "
            "Embassy or Consulate in the country of origin is required "
            "where such representation exists. The FCDO advises against "
            "all travel to Afghanistan. All Western embassies in Kabul "
            "suspended operations in August 2021; Afghan consular matters "
            "in the UK are handled through the Afghan Charge d'Affaires "
            "in London. All foreign documents require certified Dari or "
            "Pashto translation. Repatriation to Afghanistan requires a "
            "specialist with current operational contacts. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(FCDO Travel Advice: Afghanistan, 2025.)"
        ),
        'consular_template': (
            "The Afghan Charge d'Affaires or relevant authority in {city} "
            "can advise on current documentation requirements for repatriation "
            "to Afghanistan. Afghanistan is not a Hague Apostille Convention "
            "member; full consular authentication is required where available. "
            "The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "Repatriation to Afghanistan requires coordination with a "
            "specialist who maintains current operational contacts, as all "
            "Western embassies in Kabul suspended operations in August 2021. "
            "The funeral director or family representative takes custody at "
            "Hamid Karzai International Airport Kabul (KBL). Death registration "
            "is handled by local Taliban-administered authorities; certificates "
            "are issued in Dari or Pashto. Afghanistan is not a Hague "
            "Apostille member. All foreign documents require certified "
            "translation. The FCDO advises against all travel to Afghanistan. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the FCDO on +44 (0)20 7008 5000 for current Afghanistan guidance',
        'hub_url': 'repatriation-from-afghanistan',
    },
    'libya': {
        'name': 'Libya',
        'slug': 'libya',
        'key': 'ly',
        'reception': (
            "The Libyan funeral director takes custody at Mitiga International "
            "Airport Tripoli (MJI) cargo terminal or Benina International "
            "Airport Benghazi (BEN) cargo terminal, depending on the "
            "destination region. Death registration is handled by the "
            "National Centre for Civil Registration and Statistics (NCCS) "
            "at municipality level. Death certificates are issued in "
            "Arabic. Libya is not a member of the Hague Apostille "
            "Convention; full consular authentication through the Libyan "
            "Embassy or Consulate in the country of origin is required. "
            "All foreign documents require certified Arabic translation. "
            "The FCDO advises against all travel to Libya. The British "
            "Embassy in Tripoli suspended operations in 2014; FCDO "
            "assistance for British nationals in Libya is provided through "
            "the British Embassy in Tunis. Families must engage a "
            "specialist with current Libya contacts. For Muslim remains, "
            "which account for the large majority of Libya's population, "
            "Islamic law procedures apply and prompt burial is expected. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(FCDO Travel Advice: Libya, 2025.)"
        ),
        'consular_template': (
            "Libyan Embassy or Consulate in {city} can advise on documentation "
            "requirements for repatriation to Libya. Libya is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. The Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Libyan funeral director takes custody at Mitiga International "
            "Airport Tripoli (MJI) or Benina International Airport Benghazi "
            "(BEN) cargo terminal. The National Centre for Civil Registration "
            "and Statistics (NCCS) registers the death; certificates are "
            "issued in Arabic. Libya is not a Hague Apostille member; full "
            "consular authentication through the Libyan Embassy in the "
            "origin country is required. The FCDO advises against all travel "
            "to Libya; British nationals should contact the FCDO for current "
            "consular assistance. For Muslim remains, Islamic law procedures "
            "apply and prompt burial is expected. An embalming certificate "
            "and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Libyan Embassy in the origin country, or the FCDO on +44 (0)20 7008 5000 for British nationals',
        'hub_url': 'repatriation-from-libya',
    },
    'tunisia': {
        'name': 'Tunisia',
        'slug': 'tunisia',
        'key': 'tn',
        'reception': (
            "The Tunisian funeral director takes custody at Tunis-Carthage "
            "International Airport (TUN) cargo terminal, or Monastir Habib "
            "Bourguiba International Airport (MIR) for tourists in the "
            "coastal region. Death registration is handled by the local "
            "commune (municipalite) civil registry, the Bureau de l'Etat "
            "Civil. Death certificates (actes de deces) are issued in "
            "Arabic, the official language, with French widely used in "
            "Tunisian administrative practice. For Muslim remains, which "
            "account for the large majority of Tunisia's population, "
            "Islamic law procedures apply and prompt burial is expected. "
            "Tunisia is not a member of the Hague Apostille Convention; "
            "full consular authentication through the Tunisian Embassy or "
            "Consulate in the country of origin is required. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Tunisian Ministry of Foreign Affairs, 2025; FCDO Travel "
            "Advice: Tunisia, 2025.)"
        ),
        'consular_template': (
            "Tunisian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Tunisia. "
            "Tunisia is not a Hague Apostille Convention member; full "
            "consular authentication is required. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Tunisian funeral director takes custody at Tunis-Carthage "
            "International Airport (TUN) or Monastir Habib Bourguiba "
            "International Airport (MIR) cargo terminal. The local commune "
            "civil registry (Bureau de l'Etat Civil) registers the death "
            "and issues an acte de deces in Arabic, with French widely "
            "accepted in practice. For Muslim remains, Islamic law "
            "procedures apply and prompt burial is expected. Tunisia is "
            "not a Hague Apostille member; full consular authentication "
            "through the Tunisian Embassy in the origin country is "
            "required. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Tunisian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-tunisia',
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
}

ROUTES = [
    # R65 -- Cuba x5
    {
        'origin': 'united-kingdom', 'dest': 'cuba',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Cuba include tourists, business contacts, "
            "and individuals with bilateral connections. Cuba has a significant "
            "British visitor presence, particularly in Havana and the resort "
            "regions. The British Embassy in Havana assists British nationals "
            "in Cuba with registration of death and document guidance. British "
            "death certificates require certified Spanish translation and "
            "authentication by the Cuban Embassy in London. Cuba is not a "
            "member of the Hague Apostille Convention; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Cuba, 2025; Cuban Ministry of Foreign "
            "Affairs (MINREX), 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'cuba',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Cuba include tourists, academics, journalists, "
            "and Cuban-Americans visiting family. US-Cuba diplomatic relations "
            "were restored in 2015 and the US Embassy in Havana reopened; "
            "families should contact the US Embassy in Havana directly after "
            "a death. English-language US death certificates require certified "
            "Spanish translation and authentication by the Cuban Embassy in "
            "Washington DC. Cuba is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(US Embassy Havana, 2025; Cuban Ministry of Foreign Affairs "
            "(MINREX), 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'cuba',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Cuba include business professionals, "
            "academics, and individuals with deep historical and cultural "
            "ties reflecting the Spain-Cuba relationship. Spain is one of "
            "Cuba's largest trading partners. Spanish death certificates "
            "(certificado de defuncion) are accepted directly in Cuba without "
            "translation, given the shared language. Authentication by the "
            "Cuban Embassy in Madrid is required. Cuba is not a Hague "
            "Apostille Convention member; full consular authentication "
            "is required. "
            "(Cuban Ministry of Foreign Affairs (MINREX), 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'cuba',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canadian nationals in Cuba include tourists, business "
            "professionals, and a community with bilateral ties reflecting "
            "the long-standing Canada-Cuba relationship. Canada maintains "
            "an embassy in Havana and has historically had one of the "
            "stronger Western diplomatic presences in Cuba. Canadian death "
            "certificates (in English or French) require certified Spanish "
            "translation and authentication by the Cuban Embassy in Ottawa. "
            "Cuba is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(Canadian Embassy Havana, 2025; Cuban Ministry of Foreign "
            "Affairs (MINREX), 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'cuba',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Cuba include tourists and business "
            "professionals. Germany and Cuba maintain bilateral diplomatic "
            "relations. German death certificates (Sterbeurkunde, in German) "
            "require certified Spanish translation and authentication by the "
            "Cuban Embassy in Berlin. Cuba is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "The German Embassy in Havana can assist German nationals "
            "with consular matters after a death. "
            "(Cuban Ministry of Foreign Affairs (MINREX), 2025.)"
        ),
    },
    # R65 -- Venezuela x5
    {
        'origin': 'united-states', 'dest': 'venezuela',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Venezuela include business professionals and "
            "a community with bilateral ties, though the US closed its "
            "embassy in Caracas in March 2019. Consular assistance for US "
            "nationals in Venezuela is provided by the Swiss Embassy in "
            "Caracas as the protecting power. English-language US death "
            "certificates require certified Spanish translation and "
            "authentication by the Venezuelan Embassy in Washington DC. "
            "Venezuela joined the Hague Apostille Convention in November "
            "2023; apostille certificates are now accepted. Families "
            "should verify current airline routes before arranging "
            "repatriation. "
            "(US State Department, 2025; Venezuelan Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'venezuela',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals in Venezuela include a long-established "
            "community with deep historical, cultural, and bilateral ties. "
            "Spain and Venezuela maintain diplomatic relations and the "
            "Spanish Embassy in Caracas remains operational. Spanish death "
            "certificates (certificado de defuncion) are accepted directly "
            "in Venezuela without translation, given the shared language. "
            "Venezuela joined the Hague Apostille Convention in November "
            "2023; apostille certificates from Spain are now accepted. "
            "Families should verify current airline routes. "
            "(Venezuelan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'venezuela',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Venezuela include business professionals "
            "and individuals with bilateral connections. The British Embassy "
            "in Caracas handles consular matters for British nationals in "
            "Venezuela. British death certificates require certified Spanish "
            "translation and authentication by the Venezuelan Embassy in "
            "London. Venezuela joined the Hague Apostille Convention in "
            "November 2023; apostille certificates are now accepted for "
            "UK-issued documents. Families should verify current airline "
            "routes and consular access before proceeding. "
            "(FCDO Travel Advice: Venezuela, 2025; Venezuelan Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'venezuela',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Venezuela include business professionals "
            "and a community with bilateral ties reflecting German migration "
            "to Venezuela in the mid-twentieth century. Germany and Venezuela "
            "maintain bilateral diplomatic relations. German death certificates "
            "(Sterbeurkunde, in German) require certified Spanish translation "
            "and authentication by the Venezuelan Embassy in Berlin. Venezuela "
            "joined the Hague Apostille Convention in November 2023; apostille "
            "certificates are now accepted for German documents. "
            "(Venezuelan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'venezuela',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Venezuela include a long-established "
            "community reflecting significant Italian migration to Venezuela "
            "from the 1940s to 1970s. Italy and Venezuela maintain bilateral "
            "diplomatic relations and the Italian Embassy in Caracas remains "
            "operational. Italian death certificates (atto di morte, in Italian) "
            "require certified Spanish translation and authentication by the "
            "Venezuelan Embassy in Rome. Venezuela joined the Hague Apostille "
            "Convention in November 2023; apostille certificates are now accepted "
            "for Italian documents. "
            "(Venezuelan Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R65 -- Iran x5
    {
        'origin': 'united-kingdom', 'dest': 'iran',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Iran include dual nationals, academics, "
            "journalists, and individuals with family ties. The British Embassy "
            "in Tehran has not been operational since 2011; consular assistance "
            "for British nationals in Iran is provided by the Swedish Embassy "
            "in Tehran as the protecting power. Families should contact the "
            "FCDO on +44 (0)20 7008 5000 immediately after a death. British "
            "death certificates require certified Farsi translation and "
            "authentication by the Iranian Embassy in London. Iran is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. The FCDO advises against all travel to Iran. "
            "(FCDO Travel Advice: Iran, 2025; Iranian Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'iran',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Iran include Iranian-Americans visiting family "
            "and dual nationals. The United States has no embassy in Tehran; "
            "consular assistance for US nationals in Iran is provided by the "
            "Swiss Embassy in Tehran as the protecting power. Families should "
            "contact the US State Department on +1 888 407 4747 immediately "
            "after a death. English-language US death certificates require "
            "certified Farsi translation and authentication by the Iranian "
            "Interests Section (via the Pakistani Embassy) in Washington DC. "
            "Iran is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(US State Department, 2025; Iranian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'iran',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Iran include business professionals, academics, "
            "and individuals with bilateral ties reflecting Germany's historical "
            "trade relationship with Iran. The German Embassy in Tehran remains "
            "operational; families should contact it immediately after a death. "
            "German death certificates (Sterbeurkunde, in German) require certified "
            "Farsi translation and authentication by the Iranian Embassy in Berlin. "
            "Iran is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(Iranian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'iran',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Iran include business professionals, academics, "
            "and individuals with bilateral ties. The French Embassy in Tehran "
            "remains operational; families should contact it immediately after "
            "a death. French death certificates (acte de deces, in French) "
            "require certified Farsi translation and authentication by the "
            "Iranian Embassy in Paris. Iran is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Iranian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'iran',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Iran include dual nationals visiting "
            "family and individuals with bilateral ties. The Australian Embassy "
            "in Tehran was suspended in 2012; Australian nationals requiring "
            "consular assistance in Iran should contact the Australian "
            "Department of Foreign Affairs and Trade (DFAT) on 1300 555 135 "
            "(from Australia) or +61 2 6261 3305 (from overseas). Australian "
            "death certificates require certified Farsi translation and "
            "authentication by the Iranian Embassy in Canberra. Iran is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(DFAT Smartraveller: Iran, 2025; Iranian Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    # R65 -- Zimbabwe x5
    {
        'origin': 'united-kingdom', 'dest': 'zimbabwe',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Zimbabwe include a long-established community "
            "with deep historical ties, NGO workers, development professionals, "
            "and tourists visiting Victoria Falls and national parks. The UK "
            "and Zimbabwe maintain bilateral relations as Commonwealth members. "
            "The British Embassy in Harare can assist British nationals after "
            "a death. British death certificates require certified translation "
            "and authentication by the Zimbabwean Embassy or High Commission "
            "in London. Zimbabwe is a Hague Apostille Convention member; "
            "apostille certificates are accepted for UK-issued documents. "
            "(FCDO Travel Advice: Zimbabwe, 2025; Zimbabwe Ministry of Home "
            "Affairs, Registrar General Department, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'zimbabwe',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Zimbabwe include development workers, NGO "
            "professionals, and researchers. The US Embassy in Harare can "
            "assist US nationals after a death. English-language US death "
            "certificates require authentication by the Zimbabwean Embassy "
            "in Washington DC. Zimbabwe is a Hague Apostille Convention "
            "member; apostille certificates are accepted for US-issued "
            "documents. English is one of Zimbabwe's official languages "
            "and widely used in administration. "
            "(Zimbabwe Ministry of Home Affairs, Registrar General "
            "Department, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'zimbabwe',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Zimbabwe include development workers, "
            "researchers, and tourists. Germany and Zimbabwe maintain "
            "bilateral diplomatic relations and development cooperation. "
            "German death certificates (Sterbeurkunde, in German) require "
            "certified English translation and authentication by the "
            "Zimbabwean Embassy in Berlin. Zimbabwe is a Hague Apostille "
            "Convention member; apostille certificates are accepted for "
            "German-issued documents. "
            "(Zimbabwe Ministry of Home Affairs, Registrar General "
            "Department, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'zimbabwe',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Zimbabwe include development workers, "
            "researchers, and tourists, as well as individuals with bilateral "
            "Commonwealth ties. The Australian High Commission in Harare "
            "handles consular matters for Australian nationals in Zimbabwe. "
            "Australian death certificates (in English) require authentication "
            "by the Zimbabwean High Commission in Canberra. Zimbabwe is a "
            "Hague Apostille Convention member; apostille certificates are "
            "accepted for Australian documents. "
            "(Zimbabwe Ministry of Home Affairs, Registrar General "
            "Department, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'zimbabwe',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Zimbabwe include development workers, "
            "researchers, and tourists. France and Zimbabwe maintain bilateral "
            "diplomatic relations. French death certificates (acte de deces, "
            "in French) require certified English translation and authentication "
            "by the Zimbabwean Embassy in Paris. Zimbabwe is a Hague Apostille "
            "Convention member; apostille certificates are accepted for "
            "French-issued documents. "
            "(Zimbabwe Ministry of Home Affairs, Registrar General "
            "Department, 2025.)"
        ),
    },
    # R65 -- Uganda x5
    {
        'origin': 'united-kingdom', 'dest': 'uganda',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Uganda include development workers, NGO "
            "professionals, healthcare workers, and tourists visiting Bwindi "
            "Impenetrable Forest and national parks. The UK and Uganda maintain "
            "bilateral relations as Commonwealth members. The British High "
            "Commission in Kampala can assist British nationals after a death. "
            "British death certificates require authentication by the Ugandan "
            "High Commission in London. Uganda is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "English is Uganda's official language and widely used in "
            "administration. "
            "(FCDO Travel Advice: Uganda, 2025; Uganda Registration Services "
            "Bureau (URSB), 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'uganda',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Uganda include development workers, NGO "
            "professionals, healthcare workers, and researchers. The US "
            "maintains significant development cooperation with Uganda through "
            "PEPFAR and USAID programmes. The US Embassy in Kampala can "
            "assist US nationals after a death. English-language US death "
            "certificates require authentication by the Ugandan Embassy in "
            "Washington DC. Uganda is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Uganda Registration Services Bureau (URSB), 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'uganda',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Uganda include development workers, "
            "researchers, and NGO professionals. Germany and Uganda maintain "
            "bilateral development cooperation through GIZ programmes and "
            "German Embassy representation in Kampala. German death certificates "
            "(Sterbeurkunde, in German) require certified English translation "
            "and authentication by the Ugandan Embassy in Berlin. Uganda is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(Uganda Registration Services Bureau (URSB), 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'uganda',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals in Uganda include development workers, "
            "researchers, and tourists, as well as individuals with Commonwealth "
            "bilateral ties. Australian consular matters in Uganda are handled "
            "by the High Commission of Canada in Kampala under a consular "
            "services sharing arrangement, as Australia does not maintain a "
            "resident High Commission in Uganda. Australian death certificates "
            "(in English) require authentication by the Ugandan High Commission "
            "in Canberra. Uganda is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(DFAT Smartraveller: Uganda, 2025; Uganda Registration Services "
            "Bureau (URSB), 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'uganda',
        'embassy_city': 'The Hague',
        'intro': (
            "Dutch nationals in Uganda include development workers, NGO "
            "professionals, and researchers. The Netherlands has historically "
            "maintained development cooperation with Uganda. The Dutch Embassy "
            "in Kampala can assist Netherlands nationals after a death. Dutch "
            "death certificates (akte van overlijden, in Dutch) require "
            "certified English translation and authentication by the Ugandan "
            "Embassy in The Hague. Uganda is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Uganda Registration Services Bureau (URSB), 2025.)"
        ),
    },
    # R66 -- Ivory Coast x5
    {
        'origin': 'france', 'dest': 'ivory-coast',
        'embassy_city': 'Paris',
        'intro': (
            "Ivorian nationals in France form one of the largest West African "
            "diaspora communities in France, with deep cultural, linguistic, "
            "and bilateral ties reflecting the France-Ivory Coast historical "
            "relationship. France and Ivory Coast maintain close bilateral "
            "diplomatic and development cooperation. French death certificates "
            "(acte de deces, in French) are widely accepted in Ivorian "
            "administrative practice. Ivory Coast is not a Hague Apostille "
            "Convention member; full consular authentication through the "
            "Ivorian Embassy in Paris is required. "
            "(Ivorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'ivory-coast',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Ivory Coast include development workers, "
            "NGO professionals, business contacts, and researchers. The "
            "British Embassy in Abidjan can assist British nationals after "
            "a death. British death certificates require certified French "
            "translation and authentication by the Ivorian Embassy in London. "
            "Ivory Coast is not a Hague Apostille Convention member; full "
            "consular authentication is required. French is the official "
            "language and all documents must be in French or accompanied "
            "by a certified French translation. "
            "(FCDO Travel Advice: Ivory Coast, 2025; Ivorian Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'ivory-coast',
        'embassy_city': 'Brussels',
        'intro': (
            "Ivorian nationals in Belgium include a diaspora community with "
            "bilateral ties. Belgium and Ivory Coast maintain diplomatic "
            "relations and the Belgian Embassy in Abidjan is operational. "
            "Belgian death certificates (in French, Dutch, or German, depending "
            "on region) require certified French translation where not already "
            "in French, and authentication by the Ivorian Embassy in Brussels. "
            "Ivory Coast is not a Hague Apostille Convention member; full "
            "consular authentication is required. French-language Belgian "
            "documents are widely accepted in Ivorian administration. "
            "(Ivorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'ivory-coast',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Ivory Coast include development workers, "
            "business professionals, and researchers. Germany and Ivory Coast "
            "maintain bilateral development cooperation through GIZ programmes "
            "and German Embassy representation in Abidjan. German death "
            "certificates (Sterbeurkunde, in German) require certified French "
            "translation and authentication by the Ivorian Embassy in Berlin. "
            "Ivory Coast is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(Ivorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'ivory-coast',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Ivory Coast include development workers, NGO "
            "professionals, and researchers. The US maintains development "
            "cooperation with Ivory Coast and the US Embassy in Abidjan is "
            "operational. English-language US death certificates require "
            "certified French translation and authentication by the Ivorian "
            "Embassy in Washington DC. Ivory Coast is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(Ivorian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R66 -- DRC x5
    {
        'origin': 'france', 'dest': 'democratic-republic-of-the-congo',
        'embassy_city': 'Paris',
        'intro': (
            "Congolese nationals in France include one of the largest "
            "Central African diaspora communities in France, with deep "
            "cultural, linguistic, and bilateral ties reflecting the "
            "France-DRC relationship. France and the DRC maintain bilateral "
            "diplomatic and development cooperation. French death certificates "
            "(acte de deces, in French) are widely accepted in DRC "
            "administrative practice. The DRC is not a Hague Apostille "
            "Convention member; full consular authentication through the "
            "DRC Embassy in Paris is required. Families should verify "
            "current airline routes, as DRC flights can be subject to "
            "change. "
            "(DRC Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'democratic-republic-of-the-congo',
        'embassy_city': 'Brussels',
        'intro': (
            "Congolese nationals in Belgium include a substantial diaspora "
            "community with deep historical, cultural, and linguistic ties "
            "reflecting the Belgium-DRC bilateral relationship. Belgium and "
            "the DRC maintain bilateral diplomatic and development cooperation. "
            "Belgian death certificates (in French, Dutch, or German) require "
            "certified French translation where not already in French, and "
            "authentication by the DRC Embassy in Brussels. The DRC is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. French-language Belgian documents are widely accepted "
            "in DRC administration. "
            "(DRC Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'democratic-republic-of-the-congo',
        'embassy_city': 'London',
        'intro': (
            "British nationals in the DRC include development workers, NGO "
            "professionals, mining sector contacts, and researchers. The "
            "British Embassy in Kinshasa can assist British nationals after "
            "a death. British death certificates require certified French "
            "translation and authentication by the DRC Embassy in London. "
            "The DRC is not a Hague Apostille Convention member; full "
            "consular authentication is required. The FCDO advises against "
            "all travel to certain eastern DRC provinces; families should "
            "verify current security conditions before proceeding. "
            "(FCDO Travel Advice: Democratic Republic of the Congo, 2025; "
            "DRC Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'democratic-republic-of-the-congo',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in the DRC include development workers, NGO "
            "professionals, missionaries, and mining sector contacts. The "
            "US Embassy in Kinshasa can assist US nationals after a death. "
            "English-language US death certificates require certified French "
            "translation and authentication by the DRC Embassy in Washington "
            "DC. The DRC is not a Hague Apostille Convention member; full "
            "consular authentication is required. Families should verify "
            "current airline routes and the security situation before "
            "proceeding. "
            "(DRC Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'democratic-republic-of-the-congo',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in the DRC include development workers, "
            "researchers, and mining sector professionals. Germany and the "
            "DRC maintain bilateral development cooperation through GIZ "
            "programmes. German death certificates (Sterbeurkunde, in German) "
            "require certified French translation and authentication by the "
            "DRC Embassy in Berlin. The DRC is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "Families should verify current airline routes and conditions. "
            "(DRC Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R66 -- Afghanistan x5
    {
        'origin': 'united-kingdom', 'dest': 'afghanistan',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Afghanistan include individuals with "
            "family ties, journalists, and a small number of contractors "
            "and aid workers. The British Embassy in Kabul suspended "
            "operations in August 2021 following the change of government. "
            "Consular assistance for British nationals in Afghanistan is "
            "provided through the FCDO on +44 (0)20 7008 5000. British "
            "death certificates require certified Dari or Pashto translation. "
            "Afghanistan is not a Hague Apostille Convention member. "
            "Afghan consular matters in the UK are handled through the Afghan "
            "Charge d'Affaires in London. Repatriation to Afghanistan requires "
            "a specialist with current operational contacts. The FCDO advises "
            "against all travel to Afghanistan. "
            "(FCDO Travel Advice: Afghanistan, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'afghanistan',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Afghanistan include individuals with family ties, "
            "journalists, and contractors. The US Embassy in Kabul suspended "
            "operations in August 2021. Consular assistance for US nationals "
            "in Afghanistan is provided through the US State Department "
            "emergency line on +1 888 407 4747. English-language US death "
            "certificates require certified Dari or Pashto translation. "
            "Afghanistan is not a Hague Apostille Convention member; full "
            "consular authentication is required where available. Repatriation "
            "to Afghanistan requires a specialist with current operational "
            "contacts. "
            "(US State Department, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'afghanistan',
        'embassy_city': 'Berlin',
        'intro': (
            "Afghan nationals in Germany form one of the largest Afghan "
            "diaspora communities in Europe, reflecting decades of migration. "
            "The German Embassy in Kabul suspended operations in August 2021. "
            "Afghan consular matters in Germany are handled through the Afghan "
            "Embassy in Berlin. German death certificates (Sterbeurkunde, in "
            "German) require certified Dari or Pashto translation. Afghanistan "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required where available. Repatriation to "
            "Afghanistan requires a specialist with current operational contacts. "
            "(Afghan Embassy Berlin, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'afghanistan',
        'embassy_city': 'Canberra',
        'intro': (
            "Afghan nationals in Australia include a significant diaspora "
            "community, particularly following the 2021 evacuation. The "
            "Australian Embassy in Kabul suspended operations in August 2021. "
            "Consular assistance for Australian nationals in Afghanistan is "
            "provided through DFAT on 1300 555 135 (from Australia) or "
            "+61 2 6261 3305 (from overseas). Australian death certificates "
            "(in English) require certified Dari or Pashto translation. "
            "Afghanistan is not a Hague Apostille Convention member. "
            "Repatriation to Afghanistan requires a specialist with current "
            "operational contacts. "
            "(DFAT Smartraveller: Afghanistan, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'afghanistan',
        'embassy_city': 'Ottawa',
        'intro': (
            "Afghan nationals in Canada include a significant diaspora "
            "community, particularly following the 2021 evacuation. The "
            "Canadian Embassy in Kabul suspended operations in August 2021. "
            "Consular assistance for Canadian nationals in Afghanistan is "
            "provided through Global Affairs Canada on +1 613 996 8885 "
            "(collect calls accepted). Canadian death certificates (in "
            "English or French) require certified Dari or Pashto translation. "
            "Afghanistan is not a Hague Apostille Convention member; full "
            "consular authentication is required where available. Repatriation "
            "to Afghanistan requires a specialist with current operational contacts. "
            "(Global Affairs Canada, 2025.)"
        ),
    },
    # R66 -- Libya x5
    {
        'origin': 'united-kingdom', 'dest': 'libya',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Libya include oil sector contractors, "
            "journalists, and a small number of individuals with family ties. "
            "The British Embassy in Tripoli suspended operations in 2014. "
            "Consular assistance for British nationals in Libya is provided "
            "by the British Embassy in Tunis, Tunisia, and the FCDO on "
            "+44 (0)20 7008 5000. British death certificates require "
            "certified Arabic translation and authentication by the Libyan "
            "Embassy in London. Libya is not a Hague Apostille Convention "
            "member; full consular authentication is required. The FCDO "
            "advises against all travel to Libya. Repatriation to Libya "
            "requires a specialist with current operational contacts. "
            "(FCDO Travel Advice: Libya, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'libya',
        'embassy_city': 'Washington DC',
        'intro': (
            "US nationals in Libya include journalists, oil sector contractors, "
            "and individuals with family ties. The US Embassy in Tripoli "
            "suspended operations in 2014. Consular assistance for US nationals "
            "in Libya is provided through the US Embassy in Tunis and the US "
            "State Department emergency line on +1 888 407 4747. English-language "
            "US death certificates require certified Arabic translation and "
            "authentication by the Libyan Embassy in Washington DC. Libya is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(US State Department, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'libya',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Libya include oil sector professionals, "
            "construction contractors, and individuals with bilateral ties "
            "reflecting Italy's historical relationship with Libya. Italy "
            "maintains a diplomatic presence in Tripoli. Italian death "
            "certificates (atto di morte, in Italian) require certified "
            "Arabic translation and authentication by the Libyan Embassy "
            "in Rome. Libya is not a Hague Apostille Convention member; "
            "full consular authentication is required. The Italian Ministry "
            "of Foreign Affairs advises caution; families should verify "
            "current airline routes and consular access. "
            "(Libyan Government of National Unity, Ministry of Foreign "
            "Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'libya',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Libya include journalists, researchers, "
            "and oil sector contacts. The German Embassy in Tripoli "
            "suspended operations in 2014; German nationals requiring "
            "consular assistance in Libya should contact the German "
            "Embassy in Tunis or the German Foreign Office on "
            "+49 30 5000 2000. German death certificates (Sterbeurkunde, "
            "in German) require certified Arabic translation and "
            "authentication by the Libyan Embassy in Berlin. Libya is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(German Foreign Office, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'libya',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Libya include journalists, oil sector "
            "professionals, and individuals with bilateral ties. The French "
            "Embassy in Tripoli has limited operations; families should "
            "contact the French Ministry of Foreign Affairs crisis line "
            "on +33 1 43 17 67 67 after a death. French death certificates "
            "(acte de deces, in French) require certified Arabic translation "
            "and authentication by the Libyan Embassy in Paris. Libya is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(French Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R66 -- Tunisia x5
    {
        'origin': 'france', 'dest': 'tunisia',
        'embassy_city': 'Paris',
        'intro': (
            "Tunisian nationals in France form one of the largest North "
            "African diaspora communities in France, with deep cultural, "
            "linguistic, and bilateral ties. France and Tunisia maintain "
            "close bilateral diplomatic and development cooperation. French "
            "death certificates (acte de deces, in French) are widely "
            "accepted in Tunisian administrative practice alongside Arabic. "
            "Tunisia is not a Hague Apostille Convention member; full "
            "consular authentication through the Tunisian Embassy in Paris "
            "is required. For Muslim remains, which account for the large "
            "majority of Tunisia's population, Islamic law procedures apply "
            "and prompt burial is expected. "
            "(Tunisian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-kingdom', 'dest': 'tunisia',
        'embassy_city': 'London',
        'intro': (
            "British nationals in Tunisia include tourists, particularly "
            "in coastal resort areas, business professionals, and individuals "
            "with bilateral ties. The British Embassy in Tunis can assist "
            "British nationals after a death. British death certificates "
            "require certified Arabic translation and authentication by the "
            "Tunisian Embassy in London. Tunisia is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "The FCDO has country-specific travel advice for Tunisia; "
            "families should check current guidance. "
            "(FCDO Travel Advice: Tunisia, 2025; Tunisian Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'tunisia',
        'embassy_city': 'Berlin',
        'intro': (
            "Tunisian nationals in Germany include a significant diaspora "
            "community, reflecting migration bilateral ties. Germany and "
            "Tunisia maintain bilateral diplomatic relations and development "
            "cooperation. German death certificates (Sterbeurkunde, in German) "
            "require certified Arabic translation and authentication by the "
            "Tunisian Embassy in Berlin. Tunisia is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(Tunisian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'tunisia',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals in Tunisia include tourists, oil sector "
            "professionals, and individuals with bilateral ties reflecting "
            "Italy's proximity to Tunisia across the Mediterranean. Italy "
            "and Tunisia maintain bilateral diplomatic and economic relations. "
            "Italian death certificates (atto di morte, in Italian) require "
            "certified Arabic translation and authentication by the Tunisian "
            "Embassy in Rome. Tunisia is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(Tunisian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'belgium', 'dest': 'tunisia',
        'embassy_city': 'Brussels',
        'intro': (
            "Tunisian nationals in Belgium include a significant diaspora "
            "community with bilateral ties. Belgium and Tunisia maintain "
            "bilateral diplomatic relations. Belgian death certificates "
            "(in French, Dutch, or German depending on region) require "
            "certified Arabic translation and authentication by the "
            "Tunisian Embassy in Brussels. Tunisia is not a Hague "
            "Apostille Convention member; full consular authentication "
            "is required. French-language Belgian documents may be accepted "
            "in Tunisian administration alongside Arabic translation. "
            "(Tunisian Ministry of Foreign Affairs, 2025.)"
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
