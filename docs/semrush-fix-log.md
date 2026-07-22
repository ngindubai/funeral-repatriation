# Semrush fix log (22 July 2026)

Audit snapshot `6a5eb9d5` (project 29594194, repatriationfuneral.com) reported 2,890 errors, 10,254 warnings, 10,157 notices, site health 81. This log records the root causes, the fixes shipped, and the checks that now prevent recurrence. The binding rules live in `CLAUDE.md` under "LINK AND SLUG INTEGRITY" (rules S1 to S8).

## What was wrong and why

### Missing `slug` field, silent 404s (largest error class)
Hugo's `:slug` permalink token falls back to a TITLE-derived slug when `slug` is absent from front matter, not the filename. So:

- `guides/death-abroad-venezuela.md` (no `slug`) went live at `/guides/what-to-do-when-someone-dies-in-venezuela-a-guide-for-uk-families/` while every link pointed at `/guides/death-abroad-venezuela/` (404).
- Five guides (venezuela, ukraine, sierra-leone, namibia, guatemala) and nine blog posts were lost this way.

These pages built without any error and passed the old front-matter QA. Only a live crawl exposed them.

Fix: added `slug:` equal to the filename path on the five guides. For the nine blog posts the title-derived URLs were already indexed and better, so the inbound links were repointed instead (see below).

### Null slugs in the country data, empty `/repatriation-from-/` links
`site/data/countries_repatriation.json` is keyed by the canonical hub slug (equals the content directory name). 192 of 238 entries had no `slug` key, so templates reading `$c.slug` emitted `/repatriation-from-/`.

Fix: backfilled `slug` equal to the key for all 192 entries. Verified every key has a matching `site/content/countries/<key>/` directory and every non-null slug already equalled its key.

### Non-canonical hub links from route front matter
Routes carry `origin_slug: "united-states"` while the hub is `usa`; `dest_key: "us"`. The editorial-credit block hardcoded `/repatriation-from-{{ .Params.origin_slug }}/`, producing 249 broken links (121 UK, 106 US, plus UAE, Gambia, Cabo Verde, Congo, DRC, Vatican City) and the matching 4xx pages.

Fix (`routes/single.html`, `routes/route.html`): an alias map normalises the known non-canonical slugs, then the link is emitted through `site.GetPage "/countries/<slug>"` using the resolved page's `.RelPermalink`. A missing hub (for example Palestine) is dropped, never served as a 404.

### Superseded blog slugs still linked
Nine blog posts render at improved slugs (for example `repatriation-cost-guide.md` at `/blog/how-much-does-repatriation-cost/`), but 31 articles still linked the old paths. Fix: repointed all 31 to the live canonical slugs.

### `reviewedBy` on Article schema (1,008 errors)
Validators report `reviewedBy` as `NOT_RECOGNIZED` on `Article`. Fix: removed it from `countries/country-hub.html` and `blog/single.html`; Article now carries `author` and `publisher` only.

### Duplicate and over-long titles
Embassy pages built their title from `.Params.country_name`, a field embassy front matter does not have, so all 239 rendered `British Embassy in : Contacts for Death Abroad | Repatriate Service` (184 flagged as duplicate). Fix: resolve the country name from the data map keyed by `country_key`, drop the brand suffix. The suffix was also dropped from every programmatic single-page template (guide, city, blog, faq, ashes, cremation) to hold titles under 60 characters.

## Result (verified by a local Hugo build and link crawl of the built site)

- Broken internal links: 1,474 to **0**.
- Duplicate titles: 184 to **4** (the remaining four are route pages that share a title string; a generator-level fix).
- Titles over 60 characters: 298 to **92** (the rest are inherently long country names).
- `reviewedBy` schema errors: removed at source.

## Not fixed here (needs content or generator work, not a template change)

- Duplicate content (172): near-duplicate thin pages. Content review.
- Duplicate H1 and title (232): long-tail route pages whose `title` equals the H1 string. Vary the generated title.
- 67 files with Windows-1252 bytes: transcode to UTF-8 (rule S8). Renders as the replacement character on live pages.
- `wa.me` external-link warnings (about 9,720): crawler false positive (HTTP 429 from WhatsApp). No action.

## Reference: the link crawl the QA gate must run

Build first (`hugo --gc --minify --destination public`), then:

```python
import os, re, glob
from collections import Counter
root = "public"
def exists(path):
    p = path.split('#')[0].split('?')[0].strip('/')
    if p == '':
        return True
    return os.path.isfile(os.path.join(root, p)) or os.path.isfile(os.path.join(root, p, 'index.html'))
# --minify drops quotes, so match quoted and unquoted hrefs
href_re = re.compile(r'''href=(?:"([^"]*)"|'([^']*)'|([^\s>]+))''')
broken = Counter()
for f in glob.glob(os.path.join(root, "**", "index.html"), recursive=True):
    html = open(f, encoding='utf-8', errors='ignore').read()
    for m in href_re.findall(html):
        h = m[0] or m[1] or m[2]
        if h.startswith('/') and not h.startswith('//') and not exists(h):
            broken[h] += 1
assert not broken, f"{sum(broken.values())} broken internal links: {broken.most_common(20)}"
print("internal link crawl clean")
```

A clean run (zero unresolved internal links) is a hard gate before any commit that touches content, templates, or the country data.
