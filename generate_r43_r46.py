#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R43-R46.

   R43: Turkey wave 3 x5 + Malaysia wave 3 x5 + India wave 5 x5 +
        Singapore wave 5 x5 + Kuwait wave 5 x5 = 25

   R44: South Africa wave 6 x5 + USA wave 6 x5 + Germany wave 7 x5 +
        France wave 6 x5 + Oman wave 1 (NEW HUB) x5 = 25

   R45: Turkey wave 4 x5 + Malaysia wave 4 x5 + Oman wave 2 x5 +
        Switzerland wave 5 x5 + Sweden wave 5 x5 = 25

   R46: Norway wave 5 x5 + Oman wave 3 x5 + South Africa wave 7 x5 +
        Portugal wave 5 x5 + Japan wave 5 x5 = 25

   Template rotation: R42 ended on C (index 2). R43 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R42 ended C (index 2); R43 starts D (index 3)

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
    'turkey': {
        'name': 'Turkey',
        'slug': 'turkey',
        'key': 'tr',
        'reception': (
            "The Turkish funeral director (cenaze firmasi) takes custody at Istanbul "
            "Airport (IST) or Istanbul Sabiha Gokcen (SAW) cargo terminal. A transit "
            "certificate (transit belgesi) must accompany the remains. The municipality "
            "(belediye) registers the death in the nufus mudurlugu (population directorate). "
            "The Turkish Ministry of Health clearance is required before burial or cremation. "
            "All foreign documents not in Turkish require certified Turkish translation. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Turkish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Turkey. Turkish Ministry of Foreign Affairs emergency "
            "line: +90 312 292 2000 (24 hours). The Turkish Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Turkish funeral director (cenaze firmasi) takes custody at Istanbul "
            "Airport (IST) cargo terminal. A transit certificate (transit belgesi) must "
            "accompany the remains. The municipality (belediye) registers the death. "
            "The Turkish Ministry of Health clearance is required. All foreign documents "
            "require certified Turkish translation. The receiving funeral director "
            "coordinates with local municipal authorities."
        ),
        'emergency_line': '+90 312 292 2000',
        'hub_url': 'repatriation-from-turkey',
    },
    'malaysia': {
        'name': 'Malaysia',
        'slug': 'malaysia',
        'key': 'my',
        'reception': (
            "The Malaysian funeral director takes custody at Kuala Lumpur International "
            "Airport (KUL) cargo terminal. Malaysia Customs clearance is required. The "
            "National Registration Department (NRD) registers the death. The Ministry of "
            "Health may require clearance for final disposition. All foreign documents "
            "must be authenticated by the Malaysian Embassy or High Commission in the "
            "country of origin. Documents not in Malay or English require certified "
            "translation. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Malaysian High Commission or Embassy in {city} can advise on documentation "
            "requirements and authenticate foreign certificates. They cannot pay for or "
            "arrange repatriation. Malaysian Ministry of Foreign Affairs 24-hour "
            "emergency: +603 8000 8000."
        ),
        'arrival_faq': (
            "The Malaysian funeral director takes custody at Kuala Lumpur International "
            "Airport (KUL) cargo terminal. Malaysia Customs clearance requires the "
            "authenticated death certificate, transit permit, and health clearance. "
            "The National Registration Department (NRD) registers the death. All foreign "
            "documents must be authenticated by the Malaysian Embassy in the origin "
            "country. The Ministry of Health may need to be notified."
        ),
        'emergency_line': '+603 8000 8000',
        'hub_url': 'repatriation-from-malaysia',
    },
    'india': {
        'name': 'India',
        'slug': 'india',
        'key': 'in',
        'reception': (
            "The Indian funeral director takes custody at the nearest international "
            "airport cargo terminal, commonly Indira Gandhi International (DEL, Delhi), "
            "Chhatrapati Shivaji Maharaj International (BOM, Mumbai), or Kempegowda "
            "International (BLR, Bangalore). The local civil registrar records the death "
            "under the Registration of Births and Deaths Act 1969. State regulations "
            "govern burial or cremation. All foreign documents must be authenticated by "
            "the Indian Embassy or High Commission in the country of origin. Documents "
            "not in English or Hindi require certified English translation. "
            "(Indian Ministry of External Affairs, 2025.)"
        ),
        'consular_template': (
            "Indian Embassy or High Commission in {city} can advise on documentation "
            "requirements and authenticate foreign certificates. They cannot pay for or "
            "arrange repatriation. Indian Ministry of External Affairs 24-hour "
            "emergency: +91 11 2301 2113."
        ),
        'arrival_faq': (
            "The Indian funeral director takes custody at the nearest international "
            "airport cargo terminal. The local civil registrar records the death under "
            "the Registration of Births and Deaths Act 1969. All foreign documents must "
            "be authenticated by the Indian Embassy in the origin country. State "
            "regulations govern burial or cremation. The receiving funeral director "
            "coordinates with local authorities."
        ),
        'emergency_line': '+91 11 2301 2113',
        'hub_url': 'repatriation-from-india',
    },
    'singapore': {
        'name': 'Singapore',
        'slug': 'singapore',
        'key': 'sg',
        'reception': (
            "The Singapore funeral director takes custody at Changi Airport (SIN) cargo "
            "terminal. Singapore Customs clearance is required. The National Environment "
            "Agency (NEA) regulates the import of human remains into Singapore. All "
            "foreign death certificates must be authenticated by the Singapore Embassy "
            "or High Commission in the country of origin. Documents not in English "
            "require certified English translation. "
            "(Singapore Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Singapore High Commission or Embassy in {city} can advise on documentation "
            "requirements and authenticate foreign certificates. They cannot pay for or "
            "arrange repatriation. Singapore Ministry of Foreign Affairs 24-hour "
            "emergency: +65 6379 8000."
        ),
        'arrival_faq': (
            "The Singapore funeral director takes custody at Changi Airport (SIN) cargo "
            "terminal. Singapore Customs clearance requires the authenticated death "
            "certificate, transit permit, and embalming certificate. The National "
            "Environment Agency (NEA) regulates import of remains. All foreign documents "
            "must be authenticated by the Singapore Embassy in the origin country."
        ),
        'emergency_line': '+65 6379 8000',
        'hub_url': 'repatriation-from-singapore',
    },
    'kuwait': {
        'name': 'Kuwait',
        'slug': 'kuwait',
        'key': 'kw',
        'reception': (
            "The Kuwaiti funeral home takes custody at Kuwait International Airport (KWI) "
            "cargo terminal. The Ministry of Interior (Civil ID directorate) records the "
            "death. Muslim remains require procedures in accordance with Islamic law and "
            "the Ministry of Awqaf and Islamic Affairs may be involved. A Kuwaiti health "
            "authority clearance is required before any final disposition. All foreign "
            "documents not in Arabic require certified Arabic translation. Authentication "
            "by the Kuwaiti Embassy in the country of origin is required. "
            "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Kuwaiti Embassy in {city} can advise on documentation requirements for "
            "repatriation to Kuwait. Kuwaiti Ministry of Foreign Affairs emergency "
            "line: +965 2243 4567 (24 hours). The Kuwaiti Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Kuwaiti funeral home takes custody at Kuwait International Airport (KWI) "
            "cargo terminal. Ministry of Interior clearance is required. All foreign "
            "documents must be authenticated by the Kuwaiti Embassy in the origin country "
            "and require certified Arabic translation. Muslim remains are handled in "
            "accordance with Islamic law. The receiving funeral home coordinates with "
            "local health authorities."
        ),
        'emergency_line': '+965 2243 4567',
        'hub_url': 'repatriation-from-kuwait',
    },
    'south-africa': {
        'name': 'South Africa',
        'slug': 'south-africa',
        'key': 'za',
        'reception': (
            "The South African funeral director takes custody at the cargo terminal, "
            "typically O.R. Tambo International (JNB, Johannesburg), Cape Town "
            "International (CPT), or King Shaka International (DUR, Durban). A permit "
            "from the South African Department of Home Affairs (Form DHA-1744) is "
            "required before burial or cremation. The provincial health authority "
            "issues any additional permits. "
            "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
        ),
        'consular_template': (
            "South African Embassy or High Commission in {city} can advise on "
            "documentation requirements for repatriation to South Africa. They cannot "
            "pay for or arrange repatriation. Contact the nearest South African mission "
            "for assistance."
        ),
        'arrival_faq': (
            "The South African funeral director takes custody at the cargo terminal. "
            "Department of Home Affairs Form DHA-1744 is required before burial or "
            "cremation. The provincial health authority may issue additional permits. "
            "The receiving funeral director coordinates with the local registrar."
        ),
        'emergency_line': 'contact nearest South African mission',
        'hub_url': 'repatriation-from-south-africa',
    },
    'united-states': {
        'name': 'United States',
        'slug': 'united-states',
        'key': 'us',
        'reception': (
            "The US funeral director takes custody at the cargo terminal. "
            "US Customs clearance requires a transit or burial permit, the foreign death "
            "certificate, and an embalming certificate. State health department regulations "
            "apply and vary by state. The receiving funeral director notifies the medical "
            "examiner or coroner as required by state law. "
            "(US State Department, Bureau of Consular Affairs, 2025.)"
        ),
        'consular_template': (
            "US Embassy in {city} can assist US citizens and their families with "
            "consular registration of the death and provide a list of local funeral "
            "directors. They cannot pay for or arrange repatriation. State Department "
            "emergency line: +1 (888) 407-4747 (within the US) or +1 (202) 501-4444 "
            "(from overseas), 24 hours."
        ),
        'arrival_faq': (
            "The US funeral director takes custody at the cargo terminal. US Customs "
            "clearance requires the foreign death certificate, transit or burial permit, "
            "and embalming certificate. State regulations govern burial or cremation. "
            "The receiving funeral director notifies the medical examiner or coroner "
            "as required."
        ),
        'emergency_line': '+1 (202) 501-4444',
        'hub_url': 'repatriation-from-united-states',
    },
    'germany': {
        'name': 'Germany',
        'slug': 'germany',
        'key': 'de',
        'reception': (
            "The German funeral director takes custody at the cargo terminal, typically "
            "Frankfurt (FRA), Munich (MUC), or Berlin (BER). A Leichenpass (body "
            "transport passport) or equivalent laissez-passer must accompany the remains. "
            "The local Gesundheitsamt (public health authority) may inspect the remains "
            "on arrival. The receiving funeral director registers the death with the "
            "local Standesamt (civil registry) if required. "
            "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
        ),
        'consular_template': (
            "German Embassy in {city} can advise on document requirements for "
            "repatriation to Germany. Federal Foreign Office (Auswaertiges Amt) "
            "emergency assistance: +49 30 5000 2000 (24 hours). The German Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The German funeral director takes custody at the cargo terminal. "
            "A Leichenpass or laissez-passer must accompany the remains. "
            "The Gesundheitsamt may inspect the remains. The death is registered with "
            "the local Standesamt. All foreign documents must carry certified German "
            "translation where required."
        ),
        'emergency_line': '+49 30 5000 2000',
        'hub_url': 'repatriation-from-germany',
    },
    'france': {
        'name': 'France',
        'slug': 'france',
        'key': 'fr',
        'reception': (
            "The French funeral director (pompes funebres) takes custody at Charles de "
            "Gaulle (CDG, Paris) or another French international airport. The prefecture "
            "may require a permis d'inhumer (burial permit) or transport authorisation "
            "before burial or cremation can proceed. All foreign documents must carry a "
            "certified French translation. "
            "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
        ),
        'consular_template': (
            "French Embassy in {city} can advise on repatriation documentation "
            "requirements for France. French Ministry of Europe and Foreign Affairs "
            "(MAE) emergency assistance: +33 1 43 17 67 67 (24 hours). The French "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The French funeral director takes custody at Charles de Gaulle (CDG) or "
            "another French airport. The prefecture issues a permis d'inhumer before "
            "burial or cremation. All foreign documents require certified French "
            "translation. The receiving funeral director coordinates with local "
            "authorities."
        ),
        'emergency_line': '+33 1 43 17 67 67',
        'hub_url': 'repatriation-from-france',
    },
    'oman': {
        'name': 'Oman',
        'slug': 'oman',
        'key': 'om',
        'reception': (
            "The Omani funeral director takes custody at Muscat International Airport "
            "(MCT) cargo terminal. The Royal Oman Police registers the death and a "
            "burial permit from the Ministry of Health is required before any final "
            "disposition. Muslim remains are handled in accordance with Islamic law. "
            "All foreign documents not in Arabic require certified Arabic translation. "
            "Authentication by the Omani Embassy in the country of origin is required. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Omani Embassy in {city} can advise on documentation requirements for "
            "repatriation to Oman. Oman Ministry of Foreign Affairs can be reached "
            "via the Omani Embassy during business hours. The Omani Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Omani funeral director takes custody at Muscat International Airport "
            "(MCT) cargo terminal. The Royal Oman Police registers the death. A burial "
            "permit from the Ministry of Health is required. Muslim remains are handled "
            "in accordance with Islamic law. All foreign documents require certified "
            "Arabic translation and authentication by the Omani Embassy in the origin "
            "country."
        ),
        'emergency_line': 'contact Omani Embassy in origin country',
        'hub_url': 'repatriation-from-oman',
    },
    'switzerland': {
        'name': 'Switzerland',
        'slug': 'switzerland',
        'key': 'ch',
        'reception': (
            "The Swiss Bestatter (funeral director) takes custody at Zurich (ZRH) or "
            "Geneva (GVA) cargo terminal. A Leichentransportschein (body transport permit) "
            "must accompany the coffin. The Zivilstandsamt (civil registry) registers the "
            "death. The Kantonsarzt (cantonal health officer) may inspect the remains on "
            "arrival. Switzerland is a Hague Apostille Convention member. Documents not in "
            "German, French, or Italian require certified translation. "
            "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
        'consular_template': (
            "Swiss Embassy in {city} can advise on documentation requirements for "
            "repatriation to Switzerland. Swiss Federal Department of Foreign Affairs "
            "(FDFA) helpline for Swiss residents abroad: +41 800 24-7-365 (24 hours). "
            "The Swiss Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Swiss Bestatter (funeral director) takes custody at Zurich (ZRH) or "
            "Geneva (GVA) cargo terminal. A Leichentransportschein must accompany the "
            "coffin. The Zivilstandsamt registers the death. The Kantonsarzt may inspect "
            "the remains on arrival. Documents not in German, French, or Italian require "
            "certified translation. The receiving funeral director coordinates with the "
            "cantonal authorities."
        ),
        'emergency_line': '+41 800 24-7-365',
        'hub_url': 'repatriation-from-switzerland',
    },
    'sweden': {
        'name': 'Sweden',
        'slug': 'sweden',
        'key': 'se',
        'reception': (
            "The Swedish begravningsentreprenor (funeral director) takes custody at "
            "Stockholm Arlanda (ARN) or Gothenburg Landvetter (GOT) cargo terminal. "
            "A laissez-passer must accompany the remains. Skatteverket (Swedish Tax "
            "Agency) is notified to update the population register. Sweden is an EU "
            "and Hague Apostille Convention member. Documents not in Swedish or English "
            "require certified Swedish translation. "
            "(Swedish Ministry of Foreign Affairs, UD, 2025.)"
        ),
        'consular_template': (
            "Swedish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Sweden. Swedish Ministry of Foreign Affairs emergency "
            "line: +46 8 405 50 05 (24 hours). The Swedish Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Swedish begravningsentreprenor (funeral director) takes custody at "
            "Stockholm Arlanda (ARN) or Gothenburg Landvetter (GOT) cargo terminal. "
            "A laissez-passer must accompany the remains. Skatteverket is notified to "
            "update the population register. Documents not in Swedish or English require "
            "certified Swedish translation. The receiving funeral director coordinates "
            "with local authorities."
        ),
        'emergency_line': '+46 8 405 50 05',
        'hub_url': 'repatriation-from-sweden',
    },
    'norway': {
        'name': 'Norway',
        'slug': 'norway',
        'key': 'no',
        'reception': (
            "The Norwegian begravelsesbyraa (funeral director) takes custody at Oslo "
            "Gardermoen (OSL) cargo terminal. A laissez-passer or equivalent body "
            "transport document must accompany the coffin. The Folkeregisteret (National "
            "Population Register) records the death. Norway is a Hague Apostille "
            "Convention member (EEA, not EU). Documents not in Norwegian or English "
            "require certified Norwegian translation. "
            "(Norwegian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Norwegian Embassy in {city} can advise on documentation requirements for "
            "repatriation to Norway. Norwegian Ministry of Foreign Affairs emergency "
            "line: +47 23 95 00 00 (24 hours). The Norwegian Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Norwegian begravelsesbyraa (funeral director) takes custody at Oslo "
            "Gardermoen (OSL) cargo terminal. A laissez-passer must accompany the "
            "coffin. The Folkeregisteret records the death. Documents not in Norwegian "
            "or English require certified Norwegian translation. The receiving funeral "
            "director coordinates with local authorities."
        ),
        'emergency_line': '+47 23 95 00 00',
        'hub_url': 'repatriation-from-norway',
    },
    'portugal': {
        'name': 'Portugal',
        'slug': 'portugal',
        'key': 'pt',
        'reception': (
            "The Portuguese agencia funeraria (funeral director) takes custody at Lisbon "
            "(LIS), Porto (OPO), or Faro (FAO) cargo terminal. An Autoridade de Saude "
            "(health authority) clearance is required before burial or cremation can "
            "proceed. The Conservatoria do Registo Civil registers the death. Portugal "
            "is an EU and Hague Apostille Convention member. Documents from non-EU "
            "countries require certified Portuguese translation. "
            "(Portuguese Ministry of Foreign Affairs, MNE, 2025.)"
        ),
        'consular_template': (
            "Portuguese Embassy in {city} can advise on documentation requirements for "
            "repatriation to Portugal. Portuguese Ministry of Foreign Affairs (MNE) "
            "emergency assistance: +351 21 394 67 00 (24 hours). The Portuguese Embassy "
            "cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Portuguese funeral director takes custody at Lisbon (LIS) or Porto "
            "(OPO) cargo terminal. The Autoridade de Saude issues clearance before "
            "burial or cremation. The Conservatoria do Registo Civil registers the death. "
            "Documents not in Portuguese require certified translation. The receiving "
            "funeral director coordinates with local authorities."
        ),
        'emergency_line': '+351 21 394 67 00',
        'hub_url': 'repatriation-from-portugal',
    },
    'japan': {
        'name': 'Japan',
        'slug': 'japan',
        'key': 'jp',
        'reception': (
            "The Japanese funeral director takes custody at Narita International (NRT) "
            "or Tokyo Haneda (HND) cargo terminal, or Osaka Kansai International (KIX) "
            "for western Japan. The local municipal office registers the death in the "
            "koseki (family registry). Cremation is standard in Japan and a cremation "
            "permit from the municipal office is required. All foreign documents must be "
            "authenticated by the Japanese Embassy or consulate in the country of origin. "
            "Documents not in Japanese require certified Japanese translation. "
            "(Japanese Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Japanese Embassy in {city} can advise on documentation requirements for "
            "repatriation to Japan. Japanese Ministry of Foreign Affairs emergency "
            "assistance: +81 3 3580 3311 (24 hours). The Japanese Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Japanese funeral director takes custody at Narita (NRT) or Haneda "
            "(HND) cargo terminal. The municipal office registers the death in the "
            "koseki. Cremation is standard and requires a municipal permit. All foreign "
            "documents must be authenticated by the Japanese Embassy in the origin "
            "country and require certified Japanese translation."
        ),
        'emergency_line': '+81 3 3580 3311',
        'hub_url': 'repatriation-from-japan',
    },
}

# ---------------------------------------------------------------------------
# Embassy cities: destination country embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R43: Turkey wave 3
    ('russia',        'turkey'): 'Moscow',
    ('saudi-arabia',  'turkey'): 'Riyadh',
    ('jordan',        'turkey'): 'Amman',
    ('algeria',       'turkey'): 'Algiers',
    ('china',         'turkey'): 'Beijing',
    # R43: Malaysia wave 3
    ('sri-lanka',     'malaysia'): 'Colombo',
    ('pakistan',      'malaysia'): 'Islamabad',
    ('south-korea',   'malaysia'): 'Seoul',
    ('laos',          'malaysia'): 'Vientiane',
    ('hong-kong',     'malaysia'): 'Hong Kong',
    # R43: India wave 5
    ('iraq',          'india'): 'Baghdad',
    ('russia',        'india'): 'Moscow',
    ('jordan',        'india'): 'Amman',
    ('turkey',        'india'): 'Ankara',
    ('ethiopia',      'india'): 'Addis Ababa',
    # R43: Singapore wave 5
    ('ethiopia',      'singapore'): 'Addis Ababa',
    ('ghana',         'singapore'): 'Accra',
    ('morocco',       'singapore'): 'Rabat',
    ('turkey',        'singapore'): 'Ankara',
    ('iraq',          'singapore'): 'Baghdad',
    # R43: Kuwait wave 5
    ('russia',        'kuwait'): 'Moscow',
    ('algeria',       'kuwait'): 'Algiers',
    ('morocco',       'kuwait'): 'Rabat',
    ('uzbekistan',    'kuwait'): 'Tashkent',
    ('ukraine',       'kuwait'): 'Kyiv',
    # R44: South Africa wave 6
    ('ukraine',       'south-africa'): 'Kyiv',
    ('russia',        'south-africa'): 'Moscow',
    ('indonesia',     'south-africa'): 'Jakarta',
    ('bangladesh',    'south-africa'): 'Dhaka',
    ('egypt',         'south-africa'): 'Cairo',
    # R44: USA wave 6
    ('jordan',        'united-states'): 'Amman',
    ('algeria',       'united-states'): 'Algiers',
    ('uzbekistan',    'united-states'): 'Tashkent',
    ('nicaragua',     'united-states'): 'Managua',
    ('costa-rica',    'united-states'): 'San Jose',
    # R44: Germany wave 7
    ('thailand',      'germany'): 'Bangkok',
    ('myanmar',       'germany'): 'Yangon',
    ('south-africa',  'germany'): 'Pretoria',
    ('brazil',        'germany'): 'Brasilia',
    ('colombia',      'germany'): 'Bogota',
    # R44: France wave 6
    ('ethiopia',      'france'): 'Addis Ababa',
    ('kenya',         'france'): 'Nairobi',
    ('sri-lanka',     'france'): 'Colombo',
    ('nepal',         'france'): 'Kathmandu',
    ('myanmar',       'france'): 'Yangon',
    # R44: Oman wave 1 (new hub)
    ('india',         'oman'): 'New Delhi',
    ('pakistan',      'oman'): 'Islamabad',
    ('bangladesh',    'oman'): 'Dhaka',
    ('nepal',         'oman'): 'Kathmandu',
    ('philippines',   'oman'): 'Manila',
    # R45: Turkey wave 4
    ('nigeria',       'turkey'): 'Abuja',
    ('ghana',         'turkey'): 'Accra',
    ('kenya',         'turkey'): 'Nairobi',
    ('ethiopia',      'turkey'): 'Addis Ababa',
    ('bangladesh',    'turkey'): 'Dhaka',
    # R45: Malaysia wave 4
    ('nigeria',       'malaysia'): 'Abuja',
    ('ghana',         'malaysia'): 'Accra',
    ('kenya',         'malaysia'): 'Nairobi',
    ('ethiopia',      'malaysia'): 'Addis Ababa',
    ('saudi-arabia',  'malaysia'): 'Riyadh',
    # R45: Oman wave 2
    ('ethiopia',      'oman'): 'Addis Ababa',
    ('kenya',         'oman'): 'Nairobi',
    ('sri-lanka',     'oman'): 'Colombo',
    ('indonesia',     'oman'): 'Jakarta',
    ('egypt',         'oman'): 'Cairo',
    # R45: Switzerland wave 5
    ('nigeria',       'switzerland'): 'Abuja',
    ('iran',          'switzerland'): 'Tehran',
    ('bangladesh',    'switzerland'): 'Dhaka',
    ('indonesia',     'switzerland'): 'Jakarta',
    ('vietnam',       'switzerland'): 'Hanoi',
    # R45: Sweden wave 5
    ('ghana',         'sweden'): 'Accra',
    ('senegal',       'sweden'): 'Dakar',
    ('pakistan',      'sweden'): 'Islamabad',
    ('ukraine',       'sweden'): 'Kyiv',
    ('indonesia',     'sweden'): 'Jakarta',
    # R46: Norway wave 5
    ('ghana',         'norway'): 'Accra',
    ('senegal',       'norway'): 'Dakar',
    ('indonesia',     'norway'): 'Jakarta',
    ('egypt',         'norway'): 'Cairo',
    ('algeria',       'norway'): 'Algiers',
    # R46: Oman wave 3
    ('turkey',        'oman'): 'Ankara',
    ('iraq',          'oman'): 'Baghdad',
    ('iran',          'oman'): 'Tehran',
    ('jordan',        'oman'): 'Amman',
    ('morocco',       'oman'): 'Rabat',
    # R46: South Africa wave 7
    ('malaysia',      'south-africa'): 'Kuala Lumpur',
    ('vietnam',       'south-africa'): 'Hanoi',
    ('philippines',   'south-africa'): 'Manila',
    # South African High Commission covers Nepal from New Delhi
    ('nepal',         'south-africa'): 'New Delhi',
    # South African Embassy covers Myanmar from Bangkok
    ('myanmar',       'south-africa'): 'Bangkok',
    # R46: Portugal wave 5
    ('ghana',         'portugal'): 'Accra',
    ('ethiopia',      'portugal'): 'Addis Ababa',
    ('iraq',          'portugal'): 'Baghdad',
    ('egypt',         'portugal'): 'Cairo',
    ('algeria',       'portugal'): 'Algiers',
    # R46: Japan wave 5
    ('south-africa',  'japan'): 'Pretoria',
    ('nigeria',       'japan'): 'Abuja',
    ('ghana',         'japan'): 'Accra',
    ('ethiopia',      'japan'): 'Addis Ababa',
    ('kenya',         'japan'): 'Nairobi',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R43: Turkey wave 3
    ('russia', 'turkey'): (
        "Russian nationals form one of the largest tourist communities in Turkey, "
        "with millions of Russian visitors to Antalya, Istanbul, and the Aegean coast "
        "each year. Since 2022, Turkey has also become a significant destination for "
        "Russian nationals relocating abroad, with a substantial community in Istanbul. "
        "Russia and Turkey have extensive bilateral trade and energy ties, including the "
        "TurkStream pipeline project. Russian documentation requires certified Turkish "
        "translation for Turkish civil registry (belediye) purposes. The Turkish Embassy "
        "in Moscow handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('saudi-arabia', 'turkey'): (
        "Saudi Arabian nationals visit Turkey in large numbers for tourism, medical "
        "treatment, and business, with Turkey being a popular destination for Gulf "
        "travellers. Saudi Arabia and Turkey are both OIC member states and have "
        "significant bilateral trade and investment ties. Arabic documentation from "
        "Saudi Arabia is not automatically accepted by Turkish civil registry authorities "
        "and requires certified Turkish translation. The Turkish Embassy in Riyadh "
        "handles consular matters."
    ),
    ('jordan', 'turkey'): (
        "Jordanian nationals in Turkey include students, business professionals, and "
        "travellers. Jordan and Turkey have close bilateral diplomatic ties as fellow "
        "OIC member states with shared historical connections through the Ottoman period. "
        "Jordanian nationals travel to Turkey for tourism, trade, and medical treatment. "
        "Arabic documentation from Jordan requires certified Turkish translation for "
        "Turkish civil registry purposes. The Turkish Embassy in Amman handles consular "
        "matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('algeria', 'turkey'): (
        "Algerian nationals in Turkey include students, business professionals, and "
        "workers in trade sectors, with Turkey and Algeria having growing economic ties. "
        "Algeria and Turkey are both OIC member states with bilateral trade agreements "
        "and close diplomatic relations. Turkish construction companies have significant "
        "operations in Algeria, creating business travel in both directions. Arabic "
        "documentation from Algeria requires certified Turkish translation for Turkish "
        "civil registry purposes. The Turkish Embassy in Algiers handles consular matters."
    ),
    ('china', 'turkey'): (
        "Chinese nationals in Turkey include tourists, business professionals, and workers "
        "in trade sectors, with Turkey sitting on the Belt and Road Initiative corridor "
        "linking China to European markets. China and Turkey have bilateral trade and "
        "investment ties, with the Istanbul textile and manufacturing sectors drawing "
        "Chinese business activity. Mandarin documentation from China requires certified "
        "Turkish translation for Turkish civil registry (belediye) purposes. The Turkish "
        "Embassy in Beijing handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    # R43: Malaysia wave 3
    ('sri-lanka', 'malaysia'): (
        "Sri Lankan nationals form a significant migrant worker community in Malaysia, "
        "employed in plantation, domestic service, and manufacturing sectors under "
        "bilateral labour agreements. Malaysia and Sri Lanka have longstanding trade "
        "ties as fellow Commonwealth members and IORA partners. The Sri Lankan Tamil "
        "community has historical connections to Malaysia's plantation sector, and Sri "
        "Lankan workers continue to fill essential roles across the country. Sinhala "
        "and Tamil documentation requires certified Malay or English translation for "
        "Malaysian National Registration Department (NRD) purposes. The Malaysian High "
        "Commission in Colombo handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('pakistan', 'malaysia'): (
        "Pakistani nationals in Malaysia include workers in retail, hospitality, and "
        "trade sectors, alongside students at Malaysian universities. Pakistan and "
        "Malaysia have bilateral trade ties and both are OIC member states, with "
        "shared Islamic heritage creating a diaspora connection. Malaysian universities "
        "actively recruit Pakistani students, making education a significant corridor "
        "between the two countries. Urdu documentation from Pakistan requires certified "
        "Malay or English translation for Malaysian NRD purposes. The Malaysian High "
        "Commission in Islamabad handles consular matters."
    ),
    ('south-korea', 'malaysia'): (
        "South Korean nationals in Malaysia include electronics and manufacturing "
        "industry professionals, students at English-language programmes, and an "
        "established community of retirees under Malaysia's My Second Home programme. "
        "South Korea and Malaysia have bilateral trade ties and ASEAN-Korea Free Trade "
        "Agreement links. Korean documentation requires certified Malay or English "
        "translation for Malaysian NRD purposes. The Malaysian Embassy in Seoul handles "
        "consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('laos', 'malaysia'): (
        "Laotian nationals in Malaysia include workers in manufacturing and service "
        "sectors, part of the ASEAN labour mobility network. Laos and Malaysia share "
        "ASEAN membership and bilateral trade ties. Lao documentation requires certified "
        "Malay or English translation for Malaysian National Registration Department "
        "(NRD) purposes. The Malaysian Embassy in Vientiane handles consular matters."
    ),
    ('hong-kong', 'malaysia'): (
        "Hong Kong nationals form a notable community in Malaysia, with growing numbers "
        "relocating for business, property investment, and education following political "
        "changes in Hong Kong since 2019. Malaysia's My Second Home programme has "
        "attracted Hong Kong residents, and bilateral financial and trade ties are "
        "significant. Traditional Chinese documentation from Hong Kong requires certified "
        "Malay or English translation for Malaysian NRD purposes. The Malaysian Consulate "
        "General in Hong Kong handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    # R43: India wave 5
    ('iraq', 'india'): (
        "Iraqi nationals in India include patients seeking medical treatment at specialist "
        "Indian hospitals, students on educational programmes, and business professionals. "
        "India and Iraq have strong bilateral ties, with India being one of Iraq's largest "
        "oil importers. Iraqi medical tourism to India has grown substantially, with "
        "Delhi, Mumbai, and Chennai hosting significant numbers of Iraqi patients and "
        "their families. Arabic documentation from Iraq requires certified English "
        "translation for Indian civil registration purposes under the Registration of "
        "Births and Deaths Act 1969. The Indian Embassy in Baghdad handles consular "
        "matters. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    ('russia', 'india'): (
        "Russian nationals in India include tourists, students, and business professionals. "
        "Russia and India have a long-standing Special and Privileged Strategic Partnership, "
        "with strong bilateral ties in defence, space, energy, and pharmaceuticals. Russian "
        "tourist arrivals in India have grown, with Goa being a particularly popular "
        "destination. Russian documentation requires certified English translation for "
        "Indian civil registration purposes. The Indian Embassy in Moscow handles "
        "consular matters."
    ),
    ('jordan', 'india'): (
        "Jordanian nationals in India include students at Indian universities, business "
        "professionals, and medical tourists. India and Jordan have bilateral trade ties "
        "and diplomatic relations, with Jordan importing Indian pharmaceuticals, "
        "machinery, and manufactured goods. Arabic documentation from Jordan requires "
        "certified English translation for Indian civil registration purposes under the "
        "Registration of Births and Deaths Act 1969. The Indian Embassy in Amman handles "
        "consular matters. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    ('turkey', 'india'): (
        "Turkish nationals in India include business professionals in the textile, "
        "construction, and trade sectors, alongside tourists. India and Turkey have "
        "bilateral trade ties and both are G20 member states. Trade in textiles, "
        "chemicals, and engineering goods connects the two economies. Turkish "
        "documentation requires certified English translation for Indian civil "
        "registration purposes. The Indian Embassy in Ankara handles consular matters."
    ),
    ('ethiopia', 'india'): (
        "Ethiopian nationals in India include students at Indian universities and colleges "
        "under the Indian Technical and Economic Cooperation (ITEC) programme, alongside "
        "business professionals. India and Ethiopia have strong bilateral ties across "
        "education, technology, and trade, with India providing technical assistance "
        "and scholarships to Ethiopian nationals. Amharic documentation from Ethiopia "
        "requires certified English translation for Indian civil registration purposes "
        "under the Registration of Births and Deaths Act 1969. The Indian Embassy in "
        "Addis Ababa handles consular matters. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    # R43: Singapore wave 5
    ('ethiopia', 'singapore'): (
        "Ethiopian nationals in Singapore include professionals in aviation and logistics, "
        "given Ethiopian Airlines' status as Africa's largest carrier with Singapore as a "
        "key hub, alongside business professionals and students. Singapore and Ethiopia "
        "have growing bilateral trade ties, with Singapore companies investing in "
        "Ethiopian infrastructure and agriculture. Amharic documentation from Ethiopia "
        "requires certified English translation for Singapore National Environment Agency "
        "(NEA) purposes. The Singapore Embassy in Addis Ababa handles consular matters. "
        "(Singapore Ministry of Foreign Affairs, 2025.)"
    ),
    ('ghana', 'singapore'): (
        "Ghanaian nationals in Singapore include professionals in finance, technology, "
        "and education, alongside students at Singaporean universities. Singapore and "
        "Ghana have growing bilateral ties, with Singapore investors active in Ghanaian "
        "mining, agriculture, and infrastructure. English documentation from Ghana is "
        "generally understood by Singaporean authorities, though authentication by the "
        "Singapore High Commission is required. The Singapore High Commission in Accra "
        "handles consular matters."
    ),
    ('morocco', 'singapore'): (
        "Moroccan nationals in Singapore include professionals in the financial services "
        "and trade sectors, alongside students. Singapore and Morocco have bilateral "
        "trade ties, with Singapore a regional hub for Middle Eastern and African "
        "business connections. French and Arabic documentation from Morocco requires "
        "certified English translation for Singapore National Environment Agency (NEA) "
        "purposes. The Singapore Embassy in Rabat handles consular matters. "
        "(Singapore Ministry of Foreign Affairs, 2025.)"
    ),
    ('turkey', 'singapore'): (
        "Turkish nationals in Singapore include professionals in trade, finance, and "
        "technology sectors. Singapore is a significant hub for Turkish companies "
        "expanding into Southeast Asia, and bilateral trade between Turkey and Singapore "
        "spans manufacturing, logistics, and financial services. Turkish documentation "
        "requires certified English translation for Singapore NEA purposes. The Singapore "
        "Embassy in Ankara handles consular matters."
    ),
    ('iraq', 'singapore'): (
        "Iraqi nationals in Singapore include business professionals in the oil and gas "
        "sector, medical patients, and students. Singapore is a regional hub for energy "
        "trading, and Iraqi nationals use Singapore as a base for business in Southeast "
        "Asia. Arabic documentation from Iraq requires certified English translation for "
        "Singapore National Environment Agency (NEA) purposes. The Singapore Embassy "
        "in Baghdad handles consular matters. "
        "(Singapore Ministry of Foreign Affairs, 2025.)"
    ),
    # R43: Kuwait wave 5
    ('russia', 'kuwait'): (
        "Russian nationals in Kuwait include business professionals in the energy and "
        "construction sectors, alongside tourists. Kuwait and Russia have bilateral "
        "economic ties, with Russian companies active in Kuwaiti construction and "
        "industrial projects. Russian documentation requires certified Arabic translation "
        "for Kuwaiti Ministry of Interior purposes. The Kuwaiti Embassy in Moscow "
        "handles consular matters. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    ('algeria', 'kuwait'): (
        "Algerian nationals in Kuwait include workers in service, construction, and "
        "professional sectors. Algeria and Kuwait are fellow Arab League and OIC member "
        "states with bilateral diplomatic ties, and Kuwaiti development assistance has "
        "supported Algerian projects. Arabic documentation from Algeria is generally "
        "understood by Kuwaiti authorities, though official notarisation and embassy "
        "authentication are required. The Kuwaiti Embassy in Algiers handles consular "
        "matters."
    ),
    ('morocco', 'kuwait'): (
        "Moroccan nationals in Kuwait work in professional, service, and hospitality "
        "sectors. Morocco and Kuwait are OIC member states with close diplomatic ties, "
        "and Kuwaiti investment is present in Moroccan tourism and real estate. Arabic "
        "documentation from Morocco is generally understood by Kuwaiti authorities, "
        "though official notarisation and authentication by the Kuwaiti Embassy are "
        "required. The Kuwaiti Embassy in Rabat handles consular matters. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    ('uzbekistan', 'kuwait'): (
        "Uzbek nationals in Kuwait include workers in domestic service, construction, "
        "and hospitality sectors. Uzbekistan and Kuwait have bilateral relations, and "
        "Gulf states including Kuwait have become significant destinations for Uzbek "
        "labour migration. Uzbek documentation in the Latin-script Uzbek alphabet "
        "requires certified Arabic translation for Kuwaiti Ministry of Interior purposes. "
        "The Kuwaiti Embassy in Tashkent handles consular matters."
    ),
    ('ukraine', 'kuwait'): (
        "Ukrainian nationals in Kuwait include professionals in engineering, healthcare, "
        "and construction sectors, alongside a small community of displaced persons. "
        "Ukraine and Kuwait have bilateral diplomatic ties. Ukrainian documentation "
        "requires certified Arabic translation for Kuwaiti Ministry of Interior "
        "purposes. The Kuwaiti Embassy in Kyiv handles consular matters. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    # R44: South Africa wave 6
    ('ukraine', 'south-africa'): (
        "Ukrainian nationals in South Africa include business professionals, students, "
        "and a small number of displaced persons following the 2022 Russian invasion. "
        "Ukraine and South Africa have bilateral diplomatic ties, with trade in "
        "agricultural commodities and manufactured goods. Ukrainian documentation "
        "requires certified English translation for South African Home Affairs purposes. "
        "The South African Embassy in Kyiv handles consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('russia', 'south-africa'): (
        "Russian nationals in South Africa include business professionals, investors, "
        "and tourists. Russia and South Africa are fellow BRICS members and have "
        "bilateral trade ties in mining, energy, and agriculture. South Africa is a "
        "destination for Russian nationals seeking to invest or relocate, given BRICS "
        "cooperation and the country's business environment. Russian documentation "
        "requires certified English translation for South African Home Affairs purposes. "
        "The South African Embassy in Moscow handles consular matters."
    ),
    ('indonesia', 'south-africa'): (
        "Indonesian nationals in South Africa include students, business professionals, "
        "and travellers. Indonesia and South Africa have bilateral trade ties and "
        "diplomatic relations, cooperating across agriculture, mining, and manufacturing. "
        "Both countries are G20 members and share development interests across the "
        "Global South. Indonesian documentation requires certified English translation "
        "for South African Home Affairs purposes. The South African Embassy in Jakarta "
        "handles consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('bangladesh', 'south-africa'): (
        "Bangladeshi nationals in South Africa include traders in the textile and "
        "garment sector, as well as small business owners and workers. Bangladesh and "
        "South Africa have bilateral trade ties, with Bangladeshi textile exports "
        "reaching the South African market. Bengali documentation from Bangladesh "
        "requires certified English translation for South African Home Affairs "
        "purposes. The South African High Commission in Dhaka handles consular matters."
    ),
    ('egypt', 'south-africa'): (
        "Egyptian nationals in South Africa include business professionals in trade, "
        "tourism, and the financial sector, alongside students. Egypt and South Africa "
        "are both African Union members and major continental economies with strong "
        "bilateral ties. The two countries cooperate on African development and have "
        "an active trade relationship. Arabic documentation from Egypt requires "
        "certified English translation for South African Home Affairs purposes. The "
        "South African Embassy in Cairo handles consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    # R44: USA wave 6
    ('jordan', 'united-states'): (
        "Jordanian nationals form a notable diaspora community in the United States, "
        "concentrated in Detroit, Washington DC, and New York. Jordan and the United "
        "States have a Free Trade Agreement and close security and diplomatic ties, "
        "with Jordan a key US partner in the Middle East. Jordanian students attend "
        "American universities in significant numbers, and the bilateral relationship "
        "supports considerable travel in both directions. Arabic documentation from "
        "Jordan requires certified English translation for US state-level civil "
        "registration purposes. The US Embassy in Amman handles consular matters. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('algeria', 'united-states'): (
        "Algerian nationals in the United States include professionals in the energy, "
        "academic, and technology sectors, alongside students. Algeria and the United "
        "States have diplomatic relations and bilateral energy trade, with the US a "
        "significant importer of Algerian liquefied natural gas. Arabic and French "
        "documentation from Algeria requires certified English translation for US "
        "state-level civil registration purposes. The US Embassy in Algiers handles "
        "consular matters."
    ),
    ('uzbekistan', 'united-states'): (
        "Uzbek nationals in the United States include students, professionals, and a "
        "growing diaspora community, particularly in New York and other major cities. "
        "Uzbekistan and the United States have diplomatic relations and cooperation on "
        "education and security. Uzbek documentation in the Latin-script Uzbek alphabet "
        "requires certified English translation for US state-level civil registration "
        "purposes. The US Embassy in Tashkent handles consular matters. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('nicaragua', 'united-states'): (
        "Nicaraguan nationals form one of the larger Central American diaspora "
        "communities in the United States, concentrated in Miami, Los Angeles, and "
        "the Washington DC area. The United States and Nicaragua have long-standing "
        "demographic ties, with Nicaraguans emigrating in large numbers since the "
        "1970s for economic and political reasons. Spanish documentation from Nicaragua "
        "requires certified English translation for US state-level civil registration "
        "purposes. The US Embassy in Managua handles consular matters."
    ),
    ('costa-rica', 'united-states'): (
        "Costa Rican nationals in the United States include professionals, students, "
        "and a small but established diaspora community. The United States and Costa "
        "Rica have close bilateral ties under the Dominican Republic-Central America "
        "Free Trade Agreement (CAFTA-DR), and significant numbers of US citizens "
        "also retire to Costa Rica, making this a corridor travelled in both directions. "
        "Spanish documentation from Costa Rica requires certified English translation "
        "for US state-level civil registration purposes. The US Embassy in San Jose "
        "handles consular matters. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    # R44: Germany wave 7
    ('thailand', 'germany'): (
        "Thai nationals in Germany include students, academics, and professionals, "
        "alongside a community of Thai partners and spouses of German nationals. "
        "Germany has a long history of Thai cultural and academic exchange, and Thai "
        "restaurants operate across Germany. German tourists visit Thailand in large "
        "numbers annually, creating a return repatriation corridor. Thai documentation "
        "requires certified German translation for German Standesamt (civil registry) "
        "purposes. The German Embassy in Bangkok handles consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    ('myanmar', 'germany'): (
        "Myanmar nationals in Germany include refugees and asylum seekers granted "
        "protection in Germany, alongside students and professionals. Germany has been "
        "a significant destination for Myanmar nationals following military rule and "
        "political instability. Burmese documentation requires certified German "
        "translation for Standesamt purposes. The German Embassy in Yangon handles "
        "consular matters, though families should confirm current consular access "
        "arrangements given the political situation in Myanmar."
    ),
    ('south-africa', 'germany'): (
        "South African nationals in Germany include academics, professionals in the "
        "automotive and engineering sectors, and students. Germany and South Africa "
        "have strong bilateral ties across trade and investment, with German companies "
        "including BMW and Volkswagen having major manufacturing operations in South "
        "Africa. South Africa is a significant export market for German goods. English "
        "and Afrikaans documentation from South Africa requires certified German "
        "translation for Standesamt purposes. The German Embassy in Pretoria handles "
        "consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    ('brazil', 'germany'): (
        "Brazilian nationals in Germany include professionals, students, and a "
        "significant community of German-Brazilian dual nationals, reflecting the "
        "historic German settlement in southern Brazil. Germany and Brazil have "
        "extensive bilateral trade, with Germany a major investor in Brazilian "
        "industry. Portuguese documentation from Brazil requires certified German "
        "translation for Standesamt (civil registry) purposes. The German Embassy "
        "in Brasilia handles consular matters."
    ),
    ('colombia', 'germany'): (
        "Colombian nationals in Germany include students, professionals, and asylum "
        "seekers, with Germany one of the larger European destinations for Colombian "
        "migration. Germany and Colombia have bilateral trade links and diplomatic "
        "relations. Spanish documentation from Colombia requires certified German "
        "translation for Standesamt purposes. The German Embassy in Bogota handles "
        "consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    # R44: France wave 6
    ('ethiopia', 'france'): (
        "Ethiopian nationals in France include students, diplomats, and professionals, "
        "with a notable community in Paris. France and Ethiopia have longstanding "
        "diplomatic ties, and France has been a significant development partner for "
        "Ethiopia. Many Ethiopian students pursue higher education in France, and "
        "cultural and academic exchanges are well-established. Amharic documentation "
        "from Ethiopia requires certified French translation for French civil registry "
        "purposes. The French Embassy in Addis Ababa handles consular matters. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    ('kenya', 'france'): (
        "Kenyan nationals in France include students, professionals, and a small "
        "diaspora community in Paris and other French cities. France and Kenya have "
        "bilateral diplomatic and trade ties, with France being a significant market "
        "for Kenyan exports including cut flowers, coffee, and tea. Kenya and France "
        "cooperate on development assistance and French language education. Swahili "
        "and English documentation from Kenya requires certified French translation "
        "for French civil registry purposes. The French Embassy in Nairobi handles "
        "consular matters."
    ),
    ('sri-lanka', 'france'): (
        "Sri Lankan nationals in France form a substantial diaspora community, primarily "
        "in the Paris region, with the Tamil Sri Lankan community among the largest in "
        "Europe. France granted asylum to significant numbers of Sri Lankan Tamils "
        "during and after the Sri Lankan civil war. The community is now well-established, "
        "with second and third generations born in France. Sinhala and Tamil documentation "
        "requires certified French translation for French civil registry purposes. The "
        "French Embassy in Colombo handles consular matters. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    ('nepal', 'france'): (
        "Nepali nationals in France include students, Gurkha veterans' family members, "
        "and professionals. France and Nepal have diplomatic relations and France "
        "provides development assistance to Nepal. French mountaineering expeditions "
        "to the Himalayas have historically created bilateral ties. Nepali documentation "
        "in the Devanagari script requires certified French translation for French "
        "civil registry purposes. The French Embassy in Kathmandu handles consular "
        "matters."
    ),
    ('myanmar', 'france'): (
        "Myanmar nationals in France include students, asylum seekers, and a small "
        "professional community. France has accepted Myanmar refugees following "
        "political instability and the 2021 military takeover. Burmese documentation "
        "requires certified French translation for French civil registry (mairie) "
        "purposes. The French Embassy in Yangon handles consular matters, though "
        "families should confirm current consular access arrangements. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    # R44: Oman wave 1 (new hub)
    ('india', 'oman'): (
        "Indian nationals form the largest expatriate community in Oman, with several "
        "hundred thousand Indian workers and professionals employed across construction, "
        "hospitality, healthcare, retail, and financial services. India and Oman have "
        "longstanding bilateral ties, and the Indian community in Oman is one of the "
        "oldest and most established in the Gulf. Many Indian families have lived in "
        "Oman for generations, with children born in the country. Hindi, Malayalam, "
        "Tamil, and other Indian language documentation requires certified Arabic "
        "translation for Royal Oman Police registration purposes. The Omani Embassy "
        "in New Delhi handles consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    ('pakistan', 'oman'): (
        "Pakistani nationals form one of the largest expatriate communities in Oman, "
        "employed across construction, retail, domestic service, and professional "
        "sectors. Pakistan and Oman have bilateral ties as OIC member states, and "
        "Pakistani workers have been part of Oman's labour force since the Sultanate's "
        "development boom of the 1970s. Urdu documentation from Pakistan requires "
        "certified Arabic translation for Royal Oman Police registration purposes. "
        "The Omani Embassy in Islamabad handles consular matters."
    ),
    ('bangladesh', 'oman'): (
        "Bangladeshi nationals in Oman form a large community employed in construction, "
        "domestic service, and manufacturing sectors under bilateral labour agreements. "
        "Bangladesh and Oman have a Memorandum of Understanding on labour migration, "
        "and the Gulf states including Oman are among the largest recipients of "
        "Bangladeshi migrant workers. Bengali documentation requires certified Arabic "
        "translation for Royal Oman Police registration purposes. The Omani Embassy "
        "in Dhaka handles consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    ('nepal', 'oman'): (
        "Nepali nationals in Oman include workers in construction, hospitality, and "
        "domestic service sectors, part of the significant Nepali labour migration to "
        "the Gulf. Nepal and Oman have bilateral labour agreements and remittances from "
        "Omani-based Nepali workers are a significant source of income for Nepali "
        "families. Nepali documentation in the Devanagari script requires certified "
        "Arabic translation for Royal Oman Police registration purposes. The Omani "
        "Embassy in Kathmandu handles consular matters."
    ),
    ('philippines', 'oman'): (
        "Filipino nationals in Oman include domestic workers, healthcare professionals, "
        "and construction workers, part of the large-scale Philippines Overseas "
        "Employment Administration (POEA) deployment to Gulf states. Oman is an "
        "approved destination country for Overseas Filipino Workers (OFWs), and the "
        "Philippine Overseas Labour Office (POLO) in Muscat provides welfare services "
        "to the community. In the event of a death, the Philippine Overseas Labour "
        "Office in Muscat should be notified alongside the relevant Omani authorities. "
        "Filipino documentation in English is generally understood by Omani authorities, "
        "though official authentication is required. The Omani Embassy in Manila handles "
        "consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    # R45: Turkey wave 4
    ('nigeria', 'turkey'): (
        "Nigerian nationals in Turkey include students, business professionals in the "
        "textile and trade sectors, and a growing diaspora community in Istanbul. "
        "Nigeria and Turkey have bilateral diplomatic ties and growing trade links, "
        "with Turkish construction and consumer goods companies active in Nigeria. "
        "English documentation from Nigeria is not automatically accepted by Turkish "
        "civil registry authorities and requires certified Turkish translation. The "
        "Turkish Embassy in Abuja handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('ghana', 'turkey'): (
        "Ghanaian nationals in Turkey include students, business professionals, and "
        "traders. Ghana and Turkey have bilateral diplomatic ties and growing trade "
        "links, with Turkish companies investing in Ghanaian infrastructure and "
        "manufacturing. English documentation from Ghana requires certified Turkish "
        "translation for Turkish civil registry (belediye) purposes. The Turkish "
        "Embassy in Accra handles consular matters."
    ),
    ('kenya', 'turkey'): (
        "Kenyan nationals in Turkey include students, business professionals, and "
        "travellers. Kenya and Turkey have bilateral trade ties and growing diplomatic "
        "relations, with Turkey investing in Kenyan infrastructure and logistics. "
        "English and Swahili documentation from Kenya requires certified Turkish "
        "translation for Turkish civil registry purposes. The Turkish Embassy in "
        "Nairobi handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('ethiopia', 'turkey'): (
        "Ethiopian nationals in Turkey include students, airline and logistics "
        "professionals, and business travellers. Ethiopia and Turkey have bilateral "
        "trade ties and diplomatic relations, with Turkish companies active in "
        "Ethiopian construction and manufacturing. Amharic documentation from Ethiopia "
        "requires certified Turkish translation for Turkish civil registry (belediye) "
        "purposes. The Turkish Embassy in Addis Ababa handles consular matters."
    ),
    ('bangladesh', 'turkey'): (
        "Bangladeshi nationals in Turkey include workers in the textile and garment "
        "sector, students, and business professionals. Turkey and Bangladesh share "
        "significant textile industry ties, with Turkish and Bangladeshi manufacturers "
        "operating in related supply chains. OIC membership links both countries "
        "diplomatically. Bengali documentation from Bangladesh requires certified "
        "Turkish translation for Turkish civil registry purposes. The Turkish Embassy "
        "in Dhaka handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    # R45: Malaysia wave 4
    ('nigeria', 'malaysia'): (
        "Nigerian nationals in Malaysia include students at Malaysian universities, "
        "business professionals, and traders. Malaysia is one of the most popular "
        "destinations for Nigerian students pursuing international education, given "
        "the relatively affordable costs and English-medium instruction. Nigeria and "
        "Malaysia are both Commonwealth members and OIC member states. English "
        "documentation from Nigeria is generally understood by Malaysian authorities, "
        "though authentication by the Malaysian High Commission is required. The "
        "Malaysian High Commission in Abuja handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('ghana', 'malaysia'): (
        "Ghanaian nationals in Malaysia include students and business professionals, "
        "with Malaysia a popular educational destination for Ghanaians seeking "
        "internationally recognised degrees. Ghana and Malaysia are both Commonwealth "
        "members with shared English-language education ties. English documentation "
        "from Ghana is generally understood by Malaysian authorities, though "
        "authentication by the Malaysian High Commission is required. The Malaysian "
        "High Commission in Accra handles consular matters."
    ),
    ('kenya', 'malaysia'): (
        "Kenyan nationals in Malaysia include students, professionals in aviation and "
        "logistics, and business travellers. Malaysia and Kenya have bilateral trade "
        "ties and both are Commonwealth members. Malaysia's education sector attracts "
        "Kenyan students, and Kenyan professionals work in Malaysian aviation and "
        "hospitality industries. English and Swahili documentation from Kenya requires "
        "authentication by the Malaysian High Commission. The Malaysian High Commission "
        "in Nairobi handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('ethiopia', 'malaysia'): (
        "Ethiopian nationals in Malaysia include aviation and logistics professionals, "
        "given Ethiopian Airlines' expansion into Southeast Asian routes, alongside "
        "students and business travellers. Malaysia and Ethiopia have bilateral trade "
        "ties and diplomatic relations. Amharic documentation from Ethiopia requires "
        "certified Malay or English translation for Malaysian National Registration "
        "Department (NRD) purposes. The Malaysian Embassy in Addis Ababa handles "
        "consular matters."
    ),
    ('saudi-arabia', 'malaysia'): (
        "Saudi Arabian nationals in Malaysia include students at Malaysian universities "
        "and Islamic educational institutions, tourists, and business professionals "
        "drawn by Malaysia's position as a global centre for Islamic finance and "
        "halal food. Saudi Arabia and Malaysia are both OIC member states with strong "
        "bilateral ties in education and Islamic finance. Arabic documentation from "
        "Saudi Arabia requires certified Malay or English translation for Malaysian "
        "NRD purposes. The Malaysian Embassy in Riyadh handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    # R45: Oman wave 2
    ('ethiopia', 'oman'): (
        "Ethiopian nationals in Oman form a significant community in the domestic "
        "service sector, with Ethiopian women among the largest groups of domestic "
        "workers in the Gulf. Ethiopia and Oman have bilateral diplomatic relations "
        "and labour agreements governing worker migration. In death-in-service cases, "
        "the employer's assistance is required alongside consular support. Amharic "
        "documentation from Ethiopia requires certified Arabic translation for Royal "
        "Oman Police registration purposes. The Omani Embassy in Addis Ababa handles "
        "consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    ('kenya', 'oman'): (
        "Kenyan nationals in Oman include domestic workers, healthcare professionals, "
        "and hospitality staff. Kenya and Oman have bilateral ties and Kenyan workers "
        "are part of the broader East African labour migration to the Gulf. English "
        "and Swahili documentation from Kenya requires certified Arabic translation "
        "for Royal Oman Police registration purposes. The Omani Embassy in Nairobi "
        "handles consular matters."
    ),
    ('sri-lanka', 'oman'): (
        "Sri Lankan nationals in Oman form one of the oldest expatriate communities "
        "in the Gulf, with Sri Lankan workers employed in domestic service, "
        "construction, and hospitality sectors for decades. Sri Lanka and Oman have "
        "longstanding bilateral labour ties and Sri Lankan workers have been integral "
        "to Oman's service sector since the 1970s. Sinhala and Tamil documentation "
        "requires certified Arabic translation for Royal Oman Police registration "
        "purposes. The Omani Embassy in Colombo handles consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    ('indonesia', 'oman'): (
        "Indonesian nationals in Oman include domestic workers, construction workers, "
        "and hospitality staff. Indonesia and Oman are OIC member states with shared "
        "Islamic heritage and bilateral labour migration agreements. Indonesian domestic "
        "workers form a significant part of Oman's household sector workforce. Indonesian "
        "documentation in Bahasa Indonesia requires certified Arabic translation for "
        "Royal Oman Police registration purposes. The Omani Embassy in Jakarta handles "
        "consular matters."
    ),
    ('egypt', 'oman'): (
        "Egyptian nationals form a large professional and skilled-worker community in "
        "Oman, employed in education, healthcare, engineering, and government sectors. "
        "Egypt and Oman have longstanding bilateral ties as fellow Arab League members, "
        "and Egyptian professionals have been part of Oman's development since the "
        "1970s. Arabic documentation from Egypt is generally understood by Omani "
        "authorities, though official authentication by the Omani Embassy is required. "
        "The Omani Embassy in Cairo handles consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    # R45: Switzerland wave 5
    ('nigeria', 'switzerland'): (
        "Nigerian nationals in Switzerland include students, academics, business "
        "professionals, and a small but established diaspora community in Geneva and "
        "Zurich. Switzerland hosts several international organisations in Geneva, "
        "drawing Nigerian diplomats and NGO workers. Nigeria and Switzerland have "
        "bilateral ties across trade and development cooperation. English documentation "
        "from Nigeria is not automatically accepted by Swiss Zivilstandsamt (civil "
        "registry) authorities and requires certified German, French, or Italian "
        "translation. The Swiss Embassy in Abuja handles consular matters. "
        "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
    ),
    ('iran', 'switzerland'): (
        "Iranian nationals form a notable diaspora community in Switzerland, "
        "concentrated in Zurich and Geneva, with a substantial presence since the "
        "1979 Iranian Revolution. Switzerland has represented US interests in Iran "
        "since 1980, giving Swiss embassies a unique diplomatic role in the "
        "Iran-US relationship. Farsi documentation from Iran requires certified "
        "translation into German, French, or Italian for Swiss Zivilstandsamt "
        "purposes. The Swiss Embassy in Tehran handles consular matters."
    ),
    ('bangladesh', 'switzerland'): (
        "Bangladeshi nationals in Switzerland include students, professionals at "
        "international organisations in Geneva, and a small diaspora community. "
        "Switzerland hosts key international bodies including the World Health "
        "Organisation and International Labour Organisation, drawing Bangladeshi "
        "officials and professionals. Bengali documentation requires certified "
        "German, French, or Italian translation for Swiss civil registry purposes. "
        "The Swiss Embassy in Dhaka handles consular matters. "
        "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
    ),
    ('indonesia', 'switzerland'): (
        "Indonesian nationals in Switzerland include students, diplomats, and "
        "professionals at international organisations in Geneva. Indonesia and "
        "Switzerland have bilateral trade ties and diplomatic relations. Indonesian "
        "documentation in Bahasa Indonesia requires certified German, French, or "
        "Italian translation for Swiss Zivilstandsamt (civil registry) purposes. "
        "The Swiss Embassy in Jakarta handles consular matters."
    ),
    ('vietnam', 'switzerland'): (
        "Vietnamese nationals in Switzerland include students, professionals at "
        "international organisations, and a small diaspora community. Vietnam and "
        "Switzerland have bilateral trade and diplomatic ties, with Switzerland an "
        "important European partner for Vietnamese exports. Vietnamese documentation "
        "requires certified German, French, or Italian translation for Swiss "
        "Zivilstandsamt purposes. The Swiss Embassy in Hanoi handles consular "
        "matters. "
        "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
    ),
    # R45: Sweden wave 5
    ('ghana', 'sweden'): (
        "Ghanaian nationals form one of the larger sub-Saharan African communities "
        "in Sweden, with an established diaspora concentrated in Stockholm, "
        "Gothenburg, and Malmo. Ghana and Sweden have bilateral ties through "
        "development cooperation, with Sweden a significant donor to Ghanaian "
        "education and governance programmes. English documentation from Ghana "
        "requires certified Swedish translation for Skatteverket (Swedish Tax "
        "Agency) population register purposes. The Swedish Embassy in Accra handles "
        "consular matters. "
        "(Swedish Ministry of Foreign Affairs, UD, 2025.)"
    ),
    ('senegal', 'sweden'): (
        "Senegalese nationals in Sweden form a small but established diaspora "
        "community, with Senegalese residents concentrated in Stockholm and other "
        "major cities. Senegal and Sweden have bilateral development cooperation ties, "
        "with Sweden supporting Senegalese health and education programmes. French "
        "and Wolof documentation from Senegal requires certified Swedish translation "
        "for Swedish population register purposes. The Swedish Embassy in Dakar "
        "handles consular matters."
    ),
    ('pakistan', 'sweden'): (
        "Pakistani nationals form one of the larger South Asian communities in Sweden, "
        "with a significant diaspora established over several decades in Stockholm, "
        "Gothenburg, and Malmo. Sweden has been a destination for Pakistani labour "
        "migration and family reunion. Urdu documentation from Pakistan requires "
        "certified Swedish translation for Skatteverket (Swedish Tax Agency) "
        "population register purposes. The Swedish Embassy in Islamabad handles "
        "consular matters. "
        "(Swedish Ministry of Foreign Affairs, UD, 2025.)"
    ),
    ('ukraine', 'sweden'): (
        "Ukrainian nationals in Sweden include a substantial number of people who "
        "fled to Sweden following the 2022 Russian invasion, alongside an existing "
        "diaspora community of professionals and students. Sweden offered temporary "
        "protection to Ukrainian displaced persons under the EU Temporary Protection "
        "Directive. Ukrainian documentation requires certified Swedish translation "
        "for Skatteverket population register and local authority purposes. The "
        "Swedish Embassy in Kyiv handles consular matters."
    ),
    ('indonesia', 'sweden'): (
        "Indonesian nationals in Sweden include students, professionals, and a "
        "small diaspora community. Sweden and Indonesia have bilateral diplomatic "
        "and trade ties, with Swedish companies including Volvo and IKEA having "
        "operations in Indonesia. Indonesian documentation in Bahasa Indonesia "
        "requires certified Swedish translation for Swedish population register "
        "purposes. The Swedish Embassy in Jakarta handles consular matters. "
        "(Swedish Ministry of Foreign Affairs, UD, 2025.)"
    ),
    # R46: Norway wave 5
    ('ghana', 'norway'): (
        "Ghanaian nationals in Norway form an established diaspora community, "
        "with Ghanaian residents concentrated in Oslo and other Norwegian cities. "
        "Ghana and Norway have bilateral development cooperation ties, with Norway "
        "a major donor to Ghanaian oil sector governance and environmental "
        "programmes. English documentation from Ghana requires certified Norwegian "
        "translation for Folkeregisteret (National Population Register) purposes. "
        "The Norwegian Embassy in Accra handles consular matters. "
        "(Norwegian Ministry of Foreign Affairs, 2025.)"
    ),
    ('senegal', 'norway'): (
        "Senegalese nationals in Norway include a small but established diaspora "
        "community in Oslo and other Norwegian cities. Norway and Senegal have "
        "bilateral development cooperation ties, with Norway supporting Senegalese "
        "fisheries and maritime sectors. French and Wolof documentation from Senegal "
        "requires certified Norwegian translation for the Folkeregisteret (National "
        "Population Register) purposes. The Norwegian Embassy in Dakar handles "
        "consular matters."
    ),
    ('indonesia', 'norway'): (
        "Indonesian nationals in Norway include professionals in the maritime and "
        "energy sectors, alongside students and a small diaspora community. Norway "
        "and Indonesia have bilateral trade ties, with the Norwegian energy sector "
        "active in Indonesia and Indonesian seafarers employed on Norwegian vessels. "
        "Indonesian documentation requires certified Norwegian translation for "
        "Folkeregisteret purposes. The Norwegian Embassy in Jakarta handles "
        "consular matters. "
        "(Norwegian Ministry of Foreign Affairs, 2025.)"
    ),
    ('egypt', 'norway'): (
        "Egyptian nationals in Norway include professionals, students, and a "
        "small diaspora community. Norway and Egypt have bilateral trade ties, "
        "with the Norwegian energy sector having historical connections to Egypt's "
        "oil and gas industry. Arabic documentation from Egypt requires certified "
        "Norwegian translation for the Folkeregisteret (National Population Register) "
        "purposes. The Norwegian Embassy in Cairo handles consular matters."
    ),
    ('algeria', 'norway'): (
        "Algerian nationals in Norway form a small but established diaspora community, "
        "with Algerian residents concentrated in Oslo. Norway and Algeria have "
        "bilateral trade ties, with both countries being significant oil and gas "
        "producers in their respective regions. Arabic and French documentation from "
        "Algeria requires certified Norwegian translation for the Folkeregisteret "
        "(National Population Register) purposes. The Norwegian Embassy in Algiers "
        "handles consular matters. "
        "(Norwegian Ministry of Foreign Affairs, 2025.)"
    ),
    # R46: Oman wave 3
    ('turkey', 'oman'): (
        "Turkish nationals in Oman include business professionals in the construction, "
        "hospitality, and trade sectors. Turkey and Oman have bilateral trade ties and "
        "both are OIC member states with diplomatic relations. Turkish construction "
        "companies have been active in Omani development projects. Turkish documentation "
        "requires certified Arabic translation for Royal Oman Police registration "
        "purposes. The Omani Embassy in Ankara handles consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    ('iraq', 'oman'): (
        "Iraqi nationals in Oman include professionals in trade, construction, and "
        "the energy sector, alongside business travellers. Iraq and Oman are neighbouring "
        "Gulf Arab states with bilateral diplomatic ties as fellow Arab League members. "
        "Oman has played a diplomatic role in Iraqi regional affairs. Arabic "
        "documentation from Iraq is generally understood by Omani authorities, though "
        "official authentication by the Omani Embassy is required. The Omani Embassy "
        "in Baghdad handles consular matters."
    ),
    ('iran', 'oman'): (
        "Iranian nationals in Oman include business professionals in the trading "
        "and maritime sectors, reflecting the longstanding commercial ties across "
        "the Strait of Hormuz. Iran and Oman share a strategic maritime corridor "
        "and have maintained diplomatic relations even during periods of regional "
        "tension, with Oman having played a neutral diplomatic role in Iran-related "
        "negotiations. Farsi documentation from Iran requires certified Arabic "
        "translation for Royal Oman Police registration purposes. The Omani Embassy "
        "in Tehran handles consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    ('jordan', 'oman'): (
        "Jordanian nationals in Oman include professionals in healthcare, education, "
        "and engineering, as Jordan has historically provided skilled workers across "
        "the Gulf. Jordan and Oman are fellow Arab League members with close bilateral "
        "ties. Jordanian professionals, particularly doctors, nurses, and engineers, "
        "have been part of Oman's skilled workforce for decades. Arabic documentation "
        "from Jordan is generally understood by Omani authorities, though official "
        "authentication is required. The Omani Embassy in Amman handles consular "
        "matters."
    ),
    ('morocco', 'oman'): (
        "Moroccan nationals in Oman include professionals in education, hospitality, "
        "and service sectors. Morocco and Oman are fellow Arab League and OIC member "
        "states with diplomatic ties. Moroccan professionals in hospitality and "
        "education have worked in Oman as part of the wider Arab labour mobility "
        "network. Arabic documentation from Morocco is generally understood by Omani "
        "authorities, though official authentication by the Omani Embassy is required. "
        "The Omani Embassy in Rabat handles consular matters. "
        "(Oman Ministry of Foreign Affairs, 2025.)"
    ),
    # R46: South Africa wave 7
    ('malaysia', 'south-africa'): (
        "Malaysian nationals in South Africa include business professionals, tourists, "
        "and students. Malaysia and South Africa have bilateral trade ties and both "
        "are G77 developing economy members. Malaysian investment in South African "
        "retail and property has grown, and bilateral trade spans palm oil, rubber, "
        "and manufactured goods. Malay and English documentation from Malaysia "
        "requires certified English translation for South African Home Affairs "
        "purposes. The South African High Commission in Kuala Lumpur handles "
        "consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('vietnam', 'south-africa'): (
        "Vietnamese nationals in South Africa include traders, business professionals, "
        "and a small diaspora community. Vietnam and South Africa have bilateral "
        "trade ties, with trade in electronics, textiles, and agricultural goods. "
        "Both countries are members of the Non-Aligned Movement and have diplomatic "
        "relations. Vietnamese documentation requires certified English translation "
        "for South African Home Affairs purposes. The South African Embassy in Hanoi "
        "handles consular matters."
    ),
    ('philippines', 'south-africa'): (
        "Filipino nationals in South Africa include healthcare professionals, domestic "
        "workers, and a small diaspora community in Johannesburg and Cape Town. "
        "The Philippines and South Africa have bilateral diplomatic relations, with "
        "Filipino nurses and medical professionals forming part of South Africa's "
        "healthcare workforce. The Philippine Overseas Labour Office (POLO) provides "
        "welfare services to Overseas Filipino Workers (OFWs) in South Africa. "
        "English documentation from the Philippines is generally understood by "
        "South African authorities. The South African Embassy in Manila handles "
        "consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('nepal', 'south-africa'): (
        "Nepali nationals in South Africa include a small community of professionals "
        "and students. Nepal and South Africa have diplomatic relations. Nepali "
        "documentation in the Devanagari script requires certified English translation "
        "for South African Home Affairs purposes. The South African High Commission "
        "in New Delhi covers Nepal for consular matters; families should confirm "
        "current consular arrangements."
    ),
    ('myanmar', 'south-africa'): (
        "Myanmar nationals in South Africa include a small number of business "
        "professionals and students. Myanmar and South Africa have diplomatic "
        "relations. Burmese documentation requires certified English translation "
        "for South African Home Affairs purposes. The South African Embassy covers "
        "Myanmar from Bangkok; families should confirm current consular access "
        "arrangements. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    # R46: Portugal wave 5
    ('ghana', 'portugal'): (
        "Ghanaian nationals form one of the larger African communities in Portugal, "
        "with a well-established diaspora concentrated in Lisbon and Porto. Ghana "
        "and Portugal have historical and linguistic connections through Portugal's "
        "presence on the West African coast and longstanding trade ties. Many "
        "Ghanaian nationals have settled in Portugal for work and family reasons. "
        "English documentation from Ghana requires certified Portuguese translation "
        "for Conservatoria do Registo Civil purposes. The Portuguese Embassy in "
        "Accra handles consular matters. "
        "(Portuguese Ministry of Foreign Affairs, MNE, 2025.)"
    ),
    ('ethiopia', 'portugal'): (
        "Ethiopian nationals in Portugal include students, professionals, and a "
        "small diaspora community. Portugal and Ethiopia have diplomatic ties and "
        "Portugal has provided development cooperation support to Ethiopia. Ethiopian "
        "nationals in Portugal include those working in agriculture and domestic "
        "service sectors. Amharic documentation from Ethiopia requires certified "
        "Portuguese translation for Conservatoria do Registo Civil purposes. The "
        "Portuguese Embassy in Addis Ababa handles consular matters."
    ),
    ('iraq', 'portugal'): (
        "Iraqi nationals in Portugal include students, asylum seekers, and a small "
        "but growing community. Portugal has accepted Iraqi refugees and asylum "
        "seekers, and the country's relatively accessible integration pathways "
        "have made it a destination for Iraqi nationals seeking European residency. "
        "Arabic documentation from Iraq requires certified Portuguese translation "
        "for Conservatoria do Registo Civil purposes. The Portuguese Embassy in "
        "Baghdad handles consular matters. "
        "(Portuguese Ministry of Foreign Affairs, MNE, 2025.)"
    ),
    ('egypt', 'portugal'): (
        "Egyptian nationals in Portugal include students, business professionals, "
        "and a small diaspora community. Egypt and Portugal have diplomatic ties "
        "as Mediterranean neighbours with historical connections through trade "
        "routes. Arabic documentation from Egypt requires certified Portuguese "
        "translation for Conservatoria do Registo Civil purposes. The Portuguese "
        "Embassy in Cairo handles consular matters."
    ),
    ('algeria', 'portugal'): (
        "Algerian nationals in Portugal include professionals, students, and migrants "
        "who have settled in Portugal as an entry point to the EU. Algeria and "
        "Portugal have diplomatic ties and trade links. French and Arabic documentation "
        "from Algeria requires certified Portuguese translation for Conservatoria do "
        "Registo Civil purposes. The Portuguese Embassy in Algiers handles consular "
        "matters. "
        "(Portuguese Ministry of Foreign Affairs, MNE, 2025.)"
    ),
    # R46: Japan wave 5
    ('south-africa', 'japan'): (
        "South African nationals in Japan include business professionals in the "
        "automotive and mining industries, academics, and a small diaspora community. "
        "South Africa and Japan have bilateral trade ties, with Japan a significant "
        "importer of South African platinum, coal, and agricultural products. Both "
        "countries are G20 members with close economic cooperation. English "
        "and Afrikaans documentation from South Africa requires certified Japanese "
        "translation for Japanese municipal office (koseki) registration purposes. "
        "The Japanese Embassy in Pretoria handles consular matters. "
        "(Japanese Ministry of Foreign Affairs, 2025.)"
    ),
    ('nigeria', 'japan'): (
        "Nigerian nationals in Japan form a small but established diaspora community, "
        "concentrated in Tokyo's Ikebukuro district and other major cities. Nigeria "
        "and Japan have bilateral diplomatic ties and trade links in oil, manufactured "
        "goods, and electronics. English documentation from Nigeria requires certified "
        "Japanese translation for Japanese municipal office (koseki) registration "
        "purposes. The Japanese Embassy in Abuja handles consular matters."
    ),
    ('ghana', 'japan'): (
        "Ghanaian nationals in Japan include students, professionals, and a small "
        "diaspora community. Ghana and Japan have bilateral development cooperation "
        "ties, with Japan providing official development assistance (ODA) to Ghana "
        "across infrastructure and education. English documentation from Ghana "
        "requires certified Japanese translation for municipal office (koseki) "
        "registration purposes. The Japanese Embassy in Accra handles consular "
        "matters. "
        "(Japanese Ministry of Foreign Affairs, 2025.)"
    ),
    ('ethiopia', 'japan'): (
        "Ethiopian nationals in Japan include students, academics, and professionals "
        "in the aviation and logistics sectors, alongside diplomatic staff. Japan "
        "and Ethiopia have bilateral development cooperation ties and Japan has "
        "been a significant ODA donor to Ethiopia. Amharic documentation from "
        "Ethiopia requires certified Japanese translation for Japanese municipal "
        "office (koseki) registration purposes. The Japanese Embassy in Addis "
        "Ababa handles consular matters."
    ),
    ('kenya', 'japan'): (
        "Kenyan nationals in Japan include students, academics, and athletes, with "
        "Kenya having a notable presence in Japanese athletics through marathons and "
        "distance running events. Japan and Kenya have bilateral development "
        "cooperation ties and Japan provides ODA to Kenyan infrastructure and "
        "education projects. English and Swahili documentation from Kenya requires "
        "certified Japanese translation for municipal office (koseki) registration "
        "purposes. The Japanese Embassy in Nairobi handles consular matters. "
        "(Japanese Ministry of Foreign Affairs, 2025.)"
    ),
}


# ---------------------------------------------------------------------------
# Utility: read UK source file
# ---------------------------------------------------------------------------

def read_uk_file(origin_slug):
    path = os.path.join(ROUTES_DIR, f'{origin_slug}-to-united-kingdom.md')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_fm(content):
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    return m.group(1) if m else ''


def get_field(fm, field):
    m = re.search(rf'^{re.escape(field)}:\s*"?([^"\n]+)"?', fm, re.MULTILINE)
    return m.group(1).strip() if m else ''


def extract_block(fm, start_key, stop_keys):
    lines = fm.split('\n')
    start = None
    for i, line in enumerate(lines):
        if re.match(rf'^{re.escape(start_key)}\s*:', line):
            start = i
            break
    if start is None:
        return ''
    end = len(lines)
    for i in range(start + 1, len(lines)):
        stripped = lines[i]
        if not stripped.startswith(' ') and not stripped.startswith('\t') and stripped.strip():
            for sk in stop_keys:
                if re.match(rf'^{re.escape(sk)}\s*:', stripped):
                    end = i
                    break
            if end < len(lines):
                break
    return '\n'.join(lines[start:end])


# ---------------------------------------------------------------------------
# Generate a single route page
# ---------------------------------------------------------------------------

def make_route(origin_slug, dest_slug, variant):
    dest = DEST_META[dest_slug]
    dest_name = dest['name']
    dest_slug_str = dest['slug']
    dest_key = dest['key']

    uk_content = read_uk_file(origin_slug)
    if not uk_content:
        print(f"  ERROR: No UK route file for {origin_slug}")
        return None

    uk_fm = get_fm(uk_content)

    origin_name = get_field(uk_fm, 'origin_name')
    if not origin_name:
        origin_name = origin_slug.replace('-', ' ').title()

    timeline_avg = get_field(uk_fm, 'timeline_avg')
    timeline_fast = get_field(uk_fm, 'timeline_fast')
    timeline_complex = get_field(uk_fm, 'timeline_complex')
    complexity = get_field(uk_fm, 'route_complexity')
    doc_time = get_field(uk_fm, 'doc_processing_time')

    dest_embassy_city = EMBASSY_CITIES.get(
        (origin_slug, dest_slug), 'the capital'
    )

    intro = CORRIDOR_INTRO.get(
        (origin_slug, dest_slug),
        (
            f"Repatriation from {origin_name} to {dest_name} occurs when a "
            f"{dest_name}-based family has a loved one die in {origin_name} and needs "
            f"remains returned. This corridor follows {origin_name}'s standard export "
            f"procedures for international repatriation of human remains."
        )
    )

    title = f"{origin_name} to {dest_name}: Repatriation Guidance"
    if len(title) > 60:
        title = f"{origin_name} to {dest_name} Repatriation Guide"
    if len(title) > 60:
        abbrevs = {
            'Democratic Republic of the Congo': 'DR Congo',
            'Central African Republic': 'Central Africa',
            'Papua New Guinea': 'Papua New Guinea',
            'United Arab Emirates': 'UAE',
            'United States': 'United States',
            'New Zealand': 'New Zealand',
            'Saudi Arabia': 'Saudi Arabia',
            'Bosnia and Herzegovina': 'Bosnia',
            'North Macedonia': 'N. Macedonia',
            'South Africa': 'South Africa',
        }
        short_dest = abbrevs.get(dest_name, dest_name)
        short_origin = abbrevs.get(origin_name, origin_name)
        title = f"{short_origin} to {short_dest} Repatriation Guide"

    description_notes = {
        'low':           'Established process.',
        'moderate':      'Specialist support recommended.',
        'moderate-high': 'A specialist is essential.',
        'high':          'Specialist help required.',
        'very-high':     'A specialist is essential on this complex route.',
    }
    desc_note = description_notes.get(complexity, 'Specialist support recommended.')
    description = (
        f"Someone has died in {origin_name}. Repatriation to {dest_name} takes "
        f"{timeline_avg}. {desc_note} Contact us 24/7."
    )
    if len(description) > 155:
        description = description[:152] + '...'

    direct_answer_heading = (
        f'direct_answer_heading: "Repatriation from {origin_name} to {dest_name}: '
        f'what to expect"'
    )
    direct_answer_intro = f'direct_answer_intro: "{intro}"'

    dap_raw = extract_block(
        uk_fm, 'direct_answer_points',
        ['overview_heading', 'dest_reception', 'date']
    )
    dap = dap_raw
    dap = re.sub(
        r'British Embassy[^"]*advises?\.[^"]*Cannot fund repatriation\.',
        '',
        dap
    )
    dap = re.sub(
        r'British High Commission[^"]*advises?\.[^"]*Cannot fund repatriation\.',
        '',
        dap
    )
    dap = re.sub(
        r'FCDO[^"]*emergency line[^"]*\.',
        (f'{dest_name} Embassy in {dest_embassy_city} can advise. '
         f'They cannot fund repatriation.'),
        dap
    )
    dap = dap.replace('for UK acceptance', f'for {dest_name} acceptance')
    dap = dap.replace('UK funeral director', f'{dest_name} funeral director')
    dap = dap.replace('United Kingdom acceptance', f'{dest_name} acceptance')
    if 'Embassy' not in dap or dest_name not in dap:
        dap = dap.rstrip()
        dap += (
            f'\n  - "{dest_name} Embassy in {dest_embassy_city} can advise '
            f'on documentation. They cannot fund repatriation."'
        )

    overview_heading_raw = extract_block(uk_fm, 'overview_heading', ['overview_body'])
    overview_body_raw = extract_block(
        uk_fm, 'overview_body', ['dest_reception', 'dest_consular']
    )
    overview_heading = overview_heading_raw
    overview_body = overview_body_raw
    overview_body = re.sub(r'British Embassy[^.]+\.', '', overview_body)
    overview_body = re.sub(r'FCDO[^.]+\.', '', overview_body)

    dest_reception_text = dest['reception']
    consular_template = dest['consular_template']
    dest_consular_text = consular_template.format(
        city=dest_embassy_city,
        country_name=origin_name,
    )

    ts_raw = extract_block(uk_fm, 'timeline_steps', ['faqs', 'links'])
    ts = ts_raw
    ts = re.sub(
        r'(step: 3\s*\n\s*action: "[^"]*British Embassy[^"]*notified[^"]*")',
        (f'step: 3\n    action: "{dest_name} Embassy in {dest_embassy_city} notified"'),
        ts
    )
    ts = re.sub(
        r'(British Embassy \S+ notified\.)',
        f'{dest_name} Embassy {dest_embassy_city} notified.',
        ts
    )
    ts = re.sub(
        r'British Embassy[^"]+notified[^"]*',
        f'{dest_name} Embassy {dest_embassy_city} notified',
        ts
    )
    ts = re.sub(
        r'(action: "Air cargo[^"]*) to UK[^"]*"',
        rf'\1 to {dest_name}"',
        ts
    )
    ts = re.sub(
        r'(action: "Air cargo[^"]*) to United Kingdom[^"]*"',
        rf'\1 to {dest_name}"',
        ts
    )
    ts = ts.replace(
        'cargo terminal at destination', f'{dest_name} cargo terminal'
    )
    ts = re.sub(
        r'FCDO 24hr: \+44 \(0\)20 7008 5000\.',
        f'Call +44 (0)20 7008 5000 (FCDO) or {dest["emergency_line"]}.',
        ts
    )
    ts = ts.replace(
        'UK funeral director takes custody',
        f'{dest_name} funeral director takes custody'
    )
    ts = ts.replace(
        'United Kingdom funeral director takes custody',
        f'{dest_name} funeral director takes custody'
    )
    ts = ts.replace(
        'Coroner notified',
        'receiving funeral director coordinates with local authorities'
    )
    ts = re.sub(
        r'FCDO 24hr:[^\n"]+',
        f'{dest["emergency_line"]}',
        ts
    )

    faqs_raw = extract_block(uk_fm, 'faqs', ['links'])
    faqs = faqs_raw

    faqs = re.sub(
        r'(question: "How long does repatriation from [^"]*) to '
        r'(?:the )?United Kingdom take\?"',
        rf'\1 to {dest_name} take?"',
        faqs
    )
    faqs = re.sub(
        r'(question: "How long does repatriation from [^"]*) to '
        r'(?:the )?UK take\?"',
        rf'\1 to {dest_name} take?"',
        faqs
    )
    faqs = faqs.replace(
        'repatriation from ' + origin_name + ' to the UK takes',
        f'repatriation from {origin_name} to {dest_name} takes'
    )
    faqs = faqs.replace(
        'repatriation from ' + origin_name + ' to United Kingdom takes',
        f'repatriation from {origin_name} to {dest_name} takes'
    )
    faqs = faqs.replace(
        'repatriation from ' + origin_name + ' to the United Kingdom takes',
        f'repatriation from {origin_name} to {dest_name} takes'
    )

    new_embassy_q = (
        f'Does the {dest_name} Embassy in {origin_name} help with repatriation?'
    )
    new_embassy_a = (
        f'The {dest_name} Embassy in {dest_embassy_city} can assist with document '
        f'authentication and advise on repatriation requirements. They cannot pay for '
        f'or arrange repatriation. Contact the {dest_name} Embassy in {dest_embassy_city} '
        f'as soon as possible after the death.'
    )
    new_embassy_faq = (
        f'  - question: "{new_embassy_q}"\n    answer: "{new_embassy_a}"'
    )

    faqs = re.sub(
        r'  - question: "Does the (?:British|Irish) '
        r'(?:Embassy|High Commission) in [^"]*(?:help with repatriation|assist)[^"]*"\?"\n'
        r'    answer: "[^"]*"',
        new_embassy_faq,
        faqs
    )
    faqs = re.sub(
        r'  - question: "Is there an? (?:British|Irish) '
        r'(?:Embassy|High Commission) in [^"]*\?"\n    answer: "[^"]*"',
        new_embassy_faq,
        faqs
    )

    embassy_faq_q1 = f'Does the British Embassy in {origin_name} help with repatriation?'
    embassy_faq_q2 = f'Is there a British Embassy in {origin_name}?'
    embassy_faq_q3 = (
        f'Does the British High Commission in {origin_name} help with repatriation?'
    )
    for q in [embassy_faq_q1, embassy_faq_q2, embassy_faq_q3]:
        if q in faqs:
            pattern = rf'  - question: "{re.escape(q)}"\n    answer: "[^"]*"'
            faqs = re.sub(pattern, new_embassy_faq, faqs)

    faqs = re.sub(
        r'  - question: "What happens when the body arrives in '
        r'(?:the )?(?:United Kingdom|UK)\?"\n    answer: "[^"]*"',
        (f'  - question: "What happens when the body arrives in {dest_name}?"\n'
         f'    answer: "{dest["arrival_faq"]}"'),
        faqs
    )

    faqs = faqs.replace('UK funeral director', f'{dest_name} funeral director')
    faqs = faqs.replace(
        'United Kingdom funeral director', f'{dest_name} funeral director'
    )
    faqs = faqs.replace(
        'FCDO 24-hour emergency line: +44 (0)20 7008 5000',
        dest_consular_text[:80]
    )
    faqs = faqs.replace('FCDO emergency line', dest['emergency_line'])
    faqs = faqs.replace('UK coroner', f'{dest_name} receiving authority')
    faqs = faqs.replace(
        'the coroner for the district', f'the receiving authority in {dest_name}'
    )
    faqs = faqs.replace(
        'the Coroner for the district', f'the receiving authority in {dest_name}'
    )

    links = f"""links:
  upward:
    - url: "/repatriation-from-{origin_slug}/"
      text: "Full {origin_name} repatriation guide"
    - url: "/guides/death-abroad-{origin_slug}/"
      text: "What to do if someone dies in {origin_name}"
    - url: "/{dest['hub_url']}/"
      text: "Repatriation to {dest_name}: overview"
    - url: "/contact/"
      text: "Send an enquiry to our team"
  sideways:
    - url: "/routes/{origin_slug}-to-united-kingdom/"
      text: "Repatriation from {origin_name} to the UK"
    - url: "/routes/{origin_slug}-to-ireland/"
      text: "Repatriation from {origin_name} to Ireland\""""

    content = f"""---
title: "{title}"
description: "{description}"
origin_key: "{origin_slug}"
dest_key: "{dest_key}"
origin_name: "{origin_name}"
dest_name: "{dest_name}"
origin_slug: "{origin_slug}"
dest_slug: "{dest_slug_str}"
slug: "{origin_slug}-to-{dest_slug_str}"
template_variant: "{variant}"
route_complexity: "{complexity}"
timeline_avg: "{timeline_avg}"
timeline_fast: "{timeline_fast}"
timeline_complex: "{timeline_complex}"
embassy_city: "{dest_embassy_city}"
doc_processing_time: "{doc_time}"
date: 2026-05-01
{direct_answer_heading}
{direct_answer_intro}
{dap}
{overview_heading}
{overview_body}
dest_reception: "{dest_reception_text}"
dest_consular: "{dest_consular_text}"
{ts}
{faqs}
{links}
---
"""
    content = content.replace('vital statistics', 'civil registration')
    content = content.replace('state vital records', 'state civil records')
    content = content.replace('vital records', 'civil records')
    content = content.replace('—', ',')
    content = content.replace('–', ',')
    content = content.replace('\x96', ',')
    content = content.replace('\x97', ',')
    content = content.replace('---', '\x00TRIPLE\x00')
    content = content.replace('--', ',')
    content = content.replace('\x00TRIPLE\x00', '---')
    return content


# ---------------------------------------------------------------------------
# Route list: R43 (25) + R44 (25) + R45 (25) + R46 (25) = 100 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R43: Turkey wave 3 x5 + Malaysia wave 3 x5 + India wave 5 x5 +
    #     Singapore wave 5 x5 + Kuwait wave 5 x5 = 25
    ('russia',        'turkey'),
    ('saudi-arabia',  'turkey'),
    ('jordan',        'turkey'),
    ('algeria',       'turkey'),
    ('china',         'turkey'),
    ('sri-lanka',     'malaysia'),
    ('pakistan',      'malaysia'),
    ('south-korea',   'malaysia'),
    ('laos',          'malaysia'),
    ('hong-kong',     'malaysia'),
    ('iraq',          'india'),
    ('russia',        'india'),
    ('jordan',        'india'),
    ('turkey',        'india'),
    ('ethiopia',      'india'),
    ('ethiopia',      'singapore'),
    ('ghana',         'singapore'),
    ('morocco',       'singapore'),
    ('turkey',        'singapore'),
    ('iraq',          'singapore'),
    ('russia',        'kuwait'),
    ('algeria',       'kuwait'),
    ('morocco',       'kuwait'),
    ('uzbekistan',    'kuwait'),
    ('ukraine',       'kuwait'),
    # --- Block R44: South Africa wave 6 x5 + USA wave 6 x5 + Germany wave 7 x5 +
    #     France wave 6 x5 + Oman wave 1 (NEW HUB) x5 = 25
    ('ukraine',       'south-africa'),
    ('russia',        'south-africa'),
    ('indonesia',     'south-africa'),
    ('bangladesh',    'south-africa'),
    ('egypt',         'south-africa'),
    ('jordan',        'united-states'),
    ('algeria',       'united-states'),
    ('uzbekistan',    'united-states'),
    ('nicaragua',     'united-states'),
    ('costa-rica',    'united-states'),
    ('thailand',      'germany'),
    ('myanmar',       'germany'),
    ('south-africa',  'germany'),
    ('brazil',        'germany'),
    ('colombia',      'germany'),
    ('ethiopia',      'france'),
    ('kenya',         'france'),
    ('sri-lanka',     'france'),
    ('nepal',         'france'),
    ('myanmar',       'france'),
    ('india',         'oman'),
    ('pakistan',      'oman'),
    ('bangladesh',    'oman'),
    ('nepal',         'oman'),
    ('philippines',   'oman'),
    # --- Block R45: Turkey wave 4 x5 + Malaysia wave 4 x5 + Oman wave 2 x5 +
    #     Switzerland wave 5 x5 + Sweden wave 5 x5 = 25
    ('nigeria',       'turkey'),
    ('ghana',         'turkey'),
    ('kenya',         'turkey'),
    ('ethiopia',      'turkey'),
    ('bangladesh',    'turkey'),
    ('nigeria',       'malaysia'),
    ('ghana',         'malaysia'),
    ('kenya',         'malaysia'),
    ('ethiopia',      'malaysia'),
    ('saudi-arabia',  'malaysia'),
    ('ethiopia',      'oman'),
    ('kenya',         'oman'),
    ('sri-lanka',     'oman'),
    ('indonesia',     'oman'),
    ('egypt',         'oman'),
    ('nigeria',       'switzerland'),
    ('iran',          'switzerland'),
    ('bangladesh',    'switzerland'),
    ('indonesia',     'switzerland'),
    ('vietnam',       'switzerland'),
    ('ghana',         'sweden'),
    ('senegal',       'sweden'),
    ('pakistan',      'sweden'),
    ('ukraine',       'sweden'),
    ('indonesia',     'sweden'),
    # --- Block R46: Norway wave 5 x5 + Oman wave 3 x5 + South Africa wave 7 x5 +
    #     Portugal wave 5 x5 + Japan wave 5 x5 = 25
    ('ghana',         'norway'),
    ('senegal',       'norway'),
    ('indonesia',     'norway'),
    ('egypt',         'norway'),
    ('algeria',       'norway'),
    ('turkey',        'oman'),
    ('iraq',          'oman'),
    ('iran',          'oman'),
    ('jordan',        'oman'),
    ('morocco',       'oman'),
    ('malaysia',      'south-africa'),
    ('vietnam',       'south-africa'),
    ('philippines',   'south-africa'),
    ('nepal',         'south-africa'),
    ('myanmar',       'south-africa'),
    ('ghana',         'portugal'),
    ('ethiopia',      'portugal'),
    ('iraq',          'portugal'),
    ('egypt',         'portugal'),
    ('algeria',       'portugal'),
    ('south-africa',  'japan'),
    ('nigeria',       'japan'),
    ('ghana',         'japan'),
    ('ethiopia',      'japan'),
    ('kenya',         'japan'),
]

# ---------------------------------------------------------------------------
# Run generation
# ---------------------------------------------------------------------------

generated, skipped, errors = [], [], []
variant_idx = START_VARIANT

for origin_slug, dest_slug in ALL_ROUTES:
    slug = f'{origin_slug}-to-{dest_slug}'
    out_path = os.path.join(ROUTES_DIR, f'{slug}.md')

    if os.path.exists(out_path):
        skipped.append(slug)
        variant_idx += 1
        continue

    variant = VARIANTS[variant_idx % 5]
    content = make_route(origin_slug, dest_slug, variant)

    if content is None:
        errors.append(slug)
        variant_idx += 1
        continue

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    generated.append((slug, variant))
    variant_idx += 1

print(f"\nGenerated: {len(generated)}")
print(f"Skipped (already exist): {len(skipped)}")
print(f"Errors: {len(errors)}")

if generated:
    print("\nNew files:")
    for slug, var in generated:
        print(f"  {slug}.md  [variant {var}]")
if skipped:
    print("\nSkipped:")
    for s in skipped:
        print(f"  {s}")
if errors:
    print("\nERRORS (no UK source file):")
    for e in errors:
        print(f"  {e}")
