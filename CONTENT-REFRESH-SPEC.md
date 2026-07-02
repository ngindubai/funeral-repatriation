# Content Refresh Spec: quarterly regulatory-fact review

> Created 2 July 2026 as build-plan item F12 (SEO audit, brief Stories 4 and 5).
> This is a spec for a recurring pass, not a one-off task. It is Opus-designed
> and Opus-or-human-run, because it changes dated YMYL facts.

## Why this exists

Repatriation content states facts that go stale: consular phone numbers, whether
an embassy is open, travel advisories, treaty membership, processing times. A
wrong FCDO number or a claim that an embassy is open when it has closed causes
real harm to a grieving family. The site currently stamps "Updated [month]" on
every build (8 template locations use `{{ now.Format "January 2006" }}`) and
carries three hardcoded "May 2026" verification stamps, so it already presents
itself as freshly reviewed. This pass makes that claim true.

## The load-bearing principle

**Flag, never blind-apply.** No fact on this site is changed automatically. Every
proposed change is verified against a named, dated source, written into a change
report, and confirmed by Opus or a person before it touches content. If a source
cannot be found for a fact this cycle, mark the fact "unverified this cycle" and
flag it; do not guess, invent, or delete it (CLAUDE.md rule 3).

## Cadence

- **Quarterly** (four times a year), plus an **event-triggered** run whenever a
  known major consular change lands (an embassy closes, a travel advisory flips
  to "against all travel", the FCDO changes its emergency number).
- Each run produces one dated report at `docs/refresh/YYYY-QN.md` and, if changes
  are confirmed, one deploy.

## The volatile-fact register

Check these fact classes, in priority order (highest harm first). For each, the
named dated source to verify against and where the fact lives in this repo.

### 1. FCDO 24-hour emergency line (highest harm, highest spread)
- Current value: `+44 (0)20 7008 5000`, appearing ~3,029 times across route
  content plus hub and guide templates.
- Source: gov.uk FCDO "Contact the Foreign, Commonwealth & Development Office".
- If changed: a controlled find-and-replace across `site/content/routes/*.md`,
  the country data, and the `generate_r*.py` generators (so future builds inherit
  the new number). One change, verified once, applied everywhere.

### 2. British embassy operational status and contacts
- Facts: whether a post is open, which post covers a country, phone, website,
  and the hardcoded status lines in content (for example "The UK Embassy in
  Kabul suspended operations in August 2021", "British Embassy Tehran not
  operational since 2011", "consular assistance via Poland or Lithuania").
- Lives in: `data/countries_repatriation.json` `embassy_contacts.*`
  (`phone`, `website`, `address`, `type`, status notes) and in `dest_consular`
  and body text of route files and country `_index.md` files.
- Source: gov.uk "British embassies, consulates and other diplomatic missions"
  and the per-country page under gov.uk/world/organisations.

### 3. FCDO travel advisories
- Facts: "against all travel" / "against all but essential travel" statements
  (currently on Afghanistan, Russia, Ukraine, Syria, Libya and others).
- Source: gov.uk/foreign-travel-advice/{country}. This is the most frequently
  changing class; re-check every country flagged with an advisory each cycle.

### 4. Treaty and documentation facts (lower volatility)
- Facts: Hague Apostille Convention membership and accession dates
  (for example "Zimbabwe joined the Hague Apostille Convention in 2014").
- Source: the HCCH Apostille Section status table.
- Also: documentation processing-time ranges and registration-authority names.
  Lower churn; verify against the existing `source` and `confidence` fields in
  the data and re-confirm any marked low-confidence.

### 5. Cost data (currently dormant)
- After F13 (2 July 2026) the hub templates no longer render `cost_guide`, and
  route pages never carried prices. The `cost_guide` data still exists but is
  unrendered, and 18 of 238 countries carry a `source: "VERIFY BEFORE PUBLISHING"`
  flag. Because it is not user-facing, cost data is the lowest priority. Do not
  re-surface prices without a separate decision (the site's rule is qualitative
  cost guidance only).

## The freshness-date integrity fix (do this on the first run)

The "Updated [current month]" auto-stamp is technically misleading: it advances
on every build with no review behind it. Replace the 8 `{{ now.Format "January
2006" }}` occurrences and the 3 hardcoded "May 2026" stamps with a single site
parameter, for example `site.Params.lastReviewed`, that is bumped **only** when a
refresh pass completes. After that, the displayed "last reviewed" date is honest:
it moves when, and only when, the facts were actually re-checked.

## The pass workflow

1. **Enumerate**: build the working list from the register above (all advisory
   countries, all embassy status lines, the FCDO number, any low-confidence
   data fields).
2. **Verify**: for each fact, fetch or search its named source and record the
   current authoritative value with the source URL and the date checked.
3. **Diff**: compare the authoritative value to what the site currently states.
4. **Report**: write each discrepancy to `docs/refresh/YYYY-QN.md` as a row:
   fact, location(s), old value, new value, source URL, date checked, confidence.
5. **Confirm**: Opus or a person reviews the report and approves each change.
   Unverifiable facts are marked "unverified this cycle" and left unchanged.
6. **Apply**: edit the data, the generators, and the content for approved changes
   only. Bump `site.Params.lastReviewed`.
7. **Gate and deploy**: run `qa_routes.py`, `check_schema.py`, `check_titles.py`;
   commit the batch; push to master (one deploy) per the standing deploy rule.

## Model and guardrails

- **Run on Opus, or with a person in the loop.** Verifying a consular fact and
  judging whether a source is authoritative is exactly the judgement this file
  reserves for Opus; a cheaper model should not confirm YMYL fact changes.
- Every applied change cites a named, dated source in the report.
- Any rewritten copy follows the house rules: no em dashes, no banned vocabulary,
  no prices, British English, named dated sources only.
- Never blind-apply, never guess a missing fact, never delete a fact to make a
  check pass. Flag it.

## First-run checklist

- [ ] Implement the `lastReviewed` site param and replace the 8 auto-date stamps
      and 3 hardcoded "May 2026" stamps.
- [ ] Verify the FCDO emergency line against gov.uk.
- [ ] Re-check every country currently carrying a travel advisory.
- [ ] Re-check every hardcoded embassy-closure or covering-post statement.
- [ ] Write `docs/refresh/2026-Q3.md` and confirm before applying.
