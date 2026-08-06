# PCS Oahu — Daily Audit Log

Append-only. Newest entry on top. One record per daily run. Template at the bottom.

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
