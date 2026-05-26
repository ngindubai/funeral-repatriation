#!/usr/bin/env python3
"""Add Batch 34 countries to countries_repatriation.json.
Countries: tuvalu, solomon-islands, kiribati, slovakia, estonia
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_34 = {
    "tuvalu": {
        "country_key": "tuvalu",
        "country_name": "Tuvalu",
        "country_adjective": "Tuvaluan",
        "flag": "\U0001f1f9\U0001f1fb",
        "region": "Pacific",
        "languages": "Tuvaluan, English",
        "currency": "Australian Dollar (AUD) / Tuvaluan Dollar",
        "british_representation": "Non-resident — British High Commission, Suva, Fiji",
        "embassy_type": "Non-resident (BHC Suva)",
        "embassy_city": "Suva",
        "local_authority_involved": "Tuvalu Births, Deaths and Marriages Registry, Tuvalu Police Service",
        "main_airports": "FUN (Funafuti International Airport)",
        "routing_notes": "Fiji Airways serves Funafuti (FUN) via Suva/Nadi. No direct Pacific–UK service. All routing goes via Fiji, then connecting to UK via Sydney, Singapore, or Hong Kong.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "Tuvalu is one of the world's most remote nations — nine low-lying coral atolls across 756,000 km² of Pacific Ocean. Total land area: 26 km². Non-resident BHC Suva. Deaths on outer atolls require inter-island transfer to Funafuti before international repatriation. Very limited mortuary infrastructure.",
        "complexity_rating": "high",
        "complexity_notes": "Nine atolls across a vast Pacific expanse. Only Funafuti has an international airport. Fiji Airways is the sole international carrier. Very limited local mortuary and embalming capacity. Non-resident BHC Suva. Deaths on outer atolls require boat transfer to Funafuti.",
        "required_documents": [
            "Death certificate (Tuvalu Births, Deaths and Marriages Registry)",
            "Tuvalu Police Service clearance (non-natural deaths)",
            "Embalming certificate (very limited local capacity)",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (BHC Suva)"
        ],
        "religion_notes": "Predominantly Protestant Christian. Church of Tuvalu (Congregationalist) is the majority denomination.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Tuvalu. Full body repatriation via Fiji is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Suva, Fiji",
            "Nine atolls — deaths on outer islands require boat transfer to Funafuti",
            "Fiji Airways only international carrier — very limited cargo capacity",
            "Sea-level atoll nation: storm and flooding events can disrupt all operations"
        ]
    },
    "solomon-islands": {
        "country_key": "solomon-islands",
        "country_name": "Solomon Islands",
        "country_adjective": "Solomon Islander",
        "flag": "\U0001f1f8\U0001f1e7",
        "region": "Pacific",
        "languages": "English (official), Pijin, 70+ indigenous languages",
        "currency": "Solomon Islands Dollar (SBD)",
        "british_representation": "Non-resident — consular assistance via Australian High Commission, Honiara",
        "embassy_type": "Non-resident (Australian HC Honiara)",
        "embassy_city": "Honiara",
        "local_authority_involved": "Solomon Islands Registrar of Births, Deaths and Marriages; Royal Solomon Islands Police Force",
        "main_airports": "HIR (Honiara International Airport, Guadalcanal)",
        "routing_notes": "Solomon Airlines and Fiji Airways serve Honiara (HIR) via Brisbane, Port Moresby, and Nadi. All UK repatriation routes via Brisbane or Port Moresby.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "English common law jurisdiction. British colonial heritage — documentation is in English. Non-resident consular assistance via Australian HC Honiara. Deaths on outer islands (especially Malaita, Western Province, Choiseul) require inter-island boat or light aircraft transfer to Honiara.",
        "complexity_rating": "high",
        "complexity_notes": "Non-resident British representation via Australian HC. Remote Pacific archipelago of 900+ islands. Deaths outside Guadalcanal require inter-island transfer. Limited mortuary infrastructure outside Honiara. Political instability history — 2021 riots — though situation has stabilised.",
        "required_documents": [
            "Death certificate (Registrar of Births, Deaths and Marriages)",
            "Royal Solomon Islands Police Force clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (Australian HC Honiara acting for UK)"
        ],
        "religion_notes": "Predominantly Christian. Anglican, Roman Catholic, South Seas Evangelical Church, and United Church are major denominations.",
        "cremation_available": False,
        "cremation_notes": "Cremation is not available in Solomon Islands. Full body repatriation to the UK is required.",
        "no_go_zones": "FCDO advises increased caution in parts of Honiara (Malaitan/Guadalcanalese community tensions). Remote provinces have minimal infrastructure.",
        "risk_highlights": [
            "Non-resident British representation — Australian HC Honiara acts for UK",
            "900+ islands — deaths on outer islands require inter-island transfer to Honiara",
            "FCDO advises increased caution in parts of Honiara",
            "Limited mortuary infrastructure outside Guadalcanal"
        ]
    },
    "kiribati": {
        "country_key": "kiribati",
        "country_name": "Kiribati",
        "country_adjective": "I-Kiribati",
        "flag": "\U0001f1f0\U0001f1ee",
        "region": "Pacific",
        "languages": "English (official), Gilbertese (Kiribati)",
        "currency": "Australian Dollar (AUD)",
        "british_representation": "Non-resident — British High Commission, Suva, Fiji",
        "embassy_type": "Non-resident (BHC Suva)",
        "embassy_city": "Suva",
        "local_authority_involved": "Kiribati Registration of Births, Deaths and Marriages; Kiribati Police Service",
        "main_airports": "TRW (Bonriki International Airport, South Tarawa)",
        "routing_notes": "Fiji Airways serves South Tarawa (TRW) via Suva/Nadi. Air Kiribati operates inter-island domestic routes. Line Islands (Christmas Island/Kiritimati) are over 3,500 km from South Tarawa. All international routing via Fiji.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 21,
        "typical_timeline_days_max": 56,
        "timeline_notes": "Kiribati spans three island groups (Gilbert, Phoenix, Line Islands) across 3.5 million km² of Pacific Ocean — straddling both the equator and the International Date Line. Outer island deaths, particularly in the Phoenix or Line Islands, are among the most logistically extreme repatriation cases possible.",
        "complexity_rating": "high",
        "complexity_notes": "Three island groups spanning 3.5 million km² of Pacific. Deaths in Phoenix Islands or Line Islands (Kiritimati) are extremely remote with very infrequent air links back to South Tarawa. Non-resident BHC Suva. Very limited mortuary infrastructure. Australian Dollar as currency but very limited international banking.",
        "required_documents": [
            "Death certificate (Registration of Births, Deaths and Marriages, Kiribati)",
            "Kiribati Police Service clearance (non-natural deaths)",
            "Embalming certificate (very limited local capacity)",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (BHC Suva)"
        ],
        "religion_notes": "Predominantly Christian. Roman Catholic and Kiribati Protestant Church are the main denominations.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Kiribati. Full body repatriation via Fiji is required.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Suva, Fiji",
            "Three island groups spanning 3.5 million km² — among the world's most dispersed nations",
            "Deaths in Phoenix or Line Islands require internal transfer to South Tarawa before international routing",
            "Sea-level atoll nation: climate-related flooding can disrupt operations"
        ]
    },
    "slovakia": {
        "country_key": "slovakia",
        "country_name": "Slovakia",
        "country_adjective": "Slovak",
        "flag": "\U0001f1f8\U0001f1f0",
        "region": "Europe",
        "languages": "Slovak",
        "currency": "Euro (EUR)",
        "british_representation": "Resident — British Embassy, Bratislava",
        "embassy_type": "Resident Embassy",
        "embassy_city": "Bratislava",
        "local_authority_involved": "Matrika (Registry Office) at local municipal level; Police (non-natural deaths)",
        "main_airports": "BTS (Bratislava M.R. Štefánik International Airport), KSC (Košice International Airport)",
        "routing_notes": "Direct flights from Bratislava (BTS) to London (Ryanair, Wizz Air, Flybe seasonally). Vienna (VIE) is approximately 1 hour by road — many families use Vienna for additional UK connections. Košice (KSC) serves eastern Slovakia with connections via Prague or Vienna.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 14,
        "timeline_notes": "EU member state. Straightforward civil law documentation. Resident British Embassy Bratislava. Slovak death registration handled at local Matrika (registry office). Documentation in Slovak — translation to English required for UK Coroner.",
        "complexity_rating": "low",
        "complexity_notes": "EU, Schengen. Well-organised civil registration through local Matrika offices. Resident British Embassy in Bratislava. Direct flights to UK. Slovak documentation requires certified translation. Coroner's inquest in Slovakia (Prokuratúra involvement) may extend timeline in non-natural deaths.",
        "required_documents": [
            "Death certificate (Matrika — local registry office)",
            "Police report / Prokuratúra clearance (non-natural deaths)",
            "Certified English translation of death certificate",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Zinc-lined or approved sealed coffin documentation",
            "Consular registration (British Embassy, Bratislava)"
        ],
        "religion_notes": "Predominantly Roman Catholic. Lutheran and Greek Catholic minorities.",
        "cremation_available": True,
        "cremation_notes": "Cremation is widely available in Slovakia. Major crematoria in Bratislava, Košice, and other cities. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Documentation in Slovak — certified English translation required for UK Coroner",
            "Non-natural deaths involve Prokuratúra (prosecutor) clearance, which may add time",
            "Vienna (VIE) often the most practical departure airport for western Slovakia"
        ]
    },
    "estonia": {
        "country_key": "estonia",
        "country_name": "Estonia",
        "country_adjective": "Estonian",
        "flag": "\U0001f1ea\U0001f1ea",
        "region": "Europe",
        "languages": "Estonian",
        "currency": "Euro (EUR)",
        "british_representation": "Resident — British Embassy, Tallinn",
        "embassy_type": "Resident Embassy",
        "embassy_city": "Tallinn",
        "local_authority_involved": "Rahvastikuregister (Population Register, managed by Siseministeerium — Ministry of Interior); Police and Border Guard Board (non-natural deaths)",
        "main_airports": "TLL (Tallinn Lennart Meri Airport)",
        "routing_notes": "Direct flights from Tallinn (TLL) to London Gatwick and Stansted (Ryanair, easyJet). Also via Riga (RIX, 4 hours by road) or Helsinki (HEL, ferry then fly). Direct UK connections are good.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 14,
        "timeline_notes": "EU, NATO, Schengen. Advanced digital civil registration through the Rahvastikuregister (Population Register). Resident British Embassy Tallinn. Estonian documentation requires certified English translation for UK Coroner. Direct UK flights from Tallinn.",
        "complexity_rating": "low",
        "complexity_notes": "EU member with highly digitalised civil registration. Resident British Embassy Tallinn. Good direct UK air connections. Estonian documentation requires certified translation. Estonia's advanced e-government means death registration is typically efficient.",
        "required_documents": [
            "Death certificate (Rahvastikuregister — Population Register)",
            "Police and Border Guard Board clearance (non-natural deaths)",
            "Certified English translation of death certificate",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Approved sealed coffin documentation",
            "Consular registration (British Embassy, Tallinn)"
        ],
        "religion_notes": "Predominantly Lutheran, with significant Orthodox Christian minority. Estonia has high rates of non-religious affiliation.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available and widely used in Estonia. Crematoria in Tallinn and other major cities. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Documentation in Estonian — certified English translation required for UK Coroner",
            "Non-natural deaths involve Police and Border Guard Board — standard EU process",
            "Proximity to Russian border: FCDO advises awareness in north-eastern regions near the Russian Federation border"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_34.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
