#!/usr/bin/env python3
"""Standardize header nav + footer directory across every page, and create the
two missing section hubs (Schools, Data). Goal: make every section reachable
from every page so nothing is hidden."""
import re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ---- canonical NAV inner (between <nav> and </nav>) ----
NAV_EN = ("<a href='/specials'>Specials</a>"
          "<a href='/deals'>Best Deals</a>"
          "<a href='/neighborhoods/'>Neighborhoods</a>"
          "<a href='/schools/'>Schools</a>"
          "<a href='/buy/'>Buying</a>"
          "<a href='/relocate/'>Relocate</a>"
          "<a href='/guides/'>Guides</a>"
          "<a href='/tools/'>Tools</a>"
          "<a href='/es/' style='font-weight:600'>Español</a>")

NAV_ES = ("<a href='/es/'>Inicio</a>"
          "<a href='/es/comprar/'>Comprar</a>"
          "<a href='/es/especiales'>Especiales</a>"
          "<a href='/es/segunda-oportunidad'>Segunda Oportunidad</a>"
          "<a href='/es/relocate/'>Mudanza</a>"
          "<a href='/es/calculadora'>Calculadora</a>"
          "<a href='/' style='font-weight:600'>English</a>")

# ---- canonical FOOTER directory (replaces the .fgrid block, keeps disclaimers) ----
FGRID_EN = """<div class="fgrid">
    <div><h4>West FW Living</h4><p>An independent field guide to renting and buying on Fort Worth's west side — Aledo, Willow Park, Hudson Oaks, Walsh, Benbrook and the Chisholm Trail corridor. Full service is coming soon; <a href='/#list'>the early list hears first</a>.</p></div>
    <div><h4>Renting</h4><ul><li><a href='/specials'>This Month's Specials</a></li><li><a href='/deals'>Best Deals, Ranked</a></li><li><a href='/rentals/'>Browse by Feature</a></li><li><a href='/second-chance'>Second Chance Renting</a></li><li><a href='/rent-to-own'>Rent-to-Own Reality</a></li><li><a href='/areas'>Areas We Cover</a></li></ul></div>
    <div><h4>Explore West FW</h4><ul><li><a href='/neighborhoods/'>Neighborhoods</a></li><li><a href='/schools/'>Schools &amp; ISDs</a></li><li><a href='/compare/'>Compare Places</a></li><li><a href='/relocate/'>Relocating Here</a></li><li><a href='/move/'>Move Checklist</a></li><li><a href='/community/'>Community &amp; Local Life</a></li><li><a href='/military/'>Military &amp; BAH</a></li><li><a href='/guides/'>All Guides</a></li></ul></div>
    <div><h4>Buying</h4><ul><li><a href='/buy/'>Buy the West Side</a></li><li><a href='/calculator'>Rent vs. Buy Math</a></li><li><a href='/quiz'>Rent-or-Buy Quiz</a></li><li><a href='/es/'>En Español</a></li></ul></div>
    <div><h4>Data &amp; Tools</h4><ul><li><a href='/tools/'>Renter Tools</a></li><li><a href='/data/'>Rent Data &amp; Reports</a></li><li><a href='/rent-report/august-2026'>Latest Rent Report</a></li><li><a href='/resources/'>Resources</a></li></ul></div>
  </div>"""

FGRID_ES = """<div class="fgrid">
    <div><h4>West FW Living</h4><p>Una guía independiente para rentar y comprar en el oeste de Fort Worth. El servicio completo llega pronto; <a href='/es/#lista'>la lista se entera primero</a>.</p></div>
    <div><h4>Rentar</h4><ul><li><a href='/es/especiales'>Especiales del Mes</a></li><li><a href='/deals'>Mejores Ofertas</a></li><li><a href='/es/segunda-oportunidad'>Segunda Oportunidad</a></li><li><a href='/es/semanas-gratis'>Semanas Gratis</a></li><li><a href='/es/romper-contrato'>Romper el Contrato</a></li></ul></div>
    <div><h4>Comprar</h4><ul><li><a href='/es/comprar/'>Comprar Casa</a></li><li><a href='/es/comprar/renta-o-compra'>Renta o Compra</a></li><li><a href='/es/comprar/primera-vivienda-texas'>Primera Vivienda</a></li><li><a href='/es/comprar/asistencia-enganche'>Ayuda con el Enganche</a></li></ul></div>
    <div><h4>Recursos</h4><ul><li><a href='/es/calculadora'>Calculadora</a></li><li><a href='/es/puntaje-credito'>Puntaje de Crédito</a></li><li><a href='/es/relocate/'>Mudanza</a></li><li><a href='/es/comunidad/'>Comunidad</a></li><li><a href='/'>English site</a></li></ul></div>
  </div>"""

def replace_nav(html, es):
    inner = NAV_ES if es else NAV_EN
    return re.sub(r'<nav>.*?</nav>', lambda m: '<nav>' + inner + '</nav>',
                  html, count=1, flags=re.S)

def replace_fgrid(html, es):
    block = FGRID_ES if es else FGRID_EN
    start = html.find('<div class="fgrid">')
    if start == -1:
        return html
    disc = html.find('<p class="disclaim"', start)
    if disc == -1:
        return html
    # last </div> before the disclaimer closes the fgrid block
    close = html.rfind('</div>', start, disc)
    if close == -1:
        return html
    close_end = close + len('</div>')
    return html[:start] + block + html[close_end:]

def process(path):
    es = path == 'es' or path.startswith('es/') or path.startswith('es\\')
    html = open(path, encoding='utf-8').read()
    html = replace_nav(html, es)
    html = replace_fgrid(html, es)
    open(path, 'w', encoding='utf-8').write(html)

# ---------- build the two missing hubs ----------
def page(title, desc, crumb, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="max-image-preview:large">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,600&family=Instrument+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<header><div class="wrap"><div class="topbar">
  <a class='brand' href='/'>West FW <span>Living</span><small>the west side field guide</small></a>
  <nav>{NAV_EN}</nav>
</div></div></header>
<main><div class="wrap">
<p class="crumb"><a href='/'>Home</a> / {crumb}</p>
{body}
</div></main>
<footer><div class="wrap">
  {FGRID_EN}
  <p class="disclaim">West FW Living is not a real estate brokerage and does not currently offer brokerage, leasing, or apartment-locating services. All rent figures, specials, and program details are compiled from public listings and sources, change without notice, and should be verified directly with the property or program. Payment estimates are educational only — not a loan offer, prequalification, or lending advice. Equal Housing Opportunity.</p>
</div></footer>
</body>
</html>
"""

def card(href, title, note):
    return f"<div class='card'><h3><a href='{href}'>{title}</a></h3><p>{note}</p></div>"

schools_body = """<section class="hero hero-inner"><span class="eyebrow">EVERY DISTRICT, EVERY CAMPUS — THE MOVER'S SCHOOL LIBRARY</span>
<h1>Schools of the west side</h1><p class="lede">The district decision comes before the house decision out here. Start with a district hub, then drill into the individual campus files — zoning, feeder path, and an honest read for families moving in.</p></section>
<section><h2>Districts</h2><div class="grid cols2">""" + \
card('/schools/aledo-isd/', 'Aledo ISD', "The corridor's marquee district — every campus explained for movers.") + \
card('/schools/weatherford-isd/', 'Weatherford ISD', "Every campus, addresses, and the mover's read across the county seat.") + \
card('/schools/brock-isd/', 'Brock ISD', "The small-district ladder and the land-buyer's read.") + \
"""</div></section>
<section><h2>Aledo ISD campuses</h2><div class="grid cols2">""" + \
card('/schools/aledo-isd/aledo-high-school', 'Aledo High School', "Zoning, feeder path & the mover's briefing.") + \
card('/schools/aledo-isd/daniel-ninth-grade-campus', 'Daniel Ninth Grade Campus', 'The 9th-grade transition campus.') + \
card('/schools/aledo-isd/aledo-middle-school', 'Aledo Middle School', 'Zoning & feeder path.') + \
card('/schools/aledo-isd/mcanally-middle-school', 'McAnally Middle School', 'Zoning & feeder path.') + \
card('/schools/aledo-isd/mccall-elementary', 'McCall Elementary', 'The Willow Park–side campus.') + \
card('/schools/aledo-isd/walsh-elementary', 'Walsh Elementary', 'The Walsh community campus.') + \
card('/schools/aledo-isd/coder-elementary', 'Coder Elementary', 'Zoning & feeder path.') + \
card('/schools/aledo-isd/vandagriff-elementary', 'Vandagriff Elementary', 'The in-town campus.') + \
card('/schools/aledo-isd/annetta-elementary', 'Annetta Elementary', 'The Annetta-side campus.') + \
card('/schools/aledo-isd/stuard-elementary', 'Stuard Elementary', 'The Annetta-side campus.') + \
card('/schools/aledo-isd/lynn-mckinney-elementary', 'Lynn McKinney Elementary', 'Zoning & feeder path.') + \
"""</div></section>
<section><h2>For renters &amp; private options</h2><div class="grid cols2">""" + \
card('/schools/willow-park-school-zones', 'Willow Park school zones', 'Aledo ISD zones decoded for renters — how to verify before you sign.') + \
card('/schools/private-schools-west-fort-worth', 'Private schools shortlist', "All Saints', FWCD, Trinity Valley & more — with real tuition.") + \
"""</div></section>"""

data_body = """<section class="hero hero-inner"><span class="eyebrow">THE NUMBERS BEHIND THE WEST SIDE</span>
<h1>Rent data &amp; reports</h1><p class="lede">The receipts: net-effective rents, fee transparency, utility and internet costs, taxes, the construction pipeline, and how long specials really last — the data layer under every recommendation on this site.</p></section>
<section><div class="grid cols2">""" + \
card('/data/true-rent-table', 'The True Rent Table', 'Net-effective rents for every community we track.') + \
card('/data/fee-index', 'The Fee Transparency Index', 'App, admin, pet & deposit fees, community by community.') + \
card('/data/specials-longevity', 'The Specials Half-Life Tracker', 'How long move-in specials actually last.') + \
card('/data/utilities', 'Utility Cost Reality', 'What electric & water billing really add to rent.') + \
card('/data/internet', 'Internet Options', 'Fiber, cable & 5G across the west FW corridor.') + \
card('/data/property-tax', 'Property Tax Rates', 'Willow Park vs. Weatherford vs. Aledo vs. Fort Worth.') + \
card('/data/pipeline', 'The Construction Pipeline', 'New apartments coming to the corridor.') + \
"""</div></section>
<section><h2>Monthly report</h2><div class="grid cols2">""" + \
card('/rent-report/august-2026', 'Latest Rent Report', 'The current monthly roundup of specials and moves.') + \
"""</div></section>"""

os.makedirs('schools', exist_ok=True)
open('schools/index.html', 'w', encoding='utf-8').write(page(
    "West Fort Worth Schools — Every District &amp; Campus for Movers",
    "The west side school library: Aledo ISD, Weatherford ISD and Brock ISD hubs, every Aledo campus file, plus renter school zones and private-school options.",
    "Schools", schools_body))
open('data/index.html', 'w', encoding='utf-8').write(page(
    "West Fort Worth Rent Data &amp; Reports — The Numbers",
    "The data behind west Fort Worth rents: the True Rent Table, fee index, utility and internet costs, property taxes, the construction pipeline, and the specials tracker.",
    "Data", data_body))

# ---------- standardize every page ----------
count = 0
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith(('node_modules/', 'assets/')):
        continue
    process(f)
    count += 1
print(f"standardized {count} pages; created schools/index.html + data/index.html")
