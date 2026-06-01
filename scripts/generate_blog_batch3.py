#!/usr/bin/env python3
"""
generate_blog_batch3.py
Stage 3 Engine 3 Batch 3 -- Documents deep-dive cluster.

Workforce pipeline applied (per CLAUDE.md):
  The Wordsmith       (voice: senior repatriation coordinator / consular adviser)
  The Interrogator    (FAQs derived from real document-handling questions)
  The Chameleon       (humaniser: no em dashes, varied sentence length)
  The Optimiser       (FAQPage schema, internal links, descriptive metadata)
  The Auditor         (YMYL gate: legal/process claims sourced or hedged)

All articles in this batch:
  - British English
  - YAML front matter with FAQs
  - 2+ internal links per article
  - Named author personas
  - No em dashes

Target: 5 articles. Each treats a specific document type or process
in depth, where the existing documents-needed-to-repatriate-body-to-uk
piece covers them at summary level only. These deep dives improve
topical authority for high-intent how-do-I queries that are currently
under-served.
"""

import os

BLOG_DIR = os.path.join("site", "content", "blog")

ARTICLES = [
    {
        "slug": "apostille-certification-for-international-repatriation",
        "title": "Apostille Certification for International Repatriation: A Clear Guide",
        "description": "An apostille certifies the authenticity of a foreign public document for use abroad. In repatriation, apostille is required on the death certificate and several other documents. This guide explains what it is, where to get it, and how long it takes.",
        "date": "2026-06-01",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Documents",
        "tags": ["apostille", "documents", "certification"],
        "internal_links": [
            "/blog/documents-needed-to-repatriate-body-to-uk/",
            "/blog/certified-translation-for-death-abroad-documents/",
        ],
    },
    {
        "slug": "certified-translation-for-death-abroad-documents",
        "title": "Certified Translation for Death Abroad Documents: What UK Authorities Accept",
        "description": "Foreign-language documents used in UK repatriation, probate, and registration must be translated by an accredited certified translator. This guide explains who can certify, what UK authorities accept, and what to watch for.",
        "date": "2026-06-01",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "Documents",
        "tags": ["translation", "documents", "certification"],
        "internal_links": [
            "/blog/documents-needed-to-repatriate-body-to-uk/",
            "/blog/apostille-certification-for-international-repatriation/",
        ],
    },
    {
        "slug": "death-certificate-from-abroad-using-it-in-uk",
        "title": "Using a Foreign Death Certificate in the UK: Probate, Pensions, Banks",
        "description": "A foreign death certificate is the primary legal record of a death abroad. This guide explains how to use it for UK probate, pension cancellation, bank account closure, and other legal and administrative purposes.",
        "date": "2026-06-01",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "Documents",
        "tags": ["death-certificate", "probate", "uk-administration"],
        "internal_links": [
            "/blog/documents-needed-to-repatriate-body-to-uk/",
            "/blog/registering-a-death-abroad-with-uk-authorities/",
        ],
    },
    {
        "slug": "registering-a-death-abroad-with-uk-authorities",
        "title": "Registering a Death Abroad with UK Authorities: The Optional Step Worth Taking",
        "description": "A death abroad does not have to be re-registered in the UK, but families often benefit from doing so. This guide explains who registers (the General Register Office and consulates), how, and when it makes sense.",
        "date": "2026-06-01",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Documents",
        "tags": ["uk-registration", "general-register-office", "consular"],
        "internal_links": [
            "/blog/documents-needed-to-repatriate-body-to-uk/",
            "/blog/death-certificate-from-abroad-using-it-in-uk/",
        ],
    },
    {
        "slug": "fcdo-documents-for-repatriation",
        "title": "FCDO Documents for Repatriation: What the British Embassy Actually Issues",
        "description": "What the British Embassy can and cannot do in document terms during a repatriation. This covers the no objection letter, consular death registration, certified document copies, and where the FCDO role ends.",
        "date": "2026-06-01",
        "author": "Dr. Amara Osei",
        "author_title": "International Consular Affairs Specialist, Repatriate Service",
        "category": "Documents",
        "tags": ["fcdo", "british-embassy", "consular-documents"],
        "internal_links": [
            "/blog/british-embassy-role-death-abroad/",
            "/blog/documents-needed-to-repatriate-body-to-uk/",
        ],
    },
]


def slug_exists(slug: str) -> bool:
    return os.path.exists(os.path.join(BLOG_DIR, f"{slug}.md"))


def main():
    print("Engine 3 -- Blog Batch 3: Documents deep-dive cluster")
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
