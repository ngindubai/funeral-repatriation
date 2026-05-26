#!/usr/bin/env python3
"""Add Batch 33 countries to countries_repatriation.json.
Countries: cuba (already in), wait - need to check. Let me pick:
  - east-timor (already as timor-leste)
Countries: maldives (already in)
Actual batch: papua-new-guinea (already in)

Candidates: swaziland=eswatini (already in)
Fresh picks: democratic-republic-of-congo (already in)

Let me pick: dominica, haiti (already in)...

Fresh: dominica, palau, micronesia, marshall-islands, nauru
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_33 = {
    "dominica": {
        "country_key": "dominica",
        "country_name": "Dominica",
        "country_adjective": "Dominican",
        "flag": "\U0001f1e9\U0001f1f2",
        "region": "Caribbean",
        "languages": "English",
        "currency": "East Caribbean Dollar (XCD)",
        "british_representation": "Non-resident — British High Commission, Bridgetown, Barbados",
        "embassy_type": "Non-resident (BHC Bridgetown)",
        "embassy_city": "Bridgetown",
        "local_authority_involved": "Registrar General's Office, Coroner's Court (unnatural deaths)",
        "main_airports": "DOM (Douglas-Charles Airport, Dominica)",
        "routing_notes": "Via Antigua (ANU — V.C. Bird International) or Barbados (BGI), then to UK. Caribbean Airlines, LIAT, and charter services. No direct UK flights.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "English common law. Commonwealth documentation. Remote mountain terrain means deaths in the interior may require difficult ground transport to Douglas-Charles Airport.",
        "complexity_rating": "moderate",
        "complexity_notes": "Non-resident BHC Bridgetown. English common law. Dominica's interior is rugged volcanic terrain — deaths away from Roseau may require challenging ground transport. Douglas-Charles Airport has limited runway length, restricting aircraft types.",
        "required_documents": [
            "Death certificate (Registrar General's Office)",
            "Coroner's certificate (unnatural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (BHC Bridgetown)"
        ],
        "religion_notes": "Predominantly Christian. Roman Catholic majority, with Protestant denominations.",
        "cremation_available": False,
        "cremation_notes": "Cremation is not available in Dominica. Full body repatriation to the UK is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Bridgetown",
            "Rugged interior terrain — ground transport to airport may be difficult",
            "Douglas-Charles Airport has restricted aircraft capacity"
        ]
    },
    "palau": {
        "country_key": "palau",
        "country_name": "Palau",
        "country_adjective": "Palauan",
        "flag": "\U0001f1f5\U0001f1fc",
        "region": "Pacific",
        "languages": "Palauan, English",
        "currency": "US Dollar (USD)",
        "british_representation": "Non-resident — British Embassy, Manila, Philippines",
        "embassy_type": "Non-resident (Embassy Manila)",
        "embassy_city": "Manila",
        "local_authority_involved": "Bureau of Vital Statistics (Palau), Palau Police Department",
        "main_airports": "ROR (Roman Tmetuchl International, Koror/Babeldaob)",
        "routing_notes": "Via Manila (Philippines Airlines/United), via Guam (United Airlines), then to UK. No direct Pacific–UK flights. Multi-hop routing.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "Very remote Pacific island nation. Non-resident embassy in Manila. US-administered trust territory until 1994 — US influence on documentation. Very limited mortuary infrastructure.",
        "complexity_rating": "high",
        "complexity_notes": "Extremely remote. Non-resident British Embassy Manila. Limited mortuary infrastructure. Multi-hop routing via Manila or Guam. Very few British nationals visit Palau; any repatriation case is specialist.",
        "required_documents": [
            "Death certificate (Bureau of Vital Statistics)",
            "Palau Police Department clearance (non-natural deaths)",
            "Embalming certificate (limited local capacity)",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (British Embassy, Manila)"
        ],
        "religion_notes": "Predominantly Christian. Catholic and Protestant denominations.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Palau. Full body repatriation to the UK is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — Embassy Manila",
            "Extremely remote Pacific location — multi-hop routing required",
            "Very limited mortuary infrastructure"
        ]
    },
    "micronesia": {
        "country_key": "micronesia",
        "country_name": "Micronesia",
        "country_adjective": "Micronesian",
        "flag": "\U0001f1eb\U0001f1f2",
        "region": "Pacific",
        "languages": "English",
        "currency": "US Dollar (USD)",
        "british_representation": "Non-resident — British Embassy, Manila, Philippines",
        "embassy_type": "Non-resident (Embassy Manila)",
        "embassy_city": "Manila",
        "local_authority_involved": "Department of Health (state vital statistics offices for each FSM state), Police Department",
        "main_airports": "PNI (Pohnpei International), TKK (Chuuk International), KSA (Kosrae), YAP (Yap International)",
        "routing_notes": "Via Guam (United Airlines Micronesia Island Hopper), then onward to Manila or Tokyo for UK connections. Island hopper routing only.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 21,
        "typical_timeline_days_max": 56,
        "timeline_notes": "Federated States of Micronesia spans four states across 2,600 km of Pacific Ocean. Inter-island routing only via Guam. Extremely remote. Death on outer islands may require internal transfer before international repatriation.",
        "complexity_rating": "high",
        "complexity_notes": "FSM comprises four main island groups (Yap, Chuuk, Pohnpei, Kosrae) spread across 2,600 km. United Airlines Island Hopper is the only regular routing. Non-resident British Embassy Manila. Very limited mortuary infrastructure across all states. Deaths on outer islands require internal transfer.",
        "required_documents": [
            "Death certificate (state vital statistics office for relevant FSM state)",
            "Police clearance (non-natural deaths)",
            "Embalming certificate (limited local capacity)",
            "Export permit",
            "Consular registration (British Embassy, Manila)"
        ],
        "religion_notes": "Predominantly Christian. Catholic and Protestant denominations.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in FSM. Full body repatriation to the UK is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — Embassy Manila",
            "Extremely remote Pacific archipelago spanning 2,600 km",
            "Island Hopper via Guam only routing — very limited frequency",
            "Very limited mortuary infrastructure"
        ]
    },
    "marshall-islands": {
        "country_key": "marshall-islands",
        "country_name": "Marshall Islands",
        "country_adjective": "Marshallese",
        "flag": "\U0001f1f2\U0001f1ed",
        "region": "Pacific",
        "languages": "Marshallese, English",
        "currency": "US Dollar (USD)",
        "british_representation": "Non-resident — British Embassy, Manila, Philippines",
        "embassy_type": "Non-resident (Embassy Manila)",
        "embassy_city": "Manila",
        "local_authority_involved": "Vital Statistics Office (Republic of Marshall Islands), RMI Police Department",
        "main_airports": "MAJ (Amata Kabua International, Majuro)",
        "routing_notes": "Via Honolulu (Hawaii, United Airlines), then to UK via Los Angeles or New York. Very limited service. United also serves Majuro via the Island Hopper from Guam.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 21,
        "typical_timeline_days_max": 56,
        "timeline_notes": "Extremely remote atoll nation in the central Pacific. Very limited air connections via Honolulu or Guam. Deaths on outer atolls require internal inter-island transfer to Majuro, which itself may take days.",
        "complexity_rating": "high",
        "complexity_notes": "29 atolls and 5 isolated islands spread over 1.9 million km² of ocean. Air access only via Majuro or Kwajalein. Deaths on outer atolls require boat or light aircraft transfer to Majuro. Non-resident British Embassy Manila. Very limited mortuary infrastructure.",
        "required_documents": [
            "Death certificate (Vital Statistics Office, RMI)",
            "RMI Police clearance (non-natural deaths)",
            "Embalming certificate (limited local capacity)",
            "Export permit",
            "Consular registration (British Embassy, Manila)"
        ],
        "religion_notes": "Predominantly Protestant Christian.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Marshall Islands. Full body repatriation to the UK is required.",
        "no_go_zones": "Kwajalein Atoll is a US military installation — access restricted.",
        "risk_highlights": [
            "Non-resident British representation — Embassy Manila",
            "29 atolls across 1.9 million km² of ocean",
            "Deaths on outer atolls require boat or light aircraft transfer to Majuro",
            "Air access only via Honolulu or Guam — very limited frequency"
        ]
    },
    "nauru": {
        "country_key": "nauru",
        "country_name": "Nauru",
        "country_adjective": "Nauruan",
        "flag": "\U0001f1f3\U0001f1f7",
        "region": "Pacific",
        "languages": "Nauruan, English",
        "currency": "Australian Dollar (AUD)",
        "british_representation": "Non-resident — British High Commission, Suva, Fiji",
        "embassy_type": "Non-resident (BHC Suva)",
        "embassy_city": "Suva",
        "local_authority_involved": "Nauru Vital Statistics Registry, Nauru Police Force",
        "main_airports": "INU (Nauru International Airport)",
        "routing_notes": "Nauru Airlines operates Nauru to Brisbane (Australia) and Nauru to Honiara/Tarawa. Via Brisbane for international connections to UK.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "World's smallest island nation state (21 km²). Non-resident BHC Suva. Nauru Airlines is the only carrier. Very limited mortuary infrastructure. High prevalence of medical tourism to Fiji or Australia for complex cases.",
        "complexity_rating": "high",
        "complexity_notes": "World's smallest island state by area (21 km²). Population approximately 10,000. Non-resident BHC Suva. Only one airline serves Nauru. No significant medical or mortuary infrastructure. All serious cases historically evacuated to Australia or Fiji.",
        "required_documents": [
            "Death certificate (Nauru Vital Statistics Registry)",
            "Nauru Police Force clearance (non-natural deaths)",
            "Embalming certificate (very limited local capacity)",
            "Export permit",
            "Consular registration (BHC Suva)"
        ],
        "religion_notes": "Predominantly Protestant Christian. Nauru Congregational Church is the majority denomination.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Nauru. Full body repatriation via Australia is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Suva, Fiji",
            "Only one airline serves Nauru (Nauru Airlines)",
            "World's smallest island state — very limited infrastructure",
            "Routing only via Brisbane, Australia"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_33.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
