---
applyTo: "**"
---

# Build Plan Instructions

## Primary Source of Truth

`funeral-repatriation-build-plan.html` is the primary build plan. It contains phase definitions, stage breakdowns, task tables, progress badges (DONE / IN PROGRESS / TODO), and notes columns.

**Always read `funeral-repatriation-build-plan.html` before beginning any build task.**

`BUILD-PLAN.md` is a session-start summary that mirrors the current phase state. Read it at session start, then consult the HTML for full detail on individual tasks.

## Before Starting Any Task

1. Read `BUILD-PLAN.md` for current phase and top pending tasks.
2. Open `funeral-repatriation-build-plan.html` and find the specific task in the table.
3. Confirm the task status is IN PROGRESS or TODO before starting.
4. State which task you are working on and its current badge status.

## After Completing Any Task

1. Update `BUILD-PLAN.md`: change the task status in the phase summary table.
2. Update `funeral-repatriation-build-plan.html`:
   - Change the badge from TODO or IN PROGRESS to DONE (or IN PROGRESS if partially complete).
   - Update the notes/result column with what was done, pages created, and any important decisions.
   - Update the phase progress snapshot paragraph if the overall phase status has changed.
3. State the next recommended task from the HTML plan.

## Session Closing Protocol

Before ending any session, run:
- Update `BUILD-PLAN.md` with all tasks completed this session.
- Update `funeral-repatriation-build-plan.html` with badge changes and session notes.
- List any new patterns, decisions, or conventions established that should be added to `MEMORY.md`.
- State the recommended starting point for the next session.
