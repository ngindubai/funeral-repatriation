"""
Patch script: fix badly truncated descriptions in the 3 silos.
Re-generates descriptions using sentence-boundary truncation and improved templates.
Run from funeral-repatriation/ root.
"""
import json, os, re

SITE_ROOT = os.path.join(os.path.dirname(__file__), '..', 'site')
JSON_PATH = os.path.join(SITE_ROOT, 'data', 'countries_repatriation.json')

CREMATION_DIR = os.path.join(SITE_ROOT, 'content', 'cremation-transfer')
ASHES_DIR     = os.path.join(SITE_ROOT, 'content', 'bringing-ashes-home')
EMBASSY_DIR   = os.path.join(SITE_ROOT, 'content', 'embassy-contacts')

with open(JSON_PATH, encoding='utf-8') as f:
    data = json.load(f)
countries = data['countries']

BAD_ENDINGS = {'and', 'the', 'to', 'of', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'with', 'from', 'or'}

def is_bad(desc):
    last_word = desc.rstrip('.').rsplit(' ', 1)[-1].lower() if ' ' in desc else ''
    return last_word in BAD_ENDINGS

def truncate(s, max_len=160):
    """Truncate at sentence boundary, then word boundary as fallback."""
    if len(s) <= max_len:
        return s
    parts = re.split(r'(?<=[.!?])\s+', s.strip())
    result = ''
    for part in parts:
        candidate = (result + ' ' + part).strip() if result else part
        if len(candidate) <= max_len:
            result = candidate
        else:
            break
    if result:
        return result
    trimmed = s[:max_len].rsplit(' ', 1)[0]
    return trimmed.rstrip('.,;') + '.'

def country_name(c):
    return c.get('country_name') or c.get('name', '')

def make_cremation_desc(c):
    name = country_name(c)
    cremation = c.get('cremation_available')
    notes = (c.get('cremation_notes') or '').strip()
    first_sentence = notes.split('.')[0].strip() if notes else ''

    if cremation is False or str(cremation).lower() in ('false', 'no'):
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. Full body repatriation to the UK is required. Contact us for specialist guidance."
        else:
            base = f"Cremation is not available in {name}. Full body repatriation to the UK is required. Expert guidance on documentation and logistics."
    elif str(cremation).lower() in ('limited',):
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. Guidance on cremation transfer and documentation requirements for {name} to the UK."
        else:
            base = f"Limited cremation facilities in {name}. Guidance on arranging cremation and transferring ashes to the UK."
    else:
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. Documentation, packaging requirements, and routing ashes to the UK."
        else:
            base = f"Arranging cremation in {name} and transferring ashes to the UK. Documentation, packaging requirements, and routing options explained."
    return truncate(base)

def make_ashes_desc(c):
    name = country_name(c)
    cremation = c.get('cremation_available')
    notes = (c.get('cremation_notes') or '').strip()
    first_sentence = notes.split('.')[0].strip() if notes else ''

    if cremation is False or str(cremation).lower() in ('false', 'no'):
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. If cremated in a third country before transfer, we can help bring ashes to the UK."
        else:
            base = f"Cremation is not available in {name}. If remains were cremated at a third country before UK return, we can help transport ashes home."
    else:
        if first_sentence and len(first_sentence) > 20:
            base = f"{first_sentence}. How to bring cremated remains home from {name}, including airline rules and UK customs."
        else:
            base = f"How to bring cremated remains home from {name} to the UK. Documentation, packaging requirements, airline rules, and UK import guidance."
    return truncate(base)

def make_embassy_desc(c):
    name = country_name(c)
    etype = (c.get('embassy_type') or '').strip()
    brit_rep = (c.get('british_representation') or '').strip()
    ecity = (c.get('embassy_city') or '').strip()
    etype_lower = etype.lower()

    if 'crown dependency' in etype_lower:
        return f"{name} is a UK Crown Dependency. FCDO consular support is not provided. The Lieutenant Governor handles UK Crown matters on island."
    if 'sovereign base area' in etype_lower:
        return f"{name} is a UK Sovereign Base Area. Deaths are handled by the SBA Administration. Expert guidance on documentation and repatriation."
    if 'governor' in etype_lower:
        return f"The Governor of {name} is based in {ecity}. Contact information and consular guidance for UK nationals who die in {name}."

    first = brit_rep.split('.')[0].strip() if brit_rep else ''
    if first and len(first) > 20:
        candidate = f"{first}. Contact details and consular guidance for UK families dealing with a death in {name}."
        if len(candidate) <= 160:
            return candidate
        # Too long — use just a shorter form
        return truncate(f"{first}. Contact details for repatriation from {name}.")

    return f"British consular contact details and guidance for UK families dealing with a death in {name}. Emergency line, opening hours, and repatriation advice."

def fix_silo(directory, silo_name, desc_fn):
    fixed = 0
    for fn in os.listdir(directory):
        if not fn.endswith('.md') or fn == '_index.md':
            continue
        path = os.path.join(directory, fn)
        content = open(path, encoding='utf-8').read()
        m = re.search(r'description: "(.+?)"', content)
        if not m:
            continue
        desc = m.group(1)
        if not is_bad(desc):
            continue
        # Find country key
        km = re.search(r'country_key: "(.+?)"', content)
        if not km:
            continue
        key = km.group(1)
        c = countries.get(key)
        if not c:
            print(f"  WARNING: no JSON data for {key}")
            continue
        new_desc = desc_fn(c)
        new_content = content.replace(f'description: "{desc}"', f'description: "{new_desc}"', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1
    print(f"{silo_name}: fixed {fixed} descriptions")
    return fixed

fix_silo(CREMATION_DIR, "cremation-transfer", make_cremation_desc)
fix_silo(ASHES_DIR,     "bringing-ashes-home", make_ashes_desc)
fix_silo(EMBASSY_DIR,   "embassy-contacts",    make_embassy_desc)

print("Done.")
