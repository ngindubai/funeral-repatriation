"""Add Batch 3 countries to countries_repatriation.json: Bulgaria, Cuba, Barbados, Tanzania, Nigeria"""
import json, pathlib

DATA_FILE = pathlib.Path(__file__).parent.parent / "site" / "data" / "countries_repatriation.json"

NEW_COUNTRIES = {
    "bulgaria": {
        "name": "Bulgaria",
        "slug": "bulgaria",
        "region": "Europe",
        "flag": "🇧🇬",
        "currency": "BGN",
        "language": "Bulgarian",
        "religion": "Eastern Orthodox Christianity",
        "typical_timeline": "10-21 days",
        "cost_guide": {
            "min": 3500,
            "max": 7000,
            "currency": "GBP",
            "notes": "Bulgaria is a relatively affordable European destination for repatriation. Direct charter flights and the short distance to the UK keep air freight costs lower than Asia or the Caribbean. Embalming is mandatory for international repatriation.",
            "source": "FCDO guidance; Bulgarian Ministry of Health burial regulations"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Register the death",
                    "details": "Death must be registered at the local Bulgarian municipality (obshtina) where the death occurred. A Bulgarian death certificate (Akta za smartta) is issued. For unnatural or suspicious deaths, the Regional Prosecutor's Office must authorise release of the body.",
                    "source": "Bulgarian Civil Registration Act; FCDO guidance on death in Bulgaria"
                },
                {
                    "step": 2,
                    "title": "Notify the British Embassy Sofia",
                    "details": "The British Embassy in Sofia must be notified. Consular staff will issue a Notice to a Coroner (if required) and advise on Bulgarian documentation requirements. A UK death registration will need to occur on return.",
                    "source": "gov.uk/government/world/organisations/british-embassy-sofia"
                },
                {
                    "step": 3,
                    "title": "Obtain a post-mortem if required",
                    "details": "Bulgarian law requires a post-mortem for any sudden, unexplained or violent death. The autopsy is conducted by the Regional Forensic Medicine Institute. Results must be received before the body is released for repatriation.",
                    "source": "Bulgarian Forensic Medicine Regulation"
                },
                {
                    "step": 4,
                    "title": "Embalming",
                    "details": "Embalming is mandatory for international repatriation from Bulgaria. Must be carried out by a licensed Bulgarian funeral director.",
                    "source": "Bulgarian Health Act, Ordinance 2 on funeral activities"
                },
                {
                    "step": 5,
                    "title": "Obtain a Certificate of Freedom from Contagious Disease",
                    "details": "Issued by the Regional Health Inspectorate (RZI). Required for all international repatriations.",
                    "source": "Bulgarian Ministry of Health"
                },
                {
                    "step": 6,
                    "title": "Secure a laissez-passer (transit permit)",
                    "details": "The laissez-passer is issued by the Bulgarian Ministry of Foreign Affairs or via the local municipality. It is required for transportation of human remains across international borders.",
                    "source": "Council of Europe Agreement on the Transfer of Corpses (Strasbourg 1973)"
                },
                {
                    "step": 7,
                    "title": "Arrange air freight",
                    "details": "Sofia Airport (SOF) is the main hub. Direct flights to London Heathrow operate with several carriers. Human remains must be transported in a hermetically sealed zinc-lined coffin, as standard in EU regulations.",
                    "source": "IATA regulations; EU Council of Europe Agreement"
                },
                {
                    "step": 8,
                    "title": "UK customs and final arrangements",
                    "details": "On arrival at a UK airport, the Registrar or Coroner must be notified. All Bulgarian documentation should be translated. The UK funeral director collects the body from the cargo facility.",
                    "source": "UK Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Mandatory for sudden, unexplained, violent or suspicious deaths. Conducted by the Regional Forensic Medicine Institute. Delays of 5-10 days are common in peak summer season.",
            "source": "Bulgarian forensic medicine regulations"
        },
        "embassy_contacts": {
            "name": "British Embassy Sofia",
            "address": "9 Moskovska Street, Sofia 1000, Bulgaria",
            "phone": "+359 2 933 9222",
            "emergency_phone": "+359 2 933 9222",
            "email": "britishembassy.sofia@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-embassy-sofia",
            "type": "embassy"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Bulgarian cremation certificate",
                "Death certificate (translated)",
                "Certificate of freedom from contagious disease",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "Most airlines accept ashes as carry-on in the cabin. Declare at check-in. X-ray screening applies.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Bulgaria to the UK take?",
                "How much does it cost to repatriate a body from Bulgaria to the UK?",
                "What documents are needed to bring a body home from Bulgaria?",
                "Can I bring cremated ashes from Bulgaria to the UK on a plane?",
                "Does Bulgaria require embalming for repatriation?"
            ]
        }
    },
    "cuba": {
        "name": "Cuba",
        "slug": "cuba",
        "region": "Caribbean",
        "flag": "🇨🇺",
        "currency": "CUP",
        "language": "Spanish",
        "religion": "Roman Catholic / Santeria",
        "typical_timeline": "21-35 days",
        "cost_guide": {
            "min": 6000,
            "max": 12000,
            "currency": "GBP",
            "notes": "Cuba is one of the most complex Caribbean destinations for repatriation. The US embargo restricts flight routes, meaning most repatriations route via Madrid, Cancun or Toronto, adding cost and time. Cuban state bureaucracy adds significant delay.",
            "source": "FCDO guidance on death in Cuba; British Embassy Havana"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Report the death to Cuban authorities",
                    "details": "Deaths must be reported to the Registro Civil (Civil Registry) and, for unnatural deaths, to the Cuban National Police (PNR). A medical death certificate (Certificado de Defuncion) is issued by the attending physician or forensic doctor.",
                    "source": "Cuban Civil Registry Law; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Notify the British Embassy Havana",
                    "details": "The British Embassy in Havana must be notified immediately. Consular staff will assist with documentation, liaise with Cuban authorities, and advise on routing. Cuba's relationship with the US means air routes are limited.",
                    "source": "gov.uk/government/world/organisations/british-embassy-havana"
                },
                {
                    "step": 3,
                    "title": "Cuban autopsy",
                    "details": "Autopsies are routinely performed by Cuban forensic authorities (Medicina Legal) for all foreign nationals. This is a state requirement and cannot be waived. Results take 7-14 days.",
                    "source": "Cuban Ministry of Public Health (MINSAP)"
                },
                {
                    "step": 4,
                    "title": "Embalming and preparation",
                    "details": "Embalming must be carried out by a Cuban state funeral service (Empresa de Servicios Funerarios). Private funeral homes operate only in a limited capacity. The state monopoly on funeral services means choice is restricted.",
                    "source": "Cuban funeral services regulation"
                },
                {
                    "step": 5,
                    "title": "Obtain export documentation",
                    "details": "Export documentation is issued by the Cuban Ministry of Foreign Affairs (MINREX) and includes the laissez-passer, embalming certificate, and sanitary clearance. This process typically takes 10-20 days.",
                    "source": "MINREX export procedures"
                },
                {
                    "step": 6,
                    "title": "Arrange routing",
                    "details": "No direct Cuba-UK flights exist. Most repatriations route via Havana to Madrid (Iberia) or via Cancun/Toronto. Each transit point adds documentation requirements. The UK repatriation specialist must coordinate transit handling.",
                    "source": "IATA routing data; British Embassy Havana"
                },
                {
                    "step": 7,
                    "title": "UK arrival and customs",
                    "details": "The body arrives as air freight. UK Customs and the coroner in the receiving district must be notified in advance. All Spanish-language documentation must be translated.",
                    "source": "FCDO death abroad guidance"
                },
                {
                    "step": 8,
                    "title": "UK funeral arrangements",
                    "details": "The UK funeral director collects the body from the cargo facility. A UK death registration is required if the death is to be formally registered in England, Wales, or Scotland.",
                    "source": "Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_all_foreign_nationals",
            "details": "Cuba's state forensic authority (Medicina Legal) conducts autopsies on all foreign nationals regardless of cause of death. This is a non-negotiable requirement. Delay of 7-14 days is standard.",
            "source": "Cuban Ministry of Public Health"
        },
        "embassy_contacts": {
            "name": "British Embassy Havana",
            "address": "Calle 34 No. 702, Entre 7ma y 17, Miramar, Havana, Cuba",
            "phone": "+53 7 214 2200",
            "emergency_phone": "+53 7 214 2200",
            "email": "britishembassy.havana@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-embassy-havana",
            "type": "embassy"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Cuban cremation certificate",
                "Death certificate (translated)",
                "Sanitary clearance certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "No direct Cuba-UK flights. Ashes must transit via Madrid, Cancun or Toronto. Transit country rules also apply. Check with each airline.",
            "source": "FCDO guidance; British Embassy Havana"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Cuba to the UK take?",
                "How much does it cost to repatriate a body from Cuba?",
                "What are the biggest delays in Cuban repatriation?",
                "Are there direct flights from Cuba to the UK for repatriation?",
                "Does Cuba require an autopsy on foreign nationals?"
            ]
        }
    },
    "barbados": {
        "name": "Barbados",
        "slug": "barbados",
        "region": "Caribbean",
        "flag": "🇧🇧",
        "currency": "BBD",
        "language": "English",
        "religion": "Protestant Christianity",
        "typical_timeline": "10-18 days",
        "cost_guide": {
            "min": 5000,
            "max": 9000,
            "currency": "GBP",
            "notes": "Barbados is English-speaking and Commonwealth, which simplifies the documentation process. Direct flights to London Gatwick and Heathrow operate with British Airways and Virgin Atlantic, which keeps air freight costs competitive for the Caribbean region.",
            "source": "FCDO guidance on death in Barbados; British High Commission Bridgetown"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Register the death",
                    "details": "Deaths must be registered at the Registration Office (part of the Barbados Registration Department). A Barbados death certificate is issued. For suspicious or sudden deaths, the Royal Barbados Police Force (RBPF) is involved and the Coroner's court may be convened.",
                    "source": "Barbados Registration Act Cap. 192; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Notify the British High Commission Bridgetown",
                    "details": "The British High Commission in Bridgetown serves Barbados and several other Eastern Caribbean islands. Consular staff will issue relevant UK documentation and advise on the process.",
                    "source": "gov.uk/world/organisations/british-high-commission-bridgetown"
                },
                {
                    "step": 3,
                    "title": "Post-mortem examination",
                    "details": "The Coroner orders a post-mortem for unnatural, sudden or suspicious deaths. The Queen Elizabeth Hospital in Bridgetown has pathology services. Results typically take 5-10 days.",
                    "source": "Barbados Coroners Act; FCDO guidance"
                },
                {
                    "step": 4,
                    "title": "Embalming",
                    "details": "Embalming is required for international repatriation from Barbados. The island has a good standard of licensed funeral directors with experience in handling UK repatriations.",
                    "source": "Barbados Funeral Directors and Embalmers Act"
                },
                {
                    "step": 5,
                    "title": "Obtain export documentation",
                    "details": "Export paperwork is issued by the Chief Medical Officer and includes an embalming certificate, freedom from infectious disease certificate, and transit permit.",
                    "source": "Barbados Ministry of Health"
                },
                {
                    "step": 6,
                    "title": "Book air freight",
                    "details": "British Airways operates direct flights Bridgetown (BGI) to London Gatwick and Heathrow. Virgin Atlantic also serves this route. Human remains travel as air cargo in a sealed zinc-lined coffin.",
                    "source": "IATA cargo regulations"
                },
                {
                    "step": 7,
                    "title": "UK arrival and customs",
                    "details": "Human remains arrive as air cargo. The UK funeral director collects from the cargo facility. All documentation should be reviewed by the local UK coroner if required.",
                    "source": "FCDO death abroad guidance"
                },
                {
                    "step": 8,
                    "title": "UK funeral arrangements",
                    "details": "A formal UK death registration is not automatic; the family must apply to the Registration Office if required. The UK funeral director handles collection from the cargo facility.",
                    "source": "Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Required for sudden, unexplained or violent deaths. Queen Elizabeth Hospital pathology services. Results typically available in 5-10 days.",
            "source": "Barbados Coroners Act"
        },
        "embassy_contacts": {
            "name": "British High Commission Bridgetown",
            "address": "Lower Collymore Rock, Bridgetown, St Michael BB11115, Barbados",
            "phone": "+1 246 430 7800",
            "emergency_phone": "+1 246 430 7800",
            "email": "bridgetown.consular@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-high-commission-bridgetown",
            "type": "high_commission"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Barbados cremation certificate",
                "Death certificate",
                "Freedom from infectious disease certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "Direct flights to Gatwick and Heathrow. Most airlines accept ashes as carry-on. Declare at check-in. X-ray screening applies.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Barbados to the UK take?",
                "How much does it cost to bring a body home from Barbados?",
                "Which airlines fly from Barbados to the UK for repatriation?",
                "Can I bring cremated ashes from Barbados on a plane?",
                "Does Barbados require embalming for international repatriation?"
            ]
        }
    },
    "tanzania": {
        "name": "Tanzania",
        "slug": "tanzania",
        "region": "Africa",
        "flag": "🇹🇿",
        "currency": "TZS",
        "language": "Swahili, English",
        "religion": "Islam / Christianity",
        "typical_timeline": "14-28 days",
        "cost_guide": {
            "min": 6000,
            "max": 11000,
            "currency": "GBP",
            "notes": "Tanzania is a popular safari and beach (Zanzibar) destination. Repatriation from Dar es Salaam is more straightforward than from Zanzibar, which adds an island-to-mainland transfer step. Safari deaths in remote national park locations (Serengeti, Ngorongoro) add significant internal logistics costs.",
            "source": "FCDO guidance on death in Tanzania; British High Commission Dar es Salaam"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Report the death to Tanzanian authorities",
                    "details": "Deaths must be reported to the Registration, Insolvency and Trusteeship Agency (RITA) for civil registration. For violent, sudden or unexplained deaths, the Tanzania Police Force and Government Chemist Laboratory Agency (GCLA) are involved.",
                    "source": "Tanzania Registration of Births and Deaths Act; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Notify the British High Commission",
                    "details": "The British High Commission in Dar es Salaam covers mainland Tanzania. For deaths in Zanzibar, a separate consular contact exists. Consular staff will guide on documentation and liaise with Tanzanian authorities.",
                    "source": "gov.uk/world/organisations/british-high-commission-tanzania"
                },
                {
                    "step": 3,
                    "title": "Post-mortem examination",
                    "details": "Required for all violent, sudden or suspicious deaths. Conducted by the Government Chemist Laboratory Agency (GCLA). For deaths in remote safari areas, the body must first be transported to the nearest GCLA-approved facility, which can take several days.",
                    "source": "Tanzanian Criminal Procedure Act; GCLA regulations"
                },
                {
                    "step": 4,
                    "title": "Embalming and preparation",
                    "details": "Embalming is required for international repatriation. In Dar es Salaam, licensed funeral directors with international experience are available. Zanzibar Island has more limited facilities. Safari deaths may require local preparation before transfer to Dar.",
                    "source": "Tanzanian health regulations; FCDO guidance"
                },
                {
                    "step": 5,
                    "title": "Obtain export documentation",
                    "details": "Export documentation is issued by the Ministry of Health and includes an embalming certificate, freedom from infectious disease clearance, and transit permit. The Ministry of Foreign Affairs issues the laissez-passer.",
                    "source": "Tanzanian Ministry of Health; Ministry of Foreign Affairs"
                },
                {
                    "step": 6,
                    "title": "Arrange air freight",
                    "details": "Julius Nyerere International Airport (DAR) is the main cargo hub. No direct Tanzania-UK flights for cargo. Most repatriations route via Nairobi (NBO) or Addis Ababa (ADD) with Kenya Airways, Ethiopian Airlines, or British Airways via Nairobi. Zanzibar repatriations require a domestic flight or ferry to Dar first.",
                    "source": "IATA routing data"
                },
                {
                    "step": 7,
                    "title": "UK arrival and customs",
                    "details": "Human remains arrive as air freight. All documentation must be translated into English (Swahili documents). The UK coroner or registrar may need to be notified in advance.",
                    "source": "FCDO death abroad guidance"
                },
                {
                    "step": 8,
                    "title": "UK funeral arrangements",
                    "details": "The UK funeral director collects from the cargo facility. A UK death registration can be applied for through the General Register Office.",
                    "source": "Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Required for violent, sudden or suspicious deaths. Conducted by GCLA. Remote safari deaths add significant internal transport time before a post-mortem can begin. Allow 7-14 days from the point the body reaches a GCLA facility.",
            "source": "Tanzania Criminal Procedure Act; GCLA"
        },
        "embassy_contacts": {
            "name": "British High Commission Dar es Salaam",
            "address": "Umoja House, Hamburg Avenue, Dar es Salaam, Tanzania",
            "phone": "+255 22 229 0000",
            "emergency_phone": "+255 22 229 0000",
            "email": "britishhighcommission.daressalaam@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-high-commission-tanzania",
            "type": "high_commission"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Tanzanian cremation certificate",
                "Death certificate",
                "Freedom from infectious disease certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "No direct Tanzania-UK flights. Ashes transit via Nairobi or Addis Ababa. Transit country rules may apply. Declare ashes to each airline.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Tanzania to the UK take?",
                "How much does it cost to bring a body home from Tanzania?",
                "What happens if someone dies on safari in Tanzania?",
                "How do you repatriate a body from Zanzibar to the UK?",
                "Does Tanzania require a post-mortem for British nationals?"
            ]
        }
    },
    "nigeria": {
        "name": "Nigeria",
        "slug": "nigeria",
        "region": "Africa",
        "flag": "🇳🇬",
        "currency": "NGN",
        "language": "English",
        "religion": "Islam / Christianity",
        "typical_timeline": "14-35 days",
        "cost_guide": {
            "min": 5500,
            "max": 10000,
            "currency": "GBP",
            "notes": "Nigeria is one of the most common African origins for repatriation to the UK due to the large Nigerian diaspora. Lagos (LOS) and Abuja (ABV) are the main departure points. Documentation delays, particularly for the State Government death certificate and export permit, are the primary cause of extended timelines. Direct flights to London Heathrow with British Airways and Virgin Atlantic reduce air freight costs.",
            "source": "FCDO guidance on death in Nigeria; British High Commission Abuja"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Report the death and obtain a medical certificate",
                    "details": "A medical certificate of cause of death is issued by the attending physician or hospital. For deaths outside a hospital, the police must be notified and a coroner's inquest may be required. In Lagos, the Lagos State Health Management Authority oversees death certification.",
                    "source": "Nigerian Births, Deaths etc. (Compulsory Registration) Act 2004; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Obtain the National Population Commission death certificate",
                    "details": "The official Nigerian death certificate is issued by the National Population Commission (NPC). This is separate from the hospital medical certificate and can take 5-14 days to obtain. It is the legally recognised death certificate for international purposes.",
                    "source": "National Population Commission Act; NPC registration guidelines"
                },
                {
                    "step": 3,
                    "title": "Notify the British High Commission Abuja",
                    "details": "The British High Commission in Abuja is the main consular contact for Nigeria. A Deputy High Commission operates in Lagos. Consular staff will advise on documentation requirements and can assist if there are difficulties with Nigerian authorities.",
                    "source": "gov.uk/world/organisations/british-high-commission-abuja"
                },
                {
                    "step": 4,
                    "title": "Post-mortem examination",
                    "details": "A post-mortem is required for violent, sudden, unexplained or suspicious deaths, conducted by a government pathologist. Forensic pathology capacity is concentrated in Lagos and Abuja; deaths in other states face longer delays due to limited capacity.",
                    "source": "Nigerian Coroners Law; FCDO guidance"
                },
                {
                    "step": 5,
                    "title": "Embalming",
                    "details": "Embalming is mandatory for international repatriation from Nigeria. Lagos and Abuja have licensed funeral directors with international repatriation experience. Other states have more limited provision.",
                    "source": "Nigerian funeral practice guidelines"
                },
                {
                    "step": 6,
                    "title": "Obtain State Ministry of Health export permit",
                    "details": "The State Ministry of Health issues an export permit for the body. This is separate from the NPC death certificate and requires the embalming certificate, freedom from infectious disease clearance, and a copy of the NPC death certificate. Allow 7-14 days.",
                    "source": "State Ministry of Health regulations (Lagos, Abuja)"
                },
                {
                    "step": 7,
                    "title": "Arrange air freight",
                    "details": "British Airways operates direct Lagos (LOS) to London Heathrow flights with cargo capacity. Virgin Atlantic also serves Lagos-Heathrow direct. Abuja (ABV) has fewer direct cargo options; many repatriations transit Lagos. Human remains must be in a hermetically sealed zinc-lined coffin.",
                    "source": "IATA cargo regulations"
                },
                {
                    "step": 8,
                    "title": "UK arrival and customs",
                    "details": "Human remains arrive as air freight at Heathrow or Gatwick. The UK funeral director collects from the cargo terminal. A coroner's notification may be required. UK death registration can be applied for via the General Register Office.",
                    "source": "FCDO death abroad guidance; Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Required for sudden, violent or suspicious deaths. Government pathologist required. Significant capacity gaps outside Lagos and Abuja mean delays of 10-21 days are possible in other states.",
            "source": "Nigerian Coroners Law"
        },
        "embassy_contacts": {
            "name": "British High Commission Abuja",
            "address": "Dangote House, Aguiyi Ironsi Street, Maitama, Abuja, Nigeria",
            "phone": "+234 9 462 2200",
            "emergency_phone": "+234 9 462 2200",
            "email": "nigeria.consular@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-high-commission-abuja",
            "type": "high_commission"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Nigerian cremation certificate",
                "NPC death certificate",
                "Freedom from infectious disease certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "Direct flights Lagos-Heathrow with British Airways and Virgin Atlantic. Most airlines accept ashes as carry-on. Declare at check-in.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Nigeria to the UK take?",
                "How much does it cost to bring a body home from Nigeria?",
                "What is the National Population Commission death certificate in Nigeria?",
                "Which airlines repatriate bodies from Lagos to London?",
                "What are the biggest delays in repatriation from Nigeria?"
            ]
        }
    }
}

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

# Add country data
for key, value in NEW_COUNTRIES.items():
    data["countries"][key] = value

DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Done. Total countries: {len(data['countries'])}")
