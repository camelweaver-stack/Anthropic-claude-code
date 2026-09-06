# Source-of-truth reconciliation

*2026-08-24. Objective: one canonical source of truth → internally consistent
building pages → defensible public claims.*

## 1. Sources capable of producing building facts

| Source | Nature | Authority |
| --- | --- | --- |
| `site/dallastowers-data.json` | Canonical structured dataset (89 records; identity, county_2026 roll aggregates, dues where held) | **Canonical** |
| In-page V2 intelligence blocks | Per-building status panels with explicit states ("Verified", "Not yet verified — research in progress", "Dallas Towers derived") and inline provenance (e.g. "2026 listing disclosure") | Canonical presentation of status; provenanced values here outrank bare dataset values |
| Legacy deep-file prose | The classic section body on building pages; on 88 standard files it is disciplined ("pending document verification", county-sourced Q&As); Museum Tower alone carried a full legacy deep-file with unsourced specifics | Subordinate — valid only when consistent with the layers above |
| Hub/collection/derived tables | Generated from the dataset (county-file tables, roll-by-district) | Derived — regenerate, never hand-edit |
| `schemas/building.schema.json` | Architecture target incl. value-type law and verification states | Governing contract |

## 2. Precedence before this task

None existed. Museum Tower's legacy deep-file asserted exact rules, fees,
document inventories, and a legally-protected view directly beneath a V2 layer
stating those same categories were not yet verified and that no governing
documents were on file. Nothing prevented the contradiction.

## 3. Contradictions discovered (2026-08 audit)

All confined to **Museum Tower** (the deep-file prototype) plus one homepage
capability claim. 15+ findings; the critical set:

dues rate conflict (legacy ≈$1.42 vs provenanced $1.34), 5-yr dues-growth
figure with no observations, "no special assessments since 2019" absence claim,
dues-inclusion list, 12-month minimum lease + 15% rental cap + waitlist,
2-pet/100-lb limits, $500+$1,000 move fees, renovation hours, master-policy/
HO-6 terms, "Document set on file" vs "No governing documents on file yet",
"protected view — nothing can be built", parking ratios/valet/deeded storage,
exact plan tables with sf ranges, "owner-occupancy ratio ≈78%" (unproxied and
conflicting with the roll), "HOA litigation none active on record", "profile
from the most recent lender questionnaire we've reviewed", systems dues-inclusion
cells, and homepage "which stack has the protected view". The dataset itself
carried the legacy 1.42 dues figure.

## 4. Canonical precedence after this task

```
1. canonical structured field, verified with provenance      → renders as fact, source shown
2. structured reported/derived field with explicit status    → renders with its label
   ("reported — single-disclosure basis", "derived", "proxy")
3. legacy prose consistent with 1–2                          → may render
4. anything else                                             → suppressed or qualified
   ("Not yet verified — research in progress", what-to-verify framing)
```

A page must never state a specific consequential value for a category whose
canonical state is not_verified/unknown/conflicting. Enforced mechanically:
`scripts/reconcile-audit.py` (18 category detectors, severity-ranked, with
exemptions only for explicitly qualified text) runs inside
`scripts/validate-site.py`; any critical or high finding **fails production**.
Count claims on public pages are validated against the dataset. Protected-view
language, document-on-file claims, and unproxied occupancy ratios are all
detector categories.

## 5. Migration strategy for remaining legacy content

- 88 standard files: already consistent (status: reconciled). Their dues
  figures trace to the canonical dataset and carry "confirm on the resale
  certificate" framing; buildings without dues say "pending document
  verification".
- Museum Tower: reconciled in this pass — the reference implementation.
  Facts with real provenance were kept and labeled (dues from the 2026 listing
  disclosure; certified-roll sizes/bed-mix replacing the invented plan table;
  homestead proxy properly worded). Everything unsupported now renders as
  what-to-verify guidance.
- Future deep-files: authoring a rules/plans/documents section requires the
  provenance fields of `schemas/building.schema.json` first; the validator
  blocks unqualified specifics, so this contradiction class cannot quietly
  reappear.

## 6. Registry count vocabulary

- **Identified building** — entity in the census (dataset record). Currently 89.
- **Published file** — has a public building URL. Currently 89 (1:1 with census).
- **Verified file** — legacy `conf: v` (identity confirmed). Currently 78.
- **Partial file** — `conf: p`. Currently 11.
- **County-filed** — carries certified-roll economics. Currently 61.
- **Research pending** — gap set per `reports/building-coverage/`.

Every public count derives from `dallastowers-data.json`; the validator fails
any page whose stated totals drift from it. Audited 2026-08-24: /buildings
renders all 89 cards; homepage, /buildings, /dallas, /fort-worth and
/market-data figures all reconcile (no "41 of 41" state exists in this source).

## 7. Sales-data semantics (standing decision)

**No actual closed-sale dataset exists.** Texas is a non-disclosure state; the
site holds assessed values (certified rolls), deed-transfer records (dates and
counts only), and isolated listing disclosures (e.g. the Museum Tower dues
disclosure). All "real sales data"/"closed-sale" phrasing was removed in the
2026-08-24 passes; `verified_sale_price` exists in the schema for the only
legitimate future case (party-provided documented transactions) and is empty.
