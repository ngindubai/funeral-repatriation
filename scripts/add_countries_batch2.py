"""
Add Batch 2 countries to site/data/countries_repatriation.json.
Countries: singapore, ireland, maldives, jamaica, croatia
Run from project root: python scripts/add_countries_batch2.py
"""
import json
import os

DATA_FILE = os.path.join("site", "data", "countries_repatriation.json")

NEW_COUNTRIES = {
    "singapore": {
        "name": "Singapore",
        "slug": "singapore",
        "iso_code": "SG",
        "priority": "P3",
        "death_volume_rank": 32,
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "10-14 days",
            "complex_case": "21+ days",
            "complexity_factors": [
                "Coroner's inquiry (Coroners Act 2010) for sudden or unnatural deaths",
                "Police investigation for accidents or violent deaths",
                "Documentation delays over public holidays (Chinese New Year, Deepavali)",
                "Pathologist availability for post-mortem"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 3,500-8,000",
            "breakdown": {
                "embalming": "GBP 350-700",
                "zinc_lined_coffin": "GBP 500-1,000",
                "documentation_fees": "GBP 200-450",
                "freight_to_uk": "GBP 1,500-3,500",
                "local_funeral_director": "GBP 800-1,800"
            },
            "cost_notes": "Singapore's efficient administration and Changi Airport's world-class cargo infrastructure keep logistics costs competitive for the region. Singapore Airlines operates frequent direct cargo services to London Heathrow. The main variable is whether a Coroner's inquiry is required.",
            "insurance_note": "Singapore is a major hub for British expatriates working in finance and technology. Many have employer-provided cover, but this often excludes repatriation to the UK. Independent travellers should confirm comprehensive travel insurance before departure. Medical costs in Singapore before death can be high."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in Singapore",
                "details": "Call 995 for ambulance or 999 for police. In Singapore, a registered medical practitioner must certify the death and issue a Notice of Death. Any sudden, unnatural, or violent death must be reported to the police and the Coroner under the Coroners Act 2010. The police will investigate and refer to the State Coroner if required. Contact your insurer and the British High Commission immediately.",
                "local_emergency_number": "995 (ambulance), 999 (police)"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Singapore Death Certificate",
                "local_term": "Death Certificate (English)",
                "processing_time": "1-3 working days",
                "multilingual_available": False,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British High Commission Singapore",
                "embassy_phone": "+65 6424 4200",
                "consulate_locations": ["Singapore (High Commission)"],
                "embassy_can_do": [
                    "Provide list of funeral directors with UK repatriation experience",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Coroner's inquiry proceedings",
                    "Make funeral arrangements"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in Singapore",
                "required_for_repatriation": True,
                "details": "Embalming is required for international repatriation under UK regulations. Singapore has well-established funeral directors experienced with international repatriation, particularly for the large expatriate community.",
                "typical_cost_gbp": "GBP 350-700"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required by UK regulations. This is sourced as standard by international funeral directors in Singapore.",
                "typical_cost_gbp": "GBP 500-1,000"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "3-7 working days",
                "documents_needed": [
                    "Singapore Death Certificate",
                    "Coroner's clearance (if applicable)",
                    "Embalming certificate",
                    "Freedom from infection certificate",
                    "Export permit for human remains (Health Sciences Authority)",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 1,500-3,500",
                "flight_time": "13-14 hours direct",
                "main_airlines_with_cargo": ["Singapore Airlines cargo", "British Airways", "Virgin Atlantic"],
                "main_routes_to_uk": ["Singapore Changi (SIN) to London Heathrow (LHR)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow"],
                "coroner_involvement": "The UK coroner is notified on arrival. Singapore's English-language documentation and clear cause of death certification mean UK coroner review is rarely required for natural causes. Deaths investigated by the Singapore State Coroner with shared findings are typically cleared without UK inquest."
            }
        },
        "post_mortem": {
            "when_required": "Required for any sudden, unnatural, or violent death under the Coroners Act 2010. The State Coroner has broad jurisdiction and Singapore's forensic pathology services at the Health Sciences Authority are well-resourced.",
            "impact_on_timeline": "Adds 5-14 days. Singapore's system is efficient compared to many countries, but the Coroner's inquiry must run its full course before the body is released."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Singapore",
                "phone": "+65 6424 4200",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-high-commission-singapore"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "Singapore has a high cremation rate. Cremation can proceed once the Coroner releases the body. Ashes can be carried as hand luggage to the UK with a cremation certificate issued by the Singapore crematorium and a Health Sciences Authority export permit. Singapore Airlines permits ashes in hand luggage on flights to London."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Singapore to the UK take?",
                "How much does it cost to repatriate a body from Singapore to the UK?",
                "What does the Singapore Coroner do when a British national dies?",
                "Can I bring cremated ashes from Singapore to the UK on a plane?",
                "What if my family member dies in Singapore without travel insurance?"
            ]
        }
    },
    "ireland": {
        "name": "Ireland",
        "slug": "ireland",
        "iso_code": "IE",
        "priority": "P3",
        "death_volume_rank": 33,
        "typical_timeline": {
            "fastest_case": "3 days",
            "average_case": "5-10 days",
            "complex_case": "21+ days",
            "complexity_factors": [
                "Irish Coroner's inquest for sudden or violent deaths",
                "Death in a remote rural area (Connemara, Donegal, west coast)",
                "Bank holiday delays (Ireland has frequent public holidays)",
                "Post-mortem required before death certificate can be issued"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 1,500-4,000",
            "breakdown": {
                "embalming": "GBP 200-450",
                "zinc_lined_coffin": "GBP 350-750",
                "documentation_fees": "GBP 100-250",
                "freight_to_uk": "GBP 300-800",
                "local_funeral_director": "GBP 500-1,100"
            },
            "cost_notes": "Ireland is the lowest-cost repatriation origin for UK families. The proximity, English language, similar legal system, and frequent sea and air links to the UK keep all costs down. Road and ferry repatriation is also an option, removing air freight entirely for some families.",
            "insurance_note": "Many British travellers to Ireland do not take out travel insurance, assuming proximity makes it unnecessary. Irish hospital costs are high for non-EU/non-EEA residents since Brexit. FCDO strongly recommends travel insurance for Ireland, including health and repatriation cover."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in Ireland",
                "details": "Call 999 or 112 for emergency services. A registered medical practitioner must certify the death. In Ireland, sudden, violent, or unexplained deaths are reported to the Garda (police) and referred to the local Coroner under the Coroner's Act 1962 (as amended). Contact your insurer and FCDO. Note: the British Embassy in Dublin can assist, but Ireland's English-language system means families can often deal directly with Irish funeral directors without embassy intermediary.",
                "local_emergency_number": "999 or 112"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Irish Death Certificate",
                "local_term": "Death Certificate (English)",
                "processing_time": "1-5 working days",
                "multilingual_available": False,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British Embassy Ireland",
                "embassy_phone": "+353 1 205 3700",
                "consulate_locations": ["Dublin (Embassy)"],
                "embassy_can_do": [
                    "Assist with contacting family in the UK",
                    "Provide guidance on Irish death registration",
                    "Issue emergency travel document if needed"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Irish Coroner's proceedings",
                    "Make funeral arrangements"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in Ireland",
                "required_for_repatriation": True,
                "details": "Embalming is required for air or sea repatriation under UK regulations. Irish funeral directors are experienced with UK repatriation. Road and ferry repatriation may have different requirements and can be discussed directly with the funeral director.",
                "typical_cost_gbp": "GBP 200-450"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required for air repatriation. For road and ferry repatriation, requirements may differ. Confirm with your UK funeral director.",
                "typical_cost_gbp": "GBP 350-750"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "2-5 working days",
                "documents_needed": [
                    "Irish Death Certificate",
                    "Coroner's release (if applicable)",
                    "Embalming certificate",
                    "Freedom from infection certificate",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Transport to the UK",
                "typical_freight_cost_gbp": "GBP 300-800",
                "flight_time": "1-2 hours by air; 3-8 hours by ferry depending on route",
                "main_airlines_with_cargo": ["Aer Lingus", "British Airways", "Ryanair cargo"],
                "main_routes_to_uk": ["Dublin (DUB) to London Heathrow (LHR)", "Dublin (DUB) to Manchester (MAN)", "Dublin to Holyhead (ferry/road)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow", "Manchester", "Birmingham", "UK port of entry for ferry"],
                "coroner_involvement": "The UK coroner is notified on arrival. Ireland's English-language death certification and similar legal framework mean UK coroner involvement is rare for natural causes. Deaths investigated by the Irish Coroner with shared findings are typically cleared without further UK inquest."
            }
        },
        "post_mortem": {
            "when_required": "Required for sudden, violent, or unexplained deaths under the Irish Coroner's Act 1962. The Irish Coroner must be satisfied with the cause of death before releasing the body. Road accidents and drownings are the most common triggers for British nationals.",
            "impact_on_timeline": "Adds 3-14 days. Post-mortem results and the Coroner's formal release are required before repatriation can proceed."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Dublin",
                "phone": "+353 1 205 3700",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-embassy-dublin"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "Ireland has cremation facilities in Dublin, Cork, and other major cities. Cremation rates in Ireland are lower than the UK but increasing. Ashes can be brought to the UK by hand without special permits. No export restriction applies to ashes transported between Ireland and the UK."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Ireland to the UK take?",
                "How much does it cost to repatriate a body from Ireland to the UK?",
                "Can a body be repatriated from Ireland by road and ferry?",
                "Do I need travel insurance for Ireland?",
                "What does the Irish Coroner do when a British national dies?"
            ]
        }
    },
    "maldives": {
        "name": "Maldives",
        "slug": "maldives",
        "iso_code": "MV",
        "priority": "P3",
        "death_volume_rank": 34,
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "14-21 days",
            "complex_case": "35+ days",
            "complexity_factors": [
                "Death on a remote resort island requiring speedboat or seaplane transfer to Male",
                "Post-mortem ordered by Maldivian authorities (limited pathology capacity in Male)",
                "No cremation permitted in the Maldives",
                "Islamic law jurisdiction as a 100% Muslim nation affects process for Muslim deceased"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 5,000-14,000",
            "breakdown": {
                "embalming": "GBP 400-800",
                "zinc_lined_coffin": "GBP 600-1,200",
                "documentation_fees": "GBP 300-600",
                "freight_to_uk": "GBP 2,000-5,000",
                "local_funeral_director": "GBP 800-2,000",
                "island_transfer_to_male": "GBP 300-800"
            },
            "cost_notes": "The Maldives is one of the most logistically complex repatriation origins due to island geography. Virtually every death occurs on a resort island. Transfer to Male (the capital) is required before any repatriation process can begin. This transfer adds cost and time. International cargo routes operate from Velana International Airport (Male).",
            "insurance_note": "The Maldives is an exclusively luxury destination. Comprehensive travel insurance including full repatriation is essential and should be in place before booking. The FCDO notes the Maldives as a destination where health and repatriation costs can be extreme due to isolation and limited local medical infrastructure."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in the Maldives",
                "details": "Call the resort's emergency number immediately. The resort has a duty to notify the Maldives Police Service and arrange transfer to Male. The Maldives has no death certification infrastructure on resort islands. All official processes require physical presence in Male. Call 119 for ambulance in Male. Contact your insurer and the British High Commission in Colombo (which covers the Maldives) immediately.",
                "local_emergency_number": "119"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Maldivian Death Certificate",
                "local_term": "Death Certificate (Dhivehi/English)",
                "processing_time": "3-7 working days after arrival in Male",
                "multilingual_available": True,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British High Commission (covers Maldives from Colombo)",
                "embassy_phone": "+94 11 539 0639",
                "consulate_locations": ["Colombo, Sri Lanka (covers Maldives)"],
                "embassy_can_do": [
                    "Provide list of funeral directors and repatriation agents in Male",
                    "Assist with contacting family in the UK",
                    "Issue emergency travel document if needed"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Provide consular presence on resort islands",
                    "Intervene in Maldivian police proceedings"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in the Maldives",
                "required_for_repatriation": True,
                "details": "Embalming is required for international repatriation. Embalming facilities exist in Male but are limited. The Maldives is a 100% Islamic nation. For Muslim deceased, embalming is generally not permissible under Islamic law. Non-Muslim families should confirm embalming availability with the funeral director in Male immediately.",
                "typical_cost_gbp": "GBP 400-800"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required for repatriation. Zinc-lined coffins are not a standard local item and must be sourced, which can add further time. Specialist repatriation agents in Male handle this.",
                "typical_cost_gbp": "GBP 600-1,200"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "5-10 working days",
                "documents_needed": [
                    "Maldivian Death Certificate",
                    "Police clearance",
                    "Post-mortem report (if applicable)",
                    "Embalming certificate",
                    "Freedom from infection certificate",
                    "Permission to export remains from the Maldives",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 2,000-5,000",
                "flight_time": "10-12 hours to London (typically via Dubai, Doha, or Colombo)",
                "main_airlines_with_cargo": ["Emirates cargo", "Qatar Airways cargo", "SriLankan Airlines"],
                "main_routes_to_uk": ["Male Velana (MLE) to London Heathrow (LHR) via Dubai or Doha"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow"],
                "coroner_involvement": "The UK coroner is notified on arrival. Maldivian documentation in English with certified cause of death is required. Deaths from natural causes with full documentation are unlikely to require UK inquest."
            }
        },
        "post_mortem": {
            "when_required": "Required for any sudden, unnatural, or unexplained death. Maldivian pathology capacity is limited to Male, so post-mortems can take longer than in countries with distributed forensic infrastructure. Water-related deaths (drowning, diving accidents) are the most common complex cases for British nationals.",
            "impact_on_timeline": "Adds 7-21 days. Limited pathology capacity in Male is the most frequent cause of extended timelines."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Colombo (covers Maldives)",
                "phone": "+94 11 539 0639",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-high-commission-colombo"
            }
        },
        "ashes_transport": {
            "cremation_available": False,
            "critical_warning": "Cremation is not available in the Maldives. The Maldives is a 100% Muslim nation and cremation is forbidden under Islamic law. All deceased must be repatriated as full remains or buried locally according to Islamic rites. There are no exceptions to this rule. Families must plan for full-body repatriation from the outset.",
            "notes": "Full-body repatriation is the only option from the Maldives for non-Muslim families wishing to bring their loved one home. This significantly increases cost and complexity compared to destinations where cremation is available."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from the Maldives to the UK take?",
                "How much does it cost to repatriate a body from the Maldives to the UK?",
                "Can someone be cremated in the Maldives?",
                "What happens if a British tourist dies on a resort island in the Maldives?",
                "Which British embassy covers the Maldives?"
            ]
        }
    },
    "jamaica": {
        "name": "Jamaica",
        "slug": "jamaica",
        "iso_code": "JM",
        "priority": "P3",
        "death_volume_rank": 35,
        "typical_timeline": {
            "fastest_case": "10 days",
            "average_case": "14-21 days",
            "complex_case": "35+ days",
            "complexity_factors": [
                "Jamaican Coroner's inquest for violent or suspicious deaths",
                "Crime-related death (Jamaica has a high violent crime rate affecting tourists in certain areas)",
                "Post-mortem at Kingston Public Hospital (capacity limitations)",
                "Documentation processing delays"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 3,500-9,000",
            "breakdown": {
                "embalming": "GBP 350-700",
                "zinc_lined_coffin": "GBP 500-1,000",
                "documentation_fees": "GBP 200-450",
                "freight_to_uk": "GBP 1,500-4,000",
                "local_funeral_director": "GBP 700-1,600"
            },
            "cost_notes": "Direct flights from Kingston and Montego Bay to London Gatwick make freight logistics more straightforward than some Caribbean destinations. The main cost variable is whether a post-mortem is required and whether any police investigation extends the process.",
            "insurance_note": "Jamaica is a popular Caribbean destination for British tourists, with a large Jamaican-British diaspora also visiting family. Travel insurance including full repatriation cover is recommended. FCDO travel advice for Jamaica notes a high violent crime rate; certain areas carry significant risk."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in Jamaica",
                "details": "Call 119 for ambulance or 119 for police. A registered medical practitioner must certify the death. Any sudden, violent, or suspicious death is reported to the Coroner. Jamaica has a high violent crime rate and some tourist deaths are crime-related, which automatically triggers a police investigation. Contact your insurer and the British High Commission Kingston immediately.",
                "local_emergency_number": "119"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Jamaican Death Certificate",
                "local_term": "Death Certificate (English)",
                "processing_time": "3-7 working days",
                "multilingual_available": False,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British High Commission Jamaica",
                "embassy_phone": "+1 876 936 0700",
                "consulate_locations": ["Kingston (High Commission)"],
                "embassy_can_do": [
                    "Provide list of local funeral directors with UK repatriation experience",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Jamaican police or Coroner proceedings",
                    "Make funeral arrangements"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in Jamaica",
                "required_for_repatriation": True,
                "details": "Embalming is required for international repatriation. Jamaica has a well-established funeral industry serving both the domestic market and the large diaspora community. Certified embalmers operate in Kingston and Montego Bay.",
                "typical_cost_gbp": "GBP 350-700"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required by UK regulations. Available through funeral directors in Kingston and Montego Bay.",
                "typical_cost_gbp": "GBP 500-1,000"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "5-10 working days",
                "documents_needed": [
                    "Jamaican Death Certificate",
                    "Coroner's release (if applicable)",
                    "Police clearance (for violent or suspicious deaths)",
                    "Embalming certificate",
                    "Freedom from infection certificate",
                    "Export permit for human remains",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 1,500-4,000",
                "flight_time": "9-10 hours direct",
                "main_airlines_with_cargo": ["British Airways", "TUI Airways cargo", "Virgin Atlantic"],
                "main_routes_to_uk": ["Kingston Norman Manley (KIN) to London Gatwick (LGW)", "Montego Bay Sangster (MBJ) to London Gatwick (LGW)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Gatwick", "London Heathrow"],
                "coroner_involvement": "The UK coroner is notified on arrival. Deaths investigated in Jamaica with certified English-language documentation are usually cleared without UK inquest for natural causes. Crime-related deaths with ongoing Jamaican investigations may require UK coroner involvement."
            }
        },
        "post_mortem": {
            "when_required": "Required for sudden, violent, or suspicious deaths. The Coroner's jurisdiction covers these cases. Post-mortems are performed at Kingston Public Hospital. Capacity can be limited and delays occur.",
            "impact_on_timeline": "Adds 7-21 days. Crime-related deaths can take significantly longer if police investigations run in parallel."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Kingston",
                "phone": "+1 876 936 0700",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-high-commission-kingston"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "Cremation is available in Jamaica. Ashes can be carried as hand luggage on flights to the UK with a cremation certificate. The Jamaican-British diaspora community means some families opt for local burial followed by ashes transport at a later date."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Jamaica to the UK take?",
                "How much does it cost to repatriate a body from Jamaica to the UK?",
                "What happens if a British tourist dies violently in Jamaica?",
                "Can I bring cremated ashes from Jamaica to the UK on a plane?",
                "What documents are needed to bring a body home from Jamaica?"
            ]
        }
    },
    "croatia": {
        "name": "Croatia",
        "slug": "croatia",
        "iso_code": "HR",
        "priority": "P3",
        "death_volume_rank": 36,
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "10-16 days",
            "complex_case": "25+ days",
            "complexity_factors": [
                "Croatian judicial investigation ordered by state attorney",
                "Death on a Dalmatian island (ferry transfer to Split or Dubrovnik required)",
                "Seasonal capacity constraints in summer (July-August — peak tourist deaths)",
                "Documentation processing during Croatian public holidays"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 2,500-6,500",
            "breakdown": {
                "embalming": "GBP 300-600",
                "zinc_lined_coffin": "GBP 400-850",
                "documentation_fees": "GBP 200-400",
                "freight_to_uk": "GBP 700-2,000",
                "local_funeral_director": "GBP 600-1,400"
            },
            "cost_notes": "Croatia has two main international airports for repatriation purposes: Split (SPU) and Dubrovnik (DBV). Both handle cargo, though capacity can be constrained in peak summer season. Zagreb is the main hub but requires domestic transfer from coastal areas. Costs are broadly comparable to other Southern European destinations.",
            "insurance_note": "Croatia is a rapidly growing British tourist destination, particularly Dubrovnik, Split, and the Dalmatian islands. Summer months (June-September) see high visitor volumes and a corresponding increase in accident-related deaths. Comprehensive travel insurance is strongly recommended."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in Croatia",
                "details": "Call 112 for emergency services. A physician must certify the death. Unnatural deaths are referred to the state attorney (državni odvjetnik), who decides whether a judicial investigation is required. Croatia has a civil law system based on the continental European model. Contact your insurer and the British Embassy Zagreb immediately.",
                "local_emergency_number": "112"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Croatian Death Certificate",
                "local_term": "Smrtni List (Death Certificate)",
                "processing_time": "2-5 working days",
                "multilingual_available": False,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British Embassy Croatia",
                "embassy_phone": "+385 1 600 9100",
                "consulate_locations": ["Zagreb (Embassy)", "Split (Honorary Consulate)"],
                "embassy_can_do": [
                    "Provide list of funeral directors with UK repatriation experience",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Croatian judicial proceedings",
                    "Make funeral arrangements"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in Croatia",
                "required_for_repatriation": True,
                "details": "Embalming is required for international repatriation. Croatia has experienced funeral directors in Split, Dubrovnik, and Zagreb. Island deaths require transport to the mainland before preparation can begin.",
                "typical_cost_gbp": "GBP 300-600"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required by UK regulations. Standard at Croatian funeral directors handling international repatriation.",
                "typical_cost_gbp": "GBP 400-850"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "3-7 working days",
                "documents_needed": [
                    "Smrtni List (Croatian death certificate)",
                    "Medical certificate of cause of death",
                    "State attorney clearance (if judicial investigation)",
                    "Embalming certificate",
                    "Freedom from infection certificate",
                    "Permission to transport remains from Croatia",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 700-2,000",
                "flight_time": "2.5-3 hours direct",
                "main_airlines_with_cargo": ["Croatia Airlines", "British Airways", "Jet2 cargo", "easyJet"],
                "main_routes_to_uk": ["Split (SPU) to London Gatwick (LGW)", "Dubrovnik (DBV) to London Gatwick (LGW)", "Zagreb (ZAG) to London Gatwick (LGW)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Gatwick", "London Heathrow", "Manchester"],
                "coroner_involvement": "The UK coroner is notified on arrival. Deaths certified by Croatian authorities with cause of death documented are unlikely to require UK inquest for natural causes. Deaths involving state attorney investigation may require review."
            }
        },
        "post_mortem": {
            "when_required": "Required when the state attorney orders a judicial investigation for unnatural, violent, or suspicious deaths. Road accidents involving tourists and drowning incidents on the Dalmatian coast are the most common complex cases.",
            "impact_on_timeline": "Adds 5-14 days. Summer season capacity constraints can extend timelines for island cases where local authority resources are stretched."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Zagreb",
                "phone": "+385 1 600 9100",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-embassy-zagreb"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "Cremation is available in Croatia. Ashes can be carried as hand luggage on flights to the UK with a Croatian cremation certificate. Croatia's cremation rate is relatively low (Catholic country) but cremation facilities are available in Zagreb and Split."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Croatia to the UK take?",
                "How much does it cost to repatriate a body from Croatia to the UK?",
                "What happens if a British tourist dies on a Croatian island?",
                "Can I bring cremated ashes from Croatia to the UK on a plane?",
                "What documents are needed to bring a body home from Croatia?"
            ]
        }
    }
}

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, country_data in NEW_COUNTRIES.items():
        if key in data["countries"]:
            print(f"  SKIPPED (already exists): {key}")
        else:
            data["countries"][key] = country_data
            print(f"  Added: {key}")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Total countries: {len(data['countries'])}")

if __name__ == "__main__":
    main()
