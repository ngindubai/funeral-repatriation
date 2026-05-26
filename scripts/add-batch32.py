#!/usr/bin/env python3
"""Add Batch 32 countries to countries_repatriation.json.
Countries: north-korea, bhutan, saint-kitts-and-nevis, monaco, san-marino
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_32 = {
    "north-korea": {
        "country_key": "north-korea",
        "country_name": "North Korea",
        "country_adjective": "North Korean",
        "flag": "\U0001f1f0\U0001f1f5",
        "region": "East Asia",
        "languages": "Korean",
        "currency": "North Korean Won (KPW)",
        "british_representation": "Non-resident — British Embassy, Seoul, South Korea",
        "embassy_type": "Non-resident (Embassy Seoul)",
        "embassy_city": "Seoul",
        "local_authority_involved": "Korean People's Internal Security Forces; Ministry of People's Security civil registration",
        "main_airports": "FNJ (Pyongyang Sunan International)",
        "routing_notes": "Air Koryo operates Pyongyang to Beijing (PEK). Only viable international routing is via China. Access severely restricted.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 180,
        "timeline_notes": "One of the world's most inaccessible states for foreign nationals. UK does not maintain resident embassy. All foreign nationals require government-assigned minders. Death of a foreign national is a rare event requiring North Korean state cooperation. Timelines highly unpredictable.",
        "complexity_rating": "very-high",
        "complexity_notes": "No resident UK Embassy. North Korea is one of the world's most closed states. Foreign nationals cannot move freely. Air Koryo only commercial airline. All international movement requires state approval. UK has no diplomatic relations with North Korea — British Embassy Seoul is non-resident. North Korean authorities control all information and documentation. Swedish Embassy in Pyongyang provides some consular services to UK nationals by prior arrangement.",
        "required_documents": [
            "Death certificate (Korean People's Internal Security Forces / Ministry of People's Security)",
            "State authorisation for repatriation",
            "Documentation via Swedish Embassy Pyongyang (acting for UK)",
            "Consular registration (British Embassy, Seoul)"
        ],
        "religion_notes": "Officially atheist state. Traditional Korean religious practices exist covertly. No religious requirements for repatriation.",
        "cremation_available": False,
        "cremation_notes": "Cremation availability for foreign nationals is unknown. Full body repatriation assumed in all cases.",
        "no_go_zones": "FCDO advises against ALL travel to North Korea. The entire country is subject to severe travel restrictions.",
        "risk_highlights": [
            "FCDO advises against all travel to North Korea",
            "No resident UK Embassy — Swedish Embassy Pyongyang provides limited assistance",
            "All foreign nationals require state-assigned minders — no independent movement",
            "North Korean state controls all documentation and information",
            "Air Koryo (Pyongyang–Beijing) is the only viable repatriation routing"
        ]
    },
    "bhutan": {
        "country_key": "bhutan",
        "country_name": "Bhutan",
        "country_adjective": "Bhutanese",
        "flag": "\U0001f1e7\U0001f1f9",
        "region": "South Asia",
        "languages": "Dzongkha, English",
        "currency": "Bhutanese Ngultrum (BTN), pegged to Indian Rupee",
        "british_representation": "Non-resident — British High Commission, New Delhi, India",
        "embassy_type": "Non-resident (BHC New Delhi)",
        "embassy_city": "New Delhi",
        "local_authority_involved": "Civil Registration and Census Authority (CRCA), Royal Bhutan Police",
        "main_airports": "PBH (Paro International)",
        "routing_notes": "Paro International served by Drukair (Royal Bhutan Airlines) and Bhutan Airlines via Delhi, Kolkata, Bangkok, Kathmandu. Very limited capacity.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "All foreign nationals in Bhutan must be on an approved tour with a licensed guide. This means death of a foreign national involves the tour operator from the outset. Buddhist funeral customs observed for local population. Very limited mortuary infrastructure.",
        "complexity_rating": "high",
        "complexity_notes": "Bhutan restricts tourism strictly — daily visitor tariff system means all visitors are on registered tours. Limited mortuary infrastructure. Very limited air capacity at Paro (approach among world's most challenging). Non-resident BHC New Delhi. Buddhist context but no religious requirements for foreign national repatriation.",
        "required_documents": [
            "Death certificate (Civil Registration and Census Authority)",
            "Royal Bhutan Police clearance",
            "Embalming certificate (if available)",
            "Export authorisation",
            "Consular registration (BHC New Delhi)"
        ],
        "religion_notes": "Vajrayana Buddhism is the official religion. Significant Hindu minority. No Islamic burial requirements.",
        "cremation_available": False,
        "cremation_notes": "No commercial cremation facilities for foreign nationals. Full body repatriation to the UK is required.",
        "no_go_zones": "Border regions with China. Some protected nature areas restricted. Check FCDO for current advisories.",
        "risk_highlights": [
            "Non-resident British representation — BHC New Delhi",
            "Very limited air capacity at Paro airport",
            "All foreign visitors on registered tours — tour operator involved from the start",
            "Limited mortuary infrastructure"
        ]
    },
    "saint-kitts-and-nevis": {
        "country_key": "saint-kitts-and-nevis",
        "country_name": "Saint Kitts and Nevis",
        "country_adjective": "Kittitian/Nevisian",
        "flag": "\U0001f1f0\U0001f1f3",
        "region": "Caribbean",
        "languages": "English",
        "currency": "East Caribbean Dollar (XCD)",
        "british_representation": "Non-resident — British High Commission, Bridgetown, Barbados",
        "embassy_type": "Non-resident (BHC Bridgetown)",
        "embassy_city": "Bridgetown",
        "local_authority_involved": "Registrar General's Office, Coroner's Court (unnatural deaths)",
        "main_airports": "SKB (Robert L. Bradshaw International, Saint Kitts), NEV (Vance W. Amory International, Nevis)",
        "routing_notes": "Via Antigua (American Airlines/LIAT/Caribbean Airlines connections), via San Juan Puerto Rico, via Miami. Separate airport on Nevis island.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "English common law. Commonwealth documentation. Deaths on Nevis island require internal transfer to Saint Kitts before international repatriation.",
        "complexity_rating": "moderate",
        "complexity_notes": "Non-resident BHC Bridgetown. English common law. Deaths on Nevis require inter-island transfer to Saint Kitts. Cremation available. Well-established Caribbean routing.",
        "required_documents": [
            "Death certificate (Registrar General's Office)",
            "Coroner's certificate (unnatural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (BHC Bridgetown)"
        ],
        "religion_notes": "Predominantly Christian. Anglican, Methodist, and Pentecostal denominations.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available on Saint Kitts. Ashes repatriation to the UK is a practical option.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Bridgetown",
            "Deaths on Nevis island require inter-island transfer to Saint Kitts"
        ]
    },
    "monaco": {
        "country_key": "monaco",
        "country_name": "Monaco",
        "country_adjective": "Monégasque",
        "flag": "\U0001f1f2\U0001f1e8",
        "region": "Europe",
        "languages": "French (official), Italian, Monégasque",
        "currency": "Euro (EUR)",
        "british_representation": "Non-resident — British Embassy, Paris, France",
        "embassy_type": "Non-resident (Embassy Paris)",
        "embassy_city": "Paris",
        "local_authority_involved": "Direction de l'Etat Civil (Monaco civil registry), Sûreté Publique",
        "main_airports": "NCE (Nice Côte d'Azur, France — approx. 25 mins by road)",
        "routing_notes": "Road transfer to Nice Côte d'Azur Airport (NCE), then direct flights to UK airports. Helicopter transfers available Nice–Monaco. Very straightforward.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 3,
        "typical_timeline_days_max": 10,
        "timeline_notes": "Very low complexity. French civil law influences. Excellent access to Nice airport.",
        "complexity_rating": "low",
        "complexity_notes": "City-state of 2 km² on the French Riviera. French civil law influences. Direction de l'Etat Civil handles civil registration. Non-resident British Embassy Paris. Road access to Nice airport 25 minutes. Helicopter pads available. Among the simplest repatriation cases in Europe.",
        "required_documents": [
            "Death certificate (Direction de l'Etat Civil, Monaco)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export authorisation",
            "Consular registration (British Embassy, Paris)"
        ],
        "religion_notes": "Predominantly Roman Catholic.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Monaco. Transfer to Nice or Cannes in France for cremation is the standard option, followed by ashes repatriation.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — Embassy Paris",
            "No airport in Monaco — road transfer to Nice NCE (25 mins) required",
            "No cremation facilities — transfer to France required if cremation is wanted"
        ]
    },
    "san-marino": {
        "country_key": "san-marino",
        "country_name": "San Marino",
        "country_adjective": "Sammarinese",
        "flag": "\U0001f1f8\U0001f1f2",
        "region": "Europe",
        "languages": "Italian",
        "currency": "Euro (EUR)",
        "british_representation": "Non-resident — British Embassy, Rome, Italy",
        "embassy_type": "Non-resident (Embassy Rome)",
        "embassy_city": "Rome",
        "local_authority_involved": "Ufficio di Stato Civile (San Marino civil registry), Corpo della Gendarmeria",
        "main_airports": "RMI (Federico Fellini International, Rimini, Italy — approx. 30 mins by road), BLQ (Bologna Guglielmo Marconi — approx. 1 hr by road)",
        "routing_notes": "Road transfer to Rimini (RMI, approx. 30 mins) or Bologna (BLQ, approx. 1 hr), then to UK via Italian connections.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 3,
        "typical_timeline_days_max": 10,
        "timeline_notes": "Very low complexity. Italian civil law closely followed. Excellent road access to Rimini and Bologna.",
        "complexity_rating": "low",
        "complexity_notes": "Microstate of 61 km² entirely surrounded by Italy. Italian civil law closely followed. Ufficio di Stato Civile handles civil registration in Italian. Non-resident British Embassy Rome. Road to Rimini airport 30 minutes. Among the simplest repatriation cases in Europe.",
        "required_documents": [
            "Death certificate (Ufficio di Stato Civile, in Italian)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export authorisation",
            "Consular registration (British Embassy, Rome)"
        ],
        "religion_notes": "Predominantly Roman Catholic.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in San Marino. Transfer to Italy for cremation is the standard option if required.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — Embassy Rome",
            "No airport in San Marino — road transfer to Rimini RMI (30 mins) or Bologna BLQ (1 hr)",
            "Documentation in Italian — certified translation required"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_32.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
