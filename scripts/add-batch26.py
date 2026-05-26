"""
Add Batch 26 countries to site/data/countries_repatriation.json
Countries: Mali, Burkina Faso, South Sudan, Somalia, Comoros
"""
import json, sys

PATH = "site/data/countries_repatriation.json"

batch26 = {
    "mali": {
        "country_key": "mali",
        "country_name": "Mali",
        "country_adjective": "Malian",
        "flag": "🇲🇱",
        "region": "West Africa",
        "languages": ["French", "Bambara"],
        "currency": "West African CFA franc (XOF)",
        "british_representation": "Non-resident — British Embassy Dakar, Senegal",
        "embassy_type": "Non-resident",
        "embassy_city": "Dakar (non-resident)",
        "local_authority_involved": "Police Nationale du Mali, Parquet civil registrar, Ministry of Health",
        "main_airports": ["Bamako-Sénou International Airport (BKO)"],
        "routing_notes": "Ethiopian Airlines via Addis Ababa (ADD); Royal Air Maroc via Casablanca (CMN); Air Côte d'Ivoire via Abidjan (ABJ). Air France suspended Bamako service in 2023.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 90,
        "timeline_notes": "Extended by junta-controlled administration, absence of direct UK flights, and armed group activity. Cases in north/central conflict zones may not be achievable.",
        "complexity_rating": "very-high",
        "complexity_notes": "Military junta (Transition government under Col. Goïta) controls all administrative processes since 2021. FCDO advises against all travel to northern Mali and all but essential to most of the country. JNIM and ISWAP-affiliated armed groups active across large areas.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Police Nationale clearance",
            "Judicial clearance (Parquet)",
            "Ministry of Health export permit",
            "Certified English translations"
        ],
        "religion_notes": "Predominantly Muslim. Islamic burial customs apply — rapid local interment traditional and expected.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available in Mali.",
        "no_go_zones": [
            "Northern Mali (Kidal, Gao, Timbuktu regions — FCDO against all travel)",
            "Central Mali border zones (Ménaka, northern Mopti)",
            "Border areas with Burkina Faso and Niger"
        ],
        "risk_highlights": [
            "Military junta administration — processes unpredictable",
            "Air France suspended Bamako service 2023",
            "JNIM and ISWAP-affiliated groups active across large parts of country",
            "No direct UK commercial flights",
            "Non-resident Embassy coverage only"
        ]
    },
    "burkina-faso": {
        "country_key": "burkina-faso",
        "country_name": "Burkina Faso",
        "country_adjective": "Burkinabé",
        "flag": "🇧🇫",
        "region": "West Africa",
        "languages": ["French"],
        "currency": "West African CFA franc (XOF)",
        "british_representation": "Non-resident — British High Commission Accra, Ghana",
        "embassy_type": "Non-resident",
        "embassy_city": "Accra (non-resident)",
        "local_authority_involved": "Police Nationale du Burkina Faso, Tribunal de Grande Instance, Ministry of Health",
        "main_airports": ["Ouagadougou Airport (OUA)"],
        "routing_notes": "Ethiopian Airlines via Addis Ababa (ADD); Royal Air Maroc via Casablanca (CMN); Air France Ouagadougou (service irregular — verify). Brussels Airlines via Brussels.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 90,
        "timeline_notes": "CNSP junta controls administration since September 2022. FCDO all-but-essential. Cases in northern and eastern conflict zones not achievable.",
        "complexity_rating": "very-high",
        "complexity_notes": "Military junta (MPSR/CNSP under Captain Traoré) since September 2022. FCDO advises against all travel to northern, eastern, and western border regions. JNIM and ISWAP-affiliated groups active across large parts of country. Air France service to Ouagadougou irregular.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Police Nationale clearance",
            "Tribunal de Grande Instance order (non-natural deaths)",
            "Ministry of Health export permit",
            "Certified English translations"
        ],
        "religion_notes": "Mixed Muslim, Christian, and animist. Islamic burial customs for Muslim majority.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available in Burkina Faso.",
        "no_go_zones": [
            "Sahel, Nord, Centre-Nord, and Est provinces (FCDO against all travel)",
            "Border areas with Mali and Niger",
            "Eastern regions (Gourma, Tapoa provinces)",
            "Western border areas with Côte d'Ivoire and Ghana"
        ],
        "risk_highlights": [
            "Military coup September 2022 — CNSP junta",
            "FCDO all-but-essential for entire country",
            "JNIM/ISWAP widespread — large zones not achievable",
            "Air France service irregular — verify availability",
            "Non-resident Embassy adds coordination time"
        ]
    },
    "south-sudan": {
        "country_key": "south-sudan",
        "country_name": "South Sudan",
        "country_adjective": "South Sudanese",
        "flag": "🇸🇸",
        "region": "East Africa",
        "languages": ["English", "Arabic"],
        "currency": "South Sudanese pound (SSP)",
        "british_representation": "British Embassy Juba",
        "embassy_type": "Resident",
        "embassy_city": "Juba",
        "local_authority_involved": "South Sudan National Police Service, Ministry of Health, Office of the Registrar General",
        "main_airports": ["Juba International Airport (JUB)"],
        "routing_notes": "Ethiopian Airlines via Addis Ababa (ADD); Kenya Airways via Nairobi (NBO); EgyptAir via Cairo.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 21,
        "typical_timeline_days_max": 90,
        "timeline_notes": "Civil registration system severely underdeveloped since 2011 independence. Administrative capacity very limited outside Juba. Armed conflict ongoing in multiple states.",
        "complexity_rating": "very-high",
        "complexity_notes": "World's youngest country (independence 2011). Civil war 2013–2018 with fragile ceasefire. Ongoing armed conflict in Unity State, Upper Nile, and Equatoria regions. Civil registration infrastructure very limited. FCDO advises against all travel to multiple states.",
        "required_documents": [
            "Death certificate",
            "South Sudan National Police Service clearance",
            "Ministry of Health export permit",
            "Embalming certificate"
        ],
        "religion_notes": "Predominantly Christian and animist. Some Muslim population in border areas.",
        "cremation_available": False,
        "cremation_notes": "Cremation not practised or available in South Sudan.",
        "no_go_zones": [
            "Unity State (FCDO against all travel)",
            "Upper Nile State (FCDO against all travel)",
            "Western Equatoria (FCDO against all travel)",
            "Central Equatoria outside Juba (FCDO against all travel)"
        ],
        "risk_highlights": [
            "Active armed conflict in multiple states",
            "Civil registration system extremely limited",
            "FCDO against all travel to conflict states",
            "Mortuary infrastructure almost non-existent outside Juba",
            "Ceasefire fragile — situation can deteriorate rapidly"
        ]
    },
    "somalia": {
        "country_key": "somalia",
        "country_name": "Somalia",
        "country_adjective": "Somali",
        "flag": "🇸🇴",
        "region": "East Africa",
        "languages": ["Somali", "Arabic"],
        "currency": "Somali shilling (SOS)",
        "british_representation": "British Embassy Mogadishu (under severe security restrictions)",
        "embassy_type": "Resident",
        "embassy_city": "Mogadishu",
        "local_authority_involved": "Somalia Police Force, Ministry of Health (FGS), civil registration authorities",
        "main_airports": [
            "Aden Adde International Airport (MGQ), Mogadishu",
            "Egal International Airport (HGA), Hargeisa (Somaliland)",
            "Berbera Airport (BBO), Somaliland"
        ],
        "routing_notes": "Turkish Airlines via Istanbul (IST) — most reliable UK route from Mogadishu. Ethiopian Airlines via Addis Ababa (ADD). Hargeisa/Somaliland: Ethiopian Airlines via Addis Ababa.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 90,
        "timeline_notes": "Civil registration varies by region and control. Cases outside Mogadishu and accessible FGS-controlled areas may not be achievable. Somaliland has a separate, more functional administration.",
        "complexity_rating": "very-high",
        "complexity_notes": "FCDO advises against all travel to Somalia. Al-Shabaab controls large rural areas in south and central Somalia. Civil registration fragmented across Federal Government of Somalia (FGS), Puntland, and Somaliland. British Embassy Mogadishu operates under severe security restrictions and cannot provide standard consular assistance in most areas.",
        "required_documents": [
            "Death certificate",
            "Somalia Police Force clearance",
            "Ministry of Health export permit",
            "Embalming certificate"
        ],
        "religion_notes": "Almost entirely Sunni Muslim. Strong pressure for rapid local Islamic burial. Families must explicitly assert repatriation intent promptly.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available. Contrary to Islamic law.",
        "no_go_zones": [
            "All rural areas (Al-Shabaab control)",
            "Lower Shabelle region",
            "Middle and Lower Jubba",
            "Bay and Bakool regions",
            "Any area outside FGS-controlled urban centres"
        ],
        "risk_highlights": [
            "FCDO against all travel to Somalia",
            "Al-Shabaab active across large parts of south and central Somalia",
            "Civil registration fragmented across three administrations",
            "British Embassy under severe security restrictions",
            "Note: Somaliland has a separate, more accessible administration"
        ]
    },
    "comoros": {
        "country_key": "comoros",
        "country_name": "Comoros",
        "country_adjective": "Comorian",
        "flag": "🇰🇲",
        "region": "Indian Ocean",
        "languages": ["Comorian (Shikomori)", "Arabic", "French"],
        "currency": "Comorian franc (KMF)",
        "british_representation": "Non-resident — British High Commission Port Louis, Mauritius",
        "embassy_type": "Non-resident",
        "embassy_city": "Port Louis (non-resident)",
        "local_authority_involved": "Gendarmerie Nationale, Ministry of Health, civil status office",
        "main_airports": ["Prince Said Ibrahim International Airport (HAH), Grande Comore"],
        "routing_notes": "Air Austral via Réunion (REU); Ethiopian Airlines via Addis Ababa (ADD); Kenya Airways via Nairobi (NBO). All routes require 2+ connections to London.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "Small island nation with accessible civil administration, but limited capacity. Non-resident Embassy adds coordination time. Islamic burial pressure for rapid interment.",
        "complexity_rating": "high",
        "complexity_notes": "Three-island archipelago (Grande Comore, Anjouan, Mohéli) with separate local administrations. French civil law supplemented by Islamic personal status law. Non-resident Embassy adds coordination layer. Limited international air connections.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Gendarmerie Nationale clearance",
            "Ministry of Health export permit",
            "Certified English translations"
        ],
        "religion_notes": "Almost entirely Sunni Muslim. Islamic burial customs — strong pressure for rapid local interment.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available. Contrary to Islamic law.",
        "no_go_zones": [],
        "risk_highlights": [
            "Non-resident Embassy — coordination via Mauritius",
            "Three-island administration — jurisdiction depends on island of death",
            "Limited direct international air connections",
            "Islamic burial pressure for rapid interment"
        ]
    }
}

data = json.load(open(PATH, encoding='utf-8'))
added = []
for key, country in batch26.items():
    if key not in data['countries']:
        data['countries'][key] = country
        added.append(key)
    else:
        print(f"SKIP (already exists): {key}")

if added:
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"ADDED: {', '.join(added)}. Total countries: {len(data['countries'])}")
else:
    print("Nothing added.")
