#!/usr/bin/env python3
"""
scripts/audit_upward_links.py
Audit upward links in all route frontmatter against the actual Hugo content tree.

For each route page in site/content/routes/, reads links.upward from frontmatter
and checks whether each target URL corresponds to a page that exists on disk.

URLs checked:
  /repatriation-from-{slug}/   -> site/content/countries/{slug}/_index.md
  /guides/death-abroad-{slug}/ -> site/content/guides/death-abroad-{slug}.md
  /contact/                    -> site/content/contact.md or site/content/contact/_index.md
  Any other /path/             -> site/content/{path}/_index.md or site/content/{path}.md

Usage:
    python scripts/audit_upward_links.py
    python scripts/audit_upward_links.py --json       # machine-readable output
    python scripts/audit_upward_links.py --fix-map    # print the slug correction map

Run from repo root. Requires the site/content/ tree to be present locally.
"""

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Paths (relative to repo root)
# ---------------------------------------------------------------------------
ROUTES_DIR = os.path.join('site', 'content', 'routes')
COUNTRY_DIR = os.path.join('site', 'content', 'countries')
GUIDES_DIR = os.path.join('site', 'content', 'guides')
CONTENT_DIR = os.path.join('site', 'content')

# ---------------------------------------------------------------------------
# Known slug corrections (route frontmatter slug -> actual directory/file slug)
# ---------------------------------------------------------------------------
# These are the mismatches between what route generators wrote into
# origin_slug / links.upward and what Hugo actually built from the content tree.
#
# The country hub URL pattern is /repatriation-from-{country-dir-name}/
# where country-dir-name is the directory name under site/content/countries/.
# The generator used the 197-canonical slug from data/countries-197.json, but
# the country hub pages were built earlier using a different slug set.
#
# Key: wrong slug embedded in route upward links
# Value: correct slug that exists in site/content/countries/ and site/content/guides/
SLUG_CORRECTIONS = {
    'democratic-republic-of-the-congo': 'democratic-republic-of-congo',
    'united-states': 'usa',
    'gambia': 'the-gambia',
    'congo': 'republic-of-congo',
    'cabo-verde': 'cape-verde',
    'vatican-city': 'holy-see',
    # 'palestine' has no matching hub at all -- no correction available
    # 'united-arab-emirates' routes use 'uae' correctly already
}

# Slugs where no hub exists and no correction is available.
# These upward links should be omitted entirely until the hub is built.
NO_HUB_SLUGS = {'palestine'}

# ---------------------------------------------------------------------------
# Frontmatter parser
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---(?:\n|$)', re.DOTALL)


def extract_upward_links(fm_text):
    """
    Extract links.upward entries from raw YAML frontmatter text.
    Returns list of dicts with 'url' and 'text' keys.
    Uses simple regex rather than a full YAML parser to stay dependency-free.
    """
    links = []
    # Find the upward: block
    upward_match = re.search(
        r'upward:\s*\n((?:[ \t]+-[^\n]*\n(?:[ \t]+[^\n]+\n)*)*)',
        fm_text
    )
    if not upward_match:
        return links

    block = upward_match.group(1)
    # Each entry starts with '    - url:' pattern
    entry_re = re.compile(
        r'[ \t]+-[ \t]*\n?[ \t]+url:[ \t]*"?([^"\n]+)"?\n[ \t]+text:[ \t]*"?([^"\n]+)"?',
        re.MULTILINE
    )
    for m in entry_re.finditer(block):
        links.append({'url': m.group(1).strip(), 'text': m.group(2).strip()})
    return links


# ---------------------------------------------------------------------------
# Page existence checker
# ---------------------------------------------------------------------------

def url_to_expected_paths(url):
    """
    Given a Hugo site-relative URL like /repatriation-from-thailand/,
    return a list of filesystem paths that would mean the page exists.
    """
    # Strip leading/trailing slashes
    path = url.strip('/')

    if path == 'contact':
        return [
            os.path.join(CONTENT_DIR, 'contact.md'),
            os.path.join(CONTENT_DIR, 'contact', '_index.md'),
        ]

    # /repatriation-from-{slug}/
    m = re.match(r'^repatriation-from-([\w-]+)$', path)
    if m:
        slug = m.group(1)
        return [
            os.path.join(COUNTRY_DIR, slug, '_index.md'),
            os.path.join(COUNTRY_DIR, slug + '.md'),
        ]

    # /guides/death-abroad-{slug}/
    m = re.match(r'^guides/death-abroad-([\w-]+)$', path)
    if m:
        slug = m.group(1)
        return [
            os.path.join(GUIDES_DIR, f'death-abroad-{slug}.md'),
            os.path.join(GUIDES_DIR, slug, '_index.md'),
        ]

    # /routes/{slug}/
    m = re.match(r'^routes/([\w-]+)$', path)
    if m:
        slug = m.group(1)
        return [
            os.path.join(ROUTES_DIR, slug + '.md'),
        ]

    # Generic fallback: try as section _index or leaf
    return [
        os.path.join(CONTENT_DIR, path, '_index.md'),
        os.path.join(CONTENT_DIR, path + '.md'),
    ]


def page_exists(url):
    """Return True if any candidate path for this URL exists on disk."""
    for p in url_to_expected_paths(url):
        if os.path.exists(p):
            return True
    return False


# ---------------------------------------------------------------------------
# Extract slug from upward URL for correction lookup
# ---------------------------------------------------------------------------

def slug_from_upward_url(url):
    """Extract the slug embedded in a /repatriation-from-X/ or /guides/death-abroad-X/ URL."""
    path = url.strip('/')
    m = re.match(r'^repatriation-from-([\w-]+)$', path)
    if m:
        return m.group(1), 'hub'
    m = re.match(r'^guides/death-abroad-([\w-]+)$', path)
    if m:
        return m.group(1), 'guide'
    return None, None


def corrected_url(url):
    """Return the corrected URL if a slug correction is known, else None."""
    slug, kind = slug_from_upward_url(url)
    if slug is None:
        return None
    correct = SLUG_CORRECTIONS.get(slug)
    if correct is None:
        return None
    if kind == 'hub':
        return f'/repatriation-from-{correct}/'
    if kind == 'guide':
        return f'/guides/death-abroad-{correct}/'
    return None


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------

def audit_routes(routes_dir):
    results = []
    md_files = sorted([
        f for f in os.listdir(routes_dir)
        if f.endswith('.md') and f != '_index.md'
    ])

    for filename in md_files:
        path = os.path.join(routes_dir, filename)
        slug = filename[:-3]

        with open(path, 'r', encoding='utf-8') as fh:
            raw = fh.read()

        m = FRONTMATTER_RE.match(raw)
        if not m:
            continue
        fm_text = m.group(1)

        upward_links = extract_upward_links(fm_text)
        broken = []
        for link in upward_links:
            url = link['url']
            if not page_exists(url):
                correction = corrected_url(url)
                broken.append({
                    'url': url,
                    'text': link['text'],
                    'correction': correction,
                    'fixable': correction is not None,
                })

        if broken:
            results.append({'slug': slug, 'broken': broken})

    return results


def print_fix_map():
    print('=== Slug correction map ===')
    print()
    print('Used to rewrite upward link URLs in route frontmatter (Chunk 3c):')
    print()
    print(f'{"Wrong slug in frontmatter":<45} {"Correct slug (dir/file exists)"}')
    print('-' * 80)
    for wrong, right in sorted(SLUG_CORRECTIONS.items()):
        print(f'  {wrong:<43}  {right}')
    print()
    print('Slugs with no existing hub (links must be omitted until hub built):')
    for s in sorted(NO_HUB_SLUGS):
        print(f'  {s}')


def main():
    parser = argparse.ArgumentParser(
        description='Audit upward links in route frontmatter'
    )
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--fix-map', action='store_true',
                        help='Print slug correction map and exit')
    args = parser.parse_args()

    if args.fix_map:
        print_fix_map()
        return

    routes_dir = os.path.abspath(ROUTES_DIR)
    if not os.path.isdir(routes_dir):
        print(f'ERROR: routes directory not found: {routes_dir}')
        print('Run from the repository root.')
        sys.exit(1)

    results = audit_routes(routes_dir)

    total_broken_links = sum(len(r['broken']) for r in results)
    total_fixable = sum(
        sum(1 for b in r['broken'] if b['fixable'])
        for r in results
    )
    total_no_fix = total_broken_links - total_fixable

    if args.json:
        output = {
            'summary': {
                'routes_with_broken_upward': len(results),
                'total_broken_links': total_broken_links,
                'fixable': total_fixable,
                'no_fix_available': total_no_fix,
            },
            'routes': results,
        }
        print(json.dumps(output, indent=2))
        return

    print()
    print('=== audit_upward_links.py ===')
    print(f'Routes dir  : {routes_dir}')
    print(f'Routes with broken upward links : {len(results)}')
    print(f'Total broken upward link URLs   : {total_broken_links}')
    print(f'  Fixable (correction known)    : {total_fixable}')
    print(f'  No fix (no hub exists)        : {total_no_fix}')
    print()

    # Group broken links by slug pattern for a concise summary
    broken_by_url = {}
    for r in results:
        for b in r['broken']:
            url = b['url']
            if url not in broken_by_url:
                broken_by_url[url] = {'count': 0, 'correction': b['correction'],
                                       'fixable': b['fixable']}
            broken_by_url[url]['count'] += 1

    print('--- Broken URL patterns (sorted by occurrence count) ---')
    print()
    for url, info in sorted(broken_by_url.items(),
                            key=lambda x: -x[1]['count']):
        fix = info['correction'] if info['correction'] else 'NO HUB EXISTS'
        print(f'  {info["count"]:>4}x  {url}')
        print(f'          -> {fix}')
        print()

    if len(results) <= 30:
        print('--- Per-route detail ---')
        print()
        for r in results:
            print(f'  {r["slug"]}')
            for b in r['broken']:
                fix = b['correction'] if b['correction'] else 'NO FIX'
                print(f'    BROKEN: {b["url"]}')
                print(f'    FIX   : {fix}')
            print()
    else:
        print(f'(Per-route detail suppressed for {len(results)} routes;'
              f' use --json for full output)')


if __name__ == '__main__':
    main()
