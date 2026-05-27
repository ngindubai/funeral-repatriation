# The Auditor — QA Gate for Repatriate Service

> Load this file when running the QA gate (Step 5 of the quality gate). The Auditor checks every page before it is committed to master. Nothing ships with an Auditor error outstanding.

---

## AUDIT SCOPE

The Auditor checks three things:
1. **Frontmatter completeness** — all required fields present and valid
2. **Content quality** — no banned words, no thin content, no AI patterns
3. **SEO compliance** — title length, description length, schema presence

For route pages, a fourth check applies:
4. **Link integrity** — upward and sideways links are present and point to real URLs

---

## SECTION 1 — FRONTMATTER CHECKLIST (route pages)

Run these checks on every route page frontmatter block.

| Field | Rule | Pass condition |
|---|---|---|
| title | Required | Present, non-empty |
| title | Length | Under 60 characters |
| title | Content | Contains origin country name and destination country name |
| description | Required | Present, non-empty |
| description | Length | Under 155 characters |
| description | Content | Answers a direct question or states a timeline |
| origin_name | Required | Present, non-empty, matches countries_repatriation.json |
| dest_name | Required | Present, non-empty |
| slug | Required | Matches filename exactly |
| timeline_avg | Required | Present, format "X-Y days" or "X-Y weeks" |
| faqs | Required | Minimum 6 FAQ items |
| timeline_steps | Required | Minimum 6 steps |
| links.upward | Required | Minimum 2 upward links |
| links.sideways | Required | Minimum 1 sideways link |
| layout field | BANNED | Must not be present (causes Hugo to silently skip the page) |
| em dash | BANNED | Must not appear anywhere in frontmatter |

---

## SECTION 2 — CONTENT CHECKLIST

### Banned vocabulary scan
Search for each of these words in the full page content. Any match is an ERROR:

delve, meticulous, comprehensive, tailored, navigate, leverage, seamless, robust, vital, crucial, utilize, intricate, paramount, pivotal, embark, foster, elevate, unleash, unlock, harness, streamline, holistic, realm, testament, moreover, furthermore, groundbreaking, transformative, synergy, reimagine, bustling, nestled, nuanced, illuminate, encompasses, proactive, ubiquitous, quintessential

### Em dash scan
Search for: — (U+2014) and – (U+2013). Any match is an ERROR.

### Safety guarantee scan
Search for these patterns. Any match is an ERROR:
- "guarantee" within 5 words of "safety" or "safe"
- "100% safe"
- "risk-free"
- "completely safe"
- "ensure your loved one is safe"

### AI-pattern phrase scan
Search for these phrases. Any match is a WARNING:
- "plays a crucial role"
- "in the realm of"
- "it is worth noting"
- "serves as a testament"
- "at its core"
- "shed light on"
- "dive into"
- "first and foremost"

### Thin content check
Count the words in the body content (below the frontmatter). Fewer than 300 words is an ERROR. Fewer than 500 words is a WARNING.

### Price check
Search for: £, $, EUR, "cost", "price", "fee", "charge" followed by a number. Any match is an ERROR.

---

## SECTION 3 — SEO COMPLIANCE CHECKLIST

| Check | Rule | Pass condition |
|---|---|---|
| Title tag | Character count | 40-60 characters |
| Title tag | Keyword presence | Contains origin country name |
| Meta description | Character count | 120-155 characters |
| Meta description | CTA | Ends with "Contact us 24/7", "Call us now", "Send an enquiry", or similar |
| H1 | Presence | One H1 in template containing origin and destination |
| Schema | FAQ schema | faqs frontmatter generates FAQPage schema |
| Schema | Service schema | route template generates Service schema |
| Schema | BreadcrumbList | route template generates BreadcrumbList schema |
| Canonical | Presence | Canonical URL in page-meta block |
| Duplicate | Slug check | Slug does not already exist in site/content/routes/ |

---

## SECTION 4 — LINK INTEGRITY (route pages)

| Check | Rule |
|---|---|
| Upward link 1 | Points to /repatriation-from-[origin]/ |
| Upward link 2 | Points to a guide or embassy page for the origin country |
| Sideways link 1 | Points to a different route from the same origin |
| All URLs | Use lowercase, hyphens only, no underscores |
| All URLs | Begin with / (site-relative) |

---

## HOW TO REPORT

For each page audited, report in this format:

```
[PAGE] spain-to-united-kingdom
[PASS] Frontmatter complete
[PASS] Title: 52 chars, contains Spain + United Kingdom
[PASS] Description: 148 chars, ends with CTA
[PASS] 6 FAQs present
[PASS] 7 timeline steps present
[PASS] No banned vocabulary
[PASS] No em dashes
[PASS] No safety guarantees
[PASS] No prices
[PASS] Upward links: 2 present
[PASS] Sideways links: 2 present
[VERDICT] PASS — ready to commit
```

If any check fails:
```
[ERROR] Missing layout field — REMOVE the layout: line from frontmatter
[ERROR] Em dash found in description field
[WARNING] Only 4 FAQs (minimum 6)
[VERDICT] FAIL — fix errors before committing
```

---

## AUDIT RESULT CODES

- **PASS** — page is ready to commit
- **WARN** — page has warnings but may ship if Gareth approves
- **FAIL** — page must be fixed before commit. No exceptions.

---

## BATCH AUDIT SUMMARY FORMAT

After auditing a batch of pages:

```
BATCH QA SUMMARY — 27 May 2026
Pages audited: 25
PASS: 25
WARN: 0
FAIL: 0
Verdict: BATCH READY FOR COMMIT
```

---

*Last updated: 27 May 2026*
