# PCS Oahu — Daily Publishing Runbook

The operating procedure for the autonomous daily content engine. One substantial, useful,
factual item per day, published to pcsoahu.com through Netlify. Utility over volume: if no
sufficiently useful new topic exists, materially update an existing page instead.

This runbook is the executable version of the mandate in the task brief. It assumes the site
architecture documented in `README.md` (generator in `gen/`, gate in `gen/gate.py`, output in
`site/`, Netlify publishes `site/`).

## Non-negotiables (inherited from the site's publisher posture)
- **Never hand-edit `site/`.** Content lives in `gen/pages_*.py`; rebuild + re-gate.
- **Single-source data** in `gen/common.py`. Never quote a BAH/rent/median figure that isn't
  the current constant, and never print a figure the gate can't tie to a visible refresh date.
- **Publisher mode.** No brokerage/service language (the gate's `FORBIDDEN` list enforces it);
  no "crime rate"/"safest neighborhood" claims; EHO + the not-a-brokerage disclaimer on every page.
- **Never invent** prices, dates, hours, phone numbers, addresses, policies, quotes, or reviews.
  If a fact can't be confirmed from a source in the hierarchy below, omit it or label it
  explicitly (`preliminary` / `proposed` / `reported` / `unconfirmed`).

## The daily loop
1. **Review the library** — `find site -name '*.html'` and skim `editorial/EDITORIAL_CALENDAR.md`.
2. **Review the backlog + calendar** — pick from the scored backlog; keep cluster balance
   (don't ship two near-identical pages in a row).
3. **Scan for staleness** — run `editorial/staleness-scan.md` checks: obsolete dates, expired
   events, stale figures vs `gen/common.py` refresh dates, orphan/duplicate pages, weak links.
4. **Research** — authoritative sources first (hierarchy below). Capture the source URL + the
   date you verified it for the audit record.
5. **Select** — highest combined utility + relevance by the scoring model below. Updating a
   high-value page beats a weak new page.
6. **Produce** — author in `gen/pages_*.py` following the existing idiom (`page(...)`,
   `lead_form(...)`, `faq_ld(...)`). Include: direct answer up top, Oahu + military context,
   who it applies to, next steps, sources, a visible verified date, internal links (hub-and-spoke),
   a page-matched CTA, and structured metadata (Article/FAQ JSON-LD).
7. **Validate facts and dates** — re-read every number and date against its source.
8. **Wire it in** — add to the module `build()`, link from the relevant hub + ≥1 existing page
   (reciprocal), add to nav only if it's a top-level cluster (nav is fixed at 10 — usually no).
9. **Build + gate** — `cd gen && python3 build.py && python3 gate.py` → must print `GATE PASSED`.
   The gate is the merge gate: no green, no ship.
10. **Deploy** — see `CLAUDE_CODE_DEPLOY.md`. Deploy `site/` via the Netlify connector, then
    POST the changed URLs via IndexNow.
11. **Verify live** — fetch the production URL, confirm HTTP 200, confirm it appears in
    `https://pcsoahu.com/sitemap.xml`.
12. **Audit** — append a record to `editorial/AUDIT_LOG.md` (template at the bottom of that file).

## Topic scoring model
Score each candidate 1–5 on: search demand, military relevance, transaction relevance,
freshness/urgency, usefulness, geographic specificity, content-gap size, competitive weakness,
internal-linking value, lead-gen potential, backlink likelihood, source availability.
Prioritize high combined utility **and** commercial relevance — but never let commercial
relevance override factual usefulness. A topic with no reliable source does not ship.

## Source hierarchy (highest first)
1. Official military/government (DoD, DTMO, service HQ, Military OneSource, Move.mil/DPS)
2. State/county agencies (Hawaii DOE, HDOA, Honolulu.gov, DBEDT)
3. School districts
4. Official event organizers / first-party
5. Direct service-provider sites
6. MLS-derived / brokerage-authorized data (Honolulu Board of REALTORS®)
7. Reputable local media
8. Other secondary sources

## Cluster rotation (hub-and-spoke)
Bases · Neighborhoods · Buying · Renting · Selling · Leaving Hawaii · Schools & childcare ·
Family life · PCS logistics · VA financing · Military benefits · Local services.
Every item must strengthen ≥1 cluster and link to its hub.

## Do NOT autonomously publish — draft + flag for review instead
Political advocacy; legal/financial advice presented as individualized; allegations against
identifiable people/businesses; unverified safety/crime claims; crisis/casualty/crime reporting;
defamation; anything touching an active legal dispute; changes to brokerage/licensing/referral
disclosures, privacy policy, terms, or consent; paid/sponsored content; material redesigns;
destructive code changes; deletion of major pages; domain/DNS/billing/account changes.
For these: write the draft, add an entry to `editorial/AUDIT_LOG.md` marked `NEEDS REVIEW`, do
not deploy.

## Deploy-failure protocol
Preserve the prior production version. Do not repeatedly force deploys. Diagnose, record the
error in the audit log, leave a clean recovery path (the last green `site/` is committed), make
no destructive changes.
