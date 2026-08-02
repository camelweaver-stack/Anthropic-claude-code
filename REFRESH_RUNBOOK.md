# REFRESH RUNBOOK — PCS Oahu data cadence
The freshness edge only exists if the cadence actually runs. Everything is single-sourced in
`gen/common.py`; a refresh is a constants edit + rebuild + gate + deploy + IndexNow ping.

## Cadence
| Trigger | What refreshes | Deadline |
|---|---|---|
| DTMO publishes new BAH (mid-December) | `BAH` dict, `BAH_YEAR`, report edition, pitch wave | Same day rates drop — this is the annual news hook |
| Monthly, March–August (PCS season) | Rent bands in `POCKETS`, `LAST_REFRESHED` | 1st of month |
| Quarterly, off-season | Rent bands, market medians (`MED_SF`, `MED_CONDO`) | 1st of quarter |
| FHFA limits (late November) | Loan-limit figures in /buy/ copy | Within a week |

## The refresh procedure (every time, no exceptions)
1. Pull sources: DTMO calculator (grade anchors), 2–3 public listing platforms per pocket
   (record which, keep the rounding deliberate), latest Honolulu Board of REALTORS® medians.
2. Edit `gen/common.py` only: `BAH`, `POCKETS`, `MED_SF`, `MED_CONDO`, `LAST_REFRESHED`,
   and `BUILD_DATE` (report edition label).
3. `python3 gen/build.py && python3 gen/gate.py` — gate enforces the visible refresh date on
   every rates block; a stale-looking build cannot ship green by hand-editing HTML.
4. Deploy `site/`, then POST the updated URL list via IndexNow and request reindex of
   `/bah-report/` in GSC.

## December BAH-cycle special (the big one)
- Update `dateModified` in `dataset_ld()` and `temporalCoverage` to the new year.
- Archive the outgoing edition: copy the old report body to
  `/bah-report/2026-edition.html` before overwriting (add to sitemap; run gate) so citations
  to prior editions never 404 — link rot kills a citation asset.
- Fire the PITCH_KIT.md outreach wave the same day. Speed is the story: "new BAH rates vs
  what Oahu actually rents for" is only news for about a week.
