#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R37-R38.

   R37: Greece wave 2 x5 + Austria wave 2 x5 + Denmark wave 2 x5 +
        Finland wave 2 x5 + New Zealand wave 3 x5 = 25
   R38: Japan wave 3 x5 + Greece wave 3 x5 + Austria wave 3 x5 +
        Denmark wave 3 x5 + Finland wave 3 x5 = 25

   Template rotation: R36 ended on C (index 2). R37 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R36 ended C (index 2); R37 starts D (index 3)

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
    # Hubs introduced in R35
    'greece': {
        'name': 'Greece',
        'slug': 'greece',
        'key': 'gr',
        'reception': (
            "The Greek funeral director (grafeiou teletou) takes custody at Athens "
            "Eleftherios Venizelos (ATH) or Thessaloniki Macedonia (SKG) cargo terminal. "
            "A local health authority clearance is required before burial or cremation. "
            "The Lixiarcheio (civil registry) registers the death. Greece is an EU and "
            "Hague Apostille Convention member. All foreign documents not in Greek require "
            "certified Greek translation. "
            "(Greek Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Greek Embassy in {city} can advise on documentation requirements for "
            "repatriation to Greece. Greek Ministry of Foreign Affairs emergency line: "
            "+30 210 3681 000 (24 hours). The Greek Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Greek funeral director takes custody at Athens Eleftherios Venizelos (ATH) "
            "or Thessaloniki (SKG) cargo terminal. Local health authority clearance is "
            "required before burial or cremation. The Lixiarcheio registers the death. "
            "All foreign documents require certified Greek translation. The receiving "
            "funeral director coordinates with local authorities."
        ),
        'emergency_line': '+30 210 3681 000',
        'hub_url': 'repatriation-from-greece',
    },
    'austria': {
        'name': 'Austria',
        'slug': 'austria',
        'key': 'at',
        'reception': (
            "The Austrian Bestattung (funeral director) takes custody at Vienna International "
            "(VIE) cargo terminal. A Leichenbegleitschein (body transport certificate) must "
            "accompany the remains. The local Standesamt (registry office) registers the "
            "death. The Bezirksverwaltungsbehoerde (district authority) may need to approve "
            "burial or cremation. Austria is an EU and Hague Apostille Convention member. "
            "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
        ),
        'consular_template': (
            "Austrian Embassy in {city} can advise on documentation requirements for "
            "repatriation to Austria. Austrian Federal Ministry for European and International "
            "Affairs (BMEIA) emergency line: +43 1 90115 3775 (24 hours). The Austrian "
            "Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Austrian Bestattung takes custody at Vienna International (VIE) cargo "
            "terminal. A Leichenbegleitschein must accompany the remains. The local "
            "Standesamt registers the death. The Bezirksverwaltungsbehoerde approves "
            "burial or cremation. Documents not in German require certified translation."
        ),
        'emergency_line': '+43 1 90115 3775',
        'hub_url': 'repatriation-from-austria',
    },
    'denmark': {
        'name': 'Denmark',
        'slug': 'denmark',
        'key': 'dk',
        'reception': (
            "The Danish begravelsesforretning (funeral director) takes custody at Copenhagen "
            "Kastrup (CPH) cargo terminal. A ligfølgebrev (body transit certificate) must "
            "accompany the remains. The civil registry records the death. Denmark is an EU "
            "and Hague Apostille Convention member. Documents not in Danish, English, or "
            "another major European language require certified Danish translation. "
            "(Danish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Danish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Denmark. Danish Ministry of Foreign Affairs emergency line: "
            "+45 33 92 00 00 (24 hours). The Danish Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Danish begravelsesforretning takes custody at Copenhagen Kastrup (CPH) "
            "cargo terminal. A ligfølgebrev must accompany the remains. The civil registry "
            "records the death. Documents not in Danish or English require certified Danish "
            "translation. The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+45 33 92 00 00',
        'hub_url': 'repatriation-from-denmark',
    },
    'finland': {
        'name': 'Finland',
        'slug': 'finland',
        'key': 'fi',
        'reception': (
            "The Finnish hautauspalvelu (funeral director) takes custody at Helsinki-Vantaa "
            "(HEL) cargo terminal. A siirtolupa (transport permit) issued by the "
            "aluehallintovirasto (Regional State Administrative Agency) is required before "
            "the remains can be transported. The Digi- ja vaestotietovirasto (DVV, Digital "
            "and Population Data Services Agency) records the death. Finland is an EU and "
            "Hague Apostille Convention member. Documents not in Finnish, Swedish, or "
            "English require certified translation. "
            "(Finnish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Finnish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Finland. Finnish Ministry of Foreign Affairs emergency line: "
            "+358 9 1605 5555 (24 hours). The Finnish Embassy cannot pay for or arrange "
            "repatriation."
        ),
        'arrival_faq': (
            "The Finnish hautauspalvelu takes custody at Helsinki-Vantaa (HEL) cargo "
            "terminal. A siirtolupa from the aluehallintovirasto is required. The DVV "
            "records the death. Documents not in Finnish, Swedish, or English require "
            "certified translation. The receiving funeral director coordinates with "
            "regional authorities."
        ),
        'emergency_line': '+358 9 1605 5555',
        'hub_url': 'repatriation-from-finland',
    },
    # Hub introduced in R32
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
    # Hub introduced in R32
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
# Embassy cities: destination country embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R37: Greece wave 2
    ('egypt',        'greece'): 'Cairo',
    ('turkey',       'greece'): 'Ankara',
    ('nigeria',      'greece'): 'Abuja',
    ('bangladesh',   'greece'): 'Dhaka',
    ('morocco',      'greece'): 'Rabat',
    # R37: Austria wave 2
    ('pakistan',     'austria'): 'Islamabad',
    ('ukraine',      'austria'): 'Kyiv',
    # Austrian Embassy in Kabul suspended Aug 2021; covered from Islamabad
    ('afghanistan',  'austria'): 'Islamabad',
    ('egypt',        'austria'): 'Cairo',
    ('morocco',      'austria'): 'Rabat',
    # R37: Denmark wave 2
    # Danish Embassy in Kabul suspended; covered from Islamabad
    ('afghanistan',  'denmark'): 'Islamabad',
    ('india',        'denmark'): 'New Delhi',
    ('vietnam',      'denmark'): 'Hanoi',
    ('morocco',      'denmark'): 'Rabat',
    ('nigeria',      'denmark'): 'Abuja',
    # R37: Finland wave 2
    # Finnish Embassy in Kabul suspended; covered from Islamabad
    ('afghanistan',  'finland'): 'Islamabad',
    ('vietnam',      'finland'): 'Hanoi',
    ('ethiopia',     'finland'): 'Addis Ababa',
    ('kenya',        'finland'): 'Nairobi',
    ('china',        'finland'): 'Beijing',
    # R37: New Zealand wave 3
    ('nepal',        'new-zealand'): 'Kathmandu',
    # NZ High Commission covers Bangladesh from New Delhi
    ('bangladesh',   'new-zealand'): 'New Delhi',
    ('kenya',        'new-zealand'): 'Nairobi',
    ('nigeria',      'new-zealand'): 'Abuja',
    # NZ High Commission covers Sri Lanka from New Delhi
    ('sri-lanka',    'new-zealand'): 'New Delhi',
    # R38: Japan wave 3
    ('iran',         'japan'): 'Tehran',
    ('pakistan',     'japan'): 'Islamabad',
    ('hong-kong',    'japan'): 'Hong Kong',
    ('sri-lanka',    'japan'): 'Colombo',
    ('laos',         'japan'): 'Vientiane',
    # R38: Greece wave 3
    ('ukraine',      'greece'): 'Kyiv',
    ('germany',      'greece'): 'Berlin',
    ('russia',       'greece'): 'Moscow',
    ('china',        'greece'): 'Beijing',
    ('philippines',  'greece'): 'Manila',
    # R38: Austria wave 3
    ('nigeria',      'austria'): 'Abuja',
    ('philippines',  'austria'): 'Manila',
    ('russia',       'austria'): 'Moscow',
    ('iran',         'austria'): 'Tehran',
    ('bosnia-and-herzegovina', 'austria'): 'Sarajevo',
    # R38: Denmark wave 3
    ('iran',         'denmark'): 'Tehran',
    # Danish Embassy covers Sri Lanka from New Delhi
    ('sri-lanka',    'denmark'): 'New Delhi',
    ('lebanon',      'denmark'): 'Beirut',
    ('russia',       'denmark'): 'Moscow',
    ('ethiopia',     'denmark'): 'Addis Ababa',
    # R38: Finland wave 3
    ('iran',         'finland'): 'Tehran',
    ('pakistan',     'finland'): 'Islamabad',
    ('nigeria',      'finland'): 'Abuja',
    ('bangladesh',   'finland'): 'Dhaka',
    ('ukraine',      'finland'): 'Kyiv',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R37: Greece wave 2
    ('egypt', 'greece'): (
        "Egyptian nationals form a community in Greece, with professionals and students "
        "concentrated in Athens and Thessaloniki. Egypt and Greece have historical ties "
        "through the Mediterranean, the Coptic Christian diaspora, and longstanding commercial "
        "shipping routes. Arabic documentation from Egypt requires certified Greek translation "
        "for Greek civil registry purposes. The Greek Embassy in Cairo handles consular "
        "matters. This corridor also covers Egyptian tourists and business travellers who die "
        "in Greece. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('turkey', 'greece'): (
        "Turkish nationals form a community in Greece, reflecting the complex bilateral "
        "relationship between the two countries. There is a Muslim minority in Greek Thrace "
        "with Turkish cultural ties, and Greek-Turkish business and tourism flows create a "
        "consistent repatriation corridor. Turkey and Greece are both NATO members with "
        "bilateral consular relations. Turkish documentation requires certified Greek "
        "translation for Greek civil registry purposes. The Greek Embassy in Ankara handles "
        "consular matters. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('nigeria', 'greece'): (
        "Nigerian nationals form part of Greece's sub-Saharan African community, working "
        "in agriculture, trade, and service sectors. Nigeria and Greece have bilateral "
        "diplomatic relations. English documentation from Nigeria still requires certified "
        "Greek translation for Greek Lixiarcheio (civil registry) purposes. The Greek "
        "Embassy in Abuja handles consular matters. Nigeria to Greece is a growing corridor "
        "as West African migration to Southern Europe has increased in recent years."
    ),
    ('bangladesh', 'greece'): (
        "Bangladeshi nationals form a growing community in Greece, concentrated in Athens "
        "and working in agriculture, hospitality, and trade. Bangladesh and Greece have "
        "bilateral diplomatic ties. Bengali documentation from Bangladesh requires certified "
        "Greek translation. The Greek Embassy in Dhaka handles consular matters. Bangladesh "
        "to Greece is a consistent labour migration corridor with an established diaspora "
        "in the greater Athens region. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('morocco', 'greece'): (
        "Moroccan nationals form part of Greece's North African community, with migrants "
        "working in agriculture, construction, and service sectors across mainland Greece "
        "and the islands. Arabic and Darija documentation from Morocco requires certified "
        "Greek translation for Greek civil registry purposes. The Greek Embassy in Rabat "
        "handles consular matters. Morocco to Greece is part of the broader South-North "
        "Mediterranean migration pattern."
    ),
    # R37: Austria wave 2
    ('pakistan', 'austria'): (
        "Pakistani nationals form a significant community in Austria, concentrated in Vienna "
        "and Graz, with families working in trade, catering, and professional services. "
        "Pakistan and Austria have bilateral diplomatic ties. Urdu and Punjabi documentation "
        "from Pakistan requires certified German translation for Austrian Standesamt purposes. "
        "The Austrian Embassy in Islamabad handles consular matters. Pakistan to Austria is "
        "an established South Asian diaspora corridor. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    ('ukraine', 'austria'): (
        "Ukrainian nationals form a significant community in Austria, with long-standing "
        "labour migration ties and a substantial increase in arrivals following the February "
        "2022 Russian invasion. Austria received a significant number of Ukrainian refugees "
        "during 2022 and 2023, adding to the existing Ukrainian professional community in "
        "Vienna and other cities. Ukrainian documentation requires certified German translation "
        "where required by Austrian registry authorities. The Austrian Embassy in Kyiv handles "
        "consular matters."
    ),
    ('afghanistan', 'austria'): (
        "Afghan nationals form a significant refugee and asylum community in Austria, with "
        "many arriving during the 2015-2016 migration period and following the August 2021 "
        "Taliban takeover. Austria has accepted Afghan humanitarian cases over two decades. "
        "The Austrian Embassy in Islamabad covers consular matters for Afghanistan following "
        "the suspension of operations in Kabul in August 2021. Afghan documentation requires "
        "certified German translation for Austrian Standesamt purposes. Specialist support is "
        "recommended given documentation complexity from conflict-affected civil registration. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    ('egypt', 'austria'): (
        "Egyptian nationals form part of Austria's Middle Eastern and North African community, "
        "with professionals and academics in Vienna. Austria hosts the International Atomic "
        "Energy Agency (IAEA) and other international organisations in Vienna, attracting "
        "Egyptian professionals and diplomats. Arabic documentation from Egypt requires "
        "certified German translation for Austrian Standesamt purposes. The Austrian Embassy "
        "in Cairo handles consular matters."
    ),
    ('morocco', 'austria'): (
        "Moroccan nationals form part of Austria's North African diaspora, with communities "
        "in Vienna working in trade, hospitality, and service sectors. Morocco and Austria "
        "have bilateral diplomatic ties. Arabic and Darija documentation from Morocco requires "
        "certified German translation for Austrian registry purposes. The Austrian Embassy "
        "in Rabat handles consular matters. Morocco to Austria is part of the broader "
        "Maghreb-to-Central-Europe corridor. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    # R37: Denmark wave 2
    ('afghanistan', 'denmark'): (
        "Afghan nationals form a significant refugee and asylum community in Denmark, with "
        "many arriving during the 2015-2016 migration period and following the August 2021 "
        "Taliban takeover. Denmark has accepted Afghan humanitarian cases, and the Afghan "
        "diaspora in Denmark is now multi-generational in some communities. The Danish "
        "Embassy in Islamabad covers consular matters for Afghanistan. Afghan documentation "
        "requires certified Danish translation. Specialist support is recommended given "
        "documentation complexity from conflict-affected civil registration. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('india', 'denmark'): (
        "Indian nationals form a growing professional and student community in Denmark, "
        "working in technology, pharmaceuticals, and academic sectors. The Danish "
        "pharmaceutical and life-sciences industry, including Novo Nordisk and Lundbeck, "
        "has attracted Indian professionals to Copenhagen and the greater Copenhagen region. "
        "Hindi and English documentation from India may require certified Danish translation "
        "for Danish civil registry purposes. The Danish Embassy in New Delhi handles consular "
        "matters."
    ),
    ('vietnam', 'denmark'): (
        "Vietnamese nationals form a community in Denmark, with many families having arrived "
        "as Vietnamese refugees from the late 1970s onward and subsequent generations building "
        "an established Vietnamese-Danish diaspora. Danish Refugee Council history includes "
        "resettlement of Vietnamese refugees from that period. Vietnamese documentation "
        "requires certified Danish translation for Danish civil registry purposes. The Danish "
        "Embassy in Hanoi handles consular matters. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('morocco', 'denmark'): (
        "Moroccan nationals form a significant North African Muslim community in Denmark, with "
        "families who came as labour migrants from the 1960s and 1970s, creating an "
        "established multi-generational diaspora. Moroccan communities are present in "
        "Copenhagen, Aarhus, and Odense. Arabic and Darija documentation from Morocco requires "
        "certified Danish translation for Danish civil registry purposes. The Danish Embassy "
        "in Rabat handles consular matters."
    ),
    ('nigeria', 'denmark'): (
        "Nigerian nationals form part of Denmark's African community, with professionals and "
        "students in Copenhagen working across multiple sectors. Nigeria and Denmark have "
        "bilateral diplomatic ties. English documentation from Nigeria may still require "
        "certified Danish translation for Danish civil registry purposes. The Danish Embassy "
        "in Abuja handles consular matters. Nigeria to Denmark is a growing corridor for "
        "skilled professional and student migration. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    # R37: Finland wave 2
    ('afghanistan', 'finland'): (
        "Afghan nationals form a significant refugee and asylum community in Finland, with "
        "many arriving during the 2015-2016 migration period. Finland accepted Afghan "
        "humanitarian cases over several years. The Finnish Embassy in Islamabad covers "
        "consular matters for Afghanistan following the suspension of Finnish Embassy "
        "operations in Kabul after August 2021. Afghan documentation requires certified "
        "Finnish translation. Specialist support is recommended given documentation "
        "complexity from conflict-affected civil registration. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('vietnam', 'finland'): (
        "Vietnamese nationals form a community in Finland, concentrated in Helsinki and "
        "Tampere, having arrived through trade and labour migration channels since Finland "
        "established diplomatic ties with Vietnam. Vietnamese documentation requires certified "
        "Finnish translation for Finnish Digi- ja vaestotietovirasto (DVV) registry purposes. "
        "The Finnish Embassy in Hanoi handles consular matters. Vietnam to Finland is a "
        "consistent diaspora corridor."
    ),
    ('ethiopia', 'finland'): (
        "Ethiopian nationals form part of Finland's East African diaspora, concentrated in "
        "Helsinki and Turku, with many having arrived through asylum and humanitarian "
        "channels over two decades. Finland and Ethiopia have diplomatic ties. Amharic "
        "documentation from Ethiopia requires certified Finnish translation for Finnish "
        "registry authorities. The Finnish Embassy in Addis Ababa handles consular matters. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('kenya', 'finland'): (
        "Kenyan nationals form part of Finland's sub-Saharan African community, with "
        "professionals working in Helsinki and other cities. Finland and Kenya have "
        "diplomatic ties, and UN Environment Programme (UNEP) connections through Nairobi "
        "have created professional links between the two countries. Swahili and English "
        "documentation from Kenya may require certified Finnish translation. The Finnish "
        "Embassy in Nairobi handles consular matters."
    ),
    ('china', 'finland'): (
        "Chinese nationals form part of Finland's East Asian community, with professionals "
        "and students in Helsinki and Espoo, attracted by the Finnish technology industry. "
        "Finland and China have bilateral trade ties, and Finnish companies have operated "
        "in China for decades. Chinese documentation in Mandarin requires certified Finnish "
        "translation for Finnish registry purposes. The Finnish Embassy in Beijing handles "
        "consular matters. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    # R37: New Zealand wave 3
    ('nepal', 'new-zealand'): (
        "Nepali nationals form a growing community in New Zealand, with students, skilled "
        "workers, and families settling particularly in Auckland and Christchurch. Nepal and "
        "New Zealand have bilateral ties, and Nepali students have become a significant "
        "proportion of New Zealand's international student population in recent years. "
        "Nepali documentation requires certified English translation where needed for New "
        "Zealand Customs clearance. The New Zealand Embassy in Kathmandu handles consular "
        "matters. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    ('bangladesh', 'new-zealand'): (
        "Bangladeshi nationals form a growing diaspora in New Zealand, with families working "
        "in professional, trade, and service sectors, particularly in Auckland. Bangladesh "
        "and New Zealand have bilateral diplomatic ties. Bengali documentation requires "
        "certified English translation for New Zealand Customs clearance. The New Zealand "
        "High Commission covers Bangladesh from New Delhi. Specialist coordination is "
        "recommended to confirm documentation requirements. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    ('kenya', 'new-zealand'): (
        "Kenyan nationals form part of New Zealand's African diaspora, working in healthcare, "
        "technology, and professional sectors, with communities in Auckland and Wellington. "
        "New Zealand and Kenya share Commonwealth ties and have bilateral diplomatic "
        "relations. English documentation from Kenya is well understood by New Zealand "
        "authorities. The New Zealand High Commission in Nairobi handles consular matters. "
        "Kenya to New Zealand is a consistent skilled worker migration corridor."
    ),
    ('nigeria', 'new-zealand'): (
        "Nigerian nationals form part of New Zealand's West African diaspora, with "
        "professionals and students in Auckland and other cities. Nigeria and New Zealand "
        "share Commonwealth ties. English documentation from Nigeria is well understood "
        "by New Zealand authorities. The New Zealand High Commission in Abuja handles "
        "consular matters. Nigeria to New Zealand is a growing corridor for skilled "
        "professional migration. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    ('sri-lanka', 'new-zealand'): (
        "Sri Lankan nationals form a community in New Zealand, particularly in Auckland, "
        "with families working in professional, healthcare, and trade sectors. Sri Lanka "
        "and New Zealand share Commonwealth ties, and Sri Lankan migration to New Zealand "
        "has included both skilled worker and humanitarian channels. Sinhala and Tamil "
        "documentation requires certified English translation for New Zealand Customs "
        "clearance. The New Zealand High Commission covers Sri Lanka from New Delhi. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    # R38: Japan wave 3
    ('iran', 'japan'): (
        "Iranian nationals form a professional and student community in Japan, concentrated "
        "in Tokyo and other major cities. Japan and Iran have maintained diplomatic relations "
        "and bilateral trade ties, including historical energy trade. Farsi documentation "
        "requires certified Japanese translation for Japanese municipal koseki (family "
        "register) purposes. The Japanese Embassy in Tehran handles consular matters. Iran "
        "to Japan is a specialist corridor where the Japanese funeral director can advise "
        "on health and customs clearance requirements. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    ('pakistan', 'japan'): (
        "Pakistani nationals form a growing community in Japan, working in IT, engineering, "
        "trade, and service sectors in Tokyo and Osaka. Pakistan and Japan have bilateral "
        "trade and diplomatic ties. Japan has expanded its Specified Skilled Worker visa "
        "programme, creating a growing Pakistan to Japan migration corridor. Urdu and Punjabi "
        "documentation from Pakistan requires certified Japanese translation for municipal "
        "registry purposes. The Japanese Embassy in Islamabad handles consular matters."
    ),
    ('hong-kong', 'japan'): (
        "Hong Kong nationals form a significant community in Japan, with many choosing Japan "
        "for study, business, and residence. Japan and Hong Kong have extensive economic and "
        "cultural ties, and Japanese tourism is one of Hong Kong's largest outbound markets. "
        "The number of Hong Kong residents in Japan has grown notably since 2020. Traditional "
        "Chinese documentation from Hong Kong requires certified Japanese translation for "
        "Japanese municipal registry purposes. The Japanese Consulate-General in Hong Kong "
        "handles consular matters. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    ('sri-lanka', 'japan'): (
        "Sri Lankan nationals form a growing community in Japan, working in hospitality, "
        "food service, construction, and professional sectors. Japan has expanded its "
        "Specified Skilled Worker scheme to include Sri Lankan workers in priority "
        "industries. Sinhala and Tamil documentation requires certified Japanese translation "
        "for municipal koseki purposes. The Japanese Embassy in Colombo handles consular "
        "matters. Sri Lanka to Japan is a consistent labour migration corridor that has "
        "expanded in recent years."
    ),
    ('laos', 'japan'): (
        "Lao nationals form a small but established community in Japan, with students and "
        "skilled workers in Tokyo and other cities. Japan is a significant source of official "
        "development assistance for Laos, and the resulting bilateral ties support "
        "a consistent repatriation corridor. Lao documentation requires certified Japanese "
        "translation for municipal registry purposes. The Japanese Embassy in Vientiane "
        "handles consular matters. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    # R38: Greece wave 3
    ('ukraine', 'greece'): (
        "Ukrainian nationals form a growing community in Greece, with a substantial influx "
        "of refugees following the February 2022 Russian invasion of Ukraine. Greece hosted "
        "a significant number of Ukrainian refugees, and Ukrainian labour migration to "
        "Greece in agriculture and services predates 2022. Ukrainian documentation requires "
        "certified Greek translation for Greek civil registry purposes. The Greek Embassy "
        "in Kyiv handles consular matters. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('germany', 'greece'): (
        "German nationals form a significant tourism and retirement community in Greece, with "
        "many German residents on the Greek islands and mainland. Germany and Greece are EU "
        "partners, and EU freedom of movement applies to both countries. This corridor covers "
        "German nationals who die in Greece while working, retiring, or visiting. German "
        "documentation may be accepted in the original language for some EU-standard Greek "
        "procedures, but certified Greek translation may be required for the Lixiarcheio. "
        "The Greek Embassy in Berlin handles consular matters."
    ),
    ('russia', 'greece'): (
        "Russian nationals have formed a significant community in Greece, with property, "
        "business, and Orthodox Christian ties creating longstanding residency patterns. "
        "Greece and Russia share Orthodox Christian heritage and historical ties. Russian "
        "documentation in Cyrillic script requires certified Greek translation for the Greek "
        "Lixiarcheio (civil registry). The Greek Embassy in Moscow handles consular matters. "
        "Since 2022 the diplomatic context has become more complex; specialist support is "
        "recommended. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('china', 'greece'): (
        "Chinese nationals form a business and student community in Greece, with a particular "
        "presence in Athens and the Greek islands. China and Greece have bilateral trade ties, "
        "and the COSCO Shipping investment in Piraeus port created a significant Chinese "
        "business presence in the greater Athens region. Chinese documentation in Mandarin "
        "requires certified Greek translation for Greek registry purposes. The Greek Embassy "
        "in Beijing handles consular matters. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('philippines', 'greece'): (
        "Filipino nationals form a community in Greece, working in domestic service, "
        "healthcare, and hospitality sectors in Athens. Greece has recruited Filipino workers "
        "through bilateral labour agreements in recent years. Filipino documentation, primarily "
        "in English and Filipino, requires certified Greek translation for Greek Lixiarcheio "
        "purposes. The Greek Embassy in Manila handles consular matters."
    ),
    # R38: Austria wave 3
    ('nigeria', 'austria'): (
        "Nigerian nationals form part of Austria's African diaspora, with professionals and "
        "students in Vienna and Graz. Austria hosts significant international organisations "
        "in Vienna including the UN Industrial Development Organisation (UNIDO) and OPEC, "
        "attracting African professionals and diplomats. English documentation from Nigeria "
        "requires certified German translation for Austrian Standesamt purposes. The Austrian "
        "Embassy in Abuja handles consular matters. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    ('philippines', 'austria'): (
        "Filipino nationals form part of Austria's South-East Asian diaspora, working in "
        "healthcare, domestic service, and professional sectors, particularly in Vienna. "
        "Austria has recruited Filipino healthcare workers to address staffing needs. Filipino "
        "documentation requires certified German translation for Austrian Standesamt purposes. "
        "The Austrian Embassy in Manila handles consular matters."
    ),
    ('russia', 'austria'): (
        "Russian nationals have formed a significant business and investor community in "
        "Austria, with Vienna traditionally serving as a meeting point between East and West. "
        "Austria hosts the Organisation for Security and Co-operation in Europe (OSCE) and "
        "the International Atomic Energy Agency (IAEA) in Vienna. Russian documentation in "
        "Cyrillic script requires certified German translation for Austrian Standesamt "
        "purposes. The Austrian Embassy in Moscow handles consular matters. Since 2022 "
        "the diplomatic context has changed; specialist support is recommended. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    ('iran', 'austria'): (
        "Iranian nationals form a professional and student community in Austria, with Vienna "
        "hosting significant Iranian diplomatic and commercial activity. Austria and Iran have "
        "maintained diplomatic relations, and Vienna hosted the Iran nuclear deal (JCPOA) "
        "negotiations under the IAEA framework. Farsi documentation requires certified German "
        "translation for Austrian Standesamt purposes. The Austrian Embassy in Tehran handles "
        "consular matters."
    ),
    ('bosnia-and-herzegovina', 'austria'): (
        "Bosnian nationals form one of Austria's largest former-Yugoslav immigrant communities, "
        "with a significant resident population concentrated in Vienna and other cities, many "
        "having arrived as refugees during and after the 1992-1995 Bosnian War. Austria "
        "accepted large numbers of Bosnian refugees, and the community is now multi-"
        "generational. Bosnian documentation requires certified German translation where "
        "required by Austrian Standesamt authorities. The Austrian Embassy in Sarajevo handles "
        "consular matters. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    # R38: Denmark wave 3
    ('iran', 'denmark'): (
        "Iranian nationals form a significant community in Denmark, with many having arrived "
        "following the 1979 Islamic Revolution, the Iran-Iraq War, and subsequent political "
        "migration over four decades. Iran to Denmark is an established corridor for a "
        "multi-generational diaspora. Farsi documentation requires certified Danish translation "
        "for Danish civil registry purposes. The Danish Embassy in Tehran handles consular "
        "matters. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('sri-lanka', 'denmark'): (
        "Sri Lankan nationals form a significant Tamil diaspora community in Denmark, one "
        "of Scandinavia's largest Tamil populations, with many having arrived as refugees "
        "during the decades-long Sri Lankan civil conflict from 1983 to 2009. Danish Refugee "
        "Council history includes resettlement of Sri Lankan Tamils. Tamil and Sinhala "
        "documentation requires certified Danish translation for Danish civil registry "
        "purposes. The Danish Embassy in Colombo handles consular matters."
    ),
    ('lebanon', 'denmark'): (
        "Lebanese nationals form part of Denmark's Middle Eastern diaspora, with families "
        "who arrived through labour migration and refugee channels during and after the "
        "1975-1990 Lebanese Civil War period and subsequent conflicts. Arabic documentation "
        "from Lebanon requires certified Danish translation for Danish civil registry "
        "purposes. The Danish Embassy in Beirut handles consular matters. Lebanon to Denmark "
        "is a consistent repatriation corridor for a multi-generation diaspora. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('russia', 'denmark'): (
        "Russian nationals form part of Denmark's Eastern European community, with business "
        "and professional ties across the Baltic Sea region. Denmark and Russia have shared "
        "maritime proximity. Russian documentation in Cyrillic script requires certified "
        "Danish translation for Danish civil registry purposes. The Danish Embassy in Moscow "
        "handles consular matters. Since 2022 the bilateral context has changed significantly; "
        "specialist support is recommended."
    ),
    ('ethiopia', 'denmark'): (
        "Ethiopian nationals form part of Denmark's East African diaspora, with professionals "
        "and humanitarian migrants in Copenhagen and other cities. Denmark has development "
        "ties with Ethiopia and has accepted Ethiopian asylum seekers over the years. Amharic "
        "documentation from Ethiopia requires certified Danish translation for Danish civil "
        "registry purposes. The Danish Embassy in Addis Ababa handles consular matters. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    # R38: Finland wave 3
    ('iran', 'finland'): (
        "Iranian nationals form a professional and student community in Finland, having "
        "arrived through academic, professional, and asylum channels over several decades. "
        "Finland and Iran maintain diplomatic relations. Farsi documentation requires "
        "certified Finnish translation for Finnish registry authorities. The Finnish Embassy "
        "in Tehran handles consular matters. Iran to Finland is an established corridor "
        "for settled diaspora. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('pakistan', 'finland'): (
        "Pakistani nationals form a growing community in Finland, working in trade, "
        "hospitality, and technology sectors in Helsinki and Espoo. Finland and Pakistan "
        "have bilateral diplomatic ties. Urdu and Punjabi documentation from Pakistan "
        "requires certified Finnish translation for Finnish DVV registry purposes. The "
        "Finnish Embassy in Islamabad handles consular matters."
    ),
    ('nigeria', 'finland'): (
        "Nigerian nationals form part of Finland's sub-Saharan African community, with "
        "professionals and students in Helsinki. Finland and Nigeria have bilateral "
        "diplomatic ties. English documentation from Nigeria still requires certified "
        "Finnish translation for Finnish DVV registry authorities. The Finnish Embassy "
        "in Abuja handles consular matters. Nigeria to Finland is a growing corridor "
        "for skilled professional and student migration. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('bangladesh', 'finland'): (
        "Bangladeshi nationals form a small but growing community in Finland, working in "
        "professional and service sectors in Helsinki and Espoo. Finland and Bangladesh "
        "have diplomatic ties. Bengali documentation from Bangladesh requires certified "
        "Finnish translation for Finnish registry authorities. The Finnish Embassy in "
        "Dhaka handles consular matters."
    ),
    ('ukraine', 'finland'): (
        "Ukrainian nationals form a significant refugee community in Finland, with Finland "
        "receiving a substantial influx of Ukrainians following the February 2022 Russian "
        "invasion. Finland has been a strong supporter of Ukraine and welcomed Ukrainian "
        "refugees under the Temporary Protection Directive. Ukrainian documentation requires "
        "certified Finnish translation for Finnish DVV registry purposes. The Finnish Embassy "
        "in Kyiv handles consular matters. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
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
# Route list: R37 (25) + R38 (25) = 50 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R37: Greece wave 2 x5 + Austria wave 2 x5 + Denmark wave 2 x5 +
    #     Finland wave 2 x5 + New Zealand wave 3 x5 = 25
    ('egypt',        'greece'),
    ('turkey',       'greece'),
    ('nigeria',      'greece'),
    ('bangladesh',   'greece'),
    ('morocco',      'greece'),
    ('pakistan',     'austria'),
    ('ukraine',      'austria'),
    ('afghanistan',  'austria'),
    ('egypt',        'austria'),
    ('morocco',      'austria'),
    ('afghanistan',  'denmark'),
    ('india',        'denmark'),
    ('vietnam',      'denmark'),
    ('morocco',      'denmark'),
    ('nigeria',      'denmark'),
    ('afghanistan',  'finland'),
    ('vietnam',      'finland'),
    ('ethiopia',     'finland'),
    ('kenya',        'finland'),
    ('china',        'finland'),
    ('nepal',        'new-zealand'),
    ('bangladesh',   'new-zealand'),
    ('kenya',        'new-zealand'),
    ('nigeria',      'new-zealand'),
    ('sri-lanka',    'new-zealand'),
    # --- Block R38: Japan wave 3 x5 + Greece wave 3 x5 + Austria wave 3 x5 +
    #     Denmark wave 3 x5 + Finland wave 3 x5 = 25
    ('iran',         'japan'),
    ('pakistan',     'japan'),
    ('hong-kong',    'japan'),
    ('sri-lanka',    'japan'),
    ('laos',         'japan'),
    ('ukraine',      'greece'),
    ('germany',      'greece'),
    ('russia',       'greece'),
    ('china',        'greece'),
    ('philippines',  'greece'),
    ('nigeria',      'austria'),
    ('philippines',  'austria'),
    ('russia',       'austria'),
    ('iran',         'austria'),
    ('bosnia-and-herzegovina', 'austria'),
    ('iran',         'denmark'),
    ('sri-lanka',    'denmark'),
    ('lebanon',      'denmark'),
    ('russia',       'denmark'),
    ('ethiopia',     'denmark'),
    ('iran',         'finland'),
    ('pakistan',     'finland'),
    ('nigeria',      'finland'),
    ('bangladesh',   'finland'),
    ('ukraine',      'finland'),
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
