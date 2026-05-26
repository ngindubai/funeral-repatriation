"""Add Batch 23 countries to countries_repatriation.json"""
import json, os

JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "site", "data", "countries_repatriation.json")

NEW_COUNTRIES = {
    "sudan": {
        "country_name": "Sudan",
        "country_adjective": "Sudanese",
        "flag": "\U0001f1f8\U0001f1e9",
        "region": "East Africa / North Africa",
        "languages": ["Arabic", "English"],
        "currency": "Sudanese Pound (SDG)",
        "british_representation": "British Embassy, Khartoum (suspended operations since April 2023; FCDO advises against all travel to Sudan)",
        "embassy_type": "Embassy",
        "embassy_city": "Khartoum",
        "local_authority_involved": "Civil Registry for death registration; Ministry of Health for documentation; active conflict involving Sudan Armed Forces (SAF) and Rapid Support Forces (RSF) makes standard procedures unreliable across most of the country",
        "main_airports": [
            "Khartoum International Airport (KRT, currently inoperative due to conflict)",
            "Port Sudan New International Airport (PZU, limited service)"
        ],
        "routing_notes": "Khartoum Airport has been inoperative since April 2023 due to conflict. Limited flights operate from Port Sudan to Cairo, Doha, and Jeddah. Repatriation routing requires specialist assessment at time of case — the situation is highly dynamic.",
        "typical_cost_gbp_min": 8000,
        "typical_cost_gbp_max": 25000,
        "typical_cost_notes": "Very wide range. Conflict conditions, airport closures, security escort requirements, and specialist firm markups make cost prediction unreliable. Cases may require body recovery from conflict-affected areas before any standard repatriation process can begin.",
        "typical_timeline_days_min": 60,
        "typical_timeline_days_max": 365,
        "timeline_notes": "Timelines are essentially unpredictable in current conflict conditions. Cases that can be extracted to Port Sudan or a border crossing may move in 2 to 4 months. Cases in Khartoum, Darfur, Kordofan, or other active conflict zones may take significantly longer or may not be possible to complete.",
        "complexity_rating": "extreme",
        "complexity_notes": "Sudan is in active civil war since April 2023. The British Embassy in Khartoum suspended all operations. FCDO advises against all travel. Standard repatriation procedures are not functioning across most of the country. The Sudan Armed Forces (SAF) and the Rapid Support Forces (RSF) control different areas. Khartoum International Airport is non-operational. Only a small number of highly specialist firms with active Sudan and conflict-zone networks can manage cases. Families should not expect a standard repatriation timeline or process.",
        "required_documents": [
            "Sudanese death certificate from Civil Registry (where accessible)",
            "Medical certificate of cause of death (where a physician is accessible)",
            "Any available police or military authority clearance depending on area of death",
            "UK consular registration via FCDO emergency channels (British Embassy Khartoum suspended — consular support via FCDO London)",
            "Export documentation as conditions allow",
            "Certified Arabic-to-English translations of all documents"
        ],
        "religion_notes": "Sudan is approximately 97% Muslim. Islamic burial practice — swift burial, no cremation — is the norm. International repatriation from Sudan would typically involve a non-Sudanese British national or a British national of Sudanese descent returning a relative to the UK.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities exist in Sudan. Islamic burial practice is universal. Ashes repatriation is not applicable.",
        "no_go_zones": [
            "All of Sudan — FCDO advises against all travel",
            "Khartoum and surrounding areas — active SAF/RSF combat",
            "Darfur — ongoing atrocities, FCDO advises against all travel",
            "North Kordofan, South Kordofan, Blue Nile state — active conflict",
            "Sudanese-Eritrean border region"
        ],
        "risk_highlights": [
            "FCDO advises against all travel to Sudan — civil war since April 2023",
            "British Embassy Khartoum suspended operations April 2023",
            "Khartoum Airport inoperative — only Port Sudan has limited scheduled service",
            "SAF and RSF control different territories; authority structures vary by location",
            "Darfur: humanitarian crisis and active atrocities — extreme risk",
            "Even with specialist firms, repatriation from active conflict zones may not be possible"
        ]
    },
    "moldova": {
        "country_name": "Moldova",
        "country_adjective": "Moldovan",
        "flag": "\U0001f1f2\U0001f1e9",
        "region": "Eastern Europe",
        "languages": ["Romanian (Moldovan)", "Russian"],
        "currency": "Moldovan Leu (MDL)",
        "british_representation": "British Embassy, Chisinau",
        "embassy_type": "Embassy",
        "embassy_city": "Chisinau",
        "local_authority_involved": "Civil Status Agency (Agenția Servicii Publice) for death registration; State Medical Examiner Service for non-natural deaths; State Inspectorate for Emergency Situations for major incidents",
        "main_airports": [
            "Chisinau International Airport (KIV)"
        ],
        "routing_notes": "Chisinau Airport (KIV) has direct flights to London Luton (Wizz Air, FlyOne). Additional connections via Bucharest (TAROM), Vienna (Austrian), Istanbul (Turkish Airlines). Cargo follows these passenger routes. The Transnistria separatist region adds a specific regional complication.",
        "typical_cost_gbp_min": 2000,
        "typical_cost_gbp_max": 4500,
        "typical_cost_notes": "Moldova is an affordable repatriation destination by Eastern European standards. Costs reflect the small scale of the British national population and functioning civil infrastructure. Cases in Transnistria add significant complexity and cost.",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "7 to 21 days is typical for cases in Moldova proper. Cases in the Transnistria region require additional coordination and can add 2 to 4 weeks. Moldova's civil registration system functions well.",
        "complexity_rating": "medium",
        "complexity_notes": "Moldova is a manageable Eastern European repatriation destination with a resident British Embassy in Chisinau. The Civil Status Agency handles death registration efficiently. The main complication unique to Moldova is the Transnistria separatist region — a de facto independent territory not under Moldovan government control. Deaths in Transnistria involve Transnistrian authorities, not Moldovan ones, and the British Embassy's ability to assist is limited there. Documents are in Romanian (Moldovan); Russian is widely spoken. Direct London flights via Wizz Air.",
        "required_documents": [
            "Moldovan death certificate issued by Civil Status Agency (Agenția Servicii Publice)",
            "Medical certificate of cause of death",
            "State Medical Examiner report for non-natural deaths",
            "Ministry of Health export permit",
            "Embalming and preparation certificate",
            "British Embassy Chisinau consular registration",
            "Certified Romanian/Russian-to-English translations",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Moldova is majority Eastern Orthodox Christian (Moldovan Orthodox Church). Christian burial is the predominant practice. Cremation is available in Chisinau. A small Muslim Gagauz community exists in the south.",
        "cremation_available": True,
        "cremation_notes": "Cremation facilities are available in Chisinau. Ashes can be repatriated to the UK as accompanied or unaccompanied baggage. Cremation documentation follows standard European procedures.",
        "no_go_zones": [
            "Transnistria separatist region — FCDO advises against travel; British Embassy cannot provide normal consular assistance"
        ],
        "risk_highlights": [
            "Transnistria: de facto independent separatist territory — standard Moldovan procedures do not apply",
            "British Embassy Chisinau has limited capacity to assist in Transnistria",
            "Romania border: some British nationals transit via Iasi (Romania) — consular support for these cases goes through British Embassy Bucharest",
            "Direct London flights (Wizz Air to Luton) simplify cargo logistics"
        ]
    },
    "belarus": {
        "country_name": "Belarus",
        "country_adjective": "Belarusian",
        "flag": "\U0001f1e7\U0001f1fe",
        "region": "Eastern Europe",
        "languages": ["Belarusian", "Russian"],
        "currency": "Belarusian Ruble (BYN)",
        "british_representation": "British Embassy, Minsk (operating with reduced staff; FCDO advises against all but essential travel to Belarus)",
        "embassy_type": "Embassy",
        "embassy_city": "Minsk",
        "local_authority_involved": "Civil Registry Department (ZAGS equivalent) for death registration; Investigative Committee of Belarus for non-natural deaths; Ministry of Foreign Affairs for international document attestation",
        "main_airports": [
            "Minsk National Airport (MSQ)"
        ],
        "routing_notes": "Direct UK-Belarus flights are suspended. Remains route via Warsaw (LOT Polish Airlines), Vilnius, or Istanbul (Turkish Airlines). The diplomatic environment since 2020 adds complexity to official documentation.",
        "typical_cost_gbp_min": 5000,
        "typical_cost_gbp_max": 14000,
        "typical_cost_notes": "Significant costs driven by suspended direct flights, Ministry of Foreign Affairs attestation requirements, and the political context increasing specialist firm difficulty. Cases are rare given the FCDO travel advisory and low UK tourist volume.",
        "typical_timeline_days_min": 28,
        "typical_timeline_days_max": 84,
        "timeline_notes": "4 to 12 weeks is the realistic range. Belarus repatriation involves Investigative Committee clearance for non-natural deaths, Ministry of Foreign Affairs attestation for documents, and indirect routing. The political context since 2020 and further deterioration in 2022 (support for Russia's Ukraine invasion) has reduced British Embassy capacity.",
        "complexity_rating": "very-high",
        "complexity_notes": "Belarus presents serious repatriation challenges. FCDO advises against all but essential travel. The British Embassy in Minsk operates with reduced staff following diplomatic tensions since 2020. Direct UK-Belarus flights are suspended following the forced diversion of Ryanair flight FR4978 in 2021. Belarus's Ministry of Foreign Affairs attestation process applies to all international documents. The Investigative Committee is involved in all non-natural deaths. Only specialist firms with Eastern European authority networks should handle Belarus cases.",
        "required_documents": [
            "Belarusian death certificate from Civil Registry",
            "Medical certificate of cause of death",
            "Investigative Committee clearance for non-natural deaths",
            "Ministry of Foreign Affairs attestation on all export documents",
            "Export permit from Belarusian health authorities",
            "Embalming and preparation certificate",
            "British Embassy Minsk consular registration",
            "Certified Belarusian/Russian-to-English translations",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Belarus is majority Eastern Orthodox Christian (Belarusian Orthodox Church, linked to Russian Orthodox Church). Christian burial is predominant. Cremation is available in Minsk. Catholic minority exists in western Belarus near the Polish border.",
        "cremation_available": True,
        "cremation_notes": "Cremation facilities are available in Minsk and some larger cities. Ashes export requires cremation certificate and Ministry of Foreign Affairs attestation.",
        "no_go_zones": [
            "Belarus-Ukraine border region — FCDO advises against all travel within 50km of Ukrainian border",
            "All of Belarus — FCDO advises against all but essential travel"
        ],
        "risk_highlights": [
            "FCDO advises against all but essential travel to Belarus",
            "British Embassy Minsk reduced capacity since 2020",
            "Direct UK-Belarus flights suspended since 2021 — indirect routing required",
            "Ministry of Foreign Affairs attestation adds weeks to document process",
            "Political context: Belarusian authorities have detained foreign nationals — specialist firms essential",
            "Belarus-Ukraine border: active military logistics zone, FCDO all-travel advisory within 50km of border"
        ]
    },
    "tajikistan": {
        "country_name": "Tajikistan",
        "country_adjective": "Tajik",
        "flag": "\U0001f1f9\U0001f1ef",
        "region": "Central Asia",
        "languages": ["Tajik", "Russian"],
        "currency": "Tajikistani Somoni (TJS)",
        "british_representation": "British Embassy, Dushanbe",
        "embassy_type": "Embassy",
        "embassy_city": "Dushanbe",
        "local_authority_involved": "Civil Status Registration Agency (ЗАГС) for death registration; Ministry of Internal Affairs for non-natural deaths; Ministry of Health for export documentation",
        "main_airports": [
            "Dushanbe International Airport (DYU)",
            "Khujand Airport (LBD)"
        ],
        "routing_notes": "Dushanbe Airport has connections to Moscow (Aeroflot, Somon Air), Istanbul (Turkish Airlines), and Dubai (flydubai). For UK repatriation, routing is typically via Istanbul or Dubai rather than Moscow (given suspended UK-Russia flights). Khujand connects mainly to Moscow. Total cargo journey 3 to 5 days once documentation cleared.",
        "typical_cost_gbp_min": 4000,
        "typical_cost_gbp_max": 10000,
        "typical_cost_notes": "Costs reflect Central Asian routing complexity, limited international cargo infrastructure, and specialist firm requirements. The mountainous terrain of Tajikistan means cases outside Dushanbe may require internal transfer first.",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 42,
        "timeline_notes": "2 to 6 weeks is typical. Tajikistan has functioning civil registration but bureaucratic processes move slowly. The mountainous terrain and limited infrastructure outside Dushanbe can add to the timeline. Cases involving deaths in the Pamir region or near the Afghan border face the longest timelines.",
        "complexity_rating": "high",
        "complexity_notes": "Tajikistan is Central Asia's poorest country and its infrastructure reflects this. There is a resident British Embassy in Dushanbe, but capacity is limited. Documents are in Tajik (Cyrillic script) and Russian. The Pamir mountains (GBAO region) are a UK adventure travel destination — deaths occur in this region among climbers and trekkers — and body recovery from high-altitude or remote locations can be a major operational challenge. The Tajik-Afghan border region has periodic security incidents. FCDO advises against all travel to GBAO (near Afghan border) and the Tajik-Kyrgyz border region.",
        "required_documents": [
            "Tajik death certificate from Civil Status Registration Agency",
            "Medical certificate of cause of death",
            "Ministry of Internal Affairs clearance for non-natural deaths",
            "Ministry of Health export permit",
            "Embalming and preparation certificate",
            "British Embassy Dushanbe consular registration",
            "Certified Tajik/Russian-to-English translations",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Tajikistan is approximately 95% Muslim (predominantly Sunni; Ismaili Muslims in the Pamir/GBAO region). Islamic burial practice is the norm — swift burial, no cremation. International repatriation from Tajikistan typically involves an adventure traveller, aid worker, or a member of the UK Tajik diaspora.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities exist in Tajikistan. Islamic burial practice is universal. Body repatriation is the only option.",
        "no_go_zones": [
            "GBAO (Gorno-Badakhshan Autonomous Oblast) bordering Afghanistan — FCDO advises against all travel",
            "Tajik-Afghan border region",
            "Tajik-Kyrgyz border region (disputed areas) — FCDO advises against all travel"
        ],
        "risk_highlights": [
            "GBAO and Pamir region: FCDO all-travel advisory — adventure tourism deaths occur here",
            "High-altitude body recovery in Pamirs may require helicopter or specialist mountain rescue",
            "Documents in Tajik Cyrillic and Russian — certified translation required",
            "Limited Embassy capacity in Dushanbe",
            "Cases near Afghan border involve additional security and authority clearances"
        ]
    },
    "guyana": {
        "country_name": "Guyana",
        "country_adjective": "Guyanese",
        "flag": "\U0001f1ec\U0001f1fe",
        "region": "South America / Caribbean",
        "languages": ["English"],
        "currency": "Guyanese Dollar (GYD)",
        "british_representation": "British High Commission, Georgetown",
        "embassy_type": "High Commission",
        "embassy_city": "Georgetown",
        "local_authority_involved": "General Register Office for death registration; Magistrate's Court for coroner inquests; police for non-natural deaths; Ministry of Public Health for export documentation",
        "main_airports": [
            "Cheddi Jagan International Airport (GEO), Timehri",
            "Eugene F. Correia International Airport (OGL), Ogle (domestic and regional)"
        ],
        "routing_notes": "Guyana has no direct UK flights. Repatriation routes via Miami (American Airlines, Caribbean Airlines), New York JFK (Caribbean Airlines), or Barbados/Trinidad as Caribbean hub connections. Caribbean Airlines flies Georgetown-London Gatwick with connection. Total cargo journey 3 to 6 days from Georgetown to the UK.",
        "typical_cost_gbp_min": 3000,
        "typical_cost_gbp_max": 7000,
        "typical_cost_notes": "Costs reflect Caribbean routing via Miami or Trinidad. Guyana is an English-speaking Commonwealth country, which simplifies documentation. The interior jungle regions add significant cost for body recovery and transfer to Georgetown.",
        "typical_timeline_days_min": 10,
        "typical_timeline_days_max": 28,
        "timeline_notes": "10 to 28 days is typical. Guyana's General Register Office processes death certificates in reasonable time. For deaths in the interior — jungle mining camps, the Rupununi savanna — internal transfer to Georgetown is the primary time variable. Post-mortem examination in Georgetown is required for all non-natural deaths.",
        "complexity_rating": "medium",
        "complexity_notes": "Guyana is a Commonwealth country with English as the official language, which significantly simplifies documentation compared to most South American repatriations. The British High Commission in Georgetown is resident. The main complexity is geography: much of Guyana is dense Amazonian jungle interior accessible only by small aircraft or river boat. Deaths at interior mining camps (gold and diamond mining is extensive), eco-tourism lodges, or wilderness areas require specialist recovery before standard repatriation can proceed. The growing oil and gas industry (offshore Atlantic) brings more international workers and a higher risk profile.",
        "required_documents": [
            "Guyanese death certificate from General Register Office",
            "Medical certificate of cause of death",
            "Post-mortem report for non-natural deaths (Georgetown Public Hospital pathologist)",
            "Magistrate's inquest certificate where applicable",
            "Police report for violent or suspicious deaths",
            "Ministry of Public Health export permit",
            "Embalming and preparation certificate",
            "British High Commission Georgetown registration",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Guyana has significant Christian (Protestant and Catholic), Hindu, and Muslim populations, reflecting its Indo-Guyanese, Afro-Guyanese, and Amerindian communities. Christian and Hindu communities generally accept repatriation; Muslim families may prefer swift local burial. Cremation is accepted within the Hindu community.",
        "cremation_available": True,
        "cremation_notes": "Cremation facilities are available in Georgetown. The Hindu community uses cremation. Ashes can be repatriated to the UK. Export of ashes requires cremation certificate and Ministry of Public Health clearance.",
        "no_go_zones": [],
        "risk_highlights": [
            "Interior jungle regions: body recovery requires small aircraft or river boat — adds days to process",
            "Gold and diamond mining interior: occupational deaths in remote camp locations",
            "Georgetown: petty crime and road traffic incidents are most common causes of UK tourist deaths",
            "Offshore oil and gas industry: maritime deaths require specialist recovery procedures",
            "Guyana-Venezuela border region: FCDO advises against travel to border zone"
        ]
    }
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

existing = set(data["countries"].keys())
for key in NEW_COUNTRIES:
    if key in existing:
        print(f"SKIP — {key} already exists")
    else:
        data["countries"][key] = NEW_COUNTRIES[key]
        print(f"ADDED  — {key}")

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal countries in JSON: {len(data['countries'])}")
