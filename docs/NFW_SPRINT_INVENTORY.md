# North FW Living — Repositioning Sprint: Audit & Inventory

Date: 2026-09-06 · Branch: `claude/northfwliving-quality-seasoning-jqyoe9`
Full machine inventory (272 pages, all fields): `docs/NFW_SPRINT_INVENTORY.csv`.

## Strategic frame

This sprint is driven by the new GSC evidence (306 impressions / 2 clicks / ~23 active
days) — the "new Search Console evidence" the seasoning plan named as the trigger for the
next intervention. Governing constraint carried over from that plan: **the ranking cohort
(Northwest ISD 27.4, schools hub 28.6, boundary guide 23.4, Northlake 49.9, Spanish MUD/PID
10.8, Alliance 9.5) is strengthened and better-linked — additively — not rewritten in ways
that reset the experiment.** URLs, working titles, working H1s, and search intent preserved.

Portfolio role for this site: **deep North Fort Worth / Alliance–Northwest ISD corridor
authority** — distinct from Where in DFW (regional discovery) and West FW Living (west-side
operation). Editorial test applied throughout: would this page also fit a generic Texas
real-estate encyclopedia? If yes, it is localized or de-emphasized.

## Build / deploy / architecture (verified)

- **Framework:** fully static hand-authored HTML, no build step — files deploy verbatim.
  Publish directory `northfwliving/`. No in-repo generator or content manifest (the
  generator lives off-repo; this mirror is the source of truth under version control).
- **Deploy:** Netlify project `northfwliving` (site `d106e26e-05b2-4ef0-82f9-cd8a644a6590`),
  primary domain northfwliving.com. Manual/CLI deploy of the publish dir.
- **Pages:** 272 — 136 EN + 136 ES (1:1 mirror; only slug divergence `/privacy/` ↔
  `/es/privacidad/`).
- **Shared skeleton (every page):** `header.site` (brand + single `nav.main`), hero,
  `main`, one `formbox` lead form, `footer.site` (4 link columns + legal), first-touch
  attribution script. Two JSON-LD blocks minimum (BreadcrumbList + Organization); hubs add
  WebSite; FAQ/guide pages add FAQPage/Article.
- **Routing:** directory URLs, trailing slash → `index.html`. Self-referential canonicals
  everywhere; hreflang cluster en/es/x-default on all 272 pages (validated).
- **Forms/attribution:** hashed FormSubmit endpoint (`c86195fac9…` — receiving email NOT
  exposed), honeypot, consent checkbox + timestamp, UTM/referrer/landing_page/page_url
  hidden fields populated by first-touch sessionStorage capture. Compliant.

## Pre-sprint validator baseline (all green)

credibility 272 clean · technical 272 clean (canonicals/hreflang/titles/links/sitemap) ·
ledger OK (0 records, none fabricated) · 25/25 unit tests.

## Key findings → actions

| # | Finding | Evidence | Action |
|---|---------|----------|--------|
| F1 | **Northwest ISD page is thin** — the site's #1 query ("moving to northwest isd", 34 imp, pos 27.4) lands on a 3-paragraph page with no cross-links, no official-district-tool link, no intent CTA. | `schools/northwest-isd/` | Phase 3: expand into the authority hub (communities served, verification, feeder/boundary, new-construction, housing, commute, official link, cross-links, relocation CTA). Keep URL/title/H1. |
| F2 | **No central Alliance corridor hub.** Alliance content is scattered across `neighborhoods/alliance/` (ranks 9.5), `employers/alliance-logistics/`, `buy/alliance/`, `renting/alliance/`, `sell/alliance/`. Nothing ties employment access + where-to-live + schools + BTR together. | inventory | Phase 4: create `/alliance/` (+ `/es/alliance/`) as the orientation hub linking OUT to the pocket page (no cannibalization — distinct intent). |
| F3 | **Every CTA is identical** ("Get the Ledger before the incentives change") on 98 pages incl. school, boundary, relocation, tax pages where it mismatches intent. | grep: 98 identical headlines | Phase 13: intent-matched CTA variants (schools→relocation help; area→local-agent/home guidance; alliance/employer→commute relocation; tax/MUD-PID→buyer consult; BTR→rental help). Form mechanics unchanged. |
| F4 | **MUD/PID is a statewide-flavored distraction** — 101 imp / 0 clicks / pos 71.6, broad "what is a pid" queries. Spanish version ranks 10.8 (protect). | GSC | Phase 6: localize to NFW buying decisions + add a *verified-only* local framework (no fabricated DB); buyer-consult CTA. ES page: audit, do not disturb. |
| F5 | **Homepage leads with incentives, not the corridor/schools identity** GSC rewards. "Three doors" = Ledger / employers / rent-vs-own. | `index.html` | Phase 2: reframe around Alliance–Northwest ISD corridor + prominent hub links (moving, NWISD, boundaries, Alliance, Northlake/Haslet/Justin/Keller, MUD/PID, BTR, comparisons, relocation). |
| F6 | **No district-vs-district comparison** though "Northwest ISD vs Keller ISD" is a real corridor decision with search intent. Existing compares are pocket-vs-pocket only. | `compare/` | Phase 9: add `/compare/northwest-isd-vs-keller-isd/` (+ES), framework-based, no rankings. |
| F7 | Priority pages rely on nav/footer for discovery; **few contextual incoming links** into the school/corridor cluster. | link graph | Phase 10: wire hub hierarchy with natural contextual anchors. |

## Non-issues (verified healthy — left alone)

- No duplicate titles across 272 pages. No `.html`-vs-extensionless duplicate groups.
- No orphans in the strict sense (nav + footer reach every page); no noindex; robots permits crawl.
- Canonicals self-referential; hreflang reciprocal en/es/x-default sitewide.
- Existing area pages (Northlake, Haslet, Justin, Keller, Roanoke, Alliance), school pages,
  boundary guide, NWISD-life, and BTR are already corridor-specific, dated, sourced, and
  free of rankings/guarantees — they get **targeted additions** (cross-links, CTA, date),
  not rewrites.
- Builder Ledger: type-level table + append-only snapshot architecture, 0 fabricated
  records — untouched.

## Overlap / cannibalization guard

- New `/alliance/` hub targets *corridor orientation + employment access*; `neighborhoods/alliance/`
  keeps *living-in-the-pocket* intent (it ranks 9.5). Distinct anchors, bidirectional links.
- No page duplicates Where in DFW's regional-discovery role; this site stays inside the
  Alliance–NWISD–Northlake–Haslet–Justin–Keller corridor.

## Scope this pass (per task scope-control order)

1. Northwest ISD hub (F1) · 2. Alliance corridor hub (F2) · 3. School/boundary CTA+links ·
4. Local area pages: cross-links + intent CTA + verification date · 5. MUD/PID localize (F4) ·
6. BTR localize · 7. Internal links + intent CTAs (F3) · 8. NWISD-vs-Keller-ISD comparison (F6) ·
9. Spanish parity for new/priority pages · 10. Validate + deploy + verify.
Remainder → prioritized publication queue in the completion report.
