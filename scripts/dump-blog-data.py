import json

d = json.load(open('site/data/countries_repatriation.json', encoding='utf-8'))
targets = ['spain', 'france', 'greece', 'turkey', 'portugal', 'italy', 'india', 'usa']

for k in targets:
    c = d['countries'][k]
    print('=== ' + k + ' ===')
    for field in ['country_name', 'typical_timeline', 'timeline_notes', 'complexity_rating', 'complexity_notes',
                  'required_documents', 'routing_notes', 'no_go_zones', 'risk_highlights', 'religion_notes',
                  'cremation_available', 'cremation_notes', 'british_representation', 'embassy_city', 'main_airports']:
        v = c.get(field, '')
        if v:
            print(f'  {field}: {v}')
    print()
