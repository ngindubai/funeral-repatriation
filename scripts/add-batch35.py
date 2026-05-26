#!/usr/bin/env python3
"""Add Batch 35 countries to countries_repatriation.json.
Countries: latvia, lithuania, holy-see, cook-islands, niue
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_35 = {
    "latvia": {
        "country_key": "latvia",
        "country_name": "Latvia",
        "country_adjective": "Latvian",
        "flag": "\U0001f1f1\U0001f1fb",
        "region": "Europe",
        "languages": "Latvian",
        "currency": "Euro (EUR)",
        "british_representation": "Resident — British Embassy, Riga",
        "embassy_type": "Resident Embassy",
        "embassy_city": "Riga",
        "local_authority_involved": "Pilsonības un migrācijas lietu pārvalde — PMLP (Office of Citizenship and Migration Affairs); State Police (non-natural deaths)",
        "main_airports": "RIX (Riga International Airport)",
        "routing_notes": "Direct flights from Riga (RIX) to London Gatwick, Stansted, and Luton (Ryanair, Wizz Air, airBaltic). Frequent connections. Flight time approximately 3 hours.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 14,
        "timeline_notes": "EU, NATO, Schengen member. Civil registration through PMLP. Resident British Embassy Riga. Latvian documentation requires certified English translation for UK Coroner. Non-natural deaths involve State Police and Prokuratūra (Prosecutor's Office) clearance.",
        "complexity_rating": "low",
        "complexity_notes": "EU member with organised civil registration. Resident British Embassy Riga. Good direct UK air connections from RIX. Latvian death certificate requires certified translation. Non-natural deaths extend timeline due to Prokuratūra involvement.",
        "required_documents": [
            "Death certificate (PMLP — Pilsonības un migrācijas lietu pārvalde)",
            "Certified English translation of death certificate",
            "State Police / Prokuratūra clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Approved sealed coffin documentation",
            "Consular registration (British Embassy, Riga)"
        ],
        "religion_notes": "Lutheran majority. Roman Catholic minority in Latgale region. Orthodox Christian community.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Latvia. Crematoria in Riga and Daugavpils. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Documentation in Latvian — certified English translation required for UK Coroner",
            "Non-natural deaths involve Prokuratūra clearance, which may add several days",
            "FCDO advises awareness of security context near the Russian and Belarusian borders"
        ]
    },
    "lithuania": {
        "country_key": "lithuania",
        "country_name": "Lithuania",
        "country_adjective": "Lithuanian",
        "flag": "\U0001f1f1\U0001f1f9",
        "region": "Europe",
        "languages": "Lithuanian",
        "currency": "Euro (EUR)",
        "british_representation": "Resident — British Embassy, Vilnius",
        "embassy_type": "Resident Embassy",
        "embassy_city": "Vilnius",
        "local_authority_involved": "Registrų centras (Register Centre — Civil Metrical Records); Lithuanian Police (non-natural deaths)",
        "main_airports": "VNO (Vilnius International Airport), KUN (Kaunas International Airport)",
        "routing_notes": "Direct flights from Vilnius (VNO) to London Gatwick and Luton (Ryanair, Wizz Air). Kaunas (KUN) also has London connections. Flight time approximately 3 hours.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 14,
        "timeline_notes": "EU, NATO, Schengen. Civil registration via Registrų centras. Resident British Embassy Vilnius. Lithuanian documentation requires certified English translation for UK Coroner. Non-natural deaths involve Lithuanian Police and Prokuratūra clearance.",
        "complexity_rating": "low",
        "complexity_notes": "EU member with organised civil registration. Resident British Embassy Vilnius. Direct UK air connections from VNO and KUN. Lithuanian death certificate requires certified translation. Non-natural deaths extend timeline.",
        "required_documents": [
            "Death certificate (Registrų centras — Register Centre)",
            "Certified English translation of death certificate",
            "Lithuanian Police / Prokuratūra clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Approved sealed coffin documentation",
            "Consular registration (British Embassy, Vilnius)"
        ],
        "religion_notes": "Predominantly Roman Catholic. Lithuania has one of the highest rates of Catholic affiliation in the Baltic states.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Lithuania. Crematoria in Vilnius and Kaunas. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Documentation in Lithuanian — certified English translation required for UK Coroner",
            "Non-natural deaths involve Prokuratūra clearance, which may add several days",
            "FCDO advises awareness of security context: Lithuania borders Kaliningrad (Russian exclave) and Belarus"
        ]
    },
    "holy-see": {
        "country_key": "holy-see",
        "country_name": "Holy See (Vatican City)",
        "country_adjective": "Vatican",
        "flag": "\U0001f1fb\U0001f1e6",
        "region": "Europe",
        "languages": "Italian (working), Latin (official), various",
        "currency": "Euro (EUR)",
        "british_representation": "Resident — British Embassy to the Holy See, Rome (separate from British Embassy Italy)",
        "embassy_type": "Resident Embassy (to Holy See)",
        "embassy_city": "Rome",
        "local_authority_involved": "Governatorato dello Stato della Città del Vaticano (Governorate of Vatican City State); Gendarmerie Corps of Vatican City State",
        "main_airports": "FCO (Rome Fiumicino Leonardo da Vinci International Airport)",
        "routing_notes": "Vatican City has no airport. Rome Fiumicino (FCO) is the practical gateway, approximately 30 minutes by road. Direct flights from FCO to London Heathrow, Gatwick, and Stansted.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Vatican City is a sovereign state of 0.44 km² within Rome. Deaths of non-Vatican citizens in Vatican territory are extremely rare. The Governorate manages civil records. Gendarmerie investigates non-natural deaths. Italian is the working language. The Holy See has a separate British Embassy distinct from the Italian Embassy.",
        "complexity_rating": "low",
        "complexity_notes": "Vatican deaths of non-citizens are extremely rare. The Governorate of Vatican City State handles civil registration. Italian is the working language — documentation requires certified English translation. British Embassy to the Holy See is separate from British Embassy Italy. Rome Fiumicino (FCO) is the departure airport.",
        "required_documents": [
            "Death certificate (Governatorato dello Stato della Città del Vaticano)",
            "Certified English translation of death certificate",
            "Gendarmerie clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export documentation (Italian transit requirements apply)",
            "Consular registration (British Embassy to the Holy See)"
        ],
        "religion_notes": "The Holy See is the seat of the Roman Catholic Church. Deaths of Vatican personnel involve the Church's own administrative protocols alongside civil processes.",
        "cremation_available": False,
        "cremation_notes": "Cremation is not performed within Vatican City. Given the Church's historical preference for burial, families should discuss options with the British Embassy and local representatives.",
        "no_go_zones": "",
        "risk_highlights": [
            "Deaths of non-Vatican citizens in Vatican territory are extremely rare — specialist case",
            "Governorate civil registration in Italian — certified translation required",
            "British Embassy to the Holy See is distinct from British Embassy Italy — contact correct mission"
        ]
    },
    "cook-islands": {
        "country_key": "cook-islands",
        "country_name": "Cook Islands",
        "country_adjective": "Cook Islander",
        "flag": "\U0001f1e8\U0001f1f0",
        "region": "Pacific",
        "languages": "English, Cook Islands Māori (Rarotongan)",
        "currency": "New Zealand Dollar (NZD)",
        "british_representation": "Non-resident — British High Commission, Wellington, New Zealand",
        "embassy_type": "Non-resident (BHC Wellington)",
        "embassy_city": "Wellington",
        "local_authority_involved": "Cook Islands Civil Registration (Ministry of Internal Affairs); Cook Islands Police Service",
        "main_airports": "RAR (Rarotonga International Airport)",
        "routing_notes": "Air New Zealand serves Rarotonga (RAR) from Auckland (AKL). Fiji Airways also serves RAR. All UK repatriation routes via Auckland or Sydney for connecting flights.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 28,
        "timeline_notes": "Cook Islands is in free association with New Zealand. English common law. Commonwealth documentation. Non-resident BHC Wellington. Rarotonga is accessible and well-connected by Pacific standards. Deaths on the outer Northern Group islands (very remote atolls) require internal transfer to Rarotonga.",
        "complexity_rating": "moderate",
        "complexity_notes": "Free association with New Zealand. English common law. Non-resident BHC Wellington. Rarotonga airport has good connections via Auckland. Outer Northern Group islands (Penrhyn, Manihiki, Rakahanga, Pukapuka) are extremely remote and require internal transfer to Rarotonga. Cremation available at Rarotonga.",
        "required_documents": [
            "Death certificate (Cook Islands Civil Registration, Ministry of Internal Affairs)",
            "Cook Islands Police Service clearance (non-natural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (BHC Wellington)"
        ],
        "religion_notes": "Predominantly Christian. Cook Islands Christian Church (CICC, Congregationalist) is the majority denomination.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available at Rarotonga. Ashes may be repatriated to the UK in a sealed urn.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Wellington",
            "Outer Northern Group atolls are among the Pacific's most remote islands",
            "Deaths on outer islands require internal transfer to Rarotonga before international routing"
        ]
    },
    "niue": {
        "country_key": "niue",
        "country_name": "Niue",
        "country_adjective": "Niuean",
        "flag": "\U0001f1f3\U0001f1fa",
        "region": "Pacific",
        "languages": "Niuean, English",
        "currency": "New Zealand Dollar (NZD)",
        "british_representation": "Non-resident — British High Commission, Wellington, New Zealand",
        "embassy_type": "Non-resident (BHC Wellington)",
        "embassy_city": "Wellington",
        "local_authority_involved": "Niue Registrar of Births, Deaths and Marriages; Niue Police",
        "main_airports": "IUE (Niue International Airport, Alofi)",
        "routing_notes": "Air New Zealand operates Niue (IUE) to Auckland (AKL) approximately twice weekly. No other international carrier serves Niue. All UK routing via Auckland.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 28,
        "timeline_notes": "Niue is a self-governing state in free association with New Zealand. Population approximately 1,600 — one of the world's smallest. Air New Zealand twice-weekly service to Auckland. Non-resident BHC Wellington. Limited mortuary infrastructure — medical cases are routinely transferred to Auckland.",
        "complexity_rating": "moderate",
        "complexity_notes": "World's smallest self-governing state by population (approximately 1,600). Non-resident BHC Wellington. Twice-weekly Air New Zealand Auckland service. Limited local mortuary capacity — medical cases historically transferred to New Zealand. English common law. Documentation is straightforward in English.",
        "required_documents": [
            "Death certificate (Niue Registrar of Births, Deaths and Marriages)",
            "Niue Police clearance (non-natural deaths)",
            "Embalming certificate (limited local capacity)",
            "Freedom from infection certificate",
            "Export permit",
            "New Zealand transit documentation (if via Auckland)",
            "Consular registration (BHC Wellington)"
        ],
        "religion_notes": "Predominantly Christian. Ekalesia Niue (EKN, Congregationalist) is the majority denomination.",
        "cremation_available": False,
        "cremation_notes": "Cremation is not available in Niue. Full body repatriation via Auckland is required. Families may arrange cremation in New Zealand before onward repatriation to the UK.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Wellington",
            "Only Air New Zealand serves Niue — twice-weekly Auckland service",
            "World's smallest self-governing state — very limited local infrastructure",
            "New Zealand transit documentation required through Auckland"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_35.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
