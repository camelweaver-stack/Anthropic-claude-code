# West FW Living — Authority Concentration Plan

Executed 2026-08-24. Governing principle: **concentrate authority before expanding surface
area.** This pass repositioned the site from a renter-specials identity to a west-Fort-Worth
relocation and housing *decision platform*, removed credibility-damaging placeholder content,
and pointed internal authority at demonstrated GSC winners. Companion docs:
`docs/SEO_GROWTH_SYSTEM.md` (the closed-loop engine), `editorial/DAILY_RUN.md` (publishing
mechanics), `reports/seo/winner-reinforcement-*.md` (the weekly action list).

## 1 · Architecture findings (inspected before editing)

- **Homepage** was renter-specials-first: hero pitched "you're leaving money on the table,"
  specials CTA above the fold, decision tools buried mid-page. Rebalanced (see §3).
- **Navigation** (10-link EN spec) already balanced: Specials · Best Deals · Neighborhoods ·
  Schools · Buying · Selling · Relocate · Guides · Tools · Español. Unchanged — it serves both
  journeys and is gate-enforced.
- **Renter stack** (specials, deals, rentals/, second-chance, rent-to-own, tools) is the most
  built-out and earns most current impressions. Retained fully; no renter URL touched.
- **Buyer/relocation stack** existed (buy/, sell/, relocate/, compare/, move/, schools/,
  neighborhoods/) but was under-linked from the money surfaces and never the site's stated
  identity.
- **/move/** — interactive 6-phase checklist, localStorage progress, good metadata. Weakness
  was inbound: ~2 contextual inbound links. Now linked from the homepage hero + journey grid,
  the Lockheed relocation hub, renter decision-path sections, and the relocate hub.
- **/compare/** — 10 real comparison pages, good hub. Weakness: community/school pages rarely
  linked into their own comparisons. Fixed (§5). Title had a double-escaped `&amp;amp;` — fixed.
- **Lockheed cluster** — strongest GSC signal (285 imp @ pos 10.7). Renter hub + buyer spoke
  existed; no page answered the *broad relocation* question. Hub created (§4).
- **Lead capture** — hardened FormSubmit forms already carry source URL, referrer, UTM set,
  landing page, and a per-page `_subject`; CTA type is recoverable from the `uid`/page context.
  No change needed for attribution.
- **GSC system** — `scripts/seo_engine.py` (ingest/report/linkaudit/log-event) already
  operating; this pass added `reinforce` (§6).

## 2 · Credibility purge (highest priority — done first)

Literal placeholder text simulating first-hand visits was rendering publicly on 13 URLs:

- `[FIRST-HAND FIELD NOTE — added after an in-person visit.]` on all 11 `/complexes/` pages
  (olympus-willow-park, canvas-at-willow-park, gates-at-meadow-place,
  willow-crossing-townhomes, olympus-hudson-oaks, birchway-hudson-oaks, oxford-at-weatherford,
  college-park-weatherford, preserve-at-willow-park, chapel-creek-cottages,
  westpoint-at-scenic-vista)
- `FIELD PHOTO — added after an in-person visit` photo-slot divs on canvas-at-willow-park and
  willow-crossing-townhomes
- `FIELD PHOTOS — added after in-person visits` slots + a "compiled after in-person visits —
  rent sheets in hand" line on `/areas/white-settlement` and `/areas/benbrook`

**Resolution:** all removed — the pages now render nothing where no genuine observation
exists. A sweep for subtler simulated-firsthand phrasing ("we visited/toured/walked…") found
none. The compiled-from-public-listings voice used everywhere else was already honest.

**Content-state model:** `data/fieldnotes.json` — per-property records with
`status: none | planned | verified` plus text/photos/verifiedDate/author/source. All current
records are `none`. Only `verified` content may ever render, and `planned` renders nothing.

**Enforcement:** new `placeholder-assert` gate in `scripts/apply_standing_fixes.py` fails the
build if placeholder field-note/photo phrasing, visit claims, TODO/TK/DRAFT markers, or lorem
ipsum reach any production page. Negative-tested (a seeded violation fails the gate).

## 3 · Homepage repositioning

New proposition: *the decision platform for living on Fort Worth's west side.*
Title/description/WebSite-LD rewritten around relocation + where-to-live. Hero now leads
"Moving to Fort Worth's west side? Start with **where**" with CTAs to `/where-to-live` and
`/move/`. First content section is the decision hub (matcher + compare + a six-card journey
grid: Moving here / Move checklist / Schools / Commute / Rent-or-buy / Working at
Lockheed-NAS JRB). The renter market briefing, stats, three doors, tools, and specials all
remain — explicitly framed as the "renting first?" branch. No renter URL removed or weakened.

## 4 · Lockheed flagship funnel

Cluster architecture after this pass:

```
/relocate/working-at-lockheed-martin-fort-worth   ← NEW flagship hub (broad relocation intent)
├─ rent:  /guides/apartments-near-lockheed-martin-fort-worth (GSC #1) → complexes, /rentals/apartments-76108, short-term
├─ buy:   /guides/buying-a-home-near-lockheed-martin-fort-worth → sell-side bands, homestead, VA
├─ commute: shift-math + /commutes/* per-property files + which-side guide
├─ family:  /schools/tea-ratings-2026, zone decoder, living-in-{benbrook,aledo,walsh}
├─ military: /guides/apartments-near-nas-jrb-fort-worth, /military/bah-fort-worth, /military/jrb-noise
└─ decide:  /calculator, /compare/*, /where-to-live, /move/
```

ES mirror created (`/es/relocate/trabajar-en-lockheed-martin-fort-worth`), bidirectional
hreflang + visible cross-language links. The hub reuses only published, sourced figures.
**Deliberately not created** (cannibalization/permutation): per-suburb "X to Lockheed commute"
pages, a second apartments variant, any thin employer page for other employers without
demonstrated query demand.

## 5 · Internal authority concentration (tier-B reinforcement)

Contextual links added into the position-6–15 winners:
walsh → walsh-vs-parks-of-aledo + walsh-vs-morningstar + data/property-tax ·
living-in-aledo → aledo-vs-weatherford + aledo-vs-willow-park + aledo-isd file ·
olympus-four guide → willow-park-vs-hudson-oaks · rent-or-buy-willow-park →
willow-park-vs-hudson-oaks · aledo-isd hub → living-in-aledo + ISD comparison + rent-the-district ·
weatherford-isd hub → aledo-isd-vs-weatherford-isd. Renter-to-buyer decision paths added on
specials, deals, second-chance, rent-to-own, and apartments-76108 (soft, non-salesy, each
pointing at calculator/compare/move/buy paths). No sitewide exact-match anchors.

## 6 · Winner-reinforcement system

`python3 scripts/seo_engine.py reinforce` → `reports/seo/winner-reinforcement-YYYY-MM-DD.md`.
One recommended action per evidenced page (strengthen links / improve title / deepen / expand
cluster / leave alone), priority-ordered; rising-impression detection once ≥2 snapshots exist.
The default action is **leave alone** (first run: 43 of 57 pages). Run weekly.
Allocation rebalanced to 35% winners / 30% improve-6–20 / 20% new local experiments /
10% maintenance / 5% exploratory (configurable in `data/seo/config.json`).

## 7 · Topical dilution — classification (no deletions)

- **Retain, de-emphasized** (generic national renter/lease-law content at pos 40–100:
  credit-score, breaking-a-lease, subletting, deposit rule, renters-insurance pair,
  can-landlord-raise-rent, income-restricted-weatherford): kept for authority and real user
  utility; linked compactly from the guides-hub "lease law" section; receives no new
  investment. Several have impressions — URLs preserved.
- **Retain** (geographically anchored): relocate/from-* series, rent-to-own + divvy-vs-pathway
  (live GSC queries), weatherford-college.
- **Noindex (clearly justified)**: `tv.html`, `poster.html` — screen/print display artifacts,
  zero impressions, deliberately orphaned. X-Robots-Tag added in netlify.toml; removed from
  sitemap. Nothing else noindexed; nothing redirected; nothing deleted.
- **Intentional orphans kept**: thanks/gracias (form landings), newsletter, for-leasing-teams
  (B2B artifact), field-guide/relocate-guide alt versions — operator may wire or retire.

## 8 · Standing rules this plan adds

1. No firsthand claim without a `verified` fieldnotes record — gate-enforced.
2. Optimization of existing assets outranks net-new publishing (allocation above).
3. New employer pages only on demonstrated query demand with a real housing decision.
4. De-emphasis before deletion; URL changes on impression-earning pages require explicit
   justification in the audit log.
