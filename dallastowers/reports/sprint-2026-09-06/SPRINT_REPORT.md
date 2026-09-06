# Coordinated improvement sprint — 2026-09-06

## Baseline (reported in brief; no export file supplied — archive one when available)
14 active days: 639 impressions, 8 clicks, 1.25% CTR; first 7 active days
511/6 vs latest 7 days 128/2; mobile avg position 13.7 vs desktop 37.6.
Second-week decline is confounded: it overlaps the Aug-28 URL consolidation
(301s over the majority-serving clean URLs) and normal post-testing decay.
Judge against the +14/+30-day checkpoints, not this window.

## URL convention decision (Phase 2)
**`.html` retained** under the brief's own escape hatch ("unless … indexing
evidence demonstrates another convention is materially safer"): canonicals and
the sitemap have declared `.html` since site birth, Google's indexing
consolidated onto it, and the Aug-28 consolidation (119 forced single-hop
301s, 2,999 internal links aligned, validator-enforced) is only days into
Google's re-digestion. Flipping to extensionless now would create the third
canonical state in two weeks and re-redirect every ranking URL mid-
stabilization. All 22 duplicate groups named in the brief were verified
resolved live (single 301 → 200, no chains). Machine checks cover duplicate
routes, chains/loops, redirected sitemap entries, internal links to
redirects, and canonical targets.

## Experiment design amendment
The Aug-28 controls (Colonnade, Park Plaza, Bleu Ciel) were **promoted to
treated** by owner directive in this sprint (all pages now carry computed
comparables + distinct metadata). No holdout remains; measurement shifts to
site-level and page-level pre/post comparisons against the archived Aug-28
baselines in `reports/gsc/2026-08-28/`.

## Weak high-impression pages — diagnosis (Phase 5)
| Page | Wtd pos (Aug 22–26) | Diagnosis | Action this sprint |
| --- | --- | --- | --- |
| Bleu Ciel | 43 | SERP class C: developer site, Sotheby's, Homes.com own page one | Distinct metadata; comparables; no head-term chase |
| Museum Tower | 30 | Class D: official site dominates | Same; long-tail (hoa/plans queries) is the play |
| Tower Residences Ritz | 67 | Class D + brand ambiguity ("ritz residences dallas") | Metadata now disambiguates phase/name |
| Preston Tower | 63–69 | Large 1966 tower; competitor pages deeper on rules; our rules unverified | Metadata + comparables; research queue already ranks its assessment-risk file |
| The Tower (Dallas) | 29–48 | Name ambiguity — absorbing "tower 22 dallas" queries (22 impr @ 57–67) for a different entity | Metadata names it precisely; Tower 22 logged for investigation |
| Victory Park Terrace | 37 | Thin data (no dues, no rules) | Metadata; enrichment is data-acquisition work, queued |
| Turtle Creek (district) | 71–81 | "turtle creek condos" intent is transactional; we have no listings | Accept: hub serves research intent; no fabricated inventory |
| Uptown/Victory Park | 26 | District page competing with portal category pages | Stripe already roll-based; no further action |
| The House | 36–58 | Class C (Victory Park brand building) | Metadata + comparables |

## CTA / conversion review (Phase 9) — compliance decision
Dallas Towers is publisher-mode: "independent building research… no listings,
no pay-for-placement," and no brokerage services are offered. The brief's
buyer-consultation / seller-valuation CTAs would imply services that do not
exist (Phase 11 prohibits implying affiliation). **Retained and verified
instead:** the existing intent-matched capture — per-building report requests
(`building-report`), correction/update submissions (`building-update`),
registry updates — with honeypot, consent framing, per-building/source hidden
fields, and first-touch landing/referrer/UTM attribution (added Aug 24).
If brokerage representation launches, CTAs can be upgraded then.

## Dallas vs Fort Worth scope (Phase 10)
20 FW building files + downtown-fort-worth district + fort-worth hub; FW is a
clearly-labeled top-level nav item, not mixed into Dallas hubs; brand already
claims DFW ("Dallas Towers — The DFW High-Rise & Condo Guide"), and the FW
pages carried early impressions (Art House, Lone Star, The Tower FW queries).
**Recommendation: remain one property with explicit DFW positioning** —
Dallas-first brand, clearly-sectioned Fort Worth registry. FW SERPs are even
softer than Dallas ones; splitting the domain would fork authority for no
gain. Migration to a separate domain remains a user decision; nothing moved.

## Work completed this sprint
1. **Metadata**: all 89 building descriptions rewritten from the canonical
   dataset (era, roll accounts, median sf, assessed median where they fit) —
   before/after table in `metadata-before-after.csv`; og:description synced;
   duplicate-description validator added. Titles left unchanged (already
   entity-aligned "Building Condos — District, Dallas | Dallas Towers");
   changing them on ranking pages failed the "objectively weak" test.
2. **Comparables propagation**: the computed comparable-buildings module
   (district → roll value band → era → form, method disclosed) replaced the
   generic "Neighbors on file" block on the remaining 78 building pages —
   every building page now links to genuinely comparable towers.
3. **Katy Trail cluster**: hub gained The Terminal (card + regenerated
   8-building certified-roll table + count fix) and a **Travis vs. Terminal**
   comparison section (roll-sourced: 2000 mid-rise, 52 accounts, median
   1,608 sf @ $445/sf assessed vs 2022 loft conversion, 16 accounts, median
   3,185 sf @ $1,403/sf). Corridor buildings' comparables sections now link
   back to the hub. New comparisons beyond this: none — no demonstrated query
   demand yet (zero comparison queries in GSC).
4. **New pages created: 0** (per the brief's own thin-page prohibition; the
   hub upgrade covers the cluster need without new URLs).

## Post-deploy Search Console actions
1. Re-submit sitemap (unchanged URLs, refreshed content) — optional.
2. URL Inspection → Request indexing: katy-trail-condos.html,
   the-terminal-at-katy-trail.html, the-travis-at-katy-trail.html.
3. At +14d and +30d: check alternate-URL count in Coverage (should trend to
   zero as 301s digest), page-one CTR vs the 1.25% baseline, whether Park
   Highlander / Rosewood / Belvedere / 2011 Cedar Springs draw first clicks,
   whether Knox / 588 / Park Plaza / Colonnade hold or enter top ten, and
   Bleu Ciel's position band.

## Remaining risks
- Redirect digestion may suppress impressions another 1–2 weeks (expected).
- No holdout cohort remains; attribution of gains to specific changes is now
  weaker by design (owner directive).
- Descriptions are deterministic; a few trimmed variants drop the assessed
  clause for length — cosmetic only.

## Prioritized next publication queue (after +30d readout)
1. Tarrant certified-roll ingestion (unlocks 20 FW files' economics).
2. HOA dues verification for Renaissance, Twenty-One, Vendome (research queue).
3. Metadata-only floor-plan records for the Katy Trail + winner cohort.
4. "Tower 22 Dallas" entity identification (22 impressions of unmet demand).
5. Only then: new building pages that clear the thin-file threshold.
