#!/usr/bin/env python3
"""
scripts/mark_thin_routes_noindex.py
Mark thin or same-country route pages with noindex: true in their frontmatter.

A page is "thin" if:
  (a) origin slug == destination slug  (e.g. united-kingdom-to-united-kingdom)
  (b) total word count across all frontmatter field values is under 300 words
      (route pages store all content in YAML frontmatter; the body below ---
       is empty, so we count the YAML values, not the body)

Usage:
    python scripts/mark_thin_routes_noindex.py            # dry-run (no writes)
    python scripts/mark_thin_routes_noindex.py --apply    # write changes

The sitemap template (site/layouts/sitemap.xml) already excludes pages
where .Params.noindex is true, so adding noindex: true to frontmatter
automatically drops the page from the sitemap on next build.

The baseof.html layout already injects:
  <meta name="robots" content="noindex, follow">
when .Params.noindex is true. No layout changes required.
"""

import argparse
import os
import re
import sys

ROUTES_DIR = os.path.join(
    os.path.dirname(__file__), '..', 'site', 'content', 'routes'
)

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---(?:\n|$)', re.DOTALL)

# Route pages store all content in YAML frontmatter.
# A well-formed route should have at least 300 words across all field values.
# Pages significantly below this are placeholder/stub pages.
MIN_FM_WORDS = 300


def parse_file(path):
    with open(path, 'r', encoding='utf-8') as fh:
        raw = fh.read()
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return None, None, None
    fm_text = m.group(1)
    body = raw[m.end():]
    return raw, fm_text, body


def extract_slug_from_filename(filename):
    return filename.replace('.md', '')


def same_country(slug):
    """True if origin and destination slugs are identical."""
    parts = slug.split('-to-')
    if len(parts) != 2:
        return False
    return parts[0] == parts[1]


def fm_word_count(fm_text):
    """Count words across all YAML string values in the frontmatter."""
    # Strip YAML keys (lines starting with a key: pattern) and count remaining words
    # in string values. Simple approach: remove YAML structural characters and count.
    text = re.sub(r'^\s*[\w_-]+\s*:', '', fm_text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', ' ', text)
    return len(text.split())


def already_noindex(fm_text):
    return bool(re.search(r'^\s*noindex\s*:\s*true', fm_text, re.MULTILINE))


def insert_noindex(fm_text):
    return fm_text + '\nnoindex: true'


def process_file(path, apply=False):
    filename = os.path.basename(path)
    slug = extract_slug_from_filename(filename)

    raw, fm_text, body = parse_file(path)
    if raw is None:
        return 'skip', slug, 'no frontmatter'

    if already_noindex(fm_text):
        return 'already', slug, 'already noindex'

    reasons = []

    if same_country(slug):
        reasons.append('same-country pair')

    wc = fm_word_count(fm_text)
    if wc < MIN_FM_WORDS:
        reasons.append(f'frontmatter content {wc} words < {MIN_FM_WORDS}')

    if not reasons:
        return 'ok', slug, ''

    if apply:
        new_fm = insert_noindex(fm_text)
        new_raw = f'---\n{new_fm}\n---\n{body}'
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_raw)

    return 'mark', slug, '; '.join(reasons)


def main():
    parser = argparse.ArgumentParser(
        description='Mark thin route pages with noindex: true'
    )
    parser.add_argument(
        '--apply', action='store_true',
        help='Write changes (default is dry-run)'
    )
    args = parser.parse_args()

    routes_dir = os.path.abspath(ROUTES_DIR)
    if not os.path.isdir(routes_dir):
        print(f'ERROR: routes directory not found: {routes_dir}')
        sys.exit(1)

    md_files = sorted([
        f for f in os.listdir(routes_dir)
        if f.endswith('.md') and f != '_index.md'
    ])

    total = len(md_files)
    results = {'mark': [], 'already': [], 'ok': [], 'skip': []}

    for filename in md_files:
        path = os.path.join(routes_dir, filename)
        status, slug, reason = process_file(path, apply=args.apply)
        results[status].append((slug, reason))

    mode = 'APPLY' if args.apply else 'DRY-RUN'
    print(f'\n=== mark_thin_routes_noindex.py [{mode}] ===')
    print(f'Routes directory : {routes_dir}')
    print(f'Files scanned    : {total}')
    print(f'To mark noindex  : {len(results["mark"])}')
    print(f'Already noindex  : {len(results["already"])}')
    print(f'Clean (no action): {len(results["ok"])}')
    print(f'Skipped (no FM)  : {len(results["skip"])}')

    if results['mark']:
        print(f'\n--- Pages to mark noindex ({len(results["mark"])}) ---')
        for slug, reason in results['mark']:
            print(f'  MARK  {slug}  [{reason}]')

    if results['already']:
        print(f'\n--- Already noindex ({len(results["already"])}) ---')
        for slug, _ in results['already']:
            print(f'  SKIP  {slug}')

    if results['skip']:
        print(f'\n--- Skipped (no frontmatter) ---')
        for slug, reason in results['skip']:
            print(f'  SKIP  {slug}  [{reason}]')

    if args.apply and results['mark']:
        print(f'\n[APPLY] Wrote noindex: true to {len(results["mark"])} files.')
    elif not args.apply and results['mark']:
        print(
            f'\n[DRY-RUN] No files written. '
            f'Run with --apply to write {len(results["mark"])} changes.'
        )

    print()


if __name__ == '__main__':
    main()
