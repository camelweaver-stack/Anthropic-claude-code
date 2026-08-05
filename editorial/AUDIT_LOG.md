# PCS Oahu — Daily Audit Log

Append-only. Newest entry on top. One record per daily run. Template at the bottom.

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
- **Deployment status:** NOT DEPLOYED — staged on branch `claude/pcs-oahu-daily-publishing-1289q3`
  for human go-live review (first-run staging validation per the brief's activation sequence).
- **Production verification:** Pending go-live decision.
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
