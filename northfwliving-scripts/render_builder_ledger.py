#!/usr/bin/env python3
"""Renders the public Builder Ledger table fragment from verified records.

Reads the NEWEST snapshot in northfwliving-data/builder-ledger/ and emits an
HTML fragment (stdout) for the public /builder-ledger/ page:

  Builder | Community | Current offer | Verified | Expires

Publication rules (see northfwliving-data/builder-ledger/README.md):
  * Only records with source + source_url + verified_date render. Anything
    else is skipped with a warning on stderr.
  * With ZERO renderable records the script emits NOTHING (exit 0) — the
    public page keeps its current type-level table. No empty tables, no
    empty cells, no sample data.
  * Unknown expiration renders as "not published" — never an invented date.
  * source_url is kept as an internal HTML comment per row for auditability,
    not a public link, until a per-builder linking policy is decided.

This script is intentionally NOT wired into any page generation yet: it is
run manually when verified records exist, and its output is pasted/injected
into /builder-ledger/ by the normal editorial workflow.
"""
import html
import io
import json
import os
import re
import sys

DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def newest_snapshot(base):
    if not os.path.isdir(base):
        return None
    dirs = [d for d in sorted(os.listdir(base)) if DATE_RX.match(d) and os.path.isdir(os.path.join(base, d))]
    return os.path.join(base, dirs[-1]) if dirs else None


def offer_text(rec):
    if rec.get("offer_summary"):
        return rec["offer_summary"]
    parts = []
    if rec.get("flex_cash") is not None:
        parts.append(f"${rec['flex_cash']:,.0f} flex cash")
    if rec.get("advertised_rate") is not None:
        parts.append(f"{rec['advertised_rate']}% advertised rate")
    if rec.get("closing_cost_credit") is not None:
        parts.append(f"${rec['closing_cost_credit']:,.0f} closing-cost credit")
    if rec.get("design_center_credit") is not None:
        parts.append(f"${rec['design_center_credit']:,.0f} design-center credit")
    if rec.get("price_reduction") is not None:
        parts.append(f"${rec['price_reduction']:,.0f} price reduction")
    return "; ".join(parts)


def main():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "northfwliving-data", "builder-ledger")
    snap = newest_snapshot(os.path.abspath(base))
    if not snap:
        print("render_builder_ledger: no snapshots; nothing to render", file=sys.stderr)
        return 0
    data = json.load(io.open(os.path.join(snap, "records.json"), encoding="utf-8"))
    rows = []
    for rec in data.get("records", []):
        if not (rec.get("builder") and rec.get("source") and rec.get("source_url") and rec.get("verified_date")):
            print(f"render_builder_ledger: skipping unprovenanced record: {rec.get('builder')!r}", file=sys.stderr)
            continue
        offer = offer_text(rec)
        if not offer:
            print(f"render_builder_ledger: skipping record with no describable offer: {rec['builder']}", file=sys.stderr)
            continue
        expires = rec.get("expiration_date") or "not published"
        cells = [
            html.escape(rec["builder"]),
            html.escape(rec.get("community") or "—"),
            html.escape(offer),
            html.escape(rec["verified_date"]),
            html.escape(expires),
        ]
        audit = html.escape(rec["source_url"], quote=True).replace("--", "- -")
        rows.append("<tr><!-- source: " + audit + " -->" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    if not rows:
        print("render_builder_ledger: 0 renderable records; emitting nothing (page keeps its type-level table)", file=sys.stderr)
        return 0
    print('<table class="data">')
    print("<tr><th>Builder</th><th>Community</th><th>Current offer</th><th>Verified</th><th>Expires</th></tr>")
    for r in rows:
        print(r)
    print("</table>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
