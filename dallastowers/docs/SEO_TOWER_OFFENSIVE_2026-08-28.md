# SEO Tower Offensive — experiment ledger (2026-08-28)

## 0. GSC data — VALIDATED (export received 2026-08-28, archived in reports/gsc/2026-08-28/)

Validated totals (Search type: Web, property to 2026-08-26):
- **413 impressions · 4 clicks · 0.97% CTR · 92 URLs with impressions · 90 queries**
- Zero exposure through Aug 21; first impressions **Aug 22** (24), then 89 / 85 / 110 / 98
  daily — the brief's ~406/~100-a-day figures confirmed.
- Daily avg position 25.0 → 27.9 (widening query testing, not decline).
- Devices: mobile pos 12.6 (140 impr) vs desktop 37.2 (264 impr) — Google tests
  materially better positions on mobile. Countries: US 355/413.
- Page position bands: **1–5: 5 · 5–10: 21 · 10–20: 16** · 20–40: 17 · 40+: 33.
- Query bands: 1–5: 2 · 5–10: 19 · 10–20: 11 · 20–40: 21 · 40+: 37.
- Clicks: the-travis-at-katy-trail ×2 (28 impr @ 9.1, 7.1% CTR),
  colonnade-at-turtle-creek ×1, the-terminal-at-katy-trail ×1.

Statistical posture unchanged: five days of testing on a 3-week-old site is
**promising early Google testing, not established rankings**. But the pattern
is real: 42 URLs already in top-20 territory, essentially all individual
building entities.

### Duplication, measured (validates the consolidation)
**17 building pairs received impressions under BOTH URL forms.** By form:
clean 324 impressions across 65 URLs vs .html 89 across 26. Google's serving
preference was the clean form (internal links outvoted rel=canonical).
Direction review with this data: consolidation to .html retained — declared
canonicals + sitemap have said .html since birth, all signals now agree, and
301s transfer the clean-form signals; a same-day reversal to clean would
churn more than it saves. Contingency: if intervention+control positions
degrade materially at +14d in a way that correlates with redirected URLs,
the clean-URL flip remains available with a documented 1:1 map.

### Unfulfilled demand signal
"tower 22 dallas" query cluster: 22 impressions across 4 variants at
positions 57–67 — matching loosely against our pages. Investigate what
Tower 22 is (likely a new development) before considering coverage; logged
in DALLAS_TOWER_COVERAGE_MAP.md.

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

## 8. Validated cohort baseline (clean+.html combined, Aug 22–26)
| Cohort | Building | Impr | Clicks | Wtd pos |
| --- | --- | --- | --- | --- |
| I | the-travis-at-katy-trail | 28 | 2 | 9.1 |
| I | the-knox-residences-auberge | 24 | 0 | 12.3 |
| I | 588-lofts | 10 | 0 | 14.0 |
| I | park-highlander | 10 | 0 | 8.0 |
| I | rosewood-residences-turtle-creek | 9 | 0 | 8.8 |
| I | the-belvedere | 8 | 0 | 9.0 |
| I | 2011-cedar-springs-lofts | 8 | 0 | 8.9 |
| I | lone-star-tower | 5 | 0 | 10.6 |
| I | art-house-at-so7 | 5 | 0 | 7.4 |
| I | mercer-square | 4 | 0 | 8.5 |
| C | bleu-ciel | 17 | 0 | 43.3 |
| C | colonnade-at-turtle-creek | 14 | 1 | 13.5 |
| C | park-plaza | 5 | 0 | 6.2 |

Intervention totals: 111 impressions, 2 clicks. Compare at +7/+14/+30/+60 days
(deploy date 2026-08-28); combine URL forms per building when comparing, since
the consolidation merges them.
