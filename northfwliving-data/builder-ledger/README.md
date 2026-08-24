# The Builder Ledger — data architecture

The public Builder Ledger page (`/builder-ledger/`) currently tracks incentive
*types*, honest ranges, and verification paths. This directory is the
infrastructure that lets it grow into a dated, per-builder record — **as
verified observations accumulate**, not before.

## Layout

```
northfwliving-data/builder-ledger/
  schema.json          # JSON Schema for one record (all optional fields nullable)
  README.md            # this file
  2026-08-24/
    records.json       # snapshot: {"snapshot_date": ..., "records": [...]}
  2026-09-01/          # future observation passes — append-only
    records.json
```

Each snapshot directory is one observation pass. **Snapshots are append-only:
never edit or delete an old snapshot.** A change in an offer is expressed by a
new record in a new snapshot (optionally pointing back via `previous_value`).
That is what makes the Ledger able to answer, later:

* What is Builder X offering today?
* What was Builder X offering 30 days ago?
* Are incentives increasing or decreasing?
* Which communities have the largest concessions?
* Buydowns or price cuts? When does the offer expire?

## Collection rules

1. **Official sources only when they exist** — builder websites, official
   community/inventory pages, publicly advertised offers. No scraping in
   violation of site terms; no third-party summaries when an official source
   exists.
2. **Every record carries `source`, `source_url`, `verified_date`.** Records
   without them fail validation and can never render.
3. **Unknown stays null.** Especially `expiration_date`: if the builder does
   not publish one, record null and note "expiration unpublished". Never
   invent one.
4. **No sample/demo/fake records ever.** Test fixtures live in
   `northfwliving-scripts/tests/` and are generated in temp directories at
   test runtime — nothing in this tree is test data.
5. **No LLM-originated values.** See `../PROVENANCE.md`.

## Publication rules

* The public page shows **only** records that pass
  `northfwliving-scripts/validate_ledger_data.py` (schema + provenance).
  `northfwliving-scripts/render_builder_ledger.py` builds the table fragment;
  with zero verified records it emits nothing, and the page keeps its current
  type-level table.
* Empty fields are never rendered as empty cells — a column with no data is
  simply omitted.
* **No SEO page explosion.** The Ledger is a data product first: no URL per
  incentive, no URL per builder×month, no thin archive pages. Whether any
  historical/indexable pages are ever warranted is a decision for future GSC
  evidence, after the seasoning window.
