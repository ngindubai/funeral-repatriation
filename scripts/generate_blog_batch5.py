#!/usr/bin/env python3
"""
generate_blog_batch5.py
Stage 3 Engine 3 Batch 5 -- Special-circumstance cluster.

Workforce pipeline applied (per CLAUDE.md):
  The Wordsmith       (voice: senior repatriation coordinator / consular affairs)
  The Interrogator    (FAQs from genuine edge-case family questions)
  The Chameleon       (humaniser: no em dashes, varied sentence length)
  The Optimiser       (FAQPage schema, internal links, descriptive metadata)
  The Auditor         (YMYL gate: legally sensitive, careful hedging throughout)

All articles in this batch:
  - British English
  - YAML front matter with FAQs
  - 2+ internal links per article
  - Named author personas
  - No em dashes
  - Extra care: these are high-stakes sensitive topics requiring
    careful hedging (child deaths especially)

Target: 5 articles covering special circumstances that involve
materially different processes than standard adult repatriation cases.
High search intent, low existing coverage.
"""

import os

BLOG_DIR = os.path.join("site", "content", "blog")

ARTICLES = [
    {
        "slug": "death-of-a-child-abroad-repatriation",
        "title": "Death of a Child Abroad: Repatriation Guidance for Families",
        "description": "When a child dies abroad, repatriation involves the same core process but with additional legal steps, more intensive consular involvement, and specific emotional support needs. This guide explains what is different.",
        "date": "2026-06-02",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "Special circumstances",
        "tags": ["child-death", "special-circumstances", "consular"],
        "internal_links": [
            "/blog/first-24-hours-after-a-death-abroad-checklist/",
            "/blog/post-mortem-delays-and-what-families-can-control/",
        ],
    },
    {
        "slug": "repatriation-of-uk-military-personnel",
        "title": "Repatriation of UK Military Personnel: How It Differs from Civilian Cases",
        "description": "The repatriation of UK military personnel who die on active service or overseas operations follows a separate process managed by the Ministry of Defence. This guide explains how it works and what families experience.",
        "date": "2026-06-02",
        "author": "James Whitfield",
        "author_title": "Senior Repatriation Coordinator, Repatriate Service",
        "category": "Special circumstances",
        "tags": ["military", "mod-repatriation", "special-circumstances"],
        "internal_links": [
            "/blog/who-pays-for-repatriation-when-someone-dies-abroad/",
            "/blog/how-long-does-repatriation-take/",
        ],
    },
    {
        "slug": "dual-national-deaths-which-country-process-applies",
        "title": "Dual National Deaths Abroad: Which Country's Process Applies?",
        "description": "When a person with dual nationality dies abroad, both countries may have jurisdiction, creating potential complications in death registration, document authority, and consular assistance. This guide explains how these cases work in practice.",
        "date": "2026-06-02",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Special circumstances",
        "tags": ["dual-nationality", "consular", "special-circumstances"],
        "internal_links": [
            "/blog/fcdo-documents-for-repatriation/",
            "/blog/documents-needed-to-repatriate-body-to-uk/",
        ],
    },
    {
        "slug": "repatriation-when-no-family-can-be-contacted",
        "title": "Repatriation When No Family Can Be Contacted: What Happens to Unclaimed Remains",
        "description": "When a British national dies abroad and no family can be identified or contacted, a different set of procedures applies. This guide explains how unclaimed deaths are handled internationally and what the FCDO does.",
        "date": "2026-06-02",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Special circumstances",
        "tags": ["unclaimed-remains", "consular", "special-circumstances"],
        "internal_links": [
            "/blog/british-embassy-role-death-abroad/",
            "/blog/who-pays-for-repatriation-when-someone-dies-abroad/",
        ],
    },
    {
        "slug": "death-abroad-criminal-case-how-repatriation-works",
        "title": "Death Abroad Involving a Criminal Case: How Repatriation Works",
        "description": "Where a death abroad is linked to a criminal investigation, repatriation is subject to the decisions of foreign prosecutors and courts. This guide explains what families can expect and how the process interacts with the legal proceedings.",
        "date": "2026-06-02",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Special circumstances",
        "tags": ["criminal-case", "investigation", "special-circumstances"],
        "internal_links": [
            "/blog/repatriation-timeline-by-cause-of-death/",
            "/blog/post-mortem-delays-and-what-families-can-control/",
        ],
    },
]


def slug_exists(slug: str) -> bool:
    return os.path.exists(os.path.join(BLOG_DIR, f"{slug}.md"))


def main():
    print("Engine 3 -- Blog Batch 5: Special-circumstance cluster")
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
            print(f"    Links:   {', '.join(article['internal_links'])}")
            new += 1
    print()
    print(f"Summary: {new} new, {skipped} already exist")


if __name__ == "__main__":
    main()
