#!/usr/bin/env python3
"""West FW Living — generator build.

Renders every module's pages into the repository tree (WFL publishes the repo
root) and wires idempotent reciprocal links into the hand-authored hubs, so a
new spoke is always reachable from its hub.

Run from the repo root or from gen/:  python3 gen/build.py
Then ALWAYS run the final step:       python3 scripts/apply_standing_fixes.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pages_schools_ratings  # noqa: E402

MODULES = [pages_schools_ratings]

# Reciprocal links: (hub file, anchor that must exist, HTML block, insertion marker).
# Each entry is applied only when the anchor is absent, so the build is idempotent.
RECIPROCAL = [
    (
        "schools/index.html",
        "/schools/tea-ratings-2026",
        "<section><h2>This year's ratings</h2><div class=\"grid cols2\">"
        "<div class='card'><h3><a href='/schools/tea-ratings-2026.html'>2026 TEA ratings, corridor-wide</a></h3>"
        "<p>Every west-side district and campus in TEA's August 2026 release &mdash; and the three "
        "limits that keep a letter grade from being a housing decision.</p></div></div></section>\n",
        "<section><h2>Districts</h2>",
    ),
    (
        "es/escuelas/index.html",
        "/es/escuelas/calificaciones-tea-2026",
        "<section><h2>Las calificaciones de este a&ntilde;o</h2><div class=\"grid cols2\">"
        "<div class='card'><h3><a href='/es/escuelas/calificaciones-tea-2026.html'>Calificaciones TEA 2026</a></h3>"
        "<p>Cada distrito y plantel del lado oeste en la publicaci&oacute;n de agosto de 2026 de la TEA.</p>"
        "</div></div></section>\n",
        "<section><h2>Distritos</h2>",
    ),
]


def write(path, html):
    """Write a site-absolute path (e.g. /schools/x.html) into the repo tree."""
    dest = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    prior = None
    if os.path.exists(dest):
        with open(dest, encoding="utf-8") as fh:
            prior = fh.read()
    if prior == html:
        return "unchanged"
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(html)
    return "written" if prior is None else "updated"


def apply_reciprocal():
    out = []
    for rel, anchor, block, marker in RECIPROCAL:
        fp = os.path.join(ROOT, rel)
        if not os.path.exists(fp):
            out.append(f"  SKIP {rel} (missing)")
            continue
        with open(fp, encoding="utf-8") as fh:
            doc = fh.read()
        if anchor in doc:
            out.append(f"  ok   {rel} (reciprocal link already present)")
            continue
        if marker not in doc:
            out.append(f"  WARN {rel}: insertion marker not found — no reciprocal link added")
            continue
        doc = doc.replace(marker, block + marker, 1)
        with open(fp, "w", encoding="utf-8") as fh:
            fh.write(doc)
        out.append(f"  +    {rel} (reciprocal link added)")
    return out


def main():
    total = 0
    print("Building West FW Living pages…")
    for mod in MODULES:
        for path, html in mod.build().items():
            status = write(path, html)
            print(f"  {status:9} {path}")
            total += 1
    print("Reciprocal hub links:")
    for line in apply_reciprocal():
        print(line)
    print(f"\nBuild complete — {total} generated page(s).")
    print("NEXT (required): python3 scripts/apply_standing_fixes.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
