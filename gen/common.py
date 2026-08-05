# PCS Oahu — shared build framework
import json, html, os
_mfp = os.path.join(os.path.dirname(__file__), "img_manifest.json")
IMG = json.load(open(_mfp)) if os.path.exists(_mfp) else {}
_CREDITS = "; ".join(
    v["title"].replace("File:", "").rsplit(".", 1)[0][:48] + " — " + v["artist"] +
    " (" + v["license"] + ")" for v in IMG.values())

DOMAIN = "https://pcsoahu.com"
BUILD_DATE = "August 2026"
BAH_YEAR = "2026"
LAST_REFRESHED = "August 1, 2026"
SMS_NUMBER = ""  # set to E.164 (e.g. +18085551234) and rebuild to enable SMS join buttons

def sms_button(label="Text to join the list"):
    if not SMS_NUMBER: return ""
    return (f'<a class="btn ghost" href="sms:{SMS_NUMBER}?&body=Add%20me%20to%20the%20PCS%20Oahu%20'
            f'list!%20Report%20window%3A%20___%20Base%3A%20___">{label}</a>')

# ---- verified data anchors (all figures hedged + dated in copy) ----
BAH = {
    "effective": "January 1, 2026",
    "mha": "Honolulu County, HI (one Military Housing Area covers every Oahu installation)",
    "e5_dep": "$3,663", "e5_solo": "$2,856",
    "e6_dep": "$3,912", "e6_solo": "$3,036",
    "floor": "$2,598", "ceiling": "$5,040",
    "increase": "about 4.4%",
}
MED_SF = "$1,275,000"   # Oahu median single-family, June 2026
MED_CONDO = "$530,000"  # Oahu median condo, June 2026

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800'
         '&family=IBM+Plex+Mono:wght@400;600&family=Source+Sans+3:wght@400;600;700'
         '&display=swap" rel="stylesheet">')

NAV_LINKS = [
    ("/bases/", "Bases"),
    ("/bah-report/", "BAH Report"),
    ("/neighborhoods/", "Neighborhoods"),
    ("/schools/", "Schools"),
    ("/buy/", "Buying"),
    ("/sell/", "Selling"),
    ("/pcs-checklist/", "PCS Checklist"),
    ("/tla/", "TLA & Arrival"),
    ("/guides/", "Guides"),
    ("/tools/", "Tools"),
]

def nav(current=""):
    items = []
    for href, label in NAV_LINKS:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return ('<header class="site"><div class="wrap">'
            '<a class="brand" href="/"><b>PCS Oahu</b>'
            '<span>the orders-to-island field guide</span></a></div></header>'
            '<nav class="main" aria-label="Primary"><ul>' + "".join(items) + "</ul></nav>")

def rates(rows, src):
    """Signature LES-style rate lines. rows = [(label, value, hi?)]"""
    out = ['<div class="rates">']
    for r in rows:
        label, val = r[0], r[1]
        hi = ' hi' if len(r) > 2 and r[2] else ''
        out.append(f'<div class="row"><span class="k">{label}</span>'
                   f'<span class="dots"></span><span class="v{hi}">{val}</span></div>')
    out.append(f'<span class="src">{src} <strong>Last refreshed: ' + LAST_REFRESHED + '</strong></span></div>')
    return "".join(out)

def lead_form(tag, segment, context="move", heading="Get the arrival brief", blurb=None):
    """FormSubmit lead form. context: 'move' -> move_date optional, 'sell' -> sell_timeline optional."""
    if context == "sell":
        ctx = ('<label for="sell_timeline">When are you thinking of selling? '
               '<span class="opt">(optional)</span></label>'
               '<input id="sell_timeline" name="sell_timeline" type="text" '
               'placeholder="e.g., next PCS window, summer 2027">')
    else:
        ctx = ('<label for="move_date">When are you planning to move? '
               '<span class="opt">(optional)</span></label>'
               '<input id="move_date" name="move_date" type="text" '
               'placeholder="e.g., report NLT June 2027">')
    blurb = blurb or ("One useful email when the numbers change — BAH cycle updates, rent-band "
                      "refreshes, and first word when full service opens. No spam. Leave anytime.")
    return f'''
<section id="list"><h2>{heading}</h2><p style="max-width:44rem">{blurb}</p>
<form class="lead" action="https://formsubmit.co/leads@anastasiaweaver.com" method="POST">
  <input type="hidden" name="_subject" value="PCSOAHU-{tag}">
  <input type="hidden" name="audience" value="referral-hi-oahu-pcs">
  <input type="hidden" name="segment" value="{segment}">
  <label for="name">Name</label>
  <input id="name" name="name" type="text" autocomplete="name">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required autocomplete="email">
  <label for="phone">Phone</label>
  <input id="phone" name="phone" type="tel" required autocomplete="tel">
  {ctx}
  <button class="btn" type="submit">Join the list</button> {sms_button()}
  <p class="fine">Two required fields plus your phone. We never sell your info.</p>
</form></section>'''

FOOTER = f'''
<footer class="site"><div class="wrap">
  <div class="footgrid">
    <div><h4>PCS Oahu</h4>
      <p style="max-width:22rem">An independent field guide for service members and families on
      orders to — and from — Oahu. Educational content and honest math only. Full service coming soon.</p></div>
    <div><h4>Arriving</h4><ul>
      <li><a href="/bases/">Base-by-base guides</a></li>
      <li><a href="/bah-report/">The BAH Reality Report</a></li>
      <li><a href="/tla/">TLA &amp; interim housing</a></li>
      <li><a href="/tla/field-notes.html">TLA lodging field notes</a></li>
      <li><a href="/vehicle-shipping/">Vehicle shipping</a></li>
      <li><a href="/pcs-checklist/">PCS timeline checklist</a></li>
      <li><a href="/neighborhoods/">Neighborhoods</a></li>
      <li><a href="/quiz/">Pocket-match quiz</a></li>
      <li><a href="/on-base/">On-base housing</a></li>
      <li><a href="/schools/">Schools</a></li></ul></div>
    <div><h4>Buying &amp; Selling</h4><ul>
      <li><a href="/buy/">VA loans on Oahu</a></li>
      <li><a href="/sell/">PCSing out: sell or rent</a></li>
      <li><a href="/tools/">Calculators</a></li></ul></div>
    <div><h4>Life on Island</h4><ul>
      <li><a href="/guides/spouse-employment.html">Spouse employment</a></li>
      <li><a href="/guides/school-transition.html">School transitions</a></li>
      <li><a href="/guides/">All guides</a></li>
      <li><a href="/my-pcs/">My PCS dashboard</a></li>
      <li><a href="/ask/">Ask PCS Oahu</a></li>
      <li><a href="/data/">Data desk</a></li></ul></div>
  </div>
  <div class="legal">
    <p><strong>Photo credits</strong> (Wikimedia Commons, used under the stated licenses with
    thanks): {_CREDITS}. Imagery is illustrative of the areas discussed; source links in the
    build manifest.</p>
    <p>PCS Oahu is not a real estate brokerage and does not currently offer brokerage, leasing, or
    relocation services. All BAH figures, rents, prices, and program details are compiled from public
    sources — DoD/DTMO tables, public listing platforms, and Honolulu market reports — change without
    notice, and should be verified independently with the source, the property, or your installation's
    housing office. Nothing here is a valuation, a loan offer, prequalification, or lending, legal, or
    tax advice. PCS Oahu is not affiliated with, or endorsed by, the Department of Defense or any
    military service. Equal Housing Opportunity.</p>
    <p>Data anchors on this build compiled {BUILD_DATE}. BAH: DTMO {BAH_YEAR} tables, effective
    {BAH['effective']}. Market medians: Honolulu Board of REALTORS&reg; data as republished in public
    June 2026 market reports. Rent bands: public listing platforms, mid-2026, deliberately rounded.</p>
  </div>
</div></footer>'''

def page(path, title, desc, body, current="", jsonld=None, extra_head=""):
    canonical = DOMAIN + path
    ld = ""
    if jsonld:
        ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="PCS Oahu">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/og-card.png">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="stylesheet" href="/assets/style.css">
{ld}{extra_head}
</head>
<body>
{nav(current)}
<main>
{body}
</main>
{FOOTER}
</body>
</html>'''

def crumbs_ld(path):
    parts=[("Home", DOMAIN + "/")]
    segs=[x for x in path.split("/") if x and x != "index.html"]
    acc=""
    for seg in segs:
        acc += "/" + seg
        label=seg.replace(".html","").replace("-"," ").title()
        parts.append((label, DOMAIN + acc + ("/" if not seg.endswith(".html") else "")))
    return {"@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u}
                               for i,(n,u) in enumerate(parts)]}

def article_ld(path, headline, desc):
    return {"@context": "https://schema.org", "@type": "Article",
            "headline": headline, "description": desc,
            "datePublished": "2026-08-01", "dateModified": "2026-08-01",
            "author": {"@type": "Organization", "name": "PCS Oahu"},
            "publisher": {"@type": "Organization", "name": "PCS Oahu"},
            "mainEntityOfPage": DOMAIN + path}

def dataset_ld():
    return {"@context": "https://schema.org", "@type": "Dataset",
            "name": "The BAH Reality Report — Oahu BAH vs Market Rents",
            "description": "Dated comparison of Honolulu County BAH anchors against rounded "
                           "rent bands by Oahu neighborhood pocket, refreshed with the annual "
                           "BAH cycle.",
            "url": DOMAIN + "/bah-report/", "creator": {"@type": "Organization", "name": "PCS Oahu"},
            "temporalCoverage": "2026", "dateModified": "2026-08-01",
            "license": "https://pcsoahu.com/bah-report/#cite"}

def faq_ld(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}

# ---- base + neighborhood data ----
POCKETS = {
    "aiea":      ("Aiea",               "1BR $1,900–2,300 · 2BR $2,400–2,900 · 3BR $3,200–3,800"),
    "pearlcity": ("Pearl City",         "2BR $2,400–2,900 · 3BR $3,000–3,600"),
    "saltlake":  ("Salt Lake / Moanalua","1BR $1,800–2,300 · 2BR $2,300–2,900"),
    "waipahu":   ("Waipahu",            "2BR $2,000–2,500 · 3BR $2,700–3,300"),
    "mililani":  ("Mililani",           "2BR $2,500–3,000 · 3BR $3,200–3,900"),
    "ewa":       ("Ewa Beach / Kapolei","3BR $3,000–3,800 · 4BR $3,800–4,500"),
    "wahiawa":   ("Wahiawa",            "2BR $1,900–2,400 · 3BR $2,600–3,200"),
    "kaneohe":   ("Kaneohe",            "2BR $2,600–3,200 · 3BR $3,400–4,200"),
    "kailua":    ("Kailua",             "2BR $3,200–4,000 · 3BR $4,000–5,500"),
    "downtown":  ("Downtown / Kakaako", "1BR $2,000–2,600 · 2BR $2,800–3,800"),
    "kalihi":    ("Kalihi",             "1BR $1,500–2,000 · 2BR $2,000–2,600"),
}
RENT_SRC = ("Rent bands compiled from public listing platforms, mid-2026, deliberately rounded. "
            "Verify current asking rents directly — pockets move fast in PCS season (May–August).")
