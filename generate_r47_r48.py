#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R47-R48.

   R47: USA wave 7 x5 + Germany wave 8 x5 + France wave 7 x5 +
        UAE wave 7 x5 + Saudi Arabia wave 7 x5 = 25

   R48: Australia wave 6 x5 + Canada wave 6 x5 + India wave 6 (Gulf) x5 +
        Qatar wave 5 x5 + Kuwait wave 6 x5 = 25

   Template rotation: R46 ended on C (index 2). R47 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
   R48 also starts at D (R47 ended C).
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R46 ended C (index 2); R47 starts D (index 3)

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
    'united-arab-emirates': {
        'name': 'United Arab Emirates',
        'slug': 'united-arab-emirates',
        'key': 'ae',
        'reception': (
            "The UAE funeral home or government mortuary takes custody at Dubai "
            "International (DXB) or Abu Dhabi International (AUH) cargo terminal. "
            "UAE Ministry of Health clearance is required before burial or cremation. "
            "All foreign documentation must be attested by the UAE Embassy in the "
            "country of origin and authenticated by UAE authorities. "
            "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
        ),
        'consular_template': (
            "UAE Embassy in {city} handles attestation of repatriation documents. "
            "Contact the UAE Embassy for document authentication requirements. "
            "UAE Ministry of Foreign Affairs and International Cooperation (MOFAIC) "
            "can be reached via the UAE Embassy during business hours."
        ),
        'arrival_faq': (
            "The UAE funeral home takes custody at Dubai (DXB) or Abu Dhabi (AUH) "
            "cargo terminal. UAE Ministry of Health clearance is required. All documents "
            "must be attested by the UAE Embassy in the origin country. Islamic remains "
            "require certification for Islamic burial; non-Islamic remains follow "
            "separate procedures."
        ),
        'emergency_line': 'contact UAE Embassy in origin country',
        'hub_url': 'repatriation-from-united-arab-emirates',
    },
    'saudi-arabia': {
        'name': 'Saudi Arabia',
        'slug': 'saudi-arabia',
        'key': 'sa',
        'reception': (
            "The Saudi government mortuary or funeral home takes custody at King Khalid "
            "International (RUH, Riyadh), King Abdulaziz International (JED, Jeddah), "
            "or King Fahd International (DMM, Dammam) cargo terminal. Saudi Ministry "
            "of Health approval is required before the remains can be received. All "
            "documents must be authenticated by the Saudi Embassy in the country of "
            "origin. Non-Muslim remains require specific certification and procedures. "
            "(Saudi Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Saudi Embassy in {city} handles authentication of repatriation documents. "
            "Contact the Saudi Embassy for document legalisation requirements. "
            "Saudi Ministry of Foreign Affairs coordinates with the receiving authorities "
            "in Saudi Arabia."
        ),
        'arrival_faq': (
            "The Saudi government mortuary takes custody at the cargo terminal. "
            "Saudi Ministry of Health approval is required in advance. All documents "
            "must be authenticated by the Saudi Embassy in the origin country. "
            "Non-Muslim remains require specific certification. The family or sponsor "
            "arranges the receiving funeral home."
        ),
        'emergency_line': 'contact Saudi Embassy in origin country',
        'hub_url': 'repatriation-from-saudi-arabia',
    },
    'australia': {
        'name': 'Australia',
        'slug': 'australia',
        'key': 'au',
        'reception': (
            "The Australian funeral director takes custody at the cargo terminal. "
            "Australian Border Force clearance is required. The Australian Department "
            "of Health and Aged Care regulations apply. State or territory funeral "
            "regulations govern burial or cremation: requirements differ between New "
            "South Wales, Victoria, Queensland, Western Australia, South Australia, "
            "and the Northern Territory. All documentation must be authenticated. "
            "(Australian Government, Department of Foreign Affairs and Trade, DFAT, 2025.)"
        ),
        'consular_template': (
            "Australian Embassy or High Commission in {city} can assist Australian "
            "citizens and their families with consular registration of the death and "
            "provide a list of local funeral directors. They cannot pay for or arrange "
            "repatriation. Australian Government Consular Emergency Centre: "
            "+61 2 6261 3305 (24 hours)."
        ),
        'arrival_faq': (
            "The Australian funeral director takes custody at the cargo terminal. "
            "Australian Border Force clearance requires the foreign death certificate, "
            "transit permit, and embalming certificate. State or territory regulations "
            "govern burial or cremation. The receiving funeral director coordinates "
            "with the relevant state authority."
        ),
        'emergency_line': '+61 2 6261 3305',
        'hub_url': 'repatriation-from-australia',
    },
    'canada': {
        'name': 'Canada',
        'slug': 'canada',
        'key': 'ca',
        'reception': (
            "The Canadian funeral director takes custody at the cargo terminal. "
            "Canadian Border Services Agency (CBSA) clearance is required. "
            "The required documents are: the foreign death certificate, transit or "
            "burial permit, and embalming certificate. Provincial or territorial "
            "regulations apply and vary between Ontario, British Columbia, Quebec, "
            "Alberta, and other provinces. "
            "(Global Affairs Canada, 2025.)"
        ),
        'consular_template': (
            "Canadian Embassy or High Commission in {city} can assist Canadian "
            "citizens and their families with consular registration of the death and "
            "provide a list of local funeral directors. They cannot pay for or arrange "
            "repatriation. Global Affairs Canada emergency line: "
            "+1 (613) 996-8885 (24 hours, collect calls accepted)."
        ),
        'arrival_faq': (
            "The Canadian funeral director takes custody at the cargo terminal. "
            "CBSA clearance requires the foreign death certificate, transit or burial "
            "permit, and embalming certificate. Provincial regulations govern burial or "
            "cremation. The receiving funeral director notifies the appropriate "
            "provincial authority."
        ),
        'emergency_line': '+1 (613) 996-8885',
        'hub_url': 'repatriation-from-canada',
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
    'qatar': {
        'name': 'Qatar',
        'slug': 'qatar',
        'key': 'qa',
        'reception': (
            "The Qatari funeral home or government mortuary takes custody at Hamad "
            "International Airport (DOH) cargo terminal. Qatar Ministry of Public "
            "Health approval is required before the remains can be received. All "
            "documents must be attested by the Qatari Embassy in the country of origin. "
            "(Qatar Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Qatar Embassy in {city} handles attestation of repatriation documents. "
            "Contact the Qatar Embassy for document authentication requirements. "
            "Qatar Ministry of Foreign Affairs can be reached via the Qatar Embassy."
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
}

# ---------------------------------------------------------------------------
# Embassy cities: destination country embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R47: USA wave 7
    ('malaysia',        'united-states'): 'Kuala Lumpur',
    ('thailand',        'united-states'): 'Bangkok',
    ('sri-lanka',       'united-states'): 'Colombo',
    ('hong-kong',       'united-states'): 'Hong Kong',
    ('panama',          'united-states'): 'Panama City',
    # R47: Germany wave 8
    ('rwanda',          'germany'): 'Kigali',
    ('tanzania',        'germany'): 'Dar es Salaam',
    ('mozambique',      'germany'): 'Maputo',
    ('angola',          'germany'): 'Luanda',
    ('laos',            'germany'): 'Vientiane',
    # R47: France wave 7
    ('iran',            'france'): 'Tehran',
    ('afghanistan',     'france'): 'Paris',
    ('poland',          'france'): 'Warsaw',
    ('romania',         'france'): 'Bucharest',
    ('ukraine',         'france'): 'Kyiv',
    # R47: UAE wave 7
    ('guinea',          'united-arab-emirates'): 'Conakry',
    ('ivory-coast',     'united-arab-emirates'): 'Abidjan',
    ('burkina-faso',    'united-arab-emirates'): 'Abidjan',
    ('laos',            'united-arab-emirates'): 'Bangkok',
    ('cambodia',        'united-arab-emirates'): 'Phnom Penh',
    # R47: Saudi Arabia wave 7
    ('russia',          'saudi-arabia'): 'Moscow',
    ('uzbekistan',      'saudi-arabia'): 'Tashkent',
    ('myanmar',         'saudi-arabia'): 'Yangon',
    ('laos',            'saudi-arabia'): 'Bangkok',
    ('tanzania',        'saudi-arabia'): 'Dar es Salaam',
    # R48: Australia wave 6
    ('ethiopia',        'australia'): 'Addis Ababa',
    ('morocco',         'australia'): 'Rabat',
    ('sudan',           'australia'): 'Nairobi',
    ('eritrea',         'australia'): 'Nairobi',
    ('russia',          'australia'): 'Moscow',
    # R48: Canada wave 6
    ('lebanon',         'canada'): 'Beirut',
    ('syria',           'canada'): 'Beirut',
    ('algeria',         'canada'): 'Algiers',
    ('indonesia',       'canada'): 'Jakarta',
    ('myanmar',         'canada'): 'Yangon',
    # R48: India wave 6 (Gulf states)
    ('saudi-arabia',    'india'): 'Riyadh',
    ('kuwait',          'india'): 'Kuwait City',
    ('qatar',           'india'): 'Doha',
    ('oman',            'india'): 'Muscat',
    ('bahrain',         'india'): 'Manama',
    # R48: Qatar wave 5
    ('russia',          'qatar'): 'Moscow',
    ('uzbekistan',      'qatar'): 'Tashkent',
    ('azerbaijan',      'qatar'): 'Baku',
    ('georgia',         'qatar'): 'Tbilisi',
    ('armenia',         'qatar'): 'Yerevan',
    # R48: Kuwait wave 6
    ('azerbaijan',      'kuwait'): 'Baku',
    ('georgia',         'kuwait'): 'Tbilisi',
    ('armenia',         'kuwait'): 'Yerevan',
    ('mozambique',      'kuwait'): 'Nairobi',
    ('tanzania',        'kuwait'): 'Nairobi',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R47: USA wave 7
    ('malaysia', 'united-states'): (
        "Malaysian nationals in the United States include students, academics, "
        "and professionals in technology and financial services sectors. Malaysia "
        "and the United States have close trade and security ties through the "
        "ASEAN framework, and a significant number of Malaysians pursue higher "
        "education in the US each year. Malay documentation requires certified "
        "English translation for US state-level civil registration purposes. "
        "The US Embassy in Kuala Lumpur handles consular matters. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('thailand', 'united-states'): (
        "Thai nationals in the United States include a large diaspora community "
        "concentrated in California, Texas, and New York, alongside students and "
        "professionals. Thailand and the United States are treaty allies under the "
        "1954 Manila Pact, with close security, trade, and academic ties. Thai "
        "documentation requires certified English translation for US state-level "
        "civil registration purposes. The US Embassy in Bangkok handles consular "
        "matters. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('sri-lanka', 'united-states'): (
        "Sri Lankan nationals form an established diaspora community in the United "
        "States, concentrated in New York, New Jersey, and California. Sri Lanka "
        "and the United States have bilateral diplomatic ties and significant "
        "numbers of Sri Lankans, both Sinhalese and Tamil, have settled in the US "
        "over several decades. Sinhala and Tamil documentation requires certified "
        "English translation for US state-level civil registration purposes. "
        "The US Embassy in Colombo handles consular matters."
    ),
    ('hong-kong', 'united-states'): (
        "Hong Kong nationals in the United States include a long-established "
        "diaspora community concentrated in California and New York, alongside "
        "a newer wave of emigrants following Hong Kong's political changes since "
        "2019. The United States has the Hong Kong Policy Act and has offered "
        "protective status to Hong Kong residents. Traditional Chinese documentation "
        "from Hong Kong requires certified English translation for US state-level "
        "civil registration purposes. The US Consulate General in Hong Kong "
        "handles consular matters. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('panama', 'united-states'): (
        "Panamanians in the United States include professionals, students, and a "
        "diaspora community in Florida and the New York area. The United States and "
        "Panama have longstanding bilateral ties through the former US administration "
        "of the Panama Canal and the US-Panama Free Trade Agreement. Spanish "
        "documentation from Panama requires certified English translation for US "
        "state-level civil registration purposes. The US Embassy in Panama City "
        "handles consular matters."
    ),
    # R47: Germany wave 8
    ('rwanda', 'germany'): (
        "Rwandan nationals in Germany include students, academics, and a small "
        "professional community. Germany and Rwanda have bilateral development "
        "cooperation ties and diplomatic relations, with Germany a significant "
        "aid partner for Rwanda. Notably, Kinyarwanda is taught alongside French "
        "and English in Rwandan schools, reflecting varied international ties. "
        "Kinyarwanda and French documentation from Rwanda requires certified German "
        "translation for Standesamt (civil registry) purposes. The German Embassy "
        "in Kigali handles consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    ('tanzania', 'germany'): (
        "Tanzanian nationals in Germany include students, academics, and a small "
        "diaspora community. Germany and Tanzania have longstanding bilateral ties "
        "dating from the colonial period, when the territory was known as German "
        "East Africa. Germany remains a significant development and academic partner "
        "for Tanzania. Swahili and English documentation from Tanzania requires "
        "certified German translation for Standesamt (civil registry) purposes. "
        "The German Embassy in Dar es Salaam handles consular matters."
    ),
    ('mozambique', 'germany'): (
        "Mozambican nationals in Germany form a notable community, including "
        "descendants of the Vertragsarbeiter (contract workers) who came to East "
        "Germany under a 1979 solidarity agreement between the GDR and Mozambique. "
        "An established Mozambican community has remained in unified Germany since "
        "1990. Germany is a significant bilateral aid partner for Mozambique. "
        "Portuguese documentation from Mozambique requires certified German "
        "translation for Standesamt purposes. The German Embassy in Maputo handles "
        "consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    ('angola', 'germany'): (
        "Angolan nationals in Germany include students, professionals, and former "
        "Vertragsarbeiter (contract workers) who came to East Germany under "
        "solidarity agreements, alongside their descendants. Germany and Angola "
        "have bilateral diplomatic and development ties. Portuguese documentation "
        "from Angola requires certified German translation for Standesamt (civil "
        "registry) purposes. The German Embassy in Luanda handles consular matters."
    ),
    ('laos', 'germany'): (
        "Laotian nationals in Germany include refugees and their descendants who "
        "came to Germany in the 1970s and 1980s following political change in Laos, "
        "alongside students and a small professional community. Germany and Laos "
        "have bilateral development cooperation ties. Lao documentation requires "
        "certified German translation for Standesamt (civil registry) purposes. "
        "The German Embassy in Vientiane handles consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    # R47: France wave 7
    ('iran', 'france'): (
        "Iranian nationals form one of the largest Middle Eastern diaspora "
        "communities in France, concentrated in Paris and other major cities. "
        "France has been a significant destination for Iranian emigration since "
        "1979, and the French Iranian community is well-established across "
        "academic, artistic, and professional sectors. France maintains diplomatic "
        "relations with Iran and has an embassy in Tehran, though consular access "
        "should be confirmed given the state of bilateral relations. Farsi "
        "documentation requires certified French translation for French civil "
        "registry purposes. The French Embassy in Tehran handles consular matters. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    ('afghanistan', 'france'): (
        "Afghan nationals in France include refugees, asylum seekers granted "
        "protection, and a well-established diaspora community in Paris and Lyon. "
        "France accepted significant numbers of Afghan nationals, including those "
        "evacuated following the 2021 Taliban takeover. The French Embassy in "
        "Kabul suspended operations in August 2021; families in Afghanistan "
        "requiring French consular support should contact the French Ministry of "
        "Europe and Foreign Affairs emergency service in Paris at "
        "+33 1 43 17 67 67. Dari and Pashto documentation requires certified "
        "French translation for French civil registry purposes."
    ),
    ('poland', 'france'): (
        "Polish nationals in France form one of the largest Eastern European "
        "communities, with historical roots going back to 19th-century political "
        "emigrations and a larger wave following Poland's EU accession in 2004. "
        "Poland and France are both EU and NATO member states with deep bilateral "
        "diplomatic and economic ties. Polish documentation requires certified "
        "French translation for French prefecture and civil registry purposes. "
        "The French Embassy in Warsaw handles consular matters. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    ('romania', 'france'): (
        "Romanian nationals form one of the largest European communities in France, "
        "with hundreds of thousands of Romanians living and working in France "
        "following Romania's EU accession in 2007. France is one of the primary "
        "destinations for Romanian economic migration within the EU. Both countries "
        "share French as part of the Francophone world. Romanian documentation "
        "requires certified French translation for French prefecture and civil "
        "registry purposes. The French Embassy in Bucharest handles consular matters."
    ),
    ('ukraine', 'france'): (
        "Ukrainian nationals in France include those who sought refuge following "
        "the 2022 Russian invasion, granted temporary protection under the EU "
        "Temporary Protection Directive, alongside an established pre-war diaspora "
        "of professionals and students. France has been a significant host country "
        "for Ukrainian displaced persons. Ukrainian documentation requires certified "
        "French translation for French prefecture and civil registry purposes. "
        "The French Embassy in Kyiv continues to operate. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    # R47: UAE wave 7
    ('guinea', 'united-arab-emirates'): (
        "Guinean nationals in the UAE include workers in service and construction "
        "sectors and a small trading community. Guinea and the UAE have diplomatic "
        "relations, and Gulf states have become destinations for West African workers. "
        "Guinean documentation in French requires certified Arabic translation for "
        "UAE Ministry of Health and MOFAIC attestation purposes. The UAE Embassy "
        "in Conakry handles consular matters. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    ('ivory-coast', 'united-arab-emirates'): (
        "Ivorian nationals in the UAE include business professionals in trade and "
        "services, students, and workers. Ivory Coast and the UAE have bilateral "
        "economic ties, with UAE investment active across West Africa and the "
        "cocoa and commodities trade connecting the two economies. French "
        "documentation from Ivory Coast requires certified Arabic translation for "
        "UAE MOFAIC attestation purposes. The UAE Embassy in Abidjan handles "
        "consular matters."
    ),
    ('burkina-faso', 'united-arab-emirates'): (
        "Burkinabe nationals in the UAE include workers in service sectors and a "
        "small community of traders and professionals. Burkina Faso and the UAE "
        "have diplomatic relations. French and Mooré documentation from Burkina "
        "Faso requires certified Arabic translation for UAE Ministry of Health "
        "attestation purposes. The UAE Embassy in Abidjan covers Burkina Faso for "
        "consular matters; families should confirm current consular arrangements. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    ('laos', 'united-arab-emirates'): (
        "Laotian nationals in the UAE include workers in hospitality and domestic "
        "service sectors, and professionals in trade. Laos and the UAE have "
        "diplomatic relations and Southeast Asian workers are part of the Gulf "
        "labour market. Lao documentation requires certified Arabic translation "
        "for UAE Ministry of Health attestation purposes. The UAE Embassy in "
        "Bangkok covers Laos for consular matters."
    ),
    ('cambodia', 'united-arab-emirates'): (
        "Cambodian nationals in the UAE include workers in hospitality, domestic "
        "service, and construction sectors. Cambodia and the UAE have bilateral "
        "labour and diplomatic ties, and Cambodian workers are deployed to Gulf "
        "states under Cambodia's overseas employment programme. Khmer documentation "
        "requires certified Arabic translation for UAE MOFAIC attestation purposes. "
        "The UAE Embassy in Phnom Penh handles consular matters. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    # R47: Saudi Arabia wave 7
    ('russia', 'saudi-arabia'): (
        "Russian nationals in Saudi Arabia include business professionals in the "
        "energy, construction, and trade sectors, as well as tourists. Russia and "
        "Saudi Arabia have strengthened bilateral ties, cooperating on oil production "
        "policy through the OPEC+ framework, and bilateral trade has grown. Saudi "
        "Arabia and Russia restored full diplomatic relations and the Saudi Embassy "
        "in Moscow operates normally. Russian documentation requires certified "
        "Arabic translation for Saudi Ministry of Health purposes. The Saudi "
        "Embassy in Moscow handles consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('uzbekistan', 'saudi-arabia'): (
        "Uzbek nationals in Saudi Arabia include pilgrims for Hajj and Umrah, "
        "workers in the service and construction sectors, and professionals. "
        "Uzbekistan and Saudi Arabia have close bilateral ties as fellow "
        "Muslim-majority nations, and Saudi Arabia is one of the most significant "
        "religious destinations for Uzbek nationals. Deaths among Uzbek pilgrims "
        "during Hajj are handled through established procedures between Saudi "
        "authorities and the Uzbek Embassy. Uzbek documentation requires certified "
        "Arabic translation. The Saudi Embassy in Tashkent handles consular matters."
    ),
    ('myanmar', 'saudi-arabia'): (
        "Myanmar nationals in Saudi Arabia include Muslim workers from the Rakhine "
        "region and Rohingya community employed in service and domestic sectors, "
        "alongside professionals. Myanmar and Saudi Arabia have diplomatic relations "
        "and the Gulf states are a significant destination for Myanmar Muslim "
        "workers. Burmese documentation requires certified Arabic translation for "
        "Saudi Ministry of Health purposes. The Saudi Embassy in Yangon handles "
        "consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('laos', 'saudi-arabia'): (
        "Laotian nationals in Saudi Arabia include Muslim workers from Laos and "
        "professionals in service sectors. Laos and Saudi Arabia have diplomatic "
        "relations. Lao documentation requires certified Arabic translation for "
        "Saudi Ministry of Health purposes. The Saudi Embassy in Bangkok covers "
        "Laos for consular matters; families should confirm current arrangements."
    ),
    ('tanzania', 'saudi-arabia'): (
        "Tanzanian nationals in Saudi Arabia include a significant community of "
        "Muslim workers, religious pilgrims for Hajj and Umrah, and professionals "
        "in service sectors. Tanzania has a large Muslim population and Saudi "
        "Arabia is a key destination for Tanzanian pilgrims. Deaths among Tanzanian "
        "pilgrims during Hajj follow established procedures between Saudi authorities "
        "and the Tanzanian High Commission. Swahili documentation requires certified "
        "Arabic translation. The Saudi Embassy in Dar es Salaam handles consular "
        "matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    # R48: Australia wave 6
    ('ethiopia', 'australia'): (
        "Ethiopian nationals in Australia form a growing diaspora community "
        "concentrated in Melbourne and Sydney, with significant numbers arriving "
        "since the late 1990s through humanitarian and family migration programmes. "
        "Australia and Ethiopia have bilateral diplomatic ties and Australia provides "
        "development assistance to Ethiopia. Ethiopian Airlines operates direct "
        "routes from Addis Ababa to Melbourne, strengthening bilateral links. "
        "Amharic documentation requires certified English translation for Australian "
        "state or territory registration purposes. The Australian Embassy in Addis "
        "Ababa handles consular matters. "
        "(Australian Government, Department of Foreign Affairs and Trade, DFAT, 2025.)"
    ),
    ('morocco', 'australia'): (
        "Moroccan nationals in Australia include students, professionals, and a "
        "small established diaspora community in Sydney and Melbourne. Australia "
        "and Morocco have bilateral trade ties and diplomatic relations. Arabic and "
        "French documentation from Morocco requires certified English translation "
        "for Australian state or territory civil registration purposes. The "
        "Australian Embassy in Rabat handles consular matters."
    ),
    ('sudan', 'australia'): (
        "Sudanese nationals form one of the most established African communities "
        "in Australia, concentrated in Melbourne, Sydney, and Adelaide. Australia "
        "granted protection to significant numbers of Sudanese refugees from the "
        "1990s onward, resettling Sudanese families fleeing successive conflicts. "
        "The Australian Embassy operations in Khartoum have been affected by the "
        "2023 civil conflict in Sudan; the Australian Embassy covering Sudan "
        "operates from Nairobi. Families should contact the Consular Emergency "
        "Centre at +61 2 6261 3305. Arabic documentation requires certified English "
        "translation. "
        "(Australian Government, Department of Foreign Affairs and Trade, DFAT, 2025.)"
    ),
    ('eritrea', 'australia'): (
        "Eritrean nationals in Australia include refugees and humanitarian entrants "
        "who have settled in Melbourne, Sydney, and other cities over many years. "
        "Australia has accepted Eritrean refugees through humanitarian programmes. "
        "Tigrinya and Arabic documentation from Eritrea requires certified English "
        "translation for Australian state or territory registration purposes. The "
        "Australian Embassy covering Eritrea operates from Nairobi; families should "
        "contact the Consular Emergency Centre at +61 2 6261 3305."
    ),
    ('russia', 'australia'): (
        "Russian nationals in Australia include an established diaspora community, "
        "professionals in academic and technology sectors, and former students. "
        "Australia and Russia have maintained diplomatic relations, and the "
        "Australian Embassy in Moscow continues to operate. Russian documentation "
        "requires certified English translation for Australian state or territory "
        "civil registration purposes. The Australian Embassy in Moscow handles "
        "consular matters. "
        "(Australian Government, Department of Foreign Affairs and Trade, DFAT, 2025.)"
    ),
    # R48: Canada wave 6
    ('lebanon', 'canada'): (
        "Lebanese Canadians form one of the largest Arab communities in Canada, "
        "concentrated in Montreal, Toronto, and Ottawa, with an established "
        "community spanning several generations of migration. Canada and Lebanon "
        "have strong people-to-people connections and Canada evacuated thousands "
        "of Lebanese Canadians during the 2006 conflict. Arabic documentation from "
        "Lebanon requires certified English or French translation for Canadian "
        "provincial registration purposes. The Canadian Embassy in Beirut handles "
        "consular matters. "
        "(Global Affairs Canada, 2025.)"
    ),
    ('syria', 'canada'): (
        "Syrian nationals in Canada include a substantial refugee community resettled "
        "under the Canadian Government's Syrian refugee programme from 2015, which "
        "brought over 40,000 Syrians to Canada, alongside an established pre-war "
        "diaspora in Montreal, Toronto, and other cities. Canada closed its Damascus "
        "Embassy in 2012; the Canadian Embassy in Beirut covers Syria for consular "
        "matters. Arabic documentation from Syria requires certified English or "
        "French translation for Canadian provincial registration purposes."
    ),
    ('algeria', 'canada'): (
        "Algerian nationals in Canada form a notable diaspora community concentrated "
        "in Montreal and other Quebec cities. Quebec's French-speaking character "
        "has historically made Canada an attractive destination for Algerian "
        "emigration, and the Algerian community in Montreal is well-established. "
        "Arabic and French documentation from Algeria requires certified English "
        "or French translation for Canadian provincial registration purposes. "
        "The Canadian Embassy in Algiers handles consular matters. "
        "(Global Affairs Canada, 2025.)"
    ),
    ('indonesia', 'canada'): (
        "Indonesian nationals in Canada include students, professionals, and a "
        "small diaspora community. Canada and Indonesia have bilateral diplomatic "
        "and trade ties, with Canada a destination for Indonesian students "
        "pursuing higher education. Indonesian documentation requires certified "
        "English or French translation for Canadian provincial registration "
        "purposes. The Canadian Embassy in Jakarta handles consular matters."
    ),
    ('myanmar', 'canada'): (
        "Myanmar nationals in Canada include refugees granted protection in Canada "
        "over many years, alongside professionals and students. Canada has been a "
        "significant resettlement country for Myanmar refugees from various "
        "communities, including Burmese and Karen ethnic groups. Canada's commitment "
        "to refugee resettlement makes it one of the larger Western destinations "
        "for Myanmar nationals. The Canadian Embassy in Yangon handles consular "
        "matters. "
        "(Global Affairs Canada, 2025.)"
    ),
    # R48: India wave 6 (Gulf states as origins, India as destination)
    ('saudi-arabia', 'india'): (
        "Indian nationals form the largest expatriate community in Saudi Arabia, "
        "with several million Indian workers and professionals employed across "
        "construction, healthcare, domestic service, and retail. Deaths among "
        "Indian workers in Saudi Arabia represent some of the most frequent "
        "repatriation cases handled by Indian missions abroad. The Indian Embassy "
        "in Riyadh and the Consulate General in Jeddah process death certificates "
        "and consular documentation. Arabic documentation from Saudi Arabia requires "
        "certified English or Hindi translation for Indian civil registrar purposes "
        "under the Registration of Births and Deaths Act 1969. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    ('kuwait', 'india'): (
        "Indian nationals form the largest expatriate community in Kuwait, employed "
        "across construction, healthcare, domestic service, professional, and retail "
        "sectors. Kuwait has hosted Indian workers since the 1960s oil boom, and "
        "the Indian community is one of the most established in the Gulf. Deaths "
        "among Indian workers in Kuwait are handled through the Indian Embassy in "
        "Kuwait City. Arabic documentation from Kuwait requires certified English "
        "or Hindi translation for Indian civil registrar purposes under the "
        "Registration of Births and Deaths Act 1969. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    ('qatar', 'india'): (
        "Indian nationals form a large part of Qatar's expatriate workforce, "
        "employed in construction, hospitality, domestic service, and professional "
        "sectors. Qatar and India have close bilateral ties, and India is one of "
        "Qatar's most significant bilateral partners for labour and trade. The "
        "Indian Embassy in Doha processes death documentation for Indian nationals "
        "who die in Qatar. Arabic documentation from Qatar requires certified "
        "English or Hindi translation for Indian civil registrar purposes under "
        "the Registration of Births and Deaths Act 1969."
    ),
    ('oman', 'india'): (
        "Indian nationals are the single largest expatriate community in Oman, "
        "with a presence dating back centuries through the Indian Ocean trading "
        "network. Hundreds of thousands of Indian workers are employed across "
        "all sectors of the Omani economy. The Indian Embassy in Muscat and "
        "the Consulate General in Salalah process death documentation for Indian "
        "nationals who die in Oman. Arabic documentation from Oman requires "
        "certified English or Hindi translation for Indian civil registrar purposes "
        "under the Registration of Births and Deaths Act 1969. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    ('bahrain', 'india'): (
        "Indian nationals form one of the largest communities in Bahrain, employed "
        "across hospitality, construction, retail, and professional sectors, with "
        "long-established business families and trading connections. Bahrain and "
        "India have bilateral ties through the India-Gulf Cooperation Council "
        "framework, and the Indian community in Bahrain is one of the most "
        "established in the Gulf. The Indian Embassy in Manama processes death "
        "documentation for Indian nationals who die in Bahrain. Arabic documentation "
        "from Bahrain requires certified English or Hindi translation for Indian "
        "civil registrar purposes under the Registration of Births and Deaths "
        "Act 1969."
    ),
    # R48: Qatar wave 5
    ('russia', 'qatar'): (
        "Russian nationals in Qatar include business professionals in the energy "
        "and financial sectors, sports enthusiasts, and tourists. Qatar and Russia "
        "have bilateral economic ties in the liquefied natural gas sector, both "
        "being major global exporters. The 2022 FIFA World Cup drew significant "
        "Russian visitor interest prior to sanctions. Russian documentation requires "
        "certified Arabic translation for Qatar Ministry of Public Health attestation "
        "purposes. The Qatar Embassy in Moscow handles consular matters. "
        "(Qatar Ministry of Foreign Affairs, 2025.)"
    ),
    ('uzbekistan', 'qatar'): (
        "Uzbek nationals in Qatar include workers in construction, hospitality, and "
        "service sectors, part of the Central Asian labour migration to the Gulf. "
        "Uzbekistan and Qatar have bilateral ties and Gulf states are significant "
        "destinations for Uzbek workers. The FIFA 2022 World Cup construction phase "
        "drew Central Asian workers to Qatar. Uzbek documentation requires certified "
        "Arabic translation for Qatar Ministry of Public Health attestation purposes. "
        "The Qatar Embassy in Tashkent handles consular matters."
    ),
    ('azerbaijan', 'qatar'): (
        "Azerbaijani nationals in Qatar include professionals in the energy and "
        "financial sectors, alongside business travellers. Azerbaijan and Qatar are "
        "both significant hydrocarbon producers with bilateral economic cooperation "
        "in the Gulf. Azerbaijani documentation requires certified Arabic translation "
        "for Qatar Ministry of Public Health attestation purposes. The Qatar Embassy "
        "in Baku handles consular matters. "
        "(Qatar Ministry of Foreign Affairs, 2025.)"
    ),
    ('georgia', 'qatar'): (
        "Georgian nationals in Qatar include workers in construction, hospitality, "
        "and domestic service sectors. Georgia and Qatar have bilateral diplomatic "
        "ties and Georgian workers are part of the broader labour migration from "
        "the Caucasus region to Gulf states. Georgian documentation requires "
        "certified Arabic translation for Qatar Ministry of Public Health attestation "
        "purposes. The Qatar Embassy in Tbilisi handles consular matters."
    ),
    ('armenia', 'qatar'): (
        "Armenian nationals in Qatar include professionals and workers in trade, "
        "construction, and service sectors. Armenia and Qatar have diplomatic "
        "relations and the Armenian community in the Gulf includes both workers "
        "and long-established merchants. Armenian documentation requires certified "
        "Arabic translation for Qatar Ministry of Public Health attestation purposes. "
        "The Qatar Embassy in Yerevan handles consular matters. "
        "(Qatar Ministry of Foreign Affairs, 2025.)"
    ),
    # R48: Kuwait wave 6
    ('azerbaijan', 'kuwait'): (
        "Azerbaijani nationals in Kuwait include professionals in the energy and "
        "construction sectors, alongside business travellers. Azerbaijan and Kuwait "
        "are both significant oil producers with bilateral economic ties through "
        "OPEC cooperation. Azerbaijani documentation requires certified Arabic "
        "translation for Kuwaiti Ministry of Interior purposes. The Kuwaiti Embassy "
        "in Baku handles consular matters. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    ('georgia', 'kuwait'): (
        "Georgian nationals in Kuwait include workers in domestic service, "
        "hospitality, and construction sectors, alongside business professionals. "
        "Georgia and Kuwait have bilateral diplomatic ties. Georgian workers are "
        "part of the broader Caucasus labour migration to Gulf states. Georgian "
        "documentation requires certified Arabic translation for Kuwaiti Ministry "
        "of Interior purposes. The Kuwaiti Embassy in Tbilisi handles consular "
        "matters."
    ),
    ('armenia', 'kuwait'): (
        "Armenian nationals in Kuwait include professionals and traders, with an "
        "established Armenian community active in business and trade sectors. "
        "Armenia and Kuwait have diplomatic relations. Armenian documentation "
        "requires certified Arabic translation for Kuwaiti Ministry of Interior "
        "purposes. The Kuwaiti Embassy in Yerevan handles consular matters. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    ('mozambique', 'kuwait'): (
        "Mozambican nationals in Kuwait are a small community. Mozambique and "
        "Kuwait have diplomatic relations as OAU and Organisation of Islamic "
        "Cooperation member states. Portuguese documentation from Mozambique "
        "requires certified Arabic translation for Kuwaiti Ministry of Interior "
        "purposes. The Kuwaiti Embassy covering Mozambique operates from Nairobi; "
        "families should confirm current consular arrangements."
    ),
    ('tanzania', 'kuwait'): (
        "Tanzanian nationals in Kuwait include workers in domestic service and "
        "professional sectors. Tanzania and Kuwait are both OIC member states, "
        "and Kuwait has provided development assistance to Tanzania. Swahili "
        "documentation from Tanzania requires certified Arabic translation for "
        "Kuwaiti Ministry of Interior purposes. The Kuwaiti Embassy covering "
        "Tanzania operates from Nairobi; families should confirm current "
        "consular arrangements. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
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
# Route list: R47 (25) + R48 (25) = 50 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R47: USA wave 7 x5 + Germany wave 8 x5 + France wave 7 x5 +
    #     UAE wave 7 x5 + Saudi Arabia wave 7 x5 = 25
    ('malaysia',        'united-states'),
    ('thailand',        'united-states'),
    ('sri-lanka',       'united-states'),
    ('hong-kong',       'united-states'),
    ('panama',          'united-states'),
    ('rwanda',          'germany'),
    ('tanzania',        'germany'),
    ('mozambique',      'germany'),
    ('angola',          'germany'),
    ('laos',            'germany'),
    ('iran',            'france'),
    ('afghanistan',     'france'),
    ('poland',          'france'),
    ('romania',         'france'),
    ('ukraine',         'france'),
    ('guinea',          'united-arab-emirates'),
    ('ivory-coast',     'united-arab-emirates'),
    ('burkina-faso',    'united-arab-emirates'),
    ('laos',            'united-arab-emirates'),
    ('cambodia',        'united-arab-emirates'),
    ('russia',          'saudi-arabia'),
    ('uzbekistan',      'saudi-arabia'),
    ('myanmar',         'saudi-arabia'),
    ('laos',            'saudi-arabia'),
    ('tanzania',        'saudi-arabia'),
    # --- Block R48: Australia wave 6 x5 + Canada wave 6 x5 + India wave 6 (Gulf) x5 +
    #     Qatar wave 5 x5 + Kuwait wave 6 x5 = 25
    ('ethiopia',        'australia'),
    ('morocco',         'australia'),
    ('sudan',           'australia'),
    ('eritrea',         'australia'),
    ('russia',          'australia'),
    ('lebanon',         'canada'),
    ('syria',           'canada'),
    ('algeria',         'canada'),
    ('indonesia',       'canada'),
    ('myanmar',         'canada'),
    ('saudi-arabia',    'india'),
    ('kuwait',          'india'),
    ('qatar',           'india'),
    ('oman',            'india'),
    ('bahrain',         'india'),
    ('russia',          'qatar'),
    ('uzbekistan',      'qatar'),
    ('azerbaijan',      'qatar'),
    ('georgia',         'qatar'),
    ('armenia',         'qatar'),
    ('azerbaijan',      'kuwait'),
    ('georgia',         'kuwait'),
    ('armenia',         'kuwait'),
    ('mozambique',      'kuwait'),
    ('tanzania',        'kuwait'),
]


def main():
    variant_idx = START_VARIANT
    built = []
    skipped = []

    for origin, dest in ALL_ROUTES:
        slug = f'{origin}-to-{dest}'
        out_path = os.path.join(ROUTES_DIR, f'{slug}.md')

        if os.path.exists(out_path):
            print(f"  SKIP (exists): {slug}")
            skipped.append(slug)
            variant_idx = (variant_idx + 1) % 5
            continue

        variant = VARIANTS[variant_idx % 5]
        content = make_route(origin, dest, variant)
        if content is None:
            print(f"  FAIL: {slug}")
            variant_idx = (variant_idx + 1) % 5
            continue

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  OK [{variant}]: {slug}")
        built.append((slug, variant))
        variant_idx = (variant_idx + 1) % 5

    print(f"\nDone. Built: {len(built)}, Skipped: {len(skipped)}")
    if built:
        print("Built routes:")
        for s, v in built:
            print(f"  [{v}] {s}")


if __name__ == '__main__':
    main()
