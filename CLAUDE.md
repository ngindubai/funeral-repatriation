# CLAUDE.md — Repatriate Service

> **Read this first every session.** It is intentionally short. It points you at the other files that contain the real detail. Do not pull the whole repo into context — use the file map below.
>
> **The roadmap is [`funeral-repatriation-build-plan.html`](funeral-repatriation-build-plan.html). It is the only source of truth for what to build and in what order.** Every other planning file in this repo supports it — none competes with it. Never invent a parallel roadmap.

## Site overview

**Repatriate Service** (live: `repatriationfuneral.com`, final domain target: `repatriateservice.com`) is a UK-focused lead-generation website for international funeral repatriation. The audience is bereaved British families needing to bring a loved one home from abroad, plus corporate travel managers and insurers. The business model is enquiry capture (WhatsApp + quote form) routed to repatriation operators. The site is a YMYL property in the highest E-E-A-T tier — every factual claim (cost, timeline, law, regulation) must be source-cited or it is cut. **The site does not display prices.** Tech: Hugo v0.160.1 extended, Markdown + JSON data, single CSS file, deployed to Surge.

## File map (read only what you need)

### Plan / direction files — read at the start of any build task

| File | Purpose |
|---|---|
| [`funeral-repatriation-build-plan.html`](funeral-repatriation-build-plan.html) | **Authoritative roadmap.** What to build next, in what order, with which keywords/scope. Phases 0–6, every stage rowed with DONE / IN PROGRESS / TODO badges and a notes column. **Do not rewrite — only update badges and notes after a stage completes.** |
| [`BUILD-PLAN.md`](BUILD-PLAN.md) | What technical step is next + per-page Definition of Done + session protocol + current state. |
| [`DESIGN-PLAN.md`](DESIGN-PLAN.md) | How every page must look. Colour tokens, fonts, components, mobile-first rules, pre-publish design checklist. |
| [`MEMORY.md`](MEMORY.md) | Why we decided X. Architectural decisions, lessons learned, gotchas. Consult when something looks unusual; append when a new decision is made. |
| [`AGENTS.md`](AGENTS.md) + `workforce/` | Worker soul files — read the relevant one when the task is domain-specific (legal accuracy, SEO, country research, etc.). |

### Live site key files

| File | Purpose |
|---|---|
| [`site/hugo.toml`](site/hugo.toml) | Hugo config, params (brand, whatsappNumber, analytics IDs), permalinks (section reshape to `/repatriation-from-{slug}/`), sitemap. |
| [`site/layouts/_default/baseof.html`](site/layouts/_default/baseof.html) | **Master template.** Every page extends it via `title`, `page-meta`, `schema`, `main` blocks. Injects header, footer, WhatsApp float. |
| [`site/layouts/partials/header.html`](site/layouts/partials/header.html) | Top nav with Resources dropdown, transparent over hero, solid on scroll, WhatsApp link only. |
| [`site/layouts/partials/footer.html`](site/layouts/partials/footer.html) | Dark slate footer, WhatsApp + /contact CTA, no phone. |
| [`site/layouts/partials/countries/country-{a,b,c,d,e}.html`](site/layouts/partials/countries/) | Five country-hub template variants. Picked via `template_variant` frontmatter. Diversification — do not converge them. |
| [`site/assets/css/main.css`](site/assets/css/main.css) | **Only stylesheet.** All design tokens in `:root`. New rules must use these variables — never raw hex. |
| [`site/assets/js/main.js`](site/assets/js/main.js) | Only JS file. Nav scroll behaviour, accordions, form submit handlers. |
| [`site/data/countries_repatriation.json`](site/data/countries_repatriation.json) | 238-country dataset read at build time. Country pages bind via the `country_key` frontmatter. |
| [`site/data/cities_p1.json`](site/data/cities_p1.json) | City-page dataset. |
| [`site/content/`](site/content/) | All Markdown content, organised by silo: `countries/{country}/`, `guides/`, `blog/`, `faq/`, `bringing-ashes-home/`, `cremation-transfer/`, `embassy-contacts/`. |
| [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | GitHub Copilot equivalent of this file (more verbose). Cross-check if rules conflict — this file is canonical for Claude. |

## At the start of any build task — do this

1. Open [`funeral-repatriation-build-plan.html`](funeral-repatriation-build-plan.html) → find the next IN PROGRESS or TODO row → that is the **what**.
2. Open [`BUILD-PLAN.md`](BUILD-PLAN.md) → confirm the phase, read sections 3 (master template rule) and 5 (Definition of Done) → that is the **next step + order**.
3. Open [`DESIGN-PLAN.md`](DESIGN-PLAN.md) → use the listed tokens and components → that is the **look**.
4. State the row ID you're working on (e.g. "Stage 3.C23") and confirm scope before editing.
5. Build.

## Working rules

| Rule | Detail |
|---|---|
| Scope | Edit only what is asked. Never rewrite whole files unprompted. Never restructure existing files, rename pages, or reorganise directories without explicit instruction. |
| Templating | Every new page extends [`baseof.html`](site/layouts/_default/baseof.html). No standalone HTML. Reuse existing partials. |
| Styling | Use the CSS variables in [`main.css`](site/assets/css/main.css). No inline `style`. No `<style>` blocks. No new colour without a `MEMORY.md` entry. |
| Internal links | Relative URLs only. Descriptive anchor text. Never "click here" / "read more". Minimum 2 per new page. |
| Country frontmatter | Country hub `_index.md` MUST have explicit `slug: "{country-key}"`. Missing slug → ghost double-prefix URL. Verified gotcha — see [`MEMORY.md`](MEMORY.md). |
| Content rules | No prices. No phone. WhatsApp `+447703577246` + `/contact` only. Source-cite every factual claim. No banned vocab (delve, tapestry, robust, seamless, elevate, foster, navigate-as-metaphor, empower, revolutionise, game-changer). No em dashes. |
| Data | Live rate / regulation data must be sourced and verified at build time, never invented. Cite source name + date. |
| Commit messages | Descriptive: what changed, which stage row, what for. E.g. `Stage 3.C23: add 10 city pages (long-stay expat angle) — build 1681 pages`. |
| File creation | Prefer editing over creating. Do not create markdown documentation files to explain changes unless asked. |

## Build + deploy

| Step | Command (run from `site/`) |
|---|---|
| Build | `hugo --gc --minify --cleanDestinationDir` |
| Local preview | `hugo server -D` |
| Deploy | `surge public/ uk-funeral-repatriation.surge.sh` |

Deployment is **manual**. There is no GitHub Actions workflow in this repo. The Surge CLI on the local machine is already authenticated as `garethdeansomers@gmail.com` — never log out, never change account, never alter the Surge target subdomain unless explicitly instructed.

After every successful build and deploy:
- Update the relevant stage badge + notes column in [`funeral-repatriation-build-plan.html`](funeral-repatriation-build-plan.html).
- Update "Current session state" in [`BUILD-PLAN.md`](BUILD-PLAN.md).
- Add architectural decisions to [`MEMORY.md`](MEMORY.md).

## Current status

- **Phase 3 — Content Depth and Optimisation — IN PROGRESS**
- 1,671 pages live across 238 countries (as of May 2026)
- Most recent: SEMrush Round 2 audit fixes (slug + ghost-URL repairs across cremation-transfer, guides, country-hub, 5 embassy-contacts, 16 meta descriptions)
- Next: open [`funeral-repatriation-build-plan.html`](funeral-repatriation-build-plan.html) → pick the next IN PROGRESS row in Phase 3
