# Repatriate Service — Build Plan

> **Primary tracker:** `funeral-repatriation-build-plan.html`
> Always read the HTML before starting any task. This file is a session-start summary only.
> Update BOTH this file AND the HTML at the end of every session.

---

## Current Status

- **Active phase:** Phase 3 — Content Depth and Optimisation
- **Phase status:** IN PROGRESS
- **Pages live:** ~1,696 (1,671 existing + 25 new route pages, as of 27 May 2026)
- **Deployment:** repatriationfuneral.com (via GitHub push to Hostinger FTP)
- **Last session (27 May 2026):** Turn B — Route Pair Engine. New silo /routes/ created. 25 origin x destination route pages built (Stage 3.ROUTE-A). Generator script `generate_routes.py`, QA script `qa_routes.py`, and Hugo template `site/layouts/routes/single.html` all committed. `hugo.toml` updated with /routes/ permalink. Deploy workflow fixed (security:loose, secrets-based server/username, timeout:60000 — mirroring pet-transport working config). Surge deploy references removed from CLAUDE.md and MEMORY.md. **ACTION REQUIRED: FTP secrets must be set in GitHub repo Settings > Secrets: FTP_SERVER, FTP_USERNAME, FTP_PASSWORD.** Workflow cannot update itself (requires `workflows` permission scope) — workflow file must be updated manually by repo owner.

---

## Phase 3 Stage Summary

| Stage | Task | Status | Notes |
|-------|------|--------|-------|
| 3.1 | Remaining P1 country hubs | IN PROGRESS | 238 countries live, 999 pages. All hubs built. |
| 3.2 | Country hub coverage | IN PROGRESS | All 238 countries covered. |
| 3.3 | P2 city pages | DONE | City depth added across P2 countries |
| 3.4 | Bringing ashes home silo | DONE | All 238 countries covered. |
| 3.5 | Cremation transfer silo | DONE | All 238 countries covered. |
| 3.6 | Embassy contacts | DONE | All countries covered. |
| 3.7 | Blog: 2-3 articles per week | DONE | 150 articles live. |
| 3.8 | Baseline performance review | IN PROGRESS | Structure and optimisation queue documented |
| 3.9 | Content upgrades pass 2 | IN PROGRESS | All 26 hubs have direct_answer blocks. Meta desc template fixed. No costs on site. |
| 3.10 | LLM citation audit pass 2 | IN PROGRESS | Site not cited 0/4 (May 2026). Next: verify deploy is reaching Hostinger. |
| 3.CTR | CTR rescue: 25 highest-imp / lowest-CTR pages | DONE | **Turn A complete (27 May 2026).** 25 pages. 14 bare country-name titles replaced. 7 missing meta descriptions added. Titles ≤60 chars, descs ≤155 chars. |
| 3.ROUTE | Route pair engine (origin x destination pages) | IN PROGRESS | **Turn A complete (27 May 2026).** New /routes/ silo. 25 route pages committed (australia-to-ireland through vietnam-to-united-kingdom). Generator: `generate_routes.py`. QA: `qa_routes.py`. Template: `site/layouts/routes/single.html`. All 25 pages QA PASS: 6 FAQs, 7 timeline steps, 6 internal links, no em-dashes, no prices, no banned words. **Turn B:** next 25 corridors — high-value P2xP2 pairs and Ireland-origin routes. |
| 3.T | Template variant rollout (A-E) | DONE | All 238 hubs assigned template_variant A-E. |
| 3.W | Phone removal + WhatsApp CTA | DONE | All phone references removed site-wide. |
| 3.C1-C22 | City pages Chunks 1-22 (220 pages) | DONE | Build 1670 pages, 0 errors. |
| 3.11 | FAQ entity pages | DONE | Standalone FAQ pages published. |
| 3.R | Phase 3 end-of-phase review | DONE | All 8 review issues resolved. |
| 3.D | Design review pass (full site) | DONE | 23 Apr 2026. All 16 issues resolved. |
| 3.2b | Guide depth: unique country prose | DONE | 400-600 word body copy for all 26 countries. |

---

## Deployment

**Process:** Push to git (master branch) → GitHub Actions builds Hugo → FTP deploy to Hostinger.

**Required secrets** (set in GitHub repo Settings > Secrets and variables > Actions):
- `FTP_SERVER` — Hostinger FTP server address
- `FTP_USERNAME` — Hostinger FTP username
- `FTP_PASSWORD` — Hostinger FTP password

**No manual deploy step.** Surge references have been removed. Do not use `surge` commands.

**If deploy fails:** Check Actions tab in GitHub. The workflow logs the run URL and troubleshooting steps on failure. Most common cause: FTP secrets not set, or Hostinger FTP port 21 blocked.

**Workflow file** (`.github/workflows/deploy.yml`) needs manual update by repo owner to match the pet-transport working config (security:loose, secrets-based credentials, timeout:60000). The MCP GitHub integration does not have `workflows` permission scope to update it directly.

---

## How to Use This File

**At session start:**
1. Read this summary to get current phase state.
2. Open `funeral-repatriation-build-plan.html` and find the specific next task.
3. Reference `MEMORY.md` for architectural decisions and patterns.

**At session end:**
1. Update the stage status table above.
2. Update `funeral-repatriation-build-plan.html` — change badge, update notes column.
3. Add a row to the Session History in `MEMORY.md`.

---

## Phase 4 Preview

Phase 4 covers: link building strategy, schema expansion, conversion rate optimisation, and second performance review. See `funeral-repatriation-build-plan.html` for full task breakdown.

---

## Session Protocol

**Start every session with:**
```
New session. Read BUILD-PLAN.md and MEMORY.md.
Confirm: site purpose, current build status, next task.
Do not start work until confirmed.
```

**End every session with:**
```
Before closing:
1. Update BUILD-PLAN.md with tasks completed.
2. Update funeral-repatriation-build-plan.html with badge changes.
3. List any new decisions to add to MEMORY.md.
4. State the recommended starting point for the next session.
```
