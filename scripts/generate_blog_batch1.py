#!/usr/bin/env python3
"""
generate_blog_batch1.py
Stage 3 Engine 3 Batch 1 -- Blog articles on commercial-intent cost cluster.

This is the first script in the Engine 3 blog-batch factory for funeral-repatriation.
The earlier add-batch{N}.py scripts in this directory add country data to
countries_repatriation.json -- they are unrelated to blog content.

Workforce pipeline applied (per CLAUDE.md):
  The Wordsmith       (voice: senior repatriation coordinator / bereavement adviser)
  The Interrogator    (FAQs derived from real bereaved-family questions)
  The Chameleon       (humaniser: no em dashes, no banned vocab, varied sentence length)
  The Optimiser       (FAQPage schema, internal link minimum, descriptive metadata)
  The Auditor         (YMYL gate: no safety guarantees, no specific prices outside
                       broad ranges, named-source attribution on every claim)

All articles in this batch:
  - British English
  - YAML front matter
  - FAQPage schema via faqs[] frontmatter array
  - 2+ internal links per article
  - Named author personas (E-E-A-T signal)
  - No em dashes (use hyphens, commas, full stops)
  - No safety guarantees, no specific firm pricing
  - YMYL-compliant: legal and financial claims sourced or hedged

Target: 5 articles in the commercial-intent cost cluster.
These complement (not duplicate) the existing repatriation-cost-guide.md
which covers country-by-country price ranges. This batch covers:
payer responsibility, uninsured scenario, quote evaluation,
crowdfunding, and the cargo-cost mechanism.
"""

import os

BLOG_DIR = os.path.join("site", "content", "blog")

ARTICLES = [
    {
        "slug": "who-pays-for-repatriation-when-someone-dies-abroad",
        "title": "Who Pays for Repatriation When Someone Dies Abroad?",
        "description": "Travel insurance, employer schemes, the FCDO, family savings, charitable funds. A clear guide to who actually pays for repatriation in different circumstances.",
        "date": "2026-06-01",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "Cost guidance",
        "tags": ["cost", "insurance", "payer-responsibility"],
        "internal_links": [
            "/blog/repatriation-cost-guide/",
            "/blog/travel-insurance-claim-after-death-abroad/",
        ],
    },
    {
        "slug": "repatriation-cost-without-travel-insurance",
        "title": "Repatriation Cost Without Travel Insurance: What Families Face",
        "description": "If your loved one died abroad without travel insurance, the family typically pays the full repatriation cost directly. This guide explains realistic ranges, payment options, and where hardship support exists.",
        "date": "2026-06-01",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "Cost guidance",
        "tags": ["cost", "no-insurance", "hardship"],
        "internal_links": [
            "/blog/repatriation-cost-guide/",
            "/blog/death-abroad-no-travel-insurance/",
        ],
    },
    {
        "slug": "repatriation-quote-what-to-check",
        "title": "What to Check on a Repatriation Quote (Before You Pay Anything)",
        "description": "A practical checklist for evaluating a repatriation quote, with the items every quote should itemise, the red flags that signal cost padding, and the right questions to ask before paying a deposit.",
        "date": "2026-06-01",
        "author": "James Whitfield",
        "author_title": "Senior Repatriation Coordinator, Repatriate Service",
        "category": "Cost guidance",
        "tags": ["cost", "quotes", "buyer-checklist"],
        "internal_links": [
            "/blog/how-to-choose-a-repatriation-funeral-director/",
            "/blog/repatriation-cost-guide/",
        ],
    },
    {
        "slug": "crowdfunding-repatriation-costs",
        "title": "Crowdfunding Repatriation Costs: When It Helps and How to Run It",
        "description": "When travel insurance does not cover a repatriation, crowdfunding is one of the few options remaining. This guide explains when it works, which platforms families use, and how to run a campaign with dignity in a sensitive moment.",
        "date": "2026-06-01",
        "author": "Claire Sutton",
        "author_title": "Bereavement and Repatriation Adviser, Repatriate Service",
        "category": "Cost guidance",
        "tags": ["cost", "crowdfunding", "fundraising"],
        "internal_links": [
            "/blog/repatriation-cost-without-travel-insurance/",
            "/blog/death-abroad-no-travel-insurance/",
        ],
    },
    {
        "slug": "airline-cargo-costs-repatriation-explained",
        "title": "How Airline Cargo Costs Work in Repatriation: IATA Codes, Freight Rates, and Why It Varies",
        "description": "The flight portion of a repatriation is air cargo, not a passenger ticket. This explains how IATA classifies human remains, how cargo rates are calculated, and why the same route can cost very different amounts.",
        "date": "2026-06-01",
        "author": "Thomas Anand",
        "author_title": "International Logistics Coordinator, Repatriate Service",
        "category": "Cost guidance",
        "tags": ["cost", "airline-cargo", "logistics"],
        "internal_links": [
            "/blog/how-airline-cargo-booking-works-for-repatriation/",
            "/blog/repatriation-cost-guide/",
        ],
    },
]


def slug_exists(slug: str) -> bool:
    return os.path.exists(os.path.join(BLOG_DIR, f"{slug}.md"))


def main():
    print("Engine 3 -- Blog Batch 1: Commercial-intent cost cluster")
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
    print()
    print("Content files are committed directly via GitHub MCP in this batch.")
    print("Workforce loop applied per CLAUDE.md.")


if __name__ == "__main__":
    main()
