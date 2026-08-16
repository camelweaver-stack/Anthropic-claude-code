# West FW Living — Staleness / Maintenance Scan

Run every daily cycle **before** selecting a topic. If a scan surfaces something
higher-value than a new page, fix it instead — updating an important page beats a weak new
one. All commands assume the repo root.

## 0. The gate is the fast scan
Most structural rot is caught mechanically. Run this first; it finds nav drift, missing
canonicals, form-context mismatches, broken internal links, hreflang breaks and sitemap
skew in one pass:

```
python3 scripts/apply_standing_fixes.py --check
```

`--check` reports without writing. Drop the flag to apply the fixes.

## 1. Date / edition drift in copy
The site carries year-stamped pages (rent reports, builder reports, specials, tax rates), so
a lingering old year in visible copy is a flag — but some references are intentionally
historical. Check context, not just the match:

```
grep -rlE "2024|2025" --include=*.html . | grep -v '^\./\.git'
```

Known intentional: `guides/divvy-homes-review-2026.html` (compares prior-year terms),
`military/bah-fort-worth.html` (states the 2026-vs-2025 delta), relocation pages citing
prior-year state data.

**Open item (2026-08-16):** `data/property-tax.html` presents "2024–2025 published figures."
Texas taxing units adopt rates around September, so the current published cycle is one step
newer than that label. Re-verify each city / ISD / county rate against the Tarrant and Parker
appraisal districts and the taxing units themselves before relabeling — **do not** bump the
year on the label without re-verifying every rate underneath it.

## 2. Time-bound content
Specials, rent reports and builder reports expire. Each should carry a visible verified date
and get archived or refreshed once its window passes.

```
grep -rlE "specials|august-2026|rent-report|builder-report" --include=*.html . | head -20
grep -rniE "last verified|verified [0-9]{4}" --include=*.html . | wc -l
```

Cadence: monthly specials on the 1st · rent report monthly · builder report monthly ·
BAH on the DTMO cycle (mid-December) · TEA accountability ratings mid-August ·
property tax rates after adoption (~September–October).

## 3. Verified-date coverage
Any page making a price, rent, tax, benefit, rating or policy claim should name its source
inline and carry a visible verified date. Coverage was 50/298 at bootstrap — improving it is
legitimate daily work when no new topic clears the bar.

```
grep -rliE "last verified|verified [0-9]|last updated" --include=*.html . | wc -l
```

## 4. Orphans and cannibalization
Every page should be reachable from nav, a hub, or the footer. New spokes must be wired into
`RECIPROCAL` in `gen/build.py` so the hub link is created and kept.

```
# duplicate/near-duplicate titles (cannibalization)
grep -rhoE "<title>[^<]+" --include=*.html . | sort | uniq -d
```

## 5. Spanish mirror parity
The ES tree mirrors a subset of the EN tree. When a cluster with ES mirrors gains a page, the
mirror is part of the job, not a follow-up.

```
find es -name '*.html' | wc -l ; find . -name '*.html' -not -path './es/*' -not -path './.git/*' | wc -l
```

hreflang reciprocity is gated automatically. What the gate cannot check is whether the
cross-language link is **humanly visible** — verify that with a rendered screenshot.

## 6. Sourcing weakness
Scan new/edited pages for an unsourced number and fix before ship. Numbers that came from a
news roundup rather than the issuing agency should be re-pulled from the agency's own data.

## 7. Known, tracked gaps (do not "fix" without reading why)
- `/privacy/` and `/es/privacidad/` — linked from every lead-form consent checkbox, and
  do not exist. Creating them publishes a privacy/consent disclosure, which is a **safeguarded
  category**: draft and flag `NEEDS REVIEW`, never auto-publish. Listed in `KNOWN_MISSING`.
