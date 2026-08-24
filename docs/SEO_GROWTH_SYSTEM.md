# West FW Living — SEO Growth System (operating specification)

Established 2026-08-24. This is the operating spec for the closed-loop local-SEO system.
Future sessions: read this, then `editorial/DAILY_RUN.md` (publishing mechanics), then the
latest report under `reports/seo/`. The loop this document institutionalizes:

**Publish → Observe GSC → Identify emerging winners → Enrich → Interlink → Expand cluster →
Improve SERP presentation → Measure → Repeat.**

The business goal is qualified West Fort Worth / Aledo-corridor real-estate opportunities from
organic search — not pageviews. Effort goes preferentially to pages Google is already showing
signs of wanting to rank.

---

## 1 · Current architecture (audited 2026-08-24)

| Layer | Reality |
| --- | --- |
| Framework | None. Plain static HTML, ~306 pages, published from the **repository root** (`netlify.toml`: `publish="."`). No package.json; Python is the tooling language. |
| Page generation | Hybrid: ~298 hand-authored legacy pages + `gen/pages_*.py` modules rendered by `gen/build.py` using `gen/common.py` helpers (`page()`, `lead_form()`, `article_ld()`, `faq_ld()`, `_url()`). Never hand-edit generated pages. |
| Normalization + gates | `scripts/apply_standing_fixes.py` is **always the final build step**. Idempotent. Fixes nav (10-link EN / 8-link ES spec), canonicals, internal link forms, hreflang, context-aware lead-form fields; derives `sitemap.xml` fresh from disk. Seven gates; exits nonzero on failure. |
| URL/canonical policy | **Extensionless is canonical** (`/specials`, not `/specials.html`) because Netlify Pretty URLs rewrites every rendered `<a href="x.html">` platform-side. Never flip this (see DAILY_RUN.md "Netlify platform behavior"). Directory indexes keep trailing slash. |
| Routing | Filesystem. Netlify serves `/x`, `/x.html`, `/dir/` interchangeably — the reason canonical discipline matters. |
| Metadata / schema | Generated pages: full head + Article/FAQPage JSON-LD via helpers. Legacy pages vary; canonicals were backfilled site-wide 2026-08-18. FAQ rich results were retired by Google 2026-05-07 — FAQPage markup is kept for comprehension only, never as a SERP-feature play. |
| Sitemap / robots | `sitemap.xml` derived from disk every build (lastmod from git). `robots.txt`: allow all + sitemap pointer. `llms.txt` exists (update cadence: monthly-ish). |
| hreflang | EN↔ES bidirectional where mirrors exist (~65 ES pages), gated (`hreflang-assert`), resolved by file so URL spellings compare equal. |
| Internal links | Hub-and-spoke; new pages wire reciprocal hub links via `RECIPROCAL` in `gen/build.py` (idempotent). Audited by `seo_engine.py linkaudit`. |
| Lead capture | Hardened FormSubmit forms (hashed endpoint, honeypot, consent + timestamp) via `lead_form()`. Hidden fields capture **utm_source/medium/campaign/term/content, referrer, landing_page, page_url**; `_subject` encodes the originating path ("WFL — /path"). Three date-field contexts: `lease_end` (renting), `sell_timeline` (selling), `move_date` (else) — gated. |
| Analytics | **None wired.** CSP permits GA4/GTM but no tag is installed. GSC is the measurement system of record. |
| Search Console | Manual CSV/ZIP exports, ingested by the engine below. No API integration (would need credentials — candidate future upgrade). |
| Deploy | Netlify connector → `npx @netlify/mcp` from repo root; **push to GitHub before deploying** (deploys source from the pushed branch); verify the deploy's own permalink before trusting production. IndexNow auto-pings the sitemap on deploy; targeted pings for changed URLs. |
| Editorial system | `editorial/DAILY_RUN.md` (runbook), `EDITORIAL_CALENDAR.md` (scored backlog), `AUDIT_LOG.md` (append-only run records), `staleness-scan.md`. One substantial item/day, never filler. |

## 2 · Current SEO workflow (pre-system)

Daily cycle picked from a hand-scored backlog balanced across clusters; verification-first
research; hub/reciprocal linking; deploy; IndexNow. **Weakness: selection was editorial
judgment only — no feedback from what Google is actually ranking.** Publish → wait.

## 3 · Identified weaknesses (from the 2026-08-23 GSC data + audits)

1. **No feedback loop** (fixed by this system): the strongest page (Lockheed, 285 imp) was
   built pre-system and never revisited.
2. **Title/intent mismatch on the #1 opportunity**: page titled "Where to Live Near Lockheed
   Martin…" while ~140 impressions of queries say "apartments near lockheed martin…" — CTR
   0.35% at position ~10.7.
3. **URL-form splits still settling**: ~14 pages report impressions under both `.html` and
   extensionless forms (canonical fix deployed 08-18; GSC needs recrawl time). Engine merges
   forms before analysis so decisions aren't made on split data.
4. **25 orphan pages** unreachable from the homepage link graph — including
   `rentals/apartments-76108.html` (the Lockheed ZIP), several EN/ES guides.
5. **Commodity-content gravity**: largest query classes by volume are generic national
   (credit-score-to-rent 99 imp @ pos 68; closing-costs @ ~89; renters-insurance @ ~82) —
   position ~70-100 means Google is testing, not ranking. Low intent, low priority.
6. **Hidden local winners under-supported**: comparison pages at positions 2–8.5 on 1-12
   impressions; `data/property-tax` at ~8; private-schools page at 25 with tuition queries
   (`trinity valley school` at 3.25) — thin internal linking into all of them.
7. No analytics beyond GSC; lead attribution exists in form payloads but closings can't yet be
   joined back (manual step for the operator).

## 4 · The system

### Components
- **`scripts/seo_engine.py`** (stdlib-only) — subcommands:
  - `ingest <zip|dir> [--date]` → normalized snapshot in `data/gsc/YYYY-MM-DD/`
    (pages/queries/chart/devices/countries/search_appearance/filters). **Never overwrites**
    an existing snapshot. Accepts the GSC ZIP directly.
  - `report [--snapshot] [--prev]` → merges URL forms, tiers pages, scores intent, flags CTR
    gaps and cannibalization, computes deltas vs the prior snapshot, emits the weighted
    opportunity queue: `reports/seo/<snap>-opportunities.{md,json}` (dashboard included).
  - `linkaudit` → orphans, contextual-inbound counts (nav/footer excluded), heaviest
    outbound, crawl depth ≥4, broken links → `reports/seo/linkaudit-<date>.{md,json}`.
  - `log-event --url --reason --change [--kinds]` → appends to `data/seo/events.jsonl`
    with before-metrics from the latest snapshot (§8).
- **`data/seo/config.json`** — tunable weights, allocation percentages, priority clusters,
  expected-CTR curve. Edit there, not in code.
- **`data/communities.json`** — structured local data (§7 of the build brief): null-tolerant
  per-community records with provenance; the moat layer that powers comparison/neighborhood
  pages and future tools.

### Commands (the two you'll actually run)
```
python3 scripts/seo_engine.py ingest ~/Downloads/westfwliving.com-Performance-on-Search-<date>.zip
python3 scripts/seo_engine.py report          # + linkaudit monthly
```

### Known data limitations (do not over-read)
- GSC CSV exports do **not** pair queries with pages; per-page "top queries" in reports are a
  slug-token heuristic, labeled as such. (API integration would fix this.)
- Each export is a cumulative last-3-months window; deltas between snapshots are
  window-over-window, not day-over-day.
- At today's volume (6 clicks) CTR differences are noise; position and impressions carry the
  signal. **Never react to samples this small with rewrites of working pages.**

## 5 · Page-prioritization rules

Tier by merged average position (evidence floor: flag `low-evidence` under 3 impressions):

| Tier | Position | Posture |
| --- | --- | --- |
| A | 1–5 | Defend/monetize: freshness, conversion, contextual links in; **no rewrites** |
| B | 6–15 | **Push hardest**: satisfy every ranking query, deepen, interlink, fix titles |
| C | 16–30 | Selective: only where impressions or intent justify |
| D | >30 | Observe; let content season; revisit on impression growth |

Opportunity score (weights in config): position-opportunity (peaks ~9) ×3 · log-impressions
×2 · commercial intent ×3 · CTR-gap ×2 · priority-cluster ×1.5 · link-deficit ×1 ·
low-evidence −1. A #9 local-commercial page outranks a #45 generic-volume page by design.

**Commercial-intent rubric (0–3)** — scored on queries and slugs:
very-high (3): community/subdivision + housing, neighborhood comparisons, moving-to/relocation,
property tax for a place, builder/new-construction, ISD+housing, commute+housing, Lockheed/NAS
JRB housing. high (2): cost-of-living, HOA/PID/MUD, boundaries, price bands, local
apartments-near. medium (1): local lifestyle/schools without housing intent. low (0): generic
national renter/mortgage content. Low-intent pages that earn authority are kept, not deleted —
but new publishing skews high-intent local.

## 6 · Adaptive publishing allocation

The daily cycle's SELECT step now reads the latest opportunity queue first. Target mix over
any rolling ~2 weeks (configurable in `data/seo/config.json → allocation`):
35% expand demonstrated winners + their clusters · 30% improve pages ranking 6–20 ·
20% new high-intent local topics · 10% maintain factual pages · 5% exploratory.
(Rebalanced 2026-08-24: optimization of existing assets now outweighs net-new publishing —
"concentrate authority before expanding surface area." The weekly
`python3 scripts/seo_engine.py reinforce` report recommends one action per evidenced page,
and its default action is deliberately *leave alone*.)

Before any new page, answer the seven-question gate (existing intent coverage? cannibalization?
distinct intent? locally relevant? genuine information? commercial cluster? linkable?). Any
"no" → don't create it. This is recorded per page in the audit log.

## 7 · Content-quality safeguards (standing, enforced)

Inherited and kept: never invent prices/rents/fees/taxes/assignments/quotes; verify from the
source hierarchy; visible verified dates; publisher voice, email capture only, no lender
placements; safeguarded categories draft-and-flag (see DAILY_RUN.md). Added by this system:
no keyword-permutation pages (the cannibalization checks in `report` + the seven-question
gate); one intent = one page; hub-and-spoke over variants; prefer datasets/comparisons/
calculators/original synthesis over article volume. `data/communities.json` values require
`source` + `verified` per record; unknown = null, never guessed.

## 8 · Measurement methodology

- **Snapshots**: every GSC export ingested to `data/gsc/YYYY-MM-DD/`, kept forever.
- **Events**: every meaningful SEO change logged to `data/seo/events.jsonl` (URL, date,
  reason, GSC evidence, change kinds, before-metrics). After 7/28/90 days, fill
  `after_checkpoints` from the then-current snapshot (compare same-URL merged metrics).
  Small-sample discipline: no conclusions from <50 impressions or <14 days.
- **Dashboard**: the report's Dashboard section (impressions, clicks, CTR, tier mix,
  query-class mix, risers/fallers once ≥2 full snapshots exist). Content metrics come from
  the editorial calendar/audit log; lead attribution from form `_subject` + UTM payloads.
- Business joining (lead → closing) is manual for the operator: leads arrive with
  originating path + UTM; keep them.

## 9 · Lockheed cluster (proof-of-concept, built 2026-08-24)

Hub: `/guides/apartments-near-lockheed-martin-fort-worth` (285 imp @ 10.7 — the site's
strongest signal; renter-primary intent, retitled to match the dominant "apartments near
lockheed martin" queries). Spokes: `/guides/buying-a-home-near-lockheed-martin-fort-worth`
(buyer intent, new) · `/guides/apartments-near-nas-jrb-fort-worth` (military neighbor) ·
`/guides/living-in-benbrook` · `/areas/white-settlement` · complex field notes
(`/complexes/westpoint-at-scenic-vista`, `/complexes/chapel-creek-cottages`, Willow Park trio)
· commute pages · `/rentals/apartments-76108` (de-orphaned). ES mirrors both hub and new
spoke. Do **not** add per-suburb "X to Lockheed commute" permutation pages until queries for
them actually appear in GSC — the pocket table already covers the intent.

## 10 · Standing don'ts

- Don't rewrite Tier-A pages chasing marginal gains; don't churn URLs that have impressions.
- Don't flip the canonical policy (§1). Don't trust local/GitHub state as proof of deploy —
  verify the deploy permalink. Don't submit non-live URLs to IndexNow.
- Don't create ES mirrors for content with no ES-cluster precedent, and never breadcrumb-only
  cross-language links (visible in-body links, verified by rendered screenshot).
- Don't treat the query-page heuristic as ground truth.
