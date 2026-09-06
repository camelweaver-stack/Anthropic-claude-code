# URL consolidation — 2026-08-28

## Problem
Google received impressions for both `/slug` and `/slug.html` (brief report;
corroborated by Coverage "Alternate page with proper canonical tag: 5" and
"Page with redirect: 3"). Cause: split-brain signals — canonicals (119) and
the sitemap point at `.html`, while ~3,181 internal links used the clean form,
which Netlify serves 200 via implicit pretty-URL resolution.

## Decision: consolidate to `.html`
The indexed, ranking, canonical form has always been `.html` (37 URLs indexed
on it per Coverage). Flipping to clean URLs would 301 every young ranking URL —
maximum disturbance for cosmetic benefit. Keeping `.html` changes **zero
indexed URLs**: only duplicates gain redirects and internal links align.
Alternative (clean-URL flip) documented and rejected for this reason; can be
revisited once rankings are mature, though there is little reason to.

## Implementation
1. `site/_redirects`: 119 rules, `/slug  /slug.html  301`, one per sitemap
   page. Exclusions: `/` (homepage), `/thanks` (Netlify form POST target —
   a redirect would break submissions), `/404`.
2. Internal links: 2,999 `href='/slug'` occurrences rewritten to
   `/slug.html` across 122 pages. Form `action` attributes untouched.
3. Canonicals, sitemap, og:url: already `.html` — unchanged.
4. Redirect map: 1:1, no chains (targets are terminal file paths; no source
   is a `.html` path), no loops, no 404 targets — machine-verified.

## Validator guards (validate-site.py)
- `[redirects]`: every sitemap page has its clean-variant rule; all rules 301;
  no duplicate sources; no `.html` sources; targets must exist; `/thanks`
  must never be redirected.
- `[links-canonical]`: any internal clean-form href to an existing page fails
  the build.

## Other duplication audit
- www/http variants: 301 to `https://` apex at the Netlify edge (verified live
  earlier; GSC "Page with redirect: 3" is exactly these — benign).
- Trailing slashes, case variants, parameters: no internal links generate
  them; Netlify normalizes; no action.
- Alternate slugs / old building names: none exist as URLs (aliases handled
  via `alternateName`, never duplicate pages).

## Post-deploy verification checklist
`/park-highlander` → 301 → `/park-highlander.html` (single hop, 200);
`.html` URLs still 200; `/thanks` POST target untouched; sitemap unchanged;
IndexNow re-ping of all 120 canonical URLs.
