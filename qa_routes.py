"""
QA Audit for Route Pages — Repatriate Service

Runs 18 checks across all /routes/*.md files.
Prints PASS / WARN / FAIL per file and a summary.

Usage: python qa_routes.py
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
ROUTES_DIR = os.path.join(REPO_ROOT, "site", "content", "routes")

BANNED_WORDS = [
    "delve", "tapestry", "robust", "seamless", "elevate", "foster",
    "revolutionise", "game-changer", "empower", "comprehensive",
    "meticulous", "bustling", "vibrant", "synergy", "leverage",
]
SAFETY_PATTERNS = ["guarantee", "100% safe", "risk-free", "guaranteed protection"]
PRICE_PATTERNS = ["\u00a3", "GBP", "USD", "\u20ac"]
REQUIRED_FIELDS = ["title", "description", "layout", "origin_key", "dest_key",
                   "origin_name", "dest_name", "timeline_avg", "faqs", "timeline_steps"]


def check_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    errors, warnings = [], []
    lines = content.split("\n")

    # Required fields
    for field in REQUIRED_FIELDS:
        if f"{field}:" not in content:
            errors.append(f"Missing required field: {field}")

    # Title length
    title_val = next((l.replace('title: "', "").rstrip('"') for l in lines if l.startswith("title:")), "")
    if not title_val:
        errors.append("Missing title")
    elif len(title_val) > 60:
        errors.append(f"Title too long: {len(title_val)} chars (max 60)")
    elif len(title_val) < 20:
        errors.append(f"Title too short: {len(title_val)} chars (min 20)")

    # Description length
    desc_val = next((l.replace('description: "', "").rstrip('"') for l in lines if l.startswith("description:")), "")
    if not desc_val:
        errors.append("Missing description")
    elif len(desc_val) > 155:
        errors.append(f"Description too long: {len(desc_val)} chars (max 155)")

    # FAQs
    faq_count = content.count("  - question:")
    if faq_count < 4:
        errors.append(f"Only {faq_count} FAQs (minimum 4 required for FAQPage schema)")
    elif faq_count < 5:
        warnings.append(f"Only {faq_count} FAQs (5+ recommended)")

    # Timeline steps
    step_count = content.count("  - step:")
    if step_count < 5:
        errors.append(f"Only {step_count} timeline steps (minimum 5)")
    elif step_count < 7:
        warnings.append(f"Only {step_count} steps (7 recommended)")

    # Internal links
    link_count = content.count("    - url:")
    if link_count < 3:
        errors.append(f"Only {link_count} internal links (minimum 3)")

    # Em dash
    if "\u2014" in content:
        errors.append("Em dash (\u2014) present. Use comma or colon instead.")

    # Banned words
    for word in BANNED_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", content, re.IGNORECASE):
            errors.append(f"Banned word: '{word}'")

    # YMYL safety guarantees
    for pattern in SAFETY_PATTERNS:
        if pattern.lower() in content.lower():
            errors.append(f"YMYL violation: safety guarantee '{pattern}'")

    # Price references
    for pattern in PRICE_PATTERNS:
        if pattern in content:
            errors.append(f"Price reference: '{pattern}' (no costs on this site)")

    # Phone number check (should only be FCDO/embassy numbers, not business phone)
    phone_matches = re.findall(r"\+44\s?\d{4}\s?\d{6}", content)
    for m in phone_matches:
        if "7703 577246" not in m and "7008 5000" not in m and "1908 516666" not in m:
            warnings.append(f"Unexpected phone number: {m}")

    # WhatsApp or /contact/ present
    if "+447" not in content and "/contact/" not in content:
        errors.append("No WhatsApp number or /contact/ link found")

    # Schema check
    if "FAQPage" not in content and "application/ld+json" not in content:
        warnings.append("No schema block detected in content (schema is in layout template)")

    # Thin content check (frontmatter field count)
    if content.count("  - ") < 15:
        warnings.append("Low frontmatter data count. Page may render thin.")

    return errors, warnings


if __name__ == "__main__":
    if not os.path.isdir(ROUTES_DIR):
        print(f"Routes directory not found: {ROUTES_DIR}")
        raise SystemExit(1)

    files = sorted(f for f in os.listdir(ROUTES_DIR) if f.endswith(".md") and f != "_index.md")
    if not files:
        print("No route pages found.")
        raise SystemExit(0)

    total = passed = warned = failed = 0
    print(f"QA audit: {len(files)} route pages\n" + "=" * 50)

    for fn in files:
        total += 1
        path = os.path.join(ROUTES_DIR, fn)
        errs, warns = check_file(path)
        if errs:
            failed += 1
            print(f"[FAIL] {fn}")
            for e in errs:
                print(f"       ERROR: {e}")
            for w in warns:
                print(f"       WARN:  {w}")
        elif warns:
            warned += 1
            print(f"[WARN] {fn}")
            for w in warns:
                print(f"       {w}")
        else:
            passed += 1
            print(f"[PASS] {fn}")

    print("\n" + "=" * 50)
    print(f"TOTAL: {total} | PASS: {passed} | WARN: {warned} | FAIL: {failed}")
    if failed == 0:
        print("VERDICT: ALL PAGES PASS QA. Safe to commit.")
    else:
        print(f"VERDICT: {failed} PAGE(S) FAILED. Fix errors before committing.")
        raise SystemExit(1)
