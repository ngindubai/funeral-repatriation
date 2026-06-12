#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R41-R42.

   R41: Kuwait wave 4 x5 + Qatar wave 4 x5 + India wave 4 x5 +
        Turkey wave 1 (NEW HUB) x5 + Malaysia wave 1 (NEW HUB) x5 = 25

   R42: Turkey wave 2 x5 + Malaysia wave 2 x5 + South Africa wave 5 x5 +
        Saudi Arabia wave 6 x5 + UAE wave 6 x5 = 25

   Template rotation: R40 ended on C (index 2). R41 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R40 ended C (index 2); R41 starts D (index 3)

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
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
    'qatar': {
        'name': 'Qatar',
        'slug': 'qatar',
        'key': 'qa',
        'reception': (
            "The Qatari funeral director takes custody at Hamad International Airport "
            "(DOH) cargo terminal. The Qatar Ministry of Public Health must grant clearance "
            "before the remains are received. A transit permit and embalming certificate "
            "must accompany the remains. The Ministry of Interior registers the death. "
            "All foreign documents not in Arabic require certified Arabic translation and "
            "authentication by the Qatari Embassy in the country of origin. "
            "(Qatari Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Qatari Embassy in {city} can advise on documentation requirements for "
            "repatriation to Qatar. Qatari Ministry of Foreign Affairs emergency "
            "line: +974 4441 7000 (24 hours). The Qatari Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Qatari funeral director takes custody at Hamad International Airport "
            "(DOH) cargo terminal. Qatar Ministry of Public Health clearance is required "
            "in advance. All documents must be authenticated by the Qatari Embassy in "
            "the origin country and require certified Arabic translation. The receiving "
            "funeral director coordinates with the Ministry of Interior."
        ),
        'emergency_line': '+974 4441 7000',
        'hub_url': 'repatriation-from-qatar',
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
    'united-arab-emirates': {
        'name': 'United Arab Emirates',
        'slug': 'united-arab-emirates',
        'key': 'ae',
        'reception': (
            "The UAE funeral director takes custody at Dubai International (DXB), Abu "
            "Dhabi International (AUH), or Sharjah International (SHJ) cargo terminal. "
            "The UAE Ministry of Health and Prevention (MOHAP) must grant clearance "
            "before burial or cremation. A No Objection Certificate from the General "
            "Directorate of Residency and Foreigners Affairs (GDRFA) is required. All "
            "foreign documents must be authenticated by the UAE Embassy in the country "
            "of origin. Documents not in Arabic or English require certified translation. "
            "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
        ),
        'consular_template': (
            "UAE Embassy or Consulate in {city} can advise on documentation requirements "
            "for repatriation to the UAE. UAE Ministry of Foreign Affairs and "
            "International Cooperation (MOFAIC) emergency line: +971 2 495 0000 "
            "(24 hours). The UAE Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The UAE funeral director takes custody at Dubai (DXB), Abu Dhabi (AUH), "
            "or Sharjah (SHJ) cargo terminal. MOHAP clearance and a GDRFA No Objection "
            "Certificate are required in advance. All foreign documents must be "
            "authenticated by the UAE Embassy in the origin country. The receiving "
            "funeral director coordinates with local health authorities."
        ),
        'emergency_line': '+971 2 495 0000',
        'hub_url': 'repatriation-from-united-arab-emirates',
    },
    'turkey': {
        'name': 'Turkey',
        'slug': 'turkey',
        'key': 'tr',
        'reception': (
            "The Turkish funeral director (cenaze firması) takes custody at Istanbul "
            "Airport (IST) or Istanbul Sabiha Gokcen (SAW) cargo terminal. A transit "
            "certificate (transit belgesi) must accompany the remains. The municipality "
            "(belediye) registers the death in the nüfus müdürlüğü (population "
            "directorate). The Turkish Ministry of Health clearance is required before "
            "burial or cremation. All foreign documents not in Turkish require certified "
            "Turkish translation. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Turkish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Turkey. Turkish Ministry of Foreign Affairs emergency "
            "line: +90 312 292 2000 (24 hours). The Turkish Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Turkish funeral director (cenaze firması) takes custody at Istanbul "
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
    'saudi-arabia': {
        'name': 'Saudi Arabia',
        'slug': 'saudi-arabia',
        'key': 'sa',
        'reception': (
            "The Saudi government mortuary or funeral home takes custody at King Khalid "
            "International (RUH, Riyadh), King Abdulaziz International (JED, Jeddah), "
            "or King Fahd International (DMM, Dammam) cargo terminal. Saudi Ministry of "
            "Health approval is required before the remains can be received. All documents "
            "must be authenticated by the Saudi Embassy in the country of origin. "
            "Non-Muslim remains require specific certification and procedures. "
            "(Saudi Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Saudi Embassy in {city} handles authentication of repatriation documents. "
            "Contact the Saudi Embassy in {country_name} for document legalisation "
            "requirements. Saudi Ministry of Foreign Affairs coordinates with the "
            "receiving authorities in Saudi Arabia."
        ),
        'arrival_faq': (
            "The Saudi government mortuary takes custody at King Khalid (RUH), King "
            "Abdulaziz (JED), or King Fahd (DMM) cargo terminal. Saudi Ministry of "
            "Health clearance is required in advance. All documents must be authenticated "
            "by the Saudi Embassy in the origin country. Non-Muslim remains require "
            "specific certification. The family or sponsor in Saudi Arabia coordinates "
            "with the receiving authorities."
        ),
        'emergency_line': 'contact Saudi Embassy in origin country',
        'hub_url': 'repatriation-from-saudi-arabia',
    },
}

# ---------------------------------------------------------------------------
# Embassy cities: destination country embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R41: Kuwait wave 4
    ('cameroon',        'kuwait'): 'Yaoundé',
    ('senegal',         'kuwait'): 'Dakar',
    ('myanmar',         'kuwait'): 'Yangon',
    ('iraq',            'kuwait'): 'Baghdad',
    # Kuwait Embassy covers Eritrea from Addis Ababa
    ('eritrea',         'kuwait'): 'Addis Ababa',
    # R41: Qatar wave 4
    ('cameroon',        'qatar'): 'Yaoundé',
    ('senegal',         'qatar'): 'Dakar',
    ('myanmar',         'qatar'): 'Yangon',
    ('iraq',            'qatar'): 'Baghdad',
    ('oman',            'qatar'): 'Muscat',
    # R41: India wave 4
    ('vietnam',         'india'): 'Hanoi',
    ('egypt',           'india'): 'Cairo',
    ('france',          'india'): 'Paris',
    ('germany',         'india'): 'Berlin',
    ('ghana',           'india'): 'Accra',
    # R41: Turkey wave 1 (new hub)
    # Turkish Embassy in Damascus closed since 2012; families directed to MFA in Ankara
    ('syria',           'turkey'): 'Ankara',
    ('iraq',            'turkey'): 'Baghdad',
    ('iran',            'turkey'): 'Tehran',
    ('azerbaijan',      'turkey'): 'Baku',
    ('georgia',         'turkey'): 'Tbilisi',
    # R41: Malaysia wave 1 (new hub)
    ('indonesia',       'malaysia'): 'Jakarta',
    ('bangladesh',      'malaysia'): 'Dhaka',
    ('philippines',     'malaysia'): 'Manila',
    ('myanmar',         'malaysia'): 'Naypyidaw',
    ('india',           'malaysia'): 'New Delhi',
    # R42: Turkey wave 2
    ('pakistan',        'turkey'): 'Islamabad',
    ('egypt',           'turkey'): 'Cairo',
    ('germany',         'turkey'): 'Berlin',
    ('morocco',         'turkey'): 'Rabat',
    ('ukraine',         'turkey'): 'Kyiv',
    # R42: Malaysia wave 2
    ('china',           'malaysia'): 'Beijing',
    ('vietnam',         'malaysia'): 'Hanoi',
    ('nepal',           'malaysia'): 'Kathmandu',
    ('thailand',        'malaysia'): 'Bangkok',
    ('cambodia',        'malaysia'): 'Phnom Penh',
    # R42: South Africa wave 5
    ('japan',           'south-africa'): 'Tokyo',
    ('italy',           'south-africa'): 'Rome',
    ('spain',           'south-africa'): 'Madrid',
    ('brazil',          'south-africa'): 'Brasilia',
    ('portugal',        'south-africa'): 'Lisbon',
    # R42: Saudi Arabia wave 6
    ('niger',           'saudi-arabia'): 'Niamey',
    ('guinea',          'saudi-arabia'): 'Conakry',
    ('benin',           'saudi-arabia'): 'Cotonou',
    ('gambia',          'saudi-arabia'): 'Banjul',
    ('liberia',         'saudi-arabia'): 'Monrovia',
    # R42: UAE wave 6
    ('djibouti',        'united-arab-emirates'): 'Djibouti City',
    ('togo',            'united-arab-emirates'): 'Lome',
    ('mali',            'united-arab-emirates'): 'Bamako',
    ('comoros',         'united-arab-emirates'): 'Moroni',
    ('turkmenistan',    'united-arab-emirates'): 'Ashgabat',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R41: Kuwait wave 4
    ('cameroon', 'kuwait'): (
        "Cameroonian nationals working in Kuwait are employed across service, hospitality, "
        "and construction sectors in Kuwait City and surrounding areas. Cameroon and Kuwait "
        "have bilateral diplomatic relations. French and English documentation from Cameroon "
        "requires certified Arabic translation for Kuwaiti Ministry of Interior purposes. "
        "The Kuwaiti Embassy in Yaoundé handles consular matters. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    ('senegal', 'kuwait'): (
        "Senegalese nationals in Kuwait work in trade and service sectors, with Senegal's "
        "Muslim majority creating a natural diaspora link to the Gulf. Senegal and Kuwait "
        "have bilateral ties as fellow Organisation of Islamic Cooperation (OIC) member "
        "states, and Kuwait has provided development assistance to Senegal. French and "
        "Wolof documentation from Senegal requires certified Arabic translation for "
        "Kuwaiti authorities. The Kuwaiti Embassy in Dakar handles consular matters."
    ),
    ('myanmar', 'kuwait'): (
        "Myanmar nationals form a growing worker community in Kuwait, employed in domestic "
        "service, hospitality, and construction sectors. Myanmar documentation in Burmese "
        "requires certified Arabic translation for Kuwaiti Ministry of Interior purposes. "
        "The Kuwaiti Embassy in Yangon handles consular matters. As with all worker "
        "corridors to the Gulf, death-in-service cases require the employer's assistance "
        "alongside consular support. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    ('iraq', 'kuwait'): (
        "Iraqi nationals in Kuwait form a community shaped by proximity and historical "
        "migration, with Iraq and Kuwait sharing a land border. Following the normalisation "
        "of bilateral relations, Iraqi nationals are employed in professional, trade, and "
        "service sectors in Kuwait. Arabic documentation from Iraq is generally understood "
        "by Kuwaiti authorities, though official notarisation and embassy authentication "
        "are required. The Kuwaiti Embassy in Baghdad handles consular matters."
    ),
    ('eritrea', 'kuwait'): (
        "Eritrean nationals working in Kuwait are employed in service and domestic sectors. "
        "Eritrea and Kuwait have diplomatic relations. Tigrinya documentation from Eritrea "
        "requires certified Arabic translation for Kuwaiti Ministry of Interior purposes. "
        "The Kuwaiti Embassy covers Eritrea from Addis Ababa; families should confirm "
        "current consular access arrangements. "
        "(Kuwaiti Ministry of Foreign Affairs, 2025.)"
    ),
    # R41: Qatar wave 4
    ('cameroon', 'qatar'): (
        "Cameroonian nationals in Qatar work in construction, hospitality, and service "
        "sectors across Doha and the wider country. Qatar and Cameroon have diplomatic "
        "ties, and the large-scale infrastructure development in Qatar has drawn workers "
        "from across West and Central Africa. French and English documentation from "
        "Cameroon requires certified Arabic translation for Qatari Ministry of Public "
        "Health and Ministry of Interior purposes. The Qatari Embassy in Yaoundé handles "
        "consular matters. "
        "(Qatari Ministry of Foreign Affairs, 2025.)"
    ),
    ('senegal', 'qatar'): (
        "Senegalese nationals in Qatar include workers in service, hospitality, and "
        "community roles. Senegal and Qatar have close ties as fellow OIC member states "
        "and Qatar has been a significant investor in Senegal's infrastructure. French "
        "and Wolof documentation from Senegal requires certified Arabic translation for "
        "Qatari authorities. The Qatari Embassy in Dakar handles consular matters."
    ),
    ('myanmar', 'qatar'): (
        "Myanmar nationals working in Qatar are employed in domestic service and "
        "construction sectors. Qatar is a significant employer of Southeast Asian "
        "migrant workers, with Myanmar joining the Gulf labour migration network in "
        "growing numbers. Burmese documentation requires certified Arabic translation "
        "for Qatari Ministry of Public Health clearance. The Qatari Embassy in Yangon "
        "handles consular matters. "
        "(Qatari Ministry of Foreign Affairs, 2025.)"
    ),
    ('iraq', 'qatar'): (
        "Iraqi nationals in Qatar work in professional, trade, and service sectors, "
        "with both countries sharing Gulf region proximity and Arab League membership. "
        "Qatar and Iraq have bilateral diplomatic ties and commercial relationships. "
        "Arabic documentation from Iraq is generally understood by Qatari authorities, "
        "though official notarisation and authentication by the Qatari Embassy are "
        "required. The Qatari Embassy in Baghdad handles consular matters."
    ),
    ('oman', 'qatar'): (
        "Omani nationals in Qatar form a Gulf Arab community with close cultural, "
        "linguistic, and commercial ties between two neighbouring GCC member states. "
        "Oman and Qatar share Arabic language and Islamic heritage and maintain strong "
        "bilateral relations. Arabic documentation from Oman is understood by Qatari "
        "authorities. The Qatari Embassy in Muscat handles consular matters. "
        "(Qatari Ministry of Foreign Affairs, 2025.)"
    ),
    # R41: India wave 4
    ('vietnam', 'india'): (
        "Vietnamese nationals in India include students on educational exchanges, "
        "businesspeople, and professionals working in joint ventures and trade. India "
        "and Vietnam have a Strategic Partnership, with bilateral trade growing across "
        "technology, pharmaceuticals, and manufacturing. Vietnamese documentation "
        "requires certified English translation for Indian civil registration purposes "
        "under the Registration of Births and Deaths Act 1969. The Indian Embassy in "
        "Hanoi handles consular matters. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    ('egypt', 'india'): (
        "Egyptian nationals in India include students at Indian universities, "
        "businesspeople, and professionals. India and Egypt have a Strategic Partnership "
        "and longstanding diplomatic ties as founding members of the Non-Aligned Movement. "
        "Bilateral trade and technology cooperation have expanded in recent years. Arabic "
        "documentation from Egypt requires certified English translation for Indian civil "
        "registration purposes. The Indian Embassy in Cairo handles consular matters."
    ),
    ('france', 'india'): (
        "French nationals in India include business executives, cultural professionals, "
        "diplomats, and researchers concentrated in Mumbai, Delhi, Bangalore, and Pondicherry. "
        "France and India have a Strategic Partnership covering defence, space cooperation, "
        "and cultural ties. French documentation requires certified English translation for "
        "Indian civil registration purposes. The Indian Embassy in Paris handles consular "
        "matters. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    ('germany', 'india'): (
        "German nationals in India include business executives, engineers, and professionals "
        "working in the automotive, chemicals, and manufacturing sectors. Germany and India "
        "have extensive bilateral trade and a longstanding strategic partnership, with German "
        "companies including Volkswagen, BASF, and Bayer maintaining significant India "
        "operations. German documentation requires certified English translation for Indian "
        "civil registration purposes. The Indian Embassy in Berlin handles consular matters."
    ),
    ('ghana', 'india'): (
        "Ghanaian nationals in India include students at Indian universities, businesspeople, "
        "and diaspora residents. India and Ghana have bilateral ties and India provides "
        "development cooperation and technical assistance to Ghana through the Indian "
        "Technical and Economic Cooperation (ITEC) programme. English documentation from "
        "Ghana is generally understood by Indian authorities, though authentication by the "
        "Indian High Commission may be required. The Indian High Commission in Accra handles "
        "consular matters. "
        "(Indian Ministry of External Affairs, 2025.)"
    ),
    # R41: Turkey wave 1 (new hub)
    ('syria', 'turkey'): (
        "Syria to Turkey is one of the most significant repatriation corridors in the "
        "region. Turkey hosts one of the world's largest Syrian refugee populations, with "
        "millions of Syrian nationals registered across Istanbul, Gaziantep, Hatay, Şanlıurfa, "
        "and other cities. Many Syrian families live permanently in Turkey, and a death "
        "within this community requires the Turkish civil authorities to register the event. "
        "Turkish consular representation inside Syria remains limited; the Turkish Embassy "
        "in Damascus has had suspended operations and families should contact the Turkish "
        "Ministry of Foreign Affairs directly on +90 312 292 2000. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('iraq', 'turkey'): (
        "Iraqi nationals form a substantial community in Turkey, concentrated in Istanbul, "
        "Ankara, and border provinces including Hatay and Gaziantep. Iraq and Turkey are "
        "neighbouring states sharing a long common border, and bilateral trade links are "
        "substantial. Arabic documentation from Iraq requires certified Turkish translation "
        "for Turkish civil registry (belediye) purposes. The Turkish Embassy in Baghdad "
        "handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('iran', 'turkey'): (
        "Iranian nationals form one of the largest foreign national communities in Turkey, "
        "with a significant diaspora in Istanbul, Ankara, and border provinces. Iran and "
        "Turkey share a long common border and extensive bilateral trade, including energy "
        "partnerships. Many Iranian nationals travel to Turkey for business, medical "
        "treatment, and tourism. Farsi documentation from Iran requires certified Turkish "
        "translation for Turkish civil registry purposes. The Turkish Embassy in Tehran "
        "handles consular matters."
    ),
    ('azerbaijan', 'turkey'): (
        "Azerbaijani nationals have uniquely close ties to Turkey through shared Turkic "
        "language, culture, and the bilateral relationship formalised in the Shusha "
        "Declaration of 2021, building on decades of partnership. Azerbaijan and Turkey "
        "describe their relationship as 'one nation, two states'. Many Azerbaijanis study, "
        "work, and reside in Turkey, with particularly strong ties in Istanbul and Ankara. "
        "Azerbaijani documentation is closely related to Turkish but requires certified "
        "translation for formal registry purposes. The Turkish Embassy in Baku handles "
        "consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('georgia', 'turkey'): (
        "Georgian nationals form a significant labour migrant community in Turkey, "
        "concentrated in Istanbul and the Black Sea coastal provinces of Trabzon and "
        "Artvin, given Georgia's shared border with Turkey. Georgia and Turkey have "
        "bilateral trade agreements and close economic ties. Many Georgian nationals "
        "work in trade, domestic service, and construction in Turkey. Georgian "
        "documentation in the Georgian script requires certified Turkish translation "
        "for Turkish civil registry purposes. The Turkish Embassy in Tbilisi handles "
        "consular matters."
    ),
    # R41: Malaysia wave 1 (new hub)
    ('indonesia', 'malaysia'): (
        "Indonesian nationals form the largest migrant worker community in Malaysia, "
        "with hundreds of thousands employed across plantation, domestic service, "
        "construction, and manufacturing sectors. Malaysia and Indonesia share Malay "
        "language ties, Islamic heritage, and ASEAN membership. Indonesia and Malaysia "
        "have bilateral labour agreements governing worker migration. Indonesian "
        "documentation in Bahasa Indonesia is closely related to Malay and is generally "
        "understood by Malaysian authorities, though certified translation may be required "
        "for official National Registration Department (NRD) purposes. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('bangladesh', 'malaysia'): (
        "Bangladeshi nationals form one of the largest migrant worker communities in "
        "Malaysia, employed in manufacturing, construction, and service sectors under "
        "bilateral labour agreements between the two countries. Malaysia and Bangladesh "
        "have longstanding labour migration ties. Bengali documentation from Bangladesh "
        "requires certified Malay or English translation for Malaysian National "
        "Registration Department (NRD) purposes. The Malaysian High Commission in Dhaka "
        "handles consular matters."
    ),
    ('philippines', 'malaysia'): (
        "Filipino nationals form a significant community in Malaysia, employed in domestic "
        "service, healthcare, and professional sectors, with a further population in the "
        "state of Sabah. Malaysia and the Philippines have ASEAN ties and bilateral "
        "agreements governing labour migration. English documentation from the Philippines "
        "is generally understood by Malaysian authorities, though NRD authentication is "
        "required. The Malaysian Embassy in Manila handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('myanmar', 'malaysia'): (
        "Myanmar nationals form a large migrant and refugee community in Malaysia, with "
        "significant numbers of Myanmar workers in plantation, construction, and service "
        "sectors alongside a registered refugee population recognised by UNHCR. Malaysia "
        "and Myanmar have bilateral ties through ASEAN. Burmese documentation requires "
        "certified Malay or English translation for Malaysian NRD purposes. The Malaysian "
        "Embassy in Naypyidaw handles consular matters."
    ),
    ('india', 'malaysia'): (
        "Indian nationals form one of Malaysia's oldest diaspora communities, rooted in "
        "the plantation labour history of the colonial era, with the Tamil community "
        "long established in Peninsular Malaysia. More recent migration includes "
        "professionals in finance, technology, and healthcare. India and Malaysia have "
        "bilateral trade ties and high-level diplomatic relations. Tamil and other "
        "Indian language documentation requires certified English or Malay translation "
        "for Malaysian NRD purposes. The Malaysian High Commission in New Delhi handles "
        "consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    # R42: Turkey wave 2
    ('pakistan', 'turkey'): (
        "Pakistani nationals form a growing diaspora in Turkey, concentrated in Istanbul, "
        "working in trade, hospitality, retail, and textile sectors. Pakistan and Turkey "
        "have longstanding diplomatic and defence ties and describe their relationship as "
        "among the closest between Muslim-majority nations. Urdu documentation from "
        "Pakistan requires certified Turkish translation for Turkish civil registry "
        "purposes. The Turkish Embassy in Islamabad handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('egypt', 'turkey'): (
        "Egyptian nationals form a significant community in Turkey, with a notable "
        "increase in migration to Istanbul following 2013. Egypt and Turkey have had "
        "complex but engaged bilateral relations, with diplomatic normalisation "
        "progressing since 2022. Arabic documentation from Egypt is not automatically "
        "understood by Turkish registry authorities and requires certified Turkish "
        "translation. The Turkish Embassy in Cairo handles consular matters."
    ),
    ('germany', 'turkey'): (
        "Germany to Turkey is one of the highest-volume tourist and cultural corridors "
        "in Europe, with millions of German tourists visiting Turkey annually. Germany "
        "also has a large Turkish-German community that maintains family ties in Turkey, "
        "making this a consistent bilateral repatriation corridor in both directions. "
        "German documentation requires certified Turkish translation for Turkish civil "
        "registry purposes. The Turkish Embassy in Berlin handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    ('morocco', 'turkey'): (
        "Moroccan nationals in Turkey include workers, students, and diaspora residents "
        "in Istanbul. Morocco and Turkey have bilateral diplomatic ties and trade "
        "agreements, and both countries are members of the Organisation of Islamic "
        "Cooperation. Arabic documentation from Morocco requires certified Turkish "
        "translation for Turkish civil registry purposes. The Turkish Embassy in Rabat "
        "handles consular matters."
    ),
    ('ukraine', 'turkey'): (
        "Ukrainian nationals form a growing community in Turkey, with significant numbers "
        "in Antalya and Istanbul following displacement from the 2022 Russian invasion. "
        "Turkey hosts a substantial number of Ukrainian refugees and has played a "
        "diplomatic role in the Ukraine conflict. Ukrainian documentation requires "
        "certified Turkish translation for Turkish civil registry purposes. The Turkish "
        "Embassy in Kyiv handles consular matters. "
        "(Turkish Ministry of Foreign Affairs, 2025.)"
    ),
    # R42: Malaysia wave 2
    ('china', 'malaysia'): (
        "Chinese nationals form a significant community in Malaysia, linked to the large "
        "ethnic Chinese Malaysian population and modern migration for business and "
        "education. Malaysia and China have extensive bilateral trade under the "
        "China-ASEAN Free Trade Agreement. Chinese Mandarin documentation requires "
        "certified Malay or English translation for Malaysian NRD purposes. The "
        "Malaysian Embassy in Beijing handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('vietnam', 'malaysia'): (
        "Vietnamese nationals in Malaysia include workers in manufacturing, electronics, "
        "and service sectors, alongside students on educational exchanges. Malaysia and "
        "Vietnam share ASEAN membership and bilateral trade ties. Vietnamese "
        "documentation requires certified Malay or English translation for Malaysian "
        "NRD purposes. The Malaysian Embassy in Hanoi handles consular matters."
    ),
    ('nepal', 'malaysia'): (
        "Nepali nationals form a significant migrant worker community in Malaysia, "
        "employed in manufacturing, construction, and service sectors under bilateral "
        "labour agreements. Malaysia and Nepal have a Memorandum of Understanding on "
        "labour migration. Nepali documentation in the Devanagari script requires "
        "certified Malay or English translation for Malaysian NRD purposes. The "
        "Malaysian High Commission in Kathmandu handles consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    ('thailand', 'malaysia'): (
        "Thai nationals in Malaysia include workers in the border economy, professionals, "
        "and tourists given the shared ASEAN membership and the 500-kilometre common "
        "border between Malaysia and Thailand. Many Thai nationals live and work in "
        "northern Malaysia, particularly in Kelantan and Perlis. Thai documentation "
        "requires certified Malay or English translation for Malaysian NRD purposes. "
        "The Malaysian Embassy in Bangkok handles consular matters."
    ),
    ('cambodia', 'malaysia'): (
        "Cambodian nationals in Malaysia include workers in manufacturing and service "
        "sectors, part of the ASEAN labour mobility network. Malaysia and Cambodia have "
        "ASEAN ties and bilateral agreements governing labour migration. Khmer "
        "documentation from Cambodia requires certified Malay or English translation "
        "for Malaysian NRD purposes. The Malaysian Embassy in Phnom Penh handles "
        "consular matters. "
        "(Malaysian Ministry of Foreign Affairs, 2025.)"
    ),
    # R42: South Africa wave 5
    ('japan', 'south-africa'): (
        "Japanese nationals in South Africa include business executives, automotive "
        "industry professionals, and tourists. Japanese companies including Toyota and "
        "other manufacturers have operations in South Africa, and Japanese tourists "
        "visit the country in growing numbers for safari and wildlife experiences. "
        "Japanese documentation requires certified English translation for South African "
        "Home Affairs purposes. The South African Embassy in Tokyo handles consular "
        "matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('italy', 'south-africa'): (
        "Italian nationals in South Africa include tourists, business professionals, "
        "and residents. South Africa is a popular destination for Italian tourists, and "
        "Italian companies are present in wine, agriculture, and luxury goods sectors. "
        "Italy and South Africa have bilateral diplomatic ties as fellow G20 members. "
        "Italian documentation requires certified English translation for South African "
        "Home Affairs purposes. The South African Embassy in Rome handles consular "
        "matters."
    ),
    ('spain', 'south-africa'): (
        "Spanish nationals in South Africa include business professionals, tourists, and "
        "residents drawn by climate and lifestyle. Spain and South Africa have bilateral "
        "diplomatic relations and share European Union-South Africa trade links. Spanish "
        "documentation requires certified English translation for South African Home "
        "Affairs purposes. The South African Embassy in Madrid handles consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('brazil', 'south-africa'): (
        "Brazilian nationals in South Africa include professionals in mining, agriculture, "
        "and business sectors. Brazil and South Africa are both members of the BRICS "
        "grouping and have strong bilateral diplomatic ties, cooperating on trade, "
        "technology, and science. Portuguese documentation from Brazil requires certified "
        "English translation for South African Home Affairs purposes. The South African "
        "Embassy in Brasilia handles consular matters."
    ),
    ('portugal', 'south-africa'): (
        "Portuguese nationals in South Africa include business professionals and residents "
        "with historical ties. A long-established Portuguese community in South Africa "
        "arrived from Madeira and mainland Portugal from the mid-twentieth century, with "
        "further migration from Mozambique and Angola after independence. Portugal and "
        "South Africa have bilateral diplomatic ties. Portuguese documentation requires "
        "certified English translation for South African Home Affairs purposes. The "
        "South African Embassy in Lisbon handles consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    # R42: Saudi Arabia wave 6
    ('niger', 'saudi-arabia'): (
        "Nigerien nationals in Saudi Arabia include Muslim workers employed in the Hajj "
        "service sector in Mecca and Medina, and in construction and service industries. "
        "Niger and Saudi Arabia are fellow OIC member states, and Saudi Arabia has "
        "provided development assistance to Niger. French and Hausa documentation from "
        "Niger requires certified Arabic translation and authentication by the Saudi "
        "Embassy for Saudi Ministry of Health clearance. The Saudi Embassy in Niamey "
        "handles consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('guinea', 'saudi-arabia'): (
        "Guinean nationals in Saudi Arabia include Muslim workers from Guinea's majority "
        "Muslim population, employed in service and construction sectors. Guinea and "
        "Saudi Arabia are OIC member states. French documentation from Guinea requires "
        "certified Arabic translation and authentication by the Saudi Embassy for Saudi "
        "Ministry of Health clearance. The Saudi Embassy in Conakry handles consular "
        "matters."
    ),
    ('benin', 'saudi-arabia'): (
        "Beninese nationals in Saudi Arabia include Muslim workers from Benin's Muslim "
        "community, employed in service and hospitality sectors. Benin and Saudi Arabia "
        "have diplomatic relations as OIC member states. French and Fon documentation "
        "from Benin requires certified Arabic translation and authentication by the Saudi "
        "Embassy for Saudi Ministry of Health clearance. The Saudi Embassy in Cotonou "
        "handles consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('gambia', 'saudi-arabia'): (
        "Gambian nationals in Saudi Arabia form a Muslim community working in service "
        "and hospitality sectors. The Gambia is an OIC member state with strong Islamic "
        "ties, and Saudi Arabia has provided development assistance to The Gambia. "
        "English and Mandinka documentation from The Gambia requires certified Arabic "
        "translation and authentication by the Saudi Embassy for Saudi Ministry of "
        "Health clearance. The Saudi Embassy in Banjul handles consular matters."
    ),
    ('liberia', 'saudi-arabia'): (
        "Liberian nationals in Saudi Arabia include Muslim workers from Liberia's Muslim "
        "population employed in service sectors. Liberia and Saudi Arabia have diplomatic "
        "relations. English documentation from Liberia requires certified Arabic "
        "translation and authentication by the Saudi Embassy for Saudi Ministry of "
        "Health clearance. The Saudi Embassy in Monrovia handles consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    # R42: UAE wave 6
    ('djibouti', 'united-arab-emirates'): (
        "Djiboutian nationals have a notable economic corridor with the UAE, given "
        "Djibouti's role as a strategic Red Sea port nation and the commercial ties "
        "between the two countries. Djibouti and the UAE have diplomatic and trade "
        "relations, with UAE investment present in Djibouti's port infrastructure. "
        "Arabic and French documentation from Djibouti requires authentication by the "
        "UAE Embassy for UAE Customs and MOHAP clearance. The UAE Embassy in Djibouti "
        "City handles consular matters. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    ('togo', 'united-arab-emirates'): (
        "Togolese nationals in the UAE include traders, workers, and professionals in "
        "Dubai's international business environment. Togo and the UAE have diplomatic "
        "relations, and Togolese nationals participate in West African trading networks "
        "centred on Dubai. French and Ewe documentation from Togo requires certified "
        "Arabic translation and authentication by the UAE Embassy for MOHAP clearance. "
        "The UAE Embassy in Lome handles consular matters."
    ),
    ('mali', 'united-arab-emirates'): (
        "Malian nationals in the UAE include workers and traders, part of West Africa's "
        "established business community in Dubai. Mali and the UAE have diplomatic "
        "relations as fellow OIC member states, and Malian gold and commodity traders "
        "have long had connections to the Gulf. French and Bambara documentation from "
        "Mali requires certified Arabic translation and authentication by the UAE Embassy "
        "for MOHAP clearance. The UAE Embassy in Bamako handles consular matters. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    ('comoros', 'united-arab-emirates'): (
        "Comorian nationals form a small but established community in the UAE, given "
        "the Comoros Islands' Arabic-speaking Muslim identity and the Indian Ocean "
        "trade routes connecting East Africa and the Gulf. The Comoros and UAE are "
        "fellow Arab League members with diplomatic ties. Arabic documentation from "
        "the Comoros is generally understood by UAE authorities, though official "
        "authentication by the UAE Embassy is required. The UAE Embassy in Moroni "
        "handles consular matters."
    ),
    ('turkmenistan', 'united-arab-emirates'): (
        "Turkmen nationals in the UAE include workers in the energy sector and business "
        "professionals, drawn by the UAE's role as a regional commercial hub and its "
        "energy industry links. Turkmenistan and the UAE have bilateral energy and trade "
        "ties, and Turkmen nationals increasingly travel and work in the Gulf region. "
        "Turkmen documentation requires certified Arabic or English translation and "
        "authentication by the UAE Embassy for MOHAP and GDRFA clearance. The UAE "
        "Embassy in Ashgabat handles consular matters. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
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
# Route list: R41 (25) + R42 (25) = 50 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R41: Kuwait wave 4 x5 + Qatar wave 4 x5 + India wave 4 x5 +
    #     Turkey wave 1 (new hub) x5 + Malaysia wave 1 (new hub) x5 = 25
    ('cameroon',       'kuwait'),
    ('senegal',        'kuwait'),
    ('myanmar',        'kuwait'),
    ('iraq',           'kuwait'),
    ('eritrea',        'kuwait'),
    ('cameroon',       'qatar'),
    ('senegal',        'qatar'),
    ('myanmar',        'qatar'),
    ('iraq',           'qatar'),
    ('oman',           'qatar'),
    ('vietnam',        'india'),
    ('egypt',          'india'),
    ('france',         'india'),
    ('germany',        'india'),
    ('ghana',          'india'),
    ('syria',          'turkey'),
    ('iraq',           'turkey'),
    ('iran',           'turkey'),
    ('azerbaijan',     'turkey'),
    ('georgia',        'turkey'),
    ('indonesia',      'malaysia'),
    ('bangladesh',     'malaysia'),
    ('philippines',    'malaysia'),
    ('myanmar',        'malaysia'),
    ('india',          'malaysia'),
    # --- Block R42: Turkey wave 2 x5 + Malaysia wave 2 x5 + South Africa wave 5 x5 +
    #     Saudi Arabia wave 6 x5 + UAE wave 6 x5 = 25
    ('pakistan',       'turkey'),
    ('egypt',          'turkey'),
    ('germany',        'turkey'),
    ('morocco',        'turkey'),
    ('ukraine',        'turkey'),
    ('china',          'malaysia'),
    ('vietnam',        'malaysia'),
    ('nepal',          'malaysia'),
    ('thailand',       'malaysia'),
    ('cambodia',       'malaysia'),
    ('japan',          'south-africa'),
    ('italy',          'south-africa'),
    ('spain',          'south-africa'),
    ('brazil',         'south-africa'),
    ('portugal',       'south-africa'),
    ('niger',          'saudi-arabia'),
    ('guinea',         'saudi-arabia'),
    ('benin',          'saudi-arabia'),
    ('gambia',         'saudi-arabia'),
    ('liberia',        'saudi-arabia'),
    ('djibouti',       'united-arab-emirates'),
    ('togo',           'united-arab-emirates'),
    ('mali',           'united-arab-emirates'),
    ('comoros',        'united-arab-emirates'),
    ('turkmenistan',   'united-arab-emirates'),
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
