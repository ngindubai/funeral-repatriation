"""Add Batch 4 countries to countries_repatriation.json: Peru, Pakistan, Poland, Czech Republic, Hungary"""
import json, pathlib

DATA_FILE = pathlib.Path(__file__).parent.parent / "site" / "data" / "countries_repatriation.json"

NEW_COUNTRIES = {
    "peru": {
        "name": "Peru",
        "slug": "peru",
        "region": "South America",
        "flag": "🇵🇪",
        "currency": "PEN",
        "language": "Spanish",
        "religion": "Roman Catholic",
        "typical_timeline": {
            "fastest_case": "14 days",
            "average_case": "18-25 days",
            "complex_case": "35+ days",
            "complexity_factors": [
                "Post-mortem required (adds 7-14 days)",
                "Deaths in remote Andean or Amazon regions (significant internal logistics)",
                "Machu Picchu/Cusco deaths require transfer to Lima",
                "Weekend or Peruvian public holiday closures",
                "SERNANP clearance for national park/reserve deaths"
            ]
        },
        "cost_guide": {
            "min": 5500,
            "max": 10000,
            "currency": "GBP",
            "notes": "No direct Peru-UK flights. Most repatriations route via Madrid (Iberia) or via Miami/Bogota. Lima (LIM) is the main cargo hub. Remote Andean or Amazon deaths add significant internal transport costs. Altitude deaths (Cusco, Machu Picchu area) are common.",
            "source": "FCDO guidance on death in Peru; British Embassy Lima"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Register the death with Peruvian RENIEC",
                    "details": "Deaths must be registered with RENIEC (Registro Nacional de Identificacion y Estado Civil). The Acta de Defuncion (death certificate) is issued. For deaths outside Lima, local municipal offices handle registration. Deaths in remote areas may require significant travel to reach the nearest office.",
                    "source": "RENIEC regulations; FCDO guidance on death in Peru"
                },
                {
                    "step": 2,
                    "title": "Notify the British Embassy Lima",
                    "details": "The British Embassy in Lima must be notified immediately. Consular staff will issue UK documentation and advise on Peruvian requirements. For deaths outside Lima (Cusco, remote areas), the Embassy coordinates remotely. An Honorary Consul in Cusco can assist with initial steps.",
                    "source": "gov.uk/world/organisations/british-embassy-peru"
                },
                {
                    "step": 3,
                    "title": "Post-mortem by the Institute of Legal Medicine",
                    "details": "The Instituto de Medicina Legal (IML) conducts post-mortems for violent, sudden or suspicious deaths. Lima has adequate capacity; regional cities have limited forensic infrastructure. Deaths at altitude (Cusco, Machu Picchu) often involve the IML office in Cusco.",
                    "source": "Peruvian Ministry of Justice; IML regulations"
                },
                {
                    "step": 4,
                    "title": "Embalming and preparation",
                    "details": "Embalming is required for international repatriation. Lima has licensed funeral directors with international experience. Cusco has limited provision. Remote deaths require transfer to Lima or the nearest city before embalming can be completed.",
                    "source": "Peruvian funeral regulations; FCDO guidance"
                },
                {
                    "step": 5,
                    "title": "Obtain export documentation",
                    "details": "The Ministry of Health issues the sanitary clearance and embalming certificate. The Ministry of Foreign Affairs (Cancilleria) issues the laissez-passer. All documents in Spanish require certified translation.",
                    "source": "Peruvian Ministry of Health; Cancilleria"
                },
                {
                    "step": 6,
                    "title": "Internal transfer to Lima if required",
                    "details": "Most international cargo flights depart from Jorge Chavez International Airport (LIM) in Lima. Deaths in Cusco, Arequipa, or Amazon regions require domestic flight or ground transport to Lima. Domestic flights from Cusco to Lima are available daily.",
                    "source": "IATA routing data"
                },
                {
                    "step": 7,
                    "title": "Air freight via Madrid or Miami",
                    "details": "Iberia operates Lima to Madrid (MAD) with connections to UK airports. Some routings go via Miami or Bogota. Human remains travel as air cargo in a sealed zinc-lined coffin. Transit country requirements apply.",
                    "source": "IATA cargo regulations"
                },
                {
                    "step": 8,
                    "title": "UK arrival and funeral arrangements",
                    "details": "The UK funeral director collects from the cargo terminal. All Spanish documents must be translated. A UK death registration can be applied for via the General Register Office.",
                    "source": "FCDO death abroad guidance; Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Conducted by the Instituto de Medicina Legal. Regional capacity is limited; allow 7-14 days. Altitude deaths at Machu Picchu or Cusco are common and involve the Cusco IML office.",
            "source": "Peruvian Ministry of Justice; IML"
        },
        "embassy_contacts": {
            "name": "British Embassy Lima",
            "address": "Torre Parque Mar, Piso 22, Avenida Jose Larco 1301, Miraflores, Lima 18, Peru",
            "phone": "+51 1 617 3000",
            "emergency_phone": "+51 1 617 3000",
            "email": "lima.consular@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-embassy-peru",
            "type": "embassy"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Peruvian cremation certificate",
                "RENIEC death certificate (translated)",
                "Sanitary clearance certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "No direct Peru-UK flights. Ashes transit via Madrid or Miami. Transit country rules apply. Declare ashes to each airline at check-in.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Peru to the UK take?",
                "How much does it cost to bring a body home from Peru?",
                "What happens if someone dies at Machu Picchu?",
                "What happens if someone dies in Cusco, Peru?",
                "Does Peru require a post-mortem for British nationals?"
            ]
        }
    },
    "pakistan": {
        "name": "Pakistan",
        "slug": "pakistan",
        "region": "Asia",
        "flag": "🇵🇰",
        "currency": "PKR",
        "language": "Urdu, English",
        "religion": "Islam",
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "10-21 days",
            "complex_case": "35+ days",
            "complexity_factors": [
                "Police investigation for violent or sudden deaths",
                "Medico-Legal Officer post-mortem (capacity varies by city)",
                "Documentation delays outside Karachi, Lahore, Islamabad",
                "Regional and district-level bureaucracy",
                "Islamic burial preference conflicts with repatriation timeline"
            ]
        },
        "cost_guide": {
            "min": 4000,
            "max": 8000,
            "currency": "GBP",
            "notes": "Pakistan has one of the highest volumes of repatriation to the UK due to the large Pakistani diaspora. Direct flights from Lahore, Karachi, and Islamabad to London Heathrow (PIA, British Airways) keep air freight costs competitive. Documentation is the main delay factor, not flight availability.",
            "source": "FCDO guidance on death in Pakistan; British High Commission Islamabad"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Obtain the medical death certificate",
                    "details": "A medical death certificate is issued by the attending physician or hospital. For unnatural, sudden or suspicious deaths, the local police are notified and the body is referred to the Medico-Legal Officer (MLO) for examination.",
                    "source": "Pakistani Registration of Births, Deaths and Marriages Act; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Union Council death certificate",
                    "details": "The official death certificate for international purposes is issued by the Union Council (local government). This is a separate document from the hospital medical certificate. Processing time varies: 3-7 days in cities, longer in rural areas.",
                    "source": "Pakistani local government registration system"
                },
                {
                    "step": 3,
                    "title": "Notify the British High Commission Islamabad",
                    "details": "The British High Commission in Islamabad is the main consular contact. Deputy High Commissions operate in Karachi and Lahore. Consular staff will issue UK documentation and advise on Pakistani requirements.",
                    "source": "gov.uk/world/organisations/british-high-commission-islamabad"
                },
                {
                    "step": 4,
                    "title": "Medico-Legal Officer examination if required",
                    "details": "For violent, sudden or suspicious deaths, the MLO conducts a post-mortem. MLO capacity is concentrated in Karachi, Lahore, and Islamabad. Deaths in smaller cities or rural areas may require transfer to the nearest MLO facility.",
                    "source": "Pakistani Medico-Legal system"
                },
                {
                    "step": 5,
                    "title": "Embalming",
                    "details": "Embalming is required for international repatriation. Note: Islamic tradition generally opposes embalming. Families should discuss this with their UK specialist. A number of Pakistani funeral directors are experienced in meeting both legal requirements and religious considerations.",
                    "source": "International repatriation requirements; Islamic funeral guidance"
                },
                {
                    "step": 6,
                    "title": "No Objection Certificate from the District Health Authority",
                    "details": "The District Health Authority issues a No Objection Certificate (NOC) for the export of human remains. This requires the death certificate, embalming certificate, and MLO clearance (where applicable).",
                    "source": "Pakistani District Health Authority procedures"
                },
                {
                    "step": 7,
                    "title": "Air freight from Karachi, Lahore or Islamabad",
                    "details": "Pakistan International Airlines (PIA) and British Airways operate direct flights from Lahore (LHE), Karachi (KHI), and Islamabad (ISB) to London Heathrow. Human remains travel as air cargo.",
                    "source": "IATA cargo regulations"
                },
                {
                    "step": 8,
                    "title": "UK arrival and funeral arrangements",
                    "details": "The UK funeral director collects from the Heathrow cargo terminal. A UK death registration can be applied for. Many Pakistani community funeral directors in the UK have dedicated repatriation receiving services.",
                    "source": "FCDO death abroad guidance"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Conducted by the Medico-Legal Officer. Capacity concentrated in Karachi, Lahore, Islamabad. Rural deaths face transfer delays. Islamic families should note embalming is legally required for international repatriation despite religious concerns.",
            "source": "Pakistani MLO system"
        },
        "embassy_contacts": {
            "name": "British High Commission Islamabad",
            "address": "Diplomatic Enclave, Ramna 5, Islamabad, Pakistan",
            "phone": "+92 51 201 2000",
            "emergency_phone": "+92 51 201 2000",
            "email": "islamabad.consular@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-high-commission-islamabad",
            "type": "high_commission"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Pakistani cremation certificate (cremation is rare given predominantly Muslim population)",
                "Death certificate",
                "District Health Authority NOC",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "Cremation is uncommon in Pakistan due to Islamic practice. For non-Muslim deceased, direct London flights available with PIA and British Airways. Declare ashes at check-in.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Pakistan to the UK take?",
                "How much does it cost to bring a body home from Pakistan?",
                "Does repatriation from Pakistan require embalming under Islamic law?",
                "Which airlines repatriate bodies from Pakistan to London?",
                "What is the Union Council death certificate in Pakistan?"
            ]
        }
    },
    "poland": {
        "name": "Poland",
        "slug": "poland",
        "region": "Europe",
        "flag": "🇵🇱",
        "currency": "PLN",
        "language": "Polish",
        "religion": "Roman Catholic",
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "10-14 days",
            "complex_case": "21+ days",
            "complexity_factors": [
                "Post-mortem ordered by the Prosecutor (adds 5-10 days)",
                "Documentation from smaller regional offices",
                "Weekend or Polish public holiday closures",
                "Trisagion/Catholic funeral customs may affect timing discussions with family"
            ]
        },
        "cost_guide": {
            "min": 3000,
            "max": 6500,
            "currency": "GBP",
            "notes": "Poland is one of the most affordable European repatriation origins. Multiple daily direct flights from Warsaw (WAW), Krakow (KRK), Gdansk (GDN), and other Polish cities to UK airports. Poland is an EU/Council of Europe member; the Strasbourg Agreement on transfer of corpses applies.",
            "source": "FCDO guidance on death in Poland; British Embassy Warsaw"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Register the death with the Polish USC",
                    "details": "Deaths are registered at the Urzad Stanu Cywilnego (USC — Civil Registry Office) in the district where the death occurred. An Akt Zgonu (death certificate) is issued. For unnatural deaths, the police and Prosecutor's Office are notified.",
                    "source": "Polish Civil Registry Act; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Notify the British Embassy Warsaw",
                    "details": "The British Embassy in Warsaw must be notified. Consular staff will issue UK documentation. Poland has British Consular presence in several cities for emergencies.",
                    "source": "gov.uk/world/organisations/british-embassy-warsaw"
                },
                {
                    "step": 3,
                    "title": "Prosecutor's Office authorisation for unnatural deaths",
                    "details": "For violent, sudden or suspicious deaths, the District Prosecutor's Office must authorise release of the body after any necessary forensic examination. Polish forensic medicine standards are high and results are typically available within 5-10 days.",
                    "source": "Polish Code of Criminal Procedure; forensic medicine regulations"
                },
                {
                    "step": 4,
                    "title": "Embalming",
                    "details": "Embalming is mandatory for international repatriation from Poland under the Strasbourg Agreement. Polish funeral directors are experienced with international repatriations to the UK given the size of the Polish community in Britain.",
                    "source": "Council of Europe Agreement on Transfer of Corpses ETS No. 080; Polish funeral regulations"
                },
                {
                    "step": 5,
                    "title": "Obtain the laissez-passer",
                    "details": "The laissez-passer is issued by the Voivode (regional governor's office) or via the local authorities. Combined with the Akt Zgonu, embalming certificate, and freedom from contagious disease certificate, this completes the export documentation.",
                    "source": "Polish Ministry of Interior; Strasbourg Agreement procedures"
                },
                {
                    "step": 6,
                    "title": "Air freight to the UK",
                    "details": "Multiple daily direct flights from Warsaw Chopin (WAW), Krakow (KRK), Gdansk (GDN), Wroclaw (WRO), Katowice (KTW) to UK airports. LOT Polish Airlines, Ryanair, Wizz Air and British Airways all serve Polish routes. Human remains travel as cargo.",
                    "source": "IATA cargo regulations"
                },
                {
                    "step": 7,
                    "title": "UK arrival and funeral arrangements",
                    "details": "The UK funeral director collects from the cargo terminal. Polish documentation should be translated. The large Polish community in the UK means many funeral directors have significant experience with Polish repatriations in both directions.",
                    "source": "FCDO death abroad guidance"
                },
                {
                    "step": 8,
                    "title": "UK death registration if required",
                    "details": "A UK death registration can be applied for via the General Register Office if the family wishes to formally register the death in England, Wales, or Scotland.",
                    "source": "Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Ordered by the District Prosecutor. Polish forensic medicine infrastructure is well-developed. Results typically available within 5-10 days. Warsaw and other major cities have faster turnaround than smaller regional offices.",
            "source": "Polish forensic medicine regulations"
        },
        "embassy_contacts": {
            "name": "British Embassy Warsaw",
            "address": "ul. Kawalerii 12, 00-468 Warsaw, Poland",
            "phone": "+48 22 311 0000",
            "emergency_phone": "+48 22 311 0000",
            "email": "consular.warsaw@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-embassy-warsaw",
            "type": "embassy"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Polish cremation certificate",
                "Akt Zgonu (death certificate, translated)",
                "Freedom from contagious disease certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "Multiple direct Poland-UK flights daily. Most airlines accept ashes as carry-on. Declare at check-in.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Poland to the UK take?",
                "How much does it cost to bring a body home from Poland?",
                "What documents are needed for repatriation from Poland to the UK?",
                "Can I bring cremated ashes from Poland on a plane to the UK?",
                "Which airports in Poland can repatriate bodies to the UK?"
            ]
        }
    },
    "czech-republic": {
        "name": "Czech Republic",
        "slug": "czech-republic",
        "region": "Europe",
        "flag": "🇨🇿",
        "currency": "CZK",
        "language": "Czech",
        "religion": "Secular / Roman Catholic minority",
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "10-14 days",
            "complex_case": "21+ days",
            "complexity_factors": [
                "State Prosecutor must authorise release for unnatural deaths",
                "Forensic institute post-mortem (adds 5-10 days)",
                "Czech bureaucratic documentation from smaller regional offices",
                "Weekend and public holiday closures"
            ]
        },
        "cost_guide": {
            "min": 3200,
            "max": 6500,
            "currency": "GBP",
            "notes": "The Czech Republic is a popular city break destination (Prague) and skiing destination (Giant Mountains). Direct flights from Prague to London are frequent. EU member and Strasbourg Agreement signatory. Czech Republic has well-developed funeral and forensic infrastructure.",
            "source": "FCDO guidance on death in Czech Republic; British Embassy Prague"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Register the death",
                    "details": "Deaths are registered at the local Matrika (registry office) in the district where the death occurred. A death certificate (Umrtni list) is issued. For unnatural deaths, the police and State Prosecutor are notified.",
                    "source": "Czech Civil Registry Act; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Notify the British Embassy Prague",
                    "details": "The British Embassy in Prague must be notified. Consular staff will issue UK documentation and advise on Czech procedures.",
                    "source": "gov.uk/world/organisations/british-embassy-prague"
                },
                {
                    "step": 3,
                    "title": "State Prosecutor authorisation",
                    "details": "For violent, sudden or suspicious deaths, the State Prosecutor must authorise the body's release. A forensic post-mortem is conducted by the Institute of Forensic Medicine. Prague's institute is well-staffed; regional centres may be slower.",
                    "source": "Czech Code of Criminal Procedure; forensic medicine regulations"
                },
                {
                    "step": 4,
                    "title": "Embalming",
                    "details": "Embalming is mandatory for international repatriation under the Strasbourg Agreement. Czech funeral directors are experienced and Prague-based firms regularly handle UK repatriations.",
                    "source": "Council of Europe Agreement ETS No. 080; Czech funeral Act"
                },
                {
                    "step": 5,
                    "title": "Obtain the laissez-passer and documentation",
                    "details": "The laissez-passer is issued by the Czech Ministry of Interior (or delegated regional authority). Combined with the death certificate, embalming certificate, and freedom from contagious disease clearance, this forms the export package.",
                    "source": "Czech Ministry of Interior; Strasbourg Agreement"
                },
                {
                    "step": 6,
                    "title": "Air freight from Prague",
                    "details": "Vaclav Havel Airport Prague (PRG) has direct flights to London Heathrow, Gatwick, Stansted, and other UK airports. British Airways, easyJet, and Ryanair serve this route. Human remains travel as air cargo.",
                    "source": "IATA cargo regulations"
                },
                {
                    "step": 7,
                    "title": "UK arrival and funeral arrangements",
                    "details": "The UK funeral director collects from the cargo terminal. Czech documentation must be translated. A UK death registration can be applied for if required.",
                    "source": "FCDO death abroad guidance"
                },
                {
                    "step": 8,
                    "title": "UK death registration",
                    "details": "Apply via the General Register Office if a formal UK death registration is required.",
                    "source": "Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Conducted by the Institute of Forensic Medicine under State Prosecutor authority. Prague has a well-resourced institute. Regional offices are adequate but slower.",
            "source": "Czech forensic medicine regulations"
        },
        "embassy_contacts": {
            "name": "British Embassy Prague",
            "address": "Thunovska 14, 118 00 Prague 1, Czech Republic",
            "phone": "+420 257 402 111",
            "emergency_phone": "+420 257 402 111",
            "email": "consular.prague@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-embassy-prague",
            "type": "embassy"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Czech cremation certificate",
                "Umrtni list (death certificate, translated)",
                "Freedom from contagious disease certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "Direct flights Prague to multiple UK airports. Most airlines accept ashes as carry-on. Declare at check-in.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Czech Republic to the UK take?",
                "How much does it cost to bring a body home from Prague?",
                "What documents are needed for repatriation from Czech Republic to the UK?",
                "Can I bring cremated ashes from Czech Republic to the UK?",
                "What happens if someone dies in Prague as a British tourist?"
            ]
        }
    },
    "hungary": {
        "name": "Hungary",
        "slug": "hungary",
        "region": "Europe",
        "flag": "🇭🇺",
        "currency": "HUF",
        "language": "Hungarian",
        "religion": "Roman Catholic / Protestant",
        "typical_timeline": {
            "fastest_case": "7 days",
            "average_case": "10-14 days",
            "complex_case": "21+ days",
            "complexity_factors": [
                "Public Prosecutor authorisation for unnatural deaths",
                "Forensic medicine post-mortem (adds 5-10 days)",
                "Hungarian-language documentation with translation requirement",
                "Weekend and Hungarian public holiday closures"
            ]
        },
        "cost_guide": {
            "min": 3200,
            "max": 6500,
            "currency": "GBP",
            "notes": "Hungary is primarily a city break destination (Budapest). Direct flights from Budapest to London are available. EU member and Strasbourg Agreement signatory. Hungarian bureaucratic procedures are well-established but require translation of all documentation.",
            "source": "FCDO guidance on death in Hungary; British Embassy Budapest"
        },
        "repatriation_process": {
            "steps": [
                {
                    "step": 1,
                    "title": "Register the death",
                    "details": "Deaths are registered at the local anyakonyvi hivatal (civil registry office). A halotti anyakonyvi kivonat (death certificate extract) is issued. For unnatural deaths, the police and Public Prosecutor are notified.",
                    "source": "Hungarian Civil Registry Act; FCDO guidance"
                },
                {
                    "step": 2,
                    "title": "Notify the British Embassy Budapest",
                    "details": "The British Embassy in Budapest must be notified immediately. Consular staff will issue UK documentation and advise on Hungarian procedures.",
                    "source": "gov.uk/world/organisations/british-embassy-budapest"
                },
                {
                    "step": 3,
                    "title": "Public Prosecutor authorisation",
                    "details": "For violent, sudden or suspicious deaths, the Public Prosecutor authorises the body's release after forensic examination. The National Institute of Forensic Medicine in Budapest (ORVOSI) conducts post-mortems. Results typically available within 5-10 days.",
                    "source": "Hungarian Code of Criminal Procedure; forensic medicine Act"
                },
                {
                    "step": 4,
                    "title": "Embalming",
                    "details": "Embalming is mandatory for international repatriation under the Strasbourg Agreement. Hungarian funeral directors in Budapest are experienced with international repatriations.",
                    "source": "Council of Europe Agreement ETS No. 080; Hungarian funeral regulations"
                },
                {
                    "step": 5,
                    "title": "Obtain the laissez-passer and export documentation",
                    "details": "The laissez-passer is issued by the Government Office (Kormanyablak) or competent district authority. Combined with the death certificate, embalming certificate, and freedom from contagious disease clearance, this forms the export package. All documents are in Hungarian and require certified translation.",
                    "source": "Hungarian Government Office procedures"
                },
                {
                    "step": 6,
                    "title": "Air freight from Budapest",
                    "details": "Budapest Ferenc Liszt International Airport (BUD) has direct flights to London Heathrow, Gatwick, Luton, and Stansted with British Airways, easyJet, Ryanair, and Wizz Air. Human remains travel as air cargo.",
                    "source": "IATA cargo regulations"
                },
                {
                    "step": 7,
                    "title": "UK arrival and funeral arrangements",
                    "details": "The UK funeral director collects from the cargo terminal. All Hungarian documentation must be translated. A UK death registration can be applied for if required.",
                    "source": "FCDO death abroad guidance"
                },
                {
                    "step": 8,
                    "title": "UK death registration",
                    "details": "Apply via the General Register Office if a formal UK death registration is required.",
                    "source": "Registration of Deaths (Deaths Abroad) Regulations"
                }
            ]
        },
        "post_mortem": {
            "required": "mandatory_for_unnatural_deaths",
            "details": "Conducted by the National Institute of Forensic Medicine under Public Prosecutor authority. Budapest has a well-resourced institute. Regional capacity is adequate.",
            "source": "Hungarian forensic medicine Act"
        },
        "embassy_contacts": {
            "name": "British Embassy Budapest",
            "address": "Harmincad Utca 6, Budapest 1051, Hungary",
            "phone": "+36 1 266 2888",
            "emergency_phone": "+36 1 266 2888",
            "email": "consular.budapest@fco.gov.uk",
            "website": "https://www.gov.uk/world/organisations/british-embassy-budapest",
            "type": "embassy"
        },
        "ashes_transport": {
            "allowed": True,
            "requirements": [
                "Hungarian cremation certificate",
                "Halotti anyakonyvi kivonat (death certificate, translated)",
                "Freedom from contagious disease certificate",
                "Ashes in a sealed, clearly labelled container"
            ],
            "airline_notes": "Direct flights Budapest to multiple UK airports. Most airlines accept ashes as carry-on. Declare at check-in.",
            "source": "FCDO guidance; IATA regulations"
        },
        "content_angles": {
            "faq_angles": [
                "How long does repatriation from Hungary to the UK take?",
                "How much does it cost to bring a body home from Hungary?",
                "What documents are needed for repatriation from Hungary to the UK?",
                "What happens if someone dies in Budapest as a British tourist?",
                "Can I bring cremated ashes from Hungary to the UK?"
            ]
        }
    }
}

data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

for key, value in NEW_COUNTRIES.items():
    data["countries"][key] = value

DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Done. Total countries: {len(data['countries'])}")
