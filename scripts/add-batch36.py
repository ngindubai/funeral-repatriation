#!/usr/bin/env python3
"""Add Batch 36 countries to countries_repatriation.json.
Countries: aruba, curacao, cayman-islands, turks-and-caicos, macau
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_36 = {
    "aruba": {
        "country_key": "aruba",
        "country_name": "Aruba",
        "country_adjective": "Aruban",
        "flag": "\U0001f1e6\U0001f1fc",
        "region": "Caribbean",
        "languages": "Papiamento, Dutch, English, Spanish",
        "currency": "Aruban Florin (AWG)",
        "british_representation": "Non-resident — British Embassy, The Hague, Netherlands",
        "embassy_type": "Non-resident (Embassy The Hague)",
        "embassy_city": "The Hague",
        "local_authority_involved": "Departamento di Registro Civil (Civil Registry, Government of Aruba); Korps Politie Aruba (Aruban Police)",
        "main_airports": "AUA (Queen Beatrix International Airport, Oranjestad)",
        "routing_notes": "Queen Beatrix Airport (AUA) has direct flights to Amsterdam Schiphol (KLM). Also connecting via Miami or other US hubs. All UK repatriation typically routes via Amsterdam (AMS).",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Aruba is a constituent country of the Kingdom of the Netherlands — autonomous but Dutch law applies. Non-resident British consular support via British Embassy The Hague. Dutch civil registration system. Aruba is a major tourist destination with established funeral and mortuary services.",
        "complexity_rating": "moderate",
        "complexity_notes": "Dutch civil law jurisdiction. Non-resident British Embassy The Hague. Papiamento and Dutch primary languages — documentation requires certified English translation. Well-developed tourist infrastructure. Direct KLM service to Amsterdam for UK connections.",
        "required_documents": [
            "Death certificate (Departamento di Registro Civil, Government of Aruba)",
            "Certified English translation of death certificate",
            "Korps Politie Aruba clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (British Embassy, The Hague)"
        ],
        "religion_notes": "Predominantly Roman Catholic.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Aruba. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — British Embassy The Hague",
            "Documentation in Dutch/Papiamento — certified English translation required",
            "Non-natural deaths require Korps Politie Aruba investigation"
        ]
    },
    "curacao": {
        "country_key": "curacao",
        "country_name": "Curaçao",
        "country_adjective": "Curaçaoan",
        "flag": "\U0001f1e8\U0001f1fc",
        "region": "Caribbean",
        "languages": "Papiamentu, Dutch, English",
        "currency": "Netherlands Antillean Guilder (ANG)",
        "british_representation": "Non-resident — British Embassy, The Hague, Netherlands",
        "embassy_type": "Non-resident (Embassy The Hague)",
        "embassy_city": "The Hague",
        "local_authority_involved": "Registro Civil (Civil Registry of Curaçao); Korps Politie Curaçao",
        "main_airports": "CUR (Curaçao Hato International Airport, Willemstad)",
        "routing_notes": "Curaçao Hato Airport (CUR) has direct KLM service to Amsterdam Schiphol (AMS). Also connections via Miami and Bogotá. All UK repatriation typically routes via Amsterdam.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Curaçao is a constituent country of the Kingdom of the Netherlands — autonomous but Dutch law applies. Non-resident British Embassy The Hague. Dutch civil registration. Curaçao is a significant tourist and financial centre with established mortuary services.",
        "complexity_rating": "moderate",
        "complexity_notes": "Dutch civil law jurisdiction. Non-resident British Embassy The Hague. Papiamentu and Dutch primary languages — documentation requires certified English translation. Direct KLM Amsterdam service for UK connections.",
        "required_documents": [
            "Death certificate (Registro Civil, Curaçao)",
            "Certified English translation of death certificate",
            "Korps Politie Curaçao clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (British Embassy, The Hague)"
        ],
        "religion_notes": "Predominantly Roman Catholic.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Curaçao. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — British Embassy The Hague",
            "Documentation in Dutch/Papiamentu — certified English translation required",
            "Non-natural deaths require Korps Politie Curaçao investigation"
        ]
    },
    "cayman-islands": {
        "country_key": "cayman-islands",
        "country_name": "Cayman Islands",
        "country_adjective": "Caymanian",
        "flag": "\U0001f1f0\U0001f1fe",
        "region": "Caribbean",
        "languages": "English",
        "currency": "Cayman Islands Dollar (KYD)",
        "british_representation": "Governor's Office (British Overseas Territory) — Governor represents the Crown. Consular functions via FCO London.",
        "embassy_type": "British Overseas Territory (Governor's Office)",
        "embassy_city": "George Town",
        "local_authority_involved": "General Registry (Civil Registration, Cayman Islands Government); Royal Cayman Islands Police Service",
        "main_airports": "GCM (Owen Roberts International Airport, Grand Cayman), CYB (Gerrard Smith Airport, Cayman Brac)",
        "routing_notes": "Owen Roberts Airport (GCM) has direct American Airlines and Cayman Airways service to Miami (MIA) and British Airways/Cayman Airways to London Gatwick (LGW). Direct UK routing available.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 14,
        "timeline_notes": "British Overseas Territory. English common law. English language throughout. The Governor's Office and UK Government have responsibility for the Cayman Islands. Direct Cayman Airways/British Airways service to London Gatwick. Well-developed financial centre with professional mortuary services.",
        "complexity_rating": "low",
        "complexity_notes": "British Overseas Territory — English common law, English language, direct UK flights available. General Registry handles civil registration. Royal Cayman Islands Police Service handles non-natural deaths. Deaths on Cayman Brac or Little Cayman require internal transfer to Grand Cayman.",
        "required_documents": [
            "Death certificate (General Registry, Cayman Islands Government)",
            "Royal Cayman Islands Police Service clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "FCO / UK Coroner notification"
        ],
        "religion_notes": "Predominantly Protestant Christian. United Church in Jamaica and the Cayman Islands is the largest denomination.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in the Cayman Islands. Ashes may be repatriated to the UK.",
        "no_go_zones": "",
        "risk_highlights": [
            "Deaths on Cayman Brac or Little Cayman require internal transfer to Grand Cayman first",
            "British Overseas Territory — all documentation in English",
            "Direct UK flights available from Grand Cayman (LGW via Cayman Airways/BA)"
        ]
    },
    "turks-and-caicos": {
        "country_key": "turks-and-caicos",
        "country_name": "Turks and Caicos Islands",
        "country_adjective": "Turks and Caicos Islander",
        "flag": "\U0001f1f9\U0001f1e8",
        "region": "Caribbean",
        "languages": "English",
        "currency": "United States Dollar (USD)",
        "british_representation": "Governor's Office (British Overseas Territory) — Governor represents the Crown. Consular functions via FCO London.",
        "embassy_type": "British Overseas Territory (Governor's Office)",
        "embassy_city": "Cockburn Town",
        "local_authority_involved": "Registrar General's Office (Civil Registration, TCI Government); Royal Turks and Caicos Islands Police Force",
        "main_airports": "PLS (Providenciales International Airport), GDT (Grand Turk Airport)",
        "routing_notes": "Providenciales (PLS) has connections to Miami, New York, and Toronto. No direct UK service — all UK routing via US or Caribbean hub. British Airways serves Nassau, Bahamas, which can connect. Most families route via Miami (MIA).",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "British Overseas Territory. English common law. English language throughout. Multiple islands — deaths on outer islands (Grand Turk, South Caicos, North Caicos, Middle Caicos) require internal transfer to Providenciales. No direct UK flights — routing via US hubs.",
        "complexity_rating": "moderate",
        "complexity_notes": "British Overseas Territory — English common law, English language. No direct UK flights. Routing via US requires US USDA/CBP import documentation for human remains. Multiple islands: deaths outside Providenciales require inter-island transfer.",
        "required_documents": [
            "Death certificate (Registrar General's Office, TCI Government)",
            "Royal TCI Police Force clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "US transit documentation (USDA/CBP if routing via USA)",
            "FCO / UK Coroner notification"
        ],
        "religion_notes": "Predominantly Protestant Christian. Baptist and other evangelical denominations are common.",
        "cremation_available": False,
        "cremation_notes": "Cremation facilities are not available in TCI. Full body repatriation is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "No direct UK flights — routing via US requires US transit documentation",
            "Deaths on outer islands require inter-island transfer to Providenciales",
            "British Overseas Territory — all documentation in English"
        ]
    },
    "macau": {
        "country_key": "macau",
        "country_name": "Macau",
        "country_adjective": "Macanese",
        "flag": "\U0001f1f2\U0001f1f4",
        "region": "Asia",
        "languages": "Cantonese Chinese, Portuguese",
        "currency": "Macanese Pataca (MOP)",
        "british_representation": "Non-resident — British Consulate General, Hong Kong (covers Macau)",
        "embassy_type": "Non-resident (British CG Hong Kong)",
        "embassy_city": "Hong Kong",
        "local_authority_involved": "Conservatória do Registo Civil (Civil Registry Conservatory); Polícia Judiciária (Judicial Police, non-natural deaths)",
        "main_airports": "MFM (Macau International Airport)",
        "routing_notes": "Macau International Airport (MFM) has regional connections to mainland China and Southeast Asia. More practically, the Hong Kong–Macau Ferry (1 hour) or Zhuhai border crossing puts the repatriation into the Hong Kong/Guangdong routing network. Many repatriations route via Hong Kong International Airport (HKG).",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Macau is a Special Administrative Region (SAR) of China, with its own civil and legal system — influenced by Portuguese civil law (former Portuguese territory until 1999). The Conservatória do Registo Civil handles civil registration. The Polícia Judiciária (modelled on the Portuguese judicial police) handles non-natural deaths. Documentation is in Chinese and Portuguese.",
        "complexity_rating": "moderate",
        "complexity_notes": "Macau SAR has its own Portuguese-influenced civil law system. Documentation in Chinese and Portuguese requires certified English translation. Non-resident British CG Hong Kong covers Macau. Routing via Hong Kong is most practical. The gambling tourism industry means the territory has professional mortuary infrastructure.",
        "required_documents": [
            "Death certificate (Conservatória do Registo Civil)",
            "Certified English translation of death certificate",
            "Polícia Judiciária clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit (SAR Government)",
            "Consular registration (British CG, Hong Kong)"
        ],
        "religion_notes": "Predominantly Buddhist and Taoist. Catholic minority (Portuguese colonial legacy). Traditional Chinese religious practices are common.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Macau. The Macau SAR government operates cremation facilities. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — British CG Hong Kong covers Macau",
            "Documentation in Chinese and Portuguese — certified English translation required",
            "Routing practically via Hong Kong (HKG) rather than Macau Airport (MFM)"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_36.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
