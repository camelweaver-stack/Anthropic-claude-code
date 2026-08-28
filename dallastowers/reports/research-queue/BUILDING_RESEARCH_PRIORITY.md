# Building research priority queue

*Generated 2026-08-24 from the deterministic coverage scoring
(`scripts/coverage-report.py`) plus strategic weighting. This queue guides future
verification work — it does not authorize filling any field without a verified
source. No speculative values were inserted anywhere in this pass.*

GSC note: the property currently has ~0 impressions (weeks old), so search-demand
signal is absent; ranks below lean on unit count, assessed scale, transfer tempo,
district, and gap size. Re-rank once GSC accumulates building-name query data.

| # | Building / scope | Missing data | Commercial importance | Likely authoritative source | Priority |
|---|---|---|---|---|---|
| 1 | **All 20 Fort Worth buildings** (batch) | Tarrant certified roll: assessed medians, homestead proxy, transfer tempo | Unlocks county sections for the whole FW registry — largest single gap | TAD 2026 certified roll + Tarrant County recorded instruments | 1 |
| 2 | The Renaissance on Turtle Creek | HOA dues + included services | 482 units, highest-tempo tower on file (42 t12) | Budget / resale certificate / declaration | 1 |
| 3 | Twenty-One Turtle Creek | HOA dues | 310 units, 34 t12, value-collection anchor | Budget / resale certificate | 1 |
| 4 | Museum Tower | Leasing restrictions + min lease term | Flagship file; high buyer-intent relevance | Declaration / rules / resale documentation | 1 |
| 5 | The Vendome | HOA dues | Marquee Turtle Creek tower, high assessed scale | Budget / resale certificate | 1 |
| 6 | The Tower Residences (Ritz-Carlton) | HOA dues + hotel-service cost split | Hotel-branded premium file | Budget / management agreement summary | 1 |
| 7 | Turtle Creek North | Floor count + HOA dues | High homestead share (85%), corridor anchor | Site verification + budget | 2 |
| 8 | Residences at The Ritz-Carlton I | Leasing + pet rules | Has dues (1.75); rules complete the flagship pair | Declaration / rules | 2 |
| 9 | Plaza at Turtle Creek II | Floor count + HOA dues | Twin-phase entity; phase II thinner than I | Site verification + budget | 2 |
| 10 | Metropolitan Club at Hotel ZaZa | Address, floors, units | Skeletal core identity (Dallas) | County parcel record + developer filing | 2 |
| 11 | Main 7 | Address, floors, units | Skeletal FW file | Tarrant parcel record | 2 |
| 12 | Schaumburg Lofts | Address, floors, units | Skeletal FW file | Tarrant parcel record | 2 |
| 13 | Dickson Jenkins Lofts | Address, floors, units | Skeletal FW file | Tarrant parcel record | 2 |
| 14 | One Museum Place Residences | Address, floors, units | Skeletal Dallas file, Arts District | DCAD parcel record | 2 |
| 15 | The Lakeside Tower / Westview / Versailles / Royale Orleans (4 skeletal) | Addresses + core identity | Close the 9 placeholder-address gap | County parcel records | 2 |
| 16 | Bleu Ciel | Leasing + STR policy | High-value Harwood tower, frequent renter interest | Declaration / rules | 2 |
| 17 | Azure | Pet policy + leasing | High-value Harwood tower | Declaration / rules | 2 |
| 18 | The House | Rental cap + min term | Victory Park investor interest | Declaration / rules | 3 |
| 19 | W Dallas Residences | Hotel-service inclusions in dues | Hotel-branded premium file | Budget / management docs | 3 |
| 20 | Preston Tower | HOA dues + special-assessment status | 261 units, older tower — assessment risk is the buyer question | Budget / reserve study / minutes | 3 |
| 21 | The Athena | Special-assessment history | 1966 tower, no-pets bylaw already filed; assessments complete the risk picture | Budget / reserve study | 3 |
| 22 | Top-7 schematic buildings | Stack/orientation records to pair with existing plan SVGs | Converts 7 schematics into structured floor-plan records | Existing verified measurements + plan sources | 3 |
| 23 | 39 buildings missing floor count | Floor counts | Core identity completeness for verified tier | County records / site verification | 3 |
| 24 | Omni Fort Worth Residences | HOA dues + hotel-service split | Strongest FW file; completes after TAD batch | Budget / management docs | 3 |
| 25 | The Grand Treviso | Owner-occupancy proxy fields missing from county blob (`ooc_pct`) | Data-quality patch to existing county record | DCAD roll re-pull | 3 |

**Operating rule:** work top-down; each completed task updates the permanent entity
with a provenance record (source, date, confidence) per `schemas/building.schema.json`,
and history-bearing fields (HOA) append rather than overwrite.
