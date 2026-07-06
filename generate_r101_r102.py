#!/usr/bin/env python3
"""
generate_r101_r102.py -- Repatriate Service Route Generator
Chunks R101 and R102: 50 Tier C route pages, introducing ten new destinations
not previously covered anywhere in the route matrix.
R101: Saint Kitts and Nevis x5, Saint Vincent and the Grenadines x5, Dominica x5,
      Suriname x5, Cabo Verde x5
R102: Seychelles x5, Bahamas x5, Antigua and Barbuda x5, Saint Lucia x5, Grenada x5
Origins: Australia, France, Canada, Netherlands, Italy, Norway, Sweden, Belgium
(established Tier C origin pool, reused verbatim from generate_r97_r98.py).
Template variants: both chunks start at C (index 2), continuing rotation from R100
(ended on C, canada-to-liechtenstein).
Sources for new destination facts: HCCH Apostille status table (hcch.net, checked
July 2026), GOV.UK "British Embassy/High Commission" world-organisation pages and
GOV.UK bereavement guidance pages (gov.uk/guidance/when-someone-dies-in-..., all
checked July 2026), national civil registry sites (CBB Suriname, DGRNI Cabo Verde,
Registry Department Dominica, Registrar General St Kitts and Nevis and St Vincent
and the Grenadines).
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r97_r98.py / generate_r99_r100.py)
# ---------------------------------------------------------------------------

ORIGIN_DATA = {
    "australia": {
        "name": "Australia",
        "slug": "australia",
        "airport": "Sydney (SYD), Melbourne (MEL), Brisbane (BNE), Perth (PER), or other major Australian airport",
        "emergency": "000 (police, fire, ambulance)",
        "death_cert": "death certificate (state or territory Births, Deaths and Marriages registry)",
        "registry": "state or territory Births, Deaths and Marriages (BDM) registry",
        "language": "English",
        "apostille": True,
        "apostille_year": "1995",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Canberra",
        "embassy_note": "The British High Commission in Canberra can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 000 for emergency services. Death is certified by a registered medical practitioner and registered with the state or territory Births, Deaths and Marriages (BDM) registry. The coroner takes jurisdiction for sudden, violent, or unexplained deaths. Australia is a Hague Apostille Convention member since 1995. Death certificates are issued in English. The British High Commission in Canberra can assist British nationals. (DFAT Smartraveller Australia 2025; FCDO Travel Advice Australia 2025.)",
        "police_note": "The coroner takes jurisdiction for sudden, violent, or unexplained deaths. Body release may be delayed until the coroner authorises it.",
        "source": "DFAT Smartraveller Australia 2025; state BDM registry procedures 2025; Hague Conference Australia profile 1995",
        "translation_note": "Death certificates are issued in English. No translation is required for English-speaking destinations. Certified translation may be required for non-English-speaking destinations.",
    },
    "france": {
        "name": "France",
        "slug": "france",
        "airport": "Paris Charles de Gaulle (CDG), Paris Orly (ORY), Lyon Saint-Exupery (LYS), or other major French airport",
        "emergency": "15 (SAMU medical), 17 (police), 18 (fire), 112 (Europe-wide)",
        "death_cert": "acte de deces (death certificate from the local mairie)",
        "registry": "local mairie (town hall) or commune civil registration office",
        "language": "French",
        "apostille": True,
        "apostille_year": "1960",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Paris",
        "embassy_note": "The British Embassy in Paris can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 15 (SAMU), 17 (police), or 112 for emergency services. Death is registered at the local mairie (town hall) within 24 hours. The official death certificate is the acte de deces. The Procureur de la Republique (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths. France is a Hague Apostille Convention member since 1960. Death certificates are issued in French. The British Embassy in Paris can assist British nationals. (FCDO Travel Advice France 2025; French Ministry of Justice civil registration procedures 2025.)",
        "police_note": "The Procureur de la Republique takes jurisdiction for violent or suspicious deaths. A judicial investigation can significantly delay body release.",
        "source": "FCDO Travel Advice France 2025; French Ministry of Justice civil registration procedures 2025; Hague Conference France profile 1960",
        "translation_note": "The acte de deces is issued in French. Certified translation into the destination country's language is required for all non-French-speaking destinations.",
    },
    "canada": {
        "name": "Canada",
        "slug": "canada",
        "airport": "Toronto Pearson (YYZ), Vancouver (YVR), Montreal (YUL), or other major Canadian airport",
        "emergency": "911",
        "death_cert": "death certificate (provincial civil registration authority)",
        "registry": "provincial civil registration authority (the civil records office for each province and territory)",
        "language": "English or French depending on province",
        "apostille": True,
        "apostille_year": "November 2024",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "10-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Ottawa",
        "embassy_note": "The British High Commission in Ottawa can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 911 for emergency services. Death is certified by a licensed physician and registered with the provincial civil registration authority. The coroner or medical examiner takes jurisdiction for sudden, violent, or unexplained deaths. Canada joined the Hague Apostille Convention in November 2024, simplifying document authentication. Death certificates are issued in English or French depending on the province. The British High Commission in Ottawa can assist British nationals. (Global Affairs Canada consular guidance 2025; Hague Conference Canada profile November 2024.)",
        "police_note": "The coroner or medical examiner investigates sudden, violent, or unexplained deaths. Body release requires coroner authorisation before repatriation can proceed.",
        "source": "Global Affairs Canada consular guidance 2025; provincial civil registration offices 2025; Hague Conference Canada profile November 2024",
        "translation_note": "Death certificates are issued in English. Documentation is issued in English or French depending on the province. Certified translation is required where needed.",
    },
    "netherlands": {
        "name": "Netherlands",
        "slug": "netherlands",
        "airport": "Amsterdam Schiphol (AMS), Rotterdam The Hague (RTM), or Eindhoven (EIN)",
        "emergency": "112",
        "death_cert": "akte van overlijden (death certificate from the local gemeente)",
        "registry": "local gemeente (municipality), Basisregistratie Personen (BRP)",
        "language": "Dutch",
        "apostille": True,
        "apostille_year": "1960",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "The Hague",
        "embassy_note": "The British Embassy in The Hague can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 for emergency services. Death is registered with the local gemeente (municipality) in the BRP (Municipal Personal Records Database). The official death certificate is the akte van overlijden. The Officier van Justitie (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths. The Netherlands is a founding Hague Apostille Convention member since 1960. The British Embassy in The Hague can assist British nationals. (FCDO Travel Advice Netherlands 2025; Dutch Ministry of Justice civil registration procedures 2025.)",
        "police_note": "The Officier van Justitie investigates violent or suspicious deaths. Body release requires formal clearance before repatriation can proceed.",
        "source": "FCDO Travel Advice Netherlands 2025; Dutch Ministry of Justice civil registration procedures 2025; Hague Conference Netherlands profile 1960",
        "translation_note": "The akte van overlijden is issued in Dutch. Certified translation is required for non-Dutch-speaking destinations.",
    },
    "italy": {
        "name": "Italy",
        "slug": "italy",
        "airport": "Rome Fiumicino (FCO), Milan Malpensa (MXP), Naples (NAP), or other major Italian airport",
        "emergency": "112 (general), 118 (medical), 113 (police)",
        "death_cert": "atto di morte (death certificate from the local Comune)",
        "registry": "local Comune (ufficio di stato civile, civil status office)",
        "language": "Italian",
        "apostille": True,
        "apostille_year": "1978",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Rome",
        "embassy_note": "The British Embassy in Rome can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 or 118 for emergency services. Death must be declared within 24 hours at the local Comune (ufficio di stato civile). The official death certificate is the atto di morte. The Procura della Repubblica (public prosecutor) takes jurisdiction for violent, suspicious, or unexplained deaths; a formal nulla osta is required before the body can be moved. Italy is a Hague Apostille Convention member since 1978. The British Embassy in Rome can assist British nationals. (FCDO Travel Advice Italy 2025; Italian Ministry of Interior civil registration procedures 2025.)",
        "police_note": "The Procura della Repubblica investigates violent or suspicious deaths. A formal nulla osta (judicial clearance) is required before the body can be released for repatriation.",
        "source": "FCDO Travel Advice Italy 2025; Italian Ministry of Interior civil registration procedures 2025; Hague Conference Italy profile 1978",
        "translation_note": "The atto di morte is issued in Italian. Certified translation is required for non-Italian-speaking destinations.",
    },
    "belgium": {
        "name": "Belgium",
        "slug": "belgium",
        "airport": "Brussels Airport (BRU) or Brussels South Charleroi (CRL)",
        "emergency": "112 (medical and fire), 101 (police)",
        "death_cert": "acte de deces or overlijdensakte (death certificate from the local commune or gemeenten)",
        "registry": "local commune (French-speaking areas) or gemeenten (Flemish areas), Registre National/Rijksregister",
        "language": "French, Dutch, or German depending on region",
        "apostille": True,
        "apostille_year": "1975",
        "complexity": "low",
        "timeline_avg": "2-4 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "4-8 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Brussels",
        "embassy_note": "The British Embassy in Brussels can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 (ambulance and fire) or 101 (police) for emergency services. Death is registered with the local commune or gemeenten within 24 hours. The official death certificate is the acte de deces (French and German regions) or overlijdensakte (Flemish region). The Procureur du Roi takes jurisdiction for violent, suspicious, or unexplained deaths. Belgium is a Hague Apostille Convention member since 1975. The British Embassy in Brussels can assist British nationals. (FCDO Travel Advice Belgium 2025; Belgian FPS Home Affairs civil registration procedures 2025.)",
        "police_note": "The Procureur du Roi investigates violent or suspicious deaths. Formal clearance is required before the body can be released for repatriation.",
        "source": "FCDO Travel Advice Belgium 2025; Belgian FPS Home Affairs civil registration procedures 2025; Hague Conference Belgium profile 1975",
        "translation_note": "Documentation is issued in French, Dutch, or German depending on region. Certified translation is required where needed.",
    },
    "norway": {
        "name": "Norway",
        "slug": "norway",
        "airport": "Oslo Gardermoen (OSL), Bergen (BGO), or Stavanger (SVG)",
        "emergency": "112 (police), 113 (medical)",
        "death_cert": "dodsattest (death certificate from Folkeregisteret via Skatteetaten)",
        "registry": "Folkeregisteret (Norwegian Population Register), administered by Skatteetaten (Tax Administration)",
        "language": "Norwegian",
        "apostille": True,
        "apostille_year": "1980",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "3-6 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Oslo",
        "embassy_note": "The British Embassy in Oslo can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 (police) or 113 (ambulance) for emergency services. Death is registered with Folkeregisteret (Norwegian Population Register) via Skatteetaten. The official death certificate is the dodsattest. The Norwegian Police Service investigates violent, suspicious, or unexplained deaths. Norway is a Hague Apostille Convention member since 1980. The British Embassy in Oslo can assist British nationals. (FCDO Travel Advice Norway 2025; Norwegian Skatteetaten population register procedures 2025.)",
        "police_note": "The Norwegian Police Service investigates violent or suspicious deaths. Body release requires police clearance before repatriation can proceed.",
        "source": "FCDO Travel Advice Norway 2025; Norwegian Skatteetaten population register procedures 2025; Hague Conference Norway profile 1980",
        "translation_note": "The dodsattest is issued in Norwegian. Certified translation is required for non-Norwegian-speaking destinations.",
    },
    "sweden": {
        "name": "Sweden",
        "slug": "sweden",
        "airport": "Stockholm Arlanda (ARN), Gothenburg Landvetter (GOT), or other major Swedish airport",
        "emergency": "112",
        "death_cert": "dodsfallsintyg (death certificate from Skatteverket)",
        "registry": "Skatteverket (Swedish Tax Agency), which maintains the population register",
        "language": "Swedish",
        "apostille": True,
        "apostille_year": "1999",
        "complexity": "low",
        "timeline_avg": "2-3 weeks",
        "timeline_fast": "7-14 days",
        "timeline_complex": "3-6 weeks",
        "doc_processing": "5-10 days",
        "embassy_city": "Stockholm",
        "embassy_note": "The British Embassy in Stockholm can register the death with UK authorities and advise on local funeral directors. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
        "overview": "Call 112 for emergency services. Death is registered with Skatteverket (the Swedish Tax Agency population register). The official death certificate is the dodsfallsintyg. The Swedish Police Authority investigates violent, suspicious, or unexplained deaths. Sweden is a Hague Apostille Convention member since 1999. The British Embassy in Stockholm can assist British nationals. (FCDO Travel Advice Sweden 2025; Swedish Skatteverket population register procedures 2025.)",
        "police_note": "The Swedish Police Authority investigates violent or suspicious deaths. Body release requires police clearance before repatriation can proceed.",
        "source": "FCDO Travel Advice Sweden 2025; Swedish Skatteverket population register procedures 2025; Hague Conference Sweden profile 1999",
        "translation_note": "The dodsfallsintyg is issued in Swedish. Certified translation is required for non-Swedish-speaking destinations.",
    },
}

# ---------------------------------------------------------------------------
# Destination data -- ten new Tier C destinations, none previously covered
# anywhere in the route matrix. Facts sourced from HCCH Apostille status
# table (hcch.net, checked July 2026), GOV.UK "British Embassy/High
# Commission" world-organisation pages and GOV.UK bereavement guidance pages
# (all checked July 2026, individual page "last updated" dates noted where
# GOV.UK shows one).
# ---------------------------------------------------------------------------

DEST_META = {
    "saint-kitts-and-nevis": {
        "name": "Saint Kitts and Nevis",
        "slug": "saint-kitts-and-nevis",
        "display_name": "Saint Kitts and Nevis",
        "airport": "Robert L. Bradshaw International Airport (SKB), Basseterre, Saint Kitts",
        "reception": "The funeral director in Saint Kitts and Nevis takes custody at the cargo terminal at Robert L. Bradshaw International Airport (SKB), Basseterre. Death is registered with the Registrar General's Office on Saint Kitts or the Registrar General Department on Nevis, island-specific civil registries. Saint Kitts and Nevis has been a Hague Apostille Convention member since 14 December 1994. Death certificates are issued in English.",
        "consular_note": "There is no resident British High Commission in Saint Kitts and Nevis; an honorary British consul is in place, with full consular support from the British High Commission in Bridgetown, Barbados, which covers the Eastern Caribbean. Hague Apostille applies (Saint Kitts and Nevis joined 1994).",
        "apostille": "Hague Apostille (1994)",
        "timeline": "2-4 weeks standard",
        "dest_key": "saint-kitts-and-nevis",
        "country_note": "Saint Kitts and Nevis requires a post-mortem for any foreign national who dies within 24 hours of arrival on the island, at the coroner's discretion for later deaths. The examining medical examiner is based in Barbados and is not always immediately available, which can add days to the process. There is no resident British High Commission; consular support comes from Bridgetown, Barbados.",
    },
    "saint-vincent-and-the-grenadines": {
        "name": "Saint Vincent and the Grenadines",
        "slug": "saint-vincent-and-the-grenadines",
        "display_name": "Saint Vincent and the Grenadines",
        "airport": "Argyle International Airport (SVD), Saint Vincent",
        "reception": "The funeral director in Saint Vincent and the Grenadines takes custody at the cargo terminal at Argyle International Airport (SVD). Death must be registered within three days with the Civil Registry Department (Registrar General), based at the High Court in Kingstown. Saint Vincent and the Grenadines has been a Hague Apostille Convention member since 27 October 1979. Death certificates are issued in English.",
        "consular_note": "A British High Commission office exists in Kingstown but does not itself provide consular services; these come from the British High Commission in Bridgetown, Barbados. Hague Apostille applies (Saint Vincent and the Grenadines joined 1979).",
        "apostille": "Hague Apostille (1979)",
        "timeline": "2-4 weeks standard",
        "dest_key": "saint-vincent-and-the-grenadines",
        "country_note": "There are no crematoriums anywhere in Saint Vincent and the Grenadines. A body needing cremation must first be transported to a neighbouring island such as Grenada, Barbados, or Saint Lucia. Embalming certificates are required whether the case proceeds to repatriation or cremation elsewhere.",
    },
    "dominica": {
        "name": "Dominica",
        "slug": "dominica",
        "display_name": "Dominica",
        "airport": "Douglas-Charles Airport (DOM), on Dominica's northeast coast",
        "reception": "The funeral director in Dominica takes custody at the cargo terminal at Douglas-Charles Airport (DOM). Death is registered with the Registry Department (Births, Marriages and Deaths section) in Roseau. Dominica has been a Hague Apostille Convention member since 3 November 1978. Death certificates are issued in English.",
        "consular_note": "There is no resident British High Commission in Dominica. The British High Commission in Bridgetown, Barbados, covers Dominica and the wider Eastern Caribbean. Hague Apostille applies (Dominica, member since 1978).",
        "apostille": "Hague Apostille (1978)",
        "timeline": "2-4 weeks standard",
        "dest_key": "dominica",
        "country_note": "Dominica has no cremation facilities of its own. A body requiring cremation must be transported to Barbados or Saint Lucia first. Post-mortems are routine and are usually completed within four days, depending on pathologist availability. There is no resident British High Commission; consular support comes from Bridgetown, Barbados.",
    },
    "suriname": {
        "name": "Suriname",
        "slug": "suriname",
        "display_name": "Suriname",
        "airport": "Johan Adolf Pengel International Airport (PBM), Paramaribo",
        "reception": "The funeral director in Suriname takes custody at the cargo terminal at Johan Adolf Pengel International Airport (PBM), Paramaribo. Death is registered with the Centraal Bureau voor Burgerzaken (CBB), the Central Bureau of Civil Affairs, which runs 42 field offices across 10 districts. Suriname has been a Hague Apostille Convention member since 25 November 1975. The death certificate, the Overlijdens Akte, is issued in Dutch and does not record a cause of death.",
        "consular_note": "There is no resident British embassy in Suriname. The British High Commission in Georgetown, Guyana, covers Suriname, supported by an honorary British consul in Paramaribo. Hague Apostille applies (Suriname, member since 1975).",
        "apostille": "Hague Apostille (1975)",
        "timeline": "2-5 weeks standard",
        "dest_key": "suriname",
        "country_note": "The Surinamese death certificate, the Overlijdens Akte, is issued in Dutch and does not state a cause of death, which can surprise receiving authorities used to seeing one recorded. Local cremation requires a Ministry of Justice and Police licence and next-of-kin consent, and exporting ashes needs a further export permit from the same ministry. Suriname has no resident British embassy; consular support comes from the British High Commission in Georgetown, Guyana.",
    },
    "cabo-verde": {
        "name": "Cabo Verde",
        "slug": "cabo-verde",
        "display_name": "Cabo Verde",
        "airport": "Amilcar Cabral International Airport (SID), Sal Island, Cabo Verde's main international gateway",
        "reception": "The funeral director in Cabo Verde takes custody at the cargo terminal at Amilcar Cabral International Airport (SID) on Sal Island. Death is registered with the local Conservatoria do Registo Civil (Civil Registration Office), under the Direcao-Geral dos Registos, Notariado e Identificacao. Cabo Verde has been a Hague Apostille Convention member since 13 February 2010. Death certificates are issued in Portuguese.",
        "consular_note": "There is no resident British embassy in Cabo Verde. The British Embassy in Lisbon, Portugal, covers Cabo Verde and can advise on documentation. Hague Apostille applies (Cabo Verde, member since 2010).",
        "apostille": "Hague Apostille (2010)",
        "timeline": "3-5 weeks standard",
        "dest_key": "cabo-verde",
        "hub_slug": "cape-verde",
        "country_note": "Cabo Verde has no cremation facilities anywhere in the archipelago, and embalming facilities exist on only three of its ten islands: Praia, Mindelo, and Espargos on Sal. Death certificates are issued only in Portuguese, so certified translation is required for UK use. There is no resident British embassy; consular support comes from the British Embassy in Lisbon.",
    },
    "seychelles": {
        "name": "Seychelles",
        "slug": "seychelles",
        "display_name": "Seychelles",
        "airport": "Seychelles International Airport (SEZ), Mahe",
        "reception": "The funeral director in Seychelles takes custody at the cargo terminal at Seychelles International Airport (SEZ), Mahe. Death must be declared within 24 hours to the Civil Status Division, under the Department of Immigration and Civil Status, along with a Medical Certificate from a Medical Officer. Seychelles has been a Hague Apostille Convention member since 31 March 1979. Death certificates are issued in English, French, or Seychellois Creole.",
        "consular_note": "The British High Commission in Victoria, Mahe, is resident in Seychelles and provides consular assistance directly, unlike several neighbouring island nations. Hague Apostille applies (Seychelles, member since 1979).",
        "apostille": "Hague Apostille (1979)",
        "timeline": "2-4 weeks standard",
        "dest_key": "seychelles",
        "country_note": "Seychelles has a resident British High Commission in Victoria that provides consular support directly, unlike many other small island states covered from a neighbouring country. If the local death certificate is not issued in English, the family must obtain and pay for an official translation before it can be used for UK purposes.",
    },
    "bahamas": {
        "name": "The Bahamas",
        "slug": "bahamas",
        "display_name": "the Bahamas",
        "airport": "Lynden Pindling International Airport (NAS), Nassau, New Providence",
        "reception": "The funeral director in the Bahamas takes custody at the cargo terminal at Lynden Pindling International Airport (NAS), Nassau. Death must be registered within 21 days with the Registrar General's Department (RGD) in Nassau, based on the Medical Certificate of Death submitted by a mortician. The Bahamas has been a Hague Apostille Convention member since independence on 10 July 1973 (succession formally declared in 1976). Death certificates are issued in English.",
        "consular_note": "The British High Commission building in Nassau does not provide consular services at post. All consular services for British nationals in the Bahamas are provided by the British High Commission in Kingston, Jamaica. Hague Apostille applies (Bahamas, member since 1973).",
        "apostille": "Hague Apostille (1973)",
        "timeline": "2-5 weeks standard",
        "dest_key": "bahamas",
        "country_note": "Consular support for the Bahamas comes from the British High Commission in Kingston, Jamaica, not from the British High Commission building in Nassau itself, which does not handle consular casework. For a sudden or unnatural death, post-mortem toxicology samples from the Bahamas are sent to the United States and can take up to a year to return, which can significantly delay a case pending a UK coroner's inquest.",
    },
    "antigua-and-barbuda": {
        "name": "Antigua and Barbuda",
        "slug": "antigua-and-barbuda",
        "display_name": "Antigua and Barbuda",
        "airport": "V.C. Bird International Airport (ANU), near St John's, Antigua",
        "reception": "The funeral director in Antigua and Barbuda takes custody at the cargo terminal at V.C. Bird International Airport (ANU). Death is registered with the Civil Registry at the High Court, St John's, under the Civil Registration Act 2020. Antigua and Barbuda has been a Hague Apostille Convention member since independence on 1 November 1981 (succession formally declared in 1985). Death certificates are issued in English.",
        "consular_note": "A British High Commission office exists in St John's but does not provide consular services itself; the resident High Commissioner is based in Bridgetown, Barbados, with non-resident accreditation to Antigua and Barbuda. Hague Apostille applies (Antigua and Barbuda, member since 1981).",
        "apostille": "Hague Apostille (1981)",
        "timeline": "2-4 weeks standard",
        "dest_key": "antigua-and-barbuda",
        "country_note": "There are no cremation facilities in Antigua or Barbuda. A family choosing cremation over burial or repatriation must arrange it in Puerto Rico, Barbados, or Grenada through a local funeral director. The British High Commission office in St John's does not handle consular casework; that comes from Bridgetown, Barbados.",
    },
    "saint-lucia": {
        "name": "Saint Lucia",
        "slug": "saint-lucia",
        "display_name": "Saint Lucia",
        "airport": "Hewanorra International Airport (UVF), Vieux Fort, Saint Lucia's long-haul and cargo gateway",
        "reception": "The funeral director in Saint Lucia takes custody at the cargo terminal at Hewanorra International Airport (UVF), Vieux Fort. Death is registered with the Registry of Civil Status, part of the Ministry of Home Affairs, in Castries. Saint Lucia has been a Hague Apostille Convention member since 31 July 2002. Death certificates are issued in English, typically within two days of any post-mortem.",
        "consular_note": "The British High Commission office in Castries is a subsidiary office of the British High Commission in Bridgetown, Barbados, where the resident High Commissioner is based. Hague Apostille applies (Saint Lucia, member since 2002).",
        "apostille": "Hague Apostille (2002)",
        "timeline": "2-4 weeks standard",
        "dest_key": "saint-lucia",
        "country_note": "Saint Lucia operates local crematoriums, unusually for the Eastern Caribbean, though local rules restrict scattering cremated remains to designated sea areas rather than on land. The British High Commission office in Castries is a subsidiary of the High Commission in Bridgetown, Barbados, where the resident High Commissioner sits.",
    },
    "grenada": {
        "name": "Grenada",
        "slug": "grenada",
        "display_name": "Grenada",
        "airport": "Maurice Bishop International Airport (GND), St George's",
        "reception": "The funeral director in Grenada takes custody at the cargo terminal at Maurice Bishop International Airport (GND), St George's. Death is registered with the Registrar General's Department at the Grenada Family Records Centre, under the Ministry of Health. Grenada has been a Hague Apostille Convention member since 7 April 2002. Death certificates are issued in English, typically within two days.",
        "consular_note": "A British High Commission office has operated in St George's since 2019, but the resident High Commissioner is based in Bridgetown, Barbados, with non-resident accreditation to Grenada. Hague Apostille applies (Grenada, member since 2002).",
        "apostille": "Hague Apostille (2002)",
        "timeline": "2-4 weeks standard",
        "dest_key": "grenada",
        "country_note": "La Qua Brothers Funeral Home is the only crematorium in Grenada, and mortuary cold-storage capacity is limited to Grenada General Hospital and the island's two funeral directors. The British High Commission office in St George's, open since 2019, does not replace the resident High Commissioner, who remains based in Bridgetown, Barbados.",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R101: starts at template C (index 2). 25 routes.
R101_ROUTES = [
    # Saint Kitts and Nevis x5
    ("australia", "saint-kitts-and-nevis"),
    ("canada", "saint-kitts-and-nevis"),
    ("france", "saint-kitts-and-nevis"),
    ("netherlands", "saint-kitts-and-nevis"),
    ("sweden", "saint-kitts-and-nevis"),
    # Saint Vincent and the Grenadines x5
    ("italy", "saint-vincent-and-the-grenadines"),
    ("belgium", "saint-vincent-and-the-grenadines"),
    ("norway", "saint-vincent-and-the-grenadines"),
    ("canada", "saint-vincent-and-the-grenadines"),
    ("australia", "saint-vincent-and-the-grenadines"),
    # Dominica x5
    ("france", "dominica"),
    ("netherlands", "dominica"),
    ("sweden", "dominica"),
    ("italy", "dominica"),
    ("canada", "dominica"),
    # Suriname x5
    ("netherlands", "suriname"),
    ("belgium", "suriname"),
    ("norway", "suriname"),
    ("france", "suriname"),
    ("australia", "suriname"),
    # Cabo Verde x5
    ("italy", "cabo-verde"),
    ("sweden", "cabo-verde"),
    ("belgium", "cabo-verde"),
    ("canada", "cabo-verde"),
    ("norway", "cabo-verde"),
]

# R102: starts at template C (index 2). 25 routes.
R102_ROUTES = [
    # Seychelles x5
    ("australia", "seychelles"),
    ("france", "seychelles"),
    ("italy", "seychelles"),
    ("netherlands", "seychelles"),
    ("canada", "seychelles"),
    # Bahamas x5
    ("canada", "bahamas"),
    ("france", "bahamas"),
    ("sweden", "bahamas"),
    ("netherlands", "bahamas"),
    ("italy", "bahamas"),
    # Antigua and Barbuda x5
    ("australia", "antigua-and-barbuda"),
    ("canada", "antigua-and-barbuda"),
    ("norway", "antigua-and-barbuda"),
    ("belgium", "antigua-and-barbuda"),
    ("sweden", "antigua-and-barbuda"),
    # Saint Lucia x5
    ("france", "saint-lucia"),
    ("italy", "saint-lucia"),
    ("netherlands", "saint-lucia"),
    ("canada", "saint-lucia"),
    ("australia", "saint-lucia"),
    # Grenada x5
    ("norway", "grenada"),
    ("sweden", "grenada"),
    ("belgium", "grenada"),
    ("france", "grenada"),
    ("netherlands", "grenada"),
]

# ---------------------------------------------------------------------------
# Varied title shapes, description openings, intro texts (burstiness and
# anti-template-footprint measures per CLAUDE.md canonical constants, 5 Jul 2026)
# ---------------------------------------------------------------------------

TITLE_SHAPES = [
    lambda o, d: f"{o} to {d} Repatriation: Family Guidance",
    lambda o, d: f"Repatriation from {o} to {d}",
    lambda o, d: f"Bringing Someone Home from {o} to {d}",
    lambda o, d: f"{o} to {d}: Funeral Repatriation Guidance",
    lambda o, d: f"{o} to {d} Repatriation Guide",
]

DESCRIPTION_OPENERS = [
    lambda o, d, t: f"A death in {o} brings immediate questions. Repatriation to {d} takes {t}. Contact us 24/7.",
    lambda o, d, t: f"Bringing a loved one home from {o} to {d} takes {t} in most cases. All documentation handled. Contact us 24/7.",
    lambda o, d, t: f"Death in {o}, coming home to {d}. Repatriation takes {t}. Consular support included. Contact us 24/7.",
    lambda o, d, t: f"Arranging repatriation from {o} to {d}? Most cases complete within {t}. All documentation handled. Call us now.",
    lambda o, d, t: f"When someone dies in {o}, {d} families face a defined process taking {t}. Contact us 24/7.",
]

INTRO_VARS = {
    0: "The process starts the moment the death is reported.",
    1: "Repatriation from {origin} takes {timeline_avg} in most cases.",
    2: "Getting a loved one home from {origin} is possible. The process has clear steps.",
    3: "A death in {origin} brings specific documentation and consular procedures.",
    4: "Families in {dest_name} waiting for news from {origin} face a defined process.",
}

OVERVIEW_SUFFIX = {
    0: "Appoint a repatriation specialist on day one.",
    1: "Contact us at any hour on +44 7703 577246.",
    2: "The earlier a specialist is involved, the faster the process moves.",
    3: "Do not sign anything locally without specialist advice.",
    4: "Our team is available 24 hours a day, every day of the year.",
}

# ---------------------------------------------------------------------------
# Page generator
# ---------------------------------------------------------------------------

def make_title(origin_data, dest_data, page_index):
    """Generate an SEO-optimised title under 60 characters, rotating shape."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    shape = TITLE_SHAPES[page_index % len(TITLE_SHAPES)]
    title = shape(origin, dest)
    if len(title) > 60:
        title = f"{origin} to {dest} Repatriation Guide"
    if len(title) > 60:
        title = f"{origin} to {dest} Repatriation"
    return title


def make_description(origin_data, dest_data, page_index):
    """Generate an SEO description under 155 characters with CTA, rotating opener."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    timeline = origin_data["timeline_avg"]
    opener = DESCRIPTION_OPENERS[page_index % len(DESCRIPTION_OPENERS)]
    desc = opener(origin, dest, timeline)
    if len(desc) > 155:
        desc = f"Death in {origin}. Repatriation to {dest} takes {timeline}. All documentation handled. Contact us 24/7."
    if len(desc) > 155:
        desc = f"Repatriation from {origin} to {dest} takes {timeline}. Contact us 24/7."
    return desc


def make_embassy_note(dest_data, origin_name):
    """Generate destination consular note."""
    return dest_data["consular_note"]


DEST_CONSULAR_LINES = {
    "saint-kitts-and-nevis": "Notify the honorary British consul, or the British High Commission Bridgetown, Barbados. Hague Apostille applies (Saint Kitts and Nevis joined 1994).",
    "saint-vincent-and-the-grenadines": "Notify the British High Commission Bridgetown, Barbados (the Kingstown office does not handle consular casework). Hague Apostille applies (Saint Vincent and the Grenadines joined 1979).",
    "dominica": "Notify the British High Commission Bridgetown, Barbados. Hague Apostille applies (Dominica joined 1978).",
    "suriname": "Notify the British High Commission Georgetown, Guyana, or the honorary British consul in Paramaribo. Hague Apostille applies (Suriname joined 1975).",
    "cabo-verde": "Notify the British Embassy Lisbon, Portugal. Hague Apostille applies (Cabo Verde joined 2010).",
    "seychelles": "Notify the British High Commission Victoria, Mahe, which is resident and provides consular assistance directly. Hague Apostille applies (Seychelles joined 1979).",
    "bahamas": "Notify the British High Commission Kingston, Jamaica (the Nassau office does not handle consular casework). Hague Apostille applies (Bahamas member since independence in 1973).",
    "antigua-and-barbuda": "Notify the British High Commission Bridgetown, Barbados (the St John's office does not handle consular casework). Hague Apostille applies (Antigua and Barbuda member since independence in 1981).",
    "saint-lucia": "Notify the British High Commission Bridgetown, Barbados, whose Castries office is a subsidiary. Hague Apostille applies (Saint Lucia joined 2002).",
    "grenada": "Notify the British High Commission Bridgetown, Barbados (the St George's office does not replace the resident High Commissioner). Hague Apostille applies (Grenada joined 2002).",
}

DEST_RECEPTION_STEPS = {
    "saint-kitts-and-nevis": "Funeral director in Saint Kitts and Nevis takes custody at the cargo terminal at Robert L. Bradshaw International Airport (SKB), Basseterre. Registrar General's Office notified. Death certificate issued in English.",
    "saint-vincent-and-the-grenadines": "Funeral director in Saint Vincent and the Grenadines takes custody at the cargo terminal at Argyle International Airport (SVD). Civil Registry Department notified. Death certificate issued in English.",
    "dominica": "Funeral director in Dominica takes custody at the cargo terminal at Douglas-Charles Airport (DOM). Registry Department notified. Death certificate issued in English.",
    "suriname": "Funeral director in Suriname takes custody at the cargo terminal at Johan Adolf Pengel International Airport (PBM), Paramaribo. Centraal Bureau voor Burgerzaken notified. Death certificate (Overlijdens Akte) issued in Dutch.",
    "cabo-verde": "Funeral director in Cabo Verde takes custody at the cargo terminal at Amilcar Cabral International Airport (SID), Sal Island. Conservatoria do Registo Civil notified. Death certificate issued in Portuguese.",
    "seychelles": "Funeral director in Seychelles takes custody at the cargo terminal at Seychelles International Airport (SEZ), Mahe. Civil Status Division notified. Death certificate issued in English, French, or Seychellois Creole.",
    "bahamas": "Funeral director in the Bahamas takes custody at the cargo terminal at Lynden Pindling International Airport (NAS), Nassau. Registrar General's Department notified. Death certificate issued in English.",
    "antigua-and-barbuda": "Funeral director in Antigua and Barbuda takes custody at the cargo terminal at V.C. Bird International Airport (ANU). Civil Registry at the High Court, St John's, notified. Death certificate issued in English.",
    "saint-lucia": "Funeral director in Saint Lucia takes custody at the cargo terminal at Hewanorra International Airport (UVF), Vieux Fort. Registry of Civil Status notified. Death certificate issued in English.",
    "grenada": "Funeral director in Grenada takes custody at the cargo terminal at Maurice Bishop International Airport (GND), St George's. Registrar General's Department notified. Death certificate issued in English.",
}


def make_timeline_steps(origin_data, dest_data):
    """Generate 7 timeline steps appropriate to the corridor."""
    origin = origin_data["name"]
    dest_airport = dest_data["airport"]
    cert = origin_data["death_cert"]
    doc_time = origin_data["doc_processing"]
    dest_key = dest_data["dest_key"]

    consular = DEST_CONSULAR_LINES.get(dest_key, f"Notify the {dest_data['name']} Embassy in {origin}.")
    reception_step = DEST_RECEPTION_STEPS.get(dest_key, f"{dest_data['name']} funeral director takes custody at cargo terminal.")

    emergency_line = "FCDO 24-hour emergency line: +44 (0)20 7008 5000."

    steps = [
        {
            "step": 1,
            "action": "Immediate steps after death. Report to local emergency services and contact a specialist at once.",
            "timing": f"Day of death. {emergency_line}",
            "responsible": "Family or travel insurer",
        },
        {
            "step": 2,
            "action": f"Death registered. {cert.capitalize()} obtained from {origin_data['registry']}.",
            "timing": f"Registration must occur promptly. {origin_data.get('police_note', 'Local police clearance may be required.')}",
            "responsible": "Local funeral director and civil registry",
        },
        {
            "step": 3,
            "action": f"Embassy or consulate notified. {consular}",
            "timing": "Simultaneous with Step 1. Embassy provides list of local funeral directors.",
            "responsible": "Family or repatriation specialist",
        },
        {
            "step": 4,
            "action": "Embalming and preparation for international air transport.",
            "timing": "After body released by authorities. IATA P650 requirements apply.",
            "responsible": "Licensed local funeral director",
        },
        {
            "step": 5,
            "action": f"All export permits and authenticated documents obtained. {origin_data.get('translation_note', '')}",
            "timing": f"Allow {doc_time}. Cannot begin until death certificate issued.",
            "responsible": "Local funeral director and authorities",
        },
        {
            "step": 6,
            "action": f"Air cargo from {origin_data['airport']} to {dest_airport}.",
            "timing": "Once all documentation complete.",
            "responsible": "Repatriation specialist and airline cargo",
        },
        {
            "step": 7,
            "action": f"{reception_step}",
            "timing": "Within 24-48 hours of arrival.",
            "responsible": "Receiving funeral director",
        },
    ]
    return steps


DEST_FAQ6 = {
    "saint-kitts-and-nevis": lambda origin: {
        "question": f"Is a post-mortem always required for a repatriation from {origin} to Saint Kitts and Nevis?",
        "answer": (
            "Not always. Saint Kitts and Nevis requires a post-mortem for any foreign national who dies within 24 hours of arrival on the island; "
            "for deaths occurring later, the coroner decides case by case. "
            "The examining medical examiner is based in Barbados and is not always immediately available, which can add days to the timeline."
        ),
    },
    "saint-vincent-and-the-grenadines": lambda origin: {
        "question": f"Can cremation take place locally if a family from {origin} prefers it to a full repatriation?",
        "answer": (
            "No. There are no crematoriums anywhere in Saint Vincent and the Grenadines. "
            "A body needing cremation must first be transported to a neighbouring island, such as Grenada, Barbados, or Saint Lucia. "
            "Embalming certificates are required either way."
        ),
    },
    "dominica": lambda origin: {
        "question": f"Is cremation available in Dominica for a family arranging repatriation from {origin}?",
        "answer": (
            "No. Dominica has no cremation facilities of its own. "
            "A body requiring cremation must be transported to Barbados or Saint Lucia first. "
            "Post-mortems in Dominica are routine and usually complete within four days, depending on pathologist availability."
        ),
    },
    "suriname": lambda origin: {
        "question": f"Why might a Surinamese death certificate look different to families arranging repatriation from {origin}?",
        "answer": (
            "The Surinamese death certificate, the Overlijdens Akte, does not record a cause of death, unlike most European and Commonwealth certificates. "
            "It is issued in Dutch by the Centraal Bureau voor Burgerzaken. "
            "Local cremation requires a separate Ministry of Justice and Police licence, and exporting ashes needs a further export permit from the same ministry."
        ),
    },
    "cabo-verde": lambda origin: {
        "question": f"Is cremation an option in Cabo Verde for a family repatriating from {origin}?",
        "answer": (
            "No. Cabo Verde has no cremation facilities anywhere in the archipelago. "
            "Embalming facilities exist on only three of its ten islands: Praia, Mindelo, and Espargos on Sal. "
            "Death certificates are issued only in Portuguese, so certified translation is required for UK use."
        ),
    },
    "seychelles": lambda origin: {
        "question": f"Does Seychelles have its own resident British High Commission for a repatriation from {origin}?",
        "answer": (
            "Yes. The British High Commission in Victoria, Mahe, is resident in Seychelles and provides consular assistance directly, "
            "unlike several neighbouring island nations covered from another country. "
            "If the local death certificate is not issued in English, the family must obtain and pay for an official translation."
        ),
    },
    "bahamas": lambda origin: {
        "question": f"Which British post actually handles consular support for a repatriation from {origin} to the Bahamas?",
        "answer": (
            "The British High Commission in Kingston, Jamaica, not the British High Commission building in Nassau, "
            "which does not provide consular services at post. "
            "For a sudden or unnatural death, post-mortem toxicology samples from the Bahamas are sent to the United States and can take up to a year to return."
        ),
    },
    "antigua-and-barbuda": lambda origin: {
        "question": f"Is cremation available in Antigua and Barbuda for a repatriation from {origin}?",
        "answer": (
            "No. There are no cremation facilities in Antigua or Barbuda. "
            "A family choosing cremation over burial or repatriation must arrange it in Puerto Rico, Barbados, or Grenada through a local funeral director. "
            "Consular support comes from the British High Commission in Bridgetown, Barbados, not the St John's office."
        ),
    },
    "saint-lucia": lambda origin: {
        "question": f"Are there any restrictions on ashes if a family from {origin} chooses cremation in Saint Lucia?",
        "answer": (
            "Saint Lucia does operate local crematoriums, unusually for the Eastern Caribbean. "
            "Local rules restrict scattering cremated remains to designated sea areas rather than on land, though bringing the ashes home to the UK is a separate matter handled through the funeral director. "
            "The death certificate is issued in English, typically within two days of any post-mortem."
        ),
    },
    "grenada": lambda origin: {
        "question": f"Where does cremation take place in Grenada if a family from {origin} prefers it?",
        "answer": (
            "La Qua Brothers Funeral Home is the only crematorium in Grenada. "
            "Mortuary cold-storage capacity is otherwise limited to Grenada General Hospital and the island's two funeral directors. "
            "The British High Commission office in St George's, open since 2019, does not replace the resident High Commissioner, who remains based in Bridgetown, Barbados."
        ),
    },
}


def make_dest_faq6(origin_data, dest_data):
    """Generate a destination-specific sixth FAQ."""
    origin = origin_data["name"]
    dest_key = dest_data["dest_key"]
    fn = DEST_FAQ6.get(dest_key)
    if fn:
        return fn(origin)
    return {
        "question": f"What specialist support is available for repatriation from {origin} to {dest_data['name']}?",
        "answer": (
            f"A specialist repatriation company can coordinate the full process from {origin} to {dest_data['name']}, "
            "including documentation, embalming, air cargo, and reception at the destination. "
            "Call our team on +44 7703 577246 at any hour for guidance on your specific case."
        ),
    }


def make_faqs(origin_data, dest_data):
    """Generate 6 FAQs for the corridor."""
    origin = origin_data["name"]
    dest = dest_data["name"]
    timeline_avg = origin_data["timeline_avg"]
    timeline_fast = origin_data["timeline_fast"]
    timeline_complex = origin_data["timeline_complex"]
    cert = origin_data["death_cert"]

    consular_answer = origin_data.get("consular_faq")
    if not consular_answer:
        consular_answer = (
            f"The {origin_data['embassy_city']}-based British embassy or high commission can register the death "
            f"with UK authorities, provide a list of local funeral directors, and advise on documentation. "
            f"They cannot pay for or arrange repatriation. "
            f"FCDO 24-hour emergency line: +44 (0)20 7008 5000."
        )

    faqs = [
        {
            "question": f"How long does repatriation from {origin} to {dest} take?",
            "answer": (
                f"In a straightforward case, repatriation from {origin} to {dest} takes {timeline_avg}. "
                f"The fastest cases complete in {timeline_fast}. "
                f"Complex cases involving criminal investigation or remote locations can take {timeline_complex}."
            ),
        },
        {
            "question": f"What documents are required for repatriation from {origin} to {dest}?",
            "answer": (
                f"The core documents are: {cert}, "
                f"embalming certificate, freedom from infection certificate, passport of the deceased, "
                f"and all required export permits. "
                f"{origin_data.get('translation_note', 'Check destination requirements for translation.')} "
                f"Source: FCDO Travel Advice {origin} 2025."
            ),
        },
        {
            "question": f"Does the British Embassy in {origin} help with repatriation?",
            "answer": consular_answer,
        },
        {
            "question": f"What happens when the body arrives in {dest}?",
            "answer": (
                f"{dest_data['reception']} "
                f"All documentation from {origin} must be in order before the body is released for the funeral."
            ),
        },
        {
            "question": f"Can I bring ashes home from {origin} to {dest} instead of repatriating the body?",
            "answer": (
                f"Yes. Cremation in {origin} is an option in most cases, though local authorities must release "
                f"the body before cremation can take place. You will need the death certificate, cremation "
                f"certificate, and an export permit for the ashes. Ashes are simpler to transport than a body "
                f"and carry lower cargo costs. Ask our team for specific guidance on your case."
            ),
        },
        make_dest_faq6(origin_data, dest_data),
    ]
    return faqs


def format_step(step):
    lines = []
    lines.append(f"  - step: {step['step']}")
    lines.append(f"    action: \"{step['action']}\"")
    lines.append(f"    timing: \"{step['timing']}\"")
    lines.append(f"    responsible: \"{step['responsible']}\"")
    return "\n".join(lines)


def format_faq(faq):
    lines = []
    lines.append(f"  - question: \"{faq['question']}\"")
    lines.append(f"    answer: \"{faq['answer']}\"")
    return "\n".join(lines)


def build_page(origin_key, dest_key, variant, page_index):
    """Build the full YAML frontmatter for one route page."""
    o = ORIGIN_DATA[origin_key]
    d = DEST_META[dest_key]

    slug = f"{origin_key}-to-{dest_key}"
    title = make_title(o, d, page_index)
    description = make_description(o, d, page_index)

    # Both destinations are brand new to the matrix, so sideways links point
    # to the two Tier A routes that are guaranteed to already exist for every
    # origin in this batch (origin-to-UK and origin-to-Ireland).
    sideways = (
        f"/routes/{origin_key}-to-united-kingdom/", f"Repatriation from {o['name']} to the UK",
        f"/routes/{origin_key}-to-ireland/", f"Repatriation from {o['name']} to Ireland",
    )

    timeline_steps = make_timeline_steps(o, d)
    faqs = make_faqs(o, d)

    origin_hub_url = f"/repatriation-from-{origin_key}/"
    dest_hub_url = f"/repatriation-from-{d.get('hub_slug', dest_key)}/"
    dest_link_name = d["name"][4:] if d["name"].startswith("The ") else d["name"]

    intro_text = INTRO_VARS[page_index % 5].format(
        origin=o["name"], timeline_avg=o["timeline_avg"], dest_name=d["name"]
    )
    suffix_text = OVERVIEW_SUFFIX[page_index % 5]

    direct_intro = (
        f"Repatriation from {o['name']} to {d['name']} follows {o['name']}'s civil registration and export procedures. "
        f"Most cases take {o['timeline_avg']}."
    )

    lines = []
    lines.append("---")
    lines.append(f'title: "{title}"')
    lines.append(f'description: "{description}"')
    lines.append(f'origin_key: "{origin_key}"')
    lines.append(f'dest_key: "{d["dest_key"]}"')
    lines.append(f'origin_name: "{o["name"]}"')
    lines.append(f'dest_name: "{d["name"]}"')
    lines.append(f'origin_slug: "{origin_key}"')
    lines.append(f'dest_slug: "{dest_key}"')
    lines.append(f'slug: "{slug}"')
    lines.append(f'template_variant: "{variant}"')
    lines.append(f'route_complexity: "{o["complexity"]}"')
    lines.append(f'timeline_avg: "{o["timeline_avg"]}"')
    lines.append(f'timeline_fast: "{o["timeline_fast"]}"')
    lines.append(f'timeline_complex: "{o["timeline_complex"]}"')
    lines.append(f'embassy_city: "{o["embassy_city"]}"')
    lines.append(f'doc_processing_time: "{o["doc_processing"]}"')
    lines.append(f'date: 2026-07-06')
    lines.append(f'direct_answer_heading: "Repatriation from {o["name"]} to {d["name"]}: what to expect"')
    lines.append(f'direct_answer_intro: "{direct_intro}"')
    lines.append('direct_answer_points:')
    lines.append(f'  - "Key document: {o["death_cert"]}"')
    lines.append(f'  - "Documentation takes {o["doc_processing"]}. Appoint a specialist on day one."')
    lines.append(f'  - "British Embassy in {o["embassy_city"]} can advise. They cannot fund repatriation."')
    if o.get("apostille"):
        lines.append(f'  - "{o["name"]} is a Hague Apostille member ({o.get("apostille_year", "member")}). This simplifies document authentication."')
    else:
        lines.append(f'  - "{o["name"]} is not a Hague Apostille member. Documents require legalisation through the Ministry of Foreign Affairs."')
    lines.append(f'  - "Documentation is issued in {o["language"]}. Certified translation is required where needed."')
    lines.append(f'overview_heading: "What happens after a death in {o["name"]}"')
    lines.append(f'overview_body: "{o["overview"]}"')
    lines.append(f'dest_reception: "{d["reception"]}"')
    lines.append(f'dest_consular: "{make_embassy_note(d, o["name"])}"')
    lines.append("timeline_steps:")
    for step in timeline_steps:
        lines.append(format_step(step))
    lines.append("faqs:")
    for faq in faqs:
        lines.append(format_faq(faq))
    lines.append("links:")
    lines.append("  upward:")
    lines.append(f'    - url: "{origin_hub_url}"')
    lines.append(f'      text: "Full {o["name"]} repatriation guide"')
    lines.append(f'    - url: "{dest_hub_url}"')
    lines.append(f'      text: "Full {dest_link_name} repatriation guide"')
    lines.append(f'    - url: "/guides/death-abroad-{origin_key}/"')
    lines.append(f'      text: "What to do if someone dies in {o["name"]}"')
    lines.append(f'    - url: "/embassy-contacts/{origin_key}/"')
    lines.append(f'      text: "British Embassy in {o["name"]}"')
    lines.append(f'    - url: "/contact/"')
    lines.append(f'      text: "Send an enquiry to our team"')
    lines.append("  sideways:")
    lines.append(f'    - url: "{sideways[0]}"')
    lines.append(f'      text: "{sideways[1]}"')
    lines.append(f'    - url: "{sideways[2]}"')
    lines.append(f'      text: "{sideways[3]}"')
    lines.append("---")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    all_batches = [
        ("R101", R101_ROUTES, 2),  # Start at C (index 2)
        ("R102", R102_ROUTES, 2),  # Start at C (index 2)
    ]

    total_written = 0
    page_index = 0
    for chunk_name, routes, start_idx in all_batches:
        print(f"\n=== {chunk_name} ===")
        for i, (origin_key, dest_key) in enumerate(routes):
            variant_idx = (start_idx + i) % len(VARIANTS)
            variant = VARIANTS[variant_idx]
            slug = f"{origin_key}-to-{dest_key}"
            filepath = ROUTES_DIR / f"{slug}.md"

            if filepath.exists():
                print(f"  SKIP (exists): {slug}")
                page_index += 1
                continue

            content = build_page(origin_key, dest_key, variant, page_index)
            filepath.write_text(content, encoding="utf-8")
            print(f"  WROTE [{variant}]: {slug}")
            total_written += 1
            page_index += 1

    print(f"\nTotal pages written: {total_written}")


if __name__ == "__main__":
    main()

