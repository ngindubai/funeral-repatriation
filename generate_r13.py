#!/usr/bin/env python3
"""Generate Ireland Tier A route pages R13 (28 routes) -- completes Tier A."""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']

# Irish Embassy covering city for each origin country
IRISH_EMBASSY = {
    'hong-kong': 'Beijing',
    'south-korea': 'Seoul',
    'sudan': 'Cairo',
    'suriname': 'Washington DC',
    'sweden': 'Stockholm',
    'switzerland': 'Berne',
    'syria': 'Ankara',
    'taiwan': 'Beijing',
    'tajikistan': 'Ankara',
    'tanzania': 'Dar es Salaam',
    'timor-leste': 'Canberra',
    'togo': 'Accra',
    'tonga': 'Canberra',
    'trinidad-and-tobago': 'Washington DC',
    'tunisia': 'Tunis',
    'turkmenistan': 'Ankara',
    'tuvalu': 'Canberra',
    'uganda': 'Nairobi',
    'ukraine': 'Kyiv',
    'united-kingdom': 'London',
    'uruguay': 'Buenos Aires',
    'uzbekistan': 'Ankara',
    'vanuatu': 'Canberra',
    'vatican-city': 'Rome',
    'venezuela': 'Bogota',
    'yemen': 'Cairo',
    'zambia': 'Lusaka',
    'zimbabwe': 'Harare',
}

# Countries where the Irish Embassy is resident in that country's main city
RESIDENT_SAME_CITY = {
    'south-korea',
    'sweden',
    'switzerland',
    'ukraine',
    'united-kingdom',
    'tunisia',
    'tanzania',
    'uganda',
    'zambia',
    'zimbabwe',
}

ORIGIN_NAMES = {
    'hong-kong': 'Hong Kong',
    'south-korea': 'South Korea',
    'sudan': 'Sudan',
    'suriname': 'Suriname',
    'sweden': 'Sweden',
    'switzerland': 'Switzerland',
    'syria': 'Syria',
    'taiwan': 'Taiwan',
    'tajikistan': 'Tajikistan',
    'tanzania': 'Tanzania',
    'timor-leste': 'Timor-Leste',
    'togo': 'Togo',
    'tonga': 'Tonga',
    'trinidad-and-tobago': 'Trinidad and Tobago',
    'tunisia': 'Tunisia',
    'turkmenistan': 'Turkmenistan',
    'tuvalu': 'Tuvalu',
    'uganda': 'Uganda',
    'ukraine': 'Ukraine',
    'united-kingdom': 'United Kingdom',
    'uruguay': 'Uruguay',
    'uzbekistan': 'Uzbekistan',
    'vanuatu': 'Vanuatu',
    'vatican-city': 'Vatican City',
    'venezuela': 'Venezuela',
    'yemen': 'Yemen',
    'zambia': 'Zambia',
    'zimbabwe': 'Zimbabwe',
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
    """Adapt text from UK route to Ireland route."""

    # Embassy references
    text = text.replace(f'British Embassy in {origin_name}', f'Irish Embassy in {ir_city}')
    text = text.replace(f'British High Commission in {origin_name}', f'Irish Embassy in {ir_city}')

    if '(' in uk_city:
        base = uk_city.split('(')[0].strip()
        text = text.replace(f'British Embassy in {base}', f'Irish Embassy in {ir_city}')
        text = text.replace(f'British High Commission in {base}', f'Irish Embassy in {ir_city}')

    text = text.replace(f'British Embassy in {uk_city}', f'Irish Embassy in {ir_city}')
    text = text.replace(f'British High Commission in {uk_city}', f'Irish Embassy in {ir_city}')

    if uk_city and uk_city != ir_city:
        text = text.replace(f'Irish Embassy in {uk_city}', f'Irish Embassy in {ir_city}')
        if '(' in uk_city:
            base = uk_city.split('(')[0].strip()
            text = text.replace(f'Irish Embassy in {base}', f'Irish Embassy in {ir_city}')

    text = text.replace('There is no resident UK Embassy', 'There is no resident Irish Embassy')
    text = text.replace('no resident UK Embassy', 'no resident Irish Embassy')
    text = text.replace('no resident UK embassy', 'no resident Irish Embassy')
    text = text.replace('British Embassy', 'Irish Embassy')
    text = text.replace('British High Commission', 'Irish Embassy')

    # Phone and authority
    text = text.replace('+44 (0)20 7008 5000', '+353 1 408 2000')
    text = text.replace('FCDO 24-hour emergency line', 'Department of Foreign Affairs emergency line')
    text = text.replace('FCDO emergency line', 'Department of Foreign Affairs emergency line')
    text = text.replace('FCDO travel advice for', 'Department of Foreign Affairs travel advice for')
    text = text.replace('FCDO travel advice', 'Department of Foreign Affairs travel advice')
    text = text.replace('FCDO advises', 'Department of Foreign Affairs advises')
    text = text.replace('FCDO', 'Department of Foreign Affairs')
    text = text.replace('gov.uk, 2026', 'gov.ie, 2026')
    text = text.replace('gov.uk', 'gov.ie')

    # Personnel and direction
    text = text.replace('UK funeral director', 'Irish funeral director')
    text = text.replace('United Kingdom funeral director', 'Irish funeral director')
    text = text.replace('UK authorities', 'Irish authorities')
    text = text.replace('British nationals', 'Irish nationals')

    # Coroner
    text = text.replace('coroner for the district', 'Coroner for the district')
    text = text.replace('UK coroner', 'Coroner')

    # Destination country
    text = text.replace('to United Kingdom', 'to Ireland')
    text = text.replace('in United Kingdom', 'in Ireland')
    text = text.replace('the United Kingdom', 'Ireland')
    text = text.replace('United Kingdom', 'Ireland')
    text = text.replace('for UK acceptance', 'for Irish acceptance')
    text = text.replace(' for UK ', ' for Ireland ')
    text = text.replace(' to UK', ' to Ireland')
    text = text.replace(' the UK', ' Ireland')
    text = text.replace(' UK.', ' Ireland.')
    text = text.replace(' UK,', ' Ireland,')
    text = text.replace(' UK ', ' Ireland ')
    text = text.replace('Ireland Ireland', 'Ireland')

    # Timeline step 3: embassy city
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

    # Step 6 artifact
    text = text.replace('cargo terminal at destination', 'Dublin Airport cargo terminal')

    # Consular via patterns
    text = re.sub(
        r'consular assistance is (?:provided )?via [A-Z][A-Za-z\s]+(?:or [A-Z][A-Za-z]+)?',
        f'consular assistance is via {ir_city}',
        text
    )

    return text


def make_dest_reception():
    return (
        "The Irish funeral director takes custody at the cargo terminal. "
        "All documentation must be in certified English translation where required. "
        "The Coroner for the district is notified. "
        "Straightforward cases proceed directly to funeral arrangements."
    )


def make_dest_consular(ir_city, origin_name, is_resident):
    base = "Department of Foreign Affairs emergency line: +353 1 408 2000 (24 hours). "
    if is_resident:
        base += (
            f"The Irish Embassy in {ir_city} can register the death and advise on local "
            "funeral directors. They cannot pay for or arrange repatriation."
        )
    else:
        base += (
            f"The Irish Embassy in {ir_city} covers {origin_name} and can register the "
            "death and advise on documentation. They cannot pay for or arrange repatriation."
        )
    return base


def make_embassy_faq(ir_city, origin_name, is_resident):
    if is_resident:
        question = f"Does the Irish Embassy in {origin_name} help with repatriation?"
        answer = (
            f"The Irish Embassy in {ir_city} can register the death with Irish authorities, "
            f"provide a list of local funeral directors in {origin_name}, and advise on documentation. "
            "They cannot pay for or arrange repatriation. "
            "Department of Foreign Affairs emergency line: +353 1 408 2000."
        )
    else:
        question = f"Is there an Irish Embassy in {origin_name}?"
        answer = (
            f"There is no resident Irish Embassy in {origin_name}. "
            f"Consular matters are handled by the Irish Embassy in {ir_city}. "
            "Call the Department of Foreign Affairs emergency line on +353 1 408 2000 (gov.ie, 2026) "
            "as soon as possible. They can provide a list of local funeral directors and register the "
            "death with Irish authorities."
        )
    return f'  - question: "{question}"\n    answer: "{answer}"'


def make_description(origin_name, timeline_avg, complexity):
    notes = {
        'low': 'A well-documented process.',
        'moderate': 'Specialist support recommended.',
        'moderate-high': 'Complex route; a specialist is essential.',
        'high': 'Specialist help required.',
        'very-high': 'One of the most complex routes. A specialist is essential.',
    }
    note = notes.get(complexity, 'Specialist support recommended.')
    desc = (
        f"Someone has died in {origin_name}. Repatriation to Ireland takes "
        f"{timeline_avg}. {note} Contact us 24/7."
    )
    return desc[:155]


def make_uk_to_ireland():
    """Generate united-kingdom-to-ireland.md from scratch (no UK source file exists)."""
    return """---
title: "United Kingdom to Ireland: Funeral Repatriation Guidance"
description: "Someone has died in the United Kingdom. Repatriation to Ireland takes 3-7 days. A well-documented bilateral route. Contact us 24/7."
origin_key: "united-kingdom"
dest_key: "ie"
origin_name: "United Kingdom"
dest_name: "Ireland"
origin_slug: "united-kingdom"
dest_slug: "ireland"
slug: "united-kingdom-to-ireland"
template_variant: "E"
route_complexity: "low"
timeline_avg: "3-7 days"
timeline_fast: "2-4 days"
timeline_complex: "2-3 weeks"
embassy_city: "London"
doc_processing_time: "1-3 days"
date: 2026-05-01
direct_answer_heading: "Repatriation from the United Kingdom to Ireland: what to expect"
direct_answer_intro: "Repatriation from the United Kingdom to Ireland is one of the most accessible international routes. Both countries share close administrative ties and direct transport links."
direct_answer_points:
  - "Key document: UK death certificate (registered with the local Registrar)"
  - "Documentation takes 1-3 days. A specialist can have the process moving within hours."
  - "Irish Embassy in London can assist with any consular questions. They cannot fund repatriation."
  - "Both road/sea and air transport are options depending on the location of death within the UK."
  - "Irish Coroner is notified on arrival and will confirm release for funeral arrangements."
overview_heading: "What happens after a death in the United Kingdom"
overview_body: "Contact emergency services (999). A doctor certifies the death. The death must be registered with the local Registrar of Births, Deaths and Marriages within 5 days in England and Wales, 8 days in Scotland, and 5 days in Northern Ireland. The Coroner takes jurisdiction when the death is sudden, unattended, or of uncertain cause."
dest_reception: "The Irish funeral director takes custody on arrival. The UK death certificate is accepted by the Irish General Register Office for notification purposes. The Coroner for the district is notified. Straightforward cases proceed directly to funeral arrangements."
dest_consular: "Department of Foreign Affairs emergency line: +353 1 408 2000 (24 hours). The Irish Embassy in London can advise on documentation and register the death with Irish authorities. They cannot pay for or arrange repatriation."
timeline_steps:
  - step: 1
    action: "Immediate steps after death"
    timing: "Day of death. Department of Foreign Affairs 24hr: +353 1 408 2000."
    responsible: "Family or travel insurer"
  - step: 2
    action: "Death registered. UK death certificate obtained from local Registrar."
    timing: "Within 5 days (England, Wales, Northern Ireland) or 8 days (Scotland)."
    responsible: "Family and local Registrar"
  - step: 3
    action: "Irish Embassy London notified."
    timing: "Simultaneous with Step 1. Embassy advises on documentation."
    responsible: "Family or repatriation specialist"
  - step: 4
    action: "Embalming and preparation if required."
    timing: "After body released by Coroner (if applicable)."
    responsible: "Licensed UK funeral director"
  - step: 5
    action: "Export documentation obtained. Transit paperwork prepared."
    timing: "Allow 1-3 days. Cannot begin until death certificate issued."
    responsible: "Repatriation specialist"
  - step: 6
    action: "Transport to Ireland by air cargo or road/sea."
    timing: "Once all documentation is complete. Dublin Airport cargo terminal or direct sea crossing."
    responsible: "Repatriation specialist and carrier"
  - step: 7
    action: "Irish funeral director takes custody. Coroner notified."
    timing: "Within 24 hours of arrival."
    responsible: "Receiving Irish funeral director"
faqs:
  - question: "How long does repatriation from the United Kingdom to Ireland take?"
    answer: "In a straightforward case, repatriation from the United Kingdom to Ireland takes 3 to 7 days. The fastest cases can complete in 2 to 4 days when the Coroner is not involved. Cases where the Coroner takes jurisdiction can take 2 to 3 weeks or longer."
  - question: "What documents are needed for repatriation from the UK to Ireland?"
    answer: "The core documents are: the UK death certificate (certified copy), a letter of authority from the funeral director, and embalming certificate if the body has been embalmed. A certified English translation is not required since both countries use English."
  - question: "Can the body be transported by road and sea instead of by air?"
    answer: "Yes. For deaths in Great Britain, ferry services connect Holyhead, Fishguard, Pembroke, Stranraer, and Cairnryan to Irish ports. Road transport is often used for deaths in Northern Ireland, which shares a land border with the Republic of Ireland. The appropriate method depends on location and circumstances."
  - question: "Does the Irish Embassy in London help with repatriation from the UK?"
    answer: "The Irish Embassy in London can provide guidance on documentation and register the death with Irish authorities. They cannot pay for or arrange repatriation. Call the Department of Foreign Affairs emergency line on +353 1 408 2000 (gov.ie, 2026) for immediate assistance."
  - question: "Is a post-mortem required for Irish nationals who die in the United Kingdom?"
    answer: "A post-mortem is required when the UK Coroner takes jurisdiction. This happens when the death is sudden, unattended, or of uncertain cause. The body cannot leave the UK until the Coroner authorises release."
  - question: "What happens when the body arrives in Ireland?"
    answer: "The Irish funeral director takes custody on arrival. The UK death certificate is accepted for Irish registration purposes. The Coroner for the district is notified. Where the death was straightforward and the Coroner does not intervene, the family can proceed directly to funeral arrangements."
  - question: "Can I bring ashes home from the United Kingdom to Ireland instead?"
    answer: "Yes. Cremation in the United Kingdom is straightforward. Bringing ashes to Ireland is simpler than full body repatriation and does not require special documentation beyond the cremation certificate. Ashes can travel by air as cabin baggage or in checked luggage."
links:
  upward:
    - url: "/repatriation-from-united-kingdom/"
      text: "Full United Kingdom repatriation guide"
    - url: "/guides/death-abroad-united-kingdom/"
      text: "What to do if someone dies in the United Kingdom"
    - url: "/embassy-contacts/united-kingdom/"
      text: "Irish Embassy contacts for the United Kingdom"
    - url: "/contact/"
      text: "Send an enquiry to our team"
  sideways:
    - url: "/routes/ireland-to-united-kingdom/"
      text: "Repatriation from Ireland to the UK"
    - url: "/routes/united-kingdom-to-united-states/"
      text: "Repatriation from United Kingdom to United States"
---
"""


def generate_route(slug, variant_idx):
    if slug == 'united-kingdom':
        return make_uk_to_ireland()

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

    ts_raw = extract_block(uk_fm, 'timeline_steps', ['faqs', 'links'])
    faqs_raw = extract_block(uk_fm, 'faqs', ['links'])

    ts = a(ts_raw)
    faqs = a(faqs_raw)

    embassy_faq = make_embassy_faq(ir_city, origin_name, is_resident)
    faqs = re.sub(
        r'  - question: "Does the (?:British|Irish) Embassy in [^"]*help with repatriation\?"\n    answer: "[^"]*"',
        embassy_faq,
        faqs
    )
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
    'hong-kong',
    'south-korea',
    'sudan',
    'suriname',
    'sweden',
    'switzerland',
    'syria',
    'taiwan',
    'tajikistan',
    'tanzania',
    'timor-leste',
    'togo',
    'tonga',
    'trinidad-and-tobago',
    'tunisia',
    'turkmenistan',
    'tuvalu',
    'uganda',
    'ukraine',
    'united-kingdom',
    'uruguay',
    'uzbekistan',
    'vanuatu',
    'vatican-city',
    'venezuela',
    'yemen',
    'zambia',
    'zimbabwe',
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
