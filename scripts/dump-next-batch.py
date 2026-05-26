import json
with open('site/data/countries_repatriation.json', encoding='utf-8') as f:
    data = json.load(f)
countries_data = data.get('countries', data)
targets = ['saudi-arabia', 'oman', 'bahrain', 'nepal', 'tanzania', 'ethiopia']
for key in targets:
    c = countries_data.get(key, {})
    print(f'=== {key} ===')
    print(f'  deaths/yr: {c.get("deaths_per_year_uk_nationals", "N/A")}')
    print(f'  typical_timeline: {c.get("typical_timeline", "N/A")}')
    print(f'  post_mortem: {str(c.get("post_mortem_examination", ""))[:200]}')
    print(f'  cultural: {str(c.get("cultural_practices", ""))[:300]}')
    print(f'  practical: {str(c.get("practical_information", ""))[:300]}')
    print(f'  angles: {str(c.get("content_angles", ""))[:400]}')
    print()
