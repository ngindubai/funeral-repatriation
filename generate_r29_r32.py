#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R29-R32.

   R29: Germany wave 4 x5 + France wave 4 x5 + UAE wave 4 x5 +
        Canada wave 4 x5 + Australia wave 4 x5 = 25
   R30: Qatar wave 3 x5 + Kuwait wave 3 x5 + Singapore wave 3 x5 +
        South Africa wave 3 x5 + USA wave 4 x5 = 25
   R31: Switzerland wave 3 x5 + Sweden wave 3 x5 + Norway wave 3 x5 +
        Portugal wave 3 x5 + Saudi Arabia wave 3 x5 = 25
   R32: Japan (new hub) x8 + New Zealand (new hub) x7 +
        Belgium wave 4 x5 + Germany wave 5 x5 = 25

   Template rotation: R28 ended on C (index 2). R29 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R28 ended C (index 2); R29 starts D (index 3)

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
    # --- Existing hubs (carried from earlier generators) ---
    'germany': {
        'name': 'Germany',
        'slug': 'germany',
        'key': 'de',
        'reception': (
            "The German funeral director takes custody at the cargo terminal, typically "
            "Frankfurt (FRA), Munich (MUC), or Berlin (BER). A Leichenpass (body transport "
            "passport) or equivalent laissez-passer must accompany the remains. The local "
            "Gesundheitsamt (public health authority) may inspect the remains on arrival. "
            "The receiving funeral director registers the death with the local Standesamt "
            "(civil registry) if required. "
            "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
        ),
        'consular_template': (
            "German Embassy in {city} can advise on document requirements for repatriation "
            "to Germany. Federal Foreign Office (Auswaertiges Amt) emergency assistance: "
            "+49 30 5000 2000 (24 hours). The German Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The German funeral director takes custody at the cargo terminal. "
            "A Leichenpass or laissez-passer must accompany the remains. "
            "The Gesundheitsamt may inspect the remains on arrival. "
            "The death is registered with the local Standesamt. "
            "All foreign documents must carry certified German translation where required."
        ),
        'emergency_line': '+49 30 5000 2000',
        'hub_url': 'repatriation-from-germany',
    },
    'france': {
        'name': 'France',
        'slug': 'france',
        'key': 'fr',
        'reception': (
            "The French funeral director (pompes funebres) takes custody at Charles de Gaulle "
            "(CDG, Paris) or another French international airport. The prefecture may require "
            "a permis d'inhumer (burial permit) or transport authorisation before burial or "
            "cremation can proceed. All foreign documents must carry a certified French "
            "translation. "
            "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
        ),
        'consular_template': (
            "French Embassy in {city} can advise on repatriation documentation requirements "
            "for France. French Ministry of Europe and Foreign Affairs (MAE) emergency "
            "assistance: +33 1 43 17 67 67 (24 hours). The French Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The French funeral director takes custody at Charles de Gaulle (CDG) or another "
            "French airport. The prefecture issues a permis d'inhumer before burial or "
            "cremation. All foreign documents require certified French translation. "
            "The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+33 1 43 17 67 67',
        'hub_url': 'repatriation-from-france',
    },
    'united-arab-emirates': {
        'name': 'United Arab Emirates',
        'slug': 'united-arab-emirates',
        'key': 'ae',
        'reception': (
            "The UAE funeral home or government mortuary takes custody at Dubai International "
            "(DXB) or Abu Dhabi International (AUH) cargo terminal. UAE Ministry of Health "
            "clearance is required before burial or cremation. All foreign documentation must "
            "be attested by the UAE Embassy in the country of origin and authenticated by "
            "UAE authorities. "
            "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
        ),
        'consular_template': (
            "UAE Embassy in {city} handles attestation of repatriation documents. Contact "
            "the UAE Embassy in {country_name} for document authentication requirements. "
            "UAE Ministry of Foreign Affairs and International Cooperation (MOFAIC) can be "
            "reached via the UAE Embassy during business hours."
        ),
        'arrival_faq': (
            "The UAE funeral home takes custody at Dubai (DXB) or Abu Dhabi (AUH) cargo "
            "terminal. UAE Ministry of Health clearance is required. All documents must be "
            "attested by the UAE Embassy in the country of origin. Islamic remains require "
            "certification for Islamic burial; non-Islamic remains follow separate procedures."
        ),
        'emergency_line': 'contact UAE Embassy in origin country',
        'hub_url': 'repatriation-from-united-arab-emirates',
    },
    'canada': {
        'name': 'Canada',
        'slug': 'canada',
        'key': 'ca',
        'reception': (
            "The Canadian funeral director takes custody at the cargo terminal. Canadian "
            "Border Services Agency (CBSA) clearance is required. The required documents are: "
            "the foreign death certificate, transit or burial permit, and embalming "
            "certificate. Provincial or territorial regulations apply and vary between "
            "Ontario, British Columbia, Quebec, Alberta, and other provinces. "
            "(Global Affairs Canada, 2025.)"
        ),
        'consular_template': (
            "Canadian Embassy or High Commission in {city} can assist Canadian citizens "
            "and their families with consular registration of the death and provide a list "
            "of local funeral directors. They cannot pay for or arrange repatriation. "
            "Global Affairs Canada emergency line: +1 (613) 996-8885 (24 hours, collect "
            "calls accepted)."
        ),
        'arrival_faq': (
            "The Canadian funeral director takes custody at the cargo terminal. CBSA "
            "clearance requires the foreign death certificate, transit or burial permit, "
            "and embalming certificate. Provincial regulations govern the burial or "
            "cremation. The receiving funeral director notifies the appropriate "
            "provincial authority."
        ),
        'emergency_line': '+1 (613) 996-8885',
        'hub_url': 'repatriation-from-canada',
    },
    'australia': {
        'name': 'Australia',
        'slug': 'australia',
        'key': 'au',
        'reception': (
            "The Australian funeral director takes custody at the cargo terminal. Australian "
            "Border Force clearance is required. State or territory funeral regulations govern "
            "burial or cremation; requirements differ between New South Wales, Victoria, "
            "Queensland, Western Australia, South Australia, and the Northern Territory. "
            "All documentation must be authenticated. "
            "(Australian Government, Department of Foreign Affairs and Trade, DFAT, 2025.)"
        ),
        'consular_template': (
            "Australian Embassy or High Commission in {city} can assist Australian citizens "
            "and their families with consular registration of the death and provide a list "
            "of local funeral directors. They cannot pay for or arrange repatriation. "
            "Australian Government Consular Emergency Centre: +61 2 6261 3305 (24 hours)."
        ),
        'arrival_faq': (
            "The Australian funeral director takes custody at the cargo terminal. Australian "
            "Border Force clearance requires the foreign death certificate, transit permit, "
            "and embalming certificate. State or territory regulations govern burial or "
            "cremation. The receiving funeral director coordinates with the relevant "
            "state authority."
        ),
        'emergency_line': '+61 2 6261 3305',
        'hub_url': 'repatriation-from-australia',
    },
    'qatar': {
        'name': 'Qatar',
        'slug': 'qatar',
        'key': 'qa',
        'reception': (
            "The Qatari funeral home or government mortuary takes custody at Hamad "
            "International Airport (DOH) cargo terminal. Qatar Ministry of Public Health "
            "approval is required before the remains can be received. All documents must "
            "be attested by the Qatari Embassy in the country of origin. "
            "(Qatar Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Qatar Embassy in {city} handles attestation of repatriation documents. "
            "Contact the Qatar Embassy in {country_name} for document authentication "
            "requirements. Qatar Ministry of Foreign Affairs can be reached via the "
            "Qatar Embassy."
        ),
        'arrival_faq': (
            "The Qatari funeral home takes custody at Hamad International (DOH) cargo "
            "terminal. Qatar Ministry of Public Health clearance is required in advance. "
            "All documents must be attested by the Qatar Embassy in the origin country. "
            "The family or sponsor in Qatar coordinates with the receiving authorities."
        ),
        'emergency_line': 'contact Qatar Embassy in origin country',
        'hub_url': 'repatriation-from-qatar',
    },
    'kuwait': {
        'name': 'Kuwait',
        'slug': 'kuwait',
        'key': 'kw',
        'reception': (
            "The Kuwaiti funeral home or government mortuary takes custody at Kuwait "
            "International Airport (KWI). Kuwait Ministry of Health clearance is required "
            "before the remains can be received. All documents must be attested by the "
            "Kuwaiti Embassy in the country of origin. "
            "(Kuwait Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Kuwait Embassy in {city} handles attestation of repatriation documents. "
            "Contact the Kuwait Embassy in {country_name} for document authentication "
            "requirements. Kuwait Ministry of Foreign Affairs coordinates with the "
            "receiving authorities."
        ),
        'arrival_faq': (
            "The Kuwaiti funeral home takes custody at Kuwait International (KWI). "
            "Kuwait Ministry of Health clearance is required in advance. "
            "All documents must be attested by the Kuwait Embassy in the origin country. "
            "The family or sponsor in Kuwait coordinates with the receiving mortuary."
        ),
        'emergency_line': 'contact Kuwait Embassy in origin country',
        'hub_url': 'repatriation-from-kuwait',
    },
    'singapore': {
        'name': 'Singapore',
        'slug': 'singapore',
        'key': 'sg',
        'reception': (
            "The Singapore funeral director takes custody at Changi Airport (SIN) cargo "
            "terminal. Singapore Customs clearance is required. The National Environment "
            "Agency (NEA) regulates the import of human remains into Singapore. All foreign "
            "death certificates must be authenticated by the Singapore Embassy or High "
            "Commission in the country of origin. "
            "(Singapore Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Singapore High Commission or Embassy in {city} can advise on documentation "
            "requirements and authenticate foreign certificates. They cannot pay for or "
            "arrange repatriation. Singapore Ministry of Foreign Affairs 24-hour emergency: "
            "+65 6379 8000."
        ),
        'arrival_faq': (
            "The Singapore funeral director takes custody at Changi Airport (SIN) cargo "
            "terminal. Singapore Customs clearance requires the authenticated death "
            "certificate, transit permit, and embalming certificate. The National "
            "Environment Agency (NEA) regulates the import of remains. All foreign "
            "documents must be authenticated by the Singapore Embassy in the origin country."
        ),
        'emergency_line': '+65 6379 8000',
        'hub_url': 'repatriation-from-singapore',
    },
    'south-africa': {
        'name': 'South Africa',
        'slug': 'south-africa',
        'key': 'za',
        'reception': (
            "The South African funeral director takes custody at the cargo terminal, "
            "typically O.R. Tambo International (JNB, Johannesburg), Cape Town International "
            "(CPT), or King Shaka International (DUR, Durban). A permit from the South "
            "African Department of Home Affairs (Form DHA-1744) is required before burial "
            "or cremation. The provincial health authority issues any additional permits. "
            "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
        ),
        'consular_template': (
            "South African Embassy or High Commission in {city} can advise on documentation "
            "requirements for repatriation to South Africa. They cannot pay for or arrange "
            "repatriation. Contact the nearest South African mission for assistance."
        ),
        'arrival_faq': (
            "The South African funeral director takes custody at the cargo terminal. "
            "Department of Home Affairs Form DHA-1744 is required before burial or cremation. "
            "The provincial health authority may issue additional permits. "
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
            "The US funeral director takes custody at the cargo terminal. US Customs "
            "clearance requires a transit or burial permit, the foreign death certificate, "
            "and an embalming certificate. State health department regulations apply and "
            "vary by state. The receiving funeral director notifies the medical examiner "
            "or coroner as required by state law. "
            "(US State Department, Bureau of Consular Affairs, 2025.)"
        ),
        'consular_template': (
            "US Embassy in {city} can assist US citizens and their families with consular "
            "registration of the death and provide a list of local funeral directors. They "
            "cannot pay for or arrange repatriation. State Department emergency line: "
            "+1 (888) 407-4747 (within the US) or +1 (202) 501-4444 (from overseas), "
            "24 hours."
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
            "(FDFA) helpline: +41 800 24-7-365 (24 hours). The Swiss Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Swiss Bestatter takes custody at Zurich (ZRH) or Geneva (GVA) cargo "
            "terminal. A Leichentransportschein must accompany the coffin. The "
            "Zivilstandsamt registers the death. The Kantonsarzt may inspect the remains. "
            "Documents not in German, French, or Italian require certified translation."
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
            "A laissez-passer must accompany the remains. Skatteverket (Swedish Tax Agency) "
            "is notified to update the population register. Sweden is a Hague Apostille "
            "Convention member. Documents not in Swedish or English require certified "
            "Swedish translation. "
            "(Swedish Ministry of Foreign Affairs, UD, 2025.)"
        ),
        'consular_template': (
            "Swedish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Sweden. Swedish Ministry of Foreign Affairs emergency line: "
            "+46 8 405 50 05 (24 hours). The Swedish Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Swedish begravningsentreprenor takes custody at Stockholm Arlanda (ARN) "
            "or Gothenburg Landvetter (GOT) cargo terminal. A laissez-passer must "
            "accompany the remains. Skatteverket is notified to update the population "
            "register. Documents not in Swedish or English require certified Swedish "
            "translation."
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
            "Gardermoen (OSL) cargo terminal. A laissez-passer or equivalent body transport "
            "document must accompany the coffin. The Folkeregisteret (National Population "
            "Register) records the death. Norway is a Hague Apostille Convention member "
            "(EEA, not EU). Documents not in Norwegian or English require certified "
            "Norwegian translation. "
            "(Norwegian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Norwegian Embassy in {city} can advise on documentation requirements for "
            "repatriation to Norway. Norwegian Ministry of Foreign Affairs emergency line: "
            "+47 23 95 00 00 (24 hours). The Norwegian Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Norwegian begravelsesbyraa takes custody at Oslo Gardermoen (OSL) cargo "
            "terminal. A laissez-passer must accompany the coffin. The Folkeregisteret "
            "records the death. Documents not in Norwegian or English require certified "
            "Norwegian translation."
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
            "(health authority) clearance is required before burial or cremation. The "
            "Conservatoria do Registo Civil registers the death. Portugal is an EU and "
            "Hague Apostille Convention member. Documents from non-EU countries require "
            "certified Portuguese translation. "
            "(Portuguese Ministry of Foreign Affairs, MNE, 2025.)"
        ),
        'consular_template': (
            "Portuguese Embassy in {city} can advise on documentation requirements for "
            "repatriation to Portugal. Portuguese Ministry of Foreign Affairs (MNE) "
            "emergency line: +351 21 394 6000 (24 hours). The Portuguese Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Portuguese agencia funeraria takes custody at Lisbon (LIS), Porto (OPO), "
            "or Faro (FAO) cargo terminal. Autoridade de Saude clearance is required. "
            "The Conservatoria do Registo Civil registers the death. Non-EU documents "
            "require certified Portuguese translation."
        ),
        'emergency_line': '+351 21 394 6000',
        'hub_url': 'repatriation-from-portugal',
    },
    'saudi-arabia': {
        'name': 'Saudi Arabia',
        'slug': 'saudi-arabia',
        'key': 'sa',
        'reception': (
            "The Saudi government mortuary or funeral home takes custody at King Khalid "
            "International (RUH, Riyadh), King Abdulaziz International (JED, Jeddah), or "
            "King Fahd International (DMM, Dammam) cargo terminal. Saudi Ministry of Health "
            "approval is required before the remains can be received. All documents must be "
            "authenticated by the Saudi Embassy in the country of origin. Non-Muslim remains "
            "require specific certification and procedures. "
            "(Saudi Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Saudi Embassy in {city} handles authentication of repatriation documents. "
            "Contact the Saudi Embassy in {country_name} for document legalisation "
            "requirements. Saudi Ministry of Foreign Affairs coordinates with the receiving "
            "authorities in Saudi Arabia."
        ),
        'arrival_faq': (
            "The Saudi government mortuary takes custody at King Khalid (RUH), King Abdulaziz "
            "(JED), or King Fahd (DMM) cargo terminal. Saudi Ministry of Health clearance is "
            "required in advance. All documents must be authenticated by the Saudi Embassy "
            "in the origin country. Non-Muslim remains require specific certification. "
            "The family or sponsor in Saudi Arabia coordinates with the receiving authorities."
        ),
        'emergency_line': 'contact Saudi Embassy in origin country',
        'hub_url': 'repatriation-from-saudi-arabia',
    },
    'belgium': {
        'name': 'Belgium',
        'slug': 'belgium',
        'key': 'be',
        'reception': (
            "The Belgian funeral director (entrepreneur des pompes funebres or "
            "begrafenisondernemer) takes custody at Brussels Airport (BRU) or Liege Airport "
            "(LGG) cargo terminal. The local commune or gemeente registers the death with "
            "the Registre de la Population. A transport authorisation is required before "
            "burial or cremation. All foreign documents must carry a certified French or "
            "Dutch translation. "
            "(Belgian Federal Public Service Foreign Affairs, FPS Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Belgian Embassy in {city} can advise on documentation requirements for "
            "repatriation to Belgium. Belgian Federal Public Service Foreign Affairs "
            "emergency line: +32 2 501 8111 (24 hours). The Belgian Embassy cannot pay "
            "for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Belgian funeral director takes custody at Brussels Airport (BRU) cargo "
            "terminal. A transport authorisation is required before burial or cremation. "
            "The local commune or gemeente registers the death. All foreign documents "
            "require certified French or Dutch translation."
        ),
        'emergency_line': '+32 2 501 8111',
        'hub_url': 'repatriation-from-belgium',
    },
    # --- New hubs introduced in R32 ---
    'japan': {
        'name': 'Japan',
        'slug': 'japan',
        'key': 'jp',
        'reception': (
            "The Japanese funeral director (sosogiya) takes custody at Narita International "
            "(NRT) or Kansai International (KIX) cargo terminal. The municipality "
            "(shi/ku/cho/son) registers the death in the koseki (family register). A "
            "sanitised coffin certificate and laissez-passer must accompany the remains. "
            "The Ministry of Health, Labour and Welfare (MHLW) regulations apply to the "
            "import of human remains. Documents not in Japanese require certified Japanese "
            "translation. "
            "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
        ),
        'consular_template': (
            "Japanese Embassy in {city} can advise on documentation requirements for "
            "repatriation to Japan. Japanese Ministry of Foreign Affairs (MOFA) emergency "
            "line: +81 3 3580 3311 (24 hours). The Japanese Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Japanese funeral director takes custody at Narita (NRT) or Kansai (KIX) "
            "cargo terminal. The municipality registers the death in the koseki. A "
            "sanitised coffin certificate and laissez-passer must accompany the remains. "
            "Documents not in Japanese require certified Japanese translation. The receiving "
            "funeral director coordinates with the municipal office and health authorities."
        ),
        'emergency_line': '+81 3 3580 3311',
        'hub_url': 'repatriation-from-japan',
    },
    'new-zealand': {
        'name': 'New Zealand',
        'slug': 'new-zealand',
        'key': 'nz',
        'reception': (
            "The New Zealand funeral director takes custody at Auckland International (AKL), "
            "Wellington (WLG), or Christchurch (CHC) cargo terminal. New Zealand Customs "
            "clearance is required. The Registrar-General of Births, Deaths and Marriages "
            "records the death under the Births, Deaths, Marriages, and Relationships "
            "Registration Act 2021. The Coroner may need to be notified under the Coroners "
            "Act 2006. All foreign documentation must be authenticated. "
            "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
        ),
        'consular_template': (
            "New Zealand Embassy or High Commission in {city} can assist New Zealand "
            "citizens and their families with consular registration of the death and "
            "provide guidance on required documentation. They cannot pay for or arrange "
            "repatriation. New Zealand Ministry of Foreign Affairs and Trade (MFAT) "
            "emergency line: +64 4 439 8000 (24 hours)."
        ),
        'arrival_faq': (
            "The New Zealand funeral director takes custody at Auckland (AKL), Wellington "
            "(WLG), or Christchurch (CHC) cargo terminal. New Zealand Customs clearance "
            "requires the foreign death certificate, transit permit, and embalming "
            "certificate. The Registrar-General records the death. The Coroner may need "
            "to be notified. The receiving funeral director coordinates with local "
            "authorities."
        ),
        'emergency_line': '+64 4 439 8000',
        'hub_url': 'repatriation-from-new-zealand',
    },
}

# ---------------------------------------------------------------------------
# Embassy cities: destination country's embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R29: Germany wave 4
    # German Embassy in Damascus closed 2012; covered from Beirut
    ('syria',        'germany'): 'Beirut',
    ('lebanon',      'germany'): 'Beirut',
    ('jordan',       'germany'): 'Amman',
    ('indonesia',    'germany'): 'Jakarta',
    ('philippines',  'germany'): 'Manila',
    # R29: France wave 4
    ('ghana',        'france'): 'Accra',
    ('lebanon',      'france'): 'Beirut',
    ('pakistan',     'france'): 'Islamabad',
    ('india',        'france'): 'New Delhi',
    ('bangladesh',   'france'): 'Dhaka',
    # R29: UAE wave 4
    ('iran',         'united-arab-emirates'): 'Tehran',
    ('lebanon',      'united-arab-emirates'): 'Beirut',
    ('oman',         'united-arab-emirates'): 'Muscat',
    ('eritrea',      'united-arab-emirates'): 'Asmara',
    ('sudan',        'united-arab-emirates'): 'Khartoum',
    # R29: Canada wave 4
    ('colombia',     'canada'): 'Bogota',
    ('ecuador',      'canada'): 'Quito',
    ('peru',         'canada'): 'Lima',
    ('brazil',       'canada'): 'Brasilia',
    ('haiti',        'canada'): 'Port-au-Prince',
    # R29: Australia wave 4
    ('japan',        'australia'): 'Tokyo',
    ('south-africa', 'australia'): 'Pretoria',
    ('tonga',        'australia'): 'Nukualofa',
    ('papua-new-guinea', 'australia'): 'Port Moresby',
    ('ukraine',      'australia'): 'Kyiv',
    # R30: Qatar wave 3
    ('vietnam',      'qatar'): 'Hanoi',
    ('china',        'qatar'): 'Beijing',
    ('iran',         'qatar'): 'Tehran',
    ('morocco',      'qatar'): 'Rabat',
    # Qatar Embassy in Mogadishu; Somali representation via Nairobi
    ('somalia',      'qatar'): 'Nairobi',
    # R30: Kuwait wave 3
    ('jordan',       'kuwait'): 'Amman',
    ('malaysia',     'kuwait'): 'Kuala Lumpur',
    ('china',        'kuwait'): 'Beijing',
    ('turkey',       'kuwait'): 'Ankara',
    ('iran',         'kuwait'): 'Tehran',
    # R30: Singapore wave 3
    ('japan',        'singapore'): 'Tokyo',
    ('nepal',        'singapore'): 'Kathmandu',
    ('cambodia',     'singapore'): 'Phnom Penh',
    ('hong-kong',    'singapore'): 'Hong Kong',
    ('laos',         'singapore'): 'Vientiane',
    # R30: South Africa wave 3
    # South Africa has no embassy in Somalia; covers via Nairobi
    ('somalia',      'south-africa'): 'Nairobi',
    ('rwanda',       'south-africa'): 'Kigali',
    ('burundi',      'south-africa'): 'Bujumbura',
    ('eritrea',      'south-africa'): 'Asmara',
    ('ivory-coast',  'south-africa'): 'Abidjan',
    # R30: USA wave 4
    # US Embassy in Damascus closed 2012; covers Syria from Beirut
    ('russia',       'united-states'): 'Moscow',
    ('lebanon',      'united-states'): 'Beirut',
    ('eritrea',      'united-states'): 'Asmara',
    ('iraq',         'united-states'): 'Baghdad',
    ('syria',        'united-states'): 'Beirut',
    # R31: Switzerland wave 3
    ('egypt',        'switzerland'): 'Cairo',
    ('chile',        'switzerland'): 'Santiago',
    ('colombia',     'switzerland'): 'Bogota',
    ('brazil',       'switzerland'): 'Brasilia',
    ('china',        'switzerland'): 'Beijing',
    # R31: Sweden wave 3
    ('nigeria',      'sweden'): 'Abuja',
    ('kenya',        'sweden'): 'Nairobi',
    ('morocco',      'sweden'): 'Rabat',
    ('tunisia',      'sweden'): 'Tunis',
    ('china',        'sweden'): 'Beijing',
    # R31: Norway wave 3
    ('nigeria',      'norway'): 'Abuja',
    ('kenya',        'norway'): 'Nairobi',
    ('morocco',      'norway'): 'Rabat',
    ('turkey',       'norway'): 'Ankara',
    ('china',        'norway'): 'Beijing',
    # R31: Portugal wave 3
    ('morocco',      'portugal'): 'Rabat',
    ('guinea',       'portugal'): 'Conakry',
    ('senegal',      'portugal'): 'Dakar',
    ('nigeria',      'portugal'): 'Abuja',
    ('turkey',       'portugal'): 'Ankara',
    # R31: Saudi Arabia wave 3
    ('malaysia',     'saudi-arabia'): 'Kuala Lumpur',
    ('vietnam',      'saudi-arabia'): 'Hanoi',
    ('china',        'saudi-arabia'): 'Beijing',
    ('eritrea',      'saudi-arabia'): 'Asmara',
    # Saudi Embassy reopened in Tehran March 2023
    ('iran',         'saudi-arabia'): 'Tehran',
    # R32: Japan corridors
    ('china',        'japan'): 'Beijing',
    ('south-korea',  'japan'): 'Seoul',
    ('philippines',  'japan'): 'Manila',
    ('vietnam',      'japan'): 'Hanoi',
    ('india',        'japan'): 'New Delhi',
    # Japanese Embassy in Myanmar is in Yangon
    ('myanmar',      'japan'): 'Yangon',
    ('indonesia',    'japan'): 'Jakarta',
    ('brazil',       'japan'): 'Brasilia',
    # R32: New Zealand corridors
    ('india',        'new-zealand'): 'New Delhi',
    ('china',        'new-zealand'): 'Beijing',
    ('philippines',  'new-zealand'): 'Manila',
    ('fiji',         'new-zealand'): 'Suva',
    ('samoa',        'new-zealand'): 'Apia',
    ('tonga',        'new-zealand'): 'Nukualofa',
    ('south-africa', 'new-zealand'): 'Pretoria',
    ('south-korea',  'new-zealand'): 'Seoul',
    # R32: Belgium wave 4
    ('france',       'belgium'): 'Paris',
    ('kenya',        'belgium'): 'Nairobi',
    ('eritrea',      'belgium'): 'Asmara',
    ('burkina-faso', 'belgium'): 'Ouagadougou',
    ('lebanon',      'belgium'): 'Beirut',
    # R32: Germany wave 5
    ('ivory-coast',  'germany'): 'Abidjan',
    ('mali',         'germany'): 'Bamako',
    ('togo',         'germany'): 'Lome',
    ('guinea',       'germany'): 'Conakry',
    # German Embassy covering Somalia is in Nairobi
    ('somalia',      'germany'): 'Nairobi',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R29: Germany wave 4
    ('syria', 'germany'): (
        "Syrian nationals form one of Germany's largest Middle Eastern diaspora communities, "
        "with over 800,000 Syrians having arrived in Germany since 2015. Germany accepted more "
        "Syrian refugees than any other European country during that period. The German Embassy "
        "in Damascus closed in 2012; German consular services for Syria are provided from the "
        "German Embassy in Beirut. Arabic documentation requires certified German translation. "
        "Specialist coordination is recommended given the civil registration situation in "
        "different parts of Syria. (German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    ('lebanon', 'germany'): (
        "Lebanese nationals form part of Germany's Middle Eastern diaspora, with tens of "
        "thousands of residents in Berlin, Hamburg, and other German cities. Some arrived "
        "during the Lebanese civil war and its aftermath; others came more recently. The "
        "German Embassy in Beirut handles consular matters. Arabic documentation requires "
        "certified German translation. Lebanon to Germany is a consistent repatriation "
        "corridor."
    ),
    ('jordan', 'germany'): (
        "Jordanian nationals work in Germany in professional and academic roles, part of the "
        "broader Arab diaspora. The German Embassy in Amman handles consular matters. Arabic "
        "documentation from Jordan requires certified German translation. Jordan's Civil "
        "Status and Passport Department issues the official death certificate for international "
        "repatriation, and documentation is generally organised and well-structured."
    ),
    ('indonesia', 'germany'): (
        "Indonesian nationals form a growing South-East Asian community in Germany, working "
        "in technology, healthcare, and academic roles in Berlin, Hamburg, and Frankfurt. The "
        "German Embassy in Jakarta handles consular matters. Indonesian documentation requires "
        "certified German translation. This corridor sees demand from Indonesian professionals "
        "and students at German universities."
    ),
    ('philippines', 'germany'): (
        "Filipino nationals work in Germany primarily in healthcare and nursing, recruited "
        "as part of Germany's bilateral migration agreements with the Philippines. The "
        "Qualified Professionals Immigration Act has accelerated recruitment. The German "
        "Embassy in Manila handles consular matters. Filipino documentation requires certified "
        "German translation. The Philippine DFA authentication adds to the documentation "
        "timeline."
    ),
    # R29: France wave 4
    ('ghana', 'france'): (
        "Ghanaian nationals form part of France's West African diaspora, with a community "
        "in Paris and other French cities working in professional and service roles. English "
        "documentation from Ghana requires certified French translation for French civil "
        "registry purposes. The French Embassy in Accra handles consular matters. This "
        "corridor handles cases where a France-based Ghanaian has a family member die in "
        "Ghana and needs remains brought to France."
    ),
    ('lebanon', 'france'): (
        "Lebanese nationals form a significant community in France, estimated at 30,000 to "
        "40,000 residents. France and Lebanon share historical and cultural connections through "
        "the French Mandate period and the Francophonie. Many Lebanese families have dual "
        "Franco-Lebanese ties. French is widely used in Lebanese institutions, which simplifies "
        "some documentation requirements. The French Embassy in Beirut handles consular matters."
    ),
    ('pakistan', 'france'): (
        "Pakistani nationals form a growing South Asian community in France, working in "
        "retail, hospitality, and professional services across Paris and other cities. This "
        "corridor handles cases where a France-based Pakistani has a family member die in "
        "Pakistan and needs remains brought to France. Documentation in Urdu and Punjabi "
        "from Pakistan requires certified French translation. The French Embassy in Islamabad "
        "handles consular matters."
    ),
    ('india', 'france'): (
        "Indian nationals form a significant professional community in France, working in "
        "technology, pharmaceuticals, and consulting. India-France bilateral agreements have "
        "deepened people-to-people ties in recent years. The French Embassy in New Delhi "
        "handles consular matters. Hindi and regional Indian documentation requires certified "
        "French translation where required by French civil registry authorities."
    ),
    ('bangladesh', 'france'): (
        "Bangladeshi nationals form part of France's South Asian diaspora, with a community "
        "concentrated in Paris working in retail, catering, and services. This corridor "
        "handles cases where a France-based Bangladeshi has a family member die in Bangladesh "
        "and needs remains brought to France. Bengali documentation requires certified French "
        "translation. The French Embassy in Dhaka handles consular matters."
    ),
    # R29: UAE wave 4
    ('iran', 'united-arab-emirates'): (
        "Iranian nationals form one of the UAE's largest non-Arab expatriate communities, "
        "with a significant presence in Dubai's Deira and Bur Dubai districts. The UAE and "
        "Iran restored full diplomatic relations in 2023, and the UAE Embassy in Tehran "
        "resumed normal operations. All documentation must be attested by the UAE Embassy "
        "in Tehran. Arabic and Persian are both relevant on this corridor. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    ('lebanon', 'united-arab-emirates'): (
        "Lebanese nationals form a significant professional community in the UAE, concentrated "
        "in Dubai and Abu Dhabi, working in finance, law, retail, and hospitality. Lebanese "
        "nationals are among the most established Arab professional diaspora communities in "
        "the Gulf. Arabic documentation from Lebanon is the working language on both sides "
        "of this corridor, which simplifies some requirements."
    ),
    ('oman', 'united-arab-emirates'): (
        "Omani nationals travel regularly to the UAE for work and family reasons, and the "
        "two countries share a border and close GCC ties. Oman and the UAE are fellow Gulf "
        "Cooperation Council members with closely aligned regulations. Arabic documentation "
        "is the working language on both sides. The UAE Embassy in Muscat handles document "
        "attestation requirements. This is a short-distance, well-organised corridor."
    ),
    ('eritrea', 'united-arab-emirates'): (
        "Eritrean nationals work in the UAE in construction, domestic services, and retail "
        "across Dubai and Abu Dhabi. The UAE Embassy in Asmara handles document attestation "
        "requirements. Tigrinya documentation from Eritrea requires certified Arabic "
        "translation for UAE authorities. All documents must be attested by the UAE Embassy "
        "in Asmara before the body can depart. Specialist coordination is recommended."
    ),
    ('sudan', 'united-arab-emirates'): (
        "Sudanese nationals form a significant professional and worker community in the UAE, "
        "with many in Dubai and Abu Dhabi. This corridor requires careful coordination given "
        "the ongoing conflict in parts of Sudan since April 2023. The UAE Embassy works with "
        "Sudanese authorities through its mission in Khartoum, though access from "
        "conflict-affected areas may require additional time and specialist support. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    # R29: Canada wave 4
    ('colombia', 'canada'): (
        "Colombian nationals form one of Canada's larger Latin American communities, "
        "concentrated in Toronto, Montreal, and Vancouver. Canada has received Colombian "
        "migration through both economic and humanitarian channels since the 1990s. "
        "Documentation from Colombia is in Spanish, requiring certified English or French "
        "translation for Canadian authorities. The Canadian Embassy in Bogota handles "
        "consular matters."
    ),
    ('ecuador', 'canada'): (
        "Ecuadorian nationals form part of Canada's Latin American diaspora, working in "
        "construction, agriculture, and services. This corridor handles cases where a "
        "Canada-based Ecuadorian has a family member die in Ecuador and needs remains "
        "brought to Canada. Documentation from Ecuador is in Spanish, requiring certified "
        "English or French translation. The Canadian Embassy in Quito handles consular "
        "matters."
    ),
    ('peru', 'canada'): (
        "Peruvian nationals form a growing Latin American community in Canada, concentrated "
        "in Toronto and Montreal. This corridor handles cases where a Canada-based Peruvian "
        "has a family member die in Peru and needs remains brought to Canada. Documentation "
        "from Peru is in Spanish, requiring certified English or French translation for "
        "Canadian authorities. The Canadian Embassy in Lima handles consular matters."
    ),
    ('brazil', 'canada'): (
        "Brazilian nationals form a significant South American community in Canada, "
        "particularly in Toronto and Montreal. This corridor handles cases where a "
        "Canada-based Brazilian has a family member die in Brazil and needs remains brought "
        "to Canada. Documentation from Brazil is in Portuguese, requiring certified English "
        "or French translation. The Canadian Embassy in Brasilia handles consular matters."
    ),
    ('haiti', 'canada'): (
        "Haitian nationals form Canada's largest Caribbean diaspora community, with a "
        "significant population in Montreal reflecting Quebec and Haiti's shared French "
        "language connection. This corridor handles cases where a Canada-based Haitian "
        "has a family member die in Haiti and needs remains brought to Canada. The Canadian "
        "Embassy in Port-au-Prince handles consular matters, though operations have faced "
        "challenges given Haiti's security situation. Specialist coordination is recommended. "
        "(Global Affairs Canada, 2025.)"
    ),
    # R29: Australia wave 4
    ('japan', 'australia'): (
        "Japanese nationals work in Australia in business, tourism, and academic roles, "
        "and Japan to Australia is an established repatriation corridor. Australia and Japan "
        "have close bilateral ties. Japanese documentation is highly organised and the "
        "Japanese Embassy in Canberra or consulates in major cities handle matters "
        "efficiently. The Australian High Commission in Tokyo handles consular matters "
        "for Australians who die in Japan. This is a well-structured corridor on both sides."
    ),
    ('south-africa', 'australia'): (
        "South African nationals form an established immigrant community in Australia, "
        "particularly in Perth and Sydney. Many South Africans emigrated to Australia from "
        "the late 1980s onward. South Africa to Australia is an active corridor for the "
        "South African diaspora. English documentation from South Africa simplifies "
        "requirements for Australian Border Force. The Australian High Commission in "
        "Pretoria handles consular matters."
    ),
    ('tonga', 'australia'): (
        "Tongan nationals form one of Australia's most established Pacific Island communities, "
        "concentrated in Sydney and Brisbane. Australia and Tonga have close bilateral ties "
        "and Australia is the primary repatriation destination for the Tongan diaspora. "
        "Documentation from Tonga in English simplifies requirements for Australian Border "
        "Force. The Australian High Commission in Nukualofa handles consular matters. Direct "
        "flights connect Nadi (via Fiji) to Australian cities."
    ),
    ('papua-new-guinea', 'australia'): (
        "Papua New Guinean nationals and Australian residents of PNG heritage reflect the "
        "close historical and geographic relationship between the two countries. Papua New "
        "Guinea and Australia share deep bilateral ties, and Australia is the primary "
        "destination for Papua New Guinean nationals travelling abroad. Direct flights "
        "connect Port Moresby to Brisbane, Sydney, and Cairns. The Australian High "
        "Commission in Port Moresby handles consular matters."
    ),
    ('ukraine', 'australia'): (
        "Ukrainian nationals have migrated to Australia in three main waves: post-World War II, "
        "post-independence in the 1990s, and following the 2022 Russian invasion of Ukraine. "
        "Australia has received significant numbers of Ukrainian refugees since February 2022. "
        "The established Ukrainian-Australian community in Melbourne, Sydney, and Adelaide "
        "means this corridor sees consistent demand. The Australian Embassy in Kyiv handles "
        "consular matters where accessible. (DFAT, Australian Government, 2025.)"
    ),
    # R30: Qatar wave 3
    ('vietnam', 'qatar'): (
        "Vietnamese nationals work in Qatar in construction, manufacturing, and engineering, "
        "recruited under Vietnam's overseas labour programme. Vietnam and Qatar have bilateral "
        "labour agreements. The Qatar Embassy in Hanoi handles document attestation. "
        "Vietnamese documentation requires certified Arabic translation. This corridor handles "
        "cases where a Qatar-based Vietnamese worker has a family member die in Vietnam and "
        "needs remains brought to Qatar."
    ),
    ('china', 'qatar'): (
        "Chinese nationals form a significant workforce community in Qatar, particularly "
        "in construction projects built for Qatar's development programme. Qatar and China "
        "have strong bilateral commercial ties, and Chinese companies have been active in "
        "Qatar's construction and technology sectors. The Qatar Embassy in Beijing handles "
        "document attestation requirements. Chinese documentation requires certified Arabic "
        "translation."
    ),
    ('iran', 'qatar'): (
        "Iranian nationals form one of Qatar's significant non-Arab expatriate communities. "
        "Qatar and Iran share the world's largest natural gas field (North Dome on the "
        "Qatari side, South Pars on the Iranian side) and have maintained close bilateral "
        "ties. The Qatar Embassy in Tehran handles document attestation. Arabic and Persian "
        "documentation are both relevant on this corridor. This is a well-established "
        "commercial and family connection route."
    ),
    ('morocco', 'qatar'): (
        "Moroccan nationals form part of Qatar's Arab professional and worker community. "
        "Morocco and Qatar have close bilateral relations within the Arab League framework. "
        "Arabic is the working language on both sides of this corridor, which simplifies "
        "documentation requirements compared to non-Arabic routes. The Qatar Embassy in "
        "Rabat handles document attestation."
    ),
    ('somalia', 'qatar'): (
        "Somali nationals work in Qatar in commercial and service roles. This corridor "
        "requires specialist coordination given Somalia's limited civil registration "
        "infrastructure. Qatar maintains a mission in Mogadishu to handle consular and "
        "document attestation requirements. All documents must be attested by the Qatar "
        "Embassy in the origin country before the body can depart. "
        "(Qatar Ministry of Foreign Affairs, 2025.)"
    ),
    # R30: Kuwait wave 3
    ('jordan', 'kuwait'): (
        "Jordanian nationals have historically been one of Kuwait's largest Arab worker "
        "communities, with significant numbers in Kuwait City working in professional and "
        "service roles. Kuwait and Jordan have close bilateral ties within the Arab world. "
        "Arabic is the working language on both sides, simplifying documentation "
        "requirements. The Kuwait Embassy in Amman handles document attestation."
    ),
    ('malaysia', 'kuwait'): (
        "Malaysian nationals work in Kuwait in professional and service sectors. Malaysia "
        "and Kuwait have close bilateral ties through the Organisation of Islamic Cooperation "
        "(OIC) framework. The Kuwait Embassy in Kuala Lumpur handles document attestation. "
        "Malay documentation from Malaysia requires certified Arabic translation for "
        "Kuwaiti authorities."
    ),
    ('china', 'kuwait'): (
        "Chinese nationals work in Kuwait in construction, engineering, and infrastructure "
        "projects as part of bilateral agreements between China and Kuwait. Kuwait is a "
        "participant in China's Belt and Road Initiative engagement in the Gulf. The Kuwait "
        "Embassy in Beijing handles document attestation. Chinese documentation requires "
        "certified Arabic translation."
    ),
    ('turkey', 'kuwait'): (
        "Turkish nationals work in Kuwait in construction, engineering, and professional "
        "services. Turkish contractors have long operated in Gulf states. The Kuwait Embassy "
        "in Ankara handles document attestation requirements. Turkish documentation requires "
        "certified Arabic translation for Kuwaiti authorities. This corridor handles cases "
        "where a Kuwait-based Turkish national has a family member die in Turkey."
    ),
    ('iran', 'kuwait'): (
        "Iranian nationals form part of Kuwait's Shia community, and Kuwait and Iran share "
        "a maritime border. Commercial ties between the two countries remain active. The "
        "Kuwait Embassy in Tehran handles document attestation. Arabic and Persian are both "
        "relevant on this corridor. This corridor handles cases where a Kuwait-based "
        "Iranian has a family member die in Iran."
    ),
    # R30: Singapore wave 3
    ('japan', 'singapore'): (
        "Japanese nationals live in Singapore in significant numbers, working in finance, "
        "technology, and trading companies. Japan and Singapore have one of Asia's closest "
        "bilateral economic relationships, and the Japanese community in Singapore is large "
        "and well established. Japanese documentation is precise and well-recognised by "
        "Singapore authorities. The Singapore Embassy in Tokyo handles consular matters. "
        "This is one of Singapore's most professionally managed repatriation corridors."
    ),
    ('nepal', 'singapore'): (
        "Nepali nationals work in Singapore in construction, healthcare, and domestic "
        "services. Singapore receives a significant number of Nepali workers each year "
        "under work pass schemes, and the Nepali community in Singapore is well established. "
        "The Singapore High Commission in Kathmandu handles consular matters. Nepali "
        "documentation requires certified English translation for Singapore authorities."
    ),
    ('cambodia', 'singapore'): (
        "Cambodian nationals work in Singapore in construction and manufacturing, and "
        "Cambodia is an ASEAN member with close economic ties to Singapore. Singapore is "
        "a major investor in Cambodia. The Singapore Embassy in Phnom Penh handles "
        "consular matters. Khmer documentation from Cambodia requires certified English "
        "translation for Singapore Customs."
    ),
    ('hong-kong', 'singapore'): (
        "Hong Kong residents travel frequently to and from Singapore for business and "
        "family reasons. Singapore and Hong Kong are Asia's two leading international "
        "financial centres and have strong bilateral ties. This corridor handles cases "
        "where a Singapore-based person has a family member die in Hong Kong and needs "
        "remains brought to Singapore. The Singapore Consulate-General in Hong Kong "
        "handles consular matters."
    ),
    ('laos', 'singapore'): (
        "Lao nationals work in Singapore in hospitality, construction, and services. "
        "Laos is an ASEAN member with developing trade ties to Singapore. Singapore is "
        "a significant investor in Laos. The Singapore Embassy in Vientiane handles "
        "consular matters. Lao documentation requires certified English translation for "
        "Singapore Customs. This corridor handles cases where a Singapore-based Lao "
        "national has a family member die in Laos."
    ),
    # R30: South Africa wave 3
    ('somalia', 'south-africa'): (
        "Somali nationals form a significant refugee and migrant community in South Africa, "
        "concentrated in Johannesburg and Cape Town. South Africa has received Somali asylum "
        "seekers since the 1990s. This corridor requires specialist coordination given "
        "Somalia's limited civil registration infrastructure. South Africa's consular "
        "coverage for Somalia operates primarily from Nairobi, Kenya. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('rwanda', 'south-africa'): (
        "Rwandan nationals form part of South Africa's East African diaspora. South Africa "
        "and Rwanda have developed strong bilateral trade and people-to-people ties since "
        "the early 2000s. The South African High Commission in Kigali handles consular "
        "matters. Kinyarwanda documentation from Rwanda requires certified English "
        "translation for South African authorities."
    ),
    ('burundi', 'south-africa'): (
        "Burundian nationals have sought refuge in South Africa in significant numbers, "
        "with communities in Johannesburg and Cape Town. Burundi and South Africa maintain "
        "diplomatic relations. The South African High Commission in Bujumbura handles "
        "consular matters. French and Kirundi documentation from Burundi requires certified "
        "English translation for South African authorities."
    ),
    ('eritrea', 'south-africa'): (
        "Eritrean nationals form part of South Africa's East African diaspora, concentrated "
        "in Johannesburg. South Africa received Eritrean asylum seekers during the 2000s "
        "and 2010s. The South African Embassy in Asmara handles consular matters. Tigrinya "
        "documentation from Eritrea requires certified English translation for South "
        "African authorities."
    ),
    ('ivory-coast', 'south-africa'): (
        "Ivorian nationals form part of South Africa's West African diaspora. South Africa "
        "and Ivory Coast maintain diplomatic and commercial ties. The South African Embassy "
        "in Abidjan handles consular matters. French documentation from Ivory Coast requires "
        "certified English translation for South African authorities. This corridor sees "
        "demand from the Ivorian professional and student community in South Africa."
    ),
    # R30: USA wave 4
    ('russia', 'united-states'): (
        "Russian nationals and Russian-Americans form a significant diaspora community in "
        "the United States, concentrated in New York, Los Angeles, Chicago, and Miami. "
        "Following the 2022 invasion of Ukraine, US-Russia diplomatic relations deteriorated "
        "significantly, with both countries reducing embassy staffing. The US Embassy in "
        "Moscow continues to operate at a reduced capacity. Specialist coordination is "
        "strongly recommended. Russian documentation requires certified English translation. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('lebanon', 'united-states'): (
        "Lebanese nationals and Lebanese-Americans form one of the United States' most "
        "established Arab diaspora communities, with over 400,000 Lebanon-born residents "
        "and a significantly larger Lebanese-heritage population. The US Embassy in Beirut "
        "is one of the region's primary consular missions. Lebanon to USA is an established "
        "corridor with consistent demand. Arabic documentation from Lebanon requires "
        "certified English translation."
    ),
    ('eritrea', 'united-states'): (
        "Eritrean nationals form a growing East African diaspora community in the United "
        "States, concentrated in Washington DC, Oakland, Atlanta, and other cities. The "
        "US Embassy in Asmara handles consular matters. Tigrinya documentation from "
        "Eritrea requires certified English translation. Eritrea's civil registration "
        "capacity is limited in some areas, which can extend documentation processing "
        "on this corridor."
    ),
    ('iraq', 'united-states'): (
        "Iraqi nationals form a significant Middle Eastern community in the United States, "
        "with over 500,000 Iraq-born residents concentrated in Detroit, Nashville, San Diego, "
        "and Chicago. The US Embassy in Baghdad handles consular matters. Arabic documentation "
        "from Iraq requires certified English translation. Cases originating from "
        "disputed or conflict-affected areas may require additional specialist support. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('syria', 'united-states'): (
        "Syrian nationals and Syrian-Americans form a growing diaspora community in the "
        "United States following the Syrian civil war from 2011 onward. The US Embassy in "
        "Damascus closed in 2012; consular services for Syria are provided from the US "
        "Embassy in Beirut, Lebanon. Specialist coordination is recommended given the "
        "complex civil registration situation in different control areas of Syria. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    # R31: Switzerland wave 3
    ('egypt', 'switzerland'): (
        "Egyptian nationals form part of Switzerland's Middle Eastern diaspora, working in "
        "professional and academic roles. The Swiss Embassy in Cairo handles consular matters. "
        "Arabic documentation from Egypt requires certified German or French translation for "
        "Swiss authorities. Egypt's civil registration system issues the official death "
        "certificate through the Civil Registration Authority."
    ),
    ('chile', 'switzerland'): (
        "Chilean nationals form a historically established community in Switzerland, including "
        "political refugees and their descendants who arrived in the 1970s, and subsequent "
        "economic migrants. Switzerland and Chile maintain bilateral ties. Spanish "
        "documentation from Chile requires certified German or French translation for Swiss "
        "authorities. The Swiss Embassy in Santiago handles consular matters."
    ),
    ('colombia', 'switzerland'): (
        "Colombian nationals form a small Latin American community in Switzerland, working "
        "in professional and service roles in Geneva and Zurich, including in international "
        "organisations headquartered in Geneva. Spanish documentation from Colombia requires "
        "certified German or French translation for Swiss authorities. The Swiss Embassy in "
        "Bogota handles consular matters."
    ),
    ('brazil', 'switzerland'): (
        "Brazilian nationals form part of Switzerland's Latin American diaspora, working "
        "in finance, hospitality, and international organisations in Geneva and Zurich. "
        "Portugal-language documentation from Brazil requires certified German or French "
        "translation for Swiss authorities. The Swiss Embassy in Brasilia handles consular "
        "matters. This corridor handles cases where a Switzerland-based Brazilian has a "
        "family member die in Brazil."
    ),
    ('china', 'switzerland'): (
        "Chinese nationals form a growing business and academic community in Switzerland, "
        "concentrated in Basel and Zurich, working in pharmaceutical research, finance, "
        "and technology. Switzerland and China have a bilateral Free Trade Agreement, "
        "making them close economic partners. Chinese documentation requires certified "
        "German or French translation. The Swiss Embassy in Beijing handles consular matters."
    ),
    # R31: Sweden wave 3
    ('nigeria', 'sweden'): (
        "Nigerian nationals form part of Sweden's African diaspora, with a community in "
        "Stockholm and Gothenburg working in professional, academic, and service roles. "
        "English documentation from Nigeria simplifies some requirements where English is "
        "accepted alongside Swedish. The Swedish Embassy in Abuja handles consular matters. "
        "This corridor handles cases where a Sweden-based Nigerian has a family member die "
        "in Nigeria."
    ),
    ('kenya', 'sweden'): (
        "Kenyan nationals form a small but established East African community in Sweden, "
        "working in professional and academic sectors. This corridor handles cases where "
        "a Sweden-based Kenyan has a family member die in Kenya and needs remains brought "
        "to Sweden. English documentation from Kenya simplifies some requirements. The "
        "Swedish Embassy in Nairobi handles consular matters."
    ),
    ('morocco', 'sweden'): (
        "Moroccan nationals form part of Sweden's North African diaspora, with a community "
        "in Stockholm and other Swedish cities. Arabic documentation from Morocco requires "
        "certified Swedish translation for Swedish authorities. The Swedish Embassy in Rabat "
        "handles consular matters. This corridor handles cases where a Sweden-based Moroccan "
        "has a family member die in Morocco."
    ),
    ('tunisia', 'sweden'): (
        "Tunisian nationals form part of Sweden's North African diaspora. This corridor "
        "handles cases where a Sweden-based Tunisian has a family member die in Tunisia "
        "and needs remains brought to Sweden. Arabic documentation from Tunisia requires "
        "certified Swedish translation. The Swedish Embassy in Tunis handles consular "
        "matters."
    ),
    ('china', 'sweden'): (
        "Chinese nationals form a growing academic and business community in Sweden, "
        "particularly in Stockholm and Gothenburg, working in technology and life sciences "
        "at major Swedish universities and companies. Chinese documentation requires "
        "certified Swedish translation for Swedish authorities. The Swedish Embassy in "
        "Beijing handles consular matters."
    ),
    # R31: Norway wave 3
    ('nigeria', 'norway'): (
        "Nigerian nationals form part of Norway's African diaspora, with a community "
        "concentrated in Oslo. This corridor handles cases where a Norway-based Nigerian "
        "has a family member die in Nigeria and needs remains brought to Norway. English "
        "documentation from Nigeria simplifies some requirements. The Norwegian Embassy in "
        "Abuja handles consular matters."
    ),
    ('kenya', 'norway'): (
        "Kenyan nationals form part of Norway's East African diaspora, working in "
        "professional and healthcare sectors. This corridor handles cases where a "
        "Norway-based Kenyan has a family member die in Kenya and needs remains brought "
        "to Norway. English documentation from Kenya simplifies some requirements. The "
        "Norwegian Embassy in Nairobi handles consular matters."
    ),
    ('morocco', 'norway'): (
        "Moroccan nationals form part of Norway's North African diaspora, with a community "
        "in Oslo and other Norwegian cities. This corridor handles cases where a "
        "Norway-based Moroccan has a family member die in Morocco and needs remains brought "
        "to Norway. Arabic documentation requires certified Norwegian translation. The "
        "Norwegian Embassy in Rabat handles consular matters."
    ),
    ('turkey', 'norway'): (
        "Turkish nationals form part of Norway's labour migration community, reflecting the "
        "broader Turkish diaspora in Northern Europe. Turkey to Norway is an established "
        "corridor. Turkish Airlines operates regular services between Istanbul and Oslo. "
        "Turkish documentation requires certified Norwegian translation. The Norwegian "
        "Embassy in Ankara handles consular matters."
    ),
    ('china', 'norway'): (
        "Chinese nationals form a growing academic and business community in Norway, "
        "concentrated in Oslo and Bergen, working in technology, maritime, and energy "
        "sectors. The Norwegian Embassy in Beijing handles consular matters. Chinese "
        "documentation requires certified Norwegian translation for Norwegian authorities."
    ),
    # R31: Portugal wave 3
    ('morocco', 'portugal'): (
        "Moroccan nationals form a significant immigrant community in Portugal, with tens "
        "of thousands of residents working in construction, agriculture, and services. "
        "Morocco and Portugal share proximity across the Strait of Gibraltar and have "
        "active commercial ties. Arabic documentation from Morocco requires certified "
        "Portuguese translation. The Portuguese Embassy in Rabat handles consular matters."
    ),
    ('guinea', 'portugal'): (
        "Guinean nationals form part of Portugal's African diaspora. Guinea uses French "
        "as its official language, though there are community and historical ties with "
        "Portugal. French documentation from Guinea requires certified Portuguese "
        "translation. The Portuguese Embassy in Conakry handles consular matters. This "
        "corridor handles cases where a Portugal-based Guinean has a family member die "
        "in Guinea."
    ),
    ('senegal', 'portugal'): (
        "Senegalese nationals form part of Portugal's African diaspora, with a community "
        "working in services and trade. French documentation from Senegal requires "
        "certified Portuguese translation for Portuguese civil registry purposes. The "
        "Portuguese Embassy in Dakar handles consular matters. This corridor handles "
        "cases where a Portugal-based Senegalese has a family member die in Senegal."
    ),
    ('nigeria', 'portugal'): (
        "Nigerian nationals form a growing community in Portugal, concentrated in Lisbon. "
        "Portugal has seen increased Nigerian immigration in recent years. English "
        "documentation from Nigeria simplifies some requirements where English is accepted. "
        "The Portuguese Embassy in Abuja handles consular matters. This corridor handles "
        "cases where a Portugal-based Nigerian has a family member die in Nigeria."
    ),
    ('turkey', 'portugal'): (
        "Turkish nationals form a small but established community in Portugal, working in "
        "business and the tourism sector, particularly in Lisbon and the Algarve. Turkish "
        "Airlines operates regular services between Istanbul and Lisbon. Turkish "
        "documentation requires certified Portuguese translation. The Portuguese Embassy "
        "in Ankara handles consular matters."
    ),
    # R31: Saudi Arabia wave 3
    ('malaysia', 'saudi-arabia'): (
        "Malaysian nationals form a significant South-East Asian workforce community in "
        "Saudi Arabia, working in construction, healthcare, and engineering. Malaysia and "
        "Saudi Arabia have close bilateral ties through the Organisation of Islamic "
        "Cooperation (OIC) framework. Malay documentation requires certified Arabic "
        "translation. The Saudi Embassy in Kuala Lumpur handles document authentication."
    ),
    ('vietnam', 'saudi-arabia'): (
        "Vietnamese nationals work in Saudi Arabia in construction and manufacturing, "
        "recruited under Vietnam's overseas labour programme. Vietnam and Saudi Arabia "
        "have bilateral labour agreements. The Saudi Embassy in Hanoi handles document "
        "authentication. Vietnamese documentation requires certified Arabic translation. "
        "This is a growing corridor reflecting Vietnam's expanding overseas labour programme."
    ),
    ('china', 'saudi-arabia'): (
        "Chinese nationals work in Saudi Arabia in construction, engineering, and technology "
        "sectors. China and Saudi Arabia have deepened bilateral ties through Vision 2030 "
        "cooperation and Belt and Road Initiative engagement in the Gulf. The Saudi Embassy "
        "in Beijing handles document authentication. Chinese documentation requires "
        "certified Arabic translation."
    ),
    ('eritrea', 'saudi-arabia'): (
        "Eritrean nationals work in Saudi Arabia in domestic and construction sectors. "
        "The Saudi Embassy in Asmara handles document authentication requirements. Tigrinya "
        "documentation from Eritrea requires certified Arabic translation. All documents "
        "must be authenticated by the Saudi Embassy in Asmara before the body can be "
        "received in Saudi Arabia. Specialist coordination is recommended."
    ),
    ('iran', 'saudi-arabia'): (
        "Iran and Saudi Arabia restored diplomatic relations in March 2023 after a "
        "seven-year break, with the Saudi Embassy in Tehran reopening following the "
        "normalisation agreement brokered by China. Iranian nationals can now access Saudi "
        "consular services through the Saudi Embassy in Tehran. This is a sensitive corridor "
        "that benefits from specialist coordination. All documentation must be authenticated "
        "by the Saudi Embassy in Tehran. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    # R32: Japan corridors
    ('china', 'japan'): (
        "Chinese nationals form Japan's largest foreign resident community, with over "
        "800,000 residents working in manufacturing, services, and professional sectors, "
        "or studying at Japanese universities. China to Japan is one of Asia's "
        "highest-volume repatriation corridors. Chinese documentation requires certified "
        "Japanese translation for koseki registration. The Japanese Embassy in Beijing "
        "handles consular matters. (Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    ('south-korea', 'japan'): (
        "South Korean nationals form Japan's second-largest foreign resident community, "
        "with close to 500,000 residents including both recent arrivals and long-settled "
        "Zainichi Korean families. The two countries share complex historical ties and an "
        "active modern relationship with strong people-to-people links. Korea to Japan is "
        "one of Asia's most active bilateral repatriation corridors. Korean documentation "
        "requires certified Japanese translation."
    ),
    ('philippines', 'japan'): (
        "Filipino nationals form one of Japan's fastest-growing foreign communities, "
        "working in healthcare and nursing under Japan's Economic Partnership Agreement "
        "recruitment schemes, and in the service and entertainment sectors. The Japanese "
        "Embassy in Manila handles consular matters. Filipino documentation requires "
        "certified Japanese translation for Japanese authorities. The Philippine DFA "
        "authentication process adds to the documentation timeline."
    ),
    ('vietnam', 'japan'): (
        "Vietnamese nationals form Japan's third-largest foreign community, with over "
        "600,000 residents working in manufacturing and technical roles under Japan's "
        "Technical Intern Training Programme and Specified Skilled Worker schemes. Vietnam "
        "to Japan is one of Japan's busiest South-East Asian repatriation corridors. "
        "Vietnamese documentation requires certified Japanese translation. The Japanese "
        "Embassy in Hanoi handles consular matters."
    ),
    ('india', 'japan'): (
        "Indian nationals form a significant technology and business community in Japan, "
        "working in IT, consulting, and pharmaceutical sectors, particularly in Tokyo and "
        "Osaka. India-Japan bilateral agreements have strengthened people-to-people ties. "
        "The Japanese Embassy in New Delhi handles consular matters. Hindi and English "
        "documentation from India requires certified Japanese translation where required."
    ),
    ('myanmar', 'japan'): (
        "Myanmar nationals form a growing community in Japan, with workers in technical "
        "intern and skilled worker schemes across manufacturing sectors. This corridor has "
        "grown significantly since 2018 as Japanese employers recruited Myanmar nationals "
        "under bilateral agreements. The Japanese Embassy in Yangon handles consular "
        "matters. Burmese documentation requires certified Japanese translation."
    ),
    ('indonesia', 'japan'): (
        "Indonesian nationals work in Japan in healthcare, technical intern, and specialist "
        "roles under Japan's Economic Partnership Agreement with Indonesia. The Japanese "
        "Embassy in Jakarta handles consular matters. Indonesian documentation requires "
        "certified Japanese translation. Indonesia and Japan have maintained close "
        "bilateral ties for decades, and the Indonesian community in Japan is well "
        "established."
    ),
    ('brazil', 'japan'): (
        "Brazil hosts the world's largest Japanese diaspora outside Japan, with over "
        "1.5 million Nikkei (Japanese-Brazilian) residents. Some Nikkei Brazilians return "
        "to Japan to live and work, creating a reverse corridor. Japan to Japan repatriation "
        "via Brazil handles cases where Japanese-heritage Brazilians need remains returned "
        "to Japan. Portuguese documentation from Brazil requires certified Japanese "
        "translation. The Japanese Embassy in Brasilia handles consular matters."
    ),
    # R32: New Zealand corridors
    ('india', 'new-zealand'): (
        "Indian nationals form New Zealand's largest non-European immigrant community, "
        "with over 200,000 residents concentrated in Auckland. India to New Zealand is an "
        "established repatriation corridor. English documentation from India simplifies "
        "requirements for New Zealand Customs. The New Zealand High Commission in New Delhi "
        "handles consular matters. New Zealand has strong bilateral ties with India through "
        "trade and education links."
    ),
    ('china', 'new-zealand'): (
        "Chinese nationals form one of New Zealand's largest immigrant communities, with "
        "significant populations in Auckland and Wellington working in business, education, "
        "and professional sectors. China to New Zealand is an established repatriation "
        "corridor. Chinese documentation requires certified English translation for New "
        "Zealand Customs. The New Zealand Embassy in Beijing handles consular matters."
    ),
    ('philippines', 'new-zealand'): (
        "Filipino nationals form a significant community in New Zealand, working in "
        "healthcare, domestic care, and service roles. The New Zealand Embassy in Manila "
        "handles consular matters. Filipino documentation in English simplifies requirements "
        "for New Zealand Customs. The Philippine DFA authentication process is the primary "
        "documentation delay on this corridor."
    ),
    ('fiji', 'new-zealand'): (
        "Fijian nationals form one of New Zealand's most established Pacific Island "
        "communities, with New Zealand receiving Fijian emigrants since the 1970s. Fiji "
        "and New Zealand have close bilateral ties as Pacific neighbours. Direct flights "
        "connect Nadi to Auckland. English documentation from Fiji simplifies requirements "
        "for New Zealand Customs. The New Zealand High Commission in Suva handles "
        "consular matters."
    ),
    ('samoa', 'new-zealand'): (
        "Samoan nationals form New Zealand's largest Pacific Island community, with over "
        "200,000 Samoa-born and Samoan-heritage New Zealanders. Samoa and New Zealand have "
        "deep historical, social, and family ties. Direct flights connect Apia to Auckland. "
        "English and Samoan documentation from Samoa is well understood by New Zealand "
        "authorities. The New Zealand High Commission in Apia handles consular matters."
    ),
    ('tonga', 'new-zealand'): (
        "Tongan nationals form one of New Zealand's established Pacific Island communities, "
        "with over 70,000 Tongan-born and Tongan-heritage New Zealanders. Direct flights "
        "connect Nukualofa to Auckland. The New Zealand High Commission in Nukualofa handles "
        "consular matters. English and Tongan documentation is well understood by New Zealand "
        "authorities. This is one of New Zealand's most consistent Pacific repatriation "
        "corridors."
    ),
    ('south-africa', 'new-zealand'): (
        "South African nationals form an established anglophone migrant community in New "
        "Zealand, concentrated in Auckland and Wellington. Many South Africans emigrated "
        "to New Zealand from the late 1990s onward. English documentation from South Africa "
        "simplifies requirements for New Zealand Customs. The New Zealand High Commission "
        "in Pretoria handles consular matters."
    ),
    ('south-korea', 'new-zealand'): (
        "South Korean nationals form a significant East Asian community in New Zealand, "
        "particularly in Auckland, with a long-established Korean student and immigrant "
        "population. Korea to New Zealand is an established repatriation corridor. Korean "
        "documentation requires certified English translation for New Zealand authorities. "
        "The New Zealand Embassy in Seoul handles consular matters."
    ),
    # R32: Belgium wave 4
    ('france', 'belgium'): (
        "French nationals form one of Belgium's largest EU immigrant communities, "
        "concentrated in Brussels, Liege, and Namur. The two countries share borders and "
        "French is an official language in both. EU freedom of movement makes this a "
        "straightforward corridor. Direct rail and road links connect the two countries, "
        "and air cargo transits via Brussels Airport. The Belgian Embassy in Paris handles "
        "consular matters where required."
    ),
    ('kenya', 'belgium'): (
        "Kenyan nationals form part of Belgium's African diaspora, working in professional "
        "and service roles in Brussels and Antwerp. English documentation from Kenya "
        "simplifies some requirements where English is accepted alongside French or Dutch "
        "by Belgian authorities. The Belgian Embassy in Nairobi handles consular matters."
    ),
    ('eritrea', 'belgium'): (
        "Eritrean nationals form a growing community in Belgium, with significant numbers "
        "in Brussels and Ghent. Belgium received Eritrean asylum seekers during the 2010s. "
        "Eritrea's civil registration capacity requires specialist coordination. The "
        "Belgian Embassy in Asmara handles consular matters. Tigrinya documentation "
        "requires certified French or Dutch translation for Belgian authorities."
    ),
    ('burkina-faso', 'belgium'): (
        "Burkinabe nationals form part of Belgium's Francophone African diaspora, with "
        "historical connections through the Francophonie. French documentation from Burkina "
        "Faso simplifies some translation requirements for Belgian authorities where French "
        "is accepted. The Belgian Embassy in Ouagadougou handles consular matters. This "
        "corridor handles cases where a Belgium-based Burkinabe has a family member die "
        "in Burkina Faso."
    ),
    ('lebanon', 'belgium'): (
        "Lebanese nationals form part of Belgium's Middle Eastern diaspora, with a community "
        "in Brussels. Belgium and Lebanon have connections through the Francophonie and "
        "bilateral investment ties. Arabic and French documentation from Lebanon is relevant "
        "on this corridor. The Belgian Embassy in Beirut handles consular matters."
    ),
    # R32: Germany wave 5
    ('ivory-coast', 'germany'): (
        "Ivorian nationals form part of Germany's West African diaspora, working in "
        "academic, healthcare, and service roles across Berlin, Frankfurt, and Hamburg. "
        "French documentation from Ivory Coast requires certified German translation. The "
        "German Embassy in Abidjan handles consular matters. This corridor handles cases "
        "where a Germany-based Ivorian has a family member die in Ivory Coast."
    ),
    ('mali', 'germany'): (
        "Malian nationals form part of Germany's West African diaspora, with a growing "
        "community in Berlin and other German cities. Germany has received Malian migrants "
        "through skilled worker and asylum channels. French documentation from Mali requires "
        "certified German translation. The German Embassy in Bamako handles consular matters."
    ),
    ('togo', 'germany'): (
        "Togolese nationals form part of Germany's West African diaspora, and Germany and "
        "Togo have historical ties dating to the German colonial period in Togo (then "
        "Togoland) from 1884 to 1914. French documentation from Togo requires certified "
        "German translation. The German Embassy in Lome handles consular matters. This "
        "corridor handles cases where a Germany-based Togolese has a family member die "
        "in Togo."
    ),
    ('guinea', 'germany'): (
        "Guinean nationals form part of Germany's West African diaspora. Germany has "
        "received Guinean migrants through humanitarian and skills channels. French "
        "documentation from Guinea requires certified German translation. The German "
        "Embassy in Conakry handles consular matters. This corridor handles cases where "
        "a Germany-based Guinean has a family member die in Guinea."
    ),
    ('somalia', 'germany'): (
        "Somali nationals form a significant East African community in Germany, with over "
        "40,000 residents concentrated in Hamburg, Munich, and Berlin. Germany received "
        "Somali asylum seekers in significant numbers during the 2010s. This corridor "
        "requires specialist coordination given Somalia's limited civil registration "
        "capacity. German consular services for Somalia are provided from the German "
        "Embassy in Nairobi, Kenya. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
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
    uk_embassy_city = get_field(uk_fm, 'embassy_city')

    dest_embassy_city = EMBASSY_CITIES.get(
        (origin_slug, dest_slug), uk_embassy_city or 'the capital'
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
    - url: "/repatriation-from-{dest_slug_str}/"
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
    content = content.replace('—', ',')
    content = content.replace('–', ',')
    content = content.replace('\x96', ',')
    content = content.replace('\x97', ',')
    content = content.replace('---', '\x00TRIPLE\x00')
    content = content.replace('--', ',')
    content = content.replace('\x00TRIPLE\x00', '---')
    return content


# ---------------------------------------------------------------------------
# Route list: R29 (25) + R30 (25) + R31 (25) + R32 (25) = 100 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R29: Germany wave 4 x5 + France wave 4 x5 + UAE wave 4 x5 +
    #     Canada wave 4 x5 + Australia wave 4 x5 = 25
    ('syria',             'germany'),
    ('lebanon',           'germany'),
    ('jordan',            'germany'),
    ('indonesia',         'germany'),
    ('philippines',       'germany'),
    ('ghana',             'france'),
    ('lebanon',           'france'),
    ('pakistan',          'france'),
    ('india',             'france'),
    ('bangladesh',        'france'),
    ('iran',              'united-arab-emirates'),
    ('lebanon',           'united-arab-emirates'),
    ('oman',              'united-arab-emirates'),
    ('eritrea',           'united-arab-emirates'),
    ('sudan',             'united-arab-emirates'),
    ('colombia',          'canada'),
    ('ecuador',           'canada'),
    ('peru',              'canada'),
    ('brazil',            'canada'),
    ('haiti',             'canada'),
    ('japan',             'australia'),
    ('south-africa',      'australia'),
    ('tonga',             'australia'),
    ('papua-new-guinea',  'australia'),
    ('ukraine',           'australia'),
    # --- Block R30: Qatar wave 3 x5 + Kuwait wave 3 x5 + Singapore wave 3 x5 +
    #     South Africa wave 3 x5 + USA wave 4 x5 = 25
    ('vietnam',           'qatar'),
    ('china',             'qatar'),
    ('iran',              'qatar'),
    ('morocco',           'qatar'),
    ('somalia',           'qatar'),
    ('jordan',            'kuwait'),
    ('malaysia',          'kuwait'),
    ('china',             'kuwait'),
    ('turkey',            'kuwait'),
    ('iran',              'kuwait'),
    ('japan',             'singapore'),
    ('nepal',             'singapore'),
    ('cambodia',          'singapore'),
    ('hong-kong',         'singapore'),
    ('laos',              'singapore'),
    ('somalia',           'south-africa'),
    ('rwanda',            'south-africa'),
    ('burundi',           'south-africa'),
    ('eritrea',           'south-africa'),
    ('ivory-coast',       'south-africa'),
    ('russia',            'united-states'),
    ('lebanon',           'united-states'),
    ('eritrea',           'united-states'),
    ('iraq',              'united-states'),
    ('syria',             'united-states'),
    # --- Block R31: Switzerland wave 3 x5 + Sweden wave 3 x5 + Norway wave 3 x5 +
    #     Portugal wave 3 x5 + Saudi Arabia wave 3 x5 = 25
    ('egypt',             'switzerland'),
    ('chile',             'switzerland'),
    ('colombia',          'switzerland'),
    ('brazil',            'switzerland'),
    ('china',             'switzerland'),
    ('nigeria',           'sweden'),
    ('kenya',             'sweden'),
    ('morocco',           'sweden'),
    ('tunisia',           'sweden'),
    ('china',             'sweden'),
    ('nigeria',           'norway'),
    ('kenya',             'norway'),
    ('morocco',           'norway'),
    ('turkey',            'norway'),
    ('china',             'norway'),
    ('morocco',           'portugal'),
    ('guinea',            'portugal'),
    ('senegal',           'portugal'),
    ('nigeria',           'portugal'),
    ('turkey',            'portugal'),
    ('malaysia',          'saudi-arabia'),
    ('vietnam',           'saudi-arabia'),
    ('china',             'saudi-arabia'),
    ('eritrea',           'saudi-arabia'),
    ('iran',              'saudi-arabia'),
    # --- Block R32: Japan (new hub) x8 + New Zealand (new hub) x7 +
    #     Belgium wave 4 x5 + Germany wave 5 x5 = 25
    ('china',             'japan'),
    ('south-korea',       'japan'),
    ('philippines',       'japan'),
    ('vietnam',           'japan'),
    ('india',             'japan'),
    ('myanmar',           'japan'),
    ('indonesia',         'japan'),
    ('brazil',            'japan'),
    ('india',             'new-zealand'),
    ('china',             'new-zealand'),
    ('philippines',       'new-zealand'),
    ('fiji',              'new-zealand'),
    ('samoa',             'new-zealand'),
    ('tonga',             'new-zealand'),
    ('south-korea',       'new-zealand'),
    ('france',            'belgium'),
    ('kenya',             'belgium'),
    ('eritrea',           'belgium'),
    ('burkina-faso',      'belgium'),
    ('lebanon',           'belgium'),
    ('ivory-coast',       'germany'),
    ('mali',              'germany'),
    ('togo',              'germany'),
    ('guinea',            'germany'),
    ('somalia',           'germany'),
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
    print(f"  OK [{variant}]: {slug}")
    variant_idx += 1

print(f"\n--- GENERATION SUMMARY ---")
print(f"Generated: {len(generated)}")
print(f"Skipped:   {len(skipped)}")
print(f"Errors:    {len(errors)}")
if errors:
    print(f"ERROR LIST: {errors}")

# Block breakdown
R29_SLUGS = {
    'syria-to-germany', 'lebanon-to-germany', 'jordan-to-germany',
    'indonesia-to-germany', 'philippines-to-germany',
    'ghana-to-france', 'lebanon-to-france', 'pakistan-to-france',
    'india-to-france', 'bangladesh-to-france',
    'iran-to-united-arab-emirates', 'lebanon-to-united-arab-emirates',
    'oman-to-united-arab-emirates', 'eritrea-to-united-arab-emirates',
    'sudan-to-united-arab-emirates',
    'colombia-to-canada', 'ecuador-to-canada', 'peru-to-canada',
    'brazil-to-canada', 'haiti-to-canada',
    'japan-to-australia', 'south-africa-to-australia',
    'tonga-to-australia', 'papua-new-guinea-to-australia', 'ukraine-to-australia',
}
R30_SLUGS = {
    'vietnam-to-qatar', 'china-to-qatar', 'iran-to-qatar',
    'morocco-to-qatar', 'somalia-to-qatar',
    'jordan-to-kuwait', 'malaysia-to-kuwait', 'china-to-kuwait',
    'turkey-to-kuwait', 'iran-to-kuwait',
    'japan-to-singapore', 'nepal-to-singapore', 'cambodia-to-singapore',
    'hong-kong-to-singapore', 'laos-to-singapore',
    'somalia-to-south-africa', 'rwanda-to-south-africa', 'burundi-to-south-africa',
    'eritrea-to-south-africa', 'ivory-coast-to-south-africa',
    'russia-to-united-states', 'lebanon-to-united-states', 'eritrea-to-united-states',
    'iraq-to-united-states', 'syria-to-united-states',
}
R31_SLUGS = {
    'egypt-to-switzerland', 'chile-to-switzerland', 'colombia-to-switzerland',
    'brazil-to-switzerland', 'china-to-switzerland',
    'nigeria-to-sweden', 'kenya-to-sweden', 'morocco-to-sweden',
    'tunisia-to-sweden', 'china-to-sweden',
    'nigeria-to-norway', 'kenya-to-norway', 'morocco-to-norway',
    'turkey-to-norway', 'china-to-norway',
    'morocco-to-portugal', 'guinea-to-portugal', 'senegal-to-portugal',
    'nigeria-to-portugal', 'turkey-to-portugal',
    'malaysia-to-saudi-arabia', 'vietnam-to-saudi-arabia', 'china-to-saudi-arabia',
    'eritrea-to-saudi-arabia', 'iran-to-saudi-arabia',
}
R32_SLUGS = {
    'china-to-japan', 'south-korea-to-japan', 'philippines-to-japan',
    'vietnam-to-japan', 'india-to-japan', 'myanmar-to-japan',
    'indonesia-to-japan', 'brazil-to-japan',
    'india-to-new-zealand', 'china-to-new-zealand', 'philippines-to-new-zealand',
    'fiji-to-new-zealand', 'samoa-to-new-zealand', 'tonga-to-new-zealand',
    'south-korea-to-new-zealand',
    'france-to-belgium', 'kenya-to-belgium', 'eritrea-to-belgium',
    'burkina-faso-to-belgium', 'lebanon-to-belgium',
    'ivory-coast-to-germany', 'mali-to-germany', 'togo-to-germany',
    'guinea-to-germany', 'somalia-to-germany',
}

print(f"\n--- BLOCK BREAKDOWN ---")
for block_name, block_slugs in [
    ('R29', R29_SLUGS), ('R30', R30_SLUGS), ('R31', R31_SLUGS), ('R32', R32_SLUGS)
]:
    block_routes = [r for r in generated if r[0] in block_slugs]
    if block_routes:
        variants_used = ','.join(sorted(set(v for _, v in block_routes)))
        print(f"  {block_name}: {len(block_routes)} routes generated, variants {variants_used}")

total_in_all = len(generated) + len(skipped)
last_v = VARIANTS[(START_VARIANT + total_in_all - 1) % 5]
next_v = VARIANTS[(START_VARIANT + total_in_all) % 5]
print(f"\nLast variant used: {last_v}")
print(f"Next chunk should start at: {next_v}")
