# Phase 3 LLM Citation Audit - Round 2 Summary

Source data: phase3_llm_citation_audit_round2_sheet.csv
Total queries in sheet: 12

## Model Metrics

| Model | Avg Depth Score (0-3) | Scored Queries | Citation Presence | Recorded Presence Rows |
|---|---:|---:|---:|---:|
| chatgpt | 0.00 | 0/12 | 0.0% | 0/12 |
| perplexity | 0.00 | 0/12 | 0.0% | 0/12 |
| gemini | 0.00 | 0/12 | 0.0% | 0/12 |

## URL Target Match

- Exact matches: 0/12
- Contains expected URL: 0/12
- Mismatches: 0/12
- Not recorded: 12/12

## Priority Upgrade Queue

| Query | Intent | Target Page Type | Expected URL | Trigger | Recommended Fix |
|---|---|---|---|---|---|
| how to bring a body home from thailand | transactional_country | country_hub | /repatriation-from-thailand/ | not_recorded | Strengthen intro and process summary for body-home phrasing |
| repatriation cost from spain to uk | transactional_cost | country_hub | /repatriation-from-spain/ | not_recorded | Increase cost-table prominence and cost-specific headings |
| what happens when someone dies abroad | informational_process | blog | /blog/what-happens-when-someone-dies-abroad/ | not_recorded | Tighten definition paragraph and add direct answer block above fold |
| documents needed to repatriate a body to the uk | informational_documents | blog | /blog/documents-needed-to-repatriate-body-to-uk/ | not_recorded | Expand document checklist formatting and schema-friendly ordering |
| how long does repatriation from mexico take | transactional_timeline | country_hub | /repatriation-from-mexico/ | not_recorded | Strengthen timeline headings and repeat average-case answer earlier |
| who pays for repatriation after a death abroad | faq_costs | faq | /faq/repatriation-costs-who-pays/ | not_recorded | Expand FAQ answer with direct payer scenarios and summary bullets |
| can i bring ashes in hand luggage uk | faq_ashes | faq | /faq/can-i-bring-ashes-in-hand-luggage/ | not_recorded | Add airline-proof wording and top-of-page yes-but conditions summary |
| repatriation from kenya to uk process | transactional_country | country_hub | /repatriation-from-kenya/ | not_recorded | Increase process-step specificity and UK-return wording in subheads |
| repatriation from philippines to uk timeline | transactional_timeline | country_hub | /repatriation-from-philippines/ | not_recorded | Promote timeline table and shorten answer distance from H1 |
| british embassy role when someone dies abroad | faq_embassy | faq | /faq/what-does-the-british-embassy-do-when-someone-dies-abroad/ | not_recorded | Add direct scope/limits answer block and responsibilities list |
| repatriation from brazil to uk cost | transactional_cost | country_hub | /repatriation-from-brazil/ | not_recorded | Add stronger cost-led excerpt and reinforce table labels |
| repatriation from vietnam to uk requirements | transactional_requirements | country_hub | /repatriation-from-vietnam/ | not_recorded | Promote required-documents table and add requirements answer summary near top |

## Notes

- Fill all score and cited columns in the CSV before treating metrics as final.
- Score range validation is enforced (0-3). Invalid values are ignored.
- Citation presence is measured over the full query set for direct comparability.
- URL matching compares expected_url to best_cited_url and flags mismatches automatically.
