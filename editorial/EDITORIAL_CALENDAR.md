# West FW Living — Rolling 90-Day Editorial Calendar

Window: **2026-08-16 → 2026-11-14**. One substantial item per cycle; utility gates every slot.
Update this file each run: mark shipped items LIVE, re-score the backlog, keep cluster balance.

Legend — Status: `LIVE` shipped · `NEXT` queued · `IDEA` backlog · `HOLD` needs review or a
source · `UPDATE` maintenance pass · `REVIEW` safeguarded, needs a human.
Traffic / Txn: H / M / L.

Clusters: Buyers · Sellers · Renters · Relocation · Neighborhoods · Schools · Community ·
Military/BAH · Data & Tools.

## Shipped

Legend note: an item is only marked `LIVE` once the URL returns 200 in production. An item that
is authored and green but undeployed is `BUILT`.

| Date | Topic | Cluster | Audience | Target query | Src | Traffic | Txn | Status | Links |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | **September month-roll**: all 11 tracked communities re-verified (AL price-verified pages + listings + westpointtx.com/specials); Concession Index 7.5→4.0 core-4, expanded 11-community index debuts at 4.4; Rent Report No. 2 authored (`/rent-report/september-2026` + Sept chart SVG); data engine rolled (verified 2026-09-03, refresh due 2026-10-01; unverified floor plans dropped, not carried); specials EN+ES, all 11 complex pages, and sitewide stale-claim sweep (6–8-wks / August rents) updated; August report + Willow Park guide marked archive | Renters / Data & Tools | Renters, journalists citing the Index | "fort worth apartment specials", "willow park apartments free rent" | Verified (per-complex source list in AUDIT_LOG 2026-09-03) | H | H | LIVE (deploy 6a99be6b; builder-report 2026-09 deferred — no verifiable new builder packages this cycle, August edition still linked as latest) | hub cards guides/ + es/guias/ + rent-report/ index; sitewide footer → September |
| 2026-09-02 | **2026 adoption watch** on the homestead-exemption file: Aledo ISD adopted its 2026–27 rate ($1.1775, −$0.0167, eighth straight cut) on 2026-08-24; new exemption arithmetic ($1,649 / $2,355) added EN+ES; 2025 table retained as the current-bill basis; other three districts flagged not-yet-adopted | Buyers / Data & Tools | Owners, buyers running tax math | "aledo isd tax rate 2026", "texas homestead exemption 2026 amount" | Verified (aledoisd.org district news, 2026-09-02) | H | H | LIVE `/buy/homestead-exemption` + ES `/es/comprar/exencion-homestead` (maintenance update, backlog #2 first tranche) | unchanged (existing hub/reciprocal set) |
| 2026-08-24 | Buying a home near Lockheed Martin: the west-side ladder (four-pocket table: published bands × TEA 2026 × shift-honest drives) + Lockheed hub retitle/enrichment + sitewide de-orphaning pass | Buyers / Commutes | Plant hires & employees stepping up; dual-income west-side households | "buying a home near lockheed martin fort worth" (cluster spoke off the site's #1 GSC signal, 285 imp) | Verified (all bands/ratings from on-site verified files) | H | H | LIVE `/guides/buying-a-home-near-lockheed-martin-fort-worth` + ES `/es/guias/comprar-casa-cerca-de-lockheed-martin-fort-worth` (deploy 6a8bc23f, verified 200 in production 2026-08-24) | Lockheed hub (both directions), guides hub + es/guias hub cards, sell-side files ×4, homestead, rent-vs-buy, rent-or-buy WS/WP (de-orphaned), TEA page, VA loans, jrb-noise |
| 2026-08-23 | Seller net-proceeds napkin ($2,509 TDI title premium at $450K, $0 transfer tax, proration mechanics, negotiated blanks) | Sellers | Move-up sellers; owners comparing offers | "cost to sell a house texas" | Verified (TDI 2026 schedule + TX constitutional ban; example in published Willow Park band) | M | H | LIVE `/sell/net-proceeds` + ES `/es/vender/ganancias-netas` | sell hub (reciprocal card), es/vender hub, capital-gains (in-body), sell-before-buying, equity-report, home-value, homestead-exemption |
| 2026-08-22 | Homestead exemption in dollars, district by district ($140K × adopted 2025 ISD rates; Prop 13/11; filing mechanics; 10% cap) | Buyers | New buyers, 65+/disabled owners, renters running buy math | "texas homestead exemption 2026 amount" | Verified (Comptroller framework + first-party ISD adoptions + Tarrant TnT DB) | H | H | LIVE `/buy/homestead-exemption` + ES `/es/comprar/exencion-homestead` | buy hub (reciprocal card), es/comprar hub, property-taxes-for-buyers, data/property-tax, calculator, rent-vs-buy, living-in-benbrook |
| 2026-08-21 | Living in Benbrook: the value play (published Benbrook-vs-Aledo bands, A-rated middle/high inside FWISD's C, lake/daily-life, decision layer) | Neighborhoods | Priced-out Aledo buyers; renters-first households | "is benbrook a good place to live" | Verified (on-site published bands summer 2026 + TEA 2026 file) | H | H | LIVE `/guides/living-in-benbrook` + ES `/es/guias/vivir-en-benbrook` | guides hub (reciprocal card), es/guias hub, areas/benbrook, tea-ratings-2026, living-in-aledo, living-in-walsh, compare/benbrook-vs-white-settlement |
| 2026-08-16 | 2026 TEA A–F ratings for every west-corridor district + campus (Aledo holds A 92; Weatherford C→B 80; Benbrook Middle/High B→A 90; FWISD C 77) | Schools | Buyers, renters & relocating families choosing by zone | "aledo isd rating 2026", "tea ratings west fort worth" | Verified (TEA release + TEA 2026 multi-year ratings file) | H | H | LIVE `/schools/tea-ratings-2026` + ES `/es/escuelas/calificaciones-tea-2026` (deployed 2026-08-18) | schools hub (reciprocal), willow-park-school-zones, aledo-isd, weatherford-isd, brock-isd, neighborhoods, relocate, buy, living-in-aledo, living-in-walsh |


## Backlog — scored, cluster-balanced (draw the daily slot from here, highest utility first)

| # | Topic | Cluster | Audience | Target query | Src status | Traffic | Txn | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | **Privacy policy + ES mirror** — linked from every lead-form consent checkbox sitewide; currently 404 | Trust/Legal | Everyone | — | Drafted, **safeguarded** | L | H | **REVIEW** (see AUDIT_LOG 2026-08-16) |
| 2 | 2026–27 property tax rates by city + ISD, re-verified against Tarrant & Parker appraisal districts | Data & Tools | Buyers, owners | "willow park property tax rate" | Aledo ISD adopted 08-24 ($1.1775) — shipped to homestead file 09-02; City of Weatherford proposed $0.392246 (council vote 09-08); WISD / FWISD / WSISD / cities / counties pending | H | H | NEXT (in progress — refresh `data/property-tax` + `buy/property-taxes-for-buyers` once the majority adopt) |
| 3 | Aledo ISD attendance-zone changes for the Walsh/Morningstar growth corridor | Schools | Buyers in new construction | "aledo isd boundary change" | Sourceable (Aledo ISD board agendas) | M | H | IDEA |
| 4 | What the homestead exemption is actually worth on a west-side house after Prop 13 | Buyers | New owners | "texas homestead exemption 2026 amount" | SHIPPED 2026-08-22 → /buy/homestead-exemption | H | H | LIVE |
| 5 | Seller's net-proceeds napkin for a $450K Willow Park sale | Sellers | Move-up sellers | "cost to sell a house texas" | SHIPPED 2026-08-23 → /sell/net-proceeds | M | H | LIVE |
| 6 | The I-30 vs I-20 commute decision, timed by corridor and hour | Relocation | Inbound commuters | "commute fort worth from aledo" | Have (commutes/) — needs a re-timing pass | H | M | UPDATE |
| 7 | Renters insurance after a hail year: what changed at renewal | Renters | All renters | "renters insurance texas hail deductible" | Sourceable (TDI) | M | L | IDEA — **demoted** (GSC 08-23: generic renter queries sit at pos 68–100 = Google testing, not ranking; existing insurance pages cover the intent) |
| 13 | **Private-school tuition, west corridor** — enrich `/schools/private-schools-west-fort-worth` with verified tuition/admissions data | Schools | Buyers weighing private vs Aledo ISD premium | "trinity valley school" (GSC pos 3.25!), "private schools fort worth tuition" | SHIPPED 2026-08-28 (exact FWCD + TVS 2026–27 tuition on page, verified 08-28) | M | H | LIVE |
| 14 | **Lockheed cluster round 2** — watch the retitle/spoke in the next GSC export; extend only where new queries appear (NO per-suburb commute permutations) | Buyers / Commutes | Plant workforce | per next export | GSC-gated | H | H | HOLD (next GSC ingest) |
| 15 | Comparison-page push — `/compare/willow-park-vs-hudson-oaks` (pos 2), `/compare/aledo-vs-weatherford` (pos 8.5): freshness pass + inbound links, no rewrites | Neighborhoods | Movers choosing between towns | already-ranking comparison queries | Have (data layer) | M | H | IDEA — Tier A/B defend-and-push |
| 8 | Benbrook as the value play — FWISD zoning, an A-rated middle/high, and the price gap to Aledo | Neighborhoods | Priced-out Aledo buyers | "is benbrook a good place to live" | SHIPPED 2026-08-21 → /guides/living-in-benbrook | H | H | LIVE |
| 9 | Weatherford College housing + the student-renter market | Renters | Students, parents | "weatherford college housing" | Have — needs refresh | M | L | UPDATE |
| 10 | Property tax protest walkthrough for Parker vs Tarrant (deadlines differ) | Data & Tools | Owners | "protest property taxes parker county" | Sourceable (PCAD, TAD) — May deadline | H | M | HOLD (spring) |
| 11 | BAH 2027 refresh for NAS JRB Fort Worth | Military/BAH | Military renters | "nas jrb fort worth bah 2027" | Scheduled (DTMO, mid-December) | M | M | HOLD (Dec) |
| 12 | Verified-date backfill across the 248 pages that lack one | Maintenance | — | — | Internal | — | — | UPDATE (fill any no-topic day) |

## Recurring / calendar anchors
- **TEA accountability ratings** — released mid-August. Next hard trigger: August 2027.
  Rebuild `/schools/tea-ratings-2026.html` from `gen/pages_schools_ratings.py` with the new
  cycle's spreadsheet; archive the outgoing edition.
- **Property tax rates** — taxing units adopt ~September; refresh `data/property-tax.html`
  and `buy/property-taxes-for-buyers.html` once adopted (see staleness-scan §1).
- **Monthly specials + rent report + builder report** — 1st of the month.
- **BAH** — DTMO cycle, mid-December.

## Balance check (keep the mix honest across any ~2-week span)
Schools · Buyers · Sellers · Renters · Relocation · Neighborhoods · Data. Do not ship two
near-duplicate pages in a row. All five core clusters now touched: Schools (08-16),
Neighborhoods (08-21), Buyers (08-22), **Sellers** (08-23), Buyers/Commutes (08-24, GSC-driven).
Selection now starts from the GSC opportunity queue (`reports/seo/`, see
`docs/SEO_GROWTH_SYSTEM.md`) — the calendar keeps the balance honest, the queue picks the work.
Month-roll shipped 09-03 (rent report + specials; builder report deferred for lack of verifiable
new packages — catch it when Walsh/corridor builders publish September numbers). Next: #2 (2026
property-tax rates — Weatherford council votes 09-08) as districts adopt; #6 (Relocation) is the
remaining balance gap; #14 Lockheed round 2 waits on the next GSC export.
