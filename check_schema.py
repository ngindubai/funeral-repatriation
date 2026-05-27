#!/usr/bin/env python3
"""
check_schema.py -- Schema presence checker (Engine 5)
Verifies that route pages have the required schema fields in frontmatter
for Hugo to generate FAQPage, Service, and BreadcrumbList schema.

Usage: python check_schema.py [--path site/content/routes]
"""

import re
import sys
import argparse
from pathlib import Path

ROUTES_DIR = Path("site/content/routes")


def get_fm_value(content: str, key: str) -> str:
    match = re.search(rf'^{re.escape(key)}:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def count_list_items(content: str, key: str) -> int:
    lines = content.split("\n")
    in_section = False
    count = 0
    for line in lines:
        if line.startswith(f"{key}:"):
            in_section = True
            continue
        if in_section:
            stripped = line.strip()
            if stripped.startswith("- "):
                count += 1
            elif line and not line[0].isspace() and not stripped.startswith("-"):
                break
    return count


def check_schema(filepath: Path) -> list[tuple[str, str]]:
    issues = []
    content = filepath.read_text(encoding="utf-8")

    if not content.startswith("---"):
        issues.append(("ERROR", "No YAML frontmatter found"))
        return issues

    parts = content.split("---", 2)
    if len(parts) < 3:
        issues.append(("ERROR", "Malformed frontmatter"))
        return issues

    fm = parts[1]

    # FAQPage schema -- requires faqs: list with question and answer
    faq_count = count_list_items(fm, "faqs")
    if faq_count == 0:
        issues.append(("ERROR", "No faqs: list -- FAQPage schema will not be generated"))
    else:
        # Check that faqs have question and answer sub-fields
        if "question:" not in fm:
            issues.append(("ERROR", "faqs: items missing 'question:' field -- FAQPage schema will be malformed"))
        if "answer:" not in fm:
            issues.append(("ERROR", "faqs: items missing 'answer:' field -- FAQPage schema will be malformed"))

    # Service schema -- requires origin_name, dest_name, description
    for field in ["origin_name", "dest_name", "description"]:
        if not get_fm_value(fm, field):
            issues.append(("ERROR", f"Missing '{field}' -- Service schema will be incomplete"))

    # BreadcrumbList schema -- requires slug (for permalink)
    if not get_fm_value(fm, "slug"):
        issues.append(("WARNING", "Missing 'slug' -- BreadcrumbList may use wrong URL"))

    # Organization schema -- no per-page fields needed (uses site params)
    # Just confirm the template will have access to site.Params.whatsappNumber
    # This is a site-level check, not per-page -- skip here

    return issues


def main():
    parser = argparse.ArgumentParser(description="Schema checker for route pages")
    parser.add_argument("--path", default=str(ROUTES_DIR))
    args = parser.parse_args()

    routes_path = Path(args.path)
    if not routes_path.exists():
        print(f"ERROR: Path not found: {routes_path}")
        sys.exit(1)

    files = sorted([f for f in routes_path.glob("*.md") if f.name != "_index.md"])

    if not files:
        print("No route files found.")
        sys.exit(0)

    print("=" * 65)
    print("REPATRIATE SERVICE -- SCHEMA CHECK")
    print(f"Checking {len(files)} route pages")
    print("=" * 65)
    print()

    total_errors = 0
    total_warnings = 0
    failed_files = 0

    for filepath in files:
        issues = check_schema(filepath)
        errors = [i for i in issues if i[0] == "ERROR"]
        warnings = [i for i in issues if i[0] == "WARNING"]

        if errors:
            verdict = "FAIL"
            failed_files += 1
            total_errors += len(errors)
        elif warnings:
            verdict = "WARN"
            total_warnings += len(warnings)
        else:
            verdict = "PASS"

        if issues:
            print(f"[{verdict}] {filepath.name}")
            for severity, msg in issues:
                tag = "  ERROR" if severity == "ERROR" else "  warn "
                print(f"{tag}: {msg}")
        else:
            print(f"[PASS] {filepath.name}")

    print()
    print("=" * 65)
    print(f"Files checked : {len(files)}")
    print(f"Errors        : {total_errors}")
    print(f"Warnings      : {total_warnings}")
    print(f"Failed files  : {failed_files}")

    if total_errors == 0:
        print()
        print("VERDICT: ALL SCHEMA CHECKS PASS")
        sys.exit(0)
    else:
        print()
        print("VERDICT: SCHEMA ERRORS FOUND -- FIX BEFORE COMMITTING")
        sys.exit(1)


if __name__ == "__main__":
    main()
