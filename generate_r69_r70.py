#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R69-R70.

   R69 (25 routes, variants B,C,D,E,A x5):
     Jamaica x5:   united-kingdom, united-states, canada, germany, france
     Barbados x5:  united-kingdom, united-states, canada, germany, france
     Cyprus x5:    united-kingdom, germany, greece, australia, united-states
     Malta x5:     united-kingdom, italy, germany, united-states, australia
     Hungary x5:   united-kingdom, germany, austria, united-states, france

   R70 (25 routes, variants B,C,D,E,A x5):
     Bulgaria x5:        united-kingdom, germany, united-states, france, netherlands
     Czech Republic x5:  united-kingdom, germany, austria, united-states, france
     Croatia x5:         united-kingdom, germany, italy, austria, united-states
     Iceland x5:         united-kingdom, united-states, germany, denmark, france
     Hong Kong x5:       united-kingdom, united-states, australia, canada, germany

   Template rotation: R68 ended A (index 0). R69 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R70 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'jamaica': {
        'name': 'Jamaica',
        'slug': 'jamaica',
        'key': 'jm',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Jamaican funeral director takes custody at Norman Manley "
            "International Airport Kingston (KIN) or Sangster International "
            "Airport Montego Bay (MBJ) cargo terminal, depending on the final "
            "destination. Death registration in Jamaica is handled by the "
            "Registrar General's Department (RGD) under the Ministry of "
            "National Security. Death certificates are issued in English, "
            "the official language. Jamaica acceded to the Hague Apostille "
            "Convention in 2021; apostille certificates from member states "
            "are accepted for relevant documents. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports. "
            "(Registrar General's Department, Jamaica, 2025; FCDO Travel "
            "Advice: Jamaica, 2025.)"
        ),
        'consular_template': (
            "The Jamaican High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Jamaica. Jamaica "
            "acceded to the Hague Apostille Convention in 2021. The High "
            "Commission cannot pay for or arrange repatriation. Contact the "
            "Registrar General's Department in Jamaica for civil registration "
            "queries."
        ),
        'arrival_faq': (
            "The Jamaican funeral director takes custody at Norman Manley "
            "International Airport Kingston (KIN) or Sangster International "
            "Airport Montego Bay (MBJ) cargo terminal. The Registrar General's "
            "Department (RGD) under the Ministry of National Security registers "
            "the death and issues a death certificate in English. Jamaica "
            "acceded to the Hague Apostille Convention in 2021; apostille "
            "certificates from member states are accepted for foreign-issued "
            "documents. An embalming certificate and hermetically sealed coffin "
            "are required. Registration at the RGD is sometimes slower than "
            "at UK registry offices; allow 3 to 6 weeks for straightforward cases."
        ),
        'emergency_line': 'contact the Jamaican High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-jamaica',
    },
    'barbados': {
        'name': 'Barbados',
        'slug': 'barbados',
        'key': 'bb',
        'reception': (
            "The Barbadian funeral director takes custody at Grantley Adams "
            "International Airport (BGI) cargo terminal. Death registration "
            "in Barbados is handled by the Registration Department under the "
            "Ministry of Home Affairs. Death certificates are issued in English, "
            "the official language. Barbados acceded to the Hague Apostille "
            "Convention in 2019; apostille certificates from member states are "
            "accepted for relevant documents. Barbados is a Commonwealth member. "
            "An embalming certificate and hermetically sealed coffin are required "
            "for all air imports. "
            "(Registration Department of Barbados, 2025; FCDO Travel "
            "Advice: Barbados, 2025.)"
        ),
        'consular_template': (
            "The Barbados High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Barbados. Barbados "
            "acceded to the Hague Apostille Convention in 2019. The High "
            "Commission cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Barbadian funeral director takes custody at Grantley Adams "
            "International Airport (BGI) cargo terminal. The Registration "
            "Department under the Ministry of Home Affairs registers the death "
            "and issues a death certificate in English. Barbados acceded to "
            "the Hague Apostille Convention in 2019; apostille certificates "
            "from member states are accepted for foreign-issued documents. "
            "Barbados is a Commonwealth member; English is the administrative "
            "language throughout. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Barbados High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-barbados',
    },
    'cyprus': {
        'name': 'Cyprus',
        'slug': 'cyprus',
        'key': 'cy',
        'complexity_override': 'moderate',
        'reception': (
            "The Cypriot funeral director takes custody at Larnaca International "
            "Airport (LCA) or Paphos International Airport (PFO) cargo terminal. "
            "In the government-controlled areas, death registration is handled "
            "by the Civil Registry and Migration Department (CRMD) of the "
            "Republic of Cyprus, with local registration at the municipal "
            "council (demos). Death certificates are issued in Greek. Cyprus "
            "has been a member of the Hague Apostille Convention since 1983; "
            "apostille certificates from member states are accepted. The northern "
            "part of Cyprus has been under Turkish military control since 1974 "
            "and is not recognised by most countries; the FCDO advises that the "
            "Republic of Cyprus does not control these areas. Deaths in the "
            "Sovereign Base Areas at Akrotiri or Dhekelia (British territory) "
            "require contact with the Sovereign Base Area Administration. All "
            "foreign documents require certified Greek translation. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(Civil Registry and Migration Department, Cyprus, 2025; FCDO "
            "Travel Advice: Cyprus, 2025.)"
        ),
        'consular_template': (
            "The Cyprus High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Cyprus. Cyprus "
            "has been a Hague Apostille Convention member since 1983. The "
            "High Commission cannot pay for or arrange repatriation. Families "
            "with a death in the northern areas should contact the FCDO "
            "for current guidance on consular access."
        ),
        'arrival_faq': (
            "The funeral director takes custody at Larnaca (LCA) or Paphos "
            "(PFO) cargo terminal. In government-controlled areas, the Civil "
            "Registry and Migration Department (CRMD) of the Republic of "
            "Cyprus handles death registration, with local registration at "
            "the municipal council (demos); certificates are issued in Greek. "
            "Cyprus has been a Hague Apostille Convention member since 1983; "
            "apostille certificates are accepted. Deaths in northern Cyprus "
            "or the Sovereign Base Areas require separate guidance from the "
            "FCDO. All foreign documents require certified Greek translation. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Cyprus High Commission or Embassy in the origin country, or the FCDO on +44 (0)20 7008 5000 for deaths in northern Cyprus or the Sovereign Base Areas',
        'hub_url': 'repatriation-from-cyprus',
    },
    'malta': {
        'name': 'Malta',
        'slug': 'malta',
        'key': 'mt',
        'reception': (
            "The Maltese funeral director takes custody at Malta International "
            "Airport (MLA) at Luqa cargo terminal. Death registration in Malta "
            "is handled by the Public Registry, administered by Identity Malta "
            "Agency. Death certificates are issued in Maltese and English, both "
            "official languages. Malta has been a member of the Hague Apostille "
            "Convention since 1968; apostille certificates from member states "
            "are accepted. Malta is an EU and Commonwealth member; English is "
            "widely used in administration. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Identity Malta Public Registry, 2025; FCDO Travel "
            "Advice: Malta, 2025.)"
        ),
        'consular_template': (
            "The Malta High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Malta. Malta "
            "has been a Hague Apostille Convention member since 1968. The "
            "High Commission cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Maltese funeral director takes custody at Malta International "
            "Airport (MLA) Luqa cargo terminal. The Public Registry, administered "
            "by Identity Malta Agency, registers the death and issues certificates "
            "in Maltese and English. Malta has been a Hague Apostille Convention "
            "member since 1968; apostille certificates from member states are "
            "accepted. Malta is an EU and Commonwealth member; English is used "
            "throughout the administration process. An embalming certificate "
            "and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Malta High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-malta',
    },
    'hungary': {
        'name': 'Hungary',
        'slug': 'hungary',
        'key': 'hu',
        'complexity_override': 'moderate',
        'reception': (
            "The Hungarian funeral director takes custody at Budapest Ferenc "
            "Liszt International Airport (BUD) cargo terminal. Death registration "
            "in Hungary is handled by the anyakoenyvi hivatal (civil registry "
            "office) of the local district government. Death certificates are "
            "issued in Hungarian. Hungary has been a member of the Hague "
            "Apostille Convention since 1973; apostille certificates from member "
            "states are accepted. All foreign documents require certified "
            "Hungarian translation. Hungary is an EU member. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(Hungarian civil registration authority, 2025; FCDO Travel "
            "Advice: Hungary, 2025.)"
        ),
        'consular_template': (
            "The Hungarian Embassy in {city} can advise on documentation "
            "requirements for repatriation to Hungary. Hungary has been a "
            "Hague Apostille Convention member since 1973. The Embassy cannot "
            "pay for or arrange repatriation. All foreign-issued documents "
            "require certified Hungarian translation before use in Hungary."
        ),
        'arrival_faq': (
            "The Hungarian funeral director takes custody at Budapest Ferenc "
            "Liszt International Airport (BUD) cargo terminal. The "
            "anyakoenyvi hivatal (civil registry office) of the local district "
            "government registers the death; certificates are issued in "
            "Hungarian. Hungary has been a Hague Apostille Convention member "
            "since 1973; apostille certificates are accepted for foreign-issued "
            "documents. All foreign documents require certified Hungarian "
            "translation. Hungary is an EU member. An embalming certificate "
            "and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Hungarian Embassy in the origin country',
        'hub_url': 'repatriation-from-hungary',
    },
    'bulgaria': {
        'name': 'Bulgaria',
        'slug': 'bulgaria',
        'key': 'bg',
        'complexity_override': 'moderate',
        'reception': (
            "The Bulgarian funeral director takes custody at Sofia Airport (SOF), "
            "Varna Airport (VAR), or Burgas Airport (BOJ) cargo terminal, "
            "depending on the final destination. Death registration in Bulgaria "
            "is handled by the local civil registration office "
            "(grazhdanska registratsiya) at the municipality level. Death "
            "certificates are issued in Bulgarian, written in Cyrillic script. "
            "Bulgaria has been a member of the Hague Apostille Convention since "
            "2001; apostille certificates from member states are accepted. All "
            "foreign documents require certified Bulgarian translation. Bulgaria "
            "is an EU member. An embalming certificate and hermetically sealed "
            "coffin are required for all air imports. "
            "(Bulgarian civil registration authorities, 2025; FCDO Travel "
            "Advice: Bulgaria, 2025.)"
        ),
        'consular_template': (
            "The Bulgarian Embassy in {city} can advise on documentation "
            "requirements for repatriation to Bulgaria. Bulgaria has been a "
            "Hague Apostille Convention member since 2001. The Embassy cannot "
            "pay for or arrange repatriation. All foreign-issued documents "
            "require certified Bulgarian translation."
        ),
        'arrival_faq': (
            "The Bulgarian funeral director takes custody at Sofia Airport (SOF), "
            "Varna (VAR), or Burgas (BOJ) cargo terminal. The local civil "
            "registration office (grazhdanska registratsiya) at the municipality "
            "registers the death; certificates are issued in Bulgarian Cyrillic. "
            "Bulgaria has been a Hague Apostille Convention member since 2001; "
            "apostille certificates are accepted for foreign-issued documents. "
            "All foreign documents require certified Bulgarian translation. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Bulgarian Embassy in the origin country',
        'hub_url': 'repatriation-from-bulgaria',
    },
    'czech-republic': {
        'name': 'Czech Republic',
        'slug': 'czech-republic',
        'key': 'cz',
        'reception': (
            "The Czech funeral director takes custody at Vaclav Havel Airport "
            "Prague (PRG) cargo terminal. Death registration in the Czech "
            "Republic is handled by the matrika (civil registry office) at "
            "the local authority. Death certificates are issued in Czech. "
            "The Czech Republic has been a member of the Hague Apostille "
            "Convention since 1998; apostille certificates from member states "
            "are accepted. All foreign documents require certified Czech "
            "translation. The Czech Republic is an EU member. An embalming "
            "certificate and hermetically sealed coffin are required for all "
            "air imports. "
            "(Czech civil registration (matrika), 2025; FCDO Travel "
            "Advice: Czech Republic, 2025.)"
        ),
        'consular_template': (
            "The Czech Embassy in {city} can advise on documentation requirements "
            "for repatriation to the Czech Republic. The Czech Republic has "
            "been a Hague Apostille Convention member since 1998. The Embassy "
            "cannot pay for or arrange repatriation. All foreign-issued "
            "documents require certified Czech translation."
        ),
        'arrival_faq': (
            "The Czech funeral director takes custody at Vaclav Havel Airport "
            "Prague (PRG) cargo terminal. The matrika (civil registry office) "
            "at the local authority registers the death; certificates are issued "
            "in Czech. The Czech Republic has been a Hague Apostille Convention "
            "member since 1998; apostille certificates are accepted for "
            "foreign-issued documents. All foreign documents require certified "
            "Czech translation. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Czech Embassy in the origin country',
        'hub_url': 'repatriation-from-czech-republic',
    },
    'croatia': {
        'name': 'Croatia',
        'slug': 'croatia',
        'key': 'hr',
        'reception': (
            "The Croatian funeral director takes custody at Franjo Tudman "
            "Airport Zagreb (ZAG), Split Airport (SPU), Dubrovnik Airport "
            "(DBV), or Zadar Airport (ZAD) cargo terminal, depending on the "
            "destination. Death registration in Croatia is handled by the "
            "maticar (civil registrar) at the local State Administration "
            "Office. Death certificates are issued in Croatian. Croatia has "
            "been a member of the Hague Apostille Convention since 1991; "
            "apostille certificates from member states are accepted. All "
            "foreign documents require certified Croatian translation. Croatia "
            "is an EU member since 2013. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Croatian Ministry of Administration, maticar, 2025; FCDO "
            "Travel Advice: Croatia, 2025.)"
        ),
        'consular_template': (
            "The Croatian Embassy in {city} can advise on documentation "
            "requirements for repatriation to Croatia. Croatia has been a "
            "Hague Apostille Convention member since 1991. The Embassy cannot "
            "pay for or arrange repatriation. All foreign-issued documents "
            "require certified Croatian translation."
        ),
        'arrival_faq': (
            "The Croatian funeral director takes custody at Zagreb (ZAG), "
            "Split (SPU), Dubrovnik (DBV), or Zadar (ZAD) cargo terminal. "
            "The maticar (civil registrar) at the local State Administration "
            "Office registers the death; certificates are issued in Croatian. "
            "Croatia has been a Hague Apostille Convention member since 1991; "
            "apostille certificates are accepted for foreign-issued documents. "
            "All foreign documents require certified Croatian translation. "
            "An embalming certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Croatian Embassy in the origin country',
        'hub_url': 'repatriation-from-croatia',
    },
    'iceland': {
        'name': 'Iceland',
        'slug': 'iceland',
        'key': 'is',
        'reception': (
            "The Icelandic funeral director takes custody at Keflavik "
            "International Airport (KEF) cargo terminal. Death registration "
            "in Iceland is handled by Registers Iceland (Thjodskra Islandinga), "
            "the national registry. Death certificates are issued in Icelandic. "
            "Iceland has been a member of the Hague Apostille Convention since "
            "1997; apostille certificates from member states are accepted. "
            "Iceland is an EEA and Schengen member. All foreign documents "
            "require certified Icelandic translation. An embalming certificate "
            "and hermetically sealed coffin are required for all air imports. "
            "(Registers Iceland (Thjodskra Islandinga), 2025; FCDO Travel "
            "Advice: Iceland, 2025.)"
        ),
        'consular_template': (
            "The Icelandic Embassy in {city} can advise on documentation "
            "requirements for repatriation to Iceland. Iceland has been a "
            "Hague Apostille Convention member since 1997. The Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Icelandic funeral director takes custody at Keflavik "
            "International Airport (KEF) cargo terminal. Registers Iceland "
            "(Thjodskra Islandinga) registers the death; certificates are "
            "issued in Icelandic. Iceland has been a Hague Apostille Convention "
            "member since 1997; apostille certificates are accepted for "
            "foreign-issued documents. All foreign documents require certified "
            "Icelandic translation. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Icelandic Embassy in the origin country',
        'hub_url': 'repatriation-from-iceland',
    },
    'hong-kong': {
        'name': 'Hong Kong',
        'slug': 'hong-kong',
        'key': 'hk',
        'complexity_override': 'moderate',
        'reception': (
            "The Hong Kong funeral director takes custody at Hong Kong "
            "International Airport (HKG) at Chek Lap Kok cargo terminal. "
            "Death registration in Hong Kong is handled by the Births and "
            "Deaths Registry under the Immigration Department of the Hong Kong "
            "Special Administrative Region (HKSAR). Bilingual death certificates "
            "are issued in English and Chinese. Hong Kong SAR is not a member "
            "of the Hague Apostille Convention; China, to which Hong Kong was "
            "returned in 1997, is not a Convention member. Full consular "
            "authentication through the relevant consulate in Hong Kong is "
            "required for all foreign-issued documents intended for use in "
            "HKSAR. An embalming certificate and hermetically sealed coffin "
            "are required for all air imports. "
            "(Hong Kong Immigration Department Births and Deaths Registry, "
            "2025; FCDO Travel Advice: Hong Kong, 2025.)"
        ),
        'consular_template': (
            "The HKSAR Government Office in {city} can provide general "
            "information on Hong Kong documentation requirements. For consular "
            "assistance with foreign-issued documents in Hong Kong, the "
            "relevant consulate general in Hong Kong can authenticate documents. "
            "Hong Kong SAR is not a Hague Apostille Convention member; full "
            "consular authentication is required."
        ),
        'arrival_faq': (
            "The Hong Kong funeral director takes custody at Hong Kong "
            "International Airport (HKG) Chek Lap Kok cargo terminal. The "
            "Births and Deaths Registry under the Immigration Department of "
            "the HKSAR registers the death and issues bilingual certificates "
            "in English and Chinese. Hong Kong SAR is not a Hague Apostille "
            "Convention member; full consular authentication of all "
            "foreign-issued documents is required. An embalming certificate "
            "and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the HKSAR Government Office in the origin country or the FCDO on +44 (0)20 7008 5000 for British nationals',
        'hub_url': 'repatriation-from-hong-kong',
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
    'greece': {
        'name': 'Greece',
        'emergency': '112 (EU unified) / 100 (police) / 166 (ambulance)',
        'registry': 'the local lixiarheio (civil registry) of the municipality',
        'cert_name': 'lixiarchiki praxi thanatou (death certificate)',
        'cert_lang': 'Greek',
        'overview': (
            "Call 112 for the EU emergency number, 100 for police, or 166 for "
            "ambulance. Death is certified by a physician. The lixiarchiki praxi "
            "thanatou (death certificate) is registered with the local lixiarheio "
            "(civil registry) of the municipality. Police and the eisangeleas "
            "(public prosecutor) take jurisdiction for violent or unexplained deaths. "
            "Greece is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': (
            "Cremation in Greece has been legal since 2006; facilities are "
            "limited but available in Athens and Thessaloniki."
        ),
        'postmortem_trigger': 'Violent or unexplained deaths (eisangeleas, public prosecutor takes jurisdiction)',
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
    'denmark': {
        'name': 'Denmark',
        'emergency': '112',
        'registry': 'the local borgerservice (citizen services) civil registry',
        'cert_name': 'doedsgrundsattest (death certificate)',
        'cert_lang': 'Danish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The doedsgrundsattest is registered with the local borgerservice "
            "(citizen services) civil registry. Police and the anklagemyndighed "
            "(public prosecutor) take jurisdiction for violent or unexplained "
            "deaths. Denmark is an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Denmark is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (anklagemyndighed, public prosecutor takes jurisdiction)',
    },
}

ROUTES = [
    # R69 -- Jamaica x5
    {
        'origin': 'united-kingdom', 'dest': 'jamaica',
        'embassy_city': 'London',
        'intro': (
            "The Jamaican-British community is one of the largest Caribbean "
            "diaspora communities in the United Kingdom, with roots stretching "
            "back to the Windrush generation of the 1940s and 1950s. When "
            "someone from this community dies in the UK and their family "
            "wishes to repatriate the remains to Jamaica, the death must first "
            "be registered with the local register office in England and Wales "
            "within 5 days, or with the National Records of Scotland or GRONI "
            "in Northern Ireland. The Jamaican High Commission in London can "
            "authenticate documents for the Registrar General's Department "
            "(RGD) in Jamaica. UK death certificates require no translation "
            "as English is Jamaica's official language. The coroner must issue "
            "a removal order before the remains can leave England and Wales "
            "in any sudden, violent, or unexplained death. Jamaica acceded "
            "to the Hague Apostille Convention in 2021. "
            "(FCDO Travel Advice: Jamaica, 2025; Registrar General's "
            "Department, Jamaica, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'jamaica',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Jamaican-American community is one of the largest Caribbean "
            "diaspora groups in the United States, concentrated particularly "
            "in New York, Florida, and Connecticut. When a Jamaican national "
            "or a person of Jamaican heritage dies in the US, the death is "
            "registered with the state civil records office where the death "
            "occurred. The Embassy of Jamaica in Washington DC can advise on "
            "document authentication requirements for the Registrar General's "
            "Department (RGD) in Jamaica. US death certificates in English "
            "require no translation. The state coroner or medical examiner "
            "takes jurisdiction for violent, sudden, or unexplained deaths. "
            "Jamaica acceded to the Hague Apostille Convention in 2021; "
            "US-issued apostille certificates are accepted. "
            "(Embassy of Jamaica, Washington DC, 2025; Registrar General's "
            "Department, Jamaica, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'jamaica',
        'embassy_city': 'Ottawa',
        'intro': (
            "The Jamaican-Canadian community is substantial, with significant "
            "populations in Toronto and Montreal. When a Jamaican national or "
            "a person of Jamaican heritage dies in Canada, the death is "
            "registered with the provincial civil records registry. The Jamaica "
            "High Commission in Ottawa can advise on documentation requirements "
            "for the Registrar General's Department (RGD) in Jamaica. Canadian "
            "death certificates in English or French require no translation "
            "as English is Jamaica's official language. The coroner or medical "
            "examiner takes jurisdiction for sudden, violent, or unexplained "
            "deaths. Canada is a Hague Apostille Convention member; Jamaica "
            "acceded to the Convention in 2021. "
            "(Jamaica High Commission, Ottawa, 2025; Registrar General's "
            "Department, Jamaica, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'jamaica',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Jamaica include tourists visiting the island's "
            "resorts and business professionals. When a German national dies "
            "in Germany and has requested repatriation to Jamaica, or when a "
            "person with Jamaican connections dies in Germany, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified English "
            "translation for use in Jamaica. The Embassy of Jamaica in Berlin "
            "can advise on documentation authentication for the Registrar "
            "General's Department (RGD). Germany and Jamaica are both Hague "
            "Apostille Convention members; Jamaica acceded in 2021. "
            "(Embassy of Jamaica in Berlin, 2025; Registrar General's "
            "Department, Jamaica, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'jamaica',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Jamaica include tourists and individuals with "
            "personal connections. When a person with Jamaican connections "
            "dies in France and their family wishes to repatriate remains "
            "to Jamaica, the death is registered with the local mairie "
            "(town hall). The acte de deces is issued in French and requires "
            "certified English translation for use in Jamaica. The Embassy "
            "of Jamaica in Paris can advise on documentation authentication "
            "for the Registrar General's Department (RGD) in Jamaica. France "
            "and Jamaica are both Hague Apostille Convention members; Jamaica "
            "acceded in 2021. "
            "(Embassy of Jamaica in Paris, 2025; Registrar General's "
            "Department, Jamaica, 2025.)"
        ),
    },
    # R69 -- Barbados x5
    {
        'origin': 'united-kingdom', 'dest': 'barbados',
        'embassy_city': 'London',
        'intro': (
            "The Barbadian-British community has deep roots in the United "
            "Kingdom, with Barbadian nationals and families of Barbadian "
            "heritage forming part of the broader Caribbean community settled "
            "in Britain. When someone from this community dies in the UK "
            "and their family wishes to repatriate remains to Barbados, the "
            "death must be registered at the local register office in England "
            "and Wales within 5 days. The Barbados High Commission in London "
            "can authenticate documents for the Registration Department of "
            "Barbados. UK death certificates in English require no translation. "
            "The coroner must issue a removal order before remains can leave "
            "England and Wales in sudden, violent, or unexplained deaths. "
            "Barbados acceded to the Hague Apostille Convention in 2019. "
            "Barbados is a Commonwealth member. "
            "(FCDO Travel Advice: Barbados, 2025; Registration Department "
            "of Barbados, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'barbados',
        'embassy_city': 'Washington DC',
        'intro': (
            "Barbadian nationals and people of Barbadian heritage in the United "
            "States form a well-established community in New York and Florida. "
            "When someone in this community dies in the US and their family "
            "wishes to repatriate remains to Barbados, the death is registered "
            "with the state civil records office where the death occurred. The "
            "Embassy of Barbados in Washington DC can advise on documentation "
            "requirements for the Registration Department of Barbados. US "
            "death certificates in English require no translation. Barbados "
            "acceded to the Hague Apostille Convention in 2019; US-issued "
            "apostille certificates are accepted. Barbados is a Commonwealth member. "
            "(Embassy of Barbados, Washington DC, 2025; Registration "
            "Department of Barbados, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'barbados',
        'embassy_city': 'Ottawa',
        'intro': (
            "The Barbadian-Canadian community is long-established, particularly "
            "in Toronto. When a Barbadian national or a person of Barbadian "
            "heritage dies in Canada and their family wishes to repatriate "
            "remains to Barbados, the death is registered with the provincial "
            "civil records registry. The Barbados High Commission in Ottawa "
            "can advise on documentation requirements for the Registration "
            "Department of Barbados. Canadian death certificates in English "
            "or French require no translation barrier (English is Barbados' "
            "official language). Canada and Barbados are both Hague Apostille "
            "Convention members. "
            "(Barbados High Commission, Ottawa, 2025; Registration "
            "Department of Barbados, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'barbados',
        'embassy_city': 'Berlin',
        'intro': (
            "German nationals in Barbados include tourists visiting the island's "
            "resorts; individual cases occasionally arise when a German national "
            "with Barbadian connections dies in Germany and their family wishes "
            "to repatriate remains to Barbados. The death is registered with "
            "the local Standesamt (civil registry) and the Sterbeurkunde, in "
            "German, requires certified English translation for use in Barbados. "
            "The Barbados High Commission in London provides consular coverage "
            "for Germany; families should contact the High Commission directly. "
            "Germany and Barbados are both Hague Apostille Convention members. "
            "(Barbados High Commission London, 2025; Registration "
            "Department of Barbados, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'barbados',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals in Barbados include tourists and a small number "
            "of business professionals. When a person with Barbadian connections "
            "dies in France and their family wishes to repatriate remains to "
            "Barbados, the death is registered with the local mairie (town "
            "hall). The acte de deces in French requires certified English "
            "translation for use in Barbados. The Embassy of Barbados in "
            "Paris can advise on documentation authentication for the "
            "Registration Department of Barbados. France and Barbados are "
            "both Hague Apostille Convention members. "
            "(Embassy of Barbados in Paris, 2025; Registration "
            "Department of Barbados, 2025.)"
        ),
    },
    # R69 -- Cyprus x5
    {
        'origin': 'united-kingdom', 'dest': 'cyprus',
        'embassy_city': 'London',
        'intro': (
            "The Cypriot-British community is among the largest in Europe, "
            "with British nationals of Cypriot heritage forming a significant "
            "settled community in London and other major cities. The island "
            "also has a large population of British expatriates who have "
            "retired or settled there. When someone from these communities "
            "dies in the UK and their family wishes to repatriate remains "
            "to Cyprus, the death must be registered at the local register "
            "office in England and Wales within 5 days. The Cyprus High "
            "Commission in London can advise on documentation requirements "
            "for the Civil Registry and Migration Department (CRMD) of the "
            "Republic of Cyprus. UK death certificates require certified Greek "
            "translation. Cyprus has been a Hague Apostille Convention member "
            "since 1983. Deaths with any connection to northern Cyprus or the "
            "Sovereign Base Areas require separate FCDO guidance. "
            "(FCDO Travel Advice: Cyprus, 2025; Civil Registry and Migration "
            "Department, Cyprus, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'cyprus',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a significant Cypriot community and bilateral economic "
            "ties with Cyprus. When a Cypriot national or a person of Cypriot "
            "heritage dies in Germany and their family wishes to repatriate "
            "remains to Cyprus, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in "
            "German and requires certified Greek translation for use in Cyprus. "
            "The Embassy of Cyprus in Berlin can advise on documentation "
            "authentication for the Civil Registry and Migration Department "
            "(CRMD). Both Germany and Cyprus are EU and Hague Apostille "
            "Convention members; Cyprus has been a member since 1983. "
            "(Embassy of Cyprus in Berlin, 2025; Civil Registry and Migration "
            "Department, Cyprus, 2025.)"
        ),
    },
    {
        'origin': 'greece', 'dest': 'cyprus',
        'embassy_city': 'Athens',
        'intro': (
            "Greece and Cyprus share close cultural, linguistic, and historical "
            "ties; Greek is the official language in both countries. When a "
            "Greek national with Cypriot connections dies in Greece and their "
            "family wishes to repatriate remains to Cyprus, the death is "
            "registered with the local lixiarheio (civil registry). The "
            "lixiarchiki praxi thanatou is issued in Greek and requires "
            "no translation for use in Cyprus. The Embassy of Cyprus in "
            "Athens can advise on documentation authentication for the Civil "
            "Registry and Migration Department (CRMD). Both countries are "
            "EU members; Cyprus has been a Hague Apostille Convention member "
            "since 1983, and Greece is also a member. "
            "(Embassy of Cyprus in Athens, 2025; Civil Registry and "
            "Migration Department, Cyprus, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'cyprus',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has one of the largest Cypriot diaspora communities "
            "outside Europe, with significant populations of Cypriot heritage "
            "in Melbourne and Sydney. When a person with Cypriot connections "
            "dies in Australia and their family wishes to repatriate remains "
            "to Cyprus, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. Australian death "
            "certificates require certified Greek translation for use in "
            "Cyprus. The Cyprus High Commission in Canberra can advise on "
            "documentation requirements for the Civil Registry and Migration "
            "Department (CRMD). Australia and Cyprus are both Hague Apostille "
            "Convention members; Cyprus has been a member since 1983. "
            "(Cyprus High Commission, Canberra, 2025; Civil Registry and "
            "Migration Department, Cyprus, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'cyprus',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Cypriot-American community in the United States has strong "
            "ties to the island, particularly around Washington DC and New "
            "York. When a person with Cypriot connections dies in the US "
            "and their family wishes to repatriate remains to Cyprus, the "
            "death is registered with the state civil records office. US "
            "death certificates require certified Greek translation for use "
            "in Cyprus. The Embassy of Cyprus in Washington DC can advise "
            "on documentation authentication for the Civil Registry and "
            "Migration Department (CRMD). The US and Cyprus are both Hague "
            "Apostille Convention members; Cyprus has been a member since 1983. "
            "(Embassy of Cyprus, Washington DC, 2025; Civil Registry and "
            "Migration Department, Cyprus, 2025.)"
        ),
    },
    # R69 -- Malta x5
    {
        'origin': 'united-kingdom', 'dest': 'malta',
        'embassy_city': 'London',
        'intro': (
            "The Maltese-British community is long-established, with Maltese "
            "nationals and people of Maltese heritage having settled in the "
            "United Kingdom over generations of Commonwealth migration. When "
            "someone from this community dies in the UK and their family "
            "wishes to repatriate remains to Malta, the death must be "
            "registered at the local register office in England and Wales "
            "within 5 days. The Malta High Commission in London can advise "
            "on documentation requirements for the Public Registry (Identity "
            "Malta). UK death certificates in English require no translation "
            "as English is an official language in Malta. The coroner must "
            "issue a removal order before remains can leave England and Wales "
            "in sudden, violent, or unexplained deaths. Malta has been a "
            "Hague Apostille Convention member since 1968. "
            "(FCDO Travel Advice: Malta, 2025; Identity Malta Public "
            "Registry, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'malta',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Malta share geographic proximity across the "
            "Mediterranean; Maltese and Italian cultural ties are close. "
            "When an Italian national with Maltese connections dies in Italy "
            "and their family wishes to repatriate remains to Malta, the death "
            "is registered with the local Ufficio di Stato Civile. The atto "
            "di morte is issued in Italian and requires certified Maltese or "
            "English translation for use in Malta. The Embassy of Malta in "
            "Rome can advise on documentation authentication for the Public "
            "Registry (Identity Malta). Both countries are EU and Hague "
            "Apostille Convention members; Malta has been a member since 1968. "
            "(Embassy of Malta in Rome, 2025; Identity Malta Public "
            "Registry, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'malta',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a Maltese community and bilateral ties with Malta "
            "as fellow EU members. When a person with Maltese connections "
            "dies in Germany and their family wishes to repatriate remains "
            "to Malta, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde is issued in German and "
            "requires certified English or Maltese translation for use in "
            "Malta. The Embassy of Malta in Berlin can advise on documentation "
            "authentication for the Public Registry (Identity Malta). Both "
            "countries are EU and Hague Apostille Convention members; Malta "
            "has been a member since 1968. "
            "(Embassy of Malta in Berlin, 2025; Identity Malta Public "
            "Registry, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'malta',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Maltese-American community has roots in earlier twentieth-century "
            "migration from Malta to the United States. When a person with "
            "Maltese connections dies in the US and their family wishes to "
            "repatriate remains to Malta, the death is registered with the "
            "state civil records office where the death occurred. US death "
            "certificates in English require no translation for use in Malta. "
            "The Embassy of Malta in Washington DC can advise on documentation "
            "authentication for the Public Registry (Identity Malta). The US "
            "and Malta are both Hague Apostille Convention members; Malta has "
            "been a member since 1968. "
            "(Embassy of Malta, Washington DC, 2025; Identity Malta Public "
            "Registry, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'malta',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has one of the largest Maltese diaspora communities "
            "in the world, with significant populations in Melbourne and "
            "Sydney dating from post-war Commonwealth migration. When a person "
            "with Maltese connections dies in Australia and their family "
            "wishes to repatriate remains to Malta, the death is registered "
            "with the state or territory Births, Deaths and Marriages (BDM) "
            "registry. Australian death certificates in English require no "
            "translation for use in Malta. The Malta High Commission in "
            "Canberra can advise on documentation requirements for the "
            "Public Registry (Identity Malta). Australia and Malta are both "
            "Hague Apostille Convention members. "
            "(Malta High Commission, Canberra, 2025; Identity Malta Public "
            "Registry, 2025.)"
        ),
    },
    # R69 -- Hungary x5
    {
        'origin': 'united-kingdom', 'dest': 'hungary',
        'embassy_city': 'London',
        'intro': (
            "The Hungarian-British community includes post-1956 refugees, "
            "subsequent generations, and more recent migrants following "
            "Hungary's EU accession in 2004. When someone from this community "
            "dies in the UK and their family wishes to repatriate remains "
            "to Hungary, the death must be registered at the local register "
            "office in England and Wales within 5 days. The Hungarian Embassy "
            "in London can advise on documentation requirements for the "
            "anyakoenyvi hivatal (civil registry office) in Hungary. UK death "
            "certificates require certified Hungarian translation. The coroner "
            "must issue a removal order before remains can leave England and "
            "Wales in sudden, violent, or unexplained deaths. Hungary has "
            "been a Hague Apostille Convention member since 1973. "
            "(FCDO Travel Advice: Hungary, 2025; Hungarian civil registration "
            "authority, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'hungary',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has one of the largest Hungarian diaspora communities "
            "in the European Union, with significant populations in Munich, "
            "Berlin, and Frankfurt. When a Hungarian national or a person "
            "of Hungarian heritage dies in Germany and their family wishes "
            "to repatriate remains to Hungary, the death is registered with "
            "the local Standesamt (civil registry). The Sterbeurkunde is "
            "issued in German and requires certified Hungarian translation "
            "for use in Hungary. The Hungarian Embassy in Berlin can advise "
            "on documentation authentication for the anyakoenyvi hivatal "
            "(civil registry office) in Hungary. Both countries are EU and "
            "Hague Apostille Convention members; Hungary has been a member "
            "since 1973. "
            "(Hungarian Embassy in Berlin, 2025; Hungarian civil registration "
            "authority, 2025.)"
        ),
    },
    {
        'origin': 'austria', 'dest': 'hungary',
        'embassy_city': 'Vienna',
        'intro': (
            "Austria and Hungary share a border and close historical ties "
            "from the former Austro-Hungarian Empire. The Hungarian community "
            "in Austria is well-established. When a Hungarian national or "
            "a person of Hungarian heritage dies in Austria and their family "
            "wishes to repatriate remains to Hungary, the death is registered "
            "with the local Standesamt (civil registry). The Sterbeurkunde "
            "is issued in German and requires certified Hungarian translation "
            "for use in Hungary. The Hungarian Embassy in Vienna can advise "
            "on documentation requirements for the anyakoenyvi hivatal (civil "
            "registry office). Both countries are EU and Hague Apostille "
            "Convention members; Hungary has been a member since 1973. "
            "(Hungarian Embassy in Vienna, 2025; Hungarian civil registration "
            "authority, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'hungary',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Hungarian-American community has deep roots dating from "
            "nineteenth-century migration and the 1956 refugee exodus. When "
            "a person with Hungarian connections dies in the US and their "
            "family wishes to repatriate remains to Hungary, the death is "
            "registered with the state civil records office where the death "
            "occurred. US death certificates require certified Hungarian "
            "translation for use in Hungary. The Embassy of Hungary in "
            "Washington DC can advise on documentation authentication for "
            "the anyakoenyvi hivatal (civil registry office) in Hungary. "
            "The US and Hungary are both Hague Apostille Convention members; "
            "Hungary has been a member since 1973. "
            "(Embassy of Hungary, Washington DC, 2025; Hungarian civil "
            "registration authority, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'hungary',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Hungarian community reflecting bilateral cultural "
            "and economic ties. When a person with Hungarian connections dies "
            "in France and their family wishes to repatriate remains to Hungary, "
            "the death is registered with the local mairie (town hall). The "
            "acte de deces is issued in French and requires certified Hungarian "
            "translation for use in Hungary. The Hungarian Embassy in Paris "
            "can advise on documentation authentication for the anyakoenyvi "
            "hivatal (civil registry office) in Hungary. Both countries are "
            "EU and Hague Apostille Convention members; Hungary has been a "
            "member since 1973. "
            "(Hungarian Embassy in Paris, 2025; Hungarian civil registration "
            "authority, 2025.)"
        ),
    },
    # R70 -- Bulgaria x5
    {
        'origin': 'united-kingdom', 'dest': 'bulgaria',
        'embassy_city': 'London',
        'intro': (
            "The Bulgarian-British community grew significantly after Bulgaria "
            "joined the European Union in 2007, with Bulgarian nationals "
            "settling in the UK for work. When a Bulgarian national or a "
            "person of Bulgarian heritage dies in the UK and their family "
            "wishes to repatriate remains to Bulgaria, the death must be "
            "registered at the local register office in England and Wales "
            "within 5 days. The Bulgarian Embassy in London can advise on "
            "documentation requirements for the civil registration office "
            "(grazhdanska registratsiya) in Bulgaria. UK death certificates "
            "require certified Bulgarian translation. The coroner must issue "
            "a removal order before remains can leave England and Wales in "
            "sudden, violent, or unexplained deaths. Bulgaria has been a "
            "Hague Apostille Convention member since 2001. "
            "(FCDO Travel Advice: Bulgaria, 2025; Bulgarian civil "
            "registration authorities, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'bulgaria',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany hosts the largest Bulgarian diaspora community in the "
            "European Union, with significant numbers in Berlin, Munich, and "
            "Stuttgart. When a Bulgarian national dies in Germany and their "
            "family wishes to repatriate remains to Bulgaria, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires certified Bulgarian "
            "translation for use in Bulgaria. The Bulgarian Embassy in Berlin "
            "can advise on documentation authentication for the civil "
            "registration office in Bulgaria. Both countries are EU and Hague "
            "Apostille Convention members; Bulgaria has been a member since 2001. "
            "(Bulgarian Embassy in Berlin, 2025; Bulgarian civil "
            "registration authorities, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'bulgaria',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Bulgarian-American community is established in cities including "
            "New York and Chicago. When a person with Bulgarian connections "
            "dies in the US and their family wishes to repatriate remains "
            "to Bulgaria, the death is registered with the state civil records "
            "office where the death occurred. US death certificates require "
            "certified Bulgarian translation for use in Bulgaria. The Bulgarian "
            "Embassy in Washington DC can advise on documentation authentication "
            "for the civil registration office in Bulgaria. The US and Bulgaria "
            "are both Hague Apostille Convention members; Bulgaria has been "
            "a member since 2001. "
            "(Bulgarian Embassy, Washington DC, 2025; Bulgarian civil "
            "registration authorities, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'bulgaria',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Bulgarian community reflecting both earlier migration "
            "and more recent EU freedom of movement. When a person with Bulgarian "
            "connections dies in France and their family wishes to repatriate "
            "remains to Bulgaria, the death is registered with the local mairie "
            "(town hall). The acte de deces is issued in French and requires "
            "certified Bulgarian translation for use in Bulgaria. The Bulgarian "
            "Embassy in Paris can advise on documentation authentication for "
            "the civil registration office in Bulgaria. Both countries are "
            "EU and Hague Apostille Convention members; Bulgaria has been "
            "a member since 2001. "
            "(Bulgarian Embassy in Paris, 2025; Bulgarian civil "
            "registration authorities, 2025.)"
        ),
    },
    {
        'origin': 'netherlands', 'dest': 'bulgaria',
        'embassy_city': 'The Hague',
        'intro': (
            "The Netherlands has a Bulgarian community following EU accession "
            "in 2007, with Bulgarian nationals working in agriculture, logistics, "
            "and services. When a Bulgarian national dies in the Netherlands "
            "and their family wishes to repatriate remains to Bulgaria, the "
            "death is registered with the local gemeente (municipality) civil "
            "registry. The akte van overlijden is issued in Dutch and requires "
            "certified Bulgarian translation for use in Bulgaria. The Bulgarian "
            "Embassy in The Hague can advise on documentation authentication "
            "for the civil registration office in Bulgaria. Both countries "
            "are EU and Hague Apostille Convention members; Bulgaria has been "
            "a member since 2001. "
            "(Bulgarian Embassy in The Hague, 2025; Bulgarian civil "
            "registration authorities, 2025.)"
        ),
    },
    # R70 -- Czech Republic x5
    {
        'origin': 'united-kingdom', 'dest': 'czech-republic',
        'embassy_city': 'London',
        'intro': (
            "Czech nationals have settled in the United Kingdom in two main "
            "waves: following the 1968 Soviet invasion and after the Czech "
            "Republic joined the EU in 2004. When a Czech national or a "
            "person of Czech heritage dies in the UK and their family wishes "
            "to repatriate remains to the Czech Republic, the death must be "
            "registered at the local register office in England and Wales "
            "within 5 days. The Czech Embassy in London can advise on "
            "documentation requirements for the matrika (civil registry office) "
            "in the Czech Republic. UK death certificates require certified "
            "Czech translation. The coroner must issue a removal order before "
            "remains can leave England and Wales in sudden, violent, or "
            "unexplained deaths. The Czech Republic has been a Hague Apostille "
            "Convention member since 1998. "
            "(FCDO Travel Advice: Czech Republic, 2025; Czech civil "
            "registration (matrika), 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'czech-republic',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and the Czech Republic share a long border and close "
            "economic and cultural ties. The Czech community in Germany is "
            "well-established. When a Czech national dies in Germany and "
            "their family wishes to repatriate remains to the Czech Republic, "
            "the death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires certified "
            "Czech translation for use in the Czech Republic. The Czech "
            "Embassy in Berlin can advise on documentation authentication "
            "for the matrika (civil registry office). Both countries are "
            "EU and Hague Apostille Convention members; the Czech Republic "
            "has been a member since 1998. "
            "(Czech Embassy in Berlin, 2025; Czech civil registration "
            "(matrika), 2025.)"
        ),
    },
    {
        'origin': 'austria', 'dest': 'czech-republic',
        'embassy_city': 'Vienna',
        'intro': (
            "Austria and the Czech Republic share a border and close ties "
            "from the former Habsburg period. The Czech community in Austria "
            "reflects both historical and more recent migration. When a Czech "
            "national dies in Austria and their family wishes to repatriate "
            "remains to the Czech Republic, the death is registered with "
            "the local Standesamt (civil registry). The Sterbeurkunde is "
            "issued in German and requires certified Czech translation for "
            "use in the Czech Republic. The Czech Embassy in Vienna can "
            "advise on documentation authentication for the matrika (civil "
            "registry office). Both countries are EU and Hague Apostille "
            "Convention members; the Czech Republic has been a member "
            "since 1998. "
            "(Czech Embassy in Vienna, 2025; Czech civil registration "
            "(matrika), 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'czech-republic',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Czech-American community has roots in nineteenth-century "
            "migration and the post-1968 Czech diaspora. When a person with "
            "Czech connections dies in the US and their family wishes to "
            "repatriate remains to the Czech Republic, the death is registered "
            "with the state civil records office where the death occurred. "
            "US death certificates require certified Czech translation for "
            "use in the Czech Republic. The Czech Embassy in Washington DC "
            "can advise on documentation authentication for the matrika "
            "(civil registry office). The US and Czech Republic are both "
            "Hague Apostille Convention members; the Czech Republic has "
            "been a member since 1998. "
            "(Czech Embassy, Washington DC, 2025; Czech civil registration "
            "(matrika), 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'czech-republic',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Czech community reflecting both historical ties "
            "and more recent EU freedom of movement. When a person with Czech "
            "connections dies in France and their family wishes to repatriate "
            "remains to the Czech Republic, the death is registered with the "
            "local mairie (town hall). The acte de deces is issued in French "
            "and requires certified Czech translation for use in the Czech "
            "Republic. The Czech Embassy in Paris can advise on documentation "
            "authentication for the matrika (civil registry office). Both "
            "countries are EU and Hague Apostille Convention members; the "
            "Czech Republic has been a member since 1998. "
            "(Czech Embassy in Paris, 2025; Czech civil registration "
            "(matrika), 2025.)"
        ),
    },
    # R70 -- Croatia x5
    {
        'origin': 'united-kingdom', 'dest': 'croatia',
        'embassy_city': 'London',
        'intro': (
            "Croatia joined the European Union in 2013 and has grown as a "
            "popular destination for British tourists and expatriates, "
            "particularly on the Dalmatian coast. The Croatian community "
            "in the UK also includes individuals who settled here from the "
            "former Yugoslavia. When a Croatian national or a person of "
            "Croatian heritage dies in the UK and their family wishes to "
            "repatriate remains to Croatia, the death must be registered at "
            "the local register office in England and Wales within 5 days. "
            "The Croatian Embassy in London can advise on documentation "
            "requirements for the maticar (civil registrar) in Croatia. "
            "UK death certificates require certified Croatian translation. "
            "Croatia has been a Hague Apostille Convention member since 1991. "
            "(FCDO Travel Advice: Croatia, 2025; Croatian Ministry of "
            "Administration, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'croatia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has one of the largest Croatian diaspora communities "
            "outside Croatia, reflecting the Gastarbeiter labour migration "
            "from the 1960s and more recent EU movement. When a Croatian "
            "national dies in Germany and their family wishes to repatriate "
            "remains to Croatia, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in "
            "German and requires certified Croatian translation for use in "
            "Croatia. The Croatian Embassy in Berlin can advise on "
            "documentation authentication for the maticar (civil registrar). "
            "Both countries are EU and Hague Apostille Convention members; "
            "Croatia has been a member since 1991. "
            "(Croatian Embassy in Berlin, 2025; Croatian Ministry of "
            "Administration, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'croatia',
        'embassy_city': 'Rome',
        'intro': (
            "Italy and Croatia share the Adriatic Sea and have close "
            "geographic and cultural ties, with a historical Italian-speaking "
            "community in parts of Istria and Dalmatia. When an Italian "
            "national with Croatian connections dies in Italy and their "
            "family wishes to repatriate remains to Croatia, the death is "
            "registered with the local Ufficio di Stato Civile. The atto "
            "di morte is issued in Italian and requires certified Croatian "
            "translation for use in Croatia. The Croatian Embassy in Rome "
            "can advise on documentation authentication for the maticar "
            "(civil registrar). Both countries are EU and Hague Apostille "
            "Convention members; Croatia has been a member since 1991. "
            "(Croatian Embassy in Rome, 2025; Croatian Ministry of "
            "Administration, 2025.)"
        ),
    },
    {
        'origin': 'austria', 'dest': 'croatia',
        'embassy_city': 'Vienna',
        'intro': (
            "Austria has a significant Croatian community, reflecting both "
            "historical Habsburg ties and more recent migration. The "
            "Gradiscansko-Croatian (Burgenland Croatian) community has been "
            "settled in Austria for centuries. When a Croatian national dies "
            "in Austria and their family wishes to repatriate remains to "
            "Croatia, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde is issued in German and "
            "requires certified Croatian translation for use in Croatia. "
            "The Croatian Embassy in Vienna can advise on documentation "
            "requirements for the maticar (civil registrar). Both countries "
            "are EU and Hague Apostille Convention members; Croatia has been "
            "a member since 1991. "
            "(Croatian Embassy in Vienna, 2025; Croatian Ministry of "
            "Administration, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'croatia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The Croatian-American community has roots stretching back to "
            "nineteenth-century migration, with concentrations in Chicago, "
            "Pittsburgh, and New York. When a person with Croatian connections "
            "dies in the US and their family wishes to repatriate remains "
            "to Croatia, the death is registered with the state civil records "
            "office where the death occurred. US death certificates require "
            "certified Croatian translation for use in Croatia. The Embassy "
            "of Croatia in Washington DC can advise on documentation "
            "authentication for the maticar (civil registrar) in Croatia. "
            "The US and Croatia are both Hague Apostille Convention members; "
            "Croatia has been a member since 1991. "
            "(Embassy of Croatia, Washington DC, 2025; Croatian Ministry "
            "of Administration, 2025.)"
        ),
    },
    # R70 -- Iceland x5
    {
        'origin': 'united-kingdom', 'dest': 'iceland',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom and Iceland have close historical and cultural "
            "connections as North Atlantic neighbours. British nationals in "
            "Iceland include business professionals, academics, and those with "
            "personal ties. When a person with Icelandic connections dies "
            "in the UK and their family wishes to repatriate remains to Iceland, "
            "the death must be registered at the local register office in "
            "England and Wales within 5 days. The Icelandic Embassy in London "
            "can advise on documentation requirements for Registers Iceland "
            "(Thjodskra Islandinga). UK death certificates require certified "
            "Icelandic translation. Iceland has been a Hague Apostille "
            "Convention member since 1997. "
            "(FCDO Travel Advice: Iceland, 2025; Registers Iceland "
            "(Thjodskra Islandinga), 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'iceland',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Iceland have a longstanding bilateral "
            "relationship; Iceland hosted a US military presence at Keflavik "
            "until 2006. The Icelandic-American community and business ties "
            "remain active. When a person with Icelandic connections dies "
            "in the US and their family wishes to repatriate remains to Iceland, "
            "the death is registered with the state civil records office. "
            "US death certificates require certified Icelandic translation "
            "for use in Iceland. The Embassy of Iceland in Washington DC "
            "can advise on documentation authentication for Registers Iceland "
            "(Thjodskra Islandinga). The US and Iceland are both Hague "
            "Apostille Convention members; Iceland has been a member since 1997. "
            "(Embassy of Iceland, Washington DC, 2025; Registers Iceland "
            "(Thjodskra Islandinga), 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'iceland',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany is one of Iceland's main trading partners, and German "
            "tourists visit Iceland in large numbers. When a person with "
            "Icelandic connections dies in Germany and their family wishes "
            "to repatriate remains to Iceland, the death is registered with "
            "the local Standesamt (civil registry). The Sterbeurkunde is "
            "issued in German and requires certified Icelandic translation "
            "for use in Iceland. The Icelandic Embassy in Berlin can advise "
            "on documentation authentication for Registers Iceland "
            "(Thjodskra Islandinga). Both Germany and Iceland are Hague "
            "Apostille Convention members; Iceland has been a member since 1997. "
            "(Icelandic Embassy in Berlin, 2025; Registers Iceland "
            "(Thjodskra Islandinga), 2025.)"
        ),
    },
    {
        'origin': 'denmark', 'dest': 'iceland',
        'embassy_city': 'Copenhagen',
        'intro': (
            "Denmark and Iceland share deep Nordic historical and cultural "
            "ties; Iceland was part of the Danish kingdom until 1944. The "
            "two countries have close bilateral relations within the Nordic "
            "Council. When a person with Icelandic connections dies in Denmark "
            "and their family wishes to repatriate remains to Iceland, the "
            "death is registered with the local borgerservice (citizen "
            "services) civil registry. The doedsgrundsattest is issued in "
            "Danish and requires certified Icelandic translation for use "
            "in Iceland. The Icelandic Embassy in Copenhagen can advise on "
            "documentation authentication for Registers Iceland "
            "(Thjodskra Islandinga). Both countries are Hague Apostille "
            "Convention members; Iceland has been a member since 1997. "
            "(Icelandic Embassy in Copenhagen, 2025; Registers Iceland "
            "(Thjodskra Islandinga), 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'iceland',
        'embassy_city': 'Paris',
        'intro': (
            "France and Iceland have bilateral diplomatic and economic "
            "relations; Iceland is a popular destination for French tourists "
            "seeking the Northern Lights and natural landscapes. When a "
            "person with Icelandic connections dies in France and their "
            "family wishes to repatriate remains to Iceland, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "is issued in French and requires certified Icelandic translation "
            "for use in Iceland. The Icelandic Embassy in Paris can advise "
            "on documentation authentication for Registers Iceland "
            "(Thjodskra Islandinga). Both countries are Hague Apostille "
            "Convention members; Iceland has been a member since 1997. "
            "(Icelandic Embassy in Paris, 2025; Registers Iceland "
            "(Thjodskra Islandinga), 2025.)"
        ),
    },
    # R70 -- Hong Kong x5
    {
        'origin': 'united-kingdom', 'dest': 'hong-kong',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom and Hong Kong have deep historical ties; "
            "Hong Kong was a British Crown Colony until 1997. British "
            "nationals with Hong Kong connections include former residents, "
            "those holding British National (Overseas) (BN(O)) status, "
            "and recent arrivals to the UK following the 2021 BN(O) visa "
            "scheme. When a person with Hong Kong connections dies in the "
            "UK and their family wishes to repatriate remains to Hong Kong, "
            "the death must be registered at the local register office in "
            "England and Wales within 5 days. The HKSAR Government Office "
            "in London can provide general information. UK death certificates "
            "require authentication through the Hong Kong consular network. "
            "Hong Kong SAR is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(FCDO Travel Advice: Hong Kong, 2025; Hong Kong Immigration "
            "Department Births and Deaths Registry, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'hong-kong',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a long-standing relationship with Hong "
            "Kong; the US Consulate General in Hong Kong is one of the "
            "busiest in Asia. The Hong Kong-American community is substantial, "
            "particularly in California and New York. When a person with "
            "Hong Kong connections dies in the US and their family wishes "
            "to repatriate remains to Hong Kong, the death is registered "
            "with the state civil records office. US death certificates "
            "require authentication by the relevant consulate in Hong Kong. "
            "Hong Kong SAR is not a Hague Apostille Convention member; "
            "full consular authentication of US-issued documents is required "
            "for use in the HKSAR. "
            "(US Consulate General Hong Kong, 2025; Hong Kong Immigration "
            "Department Births and Deaths Registry, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'hong-kong',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has one of the largest Hong Kong diaspora communities "
            "outside Asia, with significant populations in Sydney and Melbourne "
            "reflecting migration waves from the 1980s, 1997 handover period, "
            "and after 2020. When a person with Hong Kong connections dies "
            "in Australia and their family wishes to repatriate remains to "
            "Hong Kong, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. Australian death "
            "certificates require authentication by the Australian Consulate "
            "General in Hong Kong. Hong Kong SAR is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(Australian Consulate General Hong Kong, 2025; Hong Kong "
            "Immigration Department Births and Deaths Registry, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'hong-kong',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada hosts the largest Hong Kong diaspora outside Asia, "
            "with major communities in Vancouver and Toronto that grew "
            "substantially in the years before and after the 1997 handover. "
            "When a person with Hong Kong connections dies in Canada and "
            "their family wishes to repatriate remains to Hong Kong, the "
            "death is registered with the provincial civil records registry. "
            "Canadian death certificates require authentication by the "
            "Canadian Consulate General in Hong Kong. Hong Kong SAR is "
            "not a Hague Apostille Convention member; full consular "
            "authentication of Canadian-issued documents is required for "
            "use in the HKSAR. "
            "(Canadian Consulate General Hong Kong, 2025; Hong Kong "
            "Immigration Department Births and Deaths Registry, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'hong-kong',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has active business and diplomatic relations with "
            "Hong Kong; the German Consulate General in Hong Kong serves "
            "a significant German business community on the island. When "
            "a German national with Hong Kong connections dies in Germany "
            "and their family wishes to repatriate remains to Hong Kong, "
            "the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde is issued in German and requires "
            "certified English or Chinese translation and authentication "
            "by the German Consulate General in Hong Kong. Hong Kong SAR "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(German Consulate General Hong Kong, 2025; Hong Kong "
            "Immigration Department Births and Deaths Registry, 2025.)"
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
    raise SystemExit(main())
