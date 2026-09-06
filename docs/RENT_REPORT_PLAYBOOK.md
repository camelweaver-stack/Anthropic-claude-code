# Rent Report Playbook — monthly edition template and anti-thinness rules

How to produce `/rent-report/<month>-<year>` each month so the series compounds
authority instead of accumulating near-duplicates. The hub is `/rent-report/`;
every edition is a permanent, dated archive page.

## Fixed structure (mirror the newest edition's HTML)

1. `<title>`: `West Fort Worth Rent Report — <Month> <Year> | West FW Living`
2. Dataset JSON-LD: update name, description, `url` (canonical, extensionless),
   `temporalCoverage` (`YYYY-MM`).
3. Eyebrow: `The West Fort Worth Rent Report · No. <n>` — increment the number.
4. Companion-reads line: rent-vs-buy, latest builder report, prior edition link.
5. Verified line: `✓ Edition No. <n> — all N tracked communities re-verified
   from public listings and property websites, <exact date>`.
6. "The number that defines this month" — the single headline movement.
7. Full tracked-communities table with a `vs. <prior month>` column.
8. Concession Index section: core-4 reading + expanded reading, both vs. prior.
9. A chart SVG named per-edition (`assets/chart-concession-index-<mon>-<yyyy>.svg`).
10. Second signal section (whatever the data actually shows — see rule 2).
11. Three readings (renters / would-be buyers / landlords).
12. Sources & methodology + About + prior-edition link + next-edition promise.

## Data source of truth

`assets/wfl-data.js` is rolled FIRST (verification sweep → weeksFree/beds/
histories/index), then the report is authored from it. Never let the report and
the data engine disagree.

## Anti-thinness rules (what makes each edition a distinct page)

1. **New verification, not carried forward.** Every figure re-verified in the
   edition's own sweep; unverifiable floor plans omitted, never repeated.
2. **A thesis, not a refresh.** Each edition leads with what CHANGED —
   September's was the index collapse and westward migration. If a month is
   genuinely flat, "the market held" IS the thesis; say so with the evidence.
3. **No recycled prose.** Structure repeats; sentences don't. The three-readings
   section must respond to this month's numbers.
4. **Compare backward.** Every table carries the vs.-prior column; the Index
   section cites the full history. This is what a thin page can't do.

## Month-roll checklist (links that must move with each edition)

- `gen/common.py` + `scripts/fix-nav.py`: footer "Latest Rent Report" href.
- Sitewide footer instances in hand-authored pages (tree-wide replace).
- `rent-report/index.html`: new current card; demote prior edition to archive
  wording.
- Prior edition page: add "Newer edition available" pointer under its byline.
- Hub cards: `guides/index.html`, `es/guias/index.html`, homepage field-notes
  card, homepage stats block, `data/index.html` if worded month-specifically.
- Sweep stale month-specific claims sitewide (grep the old headline numbers).
- Specials pages EN + ES, complex pages, comparison/rentals tables — full
  month-roll scope is recorded in the 2026-09-03 AUDIT_LOG entry.

## After publishing

Build + `apply_standing_fixes.py` (ten gates) + `scripts/audit_urls.py`;
deploy; live-verify; IndexNow the changed URLs; AUDIT_LOG + calendar rows.
