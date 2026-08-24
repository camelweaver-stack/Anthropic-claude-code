# North FW Living — Quality & Seasoning Plan

Date: 2026-08-24 · Scope: northfwliving.com quality/infrastructure pass followed by a deliberate 30–45 day seasoning period.
This is not a redesign, not a content-generation project, and not an instruction to chase early rankings.

---

## 1. Current architecture

**Origin note.** As of this pass, northfwliving.com had no version control: the site was generated offline and deployed to Netlify by manual zip upload (see `whereindfw` platform audit, F3). The first act of this pass was to mirror the live production deploy (`6a81fc72`, netlify project `northfwliving`, site id `d106e26e-05b2-4ef0-82f9-cd8a644a6590`) into this repository at `northfwliving/`, byte-for-byte, as commit `27efd4a`. That mirror is now the canonical source of the deployable site.

- **Framework:** fully static hand-authored/generated HTML. No build step. CSS is inlined per page; Google Fonts is the only external asset dependency. 7 licensed Wikimedia photos under `/assets/photos/`.
- **Routing:** directory URLs with trailing slash → `index.html`. 272 pages: 136 English + 136 Spanish mirror under `/es/`.
- **Homepage:** field-guide positioning for the Alliance corridor (Keller, Roanoke, Northlake, Justin, Haslet, Alliance–Presidio spine); market stats, three-doors cards, core-idea callout, latest-notes cards, early-list form.
- **Navigation:** single top nav (Renting / Buying / Builder Ledger / Neighborhoods / Employers / Schools / Selling / Relocate / Guides / Español) + four-column footer. Fully mirrored in Spanish.
- **Employers:** `/employers/` hub + 5 pages: Charles Schwab (Westlake), Fidelity (Westlake), Alliance logistics spine, BNSF, DFW Airport. Qualitative commute bands (short/moderate/longer) by deliberate policy — no fake-precise minute counts.
- **Neighborhoods/pockets:** `/neighborhoods/` + 11 pockets (Keller, Roanoke, Northlake, Justin, Haslet, Argyle, Trophy Club, Westlake, Heritage, Alliance, Golden Triangle). Each links employers hub, Builder Ledger, boundary guide, MUD/PID.
- **Schools:** `/schools/` + boundary guide, Keller ISD, Northwest ISD, Argyle ISD, Eagle Mountain-Saginaw ISD fact sheets, school-taxes, transfers guide. Explicit no-ranking policy on district quality.
- **MUD/PID:** `/buy/mud-pid-explained/` + `/tools/mud-pid-impact/` calculator.
- **Build-to-Rent:** `/renting/build-to-rent/` (+ ES mirror).
- **Builder Ledger:** `/builder-ledger/` — currently a *type-level* tracker (incentive types, honest ranges, verification paths) that deliberately publishes no per-builder claims between editions.
- **Data & Reports:** `/data/`; **Toolbox:** `/tools/` with 8 calculators (all client-side).
- **Relocation:** `/relocate/` + 6 sub-guides. **Buying/Renting/Selling:** full sections with city sub-pages.
- **Spanish:** complete 1:1 mirror under `/es/` (only slug divergence: `/privacy/` ↔ `/es/privacidad/`).
- **hreflang/canonicals:** every page carries a self-referential canonical and a 3-link cluster (en / es / x-default → EN). Verified sitewide by the new validator.
- **Metadata/structured data:** unique titles + meta descriptions; JSON-LD on every page (WebSite/Organization on homepages, BreadcrumbList on interior pages) — all blocks parse.
- **Lead capture:** one FormSubmit form per page (hashed endpoint, honeypot, consent checkbox, per-page `_subject` CTA id). This pass added first-touch UTM/referrer/landing-page attribution.
- **Sitemap/robots:** `sitemap.xml` (272 URLs, verified two-way against disk), permissive `robots.txt` with sitemap pointer.
- **Publishing/deployment:** manual zip → Netlify (project `northfwliving`). Now: repo → validators (`northfwliving-scripts/run_all_checks.sh`) → Netlify deploy of `northfwliving/`.

## 2. GSC baseline (export 2026-08-24, first impressions 2026-08-13)

Raw export preserved append-only at `northfwliving-data/gsc/2026-08-24/`. Cohort definitions in `northfwliving-data/gsc/cohorts.json`; report via `northfwliving-scripts/gsc_cohort_report.py`.

Sitewide: **24 pages with impressions · 137 impressions · 1 click · 43 distinct queries · 13.7 impressions/day over 10 active days.**

| Cohort page | Position | Impressions | Notes |
| --- | --- | --- | --- |
| /buy/mud-pid-explained/ | 69.77 | 44 | Highest discovery, ranking poorly — prime seasoning candidate |
| /guides/homestead-exemption/ | 80.25 | 16 | |
| /schools/ | 30.60 | 15 | |
| /schools/boundary-guide/ | 18.38 | 8 | Best-positioned EN content page |
| /schools/northwest-isd/ | 29.00 | 7 | "moving to northwest isd" (8 imp) |
| /neighborhoods/northlake/ | 49.88 | 8 | |
| /renting/build-to-rent/ | 64.75 | 4 | **First organic click** ("build to rent", pos 37) |
| /tools/net-effective-rent/ | 89.50 | 6 | |
| /es/renting/build-to-rent/ | 31.00 | 5 | ES outranking EN counterpart |
| /es/buy/mud-pid-explained/ | 5.75 | 4 | Strikingly favorable early ES test |
| /es/neighborhoods/ | 4.50 | 2 | |
| /es/buy/ | 2.00 | 1 | |
| /neighborhoods/ | 15.25 | 4 | |

No employer page received impressions yet; employer URLs join `cohorts.json` when they first appear.

## 3. Credibility issues found

1. **Universal mortgage shortcut** — "Your rent is already a mortgage payment. The only question is whose." and "every $850/month supports roughly $100,000 of house, taxes and insurance included" appeared as an unconditioned rule in 12 locations (homepage EN/ES, renter-to-owner EN/ES, first-time EN/ES, rent-vs-buy-by-pocket EN/ES, rent-vs-buy tool EN/ES, tools hub EN/ES).
2. **Unsupported firsthand-sounding claim** — "Fidelity … its own shift rhythms" on `/employers/` (EN+ES), with no supporting content anywhere.
3. **ES calculator emitting English output** — `/es/tools/rent-vs-buy/` printed results in English.
4. **`/es/privacidad/` had `lang="en"`**; **ES FAQ shared the EN FAQ's title** (duplicate titles across languages).
5. Placeholder scan (FIRST-HAND / FIELD NOTE / TODO / PLACEHOLDER / [INSERT / etc., case-insensitive, visible text): **clean** — no fabricated field notes or editorial leakage found in production HTML.
6. Reviewed but deliberately unchanged: "guaranteed return" in the homestead-exemption meta description (defensible — the exemption reliably reduces taxable value for qualifying homesteads, and the page is in the impression cohort).

## 4. Infrastructure changes made

- **Version control**: production mirror imported; all changes now diffable commits.
- **Credibility language corrections** (see §3, items 1–4). The $850/$100k example survives only as a *labeled modeled scenario* with explicit assumptions (≈6.5% 30-yr fixed, ~5% down, ~2.4% combined tax incl. MUD/PID, typical insurance; PMI/HOA/maintenance excluded and said so). Calculator page gained a stated-assumptions section.
- **Hard validators** (`northfwliving-scripts/`, all wired into `run_all_checks.sh`, all must pass before deploy):
  - `validate_credibility.py` — fails the build if placeholder/editorial/fake-firsthand copy reaches visible production HTML (Spanish-safe: uppercase-only `TODO:`/`FIXME` matching).
  - `validate_technical.py` — canonicals, hreflang clusters, lang attrs, unique titles, meta descriptions, noindex, internal link resolution, two-way sitemap check.
  - `validate_ledger_data.py` — Builder Ledger snapshot schema + provenance; rejects sample/fake-looking records.
  - `tests/test_validators.py` — 25 unit tests; fixtures generated in temp dirs at runtime so no test data can ever ship.
- **Provenance standard** — `northfwliving-data/PROVENANCE.md`: reusable envelope (`value/source/source_url/verified_date/effective_date/expiration_date/confidence/notes`); null beats a guess; nothing renders without source + verified_date; append-only history; no LLM-originated values.
- **Builder Ledger data architecture** — `northfwliving-data/builder-ledger/`: record schema (all incentive fields nullable), append-only dated snapshot directories, 2026-08-24 snapshot containing **zero records** (none verified yet; none invented), and `render_builder_ledger.py` which emits the public Builder/Community/Offer/Verified/Expires table **only** from provenanced records — with zero records it emits nothing and the page keeps its type-level table. No per-incentive URLs, no builder×month URLs, no archive pages.
- **Neighborhood schema** — `northfwliving-data/neighborhoods/schema.json` (provenance envelopes on every mutable field) + 11 stub records populated only with identity fields; every mutable value is null-by-policy.
- **GSC baseline + cohort tracker** (§2).
- **Employer decision pathways** — one contextual paragraph per employer page (EN+ES) linking boundary method, Builder Ledger, comparisons, two-badge guide, relocation. No new pages.
- **Lead attribution** — utm_*/referrer/landing_page/page_url hidden fields + first-touch sessionStorage capture on all 270 forms.

## 5. Pages deliberately left unchanged

- **All content of the impression cohort** (§2): MUD/PID EN, boundary guide, Northwest ISD, Northlake, schools hub, homestead guide, BTR EN, and every Spanish page — URLs, titles, headings, and body copy untouched (the only sitewide touch was invisible form-attribution markup).
- School fact sheets and transfers guide (already compliant: district vs campus distinction, address-specific boundaries, no quality rankings, verification prompts).
- The Builder Ledger public page (its type-level honesty is correct until verified records exist).
- All neighborhood, community, luxury, sell, relocate, and guide content not named in §3.
- No page added, no page removed, no URL changed, no title changed except the duplicate ES FAQ title fix.

## 6. Seasoning policy — 30–45 day strategic freeze (2026-08-24 → early/mid October)

**Allowed:** normal scheduled publishing cadence; verified Builder Ledger snapshot updates; factual corrections; data refreshes; bug fixes; provenance maintenance.

**Avoided until the checkpoint:** redesign; URL changes; mass title changes; mass content enrichment; Spanish expansion; new neighborhood pages; new employer pages; any MUD/PID rewrite or optimization; publication-volume increases.

The open experiment: *will Google's initial test pages migrate upward as the domain matures?* Nothing may obscure that experiment.

## 7. September/October measurement plan

At each future GSC export (recommended: ~2026-09-22 and ~2026-10-08, using the same "Last 3 months" web export), unzip into `northfwliving-data/gsc/<date>/` and run `python3 northfwliving-scripts/gsc_cohort_report.py` — it compares the same URLs, never sitewide averages.

Classification rules (directional, not statistical):

| Outcome | Signal (cohort positions) | Action |
| --- | --- | --- |
| **Strong maturation** | e.g. 18→top-10, 29→teens, 50→20s, 70→30s/40s while footprint grows | Continue seasoning; carefully replicate demonstrated winners |
| **Moderate maturation** | Some improve, others static | Reinforce only demonstrated winners |
| **Stagnation** | Impressions grow materially, positions flat | Selectively enrich pages Google repeatedly tests (MUD/PID first) |
| **Retraction** | Footprint/impressions materially decline | Reassess quality, architecture, topical fit |

Also track sitewide: pages with impressions (baseline 24), daily impressions (13.7), distinct queries (43), clicks (1).
