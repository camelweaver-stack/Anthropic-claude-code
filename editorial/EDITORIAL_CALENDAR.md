# PCS Oahu — Rolling 90-Day Editorial Calendar

Window: **2026-08-05 → 2026-11-03**. One substantial item/day; utility gates every slot. Update
this file each run: mark shipped items, re-score the backlog, keep cluster balance. Tracked
fields per row: Topic · Cluster · Audience · Target query · Pub date · Update date · Source
status · Traffic potential · Transaction relevance · Status · Internal-link targets.

Legend — Status: `LIVE` shipped · `NEXT` queued · `IDEA` backlog · `HOLD` needs review/source ·
`UPDATE` maintenance pass. Potential/Transaction: H/M/L.

> **⛔ ENGINE BLOCKER (opened 2026-08-16, still open as of 2026-08-23) — read before running a
> daily cycle.** Deploying `site/` from `claude/pcs-oahu-daily-publishing-1289q3` is currently
> **destructive**. Production (Netlify `pcsoahu`) is served from `claude/pcs-oahu-deploy-dd373n` and
> is a strict superset of this branch: 59 live sitemap URLs vs. 51 here, with 11 pages that exist
> only in production (`/family/` ×9, `/tools/commute-grid/`, `/bah-report/2026-rates/`) and a
> different canonical convention. A deploy from this branch would delete those 11 pages. **Build and
> gate as normal here; if the highest-utility item is already authored on this branch, port it onto
> `dd373n` directly (surgical addition, verify additive-only) rather than deploying this branch
> wholesale** — this is now a three-cycle-proven pattern (see the 2026-08-21 through 2026-08-23 entries).
> Full diagnosis and the three permanent-resolution options are in `editorial/AUDIT_LOG.md`, entry
> 2026-08-16.

## Shipped / scheduled

| Date | Topic | Cluster | Audience | Target query | Src | Traffic | Txn | Status | Links |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-05 | Household goods to Hawaii (OCONUS HHG: UB, sea shipment, NTS, pro-gear, DPS) | PCS logistics | Inbound PCS families | "shipping household goods to hawaii military" | Verified (MilOneSource, Move.mil/DPS, DTMO) | H | M | LIVE `/guides/household-goods.html` | guides hub, vehicle-shipping, pets, pcs-checklist, school-transition |
| 2026-08-05 | Registering a car in Hawaii (30-day clock, CS-L(MVR)50 exemption, out-of-state permit) | PCS logistics | Inbound PCS families w/ POV | "register car hawaii military" | Verified (Honolulu CSD, HI DOT, HRS 286) | M | L | LIVE `/guides/vehicle-registration.html` | guides hub, vehicle-shipping, pcs-checklist, on-base |
| 2026-08-06 | Rent vs. buy on Oahu with a VA loan (BAH purchasing power, PCS break-even, forced-exit risk) | Buying / VA | Inbound buyers weighing rent vs. buy | "should i buy a house in hawaii military" | Verified (VA.gov, Military OneSource, DTMO 2026, HBR June 2026) | H | H | LIVE `/guides/rent-vs-buy.html` | buy hub (reciprocal), sell, bah-report, on-base, guides hub, footer |
| 2026-08-16 | HARPTA for outbound military sellers (7.25% of amount realized, N-289 exemptions, N-288B 10-working-day clock, §121 military suspension) | Selling / Leaving | Outbound owners on PCS orders | "harpta military selling hawaii" | Verified (HI DOTAX Tax Facts 2010-1 rev. 4/2025, Form N-288B instr. rev. 2025, TIR 97-1, IRS Pub 523) | M | H | LIVE `/guides/harpta.html` — shipped 2026-08-21 (ported directly onto dd373n, see AUDIT_LOG 2026-08-21) | sell hub (reciprocal), guides hub, footer |
| 2026-08-22 | Does Hawaii have DoDEA schools? (statewide-district reality, no DOD/DoDEA schools, School Liaison Officer contacts by branch) | Schools / Family | Inbound families w/ kids | "hawaii school district military family" | Verified (HIDOE Military Families page, DoDEA Schools Worldwide) | H | M | LIVE `/guides/dodea-schools.html` — shipped same-day (ported directly onto dd373n, see AUDIT_LOG 2026-08-22) | schools hub (reciprocal), school-transition (reciprocal), guides hub |
| 2026-08-23 | On-base waitlist mechanics (HEAT's real role, IPC 7-day backdating rule, decline consequences, EFMP priority) | Renting / On-base | All inbound accompanied families | "oahu military housing waitlist" | Verified (CNIC HEAT page, MilitaryINSTALLATIONS JBPHH, IPC posted guidelines [2016, flagged]) | H | M | LIVE `/guides/on-base-waitlist.html` — shipped same-day (ported onto dd373n, see AUDIT_LOG 2026-08-23) | on-base hub (reciprocal), guides hub |

## Backlog — scored, cluster-balanced (draw the daily slot from here, highest utility first)

| # | Topic | Cluster | Audience | Target query | Src status | Traffic | Txn | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Rent-vs-buy on Oahu with a VA loan (BAH purchasing power, the leasehold trap) | Buying / VA | Inbound buyers E-6+/officer | "should i buy a house in hawaii military" | SHIPPED 2026-08-06 → /guides/rent-vs-buy.html | H | H | LIVE |
| 2 | HARPTA & the outbound seller's proceeds napkin | Selling / Leaving | Outbound owners | "harpta military selling hawaii" | SHIPPED 2026-08-21 → /guides/harpta.html | M | H | LIVE |
| 3 | Fee simple vs leasehold on Oahu — why it matters more here | Buying | Inbound buyers | "leasehold vs fee simple hawaii condo" | Sourceable (public) | M | H | IDEA |
| 4 | DoDEA vs Hawaii DOE — the statewide-district reality for PCS kids | Schools | Families w/ kids | "hawaii school district military family" | SHIPPED 2026-08-22 → /guides/dodea-schools.html | H | M | LIVE |
| 5 | On-base housing waitlist mechanics by installation (join day-one, costs nothing) | Renting / On-base | All inbound | "oahu military housing waitlist" | SHIPPED 2026-08-23 → /guides/on-base-waitlist.html | H | M | LIVE |
| 6 | The Oahu commute-first neighborhood decision (0630 drive test by gate) | Neighborhoods | All inbound | "best neighborhoods oahu military" | Have (POCKETS) | H | M | IDEA |
| 7 | Spouse licensure & the MSAAA/compact map for Hawaii | Family / Benefits | Spouses | "military spouse license hawaii" | Sourceable (DoD SECO) | M | L | IDEA |
| 8 | TLA math + the wheels-down-to-keys sequence (deepen existing /tla/) | PCS logistics | All inbound | "tla hawaii how long" | Have | M | M | UPDATE |
| 9 | VA loan condo approval on Oahu — why the list matters here | Buying / VA | Single/junior buyers | "va approved condo oahu" | Sourceable (VA) | M | H | IDEA |
| 10 | Registering your car in Honolulu — safety check, weight tax | PCS logistics | All w/ POV | "register car hawaii military" | SHIPPED 2026-08-05 → /guides/vehicle-registration.html | M | L | LIVE |
| 11 | Childcare on Oahu: MilitaryChildCare.com + realistic waitlists (deepen) | Family | Families w/ kids | "oahu military childcare waitlist" | Have | M | L | UPDATE |
| 12 | The December BAH-cycle report refresh + PITCH_KIT outreach wave | BAH / Data | Press + all | "2027 bah oahu vs rent" | Scheduled (Dec, DTMO) | H | M | HOLD (Dec) |

## Recurring / data reports (calendar anchors)
- **BAH Reality Report** — refresh with DTMO cycle (mid-December); archive outgoing edition. See
  `REFRESH_RUNBOOK.md`. Next hard trigger: 2027 rates drop.
- **Rent-band refresh** — 1st of month, March–August (PCS season); quarterly off-season. Edit
  `POCKETS` + `LAST_REFRESHED` in `common.py`. Next: 2026-09-01.
- **Market medians** (`MED_SF`, `MED_CONDO`) — quarterly from Honolulu Board of REALTORS®.

## Balance check (keep the mix honest across any ~2-week span)
Evergreen guidance · timely updates · neighborhood · base · family/youth · real estate ·
outbound PCS · service directories · recurring data. Do not ship two near-duplicate pages in a row.
