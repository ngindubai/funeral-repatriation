#!/usr/bin/env python3
"""Generate Tier B route pages: chunks R49-R50.

   R49 (25 routes, variants D,E,A,B,C x5):
     Turkey wave 5 x5: uzbekistan, india, indonesia, vietnam, philippines
     Malaysia wave 5 x5: australia, new-zealand, united-states, singapore, japan
     Oman wave 4 x5: united-arab-emirates, china, nigeria, vietnam, malaysia
     Greece wave 5 x5: iraq, jordan, armenia, azerbaijan, cyprus
     Austria wave 5 x5: iraq, lebanon, bangladesh, georgia, vietnam

   R50 (25 routes, variants D,E,A,B,C x5):
     Denmark wave 5 x5: ukraine, egypt, philippines, georgia, indonesia
     Finland wave 5 x5: egypt, philippines, armenia, georgia, azerbaijan
     Italy wave 5 x5: argentina, brazil, indonesia, colombia, sri-lanka
     Spain wave 5 x5: indonesia, vietnam, france, portugal, italy
     Netherlands wave 5 x5: france, germany, spain, portugal, ethiopia

   Template rotation: R48 ended C (index 2). R49 starts D (index 3).
   Each block of 25 cycles D,E,A,B,C x5, ending on C.
   R50 starts D again.
"""

import os
import re

ROUTES_DIR = '/home/user/funeral-repatriation/site/content/routes'
VARIANTS = ['A', 'B', 'C', 'D', 'E']
START_VARIANT = 3  # D

# ---------------------------------------------------------------------------
# Destination hub metadata
# ---------------------------------------------------------------------------

DEST_META = {
    'turkey': {
        'name': 'Turkey',
        'slug': 'turkey',
        'key': 'tr',
        'reception': (
            "The Turkish funeral director (cenaze firmasi) takes custody at Istanbul "
            "Airport (IST) or Istanbul Sabiha Gokcen (SAW) cargo terminal. A transit "
            "certificate (transit belgesi) must accompany the remains. The municipality "
            "(belediye) registers the death in the nufus mudurlugu (population "
            "directorate). The Turkish Ministry of Health clearance is required before "
            "burial or cremation. All foreign documents not in Turkish require certified "
            "Turkish translation. No cremation facilities exist in Turkey. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Turkish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Turkey. Turkish Ministry of Foreign Affairs emergency "
            "line: +90 312 292 2000 (24 hours). The Turkish Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Turkish funeral director takes custody at Istanbul Airport (IST) or "
            "Istanbul Sabiha Gokcen (SAW) cargo terminal. A transit belgesi must "
            "accompany the remains. The belediye registers the death in the nufus "
            "mudurlugu. Ministry of Health clearance is required before burial. All "
            "foreign documents require certified Turkish translation."
        ),
        'emergency_line': '+90 312 292 2000',
        'hub_url': 'repatriation-from-turkey',
    },
    'malaysia': {
        'name': 'Malaysia',
        'slug': 'malaysia',
        'key': 'my',
        'reception': (
            "The Malaysian funeral director takes custody at Kuala Lumpur International "
            "Airport (KUL) cargo terminal. Malaysia Customs clearance is required. The "
            "National Registration Department (NRD) registers the death. The Ministry "
            "of Health may require clearance for final disposition. All foreign documents "
            "must be authenticated by the Malaysian Embassy or High Commission in the "
            "country of origin. Documents not in Malay or English require certified "
            "translation. (Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Malaysian High Commission or Embassy in {city} can advise on documentation "
            "requirements and authenticate foreign certificates. They cannot pay for or "
            "arrange repatriation. Malaysian Ministry of Foreign Affairs 24-hour "
            "emergency: +603 8000 8000."
        ),
        'arrival_faq': (
            "The Malaysian funeral director takes custody at Kuala Lumpur International "
            "Airport (KUL) cargo terminal. Malaysia Customs clearance requires the "
            "authenticated death certificate, transit permit, and health clearance. The "
            "National Registration Department (NRD) registers the death. All foreign "
            "documents must be authenticated by the Malaysian Embassy in the origin "
            "country. The Ministry of Health may need to be notified."
        ),
        'emergency_line': '+603 8000 8000',
        'hub_url': 'repatriation-from-malaysia',
    },
    'oman': {
        'name': 'Oman',
        'slug': 'oman',
        'key': 'om',
        'reception': (
            "The Omani funeral director takes custody at Muscat International Airport "
            "(MCT) cargo terminal. The Royal Oman Police registers the death and a "
            "burial permit from the Ministry of Health is required before any final "
            "disposition. Muslim remains are handled in accordance with Islamic law. "
            "All foreign documents not in Arabic require certified Arabic translation. "
            "Authentication by the Omani Embassy in the country of origin is required. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Omani Embassy in {city} can advise on documentation requirements for "
            "repatriation to Oman. Oman Ministry of Foreign Affairs can be reached "
            "via the Omani Embassy during business hours. The Omani Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Omani funeral director takes custody at Muscat International Airport "
            "(MCT) cargo terminal. The Royal Oman Police registers the death. A burial "
            "permit from the Ministry of Health is required. Muslim remains are handled "
            "in accordance with Islamic law. All foreign documents require certified "
            "Arabic translation and authentication by the Omani Embassy in the origin "
            "country."
        ),
        'emergency_line': 'contact Omani Embassy in origin country',
        'hub_url': 'repatriation-from-oman',
    },
    'greece': {
        'name': 'Greece',
        'slug': 'greece',
        'key': 'gr',
        'reception': (
            "The Greek funeral director (grafeiou teletou) takes custody at Athens "
            "Eleftherios Venizelos (ATH) or Thessaloniki Macedonia (SKG) cargo "
            "terminal. A local health authority clearance is required before burial or "
            "cremation. The Lixiarcheio (civil registry) registers the death. Greece "
            "is an EU and Hague Apostille Convention member. All foreign documents not "
            "in Greek require certified Greek translation. "
            "(Greek Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Greek Embassy in {city} can advise on documentation requirements for "
            "repatriation to Greece. Greek Ministry of Foreign Affairs emergency "
            "line: +30 210 3681 000 (24 hours). The Greek Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Greek funeral director takes custody at Athens Eleftherios Venizelos "
            "(ATH) or Thessaloniki (SKG) cargo terminal. Local health authority "
            "clearance is required before burial or cremation. The Lixiarcheio "
            "registers the death. All foreign documents require certified Greek "
            "translation. The receiving funeral director coordinates with local "
            "authorities."
        ),
        'emergency_line': '+30 210 3681 000',
        'hub_url': 'repatriation-from-greece',
    },
    'austria': {
        'name': 'Austria',
        'slug': 'austria',
        'key': 'at',
        'reception': (
            "The Austrian Bestattung (funeral director) takes custody at Vienna "
            "International (VIE) cargo terminal. A Leichenbegleitschein (body transport "
            "certificate) must accompany the remains. The local Standesamt (registry "
            "office) registers the death. The Bezirksverwaltungsbehoerde (district "
            "authority) may need to approve burial or cremation. Austria is an EU and "
            "Hague Apostille Convention member. "
            "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
        ),
        'consular_template': (
            "Austrian Embassy in {city} can advise on documentation requirements for "
            "repatriation to Austria. Austrian Federal Ministry for European and "
            "International Affairs (BMEIA) emergency line: +43 1 90115 3775 (24 hours). "
            "The Austrian Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Austrian Bestattung takes custody at Vienna International (VIE) cargo "
            "terminal. A Leichenbegleitschein must accompany the remains. The local "
            "Standesamt registers the death. The Bezirksverwaltungsbehoerde may need "
            "to approve burial or cremation. Austria is an EU and Hague Apostille "
            "Convention member. All non-German-language documents require certified "
            "German translation."
        ),
        'emergency_line': '+43 1 90115 3775',
        'hub_url': 'repatriation-from-austria',
    },
    'denmark': {
        'name': 'Denmark',
        'slug': 'denmark',
        'key': 'dk',
        'reception': (
            "The Danish begravelsesforretning (funeral director) takes custody at "
            "Copenhagen Kastrup (CPH) cargo terminal. A ligfolgeskrivelse (body transit "
            "certificate) must accompany the remains. The civil registry records the "
            "death. Denmark is an EU and Hague Apostille Convention member. Documents "
            "not in Danish, English, or another major European language require certified "
            "Danish translation. (Danish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Danish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Denmark. Danish Ministry of Foreign Affairs emergency "
            "line: +45 33 92 00 00 (24 hours). The Danish Embassy cannot pay for or "
            "arrange repatriation."
        ),
        'arrival_faq': (
            "The Danish funeral director takes custody at Copenhagen Kastrup (CPH) "
            "cargo terminal. A ligfolgeskrivelse must accompany the remains. The civil "
            "registry records the death. Denmark is an EU and Hague Apostille member. "
            "Documents not in Danish, English, or a major European language require "
            "certified Danish translation. The receiving funeral director coordinates "
            "with local authorities."
        ),
        'emergency_line': '+45 33 92 00 00',
        'hub_url': 'repatriation-from-denmark',
    },
    'finland': {
        'name': 'Finland',
        'slug': 'finland',
        'key': 'fi',
        'reception': (
            "The Finnish hautauspalvelu (funeral director) takes custody at "
            "Helsinki-Vantaa (HEL) cargo terminal. A siirtolupa (transport permit) "
            "issued by the aluehallintovirasto (Regional State Administrative Agency) "
            "is required before the remains can be transported. The Digi- ja "
            "vaestotietovirasto (DVV, Digital and Population Data Services Agency) "
            "records the death. Finland is an EU and Hague Apostille Convention member. "
            "Documents not in Finnish, Swedish, or English require certified translation. "
            "(Finnish Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Finnish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Finland. Finnish Ministry of Foreign Affairs emergency "
            "line: +358 9 1605 5555 (24 hours). The Finnish Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Finnish funeral director takes custody at Helsinki-Vantaa (HEL) cargo "
            "terminal. A siirtolupa issued by the aluehallintovirasto is required. "
            "The DVV records the death. Finland is an EU and Hague Apostille member. "
            "Documents not in Finnish, Swedish, or English require certified translation. "
            "The receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+358 9 1605 5555',
        'hub_url': 'repatriation-from-finland',
    },
    'italy': {
        'name': 'Italy',
        'slug': 'italy',
        'key': 'it',
        'reception': (
            "The Italian funeral director (impresa funebre) takes custody at the "
            "cargo terminal, typically Rome Fiumicino (FCO), Milan Malpensa (MXP), or "
            "another Italian international airport. A prefettura transport authorisation "
            "is required before burial or cremation. All foreign documents must carry a "
            "certified Italian translation. The local comune registers the death with "
            "the anagrafe (civil registry). "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
        'consular_template': (
            "Italian Embassy in {city} can advise on documentation requirements for "
            "repatriation to Italy. Italian Ministry of Foreign Affairs and International "
            "Cooperation (MAECI) emergency line: +39 06 3691 3691 (24 hours). The "
            "Italian Embassy cannot pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Italian funeral director takes custody at Rome Fiumicino (FCO) or "
            "Milan Malpensa (MXP) cargo terminal. A prefettura transport authorisation "
            "is required. All foreign documents require certified Italian translation. "
            "The local comune registers the death with the anagrafe. The receiving "
            "funeral director coordinates with local authorities."
        ),
        'emergency_line': '+39 06 3691 3691',
        'hub_url': 'repatriation-from-italy',
    },
    'spain': {
        'name': 'Spain',
        'slug': 'spain',
        'key': 'es',
        'reception': (
            "The Spanish funeral director (empresa funeraria) takes custody at the "
            "cargo terminal, typically Madrid Barajas (MAD), Barcelona El Prat (BCN), "
            "or another Spanish airport. The Registro Civil registers the death. For "
            "deaths in the Canary or Balearic Islands, an internal mainland transfer "
            "is required before any international cargo flight departs. All foreign "
            "documents must carry a certified Spanish translation. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
        'consular_template': (
            "Spanish Embassy in {city} can advise on documentation requirements for "
            "repatriation to Spain. Spanish Ministry of Foreign Affairs emergency "
            "line: +34 91 379 9700 (24 hours). The Spanish Embassy cannot pay for "
            "or arrange repatriation."
        ),
        'arrival_faq': (
            "The Spanish funeral director takes custody at Madrid Barajas (MAD) or "
            "Barcelona El Prat (BCN) cargo terminal. The Registro Civil registers the "
            "death. All foreign documents require certified Spanish translation. Island "
            "cases require an additional internal transfer to the mainland. The "
            "receiving funeral director coordinates with local authorities."
        ),
        'emergency_line': '+34 91 379 9700',
        'hub_url': 'repatriation-from-spain',
    },
    'netherlands': {
        'name': 'Netherlands',
        'slug': 'netherlands',
        'key': 'nl',
        'reception': (
            "The Dutch funeral director (begrafenisondernemer or uitvaartondernemer) "
            "takes custody at Amsterdam Schiphol (AMS) or Rotterdam The Hague (RTM) "
            "cargo terminal. The local gemeente (municipality) registers the death "
            "with the Burgerlijke Stand (civil registry). A transport permit "
            "(laissez-passer) must accompany the remains. Foreign documents in "
            "languages other than Dutch, English, French, or German require certified "
            "translation. (Dutch Ministry of Foreign Affairs, 2025.)"
        ),
        'consular_template': (
            "Dutch Embassy in {city} can advise on documentation requirements for "
            "repatriation to the Netherlands. Dutch Ministry of Foreign Affairs "
            "emergency line: +31 70 348 6486 (24 hours). The Dutch Embassy cannot "
            "pay for or arrange repatriation."
        ),
        'arrival_faq': (
            "The Dutch funeral director takes custody at Amsterdam Schiphol (AMS) or "
            "Rotterdam The Hague (RTM) cargo terminal. The gemeente registers the death "
            "with the Burgerlijke Stand. A laissez-passer must accompany the remains. "
            "Documents in languages other than Dutch, English, French, or German require "
            "certified translation. The receiving funeral director coordinates with the "
            "local authorities."
        ),
        'emergency_line': '+31 70 348 6486',
        'hub_url': 'repatriation-from-netherlands',
    },
}

# ---------------------------------------------------------------------------
# Origin country data
# ---------------------------------------------------------------------------

ORIGIN_DATA = {
    'uzbekistan': {
        'name': 'Uzbekistan',
        'emergency': '102 (police) / 103 (ambulance)',
        'registry': 'the local Hukumati (civil administration) registration office',
        'cert_name': 'death certificate',
        'cert_lang': 'Uzbek or Russian',
        'overview': (
            "Contact emergency services (102 for police, 103 for ambulance). Death "
            "must be registered with the Hukumati (local civil administration) "
            "registration office. The Prosecutor's Office takes jurisdiction for "
            "violent, suspicious, or unexplained deaths."
        ),
        'doc_time': '7-10 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is available in Uzbekistan.',
        'postmortem_trigger': 'Violent, suspicious, or unexplained deaths',
    },
    'india': {
        'name': 'India',
        'emergency': '112 (national emergency) / 100 (police) / 108 (ambulance)',
        'registry': 'the local municipal authority',
        'cert_name': 'death certificate',
        'cert_lang': 'English and local language',
        'overview': (
            "Contact local emergency services (112, or 100 for police, 108 for "
            "ambulance). If death occurs outside hospital, police must be notified. "
            "Death must be registered with the local municipal authority within 21 "
            "days. India's tropical climate requires urgent embalming."
        ),
        'doc_time': '14-30 days minimum. Post-mortem cases take longer.',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '8-16 weeks or longer',
        'complexity': 'high',
        'cremation': 'Cremation in India is well established and widely available.',
        'postmortem_trigger': 'Indian police routinely order post-mortem examinations for unexpected deaths of foreign nationals',
    },
    'indonesia': {
        'name': 'Indonesia',
        'emergency': '112',
        'registry': 'the local civil registry (catatan sipil)',
        'cert_name': 'surat keterangan kematian (death certificate)',
        'cert_lang': 'Bahasa Indonesia',
        'overview': (
            "Call 112 for emergency services. Unexpected deaths require police "
            "attendance. Death registered with the local civil registry (catatan "
            "sipil). The surat keterangan kematian is issued in Bahasa Indonesia. "
            "Deaths in Bali require internal transfer to Jakarta (CGK) for "
            "international cargo departure."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Indonesia (including Bali, where Hindu cremation is traditional) is available.',
        'postmortem_trigger': 'Unexpected and unnatural deaths',
    },
    'vietnam': {
        'name': 'Vietnam',
        'emergency': '113 (police) / 115 (ambulance)',
        'registry': 'the local civil registry (nha nuoc)',
        'cert_name': 'giay chung tu (death certificate)',
        'cert_lang': 'Vietnamese',
        'overview': (
            "Call 113 for police or 115 for ambulance. A licensed physician must "
            "certify the death. Unexpected deaths trigger police notification. Death "
            "registered with the local civil registry (nha nuoc). The giay chung tu "
            "is issued in Vietnamese only."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Vietnam is available in major cities including Hanoi and Ho Chi Minh City.',
        'postmortem_trigger': 'Unexpected or accident deaths',
    },
    'philippines': {
        'name': 'Philippines',
        'emergency': '911',
        'registry': 'the Local Civil Registrar',
        'cert_name': 'certificate of death (PSA-authenticated)',
        'cert_lang': 'English',
        'overview': (
            "Contact local emergency services (911). If death is unexpected, police "
            "must be notified. The certificate of death is issued by the attending "
            "physician and filed with the Local Civil Registrar. PSA authentication "
            "and DFA countersignature are then required before international use."
        ),
        'doc_time': '3-6 weeks (PSA and DFA authentication are the main delays)',
        'timeline_avg': '4-6 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in the Philippines is available and increasingly common.',
        'postmortem_trigger': 'Unexpected, violent, or medically uncertified deaths',
    },
    'australia': {
        'name': 'Australia',
        'emergency': '000',
        'registry': 'the relevant state or territory Registry of Births, Deaths and Marriages',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 000 for emergency services. A registered medical practitioner "
            "certifies the death. The death is registered with the state or territory "
            "Registry of Births, Deaths and Marriages. The coroner takes jurisdiction "
            "for unexpected, violent, or unexplained deaths."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Australia is widely available across all states and territories.',
        'postmortem_trigger': 'Unexpected, violent, or unexplained deaths (coroner takes jurisdiction)',
    },
    'new-zealand': {
        'name': 'New Zealand',
        'emergency': '111',
        'registry': 'Births, Deaths and Marriages New Zealand (BDM)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 111 for emergency services. A registered medical practitioner "
            "certifies the death. The death is registered with Births, Deaths and "
            "Marriages New Zealand (BDM). The coroner takes jurisdiction for sudden, "
            "unexpected, or violent deaths."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in New Zealand is widely available.',
        'postmortem_trigger': 'Sudden, unexpected, or violent deaths (coroner takes jurisdiction)',
    },
    'united-states': {
        'name': 'United States',
        'emergency': '911',
        'registry': 'the state vital statistics office (civil records office)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 911 for emergency services. A licensed physician or medical examiner "
            "certifies the death. The death is registered with the state health "
            "department. The medical examiner or coroner takes jurisdiction for "
            "unexpected, violent, or unexplained deaths. State requirements vary."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '10-21 days',
        'timeline_fast': '7-10 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in the United States is widely available.',
        'postmortem_trigger': 'Unexpected, violent, or medically uncertified deaths (medical examiner or coroner)',
    },
    'singapore': {
        'name': 'Singapore',
        'emergency': '999 (police) / 995 (ambulance)',
        'registry': 'the Immigration and Checkpoints Authority (ICA)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 999 for police or 995 for ambulance. A registered medical "
            "practitioner certifies the death. The death is registered with the "
            "Immigration and Checkpoints Authority (ICA). The Coroner's Court takes "
            "jurisdiction for sudden, unexpected, or violent deaths."
        ),
        'doc_time': '5-7 days',
        'timeline_avg': '5-10 days',
        'timeline_fast': '3-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Singapore is widely available and commonly used.',
        'postmortem_trigger': 'Sudden, unexpected, or violent deaths (Coroner\'s Court)',
    },
    'japan': {
        'name': 'Japan',
        'emergency': '110 (police) / 119 (fire and ambulance)',
        'registry': 'the local municipal office (shiyakusho or kuyakusho)',
        'cert_name': 'shibo todoke (death notification) and shibo shindan-sho (death certificate)',
        'cert_lang': 'Japanese',
        'overview': (
            "Call 110 for police or 119 for fire and ambulance. A licensed physician "
            "issues the shibo shindan-sho (death certificate). Death notification "
            "(shibo todoke) must be submitted to the local municipal office within "
            "seven days. The police take jurisdiction for sudden, unnatural, or "
            "unexplained deaths. All documentation is in Japanese and requires "
            "certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '14-28 days',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Japan is standard and near-universal. The cremated remains (kotsuage) are presented to the family.',
        'postmortem_trigger': 'Sudden, unnatural, or unexplained deaths (keisatsu)',
    },
    'united-arab-emirates': {
        'name': 'United Arab Emirates',
        'emergency': '999',
        'registry': 'the Ministry of Health and Prevention (MOHAP)',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 999 for emergency services. The Ministry of Health and Prevention "
            "(MOHAP) registers the death. For Muslim remains, the body must be "
            "prepared and buried within 24 hours under Islamic law; exceptions for "
            "repatriation require specific authorisation. All documentation is in "
            "Arabic."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '5-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in the UAE. Non-Muslim remains may use designated facilities.',
        'postmortem_trigger': 'Violent, suspicious, or medically unexplained deaths',
    },
    'china': {
        'name': 'China',
        'emergency': '120 (ambulance) / 110 (police)',
        'registry': 'the local civil affairs bureau (minzhengju)',
        'cert_name': 'si wang zheng ming shu (death certificate)',
        'cert_lang': 'Mandarin Chinese',
        'overview': (
            "Call 120 for ambulance or 110 for police. Death must be certified by a "
            "physician at a recognised medical facility. The death is registered with "
            "the local civil affairs bureau (minzhengju). Police take jurisdiction for "
            "sudden, violent, or unexplained deaths. All documentation is in Mandarin "
            "Chinese and requires certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in China is the standard and in most cities the legally required method.',
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths',
    },
    'nigeria': {
        'name': 'Nigeria',
        'emergency': '112',
        'registry': 'the National Population Commission (NPopC)',
        'cert_name': 'death certificate',
        'cert_lang': 'English',
        'overview': (
            "Call 112 for emergency services. Death must be certified by a medical "
            "practitioner. Registration with the National Population Commission "
            "(NPopC) is required. Police take jurisdiction for sudden, violent, or "
            "unexplained deaths. Documentation is in English but delays in official "
            "registration are common."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Nigeria is available in some major cities but is not common.',
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths',
    },
    'malaysia': {
        'name': 'Malaysia',
        'emergency': '999',
        'registry': 'the National Registration Department (NRD)',
        'cert_name': 'death certificate (sijil kematian)',
        'cert_lang': 'Malay and English',
        'overview': (
            "Call 999 for emergency services. A registered medical practitioner "
            "certifies the death. The death is registered with the National "
            "Registration Department (NRD). The police take jurisdiction for sudden, "
            "violent, or unexplained deaths."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Malaysia is available and commonly used for non-Muslim remains.',
        'postmortem_trigger': 'Sudden, violent, or unexplained deaths',
    },
    'iraq': {
        'name': 'Iraq',
        'emergency': '104 (police) / 115 (ambulance)',
        'registry': 'the Civil Status Directorate',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 104 for police or 115 for ambulance. Death is certified by a "
            "physician and registered with the Civil Status Directorate. For violent "
            "or unexplained deaths, police and judicial procedures apply. The FCDO "
            "advises against all travel to large parts of Iraq; access to consular "
            "and civil registry services varies significantly by location. All "
            "documentation is in Arabic."
        ),
        'doc_time': '2-4 weeks (highly variable)',
        'timeline_avg': '6-12 weeks',
        'timeline_fast': '4-6 weeks',
        'timeline_complex': 'many months',
        'complexity': 'high',
        'cremation': 'Cremation is not available in Iraq for Muslim remains. Non-Muslim remains face very limited options.',
        'postmortem_trigger': 'Violent, suspicious, or unexplained deaths; security situation may further delay access',
    },
    'jordan': {
        'name': 'Jordan',
        'emergency': '911 (police) / 912 (ambulance)',
        'registry': 'the Ministry of Interior civil registry',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 911 for police or 912 for ambulance. Death is certified by a "
            "physician and registered with the local Ministry of Interior civil "
            "registry office. Police take jurisdiction for violent or unexplained "
            "deaths. All documentation is in Arabic and requires certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Jordan.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'armenia': {
        'name': 'Armenia',
        'emergency': '101 (police) / 103 (ambulance)',
        'registry': 'the State Registry Office (ZAGS)',
        'cert_name': 'death certificate (in Armenian)',
        'cert_lang': 'Armenian',
        'overview': (
            "Call 101 for police or 103 for ambulance. Death is certified by a "
            "physician and registered with the State Registry Office (ZAGS). Police "
            "take jurisdiction for violent or unexplained deaths. All documentation "
            "is in Armenian and requires certified translation."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Armenia is available but limited.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'azerbaijan': {
        'name': 'Azerbaijan',
        'emergency': '102 (police) / 103 (ambulance)',
        'registry': 'the State Statistical Committee civil registry',
        'cert_name': 'death certificate (in Azerbaijani)',
        'cert_lang': 'Azerbaijani',
        'overview': (
            "Call 102 for police or 103 for ambulance. Death is certified by a "
            "physician and registered with the State Statistical Committee civil "
            "registry. Police take jurisdiction for violent or unexplained deaths. "
            "All documentation is in Azerbaijani and requires certified translation."
        ),
        'doc_time': '7-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is limited in Azerbaijan. Families should confirm availability.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'cyprus': {
        'name': 'Cyprus',
        'emergency': '112',
        'registry': 'the Civil Registry and Migration Department',
        'cert_name': 'death certificate',
        'cert_lang': 'Greek and English',
        'overview': (
            "Call 112 for emergency services. A registered medical practitioner "
            "certifies the death. The death is registered with the Civil Registry "
            "and Migration Department. Cyprus is an EU member and Hague Apostille "
            "Convention member, which simplifies document recognition across EU "
            "member states."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '5-10 days',
        'timeline_fast': '3-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Cyprus is available.',
        'postmortem_trigger': 'Violent, sudden, or unexplained deaths',
    },
    'lebanon': {
        'name': 'Lebanon',
        'emergency': '140 (police) / 125 (ambulance)',
        'registry': 'the Ministry of Interior civil registry',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 140 for police or 125 for ambulance. Death is certified by a "
            "physician and registered at the local Ministry of Interior civil "
            "registry. For violent or unexplained deaths, police procedures apply. "
            "Families should monitor FCDO travel advice for Lebanon given the "
            "security situation in the region. All documentation is in Arabic."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '3-6 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate-high',
        'cremation': 'Cremation is limited in Lebanon. Families should confirm availability.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'bangladesh': {
        'name': 'Bangladesh',
        'emergency': '999',
        'registry': 'the local registration office',
        'cert_name': 'death certificate (in Bengali)',
        'cert_lang': 'Bengali',
        'overview': (
            "Call 999 for emergency services. Death is certified by a physician and "
            "registered with the local registration office. Police take jurisdiction "
            "for violent or unexplained deaths. Documentation is in Bengali and "
            "requires certified translation."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '3-5 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '6-12 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Bangladesh is available for non-Muslim remains.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'georgia': {
        'name': 'Georgia',
        'emergency': '112',
        'registry': 'the Public Services Development Agency (PSDA)',
        'cert_name': 'death certificate (in Georgian)',
        'cert_lang': 'Georgian',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician and "
            "registered with the Public Services Development Agency (PSDA). Police "
            "take jurisdiction for violent or unexplained deaths. Documentation is "
            "in Georgian and requires certified translation."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Georgia is available but limited.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'ukraine': {
        'name': 'Ukraine',
        'emergency': '102 (police) / 103 (ambulance)',
        'registry': 'the civil registry office (DRACS)',
        'cert_name': 'death certificate (in Ukrainian)',
        'cert_lang': 'Ukrainian',
        'overview': (
            "Call 102 for police or 103 for ambulance. In areas not affected by "
            "hostilities, death is certified by a physician and registered with the "
            "civil registry office (DRACS). In areas affected by the ongoing conflict, "
            "access to civil registry services and the ability to transport remains "
            "may be severely limited or impossible. The FCDO advises against all "
            "travel to Ukraine. Families should contact their embassy immediately "
            "and not travel to Ukraine."
        ),
        'doc_time': '7-14 days (stable areas); highly variable in conflict zones',
        'timeline_avg': '3-6 weeks (stable areas)',
        'timeline_fast': '2-4 weeks',
        'timeline_complex': 'many months or impossible in conflict zones',
        'complexity': 'high',
        'cremation': 'Cremation in Ukraine is available in major cities in non-conflict areas.',
        'postmortem_trigger': 'Violent, unexplained, or conflict-related deaths',
    },
    'egypt': {
        'name': 'Egypt',
        'emergency': '122 (police) / 123 (ambulance)',
        'registry': 'the Ministry of Interior civil registry',
        'cert_name': 'death certificate (in Arabic)',
        'cert_lang': 'Arabic',
        'overview': (
            "Call 122 for police or 123 for ambulance. Death is certified by a "
            "physician and registered with the local Ministry of Interior civil "
            "registry. Police take jurisdiction for violent or unexplained deaths. "
            "All documentation is in Arabic and requires certified translation."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '2-3 weeks',
        'timeline_fast': '10-14 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is not available for Muslim remains in Egypt.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'argentina': {
        'name': 'Argentina',
        'emergency': '101 (police) / 107 (ambulance)',
        'registry': 'the Registro Civil y Capacidad de las Personas',
        'cert_name': 'Acta de Defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 101 for police or 107 for ambulance. Death is certified by a "
            "physician and registered with the Registro Civil y Capacidad de las "
            "Personas. The Acta de Defuncion is issued in Spanish. Police and the "
            "judicial system take jurisdiction for violent or unexplained deaths."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Argentina is available in major cities.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'brazil': {
        'name': 'Brazil',
        'emergency': '190 (police) / 192 (ambulance)',
        'registry': 'the Registro Civil (local cartorio)',
        'cert_name': 'Certidao de Obito (death certificate)',
        'cert_lang': 'Portuguese',
        'overview': (
            "Call 190 for police or 192 for ambulance. Death is certified by a "
            "physician and the Certidao de Obito is registered at the local cartorio "
            "(Registro Civil). Police and the delegacia (police station) take "
            "jurisdiction for violent or unexplained deaths."
        ),
        'doc_time': '5-10 days',
        'timeline_avg': '7-14 days',
        'timeline_fast': '5-7 days',
        'timeline_complex': '3-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Brazil is widely available in major cities.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'colombia': {
        'name': 'Colombia',
        'emergency': '112',
        'registry': 'the Registraduria Nacional del Estado Civil',
        'cert_name': 'Registro Civil de Defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician "
            "and registered with the Registraduria Nacional del Estado Civil. The "
            "Registro Civil de Defuncion is issued in Spanish. Police take "
            "jurisdiction for violent or unexplained deaths."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '10-21 days',
        'timeline_fast': '7-10 days',
        'timeline_complex': '4-6 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Colombia is available in major cities.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'sri-lanka': {
        'name': 'Sri Lanka',
        'emergency': '119 (police) / 110 (ambulance)',
        'registry': 'the local Divisional Secretariat',
        'cert_name': 'death certificate',
        'cert_lang': 'Sinhala, Tamil, and English',
        'overview': (
            "Call 119 for police or 110 for ambulance. Death is certified by a "
            "physician and registered with the local Divisional Secretariat. Police "
            "take jurisdiction for violent or unexplained deaths. Documentation is "
            "issued in Sinhala, Tamil, and English."
        ),
        'doc_time': '7-14 days',
        'timeline_avg': '2-4 weeks',
        'timeline_fast': '14-21 days',
        'timeline_complex': '4-8 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation in Sri Lanka is available and commonly used.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'france': {
        'name': 'France',
        'emergency': '15 (SAMU) / 17 (police) / 18 (fire) / 112',
        'registry': 'the mairie (town hall) civil registry',
        'cert_name': 'acte de deces (death certificate)',
        'cert_lang': 'French',
        'overview': (
            "Call 15 (SAMU ambulance), 17 (police), or 112. Death is certified by a "
            "physician and the acte de deces is registered at the mairie (town hall). "
            "The procureur de la Republique (prosecutor) takes jurisdiction for "
            "violent or unexplained deaths. France is an EU member and Hague Apostille "
            "Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in France is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (procureur de la Republique)',
    },
    'germany': {
        'name': 'Germany',
        'emergency': '112',
        'registry': 'the local Standesamt (civil registry)',
        'cert_name': 'Sterbeurkunde (death certificate)',
        'cert_lang': 'German',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician and "
            "registered with the local Standesamt (civil registry). The Sterbeurkunde "
            "is issued in German. Police and the Staatsanwaltschaft (public prosecutor) "
            "take jurisdiction for violent or unexplained deaths. Germany is an EU "
            "member and Hague Apostille Convention member."
        ),
        'doc_time': '3-5 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Germany is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (Staatsanwaltschaft)',
    },
    'portugal': {
        'name': 'Portugal',
        'emergency': '112',
        'registry': 'the Conservatoria do Registo Civil',
        'cert_name': 'Certidao de Obito (death certificate)',
        'cert_lang': 'Portuguese',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician and "
            "the Certidao de Obito is registered at the Conservatoria do Registo "
            "Civil. The Ministerio Publico (public prosecutor) takes jurisdiction for "
            "violent or unexplained deaths. Portugal is an EU member and Hague "
            "Apostille Convention member."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Portugal is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (Ministerio Publico)',
    },
    'ethiopia': {
        'name': 'Ethiopia',
        'emergency': '911',
        'registry': 'the Vital Events Registration Agency (VERA)',
        'cert_name': 'death certificate (in Amharic)',
        'cert_lang': 'Amharic',
        'overview': (
            "Call 911 for emergency services. Death is certified by a physician or "
            "health officer and registered with the Vital Events Registration Agency "
            "(VERA). Police take jurisdiction for violent or unexplained deaths. "
            "Documentation is in Amharic and requires certified translation."
        ),
        'doc_time': '7-21 days',
        'timeline_avg': '4-8 weeks',
        'timeline_fast': '3-4 weeks',
        'timeline_complex': '8-16 weeks',
        'complexity': 'moderate',
        'cremation': 'Cremation is limited in Ethiopia and not widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths',
    },
    'italy': {
        'name': 'Italy',
        'emergency': '112 / 118 (ambulance)',
        'registry': 'the local comune via the Ufficio di Stato Civile',
        'cert_name': 'atto di morte (death certificate)',
        'cert_lang': 'Italian',
        'overview': (
            "Call 112 or 118 for ambulance. Death is certified by a physician. The "
            "atto di morte is registered with the local comune through the Ufficio "
            "di Stato Civile. The procura della Repubblica (public prosecutor) takes "
            "jurisdiction for violent or unexplained deaths. Italy is an EU member "
            "and Hague Apostille Convention member."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Italy is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (procura della Repubblica)',
    },
    'spain': {
        'name': 'Spain',
        'emergency': '112',
        'registry': 'the Registro Civil',
        'cert_name': 'certificado de defuncion (death certificate)',
        'cert_lang': 'Spanish',
        'overview': (
            "Call 112 for emergency services. Death is certified by a physician and "
            "registered with the local Registro Civil. The Juzgado de Guardia (duty "
            "court) takes jurisdiction for violent or unexplained deaths. Spain is "
            "an EU member and Hague Apostille Convention member."
        ),
        'doc_time': '3-7 days',
        'timeline_avg': '3-7 days',
        'timeline_fast': '2-5 days',
        'timeline_complex': '2-4 weeks',
        'complexity': 'low',
        'cremation': 'Cremation in Spain is widely available.',
        'postmortem_trigger': 'Violent or unexplained deaths (Juzgado de Guardia)',
    },
}

# ---------------------------------------------------------------------------
# Route definitions
# ---------------------------------------------------------------------------

ROUTES = [
    # R49 -- Turkey wave 5
    {
        'origin': 'uzbekistan', 'dest': 'turkey',
        'embassy_city': 'Tashkent',
        'intro': (
            "Uzbek nationals in Turkey number in the hundreds of thousands, making "
            "Turkey one of the most significant diaspora destinations for Uzbeks. "
            "Uzbekistan and Turkey share Turkic language roots and cultural bonds "
            "through the Organisation of Turkic States and related frameworks. Many "
            "Uzbeks work in construction, trade, and service sectors across Istanbul, "
            "Ankara, and other Turkish cities. Uzbek documentation in the Latin-script "
            "Uzbek alphabet requires certified Turkish translation for the nufus "
            "mudurlugu (civil registry). The Turkish Embassy in Tashkent handles "
            "consular matters. (Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'india', 'dest': 'turkey',
        'embassy_city': 'New Delhi',
        'intro': (
            "Indian nationals in Turkey include a growing community of students, "
            "technology professionals, and business travellers, concentrated in "
            "Istanbul and Ankara. India and Turkey have bilateral diplomatic ties "
            "within the G20 framework, and the two countries have strengthened trade "
            "and economic ties in recent years. Hindi, Malayalam, Tamil, and other "
            "Indian language documentation requires certified Turkish translation for "
            "nufus mudurlugu (civil registry) purposes. Post-mortem examinations are "
            "routine in India for unexpected deaths, which significantly extends the "
            "timeline. The Turkish Embassy in New Delhi handles consular matters. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'indonesia', 'dest': 'turkey',
        'embassy_city': 'Jakarta',
        'intro': (
            "Indonesian nationals in Turkey include students, professionals, and a "
            "small Muslim diaspora community, reflecting the shared Islamic heritage "
            "of the two countries. Indonesia and Turkey have bilateral ties within "
            "the Organisation of Islamic Cooperation (OIC) and the G20 framework, "
            "with trade and diplomatic relations well established. Bahasa Indonesia "
            "documentation requires certified Turkish translation for nufus mudurlugu "
            "(civil registry) purposes. The Turkish Embassy in Jakarta handles consular "
            "matters. (Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'vietnam', 'dest': 'turkey',
        'embassy_city': 'Hanoi',
        'intro': (
            "Vietnamese nationals in Turkey include students, professionals, and "
            "traders, with the community growing as Turkey and Vietnam deepen trade "
            "and diplomatic ties. Turkey has become an increasingly significant "
            "trade partner for Southeast Asia, and bilateral business exchanges have "
            "expanded. Vietnamese documentation requires certified Turkish translation "
            "for nufus mudurlugu (civil registry) purposes. The Turkish Embassy in "
            "Hanoi handles consular matters. (Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'philippines', 'dest': 'turkey',
        'embassy_city': 'Manila',
        'intro': (
            "Filipino nationals in Turkey include professionals, domestic workers, "
            "and students, concentrated in Istanbul. Turkey and the Philippines have "
            "bilateral diplomatic ties, and Filipinos work across trade, domestic "
            "service, and hospitality sectors. Philippine documentation requires PSA "
            "authentication and DFA countersignature before certified Turkish "
            "translation can be obtained for nufus mudurlugu (civil registry) purposes. "
            "The Turkish Embassy in Manila handles consular matters. "
            "(Turkish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R49 -- Malaysia wave 5
    {
        'origin': 'australia', 'dest': 'malaysia',
        'embassy_city': 'Canberra',
        'intro': (
            "Malaysia has one of the most significant student and professional "
            "communities in Australia, with tens of thousands of Malaysians studying "
            "at Australian universities and many settling permanently in Australian "
            "cities. Malaysia and Australia have close trade and educational ties "
            "through the ASEAN-Australia framework. English documentation from "
            "Australia is generally accepted by Malaysian authorities. The Malaysian "
            "High Commission in Canberra handles consular matters. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'new-zealand', 'dest': 'malaysia',
        'embassy_city': 'Wellington',
        'intro': (
            "Malaysian students and professionals form a notable part of New "
            "Zealand's Asian community, with many Malaysians studying at New Zealand "
            "universities and working in professional services. New Zealand and "
            "Malaysia have close Commonwealth and trade ties. English documentation "
            "from New Zealand is generally accepted by Malaysian authorities without "
            "the need for further translation. The Malaysian High Commission in "
            "Wellington handles consular matters. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'united-states', 'dest': 'malaysia',
        'embassy_city': 'Washington DC',
        'intro': (
            "Malaysian nationals in the United States include students, academics, "
            "and an established professional community in states with strong university "
            "and technology sectors, particularly California, New York, and "
            "Massachusetts. Malaysia and the United States have bilateral trade and "
            "security ties through the ASEAN framework. English documentation from "
            "the United States is accepted by Malaysian authorities without translation. "
            "The Malaysian Embassy in Washington DC handles consular matters. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'singapore', 'dest': 'malaysia',
        'embassy_city': 'Singapore',
        'intro': (
            "Singapore and Malaysia share the Causeway and the Second Link, and "
            "hundreds of thousands of Malaysians live and work in Singapore. This is "
            "one of the most active cross-border worker corridors in the world: over "
            "300,000 Malaysians commute between Johor Bahru and Singapore daily, and "
            "many have lived in Singapore for years. Malay and English documentation "
            "from Singapore is accepted by Malaysian authorities. The Malaysian High "
            "Commission in Singapore handles consular matters. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'japan', 'dest': 'malaysia',
        'embassy_city': 'Tokyo',
        'intro': (
            "Malaysian nationals in Japan include students, academics, and "
            "professionals, with Malaysia a significant participant in Japan's "
            "Look East Policy since the 1980s. Thousands of Malaysian students have "
            "studied at Japanese universities under government scholarship programmes, "
            "and business ties between Malaysia and Japan are longstanding. Japanese "
            "documentation requires certified Malay or English translation for Malaysian "
            "National Registration Department (NRD) purposes. The Malaysian Embassy "
            "in Tokyo handles consular matters. "
            "(Malaysian Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R49 -- Oman wave 4
    {
        'origin': 'united-arab-emirates', 'dest': 'oman',
        'embassy_city': 'Abu Dhabi',
        'intro': (
            "Omani nationals form a significant community in the United Arab Emirates, "
            "which shares a long land border with Oman. Many Omanis work in Dubai, "
            "Abu Dhabi, and Sharjah in trade, construction, finance, and professional "
            "services. Oman and the UAE are members of the Gulf Cooperation Council "
            "(GCC), which facilitates movement and documentation across member states. "
            "Arabic documentation from the UAE is accepted by Omani authorities. "
            "The Omani Embassy in Abu Dhabi handles consular matters. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'china', 'dest': 'oman',
        'embassy_city': 'Beijing',
        'intro': (
            "Chinese nationals in Oman include a growing community of business "
            "professionals and construction workers involved in the substantial "
            "Chinese investment in the Sultanate's infrastructure and special economic "
            "zone projects, including the Duqm Special Economic Zone. China and Oman "
            "have strengthened ties under the Belt and Road Initiative. Mandarin "
            "documentation requires certified Arabic translation for Royal Oman Police "
            "registration purposes. The Omani Embassy in Beijing handles consular "
            "matters. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'nigeria', 'dest': 'oman',
        'embassy_city': 'Abuja',
        'intro': (
            "Nigerian nationals in Oman include traders, professionals, and workers "
            "in the trade and service sectors. Nigeria and Oman have bilateral "
            "diplomatic ties, and West African workers have become an increasingly "
            "significant part of the Gulf workforce. English documentation from Nigeria "
            "is generally understood by Omani authorities, though certified Arabic "
            "translation may be required for Royal Oman Police registration. The "
            "Omani Embassy in Abuja handles consular matters. "
            "(Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'vietnam', 'dest': 'oman',
        'embassy_city': 'Hanoi',
        'intro': (
            "Vietnamese nationals in Oman include workers deployed under bilateral "
            "labour agreements in construction, healthcare, domestic service, and "
            "manufacturing sectors. Vietnam and Oman have established labour migration "
            "protocols, and Vietnamese workers are a growing part of the Omani "
            "workforce. Vietnamese documentation requires certified Arabic translation "
            "for Royal Oman Police registration purposes. The Omani Embassy in Hanoi "
            "handles consular matters. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'malaysia', 'dest': 'oman',
        'embassy_city': 'Kuala Lumpur',
        'intro': (
            "Malaysian nationals in Oman include professionals in the oil and gas, "
            "healthcare, and construction sectors, reflecting Malaysia's expertise "
            "in energy and engineering. Malaysia and Oman have bilateral diplomatic "
            "ties and share a Muslim heritage, which eases some procedural elements "
            "for Islamic burial preparations. Malay documentation requires certified "
            "Arabic translation for Royal Oman Police registration and Omani Ministry "
            "of Health purposes. The Omani Embassy in Kuala Lumpur handles consular "
            "matters. (Oman Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R49 -- Greece wave 5
    {
        'origin': 'iraq', 'dest': 'greece',
        'embassy_city': 'Baghdad',
        'intro': (
            "Iraqi nationals in Greece form one of the largest non-EU communities "
            "in the country, following large-scale arrivals through the Eastern "
            "Mediterranean route. Greece has registered tens of thousands of Iraqi "
            "nationals, many of whom have since obtained asylum or residency. Arabic "
            "documentation from Iraq requires certified Greek translation for the "
            "Lixiarcheio (civil registry). The Greek Embassy in Baghdad handles "
            "consular matters. The FCDO advises against all travel to large parts of "
            "Iraq; families should confirm the specific location before planning travel. "
            "(Greek Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'jordan', 'dest': 'greece',
        'embassy_city': 'Amman',
        'intro': (
            "Jordanian nationals and Greek nationals living or travelling in Jordan "
            "form the community most likely to need this corridor. Jordan and Greece "
            "have bilateral diplomatic ties within the Mediterranean framework, and "
            "there is a small but active community of Greek professionals and visitors "
            "engaged in Jordan's tourism and cultural heritage sectors. Arabic "
            "documentation from Jordan requires certified Greek translation for the "
            "Lixiarcheio (civil registry). The Greek Embassy in Amman handles "
            "consular matters. (Greek Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'armenia', 'dest': 'greece',
        'embassy_city': 'Yerevan',
        'intro': (
            "Greece and Armenia have one of the most historically deep bilateral "
            "relationships in the region, rooted in centuries of diaspora history "
            "and the Greek-Armenian communities of the eastern Mediterranean. Greek "
            "Armenians, Armenians with Greek citizenship or residency, and Armenians "
            "with family in Greece maintain strong ties across the two countries. "
            "Armenian documentation requires certified Greek translation for the "
            "Lixiarcheio (civil registry). The Greek Embassy in Yerevan handles "
            "consular matters. (Greek Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'azerbaijan', 'dest': 'greece',
        'embassy_city': 'Baku',
        'intro': (
            "Azerbaijani nationals in Greece include students, professionals, and "
            "a small diaspora community. Azerbaijan and Greece have bilateral trade "
            "and energy ties: Azerbaijan is a significant supplier of natural gas "
            "to Europe through the Southern Gas Corridor, with the Trans Adriatic "
            "Pipeline (TAP) landing in northern Greece. Azerbaijani documentation "
            "requires certified Greek translation for the Lixiarcheio (civil registry). "
            "The Greek Embassy in Baku handles consular matters. "
            "(Greek Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'cyprus', 'dest': 'greece',
        'embassy_city': 'Nicosia',
        'intro': (
            "Cyprus and Greece have uniquely close ties: approximately 80 percent of "
            "Cyprus's population is Greek Cypriot, with strong cultural, linguistic, "
            "and family connections to mainland Greece. Both countries are EU and "
            "Schengen Area members, and many Cypriots hold or are eligible for dual "
            "Cypriot and Greek nationality. Greek-language documentation from Cyprus "
            "is accepted for Lixiarcheio (civil registry) purposes in Greece with "
            "minimal additional requirements, as both are EU and Hague Apostille "
            "members. The Greek Embassy in Nicosia handles consular matters. "
            "(Greek Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R49 -- Austria wave 5
    {
        'origin': 'iraq', 'dest': 'austria',
        'embassy_city': 'Baghdad',
        'intro': (
            "Iraqi nationals form one of Austria's significant refugee and asylum-seeker "
            "communities, with many Iraqis having arrived in Austria since the 2000s "
            "and particularly following the 2015 migration flows. Austria has recognised "
            "thousands of Iraqis under refugee or subsidiary protection status and "
            "maintains an active bilateral relationship. Arabic documentation from Iraq "
            "requires certified German translation for the Austrian Standesamt (civil "
            "registry). The Austrian Embassy in Baghdad handles consular matters. The "
            "FCDO advises against all travel to large parts of Iraq; families should "
            "confirm the specific location before planning travel. "
            "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
        ),
    },
    {
        'origin': 'lebanon', 'dest': 'austria',
        'embassy_city': 'Beirut',
        'intro': (
            "Lebanese nationals and Austrians with Lebanese heritage form a notable "
            "community in Austria, with Lebanese professionals concentrated in Vienna. "
            "Lebanon and Austria have bilateral diplomatic ties and significant "
            "trade and academic connections. Austrian universities have historically "
            "attracted Lebanese students. Arabic documentation from Lebanon requires "
            "certified German translation for the Austrian Standesamt (civil registry). "
            "The Austrian Embassy in Beirut handles consular matters. Families should "
            "monitor FCDO travel advice for Lebanon given the regional security "
            "situation. (Austrian Federal Ministry for European and International "
            "Affairs, BMEIA, 2025.)"
        ),
    },
    {
        'origin': 'bangladesh', 'dest': 'austria',
        'embassy_city': 'Dhaka',
        'intro': (
            "Bangladeshi nationals in Austria include students, professionals, and "
            "a small diaspora community in Vienna and other Austrian cities. Bangladesh "
            "and Austria have bilateral diplomatic relations, and Austrian development "
            "cooperation supports several projects in Bangladesh. Bengali documentation "
            "requires certified German translation for the Austrian Standesamt (civil "
            "registry). The Austrian Embassy in Dhaka handles consular matters. "
            "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
        ),
    },
    {
        'origin': 'georgia', 'dest': 'austria',
        'embassy_city': 'Tbilisi',
        'intro': (
            "Georgian nationals in Austria include students, professionals, and a "
            "growing diaspora, as Georgia's EU Association Agreement and visa "
            "liberalisation have encouraged closer mobility links with Austria and "
            "other EU member states. Austria and Georgia have bilateral diplomatic "
            "ties, and Austria has been active in South Caucasus diplomacy. Georgian "
            "documentation requires certified German translation for the Austrian "
            "Standesamt (civil registry). The Austrian Embassy in Tbilisi handles "
            "consular matters. "
            "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
        ),
    },
    {
        'origin': 'vietnam', 'dest': 'austria',
        'embassy_city': 'Hanoi',
        'intro': (
            "Vietnamese nationals in Austria include an established diaspora community "
            "in Vienna, with roots going back to Vietnamese workers who came to Austria "
            "in the 1980s and subsequent waves of refugees and economic migrants. "
            "Vienna's Vietnamese community is among the most settled in Central Europe. "
            "Austria and Vietnam have bilateral diplomatic and trade ties. Vietnamese "
            "documentation requires certified German translation for the Austrian "
            "Standesamt (civil registry). The Austrian Embassy in Hanoi handles "
            "consular matters. "
            "(Austrian Federal Ministry for European and International Affairs, BMEIA, 2025.)"
        ),
    },
    # R50 -- Denmark wave 5
    {
        'origin': 'ukraine', 'dest': 'denmark',
        'embassy_city': 'Kyiv',
        'intro': (
            "Ukrainian nationals in Denmark include those who arrived following the "
            "2022 Russian invasion, granted temporary protection under the EU Temporary "
            "Protection Directive, alongside a pre-war diaspora of professionals and "
            "students. Denmark has been a significant host for Ukrainian displaced "
            "persons. The FCDO advises against all travel to Ukraine. In stable areas "
            "of Ukraine, Ukrainian documentation requires certified Danish translation "
            "for Danish civil registry purposes; in areas affected by hostilities, "
            "documentation access is severely restricted or impossible. The Danish "
            "Embassy in Kyiv handles consular matters where accessible. "
            "(Danish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'egypt', 'dest': 'denmark',
        'embassy_city': 'Cairo',
        'intro': (
            "Egyptian nationals in Denmark form a notable community in Copenhagen and "
            "other cities, working in trade, professional services, and the hospitality "
            "sector. Egypt and Denmark have bilateral diplomatic ties, with Denmark an "
            "active partner in Euro-Mediterranean dialogue and development cooperation. "
            "Arabic documentation from Egypt requires certified Danish translation for "
            "the Danish civil registry. The Danish Embassy in Cairo handles consular "
            "matters. (Danish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'philippines', 'dest': 'denmark',
        'embassy_city': 'Manila',
        'intro': (
            "Filipino nationals in Denmark include healthcare professionals, maritime "
            "workers, and a small diaspora. Denmark's large maritime and shipping "
            "sector employs many Filipino seafarers, and the Philippines is a "
            "significant source country for Danish healthcare recruitment. Philippine "
            "documentation requires PSA authentication and DFA countersignature. "
            "The Danish Embassy in Manila handles consular matters. "
            "(Danish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'georgia', 'dest': 'denmark',
        'embassy_city': 'Tbilisi',
        'intro': (
            "Georgian nationals in Denmark include students, professionals, and a "
            "small diaspora. Georgia and Denmark have diplomatic ties within the "
            "EU-Georgia Association Agreement framework, and Denmark has supported "
            "Georgian integration and democratic development. Georgian documentation "
            "requires certified Danish translation for the Danish civil registry. "
            "The Danish Embassy in Tbilisi handles consular matters. "
            "(Danish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'indonesia', 'dest': 'denmark',
        'embassy_city': 'Jakarta',
        'intro': (
            "Indonesian nationals in Denmark include students, professionals, and "
            "a small community in Copenhagen and other Danish cities. Indonesia and "
            "Denmark have trade and development cooperation ties, with Danish companies "
            "active in Indonesia's energy, maritime, and environmental sectors. "
            "Bahasa Indonesia documentation requires certified Danish translation for "
            "the Danish civil registry. The Danish Embassy in Jakarta handles "
            "consular matters. (Danish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R50 -- Finland wave 5
    {
        'origin': 'egypt', 'dest': 'finland',
        'embassy_city': 'Cairo',
        'intro': (
            "Egyptian nationals in Finland include students, professionals, and a "
            "small diaspora. Egypt and Finland have diplomatic ties, and Finnish "
            "development and humanitarian engagement with the Nile Valley and "
            "surrounding region has built bilateral links over decades. Arabic "
            "documentation from Egypt requires certified Finnish translation for the "
            "Digi- ja vaestotietovirasto (DVV, Digital and Population Data Services "
            "Agency) registration. The Finnish Embassy in Cairo handles consular "
            "matters. (Finnish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'philippines', 'dest': 'finland',
        'embassy_city': 'Manila',
        'intro': (
            "Filipino nationals in Finland include nurses and other healthcare "
            "professionals, reflecting Finland's active recruitment from the "
            "Philippines for its healthcare and social care sectors, as well as "
            "students and other professionals. Finland and the Philippines have "
            "bilateral labour cooperation, and formal recruitment arrangements "
            "connect the Finnish healthcare sector with Philippine agencies. Philippine "
            "documentation requires PSA authentication and DFA countersignature. "
            "The Finnish Embassy in Manila handles consular matters. "
            "(Finnish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'armenia', 'dest': 'finland',
        'embassy_city': 'Yerevan',
        'intro': (
            "Armenian nationals in Finland include students, professionals, and a "
            "small but established diaspora, as Finland has received Armenian "
            "refugees since the 1990s conflict in Nagorno-Karabakh and subsequent "
            "waves. Finland has been an active supporter of Armenia's EU integration "
            "process and maintains diplomatic ties with Yerevan. Armenian "
            "documentation requires certified Finnish translation for the Digi- ja "
            "vaestotietovirasto (DVV) registration. The Finnish Embassy in Yerevan "
            "handles consular matters. (Finnish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'georgia', 'dest': 'finland',
        'embassy_city': 'Tbilisi',
        'intro': (
            "Georgian nationals in Finland include students, professionals, and a "
            "small diaspora. Finland and Georgia have diplomatic relations, and "
            "Georgia's EU Association Agreement and NATO aspirations have aligned "
            "the two countries in terms of shared values and security cooperation. "
            "Georgian documentation requires certified Finnish translation for the "
            "Digi- ja vaestotietovirasto (DVV) registration. The Finnish Embassy "
            "in Tbilisi handles consular matters. "
            "(Finnish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'azerbaijan', 'dest': 'finland',
        'embassy_city': 'Baku',
        'intro': (
            "Azerbaijani nationals in Finland include students, professionals, and "
            "a small diaspora. Azerbaijan and Finland have diplomatic ties, and "
            "Azerbaijan has become significant to European energy diversification "
            "through the Southern Gas Corridor, deepening bilateral engagement. "
            "Azerbaijani documentation requires certified Finnish translation for "
            "the Digi- ja vaestotietovirasto (DVV). The Finnish Embassy in Baku "
            "handles consular matters. (Finnish Ministry of Foreign Affairs, 2025.)"
        ),
    },
    # R50 -- Italy wave 5
    {
        'origin': 'argentina', 'dest': 'italy',
        'embassy_city': 'Buenos Aires',
        'intro': (
            "Argentina has one of the world's largest communities of Italian descent, "
            "with an estimated 25 million Argentines tracing ancestry to Italy. "
            "Millions of Argentines hold or are eligible for Italian citizenship "
            "through jure sanguinis (bloodline citizenship), reflecting waves of "
            "Italian migration from the 1870s onward. Argentina and Italy are linked "
            "by family, language, and cultural connections at a depth found in few "
            "other country pairs. Spanish documentation (Acta de Defuncion) from "
            "Argentina requires certified Italian translation for prefettura and "
            "anagrafe (civil registry) purposes. The Italian Embassy in Buenos Aires "
            "handles consular matters. "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
    },
    {
        'origin': 'brazil', 'dest': 'italy',
        'embassy_city': 'Brasilia',
        'intro': (
            "Brazil has the world's largest Italian diaspora, with an estimated "
            "30 million Brazilians of Italian ancestry. Italian migration to Brazil, "
            "concentrated in Sao Paulo, Rio Grande do Sul, and Santa Catarina, was "
            "massive from the 1880s to 1960s, and millions of Brazilians hold or are "
            "eligible for Italian citizenship through jure sanguinis. Portugal-language "
            "documentation (Certidao de Obito) from Brazil requires certified Italian "
            "translation for prefettura and anagrafe purposes. The Italian Embassy in "
            "Brasilia and the Consulate General in Sao Paulo handle consular matters. "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
    },
    {
        'origin': 'indonesia', 'dest': 'italy',
        'embassy_city': 'Jakarta',
        'intro': (
            "Indonesian nationals in Italy include students, professionals, and "
            "workers in the domestic service and hospitality sectors in Rome, Milan, "
            "and other Italian cities. Italy and Indonesia have bilateral trade and "
            "diplomatic ties within the G20 framework. Bahasa Indonesia documentation "
            "requires certified Italian translation for the prefettura authorisation "
            "and anagrafe (civil registry) purposes. The Italian Embassy in Jakarta "
            "handles consular matters. "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
    },
    {
        'origin': 'colombia', 'dest': 'italy',
        'embassy_city': 'Bogota',
        'intro': (
            "Colombian nationals form part of Italy's Latin American community, "
            "with Colombians concentrated in Rome, Milan, and Turin working in "
            "service, catering, and professional sectors. Colombia and Italy have "
            "bilateral diplomatic ties and close cultural connections through shared "
            "Romance language heritage. Spanish documentation (Acta de Defuncion) "
            "from Colombia requires certified Italian translation for prefettura and "
            "anagrafe (civil registry) purposes. The Italian Embassy in Bogota "
            "handles consular matters. "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
    },
    {
        'origin': 'sri-lanka', 'dest': 'italy',
        'embassy_city': 'Colombo',
        'intro': (
            "Sri Lankan nationals form one of Italy's largest South Asian communities, "
            "with tens of thousands of Sri Lankans working in domestic service, "
            "cleaning, and catering across Rome, Milan, and other Italian cities. "
            "Sri Lankan migration to Italy has been well established since the 1980s, "
            "and Italy is one of the primary destinations for Sri Lankan economic "
            "migration in Europe. Sinhala and Tamil documentation requires certified "
            "Italian translation for the prefettura authorisation and anagrafe (civil "
            "registry) purposes. The Italian Embassy in Colombo handles consular "
            "matters. "
            "(Italian Ministry of Foreign Affairs and International Cooperation, MAECI, 2025.)"
        ),
    },
    # R50 -- Spain wave 5
    {
        'origin': 'indonesia', 'dest': 'spain',
        'embassy_city': 'Jakarta',
        'intro': (
            "Indonesian nationals in Spain form a small but growing community, "
            "including students and professionals in Barcelona, Madrid, and other "
            "major cities. Spain and Indonesia have bilateral trade and diplomatic "
            "ties within the G20. Bahasa Indonesia documentation requires certified "
            "Spanish translation for the Registro Civil. The Spanish Embassy in "
            "Jakarta handles consular matters. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'vietnam', 'dest': 'spain',
        'embassy_city': 'Hanoi',
        'intro': (
            "Vietnamese nationals in Spain form a small but established community "
            "in Madrid and Barcelona, engaged in trade, hospitality, and service "
            "sectors. Spain and Vietnam have bilateral diplomatic ties, with Spain "
            "a significant trade partner and development cooperation donor for "
            "Vietnam within the EU framework. Vietnamese documentation requires "
            "certified Spanish translation for the Registro Civil. The Spanish "
            "Embassy in Hanoi handles consular matters. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'france', 'dest': 'spain',
        'embassy_city': 'Paris',
        'intro': (
            "France and Spain share one of the longest land borders in the EU, and "
            "hundreds of thousands of French nationals live, work, and retire in "
            "Spain. The French community is concentrated on the Costa Brava, Costa "
            "del Sol, and in Madrid and Barcelona. Both countries are EU and Schengen "
            "Area members, and Hague Apostille document recognition simplifies "
            "cross-border repatriation significantly. French documentation (acte de "
            "deces) requires certified Spanish translation for the Registro Civil "
            "in most cases, though EU procedures apply. The Spanish Embassy in Paris "
            "handles consular matters. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'spain',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portugal and Spain share the Iberian Peninsula and one of Europe's "
            "longest bilateral borders. Hundreds of thousands of Portuguese nationals "
            "live and work in Spain, concentrated in Madrid, the Basque Country, "
            "Catalonia, and the border regions. Both are EU and Schengen Area members. "
            "Portuguese documentation (Certidao de Obito) may require certified "
            "Spanish translation for the Registro Civil; EU Apostille conventions "
            "apply across both countries. The Spanish Embassy in Lisbon handles "
            "consular matters. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
    },
    {
        'origin': 'italy', 'dest': 'spain',
        'embassy_city': 'Rome',
        'intro': (
            "Italian nationals form one of Spain's largest EU expatriate communities, "
            "with Italians concentrated in Barcelona, Madrid, and the Canary Islands. "
            "Italy and Spain are Mediterranean neighbours with longstanding migration "
            "ties dating from the mid-20th century. Both countries are EU and Schengen "
            "Area members. Italian documentation (atto di morte) requires certified "
            "Spanish translation for the Registro Civil, though EU Apostille procedures "
            "apply. The Spanish Embassy in Rome handles consular matters. "
            "(Spanish Ministry of Foreign Affairs, European Union and Cooperation, 2025.)"
        ),
    },
    # R50 -- Netherlands wave 5
    {
        'origin': 'france', 'dest': 'netherlands',
        'embassy_city': 'Paris',
        'intro': (
            "French nationals form one of the Netherlands' larger EU expatriate "
            "communities, concentrated in Amsterdam, The Hague, and Rotterdam. "
            "France and the Netherlands are EU and Schengen Area neighbours with "
            "longstanding bilateral and former colonial ties, and significant numbers "
            "of French nationals work in the Netherlands' international business "
            "environment. French documentation (acte de deces) is accepted by Dutch "
            "authorities without translation in many cases, as French is one of the "
            "accepted major languages. The Dutch Embassy in Paris handles consular "
            "matters. (Dutch Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'germany', 'dest': 'netherlands',
        'embassy_city': 'Berlin',
        'intro': (
            "Germany and the Netherlands share a long land border, and hundreds of "
            "thousands of Germans live in the Netherlands, working in the "
            "cross-border region between North Rhine-Westphalia and the Dutch "
            "provinces of Gelderland, Overijssel, and Limburg. Germany and the "
            "Netherlands are EU and Schengen Area members. German documentation "
            "(Sterbeurkunde) is accepted by the Dutch Burgerlijke Stand (civil "
            "registry) without further translation in most cases, as German is one "
            "of the accepted major languages. The Dutch Embassy in Berlin handles "
            "consular matters. (Dutch Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'spain', 'dest': 'netherlands',
        'embassy_city': 'Madrid',
        'intro': (
            "Spanish nationals form one of the Netherlands' significant EU expatriate "
            "communities, working in Amsterdam, Rotterdam, and other Dutch cities in "
            "technology, finance, and logistics sectors. Spanish migration to the "
            "Netherlands increased during the economic difficulties of 2008-2013 and "
            "has remained steady since. Both countries are EU and Schengen Area "
            "members. Spanish documentation (certificado de defuncion) requires "
            "certified Dutch translation for the Burgerlijke Stand, though EU Apostille "
            "applies. The Dutch Embassy in Madrid handles consular matters. "
            "(Dutch Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'portugal', 'dest': 'netherlands',
        'embassy_city': 'Lisbon',
        'intro': (
            "Portuguese nationals form one of the Netherlands' largest EU migrant "
            "communities, with a long history of migration dating from the 1960s "
            "and 1970s. Portuguese workers have settled in Amsterdam, Rotterdam, and "
            "across the Dutch countryside in agricultural and logistics sectors. "
            "Portugal and the Netherlands are EU and Schengen Area members. Portuguese "
            "documentation (Certidao de Obito) requires certified Dutch translation "
            "for the Burgerlijke Stand; the EU Apostille applies. The Dutch Embassy "
            "in Lisbon handles consular matters. (Dutch Ministry of Foreign Affairs, 2025.)"
        ),
    },
    {
        'origin': 'ethiopia', 'dest': 'netherlands',
        'embassy_city': 'Addis Ababa',
        'intro': (
            "Ethiopian nationals form a significant community in the Netherlands, "
            "with thousands of Ethiopians having sought asylum or settled in Dutch "
            "cities since the 1980s and during subsequent periods of Ethiopian "
            "instability. The Netherlands has been an active development partner and "
            "diplomatic presence in Ethiopia for decades. Amharic documentation "
            "requires certified Dutch translation for the Burgerlijke Stand (civil "
            "registry). The Dutch Embassy in Addis Ababa handles consular matters. "
            "(Dutch Ministry of Foreign Affairs, 2025.)"
        ),
    },
]

# ---------------------------------------------------------------------------
# Generate route content
# ---------------------------------------------------------------------------

def make_doc_key(origin_slug):
    """Return a 2-3 letter key code for the destination (used in dest_key field)."""
    keys = {
        'turkey': 'tr', 'malaysia': 'my', 'oman': 'om', 'greece': 'gr',
        'austria': 'at', 'denmark': 'dk', 'finland': 'fi', 'italy': 'it',
        'spain': 'es', 'netherlands': 'nl',
    }
    return keys.get(origin_slug, origin_slug[:2])


def complexity_to_desc(c):
    labels = {
        'low': 'Established process.',
        'moderate': 'Specialist support recommended.',
        'moderate-high': 'Complex route. Specialist required.',
        'high': 'Complex process. A specialist is essential.',
        'very-high': 'A specialist is essential on this complex route.',
    }
    return labels.get(c, 'Specialist support recommended.')


def render_route(route, variant):
    origin_slug = route['origin']
    dest_slug = route['dest']
    embassy_city = route['embassy_city']
    intro = route['intro']

    od = ORIGIN_DATA[origin_slug]
    dm = DEST_META[dest_slug]

    origin_name = od['name']
    dest_name = dm['name']
    slug = f"{origin_slug}-to-{dest_slug}"

    complexity = od['complexity']
    timeline_avg = od['timeline_avg']
    timeline_fast = od['timeline_fast']
    timeline_complex = od['timeline_complex']
    doc_time = od['doc_time']
    dest_key = dm['key']
    emergency_line = dm['emergency_line']

    desc_note = complexity_to_desc(complexity)
    description = (
        f"Someone has died in {origin_name}. Repatriation to {dest_name} "
        f"takes {timeline_avg}. {desc_note} Contact us 24/7."
    )

    dest_reception = dm['reception']
    dest_consular = dm['consular_template'].format(city=embassy_city)
    arrival_faq = dm['arrival_faq']

    # Build direct_answer_points
    pts = [
        f"Key document: {od['cert_name']} (in {od['cert_lang']})",
        f"Documentation takes {doc_time}. Appoint a specialist on day one.",
        f"British Embassy or High Commission in {embassy_city} registers the death and advises. They cannot fund repatriation.",
        f"Death must be registered with {od['registry']} promptly.",
        f"{dest_name} Embassy in {embassy_city} can advise on documentation. They cannot fund repatriation.",
    ]

    # overview
    overview_body = od['overview']

    # Build YAML content
    pts_yaml = "\n".join(f'  - "{p}"' for p in pts)

    # timeline steps
    step2_action = f"Death registered. {od['cert_name'].capitalize()} obtained."
    step2_timing = (
        f"Death must be registered with {od['registry']}. "
        f"{od['postmortem_trigger']} may delay this step."
    )

    timeline_steps = f"""  - step: 1
    action: "Immediate steps after death"
    timing: "Day of death. Call +44 (0)20 7008 5000 (FCDO) or {emergency_line}."
    responsible: "Family or travel insurer"
  - step: 2
    action: "{step2_action}"
    timing: "{step2_timing}"
    responsible: "Local funeral director and registry"
  - step: 3
    action: "{dest_name} Embassy in {embassy_city} notified"
    timing: "Simultaneous with Step 1. Embassy provides a list of local funeral directors."
    responsible: "Family or repatriation specialist"
  - step: 4
    action: "Embalming and preparation."
    timing: "After body released by authorities."
    responsible: "Licensed local funeral director"
  - step: 5
    action: "All export documentation and permits obtained."
    timing: "Allow {doc_time}. Cannot begin until death certificate issued."
    responsible: "Local funeral director and authorities"
  - step: 6
    action: "Air cargo to {dest_name}"
    timing: "Once all documentation complete."
    responsible: "Repatriation specialist and airline cargo"
  - step: 7
    action: "{dest_name} funeral director takes custody. Receiving funeral director coordinates with local authorities."
    timing: "Within 24 hours of arrival."
    responsible: "Receiving funeral director"
"""

    # FAQs
    faqs = f"""  - question: "How long does repatriation from {origin_name} to {dest_name} take?"
    answer: "In a straightforward case, repatriation from {origin_name} to {dest_name} takes {timeline_avg}. The fastest cases complete in {timeline_fast}. Complex cases can take {timeline_complex} or longer."
  - question: "What should I know first about repatriation from {origin_name}?"
    answer: "Death must be registered with {od['registry']} promptly. {od['postmortem_trigger']} may add time before the body can be released."
  - question: "What documents are required for repatriation from {origin_name} to {dest_name}?"
    answer: "The core documents are: {od['cert_name']} with certified translation where required, embalming certificate, export permit, freedom from infection certificate, and passport of the deceased. Your repatriation coordinator handles obtaining these on your behalf."
  - question: "Does the {dest_name} Embassy in {origin_name} help with repatriation?"
    answer: "The {dest_name} Embassy in {embassy_city} can assist with document authentication and advise on repatriation requirements. They cannot pay for or arrange repatriation. Contact the {dest_name} Embassy in {embassy_city} as soon as possible after the death."
  - question: "Is a post-mortem required when someone dies in {origin_name}?"
    answer: "{od['postmortem_trigger']} may trigger a post-mortem examination. This adds time: the body cannot be released until the authorities authorise it."
  - question: "What happens when the body arrives in {dest_name}?"
    answer: "{arrival_faq}"
  - question: "Can I bring ashes home from {origin_name} instead of repatriating the body?"
    answer: "{od['cremation']} You will need the local death certificate, cremation certificate, and relevant export documentation. Your repatriation specialist can advise on the current position."
"""

    # Links
    links = f"""  upward:
    - url: "/repatriation-from-{origin_slug}/"
      text: "Full {origin_name} repatriation guide"
    - url: "/guides/death-abroad-{origin_slug}/"
      text: "What to do if someone dies in {origin_name}"
    - url: "/{dm['hub_url']}/"
      text: "Repatriation to {dest_name}: overview"
    - url: "/contact/"
      text: "Send an enquiry to our team"
  sideways:
    - url: "/routes/{origin_slug}-to-united-kingdom/"
      text: "Repatriation from {origin_name} to the UK"
    - url: "/routes/{origin_slug}-to-ireland/"
      text: "Repatriation from {origin_name} to Ireland"
"""

    content = f"""---
title: "{origin_name} to {dest_name}: Repatriation Guidance"
description: "{description}"
origin_key: "{origin_slug}"
dest_key: "{dest_key}"
origin_name: "{origin_name}"
dest_name: "{dest_name}"
origin_slug: "{origin_slug}"
dest_slug: "{dest_slug}"
slug: "{slug}"
template_variant: "{variant}"
route_complexity: "{complexity}"
timeline_avg: "{timeline_avg}"
timeline_fast: "{timeline_fast}"
timeline_complex: "{timeline_complex}"
embassy_city: "{embassy_city}"
doc_processing_time: "{doc_time}"
date: 2026-05-01
direct_answer_heading: "Repatriation from {origin_name} to {dest_name}: what to expect"
direct_answer_intro: "{intro}"
direct_answer_points:
{pts_yaml}
overview_heading: "What happens after a death in {origin_name}"
overview_body: "{overview_body}"
dest_reception: "{dest_reception}"
dest_consular: "{dest_consular}"
timeline_steps:
{timeline_steps}faqs:
{faqs}links:
{links}---
"""
    return content


def main():
    os.makedirs(ROUTES_DIR, exist_ok=True)
    variant_idx = START_VARIANT
    created = []

    for route in ROUTES:
        variant = VARIANTS[variant_idx % 5]
        slug = f"{route['origin']}-to-{route['dest']}"
        path = os.path.join(ROUTES_DIR, f"{slug}.md")

        if os.path.exists(path):
            print(f"SKIP (exists): {slug}")
            variant_idx += 1
            continue

        content = render_route(route, variant)

        # QA: check for em dashes
        if '--' in content.replace('---', '').replace('--gc', '') or '—' in content:
            print(f"ERROR em dash in {slug}")
            continue

        # QA: banned vocab check
        banned = [
            'delve', 'meticulous', 'comprehensive', 'tailored', 'navigate',
            'leverage', 'seamless', 'robust', 'crucial', 'utilize', 'intricate',
            'paramount', 'pivotal', 'embark', 'foster', 'elevate', 'unleash',
            'unlock', 'harness', 'streamline', 'holistic', 'realm',
            'groundbreaking', 'transformative', 'synergy', 'reimagine',
            'bustling', 'nestled', 'nuanced', 'illuminate', 'encompasses',
            'proactive', 'ubiquitous', 'quintessential', 'moreover', 'furthermore',
        ]
        lower_content = content.lower()
        found_banned = [w for w in banned if w in lower_content]
        if found_banned:
            print(f"ERROR banned vocab in {slug}: {found_banned}")
            continue

        # QA: no prices
        price_patterns = ['prices start', 'from £', 'from $', 'cost from', 'price from']
        if any(p in lower_content for p in price_patterns):
            print(f"ERROR price language in {slug}")
            continue

        with open(path, 'w') as f:
            f.write(content)

        print(f"CREATED ({variant}): {slug}")
        created.append((slug, variant))
        variant_idx += 1

    print(f"\nTotal created: {len(created)}")
    for slug, v in created:
        print(f"  [{v}] {slug}")


if __name__ == '__main__':
    main()
