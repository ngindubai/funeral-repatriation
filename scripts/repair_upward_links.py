#!/usr/bin/env python3
"""
scripts/repair_upward_links.py
Rewrite broken upward link URLs in all route frontmatter files.

Applies the slug correction map from Chunk 3b audit to every .md file in
site/content/routes/. Pure text substitution -- no YAML parser required.

Usage:
    python scripts/repair_upward_links.py            # dry-run (show changes, no writes)
    python scripts/repair_upward_links.py --apply    # write changes

Run from the repository root.

Safe to run multiple times: already-corrected files are skipped (idempotent).
"""

import argparse
import os
import sys

ROUTES_DIR = os.path.join('site', 'content', 'routes')

# ---------------------------------------------------------------------------
# URL substitution map
# Key   = broken URL string currently in route frontmatter upward links
# Value = correct URL that corresponds to an existing Hugo page
# ---------------------------------------------------------------------------
# Root cause: route generators used the 197-canonical country slug from
# data/countries-197.json as origin_slug and wrote upward links using those
# slugs, but the country hub pages were built earlier using a different slug
# set (the one in site/content/countries/ directory names).
#
# The layout filter (Chunk 3a) already suppresses broken links from rendering.
# This script fixes the underlying data so correct links restore on next build.
CORRECTIONS = {
    # United States routes used 'united-states' but hub is under 'usa'
    '/repatriation-from-united-states/': '/repatriation-from-usa/',
    '/guides/death-abroad-united-states/': '/guides/death-abroad-usa/',

    # DRC routes used 'democratic-republic-of-the-congo' but hub is under
    # 'democratic-republic-of-congo' (without 'the')
    '/repatriation-from-democratic-republic-of-the-congo/': '/repatriation-from-democratic-republic-of-congo/',
    '/guides/death-abroad-democratic-republic-of-the-congo/': '/guides/death-abroad-democratic-republic-of-congo/',

    # Gambia routes used 'gambia' but hub is under 'the-gambia'
    '/repatriation-from-gambia/': '/repatriation-from-the-gambia/',
    '/guides/death-abroad-gambia/': '/guides/death-abroad-the-gambia/',

    # Congo (Republic) routes used 'congo' but hub is under 'republic-of-congo'
    '/repatriation-from-congo/': '/repatriation-from-republic-of-congo/',
    '/guides/death-abroad-congo/': '/guides/death-abroad-republic-of-congo/',

    # Cabo Verde routes used 'cabo-verde' but hub is under 'cape-verde'
    '/repatriation-from-cabo-verde/': '/repatriation-from-cape-verde/',
    '/guides/death-abroad-cabo-verde/': '/guides/death-abroad-cape-verde/',

    # Vatican City routes used 'vatican-city' but hub is under 'holy-see'
    '/repatriation-from-vatican-city/': '/repatriation-from-holy-see/',
    '/guides/death-abroad-vatican-city/': '/guides/death-abroad-holy-see/',

    # NOTE: 'palestine' has no existing hub page. Its upward links are left
    # as-is; the Chunk 3a layout filter suppresses them from rendering until
    # a palestine hub page is built.
}


def repair_file(path, apply=False):
    """Apply URL corrections to a single file. Returns (changed, old, new)."""
    with open(path, 'r', encoding='utf-8') as fh:
        original = fh.read()

    patched = original
    for wrong, right in CORRECTIONS.items():
        patched = patched.replace(wrong, right)

    if patched == original:
        return False, original, original

    if apply:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(patched)

    return True, original, patched


def main():
    parser = argparse.ArgumentParser(
        description='Repair broken upward link URLs in route frontmatter'
    )
    parser.add_argument(
        '--apply', action='store_true',
        help='Write changes (default is dry-run)'
    )
    args = parser.parse_args()

    routes_dir = os.path.abspath(ROUTES_DIR)
    if not os.path.isdir(routes_dir):
        print(f'ERROR: routes directory not found: {routes_dir}')
        print('Run from the repository root.')
        sys.exit(1)

    md_files = sorted([
        f for f in os.listdir(routes_dir)
        if f.endswith('.md') and f != '_index.md'
    ])

    mode = 'APPLY' if args.apply else 'DRY-RUN'
    changed_files = []
    unchanged = 0

    for filename in md_files:
        path = os.path.join(routes_dir, filename)
        changed, original, patched = repair_file(path, apply=args.apply)
        if changed:
            changed_files.append(filename)
            if not args.apply:
                # Show what would change
                for wrong, right in CORRECTIONS.items():
                    if wrong in original:
                        print(f'  [{filename}]  {wrong}  ->  {right}')
        else:
            unchanged += 1

    print()
    print(f'=== repair_upward_links.py [{mode}] ===')
    print(f'Routes directory : {routes_dir}')
    print(f'Files scanned    : {len(md_files)}')
    print(f'Files changed    : {len(changed_files)}')
    print(f'Files unchanged  : {unchanged}')
    print()

    if args.apply and changed_files:
        print(f'[APPLY] Wrote corrections to {len(changed_files)} files.')
        print()
        print('Changed files:')
        for f in changed_files:
            print(f'  {f}')
    elif not args.apply and changed_files:
        print(f'[DRY-RUN] No files written.')
        print(f'Run with --apply to fix {len(changed_files)} files.')

    print()


if __name__ == '__main__':
    main()
