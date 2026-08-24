# North FW Living — Provenance Standard

Every mutable data point that can reach a public page must be auditable.
This standard defines the reusable provenance envelope used across the
Builder Ledger, the neighborhood/pocket dataset, and any future dataset.

## The provenance envelope

A provenanced value is an object, not a bare scalar:

```json
{
  "value": null,
  "source": null,
  "source_url": null,
  "verified_date": null,
  "effective_date": null,
  "expiration_date": null,
  "confidence": null,
  "notes": null
}
```

| Field | Meaning |
| --- | --- |
| `value` | The datum itself. `null` = unknown. Never guess. |
| `source` | Human-readable origin (e.g. "Official builder community page", "Denton CAD record", "Northwest ISD attendance-zone tool"). |
| `source_url` | Direct URL to the source when one exists. |
| `verified_date` | ISO date the value was last checked against the source. |
| `effective_date` | ISO date the value took effect, if known. |
| `expiration_date` | ISO date the value expires, if known. If unknown, leave `null` — never invent one. |
| `confidence` | `"verified"` (checked against a primary source), `"reported"` (secondary source), or `"estimated"` (modeled — the model must be described in `notes`). |
| `notes` | Free text: conditions, caveats, how it was checked. |

Not every field is required everywhere. The rules that ARE mandatory:

1. **`null` beats a guess.** An unknown stays `null`/`"unknown"`. No field is
   ever populated to make a table look complete.
2. **Nothing renders publicly without `source` + `verified_date`.** Render
   scripts must skip records that lack them.
3. **Primary sources outrank summaries.** When an official builder/agency
   source exists, third-party summaries are not acceptable evidence.
4. **History is append-only.** New observations are added as new dated
   snapshots; old records are never overwritten (see the Builder Ledger
   snapshot layout).
5. **No LLM-invented values.** Language models may format and check this
   data; they may not originate values for it.

## Dataset locations

| Dataset | Path | Snapshot policy |
| --- | --- | --- |
| Builder Ledger | `northfwliving-data/builder-ledger/<YYYY-MM-DD>/records.json` | One dated directory per observation pass; append-only |
| Neighborhoods/pockets | `northfwliving-data/neighborhoods/*.json` | In-place, but every field carries `verified_date`; superseded values move to the record's `history` list |
| GSC baselines | `northfwliving-data/gsc/<YYYY-MM-DD>/` | One dated directory per export; append-only |
