"""
Add Batch 27 countries to site/data/countries_repatriation.json
Countries: Guinea, Liberia, Chad, Mauritania, Central African Republic
"""
import json

PATH = "site/data/countries_repatriation.json"

batch27 = {
    "guinea": {
        "country_key": "guinea",
        "country_name": "Guinea",
        "country_adjective": "Guinean",
        "flag": "🇬🇳",
        "region": "West Africa",
        "languages": ["French"],
        "currency": "Guinean franc (GNF)",
        "british_representation": "Non-resident — British High Commission Freetown, Sierra Leone",
        "embassy_type": "Non-resident",
        "embassy_city": "Freetown (non-resident)",
        "local_authority_involved": "Gendarmerie Nationale, Tribunal de Première Instance, Ministry of Health",
        "main_airports": ["Conakry-Gbessia International Airport (CKY)"],
        "routing_notes": "Air France via Paris CDG (primary UK route); Royal Air Maroc via Casablanca; Ethiopian Airlines via Addis Ababa; Brussels Airlines via Brussels.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "Military junta (CNRD under Col. Doumbouya) since September 2021. Administrative processes run through junta-controlled channels but have remained broadly functional in Conakry.",
        "complexity_rating": "high",
        "complexity_notes": "Military junta (CNRD) since September 2021 coup. FCDO advises against all but essential travel. French civil law. Non-resident Embassy via Freetown. Air France maintains Conakry service. Gendarmerie clearance and Tribunal de Première Instance required for non-natural deaths.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Gendarmerie Nationale clearance",
            "Tribunal de Première Instance order (non-natural deaths)",
            "Ministry of Health export permit",
            "Certified English translations"
        ],
        "religion_notes": "Predominantly Muslim. Islamic burial customs — pressure for rapid interment.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available in Guinea.",
        "no_go_zones": [
            "Forested region (N'Zérékoré area) — periodic inter-communal violence"
        ],
        "risk_highlights": [
            "Military junta (CNRD) since September 2021",
            "FCDO all-but-essential advisory",
            "Non-resident Embassy — coordination via Freetown",
            "Islamic burial pressure for rapid interment"
        ]
    },
    "liberia": {
        "country_key": "liberia",
        "country_name": "Liberia",
        "country_adjective": "Liberian",
        "flag": "🇱🇷",
        "region": "West Africa",
        "languages": ["English"],
        "currency": "Liberian dollar (LRD)",
        "british_representation": "British Embassy Monrovia",
        "embassy_type": "Resident",
        "embassy_city": "Monrovia",
        "local_authority_involved": "Liberia National Police, Ministry of Health, Vital Statistics Division",
        "main_airports": ["Roberts International Airport (ROB)"],
        "routing_notes": "Brussels Airlines via Brussels (primary UK route); Ethiopian Airlines via Addis Ababa; Air Maroc via Casablanca. Roberts International Airport is 60km from Monrovia.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 35,
        "timeline_notes": "English-language documentation throughout. Resident British Embassy. Process relatively straightforward for Monrovia cases. Infrastructure outside Monrovia is limited.",
        "complexity_rating": "moderate",
        "complexity_notes": "English-speaking West African country with resident British Embassy. Civil registration through Vital Statistics Division. Liberia National Police clearance for non-natural deaths. Limited infrastructure outside Monrovia — rubber plantation and mining death cases may require road transfer to capital.",
        "required_documents": [
            "Death certificate",
            "Liberia National Police clearance",
            "Ministry of Health export permit",
            "Embalming certificate"
        ],
        "religion_notes": "Mixed Christian (majority), Muslim, and indigenous beliefs.",
        "cremation_available": False,
        "cremation_notes": "Cremation not widely available in Liberia.",
        "no_go_zones": [],
        "risk_highlights": [
            "Roberts International Airport is 60km from Monrovia",
            "Infrastructure outside Monrovia severely limited",
            "Limited mortuary facilities outside capital"
        ]
    },
    "chad": {
        "country_key": "chad",
        "country_name": "Chad",
        "country_adjective": "Chadian",
        "flag": "🇹🇩",
        "region": "Central Africa",
        "languages": ["French", "Arabic"],
        "currency": "Central African CFA franc (XAF)",
        "british_representation": "Non-resident — British Embassy Yaoundé, Cameroon",
        "embassy_type": "Non-resident",
        "embassy_city": "Yaoundé (non-resident)",
        "local_authority_involved": "Police Nationale Tchadienne, Tribunal correctionnel, Ministry of Public Health",
        "main_airports": ["Hassan Djamous N'Djamena International Airport (NDJ)"],
        "routing_notes": "Ethiopian Airlines via Addis Ababa (ADD); Air France via Paris CDG (N'Djamena service); Royal Air Maroc via Casablanca. Ethiopian Airlines most reliable UK cargo route.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 84,
        "timeline_notes": "Transitional military authority controls administration following 2021 transition. FCDO advises against all but essential travel. Conflict in eastern and northern regions. Non-resident Embassy adds coordination layer.",
        "complexity_rating": "very-high",
        "complexity_notes": "Chad is one of the world's most fragile states. Transitional Military Council (CMT) under Mahamat Idriss Déby controls government since April 2021. FCDO advises against all travel to northern, eastern, and southern border regions. Conflict with armed groups ongoing. Non-resident Embassy via Yaoundé.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Police Nationale Tchadienne clearance",
            "Tribunal correctionnel order (non-natural deaths)",
            "Ministry of Public Health export permit",
            "Certified English translations"
        ],
        "religion_notes": "Predominantly Muslim in north; Christian and animist in south.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available in Chad.",
        "no_go_zones": [
            "Northern Chad (Tibesti, Borkou — FCDO against all travel)",
            "Eastern Chad (border with Sudan — armed conflict spillover)",
            "Southern border regions (CAR border)",
            "Lake Chad region (Boko Haram/ISWAP activity)"
        ],
        "risk_highlights": [
            "Transitional Military Council controls administration",
            "FCDO all-but-essential for N'Djamena; against all travel for border regions",
            "Non-resident Embassy — coordination via Yaoundé",
            "Eastern Chad: Sudan conflict spillover including refugee crisis"
        ]
    },
    "mauritania": {
        "country_key": "mauritania",
        "country_name": "Mauritania",
        "country_adjective": "Mauritanian",
        "flag": "🇲🇷",
        "region": "West Africa",
        "languages": ["Arabic", "French"],
        "currency": "Mauritanian ouguiya (MRU)",
        "british_representation": "Non-resident — British Embassy Rabat, Morocco",
        "embassy_type": "Non-resident",
        "embassy_city": "Rabat (non-resident)",
        "local_authority_involved": "Police Nationale, Parquet (civil registrar), Ministry of Health",
        "main_airports": ["Nouakchott-Oumtounsy International Airport (NKC)"],
        "routing_notes": "Royal Air Maroc via Casablanca (CMN — primary UK route); Air Mauritanie domestic; Turkish Airlines via Istanbul. Casablanca connection most reliable for UK cargo.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "Civilian government with strong military influence. Administrative process broadly functional in Nouakchott. Non-resident Embassy via Rabat adds coordination time. Saharan desert recovery cases extremely difficult.",
        "complexity_rating": "high",
        "complexity_notes": "Mauritania bridges the Maghreb and sub-Saharan West Africa. Predominantly Arabic and French documentation. Non-resident Embassy coverage from Rabat. FCDO advises against all travel to the Saharan interior (risk of kidnap by armed groups). Civil law system based on French model but supplemented by Islamic personal status law.",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Police Nationale clearance",
            "Parquet judicial clearance (non-natural deaths)",
            "Ministry of Health export permit",
            "Certified English translations"
        ],
        "religion_notes": "Almost entirely Sunni Muslim. Strong Islamic burial pressure — rapid interment expected.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available. Contrary to Islamic law.",
        "no_go_zones": [
            "Saharan interior (risk of kidnap — FCDO against all travel)",
            "Eastern border areas near Mali"
        ],
        "risk_highlights": [
            "Non-resident Embassy — coordination via Rabat",
            "FCDO against all travel to Saharan interior",
            "Islamic burial pressure for rapid interment",
            "Arabic-language documentation — translation required"
        ]
    },
    "central-african-republic": {
        "country_key": "central-african-republic",
        "country_name": "Central African Republic",
        "country_adjective": "Central African",
        "flag": "🇨🇫",
        "region": "Central Africa",
        "languages": ["French", "Sango"],
        "currency": "Central African CFA franc (XAF)",
        "british_representation": "Non-resident — British Embassy Yaoundé, Cameroon",
        "embassy_type": "Non-resident",
        "embassy_city": "Yaoundé (non-resident)",
        "local_authority_involved": "Forces Armées Centrafricaines (FACA), Ministry of Health, civil registrar",
        "main_airports": ["Bangui M'Poko International Airport (BGF)"],
        "routing_notes": "Ethiopian Airlines via Addis Ababa (ADD); Air France via Paris CDG (BGF service); Kenya Airways via Nairobi. Ethiopian Airlines most reliable UK cargo route.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 90,
        "timeline_notes": "FCDO advises against all but essential travel to Bangui and against all travel to the rest of the country. Armed groups (including ex-Séléka and anti-Balaka factions) control large parts of the country. Cases outside Bangui are not achievable.",
        "complexity_rating": "very-high",
        "complexity_notes": "CAR is consistently ranked among the world's most fragile states. Russian Wagner Group (Africa Corps) has significant influence. MINUSCA UN peacekeeping force present. Armed groups control most of the country outside Bangui. Non-resident Embassy via Yaoundé. FCDO against all travel except Bangui (all-but-essential).",
        "required_documents": [
            "Death certificate (acte de décès)",
            "Police/FACA clearance",
            "Ministry of Health export permit",
            "Certified English translations"
        ],
        "religion_notes": "Mixed Christian, Muslim, and animist.",
        "cremation_available": False,
        "cremation_notes": "Cremation not available in CAR.",
        "no_go_zones": [
            "All areas outside Bangui (FCDO against all travel)",
            "Border regions with Sudan, South Sudan, DRC, Cameroon, Congo"
        ],
        "risk_highlights": [
            "FCDO against all travel outside Bangui",
            "Armed groups control most of the country",
            "Non-resident Embassy — coordination via Yaoundé",
            "Wagner/Africa Corps influence on government operations",
            "UN MINUSCA present but country remains severely unstable"
        ]
    }
}

data = json.load(open(PATH, encoding='utf-8'))
added = []
for key, country in batch27.items():
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
