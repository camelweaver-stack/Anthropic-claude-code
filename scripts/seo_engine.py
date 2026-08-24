#!/usr/bin/env python3
"""West FW Living — GSC opportunity engine.

The closed-loop half of the publishing system: ingest Google Search Console
exports, keep longitudinal snapshots, and turn them into a ranked, intent-
weighted optimization queue. Stdlib only. See docs/SEO_GROWTH_SYSTEM.md for
the operating specification and data/seo/config.json for tunable weights.

Usage (from repo root):
  python3 scripts/seo_engine.py ingest <export.zip|dir> [--date YYYY-MM-DD]
  python3 scripts/seo_engine.py report [--snapshot YYYY-MM-DD] [--prev YYYY-MM-DD]
  python3 scripts/seo_engine.py linkaudit
  python3 scripts/seo_engine.py log-event --url /path --reason "..." --change "..." \
      [--kinds title,content,links,schema,cluster]

Snapshots live in data/gsc/YYYY-MM-DD/ and are never overwritten.
Reports land in reports/seo/. Optimization events append to data/seo/events.jsonl.
"""
import argparse
import csv
import io
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict, deque
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DOMAIN = "https://westfwliving.com"
GSC_DIR = "data/gsc"
SEO_DIR = "data/seo"
REPORT_DIR = "reports/seo"
CONFIG_PATH = os.path.join(SEO_DIR, "config.json")
EVENTS_PATH = os.path.join(SEO_DIR, "events.jsonl")

DEFAULT_CONFIG = {
    "weights": {
        "position_opportunity": 3.0,   # peaks in the strike zone (pos 6-15)
        "impressions": 2.0,            # log-scaled demand evidence
        "commercial_intent": 3.0,      # 0-3 rubric, see intent_score()
        "ctr_gap": 2.0,                # underperforming CTR at earning positions
        "cluster_strategic": 1.5,      # member of a priority cluster
        "link_deficit": 1.0,           # few inbound internal links (needs linkaudit run)
        "low_evidence_penalty": -1.0,  # impressions < min_evidence
    },
    "min_evidence_impressions": 3,
    "priority_clusters": ["lockheed", "aledo", "walsh", "benbrook", "willow-park",
                          "hudson-oaks", "white-settlement", "property-tax", "isd",
                          "new-construction", "compare"],
    "allocation": {"expand_winners": 0.40, "push_6_20": 0.25,
                   "new_high_intent": 0.20, "maintain_factual": 0.10,
                   "exploratory": 0.05},
    "expected_ctr_by_position": [[1, 0.28], [2, 0.15], [3, 0.10], [4, 0.07],
                                  [5, 0.05], [10, 0.03], [20, 0.015], [100, 0.005]],
}

# ---------------------------------------------------------------- intent rubric
VERY_HIGH = ["moving to", "relocat", "best neighborhood", "vs ", " vs", "property tax",
             "new construction", "new homes", "homes for sale", "buying", "buy a house",
             "school district", "isd", "commute", "subdivision", "builder", "lockheed",
             "nas jrb", "living in", "walsh", "morningstar", "parks of aledo", "summit ranch",
             "homestead", "aledo bluffs", "silverado", "montserrat", "montrachet", "grasslands"]
HIGH = ["cost of living", "hoa", "pid", "mud", "school boundar", "school zone", "price range",
        "aledo", "willow park", "hudson oaks", "benbrook", "white settlement", "weatherford",
        "apartments near", "apartments for rent aledo", "closing cost", "va loan", "bah",
        "rent report", "specials", "weeks free", "sell", "net proceeds", "tuition",
        "down payment", "first time"]
MEDIUM = ["restaurant", "bbq", "recreation", "school", "elementary", "high school",
          "fort worth", "events", "sports", "kids", "private school"]
LOCAL_TOKENS = ["aledo", "willow park", "hudson oaks", "benbrook", "white settlement",
                "weatherford", "fort worth", "walsh", "lockheed", "nas jrb", "parker county",
                "tarrant", "76008", "76108", "brock", "annetta", "dfw"]
GENERIC_LOW = ["credit score", "break a lease", "breaking a lease", "renters insurance",
               "sublet", "sublease", "reletting", "rent to own homes", "lease to own",
               "apartments for rent near me", "homes for rent near me", "houses for rent near me",
               "rental score", "rentgrow", "progress residential", "zillow"]


def intent_score(text):
    """0-3 commercial-intent rubric for a query or a URL slug."""
    t = " " + text.lower().replace("-", " ").replace("/", " ") + " "
    local = any(k in t for k in LOCAL_TOKENS)
    if any(k in t for k in GENERIC_LOW) and not local:
        return 0
    if any(k in t for k in VERY_HIGH) and local:
        return 3
    if any(k in t for k in VERY_HIGH) or (any(k in t for k in HIGH) and local):
        return 2 if local else 1
    if any(k in t for k in HIGH):
        return 1
    if any(k in t for k in MEDIUM) and local:
        return 1
    return 0


def intent_label(s):
    return {3: "very-high", 2: "high", 1: "medium", 0: "low"}[s]


# ---------------------------------------------------------------- url handling
def canon_url(u):
    """Normalize a GSC URL to the site's canonical extensionless path."""
    p = u.replace(DOMAIN, "").split("?")[0].split("#")[0] or "/"
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    elif p.endswith(".html"):
        p = p[:-5]
    return p


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    os.makedirs(SEO_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=1)
    return dict(DEFAULT_CONFIG)


def expected_ctr(pos, cfg):
    for limit, ctr in cfg["expected_ctr_by_position"]:
        if pos <= limit:
            return ctr
    return 0.005


# ---------------------------------------------------------------- snapshots
CSV_ALIASES = {  # GSC export filename -> normalized snapshot filename
    "pages.csv": "pages.csv", "queries.csv": "queries.csv", "chart.csv": "chart.csv",
    "devices.csv": "devices.csv", "countries.csv": "countries.csv",
    "search appearance.csv": "search_appearance.csv", "search_appearance.csv": "search_appearance.csv",
    "filters.csv": "filters.csv", "dates.csv": "chart.csv",
}
HEADER_MAP = {"top pages": "page", "page": "page", "top queries": "query", "query": "query",
              "date": "date", "device": "device", "country": "country",
              "search appearance": "search_appearance", "clicks": "clicks",
              "impressions": "impressions", "ctr": "ctr_pct", "position": "position",
              "filter": "filter", "value": "value"}


def _norm_rows(text):
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return []
    hdr = [HEADER_MAP.get(h.strip().lower(), h.strip().lower()) for h in rows[0]]
    out = [hdr]
    for r in rows[1:]:
        r = [c.replace("%", "").strip() for c in r]
        out.append(r)
    return out


def cmd_ingest(args):
    snap_date = args.date or date.today().isoformat()
    dest = os.path.join(GSC_DIR, snap_date)
    if os.path.exists(dest):
        sys.exit(f"refusing to overwrite existing snapshot {dest} — pass --date for a new one")
    os.makedirs(dest)
    sources = {}
    if args.path.lower().endswith(".zip"):
        with zipfile.ZipFile(args.path) as z:
            for name in z.namelist():
                key = CSV_ALIASES.get(os.path.basename(name).lower())
                if key:
                    sources[key] = z.read(name).decode("utf-8-sig")
    elif os.path.isdir(args.path):
        for fn in os.listdir(args.path):
            key = CSV_ALIASES.get(fn.lower())
            if key:
                sources[key] = open(os.path.join(args.path, fn), encoding="utf-8-sig").read()
    else:
        sys.exit("path must be a GSC ZIP export or a directory of its CSVs")
    if not sources:
        sys.exit("no recognizable GSC CSVs found (Pages.csv, Queries.csv, ...)")
    for key, text in sources.items():
        rows = _norm_rows(text)
        with open(os.path.join(dest, key), "w", newline="") as f:
            csv.writer(f).writerows(rows)
    with open(os.path.join(dest, "meta.json"), "w") as f:
        json.dump({"snapshot_date": snap_date, "source": os.path.basename(args.path),
                   "files": sorted(sources), "ingested": date.today().isoformat(),
                   "window": "as exported (GSC default: last 3 months, cumulative)"}, f, indent=1)
    print(f"ingested {sorted(sources)} -> {dest}")
    print("next: python3 scripts/seo_engine.py report")


def snapshots():
    if not os.path.isdir(GSC_DIR):
        return []
    return sorted(d for d in os.listdir(GSC_DIR)
                  if re.match(r"\d{4}-\d{2}-\d{2}$", d)
                  and os.path.exists(os.path.join(GSC_DIR, d, "pages.csv")))


def read_pages(snap):
    """Canonical-merged page metrics: {path: {clicks, impressions, position, forms}}."""
    out = {}
    with open(os.path.join(GSC_DIR, snap, "pages.csv")) as f:
        for row in csv.DictReader(f):
            p = canon_url(row["page"])
            c, i = int(float(row["clicks"] or 0)), int(float(row["impressions"] or 0))
            pos = float(row["position"] or 0)
            e = out.setdefault(p, {"clicks": 0, "impressions": 0, "_possum": 0.0, "forms": 0})
            e["clicks"] += c
            e["impressions"] += i
            e["_possum"] += pos * max(i, 1)
            e["forms"] += 1
    for p, e in out.items():
        e["position"] = round(e["_possum"] / max(e["impressions"], e["forms"]), 2)
        e["ctr"] = e["clicks"] / e["impressions"] if e["impressions"] else 0.0
        del e["_possum"]
    return out


def read_queries(snap):
    path = os.path.join(GSC_DIR, snap, "queries.csv")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [{"query": r["query"], "clicks": int(float(r["clicks"] or 0)),
                 "impressions": int(float(r["impressions"] or 0)),
                 "position": float(r["position"] or 0)} for r in csv.DictReader(f)]


def guess_queries_for_page(path, queries):
    """GSC CSV exports don't pair queries with pages; approximate by token overlap
    between the slug and the query. Heuristic only — flagged as such in output."""
    slug_tokens = set(re.split(r"[-/]", path.strip("/"))) - {"", "guides", "es", "index", "html"}
    hits = []
    for q in queries:
        qt = set(q["query"].lower().split())
        score = len(slug_tokens & qt)
        if score >= 2 or (score == 1 and len(slug_tokens) <= 2):
            hits.append((score, q))
    hits.sort(key=lambda x: (-x[0], -x[1]["impressions"]))
    return [q for _, q in hits[:5]]


# ---------------------------------------------------------------- link graph
def site_files():
    out = []
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "gen", "docs", "reports",
                        "editorial", "scripts", "netlify", ".netlify")
                       and os.path.join(dirpath, d).replace("./", "") not in
                       ("data/gsc", "data/seo")]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, fn), ".").replace(os.sep, "/"))
    return sorted(out)


def url_of(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[:-5] if rel.endswith(".html") else "/" + rel


def file_of(path, files_set):
    p = path.strip("/")
    for cand in ([p, p + ".html", (p + "/index.html").lstrip("/")] if p else ["index.html"]):
        if cand in files_set:
            return cand
    return None


def build_graph():
    files = site_files()
    fset = set(files)
    links = defaultdict(set)   # file -> set(target files)
    inbound = defaultdict(set)
    broken = defaultdict(set)
    for rel in files:
        doc = open(rel, encoding="utf-8", errors="replace").read()
        body = re.split(r"<footer", doc)[0]          # count body+nav, not footer boilerplate
        nav_stripped = re.sub(r"<nav>.*?</nav>", "", body, flags=re.S)
        for href in set(re.findall(r"href=[\"'](/[^\"'#?]*)[\"']", nav_stripped)):
            if href.endswith((".css", ".js", ".xml", ".txt", ".png", ".jpg", ".svg",
                              ".webp", ".ico", ".pdf", ".csv")):
                continue
            tgt = file_of(href, fset)
            if tgt is None:
                broken[rel].add(href)
            elif tgt != rel:
                links[rel].add(tgt)
                inbound[tgt].add(rel)
    # crawl depth BFS from homepage over nav+body+footer (full document reachability)
    full_links = defaultdict(set)
    for rel in files:
        doc = open(rel, encoding="utf-8", errors="replace").read()
        for href in set(re.findall(r"href=[\"'](/[^\"'#?]*)[\"']", doc)):
            tgt = file_of(href, fset)
            if tgt and tgt != rel:
                full_links[rel].add(tgt)
    depth = {"index.html": 0}
    dq = deque(["index.html"])
    while dq:
        cur = dq.popleft()
        for nxt in full_links.get(cur, ()):
            if nxt not in depth:
                depth[nxt] = depth[cur] + 1
                dq.append(nxt)
    return files, links, inbound, broken, depth


def cmd_linkaudit(_args):
    files, links, inbound, broken, depth = build_graph()
    today = date.today().isoformat()
    orphans = [f for f in files if f not in depth]
    thin = sorted(((len(inbound[f]), f) for f in files
                   if len(inbound[f]) <= 1 and f not in ("thanks.html", "es/gracias.html")))
    heavy = sorted(((len(links[f]), f) for f in files), reverse=True)[:15]
    deep = sorted(((d, f) for f, d in depth.items() if d >= 4), reverse=True)
    out = {
        "date": today, "pages": len(files),
        "orphans": orphans,
        "thin_inbound": [{"file": f, "inbound_contextual": n} for n, f in thin[:40]],
        "heaviest_outbound": [{"file": f, "outbound": n} for n, f in heavy],
        "depth_ge_4": [{"file": f, "depth": d} for d, f in deep],
        "broken": {k: sorted(v) for k, v in broken.items()},
        "notes": "inbound counts exclude nav and footer boilerplate; depth uses full document links",
    }
    os.makedirs(REPORT_DIR, exist_ok=True)
    jpath = os.path.join(REPORT_DIR, f"linkaudit-{today}.json")
    json.dump(out, open(jpath, "w"), indent=1)
    lines = [f"# Internal link audit — {today}", "",
             f"Pages: {len(files)} · orphans (unreachable from home): {len(orphans)} · "
             f"broken internal hrefs: {sum(len(v) for v in broken.values())}", ""]
    if orphans:
        lines += ["## Orphans", *[f"- {f}" for f in orphans], ""]
    lines += ["## Fewest contextual inbound links (nav/footer excluded)",
              *[f"- {n:2d} ← {f}" for n, f in thin[:25]], "",
              "## Heaviest outbound pages", *[f"- {n:3d} → {f}" for n, f in heavy[:10]], ""]
    if deep:
        lines += ["## Depth ≥ 4 from homepage", *[f"- depth {d}: {f}" for d, f in deep], ""]
    if broken:
        lines += ["## Broken internal links",
                  *[f"- {k}: {', '.join(sorted(v))}" for k, v in sorted(broken.items())], ""]
    mpath = os.path.join(REPORT_DIR, f"linkaudit-{today}.md")
    open(mpath, "w").write("\n".join(lines))
    print(f"wrote {mpath} and {jpath}")
    print(f"pages={len(files)} orphans={len(orphans)} "
          f"thin(<2 contextual inbound)={len(thin)} broken={sum(len(v) for v in broken.values())}")
    return out


# ---------------------------------------------------------------- report
def tier_of(pos, impressions):
    if pos <= 5:
        return "A"
    if pos <= 15:
        return "B"
    if pos <= 30:
        return "C"
    return "D"


TIER_ACTION = {
    "A": "Defend: keep facts fresh, tighten conversion, add contextual links; no rewrites",
    "B": "Push: deepen content, satisfy every ranking query, strengthen inbound links, fix title/meta",
    "C": "Selective: improve only if impressions/intent justify; find missing subtopics",
    "D": "Observe: let it season; revisit if impressions rise",
}


def cmd_report(args):
    cfg = load_config()
    snaps = snapshots()
    if not snaps:
        sys.exit("no snapshots with pages.csv under data/gsc/ — run ingest first")
    snap = args.snapshot or snaps[-1]
    prev = args.prev or (snaps[-2] if len(snaps) > 1 and snaps[-2] != snap else None)
    pages = read_pages(snap)
    queries = read_queries(snap)
    prev_pages = read_pages(prev) if prev else {}
    w = cfg["weights"]
    min_ev = cfg["min_evidence_impressions"]

    # link-audit input if a recent one exists
    inbound_counts = {}
    audits = sorted(f for f in os.listdir(REPORT_DIR)
                    if f.startswith("linkaudit-") and f.endswith(".json")) if os.path.isdir(REPORT_DIR) else []
    if audits:
        aud = json.load(open(os.path.join(REPORT_DIR, audits[-1])))
        for e in aud.get("thin_inbound", []):
            inbound_counts[url_of(e["file"])] = e["inbound_contextual"]

    rows = []
    for path, m in pages.items():
        pos, imp = m["position"], m["impressions"]
        t = tier_of(pos, imp)
        iscore = intent_score(path)
        exp = expected_ctr(pos, cfg)
        ctr_gap = (imp >= 20 and pos <= 12 and m["ctr"] < exp * 0.5)
        pos_opp = max(0.0, 1 - abs(pos - 9) / 9) if pos <= 30 else 0.0  # peaks near 9
        cluster = any(k in path for k in cfg["priority_clusters"])
        score = (w["position_opportunity"] * pos_opp
                 + w["impressions"] * math.log10(imp + 1)
                 + w["commercial_intent"] * iscore
                 + w["ctr_gap"] * (1 if ctr_gap else 0)
                 + w["cluster_strategic"] * (1 if cluster else 0)
                 + w["link_deficit"] * (1 if inbound_counts.get(path, 99) <= 1 else 0)
                 + w["low_evidence_penalty"] * (1 if imp < min_ev else 0))
        d_imp = d_pos = None
        if path in prev_pages:
            d_imp = imp - prev_pages[path]["impressions"]
            d_pos = round(prev_pages[path]["position"] - pos, 1)  # positive = improved
        rows.append({"path": path, "tier": t, "position": pos, "impressions": imp,
                     "clicks": m["clicks"], "ctr_pct": round(m["ctr"] * 100, 2),
                     "intent": intent_label(iscore), "intent_score": iscore,
                     "ctr_gap": ctr_gap, "cluster": cluster,
                     "url_forms_seen": m["forms"],
                     "delta_impressions": d_imp, "delta_position": d_pos,
                     "opportunity": round(score, 2),
                     "top_queries_heuristic": [q["query"] for q in guess_queries_for_page(path, queries)],
                     "action": TIER_ACTION[t]})
    rows.sort(key=lambda r: -r["opportunity"])

    # cannibalization: URL-form splits + slug-sibling overlap
    split_forms = [r for r in rows if r["url_forms_seen"] > 1]
    sibs = defaultdict(list)
    for r in rows:
        toks = frozenset(re.split(r"[-/]", r["path"].strip("/"))) - {"", "es", "guides", "index"}
        for other in rows:
            if other["path"] >= r["path"]:
                continue
            otoks = frozenset(re.split(r"[-/]", other["path"].strip("/"))) - {"", "es", "guides", "index"}
            inter = toks & otoks
            if len(inter) >= 3:
                sibs[tuple(sorted(inter))].append((r["path"], other["path"]))

    # query-class rollup
    qclass = defaultdict(lambda: [0, 0.0])
    for q in queries:
        s = intent_score(q["query"])
        qclass[intent_label(s)][0] += q["impressions"]
        qclass[intent_label(s)][1] += q["position"] * q["impressions"]

    totals = {"impressions": sum(m["impressions"] for m in pages.values()),
              "clicks": sum(m["clicks"] for m in pages.values()),
              "pages_with_impressions": len(pages), "queries": len(queries)}

    today = date.today().isoformat()
    os.makedirs(REPORT_DIR, exist_ok=True)
    jout = os.path.join(REPORT_DIR, f"{snap}-opportunities.json")
    json.dump({"snapshot": snap, "prev": prev, "generated": today, "totals": totals,
               "config": cfg, "queue": rows,
               "cannibalization": {"url_form_splits": [r["path"] for r in split_forms],
                                    "slug_siblings": {" ".join(k): v for k, v in sibs.items()}},
               "query_classes": {k: {"impressions": v[0],
                                      "avg_position": round(v[1] / v[0], 1) if v[0] else None}
                                 for k, v in qclass.items()}},
              open(jout, "w"), indent=1)

    L = [f"# SEO opportunity report — snapshot {snap}", "",
         f"Generated {today}. Window: cumulative last-3-months as exported. "
         f"Prev snapshot for deltas: {prev or 'none (first full snapshot)'}.", "",
         "## Dashboard",
         f"- Impressions {totals['impressions']} · clicks {totals['clicks']} · "
         f"CTR {100*totals['clicks']/max(totals['impressions'],1):.2f}% · "
         f"pages appearing {totals['pages_with_impressions']} · queries {totals['queries']}",
         "- Query-class mix: " + " · ".join(
             f"{k}: {v[0]} imp @ {v[1]/v[0]:.0f}" for k, v in sorted(qclass.items(), key=lambda x: -x[1][0]) if v[0]),
         ""]
    tiers = defaultdict(int)
    for r in rows:
        tiers[r["tier"]] += 1
    L += [f"- Tiers: " + " · ".join(f"{t}: {tiers[t]}" for t in "ABCD"), ""]
    L += ["## Top 20 opportunity queue", "",
          "| # | Path | Tier | Pos | Impr | CTR% | Intent | Flags | Score |",
          "|---|------|------|-----|------|------|--------|-------|-------|"]
    for i, r in enumerate(rows[:20], 1):
        flags = []
        if r["ctr_gap"]:
            flags.append("CTR-gap")
        if r["url_forms_seen"] > 1:
            flags.append("url-split")
        if r["cluster"]:
            flags.append("cluster")
        L.append(f"| {i} | {r['path']} | {r['tier']} | {r['position']} | {r['impressions']} | "
                 f"{r['ctr_pct']} | {r['intent']} | {', '.join(flags) or '—'} | {r['opportunity']} |")
    L += ["", "## CTR-gap flags (impressions ≥20, pos ≤12, CTR under half expected)"]
    ctrf = [r for r in rows if r["ctr_gap"]]
    L += [f"- {r['path']} — pos {r['position']}, {r['impressions']} imp, {r['ctr_pct']}% CTR"
          for r in ctrf] or ["- none"]
    L += ["", "## URL-form splits still visible in GSC (canonical consolidation in progress)"]
    L += [f"- {r['path']} ({r['url_forms_seen']} forms)" for r in split_forms] or ["- none"]
    if sibs:
        L += ["", "## Possible cannibalization (slug-token siblings — review, most are legitimate hubs/spokes)"]
        for k, v in list(sibs.items())[:10]:
            L += [f"- tokens `{' '.join(k)}`: " + "; ".join(f"{a} ↔ {b}" for a, b in v[:3])]
    L += ["", "## Tier actions", *[f"- **{t}** ({tiers[t]}): {TIER_ACTION[t]}" for t in "ABCD"], "",
          f"Full machine-readable queue: `{jout}`", ""]
    mout = os.path.join(REPORT_DIR, f"{snap}-opportunities.md")
    open(mout, "w").write("\n".join(L))
    print(f"wrote {mout}")
    print(f"wrote {jout}")
    for r in rows[:8]:
        print(f"  {r['opportunity']:5.2f}  {r['tier']}  pos {r['position']:<6} "
              f"imp {r['impressions']:<4} {r['path']}")


# ---------------------------------------------------------------- event log
def cmd_log_event(args):
    snaps = snapshots()
    before = {}
    if snaps:
        pages = read_pages(snaps[-1])
        before = pages.get(canon_url(args.url), {})
    os.makedirs(SEO_DIR, exist_ok=True)
    evt = {"date": date.today().isoformat(), "url": canon_url(args.url),
           "reason": args.reason, "change": args.change,
           "kinds": (args.kinds or "").split(",") if args.kinds else [],
           "gsc_snapshot": snaps[-1] if snaps else None,
           "before": {k: before.get(k) for k in ("clicks", "impressions", "position", "ctr")},
           "after_checkpoints": {"7d": None, "28d": None, "90d": None}}
    with open(EVENTS_PATH, "a") as f:
        f.write(json.dumps(evt) + "\n")
    print(f"logged: {evt['url']} — {args.reason}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("ingest")
    p.add_argument("path")
    p.add_argument("--date")
    p.set_defaults(fn=cmd_ingest)
    p = sub.add_parser("report")
    p.add_argument("--snapshot")
    p.add_argument("--prev")
    p.set_defaults(fn=cmd_report)
    p = sub.add_parser("linkaudit")
    p.set_defaults(fn=cmd_linkaudit)
    p = sub.add_parser("log-event")
    p.add_argument("--url", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--change", required=True)
    p.add_argument("--kinds")
    p.set_defaults(fn=cmd_log_event)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
