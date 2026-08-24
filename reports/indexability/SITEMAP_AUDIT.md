# Sitemap Forensic Audit — pcsoahu.com

**Audit date:** 2026-08-24 · **Production sitemap:** `https://pcsoahu.com/sitemap.xml` (single flat sitemap, no index file; declared in `robots.txt`)

## Live audit at time of inspection (pre-fix, 59 URLs)

| Metric | Count |
|---|---|
| total sitemap URLs | 59 |
| 200 canonical (self-consistent) | 59 |
| redirects | 0 |
| 404 | 0 |
| noindex | 0 |
| canonical mismatch | 0 |
| duplicate | 0 |

Every sitemap URL was fetched live: all 59 returned HTTP 200 directly (no redirect chains), `content-type: text/html; charset=UTF-8`, no `X-Robots-Tag`, no meta noindex, no hreflang, and a self-referential canonical exactly equal to the sitemap URL. One transient network failure (`/embed/`) re-fetched clean. Host and protocol are correct (`https://pcsoahu.com`, apex).

## URL-form conventions
- Directory pages are listed with trailing slash (`/buy/`); flat pages with `.html` (`/bases/tripler.html`). Consistent with each page's canonical tag — the sitemap form always equals the canonical form.
- Netlify Pretty URLs additionally serves each flat page at its extensionless twin (e.g. `/guides/harpta`, HTTP 200) and rewrites internal hrefs to that form at deploy time. **All 30 extensionless twins were fetched: every one returns 200 and carries the canonical pointing at the `.html` form**, so Google consolidates the pair correctly. Trailing-slash variants of flat pages 301 to the extensionless form; uppercase variants 301. No indexable duplicate exists without a correct canonical.

## lastmod discipline
`gen/build.py` stamps each URL's `lastmod` from that page's own Article JSON-LD `dateModified` (the date the content was actually authored/verified), falling back to the sitewide data-refresh date (`2026-08-01`) for hub/tool pages with no article date. **No deployment-date stamping**: e.g. the two guides restored during this audit carry `2026-08-06` and `2026-08-05` — their true content dates — not the deploy date. The gate (`gen/gate.py` §7b) fails any missing, malformed, or future lastmod. This defect existed historically (uniform hardcoded date) and was fixed 2026-08-18.

## Completeness (inventory vs sitemap)
- Canonical indexable pages missing from sitemap: **0**
- Sitemap-only URLs with no page: **0**
- Intentional-noindex pages in sitemap: **0** (`/embed/bah-widget.html` and `/404.html` are excluded by the generator and gate-enforced)

## Restorations made during this audit (proven stale-route regressions)
Two guides were published and production-verified on 2026-08-05/06, then silently dropped from production by the documented branch-divergence overwrite (see `editorial/AUDIT_LOG.md`, 2026-08-16): they returned **HTTP 404 live** while remaining in Google's discovery set (they appeared in the sitemap Google last read before 2026-08-16). Both restored verbatim from the editorial branch, with their original verified dates:
- `/guides/rent-vs-buy.html` (lastmod 2026-08-06)
- `/guides/vehicle-registration.html` (lastmod 2026-08-05)

**Post-fix sitemap: 61 URLs.** Additive-only verified: live 59 → 61, exactly the two restorations added, nothing removed or renamed.

## GSC submission
Submit/verify in Search Console as: property `https://pcsoahu.com` → Sitemaps → enter **`sitemap.xml`** (the path only — the UI prepends the property origin; pasting the full URL is a common cause of "invalid sitemap" errors). No prior successful submission is recorded in the repository, and one failed submission attempt is documented (2026-08-20, "invalid sitemap address") — treat submission as **not yet verified**.
