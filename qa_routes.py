#!/usr/bin/env python3
"""
qa_routes.py -- Repatriate Service QA Gate (Engine 5)
Runs the full 18-point audit on all route pages before any commit.
Usage: python qa_routes.py [--path site/content/routes]

Exit code 0 = all pages pass. Exit code 1 = one or more FAIL.
"""

import os
import re
import sys
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROUTES_DIR = Path("site/content/routes")

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
    "in today's digital age",
]

SAFETY_PATTERNS = [
    r"guarantee[ds]?\s+(safety|protection|safe)",
    r"100%\s+safe",
    r"completely\s+safe",
    r"risk[- ]free",
    r"guaranteed\s+protection",
]

PRICE_PATTERNS = [
    r"\u00a3\s*\d",
    r"\$\s*\d",
    r"EUR\s*\d",
    r"\bcost[s]?\s+\d",
    r"\bprice[s]?\s+\d",
    r"\bfee[s]?\s+\d",
]

REQUIRED_FRONTMATTER = [
    "title",
    "description",
    "origin_name",
    "dest_name",
    "slug",
    "timeline_avg",
    "faqs",
    "timeline_steps",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_frontmatter(content: str) -> tuple[str, str]:
    """Split YAML frontmatter from body. Returns (frontmatter, body)."""
    if not content.startswith("---"):
        return "", content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return "", content
    return parts[1], parts[2]


def get_fm_value(frontmatter: str, key: str) -> str:
    """Extract a simple scalar value from YAML frontmatter."""
    match = re.search(rf'^{re.escape(key)}:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def count_list_items(frontmatter: str, key: str) -> int:
    """Count list items under a YAML key (lines starting with '  -')."""
    lines = frontmatter.split("\n")
    in_section = False
    count = 0
    for line in lines:
        if line.startswith(f"{key}:"):
            in_section = True
            continue
        if in_section:
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("-\t"):
                count += 1
            elif line and not line[0].isspace() and not stripped.startswith("-"):
                break
    return count


# ---------------------------------------------------------------------------
# Audit function
# ---------------------------------------------------------------------------

def audit_page(filepath: Path) -> list[tuple[str, str]]:
    """
    Audit a single route markdown file.
    Returns list of (severity, message) tuples.
    Severity: ERROR | WARNING
    """
    issues = []
    content = filepath.read_text(encoding="utf-8")
    frontmatter, body = extract_frontmatter(content)
    text_lower = content.lower()
    slug = filepath.stem

    # ------------------------------------------------------------------
    # SECTION 1 -- Frontmatter completeness
    # ------------------------------------------------------------------

    # Banned: layout field
    if re.search(r'^layout:', frontmatter, re.MULTILINE):
        issues.append(("ERROR", "layout: field present -- remove it (causes Hugo to silently skip the page)"))

    # Required fields
    for field in REQUIRED_FRONTMATTER:
        if not get_fm_value(frontmatter, field) and f"{field}:" not in frontmatter:
            issues.append(("ERROR", f"Missing required frontmatter field: {field}"))

    # Title length
    title = get_fm_value(frontmatter, "title")
    if title:
        if len(title) > 60:
            issues.append(("ERROR", f"Title too long: {len(title)} chars (max 60). Title: {title[:70]}"))
        elif len(title) < 30:
            issues.append(("WARNING", f"Title very short: {len(title)} chars (aim 40-60). Title: {title}"))

    # Description length
    description = get_fm_value(frontmatter, "description")
    if description:
        if len(description) > 155:
            issues.append(("ERROR", f"Description too long: {len(description)} chars (max 155)"))
        elif len(description) < 100:
            issues.append(("WARNING", f"Description short: {len(description)} chars (aim 120-155)"))

    # Slug matches filename
    slug_fm = get_fm_value(frontmatter, "slug")
    if slug_fm and slug_fm != slug:
        issues.append(("ERROR", f"Slug mismatch: frontmatter slug '{slug_fm}' != filename '{slug}'"))

    # FAQ count
    faq_count = count_list_items(frontmatter, "faqs")
    if faq_count == 0:
        issues.append(("ERROR", "No FAQs found (minimum 6 required)"))
    elif faq_count < 6:
        issues.append(("WARNING", f"Only {faq_count} FAQs (minimum 6 recommended)"))

    # Timeline steps count
    step_count = count_list_items(frontmatter, "timeline_steps")
    if step_count == 0:
        issues.append(("ERROR", "No timeline_steps found (minimum 6 required)"))
    elif step_count < 6:
        issues.append(("WARNING", f"Only {step_count} timeline steps (minimum 6 recommended)"))

    # Upward links
    upward_count = 0
    in_upward = False
    for line in frontmatter.split("\n"):
        if "upward:" in line:
            in_upward = True
            continue
        if in_upward:
            if line.strip().startswith("- url:") or line.strip().startswith("- "):
                upward_count += 1
            elif "sideways:" in line:
                break
    if upward_count < 2:
        issues.append(("WARNING", f"Only {upward_count} upward links (minimum 2 recommended)"))

    # ------------------------------------------------------------------
    # SECTION 2 -- Content quality
    # ------------------------------------------------------------------

    # Em dash check
    if "\u2014" in content:
        issues.append(("ERROR", "Em dash (\u2014) found -- replace with comma, colon, or full stop"))
    if "\u2013" in content:
        issues.append(("WARNING", "En dash (\u2013) found"))

    # Banned vocabulary
    for word in BANNED_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            issues.append(("ERROR", f"Banned word: '{word}'"))

    # AI-pattern phrases
    for phrase in AI_PHRASES:
        if phrase.lower() in text_lower:
            issues.append(("WARNING", f"AI-pattern phrase: '{phrase}'"))

    # Safety guarantees
    for pattern in SAFETY_PATTERNS:
        if re.search(pattern, text_lower):
            issues.append(("ERROR", f"Safety guarantee pattern: '{pattern}'"))

    # Price check
    for pattern in PRICE_PATTERNS:
        if re.search(pattern, text_lower):
            issues.append(("ERROR", f"Price reference found (no prices on route pages): pattern '{pattern}'"))

    # Thin content (body word count)
    body_words = len(body.split())
    if body_words < 100:
        # Body is mostly template-driven so threshold is low for frontmatter-only pages
        issues.append(("WARNING", f"Body content very thin: {body_words} words (check template renders correctly)"))

    # ------------------------------------------------------------------
    # SECTION 3 -- SEO
    # ------------------------------------------------------------------

    # Description CTA check
    cta_endings = ["24/7", "call us", "contact us", "send an enquiry", "enquire now", "get in touch"]
    if description and not any(cta.lower() in description.lower() for cta in cta_endings):
        issues.append(("WARNING", "Description does not end with a CTA (24/7, Contact us, Call us, etc.)"))

    # Origin name in title
    origin_name = get_fm_value(frontmatter, "origin_name")
    if origin_name and title and origin_name.lower() not in title.lower():
        issues.append(("WARNING", f"Origin name '{origin_name}' not found in title"))

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="QA audit for funeral-repatriation route pages")
    parser.add_argument("--path", default=str(ROUTES_DIR), help="Path to routes directory")
    parser.add_argument("--fail-on-warning", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    routes_path = Path(args.path)
    if not routes_path.exists():
        print(f"ERROR: Routes directory not found: {routes_path}")
        sys.exit(1)

    files = sorted([f for f in routes_path.glob("*.md") if f.name != "_index.md"])

    if not files:
        print(f"No route files found in {routes_path}")
        sys.exit(0)

    total = len(files)
    passed = 0
    warned = 0
    failed = 0

    print("=" * 65)
    print("REPATRIATE SERVICE -- ROUTE QA AUDIT")
    print(f"Scanning {total} route pages in {routes_path}")
    print("=" * 65)
    print()

    for filepath in files:
        issues = audit_page(filepath)
        errors = [i for i in issues if i[0] == "ERROR"]
        warnings = [i for i in issues if i[0] == "WARNING"]

        if errors:
            verdict = "FAIL"
            failed += 1
        elif warnings:
            verdict = "WARN"
            warned += 1
            if args.fail_on_warning:
                failed += 1
            else:
                passed += 1
        else:
            verdict = "PASS"
            passed += 1

        print(f"[{verdict}] {filepath.name}")
        for severity, msg in issues:
            prefix = "  ERROR" if severity == "ERROR" else "  warn "
            print(f"{prefix}: {msg}")

    print()
    print("=" * 65)
    print(f"BATCH QA SUMMARY")
    print(f"Pages audited : {total}")
    print(f"PASS          : {passed}")
    print(f"WARN          : {warned}")
    print(f"FAIL          : {failed}")

    if failed == 0:
        print()
        print("VERDICT: BATCH READY FOR COMMIT")
    else:
        print()
        print(f"VERDICT: {failed} PAGE(S) FAILED -- FIX ERRORS BEFORE COMMITTING")

    print("=" * 65)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
