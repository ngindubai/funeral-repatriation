# Phase 3 LLM Citation Audit - Round 2

Date: 21 April 2026
Stage: 3.10 (Second LLM citation audit)
Scope: Establish structured Round 2 audit worksheet after table upgrades and city-depth expansion.

## 1) Audit Objective

Measure whether the site is cited more often than baseline for high-intent repatriation queries after:

- Structured cost and requirement tables were added to country pages.
- City-depth coverage reached all 26 country hubs.

## 2) Baseline Reference

- Prior baseline anchor: Phase 2.12 baseline citation audit task in build plan.
- Structural baseline reference: `phase3_performance_review_baseline_2026-04-21.md`.

## 3) Round 2 Query Set

Use exact prompts below in each LLM and record citation behavior:

1. how to bring a body home from thailand
2. repatriation cost from spain to uk
3. what happens when someone dies abroad
4. documents needed to repatriate a body to the uk
5. how long does repatriation from mexico take
6. who pays for repatriation after a death abroad
7. can i bring ashes in hand luggage uk
8. repatriation from kenya to uk process
9. repatriation from philippines to uk timeline
10. british embassy role when someone dies abroad
11. repatriation from brazil to uk cost
12. repatriation from vietnam to uk requirements

## 4) LLMs To Test

Run each query in:

- ChatGPT
- Perplexity
- Gemini

## 5) Scoring Framework

For each query and model, capture:

- Direct citation present to this domain: Yes/No
- Citation depth level:
  - 0 = no mention
  - 1 = domain mention only
  - 2 = correct page cited but weak relevance
  - 3 = correct, high-relevance page cited in top answer body
- Cited page type:
  - country hub
  - city page
  - guide
  - faq
  - blog
  - ashes page
  - embassy page
  - cremation page
- Citation quality notes (brief)

## 6) Round 2 Measurement Sheet

Fill this table during live audit execution.

| Query | ChatGPT (0-3) | Perplexity (0-3) | Gemini (0-3) | Best-cited URL | Notes |
|---|---:|---:|---:|---|---|
| how to bring a body home from thailand | TBD | TBD | TBD | TBD | |
| repatriation cost from spain to uk | TBD | TBD | TBD | TBD | |
| what happens when someone dies abroad | TBD | TBD | TBD | TBD | |
| documents needed to repatriate a body to the uk | TBD | TBD | TBD | TBD | |
| how long does repatriation from mexico take | TBD | TBD | TBD | TBD | |
| who pays for repatriation after a death abroad | TBD | TBD | TBD | TBD | |
| can i bring ashes in hand luggage uk | TBD | TBD | TBD | TBD | |
| repatriation from kenya to uk process | TBD | TBD | TBD | TBD | |
| repatriation from philippines to uk timeline | TBD | TBD | TBD | TBD | |
| british embassy role when someone dies abroad | TBD | TBD | TBD | TBD | |
| repatriation from brazil to uk cost | TBD | TBD | TBD | TBD | |
| repatriation from vietnam to uk requirements | TBD | TBD | TBD | TBD | |

## 7) Structural Readiness Check (Completed)

Confirmed before running live prompts:

- Country hub coverage: 26/26
- Countries without city pages: 0
- City pages live: 79
- Structured cost/requirement tables: live via country template

## 8) Initial Interpretation

Round 2 is ready for live citation execution. Structural prerequisites are met and materially stronger than baseline.

No external citation claims are made in this document yet. Citation deltas must only be recorded after executing the query set in the three target LLMs.

## 9) Next Step

Execute the 12-query matrix in ChatGPT, Perplexity, and Gemini. Then calculate:

- Citation presence rate per model
- Average citation depth score per model
- Query clusters with strongest and weakest citation performance
- Priority page upgrades for weak clusters

## 10) Execution Files

Round 2 now has an execution workbook and auto-summary tool:

- Input workbook: phase3_llm_citation_audit_round2_sheet.csv
- Summary generator: scripts/compute_citation_audit_round2.py
- Generated summary: phase3_llm_citation_audit_round2_summary.md
- Expected target URLs are prefilled for all 12 queries in the workbook.
- Summary output now includes URL target match status (exact, contains expected, mismatch, not recorded).
- Workbook now includes intent clusters and recommended fix actions for each query.
- Summary output now generates a priority upgrade queue for missed, mismatched, or weak-scoring queries.

Run command:

- python scripts/compute_citation_audit_round2.py

Recommended workflow:

1. Fill one row per query in the CSV workbook after each model check.
2. Run the summary script.
3. Paste key deltas back into this report and update build-plan 3.10 output.
