#!/usr/bin/env python3
"""Generate Ireland Tier A route pages R9-R12 (100 routes)."""

import os, re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

IRISH_EMBASSY = {
    'democratic-republic-of-the-congo': 'Nairobi',
    'costa-rica': 'Mexico City',
    'croatia': 'Zagreb',
    'cuba': 'Mexico City',
    'czech-republic': 'Prague',
    'denmark': 'Copenhagen',
    'djibouti': 'Nairobi',
    'dominica': 'Washington DC',
    'dominican-republic': 'Washington DC',
    'ecuador': 'Bogota',
    'el-salvador': 'Mexico City',
    'equatorial-guinea': 'Abuja',
    'eritrea': 'Nairobi',
    'estonia': 'Tallinn',
    'eswatini': 'Pretoria',
    'ethiopia': 'Addis Ababa',
    'fiji': 'Canberra',
    'finland': 'Helsinki',
    'gabon': 'Abuja',
    'gambia': 'Accra',
    'georgia': 'Ankara',
    'grenada': 'Washington DC',
    'guatemala': 'Mexico City',
    'guinea': 'Abidjan',
    'guinea-bissau': 'Accra',
    'guyana': 'Washington DC',
    'haiti': 'Washington DC',
    'honduras': 'Mexico City',
    'hungary': 'Budapest',
    'iceland': 'Copenhagen',
    'iran': 'Ankara',
    'iraq': 'Abu Dhabi',
    'ivory-coast': 'Abidjan',
    'jamaica': 'Washington DC',
    'kazakhstan': 'Ankara',
    'kiribati': 'Canberra',
    'kuwait': 'Abu Dhabi',
    'kyrgyzstan': 'Ankara',
    'laos': 'Bangkok',
    'latvia': 'Riga',
    'lebanon': 'Beirut',
    'lesotho': 'Pretoria',
    'liberia': 'Accra',
    'libya': 'Tunis',
    'liechtenstein': 'Berne',
    'lithuania': 'Vilnius',
    'luxembourg': 'Brussels',
    'madagascar': 'Nairobi',
    'malawi': 'Nairobi',
    'malaysia': 'Singapore',
    'maldives': 'Singapore',
    'mali': 'Abidjan',
    'malta': 'Valletta',
    'marshall-islands': 'Canberra',
    'mauritania': 'Rabat',
    'mauritius': 'Pretoria',
    'micronesia': 'Canberra',
    'moldova': 'Bucharest',
    'monaco': 'Paris',
    'mongolia': 'Beijing',
    'montenegro': 'Zagreb',
    'mozambique': 'Pretoria',
    'myanmar': 'Bangkok',
    'namibia': 'Pretoria',
    'nauru': 'Canberra',
    'nepal': 'New Delhi',
    'netherlands': 'The Hague',
    'nicaragua': 'Mexico City',
    'niger': 'Abuja',
    'north-korea': 'Beijing',
    'north-macedonia': 'Zagreb',
    'norway': 'Oslo',
    'oman': 'Abu Dhabi',
    'palau': 'Canberra',
    'palestine': 'Ramallah',
    'panama': 'Mexico City',
    'papua-new-guinea': 'Canberra',
    'paraguay': 'Buenos Aires',
    'peru': 'Lima',
    'poland': 'Warsaw',
    'qatar': 'Abu Dhabi',
    'romania': 'Bucharest',
    'russia': 'Moscow',
    'rwanda': 'Nairobi',
    'saint-kitts-and-nevis': 'Washington DC',
    'saint-lucia': 'Washington DC',
    'saint-vincent-and-the-grenadines': 'Washington DC',
    'samoa': 'Canberra',
    'san-marino': 'Rome',
    'sao-tome-and-principe': 'Accra',
    'saudi-arabia': 'Riyadh',
    'senegal': 'Dakar',
    'serbia': 'Belgrade',
    'seychelles': 'Nairobi',
    'sierra-leone': 'Accra',
    'slovakia': 'Bratislava',
    'slovenia': 'Ljubljana',
    'solomon-islands': 'Canberra',
    'somalia': 'Nairobi',
    'south-sudan': 'Nairobi',
}

RESIDENT_SAME_CITY = {
    'croatia', 'czech-republic', 'denmark', 'estonia', 'ethiopia', 'finland',
    'hungary', 'latvia', 'lebanon', 'lithuania', 'malta', 'netherlands',
    'norway', 'poland', 'romania', 'russia', 'saudi-arabia', 'senegal',
    'serbia', 'slovakia', 'slovenia', 'ivory-coast', 'kuwait',
    'oman', 'qatar', 'peru', 'malaysia',
}

ORIGIN_NAMES = {
    'democratic-republic-of-the-congo': 'Democratic Republic of the Congo',
    'costa-rica': 'Costa Rica',
    'croatia': 'Croatia',
    'cuba': 'Cuba',
    'czech-republic': 'Czech Republic',
    'denmark': 'Denmark',
    'djibouti': 'Djibouti',
    'dominica': 'Dominica',
    'dominican-republic': 'Dominican Republic',
    'ecuador': 'Ecuador',
    'el-salvador': 'El Salvador',
    'equatorial-guinea': 'Equatorial Guinea',
    'eritrea': 'Eritrea',
    'estonia': 'Estonia',
    'eswatini': 'Eswatini',
    'ethiopia': 'Ethiopia',
    'fiji': 'Fiji',
    'finland': 'Finland',
    'gabon': 'Gabon',
    'gambia': 'Gambia',
    'georgia': 'Georgia',
    'grenada': 'Grenada',
    'guatemala': 'Guatemala',
    'guinea': 'Guinea',
    'guinea-bissau': 'Guinea-Bissau',
    'guyana': 'Guyana',
    'haiti': 'Haiti',
    'honduras': 'Honduras',
    'hungary': 'Hungary',
    'iceland': 'Iceland',
    'iran': 'Iran',
    'iraq': 'Iraq',
    'ivory-coast': 'Ivory Coast',
    'jamaica': 'Jamaica',
    'kazakhstan': 'Kazakhstan',
    'kiribati': 'Kiribati',
    'kuwait': 'Kuwait',
    'kyrgyzstan': 'Kyrgyzstan',
    'laos': 'Laos',
    'latvia': 'Latvia',
    'lebanon': 'Lebanon',
    'lesotho': 'Lesotho',
    'liberia': 'Liberia',
    'libya': 'Libya',
    'liechtenstein': 'Liechtenstein',
    'lithuania': 'Lithuania',
    'luxembourg': 'Luxembourg',
    'madagascar': 'Madagascar',
    'malawi': 'Malawi',
    'malaysia': 'Malaysia',
    'maldives': 'Maldives',
    'mali': 'Mali',
    'malta': 'Malta',
    'marshall-islands': 'Marshall Islands',
    'mauritania': 'Mauritania',
    'mauritius': 'Mauritius',
    'micronesia': 'Micronesia',
    'moldova': 'Moldova',
    'monaco': 'Monaco',
    'mongolia': 'Mongolia',
    'montenegro': 'Montenegro',
    'mozambique': 'Mozambique',
    'myanmar': 'Myanmar',
    'namibia': 'Namibia',
    'nauru': 'Nauru',
    'nepal': 'Nepal',
    'netherlands': 'Netherlands',
    'nicaragua': 'Nicaragua',
    'niger': 'Niger',
    'north-korea': 'North Korea',
    'north-macedonia': 'North Macedonia',
    'norway': 'Norway',
    'oman': 'Oman',
    'palau': 'Palau',
    'palestine': 'Palestine',
    'panama': 'Panama',
    'papua-new-guinea': 'Papua New Guinea',
    'paraguay': 'Paraguay',
    'peru': 'Peru',
    'poland': 'Poland',
    'qatar': 'Qatar',
    'romania': 'Romania',
    'russia': 'Russia',
    'rwanda': 'Rwanda',
    'saint-kitts-and-nevis': 'Saint Kitts and Nevis',
    'saint-lucia': 'Saint Lucia',
    'saint-vincent-and-the-grenadines': 'Saint Vincent and the Grenadines',
    'samoa': 'Samoa',
    'san-marino': 'San Marino',
    'sao-tome-and-principe': 'Sao Tome and Principe',
    'saudi-arabia': 'Saudi Arabia',
    'senegal': 'Senegal',
    'serbia': 'Serbia',
    'seychelles': 'Seychelles',
    'sierra-leone': 'Sierra Leone',
    'slovakia': 'Slovakia',
    'slovenia': 'Slovenia',
    'solomon-islands': 'Solomon Islands',
    'somalia': 'Somalia',
    'south-sudan': 'South Sudan',
}


def read_uk_file(slug):
    path = os.path.join(ROUTES_DIR, f'{slug}-to-united-kingdom.md')
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


def adapt(text, uk_city, ir_city, origin_name):
    """Adapt text from UK route to Ireland route, carefully."""

    # --- Embassy references ---
    # Replace "British Embassy in [origin_name]" (FAQ question pattern)
    text = text.replace(f'British Embassy in {origin_name}', f'Irish Embassy in {ir_city}')
    text = text.replace(f'British High Commission in {origin_name}', f'Irish Embassy in {ir_city}')

    # Handle uk_city variants with parenthetical notes e.g. "Lagos (covering embassy, Nigeria)"
    if '(' in uk_city:
        base = uk_city.split('(')[0].strip()
        text = text.replace(f'British Embassy in {base}', f'Irish Embassy in {ir_city}')
        text = text.replace(f'British High Commission in {base}', f'Irish Embassy in {ir_city}')

    # Replace specific UK city embassy references
    text = text.replace(f'British Embassy in {uk_city}', f'Irish Embassy in {ir_city}')
    text = text.replace(f'British High Commission in {uk_city}', f'Irish Embassy in {ir_city}')

    # Fix any residual "Irish Embassy in [wrong city]" left from prior runs
    if uk_city and uk_city != ir_city:
        text = text.replace(f'Irish Embassy in {uk_city}', f'Irish Embassy in {ir_city}')
        if '(' in uk_city:
            base = uk_city.split('(')[0].strip()
            text = text.replace(f'Irish Embassy in {base}', f'Irish Embassy in {ir_city}')

    # Generic fallbacks
    text = text.replace('There is no resident UK Embassy', 'There is no resident Irish Embassy')
    text = text.replace('no resident UK Embassy', 'no resident Irish Embassy')
    text = text.replace('no resident UK embassy', 'no resident Irish Embassy')
    text = text.replace('British Embassy', 'Irish Embassy')
    text = text.replace('British High Commission', 'Irish Embassy')

    # --- Phone and authority ---
    text = text.replace('+44 (0)20 7008 5000', '+353 1 408 2000')
    text = text.replace('FCDO 24-hour emergency line', 'Department of Foreign Affairs emergency line')
    text = text.replace('FCDO emergency line', 'Department of Foreign Affairs emergency line')
    text = text.replace('FCDO travel advice for', 'Department of Foreign Affairs travel advice for')
    text = text.replace('FCDO travel advice', 'Department of Foreign Affairs travel advice')
    text = text.replace('FCDO advises', 'Department of Foreign Affairs advises')
    text = text.replace('FCDO', 'Department of Foreign Affairs')
    text = text.replace('gov.uk, 2026', 'gov.ie, 2026')
    text = text.replace('gov.uk', 'gov.ie')

    # --- Personnel and direction ---
    text = text.replace('UK funeral director', 'Irish funeral director')
    text = text.replace('United Kingdom funeral director', 'Irish funeral director')
    text = text.replace('UK authorities', 'Irish authorities')
    text = text.replace('British nationals', 'Irish nationals')

    # --- Coroner ---
    text = text.replace('coroner for the district', 'Coroner for the district')
    text = text.replace('UK coroner', 'Coroner')

    # --- Destination country ---
    text = text.replace('to United Kingdom', 'to Ireland')
    text = text.replace('in United Kingdom', 'in Ireland')
    text = text.replace('the United Kingdom', 'Ireland')
    text = text.replace('United Kingdom', 'Ireland')
    text = text.replace('for UK acceptance', 'for Irish acceptance')
    # Avoid "for UK" → "for Ireland" which could produce "for Irelandish" etc.
    text = text.replace(' for UK ', ' for Ireland ')
    text = text.replace(' to UK', ' to Ireland')
    text = text.replace(' the UK', ' Ireland')
    text = text.replace(' UK.', ' Ireland.')
    text = text.replace(' UK,', ' Ireland,')
    text = text.replace(' UK ', ' Ireland ')
    # Clean any doubled replacements
    text = text.replace('Ireland Ireland', 'Ireland')

    # --- Timeline step 3: embassy city ---
    # "Irish Embassy Kinshasa notified" → "Irish Embassy Nairobi notified"
    text = re.sub(
        r'Irish Embassy \S+ notified\.',
        f'Irish Embassy {ir_city} notified.',
        text
    )
    text = re.sub(
        r'Irish Embassy \S+\s+\S+ notified\.',
        f'Irish Embassy {ir_city} notified.',
        text
    )

    # --- Step 6 artifact ---
    text = text.replace('cargo terminal at destination', 'Dublin Airport cargo terminal')

    # --- Consular "via" patterns for countries without resident embassy ---
    # e.g. "consular assistance is via Nigeria" → "consular assistance is via {ir_city}"
    # e.g. "consular assistance is via Nigeria or Cameroon" → ...
    text = re.sub(
        r'consular assistance is (?:provided )?via [A-Z][A-Za-z\s]+(?:or [A-Z][A-Za-z]+)?',
        f'consular assistance is via {ir_city}',
        text
    )
    text = re.sub(
        r'consular assistance is (?:provided )?via [A-Z][A-Za-z]+(?: or [A-Z][A-Za-z]+)?',
        f'consular assistance is via {ir_city}',
        text
    )

    return text


def make_dest_reception():
    return ("The Irish funeral director takes custody at the cargo terminal. "
            "All documentation must be in certified English translation where required. "
            "The Coroner for the district is notified. "
            "Straightforward cases proceed directly to funeral arrangements.")


def make_dest_consular(ir_city, origin_name, is_resident):
    base = "Department of Foreign Affairs emergency line: +353 1 408 2000 (24 hours). "
    if is_resident:
        base += (f"The Irish Embassy in {ir_city} can register the death and advise on local "
                 "funeral directors. They cannot pay for or arrange repatriation.")
    else:
        base += (f"The Irish Embassy in {ir_city} covers {origin_name} and can register the "
                 "death and advise on documentation. They cannot pay for or arrange repatriation.")
    return base


def make_embassy_faq(ir_city, origin_name, is_resident, slug):
    if is_resident:
        question = f"Does the Irish Embassy in {origin_name} help with repatriation?"
        answer = (f"The Irish Embassy in {ir_city} can register the death with Irish authorities, "
                  f"provide a list of local funeral directors in {origin_name}, and advise on documentation. "
                  "They cannot pay for or arrange repatriation. "
                  "Department of Foreign Affairs emergency line: +353 1 408 2000.")
    else:
        question = f"Is there an Irish Embassy in {origin_name}?"
        answer = (f"There is no resident Irish Embassy in {origin_name}. "
                  f"Consular matters are handled by the Irish Embassy in {ir_city}. "
                  "Call the Department of Foreign Affairs emergency line on +353 1 408 2000 (gov.ie, 2026) "
                  "as soon as possible. They can provide a list of local funeral directors and register the "
                  "death with Irish authorities.")
    return f'  - question: "{question}"\n    answer: "{answer}"'


def make_description(origin_name, timeline_avg, complexity):
    notes = {
        'low': 'A well-documented EU process.',
        'moderate': 'Specialist support recommended.',
        'moderate-high': 'Complex route; a specialist is essential.',
        'high': 'Specialist help required.',
        'very-high': 'One of the most complex routes. A specialist is essential.',
    }
    note = notes.get(complexity, 'Specialist support recommended.')
    desc = (f"Someone has died in {origin_name}. Repatriation to Ireland takes "
            f"{timeline_avg}. {note} Contact us 24/7.")
    return desc[:155]


def generate_route(slug, variant_idx):
    origin_name = ORIGIN_NAMES.get(slug, slug.replace('-', ' ').title())
    ir_city = IRISH_EMBASSY.get(slug, 'Dublin')
    is_resident = slug in RESIDENT_SAME_CITY
    variant = VARIANTS[variant_idx % 5]

    uk_content = read_uk_file(slug)
    if not uk_content:
        print(f"  ERROR: No UK route for {slug}")
        return None

    uk_fm = get_fm(uk_content)
    uk_city = get_field(uk_fm, 'embassy_city')

    timeline_avg = get_field(uk_fm, 'timeline_avg')
    timeline_fast = get_field(uk_fm, 'timeline_fast')
    timeline_complex = get_field(uk_fm, 'timeline_complex')
    complexity = get_field(uk_fm, 'route_complexity')
    doc_time = get_field(uk_fm, 'doc_processing_time')

    def a(text):
        return adapt(text, uk_city, ir_city, origin_name)

    dah = a(extract_block(uk_fm, 'direct_answer_heading',
                          ['direct_answer_intro', 'direct_answer_points', 'overview_heading']))
    dai = a(extract_block(uk_fm, 'direct_answer_intro',
                          ['direct_answer_points', 'overview_heading']))
    dap = a(extract_block(uk_fm, 'direct_answer_points',
                          ['overview_heading', 'dest_reception', 'date']))
    oh = a(extract_block(uk_fm, 'overview_heading', ['overview_body', 'dest_reception']))
    ob = a(extract_block(uk_fm, 'overview_body', ['dest_reception', 'dest_consular']))

    # Timeline steps and FAQs
    ts_raw = extract_block(uk_fm, 'timeline_steps', ['faqs', 'links'])
    faqs_raw = extract_block(uk_fm, 'faqs', ['links'])

    ts = a(ts_raw)
    faqs = a(faqs_raw)

    # Replace the "Does the British Embassy" FAQ with a clean Irish version
    embassy_faq = make_embassy_faq(ir_city, origin_name, is_resident, slug)
    # Remove any remaining British-Embassy-style FAQ question and replace
    faqs = re.sub(
        r'  - question: "Does the (?:British|Irish) Embassy in [^"]*help with repatriation\?"\n    answer: "[^"]*"',
        embassy_faq,
        faqs
    )
    # Also handle "Is there an Irish Embassy in X" pattern that might have been generated
    faqs = re.sub(
        r'  - question: "Is there an? (?:British|Irish) Embassy in [^"]*\?"\n    answer: "[^"]*"',
        embassy_faq,
        faqs
    )

    dest_rec = make_dest_reception()
    dest_con = make_dest_consular(ir_city, origin_name, is_resident)
    description = make_description(origin_name, timeline_avg, complexity)
    title = f"{origin_name} to Ireland: Funeral Repatriation Guidance"

    links = f"""links:
  upward:
    - url: "/repatriation-from-{slug}/"
      text: "Full {origin_name} repatriation guide"
    - url: "/guides/death-abroad-{slug}/"
      text: "What to do if someone dies in {origin_name}"
    - url: "/embassy-contacts/{slug}/"
      text: "Irish Embassy contacts for {origin_name}"
    - url: "/contact/"
      text: "Send an enquiry to our team"
  sideways:
    - url: "/routes/{slug}-to-united-kingdom/"
      text: "Repatriation from {origin_name} to the UK"
    - url: "/routes/ireland-to-{slug}/"
      text: "Repatriation from Ireland to {origin_name}\""""

    content = f"""---
title: "{title}"
description: "{description}"
origin_key: "{slug}"
dest_key: "ie"
origin_name: "{origin_name}"
dest_name: "Ireland"
origin_slug: "{slug}"
dest_slug: "ireland"
slug: "{slug}-to-ireland"
template_variant: "{variant}"
route_complexity: "{complexity}"
timeline_avg: "{timeline_avg}"
timeline_fast: "{timeline_fast}"
timeline_complex: "{timeline_complex}"
embassy_city: "{ir_city}"
doc_processing_time: "{doc_time}"
date: 2026-05-01
{dah}
{dai}
{dap}
{oh}
{ob}
dest_reception: "{dest_rec}"
dest_consular: "{dest_con}"
{ts}
{faqs}
{links}
---
"""
    return content


ALL_SLUGS = [
    # R9
    'democratic-republic-of-the-congo', 'costa-rica', 'croatia', 'cuba', 'czech-republic',
    'denmark', 'djibouti', 'dominica', 'dominican-republic', 'ecuador',
    'el-salvador', 'equatorial-guinea', 'eritrea', 'estonia', 'eswatini',
    'ethiopia', 'fiji', 'finland', 'gabon', 'gambia',
    'georgia', 'grenada', 'guatemala', 'guinea', 'guinea-bissau',
    # R10
    'guyana', 'haiti', 'honduras', 'hungary', 'iceland',
    'iran', 'iraq', 'ivory-coast', 'jamaica', 'kazakhstan',
    'kiribati', 'kuwait', 'kyrgyzstan', 'laos', 'latvia',
    'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein',
    'lithuania', 'luxembourg', 'madagascar', 'malawi', 'malaysia',
    # R11
    'maldives', 'mali', 'malta', 'marshall-islands', 'mauritania',
    'mauritius', 'micronesia', 'moldova', 'monaco', 'mongolia',
    'montenegro', 'mozambique', 'myanmar', 'namibia', 'nauru',
    'nepal', 'netherlands', 'nicaragua', 'niger', 'north-korea',
    'north-macedonia', 'norway', 'oman', 'palau', 'palestine',
    # R12
    'panama', 'papua-new-guinea', 'paraguay', 'peru', 'poland',
    'qatar', 'romania', 'russia', 'rwanda', 'saint-kitts-and-nevis',
    'saint-lucia', 'saint-vincent-and-the-grenadines', 'samoa', 'san-marino', 'sao-tome-and-principe',
    'saudi-arabia', 'senegal', 'serbia', 'seychelles', 'sierra-leone',
    'slovakia', 'slovenia', 'solomon-islands', 'somalia', 'south-sudan',
]

generated, skipped, errors = [], [], []

for i, slug in enumerate(ALL_SLUGS):
    out_path = os.path.join(ROUTES_DIR, f'{slug}-to-ireland.md')
    if os.path.exists(out_path):
        skipped.append(slug)
        continue
    content = generate_route(slug, i)
    if content is None:
        errors.append(slug)
        continue
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    generated.append(slug)
    print(f"  OK: {slug}-to-ireland.md [variant {VARIANTS[i % 5]}]")

print(f"\nGenerated: {len(generated)}, Skipped: {len(skipped)}, Errors: {len(errors)}")
if errors:
    print("Errors:", errors)
