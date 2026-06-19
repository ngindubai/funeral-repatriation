# Chunk 2: Diversification Pattern for Route Generators

Applied to `generate_r65_r66.py` (reference implementation). Port to all older generators in Chunk 2b.

## Dry-run result (2026-06-19)

```
=== mark_thin_routes_noindex.py [DRY-RUN] ===
Files scanned    : 1,723
To mark noindex  : 0
Already noindex  : 0
Clean (no action): 1,723
Skipped (no FM)  : 0

[DRY-RUN] No files written. 0 changes needed.
```

No same-country pairs exist (generator never builds origin==destination).
No thin pages exist (all 1,723 routes pass the 300-word FM threshold).
Script is ready for ongoing use as new routes are added.

## Three levers applied to generate_r65_r66.py

### Lever 1: FAQ question rotation
Add 3 variant phrasings per question slot, selected by `(variant_idx % 3)`.
Breaks the 7-question fixed template shared across all route pages.

```python
FAQ_Q_TIMELINE = [
    "How long does repatriation from {origin} to {dest} take?",
    "What is the typical timeline for repatriation from {origin} to {dest}?",
    "How many days does repatriation from {origin} to {dest} usually take?",
]
# ... (7 question slots x 3 variants each)

def pick(lst, idx):
    return lst[idx % len(lst)]

# In render_route():
q_timeline = pick(FAQ_Q_TIMELINE, variant_idx).format(origin=origin_name, dest=dest_name)
```

### Lever 2: direct_answer_points bullet-1 rotation
Two alternative framings for the key-document bullet.

```python
def bullet_key_doc(cert_name, cert_lang, variant_idx):
    if variant_idx % 2 == 0:
        return f"Key document: {cert_name} (in {cert_lang})"
    else:
        return f"Primary certificate required: {cert_name}, issued in {cert_lang}"
```

### Lever 3: overview_heading variation
Three H2 headings instead of the single fixed form.

```python
OVERVIEW_HEADINGS = [
    "What happens after a death in {origin}",
    "The immediate steps following a death in {origin}",
    "What to do when someone dies in {origin}",
]

# In render_route():
overview_heading = pick(OVERVIEW_HEADINGS, variant_idx).format(origin=origin_name)
```

## How to port to older generators (Chunk 2b)

1. Add the `OVERVIEW_HEADINGS`, `FAQ_Q_*` lists and `pick()` function at the top of the file after the existing constants.
2. Add the `bullet_key_doc()` function.
3. Update `render_route(route, variant)` to `render_route(route, variant, variant_idx)`.
4. Inside `render_route()`, replace:
   - `f"Key document: {od['cert_name']} (in {od['cert_lang']})"` with `bullet_key_doc(od['cert_name'], od['cert_lang'], variant_idx)`
   - `"What happens after a death in {origin_name}"` with `pick(OVERVIEW_HEADINGS, variant_idx).format(origin=origin_name)`
   - Each FAQ question string with the `pick(FAQ_Q_*, variant_idx).format(...)` pattern
5. Update `main()` to pass `variant_idx` to `render_route()`.
6. Run the existing QA gate (`banned`, `price_patterns`, `safety_patterns`) checks unchanged.

## Acceptance criteria for Chunk 2b
- All 30+ generate_r*.py scripts updated with all 3 levers
- `python generate_rXX_rYY.py` still produces 0 QA errors on a test run
- No layout files modified
- Commit on master
