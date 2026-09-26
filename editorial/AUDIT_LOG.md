# West FW Living — Daily Audit Log

Append-only. Newest entry on top. One record per daily run. Template at the bottom.

---

## 2026-08-28 (second run) — Licensed photography sourcing — LIVE

- **Trigger:** Operator — "scrape sources for photography." Executed within standing rules:
  no competitor images, no copyrighted material, nothing presented as first-hand. Sourced
  four properly licensed images via the Wikimedia Commons API (visually verified before
  publishing; upload host rate-limited the proxy, worked around via the commons thumb.php
  endpoint): USAF Lockheed Fort Worth facility entrance (PD) → Lockheed apartments guide
  EN+ES, replacing the generic Stockyards photo; US Navy NAS JRB flightline panorama, 2008,
  date in caption (PD) → NAS JRB guide; Parker County Courthouse by Michael Barera
  (CC BY-SA 4.0, credited with linked license) → /compare/aledo-vs-weatherford; USACE
  Benbrook Lake aerial (PD) → /areas/benbrook, filling the slot where the placeholder was
  removed. Every image carries a figcaption credit. PHOTO_REQUIREMENTS.md updated (filled
  vs still-wanting-original-photography). Gates + production validator green; deploy
  **6a919635** verified live on all five pages including image bytes (200 image/jpeg) and
  attributions. Still wanted as original photography: complex exteriors, town entry markers,
  the I-30/I-20 seam.

---

## 2026-08-24 (fifth run) — Surgical correction: Olympus report + guard hardening — LIVE

- **Trigger:** Operator — live placeholder reported on /complexes/olympus-willow-park;
  three Lockheed assertions reported still present. Verify, fix, stop.
- **Finding:** live Olympus, source, and all six historical problem pages verified clean at
  time of investigation (0 prohibited hits). Olympus was removed in the same commit as
  Canvas/Westpoint (8a6f583, 12:16 UTC) and deployed with them at 12:24 UTC; the report
  matches pre-12:24 production or an immutable old deploy permalink, same as the earlier
  Canvas report. The three Lockheed claims were replaced in the fourth run; fragment scan
  ("plant-shift timing", "plant's stability", "lenders comfortable", "offer letters satisfy",
  "nearly everywhere") = zero production matches after this run.
- **Hardening anyway:** denylist gains unhyphenated variants (FIRST HAND FIELD NOTE,
  [FIRST HAND) + explicit [ADD PHOTO; fieldnotes content-state rule now build-enforced
  (non-verified record carrying text/photos fails placeholder-assert); test suite extended to
  14 violation classes across BOTH gates plus Tests E (planned+content must fail) and F
  (verified+content must pass) — all green. One analogous claim fixed:
  credit-score guide's "approved nearly everywhere on score alone" → per-property criteria
  framing.
- **Verify:** GATE PASSED ×8; deploy validator 310 files / 0 placeholder / 0 editorial
  matches (deploy dir = repo root per netlify.toml publish="."); linkaudit + sitemap gates
  green. Deploy **6a8c560e** through the validating build (commit 21cd16b). Live: all six
  URLs 200 / 0 placeholders; Lockheed live HTML: plant-shift 0, lender-comfort 0,
  offer-letter-everywhere 0, replacement language present ×3. Site enters structural
  stability; next intervention on new GSC evidence only.

---

## 2026-08-24 (fourth run) — Corrective pass: deploy-pipeline guard + claim tightening — LIVE

- **Trigger:** Operator — placeholder observed on live /complexes/canvas-at-willow-park;
  narrow corrective pass, then structural stability for GSC maturation.

### Root cause (why the placeholder survived "the previous cleanup")
The source purge worked; the failure was **timing plus an unenforced pipeline**. Placeholders
were removed from source at 12:16 UTC (commit 8a6f583) and reached production with deploy
6a8c3809 at 12:24 UTC — the day's first deploy (6a8bc23f, 04:02 UTC) predated the purge and
served placeholders all morning; old deploy permalinks serve them forever. Structurally, the
placeholder gate lived only in a *manually invoked* script; netlify.toml's build command ran
zero validation (`ping-indexnow.js || true`), so nothing in the deployment pipeline could
block dirty HTML. Current repo, current build, and current production scans: 0 hits (all
file types, both URL forms, apex + netlify subdomain).

### Fixes
1. **Deploy-time guard (cannot be skipped):** netlify.toml build command is now
   `node scripts/validate-production.js && (ping || true)` — the validator scans every HTML
   file in the publish tree against `scripts/prohibited-content.json` and exits nonzero →
   Netlify build FAILS → deploy blocked. First live run succeeded on deploy 6a8c4ce2.
2. **Single denylist config:** `scripts/prohibited-content.json` now feeds BOTH the deploy
   validator and the local placeholder-assert gate (no drift). Test suite extended: each of
   12 violation classes must fail *both* gates; 4 legitimate phrasings must pass — green.
3. **Markup bug found & fixed:** doubled `<h2>Shift math:<h2>` on the Lockheed guide (a
   reciprocal-block marker duplication from the 08-24 second run); build entry corrected so
   it cannot recur. No other doubled headings sitewide.
4. **Claim tightening (surgical; URLs/intents/headings preserved):**
   - Shift-commute: "assume plant-shift timing, friendlier than downtown rush" → estimate
     framing with test-your-route guidance (pocket-table note, shift-math paragraph, meta
     "shift-honest"→"estimated", EN+ES pages, both gen modules, guides-hub cards EN+ES).
   - Offer letters: "satisfy income verification nearly/essentially everywhere" → "vary by
     property — confirm before paying an application fee" (Lockheed EN+ES ×2 each incl.
     FAQ JSON-LD, family guide EN+ES). "most offices will slide a lease start" → "some".
   - Lender comfort: "the plant's stability makes lenders comfortable" / "aerospace
     stability helps on the mortgage side" → neutral discuss-documentation-with-your-lender
     guidance (Lockheed EN+ES FAQ + JSON-LD, buying-spoke module).

### Verify
GATE PASSED ×8 + dual-gate test suite; production validator: 310 files, 0 prohibited;
linkaudit unchanged (broken = 2 tracked privacy targets). Deploy **6a8c4ce2** (pushed first,
permalink verified) — first deploy through the validating build. Live checks: Canvas,
Westpoint, College Park, Chapel Creek, Lockheed guide all 200 with 0 prohibited strings;
corrected claims confirmed in live HTML; old formulations absent. Site now holds structurally
stable — next substantive intervention waits for new GSC evidence.

---

## 2026-08-24 (third run) — Credibility & provenance cleanup — LIVE

- **Trigger:** Operator — "clean, verify, strengthen, then stop changing things unnecessarily."
  No redesign, no expansion; site now seasons for GSC maturation.

### Findings + resolutions
1. **Explicit placeholders:** none found (08-24 second-run purge held; production scan clean).
2. **Simulated field-verification:** all 11 /commutes/ pages carried a "FIELD-CHECKED COMMUTE
   NOTES" eyebrow with no visits behind it → replaced with "COMMUTE NOTES · OFF-PEAK MAPPING
   ESTIMATES". (The pages' tables already used ranged off-peak estimates with a public-mapping
   source note and drive-it-yourself advice — the eyebrow was the only violation.)
3. **Unsupported claims:** family guide's "consistently the smoothest experience locals
   report" (unsupported sentiment) → removed; willow-crossing "we have seen $65 apps…" →
   "advertised fees vary across public listings (… appear on some)"; westpoint's "20-minute
   difference is roughly 160 hours a year" → assumptions made explicit (20 min × 2 × 5 days ×
   ~48 weeks ≈ 160 h, labeled an estimate).
4. **BAH page:** source note no longer leans on "republished by base-guide services" — DTMO
   named as the authoritative source, official rate-lookup linked, unlisted grades explicitly
   not estimated. Anchors UNCHANGED (DoD site returns 403 from build environment;
   `verified_against_primary: false` + operator note recorded in wfl-data.js provenance).
5. **Structured data bug:** 8 pages (sell/ + es/vender/ Aug-1 vintage) shipped JSON-LD with a
   single-quoted headline — invalid JSON, ignored by parsers → repaired, all blocks re-parse.
6. **Provenance:** wfl-data.js gained a provenance block (source/verified_date/refresh_due/
   confidence/scope) covering every mutable rental datapoint; canvas + willow-crossing pages
   gained the standard visible "verified from public listings July 31, 2026" line (all 11
   complexes now carry it). School language already met the "district area — verify campus"
   standard sitewide (audit found zero "will attend" claims).

### Guard hardened + tested
placeholder-assert denylist extended: field-checked/field-tested, "we visited/toured…",
"locals report", [FIELD NOTE/[PLACEHOLDER, bracketed editorial instructions. New test suite
`scripts/test_credibility_gate.py`: 12 violation classes must fail the build, 4 legitimate
phrasings (Spanish "todo:", reader-directed "you tour", ordinary brackets) must not — PASSED.

### Deliberately unchanged
Homepage (relocation-first hierarchy verified, no further correction needed), Lockheed
cluster (hub links all 18 target nodes, 8 inbound — no gaps, no new pages), all ranking URLs
(zero URL/intent changes; commute-eyebrow + provenance edits are cosmetic/credibility only),
publishing cadence (change-class rule added to DAILY_RUN instead).

### Verify
GATE PASSED ×8 + gate test; 310 pages / 306 sitemap URLs; no duplicate titles or
descriptions; all JSON-LD valid; named pages (homepage, 4 complexes, Lockheed guide,
commutes, BAH, family guide, /move/, /compare/) each: 1 title, 1 canonical, 0 placeholder
hits. **Deploy 6a8c42aa** (pushed first; permalink verified before production). Live
production scan: crawled all 306 sitemap URLs of the deployed site — 0 placeholder/first-hand
hits, all 200, single canonicals (4 transient proxy timeouts re-verified clean). IndexNow 200
for 24 changed URLs.

---

## 2026-08-24 (second run) — Authority concentration pass — LIVE

- **Trigger:** Operator — "concentrate authority before expanding surface area": credibility
  purge, relocation-first repositioning, Lockheed flagship funnel, winner reinforcement.
  Full findings + decisions in `docs/AUTHORITY_CONCENTRATION_PLAN.md`.

### Credibility purge (highest priority)
Removed literal placeholder text simulating in-person visits from **13 production URLs**
(all 11 /complexes/ pages + /areas/white-settlement + /areas/benbrook): `[FIRST-HAND FIELD
NOTE — added after an in-person visit.]` paragraphs and `FIELD PHOTO` slots. Nothing renders
where no genuine observation exists. New content-state model `data/fieldnotes.json`
(none|planned|verified; all currently none). New **placeholder-assert gate** in
apply_standing_fixes.py fails the build on any placeholder/visit-claim phrasing —
negative-tested. A site-wide sweep for subtler simulated-firsthand language found none.

### Repositioning + Lockheed flagship
Homepage retitled/reworked to relocation-decision-platform framing (renter content retained
as an explicit branch; no renter URL touched). New flagship hub
`/relocate/working-at-lockheed-martin-fort-worth` + ES mirror — broad relocation intent,
distinct from the renter hub (GSC #1) and buyer spoke; organizes rent/buy/commute/family/
military/decision paths from published data only. Wired: relocate hubs (EN/ES), military hub,
NAS JRB guide, both Lockheed guides, homepage journey grid.

### Authority concentration
Renter-to-buyer decision paths added on specials, deals, second-chance, rent-to-own,
apartments-76108 (soft, page-matched). Contextual links into tier-B winners: walsh→2
comparisons+tax page, living-in-aledo→2 comparisons+ISD file, olympus-four→willow-park-vs-
hudson-oaks, rent-or-buy-willow-park→same, aledo-isd→living-in-aledo+ISD-comparison,
weatherford-isd→ISD-comparison. New `seo_engine.py reinforce` weekly report (first run: 57
evidenced pages, 43 = leave alone). Allocation rebalanced to 35/30/20/10/5 — improvement now
outweighs net-new publishing. Dilution: tv.html + poster.html noindexed (display artifacts,
0 impressions); generic national guides retained + de-emphasized; **no deletions, no URL
changes, no redirects**. Fixed `&amp;amp;` entity in /compare/ title.

### Build, deploy, verify
GATE PASSED (now 8 gates incl. placeholder-assert), idempotent; 310 pages / 306 sitemap URLs
(thanks, gracias, tv, poster excluded). Deploy **6a8c3809** (pushed first; permalink verified
before production): hub EN/ES 200, homepage title live, placeholder scan of production output
= 0 hits, tv.html serves `x-robots-tag: noindex`, sitemap correct, 404s correct, canonical +
hreflang resolve. IndexNow POST 200 for 36 changed URLs. Netlify connector 502'd three times
(~7 min outage) before recovering — backoff protocol held; an expired earlier proxy token
returned 401 (expected).

### Standing
Orphans intentionally kept: form landings, newsletter, for-leasing-teams, alt-version pages.
/privacy/ + /es/privacidad/ still NEEDS REVIEW (backlog #1). Next: weekly `reinforce` runs;
Sept-1 month-roll; #2 tax-rate refresh on adoption (also fixes the data/property-tax CTR gap).

---

## 2026-08-24 — SEO growth system build + Lockheed cluster expansion — LIVE

- **Trigger:** Operator — evolve WFL into a closed-loop local SEO system (18-phase brief),
  GSC performance export of 2026-08-23 attached as the authoritative prioritization source.

### System built (see `docs/SEO_GROWTH_SYSTEM.md` for the full spec)
- `scripts/seo_engine.py` (stdlib-only): `ingest` (immutable snapshots to `data/gsc/YYYY-MM-DD/`,
  refuses overwrite) · `report` (URL-form merging, tier A–D, commercial-intent 0–3, CTR-gap,
  cannibalization, deltas, weighted opportunity queue → `reports/seo/`) · `linkaudit` (orphans,
  contextual inbound, depth, broken) · `log-event` (→ `data/seo/events.jsonl` with before-metrics
  and 7/28/90-day after-checkpoints).
- `data/seo/config.json` (weights/allocation/priority clusters), `data/communities.json`
  (null-tolerant structured community data, every value with source + verified date).
- Snapshots ingested: 2026-08-23 (121 pages / 197 queries) + partial 2026-08-20.
- `DAILY_RUN.md` SELECT step now reads the opportunity queue first (40/25/20/10/5 allocation,
  seven-question new-page gate); calendar backlog re-scored on GSC evidence.

### GSC-driven work shipped this run
1. **Lockheed hub retitled + enriched** (`/guides/apartments-near-lockheed-martin-fort-worth`,
   opportunity #1 at score 19.85: 285 imp @ pos 10.7, CTR 0.35%, ~140 imp of "apartments near
   lockheed martin" queries vs the old "Where to live…" title). New "communities people search
   by name" section links the named complex notes and de-orphans `/rentals/apartments-76108`.
2. **New buyer spoke** `/guides/buying-a-home-near-lockheed-martin-fort-worth` + ES mirror
   `/es/guias/comprar-casa-cerca-de-lockheed-martin-fort-worth` — four-pocket ladder built
   entirely from on-site verified data (published sale bands 08-23, TEA 2026 ratings 08-16,
   adopted 2025 ISD rates 08-22, shift-honest drives). Distinct buyer intent vs the renter hub;
   passed the seven-question gate; hub↔spoke linked both directions in both languages;
   cross-language links verified by rendered Chromium screenshots.
3. **De-orphaning pass** (orphans 25 → 10): guides hub gained Aledo/Walsh definitive-guide
   cards + a lease-law/Weatherford section (5 EN guides reconnected); es/guias gained a
   tenant-rights/insurance section (7 ES guides); rentals hub gained the three ZIP pages;
   the buyer spoke links both rent-or-buy pocket pages. Remaining 10 orphans are intentional
   utility/alt pages (thanks, gracias, poster, tv, newsletter, for-leasing-teams, field-guide,
   relocate/guide, donde-vivir, screening-signals) — operator may wire or retire.
4. Three change events logged to `data/seo/events.jsonl` for before/after measurement.

### Explicitly NOT created (anti-permutation rule)
Per-suburb "X to Lockheed commute" pages (pocket table covers the intent), a second
"where to live near Lockheed" variant (would cannibalize the hub), generic credit-score/
closing-costs variants (pos 68–100 = Google testing, low intent).

### Build, deploy, verify
`gen/build.py` + `apply_standing_fixes.py` → **GATE PASSED**, 308 pages / 306 sitemap URLs,
idempotent on re-run; only the two tracked `/privacy/` warnings. Deploy **6a8bc23f** (pushed
first, permalink verified before production): new EN/ES pages 200 on permalink and apex,
bogus path 404, 4 lockheed URLs in live sitemap, canonical + hreflang resolve both directions,
live hub `<title>` confirmed retitled. IndexNow POST 200 for 7 changed URLs. One Netlify
connector 502 on first deploy call — retried after 70s per protocol, succeeded.

### Standing
`/privacy/` + `/es/privacidad/` remain drafted, safeguarded, **NEEDS REVIEW** (backlog #1).
Next GSC export: `ingest` → `report` → compare the Lockheed retitle's checkpoints.

---

## 2026-08-23 — Daily cycle: seller net-proceeds napkin (EN + ES) — LIVE

- **Trigger:** Operator — "Run the West FW Living daily publishing cycle."

### Staleness scan
Gate `--check` green (304 pages), only the two tracked `/privacy/` warnings. Month-roll
(specials / rent report / builder report) not yet ripe on 08-23; 2026 tax-rate adoption
(#2) likewise. Nothing outranked a new page.

### Selection
Backlog **#5 — seller's net-proceeds napkin** (Sellers, M/H): the only core cluster untouched
(Schools 08-16, Neighborhoods 08-21, Buyers 08-22). New page `/sell/net-proceeds` + ES
`/es/vender/ganancias-netas`. No cannibalization: `/sell/capital-gains` covers taxes on the
gain; this covers the closing-cost ledger, and each links the other as the two halves.

### Research + verification
- **Owner's title policy at $450,000 = $2,509** — TDI basic premium schedule **effective
  2026-03-01**, fetched from tdi.texas.gov this run: $780 at $100K; (face − $100K) × 0.00494
  + $780 for $100,001–$1M; arithmetic computed in-session ((350,000 × 0.00494) + 780 = 2,509).
- **$0 transfer tax** — real-estate transfer taxes constitutionally prohibited in Texas
  (statewide Prop 1, approved 2015, in effect since 2016) — so stated as no state *or local*
  transfer tax.
- **$450K example price** — sits inside the site's published Willow Park band ($430K–$600K,
  public listings, summer 2026, per `/sell/willow-park`).
- **Everything else deliberately number-free**: escrow fees ("varies by company — get the fee
  sheet"), HOA resale package ("itemized, in writing"), payoff (mechanics only), tax proration
  (mechanics only: paid in arrears, credit Jan 1 → closing), and **agent compensation stated
  as negotiable with no percentages** — both the never-invent rule and the publisher posture
  point the same way. Earlier-remembered figures (e.g. a statutory HOA resale-cert cap) were
  omitted rather than stated unverified.

### Safeguards
Educational mechanics with an explicit not-advice line; no individualized advice, no
percentages that could read as steering compensation norms. None triggered.

### Produced
Napkin table (two hard lines + labeled blanks) · the three documents that fill the blanks ·
who it applies to · next steps · sources with the TDI formula spelled out · visible verified
date 2026-08-23 · Article + FAQPage JSON-LD · **sell_timeline form context both languages** —
`lead_form()` gained a `selling=True` variant emitting the same field/label the 26 existing
sell pages carry, so form-assert's selling rule passes natively · bidirectional hreflang +
visible cross-language links **verified by rendered Chromium screenshot**. Reciprocals:
sell hub card, es/vender hub card, in-body link from `/sell/capital-gains`.

### Build + gate
`GATE PASSED` — all seven asserts green. **306 pages, 304 sitemap URLs.** Second run a
clean no-op.

### Deployment + verification
One 502 from the connector gateway → 75s backoff, second attempt clean. Pushed before
deploying. Deploy `6a8b258f1dbe3417f989eeb8` — ready, production; deploy permalink verified
first. Live: EN + ES → 200, extensionless canonicals, 404 ok, both URLs in the live sitemap
(re-fetched after one flaky 000 response from the sandbox proxy — first sitemap read falsely
showed 0 matches; retry showed 304 URLs incl. both new pages), hreflang both directions.

### IndexNow
5 changed URLs (2 new, sell hub, es/vender hub, capital-gains) → HTTP 200.

### Next recommended action
`/privacy/` (backlog #1) still awaits human review. **Sept 1 month-roll is next** (specials /
rent report / builder report), then #2 (2026 tax rates) as districts adopt. After the Data
work, #6/#7 (Relocation/Renters) are the remaining balance gaps.

---

## 2026-08-22 — Daily cycle: homestead exemption in dollars (EN + ES) — LIVE

- **Trigger:** Operator — "Run the West FW Living daily publishing cycle."

### Staleness scan
Gate `--check` green (302 pages) with only the two tracked `/privacy/` warnings. August
time-bound pages still in-month (they roll on Sept 1 — next run should check the monthly
specials/rent-report/builder-report set). Nothing outranked a new page.

### Selection
Backlog **#4 — homestead exemption after Prop 13** (Buyers, H/H), per the balance note
(Schools 08-16, Neighborhoods 08-21 → Buyers/Data next; #2 property tax still holds for
September adoption). New page `/buy/homestead-exemption` + ES `/es/comprar/exencion-homestead`.
No cannibalization: `/buy/property-taxes-for-buyers` covers three levers broadly; this page is
the deep dive on one lever with per-district dollar arithmetic, and each links the other.

### Research + verification
- **Prop 13 (Nov 2025):** general school homestead exemption $100K→$140K, applying beginning
  with tax year 2025; **Prop 11:** additional 65+/disabled exemption to $60K ($200K total).
  Consistent with the site's existing claims on `/buy/property-taxes-for-buyers`.
- **Adopted 2025 school rates**, each from primary or official-county sources this run:
  Aledo ISD **$1.1942** (district news; seventh consecutive cut, −$0.0110) · Weatherford ISD
  **$1.0342** (district news, adopted 8/26/2025; M&O $0.7552 + I&S $0.2790, unchanged YoY) ·
  Fort Worth ISD **$1.0291** (board adoption 8/26/2025; **cross-checked against the county
  Form 50-859 worksheet** — extracted from the raw PDF streams after two search-engine
  summaries returned contradictory figures ($1.3754 vs $1.0624); the worksheet showed 2024
  adopted $1.0624 and 2025 voter-approval $1.0291, matching the adoption) · White Settlement
  ISD **$1.2069** (official Tarrant County truth-in-taxation database).
- Dollar values are arithmetic (exemption × rate), asserted in-session against the table:
  $1,441 / $1,448 / $1,672 / $1,690 per year; $2,058–$2,414 at 65+/disabled; the Prop-13
  increment alone ≈ $410–$480/yr. Stated as "≈" throughout.
- Deliberately omitted (unverified): city/county optional-exemption percentages; PCAD URL.
  Page says "check your appraisal district" instead.

### Safeguards
General educational tax content with an explicit not-tax-advice line — same category as the
existing property-tax page; not individualized advice. None triggered.

### Produced
Direct answer up top · per-district worth table · free-filing mechanics (Form 50-114, TAD/PCAD,
"never pay a filing service") · 10% appraisal cap · **September-2026 rate-adoption timing
note** (ties to calendar anchor; page refreshes each cycle) · sources with rates and dates ·
visible verified date 2026-08-22 · Article + FAQPage JSON-LD · move_date form context both
languages · bidirectional hreflang + visible cross-language links **verified by rendered
Chromium screenshot**. Reciprocal: buy hub card, es/comprar hub card, keep-reading link from
`/buy/property-taxes-for-buyers`.

### Build + gate
`GATE PASSED` — all seven asserts green. **304 pages, 302 sitemap URLs.** Second run a
clean no-op.

### Deployment + verification
Pushed before deploying. Deploy `6a899e25ceda1ce4259baa1e` — ready, production; deploy's own
permalink verified first. Live: EN + ES → 200 with extensionless canonicals · 404 check ok ·
both URLs in live sitemap · hreflang resolves both directions.

### IndexNow
5 changed URLs (2 new, buy hub, es/comprar hub, property-tax playbook) → HTTP 200.

### Next recommended action
`/privacy/` (backlog #1) still awaits human review. **September window opens next week:**
month-roll of specials/rent-report/builder-report on ~Sept 1, then #2 (2026 property-tax
rates) as districts adopt — this page and `data/property-tax.html` refresh together then.

---

## 2026-08-21 — Daily cycle: Living in Benbrook value-play guide (EN + ES) — LIVE

- **Trigger:** Operator — "Run the West FW Living daily publishing cycle."

### Staleness scan
Gate `--check` green (300 pages pre-run) with only the two tracked `/privacy/` warnings.
August time-bound pages (specials, rent report, builder report) still in-month; nothing
outranked a new page. Noted in passing: the guides hub linked neither living-in flagship
(fixed as a side effect of this run's reciprocal wiring pattern — the new card sits beside
where they should be; adding aledo/walsh cards is a one-line future RECIPROCAL entry each).

### Selection
Backlog **#8 — Benbrook as the value play** (Neighborhoods, H/H). Calendar balance called
for non-Schools after 08-16; tax item (#2) still holds until ~September adoption. Authored
as `/guides/living-in-benbrook` in the living-in-aledo/walsh flagship pattern — target query
"is benbrook a good place to live" had no existing page; the renter-oriented
`/areas/benbrook` remains distinct (no cannibalization; each links the other).

### Research + verification (no new facts invented)
Every figure reused from already-published, sourced site data or the verified TEA file:
- Sale bands/$-sqft/days: `/sell/benbrook` ($300K–$420K; $165–$205; 35–65d) vs `/sell/aledo`
  ($520K–$750K; $210–$260; 45–75d) — public listings, summer 2026. Gap stated as arithmetic
  between published bands, never as a valuation.
- Rents + platform-trend-conflict caveat: `/areas/benbrook` (May–Jul 2026), caveat carried
  forward verbatim in spirit (platforms disagree on trend direction → get written quotes).
- Schools: TEA 2026 spreadsheet (verified 2026-08-16): FWISD C 77; Benbrook M/HS A 90 (↑B),
  Westpark A 92, Benbrook El B 89 (↓A), Luella Merrett B 84, Ridglea Hills C 79,
  Waverly Park C 74 (↓B), Western Hills HS C 74 (↑D). Counterweights stated on-page.

### Safeguards
None triggered. No crime/safety claims, no individualized advice, publisher voice, email
capture only, no lender placement.

### Produced
- `/guides/living-in-benbrook` + ES mirror `/es/guias/vivir-en-benbrook` — direct answer up
  top, money/schools/daily-life/decision layers, next steps, inline sources, visible
  verified date 2026-08-20, Article + FAQPage JSON-LD, move_date form context (both langs
  to spec). Bidirectional hreflang + humanly visible cross-language links, **verified by
  rendered Chromium screenshot** both directions.
- Reciprocal links (all idempotent via `RECIPROCAL` or module edit): guides hub card,
  es/guias hub card, keep-reading link on `/areas/benbrook`, and a link from the TEA
  ratings page's Benbrook section.

### Build + gate
`GATE PASSED` — all seven asserts green. **302 pages, 300 sitemap URLs.** Second
build+fix run a clean no-op.

### Deployment
Two 502s from the connector gateway (retryable, per its own guidance) → backed off 60s/130s,
third attempt succeeded. Pushed to GitHub **before** deploying per the 08-18 platform lesson.
Deploy `6a8807e293e2753087e69883` — ready, production. Verified the deploy's own permalink
before production.

### Production verification
EN + ES → 200 with correct extensionless canonicals · nonexistent path → 404 · both URLs in
live sitemap.xml · hreflang resolves both directions live.

### IndexNow
6 changed URLs (2 new pages, 2 hubs, areas/benbrook, TEA page) → HTTP 200. The deploy's
build command also auto-pinged the full sitemap.

### Next recommended action
Backlog #1 (`/privacy/`, human review) remains the standing highest-severity item. Next
content slot: cluster balance now suggests Buyers or Data — #2 (property tax) unlocks on
~September adoption; #4 (homestead exemption after Prop 13) is the strongest interim pick.

---

## 2026-08-18 — Search Console coverage fix: canonical form flip (extensionless), deployed

- **Trigger:** Operator uploaded a Search Console coverage export
  (`westfwliving.comCoverage20260818.zip`): 68 pages not indexed — 63 "Alternate page with
  proper canonical tag," 3 "Page with redirect," 2 "Duplicate without user-selected canonical."
  `Chart.csv` shows not-indexed jumping 25→68 on 2026-08-07 while indexed fell 189→146.

### Diagnosis
1. Exactly 68 pages in the then-live commit (`4a9f74f`) had no `<link rel="canonical">` — 43 EN
   + 25 ES, matching the report's counts and its Aug-7 step precisely. (Canonicals for these
   were already added in the 2026-08-16 commit but never deployed — see that entry's "Deployment
   status: BLOCKED.")
2. The deeper cause: Netlify's Pretty URLs post-processing rewrites every rendered
   `<a href="x.html">` to `<a href="x">` on **every deploy**, platform-side, regardless of
   source content. 3,682 internal link instances across the site pointed at a URL form (mostly
   extensionless, matching the original nav/footer templates) different from what ~186 pages'
   canonical tags declared (mostly `.html`). Google crawled both forms, found byte-identical
   200s, and filed the mismatch as "alternate page with proper canonical tag."

### First attempt (WRONG DIRECTION — corrected same session)
Initially made `.html` the canonical form and rewrote all internal links to match. Deployed,
then verified against the **deploy's own permalink** (not just local/GitHub content) and found
the fix had been silently undone: 0 of the `.html` hrefs survived publish. Isolated this with a
diagnostic marker (an HTML comment appended to `index.html`, committed, pushed, deployed) — the
marker survived while the href rewrites did not, proving the reversion was a platform-level
transform of `<a href>` specifically, not a stale-content/caching bug. Four deploy attempts were
burned confirming this (cache clears, `--no-wait` and waited variants, fresh proxy tokens each
time) before the mechanism was identified.

### Corrected fix
Flipped the policy: **extensionless is the one correct canonical form**, since that's what
Netlify actually serves via links regardless of source, and it matches the site's original
(pre-session) nav/footer convention. `url_for()` / `canonical_path()` in
`scripts/apply_standing_fixes.py` now derive and enforce this; a `.html`-form canonical is
actively corrected, not passively accepted (the earlier "don't rewrite existing valid
canonicals" design was itself a symptom of the wrong initial assumption). Added `fix_hreflang()`
— hreflang `<link>` hrefs are absolute URLs untouched by Pretty URLs, so they drift
independently and needed their own normalization pass. `gen/common.py`'s nav/footer constants
and `gen/pages_schools_ratings.py`'s links were reverted to extensionless, and a `_url()` helper
added to `gen/common.py` so generator output already matches the final form on first build —
verified idempotent (two full `build.py` + `apply_standing_fixes.py` passes produce identical
output, second run reports zero changes).

### Build + gate
`GATE PASSED — nav-assert, form-assert, canonical-assert, hreflang-assert, link-assert,
link-canonical-assert, sitemap-assert all green.` 300 pages, 298 sitemap URLs. Confirmed
sitewide: 0 non-canonical `<a href>`, 0 non-canonical hreflang, all 300 pages carry a matching
canonical.

### Deployment
Deploy `6a849186b1c07328330aeb3c` — **ready**, production. Verified against the deploy's own
permalink *before* trusting production (lesson from the four failed attempts above): nav hrefs
extensionless, canonical extensionless, matches source exactly.

### Production verification
- `/schools/tea-ratings-2026` → 200, `/es/escuelas/calificaciones-tea-2026` → 200, nonexistent
  path → 404.
- Canonical on `/`, `/specials`, `/deals`, `/schools/tea-ratings-2026`,
  `/es/escuelas/calificaciones-tea-2026`, `/sell/aledo` all confirmed extensionless (or their
  correct form for `/sell/`, which was already extensionless and untouched).
- Both URLs present in `https://westfwliving.com/sitemap.xml`, itself now fully extensionless
  (298 URLs).
- ES hreflang resolves both directions live; the visible cross-language link renders with the
  extensionless href.
- Rendered-DOM verification via headless Chromium was attempted against the live domain but
  blocked by this session's outbound proxy config (Playwright couldn't reach the public
  westfwliving.com domain; curl could). Substituted with the equivalent curl-based checks above
  plus an earlier local-server Chromium screenshot of the page structure (2026-08-16 entry).

### IndexNow
Submitted all 298 sitemap URLs (now extensionless) to `https://api.indexnow.org/indexnow` — 
HTTP 200. A second batch was also submitted earlier in this run for the (subsequently corrected)
`.html`-form URL set; that submission is superseded by this one and is expected to be
self-correcting once Google recrawls and sees the canonical tag.

### What was NOT touched
No safeguarded-category content. No new pages beyond what the 2026-08-16 run already produced.
The `/privacy/` gap remains open (backlog #1, unchanged).

### Lesson recorded for future runs
Local disk / GitHub content matching what you intend to ship is necessary but **not
sufficient** — this host's Pretty URLs post-processing means the only way to confirm a link/URL
form fix actually took effect is to check the **deploy's own permalink** (or production) after
the fact, not just the source. Added this as a standing note to `DAILY_RUN.md`.

---

## 2026-08-16 — Bootstrap run + 2026 TEA ratings page (built & gated; deployed 2026-08-18, see entry above)

- **Trigger:** Operator — "Run the West FW Living daily publishing cycle." First WFL run; the
  Drive driver doc listed WFL as "not yet onboarded … no generator/gate or editorial log."

### Staleness scan (run before topic selection)
Findings, in the order they were surfaced:
1. **`/privacy/` and `/es/privacidad/` 404** while being linked from the **required** consent
   checkbox on every lead form — 197 EN pages and 42 ES pages. The site asks users to accept a
   document it does not serve. **Safeguarded category (privacy/consent disclosure) → drafted
   and flagged `NEEDS REVIEW`, not published.** Draft:
   `editorial/drafts/privacy-policy-DRAFT.md`. Tracked in `KNOWN_MISSING` so the gate reports
   it every run without blocking, and so a *new* dead link still fails the gate.
2. **`/where-to-live.html` nav had 9 links** — the `Selling` link was missing, violating the
   10-link spec. Fixed by the standing-fix pass.
3. **68 pages had no `<link rel="canonical">`**, including the `/schools/` hub and 20+ ES
   guides. Fixed (added, not rewritten — see note below).
4. **Lead-form drift:** 3 ES pages used `¿Cuándo planeas mudarte?` instead of the spec string
   `¿Para cuándo planea mudarse?`; 7 EN `lease_end` labels had drifted to ad-hoc wording
   ("When's your report / move date?", "How long do you need, and starting when?"); 2 pages
   (`where-to-live.html`, `es/donde-vivir.html`) had a lead form with **no** date field at all.
   All normalized.
5. **`data/property-tax.html` still labels its rates "2024–2025 published figures."** One cycle
   stale. **Not fixed this run** — correcting it means re-verifying every city/ISD/county rate
   against Tarrant and Parker appraisal districts, and Texas taxing units adopt new rates around
   September. Queued as backlog #2 with an explicit instruction not to bump the label without
   re-verifying the rates underneath it.
6. Verified-date coverage is **50/298 pages**. Queued as backlog #12 (fills a no-topic day).
7. No dead sitemap entries, no duplicate titles, no broken internal links other than #1.

### Selection
**2026 TEA A–F accountability ratings for the west Fort Worth corridor.** Chosen over the
maintenance items and the rest of the backlog because: TEA released the data **two days prior**
(2026-08-14), the site had **zero** pages mentioning accountability ratings despite a 17-page
schools cluster, school zoning is a primary driver of west-side housing decisions, and the
source is tier-1 authoritative. Cluster: Schools.

### Research + verification
- Primary: **TEA 2026 Statewide Multi-Year Ratings spreadsheet** (18.6 MB `.xlsx`, the
  authoritative per-district and per-campus file behind TXschools.gov), downloaded and parsed
  directly. Every district and campus figure on the page comes from this file.
- Corroborating: TEA's 2026 release announcement (1,202 districts / 9,105 campuses rated);
  FOX 4 and CBS Texas independently reported Fort Worth ISD at **C, 77, up from 73**, and Lake
  Worth ISD holding a **D** — both match the spreadsheet exactly. That agreement is the
  cross-check on the parse.
- **Year-conflation trap avoided:** the top-ranked local result for Parker County school
  ratings was a **2022** Weatherford Democrat article ("first ratings in three years") listing
  Weatherford ISD as a B (89) and Brock as an A (95). Those are *2021-22* figures. Discarded;
  none of it reached the page. Recorded as a standing warning in `DAILY_RUN.md`.
- Headline findings: Aledo ISD **A, 92** (held); Brock ISD **A, 91**; Weatherford ISD
  **C→B, 80**; Fort Worth ISD **C, 77** (up 4); White Settlement ISD **C, 75**; Benbrook
  Middle/High **B→A, 90**. Campus tables for Aledo, Weatherford, Benbrook-area FWISD and
  White Settlement.

### Safeguard decisions on this page
- **Active legal dispute — avoided.** Fort Worth ISD has been reported as considering joining
  litigation against TEA's A–F system. Reporting TEA's published ratings is ordinary factual
  reporting, but the litigation itself falls under the "active legal dispute" safeguard, so the
  page does **not** mention it in any form.
- **Low ratings handled factually.** Liberty Elementary (White Settlement ISD) rated **F, 55**.
  This is published government accountability data, not an allegation against an identifiable
  person or business. Presented neutrally, with the note that a low rating triggers state
  support requirements for the campus rather than describing the children in it.
- No individualized advice, no crime/safety claims, no political content, no sponsored content.

### Produced
- `/schools/tea-ratings-2026.html` (EN) and `/es/escuelas/calificaciones-tea-2026.html` (ES).
- Direct answer up top · corridor context (Willow Park, Hudson Oaks, Weatherford, Aledo,
  Benbrook, White Settlement, the I-30/Loop 820 and I-20 geography) · who it applies to ·
  a "what a rating does not tell you" section · next steps · inline sources · **visible verified
  date (2026-08-16)** · Article + FAQPage JSON-LD · page-matched CTA (email capture only, no
  lender placement, no brokerage language).
- **Hub-and-spoke:** links to `/schools/`, plus a **reciprocal** card added to the schools hub
  and the ES schools hub, wired into `RECIPROCAL` in `gen/build.py` so it is re-applied
  idempotently on every build.
- **ES mirror:** bidirectional hreflang, and a **humanly visible** in-body cross-language link
  in both directions. **Verified by rendered screenshot** (headless Chromium, not grep): both
  links confirmed `is_visible()` with correct text and href. The render also caught a real
  defect — the EN page's Spanish link was missing its accents ("pagina en espanol"); fixed and
  re-rendered.

### Bootstrapped this run (WFL had none of this before)
- `editorial/DAILY_RUN.md`, `EDITORIAL_CALENDAR.md` (90-day, seeded 12-item scored backlog),
  `staleness-scan.md`, this log, and `editorial/drafts/`.
- `gen/common.py` (`page()`, `lead_form()`, `article_ld()`, `faq_ld()`), `gen/build.py`,
  `gen/pages_schools_ratings.py`.
- `scripts/apply_standing_fixes.py` — the final build step: nav / canonical / form
  normalization, sitemap derived fresh from disk, and six gates.

### Build + gate
```
python3 gen/build.py
python3 scripts/apply_standing_fixes.py
```
`GATE PASSED — nav-assert, form-assert, canonical-assert, hreflang-assert, link-assert,
sitemap-assert all green.` · **300 pages · 298 sitemap URLs.**
Idempotency verified: a second consecutive run reports "nothing to change" and stays green.
2 tracked warnings (the `/privacy/` pair above), which are reported, not suppressed.

Two deliberate deviations from a literal reading of the task spec, both flagged for the operator:
- **`sell_timeline` preserved as a third form context.** The spec says renting pages use
  `lease_end` and "all others" use `move_date`. The 26 `sell/` and `es/vender/` pages carry a
  purpose-built `sell_timeline` ("when are you planning to sell?"), which is a better question
  for a seller than a move date. Flattening it would have been a regression, so it was kept.
  Reversible in one edit — see `DAILY_RUN.md`.
- **Existing canonicals not rewritten.** The site uses three equivalent apex spellings
  (`/x.html`, `/x`, `/dir/`); 24 live pages (all of `sell/` and `es/vender/`) declare the
  extensionless form and the sitemap matches. Canonicals were **added** where missing and left
  alone where already valid, rather than churning 24 live canonical URLs for cosmetic
  uniformity. `hreflang-assert` and `link-assert` resolve URLs to files, so all three spellings
  compare equal.

### Deployment status — **BLOCKED, NOTHING DEPLOYED**
- **Cause:** the Netlify MCP connector is authorized at org level (`ListConnectors` reports
  `connected: true, enabledInChat: true`) but **its tools are not loaded in this session.**
  `ToolSearch` finds no `netlify` tools under any name, and `ListMcpResourcesTool` shows only
  the `github` and `Instacart` servers present. This is the documented caveat that
  interactively-authenticated MCP servers may be absent in headless/remote runs.
- **Fallback attempted and rejected:** `netlify-cli` is installable but reports
  `Not logged in`, and no `NETLIFY_AUTH_TOKEN` exists in the environment. No credential path.
- **Not attempted, deliberately:** pushing to `claude/deploy-anastasiaweaver-netlify-8kboru`
  (the production-source branch) to trigger a git-based build. That branch is outside the
  authorized push target for this run, and force-routing a deploy around a missing credential
  is exactly what the deploy-failure protocol forbids.
- **Production integrity confirmed intact** (nothing was half-shipped): `/` → 200,
  `/schools/` → 200, a nonexistent path → 404, `/f61db218…txt` → 200. The new URL correctly
  → 404, i.e. not yet live.
- **IndexNow: deliberately NOT sent.** Submitting URLs that currently 404 would be actively
  harmful. Note that `netlify.toml`'s build command already pings IndexNow from the freshly
  built sitemap on every deploy, so the ping fires automatically once the deploy runs.
- **IndexNow first-run setup was already satisfied**, so no key generation was needed: key
  `f61db218770282944b56755e36b90509` is live at
  https://westfwliving.com/f61db218770282944b56755e36b90509.txt (verified 200) and is recorded
  in `DAILY_RUN.md` along with the siteId.

### Recovery path (clean — no partial state to unwind)
Everything is committed on `claude/wfl-daily-publishing-i7lmp9` and gates green from a clean
checkout. To finish the cycle, in a session where the Netlify connector's tools are loaded
(or with `NETLIFY_AUTH_TOKEN` set):
1. `python3 gen/build.py && python3 scripts/apply_standing_fixes.py` → expect `GATE PASSED`.
2. Deploy siteId `a975e513-e8b1-46c2-9d31-1f769e103f2c` via the connector, `--no-wait`, poll
   to `state=ready`.
3. Verify: `/schools/tea-ratings-2026.html` → 200 · nonexistent path → 404 · both URLs in
   `https://westfwliving.com/sitemap.xml` · canonical is the apex URL · ES hreflang resolves
   both ways.
4. IndexNow fires automatically via the build command; confirm in the deploy log, or POST the
   two changed URLs manually with the key above.
5. Append the deploy ID + verification results to this entry and mark the calendar row LIVE.

### Next recommended action
Resolve the **`/privacy/` gap** (backlog #1) — it is the highest-severity finding on the site
and it is a human decision, not a content decision. Then backlog #2 (property tax rates) once
the taxing units adopt in September.

---

## 2026-09-02 — Trust layer + _redirects moved into the build; Aledo ISD 2026–27 rate shipped to the homestead file

- **Trigger:** Daily cycle (chat session, Netlify connector available). Preceded by a portfolio review that found the 2026-08-16 mirror-injected trust layer gone from 0/38 sampled live pages and the 2026-08-23 `_redirects` never live — both overwritten by deploys from this tree.
### Staleness scan
- `apply_standing_fixes.py --check`: green. Full on-page audit (310 pages): no missing canonicals/hreflang/alt/viewport/H1, all JSON-LD parses, no dead internal refs beyond the tracked privacy pair. Soft finding: 257 titles >70 chars, 234 descriptions >170 chars (SERP truncation) — editorial batch work, not a script.
- Time-bound: September month-roll (specials / rent report / builder report) is due and **not done** — requires per-complex first-party verification; not fabricated.
### Selection
- Backlog #13 (private-school tuition) found already shipped 2026-08-28 — calendar corrected to LIVE.
- Chose backlog #2 first tranche: Aledo ISD's 2026–27 adoption is live on the district site; a maintenance update to the homestead file (generated) beats a new page. Other districts not yet adopted → table stays on 2025 rates with an explicit adoption-watch section.
### Research + verification
- Aledo ISD 2026–27 adopted rate $1.1775/$100, −$0.0167 from $1.1942, eighth consecutive reduction, budget $138,549,072 — aledoisd.org district news "Aledo ISD Trustees adopt 2026-2027 budget", dated 2026-08-24, verified 2026-09-02.
- Weatherford ISD: 2026 adoption not found on weatherfordisd.com as of 2026-09-02 (latest is 2025-08-26). City of Weatherford: FY27 *proposed* $0.392246, council consideration 2026-09-08 (weatherfordtx.gov) — proposed only, not used.
- Arithmetic: $140,000 × 1.1775% = $1,648.50 → "about $1,649"; $200,000 × 1.1775% = $2,355.
### Safeguard decisions
- Privacy pages: still REVIEW; operator has the three retention/unsubscribe/sharing answers on file (24 months; reply-STOP + contact address; shared only with a future licensed brokerage affiliate) but declined to finalize this session — controller name + contact address still open. Nothing deployed.
### Produced
- `gen/pages_buy_homestead.py`: SRC_ALEDO_2026, "2026 adoption watch" section EN + "Seguimiento de las tasas 2026" ES, sources list updated, VERIFIED → 2026-09-02. Rebuilt `/buy/homestead-exemption` + `/es/comprar/exencion-homestead`.
- `scripts/apply_standing_fixes.py`: new sitewide fixes `fix_trust_layer` (Organization JSON-LD + org byline with git last-updated date; uncommitted content edits date as today via `_materially_changed`, trust-layer-only diffs do not) and `build_redirects` (one forced `301!` per page, .html → extensionless); new gates `trust-assert`, `redirects-assert`. `styles.css`: `.byline`.
### Build + gate
- `gen/build.py` → 12 generated pages; `apply_standing_fixes.py` → GATE PASSED (10 gates); second run idempotent no-op. Pages 310 · sitemap 306 · `_redirects` 310 rules.
### Deployment status
- Deploy 6a98e918 (trust layer + redirects) verified live 2026-09-02. Deploy 6a98f1ce (homestead update + audit log) state=ready 2026-09-02; /buy/homestead-exemption 200 with adoption-watch section, ES mirror 200, nonexistent path 404, sitemap lastmod 2026-09-02, .html → 301.
### Production verification
- `.html` → 301 (5/5 sampled); extensionless 200, no loop; trust layer 25/25 sampled EN+ES; homepage WebSite + Organization JSON-LD.
### IndexNow
- Fires from `netlify.toml` build command on deploy; both changed URLs also POSTed manually → HTTP 200.
### Repo reconciliation (Claude Code, 2026-09-03)
- Handoff bundle audited line-by-line before applying (gate-script diff, content diff, patch);
  premise verified against live production; $1.1775 independently corroborated on aledoisd.org.
- Source landed as commit 0e1328d; rebuilt tree (GATE PASSED, **ten gates** incl. trust-assert
  + redirects-assert; --check green on the fixed tree) as commit 3527e27 — 312 files,
  _redirects created (312 lines). Sanity checks per handoff: one org-jsonld + one byline on
  index.html; only the two homestead pages carry a September date. Both commits pushed.
- **Proof deploy 6a99b5f2** (2026-09-03, via the validating Netlify build): summary reads
  "All files already uploaded by a previous deploy with the same commits" — repo == production,
  byte-for-byte — with 310 redirect rules processed. Live re-verified: /areas.html → 301
  /areas; homepage org-jsonld + byline ×1; homestead EN/ES 200 with adoption watch + $1.1775;
  404 correct; sitemap 306 URLs, homestead lastmod September.
### Next recommended action
- September month-roll (specials/rent/builder) with per-complex first-party verification;
  #2 remainder as WISD/FWISD/cities adopt; privacy pages only when the operator supplies the
  controller legal name + contact email (retention/unsubscribe/sharing already answered).

---

## 2026-09-03 — September month-roll: Concession Index 7.5→4.0, Rent Report No. 2, sitewide refresh

- **Trigger:** Daily cycle; data engine refresh_due 2026-09-01 overdue; handoff standing rule
  ("the September month-roll is next, with per-complex first-party verification").
### Staleness scan
`assets/wfl-data.js` verified 2026-07-31 (overdue); sitewide "6–8 weeks free" claims, the
August rent-report footer link (~300 pages), homepage stats, all 11 complex pages, specials
EN+ES, and the rentals/guide comparison tables all carried August or July figures.
### Selection
September month-roll (calendar recurring item, due 1st): re-verify all 11 tracked
communities, roll the data engine, author Rent Report No. 2, sweep every stale claim.
### Research + verification (all 2026-09-03)
ApartmentList price-verified pages (same-day stamps): Olympus Willow Park "2 Weeks Free on
Select Units", 1BR $1,425 / 2BR $1,579; Olympus Hudson Oaks up to 6 wks, $1,267/$1,594;
Birchway "Up to 8 Weeks Base Rent Free", $1,378/$1,708; Oxford NO specials, $1,284/$1,647
(was "2 months free"); College Park no specials, 2BR $1,200 std / $1,300 remodeled, 3.5x
income, 6–13 mo; Willow Crossing "Up to 4 weeks free", 3BR from $2,475 (range to $2,627).
Listing search results: Gates 4 wks, from ~$1,412; Canvas up to 6 wks on 13–15 mo leases,
8 homes $2,299–$2,699; Preserve 55+ "1 Month Free", from $1,255; Chapel Creek Cottages
"Get Up to 8 Weeks FREE" (NEW — was 0 in Aug), $1,530–$1,999 across 1–3BR. First-party:
westpointtx.com/specials confirms active offers (details posted as images; 6 wks + no app
fee per listings, range $1,299–$1,649). Computed: core-4 index (2+4+6+4)/4 = 4.0 (was 7.5);
expanded 11-community 48.3/11 ≈ 4.4. Conflicting/stale listings (Olympus "8 wks", Willow
Crossing "8 wks") resolved in favor of dated price-verified quotes and noted on-page.
### Safeguard decisions
No safeguarded categories touched. Unverifiable floor plans dropped from `beds` rather than
carried forward (consumer pages null-check); unit-basis caveats written into specialNotes
(College Park 2BR basis, Chapel Creek range floor, Westpoint image-only specials page).
Builder report 2026-09 deferred — no verifiable new builder packages found this cycle;
September report links the August edition as "latest, September's in verification".
### Produced
`/rent-report/september-2026` (Edition No. 2 + Dataset JSON-LD + Sept chart SVG); data
engine rolled (verified "September 3, 2026", refresh_due 2026-10-01, reportMonth September,
weeksHistory/priceHistory Sep appends, index 4.0 + expandedCurrent 4.4); specials EN +
`/es/especiales` September tables; all 11 `/complexes/` pages re-dated with September
figures and honest-take rewrites; sitewide footer "Latest Rent Report" → September (~300
pages incl. gen/common.py + scripts/fix-nav.py); stale-claim sweep across homepage EN/ES,
guides (Lockheed, NAS JRB, Medical City, Weatherford College, renewal, rent-to-own,
glossary, comparisons), rentals feature/zip pages, buy/rent-or-buy pages; August report and
Willow Park August guide marked archive with September pointers. No ES mirror of the rent
report (no ES precedent for the cluster); ES surfaces updated in place.
### Build + gate
gen/build.py 12 pages; apply_standing_fixes.py **GATE PASSED** ×2 (idempotent) — all ten
gates green; 311 pages, sitemap 307 (September report added); trust layer re-dated the
~256 materially-changed pages to 2026-09-03 (expected for a month-roll). validate-production:
311 HTML files, 0 prohibited strings. Known non-blocking warnings unchanged (/privacy/ + 
/es/privacidad/ pending controller name/email — REVIEW).
### Deployment status
Commit `9e302e7` pushed; deploy **6a99be6b** (build 6a99be6b0a781d0a85488e86) ready on
https://westfwliving.com.
### Production verification
200: september report (canonical extensionless, core-4 4.0 + expanded 4.4 in body),
rent-report index (September card), specials EN (Sept 3 verified line) + ES ("3 de
septiembre"), olympus complex page ("2 WEEKS FREE", "As of September 3, 2026"), Sept chart
SVG, wfl-data.js (verified/reportMonth/index all September). 404 correct. Sitemap 307 URLs
incl. september-2026. Homepage serving "9 of 11" / "7.5→4.0" stats.
### IndexNow
36 URLs submitted (report + hubs + specials EN/ES + all 11 complex pages + swept guides/
rentals/buy pages) — HTTP 200.
### Next recommended action
- #2 tax-rate refresh as districts adopt (City of Weatherford council vote 09-08).
- Builder report 2026-09 when verifiable packages publish; Lockheed round 2 on next GSC
  export; privacy pages still blocked on controller legal name + contact email.

---

## 2026-09-06 — URL-duplication audit and canonicalization hardening (operator-requested)

- **Trigger:** Operator request following GSC coverage report (74 "alternate page" +
  redirect/duplicate buckets): audit and fix URL duplication sitewide.
### Audit findings
Convention confirmed (extensionless pages, trailing-slash section indexes) and already
enforced for links/canonicals/sitemap/redirects by the standing gates. New findings:
(1) ~180 absolute https://westfwliving.com/*.html URLs in non-link positions — JSON-LD
url/mainEntityOfPage on ~115 pages and every lead form's _next post-submit target —
which the link canonicalizer never covered; (2) netlify.toml X-Robots-Tag noindex
headers matched only .html paths, which now 301, so /thanks, /es/gracias, /tv, /poster
served canonically with NO noindex (tv/poster also lacked meta fallback); (3) sitemap
listed two inline-noindexed gated pages (buy/field-guide, relocate/guide). Clean:
internal links, canonical tags, hreflang (form + reciprocity), sitemap forms, case
variants, redirect chains/loops (none), _redirects parity (311 rules).
### Fixes (commit d323dad, deploy 6a9d7552)
fix_absolute_html_urls pass + gate added to apply_standing_fixes.py (folds into
link-canonical-assert; idempotent); noindex headers added for the four extensionless
paths (kept .html forms); meta noindex added to tv.html/poster.html; sitemap generation
+ parity gate now detect inline meta noindex (sitemap 307 -> 305); new
scripts/audit_urls.py (static + --live URL auditor: canonical uniqueness, redirect
parity, chain/loop, non-canonical links, absolute .html URLs, sitemap parity, hreflang
reciprocity; live mode probes every canonical for 200 and every alternate for one
direct 301).
### Verification
Ten gates GATE PASSED x2 (idempotent); validator 311 files 0 prohibited; auditor repo
mode clean; full live probe (311 pages x 2-3 URLs) clean; user-listed duplicate groups
each 301 once directly to canonical; Lockheed guide 200 at canonical, .html variant
single 301; X-Robots-Tag noindex confirmed on all four canonical utility URLs; forms
post to /thanks (200); JSON-LD urls canonical (spot-checked); live sitemap 305.
### Next recommended action
- Resubmit sitemap.xml in GSC (URL set changed: -2 noindexed pages) and Request
  Indexing on the Lockheed guide's canonical URL. Coverage re-export ~09-22 (reminder set).

---

## 2026-09-06 — SEO sprint: CTR engineering + freshness pass on GSC strike-zone pages (operator-requested)

- **Trigger:** Operator sprint brief with GSC baseline (1,868 imp / 11 clicks / 0.59% CTR,
  ~35 active days; page-one zero-click pages named).
### Validated, not recreated
Phases 1-2 of the brief were already shipped and re-verified rather than redone: URL
consolidation (09-02/09-06, auditor green repo+live), sitemap/canonical/hreflang gates,
hub architecture (relocate/, schools/, military/, compare/, neighborhoods/, data/,
working-at-lockheed hub), lead-form protections, trust layer. New page inventory at
reports/seo/2026-09-06-page-inventory.csv (311 pages, 0 duplicate titles, 4 orphans).
### Changes (commit 781a93f, deploy 6a9d77ab)
CTR/metadata: Divvy review (title/desc to verified-status question; Divvy status
re-checked 2026-09-06 via its own site — new-application path still absent — and dated
on-page + in the rent-to-own status table), fine-print guide (desc; new clawback
trapdoor), Westpoint complex page (title+dated desc), private-schools (110-char title
trimmed), WP-vs-HO compare (desc + September rental-divergence section). Content:
Lockheed guide (gates/corridors/pets section, Sept spot-check note on bands, dual CTA
row), data/property-tax (2026 adoption watch: Aledo ISD $1.1775 adopted 08-24;
Weatherford $0.392246 PROPOSED, vote 09-08; parcel-verify path via parkercad.org /
tad.org / comptroller.texas.gov; compare links). Orphans fixed: screening-signals,
es/donde-vivir, newsletter, for-leasing-teams. docs/RENT_REPORT_PLAYBOOK.md added.
Walsh-vs-Morningstar (pos 2.9) deliberately untouched.
### Verification
Ten gates GATE PASSED x2; auditor repo + live-sample green post-deploy; validator 311/0;
no duplicate titles; FAQ JSON-LD matches rendered content on touched pages; changed
pages 200 live with new content confirmed. 7 events logged to data/seo/events.jsonl
(before-positions from 2026-08-28 snapshot + operator baseline); IndexNow 11 URLs (200).
### Next recommended action
- Operator: GSC sitemap resubmit if not done 09-06; Request Indexing on Lockheed guide,
  Divvy review, property-tax page. Fresh GSC export ~09-20 unlocks Lockheed round 2 and
  the 7d/28d checkpoints on today's ledger entries.

---

## 2026-09-18 — Daily cycle: 2026–27 adopted tax rates land (Weatherford city + WISD)

- **Trigger:** Daily cycle. Staleness scan hit: data/property-tax still said Weatherford's
  rate vote was "scheduled September 8" (10 days past). Backlog #2 actionable.
### Selection
#2 (2026–27 tax rates as districts adopt) — Data & Tools/Buyers cluster; fixes a stale
claim on a ranking page (pos 8–10) rather than creating a new page.
### Research + verification (2026-09-18)
City of Weatherford: adopted $0.392246 per $100 on 2026-09-08, unchanged from 2025 (the
no-new-revenue rate) — first-party, weatherfordtx.gov/3232/Property-Tax-Rates.
Weatherford ISD: adopted $0.9342 for 2026–27 on 2026-09-14 (M&O $0.7552 + I&S $0.1790),
−$0.10 vs 2025's $1.0342 — board action as reported by the Weatherford Democrat
(district's own tax pages still showed 2025–26 on verify date; labeled accordingly).
Exemption arithmetic: $140,000 × 0.9342% = $1,307.88 (~$1,308); $200,000 × 0.9342% =
$1,868.40 (~$1,868); Aledo–WISD school-rate gap widens to $0.2433. Pending, verified as
unfindable/not adopted: Parker County (hearing notices posted; ambiguous vintage — number
omitted), Willow Park (site posts FY25-26 PDFs), Aledo/Hudson Oaks cities, FWISD, WSISD.
### Safeguard decisions
None triggered. Mixed-year stacks avoided per the page's own rule; WISD figure source
labeled as press-reported board action, not first-party.
### Produced
Adoption-watch updates on /data/property-tax (as-of 2026-09-18, three adopted units,
honest pending list, gap-widening analysis) and /buy/homestead-exemption EN + ES mirror
(via gen/pages_buy_homestead.py; VERIFIED 2026-09-18; new WISD dollar arithmetic).
### Build + gate
gen/build.py 12 pages; GATE PASSED all ten gates ×2 (idempotent, 0 rewrites on second
pass); URL auditor green; validator 311 files / 0 prohibited. Only the three content
pages + sitemap lastmod changed (5 files).
### Deployment status
Commit e65478b pushed; deploy 6aad5678 ready on westfwliving.com.
### Production verification
All three URLs 200; 404 correct; hreflang EN↔ES resolves both directions live; sitemap
carries all three; $0.9342/$1,308 confirmed in served EN and ES HTML.
### IndexNow
3 URLs, HTTP 200.
### Next recommended action
- Re-check FWISD/WSISD/counties/cities adoptions next cycle; roll the full 2026–27 stacks
  into wfl-data.js tax table once a majority land. GSC coverage re-export reminder fires
  09-22. October month-roll due 10-01 (playbook: docs/RENT_REPORT_PLAYBOOK.md).

---

## 2026-09-22 — Daily cycle (run from primary session): Parker County proposed rate + automation incident record

- **Trigger:** Daily cycle, run in the primary session after the scheduled fresh-session
  runs of 09-20/21/22 all completed work but failed to push (see incident below).
### Selection
Adoption-watch continuation (#2): re-check FWISD, WSISD, Parker/Tarrant counties.
### Research + verification (2026-09-22)
Parker County: FY27 rate PROPOSED at the no-new-revenue level, $0.284719 combined; public
hearing and expected adoption 2026-09-22 (per the commissioners court's posted rate-setting
actions) — labeled proposed on-page, confirm adoption next cycle. FWISD: no 2026–27
adoption findable (district Adopted Tax Rates page and press show 2025–26 $1.0291 as
latest) — stays pending. WSISD/Tarrant: pending.
### Produced
data/property-tax adoption-watch: as-of date → 09-22; Parker County upgraded from vague
"hearings in process" to the labeled proposed NNR figure with date; pending list trimmed.
### Build + gate
Ten gates GATE PASSED; URL auditor green; validator 311/0.
### Deployment status
Commit + connector deploy from this session (SHA/deploy ID in the commit that follows).
### AUTOMATION INCIDENT (recorded for operations)
The scheduled fresh-session Routine ran 09-20, 09-21, and twice on 09-22 (~$3/run). Every
run completed its cycle but ended with staged, unpushed work that was lost on container
reclaim. Mitigations tried: project .claude/settings.json permission allowlist (commit
4db72ec) — did not resolve; prompt hardening with commit-first ordering and a
mcp__github__push_files API fallback — did not resolve. Root cause in trigger-spawned
fresh sessions not yet identified (their transcripts are not inspectable from here).
Resolution: fresh-session Routine DISABLED (trig_01DbXbb242wkuSy9gtrTN7mL); replaced by a
Routine that fires the cycle into the primary session (trig_012Be7REkereqSKQbFUzi9ir,
daily 12:01 UTC), where push/deploy/verify are proven. GitHub Actions deploy workflow
remains in place; NETLIFY_AUTH_TOKEN secret still not configured (guard fails), so
deploys continue via the Netlify connector from the primary session.
### Next recommended action
- Confirm Parker County adoption (vote was today) next cycle; FWISD/WSISD re-check.
- Operator: NETLIFY_AUTH_TOKEN secret; fresh GSC coverage export (requested 09-22).
- October month-roll due 10-01.

---

## 2026-09-23 — Daily cycle (first scheduled main-session run): City of Willow Park adopts $0.429041

- **Trigger:** Scheduled Routine (main-session binding), first firing.
### Staleness scan
Property-tax watch said Parker County adoption "expected September 22" — checked; no
adoption confirmation findable yet (only the proposed ceiling $0.284719, components M&O
$0.185698 + I&S $0.049859 + R&B $0.049162, hearing held 09-22). Wording already hedged
correctly; left as-is.
### Selection + research (2026-09-23)
Adoption watch #2 continuation. VERIFIED: City of Willow Park adopted $0.429041 per $100
for FY 2026–27 — the no-new-revenue rate, down from $0.4325 — per Weatherford Democrat
coverage of the council's budget/rate adoption, matching the council's published proposed
rate 0.429041. NOT verifiable, left pending: WSISD (2026 tax-rate ordinance posted on the
district's transparency page but the figure is only in PDFs; an adoption-notice snippet
exists but is ambiguous — no number published), FWISD, Tarrant County, Aledo/Hudson Oaks
cities.
### Produced
data/property-tax adoption watch: Willow Park city added to adopted list (4 units now:
Aledo ISD, City of Weatherford, WISD, City of Willow Park); note that the flagship Willow
Park–Aledo ISD stack has 2 of 3 slices adopted, both down (~2¢ stack shrink pending the
county slice); WSISD pending note clarified; as-of 09-23. Full-stack roll into
wfl-data.js still deferred (county slices pending — no mixed-year stacks).
### Build + gate
Ten gates GATE PASSED ×2 (idempotent); URL auditor green; validator 311/0.
### Deployment status + verification + IndexNow
Commit/deploy from this session; live checks and IndexNow recorded in the shipping
commit sequence.
### Next recommended action
- Confirm Parker County adoption (minutes/order should post within days) — that
  completes the Willow Park and Weatherford stacks and triggers the wfl-data.js roll.
- WSISD/FWISD re-check; October month-roll due 10-01; operator still owes GSC coverage
  export + NETLIFY_AUTH_TOKEN secret.

---

## 2026-09-23 (supplemental) — WSISD $1.1528 and FWISD $1.029099 adopted: all four corridor ISDs done

- **Trigger:** Operator said "Continue" after the scheduled cycle's summary — deeper dig
  on the same adoption-watch item.
### Research
Found Tarrant County's official Truth-in-Taxation summary
(tarrantcountytx.gov /tax/property-tax/truth-in-taxation-summary.html), which renders
"Adopted Tax Rate" values inline — solving the WSISD PDF-only problem from the morning
run. VERIFIED there: **White Settlement ISD 2026 adopted $1.152800** (M&O $0.6928 + I&S
$0.46; down $0.0541 from $1.2069 — the corridor's largest school-district cut) and
**Fort Worth ISD 2026 adopted $1.029099** (M&O $0.7869 + I&S $0.242199; flat). Tarrant
County / JPS hospital district / TCC rows show empty 2026 cells (not yet adopted).
### Produced
- data/property-tax adoption watch: both districts added with source link; "completes
  all four corridor school districts for 2026–27, every one flat or down"; pending list
  narrowed to county-side slices + Parker County (still proposed $0.284719) + Aledo and
  Hudson Oaks cities.
- buy/homestead-exemption EN/ES (generator): adoption-watch paragraph extended with both
  adopted rates and exemption values (WSISD ~$1,614 at $140K / ~$2,306 at $200K; FWISD
  ~$1,441 / ~$2,058); verified date rolled to 2026-09-23. Main table stays on 2025–26
  rates until Parker-side figures are cross-confirmed on the official county record.
### Build + gate
Ten gates GATE PASSED, third pass idempotent no-op; URL auditor green; validator 311/0.
### Deployment + verification + IndexNow
Commit 9e06111 pushed; Netlify deploy 6ab44612 "Deploy is ready"; live checks: all three
pages 200 with $1.1528 and $1.029099 present, 404 handling intact; IndexNow 200 for
/data/property-tax, /buy/homestead-exemption, /es/comprar/exencion-homestead.
### Next recommended action
- Parker County adoption + Tarrant county-side slices (county/JPS/TCC) are now the only
  blockers for rolling full 2026–27 stacks into wfl-data.js and the homestead main table.
- Re-check Aledo & Hudson Oaks city adoptions; October month-roll due 10-01.

---

## 2026-09-24 — Adoption watch: no new adoptions; Aledo city proposed rate added (labeled proposed)

- **Trigger:** Operator "Continue" — next pass on the pending adoption-watch units.
### Research (all official/first-party checks)
- Parker County: financial-transparency page (parkercountytx.gov/155) still lists only
  proposed FY 2026–27 documents; adopted rates shown remain 2025–26 ($0.285070 total).
  Hearing was held 09-22 but no adoption posted. A Weatherford Democrat "Parker County
  adopts tax rate decrease" headline turned out to be from **2018** — rejected as a source.
- Tarrant County Truth-in-Taxation summary: Tarrant County, JPS, TCC 2026 cells still empty.
- City of Aledo: finance page posts a **proposed** FY 26–27 rate of $0.352415
  (M&O $0.267298 + I&S $0.085117), a shade under the current adopted $0.355353. NEW —
  publishable labeled proposed.
- Hudson Oaks: nothing published/findable.
### Produced
data/property-tax adoption watch only: as-of rolled to 09-24; Parker County sentence now
carries the proposed components and post-hearing status (hearing held, adoption not yet
on the official record); Aledo city proposed rate added with source link, marked
"proposed only, pending council adoption." No adopted-rate claims added; no table changes.
### Build + gate
Ten gates GATE PASSED ×2 then idempotent no-op; URL auditor green; validator 311/0.
### Deployment + verification + IndexNow
Commit f094575; Netlify deploy 6ab4eb41 "Deploy is ready"; live check 200 with $0.352415
and the 09-24 date present; IndexNow 200 for /data/property-tax.
### Next recommended action
- Parker County adoption should post to the transparency page within days — check the
  DocumentCenter for an adopted-budget/tax-rate order; that plus Tarrant county-side
  slices remain the gate for the full 2026–27 stack roll.
- Aledo city council adoption (from $0.352415 proposed); Hudson Oaks; October month-roll
  due 10-01; operator still owes GSC coverage export + NETLIFY_AUTH_TOKEN secret.

---

## 2026-09-24 (scheduled firing) — Mortgage-rate roll to 6.95% (PMMS), sitewide

- **Trigger:** Daily Routine fired 12:04 UTC. The adoption watch had already been checked
  and shipped earlier today (f094575 / deploy 6ab4eb41), so this run took the staleness
  scan's next finding.
### Staleness scan
Oldest live stamp on the site: calculator.html `RATE = 0.0675 // verified 2026-07-30`,
whose own config comment says "update RATE monthly" — 8 weeks overdue. Same stale rate in
assets/wfl-buy-data.js (`resale30: 6.75`, verified Jul 31, feeds the rent-vs-buy /
affordability / rent-or-buy town pages / VA-loans cluster) and wfl-data.js mortgage note.
Community-page "August 2026" verification stamps and the August rent report's ~6.75%
reference are contemporaneous archives/labels — left alone. Weatherford College guide
already freshness-passed 09-06.
### Research
Freddie Mac PMMS week of 2026-09-17: 30-yr fixed **6.95%** (up from 6.76%, highest since
January 2025) — confirmed on freddiemac.com/pmms AND Freddie Mac's own press release.
### Produced
Rate rolled to 6.95% in calculator.html (RATE, stamp, initial $195K→$200K to match the
formula at $1,650), es/calculadora (heuristic recomputed from the EN formula: $11,700→
$11,500 per $100, divisor 8.5→8.7, meta/lede/JS), es/index card, wfl-buy-data.js
resale30 + PMMS-dated note, wfl-data.js mortgage note. Builder buydown/incentive figures
untouched (not re-verified). Updated dates rolled to 09-24 on both calculator pages.
### Build + gate
Ten gates GATE PASSED ×2 then idempotent no-op; URL auditor green; validator 311/0.
### Deployment + verification + IndexNow
Commit 67a2e02; deploy 6ab51374 "Deploy is ready"; live: calculator, es/calculadora,
es/, and the served wfl-buy-data.js all show 6.95/11,500 with zero stale strings;
IndexNow 200 for the two calculator pages, es/, rent-vs-buy, affordability-calculator.
### Next recommended action
- Parker County adoption + Tarrant county-side slices (stack-roll gate); Aledo city
  ($0.352415 proposed) and Hudson Oaks; October month-roll due 10-01 — roll `resale30`
  again with the Builder Report per its note.

---

## 2026-09-25 — Daily cycle: comparison-page freshness pass (backlog #15)

- **Trigger:** Daily Routine fired 12:04 UTC.
### Staleness scan + adoption watch
Parker County: transparency page still proposed-only (new "Taxpayer Impact Statement"
doc posted, still no adopted budget; two more Democrat "approved" headlines checked and
both dated to prior years — rejected). Tarrant county-side 2026 cells (county/JPS/TCC)
still empty. Nothing new to adopt-watch today.
### Selection
Backlog #15 — Tier A/B defend-and-push on the two already-ranking comparison pages
(/compare/willow-park-vs-hudson-oaks GSC pos ~2; /compare/aledo-vs-weatherford pos ~8.5),
which still showed only 2024–25 stacks with no mention of the 2026–27 adoption wave.
### Produced
One clearly labeled "2026–27 adoption update (verified September 25, 2026)" paragraph
under each comparison table, built only from facts already verified on-site (Willow Park
city $0.429041; WISD $0.9342; City of Weatherford flat; Aledo ISD $1.1775; City of Aledo
$0.352415 labeled proposed; pending units named), each linking to the tax table's
adoption watch. Table figures + FAQ schema untouched (no mixed-year stacks). Bylines
rolled to 09-25. Inbound-link audit: both pages already have 8+ referrers incl. hubs and
data/property-tax — no new links needed.
### Build + gate
Ten gates GATE PASSED ×2 then idempotent no-op; URL auditor green; validator 311/0.
### Deployment + verification + IndexNow
Commit 171ceed; deploy 6ab66460 "Deploy is ready"; both pages live 200 with the update
paragraph and 09-25 date; IndexNow 200 for both URLs.
### Next recommended action
- Parker County adoption + Tarrant county-side slices (stack-roll gate); Aledo city and
  Hudson Oaks adoptions; October month-roll due 10-01 (specials + rent report + builder
  check + resale30 refresh per its note); operator still owes GSC coverage export +
  NETLIFY_AUTH_TOKEN secret.

---

## 2026-09-25 (supplemental) — Growth directive: compare-cluster expansion, tranche 1

- **Trigger:** Operator: "We need this site to be more, have more. It needs to bring in
  more traffic."
### Strategy (grounded in reports/seo/2026-08-28-opportunities.md)
Google ranks this site's compare cluster fastest (pos 2–16 on near-zero inbound links)
while generic national topics sit at pos 68–100 (testing, not ranking). Growth therefore
= expand proven clusters + widen the town footprint, never thin filler. Scored expansion
backlog added to the calendar (#16 compare build-out, #17 WISD campus files, #18 Brock →
Azle/Springtown town expansion, #19 cost-of-living file, #20 operator measurement items).
### Produced (tranche 1)
Two new comparison pages, template-faithful (Article+FAQPage JSON-LD, hardened form,
canonical, provenance note), every figure from the site's own verified layer:
- /compare/willow-park-vs-weatherford — price-vs-proximity ladder (2.091% vs 1.902%
  2024–25 stacks; Aledo ISD seam vs WISD 11 campuses; District/Crown Pointe vs courthouse
  square; commute delta) + labeled 2026–27 adoption update.
- /compare/hudson-oaks-vs-weatherford — shared-WISD matchup: ~1.32% median effective vs
  1.902% published stack; lightest line vs lowest entry prices + adoption note.
Wired: compare hub link list + JS pair map; inbound links from both towns' vibe files,
rent-or-buy-willow-park, rent-or-buy-weatherford. Site now 313 pages / sitemap 307.
### Build + gate
Ten gates GATE PASSED ×2 then idempotent no-op; URL auditor green; validator 313/0.
### Deployment + verification + IndexNow
Commit 242c44b; deploy 6ab6f36f "Deploy is ready"; both pages live 200 with canonical,
table and adoption paragraph; .html forms 301 to canonical; both in sitemap; IndexNow 200
(both URLs + /compare/).
### Next recommended action
- Tranche 2 (#17): WISD campus files off the TEA 2026 spreadsheet via the schools
  generator. Then #18 Brock town coverage (its ISD compare already ranks pos 3).
- OPERATOR: request GSC indexing for the two new URLs; fresh GSC coverage/performance
  export (owed since 09-22) to re-score the queue; NETLIFY_AUTH_TOKEN secret; decide on
  GA4 (CSP already allows it).

---

## 2026-09-26 — Daily cycle (growth tranche 2): ten Weatherford ISD campus files

- **Trigger:** Daily Routine fired 12:04 UTC; growth mode per operator directive 09-25.
### Adoption watch
Parker County transparency page still proposed-only (now also posts Taxpayer Impact
Statement, Elected Officials Salaries Notice, Notice of Estimated Taxes — all still
pre-adoption). No publish from the watch today.
### Selection
Backlog #17. Evidence: Aledo ISD campus pages rank pos 7.6–9.3 in GSC with near-zero
support; WISD had a hub but no campus pages despite the district's C→B 2026 story.
### Produced
Ten campus pages under /schools/weatherford-isd/ (WHS, Tison, Hall, Mary Martin, Austin,
Ikard, Seguin, Wright, Curtis, Crockett) on the Aledo campus template: TEA 2026-vs-2025
result per campus (from the on-site TEA data), campus-specific role notes (Tison D→B +14
— the corridor's biggest jump; Mary Martin as the Hudson Oaks seam campus; Crockett Pre-K
hub; Curtis −15 flagged with letter-grade caveats), written-zone-verification rule via
wisd.net, district tax math (published 1.0342% ≈ $1,448 exemption value; adopted $0.9342
for 2026–27 ≈ $1,308). Addresses from the hub's verified July 2026 directory — zero new
unverified claims. Hub directory links all ten. Site: 323 pages / sitemap 317.
### Build + gate
Ten gates GATE PASSED ×2 then idempotent no-op; URL auditor green; validator 323/0.
### Deployment + verification + IndexNow
Commit 390482d; deploy 6ab7b8a1 "Deploy is ready"; all 10 pages live 200, hub links live,
Tison's TEA line verified in production; IndexNow 200 (hub + 10 URLs).
### Next recommended action
- Tranche 3 (#18): Brock town coverage (its ISD compare ranks pos 3 bare). Then #19
  cost-of-living file. October month-roll due 10-01 (Thursday) — takes precedence.
- OPERATOR: request GSC indexing for the new URLs; fresh GSC export re-scores the queue.

---

## Entry template

```
## YYYY-MM-DD — <headline>

- **Trigger:**
### Staleness scan
### Selection
### Research + verification   (source URL + date verified for every figure)
### Safeguard decisions
### Produced                  (URLs, hub + reciprocal links, ES mirror, verified date)
### Build + gate              (GATE PASSED line, page/sitemap counts, idempotency check)
### Deployment status         (deploy ID, state, timestamp — or the blocker + recovery path)
### Production verification   (200 / 404 / sitemap / canonical / hreflang)
### IndexNow                  (URLs submitted, HTTP status — or why not)
### Next recommended action
```

---

