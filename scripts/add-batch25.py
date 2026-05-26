"""Add Batch 25 countries to site/data/countries_repatriation.json"""
import json

BATCH25 = {
    "djibouti": {
        "country_key": "djibouti",
        "country_name": "Djibouti",
        "country_adjective": "Djiboutian",
        "flag": "\U0001f1e9\U0001f1ef",
        "region": "East Africa",
        "languages": ["French", "Arabic", "Somali", "Afar"],
        "currency": "Djiboutian Franc (DJF)",
        "british_representation": "British Embassy Addis Ababa (non-resident accreditation)",
        "embassy_type": "Non-resident",
        "embassy_city": "Addis Ababa (covering Djibouti)",
        "local_authority_involved": "Police Nationale; Ministry of Health; Tribunal de Première Instance (for non-natural deaths)",
        "main_airports": ["Djibouti-Ambouli International Airport (JIB)"],
        "routing_notes": "Djibouti via Addis Ababa (Ethiopian Airlines), Dubai (flydubai, Air Arabia), Istanbul (Turkish Airlines). Direct Addis Ababa route is primary for UK cargo connections.",
        "typical_cost_gbp_min": 7000,
        "typical_cost_gbp_max": 18000,
        "typical_cost_notes": "Non-resident Embassy adds consular coordination costs. French-language documentation requires certified translation throughout.",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "14-42 days. No resident British Embassy — all consular support via Addis Ababa. French/Arabic documentation requires certified translation. Tribunal involvement for non-natural deaths adds time.",
        "complexity_rating": "moderate",
        "complexity_notes": "Moderate complexity. No resident British Embassy in country — covered non-residently from Addis Ababa, Ethiopia. French-language civil law system. Strategic location (French and US military bases) does not affect civilian repatriation. Transit routing via Addis Ababa is well-established for UK cargo.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Medical certificate",
            "Tribunal de Première Instance clearance (non-natural deaths)",
            "Police Nationale clearance",
            "Ministry of Health export permit",
            "Certified French/Arabic-English translations"
        ],
        "religion_notes": "Islam is the state religion (Sunni). Somali and Afar communities have established Islamic burial practices. French civil law applies to civil registration regardless of religion.",
        "cremation_available": False,
        "cremation_notes": "No cremation in Djibouti. Predominantly Muslim country.",
        "no_go_zones": [
            "Areas near Djibouti-Eritrea border",
            "Remote interior near Eritrean border (disputed territory)"
        ],
        "risk_highlights": [
            "No resident British Embassy — all consular support via non-resident coverage from Addis Ababa",
            "French-language civil law system — all documentation in French requires certified translation",
            "Tribunal de Première Instance involvement for non-natural deaths — judicial process adds time"
        ]
    },
    "lesotho": {
        "country_key": "lesotho",
        "country_name": "Lesotho",
        "country_adjective": "Basotho",
        "flag": "\U0001f1f1\U0001f1f8",
        "region": "Southern Africa",
        "languages": ["Sesotho", "English"],
        "currency": "Lesotho Loti (LSL)",
        "british_representation": "British High Commission Maseru",
        "embassy_type": "High Commission",
        "embassy_city": "Maseru",
        "local_authority_involved": "Lesotho Mounted Police Service; Ministry of Health; Registrar of Births and Deaths",
        "main_airports": ["Moshoeshoe I International Airport (MSU), Maseru"],
        "routing_notes": "No direct international flights beyond Johannesburg. All routing via Johannesburg O.R. Tambo International (JNB). Maseru to JNB: South African Airlink or road transfer (~5 hours).",
        "typical_cost_gbp_min": 5000,
        "typical_cost_gbp_max": 12000,
        "typical_cost_notes": "English documentation and JNB routing keep costs manageable. Mountain terrain deaths may add recovery cost.",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 21,
        "timeline_notes": "10-21 days. English documentation throughout. All cargo via JNB. Mountain deaths in Maluti or Drakensberg ranges may require ground recovery before standard process.",
        "complexity_rating": "moderate",
        "complexity_notes": "Moderate complexity. English is official language — documentation accessible. British High Commission resident in Maseru. Lesotho is a constitutional monarchy completely surrounded by South Africa. All cargo must transit Johannesburg. Highlanders (mountain region) deaths require ground recovery — Lesotho has very limited aviation outside Maseru.",
        "required_documents": [
            "Death certificate",
            "Medical certificate",
            "Lesotho Mounted Police Service clearance",
            "Ministry of Health export permit",
            "Embalming certificate"
        ],
        "religion_notes": "Predominantly Christian (Catholic and Evangelical). No religious restrictions on repatriation.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Lesotho. All repatriations involve body transport.",
        "no_go_zones": [],
        "risk_highlights": [
            "All cargo must route via Johannesburg — no direct international air service",
            "Mountain deaths (Maluti/Drakensberg highland areas) require ground recovery before standard process",
            "British High Commission Maseru is resident and experienced"
        ]
    },
    "suriname": {
        "country_key": "suriname",
        "country_name": "Suriname",
        "country_adjective": "Surinamese",
        "flag": "\U0001f1f8\U0001f1f7",
        "region": "South America",
        "languages": ["Dutch", "Sranan Tongo", "English"],
        "currency": "Surinamese Dollar (SRD)",
        "british_representation": "British Embassy Georgetown, Guyana (non-resident accreditation for Suriname)",
        "embassy_type": "Non-resident",
        "embassy_city": "Georgetown, Guyana (covering Suriname)",
        "local_authority_involved": "Korps Politie Suriname (KPS); Bureau voor Openbare Gezondheidszorg (BOG); Civil Registry (Centraal Bureau Burgerzaken)",
        "main_airports": ["Johan Adolf Pengel International Airport (PBM), near Paramaribo"],
        "routing_notes": "Paramaribo via Miami (Surinam Airways, Caribbean Airlines), Amsterdam (KLM, TUI fly Netherlands), Port of Spain Trinidad (Caribbean Airlines). Amsterdam route most relevant for UK cargo.",
        "typical_cost_gbp_min": 6000,
        "typical_cost_gbp_max": 15000,
        "typical_cost_notes": "Dutch-language documentation requires certified translation throughout. Non-resident Embassy adds coordination cost.",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 35,
        "timeline_notes": "14-35 days. Dutch civil law system — all documentation in Dutch. No resident British Embassy — covered from Georgetown, Guyana. Interior jungle deaths add recovery time.",
        "complexity_rating": "moderate",
        "complexity_notes": "Moderate complexity. Dutch-speaking country on the South American coast, bordered by Guyana, Brazil, and French Guiana. No resident British Embassy — non-resident coverage from Georgetown. Dutch civil law framework. Interior rainforest deaths (gold mining areas, eco-tourism) require river or air recovery. Amsterdam KLM route is standard for UK cargo.",
        "required_documents": [
            "Death certificate (overlijdensakte)",
            "Medical certificate",
            "KPS police clearance",
            "BOG export permit",
            "Certified Dutch-English translations"
        ],
        "religion_notes": "Highly diverse: Hindu, Muslim, Christian (various), and Winti (Surinamese Afro-Caribbean religion). No single dominant religious framework for burial — family practice varies.",
        "cremation_available": True,
        "cremation_notes": "Cremation available in Paramaribo. Hindu community uses cremation regularly. Ashes can be transported to the UK as cremated remains.",
        "no_go_zones": [
            "Interior gold mining areas (informal settlements — Maroon and Amerindian interior territory)"
        ],
        "risk_highlights": [
            "Dutch-language civil law — all documents require certified translation",
            "No resident British Embassy — non-resident coverage from Georgetown, Guyana",
            "Interior gold mining area deaths (French Guiana border region) require river or air recovery",
            "Amsterdam KLM route is the most reliable UK cargo pathway"
        ]
    },
    "timor-leste": {
        "country_key": "timor-leste",
        "country_name": "Timor-Leste",
        "country_adjective": "Timorese",
        "flag": "\U0001f1f9\U0001f1f1",
        "region": "South-East Asia",
        "languages": ["Tetum", "Portuguese", "Indonesian", "English"],
        "currency": "US Dollar (USD)",
        "british_representation": "Australian Embassy Dili (consular assistance for British nationals under UK-Australia sharing arrangement)",
        "embassy_type": "Shared (Australian Embassy)",
        "embassy_city": "Dili",
        "local_authority_involved": "National Police of Timor-Leste (PNTL); Ministry of Health; Civil Registration Service",
        "main_airports": ["Presidente Nicolau Lobato International Airport (DIL), Dili"],
        "routing_notes": "Dili via Darwin, Australia (Airnorth); Bali, Indonesia (TransNusa, Garuda); Singapore (Silk Air/Scoot). UK routing via Bali–Singapore–London or Darwin–Sydney–London.",
        "typical_cost_gbp_min": 7000,
        "typical_cost_gbp_max": 18000,
        "typical_cost_notes": "Multi-leg routing via Indonesia or Australia adds cargo time and cost. Portuguese/Tetum documentation requires certified translation.",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "14-42 days. No resident British Embassy — Australian Embassy provides consular assistance. Portuguese-language civil law (Portuguese colonial system). Limited mortuary infrastructure outside Dili.",
        "complexity_rating": "moderate",
        "complexity_notes": "Moderate complexity. Timor-Leste became independent in 2002 — civil registration systems are still maturing. No resident British Embassy: British nationals receive consular assistance from the Australian Embassy under the UK-Australia sharing arrangement. Portuguese civil law framework. Very limited mortuary facilities outside Dili. Routing via Bali or Darwin for UK cargo.",
        "required_documents": [
            "Death certificate",
            "Medical certificate",
            "PNTL police clearance",
            "Ministry of Health export permit",
            "Certified Portuguese/Tetum-English translations"
        ],
        "religion_notes": "Predominantly Roman Catholic (over 96%). No religious restrictions on repatriation.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Timor-Leste. All repatriations involve body transport.",
        "no_go_zones": [
            "Remote border areas with Indonesia (West Timor)"
        ],
        "risk_highlights": [
            "No resident British Embassy — Australian Embassy provides consular assistance under UK-Australia sharing",
            "Portuguese-language civil law system — all documentation requires certified translation",
            "Limited mortuary infrastructure outside capital Dili",
            "Multi-leg routing via Bali or Darwin adds 1-3 days to cargo journey"
        ]
    },
    "niger": {
        "country_key": "niger",
        "country_name": "Niger",
        "country_adjective": "Nigerien",
        "flag": "\U0001f1f3\U0001f1ea",
        "region": "West Africa",
        "languages": ["French", "Hausa", "Zarma", "Tamasheq"],
        "currency": "West African CFA Franc (XOF)",
        "british_representation": "British Embassy Abuja, Nigeria (non-resident accreditation for Niger)",
        "embassy_type": "Non-resident",
        "embassy_city": "Abuja, Nigeria (covering Niger)",
        "local_authority_involved": "Police Nationale du Niger; Ministry of Public Health; Civil Status Office",
        "main_airports": ["Diori Hamani International Airport (NIM), Niamey"],
        "routing_notes": "Niamey via Addis Ababa (Ethiopian Airlines), Casablanca (Royal Air Maroc), Paris CDG (Air France, when operating). Air France and Ethiopian are the primary routes for UK cargo connections.",
        "typical_cost_gbp_min": 9000,
        "typical_cost_gbp_max": 22000,
        "typical_cost_notes": "FCDO against all but essential travel. Military junta since July 2023 has reduced international airline access. Non-resident Embassy. High specialist firm requirement.",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 90,
        "timeline_notes": "28-90 days post-coup. Military junta (CNSP) controls administrative outcomes. ECOWAS sanctions period (now partially lifted) disrupted access. French civil law documentation. Non-resident British Embassy.",
        "complexity_rating": "very-high",
        "complexity_notes": "Very high complexity. Military coup July 2023 (CNSP). FCDO advises against all but essential travel. No resident British Embassy — non-resident coverage from Abuja. French civil law documentation. Air France suspended Niamey service after the coup (service status variable). Limited international flights to Niamey. UK deaths in Niger are rare and primarily involve aid/development workers and journalists.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Medical certificate",
            "Police Nationale clearance",
            "Ministry of Public Health export permit",
            "Certified French-English translations"
        ],
        "religion_notes": "Predominantly Sunni Muslim (over 98%). Islamic burial practice is standard. French civil law applies to civil registration.",
        "cremation_available": False,
        "cremation_notes": "No cremation in Niger. Islamic burial practices predominant.",
        "no_go_zones": [
            "Regions of Diffa (Lake Chad basin, Boko Haram)",
            "Region of Tillabéri (Mali/Burkina Faso border, Sahel armed groups)",
            "Region of Tahoua (north, armed group activity)",
            "All northern desert areas near Libyan and Algerian borders"
        ],
        "risk_highlights": [
            "Military coup July 2023 — CNSP junta controls administrative outcomes",
            "FCDO advises against all but essential travel to Niger",
            "No resident British Embassy — non-resident coverage from Abuja",
            "Significant armed group activity in Tillabéri, Diffa, and Tahoua regions",
            "Air France suspended Niamey service post-coup — limited international flights"
        ]
    }
}

with open("site/data/countries_repatriation.json", encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH25.items():
    if key not in data["countries"]:
        data["countries"][key] = country
        added.append(key)
    else:
        print(f"SKIP {key} — already exists")

country_count = sum(1 for k in data["countries"] if not k.startswith("_"))
print(f"ADDED {', '.join(added)}. Total countries: {country_count}")

with open("site/data/countries_repatriation.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
