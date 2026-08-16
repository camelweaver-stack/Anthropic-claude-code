# PCS Oahu — Daily Audit Log

Append-only. Newest entry on top. One record per daily run. Template at the bottom.

---

## 2026-08-16 — HARPTA for outbound military sellers (BUILT + GATE-GREEN, **NOT DEPLOYED — NEEDS REVIEW**)

- **Date/time:** 2026-08-16 (America/Honolulu editorial day)
- **Selected topic:** HARPTA — Hawaii's 7.25% withholding on dispositions of Hawaii real property,
  written for outbound military sellers on Oahu. Backlog #2, the standing `NEXT` item.
- **Reason for selection:** Highest-utility unshipped backlog item (Traffic M / Transaction H) and
  the correct cluster rotation — the last three ships were PCS logistics, PCS logistics, and
  Buying/VA, so Selling/Leaving Hawaii was the balanced draw. It also absorbed a real staleness
  finding (below): the `/sell/` hub carried two materially wrong HARPTA statements, so the
  fix-an-existing-page path and the new-page path were the same piece of work.
- **Audience:** Outbound service members and families selling an Oahu home on PCS orders.
- **Content type:** Evergreen tax-process explainer (publisher mode; explicitly not tax advice).
- **URL:** `/guides/harpta.html` — **built and gate-green locally, not live.**

### Staleness scan (all six checks in `editorial/staleness-scan.md`)
1. **Data freshness** — `LAST_REFRESHED` August 1, 2026; `BUILD_DATE` August 2026; `BAH_YEAR` 2026;
   medians June 2026. All inside cadence (rent-band refresh next due 2026-09-01; medians quarterly;
   BAH on the December DTMO cycle). No action.
2. **Date/edition drift** — 51 `2024|2025` matches, all inside the shared photo-credit block
   ("2025 Pearl Harbor 02" is a Wikimedia filename). No visible-copy drift. No action.
3. **Expired/time-bound content** — none; site is still evergreen. No action.
4. **Broken / orphan / duplicate** — internal-link target check clean (0 missing); duplicate-title
   check clean; only orphans are `/404.html` and the noindex `embed/bah-widget.html`, both
   intentional. No action.
5. **Sitemap parity + gate** — baseline `GATE PASSED — 50 pages, 48 sitemap URLs` before changes.
6. **Sourcing weakness — TWO DEFECTS FOUND AND FIXED** on `/sell/` (see below).

### Corrections made to an existing page (`/sell/`)
Both checked against Hawaii DOTAX Tax Facts 2010-1 (rev. April 2025), the Department's own guidance:
- **"7.25% of the gross sale price" → "7.25% of the amount realized."** The statute withholds on the
  *amount realized*, which the Department explicitly distinguishes from the sales price (it also
  includes the fair market value of property received and any liability the buyer assumes). Appeared
  twice in copy plus once in the FAQ JSON-LD.
- **"It does not apply to Hawaii residents at closing" → corrected.** The Department names this by
  name as a common misperception: HARPTA *does* apply when the seller is a Hawaii resident; the buyer
  is simply not required to withhold *if the seller gives the buyer Form N-289*. A resident seller who
  never hands over the form gets 7.25% withheld anyway, and a buyer who fails to withhold is
  personally liable. This was the more consequential of the two — it told resident sellers they were
  automatically safe.
- Also softened "service members … are typically non-residents for HARPTA purposes" to match what the
  source actually supports: residency turns on domicile *and* the purpose of presence under TIR 97-1,
  and a mainland state of legal residence does not settle it in either direction.

### Sources used (verified 2026-08-16)
- **Hawaii DOTAX, Tax Facts 2010-1, "Understanding HARPTA" (rev. April 2025)** —
  `https://files.hawaii.gov/tax/legal/taxfacts/tf2025-2010-1.pdf`. HRS §235-68; 7.25% of the amount
  realized; withholding is an estimated tax payment, not a tax; the resident misperception (Q2); the
  three Form N-289 exemptions incl. the $300,000 principal-residence ceiling (Q31); Forms N-288/N-288A
  due the 20th day after the transfer date (Q9); Form N-288C tentative refund and escrow's inability
  to claim it (Q7, Q26); Hawaii's conformity to IRC §121 and the rule that N-288B is unavailable if
  any gain remains after the exclusion (Q21); resident/nonresident definitions and the TIR 97-1
  pointer (Q4); DOTAX phone numbers (p.8).
- **Hawaii DOTAX, Instructions for Form N-288B (rev. 2025)** —
  `https://files.hawaii.gov/tax/forms/current/n288b_i.pdf`. The 10-working-day pre-transfer filing
  deadline, verbatim, plus the consequence for late filings.
- **Hawaii DOTAX, TIR 97-1, "Determination of Residence Status"** — cited for residency determination.
- **IRS Publication 523, "Selling Your Home"** — `https://www.irs.gov/publications/p523`. §121
  exclusion $250,000 / $500,000 MFJ; uniformed-services suspension of the five-year test capped at
  **10 years**; qualified official extended duty = duty station ≥ **50 miles** from the home under
  orders for an indefinite period or a definite period of **more than 90 days**.
- Arithmetic disclosure: the two "HARPTA withheld" figures (≈$92,400 and ≈$38,400) are 7.25% of this
  site's own published June 2026 medians ($1,275,000 → $92,437.50; $530,000 → $38,425), rounded and
  labelled in the source line as scale-only, not a quote or tax computation.
- **Nothing was asserted that a source did not carry.** The one place the honest answer was "it
  depends" — whether a given service member is a Hawaii "resident person" — is written as
  fact-specific and routed to DOTAX/TIR 97-1 rather than resolved on the page. The §121 military
  suspension is labelled as a *federal* election with Hawaii treatment to be confirmed, because Tax
  Facts states conformity to §121 generally but does not address §121(d)(9) specifically.
- **Facts requiring future revalidation:** the 7.25% rate (statutory, last changed 2018); the $300,000
  N-289 ceiling; the 10-working-day N-288B deadline (recheck at each form revision); §121 exclusion
  amounts; DOTAX phone numbers; the June 2026 medians when the quarterly refresh lands.
- **Internal links added:** New page → `/sell/`, `/pcs-checklist/`, plus nav/footer. Reciprocal links
  added **FROM** `/sell/` (hub, in-body), `/guides/` (hub, new Departing card), and
  `/guides/rent-vs-buy.html` (existing page, forced-exit callout), plus the shared footer
  ("Buying & Selling" list) which puts it on all 50 other pages.
- **CTA used:** "Selling the Oahu house on this set of orders?" → lead form, segment `pcs-seller`,
  context `sell` (so `sell_timeline`, per the gate's seller-form rule), tag `PCSOAHU-HARPTA`.
- **Files changed:** `gen/pages_content.py` (new `harpta()`, wired into `build()`; guides-hub card;
  `/sell/` corrections; `/guides/rent-vs-buy.html` reciprocal), `gen/common.py` (footer link).
  Regenerated `site/` (51 pages), `site/sitemap.xml` (49 URLs), `indexnow-payload.json`.
- **Build status:** `GATE PASSED — 51 pages, 49 sitemap URLs, all assertions green.`

### Deployment status: **NOT DEPLOYED — held under safeguard (deleting major pages / material redesign)**

Deploying this branch's `site/` today would have been destructive to production. Evidence gathered
before attempting any deploy:

- The currently published Netlify deploy is **`6a81d76309294fc3d42c8fe5`**, state `ready`, published
  **2026-08-16T15:30:11Z — roughly 25 minutes before this run started** — from branch
  **`claude/pcs-oahu-deploy-dd373n`**, titled *"SEO: canonical unification, 2026 BAH table, orphan
  rescue (draft v2)"*, `manual_deploy: true`, context `deploy-preview`.
- Production's live sitemap carries **59 URLs**; this branch builds **49**. Diffing the two
  (normalizing the `.html` suffix) shows **production is a strict superset** — every page this branch
  builds is already live, and **11 live URLs exist only in production**:
  `/family/` + its 8 children, `/tools/commute-grid/`, and `/bah-report/2026-rates/`.
- Separately, **29 pages would change URL form**: production serves extensionless canonicals
  (`/guides/rent-vs-buy`), this branch emits `.html` canonicals. Deploying would flip the canonical
  tag on 29 already-indexed pages and reintroduce `.html` into the sitemap.
- Net effect of a deploy: **delete 11 live pages, churn 29 canonicals, roll back a 25-minute-old
  deploy** from another workstream that was explicitly about canonical unification and orphan rescue.

That lands squarely on two items in the do-not-auto-publish list in `DAILY_RUN.md` — *deletion of
major pages* and *material redesigns* — so per the runbook the correct action was to build, gate, and
**stop**. No deploy was attempted; no force; production is untouched and still serving the dd373n
build. This is the same branch-divergence risk flagged in the 2026-08-10 entry, now materially worse:
it is no longer 9 untracked pages, it is a full URL-convention fork plus a live deploy from the other
branch.

- **IndexNow:** **not submitted.** Nothing changed in production, so pinging would have been a false
  freshness signal. `indexnow-payload.json` is regenerated in the repo and ready for the operator.
- **Production verification:** N/A — nothing deployed. Confirmed production is unchanged and healthy
  after this run: `/` 200, `/sell/` 200, `/family/` 200, `/tools/commute-grid/` 200, `/sitemap.xml`
  200 (still 59 URLs), nonexistent path 404, `/guides/rent-vs-buy.html` 301 → the extensionless
  canonical (expected under production's current convention).

### Recovery path / what the operator needs to decide
The last green `site/` for this branch is committed on
`claude/pcs-oahu-daily-publishing-1289q3`; nothing is lost and nothing is half-applied. Publishing
`/guides/harpta.html` needs one of:
1. **Treat `dd373n` as production source** — port `harpta()` and the `/sell/` corrections into that
   branch and deploy from there. Fastest path to getting today's item live; leaves the fork in place.
2. **Reconcile onto `1289q3`** — port `/family/` (9 URLs), `/tools/commute-grid/`, and
   `/bah-report/2026-rates/` into this generator *and* switch `page()` to extensionless canonicals so
   the build matches what is already indexed, then deploy. This is the durable fix and would let the
   daily engine run unblocked, but it is a material change to every canonical on the site and wants an
   explicit go-ahead.
3. Retire one branch outright.
Until one of those happens, **the daily cycle cannot deploy from `1289q3` without destroying live
pages** — this is now a hard blocker on the engine, not a background risk.

- **Next recommended related topics:** Backlog #3 (fee simple vs leasehold) pairs naturally with this
  one on the Buying/Selling axis; #5 (on-base waitlist mechanics) and #4 (DoDEA vs Hawaii DOE) remain
  the highest-utility unshipped items in other clusters.

---

## 2026-08-10 — Lead-form security fix (Session 1, Where In DFW Acceleration Plan)

- **Trigger:** Explicit task from the operator's Acceleration Plan (Drive doc 21): "PCS Oahu form
  fix — carried forward as the first item of Session 1," itself carried forward from a gap flagged
  in the Phase 0 current-state audit (F1: cleartext lead-routing email harvestable from every
  page's HTML, no spam/consent protections).
- **Fix:** `gen/common.py`'s `lead_form()` (single-sourced, every form on the site calls it):
  switched `action` from cleartext `formsubmit.co/leads@anastasiaweaver.com` to the hashed
  `formsubmit.co/c86195fac91694c985b7fc55c96e4f77` (WFL's already-activated hash for the same
  destination email — FormSubmit's hash is a privacy proxy for the address, not domain-locked, so
  reuse is safe); added an off-screen `_honey` honeypot field; added a required `consent`
  checkbox. Worded the consent copy without a privacy-policy link, since the WFL pattern this
  mirrors links to a `/privacy/` page that doesn't actually exist on either site yet.
- **Files changed:** `gen/common.py` (form template), `gen/gate.py` (three new/updated
  assertions: hashed endpoint required, honeypot required, consent checkbox required, plus a
  page-wide defense-in-depth check that the cleartext endpoint never appears anywhere). Regenerated
  all of `site/` (50 pages).
- **Build status:** `GATE PASSED — 50 pages, 48 sitemap URLs, all assertions green.` (verified the
  new assertions actually run, not just that the old one was removed).
- **Deployment status:** DEPLOYED to production. Netlify project `pcsoahu`, deploy
  `6a7939b617469016cf4a8405`, state `ready`, published 2026-08-10T02:38:56Z (8s, context
  production, alias pcsoahu.com). Secret scan clean (0 matches, 193 files scanned).
- **Production verification:** PASS — full `CLAUDE_CODE_DEPLOY.md` §3 checklist run: all 13 listed
  routes 200, nonexistent route 404, canonical on `/buy/` correct. Rendered check (not grep) of
  the live homepage form confirms the new markup byte-for-byte. Did **not** test-submit the form
  per `CLAUDE_CODE_DEPLOY.md` §5 — that's reserved for the operator's one deliberate test.
- **Anomaly found (pre-existing, not caused by this change, not fixed here):** deployed from
  `claude/pcs-oahu-daily-publishing-1289q3` (the branch this asset's driver-doc entry names as the
  working branch). That branch is missing 9 pages that exist on `claude/pcs-oahu-deploy-dd373n`
  (the "production-source" branch) — the whole `/family/` section (8 pages) and
  `/tools/commute-grid/` — not referenced anywhere in `1289q3`'s generator, nav, or sitemap.
  Checked post-deploy: all 9 are **still live** (200, confirmed fresh from origin, not a cache
  artifact) — Netlify's deploy here does not wholesale-replace the published directory, so no
  content was lost. But this means those 9 pages are now orphaned relative to `1289q3`'s own
  bookkeeping (invisible to its sitemap/gate) and their presence in production silently depends on
  a Netlify deploy-retention behavior rather than being tracked by any branch's `site/`. Same class
  of branch-divergence risk as the 2026-08-06 floating-launcher regression above — that incident
  ported content forward once; this drift (family layer + commute-grid) hasn't been. Flagging for
  the operator rather than reconciling here — out of scope for a targeted form-security fix on a
  live site.
- **Next recommended action:** either port `/family/` + `/tools/commute-grid/` forward into
  `1289q3` (mirroring the 2026-08-06 fix pattern) so they're tracked and gated, or formally retire
  `dd373n` as a concept and treat `1289q3` as the sole source of truth — the two-branch setup is an
  ongoing regression risk as long as they keep diverging silently.

---

## 2026-08-06 (maintenance) — Restore the site-wide floating "Ask" launcher (regression)

- **Trigger:** User — "It used to be a floating input box. Now it's not there."
- **Root cause (branch divergence I introduced):** The site-wide floating concierge launcher
  (`#pcs-ask-launcher`, a fixed bottom-right button + slide-up chat panel on every page) was built
  on the `claude/pcs-oahu-deploy-dd373n` line (commit `fd8a201`, "Surface the AI concierge … sitewide
  floating launcher"; carried through the family-layer work). Production/Netlify is tied to that
  branch alias, so the live site had the launcher. The publishing branch I was told to deploy from,
  `claude/pcs-oahu-daily-publishing-1289q3`, forked from `2881533` **before** `fd8a201` and never had
  it. My deploys earlier today (rent-vs-buy, then the nav/concierge fix) shipped `1289q3`'s `site/`
  over production — an atomic snapshot — which removed the floating launcher. The earlier "add Ask to
  nav" change added a header link but not the floating box the user was actually describing.
- **Fix:** Ported the original launcher verbatim from `dd373n` (`345f10c:gen/common.py`) into
  `1289q3`: `CHAT_LAUNCHER` constant in `gen/common.py`, injected by `page()` on every page except
  `/ask/` (which is the full chat) and the standalone noindex `embed/bah-widget.html` iframe.
  Restored the gate's regression guard so the launcher can never silently disappear again
  (`gen/gate.py`: require `id="pcs-ask-launcher"` on all pages except those two; fail if present on
  `/ask/`). Same `/.netlify/functions/concierge` endpoint; dark-mode styles included.
- **Files changed:** `gen/common.py` (CHAT_LAUNCHER + page() injection), `gen/gate.py` (launcher
  regression check). Rebuilt `site/` (50 pages) — launcher now on 48 pages (all but `/ask/` and the
  raw embed iframe).
- **Build status:** `GATE PASSED — 50 pages, 48 sitemap URLs, all assertions green.`
- **Deployment status:** DEPLOYED to production. Netlify `pcsoahu`, deploy `6a752f2d899b5dd12de94ef8`,
  state `ready`, published 2026-08-07T01:04:57Z (10s, context production). 49 pages + concierge
  function; secret scan clean (126 files). One transient 502 on the first connector call; succeeded on
  retry after backoff. IndexNow POSTed (HTTP 200) for `/`.
- **Production verification:** PASS — floating launcher + input box (`#pcs-ask-launcher` / `#pcsAskQ`)
  live on `/`, `/buy/`, `/bases/tripler.html`, `/guides/rent-vs-buy.html`; suppressed on `/ask/`;
  `/` and `/ask/` 200, nonexistent route 404.
- **Follow-up / known divergence:** `dd373n` also carries a `site/family/…` layer that `1289q3` does
  not. Deploying `1289q3` means those family pages are not in the current production snapshot. Not
  addressed here (out of scope for this request) — flagged for the operator to decide whether to
  reconcile the two branches.

---

## 2026-08-06 (maintenance) — AI concierge investigation + nav discoverability fix

- **Trigger:** User report — "the AI chat widget is missing or not working."
- **Diagnosis:** The `/ask/` concierge is **not broken**. Live-tested the production
  function (`/.netlify/functions/concierge`) — HTTP 200 with a genuine Claude answer; the
  `ANTHROPIC_API_KEY` is set and the model (`claude-sonnet-4-6`) is valid. Root cause of the
  "missing" perception: `/ask/` was linked only from the footer and the Data Desk card — it was
  **not** in the fixed 10-item primary nav, so there was no header entry point (and no site-wide
  floating widget). Also found two content bugs in the concierge's system prompt.
- **Changes (approved by operator):**
  1. **Nav:** added `("/ask/", "Ask")` to `NAV_LINKS` (now 11 items); bumped gate
     `NAV_EXPECTED` 10→11; set the `/ask/` page's active-nav state to `/ask/`. Nav now renders
     site-wide, so all pages rebuilt.
  2. **Concierge factual fix:** system-prompt knowledge said Hawaii vehicle registration is due
     "within 10 days" of arrival — corrected to **30 days** (same error fixed across the site
     earlier today; verified vs. Honolulu CSD + HRS 286).
  3. **Concierge guardrail:** added a hard rule forbidding the model from naming third-party
     listing sites/apps/brokerages (Zillow, Apartments.com, Redfin, Trulia, Realtor.com, Hotpads,
     etc.) — it had violated the existing "no paid services" rule in a live answer.
- **Files changed:** `gen/common.py` (NAV_LINKS), `gen/gate.py` (NAV_EXPECTED), `gen/pages_phase_a.py`
  (ask() current-nav), `netlify/functions/concierge.js` (30-day fix + third-party guardrail). Rebuilt
  `site/` (50 pages), sitemap (48 URLs).
- **Build status:** `GATE PASSED — 50 pages, 48 sitemap URLs, all assertions green.`
- **Deployment status:** DEPLOYED to production. Netlify `pcsoahu`, deploy `6a750adcaf1df642e8626581`,
  state `ready`, published 2026-08-06T22:30:06Z (16s, context production). 49 pages + concierge
  function; secret scan clean (126 files). IndexNow POSTed (HTTP 200) for `/` + `/ask/`.
- **Production verification:** PASS — homepage nav now has 11 links incl. "Ask"; `/`, `/ask/`,
  `/buy/`, `/guides/rent-vs-buy.html`, `/sitemap.xml` all 200; nonexistent route 404. Live concierge
  test now answers "30 days" (no "10 day") and declines to name listing platforms.

---

## 2026-08-06 — Rent vs. buy on Oahu with a VA loan (decision framework)

- **Date/time:** 2026-08-06 (America/Honolulu editorial day).
- **Selected topic:** Backlog #1 — Rent-vs-buy on Oahu with a VA loan (BAH purchasing power, the
  PCS break-even horizon, the leasehold/forced-exit risk).
- **Reason for selection:** Highest-utility scored backlog item (H traffic / H transaction, status
  NEXT; the recommended next topic in both prior audit entries). Cluster balance: the last two
  ships were both PCS-logistics (household goods, vehicle registration), so a Buying/VA decision
  page diversifies the mix. Targets a distinct decision-stage query ("should i buy a house in
  hawaii military") that the existing `/buy/` mechanics page does not serve — `/buy/` assumes the
  buy decision is made and explains entitlement; this page is the decision *before* that. No filler;
  a genuine content gap with authoritative, verifiable sources.
- **Audience:** Inbound service members/families weighing rent vs. buy (all grades); buyer-side CTA
  (`pcs-buyer`).
- **Content type:** Evergreen decision-framework guide.
- **URL:** https://pcsoahu.com/guides/rent-vs-buy.html
- **Sources used (verified 2026-08-06):**
  - VA.gov — VA-backed purchase loan benefits: no down payment (up to appraised value), no PMI
    (va.gov/housing-assistance/home-loans/loan-types/purchase-loan/).
  - VA.gov — funding-fee exemption for those receiving/eligible for VA compensation for a
    service-connected disability (va.gov/housing-assistance/home-loans/funding-fee-and-closing-costs/).
  - Military OneSource — BAH excluded from gross income; not subject to federal/state income tax
    (militaryonesource.mil/financial-legal/taxes/military-housing-allowance/).
  - `gen/common.py` anchors — DTMO 2026 BAH (E-5 dep $3,663, E-6 dep $3,912, ceiling $5,040,
    effective Jan 1 2026; one Honolulu County MHA) and Honolulu Board of REALTORS® June 2026 medians
    ($1,275,000 SF / $530,000 condo).
- **Facts requiring future revalidation:** BAH anchors at the next DTMO cycle; June 2026 medians at
  the next quarterly refresh; VA funding-fee schedule and conforming-limit figures (deliberately
  described qualitatively / pointed to source rather than asserting a percentage or exact county
  cap). No specific closing-cost or break-even number was invented — all framed as ranges/"years."
- **Maintenance fix (staleness pass):** Corrected a lingering factual error on the guides hub — the
  vehicle-shipping card still read "the 10-day registration clock"; the registration deadline is
  **30 days** (fixed everywhere else in the 2026-08-05 run-2 pass). Now reads "30-day registration
  clock." Full staleness scan otherwise clean: no broken internal links, no duplicate titles, no
  year-drift in copy (2024/2025 matches are image-credit filenames only), anchors current.
- **Internal links added:** New page → `/buy/` (hub), `/sell/`, `/bah-report/`, `/on-base/`, and the
  two VA.gov + Military OneSource sources inline. Reciprocal links added FROM: `/buy/` (honest-close
  paragraph → rent-vs-buy framework), guides hub (new Buying card), site footer (Buying & Selling
  list).
- **CTA used:** "Weighing the rent-or-buy call this tour?" → lead form, segment `pcs-buyer`, tag
  `PCSOAHU-RENTBUY`, context `move_date`.
- **Files changed:** `gen/pages_content.py` (new `rent_vs_buy()` + build wiring + guides-hub card +
  `/buy/` reciprocal link + 10→30-day hub fix), `gen/common.py` (footer link). Regenerated `site/`
  (50 pages), sitemap (48 URLs), `indexnow-payload.json`.
- **Build status:** `GATE PASSED — 50 pages, 48 sitemap URLs, all assertions green.`
- **Deployment status:** DEPLOYED to production. Netlify project `pcsoahu`, deploy
  `6a74bab8bc9c1e2700fb9a03`, state `ready`, published 2026-08-06T16:48:12Z (17s, context
  production). 50 files + concierge function; secret scan clean (125 files, 0 matches). Deployed via
  the Netlify deploy-site connector (`npx @netlify/mcp --no-wait`; polled to `ready`).
  IndexNow POSTed (HTTP 200) for the new page + `/buy/` + `/guides/` (host pcsoahu.com, key file
  live at /12ef30fd51aefc63524ab6eb41e58f99.txt).
- **Production verification:** PASS — `/guides/rent-vs-buy.html` HTTP 200 (pretty URL
  `/guides/rent-vs-buy` also 200); `/buy/`, `/guides/`, `/sell/`, `/bah-report/`, `/`, `/sitemap.xml`
  all 200; nonexistent route 404; new URL present in live sitemap.xml; canonical =
  https://pcsoahu.com/guides/rent-vs-buy.html (apex); reciprocal link live on `/buy/`; the 30-day
  hub fix is live.
- **Next recommended related topics:** Backlog #5 (on-base housing waitlist mechanics by
  installation), #4 (DoDEA vs Hawaii DOE for PCS kids), #2 (HARPTA outbound seller's proceeds) —
  see EDITORIAL_CALENDAR.md. (Rotate clusters: next non-Buying to keep the mix honest.)

---

## 2026-08-05 (run 2) — Registering a car in Hawaii (vehicle-registration guide)

- **Date/time:** 2026-08-05 — process-verification run against the Daily Publishing Driver.
- **Selected topic:** Registering an imported vehicle on Oahu for PCS families.
- **Reason for selection:** High-utility PCS-logistics gap the site already gestured at (the
  vehicle-shipping page referenced a "registration clock" with no dedicated page). Concrete,
  verifiable facts; low safeguard risk; strong internal-linking value. Different enough from the
  run-1 HHG guide to preserve cluster variety.
- **Audience:** Inbound PCS service members/families with a POV; renter-leaning CTA.
- **Content type:** Evergreen procedural guide.
- **URL:** https://pcsoahu.com/guides/vehicle-registration.html
- **Sources used (verified 2026-08-05):** City & County of Honolulu, Dept. of Customer Services
  (motor-vehicle registration + military service-members pages: Form CS-L(MVR)50 dated 04/2026,
  out-of-state permit CS-L(MVR)27, nonresident weight-tax exemption, failed-inspection sequence);
  Hawaii DOT (safety inspection); HRS ch. 286 / capitol.hawaii.gov (30-day-from-arrival deadline).
- **Maintenance fix (staleness pass):** Corrected a live factual error on `/vehicle-shipping/` —
  the registration deadline is **30 days from arrival on Oahu**, not "10 days" (was asserted in 4
  places). Verified against Honolulu CSD + HRS 286. Added reciprocal link to the new guide.
- **Facts requiring future revalidation:** CS-L(MVR)50/27 form versions and the 04/2026 date;
  safety-inspection fee (state updated 2025); the 30-day windows; Satellite City Hall / JBPHH
  registration availability.
- **Internal links added:** New page → vehicle-shipping, pcs-checklist, on-base. Reciprocal from
  vehicle-shipping (FAQ + section 8), guides hub (new card), footer.
- **CTA used:** "Working the arrival checklist?" → lead form, segment `pcs-renter`, `PCSOAHU-VEHREG`.
- **Files changed:** `gen/pages_content.py` (new `vehicle_registration()` + build wiring + hub card),
  `gen/common.py` (footer link), `gen/pages_vehicle.py` (10→30-day fix + reciprocal link).
  Regenerated `site/` (49 pages), sitemap (47 URLs), indexnow-payload.json.
- **Build status:** `GATE PASSED — 49 pages, 47 sitemap URLs, all assertions green.`
- **Deployment status:** DEPLOYED to production. Netlify `pcsoahu`, deploy
  `6a73afcf97402e20214f1242`, state `ready`, published 2026-08-05T21:49:15Z (10s, context
  production). Secret scan clean. (One transient 502 on the first deploy call; succeeded on retry.)
  IndexNow pinged (HTTP 200) for the new page + `/guides/` + `/vehicle-shipping/`.
- **Production verification:** PASS — new page HTTP 200; `/vehicle-shipping/`, `/guides/`,
  `/sitemap.xml` 200; nonexistent route 404; new URL in live sitemap; canonical = apex; the
  `/vehicle-shipping/` fix is live (no "10 days"; now "30 days").
- **Next recommended related topics:** Backlog #1 (rent-vs-buy with a VA loan), #5 (on-base waitlist
  mechanics), #4 (DoDEA vs Hawaii DOE) — see EDITORIAL_CALENDAR.md.

---

## 2026-08-05 — Household goods to Hawaii (OCONUS HHG guide)

- **Date/time:** 2026-08-05 (America/Honolulu editorial day)
- **Selected topic:** Shipping household goods to Hawaii on PCS orders — the OCONUS move
- **Reason for selection:** High-demand PCS-logistics query with a clear content gap. The site
  already covered the two companion inbound-shipping decisions (vehicle shipping, pets) but not
  the largest one — household goods. Fills the missing third leg and strengthens the PCS-logistics
  cluster with strong internal-linking value. Sources are authoritative and readily verifiable.
- **Audience:** Inbound PCS service members and families (all grades); renter-leaning CTA.
- **Content type:** Evergreen process guide.
- **URL:** https://pcsoahu.com/guides/household-goods.html
- **Sources used (verified 2026-08-05):**
  - Military OneSource — Personal Property / OCONUS moves / PCS entitlements (UB, pro-gear incl.
    spouse 500-lb cap, consumables allowance concept, "weeks to months" transit).
  - Move.mil / DPS — booking system, shipment types, 833-MIL-MOVE (833-645-6683) call center.
  - DTMO / Joint Travel Regulations — weight allowances by grade; OCONUS administrative-reduction
    location list.
  - MilitaryINSTALLATIONS (Schofield Barracks / Fort Shafter) — local transportation office
    address + phone.
- **Facts requiring future revalidation:** Whether any specific Oahu installation appears on the
  DTMO administratively-reduced-allowance list or the Authorized Consumable Goods Allowance list
  (deliberately not asserted — reader directed to their TO). Local TO address/phone/hours. Spouse
  pro-gear cap and consumables poundage (JTR-set; recheck at next JTR change).
- **Internal links added:** New page → vehicle-shipping, pets-to-hawaii, TLA, school-transition,
  pcs-checklist. Reciprocal links added FROM: guides hub (new card), site footer (Arriving list),
  vehicle-shipping intro (three-clocks paragraph).
- **CTA used:** "Building your shipment plan?" → lead form, segment `pcs-renter`, `PCSOAHU-HHG`.
- **Files changed:** `gen/pages_content.py` (new `household_goods()` + wired into `build()` +
  guides-hub card), `gen/common.py` (footer link), `gen/pages_vehicle.py` (reciprocal link).
  Regenerated `site/` (48 pages), `site/sitemap.xml` (46 URLs), `indexnow-payload.json`.
- **Build status:** `GATE PASSED — 48 pages, 46 sitemap URLs, all assertions green.`
- **Deployment status:** DEPLOYED to production. Netlify project `pcsoahu`, deploy
  `6a72a8a03241549d0129213d`, state `ready`, published 2026-08-05T03:06:18Z (8s, context
  production, alias pcsoahu.com). 48 files + concierge function; secret scan clean (0 matches).
  IndexNow pinged (HTTP 200) for the new page + `/guides/` + `/vehicle-shipping/`.
- **Production verification:** PASS — `/guides/household-goods.html` HTTP 200; key routes (/, /guides/,
  /vehicle-shipping/, /bah-report/, /sitemap.xml, /robots.txt) 200; nonexistent route 404; new URL
  present in live sitemap.xml; canonical = https://pcsoahu.com/guides/household-goods.html.
- **Next recommended related topics:** Backlog #1 (rent-vs-buy with a VA loan), #5 (on-base
  waitlist mechanics), #10 (Honolulu vehicle registration 10-day clock) — see EDITORIAL_CALENDAR.md.

---

## Record template (copy for each run)

```
## YYYY-MM-DD — <topic short name>
- Date/time:
- Selected topic:
- Reason for selection:
- Audience:
- Content type:
- URL:
- Sources used (verified YYYY-MM-DD):
- Facts requiring future revalidation:
- Internal links added:
- CTA used:
- Files changed:
- Build status:            # paste the gate line
- Deployment status:       # deploy id / URL, or NOT DEPLOYED + reason
- Production verification:  # HTTP status + sitemap presence
- Next recommended related topics:
```
