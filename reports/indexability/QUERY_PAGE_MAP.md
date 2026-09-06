# Query-to-Page Map — pcsoahu.com (2026-09-06 sprint)

Source: Search Console queries with impressions (25-day window). One primary page per cluster;
titles/H1s/links updated this sprint to reinforce each mapping. No exact-match stuffing.

| Cluster | Queries (impr.) | PRIMARY page | Supporting | Overlap handling |
|---|---|---|---|---|
| **PCS to Hawaii / Oahu** | PCS to Hawaii (12), PCSing to Hawaii (5), PCS Oahu (3), military PCS services Honolulu (14) | **`/pcs-to-hawaii/` (NEW master hub)** — "PCS to Hawaii: The Complete Oahu Move Guide" | `/pcs-checklist/` (interactive tool, distinct intent), `/guides/` shelf | No competing general PCS guide existed or was created; the checklist keeps its tool framing and is linked FROM the hub. "Military PCS services Honolulu" maps here too — deliberately NOT a vague services page; the hub + referral-disclosed lead form serve that intent honestly. |
| **Oahu / Honolulu / Hawaii BAH** | Oahu BAH (10), Honolulu BAH (9), Hawaii BAH (6), BAH Oahu (4), BAH Honolulu (4) | **`/bah-report/`** — title already leads "2026 Oahu BAH vs Actual Rents" | `/data/` (machine-readable), `/bah-report/2026-edition/` (archive) | One MHA covers the island, so ONE hub — per-station BAH *pages* would duplicate identical rates 7×. Instead: new `#by-base` section explains the one-rate structure and routes to each base guide. Archive H1 differentiated ("— August 2026 archived edition") to end H1 duplication. |
| **Schofield Barracks BAH** | BAH for Schofield Barracks (5) + variants | **`/bases/schofield-wheeler.html`** — title carries "BAH vs Rent"; NEW `#bah` section "Schofield Barracks BAH, in practice" | `/bah-report/` (rates), `/neighborhoods/wahiawa.html`, `/neighborhoods/mililani.html` | Differentiation is real, not templated: only Schofield gets the dedicated BAH section, and its content is Schofield-specific (band data shows Wahiawa 3BR $2,600–3,200 sits inside the $3,663 E-5-dep anchor; Mililani straddles it). Other base pages keep their standard allowance ledger without the duplicated section. |
| **Temporary lodging** | Temporary lodging for PCS Hawaii (3), PCS lodging Oahu (2) | **`/tla/`** — retitled "Temporary Lodging for a Hawaii PCS: How TLA & Interim Housing Work"; H1 now leads with "Temporary lodging" | `/tla/field-notes.html` (where-to-stay notes) | Query language says "temporary lodging"; the page led with the acronym. TLA literally means Temporary Lodging Allowance, so the retitle is a spelling-out, not stuffing. Field-notes stays the lodging-inventory spoke. |
| **Base/duty-station** (latent) | Schofield Barracks BAH today; other bases expected | `/bases/` hub + 7 base pages | `/family/*` per-base family layers | Base pages gained a 2nd/3rd inbound link each (master hub list + BAH hub `#by-base`), fixing the 1-inbound weakness from the 2026-08-24 audit. |

## Homepage role correction
The homepage keeps its brand/"PCS Oahu" strength (position 15.3 on that query) but now routes
instead of absorbing: primary hero CTA → `/pcs-to-hawaii/`, secondary → BAH report/checklist/quiz,
lede links the master guide and `/tla/` with distinct anchors. Nav gained "PCS Guide" as the first
item (12 nav links sitewide, gate-enforced); footer's Arriving list leads with the master guide.
