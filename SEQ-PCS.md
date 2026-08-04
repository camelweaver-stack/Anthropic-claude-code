# SEQ-PCS — PCS Oahu Nurture Tracks (CRM build sheet)
Three tracks for the Sheets + Gmail + Apps Script CRM, keyed to pcsoahu.com form tags.
Voice: same as the site — respectful, factual, zero kitsch. Every email earns its send with
one useful thing; every email exits cleanly.

## Wiring (Apps Script side)
- **Intake:** FormSubmit → leads@anastasiaweaver.com. Parse `_subject` (PCSOAHU-*), `audience`
  (referral-hi-oahu-pcs), `segment` (pcs-renter | pcs-buyer | pcs-seller), `move_date` /
  `sell_timeline` free text. New row in the lead tracker; Track column = SEQ-PCS-R / -B / -S
  by segment.
- **Pacing anchor:** attempt to parse a month/year from the context field ("report NLT June
  2027" → 2027-06). If parsed: schedule sends backward from report month per each track's
  offsets. If blank/unparseable: default cadence (Day 0, 3, 10, 21, 42, 70).
- **Data merge:** each send pulls the CURRENT constants (BAH anchors, refresh date) from a
  "Data" sheet mirroring gen/common.py — update it on every site refresh so emails never quote
  stale numbers.
- **Heat scoring:** open/click bumps per existing WFL model; reply → Track=MANUAL + task row;
  keyword **AGENT** anywhere in a reply → Referral handoff row (see compliance note).
- **Exit rules:** unsubscribe honored globally; sequence completes → monthly BAH-report edition
  list only. Post-arrival (report month passed): auto-move renters to a 60-day "settled
  check-in" single send, buyers/sellers to MANUAL review.
- **Compliance note (review before activation):** site publisher-mode rules govern pcsoahu.com;
  these emails may go one step further — connecting a lead who explicitly requests it to a
  licensed agent through Anastasia's Hawaii brokerage referral pipeline (her HI license is
  active). Keep all service language OUT of the emails themselves except the single AGENT
  reply mechanism, and have the brokerage confirm the referral-handoff wording before launch.
  No lender content anywhere, ever.

---

## TRACK R — SEQ-PCS-R (pcs-renter) · 6 sends
**R1 · Day 0 — "Your Oahu arrival brief (the short version)"**
You joined from pcsoahu.com — here's the working brief. One fact reorganizes your whole
search: every Oahu base pays the same BAH (Honolulu County). What differs is rent on the other
side of each gate. Current anchors: E-5 w/dep {BAH_E5_DEP}; island range {BAH_RANGE} (DTMO,
effective {BAH_EFFECTIVE}). Your two links today: your base guide [link by inferred base tag,
else /bases/] and the pocket-match quiz. Reply with your report month and we'll pace the rest
of these to your actual timeline.

**R2 · report−150d (or Day 3) — "The two clocks that start before you fly"**
Pets and the on-base waitlist. Hawaii's quarantine sequence is measured in months — if an
animal is coming, the checklist starts this week (guide: /guides/pets-to-hawaii.html). And the
on-base waitlist costs nothing to join and holds while you shop off-base — call the housing
office the day orders publish. Neither can be fixed late. Both are free now.

**R3 · report−120d (or Day 10) — "Ship the car? The three-number test"**
One POV ships free on your orders; the second is a retail decision. Second-vehicle West Coast
≈ $1,000–1,600, gap rentals ≈ $600–900+/wk, and Oahu's used market runs a premium. The full
end-to-end (PCSmyPOV, the quarter-tank rule, the 10-day registration clock):
/vehicle-shipping/. Decide before the mover calendar decides for you.

**R4 · report−75d (or Day 21) — "Shortlist three pockets, not one"**
PCS-season inventory moves in days, so the winning method is a pre-built shortlist: three
pockets that survive the 0630 drive test to your gate, ranked by band vs. your grade's number.
The pocket table [/neighborhoods/] has current bands (refreshed {LAST_REFRESHED}); every pocket
page lists its honest trade. Staging documents now — orders, LES, references, pet records —
is what lets you apply same-day later.

**R5 · report−30d (or Day 42) — "Wheels-down week, hour by hour"**
TLA does the bridging if you run it right: book base lodging first, keep every receipt, and
know the search-evidence requirement. Lodging field notes (incl. the Hale Koa option):
/tla/field-notes.html. Checklist for the whole week: /pcs-checklist/. Tour at your real
commute hours; apply fast when a unit fits the band.

**R6 · report+45d — "Settled? One favor and one offer"**
The favor: reply with the one thing you wish you'd known — it goes into the next refresh and
the next family's brief. The offer: we keep watching the bands so you don't have to; you'll
get the BAH Reality Report each edition. If your situation turns into a buying question this
tour, the VA brief is here: /buy/. (Full service is coming; you'll hear it here first.)

---

## TRACK B — SEQ-PCS-B (pcs-buyer) · 5 sends
**B1 · Day 0 — "Buying on Oahu: the three gates"**
Entitlement, condo approval, leasehold — in that order. Full vs. partial entitlement changes
zero-down math at Oahu prices (medians: SF {MED_SF}, condo {MED_CONDO}, June 2026); VA condo
financing lives and dies by the approved-project list; and "leasehold" is the word that makes
a bargain not one. The flagship brief: /buy/. Reply with your report month to pace the rest.

**B2 · report−120d (or Day 5) — "COE and a real preapproval, early"**
Two documents make an Oahu VA offer credible: your Certificate of Eligibility and a
preapproval underwritten on gaining-station BAH. Both take longer than sellers wait. Your
lender is your choice (we don't place or recommend lenders — policy); what we can give you is
the question list: entitlement status, condo-project experience, HOA-fee treatment in DTI.

**B3 · report−90d (or Day 14) — "Where VA buying actually happens"**
The center of gravity is leeward new construction (Ewa/Kapolei) and the close-in condo pockets
— for opposite reasons. Pocket pages carry buyer notes where they matter: [/neighborhoods/].
The quiz ranks your fit in ninety seconds: /quiz/. HOA fees are payment, not fine print —
price them first.

**B4 · report−45d (or Day 30) — "The exit is part of the purchase"**
Orders don't wait for market timing, so buy with the departure math open: HARPTA facts,
rent-vs-sell from five time zones, entitlement restoration. The PCS-out brief: /sell/. A house
that only works if you never leave doesn't work on orders.

**B5 · report+30d — "Boots down. Current numbers, current list"**
You're on island; the numbers moved while you flew. Current medians and bands are in the
latest report edition [/bah-report/], refreshed {LAST_REFRESHED}. From here we send edition
updates only — unless you reply, in which case a human reads it. (AGENT mechanism per
compliance note.)

---

## TRACK S — SEQ-PCS-S (pcs-seller) · 5 sends
**S1 · Day 0 — "Sell or rent: the five-line napkin"**
Market rent, PITI+HOA+GET, remote management (≈8–12%), an honest vacancy reserve, and the
equity a sale frees. Run it before sentiment votes: /sell/ has the framework and the tools
page automates it (/tools/). Reply with your departure window and we'll pace the rest.

**S2 · departure−120d (or Day 5) — "HARPTA is a residency question"**
7.25% withholding on non-resident sellers — and SCRA members who kept mainland residency are
typically non-residents even after years on island. Withholding ≠ tax; timing and status are
real-money questions for a tax professional. The facts, straight: /sell/#harpta.

**S3 · departure−90d (or Day 14) — "The VA seller's two levers"**
Entitlement restoration (file it — not automatic) and assumability (your rate may be worth
real money to a VA buyer, with an entitlement catch). Both belong in your listing strategy
conversation, whoever conducts it. Brief: /sell/.

**S4 · departure−60d (or Day 28) — "If you keep it: landlording from five time zones"**
GET registration, management selection, reserves, and a lease calendar that respects the next
PCS cycle's tenant pool. The rent side of the ledger is the same pocket table buyers use —
your pocket's current band: [/neighborhoods/].

**S5 · departure−21d — "Decision week"**
Whichever way the napkin came out, the checklist tail matters: shipping the car back
(/vehicle-shipping/ covers the reverse run), records, and the settled-family favor — reply
with what you'd tell the next seller. Edition updates continue; a reply always reaches a
human. (AGENT mechanism per compliance note.)
