"""Add Batch 24 countries to site/data/countries_repatriation.json"""
import json

BATCH24 = {
    "brunei": {
        "country_key": "brunei",
        "country_name": "Brunei",
        "country_adjective": "Bruneian",
        "flag": "\U0001f1e7\U0001f1f3",
        "region": "South-East Asia",
        "languages": ["Malay", "English"],
        "currency": "Brunei Dollar (BND)",
        "british_representation": "British High Commission Bandar Seri Begawan",
        "embassy_type": "High Commission",
        "embassy_city": "Bandar Seri Begawan",
        "local_authority_involved": "Royal Brunei Police Force; Attorney General's Chambers; Department of Religious Affairs (for Muslim deaths)",
        "main_airports": ["Brunei International Airport (BWN)"],
        "routing_notes": "Direct flights London Heathrow to Bandar Seri Begawan (Royal Brunei Airlines RB001/RB002). Standard cargo on Royal Brunei Airlines or via Singapore SIN.",
        "typical_cost_gbp_min": 5000,
        "typical_cost_gbp_max": 12000,
        "typical_cost_notes": "Standard repatriation, no major complications expected.",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "Standard civil cases 7-14 days. Muslim deaths must follow Islamic funeral law process via Department of Religious Affairs before export clearance, which may add 2-5 days.",
        "complexity_rating": "moderate",
        "complexity_notes": "Moderate complexity. Islam is the state religion: Muslim deaths follow Sharia-based Religious Affairs process before civil export clearance. Non-Muslim expatriate deaths follow civil law only. British Garrison Brunei provides a specialist military repatriation track for service deaths.",
        "required_documents": [
            "Death certificate",
            "Medical certificate",
            "Royal Brunei Police Force clearance",
            "Attorney General clearance (non-natural deaths)",
            "Department of Religious Affairs clearance (Muslim deaths)",
            "Ministry of Health export permit",
            "Embalming certificate",
            "Certified Malay-English translations"
        ],
        "religion_notes": "Islam is the state religion. Muslim deaths require Department of Religious Affairs clearance before export. Non-Muslim deaths follow civil law. British High Commission advises on specific religious authority requirements.",
        "cremation_available": False,
        "cremation_notes": "Cremation is not available for Muslim deaths by law. Cremation technically possible for non-Muslims but extremely uncommon in Brunei.",
        "no_go_zones": [],
        "risk_highlights": [
            "Sharia law applies to Muslim deaths — Religious Affairs clearance required before export",
            "British Garrison Brunei provides specialist military repatriation track for service deaths",
            "Direct Royal Brunei Airlines London Heathrow to BWN simplifies cargo routing"
        ]
    },
    "democratic-republic-of-congo": {
        "country_key": "democratic-republic-of-congo",
        "country_name": "Democratic Republic of Congo",
        "country_adjective": "Congolese",
        "flag": "\U0001f1e8\U0001f1e9",
        "region": "Central Africa",
        "languages": ["French", "Lingala", "Swahili", "Kikongo"],
        "currency": "Congolese Franc (CDF)",
        "british_representation": "British Embassy Kinshasa",
        "embassy_type": "Embassy",
        "embassy_city": "Kinshasa",
        "local_authority_involved": "Parquet (state prosecutor); Police Nationale Congolaise; Institut National Medico-Legal (INML)",
        "main_airports": [
            "Ndjili International Airport (FIH), Kinshasa",
            "Goma International Airport (GOM)"
        ],
        "routing_notes": "Kinshasa via Brussels (Brussels Airlines), Addis Ababa (Ethiopian Airlines), Nairobi (Kenya Airways). Eastern DRC (Goma) may route via Nairobi or Kigali.",
        "typical_cost_gbp_min": 9000,
        "typical_cost_gbp_max": 25000,
        "typical_cost_notes": "Wide range reflecting significant variation by location — Kinshasa accessible vs. eastern provinces highly complex or inaccessible.",
        "typical_timeline_days_min": 21,
        "typical_timeline_days_max": 84,
        "timeline_notes": "Kinshasa standard cases 21-42 days. Eastern DRC conflict areas (North Kivu, South Kivu, Ituri) significantly longer where accessible at all. Bodies in active combat areas may not be recoverable.",
        "complexity_rating": "very-high",
        "complexity_notes": "Very high complexity. Ongoing armed conflict in eastern provinces. Bureaucratic layers in Kinshasa. INML capacity is limited. FCDO advises against all travel to eastern DRC provinces. Repatriation from Kinshasa is achievable; from conflict zones it may not be.",
        "required_documents": [
            "Death certificate (acte de deces)",
            "Medical certificate",
            "Parquet clearance",
            "INML forensic certificate (non-natural deaths)",
            "Police Nationale Congolaise clearance",
            "Ministry of Health export permit",
            "Certified French-English translations"
        ],
        "religion_notes": "Predominantly Christian (Catholic, Protestant, Kimbanguist). Local funeral practices vary significantly by region and community.",
        "cremation_available": False,
        "cremation_notes": "No commercial cremation facilities in DRC.",
        "no_go_zones": [
            "North Kivu",
            "South Kivu",
            "Ituri province",
            "Tanganyika province conflict areas",
            "Areas near DRC-Rwanda border",
            "Areas near DRC-Uganda border"
        ],
        "risk_highlights": [
            "Ongoing armed conflict in eastern DRC — repatriation may not be achievable from conflict zones",
            "FCDO advises against all travel to North Kivu, South Kivu, and Ituri",
            "INML forensic capacity in Kinshasa is limited — delays common",
            "Bodies in eastern conflict areas may be inaccessible"
        ]
    },
    "eritrea": {
        "country_key": "eritrea",
        "country_name": "Eritrea",
        "country_adjective": "Eritrean",
        "flag": "\U0001f1ea\U0001f1f7",
        "region": "East Africa",
        "languages": ["Tigrinya", "Arabic", "English"],
        "currency": "Eritrean Nakfa (ERN)",
        "british_representation": "British Embassy Asmara",
        "embassy_type": "Embassy",
        "embassy_city": "Asmara",
        "local_authority_involved": "Ministry of Health; Regional Administration; National Security (PFDJ)",
        "main_airports": ["Asmara International Airport (ASM)"],
        "routing_notes": "Asmara via Cairo (EgyptAir), Dubai (connections via Ethiopian Airlines or flydubai), Addis Ababa (Ethiopian Airlines). Limited direct international service.",
        "typical_cost_gbp_min": 8000,
        "typical_cost_gbp_max": 20000,
        "typical_cost_notes": "High costs reflect limited airline access, specialist firm requirement, and unpredictable timelines.",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 90,
        "timeline_notes": "28-90 days. The government controls all administrative processes. Delays occur without explanation. Families should plan for the maximum end of this range.",
        "complexity_rating": "very-high",
        "complexity_notes": "Very high complexity. Eritrea operates as one of the world's most closed states. Government (PFDJ) controls all administrative outcomes. British Embassy Asmara has limited capacity to intervene in domestic processes. UK-Eritrean diaspora repatriations are the primary use case.",
        "required_documents": [
            "Death certificate",
            "Medical certificate",
            "Ministry of Health clearance",
            "Regional Administration clearance",
            "National Security clearance (may be required)",
            "Export permit",
            "Certified Tigrinya/Arabic-English translations"
        ],
        "religion_notes": "Predominantly Eritrean Orthodox Christian and Sunni Muslim. Both religious communities have established burial practices. Government controls all religious institutions.",
        "cremation_available": False,
        "cremation_notes": "No cremation in Eritrea. Orthodox Christian and Islamic burial practices predominant.",
        "no_go_zones": [
            "Eritrean-Ethiopian border areas",
            "Eritrean-Djibouti border areas",
            "Eritrean-Sudanese border areas"
        ],
        "risk_highlights": [
            "One of the world's most closed states — government controls all administrative outcomes",
            "National security clearance may be required without prior notice",
            "British Embassy Asmara has limited ability to intervene in domestic processes",
            "UK-Eritrean diaspora is the primary use case for this repatriation route"
        ]
    },
    "mongolia": {
        "country_key": "mongolia",
        "country_name": "Mongolia",
        "country_adjective": "Mongolian",
        "flag": "\U0001f1f2\U0001f1f3",
        "region": "East Asia",
        "languages": ["Mongolian"],
        "currency": "Mongolian Togrog (MNT)",
        "british_representation": "British Embassy Ulaanbaatar",
        "embassy_type": "Embassy",
        "embassy_city": "Ulaanbaatar",
        "local_authority_involved": "National Police Agency; State Forensic Science Center; Civil Registration and Information Department",
        "main_airports": ["Chinggis Khaan International Airport (UBN), Ulaanbaatar"],
        "routing_notes": "Ulaanbaatar via Beijing (MIAT Mongolian Airlines, Air China), Seoul (Korean Air, MIAT). No direct UK-Mongolia service. Beijing or Seoul are the primary cargo transit points.",
        "typical_cost_gbp_min": 6000,
        "typical_cost_gbp_max": 15000,
        "typical_cost_notes": "Remote interior recovery adds significant cost above urban Ulaanbaatar cases.",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 35,
        "timeline_notes": "14-35 days. State Forensic Science Center required for non-natural deaths. Remote steppe, Gobi desert, or Altai mountain deaths add body recovery time before standard process begins.",
        "complexity_rating": "moderate",
        "complexity_notes": "Moderate complexity. State Forensic Science Center handles all non-natural deaths. Remote death locations (Gobi desert, steppe, Altai mountains) require helicopter or ground recovery — a UK adventure tourism factor. British Embassy Ulaanbaatar is resident and experienced with UK traveller deaths.",
        "required_documents": [
            "Death certificate",
            "Medical certificate",
            "State Forensic Science Center certificate (non-natural deaths)",
            "National Police Agency clearance",
            "Civil Registration certificate",
            "Ministry of Health export permit",
            "Certified Mongolian-English translations"
        ],
        "religion_notes": "Predominantly Tibetan Buddhist and shamanist. No religious restrictions on repatriation. Urban Ulaanbaatar cases largely follow civil process.",
        "cremation_available": True,
        "cremation_notes": "Cremation available in Ulaanbaatar. No cremation facilities outside urban centres.",
        "no_go_zones": [],
        "risk_highlights": [
            "Remote deaths (Gobi desert, steppe, Altai) require specialist body recovery before standard process",
            "Adventure tourism and horse trekking a growing UK traveller segment with associated death risk",
            "New Chinggis Khaan International Airport opened 2021 — cargo routing updated from old Buyant-Ukhaa airport"
        ]
    },
    "eswatini": {
        "country_key": "eswatini",
        "country_name": "Eswatini",
        "country_adjective": "Swazi",
        "flag": "\U0001f1f8\U0001f1ff",
        "region": "Southern Africa",
        "languages": ["siSwati", "English"],
        "currency": "Swazi Lilangeni (SZL)",
        "british_representation": "British High Commission Mbabane",
        "embassy_type": "High Commission",
        "embassy_city": "Mbabane",
        "local_authority_involved": "Royal Eswatini Police Service; Ministry of Health; Registrar General",
        "main_airports": [
            "King Mswati III International Airport (SHO)",
            "Matsapha Airport (MTS)"
        ],
        "routing_notes": "No direct UK-Eswatini service. All routing via Johannesburg O.R. Tambo International (JNB) with multiple daily connections to London Heathrow. Alternatively via Nairobi NBO or Addis Ababa ADD.",
        "typical_cost_gbp_min": 5000,
        "typical_cost_gbp_max": 11000,
        "typical_cost_notes": "Standard Southern Africa routing via Johannesburg. English-language process reduces administrative cost.",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 21,
        "timeline_notes": "10-21 days for standard cases. English-language documentation throughout. JNB transit adds 1-2 days compared to direct-flight destinations.",
        "complexity_rating": "moderate",
        "complexity_notes": "Moderate complexity. English is an official language — documentation accessible. British High Commission Mbabane resident. Absolute monarchy: all administrative decisions are ultimately centralised through royal government structures, which creates predictability in process but limited room to challenge delays.",
        "required_documents": [
            "Death certificate",
            "Medical certificate",
            "Royal Eswatini Police Service clearance",
            "Ministry of Health export permit",
            "Embalming certificate"
        ],
        "religion_notes": "Mixed Christian (Zionist, Catholic, Protestant) and Swazi traditional religion. No religious restrictions on repatriation.",
        "cremation_available": False,
        "cremation_notes": "No commercial cremation facilities in Eswatini. All repatriations involve body transport.",
        "no_go_zones": [],
        "risk_highlights": [
            "All routing via Johannesburg JNB — cargo specialist with JNB experience essential",
            "Absolute monarchy centralises all administrative decisions",
            "English-language documentation throughout simplifies process significantly"
        ]
    }
}

with open("site/data/countries_repatriation.json", encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH24.items():
    if key not in data["countries"]:
        data["countries"][key] = country
        added.append(key)
    else:
        print(f"SKIP {key} — already exists")

data["_metadata"]["total_countries"] = len(data["countries"]) - 1  # exclude _metadata key if present
# Recalculate — count only actual country entries
country_count = sum(1 for k in data["countries"] if not k.startswith("_"))
print(f"ADDED {', '.join(added)}. Total countries: {country_count}")

with open("site/data/countries_repatriation.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
