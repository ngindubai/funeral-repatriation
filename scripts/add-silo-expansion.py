"""
Silo expansion: generate cremation-transfer, bringing-ashes-home, and embassy-contacts
pages for all countries in countries_repatriation.json that do not yet have a page.
Run from funeral-repatriation/ root.
"""
import json
import os

SITE_ROOT = os.path.join(os.path.dirname(__file__), '..', 'site')
JSON_PATH = os.path.join(SITE_ROOT, 'data', 'countries_repatriation.json')

CREMATION_DIR = os.path.join(SITE_ROOT, 'content', 'cremation-transfer')
ASHES_DIR     = os.path.join(SITE_ROOT, 'content', 'bringing-ashes-home')
EMBASSY_DIR   = os.path.join(SITE_ROOT, 'content', 'embassy-contacts')

with open(JSON_PATH, encoding='utf-8') as f:
    data = json.load(f)

countries = data['countries']

# Existing pages (by country key / slug, excluding _index)
def existing_slugs(directory):
    return {
        os.path.splitext(fn)[0]
        for fn in os.listdir(directory)
        if fn.endswith('.md') and fn != '_index.md'
    }

existing_cremation = existing_slugs(CREMATION_DIR)
existing_ashes     = existing_slugs(ASHES_DIR)
existing_embassy   = existing_slugs(EMBASSY_DIR)

def truncate(s, max_len=155):
    """Truncate string to max_len, ending at a word boundary."""
    if len(s) <= max_len:
        return s
    trimmed = s[:max_len].rsplit(' ', 1)[0]
    return trimmed.rstrip('.,;') + '.'

def country_name(c):
    return c.get('country_name') or c.get('name', '')

def make_cremation_title(c):
    name = country_name(c)
    cremation = c.get('cremation_available')
    if cremation is False or str(cremation).lower() in ('false', 'no'):
        return f"No Cremation in {name}: Body Repatriation to the UK"
    return f"Cremation Transfer from {name} to the UK"

def make_cremation_desc(c):
    name = country_name(c)
    cremation = c.get('cremation_available')
    notes = (c.get('cremation_notes') or '').strip()
    # Use first sentence from notes if available
    first_sentence = notes.split('.')[0].strip() if notes else ''

    if cremation is False or str(cremation).lower() in ('false', 'no'):
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. Full body repatriation to the UK is required. Contact us for specialist guidance."
        else:
            base = f"Cremation is not available in {name}. Full body repatriation to the UK is required. Contact us for specialist guidance on documentation and logistics."
    elif str(cremation).lower() in ('limited',):
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. Contact us for guidance on cremation transfer from {name} to the UK, including documentation requirements."
        else:
            base = f"Limited cremation facilities in {name}. Guidance on arranging cremation and transferring ashes to the UK, including documentation requirements."
    else:
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. Guidance on documentation, packaging requirements, and routing ashes to the UK."
        else:
            base = f"Arranging cremation in {name} and transferring ashes to the UK. Documentation, packaging requirements, and routing options explained."
    return truncate(base)

def make_ashes_title(c):
    name = country_name(c)
    return f"Bringing Ashes Home from {name} to the UK"

def make_ashes_desc(c):
    name = country_name(c)
    cremation = c.get('cremation_available')
    notes = (c.get('cremation_notes') or '').strip()
    first_sentence = notes.split('.')[0].strip() if notes else ''

    if cremation is False or str(cremation).lower() in ('false', 'no'):
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. If your loved one was cremated in a third country before transfer, we can help bring ashes to the UK."
        else:
            base = f"Cremation is not available in {name}. If remains were cremated elsewhere before UK return, we can help transport ashes home from the transfer point."
    else:
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. Guidance on bringing cremated remains home from {name}, including airline rules and UK import documentation."
        else:
            base = f"How to bring cremated remains home from {name} to the UK. Documentation, packaging requirements, airline rules, and what to expect at UK customs."
    return truncate(base)

def make_embassy_title(c):
    name = country_name(c)
    etype = (c.get('embassy_type') or '').lower()
    ecity = (c.get('embassy_city') or '').strip()

    if 'crown dependency' in etype:
        return f"{name}: Consular Contacts and Repatriation Guidance"
    if 'sovereign base area' in etype:
        return f"{name}: Consular Contacts for UK Families"
    if "governor" in etype:
        return f"Governor's Office {name}: Contacts for UK Families"
    if 'high commission' in etype:
        loc = ecity or name
        return f"British High Commission {name}: Consular Contacts for Repatriation"
    # Default: Embassy (resident or non-resident)
    return f"British Embassy {name}: Contact Details for Repatriation"

def make_embassy_desc(c):
    name = country_name(c)
    etype = (c.get('embassy_type') or '').strip()
    brit_rep = (c.get('british_representation') or '').strip()
    ecity = (c.get('embassy_city') or '').strip()

    # Use first sentence of british_representation
    first = brit_rep.split('.')[0].strip() if brit_rep else ''

    etype_lower = etype.lower()
    if 'crown dependency' in etype_lower:
        base = f"{name} is a UK Crown Dependency. FCDO consular support is not provided. The Lieutenant Governor handles UK Crown matters on island."
    elif 'sovereign base area' in etype_lower:
        base = f"{name} is a UK Sovereign Base Area. Deaths are handled by the SBA Administration. Contact us for specialist guidance on documentation and repatriation."
    elif 'governor' in etype_lower:
        base = f"The Governor of the {name} is based in {ecity}. Contact information and guidance on consular support for UK nationals who die in {name}."
    elif first and len(first) > 20:
        base = f"{first}. Contact details, consular services, and guidance on what the Embassy can and cannot do to assist with repatriation from {name}."
    else:
        base = f"British consular contact details for UK families dealing with a death in {name}. Emergency line, opening hours, and repatriation guidance."
    return truncate(base)


cremation_created = 0
ashes_created = 0
embassy_created = 0

for key, c in countries.items():
    name = country_name(c)
    if not name:
        print(f"SKIP {key}: no country name")
        continue

    # --- cremation-transfer ---
    if key not in existing_cremation:
        title = make_cremation_title(c)
        desc  = make_cremation_desc(c)
        content = f"""---
title: "{title}"
description: "{desc}"
country_key: "{key}"
slug: "{key}"
layout: "cremation-transfer"
date: 2026-05-06
---
"""
        path = os.path.join(CREMATION_DIR, f"{key}.md")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        cremation_created += 1

    # --- bringing-ashes-home ---
    if key not in existing_ashes:
        title = make_ashes_title(c)
        desc  = make_ashes_desc(c)
        content = f"""---
title: "{title}"
description: "{desc}"
country_key: "{key}"
slug: "{key}"
layout: "bringing-ashes-home"
date: 2026-05-06
---
"""
        path = os.path.join(ASHES_DIR, f"{key}.md")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        ashes_created += 1

    # --- embassy-contacts ---
    if key not in existing_embassy:
        title = make_embassy_title(c)
        desc  = make_embassy_desc(c)
        content = f"""---
title: "{title}"
description: "{desc}"
country_key: "{key}"
slug: "{key}"
layout: "embassy-contacts"
date: 2026-05-06
---
"""
        path = os.path.join(EMBASSY_DIR, f"{key}.md")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        embassy_created += 1

total = cremation_created + ashes_created + embassy_created
print(f"Created {cremation_created} cremation-transfer pages")
print(f"Created {ashes_created} bringing-ashes-home pages")
print(f"Created {embassy_created} embassy-contacts pages")
print(f"Total new pages: {total}")
