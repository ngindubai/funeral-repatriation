#!/usr/bin/env python3
"""Generate Tier C route pages: chunks R75-R76.

   R75 (25 routes, variants B,C,D,E,A x5):
     Botswana x5:  united-kingdom, south-africa, germany, united-states, france
     Namibia x5:   united-kingdom, germany, south-africa, united-states, france
     Malawi x5:    united-kingdom, south-africa, united-states, germany, france
     Lesotho x5:   united-kingdom, south-africa, united-states, germany, france
     Guyana x5:    united-kingdom, united-states, canada, germany, france

   R76 (25 routes, variants B,C,D,E,A x5):
     Fiji x5:             united-kingdom, australia, united-states, germany, france
     Papua New Guinea x5: united-kingdom, australia, united-states, germany, france
     Belize x5:           united-kingdom, united-states, canada, germany, france
     Gambia x5:           united-kingdom, united-states, germany, france, spain
     Sierra Leone x5:     united-kingdom, united-states, germany, france, spain

   Template rotation: R74 ended on A. R75 starts B (index 1).
   Each block of 25 cycles B,C,D,E,A x5, ending on A.
   R76 also starts B (index 1), ending on A.
"""

import os

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 1  # B

DEST_META = {
    'botswana': {
        'name': 'Botswana',
        'slug': 'botswana',
        'key': 'bw',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Botswana funeral director takes custody at Sir Seretse Khama "
            "International Airport (GBE) in Gaborone or Kasane Airport (BBK) "
            "in northern Botswana cargo terminal. Death registration in Botswana "
            "is handled by the Department of Civil Registration under the Ministry "
            "of Nationality and Passport Services. Death certificates are issued "
            "in English. Botswana is not a Hague Apostille Convention member; "
            "full consular authentication of all foreign documents is required "
            "by Botswana authorities. Botswana is a Commonwealth member. An "
            "embalming certificate and hermetically sealed coffin are required "
            "for all air imports. "
            "(Department of Civil Registration, Ministry of Nationality and "
            "Passport Services, Botswana, 2025; FCDO Travel Advice: Botswana, 2025.)"
        ),
        'consular_template': (
            "The Botswana High Commission or Embassy in {city} can advise on "
            "documentation requirements for repatriation to Botswana. Botswana "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required for all foreign documents. The High "
            "Commission cannot pay for or arrange repatriation. Contact the "
            "Department of Civil Registration in Botswana for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Botswana funeral director takes custody at Sir Seretse Khama "
            "International Airport (GBE) in Gaborone or Kasane Airport (BBK) "
            "in northern Botswana cargo terminal. The Department of Civil "
            "Registration under the Ministry of Nationality and Passport "
            "Services registers the death and issues a death certificate in "
            "English. All foreign documents require consular authentication "
            "before submission to Botswana authorities. Botswana is not a "
            "Hague Apostille Convention member. Botswana is a Commonwealth "
            "member. An embalming certificate and hermetically sealed coffin "
            "are required."
        ),
        'emergency_line': 'contact the Botswana High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-botswana',
    },
    'namibia': {
        'name': 'Namibia',
        'slug': 'namibia',
        'key': 'na',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Namibian funeral director takes custody at Hosea Kutako "
            "International Airport (WDH) near Windhoek cargo terminal. "
            "Death registration in Namibia is handled by the civil "
            "registration division under the Ministry of Home Affairs, "
            "Immigration, Safety and Security. Death certificates are "
            "issued in English. Namibia joined the Hague Apostille "
            "Convention in 2002; apostille certificates from member states "
            "are accepted. Namibia is a Commonwealth member. An embalming "
            "certificate and hermetically sealed coffin are required for "
            "all air imports. "
            "(Ministry of Home Affairs, Immigration, Safety and Security, "
            "Namibia, 2025; FCDO Travel Advice: Namibia, 2025.)"
        ),
        'consular_template': (
            "The Namibian High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Namibia. "
            "Namibia joined the Hague Apostille Convention in 2002. The "
            "High Commission cannot pay for or arrange repatriation. "
            "Contact the civil registration division of the Ministry of "
            "Home Affairs in Namibia for registration queries."
        ),
        'arrival_faq': (
            "The Namibian funeral director takes custody at Hosea Kutako "
            "International Airport (WDH) near Windhoek cargo terminal. "
            "The civil registration division under the Ministry of Home "
            "Affairs, Immigration, Safety and Security registers the death "
            "and issues a death certificate in English. Namibia joined the "
            "Hague Apostille Convention in 2002; apostille certificates "
            "from member states are accepted. Namibia is a Commonwealth "
            "member. An embalming certificate and hermetically sealed "
            "coffin are required."
        ),
        'emergency_line': 'contact the Namibian High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-namibia',
    },
    'malawi': {
        'name': 'Malawi',
        'slug': 'malawi',
        'key': 'mw',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Malawian funeral director takes custody at Kamuzu "
            "International Airport (LLW) in Lilongwe or Chileka Airport "
            "(BLZ) in Blantyre cargo terminal. Death registration in "
            "Malawi is handled by the Registrar General's Office under "
            "the Ministry of Justice and Constitutional Affairs. Death "
            "certificates are issued in English. Malawi is not a Hague "
            "Apostille Convention member; full consular authentication "
            "of all foreign documents is required by Malawian authorities. "
            "Malawi is a Commonwealth member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(Registrar General's Office, Ministry of Justice and "
            "Constitutional Affairs, Malawi, 2025; FCDO Travel Advice: "
            "Malawi, 2025.)"
        ),
        'consular_template': (
            "The Malawi High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Malawi. "
            "Malawi is not a Hague Apostille Convention member; full "
            "consular authentication is required for all foreign "
            "documents. The High Commission cannot pay for or arrange "
            "repatriation. Contact the Registrar General's Office in "
            "Malawi for civil registration queries."
        ),
        'arrival_faq': (
            "The Malawian funeral director takes custody at Kamuzu "
            "International Airport (LLW) in Lilongwe or Chileka Airport "
            "(BLZ) in Blantyre cargo terminal. The Registrar General's "
            "Office under the Ministry of Justice and Constitutional "
            "Affairs registers the death and issues a death certificate "
            "in English. All foreign documents require consular "
            "authentication before submission to Malawian authorities. "
            "Malawi is not a Hague Apostille Convention member. Malawi "
            "is a Commonwealth member. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Malawi High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-malawi',
    },
    'lesotho': {
        'name': 'Lesotho',
        'slug': 'lesotho',
        'key': 'ls',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Lesotho funeral director takes custody at Moshoeshoe I "
            "International Airport (MSU) near Maseru cargo terminal. "
            "Death registration in Lesotho is handled by the Civil "
            "Registration Department under the Ministry of Home Affairs. "
            "Death certificates are issued in English and Sesotho "
            "(both are official languages). Lesotho is not a Hague "
            "Apostille Convention member; full consular authentication "
            "of all foreign documents is required by Lesotho authorities. "
            "Lesotho is a Commonwealth member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(Civil Registration Department, Ministry of Home Affairs, "
            "Lesotho, 2025; FCDO Travel Advice: Lesotho, 2025.)"
        ),
        'consular_template': (
            "The Lesotho High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Lesotho. "
            "Lesotho is not a Hague Apostille Convention member; full "
            "consular authentication is required for all foreign "
            "documents. The High Commission cannot pay for or arrange "
            "repatriation. Contact the Civil Registration Department "
            "in Lesotho for civil registration queries."
        ),
        'arrival_faq': (
            "The Lesotho funeral director takes custody at Moshoeshoe I "
            "International Airport (MSU) near Maseru cargo terminal. "
            "The Civil Registration Department under the Ministry of "
            "Home Affairs registers the death and issues a death "
            "certificate in English and Sesotho. All foreign documents "
            "require consular authentication before submission to "
            "Lesotho authorities. Lesotho is not a Hague Apostille "
            "Convention member. Lesotho is a Commonwealth member. An "
            "embalming certificate and hermetically sealed coffin are "
            "required."
        ),
        'emergency_line': 'contact the Lesotho High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-lesotho',
    },
    'guyana': {
        'name': 'Guyana',
        'slug': 'guyana',
        'key': 'gy',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Guyana funeral director takes custody at Cheddi Jagan "
            "International Airport (GEO) near Georgetown cargo terminal. "
            "Death registration in Guyana is handled by the General "
            "Register Office under the Ministry of Legal Affairs. Death "
            "certificates are issued in English. Guyana is not a Hague "
            "Apostille Convention member; full consular authentication "
            "of all foreign documents is required by Guyanese authorities. "
            "Guyana is a Commonwealth member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(General Register Office, Ministry of Legal Affairs, "
            "Guyana, 2025; FCDO Travel Advice: Guyana, 2025.)"
        ),
        'consular_template': (
            "The Guyana High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Guyana. "
            "Guyana is not a Hague Apostille Convention member; full "
            "consular authentication is required for all foreign "
            "documents. The High Commission cannot pay for or arrange "
            "repatriation. Contact the General Register Office in "
            "Guyana for civil registration queries."
        ),
        'arrival_faq': (
            "The Guyana funeral director takes custody at Cheddi Jagan "
            "International Airport (GEO) near Georgetown cargo terminal. "
            "The General Register Office under the Ministry of Legal "
            "Affairs registers the death and issues a death certificate "
            "in English. All foreign documents require consular "
            "authentication before submission to Guyanese authorities. "
            "Guyana is not a Hague Apostille Convention member. Guyana "
            "is a Commonwealth member. An embalming certificate and "
            "hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Guyana High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-guyana',
    },
    'fiji': {
        'name': 'Fiji',
        'slug': 'fiji',
        'key': 'fj',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Fiji funeral director takes custody at Nadi International "
            "Airport (NAN) or Suva Nausori Airport (SUV) cargo terminal. "
            "Death registration in Fiji is handled by the Registrar-"
            "General's Office under the Ministry of Justice. Death "
            "certificates are issued in English. Fiji is not a Hague "
            "Apostille Convention member; full consular authentication "
            "of all foreign documents is required by Fiji authorities. "
            "Fiji is a Commonwealth member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(Registrar-General's Office, Ministry of Justice, Fiji, "
            "2025; FCDO Travel Advice: Fiji, 2025.)"
        ),
        'consular_template': (
            "The Fiji High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Fiji. "
            "Fiji is not a Hague Apostille Convention member; full "
            "consular authentication is required for all foreign "
            "documents. The High Commission cannot pay for or arrange "
            "repatriation. Contact the Registrar-General's Office in "
            "Fiji for civil registration queries."
        ),
        'arrival_faq': (
            "The Fiji funeral director takes custody at Nadi International "
            "Airport (NAN) or Suva Nausori Airport (SUV) cargo terminal. "
            "The Registrar-General's Office under the Ministry of Justice "
            "registers the death and issues a death certificate in English. "
            "All foreign documents require consular authentication before "
            "submission to Fiji authorities. Fiji is not a Hague Apostille "
            "Convention member. Fiji is a Commonwealth member. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Fiji High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-fiji',
    },
    'papua-new-guinea': {
        'name': 'Papua New Guinea',
        'slug': 'papua-new-guinea',
        'key': 'pg',
        'complexity_override': 'high',
        'timeline_avg_override': '4-8 weeks',
        'timeline_fast_override': '3-5 weeks',
        'timeline_complex_override': '10-16 weeks',
        'reception': (
            "The Papua New Guinea funeral director takes custody at "
            "Jacksons International Airport (POM) in Port Moresby cargo "
            "terminal. For deaths in remote areas, the body must be "
            "transferred to Port Moresby before international repatriation "
            "can proceed. Death registration in Papua New Guinea is "
            "handled by the Civil Registration Authority under the "
            "Department of Justice and Attorney General. Death "
            "certificates are issued in English. Papua New Guinea is "
            "not a Hague Apostille Convention member; full consular "
            "authentication of all foreign documents is required. Papua "
            "New Guinea is a Commonwealth member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports; a specialist is essential on this corridor given "
            "the geographic and logistical complexity. "
            "(Civil Registration Authority, Department of Justice and "
            "Attorney General, Papua New Guinea, 2025; FCDO Travel "
            "Advice: Papua New Guinea, 2025.)"
        ),
        'consular_template': (
            "The Papua New Guinea High Commission or Embassy in {city} "
            "can advise on documentation requirements for repatriation "
            "to Papua New Guinea. Papua New Guinea is not a Hague "
            "Apostille Convention member; full consular authentication "
            "is required for all foreign documents. The High Commission "
            "cannot pay for or arrange repatriation. Contact the Civil "
            "Registration Authority in Papua New Guinea for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Papua New Guinea funeral director takes custody at "
            "Jacksons International Airport (POM) in Port Moresby cargo "
            "terminal. For deaths in remote locations, transfer to Port "
            "Moresby is required before international repatriation can "
            "proceed. The Civil Registration Authority under the "
            "Department of Justice and Attorney General registers the "
            "death and issues a death certificate in English. All "
            "foreign documents require consular authentication. Papua "
            "New Guinea is not a Hague Apostille Convention member. "
            "Papua New Guinea is a Commonwealth member. An embalming "
            "certificate and hermetically sealed coffin are required. "
            "A specialist with experience of PNG procedures is essential."
        ),
        'emergency_line': 'contact the Papua New Guinea High Commission or Embassy in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-papua-new-guinea',
    },
    'belize': {
        'name': 'Belize',
        'slug': 'belize',
        'key': 'bz',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Belize funeral director takes custody at Philip S.W. "
            "Goldson International Airport (BZE) near Belize City cargo "
            "terminal. Death registration in Belize is handled by the "
            "General Registry Office under the Ministry of Human "
            "Development. Death certificates are issued in English. "
            "Belize joined the Hague Apostille Convention in 2019; "
            "apostille certificates from member states are accepted. "
            "Belize is a Commonwealth member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(General Registry Office, Ministry of Human Development, "
            "Belize, 2025; FCDO Travel Advice: Belize, 2025.)"
        ),
        'consular_template': (
            "The Belize High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to Belize. "
            "Belize joined the Hague Apostille Convention in 2019. The "
            "High Commission cannot pay for or arrange repatriation. "
            "Contact the General Registry Office in Belize for civil "
            "registration queries."
        ),
        'arrival_faq': (
            "The Belize funeral director takes custody at Philip S.W. "
            "Goldson International Airport (BZE) near Belize City cargo "
            "terminal. The General Registry Office under the Ministry "
            "of Human Development registers the death and issues a death "
            "certificate in English. Belize joined the Hague Apostille "
            "Convention in 2019; apostille certificates from member "
            "states are accepted. Belize is a Commonwealth member. An "
            "embalming certificate and hermetically sealed coffin are "
            "required."
        ),
        'emergency_line': 'contact the Belize High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-belize',
    },
    'gambia': {
        'name': 'The Gambia',
        'slug': 'gambia',
        'key': 'gm',
        'short_title': 'Gambia',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-5 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Gambia funeral director takes custody at Banjul "
            "International Airport (BJL) cargo terminal. Death "
            "registration in The Gambia is handled by the General "
            "Register Office. Death certificates are issued in English. "
            "The Gambia is not a Hague Apostille Convention member; "
            "full consular authentication of all foreign documents is "
            "required by Gambian authorities. The Gambia is a "
            "Commonwealth member. An embalming certificate and "
            "hermetically sealed coffin are required for all air "
            "imports. "
            "(General Register Office, The Gambia, 2025; FCDO Travel "
            "Advice: The Gambia, 2025.)"
        ),
        'consular_template': (
            "The Gambia High Commission or Embassy in {city} can advise "
            "on documentation requirements for repatriation to The Gambia. "
            "The Gambia is not a Hague Apostille Convention member; full "
            "consular authentication is required for all foreign "
            "documents. The High Commission cannot pay for or arrange "
            "repatriation. Contact the General Register Office in "
            "The Gambia for civil registration queries."
        ),
        'arrival_faq': (
            "The Gambia funeral director takes custody at Banjul "
            "International Airport (BJL) cargo terminal. The General "
            "Register Office registers the death and issues a death "
            "certificate in English. All foreign documents require "
            "consular authentication before submission to Gambian "
            "authorities. The Gambia is not a Hague Apostille Convention "
            "member. The Gambia is a Commonwealth member. An embalming "
            "certificate and hermetically sealed coffin are required."
        ),
        'emergency_line': 'contact the Gambia High Commission or Embassy in the origin country',
        'hub_url': 'repatriation-from-gambia',
    },
    'sierra-leone': {
        'name': 'Sierra Leone',
        'slug': 'sierra-leone',
        'key': 'sl',
        'complexity_override': 'moderate',
        'timeline_avg_override': '3-6 weeks',
        'timeline_fast_override': '2-3 weeks',
        'timeline_complex_override': '8-12 weeks',
        'reception': (
            "The Sierra Leone funeral director takes custody at Freetown "
            "Lungi International Airport (FNA) cargo terminal. The "
            "airport is located in Lungi, across the Sierra Leone River "
            "estuary from Freetown; transfer by helicopter, hovercraft, "
            "or road via Lungi town is required and adds to logistical "
            "complexity. Death registration in Sierra Leone is handled "
            "by the Office of the Administrator and Registrar General. "
            "Death certificates are issued in English. Sierra Leone is "
            "not a Hague Apostille Convention member; full consular "
            "authentication of all foreign documents is required. Sierra "
            "Leone is a Commonwealth member. An embalming certificate "
            "and hermetically sealed coffin are required for all air "
            "imports. "
            "(Office of the Administrator and Registrar General, Sierra "
            "Leone, 2025; FCDO Travel Advice: Sierra Leone, 2025.)"
        ),
        'consular_template': (
            "The Sierra Leone High Commission or Embassy in {city} can "
            "advise on documentation requirements for repatriation to "
            "Sierra Leone. Sierra Leone is not a Hague Apostille "
            "Convention member; full consular authentication is required "
            "for all foreign documents. The High Commission cannot pay "
            "for or arrange repatriation. Contact the Office of the "
            "Administrator and Registrar General in Sierra Leone for "
            "civil registration queries."
        ),
        'arrival_faq': (
            "The Sierra Leone funeral director takes custody at Freetown "
            "Lungi International Airport (FNA) cargo terminal. The "
            "airport is located in Lungi, across the Sierra Leone River "
            "estuary from Freetown; transfer by helicopter, hovercraft, "
            "or road is required. The Office of the Administrator and "
            "Registrar General registers the death and issues a death "
            "certificate in English. All foreign documents require "
            "consular authentication. Sierra Leone is not a Hague "
            "Apostille Convention member. Sierra Leone is a Commonwealth "
            "member. An embalming certificate and hermetically sealed "
            "coffin are required. A specialist with experience of "
            "Sierra Leone procedures is recommended."
        ),
        'emergency_line': 'contact the Sierra Leone High Commission or Embassy in the origin country, or the FCDO on +44 (0)20 7008 5000',
        'hub_url': 'repatriation-from-sierra-leone',
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
}

ROUTES = [
    # R75 -- Botswana x5
    {
        'origin': 'united-kingdom', 'dest': 'botswana',
        'embassy_city': 'London',
        'intro': (
            "Botswana is a Commonwealth member with strong ties to the United "
            "Kingdom, and a destination for British NGO workers, development "
            "professionals, and wildlife tourists visiting Chobe and the Okavango "
            "Delta. The British High Commission in Gaborone is fully operational. "
            "When someone from the United Kingdom dies and their family wishes to "
            "repatriate remains to Botswana, the death must be registered at the "
            "local register office in England and Wales within 5 days, or with "
            "the National Records of Scotland or GRONI in Northern Ireland. The "
            "Botswana High Commission in London can advise on documentation "
            "requirements for the Department of Civil Registration. UK death "
            "certificates require consular authentication. Botswana is not a "
            "Hague Apostille Convention member. "
            "(FCDO Travel Advice: Botswana, 2025; Department of Civil "
            "Registration, Botswana, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'botswana',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa and Botswana share a long border, and there is "
            "substantial cross-border movement for work, family, and trade. "
            "Many Batswana live and work in South Africa, particularly in "
            "the Gauteng and North West provinces, and repatriation between "
            "the two countries is a well-established corridor. When a Botswana "
            "national dies in South Africa, the death is registered with the "
            "Department of Home Affairs via the local Home Affairs office. The "
            "death certificate is issued in English. The Botswana High Commission "
            "in Pretoria can advise on documentation requirements for the "
            "Department of Civil Registration. Botswana is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Botswana, 2025; Department of Civil "
            "Registration, Botswana, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'botswana',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a development cooperation relationship with Botswana, "
            "and a small German community works in the development and mining "
            "sectors in Botswana. The German Embassy in Gaborone is operational. "
            "When a Botswana national or a person with Botswana family connections "
            "dies in Germany and their family wishes to repatriate remains to "
            "Botswana, the death is registered with the local Standesamt (civil "
            "registry). The Sterbeurkunde is issued in German and requires "
            "consular authentication for submission to the Department of Civil "
            "Registration. The Botswana Embassy in Berlin can advise on "
            "documentation requirements. Botswana is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Botswana, 2025; Department of Civil "
            "Registration, Botswana, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'botswana',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a development partnership with Botswana, "
            "including significant PEPFAR health programmes, and a small American "
            "community of development workers and researchers is based in Botswana. "
            "The US Embassy in Gaborone is fully operational. When a Botswana "
            "national or a person with Botswana family connections dies in the "
            "United States, the death is registered with the state civil records "
            "office where the death occurred. The Botswana Embassy in Washington "
            "DC can advise on documentation requirements for the Department of "
            "Civil Registration. US death certificates require consular "
            "authentication. Botswana is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(FCDO Travel Advice: Botswana, 2025; Department of Civil "
            "Registration, Botswana, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'botswana',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains diplomatic and development cooperation relations "
            "with Botswana, and a small French community works in Botswana "
            "in the development and resource sectors. The French Embassy in "
            "Gaborone is operational. When a Botswana national dies in France "
            "and their family wishes to repatriate remains to Botswana, the "
            "death is registered with the local mairie (town hall). The acte "
            "de deces is issued in French and requires consular authentication "
            "for submission to the Department of Civil Registration. The "
            "Botswana Embassy in Paris can advise on documentation requirements. "
            "Botswana is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Botswana, 2025; Department of Civil "
            "Registration, Botswana, 2025.)"
        ),
    },
    # R75 -- Namibia x5
    {
        'origin': 'united-kingdom', 'dest': 'namibia',
        'embassy_city': 'London',
        'intro': (
            "Namibia is a Commonwealth member and a popular destination for "
            "British tourists visiting the Namib Desert, Sossusvlei, and Etosha "
            "National Park. The British High Commission in Windhoek is fully "
            "operational. When someone from the United Kingdom dies and their "
            "family wishes to repatriate remains to Namibia, the death must be "
            "registered at the local register office in England and Wales within "
            "5 days, or with the National Records of Scotland or GRONI in "
            "Northern Ireland. The Namibia High Commission in London can advise "
            "on documentation requirements for the civil registration division. "
            "UK death certificates are apostilled; Namibia joined the Hague "
            "Apostille Convention in 2002. "
            "(FCDO Travel Advice: Namibia, 2025; Ministry of Home Affairs, "
            "Immigration, Safety and Security, Namibia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'namibia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has deep historical ties with Namibia, which was the German "
            "colony of German South West Africa from 1884 until 1915. An "
            "established German-Namibian community of some 20,000 people remains "
            "in Namibia, centred on Windhoek, Swakopmund, and Luderitz, and "
            "there is significant ongoing migration between the two countries. "
            "The Germany-Namibia repatriation corridor is among the most active "
            "in sub-Saharan Africa for European origin countries. When a Namibian "
            "national or person of Namibian heritage dies in Germany, the death "
            "is registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German. The Namibia Embassy in Berlin "
            "can advise on documentation requirements. Both Germany and Namibia "
            "are Hague Apostille Convention members; Namibia joined in 2002. "
            "(FCDO Travel Advice: Namibia, 2025; Ministry of Home Affairs, "
            "Immigration, Safety and Security, Namibia, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'namibia',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa and Namibia share a long border and close historical, "
            "economic, and social ties. Many Namibians live and work in South "
            "Africa, and many South Africans work and retire in Namibia. The "
            "South Africa-Namibia repatriation corridor is well-established. "
            "When a Namibian national dies in South Africa, the death is "
            "registered with the Department of Home Affairs via the local Home "
            "Affairs office. The death certificate is issued in English. The "
            "Namibia High Commission in Pretoria can advise on documentation "
            "requirements for the civil registration division. Both countries "
            "are Hague Apostille Convention members; Namibia joined in 2002. "
            "(FCDO Travel Advice: Namibia, 2025; Ministry of Home Affairs, "
            "Immigration, Safety and Security, Namibia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'namibia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States maintains development and diplomatic relations "
            "with Namibia, and a small American community works in Namibia in "
            "the development, mining, and conservation sectors. The US Embassy "
            "in Windhoek is operational. When a Namibian national or a person "
            "with Namibian family connections dies in the United States, the "
            "death is registered with the state civil records office where the "
            "death occurred. The Namibia Embassy in Washington DC can advise "
            "on documentation requirements for the civil registration division. "
            "Namibia joined the Hague Apostille Convention in 2002; US-issued "
            "apostille certificates are accepted. "
            "(FCDO Travel Advice: Namibia, 2025; Ministry of Home Affairs, "
            "Immigration, Safety and Security, Namibia, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'namibia',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains diplomatic and development relations with Namibia, "
            "and a small French community works in Namibia in the development, "
            "energy, and conservation sectors. The French Embassy in Windhoek "
            "is operational. When a Namibian national dies in France and their "
            "family wishes to repatriate remains to Namibia, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "is issued in French and requires certified translation for submission "
            "to Namibian civil registration authorities. The Namibia Embassy "
            "in Paris can advise on documentation requirements. Namibia joined "
            "the Hague Apostille Convention in 2002; French-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Namibia, 2025; Ministry of Home Affairs, "
            "Immigration, Safety and Security, Namibia, 2025.)"
        ),
    },
    # R75 -- Malawi x5
    {
        'origin': 'united-kingdom', 'dest': 'malawi',
        'embassy_city': 'London',
        'intro': (
            "Malawi is a Commonwealth member with long historical ties to the "
            "United Kingdom, rooted in the work of David Livingstone and the "
            "colonial era. A significant community of British NGO workers, aid "
            "professionals, and missionaries lives and works in Malawi. The "
            "British High Commission in Lilongwe is fully operational. When "
            "someone from the United Kingdom dies and their family wishes to "
            "repatriate remains to Malawi, the death must be registered at the "
            "local register office in England and Wales within 5 days, or with "
            "the National Records of Scotland or GRONI in Northern Ireland. The "
            "Malawi High Commission in London can advise on documentation "
            "requirements for the Registrar General's Office. Malawi is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Malawi, 2025; Registrar General's Office, "
            "Malawi, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'malawi',
        'embassy_city': 'Pretoria',
        'intro': (
            "South Africa hosts a large Malawian migrant worker community, "
            "drawn particularly to the mining, agricultural, and domestic "
            "sectors. The South Africa-Malawi repatriation corridor carries "
            "significant volume, with many families needing to repatriate "
            "remains of workers who died far from home. When a Malawian "
            "national dies in South Africa, the death is registered with the "
            "Department of Home Affairs via the local Home Affairs office. "
            "The death certificate is issued in English. The Malawi High "
            "Commission in Pretoria can advise on documentation requirements "
            "for the Registrar General's Office. Malawi is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Malawi, 2025; Registrar General's Office, "
            "Malawi, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'malawi',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a development and health partnership with "
            "Malawi, including PEPFAR and USAID programmes, and a small American "
            "community of health workers and development professionals is based "
            "in Malawi. The US Embassy in Lilongwe is fully operational. When a "
            "Malawian national or a person with Malawian family connections dies "
            "in the United States, the death is registered with the state civil "
            "records office where the death occurred. The Malawi Embassy in "
            "Washington DC can advise on documentation requirements for the "
            "Registrar General's Office. Malawi is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Malawi, 2025; Registrar General's Office, "
            "Malawi, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'malawi',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains development cooperation with Malawi through "
            "GIZ and KfW programmes, and a small German community of development "
            "workers is based in Malawi. The German Embassy in Lilongwe is "
            "operational. When a Malawian national or a person with Malawian "
            "family connections dies in Germany and their family wishes to "
            "repatriate remains to Malawi, the death is registered with the "
            "local Standesamt (civil registry). The Sterbeurkunde is issued "
            "in German and requires consular authentication for submission "
            "to the Registrar General's Office. The Malawi Embassy in Berlin "
            "can advise on documentation requirements. Malawi is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Malawi, 2025; Registrar General's Office, "
            "Malawi, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'malawi',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains development and diplomatic relations with Malawi, "
            "with French nationals working in the development and health sectors "
            "in Malawi. The French Embassy in Lilongwe is operational. When a "
            "Malawian national dies in France and their family wishes to "
            "repatriate remains to Malawi, the death is registered with the "
            "local mairie (town hall). The acte de deces is issued in French "
            "and requires consular authentication for submission to the "
            "Registrar General's Office in Malawi. The Malawi Embassy in "
            "Paris can advise on documentation requirements. Malawi is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Malawi, 2025; Registrar General's Office, "
            "Malawi, 2025.)"
        ),
    },
    # R75 -- Lesotho x5
    {
        'origin': 'united-kingdom', 'dest': 'lesotho',
        'embassy_city': 'London',
        'intro': (
            "Lesotho is a Commonwealth member and an independent kingdom entirely "
            "surrounded by South Africa. The United Kingdom maintains diplomatic "
            "ties with Lesotho; the British High Commission in Pretoria, South "
            "Africa, is accredited to Lesotho and can assist British nationals. "
            "When someone from the United Kingdom dies and their family wishes "
            "to repatriate remains to Lesotho, the death must be registered at "
            "the local register office in England and Wales within 5 days, or "
            "with the National Records of Scotland or GRONI in Northern Ireland. "
            "The Lesotho High Commission in London can advise on documentation "
            "requirements for the Civil Registration Department. Lesotho is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Lesotho, 2025; Civil Registration Department, "
            "Ministry of Home Affairs, Lesotho, 2025.)"
        ),
    },
    {
        'origin': 'south-africa', 'dest': 'lesotho',
        'embassy_city': 'Pretoria',
        'intro': (
            "Lesotho is an enclave within South Africa, and there is very "
            "significant cross-border movement: large numbers of Basotho "
            "nationals work in South Africa's mining and agricultural sectors "
            "and in domestic service. This makes South Africa one of the "
            "highest-volume repatriation corridors for Lesotho. When a "
            "Lesotho national dies in South Africa, the death is registered "
            "with the Department of Home Affairs via the local Home Affairs "
            "office. The death certificate is issued in English. The Lesotho "
            "High Commission in Pretoria can advise on documentation requirements "
            "for the Civil Registration Department. Lesotho is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Lesotho, 2025; Civil Registration Department, "
            "Ministry of Home Affairs, Lesotho, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'lesotho',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a substantial health and development "
            "partnership with Lesotho, particularly through PEPFAR, which "
            "has been central to the country's HIV/AIDS response. A small "
            "American community of health and development workers is based "
            "in Lesotho. The US Embassy in Maseru is operational. When a "
            "Lesotho national or a person with Lesotho family connections "
            "dies in the United States, the death is registered with the "
            "state civil records office where the death occurred. The Lesotho "
            "Embassy in Washington DC can advise on documentation requirements "
            "for the Civil Registration Department. Lesotho is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Lesotho, 2025; Civil Registration Department, "
            "Lesotho, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'lesotho',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains development cooperation with Lesotho, and a "
            "small German community of development workers is present in Lesotho. "
            "Germany does not maintain a resident embassy in Maseru; German "
            "nationals in Lesotho are advised to contact the German Embassy "
            "in Pretoria, South Africa. When a Lesotho national dies in Germany "
            "and their family wishes to repatriate remains to Lesotho, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires consular "
            "authentication for submission to the Civil Registration Department. "
            "The Lesotho Embassy in Berlin can advise on documentation "
            "requirements. Lesotho is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(FCDO Travel Advice: Lesotho, 2025; Civil Registration Department, "
            "Lesotho, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'lesotho',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains development and diplomatic relations with Lesotho. "
            "France does not maintain a resident embassy in Maseru; French "
            "nationals in Lesotho are directed to the French Embassy in Pretoria, "
            "South Africa, or to the French Embassy in Harare, Zimbabwe, depending "
            "on their circumstances. When a Lesotho national dies in France and "
            "their family wishes to repatriate remains to Lesotho, the death is "
            "registered with the local mairie (town hall). The acte de deces is "
            "issued in French and requires consular authentication for submission "
            "to the Civil Registration Department in Lesotho. The Lesotho "
            "Embassy in Paris can advise on documentation requirements. Lesotho "
            "is not a Hague Apostille Convention member. "
            "(FCDO Travel Advice: Lesotho, 2025; Civil Registration Department, "
            "Lesotho, 2025.)"
        ),
    },
    # R75 -- Guyana x5
    {
        'origin': 'united-kingdom', 'dest': 'guyana',
        'embassy_city': 'London',
        'intro': (
            "Guyana is a Commonwealth member with deep historical and family "
            "ties to the United Kingdom, built on migration since the Windrush "
            "era. The Guyanese community in the United Kingdom is significant, "
            "concentrated in London and other cities, and repatriation between "
            "the two countries is a well-established corridor. The British High "
            "Commission in Georgetown is fully operational. When someone from "
            "the United Kingdom dies and their family wishes to repatriate "
            "remains to Guyana, the death must be registered at the local "
            "register office in England and Wales within 5 days, or with the "
            "National Records of Scotland or GRONI in Northern Ireland. The "
            "Guyana High Commission in London can advise on documentation "
            "requirements for the General Register Office. Guyana is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Guyana, 2025; General Register Office, "
            "Guyana, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'guyana',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has the largest Guyanese diaspora community "
            "outside Guyana, concentrated in New York City (particularly "
            "Brooklyn and Queens), New Jersey, and Florida. This community "
            "maintains strong family ties to Guyana, making the US-Guyana "
            "corridor one of the highest-volume repatriation routes for the "
            "country. When a Guyanese national or a person with Guyanese "
            "family connections dies in the United States, the death is "
            "registered with the state civil records office where the death "
            "occurred. The Guyana Embassy in Washington DC can advise on "
            "documentation requirements for the General Register Office. "
            "Guyana is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Guyana, 2025; General Register Office, "
            "Guyana, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'guyana',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a substantial Guyanese diaspora community, "
            "concentrated in Toronto, Ontario, with significant numbers "
            "also in Montreal and other cities. Canada is among the primary "
            "destinations for Guyanese nationals who migrate abroad, and "
            "strong family ties are maintained with Guyana. When a Guyanese "
            "national dies in Canada, the death is registered with the "
            "provincial civil records registry. The Guyana High Commission "
            "in Ottawa can advise on documentation requirements for the "
            "General Register Office. Guyana is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Guyana, 2025; General Register Office, "
            "Guyana, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'guyana',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains diplomatic and development relations with Guyana, "
            "and a small German community is present in Guyana, drawn to the "
            "mining, energy, and development sectors. The German Embassy in "
            "Georgetown is operational. When a Guyanese national or a person "
            "with Guyanese family connections dies in Germany and their family "
            "wishes to repatriate remains to Guyana, the death is registered "
            "with the local Standesamt (civil registry). The Sterbeurkunde "
            "is issued in German and requires consular authentication for "
            "submission to the General Register Office. The Guyana Embassy "
            "in Berlin can advise on documentation requirements. Guyana is "
            "not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Guyana, 2025; General Register Office, "
            "Guyana, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'guyana',
        'embassy_city': 'Paris',
        'intro': (
            "France borders Guyana through French Guiana, an overseas "
            "territory that shares a land frontier with Guyana. This "
            "geographic proximity creates cross-border movement and family "
            "connections between French Guiana and Guyana. When a Guyanese "
            "national dies in France and their family wishes to repatriate "
            "remains to Guyana, the death is registered with the local "
            "mairie (town hall). The acte de deces is issued in French "
            "and requires consular authentication for submission to the "
            "General Register Office. The Guyana Embassy in Paris can "
            "advise on documentation requirements. Guyana is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Guyana, 2025; General Register Office, "
            "Guyana, 2025.)"
        ),
    },
    # R76 -- Fiji x5
    {
        'origin': 'united-kingdom', 'dest': 'fiji',
        'embassy_city': 'London',
        'intro': (
            "Fiji is a Commonwealth member and a popular destination for British "
            "tourists, honeymooners, and divers. The Fijian-British community "
            "in the United Kingdom is established, with Fijian nurses and "
            "healthcare workers forming a significant part. The British High "
            "Commission in Suva is fully operational. When someone from the "
            "United Kingdom dies and their family wishes to repatriate remains "
            "to Fiji, the death must be registered at the local register office "
            "in England and Wales within 5 days, or with the National Records "
            "of Scotland or GRONI in Northern Ireland. The Fiji High Commission "
            "in London can advise on documentation requirements for the "
            "Registrar-General's Office. Fiji is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Fiji, 2025; Registrar-General's Office, "
            "Ministry of Justice, Fiji, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'fiji',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia has the largest Fijian diaspora community outside the "
            "Pacific, with a well-established Fijian-Australian population "
            "in Melbourne, Sydney, and Brisbane, drawn by work, study, and "
            "family migration. Australia is also a major source of tourists "
            "and investors in Fiji. The Australia-Fiji repatriation corridor "
            "is among the most active in the Pacific. When a Fijian national "
            "dies in Australia and their family wishes to repatriate remains "
            "to Fiji, the death is registered with the state or territory "
            "Births, Deaths and Marriages (BDM) registry. The Fiji High "
            "Commission in Canberra can advise on documentation requirements. "
            "Fiji is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Fiji, 2025; Registrar-General's Office, "
            "Ministry of Justice, Fiji, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'fiji',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Fijian diaspora community, including "
            "former military personnel from the Republic of Fiji Military "
            "Forces who served alongside US forces, concentrated in California "
            "and Hawaii. The US Embassy in Suva is operational. When a Fijian "
            "national dies in the United States and their family wishes to "
            "repatriate remains to Fiji, the death is registered with the state "
            "civil records office where the death occurred. The Fiji Embassy "
            "in Washington DC can advise on documentation requirements for the "
            "Registrar-General's Office. Fiji is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: Fiji, 2025; Registrar-General's Office, "
            "Ministry of Justice, Fiji, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'fiji',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a development and diplomatic relationship with Fiji, "
            "and Fiji is a destination for German tourists and divers. Germany "
            "does not maintain a resident embassy in Suva; German nationals "
            "in Fiji are advised to contact the German Embassy in Canberra, "
            "Australia. When a Fijian national dies in Germany and their "
            "family wishes to repatriate remains to Fiji, the death is "
            "registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires consular "
            "authentication for submission to the Registrar-General's Office. "
            "The Fiji Embassy in Berlin can advise on documentation "
            "requirements. Fiji is not a Hague Apostille Convention member; "
            "full consular authentication is required. "
            "(FCDO Travel Advice: Fiji, 2025; Registrar-General's Office, "
            "Ministry of Justice, Fiji, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'fiji',
        'embassy_city': 'Paris',
        'intro': (
            "France has a presence in the Pacific through its overseas "
            "territories of New Caledonia and French Polynesia, both of which "
            "are geographically close to Fiji. France maintains diplomatic "
            "ties with Fiji. The French Embassy in Suva is operational. When "
            "a Fijian national dies in France and their family wishes to "
            "repatriate remains to Fiji, the death is registered with the "
            "local mairie (town hall). The acte de deces is issued in French "
            "and requires consular authentication for submission to the "
            "Registrar-General's Office. The Fiji Embassy in Paris can "
            "advise on documentation requirements. Fiji is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Fiji, 2025; Registrar-General's Office, "
            "Ministry of Justice, Fiji, 2025.)"
        ),
    },
    # R76 -- Papua New Guinea x5
    {
        'origin': 'united-kingdom', 'dest': 'papua-new-guinea',
        'embassy_city': 'London',
        'intro': (
            "Papua New Guinea is a Commonwealth member with historical ties "
            "to the United Kingdom through the colonial era and post-independence "
            "partnership. British nationals work in Papua New Guinea in the "
            "resources, development, and aid sectors. The British High Commission "
            "in Port Moresby is fully operational. When someone from the United "
            "Kingdom dies and their family wishes to repatriate remains to Papua "
            "New Guinea, the death must be registered at the local register "
            "office in England and Wales within 5 days, or with the National "
            "Records of Scotland or GRONI in Northern Ireland. For deaths in "
            "remote areas of PNG, transfer to Port Moresby may add significant "
            "time. A specialist with experience of PNG procedures is strongly "
            "recommended. Papua New Guinea is not a Hague Apostille Convention "
            "member. "
            "(FCDO Travel Advice: Papua New Guinea, 2025; Civil Registration "
            "Authority, Department of Justice and Attorney General, PNG, 2025.)"
        ),
    },
    {
        'origin': 'australia', 'dest': 'papua-new-guinea',
        'embassy_city': 'Canberra',
        'intro': (
            "Australia and Papua New Guinea share deep historical, cultural, "
            "and economic ties: Australia administered what is now PNG until "
            "independence in 1975, and Australia remains PNG's closest bilateral "
            "partner. A significant Australian community works in PNG in the "
            "resources, development, and government sectors, and many Papua New "
            "Guineans have family connections in Australia. The Australia-PNG "
            "repatriation corridor is the highest-volume route for PNG. When a "
            "Papua New Guinean national dies in Australia and their family wishes "
            "to repatriate remains to PNG, the death is registered with the "
            "state or territory BDM registry. The PNG High Commission in Canberra "
            "can advise on documentation requirements. For deaths in remote areas "
            "of PNG, transfer to Port Moresby may be required. A specialist is "
            "essential on this corridor. "
            "(FCDO Travel Advice: Papua New Guinea, 2025; Civil Registration "
            "Authority, Department of Justice and Attorney General, PNG, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'papua-new-guinea',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States maintains diplomatic and development relations "
            "with Papua New Guinea, with a US Embassy in Port Moresby. American "
            "nationals work in PNG in the energy, mining, and development sectors. "
            "When a Papua New Guinean national or a person with PNG family "
            "connections dies in the United States, the death is registered "
            "with the state civil records office where the death occurred. The "
            "Papua New Guinea Embassy in Washington DC can advise on "
            "documentation requirements for the Civil Registration Authority. "
            "For deaths in remote PNG locations, transfer to Port Moresby may "
            "be required before international repatriation can proceed. Papua "
            "New Guinea is not a Hague Apostille Convention member; full "
            "consular authentication is required. "
            "(FCDO Travel Advice: Papua New Guinea, 2025; Civil Registration "
            "Authority, PNG, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'papua-new-guinea',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains development cooperation with Papua New Guinea "
            "and a small German community works in PNG in the resource and "
            "development sectors. Germany does not maintain a resident embassy "
            "in Port Moresby; German nationals in PNG are advised to contact "
            "the German Embassy in Canberra, Australia. When a Papua New "
            "Guinean national dies in Germany and their family wishes to "
            "repatriate remains to PNG, the death is registered with the local "
            "Standesamt (civil registry). The Sterbeurkunde is issued in German "
            "and requires consular authentication for submission to the Civil "
            "Registration Authority. The Papua New Guinea High Commission or "
            "Embassy in Berlin can advise on documentation. Papua New Guinea "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Papua New Guinea, 2025; Civil Registration "
            "Authority, PNG, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'papua-new-guinea',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains diplomatic relations with Papua New Guinea, "
            "with a French Embassy in Port Moresby. France's presence in "
            "the Pacific through New Caledonia provides regional context for "
            "the relationship. When a Papua New Guinean national dies in "
            "France and their family wishes to repatriate remains to PNG, "
            "the death is registered with the local mairie (town hall). "
            "The acte de deces is issued in French and requires consular "
            "authentication for submission to the Civil Registration Authority "
            "in PNG. The Papua New Guinea Embassy in Paris can advise on "
            "documentation requirements. Papua New Guinea is not a Hague "
            "Apostille Convention member; full consular authentication is "
            "required. "
            "(FCDO Travel Advice: Papua New Guinea, 2025; Civil Registration "
            "Authority, Department of Justice and Attorney General, PNG, 2025.)"
        ),
    },
    # R76 -- Belize x5
    {
        'origin': 'united-kingdom', 'dest': 'belize',
        'embassy_city': 'London',
        'intro': (
            "Belize is a Commonwealth member and was formerly British Honduras, "
            "with the Union Flag lowered on independence in 1981. Strong cultural, "
            "linguistic, and family ties remain between Belize and the United "
            "Kingdom, and a British defence presence continues at British Forces "
            "Belize. When someone from the United Kingdom dies and their family "
            "wishes to repatriate remains to Belize, the death must be registered "
            "at the local register office in England and Wales within 5 days, or "
            "with the National Records of Scotland or GRONI in Northern Ireland. "
            "The Belize High Commission in London can advise on documentation "
            "requirements for the General Registry Office. Belize joined the "
            "Hague Apostille Convention in 2019. "
            "(FCDO Travel Advice: Belize, 2025; General Registry Office, "
            "Ministry of Human Development, Belize, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'belize',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a substantial Belizean diaspora community, "
            "concentrated in New York City, Los Angeles, and Chicago, with "
            "strong family ties to Belize. The US is also one of the largest "
            "sources of tourists to Belize, and many American retirees live "
            "in Belize. When a Belizean national or a person with Belizean "
            "family connections dies in the United States, the death is "
            "registered with the state civil records office where the death "
            "occurred. The Belize Embassy in Washington DC can advise on "
            "documentation requirements for the General Registry Office. "
            "Belize joined the Hague Apostille Convention in 2019; US-issued "
            "apostille certificates are accepted. "
            "(FCDO Travel Advice: Belize, 2025; General Registry Office, "
            "Belize, 2025.)"
        ),
    },
    {
        'origin': 'canada', 'dest': 'belize',
        'embassy_city': 'Ottawa',
        'intro': (
            "Canada has a Belizean diaspora community, with Belizean nationals "
            "concentrated in Toronto and other Ontario cities. Within the "
            "Caribbean Community (CARICOM), Canada maintains development and "
            "immigration ties with Belize. When a Belizean national dies in "
            "Canada and their family wishes to repatriate remains to Belize, "
            "the death is registered with the provincial civil records registry. "
            "The Belize High Commission in Ottawa can advise on documentation "
            "requirements for the General Registry Office. Belize joined the "
            "Hague Apostille Convention in 2019; Canadian-issued apostille "
            "certificates are accepted. "
            "(FCDO Travel Advice: Belize, 2025; General Registry Office, "
            "Belize, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'belize',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains diplomatic and development relations with Belize. "
            "Germany does not maintain a resident embassy in Belmopan; German "
            "nationals in Belize are advised to contact the German Embassy in "
            "Guatemala City, Guatemala. Belize is a destination for German "
            "eco-tourists and divers drawn to the Belize Barrier Reef. When "
            "a Belizean national dies in Germany and their family wishes to "
            "repatriate remains to Belize, the death is registered with the "
            "local Standesamt (civil registry). The Sterbeurkunde is issued "
            "in German. The Belize Embassy in Berlin can advise on "
            "documentation requirements for the General Registry Office. "
            "Belize joined the Hague Apostille Convention in 2019; German-"
            "issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Belize, 2025; General Registry Office, "
            "Belize, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'belize',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains diplomatic relations with Belize. France does "
            "not maintain a resident embassy in Belmopan; French nationals "
            "in Belize are advised to contact the French Embassy in Mexico "
            "City or the French Embassy in Guatemala City, depending on "
            "their location. When a Belizean national dies in France and "
            "their family wishes to repatriate remains to Belize, the death "
            "is registered with the local mairie (town hall). The acte de "
            "deces is issued in French. The Belize Embassy in Paris can "
            "advise on documentation requirements for the General Registry "
            "Office. Belize joined the Hague Apostille Convention in 2019; "
            "French-issued apostille certificates are accepted. "
            "(FCDO Travel Advice: Belize, 2025; General Registry Office, "
            "Belize, 2025.)"
        ),
    },
    # R76 -- Gambia x5
    {
        'origin': 'united-kingdom', 'dest': 'gambia',
        'embassy_city': 'London',
        'intro': (
            "The Gambia is a Commonwealth member and the United Kingdom is home "
            "to one of the largest Gambian diaspora communities outside West "
            "Africa, concentrated in London, Birmingham, and other cities. The "
            "Gambia is also among the most popular West African holiday "
            "destinations for British tourists, known as the Smiling Coast. "
            "The British High Commission in Banjul is fully operational. When "
            "someone from the United Kingdom dies and their family wishes to "
            "repatriate remains to The Gambia, the death must be registered at "
            "the local register office in England and Wales within 5 days, or "
            "with the National Records of Scotland or GRONI in Northern Ireland. "
            "The Gambia High Commission in London can advise on documentation "
            "requirements for the General Register Office. The Gambia is not "
            "a Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: The Gambia, 2025; General Register Office, "
            "The Gambia, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'gambia',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Gambian diaspora community, with nationals "
            "concentrated in the Washington DC metropolitan area, New York, and "
            "Philadelphia. The US maintains development and diplomatic ties with "
            "The Gambia, and the US Embassy in Banjul is operational. When a "
            "Gambian national or a person with Gambian family connections dies "
            "in the United States, the death is registered with the state civil "
            "records office where the death occurred. The Gambia Embassy in "
            "Washington DC can advise on documentation requirements for the "
            "General Register Office. The Gambia is not a Hague Apostille "
            "Convention member; full consular authentication is required. "
            "(FCDO Travel Advice: The Gambia, 2025; General Register Office, "
            "The Gambia, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'gambia',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany has a Gambian diaspora community in cities including "
            "Hamburg, Berlin, and Munich, and The Gambia is a destination "
            "for German tourists seeking winter sunshine. Germany does not "
            "maintain a resident embassy in Banjul; German nationals in "
            "The Gambia are advised to contact the German Embassy in Dakar, "
            "Senegal. When a Gambian national dies in Germany and their "
            "family wishes to repatriate remains to The Gambia, the death "
            "is registered with the local Standesamt (civil registry). The "
            "Sterbeurkunde is issued in German and requires consular "
            "authentication for submission to the General Register Office. "
            "The Gambia Embassy in Berlin can advise on documentation "
            "requirements. The Gambia is not a Hague Apostille Convention "
            "member; full consular authentication is required. "
            "(FCDO Travel Advice: The Gambia, 2025; General Register Office, "
            "The Gambia, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'gambia',
        'embassy_city': 'Paris',
        'intro': (
            "France has a Gambian diaspora community in Paris and other cities, "
            "and The Gambia is surrounded on three sides by Senegal, a "
            "Francophone country with which France has close ties. The French "
            "Embassy in Dakar, Senegal, covers The Gambia for French nationals "
            "in The Gambia. When a Gambian national dies in France and their "
            "family wishes to repatriate remains to The Gambia, the death is "
            "registered with the local mairie (town hall). The acte de deces "
            "is issued in French and requires consular authentication for "
            "submission to the General Register Office. The Gambia Embassy "
            "in Paris can advise on documentation requirements. The Gambia "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: The Gambia, 2025; General Register Office, "
            "The Gambia, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'gambia',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain has a Gambian diaspora community in cities including Madrid, "
            "Barcelona, and Bilbao, with Gambian nationals working in the "
            "agricultural, hospitality, and service sectors. The Canary Islands, "
            "a Spanish autonomous community off the West African coast, are also "
            "a transit point with proximity to West Africa. The Spanish Embassy "
            "in Dakar, Senegal, covers The Gambia for Spanish nationals there. "
            "When a Gambian national dies in Spain and their family wishes to "
            "repatriate remains to The Gambia, the death is registered with the "
            "local Registro Civil (civil registry). The certificado de defuncion "
            "is issued in Spanish and requires consular authentication for "
            "submission to the General Register Office in The Gambia. The "
            "Gambia Embassy in Madrid can advise on documentation requirements. "
            "The Gambia is not a Hague Apostille Convention member. "
            "(FCDO Travel Advice: The Gambia, 2025; General Register Office, "
            "The Gambia, 2025.)"
        ),
    },
    # R76 -- Sierra Leone x5
    {
        'origin': 'united-kingdom', 'dest': 'sierra-leone',
        'embassy_city': 'London',
        'intro': (
            "Sierra Leone is a Commonwealth member and the United Kingdom is "
            "home to one of the largest Sierra Leonean diaspora communities "
            "outside West Africa, with many families arriving in the UK during "
            "and after the 1991 to 2002 civil war. Strong family and cultural "
            "ties are maintained between the two countries. The British High "
            "Commission in Freetown is fully operational. When someone from "
            "the United Kingdom dies and their family wishes to repatriate "
            "remains to Sierra Leone, the death must be registered at the "
            "local register office in England and Wales within 5 days, or "
            "with the National Records of Scotland or GRONI in Northern "
            "Ireland. Families should be aware that Freetown Lungi Airport "
            "is across the estuary from Freetown, requiring additional "
            "transfer on arrival. The Sierra Leone High Commission in London "
            "can advise on documentation requirements. Sierra Leone is not "
            "a Hague Apostille Convention member. "
            "(FCDO Travel Advice: Sierra Leone, 2025; Office of the "
            "Administrator and Registrar General, Sierra Leone, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'sierra-leone',
        'embassy_city': 'Washington DC',
        'intro': (
            "The United States has a Sierra Leonean diaspora community, "
            "concentrated in the Washington DC and Maryland area, New York, "
            "and Atlanta, with significant numbers having arrived during the "
            "civil war period. The US also maintains substantial development "
            "and health partnerships with Sierra Leone. The US Embassy in "
            "Freetown is operational. When a Sierra Leonean national or a "
            "person with Sierra Leonean family connections dies in the United "
            "States, the death is registered with the state civil records "
            "office where the death occurred. The Sierra Leone Embassy in "
            "Washington DC can advise on documentation requirements for the "
            "Office of the Administrator and Registrar General. Sierra Leone "
            "is not a Hague Apostille Convention member; full consular "
            "authentication is required. "
            "(FCDO Travel Advice: Sierra Leone, 2025; Office of the "
            "Administrator and Registrar General, Sierra Leone, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'sierra-leone',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany maintains development cooperation with Sierra Leone through "
            "GIZ and other programmes, particularly in post-war reconstruction "
            "and governance. A small German community of development workers "
            "is present in Sierra Leone. The German Embassy in Freetown is "
            "operational. When a Sierra Leonean national dies in Germany and "
            "their family wishes to repatriate remains to Sierra Leone, the "
            "death is registered with the local Standesamt (civil registry). "
            "The Sterbeurkunde is issued in German and requires consular "
            "authentication for submission to the Office of the Administrator "
            "and Registrar General. The Sierra Leone Embassy in Berlin can "
            "advise on documentation requirements. Sierra Leone is not a "
            "Hague Apostille Convention member; full consular authentication "
            "is required. "
            "(FCDO Travel Advice: Sierra Leone, 2025; Office of the "
            "Administrator and Registrar General, Sierra Leone, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'sierra-leone',
        'embassy_city': 'Paris',
        'intro': (
            "France maintains diplomatic and development relations with "
            "Sierra Leone. A small French community of development workers "
            "is present in Sierra Leone, and Sierra Leone borders Guinea "
            "and Liberia, both Francophone countries, creating regional "
            "connections with the French-speaking world. The French Embassy "
            "in Freetown is operational. When a Sierra Leonean national "
            "dies in France and their family wishes to repatriate remains "
            "to Sierra Leone, the death is registered with the local "
            "mairie (town hall). The acte de deces is issued in French "
            "and requires consular authentication for submission to the "
            "Office of the Administrator and Registrar General. The Sierra "
            "Leone Embassy in Paris can advise on documentation requirements. "
            "Sierra Leone is not a Hague Apostille Convention member. "
            "(FCDO Travel Advice: Sierra Leone, 2025; Office of the "
            "Administrator and Registrar General, Sierra Leone, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'sierra-leone',
        'embassy_city': 'Madrid',
        'intro': (
            "Spain maintains diplomatic relations with Sierra Leone. A small "
            "Sierra Leonean community lives in Spain, with nationals working "
            "in the agricultural and service sectors. Spain does not maintain "
            "a resident embassy in Freetown; Spanish nationals in Sierra Leone "
            "are advised to contact the Spanish Embassy in Dakar, Senegal. "
            "When a Sierra Leonean national dies in Spain and their family "
            "wishes to repatriate remains to Sierra Leone, the death is "
            "registered with the local Registro Civil (civil registry). "
            "The certificado de defuncion is issued in Spanish and requires "
            "consular authentication for submission to the Office of the "
            "Administrator and Registrar General. The Sierra Leone Embassy "
            "in Madrid can advise on documentation requirements. Sierra "
            "Leone is not a Hague Apostille Convention member. "
            "(FCDO Travel Advice: Sierra Leone, 2025; Office of the "
            "Administrator and Registrar General, Sierra Leone, 2025.)"
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
