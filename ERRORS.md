# ERRORS.md — Repatriate Service

> Log of failed approaches and mistakes. Read before trying anything that has been attempted before. Updated every session.

---

## ERROR LOG

### E001 — layout: frontmatter causes Hugo to silently skip pages
**Date:** May 2026
**What happened:** Route pages had `layout: route` in frontmatter. Hugo looked for `layouts/routes/route.html`, which did not exist. Hugo silently skipped building those pages. The build succeeded with no errors, but the pages did not exist in `public/`.
**Fix:** Remove `layout:` field entirely from all route page frontmatter. Hugo auto-selects `layouts/routes/single.html` for pages in the routes section.
**Rule added to MEMORY.md:** NEVER add `layout:` field to route page frontmatter.

### E002 — Wrong server-dir in deploy.yml caused files to land in wrong Hostinger directory
**Date:** May 2026
**What happened:** server-dir was changed to `/home/u356263466/domains/repatriationfuneral.com/public_html/`. FTP chroots the user to account home, so this created a nested directory `public_html/home/u356263466/...`. Files went to the wrong place. Route pages 404d. The live site (already deployed to the real `/public_html/`) kept working because those files were already in the right place.
**Fix:** Revert server-dir to `/public_html/`. This is the correct path, confirmed by Hostinger File Manager showing the live site files at `home > public_html`.
**Rule added to MEMORY.md:** server-dir is `/public_html/`. Never change it.

### E003 — Stale .ftp-deploy-sync-state.json caused incremental deploy to skip real missing files
**Date:** May 2026
**What happened:** The FTP sync-state file recorded route pages as "already uploaded" from a prior deploy that wrote them to the wrong directory (E002). Subsequent deploys skipped uploading the routes because the state said they were current. The routes were never in the real `/public_html/routes/` folder.
**Fix:** The state file was cleared (via a curl delete step in the workflow), forcing a full re-scan and re-upload.
**Prevention:** Keep the state file intact. Only delete it when diagnosing a confirmed sync mismatch. NOTE: the one-time delete step was never removed from deploy.yml and still runs on every deploy. See the structural-issue note at the end of this file.

### E004 — deploy.yml YAML parse error from paste duplication
**Date:** May 2026
**What happened:** When Gareth pasted new workflow content into the GitHub web editor without selecting-all first, the new content was appended to the old content. The resulting file had duplicated YAML sections causing a parse error.
**Fix:** Always instruct Gareth to: (1) tap into the code area, (2) select all, (3) delete everything so the box is blank, (4) then paste.

### E005 — MCP token cannot write to .github/workflows/ in funeral-repatriation repo
**Date:** May 2026
**What happened:** Every attempt to update deploy.yml via the MCP GitHub connector returned 403 Resource not accessible by integration. The token lacks the `workflows` scope for this specific repo.
**Fix:** Gareth must edit the workflow file manually via the GitHub web editor. Always provide the complete file content, never a diff or partial snippet.

### E006 — README.md in site/data/ subdirectory breaks Hugo build
**Date:** May 2026
**What happened:** A README.md file was placed inside site/data/route_data/ for documentation. Hugo scans every file in site/data/ and tries to parse it as structured data. It cannot parse .md files and threw: `unmarshal of format "" is not supported`. This broke the entire build.
**Fix:** Delete any non-JSON/TOML/YAML files from site/data/ and all subdirectories.
**Rule:** NEVER place .md, .txt, or any non-data-format files inside site/data/ or any subdirectory of site/data/.

### E007 — baseURL missing www causes site-wide canonical mismatch
**Date:** 1 June 2026
**What happened:** baseURL in hugo.toml was `https://repatriationfuneral.com/` (no www). Google was crawling the www. version of the site, but every canonical tag, og:url, and JSON-LD URL output by Hugo pointed to non-www. GSC flagged this as 'Alternate page with proper canonical tag' for every page.
**Fix:** Set baseURL to `https://www.repatriationfuneral.com/`. Update any hardcoded URLs in templates that bypass site.BaseURL.
**Rule:** baseURL MUST include www. Never reference a hardcoded non-www URL anywhere.

### E008 — 70 broken sideways links across route silo from unbuilt reverse routes
**Date:** 1 June 2026
**What happened:** Every route page (e.g. `singapore-to-united-kingdom`) had a sideways link in frontmatter pointing to `/routes/united-kingdom-to-{country}/`. The reverse-direction route pages (UK-to-X, Ireland-to-X) had never been built. Result: 70 broken internal links across the route silo, served as HTML <a> tags rendering 404s when clicked.
**Fix:** Patched `site/layouts/routes/single.html` to filter sideways links through `site.GetPage` existence check. Built a `$validSideways` slice at the top of the template and replaced all 5 variant `range .Params.links.sideways` calls with `range $validSideways`. Broken links no longer render. When reverse routes are built later, links auto-restore with no content file changes.
**Rule:** When rendering frontmatter-driven internal links in templates, use `site.GetPage` to verify existence. Never trust author-supplied URLs.

### E009 — robots.txt and llms.txt served non-www URLs after baseURL fix
**Date:** 1 June 2026
**What happened:** E007 was fixed in hugo.toml and template JSON-LD, but the static files `site/static/robots.txt` and `site/static/llms.txt` still contained 50+ hardcoded `https://repatriationfuneral.com/` URLs. These bypass Hugo and are served as static content. Google read robots.txt with a non-www sitemap reference; AI crawlers read llms.txt with non-www URLs throughout.
**Fix:** Rewrite both files with www URLs.
**Rule:** Any static file containing URLs must be checked for www consistency every time baseURL changes. Static files are not templated and do not use site.BaseURL.

### E010 — Missing cremation-transfer permalink rule in hugo.toml
**Date:** 1 June 2026
**What happened:** The `[permalinks.page]` block in hugo.toml had entries for every content section except cremation-transfer. Hugo fell back to default routing for those 238 pages, which produced the correct URL by coincidence (section + slug) but left no explicit canonical rule. This made the configuration fragile and inconsistent with the rest of the site.
**Fix:** Add `"cremation-transfer" = "/cremation-transfer/:slug/"` to the page permalink block.
**Rule:** Every content section must have an explicit permalink rule in hugo.toml. Do not rely on Hugo defaults for production URLs.

### E011 — Broken sameAs TODO array and dead social links in production
**Date:** 1 June 2026
**What happened:** Site-wide Organization schema in baseof.html contained `"sameAs": ["TODO: Facebook URL", "TODO: LinkedIn URL"]` — literal placeholder strings being served to Google. Footer contained 4 social icon links with `href="#"` that did nothing on click.
**Fix:** Removed sameAs array from schema until real URLs exist. Removed social icons block from footer until real accounts exist. Both can be added back when accounts are live.
**Rule:** Never ship placeholder text inside JSON-LD or as href="#" dead links. Either implement properly or omit until ready.

### E012 — Future-dated content silently skipped by Hugo, causing 404s on a successful build
**Date:** 2 June 2026
**What happened:** Engine 3 Batch 4-6 blog articles (15 files) were given `date: 2026-06-02` in their frontmatter, matching the calendar day they were written. The GitHub Actions build that should have published them ran on 1 June at 21:37 UTC. Hugo's default `buildFuture` is `false`, so it treated every 2 June page as a future-scheduled draft and silently excluded it from `site/public/`. The build reported SUCCESS with no error, the `live` branch updated normally, but the 15 pages did not exist and every URL returned 404. Batch 1-3 articles (dated 1 June or earlier) were unaffected and built normally.
**Why it was misleading:** This presented as a deploy problem. There are two workflows, run #66 had failed, and deploy.yml deletes the sync-state on every run. None of those were the cause. The build that published was GREEN; it simply contained 15 fewer pages than expected because Hugo excluded them.
**Fix:** Added `buildFuture = true` to hugo.toml. Every page on this site publishes on commit (there is no editorial schedule), so building future-dated content is correct. With this set, the build-time clock no longer matters and a page dated "today" can never silently vanish again.
**Rules:**
- Set and keep `buildFuture = true`. Do not remove it.
- When a SUCCESSFUL build is missing pages, suspect content exclusion FIRST (future dates, `draft: true`, expired `expiryDate`, layout mismatch per E001), not the deploy pipeline. A green build that omits pages is almost always Hugo excluding content.
- Avoid dating content ahead of UTC. The runner builds in UTC; local "today" can be UTC "tomorrow".

---

## STRUCTURAL ISSUE (not yet fixed) — duplicate deploy workflows race on every push

**Date observed:** 2 June 2026
**What happens:** Two workflow files both trigger on push to master.
- `build-and-publish.yml` builds Hugo and force-pushes `site/public` to the `live` branch (`peaceiris/actions-gh-pages`, `force_orphan: true`).
- `deploy.yml` builds Hugo and FTP-deploys to Hostinger (`SamKirkland/FTP-Deploy-Action`), and also runs a `curl ... DELE .ftp-deploy-sync-state.json` step on every run.

On rapid successive pushes the two runs race; the `live`-branch force-push can lose the race and the run fails. This is what failed on run #66 (the BUILD-PLAN commit). It is cosmetically alarming but did NOT cause the Batch 4-6 404s (that was E012).

**Why it should be cleaned up:**
1. Two full pipelines run on every push, doubling build minutes.
2. The sync-state DELE step in deploy.yml was a one-time fix for E003 and was never removed. It now forces a full FTP re-scan on every deploy, defeating the incremental design.
3. It is ambiguous which pipeline actually serves repatriationfuneral.com. This must be established.

**Action required (Gareth, manual — MCP cannot edit workflow files per E005):**
- Confirm which pipeline serves the production domain (FTP to Hostinger, or the `live` branch). Hostinger hosting implies FTP (`deploy.yml`) is the live one; if so, the `live` branch / GitHub Pages workflow is redundant.
- Keep one pipeline. Delete or disable the other (or restrict its `on:` triggers).
- Remove the sync-state DELE step from deploy.yml.
- Do this as a SEPARATE change, never mixed with content commits, to avoid concurrent-deploy clobbering during the change itself.

---

*Last updated: 2 June 2026*
