#!/usr/bin/env python3
"""Add Batch 38 countries to countries_repatriation.json.
Countries: french-polynesia, martinique, guadeloupe, reunion, new-caledonia
All French overseas territories — French civil law, documentation in French,
certified English translation required, routing via Paris CDG (Air France).
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_38 = {
    "french-polynesia": {
        "country_key": "french-polynesia",
        "country_name": "French Polynesia",
        "country_adjective": "French Polynesian",
        "flag": "\U0001f1f5\U0001f1eb",
        "region": "Pacific",
        "languages": "French, Tahitian",
        "currency": "CFP Franc (XPF)",
        "british_representation": "Non-resident — British Embassy, Paris, France",
        "embassy_type": "Non-resident (Embassy Paris)",
        "embassy_city": "Paris",
        "local_authority_involved": "Service de l'État Civil (Civil Registration, Government of French Polynesia); Gendarmerie nationale or Police nationale (non-natural deaths depending on commune)",
        "main_airports": "PPT (Faa'a International Airport, Papeete, Tahiti); outer island airstrips throughout the 5 archipelagos",
        "routing_notes": "Faa'a International Airport (PPT) in Papeete, Tahiti, has direct Air France and Air Tahiti Nui service to Paris Charles de Gaulle (CDG). Flight time approximately 22 hours. All UK repatriation routes via Paris CDG. Deaths on outer islands (Bora Bora, Moorea, Marquesas, Tuamotu, Austral archipelagos) require inter-island Air Tahiti transfer to Papeete first.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 28,
        "timeline_notes": "French Polynesia is an overseas collectivity (collectivité d'outre-mer) of France. French civil law applies. French civil registration via Service de l'État Civil. Documentation in French — certified English translation required. Very remote Pacific location. Outer islands (Marquesas, Tuamotu, Austral) are extremely remote and may have very limited mortuary facilities. Major tourist islands (Tahiti, Bora Bora, Moorea) have better infrastructure.",
        "complexity_rating": "high",
        "complexity_notes": "Extreme distance from UK — approximately 15,700 km. 5 archipelagos spanning a vast area of the Pacific Ocean. Deaths on outer islands require inter-island Air Tahiti transfer. Non-resident British Embassy Paris. All documentation in French — certified English translation required. Very limited mortuary infrastructure outside Papeete. Embalming standards and refrigeration capacity outside Tahiti are constrained.",
        "required_documents": [
            "Acte de décès (death certificate, Service de l'État Civil)",
            "Certified English translation of death certificate",
            "Gendarmerie/Police nationale clearance (non-natural deaths)",
            "Embalming certificate (certificat d'embaumement)",
            "Freedom from infection certificate (certificat de non-contagion)",
            "Export permit (autorisation de sortie du territoire)",
            "Consular registration (British Embassy, Paris)"
        ],
        "religion_notes": "Predominantly Protestant (Mā'ohi Protestant Church) and Catholic. Traditional Polynesian religious practices persist.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Papeete, Tahiti. Cremation may not be available on outer islands. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Extreme remoteness — 15,700 km from UK, routing via Paris CDG",
            "Deaths on outer islands (Marquesas, Tuamotu, Austral) require inter-island Air Tahiti transfer to Papeete",
            "Very limited mortuary infrastructure outside Papeete",
            "Non-resident British Embassy Paris",
            "All documentation in French — certified English translation required"
        ]
    },
    "martinique": {
        "country_key": "martinique",
        "country_name": "Martinique",
        "country_adjective": "Martiniquais",
        "flag": "\U0001f1f2\U0001f1f6",
        "region": "Caribbean",
        "languages": "French, Antillean Creole",
        "currency": "Euro (EUR)",
        "british_representation": "Non-resident — British Embassy, Paris, France",
        "embassy_type": "Non-resident (Embassy Paris)",
        "embassy_city": "Paris",
        "local_authority_involved": "Mairie (municipal civil registry — mairie of the commune of death); Gendarmerie nationale or Police nationale (non-natural deaths)",
        "main_airports": "FDF (Martinique Aimé Césaire International Airport, Le Lamentin)",
        "routing_notes": "Martinique Aimé Césaire Airport (FDF) has direct Air France service to Paris Charles de Gaulle (CDG). Flight time approximately 9 hours. All UK repatriation routes via Paris CDG. No direct UK flights.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Martinique is an overseas region and department (région et département d'outre-mer) of France — legally part of metropolitan France. French civil law applies in full. Death registration via the mairie of the commune where death occurred. Documentation in French. Certified English translation required for UK Coroner.",
        "complexity_rating": "moderate",
        "complexity_notes": "French civil law — same legal system as metropolitan France. Non-resident British Embassy Paris. Documentation in French — certified English translation required. Direct Air France service to Paris CDG. Martinique has an established tourist industry with professional funeral services.",
        "required_documents": [
            "Acte de décès (death certificate, mairie of commune of death)",
            "Certified English translation of death certificate",
            "Gendarmerie/Police nationale clearance (non-natural deaths)",
            "Embalming certificate (certificat d'embaumement)",
            "Freedom from infection certificate (certificat de non-contagion)",
            "Export permit (autorisation de sortie du territoire)",
            "Consular registration (British Embassy, Paris)"
        ],
        "religion_notes": "Predominantly Roman Catholic.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Martinique. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British Embassy Paris",
            "All documentation in French — certified English translation required",
            "No direct UK flights — routing via Paris CDG"
        ]
    },
    "guadeloupe": {
        "country_key": "guadeloupe",
        "country_name": "Guadeloupe",
        "country_adjective": "Guadeloupean",
        "flag": "\U0001f1ec\U0001f1f5",
        "region": "Caribbean",
        "languages": "French, Antillean Creole",
        "currency": "Euro (EUR)",
        "british_representation": "Non-resident — British Embassy, Paris, France",
        "embassy_type": "Non-resident (Embassy Paris)",
        "embassy_city": "Paris",
        "local_authority_involved": "Mairie (municipal civil registry — mairie of the commune of death); Gendarmerie nationale or Police nationale (non-natural deaths)",
        "main_airports": "PTP (Pointe-à-Pitre Les Abymes International Airport, Grande-Terre); outer island airports on Marie-Galante, Les Saintes, La Désirade",
        "routing_notes": "Pointe-à-Pitre Les Abymes Airport (PTP) has direct Air France service to Paris Charles de Gaulle (CDG). Flight time approximately 8.5 hours. All UK repatriation routes via Paris CDG. Deaths on outer islands (Marie-Galante, Les Saintes, La Désirade) require inter-island transfer to Grande-Terre. Saint-Barthélemy and Saint-Martin (French) are separate collectivities — different jurisdictions.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Guadeloupe is an overseas region and department of France — legally part of metropolitan France. French civil law in full. Death registration via the mairie of the commune of death. Documentation in French — certified English translation required for UK Coroner.",
        "complexity_rating": "moderate",
        "complexity_notes": "French civil law — same legal system as metropolitan France. Non-resident British Embassy Paris. Documentation in French — certified English translation required. Direct Air France to Paris CDG. Note: Saint-Barthélemy (St Barts) and Saint-Martin (French side) are separate collectivities — not part of Guadeloupe. Confirm correct jurisdiction.",
        "required_documents": [
            "Acte de décès (death certificate, mairie of commune of death)",
            "Certified English translation of death certificate",
            "Gendarmerie/Police nationale clearance (non-natural deaths)",
            "Embalming certificate (certificat d'embaumement)",
            "Freedom from infection certificate (certificat de non-contagion)",
            "Export permit (autorisation de sortie du territoire)",
            "Consular registration (British Embassy, Paris)"
        ],
        "religion_notes": "Predominantly Roman Catholic.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Guadeloupe. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British Embassy Paris",
            "All documentation in French — certified English translation required",
            "Outer islands (Marie-Galante, Les Saintes, La Désirade) require inter-island transfer",
            "Saint-Barthélemy and Saint-Martin are separate jurisdictions — not Guadeloupe"
        ]
    },
    "reunion": {
        "country_key": "reunion",
        "country_name": "Réunion",
        "country_adjective": "Réunionese",
        "flag": "\U0001f1f7\U0001f1ea",
        "region": "Indian Ocean",
        "languages": "French, Réunion Creole",
        "currency": "Euro (EUR)",
        "british_representation": "Non-resident — British Embassy, Paris, France",
        "embassy_type": "Non-resident (Embassy Paris)",
        "embassy_city": "Paris",
        "local_authority_involved": "Mairie (municipal civil registry — mairie of the commune of death); Gendarmerie nationale or Police nationale (non-natural deaths)",
        "main_airports": "RUN (Roland Garros Airport, Saint-Denis)",
        "routing_notes": "Roland Garros Airport (RUN) in Saint-Denis has direct Air France service to Paris Charles de Gaulle (CDG). Flight time approximately 11 hours. All UK repatriation routes via Paris CDG. No direct UK service.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Réunion is an overseas region and department of France in the Indian Ocean — legally part of metropolitan France. French civil law in full. Death registration via the mairie. Documentation in French. Certified English translation required for UK Coroner. Réunion has a higher shark attack risk coastal zone; the western coast lagoon area is generally safer.",
        "complexity_rating": "moderate",
        "complexity_notes": "French civil law — same legal system as metropolitan France. Non-resident British Embassy Paris. Documentation in French — certified English translation required. Indian Ocean location — somewhat further from UK than French Caribbean. Direct Air France Paris CDG service. Réunion has an active volcano (Piton de la Fournaise) in the south-east — check FCDO travel advice for current activity.",
        "required_documents": [
            "Acte de décès (death certificate, mairie of commune of death)",
            "Certified English translation of death certificate",
            "Gendarmerie/Police nationale clearance (non-natural deaths)",
            "Embalming certificate (certificat d'embaumement)",
            "Freedom from infection certificate (certificat de non-contagion)",
            "Export permit (autorisation de sortie du territoire)",
            "Consular registration (British Embassy, Paris)"
        ],
        "religion_notes": "Predominantly Roman Catholic. Significant Hindu, Muslim, and Buddhist communities reflecting historical indentured labour migration.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Réunion. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "Active volcano zone (Piton de la Fournaise, south-east Réunion) — check FCDO and local prefectural advisories for current restricted areas.",
        "risk_highlights": [
            "Non-resident British Embassy Paris",
            "All documentation in French — certified English translation required",
            "Active volcano (Piton de la Fournaise) — restricted zones possible in south-east",
            "Shark attack risk on unprotected coastal beaches",
            "Indian Ocean distance — routing via Paris CDG approximately 11 hours"
        ]
    },
    "new-caledonia": {
        "country_key": "new-caledonia",
        "country_name": "New Caledonia",
        "country_adjective": "New Caledonian",
        "flag": "\U0001f1f3\U0001f1e8",
        "region": "Pacific",
        "languages": "French, Kanak languages",
        "currency": "CFP Franc (XPF)",
        "british_representation": "Non-resident — British Embassy, Paris, France",
        "embassy_type": "Non-resident (Embassy Paris)",
        "embassy_city": "Paris",
        "local_authority_involved": "Service de l'État Civil (Civil Registration); Gendarmerie nationale or Police nationale (non-natural deaths). New Caledonia has a special status — a sui generis collectivity with its own government (Gouvernement de la Nouvelle-Calédonie).",
        "main_airports": "NOU/GEA (La Tontouta International Airport, Nouméa); Magenta Airport (GEA) for domestic flights",
        "routing_notes": "La Tontouta International Airport (NOU) near Nouméa has direct Air France and Air Calédonie International (Aircalin) service to Paris Charles de Gaulle (CDG). Also connections to Sydney (SYD) and Auckland (AKL). UK routing via Paris CDG is primary. Sydney routing provides an alternative via London connections.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 28,
        "timeline_notes": "New Caledonia is a special collectivity (collectivité sui generis) of France in the South Pacific. French civil law applies, administered through its own government. Documentation in French. Remote Pacific location — approximately 18,900 km from UK. Political situation: New Caledonia held three independence referendums (2018, 2020, 2021) — all returned votes to remain part of France. Civil unrest has occurred; check FCDO advice for current situation.",
        "complexity_rating": "high",
        "complexity_notes": "Remote Pacific location — approximately 18,900 km from UK. Non-resident British Embassy Paris. Documentation in French — certified English translation required. New Caledonia has a complex political situation regarding independence, with periods of civil unrest. Outer islands (Loyalty Islands, Isle of Pines) require inter-island Air Calédonie transfer to Nouméa. Mining and industrial sector means some expat workers present.",
        "required_documents": [
            "Acte de décès (death certificate, Service de l'État Civil)",
            "Certified English translation of death certificate",
            "Gendarmerie/Police nationale clearance (non-natural deaths)",
            "Embalming certificate (certificat d'embaumement)",
            "Freedom from infection certificate (certificat de non-contagion)",
            "Export permit (autorisation de sortie du territoire)",
            "Consular registration (British Embassy, Paris)"
        ],
        "religion_notes": "Predominantly Roman Catholic. Significant Protestant minority (mainly Kanak community). Traditional Kanak spiritual practices.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Nouméa. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Remote Pacific location — approximately 18,900 km from UK",
            "Non-resident British Embassy Paris",
            "Political tension over independence — periods of civil unrest; check FCDO advice",
            "Outer islands (Loyalty Islands, Isle of Pines) require inter-island transfer to Nouméa",
            "All documentation in French — certified English translation required"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_38.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
