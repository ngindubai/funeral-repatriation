---
url: "/countries/"
title: "Country repatriation guides"
description: "Step-by-step guides for repatriating a loved one from abroad to the United Kingdom."
hero_image: "/images/airport-exterior.jpg"
# Each country below is its own nested section. They are covered by the single
# /countries/sitemap.xml (built from top-level .Section), so suppress their
# individual sitemap output to avoid 238 orphan sitemap files in the sitemap
# split (4 Jul 2026). _target scopes this to the nested country sections only,
# so the /countries/ landing keeps its own SectionSitemap output.
cascade:
  - target:
      path: "/countries/**"
    outputs:
      - HTML
---

