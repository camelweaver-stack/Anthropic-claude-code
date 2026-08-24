#!/usr/bin/env python3
"""Validates Builder Ledger snapshots against the record schema and the
provenance rules in northfwliving-data/PROVENANCE.md.

Checks, per snapshot directory (northfwliving-data/builder-ledger/YYYY-MM-DD/):
  * records.json parses and has snapshot_date matching its directory name
  * every record has the mandatory provenance trio: source, source_url,
    verified_date (ISO date), plus a non-empty builder name
  * no unknown fields (schema drift guard), and enums/types are respected
  * verified_date is not in the future relative to snapshot_date
  * no obviously fake/sample data (builder names like "test", "sample",
    "example", "acme", "todo")

Exit 0 = all snapshots valid (zero snapshots is also valid).
Exit 1 = validation failure — the build/deploy must abort.
"""
import io
import json
import os
import re
import sys

ALLOWED_FIELDS = {
    "builder", "community", "city", "offer_type", "offer_summary",
    "advertised_rate", "rate_conditions", "closing_cost_credit",
    "design_center_credit", "flex_cash", "price_reduction",
    "eligible_inventory", "effective_date", "expiration_date", "source",
    "source_url", "verified_date", "confidence", "previous_value", "notes",
}
OFFER_TYPES = {
    "flex_cash", "permanent_buydown", "temporary_buydown_2_1",
    "closing_cost_credit", "design_center_credit", "price_reduction",
    "quick_move_in", "other", None,
}
CONFIDENCE = {"verified", "reported", None}
DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FAKE_RX = re.compile(r"\b(test|sample|example|acme|todo|fake|placeholder|demo)\b", re.I)
NUMERIC_FIELDS = {
    "advertised_rate", "closing_cost_credit", "design_center_credit",
    "flex_cash", "price_reduction",
}
DATE_FIELDS = {"effective_date", "expiration_date"}


def validate_record(rec, idx, snapshot_date, errors):
    where = f"record[{idx}]"
    if not isinstance(rec, dict):
        errors.append(f"{where}: not an object")
        return
    unknown = set(rec) - ALLOWED_FIELDS
    if unknown:
        errors.append(f"{where}: unknown fields {sorted(unknown)}")
    for req in ("builder", "source", "source_url", "verified_date"):
        if not rec.get(req):
            errors.append(f"{where}: missing required provenance field '{req}'")
    b = rec.get("builder") or ""
    if FAKE_RX.search(b):
        errors.append(f"{where}: builder name {b!r} looks like sample/fake data")
    vd = rec.get("verified_date") or ""
    if vd and not DATE_RX.match(vd):
        errors.append(f"{where}: verified_date {vd!r} is not an ISO date")
    elif vd and vd > snapshot_date:
        errors.append(f"{where}: verified_date {vd} is after snapshot {snapshot_date}")
    for f in DATE_FIELDS:
        v = rec.get(f)
        if v is not None and (not isinstance(v, str) or not DATE_RX.match(v)):
            errors.append(f"{where}: {f} must be null or ISO date, got {v!r}")
    for f in NUMERIC_FIELDS:
        v = rec.get(f)
        if v is not None and not isinstance(v, (int, float)):
            errors.append(f"{where}: {f} must be null or a number, got {v!r}")
    if rec.get("offer_type") not in OFFER_TYPES:
        errors.append(f"{where}: offer_type {rec.get('offer_type')!r} not in {sorted(t for t in OFFER_TYPES if t)}")
    if rec.get("confidence") not in CONFIDENCE:
        errors.append(f"{where}: confidence {rec.get('confidence')!r} invalid")
    su = rec.get("source_url") or ""
    if su and not su.startswith(("http://", "https://")):
        errors.append(f"{where}: source_url {su!r} is not a URL")


def main(base=None):
    base = base or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "northfwliving-data", "builder-ledger"
    )
    base = os.path.abspath(base)
    errors = []
    snapshots = 0
    records = 0
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            d = os.path.join(base, name)
            if not os.path.isdir(d):
                continue
            if not DATE_RX.match(name):
                errors.append(f"{name}: snapshot directory is not YYYY-MM-DD")
                continue
            snapshots += 1
            rj = os.path.join(d, "records.json")
            if not os.path.isfile(rj):
                errors.append(f"{name}: missing records.json")
                continue
            try:
                data = json.load(io.open(rj, encoding="utf-8"))
            except ValueError as e:
                errors.append(f"{name}/records.json: invalid JSON: {e}")
                continue
            if data.get("snapshot_date") != name:
                errors.append(f"{name}: snapshot_date {data.get('snapshot_date')!r} != directory name")
            recs = data.get("records")
            if not isinstance(recs, list):
                errors.append(f"{name}: 'records' must be a list")
                continue
            records += len(recs)
            for i, rec in enumerate(recs):
                validate_record(rec, i, name, errors)
    if errors:
        for e in errors:
            print("ERROR " + str(e))
        print(f"ledger validator: FAIL — {len(errors)} error(s)")
        return 1
    print(f"ledger validator: OK — {snapshots} snapshot(s), {records} verified record(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
