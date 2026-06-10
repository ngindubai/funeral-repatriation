#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R33-R34.

   R33: Japan wave 2 x5 + New Zealand wave 2 x5 + Italy wave 4 x5 +
        Spain wave 4 x5 + Netherlands wave 4 x5 = 25
   R34: Portugal wave 4 x5 + Switzerland wave 4 x5 + Sweden wave 4 x5 +
        Norway wave 4 x5 + Saudi Arabia wave 4 x5 = 25

   Template rotation: R32 ended on C (index 2). R33 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R32 ended C (index 2); R33 starts D (index 3)

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
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
    'italy': {
        'name': 'Italy',
        'slug': 'italy',
        'key': 'it',
        'reception': (
            "The Italian funeral director (impresa funebre) takes custody at the cargo "
            "terminal, typically Rome Fiumicino (FCO), Milan Malpensa (MXP), or another "
            "Italian international airport. A prefettura transport authorisation is required "
            "before burial or cremation. All foreign documents must carry a certified Italian "
            "translation. The local commune registers the death with the anagrafe (civil "
            "registry). "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
        'consular_template': (
            "Italian Embassy in {city} can advise on documentation requirements for "
            "repatriation to Italy. Italian Ministry of Foreign Affairs and International "
            "Cooperation (MAECI) emergency line: +39 06 3691 3691 (24 hours). The Italian "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Italian funeral director takes custody at the cargo terminal. A prefettura "
            "transport authorisation is required before burial or cremation can proceed. "
            "All foreign documents require certified Italian translation. The local commune "
            "registers the death with the anagrafe. The receiving funeral director "
            "coordinates with the prefettura and local authorities."
        ),
        'emergency_line': '+39 06 3691 3691',
        'hub_url': 'repatriation-from-italy',
    },
    'spain': {
        'name': 'Spain',
        'slug': 'spain',
        'key': 'es',
        'reception': (
            "The Spanish funeral director (empresa funeraria) takes custody at the cargo "
            "terminal, typically Madrid Barajas (MAD), Barcelona El Prat (BCN), or another "
            "Spanish airport. The Registro Civil registers the death. For deaths in the "
            "Canary or Balearic Islands, an internal mainland transfer is required before "
            "any international cargo flight departs. All foreign documents must carry a "
            "certified Spanish translation. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
        'consular_template': (
            "Spanish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Spain. Spanish Ministry of Foreign Affairs emergency line: "
            "+34 91 379 9700 (24 hours). The Spanish Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Spanish funeral director takes custody at the cargo terminal. The Registro "
            "Civil registers the death. Island deaths require a mainland transfer first. "
            "Unexpected deaths may require a Juzgado de Instruccion investigation before "
            "release. All foreign documents require certified Spanish translation. The "
            "receiving funeral director coordinates with the Registro Civil and local "
            "health authorities."
        ),
        'emergency_line': '+34 91 379 9700',
        'hub_url': 'repatriation-from-spain',
    },
    'netherlands': {
        'name': 'Netherlands',
        'slug': 'netherlands',
        'key': 'nl',
        'reception': (
            "The Dutch funeral director (begrafenisondernemer or uitvaartondernemer) takes "
            "custody at Amsterdam Schiphol (AMS) or Rotterdam The Hague (RTM) cargo "
            "terminal. The local gemeente (municipality) registers the death with the "
            "Burgerlijke Stand (civil registry). A transport permit (laissez-passer) must "
            "accompany the remains. Foreign documents in languages other than Dutch, "
            "English, French, or German require certified translation. "
            "(Dutch Ministry of Foreign Affairs, BZ, 2025.)"
        ),
        'consular_template': (
            "Dutch Embassy in {city} can advise on documentation requirements for "
            "repatriation to the Netherlands. Dutch Ministry of Foreign Affairs emergency "
            "line: +31 70 348 6486 (24 hours). The Dutch Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Dutch funeral director takes custody at Amsterdam Schiphol (AMS) cargo "
            "terminal. A laissez-passer must accompany the remains. The local gemeente "
            "registers the death with the Burgerlijke Stand. Documents not in Dutch, "
            "English, French, or German require certified translation. The receiving "
            "funeral director coordinates with the gemeente and health authorities."
        ),
        'emergency_line': '+31 70 348 6486',
        'hub_url': 'repatriation-from-netherlands',
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
}

# ---------------------------------------------------------------------------
# Embassy cities: destination country's embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R33: Japan wave 2
    ('nepal',       'japan'): 'Kathmandu',
    ('thailand',    'japan'): 'Bangkok',
    ('cambodia',    'japan'): 'Phnom Penh',
    ('malaysia',    'japan'): 'Kuala Lumpur',
    ('bangladesh',  'japan'): 'Dhaka',
    # R33: New Zealand wave 2
    ('indonesia',   'new-zealand'): 'Jakarta',
    ('vietnam',     'new-zealand'): 'Hanoi',
    # New Zealand Embassy for Myanmar is in Yangon
    ('myanmar',     'new-zealand'): 'Yangon',
    ('pakistan',    'new-zealand'): 'Islamabad',
    ('malaysia',    'new-zealand'): 'Kuala Lumpur',
    # R33: Italy wave 4
    ('turkey',      'italy'): 'Ankara',
    ('kenya',       'italy'): 'Nairobi',
    ('ethiopia',    'italy'): 'Addis Ababa',
    ('cameroon',    'italy'): 'Yaounde',
    ('algeria',     'italy'): 'Algiers',
    # R33: Spain wave 4
    ('turkey',      'spain'): 'Ankara',
    ('kenya',       'spain'): 'Nairobi',
    ('ethiopia',    'spain'): 'Addis Ababa',
    ('cameroon',    'spain'): 'Yaounde',
    ('algeria',     'spain'): 'Algiers',
    # R33: Netherlands wave 4
    ('iran',        'netherlands'): 'Tehran',
    ('russia',      'netherlands'): 'Moscow',
    ('poland',      'netherlands'): 'Warsaw',
    ('south-korea', 'netherlands'): 'Seoul',
    ('colombia',    'netherlands'): 'Bogota',
    # R34: Portugal wave 4
    ('bangladesh',  'portugal'): 'Dhaka',
    ('kenya',       'portugal'): 'Nairobi',
    ('pakistan',    'portugal'): 'Islamabad',
    ('ivory-coast', 'portugal'): 'Abidjan',
    ('cameroon',    'portugal'): 'Yaounde',
    # R34: Switzerland wave 4
    # Swiss Embassy in Kabul suspended Aug 2021; Afghanistan covered from Islamabad
    ('afghanistan', 'switzerland'): 'Islamabad',
    ('kenya',       'switzerland'): 'Nairobi',
    ('poland',      'switzerland'): 'Warsaw',
    ('algeria',     'switzerland'): 'Algiers',
    ('russia',      'switzerland'): 'Moscow',
    # R34: Sweden wave 4
    ('india',       'sweden'): 'New Delhi',
    ('bangladesh',  'sweden'): 'Dhaka',
    ('south-korea', 'sweden'): 'Seoul',
    ('russia',      'sweden'): 'Moscow',
    ('vietnam',     'sweden'): 'Hanoi',
    # R34: Norway wave 4
    ('russia',      'norway'): 'Moscow',
    ('bangladesh',  'norway'): 'Dhaka',
    ('ukraine',     'norway'): 'Kyiv',
    ('south-korea', 'norway'): 'Seoul',
    # Norwegian Embassy covers Cambodia from Bangkok
    ('cambodia',    'norway'): 'Bangkok',
    # R34: Saudi Arabia wave 4
    ('oman',        'saudi-arabia'): 'Muscat',
    ('lebanon',     'saudi-arabia'): 'Beirut',
    ('senegal',     'saudi-arabia'): 'Dakar',
    ('cameroon',    'saudi-arabia'): 'Yaounde',
    ('mali',        'saudi-arabia'): 'Bamako',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R33: Japan wave 2
    ('nepal', 'japan'): (
        "Nepali nationals form Japan's fifth-largest foreign resident community, with over "
        "130,000 residents working in manufacturing, food service, and technical roles under "
        "Japan's Specified Skilled Worker programme. Nepal to Japan is a growing repatriation "
        "corridor reflecting significant South Asian migration to Japanese industry. Nepali "
        "documentation requires certified Japanese translation. The Japanese Embassy in "
        "Kathmandu handles consular matters. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    ('thailand', 'japan'): (
        "Thai nationals live and work in Japan in food service, hospitality, and care "
        "roles, with a community of over 50,000 residents concentrated in Tokyo and Osaka. "
        "Thailand and Japan share extensive trade and tourism ties. Thailand to Japan is also "
        "a high-volume tourism corridor, so this route handles both resident deaths and deaths "
        "of Japanese tourists in Thailand. Thai documentation requires certified Japanese "
        "translation. The Japanese Embassy in Bangkok handles consular matters."
    ),
    ('cambodia', 'japan'): (
        "Cambodian nationals work in Japan primarily under the Technical Intern Training "
        "Programme, in manufacturing and agriculture. Japan has accepted Cambodian workers "
        "since the 2010s under bilateral labour agreements. The Japanese Embassy in Phnom "
        "Penh handles consular matters. Khmer documentation requires certified Japanese "
        "translation. This corridor has grown as Japan has expanded its skilled worker "
        "recruitment from South-East Asia."
    ),
    ('malaysia', 'japan'): (
        "Malaysian nationals form an educated professional community in Japan, working in "
        "technology, academia, and business sectors. Malaysia and Japan have close bilateral "
        "trade and investment ties, including significant Japanese manufacturing investment "
        "in Malaysia. Malaysian documentation, primarily in Malay and English, requires "
        "certified Japanese translation where needed. The Japanese Embassy in Kuala Lumpur "
        "handles consular matters."
    ),
    ('bangladesh', 'japan'): (
        "Bangladeshi nationals form a growing community in Japan, working in manufacturing "
        "and technical roles under Japan's Specified Skilled Worker and Technical Intern "
        "Training schemes. Japan has expanded its bilateral labour recruitment from South "
        "Asia in recent years. The Japanese Embassy in Dhaka handles consular matters. "
        "Bangladeshi documentation in Bengali requires certified Japanese translation. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    # R33: New Zealand wave 2
    ('indonesia', 'new-zealand'): (
        "Indonesian nationals form a growing South-East Asian community in New Zealand, "
        "working in hospitality, academia, and professional services. New Zealand and "
        "Indonesia have bilateral ties through trade and education. Indonesian documentation "
        "requires certified English translation for New Zealand Customs purposes. The New "
        "Zealand Embassy in Jakarta handles consular matters. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    ('vietnam', 'new-zealand'): (
        "Vietnamese nationals form a growing community in New Zealand, with populations "
        "in Auckland and Wellington working in professional and service roles. This corridor "
        "also handles students and skilled workers holding residence visas. Vietnamese "
        "documentation requires certified English translation for New Zealand Customs. "
        "The New Zealand Embassy in Hanoi handles consular matters."
    ),
    ('myanmar', 'new-zealand'): (
        "Myanmar nationals form a small but established community in New Zealand, working "
        "in professional and service roles, with some arriving through humanitarian pathways. "
        "The New Zealand Embassy in Yangon handles consular matters. Burmese documentation "
        "requires certified English translation for New Zealand Customs. Specialist "
        "coordination is recommended given civil registration challenges in Myanmar. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    ('pakistan', 'new-zealand'): (
        "Pakistani nationals form part of New Zealand's South Asian community, working in "
        "professional and service sectors, with a significant population in Auckland. "
        "Pakistan and New Zealand have bilateral ties through the Commonwealth. Pakistani "
        "documentation in Urdu and Punjabi requires certified English translation where New "
        "Zealand Customs require it. The New Zealand High Commission in Islamabad handles "
        "consular matters."
    ),
    ('malaysia', 'new-zealand'): (
        "Malaysian nationals form an established community in New Zealand, with many having "
        "studied or worked there over the past three decades through education and skilled "
        "migration pathways. Malaysia and New Zealand share Commonwealth ties and close "
        "educational links. English documentation from Malaysia simplifies some requirements "
        "for New Zealand Customs. The New Zealand High Commission in Kuala Lumpur handles "
        "consular matters."
    ),
    # R33: Italy wave 4
    ('turkey', 'italy'): (
        "Turkish nationals form Italy's second-largest non-EU immigrant community, with over "
        "300,000 residents working in trade, construction, and professional services across "
        "northern Italy, particularly in Milan and Turin. Turkey and Italy have close trade "
        "links and a long-standing bilateral relationship. Turkish documentation requires "
        "certified Italian translation for Italian civil registry purposes. The Italian "
        "Embassy in Ankara handles consular matters. "
        "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
    ),
    ('kenya', 'italy'): (
        "Kenyan nationals form part of Italy's East African diaspora, working in caregiving, "
        "healthcare, and professional roles. Kenya and Italy have bilateral ties through "
        "development cooperation and the Rome-based UN Food and Agriculture Organisation. "
        "English documentation from Kenya requires certified Italian translation where "
        "required by Italian registry authorities. The Italian Embassy in Nairobi handles "
        "consular matters."
    ),
    ('ethiopia', 'italy'): (
        "Ethiopian nationals form part of Italy's East African diaspora. Italy and Ethiopia "
        "have historical connections through the Italian colonial period in neighbouring "
        "Eritrea and the 1935 occupation. Italy accepted Ethiopian migrants and asylum "
        "seekers during the 2010s. Amharic documentation from Ethiopia requires certified "
        "Italian translation. The Italian Embassy in Addis Ababa handles consular matters."
    ),
    ('cameroon', 'italy'): (
        "Cameroonian nationals form part of Italy's Central and West African diaspora, "
        "working in service and professional roles in Rome, Milan, and other cities. "
        "French documentation from francophone Cameroon requires certified Italian "
        "translation; English documentation from Anglophone Cameroon may also require "
        "certified translation for some registry purposes. The Italian Embassy in "
        "Yaounde handles consular matters."
    ),
    ('algeria', 'italy'): (
        "Algerian nationals form one of Italy's largest North African immigrant communities, "
        "with over 70,000 residents concentrated in Lombardy, Piedmont, and Liguria. "
        "Algeria and Italy have close energy and trade ties, including a major gas pipeline "
        "linking the two countries. Arabic documentation from Algeria requires certified "
        "Italian translation for Italian civil registry purposes. The Italian Embassy in "
        "Algiers handles consular matters."
    ),
    # R33: Spain wave 4
    ('turkey', 'spain'): (
        "Turkish nationals form part of Spain's Middle Eastern and Mediterranean immigrant "
        "community, working in trade and professional services. Turkey and Spain have "
        "bilateral trade links and significant tourist exchange. Turkish Airlines operates "
        "regular routes between Turkish cities and Spanish airports. Turkish documentation "
        "requires certified Spanish translation for the Registro Civil. The Spanish Embassy "
        "in Ankara handles consular matters. "
        "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
    ),
    ('kenya', 'spain'): (
        "Kenyan nationals form part of Spain's East African diaspora, working in hospitality, "
        "care, and professional roles in Madrid and Barcelona. English documentation from "
        "Kenya requires certified Spanish translation where required by Spanish registry "
        "authorities. The Spanish Embassy in Nairobi handles consular matters. Kenya to "
        "Spain is a growing corridor reflecting increased East African migration to "
        "southern Europe."
    ),
    ('ethiopia', 'spain'): (
        "Ethiopian nationals form part of Spain's East African diaspora, with a community "
        "in Madrid and Barcelona. Spain accepted Ethiopian and Eritrean migrants during "
        "the 2010s migration period. Amharic documentation from Ethiopia requires certified "
        "Spanish translation for the Registro Civil. The Spanish Embassy in Addis Ababa "
        "handles consular matters."
    ),
    ('cameroon', 'spain'): (
        "Cameroonian nationals form part of Spain's Central African diaspora, with communities "
        "in Madrid and Barcelona. Spain and Cameroon have bilateral ties including through "
        "francophone networks. French documentation from francophone Cameroon requires "
        "certified Spanish translation; English documentation from Anglophone Cameroon "
        "also requires certified translation. The Spanish Embassy in Yaounde handles "
        "consular matters."
    ),
    ('algeria', 'spain'): (
        "Algerian nationals form Spain's largest North African immigrant community, with over "
        "60,000 residents concentrated in Catalonia, Andalusia, and the Canary Islands. "
        "Algeria and Spain share the Mediterranean and significant trade ties; a gas "
        "pipeline connects the two countries directly. Arabic documentation from Algeria "
        "requires certified Spanish translation for the Registro Civil. The Spanish Embassy "
        "in Algiers handles consular matters."
    ),
    # R33: Netherlands wave 4
    ('iran', 'netherlands'): (
        "Iranian nationals form one of the Netherlands' largest Middle Eastern communities, "
        "with over 40,000 residents in Amsterdam, The Hague, and other Dutch cities. Many "
        "Iranians arrived as students and refugees from the late 1980s onward. Farsi "
        "documentation from Iran requires certified Dutch or English translation for Dutch "
        "registry authorities. The Dutch Embassy in Tehran handles consular matters. "
        "(Dutch Ministry of Foreign Affairs, BZ, 2025.)"
    ),
    ('russia', 'netherlands'): (
        "Russian nationals have a significant community in the Netherlands, particularly in "
        "Amsterdam and The Hague, working in business, technology, and professional services. "
        "The Netherlands hosted major Russian energy and corporate operations before 2022. "
        "Russian documentation requires certified Dutch or English translation for Dutch "
        "registry authorities. The Dutch Embassy in Moscow handles consular matters. "
        "Specialist coordination is recommended given the changed diplomatic context."
    ),
    ('poland', 'netherlands'): (
        "Polish nationals form one of the Netherlands' largest EU immigrant communities, "
        "with over 200,000 residents working in construction, agriculture, logistics, and "
        "professional services. Poland and the Netherlands are EU partners, and EU freedom "
        "of movement applies. Polish documentation requires certified Dutch or English "
        "translation where required. The Dutch Embassy in Warsaw handles consular matters. "
        "Poland to Netherlands is a consistently high-volume labour migration corridor."
    ),
    ('south-korea', 'netherlands'): (
        "South Korean nationals form part of the Netherlands' East Asian community, working "
        "in technology, electronics, and business sectors. Several major Korean companies, "
        "including Samsung and LG Electronics, have European operations in the Netherlands. "
        "Korean documentation requires certified Dutch or English translation for Dutch "
        "registry authorities. The Dutch Embassy in Seoul handles consular matters."
    ),
    ('colombia', 'netherlands'): (
        "Colombian nationals form part of the Netherlands' South American diaspora, with a "
        "community in Amsterdam and Rotterdam. Colombia and the Netherlands have bilateral "
        "ties partly through Suriname, a former Dutch colony with South American connections. "
        "Spanish documentation from Colombia requires certified Dutch translation for Dutch "
        "registry authorities. The Dutch Embassy in Bogota handles consular matters."
    ),
    # R34: Portugal wave 4
    ('bangladesh', 'portugal'): (
        "Bangladeshi nationals form a growing community in Portugal, concentrated in Lisbon, "
        "working in hospitality and service roles. Portugal has seen increased South Asian "
        "immigration in recent years under its visa liberalisation policies. Bengali "
        "documentation from Bangladesh requires certified Portuguese translation. The "
        "Portuguese Embassy in Dhaka handles consular matters. "
        "(Portuguese Ministry of Foreign Affairs, MNE, 2025.)"
    ),
    ('kenya', 'portugal'): (
        "Kenyan nationals form part of Portugal's African diaspora, working in professional "
        "and service roles in Lisbon and Porto. English documentation from Kenya requires "
        "certified Portuguese translation where required by Portuguese civil registry "
        "authorities. The Portuguese Embassy in Nairobi handles consular matters. Kenya "
        "to Portugal is a growing corridor reflecting increased East African migration "
        "to the Iberian peninsula."
    ),
    ('pakistan', 'portugal'): (
        "Pakistani nationals form a growing community in Portugal, concentrated in Lisbon, "
        "working in hospitality, retail, and service roles. Portugal has seen increased "
        "South Asian immigration in recent years. Urdu and Punjabi documentation from "
        "Pakistan requires certified Portuguese translation. The Portuguese Embassy in "
        "Islamabad handles consular matters."
    ),
    ('ivory-coast', 'portugal'): (
        "Ivorian nationals form part of Portugal's West African diaspora, with connections "
        "through the PALOP (Portuguese-speaking African countries) cooperation framework "
        "and francophone networks. French documentation from Ivory Coast requires certified "
        "Portuguese translation where required by registry authorities. The Portuguese "
        "Embassy in Abidjan handles consular matters."
    ),
    ('cameroon', 'portugal'): (
        "Cameroonian nationals form part of Portugal's African diaspora, working in "
        "professional and service roles. Portuguese and Cameroon share Lusophone and "
        "Francophone African networks. French documentation from francophone Cameroon "
        "requires certified Portuguese translation; English documentation from Anglophone "
        "Cameroon may simplify some requirements. The Portuguese Embassy in Yaounde "
        "handles consular matters."
    ),
    # R34: Switzerland wave 4
    ('afghanistan', 'switzerland'): (
        "Afghan nationals form a significant community in Switzerland, with over 20,000 "
        "residents who arrived as asylum seekers and refugees during the 2010s and 2020s. "
        "The Swiss Embassy in Kabul suspended operations in August 2021 following the "
        "Taliban takeover; Afghan consular matters are now handled via the Swiss Embassy "
        "in Islamabad, Pakistan. Dari and Pashto documentation requires certified German, "
        "French, or Italian translation. Specialist coordination is strongly recommended "
        "given the disrupted civil registration situation in Afghanistan. "
        "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
    ),
    ('kenya', 'switzerland'): (
        "Kenyan nationals form part of Switzerland's East African community, working in "
        "international organisations in Geneva and in professional and service roles in "
        "Zurich. Switzerland hosts numerous UN agencies and international bodies in Geneva, "
        "attracting Kenyan professionals to the city. English documentation from Kenya "
        "simplifies some requirements for Swiss authorities. The Swiss Embassy in Nairobi "
        "handles consular matters."
    ),
    ('poland', 'switzerland'): (
        "Polish nationals form one of Switzerland's EU-adjacent immigrant communities, "
        "working in construction, healthcare, and professional services. Switzerland has "
        "bilateral agreements with the EU governing the movement of EU nationals. Polish "
        "documentation requires certified German, French, or Italian translation depending "
        "on the receiving canton. The Swiss Embassy in Warsaw handles consular matters."
    ),
    ('algeria', 'switzerland'): (
        "Algerian nationals form part of Switzerland's North African diaspora, with "
        "communities in Geneva, Lausanne, and other Swiss cities working in professional "
        "and service roles. Arabic documentation from Algeria requires certified German, "
        "French, or Italian translation for Swiss civil registry authorities. The Swiss "
        "Embassy in Algiers handles consular matters. Geneva's Francophone character means "
        "French-speaking Algerian families often choose Geneva as the receiving airport."
    ),
    ('russia', 'switzerland'): (
        "Russian nationals form a significant community in Switzerland, particularly in "
        "Geneva, Zurich, and Zug, working in finance, business, and the substantial "
        "international organisation sector. Switzerland hosts the UN European headquarters "
        "in Geneva and numerous international bodies that attract Russian nationals in "
        "professional roles. Russian documentation requires certified German, French, or "
        "Italian translation. The Swiss Embassy in Moscow handles consular matters. "
        "Switzerland has maintained diplomatic relations with Russia and continues to "
        "provide consular services."
    ),
    # R34: Sweden wave 4
    ('india', 'sweden'): (
        "Indian nationals form a growing professional community in Sweden, working in "
        "technology, pharmaceuticals, and academia, particularly in Stockholm, Gothenburg, "
        "and Malmo. India and Sweden have bilateral ties through major Swedish companies "
        "including Ericsson, Volvo, and AstraZeneca, all with significant Indian operations. "
        "Hindi and English documentation from India requires certified Swedish translation "
        "where required. The Swedish Embassy in New Delhi handles consular matters. "
        "(Swedish Ministry of Foreign Affairs, UD, 2025.)"
    ),
    ('bangladesh', 'sweden'): (
        "Bangladeshi nationals form a growing community in Sweden, working in manufacturing "
        "and service roles, with communities in Stockholm and Gothenburg. Sweden received "
        "Bangladeshi migrants through labour and humanitarian channels. Bengali documentation "
        "from Bangladesh requires certified Swedish translation. The Swedish Embassy in Dhaka "
        "handles consular matters."
    ),
    ('south-korea', 'sweden'): (
        "South Korean nationals form part of Sweden's East Asian community, working in "
        "technology, electronics, and automotive sectors driven by Korean company operations "
        "in Sweden. Several Korean multinationals have Scandinavian operations or partnerships "
        "with Swedish firms. Korean documentation requires certified Swedish translation for "
        "Swedish registry authorities. The Swedish Embassy in Seoul handles consular matters."
    ),
    ('russia', 'sweden'): (
        "Russian nationals form part of Sweden's Eastern European diaspora, with communities "
        "in Stockholm and other Swedish cities. Sweden and Russia have shared Baltic Sea "
        "geography and historically significant ties. Russian documentation requires certified "
        "Swedish translation for Swedish registry authorities. The Swedish Embassy in Moscow "
        "handles consular matters. Specialist coordination is recommended given the changed "
        "diplomatic context since 2022."
    ),
    ('vietnam', 'sweden'): (
        "Vietnamese nationals form part of Sweden's South-East Asian diaspora, with a "
        "long-established community of Vietnamese refugees and their descendants who arrived "
        "in Sweden from the late 1970s following the end of the Vietnam War. Sweden was among "
        "the first Western countries to open diplomatic relations with Vietnam. Vietnamese "
        "documentation requires certified Swedish translation. The Swedish Embassy in Hanoi "
        "handles consular matters."
    ),
    # R34: Norway wave 4
    ('russia', 'norway'): (
        "Russian nationals form a community in Norway, particularly in the northernmost "
        "Finnmark region near the Norwegian-Russian border, reflecting centuries of shared "
        "maritime and trade history in the Barents region. The Norwegian Embassy in Moscow "
        "handles consular matters. Russian documentation requires certified Norwegian "
        "translation for Norwegian registry purposes. The short overland distance in the "
        "Barents region means some cases involve land transport rather than air cargo. "
        "(Norwegian Ministry of Foreign Affairs, 2025.)"
    ),
    ('bangladesh', 'norway'): (
        "Bangladeshi nationals form a growing community in Norway, working in services, "
        "hospitality, and professional roles in Oslo and Bergen. Norway received South "
        "Asian migrants through labour and family reunification channels from the 1970s "
        "onward. Bengali documentation from Bangladesh requires certified Norwegian "
        "translation. The Norwegian Embassy in Dhaka handles consular matters."
    ),
    ('ukraine', 'norway'): (
        "Ukrainian nationals have formed a significant community in Norway since 2022, when "
        "Norway granted temporary protection to Ukrainians fleeing the war. Norway accepted "
        "tens of thousands of Ukrainian refugees under the collective protection scheme. "
        "Ukrainian documentation requires certified Norwegian translation. The Norwegian "
        "Embassy in Kyiv handles consular matters, operating where security conditions "
        "allow. "
        "(Norwegian Ministry of Foreign Affairs, 2025.)"
    ),
    ('south-korea', 'norway'): (
        "South Korean nationals form part of Norway's East Asian community, working in "
        "technology and maritime sectors. Norway's offshore oil and maritime industry "
        "attracts Korean professionals through bilateral company relationships and joint "
        "ventures. Korean documentation requires certified Norwegian translation for "
        "Norwegian registry authorities. The Norwegian Embassy in Seoul handles "
        "consular matters."
    ),
    ('cambodia', 'norway'): (
        "Cambodian nationals form a small but established community in Norway, some having "
        "arrived as refugees and others through labour and family channels. Norwegian "
        "consular matters for Cambodia are handled from the Norwegian Embassy in Bangkok, "
        "Thailand. Khmer documentation from Cambodia requires certified Norwegian "
        "translation. Specialist coordination is recommended given the added complexity "
        "of cross-embassy coverage on this corridor."
    ),
    # R34: Saudi Arabia wave 4
    ('oman', 'saudi-arabia'): (
        "Omani nationals form a Gulf Cooperation Council (GCC) community in Saudi Arabia, "
        "with movement between the two neighbouring countries common for work, commerce, "
        "and family reasons. Oman and Saudi Arabia are both GCC members, which simplifies "
        "some border formalities, but the Saudi Ministry of Health clearance requirement "
        "for the import of human remains still applies. The Saudi Embassy in Muscat handles "
        "document authentication. Arabic documentation from Oman is well understood by "
        "Saudi authorities. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('lebanon', 'saudi-arabia'): (
        "Lebanese nationals form one of Saudi Arabia's largest Arab expatriate communities, "
        "with over 300,000 residents working in business, finance, engineering, and "
        "professional services in Riyadh and Jeddah. Lebanon and Saudi Arabia have long "
        "bilateral ties through the Gulf labour market. Arabic documentation from Lebanon "
        "is understood by Saudi authorities. The Saudi Embassy in Beirut handles document "
        "authentication. Lebanon to Saudi Arabia is an established and high-volume "
        "repatriation corridor."
    ),
    ('senegal', 'saudi-arabia'): (
        "Senegalese nationals work in Saudi Arabia in construction, domestic service, and "
        "religious contexts. Senegal has a predominantly Muslim population and strong "
        "cultural ties to the Hajj and Umrah, meaning Senegalese nationals in Saudi Arabia "
        "include both workers and pilgrims. Saudi Arabia and Senegal have bilateral ties "
        "through the Organisation of Islamic Cooperation (OIC). French documentation from "
        "Senegal requires certified Arabic translation. The Saudi Embassy in Dakar handles "
        "document authentication."
    ),
    ('cameroon', 'saudi-arabia'): (
        "Cameroonian nationals work in Saudi Arabia primarily in construction and domestic "
        "service. Saudi Arabia and Cameroon have ties through the Organisation of Islamic "
        "Cooperation framework. French documentation from francophone Cameroon requires "
        "certified Arabic translation; English documentation from Anglophone Cameroon also "
        "requires certified Arabic translation for Saudi authorities. The Saudi Embassy "
        "in Yaounde handles document authentication."
    ),
    ('mali', 'saudi-arabia'): (
        "Malian nationals work in Saudi Arabia in construction and religious service "
        "contexts. Mali has a predominantly Muslim population with deep ties to the Hajj, "
        "and Malian workers and pilgrims are a regular presence in the Hijaz region. "
        "Saudi Arabia and Mali have bilateral ties through the Organisation of Islamic "
        "Cooperation (OIC). French documentation from Mali requires certified Arabic "
        "translation. The Saudi Embassy in Bamako handles document authentication."
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
            'Saudi Arabia': 'Saudi Arabia',
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
# Route list: R33 (25) + R34 (25) = 50 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R33: Japan wave 2 x5 + New Zealand wave 2 x5 + Italy wave 4 x5 +
    #     Spain wave 4 x5 + Netherlands wave 4 x5 = 25
    ('nepal',         'japan'),
    ('thailand',      'japan'),
    ('cambodia',      'japan'),
    ('malaysia',      'japan'),
    ('bangladesh',    'japan'),
    ('indonesia',     'new-zealand'),
    ('vietnam',       'new-zealand'),
    ('myanmar',       'new-zealand'),
    ('pakistan',      'new-zealand'),
    ('malaysia',      'new-zealand'),
    ('turkey',        'italy'),
    ('kenya',         'italy'),
    ('ethiopia',      'italy'),
    ('cameroon',      'italy'),
    ('algeria',       'italy'),
    ('turkey',        'spain'),
    ('kenya',         'spain'),
    ('ethiopia',      'spain'),
    ('cameroon',      'spain'),
    ('algeria',       'spain'),
    ('iran',          'netherlands'),
    ('russia',        'netherlands'),
    ('poland',        'netherlands'),
    ('south-korea',   'netherlands'),
    ('colombia',      'netherlands'),
    # --- Block R34: Portugal wave 4 x5 + Switzerland wave 4 x5 + Sweden wave 4 x5 +
    #     Norway wave 4 x5 + Saudi Arabia wave 4 x5 = 25
    ('bangladesh',    'portugal'),
    ('kenya',         'portugal'),
    ('pakistan',      'portugal'),
    ('ivory-coast',   'portugal'),
    ('cameroon',      'portugal'),
    ('afghanistan',   'switzerland'),
    ('kenya',         'switzerland'),
    ('poland',        'switzerland'),
    ('algeria',       'switzerland'),
    ('russia',        'switzerland'),
    ('india',         'sweden'),
    ('bangladesh',    'sweden'),
    ('south-korea',   'sweden'),
    ('russia',        'sweden'),
    ('vietnam',       'sweden'),
    ('russia',        'norway'),
    ('bangladesh',    'norway'),
    ('ukraine',       'norway'),
    ('south-korea',   'norway'),
    ('cambodia',      'norway'),
    ('oman',          'saudi-arabia'),
    ('lebanon',       'saudi-arabia'),
    ('senegal',       'saudi-arabia'),
    ('cameroon',      'saudi-arabia'),
    ('mali',          'saudi-arabia'),
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
