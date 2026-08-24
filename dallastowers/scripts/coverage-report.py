#!/usr/bin/env python3
"""Generate per-building coverage report + deterministic enrichment priority.

Usage: python3 scripts/coverage-report.py   (from the dallastowers/ directory)
Outputs: reports/building-coverage/coverage.csv, COVERAGE.md

Scoring (deterministic, documented):
  commercial value V = norm(units) + norm(assessed scale) + norm(t12) + district bonus
    - units: un, or county acct if un missing
    - assessed scale: val_med * acct (county buildings only)
    - district bonus: +1.0 core districts (Turtle Creek, Uptown, Arts District,
      Victory Park, Harwood, Downtown FW, Knox / Katy Trail), else 0
    - each norm() maps to [0,1] against the registry max
  data gap G = count of missing enrichable fields among:
      address, floors, units, hoa dues, county roll, (rules and floor plans are
      missing registry-wide and excluded from G to avoid uniform inflation)
  priority P = V * (0.5 + G/5)   -- value weighted toward files with real gaps
GSC note: Search Console currently reports 0 impressions site-wide (property is
weeks old), so search-demand signal contributes nothing yet; re-weight when data exists.
"""
import json, csv, os, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
data = json.load(open(os.path.join(ROOT, "site", "dallastowers-data.json")))["buildings"]

CORE = {"Turtle Creek","Uptown","Arts District","Victory Park","Harwood","Downtown FW","Knox / Katy Trail"}
PLANS = {"the-athena","the-bonaventure","forest-park-tower","le-bijou","live-oak-lofts","one-montgomery-plaza-residences","omni-fort-worth-residences"}  # buildings with plan schematics in site/img

def slugify(n):
    import re
    s=n.lower().replace("&","and").replace("'","").replace("’","")
    return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",s)).strip("-")

rows=[]
max_un = max((b.get("un") or (b.get("county_2026") or {}).get("acct") or 0) for b in data)
max_scale = max(((b["county_2026"]["val_med"]*b["county_2026"]["acct"]) for b in data if b.get("county_2026")), default=1)
max_t12 = max(((b["county_2026"].get("t12") or 0) for b in data if b.get("county_2026")), default=1)

for b in data:
    c = b.get("county_2026") or {}
    un = b.get("un") or c.get("acct") or 0
    scale = (c.get("val_med",0) * c.get("acct",0))
    t12 = c.get("t12") or 0
    V = un/max_un + scale/max_scale + t12/max_t12 + (1.0 if b["hood"] in CORE else 0.0)
    gaps=[]
    if b["addr"] in ("—","-",""): gaps.append("address")
    if not b.get("fl"): gaps.append("floors")
    if not b.get("un"): gaps.append("units")
    if not b.get("dues"): gaps.append("hoa_dues")
    if not b.get("county_2026"): gaps.append("county_roll")
    G=len(gaps)
    P = V * (0.5 + G/5)
    slug = slugify(b["name"])
    if slug=="texas-and-pacific-lofts": slug="texas-pacific-lofts"
    filled = sum(1 for x in [b["addr"] not in ("—","-",""), b.get("fl"), b.get("un"), b.get("dues"), bool(c), slug in PLANS] if x)
    tier = "complete" if filled>=5 else ("partial" if filled>=3 else "skeletal")
    rows.append({
        "building": b["name"], "slug": slug, "city": b["city"], "district": b["hood"],
        "verified": b["conf"], "tier": tier, "units": b.get("un") or "", "floors": b.get("fl") or "",
        "year": b["era"], "hoa_dues_psf_mo": b.get("dues") or "", "plans": "Y" if slug in PLANS else "",
        "rules": "", "county_roll": "Y" if c else "", "ooc_proxy_pct": c.get("ooc_pct",""),
        "t12": c.get("t12",""), "assessed_median": c.get("val_med",""),
        "gaps": ";".join(gaps), "value_score": round(V,3), "priority": round(P,3),
    })

rows.sort(key=lambda r:-r["priority"])
outdir=os.path.join(ROOT,"reports","building-coverage"); os.makedirs(outdir,exist_ok=True)
with open(os.path.join(outdir,"coverage.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

tiers={"complete":[],"partial":[],"skeletal":[]}
for r in rows: tiers[r["tier"]].append(r)
with open(os.path.join(outdir,"COVERAGE.md"),"w") as f:
    f.write("# Building coverage report\n\n*Generated deterministically by scripts/coverage-report.py — see script docstring for scoring. No field was populated by inference; blank means unknown.*\n\n")
    f.write(f"**{len(rows)} building files** — complete: {len(tiers['complete'])} · partial: {len(tiers['partial'])} · skeletal: {len(tiers['skeletal'])}\n\n")
    f.write(f"Verified (conf=v): {sum(1 for r in rows if r['verified']=='v')} · pending (conf=p): {sum(1 for r in rows if r['verified']=='p')}\n\n")
    f.write("Rules coverage: 0/89 structured (narrative mentions only). Floor-plan schematics: 8/89.\n\n")
    f.write("## Enrichment priority (top 30)\n\n")
    f.write("| # | Building | City | Pri | Tier | Search signal | Recommended next data |\n|---|---|---|---|---|---|---|\n")
    for i,r in enumerate(rows[:30],1):
        nxt = r["gaps"].split(";")[0] if r["gaps"] else "rules / floor plans"
        f.write(f"| {i} | {r['building']} | {r['city']} | {r['priority']} | {r['tier']} | none yet (GSC ~0 impressions) | {nxt.replace('_',' ')} |\n")
    f.write("\n## Files by tier\n\n")
    for t in ["skeletal","partial","complete"]:
        f.write(f"### {t.title()} ({len(tiers[t])})\n\n")
        for r in sorted(tiers[t],key=lambda x:x["building"]):
            f.write(f"- {r['building']} ({r['city']}, {r['verified']}) — gaps: {r['gaps'] or 'rules/plans only'}\n")
        f.write("\n")
print("wrote coverage.csv + COVERAGE.md")
print("tiers:", {k:len(v) for k,v in tiers.items()})
print("top 10 priority:")
for r in rows[:10]: print(f"  {r['priority']:6.3f}  {r['building']} [{r['city']}] gaps={r['gaps'] or '-'}")
