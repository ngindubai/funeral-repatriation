#!/usr/bin/env python3
"""Add Batch 37 countries to countries_repatriation.json.
Countries: bermuda, british-virgin-islands, anguilla, montserrat, sint-maarten
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_37 = {
    "bermuda": {
        "country_key": "bermuda",
        "country_name": "Bermuda",
        "country_adjective": "Bermudian",
        "flag": "\U0001f1e7\U0001f1f2",
        "region": "North Atlantic",
        "languages": "English",
        "currency": "Bermudian Dollar (BMD)",
        "british_representation": "Governor's Office (British Overseas Territory) — Governor represents the Crown. Consular functions via FCO London.",
        "embassy_type": "British Overseas Territory (Governor's Office)",
        "embassy_city": "Hamilton",
        "local_authority_involved": "Registrar General's Office (Civil Registration, Government of Bermuda); Bermuda Police Service",
        "main_airports": "BDA (L.F. Wade International Airport, St George's Parish)",
        "routing_notes": "L.F. Wade International Airport (BDA) has direct British Airways service to London Gatwick (LGW). Also direct flights to New York, Boston, Toronto, and other US/Canadian cities. Direct UK routing available year-round.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 14,
        "timeline_notes": "British Overseas Territory. English common law. English language throughout. Direct British Airways service to London Gatwick. Bermuda is a well-developed financial and tourist centre with professional funeral and mortuary services.",
        "complexity_rating": "low",
        "complexity_notes": "British Overseas Territory — English common law, English language, direct UK BA flights available. Registrar General's Office handles civil registration. Bermuda Police Service handles non-natural deaths. Well-developed professional services infrastructure.",
        "required_documents": [
            "Death certificate (Registrar General's Office, Government of Bermuda)",
            "Bermuda Police Service clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "FCO / UK Coroner notification"
        ],
        "religion_notes": "Predominantly Protestant Christian. Anglican is the largest denomination, with significant Catholic and other Christian communities.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Bermuda. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "British Overseas Territory — all documentation in English",
            "Direct British Airways service from Bermuda (BDA) to London Gatwick (LGW)",
            "Well-developed financial centre with professional mortuary services"
        ]
    },
    "british-virgin-islands": {
        "country_key": "british-virgin-islands",
        "country_name": "British Virgin Islands",
        "country_adjective": "Virgin Islander",
        "flag": "\U0001f1fb\U0001f1ec",
        "region": "Caribbean",
        "languages": "English",
        "currency": "United States Dollar (USD)",
        "british_representation": "Governor's Office (British Overseas Territory) — Governor represents the Crown. Consular functions via FCO London.",
        "embassy_type": "British Overseas Territory (Governor's Office)",
        "embassy_city": "Road Town (Tortola)",
        "local_authority_involved": "Civil Registry and Passport Office (Civil Registration, BVI Government); Royal Virgin Islands Police Force",
        "main_airports": "EIS (Terrance B. Lettsome International Airport, Beef Island, Tortola), VIJ (Virgin Gorda Airport)",
        "routing_notes": "Terrance B. Lettsome Airport (EIS) on Beef Island near Tortola has connections to Antigua (ANU), San Juan (SJU, Puerto Rico), and other Caribbean hubs. No direct UK service. Most practical UK routing via Antigua (direct BA/LIAT to London Gatwick) or via Miami/New York.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "British Overseas Territory. English common law. English language throughout. No direct UK flights — routing via Antigua or US hubs. BVI is a well-known sailing and tourist destination with basic funeral services, though mortuary infrastructure is more limited than larger territories.",
        "complexity_rating": "moderate",
        "complexity_notes": "British Overseas Territory — English common law, English language. No direct UK flights — routing via Antigua (for BA London connection) or US hub. Outer islands (Virgin Gorda, Jost Van Dyke, Anegada) require inter-island water taxi or light aircraft transfer to Tortola. Deaths in USVI across the Drake Passage do not fall under BVI jurisdiction.",
        "required_documents": [
            "Death certificate (Civil Registry and Passport Office, BVI Government)",
            "Royal Virgin Islands Police Force clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "FCO / UK Coroner notification"
        ],
        "religion_notes": "Predominantly Protestant Christian. Methodist, Anglican, and Baptist denominations are significant.",
        "cremation_available": False,
        "cremation_notes": "Cremation facilities are not available in the BVI. Full body repatriation to the UK is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "No direct UK flights — routing via Antigua or US hub required",
            "Deaths on outer islands (Virgin Gorda, Jost Van Dyke, Anegada) require inter-island transfer to Tortola",
            "No cremation facilities in BVI",
            "British Overseas Territory — all documentation in English"
        ]
    },
    "anguilla": {
        "country_key": "anguilla",
        "country_name": "Anguilla",
        "country_adjective": "Anguillian",
        "flag": "\U0001f1e6\U0001f1ee",
        "region": "Caribbean",
        "languages": "English",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "british_representation": "Governor's Office (British Overseas Territory) — Governor represents the Crown. Consular functions via FCO London.",
        "embassy_type": "British Overseas Territory (Governor's Office)",
        "embassy_city": "The Valley",
        "local_authority_involved": "Registrar's Office (Civil Registration, Government of Anguilla); Royal Anguilla Police Force",
        "main_airports": "AXA (Clayton J. Lloyd International Airport, The Valley); connections via St Maarten (SXM) or Antigua (ANU)",
        "routing_notes": "Clayton J. Lloyd Airport (AXA) has limited regional service. Most travellers connect via Princess Juliana Airport, Sint Maarten (SXM) by air shuttle (10 minutes) or via Antigua (ANU). UK routing via Antigua (direct BA to LGW) or via SXM to Amsterdam. A short ferry also connects to St Maarten.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "British Overseas Territory. English common law. English language throughout. Small island — no direct UK flights. Routing via Sint Maarten or Antigua. Anguilla is a luxury tourism destination with limited funeral and mortuary infrastructure.",
        "complexity_rating": "moderate",
        "complexity_notes": "British Overseas Territory — English common law, English language. Small island with limited mortuary infrastructure. No direct UK flights. Routing requires connection through Sint Maarten (SXM) or Antigua (ANU). The ferry to Sint Maarten (French/Dutch side) is an alternative routing option.",
        "required_documents": [
            "Death certificate (Registrar's Office, Government of Anguilla)",
            "Royal Anguilla Police Force clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "FCO / UK Coroner notification"
        ],
        "religion_notes": "Predominantly Protestant Christian. Anglican and Methodist denominations are predominant.",
        "cremation_available": False,
        "cremation_notes": "Cremation facilities are not available in Anguilla. Full body repatriation to the UK is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "No direct UK flights — routing via Sint Maarten or Antigua required",
            "Limited mortuary infrastructure on small island",
            "No cremation facilities in Anguilla",
            "British Overseas Territory — all documentation in English"
        ]
    },
    "montserrat": {
        "country_key": "montserrat",
        "country_name": "Montserrat",
        "country_adjective": "Montserratian",
        "flag": "\U0001f1f2\U0001f1f8",
        "region": "Caribbean",
        "languages": "English",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "british_representation": "Governor's Office (British Overseas Territory) — Governor represents the Crown. Consular functions via FCO London.",
        "embassy_type": "British Overseas Territory (Governor's Office)",
        "embassy_city": "Brades (de facto capital; Plymouth is the official capital but was buried by the 1997 Soufrière Hills eruption)",
        "local_authority_involved": "Registrar General's Office (Civil Registration, Government of Montserrat); Royal Montserrat Police Force",
        "main_airports": "MNI (John A. Osborne Airport, Brades); connections via Antigua (ANU)",
        "routing_notes": "John A. Osborne Airport (MNI) has limited capacity — ATR turboprop service only to Antigua (ANU) via regional airlines. No jet service to Montserrat. All UK routing goes via Antigua (direct BA to London Gatwick). The southern half of the island (Exclusion Zone) remains off-limits due to the Soufrière Hills volcano.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 28,
        "timeline_notes": "British Overseas Territory. English common law. English language throughout. Very small population (~5,000). Limited funeral and mortuary infrastructure. All routing goes via Antigua. The Soufrière Hills Exclusion Zone covers the southern third of the island including the former capital Plymouth.",
        "complexity_rating": "moderate",
        "complexity_notes": "British Overseas Territory — English common law, English language. Very limited local mortuary capacity. No direct UK flights — small turboprop only to Antigua, then BA to London. Soufrière Hills Exclusion Zone still active — the southern part of the island is inaccessible. Funeral services have limited capacity. Mortuary refrigeration capacity is constrained.",
        "required_documents": [
            "Death certificate (Registrar General's Office, Government of Montserrat)",
            "Royal Montserrat Police Force clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "FCO / UK Coroner notification"
        ],
        "religion_notes": "Predominantly Protestant Christian. Anglican and Methodist denominations are predominant. Significant Catholic minority.",
        "cremation_available": False,
        "cremation_notes": "Cremation facilities are not available in Montserrat. Full body repatriation to the UK is required.",
        "no_go_zones": "Soufrière Hills Exclusion Zone — southern third of island including former capital Plymouth. Zone boundaries subject to change; check MVO (Montserrat Volcano Observatory) bulletins.",
        "risk_highlights": [
            "No direct UK flights — small turboprop only to Antigua, then BA to London",
            "Soufrière Hills Exclusion Zone covers the southern third of the island",
            "Very limited local mortuary infrastructure (~5,000 population island)",
            "No cremation facilities in Montserrat",
            "British Overseas Territory — all documentation in English"
        ]
    },
    "sint-maarten": {
        "country_key": "sint-maarten",
        "country_name": "Sint Maarten",
        "country_adjective": "Sint Maartener",
        "flag": "\U0001f1f8\U0001f1fd",
        "region": "Caribbean",
        "languages": "Dutch, English",
        "currency": "Netherlands Antillean Guilder (ANG)",
        "british_representation": "Non-resident — British Embassy, The Hague, Netherlands",
        "embassy_type": "Non-resident (Embassy The Hague)",
        "embassy_city": "The Hague",
        "local_authority_involved": "Civil Registry of Sint Maarten; Sint Maarten Police Force (KPSM — Korps Politie Sint Maarten)",
        "main_airports": "SXM (Princess Juliana International Airport, Philipsburg); one of the Caribbean's busiest airports",
        "routing_notes": "Princess Juliana International Airport (SXM) is one of the Caribbean's main hubs, with direct KLM service to Amsterdam Schiphol (AMS). Also direct connections to Miami, New York, and other North American cities. Sint Maarten and Saint Martin share the same island — the French side (Saint Martin / Grand Case Airport SFG) is a separate jurisdiction. UK routing via Amsterdam is the primary route.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Sint Maarten is a constituent country of the Kingdom of the Netherlands — autonomous but Dutch law applies. Non-resident British Embassy The Hague. Dutch civil registration system. Sint Maarten is a major Caribbean hub with well-developed tourist infrastructure. Note: the island is divided — the Dutch southern half is Sint Maarten, the French northern half is Saint Martin (Collectivité de Saint-Martin). Different jurisdictions and legal systems apply on each side.",
        "complexity_rating": "moderate",
        "complexity_notes": "Dutch civil law jurisdiction. Non-resident British Embassy The Hague. Dutch/English documentation — certified English translation of Dutch documents required. Sint Maarten suffered major damage from Hurricane Irma (2017) but has largely recovered. The island shares a border with French Saint Martin — ensure the correct jurisdiction is confirmed. Direct KLM Amsterdam for UK connections.",
        "required_documents": [
            "Death certificate (Civil Registry of Sint Maarten)",
            "Certified English translation of Dutch documents",
            "KPSM clearance (Korps Politie Sint Maarten, non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (British Embassy, The Hague)"
        ],
        "religion_notes": "Mix of Protestant and Catholic Christians, reflecting the island's Dutch and French heritage. Significant Haitian and other Caribbean immigrant communities.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Sint Maarten. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — British Embassy The Hague",
            "Island is divided — Dutch Sint Maarten (south) and French Saint Martin (north) are different jurisdictions",
            "Dutch documentation requires certified English translation",
            "Non-natural deaths require KPSM investigation"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_37.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
