#!/usr/bin/env python3
"""Add Batch 31 countries to countries_repatriation.json.
Countries: iran, burundi, saint-vincent-and-the-grenadines, andorra, liechtenstein
"""
import json

JSON_PATH = "site/data/countries_repatriation.json"

BATCH_31 = {
    "iran": {
        "country_key": "iran",
        "country_name": "Iran",
        "country_adjective": "Iranian",
        "flag": "\U0001f1ee\U0001f1f7",
        "region": "Middle East",
        "languages": "Persian (Farsi)",
        "currency": "Iranian Rial (IRR)",
        "british_representation": "British Embassy Tehran",
        "embassy_type": "Embassy",
        "embassy_city": "Tehran",
        "local_authority_involved": "State Organisation for Civil Registration (SABTE AHVAL); Medical Legal Organisation (Pezeshki Qanuni)",
        "main_airports": "IKA (Imam Khomeini International, Tehran), THR (Mehrabad, Tehran)",
        "routing_notes": "Via Istanbul (Turkish Airlines), Dubai (Emirates/flydubai), Doha (Qatar Airways). Direct UK routes suspended since 2012.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 56,
        "timeline_notes": "Islamic burial 24hr pressure. Medical Legal Organisation clearance required for non-natural deaths. British-Iranian dual nationals face additional complications. UK-Iran diplomatic tensions can delay consular processing.",
        "complexity_rating": "very-high",
        "complexity_notes": "British-Iranian dual nationals not recognised as British by Iranian authorities — significant complication. Risk of arbitrary detention. UK-Iran tensions ongoing. Nuclear-related sanctions complicate financial transactions. British Embassy operational but access to detained nationals historically restricted.",
        "required_documents": [
            "Death certificate (State Organisation for Civil Registration)",
            "Medical Legal Organisation clearance (non-natural causes)",
            "Embalming certificate",
            "Freedom from infection certificate (Ministry of Health)",
            "Export permit (Ministry of Interior)",
            "Consular death registration (British Embassy, Tehran)"
        ],
        "religion_notes": "Approximately 98% Muslim (predominantly Shia). Islamic burial within 24 hours strongly observed. Zoroastrian, Christian, and Jewish minorities exist.",
        "cremation_available": False,
        "cremation_notes": "Cremation is not practised in Iran. Full body repatriation to the UK is required.",
        "no_go_zones": "Border regions with Iraq, Afghanistan, and Pakistan subject to FCDO advisories. Sistan-Baluchestan province. Kurdish border areas in the north-west.",
        "risk_highlights": [
            "FCDO advises against all but essential travel to Iran generally",
            "British-Iranian dual nationals not recognised as British nationals by Iranian authorities",
            "Risk of arbitrary detention of British nationals",
            "UK-Iran diplomatic tensions — consular access can be restricted"
        ]
    },
    "burundi": {
        "country_key": "burundi",
        "country_name": "Burundi",
        "country_adjective": "Burundian",
        "flag": "\U0001f1e7\U0001f1ee",
        "region": "East Africa",
        "languages": "Kirundi, French, English",
        "currency": "Burundian Franc (BIF)",
        "british_representation": "Non-resident — British High Commission, Kampala, Uganda",
        "embassy_type": "Non-resident (BHC Kampala)",
        "embassy_city": "Kampala",
        "local_authority_involved": "Civil registry (registrar des actes de l'état civil), Public Prosecutor's Office",
        "main_airports": "BJM (Melchior Ndadaye International, Bujumbura)",
        "routing_notes": "Via Nairobi (Kenya Airways/Ethiopian Airlines), via Brussels (Brussels Airlines), via Addis Ababa (Ethiopian Airlines).",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "Non-resident embassy adds consular processing time. French civil law documentation requires certified translation.",
        "complexity_rating": "high",
        "complexity_notes": "Non-resident British representation (BHC Kampala). French civil law documentation — Kirundi/French. Some areas subject to FCDO security advisories. Limited specialist firm capacity in Burundi.",
        "required_documents": [
            "Death certificate (civil registry)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (BHC Kampala)"
        ],
        "religion_notes": "Predominantly Christian (Catholic majority). Small Muslim minority.",
        "cremation_available": False,
        "cremation_notes": "Cremation is not widely available in Burundi. Full body repatriation to the UK is standard.",
        "no_go_zones": "Some border areas and rural provinces subject to FCDO advisories. Check current FCDO travel advice.",
        "risk_highlights": [
            "Non-resident British representation — BHC Kampala",
            "Some areas subject to FCDO security advisories",
            "French civil law documentation — translation required"
        ]
    },
    "saint-vincent-and-the-grenadines": {
        "country_key": "saint-vincent-and-the-grenadines",
        "country_name": "Saint Vincent and the Grenadines",
        "country_adjective": "Vincentian",
        "flag": "\U0001f1fb\U0001f1e8",
        "region": "Caribbean",
        "languages": "English",
        "currency": "East Caribbean Dollar (XCD)",
        "british_representation": "Non-resident — British High Commission, Bridgetown, Barbados",
        "embassy_type": "Non-resident (BHC Bridgetown)",
        "embassy_city": "Bridgetown",
        "local_authority_involved": "Registrar General's Office, Coroner's Court (unnatural deaths)",
        "main_airports": "SVD (Argyle International, Saint Vincent), BGI (Grantley Adams, Barbados — international connections)",
        "routing_notes": "Via Barbados (Caribbean connections), via Miami or New York. Well-connected for Caribbean region.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "English common law, Commonwealth documentation. Generally manageable. Outlying Grenadines islands may require internal transfer.",
        "complexity_rating": "moderate",
        "complexity_notes": "Non-resident BHC in Barbados. English common law. Good Caribbean routing. Grenadines islands (Mustique, Bequia, Canouan, Union Island) add logistical complexity if death occurs on outlying islands — internal boat or light aircraft transfer required before international repatriation.",
        "required_documents": [
            "Death certificate (Registrar General's Office)",
            "Coroner's certificate (unnatural deaths)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export permit",
            "Consular registration (BHC Bridgetown)"
        ],
        "religion_notes": "Predominantly Christian. Anglican, Methodist, Pentecostal, and Catholic denominations.",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Saint Vincent. Repatriation of ashes to the UK is a practical option.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — BHC Bridgetown",
            "Deaths on outlying Grenadines islands require internal transfer before international repatriation can begin"
        ]
    },
    "andorra": {
        "country_key": "andorra",
        "country_name": "Andorra",
        "country_adjective": "Andorran",
        "flag": "\U0001f1e6\U0001f1e9",
        "region": "Europe",
        "languages": "Catalan (official), Spanish, French",
        "currency": "Euro (EUR)",
        "british_representation": "Non-resident — British Embassy, Madrid, Spain",
        "embassy_type": "Non-resident (Embassy Madrid)",
        "embassy_city": "Madrid",
        "local_authority_involved": "Andorran civil registry (via parish Comú), Cos de Policia d'Andorra",
        "main_airports": "BCN (Barcelona El Prat, Spain — approx. 3 hrs by road), TLS (Toulouse-Blagnac, France — approx. 3 hrs by road)",
        "routing_notes": "Road transfer to Barcelona or Toulouse, then direct flights to UK. No airport in Andorra.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 5,
        "typical_timeline_days_max": 14,
        "timeline_notes": "Very low complexity. Spanish/French legal influences. Road transfer to major airports straightforward.",
        "complexity_rating": "low",
        "complexity_notes": "Co-principality with French and Spanish legal influences. Civil registration in Catalan. Non-resident embassy in Madrid. Road access to Barcelona (Spain) or Toulouse (France) is standard and straightforward. No airport in Andorra.",
        "required_documents": [
            "Death certificate (Andorran civil registry, in Catalan)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export authorisation",
            "Consular registration (British Embassy, Madrid)"
        ],
        "religion_notes": "Predominantly Catholic.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities in Andorra. Body repatriation to the UK, or transfer to Spain or France for cremation followed by ashes repatriation, are both viable options.",
        "no_go_zones": "",
        "risk_highlights": [
            "No airport in Andorra — road transfer to Barcelona or Toulouse required",
            "Non-resident British representation — Embassy Madrid",
            "Documentation in Catalan — certified translation required"
        ]
    },
    "liechtenstein": {
        "country_key": "liechtenstein",
        "country_name": "Liechtenstein",
        "country_adjective": "Liechtenstein",
        "flag": "\U0001f1f1\U0001f1ee",
        "region": "Europe",
        "languages": "German",
        "currency": "Swiss Franc (CHF)",
        "british_representation": "Non-resident — British Embassy, Bern, Switzerland",
        "embassy_type": "Non-resident (Embassy Bern)",
        "embassy_city": "Bern",
        "local_authority_involved": "Amt für Bevölkerung und Zivilregister (Population and Civil Registry Office), Landgericht (Regional Court)",
        "main_airports": "ZRH (Zürich Kloten, Switzerland — approx. 1.5 hrs by road), BSL (Basel-Mulhouse — approx. 2 hrs by road)",
        "routing_notes": "Road transfer to Zürich or Basel, then direct flights to UK. Very straightforward.",
        "typical_cost_gbp_min": 0,
        "typical_cost_gbp_max": 0,
        "typical_cost_notes": "Contact specialist firm for current pricing",
        "typical_timeline_days_min": 3,
        "typical_timeline_days_max": 10,
        "timeline_notes": "Very low complexity. German civil law. Excellent access to Zürich airport.",
        "complexity_rating": "low",
        "complexity_notes": "One of the world's smallest and most stable states. German civil law. Close proximity to Zürich. Non-resident embassy in Bern but process is straightforward.",
        "required_documents": [
            "Death certificate (Amt für Bevölkerung und Zivilregister)",
            "Embalming certificate",
            "Freedom from infection certificate",
            "Export authorisation",
            "Consular registration (British Embassy, Bern)"
        ],
        "religion_notes": "Predominantly Catholic and Protestant (Reformed Church).",
        "cremation_available": True,
        "cremation_notes": "Cremation is available in Liechtenstein. Repatriation of ashes to the UK is a practical option.",
        "no_go_zones": "",
        "risk_highlights": [
            "Non-resident British representation — Embassy Bern",
            "No airport in Liechtenstein — road transfer to Zürich or Basel required",
            "Documentation in German — certified translation required"
        ]
    }
}

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

added = []
for key, country in BATCH_31.items():
    if key in data["countries"]:
        print(f"SKIP (already exists): {key}")
    else:
        data["countries"][key] = country
        added.append(key)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"ADDED: {', '.join(added)}")
print(f"Total countries: {len(data['countries'])}")
