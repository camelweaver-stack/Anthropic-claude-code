#!/usr/bin/env python3
"""Seasoning cohort tracker for northfwliving.com.

Reads dated GSC performance exports from northfwliving-data/gsc/<YYYY-MM-DD>/
(the standard Search Console CSV export: Pages.csv, Queries.csv, Chart.csv)
and reports, per export:

  * the seasoning cohort pages (defined in cohorts.json) with impressions,
    clicks, CTR, and average position — compared URL-by-URL across exports,
    never as a sitewide average
  * sitewide totals: pages receiving impressions, total impressions, clicks,
    distinct queries, and average daily impressions over the active window

Usage:
  gsc_cohort_report.py                 # report every snapshot, oldest first
  gsc_cohort_report.py 2026-08-24 2026-10-01   # compare two snapshots

New exports: unzip the GSC "Performance on Search" download into
northfwliving-data/gsc/<export-date>/ and re-run. Directories are
append-only; never overwrite an old export.
"""
import csv
import io
import json
import os
import re
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "northfwliving-data", "gsc"))
DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_pages(d):
    out = {}
    with io.open(os.path.join(d, "Pages.csv"), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            url = row.get("Top pages") or row.get("Page")
            if not url:
                continue
            out[url] = {
                "clicks": int(row["Clicks"]),
                "impressions": int(row["Impressions"]),
                "ctr": row["CTR"],
                "position": float(row["Position"]),
            }
    return out


def load_totals(d):
    days_active = 0
    impressions = 0
    clicks = 0
    chart = os.path.join(d, "Chart.csv")
    if os.path.isfile(chart):
        with io.open(chart, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                imp = int(row["Impressions"] or 0)
                impressions += imp
                clicks += int(row["Clicks"] or 0)
                if imp:
                    days_active += 1
    queries = 0
    qf = os.path.join(d, "Queries.csv")
    if os.path.isfile(qf):
        with io.open(qf, encoding="utf-8-sig") as f:
            queries = sum(1 for _ in csv.DictReader(f))
    return {"impressions": impressions, "clicks": clicks, "days_with_impressions": days_active, "distinct_queries": queries}


def main(argv):
    cohorts = json.load(io.open(os.path.join(BASE, "cohorts.json"), encoding="utf-8"))
    snaps = argv or sorted(d for d in os.listdir(BASE) if DATE_RX.match(d) and os.path.isdir(os.path.join(BASE, d)))
    if not snaps:
        print("no GSC snapshots found under", BASE)
        return 1
    data = {}
    for s in snaps:
        d = os.path.join(BASE, s)
        if not os.path.isdir(d):
            print(f"snapshot {s} not found under {BASE}")
            return 1
        data[s] = {"pages": load_pages(d), "totals": load_totals(d)}

    w = max(len(c["label"]) for c in cohorts["cohorts"]) + 2
    print("SEASONING COHORTS — position (impressions) by export date")
    print("Baseline: " + cohorts["baseline_date"] + " · compare the same URLs, not sitewide averages\n")
    header = "".ljust(w) + "".join(s.center(20) for s in snaps)
    print(header)
    for c in cohorts["cohorts"]:
        line = c["label"].ljust(w)
        for s in snaps:
            p = data[s]["pages"].get(c["url"])
            cell = f"{p['position']:.1f} ({p['impressions']})" if p else "—"
            line += cell.center(20)
        print(line)

    print("\nSITEWIDE")
    for s in snaps:
        t = data[s]["totals"]
        pages_with_impressions = sum(1 for v in data[s]["pages"].values() if v["impressions"] > 0)
        daily = t["impressions"] / t["days_with_impressions"] if t["days_with_impressions"] else 0
        print(
            f"  {s}: {pages_with_impressions} pages with impressions · "
            f"{t['impressions']} impressions · {t['clicks']} clicks · "
            f"{t['distinct_queries']} distinct queries · "
            f"{daily:.1f} impressions/day over {t['days_with_impressions']} active days"
        )

    if len(snaps) >= 2:
        a, b = snaps[0], snaps[-1]
        print(f"\nMOVEMENT {a} → {b} (cohort pages)")
        for c in cohorts["cohorts"]:
            pa, pb = data[a]["pages"].get(c["url"]), data[b]["pages"].get(c["url"])
            if pa and pb:
                delta = pa["position"] - pb["position"]
                arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "→")
                print(f"  {c['label']}: {pa['position']:.1f} → {pb['position']:.1f}  {arrow} {abs(delta):.1f}")
            elif pa and not pb:
                print(f"  {c['label']}: dropped out of the report (was {pa['position']:.1f})")
            elif pb and not pa:
                print(f"  {c['label']}: newly receiving impressions at {pb['position']:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
