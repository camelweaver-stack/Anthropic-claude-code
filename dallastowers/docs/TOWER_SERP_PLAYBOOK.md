# Tower SERP Playbook

*What we know (2026-08-28) about ranking for individual Dallas residential
buildings. Evidence: first GSC cycle (unvalidated figures — see ledger §0),
live SERP research on 7 building queries, and the registry's own architecture.*

## What Google appears to reward on building queries
1. **Entity clarity** — page unambiguously about one physical building: name +
   address + neighborhood in title/H1/opening, one canonical URL, consistent
   internal anchors. Our pages already do this; it is likely why a 3-week-old
   domain got tested at positions 5–15 at all.
2. **Being the only substantive page** — winner SERPs are HAR templates + tiny
   brokerage directories. Google tests anything that looks deeper.
3. **Freshness-neutral reference format** — dated, sourced facts; no listing
   churn dependence.

## What weak ranking competitors commonly lack (verified)
HOA rigor (amounts with dates/sources), any public-record economics (assessed
medians, homestead share, transfer tempo — **nobody** in the local set has
this), building rules with provenance, comparables chosen on criteria,
disambiguation of renamed buildings.

## Required tower-page information (the definitive page)
Identity (name, aliases, address, district, type, era) → register strip →
county record (roll accounts, sizes, assessed medians, homestead proxy,
transfer tempo) → fees/dues with provenance state → rules as what-to-verify
until sourced → documents status → location/around-the-building → comparable
buildings (criteria-chosen) → FAQ answering the queries people actually type
([building] hoa/floor plans/pet policy/for sale).
Optional high-value: floor-plan/stack records (rights-clean), photography,
dues history, developer/architect where sourced.

## Aliases (entity resolution)
Searchers and portals use variant names. Verified examples: Travis at Katy
Trail = "Travis at Knox"; Park Highlander = former "Drexel Highlander";
"ArtHouse at So7"; "LoneStar Tower". Pattern: `alternateName` in the building
JSON-LD + one natural prose mention attributing the variant to listing
portals. Never keyword-stuff; never create duplicate pages for aliases.

## Metadata patterns
`<Building> Condos — <District>, <City> | Dallas Towers`; description names
the file's contents (HOA, floor plans, policies, taxes, transfers). Schema:
ApartmentComplex (+alternateName) + BreadcrumbList + FAQPage, all mirroring
visible content. Known caveat: numberOfAccommodationUnits currently carries
roll-account counts — fix to typed semantics before expanding schema.

## Internal relationships
District hub → building; building → comparable buildings (district, roll
value band, era, form — deterministic, labeled); collections as query-matched
lists. Avoid indiscriminate neighbor blocks (the old "Neighbors on file" was
one; replaced on the intervention cohort).

## When NOT to invest in a building SERP
Official developer/building site + active press cycle (Museum Tower, Bleu
Ciel, Knox/Auberge, Rosewood): keep the file excellent as reference and for
long-tail (hoa/rules/plans queries), but do not chase the head term.

## SERP barriers observed
HAR.com ranks on domain authority with template pages (beatable on content,
slowly); official sites are unbeatable on brand terms; new-development SERPs
are press-dominated until construction news fades.

## Expansion rule
A new building page must clear the thin-file threshold (schema), target an
A/B-class SERP, and have at least county-roll data. Improve what Google is
already testing before adding URLs.
