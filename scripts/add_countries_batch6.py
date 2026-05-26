import json, pathlib

DATA = pathlib.Path(__file__).parent.parent / "site" / "data" / "countries_repatriation.json"

NEW_COUNTRIES = {
    "oman": {
        "name": "Oman",
        "flag": "🇴🇲",
        "region": "Middle East",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "10 days",
            "average_case": "14-21 days",
            "complex_case": "30+ days",
            "complexity_factors": [
                "Royal Oman Police investigation for unnatural deaths adds 7-14 days",
                "Ministry of Health NOC required before export",
                "All documentation in Arabic requires certified translation",
                "Limited direct flights to UK; routing via Dubai or Doha typical"
            ]
        },
        "cost_range_gbp": {
            "min": 4000,
            "max": 8500,
            "notes": "Costs reflect Middle East routing complexity. Most travel insurance policies cover Oman."
        },
        "documentation_required": [
            "Omani death certificate from Civil Status Authority (Arabic)",
            "Royal Oman Police report (for unnatural deaths)",
            "Ministry of Health No Objection Certificate (NOC) for export",
            "Embalming certificate from licensed mortuary",
            "Freedom from contagious disease certificate",
            "British Embassy Muscat consular death certificate or certified copy",
            "Certified translations into English of all Arabic documents"
        ],
        "key_authorities": {
            "death_registration": "Civil Status Authority (Hayat al-Ahwal al-Madaniya)",
            "post_mortem": "Royal Oman Police forensic department",
            "release_authorisation": "Royal Oman Police (for unnatural deaths)",
            "export_permit": "Ministry of Health NOC"
        },
        "british_consulate": {
            "name": "British Embassy Muscat",
            "address": "PO Box 185, Mina Al Fahal, Muscat 116",
            "phone": "+968 2460 9000",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["MCT (Muscat International)"],
        "airlines": ["Oman Air", "British Airways (via connections)", "Emirates", "Qatar Airways"],
        "direct_uk_flights": False,
        "embalming_required": True,
        "cremation_available": False,
        "repatriation_complexity": "medium",
        "ashes_transport_days_estimate": "4-7 days from Muscat once documentation complete",
        "notable_considerations": [
            "Oman is a Muslim-majority country; cremation is not available for Muslim nationals. For non-Muslim British nationals, cremation at licensed facilities may be possible but must be confirmed with the Embassy",
            "No direct flights to UK; routing via Dubai (Emirates) or Doha (Qatar Airways) is standard for cargo",
            "Growing tourism destination: Muscat, Salalah, and Wahiba Sands attract increasing numbers of British visitors",
            "Arabic documentation requires certified translation — allow for this in timeline"
        ]
    },
    "argentina": {
        "name": "Argentina",
        "flag": "🇦🇷",
        "region": "South America",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "14 days",
            "average_case": "18-28 days",
            "complex_case": "40+ days",
            "complexity_factors": [
                "Judicial order required for unnatural deaths; Argentine judiciary can be slow outside Buenos Aires",
                "No direct flights to UK; routing via Madrid, São Paulo, or Miami",
                "Deaths in Patagonia, Mendoza, or Iguazu require transfer to Buenos Aires",
                "Spanish documentation requires certified translation"
            ]
        },
        "cost_range_gbp": {
            "min": 4500,
            "max": 9500,
            "notes": "Multi-leg routing and longer timelines drive higher cost. Adventure travel insurance important for Patagonia visitors."
        },
        "documentation_required": [
            "Argentine death certificate (Acta de Defuncion) from Registro Civil",
            "Judicial order permitting release of body (for unnatural/violent deaths)",
            "Forensic post-mortem report (Cuerpo Medico Forense) if ordered",
            "Embalming certificate from licensed Argentine mortuary",
            "Freedom from contagious disease certificate (from provincial health authority)",
            "British Embassy Buenos Aires consular documentation",
            "Certified translations into English of all documents"
        ],
        "key_authorities": {
            "death_registration": "Registro Civil (Civil Registry) in the jurisdiction of death",
            "post_mortem": "Cuerpo Medico Forense (Forensic Medical Corps)",
            "release_authorisation": "Judiciary (Poder Judicial) — judge orders release for unnatural deaths",
            "export_permit": "Ministry of Health provincial or national authority"
        },
        "british_consulate": {
            "name": "British Embassy Buenos Aires",
            "address": "Dr. Luis Agote 2412, C1425EOF Buenos Aires",
            "phone": "+54 11 4808 2200",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["EZE (Ministro Pistarini International, Buenos Aires)", "AEP (Jorge Newbery, Buenos Aires domestic)"],
        "airlines": ["Aerolíneas Argentinas", "Iberia", "LATAM", "British Airways (via connections)"],
        "direct_uk_flights": False,
        "embalming_required": True,
        "cremation_available": True,
        "repatriation_complexity": "high",
        "ashes_transport_days_estimate": "5-10 days from Buenos Aires once documentation complete",
        "notable_considerations": [
            "No direct flights from Argentina to UK; routing typically via Madrid (Iberia) or São Paulo — add 1-2 days for cargo",
            "Patagonia deaths (hiking, trekking, mountaineering near Bariloche or El Calafate) require land or domestic flight transfer to Buenos Aires — add 1-3 days",
            "Argentine judicial system for releasing bodies in unnatural death cases can be slower in provinces than in Buenos Aires",
            "Adventure travel insurance with body repatriation cover is strongly recommended for Patagonia trekkers"
        ]
    },
    "costa-rica": {
        "name": "Costa Rica",
        "flag": "🇨🇷",
        "region": "Central America",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "12 days",
            "average_case": "16-22 days",
            "complex_case": "30+ days",
            "complexity_factors": [
                "OIJ (judicial investigation) for unnatural deaths can take 7-14 days",
                "Deaths in national parks (Corcovado, Arenal, Monteverde) require OIJ on-site investigation before transfer",
                "No direct UK flights; routing via Miami or Houston",
                "Spanish documentation requires certified translation"
            ]
        },
        "cost_range_gbp": {
            "min": 4000,
            "max": 8500,
            "notes": "Eco-tourism destination with strong travel insurance availability. Most standard UK policies cover Costa Rica."
        },
        "documentation_required": [
            "Costa Rican death certificate (Certificado de Defuncion) from RCEC (Registro Civil)",
            "OIJ investigation report (for unnatural/violent deaths)",
            "Forensic post-mortem report from INCIENSA or OIJ forensics",
            "Embalming certificate from licensed Costa Rican mortuary",
            "Ministry of Health export permit for human remains",
            "British Embassy San Jose consular documentation",
            "Certified translations into English of all documents"
        ],
        "key_authorities": {
            "death_registration": "Registro Civil (RCEC) in the canton of death",
            "post_mortem": "OIJ (Organismo de Investigacion Judicial) forensics",
            "release_authorisation": "OIJ and Ministerio Publico (for criminal/suspicious deaths)",
            "export_permit": "Ministry of Health (Ministerio de Salud)"
        },
        "british_consulate": {
            "name": "British Embassy San Jose",
            "address": "Edificio Centro Colon, Paseo Colon, San Jose",
            "phone": "+506 2258 2025",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["SJO (Juan Santamaria International, San Jose)", "LIR (Daniel Oduber, Liberia — for Guanacaste)"],
        "airlines": ["Copa Airlines", "American Airlines", "United Airlines", "LATAM"],
        "direct_uk_flights": False,
        "embalming_required": True,
        "cremation_available": True,
        "repatriation_complexity": "medium",
        "ashes_transport_days_estimate": "4-7 days from San Jose once documentation complete",
        "notable_considerations": [
            "Costa Rica is the most popular Central American destination for British tourists; eco-tourism deaths in national parks and jungle areas are documented",
            "OIJ (judicial police) investigation is mandatory for any unnatural death including accidents in national parks",
            "No direct UK flights; routing via Miami (American/United) or Panama City (Copa) is standard",
            "INCIENSA (national forensic laboratory) in San Jose handles post-mortems; regional transfers are required for deaths outside the Central Valley"
        ]
    },
    "senegal": {
        "name": "Senegal",
        "flag": "🇸🇳",
        "region": "Africa",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "14 days",
            "average_case": "21-28 days",
            "complex_case": "45+ days",
            "complexity_factors": [
                "Gendarmerie investigation for unnatural deaths; capacity outside Dakar is limited",
                "Infrastructure for international repatriation is concentrated in Dakar",
                "Documentation in French requires certified translation",
                "No direct UK flights; routing via Paris or Casablanca"
            ]
        },
        "cost_range_gbp": {
            "min": 4500,
            "max": 9000,
            "notes": "West African origin with complex logistics. Travel insurance strongly recommended including repatriation cover."
        },
        "documentation_required": [
            "Senegalese death certificate (Acte de Deces) from local Civil Registry (Etat Civil)",
            "Gendarmerie or Police report (for unnatural deaths)",
            "Post-mortem report from Institut Medico-Legal or authorised facility",
            "Embalming certificate from licensed mortuary in Dakar",
            "Certificat de Non-Contagion (freedom from contagious disease)",
            "Laissez-passer from Ministry of Interior or regional authority",
            "British Honorary Consul Dakar or Embassy Dakar documentation",
            "Certified translations into English of all French documents"
        ],
        "key_authorities": {
            "death_registration": "Etat Civil (Civil Registry) in the commune of death",
            "post_mortem": "Institut Medico-Legal (IML), Dakar",
            "release_authorisation": "Parquet (Prosecutor's Office) for unnatural deaths",
            "export_permit": "Ministry of Interior laissez-passer; Ministry of Health certificate"
        },
        "british_consulate": {
            "name": "British Embassy Dakar",
            "address": "20 Rue du Docteur Guillet, Dakar",
            "phone": "+221 33 823 7392",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["DSS (Blaise Diagne International, Dakar)"],
        "airlines": ["Air Senegal", "Air France", "Royal Air Maroc", "Brussels Airlines"],
        "direct_uk_flights": False,
        "embalming_required": True,
        "cremation_available": False,
        "repatriation_complexity": "high",
        "ashes_transport_days_estimate": "7-14 days from Dakar once documentation complete",
        "notable_considerations": [
            "Senegal is a Muslim-majority country; cremation is generally not available or acceptable",
            "No direct UK flights; routing via Paris (Air France) or Casablanca (Royal Air Maroc) is standard",
            "Dakar is the regional hub for West Africa — deaths elsewhere in Senegal (Saint-Louis, Casamance, Ziguinchor) require transfer to Dakar",
            "Former French colony: documentation is in French throughout. Certified English translation required"
        ]
    },
    "ethiopia": {
        "name": "Ethiopia",
        "flag": "🇪🇹",
        "region": "Africa",
        "eu_member": False,
        "strasbourg_signatory": False,
        "typical_timeline": {
            "fastest_case": "14 days",
            "average_case": "21-35 days",
            "complex_case": "50+ days",
            "complexity_factors": [
                "Federal Police investigation for unnatural deaths; capacity outside Addis Ababa is very limited",
                "Deaths in the regions (Lalibela, Simien Mountains, Omo Valley) require physical transfer to Addis Ababa",
                "Amharic documentation requires certified translation",
                "Ethiopian Airlines is a major hub airline but cargo documentation requirements are specific",
                "Ministry of Health and Federal Police both involved in export clearance"
            ]
        },
        "cost_range_gbp": {
            "min": 5000,
            "max": 10000,
            "notes": "High complexity African origin. Extended timelines for regional deaths drive higher costs. Specialist required."
        },
        "documentation_required": [
            "Ethiopian death certificate from Addis Ababa or regional Civil Registry",
            "Federal Police report (for unnatural deaths)",
            "Post-mortem report from St. Paul's Hospital Millennium Medical College or authorised facility",
            "Ministry of Health export permit for human remains",
            "Embalming certificate from licensed Addis Ababa mortuary",
            "Freedom from contagious disease certificate",
            "British Embassy Addis Ababa consular documentation",
            "Certified translations into English of all Amharic documents"
        ],
        "key_authorities": {
            "death_registration": "Addis Ababa City Administration or regional civil registry",
            "post_mortem": "St. Paul's Hospital Millennium Medical College (Addis Ababa) or Federal Police forensics",
            "release_authorisation": "Federal Police (for criminal or unnatural deaths)",
            "export_permit": "Ministry of Health export permit"
        },
        "british_consulate": {
            "name": "British Embassy Addis Ababa",
            "address": "Comoros Street, PO Box 858, Addis Ababa",
            "phone": "+251 11 617 0100",
            "emergency": "+44 1908 516666"
        },
        "main_airports": ["ADD (Bole International Airport, Addis Ababa)"],
        "airlines": ["Ethiopian Airlines", "British Airways (via connections)"],
        "direct_uk_flights": False,
        "embalming_required": True,
        "cremation_available": False,
        "repatriation_complexity": "very_high",
        "ashes_transport_days_estimate": "10-14 days from Addis Ababa once documentation complete",
        "notable_considerations": [
            "Ethiopian Airlines operates the main hub at Addis Ababa (ADD) with connections to Heathrow; cargo is routed via ADD regardless of origin in Ethiopia",
            "Deaths in popular tourist areas (Lalibela, Simien Mountains, Danakil Depression) require physical transfer to Addis Ababa — often by road or small aircraft, adding 2-5 days",
            "Cremation is generally not available or culturally accepted in Ethiopia",
            "Amharic is written in the Ge'ez script — certified translation requires a specialist Amharic-English translator, not a general East African language service",
            "The British Embassy in Addis Ababa also covers Djibouti; confirm jurisdiction when notifying"
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
