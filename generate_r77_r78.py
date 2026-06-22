#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R77-R78.

   R77 (25 routes, variants B,C,D,E,A x5):
     Israel x5:  united-kingdom, united-states, germany, france, australia
     Spain x5:   united-kingdom, united-states, germany, australia, canada
     Italy x5:   united-kingdom, united-states, germany, france, australia
     Greece x5:  united-kingdom, united-states, france, australia, canada
     Canada x5:  united-kingdom, united-states, germany, france, australia

   R78 (25 routes, variants B,C,D,E,A x5):
     Portugal x5:  united-kingdom, united-states, germany, australia, ireland
     Austria x5:   united-kingdom, united-states, germany, france, australia
     Belgium x5:   united-kingdom, united-states, germany, australia, canada
     Singapore x5: united-kingdom, united-states, germany, france, canada
     Sweden x5:    united-kingdom, united-states, germany, france, australia

   Template rotation: R76 ended on A. R77 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   Rotation continues across both blocks (does not reset between R77 and R78).
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
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Israeli funeral director takes custody at Ben Gurion "
            "International Airport (TLV) near Tel Aviv cargo terminal. "
            "Death registration in Israel is handled by the Population "
            "Registry Authority under the Ministry of Interior "
            "(Misrad HaPnim). The Israeli death certificate is issued "
            "in Hebrew. All foreign-language death certificates require "
            "certified Hebrew translation before submission to the "
            "Population Registry. Families should be aware that religious "
            "considerations may affect burial timing; the Rabbinic Burial "
            "Society (Chevra Kadisha) handles Jewish burials according to "
            "traditional practice, while non-Jewish deceased are handled "
            "by other licensed burial societies. Israel joined the Hague "
            "Apostille Convention in 1978; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Population Registry Authority, Ministry of Interior, Israel, "
            "2025; FCDO Travel Advice: Israel, 2025.)"
        ),
        'consular_template': (
            "The Israeli Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Israel. "
            "Israel joined the Hague Apostille Convention in 1978. "
            "The Embassy cannot pay for or arrange repatriation. "
            "Contact the Population Registry Authority under the "
            "Ministry of Interior for civil registration queries."
        ),
        'arrival_faq': (
            "The Israeli funeral director takes custody at Ben Gurion "
            "International Airport (TLV) near Tel Aviv cargo terminal. "
            "The Population Registry Authority under the Ministry of "
            "Interior (Misrad HaPnim) registers the death. All foreign-"
            "language documents require certified Hebrew translation. "
            "Families should note that religious customs may affect "
            "burial timing and arrangements. Israel joined the Hague "
            "Apostille Convention in 1978; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Israeli Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-israel',
    },
    'spain': {
        'name': 'Spain',
        'slug': 'spain',
        'key': 'es',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Spanish funeral director takes custody at Madrid Barajas "
            "Airport (MAD), Barcelona El Prat Airport (BCN), Malaga Airport "
            "(AGP), or another airport depending on the family's destination. "
            "Death registration in Spain is handled by the Registro Civil "
            "(Civil Registry) under the Ministerio de Justicia. Foreign "
            "death certificates must be apostilled and, where not in Spanish, "
            "accompanied by a certified Spanish translation for the Registro "
            "Civil. Sanidad Exterior (the Spanish public health authority) "
            "may require documentation confirming the body is cleared for "
            "import. Spain joined the Hague Apostille Convention in 1978; "
            "apostille certificates from member states are accepted. An "
            "embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Registro Civil, Ministerio de Justicia, Spain, 2025; "
            "Ministerio de Sanidad, Spain, 2025; FCDO Travel Advice: "
            "Spain, 2025.)"
        ),
        'consular_template': (
            "The Spanish Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Spain. Spain "
            "joined the Hague Apostille Convention in 1978. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Registro "
            "Civil in the receiving municipality for civil registration "
            "queries."
        ),
        'arrival_faq': (
            "The Spanish funeral director takes custody at the receiving "
            "airport cargo terminal. The Registro Civil under the Ministerio "
            "de Justicia registers the death. Foreign death certificates "
            "must be apostilled and accompanied by a certified Spanish "
            "translation where not already in Spanish. Sanidad Exterior "
            "may require a health clearance document for import. Spain "
            "joined the Hague Apostille Convention in 1978. An embalming "
            "certificate and hermetically sealed coffin are required. "
            "The receiving funeral director coordinates with the local "
            "Registro Civil and the relevant health authority."
        ),
        'emergency_line': 'contact the Spanish Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-spain',
    },
    'italy': {
        'name': 'Italy',
        'slug': 'italy',
        'key': 'it',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Italian funeral director takes custody at Rome Fiumicino "
            "Airport (FCO), Milan Malpensa Airport (MXP), or another airport "
            "depending on the family's destination. Death registration in "
            "Italy is handled by the Comune (municipal administration) via "
            "the Ufficio di Stato Civile. Foreign death certificates must "
            "be apostilled and accompanied by a certified Italian translation "
            "(traduzione giurata) for submission to the Comune. The local "
            "Azienda Sanitaria Locale (ASL) may require clearance before "
            "burial or cremation proceeds. Italy joined the Hague Apostille "
            "Convention in 1978; apostille certificates from member states "
            "are accepted. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(Ministero dell'Interno, Ufficio di Stato Civile, Italy, 2025; "
            "FCDO Travel Advice: Italy, 2025.)"
        ),
        'consular_template': (
            "The Italian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Italy. Italy "
            "joined the Hague Apostille Convention in 1978. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Ufficio "
            "di Stato Civile in the receiving Comune for civil registration "
            "queries."
        ),
        'arrival_faq': (
            "The Italian funeral director takes custody at the receiving "
            "airport cargo terminal. The Ufficio di Stato Civile within the "
            "local Comune registers the death. Foreign death certificates "
            "must be apostilled and accompanied by a certified Italian "
            "translation (traduzione giurata). The local ASL may require "
            "clearance before burial or cremation proceeds. Italy joined "
            "the Hague Apostille Convention in 1978. An embalming certificate "
            "and hermetically sealed coffin are required. The receiving "
            "funeral director coordinates with the Comune and the ASL."
        ),
        'emergency_line': 'contact the Italian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-italy',
    },
    'greece': {
        'name': 'Greece',
        'slug': 'greece',
        'key': 'gr',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Greek funeral director takes custody at Athens "
            "Eleftherios Venizelos Airport (ATH) or Thessaloniki "
            "International Airport (SKG) cargo terminal, depending on "
            "the family's destination. Death registration in Greece is "
            "handled by the Lixiarheio (civil registry) under the General "
            "Secretariat for Civil Registration of the Ministry of Interior. "
            "Foreign death certificates must be apostilled and accompanied "
            "by a certified Greek translation for submission to the Lixiarheio. "
            "The Hellenic Police (EL.AS.) is notified for medico-legal "
            "purposes where required. Greece joined the Hague Apostille "
            "Convention in 1985; apostille certificates from member states "
            "are accepted. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(General Secretariat for Civil Registration, Ministry of "
            "Interior, Greece, 2025; FCDO Travel Advice: Greece, 2025.)"
        ),
        'consular_template': (
            "The Greek Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Greece. "
            "Greece joined the Hague Apostille Convention in 1985. "
            "The Embassy cannot pay for or arrange repatriation. "
            "Contact the Lixiarheio in the receiving municipality for "
            "civil registration queries."
        ),
        'arrival_faq': (
            "The Greek funeral director takes custody at the receiving "
            "airport cargo terminal. The Lixiarheio (civil registry) under "
            "the General Secretariat for Civil Registration registers the "
            "death. Foreign death certificates must be apostilled and "
            "accompanied by a certified Greek translation. The Hellenic "
            "Police (EL.AS.) is notified where required. Greece joined "
            "the Hague Apostille Convention in 1985. An embalming "
            "certificate and hermetically sealed coffin are required. "
            "The receiving funeral director coordinates with the local "
            "Lixiarheio."
        ),
        'emergency_line': 'contact the Greek Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-greece',
    },
    'canada': {
        'name': 'Canada',
        'slug': 'canada',
        'key': 'ca',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Canadian funeral director takes custody at Toronto Pearson "
            "International Airport (YYZ), Vancouver International Airport "
            "(YVR), Montreal Pierre Elliott Trudeau International Airport "
            "(YUL), or another major airport cargo terminal, depending on "
            "the family's destination. Death registration in Canada is "
            "handled by the provincial civil registration authority in the "
            "province where the death is registered: for example, Service "
            "Ontario in Ontario, or the Quebec Directeur "
            "de l'etat civil. Foreign death certificates must be apostilled "
            "and, where not in English or French, accompanied by a certified "
            "translation. Canada Border Services Agency (CBSA) clearance "
            "is required for all imported human remains. Provincial "
            "regulations for burial and cremation vary and are enforced "
            "by the receiving funeral director. Canada joined the Hague "
            "Apostille Convention; it entered into force in November 2024. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Service Canada, Provincial civil registration offices, 2025; "
            "Canada Border Services Agency (CBSA), 2025; FCDO Travel "
            "Advice: Canada, 2025.)"
        ),
        'consular_template': (
            "The Canadian High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Canada. "
            "Canada joined the Hague Apostille Convention, in force "
            "November 2024. The High Commission cannot pay for or arrange "
            "repatriation. Contact the relevant provincial civil registration "
            "authority for civil registration queries."
        ),
        'arrival_faq': (
            "The Canadian funeral director takes custody at the receiving "
            "airport cargo terminal. The relevant provincial civil registration "
            "authority registers the death. Foreign death certificates must "
            "be apostilled and accompanied by a certified translation where "
            "not in English or French. Canada Border Services Agency (CBSA) "
            "clearance is required for all imported human remains. "
            "Provincial regulations for burial and cremation vary. Canada "
            "joined the Hague Apostille Convention; it entered into force "
            "in November 2024. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Canadian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-canada',
    },
    'portugal': {
        'name': 'Portugal',
        'slug': 'portugal',
        'key': 'pt',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Portuguese funeral director takes custody at Lisbon "
            "Humberto Delgado Airport (LIS), Porto Francisco Sa Carneiro "
            "Airport (OPO), or Faro Airport (FAO) cargo terminal, depending "
            "on the family's destination. Death registration in Portugal "
            "is handled by the Conservatoria do Registo Civil under the "
            "Instituto dos Registos e do Notariado (IRN). Foreign death "
            "certificates must be apostilled and, where not in Portuguese, "
            "accompanied by a certified Portuguese translation for submission "
            "to the Conservatoria do Registo Civil. The Instituto Nacional "
            "de Medicina Legal e Ciencias Forenses (INMLCF) handles "
            "medico-legal cases. Portugal joined the Hague Apostille "
            "Convention in 1968; apostille certificates from member states "
            "are accepted. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(Conservatoria do Registo Civil, IRN, Portugal, 2025; "
            "FCDO Travel Advice: Portugal, 2025.)"
        ),
        'consular_template': (
            "The Portuguese Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Portugal. "
            "Portugal joined the Hague Apostille Convention in 1968. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the Conservatoria do Registo Civil via the IRN for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Portuguese funeral director takes custody at the receiving "
            "airport cargo terminal. The Conservatoria do Registo Civil "
            "under the IRN registers the death. Foreign death certificates "
            "must be apostilled and accompanied by a certified Portuguese "
            "translation where not already in Portuguese. The INMLCF "
            "handles medico-legal cases. Portugal joined the Hague Apostille "
            "Convention in 1968. An embalming certificate and hermetically "
            "sealed coffin are required. The receiving funeral director "
            "coordinates with the local Conservatoria do Registo Civil."
        ),
        'emergency_line': 'contact the Portuguese Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-portugal',
    },
    'austria': {
        'name': 'Austria',
        'slug': 'austria',
        'key': 'at',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Austrian funeral director takes custody at Vienna "
            "International Airport (VIE) cargo terminal. Death registration "
            "in Austria is handled by the Standesamt (civil registry office) "
            "in the municipality where the death is registered. Foreign "
            "death certificates must be apostilled and, where not in German, "
            "accompanied by a certified German translation (beglaubigte "
            "Ubersetzung) for submission to the Standesamt. The Gerichtsmedizin "
            "(Institute of Forensic Medicine) handles medico-legal cases. "
            "Austria joined the Hague Apostille Convention in 1968; apostille "
            "certificates from member states are accepted. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Standesamt, Bundesministerium fur Inneres, Austria, 2025; "
            "FCDO Travel Advice: Austria, 2025.)"
        ),
        'consular_template': (
            "The Austrian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Austria. Austria "
            "joined the Hague Apostille Convention in 1968. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Standesamt "
            "in the receiving municipality for civil registration queries."
        ),
        'arrival_faq': (
            "The Austrian funeral director takes custody at Vienna "
            "International Airport (VIE) cargo terminal. The Standesamt "
            "(civil registry office) in the receiving municipality registers "
            "the death. Foreign death certificates must be apostilled and "
            "accompanied by a certified German translation where not already "
            "in German. The Gerichtsmedizin handles medico-legal cases. "
            "Austria joined the Hague Apostille Convention in 1968. "
            "An embalming certificate and hermetically sealed coffin are "
            "required. The receiving funeral director coordinates with the "
            "local Standesamt."
        ),
        'emergency_line': 'contact the Austrian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-austria',
    },
    'belgium': {
        'name': 'Belgium',
        'slug': 'belgium',
        'key': 'be',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Belgian funeral director takes custody at Brussels Airport "
            "(BRU) cargo terminal. Death registration in Belgium is handled "
            "by the commune (gemeentehuis) in the municipality where the "
            "death is registered, via the Registre National des Personnes "
            "Physiques (National Register). Foreign death certificates must "
            "be apostilled and, where not in French, Dutch, or German, "
            "accompanied by a certified translation into the language of "
            "the relevant Belgian region. The Parquet (public prosecutor's "
            "office) is notified for medico-legal cases. Belgium joined the "
            "Hague Apostille Convention in 1975; apostille certificates "
            "from member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(SPF Justice, Belgium, 2025; Commune administration, Belgium, "
            "2025; FCDO Travel Advice: Belgium, 2025.)"
        ),
        'consular_template': (
            "The Belgian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Belgium. Belgium "
            "joined the Hague Apostille Convention in 1975. The Embassy "
            "cannot pay for or arrange repatriation. Contact the relevant "
            "commune administration for civil registration queries."
        ),
        'arrival_faq': (
            "The Belgian funeral director takes custody at Brussels Airport "
            "(BRU) cargo terminal. The commune (gemeentehuis) registers the "
            "death via the Registre National des Personnes Physiques. "
            "Foreign death certificates must be apostilled and accompanied "
            "by a certified translation into the relevant Belgian language "
            "(French, Dutch, or German). The Parquet is notified for "
            "medico-legal cases. Belgium joined the Hague Apostille Convention "
            "in 1975. An embalming certificate and hermetically sealed coffin "
            "are required. The receiving funeral director coordinates with "
            "the local commune."
        ),
        'emergency_line': 'contact the Belgian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-belgium',
    },
    'singapore': {
        'name': 'Singapore',
        'slug': 'singapore',
        'key': 'sg',
        'complexity_override': 'moderate',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '6-10 weeks',
        'reception': (
            "The Singapore funeral service takes custody at Singapore Changi "
            "Airport (SIN) cargo terminal. Death registration in Singapore "
            "is handled by the Registry of Births and Deaths under the "
            "Immigration and Checkpoints Authority (ICA). All foreign "
            "documents must be authenticated by consular means; Singapore "
            "is not a member of the Hague Apostille Convention, so apostille "
            "certificates are not accepted. Foreign death certificates "
            "require authentication by the Singapore Embassy or Consulate "
            "in the country of issue, followed by the Ministry of Foreign "
            "Affairs in Singapore (MFA legalisation). The National "
            "Environment Agency (NEA) regulates the handling of human "
            "remains. Ministry of Health (MOH) regulations apply to import "
            "and cremation or burial. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Immigration and Checkpoints Authority (ICA), Singapore, 2025; "
            "Ministry of Health (MOH), Singapore, 2025; FCDO Travel "
            "Advice: Singapore, 2025.)"
        ),
        'consular_template': (
            "The Singapore High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Singapore. "
            "Singapore is not a Hague Apostille Convention member; all "
            "foreign documents require consular authentication followed by "
            "MFA legalisation in Singapore. The High Commission cannot "
            "pay for or arrange repatriation. Contact the ICA Registry of "
            "Births and Deaths for civil registration queries."
        ),
        'arrival_faq': (
            "The Singapore funeral service takes custody at Changi Airport "
            "(SIN) cargo terminal. The Registry of Births and Deaths under "
            "the ICA registers the death. All foreign documents must be "
            "authenticated by consular means; apostille certificates are "
            "not accepted as Singapore is not a Hague Apostille member. "
            "Documents require authentication by the Singapore Embassy in "
            "the country of issue, then MFA legalisation in Singapore. "
            "The NEA regulates the handling of human remains. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Singapore High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-singapore',
    },
    'sweden': {
        'name': 'Sweden',
        'slug': 'sweden',
        'key': 'se',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Swedish funeral director takes custody at Stockholm Arlanda "
            "Airport (ARN) or Gothenburg Landvetter Airport (GOT) cargo "
            "terminal, depending on the family's destination. Death "
            "registration in Sweden is handled by Skatteverket (the Swedish "
            "Tax Agency), which maintains the civil registration records. "
            "Foreign death certificates must be apostilled and, where not "
            "in Swedish, accompanied by a certified Swedish translation "
            "for Skatteverket registration. Socialstyrelsen (the National "
            "Board of Health and Welfare) regulates funeral operations and "
            "the handling of human remains. Sweden joined the Hague "
            "Apostille Convention in 1999; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Skatteverket, Sweden, 2025; Socialstyrelsen, Sweden, 2025; "
            "FCDO Travel Advice: Sweden, 2025.)"
        ),
        'consular_template': (
            "The Swedish Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Sweden. Sweden "
            "joined the Hague Apostille Convention in 1999. The Embassy "
            "cannot pay for or arrange repatriation. Contact Skatteverket "
            "for civil registration queries."
        ),
        'arrival_faq': (
            "The Swedish funeral director takes custody at the receiving "
            "airport cargo terminal. Skatteverket (the Swedish Tax Agency) "
            "handles civil registration. Foreign death certificates must "
            "be apostilled and accompanied by a certified Swedish translation "
            "where not already in Swedish. Socialstyrelsen regulates the "
            "handling of human remains and funeral operations. Sweden joined "
            "the Hague Apostille Convention in 1999. An embalming certificate "
            "and hermetically sealed coffin are required. The receiving "
            "funeral director coordinates with Skatteverket."
        ),
        'emergency_line': 'contact the Swedish Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-sweden',
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
    'ireland': {
        'name': 'Ireland',
        'emergency': '999 or 112',
        'registry': 'the local civil registration service (General Register Office)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 999 or 112 for emergency services. Death is certified by a "
            "physician or, where necessary, the coroner. The death must be "
            "registered with the local civil registration service. The coroner "
            "takes jurisdiction for sudden, violent, or unexplained deaths and "
            "must issue a burial or cremation order before the body can be "
            "released. Ireland is a Hague Apostille Convention member. In "
            "complex cases, the coroner's investigation can take several weeks "
            "before the body is released."
        ),
        'doc_time': '3-7 days (coroner cases longer)',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '6-10 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Ireland is available at a number of approved "
            "locations, including facilities in Dublin and other cities."
        ),
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
}

ROUTES = [
    # R77 -- Israel x5
    {
        'origin': 'united-kingdom', 'dest': 'israel',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom is home to a large and established Jewish "
            "community, and many British nationals of Jewish heritage or with "
            "family connections in Israel maintain close ties to the country. "
            "Israel is also one of the most visited destinations for British "
            "tourists and pilgrims. The British Embassy in Tel Aviv is fully "
            "operational. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Israel, the death must be "
            "registered at the local register office in England and Wales "
            "within 5 days, or with the National Records of Scotland or GRONI "
            "in Northern Ireland. The UK death certificate is apostilled; "
            "Israel joined the Hague Apostille Convention in 1978. A certified "
            "Hebrew translation is required for submission to the Population "
            "Registry Authority (Misrad HaPnim). Families should be aware "
            "that religious customs may affect burial timing and arrangements. "
            "(FCDO Travel Advice: Israel, 2025; Population Registry Authority, "
            "Ministry of Interior, Israel, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'israel',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States is home to one of the world's largest Jewish "
            "diaspora communities, concentrated in New York, Los Angeles, "
            "Chicago, and Miami, with very strong family, cultural, and "
            "religious ties to Israel. The US Embassy is located in Jerusalem. "
            "When a person with Israeli family connections dies in the United "
            "States, the death is registered with the state civil records office "
            "where the death occurred. The Israeli Embassy in Washington DC "
            "can advise on documentation requirements for the Population "
            "Registry Authority (Misrad HaPnim). US death certificates are "
            "apostilled; Israel joined the Hague Apostille Convention in 1978. "
            "A certified Hebrew translation is required for the Population "
            "Registry Authority. "
            "(FCDO Travel Advice: Israel, 2025; Population Registry Authority, "
            "Ministry of Interior, Israel, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'israel',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to a significant and growing Israeli community, "
            "concentrated particularly in Berlin, with estimates of around "
            "20,000 Israeli nationals living in Germany. The German-Israeli "
            "bilateral relationship is active at diplomatic and cultural level. "
            "The Israeli Embassy in Berlin is fully operational. When an Israeli "
            "national or a person with Israeli family connections dies in "
            "Germany, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde is issued in German and "
            "requires a certified Hebrew translation for submission to the "
            "Population Registry Authority (Misrad HaPnim). Both Germany and "
            "Israel are Hague Apostille Convention members; Israel joined in "
            "1978. "
            "(FCDO Travel Advice: Israel, 2025; Population Registry Authority, "
            "Ministry of Interior, Israel, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'israel',
        'embassy_city': 'Paris',
        'intro': (
            "France is home to one of the largest Jewish communities in Europe, "
            "and there has been substantial aliyah (emigration to Israel) from "
            "France over recent decades. Significant family ties exist between "
            "French nationals and Israel. The Israeli Embassy in Paris is fully "
            "operational. When a person with Israeli family connections dies in "
            "France, the death is registered with the local mairie (town hall). "
            "The acte de deces is issued in French and requires a certified "
            "Hebrew translation for submission to the Population Registry "
            "Authority (Misrad HaPnim). Both France and Israel are Hague "
            "Apostille Convention members; Israel joined in 1978. "
            "(FCDO Travel Advice: Israel, 2025; Population Registry Authority, "
            "Ministry of Interior, Israel, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'israel',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has an established Jewish community and a number of "
            "nationals with family and cultural ties to Israel, as well as "
            "an active travel and pilgrimage corridor. The Israeli Embassy in "
            "Canberra is fully operational, with a consulate also in Sydney. "
            "When a person with Israeli family connections dies in Australia, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. The death certificate is apostilled; "
            "Israel joined the Hague Apostille Convention in 1978. A certified "
            "Hebrew translation is required for submission to the Population "
            "Registry Authority (Misrad HaPnim). "
            "(FCDO Travel Advice: Israel, 2025; Population Registry Authority, "
            "Ministry of Interior, Israel, 2025.)"
        ),
    },
    # R77 -- Spain x5
    {
        'origin': 'united-kingdom', 'dest': 'spain',
        'embassy_city': 'London',
        'intro': (
            "Spain is home to the largest British expatriate community in "
            "Europe, with several hundred thousand British nationals registered "
            "as residents, concentrated along the Costa del Sol, Costa Blanca, "
            "the Balearic Islands, and in major cities. Spain is also the most "
            "visited foreign country for British tourists, receiving well over "
            "10 million British visitors each year. When someone from the "
            "United Kingdom dies and their family wishes to repatriate remains "
            "to Spain, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The UK death "
            "certificate is apostilled; both countries are Hague Apostille "
            "Convention members. The Spanish Consulate in London can advise "
            "on documentation requirements for the Registro Civil. "
            "(FCDO Travel Advice: Spain, 2025; Registro Civil, Ministerio "
            "de Justicia, Spain, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'spain',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant population with Spanish "
            "heritage, and Spain is a popular destination for American "
            "tourists, students studying abroad, and professionals. Many "
            "American nationals also live in Spain under residency schemes. "
            "The Spanish Embassy in Washington DC is fully operational. When "
            "a person with Spanish family connections dies in the United "
            "States, the death is registered with the state civil records "
            "office where the death occurred. The US death certificate is "
            "apostilled; both countries are Hague Apostille Convention "
            "members. The Spanish Embassy in Washington DC can advise on "
            "documentation requirements for the Registro Civil. "
            "(FCDO Travel Advice: Spain, 2025; Registro Civil, Ministerio "
            "de Justicia, Spain, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'spain',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a significant population with Spanish heritage, with "
            "Spanish nationals among the largest migration communities in "
            "Germany following migration waves in the 1960s and 1970s and again "
            "after 2010. Spain is also one of the most popular holiday and "
            "retirement destinations for German nationals. The Spanish Embassy "
            "in Berlin is fully operational. When a person with Spanish family "
            "connections dies in Germany, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde requires a certified "
            "Spanish translation for the Registro Civil. Both countries are "
            "Hague Apostille Convention members. "
            "(FCDO Travel Advice: Spain, 2025; Registro Civil, Ministerio "
            "de Justicia, Spain, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'spain',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Spanish-speaking community with family ties to "
            "Spain, and Spain is a popular destination for Australian tourists "
            "and backpackers. The Spanish Embassy in Canberra is operational, "
            "with a consulate in Sydney. When a person with Spanish family "
            "connections dies in Australia, the death is registered with the "
            "state or territory Births, Deaths and Marriages (BDM) registry. "
            "The death certificate is apostilled; both countries are Hague "
            "Apostille Convention members. A certified Spanish translation "
            "may be required for the Registro Civil. "
            "(FCDO Travel Advice: Spain, 2025; Registro Civil, Ministerio "
            "de Justicia, Spain, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'spain',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a small but established Spanish-speaking community, "
            "and Spain is a destination for Canadian tourists, particularly "
            "those visiting cities such as Barcelona, Madrid, and Seville. "
            "Canada and Spain also share bilateral migration history through "
            "the Spanish emigration of the 1960s to 1980s. The Spanish Embassy "
            "in Ottawa is fully operational. When a person with Spanish family "
            "connections dies in Canada, the death is registered with the "
            "provincial civil registration authority. Canada joined the Hague "
            "Apostille Convention, in force November 2024; the provincial "
            "death certificate is apostilled and a certified Spanish translation "
            "may be required for the Registro Civil. "
            "(FCDO Travel Advice: Spain, 2025; Registro Civil, Ministerio "
            "de Justicia, Spain, 2025.)"
        ),
    },
    # R77 -- Italy x5
    {
        'origin': 'united-kingdom', 'dest': 'italy',
        'embassy_city': 'London',
        'intro': (
            "Italy and the United Kingdom share a long bilateral history, and "
            "there is a substantial Italian community in the UK, with around "
            "700,000 Italian nationals registered as residents and many more "
            "of Italian heritage. Many British nationals also live, retire, "
            "and work in Italy, and Italy is one of the most visited "
            "destinations for British tourists. When someone from the United "
            "Kingdom dies and their family wishes to repatriate remains to "
            "Italy, the death must be registered at the local register office "
            "in England and Wales within 5 days, or with the National Records "
            "of Scotland or GRONI in Northern Ireland. The UK death certificate "
            "is apostilled; both countries are Hague Apostille Convention "
            "members. The Italian Consulate in London can advise on "
            "documentation requirements for the Ufficio di Stato Civile. "
            "(FCDO Travel Advice: Italy, 2025; Ministero dell'Interno, "
            "Ufficio di Stato Civile, Italy, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'italy',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has one of the world's largest communities of "
            "Italian heritage, with an estimated 17 million or more Americans "
            "of Italian background, concentrated in the Northeast and in "
            "California. Many American-Italian families maintain strong "
            "connections to ancestral regions including Sicily, Campania, "
            "Calabria, and Veneto. The Italian Embassy in Washington DC is "
            "fully operational. When a person with Italian family connections "
            "dies in the United States, the death is registered with the state "
            "civil records office where the death occurred. The Italian Embassy "
            "in Washington DC can advise on documentation requirements for the "
            "Ufficio di Stato Civile. Both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Italy, 2025; Ministero dell'Interno, "
            "Italy, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'italy',
        'embassy_city': 'Berlin',
        'intro': (
            "Italy and Germany share a long border and are among the closest "
            "bilateral partners in the European Union. Germany is home to one "
            "of the largest Italian diaspora communities in Europe, with over "
            "650,000 Italian nationals registered as residents and historical "
            "migration going back to the 1950s labour agreements. The "
            "German-Italian repatriation corridor is well-established. When "
            "an Italian national dies in Germany, the death is registered with "
            "the local Standesamt (civil registry). The Sterbeurkunde is "
            "issued in German and requires a certified Italian translation "
            "(traduzione giurata) for the receiving Ufficio di Stato Civile. "
            "Both countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Italy, 2025; Ministero dell'Interno, "
            "Italy, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'italy',
        'embassy_city': 'Paris',
        'intro': (
            "France and Italy are neighbours with a shared border and "
            "substantial cross-border movement. France is home to a large "
            "Italian community, particularly in the south of France and in "
            "Paris, with historical migration going back generations. Many "
            "French nationals of Italian heritage maintain family connections "
            "in Italy. The Italian Embassy in Paris is fully operational. "
            "When an Italian national or a person with Italian family "
            "connections dies in France, the death is registered with the "
            "local mairie (town hall). The acte de deces requires a certified "
            "Italian translation for the receiving Ufficio di Stato Civile. "
            "Both countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Italy, 2025; Ministero dell'Interno, "
            "Italy, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'italy',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has one of the largest Italian diaspora communities "
            "outside Italy, with around one million Australians of Italian "
            "background, concentrated in Melbourne, Sydney, and Adelaide. "
            "The Australia-Italy repatriation corridor is among the most "
            "active for European-destination routes from Australia. The "
            "Italian Embassy in Canberra is fully operational. When an "
            "Italian national or a person of Italian heritage dies in "
            "Australia, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. The death "
            "certificate is apostilled; both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Italy, 2025; Ministero dell'Interno, "
            "Italy, 2025.)"
        ),
    },
    # R77 -- Greece x5
    {
        'origin': 'united-kingdom', 'dest': 'greece',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom is home to around 400,000 people of Greek and "
            "Greek Cypriot origin, and Greece is one of the most popular "
            "holiday destinations for British tourists, with over three million "
            "British visitors each year to the mainland and islands. The British "
            "Embassy in Athens is fully operational. When someone from the "
            "United Kingdom dies and their family wishes to repatriate remains "
            "to Greece, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The UK death "
            "certificate is apostilled; Greece joined the Hague Apostille "
            "Convention in 1985. The Greek Consulate or Embassy in London "
            "can advise on documentation for the Lixiarheio. A certified "
            "Greek translation is required for the Lixiarheio registration. "
            "(FCDO Travel Advice: Greece, 2025; General Secretariat for Civil "
            "Registration, Ministry of Interior, Greece, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'greece',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant Greek-American community, "
            "estimated at over one million people, concentrated in New York, "
            "Chicago, Boston, and Baltimore, with strong cultural and family "
            "ties to Greece and the Greek islands. The Greek Embassy in "
            "Washington DC is fully operational. When a Greek national or a "
            "person with Greek family connections dies in the United States, "
            "the death is registered with the state civil records office where "
            "the death occurred. The Greek Embassy in Washington DC can advise "
            "on documentation requirements for the Lixiarheio. Both countries "
            "are Hague Apostille Convention members; Greece joined in 1985. "
            "(FCDO Travel Advice: Greece, 2025; General Secretariat for Civil "
            "Registration, Ministry of Interior, Greece, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'greece',
        'embassy_city': 'Paris',
        'intro': (
            "France and Greece have long diplomatic and cultural ties, and "
            "Greece is a popular destination for French tourists, particularly "
            "during summer. A Greek community is present in France, and French "
            "nationals of Greek heritage maintain family connections in Greece. "
            "The Greek Embassy in Paris is fully operational. When a Greek "
            "national or a person with Greek family connections dies in France, "
            "the death is registered with the local mairie (town hall). The "
            "acte de deces requires a certified Greek translation for the "
            "receiving Lixiarheio. Both countries are Hague Apostille Convention "
            "members; Greece joined in 1985. "
            "(FCDO Travel Advice: Greece, 2025; General Secretariat for Civil "
            "Registration, Ministry of Interior, Greece, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'greece',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has one of the largest Greek communities outside Greece, "
            "with around 400,000 people of Greek heritage concentrated "
            "particularly in Melbourne, which is sometimes described as the "
            "third largest Greek city in the world by population. The "
            "Australia-Greece repatriation corridor is one of the most active "
            "from Australia to Europe. The Greek Embassy in Canberra is "
            "operational. When a Greek national or a person of Greek heritage "
            "dies in Australia, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. Both "
            "countries are Hague Apostille Convention members; Greece joined "
            "in 1985. "
            "(FCDO Travel Advice: Greece, 2025; General Secretariat for Civil "
            "Registration, Ministry of Interior, Greece, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'greece',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a Greek-Canadian community estimated at around 200,000, "
            "concentrated particularly in Toronto and Montreal, with strong "
            "family ties to Greece and the Greek islands. Canada is also a "
            "popular source of tourists visiting Greece. The Greek Embassy in "
            "Ottawa is fully operational. When a Greek national or a person "
            "with Greek family connections dies in Canada, the death is "
            "registered with the provincial civil registration authority. Canada "
            "joined the Hague Apostille Convention, in force November 2024; "
            "Greece joined the Convention in 1985. A certified Greek translation "
            "is required for the Lixiarheio. "
            "(FCDO Travel Advice: Greece, 2025; General Secretariat for Civil "
            "Registration, Ministry of Interior, Greece, 2025.)"
        ),
    },
    # R77 -- Canada x5
    {
        'origin': 'united-kingdom', 'dest': 'canada',
        'embassy_city': 'London',
        'intro': (
            "Canada and the United Kingdom share deep historical, cultural, "
            "and Commonwealth ties, and Canada is home to over 600,000 "
            "UK-born residents, one of the largest British communities abroad. "
            "British nationals retire, work, and study in Canada across "
            "all provinces, with particularly large communities in Ontario, "
            "British Columbia, and Alberta. The Canadian High Commission in "
            "London is fully operational. When someone from the United Kingdom "
            "dies and their family wishes to repatriate remains to Canada, "
            "the death must be registered at the local register office in "
            "England and Wales within 5 days, or with the National Records "
            "of Scotland or GRONI in Northern Ireland. Canada joined the "
            "Hague Apostille Convention; it entered into force in November "
            "2024. The UK death certificate is apostilled. "
            "(FCDO Travel Advice: Canada, 2025; Service Canada, Provincial "
            "civil registration offices, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'canada',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Canada share the world's longest undefended "
            "border and a deeply integrated bilateral relationship. Millions "
            "of Americans and Canadians live on either side of the border, "
            "and cross-border family ties are extremely common, particularly "
            "between the northern US states and Canadian provinces. The "
            "Canadian Embassy in Washington DC is fully operational. When a "
            "person with Canadian family connections dies in the United States, "
            "the death is registered with the state civil records office. The "
            "Canadian Embassy in Washington DC can advise on documentation "
            "requirements. Canada joined the Hague Apostille Convention; it "
            "entered into force in November 2024. "
            "(FCDO Travel Advice: Canada, 2025; Service Canada, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'canada',
        'embassy_city': 'Berlin',
        'intro': (
            "Canada has one of the world's largest German-heritage communities, "
            "with over three million Canadians of German background, concentrated "
            "in Ontario, the Prairie provinces, and British Columbia. Significant "
            "bilateral migration between Germany and Canada has occurred across "
            "multiple generations. The Canadian Embassy in Berlin is fully "
            "operational. When a person with Canadian family connections dies "
            "in Germany, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde requires a certified English "
            "translation for the provincial civil registration authority. Canada "
            "joined the Hague Apostille Convention, in force November 2024; "
            "Germany is also a Hague member. "
            "(FCDO Travel Advice: Canada, 2025; Service Canada, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'canada',
        'embassy_city': 'Paris',
        'intro': (
            "France and Canada maintain a close bilateral relationship rooted "
            "in the Francophone heritage of Quebec and the Acadian regions. "
            "France and Quebec have a formal cultural and diplomatic framework, "
            "and there is an active migration corridor between France and "
            "francophone Canada. The Canadian Embassy in Paris is fully "
            "operational. When a person with Canadian family connections dies "
            "in France, the death is registered with the local mairie (town "
            "hall). The acte de deces is in French, which is one of Canada's "
            "two official languages, simplifying reception in Quebec. Canada "
            "joined the Hague Apostille Convention, in force November 2024; "
            "France is also a Hague member. "
            "(FCDO Travel Advice: Canada, 2025; Service Canada, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'canada',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Canada share strong Anglosphere ties as fellow "
            "Commonwealth nations, and there is an active bilateral migration "
            "corridor, particularly among young professionals and families "
            "relocating between the two countries. Many Australians live and "
            "work in Canada, particularly in British Columbia and Ontario. "
            "The Canadian High Commission in Canberra is fully operational. "
            "When a person with Canadian family connections dies in Australia, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Canada joined the Hague Apostille "
            "Convention, in force November 2024; Australia is also a Hague "
            "member. "
            "(FCDO Travel Advice: Canada, 2025; Service Canada, 2025.)"
        ),
    },
    # R78 -- Portugal x5
    {
        'origin': 'united-kingdom', 'dest': 'portugal',
        'embassy_city': 'London',
        'intro': (
            "Portugal is home to one of the largest British expatriate "
            "communities in Europe, with tens of thousands of British nationals "
            "living in the Algarve, Lisbon, Porto, and the Silver Coast. "
            "Portugal is also a leading retirement destination for British "
            "nationals, attracted by the climate, lifestyle, and residency "
            "options. The British Embassy in Lisbon is fully operational. "
            "When someone from the United Kingdom dies and their family wishes "
            "to repatriate remains to Portugal, the death must be registered at "
            "the local register office in England and Wales within 5 days, or "
            "with the National Records of Scotland or GRONI in Northern Ireland. "
            "The UK death certificate is apostilled; both countries are Hague "
            "Apostille Convention members. The Portuguese Embassy in London "
            "can advise on documentation for the Conservatoria do Registo Civil. "
            "(FCDO Travel Advice: Portugal, 2025; Conservatoria do Registo "
            "Civil, IRN, Portugal, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'portugal',
        'embassy_city': 'Washington DC',
        'intro': (
            "Portugal has attracted a growing number of American nationals "
            "under its residency and digital nomad programmes, and American "
            "tourists and retirees have discovered Lisbon, Porto, and the "
            "Algarve as increasingly popular destinations. A Portuguese-American "
            "community has existed for generations, particularly in the "
            "northeastern United States. The Portuguese Embassy in Washington "
            "DC is fully operational. When a person with Portuguese family "
            "connections dies in the United States, the death is registered "
            "with the state civil records office where the death occurred. "
            "Both countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Portugal, 2025; Conservatoria do Registo "
            "Civil, IRN, Portugal, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'portugal',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is home to one of the largest Portuguese diaspora "
            "communities in Europe, with around 130,000 Portuguese nationals "
            "registered in Germany, concentrated in Frankfurt, Stuttgart, and "
            "Hamburg. The Germany-Portugal repatriation corridor is well-"
            "established and regularly used. The Portuguese Embassy in Berlin "
            "is fully operational. When a Portuguese national or a person with "
            "Portuguese family connections dies in Germany, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde requires a certified Portuguese translation for "
            "the Conservatoria do Registo Civil. Both countries are Hague "
            "Apostille Convention members. "
            "(FCDO Travel Advice: Portugal, 2025; Conservatoria do Registo "
            "Civil, IRN, Portugal, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'portugal',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Portuguese-speaking community with family ties "
            "to Portugal and the Azores, and Portugal has become a popular "
            "destination for Australian tourists and those exploring the "
            "European Union. The Portuguese Embassy in Canberra is operational. "
            "When a person with Portuguese family connections dies in Australia, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Both countries are Hague Apostille "
            "Convention members. A certified Portuguese translation may be "
            "required for the Conservatoria do Registo Civil. "
            "(FCDO Travel Advice: Portugal, 2025; Conservatoria do Registo "
            "Civil, IRN, Portugal, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'portugal',
        'embassy_city': 'Dublin',
        'intro': (
            "Portugal has become a notable destination for Irish nationals "
            "under digital nomad and residency schemes, with many Irish "
            "professionals and remote workers relocating to Lisbon, Porto, "
            "and the Algarve in recent years. Ireland and Portugal are both "
            "EU member states with active bilateral ties. The Portuguese "
            "Embassy in Dublin is fully operational. When someone from "
            "Ireland dies and their family wishes to repatriate remains to "
            "Portugal, the death must be registered with the local civil "
            "registration service. Ireland is a Hague Apostille Convention "
            "member, and the death certificate is apostilled. Portugal joined "
            "the Hague Apostille Convention in 1968; apostille certificates "
            "from member states are accepted. A certified Portuguese translation "
            "may be required for the Conservatoria do Registo Civil. "
            "(FCDO Travel Advice: Portugal, 2025; Conservatoria do Registo "
            "Civil, IRN, Portugal, 2025.)"
        ),
    },
    # R78 -- Austria x5
    {
        'origin': 'united-kingdom', 'dest': 'austria',
        'embassy_city': 'London',
        'intro': (
            "Austria is a popular destination for British tourists, "
            "particularly for skiing in the Alps and cultural visits to "
            "Vienna and Salzburg. A number of British nationals also live "
            "and work in Austria, and Vienna hosts international organisations "
            "with British staff. The British Embassy in Vienna is fully "
            "operational. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Austria, the death must "
            "be registered at the local register office in England and Wales "
            "within 5 days, or with the National Records of Scotland or GRONI "
            "in Northern Ireland. The UK death certificate is apostilled; "
            "both countries are Hague Apostille Convention members. The "
            "Austrian Embassy in London can advise on documentation for the "
            "Standesamt. A certified German translation is required. "
            "(FCDO Travel Advice: Austria, 2025; Standesamt, Bundesministerium "
            "fur Inneres, Austria, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'austria',
        'embassy_city': 'Washington DC',
        'intro': (
            "Austria is a destination for American tourists, students at "
            "the several American-affiliated academic institutions in Vienna, "
            "and US government personnel given Vienna's role as a hub for "
            "international organisations. An Austrian-American community also "
            "maintains bilateral family ties. The Austrian Embassy in "
            "Washington DC is fully operational. When a person with Austrian "
            "family connections dies in the United States, the death is "
            "registered with the state civil records office where the death "
            "occurred. The Austrian Embassy in Washington DC can advise on "
            "documentation requirements for the Standesamt. Both countries "
            "are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Austria, 2025; Standesamt, Bundesministerium "
            "fur Inneres, Austria, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'austria',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Austria share a language and a long border, and the "
            "bilateral migration corridor between the two countries is one of "
            "the most active in central Europe. Many Germans retire to or work "
            "in Austria, and many Austrians live in Germany. The German-Austrian "
            "repatriation corridor is well-established. When a person with "
            "Austrian family connections dies in Germany, the death is registered "
            "with the local Standesamt (civil registry). The Sterbeurkunde is "
            "issued in German, which is also Austria's official language, "
            "simplifying the documentation for the Austrian Standesamt. Both "
            "countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Austria, 2025; Standesamt, Bundesministerium "
            "fur Inneres, Austria, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'austria',
        'embassy_city': 'Paris',
        'intro': (
            "France and Austria maintain active bilateral diplomatic and "
            "cultural ties as fellow EU member states. French tourists visit "
            "Austria for skiing and cultural tourism, and Vienna hosts a "
            "number of international organisations with French personnel. "
            "The Austrian Embassy in Paris is fully operational. When a person "
            "with Austrian family connections dies in France, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "is issued in French and requires a certified German translation "
            "(beglaubigte Ubersetzung) for submission to the Austrian Standesamt. "
            "Both countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Austria, 2025; Standesamt, Bundesministerium "
            "fur Inneres, Austria, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'austria',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has an Austrian diaspora community with historical roots "
            "in post-Second World War migration; many Austrians emigrated to "
            "Australia in the late 1940s and 1950s, and families maintain "
            "bilateral ties. Austria is also a popular winter sports and "
            "cultural destination for Australian tourists. The Austrian Embassy "
            "in Canberra is operational. When a person with Austrian family "
            "connections dies in Australia, the death is registered with the "
            "state or territory Births, Deaths and Marriages (BDM) registry. "
            "Both countries are Hague Apostille Convention members. A certified "
            "German translation is required for the Austrian Standesamt. "
            "(FCDO Travel Advice: Austria, 2025; Standesamt, Bundesministerium "
            "fur Inneres, Austria, 2025.)"
        ),
    },
    # R78 -- Belgium x5
    {
        'origin': 'united-kingdom', 'dest': 'belgium',
        'embassy_city': 'London',
        'intro': (
            "Belgium and the United Kingdom have deep historical ties, "
            "including the role of Belgian territory in both World Wars. "
            "Belgium hosts the European Union and NATO headquarters in Brussels, "
            "with a significant British professional presence. The Commonwealth "
            "War Graves Commission maintains numerous cemeteries in Belgium, "
            "and many British families have historical connections to the "
            "country. The British Embassy in Brussels is fully operational. "
            "When someone from the United Kingdom dies and their family wishes "
            "to repatriate remains to Belgium, the death must be registered "
            "at the local register office in England and Wales within 5 days, "
            "or with the National Records of Scotland or GRONI in Northern "
            "Ireland. Both countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Belgium, 2025; SPF Justice, Belgium, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'belgium',
        'embassy_city': 'Washington DC',
        'intro': (
            "Belgium hosts NATO headquarters and several major international "
            "organisations in Brussels, maintaining a significant American "
            "military and diplomatic presence. The United States has historical "
            "connections to Belgium from both World Wars, and American tourists "
            "visit Belgian battlefields and cities. The Belgian Embassy in "
            "Washington DC is fully operational. When a person with Belgian "
            "family connections dies in the United States, the death is "
            "registered with the state civil records office where the death "
            "occurred. The Belgian Embassy in Washington DC can advise on "
            "documentation requirements for the commune administration. Both "
            "countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Belgium, 2025; SPF Justice, Belgium, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'belgium',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Belgium share a border and maintain a close bilateral "
            "relationship as fellow EU and Eurozone members. Belgium has a "
            "German-speaking community in the Eupen-Malmedy area (eastern "
            "Belgium), which has historical and cultural connections to Germany. "
            "Cross-border movement between Germany and Belgium is common. The "
            "Belgian Embassy in Berlin is fully operational. When a person "
            "with Belgian family connections dies in Germany, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German, which is an official language "
            "of Belgium, and may simplify documentation in the German-speaking "
            "community. Both countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Belgium, 2025; SPF Justice, Belgium, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'belgium',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Belgium maintain diplomatic and bilateral ties, "
            "and Australian tourists visit Belgium for its historic battlefields "
            "and cultural cities. A small Belgian diaspora community is present "
            "in Australia, and some Australians of Belgian heritage maintain "
            "family connections in Belgium. The Belgian Embassy in Canberra "
            "is operational. When a person with Belgian family connections "
            "dies in Australia, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. Both "
            "countries are Hague Apostille Convention members. A certified "
            "translation may be required for the Belgian commune. "
            "(FCDO Travel Advice: Belgium, 2025; SPF Justice, Belgium, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'belgium',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has historical military connections to Belgium from the "
            "First and Second World Wars, and Canadian tourists visit Belgian "
            "battlefields, Flanders Fields, and cities such as Bruges and "
            "Brussels. A small Belgian-Canadian community maintains family "
            "ties to Belgium. The Belgian Embassy in Ottawa is fully "
            "operational. When a person with Belgian family connections dies "
            "in Canada, the death is registered with the provincial civil "
            "registration authority. Canada joined the Hague Apostille Convention, "
            "in force November 2024; Belgium joined in 1975. A certified "
            "translation into the relevant Belgian language (French, Dutch, "
            "or German) may be required for the commune administration. "
            "(FCDO Travel Advice: Belgium, 2025; SPF Justice, Belgium, 2025.)"
        ),
    },
    # R78 -- Singapore x5
    {
        'origin': 'united-kingdom', 'dest': 'singapore',
        'embassy_city': 'London',
        'intro': (
            "Singapore is home to around 30,000 British nationals and is one "
            "of the most significant centres for British business, finance, "
            "law, and regional operations in Asia. British nationals work "
            "across banking, law, technology, and professional services. "
            "The British High Commission in Singapore is one of the most "
            "active in the region. When someone from the United Kingdom dies "
            "and their family wishes to repatriate remains to Singapore, the "
            "death must be registered at the local register office in England "
            "and Wales within 5 days, or with the National Records of Scotland "
            "or GRONI in Northern Ireland. Singapore is not a Hague Apostille "
            "Convention member; the UK death certificate must be authenticated "
            "by the Singapore High Commission in London and then legalised "
            "by the Singapore Ministry of Foreign Affairs (MFA). "
            "(FCDO Travel Advice: Singapore, 2025; Immigration and Checkpoints "
            "Authority (ICA), Singapore, 2025; Ministry of Health, Singapore, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'singapore',
        'embassy_city': 'Washington DC',
        'intro': (
            "Singapore is a major regional hub for American multinational "
            "corporations, with an estimated 30,000 American nationals "
            "residing in the city-state across finance, technology, and "
            "professional services. The US Embassy in Singapore is fully "
            "operational. When a person with Singaporean family connections "
            "dies in the United States, the death is registered with the "
            "state civil records office. Singapore is not a Hague Apostille "
            "Convention member; the US death certificate requires consular "
            "authentication by the Singapore Embassy in Washington DC, "
            "followed by MFA legalisation in Singapore. "
            "(FCDO Travel Advice: Singapore, 2025; Immigration and Checkpoints "
            "Authority (ICA), Singapore, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'singapore',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Singapore maintain an active trade and diplomatic "
            "relationship. German businesses are present across multiple "
            "sectors in Singapore, including engineering, chemicals, and "
            "financial services, and a German community is established in "
            "the city. The German Embassy in Singapore is operational. "
            "When a person with Singaporean family connections dies in Germany, "
            "the death is registered with the local Standesamt (civil registry). "
            "Singapore is not a Hague Apostille Convention member; the "
            "Sterbeurkunde requires consular authentication by the Singapore "
            "Embassy in Berlin, followed by MFA legalisation in Singapore. "
            "(FCDO Travel Advice: Singapore, 2025; Immigration and Checkpoints "
            "Authority (ICA), Singapore, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'singapore',
        'embassy_city': 'Paris',
        'intro': (
            "France and Singapore maintain bilateral diplomatic and trade "
            "ties. A French community is present in Singapore, and France "
            "operates the Lycee Francais de Singapour, reflecting the scale "
            "of the French professional community. The French Embassy in "
            "Singapore is operational. When a person with Singaporean family "
            "connections dies in France, the death is registered with the "
            "local mairie (town hall). Singapore is not a Hague Apostille "
            "Convention member; the acte de deces requires consular "
            "authentication by the Singapore Embassy in Paris, followed by "
            "MFA legalisation in Singapore. "
            "(FCDO Travel Advice: Singapore, 2025; Immigration and Checkpoints "
            "Authority (ICA), Singapore, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'singapore',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada and Singapore maintain a strong bilateral relationship "
            "with active trade and people-to-people ties. A Canadian business "
            "community is established in Singapore, and Canadian nationals "
            "work in technology, finance, and professional services. The "
            "Canadian High Commission in Singapore is operational. When a "
            "person with Singaporean family connections dies in Canada, the "
            "death is registered with the provincial civil registration authority. "
            "Singapore is not a Hague Apostille Convention member; the "
            "provincial death certificate requires consular authentication "
            "by the Singapore High Commission in Ottawa, followed by MFA "
            "legalisation in Singapore. "
            "(FCDO Travel Advice: Singapore, 2025; Immigration and Checkpoints "
            "Authority (ICA), Singapore, 2025.)"
        ),
    },
    # R78 -- Sweden x5
    {
        'origin': 'united-kingdom', 'dest': 'sweden',
        'embassy_city': 'London',
        'intro': (
            "Sweden and the United Kingdom maintain close bilateral ties as "
            "European neighbours, and a British community is present in "
            "Sweden, concentrated in Stockholm and Gothenburg. British "
            "nationals work in Sweden in technology, automotive, and "
            "professional services. Sweden is also a popular destination "
            "for British tourists. The British Embassy in Stockholm is "
            "fully operational. When someone from the United Kingdom dies "
            "and their family wishes to repatriate remains to Sweden, the "
            "death must be registered at the local register office in England "
            "and Wales within 5 days, or with the National Records of "
            "Scotland or GRONI in Northern Ireland. The UK death certificate "
            "is apostilled; both countries are Hague Apostille Convention "
            "members. A certified Swedish translation may be required for "
            "Skatteverket registration. "
            "(FCDO Travel Advice: Sweden, 2025; Skatteverket, Sweden, 2025; "
            "Socialstyrelsen, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'sweden',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a significant Swedish-American heritage "
            "community, reflecting the substantial Swedish emigration to "
            "the Midwest and Upper Midwest in the 19th and early 20th "
            "centuries. Many Swedish-Americans maintain family ties to "
            "Sweden, and American nationals also live and work in Sweden "
            "in technology and multinational companies. The Swedish Embassy "
            "in Washington DC is fully operational. When a person with "
            "Swedish family connections dies in the United States, the "
            "death is registered with the state civil records office. "
            "Both countries are Hague Apostille Convention members. "
            "(FCDO Travel Advice: Sweden, 2025; Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'sweden',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Sweden are close neighbours and active bilateral "
            "partners within the European Union. Cross-border migration is "
            "active, and a German community lives in Sweden, particularly "
            "in Stockholm and the university cities. Swedish nationals also "
            "live and work in Germany in large numbers. The Swedish Embassy "
            "in Berlin is fully operational. When a person with Swedish "
            "family connections dies in Germany, the death is registered "
            "with the local Standesamt (civil registry). The Sterbeurkunde "
            "is issued in German and requires a certified Swedish translation "
            "for Skatteverket registration. Both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Sweden, 2025; Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'sweden',
        'embassy_city': 'Paris',
        'intro': (
            "France and Sweden maintain active bilateral ties as EU member "
            "states, and French nationals are present in Sweden in "
            "international business and professional roles. Swedish nationals "
            "also live in France, particularly in Paris and the south. "
            "The Swedish Embassy in Paris is fully operational. When a person "
            "with Swedish family connections dies in France, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "is issued in French and requires a certified Swedish translation "
            "for Skatteverket registration. Both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Sweden, 2025; Skatteverket, Sweden, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'sweden',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Swedish-heritage community reflecting 19th and "
            "early 20th century migration, and some Australians of Swedish "
            "descent maintain family connections in Sweden. Sweden is also "
            "a destination for Australian tourists exploring Scandinavia. "
            "The Swedish Embassy in Canberra is operational. When a person "
            "with Swedish family connections dies in Australia, the death "
            "is registered with the state or territory Births, Deaths and "
            "Marriages (BDM) registry. Both countries are Hague Apostille "
            "Convention members; Sweden joined in 1999. A certified Swedish "
            "translation may be required for Skatteverket registration. "
            "(FCDO Travel Advice: Sweden, 2025; Skatteverket, Sweden, 2025.)"
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
