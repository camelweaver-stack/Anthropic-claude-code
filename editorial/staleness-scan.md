# PCS Oahu — Staleness / Maintenance Scan

Run every daily cycle before selecting a topic. If a scan surfaces something higher-value than a
new page, fix it instead — updating an important page beats a weak new one. Commands assume repo
root.

## 1. Data freshness (the figures that go stale first)
- Current anchors live in `gen/common.py`: `LAST_REFRESHED`, `BUILD_DATE`, `BAH`, `POCKETS`,
  `MED_SF`, `MED_CONDO`. Compare against the cadence in `REFRESH_RUNBOOK.md`.
- Rent bands: refresh 1st of month Mar–Aug, else quarterly. Medians: quarterly. BAH: DTMO cycle.
- `grep -n "LAST_REFRESHED\|BUILD_DATE\|BAH_YEAR" gen/common.py`

## 2. Date/edition drift in copy
- `grep -rniE "2024|2025" site --include=*.html` → any lingering old year in visible copy is a flag
  (some archived-edition references are intentional — check context, not just the match).
- Confirm the BAH report edition label and the archived edition still align with `common.py`.

## 3. Expired / time-bound content
- The site is currently evergreen (no live event pages). When event or "specials"-style pages are
  added, each must carry an explicit event date + "last verified" date; auto-archive once the date
  passes. Scan: `grep -rniE "last verified|event date|registration (deadline|closes)" site`.

## 4. Broken / orphan / duplicate structure
- Orphans: every `site/**.html` should be reachable from nav, a hub, or the footer. Spot-check new
  pages are linked from ≥1 hub.
- Internal-link sanity (targets exist):
  `for f in $(grep -rhoE 'href="/[a-z0-9/-]+\.html"' site --include=*.html | sed -E 's/href="//;s/"//' | sort -u); do [ -f "site$f" ] || echo "MISSING: $f"; done`
- Duplicate/near-duplicate city/base/neighborhood pages: check titles for cannibalization
  `grep -rhoE "<title>[^<]+" site --include=*.html | sort | uniq -d`

## 5. Sitemap parity + gate
- The gate (`gen/gate.py`) already enforces sitemap↔file parity, canonical/OG/meta, EHO +
  publisher disclaimer, forbidden language, and form correctness. Treat a red gate as a blocker.
- `cd gen && python3 build.py && python3 gate.py`

## 6. Sourcing weakness
- Any page making a real-estate / tax / benefit / policy claim should name its source inline and
  carry a visible verified date. Scan new/edited pages for an unsourced number and fix before ship.
