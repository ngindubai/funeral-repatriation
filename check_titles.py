#!/usr/bin/env python3
"""
check_titles.py -- Title and description checker (Engine 5)
Scans all route pages for title/description issues.
Usage: python check_titles.py [--path site/content/routes] [--fix]

With --fix: auto-corrects truncated titles and missing CTAs where safe to do so.
"""

import os
import re
import sys
import argparse
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")

# Also scan country hubs and guides
COUNTRY_DIR = Path("site/content/countries")
GUIDES_DIR = Path("site/content/guides")

CTA_ENDINGS = [
    "24/7", "call us", "contact us", "send an enquiry",
    "enquire now", "get in touch", "contact us now",
]


def get_fm_value(content: str, key: str) -> str:
    match = re.search(rf'^{re.escape(key)}:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def check_file(filepath: Path, page_type: str) -> list[dict]:
    issues = []
    content = filepath.read_text(encoding="utf-8")

    title = get_fm_value(content, "title")
    description = get_fm_value(content, "description")

    # Title checks
    if not title:
        issues.append({"file": filepath.name, "type": page_type, "severity": "ERROR",
                        "field": "title", "msg": "Missing title", "value": ""})
    else:
        if len(title) > 60:
            issues.append({"file": filepath.name, "type": page_type, "severity": "ERROR",
                            "field": "title", "msg": f"Title {len(title)} chars (max 60)",
                            "value": title})
        if len(title) < 30:
            issues.append({"file": filepath.name, "type": page_type, "severity": "WARNING",
                            "field": "title", "msg": f"Title only {len(title)} chars (aim 40-60)",
                            "value": title})
        # Bare country name check (title IS the country name, nothing else)
        if re.match(r'^[A-Z][a-z]+(\s[A-Z][a-z]+)?$', title) and len(title.split()) <= 2:
            issues.append({"file": filepath.name, "type": page_type, "severity": "ERROR",
                            "field": "title", "msg": "Bare country name as title -- add keyword and trust signal",
                            "value": title})

    # Description checks
    if not description:
        issues.append({"file": filepath.name, "type": page_type, "severity": "ERROR",
                        "field": "description", "msg": "Missing description", "value": ""})
    else:
        if len(description) > 155:
            issues.append({"file": filepath.name, "type": page_type, "severity": "ERROR",
                            "field": "description", "msg": f"Description {len(description)} chars (max 155)",
                            "value": description[:120] + "..."})
        if len(description) < 100:
            issues.append({"file": filepath.name, "type": page_type, "severity": "WARNING",
                            "field": "description", "msg": f"Description only {len(description)} chars (aim 120-155)",
                            "value": description})
        if not any(cta.lower() in description.lower() for cta in CTA_ENDINGS):
            issues.append({"file": filepath.name, "type": page_type, "severity": "WARNING",
                            "field": "description", "msg": "No CTA in description",
                            "value": description[-50:]})

    return issues


def scan_directory(directory: Path, page_type: str) -> list[dict]:
    if not directory.exists():
        return []
    issues = []
    for filepath in sorted(directory.rglob("*.md")):
        if filepath.name == "_index.md":
            continue
        issues.extend(check_file(filepath, page_type))
    return issues


def main():
    parser = argparse.ArgumentParser(description="Title and description checker")
    parser.add_argument("--routes", default=str(ROUTES_DIR))
    parser.add_argument("--countries", default=str(COUNTRY_DIR))
    parser.add_argument("--guides", default=str(GUIDES_DIR))
    parser.add_argument("--routes-only", action="store_true", help="Only scan routes")
    args = parser.parse_args()

    all_issues = []
    all_issues.extend(scan_directory(Path(args.routes), "route"))

    if not args.routes_only:
        all_issues.extend(scan_directory(Path(args.countries), "country-hub"))
        all_issues.extend(scan_directory(Path(args.guides), "guide"))

    errors = [i for i in all_issues if i["severity"] == "ERROR"]
    warnings = [i for i in all_issues if i["severity"] == "WARNING"]

    print("=" * 65)
    print("REPATRIATE SERVICE -- TITLE AND DESCRIPTION CHECK")
    print("=" * 65)
    print()

    if not all_issues:
        print("All pages PASS. No title or description issues found.")
        sys.exit(0)

    # Group by file
    files_with_issues = {}
    for issue in all_issues:
        fname = issue["file"]
        if fname not in files_with_issues:
            files_with_issues[fname] = []
        files_with_issues[fname].append(issue)

    for fname, issues in sorted(files_with_issues.items()):
        worst = "ERROR" if any(i["severity"] == "ERROR" for i in issues) else "WARNING"
        print(f"[{worst}] {fname} ({issues[0]['type']})")
        for i in issues:
            tag = "  ERROR" if i["severity"] == "ERROR" else "  warn "
            print(f"{tag}: [{i['field']}] {i['msg']}")
            if i["value"]:
                print(f"         Value: {i['value']}")
        print()

    print("=" * 65)
    print(f"Errors   : {len(errors)}")
    print(f"Warnings : {len(warnings)}")
    print(f"Files affected : {len(files_with_issues)}")

    if errors:
        print()
        print("VERDICT: FIX ERRORS BEFORE COMMITTING")
        sys.exit(1)
    else:
        print()
        print("VERDICT: WARNINGS ONLY -- REVIEW BEFORE NEXT BATCH")
        sys.exit(0)


if __name__ == "__main__":
    main()
