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
- Also found while reading this file: two em dashes (`Repatriation enquiry — Repatriate Service` in the hidden `_subject` field; `country, circumstances, timeline — will help us respond` in the message placeholder). Fix both while in this file (absolute ban).

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

_No design changes built yet. Entries appended per item as they are executed, with file, what, and why, matching the SEO build plan's changelog style._
