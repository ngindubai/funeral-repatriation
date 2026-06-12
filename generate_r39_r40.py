#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R39-R40.

   R39: Japan wave 4 x5 + New Zealand wave 4 x5 + Greece wave 4 x5 +
        Austria wave 4 x5 + Denmark wave 4 x5 = 25
   R40: Finland wave 4 x5 + Singapore wave 4 x5 + South Africa wave 4 x5 +
        Saudi Arabia wave 5 x5 + USA wave 5 x5 = 25

   Template rotation: R38 ended on C (index 2). R39 starts at D (index 3).
   Each block of 25 routes cycles D,E,A,B,C x5, ending on C.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

START_VARIANT = 3  # R38 ended C (index 2); R39 starts D (index 3)

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
}

# ---------------------------------------------------------------------------
# Embassy cities: destination country embassy city in the origin country
# ---------------------------------------------------------------------------

EMBASSY_CITIES = {
    # R39: Japan wave 4
    ('usa',           'japan'): 'Washington DC',
    ('australia',     'japan'): 'Canberra',
    ('france',        'japan'): 'Paris',
    ('germany',       'japan'): 'Berlin',
    ('italy',         'japan'): 'Rome',
    # R39: New Zealand wave 4
    ('australia',     'new-zealand'): 'Canberra',
    ('usa',           'new-zealand'): 'Washington DC',
    ('south-africa',  'new-zealand'): 'Pretoria',
    ('canada',        'new-zealand'): 'Ottawa',
    ('hong-kong',     'new-zealand'): 'Hong Kong',
    # R39: Greece wave 4
    ('georgia',       'greece'): 'Tbilisi',
    ('serbia',        'greece'): 'Belgrade',
    ('north-macedonia', 'greece'): 'Skopje',
    ('ethiopia',      'greece'): 'Addis Ababa',
    ('iran',          'greece'): 'Tehran',
    # R39: Austria wave 4
    ('hungary',       'austria'): 'Budapest',
    ('croatia',       'austria'): 'Zagreb',
    ('slovakia',      'austria'): 'Bratislava',
    ('czech-republic', 'austria'): 'Prague',
    ('albania',       'austria'): 'Tirana',
    # R39: Denmark wave 4
    ('china',         'denmark'): 'Beijing',
    ('ghana',         'denmark'): 'Accra',
    ('kenya',         'denmark'): 'Nairobi',
    ('bangladesh',    'denmark'): 'Dhaka',
    # Danish Embassy covers Eritrea from Addis Ababa
    ('eritrea',       'denmark'): 'Addis Ababa',
    # R40: Finland wave 4
    ('ghana',         'finland'): 'Accra',
    # Finnish Embassy covers Eritrea from Addis Ababa
    ('eritrea',       'finland'): 'Addis Ababa',
    ('morocco',       'finland'): 'Rabat',
    ('indonesia',     'finland'): 'Jakarta',
    ('senegal',       'finland'): 'Dakar',
    # R40: Singapore wave 4
    ('australia',     'singapore'): 'Canberra',
    ('usa',           'singapore'): 'Washington DC',
    ('south-africa',  'singapore'): 'Pretoria',
    ('kenya',         'singapore'): 'Nairobi',
    ('nigeria',       'singapore'): 'Abuja',
    # R40: South Africa wave 4
    ('france',        'south-africa'): 'Paris',
    ('usa',           'south-africa'): 'Washington DC',
    ('germany',       'south-africa'): 'Berlin',
    ('australia',     'south-africa'): 'Canberra',
    ('netherlands',   'south-africa'): 'The Hague',
    # R40: Saudi Arabia wave 5
    ('morocco',       'saudi-arabia'): 'Rabat',
    ('ivory-coast',   'saudi-arabia'): 'Abidjan',
    ('burkina-faso',  'saudi-arabia'): 'Ouagadougou',
    ('togo',          'saudi-arabia'): 'Lome',
    ('djibouti',      'saudi-arabia'): 'Djibouti City',
    # R40: USA wave 5
    ('japan',         'united-states'): 'Tokyo',
    ('argentina',     'united-states'): 'Buenos Aires',
    ('south-africa',  'united-states'): 'Pretoria',
    ('georgia',       'united-states'): 'Tbilisi',
    ('tanzania',      'united-states'): 'Dar es Salaam',
}

# ---------------------------------------------------------------------------
# Corridor intro text
# ---------------------------------------------------------------------------

CORRIDOR_INTRO = {
    # R39: Japan wave 4
    ('usa', 'japan'): (
        "Japanese Americans and American nationals of Japanese descent maintain strong "
        "family ties to Japan, making the United States to Japan corridor a consistent "
        "repatriation route. California, Hawaii, and New York have long-established "
        "Japanese American communities. Japan requires MOFA export approval, the Burial "
        "Permit (Maiso Kyoka), and a sanitised coffin certificate before remains can "
        "depart. The Japanese Embassy in Washington DC handles consular matters for "
        "Japanese families affected by a death in the United States. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    ('australia', 'japan'): (
        "Japanese nationals form a community in Australia, with students, working holiday "
        "visa holders, and professionals concentrated in Melbourne, Sydney, and Cairns. "
        "Australia and Japan have close bilateral ties including a Free Trade Agreement "
        "and a Status of Forces Agreement. Australian English documentation requires "
        "certified Japanese translation for Japanese municipal koseki (family register) "
        "purposes. The Japanese Embassy in Canberra handles consular matters."
    ),
    ('france', 'japan'): (
        "Japanese nationals form a community in France, concentrated in Paris and the "
        "greater Paris region, with Paris hosting one of the largest Japanese communities "
        "in Europe. Japan and France share extensive cultural, trade, and diplomatic ties, "
        "including the Japan-EU Economic Partnership Agreement. French documentation "
        "requires certified Japanese translation for Japanese municipal registry purposes. "
        "The Japanese Embassy in Paris handles consular matters. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    ('germany', 'japan'): (
        "Japanese nationals form a significant business community in Germany, concentrated "
        "in Dusseldorf, Frankfurt, and Hamburg. Dusseldorf hosts one of the largest Japanese "
        "communities in Europe, with many Japanese companies operating European headquarters "
        "there. The Japan-Germany economic relationship is longstanding and extensive. "
        "German documentation requires certified Japanese translation for Japanese municipal "
        "registry purposes. The Japanese Embassy in Berlin handles consular matters."
    ),
    ('italy', 'japan'): (
        "Japanese nationals form a tourist and professional community in Italy, with "
        "significant numbers in Rome, Florence, Venice, and Milan. Italy is one of the "
        "top destinations for Japanese tourists worldwide, and Japanese residents working "
        "in Italian fashion, arts, and gastronomy industries have grown in recent years. "
        "Italian documentation requires certified Japanese translation for Japanese "
        "municipal registry purposes. The Japanese Embassy in Rome handles consular "
        "matters. "
        "(Japanese Ministry of Foreign Affairs, MOFA, 2025.)"
    ),
    # R39: New Zealand wave 4
    ('australia', 'new-zealand'): (
        "Australians form the largest foreign national group in New Zealand, with hundreds "
        "of thousands of Australian citizens living and working across the country under "
        "the Trans-Tasman Travel Arrangement, which allows citizens of each country to "
        "live and work in the other. This corridor is one of the highest-volume repatriation "
        "routes between the two countries. English documentation from Australia requires no "
        "translation for New Zealand Customs clearance. The New Zealand High Commission in "
        "Canberra handles consular matters. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    ('usa', 'new-zealand'): (
        "American nationals form a professional and business community in New Zealand, "
        "particularly in Auckland, Wellington, and Queenstown, drawn by lifestyle and "
        "work opportunities. The US and New Zealand share Anglophone ties and bilateral "
        "diplomatic relations. American tourists and expatriates represent a consistent "
        "repatriation corridor. English documentation from the US requires no translation "
        "for New Zealand Customs clearance. The New Zealand Embassy in Washington DC "
        "handles consular matters."
    ),
    ('south-africa', 'new-zealand'): (
        "South African nationals form a significant migrant community in New Zealand, "
        "concentrated in Auckland, Wellington, and Christchurch, having arrived through "
        "skilled worker and professional visa channels over several decades. South Africa "
        "and New Zealand share Commonwealth ties, and South African professionals in "
        "healthcare, engineering, and finance are well represented. English documentation "
        "from South Africa requires no translation for New Zealand Customs clearance. "
        "The New Zealand High Commission in Pretoria handles consular matters. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    ('canada', 'new-zealand'): (
        "Canadian nationals form a professional community in New Zealand, with workers, "
        "students, and travellers in Auckland and other cities. Canada and New Zealand "
        "share Commonwealth ties and similar legal frameworks. Many Canadians visit New "
        "Zealand on working holiday visas or settle as skilled migrants. English "
        "documentation from Canada requires no translation for New Zealand Customs "
        "clearance. The New Zealand High Commission in Ottawa handles consular matters."
    ),
    ('hong-kong', 'new-zealand'): (
        "Hong Kong nationals form a significant community in New Zealand, with a notable "
        "increase in migration since 2020 under the New Zealand residence visa pathway "
        "for Hong Kong British National (Overseas) holders. Auckland has one of the "
        "largest Hong Kong diaspora communities in the world relative to city size. "
        "Traditional Chinese documentation from Hong Kong requires certified English "
        "translation where needed for New Zealand Customs clearance. The New Zealand "
        "Consulate-General in Hong Kong handles consular matters. "
        "(New Zealand Ministry of Foreign Affairs and Trade, MFAT, 2025.)"
    ),
    # R39: Greece wave 4
    ('georgia', 'greece'): (
        "Georgian nationals form a growing community in Greece, working in construction, "
        "agriculture, and trade in Athens and Thessaloniki. Georgia and Greece have "
        "bilateral diplomatic relations, and Georgian labour migration to Southern Europe "
        "has grown consistently in recent years. Georgian documentation in the Georgian "
        "script requires certified Greek translation for Greek Lixiarcheio (civil registry) "
        "purposes. The Greek Embassy in Tbilisi handles consular matters. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('serbia', 'greece'): (
        "Serbian nationals form a community in Greece, with long-standing cultural, "
        "Orthodox Christian, and commercial ties between the two countries. Serbian "
        "nationals work in tourism, construction, and seasonal agriculture in Greece, "
        "and Serbia is an EU candidate country with bilateral agreements with Greece. "
        "Serbian documentation requires certified Greek translation for Greek civil "
        "registry purposes. The Greek Embassy in Belgrade handles consular matters."
    ),
    ('north-macedonia', 'greece'): (
        "North Macedonian nationals form one of Greece's larger Balkan immigrant "
        "communities, working in agriculture, construction, and seasonal industries "
        "across mainland Greece. Following the 2018 Prespa Agreement, which resolved "
        "the bilateral name dispute, North Macedonia and Greece normalised relations "
        "and expanded economic ties. Macedonian documentation requires certified Greek "
        "translation for Greek Lixiarcheio purposes. The Greek Embassy in Skopje handles "
        "consular matters. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    ('ethiopia', 'greece'): (
        "Ethiopian nationals form part of Greece's sub-Saharan African diaspora, with "
        "asylum seekers and migrants concentrated in Athens following the Eastern "
        "Mediterranean migration routes. Greece has received Ethiopian nationals through "
        "the Aegean crossing and overland routes. Amharic documentation from Ethiopia "
        "requires certified Greek translation for Greek civil registry purposes. The "
        "Greek Embassy in Addis Ababa handles consular matters. Ethiopia to Greece is a "
        "growing corridor as East African migration to Southern Europe has increased."
    ),
    ('iran', 'greece'): (
        "Iranian nationals form a growing diaspora in Greece, with asylum seekers and "
        "established residents concentrated in Athens. Greece and Iran maintain diplomatic "
        "relations, and many Iranians have settled in Greece through legal migration "
        "and humanitarian channels. Farsi documentation from Iran requires certified "
        "Greek translation for Greek Lixiarcheio purposes. The Greek Embassy in Tehran "
        "handles consular matters. Iran to Greece is a significant migration corridor "
        "requiring specialist document handling. "
        "(Greek Ministry of Foreign Affairs, 2025.)"
    ),
    # R39: Austria wave 4
    ('hungary', 'austria'): (
        "Hungarian nationals form Austria's largest neighbouring diaspora, with thousands "
        "working in Vienna and across eastern Austria. Austria and Hungary share a land "
        "border, EU membership, and historical Austro-Hungarian ties that have shaped "
        "the bilateral relationship for over a century. Many Hungarian nationals commute "
        "daily to Vienna for work and others reside permanently in Austria. Hungarian "
        "documentation requires certified German translation for Austrian Standesamt "
        "purposes. The Austrian Embassy in Budapest handles consular matters. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    ('croatia', 'austria'): (
        "Croatian nationals form a significant community in Austria, with families who "
        "arrived as labour migrants from the 1960s onward and subsequent generations "
        "settling permanently, particularly in Vienna and Graz. Austria and Croatia are "
        "both EU members, and the Croatian diaspora in Austria is among the largest "
        "outside Croatia. Croatian documentation requires certified German translation "
        "for Austrian civil registry purposes. The Austrian Embassy in Zagreb handles "
        "consular matters."
    ),
    ('slovakia', 'austria'): (
        "Slovak nationals form a large community in Austria, with many living in Vienna "
        "and maintaining ties to Bratislava, which is 60 kilometres from Vienna. The "
        "Bratislava-Vienna corridor is one of the most active bilateral commuter and "
        "residential routes in Central Europe. Austria and Slovakia share EU membership "
        "and an open border. Slovak documentation requires certified German translation "
        "for Austrian Standesamt purposes. The Austrian Embassy in Bratislava handles "
        "consular matters. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    ('czech-republic', 'austria'): (
        "Czech nationals form a significant community in Austria, with labour migration "
        "and cultural ties that predate EU membership. Austria and the Czech Republic "
        "share a land border and extensive bilateral trade. The Czech diaspora in Vienna "
        "has grown since EU accession in 2004, with professionals, students, and workers "
        "settling across eastern Austria. Czech documentation requires certified German "
        "translation for Austrian civil registry authorities. The Austrian Embassy in "
        "Prague handles consular matters."
    ),
    ('albania', 'austria'): (
        "Albanian nationals form a significant diaspora in Austria, concentrated in Vienna "
        "and Graz, having arrived through labour migration since the 1990s following the "
        "collapse of the communist system in Albania. Albania is an EU candidate country "
        "with longstanding migration ties to Austria, and many Albanian families in Austria "
        "are now multi-generational. Albanian documentation requires certified German "
        "translation for Austrian Standesamt purposes. The Austrian Embassy in Tirana "
        "handles consular matters. "
        "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
    ),
    # R39: Denmark wave 4
    ('china', 'denmark'): (
        "Chinese nationals form part of Denmark's East Asian community, with professionals, "
        "students, and business owners in Copenhagen. Denmark and China have bilateral "
        "trade ties, and Danish companies including Maersk and Novo Nordisk have "
        "significant China operations, creating professional exchange between the two "
        "countries. Chinese documentation in Mandarin requires certified Danish translation "
        "for Danish civil registry purposes. The Danish Embassy in Beijing handles consular "
        "matters. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('ghana', 'denmark'): (
        "Ghanaian nationals form part of Denmark's West African diaspora, with professionals "
        "and students in Copenhagen across multiple sectors. Ghana and Denmark have bilateral "
        "diplomatic ties and development cooperation links through DANIDA. English "
        "documentation from Ghana may still require certified Danish translation for Danish "
        "civil registry purposes. The Danish Embassy in Accra handles consular matters. "
        "Ghana to Denmark is a growing corridor for skilled professional and student migration."
    ),
    ('kenya', 'denmark'): (
        "Kenyan nationals form part of Denmark's East African diaspora, with professionals "
        "in Copenhagen across healthcare, technology, and academic sectors. Denmark and "
        "Kenya have development cooperation ties through DANIDA. Swahili and English "
        "documentation from Kenya may require certified Danish translation for Danish "
        "civil registry purposes. The Danish Embassy in Nairobi handles consular matters. "
        "Kenya to Denmark is a consistent corridor for skilled workers and students. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    ('bangladesh', 'denmark'): (
        "Bangladeshi nationals form a growing community in Denmark, with families working "
        "in trade, hospitality, and professional sectors in Copenhagen and Aarhus. Denmark "
        "and Bangladesh have bilateral diplomatic ties. Bengali documentation from Bangladesh "
        "requires certified Danish translation for Danish civil registry purposes. The Danish "
        "Embassy in Dhaka handles consular matters. Bangladesh to Denmark is a consistent "
        "diaspora corridor."
    ),
    ('eritrea', 'denmark'): (
        "Eritrean nationals form one of Denmark's larger East African diaspora communities, "
        "with many having arrived as refugees through the Red Sea and Mediterranean routes "
        "over two decades. Denmark accepted Eritrean humanitarian cases, and the Eritrean "
        "community is established in Copenhagen, Aarhus, and other cities. Tigrinya "
        "documentation from Eritrea requires certified Danish translation for Danish civil "
        "registry purposes. The Danish Embassy covers Eritrea from Addis Ababa. "
        "(Danish Ministry of Foreign Affairs, 2025.)"
    ),
    # R40: Finland wave 4
    ('ghana', 'finland'): (
        "Ghanaian nationals form part of Finland's sub-Saharan African community, with "
        "professionals and students in Helsinki and Tampere. Finland and Ghana have "
        "diplomatic ties and development cooperation links. English documentation from "
        "Ghana may still require certified Finnish translation for Finnish DVV registry "
        "purposes. The Finnish Embassy in Accra handles consular matters. Ghana to "
        "Finland is a growing corridor for skilled workers and international students."
    ),
    ('eritrea', 'finland'): (
        "Eritrean nationals form one of Finland's East African refugee communities, with "
        "many having arrived through asylum channels over two decades. Finland has accepted "
        "Eritrean humanitarian cases, and the community is established in Helsinki and "
        "Espoo. Tigrinya documentation from Eritrea requires certified Finnish translation "
        "for Finnish DVV registry authorities. The Finnish Embassy covers Eritrea from "
        "Addis Ababa. Specialist support is recommended to confirm current consular access. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('morocco', 'finland'): (
        "Moroccan nationals form part of Finland's North African diaspora, with workers "
        "and students in Helsinki and other cities. Finland and Morocco have bilateral "
        "diplomatic ties. Arabic and Darija documentation from Morocco requires certified "
        "Finnish translation for Finnish DVV registry purposes. The Finnish Embassy in "
        "Rabat handles consular matters. Morocco to Finland is part of the broader "
        "Maghreb-to-Northern-Europe migration corridor."
    ),
    ('indonesia', 'finland'): (
        "Indonesian nationals form a small but established community in Finland, with "
        "students, professionals, and families in Helsinki and Espoo. Finland and Indonesia "
        "have bilateral diplomatic ties and trade links through Finnish companies operating "
        "in South East Asia. Indonesian documentation in Bahasa Indonesia requires certified "
        "Finnish translation for Finnish registry purposes. The Finnish Embassy in Jakarta "
        "handles consular matters. "
        "(Finnish Ministry of Foreign Affairs, 2025.)"
    ),
    ('senegal', 'finland'): (
        "Senegalese nationals form part of Finland's West African diaspora, with traders "
        "and professionals in Helsinki. Finland and Senegal have development cooperation "
        "ties and bilateral diplomatic relations. Wolof and French documentation from "
        "Senegal requires certified Finnish translation for Finnish DVV registry purposes. "
        "The Finnish Embassy in Dakar handles consular matters. Senegal to Finland is a "
        "growing corridor."
    ),
    # R40: Singapore wave 4
    ('australia', 'singapore'): (
        "Australian nationals form a significant professional and business community in "
        "Singapore, drawn by Singapore's role as a major financial and commercial hub in "
        "Asia. Australia and Singapore share a Free Trade Agreement and close defence ties. "
        "English documentation from Australia is well understood by Singapore authorities "
        "and requires no translation for most administrative purposes. The Singapore High "
        "Commission in Canberra handles consular matters. "
        "(Singapore Ministry of Foreign Affairs, 2025.)"
    ),
    ('usa', 'singapore'): (
        "American nationals form a significant expatriate community in Singapore, drawn by "
        "multinational corporate presence and Singapore's role as a regional financial "
        "centre. The US and Singapore have close economic and defence ties under the "
        "US-Singapore Free Trade Agreement. English documentation from the US is well "
        "understood by Singapore authorities. The Singapore Embassy in Washington DC "
        "handles consular matters. USA to Singapore is a high-volume professional "
        "repatriation corridor."
    ),
    ('south-africa', 'singapore'): (
        "South African nationals form part of Singapore's professional expatriate community, "
        "attracted by financial services, trade, and technology roles. South Africa and "
        "Singapore have bilateral diplomatic ties and commercial links. English documentation "
        "from South Africa is generally understood by Singapore authorities, though "
        "authentication by the Singapore High Commission is required before customs "
        "clearance. The Singapore High Commission in Pretoria handles consular matters. "
        "(Singapore Ministry of Foreign Affairs, 2025.)"
    ),
    ('kenya', 'singapore'): (
        "Kenyan nationals form part of Singapore's African professional community, working "
        "in financial services, technology, and trade. Kenya and Singapore have bilateral "
        "diplomatic relations and growing commercial links. English documentation from Kenya "
        "is generally understood by Singapore authorities, though authentication by the "
        "Singapore High Commission is required. The Singapore High Commission in Nairobi "
        "handles consular matters."
    ),
    ('nigeria', 'singapore'): (
        "Nigerian nationals form part of Singapore's West African professional community, "
        "attracted by Singapore's financial sector and technology industry. Nigeria and "
        "Singapore have bilateral diplomatic ties. English documentation from Nigeria "
        "requires authentication by the Singapore High Commission before Singapore Customs "
        "clearance. The Singapore High Commission in Abuja handles consular matters. "
        "Nigeria to Singapore is a growing corridor for skilled professional migration. "
        "(Singapore Ministry of Foreign Affairs, 2025.)"
    ),
    # R40: South Africa wave 4
    ('france', 'south-africa'): (
        "French nationals form a significant expatriate community in South Africa, "
        "concentrated in Cape Town, Johannesburg, and Durban across business, viticulture, "
        "agriculture, and professional sectors. South Africa is among France's most "
        "significant African trading partners, and French investment in South Africa is "
        "substantial. French documentation may require certified translation for South "
        "African Home Affairs purposes. The South African Embassy in Paris handles "
        "consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('usa', 'south-africa'): (
        "American nationals form a significant expatriate and tourist community in South "
        "Africa, drawn by the safari industry, natural beauty, and business opportunities. "
        "South Africa is a major destination for American tourists and business travellers, "
        "and US corporate investment in South Africa is substantial. English documentation "
        "from the USA is understood by South African Home Affairs authorities. The South "
        "African Embassy in Washington DC handles consular matters."
    ),
    ('germany', 'south-africa'): (
        "German nationals form a significant tourist and business community in South Africa, "
        "with Germany being one of South Africa's most important European trading partners. "
        "German tourists represent a major segment of South Africa's inbound tourism market, "
        "and German companies have significant investment interests in South Africa. German "
        "documentation requires certified translation for South African Home Affairs "
        "purposes. The South African Embassy in Berlin handles consular matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    ('australia', 'south-africa'): (
        "Australian nationals form a significant diaspora and business community in South "
        "Africa, with many Australians of South African heritage maintaining family ties "
        "to both countries. Australia and South Africa share Commonwealth ties and "
        "significant community overlap, with South Africans also representing one of the "
        "largest migrant groups in Australia. English documentation from Australia is "
        "understood by South African Home Affairs authorities. The South African High "
        "Commission in Canberra handles consular matters."
    ),
    ('netherlands', 'south-africa'): (
        "Dutch nationals have a particular historical connection to South Africa through "
        "the Afrikaner community and the longstanding Netherlands-South Africa relationship. "
        "Dutch tourists and business travellers visit South Africa in significant numbers, "
        "and the linguistic proximity between Dutch and Afrikaans facilitates bilateral "
        "interaction. Dutch documentation requires certified translation for South African "
        "Home Affairs purposes. The South African Embassy in The Hague handles consular "
        "matters. "
        "(South African Department of International Relations and Cooperation, DIRCO, 2025.)"
    ),
    # R40: Saudi Arabia wave 5
    ('morocco', 'saudi-arabia'): (
        "Moroccan nationals form one of the larger North African worker communities in "
        "Saudi Arabia, with thousands of Moroccans employed across construction, services, "
        "and professional sectors. Morocco and Saudi Arabia have strong bilateral ties as "
        "fellow Arab League and Organisation of Islamic Cooperation (OIC) member states. "
        "Arabic documentation from Morocco is generally understood by Saudi authorities, "
        "though notarisation and authentication by the Saudi Embassy are required. "
        "The Saudi Embassy in Rabat handles consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('ivory-coast', 'saudi-arabia'): (
        "Ivorian nationals working in Saudi Arabia include Muslim workers from Ivory Coast's "
        "substantial Muslim majority population, employed in construction, agriculture, and "
        "service sectors. Ivory Coast and Saudi Arabia have diplomatic relations, with Saudi "
        "Arabia maintaining an embassy in Abidjan. French and local language documentation "
        "from Ivory Coast requires Arabic translation and authentication by the Saudi Embassy "
        "for Saudi Ministry of Health clearance. The Saudi Embassy in Abidjan handles "
        "consular matters."
    ),
    ('burkina-faso', 'saudi-arabia'): (
        "Burkinabe nationals working in Saudi Arabia include Muslim workers from Burkina "
        "Faso's majority-Muslim population, employed in the service and construction sectors. "
        "Burkina Faso and Saudi Arabia have diplomatic ties as fellow OIC member states. "
        "French documentation from Burkina Faso requires certified Arabic translation and "
        "authentication by the Saudi Embassy for Saudi Ministry of Health clearance. "
        "The Saudi Embassy in Ouagadougou handles consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    ('togo', 'saudi-arabia'): (
        "Togolese nationals working in Saudi Arabia include Muslim workers from Togo's "
        "Muslim community employed in trade and service sectors. Togo and Saudi Arabia "
        "have diplomatic relations as OIC member states, with Saudi Arabia maintaining "
        "an embassy in Lome. French documentation from Togo requires certified Arabic "
        "translation and authentication by the Saudi Embassy for official purposes. "
        "The Saudi Embassy in Lome handles consular matters."
    ),
    ('djibouti', 'saudi-arabia'): (
        "Djiboutian nationals have a close connection to Saudi Arabia through the "
        "geographical proximity of Djibouti across the Gulf of Aden, as well as shared "
        "Arabic-speaking and Muslim communities. Djibouti and Saudi Arabia are fellow "
        "Arab League members with strong bilateral ties. Arabic documentation from "
        "Djibouti is generally understood by Saudi authorities, though authentication "
        "by the Saudi Embassy is required. The Saudi Embassy in Djibouti City handles "
        "consular matters. "
        "(Saudi Ministry of Foreign Affairs, 2025.)"
    ),
    # R40: USA wave 5
    ('japan', 'united-states'): (
        "Japanese Americans and American nationals of Japanese descent maintain strong "
        "family ties to Japan, and Japan has a long-established diplomatic and trade "
        "relationship with the United States. California, Hawaii, and New York host "
        "large Japanese American communities. A death in Japan requires the Japanese "
        "authorities to issue an export permit and a sanitised coffin certificate before "
        "remains can depart. The US Embassy in Tokyo handles consular matters for American "
        "nationals dying in Japan. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('argentina', 'united-states'): (
        "Argentine nationals form a significant diaspora in the United States, concentrated "
        "in Florida, New York, California, and Texas, with established Argentine-American "
        "communities in Miami and New York City. Argentina and the United States have "
        "bilateral diplomatic relations as Western Hemisphere partners. Spanish "
        "documentation from Argentina requires certified English translation for US state "
        "requirements. The US Embassy in Buenos Aires handles consular matters."
    ),
    ('south-africa', 'united-states'): (
        "South African nationals form a professional diaspora in the United States, "
        "concentrated in New York, Los Angeles, and Houston, with South African-born "
        "professionals working in medicine, finance, and technology sectors. South Africa "
        "and the United States have bilateral diplomatic relations. English documentation "
        "from South Africa is understood by US Customs and state authorities. The US "
        "Embassy in Pretoria handles consular matters. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
    ),
    ('georgia', 'united-states'): (
        "Georgian nationals form a growing diaspora in the United States, concentrated in "
        "New York, New Jersey, and Los Angeles. Georgia and the United States have strong "
        "bilateral ties, and many Georgians emigrated following the 1990s political and "
        "economic challenges, with further migration after the 2008 conflict. Georgian "
        "documentation in the Georgian script requires certified English translation for "
        "US state and customs requirements. The US Embassy in Tbilisi handles consular "
        "matters."
    ),
    ('tanzania', 'united-states'): (
        "Tanzanian nationals form part of the United States' East African diaspora, "
        "concentrated in cities including Minneapolis, New York, and Washington DC. "
        "Tanzania and the United States have bilateral diplomatic relations and development "
        "cooperation ties. Swahili documentation from Tanzania requires certified English "
        "translation for US Customs and state requirements. The US Embassy in Dar es Salaam "
        "handles consular matters. Tanzania to the United States is a consistent corridor "
        "for the East African diaspora. "
        "(US State Department, Bureau of Consular Affairs, 2025.)"
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
# Route list: R39 (25) + R40 (25) = 50 routes
# Template rotation starts at D (index 3). Each block of 25 cycles D,E,A,B,C x5.
# ---------------------------------------------------------------------------

ALL_ROUTES = [
    # --- Block R39: Japan wave 4 x5 + New Zealand wave 4 x5 + Greece wave 4 x5 +
    #     Austria wave 4 x5 + Denmark wave 4 x5 = 25
    ('usa',              'japan'),
    ('australia',        'japan'),
    ('france',           'japan'),
    ('germany',          'japan'),
    ('italy',            'japan'),
    ('australia',        'new-zealand'),
    ('usa',              'new-zealand'),
    ('south-africa',     'new-zealand'),
    ('canada',           'new-zealand'),
    ('hong-kong',        'new-zealand'),
    ('georgia',          'greece'),
    ('serbia',           'greece'),
    ('north-macedonia',  'greece'),
    ('ethiopia',         'greece'),
    ('iran',             'greece'),
    ('hungary',          'austria'),
    ('croatia',          'austria'),
    ('slovakia',         'austria'),
    ('czech-republic',   'austria'),
    ('albania',          'austria'),
    ('china',            'denmark'),
    ('ghana',            'denmark'),
    ('kenya',            'denmark'),
    ('bangladesh',       'denmark'),
    ('eritrea',          'denmark'),
    # --- Block R40: Finland wave 4 x5 + Singapore wave 4 x5 + South Africa wave 4 x5 +
    #     Saudi Arabia wave 5 x5 + USA wave 5 x5 = 25
    ('ghana',            'finland'),
    ('eritrea',          'finland'),
    ('morocco',          'finland'),
    ('indonesia',        'finland'),
    ('senegal',          'finland'),
    ('australia',        'singapore'),
    ('usa',              'singapore'),
    ('south-africa',     'singapore'),
    ('kenya',            'singapore'),
    ('nigeria',          'singapore'),
    ('france',           'south-africa'),
    ('usa',              'south-africa'),
    ('germany',          'south-africa'),
    ('australia',        'south-africa'),
    ('netherlands',      'south-africa'),
    ('morocco',          'saudi-arabia'),
    ('ivory-coast',      'saudi-arabia'),
    ('burkina-faso',     'saudi-arabia'),
    ('togo',             'saudi-arabia'),
    ('djibouti',         'saudi-arabia'),
    ('japan',            'united-states'),
    ('argentina',        'united-states'),
    ('south-africa',     'united-states'),
    ('georgia',          'united-states'),
    ('tanzania',         'united-states'),
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
