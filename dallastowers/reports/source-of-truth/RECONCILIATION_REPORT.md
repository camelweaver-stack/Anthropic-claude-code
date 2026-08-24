# Reconciliation report — 2026-08-24

Detector: `scripts/reconcile-audit.py` over all 89 building files
(18 categories; critical/high/moderate). Post-fix state: **0 findings**.

| Building | Critical | High | Moderate | Reconciled | Remaining |
| --- | --- | --- | --- | --- | --- |
| Museum Tower | 14 | 2 | 2 | 18 | 0 |
| Other 88 files | 0 | 0 | 0 | — | 0 |
| index.html (capability claim) | 1 | 0 | 0 | 1 | 0 |

## Critical contradictions and resolutions (Museum Tower)

| Canonical field | Canonical state | Legacy assertion | Provenance found? | Resolution |
| --- | --- | --- | --- | --- |
| hoa_amount | verified ($1.34/sf/mo, 2026 listing disclosure) | "≈$1.42/sf/month" (page + dataset + FAQ) | Yes — for $1.34 only | Migrated: $1.34 with source stated; dataset corrected (v2026-08.3) |
| hoa_includes | not_verified | "Dues include chilled water HVAC, valet, concierge, gas, water, trash, reserves" (×3 incl. FAQ, systems table) | No | Suppressed; "inclusions not yet verified — confirm on resale certificate" |
| dues history | no observations | "5-yr dues growth +3.1%/yr avg" | No | Removed; "Not yet observed — tracking begins 2026" |
| special_assessment | not_verified | "None on record since 2019" | No | Replaced with "Not yet verified" (absence never inferred from missing evidence) |
| leasing_allowed / rental_cap / minimum_lease_term | not_verified | "12-month minimum; 15% cap; waitlist; STR prohibited" (§03 + FAQ) | No | Suppressed; what-to-verify framing |
| pet_policy | not_verified | "Max 2 pets, 100 lb combined" | No | Suppressed; what-to-verify framing |
| move fees | not_verified | "$500 fee + $1,000 deposit" | No | Suppressed |
| renovation_rules | not_verified | "work hours 9–5 weekdays…" | No | Suppressed |
| insurance | not_verified | "Master policy to drywall; HO-6 $50K minimum" | No | Suppressed |
| documents | none on file | "Document set on file: declaration · bylaws · rules · budgets · reserve study · resale certificate — request the set" | No | Replaced with "None on file yet" + request checklist (matches V2) |
| view protection | not_verified | "'01' stack… is the protected view — nothing can be built"; "protected ✓" | No legal evidence | Directional/public-space facts retained; protection claim removed |
| parking / storage | not_verified | "2–4 assigned spaces/unit; valet included in dues; deeded storage" | No | Suppressed; verify-on-deed guidance |
| litigation | not_verified | "HOA litigation: none active on record" | No | "Not yet verified" |
| occupancy proxy | 65% homestead (roll) | "Owner-occupancy ratio ≈78%" | Conflicting, unproxied | Replaced with homestead-proxy wording, 65%, certified roll |

High: plan table (Plans A–D + penthouse sf ranges; "Dimensioned PDFs for every
plan available on request") and per-stack orientation map — replaced with
certified-roll size/bed-mix panel + research-in-progress status. Moderate:
amenities list and governance specifics — amenities retained under a
"reported — not yet recorded as verified" label; board/staff figures suppressed.

Homepage: "which stack in the building has the protected view" capability claim
rewritten to a defensible directional example.

## Regression guards now in production

critical/high detector findings fail the build; document-on-file, protected-view,
unproxied-occupancy, dues-inclusion and count-drift are all detector categories;
qualified language ("not yet verified/observed/recorded", what-to-verify) is the
only exemption path.
