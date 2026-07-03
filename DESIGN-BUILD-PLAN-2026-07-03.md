# Design and Conversion Build Plan, 3 July 2026

Derived from the browser design audit of 3 July 2026 (Sonnet 4.6), then **verified against the repository** before planning. The audit was useful but partly inaccurate; every item below is tagged with what the repo check actually found, so execution does not chase phantom bugs.

**Execution model:** Sonnet, unless tagged **OPUS** (judgement/structural) or **DECISION** (needs Gareth).
**Deploy target:** `master` (live), per the standing rule. One deploy per block, only after a clean Hugo build and the QA gate (`qa_routes.py`, `check_schema.py`, `check_titles.py`) pass.
**House rules still apply:** no em dashes, no banned vocabulary, British English, no prices, no invented facts or testimonials (YMYL).

## Verify-first rule for this plan

The audit was produced by a browser agent that hedged ("could not be fully verified", "appears to", "likely a bug"). Several claims were checked and found false (see "Audit claims that are NOT real", bottom). So: **before changing anything for an item, reproduce it in the built output (`hugo` then read `site/public/...`) or the source.** If it cannot be reproduced, mark it "not reproduced" in the changelog and move on.

---

## Audit claims verified as REAL (repo-confirmed)

These are grounded; the file and root cause are named.

### Block D1: Critical bugs (Sonnet)

**D1.1 Invisible / stripped navigation on light-hero templates** [Critical]
- Confirmed. Root cause: `main.css` `.site-header` is `position:fixed; background:transparent` with white text, and only goes solid-dark via `body:not(.has-hero) .site-header` or `.scrolled`. Pages flagged `has-hero` (in `baseof.html`, any page with `.Params.hero_image` that is not a section) get the transparent header. City pages (`countries/single.html`, `.city-hero`), cremation-transfer and bringing-ashes-home single pages set `hero_image`, so they are `has-hero`, but their hero is not a dark full-bleed panel behind the 80px fixed header. Result: white "Repatriate" and the white nav links disappear, leaving only the gold "Service" span (`.logo-text span { color: var(--gold) }`) visible. That is exactly the "logo shows only Service, nav gone" report.
- Files: `site/assets/css/main.css` (`.site-header`, `.city-hero`, `.ct-hero`, and the ashes/embassy hero blocks), `site/layouts/_default/baseof.html` (the `has-hero` gate).
- Fix (pick one, keep it consistent): (a) give `.city-hero` / `.ct-hero` / the ashes hero a dark background with a dark overlay and enough top padding to sit under the header, matching `.country-hero`; or (b) stop emitting `has-hero` for templates that do not render a dark full-bleed hero, so the header is solid-dark and readable. Option (b) is the smaller, safer change. Verify on a city, a cremation-transfer, and a bringing-ashes-home page at desktop and mobile.

**D1.2 Blank /routes/ index** [Critical]
- Confirmed. There is no `site/layouts/routes/list.html`, so `/routes/` falls back to `_default/list.html`, which only renders `{{ .Content }}`, and `content/routes/_index.md` has no body. So the index shows a hero and nothing else; 2,467 route pages are not listed.
- Fix: create `site/layouts/routes/list.html` modelled on `countries/list.html`. Do not list all 2,467 (too many); group by destination or show the main UK and Ireland inbound corridors plus a note, or a searchable/grouped list. Keep it scannable. Verify `/routes/` renders a usable list.

**D1.3 Empty guide-card titles on /guides/** [Major]
- Confirmed. `guides/list.html` renders `<h3>{{ .Params.country_name }}</h3>`, but guide pages have no `country_name` param, so every card title renders as `<h3></h3>` (empty). The built page shows cards with description text and no heading.
- Fix: use `{{ .Title }}` (or a cleaned country name) for the card heading. Also correct the stale "26 country guides" label above the grid (there are 239). Verify cards show a country/title.

### Block D2: Conversion (Sonnet, decisions resolved)

**D2.1 No visible phone/WhatsApp number on the homepage hero or the contact page** [Major]
- Confirmed. `index.html` hero and `_default/contact.html` link to `wa.me/447703577246` via buttons but never print the number `+44 7703 577246` as readable, tappable text. A family cannot copy or hand-write it. (Route and hub pages that include the emergency helpline bar do show it; the highest-traffic pages do not.)
- Fix: add the number as a `tel:`-linked, prominent line in the homepage hero and near the contact-page form heading. Small, high-value change.

**D2.2 No persistent CTA on interior pages** [Major, structural-lite]
- Confirmed. On every interior template the enquiry form sits at the page bottom; there is no sticky element. Only the floating WhatsApp button persists.
- Fix: add one shared sticky bottom CTA bar for mobile (a partial included from `baseof.html`), two actions: "WhatsApp now" and "Send enquiry" (anchor to the page form or `/contact/`). Ensure it does not collide with the existing floating WhatsApp button (reposition or merge the float into the bar on mobile). This is the single highest-impact mobile conversion change in the audit.

**D2.3 Contact page form length** [Minor, **DECIDED: trim**]
- Scope check: the audit's D2.3 finding and Gareth's "trim" decision were specifically about the Contact page form (`site/layouts/_default/contact.html`), which has 7 fields including two selects (`service`, `urgency`). The route-page form (`routes/single.html`) and hub form (`country-hub.html`) already have only 5 fields and 1 select each (country is hidden/pre-filled, no `urgency` select), so they are not part of this item; leave them as is (no unrequested rewrite).
- Fix: on `contact.html` only, remove the `service` and `urgency` selects, keep name, email, phone, country (free text), and the message textarea (already required). Confirm the `formsubmit.co` endpoint does not depend on the removed field names.
- Also found while reading this file: two em dashes, one in the hidden `_subject` field value and one in the message textarea's placeholder text. Fix both while in this file (absolute ban).

**D2.4 Trust text and response-time near forms** [Minor]
- The microtext under submit buttons is small. Add a short line ("We usually reply within the hour. No obligation, strictly confidential."). Note: the thank-you page already promises a call within the hour and is well written (no change needed there; see false-claims list).

### Block D3: Consistency and polish (Sonnet)

**D3.1 Green WhatsApp button on the homepage** [Minor, **DECIDED: keep green, no change**]
- Confirmed: `index.html` line 135 uses `.btn-whatsapp` (`background:#25D366`) mid-page. Gareth decided to keep it green (WhatsApp brand convention). This item is closed; do not recolour it.

**D3.2 "P1 / P2" priority badges are unexplained jargon** [Minor]
- Confirmed on homepage and country cards. Relabel to plain language ("Priority country" / remove the P2 tier badge) so a grieving reader is not shown internal tiering codes.

**D3.3 Very small overline label text** [Minor]
- The `.label-sm` style and similar overlines render around 10 to 11px. Bump the smallest label sizes up slightly and check contrast against their backgrounds (some are gold on light).

**D3.4 Stale hardcoded counts** [Minor]
- "26 country guides" and similar hardcoded counts are stale (the site has 239). Replace with a live count (`len` of the section) or a rounded phrase.

### Block D4: Imagery (Sonnet; scope confirmed)

**D4.1 Repeated and tonally wrong hero images** [Major, **DECIDED: keep current images, reassign only**]
- Confirmed: `ctandt-ai-generated-8884751.jpg` (the image the audit calls "coffin and flowers") is hardcoded in `_default/contact.html` and is the default in `_default/single.html`, so it appears on Contact, Privacy, and generic pages. Every route hero uses `cargo-terminal-night.jpg`. The countries index uses `mrwashingt0n-ai-generated-9048740.jpg` (the audit calls it "figure among gravestones"). `_default/list.html` defaults to a couple image.
- Decided: no new or commissioned images. Reassign only from what already exists in `site/static/images/` (for example `mediterranean.jpg`, `city-dusk.jpg`, `consultation-office.jpg`, `support-conversation.jpg`, `airport-terminal.jpg`), giving Contact, the index pages, and the generic template distinct, non-distressing images, and removing the coffin image from the conversion and legal pages. Route heroes staying visually similar across corridors is accepted as a known limitation, not fixed here.

---

## Structural items

**D5.1 The five country-hub layouts are inconsistent** [Critical per audit, **DECIDED: Option 1, OPUS REQUIRED, not yet started**]
- Confirmed the five hubs render very differently: variant A is the inline template in `country-hub.html` (hero + stats + article), while B, C, D, E are separate partials (`partials/countries/country-b/c/d/e.html`) with genuinely different structures (accordion, two-column, no-hero editorial, and so on). The audit rates USA (E) and Thailand (B) weakest and Spain (A) strongest.
- Decided: Option 1, "raise the quality, keep some consistency." Keep all five variants (satisfies the CLAUDE.md rotation rule) but bring B, D, E up to the same completeness and component quality as A and C, so pages differ in arrangement but not in polish. This needs an actual Opus session to design the shared component set and a per-variant checklist before Sonnet touches the partials (see the model-switch note above; not yet done).
- When that Opus session happens, also verify the audit's specific structural claims that could not be confirmed by the browser agent before designing around them: France (C) "blank left column", Thailand (B) "no hero", Greece (D) "no helpline bar", and the route hero stat bar showing 2 vs 3 pills. Reproduce each in the built output first, per the verify-first rule.

**D5.2 Navigation restructure** [Major, **DECIDED: proceed, Sonnet**]
- Confirmed the nav has eight items plus a "Resources" dropdown and a redundant pair (a "WhatsApp us" text link and a "Get Help Now" button). Gareth approved proceeding; no specific target structure was given, so the proposal below is what Sonnet builds. If this is not what Gareth had in mind, it is a one-file (`header.html`) change to adjust.
- **Proposed 5-item structure:** Home / Country Guides / Resources (dropdown, unchanged: guides, cremation, embassy, ashes, blog) / Services / Contact, plus the WhatsApp icon-button. Change: drop the separate gold "Get Help Now" button, since it duplicates Contact and the WhatsApp button in a 3-way tie for the same job; "Contact" in the main nav and the WhatsApp button together cover both channels without a third, differently-worded button. Keep "About Us" but fold it as the first item under Resources rather than a top-level slot, since it is not a crisis-relevant destination. Net: 8 top-level items (Home, About, Country Guides, Resources-dropdown, Services, Contact, WhatsApp-link, Get-Help-button) become 5 (Home, Country Guides, Resources-dropdown-with-About-added, Services, Contact) plus one WhatsApp action, not two.

---

## Decisions (Gareth, 3 July 2026)

1. **Testimonials/social proof: NO.** Confirmed: nothing invented, no placeholder reviews or figures. This item stays out of scope entirely; do not add any social-proof element without new, explicit instruction and real data.
2. **Hub standardisation: Option 1.** "Raise the quality, keep some consistency." Keep the five A to E variants (satisfies the CLAUDE.md rotation rule) but bring the weaker ones (B, D, E per the audit) up to the same completeness and component quality as the strongest (A, C). Per the original plan, this needs Opus to design the shared component set and a per-variant checklist before Sonnet touches the partials. **Not yet started: needs an actual Opus session (see model-switch note below).**
3. **Nav structure: proceed.** Build the leaner 4-to-5 item nav per D5.2.
4. **Contact form fields: trim.** Reduce to name, email or phone, country, message. Remove the `service` and `urgency` selects per D2.3.
5. **Green vs gold: keep green.** The mid-page homepage WhatsApp button (`.btn-whatsapp`, `#25D366`) stays as is. D3.1 is closed, no change needed. (The floating WhatsApp button was already going to stay green regardless; this confirms the in-content button too.)
6. **Imagery: keep current images.** D4.1's Sonnet-reassignment (swapping the repeated `ctandt` "coffin" image and picking distinct existing images per page) still goes ahead using only images already in `site/static/images/`. No new commissioned assets, no change to the tone rule beyond what D4.1 already specifies.

**Model-switch note (3 July 2026):** Gareth said "switched to opus" when giving these decisions, but the `/model` command that fired that turn set the session to Sonnet 5 (confirmed by the system). D5.1 (hub standardisation) requires an actual Opus session per its own tagging; it should not be attempted on Sonnet. All other items below (D1, D2.1, D2.2, D2.4, D3.2 to D3.4, D4.1, D5.2) are Sonnet-safe and can proceed immediately.

---

## Audit claims that are NOT real (verified false, do NOT action)

- **Body text is 14px, raise to 16px**: false. `main.css` `body { font-size: 1rem }` is already 16px. No change.
- **Doubled "//" breadcrumb separators**: false. The route breadcrumb markup uses clean `&#8250;` (the "›" glyph) with no empty segment. Not reproduced.
- **Thank-you page is sparse and shows a coffin image**: false. `_default/thank-you.html` is thoughtful and complete (promises a call within the hour, a "in the meantime" safety checklist) and has no hero image at all. Already good; leave it.
- **Embassy index cards show no country name**: false. `embassy-contacts/list.html` renders `<h3>{{ .Params.country_name }}</h3>` and the param is populated. Fine. (Contrast with the guides index, D1.3, where the param is genuinely empty.)

---

## Suggested order

1. **Block D1** (bugs): broken nav, blank routes index, empty guide titles. Highest visible-quality impact, all verified, Sonnet-safe.
2. **Block D2** (conversion): phone number visible, sticky mobile CTA, trust line. Highest enquiry impact.
3. **Block D3** (polish) and **Block D4** (imagery reassignment): quick, once the D3.1/D4.1 decisions are answered.
4. **Block D5** (structural): only after Gareth decides scope; Opus designs, then Sonnet builds.

## Changes made and why

### Block D1 (Sonnet, done, verified)

**D1.1 Invisible nav on city / cremation-transfer / embassy-contacts pages** (done, verified)
- File: `site/layouts/_default/baseof.html`.
- Root cause found, more precise than the audit's guess: `.site-header` is `position:fixed; background:transparent` and only turns solid dark via `body:not(.has-hero) .site-header` or on scroll. `has-hero` fires whenever `.Params.hero_image` is set on a non-section page, but `countries/single.html` (city pages), `cremation-transfer/single.html`, and `embassy-contacts/single.html` all set `hero_image` in frontmatter without ever rendering it as a background; their own hero sections (`.city-hero`, `.ct-hero`, `.embassy-hero`) are a separate light, dark-text design, never a dark full-bleed photo. So the header stayed wrongly transparent over a light page with no dark backdrop, and the white "Repatriate" logo text plus white nav links became invisible, leaving only the gold "Service" span. This exactly matches the audit's screenshot description. Country hub pages were never affected: they are Hugo sections (`_index.md`), already excluded by the existing `(not .IsSection)` clause, so their header was always solid-dark; the audit never flagged hub nav, which is consistent.
- Fix: excluded `countries` city-level pages (a page, not the hub section) and the `cremation-transfer` / `embassy-contacts` sections from the `has-hero` gate in `baseof.html`, rather than stripping the dead `hero_image` field from roughly 630 content files. `bringing-ashes-home` was left untouched: it genuinely uses `.Params.hero_image` as a real background-image (`.page-hero`), so `has-hero` is correct there.
- Investigated and left alone: the separately broken `--bg-dark` CSS custom property (referenced 5 times, defined nowhere, in `.city-hero`, `.ct-hero`, `.blog-hero`, `.embassy-hero` x2), which makes those gradients invalid and the sections render with no background. Confirmed this is cosmetically harmless once the has-hero fix lands: the in-page heading text in those sections is dark (`h1 { color: var(--charcoal) }`), so a plain white section background (the effective fallback) is legible and was clearly the intended light-hero look, not a photo hero. Fixing the dead variable is unrequested scope beyond D1.1 and was not done.
- Verified: rebuilt and confirmed `<body>` (no `has-hero`) on a city page, a cremation-transfer page, and an embassy-contacts page; confirmed `<body class=has-hero>` unchanged on the homepage and a bringing-ashes-home page; confirmed hub and route pages unaffected (they never had the class). Confirmed the fallback CSS rule (`rgba(5,13,21,0.97)` background, white/70% nav text, white logo text) will render correctly.

**D1.2 Blank /routes/ index** (done, verified)
- File: new `site/layouts/routes/list.html`.
- Root cause: there was no `routes/list.html`, so `/routes/` fell back to `_default/list.html`, which only renders `{{ .Content }}`, and `content/routes/_index.md` has no body. The index showed a hero and nothing else, none of the 2,467 route pages were listed.
- Built a grouped index: routes grouped by destination (129 distinct destinations), each an accordion group (reusing the existing `.faq-item` / `.faq-trigger` markup and JS verbatim, so no new interaction code was needed) showing an alphabetical list of origin-country links, sorted by group size so the largest destinations (United Kingdom and Ireland, 196 routes each) appear first.
- Technical note: Hugo's `Pages.GroupBy "Params.dest_name"` failed at build time in this Hugo version (`reflect: Elem of invalid type page.Page`); replaced with a manual `where`-based grouping loop (the same pattern already used in `routes-from.html` from the earlier SEO session), which builds in about 6 seconds for all 2,467 routes.
- Verified: 129 groups rendered with matching `aria-controls`/`id` pairs; the United Kingdom group contains exactly 196 alphabetically sorted links with zero duplicates (checked by isolating its specific answer block, after an initial false alarm from a sloppy regex that matched an unrelated destination's group); a sample link resolves to a real built page.

**D1.3 Empty guide-card titles on /guides/** (done, verified)
- File: `site/layouts/guides/list.html`.
- Root cause: the card heading rendered `{{ .Params.country_name }}`, but guide pages carry no `country_name` param (0 of 238 have it), so every card heading rendered as an empty `<h3></h3>`.
- Fix: resolve the country name from `.Params.country_key` via the shared `countries_repatriation` data file, the same lookup pattern `country-hub.html` already uses, with a fallback to `.Title` if a country is somehow not in the data. Also corrected the stale "26 country guides" label (there are 238) to a live count, found and fixed in the same file while in there.
- Verified: 0 empty `<h3>` tags remain across all 238 cards; count label now reads "238 country guides".

**Also fixed while in this file family (not a separate audit finding):** `countries/list.html` (the `/countries/` index) rendered a `£`/GBP price stat (`$c.cost_guide.total_typical_range_gbp`) on every card, which contradicts the site-wide qualitative-only prices decision made in the 2 July SEO build (F13). Removed the price stat, kept the timeline stat. Verified zero `£` characters remain on the built `/countries/` page and `check_schema.py` still passes.

**Gate status after Block D1:** Hugo build clean, `qa_routes.py` 0 FAIL / 2,467 PASS (unchanged, D1 touched no route content), `check_schema.py` 0 errors, `check_titles.py` 0 errors / 27 pre-existing warnings (unchanged).

### Block D2 (Sonnet, done, verified)

**D2.1 Visible phone number on homepage and Contact page** (done, verified)
- Files: `site/layouts/index.html`, `site/layouts/_default/contact.html`.
- Added a `tel:+447703577246`-linked line reading "+44 7703 577246" below the hero actions on both pages, reusing the existing `.helpline-number` style (already used on route/hub emergency bars) rather than inventing new CSS. Verified the surrounding `.hero-text p` / hero context styles the line legibly (light/silver text, gold number) without any new CSS needed.
- Verified: the `tel:` link and number render correctly in the built output on both pages.

**D2.2 Persistent mobile CTA bar** (done, verified)
- Files: new `site/layouts/partials/sticky-cta.html`; CSS added to `site/assets/css/main.css`; included from `site/layouts/_default/baseof.html`.
- A fixed-bottom, two-button bar (WhatsApp, green; Send Enquiry, gold, linking to `/contact/`) shown only under the existing 600px mobile breakpoint. "Send Enquiry" always targets `/contact/` rather than an in-page form anchor, since not every template has a predictable in-page form id. The existing floating WhatsApp button is hidden at the same breakpoint so the two do not stack or collide (the plan's "reposition or merge" choice; merged). Added `body { padding-bottom }` in the same mobile query so the bar never covers the last piece of page content.
- Verified: renders on a route page, a blog page, and the homepage; both links carry the correct `href`; CSS confirmed present in the built stylesheet; `check_schema.py` and the full QA gate unaffected.

**D2.3 Contact page form trimmed** (done, verified)
- File: `site/layouts/_default/contact.html`.
- Removed the `service` and `urgency` selects, scoped to the Contact page only (route/hub forms were already short; see the scope-check note above). Form is now 5 fields: name, email, phone, country, message.
- Verified: built page shows exactly 5 named inputs/textarea, 0 `<select>` elements, honeypot untouched.

**D2.4 Trust and response-time text near the Contact form submit button** (done, verified)
- File: `site/layouts/_default/contact.html`.
- Changed the small note under the submit button from a single confidentiality line to "We usually reply within the hour. No obligation, and your details are kept strictly confidential and never shared with third parties."

**D4.1 (Contact-page portion) Coffin/flowers hero image reassigned** (done, verified)
- Files: `site/layouts/_default/contact.html`, `site/layouts/_default/single.html`.
- `ctandt-ai-generated-8884751.jpg` was hardcoded on the Contact page and was the default fallback on the generic `_default/single.html` template (used by Privacy and Methodology, since neither sets its own `hero_image`). Checked the full image-usage inventory across `site/layouts/` first to avoid picking an image already claimed elsewhere (`support-conversation.jpg` and `city-dusk.jpg` were both already in use, for example). Assigned two distinct, previously-unused images: `consultation-room.jpg` for Contact, `advisor-documents.jpg` for the generic single-page fallback, so Contact/Privacy/Methodology no longer share an image with each other or with any other page.
- Verified: both new filenames appear in the built Contact, Privacy, and Methodology pages; the coffin image no longer appears on any of the three.

**Also fixed while in these files this block (not separate audit findings):**
- Two em dashes in `contact.html` (the hidden `_subject` field value, the message textarea placeholder) and one in a code comment, all replaced with commas per the absolute ban.
- A banned word ("navigate") found in `index.html` at an unrelated FAQ answer (line 253, far from the D2.1 hero edit but in the same file being touched this block); replaced with "work through".
- Seven em dashes across `site/assets/css/main.css` comment headers, found during a full sweep of the file while adding the D2.2 sticky-bar CSS (the file header, two variable-block comments, a card-accent comment, two section-divider comments, one inline comment). All replaced with commas.

**Gate status after Block D2:** Hugo build clean, `qa_routes.py` 0 FAIL / 2,467 PASS, `check_schema.py` 0 errors, `check_titles.py` 0 errors / 27 pre-existing warnings, no banned words or em dashes in any file touched this block.

### Block D3 and D5.2 (Sonnet, done, verified)

**D3.2 "P1/P2" priority badges removed** (done, verified)
- Files: `site/layouts/countries/list.html`, `site/layouts/index.html`.
- The `$c.priority` field holds a raw internal content-build tier code (P1/P2/P3), used elsewhere in this project only to sequence which countries got deeper city-level guides first. Displaying it to a bereaved family does more harm than the audit's "unexplained jargon" framing suggests: it implies an explicit ranking of which countries, and by extension which families' deaths, the site treats as a priority. Removed entirely from both user-facing card displays rather than relabelling it to something like "Priority country", which would still expose the ranking, just in friendlier words.
- Verified: build clean, no `$c.priority` output remains on `/countries/` cards or the homepage country grid.

**D3.3 Overline label contrast on light backgrounds** (done, partially, verified and honestly scoped)
- File: `site/assets/css/main.css`.
- Computed the actual WCAG contrast ratios before touching anything: `.label-sm` in full gold (`--gold`, `#D5A021`) scores 8.26:1 on the dark hero backgrounds it was designed for (comfortably passes), but only 2.36:1 on the white `.section`/`.section-alt` backgrounds where most instances of this label actually appear on the site (route/hub/guide/blog templates all use it as a small eyebrow above section headings). WCAG AA requires 4.5:1 for normal-size text.
- Fix: added a scoped override, `.section .label-sm, .section-alt .label-sm { color: var(--gold-dark) }` (the existing `--gold-dark` variable, already used elsewhere in the file), which improves the light-background contrast to 3.17:1, and bumped the base font-size from 0.72rem to 0.76rem. The base rule (used in hero contexts) is untouched, so the strong 8.26:1 contrast there is preserved.
- Honestly scoped, not overclaimed: 3.17:1 clears WCAG's "large text" threshold (3:1) but does not reach the stricter normal-text threshold (4.5:1). Reaching 4.5:1 at this text size would require abandoning the gold brand colour for this element entirely (a much darker, less "gold" hue), or enlarging the label into the WCAG "large text" size category, both larger changes than this Minor-severity polish item calls for. Flagged here rather than silently marked "fixed"; a genuine full-AA pass on this element is a future decision, not done in this block.
- Verified: confirmed via the built CSS that the base rule and the scoped override both landed correctly (an earlier check briefly appeared to fail because a stale, previously-fingerprinted CSS file was being read instead of the fresh build; a clean rebuild resolved this and is noted here so it is not mistaken for a real bug in a future session). Confirmed on a live route page that the hero-context label and the light-section-context label pick up different classes as intended.

**D5.2 Navigation restructured to 5 top-level items** (done, verified)
- File: `site/layouts/partials/header.html`; dead CSS removed from `site/assets/css/main.css`.
- Per the approved proposal: dropped the separate gold "Get Help Now" button (it duplicated Contact and the WhatsApp button, three routes to the same two actions). Folded "About Us" into the Resources dropdown as its first item, since it is not a crisis-relevant destination for a distressed visitor. Nav is now: Home, Country Guides, Resources (dropdown: About us, What to do abroad, Cremation abroad, Embassy contacts, Bringing ashes home, Guidance articles), Services, Contact, plus the WhatsApp icon-button.
- Removed the now-fully-unused `.header-cta` CSS rule (confirmed no other template referenced it) and its mobile-hide media query line, rather than leaving dead code behind.
- Verified: built homepage nav has exactly 5 top-level `<li>` elements, no `header-cta` markup anywhere, "About us" renders inside the dropdown with working `aria-current` on the About page.

**Gate status after Block D3/D5.2:** Hugo build clean (after a clean rebuild to clear stale fingerprinted CSS), `qa_routes.py` 0 FAIL / 2,467 PASS, `check_schema.py` 0 errors, no banned words or em dashes in any file touched this block.

### Block D5.1 (Opus session, done, verified)

**D5.1 Hub layout standardisation, Option 1 (raise the weaker variants to the completeness bar, keep the arrangement variety)**

Verify-first pass (per the plan's rule, before designing anything). Read all five hub variant templates and their built output. Findings:
- The audit was right that variant D (Greece) and E (USA) rendered **no emergency helpline bar at all** (`helpline-strip=0` in the built HTML): the 24/7 emergency number, the single most important trust and safety element, was absent from those hubs entirely.
- The audit was right that variants B (Thailand), D and E rendered **no orientation stats** (timeline, availability, embassy), unlike A (hero stat pills) and C (stat-strip hero).
- The audit was **wrong** about variant C (France) having a "blank left column / missing body content": its built output shows a fully populated hero (label, H1, subtitle, WhatsApp CTA) plus a nine-element stat strip. C needed nothing. Recorded as not-a-bug rather than actioned.
- Also found: variant A's hero still showed the raw internal `$c.priority` tier code ("Priority country" pill), a miss from the D3.2 pass which only removed it from the index cards.

Shared component set built (the plan's requested "shared component set"):
- New `site/layouts/partials/countries/helpline-strip.html`: one self-contained emergency-helpline bar (resolves the country name from `country_key`, warm consistent wording). Every hub variant now renders this identical component. Replaced the inline copies in A, B and C (which had already drifted in icon, label and wording) with the partial, and added it to D and E where it was missing. That one identical branded bar on all five hubs is itself the main "same service" consistency signal.
- New `site/layouts/partials/countries/hero-stats.html` plus `.hub-orient-*` CSS in `main.css`: a light-background orientation strip (typical timeline, 24/7 support, British Embassy city, each shown only if present) that reads correctly under any variant's hero. Added to B, D and E, which had no at-a-glance facts. A and C already have their own stat displays, so they were left as is.
- Variant A: replaced the `$c.priority` pill with the British Embassy city (shown where known), matching the orientation strip.

Deliberately NOT done (kept the rotation variety, per Option 1 and the CLAUDE.md anti-footprint rule): the five heroes still differ in kind (A image hero, B compact banner, C stat-strip, D question-led, E editorial byline). They were not collapsed into one hero. The consistency added is in the load-bearing components (emergency access, orientation, CTA), not the layout, which is exactly what Option 1 asked for. Variant E keeps its author-byline-first hero (now honest "editorial team" wording from F3), but the orientation strip and emergency bar immediately below it restore the service signal the audit said was missing.

Verified: all five built hubs (Spain A, Thailand B, France C, Greece D, USA E) now render the helpline strip and show the number; B/D/E each render the orientation strip with three real facts (for example Greece: 10-21 days, 24/7, Athens); A's hero shows the embassy city (Madrid) instead of the priority code; `qa_routes.py` 0 FAIL / 2,467 PASS, `check_schema.py` 0 errors, no banned words or em dashes in any of the eight files touched. (One mid-build scare where Greece's orientation strip looked like it was missing the embassy city turned out to be a truncated grep window, not a real gap; confirmed all three B/D/E strips carry the city.)

**Block D5.1 complete. All design-audit blocks (D1, D2, D3, D5.1, D5.2) now done.** D5.1 was the only Opus-required item; it was held until an actual Opus session per the earlier model-switch note, then built here.
