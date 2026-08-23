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
import pages_guides_benbrook  # noqa: E402
import pages_buy_homestead  # noqa: E402
import pages_sell_net_proceeds  # noqa: E402

MODULES = [pages_schools_ratings, pages_guides_benbrook, pages_buy_homestead, pages_sell_net_proceeds]

# Reciprocal links: (hub file, anchor that must exist, HTML block, insertion marker).
# Each entry is applied only when the anchor is absent, so the build is idempotent.
RECIPROCAL = [
    (
        "sell/index.html",
        "/sell/net-proceeds",
        "<a href='/sell/net-proceeds'><h3>The net-proceeds napkin</h3>"
        "<p>What selling actually costs, worked at $450K: the state-set title premium, the $0 "
        "transfer tax, and the blanks only your documents can fill.</p></a> ",
        "<a href='/sell/capital-gains'><h3>",
    ),
    (
        "es/vender/index.html",
        "/es/vender/ganancias-netas",
        "<a href='/es/vender/ganancias-netas'><h3>Las cuentas netas del cierre</h3>"
        "<p>Lo que vender cuesta de verdad, a $450K: la prima de t\u00edtulo fijada por el estado, "
        "el impuesto de transferencia de $0, y los espacios que llenan sus documentos.</p></a> ",
        "<a href='/es/vender/impuestos-ganancias'><h3>",
    ),
    (
        "sell/capital-gains.html",
        "/sell/net-proceeds",
        "<section><div class=\"prose\"><p>Taxes on the gain are only half the ledger \u2014 "
        "<a href=\"/sell/net-proceeds\">the net-proceeds napkin</a> works the other half: title "
        "premium, prorations, and the negotiated blanks, line by line.</p></div></section>\n"
        "<div class=\"leadbox\"><h2>Get your area's sale data</h2>",
        "<div class=\"leadbox\"><h2>Get your area's sale data</h2>",
    ),
    (
        "buy/index.html",
        "/buy/homestead-exemption",
        "<div class=\"card\"><h3><a href=\"/buy/homestead-exemption\">The homestead exemption, in dollars</a></h3>"
        "<p>What the $140K exemption is actually worth in each corridor district at adopted 2025 "
        "rates \u2014 and the 10% cap it switches on.</p></div>",
        "<div class=\"card\"><h3><a href=\"/buy/property-taxes-for-buyers\">",
    ),
    (
        "es/comprar/index.html",
        "/es/comprar/exencion-homestead",
        "<div class=\"card\"><h3><a href=\"/es/comprar/exencion-homestead\">La exenci\u00f3n homestead, en d\u00f3lares</a></h3>"
        "<p>Cu\u00e1nto vale la exenci\u00f3n de $140K en cada distrito del corredor con las tasas "
        "adoptadas de 2025.</p></div>",
        "<div class=\"card\"><h3><a href=\"/es/comprar/renta-o-compra",
    ),
    (
        "buy/property-taxes-for-buyers.html",
        "/buy/homestead-exemption",
        "<a href=\"/buy/homestead-exemption\">the exemption in dollars, district by district</a> \u00b7 ",
        "<a href=\"/buy/\">the buyer's guide</a>",
    ),
    (
        "guides/index.html",
        "/guides/living-in-benbrook",
        "<div class=\"card\"><span class=\"kicker\">Definitive Guide &middot; Benbrook</span>"
        "<h3><a href='/guides/living-in-benbrook'>Living in Benbrook: the value play, by the numbers</a></h3>"
        "<p>The published $200K gap to Aledo, an A-rated middle/high inside a C-rated district, "
        "and who the trade actually fits.</p></div>",
        "<div class=\"card\"><span class=\"kicker\">Pillar \u00b7 Family Relocation</span>",
    ),
    (
        "es/guias/index.html",
        "/es/guias/vivir-en-benbrook",
        "<div class=\"card\"><span class=\"kicker\">Gu\u00eda Definitiva \u00b7 Benbrook</span>"
        "<h3><a href='/es/guias/vivir-en-benbrook'>Vivir en Benbrook: la jugada de valor</a></h3>"
        "<p>La brecha publicada de $200K con Aledo, una secundaria con A dentro de un distrito con C, "
        "y a qui\u00e9n le conviene.</p></div>",
        "<div class=\"card\"><span class=\"kicker\">Gu\u00eda Definitiva \u00b7 Aledo</span>",
    ),
    (
        "areas/benbrook.html",
        "/guides/living-in-benbrook",
        "<a href=\"/guides/living-in-benbrook\">the definitive Benbrook guide</a> \u00b7 ",
        "<a href=\"/neighborhoods/\">the neighborhood library</a>",
    ),
    (
        "schools/index.html",
        "/schools/tea-ratings-2026",
        "<section><h2>This year's ratings</h2><div class=\"grid cols2\">"
        "<div class='card'><h3><a href='/schools/tea-ratings-2026'>2026 TEA ratings, corridor-wide</a></h3>"
        "<p>Every west-side district and campus in TEA's August 2026 release &mdash; and the three "
        "limits that keep a letter grade from being a housing decision.</p></div></div></section>\n",
        "<section><h2>Districts</h2>",
    ),
    (
        "es/escuelas/index.html",
        "/es/escuelas/calificaciones-tea-2026",
        "<section><h2>Las calificaciones de este a&ntilde;o</h2><div class=\"grid cols2\">"
        "<div class='card'><h3><a href='/es/escuelas/calificaciones-tea-2026'>Calificaciones TEA 2026</a></h3>"
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
