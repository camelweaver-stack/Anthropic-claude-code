#!/usr/bin/env python3
"""Refresh the BAH Reality Report to a new edition (built now; run when DTMO drops new rates).

Single source of truth: data/source/bah_report_source.json. This script edits that ONE file,
rebuilds + gates, and prints an old->new diff for a human eyeball before deploy. It does NOT
deploy — run the standard Netlify pipeline after the diff looks right (see step 7 in
bah-refresh-december-runbook.md), then request GSC indexing for /bah-report/ and /data/.

Usage:
  python3 scripts/refresh-bah-edition.py --input new_rates.json
  python3 scripts/refresh-bah-edition.py            # interactive prompts

new_rates.json (all keys optional except bah_anchors + bah_effective_iso):
  {
    "edition": "2026.12", "edition_label": "December 2026",
    "bah_effective_iso": "2027-01-01", "bah_effective_label": "January 1, 2027",
    "yoy_change_label": "about 3.1%",
    "bah_anchors": {"e5_dep": 3777, "e5_solo": 2945, "e6_dep": 4033,
                    "e6_solo": 3130, "floor": 2679, "ceiling": 5196}
    // rent_bands / medians carry forward unless supplied (December is a BAH refresh)
  }
Idempotent-ish: re-running with the same input reproduces the same source file + build.
"""
import json, os, sys, subprocess, argparse, datetime, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "source", "bah_report_source.json")
GEN = os.path.join(ROOT, "gen")
SITE = os.path.join(ROOT, "site")
ANCHORS = ["e5_dep", "e5_solo", "e6_dep", "e6_solo", "floor", "ceiling"]

def die(msg): print("ABORT:", msg); sys.exit(1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="JSON file with new edition figures")
    ap.add_argument("--yes", action="store_true", help="skip the confirm prompt")
    args = ap.parse_args()

    old = json.load(open(SRC))
    new_in = json.load(open(args.input)) if args.input else prompt_interactive(old)

    # ---- 1. Archive the OUTGOING edition's data files (citations never break) ----
    adir = os.path.join(SITE, "data", "archive")
    os.makedirs(adir, exist_ok=True)
    ed = old["edition"].replace(".", "-")
    for ext in ("json", "csv"):
        cur = os.path.join(SITE, "data", f"bah-reality-report.{ext}")
        if os.path.exists(cur):
            shutil.copy(cur, os.path.join(adir, f"bah-reality-report-{ed}.{ext}"))
    print(f"[1] archived outgoing edition {old['edition']} -> data/archive/bah-reality-report-{ed}.*")

    # ---- 2/3. Merge new figures, bump edition, stamp refresh date ----
    src = dict(old)
    anchors = dict(old["bah_anchors"]); anchors.update(new_in.get("bah_anchors", {}))
    for k in ANCHORS:
        if k not in anchors: die(f"missing anchor '{k}'")
    # sanity gate: new effective date must be later; anchors within +/-15% of prior (typo guard)
    eff_new = new_in.get("bah_effective_iso", old["bah_effective_iso"])
    if eff_new <= old["bah_effective_iso"]:
        die(f"new bah_effective_iso {eff_new} not later than current {old['bah_effective_iso']}")
    for k in ANCHORS:
        o, n = old["bah_anchors"][k], anchors[k]
        if not (0.85 * o <= n <= 1.15 * o):
            die(f"anchor {k}: {n} is outside +/-15% of prior {o} — confirm this is real, not a typo")
    src["bah_anchors"] = anchors
    src["bah_effective_iso"] = eff_new
    src["bah_effective_label"] = new_in.get("bah_effective_label", old["bah_effective_label"])
    src["bah_year"] = eff_new[:4]
    src["edition"] = new_in.get("edition", bump_edition(old["edition"]))
    src["edition_label"] = new_in.get("edition_label", old["edition_label"])
    src["yoy_change_label"] = new_in.get("yoy_change_label", old["yoy_change_label"])
    src["date_refreshed_iso"] = datetime.date.today().isoformat()
    src["date_refreshed_label"] = datetime.date.today().strftime("%B %-d, %Y")
    # rent bands + medians carry forward unless explicitly supplied
    for k in ("rent_bands", "pockets", "median_single_family", "median_condo"):
        if k in new_in: src[k] = new_in[k]

    print(f"[2/3] new edition {src['edition']} ({src['edition_label']}), effective {src['bah_effective_iso']}, "
          f"refreshed {src['date_refreshed_iso']}")
    diff(old, src)
    if not args.yes and input("\nWrite this to the source file and rebuild? [y/N] ").strip().lower() != "y":
        die("no changes written")

    json.dump(src, open(SRC, "w"), indent=2)

    # ---- 4/5. Rebuild through the pipeline (build regenerates sitemap fresh) ----
    print("[4] rebuilding…")
    r = subprocess.run([sys.executable, "build.py"], cwd=GEN, capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode: die("build failed")
    print("[5] gate…")
    g = subprocess.run([sys.executable, "gate.py", SITE], cwd=GEN, capture_output=True, text=True)
    print(g.stdout.strip() or g.stderr.strip())
    if g.returncode: die("GATE FAILED — do not deploy; fix and re-run")

    # ---- 6/7. Human eyeball, then deploy manually ----
    print("\n[6] DONE. Eyeball the diff above.")
    print("[7] Deploy via the standard Netlify pipeline, verify the §9 battery, then request GSC "
          "indexing for /bah-report/ and /data/. Fire the R1 list email (runbook) the same day.")

def bump_edition(ed):
    y, m = ed.split("."); return f"{y}.12" if m != "12" else f"{int(y)+1}.08"

def diff(old, new):
    print("\n--- anchor diff (old -> new) ---")
    for k in ANCHORS:
        o, n = old["bah_anchors"][k], new["bah_anchors"][k]
        pct = (n - o) / o * 100
        print(f"  {k:9} {o:>6,} -> {n:>6,}  ({pct:+.1f}%)")

def prompt_interactive(old):
    print("Enter new BAH anchors (blank = carry forward):")
    a = {}
    for k in ANCHORS:
        v = input(f"  {k} [{old['bah_anchors'][k]}]: ").strip()
        if v: a[k] = int(v.replace(",", "").replace("$", ""))
    return {"bah_anchors": a,
            "bah_effective_iso": input(f"  bah_effective_iso [{old['bah_effective_iso']}]: ").strip() or old["bah_effective_iso"],
            "bah_effective_label": input("  bah_effective_label (e.g. 'January 1, 2027'): ").strip() or old["bah_effective_label"],
            "yoy_change_label": input("  yoy_change_label (e.g. 'about 3.1%'): ").strip() or old["yoy_change_label"]}

if __name__ == "__main__":
    main()
