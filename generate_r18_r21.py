#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R18-R21.
   R18: Qatar (10) + Kuwait (8) + Singapore (7) = 25
   R19: South Africa (15) + USA second wave (10) = 25
   R20: UAE second wave (8) + Germany second wave (8) + France second wave (9) = 25
   R21: Canada second wave (9) + Australia second wave (8) + India second wave (8) = 25
   Template rotation continues from R17 last variant C, so R18 starts at D (index 3).
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

# R17 ended on variant C (index 2). R18 starts at D (index 3).
START_VARIANT = 3

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
    'united-states': {
        'name': 'United States',
        'slug': 'united-states',
        'key': 'us',
        'reception': (
            "The US funeral director takes custody at the cargo terminal. "
            "US Customs clearance requires a transit or burial permit, the foreign death certificate, "
            "and an embalming certificate. State health department regulations apply and vary by state. "
            "The receiving funeral director notifies the medical examiner or coroner as required by state law. "
            "(US State Department, Bureau of Consular Affairs, 2025.)"
        ),
        'consular_template': (
            "US Embassy in {city} can assist US citizens and their families with consular registration "
            "of the death and provide a list of local funeral directors. They cannot pay for or arrange "
            "repatriation. State Department emergency line: +1 (888) 407-4747 (within the US) or "
            "+1 (202) 501-4444 (from overseas), 24 hours."
        ),
        'arrival_faq': (
            "The US funeral director takes custody at the cargo terminal. US Customs clearance requires "
            "the foreign death certificate, transit or burial permit, and embalming certificate. "
            "State regulations govern burial or cremation. The receiving funeral director notifies the "
            "medical examiner or coroner as required."
        ),
        'emergency_line': '+1 (202) 501-4444',
        'hub_url': 'repatriation-from-united-states',
    },
    'united-arab-emirates': {
        'name': 'United Arab Emirates',
        'slug': 'united-arab-emirates',
        'key': 'ae',
        'reception': (
            "The UAE funeral home or government mortuary takes custody at Dubai International (DXB) "
            "or Abu Dhabi International (AUH) cargo terminal. UAE Ministry of Health clearance is "
            "required before burial or cremation. All foreign documentation must be attested by the "
            "UAE Embassy in the country of origin and authenticated by UAE authorities. "
            "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
        ),
        'consular_template': (
            "UAE Embassy in {city} handles attestation of repatriation documents. Contact the "
            "UAE Embassy in {country_name} for document authentication requirements. "
            "UAE Ministry of Foreign Affairs and International Cooperation (MOFAIC) can be reached "
            "via the UAE Embassy during business hours."
        ),
        'arrival_faq': (
            "The UAE funeral home takes custody at Dubai (DXB) or Abu Dhabi (AUH) cargo terminal. "
            "UAE Ministry of Health clearance is required. All documents must be attested by the "
            "UAE Embassy in the country of origin. Islamic remains require certification for "
            "Islamic burial; non-Islamic remains follow separate procedures."
        ),
        'emergency_line': 'contact UAE Embassy in origin country',
        'hub_url': 'repatriation-from-united-arab-emirates',
    },
    'saudi-arabia': {
        'name': 'Saudi Arabia',
        'slug': 'saudi-arabia',
        'key': 'sa',
        'reception': (
            "The Saudi government mortuary or funeral home takes custody at King Khalid International "
            "(RUH, Riyadh), King Abdulaziz International (JED, Jeddah), or King Fahd International "
            "(DMM, Dammam) cargo terminal. Saudi Ministry of Health approval is required before the "
            "remains can be received. All documents must be authenticated by the Saudi Embassy in the "
            "country of origin. Non-Muslim remains require specific certification and procedures. "
            "(Saudi Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Saudi Embassy in {city} handles authentication of repatriation documents. "
            "Contact the Saudi Embassy in {country_name} for document legalisation requirements. "
            "Saudi Ministry of Foreign Affairs coordinates with the receiving authorities in Saudi Arabia."
        ),
        'arrival_faq': (
            "The Saudi government mortuary takes custody at the cargo terminal. "
            "Saudi Ministry of Health approval is required in advance. "
            "All documents must be authenticated by the Saudi Embassy in the origin country. "
            "Non-Muslim remains require specific certification. The family or sponsor arranges "
            "the receiving funeral home."
        ),
        'emergency_line': 'contact Saudi Embassy in origin country',
        'hub_url': 'repatriation-from-saudi-arabia',
    },
    'germany': {
        'name': 'Germany',
        'slug': 'germany',
        'key': 'de',
        'reception': (
            "The German funeral director takes custody at the cargo terminal, typically Frankfurt (FRA), "
            "Munich (MUC), or Berlin (BER). A Leichenpass (body transport passport) or equivalent "
            "laissez-passer must accompany the remains. The local Gesundheitsamt (public health authority) "
            "may inspect the remains on arrival. The receiving funeral director registers the death with "
            "the local Standesamt (civil registry) if required. "
            "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
        ),
        'consular_template': (
            "German Embassy in {city} can advise on document requirements for repatriation to Germany. "
            "Federal Foreign Office (Auswaertiges Amt) emergency assistance: +49 30 5000 2000 (24 hours). "
            "The German Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The German funeral director takes custody at the cargo terminal. "
            "A Leichenpass or laissez-passer must accompany the remains. "
            "The Gesundheitsamt may inspect the remains. "
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
            "The French funeral director (pompes funebres) takes custody at Charles de Gaulle (CDG, Paris) "
            "or another French international airport. The prefecture may require a permis d'inhumer "
            "(burial permit) or transport authorisation before burial or cremation can proceed. "
            "All foreign documents must carry a certified French translation. "
            "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
        ),
        'consular_template': (
            "French Embassy in {city} can advise on repatriation documentation requirements for France. "
            "French Ministry of Europe and Foreign Affairs (MAE) emergency assistance: "
            "+33 1 43 17 67 67 (24 hours). The French Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The French funeral director takes custody at Charles de Gaulle (CDG) or another French airport. "
            "The prefecture issues a permis d'inhumer before burial or cremation. "
            "All foreign documents require certified French translation. "
            "The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+33 1 43 17 67 67',
        'hub_url': 'repatriation-from-france',
    },
    'canada': {
        'name': 'Canada',
        'slug': 'canada',
        'key': 'ca',
        'reception': (
            "The Canadian funeral director takes custody at the cargo terminal. "
            "Canadian Border Services Agency (CBSA) clearance is required. "
            "The required documents are: the foreign death certificate, transit or burial permit, "
            "and embalming certificate. Provincial or territorial regulations apply and vary between "
            "Ontario, British Columbia, Quebec, Alberta, and other provinces. "
            "(Global Affairs Canada, 2025.)"
        ),
        'consular_template': (
            "Canadian Embassy or High Commission in {city} can assist Canadian citizens and their "
            "families with consular registration of the death and provide a list of local funeral directors. "
            "They cannot pay for or arrange repatriation. Global Affairs Canada emergency line: "
            "+1 (613) 996-8885 (24 hours, collect calls accepted)."
        ),
        'arrival_faq': (
            "The Canadian funeral director takes custody at the cargo terminal. "
            "CBSA clearance requires the foreign death certificate, transit or burial permit, "
            "and embalming certificate. Provincial regulations govern the burial or cremation. "
            "The receiving funeral director notifies the appropriate provincial authority."
        ),
        'emergency_line': '+1 (613) 996-8885',
        'hub_url': 'repatriation-from-canada',
    },
    'australia': {
        'name': 'Australia',
        'slug': 'australia',
        'key': 'au',
        'reception': (
            "The Australian funeral director takes custody at the cargo terminal. "
            "Australian Border Force clearance is required. "
            "The Australian Department of Health and Aged Care regulations apply. "
            "State or territory funeral regulations govern burial or cremation: requirements differ "
            "between New South Wales, Victoria, Queensland, Western Australia, South Australia, "
            "and the Northern Territory. All documentation must be authenticated. "
            "(Australian Government, Department of Foreign Affairs and Trade, DFAT, 2025.)"
        ),
        'consular_template': (
            "Australian Embassy or High Commission in {city} can assist Australian citizens and their "
            "families with consular registration of the death and provide a list of local funeral directors. "
            "They cannot pay for or arrange repatriation. Australian Government Consular Emergency Centre: "
            "+61 2 6261 3305 (24 hours)."
        ),
        'arrival_faq': (
            "The Australian funeral director takes custody at the cargo terminal. "
            "Australian Border Force clearance requires the foreign death certificate, transit permit, "
            "and embalming certificate. State or territory regulations govern burial or cremation. "
            "The receiving funeral director coordinates with the relevant state authority."
        ),
        'emergency_line': '+61 2 6261 3305',
        'hub_url': 'repatriation-from-australia',
    },
    'qatar': {
        'name': 'Qatar',
        'slug': 'qatar',
        'key': 'qa',
        'reception': (
            "The Qatari funeral home or government mortuary takes custody at Hamad International "
            "Airport (DOH) cargo terminal. Qatar Ministry of Public Health approval is required "
            "before the remains can be received. All documents must be attested by the Qatari "
            "Embassy in the country of origin. "
            "(Qatar Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Qatar Embassy in {city} handles attestation of repatriation documents. "
            "Contact the Qatar Embassy in {country_name} for document authentication requirements. "
            "Qatar Ministry of Foreign Affairs can be reached via the Qatar Embassy."
        ),
        'arrival_faq': (
            "The Qatari funeral home takes custody at Hamad International (DOH) cargo terminal. "
            "Qatar Ministry of Public Health clearance is required in advance. "
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
            "The Kuwaiti funeral home or government mortuary takes custody at Kuwait International "
            "Airport (KWI). Kuwait Ministry of Health clearance is required before the remains "
            "can be received. All documents must be attested by the Kuwaiti Embassy in the "
            "country of origin. "
            "(Kuwait Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Kuwait Embassy in {city} handles attestation of repatriation documents. "
            "Contact the Kuwait Embassy in {country_name} for document authentication requirements. "
            "Kuwait Ministry of Foreign Affairs coordinates with the receiving authorities."
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
            "The Singapore funeral director takes custody at Changi Airport (SIN) cargo terminal. "
            "Singapore Customs clearance is required. The National Environment Agency (NEA) "
            "regulates the import of human remains into Singapore. All foreign death certificates "
            "must be authenticated by the Singapore Embassy or High Commission in the country of origin. "
            "(Singapore Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Singapore High Commission or Embassy in {city} can advise on documentation "
            "requirements and authenticate foreign certificates. They cannot pay for or arrange "
            "repatriation. Singapore Ministry of Foreign Affairs 24-hour emergency: +65 6379 8000."
        ),
        'arrival_faq': (
            "The Singapore funeral director takes custody at Changi Airport (SIN) cargo terminal. "
            "Singapore Customs clearance requires the authenticated death certificate, transit permit, "
            "and embalming certificate. The National Environment Agency (NEA) regulates import of remains. "
            "All foreign documents must be authenticated by the Singapore Embassy in the origin country."
        ),
        'emergency_line': '+65 6379 8000',
        'hub_url': 'repatriation-from-singapore',
    },
    'south-africa': {
        'name': 'South Africa',
        'slug': 'south-africa',
        'key': 'za',
        'reception': (
            "The South African funeral director takes custody at the cargo terminal, typically "
            "O.R. Tambo International (JNB, Johannesburg), Cape Town International (CPT), "
            "or King Shaka International (DUR, Durban). A permit from the South African "
            "Department of Home Affairs (Form DHA-1744) is required before burial or cremation. "
            "The provincial health authority issues any additional permits. "
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
    'india': {
        'name': 'India',
        'slug': 'india',
        'key': 'in',
        'reception': (
            "The Indian funeral director takes custody at the cargo terminal. "
            "Custom House clearance is required. The remains must be embalmed and sealed in a "
            "zinc-lined coffin for international transport. State government regulations apply "
            "and may require a state-level permit. Major international entry points are Indira "
            "Gandhi International (DEL, Delhi), Chhatrapati Shivaji Maharaj (BOM, Mumbai), "
            "Chennai International (MAA), and Netaji Subhas Chandra Bose (CCU, Kolkata). "
            "(Indian Ministry of External Affairs, 2025.)"
        ),
        'consular_template': (
            "Indian Embassy or High Commission in {city} can assist with consular registration "
            "of the death and provide guidance on required documentation. They cannot pay for "
            "or arrange repatriation. Indian Ministry of External Affairs helpline: "
            "+91 11 2301 2113 (24 hours)."
        ),
        'arrival_faq': (
            "The Indian funeral director takes custody at the cargo terminal. "
            "Custom House clearance requires the foreign death certificate, embalming certificate, "
            "and transit permit. The remains must be in a zinc-lined sealed coffin. "
            "State regulations govern the release for burial or cremation at the destination."
        ),
        'emergency_line': '+91 11 2301 2113',
        'hub_url': 'repatriation-from-india',
    },
}

# ---------------------------------------------------------------------------
# Embassy cities for new corridors
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # Qatar corridors
    ('india', 'qatar'):       'New Delhi',
    ('pakistan', 'qatar'):    'Islamabad',
    ('bangladesh', 'qatar'):  'Dhaka',
    ('philippines', 'qatar'): 'Manila',
    ('nepal', 'qatar'):       'Kathmandu',
    ('egypt', 'qatar'):       'Cairo',
    ('sri-lanka', 'qatar'):   'Colombo',
    ('ethiopia', 'qatar'):    'Addis Ababa',
    ('indonesia', 'qatar'):   'Jakarta',
    ('kenya', 'qatar'):       'Nairobi',
    # Kuwait corridors
    ('india', 'kuwait'):      'New Delhi',
    ('pakistan', 'kuwait'):   'Islamabad',
    ('bangladesh', 'kuwait'): 'Dhaka',
    ('philippines', 'kuwait'): 'Manila',
    ('egypt', 'kuwait'):      'Cairo',
    ('sri-lanka', 'kuwait'):  'Colombo',
    ('nepal', 'kuwait'):      'Kathmandu',
    ('ethiopia', 'kuwait'):   'Addis Ababa',
    # Singapore corridors
    ('india', 'singapore'):       'New Delhi',
    ('china', 'singapore'):       'Beijing',
    ('malaysia', 'singapore'):    'Kuala Lumpur',
    ('philippines', 'singapore'): 'Manila',
    ('bangladesh', 'singapore'):  'Dhaka',
    ('indonesia', 'singapore'):   'Jakarta',
    ('myanmar', 'singapore'):     'Naypyidaw',
    # South Africa corridors
    ('zimbabwe', 'south-africa'):                       'Harare',
    ('mozambique', 'south-africa'):                     'Maputo',
    ('lesotho', 'south-africa'):                        'Maseru',
    ('malawi', 'south-africa'):                         'Lilongwe',
    ('zambia', 'south-africa'):                         'Lusaka',
    ('democratic-republic-of-the-congo', 'south-africa'): 'Kinshasa',
    ('tanzania', 'south-africa'):                       'Dar es Salaam',
    ('botswana', 'south-africa'):                       'Gaborone',
    ('namibia', 'south-africa'):                        'Windhoek',
    ('nigeria', 'south-africa'):                        'Abuja',
    ('ghana', 'south-africa'):                          'Accra',
    ('kenya', 'south-africa'):                          'Nairobi',
    ('ethiopia', 'south-africa'):                       'Addis Ababa',
    ('angola', 'south-africa'):                         'Luanda',
    ('cameroon', 'south-africa'):                       'Yaounde',
    # USA second wave
    ('bangladesh', 'united-states'):  'Dhaka',
    ('turkey', 'united-states'):      'Ankara',
    ('egypt', 'united-states'):       'Cairo',
    ('poland', 'united-states'):      'Warsaw',
    ('morocco', 'united-states'):     'Rabat',
    ('indonesia', 'united-states'):   'Jakarta',
    ('kenya', 'united-states'):       'Nairobi',
    ('senegal', 'united-states'):     'Dakar',
    ('laos', 'united-states'):        'Vientiane',
    ('ivory-coast', 'united-states'): 'Abidjan',
    # UAE second wave
    ('turkey', 'united-arab-emirates'):      'Ankara',
    ('ghana', 'united-arab-emirates'):       'Accra',
    ('nigeria', 'united-arab-emirates'):     'Abuja',
    ('south-korea', 'united-arab-emirates'): 'Seoul',
    ('china', 'united-arab-emirates'):       'Beijing',
    ('vietnam', 'united-arab-emirates'):     'Hanoi',
    ('iraq', 'united-arab-emirates'):        'Baghdad',
    ('afghanistan', 'united-arab-emirates'): 'Kabul',
    # Germany second wave
    ('india', 'germany'):      'New Delhi',
    ('bangladesh', 'germany'): 'Dhaka',
    ('china', 'germany'):      'Beijing',
    ('spain', 'germany'):      'Madrid',
    ('portugal', 'germany'):   'Lisbon',
    ('algeria', 'germany'):    'Algiers',
    ('tunisia', 'germany'):    'Tunis',
    ('pakistan', 'germany'):   'Islamabad',
    # France second wave
    ('nigeria', 'france'):       'Abuja',
    ('burkina-faso', 'france'):  'Ouagadougou',
    ('guinea-bissau', 'france'): 'Bissau',
    ('niger', 'france'):         'Niamey',
    ('chad', 'france'):          "N'Djamena",
    ('mauritania', 'france'):    'Nouakchott',
    ('togo', 'france'):          'Lome',
    ('benin', 'france'):         'Cotonou',
    ('gabon', 'france'):         'Libreville',
    # Canada second wave
    ('bangladesh', 'canada'):          'Dhaka',
    ('ghana', 'canada'):               'Accra',
    ('jamaica', 'canada'):             'Kingston',
    ('trinidad-and-tobago', 'canada'): 'Port of Spain',
    ('kenya', 'canada'):               'Nairobi',
    ('ethiopia', 'canada'):            'Addis Ababa',
    ('mexico', 'canada'):              'Mexico City',
    ('vietnam', 'canada'):             'Hanoi',
    ('iraq', 'canada'):                'Baghdad',
    # Australia second wave
    ('bangladesh', 'australia'): 'Dhaka',
    ('pakistan', 'australia'):   'Islamabad',
    ('myanmar', 'australia'):    'Naypyidaw',
    ('fiji', 'australia'):       'Suva',
    ('sri-lanka', 'australia'):  'Colombo',
    ('singapore', 'australia'):  'Singapore',
    ('kenya', 'australia'):      'Nairobi',
    ('ghana', 'australia'):      'Accra',
    # India second wave
    ('pakistan', 'india'):   'Islamabad',
    ('china', 'india'):      'Beijing',
    ('sri-lanka', 'india'):  'Colombo',
    ('thailand', 'india'):   'Bangkok',
    ('japan', 'india'):      'Tokyo',
    ('kenya', 'india'):      'Nairobi',
    ('nigeria', 'india'):    'Abuja',
    ('indonesia', 'india'):  'Jakarta',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R18: To Qatar
    ('india', 'qatar'): (
        "Indian nationals are the single largest expatriate group in Qatar. "
        "When a Qatar-based Indian worker has a family member die in India, repatriation "
        "of remains to Qatar follows an established documentation pathway through the "
        "Qatari Embassy in New Delhi. This is one of the highest-volume South Asia to Gulf "
        "repatriation corridors."
    ),
    ('pakistan', 'qatar'): (
        "Pakistani nationals form one of the largest expatriate communities in Qatar. "
        "This corridor handles cases where a Qatar-based Pakistani has a family member die "
        "in Pakistan and needs remains brought to Qatar. Documentation is attested through "
        "the Qatari Embassy in Islamabad."
    ),
    ('bangladesh', 'qatar'): (
        "Bangladeshi nationals work in Qatar in substantial numbers, particularly in "
        "construction and service sectors. This corridor handles cases where a Qatar-based "
        "Bangladeshi national has a family member die in Bangladesh and needs remains "
        "brought to Qatar. All documents must be attested by the Qatar Embassy in Dhaka."
    ),
    ('philippines', 'qatar'): (
        "Filipino nationals form a significant expatriate community in Qatar, working in "
        "professional, domestic, and service roles. This corridor handles repatriation of "
        "remains from the Philippines to Qatar when a Qatar-based Filipino has a family "
        "member die in the Philippines. The Philippine government's Overseas Workers Welfare "
        "Administration (OWWA) provides support for overseas workers on this corridor."
    ),
    ('nepal', 'qatar'): (
        "Nepali nationals work in Qatar in large numbers, particularly in construction. "
        "This corridor handles cases where a Qatar-based Nepali worker has a family member "
        "die in Nepal and needs remains brought to Qatar. Nepal's Department of Foreign "
        "Employment provides support structures for overseas workers."
    ),
    ('egypt', 'qatar'): (
        "Egyptian nationals form part of Qatar's substantial Arab professional and business "
        "community. This corridor handles cases where a Qatar-based Egyptian has a family "
        "member die in Egypt and needs remains brought to Qatar. Documentation is attested "
        "through the Qatar Embassy in Cairo."
    ),
    ('sri-lanka', 'qatar'): (
        "Sri Lankan nationals work across Qatar in domestic, professional, and service roles. "
        "This corridor handles cases where a Qatar-based Sri Lankan has a family member die "
        "in Sri Lanka and needs remains brought to Qatar. Documentation requires attestation "
        "by the Qatar Embassy in Colombo."
    ),
    ('ethiopia', 'qatar'): (
        "Ethiopian nationals work in Qatar in domestic and service roles. "
        "This corridor handles cases where a Qatar-based Ethiopian has a family member die "
        "in Ethiopia and needs remains brought to Qatar. Amharic documentation requires "
        "certified translation for Qatari authorities."
    ),
    ('indonesia', 'qatar'): (
        "Indonesian nationals work in Qatar, particularly in domestic and professional roles. "
        "This corridor handles cases where a Qatar-based Indonesian has a family member die "
        "in Indonesia and needs remains brought to Qatar. Indonesia has government support "
        "structures for overseas workers in repatriation cases."
    ),
    ('kenya', 'qatar'): (
        "Kenyan nationals work in Qatar in various professional and service sectors. "
        "This corridor handles cases where a Qatar-based Kenyan has a family member die in "
        "Kenya and needs remains brought to Qatar. Documentation is attested through the "
        "Qatar Embassy in Nairobi."
    ),
    # R18: To Kuwait
    ('india', 'kuwait'): (
        "Indian nationals are the largest expatriate community in Kuwait, working in "
        "professional, business, and service roles. This corridor handles cases where a "
        "Kuwait-based Indian worker has a family member die in India and needs remains "
        "brought to Kuwait. The Kuwait Embassy in New Delhi handles document attestation."
    ),
    ('pakistan', 'kuwait'): (
        "Pakistani nationals form a major expatriate community in Kuwait. This corridor "
        "handles cases where a Kuwait-based Pakistani has a family member die in Pakistan "
        "and needs remains brought to Kuwait. Documentation is attested through the "
        "Kuwaiti Embassy in Islamabad."
    ),
    ('bangladesh', 'kuwait'): (
        "Bangladeshi nationals work in Kuwait in construction, domestic, and service sectors. "
        "This corridor handles cases where a Kuwait-based Bangladeshi has a family member die "
        "in Bangladesh and needs remains brought to Kuwait. All documents require attestation "
        "by the Kuwait Embassy in Dhaka."
    ),
    ('philippines', 'kuwait'): (
        "Filipino nationals form a significant expatriate community in Kuwait, working in "
        "domestic, professional, and healthcare roles. This corridor handles repatriation of "
        "remains from the Philippines to Kuwait when a Kuwait-based Filipino has a family "
        "member die in the Philippines."
    ),
    ('egypt', 'kuwait'): (
        "Egyptian nationals form part of Kuwait's large Arab professional community. "
        "This corridor handles cases where a Kuwait-based Egyptian has a family member die "
        "in Egypt and needs remains brought to Kuwait. Documentation is attested through "
        "the Kuwait Embassy in Cairo."
    ),
    ('sri-lanka', 'kuwait'): (
        "Sri Lankan nationals work in Kuwait in domestic and service roles. This corridor "
        "handles cases where a Kuwait-based Sri Lankan has a family member die in Sri Lanka "
        "and needs remains brought to Kuwait. Documentation requires attestation by the "
        "Kuwait Embassy in Colombo."
    ),
    ('nepal', 'kuwait'): (
        "Nepali nationals work in Kuwait in construction and service roles. This corridor "
        "handles cases where a Kuwait-based Nepali has a family member die in Nepal and "
        "needs remains brought to Kuwait. Nepal's Department of Foreign Employment provides "
        "support structures for overseas workers."
    ),
    ('ethiopia', 'kuwait'): (
        "Ethiopian nationals work in Kuwait in domestic and service roles. This corridor "
        "handles cases where a Kuwait-based Ethiopian has a family member die in Ethiopia "
        "and needs remains brought to Kuwait. Amharic documentation requires certified "
        "translation for Kuwaiti authorities."
    ),
    # R18: To Singapore
    ('india', 'singapore'): (
        "Indian nationals form one of Singapore's largest communities, working in technology, "
        "finance, and services. This corridor handles cases where a Singapore-based Indian "
        "has a family member die in India and needs remains brought to Singapore. "
        "The Singapore High Commission in New Delhi handles document authentication."
    ),
    ('china', 'singapore'): (
        "Chinese nationals and Singaporeans of Chinese heritage make Singapore's China "
        "connections among the strongest in the region. This corridor handles cases where a "
        "Singapore-based Chinese national has a family member die in China and needs remains "
        "brought to Singapore. Documentation requires certified English translation."
    ),
    ('malaysia', 'singapore'): (
        "Malaysian nationals cross into Singapore for work in large numbers, and the two "
        "countries share close cultural and family ties. This is one of the highest-volume "
        "short-haul repatriation corridors in South-East Asia. Singapore and Malaysia share "
        "administrative traditions that simplify some documentation requirements."
    ),
    ('philippines', 'singapore'): (
        "Filipino nationals work across Singapore in domestic, professional, and service roles. "
        "This corridor handles cases where a Singapore-based Filipino has a family member die "
        "in the Philippines and needs remains brought to Singapore. The Philippine government "
        "provides support for overseas workers through OWWA."
    ),
    ('bangladesh', 'singapore'): (
        "Bangladeshi nationals work in Singapore in construction and service sectors. "
        "This corridor handles cases where a Singapore-based Bangladeshi worker has a family "
        "member die in Bangladesh and needs remains brought to Singapore. All documents must "
        "be authenticated by the Singapore High Commission in Dhaka."
    ),
    ('indonesia', 'singapore'): (
        "Indonesian nationals work in Singapore in domestic, construction, and service sectors. "
        "This is one of the busiest short-haul repatriation corridors in the region, given "
        "the close proximity of the two countries and the large number of Indonesian workers "
        "in Singapore. Direct ferry and air links connect the two countries."
    ),
    ('myanmar', 'singapore'): (
        "Myanmar nationals work in Singapore in various sectors, including construction and "
        "domestic work. This corridor handles cases where a Singapore-based Myanmar national "
        "has a family member die in Myanmar and needs remains brought to Singapore. "
        "Documentation requires authentication by the Singapore Embassy in Naypyidaw."
    ),
    # R19: To South Africa
    ('zimbabwe', 'south-africa'): (
        "Zimbabwean nationals form the largest foreign national community in South Africa. "
        "This is one of the highest-volume repatriation corridors in southern Africa. "
        "Many South Africa-based Zimbabweans need remains of family members brought from "
        "Zimbabwe for burial. South African funeral directors in Limpopo and Gauteng have "
        "direct experience of the Zimbabwe documentation process."
    ),
    ('mozambique', 'south-africa'): (
        "Mozambican nationals work in South Africa in large numbers, particularly in mining "
        "and agriculture. This corridor handles repatriation of remains from Mozambique to "
        "South Africa when a South Africa-based Mozambican has a family member die in "
        "Mozambique. Portuguese documentation requires certified translation."
    ),
    ('lesotho', 'south-africa'): (
        "Lesotho is entirely surrounded by South Africa, and Basotho nationals work in South "
        "Africa in substantial numbers, particularly in mining. This corridor handles "
        "repatriation of remains from Lesotho to South Africa for families of South "
        "Africa-based Basotho nationals. Cross-border coordination is well-established."
    ),
    ('malawi', 'south-africa'): (
        "Malawian nationals work in South Africa in various sectors. This corridor handles "
        "cases where a South Africa-based Malawian has a family member die in Malawi and "
        "needs remains brought to South Africa. The South African Embassy in Lilongwe "
        "advises on documentation requirements."
    ),
    ('zambia', 'south-africa'): (
        "Zambian nationals work and study in South Africa, and cross-border movement is "
        "well-established within the SADC region. This corridor handles repatriation of "
        "remains from Zambia to South Africa when a South Africa-based Zambian has a family "
        "member die in Zambia."
    ),
    ('democratic-republic-of-the-congo', 'south-africa'): (
        "Congolese nationals form a significant community in South Africa, particularly in "
        "Johannesburg's central business district. This corridor handles cases where a "
        "South Africa-based Congolese national has a family member die in the DRC and needs "
        "remains brought to South Africa. French documentation requires certified translation."
    ),
    ('tanzania', 'south-africa'): (
        "Tanzanian nationals work in South Africa across several sectors. This corridor "
        "handles cases where a South Africa-based Tanzanian has a family member die in "
        "Tanzania and needs remains brought to South Africa. The SADC framework supports "
        "cross-border repatriation within southern and eastern Africa."
    ),
    ('botswana', 'south-africa'): (
        "Botswanan nationals share a long border with South Africa and cross-border movement "
        "between the two countries is constant. This corridor handles cases where a South "
        "Africa-based Botswanan has a family member die in Botswana and needs remains "
        "brought to South Africa."
    ),
    ('namibia', 'south-africa'): (
        "Namibian nationals work and study in South Africa, and the two countries share close "
        "historical and administrative ties. This corridor handles repatriation of remains "
        "from Namibia to South Africa when a South Africa-based Namibian has a family "
        "member die in Namibia."
    ),
    ('nigeria', 'south-africa'): (
        "Nigerian nationals form a significant professional and business community in South "
        "Africa, particularly in Johannesburg. This corridor handles cases where a South "
        "Africa-based Nigerian has a family member die in Nigeria and needs remains brought "
        "to South Africa. Nigeria's documentation process requires engagement with the "
        "National Population Commission."
    ),
    ('ghana', 'south-africa'): (
        "Ghanaian nationals work in South Africa in professional and business roles. "
        "This corridor handles cases where a South Africa-based Ghanaian has a family member "
        "die in Ghana and needs remains brought to South Africa. Ghana's documentation "
        "process is well-mapped for the diaspora community."
    ),
    ('kenya', 'south-africa'): (
        "Kenyan nationals work across South Africa in professional sectors. This corridor "
        "handles cases where a South Africa-based Kenyan has a family member die in Kenya "
        "and needs remains brought to South Africa. Both countries are English-speaking, "
        "which simplifies some documentation requirements."
    ),
    ('ethiopia', 'south-africa'): (
        "Ethiopian nationals form a growing community in South Africa. This corridor handles "
        "cases where a South Africa-based Ethiopian has a family member die in Ethiopia and "
        "needs remains brought to South Africa. Amharic documentation requires certified "
        "English translation for South African authorities."
    ),
    ('angola', 'south-africa'): (
        "Angolan nationals work in South Africa and cross-border repatriation between the "
        "two countries is established within the SADC framework. This corridor handles cases "
        "where a South Africa-based Angolan has a family member die in Angola. "
        "Portuguese documentation requires certified translation."
    ),
    ('cameroon', 'south-africa'): (
        "Cameroonian nationals work and study in South Africa. This corridor handles cases "
        "where a South Africa-based Cameroonian has a family member die in Cameroon and "
        "needs remains brought to South Africa. Cameroon's bilingual French and English "
        "documentation simplifies some translation requirements."
    ),
    # R19: USA second wave
    ('bangladesh', 'united-states'): (
        "Bangladeshi-American communities, concentrated in New York City, New Jersey, and "
        "Michigan, account for significant repatriation demand on this corridor. "
        "Bangladesh's documentation process requires certified English translation and "
        "coordination with the civil registration authority."
    ),
    ('turkey', 'united-states'): (
        "Turkish-American communities across New York, New Jersey, and California account "
        "for consistent repatriation demand. Turkey's well-organised civil registration "
        "system makes documentation on this corridor relatively straightforward with a "
        "specialist. The nufus mudurlugu (civil registry) handles official documentation."
    ),
    ('egypt', 'united-states'): (
        "Egyptian-American communities in California, New York, and New Jersey account for "
        "steady repatriation demand. Egyptian documentation is in Arabic and requires "
        "certified English translation. The US Embassy in Cairo can assist with consular "
        "services. Egypt's civil registry handles official death documentation."
    ),
    ('poland', 'united-states'): (
        "Polish-American communities in Chicago, New York, and Michigan are among the "
        "longest-established in the United States. Poland's documentation process is "
        "well-organised, and the EU apostille framework simplifies authentication of "
        "Polish official documents for US acceptance."
    ),
    ('morocco', 'united-states'): (
        "Moroccan-American communities in New York, New Jersey, and Virginia account for "
        "growing repatriation demand. Moroccan documentation is in Arabic and French and "
        "requires certified English translation. Royal Air Maroc operates direct cargo "
        "connections between Casablanca and US cities."
    ),
    ('indonesia', 'united-states'): (
        "Indonesian-American communities across California and New York account for "
        "repatriation demand on this corridor. Indonesian documentation is in Bahasa "
        "Indonesia and requires certified English translation. Jakarta has direct cargo "
        "connections to the US through major hub airports."
    ),
    ('kenya', 'united-states'): (
        "Kenyan-American communities across Texas, Minnesota, and Washington account for "
        "consistent repatriation demand. Kenya's documentation process runs through the "
        "civil registry and the Kenya National Bureau of Statistics. English documentation "
        "simplifies some translation requirements."
    ),
    ('senegal', 'united-states'): (
        "Senegalese-American communities in New York, particularly in Harlem, and in "
        "Atlanta account for repatriation demand on this corridor. Senegalese documentation "
        "is in French and requires certified English translation for US acceptance."
    ),
    ('laos', 'united-states'): (
        "Laotian-American communities in California, Minnesota, and Texas are among the "
        "larger South-East Asian diaspora groups in the United States. Laotian documentation "
        "requires certified English translation and coordination with the Ministry of Interior."
    ),
    ('ivory-coast', 'united-states'): (
        "Ivorian-American communities in New York, Maryland, and Georgia account for growing "
        "repatriation demand. Documentation from Ivory Coast is in French and requires "
        "certified English translation. Air France and other carriers connect Abidjan to "
        "US cities via European hubs."
    ),
    # R20: UAE second wave
    ('turkey', 'united-arab-emirates'): (
        "Turkish nationals form a professional and business community in the UAE, "
        "particularly in Dubai and Abu Dhabi. This corridor handles cases where a UAE-based "
        "Turkish national has a family member die in Turkey and needs remains brought to "
        "the UAE. The UAE Embassy in Ankara handles document attestation."
    ),
    ('ghana', 'united-arab-emirates'): (
        "Ghanaian nationals work across the UAE in professional and service roles. "
        "This corridor handles cases where a UAE-based Ghanaian has a family member die in "
        "Ghana and needs remains brought to the UAE. The UAE Embassy in Accra handles "
        "document attestation."
    ),
    ('nigeria', 'united-arab-emirates'): (
        "Nigerian nationals form a growing professional and business community in the UAE. "
        "This corridor handles cases where a UAE-based Nigerian has a family member die in "
        "Nigeria and needs remains brought to the UAE. Documentation requires attestation "
        "by the UAE Embassy in Abuja."
    ),
    ('south-korea', 'united-arab-emirates'): (
        "South Korean nationals work in the UAE in business, engineering, and professional "
        "roles. This corridor handles repatriation of remains from South Korea to the UAE "
        "when a UAE-based Korean has a family member die in South Korea. Korean documentation "
        "requires certified translation for UAE authorities."
    ),
    ('china', 'united-arab-emirates'): (
        "Chinese nationals form a significant business and professional community in the UAE, "
        "particularly in Dubai's international trade sector. This corridor handles cases where "
        "a UAE-based Chinese national has a family member die in China and needs remains "
        "brought to the UAE. Documentation requires certified translation."
    ),
    ('vietnam', 'united-arab-emirates'): (
        "Vietnamese nationals work in the UAE in professional and service roles. This corridor "
        "handles cases where a UAE-based Vietnamese national has a family member die in Vietnam "
        "and needs remains brought to the UAE. Vietnamese documentation requires certified "
        "translation for UAE attestation."
    ),
    ('iraq', 'united-arab-emirates'): (
        "Iraqi nationals form part of the UAE's Arab professional and business community. "
        "This corridor handles cases where a UAE-based Iraqi national has a family member "
        "die in Iraq and needs remains brought to the UAE. Documentation requires attestation "
        "by the UAE Embassy in Baghdad."
    ),
    ('afghanistan', 'united-arab-emirates'): (
        "Afghan nationals form a community in the UAE, particularly in Dubai and Sharjah. "
        "This corridor handles cases where a UAE-based Afghan has a family member die in "
        "Afghanistan and needs remains brought to the UAE. The political situation in "
        "Afghanistan since 2021 means specialist coordination is essential on this corridor."
    ),
    # R20: Germany second wave
    ('india', 'germany'): (
        "Indian nationals form a growing professional and academic community in Germany, "
        "particularly in technology, research, and medical sectors. This corridor handles "
        "cases where a Germany-based Indian has a family member die in India and needs "
        "remains brought to Germany. Documentation requires certified German translation."
    ),
    ('bangladesh', 'germany'): (
        "Bangladeshi nationals form part of Germany's South Asian diaspora community. "
        "This corridor handles cases where a Germany-based Bangladeshi has a family member "
        "die in Bangladesh and needs remains brought to Germany. Documentation from Bangladesh "
        "requires certified German translation."
    ),
    ('china', 'germany'): (
        "Chinese nationals form a significant professional and student community in Germany. "
        "This corridor handles cases where a Germany-based Chinese national has a family "
        "member die in China and needs remains brought to Germany. Documentation requires "
        "certified German translation from Mandarin."
    ),
    ('spain', 'germany'): (
        "Spanish nationals work in Germany as part of the EU freedom of movement. This "
        "corridor handles cases where a Germany-based Spaniard has a family member die in "
        "Spain and needs remains brought to Germany. The EU Berlin Convention and apostille "
        "framework simplifies some authentication requirements."
    ),
    ('portugal', 'germany'): (
        "Portuguese nationals are among the older EU migrant communities in Germany, with "
        "ties going back to guest worker programmes in the 1960s. This corridor handles "
        "cases where a Germany-based Portuguese has a family member die in Portugal and "
        "needs remains brought to Germany."
    ),
    ('algeria', 'germany'): (
        "Algerian nationals form part of Germany's North African diaspora community. "
        "This corridor handles cases where a Germany-based Algerian has a family member "
        "die in Algeria and needs remains brought to Germany. Arabic documentation requires "
        "certified German translation."
    ),
    ('tunisia', 'germany'): (
        "Tunisian nationals form part of Germany's North African diaspora community. "
        "This corridor handles repatriation of remains from Tunisia to Germany for families "
        "of Germany-based Tunisians. Arabic documentation requires certified German translation."
    ),
    ('pakistan', 'germany'): (
        "Pakistani nationals form a growing South Asian community in Germany, particularly "
        "in North Rhine-Westphalia and Bavaria. This corridor handles cases where a Germany-based "
        "Pakistani has a family member die in Pakistan and needs remains brought to Germany. "
        "Documentation requires certified German translation."
    ),
    # R20: France second wave
    ('nigeria', 'france'): (
        "Nigerian nationals form a growing community in France, with communities in Paris "
        "and Lyon. This corridor handles cases where a France-based Nigerian has a family "
        "member die in Nigeria and needs remains brought to France. Documentation from "
        "Nigeria requires certified French translation."
    ),
    ('burkina-faso', 'france'): (
        "Burkinabe nationals form part of France's West African diaspora, with communities "
        "in Paris and Lyon. This corridor handles cases where a France-based Burkinabe has "
        "a family member die in Burkina Faso and needs remains brought to France. "
        "The situation in Burkina Faso since 2022 may affect logistics on this corridor."
    ),
    ('guinea-bissau', 'france'): (
        "Guinea-Bissau nationals form part of France's West African diaspora. This corridor "
        "handles repatriation of remains from Guinea-Bissau to France. Guinea-Bissau's "
        "official language is Portuguese, so documents may require French translation for "
        "the French authorities."
    ),
    ('niger', 'france'): (
        "Nigerien nationals form part of France's Sahelian West African diaspora community. "
        "This corridor handles cases where a France-based Nigerien has a family member die "
        "in Niger and needs remains brought to France. French documentation from Niger "
        "simplifies translation requirements."
    ),
    ('chad', 'france'): (
        "Chadian nationals form part of France's Central African diaspora. This corridor "
        "handles cases where a France-based Chadian has a family member die in Chad and "
        "needs remains brought to France. Chad uses French as an official language, "
        "which simplifies the translation requirement."
    ),
    ('mauritania', 'france'): (
        "Mauritanian nationals form part of France's Saharan West African diaspora. "
        "This corridor handles cases where a France-based Mauritanian has a family member "
        "die in Mauritania and needs remains brought to France. Mauritania uses Arabic and "
        "French as official languages."
    ),
    ('togo', 'france'): (
        "Togolese nationals form part of France's West African diaspora. This corridor "
        "handles cases where a France-based Togolese national has a family member die in "
        "Togo and needs remains brought to France. Togo uses French as its official language, "
        "which simplifies the translation requirement."
    ),
    ('benin', 'france'): (
        "Beninese nationals form part of France's West African diaspora community. This "
        "corridor handles cases where a France-based Beninese has a family member die in "
        "Benin and needs remains brought to France. Benin uses French as its official language."
    ),
    ('gabon', 'france'): (
        "Gabonese nationals form part of France's Central African diaspora. This corridor "
        "handles cases where a France-based Gabonese national has a family member die in "
        "Gabon and needs remains brought to France. Gabon uses French as its official language."
    ),
    # R21: Canada second wave
    ('bangladesh', 'canada'): (
        "Bangladeshi-Canadians form a growing South Asian community in Canada, particularly "
        "in Toronto and Calgary. This corridor handles cases where a Canada-based Bangladeshi "
        "has a family member die in Bangladesh and needs remains brought to Canada. "
        "Global Affairs Canada emergency line: +1 (613) 996-8885."
    ),
    ('ghana', 'canada'): (
        "Ghanaian-Canadians form part of Canada's sub-Saharan African diaspora, concentrated "
        "in the Greater Toronto Area. This corridor handles cases where a Canada-based "
        "Ghanaian has a family member die in Ghana and needs remains brought to Canada. "
        "The Canadian High Commission in Accra can assist with consular matters."
    ),
    ('jamaica', 'canada'): (
        "Jamaican-Canadians form one of Canada's largest Caribbean diaspora communities, "
        "with a long history of settlement particularly in Toronto. This corridor handles "
        "cases where a Canada-based Jamaican has a family member die in Jamaica and needs "
        "remains brought to Canada. Direct flights connect Jamaica to Canadian cities."
    ),
    ('trinidad-and-tobago', 'canada'): (
        "Trinidadian and Tobagonian communities in Toronto and other Canadian cities account "
        "for consistent repatriation demand. Trinidad and Tobago has established repatriation "
        "procedures and direct air links to Canada. The Canadian High Commission in Port of "
        "Spain can provide consular assistance."
    ),
    ('kenya', 'canada'): (
        "Kenyan-Canadians form a growing East African community in Canada. This corridor "
        "handles cases where a Canada-based Kenyan has a family member die in Kenya and "
        "needs remains brought to Canada. Both countries share Commonwealth administrative "
        "traditions that simplify some documentation requirements."
    ),
    ('ethiopia', 'canada'): (
        "Ethiopian-Canadians form a significant community in Toronto, Ottawa, and other "
        "Canadian cities. This corridor handles cases where a Canada-based Ethiopian has a "
        "family member die in Ethiopia and needs remains brought to Canada. Amharic "
        "documentation requires certified English translation."
    ),
    ('mexico', 'canada'): (
        "Mexican nationals working temporarily or permanently in Canada account for "
        "repatriation demand on this corridor. Mexico has direct air cargo links to major "
        "Canadian cities. Documentation runs through the Mexican civil registry (Registro Civil) "
        "and requires certified English or French translation."
    ),
    ('vietnam', 'canada'): (
        "Vietnamese-Canadians form a significant community in Toronto, Vancouver, and Montreal. "
        "This corridor handles cases where a Canada-based Vietnamese has a family member die "
        "in Vietnam and needs remains brought to Canada. Vietnamese documentation requires "
        "certified English translation."
    ),
    ('iraq', 'canada'): (
        "Iraqi-Canadians form part of Canada's Middle Eastern diaspora community, with "
        "significant populations in Toronto and Ottawa. This corridor handles cases where a "
        "Canada-based Iraqi has a family member die in Iraq and needs remains brought to "
        "Canada. Arabic documentation requires certified English translation."
    ),
    # R21: Australia second wave
    ('bangladesh', 'australia'): (
        "Bangladeshi-Australians form a growing community in Sydney and Melbourne. This "
        "corridor handles cases where an Australia-based Bangladeshi has a family member die "
        "in Bangladesh and needs remains brought to Australia. The Australian High Commission "
        "in Dhaka can provide consular assistance."
    ),
    ('pakistan', 'australia'): (
        "Pakistani-Australians form a significant South Asian community in Sydney and "
        "Melbourne. This corridor handles cases where an Australia-based Pakistani has a "
        "family member die in Pakistan and needs remains brought to Australia. The Australian "
        "High Commission in Islamabad assists with consular matters."
    ),
    ('myanmar', 'australia'): (
        "Myanmar nationals have formed a community in Australia, with significant numbers "
        "in Melbourne and Sydney. This corridor handles cases where an Australia-based Myanmar "
        "national has a family member die in Myanmar and needs remains brought to Australia. "
        "Documentation requires certified English translation."
    ),
    ('fiji', 'australia'): (
        "Fijian-Australians form a significant Pacific Islander community, particularly in "
        "New South Wales and Queensland. This corridor handles cases where an Australia-based "
        "Fijian has a family member die in Fiji and needs remains brought to Australia. "
        "Direct flights connect Fiji to Sydney and Melbourne."
    ),
    ('sri-lanka', 'australia'): (
        "Sri Lankan-Australians form a significant community in Melbourne and Sydney. This "
        "corridor handles cases where an Australia-based Sri Lankan has a family member die "
        "in Sri Lanka and needs remains brought to Australia. The Australian High Commission "
        "in Colombo can provide consular assistance."
    ),
    ('singapore', 'australia'): (
        "Singaporeans work and study in Australia in significant numbers, and the two countries "
        "share strong bilateral ties. This corridor handles cases where an Australia-based "
        "Singaporean has a family member die in Singapore and needs remains brought to "
        "Australia. Shared Commonwealth administrative traditions simplify some requirements."
    ),
    ('kenya', 'australia'): (
        "Kenyan-Australians form a growing East African community in Melbourne and Sydney. "
        "This corridor handles cases where an Australia-based Kenyan has a family member die "
        "in Kenya and needs remains brought to Australia. Commonwealth administrative ties "
        "simplify some documentation requirements."
    ),
    ('ghana', 'australia'): (
        "Ghanaian-Australians form part of Australia's sub-Saharan African diaspora. This "
        "corridor handles cases where an Australia-based Ghanaian has a family member die in "
        "Ghana and needs remains brought to Australia. The Australian High Commission in "
        "Accra can provide consular assistance."
    ),
    # R21: India second wave
    ('pakistan', 'india'): (
        "Pakistan and India share complex historical, cultural, and family ties. This corridor "
        "handles cases where an India-based person has a family member die in Pakistan and "
        "needs remains brought to India. Given the state of diplomatic relations between the "
        "two countries, specialist coordination is essential on this corridor."
    ),
    ('china', 'india'): (
        "Chinese nationals work and study in India, and there is a resident Chinese business "
        "community in some Indian cities. This corridor handles cases where an India-based "
        "person has a family member die in China and needs remains brought to India. "
        "Documentation requires certified translation from Mandarin."
    ),
    ('sri-lanka', 'india'): (
        "Sri Lankan nationals form a community in India, and the two countries share "
        "historic, cultural, and geographic connections. This corridor handles cases where "
        "an India-based person has a family member die in Sri Lanka and needs remains "
        "brought to India. Direct air links connect Colombo to Chennai, Mumbai, and Delhi."
    ),
    ('thailand', 'india'): (
        "Thai nationals visit India for business and tourism, and there is a resident Thai "
        "community in some Indian cities. This corridor handles cases where an India-based "
        "person has a family member die in Thailand and needs remains brought to India. "
        "Thai documentation requires certified translation."
    ),
    ('japan', 'india'): (
        "Japanese nationals work and study in India, particularly in technology and "
        "automotive sectors. This corridor handles cases where an India-based person has "
        "a family member die in Japan and needs remains brought to India. Japanese "
        "documentation requires certified translation."
    ),
    ('kenya', 'india'): (
        "Kenyan nationals of Indian heritage maintain strong family ties to India, and the "
        "historical connection between Kenya and the Indian subcontinent means this corridor "
        "sees consistent demand. Kenya Airways provides direct cargo links between Nairobi "
        "and Indian cities."
    ),
    ('nigeria', 'india'): (
        "Nigerian nationals work and study in India in growing numbers. This corridor handles "
        "cases where an India-based person has a family member die in Nigeria and needs "
        "remains brought to India. Nigeria's documentation process requires engagement with "
        "the National Population Commission."
    ),
    ('indonesia', 'india'): (
        "Indonesian nationals visit and work in India in professional and business capacities. "
        "This corridor handles cases where an India-based person has a family member die in "
        "Indonesia and needs remains brought to India. Documentation requires certified "
        "translation from Bahasa Indonesia."
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

    dest_embassy_city = EMBASSY_CITIES.get((origin_slug, dest_slug), uk_embassy_city or 'the capital')

    intro = CORRIDOR_INTRO.get(
        (origin_slug, dest_slug),
        (
            f"Repatriation from {origin_name} to {dest_name} occurs when a {dest_name}-based "
            f"family has a loved one die in {origin_name} and needs remains returned. "
            f"This corridor follows {origin_name}'s standard export procedures for "
            f"international repatriation of human remains."
        )
    )

    title = f"{origin_name} to {dest_name}: Repatriation Guidance"
    if len(title) > 60:
        title = f"{origin_name} to {dest_name} Repatriation Guide"
    if len(title) > 60:
        abbrevs = {'Democratic Republic of the Congo': 'DR Congo'}
        short_origin = abbrevs.get(origin_name, origin_name)
        title = f"{short_origin} to {dest_name} Repatriation Guide"
    description_notes = {
        'low': 'Established process.',
        'moderate': 'Specialist support recommended.',
        'moderate-high': 'A specialist is essential.',
        'high': 'Specialist help required.',
        'very-high': 'A specialist is essential on this complex route.',
    }
    desc_note = description_notes.get(complexity, 'Specialist support recommended.')
    description = (
        f"Someone has died in {origin_name}. Repatriation to {dest_name} takes "
        f"{timeline_avg}. {desc_note} Contact us 24/7."
    )
    if len(description) > 155:
        description = description[:152] + '...'

    direct_answer_heading = f'direct_answer_heading: "Repatriation from {origin_name} to {dest_name}: what to expect"'
    direct_answer_intro = f'direct_answer_intro: "{intro}"'

    dap_raw = extract_block(uk_fm, 'direct_answer_points', ['overview_heading', 'dest_reception', 'date'])
    dap = dap_raw
    dap = re.sub(r'British Embassy[^"]*advises?\.[^"]*Cannot fund repatriation\.', '', dap)
    dap = re.sub(r'British High Commission[^"]*advises?\.[^"]*Cannot fund repatriation\.', '', dap)
    dap = re.sub(
        r'FCDO[^"]*emergency line[^"]*\.',
        f'{dest_name} Embassy in {dest_embassy_city} can advise. They cannot fund repatriation.',
        dap
    )
    dap = dap.replace('for UK acceptance', f'for {dest_name} acceptance')
    dap = dap.replace('UK funeral director', f'{dest_name} funeral director')
    dap = dap.replace('United Kingdom acceptance', f'{dest_name} acceptance')
    if 'Embassy' not in dap or dest_name not in dap:
        dap = dap.rstrip()
        dap += f'\n  - "{dest_name} Embassy in {dest_embassy_city} can advise on documentation. They cannot fund repatriation."'

    overview_heading_raw = extract_block(uk_fm, 'overview_heading', ['overview_body'])
    overview_body_raw = extract_block(uk_fm, 'overview_body', ['dest_reception', 'dest_consular'])
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
        f'step: 3\n    action: "{dest_name} Embassy in {dest_embassy_city} notified"',
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
    ts = ts.replace('cargo terminal at destination', f'{dest_name} cargo terminal')
    ts = re.sub(
        r'FCDO 24hr: \+44 \(0\)20 7008 5000\.',
        f'Call +44 (0)20 7008 5000 (FCDO) or {dest["emergency_line"]}.',
        ts
    )
    ts = ts.replace('UK funeral director takes custody', f'{dest_name} funeral director takes custody')
    ts = ts.replace('United Kingdom funeral director takes custody', f'{dest_name} funeral director takes custody')
    ts = ts.replace('Coroner notified', 'receiving funeral director coordinates with local authorities')
    ts = re.sub(r'FCDO 24hr:[^\n"]+', f'{dest["emergency_line"]}', ts)

    faqs_raw = extract_block(uk_fm, 'faqs', ['links'])
    faqs = faqs_raw

    faqs = re.sub(
        r'(question: "How long does repatriation from [^"]*) to (?:the )?United Kingdom take\?"',
        rf'\1 to {dest_name} take?"',
        faqs
    )
    faqs = re.sub(
        r'(question: "How long does repatriation from [^"]*) to (?:the )?UK take\?"',
        rf'\1 to {dest_name} take?"',
        faqs
    )
    faqs = faqs.replace('repatriation from ' + origin_name + ' to the UK takes',
                        f'repatriation from {origin_name} to {dest_name} takes')
    faqs = faqs.replace('repatriation from ' + origin_name + ' to United Kingdom takes',
                        f'repatriation from {origin_name} to {dest_name} takes')
    faqs = faqs.replace('repatriation from ' + origin_name + ' to the United Kingdom takes',
                        f'repatriation from {origin_name} to {dest_name} takes')

    new_embassy_q = f'Does the {dest_name} Embassy in {origin_name} help with repatriation?'
    new_embassy_a = (
        f'The {dest_name} Embassy in {dest_embassy_city} can assist with document '
        f'authentication and advise on repatriation requirements. They cannot pay for '
        f'or arrange repatriation. Contact the {dest_name} Embassy in {dest_embassy_city} '
        f'as soon as possible after the death.'
    )
    new_embassy_faq = f'  - question: "{new_embassy_q}"\n    answer: "{new_embassy_a}"'

    faqs = re.sub(
        rf'  - question: "Does the (?:British|Irish) (?:Embassy|High Commission) in [^"]*(?:help with repatriation|assist)[^"]*"\?"\n    answer: "[^"]*"',
        new_embassy_faq,
        faqs
    )
    faqs = re.sub(
        rf'  - question: "Is there an? (?:British|Irish) (?:Embassy|High Commission) in [^"]*\?"\n    answer: "[^"]*"',
        new_embassy_faq,
        faqs
    )

    embassy_faq_q1 = f'Does the British Embassy in {origin_name} help with repatriation?'
    embassy_faq_q2 = f'Is there a British Embassy in {origin_name}?'
    embassy_faq_q3 = f'Does the British High Commission in {origin_name} help with repatriation?'
    for q in [embassy_faq_q1, embassy_faq_q2, embassy_faq_q3]:
        if q in faqs:
            pattern = rf'  - question: "{re.escape(q)}"\n    answer: "[^"]*"'
            faqs = re.sub(pattern, new_embassy_faq, faqs)

    faqs = re.sub(
        r'  - question: "What happens when the body arrives in (?:the )?(?:United Kingdom|UK)\?"\n    answer: "[^"]*"',
        f'  - question: "What happens when the body arrives in {dest_name}?"\n    answer: "{dest["arrival_faq"]}"',
        faqs
    )

    faqs = faqs.replace('UK funeral director', f'{dest_name} funeral director')
    faqs = faqs.replace('United Kingdom funeral director', f'{dest_name} funeral director')
    faqs = faqs.replace('FCDO 24-hour emergency line: +44 (0)20 7008 5000', dest_consular_text[:80])
    faqs = faqs.replace('FCDO emergency line', dest['emergency_line'])
    faqs = faqs.replace('UK coroner', f'{dest_name} receiving authority')
    faqs = faqs.replace('the coroner for the district', f'the receiving authority in {dest_name}')
    faqs = faqs.replace('the Coroner for the district', f'the receiving authority in {dest_name}')

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
    # Strip banned vocabulary inherited from UK source files
    content = content.replace('vital statistics', 'civil registration')
    content = content.replace('—', ',')
    # Protect YAML front-matter delimiters before stripping double-hyphens
    content = content.replace('---', '\x00TRIPLE\x00')
    content = content.replace('--', ',')
    content = content.replace('\x00TRIPLE\x00', '---')
    return content


# ---------------------------------------------------------------------------
# Route list: 4 blocks of 25 = 100 routes (R18-R21)
# Template rotation starts at D (index 3) -- R17 ended on C.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # Block R18: Qatar (10) + Kuwait (8) + Singapore (7) = 25
    ('india', 'qatar'),
    ('pakistan', 'qatar'),
    ('bangladesh', 'qatar'),
    ('philippines', 'qatar'),
    ('nepal', 'qatar'),
    ('egypt', 'qatar'),
    ('sri-lanka', 'qatar'),
    ('ethiopia', 'qatar'),
    ('indonesia', 'qatar'),
    ('kenya', 'qatar'),
    ('india', 'kuwait'),
    ('pakistan', 'kuwait'),
    ('bangladesh', 'kuwait'),
    ('philippines', 'kuwait'),
    ('egypt', 'kuwait'),
    ('sri-lanka', 'kuwait'),
    ('nepal', 'kuwait'),
    ('ethiopia', 'kuwait'),
    ('india', 'singapore'),
    ('china', 'singapore'),
    ('malaysia', 'singapore'),
    ('philippines', 'singapore'),
    ('bangladesh', 'singapore'),
    ('indonesia', 'singapore'),
    ('myanmar', 'singapore'),
    # Block R19: South Africa (15) + USA second wave (10) = 25
    ('zimbabwe', 'south-africa'),
    ('mozambique', 'south-africa'),
    ('lesotho', 'south-africa'),
    ('malawi', 'south-africa'),
    ('zambia', 'south-africa'),
    ('democratic-republic-of-the-congo', 'south-africa'),
    ('tanzania', 'south-africa'),
    ('botswana', 'south-africa'),
    ('namibia', 'south-africa'),
    ('nigeria', 'south-africa'),
    ('ghana', 'south-africa'),
    ('kenya', 'south-africa'),
    ('ethiopia', 'south-africa'),
    ('angola', 'south-africa'),
    ('cameroon', 'south-africa'),
    ('bangladesh', 'united-states'),
    ('turkey', 'united-states'),
    ('egypt', 'united-states'),
    ('poland', 'united-states'),
    ('morocco', 'united-states'),
    ('indonesia', 'united-states'),
    ('kenya', 'united-states'),
    ('senegal', 'united-states'),
    ('laos', 'united-states'),
    ('ivory-coast', 'united-states'),
    # Block R20: UAE second wave (8) + Germany second wave (8) + France second wave (9) = 25
    ('turkey', 'united-arab-emirates'),
    ('ghana', 'united-arab-emirates'),
    ('nigeria', 'united-arab-emirates'),
    ('south-korea', 'united-arab-emirates'),
    ('china', 'united-arab-emirates'),
    ('vietnam', 'united-arab-emirates'),
    ('iraq', 'united-arab-emirates'),
    ('afghanistan', 'united-arab-emirates'),
    ('india', 'germany'),
    ('bangladesh', 'germany'),
    ('china', 'germany'),
    ('spain', 'germany'),
    ('portugal', 'germany'),
    ('algeria', 'germany'),
    ('tunisia', 'germany'),
    ('pakistan', 'germany'),
    ('nigeria', 'france'),
    ('burkina-faso', 'france'),
    ('guinea-bissau', 'france'),
    ('niger', 'france'),
    ('chad', 'france'),
    ('mauritania', 'france'),
    ('togo', 'france'),
    ('benin', 'france'),
    ('gabon', 'france'),
    # Block R21: Canada second wave (9) + Australia second wave (8) + India second wave (8) = 25
    ('bangladesh', 'canada'),
    ('ghana', 'canada'),
    ('jamaica', 'canada'),
    ('trinidad-and-tobago', 'canada'),
    ('kenya', 'canada'),
    ('ethiopia', 'canada'),
    ('mexico', 'canada'),
    ('vietnam', 'canada'),
    ('iraq', 'canada'),
    ('bangladesh', 'australia'),
    ('pakistan', 'australia'),
    ('myanmar', 'australia'),
    ('fiji', 'australia'),
    ('sri-lanka', 'australia'),
    ('singapore', 'australia'),
    ('kenya', 'australia'),
    ('ghana', 'australia'),
    ('pakistan', 'india'),
    ('china', 'india'),
    ('sri-lanka', 'india'),
    ('thailand', 'india'),
    ('japan', 'india'),
    ('kenya', 'india'),
    ('nigeria', 'india'),
    ('indonesia', 'india'),
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

blocks = {
    'R18 (Qatar/Kuwait/Singapore)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['qatar', 'kuwait', 'singapore']
    )],
    'R19 (South Africa/USA wave 2)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['south-africa', 'united-states']
    )],
    'R20 (UAE/Germany/France wave 2)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['united-arab-emirates', 'germany', 'france']
    )],
    'R21 (Canada/Australia/India wave 2)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['canada', 'australia', 'india']
    )],
}
for block, routes in blocks.items():
    if routes:
        print(f"  {block}: {len(routes)} routes, variants {','.join(set(v for _, v in routes))}")
