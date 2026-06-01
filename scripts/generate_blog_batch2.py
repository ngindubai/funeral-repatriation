#!/usr/bin/env python3
"""
generate_blog_batch2.py
Stage 3 Engine 3 Batch 2 -- Timeline cluster.

Workforce pipeline applied (per CLAUDE.md):
  The Wordsmith       (voice: senior repatriation coordinator)
  The Interrogator    (FAQs derived from real bereaved-family timeline questions)
  The Chameleon       (humaniser: no em dashes, varied sentence length)
  The Optimiser       (FAQPage schema, internal links, descriptive metadata)
  The Auditor         (YMYL gate: realistic ranges only, no promises of speed)

All articles in this batch:
  - British English
  - YAML front matter with FAQs
  - 2+ internal links per article
  - Named author personas
  - No em dashes
  - No promises of expedited delivery
  - Ranges hedged with realistic worst-case scenarios

Target: 5 articles covering timeline scenarios that the single existing
generic timeline article does not address in depth. The existing
how-long-does-repatriation-take piece gives broad ranges; these articles
cover scenario-specific timelines (cause of death, region, post-mortem
extension, popular tourist destinations, expedited requests).
"""

import os

BLOG_DIR = os.path.join("site", "content", "blog")

ARTICLES = [
    {
        "slug": "repatriation-timeline-by-cause-of-death",
        "title": "Repatriation Timeline by Cause of Death: What Families Should Expect",
        "description": "Natural death, accident, suspected suicide, suspected homicide, deaths involving alcohol or drugs. Cause of death is the biggest determinant of how long repatriation takes. This guide explains why.",
        "date": "2026-06-01",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Timeline guidance",
        "tags": ["timeline", "cause-of-death", "post-mortem"],
        "internal_links": [
            "/blog/how-long-does-repatriation-take/",
            "/blog/post-mortem-delays-and-what-families-can-control/",
        ],
    },
    {
        "slug": "repatriation-from-tourist-destinations-typical-timeline",
        "title": "Repatriation from Tourist Destinations: Realistic Timelines for Common Holiday Locations",
        "description": "Spain, Greece, Turkey, Egypt, Thailand, Mexico, the Canary Islands. How long does repatriation actually take from the destinations where most British holiday deaths occur, and what slows it down.",
        "date": "2026-06-01",
        "author": "James Whitfield",
        "author_title": "Senior Repatriation Coordinator, Repatriate Service",
        "category": "Timeline guidance",
        "tags": ["timeline", "tourist-destinations", "holiday-deaths"],
        "internal_links": [
            "/blog/how-long-does-repatriation-take/",
            "/repatriation-from-spain/",
        ],
    },
    {
        "slug": "repatriation-from-asia-timeline-realistic-expectations",
        "title": "Repatriation from Asia: Realistic Timeline Expectations for UK Families",
        "description": "Thailand, India, Vietnam, Philippines, Indonesia, Sri Lanka. Why Asia repatriation timelines are longer than European ones, where the delays sit, and what families can do.",
        "date": "2026-06-01",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Timeline guidance",
        "tags": ["timeline", "asia", "long-haul"],
        "internal_links": [
            "/repatriation-from-thailand/",
            "/blog/how-long-does-repatriation-take/",
        ],
    },
    {
        "slug": "post-mortem-extension-impact-on-repatriation-timeline",
        "title": "When a Post-Mortem Extends the Timeline: What Families Can Expect",
        "description": "Post-mortems are the single biggest reason a repatriation case extends from days into weeks. This guide explains exactly how the extension works, country by country, and what families can do during the wait.",
        "date": "2026-06-01",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Timeline guidance",
        "tags": ["timeline", "post-mortem", "coroner"],
        "internal_links": [
            "/blog/post-mortem-delays-and-what-families-can-control/",
            "/blog/how-long-does-repatriation-take/",
        ],
    },
    {
        "slug": "expedited-repatriation-when-and-how",
        "title": "Expedited Repatriation: When It Is Possible and How to Request It",
        "description": "Where genuine hardship justifies it, repatriation timelines can sometimes be shortened. This guide explains the realistic circumstances, the right channels, and the limits of what speed can achieve.",
        "date": "2026-06-01",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Timeline guidance",
        "tags": ["timeline", "expedited", "consular-support"],
        "internal_links": [
            "/blog/how-long-does-repatriation-take/",
            "/blog/post-mortem-delays-and-what-families-can-control/",
        ],
    },
]


def slug_exists(slug: str) -> bool:
    return os.path.exists(os.path.join(BLOG_DIR, f"{slug}.md"))


def main():
    print("Engine 3 -- Blog Batch 2: Timeline cluster")
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
