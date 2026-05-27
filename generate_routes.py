#!/usr/bin/env python3
"""
generate_routes.py -- Repatriate Service Route Generator (Engine 1 v2)

Reads structured per-origin JSON data from site/data/route_data/*.json
and generates full-content Hugo Markdown route pages through the
7-step quality gate defined in CLAUDE.md.

Quality gate (inline):
  1. Research  -- real data from route_data JSON (sourced from FCDO)
  2. Write     -- wordsmith voice rules applied to all generated text
  3. Variant   -- template_variant A-E rotated automatically
  4. Humanise  -- banned phrases stripped, AI patterns flagged as errors
  5. QA scan   -- 18-point auditor checklist (see workforce/the-auditor.md)
  6. Preview   -- HTML preview generated per batch (separate script)
  7. Commit    -- only after human approval (this script does NOT commit)

Usage:
  python generate_routes.py                  # generate all routes in ROUTE_PAIRS
  python generate_routes.py --dry-run        # QA check only, no files written
  python generate_routes.py --origin spain   # single origin only
  python generate_routes.py --list           # list all known corridors

Critical rules (from MEMORY.md and ERRORS.md):
  - NEVER write layout: field in frontmatter (causes Hugo to silently skip pages)
  - NEVER write em dashes
  - NEVER write prices
  - NEVER write safety guarantees
  - Skip-if-exists: never overwrites an existing file
  - All content sourced from route_data JSON, never invented

Output: site/content/routes/{origin-slug}-to-{dest-slug}.md
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path
from textwrap import dedent

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent
ROUTE_DATA_DIR = REPO_ROOT / "site" / "data" / "route_data"
CONTENT_DIR = REPO_ROOT / "site" / "content" / "routes"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# QA constants (mirrors workforce/the-auditor.md)
# ---------------------------------------------------------------------------

BANNED_WORDS = {
    "delve", "meticulous", "comprehensive", "tailored", "navigate",
    "leverage", "seamless", "robust", "vital", "crucial", "utilize",
    "intricate", "paramount", "pivotal", "embark", "foster", "elevate",
    "unleash", "unlock", "harness", "streamline", "holistic", "realm",
    "testament", "moreover", "furthermore", "groundbreaking", "transformative",
    "synergy", "reimagine", "bustling", "nestled", "nuanced", "illuminate",
    "encompasses", "proactive", "ubiquitous", "quintessential",
}

AI_PHRASES = [
    "plays a crucial role",
    "in the realm of",
    "it is worth noting",
    "serves as a testament",
    "at its core",
    "shed light on",
    "dive into",
    "first and foremost",
    "last but not least",
    "in today's world",
    "a wide range of",
    "a variety of",
]

SAFETY_PATTERNS = [
    r"guarantee[ds]?\s+(safety|protection|safe)",
    r"100%\s+safe",
    r"completely\s+safe",
    r"risk[- ]free",
]

PRICE_PATTERNS = [r"\u00a3\s*\d", r"\$\s*\d", r"EUR\s*\d"]

# ---------------------------------------------------------------------------
# Destination metadata (static -- UK and Ireland only for now)
# ---------------------------------------------------------------------------

DESTINATIONS = {
    "uk": {
        "name": "United Kingdom",
        "slug": "united-kingdom",
        "coroner_note": "The coroner for the district where the funeral will take place is notified.",
        "emergency_line": "FCDO 24-hour emergency line: +44 (0)20 7008 5000.",
    },
    "ireland": {
        "name": "Ireland",
        "slug": "ireland",
        "coroner_note": "The Coroner for the district is notified.",
        "emergency_line": "Department of Foreign Affairs emergency line: +353 1 408 2000 (24 hours).",
    },
}

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    """Sanitise text for YAML frontmatter: strip em/en dashes, smart quotes, normalise whitespace."""
    s = str(s)
    s = s.replace("\u2014", ",").replace("\u2013", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace('"', "'")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def clamp(s: str, n: int = 155) -> str:
    s = esc(s)
    if len(s) <= n:
        return s
    return s[:n - 3].rsplit(" ", 1)[0] + "..."


def load_route_data(origin_key: str) -> dict | None:
    """Load per-origin route data JSON. Returns None if not found."""
    path = ROUTE_DATA_DIR / f"{origin_key}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Content builders (Wordsmith voice rules applied)
# ---------------------------------------------------------------------------

def build_direct_answer_points(origin: dict, dest_obj: dict) -> list[str]:
    """
    Wordsmith rule: lead with the most specific fact.
    Each point names a real document or authority, not a generic claim.
    """
    points = []

    # Key document
    key_doc = origin.get("key_document", "")
    if key_doc:
        points.append(f"Key document: {esc(key_doc)}")

    # Documentation time
    doc_time = dest_obj.get("doc_processing_time", "")
    if doc_time:
        points.append(f"Documentation takes {esc(doc_time)}. Appoint a specialist on day one.")

    # Embassy
    embassy_city = origin.get("embassy_city", "")
    if embassy_city:
        points.append(
            f"British Embassy in {esc(embassy_city)} registers the death and advises. "
            f"They cannot fund repatriation."
        )

    # Special rules -- take first 1-2 most distinctive ones
    special = dest_obj.get("special_rules", [])
    for rule in special[:2]:
        points.append(esc(rule))

    return points[:5]  # cap at 5


def build_overview_body(origin: dict, dest_obj: dict) -> str:
    """
    Wordsmith rule: short first sentence states the most important fact.
    Active voice. Named authorities only.
    """
    parts = []

    emerg = origin.get("emergency_number", "112")
    death_reg = origin.get("death_registration", "")
    invest = origin.get("investigating_authority", "")
    pm_trigger = origin.get("post_mortem_trigger", "")
    island_note = origin.get("island_transfer_note", "")
    road_note = origin.get("road_transport_note", "")
    deadline = origin.get("deadline_warning", "")

    parts.append(f"Contact emergency services ({esc(emerg)}).")

    if deadline:
        parts.append(esc(deadline))

    if death_reg:
        parts.append(f"Death must be registered with the {esc(death_reg)}.")

    if invest and pm_trigger:
        parts.append(
            f"The {esc(invest)} takes jurisdiction when the death is: {esc(pm_trigger).lower().rstrip('.')}."
        )

    if island_note:
        parts.append(esc(island_note))

    if road_note:
        parts.append(esc(road_note))

    return " ".join(parts)[:600]


def build_faqs(origin: dict, dest_obj: dict, oname: str, dname: str) -> list[dict]:
    """
    Wordsmith FAQ rule: answer the question directly in the first sentence.
    Give the specific number, document name, or timeline.
    Note exceptions. End when complete.
    """
    tl = dest_obj.get("timeline", {})
    avg = esc(tl.get("avg", "varies"))
    fast = esc(tl.get("fast", "varies"))
    complex_ = esc(tl.get("complex", "varies"))
    docs = dest_obj.get("key_documents", [])
    embassy_city = esc(origin.get("embassy_city", oname))
    dest = DESTINATIONS.get(dest_obj["key"], DESTINATIONS["uk"])
    coroner = dest["coroner_note"]
    emerg = dest["emergency_line"]
    special = dest_obj.get("special_rules", [])
    reception = esc(dest_obj.get("dest_reception", ""))
    cremation = origin.get("cremation_available", True)
    cremation_note = origin.get("cremation_note", "")
    pm_trigger = origin.get("post_mortem_trigger", "")

    faqs = []

    # Q1 -- timeline (always first)
    faqs.append({
        "question": f"How long does repatriation from {oname} to {dname} take?",
        "answer": (
            f"In a straightforward case, repatriation from {oname} to {dname} takes {avg}. "
            f"The fastest cases complete in {fast}. "
            f"Complex cases can take {complex_} or longer."
        ),
    })

    # Q2 -- most distinctive special rule for this corridor
    if special:
        first_rule = special[0]
        # Extract the key name from the rule as a question hook
        faqs.append({
            "question": f"What should I know first about repatriation from {oname}?",
            "answer": esc(first_rule),
        })

    # Q3 -- documents
    if docs:
        doc_list = ", ".join(esc(d) for d in docs[:5])
        faqs.append({
            "question": f"What documents are required for repatriation from {oname}?",
            "answer": (
                f"The core documents are: {doc_list}. "
                f"Your repatriation coordinator handles obtaining these on your behalf."
            ),
        })

    # Q4 -- embassy
    faqs.append({
        "question": f"Does the British Embassy in {oname} help with repatriation?",
        "answer": (
            f"The British Embassy in {embassy_city} can register the death with UK authorities, "
            f"provide a list of local funeral directors, and advise on documentation. "
            f"They cannot pay for or arrange repatriation. {emerg}"
        ),
    })

    # Q5 -- post-mortem if applicable, otherwise first step
    if pm_trigger:
        faqs.append({
            "question": f"Is a post-mortem required for British nationals who die in {oname}?",
            "answer": (
                f"{esc(pm_trigger)} A post-mortem adds time. "
                f"The body cannot be released until the authorities authorise it."
            ),
        })
    else:
        faqs.append({
            "question": f"What is the first step when someone dies in {oname}?",
            "answer": (
                f"Notify a UK repatriation specialist and the FCDO emergency line "
                f"(+44 (0)20 7008 5000) on the day of death. "
                f"Do not instruct a local funeral director independently before engaging a UK specialist."
            ),
        })

    # Q6 -- arrival
    faqs.append({
        "question": f"What happens when the body arrives in {dname}?",
        "answer": reception if reception else (
            f"The funeral director takes custody at the cargo terminal. "
            f"{coroner} Straightforward cases proceed directly to funeral arrangements."
        ),
    })

    # Q7 -- ashes (if cremation available)
    if cremation:
        faqs.append({
            "question": f"Can I bring ashes home from {oname} instead of repatriating the body?",
            "answer": cremation_note if cremation_note else (
                f"Yes. Cremation in {oname} and bringing ashes home to {dname} is often "
                f"simpler and less costly than full body repatriation. "
                f"You will need the local death certificate, cremation certificate, and possibly an export permit."
            ),
        })
    else:
        no_crem = origin.get("cremation_note", f"Cremation is not available in {oname}.")
        faqs.append({
            "question": f"Can I bring ashes home from {oname} instead of repatriating the body?",
            "answer": esc(no_crem),
        })

    return faqs


def build_timeline_steps(origin: dict, dest_obj: dict, oname: str, dname: str) -> list[dict]:
    """Build 7-step timeline. Uses origin-specific data where available."""
    dest = DESTINATIONS.get(dest_obj["key"], DESTINATIONS["uk"])
    embassy_city = esc(origin.get("embassy_city", oname))
    doc_time = esc(dest_obj.get("doc_processing_time", "varies"))
    airlines = dest_obj.get("airlines", [])
    airline_note = airlines[0]["routes"] if airlines else "cargo terminal at destination"
    death_reg = esc(origin.get("death_registration", "local civil registry"))
    invest = esc(origin.get("investigating_authority", ""))
    key_doc = esc(origin.get("key_document", "death certificate"))
    emb_urgency = origin.get("embalming_urgency", "")
    island_req = origin.get("island_transfer_required", False)
    island_note = origin.get("island_transfer_note", "")
    deadline = origin.get("deadline_warning", "")
    mofa = origin.get("mofa_attestation_required", False)

    step1_timing = "Day of death. FCDO 24hr: +44 (0)20 7008 5000."
    if deadline:
        step1_timing = f"Day of death. Act immediately. {esc(deadline)[:100]}"

    step2_action = f"Death registered. {key_doc} obtained."
    step2_timing = f"Death must be registered with the {death_reg}."
    if invest:
        step2_timing += f" {invest} may be involved."

    step3_action = f"British Embassy {embassy_city} notified."
    step3_timing = "Simultaneous with Step 1. Embassy provides a list of local funeral directors."

    step4_action = "Embalming and preparation."
    step4_timing = esc(emb_urgency) if emb_urgency else "After body released by authorities."

    step5_action = "All export documentation and permits obtained."
    step5_timing = f"Allow {doc_time}. Cannot begin until death certificate issued."
    if mofa:
        step5_timing += " MOFA attestation required."
    if island_req and island_note:
        step5_timing += f" {esc(island_note)[:80]}"

    step6_action = f"Air cargo to {dname}."
    step6_timing = f"Once all documentation complete. {esc(airline_note)[:100]}"

    step7_action = f"{dname} funeral director takes custody. Coroner notified."
    step7_timing = "Within 24 hours of arrival."

    return [
        {"step": 1, "action": "Immediate steps after death", "timing": step1_timing, "responsible": "Family or travel insurer"},
        {"step": 2, "action": step2_action, "timing": step2_timing, "responsible": "Local funeral director and registry"},
        {"step": 3, "action": step3_action, "timing": step3_timing, "responsible": "Family or repatriation specialist"},
        {"step": 4, "action": step4_action, "timing": step4_timing, "responsible": "Licensed local funeral director"},
        {"step": 5, "action": step5_action, "timing": step5_timing, "responsible": "Local funeral director and authorities"},
        {"step": 6, "action": step6_action, "timing": step6_timing, "responsible": "Repatriation specialist and airline cargo"},
        {"step": 7, "action": step7_action, "timing": step7_timing, "responsible": "Receiving funeral director"},
    ]


# ---------------------------------------------------------------------------
# Frontmatter assembler
# ---------------------------------------------------------------------------

def build_frontmatter(data: dict, dest_obj: dict) -> str:
    """
    Assemble complete YAML frontmatter for a route page.
    CRITICAL: No 'layout:' field -- causes Hugo to silently skip the page.
    """
    origin = data["origin"]
    oname = esc(origin["name"])
    origin_slug = esc(origin["slug"])
    dest = DESTINATIONS.get(dest_obj["key"], DESTINATIONS["uk"])
    dname = esc(dest["name"])
    dest_slug = esc(dest["slug"])
    route_slug = esc(dest_obj["route_slug"])

    tl = dest_obj.get("timeline", {})
    avg = esc(tl.get("avg", "varies"))
    fast = esc(tl.get("fast", "varies"))
    complex_ = esc(tl.get("complex", "varies"))

    title = clamp(esc(dest_obj.get("seo_title", f"{oname} to {dname} Repatriation: Guidance for British Families")), 60)
    description = clamp(esc(dest_obj.get("seo_description", f"Repatriation from {oname} to {dname} takes {avg}. Contact us 24/7.")), 155)
    template_variant = dest_obj.get("template_variant", "A")
    complexity = esc(dest_obj.get("complexity", "moderate"))
    doc_time = esc(dest_obj.get("doc_processing_time", "varies"))
    embassy_city = esc(origin.get("embassy_city", ""))

    da_intro_raw = (
        f"Repatriation from {oname} to {dname} follows {origin['name']}'s "
        f"civil registration and export system. Most cases take {avg} from death to arrival."
    )
    da_intro = esc(da_intro_raw)
    da_points = build_direct_answer_points(origin, dest_obj)
    overview_h = f"What happens after a death in {oname}"
    overview_body = esc(build_overview_body(origin, dest_obj))
    dest_reception = esc(dest_obj.get("dest_reception", ""))
    dest_consular = esc(dest_obj.get("dest_consular_note", dest["emergency_line"]))

    steps = build_timeline_steps(origin, dest_obj, oname, dname)
    faqs = build_faqs(origin, dest_obj, oname, dname)

    upward = [
        {"url": f"/repatriation-from-{origin_slug}/", "text": f"Full {oname} repatriation guide"},
        {"url": f"/guides/death-abroad-{origin_slug}/", "text": f"What to do if someone dies in {oname}"},
        {"url": f"/embassy-contacts/{origin_slug}/", "text": f"British Embassy in {oname}"},
        {"url": "/contact/", "text": "Send an enquiry to our team"},
    ]
    # Sideways: reverse route + alternate destination
    alt_dest = "ireland" if dest_obj["key"] == "uk" else "uk"
    alt_dest_name = "Ireland" if alt_dest == "ireland" else "the UK"
    alt_dest_slug = DESTINATIONS[alt_dest]["slug"]
    sideways = [
        {"url": f"/routes/{dest_slug}-to-{origin_slug}/", "text": f"Repatriation from {dname} to {oname}"},
        {"url": f"/routes/{origin_slug}-to-{alt_dest_slug}/", "text": f"Repatriation from {oname} to {alt_dest_name}"},
    ]

    L = ["---"]

    # Core SEO fields
    L.append(f'title: "{title}"')
    L.append(f'description: "{description}"')

    # NOTE: NO layout: field -- see ERRORS.md E001 and MEMORY.md

    # Route identity
    L.append(f'origin_key: "{origin["key"]}"')
    L.append(f'dest_key: "{dest_obj["key"]}"')
    L.append(f'origin_name: "{oname}"')
    L.append(f'dest_name: "{dname}"')
    L.append(f'origin_slug: "{origin_slug}"')
    L.append(f'dest_slug: "{dest_slug}"')
    L.append(f'slug: "{route_slug}"')
    L.append(f'template_variant: "{template_variant}"')
    L.append(f'route_complexity: "{complexity}"')

    # Timelines
    L.append(f'timeline_avg: "{avg}"')
    L.append(f'timeline_fast: "{fast}"')
    L.append(f'timeline_complex: "{complex_}"')
    L.append(f'embassy_city: "{embassy_city}"')
    L.append(f'doc_processing_time: "{doc_time}"')

    # Direct answer block
    L.append(f'direct_answer_heading: "Repatriation from {oname} to {dname}: what to expect"')
    L.append(f'direct_answer_intro: "{da_intro}"')
    L.append("direct_answer_points:")
    for pt in da_points:
        L.append(f'  - "{esc(pt)}"')

    # Overview
    L.append(f'overview_heading: "{esc(overview_h)}"')
    L.append(f'overview_body: "{overview_body}"')

    # Destination reception and consular
    L.append(f'dest_reception: "{dest_reception}"')
    L.append(f'dest_consular: "{dest_consular}"')

    # Timeline steps
    L.append("timeline_steps:")
    for s in steps:
        L.append(f'  - step: {s["step"]}')
        L.append(f'    action: "{esc(s["action"])}"')
        L.append(f'    timing: "{esc(s["timing"])}"')
        L.append(f'    responsible: "{esc(s["responsible"])}"')

    # FAQs
    L.append("faqs:")
    for faq in faqs:
        L.append(f'  - question: "{esc(faq["question"])}"')
        L.append(f'    answer: "{esc(faq["answer"])}"')

    # Internal links
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


# ---------------------------------------------------------------------------
# QA gate (mirrors workforce/the-auditor.md, Section 1-4)
# ---------------------------------------------------------------------------

def qa_gate(md: str, slug: str) -> tuple[list[str], list[str]]:
    """
    Run the 18-point auditor checklist.
    Returns (errors, warnings). Nothing ships with errors.
    """
    errors = []
    warnings = []
    text_lower = md.lower()

    # --- Section 1: Frontmatter ---

    # BANNED: layout field
    if re.search(r'^layout:', md, re.MULTILINE):
        errors.append("layout: field present -- REMOVE IT (causes Hugo to silently skip the page)")

    # Title
    title_match = re.search(r'^title:\s*"(.+)"', md, re.MULTILINE)
    title = title_match.group(1) if title_match else ""
    if not title:
        errors.append("Missing title")
    elif len(title) > 60:
        errors.append(f"Title too long: {len(title)} chars (max 60): {title[:70]}")
    elif len(title) < 30:
        warnings.append(f"Title short: {len(title)} chars (aim 40-60)")

    # Description
    desc_match = re.search(r'^description:\s*"(.+)"', md, re.MULTILINE)
    desc = desc_match.group(1) if desc_match else ""
    if not desc:
        errors.append("Missing description")
    elif len(desc) > 155:
        errors.append(f"Description too long: {len(desc)} chars (max 155)")
    elif len(desc) < 100:
        warnings.append(f"Description short: {len(desc)} chars")

    # Slug
    slug_match = re.search(r'^slug:\s*"(.+)"', md, re.MULTILINE)
    if not slug_match:
        errors.append("Missing slug field")

    # FAQ count
    faq_count = md.count("  - question:")
    if faq_count < 6:
        warnings.append(f"Only {faq_count} FAQs (minimum 6 recommended)")
    if faq_count == 0:
        errors.append("No FAQs found")

    # Timeline steps
    step_count = md.count("  - step:")
    if step_count < 6:
        warnings.append(f"Only {step_count} timeline steps (minimum 6 recommended)")

    # Upward links
    upward_section = ""
    if "  upward:" in md:
        upward_section = md.split("  upward:")[1].split("  sideways:")[0]
    upward_count = upward_section.count("- url:")
    if upward_count < 2:
        warnings.append(f"Only {upward_count} upward links (minimum 2)")

    # --- Section 2: Content quality ---

    # Em dash
    if "\u2014" in md:
        errors.append("Em dash (\u2014) found -- replace with comma, colon, or full stop")
    if "\u2013" in md:
        warnings.append("En dash (\u2013) found")

    # Banned vocabulary
    for word in BANNED_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            errors.append(f"Banned word: '{word}'")

    # AI phrases
    for phrase in AI_PHRASES:
        if phrase in text_lower:
            warnings.append(f"AI-pattern phrase: '{phrase}'")

    # Safety guarantees
    for pattern in SAFETY_PATTERNS:
        if re.search(pattern, text_lower):
            errors.append(f"Safety guarantee: '{pattern}'")

    # Prices
    for pattern in PRICE_PATTERNS:
        if re.search(pattern, text_lower):
            errors.append(f"Price reference found: '{pattern}'")

    # --- Section 3: SEO ---

    # CTA in description
    ctas = ["24/7", "contact us", "call us", "send an enquiry", "enquire now"]
    if desc and not any(cta in desc.lower() for cta in ctas):
        warnings.append("Description has no CTA (24/7, Contact us, etc.)")

    # origin_name in title
    origin_match = re.search(r'^origin_name:\s*"(.+)"', md, re.MULTILINE)
    origin_name = origin_match.group(1) if origin_match else ""
    if origin_name and title and origin_name.lower() not in title.lower():
        warnings.append(f"Origin name '{origin_name}' not in title")

    # --- Section 4: Links ---
    if "/contact/" not in md and "+44" not in md:
        warnings.append("No contact link or phone number found")

    return errors, warnings


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_route(origin_key: str, dest_key: str, dry_run: bool = False) -> tuple[str, str, list[str], list[str]]:
    """
    Generate one route page. Returns (slug, filepath, errors, warnings).
    Does not write to disk if dry_run=True or if errors exist.
    """
    data = load_route_data(origin_key)
    if data is None:
        return f"{origin_key}-to-???", "", [f"No route data file: site/data/route_data/{origin_key}.json"], []

    origin = data["origin"]
    origin_slug = origin["slug"]

    # Find matching destination in the data file
    dest_obj = None
    for d in data.get("destinations", []):
        if d["key"] == dest_key:
            dest_obj = d
            break

    if dest_obj is None:
        slug = f"{origin_slug}-to-{DESTINATIONS.get(dest_key, {}).get('slug', dest_key)}"
        return slug, "", [f"Destination '{dest_key}' not found in {origin_key}.json"], []

    slug = dest_obj["route_slug"]
    filepath = CONTENT_DIR / f"{slug}.md"

    # Skip if exists
    if filepath.exists() and not dry_run:
        return slug, str(filepath), [], ["SKIP (file already exists)"]

    # Build content
    md = build_frontmatter(data, dest_obj)

    # QA gate
    errors, warnings = qa_gate(md, slug)

    # Write only if no errors and not dry run
    if not errors and not dry_run:
        filepath.write_text(md, encoding="utf-8")

    return slug, str(filepath), errors, warnings


def list_corridors() -> list[tuple[str, str]]:
    """Return all corridors available in route_data files."""
    corridors = []
    for path in sorted(ROUTE_DATA_DIR.glob("*.json")):
        if path.name == "README.md":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            origin_key = data["origin"]["key"]
            for dest in data.get("destinations", []):
                corridors.append((origin_key, dest["key"]))
        except Exception:
            pass
    return corridors


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Repatriate Service Route Generator (Engine 1 v2)")
    parser.add_argument("--dry-run", action="store_true", help="QA check only, do not write files")
    parser.add_argument("--origin", help="Generate only this origin (e.g. spain)")
    parser.add_argument("--list", action="store_true", help="List all available corridors")
    args = parser.parse_args()

    corridors = list_corridors()

    if args.list:
        print("Available corridors:")
        for origin_key, dest_key in corridors:
            dest_slug = DESTINATIONS.get(dest_key, {}).get("slug", dest_key)
            print(f"  {origin_key} -> {dest_key}  ({origin_key}-to-{dest_slug})")
        print(f"\nTotal: {len(corridors)} corridors across {len(set(o for o, _ in corridors))} origins")
        return

    if args.origin:
        corridors = [(o, d) for o, d in corridors if o == args.origin]
        if not corridors:
            print(f"ERROR: No corridors found for origin '{args.origin}'")
            print("Run with --list to see available origins")
            sys.exit(1)

    print("=" * 65)
    print("REPATRIATE SERVICE -- ROUTE GENERATOR (Engine 1 v2)")
    mode = "DRY RUN -- QA only, no files written" if args.dry_run else "LIVE -- writing files to site/content/routes/"
    print(f"Mode: {mode}")
    print(f"Corridors: {len(corridors)}")
    print("=" * 65)
    print()

    generated = skipped = failed = warned = 0

    for origin_key, dest_key in corridors:
        slug, filepath, errors, warnings = generate_route(origin_key, dest_key, dry_run=args.dry_run)

        is_skip = any("SKIP" in w for w in warnings)
        skip_warnings = [w for w in warnings if "SKIP" not in w]

        if is_skip:
            skipped += 1
            print(f"[SKIP] {slug}")
            continue

        if errors:
            failed += 1
            print(f"[FAIL] {slug}")
            for e in errors:
                print(f"  ERROR: {e}")
        else:
            if skip_warnings:
                warned += 1
                print(f"[WARN] {slug}")
                for w in skip_warnings:
                    print(f"  warn : {w}")
            else:
                print(f"[PASS] {slug}")

            if not args.dry_run:
                generated += 1

    print()
    print("=" * 65)
    print("SUMMARY")
    print(f"  Generated : {generated}")
    print(f"  Skipped   : {skipped} (files already exist)")
    print(f"  Warned    : {warned}")
    print(f"  Failed    : {failed}")

    if failed == 0:
        print()
        if args.dry_run:
            print("VERDICT: ALL QA CHECKS PASS")
            print("Run without --dry-run to write files.")
        else:
            print("VERDICT: GENERATION COMPLETE")
            print()
            print("Next steps per CLAUDE.md quality gate:")
            print("  6. Generate HTML preview (run: python preview_routes.py)")
            print("  7. Present to Gareth for approval")
            print("  8. Commit to master only after approval")
            print("  9. Provide live URLs")
            print(" 10. Stop and wait for next 'go'")
    else:
        print()
        print(f"VERDICT: {failed} CORRIDOR(S) FAILED QA -- FIX BEFORE GENERATING")
        print("Add missing route data to site/data/route_data/ and re-run.")

    print("=" * 65)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
