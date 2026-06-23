#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R79-R80.

   R79 (25 routes, START_VARIANT=2=C):
     Norway x5:      united-kingdom, united-states, germany, france, australia
     Denmark x5:     united-kingdom, united-states, germany, france, australia
     Finland x5:     united-kingdom, united-states, germany, france, australia
     Netherlands x5: united-kingdom, united-states, australia, canada, ireland
     Switzerland x5: united-kingdom, united-states, australia, canada, ireland

   R80 (25 routes, continues from R79, START same cycle):
     Germany x5:     united-kingdom, united-states, france, australia, canada
     France x5:      united-kingdom, united-states, germany, australia, canada
     Australia x5:   united-kingdom, united-states, germany, france, canada
     New Zealand x5: united-kingdom, united-states, ireland, norway, denmark
     South Korea x5: united-kingdom, united-states, ireland, norway, denmark

   Template rotation: R78 ended on A. After processing au-to-sweden (index 49 in R77-R78,
   variant_idx ended at 50+1=51 after increment => next is 51%5=1=B).
   But actual files confirm uk-to-norway starts at C (variant_idx=2). R79 START_VARIANT=2.
   Each route increments variant_idx by 1. R79 ends at variant_idx=27 (27%5=2=C for first R80 route).
   R80 also starts at C. Rotation: C,D,E,A,B repeating.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 2  # C

DEST_META = {
    'norway': {
        'name': 'Norway',
        'slug': 'norway',
        'key': 'no',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Norwegian funeral director takes custody at Oslo Gardermoen "
            "Airport (OSL) cargo terminal, or at Bergen Airport (BGO) or "
            "Stavanger Airport (SVG) if the final destination is in western "
            "Norway. Death registration in Norway is handled by Folkeregisteret "
            "(the civil registration system administered by the Norwegian Tax "
            "Administration / Skatteetaten). The dodsattest (death certificate) "
            "is issued in Norwegian. Foreign death certificates must be "
            "apostilled and accompanied by a certified Norwegian translation "
            "where not already in Norwegian. The police take jurisdiction for "
            "violent or unexplained deaths and must close their investigation "
            "before the body can be released. Note that deaths occurring in "
            "Svalbard require transfer to mainland Norway before any "
            "international cargo flight can depart. Norway joined the Hague "
            "Apostille Convention in 1980; apostille certificates from member "
            "states are accepted. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(Folkeregisteret, Skatteetaten, Norway, 2025; FCDO Travel "
            "Advice: Norway, 2025.)"
        ),
        'consular_template': (
            "The Norwegian Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Norway. Norway "
            "joined the Hague Apostille Convention in 1980. The Embassy "
            "cannot pay for or arrange repatriation. Contact Folkeregisteret "
            "(Skatteetaten) for civil registration queries. Note that deaths "
            "in Svalbard require transfer to mainland Norway first."
        ),
        'arrival_faq': (
            "The Norwegian funeral director takes custody at Oslo Gardermoen "
            "(OSL), Bergen (BGO), or another cargo terminal depending on the "
            "final destination. Folkeregisteret registers the death. Foreign "
            "death certificates must be apostilled and accompanied by a "
            "certified Norwegian translation where not already in Norwegian. "
            "The police handle violent or unexplained deaths and must release "
            "the body before preparation proceeds. Svalbard deaths require "
            "mainland transfer first. Norway joined the Hague Apostille "
            "Convention in 1980. An embalming certificate and hermetically "
            "sealed coffin are required."
        ),
        'emergency_line': 'contact the Norwegian Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-norway',
    },
    'denmark': {
        'name': 'Denmark',
        'slug': 'denmark',
        'key': 'dk',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Danish funeral director takes custody at Copenhagen Kastrup "
            "Airport (CPH) cargo terminal. For deaths in Jutland, Billund "
            "Airport (BLL) or Aarhus Airport (AAR) may be used depending on "
            "the final destination. Death registration in Denmark is handled "
            "by the local municipality (kommunen), which enters the death "
            "into the CPR-registret (the national civil registration system). "
            "The dodsattest is issued in Danish. Foreign death certificates "
            "must be apostilled and accompanied by a certified Danish "
            "translation where not already in Danish. The police and "
            "retsmediciner (forensic medical examiner) take jurisdiction "
            "for violent or unexplained deaths. Denmark joined the Hague "
            "Apostille Convention in 1978; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Danish CPR-registret / kommunen, 2025; FCDO Travel Advice: "
            "Denmark, 2025.)"
        ),
        'consular_template': (
            "The Danish Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Denmark. Denmark "
            "joined the Hague Apostille Convention in 1978. The Embassy "
            "cannot pay for or arrange repatriation. Contact the local "
            "kommunen and CPR-registret for civil registration queries."
        ),
        'arrival_faq': (
            "The Danish funeral director takes custody at Copenhagen Kastrup "
            "(CPH) or the relevant regional airport cargo terminal. The local "
            "kommunen enters the death into the CPR-registret. Foreign "
            "death certificates must be apostilled and accompanied by a "
            "certified Danish translation where not already in Danish. The "
            "police and retsmediciner handle violent or unexplained deaths. "
            "Denmark joined the Hague Apostille Convention in 1978. An "
            "embalming certificate and hermetically sealed coffin are required. "
            "The receiving funeral director coordinates with the kommunen."
        ),
        'emergency_line': 'contact the Danish Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-denmark',
    },
    'finland': {
        'name': 'Finland',
        'slug': 'finland',
        'key': 'fi',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Finnish funeral director takes custody at Helsinki-Vantaa "
            "Airport (HEL) cargo terminal, or at Tampere (TMP) or Turku (TKU) "
            "Airport depending on the final destination. Death registration in "
            "Finland is handled by the Digital and Population Data Services "
            "Agency (DVV / Digi- ja vaestovirasto), which maintains the "
            "Population Information System. The kuolintodistus (death "
            "certificate) is issued in Finnish, Swedish, or both. Foreign "
            "death certificates must be apostilled and, where not in Finnish "
            "or Swedish, accompanied by a certified translation for DVV. The "
            "police and medical examiner take jurisdiction for violent or "
            "unexplained deaths. Finland joined the Hague Apostille Convention "
            "in 2009; apostille certificates from member states are accepted. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(DVV / Digi- ja vaestovirasto, Finland, 2025; FCDO Travel "
            "Advice: Finland, 2025.)"
        ),
        'consular_template': (
            "The Finnish Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Finland. Finland "
            "joined the Hague Apostille Convention in 2009. The Embassy "
            "cannot pay for or arrange repatriation. Contact the DVV "
            "(Digital and Population Data Services Agency) for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Finnish funeral director takes custody at Helsinki-Vantaa "
            "(HEL) or the relevant regional airport cargo terminal. The DVV "
            "(Digi- ja vaestovirasto) handles civil registration. Foreign "
            "death certificates must be apostilled and accompanied by a "
            "certified Finnish or Swedish translation where not already in "
            "those languages. The police and medical examiner handle violent "
            "or unexplained deaths. Finland joined the Hague Apostille "
            "Convention in 2009. An embalming certificate and hermetically "
            "sealed coffin are required. The receiving funeral director "
            "coordinates with the DVV."
        ),
        'emergency_line': 'contact the Finnish Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-finland',
    },
    'netherlands': {
        'name': 'the Netherlands',
        'slug': 'netherlands',
        'key': 'nl',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Dutch funeral director takes custody at Amsterdam Schiphol "
            "Airport (AMS) cargo terminal. For destinations in southern "
            "Netherlands, Rotterdam The Hague Airport (RTM) or Eindhoven "
            "Airport (EIN) may be used. Death registration in the Netherlands "
            "is handled by the local municipality (gemeente), which registers "
            "the death in the Basisregistratie Personen (BRP, the personal "
            "records database). The akte van overlijden (death certificate) "
            "is issued by the gemeente. Foreign death certificates must be "
            "apostilled and, where not in Dutch, accompanied by a certified "
            "Dutch translation for the gemeente. The officier van justitie "
            "(public prosecutor) is notified for violent or unexplained "
            "deaths. The Netherlands joined the Hague Apostille Convention "
            "in 1960; apostille certificates from member states are accepted. "
            "An embalming certificate and hermetically sealed coffin are "
            "required for all air imports. "
            "(Basisregistratie Personen BRP, Gemeente, Netherlands, 2025; "
            "FCDO Travel Advice: Netherlands, 2025.)"
        ),
        'consular_template': (
            "The Netherlands Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to the Netherlands. "
            "The Netherlands joined the Hague Apostille Convention in 1960. "
            "The Embassy cannot pay for or arrange repatriation. Contact the "
            "receiving gemeente for civil registration queries."
        ),
        'arrival_faq': (
            "The Dutch funeral director takes custody at Amsterdam Schiphol "
            "(AMS) or the relevant regional airport cargo terminal. The "
            "gemeente registers the death in the Basisregistratie Personen "
            "(BRP). Foreign death certificates must be apostilled and "
            "accompanied by a certified Dutch translation where not already "
            "in Dutch. The officier van justitie handles violent or unexplained "
            "deaths. The Netherlands joined the Hague Apostille Convention in "
            "1960. An embalming certificate and hermetically sealed coffin "
            "are required. The receiving funeral director coordinates with "
            "the local gemeente."
        ),
        'emergency_line': 'contact the Netherlands Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-netherlands',
    },
    'switzerland': {
        'name': 'Switzerland',
        'slug': 'switzerland',
        'key': 'ch',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Swiss funeral director takes custody at Zurich Airport "
            "(ZRH) or Geneva Airport (GVA) cargo terminal, or at EuroAirport "
            "Basel Mulhouse (BSL/MLH) depending on the final destination. "
            "Death registration in Switzerland is handled by the Zivilstandsamt "
            "(civil registry office) in the canton where the death is "
            "registered. Switzerland has four official languages: German, "
            "French, Italian, and Romansh. The Todesurkunde (death "
            "certificate) is issued in the language of the relevant canton. "
            "Foreign death certificates must be apostilled and accompanied "
            "by a certified translation into the language of the receiving "
            "canton where not already in the appropriate language. The "
            "cantonal public prosecutor (Staatsanwaltschaft) takes "
            "jurisdiction for violent or unexplained deaths. Switzerland "
            "joined the Hague Apostille Convention in 1972; apostille "
            "certificates from member states are accepted. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Zivilstandsamt, Federal Civil Registry Office, Switzerland, "
            "2025; FCDO Travel Advice: Switzerland, 2025.)"
        ),
        'consular_template': (
            "The Swiss Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Switzerland. "
            "Switzerland joined the Hague Apostille Convention in 1972. "
            "The Embassy cannot pay for or arrange repatriation. Contact "
            "the Zivilstandsamt in the receiving canton for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Swiss funeral director takes custody at Zurich (ZRH), "
            "Geneva (GVA), or Basel (BSL) cargo terminal. The Zivilstandsamt "
            "(civil registry office) in the receiving canton registers the "
            "death. Foreign death certificates must be apostilled and "
            "accompanied by a certified translation into the language of "
            "the relevant canton (German, French, or Italian). The cantonal "
            "Staatsanwaltschaft handles violent or unexplained deaths. "
            "Switzerland joined the Hague Apostille Convention in 1972. "
            "An embalming certificate and hermetically sealed coffin are "
            "required. The receiving funeral director coordinates with the "
            "local Zivilstandsamt."
        ),
        'emergency_line': 'contact the Swiss Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-switzerland',
    },
    'germany': {
        'name': 'Germany',
        'slug': 'germany',
        'key': 'de',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The German funeral director takes custody at Frankfurt Airport "
            "(FRA), Munich Airport (MUC), or Berlin Brandenburg Airport (BER) "
            "cargo terminal, depending on the final destination. Death "
            "registration in Germany is handled by the local Standesamt "
            "(civil registry office) in the municipality where the death "
            "is registered. The Sterbeurkunde (death certificate) is issued "
            "in German. Foreign death certificates must be apostilled and, "
            "where not in German, accompanied by a certified German "
            "translation (beglaubigte Ubersetzung) for the Standesamt. "
            "The Staatsanwaltschaft (public prosecutor) takes jurisdiction "
            "for violent or unexplained deaths. Germany joined the Hague "
            "Apostille Convention in 1965; apostille certificates from "
            "member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(Standesamt, Bundesministerium des Innern, Germany, 2025; "
            "FCDO Travel Advice: Germany, 2025.)"
        ),
        'consular_template': (
            "The German Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to Germany. Germany "
            "joined the Hague Apostille Convention in 1965. The Embassy "
            "cannot pay for or arrange repatriation. Contact the Standesamt "
            "in the receiving municipality for civil registration queries."
        ),
        'arrival_faq': (
            "The German funeral director takes custody at the receiving "
            "airport cargo terminal. The local Standesamt registers the "
            "death and issues the Sterbeurkunde. Foreign death certificates "
            "must be apostilled and accompanied by a certified German "
            "translation (beglaubigte Ubersetzung). The Staatsanwaltschaft "
            "handles violent or unexplained deaths. Germany joined the Hague "
            "Apostille Convention in 1965. An embalming certificate and "
            "hermetically sealed coffin are required. The receiving funeral "
            "director coordinates with the local Standesamt."
        ),
        'emergency_line': 'contact the German Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-germany',
    },
    'france': {
        'name': 'France',
        'slug': 'france',
        'key': 'fr',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The French funeral director takes custody at Paris Charles de "
            "Gaulle Airport (CDG), Paris Orly (ORY), Nice Airport (NCE), "
            "or another cargo terminal depending on the final destination. "
            "Death registration in France is handled by the mairie (town hall) "
            "in the municipality where the death is registered. The acte de "
            "deces is issued in French. Foreign death certificates must be "
            "apostilled and, where not in French, accompanied by a certified "
            "French translation for the mairie. The Procureur de la Republique "
            "(public prosecutor) takes jurisdiction for violent or unexplained "
            "deaths. France joined the Hague Apostille Convention in 1960; "
            "apostille certificates from member states are accepted. An "
            "embalming certificate and hermetically sealed coffin are required "
            "for all air imports; French regulations on embalming must be "
            "observed. "
            "(Mairie / direction des affaires civiles, France, 2025; FCDO "
            "Travel Advice: France, 2025.)"
        ),
        'consular_template': (
            "The French Embassy or Consulate in {city} can advise on "
            "documentation requirements for repatriation to France. France "
            "joined the Hague Apostille Convention in 1960. The Embassy "
            "cannot pay for or arrange repatriation. Contact the mairie "
            "in the receiving municipality for civil registration queries."
        ),
        'arrival_faq': (
            "The French funeral director takes custody at the receiving "
            "airport cargo terminal. The local mairie registers the death "
            "and issues the acte de deces. Foreign death certificates must "
            "be apostilled and accompanied by a certified French translation "
            "where not already in French. The Procureur de la Republique "
            "handles violent or unexplained deaths. France joined the Hague "
            "Apostille Convention in 1960. An embalming certificate and "
            "hermetically sealed coffin are required; French embalming "
            "regulations apply. The receiving funeral director coordinates "
            "with the local mairie."
        ),
        'emergency_line': 'contact the French Embassy or Consulate in the origin country',
        'hub_url': 'repatriation-from-france',
    },
    'australia': {
        'name': 'Australia',
        'slug': 'australia',
        'key': 'au',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The Australian funeral director takes custody at Sydney "
            "Kingsford Smith Airport (SYD), Melbourne Airport (MEL), Brisbane "
            "Airport (BNE), or Perth Airport (PER) cargo terminal, depending "
            "on the family's destination. Death registration in Australia is "
            "handled by the state or territory Births, Deaths and Marriages "
            "(BDM) registry. The Australian death certificate is issued in "
            "English. Foreign death certificates must be apostilled and, "
            "where not in English, accompanied by a certified English "
            "translation for the receiving BDM registry. The coroner takes "
            "jurisdiction for sudden, violent, or unexplained deaths under "
            "the relevant state or territory Coroners Act. Australian Customs "
            "clearance (operated by the Australian Border Force) is required "
            "for all imported human remains. Australia joined the Hague "
            "Apostille Convention in 1995; apostille certificates from member "
            "states are accepted. An embalming certificate and hermetically "
            "sealed coffin are required for all air imports. "
            "(State and Territory BDM Registries, Australia, 2025; Australian "
            "Border Force, 2025; FCDO Travel Advice: Australia, 2025.)"
        ),
        'consular_template': (
            "The Australian High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Australia. "
            "Australia joined the Hague Apostille Convention in 1995. The "
            "High Commission cannot pay for or arrange repatriation. Contact "
            "the relevant state or territory BDM registry for civil "
            "registration queries. Australian Border Force clearance is "
            "required for all imported human remains."
        ),
        'arrival_faq': (
            "The Australian funeral director takes custody at the receiving "
            "state or territory airport cargo terminal. The state or territory "
            "BDM (Births, Deaths and Marriages) registry registers the death. "
            "Foreign death certificates must be apostilled and accompanied by "
            "a certified English translation where not already in English. "
            "The coroner handles sudden, violent, or unexplained deaths under "
            "state or territory legislation. Australian Border Force clearance "
            "is required. Australia joined the Hague Apostille Convention in "
            "1995. An embalming certificate and hermetically sealed coffin "
            "are required. The receiving funeral director coordinates with "
            "the local BDM registry."
        ),
        'emergency_line': 'contact the Australian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-australia',
    },
    'new-zealand': {
        'name': 'New Zealand',
        'slug': 'new-zealand',
        'key': 'nz',
        'complexity_override': 'low',
        'timeline_avg_override': '2-4 weeks',
        'timeline_fast_override': '10-14 days',
        'timeline_complex_override': '4-8 weeks',
        'reception': (
            "The New Zealand funeral director takes custody at Auckland "
            "International Airport (AKL), Wellington Airport (WLG), or "
            "Christchurch Airport (CHC) cargo terminal, depending on the "
            "family's destination. Death registration in New Zealand is "
            "handled by the Births, Deaths and Marriages (BDM) office "
            "within the Department of Internal Affairs (Te Tari Taiwhenua). "
            "The death must be registered under the Births, Deaths, Marriages, "
            "and Relationships Registration Act 2021. The Coroner may need "
            "to be notified under the Coroners Act 2006 for sudden or "
            "unexplained deaths. All foreign documentation must be "
            "authenticated for import. New Zealand Customs clearance is "
            "required for all imported human remains. New Zealand joined "
            "the Hague Apostille Convention in 2001; apostille certificates "
            "from member states are accepted. An embalming certificate and "
            "hermetically sealed coffin are required for all air imports. "
            "(New Zealand BDM / Department of Internal Affairs, 2025; "
            "New Zealand Customs Service, 2025; FCDO Travel Advice: "
            "New Zealand, 2025.)"
        ),
        'consular_template': (
            "The New Zealand High Commission or Embassy responsible for "
            "{city} can advise on documentation requirements for repatriation "
            "to New Zealand. New Zealand joined the Hague Apostille Convention "
            "in 2001. The High Commission cannot pay for or arrange "
            "repatriation. Contact New Zealand BDM (Department of Internal "
            "Affairs) for civil registration queries. New Zealand MFAT "
            "emergency line: +64 4 439 8000 (24 hours)."
        ),
        'arrival_faq': (
            "The New Zealand funeral director takes custody at Auckland (AKL), "
            "Wellington (WLG), or Christchurch (CHC) cargo terminal. The BDM "
            "office within the Department of Internal Affairs registers the "
            "death under the Births, Deaths, Marriages, and Relationships "
            "Registration Act 2021. The Coroner may be notified for sudden "
            "or unexplained deaths. New Zealand Customs clearance is required. "
            "New Zealand joined the Hague Apostille Convention in 2001. An "
            "embalming certificate and hermetically sealed coffin are required. "
            "The receiving funeral director coordinates with the local BDM "
            "office and Customs."
        ),
        'emergency_line': 'contact the New Zealand High Commission or Embassy responsible for the origin country. New Zealand MFAT emergency line: +64 4 439 8000',
        'hub_url': 'repatriation-from-new-zealand',
    },
    'south-korea': {
        'name': 'South Korea',
        'slug': 'south-korea',
        'key': 'kr',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '14-21 days',
        'timeline_complex_override': '8-16 weeks',
        'reception': (
            "The Korean funeral director (jang-ye-jido-sa) takes custody "
            "at Incheon International Airport (ICN) cargo terminal, or at "
            "Gimhae International Airport (PUS) for destinations in the "
            "south of the country. The local gu office (ward office) "
            "registers the death and a jang-ui-hwakinjung (burial or "
            "cremation confirmation certificate) is required before final "
            "disposition. South Korea is not a member of the Hague Apostille "
            "Convention; all foreign documents must be authenticated through "
            "Korean embassy channels in the country of origin and then "
            "legalised by the South Korean Ministry of Foreign Affairs. "
            "A certified Korean translation is required for all non-Korean "
            "documentation. Korean Ministry of Foreign Affairs 24-hour "
            "emergency line: +82 2 3210 0404. "
            "(Korean Ministry of Foreign Affairs, 2025; Gu office / ward "
            "office civil registration, South Korea, 2025.)"
        ),
        'consular_template': (
            "The Embassy of the Republic of Korea in {city} can advise on "
            "documentation requirements for repatriation to South Korea. "
            "South Korea is not a Hague Apostille member; all foreign "
            "documents require authentication through the Korean Embassy in "
            "the origin country followed by Ministry of Foreign Affairs "
            "legalisation in Seoul. The Embassy cannot pay for or arrange "
            "repatriation. Korean Ministry of Foreign Affairs emergency "
            "line: +82 2 3210 0404."
        ),
        'arrival_faq': (
            "The Korean funeral director takes custody at Incheon (ICN) or "
            "Gimhae (PUS) cargo terminal. The gu office (ward office) "
            "registers the death. A jang-ui-hwakinjung (burial or cremation "
            "confirmation certificate) is required before final disposition. "
            "South Korea is not a Hague Apostille Convention member; all "
            "foreign documents require authentication through Korean embassy "
            "channels in the country of origin and then Ministry of Foreign "
            "Affairs legalisation in Seoul. A certified Korean translation "
            "is required. Korean Ministry of Foreign Affairs emergency line: "
            "+82 2 3210 0404."
        ),
        'emergency_line': 'contact the Korean Embassy or Consulate in the origin country. Korean Ministry of Foreign Affairs emergency line: +82 2 3210 0404',
        'hub_url': 'repatriation-from-south-korea',
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
    'denmark': {
        'name': 'Denmark',
        'emergency': '112',
        'registry': 'the local kommunen (municipality) via the CPR-registret',
        'cert_name': 'dodsattest (death certificate)',
        'cert_lang': 'Danish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician. "
            "The dodsattest is registered with the local kommunen (municipality), "
            "which enters the death into the CPR-registret (national civil "
            "registration system). The police and retsmediciner (forensic "
            "medical examiner) take jurisdiction for violent or unexplained "
            "deaths. Denmark is a Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': "Cremation in Denmark is widely available.",
        'postmortem_trigger': 'Violent or unexplained deaths (police and retsmediciner take jurisdiction)',
    },
}

ROUTES = [
    # R79 -- Norway x5
    {
        'origin': 'united-kingdom', 'dest': 'norway',
        'embassy_city': 'London',
        'intro': (
            "Norway and the United Kingdom share close bilateral ties rooted "
            "in history, trade, and the Second World War. British nationals "
            "work in Norway across the oil and gas sector, maritime industries, "
            "and international organisations in Oslo. Norway is also a popular "
            "destination for British tourists visiting the fjords, the northern "
            "lights, and the mountain regions. The British Embassy in Oslo is "
            "fully operational. When someone from the United Kingdom dies and "
            "their family wishes to repatriate remains to Norway, the death "
            "must be registered at the local register office in England and "
            "Wales within 5 days, or with the National Records of Scotland or "
            "GRONI in Northern Ireland. The UK death certificate is apostilled; "
            "Norway joined the Hague Apostille Convention in 1980. The Norwegian "
            "Embassy in London can advise on documentation requirements for "
            "Folkeregisteret. "
            "(FCDO Travel Advice: Norway, 2025; Folkeregisteret, Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'norway',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has one of the world's largest Norwegian-heritage "
            "communities, concentrated in Minnesota, Wisconsin, North Dakota, "
            "and the Pacific Northwest, reflecting the large Norwegian emigration "
            "of the 19th and early 20th centuries. American nationals also work "
            "in Norway in oil and gas, technology, and international business. "
            "The Norwegian Embassy in Washington DC is fully operational. When "
            "a person with Norwegian family connections dies in the United States, "
            "the death is registered with the state civil records office. The "
            "Norwegian Embassy in Washington DC can advise on documentation "
            "requirements for Folkeregisteret. Both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Norway, 2025; Folkeregisteret, Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'norway',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Norway maintain active bilateral ties as European "
            "neighbours and close trade partners, with Norway as one of "
            "Germany's largest energy suppliers. German nationals work in "
            "Norway's oil and gas sector and in maritime industries, and "
            "Norway is a popular holiday destination for German tourists. "
            "The Norwegian Embassy in Berlin is fully operational. When a "
            "person with Norwegian family connections dies in Germany, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde requires a certified Norwegian translation for "
            "Folkeregisteret. Both countries are Hague Apostille Convention "
            "members. "
            "(FCDO Travel Advice: Norway, 2025; Folkeregisteret, Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'norway',
        'embassy_city': 'Paris',
        'intro': (
            "France and Norway maintain bilateral ties as NATO allies and "
            "European trade partners. French nationals work in Norway in "
            "international organisations, the energy sector, and professional "
            "services. Norway is a destination for French tourists on "
            "Scandinavian itineraries. The Norwegian Embassy in Paris is "
            "fully operational. When a person with Norwegian family connections "
            "dies in France, the death is registered with the local mairie "
            "(town hall). The acte de deces requires a certified Norwegian "
            "translation for Folkeregisteret. Both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Norway, 2025; Folkeregisteret, Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'norway',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a Norwegian-heritage community reflecting 19th and "
            "early 20th century migration, with Australian nationals of Norwegian "
            "descent maintaining family connections in Norway. Norway is also a "
            "destination for Australian tourists on Scandinavian and Arctic "
            "itineraries. The Norwegian Embassy in Canberra is operational. "
            "When a person with Norwegian family connections dies in Australia, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Both countries are Hague Apostille "
            "Convention members; Norway joined in 1980. "
            "(FCDO Travel Advice: Norway, 2025; Folkeregisteret, Skatteetaten, "
            "Norway, 2025.)"
        ),
    },
    # R79 -- Denmark x5
    {
        'origin': 'united-kingdom', 'dest': 'denmark',
        'embassy_city': 'London',
        'intro': (
            "Denmark and the United Kingdom share close bilateral ties, "
            "deep historical connections including Viking history and the "
            "North Sea region, and a mutual British and Danish presence in "
            "each other's countries. British nationals live and work in "
            "Denmark across pharmaceuticals, shipping, and professional "
            "services in Copenhagen and Aarhus. The British Embassy in "
            "Copenhagen is fully operational. When someone from the United "
            "Kingdom dies and their family wishes to repatriate remains to "
            "Denmark, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The UK death "
            "certificate is apostilled; Denmark joined the Hague Apostille "
            "Convention in 1978. The Danish Embassy in London can advise on "
            "documentation requirements for the CPR-registret. "
            "(FCDO Travel Advice: Denmark, 2025; Danish CPR-registret, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'denmark',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Denmark maintain active bilateral ties "
            "as NATO allies and trade partners. American nationals work in "
            "Denmark in pharmaceutical, shipping, and international business "
            "sectors. The Danish Embassy in Washington DC is fully operational. "
            "When a person with Danish family connections dies in the United "
            "States, the death is registered with the state civil records "
            "office. The Danish Embassy in Washington DC can advise on "
            "documentation requirements for the CPR-registret. Both countries "
            "are Hague Apostille Convention members; Denmark joined in 1978. "
            "(FCDO Travel Advice: Denmark, 2025; Danish CPR-registret, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'denmark',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Denmark share a land border and one of the most "
            "active cross-border migration corridors in northern Europe. "
            "A German-speaking minority community has historically existed "
            "in southern Denmark (Schleswig), and cross-border family ties "
            "are common. The Danish Embassy in Berlin is fully operational. "
            "When a person with Danish family connections dies in Germany, "
            "the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde requires a certified Danish "
            "translation for the CPR-registret. Both countries are Hague "
            "Apostille Convention members. "
            "(FCDO Travel Advice: Denmark, 2025; Danish CPR-registret, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'denmark',
        'embassy_city': 'Paris',
        'intro': (
            "France and Denmark maintain bilateral diplomatic ties as EU "
            "and NATO partners. French nationals work in Denmark in "
            "pharmaceutical and professional sectors, and Copenhagen attracts "
            "French cultural visitors. The Danish Embassy in Paris is fully "
            "operational. When a person with Danish family connections dies "
            "in France, the death is registered with the local mairie (town "
            "hall). The acte de deces requires a certified Danish translation "
            "for the CPR-registret. Both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Denmark, 2025; Danish CPR-registret, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'denmark',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Denmark maintain bilateral ties, and Australian "
            "nationals of Danish heritage have family connections in Denmark "
            "reflecting 19th and early 20th century migration. Denmark is "
            "also a destination for Australian tourists on Scandinavian "
            "itineraries. The Danish Embassy in Canberra is operational. "
            "When a person with Danish family connections dies in Australia, "
            "the death is registered with the state or territory Births, "
            "Deaths and Marriages (BDM) registry. Both countries are Hague "
            "Apostille Convention members; Denmark joined in 1978. "
            "(FCDO Travel Advice: Denmark, 2025; Danish CPR-registret, 2025.)"
        ),
    },
    # R79 -- Finland x5
    {
        'origin': 'united-kingdom', 'dest': 'finland',
        'embassy_city': 'London',
        'intro': (
            "Finland and the United Kingdom maintain close bilateral ties as "
            "EU and NATO partners. British nationals work in Finland across "
            "technology, gaming, and international professional sectors, "
            "with a concentration in Helsinki. Finland joined NATO in April "
            "2023, strengthening security ties with the UK. The British "
            "Embassy in Helsinki is fully operational. When someone from the "
            "United Kingdom dies and their family wishes to repatriate remains "
            "to Finland, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The UK death "
            "certificate is apostilled; Finland joined the Hague Apostille "
            "Convention in 2009. The Finnish Embassy in London can advise on "
            "documentation requirements for the DVV. "
            "(FCDO Travel Advice: Finland, 2025; DVV / Digi- ja vaestovirasto, "
            "Finland, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'finland',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Finland have deepened bilateral security "
            "and trade ties since Finland's NATO accession in April 2023. "
            "American nationals are present in Finland across technology, "
            "defence, and international organisations. The Finnish Embassy "
            "in Washington DC is fully operational. When a person with Finnish "
            "family connections dies in the United States, the death is "
            "registered with the state civil records office. The Finnish "
            "Embassy in Washington DC can advise on documentation requirements "
            "for the DVV. Both countries are Hague Apostille Convention "
            "members; Finland joined in 2009. "
            "(FCDO Travel Advice: Finland, 2025; DVV / Digi- ja vaestovirasto, "
            "Finland, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'finland',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and Finland are EU partners with active bilateral trade "
            "and cultural ties. German nationals visit Finland for Lapland "
            "tourism and the midnight sun, and German companies are active "
            "in Finland's industrial and technology sectors. The Finnish "
            "Embassy in Berlin is fully operational. When a person with "
            "Finnish family connections dies in Germany, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde requires a certified Finnish or Swedish translation "
            "for the DVV. Both countries are Hague Apostille Convention "
            "members; Finland joined in 2009. "
            "(FCDO Travel Advice: Finland, 2025; DVV / Digi- ja vaestovirasto, "
            "Finland, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'finland',
        'embassy_city': 'Paris',
        'intro': (
            "France and Finland are EU and NATO allies with active bilateral "
            "ties. French nationals visit Finland for Arctic tourism, and "
            "Finnish nationals are present in France in academic and "
            "professional contexts. The Finnish Embassy in Paris is fully "
            "operational. When a person with Finnish family connections dies "
            "in France, the death is registered with the local mairie (town "
            "hall). The acte de deces requires a certified Finnish or Swedish "
            "translation for the DVV. Both countries are Hague Apostille "
            "Convention members; Finland joined in 2009. "
            "(FCDO Travel Advice: Finland, 2025; DVV / Digi- ja vaestovirasto, "
            "Finland, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'finland',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a small Finnish-heritage community reflecting "
            "mid-20th century migration, with Australian nationals of Finnish "
            "descent maintaining family connections in Finland. Finland is a "
            "destination for Australian tourists visiting Lapland and the "
            "Arctic. The Finnish Embassy in Canberra is operational. When a "
            "person with Finnish family connections dies in Australia, the "
            "death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Both countries are Hague Apostille "
            "Convention members; Finland joined in 2009. "
            "(FCDO Travel Advice: Finland, 2025; DVV / Digi- ja vaestovirasto, "
            "Finland, 2025.)"
        ),
    },
    # R79 -- Netherlands x5
    {
        'origin': 'united-kingdom', 'dest': 'netherlands',
        'embassy_city': 'London',
        'intro': (
            "The Netherlands is home to one of the largest British expatriate "
            "communities in continental Europe. British nationals are established "
            "in Amsterdam, Rotterdam, The Hague, and Eindhoven across finance, "
            "technology, and professional services. The Hague hosts the "
            "International Court of Justice and the International Criminal Court, "
            "with a significant British legal and diplomatic presence. The "
            "British Embassy in The Hague is fully operational. When someone "
            "from the United Kingdom dies and their family wishes to repatriate "
            "remains to the Netherlands, the death must be registered at the "
            "local register office in England and Wales within 5 days, or with "
            "the National Records of Scotland or GRONI in Northern Ireland. "
            "Both countries are Hague Apostille Convention members. The "
            "Netherlands Embassy in London can advise on documentation for "
            "the receiving gemeente. "
            "(FCDO Travel Advice: Netherlands, 2025; BRP, Gemeente, "
            "Netherlands, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'netherlands',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and the Netherlands maintain a close bilateral "
            "relationship with deep historical roots in the Dutch settlement "
            "of New Amsterdam (now New York) and active present-day trade "
            "ties. The Netherlands hosts the headquarters of several major "
            "US multinationals and international organisations. The US Embassy "
            "in The Hague is fully operational. When a person with Dutch "
            "family connections dies in the United States, the death is "
            "registered with the state civil records office. The Netherlands "
            "Embassy in Washington DC can advise on documentation for the "
            "receiving gemeente. Both countries are Hague Apostille Convention "
            "members. "
            "(FCDO Travel Advice: Netherlands, 2025; BRP, Gemeente, "
            "Netherlands, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'netherlands',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has one of the largest Dutch-heritage communities "
            "outside the Netherlands, with several hundred thousand Australians "
            "of Dutch descent, reflecting substantial post-Second World War "
            "migration in the late 1940s and 1950s. The Australia-Netherlands "
            "repatriation corridor is among the most active from Australia "
            "to northern Europe. The Netherlands Embassy in Canberra is "
            "operational. When a person with Dutch family connections dies "
            "in Australia, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. Both countries are "
            "Hague Apostille Convention members. "
            "(FCDO Travel Advice: Netherlands, 2025; BRP, Gemeente, "
            "Netherlands, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'netherlands',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada and the Netherlands share a special relationship rooted "
            "in the liberation of the Netherlands by Canadian forces in 1944 "
            "and 1945. The Netherlands sends tulips to Ottawa each year as "
            "a symbol of gratitude, and the two countries maintain strong "
            "people-to-people ties. Canadian nationals with Dutch family "
            "connections maintain bilateral family links across generations. "
            "The Netherlands Embassy in Ottawa is fully operational. When a "
            "person with Dutch family connections dies in Canada, the death "
            "is registered with the provincial civil registration authority. "
            "Canada joined the Hague Apostille Convention, in force November "
            "2024; the Netherlands joined in 1960. "
            "(FCDO Travel Advice: Netherlands, 2025; BRP, Gemeente, "
            "Netherlands, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'netherlands',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and the Netherlands are EU partners with an active "
            "bilateral migration corridor. Irish nationals work in Amsterdam "
            "and other Dutch cities in financial services, technology, and "
            "professional roles. The Netherlands has become an increasingly "
            "popular destination for Irish professionals following the "
            "relocation of several multinationals within the EU. The "
            "Netherlands Embassy in Dublin is fully operational. When someone "
            "from Ireland dies and their family wishes to repatriate remains "
            "to the Netherlands, the death must be registered with the local "
            "civil registration service. Both countries are Hague Apostille "
            "Convention members. The Netherlands Embassy in Dublin can advise "
            "on documentation for the receiving gemeente. "
            "(FCDO Travel Advice: Netherlands, 2025; BRP, Gemeente, "
            "Netherlands, 2025.)"
        ),
    },
    # R79 -- Switzerland x5
    {
        'origin': 'united-kingdom', 'dest': 'switzerland',
        'embassy_city': 'London',
        'intro': (
            "Switzerland is home to one of the largest British communities "
            "in continental Europe, with British nationals established across "
            "Zurich, Geneva, Basel, and the Alpine regions. Geneva hosts "
            "major international organisations including the United Nations "
            "European headquarters and the WHO, with a substantial British "
            "professional presence. Switzerland is also a leading retirement "
            "and lifestyle destination for British nationals. The British "
            "Embassy in Bern is fully operational. When someone from the "
            "United Kingdom dies and their family wishes to repatriate remains "
            "to Switzerland, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. The UK death "
            "certificate is apostilled; Switzerland joined the Hague Apostille "
            "Convention in 1972. The Swiss Embassy in London can advise on "
            "documentation requirements for the Zivilstandsamt. "
            "(FCDO Travel Advice: Switzerland, 2025; Federal Civil Registry "
            "Office, Switzerland, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'switzerland',
        'embassy_city': 'Washington DC',
        'intro': (
            "Switzerland hosts the European headquarters or regional offices "
            "of many major US corporations in Zurich and Geneva, and Geneva "
            "houses the United Nations European headquarters and several "
            "other international organisations with American personnel. "
            "The US Embassy in Bern is fully operational. When a person "
            "with Swiss family connections dies in the United States, the "
            "death is registered with the state civil records office. The "
            "Swiss Embassy in Washington DC can advise on documentation "
            "requirements for the Zivilstandsamt. Both countries are Hague "
            "Apostille Convention members; Switzerland joined in 1972. "
            "(FCDO Travel Advice: Switzerland, 2025; Federal Civil Registry "
            "Office, Switzerland, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'switzerland',
        'embassy_city': 'Canberra',
        'intro': (
            "Australian nationals work in Switzerland in pharmaceutical, "
            "financial, and international organisation sectors. Switzerland "
            "is a destination for Australian tourists on Alpine and European "
            "itineraries, and a small Australian community is established "
            "in Geneva and Zurich. The Swiss Embassy in Canberra is "
            "operational. When a person with Swiss family connections dies "
            "in Australia, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. Both countries "
            "are Hague Apostille Convention members; Switzerland joined "
            "in 1972. A certified translation into the language of the "
            "receiving canton may be required for the Zivilstandsamt. "
            "(FCDO Travel Advice: Switzerland, 2025; Federal Civil Registry "
            "Office, Switzerland, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'switzerland',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada and Switzerland maintain bilateral ties through shared "
            "membership of international organisations headquartered in "
            "Geneva, including the United Nations and the International "
            "Committee of the Red Cross. Canadian nationals work in "
            "Switzerland's international sector and financial services. "
            "The Swiss Embassy in Ottawa is fully operational. When a "
            "person with Swiss family connections dies in Canada, the "
            "death is registered with the provincial civil registration "
            "authority. Canada joined the Hague Apostille Convention, "
            "in force November 2024; Switzerland joined in 1972. A "
            "certified translation into the language of the receiving "
            "canton may be required. "
            "(FCDO Travel Advice: Switzerland, 2025; Federal Civil Registry "
            "Office, Switzerland, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'switzerland',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and Switzerland maintain bilateral ties as European "
            "trade and research partners. Irish nationals work in Switzerland "
            "in pharmaceutical, financial, and international organisation "
            "sectors, particularly in Basel and Geneva. The Swiss Embassy "
            "in Dublin is fully operational. When someone from Ireland dies "
            "and their family wishes to repatriate remains to Switzerland, "
            "the death must be registered with the local civil registration "
            "service. Both countries are Hague Apostille Convention members; "
            "Switzerland joined in 1972. A certified translation into the "
            "language of the receiving canton may be required for the "
            "Zivilstandsamt. "
            "(FCDO Travel Advice: Switzerland, 2025; Federal Civil Registry "
            "Office, Switzerland, 2025.)"
        ),
    },
    # R80 -- Germany (as destination) x5
    {
        'origin': 'united-kingdom', 'dest': 'germany',
        'embassy_city': 'London',
        'intro': (
            "Germany is home to around 100,000 British nationals, concentrated "
            "in Berlin, Hamburg, Munich, and Frankfurt. British nationals work "
            "in Germany across technology, automotive, finance, and professional "
            "services. The UK-Germany migration corridor is among the most "
            "active in Europe, and many British families have dual connections "
            "to both countries. The British Embassy in Berlin is fully "
            "operational. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Germany, the death must "
            "be registered at the local register office in England and Wales "
            "within 5 days, or with the National Records of Scotland or GRONI "
            "in Northern Ireland. The UK death certificate is apostilled; "
            "both countries are Hague Apostille Convention members. The German "
            "Embassy in London can advise on documentation requirements for "
            "the Standesamt. A certified German translation is required. "
            "(FCDO Travel Advice: Germany, 2025; Standesamt, Bundesministerium "
            "des Innern, Germany, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'germany',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States maintains a large military and civilian "
            "presence in Germany, with US forces based at Ramstein, Grafenwoehr, "
            "and other installations, and a significant American civilian "
            "community in Frankfurt, Munich, and Berlin. German-Americans "
            "form one of the largest ancestry groups in the United States, "
            "and family ties between the two countries are extensive. The "
            "US Embassy in Berlin is fully operational. When a person with "
            "German family connections dies in the United States, the death "
            "is registered with the state civil records office. The German "
            "Embassy in Washington DC can advise on documentation requirements "
            "for the Standesamt. Both countries are Hague Apostille Convention "
            "members. "
            "(FCDO Travel Advice: Germany, 2025; Standesamt, Bundesministerium "
            "des Innern, Germany, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'germany',
        'embassy_city': 'Paris',
        'intro': (
            "France and Germany share a border and form the bilateral axis "
            "at the heart of the European Union. Cross-border migration between "
            "the two countries is one of the most active in Europe, with "
            "hundreds of thousands of French nationals living in Germany and "
            "German nationals in France. The France-Germany repatriation "
            "corridor is well-established. When a French national or a person "
            "with German family connections dies in France, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "requires a certified German translation (beglaubigte Ubersetzung) "
            "for the receiving Standesamt. Both countries are Hague Apostille "
            "Convention members. "
            "(FCDO Travel Advice: Germany, 2025; Standesamt, Bundesministerium "
            "des Innern, Germany, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'germany',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has a significant German-heritage community, with "
            "several hundred thousand Australians of German descent, reflecting "
            "migration across multiple generations including post-Second World "
            "War arrivals. The Australia-Germany repatriation corridor is used "
            "regularly. The German Embassy in Canberra is fully operational. "
            "When a person with German family connections dies in Australia, "
            "the death is registered with the state or territory Births, Deaths "
            "and Marriages (BDM) registry. Both countries are Hague Apostille "
            "Convention members. A certified German translation is required "
            "for the receiving Standesamt. "
            "(FCDO Travel Advice: Germany, 2025; Standesamt, Bundesministerium "
            "des Innern, Germany, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'germany',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada is home to over three million people of German heritage, "
            "concentrated in Ontario, the Prairie provinces, and British "
            "Columbia, reflecting migration waves across several generations. "
            "Canadian nationals of German descent maintain family connections "
            "in Germany, and bilateral ties between the two countries are "
            "strong. The German Embassy in Ottawa is fully operational. When "
            "a person with German family connections dies in Canada, the death "
            "is registered with the provincial civil registration authority. "
            "Canada joined the Hague Apostille Convention, in force November "
            "2024; Germany joined in 1965. A certified German translation "
            "is required for the receiving Standesamt. "
            "(FCDO Travel Advice: Germany, 2025; Standesamt, Bundesministerium "
            "des Innern, Germany, 2025.)"
        ),
    },
    # R80 -- France (as destination) x5
    {
        'origin': 'united-kingdom', 'dest': 'france',
        'embassy_city': 'London',
        'intro': (
            "France is home to an estimated 150,000 to 200,000 British "
            "nationals registered as residents, making it one of the largest "
            "concentrations of UK nationals abroad. British nationals are "
            "settled across Paris, Normandy, Brittany, the Dordogne, Provence, "
            "and the Cote d'Azur. The UK-France repatriation corridor is one "
            "of the highest volume in Europe. The British Embassy in Paris "
            "is fully operational. When someone from the United Kingdom dies "
            "and their family wishes to repatriate remains to France, the "
            "death must be registered at the local register office in England "
            "and Wales within 5 days, or with the National Records of Scotland "
            "or GRONI in Northern Ireland. The UK death certificate is "
            "apostilled; both countries are Hague Apostille Convention members. "
            "The French Embassy in London can advise on documentation "
            "requirements for the receiving mairie. "
            "(FCDO Travel Advice: France, 2025; Mairie civil registry, "
            "France, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'france',
        'embassy_city': 'Washington DC',
        'intro': (
            "France and the United States share a historic alliance dating "
            "to the American Revolution, and an enduring bilateral relationship "
            "in trade, culture, and security. An American community of over "
            "100,000 nationals is established in France, concentrated in Paris, "
            "the south of France, and the Bordeaux region. The US Embassy in "
            "Paris is among the largest American embassies in Europe. When a "
            "person with French family connections dies in the United States, "
            "the death is registered with the state civil records office. The "
            "French Embassy in Washington DC can advise on documentation "
            "requirements for the receiving mairie. Both countries are Hague "
            "Apostille Convention members. "
            "(FCDO Travel Advice: France, 2025; Mairie civil registry, "
            "France, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'france',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and France share a border and maintain the most active "
            "bilateral migration corridor in Europe. A large German community "
            "is established in France, particularly in Alsace, Paris, and the "
            "major cities. Many German nationals retire to or work in France, "
            "and the France-Germany repatriation corridor is well-established. "
            "When a German national or a person with French family connections "
            "dies in Germany, the death is registered with the local Standesamt "
            "(civil registry). The Sterbeurkunde requires a certified French "
            "translation for the receiving mairie. Both countries are Hague "
            "Apostille Convention members. "
            "(FCDO Travel Advice: France, 2025; Mairie civil registry, "
            "France, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'france',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and France share Pacific regional connections through "
            "New Caledonia and French Polynesia, and an active bilateral "
            "relationship. French nationals form a community in Australia, "
            "and Australian nationals with French family connections maintain "
            "bilateral ties across generations. The French Embassy in Canberra "
            "is fully operational. When a person with French family connections "
            "dies in Australia, the death is registered with the state or "
            "territory Births, Deaths and Marriages (BDM) registry. Both "
            "countries are Hague Apostille Convention members. A certified "
            "French translation is required for the receiving mairie. "
            "(FCDO Travel Advice: France, 2025; Mairie civil registry, "
            "France, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'france',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada and France maintain a close bilateral relationship "
            "rooted in the Francophone heritage of Quebec and the Acadian "
            "regions. The Elysee Treaty provisions extend to France-Quebec "
            "relations, and the two countries have an active cultural and "
            "institutional framework. Many French nationals live in Canada "
            "and many Canadians, particularly from Quebec, live in France. "
            "The French Embassy in Ottawa is fully operational. When a person "
            "with French family connections dies in Canada, the death is "
            "registered with the provincial civil registration authority. "
            "Canada joined the Hague Apostille Convention, in force November "
            "2024; France joined in 1960. The acte de deces is in French, "
            "which is one of Canada's two official languages. "
            "(FCDO Travel Advice: France, 2025; Mairie civil registry, "
            "France, 2025.)"
        ),
    },
    # R80 -- Australia (as destination) x5
    {
        'origin': 'united-kingdom', 'dest': 'australia',
        'embassy_city': 'London',
        'intro': (
            "Australia is home to over one million British-born residents, "
            "making it one of the largest concentrations of UK nationals "
            "anywhere in the world outside the United Kingdom itself. British "
            "nationals have settled across Sydney, Melbourne, Brisbane, Perth, "
            "and regional Australia across multiple generations. The UK-Australia "
            "repatriation corridor is one of the most active globally. The "
            "British High Commission in Canberra is fully operational, with "
            "additional consular offices in major cities. When someone from "
            "the United Kingdom dies and their family wishes to repatriate "
            "remains to Australia, the death must be registered at the local "
            "register office in England and Wales within 5 days, or with the "
            "National Records of Scotland or GRONI in Northern Ireland. Both "
            "countries are Hague Apostille Convention members. Australian "
            "Border Force clearance is required on arrival. "
            "(FCDO Travel Advice: Australia, 2025; State and Territory BDM "
            "Registries, Australia, 2025; Australian Border Force, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'australia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and Australia maintain a close bilateral "
            "alliance through the ANZUS treaty and the Five Eyes intelligence "
            "partnership. American nationals are established across all major "
            "Australian cities in technology, finance, and professional "
            "services, and the US-Australia migration corridor is active. "
            "The US Embassy in Canberra is fully operational. When a person "
            "with Australian family connections dies in the United States, "
            "the death is registered with the state civil records office. "
            "The Australian Embassy in Washington DC can advise on "
            "documentation requirements for the state or territory BDM "
            "registry. Both countries are Hague Apostille Convention members. "
            "Australian Border Force clearance is required on arrival. "
            "(FCDO Travel Advice: Australia, 2025; State and Territory BDM "
            "Registries, Australia, 2025; Australian Border Force, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'australia',
        'embassy_city': 'Berlin',
        'intro': (
            "Australia has a significant German-heritage community, with "
            "substantial German migration in the 19th century and again in "
            "the post-Second World War period. South Australia in particular "
            "has deep German cultural roots in the Barossa Valley and Hahndorf. "
            "The German Embassy in Canberra is fully operational. When a "
            "person with Australian family connections dies in Germany, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Australian Embassy in Berlin can advise on documentation "
            "requirements for the state or territory BDM registry. Both "
            "countries are Hague Apostille Convention members. Australian "
            "Border Force clearance is required on arrival. "
            "(FCDO Travel Advice: Australia, 2025; State and Territory BDM "
            "Registries, Australia, 2025; Australian Border Force, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'australia',
        'embassy_city': 'Paris',
        'intro': (
            "France and Australia share Pacific regional connections and "
            "an active bilateral relationship. French nationals are present "
            "in Australia across major cities, and Australian nationals of "
            "French heritage maintain bilateral ties. France and Australia "
            "also share defence and intelligence relationships in the Pacific. "
            "The French Embassy in Canberra is fully operational. When a "
            "person with Australian family connections dies in France, the "
            "death is registered with the local mairie (town hall). The "
            "Australian Embassy in Paris can advise on documentation "
            "requirements for the state or territory BDM registry. Both "
            "countries are Hague Apostille Convention members. Australian "
            "Border Force clearance is required on arrival. "
            "(FCDO Travel Advice: Australia, 2025; State and Territory BDM "
            "Registries, Australia, 2025; Australian Border Force, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'australia',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada and Australia share Commonwealth ties and a bilateral "
            "relationship characterised by reciprocal working holiday "
            "arrangements and active migration in both directions. Many "
            "Canadians and Australians live and work in each other's "
            "countries, particularly among young professionals. The "
            "Australian High Commission in Ottawa is fully operational. "
            "When a person with Australian family connections dies in "
            "Canada, the death is registered with the provincial civil "
            "registration authority. Both countries are Hague Apostille "
            "Convention members. Australian Border Force clearance is "
            "required on arrival. "
            "(FCDO Travel Advice: Australia, 2025; State and Territory BDM "
            "Registries, Australia, 2025; Australian Border Force, 2025.)"
        ),
    },
    # R80 -- New Zealand x5
    {
        'origin': 'united-kingdom', 'dest': 'new-zealand',
        'embassy_city': 'London',
        'intro': (
            "New Zealand is home to over 200,000 UK-born residents, one of "
            "the most established British communities in any country. The "
            "UK-New Zealand migration corridor is among the most active "
            "between any two countries, facilitated by shared language, "
            "cultural ties, and the long-running Working Holiday visa "
            "arrangement. The British High Commission in Wellington is fully "
            "operational. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to New Zealand, the death "
            "must be registered at the local register office in England and "
            "Wales within 5 days, or with the National Records of Scotland "
            "or GRONI in Northern Ireland. The UK death certificate is "
            "apostilled; both countries are Hague Apostille Convention members. "
            "The New Zealand High Commission in London can advise on "
            "documentation requirements. New Zealand Customs clearance is "
            "required on arrival. "
            "(FCDO Travel Advice: New Zealand, 2025; New Zealand BDM, "
            "Department of Internal Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'new-zealand',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States and New Zealand maintain an active bilateral "
            "relationship through the ANZUS framework and Five Eyes "
            "intelligence partnership, with American nationals present in "
            "New Zealand in technology, academia, and professional services. "
            "New Zealand is also a destination for American retirees and "
            "lifestyle migrants. The New Zealand Embassy in Washington DC "
            "is fully operational. When a person with New Zealand family "
            "connections dies in the United States, the death is registered "
            "with the state civil records office. The New Zealand Embassy "
            "in Washington DC can advise on documentation requirements. Both "
            "countries are Hague Apostille Convention members. New Zealand "
            "Customs clearance is required on arrival. "
            "(FCDO Travel Advice: New Zealand, 2025; New Zealand BDM, "
            "Department of Internal Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'new-zealand',
        'embassy_city': 'Dublin',
        'intro': (
            "New Zealand has a significant Irish diaspora community reflecting "
            "migration across generations, and the Ireland-New Zealand "
            "migration corridor remains active under the reciprocal Working "
            "Holiday arrangement. Irish nationals are established across "
            "Auckland, Wellington, Christchurch, and regional New Zealand. "
            "The New Zealand Embassy in Dublin is fully operational. When "
            "someone from Ireland dies and their family wishes to repatriate "
            "remains to New Zealand, the death must be registered with the "
            "local civil registration service. Both countries are Hague "
            "Apostille Convention members; New Zealand joined in 2001. New "
            "Zealand Customs clearance is required on arrival. "
            "(FCDO Travel Advice: New Zealand, 2025; New Zealand BDM, "
            "Department of Internal Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'new-zealand',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and New Zealand maintain bilateral ties, and a small "
            "Norwegian-heritage community is present in New Zealand reflecting "
            "historical migration. Norwegian nationals occasionally relocate "
            "to New Zealand, and family connections exist in both directions. "
            "The New Zealand High Commission in London also covers Norway "
            "for consular matters. The British Embassy in Oslo can assist "
            "British nationals in Norway. When a person with New Zealand "
            "family connections dies in Norway, the death is registered "
            "with Folkeregisteret (the civil registration system). The "
            "dodsattest requires a certified English translation for New "
            "Zealand authorities. Both countries are Hague Apostille "
            "Convention members. New Zealand Customs clearance is required "
            "on arrival. "
            "(FCDO Travel Advice: New Zealand, 2025; New Zealand BDM, "
            "Department of Internal Affairs, 2025; Folkeregisteret, "
            "Skatteetaten, Norway, 2025.)"
        ),
    },
    {
        'origin': 'denmark', 'dest': 'new-zealand',
        'embassy_city': 'Copenhagen',
        'intro': (
            "Denmark and New Zealand maintain bilateral diplomatic ties, "
            "and a small Danish-heritage community is present in New Zealand. "
            "Danish nationals have migrated to New Zealand over generations, "
            "and family connections exist in both directions. The New Zealand "
            "High Commission in London also covers Denmark for consular "
            "matters. When a person with New Zealand family connections dies "
            "in Denmark, the death is registered with the local kommunen "
            "(municipality) and entered into the CPR-registret. The dodsattest "
            "requires a certified English translation for New Zealand "
            "authorities. Both countries are Hague Apostille Convention "
            "members. New Zealand Customs clearance is required on arrival. "
            "(FCDO Travel Advice: New Zealand, 2025; New Zealand BDM, "
            "Department of Internal Affairs, 2025; Danish CPR-registret, "
            "2025.)"
        ),
    },
    # R80 -- South Korea x5
    {
        'origin': 'united-kingdom', 'dest': 'south-korea',
        'embassy_city': 'London',
        'intro': (
            "The United Kingdom and South Korea maintain an active bilateral "
            "relationship. South Korea is home to a community of British "
            "nationals working in technology, education, and professional "
            "services in Seoul and Busan. A significant Korean community "
            "also lives in the United Kingdom. The British Embassy in Seoul "
            "is fully operational. When someone from the United Kingdom dies "
            "and their family wishes to repatriate remains to South Korea, "
            "the death must be registered at the local register office in "
            "England and Wales within 5 days, or with the National Records "
            "of Scotland or GRONI in Northern Ireland. South Korea is not "
            "a member of the Hague Apostille Convention; the UK death "
            "certificate must be authenticated through the South Korean "
            "Embassy in London and then legalised by the Korean Ministry "
            "of Foreign Affairs. A certified Korean translation is required "
            "for all documentation. "
            "(FCDO Travel Advice: South Korea, 2025; Korean Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'south-korea',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States maintains one of the largest military "
            "presences outside its own territory in South Korea, with around "
            "28,500 US military personnel based in the country under the "
            "US-Republic of Korea Mutual Defense Treaty, alongside a large "
            "civilian diplomatic and business community. Korean-Americans "
            "form a significant community in the United States, with around "
            "two million people of Korean heritage concentrated in Los "
            "Angeles, New York, and the Washington DC area. The US Embassy "
            "in Seoul is among the largest in the region. South Korea is "
            "not a Hague Apostille Convention member; the US death certificate "
            "must be authenticated through the Korean Embassy in Washington "
            "DC, then legalised by the Korean Ministry of Foreign Affairs. "
            "(FCDO Travel Advice: South Korea, 2025; Korean Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ireland', 'dest': 'south-korea',
        'embassy_city': 'Dublin',
        'intro': (
            "Ireland and South Korea have active bilateral ties rooted "
            "in education and trade. South Korean students form one of "
            "the largest groups attending Irish English-language schools "
            "and universities. Irish nationals work in South Korea in "
            "education and technology sectors. The Korean Embassy in Dublin "
            "is fully operational. When someone from Ireland dies and their "
            "family wishes to repatriate remains to South Korea, the death "
            "must be registered with the local civil registration service. "
            "South Korea is not a Hague Apostille Convention member; the "
            "Irish death certificate must be authenticated through the "
            "Korean Embassy in Dublin, then legalised by the Korean Ministry "
            "of Foreign Affairs. A certified Korean translation is required. "
            "(FCDO Travel Advice: South Korea, 2025; Korean Ministry of "
            "Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'norway', 'dest': 'south-korea',
        'embassy_city': 'Oslo',
        'intro': (
            "Norway and South Korea maintain active bilateral ties, "
            "particularly in maritime industries and shipping. Norwegian "
            "nationals work in South Korea's maritime and engineering "
            "sectors, and Korean nationals are present in Norway in "
            "technology and education. The Korean Embassy in Oslo is fully "
            "operational. When a person with South Korean family connections "
            "dies in Norway, the death is registered with Folkeregisteret "
            "(the civil registration system). South Korea is not a Hague "
            "Apostille Convention member; the Norwegian dodsattest must be "
            "authenticated through the Korean Embassy in Oslo and then "
            "legalised by the Korean Ministry of Foreign Affairs in Seoul. "
            "A certified Korean translation is required for all documentation. "
            "(FCDO Travel Advice: South Korea, 2025; Korean Ministry of "
            "Foreign Affairs, 2025; Folkeregisteret, Skatteetaten, Norway, "
            "2025.)"
        ),
    },
    {
        'origin': 'denmark', 'dest': 'south-korea',
        'embassy_city': 'Copenhagen',
        'intro': (
            "Denmark and South Korea maintain bilateral relations through "
            "trade and shipping sectors. Danish nationals, including those "
            "in the shipping industry, work in South Korea, and Korean "
            "nationals study and work in Denmark. The Korean Embassy in "
            "Copenhagen is fully operational. When a person with South "
            "Korean family connections dies in Denmark, the death is "
            "registered with the local kommunen and entered into the "
            "CPR-registret. South Korea is not a Hague Apostille Convention "
            "member; the Danish dodsattest must be authenticated through "
            "the Korean Embassy in Copenhagen and then legalised by the "
            "Korean Ministry of Foreign Affairs in Seoul. A certified Korean "
            "translation is required. "
            "(FCDO Travel Advice: South Korea, 2025; Korean Ministry of "
            "Foreign Affairs, 2025; Danish CPR-registret, 2025.)"
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
