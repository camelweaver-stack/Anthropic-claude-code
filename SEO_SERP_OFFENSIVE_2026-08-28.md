# SEO SERP Offensive — experiment record (2026-08-28)

Controlled ranking experiment: query-level competitive analysis → surgical improvements to
pages Google already tests at positions ~5–20 → measure movement in subsequent GSC exports.

## Phase 0 — baseline

- **Baseline date:** 2026-08-28
- **Baseline commit (pre-intervention):** `c2f5676` on `claude/wfl-daily-publishing-i7lmp9`
- **Architecture (audited):** plain static HTML, 310 pages, published from repo root
  (`netlify.toml publish="."`); Python generator (`gen/`) + `apply_standing_fixes.py` final
  step (8 gates incl. placeholder-assert); deploy = Netlify connector with validating build
  command (`validate-production.js`); extensionless canonicals; EN↔ES hreflang; sitemap
  derived from disk. All gates green at baseline.
- **DATA NOTE:** the 08-28 ZIP arrived mid-session after target selection had begun on the
  08-23 snapshot; it was then ingested as `data/gsc/2026-08-28/` and **the 08-28 numbers
  below are the official experiment baseline**. The export fully confirmed the target
  selection — identical strike-zone queries, modestly higher volume.
- **Baseline GSC totals (2026-08-28 export):** 8 clicks · 1,420 impressions · 125 page rows
  · 208 query rows. Lockheed query cluster grew to **~179 impressions across 6 variants at
  positions 11.2–15** (was ~140 in the 08-23 window) — exposure still climbing pre-
  intervention. All other cohort baselines within noise of the 08-23 values except as
  updated in the Phase 15 table.

## Phase 1–2 — opportunity table (strike zone: pos 5–20, commercial intent weighted)

| # | Query (family) | URL | Clicks | Impr | CTR | Pos | Intent | Comm. | Lead | Page quality | Opp. | Action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | apartments near lockheed martin fort worth (+texas/tx/bare/brand, 6 variants) | /guides/apartments-near-lockheed-martin-fort-worth | 0 | ~140 | 0% | 11.2–15 | renter relocation near employer | High | High | Strong (retitled 08-24) | High | Improve |
| 2 | fort worth country day tuition (+fwcd/country day variants) | /schools/private-schools-west-fort-worth | 0 | 10 | 0% | 11–38 | school cost research (relocation adjacent) | Med | Med | Medium (FWCD tuition missing) | High | Improve |
| 3 | trinity valley school (+fort worth) | same | 0 | 8 | 0% | 3.25–5 | school research | Med | Med | Strong | Med (defend/CTR) | Improve |
| 4 | weatherford property tax rate | /data/property-tax | 0 | 4 | 0% | 10.5 | buyer cost research | High | High | Strong | High | Improve |
| 5 | aledo property tax rate | /data/property-tax | 0 | 3 | 0% | 7.67 | buyer cost research | High | High | Strong | High | Improve |
| 6 | westpoint at scenic vista (apartments) | /complexes/westpoint-at-scenic-vista | 0 | 7 | 0% | 7.25–7.33 | named-complex research | High | Med | Strong | Med | Improve (light) |
| 7 | apartments near nas jrb fort worth | /guides/apartments-near-nas-jrb-fort-worth | 0 | 1 | 0% | 9 | military relocation | High | High | Strong | Med | Improve |
| 8 | (page-side) willow park vs hudson oaks queries | /compare/willow-park-vs-hudson-oaks | 0 | 12 | 0% | 7.5 | town-vs-town buyer decision | Very High | High | Medium (no TEA data) | High | Improve |
| 9 | (page-side) aledo vs weatherford | /compare/aledo-vs-weatherford | 0 | 6 | 0% | 6.5 | town-vs-town buyer decision | Very High | High | Medium (no TEA data) | High | Improve |
| 10 | weatherford high school campus map | /schools/weatherford-isd/ | 0 | 3 | 0% | 11 | school geography | Med | Low | Medium | Low | Improve (one link) |
| 11 | working at lockheed martin | /relocate/working-at-lockheed-martin-fort-worth | 0 | 1 | 0% | 29 | employer relocation | High | High | Strong (new 08-24) | Observe | Leave alone (too new) |
| 12 | second chance apartments fort worth under $1000… | /second-chance | 0 | 2 | 0% | 19 | renter | Med | Low | Strong | Low | Leave alone |
| 13 | 6 weeks free / six weeks free | /specials | 0 | 2 | 0% | 10 | brand-ish deal | Med | Med | Strong | Low | Leave alone |
| 14 | rent to own homes (national) | /rent-to-own | 0 | 2 | 0% | 14.5 | generic national | Low | Low | Strong | Low | Leave alone |
| 15 | schools/aledo-isd pages (pos 7.5–9.3) | /schools/aledo-isd/* | 0 | 14 | 0% | 7.5–9.3 | district research | High | Med | Strong (linked 08-24) | Med | Leave alone this round (links just added; avoid churn) |

## Phase 3 — SERP forensics (live searches, 2026-08-28)

**Q1 — "apartments near lockheed martin fort worth"** (and variants): organic results are
(1) equityapartments.com brand collection page, (2) **shorttermhousing.com corporate-housing
service** (position ~2 — furnished/short-term intent is validated), (3–7) individual
communities' own "maps & directions" doorway pages (The Kelley, Royalton at Chapel Creek,
Village of Hawks Creek, Silver Leaf, Sansom Bluff, Oxford at Lake Worth), (8) an apartment-
locator listicle. **No neutral multi-community comparison ranks above us.** Advantages we
can't replicate: national/brand domain authority (Equity), property-brand exactness.
Exploitable weaknesses: every competitor is self-promotional (one property or one service);
none compares pockets, prices, or commutes; none covers short-term AND long-term AND
buy-adjacent paths. Their geographic spread (Westworth Village, Lake Worth, north side)
exceeds our pocket table's explicit naming.

**Q2 — "weatherford property tax rate" / "aledo tx property tax rate"**: Ownwell
programmatic county-trend pages (2–3 slots each), official city finance pages, property-
tax.info, local news, a homebuyer blog. Weaknesses: Ownwell shows *effective median %* (and
different numbers for the Parker vs Tarrant slices, which confuses); city pages show *only
the city's own levy* ($0.3996 Weatherford; $0.390082 Aledo 2024-25). **Nobody assembles the
full combined stack (city+ISD+county+college) with dollar examples — we already do.** The
missing piece on our page: a section that explicitly reconciles the three numbers a searcher
sees (city-only rate vs median-effective % vs the true combined stack).

**Q3 — "fort worth country day tuition" / "trinity valley school"**: aggregators (Niche,
Homes.com, US News, FindingSchool, privateschoolreview) + official school pages.
**Primary-source verification (2026-08-28):** FWCD publishes exact 2026-27 tuition at
fwcd.org/admission/tuition-and-financial-assistance — JK $18,050 · K-4 $28,470 · 5-8
$30,510 · 9-12 $31,770, plus meal plans $840–$1,450, activity fee $500, $4.6M aid / 1-in-4
students. TVS publishes at tvs.org/admission/tuition-fees — Pre-K $18,750 · K-4 $29,450 ·
5-8 $30,750 · 9-12 $31,625, books/lab fees included, need-blind admission. **Our page
wrongly stated FWCD releases exact figures only to applicants — fixing this with the
verified schedule is the single highest-quality content correction available.** Aggregators
give one stale number with no corridor/commute context; our page pairs verified tuition
with west-side geography — the differentiation.

**Q4 — "apartments near nas jrb fort worth"**: ILS giants (Apartments.com military page,
ApartmentGuide, Rent.com), Yelp, the on-base privatized housing operator
(nasjrbfortworthhomes.com), and official Navy Housing (ffr.cnic.navy.mil). Authority we
can't match: ILS inventory scale. Weakness: none integrates BAH math, jet-noise contours,
gate-to-door times, or the on-base-vs-off-base decision; official pages are on-base only.
Add: explicit on-base vs off-base orientation with a link to the official Navy Housing
office — the one authoritative resource a PCS family needs that the ILS pages omit.

**Q5 — town-vs-town comparisons (willow park vs hudson oaks; aledo vs weatherford)**: SERPs
are thin (Niche/city-data style aggregates, no purpose-built comparisons). Our pages
already rank 6.5–7.5 but **contain zero school-rating data** — the top decision factor.
Adding the verified 2026 TEA ratings deepens exactly what the queries imply.

## Phase 4 — content gap matrix (condensed to decisive gaps)

| Information | WFL | Competitors | Opportunity |
|---|---|---|---|
| Neutral multi-pocket Lockheed comparison w/ rent bands + drives | ✅ | ❌ (all self-promotional) | Press advantage |
| Short-term/corporate housing near plant | link only | ✅ (ranks #2) | Add visible section |
| Westworth Village / Lake Worth pocket naming | ❌ | ✅ (property pages) | Add geography (verifiable) |
| Combined tax stack per city + $ examples | ✅ | ❌ | Press; add reconciliation explainer |
| City-rate vs effective-median vs combined confusion | ❌ | ❌ | Category-3 gap — add |
| FWCD exact 2026-27 tuition | ❌ (claimed unpublished) | official site only | Add verified schedule + table |
| TVS exact tuition | ✅ | aggregators stale | Keep; table format |
| On-base vs off-base NAS JRB orientation + official housing office | ❌ | official site (on-base only) | Add |
| TEA 2026 ratings in town comparisons | ❌ | ❌ | Category-3 gap — add |

## Phase 6 — first offensive cohort (all improve-in-place; no new URLs)

Tier A: (1) Lockheed apartments guide · (2) private-schools (tuition) · (3) data/property-tax
Tier B: (4) willow-park-vs-hudson-oaks · (5) aledo-vs-weatherford · (6) NAS JRB guide ·
(7) westpoint-at-scenic-vista (meta only) · (8) weatherford-isd (one authoritative link)
Deliberately untouched: aledo-isd pages (links added 08-24 — let them settle), the new
relocation hub (4 days old), all Tier-D generic pages.

## Phase 15 — per-page ledger (deployed 2026-08-28)

Common fields: deployment date 2026-08-28 · no URLs changed · no URLs created · no titles
changed (all already intent-matched; churn avoided) · all baselines from the 08-23 snapshot.

| URL | Primary query | Secondary | Base impr | Base clicks | Base CTR | Base pos | Main competitors | Their edge | Gap closed | Changes |
|---|---|---|---|---|---|---|---|---|---|---|
| /guides/apartments-near-lockheed-martin-fort-worth | apartments near lockheed martin fort worth (texas) | lockheed martin apartments; …tx | ~179 (6 variants, 08-28) | 0 | 0% | 11.2–15 | equityapartments.com collection; shorttermhousing.com; 6 property doorway pages | brand/domain authority; property exactness | short-term/corporate option now visible; Westworth Village + Lake Worth named | new "Two pockets + short-term option" section |
| /schools/private-schools-west-fort-worth | fort worth country day tuition | fwcd tuition; trinity valley school (+fw) | 18 (all variants) | 0 | 0% | 3.25–38 | fwcd.org, Niche, Homes.com, US News, FindingSchool | official source; aggregator authority | page now carries the verified 2026-27 answer both query families seek | verified FWCD schedule + 2-school tuition table; corrected stale claim |
| /data/property-tax | weatherford property tax rate | aledo property tax rate | 7 | 0 | 0% | 7.67–10.5 | Ownwell trend pages ×3; weatherfordtx.gov; aledotx.gov | programmatic scale; official levies | reconciliation of city-only vs median-effective vs combined stack (nobody had it) | new explainer section + homestead link |
| /compare/willow-park-vs-hudson-oaks | (page-side) willow park vs hudson oaks | — | 12 | 0 | 0% | 7.5 | thin aggregator comparisons | none meaningful | school ratings were absent from a schools-decided comparison | TEA 2026 section (A 92 vs B 80, split-street caveat) + 2 district links |
| /compare/aledo-vs-weatherford | (page-side) aledo vs weatherford | — | 6 | 0 | 0% | 6.5 | same class | none meaningful | same gap | TEA 2026 "what changed" section + district links |
| /guides/apartments-near-nas-jrb-fort-worth | apartments near nas jrb fort worth | nas jrb fort worth housing | 4 | 0 | 0% | 9–38 | Apartments.com military page; ApartmentGuide; Rent.com; ffr.cnic.navy.mil | inventory scale; official status | on-base vs off-base orientation + official Navy Housing link (ILS pages omit both) | new orientation section |
| /schools/weatherford-isd/ | weatherford high school campus map | — | 5 | 0 | 0% | 11 | wisd.net official | authority | routes map-intent to the authority instead of dead-ending | one wisd.net sentence |
| /complexes/westpoint-at-scenic-vista | westpoint at scenic vista (apartments) | — | 7 | 0 | 0% | 7.25–7.33 | property's own site + ILS | official status | none needed | reviewed; meta already strong — deliberately unchanged |

Internal links added: 6 outbound-in-body (2× tea-ratings, 2× isd-comparison, Navy Housing
official, wisd.net official, homestead, short-term guide). No changes to titles, H1s,
canonicals, sitemap membership, or schema beyond content-supported text.
