#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R35-R36.

   R35: Greece wave 1 x5 + Austria wave 1 x5 + Denmark wave 1 x5 +
        France wave 5 x5 + Germany wave 6 x5 = 25
   R36: Finland wave 1 x5 + UAE wave 5 x5 + Canada wave 5 x5 +
        Australia wave 5 x5 + Belgium wave 5 x5 = 25

   Template rotation: R34 ended on C (index 2). R35 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R34 ended C (index 2); R35 starts D (index 3)

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
    # --- New hubs introduced in R35 ---
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
    # --- New hub introduced in R36 ---
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
    # --- Existing hubs (carried from earlier generators) ---
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
}

# ---------------------------------------------------------------------------
# Embassy cities: destination country's embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R35: Greece wave 1
    ('albania',      'greece'): 'Tirana',
    ('bulgaria',     'greece'): 'Sofia',
    ('romania',      'greece'): 'Bucharest',
    ('pakistan',     'greece'): 'Islamabad',
    ('india',        'greece'): 'New Delhi',
    # R35: Austria wave 1
    ('turkey',       'austria'): 'Ankara',
    ('serbia',       'austria'): 'Belgrade',
    ('romania',      'austria'): 'Bucharest',
    ('india',        'austria'): 'New Delhi',
    ('china',        'austria'): 'Beijing',
    # R35: Denmark wave 1
    ('turkey',       'denmark'): 'Ankara',
    # Danish Embassy covers Somalia from Nairobi
    ('somalia',      'denmark'): 'Nairobi',
    ('poland',       'denmark'): 'Warsaw',
    ('iraq',         'denmark'): 'Baghdad',
    ('pakistan',     'denmark'): 'Islamabad',
    # R35: France wave 5
    ('egypt',        'france'): 'Cairo',
    ('indonesia',    'france'): 'Jakarta',
    ('philippines',  'france'): 'Manila',
    ('eritrea',      'france'): 'Asmara',
    ('angola',       'france'): 'Luanda',
    # R35: Germany wave 6
    ('south-korea',  'germany'): 'Seoul',
    ('georgia',      'germany'): 'Tbilisi',
    ('armenia',      'germany'): 'Yerevan',
    ('azerbaijan',   'germany'): 'Baku',
    ('uzbekistan',   'germany'): 'Tashkent',
    # R36: Finland wave 1
    ('iraq',         'finland'): 'Baghdad',
    # Finnish Embassy covers Somalia from Nairobi
    ('somalia',      'finland'): 'Nairobi',
    ('russia',       'finland'): 'Moscow',
    ('india',        'finland'): 'New Delhi',
    ('turkey',       'finland'): 'Ankara',
    # R36: UAE wave 5
    ('russia',       'united-arab-emirates'): 'Moscow',
    ('uzbekistan',   'united-arab-emirates'): 'Tashkent',
    ('algeria',      'united-arab-emirates'): 'Algiers',
    ('somalia',      'united-arab-emirates'): 'Mogadishu',
    ('angola',       'united-arab-emirates'): 'Luanda',
    # R36: Canada wave 5
    ('turkey',       'canada'): 'Ankara',
    ('russia',       'canada'): 'Moscow',
    ('jordan',       'canada'): 'Amman',
    ('romania',      'canada'): 'Bucharest',
    ('eritrea',      'canada'): 'Asmara',
    # R36: Australia wave 5
    ('iraq',         'australia'): 'Baghdad',
    ('iran',         'australia'): 'Tehran',
    ('turkey',       'australia'): 'Ankara',
    ('egypt',        'australia'): 'Cairo',
    ('jordan',       'australia'): 'Amman',
    # R36: Belgium wave 5
    ('china',        'belgium'): 'Beijing',
    ('indonesia',    'belgium'): 'Jakarta',
    ('philippines',  'belgium'): 'Manila',
    ('brazil',       'belgium'): 'Brasilia',
    ('guinea',       'belgium'): 'Conakry',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R35: Greece wave 1
    ('albania', 'greece'): (
        "Albanian nationals form Greece's largest immigrant community, with over 400,000 "
        "residents working across construction, agriculture, hospitality, and service sectors "
        "throughout mainland Greece and the islands. Albania and Greece share a land border, "
        "and Albanians have migrated to Greece in large numbers since the early 1990s. The "
        "Albanian diaspora in Greece is well established, and the Greece to Albania repatriation "
        "corridor is one of the highest-volume in the region. Albanian documentation requires "
        "certified Greek translation. The Greek Embassy in Tirana handles consular matters. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('bulgaria', 'greece'): (
        "Bulgarian nationals form a significant EU immigrant community in Greece, working "
        "in agriculture, construction, and service sectors. Bulgaria and Greece share a land "
        "border, and EU freedom of movement facilitates labour migration between the two "
        "countries. Bulgarian documentation requires certified Greek translation for Greek "
        "civil registry purposes. The Greek Embassy in Sofia handles consular matters. "
        "This corridor also covers Bulgarian tourists who die in Greece and need repatriation "
        "to Bulgarian cities. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('romania', 'greece'): (
        "Romanian nationals form a significant EU labour migration community in Greece, working "
        "in agriculture, construction, and hospitality. Romania and Greece share EU membership, "
        "and EU freedom of movement applies. Romanian documentation requires certified Greek "
        "translation for Greek civil registry purposes. The Greek Embassy in Bucharest handles "
        "consular matters. Romania to Greece is a consistent seasonal migration corridor, and "
        "a proportion of repatriation cases involve agricultural workers."
    ),
    ('pakistan', 'greece'): (
        "Pakistani nationals form Greece's largest non-EU immigrant community, with over "
        "60,000 residents concentrated in Athens, Patras, and Thessaloniki, working in "
        "agriculture, catering, and trade. Pakistan to Greece is a significant migration "
        "corridor, with Pakistani workers arriving through labour and asylum channels since "
        "the 1990s. Urdu and Punjabi documentation from Pakistan requires certified Greek "
        "translation. The Greek Embassy in Islamabad handles consular matters. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('india', 'greece'): (
        "Indian nationals form a growing professional and business community in Greece, with "
        "traders, students, and skilled workers concentrated in Athens and Thessaloniki. "
        "India and Greece have bilateral ties through trade and tourism. Greek civil registry "
        "authorities require certified Greek translation of foreign documents. The Greek "
        "Embassy in New Delhi handles consular matters. This corridor also covers Indian "
        "tourists who die in Greece, a significant population given Greek tourism volumes."
    ),
    # R35: Austria wave 1
    ('turkey', 'austria'): (
        "Turkish nationals form Austria's largest immigrant community, with over 100,000 "
        "residents whose families came as guest workers from the 1960s onward. Turkish "
        "communities are concentrated in Vienna, Graz, and Linz, working across construction, "
        "trade, hospitality, and professional services. Turkey to Austria is one of the "
        "highest-volume repatriation corridors in the region. Turkish documentation requires "
        "certified German translation for Austrian Standesamt purposes. The Austrian Embassy "
        "in Ankara handles consular matters. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    ('serbia', 'austria'): (
        "Serbian nationals form one of Austria's largest former-Yugoslav immigrant communities, "
        "with over 120,000 residents concentrated in Vienna, working in construction, transport, "
        "and professional services. Austria and Serbia have close historical and economic ties, "
        "and Serbian migration to Austria predates the post-1991 Yugoslav wars. Serbian "
        "documentation requires certified German translation for Austrian Standesamt purposes. "
        "The Austrian Embassy in Belgrade handles consular matters."
    ),
    ('romania', 'austria'): (
        "Romanian nationals form a significant EU labour migration community in Austria, working "
        "in care, construction, healthcare, and service sectors. EU freedom of movement "
        "facilitates Romanian migration to Austria. Romanian documentation requires certified "
        "German translation where required by Austrian registry authorities. The Austrian "
        "Embassy in Bucharest handles consular matters. Romania to Austria is an established "
        "corridor for both settled diaspora and seasonal workers."
    ),
    ('india', 'austria'): (
        "Indian nationals form a growing professional and student community in Austria, "
        "concentrated in Vienna, working in technology, research, and international "
        "organisation sectors. Austria hosts significant UN and IAEA operations in Vienna, "
        "attracting Indian professionals and academics. Hindi and English documentation "
        "from India may require certified German translation for Austrian authorities. "
        "The Austrian Embassy in New Delhi handles consular matters."
    ),
    ('china', 'austria'): (
        "Chinese nationals form part of Austria's East Asian community, with a business, "
        "student, and tourism population concentrated in Vienna. Austria and China have "
        "bilateral trade ties, and Vienna hosts significant Chinese-invested businesses. "
        "Chinese documentation in Mandarin requires certified German translation for "
        "Austrian Standesamt purposes. The Austrian Embassy in Beijing handles consular "
        "matters. This corridor also covers Chinese tourists who die in Austria. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    # R35: Denmark wave 1
    ('turkey', 'denmark'): (
        "Turkish nationals form Denmark's largest non-Western immigrant community, with over "
        "60,000 residents whose families arrived as guest workers from the 1960s and 1970s. "
        "Turkish communities are concentrated in Copenhagen, Aarhus, and Odense, working in "
        "trade, hospitality, and professional services across generations. Turkey to Denmark "
        "is an established and consistent repatriation corridor. Turkish documentation "
        "requires certified Danish translation for Danish civil registry purposes. The Danish "
        "Embassy in Ankara handles consular matters. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('somalia', 'denmark'): (
        "Somali nationals form Denmark's largest African immigrant community, with over "
        "25,000 residents who arrived as refugees from the early 1990s onward, many settling "
        "in Copenhagen, Aarhus, and Odense. Denmark was among the early recipients of Somali "
        "asylum seekers in Scandinavia. The Danish Embassy in Nairobi, Kenya handles consular "
        "matters for Somalia, as there is no resident Danish Embassy in Mogadishu. Somali "
        "documentation requires certified Danish translation. Specialist coordination is "
        "recommended given the added complexity of cross-embassy coverage."
    ),
    ('poland', 'denmark'): (
        "Polish nationals form Denmark's largest EU labour migration community, with over "
        "80,000 residents working in construction, agriculture, logistics, and service "
        "sectors. Poland and Denmark are EU partners, and EU freedom of movement facilitates "
        "labour migration. Polish documentation requires certified Danish translation where "
        "required by Danish civil registry authorities. The Danish Embassy in Warsaw handles "
        "consular matters. Poland to Denmark is a well-established seasonal and permanent "
        "migration corridor."
    ),
    ('iraq', 'denmark'): (
        "Iraqi nationals form a significant community in Denmark, with many families arriving "
        "as refugees and asylum seekers during the 1990s Gulf War period, the 2003 post-"
        "invasion displacement, and the 2014-2015 IS crisis. The Danish Embassy in Baghdad "
        "handles consular matters. Arabic documentation from Iraq requires certified Danish "
        "translation for Danish civil registry purposes. Specialist support is recommended "
        "for Iraq to Denmark repatriation given documentation complexity from conflict-"
        "affected civil registration. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('pakistan', 'denmark'): (
        "Pakistani nationals form a significant Muslim community in Denmark, with families "
        "who came as labour migrants from the 1960s and 1970s establishing an established "
        "two to three generation diaspora. Pakistani communities are concentrated in "
        "Copenhagen and Aarhus. Urdu and Punjabi documentation from Pakistan requires "
        "certified Danish translation for Danish civil registry purposes. The Danish Embassy "
        "in Islamabad handles consular matters. Pakistan to Denmark is an established "
        "repatriation corridor for both settled diaspora and Pakistani workers."
    ),
    # R35: France wave 5
    ('egypt', 'france'): (
        "Egyptian nationals form a significant community in France, concentrated in Paris "
        "and Lyon, with over 80,000 residents working in business, academia, and professional "
        "services. France and Egypt have close historical and cultural ties, including "
        "France's role in the 19th century Egyptian modernisation period and the French "
        "language's longstanding presence in Egyptian education. Arabic documentation from "
        "Egypt requires certified French translation for French registry purposes. The French "
        "Embassy in Cairo handles consular matters. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    ('indonesia', 'france'): (
        "Indonesian nationals form a growing community in France, with students, professionals, "
        "and cultural exchange participants in Paris and other French cities. France and "
        "Indonesia have bilateral trade and cultural ties. Indonesian documentation requires "
        "certified French translation for French prefecture and registry purposes. The French "
        "Embassy in Jakarta handles consular matters. This corridor also covers Indonesian "
        "tourists and business travellers who die in France."
    ),
    ('philippines', 'france'): (
        "Filipino nationals form part of France's South-East Asian diaspora, working in "
        "domestic service, healthcare, and professional sectors, concentrated in Paris. "
        "The Philippines and France have bilateral ties through trade and diplomatic "
        "relations. Filipino documentation, primarily in English and Filipino, requires "
        "certified French translation for French registry and prefecture purposes. The French "
        "Embassy in Manila handles consular matters. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    ('eritrea', 'france'): (
        "Eritrean nationals form a significant refugee and asylum community in France, with "
        "many having arrived during the 1990s post-independence period and the 2010s as part "
        "of wider East African migration. France has received Eritrean asylum seekers through "
        "the OFPRA (French Office for the Protection of Refugees and Stateless Persons) "
        "process. Tigrinya documentation from Eritrea requires certified French translation. "
        "The French Embassy in Asmara handles consular matters."
    ),
    ('angola', 'france'): (
        "Angolan nationals form part of France's Lusophone and African diaspora, with a "
        "community in Paris connected through French and Portuguese-speaking African networks. "
        "Angola and France have diplomatic and economic ties. Portuguese documentation from "
        "Angola requires certified French translation for French prefecture and registry "
        "authorities. The French Embassy in Luanda handles consular matters. Angola to France "
        "is a growing corridor reflecting Angolan migration to continental Europe. "
        "(French Ministry of Europe and Foreign Affairs, MAE, 2025.)"
    ),
    # R35: Germany wave 6
    ('south-korea', 'germany'): (
        "South Korean nationals form a significant professional and student community in "
        "Germany, working in technology, automotive, electronics, and academic sectors. "
        "Germany and South Korea have strong bilateral trade ties, with German companies "
        "including Volkswagen and BASF operating in Korea, and Korean companies including "
        "Samsung and LG Electronics having European presences in Germany. Korean documentation "
        "requires certified German translation for Standesamt purposes. The German Embassy "
        "in Seoul handles consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    ('georgia', 'germany'): (
        "Georgian nationals form a growing community in Germany, with many arriving after "
        "Georgia obtained EU visa-free access in 2017. Georgian communities work in trade, "
        "hospitality, and professional services in Berlin, Frankfurt, and other German cities. "
        "Germany and Georgia have bilateral ties through the EU association agreement and "
        "significant German investment in Georgia's economy. Georgian documentation requires "
        "certified German translation. The German Embassy in Tbilisi handles consular matters."
    ),
    ('armenia', 'germany'): (
        "Armenian nationals form a significant diaspora in Germany, concentrated in Munich, "
        "Stuttgart, and Cologne, with many having arrived following the Soviet collapse and "
        "subsequent Nagorno-Karabakh conflicts. Germany and Armenia have bilateral ties "
        "through the EU-Armenia Enhanced Partnership Agreement. Armenian "
        "documentation in Armenian script requires certified German translation. The German "
        "Embassy in Yerevan handles consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    ('azerbaijan', 'germany'): (
        "Azerbaijani nationals form a growing professional and student community in Germany, "
        "working in business, energy, and academic sectors. Germany and Azerbaijan have "
        "energy ties through the Southern Gas Corridor, which carries Azerbaijani gas to "
        "European markets including Germany. Azerbaijani documentation requires certified "
        "German translation for Standesamt purposes. The German Embassy in Baku handles "
        "consular matters."
    ),
    ('uzbekistan', 'germany'): (
        "Uzbek nationals form a growing community in Germany, with student and skilled "
        "worker migration channels expanding as Uzbekistan has pursued economic liberalisation "
        "since 2016. German companies have invested in Uzbekistan's manufacturing and energy "
        "sectors. Uzbek documentation in Cyrillic script requires certified German translation "
        "for Standesamt purposes. The German Embassy in Tashkent handles consular matters. "
        "(German Federal Foreign Office, Auswaertiges Amt, 2025.)"
    ),
    # R36: Finland wave 1
    ('iraq', 'finland'): (
        "Iraqi nationals form Finland's largest Middle Eastern immigrant community, with many "
        "families arriving as refugees following the 1990s Gulf War period, the 2003 post-"
        "invasion displacement, and the 2014-2015 IS crisis. Finland accepted significant "
        "numbers of Iraqi asylum seekers, particularly between 2014 and 2016. Arabic "
        "documentation from Iraq requires certified Finnish translation for Finnish registry "
        "authorities. The Finnish Embassy in Baghdad handles consular matters. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('somalia', 'finland'): (
        "Somali nationals form Finland's largest African immigrant community, with over "
        "20,000 residents concentrated in Helsinki, Turku, and Tampere, many having arrived "
        "as refugees from the 1990s onward. Finland was among the first Scandinavian "
        "countries to accept Somali refugees in significant numbers, and has an established "
        "Somali-Finnish community spanning two generations. The Finnish Embassy in Nairobi "
        "handles consular matters for Somalia. Somali documentation requires certified "
        "Finnish translation. Specialist coordination is recommended."
    ),
    ('russia', 'finland'): (
        "Russian nationals form a significant community in Finland, with historical ties "
        "through geography and Finland's period as a Russian Grand Duchy until 1917. Finland "
        "and Russia share a long land border. Russian communities work in business and trade "
        "in Helsinki and eastern Finland. Russian documentation requires certified Finnish "
        "translation for Finnish registry authorities. The Finnish Embassy in Moscow handles "
        "consular matters. Since 2022 the diplomatic context has changed significantly; "
        "specialist support is recommended. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('india', 'finland'): (
        "Indian nationals form a growing professional and student community in Finland, "
        "particularly in technology, engineering, and research sectors. Nokia, Finnish "
        "universities, and the Finnish technology industry have attracted Indian professionals "
        "and students to Helsinki, Tampere, and Espoo. Hindi and English documentation from "
        "India may require certified Finnish translation for Finnish registry authorities. "
        "The Finnish Embassy in New Delhi handles consular matters."
    ),
    ('turkey', 'finland'): (
        "Turkish nationals form part of Finland's immigrant community, working in service, "
        "trade, and business sectors in Helsinki and other cities. Finland and Turkey share "
        "NATO membership, with Finland joining the alliance in April 2023. Turkish "
        "documentation requires certified Finnish translation for Finnish registry purposes. "
        "The Finnish Embassy in Ankara handles consular matters. Turkey to Finland is a "
        "growing corridor as bilateral ties have deepened through the NATO framework. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    # R36: UAE wave 5
    ('russia', 'united-arab-emirates'): (
        "Russian nationals form a significant community in the UAE, concentrated in Dubai, "
        "working in business, real estate, finance, and professional services. Russian "
        "investment in UAE property expanded considerably from 2022 onward. The UAE Embassy "
        "in Moscow handles document attestation. Russian documentation in Cyrillic script "
        "requires certified Arabic or English translation for UAE authorities. Specialist "
        "support is recommended given the changed diplomatic context. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    ('uzbekistan', 'united-arab-emirates'): (
        "Uzbek nationals form a growing labour migration community in the UAE, working in "
        "construction, hospitality, and service sectors under GCC employment visa schemes. "
        "UAE and Uzbekistan have bilateral labour agreements, and Uzbekistan is among the "
        "Central Asian countries sending workers to the Gulf. The UAE Embassy in Tashkent "
        "handles document attestation. Uzbek documentation requires certified Arabic "
        "translation for UAE authorities."
    ),
    ('algeria', 'united-arab-emirates'): (
        "Algerian nationals work in the UAE in professional, technology, and business sectors, "
        "with a community in Dubai and Abu Dhabi. UAE and Algeria have bilateral ties through "
        "the Arab League and Organisation of Islamic Cooperation frameworks. Arabic "
        "documentation from Algeria is well understood by UAE authorities, which can simplify "
        "some administrative steps. The UAE Embassy in Algiers handles document attestation. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    ('somalia', 'united-arab-emirates'): (
        "Somali nationals form a diaspora community in the UAE, concentrated in Dubai's "
        "established Somali quarter in Deira. UAE has hosted Somali traders, business "
        "families, and professionals for decades, creating well-established community and "
        "commercial networks. The UAE Embassy in Mogadishu handles document attestation. "
        "Somali documentation requires certified Arabic translation for UAE Ministry of "
        "Health clearance purposes."
    ),
    ('angola', 'united-arab-emirates'): (
        "Angolan nationals work in the UAE in oil and gas, construction, and business "
        "sectors, driven by Angola's ties with UAE energy companies and Gulf investment. "
        "The UAE and Angola have bilateral economic ties through their shared status as "
        "major oil producers. Portuguese documentation from Angola requires certified Arabic "
        "translation for UAE authorities. The UAE Embassy in Luanda handles document "
        "attestation. "
        "(UAE Ministry of Foreign Affairs and International Cooperation, MOFAIC, 2025.)"
    ),
    # R36: Canada wave 5
    ('turkey', 'canada'): (
        "Turkish nationals form a growing community in Canada, with communities in Toronto, "
        "Montreal, and Vancouver working in professional, trade, and service sectors. Canada "
        "and Turkey are both NATO members and have bilateral trade ties. Turkish documentation "
        "requires certified English or French translation for Canadian Border Services Agency "
        "clearance. The Canadian Embassy in Ankara handles consular matters. Turkey to Canada "
        "is an established corridor for both settled diaspora and skilled worker migration. "
        "(Global Affairs Canada, 2025.)"
    ),
    ('russia', 'canada'): (
        "Russian nationals form a significant community in Canada, particularly in Toronto, "
        "Vancouver, and Montreal, including a longstanding Russian-Canadian diaspora going "
        "back to early 20th century emigration and more recent arrivals after 2022. Russian "
        "documentation in Cyrillic script requires certified English or French translation "
        "for CBSA clearance. The Canadian Embassy in Moscow handles consular matters. "
        "Specialist support is recommended given the changed diplomatic context. "
        "(Global Affairs Canada, 2025.)"
    ),
    ('jordan', 'canada'): (
        "Jordanian nationals form part of Canada's Arab diaspora, working in professional, "
        "academic, and business sectors in Toronto and other cities. Canada and Jordan have "
        "bilateral ties, and Canada has accepted Jordanian and Jordanian-Palestinian migrants "
        "through family reunification and skilled worker channels over several decades. "
        "Arabic documentation from Jordan requires certified English or French translation "
        "for CBSA clearance. The Canadian Embassy in Amman handles consular matters."
    ),
    ('romania', 'canada'): (
        "Romanian nationals form a significant Eastern European community in Canada, "
        "particularly in Ontario and British Columbia, working in professional, trade, "
        "and service sectors. Canada and Romania have bilateral ties through NATO and "
        "Canadian investment in Romania. Romanian documentation requires certified English "
        "or French translation for CBSA clearance. The Canadian Embassy in Bucharest handles "
        "consular matters. Romania to Canada is a consistent skilled migration corridor. "
        "(Global Affairs Canada, 2025.)"
    ),
    ('eritrea', 'canada'): (
        "Eritrean nationals form a significant diaspora in Canada, concentrated in Toronto, "
        "with many having arrived as refugees following the 1991 post-independence conflicts "
        "and the 1998-2000 Eritrea-Ethiopia war. Canada has accepted Eritrean asylum seekers "
        "over two decades, creating an established community. Tigrinya documentation from "
        "Eritrea requires certified English or French translation for CBSA clearance. "
        "The Canadian Embassy in Asmara handles consular matters."
    ),
    # R36: Australia wave 5
    ('iraq', 'australia'): (
        "Iraqi nationals form a significant community in Australia, with many families "
        "arriving as refugees following the 1990 Gulf War, the 2003 invasion, and the "
        "2014-2015 IS crisis. Australia has accepted large numbers of Iraqi asylum seekers "
        "and humanitarian entrants over three decades. Chaldean and other Christian Iraqi "
        "communities are particularly established in Sydney and Melbourne. Arabic documentation "
        "from Iraq requires certified English translation for Australian Border Force clearance. "
        "The Australian Embassy in Baghdad handles consular matters. "
        "(Australian Government, DFAT, 2025.)"
    ),
    ('iran', 'australia'): (
        "Iranian nationals form a significant community in Australia, concentrated in "
        "Melbourne and Sydney, working in professional, academic, and business sectors. Many "
        "arrived as students and asylum seekers from the late 1980s onward. Iran and Australia "
        "do not have an extradition treaty, but consular cooperation on repatriation of "
        "remains is available through each country's embassy. Farsi documentation requires "
        "certified English translation for Australian Border Force clearance. The Australian "
        "Embassy in Tehran handles consular matters. "
        "(Australian Government, DFAT, 2025.)"
    ),
    ('turkey', 'australia'): (
        "Turkish nationals form a long-established community in Australia, with many families "
        "having arrived as labour migrants from the 1960s and 1970s under bilateral agreements. "
        "Turkish-Australian communities are concentrated in Melbourne and Sydney and span "
        "multiple generations. This corridor also handles deaths of Australian tourists in "
        "Turkey, a significant volume given Turkey's popularity as a tourist destination. "
        "Turkish documentation requires certified English translation for Australian Border "
        "Force clearance. The Australian Embassy in Ankara handles consular matters."
    ),
    ('egypt', 'australia'): (
        "Egyptian nationals form part of Australia's Middle Eastern and Coptic Christian "
        "diaspora, with established communities in Sydney and Melbourne. Egypt and Australia "
        "have bilateral diplomatic ties. Arabic and Coptic documentation from Egypt requires "
        "certified English translation for Australian Border Force clearance. The Australian "
        "Embassy in Cairo handles consular matters. This corridor also covers Egyptian-"
        "Australians who die in Egypt while visiting family. "
        "(Australian Government, DFAT, 2025.)"
    ),
    ('jordan', 'australia'): (
        "Jordanian nationals form part of Australia's Arab diaspora, including Palestinian-"
        "Jordanian communities in Sydney and Melbourne. Australia and Jordan have bilateral "
        "diplomatic ties, and Australia has accepted Jordanian migrants through family and "
        "skilled worker channels. Arabic documentation from Jordan requires certified English "
        "translation for Australian Border Force clearance. The Australian Embassy in Amman "
        "handles consular matters."
    ),
    # R36: Belgium wave 5
    ('china', 'belgium'): (
        "Chinese nationals form a significant community in Belgium, particularly in Antwerp, "
        "which hosts one of Europe's oldest Chinese communities dating to the 1930s, and in "
        "Brussels where Chinese business ties to EU institutions are long-established. Belgian "
        "and Chinese bilateral trade ties have grown significantly in recent decades. Chinese "
        "documentation in Mandarin requires certified French or Dutch translation for Belgian "
        "civil registry purposes. The Belgian Embassy in Beijing handles consular matters. "
        "(Belgian Federal Public Service Foreign Affairs, FPS Foreign Affairs, 2025.)"
    ),
    ('indonesia', 'belgium'): (
        "Indonesian nationals form a growing community in Belgium, particularly in Brussels, "
        "working in EU institutions, professional services, and academic roles. Belgium and "
        "Indonesia have bilateral trade and diplomatic ties. Indonesian documentation requires "
        "certified French or Dutch translation for Belgian commune or gemeente registration. "
        "The Belgian Embassy in Jakarta handles consular matters. This corridor also covers "
        "Indonesian tourists and business travellers who die in Belgium."
    ),
    ('philippines', 'belgium'): (
        "Filipino nationals form part of Belgium's South-East Asian diaspora, working in "
        "healthcare, domestic service, and professional sectors in Brussels and other "
        "Belgian cities. Belgium and the Philippines have bilateral diplomatic ties. Filipino "
        "documentation, primarily in English and Filipino, may simplify some requirements "
        "for Belgian authorities. The Belgian Embassy in Manila handles consular matters. "
        "(Belgian Federal Public Service Foreign Affairs, FPS Foreign Affairs, 2025.)"
    ),
    ('brazil', 'belgium'): (
        "Brazilian nationals form part of Belgium's South American diaspora, concentrated "
        "in Brussels and Antwerp, working in EU institutions, business, and professional "
        "services. Belgium and Brazil have bilateral diplomatic ties through EU-Mercosur "
        "relations. Brazilian documentation in Portuguese requires certified French or Dutch "
        "translation for Belgian civil registry authorities. The Belgian Embassy in Brasilia "
        "handles consular matters."
    ),
    ('guinea', 'belgium'): (
        "Guinean nationals form part of Belgium's West African francophone diaspora. "
        "Belgium and Guinea share Francophone connections, and Guinean migrants often "
        "travel between France and Belgium. French documentation from Guinea is accepted "
        "in francophone Belgium, though Flemish registry authorities may require certified "
        "Dutch translation. The Belgian Embassy in Conakry handles consular matters. "
        "(Belgian Federal Public Service Foreign Affairs, FPS Foreign Affairs, 2025.)"
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
# Route list: R35 (25) + R36 (25) = 50 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R35: Greece wave 1 x5 + Austria wave 1 x5 + Denmark wave 1 x5 +
    #     France wave 5 x5 + Germany wave 6 x5 = 25
    ('albania',      'greece'),
    ('bulgaria',     'greece'),
    ('romania',      'greece'),
    ('pakistan',     'greece'),
    ('india',        'greece'),
    ('turkey',       'austria'),
    ('serbia',       'austria'),
    ('romania',      'austria'),
    ('india',        'austria'),
    ('china',        'austria'),
    ('turkey',       'denmark'),
    ('somalia',      'denmark'),
    ('poland',       'denmark'),
    ('iraq',         'denmark'),
    ('pakistan',     'denmark'),
    ('egypt',        'france'),
    ('indonesia',    'france'),
    ('philippines',  'france'),
    ('eritrea',      'france'),
    ('angola',       'france'),
    ('south-korea',  'germany'),
    ('georgia',      'germany'),
    ('armenia',      'germany'),
    ('azerbaijan',   'germany'),
    ('uzbekistan',   'germany'),
    # --- Block R36: Finland wave 1 x5 + UAE wave 5 x5 + Canada wave 5 x5 +
    #     Australia wave 5 x5 + Belgium wave 5 x5 = 25
    ('iraq',         'finland'),
    ('somalia',      'finland'),
    ('russia',       'finland'),
    ('india',        'finland'),
    ('turkey',       'finland'),
    ('russia',       'united-arab-emirates'),
    ('uzbekistan',   'united-arab-emirates'),
    ('algeria',      'united-arab-emirates'),
    ('somalia',      'united-arab-emirates'),
    ('angola',       'united-arab-emirates'),
    ('turkey',       'canada'),
    ('russia',       'canada'),
    ('jordan',       'canada'),
    ('romania',      'canada'),
    ('eritrea',      'canada'),
    ('iraq',         'australia'),
    ('iran',         'australia'),
    ('turkey',       'australia'),
    ('egypt',        'australia'),
    ('jordan',       'australia'),
    ('china',        'belgium'),
    ('indonesia',    'belgium'),
    ('philippines',  'belgium'),
    ('brazil',       'belgium'),
    ('guinea',       'belgium'),
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
