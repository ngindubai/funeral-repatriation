#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R26-R28.

   R26: Switzerland x5 + Sweden x5 + Norway x5 + Portugal x5 + extra waves x5 = 25
   R27: Switzerland wave 2 x5 + Sweden wave 2 x5 + Norway wave 2 x5 +
        Portugal wave 2 x5 + additional Tier B x5 = 25
   R28: Spain wave 3 x5 + Netherlands wave 3 x5 + Italy wave 3 x5 +
        Belgium wave 3 x5 + Saudi Arabia wave 2 x5 = 25

   R26: turkey/portugal/italy/germany/india-switzerland;
        syria/somalia/iraq/poland/afghanistan-sweden;
        poland/somalia/pakistan/india/philippines-norway;
        brazil/angola/mozambique/cabo-verde/guinea-bissau-portugal;
        turkey/iraq-france, ghana-netherlands, ghana/spain-spain, kenya-netherlands

   R27: france/spain/morocco/eritrea/pakistan-switzerland;
        turkey/iran/eritrea/ethiopia/bosnia-and-herzegovina-sweden;
        iraq/iran/vietnam/eritrea/ethiopia-norway;
        france/spain/india/china/venezuela-portugal;
        eritrea-italy, ethiopia/kenya/senegal/cameroon-germany

   R28: argentina/cuba/brazil/philippines/senegal-spain;
        nigeria/bangladesh/vietnam/somalia/eritrea-netherlands;
        ecuador/peru/ghana/tunisia/ivory-coast-italy;
        algeria/ivory-coast/ghana/poland/vietnam-belgium;
        somalia/iraq/yemen/turkey/sudan-saudi-arabia

   Template rotation continues from R25 last variant C, so R26 starts at D (index 3).
   R26 ends on variant C (index 2). R27 starts at D (index 3).
   R27 ends on variant C (index 2). R28 starts at D (index 3).
   R28 ends on variant C (index 2). R29 starts at D (index 3).
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

# R25 ended on variant C (index 2). R26 starts at D (index 3).
START_VARIANT = 3

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
    # --- Four new Tier B hubs introduced in R26 ---
    'switzerland': {
        'name': 'Switzerland',
        'slug': 'switzerland',
        'key': 'ch',
        'reception': (
            "The Swiss Bestatter (funeral director) takes custody at Zurich (ZRH) or "
            "Geneva (GVA) cargo terminal. A Leichentransportschein (body transport permit) "
            "must accompany the coffin. The Zivilstandsamt (civil registry) registers the death. "
            "The Kantonsarzt (cantonal health officer) may inspect the remains on arrival. "
            "Switzerland is a Hague Apostille Convention member. Documents not in German, "
            "French, or Italian require certified translation. "
            "(Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
        ),
        'consular_template': (
            "Swiss Embassy in {city} can advise on documentation requirements for repatriation "
            "to Switzerland. Swiss Federal Department of Foreign Affairs (FDFA) helpline for "
            "Swiss residents abroad: +41 800 24-7-365 (24 hours). The Swiss Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Swiss Bestatter (funeral director) takes custody at Zurich (ZRH) or Geneva (GVA) "
            "cargo terminal. A Leichentransportschein must accompany the coffin. The Zivilstandsamt "
            "registers the death. The Kantonsarzt may inspect the remains on arrival. "
            "Documents not in German, French, or Italian require certified translation. "
            "The receiving funeral director coordinates with the cantonal authorities."
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
            "is notified to update the population register. The Polismyndigheten (Swedish Police) "
            "is informed if the death was violent or unexplained. Sweden is an EU and Hague "
            "Apostille Convention member. Documents not in Swedish or English require "
            "certified Swedish translation. "
            "(Swedish Ministry of Foreign Affairs, UD, 2025.)"
        ),
        'consular_template': (
            "Swedish Embassy in {city} can advise on documentation requirements for repatriation "
            "to Sweden. Swedish Ministry of Foreign Affairs emergency line: +46 8 405 50 05 "
            "(24 hours). The Swedish Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Swedish begravningsentreprenor (funeral director) takes custody at "
            "Stockholm Arlanda (ARN) or Gothenburg Landvetter (GOT) cargo terminal. "
            "A laissez-passer must accompany the remains. Skatteverket is notified to update "
            "the population register. Documents not in Swedish or English require certified "
            "Swedish translation. The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+46 8 405 50 05',
        'hub_url': 'repatriation-from-sweden',
    },
    'norway': {
        'name': 'Norway',
        'slug': 'norway',
        'key': 'no',
        'reception': (
            "The Norwegian begravelsesbyraa (funeral director) takes custody at "
            "Oslo Gardermoen (OSL) cargo terminal. A laissez-passer or equivalent body "
            "transport document must accompany the coffin. The Folkeregisteret (National "
            "Population Register) records the death. Norway is a Hague Apostille Convention "
            "member (EEA, not EU). Documents not in Norwegian or English require certified "
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
            "The Norwegian begravelsesbyraa (funeral director) takes custody at Oslo Gardermoen "
            "(OSL) cargo terminal. A laissez-passer must accompany the coffin. The Folkeregisteret "
            "records the death. Documents not in Norwegian or English require certified Norwegian "
            "translation. The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+47 23 95 00 00',
        'hub_url': 'repatriation-from-norway',
    },
    'portugal': {
        'name': 'Portugal',
        'slug': 'portugal',
        'key': 'pt',
        'reception': (
            "The Portuguese agencia funeraria (funeral director) takes custody at Lisbon (LIS), "
            "Porto (OPO), or Faro (FAO) cargo terminal. An Autoridade de Saude (health authority) "
            "clearance is required before burial or cremation can proceed. The Conservatoria do "
            "Registo Civil registers the death. Portugal is an EU and Hague Apostille Convention "
            "member. Documents from EU-origin countries may use a multilingual EU death certificate. "
            "Documents from non-EU countries require certified Portuguese translation. "
            "(Portuguese Ministry of Foreign Affairs, MNE, 2025.)"
        ),
        'consular_template': (
            "Portuguese Embassy in {city} can advise on documentation requirements for "
            "repatriation to Portugal. Portuguese Ministry of Foreign Affairs (MNE) emergency "
            "line: +351 21 394 6000 (24 hours). The Portuguese Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Portuguese agencia funeraria (funeral director) takes custody at Lisbon (LIS), "
            "Porto (OPO), or Faro (FAO) cargo terminal. Autoridade de Saude clearance is required. "
            "The Conservatoria do Registo Civil registers the death. EU-origin documents may use "
            "a multilingual EU certificate. Non-EU documents require certified Portuguese translation. "
            "The receiving funeral director coordinates with local health authorities."
        ),
        'emergency_line': '+351 21 394 6000',
        'hub_url': 'repatriation-from-portugal',
    },
    # --- Carry-over hubs from R22-R25 (used in R26 extra waves) ---
    'france': {
        'name': 'France',
        'slug': 'france',
        'key': 'fr',
        'reception': (
            "The French funeral director (pompes funebres) takes custody at Charles de Gaulle "
            "(CDG, Paris) or another French international airport. The prefecture may require a "
            "permis d'inhumer (burial permit) or transport authorisation before burial or "
            "cremation can proceed. All foreign documents must carry a certified French translation. "
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
            "French airport. The prefecture issues a permis d'inhumer before burial or cremation. "
            "All foreign documents require certified French translation. "
            "The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+33 1 43 17 67 67',
        'hub_url': 'repatriation-from-france',
    },
    'netherlands': {
        'name': 'Netherlands',
        'slug': 'netherlands',
        'key': 'nl',
        'reception': (
            "The Dutch funeral director (begrafenisondernemer or uitvaartondernemer) takes "
            "custody at Amsterdam Schiphol (AMS) or Rotterdam The Hague (RTM) cargo terminal. "
            "The local gemeente (municipality) registers the death with the Burgerlijke Stand "
            "(civil registry). A transport permit (laissez-passer) must accompany the remains. "
            "Foreign documents in languages other than Dutch, English, French, or German "
            "require certified translation. "
            "(Dutch Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Dutch Embassy in {city} can advise on documentation requirements for repatriation "
            "to the Netherlands. Dutch Ministry of Foreign Affairs emergency line: "
            "+31 70 348 6486 (24 hours). The Dutch Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Dutch funeral director takes custody at Amsterdam Schiphol (AMS) cargo terminal. "
            "A laissez-passer must accompany the remains. The local gemeente registers the death "
            "with the Burgerlijke Stand. Documents not in Dutch, English, French, or German "
            "require certified translation. The receiving funeral director coordinates with "
            "the gemeente and health authorities."
        ),
        'emergency_line': '+31 70 348 6486',
        'hub_url': 'repatriation-from-netherlands',
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
            "+34 91 379 9700 (24 hours). The Spanish Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Spanish funeral director takes custody at the cargo terminal. The Registro Civil "
            "registers the death. Island deaths require a mainland transfer first. Unexpected "
            "deaths may require a Juzgado de Instruccion investigation before release. All "
            "foreign documents require certified Spanish translation. The receiving funeral "
            "director coordinates with the Registro Civil and local health authorities."
        ),
        'emergency_line': '+34 91 379 9700',
        'hub_url': 'repatriation-from-spain',
    },
    # --- Additional hubs introduced in R27-R28 ---
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
    'italy': {
        'name': 'Italy',
        'slug': 'italy',
        'key': 'it',
        'reception': (
            "The Italian funeral director (impresa funebre) takes custody at the cargo "
            "terminal, typically Rome Fiumicino (FCO), Milan Malpensa (MXP), or another "
            "Italian international airport. A prefettura transport authorisation is required "
            "before burial or cremation. All foreign documents must carry a certified Italian "
            "translation. The local comune registers the death with the anagrafe (civil "
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
            "The Italian funeral director takes custody at the cargo terminal. "
            "A prefettura transport authorisation is required before burial or cremation. "
            "All foreign documents require certified Italian translation. "
            "The local comune registers the death with the anagrafe. "
            "The receiving funeral director coordinates with the prefettura and local authorities."
        ),
        'emergency_line': '+39 06 3691 3691',
        'hub_url': 'repatriation-from-italy',
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
            "The Belgian funeral director takes custody at Brussels Airport (BRU) cargo terminal. "
            "A transport authorisation is required before burial or cremation. "
            "The local commune or gemeente registers the death. "
            "All foreign documents require certified French or Dutch translation. "
            "The receiving funeral director coordinates with the commune and local health authorities."
        ),
        'emergency_line': '+32 2 501 8111',
        'hub_url': 'repatriation-from-belgium',
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
            "The Saudi government mortuary takes custody at King Khalid (RUH, Riyadh), "
            "King Abdulaziz (JED, Jeddah), or King Fahd (DMM, Dammam) cargo terminal. "
            "Saudi Ministry of Health clearance is required in advance. "
            "All documents must be authenticated by the Saudi Embassy in the origin country. "
            "Non-Muslim remains require specific certification. "
            "The family or sponsor in Saudi Arabia coordinates with the receiving authorities."
        ),
        'emergency_line': 'contact Saudi Embassy in origin country',
        'hub_url': 'repatriation-from-saudi-arabia',
    },
}

# ---------------------------------------------------------------------------
# Embassy cities: the destination country's embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R26: Switzerland corridors
    ('turkey', 'switzerland'):   'Ankara',
    ('portugal', 'switzerland'): 'Lisbon',
    ('italy', 'switzerland'):    'Rome',
    ('germany', 'switzerland'):  'Berlin',
    ('india', 'switzerland'):    'New Delhi',
    # R26: Sweden corridors
    # Swedish Embassy in Damascus closed 2012; Swedish interests covered by Beirut
    ('syria', 'sweden'):         'Beirut',
    # Swedish Embassy covering Somalia is in Nairobi
    ('somalia', 'sweden'):       'Nairobi',
    ('iraq', 'sweden'):          'Baghdad',
    ('poland', 'sweden'):        'Warsaw',
    # Swedish Embassy covering Afghanistan is via Islamabad
    ('afghanistan', 'sweden'):   'Islamabad',
    # R26: Norway corridors
    ('poland', 'norway'):        'Warsaw',
    # Norwegian Embassy covering Somalia is in Nairobi
    ('somalia', 'norway'):       'Nairobi',
    ('pakistan', 'norway'):      'Islamabad',
    ('india', 'norway'):         'New Delhi',
    ('philippines', 'norway'):   'Manila',
    # R26: Portugal corridors
    ('brazil', 'portugal'):      'Brasilia',
    ('angola', 'portugal'):      'Luanda',
    ('mozambique', 'portugal'):  'Maputo',
    ('cabo-verde', 'portugal'):  'Praia',
    ('guinea-bissau', 'portugal'): 'Bissau',
    # R26: Extra waves
    ('turkey', 'france'):        'Ankara',
    ('iraq', 'france'):          'Baghdad',
    ('ghana', 'netherlands'):    'Accra',
    ('ghana', 'spain'):          'Accra',
    ('kenya', 'netherlands'):    'Nairobi',
    # R27: Switzerland wave 2
    ('france',   'switzerland'): 'Paris',
    ('spain',    'switzerland'): 'Madrid',
    ('morocco',  'switzerland'): 'Rabat',
    # Switzerland covers Eritrea consularly from Addis Ababa
    ('eritrea',  'switzerland'): 'Addis Ababa',
    ('pakistan', 'switzerland'): 'Islamabad',
    # R27: Sweden wave 2
    ('turkey',                 'sweden'): 'Ankara',
    ('iran',                   'sweden'): 'Tehran',
    # Swedish Embassy covering Eritrea is in Nairobi
    ('eritrea',                'sweden'): 'Nairobi',
    ('ethiopia',               'sweden'): 'Addis Ababa',
    ('bosnia-and-herzegovina', 'sweden'): 'Sarajevo',
    # R27: Norway wave 2
    ('iraq',    'norway'): 'Baghdad',
    ('iran',    'norway'): 'Tehran',
    ('vietnam', 'norway'): 'Hanoi',
    # Norwegian Embassy covering Eritrea is in Nairobi
    ('eritrea', 'norway'): 'Nairobi',
    ('ethiopia','norway'): 'Addis Ababa',
    # R27: Portugal wave 2
    ('france',    'portugal'): 'Paris',
    ('spain',     'portugal'): 'Madrid',
    ('india',     'portugal'): 'New Delhi',
    ('china',     'portugal'): 'Beijing',
    ('venezuela', 'portugal'): 'Caracas',
    # R27: Additional Tier B waves
    ('eritrea',  'italy'):   'Asmara',
    ('ethiopia', 'germany'): 'Addis Ababa',
    ('kenya',    'germany'): 'Nairobi',
    ('senegal',  'germany'): 'Dakar',
    ('cameroon', 'germany'): 'Yaounde',
    # R28: Spain wave 3
    ('argentina',   'spain'): 'Buenos Aires',
    ('cuba',        'spain'): 'Havana',
    ('brazil',      'spain'): 'Brasilia',
    ('philippines', 'spain'): 'Manila',
    ('senegal',     'spain'): 'Dakar',
    # R28: Netherlands wave 3
    ('nigeria',    'netherlands'): 'Abuja',
    ('bangladesh', 'netherlands'): 'Dhaka',
    ('vietnam',    'netherlands'): 'Hanoi',
    # Dutch Embassy covering Somalia is in Nairobi
    ('somalia',    'netherlands'): 'Nairobi',
    # Dutch Embassy covering Eritrea is in Addis Ababa
    ('eritrea',    'netherlands'): 'Addis Ababa',
    # R28: Italy wave 3
    ('ecuador',      'italy'): 'Quito',
    ('peru',         'italy'): 'Lima',
    ('ghana',        'italy'): 'Accra',
    ('tunisia',      'italy'): 'Tunis',
    ('ivory-coast',  'italy'): 'Abidjan',
    # R28: Belgium wave 3
    ('algeria',     'belgium'): 'Algiers',
    ('ivory-coast', 'belgium'): 'Abidjan',
    ('ghana',       'belgium'): 'Accra',
    ('poland',      'belgium'): 'Warsaw',
    ('vietnam',     'belgium'): 'Hanoi',
    # R28: Saudi Arabia wave 2
    ('somalia', 'saudi-arabia'): 'Mogadishu',
    ('iraq',    'saudi-arabia'): 'Baghdad',
    # Yemen: Saudi Embassy coordinates with recognised government in Aden
    ('yemen',   'saudi-arabia'): 'Aden',
    ('turkey',  'saudi-arabia'): 'Ankara',
    # Sudan: nominal capital; situation complex since April 2023 conflict
    ('sudan',   'saudi-arabia'): 'Khartoum',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R26: Switzerland corridors
    ('turkey', 'switzerland'): (
        "Turkish nationals form one of Switzerland's largest non-EU immigrant communities, "
        "with over 100,000 residents concentrated in Zurich, Basel, and Bern. This is a "
        "well-established repatriation corridor. Turkish Airlines operates direct cargo "
        "services between Istanbul and Zurich. Documentation takes 5 to 10 days."
    ),
    ('portugal', 'switzerland'): (
        "Portuguese nationals form one of Switzerland's largest migrant communities, with an "
        "estimated 250,000 to 280,000 residents concentrated in the French-speaking cantons "
        "of Geneva and Vaud. Portugal to Switzerland is an active repatriation corridor, "
        "with direct air links and well-established procedures on both sides. Documentation "
        "is in Portuguese from the origin side, requiring certified German or French translation "
        "for Swiss authorities."
    ),
    ('italy', 'switzerland'): (
        "Italian nationals and people of Italian heritage form Switzerland's largest historical "
        "migrant community, with ties going back to the guest-worker era of the 1950s to 1970s. "
        "Over 600,000 Italian-heritage residents live in Switzerland, concentrated in the "
        "Italian-speaking canton of Ticino and across the German-speaking cantons. "
        "Proximity and regular direct flights make this one of the shorter European "
        "repatriation turnarounds."
    ),
    ('germany', 'switzerland'): (
        "German nationals and professionals form a significant community in German-speaking "
        "Switzerland, particularly in Zurich and Basel, working in finance, engineering, "
        "pharmaceutical, and academic sectors. This corridor handles cases where a "
        "Switzerland-based German national has a family member die in Germany and needs "
        "remains brought to Switzerland. German documentation is straightforward for "
        "Swiss authorities, and direct rail and air links connect the two countries."
    ),
    ('india', 'switzerland'): (
        "Indian nationals work in Switzerland in pharmaceutical, technology, and financial "
        "services sectors, with significant numbers in the Basel and Zurich areas. This "
        "corridor handles cases where a Switzerland-based Indian has a family member die "
        "in India and needs remains brought to Switzerland. Indian documentation requires "
        "certified German or French translation for Swiss authorities, and the process "
        "typically takes longer than European corridors."
    ),
    # R26: Sweden corridors
    ('syria', 'sweden'): (
        "Syrian nationals form one of Sweden's largest immigrant communities. Sweden accepted "
        "more Syrian refugees per capita than almost any other European country between 2011 "
        "and 2016. This corridor handles cases where a Sweden-based Syrian has a family member "
        "die in Syria and needs remains brought to Sweden. Documentation from Syria is "
        "complicated by the ongoing situation in the country. Specialist coordination is "
        "essential. The Swedish Embassy in Damascus closed in 2012; Swedish consular services "
        "for Syria are handled from Beirut. (FCDO Syria travel advice, 2025.)"
    ),
    ('somalia', 'sweden'): (
        "Somali nationals form one of Sweden's larger African communities, with significant "
        "populations in Stockholm, Gothenburg, and Malmo. Sweden has one of the largest Somali "
        "diaspora populations in Europe. Somalia to Sweden is a complex corridor: Somalia's "
        "fragile civil registration system and limited consular infrastructure mean specialist "
        "coordination is essential. The Swedish Embassy covering Somalia is based in Nairobi, "
        "Kenya. (Swedish Ministry of Foreign Affairs, UD, 2025.)"
    ),
    ('iraq', 'sweden'): (
        "Iraqi nationals form one of Sweden's larger Middle Eastern communities. Sweden "
        "received significant numbers of Iraqi refugees in the 1990s and 2000s. This corridor "
        "handles cases where a Sweden-based Iraqi has a family member die in Iraq and needs "
        "remains brought to Sweden. The Swedish Embassy in Baghdad handles consular matters. "
        "Arabic documentation requires certified Swedish translation."
    ),
    ('poland', 'sweden'): (
        "Polish nationals work in Sweden in construction, agriculture, healthcare, and "
        "service industries, part of EU freedom of movement labour migration. Poland to "
        "Sweden is an established EU repatriation corridor with straightforward documentation "
        "procedures on both sides. The EU apostille framework applies and direct flights "
        "connect Warsaw, Krakow, and Gdansk to Stockholm and Gothenburg."
    ),
    ('afghanistan', 'sweden'): (
        "Afghan nationals and Swedish residents of Afghan heritage form a community across "
        "Swedish cities, with arrivals in several waves since the 1990s and accelerating "
        "following 2021. This corridor handles cases where a Sweden-based Afghan has a family "
        "member die in Afghanistan and needs remains brought to Sweden. The Swedish Embassy "
        "in Kabul closed in 2021; Swedish consular services for Afghanistan are handled "
        "via Islamabad. Specialist coordination is essential. (Swedish MFA, UD, 2025.)"
    ),
    # R26: Norway corridors
    ('poland', 'norway'): (
        "Polish nationals form Norway's largest immigrant community, with over 100,000 "
        "residents working in construction, agriculture, and industry across the country. "
        "Poland to Norway is one of Norway's highest-volume repatriation corridors. "
        "EU documentation procedures apply on both sides, and the Norwegian Embassy in "
        "Warsaw handles any consular matters. Direct flights connect Warsaw and Krakow to Oslo."
    ),
    ('somalia', 'norway'): (
        "Somali nationals form one of Norway's larger non-European communities, "
        "concentrated in Oslo. Norway has a significant Somali diaspora community. "
        "Somalia to Norway is a complex corridor: Somalia's fragile civil registration "
        "infrastructure and lack of a resident Norwegian Embassy in Mogadishu mean "
        "specialist coordination is essential. Norwegian consular services for Somalia "
        "are handled from the Norwegian Embassy in Nairobi, Kenya. (Norwegian MFA, 2025.)"
    ),
    ('pakistan', 'norway'): (
        "Pakistani nationals form Norway's second-largest immigrant community by origin "
        "country, with over 40,000 residents concentrated in Oslo. This is a well-established "
        "repatriation corridor with consistent demand. Pakistani documentation takes 10 to 21 "
        "days and requires certified Norwegian translation. The Norwegian Embassy in "
        "Islamabad handles consular matters."
    ),
    ('india', 'norway'): (
        "Indian nationals work in Norway in technology, healthcare, oil and gas, and "
        "engineering sectors, with significant numbers in Oslo and Stavanger. This corridor "
        "handles cases where a Norway-based Indian has a family member die in India and "
        "needs remains brought to Norway. Indian documentation requires certified Norwegian "
        "translation and typically takes several weeks."
    ),
    ('philippines', 'norway'): (
        "Filipino nationals work in Norway in healthcare, domestic, and maritime sectors. "
        "This corridor handles cases where a Norway-based Filipino has a family member die "
        "in the Philippines and needs remains brought to Norway. The Philippine DFA "
        "authentication process is the primary documentation delay on this corridor. "
        "The Norwegian Embassy in Manila handles consular matters."
    ),
    # R26: Portugal corridors
    ('brazil', 'portugal'): (
        "Brazilian nationals form the largest immigrant community in Portugal, with over "
        "400,000 residents. Brazil and Portugal share language, legal traditions, and close "
        "cultural ties. This is Portugal's highest-volume non-EU repatriation corridor. "
        "Documentation is in Portuguese on both sides, which simplifies many requirements. "
        "Direct flights connect Sao Paulo, Rio de Janeiro, and other Brazilian cities to Lisbon."
    ),
    ('angola', 'portugal'): (
        "Angolan nationals form a significant community in Portugal, reflecting historical "
        "and cultural ties between the two countries. Angola and Portugal share the "
        "Portuguese language, which simplifies documentation requirements. This corridor "
        "sees consistent repatriation demand. The Portuguese Embassy in Luanda handles "
        "consular matters. Angola's Conservatoria do Registo Civil issues the certidao de obito."
    ),
    ('mozambique', 'portugal'): (
        "Mozambican nationals form part of Portugal's Lusophone African diaspora. Portugal "
        "and Mozambique share the Portuguese language and longstanding cultural connections. "
        "This corridor handles cases where a Portugal-based Mozambican has a family member "
        "die in Mozambique and needs remains brought to Portugal. Documentation is in "
        "Portuguese on both sides, and the Portuguese Embassy in Maputo handles consular matters."
    ),
    ('cabo-verde', 'portugal'): (
        "Cabo Verdean nationals form one of Portugal's most established immigrant communities, "
        "with deep roots going back to the 1970s. The two countries share language and close "
        "cultural ties, with significant Cabo Verdean communities in Lisbon and Setubal. "
        "Direct flights connect Praia and Sao Vicente to Lisbon. Documentation is in "
        "Portuguese on both sides, and the Portuguese Embassy in Praia handles consular matters."
    ),
    ('guinea-bissau', 'portugal'): (
        "Guinea-Bissau nationals form part of Portugal's Lusophone African diaspora, "
        "with a community concentrated in Lisbon. Guinea-Bissau uses Portuguese as its "
        "official language, which simplifies documentation requirements. This corridor "
        "handles cases where a Portugal-based Guinean has a family member die in "
        "Guinea-Bissau and needs remains brought to Portugal. The UK has no resident "
        "embassy in Guinea-Bissau; British nationals should contact the FCDO emergency "
        "line. The Portuguese Embassy in Bissau handles consular matters for Portugal. "
        "(FCDO Guinea-Bissau travel advice, 2025.)"
    ),
    # R26: Extra waves to established hubs
    ('turkey', 'france'): (
        "Turkish nationals form a significant immigrant community in France, with an "
        "estimated 500,000 residents concentrated in the Alsace-Moselle region, the Paris "
        "area, and Lyon. France is the third-largest European destination for Turkish "
        "diaspora after Germany and the Netherlands. Turkish Airlines operates direct cargo "
        "services between Istanbul and Charles de Gaulle. Documentation takes 5 to 10 days."
    ),
    ('iraq', 'france'): (
        "Iraqi nationals form part of France's Middle Eastern diaspora, with communities "
        "in Paris and other major cities. France received significant Iraqi migration "
        "following the Gulf War and the 2003 conflict. This corridor handles cases where "
        "a France-based Iraqi has a family member die in Iraq and needs remains brought "
        "to France. Arabic documentation requires certified French translation."
    ),
    ('ghana', 'netherlands'): (
        "Ghanaian nationals form one of the Netherlands' established West African communities, "
        "with over 40,000 residents concentrated in Amsterdam, particularly in the "
        "Zuidoost district. This corridor handles cases where a Netherlands-based Ghanaian "
        "has a family member die in Ghana and needs remains brought to the Netherlands. "
        "English documentation from Ghana simplifies translation requirements for "
        "Dutch authorities where English is accepted."
    ),
    ('ghana', 'spain'): (
        "Ghanaian nationals form part of Spain's West African diaspora, with communities "
        "in Madrid, Barcelona, and Valencia. This corridor handles cases where a "
        "Spain-based Ghanaian has a family member die in Ghana and needs remains brought "
        "to Spain. English documentation from Ghana requires certified Spanish translation "
        "for Spanish civil registry purposes."
    ),
    ('kenya', 'netherlands'): (
        "Kenyan nationals form part of the Netherlands' East African diaspora, working "
        "in professional, academic, and service roles. This corridor handles cases where "
        "a Netherlands-based Kenyan has a family member die in Kenya and needs remains "
        "brought to the Netherlands. English documentation from Kenya simplifies "
        "translation requirements where Dutch or English is accepted."
    ),
    # R27: Switzerland wave 2
    ('france', 'switzerland'): (
        "French nationals form Switzerland's largest EU immigrant community, with an "
        "estimated 310,000 residents concentrated in the French-speaking cantons of "
        "Geneva, Vaud, and Neuchatel. Many work in international organisations, finance, "
        "and the hospitality sector. This is one of Switzerland's most active European "
        "repatriation corridors, with frequent direct flights and well-understood "
        "procedures on both sides."
    ),
    ('spain', 'switzerland'): (
        "Spanish nationals form a significant community in Switzerland, with around "
        "80,000 residents working in hospitality, construction, and professional services. "
        "Many settled during the guest-worker era of the 1950s and 1960s. Direct flights "
        "connect Madrid and Barcelona to Zurich and Geneva. Spanish documentation is "
        "straightforward for Swiss authorities with certified German or French translation."
    ),
    ('morocco', 'switzerland'): (
        "Moroccan nationals form one of Switzerland's largest non-EU communities, with "
        "around 80,000 residents concentrated in the German and French-speaking cantons. "
        "This corridor handles cases where a Switzerland-based Moroccan has a family "
        "member die in Morocco and needs remains brought to Switzerland. Arabic "
        "documentation requires certified German or French translation for Swiss authorities."
    ),
    ('eritrea', 'switzerland'): (
        "Switzerland hosts one of the world's largest Eritrean diaspora communities per "
        "capita, with around 35,000 residents. Switzerland accepted significant numbers "
        "of Eritrean asylum seekers from 2010 onward. This is an active repatriation "
        "corridor, though Eritrea's civil registration system and documentation procedures "
        "require specialist coordination. Switzerland covers Eritrea consularly from its "
        "Embassy in Addis Ababa. (Swiss Federal Department of Foreign Affairs, FDFA, 2025.)"
    ),
    ('pakistan', 'switzerland'): (
        "Pakistani nationals form a growing community in Switzerland, concentrated in "
        "Zurich, Geneva, and Basel, working in healthcare, technology, and service "
        "industries. This corridor handles cases where a Switzerland-based Pakistani has "
        "a family member die in Pakistan and needs remains brought to Switzerland. "
        "Pakistani documentation requires certified German or French translation and "
        "typically takes several weeks."
    ),
    # R27: Sweden wave 2
    ('turkey', 'sweden'): (
        "Turkish nationals and Swedish residents of Turkish heritage form Sweden's largest "
        "Muslim community, with over 150,000 residents concentrated in Stockholm, "
        "Gothenburg, and Malmo. Many arrived during the labour migration of the 1960s "
        "and 1970s. Turkey to Sweden is an established repatriation corridor. Turkish "
        "Airlines operates direct services between Istanbul and Swedish airports."
    ),
    ('iran', 'sweden'): (
        "Iranian nationals form one of Sweden's largest Middle Eastern communities, with "
        "over 80,000 residents. Sweden received significant numbers of Iranian refugees "
        "following the 1979 revolution and again after 2009. This corridor handles cases "
        "where a Sweden-based Iranian has a family member die in Iran and needs remains "
        "brought to Sweden. Persian documentation requires certified Swedish translation. "
        "The Swedish Embassy in Tehran handles consular matters."
    ),
    ('eritrea', 'sweden'): (
        "Eritrean nationals form one of Sweden's largest African communities, with over "
        "60,000 residents. Sweden received substantial numbers of Eritrean asylum seekers "
        "from 2010 onward. This corridor sees consistent repatriation demand. Eritrea's "
        "civil registration system requires specialist coordination. The Swedish Embassy "
        "covering Eritrea is based in Nairobi, Kenya. (Swedish Ministry of Foreign "
        "Affairs, UD, 2025.)"
    ),
    ('ethiopia', 'sweden'): (
        "Ethiopian nationals form a growing community in Sweden, concentrated in "
        "Stockholm and Gothenburg. This corridor handles cases where a Sweden-based "
        "Ethiopian has a family member die in Ethiopia and needs remains brought to Sweden. "
        "The Swedish Embassy in Addis Ababa handles consular matters. Amharic documentation "
        "requires certified Swedish translation."
    ),
    ('bosnia-and-herzegovina', 'sweden'): (
        "Bosnian nationals and Swedish residents of Bosnian heritage form a significant "
        "community in Sweden, concentrated in cities across Skane, Stockholm, and "
        "Gothenburg. The majority arrived as refugees during the 1992 to 1995 conflict. "
        "Sweden has one of the largest Bosnian diaspora communities in Europe. Direct "
        "flights and EU-adjacent documentation procedures make this a manageable corridor."
    ),
    # R27: Norway wave 2
    ('iraq', 'norway'): (
        "Iraqi nationals form one of Norway's larger Middle Eastern communities, with "
        "significant numbers concentrated in Oslo. Norway received Iraqi refugees in the "
        "1990s and 2000s. This corridor handles cases where a Norway-based Iraqi has a "
        "family member die in Iraq and needs remains brought to Norway. The Norwegian "
        "Embassy in Baghdad handles consular matters. Arabic documentation requires "
        "certified Norwegian translation."
    ),
    ('iran', 'norway'): (
        "Iranian nationals form a significant community in Norway, concentrated in Oslo "
        "and Bergen. Norway received Iranian refugees across several waves from 1979 "
        "onward. This corridor handles cases where a Norway-based Iranian has a family "
        "member die in Iran and needs remains brought to Norway. The Norwegian Embassy "
        "in Tehran handles consular matters."
    ),
    ('vietnam', 'norway'): (
        "Vietnamese nationals form one of Norway's more established Asian communities, "
        "with many having arrived as refugees in the late 1970s and 1980s. This corridor "
        "handles cases where a Norway-based Vietnamese has a family member die in Vietnam "
        "and needs remains brought to Norway. The Norwegian Embassy in Hanoi handles "
        "consular matters."
    ),
    ('eritrea', 'norway'): (
        "Eritrean nationals form one of Norway's larger African communities. Norway "
        "received significant numbers of Eritrean asylum seekers from 2010 onward. "
        "This corridor requires specialist coordination, as Eritrea's civil registration "
        "system is limited. Norwegian consular services for Eritrea are provided from "
        "the Norwegian Embassy in Nairobi, Kenya. (Norwegian Ministry of Foreign "
        "Affairs, 2025.)"
    ),
    ('ethiopia', 'norway'): (
        "Ethiopian nationals form a growing community in Norway, concentrated in Oslo. "
        "This corridor handles cases where a Norway-based Ethiopian has a family member "
        "die in Ethiopia and needs remains brought to Norway. The Norwegian Embassy in "
        "Addis Ababa handles consular matters. Amharic documentation requires certified "
        "Norwegian translation."
    ),
    # R27: Portugal wave 2
    ('france', 'portugal'): (
        "Around 580,000 Portuguese nationals live and work in France, forming one of "
        "France's largest immigrant communities. When a Portugal-based family loses a "
        "member who died in France, or a Portugal-based person loses a French-resident "
        "relative, repatriation to Portugal is one of the most common European corridors. "
        "EU documentation procedures apply on both sides, and direct air links connect "
        "Paris, Lyon, and other French cities to Lisbon and Porto."
    ),
    ('spain', 'portugal'): (
        "Portuguese nationals form Spain's largest EU immigrant community, with around "
        "400,000 residents working across Spanish regions. When a Portugal-based family "
        "has a member die in Spain, EU freedom of movement procedures apply on both "
        "sides. Direct road and air links mean transfer logistics are relatively "
        "straightforward. The Portuguese Embassy in Madrid handles consular matters."
    ),
    ('india', 'portugal'): (
        "Indian nationals form a growing professional and business community in Portugal, "
        "concentrated in Lisbon and the Algarve. The Indian community has expanded "
        "significantly since 2015 with Portugal's Golden Visa programme. This corridor "
        "handles cases where a Portugal-based Indian has a family member die in India "
        "and needs remains brought to Portugal. The Portuguese Embassy in New Delhi "
        "handles consular matters."
    ),
    ('china', 'portugal'): (
        "Chinese nationals form an established business community in Portugal, concentrated "
        "in Lisbon, where a significant Chinese-heritage population has been settled for "
        "several decades. This corridor handles cases where a Portugal-based Chinese "
        "national has a family member die in China and needs remains brought to Portugal. "
        "Chinese documentation requires certified Portuguese translation."
    ),
    ('venezuela', 'portugal'): (
        "Portugal has received a significant number of Venezuelans since 2015, many "
        "claiming Portuguese heritage through the Law of Return. The community in Lisbon "
        "and Porto has grown considerably. This corridor handles cases where a "
        "Portugal-based Venezuelan has a family member die in Venezuela and needs remains "
        "brought to Portugal. Documentation is in Spanish from Venezuela, requiring "
        "certified Portuguese translation."
    ),
    # R27: Additional Tier B waves
    ('eritrea', 'italy'): (
        "Eritrean nationals form one of Italy's most established African communities, "
        "with over 40,000 registered residents concentrated in Rome and other major "
        "cities. Many arrived via the Mediterranean crossing routes during the 2010s. "
        "Italy has historical connections with Eritrea dating to the colonial period. "
        "The Italian Embassy in Asmara handles consular matters. Tigrinya and Amharic "
        "documentation requires certified Italian translation. "
        "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
    ),
    ('ethiopia', 'germany'): (
        "Ethiopian nationals form Germany's largest East African community, with over "
        "30,000 residents concentrated in Berlin, Frankfurt, and Hamburg. The Ethiopian "
        "community in Germany includes students, professionals, and long-settled families. "
        "The German Embassy in Addis Ababa handles consular matters. Amharic documentation "
        "requires certified German translation."
    ),
    ('kenya', 'germany'): (
        "Kenyan nationals work in Germany in healthcare, academia, and professional "
        "services. This corridor handles cases where a Germany-based Kenyan has a family "
        "member die in Kenya and needs remains brought to Germany. The German Embassy "
        "in Nairobi handles consular matters. English documentation from Kenya simplifies "
        "requirements where German or English is accepted."
    ),
    ('senegal', 'germany'): (
        "Senegalese nationals form part of Germany's West African diaspora, working in "
        "healthcare, academic, and service roles across cities including Berlin and "
        "Frankfurt. This corridor handles cases where a Germany-based Senegalese has a "
        "family member die in Senegal and needs remains brought to Germany. French "
        "documentation from Senegal requires certified German translation."
    ),
    ('cameroon', 'germany'): (
        "Cameroonian nationals form a significant West African community in Germany, with "
        "students and professionals concentrated in Berlin, Frankfurt, and Hamburg. "
        "Cameroon and Germany have historical ties dating to the colonial period. This "
        "corridor handles cases where a Germany-based Cameroonian has a family member "
        "die in Cameroon and needs remains brought to Germany. French and English "
        "documentation from Cameroon requires certified German translation."
    ),
    # R28: Spain wave 3
    ('argentina', 'spain'): (
        "Argentine nationals form a large Latin American community in Spain, with over "
        "300,000 residents concentrated in Madrid, Barcelona, and Valencia. Argentina "
        "and Spain share language and many legal traditions, with documentation in "
        "Spanish on both sides. Direct flights connect Buenos Aires to Madrid. Argentina "
        "to Spain is one of the more straightforward transatlantic repatriation corridors."
    ),
    ('cuba', 'spain'): (
        "Cuban nationals form part of Spain's Caribbean diaspora, with a community "
        "concentrated in Madrid and the Canary Islands. Cuba and Spain share language "
        "and historical connections. This corridor handles cases where a Spain-based "
        "Cuban has a family member die in Cuba and needs remains brought to Spain. "
        "Documentation is in Spanish on both sides, and the Spanish Embassy in Havana "
        "handles consular matters."
    ),
    ('brazil', 'spain'): (
        "Brazilian nationals form one of Spain's larger Latin American communities, "
        "with over 150,000 residents. Close family ties and a significant number of "
        "dual nationals mean this corridor sees consistent demand. Documentation from "
        "Brazil is in Portuguese, requiring certified Spanish translation for Spanish "
        "civil registry purposes. Direct flights connect Sao Paulo, Rio de Janeiro, "
        "and other Brazilian cities to Madrid and Barcelona."
    ),
    ('philippines', 'spain'): (
        "Filipino nationals work in Spain in domestic care, healthcare, and service "
        "roles, particularly in Madrid and Barcelona. The Spanish Embassy in Manila "
        "handles consular matters. This corridor handles cases where a Spain-based "
        "Filipino has a family member die in the Philippines and needs remains brought "
        "to Spain. The Philippine DFA authentication process is the primary documentation "
        "delay. Filipino documentation requires certified Spanish translation."
    ),
    ('senegal', 'spain'): (
        "Senegalese nationals form part of Spain's West African diaspora, concentrated "
        "in Catalonia and the Canary Islands. Senegal is one of the primary origins of "
        "West African migration to Spain. This corridor handles cases where a Spain-based "
        "Senegalese has a family member die in Senegal and needs remains brought to Spain. "
        "French documentation from Senegal requires certified Spanish translation."
    ),
    # R28: Netherlands wave 3
    ('nigeria', 'netherlands'): (
        "Nigerian nationals form one of the Netherlands' largest African communities, "
        "with over 40,000 residents concentrated in Amsterdam and Rotterdam. This "
        "corridor handles cases where a Netherlands-based Nigerian has a family member "
        "die in Nigeria and needs remains brought to the Netherlands. English "
        "documentation from Nigeria simplifies requirements where Dutch or English is "
        "accepted. The Dutch Embassy in Abuja handles consular matters."
    ),
    ('bangladesh', 'netherlands'): (
        "Bangladeshi nationals form a growing South Asian community in the Netherlands, "
        "concentrated in Amsterdam and Rotterdam. This corridor handles cases where a "
        "Netherlands-based Bangladeshi has a family member die in Bangladesh and needs "
        "remains brought to the Netherlands. Bengali documentation requires certified "
        "Dutch translation. The Dutch Embassy in Dhaka handles consular matters."
    ),
    ('vietnam', 'netherlands'): (
        "Vietnamese nationals form one of the Netherlands' established Asian communities, "
        "with significant numbers in Rotterdam and Amsterdam. This corridor handles cases "
        "where a Netherlands-based Vietnamese has a family member die in Vietnam and "
        "needs remains brought to the Netherlands. Vietnamese documentation requires "
        "certified Dutch translation. The Dutch Embassy in Hanoi handles consular matters."
    ),
    ('somalia', 'netherlands'): (
        "Somali nationals form one of the Netherlands' larger African communities, "
        "concentrated in Amsterdam. The Netherlands received substantial numbers of "
        "Somali asylum seekers in the 1990s and 2000s. This corridor requires specialist "
        "coordination, as Somalia's fragile civil registration system limits "
        "documentation availability. Dutch consular services for Somalia are provided "
        "from the Dutch Embassy in Nairobi, Kenya. (Dutch Ministry of Foreign Affairs, 2025.)"
    ),
    ('eritrea', 'netherlands'): (
        "Eritrean nationals form part of the Netherlands' African diaspora, with a "
        "growing community in Amsterdam and other Dutch cities. The Netherlands received "
        "significant numbers of Eritrean asylum seekers from 2010 onward. This corridor "
        "requires specialist coordination given Eritrea's limited civil registration "
        "capacity. Dutch consular services for Eritrea are provided from the Dutch "
        "Embassy in Addis Ababa, Ethiopia. (Dutch Ministry of Foreign Affairs, 2025.)"
    ),
    # R28: Italy wave 3
    ('ecuador', 'italy'): (
        "Ecuadorian nationals form one of Italy's larger Latin American communities, "
        "with over 75,000 residents concentrated in Milan, Genoa, and other northern "
        "cities. Many arrived during the economic crisis in Ecuador in the late 1990s "
        "and early 2000s. Documentation from Ecuador is in Spanish, requiring certified "
        "Italian translation. The Italian Embassy in Quito handles consular matters."
    ),
    ('peru', 'italy'): (
        "Peruvian nationals form a significant Latin American community in Italy, with "
        "over 100,000 residents concentrated in Milan, Turin, and Rome. Peru to Italy "
        "is one of Italy's more established South American repatriation corridors. "
        "Documentation from Peru is in Spanish, requiring certified Italian translation. "
        "The Italian Embassy in Lima handles consular matters."
    ),
    ('ghana', 'italy'): (
        "Ghanaian nationals form one of Italy's established West African communities, "
        "concentrated in Brescia, Bergamo, and other northern cities. Many work in "
        "manufacturing, agriculture, and domestic services. English documentation from "
        "Ghana requires certified Italian translation for Italian civil registry purposes. "
        "The Italian Embassy in Accra handles consular matters."
    ),
    ('tunisia', 'italy'): (
        "Tunisian nationals form one of Italy's oldest non-EU immigrant communities, "
        "with over 100,000 residents concentrated in Sicily, Sardinia, and northern "
        "industrial cities. The geographic proximity of Tunis to Sicily means this "
        "corridor involves shorter transit distances than most Mediterranean routes. "
        "Arabic documentation requires certified Italian translation. The Italian "
        "Embassy in Tunis handles consular matters."
    ),
    ('ivory-coast', 'italy'): (
        "Ivorian nationals form part of Italy's West African diaspora, with communities "
        "in Milan, Turin, and Rome. This corridor handles cases where an Italy-based "
        "Ivorian has a family member die in Ivory Coast and needs remains brought to "
        "Italy. French documentation from Ivory Coast requires certified Italian "
        "translation. The Italian Embassy in Abidjan handles consular matters."
    ),
    # R28: Belgium wave 3
    ('algeria', 'belgium'): (
        "Algerian nationals form a significant part of Belgium's Maghrebi diaspora, "
        "with a community concentrated in Brussels, Liege, and Antwerp. France and "
        "Belgium share close ties with the Maghreb; French documentation from Algeria "
        "simplifies some translation requirements for Belgian authorities. The Belgian "
        "Embassy in Algiers handles consular matters."
    ),
    ('ivory-coast', 'belgium'): (
        "Ivorian nationals form a significant Francophone African community in Belgium, "
        "reflecting linguistic and historical connections. French documentation from "
        "Ivory Coast simplifies some requirements for Belgian authorities. This corridor "
        "handles cases where a Belgium-based Ivorian has a family member die in Ivory "
        "Coast and needs remains brought to Belgium. The Belgian Embassy in Abidjan "
        "handles consular matters."
    ),
    ('ghana', 'belgium'): (
        "Ghanaian nationals form part of Belgium's African diaspora, with communities "
        "in Brussels and Antwerp. This corridor handles cases where a Belgium-based "
        "Ghanaian has a family member die in Ghana and needs remains brought to Belgium. "
        "English documentation from Ghana requires certified French or Dutch translation "
        "for Belgian civil registry purposes. The Belgian Embassy in Accra handles "
        "consular matters."
    ),
    ('poland', 'belgium'): (
        "Polish nationals form one of Belgium's largest EU immigrant communities, "
        "working in construction, agriculture, logistics, and industry. EU freedom of "
        "movement and the Apostille Convention make documentation on this corridor "
        "relatively straightforward. Direct flights connect Warsaw and Krakow to "
        "Brussels. The Belgian Embassy in Warsaw handles consular matters."
    ),
    ('vietnam', 'belgium'): (
        "Vietnamese nationals form one of Belgium's established Asian communities, "
        "concentrated in Brussels. Belgium has historical ties with Vietnam through "
        "the French colonial connection to Indochina. This corridor handles cases "
        "where a Belgium-based Vietnamese has a family member die in Vietnam and needs "
        "remains brought to Belgium. Vietnamese documentation requires certified French "
        "or Dutch translation. The Belgian Embassy in Hanoi handles consular matters."
    ),
    # R28: Saudi Arabia wave 2
    ('somalia', 'saudi-arabia'): (
        "Somali nationals form a significant community in Saudi Arabia, many working in "
        "trade, construction, and domestic services across Riyadh, Jeddah, and Mecca. "
        "Saudi Arabia reopened its Embassy in Mogadishu in 2023 following years of "
        "reduced engagement. This corridor requires specialist coordination given "
        "Somalia's limited civil registration capacity. All documents must be "
        "authenticated by the Saudi Embassy in the origin country. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('iraq', 'saudi-arabia'): (
        "Iraqi nationals form part of Saudi Arabia's expatriate workforce and diaspora, "
        "working in construction, engineering, and professional services. This corridor "
        "handles cases where a Saudi-based Iraqi has a family member die in Iraq and "
        "needs remains brought to Saudi Arabia. Arabic documentation is the working "
        "language on both sides. The Saudi Embassy in Baghdad handles consular matters."
    ),
    ('yemen', 'saudi-arabia'): (
        "Yemeni nationals have historically formed a very large community in Saudi Arabia. "
        "The repatriation corridor from Yemen to Saudi Arabia involves considerable "
        "complexity because of the ongoing conflict in Yemen since 2015. Documentation "
        "from Houthi-controlled areas and from government-controlled areas follows "
        "different paths. The Saudi Embassy coordinates with the internationally recognised "
        "Yemeni government based in Aden. Specialist coordination is essential on this "
        "corridor. (Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('turkey', 'saudi-arabia'): (
        "Turkish nationals work in Saudi Arabia in construction, engineering, and "
        "professional services, with Turkish contractors historically active in large "
        "infrastructure projects. Turkish Airlines operates direct services between "
        "Istanbul and Riyadh, Jeddah, and Dammam. This corridor handles cases where a "
        "Saudi-based Turkish national has a family member die in Turkey and needs remains "
        "brought to Saudi Arabia. The Saudi Embassy in Ankara handles consular matters."
    ),
    ('sudan', 'saudi-arabia'): (
        "Sudanese nationals form a significant community in Saudi Arabia, many working "
        "in agriculture, construction, and domestic services. This corridor handles "
        "cases where a Saudi-based Sudanese has a family member die in Sudan and needs "
        "remains brought to Saudi Arabia. The ongoing conflict in Sudan since April 2023 "
        "means documentation access from affected regions requires specialist support. "
        "The Saudi Embassy coordinates with authorities in Khartoum. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
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
        }
        short_origin = abbrevs.get(origin_name, origin_name)
        title = f"{short_origin} to {dest_name} Repatriation Guide"

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
    # Strip any em dashes or double-hyphens inherited from source files
    content = content.replace('vital statistics', 'civil registration')
    content = content.replace('—', ',')
    content = content.replace('–', ',')
    # Protect YAML front-matter delimiters before stripping double-hyphens
    content = content.replace('---', '\x00TRIPLE\x00')
    content = content.replace('--', ',')
    content = content.replace('\x00TRIPLE\x00', '---')
    return content


# ---------------------------------------------------------------------------
# Route list: chunk R26 = 25 routes
# Template rotation starts at D (index 3) -- R25 ended on C.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # Block R26: Switzerland x5 + Sweden x5 + Norway x5 + Portugal x5 + extra x5 = 25
    # Template rotation: D,E,A,B,C,D,E,A,B,C,D,E,A,B,C,D,E,A,B,C,D,E,A,B,C (ends C)
    ('turkey',        'switzerland'),
    ('portugal',      'switzerland'),
    ('italy',         'switzerland'),
    ('germany',       'switzerland'),
    ('india',         'switzerland'),
    ('syria',         'sweden'),
    ('somalia',       'sweden'),
    ('iraq',          'sweden'),
    ('poland',        'sweden'),
    ('afghanistan',   'sweden'),
    ('poland',        'norway'),
    ('somalia',       'norway'),
    ('pakistan',      'norway'),
    ('india',         'norway'),
    ('philippines',   'norway'),
    ('brazil',        'portugal'),
    ('angola',        'portugal'),
    ('mozambique',    'portugal'),
    ('cabo-verde',    'portugal'),
    ('guinea-bissau', 'portugal'),
    ('turkey',        'france'),
    ('iraq',          'france'),
    ('ghana',         'netherlands'),
    ('ghana',         'spain'),
    ('kenya',         'netherlands'),
    # Block R27: Switzerland wave 2 x5 + Sweden wave 2 x5 + Norway wave 2 x5 +
    #            Portugal wave 2 x5 + additional Tier B x5 = 25
    # Template rotation continues: D,E,A,B,C,D,E,A,B,C,D,E,A,B,C,D,E,A,B,C,D,E,A,B,C (ends C)
    ('france',                 'switzerland'),
    ('spain',                  'switzerland'),
    ('morocco',                'switzerland'),
    ('eritrea',                'switzerland'),
    ('pakistan',               'switzerland'),
    ('turkey',                 'sweden'),
    ('iran',                   'sweden'),
    ('eritrea',                'sweden'),
    ('ethiopia',               'sweden'),
    ('bosnia-and-herzegovina', 'sweden'),
    ('iraq',                   'norway'),
    ('iran',                   'norway'),
    ('vietnam',                'norway'),
    ('eritrea',                'norway'),
    ('ethiopia',               'norway'),
    ('france',                 'portugal'),
    ('spain',                  'portugal'),
    ('india',                  'portugal'),
    ('china',                  'portugal'),
    ('venezuela',              'portugal'),
    ('eritrea',                'italy'),
    ('ethiopia',               'germany'),
    ('kenya',                  'germany'),
    ('senegal',                'germany'),
    ('cameroon',               'germany'),
    # Block R28: Spain wave 3 x5 + Netherlands wave 3 x5 + Italy wave 3 x5 +
    #            Belgium wave 3 x5 + Saudi Arabia wave 2 x5 = 25
    # Template rotation continues: D,E,A,B,C,D,E,A,B,C,D,E,A,B,C,D,E,A,B,C,D,E,A,B,C (ends C)
    ('argentina',   'spain'),
    ('cuba',        'spain'),
    ('brazil',      'spain'),
    ('philippines', 'spain'),
    ('senegal',     'spain'),
    ('nigeria',     'netherlands'),
    ('bangladesh',  'netherlands'),
    ('vietnam',     'netherlands'),
    ('somalia',     'netherlands'),
    ('eritrea',     'netherlands'),
    ('ecuador',     'italy'),
    ('peru',        'italy'),
    ('ghana',       'italy'),
    ('tunisia',     'italy'),
    ('ivory-coast', 'italy'),
    ('algeria',     'belgium'),
    ('ivory-coast', 'belgium'),
    ('ghana',       'belgium'),
    ('poland',      'belgium'),
    ('vietnam',     'belgium'),
    ('somalia',     'saudi-arabia'),
    ('iraq',        'saudi-arabia'),
    ('yemen',       'saudi-arabia'),
    ('turkey',      'saudi-arabia'),
    ('sudan',       'saudi-arabia'),
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

total_processed = len(generated) + len(skipped) + len(errors)
print(f"\n--- BLOCK BREAKDOWN ---")
if total_processed > 25:
    r26 = [r for r in generated if r[0] in [
        'turkey-to-switzerland','portugal-to-switzerland','italy-to-switzerland',
        'germany-to-switzerland','india-to-switzerland','syria-to-sweden',
        'somalia-to-sweden','iraq-to-sweden','poland-to-sweden','afghanistan-to-sweden',
        'poland-to-norway','somalia-to-norway','pakistan-to-norway','india-to-norway',
        'philippines-to-norway','brazil-to-portugal','angola-to-portugal',
        'mozambique-to-portugal','cabo-verde-to-portugal','guinea-bissau-to-portugal',
        'turkey-to-france','iraq-to-france','ghana-to-netherlands',
        'ghana-to-spain','kenya-to-netherlands',
    ]]
    r27 = [r for r in generated if r[0] in [
        'france-to-switzerland','spain-to-switzerland','morocco-to-switzerland',
        'eritrea-to-switzerland','pakistan-to-switzerland',
        'turkey-to-sweden','iran-to-sweden','eritrea-to-sweden',
        'ethiopia-to-sweden','bosnia-and-herzegovina-to-sweden',
        'iraq-to-norway','iran-to-norway','vietnam-to-norway',
        'eritrea-to-norway','ethiopia-to-norway',
        'france-to-portugal','spain-to-portugal','india-to-portugal',
        'china-to-portugal','venezuela-to-portugal',
        'eritrea-to-italy','ethiopia-to-germany','kenya-to-germany',
        'senegal-to-germany','cameroon-to-germany',
    ]]
    r28 = [r for r in generated if r[0] in [
        'argentina-to-spain','cuba-to-spain','brazil-to-spain',
        'philippines-to-spain','senegal-to-spain',
        'nigeria-to-netherlands','bangladesh-to-netherlands',
        'vietnam-to-netherlands','somalia-to-netherlands','eritrea-to-netherlands',
        'ecuador-to-italy','peru-to-italy','ghana-to-italy',
        'tunisia-to-italy','ivory-coast-to-italy',
        'algeria-to-belgium','ivory-coast-to-belgium','ghana-to-belgium',
        'poland-to-belgium','vietnam-to-belgium',
        'somalia-to-saudi-arabia','iraq-to-saudi-arabia','yemen-to-saudi-arabia',
        'turkey-to-saudi-arabia','sudan-to-saudi-arabia',
    ]]
    for block_name, block_routes in [('R26', r26), ('R27', r27), ('R28', r28)]:
        if block_routes:
            print(
                f"  {block_name}: {len(block_routes)} routes, "
                f"variants {','.join(sorted(set(v for _, v in block_routes)))}"
            )
else:
    if generated:
        print(
            f"  R26: {len(generated)} routes, "
            f"variants {','.join(sorted(set(v for _, v in generated)))}"
        )

last_variant = VARIANTS[(START_VARIANT + len(generated) + len(skipped) - 1) % 5]
print(f"\nLast variant used: {last_variant}")
print(f"Next chunk should start at: {VARIANTS[(START_VARIANT + len(generated) + len(skipped)) % 5]}")
