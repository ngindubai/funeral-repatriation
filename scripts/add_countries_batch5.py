import json, pathlib

DATA = pathlib.Path(__file__).parent.parent / "site" / "data" / "countries_repatriation.json"

NEW_COUNTRIES = {
    "romania": {
        "name": "Romania",
        "flag": "🇷🇴",
        "region": "Europe",
        "eu_member": True,
        "strasbourg_signatory": True,
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "10-14 days",
            "complex_case": "21+ days",
            "complexity_factors": ["Prosecutor post-mortem for unnatural death adds 5-10 days", "Rural deaths require transfer to Bucharest or regional IML institute", "Romanian documentation requires certified translation"]
        },
        "cost_range_gbp": {
            "min": 3000,
            "max": 6500,
            "notes": "Affordable European origin. Travel insurance covers in most standard policies."
        },
        "documentation_required": [
            "Romanian death certificate (Certificat de deces) from Starea Civila",
            "Post-mortem report (if applicable, from Institute of Forensic Medicine)",
            "Prosecutor release authorisation (for unnatural deaths)",
            "Embalming certificate",
            "Freedom from contagious disease certificate",
            "Laissez-passer (from County Council or local authority)",
            "Certified translations into English of all documents"
        ],
        "key_authorities": {
            "death_registration": "Starea Civila (Civil Status Office) in the district of death",
            "post_mortem": "Institute of Forensic Medicine (Institut de Medicina Legala)",
            "release_authorisation": "Prosecutor's Office (Parchet)",
            "export_permit": "County Council (Consiliul Judetean) or local authority"
        },
        "british_consulate": {
            "name": "British Embassy Bucharest",
            "address": "Strada Jules Michelet 24, 010463 Bucharest",
            "phone": "+40 21 207 2000",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["OTP (Henri Coanda International, Bucharest)", "CLJ (Cluj-Napoca)"],
        "airlines": ["TAROM", "Ryanair", "Wizz Air", "British Airways"],
        "direct_uk_flights": True,
        "embalming_required": True,
        "cremation_available": True,
        "repatriation_complexity": "low",
        "ashes_transport_days_estimate": "3-5 days from Bucharest once documentation complete",
        "notable_considerations": [
            "Large Romanian diaspora in UK means many funeral directors on both sides are experienced with this route",
            "Strasbourg Agreement simplifies documentation compared to non-signatory countries",
            "Multiple Wizz Air and Ryanair daily departures from Bucharest Otopeni (OTP) to Luton, Stansted, and other UK airports"
        ]
    },
    "albania": {
        "name": "Albania",
        "flag": "🇦🇱",
        "region": "Europe",
        "eu_member": False,
        "strasbourg_signatory": True,
        "typical_timeline": {
            "fastest_case": "10 days",
            "average_case": "14-21 days",
            "complex_case": "28+ days",
            "complexity_factors": ["Prosecutor post-mortem for unnatural deaths adds 7-14 days", "Infrastructure outside Tirana is less developed", "All documentation in Albanian requires certified translation", "Limited direct flight options from Tirana"]
        },
        "cost_range_gbp": {
            "min": 3500,
            "max": 7500,
            "notes": "Slightly higher than Western European origins due to routing complexity and less developed infrastructure."
        },
        "documentation_required": [
            "Albanian death certificate (Certifikate vdekje) from RGJC",
            "Post-mortem report (if applicable)",
            "Prosecutor release authorisation (for unnatural deaths)",
            "Embalming certificate",
            "Freedom from contagious disease certificate",
            "Laissez-passer from Ministry of Interior or local authority",
            "Certified translations into English of all documents"
        ],
        "key_authorities": {
            "death_registration": "RGJC (National Civil Registry) local office",
            "post_mortem": "Institute of Forensic Medicine (Institut i Mjekesise Ligjore), Tirana",
            "release_authorisation": "Prosecutor's Office (Prokuroria)",
            "export_permit": "Ministry of Interior or local prefecture"
        },
        "british_consulate": {
            "name": "British Embassy Tirana",
            "address": "Rruga Skenderbej 12, Tirana",
            "phone": "+355 4 223 4973",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["TIA (Tirana International Nene Tereza)"],
        "airlines": ["Air Albania", "Ryanair", "Wizz Air", "British Airways (via connections)"],
        "direct_uk_flights": True,
        "embalming_required": True,
        "cremation_available": True,
        "repatriation_complexity": "medium",
        "ashes_transport_days_estimate": "4-7 days from Tirana once documentation complete",
        "notable_considerations": [
            "Albania is a Council of Europe member and Strasbourg Agreement signatory, which simplifies documentation",
            "Growing tourist destination with increasing numbers of British visitors to the Albanian Riviera",
            "Limited direct flights to the UK — Ryanair and Wizz Air serve Luton and other airports but frequency is lower than Western European routes",
            "Albanian language is linguistically isolated; certified translation is essential"
        ]
    },
    "colombia": {
        "name": "Colombia",
        "flag": "🇨🇴",
        "region": "South America",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "14 days",
            "average_case": "18-25 days",
            "complex_case": "35+ days",
            "complexity_factors": ["Instituto de Medicina Legal post-mortem adds 7-14 days", "Deaths in tourist areas (Cartagena, Medellin, coffee region) require transfer to Bogota for international air cargo", "Multi-leg routing via Miami or Madrid adds transit time", "Spanish documentation requires certified translation"]
        },
        "cost_range_gbp": {
            "min": 4500,
            "max": 9500,
            "notes": "Higher cost reflects multi-leg routing and longer timelines. Adventure travel insurance essential."
        },
        "documentation_required": [
            "Colombian death certificate (Registro Civil de Defuncion) from DANE notary",
            "Instituto de Medicina Legal post-mortem report (for unnatural deaths)",
            "Fiscalia (Attorney General) release authorisation (for criminal or suspicious deaths)",
            "Embalming certificate from licensed mortuary",
            "Freedom from contagious disease clearance",
            "Health permit for export of human remains (INVIMA)",
            "British Embassy apostille or consular legalisation",
            "Certified translations into English of all documents"
        ],
        "key_authorities": {
            "death_registration": "Notaria (notary office) for Registro Civil de Defuncion",
            "post_mortem": "Instituto de Medicina Legal (IML) and Ciencias Forenses",
            "release_authorisation": "Fiscalia General de la Nacion (for criminal cases)",
            "export_permit": "INVIMA (National Institute for Food and Drug Surveillance)"
        },
        "british_consulate": {
            "name": "British Embassy Bogota",
            "address": "Carrera 9 No. 76-49, Bogota",
            "phone": "+57 1 326 8300",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["BOG (El Dorado International, Bogota)", "MDE (Jose Maria Cordova, Medellin)", "CTG (Rafael Nunez, Cartagena)"],
        "airlines": ["Avianca", "Copa Airlines", "American Airlines", "British Airways (via connections)"],
        "direct_uk_flights": False,
        "embalming_required": True,
        "cremation_available": True,
        "repatriation_complexity": "high",
        "ashes_transport_days_estimate": "5-10 days from Bogota once documentation complete",
        "notable_considerations": [
            "No direct flights to the UK from Colombia; routing is via Miami, Panama City, or Madrid — add 1-2 days for cargo routing",
            "Growing adventure tourism destination: coffee region, Tayrona park, Lost City trek all attract British visitors",
            "Deaths in remote areas (jungle, mountain regions) require recovery and transfer before any documentation begins",
            "INVIMA export permit is specific to Colombia and often unfamiliar to UK funeral directors without Latin America experience"
        ]
    },
    "china": {
        "name": "China",
        "flag": "🇨🇳",
        "region": "Asia",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "14 days",
            "average_case": "21-28 days",
            "complex_case": "45+ days",
            "complexity_factors": ["Public Security Bureau investigation for unnatural deaths adds 7-21 days", "Chinese documentation requires certified translation and authentication", "Approved mortuary required — not all provinces have facilities meeting international standards", "COVID-era restrictions on international remains movement have eased but documentation requirements remain complex"]
        },
        "cost_range_gbp": {
            "min": 5000,
            "max": 12000,
            "notes": "Among the most expensive Asian repatriations due to complexity, documentation volume, and authentication requirements."
        },
        "documentation_required": [
            "Chinese death certificate (Si Wang Yi Zheng Shu) from Ministry of Civil Affairs",
            "Public Security Bureau (PSB) report (for unnatural deaths)",
            "Forensic post-mortem report (for PSB-referred cases)",
            "Embalming certificate from an approved mortuary",
            "Freedom from contagious disease certificate (Jian Yi Zheng Shu) from Customs",
            "Chinese exit permit for human remains (issued by local Civil Affairs Bureau)",
            "British Embassy Beijing consular death certificate or certified copy",
            "Authenticated certified translations of all Chinese-language documents"
        ],
        "key_authorities": {
            "death_registration": "Local Civil Affairs Bureau (Minzheng Ju)",
            "post_mortem": "Forensic department of the Public Security Bureau (PSB)",
            "release_authorisation": "Public Security Bureau (for unnatural deaths)",
            "export_permit": "Local Civil Affairs Bureau exit permit; Chinese Customs clearance"
        },
        "british_consulate": {
            "name": "British Embassy Beijing",
            "address": "11 Guang Hua Lu, Chaoyang District, Beijing 100600",
            "phone": "+86 10 5192 4000",
            "emergency": "+44 1908 516666",
            "additional_posts": ["British Consulate-General Shanghai", "British Consulate-General Guangzhou", "British Consulate-General Chengdu", "British Consulate-General Wuhan"]
        },
        "main_airports": ["PEK/PKX (Beijing Capital / Daxing International)", "PVG (Shanghai Pudong)", "CAN (Guangzhou Baiyun)", "CTU (Chengdu Tianfu)"],
        "airlines": ["Air China", "China Eastern", "British Airways", "Virgin Atlantic"],
        "direct_uk_flights": True,
        "embalming_required": True,
        "cremation_available": True,
        "repatriation_complexity": "very_high",
        "ashes_transport_days_estimate": "7-14 days from point of exit once documentation complete",
        "notable_considerations": [
            "China does not recognise the Strasbourg Agreement; all documentation follows Chinese domestic law and bilateral consular conventions",
            "Specialist Chinese-language funeral directors are essential — a generalist UK firm without China experience will struggle",
            "The approved mortuary must be pre-cleared by local Civil Affairs; families should not engage any facility until the Embassy advises",
            "Direct BA and Virgin flights from Beijing and Shanghai to Heathrow are an advantage, but cargo booking requires all documentation to be cleared first"
        ]
    },
    "hong-kong": {
        "name": "Hong Kong",
        "flag": "🇭🇰",
        "region": "Asia",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "10 days",
            "average_case": "14-21 days",
            "complex_case": "30+ days",
            "complexity_factors": ["Coroner's inquest for unnatural deaths adds 7-21 days; Coroner's Court system is thorough", "Deaths require Coroner's permission to remove the body from Hong Kong", "Documentation requires authentication for UK use"]
        },
        "cost_range_gbp": {
            "min": 4000,
            "max": 8000,
            "notes": "Higher cost than mainland China due to Coroner's Court timelines. Direct frequent flights to Heathrow contain some costs."
        },
        "documentation_required": [
            "Hong Kong death certificate from Births Deaths and Marriages Registry",
            "Coroner's Court order permitting removal (for unnatural or sudden deaths)",
            "Post-mortem report (if ordered by Coroner)",
            "Embalming certificate from licensed funeral director",
            "Freedom from contagious disease certificate (from Department of Health)",
            "Export permit for human remains (Department of Health, Cap. 132)",
            "British Consulate-General consular death certificate or certified copy"
        ],
        "key_authorities": {
            "death_registration": "Births Deaths and Marriages Registry (BDMR)",
            "post_mortem": "Government Forensic Pathologist (under Coroner's Court jurisdiction)",
            "release_authorisation": "Coroner's Court (Coroner's Office)",
            "export_permit": "Department of Health under Public Health and Municipal Services Ordinance (Cap. 132)"
        },
        "british_consulate": {
            "name": "British Consulate-General Hong Kong",
            "address": "1 Supreme Court Road, Admiralty, Hong Kong",
            "phone": "+852 2901 3000",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["HKG (Hong Kong International Airport)"],
        "airlines": ["Cathay Pacific", "British Airways", "Virgin Atlantic"],
        "direct_uk_flights": True,
        "embalming_required": True,
        "cremation_available": True,
        "repatriation_complexity": "medium",
        "ashes_transport_days_estimate": "3-5 days from Hong Kong once Coroner's permission granted",
        "notable_considerations": [
            "Hong Kong operates a separate legal system from mainland China under One Country Two Systems; do not confuse mainland China procedures with Hong Kong procedures",
            "The Coroner's Court system in Hong Kong is modelled on the UK system and is familiar to experienced repatriation specialists",
            "Cathay Pacific and British Airways both operate direct daily flights to Heathrow — among the best-connected routes from Asia",
            "Significant British expat community means British Consulate-General staff are experienced with repatriation cases"
        ]
    }
}

with open(DATA, "r", encoding="utf-8") as f:
    data = json.load(f)

for key, val in NEW_COUNTRIES.items():
    data["countries"][key] = val

data["_metadata"]["total_countries"] = len(data["countries"])

with open(DATA, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Done. Total countries: {len(data['countries'])}")
