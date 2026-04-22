# Tech Stack Recommendation — Funeral Repatriation Site

## Status
Task 0.9 (Gareth's strategic answers) is still PENDING. Some decisions here may shift depending on answers. Where a decision is blocked, defaults are provided that work for all likely scenarios.

---

## Recommended Stack

### Static Site Generator: Hugo

**Why Hugo:**
- **Scale:** Target is 2,000+ pages at full build (26 countries x multiple page types + city pages + guides + blog). Hugo builds 5,000 pages in under 10 seconds.
- **Data-driven templating:** Our build is JSON data files (countries_repatriation.json, cities_p1.json) piped through templates. Hugo's `range` over data files is built for this.
- **No client-side JavaScript needed:** Families searching for repatriation help don't need interactive features. Pure static HTML = fastest loads, best Core Web Vitals, highest trust signals.
- **i18n support:** Future expansion to multilingual content (Urdu for Pakistan diaspora, Arabic for Middle East, Hindi for India) is native in Hugo.

**Alternatives considered:**
- Astro: Good, but Node-based build is slower at 2,000+ pages. Better if we needed interactive components.
- 11ty: Close second. More flexible but slower at scale.
- Next.js (SSG mode): Overkill. No React needed. 10-50x slower builds.

### Hosting: Cloudflare Pages

**Why Cloudflare:**
- **Edge network:** Our visitors are UK-based families, but also diaspora communities worldwide (India, Philippines, Kenya, Morocco). Cloudflare has edge presence in all these locations.
- **Free tier:** Unlimited sites, unlimited bandwidth, 500 builds/month.
- **YMYL trust:** Fast page loads are a ranking factor. Cloudflare edge delivery means sub-second loads globally.
- **Security:** WAF, DDoS protection, bot management all in one dashboard. A funeral services site could attract scammers trying to inject phishing content.

**Alternatives:**
- Netlify: Better DX. Bandwidth cap matters at scale. Good fallback option.
- Vercel: Next.js-first. Wasted on Hugo.

### Contact Forms: Formspree or Cloudflare Worker

**YMYL sensitivity requirements:**
- Families contacting us are in extreme distress. Form must work perfectly, every time.
- No unnecessary data collection. Name, email, phone, country of death, brief message.
- GDPR compliant. No data stored longer than necessary.
- Confirmation email immediately so families know their message was received.

**Recommended approach:**
- **Phase 1:** Formspree (battle-tested, GDPR compliant, email notifications). Simple and reliable.
- **Phase 2:** Custom Cloudflare Worker that sends to email + logs to Supabase for CRM.
- NOTE: Unlike the security project, PGP encryption is not needed. Repatriation enquiries are not security-sensitive in the same way.

**Key form elements:**
- Name, email, phone number
- Country where death occurred (dropdown from our 26 countries)
- Urgency indicator (just happened / within last week / planning ahead)
- Free text message
- Immediate auto-response: "We have received your enquiry and will respond within [X hours]."

### Domain and DNS

**Blocked by 0.9/0.10.** Cannot select domain until brand name is decided.

**Recommendations regardless:**
- .co.uk preferred (UK-focused service, UK families are 90%+ of audience). Also register .com.
- Exact-match domain options to consider: repatriation.co.uk, funeralrepatriation.co.uk, bringhome.co.uk
- Register via Cloudflare Registrar (at-cost pricing, integrates with Pages).
- DNSSEC enabled. SSL via Cloudflare (automatic).

### CMS: None (Phase 1)

**Phase 1 (launch):**
- Content generated from JSON data + Hugo templates via build scripts.
- Blog and guide posts are Markdown files in /content/.
- No CMS overhead. The JSON data pipeline IS the CMS.

**Phase 2 (if non-technical editors needed):**
- Decap CMS (Git-based, no database, works with Hugo).
- Browser UI that commits to Git repo.

### Analytics: Plausible

- Privacy-first. No cookie banners. GDPR compliant by default.
- Lightweight (< 1KB script). No cookies.
- A funeral services site should NOT share visitor behaviour with Google Analytics. These are grieving families.
- Plausible self-hosted or $9/month hosted.

### Monitoring and Uptime

- **Google Search Console:** SEO monitoring. Mandatory.
- **Cloudflare Web Analytics:** Free, no JS required.
- **Better Uptime or UptimeRobot:** Downtime alerts. Site must be up 24/7 because deaths happen at any hour.

---

## Site Architecture (URL Structure)

```
/                                          # Homepage
/repatriation-from-spain/                  # Country repatriation page (x26)
/death-abroad/spain/                       # "What to do" guide (x26)
/death-in-phuket-thailand/                 # City-specific guide (x44 for P1)
/faq/repatriation-from-spain/             # Country FAQ page (x26)
/ashes-transport-from-spain/              # Ashes transport page (x26)
/compare/spain-vs-france/                 # Country comparison (selected pairs)
/services/                                # Our services overview
/services/repatriation/                   # Body repatriation service
/services/ashes-transport/                # Ashes transport service
/services/cremation-abroad/               # Cremation abroad coordination
/about/                                   # About us (E-E-A-T: expertise, experience)
/contact/                                 # Contact form
/emergency/                               # 24/7 emergency contact (prominent)
/blog/                                    # Blog index
/blog/{post-slug}/                        # Blog posts
/resources/                               # Guides and resources hub
/privacy/                                 # Privacy policy
/terms/                                   # Terms and conditions
```

## Page Count Estimates

| Page Type | Phase 1 (P1) | Phase 2 (P1+P2) | Full Build |
|-----------|--------------|------------------|------------|
| Country repatriation | 10 | 26 | 50+ |
| Death abroad guides | 10 | 26 | 50+ |
| City guides | 44 | 100+ | 200+ |
| Country FAQs | 10 | 26 | 50+ |
| Ashes transport | 10 | 26 | 50+ |
| Country comparisons | 10 | 30 | 50+ |
| Service pages | 5 | 5 | 10 |
| Core pages | 6 | 6 | 6 |
| Blog posts | 10 | 30 | 100+ |
| **Total** | **~115** | **~275** | **~566+** |

## Build Pipeline

```
JSON data files (countries, cities, keywords)
    |
    v
Hugo templates (country_repatriation.html, death_guide.html, city_guide.html, etc.)
    |
    v
Build script (generate.py or Hugo native)
    |
    v
Static HTML (Cloudflare Pages deploy)
    |
    v
Post-build: sitemap.xml, robots.txt, structured data validation
```

## YMYL-Specific Technical Requirements

1. **HTTPS everywhere.** No mixed content. Cloudflare handles this.
2. **Structured data (JSON-LD):** FAQPage, Service, BreadcrumbList, Organization. Every page.
3. **Author attribution:** Every content page has a named author with credentials. E-E-A-T signal.
4. **Source citations:** Inline citations linking to GOV.UK, FCO, embassy websites. Trust signals.
5. **Last updated date:** Every page shows when it was last reviewed. Stale YMYL content is penalised.
6. **Contact information visible:** Phone number and contact form accessible from every page. Trust signal.
7. **Fast loads:** < 1 second LCP target. Static HTML + Cloudflare edge achieves this.
8. **Mobile-first:** 70%+ of distressed family searches happen on phones.

---

## Decisions Pending (from Gareth, Task 0.9)

1. **Brand name** - Determines domain, all branding, business registration
2. **Business model** - Coordinator/broker vs. full-service provider. Affects service page content.
3. **Response time commitment** - "Within 24 hours" or "Within 2 hours"? Affects CTA copy.
4. **Phone line** - Will there be a 24/7 phone number? Affects contact page and trust signals.
5. **Author persona** - Real name or brand persona for E-E-A-T bylines?
6. **Insurance partnerships** - Will we work with travel insurance companies? Affects whole content strategy.
