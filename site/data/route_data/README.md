# route_data/

Per-origin JSON files for the route generator (Engine 1).

Each file covers one origin country and all its destination corridors.
The generator reads these files to produce full-content route pages.

## Structure

```
route_data/
  spain.json
  thailand.json
  uae.json
  ...
```

## Schema

Each file is a JSON object with:
- `origin` -- origin country metadata
- `destinations` -- array of destination objects, one per corridor

Each destination object contains:
- `key` -- destination slug (uk, ireland, usa, australia)
- `name` -- display name
- `dest_slug` -- URL slug for destination
- `route_slug` -- full route slug (origin-to-destination)
- `consular` -- Irish or UK consular contact details
- `timeline` -- avg, fast, complex timelines
- `doc_processing_time` -- documentation processing time string
- `complexity` -- low / moderate / high
- `key_documents` -- list of required documents
- `airlines` -- airlines and airports serving the route
- `special_rules` -- list of route-specific rules and considerations
- `dest_reception` -- what happens when body arrives at destination
- `dest_consular_note` -- destination consular helpline text
- `seo_title` -- pre-researched SEO title (under 60 chars)
- `seo_description` -- pre-researched meta description (under 155 chars)
- `template_variant` -- A / B / C / D / E

## Source

All data sourced from:
- FCDO Travel Advice (gov.uk), updated 2025-2026
- Official embassy and consulate contacts
- IATA cargo regulations
- Professional repatriation experience

No facts are invented. Every claim is source-able.

*Last updated: 27 May 2026*
