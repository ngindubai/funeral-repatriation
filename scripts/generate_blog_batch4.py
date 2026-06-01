#!/usr/bin/env python3
"""
generate_blog_batch4.py
Stage 3 Engine 3 Batch 4 -- Religious and cultural specifics.

Workforce pipeline applied (per CLAUDE.md):
  The Wordsmith       (voice: bereavement adviser, respectful and precise)
  The Interrogator    (FAQs derived from real faith-specific family questions)
  The Chameleon       (humaniser: no em dashes, varied sentence length)
  The Optimiser       (FAQPage schema, internal links, descriptive metadata)
  The Auditor         (YMYL gate: no sweeping religious claims, hedged where
                       practice varies within traditions)

All articles in this batch:
  - British English
  - YAML front matter with FAQs
  - 2+ internal links per article
  - Named author personas
  - No em dashes
  - Respectful and accurate tone on all faith topics
  - Hedged where practice varies within traditions (e.g. different madhabs
    in Islam, different communities in Judaism)
  - No prescriptive religious rulings -- describes common practice,
    not religious law

Target: 5 articles covering faith-specific repatriation considerations.
The existing general piece on religious repatriation covers this at
summary level only. These deep dives serve families searching for
specific answers about their tradition.
"""

import os

BLOG_DIR = os.path.join("site", "content", "blog")

ARTICLES = [
    {
        "slug": "muslim-repatriation-requirements-and-ghusl",
        "title": "Muslim Repatriation: Ghusl, Kafan, and What UK Families Need to Know",
        "description": "Muslim funeral rites require ghusl (ritual washing), kafan (shrouding), and prompt burial. When a Muslim dies abroad, these requirements interact with international repatriation in specific ways. This guide explains what to expect.",
        "date": "2026-06-02",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Religious guidance",
        "tags": ["muslim", "islamic-funeral", "ghusl", "cultural-requirements"],
        "internal_links": [
            "/blog/repatriation-from-uae-guide/",
            "/blog/how-long-does-repatriation-take/",
        ],
    },
    {
        "slug": "jewish-repatriation-requirements-and-tahara",
        "title": "Jewish Repatriation: Tahara, Shmirah, and Halacha in International Cases",
        "description": "Jewish law requires prompt burial, tahara (ritual purification), and uninterrupted shmirah (guarding). International repatriation creates specific halachic challenges. This guide explains the main considerations for UK families.",
        "date": "2026-06-02",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Religious guidance",
        "tags": ["jewish", "halacha", "tahara", "cultural-requirements"],
        "internal_links": [
            "/blog/how-long-does-repatriation-take/",
            "/blog/post-mortem-delays-and-what-families-can-control/",
        ],
    },
    {
        "slug": "hindu-repatriation-cremation-options-abroad",
        "title": "Hindu Repatriation: Cremation Abroad or Repatriation to the UK?",
        "description": "Hindu tradition strongly favours cremation, ideally on the banks of a sacred river. When a Hindu dies abroad, families face a real choice: cremation in the country of death or repatriation of the body. This guide covers the practical and religious considerations.",
        "date": "2026-06-02",
        "author": "Thomas Anand",
        "author_title": "International Logistics Coordinator, Repatriate Service",
        "category": "Religious guidance",
        "tags": ["hindu", "cremation", "cultural-requirements"],
        "internal_links": [
            "/blog/bringing-ashes-home-on-a-passenger-flight/",
            "/blog/repatriation-cost-guide/",
        ],
    },
    {
        "slug": "sikh-repatriation-considerations",
        "title": "Sikh Repatriation: Funeral Rites, Cremation, and International Cases",
        "description": "Sikh funeral rites centre on cremation and the reading of Sikh scriptures. When a Sikh dies abroad, families may repatriate the body or have cremation performed locally. This guide covers the key considerations.",
        "date": "2026-06-02",
        "author": "Thomas Anand",
        "author_title": "International Logistics Coordinator, Repatriate Service",
        "category": "Religious guidance",
        "tags": ["sikh", "cremation", "cultural-requirements"],
        "internal_links": [
            "/blog/bringing-ashes-through-connecting-flights/",
            "/blog/repatriation-cost-guide/",
        ],
    },
    {
        "slug": "non-religious-secular-repatriation",
        "title": "Non-Religious and Secular Repatriation: Practical Choices Without Religious Requirements",
        "description": "For families with no religious tradition, the decisions around repatriation and final arrangements are entirely personal. This guide covers the practical choices available and how to approach them without religious constraint.",
        "date": "2026-06-02",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "Religious guidance",
        "tags": ["secular", "non-religious", "humanist", "choices"],
        "internal_links": [
            "/blog/repatriation-cost-guide/",
            "/blog/who-pays-for-repatriation-when-someone-dies-abroad/",
        ],
    },
]


def slug_exists(slug: str) -> bool:
    return os.path.exists(os.path.join(BLOG_DIR, f"{slug}.md"))


def main():
    print("Engine 3 -- Blog Batch 4: Religious and cultural specifics")
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
