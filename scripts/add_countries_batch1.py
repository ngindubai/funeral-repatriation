"""
Add 5 new countries to site/data/countries_repatriation.json.
Countries: malta, new-zealand, netherlands, japan, malaysia
Run from project root: python scripts/add_countries_batch1.py
"""
import json
import os

DATA_FILE = os.path.join("site", "data", "countries_repatriation.json")

NEW_COUNTRIES = {
    "malta": {
        "name": "Malta",
        "slug": "malta",
        "iso_code": "MT",
        "priority": "P3",
        "death_volume_rank": 27,
        "typical_timeline": {
            "fastest_case": "5 days",
            "average_case": "8-12 days",
            "complex_case": "21+ days",
            "complexity_factors": [
                "Post-mortem ordered by Maltese coroner",
                "Weekend or public holiday delays",
                "Documentation missing from the deceased's home country",
                "Insurance disputes causing hold"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 2,500-5,500",
            "breakdown": {
                "embalming": "GBP 250-500",
                "zinc_lined_coffin": "GBP 400-800",
                "documentation_fees": "GBP 150-350",
                "freight_to_uk": "GBP 800-1,800",
                "local_funeral_director": "GBP 600-1,200"
            },
            "cost_notes": "Malta is one of the lower-cost European repatriation origins. Short flight times to the UK mean freight costs are comparatively modest. The main variable is whether a post-mortem is required.",
            "insurance_note": "FCDO travel insurance statistics show Malta is a high-claim destination relative to its visitor volume, particularly for older travellers with pre-existing conditions. Confirm your policy covers repatriation before travel."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in Malta",
                "details": "Call 112 for police and ambulance. A doctor must certify the death before the body can be moved. If the death is sudden or unnatural, the Maltese police will involve the duty magistrate, who may order a post-mortem. Contact your travel insurer and FCDO within 24 hours.",
                "local_emergency_number": "112"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Maltese Death Certificate",
                "local_term": "Ċertifikat tal-Mewt",
                "processing_time": "1-3 working days",
                "multilingual_available": True,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British High Commission Malta",
                "embassy_phone": "+356 2323 0000",
                "consulate_locations": ["Valletta"],
                "embassy_can_do": [
                    "Provide list of local funeral directors",
                    "Issue emergency travel document for deceased if needed",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Make arrangements on your behalf",
                    "Intervene in Maltese legal proceedings"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in Malta",
                "required_for_repatriation": True,
                "details": "Embalming is required under UK regulations for repatriation of human remains. Certified embalming services are available at licensed Maltese funeral homes, primarily in the Valletta and Sliema areas.",
                "typical_cost_gbp": "GBP 250-500"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "UK regulations require a zinc-lined or hermetically sealed coffin for repatriated remains. This is standard practice at Maltese funeral homes experienced in international repatriation.",
                "typical_cost_gbp": "GBP 400-800"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "2-5 working days",
                "documents_needed": [
                    "Ċertifikat tal-Mewt (Maltese death certificate)",
                    "Freedom from infection certificate (embalmer's certificate)",
                    "Permission to remove remains from Malta (issued by Maltese authorities)",
                    "Passport of deceased",
                    "Embalming certificate"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 800-1,800",
                "flight_time": "3-4 hours to London",
                "main_airlines_with_cargo": ["Air Malta", "Ryanair cargo", "British Airways"],
                "main_routes_to_uk": ["Malta Luqa (MLA) to London Heathrow (LHR)", "Malta Luqa (MLA) to Manchester (MAN)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow", "Manchester"],
                "coroner_involvement": "The UK coroner is notified on arrival. If the death was investigated in Malta with post-mortem results available, a UK coroner's inquest is unlikely. Deaths from unknown or unnatural causes may require UK coroner review before release to a funeral director."
            }
        },
        "post_mortem": {
            "when_required": "Required when death is sudden, unnatural, or the cause is unclear. The duty magistrate in Malta orders post-mortems for these cases. Common triggers include road accidents, drowning, and deaths without a treating physician.",
            "impact_on_timeline": "Adds 3-10 days depending on pathologist availability and magistrate scheduling. Post-mortem results must be certified before the permission to remove is issued."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Valletta",
                "phone": "+356 2323 0000",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-high-commission-malta"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "Cremation services are available in Malta, though Malta is a predominantly Catholic country and cremation rates remain lower than Northern Europe. The Santa Maria Addolorata Crematorium near Paola is the main facility. UK rules permit carrying ashes on a flight in hand luggage with the cremation certificate."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Malta to the UK take?",
                "How much does it cost to repatriate a body from Malta to the UK?",
                "What documents are needed to bring a body home from Malta?",
                "Can I bring cremated ashes from Malta on a plane to the UK?",
                "What if there is no travel insurance for a death in Malta?"
            ]
        }
    },
    "new-zealand": {
        "name": "New Zealand",
        "slug": "new-zealand",
        "iso_code": "NZ",
        "priority": "P3",
        "death_volume_rank": 28,
        "typical_timeline": {
            "fastest_case": "10 days",
            "average_case": "14-21 days",
            "complex_case": "35+ days",
            "complexity_factors": [
                "Coroner's inquest (New Zealand Coroners Act 2006)",
                "Long-haul freight logistics from Oceania",
                "Insurance dispute or uninsured death",
                "Death in a remote region (Fiordland, Bay of Islands, Queenstown backcountry)"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 5,000-12,000",
            "breakdown": {
                "embalming": "GBP 300-600",
                "zinc_lined_coffin": "GBP 500-1,000",
                "documentation_fees": "GBP 200-400",
                "freight_to_uk": "GBP 2,500-6,000",
                "local_funeral_director": "GBP 800-1,800"
            },
            "cost_notes": "Long-haul freight from New Zealand is the dominant cost factor. Auckland has the strongest cargo connections; deaths in the South Island (Christchurch, Queenstown) require domestic transfer before international freight. Costs are broadly comparable to Australia.",
            "insurance_note": "New Zealand and Australia are favourite destinations for British working holiday (OE) travellers, many of whom travel without adequate repatriation insurance. The FCDO consistently advises comprehensive travel insurance covering repatriation before departing for New Zealand."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in New Zealand",
                "details": "Call 111 for police and ambulance. A doctor or nurse practitioner must certify the death. In New Zealand, a Coroner must be notified of any sudden, unexplained, or violent death under the Coroners Act 2006. The Coroner has jurisdiction over the body until they release it. Contact your insurer and the FCDO immediately.",
                "local_emergency_number": "111"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the New Zealand Death Certificate",
                "local_term": "Death Certificate (English)",
                "processing_time": "3-10 working days (can be extended if coroner involved)",
                "multilingual_available": False,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British High Commission New Zealand",
                "embassy_phone": "+64 4 924 2888",
                "consulate_locations": ["Wellington (High Commission)", "Auckland (Consulate)"],
                "embassy_can_do": [
                    "Provide list of local funeral directors",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Coroner's proceedings",
                    "Make funeral arrangements"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in New Zealand",
                "required_for_repatriation": True,
                "details": "Embalming is required for international repatriation. New Zealand funeral directors are familiar with this requirement. Certified services are available in all main centres.",
                "typical_cost_gbp": "GBP 300-600"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required by UK regulations. New Zealand funeral directors working on international cases will source this as standard.",
                "typical_cost_gbp": "GBP 500-1,000"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "5-14 working days",
                "documents_needed": [
                    "New Zealand Death Certificate",
                    "Coroner's release (if applicable, Coroners Act 2006)",
                    "Embalming certificate",
                    "Permission to transport human remains from New Zealand",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 2,500-6,000",
                "flight_time": "24-26 hours (typically via Singapore, Hong Kong, or Dubai)",
                "main_airlines_with_cargo": ["Air New Zealand cargo", "Singapore Airlines", "Emirates"],
                "main_routes_to_uk": ["Auckland (AKL) to London Heathrow (LHR) via Singapore or Dubai", "Christchurch (CHC) to London Heathrow via Auckland or Singapore"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow"],
                "coroner_involvement": "The UK coroner is notified on arrival. Deaths investigated by the New Zealand Coroner with results shared will usually not require a further UK inquest. Sudden deaths without full investigation may trigger UK coroner review."
            }
        },
        "post_mortem": {
            "when_required": "The New Zealand Coroner has broad jurisdiction under the Coroners Act 2006 and must be notified of any sudden, unnatural, or unexplained death. Post-mortem is ordered at the Coroner's discretion. NZ coroners are generally thorough and the process is well-organised.",
            "impact_on_timeline": "Adds 7-21 days. The Coroner must formally release the body before repatriation can proceed. This is the most common cause of extended timelines for UK families."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Wellington",
                "phone": "+64 4 924 2888",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-high-commission-new-zealand"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "New Zealand has a high cremation rate (around 75%). Cremation can proceed once the Coroner releases the body and, if applicable, post-mortem is completed. Ashes can be carried as hand luggage on flights to the UK. A cremation certificate issued by the New Zealand crematorium and a permit to export human remains are required."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from New Zealand to the UK take?",
                "How much does it cost to repatriate a body from New Zealand to the UK?",
                "What does the New Zealand Coroner do when a British tourist dies?",
                "Can I bring cremated ashes from New Zealand to the UK on a plane?",
                "My family member died in New Zealand with no travel insurance. What happens?"
            ]
        }
    },
    "netherlands": {
        "name": "Netherlands",
        "slug": "netherlands",
        "iso_code": "NL",
        "priority": "P3",
        "death_volume_rank": 29,
        "typical_timeline": {
            "fastest_case": "5 days",
            "average_case": "7-12 days",
            "complex_case": "21+ days",
            "complexity_factors": [
                "Dutch judicial investigation (gerechtelijke sectie) ordered",
                "Death in a canal or waterway (drowning investigations)",
                "Drug-related death in Amsterdam (police involvement is automatic)",
                "Documentation gaps"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 2,500-6,000",
            "breakdown": {
                "embalming": "GBP 300-600",
                "zinc_lined_coffin": "GBP 450-900",
                "documentation_fees": "GBP 150-350",
                "freight_to_uk": "GBP 600-1,500",
                "local_funeral_director": "GBP 700-1,400"
            },
            "cost_notes": "The Netherlands has excellent cargo infrastructure at Amsterdam Schiphol, which reduces freight costs and logistics complexity compared to more remote destinations. The process is efficient when documentation is straightforward.",
            "insurance_note": "Amsterdam sees a significant number of tourist deaths, particularly drug-related incidents and canal accidents. Travel insurance is strongly recommended. Deaths involving illegal substances can complicate insurance claims."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in the Netherlands",
                "details": "Call 112 for emergency services. A treating physician or GGD (Municipal Health Service) doctor must certify the death. Unnatural deaths are automatically referred to police and the public prosecutor. Contact your insurer and the FCDO on the same day.",
                "local_emergency_number": "112"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Dutch Death Certificate",
                "local_term": "Akte van Overlijden",
                "processing_time": "1-3 working days",
                "multilingual_available": True,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British Embassy Netherlands",
                "embassy_phone": "+31 70 427 0427",
                "consulate_locations": ["The Hague (Embassy)", "Amsterdam (Consulate)"],
                "embassy_can_do": [
                    "Provide list of local funeral directors",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration",
                    "Issue emergency travel document for deceased if needed"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Dutch police or prosecutor proceedings",
                    "Make funeral arrangements"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in the Netherlands",
                "required_for_repatriation": True,
                "details": "Embalming is required for international repatriation under UK regulations. Dutch funeral directors in Amsterdam and The Hague are experienced with UK repatriation requirements.",
                "typical_cost_gbp": "GBP 300-600"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required by UK regulations. Standard practice at Dutch funeral directors handling international repatriation.",
                "typical_cost_gbp": "GBP 450-900"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "2-5 working days",
                "documents_needed": [
                    "Akte van Overlijden (Dutch death certificate)",
                    "Medical certificate of cause of death (Verklaring van Overlijden)",
                    "Freedom from infection certificate",
                    "Permission to transport human remains from the Netherlands",
                    "Embalming certificate",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 600-1,500",
                "flight_time": "1 hour to London",
                "main_airlines_with_cargo": ["KLM Cargo", "British Airways", "easyJet (cargo)", "Transavia"],
                "main_routes_to_uk": ["Amsterdam Schiphol (AMS) to London Heathrow (LHR)", "Amsterdam Schiphol (AMS) to Manchester (MAN)", "Amsterdam Schiphol (AMS) to Edinburgh (EDI)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow", "Manchester", "Edinburgh"],
                "coroner_involvement": "The UK coroner is notified on arrival. Deaths investigated by Dutch authorities with certified cause of death are unlikely to require UK inquest. Unresolved or drug-related deaths may require UK coroner review."
            }
        },
        "post_mortem": {
            "when_required": "Required for any unnatural death, death in a public place, or where the cause is unclear. In Amsterdam, deaths involving drugs automatically trigger police involvement and referral to the public prosecutor, who may order a judicial post-mortem (gerechtelijke sectie).",
            "impact_on_timeline": "Adds 3-14 days. Canal drownings and drug-related deaths are the most common complex cases involving British nationals in the Netherlands."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "The Hague",
                "phone": "+31 70 427 0427",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-embassy-the-hague"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "The Netherlands has a high cremation rate (around 65%). Dutch crematoriums are modern and the process is efficient. Ashes can be carried as hand luggage to the UK with a cremation certificate. Export permits for ashes are not required from the Netherlands."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from the Netherlands to the UK take?",
                "How much does it cost to repatriate a body from Amsterdam to the UK?",
                "What happens if a British tourist dies in Amsterdam?",
                "Can I bring cremated ashes from the Netherlands to the UK on a plane?",
                "What documents are needed to bring a body home from the Netherlands?"
            ]
        }
    },
    "japan": {
        "name": "Japan",
        "slug": "japan",
        "iso_code": "JP",
        "priority": "P3",
        "death_volume_rank": 30,
        "typical_timeline": {
            "fastest_case": "10 days",
            "average_case": "14-21 days",
            "complex_case": "35+ days",
            "complexity_factors": [
                "Police investigation for unnatural deaths (Keisatsu notification mandatory)",
                "Translation of all Japanese documents into English required",
                "Japanese judicial post-mortem (gyousei kansatsu) ordered",
                "Death in a remote area (Japan Alps, rural Kyushu, Hokkaido)"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 4,000-10,000",
            "breakdown": {
                "embalming": "GBP 400-900",
                "zinc_lined_coffin": "GBP 600-1,200",
                "documentation_fees": "GBP 300-600",
                "freight_to_uk": "GBP 1,800-4,000",
                "local_funeral_director": "GBP 900-2,000",
                "document_translation": "GBP 200-500"
            },
            "cost_notes": "Japan's funeral industry is highly developed but oriented entirely towards cremation. Full-body repatriation is unusual for Japanese families (Japan has a 99.9% cremation rate) but is a standard requirement for British families. Funeral directors experienced with Western repatriation requirements are primarily found in Tokyo and Osaka.",
            "insurance_note": "Travel insurance is essential for Japan. The cost of medical care in Japan before death can be very high, and repatriation costs are significant. Confirm your policy covers full-body repatriation, not just cremation and ashes return."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in Japan",
                "details": "Call 119 for ambulance or 110 for police. In Japan, a licensed physician must certify the death and issue a death notification document. Any sudden, unnatural, or suspicious death is automatically referred to the police (Keisatsu) and may be subject to a judicial administrative inspection. Contact your insurer and the British Embassy Tokyo immediately.",
                "local_emergency_number": "119 (ambulance), 110 (police)"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Japanese Death Certificate",
                "local_term": "死亡診断書 (Shi-bou Shindan-sho)",
                "processing_time": "2-5 working days",
                "multilingual_available": False,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British Embassy Japan",
                "embassy_phone": "+81 3 5211 1100",
                "consulate_locations": ["Tokyo (Embassy)", "Osaka (Consulate-General)"],
                "embassy_can_do": [
                    "Provide list of funeral directors experienced with Western repatriation",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration",
                    "Help with document translation coordination"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Japanese police or judicial proceedings",
                    "Translate documents officially"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in Japan",
                "required_for_repatriation": True,
                "details": "Embalming for international repatriation is available in Tokyo and Osaka through specialist funeral directors. It is not a standard practice in Japan (where cremation is the norm), so it is essential to engage a funeral director with documented experience in international repatriation.",
                "typical_cost_gbp": "GBP 400-900"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required. Japan does not manufacture these as standard items, so they are typically sourced by specialist international funeral directors in Tokyo or Osaka. Allow extra time for procurement.",
                "typical_cost_gbp": "GBP 600-1,200"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "5-10 working days",
                "documents_needed": [
                    "死亡診断書 (Japanese death certificate) with certified English translation",
                    "Police release document (if applicable)",
                    "Embalming certificate",
                    "Permission to export human remains from Japan (Ministry of Health involvement)",
                    "Passport of deceased",
                    "Certified translations of all Japanese documents"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 1,800-4,000",
                "flight_time": "12-14 hours direct",
                "main_airlines_with_cargo": ["Japan Airlines cargo", "ANA Cargo", "British Airways", "Virgin Atlantic"],
                "main_routes_to_uk": ["Tokyo Narita (NRT) to London Heathrow (LHR)", "Osaka Kansai (KIX) to London Heathrow (LHR)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow"],
                "coroner_involvement": "The UK coroner is notified on arrival. Certified cause of death documentation from Japan with English translation should be presented. Deaths from natural causes are unlikely to require UK inquest. Unnatural deaths may be reviewed."
            }
        },
        "post_mortem": {
            "when_required": "In Japan, any sudden, unnatural, suspicious, or unattended death triggers mandatory police notification and a gyousei kansatsu (administrative inspection). A judicial post-mortem is ordered if the cause of death is unclear. Japan's forensic pathology infrastructure is well-developed.",
            "impact_on_timeline": "Adds 7-21 days. Translation of Japanese documents adds further time. This is the most common source of extended timelines for UK families."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Tokyo",
                "phone": "+81 3 5211 1100",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-embassy-tokyo"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "critical_warning": "Japan has a cremation rate of approximately 99.9% (Ministry of Health, Labour and Welfare, 2022). Cremation is the default outcome for deaths in Japan, including deaths of foreign nationals. If your family member has religious or personal objections to cremation, you must act quickly and explicitly instruct the Japanese funeral director and hospital that full-body repatriation is required. This must be documented in writing before any preparations begin.",
            "notes": "Ashes can be transported to the UK as hand luggage. A cremation certificate issued by the Japanese crematorium and an export permit from the local ward office (kuyakusho) are required."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Japan to the UK take?",
                "How much does it cost to repatriate a body from Japan to the UK?",
                "Will my family member be cremated in Japan without my consent?",
                "What documents are needed to bring a body home from Japan?",
                "Can I bring cremated ashes from Japan to the UK on a plane?"
            ]
        }
    },
    "malaysia": {
        "name": "Malaysia",
        "slug": "malaysia",
        "iso_code": "MY",
        "priority": "P3",
        "death_volume_rank": 31,
        "typical_timeline": {
            "fastest_case": "8 days",
            "average_case": "10-21 days",
            "complex_case": "35+ days",
            "complexity_factors": [
                "Death on an island or in a remote area (Sabah, Sarawak, offshore islands)",
                "Muslim deceased subject to Sharia court jurisdiction (separate process)",
                "Police investigation for unnatural death",
                "Insurance disputes or uninsured death"
            ]
        },
        "cost_guide": {
            "total_typical_range_gbp": "GBP 3,000-7,000",
            "breakdown": {
                "embalming": "GBP 300-600",
                "zinc_lined_coffin": "GBP 450-900",
                "documentation_fees": "GBP 200-400",
                "freight_to_uk": "GBP 1,200-3,000",
                "local_funeral_director": "GBP 700-1,500"
            },
            "cost_notes": "Kuala Lumpur is well-connected with direct flights to the UK, which keeps freight costs comparatively reasonable. Deaths in East Malaysia (Sabah, Sarawak) or on offshore islands involve domestic transfer costs before international freight.",
            "insurance_note": "British travellers to Malaysia are a mix of tourists and expatriates. Expatriates often have employer-provided cover, but this may not include repatriation. Independent travellers should confirm that their travel insurance includes full repatriation to the UK, not just medical evacuation to Singapore."
        },
        "repatriation_process": {
            "step_1_immediate": {
                "title": "Immediate Steps After a Death in Malaysia",
                "details": "Call 999 for police and ambulance. A registered medical officer must certify the death. Unnatural or sudden deaths are referred to the police and may involve a post-mortem by a government pathologist. If the deceased was Muslim, the Syariah (Sharia) court has jurisdiction and the process follows Islamic law, including preparation for burial within 24 hours. Contact your insurer and the British High Commission immediately.",
                "local_emergency_number": "999"
            },
            "step_2_death_certificate": {
                "title": "Obtaining the Malaysian Death Certificate",
                "local_term": "Sijil Kematian",
                "processing_time": "2-5 working days",
                "multilingual_available": True,
                "shows_cause_of_death": True
            },
            "step_3_embassy_notification": {
                "title": "Notifying the British High Commission Malaysia",
                "embassy_phone": "+60 3 2170 2200",
                "consulate_locations": ["Kuala Lumpur (High Commission)"],
                "embassy_can_do": [
                    "Provide list of local funeral directors",
                    "Assist with contacting family in the UK",
                    "Issue Certified Copy of Death Certificate for UK registration"
                ],
                "embassy_cannot_do": [
                    "Pay for repatriation costs",
                    "Intervene in Syariah court proceedings for Muslim deceased",
                    "Make funeral arrangements"
                ]
            },
            "step_4_embalming": {
                "title": "Embalming in Malaysia",
                "required_for_repatriation": True,
                "details": "Embalming is required for international repatriation. Certified embalming services are available in Kuala Lumpur, Penang, and Johor Bahru. Services in East Malaysia (Kota Kinabalu, Kuching) are more limited. Note: embalming is generally not permitted for Muslim deceased, which means Muslim families may need to pursue alternative repatriation arrangements.",
                "typical_cost_gbp": "GBP 300-600"
            },
            "step_5_coffin": {
                "title": "Zinc-Lined Coffin Requirement",
                "zinc_lined_required": True,
                "details": "A zinc-lined or hermetically sealed coffin is required. Available through international funeral directors in Kuala Lumpur and Penang.",
                "typical_cost_gbp": "GBP 450-900"
            },
            "step_6_documentation": {
                "title": "Repatriation Documentation",
                "processing_time": "3-7 working days",
                "documents_needed": [
                    "Sijil Kematian (Malaysian death certificate)",
                    "Police clearance (if unnatural death)",
                    "Embalming certificate",
                    "Freedom from infection certificate",
                    "Export permit for human remains from the National Registration Department",
                    "Passport of deceased"
                ]
            },
            "step_7_transport": {
                "title": "Air Freight to the UK",
                "typical_freight_cost_gbp": "GBP 1,200-3,000",
                "flight_time": "13-14 hours direct",
                "main_airlines_with_cargo": ["Malaysia Airlines cargo", "British Airways", "AirAsia X"],
                "main_routes_to_uk": ["Kuala Lumpur KLIA (KUL) to London Heathrow (LHR)", "Kuala Lumpur KLIA (KUL) to Manchester (MAN)"]
            },
            "step_8_uk_reception": {
                "title": "Reception in the UK",
                "uk_airport_reception": ["London Heathrow", "Manchester"],
                "coroner_involvement": "The UK coroner is notified on arrival. Certified cause of death from Malaysian authorities should be provided. Deaths from natural causes are unlikely to require further UK inquest."
            }
        },
        "post_mortem": {
            "when_required": "Required for any sudden, unnatural, or unexplained death. Government pathologist post-mortems are performed at Hospital Kuala Lumpur and major regional hospitals. For Muslim deceased, Islamic post-mortem procedures apply and the Syariah court may be involved.",
            "impact_on_timeline": "Adds 5-14 days. Island and remote area logistics add further time for domestic transfer to a main city before international documentation can be processed."
        },
        "embassy_contacts": {
            "british_embassy": {
                "city": "Kuala Lumpur",
                "phone": "+60 3 2170 2200",
                "emergency_phone_fcdo": "+44 (0)20 7008 5000",
                "website": "https://www.gov.uk/world/organisations/british-high-commission-kuala-lumpur"
            }
        },
        "ashes_transport": {
            "cremation_available": True,
            "notes": "Cremation is available for non-Muslim deceased. Malaysia has modern cremation facilities in KL and Penang. Ashes can be carried as hand luggage on flights to the UK with a cremation certificate. Note: cremation is not permitted for Muslim deceased under Islamic law."
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Malaysia to the UK take?",
                "How much does it cost to repatriate a body from Malaysia to the UK?",
                "What happens if a Muslim British national dies in Malaysia?",
                "Can I bring cremated ashes from Malaysia to the UK on a plane?",
                "What documents are needed to bring a body home from Malaysia?"
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
