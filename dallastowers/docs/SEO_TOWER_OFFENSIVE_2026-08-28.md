# SEO Tower Offensive — experiment ledger (2026-08-28)

## 0. Data caveat — read first
The GSC export `dallastowers.com-Performance-on-Search-2026-08-28.zip` was **not
accessible** in this session (not in uploads, Drive, or Gmail). All GSC figures
below are the brief's reported values, **unvalidated**: ~406 impressions over
five days from ~Aug 22, ~4 clicks, ~92 URLs with impressions, ~100 impressions/day,
building pages around positions 5–15. Independently corroborated: the Aug-23
Coverage export showed the index jump (2 → 90 known URLs, 37 indexed on Aug 17)
and "Alternate page with proper canonical tag: 5" — Google discovering clean-URL
duplicates. **Re-run the forensics of §3 of the brief when the export is supplied.**

Statistical posture: five days of a 3-week-old site is **early Google testing,
not established rankings**. Impressions at positions 5–15 on low-volume building
queries are consistent with ordinary new-site discovery given the sitemap
submission (~Aug 21) and IndexNow pings. Treat as promising, not validated.

## 1. Production state at start
Branch `claude/indexing-report-corrections-eepkhd` · pre-change HEAD `f7cfcd1` ·
production deploy `6a8cc103cf7780d4d92abd52` · validators PASS (122 pages,
120 sitemap URLs). Static HTML, no build step; canonical = `/<slug>.html`;
sitemap all `.html`; internal links were ~3,181 clean-form — the split-brain
this pass eliminates.

## 2. Why winners win and losers lose (SERP-verified 2026-08-28)
Live SERP research (WebSearch, 7 building queries) shows two SERP species:

- **Winner SERPs** (Travis, 588 Lofts, Park Highlander, Art House at So7,
  Lone Star Tower — and by extension Mercer Square, 2011 Cedar Springs,
  Belvedere, Park Plaza, Colonnade): occupied by HAR.com's templated building
  pages plus small local brokerage directories (knoxre, dfwurbanrealty,
  cityspacesdfw, skyrises, texaspriderealty, condomania sites). Thin,
  listing-oriented, no HOA rigor, no public-record data, older buildings with
  **no official website**. A young domain can be tested into these SERPs
  because no strong entity page exists.
- **Loser SERPs** (Bleu Ciel, Museum Tower, Knox/Auberge, Rosewood): official
  developer/building sites (museumtowerdallas.com, bleucielliving.com,
  auberge.com, rosewoodhotels.com, residencesturtlecreek.com), national
  portals (Homes.com), Sotheby's, and fresh press (Dallas Morning News,
  PaperCity, CultureMap, CandysDirt). Domain authority + official-entity
  status locks page one.

Conclusion: divergence is **SERP competition, not page quality** — our winner
and loser pages are the same template. The exploitable systematic edge:
buildings without official sites, i.e. most of the 1960s–2000s condo stock.

## 3. SERP beatability classes
- **A (attack):** Park Highlander, Mercer Square, 2011 Cedar Springs Lofts,
  The Belvedere, Park Plaza, Colonnade, Lone Star Tower, Art House at So7
- **B (attack):** The Travis at Katy Trail, 588 Lofts (semi-official sites, thin)
- **C (control):** Bleu Ciel (developer + Sotheby's + Homes.com)
- **D (do not chase):** Museum Tower, Knox Residences/Auberge, Rosewood
  Residences (official + press-dominated; our pages remain reference files)

## 4. Cohorts
**Intervention (10):** the-travis-at-katy-trail, the-knox-residences-auberge,
588-lofts, rosewood-residences-turtle-creek, the-belvedere, park-highlander,
2011-cedar-springs-lofts, mercer-square, art-house-at-so7, lone-star-tower.
(Knox and Rosewood included deliberately as in-cohort hard cases.)
**Controls (untouched):** colonnade-at-turtle-creek, park-plaza (matched
winners), bleu-ciel (competitive control), plus all other building files.
**Site-wide neutral change (affects all cohorts equally):** internal-link
canonicalization + `_redirects` (see URL_CONSOLIDATION_2026-08-28.md).

## 5. Interventions applied (per page)
| Field | Value |
| --- | --- |
| Changes | "Neighbors on file" boilerplate replaced with **Comparable buildings** — deterministically chosen (same district first, then certified-roll $/sf band, era, building form), with method note; internal links in canonical .html form |
| Aliases | Travis: `alternateName` "Travis at Knox" + prose; Park Highlander: `alternateName` "Drexel Highlander" + prose; Art House: `alternateName` "ArtHouse at So7"; Lone Star: `alternateName` "LoneStar Tower". Sourced from multiple independent listing portals (HAR + brokerage sites), phrased as portal-attribution, not building fact |
| Not changed | Titles, H1s, meta descriptions (already entity-aligned), county sections, FAQ, forms |
| Baseline GSC | unvalidated — capture from the export when supplied |
| Deployment | this pass; commit recorded in git log |

Known caveat: `ApartmentComplex.numberOfAccommodationUnits` in per-building
JSON-LD equals the certified-roll account count (e.g. Travis 52). Semantically
that is "residential unit accounts", not confirmed physical units. Left as-is
site-wide this pass; candidate for a later typed-schema correction.

## 6. Measurement plan
Compare intervention vs controls at **+7 / +14 / +30 / +60 days** from deploy
date (2026-08-28) on: impressions, clicks, CTR, avg position, query count,
top-10 and top-20 query counts, per URL. The .html/clean consolidation applies
to both cohorts equally, so cohort differences isolate the content changes;
URL-consolidation effects show up as site-wide shifts (watch GSC "Page with
redirect" and "Alternate page" counts fall).
Success definitions per brief §35. Early-site volatility is expected — do not
attribute movement to the intervention before +14 days minimum.

## 7. Success criteria snapshot
Exceptional: several intervention pages reach positions 1–5. Strong:
intervention beats controls on Δposition and Δimpressions. Neutral: cohorts
move together (conclude content wasn't the constraint). Negative: intervention
underperforms controls → revert comparables module and reassess.
