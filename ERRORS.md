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
**Prevention:** Keep the state file intact. Only delete it when diagnosing a confirmed sync mismatch. The curl delete step can be added to the workflow for one deploy, then removed.

### E004 — deploy.yml YAML parse error from paste duplication
**Date:** May 2026
**What happened:** When Gareth pasted new workflow content into the GitHub web editor without selecting-all first, the new content was appended to the old content. The resulting file had duplicated YAML sections causing a parse error on line 65: `Unexpected value 'with'`.
**Fix:** Always instruct Gareth to: (1) tap into the code area, (2) select all, (3) delete everything so the box is blank, (4) then paste.
**Rule added to CLAUDE.md:** When providing code for manual paste, always give explicit select-all-delete-paste instructions.

### E005 — MCP token cannot write to .github/workflows/ in funeral-repatriation repo
**Date:** May 2026
**What happened:** Every attempt to update deploy.yml via the MCP GitHub connector returned 403 Resource not accessible by integration. The token lacks the `workflows` scope for this specific repo.
**Fix:** Gareth must edit the workflow file manually via the GitHub web editor. Always provide the complete file content, never a diff or partial snippet.
**Note:** The MCP connector CAN write to .github/workflows/ in the pet-transport repo, but not funeral-repatriation. This appears to be a per-repo token scope issue.

### E006 — README.md in site/data/ subdirectory breaks Hugo build
**Date:** May 2026
**What happened:** A README.md file was placed inside site/data/route_data/ for documentation. Hugo scans every file in site/data/ and tries to parse it as structured data. It cannot parse .md files and threw: `unmarshal of format "" is not supported`. This broke the entire build.
**Fix:** Delete any non-JSON/TOML/YAML files from site/data/ and all subdirectories. Documentation for data files must live at repo root or in a non-data directory.
**Rule:** NEVER place .md, .txt, or any non-data-format files inside site/data/ or any subdirectory of site/data/.

---

*Last updated: 27 May 2026*
