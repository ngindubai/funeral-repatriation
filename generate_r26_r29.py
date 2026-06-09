#!/usr/bin/env python3
"""Generate Tier B route pages: chunk R26.

   R26: Switzerland x5 + Sweden x5 + Norway x5 + Portugal x5 + extra waves x5 = 25

   Switzerland (new hub): turkey, portugal, italy, germany, india
   Sweden      (new hub): syria, somalia, iraq, poland, afghanistan
   Norway      (new hub): poland, somalia, pakistan, india, philippines
   Portugal    (new hub): brazil, angola, mozambique, cabo-verde, guinea-bissau
   Extra waves:           turkey-france, iraq-france, ghana-netherlands,
                          ghana-spain, kenya-netherlands

   Template rotation continues from R25 last variant C, so R26 starts at D (index 3).
   R26 ends on variant C (index 2). R27 starts at D (index 3).
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
    'R26 (Switzerland/Sweden/Norway/Portugal + extra waves)': generated,
}
for block, routes in blocks.items():
    if routes:
        print(
            f"  {block}: {len(routes)} routes, "
            f"variants {','.join(sorted(set(v for _, v in routes)))}"
        )

last_variant = VARIANTS[(START_VARIANT + len(generated) - 1 + len(skipped)) % 5]
print(f"\nLast variant used: {last_variant}")
print(f"Next chunk (R27) should start at: {VARIANTS[(START_VARIANT + 25) % 5]}")
