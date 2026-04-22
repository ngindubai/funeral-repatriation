# Self-Review Checklist

Review the work just completed against these criteria.
Report each check as PASS or FAIL with a brief reason.
If any check FAILS, fix it before reporting done.

---

## Hugo Build

- [ ] Hugo builds without errors: run `hugo --gc --minify --cleanDestinationDir` from `site/`
- [ ] Page count is equal to or greater than before the session started (no pages accidentally removed)
- [ ] No ghost/double-prefix URLs in built output: `Get-ChildItem public -Directory | Where-Object { $_.Name -like "*repatriation-from-repatriation*" }` returns empty
- [ ] All new country `_index.md` files have explicit `slug:` field set to just the country key

## Content Quality

- [ ] No banned vocabulary: delve, tapestry, robust, seamless, elevate, foster, navigate (metaphorical), empower, revolutionise, game-changer
- [ ] No em dashes used anywhere in new content
- [ ] Source attribution present for all factual claims (costs, timelines, legal requirements)
- [ ] No safety guarantees or implied certainty ("will protect", "guaranteed", "stay safe")
- [ ] Tone is senior consultant — not travel blog, not brochure
- [ ] Sentence rhythm varies — mix of short and long sentences, not uniform paragraph length

## SEO Compliance

- [ ] Unique title tag (50–60 characters) contains primary keyword
- [ ] Meta description (140–160 characters) contains keyword and CTA
- [ ] Exactly one H1 on the page, containing primary keyword
- [ ] Target keyword appears in first 100 words of body copy
- [ ] All images have descriptive alt text
- [ ] At least 2 internal links with descriptive anchor text (not "click here" or "read more")
- [ ] FAQ schema JSON-LD added if this is a FAQ or informational page
- [ ] `short_answer` or `direct_answer_*` block added if this is a target page for LLM citation

## Build Plan

- [ ] `BUILD-PLAN.md` updated to reflect task completion or progress
- [ ] `funeral-repatriation-build-plan.html` updated: badge changed, notes column updated with result
- [ ] Next recommended task identified from the build plan

---

## Output Format

List all files changed, with one line per file explaining the change.

Then state clearly:

> **Ready for next task** — [name the next task from the build plan]

or

> **Issues found:** [list each failing check with what needs to be fixed]
