#!/usr/bin/env python3
"""
rebuild_link_graph.py -- Repatriate Service Engine 4

Rebuilds the internal link graph across all route pages.
Every route page must link:
  Upward (2 minimum):
    - /repatriation-from-{origin}/ (origin country hub)
    - /guides/death-abroad-{origin}/ (origin guide)
    - /embassy-contacts/{origin}/ (origin embassy page)
    - /contact/ (enquiry CTA)
  Sideways (2 minimum):
    - /routes/{dest}-to-{origin}/ (reverse route)
    - /routes/{origin}-to-{alt-dest}/ (alternate destination)

Usage:
  python rebuild_link_graph.py            # audit + report, no changes
  python rebuild_link_graph.py --fix      # audit + patch missing links
  python rebuild_link_graph.py --report   # output full link inventory as CSV

Exit 0 = all pages pass. Exit 1 = missing links found.
"""

import re
import sys
import csv
import argparse
from pathlib import Path
from collections import defaultdict

ROUTES_DIR = Path("site/content/routes")

# Known destinations slug map
DESTINATIONS = {
    "united-kingdom": "the UK",
    "ireland": "Ireland",
}
ALT_DEST = {
    "united-kingdom": "ireland",
    "ireland": "united-kingdom",
}
ALT_DEST_NAME = {
    "united-kingdom": "Ireland",
    "ireland": "the UK",
}


def parse_frontmatter(content: str) -> dict:
    """Extract key frontmatter values without a full YAML parser."""
    fm = {}
    if not content.startswith("---"):
        return fm
    parts = content.split("---", 2)
    if len(parts) < 3:
        return fm
    block = parts[1]

    for key in ["slug", "origin_name", "dest_name", "origin_slug", "dest_slug"]:
        m = re.search(rf'^{key}:\s*["\']?([^"\'\'\n]+?)["\']?\s*$', block, re.MULTILINE)
        if m:
            fm[key] = m.group(1).strip()

    # Extract upward links
    upward_urls = re.findall(r'upward:.*?sideways:', block, re.DOTALL)
    fm["upward_urls"] = re.findall(r'- url:\s*["\']?(/[^"\'\'\n]+)["\']?', upward_urls[0]) if upward_urls else []

    # Extract sideways links
    sideways_match = re.search(r'sideways:(.*?)(?=\Z|^---)', block, re.DOTALL | re.MULTILINE)
    fm["sideways_urls"] = re.findall(r'- url:\s*["\']?(/[^"\'\'\n]+)["\']?', sideways_match.group(1)) if sideways_match else []

    return fm


def expected_links(fm: dict) -> dict:
    """Return the expected upward and sideways links for this page."""
    origin_slug = fm.get("origin_slug", "")
    dest_slug = fm.get("dest_slug", "")
    alt_dest_slug = ALT_DEST.get(dest_slug, "ireland" if dest_slug == "united-kingdom" else "united-kingdom")
    alt_dest_name = ALT_DEST_NAME.get(dest_slug, "Ireland")
    origin_name = fm.get("origin_name", origin_slug.replace("-", " ").title())
    dest_name = fm.get("dest_name", dest_slug.replace("-", " ").title())

    return {
        "upward": [
            {"url": f"/repatriation-from-{origin_slug}/",
             "text": f"Full {origin_name} repatriation guide"},
            {"url": f"/guides/death-abroad-{origin_slug}/",
             "text": f"What to do if someone dies in {origin_name}"},
            {"url": f"/embassy-contacts/{origin_slug}/",
             "text": f"British Embassy in {origin_name}"},
            {"url": "/contact/",
             "text": "Send an enquiry to our team"},
        ],
        "sideways": [
            {"url": f"/routes/{dest_slug}-to-{origin_slug}/",
             "text": f"Repatriation from {dest_name} to {origin_name}"},
            {"url": f"/routes/{origin_slug}-to-{alt_dest_slug}/",
             "text": f"Repatriation from {origin_name} to {alt_dest_name}"},
        ],
    }


def build_link_block(expected: dict) -> str:
    """Render a links: frontmatter block from expected links."""
    lines = ["links:"]
    lines.append("  upward:")
    for lk in expected["upward"]:
        lines.append(f'    - url: "{lk["url"]}"')
        lines.append(f'      text: "{lk["text"]}"')
    lines.append("  sideways:")
    for lk in expected["sideways"]:
        lines.append(f'    - url: "{lk["url"]}"')
        lines.append(f'      text: "{lk["text"]}"')
    return "\n".join(lines)


def patch_links(content: str, expected: dict) -> str:
    """Replace the links: block in the frontmatter with the correct one."""
    new_block = build_link_block(expected)
    # Replace existing links: block (from 'links:' to end of frontmatter '---')
    # The frontmatter ends at the second '---'
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content
    fm_block = parts[1]

    # Find and replace the links section
    links_match = re.search(r'\nlinks:.*$', fm_block, re.DOTALL)
    if links_match:
        fm_block = fm_block[:links_match.start()] + "\n" + new_block + "\n"
    else:
        # No links section yet, append before closing
        fm_block = fm_block.rstrip() + "\n" + new_block + "\n"

    return "---" + fm_block + "---" + parts[2]


def audit_page(filepath: Path) -> dict:
    """
    Audit a single route page's link graph.
    Returns a result dict with pass/fail status and details.
    """
    content = filepath.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    slug = fm.get("slug", filepath.stem)
    expected = expected_links(fm)

    missing_upward = []
    for lk in expected["upward"]:
        if lk["url"] not in fm.get("upward_urls", []):
            missing_upward.append(lk["url"])

    missing_sideways = []
    for lk in expected["sideways"]:
        if lk["url"] not in fm.get("sideways_urls", []):
            missing_sideways.append(lk["url"])

    upward_count = len(fm.get("upward_urls", []))
    sideways_count = len(fm.get("sideways_urls", []))

    passed = len(missing_upward) == 0 and len(missing_sideways) == 0

    return {
        "slug": slug,
        "filepath": filepath,
        "content": content,
        "fm": fm,
        "expected": expected,
        "upward_count": upward_count,
        "sideways_count": sideways_count,
        "missing_upward": missing_upward,
        "missing_sideways": missing_sideways,
        "passed": passed,
    }


def main():
    parser = argparse.ArgumentParser(description="Engine 4: Link graph audit and repair")
    parser.add_argument("--fix", action="store_true", help="Patch missing links in-place")
    parser.add_argument("--report", action="store_true", help="Output full link inventory as CSV to link_graph_report.csv")
    parser.add_argument("--path", default=str(ROUTES_DIR), help="Path to routes directory")
    args = parser.parse_args()

    routes_path = Path(args.path)
    if not routes_path.exists():
        print(f"ERROR: Routes directory not found: {routes_path}")
        sys.exit(1)

    files = sorted([f for f in routes_path.glob("*.md") if f.name != "_index.md"])
    if not files:
        print("No route files found.")
        sys.exit(0)

    print("=" * 65)
    print("REPATRIATE SERVICE -- ENGINE 4: LINK GRAPH")
    print(f"Auditing {len(files)} route pages")
    if args.fix:
        print("Mode: FIX (patching missing links)")
    else:
        print("Mode: AUDIT ONLY (no changes)")
    print("=" * 65)
    print()

    results = [audit_page(f) for f in files]
    passed = [r for r in results if r["passed"]]
    failed = [r for r in results if not r["passed"]]
    fixed = 0

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['slug']}")
        print(f"        upward: {r['upward_count']} links | sideways: {r['sideways_count']} links")
        for url in r["missing_upward"]:
            print(f"  MISSING upward : {url}")
        for url in r["missing_sideways"]:
            print(f"  MISSING sideways: {url}")

        if args.fix and not r["passed"]:
            patched = patch_links(r["content"], r["expected"])
            r["filepath"].write_text(patched, encoding="utf-8")
            fixed += 1
            print(f"  FIXED: link block rebuilt")

    # CSV report
    if args.report:
        report_path = Path("link_graph_report.csv")
        with open(report_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["slug", "upward_count", "sideways_count",
                             "missing_upward", "missing_sideways", "status"])
            for r in results:
                writer.writerow([
                    r["slug"],
                    r["upward_count"],
                    r["sideways_count"],
                    " | ".join(r["missing_upward"]),
                    " | ".join(r["missing_sideways"]),
                    "PASS" if r["passed"] else "FAIL",
                ])
        print(f"\nLink graph report written to: {report_path}")

    # Summary
    print()
    print("=" * 65)
    print(f"Pages audited : {len(results)}")
    print(f"PASS          : {len(passed)}")
    print(f"FAIL          : {len(failed)}")
    if args.fix:
        print(f"Fixed         : {fixed}")

    if not failed:
        print()
        print("VERDICT: ALL PAGES HAVE COMPLETE LINK GRAPHS")
        sys.exit(0)
    else:
        print()
        if args.fix:
            print(f"VERDICT: {len(failed)} pages had incomplete links -- all patched")
            sys.exit(0)
        else:
            print(f"VERDICT: {len(failed)} pages have incomplete links -- run with --fix to patch")
            sys.exit(1)


if __name__ == "__main__":
    main()
