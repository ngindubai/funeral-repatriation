# Repatriate Service — Design Plan

> The design system already exists in [`site/assets/css/main.css`](site/assets/css/main.css) and the partials under [`site/layouts/`](site/layouts/). This document is the **rulebook**: it freezes the tokens and components, defines the aesthetic, and sets a hard reuse rule.
> Every new page reuses these exact tokens and components. No one-off styles. No new colours. No new fonts.

---

## 1. Aesthetic direction

UK funeral repatriation is a **YMYL** (Your Money or Your Life) category. Visitors are bereaved or panicked. The site must look:

| Should feel | Should NOT feel |
|---|---|
| Dignified, calm, certain | Cheerful, casual, salesy |
| Authoritative, like a senior consultant | Clinical, corporate, military |
| Quiet luxury — dark navy + restrained gold | Neon, bright, gradient-heavy |
| Editorial: serif headings, generous line-height | Tech-startup: rounded everything, big primaries |
| Data-led and source-cited | Decorative |

Reference: Virtuary template adaptation. Conservative with colour. Type does the work, not effects.

## 2. Colour tokens (frozen)

Defined in `:root` of [`site/assets/css/main.css`](site/assets/css/main.css). **Use the CSS variable, never the hex literal, in any new rule.**

### Core palette

| Variable | Hex | Role |
|---|---|---|
| `--charcoal` | `#050D15` | Primary text, dark backgrounds, navy hero |
| `--charcoal-light` | `#08131E` | Slight elevation on dark surfaces |
| `--slate` | `#16222E` | Dark cards, footer |
| `--gold` | `#D5A021` | Single accent — links, CTA, highlights |
| `--gold-light` | `#E0B64A` | Hover lift, soft accents |
| `--gold-dark` | `#B8891A` | Active state, link hover |
| `--gold-muted` | `#C4A44E` | Borders, muted accent backgrounds |

### Neutrals

| Variable | Hex | Role |
|---|---|---|
| `--warm-white` | `#F8F6F3` | Page background alternative |
| `--cream` | `#F5F2ED` | Section bands, card backgrounds |
| `--light` | `#E9E9E9` | Borders |
| `--silver` | `#BFBDBD` | Disabled, very muted text |
| `--muted` | `#7A7A7A` | Body copy default |
| `--steel` | `#5A5856` | Secondary text on light |
| `--white` | `#FFFFFF` | Default body background |

### Functional

| Variable | Hex | Role |
|---|---|---|
| `--error` | `#c44f4f` | Form errors, warnings |
| `--success` | `#4a7c6f` | Form success, confirmation |

### Legacy aliases (do not introduce new ones)

`--sage`, `--sage-*`, `--accent`, `--blue-mid`, `--text-*`, `--bg-*`, `--border*` are mapped to the core palette for template compatibility. Use the **core** names in new code.

**Rule:** Never add a new colour variable. If a new shade is needed, justify it in [`MEMORY.md`](MEMORY.md), then add it to `:root` first.

## 3. Typography

Loaded from Google Fonts in [`site/layouts/_default/baseof.html`](site/layouts/_default/baseof.html):

```
Cinzel:wght@500;600
Inter:wght@300;400;500;600;700
Playfair Display:wght@500;600;700
```

| Use | Family | Weight | Notes |
|---|---|---|---|
| Headings `h1`–`h4` | **Playfair Display**, Georgia, serif | 500 / 600 / 700 | `letter-spacing: -0.01em`, `line-height: 1.25` |
| Body, UI, forms | **Inter**, system stack | 300 default, 400 / 500 / 600 / 700 | `line-height: 1.7`, `color: var(--muted)` |
| Small caps labels (`.label-sm`) | **Cinzel**, serif | 500 | `font-size: 0.72rem`, `text-transform: uppercase`, `letter-spacing: 0.15em` |

### Fluid scale (already defined)

| Element | `clamp()` |
|---|---|
| `h1` | `clamp(1.75rem, 4vw, 2.75rem)` |
| `h2` | `clamp(1.35rem, 3vw, 2rem)` |
| `h3` | `clamp(1.05rem, 2vw, 1.35rem)` |
| Body | `1rem` |

**Rule:** Never introduce a new font family. Never override `font-family` inline.

## 4. Spacing, radius, shadow scales

| Token | Value |
|---|---|
| `--radius-sm` | `4px` |
| `--radius` | `6px` |
| `--radius-lg` | `8px` |
| `--shadow-sm` | `0 2px 8px rgba(5,13,21,0.08)` |
| `--shadow-md` | `0 4px 20px rgba(5,13,21,0.12)` |
| `--shadow-lg` | `0 8px 40px rgba(5,13,21,0.18)` |
| `--shadow-glass` | `0 8px 32px rgba(0,0,0,0.2)` (dark hero overlays) |
| `--transition` | `0.3s ease` |

Spacing is **rem-based with consistent rhythm**. Standard section padding `padding: 4rem 0`, container `max-width: 1200px; margin: 0 auto; padding: 0 1.5rem`. Inspect existing partials before inventing new spacing values.

## 5. Reusable components (frozen — reuse, do not redesign)

| Component | Location | Notes |
|---|---|---|
| Header / nav | [`site/layouts/partials/header.html`](site/layouts/partials/header.html) | Transparent over hero, solid on scroll. Resources dropdown. WhatsApp link only — no phone. |
| Footer | [`site/layouts/partials/footer.html`](site/layouts/partials/footer.html) | Dark slate, gold accent links, WhatsApp + /contact CTA |
| Floating WhatsApp button | injected in `baseof.html` | `+447703577246`. Never remove or duplicate. |
| Hero (homepage + section heroes) | `home.html` / `list.html` blocks | Dark navy bg, Playfair H1, gold sub-rule, single primary CTA |
| Country hub variant A–E | [`site/layouts/partials/countries/country-{a,b,c,d,e}.html`](site/layouts/partials/countries/) | Picked by `template_variant` frontmatter. Do NOT modify A–E to converge; diversification is the point. |
| Country card | within country list | Image card with country name + estimated timeline. Never displays cost. |
| Rate / fact comparison block | within country single | Two-column or definition list. Cream band background. Source citation under each row. |
| Quote / contact form | [`site/layouts/_default/contact.html`](site/layouts/_default/contact.html) | Posts to `quoteFormEndpoint` (formsubmit.co). WhatsApp fallback under the submit. |
| FAQ accordion | per FAQ template | Detail/summary with chevron. JSON-LD FAQPage emitted server-side from same data. |
| CTA block (mid-page) | reused across silos | Dark slate background, gold border-left, "WhatsApp now" + "Request quote" — never a phone number. |
| Breadcrumb | section single templates | Schema BreadcrumbList included. |
| Direct-answer block | country hubs + key FAQ/blog | Renders `short_answer`, `direct_answer_heading`, `direct_answer_intro`, `direct_answer_points`, `direct_answer_note` — for LLM citation visibility. |

**Rule:** If a new component is needed, propose it first in [`MEMORY.md`](MEMORY.md) and add it as a reusable partial. Never inline a one-off.

## 6. Responsive behaviour

Mobile-first. Test at:

| Breakpoint | Width | Purpose |
|---|---|---|
| Mobile | 360 px | Floor target (small Android) |
| Mobile L | 414 px | iPhone Plus / Pro Max |
| Tablet | 768 px | iPad portrait |
| Desktop | 1024 px | Laptop |
| Wide | 1440 px | Standard desktop |

Required behaviours:

- Navigation collapses to off-canvas / hamburger below 768 px
- Tables (timelines, cost comparisons, embassy contacts) become stacked card layout below 640 px — never horizontally scrolling tables
- Floating WhatsApp button is always visible, bottom-right, never overlaps the in-page primary CTA
- Hero image scales via `object-fit: cover`, never letterboxes
- All form fields full-width below 640 px, `font-size: 16px` minimum to prevent iOS zoom

## 7. Hard reuse rule

> **Every new page reuses these exact tokens and components. No one-off styles.**

If you reach for a new colour, font, spacing value, or component, **stop**. Either:
1. Find the existing variable / partial that already does it, or
2. Propose the new token in [`MEMORY.md`](MEMORY.md) and add it to `main.css` `:root` / a new partial before using it.

No inline `style="…"`. No `<style>` blocks in templates. All styling goes through `main.css` variables and reusable classes.

## 8. Pre-publish design checklist

Run for every new page before marking the HTML row DONE:

- [ ] Exactly one `<h1>`, Playfair Display, clamp-scaled
- [ ] Typography hierarchy intact (H1 → H2 → H3, no skipped levels)
- [ ] Body copy in `--muted` on white, or `--cream` on `--charcoal` — verify contrast ≥ 4.5:1 (WCAG AA)
- [ ] All gold accents use `--gold` token, never a raw hex
- [ ] All section padding consistent with surrounding pages (sample one neighbouring page side-by-side)
- [ ] Tables collapse to stacked cards under 640 px
- [ ] CTA block uses the standard partial; WhatsApp + /contact only, no phone
- [ ] Floating WhatsApp button visible and not overlapping in-page CTA at 360 px width
- [ ] All images have descriptive `alt`; hero image uses `loading="eager"`, others `loading="lazy"`
- [ ] No inline styles, no `<style>` blocks
- [ ] Page extends `baseof.html` (check view-source: header, footer, WhatsApp float all present)
- [ ] Tested at 360 / 414 / 768 / 1024 / 1440 (responsive devtools)
- [ ] Visual diff against a neighbouring page in the same silo — looks like a sibling, not a stranger

## 9. Wiring with the rest of the planning system

| For… | Read |
|---|---|
| What page to build | [`funeral-repatriation-build-plan.html`](funeral-repatriation-build-plan.html) |
| Technical phase / DoD | [`BUILD-PLAN.md`](BUILD-PLAN.md) |
| How it must look | This file |
| Project context / agent rules | [`CLAUDE.md`](CLAUDE.md) |
| Past design decisions (e.g. "no costs on site", "phone removed") | [`MEMORY.md`](MEMORY.md) |
