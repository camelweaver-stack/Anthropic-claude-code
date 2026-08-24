#!/usr/bin/env python3
"""Source-of-truth contradiction detector.

Canonical state (2026-08): the structured layer (dallastowers-data.json +
in-page V2 intelligence blocks) has NO verified rules, documents, floor-plan
mappings, parking policies, or view protections for ANY building; HOA dues have
provenance only where a page's V2 block cites a source. Therefore any exact
consequential assertion in legacy prose is unsupported unless the page carries
an explicit provenance marker for that category.

Severity: critical = consequential buyer info; high = physical/unit specifics;
moderate = amenities/governance color.
Output: reports/source-of-truth/contradictions.csv + summary to stdout.
"""
import re, os, csv, html, json

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
data = json.load(open(os.path.join(ROOT, "dallastowers-data.json")))["buildings"]

CHECKS = [
    # (category, severity, regex on visible text)
    ("leasing_cap",   "critical", r"\b\d{1,2}%\s*(of units\s*)?(leased|rental cap|caps rentals)|caps rentals at \d{1,2}%"),
    ("lease_term",    "critical", r"\b(minimum lease( term)?|leases must run)\s*(of\s*)?\d{1,2}\+?\s*months?"),
    ("pets",          "critical", r"\b(max(imum)?\s*\d\s*pets?|\d\s*pets? (permitted|allowed|max))|weight limit\s*\d{2,3}\s*lb|\d{2,3}\s*lb (combined|weight)"),
    ("move_fees",     "critical", r"\$\d{2,4}[^.<]{0,30}(move-?in|move-?out|non-refundable fee)|\$\d{2,4}\s*refundable deposit"),
    ("renovation",    "critical", r"work hours\s*\d|renovation[^.<]{0,60}(9–5|9-5|weekday)"),
    ("insurance",     "critical", r"master policy covers|insurance to (the )?drywall|HO-?6 required"),
    ("assessments",   "critical", r"(no|none)[^.<]{0,30}special assessments?[^.<]{0,30}(since|on record)|special assessments?[^.<]{0,20}(none|no)\b[^.<]{0,25}(since \d{4}|on record)"),
    ("dues_history",  "critical", r"\d(-|\s)?yr dues growth|dues (grew|increased)[^.<]{0,20}\d+(\.\d+)?%|\+\d+(\.\d+)?%\s*/\s*yr avg"),
    ("dues_included", "critical", r"[Dd]ues include[sd]?\s"),
    ("view_protect",  "critical", r"protected view|nothing can be built|cannot be built|permanent(ly)? unobstructed|view[- ]protected|protected\s*✓"),
    ("documents",     "critical", r"[Dd]ocument set on file|(declaration|bylaws|reserve study|resale certificate)[^.<]{0,50}on file"),
    ("parking",       "critical", r"\d(–|-)\d assigned spaces|assigned spaces?\s*/\s*unit|valet[^.<]{0,25}included in dues|deeded storage"),
    ("floor_plans",   "high",     r"Plan [A-Z]\b[^<]{0,60}\d,\d{3}(–|-)\d,\d{3}\s*sf|Dimensioned PDFs"),
    ("stack_claims",  "high",     r"[“\"]?0\d[”\"]?\s*stack (faces|looks)"),
    ("amenity_spec",  "moderate", r"\d{2}'? ?(infinity|lap)[- ]?(edge )?pool|guest suites \(\d\)"),
    ("governance",    "moderate", r"Board\s*\d\s*owner-elected|≈?\d+\s*FTE"),
    ("litigation",    "critical", r"litigation[^.<]{0,30}[Nn]one (active )?on record"),
    ("questionnaire", "critical", r"questionnaire we'?ve reviewed"),
    ("ooc_unproxied", "critical", r"[Oo]wner-occupancy ratio\s*≈?\d{2}%"),
    ("dues_incl2",    "critical", r"included in dues|[Bb]uilding-paid, in dues"),
]
# a finding is exempt when the surrounding text explicitly qualifies it
QUALIFIED = re.compile(r"not yet (verified|observed|recorded)|what to verify|research in progress|publish(es)? only (with|from) (the )?(governing )?document", re.I)
# provenance markers that legitimize a category on that page
PROV = {
    "dues_included": r"(listing disclosure|resale certificate dated|per the (declaration|budget) dated)",
}

def visible(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))

def slugify(n):
    x=n.lower().replace("&","and").replace("'","").replace("’","")
    return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",x)).strip("-")
slugs={slugify(b["name"]) for b in data} | {"texas-pacific-lofts"}

rows=[]
for fn in sorted(os.listdir(ROOT)):
    if not fn.endswith(".html") or fn[:-5] not in slugs: continue
    vt = visible(open(os.path.join(ROOT, fn), encoding="utf-8").read())
    for cat, sev, pat in CHECKS:
        for m in re.finditer(pat, vt):
            ctx = vt[max(0,m.start()-60):m.end()+60]
            wide = vt[max(0,m.start()-260):m.end()+260]
            if QUALIFIED.search(wide): continue
            if cat in PROV and re.search(PROV[cat], ctx, re.I): continue
            rows.append({"building": fn[:-5], "category": cat, "severity": sev,
                         "canonical_state": "not_verified", "assertion": ctx.strip()[:160]})
            break  # one hit per category per page is enough for the report

os.makedirs(os.path.join(os.path.dirname(ROOT), "reports", "source-of-truth"), exist_ok=True)
out=os.path.join(os.path.dirname(ROOT), "reports", "source-of-truth", "contradictions.csv")
with open(out,"w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=["building","category","severity","canonical_state","assertion"])
    w.writeheader(); w.writerows(rows)
from collections import Counter
print(f"{len(rows)} findings across {len(set(r['building'] for r in rows))} buildings -> {out}")
print("by severity:", dict(Counter(r["severity"] for r in rows)))
print("by category:", dict(Counter(r["category"] for r in rows)))
print("\nbuildings with critical findings:")
crit = Counter(r["building"] for r in rows if r["severity"]=="critical")
for b,c in crit.most_common(20): print(f"  {c:2d}  {b}")
