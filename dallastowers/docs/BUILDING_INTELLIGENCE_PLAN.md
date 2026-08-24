# Dallas Towers — Building Intelligence Plan

*Established 2026-08-24. Governing thesis: Dallas Towers is a building-intelligence
database that happens to rank in search, not an SEO content site. One authoritative
building file is worth more than dozens of generic articles.*

## 1. Existing architecture (as found)

**Stack.** Plain static HTML, one page per building, no framework, no build step.
Hosted on Netlify (project `dallastowers`, site `d42e0b99-e6d2-4d3b-9db3-5671ac087727`),
deployed by zip upload — the site had **no version control** before this pass; this
repository directory (`dallastowers/site/`) is now the canonical deployable source.

**Routing.** Flat: `/<building-slug>.html` for the 89 building files (Netlify also
serves extensionless variants; every page declares a canonical to the `.html` URL).
Hubs: `/dallas.html`, `/fort-worth.html`, `/buildings.html` (full registry + client-side
search), `/neighborhoods.html` + district pages (`/turtle-creek.html`,
`/uptown-victory-park.html`, `/downtown-fort-worth.html`, …), `/collections.html` +
9 collection pages, `/market-data.html`, `/open-data.html`, `/new-developments.html`,
`/tower-report-q3-2026.html`, editorial + utility pages. 120 sitemap URLs.

**Data model.** A single dataset, `site/dallastowers-data.json` (CC BY 4.0,
also the public open-data download): 89 building records with
`name, city (DAL|FW|BEY), hood, addr, era, fl (floors), un (units), type, conf (v|p)`,
plus optional `dues` ($/sf/mo, 15 buildings), `psf` (legacy — see §4), and
`county_2026` (61 buildings): Dallas CAD certified-roll aggregates —
`acct, ooc_pct, sf_min/med/max, yr_mode, bed_mix, bath_mix, val_med, psf_med,
hs_pct, t12, t24, latest_deed, fp_pct`.

**Appraisal ingestion.** County fields are batch aggregates of Dallas CAD 2026
certified-roll unit accounts (per the dataset's own notes). There is no in-repo
ingestion pipeline; ingestion happens upstream and lands as `county_2026` blobs.
Tarrant County (TAD) has not been ingested: **0 of 20 Fort Worth buildings carry
county data.**

**Floor plans.** ~8 buildings have independently drawn schematic SVGs
(`site/img/*-plan.svg`). No structured floor-plan/stack records exist yet.

**HOA fields.** `dues` ($/sf/mo) on 15 buildings, rendered in prose and FAQ blocks.
No effective dates, no per-unit variation, no history, no included-services data.

**Documents.** `guide-documents.html` teaches buyers what to request; building
pages reference document categories. No per-building document inventory exists.

**Comparison.** `compare.html` is a client-side tool over the JSON dataset.
No static pairwise comparison URLs (correct — keep it that way).

**Structured data.** Organization + WebSite JSON-LD site-wide; Article JSON-LD on
verify pages; Dataset JSON-LD on `/open-data.html` (added 2026-08-21). No fabricated
ratings/reviews/prices anywhere.

**Spanish.** None on this property (the sister property westfwliving.com carries ES).

**Lead capture.** Netlify Forms: `registry-updates` (site-wide), `building-report`
and `building-update` (building pages), with hidden `building`/`source` fields and a
`bot-field` honeypot. This pass adds `landing_url`, `referrer`, and UTM capture.

**Analytics.** GA4 `G-VLBFHWJ3NX` — embedded in generated pages *and* injected by
Netlify snippet injection (a known pre-existing double-load; see §5).

**Publishing automation.** None before this pass. Now: `scripts/validate-site.py`
must pass before any deploy; deploys are zip uploads of `site/` to the Netlify site.

## 2. Current data coverage (actual repository values, 2026-08-24)

| Segment | Files | Verified (`conf=v`) | Partial (`conf=p`) | County roll |
| --- | --- | --- | --- | --- |
| Dallas | 66 | 63 | 3 | 59 |
| Fort Worth | 20 | 13 | 7 | 0 |
| Beyond DFW core | 3 | 2 | 1 | 2 |
| **Total** | **89** | **78** | **11** | **61** |

Field coverage across 89 records: address 80 (9 placeholders), era 89, floors 50,
units 78, HOA dues 15, county economics 61, floor-plan schematics ≈8.
Full per-building detail: `reports/building-coverage/`.

## 3. Missing-data patterns

1. **Tarrant County roll** — the single largest gap: every FW building lacks
   assessed values, owner-occupancy proxy, and transfer tempo.
2. **Floor counts** — missing on 39 of 89 (mostly mid-rises and conversions).
3. **HOA dues** — verified on only 15 of 89; no effective dates or history.
4. **Rules** (leasing, pets, minimum term, STR) — structured data absent site-wide;
   only narrative mentions on a handful of files.
5. **Addresses** — 9 buildings carry a placeholder address (core identity gap).
6. **Floor plans/stacks** — no structured records; 8 schematics only.
7. **Documents** — no per-building inventory of declaration/bylaws/budget status.

## 4. Changes implemented in this pass (2026-08-24)

1. **Value-semantics repair (hard requirement).** Texas is a non-disclosure state,
   and the site said so — while 13 building pages simultaneously published
   unsourced "closed-sale tracking ~$X/sf recent avg" figures, Museum Tower carried
   a table of specific per-unit transaction prices, the homepage claimed
   "real sales data" / "closed-sale data", and the About sources card claimed
   "Closed sale prices … from recorded instruments" (impossible from TX deeds).
   All removed/rewritten: the 88 "Sales & tracking" sections are now
   "Transfers & tracking" built strictly from verified deed-transfer tempo
   (`t12`, `t24`, `latest_deed`) with an explicit non-disclosure statement; no
   dollar sale figures remain anywhere. The legacy `psf` field is retired from
   display and marked deprecated in the dataset docs.
2. **Assessed labeling.** Registry/collection cards rendered bare "$N/sf" derived
   from certified-roll medians; all such cards now read "assessed $N/sf".
   Alert-email copy "every closed sale" → "every recorded transfer".
3. **Completeness claim softened.** "Every tower. Every floor plan. One guide." and
   "every named condominium building in the Metroplex" could not be substantiated
   by 89 files and ≈8 floor-plan schematics. Replaced with registry language
   consistent with the site's voice; the 89-file count is stated plainly.
4. **Verification states + provenance architecture** formalized in
   `schemas/building.schema.json` (see §6 of that file) — including strict
   assessed-vs-transaction value types.
5. **Production validators** (`scripts/validate-site.py`): value-semantics guard,
   placeholder guard, internal-link check, sitemap consistency, canonical/noindex
   checks, JSON-LD validity, duplicate titles. Deploy is blocked on failure.
6. **Lead attribution**: all Netlify forms now carry `landing_url`, `referrer`,
   `utm_source/medium/campaign` hidden fields populated client-side.
7. **Coverage report + research queue** generated under `reports/`.
8. **Version control**: full site source committed to git for the first time.

## 5. Deliberately NOT implemented

- **No new building pages, articles, or comparison URLs.** Depth over breadth.
- **No visible completeness meter** on building pages: with rules/plans/documents
  fields still absent from the dataset, any percentage would imply false precision.
  Revisit when the structured fields exist to score against. The existing
  voice-level pattern ("pending the next verification pass") stands in.
- **No populated schema fields without sources** — the canonical schema is an
  architecture target; no field was filled by inference. Unknown stays unknown.
- **No Tarrant/TAD ingestion** — requires upstream roll processing; queued as the
  top research priority rather than approximated.
- **No GA double-load fix** — the duplicated GA tag (embedded + Netlify snippet
  injection) predates this pass; fixing it means choosing which copy survives,
  an owner decision (recommended: turn off snippet injection).
- **No geographic expansion, no district restructuring, no slug changes,
  no mass metadata rewrites.** All 120 indexed URLs unchanged.
- **IDX-SLOT comments retained** — hidden integration markers for a planned
  November inventory integration; not user-visible, whitelisted in the validator.

## 6. Future data acquisition priorities

Ranked queue with sources: `reports/research-queue/BUILDING_RESEARCH_PRIORITY.md`.
Strategic order: (1) Tarrant certified roll for all 20 FW buildings;
(2) HOA dues with effective dates for the high-value Dallas towers;
(3) leasing/pet/STR rules from declarations for the top-traffic files;
(4) missing floor counts and the 9 placeholder addresses;
(5) structured floor-plan/stack records for buildings with verified plan sources.
