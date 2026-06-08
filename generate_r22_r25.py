#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R22-R25.
   R22: Italy x7 + Spain x7 + Netherlands x6 + Belgium x5 = 25
   R23: Italy x5 + Spain x5 + Netherlands x5 + Belgium x5 + USA wave 3 x5 = 25
   R24: UAE wave 3 x5 + Germany wave 3 x5 + France wave 3 x5 + Canada wave 3 x5 + Australia wave 3 x5 = 25
   R25: India wave 3 x5 + Singapore wave 2 x5 + Qatar wave 2 x5 + Kuwait wave 2 x5 + South Africa wave 2 x5 = 25
   Template rotation continues from R21 last variant C, so R22 starts at D (index 3).
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

# R21 ended on variant C (index 2). R22 starts at D (index 3).
START_VARIANT = 3

# ---------------------------------------------------------------------------
# Destination hub metadata (inherited hubs + four new hubs)
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
    # --- New Tier B hubs (R22 onward) ---
    'italy': {
        'name': 'Italy',
        'slug': 'italy',
        'key': 'it',
        'reception': (
            "The Italian funeral director (impresa funebre) takes custody at the cargo terminal, "
            "typically Rome Fiumicino (FCO), Milan Malpensa (MXP), or another Italian international airport. "
            "A prefettura transport authorisation is required before burial or cremation. "
            "All foreign documents must carry a certified Italian translation. "
            "The local commune registers the death with the anagrafe (civil registry). "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
        'consular_template': (
            "Italian Embassy in {city} can advise on documentation requirements for repatriation to Italy. "
            "Italian Ministry of Foreign Affairs and International Cooperation (MAECI) emergency line: "
            "+39 06 3691 3691 (24 hours). The Italian Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Italian funeral director takes custody at the cargo terminal. "
            "A prefettura transport authorisation is required before burial or cremation can proceed. "
            "All foreign documents require certified Italian translation. "
            "The local commune registers the death with the anagrafe. "
            "The receiving funeral director coordinates with the prefettura and local authorities."
        ),
        'emergency_line': '+39 06 3691 3691',
        'hub_url': 'repatriation-from-italy',
    },
    'spain': {
        'name': 'Spain',
        'slug': 'spain',
        'key': 'es',
        'reception': (
            "The Spanish funeral director (empresa funeraria) takes custody at the cargo terminal, "
            "typically Madrid Barajas (MAD), Barcelona El Prat (BCN), or another Spanish airport. "
            "The Registro Civil registers the death. For deaths in the Canary or Balearic Islands, "
            "an internal mainland transfer is required before any international cargo flight departs. "
            "All foreign documents must carry a certified Spanish translation. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
        'consular_template': (
            "Spanish Embassy in {city} can advise on documentation requirements for repatriation to Spain. "
            "Spanish Ministry of Foreign Affairs emergency line: +34 91 379 9700 (24 hours). "
            "The Spanish Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Spanish funeral director takes custody at the cargo terminal. "
            "The Registro Civil registers the death. Island deaths require a mainland transfer first. "
            "Unexpected deaths may require a Juzgado de Instruccion investigation before release. "
            "All foreign documents require certified Spanish translation. "
            "The receiving funeral director coordinates with the Registro Civil and local health authorities."
        ),
        'emergency_line': '+34 91 379 9700',
        'hub_url': 'repatriation-from-spain',
    },
    'netherlands': {
        'name': 'Netherlands',
        'slug': 'netherlands',
        'key': 'nl',
        'reception': (
            "The Dutch funeral director (begrafenisondernemer or uitvaartondernemer) takes custody "
            "at Amsterdam Schiphol (AMS) or Rotterdam The Hague (RTM) cargo terminal. "
            "The local gemeente (municipality) registers the death with the Burgerlijke Stand (civil registry). "
            "A transport permit (laissez-passer) must accompany the remains. "
            "Foreign documents in languages other than Dutch, English, French, or German require certified translation. "
            "(Dutch Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Dutch Embassy in {city} can advise on documentation requirements for repatriation to the Netherlands. "
            "Dutch Ministry of Foreign Affairs emergency line: +31 70 348 6486 (24 hours). "
            "The Dutch Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Dutch funeral director takes custody at Amsterdam Schiphol (AMS) cargo terminal. "
            "A laissez-passer must accompany the remains. "
            "The local gemeente registers the death with the Burgerlijke Stand. "
            "Documents not in Dutch, English, French, or German require certified translation. "
            "The receiving funeral director coordinates with the gemeente and health authorities."
        ),
        'emergency_line': '+31 70 348 6486',
        'hub_url': 'repatriation-from-netherlands',
    },
    'belgium': {
        'name': 'Belgium',
        'slug': 'belgium',
        'key': 'be',
        'reception': (
            "The Belgian funeral director (entrepreneur des pompes funebres or begrafenisondernemer) "
            "takes custody at Brussels Airport (BRU) or Liege Airport (LGG) cargo terminal. "
            "The local commune or gemeente registers the death with the Registre de la Population. "
            "A transport authorisation is required before burial or cremation. "
            "All foreign documents must carry a certified French or Dutch translation. "
            "(Belgian Federal Public Service Foreign Affairs, FPS Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Belgian Embassy in {city} can advise on documentation requirements for repatriation to Belgium. "
            "Belgian Federal Public Service Foreign Affairs emergency line: +32 2 501 8111 (24 hours). "
            "The Belgian Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Belgian funeral director takes custody at Brussels Airport (BRU) cargo terminal. "
            "A transport authorisation is required before burial or cremation. "
            "The local commune or gemeente registers the death. "
            "All foreign documents require certified French or Dutch translation. "
            "The receiving funeral director coordinates with the commune and local health authorities."
        ),
        'emergency_line': '+32 2 501 8111',
        'hub_url': 'repatriation-from-belgium',
    },
}

# ---------------------------------------------------------------------------
# Embassy cities for new corridors (city of destination country embassy
# in the origin country)
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R22: Italy corridors
    ('morocco', 'italy'):       'Rabat',
    ('romania', 'italy'):       'Bucharest',
    ('albania', 'italy'):       'Tirana',
    ('china', 'italy'):         'Beijing',
    ('ukraine', 'italy'):       'Kyiv',
    ('philippines', 'italy'):   'Manila',
    ('bangladesh', 'italy'):    'Dhaka',
    # R22: Spain corridors
    ('morocco', 'spain'):             'Rabat',
    ('romania', 'spain'):             'Bucharest',
    ('colombia', 'spain'):            'Bogota',
    ('venezuela', 'spain'):           'Caracas',
    ('ecuador', 'spain'):             'Quito',
    ('china', 'spain'):               'Beijing',
    ('bolivia', 'spain'):             'La Paz',
    # R22: Netherlands corridors
    ('turkey', 'netherlands'):        'Ankara',
    ('morocco', 'netherlands'):       'Rabat',
    ('suriname', 'netherlands'):      'Paramaribo',
    ('indonesia', 'netherlands'):     'Jakarta',
    ('china', 'netherlands'):         'Beijing',
    ('india', 'netherlands'):         'New Delhi',
    # R22: Belgium corridors
    ('morocco', 'belgium'):                           'Rabat',
    ('democratic-republic-of-the-congo', 'belgium'):  'Kinshasa',
    ('turkey', 'belgium'):                            'Ankara',
    ('rwanda', 'belgium'):                            'Kigali',
    ('india', 'belgium'):                             'New Delhi',
    # R23: Italy wave 2
    ('egypt', 'italy'):         'Cairo',
    ('india', 'italy'):         'New Delhi',
    ('pakistan', 'italy'):      'Islamabad',
    ('senegal', 'italy'):       'Dakar',
    ('nigeria', 'italy'):       'Abuja',
    # R23: Spain wave 2
    ('ukraine', 'spain'):             'Kyiv',
    ('nigeria', 'spain'):             'Abuja',
    ('pakistan', 'spain'):            'Islamabad',
    ('peru', 'spain'):                'Lima',
    ('dominican-republic', 'spain'):  'Santo Domingo',
    # R23: Netherlands wave 2
    ('iraq', 'netherlands'):          'Baghdad',
    ('afghanistan', 'netherlands'):   'Kabul',
    ('pakistan', 'netherlands'):      'Islamabad',
    ('ukraine', 'netherlands'):       'Kyiv',
    ('egypt', 'netherlands'):         'Cairo',
    # R23: Belgium wave 2
    ('cameroon', 'belgium'):          'Yaounde',
    ('ethiopia', 'belgium'):          'Addis Ababa',
    ('senegal', 'belgium'):           'Dakar',
    ('nigeria', 'belgium'):           'Abuja',
    ('pakistan', 'belgium'):          'Islamabad',
    # R23: USA wave 3
    ('somalia', 'united-states'):     'Nairobi',
    ('venezuela', 'united-states'):   'Bogota',
    ('afghanistan', 'united-states'): 'Doha',
    ('nepal', 'united-states'):       'Kathmandu',
    ('myanmar', 'united-states'):     'Rangoon',
    # R24: UAE wave 3
    ('malaysia', 'united-arab-emirates'):   'Kuala Lumpur',
    ('senegal', 'united-arab-emirates'):    'Dakar',
    ('cameroon', 'united-arab-emirates'):   'Yaounde',
    ('myanmar', 'united-arab-emirates'):    'Naypyidaw',
    ('tanzania', 'united-arab-emirates'):   'Dar es Salaam',
    # R24: Germany wave 3
    ('greece', 'germany'):    'Athens',
    ('iran', 'germany'):      'Tehran',
    ('egypt', 'germany'):     'Cairo',
    ('hungary', 'germany'):   'Budapest',
    ('bulgaria', 'germany'):  'Sofia',
    # R24: France wave 3
    ('democratic-republic-of-the-congo', 'france'):  'Kinshasa',
    ('rwanda', 'france'):                            'Kigali',
    ('comoros', 'france'):                           'Moroni',
    ('vietnam', 'france'):                           'Hanoi',
    ('china', 'france'):                             'Beijing',
    # R24: Canada wave 3
    ('morocco', 'canada'):          'Rabat',
    ('afghanistan', 'canada'):      'Kabul',
    ('egypt', 'canada'):            'Cairo',
    ('sri-lanka', 'canada'):        'Colombo',
    ('malaysia', 'canada'):         'Kuala Lumpur',
    # R24: Australia wave 3
    ('cambodia', 'australia'):   'Phnom Penh',
    ('laos', 'australia'):       'Vientiane',
    ('thailand', 'australia'):   'Bangkok',
    ('zimbabwe', 'australia'):   'Harare',
    ('nigeria', 'australia'):    'Abuja',
    # R25: India wave 3
    ('myanmar', 'india'):      'Naypyidaw',
    ('afghanistan', 'india'):  'Kabul',
    ('iran', 'india'):         'Tehran',
    ('south-korea', 'india'):  'Seoul',
    ('philippines', 'india'):  'Manila',
    # R25: Singapore wave 2
    ('vietnam', 'singapore'):      'Hanoi',
    ('south-korea', 'singapore'):  'Seoul',
    ('thailand', 'singapore'):     'Bangkok',
    ('pakistan', 'singapore'):     'Islamabad',
    ('sri-lanka', 'singapore'):    'Colombo',
    # R25: Qatar wave 2
    ('turkey', 'qatar'):    'Ankara',
    ('ghana', 'qatar'):     'Accra',
    ('nigeria', 'qatar'):   'Abuja',
    ('jordan', 'qatar'):    'Amman',
    ('malaysia', 'qatar'):  'Kuala Lumpur',
    # R25: Kuwait wave 2
    ('kenya', 'kuwait'):      'Nairobi',
    ('indonesia', 'kuwait'):  'Jakarta',
    ('vietnam', 'kuwait'):    'Hanoi',
    ('ghana', 'kuwait'):      'Accra',
    ('nigeria', 'kuwait'):    'Abuja',
    # R25: South Africa wave 2
    ('senegal', 'south-africa'):      'Dakar',
    ('south-korea', 'south-africa'):  'Seoul',
    ('china', 'south-africa'):        'Beijing',
    ('india', 'south-africa'):        'New Delhi',
    ('pakistan', 'south-africa'):     'Islamabad',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R22: Italy
    ('morocco', 'italy'): (
        "Moroccan nationals are Italy's largest non-EU immigrant community, with over 400,000 "
        "registered residents concentrated in Lombardy, Emilia-Romagna, and Veneto. "
        "This is one of Italy's most established repatriation corridors, with regular "
        "direct air services between Casablanca and Italian cities."
    ),
    ('romania', 'italy'): (
        "Romanian nationals form Italy's largest immigrant community overall, with over one million "
        "residents. Romanian-Italian repatriation is one of the highest-volume corridors in Europe. "
        "EU freedom of movement simplifies document verification; the Romanian civil registry "
        "system is well-mapped for Italian authorities."
    ),
    ('albania', 'italy'): (
        "Albanian nationals form one of Italy's oldest and largest immigrant communities, with over "
        "400,000 residents concentrated in Calabria, Puglia, and Tuscany. The Albania to Italy "
        "corridor is well-established with direct air and ferry connections from Tirana and Durres."
    ),
    ('china', 'italy'): (
        "Chinese nationals form a significant professional and business community in Italy, "
        "concentrated in Prato, Milan, and Rome. Prato hosts one of Europe's largest Chinese "
        "textile industry communities. Documentation from China requires certified Italian translation."
    ),
    ('ukraine', 'italy'): (
        "Ukrainian nationals form one of Italy's larger Eastern European communities, with "
        "significant numbers employed in domestic care and services, particularly in the "
        "Veneto and Lombardy regions. The conflict in Ukraine since 2022 means specialist "
        "coordination is needed for documentation on this corridor."
    ),
    ('philippines', 'italy'): (
        "Filipino nationals work across Italy in domestic care, healthcare, and service roles. "
        "This corridor handles cases where an Italy-based Filipino has a family member die in "
        "the Philippines and needs remains brought to Italy. The Philippine government's OWWA "
        "provides support structures for overseas workers."
    ),
    ('bangladesh', 'italy'): (
        "Bangladeshi nationals form a growing South Asian community in Italy, concentrated in "
        "Rome and Milan. This corridor handles cases where an Italy-based Bangladeshi has a "
        "family member die in Bangladesh and needs remains brought to Italy. "
        "Documentation requires certified Italian translation."
    ),
    # R22: Spain
    ('morocco', 'spain'): (
        "Moroccan nationals are Spain's largest non-EU immigrant community, with over 900,000 "
        "registered residents. This is Spain's highest-volume repatriation corridor from outside "
        "the EU, with regular direct cargo services and well-established documentation procedures "
        "on both sides."
    ),
    ('romania', 'spain'): (
        "Romanian nationals form Spain's largest EU immigrant community, with over 650,000 "
        "residents concentrated in Catalonia, Valencia, and Madrid. EU freedom of movement "
        "and Spain's established procedures make documentation on this corridor relatively "
        "straightforward with a specialist."
    ),
    ('colombia', 'spain'): (
        "Colombian nationals form Spain's largest Latin American community, with over 430,000 "
        "residents. Spain and Colombia share language and many legal traditions; documentation "
        "is in Spanish throughout on both sides, which simplifies some requirements."
    ),
    ('venezuela', 'spain'): (
        "Venezuelan nationals have arrived in Spain in large numbers since 2015, with the "
        "community growing substantially to nearly 400,000. Spain is the primary European "
        "destination for Venezuelan migration. Documentation is in Spanish on both sides."
    ),
    ('ecuador', 'spain'): (
        "Ecuadorian nationals form a well-established Latin American community in Spain, "
        "concentrated in Madrid and Catalonia. Ecuador-Spain repatriation is well-mapped; "
        "documentation is in Spanish throughout and direct air links connect Quito and Guayaquil "
        "to Madrid."
    ),
    ('china', 'spain'): (
        "Chinese nationals form a significant professional and business community in Spain, "
        "particularly in Madrid and Barcelona. Chinese communities in Spain are concentrated "
        "in wholesale trade and food service sectors. Documentation from China requires "
        "certified Spanish translation."
    ),
    ('bolivia', 'spain'): (
        "Bolivian nationals form part of Spain's Latin American diaspora, with a community "
        "concentrated in Madrid and Catalonia. Documentation is in Spanish on both sides. "
        "The Bolivian civil registry (Servicio de Registro Civico) handles official documentation."
    ),
    # R22: Netherlands
    ('turkey', 'netherlands'): (
        "Turkish nationals form one of the Netherlands' two largest non-EU communities, "
        "with over 400,000 residents. Turkey to Netherlands is among the Netherlands' "
        "highest-volume repatriation corridors. Turkish Airlines operates direct cargo "
        "services between Istanbul and Amsterdam Schiphol."
    ),
    ('morocco', 'netherlands'): (
        "Moroccan nationals form the Netherlands' other largest non-EU community, with over "
        "400,000 residents concentrated in Amsterdam, Rotterdam, and The Hague. This is one "
        "of the Netherlands' highest-volume repatriation corridors, with established procedures "
        "on both sides."
    ),
    ('suriname', 'netherlands'): (
        "Surinamese nationals form one of the Netherlands' oldest immigrant communities, "
        "with family and historical ties dating to the colonial era. This corridor handles "
        "cases where a Netherlands-based Surinamese has a family member die in Suriname "
        "and needs remains brought to the Netherlands. Direct flights connect Paramaribo to Amsterdam."
    ),
    ('indonesia', 'netherlands'): (
        "Indonesian nationals and Dutch citizens of Indonesian heritage maintain family "
        "connections between the two countries, reflecting historical ties. This corridor "
        "handles repatriation from Indonesia to the Netherlands for families of Netherlands-based "
        "Indonesian nationals. Documentation from Indonesia requires certified Dutch translation."
    ),
    ('china', 'netherlands'): (
        "Chinese nationals form a professional and business community in the Netherlands, "
        "concentrated in Amsterdam and Rotterdam. This corridor handles cases where a "
        "Netherlands-based Chinese national has a family member die in China and needs "
        "remains brought to the Netherlands. Documentation requires certified translation."
    ),
    ('india', 'netherlands'): (
        "Indian nationals form a growing professional and technology community in the Netherlands, "
        "particularly in Amsterdam and Eindhoven. This corridor handles cases where a Netherlands-based "
        "Indian has a family member die in India and needs remains brought to the Netherlands."
    ),
    # R22: Belgium
    ('morocco', 'belgium'): (
        "Moroccan nationals are Belgium's largest non-EU immigrant community, with over 500,000 "
        "residents concentrated in Brussels, Liege, and Antwerp. This is Belgium's highest-volume "
        "repatriation corridor from outside the EU, with well-established procedures on both sides."
    ),
    ('democratic-republic-of-the-congo', 'belgium'): (
        "Congolese nationals form a significant community in Belgium, reflecting the historical "
        "colonial relationship between the two countries. Belgium has an established Congolese "
        "community of over 200,000, concentrated in Brussels. French documentation from the DRC "
        "simplifies some translation requirements."
    ),
    ('turkey', 'belgium'): (
        "Turkish nationals form one of Belgium's larger non-EU communities, with significant "
        "populations in Brussels, Liege, and Ghent. This corridor handles cases where a "
        "Belgium-based Turkish national has a family member die in Turkey and needs remains "
        "brought to Belgium."
    ),
    ('rwanda', 'belgium'): (
        "Rwandan nationals form a community in Belgium with connections that reflect historical "
        "Belgian colonial ties. Brussels has a Rwandan community in professional and academic "
        "roles. Documentation from Rwanda requires certified French or Dutch translation for "
        "Belgian authorities."
    ),
    ('india', 'belgium'): (
        "Indian nationals form a growing professional community in Belgium, particularly in "
        "Brussels and Antwerp. Technology, diamond trade, and EU institution workers account "
        "for much of this community. Documentation from India requires certified French or "
        "Dutch translation."
    ),
    # R23: Italy wave 2
    ('egypt', 'italy'): (
        "Egyptian nationals form a significant Middle Eastern community in Italy, concentrated "
        "in Milan, Rome, and Florence. This corridor handles cases where an Italy-based Egyptian "
        "has a family member die in Egypt and needs remains brought to Italy. Arabic "
        "documentation requires certified Italian translation."
    ),
    ('india', 'italy'): (
        "Indian nationals form a growing professional and academic community in Italy, "
        "with significant numbers in Milan, Rome, and Turin. This corridor handles cases where "
        "an Italy-based Indian has a family member die in India and needs remains brought to "
        "Italy. Documentation requires certified Italian translation."
    ),
    ('pakistan', 'italy'): (
        "Pakistani nationals form part of Italy's South Asian diaspora community. This corridor "
        "handles cases where an Italy-based Pakistani has a family member die in Pakistan and "
        "needs remains brought to Italy. Documentation requires certified Italian translation."
    ),
    ('senegal', 'italy'): (
        "Senegalese nationals form a significant West African community in Italy, one of the "
        "largest in Europe, with communities in Milan, Venice, and other northern Italian cities. "
        "This corridor handles cases where an Italy-based Senegalese national has a family "
        "member die in Senegal and needs remains brought to Italy."
    ),
    ('nigeria', 'italy'): (
        "Nigerian nationals form a growing community in Italy, concentrated in major urban "
        "areas. This corridor handles cases where an Italy-based Nigerian has a family member "
        "die in Nigeria and needs remains brought to Italy. Documentation from Nigeria requires "
        "certified Italian translation."
    ),
    # R23: Spain wave 2
    ('ukraine', 'spain'): (
        "Ukrainian nationals have arrived in Spain in significant numbers, with a community "
        "growing substantially since 2022. This corridor handles cases where a Spain-based "
        "Ukrainian has a family member die in Ukraine and needs remains brought to Spain. "
        "The ongoing conflict means specialist coordination is essential."
    ),
    ('nigeria', 'spain'): (
        "Nigerian nationals form a growing community in Spain, concentrated in Madrid, Barcelona, "
        "and Valencia. This corridor handles cases where a Spain-based Nigerian has a family "
        "member die in Nigeria and needs remains brought to Spain. Documentation requires "
        "certified Spanish translation."
    ),
    ('pakistan', 'spain'): (
        "Pakistani nationals form part of Spain's South Asian diaspora, concentrated in "
        "Barcelona and Madrid. This corridor handles cases where a Spain-based Pakistani has "
        "a family member die in Pakistan and needs remains brought to Spain."
    ),
    ('peru', 'spain'): (
        "Peruvian nationals form part of Spain's Latin American community. This corridor "
        "handles cases where a Spain-based Peruvian has a family member die in Peru and "
        "needs remains brought to Spain. Documentation is in Spanish on both sides."
    ),
    ('dominican-republic', 'spain'): (
        "Dominican nationals form a significant Latin American community in Spain, concentrated "
        "in Madrid and Barcelona. This corridor handles cases where a Spain-based Dominican "
        "has a family member die in the Dominican Republic and needs remains brought to Spain. "
        "Documentation is in Spanish on both sides."
    ),
    # R23: Netherlands wave 2
    ('iraq', 'netherlands'): (
        "Iraqi nationals form part of the Netherlands' Middle Eastern diaspora community. "
        "This corridor handles cases where a Netherlands-based Iraqi has a family member die "
        "in Iraq and needs remains brought to the Netherlands. Arabic documentation requires "
        "certified Dutch or English translation."
    ),
    ('afghanistan', 'netherlands'): (
        "Afghan nationals form a community in the Netherlands, with significant numbers who "
        "arrived in waves following periods of conflict. This corridor handles cases where a "
        "Netherlands-based Afghan has a family member die in Afghanistan and needs remains "
        "brought to the Netherlands. Specialist coordination is essential given the situation "
        "in Afghanistan since 2021."
    ),
    ('pakistan', 'netherlands'): (
        "Pakistani nationals form part of the Netherlands' South Asian diaspora. This corridor "
        "handles cases where a Netherlands-based Pakistani has a family member die in Pakistan "
        "and needs remains brought to the Netherlands. Documentation requires certified Dutch "
        "or English translation."
    ),
    ('ukraine', 'netherlands'): (
        "Ukrainian nationals have arrived in the Netherlands in significant numbers since 2022. "
        "This corridor handles cases where a Netherlands-based Ukrainian has a family member "
        "die in Ukraine and needs remains brought to the Netherlands. The ongoing conflict "
        "means specialist coordination is essential on this corridor."
    ),
    ('egypt', 'netherlands'): (
        "Egyptian nationals form part of the Netherlands' Middle Eastern community. This "
        "corridor handles cases where a Netherlands-based Egyptian has a family member die "
        "in Egypt and needs remains brought to the Netherlands. Arabic documentation requires "
        "certified Dutch or English translation."
    ),
    # R23: Belgium wave 2
    ('cameroon', 'belgium'): (
        "Cameroonian nationals form part of Belgium's Central African diaspora community. "
        "Cameroon is bilingual in French and English, which simplifies documentation requirements "
        "for Belgian authorities. This corridor handles cases where a Belgium-based Cameroonian "
        "has a family member die in Cameroon and needs remains brought to Belgium."
    ),
    ('ethiopia', 'belgium'): (
        "Ethiopian nationals form a growing community in Belgium, concentrated in Brussels. "
        "This corridor handles cases where a Belgium-based Ethiopian has a family member die "
        "in Ethiopia and needs remains brought to Belgium. Amharic documentation requires "
        "certified French or Dutch translation."
    ),
    ('senegal', 'belgium'): (
        "Senegalese nationals form part of Belgium's West African diaspora. Senegal uses French "
        "as its official language, which simplifies translation requirements for French-speaking "
        "Belgian authorities. This corridor handles cases where a Belgium-based Senegalese has "
        "a family member die in Senegal."
    ),
    ('nigeria', 'belgium'): (
        "Nigerian nationals form a growing community in Belgium, concentrated in Brussels. "
        "This corridor handles cases where a Belgium-based Nigerian has a family member die "
        "in Nigeria and needs remains brought to Belgium. Documentation requires certified "
        "French or Dutch translation."
    ),
    ('pakistan', 'belgium'): (
        "Pakistani nationals form part of Belgium's South Asian diaspora community. This "
        "corridor handles cases where a Belgium-based Pakistani has a family member die in "
        "Pakistan and needs remains brought to Belgium. Documentation requires certified "
        "French or Dutch translation."
    ),
    # R23: USA wave 3
    ('somalia', 'united-states'): (
        "Somali-Americans form significant communities in Minneapolis-Saint Paul, Columbus Ohio, "
        "and Seattle, one of the largest Somali diaspora concentrations in the world. "
        "Somalia's fragile state infrastructure means specialist coordination is essential. "
        "The US Embassy does not operate in Mogadishu; consular services for Somalia are "
        "handled from the US Embassy in Nairobi. (US State Department, 2025.)"
    ),
    ('venezuela', 'united-states'): (
        "Venezuelan-Americans form a growing community across Florida, New York, and Texas, "
        "with arrivals accelerating significantly since 2016. The United States suspended "
        "normal diplomatic relations with Venezuela in 2019; US consular services in "
        "Venezuela are handled through the US Embassy in Bogota, Colombia. "
        "Specialist coordination is essential on this corridor. (US State Department, 2025.)"
    ),
    ('afghanistan', 'united-states'): (
        "Afghan-Americans form communities across Virginia, California, and New York, with "
        "the community growing substantially following evacuations in 2021. US Embassy "
        "operations in Kabul were suspended in 2021; consular services for Afghanistan are "
        "handled from the US Embassy in Doha, Qatar. Specialist coordination is essential "
        "on this corridor. (US State Department, 2025.)"
    ),
    ('nepal', 'united-states'): (
        "Nepali-Americans form growing communities in New York, Texas, and New England, "
        "with the diaspora expanding substantially in recent years. Nepal's documentation "
        "process runs through the civil registry and requires certified English translation. "
        "The US Embassy in Kathmandu handles consular matters for Nepal-based Americans."
    ),
    ('myanmar', 'united-states'): (
        "Myanmar-Americans form communities in California, Indiana, and New York. "
        "The situation in Myanmar since the 2021 military takeover means specialist "
        "coordination is essential on this corridor. Documentation requires certified "
        "English translation. The US Embassy in Rangoon handles consular matters. "
        "(US State Department, 2025.)"
    ),
    # R24: UAE wave 3
    ('malaysia', 'united-arab-emirates'): (
        "Malaysian nationals work in the UAE in professional, engineering, and service roles. "
        "This corridor handles cases where a UAE-based Malaysian has a family member die in "
        "Malaysia and needs remains brought to the UAE. The UAE Embassy in Kuala Lumpur "
        "handles document attestation."
    ),
    ('senegal', 'united-arab-emirates'): (
        "Senegalese nationals work in the UAE in service and professional roles. This corridor "
        "handles cases where a UAE-based Senegalese has a family member die in Senegal and "
        "needs remains brought to the UAE. French documentation from Senegal requires "
        "certified translation for UAE attestation."
    ),
    ('cameroon', 'united-arab-emirates'): (
        "Cameroonian nationals work in the UAE in various professional roles. This corridor "
        "handles cases where a UAE-based Cameroonian has a family member die in Cameroon "
        "and needs remains brought to the UAE. Cameroon's bilingual documentation "
        "simplifies some translation requirements."
    ),
    ('myanmar', 'united-arab-emirates'): (
        "Myanmar nationals work in the UAE in domestic and service sectors. This corridor "
        "handles cases where a UAE-based Myanmar national has a family member die in Myanmar "
        "and needs remains brought to the UAE. The situation in Myanmar since 2021 may "
        "affect documentation procedures on this corridor."
    ),
    ('tanzania', 'united-arab-emirates'): (
        "Tanzanian nationals work in the UAE in various professional and service roles. "
        "This corridor handles cases where a UAE-based Tanzanian has a family member die "
        "in Tanzania and needs remains brought to the UAE. Documentation requires "
        "certified translation for UAE attestation."
    ),
    # R24: Germany wave 3
    ('greece', 'germany'): (
        "Greek nationals form one of Germany's older EU immigrant communities, with ties "
        "going back to guest worker programmes in the 1960s and deepened by economic "
        "migration since 2010. EU freedom of movement and the apostille framework simplify "
        "document authentication. Germany has Greece's largest diaspora community."
    ),
    ('iran', 'germany'): (
        "Iranian nationals form a significant professional and academic community in Germany, "
        "with one of the world's largest Iranian diaspora populations. This corridor handles "
        "cases where a Germany-based Iranian has a family member die in Iran and needs remains "
        "brought to Germany. Farsi documentation requires certified German translation."
    ),
    ('egypt', 'germany'): (
        "Egyptian nationals form part of Germany's Middle Eastern and North African diaspora "
        "community. This corridor handles cases where a Germany-based Egyptian has a family "
        "member die in Egypt and needs remains brought to Germany. Arabic documentation "
        "requires certified German translation."
    ),
    ('hungary', 'germany'): (
        "Hungarian nationals form part of Germany's Central European EU community, with "
        "significant numbers in Bavaria and Baden-Wurttemberg. EU freedom of movement "
        "and the apostille framework simplify documentation. This corridor sees consistent "
        "repatriation demand within the EU."
    ),
    ('bulgaria', 'germany'): (
        "Bulgarian nationals work in Germany in various sectors, part of EU freedom of "
        "movement migration. This corridor handles cases where a Germany-based Bulgarian has "
        "a family member die in Bulgaria and needs remains brought to Germany. "
        "The EU apostille framework simplifies document authentication."
    ),
    # R24: France wave 3
    ('democratic-republic-of-the-congo', 'france'): (
        "Congolese nationals from the DRC form a significant community in France, "
        "reflecting the French language connection between the two countries. This corridor "
        "handles cases where a France-based Congolese national has a family member die in "
        "the DRC and needs remains brought to France. Documentation is in French on both sides."
    ),
    ('rwanda', 'france'): (
        "Rwandan nationals form part of France's Central African diaspora community. "
        "Rwanda uses French as a former official language alongside Kinyarwanda and English. "
        "This corridor handles cases where a France-based Rwandan has a family member die "
        "in Rwanda and needs remains brought to France."
    ),
    ('comoros', 'france'): (
        "Comorian nationals form part of France's Indian Ocean diaspora, with a large "
        "community concentrated in Marseille. France and the Comoros share language ties; "
        "French is one of the official languages of the Comoros. This is a well-established "
        "corridor with direct air connections."
    ),
    ('vietnam', 'france'): (
        "Vietnamese nationals form one of France's largest Asian diaspora communities, "
        "reflecting historical colonial connections. The community is concentrated in Paris, "
        "particularly in the 13th arrondissement. Vietnamese documentation requires certified "
        "French translation."
    ),
    ('china', 'france'): (
        "Chinese nationals form a significant professional and business community in France, "
        "with communities in Paris and Lyon. The Wenzhou community in Paris is among the "
        "largest in Europe. Documentation from China requires certified French translation."
    ),
    # R24: Canada wave 3
    ('morocco', 'canada'): (
        "Moroccan-Canadians form a growing community in Quebec and Ontario, particularly "
        "in Montreal where French-language ties support settlement. This corridor handles "
        "cases where a Canada-based Moroccan has a family member die in Morocco and needs "
        "remains brought to Canada. French documentation from Morocco simplifies Quebec requirements."
    ),
    ('afghanistan', 'canada'): (
        "Afghan-Canadians form a community in Toronto, Ottawa, and Vancouver, with "
        "the community growing following arrivals in 2021. This corridor handles cases where "
        "a Canada-based Afghan has a family member die in Afghanistan and needs remains "
        "brought to Canada. Specialist coordination is essential given Afghanistan's current situation."
    ),
    ('egypt', 'canada'): (
        "Egyptian-Canadians form part of Canada's Middle Eastern diaspora, concentrated in "
        "Toronto, Ottawa, and Montreal. This corridor handles cases where a Canada-based "
        "Egyptian has a family member die in Egypt and needs remains brought to Canada. "
        "Arabic documentation requires certified English or French translation."
    ),
    ('sri-lanka', 'canada'): (
        "Sri Lankan-Canadians form a significant community in Toronto, particularly in the "
        "Scarborough area, one of the largest Sri Lankan diaspora concentrations outside Asia. "
        "This corridor handles cases where a Canada-based Sri Lankan has a family member die "
        "in Sri Lanka and needs remains brought to Canada."
    ),
    ('malaysia', 'canada'): (
        "Malaysian-Canadians form a growing community in Toronto, Vancouver, and Calgary. "
        "This corridor handles cases where a Canada-based Malaysian has a family member die "
        "in Malaysia and needs remains brought to Canada. English documentation from Malaysia "
        "simplifies some requirements."
    ),
    # R24: Australia wave 3
    ('cambodia', 'australia'): (
        "Cambodian-Australians form a community in Sydney and Melbourne, one of the larger "
        "South-East Asian diaspora groups in Australia. This corridor handles cases where an "
        "Australia-based Cambodian has a family member die in Cambodia and needs remains "
        "brought to Australia. Khmer documentation requires certified English translation."
    ),
    ('laos', 'australia'): (
        "Laotian-Australians form a small but established community in Melbourne and Sydney. "
        "This corridor handles cases where an Australia-based Laotian has a family member "
        "die in Laos and needs remains brought to Australia. Lao documentation requires "
        "certified English translation."
    ),
    ('thailand', 'australia'): (
        "Thai nationals and Thai-Australians form a significant community across Australian "
        "cities, with Thai restaurants and businesses a visible presence. This corridor "
        "handles cases where an Australia-based Thai has a family member die in Thailand "
        "and needs remains brought to Australia. Thai documentation requires certified English translation."
    ),
    ('zimbabwe', 'australia'): (
        "Zimbabwean-Australians form a community particularly in Melbourne and Sydney. "
        "This corridor handles cases where an Australia-based Zimbabwean has a family member "
        "die in Zimbabwe and needs remains brought to Australia. English documentation from "
        "Zimbabwe simplifies translation requirements."
    ),
    ('nigeria', 'australia'): (
        "Nigerian-Australians form a growing community in Sydney and Melbourne. This corridor "
        "handles cases where an Australia-based Nigerian has a family member die in Nigeria "
        "and needs remains brought to Australia. English documentation from Nigeria simplifies "
        "translation requirements."
    ),
    # R25: India wave 3
    ('myanmar', 'india'): (
        "Myanmar and India share a long land border and historical connections. "
        "This corridor handles cases where an India-based person has a family member die "
        "in Myanmar and needs remains brought to India. Direct road and air links connect "
        "Myanmar to northeast India. Documentation requires certified translation."
    ),
    ('afghanistan', 'india'): (
        "Afghan nationals and Afghan-origin communities in India have long-established ties. "
        "This corridor handles cases where an India-based person has a family member die in "
        "Afghanistan and needs remains brought to India. The situation in Afghanistan since "
        "2021 means specialist coordination is essential on this corridor."
    ),
    ('iran', 'india'): (
        "Iranian nationals visit and work in India in professional and business capacities, "
        "and there are historic cultural connections between the two countries. "
        "This corridor handles cases where an India-based person has a family member die "
        "in Iran and needs remains brought to India. Documentation requires certified translation."
    ),
    ('south-korea', 'india'): (
        "South Korean nationals work in India in business, manufacturing, and technology "
        "sectors, with Korean companies operating significant facilities in Chennai and "
        "other cities. This corridor handles cases where an India-based person has a family "
        "member die in South Korea and needs remains brought to India."
    ),
    ('philippines', 'india'): (
        "Filipino nationals work in India in professional and service roles. This corridor "
        "handles cases where an India-based person has a family member die in the Philippines "
        "and needs remains brought to India. Direct air links connect Manila to Indian cities."
    ),
    # R25: Singapore wave 2
    ('vietnam', 'singapore'): (
        "Vietnamese nationals work in Singapore in various professional and service sectors. "
        "This corridor handles cases where a Singapore-based Vietnamese has a family member "
        "die in Vietnam and needs remains brought to Singapore. Vietnamese documentation "
        "requires certified English translation."
    ),
    ('south-korea', 'singapore'): (
        "South Korean nationals work in Singapore in business, finance, and technology. "
        "Singapore is a major hub for Korean corporate operations in South-East Asia. "
        "This corridor handles cases where a Singapore-based Korean has a family member "
        "die in South Korea and needs remains brought to Singapore."
    ),
    ('thailand', 'singapore'): (
        "Thai nationals work in Singapore in domestic, hospitality, and professional roles. "
        "Singapore and Thailand have close bilateral ties and regular direct flights. "
        "This corridor handles cases where a Singapore-based Thai has a family member "
        "die in Thailand and needs remains brought to Singapore."
    ),
    ('pakistan', 'singapore'): (
        "Pakistani nationals work in Singapore in professional and service roles. This "
        "corridor handles cases where a Singapore-based Pakistani has a family member die "
        "in Pakistan and needs remains brought to Singapore. All documents must be authenticated "
        "by the Singapore High Commission in Islamabad."
    ),
    ('sri-lanka', 'singapore'): (
        "Sri Lankan nationals work in Singapore in domestic, professional, and service roles, "
        "and the two countries share Commonwealth administrative ties. This corridor handles "
        "cases where a Singapore-based Sri Lankan has a family member die in Sri Lanka and "
        "needs remains brought to Singapore."
    ),
    # R25: Qatar wave 2
    ('turkey', 'qatar'): (
        "Turkish nationals work in Qatar in construction, engineering, and business roles. "
        "This corridor handles cases where a Qatar-based Turkish national has a family member "
        "die in Turkey and needs remains brought to Qatar. Documentation is attested through "
        "the Qatar Embassy in Ankara."
    ),
    ('ghana', 'qatar'): (
        "Ghanaian nationals work in Qatar in professional and service roles. This corridor "
        "handles cases where a Qatar-based Ghanaian has a family member die in Ghana and "
        "needs remains brought to Qatar. Documentation is attested through the Qatar "
        "Embassy in Accra."
    ),
    ('nigeria', 'qatar'): (
        "Nigerian nationals work in Qatar in professional roles. This corridor handles cases "
        "where a Qatar-based Nigerian has a family member die in Nigeria and needs remains "
        "brought to Qatar. Documentation is attested through the Qatar Embassy in Abuja."
    ),
    ('jordan', 'qatar'): (
        "Jordanian nationals form part of Qatar's Arab professional community, working "
        "in business, education, and public service roles. This corridor handles cases where "
        "a Qatar-based Jordanian has a family member die in Jordan and needs remains brought "
        "to Qatar. Documentation is attested through the Qatar Embassy in Amman."
    ),
    ('malaysia', 'qatar'): (
        "Malaysian nationals work in Qatar in engineering, professional, and service roles. "
        "This corridor handles cases where a Qatar-based Malaysian has a family member die "
        "in Malaysia and needs remains brought to Qatar. Documentation is attested through "
        "the Qatar Embassy in Kuala Lumpur."
    ),
    # R25: Kuwait wave 2
    ('kenya', 'kuwait'): (
        "Kenyan nationals work in Kuwait in professional and domestic service roles. "
        "This corridor handles cases where a Kuwait-based Kenyan has a family member die "
        "in Kenya and needs remains brought to Kuwait. Documentation is attested through "
        "the Kuwait Embassy in Nairobi."
    ),
    ('indonesia', 'kuwait'): (
        "Indonesian nationals work in Kuwait in domestic and professional roles. This "
        "corridor handles cases where a Kuwait-based Indonesian has a family member die "
        "in Indonesia and needs remains brought to Kuwait. Documentation is attested through "
        "the Kuwait Embassy in Jakarta."
    ),
    ('vietnam', 'kuwait'): (
        "Vietnamese nationals work in Kuwait in professional and service roles. This "
        "corridor handles cases where a Kuwait-based Vietnamese has a family member die "
        "in Vietnam and needs remains brought to Kuwait. Vietnamese documentation requires "
        "certified translation for Kuwaiti attestation."
    ),
    ('ghana', 'kuwait'): (
        "Ghanaian nationals work in Kuwait in professional and service roles. This corridor "
        "handles cases where a Kuwait-based Ghanaian has a family member die in Ghana and "
        "needs remains brought to Kuwait. Documentation is attested through the Kuwait "
        "Embassy in Accra."
    ),
    ('nigeria', 'kuwait'): (
        "Nigerian nationals work in Kuwait in professional roles. This corridor handles "
        "cases where a Kuwait-based Nigerian has a family member die in Nigeria and needs "
        "remains brought to Kuwait. Documentation is attested through the Kuwait Embassy in Abuja."
    ),
    # R25: South Africa wave 2
    ('senegal', 'south-africa'): (
        "Senegalese nationals work in South Africa in trade and professional roles. This "
        "corridor handles cases where a South Africa-based Senegalese has a family member "
        "die in Senegal and needs remains brought to South Africa. French documentation "
        "from Senegal requires certified translation for South African authorities."
    ),
    ('south-korea', 'south-africa'): (
        "South Korean nationals work in South Africa in business and manufacturing, with "
        "Korean corporate investment significant in several sectors. This corridor handles "
        "cases where a South Africa-based Korean has a family member die in South Korea "
        "and needs remains brought to South Africa."
    ),
    ('china', 'south-africa'): (
        "Chinese nationals form a growing business and professional community in South Africa, "
        "with significant Chinese investment in mining, construction, and trade. This corridor "
        "handles cases where a South Africa-based Chinese national has a family member die "
        "in China and needs remains brought to South Africa."
    ),
    ('india', 'south-africa'): (
        "Indian-South Africans form one of South Africa's oldest and most established "
        "diaspora communities, with roots going back to indentured labour in the 19th century. "
        "This corridor handles cases where a South Africa-based person of Indian heritage "
        "has a family member die in India and needs remains brought to South Africa."
    ),
    ('pakistan', 'south-africa'): (
        "Pakistani nationals work in South Africa in trade and professional roles. This "
        "corridor handles cases where a South Africa-based Pakistani has a family member "
        "die in Pakistan and needs remains brought to South Africa. Documentation requires "
        "certified translation."
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
# Route list: 4 blocks of 25 = 100 routes (R22-R25)
# Template rotation starts at D (index 3) -- R21 ended on C.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # Block R22: Italy x7 + Spain x7 + Netherlands x6 + Belgium x5 = 25
    ('morocco', 'italy'),
    ('romania', 'italy'),
    ('albania', 'italy'),
    ('china', 'italy'),
    ('ukraine', 'italy'),
    ('philippines', 'italy'),
    ('bangladesh', 'italy'),
    ('morocco', 'spain'),
    ('romania', 'spain'),
    ('colombia', 'spain'),
    ('venezuela', 'spain'),
    ('ecuador', 'spain'),
    ('china', 'spain'),
    ('bolivia', 'spain'),
    ('turkey', 'netherlands'),
    ('morocco', 'netherlands'),
    ('suriname', 'netherlands'),
    ('indonesia', 'netherlands'),
    ('china', 'netherlands'),
    ('india', 'netherlands'),
    ('morocco', 'belgium'),
    ('democratic-republic-of-the-congo', 'belgium'),
    ('turkey', 'belgium'),
    ('rwanda', 'belgium'),
    ('india', 'belgium'),
    # Block R23: Italy wave 2 x5 + Spain wave 2 x5 + NL wave 2 x5 + BE wave 2 x5 + USA wave 3 x5 = 25
    ('egypt', 'italy'),
    ('india', 'italy'),
    ('pakistan', 'italy'),
    ('senegal', 'italy'),
    ('nigeria', 'italy'),
    ('ukraine', 'spain'),
    ('nigeria', 'spain'),
    ('pakistan', 'spain'),
    ('peru', 'spain'),
    ('dominican-republic', 'spain'),
    ('iraq', 'netherlands'),
    ('afghanistan', 'netherlands'),
    ('pakistan', 'netherlands'),
    ('ukraine', 'netherlands'),
    ('egypt', 'netherlands'),
    ('cameroon', 'belgium'),
    ('ethiopia', 'belgium'),
    ('senegal', 'belgium'),
    ('nigeria', 'belgium'),
    ('pakistan', 'belgium'),
    ('somalia', 'united-states'),
    ('venezuela', 'united-states'),
    ('afghanistan', 'united-states'),
    ('nepal', 'united-states'),
    ('myanmar', 'united-states'),
    # Block R24: UAE wave 3 x5 + Germany wave 3 x5 + France wave 3 x5 + Canada wave 3 x5 + Australia wave 3 x5 = 25
    ('malaysia', 'united-arab-emirates'),
    ('senegal', 'united-arab-emirates'),
    ('cameroon', 'united-arab-emirates'),
    ('myanmar', 'united-arab-emirates'),
    ('tanzania', 'united-arab-emirates'),
    ('greece', 'germany'),
    ('iran', 'germany'),
    ('egypt', 'germany'),
    ('hungary', 'germany'),
    ('bulgaria', 'germany'),
    ('democratic-republic-of-the-congo', 'france'),
    ('rwanda', 'france'),
    ('comoros', 'france'),
    ('vietnam', 'france'),
    ('china', 'france'),
    ('morocco', 'canada'),
    ('afghanistan', 'canada'),
    ('egypt', 'canada'),
    ('sri-lanka', 'canada'),
    ('malaysia', 'canada'),
    ('cambodia', 'australia'),
    ('laos', 'australia'),
    ('thailand', 'australia'),
    ('zimbabwe', 'australia'),
    ('nigeria', 'australia'),
    # Block R25: India wave 3 x5 + Singapore wave 2 x5 + Qatar wave 2 x5 + Kuwait wave 2 x5 + SA wave 2 x5 = 25
    ('myanmar', 'india'),
    ('afghanistan', 'india'),
    ('iran', 'india'),
    ('south-korea', 'india'),
    ('philippines', 'india'),
    ('vietnam', 'singapore'),
    ('south-korea', 'singapore'),
    ('thailand', 'singapore'),
    ('pakistan', 'singapore'),
    ('sri-lanka', 'singapore'),
    ('turkey', 'qatar'),
    ('ghana', 'qatar'),
    ('nigeria', 'qatar'),
    ('jordan', 'qatar'),
    ('malaysia', 'qatar'),
    ('kenya', 'kuwait'),
    ('indonesia', 'kuwait'),
    ('vietnam', 'kuwait'),
    ('ghana', 'kuwait'),
    ('nigeria', 'kuwait'),
    ('senegal', 'south-africa'),
    ('south-korea', 'south-africa'),
    ('china', 'south-africa'),
    ('india', 'south-africa'),
    ('pakistan', 'south-africa'),
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
    'R22 (Italy/Spain/Netherlands/Belgium)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['italy', 'spain', 'netherlands', 'belgium']
    )],
    'R23 (Italy+Spain+NL+BE wave2 / USA wave3)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['italy', 'spain', 'netherlands', 'belgium', 'united-states']
    )],
    'R24 (UAE/Germany/France/Canada/Australia wave3)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['united-arab-emirates', 'germany', 'france', 'canada', 'australia']
    )],
    'R25 (India/Singapore/Qatar/Kuwait/SA wave2-3)': [(o, d) for o, d in generated if any(
        d.endswith(x) for x in ['india', 'singapore', 'qatar', 'kuwait', 'south-africa']
    )],
}
for block, routes in blocks.items():
    if routes:
        print(f"  {block}: {len(routes)} routes, variants {','.join(sorted(set(v for _, v in routes)))}")
