"""Add Batch 22 countries to countries_repatriation.json"""
import json, os

JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "site", "data", "countries_repatriation.json")

NEW_COUNTRIES = {
    "russia": {
        "country_name": "Russia",
        "country_adjective": "Russian",
        "flag": "\U0001f1f7\U0001f1fa",
        "region": "Eastern Europe / Northern Asia",
        "languages": ["Russian"],
        "currency": "Russian Ruble (RUB)",
        "british_representation": "British Embassy, Moscow (operating with significantly reduced staff since 2022; FCDO advises against all travel to Russia)",
        "embassy_type": "Embassy",
        "embassy_city": "Moscow",
        "local_authority_involved": "ZAGS Civil Registry Office for death registration; Investigative Committee of Russia for non-natural deaths; Ministry of Foreign Affairs attestation required for all export documents",
        "main_airports": [
            "Moscow Sheremetyevo International Airport (SVO)",
            "Moscow Domodedovo Airport (DME)",
            "St Petersburg Pulkovo Airport (LED)"
        ],
        "routing_notes": "Direct UK-Russia passenger and cargo flights suspended since 2022. Remains route via Istanbul (Turkish Airlines), Dubai (Emirates), or other non-Western hub airports. Total journey time highly variable depending on connection availability and diplomatic clearances.",
        "typical_cost_gbp_min": 6000,
        "typical_cost_gbp_max": 18000,
        "typical_cost_notes": "Wide range driven by routing complexity since 2022 airspace closures, Ministry of Foreign Affairs attestation fees, and specialist firm requirements. Cases involving FSB or Investigative Committee can incur significant additional legal costs.",
        "typical_timeline_days_min": 42,
        "typical_timeline_days_max": 140,
        "timeline_notes": "6 to 20 weeks is the realistic range. Russia's repatriation bureaucracy involves multiple government ministries. Cases with criminal investigation involvement, or where the deceased held dual nationality, are significantly longer. Consular access can be restricted.",
        "complexity_rating": "very-high",
        "complexity_notes": "Russia is one of the most complex repatriation destinations for UK families. Multiple factors: FCDO advises against all travel; British Embassy Moscow operates with reduced staff and limited consular capacity; all documents must go through Ministry of Foreign Affairs apostille; direct UK-Russia flights suspended since 2022; Investigative Committee involvement in any non-natural death; potential FSB interest in deaths of dual nationals or those connected to sensitive sectors. Only specialist international funeral firms with Russia experience should be engaged.",
        "required_documents": [
            "Russian death certificate (Svidetelstvo o smerti) from ZAGS Civil Registry",
            "Certificate of cause of death from attending physician or pathologist",
            "Ministry of Foreign Affairs apostille on all documents",
            "Investigative Committee clearance for non-natural deaths",
            "Embalming certificate from licensed Russian mortuary",
            "Export permit from Russian health authorities",
            "British Embassy Moscow consular notification",
            "Certified Russian-to-English translations of all documents",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Russian Orthodox Christianity is the majority faith, with burial the traditional practice. Cremation is available in major cities. Significant Muslim population in regions such as Chechnya, Dagestan, and Tatarstan, where Islamic burial practice (swift burial, no cremation) is the norm.",
        "cremation_available": True,
        "cremation_notes": "Cremation facilities are available in Moscow, St Petersburg, and other major cities. Rural areas typically have no cremation facilities. Ashes export requires a cremation certificate and Ministry of Health clearance. The ashes of a British national can be brought home to the UK as accompanied or unaccompanied baggage subject to airline and carrier rules.",
        "no_go_zones": [
            "Chechnya, Dagestan, Ingushetia and the wider North Caucasus (FCDO: advise against all travel)",
            "All areas within 10km of the Ukraine border",
            "Occupied Ukrainian territories: Crimea, Donetsk, Luhansk, Zaporizhzhia, Kherson (FCDO: advise against all travel)"
        ],
        "risk_highlights": [
            "FCDO advises against all travel to Russia — consular support severely limited",
            "Direct UK-Russia flights suspended since 2022 — specialist routing required",
            "Ministry of Foreign Affairs apostille adds weeks to document processing",
            "Investigative Committee involvement in any non-natural death",
            "Dual nationals may face additional complications and delays",
            "North Caucasus region: active conflict and FCDO 'do not travel' advisory"
        ]
    },
    "bosnia-and-herzegovina": {
        "country_name": "Bosnia and Herzegovina",
        "country_adjective": "Bosnian",
        "flag": "\U0001f1e7\U0001f1e6",
        "region": "Balkans / Southeastern Europe",
        "languages": ["Bosnian", "Croatian", "Serbian"],
        "currency": "Bosnia-Herzegovina Convertible Mark (BAM)",
        "british_representation": "British Embassy, Sarajevo",
        "embassy_type": "Embassy",
        "embassy_city": "Sarajevo",
        "local_authority_involved": "Municipal register office for death registration; Federal Institute of Forensic Medicine (Sarajevo, Federation entity) or Institute of Forensic Medicine of Republika Srpska (Banja Luka) for non-natural deaths",
        "main_airports": [
            "Sarajevo International Airport (SJJ)",
            "Mostar Airport (OMO, limited scheduled service)"
        ],
        "routing_notes": "Most repatriations route via Sarajevo Airport (SJJ) with Austrian Airlines via Vienna, Turkish Airlines via Istanbul, or Wizz Air connections. Mostar has limited scheduled service. Banja Luka Airport has regional connections to Belgrade.",
        "typical_cost_gbp_min": 2500,
        "typical_cost_gbp_max": 5000,
        "typical_cost_notes": "Standard range for adult repatriation from Sarajevo. Cases in Republika Srpska may add cross-entity administrative steps. Mostar and tourist-area cases are comparable in cost. Documentation is generally efficient for the region.",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "7 to 21 days is typical. Bosnia and Herzegovina has a functioning civil documentation system. The main variable is the entity: cases in the Federation of Bosnia and Herzegovina and cases in Republika Srpska involve different authorities and slightly different administrative procedures.",
        "complexity_rating": "medium",
        "complexity_notes": "Bosnia and Herzegovina has a resident British Embassy in Sarajevo and established civil registration procedures. The country is divided into two entities — the Federation of Bosnia and Herzegovina and Republika Srpska — with separate administrative systems. Deaths in the Federation are handled by the Federal Institute of Forensic Medicine in Sarajevo; deaths in Republika Srpska by the Institute in Banja Luka. Cross-entity cases can add time. Documents are in Bosnian/Croatian/Serbian using Latin script (Republika Srpska may also use Cyrillic). Mostar and the Neretva valley are popular UK tourist destinations.",
        "required_documents": [
            "Death certificate (Smrtovnica) from municipal register office",
            "Forensic certificate for non-natural deaths",
            "Police report and clearance for non-natural deaths",
            "Embalming and preservation certificate",
            "Export permit from cantonal or entity health ministry",
            "British Embassy Sarajevo consular registration",
            "Certified translations of all documents into English",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Bosnia and Herzegovina has three main communities: Bosniaks (Sunni Muslim majority — Islamic burial practice, no cremation, swift burial), Orthodox Serbs, and Catholic Croats. Death practices vary significantly by community. Repatriation firms must be aware of religious requirements when coordinating with local mortuaries.",
        "cremation_available": True,
        "cremation_notes": "Cremation facilities exist in Sarajevo (the Bare Crematorium) and a limited number of cities. Not available everywhere. For Muslim Bosniak families, cremation is not consistent with Islamic burial practice. Ashes export requires cremation certificate and ministry health clearance.",
        "no_go_zones": [],
        "risk_highlights": [
            "Landmine risk in rural and mountainous areas from the 1992-1995 war — marked paths only",
            "Divided administrative system (Federation and Republika Srpska) may add cross-entity steps",
            "Mostar: popular UK tourist destination — cases in July-August see seasonal surge",
            "Mountain hiking incidents in the Dinaric Alps are the most common tourist death context"
        ]
    },
    "kosovo": {
        "country_name": "Kosovo",
        "country_adjective": "Kosovar",
        "flag": "\U0001f1fd\U0001f1f0",
        "region": "Balkans / Southeastern Europe",
        "languages": ["Albanian", "Serbian"],
        "currency": "Euro (EUR)",
        "british_representation": "British Embassy, Pristina",
        "embassy_type": "Embassy",
        "embassy_city": "Pristina",
        "local_authority_involved": "Civil Status Agency for death registration; Institute of Forensic Medicine, Pristina for non-natural deaths; Kosovo Police for sudden or violent deaths",
        "main_airports": [
            "Pristina Adem Jashari International Airport (PRN)"
        ],
        "routing_notes": "Pristina Airport (PRN) has direct flights to London Luton (Wizz Air, British Airways codeshare) and London Gatwick. Connections also via Vienna (Austrian Airlines), Istanbul (Turkish Airlines), Zurich, and Amsterdam. Cargo routing typically follows passenger routes.",
        "typical_cost_gbp_min": 2000,
        "typical_cost_gbp_max": 4500,
        "typical_cost_notes": "Kosovo is a relatively affordable Balkan repatriation destination. Euro currency simplifies payments. British Embassy Pristina is experienced with repatriation cases given the large British-Kosovar diaspora community in the UK.",
        "typical_timeline_days_min": 7,
        "typical_timeline_days_max": 21,
        "timeline_notes": "7 to 21 days in most cases. Kosovo has a functioning civil registry. The Institute of Forensic Medicine in Pristina handles non-natural deaths. The large British-Kosovar diaspora means Pristina Embassy staff are experienced with repatriation coordination.",
        "complexity_rating": "medium",
        "complexity_notes": "Kosovo has a resident British Embassy in Pristina and is one of the more manageable Balkan repatriation destinations. UK recognised Kosovo independence in 2008. The British-Kosovar community in the UK is substantial — the Embassy in Pristina handles a meaningful number of repatriation cases relative to population size. Documents are in Albanian and Serbian. Some international entities and airlines do not recognise Kosovo's independence, which can occasionally complicate cargo documentation — a specialist firm will navigate this. NATO KFOR military presence provides additional institutional stability.",
        "required_documents": [
            "Death certificate issued by Civil Status Agency, Kosovo",
            "Forensic report from Institute of Forensic Medicine, Pristina for non-natural deaths",
            "Kosovo Police report for sudden or violent deaths",
            "Embalming and preservation certificate",
            "Export permit from Kosovo health authorities",
            "British Embassy Pristina consular registration",
            "Certified translations into English where required",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Kosovo is predominantly Muslim (approximately 95% of population). Islamic burial practice — swift burial in a shroud, no cremation — is the dominant custom. A small Serbian Orthodox Christian minority exists. UK repatriation from Kosovo most often involves a British-Kosovar family bringing a relative home.",
        "cremation_available": False,
        "cremation_notes": "No cremation facilities exist in Kosovo. In practice, almost all repatriation cases from Kosovo involve body repatriation. Cremation would require transfer to Serbia or another country with facilities, which adds significant complexity and time.",
        "no_go_zones": [],
        "risk_highlights": [
            "Kosovo-Serbia border tension: avoid areas near the northern border boundary",
            "Pristina is generally safe; rural northern Kosovo near Serbia border has periodic incidents",
            "Large British-Kosovar diaspora means British Embassy Pristina has high repatriation case volume",
            "Some airlines and cargo carriers may not accept Kosovo-issued documentation — specialist firms required"
        ]
    },
    "luxembourg": {
        "country_name": "Luxembourg",
        "country_adjective": "Luxembourgish",
        "flag": "\U0001f1f1\U0001f1fa",
        "region": "Western Europe",
        "languages": ["Luxembourgish", "French", "German"],
        "currency": "Euro (EUR)",
        "british_representation": "British Embassy, Luxembourg City",
        "embassy_type": "Embassy",
        "embassy_city": "Luxembourg City",
        "local_authority_involved": "Civil Status Registry (Etat Civil) for death registration; Parquet Général (public prosecutor) for non-natural deaths; State Laboratory for forensic cases",
        "main_airports": [
            "Luxembourg Findel Airport (LUX)"
        ],
        "routing_notes": "Luxembourg Findel Airport (LUX) has direct connections to London Heathrow (British Airways), London City, and multiple UK regional airports. Cargo connections via Amsterdam, Frankfurt, and Brussels. One of the most straightforward routing situations in Europe.",
        "typical_cost_gbp_min": 1500,
        "typical_cost_gbp_max": 3500,
        "typical_cost_notes": "Luxembourg is one of the most affordable and efficient European repatriation destinations. Procedures are well-established, documentation is in order, and routing is straightforward. High local service costs reflect the country's cost of living but the overall case is compact.",
        "typical_timeline_days_min": 4,
        "typical_timeline_days_max": 10,
        "timeline_notes": "4 to 10 days is typical. Luxembourg has highly efficient administrative procedures, a resident British Embassy, and direct London flights. It is among the fastest European repatriation destinations. Non-natural death investigations by the Parquet Général can extend timelines but Luxembourg's legal system operates efficiently.",
        "complexity_rating": "low",
        "complexity_notes": "Luxembourg is one of the simplest EU repatriation destinations. The British Embassy Luxembourg City is resident, administrative procedures are efficient, trilingual documentation (Luxembourgish, French, German) is well-understood by specialist firms, and Findel Airport has direct London connections. The main UK population in Luxembourg consists of EU civil servants, financial sector workers, and EU institution employees — a specific and relatively affluent expatriate community. Deaths are rare but cases do occur.",
        "required_documents": [
            "Luxembourg death certificate (Acte de décès) from civil status registry",
            "Medical certificate of cause of death (Certificat médical de constat de décès)",
            "Prosecutor clearance for non-natural deaths (Parquet Général)",
            "Embalming and preparation certificate from licensed Luxembourg funeral director",
            "Export authorisation from Luxembourg health authorities",
            "British Embassy Luxembourg consular notification",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Luxembourg is predominantly Roman Catholic, though secularism is widespread. Christian burial practice is common. A significant Portuguese, Italian, and international community exists given the EU institutions. Cremation is available and commonly used.",
        "cremation_available": True,
        "cremation_notes": "Luxembourg has modern cremation facilities. Ashes can be repatriated to the UK as accompanied or unaccompanied baggage under standard airline and courier rules. Export of ashes requires cremation certificate and health authority clearance.",
        "no_go_zones": [],
        "risk_highlights": [
            "Very low personal safety risk — Luxembourg consistently ranks among the safest countries in Europe",
            "Deaths most often involve road accidents or medical emergencies in the financial district",
            "EU institution employees form a significant proportion of British nationals in Luxembourg",
            "Ardennes region: rural road accidents and hiking incidents are the most common context outside the capital"
        ]
    },
    "uruguay": {
        "country_name": "Uruguay",
        "country_adjective": "Uruguayan",
        "flag": "\U0001f1fa\U0001f1fe",
        "region": "South America",
        "languages": ["Spanish"],
        "currency": "Uruguayan Peso (UYU)",
        "british_representation": "British Embassy, Montevideo",
        "embassy_type": "Embassy",
        "embassy_city": "Montevideo",
        "local_authority_involved": "Civil Registry (Registro Civil) for death registration; Medical Examiner (Médico Forense) and Ministry of Public Health for cause of death certification; judiciary for non-natural deaths",
        "main_airports": [
            "Montevideo Carrasco International Airport (MVD)"
        ],
        "routing_notes": "Repatriation from Montevideo routes via Buenos Aires Ezeiza (EZE) or São Paulo Guarulhos (GRU) for transatlantic connections to London. Direct Montevideo-London flights do not exist. Iberia Madrid and Air France Paris connections are common. Total cargo journey 2 to 4 days once paperwork is cleared.",
        "typical_cost_gbp_min": 3500,
        "typical_cost_gbp_max": 8000,
        "typical_cost_notes": "Costs reflect South American routing requirements via Buenos Aires or São Paulo for transatlantic legs. Uruguay's efficient civil service keeps documentation costs moderate relative to neighbours. Growing expat and retirement community means local specialist firms have experience with UK repatriations.",
        "typical_timeline_days_min": 14,
        "typical_timeline_days_max": 28,
        "timeline_notes": "14 to 28 days is typical. Uruguay's civil institutions are efficient by South American standards. The Registro Civil processes death certificates in reasonable time. Routing complexity via Buenos Aires adds days to cargo transit. Non-natural deaths requiring medical examiner involvement can extend timelines.",
        "complexity_rating": "medium",
        "complexity_notes": "Uruguay is a stable, well-governed South American country with a functioning civil service and a resident British Embassy in Montevideo. It has one of the highest standards of living in South America and a growing expat and retirement community of British and Irish nationals. The main complexity factors are: Spanish-language documentation requiring certified translation, routing via Buenos Aires or São Paulo, and the requirement for Medical Examiner certification for any sudden or unnatural death. Uruguay allows cremation. The country is regarded as low-risk for personal safety.",
        "required_documents": [
            "Uruguayan death certificate (Partida de Defunción) from Registro Civil",
            "Medical Examiner certificate for sudden or non-natural deaths",
            "Police report for violent or suspicious deaths",
            "Ministry of Public Health export permit",
            "Embalming and preparation certificate",
            "British Embassy Montevideo consular notification",
            "Apostille of all official documents under the Hague Convention",
            "Certified Spanish-to-English translations of all documents",
            "UK Coroner notification on arrival"
        ],
        "religion_notes": "Uruguay is one of the most secular countries in South America. Roman Catholicism is nominally predominant but secularism is widespread. Both burial and cremation are common. No significant religious restrictions on repatriation procedures.",
        "cremation_available": True,
        "cremation_notes": "Modern cremation facilities are available in Montevideo. Ashes can be repatriated to the UK as accompanied or unaccompanied baggage. Export of ashes requires cremation certificate, Registro Civil documentation, and apostille.",
        "no_go_zones": [],
        "risk_highlights": [
            "Uruguay is one of South America's safest countries — low violent crime relative to regional neighbours",
            "Petty theft in Montevideo's Ciudad Vieja and at Pocitos beach is the most common risk",
            "Road accidents on rural highways are the primary cause of tourist deaths",
            "Punta del Este summer season (December to March) — high UK visitor concentration, seasonal case volume"
        ]
    }
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Check none already exist
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
