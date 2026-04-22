# Setup Guide — Repatriate Service (Standalone Instance)

This file documents the steps to complete the migration from the Research monorepo to a standalone VS Code instance on Desktop.

---

## Files Created in This Migration

All files below were created before the copy to Desktop:

| File | Purpose |
|------|---------|
| `.github/copilot-instructions.md` | Auto-loaded every session. Site identity, conventions, rules. |
| `.github/instructions/build-plan.instructions.md` | Instructs Copilot to read HTML build plan before and after every task. |
| `.github/instructions/code-standards.instructions.md` | Hugo file conventions, slug rules, build commands. |
| `.github/instructions/seo-rules.instructions.md` | SEO requirements for all content and layout files. |
| `.github/prompts/self-review.prompt.md` | Quality checklist — run after every task before marking done. |
| `.github/prompts/new-page.prompt.md` | Standardised new page creation prompt. |
| `.github/agents/reviewer.agent.md` | Read-only reviewer agent for batch QA passes. |
| `MEMORY.md` | Project history, decisions, patterns. Attach at session start. |
| `BUILD-PLAN.md` | Session-start phase summary. References HTML build plan. |
| `AGENTS.md` | Workforce map — 14 worker soul files and when to engage them. |

---

## Post-Copy Steps (Already Executed)

The following have been completed by the migration script:

- [x] `funeral-repatriation/` copied to `C:\Users\garet\Desktop\funeral-repatriation`
- [x] Fresh git repository initialised at `C:\Users\garet\Desktop\funeral-repatriation`
- [x] Initial commit created with all files
- [x] Hugo build verified — page count confirmed, no ghost URLs

---

## First VS Code Session

1. Open VS Code.
2. File → Open Folder → `C:\Users\garet\Desktop\funeral-repatriation`
3. Open GitHub Copilot Chat (new chat).
4. Send this opening message:

```
New session. Attach: #file:MEMORY.md #file:BUILD-PLAN.md

Confirm you understand:
- The site's purpose and current build status
- The next task from funeral-repatriation-build-plan.html
- The Hugo conventions from copilot-instructions.md

Do not start any work yet. Just confirm your understanding.
```

5. Read Copilot's summary and correct anything wrong before starting work.
6. Then use `#file:.github/prompts/new-page.prompt.md` for any new page creation.

---

## Session End Protocol (Every Session)

Before closing:
1. Update `BUILD-PLAN.md` — mark completed tasks in the phase table.
2. Update `funeral-repatriation-build-plan.html` — change badges, update notes column.
3. Add a row to the Session History table in `MEMORY.md`.
4. Ask Copilot: "List any new patterns or decisions from this session that should be added to MEMORY.md."

---

## Build and Deploy Reference

```powershell
# Navigate to Hugo project root
cd C:\Users\garet\Desktop\funeral-repatriation\site

# Full clean build
hugo --gc --minify --cleanDestinationDir

# Verify no ghost URLs
Get-ChildItem public -Directory | Where-Object { $_.Name -like "*repatriation-from-repatriation*" }
# Expected output: (empty)

# Deploy
surge public/ uk-funeral-repatriation.surge.sh
```

---

## Post-Move Verification Checklist

Run this after the copy to Desktop is complete:

- [ ] `C:\Users\garet\Desktop\funeral-repatriation\site\public\` exists and contains built output
- [ ] Hugo build runs without errors from the new path
- [ ] Page count matches or exceeds 269
- [ ] Ghost URL check returns empty
- [ ] `funeral-repatriation-build-plan.html` opens correctly in browser
- [ ] `site/data/countries_repatriation.json` is present and intact
- [ ] `workforce/` directory contains all soul files
- [ ] `.github/copilot-instructions.md` is present
- [ ] Git log shows initial commit

---

## Original Location

Source was: `C:\Users\garet\Desktop\Research\funeral-repatriation\`

The original folder in the Research monorepo can be deleted after verification is complete. Do not delete until the verification checklist above is fully checked off.
