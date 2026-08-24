# Indexability Matrix — pcsoahu.com

**Audit date:** 2026-08-24 · All values verified against **live production** (`https://pcsoahu.com`), not local build, except the two FIXED rows which were verified live post-deploy. Depth/inbound from the rendered-link crawl (`INTERNAL_LINK_GRAPH.md`).

## Critical URL acceptance

| URL | 200 | Canonical | Meta robots / X-Robots-Tag | Sitemap | Inbound | Depth | Static content | Verdict |
|---|---|---|---|---|---|---|---|---|
| / | ✓ | self | none / none | ✓ | 58 | 0 | ✓ (~1.6k words) | PASS |
| /bah-report/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ full data in HTML | PASS |
| /pcs-checklist/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ | PASS |
| /bases/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ | PASS |
| /neighborhoods/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ | PASS |
| /bases/pearl-harbor-hickam.html | ✓ | self | none / none | ✓ | 1 | 2 | ✓ | PASS |
| /bases/schofield-wheeler.html | ✓ | self | none / none | ✓ | 1 | 2 | ✓ | PASS |
| /bases/kaneohe-bay.html (MCBH) | ✓ | self | none / none | ✓ | 1 | 2 | ✓ | PASS |
| /bases/tripler.html | ✓ | self | none / none | ✓ | 1 | 2 | ✓ | PASS |
| /tools/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ | PASS |
| /buy/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ | PASS |
| /sell/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ | PASS |
| /on-base/ | ✓ | self | none / none | ✓ | 58 | 1 | ✓ | PASS |
| /guides/rent-vs-buy.html | ✓ (was 404) | self | none / none | ✓ (restored) | footer+hub+in-body | 1 | ✓ | **FIXED** |
| /guides/vehicle-registration.html | ✓ (was 404) | self | none / none | ✓ (restored) | footer+hub | 1 | ✓ | **FIXED** |
| /embed/bah-widget.html | ✓ | self | noindex / none | excluded | n/a | n/a | ✓ | INTENTIONAL NOINDEX |
| /404.html | serves 404 | self | none | excluded | n/a | n/a | ✓ | PASS (hard 404, no soft-404) |

All 44 remaining sitemap URLs (guides, neighborhoods, family pages, TLA, quiz, data desk, etc.): live-fetched, every one **200 · self-canonical · no noindex · in sitemap · link-reachable · static HTML ≥500 visible words** → PASS. Full per-URL data: `canonical_url_inventory.json` + `INTERNAL_LINK_GRAPH.md`.

## Structured data
- 9 pages carried `FAQPage` JSON-LD whose Q&A text was **not visible anywhere on the page** — a violation of Google's FAQ structured-data content guidelines ("unsupported FAQ schema"). **FIXED: FAQPage nodes removed** from all nine emitters (`/bah-report/`, `/buy/`, `/sell/`, `/on-base/`, `/vehicle-shipping/`, `/guides/{pets-to-hawaii,harpta,dodea-schools,on-base-waitlist}`) and from the two restored guides. Article/Dataset/other schema retained; no visible content changed. (Future option, out of scope here: render the Q&A visibly and re-add the markup.)
- No Review/AggregateRating/LocalBusiness/Offer/Product types anywhere (gate-enforced blocklist). Article `mainEntityOfPage` self-consistent on every page. All JSON-LD parses (gate §8.1).

## Duplicates / variants
- Netlify Pretty URLs serves each flat page at `.html` and extensionless forms, both 200; extensionless form always canonicalizes to the `.html` form → consolidates correctly. Trailing-slash and uppercase variants 301. No un-canonicalized duplicates. English-only; zero hreflang anywhere (gate-enforced).

## Notes for later (explicitly NOT fixed — outside proven-defect authority)
- Base pages: 1 unique inbound link each (their hub). Weak but not orphaned. Recommend natural neighborhood→base and base↔family cross-links in a future editorial pass.
- Thin-page diagnostics flagged nothing skeletal (thinnest indexable page ≈530 visible words); no rendering bugs.
- CONTENT-QUALITY REVIEW LATER applies to nothing at this time; if clean pages remain unindexed after several more weeks, revisit page-level index selection per the audit brief's stop condition.
