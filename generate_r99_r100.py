#!/usr/bin/env python3
"""
generate_r99_r100.py -- Repatriate Service Route Generator
Chunks R99 and R100: 50 Tier C route pages, introducing ten new destinations.
R99: Uruguay x5, Panama x5, Guatemala x5, El Salvador x5, Honduras x5
R100: Nicaragua x5, Paraguay x5, Bolivia x5, San Marino x5, Liechtenstein x5
Origins: Australia, France, Canada, Netherlands, Italy, Norway, Sweden, Belgium (established Tier C origin pool).
Template variants: Both R99 and R100 start at C (index 2), continuing rotation from R98 (ended on B).
Sources for new destination facts: HCCH Apostille status table (hcch.net, checked July 2026), national civil
registry authority sites (RENAP Guatemala, RNPN/RNP El Salvador and Honduras, SERECI Bolivia, Registro del
Estado Civil Paraguay and Uruguay and Nicaragua, Tribunal Electoral Panama, Ufficio di Stato Civile San Marino,
Zivilstandsamt Liechtenstein), GOV.UK "British Embassy" world-organisation pages, all checked July 2026.
"""

import os
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")
ROUTES_DIR.mkdir(parents=True, exist_ok=True)

VARIANTS = ["A", "B", "C", "D", "E"]

# ---------------------------------------------------------------------------
# Origin data (reused verbatim from the established Tier C origin pool,
# generate_r97_r98.py)
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
        "translation_note": "Death certificates are issued in English or French depending on the province. Certified translation is required for non-English and non-French-speaking destinations.",
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
        "translation_note": "Death certificates are issued in French, Dutch, or German depending on region. Certified translation is required for non-Belgian language destinations.",
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
# Destination data -- ten new Tier C destinations
# ---------------------------------------------------------------------------

DEST_META = {
    "uruguay": {
        "name": "Uruguay",
        "slug": "uruguay",
        "display_name": "Uruguay",
        "airport": "Carrasco International Airport (MVD), Montevideo",
        "reception": "The Uruguayan funeral director takes custody at the cargo terminal at Carrasco International Airport (MVD) near Montevideo. Death is registered with the Direccion General del Registro de Estado Civil, the national civil registry under the Ministry of Education and Culture. Uruguay is a Hague Apostille Convention member since 14 October 2012. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy Montevideo: contact the embassy for documentation guidance. Hague Apostille applies (Uruguay joined 2012). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2012)",
        "timeline": "3-5 weeks standard",
        "dest_key": "uruguay",
        "country_note": "Uruguay is a Hague Apostille member since 14 October 2012. Death registration runs through the Direccion General del Registro de Estado Civil, and Montevideo has offered free digital certified copies of death records since 2013, which can speed up the documentation stage.",
    },
    "panama": {
        "name": "Panama",
        "slug": "panama",
        "display_name": "Panama",
        "airport": "Tocumen International Airport (PTY), Panama City",
        "reception": "The Panamanian funeral director takes custody at the cargo terminal at Tocumen International Airport (PTY), Panama City. Death is registered with the Direccion Nacional del Registro Civil, a department of the Tribunal Electoral (Electoral Tribunal) established in 1974, with civil registry offices in every provincial capital. Panama is a Hague Apostille Convention member since 4 August 1991. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy Panama City: contact the embassy for documentation guidance. Hague Apostille applies (Panama joined 1991). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (1991)",
        "timeline": "2-4 weeks standard",
        "dest_key": "panama",
        "country_note": "Panama is a Hague Apostille member since 4 August 1991, one of the longest-standing memberships in Central America. Civil registration, including death certificates, runs through the Tribunal Electoral rather than a justice or health ministry, and certificates can be obtained from any provincial branch office.",
    },
    "guatemala": {
        "name": "Guatemala",
        "slug": "guatemala",
        "display_name": "Guatemala",
        "airport": "La Aurora International Airport (GUA), Guatemala City",
        "reception": "The Guatemalan funeral director takes custody at the cargo terminal at La Aurora International Airport (GUA), Guatemala City. Death is registered with RENAP (Registro Nacional de las Personas), the national civil registry that also issues the country's national ID. Guatemala is a Hague Apostille Convention member since 18 September 2017. Death certificates are issued in Spanish and carry a QR verification code.",
        "consular_note": "British Embassy Guatemala City: contact the embassy for documentation guidance. This embassy also covers Honduras. Hague Apostille applies (Guatemala joined 2017). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2017)",
        "timeline": "3-5 weeks standard",
        "dest_key": "guatemala",
        "country_note": "Guatemala is a Hague Apostille member since 18 September 2017, one of the more recent accessions in the region. RENAP death certificates carry a QR code that can be scanned to verify authenticity, which can speed up acceptance by receiving authorities abroad.",
    },
    "el-salvador": {
        "name": "El Salvador",
        "slug": "el-salvador",
        "display_name": "El Salvador",
        "airport": "El Salvador International Airport (SAL), also known as Comalapa, near San Salvador",
        "reception": "The Salvadoran funeral director takes custody at the cargo terminal at El Salvador International Airport (SAL). Death is registered at the municipal civil registry office (registro del estado familiar) where the death occurred. Authentication of the death certificate for use abroad is handled separately by the RNPN (Registro Nacional de las Personas Naturales). El Salvador is a Hague Apostille Convention member since 31 May 1996. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy San Salvador: contact the embassy for documentation guidance. Hague Apostille applies (El Salvador joined 1996). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (1996)",
        "timeline": "3-5 weeks standard",
        "dest_key": "el-salvador",
        "country_note": "El Salvador is a Hague Apostille member since 31 May 1996. The death certificate itself is issued by the municipality where the death was registered, but authentication for use outside the country is a separate step handled by the RNPN, the national identity registry.",
    },
    "honduras": {
        "name": "Honduras",
        "slug": "honduras",
        "display_name": "Honduras",
        "airport": "Palmerola International Airport (XPL), roughly 60km northwest of Tegucigalpa, the country's international cargo and passenger gateway since December 2021",
        "reception": "The Honduran funeral director takes custody at the cargo terminal at Palmerola International Airport (XPL). Palmerola replaced Tegucigalpa's old Toncontin Airport for all international commercial flights from December 2021; Toncontin now handles domestic traffic only. Death is registered with the RNP (Registro Nacional de las Personas). Honduras is a Hague Apostille Convention member since 30 September 2004. Death certificates are issued in Spanish.",
        "consular_note": "There is no British Embassy in Honduras. The British Embassy in Guatemala City handles relations with Honduras and can advise on documentation. Hague Apostille applies (Honduras joined 2004). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2004)",
        "timeline": "3-5 weeks standard",
        "dest_key": "honduras",
        "country_note": "A repatriation to Tegucigalpa now lands at Palmerola International Airport (XPL), about 60km from the city, not the old Toncontin Airport, which stopped handling international commercial flights in December 2021. Families researching an older route may still expect Toncontin; confirming the current airport avoids delay at the reception end. Honduras has no resident British Embassy; consular support comes from Guatemala City.",
    },
    "nicaragua": {
        "name": "Nicaragua",
        "slug": "nicaragua",
        "display_name": "Nicaragua",
        "airport": "Augusto C. Sandino International Airport (MGA), Managua",
        "reception": "The Nicaraguan funeral director takes custody at the cargo terminal at Augusto C. Sandino International Airport (MGA), Managua. Death is registered with the Registro del Estado Civil de las Personas at the Central Registry in Managua or the local registry office where the death occurred. Nicaragua is a Hague Apostille Convention member since 14 May 2013. Death certificates are issued in Spanish.",
        "consular_note": "There is no British Embassy in Managua; a British Honorary Consulate operates there by appointment. The British Embassy in San Jose, Costa Rica, holds overall responsibility for Nicaragua and can advise on documentation. Hague Apostille applies (Nicaragua joined 2013). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2013)",
        "timeline": "3-6 weeks standard",
        "dest_key": "nicaragua",
        "country_note": "Nicaragua has no British Embassy. Consular responsibility sits with the British Embassy in San Jose, Costa Rica, though a British Honorary Consulate in Managua can assist by appointment. Nicaragua is a Hague Apostille member since 14 May 2013, and death certificates can be requested either where the death was registered or at the Central Registry in Managua.",
    },
    "paraguay": {
        "name": "Paraguay",
        "slug": "paraguay",
        "display_name": "Paraguay",
        "airport": "Silvio Pettirossi International Airport (ASU), Asuncion",
        "reception": "The Paraguayan funeral director takes custody at the cargo terminal at Silvio Pettirossi International Airport (ASU), Asuncion. Death must be registered with the Registro del Estado Civil within 24 hours; the acta de defuncion (death certificate) is issued from this registration. Paraguay is a Hague Apostille Convention member since 30 August 2014. Death certificates are issued in Spanish.",
        "consular_note": "British Embassy Asuncion: contact the embassy for documentation guidance. Hague Apostille applies (Paraguay joined 2014). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2014)",
        "timeline": "3-5 weeks standard",
        "dest_key": "paraguay",
        "country_note": "Paraguay is a Hague Apostille member since 30 August 2014. Registration of a death is required within 24 hours by law, faster than most Tier C destinations, though a certified copy of the resulting acta de defuncion typically still takes 3 to 10 business days to issue.",
    },
    "bolivia": {
        "name": "Bolivia",
        "slug": "bolivia",
        "display_name": "Bolivia",
        "airport": "El Alto International Airport (LPB), La Paz, or Viru Viru International Airport (VVI), Santa Cruz",
        "reception": "The Bolivian funeral director takes custody at the cargo terminal at El Alto International Airport (LPB) near La Paz or Viru Viru International Airport (VVI) near Santa Cruz, depending on where the receiving family and funeral home are based. Death is registered with SERECI (Servicio de Registro Civico), which sits under the Tribunal Supremo Electoral rather than a justice or health ministry. Bolivia is a Hague Apostille Convention member since 7 May 2018. Death certificates are issued in Spanish and must carry a QR code to be valid.",
        "consular_note": "British Embassy La Paz: contact the embassy for documentation guidance; an honorary consulate in Santa Cruz can also assist. Hague Apostille applies (Bolivia joined 2018). Certified translation into the destination language is required outside Spanish-speaking countries.",
        "apostille": "Hague Apostille (2018)",
        "timeline": "3-6 weeks standard",
        "dest_key": "bolivia",
        "country_note": "Bolivia is a Hague Apostille member since 7 May 2018, one of the most recent accessions in South America. Civil registration runs through SERECI under the Tribunal Supremo Electoral, the electoral authority, and current death certificates must carry a QR code for validity. Reception can be at either of two major airports, La Paz or Santa Cruz, depending on the family's location.",
    },
    "san-marino": {
        "name": "San Marino",
        "slug": "san-marino",
        "display_name": "San Marino",
        "airport": "No commercial airport. The nearest international gateway is Federico Fellini International Airport, Rimini (RMI), Italy, roughly 15km away, with onward transfer by road",
        "reception": "The San Marino funeral director takes custody following arrival via Federico Fellini International Airport in Rimini, Italy, since San Marino has no commercial airport of its own. Death is registered with the Ufficio di Stato Civile (Civil Status Office) in San Marino City. San Marino is a Hague Apostille Convention member since 13 February 1995. Death certificates are issued in Italian.",
        "consular_note": "There is no British Embassy or consulate in San Marino. The British Embassy in Rome, with support from the Consulate-General in Milan, handles consular services for San Marino. Hague Apostille applies (San Marino joined 1995). Because San Marino has no international airport, every air cargo route runs via Rimini, Italy, followed by a short road transfer.",
        "apostille": "Hague Apostille (1995)",
        "timeline": "2-3 weeks standard",
        "dest_key": "san-marino",
        "country_note": "San Marino has no commercial airport, so every repatriation there routes through Federico Fellini International Airport in Rimini, Italy, with a short road transfer to complete the journey. There is also no resident British Embassy; consular support comes from the British Embassy in Rome and the Consulate-General in Milan.",
    },
    "liechtenstein": {
        "name": "Liechtenstein",
        "slug": "liechtenstein",
        "display_name": "Liechtenstein",
        "airport": "No commercial airport. The nearest international gateway is Zurich Airport (ZRH), Switzerland, roughly 120km away, with onward transfer by road",
        "reception": "The Liechtenstein funeral director takes custody following arrival via Zurich Airport in Switzerland, since Liechtenstein has no commercial airport of its own. Death is registered with the Zivilstandsamt (Civil Registry Office) in Vaduz. Liechtenstein is a Hague Apostille Convention member since 1972. Death certificates are issued in German.",
        "consular_note": "There is no British Embassy in Liechtenstein. The British Embassy in Bern, Switzerland, handles consular services for Liechtenstein. Hague Apostille applies (Liechtenstein joined 1972). Because Liechtenstein has no international airport, every air cargo route runs via Zurich, Switzerland, followed by a road transfer.",
        "apostille": "Hague Apostille (1972)",
        "timeline": "2-3 weeks standard",
        "dest_key": "liechtenstein",
        "country_note": "Liechtenstein has no commercial airport, so every repatriation there routes through Zurich Airport in Switzerland, roughly 120km away, with a road transfer to complete the journey. There is also no resident British Embassy; consular support comes from the British Embassy in Bern.",
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

# R99: starts at template C (index 2). 25 routes.
R99_ROUTES = [
    # Uruguay x5
    ("australia", "uruguay"),
    ("france", "uruguay"),
    ("italy", "uruguay"),
    ("netherlands", "uruguay"),
    ("canada", "uruguay"),
    # Panama x5
    ("canada", "panama"),
    ("france", "panama"),
    ("sweden", "panama"),
    ("netherlands", "panama"),
    ("italy", "panama"),
    # Guatemala x5
    ("australia", "guatemala"),
    ("canada", "guatemala"),
    ("norway", "guatemala"),
    ("belgium", "guatemala"),
    ("sweden", "guatemala"),
    # El Salvador x5
    ("france", "el-salvador"),
    ("italy", "el-salvador"),
    ("netherlands", "el-salvador"),
    ("canada", "el-salvador"),
    ("australia", "el-salvador"),
    # Honduras x5
    ("norway", "honduras"),
    ("sweden", "honduras"),
    ("belgium", "honduras"),
    ("france", "honduras"),
    ("netherlands", "honduras"),
]

# R100: starts at template C (index 2). 25 routes.
R100_ROUTES = [
    # Nicaragua x5
    ("italy", "nicaragua"),
    ("canada", "nicaragua"),
    ("australia", "nicaragua"),
    ("sweden", "nicaragua"),
    ("norway", "nicaragua"),
    # Paraguay x5
    ("netherlands", "paraguay"),
    ("france", "paraguay"),
    ("italy", "paraguay"),
    ("belgium", "paraguay"),
    ("canada", "paraguay"),
    # Bolivia x5
    ("australia", "bolivia"),
    ("norway", "bolivia"),
    ("sweden", "bolivia"),
    ("netherlands", "bolivia"),
    ("france", "bolivia"),
    # San Marino x5
    ("italy", "san-marino"),
    ("belgium", "san-marino"),
    ("canada", "san-marino"),
    ("norway", "san-marino"),
    ("australia", "san-marino"),
    # Liechtenstein x5
    ("france", "liechtenstein"),
    ("sweden", "liechtenstein"),
    ("netherlands", "liechtenstein"),
    ("italy", "liechtenstein"),
    ("canada", "liechtenstein"),
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


def make_timeline_steps(origin_data, dest_data):
    """Generate 7 timeline steps appropriate to the corridor."""
    origin = origin_data["name"]
    dest_airport = dest_data["airport"]
    cert = origin_data["death_cert"]
    doc_time = origin_data["doc_processing"]
    dest_key = dest_data["dest_key"]

    if dest_key == "uruguay":
        consular = f"Notify the British Embassy Montevideo. Hague Apostille applies (Uruguay joined 2012)."
        reception_step = (
            "Uruguayan funeral director takes custody at cargo terminal at Carrasco International Airport (MVD), Montevideo. "
            "Direccion General del Registro de Estado Civil notified. "
            "Death certificate issued in Spanish."
        )
    elif dest_key == "panama":
        consular = f"Notify the British Embassy Panama City. Hague Apostille applies (Panama joined 1991)."
        reception_step = (
            "Panamanian funeral director takes custody at cargo terminal at Tocumen International Airport (PTY), Panama City. "
            "Direccion Nacional del Registro Civil (Tribunal Electoral) notified. "
            "Death certificate issued in Spanish."
        )
    elif dest_key == "guatemala":
        consular = f"Notify the British Embassy Guatemala City. Hague Apostille applies (Guatemala joined 2017)."
        reception_step = (
            "Guatemalan funeral director takes custody at cargo terminal at La Aurora International Airport (GUA), Guatemala City. "
            "RENAP (Registro Nacional de las Personas) notified. "
            "Death certificate issued in Spanish with a QR verification code."
        )
    elif dest_key == "el-salvador":
        consular = f"Notify the British Embassy San Salvador. Hague Apostille applies (El Salvador joined 1996)."
        reception_step = (
            "Salvadoran funeral director takes custody at cargo terminal at El Salvador International Airport (SAL). "
            "Municipal civil registry notified; RNPN handles authentication of the certificate for use abroad. "
            "Death certificate issued in Spanish."
        )
    elif dest_key == "honduras":
        consular = f"Notify the British Embassy Guatemala City, which covers Honduras (there is no resident British Embassy). Hague Apostille applies (Honduras joined 2004)."
        reception_step = (
            "Honduran funeral director takes custody at cargo terminal at Palmerola International Airport (XPL), roughly 60km from Tegucigalpa, "
            "the international gateway since Toncontin stopped handling commercial flights in December 2021. "
            "RNP (Registro Nacional de las Personas) notified. Death certificate issued in Spanish."
        )
    elif dest_key == "nicaragua":
        consular = f"Notify the British Embassy San Jose, Costa Rica, which holds overall responsibility for Nicaragua; a British Honorary Consulate in Managua can also assist. Hague Apostille applies (Nicaragua joined 2013)."
        reception_step = (
            "Nicaraguan funeral director takes custody at cargo terminal at Augusto C. Sandino International Airport (MGA), Managua. "
            "Registro del Estado Civil de las Personas notified. "
            "Death certificate issued in Spanish."
        )
    elif dest_key == "paraguay":
        consular = f"Notify the British Embassy Asuncion. Hague Apostille applies (Paraguay joined 2014)."
        reception_step = (
            "Paraguayan funeral director takes custody at cargo terminal at Silvio Pettirossi International Airport (ASU), Asuncion. "
            "Registro del Estado Civil notified. Registration is required within 24 hours by Paraguayan law. "
            "Death certificate issued in Spanish."
        )
    elif dest_key == "bolivia":
        consular = f"Notify the British Embassy La Paz, or the honorary consulate in Santa Cruz. Hague Apostille applies (Bolivia joined 2018)."
        reception_step = (
            "Bolivian funeral director takes custody at cargo terminal at El Alto International Airport (LPB), La Paz, "
            "or Viru Viru International Airport (VVI), Santa Cruz, depending on family location. "
            "SERECI (Tribunal Supremo Electoral) notified. Death certificate issued in Spanish with a QR code."
        )
    elif dest_key == "san-marino":
        consular = f"Notify the British Embassy Rome, with support from the Consulate-General in Milan. Hague Apostille applies (San Marino joined 1995). Route via Rimini, Italy, since San Marino has no commercial airport."
        reception_step = (
            "San Marino funeral director takes custody following arrival via Federico Fellini International Airport (RMI) in Rimini, Italy, "
            "and a short road transfer, since San Marino has no commercial airport of its own. "
            "Ufficio di Stato Civile notified. Death certificate issued in Italian."
        )
    elif dest_key == "liechtenstein":
        consular = f"Notify the British Embassy Bern, Switzerland. Hague Apostille applies (Liechtenstein joined 1972). Route via Zurich, Switzerland, since Liechtenstein has no commercial airport."
        reception_step = (
            "Liechtenstein funeral director takes custody following arrival via Zurich Airport (ZRH) in Switzerland "
            "and a road transfer, since Liechtenstein has no commercial airport of its own. "
            "Zivilstandsamt (Civil Registry Office) in Vaduz notified. Death certificate issued in German."
        )
    else:
        consular = f"Notify the {dest_data['name']} Embassy in {origin}."
        reception_step = f"{dest_data['name']} funeral director takes custody at cargo terminal."

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


def make_dest_faq6(origin_data, dest_data):
    """Generate a destination-specific sixth FAQ."""
    origin = origin_data["name"]
    dest_key = dest_data["dest_key"]

    if dest_key == "uruguay":
        return {
            "question": f"Is Uruguay a Hague Apostille member and how does this affect repatriation from {origin}?",
            "answer": (
                "Uruguay is a Hague Apostille Convention member since 14 October 2012. "
                "Death registration runs through the Direccion General del Registro de Estado Civil, part of the Ministry of Education and Culture. "
                f"Certified translation of documents from {origin} into Spanish is typically required by the receiving Uruguayan registry."
            ),
        }
    elif dest_key == "panama":
        return {
            "question": f"Which authority issues a Panamanian death certificate for a repatriation from {origin}?",
            "answer": (
                "Civil registration in Panama, including death certificates, runs through the Direccion Nacional del Registro Civil, "
                "a department of the Tribunal Electoral (Electoral Tribunal) created in 1974, rather than a justice or health ministry. "
                f"Panama is a Hague Apostille member since 1991, and certificates can be obtained from any provincial branch office, not only in Panama City."
            ),
        }
    elif dest_key == "guatemala":
        return {
            "question": f"How is a Guatemalan death certificate verified for a repatriation from {origin}?",
            "answer": (
                "RENAP (Registro Nacional de las Personas), Guatemala's national civil registry, issues death certificates that carry a QR code "
                "which can be scanned or checked on RENAP's validation page to confirm authenticity. "
                f"Guatemala is a Hague Apostille member since 2017. RENAP also covers Honduras' documentation questions through the same regional British Embassy in Guatemala City."
            ),
        }
    elif dest_key == "el-salvador":
        return {
            "question": f"Does the municipality or a national body issue the death certificate for repatriation from {origin} to El Salvador?",
            "answer": (
                "Both, at different stages. The municipality where the death occurred issues the original partida de defuncion. "
                "The RNPN (Registro Nacional de las Personas Naturales), the national identity registry, then authenticates that certificate for use outside El Salvador. "
                "El Salvador is a Hague Apostille member since 1996, and this authentication step is required before the certificate can support a repatriation case."
            ),
        }
    elif dest_key == "honduras":
        return {
            "question": f"Which airport actually receives a repatriation from {origin} to Honduras now?",
            "answer": (
                "Palmerola International Airport (XPL), roughly 60km northwest of Tegucigalpa, has handled all international commercial flights to the capital since December 2021, "
                "when the older Toncontin Airport in the city itself stopped taking international traffic and switched to domestic flights only. "
                "Honduras has no resident British Embassy; the British Embassy in Guatemala City covers documentation queries for Honduras."
            ),
        }
    elif dest_key == "nicaragua":
        return {
            "question": f"Who provides British consular support for a repatriation from {origin} to Nicaragua?",
            "answer": (
                "There is no British Embassy in Managua. Overall responsibility for Nicaragua sits with the British Embassy in San Jose, Costa Rica, "
                "though a British Honorary Consulate in Managua's Residencial Bolonia area can assist by appointment. "
                "Nicaragua is a Hague Apostille member since 14 May 2013."
            ),
        }
    elif dest_key == "paraguay":
        return {
            "question": f"How quickly must a death be registered in Paraguay for a repatriation from {origin}?",
            "answer": (
                "Paraguayan law requires death registration with the Registro del Estado Civil within 24 hours, faster than most comparable countries. "
                "A certified copy of the resulting acta de defuncion typically takes 3 to 10 business days to issue. "
                "Paraguay is a Hague Apostille member since 30 August 2014."
            ),
        }
    elif dest_key == "bolivia":
        return {
            "question": f"Which city receives a repatriation from {origin} to Bolivia?",
            "answer": (
                "It depends on where the family is based: El Alto International Airport (LPB) serves La Paz, and Viru Viru International Airport (VVI) serves Santa Cruz, "
                "Bolivia's largest city. Bolivia is a Hague Apostille member since 7 May 2018, and current SERECI death certificates must carry a QR code to be considered valid."
            ),
        }
    elif dest_key == "san-marino":
        return {
            "question": f"How does a repatriation from {origin} actually reach San Marino, given it has no airport?",
            "answer": (
                "San Marino has no commercial airport of its own. "
                "Every air cargo repatriation lands at Federico Fellini International Airport in Rimini, Italy, roughly 15km away, followed by a short road transfer across the border. "
                "There is also no resident British Embassy; consular support for San Marino comes from the British Embassy in Rome and the Consulate-General in Milan."
            ),
        }
    elif dest_key == "liechtenstein":
        return {
            "question": f"How does a repatriation from {origin} actually reach Liechtenstein, given it has no airport?",
            "answer": (
                "Liechtenstein has no commercial airport of its own. "
                "Every air cargo repatriation lands at Zurich Airport in Switzerland, roughly 120km away, followed by a road transfer to Vaduz. "
                "There is also no resident British Embassy; consular support for Liechtenstein comes from the British Embassy in Bern."
            ),
        }
    else:
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
    dest_hub_url = f"/repatriation-from-{dest_key}/"

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
    lines.append(f'date: 2026-07-05')
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
        ("R99", R99_ROUTES, 2),    # Start at C (index 2)
        ("R100", R100_ROUTES, 2),  # Start at C (index 2)
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
