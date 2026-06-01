#!/usr/bin/env python3
"""
generate_blog_batch6.py
Stage 3 Engine 3 Batch 6 -- UK reception cluster.

What happens when the body arrives in the UK is almost entirely
undocumented on the site. Families asking what to expect after the
flight have no current content to land on. This batch fills that gap.

Workforce pipeline applied (per CLAUDE.md):
  The Wordsmith       (voice: senior repatriation coordinator)
  The Interrogator    (FAQs from real UK-reception family questions)
  The Chameleon       (humaniser: no em dashes, varied sentence length)
  The Optimiser       (FAQPage schema, internal links, metadata)
  The Auditor         (YMYL gate: accurate UK legal process, hedged)

All articles:
  - British English, no em dashes
  - FAQs in frontmatter
  - 2+ internal links
  - Named author personas
"""

import os

BLOG_DIR = os.path.join("site", "content", "blog")

ARTICLES = [
    {
        "slug": "what-happens-when-body-arrives-uk-from-abroad",
        "title": "What Happens When a Body Arrives in the UK from Abroad",
        "description": "From cargo terminal to chapel of rest: a step-by-step explanation of what happens when a repatriated body arrives at a UK airport, who handles it, and what the family does next.",
        "date": "2026-06-02",
        "author": "James Whitfield",
        "author_title": "Senior Repatriation Coordinator, Repatriate Service",
        "category": "UK reception",
        "tags": ["uk-reception", "arrival", "cargo-terminal"],
        "internal_links": [
            "/blog/how-airline-cargo-booking-works-for-repatriation/",
            "/blog/how-to-choose-a-repatriation-funeral-director/",
        ],
    },
    {
        "slug": "uk-coroner-and-repatriated-bodies",
        "title": "UK Coroner and Repatriated Bodies: When a Coroner Gets Involved",
        "description": "Not every repatriated body goes directly to the funeral director. Some are referred to the UK coroner. This guide explains when a coroner referral happens, what it means, and how it affects the funeral timeline.",
        "date": "2026-06-02",
        "author": "James Whitfield",
        "author_title": "Senior Repatriation Coordinator, Repatriate Service",
        "category": "UK reception",
        "tags": ["uk-coroner", "uk-reception", "legal-process"],
        "internal_links": [
            "/blog/what-happens-when-body-arrives-uk-from-abroad/",
            "/blog/repatriation-timeline-by-cause-of-death/",
        ],
    },
    {
        "slug": "uk-port-health-and-repatriation",
        "title": "UK Port Health and Repatriation: What Checks Apply at UK Airports",
        "description": "Human remains arriving in the UK from abroad are subject to port health checks. This guide explains what port health is, what they check, and what documentation must be in order.",
        "date": "2026-06-02",
        "author": "Thomas Anand",
        "author_title": "International Logistics Coordinator, Repatriate Service",
        "category": "UK reception",
        "tags": ["port-health", "uk-reception", "documentation"],
        "internal_links": [
            "/blog/documents-needed-to-repatriate-body-to-uk/",
            "/blog/what-happens-when-body-arrives-uk-from-abroad/",
        ],
    },
    {
        "slug": "registering-a-death-in-uk-after-repatriation",
        "title": "Registering a Death in the UK After Repatriation: What UK Funeral Directors Need",
        "description": "After a repatriated body arrives in the UK, there are specific registration and notification steps before the funeral can proceed. This guide covers what the UK funeral director needs, what families must provide, and what happens next.",
        "date": "2026-06-02",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "UK reception",
        "tags": ["uk-registration", "funeral-director", "uk-reception"],
        "internal_links": [
            "/blog/registering-a-death-abroad-with-uk-authorities/",
            "/blog/death-certificate-from-abroad-using-it-in-uk/",
        ],
    },
    {
        "slug": "uk-funeral-after-repatriation-what-to-expect",
        "title": "UK Funeral After Repatriation: Timing, Planning, and What to Expect",
        "description": "Planning a UK funeral for a repatriated person involves different timing constraints than a domestic death. This guide covers when you can book, what to tell the venue, and how to manage family expectations.",
        "date": "2026-06-02",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "UK reception",
        "tags": ["uk-funeral", "planning", "uk-reception"],
        "internal_links": [
            "/blog/what-happens-when-body-arrives-uk-from-abroad/",
            "/blog/repatriation-from-tourist-destinations-typical-timeline/",
        ],
    },
]


def slug_exists(slug: str) -> bool:
    return os.path.exists(os.path.join(BLOG_DIR, f"{slug}.md"))


def main():
    print("Engine 3 -- Blog Batch 6: UK reception cluster")
    print(f"Articles defined: {len(ARTICLES)}")
    print()
    new = 0
    skipped = 0
    for article in ARTICLES:
        if slug_exists(article["slug"]):
            print(f"  SKIP (exists): {article['slug']}.md")
            skipped += 1
        else:
            print(f"  NEW:           {article['slug']}.md")
            print(f"    Title:   {article['title']}")
            print(f"    Author:  {article['author']}")
            new += 1
    print()
    print(f"Summary: {new} new, {skipped} already exist")


if __name__ == "__main__":
    main()
