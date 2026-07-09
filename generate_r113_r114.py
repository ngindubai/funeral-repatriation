#!/usr/bin/env python3
"""
generate_r113_r114.py -- Repatriate Service Route Generator
Chunk R113-R114: 50 Tier C route pages, continuing the origin-pool fill-out
phase begun in R112. Every Tier C "single wave" destination introduced
between R97 and R110 was originally given only 5 of the 8 established
origins (Australia, France, Canada, Netherlands, Italy, Norway, Sweden,
Belgium), missing exactly 3 each. R112 completed 8 of these destinations
plus 2 of Monaco's 3 missing origins. This chunk continues in the order
BUILD-PLAN.md set out: Monaco's last missing origin, then Costa Rica
(R98), then the R99-R110 destinations in the order they were introduced,
as far as 50 routes reaches.

R113 (25 routes, template start C): Monaco (1 remaining origin), Costa
Rica, Uruguay, Panama, Guatemala, El Salvador, Honduras, Nicaragua,
Paraguay -- each completed to full 8/8 origin coverage.

R114 (25 routes, template start C, continuing seamlessly): Bolivia, San
Marino, Liechtenstein, Saint Kitts and Nevis, Saint Vincent and the
Grenadines, Dominica, Suriname, Cabo Verde completed to full 8/8; Seychelles
given 1 of its 3 missing origins (Norway), leaving Sweden and Belgium for a
future chunk, the same partial-completion pattern already used for Monaco
in R112.

No new destination research was required for this chunk: every fact below
is reused verbatim from the generator that originally introduced that
destination (generate_r97_r98.py for Monaco and Costa Rica,
generate_r99_r100.py for Uruguay through Liechtenstein,
generate_r101_r102.py for Saint Kitts and Nevis through Seychelles), each
itself sourced from the HCCH Apostille status table, national civil
registry sites, and GOV.UK British Embassy/High Commission pages, checked
July 2026.

Origins (unchanged pool): Australia, France, Canada, Netherlands, Italy,
Norway, Sweden, Belgium.

Template variants: R112 ended at index 1 (B), 26 routes from a start of 1.
R113 starts at C (index 2), 25 routes, ending at index 1 (B). R114
continues seamlessly from index 2 (C) since 25 is a multiple of 5, ending
at index 1 (B) again. No two consecutive pages share a variant.
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r111_r112.py)
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
# Destination data. All reused verbatim from the generator that originally
# introduced each destination (see module docstring for sourcing).
# ---------------------------------------------------------------------------

DEST_META = {
    "monaco": {
        "name": "Monaco",
        "slug": "monaco",
        "airport": "No commercial airport. The nearest international gateway is Nice Cote d'Azur Airport (NCE) in France, with onward transfer by road",
        "reception": "The Monegasque funeral director takes custody following arrival via Nice Cote d'Azur Airport (NCE), since Monaco has no commercial airport of its own. Death is registered with the Etat Civil (Civil Registry) at the Mairie de Monaco (Monaco City Hall). Apostille certification is issued by Monaco's Department of Justice. Monaco is a Hague Apostille Convention member since 31 December 2002. Death certificates are issued in French.",
        "consular_note": "Consulate of Monaco in {origin_country}: contact the Monegasque Consulate for documentation guidance. Hague Apostille applies (Monaco joined 2002). Because Monaco has no international airport, every air cargo route runs via Nice, France, followed by a short road transfer.",
        "apostille": "Hague Apostille (2002)",
        "timeline": "2-3 weeks standard",
        "dest_key": "monaco",
    },
    "costa-rica": {
        "name": "Costa Rica",
        "slug": "costa-rica",
        "airport": "Juan Santamaria International Airport (SJO), San Jose",
        "reception": "The Costa Rican funeral director takes custody at the cargo terminal at Juan Santamaria International Airport (SJO) near San Jose. Death is registered with the Registro Civil, part of the Tribunal Supremo de Elecciones, Costa Rica's electoral authority rather than a justice ministry. Apostille certification is issued by the Ministry of Foreign Affairs and Worship in San Jose. Costa Rica joined the Hague Apostille Convention in 2011. Death certificates are issued in Spanish.",
        "consular_note": "Embassy of Costa Rica in {origin_country}: contact the Costa Rican Embassy for documentation guidance. Hague Apostille applies (Costa Rica joined 2011).",
        "apostille": "Hague Apostille (2011)",
        "timeline": "2-4 weeks standard",
        "dest_key": "costa-rica",
    },
    "uruguay": {
        "name": "Uruguay",
        "slug": "uruguay",
        "airport": "Carrasco International Airport (MVD), Montevideo",
        "reception": "The Uruguayan funeral director takes custody at the cargo terminal at Carrasco International Airport (MVD) near Montevideo. Death is registered with the Direccion General del Registro de Estado Civil, the national civil registry under the Ministry of Education and Culture. Uruguay is a Hague Apostille Convention member since 14 October 2012. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy Montevideo: contact the embassy for documentation guidance. Hague Apostille applies (Uruguay joined 2012). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2012)",
        "timeline": "3-5 weeks standard",
        "dest_key": "uruguay",
    },
    "panama": {
        "name": "Panama",
        "slug": "panama",
        "airport": "Tocumen International Airport (PTY), Panama City",
        "reception": "The Panamanian funeral director takes custody at the cargo terminal at Tocumen International Airport (PTY), Panama City. Death is registered with the Direccion Nacional del Registro Civil, a department of the Tribunal Electoral (Electoral Tribunal) established in 1974, with civil registry offices in every provincial capital. Panama is a Hague Apostille Convention member since 4 August 1991. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy Panama City: contact the embassy for documentation guidance. Hague Apostille applies (Panama joined 1991). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (1991)",
        "timeline": "2-4 weeks standard",
        "dest_key": "panama",
    },
    "guatemala": {
        "name": "Guatemala",
        "slug": "guatemala",
        "airport": "La Aurora International Airport (GUA), Guatemala City",
        "reception": "The Guatemalan funeral director takes custody at the cargo terminal at La Aurora International Airport (GUA), Guatemala City. Death is registered with RENAP (Registro Nacional de las Personas), the national civil registry that also issues the country's national ID. Guatemala is a Hague Apostille Convention member since 18 September 2017. Death certificates are issued in Spanish and carry a QR verification code.",
        "consular_note": "British Embassy Guatemala City: contact the embassy for documentation guidance. This embassy also covers Honduras. Hague Apostille applies (Guatemala joined 2017). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2017)",
        "timeline": "3-5 weeks standard",
        "dest_key": "guatemala",
    },
    "el-salvador": {
        "name": "El Salvador",
        "slug": "el-salvador",
        "airport": "El Salvador International Airport (SAL), also known as Comalapa, near San Salvador",
        "reception": "The Salvadoran funeral director takes custody at the cargo terminal at El Salvador International Airport (SAL). Death is registered at the municipal civil registry office (registro del estado familiar) where the death occurred. Authentication of the death certificate for use abroad is handled separately by the RNPN (Registro Nacional de las Personas Naturales). El Salvador is a Hague Apostille Convention member since 31 May 1996. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy San Salvador: contact the embassy for documentation guidance. Hague Apostille applies (El Salvador joined 1996). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (1996)",
        "timeline": "3-5 weeks standard",
        "dest_key": "el-salvador",
    },
    "honduras": {
        "name": "Honduras",
        "slug": "honduras",
        "airport": "Palmerola International Airport (XPL), roughly 60km northwest of Tegucigalpa, the country's international cargo and passenger gateway since December 2021",
        "reception": "The Honduran funeral director takes custody at the cargo terminal at Palmerola International Airport (XPL). Palmerola replaced Tegucigalpa's old Toncontin Airport for all international commercial flights from December 2021; Toncontin now handles domestic traffic only. Death is registered with the RNP (Registro Nacional de las Personas). Honduras is a Hague Apostille Convention member since 30 September 2004. Death certificates are issued in Spanish.",
        "consular_note": "There is no British Embassy in Honduras. The British Embassy in Guatemala City handles relations with Honduras and can advise on documentation. Hague Apostille applies (Honduras joined 2004). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2004)",
        "timeline": "3-5 weeks standard",
        "dest_key": "honduras",
    },
    "nicaragua": {
        "name": "Nicaragua",
        "slug": "nicaragua",
        "airport": "Augusto C. Sandino International Airport (MGA), Managua",
        "reception": "The Nicaraguan funeral director takes custody at the cargo terminal at Augusto C. Sandino International Airport (MGA), Managua. Death is registered with the Registro del Estado Civil de las Personas at the Central Registry in Managua or the local registry office where the death occurred. Nicaragua is a Hague Apostille Convention member since 14 May 2013. Death certificates are issued in Spanish.",
        "consular_note": "There is no British Embassy in Managua; a British Honorary Consulate operates there by appointment. The British Embassy in San Jose, Costa Rica, holds overall responsibility for Nicaragua and can advise on documentation. Hague Apostille applies (Nicaragua joined 2013). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2013)",
        "timeline": "3-6 weeks standard",
        "dest_key": "nicaragua",
    },
    "paraguay": {
        "name": "Paraguay",
        "slug": "paraguay",
        "airport": "Silvio Pettirossi International Airport (ASU), Asuncion",
        "reception": "The Paraguayan funeral director takes custody at the cargo terminal at Silvio Pettirossi International Airport (ASU), Asuncion. Death must be registered with the Registro del Estado Civil within 24 hours; the acta de defuncion (death certificate) is issued from this registration. Paraguay is a Hague Apostille Convention member since 30 August 2014. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy Asuncion: contact the embassy for documentation guidance. Hague Apostille applies (Paraguay joined 2014). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2014)",
        "timeline": "3-5 weeks standard",
        "dest_key": "paraguay",
    },
    "bolivia": {
        "name": "Bolivia",
        "slug": "bolivia",
        "airport": "El Alto International Airport (LPB), La Paz, or Viru Viru International Airport (VVI), Santa Cruz",
        "reception": "The Bolivian funeral director takes custody at the cargo terminal at El Alto International Airport (LPB) near La Paz or Viru Viru International Airport (VVI) near Santa Cruz, depending on where the receiving family and funeral home are based. Death is registered with SERECI (Servicio de Registro Civico), which sits under the Tribunal Supremo Electoral rather than a justice or health ministry. Bolivia is a Hague Apostille Convention member since 7 May 2018. Death certificates are issued in Spanish and must carry a QR code to be valid.",
        "consular_note": "British Embassy La Paz: contact the embassy for documentation guidance; an honorary consulate in Santa Cruz can also assist. Hague Apostille applies (Bolivia joined 2018). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2018)",
        "timeline": "3-6 weeks standard",
        "dest_key": "bolivia",
    },
    "san-marino": {
        "name": "San Marino",
        "slug": "san-marino",
        "airport": "No commercial airport. The nearest international gateway is Federico Fellini International Airport, Rimini (RMI), Italy, roughly 15km away, with onward transfer by road",
        "reception": "The San Marino funeral director takes custody following arrival via Federico Fellini International Airport in Rimini, Italy, since San Marino has no commercial airport of its own. Death is registered with the Ufficio di Stato Civile (Civil Status Office) in San Marino City. San Marino is a Hague Apostille Convention member since 13 February 1995. Death certificates are issued in Italian.",
        "consular_note": "There is no British Embassy or consulate in San Marino. The British Embassy in Rome, with support from the Consulate-General in Milan, handles consular services for San Marino. Hague Apostille applies (San Marino joined 1995). Because San Marino has no international airport, every air cargo route runs via Rimini, Italy, followed by a short road transfer.",
        "apostille": "Hague Apostille (1995)",
        "timeline": "2-3 weeks standard",
        "dest_key": "san-marino",
    },
    "liechtenstein": {
        "name": "Liechtenstein",
        "slug": "liechtenstein",
        "airport": "No commercial airport. The nearest international gateway is Zurich Airport (ZRH), Switzerland, roughly 120km away, with onward transfer by road",
        "reception": "The Liechtenstein funeral director takes custody following arrival via Zurich Airport in Switzerland, since Liechtenstein has no commercial airport of its own. Death is registered with the Zivilstandsamt (Civil Registry Office) in Vaduz. Liechtenstein is a Hague Apostille Convention member since 1972. Death certificates are issued in German.",
        "consular_note": "There is no British Embassy in Liechtenstein. The British Embassy in Bern, Switzerland, handles consular services for Liechtenstein. Hague Apostille applies (Liechtenstein joined 1972). Because Liechtenstein has no international airport, every air cargo route runs via Zurich, Switzerland, followed by a road transfer.",
        "apostille": "Hague Apostille (1972)",
        "timeline": "2-3 weeks standard",
        "dest_key": "liechtenstein",
    },
    "saint-kitts-and-nevis": {
        "name": "Saint Kitts and Nevis",
        "slug": "saint-kitts-and-nevis",
        "airport": "Robert L. Bradshaw International Airport (SKB), Basseterre, Saint Kitts",
        "reception": "The funeral director in Saint Kitts and Nevis takes custody at the cargo terminal at Robert L. Bradshaw International Airport (SKB), Basseterre. Death is registered with the Registrar General's Office on Saint Kitts or the Registrar General Department on Nevis, island-specific civil registries. Saint Kitts and Nevis has been a Hague Apostille Convention member since 14 December 1994. Death certificates are issued in English.",
        "consular_note": "There is no resident British High Commission in Saint Kitts and Nevis; an honorary British consul is in place, with full consular support from the British High Commission in Bridgetown, Barbados, which covers the Eastern Caribbean. Hague Apostille applies (Saint Kitts and Nevis joined 1994).",
        "apostille": "Hague Apostille (1994)",
        "timeline": "2-4 weeks standard",
        "dest_key": "saint-kitts-and-nevis",
    },
    "saint-vincent-and-the-grenadines": {
        "name": "Saint Vincent and the Grenadines",
        "slug": "saint-vincent-and-the-grenadines",
        "airport": "Argyle International Airport (SVD), Saint Vincent",
        "reception": "The funeral director in Saint Vincent and the Grenadines takes custody at the cargo terminal at Argyle International Airport (SVD). Death must be registered within three days with the Civil Registry Department (Registrar General), based at the High Court in Kingstown. Saint Vincent and the Grenadines has been a Hague Apostille Convention member since 27 October 1979. Death certificates are issued in English.",
        "consular_note": "A British High Commission office exists in Kingstown but does not itself provide consular services; these come from the British High Commission in Bridgetown, Barbados. Hague Apostille applies (Saint Vincent and the Grenadines joined 1979).",
        "apostille": "Hague Apostille (1979)",
        "timeline": "2-4 weeks standard",
        "dest_key": "saint-vincent-and-the-grenadines",
    },
    "dominica": {
        "name": "Dominica",
        "slug": "dominica",
        "airport": "Douglas-Charles Airport (DOM), on Dominica's northeast coast",
        "reception": "The funeral director in Dominica takes custody at the cargo terminal at Douglas-Charles Airport (DOM). Death is registered with the Registry Department (Births, Marriages and Deaths section) in Roseau. Dominica has been a Hague Apostille Convention member since 3 November 1978. Death certificates are issued in English.",
        "consular_note": "There is no resident British High Commission in Dominica. The British High Commission in Bridgetown, Barbados, covers Dominica and the wider Eastern Caribbean. Hague Apostille applies (Dominica, member since 1978).",
        "apostille": "Hague Apostille (1978)",
        "timeline": "2-4 weeks standard",
        "dest_key": "dominica",
    },
    "suriname": {
        "name": "Suriname",
        "slug": "suriname",
        "airport": "Johan Adolf Pengel International Airport (PBM), Paramaribo",
        "reception": "The funeral director in Suriname takes custody at the cargo terminal at Johan Adolf Pengel International Airport (PBM), Paramaribo. Death is registered with the Centraal Bureau voor Burgerzaken (CBB), the Central Bureau of Civil Affairs, which runs 42 field offices across 10 districts. Suriname has been a Hague Apostille Convention member since 25 November 1975. The death certificate, the Overlijdens Akte, is issued in Dutch and does not record a cause of death.",
        "consular_note": "There is no resident British embassy in Suriname. The British High Commission in Georgetown, Guyana, covers Suriname, supported by an honorary British consul in Paramaribo. Hague Apostille applies (Suriname, member since 1975).",
        "apostille": "Hague Apostille (1975)",
        "timeline": "2-5 weeks standard",
        "dest_key": "suriname",
    },
    "cabo-verde": {
        "name": "Cabo Verde",
        "slug": "cabo-verde",
        "hub_slug": "cape-verde",
        "airport": "Amilcar Cabral International Airport (SID), Sal Island, Cabo Verde's main international gateway",
        "reception": "The funeral director in Cabo Verde takes custody at the cargo terminal at Amilcar Cabral International Airport (SID) on Sal Island. Death is registered with the local Conservatoria do Registo Civil (Civil Registration Office), under the Direcao-Geral dos Registos, Notariado e Identificacao. Cabo Verde has been a Hague Apostille Convention member since 13 February 2010. Death certificates are issued in Portuguese.",
        "consular_note": "There is no resident British embassy in Cabo Verde. The British Embassy in Lisbon, Portugal, covers Cabo Verde and can advise on documentation. Hague Apostille applies (Cabo Verde, member since 2010).",
        "apostille": "Hague Apostille (2010)",
        "timeline": "3-5 weeks standard",
        "dest_key": "cabo-verde",
    },
    "seychelles": {
        "name": "Seychelles",
        "slug": "seychelles",
        "airport": "Seychelles International Airport (SEZ), Mahe",
        "reception": "The funeral director in Seychelles takes custody at the cargo terminal at Seychelles International Airport (SEZ), Mahe. Death must be declared within 24 hours to the Civil Status Division, under the Department of Immigration and Civil Status, along with a Medical Certificate from a Medical Officer. Seychelles has been a Hague Apostille Convention member since 31 March 1979. Death certificates are issued in English, French, or Seychellois Creole.",
        "consular_note": "The British High Commission in Victoria, Mahe, is resident in Seychelles and provides consular assistance directly, unlike several neighbouring island nations. Hague Apostille applies (Seychelles, member since 1979).",
        "apostille": "Hague Apostille (1979)",
        "timeline": "2-4 weeks standard",
        "dest_key": "seychelles",
    },
}

# ---------------------------------------------------------------------------
# Route definitions -- exact missing origin/destination combinations,
# confirmed by a direct filesystem check of site/content/routes/ against
# the 8-origin pool before this chunk was generated.
# ---------------------------------------------------------------------------

# R113: starts at template C (index 2). 25 routes.
R113_ROUTES = [
    ("netherlands", "monaco"),
    ("france", "costa-rica"),
    ("italy", "costa-rica"),
    ("belgium", "costa-rica"),
    ("norway", "uruguay"),
    ("sweden", "uruguay"),
    ("belgium", "uruguay"),
    ("australia", "panama"),
    ("norway", "panama"),
    ("belgium", "panama"),
    ("france", "guatemala"),
    ("netherlands", "guatemala"),
    ("italy", "guatemala"),
    ("norway", "el-salvador"),
    ("sweden", "el-salvador"),
    ("belgium", "el-salvador"),
    ("australia", "honduras"),
    ("canada", "honduras"),
    ("italy", "honduras"),
    ("france", "nicaragua"),
    ("netherlands", "nicaragua"),
    ("belgium", "nicaragua"),
    ("australia", "paraguay"),
    ("norway", "paraguay"),
    ("sweden", "paraguay"),
]

# R114: starts at template C (index 2), continuing seamlessly from R113
# (25 is a multiple of 5, so the rotation index does not shift). 25 routes.
R114_ROUTES = [
    ("canada", "bolivia"),
    ("italy", "bolivia"),
    ("belgium", "bolivia"),
    ("france", "san-marino"),
    ("netherlands", "san-marino"),
    ("sweden", "san-marino"),
    ("australia", "liechtenstein"),
    ("norway", "liechtenstein"),
    ("belgium", "liechtenstein"),
    ("italy", "saint-kitts-and-nevis"),
    ("norway", "saint-kitts-and-nevis"),
    ("belgium", "saint-kitts-and-nevis"),
    ("france", "saint-vincent-and-the-grenadines"),
    ("netherlands", "saint-vincent-and-the-grenadines"),
    ("sweden", "saint-vincent-and-the-grenadines"),
    ("australia", "dominica"),
    ("norway", "dominica"),
    ("belgium", "dominica"),
    ("canada", "suriname"),
    ("italy", "suriname"),
    ("sweden", "suriname"),
    ("australia", "cabo-verde"),
    ("france", "cabo-verde"),
    ("netherlands", "cabo-verde"),
    ("norway", "seychelles"),
]

# ---------------------------------------------------------------------------
# Varied title shapes, description openings (burstiness and
# anti-template-footprint measures per CLAUDE.md canonical constants)
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
    """Generate destination consular note. No-op replace when the older
    {origin_country} placeholder style is not present in the string."""
    return dest_data["consular_note"].replace("{origin_country}", origin_name)


DEST_CONSULAR_LINES = {
    "monaco": lambda origin: f"Notify the Consulate of Monaco in {origin}. Hague Apostille applies (2002). Route via Nice, France, since Monaco has no commercial airport.",
    "costa-rica": lambda origin: f"Notify the Embassy of Costa Rica in {origin}. Hague Apostille applies (2011).",
    "uruguay": lambda origin: "Notify the British Embassy Montevideo. Hague Apostille applies (Uruguay joined 2012).",
    "panama": lambda origin: "Notify the British Embassy Panama City. Hague Apostille applies (Panama joined 1991).",
    "guatemala": lambda origin: "Notify the British Embassy Guatemala City. Hague Apostille applies (Guatemala joined 2017).",
    "el-salvador": lambda origin: "Notify the British Embassy San Salvador. Hague Apostille applies (El Salvador joined 1996).",
    "honduras": lambda origin: "Notify the British Embassy Guatemala City, which covers Honduras (there is no resident British Embassy). Hague Apostille applies (Honduras joined 2004).",
    "nicaragua": lambda origin: "Notify the British Embassy San Jose, Costa Rica, which holds overall responsibility for Nicaragua; a British Honorary Consulate in Managua can also assist. Hague Apostille applies (Nicaragua joined 2013).",
    "paraguay": lambda origin: "Notify the British Embassy Asuncion. Hague Apostille applies (Paraguay joined 2014).",
    "bolivia": lambda origin: "Notify the British Embassy La Paz, or the honorary consulate in Santa Cruz. Hague Apostille applies (Bolivia joined 2018).",
    "san-marino": lambda origin: "Notify the British Embassy Rome, with support from the Consulate-General in Milan. Hague Apostille applies (San Marino joined 1995). Route via Rimini, Italy, since San Marino has no commercial airport.",
    "liechtenstein": lambda origin: "Notify the British Embassy Bern, Switzerland. Hague Apostille applies (Liechtenstein joined 1972). Route via Zurich, Switzerland, since Liechtenstein has no commercial airport.",
    "saint-kitts-and-nevis": lambda origin: "Notify the honorary British consul, or the British High Commission Bridgetown, Barbados. Hague Apostille applies (Saint Kitts and Nevis joined 1994).",
    "saint-vincent-and-the-grenadines": lambda origin: "Notify the British High Commission Bridgetown, Barbados (the Kingstown office does not handle consular casework). Hague Apostille applies (Saint Vincent and the Grenadines joined 1979).",
    "dominica": lambda origin: "Notify the British High Commission Bridgetown, Barbados. Hague Apostille applies (Dominica joined 1978).",
    "suriname": lambda origin: "Notify the British High Commission Georgetown, Guyana, or the honorary British consul in Paramaribo. Hague Apostille applies (Suriname joined 1975).",
    "cabo-verde": lambda origin: "Notify the British Embassy Lisbon, Portugal. Hague Apostille applies (Cabo Verde joined 2010).",
    "seychelles": lambda origin: "Notify the British High Commission Victoria, Mahe, which is resident and provides consular assistance directly. Hague Apostille applies (Seychelles joined 1979).",
}

DEST_RECEPTION_STEPS = {
    "monaco": "Monegasque funeral director takes custody following arrival via Nice Cote d'Azur Airport (NCE) and a short road transfer, since Monaco has no commercial airport of its own. Etat Civil at the Mairie de Monaco notified. Death certificate issued in French.",
    "costa-rica": "Costa Rican funeral director takes custody at cargo terminal at Juan Santamaria International Airport (SJO), San Jose. Registro Civil, part of the Tribunal Supremo de Elecciones, notified. Death certificate issued in Spanish.",
    "uruguay": "Uruguayan funeral director takes custody at cargo terminal at Carrasco International Airport (MVD), Montevideo. Direccion General del Registro de Estado Civil notified. Death certificate issued in Spanish.",
    "panama": "Panamanian funeral director takes custody at cargo terminal at Tocumen International Airport (PTY), Panama City. Direccion Nacional del Registro Civil (Tribunal Electoral) notified. Death certificate issued in Spanish.",
    "guatemala": "Guatemalan funeral director takes custody at cargo terminal at La Aurora International Airport (GUA), Guatemala City. RENAP (Registro Nacional de las Personas) notified. Death certificate issued in Spanish with a QR verification code.",
    "el-salvador": "Salvadoran funeral director takes custody at cargo terminal at El Salvador International Airport (SAL). Municipal civil registry notified; RNPN handles authentication of the certificate for use abroad. Death certificate issued in Spanish.",
    "honduras": "Honduran funeral director takes custody at cargo terminal at Palmerola International Airport (XPL), roughly 60km from Tegucigalpa, the international gateway since Toncontin stopped handling commercial flights in December 2021. RNP (Registro Nacional de las Personas) notified. Death certificate issued in Spanish.",
    "nicaragua": "Nicaraguan funeral director takes custody at cargo terminal at Augusto C. Sandino International Airport (MGA), Managua. Registro del Estado Civil de las Personas notified. Death certificate issued in Spanish.",
    "paraguay": "Paraguayan funeral director takes custody at cargo terminal at Silvio Pettirossi International Airport (ASU), Asuncion. Registro del Estado Civil notified. Registration is required within 24 hours by Paraguayan law. Death certificate issued in Spanish.",
    "bolivia": "Bolivian funeral director takes custody at cargo terminal at El Alto International Airport (LPB), La Paz, or Viru Viru International Airport (VVI), Santa Cruz, depending on family location. SERECI (Tribunal Supremo Electoral) notified. Death certificate issued in Spanish with a QR code.",
    "san-marino": "San Marino funeral director takes custody following arrival via Federico Fellini International Airport (RMI) in Rimini, Italy, and a short road transfer, since San Marino has no commercial airport of its own. Ufficio di Stato Civile notified. Death certificate issued in Italian.",
    "liechtenstein": "Liechtenstein funeral director takes custody following arrival via Zurich Airport (ZRH) in Switzerland and a road transfer, since Liechtenstein has no commercial airport of its own. Zivilstandsamt (Civil Registry Office) in Vaduz notified. Death certificate issued in German.",
    "saint-kitts-and-nevis": "Funeral director in Saint Kitts and Nevis takes custody at the cargo terminal at Robert L. Bradshaw International Airport (SKB), Basseterre. Registrar General's Office notified. Death certificate issued in English.",
    "saint-vincent-and-the-grenadines": "Funeral director in Saint Vincent and the Grenadines takes custody at the cargo terminal at Argyle International Airport (SVD). Civil Registry Department notified. Death certificate issued in English.",
    "dominica": "Funeral director in Dominica takes custody at the cargo terminal at Douglas-Charles Airport (DOM). Registry Department notified. Death certificate issued in English.",
    "suriname": "Funeral director in Suriname takes custody at the cargo terminal at Johan Adolf Pengel International Airport (PBM), Paramaribo. Centraal Bureau voor Burgerzaken notified. Death certificate (Overlijdens Akte) issued in Dutch.",
    "cabo-verde": "Funeral director in Cabo Verde takes custody at the cargo terminal at Amilcar Cabral International Airport (SID), Sal Island. Conservatoria do Registo Civil notified. Death certificate issued in Portuguese.",
    "seychelles": "Funeral director in Seychelles takes custody at the cargo terminal at Seychelles International Airport (SEZ), Mahe. Civil Status Division notified. Death certificate issued in English, French, or Seychellois Creole.",
}


def make_timeline_steps(origin_data, dest_data):
    """Generate 7 timeline steps appropriate to the corridor."""
    origin = origin_data["name"]
    dest_airport = dest_data["airport"]
    cert = origin_data["death_cert"]
    doc_time = origin_data["doc_processing"]
    dest_key = dest_data["dest_key"]

    consular_fn = DEST_CONSULAR_LINES.get(dest_key, lambda o: f"Notify the {dest_data['name']} Embassy in {o}.")
    consular = consular_fn(origin)
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
    "monaco": lambda origin: {
        "question": f"How does a repatriation from {origin} actually reach Monaco, given it has no airport?",
        "answer": (
            "Monaco has no commercial airport of its own. "
            "Every air cargo repatriation to Monaco lands at Nice Cote d'Azur Airport (NCE) in neighbouring France, followed by a short road transfer across the border. "
            "Monaco is a Hague Apostille member since 31 December 2002, and death is registered with the Etat Civil at the Mairie de Monaco once the body arrives."
        ),
    },
    "costa-rica": lambda origin: {
        "question": f"Which government body registers a death for repatriation from {origin} to Costa Rica?",
        "answer": (
            "Costa Rican civil registration, including death certificates, runs through the Registro Civil, which sits under the Tribunal Supremo de Elecciones, "
            "the country's electoral authority, rather than a justice or interior ministry as in most countries. "
            "Costa Rica joined the Hague Apostille Convention in 2011, and apostille certification is issued separately by the Ministry of Foreign Affairs and Worship in San Jose."
        ),
    },
    "uruguay": lambda origin: {
        "question": f"Is Uruguay a Hague Apostille member and how does this affect repatriation from {origin}?",
        "answer": (
            "Uruguay is a Hague Apostille Convention member since 14 October 2012. "
            "Death registration runs through the Direccion General del Registro de Estado Civil, part of the Ministry of Education and Culture. "
            f"Certified translation of documents from {origin} into Spanish is typically required by the receiving Uruguayan registry."
        ),
    },
    "panama": lambda origin: {
        "question": f"Which authority issues a Panamanian death certificate for a repatriation from {origin}?",
        "answer": (
            "Civil registration in Panama, including death certificates, runs through the Direccion Nacional del Registro Civil, "
            "a department of the Tribunal Electoral (Electoral Tribunal) created in 1974, rather than a justice or health ministry. "
            "Panama is a Hague Apostille member since 1991, and certificates can be obtained from any provincial branch office, not only in Panama City."
        ),
    },
    "guatemala": lambda origin: {
        "question": f"How is a Guatemalan death certificate verified for a repatriation from {origin}?",
        "answer": (
            "RENAP (Registro Nacional de las Personas), Guatemala's national civil registry, issues death certificates that carry a QR code "
            "which can be scanned or checked on RENAP's validation page to confirm authenticity. "
            f"Guatemala is a Hague Apostille member since 2017. RENAP also covers Honduras' documentation questions through the same regional British Embassy in Guatemala City."
        ),
    },
    "el-salvador": lambda origin: {
        "question": f"Does the municipality or a national body issue the death certificate for repatriation from {origin} to El Salvador?",
        "answer": (
            "Both, at different stages. The municipality where the death occurred issues the original partida de defuncion. "
            "The RNPN (Registro Nacional de las Personas Naturales), the national identity registry, then authenticates that certificate for use outside El Salvador. "
            "El Salvador is a Hague Apostille member since 1996, and this authentication step is required before the certificate can support a repatriation case."
        ),
    },
    "honduras": lambda origin: {
        "question": f"Which airport actually receives a repatriation from {origin} to Honduras now?",
        "answer": (
            "Palmerola International Airport (XPL), roughly 60km northwest of Tegucigalpa, has handled all international commercial flights to the capital since December 2021, "
            "when the older Toncontin Airport in the city itself stopped taking international traffic and switched to domestic flights only. "
            "Honduras has no resident British Embassy; the British Embassy in Guatemala City covers documentation queries for Honduras."
        ),
    },
    "nicaragua": lambda origin: {
        "question": f"Who provides British consular support for a repatriation from {origin} to Nicaragua?",
        "answer": (
            "There is no British Embassy in Managua. Overall responsibility for Nicaragua sits with the British Embassy in San Jose, Costa Rica, "
            "though a British Honorary Consulate in Managua's Residencial Bolonia area can assist by appointment. "
            "Nicaragua is a Hague Apostille member since 14 May 2013."
        ),
    },
    "paraguay": lambda origin: {
        "question": f"How quickly must a death be registered in Paraguay for a repatriation from {origin}?",
        "answer": (
            "Paraguayan law requires death registration with the Registro del Estado Civil within 24 hours, faster than most comparable countries. "
            "A certified copy of the resulting acta de defuncion typically takes 3 to 10 business days to issue. "
            "Paraguay is a Hague Apostille member since 30 August 2014."
        ),
    },
    "bolivia": lambda origin: {
        "question": f"Which city receives a repatriation from {origin} to Bolivia?",
        "answer": (
            "It depends on where the family is based: El Alto International Airport (LPB) serves La Paz, and Viru Viru International Airport (VVI) serves Santa Cruz, "
            "Bolivia's largest city. Bolivia is a Hague Apostille member since 7 May 2018, and current SERECI death certificates must carry a QR code to be considered valid."
        ),
    },
    "san-marino": lambda origin: {
        "question": f"How does a repatriation from {origin} actually reach San Marino, given it has no airport?",
        "answer": (
            "San Marino has no commercial airport of its own. "
            "Every air cargo repatriation lands at Federico Fellini International Airport in Rimini, Italy, roughly 15km away, followed by a short road transfer across the border. "
            "There is also no resident British Embassy; consular support for San Marino comes from the British Embassy in Rome and the Consulate-General in Milan."
        ),
    },
    "liechtenstein": lambda origin: {
        "question": f"How does a repatriation from {origin} actually reach Liechtenstein, given it has no airport?",
        "answer": (
            "Liechtenstein has no commercial airport of its own. "
            "Every air cargo repatriation lands at Zurich Airport in Switzerland, roughly 120km away, followed by a road transfer to Vaduz. "
            "There is also no resident British Embassy; consular support for Liechtenstein comes from the British Embassy in Bern."
        ),
    },
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

    # All destinations in this batch already exist in the matrix with 5 of
    # 8 origins built, so sideways links point to the two Tier A routes
    # guaranteed to exist for every origin in the pool: origin-to-UK and
    # origin-to-Ireland.
    sideways = (
        f"/routes/{origin_key}-to-united-kingdom/", f"Repatriation from {o['name']} to the UK",
        f"/routes/{origin_key}-to-ireland/", f"Repatriation from {o['name']} to Ireland",
    )

    timeline_steps = make_timeline_steps(o, d)
    faqs = make_faqs(o, d)

    origin_hub_url = f"/repatriation-from-{origin_key}/"
    dest_hub_url = f"/repatriation-from-{d.get('hub_slug', dest_key)}/"

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
    lines.append(f'date: 2026-07-09')
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
    lines.append(f'      text: "Full {d["name"]} repatriation guide"')
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
        ("R113", R113_ROUTES, 2),  # Start at C (index 2), 25 routes
        ("R114", R114_ROUTES, 2),  # Start at C (index 2), continues seamlessly (25 is a multiple of 5)
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
