import json

d = json.load(open('data/countries_repatriation.json', encoding='utf-8'))
sample = ['afghanistan', 'jersey', 'isle-of-man', 'bonaire', 'north-korea', 'russia', 'iran', 'tokelau', 'pitcairn-islands', 'akrotiri-and-dhekelia']
for k in sample:
    c = d['countries'].get(k, {})
    name = c.get('country_name', c.get('name', ''))
    print(f"{k}:")
    print(f"  name={name}")
    print(f"  cremation_available={c.get('cremation_available', '')}")
    print(f"  cremation_notes={c.get('cremation_notes', '')[:80]}")
    print(f"  embassy_type={c.get('embassy_type', '')}")
    print(f"  embassy_city={c.get('embassy_city', '')}")
    print(f"  british_representation={c.get('british_representation', '')[:60]}")
    print()
