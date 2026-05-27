"""
Route Page Generator — Repatriate Service
Stage 3.ROUTE-A

Generates Hugo Markdown route pages for origin x destination country pairs.
All content is frontmatter-driven. Template: site/layouts/routes/single.html.
Skip-if-exists: never overwrites an existing file.
Runs QA gate inline — rejects pages that fail hard checks.

Usage:
  python generate_routes.py                # generate all routes in ROUTES list
  python generate_routes.py --dry-run      # QA check only, no files written

Output: site/content/routes/{origin-slug}-to-{dest-slug}.md
"""

import json
import os
import hashlib
import sys
import re

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(REPO_ROOT, "data", "countries_repatriation.json")
CONTENT_DIR = os.path.join(REPO_ROOT, "site", "content", "routes")
os.makedirs(CONTENT_DIR, exist_ok=True)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    COUNTRIES = json.load(f)["countries"]

DEST_DATA = {
    "uk": {
        "name": "United Kingdom", "slug": "united-kingdom",
        "reception": "The UK funeral director takes custody at the cargo terminal. All foreign documentation must be in certified English. The coroner for the district where the funeral will take place is notified. Straightforward cases with complete documentation proceed to funeral arrangements. Deaths involving an overseas investigation may require coroner review before burial or cremation is authorised.",
        "consular": "FCDO 24-hour emergency line: +44 (0)20 7008 5000. The FCDO can provide information and a list of local funeral directors. They cannot pay for or arrange repatriation.",
    },
    "ie": {
        "name": "Ireland", "slug": "ireland",
        "reception": "The Irish funeral director takes custody at the cargo terminal. All foreign documentation must be in certified English. The Coroner for the district is notified. Straightforward cases with complete documentation proceed to funeral arrangements without delay.",
        "consular": "Department of Foreign Affairs emergency line: +353 1 408 2000 (24 hours). The Irish Embassy in the country of death can register the death and advise on documentation. They cannot pay for or arrange repatriation.",
    },
}

BANNED_WORDS = [
    "delve", "tapestry", "robust", "seamless", "elevate", "foster",
    "revolutionise", "game-changer", "empower", "navigate",
    "comprehensive", "meticulous", "bustling", "vibrant",
]
SAFETY_PATTERNS = ["guarantee", "100% safe", "risk-free", "guaranteed protection"]
PRICE_PATTERNS = ["\u00a3", "GBP", "USD", "\u20ac"]

TITLE_TEMPLATES = [
    "{origin} to {dest} Repatriation: Guidance for British Families",
    "{origin} Repatriation to {dest}: Every Step Explained",
    "Repatriation from {origin} to {dest}: 24/7 Support",
    "{origin} to {dest}: Funeral Repatriation for UK Families",
]
DESC_TEMPLATES = [
    "Repatriation from {origin} to {dest} typically takes {avg}. {doc_note} We guide British families through every step. Contact us 24/7.",
    "Someone has died in {origin}. Repatriation to {dest} takes {avg} in a straightforward case. Documentation, flights and UK handover all handled.",
    "{origin} to {dest} repatriation: {avg} typical timeline. Expert guidance for British families. WhatsApp or enquiry form.",
]
DA_INTRO_TEMPLATES = [
    "Repatriation from {origin} to {dest} follows a clear process once the right specialist is appointed. Documentation runs through local authorities and typically takes {doc_time} to complete.",
    "Getting a loved one home from {origin} to {dest} is entirely achievable. The process follows {origin}s civil registration and export system. Most cases take {avg} from death to arrival.",
    "If someone has died in {origin} and you need to bring them home to {dest}, appoint a UK repatriation specialist as the first step. They coordinate everything from the {origin} side.",
    "Repatriation from {origin} is a route our team handles regularly. The process involves local documentation, cargo booking, and {dest} reception. Typical timeline: {avg}.",
]
OVERVIEW_H_TEMPLATES = [
    "What happens after a death in {origin}",
    "The repatriation process from {origin}",
    "Key steps for {origin} to {dest} repatriation",
    "How repatriation from {origin} works",
]


def esc(s):
    s = str(s)
    s = s.replace("\u2014", ",").replace("\u2013", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace('"', "'")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def clamp(s, n=155):
    s = esc(s)
    return s if len(s) <= n else s[:n - 3].rsplit(" ", 1)[0] + "..."


def pick(templates, slug):
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    return templates[h % len(templates)]


def generate_route_md(origin_key, dest_key):
    d = COUNTRIES[origin_key]
    oname = esc(d.get("name") or d.get("country_name", origin_key.title()))
    origin_slug = d.get("slug", origin_key)
    dest = DEST_DATA[dest_key]
    dname = dest["name"]
    dest_slug = dest["slug"]
    slug = f"{origin_slug}-to-{dest_slug}"
    tl = d.get("typical_timeline", {})
    avg = esc(tl.get("average_case", "varies"))
    fast = esc(tl.get("fastest_case", "varies"))
    complex_ = esc(tl.get("complex_case", "varies"))
    proc = d.get("repatriation_process", {})
    docs = proc.get("step_6_documentation", {})
    doc_time = esc(docs.get("processing_time", "varies"))
    doc_list = docs.get("documents_needed", [])
    emb = d.get("embassy_contacts", {}).get("british_embassy", {})
    emb_city = esc(emb.get("city", ""))
    pm = d.get("post_mortem", {})
    pm_when = esc(pm.get("when_required", "") or "")
    pm_impact = esc(pm.get("impact_on_timeline", "several weeks") or "several weeks")
    s1 = proc.get("step_1_immediate", {})
    s2 = proc.get("step_2_death_certificate", {})
    s3 = proc.get("step_3_embassy_notification", {})
    s4 = proc.get("step_4_embalming", {})
    s7 = proc.get("step_7_transport", {})

    title_tpl = pick(TITLE_TEMPLATES, slug)
    title = title_tpl.format(origin=oname, dest=dname)
    if len(title) > 60:
        title = f"{oname} to {dname}: Repatriation Guidance"
    if len(title) > 60:
        title = f"{oname} to {dname} Repatriation"

    dnote = f"Documentation takes {doc_time}." if doc_time and doc_time != "varies" else ""
    desc_tpl = pick(DESC_TEMPLATES, slug + "d")
    desc = clamp(desc_tpl.format(origin=oname, dest=dname, avg=avg, doc_note=dnote), 155)

    da_intro_tpl = pick(DA_INTRO_TEMPLATES, slug + "da")
    da_intro = esc(da_intro_tpl.format(origin=oname, dest=dname, avg=avg, doc_time=doc_time))

    da_points = []
    if doc_list:
        da_points.append(f"Key documents: {esc(doc_list[0])} and {esc(doc_list[1]) if len(doc_list) > 1 else 'embalming certificate'}")
    if doc_time and doc_time != "varies":
        da_points.append(f"Documentation takes {doc_time}. Appoint a specialist on day one.")
    if emb_city:
        da_points.append(f"British Embassy in {emb_city} registers the death and advises. They cannot fund repatriation.")
    if pm_when:
        da_points.append(f"Post-mortem may be required: {pm_when[:120].rstrip('.')}.")

    overview_h = pick(OVERVIEW_H_TEMPLATES, slug + "oh").format(origin=oname, dest=dname)
    s1_det = esc((s1.get("details", "") or s1.get("notes", "")))[:300]
    s2_det = esc((s2.get("details", "") or s2.get("notes", "")))[:200]
    overview_body = (s1_det + " " + s2_det).strip()[:450]

    steps = [
        {"step": 1, "action": esc(s1.get("title", "Notify local authorities and a UK repatriation specialist")), "timing": "Day of death. FCDO 24hr: +44 (0)20 7008 5000.", "responsible": "Family or travel insurer"},
        {"step": 2, "action": esc(s2.get("title", "Death certificate obtained from local civil registry")), "timing": esc((s2.get("notes", "") or s2.get("details", ""))[:100] or "Varies by country and circumstances"), "responsible": "Local funeral director and registry"},
        {"step": 3, "action": esc(s3.get("title", "British Embassy notified and death registered with UK authorities")), "timing": "Simultaneous with Step 1. Embassy provides a list of local funeral directors.", "responsible": "Family or repatriation specialist"},
        {"step": 4, "action": esc(s4.get("title", "Embalming and zinc-lined coffin preparation")), "timing": esc((s4.get("notes", "") or s4.get("details", ""))[:100] or "After body released by authorities. Zinc-lined coffin required for air transport."), "responsible": "Licensed local funeral director"},
        {"step": 5, "action": "Complete export documentation and obtain all permits", "timing": f"Allow {doc_time}. Cannot begin until death certificate issued.", "responsible": "Local funeral director and authorities"},
        {"step": 6, "action": esc(s7.get("title", "Air cargo booked and body transported to destination")), "timing": "Once all documentation is complete and cleared.", "responsible": "Repatriation specialist and airline cargo"},
        {"step": 7, "action": f"{dname} funeral director takes custody. Coroner notified.", "timing": "Within 24 hours of arrival.", "responsible": "Receiving funeral director"},
    ]

    faqs = [
        {"question": f"How long does repatriation from {oname} to {dname} take?", "answer": f"In a straightforward case, repatriation from {oname} to {dname} takes {avg}. The fastest cases complete in {fast} when documentation is issued promptly. Complex cases involving a post-mortem, investigation, or remote location can take {complex_} or longer."},
        {"question": f"What documents are required for repatriation from {oname}?", "answer": "The core documents are: " + (", ".join(esc(x) for x in doc_list[:5]) if doc_list else "local death certificate, embalming certificate, freedom from infection certificate, and airline cargo documentation") + ". Your repatriation coordinator handles obtaining these on your behalf."},
        {"question": f"Does the British Embassy in {oname} help with repatriation?", "answer": f"The British Embassy in {emb_city if emb_city else oname} can register the death with UK authorities, provide a list of local funeral directors, and advise on documentation. They cannot pay for or arrange repatriation. FCDO 24-hour emergency line: +44 (0)20 7008 5000."},
        {"question": f"Is a post-mortem required for British nationals who die in {oname}?" if pm_when else f"What is the first step when someone dies in {oname}?", "answer": f"{pm_when[:250].rstrip('.')}. This adds time: {pm_impact}. The body cannot be released for repatriation until authorities authorise it." if pm_when else f"Notify a UK repatriation specialist and the FCDO emergency line (+44 (0)20 7008 5000) on the day of death. Do not instruct a local funeral director independently before engaging a UK specialist, as this can complicate documentation."},
        {"question": f"What happens when the body arrives in {dname}?", "answer": esc(dest["reception"])},
        {"question": f"Can I bring ashes home from {oname} instead of repatriating the body?", "answer": f"Yes. Cremation in {oname} and bringing ashes home to {dname} is often simpler and less costly than full body repatriation. You will need the local death certificate, cremation certificate, and possibly an export permit. See our bringing ashes home guide for the full documentation list."},
    ]

    upward = [
        {"url": f"/repatriation-from-{origin_slug}/", "text": f"Full {oname} repatriation guide"},
        {"url": f"/guides/death-abroad-{origin_slug}/", "text": f"What to do if someone dies in {oname}"},
        {"url": f"/embassy-contacts/{origin_slug}/", "text": f"British Embassy in {oname}"},
        {"url": "/contact/", "text": "Send an enquiry to our team"},
    ]
    sideways = [
        {"url": f"/routes/{dest_slug}-to-{origin_slug}/", "text": f"Repatriation from {dname} to {oname}"},
        {"url": f"/routes/{origin_slug}-to-{'ireland' if dest_key == 'uk' else 'united-kingdom'}/", "text": f"Repatriation from {oname} to {'Ireland' if dest_key == 'uk' else 'the UK'}"},
    ]

    try:
        n = int(avg.split("-")[0].replace(" days", "").replace(" weeks", "").strip())
        complexity = "low" if ("day" in avg and n <= 10) else ("high" if ("week" in avg and n >= 4) else "moderate")
    except Exception:
        complexity = "moderate"

    L = ["---"]
    L.append(f'title: "{esc(title)}"')
    L.append(f'description: "{esc(desc)}"')
    L.append("layout: route")
    L.append(f'origin_key: "{origin_key}"')
    L.append(f'dest_key: "{dest_key}"')
    L.append(f'origin_name: "{oname}"')
    L.append(f'dest_name: "{dname}"')
    L.append(f'origin_slug: "{origin_slug}"')
    L.append(f'dest_slug: "{dest_slug}"')
    L.append(f'slug: "{slug}"')
    L.append(f'route_complexity: "{complexity}"')
    L.append(f'timeline_avg: "{avg}"')
    L.append(f'timeline_fast: "{fast}"')
    L.append(f'timeline_complex: "{complex_}"')
    L.append(f'embassy_city: "{emb_city}"')
    L.append(f'doc_processing_time: "{doc_time}"')
    L.append(f'direct_answer_heading: "Repatriation from {oname} to {dname}: what to expect"')
    L.append(f'direct_answer_intro: "{da_intro}"')
    L.append("direct_answer_points:")
    for pt in da_points:
        L.append(f'  - "{esc(pt)}"')
    L.append(f'overview_heading: "{esc(overview_h)}"')
    L.append(f'overview_body: "{esc(overview_body)}"')
    L.append(f'dest_reception: "{esc(dest["reception"])}"')
    L.append(f'dest_consular: "{esc(dest["consular"])}"')
    L.append("timeline_steps:")
    for s in steps:
        L.append(f'  - step: {s["step"]}')
        L.append(f'    action: "{esc(s["action"])}"')
        L.append(f'    timing: "{esc(s["timing"])}"')
        L.append(f'    responsible: "{esc(s["responsible"])}"')
    L.append("faqs:")
    for faq in faqs:
        L.append(f'  - question: "{esc(faq["question"])}"')
        L.append(f'    answer: "{esc(faq["answer"])}"')
    L.append("links:")
    L.append("  upward:")
    for lk in upward:
        L.append(f'    - url: "{lk["url"]}"')
        L.append(f'      text: "{esc(lk["text"])}"')
    L.append("  sideways:")
    for lk in sideways:
        L.append(f'    - url: "{lk["url"]}"')
        L.append(f'      text: "{esc(lk["text"])}"')
    L.append("---")
    return "\n".join(L)


def qa_check(md, slug):
    errors, warnings = [], []
    lines = md.split("\n")
    title_val = next((l.replace('title: "', "").rstrip('"') for l in lines if l.startswith("title:")), "")
    desc_val = next((l.replace('description: "', "").rstrip('"') for l in lines if l.startswith("description:")), "")
    faq_count = md.count("  - question:")
    step_count = md.count("  - step:")
    link_count = md.count("    - url:")
    if len(title_val) > 60:
        errors.append(f"Title too long: {len(title_val)} chars")
    if len(title_val) < 20:
        errors.append(f"Title too short: {len(title_val)} chars")
    if len(desc_val) > 155:
        errors.append(f"Description too long: {len(desc_val)} chars")
    if faq_count < 4:
        errors.append(f"Only {faq_count} FAQs (minimum 4)")
    if step_count < 5:
        errors.append(f"Only {step_count} timeline steps (minimum 5)")
    if link_count < 3:
        errors.append(f"Only {link_count} internal links (minimum 3)")
    if "\u2014" in md:
        errors.append("Em dash present")
    for w in BANNED_WORDS:
        if re.search(r"\b" + re.escape(w) + r"\b", md, re.IGNORECASE):
            errors.append(f"Banned word: '{w}'")
    for p in SAFETY_PATTERNS:
        if p.lower() in md.lower():
            errors.append(f"YMYL violation: '{p}'")
    for p in PRICE_PATTERNS:
        if p in md:
            errors.append(f"Price reference found: '{p}'")
    if "+447" not in md and "/contact/" not in md:
        warnings.append("No WhatsApp or /contact/ link found")
    return errors, warnings


ROUTES = [
    ("spain", "uk"), ("thailand", "uk"), ("uae", "uk"), ("usa", "uk"),
    ("australia", "uk"), ("greece", "uk"), ("cyprus", "uk"), ("turkey", "uk"),
    ("philippines", "uk"), ("spain", "ie"), ("thailand", "ie"), ("uae", "ie"),
    ("usa", "ie"), ("australia", "ie"), ("france", "uk"), ("italy", "uk"),
    ("portugal", "uk"), ("india", "uk"), ("kenya", "uk"), ("egypt", "uk"),
    ("vietnam", "uk"), ("germany", "uk"), ("morocco", "uk"),
    ("sri-lanka", "uk"), ("south-africa", "uk"),
]

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    generated = skipped = errors_total = 0
    for origin_key, dest_key in ROUTES:
        if origin_key not in COUNTRIES:
            print(f"  SKIP (not in dataset): {origin_key}")
            continue
        if dest_key not in DEST_DATA:
            print(f"  SKIP (unknown destination): {dest_key}")
            continue
        d = COUNTRIES[origin_key]
        origin_slug = d.get("slug", origin_key)
        dest_slug = DEST_DATA[dest_key]["slug"]
        slug = f"{origin_slug}-to-{dest_slug}"
        filepath = os.path.join(CONTENT_DIR, f"{slug}.md")
        if os.path.exists(filepath) and not dry_run:
            skipped += 1
            continue
        md = generate_route_md(origin_key, dest_key)
        errs, warns = qa_check(md, slug)
        if errs:
            print(f"  [FAIL] {slug}")
            for e in errs:
                print(f"    ERROR: {e}")
            errors_total += 1
            continue
        if warns:
            for w in warns:
                print(f"  [WARN] {slug}: {w}")
        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md)
            generated += 1
            print(f"  [PASS] {slug}")
        else:
            print(f"  [DRY-RUN PASS] {slug}")
    print(f"\nDone. Generated: {generated} | Skipped: {skipped} | Errors: {errors_total}")
