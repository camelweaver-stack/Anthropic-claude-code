# DEPLOY BRIEF — PCS Oahu (pcsoahu.com)
Build date: August 2026 · 24 pages · gate: PASSED

## What this is
Dedicated Oahu military/PCS publisher site — WFL family, its own brand. Educational content +
email capture only; referral-first lead routing (Hawaii pipeline).

## Package contents
- `site/` — deployable static site (24 pages incl. 404, assets, sitemap.xml, robots.txt)
- `gen/` — Python generator (`build.py`) + QA gate (`gate.py`). Edit content in gen/, rebuild,
  re-gate, redeploy. Never hand-edit site/ without re-running the gate.
- `indexnow-payload.json` — IndexNow submission body (key placeholder, see step 5)
- `REFRESH_RUNBOOK.md` — the data cadence that powers the freshness edge (gate-enforced)
- `PITCH_KIT.md` — BAH Reality Report link-outreach targets + drafted templates (fire in December)

## Claude Code deploy steps
1. `cd gen && python3 build.py && python3 gate.py` — must print GATE PASSED.
2. Point pcsoahu.com DNS at host; deploy `site/` as web root.
3. Verify live: `/`, `/bases/pearl-harbor-hickam.html`, `/bah-report/`, `/pcs-checklist/`
   (check localStorage progress save), `/tools/` (all three calculators compute).
4. Submit `sitemap.xml` in Google Search Console + Bing Webmaster.
5. IndexNow: generate a key, drop `{key}.txt` at site root, replace both placeholders in
   `indexnow-payload.json`, POST to `https://api.indexnow.org/indexnow`.

## Chris — human checklist
- [ ] **Register pcsoahu.com** (verified available Aug 1, 2026 — RDAP 404 + no DNS; re-check at
      registrar before assuming).
- [ ] **FormSubmit activation:** submit one test lead from EACH tag so FormSubmit activates the
      endpoint per-form and Anastasia confirms receipt. Tags in this build:
      HOME, BASES, JBPHH, SCHOFIELD, MCBH, CAMPSMITH, TRIPLER, USCG, BAHREPORT, NEIGHBORHOODS,
      SCHOOLS, BUY, SELL, CHECKLIST, TLA, GUIDES, SPOUSE, SCHOOLTRANSITION, PETS, TOOLS,
      SHAFTER, QUIZ, ONBASE, NOTFOUND.
      All carry `audience=referral-hi-oahu-pcs` + `segment=pcs-renter|pcs-buyer|pcs-seller`.
- [ ] **GSC inspection priorities (in order):** `/bah-report/` (the backlink asset), `/buy/`
      (flagship VA brief, FAQ schema), the six `/bases/*` pages, `/sell/`, home.
- [ ] **Spec note — documented deviation:** house spec says renter-page forms use the lease-end
      question. On a PCS site, inbound "renters" have report dates, not local leases, so ALL
      inbound forms (pcs-renter + pcs-buyer) use the move_date field ("When are you planning to
      move?", optional); seller forms use sell_timeline (optional). The gate enforces this
      mapping. If you want lease-end anywhere, say the word and we re-gate.
- [ ] **Photography:** build ships zero photos by design (no fabricated imagery). Before or soon
      after launch, add licensed/CC island + base-adjacent photography with credits in the footer
      (WFL pattern). Hero sections are designed to take a background image drop-in.
- [ ] **SMS join path (flag-gated, currently OFF):** set `SMS_NUMBER` in gen/common.py to the
      E.164 number for the HI list (do NOT reuse the WFL TX line without deciding routing),
      rebuild + gate — SMS buttons then render next to every form's submit. Until set, no
      broken buttons ship.
- [ ] **404 page:** configure the host to serve /404.html for not-found routes (Netlify:
      automatic by filename; other hosts: set error document).
- [ ] **Social cards:** og-card.png ships as the sitewide share image; every page carries full
      OG/Twitter meta. Test one URL in a card validator post-deploy.
- [ ] **llms.txt** ships at root — AI-assistant citability surface; keep it in refresh scope.
- [ ] **SEO launch order:** deploy → sitemap to GSC/Bing + IndexNow same day → request
      indexing on /bah-report/, /sell/, /buy/, then the eight /bases/ pages. Uncontested
      clusters (sell-side, per-base live-on-or-off, pet quarantine) are the first-rankings play.
- [ ] **Deferred by decision (Aug 2026):** the reviewed-by byline / Person schema (E-E-A-T
      item) is built into the plan but NOT the build — revisit when Anastasia signs off.
- [ ] **BAH cycle calendar item:** the BAH Reality Report and all rate lines refresh when DTMO
      publishes 2027 rates (December 2026). Rent bands: refresh quarterly minimum, monthly in
      PCS season.

## Data provenance (for refresh discipline)
- BAH anchors: DTMO 2026 tables, Honolulu County MHA, effective Jan 1 2026 (E-5 w/dep $3,663,
  E-6 w/dep $3,912, floor ~$2,598, ceiling ~$5,040, +4.4%). One MHA covers all six installations.
- Market medians: Oahu June 2026 — SF $1,275,000, condo $530,000 (Honolulu Board of REALTORS®
  data via public market reports).
- Rent bands: public listing platforms (Zumper/Redfin/Rent.com), mid-2026, deliberately rounded.
- Loan limits: FHFA 2026 — national baseline $832,750, HI statutory ceiling $1,873,675. Sources
  conflict on the exact Honolulu County figure (~$1.2–1.25M): site copy deliberately hedges to
  the FHFA map rather than printing a number we couldn't confirm from the primary source.
- HARPTA: 7.25% non-resident withholding per HI Dept of Taxation; copy directs verification there.

## House-rule compliance summary
Publisher mode ✓ (gate greps forbidden service language) · 10-link nav ✓ (no language link —
no second language ships; gate asserts zero hreflang) · EHO + data disclaimers every page ✓ ·
No crime/safety rankings, no school rankings, no steering, no lender placements ✓ · Named data
product ✓ (The BAH Reality Report) · JSON-LD: WebSite (home), FAQPage (/buy/, /bah-report/),
Article (bases, guides, /sell/, /tla/, /schools/) ✓ · Tone: zero hooah-kitsch; every base and
program name verified against current public sources ✓
