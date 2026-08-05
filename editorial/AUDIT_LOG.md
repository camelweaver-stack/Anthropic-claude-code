# PCS Oahu — Daily Audit Log

Append-only. Newest entry on top. One record per daily run. Template at the bottom.

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
