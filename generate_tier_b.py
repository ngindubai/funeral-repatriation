#!/usr/bin/env python3
"""Generate Tier B route pages: diaspora corridors to 12 destination hubs.
   Chunks R14-R17. Template rotation continues from C (last of R13), so next is D.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

# Starting variant index: R13 ended on C (index 2), so R14 starts at D (index 3).
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
# Embassy city for (origin_slug, dest_slug) pairs
# Maps origin slug -> {dest_slug -> city_name}
# Defaults to origin country capital for most cases.
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # USA embassies
    ('mexico', 'united-states'):              'Mexico City',
    ('philippines', 'united-states'):         'Manila',
    ('india', 'united-states'):               'New Delhi',
    ('china', 'united-states'):               'Beijing',
    ('el-salvador', 'united-states'):         'San Salvador',
    ('dominican-republic', 'united-states'):  'Santo Domingo',
    ('vietnam', 'united-states'):             'Hanoi',
    ('cuba', 'united-states'):                'Havana',
    ('south-korea', 'united-states'):         'Seoul',
    ('guatemala', 'united-states'):           'Guatemala City',
    ('jamaica', 'united-states'):             'Kingston',
    ('haiti', 'united-states'):               'Port-au-Prince',
    ('colombia', 'united-states'):            'Bogota',
    ('nigeria', 'united-states'):             'Abuja',
    ('pakistan', 'united-states'):            'Islamabad',
    ('brazil', 'united-states'):              'Brasilia',
    ('honduras', 'united-states'):            'Tegucigalpa',
    ('ecuador', 'united-states'):             'Quito',
    ('ethiopia', 'united-states'):            'Addis Ababa',
    ('ghana', 'united-states'):               'Accra',
    ('ukraine', 'united-states'):             'Kyiv',
    ('iran', 'united-states'):                'Tehran',
    ('peru', 'united-states'):                'Lima',
    ('cambodia', 'united-states'):            'Phnom Penh',
    ('trinidad-and-tobago', 'united-states'): 'Port of Spain',
    # UAE embassies
    ('india', 'united-arab-emirates'):             'New Delhi',
    ('pakistan', 'united-arab-emirates'):          'Islamabad',
    ('bangladesh', 'united-arab-emirates'):        'Dhaka',
    ('philippines', 'united-arab-emirates'):       'Manila',
    ('egypt', 'united-arab-emirates'):             'Cairo',
    ('nepal', 'united-arab-emirates'):             'Kathmandu',
    ('sri-lanka', 'united-arab-emirates'):         'Colombo',
    ('jordan', 'united-arab-emirates'):            'Amman',
    ('kenya', 'united-arab-emirates'):             'Nairobi',
    ('ethiopia', 'united-arab-emirates'):          'Addis Ababa',
    ('indonesia', 'united-arab-emirates'):         'Jakarta',
    ('morocco', 'united-arab-emirates'):           'Rabat',
    # Saudi Arabia embassies
    ('pakistan', 'saudi-arabia'):    'Islamabad',
    ('india', 'saudi-arabia'):       'New Delhi',
    ('bangladesh', 'saudi-arabia'):  'Dhaka',
    ('philippines', 'saudi-arabia'): 'Manila',
    ('indonesia', 'saudi-arabia'):   'Jakarta',
    ('egypt', 'saudi-arabia'):       'Cairo',
    ('nepal', 'saudi-arabia'):       'Kathmandu',
    ('ethiopia', 'saudi-arabia'):    'Addis Ababa',
    ('jordan', 'saudi-arabia'):      'Amman',
    ('kenya', 'saudi-arabia'):       'Nairobi',
    ('sri-lanka', 'saudi-arabia'):   'Colombo',
    ('ghana', 'saudi-arabia'):       'Accra',
    ('nigeria', 'saudi-arabia'):     'Abuja',
    ('yemen', 'saudi-arabia'):       'Sanaa',
    # Germany embassies
    ('turkey', 'germany'):      'Ankara',
    ('poland', 'germany'):      'Warsaw',
    ('russia', 'germany'):      'Moscow',
    ('romania', 'germany'):     'Bucharest',
    ('italy', 'germany'):       'Rome',
    ('serbia', 'germany'):      'Belgrade',
    ('ukraine', 'germany'):     'Kyiv',
    ('iraq', 'germany'):        'Baghdad',
    ('morocco', 'germany'):     'Rabat',
    ('ghana', 'germany'):       'Accra',
    ('nigeria', 'germany'):     'Abuja',
    ('vietnam', 'germany'):     'Hanoi',
    ('afghanistan', 'germany'): 'Kabul',
    # France embassies
    ('morocco', 'france'):      'Rabat',
    ('algeria', 'france'):      'Algiers',
    ('tunisia', 'france'):      'Tunis',
    ('portugal', 'france'):     'Lisbon',
    ('senegal', 'france'):      'Dakar',
    ('ivory-coast', 'france'):  'Abidjan',
    ('cameroon', 'france'):     'Yaounde',
    ('mali', 'france'):         'Bamako',
    ('guinea', 'france'):       'Conakry',
    ('congo', 'france'):        'Brazzaville',
    ('madagascar', 'france'):   'Antananarivo',
    ('haiti', 'france'):        'Port-au-Prince',
    # Canada embassies
    ('india', 'canada'):        'New Delhi',
    ('philippines', 'canada'):  'Manila',
    ('china', 'canada'):        'Beijing',
    ('pakistan', 'canada'):     'Islamabad',
    ('nigeria', 'canada'):      'Abuja',
    ('ukraine', 'canada'):      'Kyiv',
    ('south-korea', 'canada'):  'Seoul',
    ('iran', 'canada'):         'Tehran',
    # Australia embassies
    ('india', 'australia'):       'New Delhi',
    ('china', 'australia'):       'Beijing',
    ('philippines', 'australia'): 'Manila',
    ('vietnam', 'australia'):     'Hanoi',
    ('malaysia', 'australia'):    'Kuala Lumpur',
    ('south-korea', 'australia'): 'Seoul',
    ('new-zealand', 'australia'): 'Wellington',
    ('indonesia', 'australia'):   'Jakarta',
    ('nepal', 'australia'):       'Kathmandu',
    # India embassies (origin -> India)
    ('bangladesh', 'india'):         'Dhaka',
    ('nepal', 'india'):              'Kathmandu',
    ('singapore', 'india'):          'Singapore',
    ('malaysia', 'india'):           'Kuala Lumpur',
    ('united-states', 'india'):      'Washington DC',
    ('canada', 'india'):             'Ottawa',
    ('australia', 'india'):          'Canberra',
    ('united-arab-emirates', 'india'): 'Abu Dhabi',
}


# ---------------------------------------------------------------------------
# Corridor intro text (brief, specific to the diaspora connection)
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # To USA
    ('mexico', 'united-states'): (
        "Mexico to the United States is one of the highest-volume international repatriation "
        "corridors in the world. Mexican-American communities across California, Texas, New York, "
        "Illinois, and Arizona account for many cases. Deaths in Mexico require SEMEFO clearance "
        "before any repatriation can proceed."
    ),
    ('philippines', 'united-states'): (
        "Filipino-American communities are among the largest diaspora groups in the United States. "
        "The Philippines-to-USA corridor is well-established, with direct cargo connections from "
        "Manila to major US cities. Documentation is in Filipino and English, which simplifies "
        "the translation requirement."
    ),
    ('india', 'united-states'): (
        "The Indian-American diaspora is one of the largest in the United States. "
        "Repatriation from India to the US occurs when an Indian-American dies during a "
        "visit home, or when a US-based person with Indian heritage needs remains returned. "
        "Documentation in India is complex and requires certified translation."
    ),
    ('china', 'united-states'): (
        "Chinese-American communities across California, New York, and Texas account for "
        "significant repatriation volume on this corridor. Chinese documentation is complex "
        "and requires certified English translation at each stage."
    ),
    ('el-salvador', 'united-states'): (
        "Salvadoran-American communities in Los Angeles, Houston, and Washington DC account "
        "for substantial repatriation volume on this corridor. El Salvador's documentation "
        "process is managed through the Registro Nacional de las Personas Naturales."
    ),
    ('dominican-republic', 'united-states'): (
        "Dominican-American communities, concentrated in New York and New Jersey, generate "
        "significant repatriation demand on this corridor. The Dominican Republic has a "
        "well-established repatriation industry given the volume of cases."
    ),
    ('vietnam', 'united-states'): (
        "Vietnamese-American communities across California, Texas, and Virginia account for "
        "substantial repatriation volume on this corridor. Vietnamese documentation requires "
        "certified English translation and official authentication."
    ),
    ('cuba', 'united-states'): (
        "Cuban-American communities, particularly in Florida, account for repatriation demand "
        "on this corridor. The US Embassy in Havana provides limited consular services. "
        "Documentation requirements have become more established in recent years."
    ),
    ('south-korea', 'united-states'): (
        "Korean-American communities across California, New York, and New Jersey account for "
        "consistent repatriation demand on this corridor. South Korea has a well-organised "
        "system for handling international repatriation cases."
    ),
    ('guatemala', 'united-states'): (
        "Guatemalan-American communities across California, Florida, and Texas account for "
        "significant repatriation demand. Guatemala's documentation process runs through the "
        "Registro Civil and requires certified English translation."
    ),
    ('jamaica', 'united-states'): (
        "Jamaican-American communities in New York, Florida, and Connecticut generate "
        "consistent repatriation demand on this corridor. Jamaica has a well-established "
        "process for international repatriation, with direct air links to US cities."
    ),
    ('haiti', 'united-states'): (
        "Haitian-American communities in Florida, New York, and Massachusetts account for "
        "significant repatriation demand. Haiti's documentation process can be affected by "
        "administrative capacity; a specialist is particularly important on this corridor."
    ),
    ('colombia', 'united-states'): (
        "Colombian-American communities in Florida, New York, and New Jersey account for "
        "consistent repatriation demand. Colombia has established procedures for international "
        "repatriation, managed through the Notaria and the Colombian civil registry."
    ),
    ('nigeria', 'united-states'): (
        "Nigerian-American communities across Texas, Maryland, Georgia, and New York account "
        "for significant repatriation demand on this corridor. Nigeria's documentation process "
        "requires engagement with state government authorities and the National Population Commission."
    ),
    ('pakistan', 'united-states'): (
        "Pakistani-American communities across New York, Chicago, and Texas account for "
        "consistent repatriation demand on this corridor. Pakistan's documentation process "
        "is well-established given the volume of overseas Pakistani nationals."
    ),
    ('brazil', 'united-states'): (
        "Brazilian-American communities in Florida, New York, and Massachusetts account for "
        "growing repatriation demand. Brazil's documentation is in Portuguese and requires "
        "certified English translation. São Paulo and Rio de Janeiro have international cargo connections."
    ),
    ('honduras', 'united-states'): (
        "Honduran-American communities across California, New York, and Florida account for "
        "significant repatriation demand. Honduras's documentation process runs through "
        "the Registro Nacional de las Personas."
    ),
    ('ecuador', 'united-states'): (
        "Ecuadorian-American communities in New York and New Jersey account for consistent "
        "repatriation demand. Ecuador has direct air links to the US and established procedures "
        "for international repatriation through the Registro Civil."
    ),
    ('ethiopia', 'united-states'): (
        "Ethiopian-American communities across Washington DC, Minnesota, and California "
        "account for significant repatriation demand. Ethiopia's Amharic documentation "
        "requires certified English translation."
    ),
    ('ghana', 'united-states'): (
        "Ghanaian-American communities in New York, Washington DC, and New Jersey generate "
        "consistent repatriation demand. Ghana has established procedures for repatriation "
        "of diaspora members, and the documentation process is relatively well-mapped."
    ),
    ('ukraine', 'united-states'): (
        "Ukrainian-American communities, particularly in New York, Pennsylvania, and Illinois, "
        "account for consistent repatriation demand. Ukraine's documentation process is managed "
        "through the civil registry (DRACS) and requires certified English translation."
    ),
    ('iran', 'united-states'): (
        "Iranian-American communities across California and New York account for repatriation "
        "demand on this corridor. The absence of a US Embassy in Iran means consular assistance "
        "is handled through third-party channels; a specialist is particularly important."
    ),
    ('peru', 'united-states'): (
        "Peruvian-American communities in Florida, New Jersey, and California generate "
        "consistent repatriation demand. Peru's documentation runs through the Registro Nacional "
        "de Identificacion y Estado Civil (RENIEC) and requires certified English translation."
    ),
    ('cambodia', 'united-states'): (
        "Cambodian-American communities in California and Massachusetts account for "
        "repatriation demand on this corridor. Cambodia's documentation process requires "
        "certified English translation and coordination with the Ministry of Interior."
    ),
    ('trinidad-and-tobago', 'united-states'): (
        "Trinidadian and Tobagonian communities in New York and Florida account for "
        "consistent repatriation demand. Trinidad and Tobago has well-established "
        "processes for international repatriation, with direct air links to US cities."
    ),
    # To UAE
    ('india', 'united-arab-emirates'): (
        "The Indian community is the largest expatriate group in the UAE. "
        "This corridor handles the return of remains when an Indian family member in the UAE "
        "has a loved one die in India. Documentation must be attested by the UAE Embassy in "
        "India before departure."
    ),
    ('pakistan', 'united-arab-emirates'): (
        "Pakistani nationals form one of the largest communities in the UAE. "
        "When a UAE-based Pakistani worker has a family member die in Pakistan, "
        "repatriation of remains to the UAE follows an established documentation pathway "
        "through the UAE Embassy in Islamabad."
    ),
    ('bangladesh', 'united-arab-emirates'): (
        "Bangladeshi nationals are among the largest worker communities in the UAE. "
        "This corridor manages the return of remains when a UAE-based Bangladeshi national "
        "loses a family member in Bangladesh. Documentation must be attested by the UAE "
        "Embassy in Dhaka."
    ),
    ('philippines', 'united-arab-emirates'): (
        "Filipino nationals form a significant community across the UAE. "
        "This corridor handles cases where a UAE-based Filipino has a family member "
        "die in the Philippines and needs remains brought to the UAE. "
        "The Philippines has established government support for overseas workers."
    ),
    ('egypt', 'united-arab-emirates'): (
        "Egyptian nationals form a substantial community in the UAE, particularly in Dubai "
        "and Abu Dhabi. This corridor handles repatriation of remains from Egypt to the UAE "
        "for family members of UAE-based Egyptians."
    ),
    ('nepal', 'united-arab-emirates'): (
        "Nepali nationals work in large numbers across the UAE. "
        "This corridor handles cases where a UAE-based Nepali national has a family member "
        "die in Nepal and needs remains brought to the UAE for burial or cremation."
    ),
    ('sri-lanka', 'united-arab-emirates'): (
        "Sri Lankan nationals form a significant worker community in the UAE. "
        "This corridor handles cases where a UAE-based Sri Lankan has a family member die "
        "in Sri Lanka and needs remains returned to the UAE."
    ),
    ('jordan', 'united-arab-emirates'): (
        "Jordanian nationals form a professional community in the UAE. "
        "This corridor handles repatriation of remains from Jordan to the UAE for families "
        "of UAE-based Jordanians. Documentation includes UAE Embassy attestation in Amman."
    ),
    ('kenya', 'united-arab-emirates'): (
        "Kenyan nationals work across the UAE in various sectors. "
        "This corridor handles cases where a UAE-based Kenyan national needs remains "
        "of a family member brought from Kenya to the UAE."
    ),
    ('ethiopia', 'united-arab-emirates'): (
        "Ethiopian nationals form part of the UAE's diverse worker community. "
        "This corridor handles repatriation of remains from Ethiopia to the UAE, "
        "typically for family members of UAE-based Ethiopians."
    ),
    ('indonesia', 'united-arab-emirates'): (
        "Indonesian nationals work across the UAE. This corridor handles cases "
        "where a UAE-based Indonesian has a family member die in Indonesia and "
        "needs remains brought to the UAE. Indonesia has government support structures "
        "for overseas workers in repatriation cases."
    ),
    ('morocco', 'united-arab-emirates'): (
        "Moroccan nationals form part of the UAE's diverse expatriate community. "
        "This corridor handles repatriation of remains from Morocco to the UAE for "
        "family members of UAE-based Moroccans."
    ),
    # To Saudi Arabia
    ('pakistan', 'saudi-arabia'): (
        "Pakistani nationals form one of the largest expatriate communities in Saudi Arabia. "
        "This corridor handles cases where a Saudi-based Pakistani national has a family member "
        "die in Pakistan and needs remains brought back to Saudi Arabia. "
        "This is one of the highest-volume South Asia to Gulf repatriation corridors."
    ),
    ('india', 'saudi-arabia'): (
        "Indian nationals form the largest single expatriate group in Saudi Arabia. "
        "This corridor handles cases where a Saudi-based Indian national has a family member "
        "die in India and needs remains brought to Saudi Arabia. Documentation requires "
        "Saudi Embassy attestation from New Delhi, Mumbai, Chennai, or Kolkata."
    ),
    ('bangladesh', 'saudi-arabia'): (
        "Bangladeshi nationals work in large numbers across Saudi Arabia. "
        "This corridor handles cases where a Saudi-based Bangladeshi national has a family "
        "member die in Bangladesh and needs remains brought to Saudi Arabia."
    ),
    ('philippines', 'saudi-arabia'): (
        "Filipino nationals work across Saudi Arabia in professional and domestic roles. "
        "This corridor handles cases where a Saudi-based Filipino has a family member die "
        "in the Philippines and needs remains brought to Saudi Arabia. The Philippines "
        "has government support structures for overseas workers."
    ),
    ('indonesia', 'saudi-arabia'): (
        "Indonesian nationals work in Saudi Arabia in significant numbers. "
        "This corridor handles cases where a Saudi-based Indonesian has a family member "
        "die in Indonesia and needs remains brought to Saudi Arabia."
    ),
    ('egypt', 'saudi-arabia'): (
        "Egyptian nationals form one of the largest Arab expatriate communities in Saudi Arabia. "
        "This corridor handles repatriation of remains from Egypt to Saudi Arabia for "
        "families of Saudi-based Egyptians."
    ),
    ('nepal', 'saudi-arabia'): (
        "Nepali nationals work in Saudi Arabia in substantial numbers. "
        "This corridor handles cases where a Saudi-based Nepali national has a family member "
        "die in Nepal and needs remains brought to Saudi Arabia."
    ),
    ('ethiopia', 'saudi-arabia'): (
        "Ethiopian nationals work in Saudi Arabia in domestic and service roles. "
        "This corridor handles cases where a Saudi-based Ethiopian has a family member "
        "die in Ethiopia and needs remains brought to Saudi Arabia."
    ),
    ('jordan', 'saudi-arabia'): (
        "Jordanian nationals work as professionals across Saudi Arabia. "
        "This corridor handles cases where a Saudi-based Jordanian has a family member "
        "die in Jordan and needs remains brought to Saudi Arabia."
    ),
    ('kenya', 'saudi-arabia'): (
        "Kenyan nationals work in Saudi Arabia across various sectors. "
        "This corridor handles cases where a Saudi-based Kenyan has a family member "
        "die in Kenya and needs remains brought to Saudi Arabia."
    ),
    ('sri-lanka', 'saudi-arabia'): (
        "Sri Lankan nationals form part of Saudi Arabia's expatriate worker community. "
        "This corridor handles repatriation of remains from Sri Lanka to Saudi Arabia "
        "for families of Saudi-based Sri Lankans."
    ),
    ('ghana', 'saudi-arabia'): (
        "Ghanaian nationals work in Saudi Arabia in various professional roles. "
        "This corridor handles cases where a Saudi-based Ghanaian has a family member "
        "die in Ghana and needs remains brought to Saudi Arabia."
    ),
    ('nigeria', 'saudi-arabia'): (
        "Nigerian nationals work in Saudi Arabia in professional and technical roles. "
        "This corridor handles cases where a Saudi-based Nigerian has a family member "
        "die in Nigeria and needs remains brought to Saudi Arabia."
    ),
    ('yemen', 'saudi-arabia'): (
        "Yemeni nationals have historically formed part of Saudi Arabia's worker community. "
        "This corridor handles repatriation of remains from Yemen to Saudi Arabia. "
        "The ongoing conflict in Yemen has added complexity to documentation and logistics."
    ),
    # To Germany
    ('turkey', 'germany'): (
        "Turkish nationals form the largest non-EU migrant community in Germany. "
        "This is one of the highest-volume European repatriation corridors. "
        "Turkish-Germans whose family members die in Turkey need remains brought to Germany, "
        "typically via Frankfurt or Munich cargo terminals."
    ),
    ('poland', 'germany'): (
        "Polish nationals form one of the largest EU migrant groups in Germany. "
        "This corridor handles cases where a Germany-based Pole has a family member "
        "die in Poland and needs remains brought to Germany. The EU regulatory framework "
        "simplifies some documentation requirements."
    ),
    ('russia', 'germany'): (
        "Russian nationals form a significant community in Germany. "
        "This corridor handles cases where a Germany-based Russian has a family member "
        "die in Russia and needs remains brought to Germany. Note that diplomatic relations "
        "have been significantly affected since 2022."
    ),
    ('romania', 'germany'): (
        "Romanian nationals form one of the largest EU migrant communities in Germany. "
        "This corridor handles cases where a Germany-based Romanian has a family member "
        "die in Romania and needs remains brought to Germany."
    ),
    ('italy', 'germany'): (
        "Italian nationals work in Germany as part of the long-established EU freedom of movement. "
        "This corridor handles cases where a Germany-based Italian has a family member "
        "die in Italy and needs remains brought to Germany."
    ),
    ('serbia', 'germany'): (
        "Serbian nationals form a significant community in Germany, particularly in Bavaria "
        "and Baden-Wurttemberg. This corridor handles cases where a Germany-based Serb "
        "has a family member die in Serbia and needs remains brought to Germany."
    ),
    ('ukraine', 'germany'): (
        "Ukrainian nationals have formed a large community in Germany, particularly since 2022. "
        "This corridor handles cases where a Germany-based Ukrainian has a family member die "
        "in Ukraine and needs remains brought to Germany."
    ),
    ('iraq', 'germany'): (
        "Iraqi nationals form a significant community in Germany. "
        "This corridor handles cases where a Germany-based Iraqi has a family member die "
        "in Iraq and needs remains brought to Germany. Documentation requires certified "
        "German translation from Arabic."
    ),
    ('morocco', 'germany'): (
        "Moroccan nationals form part of Germany's North African diaspora community. "
        "This corridor handles repatriation of remains from Morocco to Germany for "
        "families of Germany-based Moroccans."
    ),
    ('ghana', 'germany'): (
        "Ghanaian nationals form part of Germany's sub-Saharan African community. "
        "This corridor handles cases where a Germany-based Ghanaian has a family member "
        "die in Ghana and needs remains brought to Germany."
    ),
    ('nigeria', 'germany'): (
        "Nigerian nationals form a growing community in Germany. "
        "This corridor handles cases where a Germany-based Nigerian has a family member "
        "die in Nigeria and needs remains brought to Germany."
    ),
    ('vietnam', 'germany'): (
        "Vietnamese nationals form one of the larger Asian diaspora communities in Germany, "
        "particularly in former East Germany. This corridor handles cases where a "
        "Germany-based Vietnamese has a family member die in Vietnam and needs remains "
        "brought to Germany."
    ),
    ('afghanistan', 'germany'): (
        "Afghan nationals form a significant community in Germany. "
        "This corridor handles cases where a Germany-based Afghan has a family member "
        "die in Afghanistan and needs remains brought to Germany. The situation in "
        "Afghanistan since 2021 requires specialist coordination."
    ),
    # To France
    ('morocco', 'france'): (
        "Moroccan nationals form the largest North African diaspora community in France. "
        "This is one of the highest-volume repatriation corridors between France and North Africa. "
        "Documentation requires certified French translation and official apostille or legalisation."
    ),
    ('algeria', 'france'): (
        "Algerian nationals form a major diaspora community in France. "
        "This corridor handles cases where a France-based Algerian has a family member "
        "die in Algeria and needs remains brought to France. The France-Algeria corridor "
        "is one of the highest-volume in Europe."
    ),
    ('tunisia', 'france'): (
        "Tunisian nationals form part of France's large North African diaspora. "
        "This corridor handles repatriation of remains from Tunisia to France for "
        "families of France-based Tunisians."
    ),
    ('portugal', 'france'): (
        "Portuguese nationals are among the oldest and largest EU migrant communities in France. "
        "This corridor handles cases where a France-based Portuguese has a family member "
        "die in Portugal and needs remains brought to France. EU documentation simplifies "
        "some requirements."
    ),
    ('senegal', 'france'): (
        "Senegalese nationals form part of France's significant West African diaspora. "
        "This corridor handles cases where a France-based Senegalese has a family member "
        "die in Senegal and needs remains brought to France."
    ),
    ('ivory-coast', 'france'): (
        "Ivorian nationals form part of France's West African diaspora community. "
        "This corridor handles repatriation of remains from Ivory Coast to France for "
        "families of France-based Ivorians."
    ),
    ('cameroon', 'france'): (
        "Cameroonian nationals form part of France's Central African diaspora community. "
        "Cameroon's French-speaking population means documentation is already in French, "
        "which simplifies one requirement on this corridor."
    ),
    ('mali', 'france'): (
        "Malian nationals form part of France's West African diaspora. "
        "This corridor handles repatriation of remains from Mali to France for "
        "families of France-based Malians. Note that the situation in Mali since 2021 "
        "requires specialist coordination in some cases."
    ),
    ('guinea', 'france'): (
        "Guinean nationals form part of France's West African diaspora community. "
        "This corridor handles cases where a France-based Guinean has a family member "
        "die in Guinea and needs remains brought to France."
    ),
    ('congo', 'france'): (
        "Congolese nationals (Republic of the Congo) form part of France's "
        "Central African diaspora. This corridor handles repatriation of remains from "
        "the Congo to France for families of France-based Congolese nationals."
    ),
    ('madagascar', 'france'): (
        "Malagasy nationals form part of France's Indian Ocean diaspora. "
        "This corridor handles repatriation of remains from Madagascar to France for "
        "families of France-based Malagasy nationals. French is widely used in Madagascar, "
        "which simplifies documentation translation."
    ),
    ('haiti', 'france'): (
        "Haitian nationals form a significant community in France, particularly in Paris "
        "and overseas territories. French documentation requirements are simplified since "
        "Haiti uses French, but the administrative capacity in Haiti can affect timelines."
    ),
    # To Canada
    ('india', 'canada'): (
        "Indian-Canadians form one of the largest South Asian diaspora groups in Canada. "
        "This corridor handles cases where a Canada-based Indian has a family member die "
        "in India and needs remains brought to Canada. Indian documentation requires "
        "certified English translation."
    ),
    ('philippines', 'canada'): (
        "Filipino-Canadians form a significant diaspora community. "
        "This corridor handles cases where a Canada-based Filipino has a family member "
        "die in the Philippines and needs remains brought to Canada."
    ),
    ('china', 'canada'): (
        "Chinese-Canadians form one of the largest Asian diaspora groups in Canada. "
        "This corridor handles cases where a Canada-based Chinese national has a family "
        "member die in China and needs remains brought to Canada. Documentation requires "
        "certified English translation."
    ),
    ('pakistan', 'canada'): (
        "Pakistani-Canadians form a significant South Asian community in Canada. "
        "This corridor handles cases where a Canada-based Pakistani has a family member "
        "die in Pakistan and needs remains brought to Canada."
    ),
    ('nigeria', 'canada'): (
        "Nigerian-Canadians form a growing community across Ontario and British Columbia. "
        "This corridor handles cases where a Canada-based Nigerian has a family member "
        "die in Nigeria and needs remains brought to Canada."
    ),
    ('ukraine', 'canada'): (
        "Ukrainian-Canadians form a significant and historic community in Canada, particularly "
        "in the Prairie provinces. This corridor handles cases where a Canada-based Ukrainian "
        "has a family member die in Ukraine and needs remains brought to Canada."
    ),
    ('south-korea', 'canada'): (
        "Korean-Canadians form a significant community in British Columbia and Ontario. "
        "This corridor handles cases where a Canada-based Korean has a family member "
        "die in South Korea and needs remains brought to Canada."
    ),
    ('iran', 'canada'): (
        "Iranian-Canadians form one of the larger Middle Eastern diaspora communities in Canada. "
        "This corridor handles cases where a Canada-based Iranian has a family member die "
        "in Iran and needs remains brought to Canada. Canada closed its embassy in Tehran in 2012; "
        "the Italian Embassy handles Canadian consular interests there."
    ),
    # To Australia
    ('india', 'australia'): (
        "Indian-Australians form one of the largest South Asian communities in Australia. "
        "This corridor handles cases where an Australia-based Indian has a family member die "
        "in India and needs remains brought to Australia. Indian documentation requires "
        "certified English translation."
    ),
    ('china', 'australia'): (
        "Chinese-Australians form one of the largest Asian communities in Australia. "
        "This corridor handles cases where an Australia-based Chinese national has a family "
        "member die in China and needs remains brought to Australia. Documentation requires "
        "certified English translation."
    ),
    ('philippines', 'australia'): (
        "Filipino-Australians form a significant community in Australia. "
        "This corridor handles cases where an Australia-based Filipino has a family member "
        "die in the Philippines and needs remains brought to Australia."
    ),
    ('vietnam', 'australia'): (
        "Vietnamese-Australians form a significant community in Australia. "
        "This corridor handles cases where an Australia-based Vietnamese has a family member "
        "die in Vietnam and needs remains brought to Australia. Documentation requires "
        "certified English translation."
    ),
    ('malaysia', 'australia'): (
        "Malaysian nationals study and work in Australia in significant numbers. "
        "This corridor handles cases where an Australia-based Malaysian has a family member "
        "die in Malaysia and needs remains brought to Australia."
    ),
    ('south-korea', 'australia'): (
        "Korean-Australians form a significant community in New South Wales and Victoria. "
        "This corridor handles cases where an Australia-based Korean has a family member "
        "die in South Korea and needs remains brought to Australia."
    ),
    ('new-zealand', 'australia'): (
        "New Zealanders are the largest group of permanent migrants in Australia. "
        "This corridor handles cases where an Australia-based New Zealander has a family "
        "member die in New Zealand and needs remains brought to Australia. The CER agreement "
        "and shared administrative traditions simplify some requirements."
    ),
    ('indonesia', 'australia'): (
        "Indonesian nationals work and study in Australia in significant numbers. "
        "This corridor handles cases where an Australia-based Indonesian has a family "
        "member die in Indonesia and needs remains brought to Australia. Documentation "
        "requires certified English translation."
    ),
    ('nepal', 'australia'): (
        "Nepali nationals form a growing community in Australia, particularly in higher "
        "education. This corridor handles cases where an Australia-based Nepali has a family "
        "member die in Nepal and needs remains brought to Australia."
    ),
    # To India
    ('bangladesh', 'india'): (
        "This corridor handles cases where an India-based Bangladeshi or a person with family "
        "in India has a loved one die in Bangladesh and needs remains brought to India. "
        "The close geographic and cultural ties between Bangladesh and India make this "
        "an established bilateral repatriation route."
    ),
    ('nepal', 'india'): (
        "Nepali nationals form one of the largest migrant communities in India. "
        "This corridor handles cases where an India-based Nepali family member needs "
        "remains of a loved one brought from Nepal to India."
    ),
    ('singapore', 'india'): (
        "This corridor handles cases where an India-based person has a family member die "
        "in Singapore and needs remains brought to India. Singapore has a significant "
        "Indian diaspora, and repatriation in both directions is common."
    ),
    ('malaysia', 'india'): (
        "Malaysian nationals of Indian heritage form a significant community. "
        "This corridor handles cases where an India-based person has a family member die "
        "in Malaysia and needs remains brought to India."
    ),
    ('united-states', 'india'): (
        "This corridor handles cases where an India-based person has a family member die "
        "in the United States and needs remains brought to India. Indian-Americans who "
        "pass away in the US are frequently repatriated to India for funeral rites."
    ),
    ('canada', 'india'): (
        "This corridor handles cases where an India-based person has a family member die "
        "in Canada and needs remains brought to India. Indian-Canadians who pass away in "
        "Canada are frequently repatriated to India for funeral rites."
    ),
    ('australia', 'india'): (
        "This corridor handles cases where an India-based person has a family member die "
        "in Australia and needs remains brought to India. Indian-Australians who pass away "
        "in Australia are frequently repatriated to India for Hindu or Sikh funeral rites."
    ),
    ('united-arab-emirates', 'india'): (
        "Indian nationals form the largest expatriate group in the UAE. "
        "When an Indian expat dies in the UAE, their family in India often needs remains "
        "returned to India for funeral rites. This is one of the highest-volume Gulf-to-India "
        "repatriation corridors."
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

    # Destination embassy city in origin country
    dest_embassy_city = EMBASSY_CITIES.get((origin_slug, dest_slug), uk_embassy_city or 'the capital')

    # Corridor intro
    intro = CORRIDOR_INTRO.get(
        (origin_slug, dest_slug),
        (
            f"Repatriation from {origin_name} to {dest_name} occurs when a {dest_name}-based "
            f"family has a loved one die in {origin_name} and needs remains returned. "
            f"This corridor follows {origin_name}'s standard export procedures for "
            f"international repatriation of human remains."
        )
    )

    # Title and description
    title = f"{origin_name} to {dest_name}: Repatriation Guidance"
    if len(title) > 60:
        title = f"{origin_name} to {dest_name} Repatriation Guide"
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

    # Direct answer heading
    direct_answer_heading = f'direct_answer_heading: "Repatriation from {origin_name} to {dest_name}: what to expect"'

    # Direct answer intro
    direct_answer_intro = f'direct_answer_intro: "{intro}"'

    # Extract origin doc info from UK file for direct_answer_points
    dap_raw = extract_block(uk_fm, 'direct_answer_points', ['overview_heading', 'dest_reception', 'date'])
    # Replace UK-specific references in the points
    dap = dap_raw
    dap = re.sub(r'British Embassy[^"]*advises?\.[^"]*Cannot fund repatriation\.', '', dap)
    dap = re.sub(r'British High Commission[^"]*advises?\.[^"]*Cannot fund repatriation\.', '', dap)
    dap = re.sub(r'FCDO[^"]*emergency line[^"]*\.',
                 f'{dest_name} Embassy in {dest_embassy_city} can advise. They cannot fund repatriation.',
                 dap)
    # Replace generic UK destination references
    dap = dap.replace('for UK acceptance', f'for {dest_name} acceptance')
    dap = dap.replace('UK funeral director', f'{dest_name} funeral director')
    dap = dap.replace('United Kingdom acceptance', f'{dest_name} acceptance')
    # Ensure last point mentions destination consular
    if 'Embassy' not in dap or dest_name not in dap:
        dap = dap.rstrip()
        dap += f'\n  - "{dest_name} Embassy in {dest_embassy_city} can advise on documentation. They cannot fund repatriation."'

    # Overview: keep from UK file (origin-specific process)
    overview_heading_raw = extract_block(uk_fm, 'overview_heading', ['overview_body'])
    overview_body_raw = extract_block(uk_fm, 'overview_body', ['dest_reception', 'dest_consular'])
    # Minimal adaptation for overview
    overview_heading = overview_heading_raw
    overview_body = overview_body_raw
    # Remove UK-centric references from overview body
    overview_body = re.sub(r'British Embassy[^.]+\.', '', overview_body)
    overview_body = re.sub(r'FCDO[^.]+\.', '', overview_body)

    # Destination reception and consular
    dest_reception_text = dest['reception']
    consular_template = dest['consular_template']
    dest_consular_text = consular_template.format(
        city=dest_embassy_city,
        country_name=origin_name,
    )

    # Timeline steps: adapt from UK file
    ts_raw = extract_block(uk_fm, 'timeline_steps', ['faqs', 'links'])
    ts = ts_raw
    # Step 3: update embassy reference
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
    # Step 6: update destination
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
    # Step 1: update FCDO reference
    ts = re.sub(
        r'FCDO 24hr: \+44 \(0\)20 7008 5000\.',
        f'Call +44 (0)20 7008 5000 (FCDO) or {dest["emergency_line"]}.',
        ts
    )
    # Step 7: update receiving director
    ts = ts.replace('UK funeral director takes custody', f'{dest_name} funeral director takes custody')
    ts = ts.replace('United Kingdom funeral director takes custody', f'{dest_name} funeral director takes custody')
    ts = ts.replace('Coroner notified', 'receiving funeral director coordinates with local authorities')
    # Remove remaining FCDO/UK references
    ts = re.sub(r'FCDO 24hr:[^\n"]+', f'{dest["emergency_line"]}', ts)

    # FAQs: adapt from UK file
    faqs_raw = extract_block(uk_fm, 'faqs', ['links'])
    faqs = faqs_raw

    # Update "How long does repatriation from X to UK take?" FAQ
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
    # Update answer references to "UK"
    faqs = faqs.replace('repatriation from ' + origin_name + ' to the UK takes',
                        f'repatriation from {origin_name} to {dest_name} takes')
    faqs = faqs.replace('repatriation from ' + origin_name + ' to United Kingdom takes',
                        f'repatriation from {origin_name} to {dest_name} takes')
    faqs = faqs.replace('repatriation from ' + origin_name + ' to the United Kingdom takes',
                        f'repatriation from {origin_name} to {dest_name} takes')

    # Update embassy FAQ
    embassy_faq_q1 = f'Does the British Embassy in {origin_name} help with repatriation?'
    embassy_faq_q2 = f'Is there a British Embassy in {origin_name}?'
    embassy_faq_q3 = f'Does the British High Commission in {origin_name} help with repatriation?'

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
    # Fallback: simpler pattern
    for q in [embassy_faq_q1, embassy_faq_q2, embassy_faq_q3]:
        if q in faqs:
            # Replace the whole FAQ block
            pattern = rf'  - question: "{re.escape(q)}"\n    answer: "[^"]*"'
            faqs = re.sub(pattern, new_embassy_faq, faqs)

    # Update "what happens when body arrives in UK" FAQ
    faqs = re.sub(
        r'  - question: "What happens when the body arrives in (?:the )?(?:United Kingdom|UK)\?"\n    answer: "[^"]*"',
        f'  - question: "What happens when the body arrives in {dest_name}?"\n    answer: "{dest["arrival_faq"]}"',
        faqs
    )

    # Remove any remaining UK/FCDO references in answers
    faqs = faqs.replace('UK funeral director', f'{dest_name} funeral director')
    faqs = faqs.replace('United Kingdom funeral director', f'{dest_name} funeral director')
    faqs = faqs.replace('FCDO 24-hour emergency line: +44 (0)20 7008 5000', dest_consular_text[:80])
    faqs = faqs.replace('FCDO emergency line', dest['emergency_line'])
    faqs = faqs.replace('UK coroner', f'{dest_name} receiving authority')
    faqs = faqs.replace('the coroner for the district', f'the receiving authority in {dest_name}')
    faqs = faqs.replace('the Coroner for the district', f'the receiving authority in {dest_name}')

    # Links
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

    # Build final content
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
    # Safety: strip any em dashes that crept in
    content = content.replace('—', ',')
    content = content.replace('--', ',')

    return content


# ---------------------------------------------------------------------------
# Route list: 4 blocks of 25 = 100 routes
# Template rotation starts at D (index 3), from R13's last variant C.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # Block R14: 25 routes to United States
    ('mexico', 'united-states'),
    ('philippines', 'united-states'),
    ('india', 'united-states'),
    ('china', 'united-states'),
    ('el-salvador', 'united-states'),
    ('dominican-republic', 'united-states'),
    ('vietnam', 'united-states'),
    ('cuba', 'united-states'),
    ('south-korea', 'united-states'),
    ('guatemala', 'united-states'),
    ('jamaica', 'united-states'),
    ('haiti', 'united-states'),
    ('colombia', 'united-states'),
    ('nigeria', 'united-states'),
    ('pakistan', 'united-states'),
    ('brazil', 'united-states'),
    ('honduras', 'united-states'),
    ('ecuador', 'united-states'),
    ('ethiopia', 'united-states'),
    ('ghana', 'united-states'),
    ('ukraine', 'united-states'),
    ('iran', 'united-states'),
    ('peru', 'united-states'),
    ('cambodia', 'united-states'),
    ('trinidad-and-tobago', 'united-states'),
    # Block R15: 25 routes to UAE (12) and Saudi Arabia (13)
    ('india', 'united-arab-emirates'),
    ('pakistan', 'united-arab-emirates'),
    ('bangladesh', 'united-arab-emirates'),
    ('philippines', 'united-arab-emirates'),
    ('egypt', 'united-arab-emirates'),
    ('nepal', 'united-arab-emirates'),
    ('sri-lanka', 'united-arab-emirates'),
    ('jordan', 'united-arab-emirates'),
    ('kenya', 'united-arab-emirates'),
    ('ethiopia', 'united-arab-emirates'),
    ('indonesia', 'united-arab-emirates'),
    ('morocco', 'united-arab-emirates'),
    ('pakistan', 'saudi-arabia'),
    ('india', 'saudi-arabia'),
    ('bangladesh', 'saudi-arabia'),
    ('philippines', 'saudi-arabia'),
    ('indonesia', 'saudi-arabia'),
    ('egypt', 'saudi-arabia'),
    ('nepal', 'saudi-arabia'),
    ('ethiopia', 'saudi-arabia'),
    ('jordan', 'saudi-arabia'),
    ('kenya', 'saudi-arabia'),
    ('sri-lanka', 'saudi-arabia'),
    ('ghana', 'saudi-arabia'),
    ('nigeria', 'saudi-arabia'),
    # Block R16: 25 routes to Germany (13) and France (12)
    ('turkey', 'germany'),
    ('poland', 'germany'),
    ('russia', 'germany'),
    ('romania', 'germany'),
    ('italy', 'germany'),
    ('serbia', 'germany'),
    ('ukraine', 'germany'),
    ('iraq', 'germany'),
    ('morocco', 'germany'),
    ('ghana', 'germany'),
    ('nigeria', 'germany'),
    ('vietnam', 'germany'),
    ('afghanistan', 'germany'),
    ('morocco', 'france'),
    ('algeria', 'france'),
    ('tunisia', 'france'),
    ('portugal', 'france'),
    ('senegal', 'france'),
    ('ivory-coast', 'france'),
    ('cameroon', 'france'),
    ('mali', 'france'),
    ('guinea', 'france'),
    ('congo', 'france'),
    ('madagascar', 'france'),
    ('haiti', 'france'),
    # Block R17: 25 routes to Canada (8), Australia (9), India (8)
    ('india', 'canada'),
    ('philippines', 'canada'),
    ('china', 'canada'),
    ('pakistan', 'canada'),
    ('nigeria', 'canada'),
    ('ukraine', 'canada'),
    ('south-korea', 'canada'),
    ('iran', 'canada'),
    ('india', 'australia'),
    ('china', 'australia'),
    ('philippines', 'australia'),
    ('vietnam', 'australia'),
    ('malaysia', 'australia'),
    ('south-korea', 'australia'),
    ('new-zealand', 'australia'),
    ('indonesia', 'australia'),
    ('nepal', 'australia'),
    ('bangladesh', 'india'),
    ('nepal', 'india'),
    ('singapore', 'india'),
    ('malaysia', 'india'),
    ('united-states', 'india'),
    ('canada', 'india'),
    ('australia', 'india'),
    ('united-arab-emirates', 'india'),
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

# Summary
print(f"\n--- GENERATION SUMMARY ---")
print(f"Generated: {len(generated)}")
print(f"Skipped:   {len(skipped)}")
print(f"Errors:    {len(errors)}")
if errors:
    print(f"ERROR LIST: {errors}")

# Block breakdown
blocks = {
    'R14 (to USA)': [(o, d) for o, d in generated if d.endswith('united-states')],
    'R15 (to UAE/SA)': [(o, d) for o, d in generated if any(d.endswith(x) for x in ['united-arab-emirates', 'saudi-arabia'])],
    'R16 (to DE/FR)': [(o, d) for o, d in generated if any(d.endswith(x) for x in ['germany', 'france'])],
    'R17 (to CA/AU/IN)': [(o, d) for o, d in generated if any(d.endswith(x) for x in ['canada', 'australia', 'india'])],
}
for block, routes in blocks.items():
    print(f"  {block}: {len(routes)} routes, variants {','.join(set(v for _, v in routes))}")
