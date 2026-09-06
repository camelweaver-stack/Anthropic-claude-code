# Floor-plan opportunity assessment — 2026-08-28

## Demand signal
"[building] floor plans" queries are served almost exclusively by official
building sites (Museum Tower's own floor-plans pages dominate its SERP) and
are simply **absent** for the older non-official-site buildings — HAR/brokerage
pages describe bed/bath mixes in prose at best. For A/B-class buildings the
floor-plan SERP is effectively empty. This is a genuine moat candidate: high
buyer value, structurally hard for portals (listing-oriented) to backfill.

## Rights position (hard constraints)
- No copying developer/MLS floor-plan artwork without license. No tracing.
- Legitimate paths: owner/HOA-provided documents; developer material with
  permission; independently drawn schematics from verifiable, non-copyrightable
  facts (unit dimensions from public records/measurement), labeled
  "schematic — not to scale"; or **metadata-only plan records** (no image).
- The schema already supports this: floor_plans[] with rights_class
  {licensed_official, public_document, independent_schematic, metadata_only,
  unknown} — no image renders unless rights-clean.

## Current assets
7 independently drawn plan schematics (site/img/*-plan.svg) + certified-roll
size/bed-mix distributions for 61 buildings (already rendered on Museum Tower
as the verified alternative to invented plan tables).

## Recommended sequence (post-measurement)
1. Metadata-only plan records for the intervention cohort (unit types, sf
   ranges, bed/bath from roll bed-mix + sourced listings) — no artwork needed.
2. Independent schematics only where measurements can be verified.
3. A "/floor-plans" index per building only when ≥3 verified plan records
   exist (thin-file guard applies).
Do not build plan pages from inference; the roll's size distribution is the
honest substitute until real plan sources are acquired.
