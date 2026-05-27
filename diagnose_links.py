#!/usr/bin/env python3
"""
diagnose_links.py -- Engine 4 diagnostic tool

Scans all route pages and shows:
- Which pages are linked to (are they reachable?)
- Which pages have no inbound links from other route pages (orphans)
- Which sideways links point to routes that do not yet exist
- Summary of link coverage across the site

Usage:
  python diagnose_links.py
  python diagnose_links.py --orphans-only

This is a read-only diagnostic. It never modifies files.
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

ROUTES_DIR = Path("site/content/routes")


def extract_all_links(content: str) -> list[str]:
    """Extract all /routes/... URLs from page content."""
    return re.findall(r'url:\s*["\']?(/routes/[^"\'\'\n\s]+)["\']?', content)


def main():
    parser = argparse.ArgumentParser(description="Engine 4: Link graph diagnostics")
    parser.add_argument("--orphans-only", action="store_true", help="Only show orphan pages")
    args = parser.parse_args()

    routes_path = ROUTES_DIR
    files = sorted([f for f in routes_path.glob("*.md") if f.name != "_index.md"])

    if not files:
        print("No route files found.")
        sys.exit(0)

    # Map slug -> filepath for existence checks
    existing_slugs = {f.stem for f in files}
    # e.g. 'spain-to-united-kingdom'
    existing_urls = {f"/routes/{slug}/" for slug in existing_slugs}

    # Build inbound link map: which pages link TO each route URL
    inbound = defaultdict(list)
    # Build outbound link map: which URLs does each page link to
    outbound = defaultdict(list)
    # Track broken sideways links (link to non-existent route)
    broken = []

    for filepath in files:
        content = filepath.read_text(encoding="utf-8")
        slug = filepath.stem
        page_url = f"/routes/{slug}/"
        links = extract_all_links(content)
        outbound[slug] = links
        for link in links:
            inbound[link].append(slug)
            if link not in existing_urls and link != page_url:
                broken.append({"from": slug, "to": link})

    print("=" * 65)
    print("REPATRIATE SERVICE -- ENGINE 4: LINK DIAGNOSTICS")
    print(f"Route pages: {len(files)}")
    print("=" * 65)
    print()

    # Orphan pages (zero inbound links from other route pages)
    orphans = []
    for filepath in files:
        slug = filepath.stem
        page_url = f"/routes/{slug}/"
        if not inbound.get(page_url):
            orphans.append(slug)

    if orphans:
        print(f"ORPHAN PAGES ({len(orphans)}) -- no inbound links from other route pages:")
        for slug in orphans:
            print(f"  {slug}")
        print()

    if not args.orphans_only:
        # Broken sideways links
        if broken:
            print(f"BROKEN SIDEWAYS LINKS ({len(broken)}) -- link to non-existent route:")
            for b in broken:
                print(f"  {b['from']} -> {b['to']}")
            print()

        # Link coverage summary
        print("LINK COVERAGE SUMMARY:")
        print(f"  Total existing route pages : {len(files)}")
        print(f"  Pages with inbound links   : {len([s for s in existing_slugs if inbound.get(f'/routes/{s}/')])}/{len(files)}")
        print(f"  Orphan pages               : {len(orphans)}")
        print(f"  Broken sideways links      : {len(broken)}")
        print()

        # Most-linked pages
        sorted_inbound = sorted(
            [(url, len(sources)) for url, sources in inbound.items() if url in existing_urls],
            key=lambda x: x[1], reverse=True
        )[:10]
        if sorted_inbound:
            print("TOP 10 MOST-LINKED ROUTE PAGES:")
            for url, count in sorted_inbound:
                print(f"  {count:3} inbound links: {url}")

    print()
    print("=" * 65)
    if orphans:
        print(f"ACTION REQUIRED: Run 'python rebuild_link_graph.py --fix' to repair link graphs")
        sys.exit(1)
    else:
        print("All route pages have inbound links.")
        sys.exit(0)


if __name__ == "__main__":
    main()
