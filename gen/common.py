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
    ("/ask/", "Ask"),
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
<form class="lead" action="https://formsubmit.co/c86195fac91694c985b7fc55c96e4f77" method="POST">
  <input type="text" name="_honey" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;height:0;overflow:hidden;" aria-hidden="true">
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
  <label class="consent" style="display:flex;gap:.5rem;align-items:flex-start;font-size:.85rem;margin:.75rem 0;"><input type="checkbox" name="consent" value="agreed" required style="margin-top:.2rem;"><span>I agree to be contacted about my inquiry by email or phone. No spam — unsubscribe anytime.</span></label>
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
      <li><a href="/guides/household-goods.html">Household goods shipping</a></li>
      <li><a href="/guides/vehicle-registration.html">Vehicle registration</a></li>
      <li><a href="/pcs-checklist/">PCS timeline checklist</a></li>
      <li><a href="/neighborhoods/">Neighborhoods</a></li>
      <li><a href="/quiz/">Pocket-match quiz</a></li>
      <li><a href="/on-base/">On-base housing</a></li>
      <li><a href="/schools/">Schools</a></li></ul></div>
    <div><h4>Buying &amp; Selling</h4><ul>
      <li><a href="/buy/">VA loans on Oahu</a></li>
      <li><a href="/guides/rent-vs-buy.html">Rent vs buy with a VA loan</a></li>
      <li><a href="/sell/">PCSing out: sell or rent</a></li>
      <li><a href="/guides/harpta.html">HARPTA for outbound sellers</a></li>
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

# Sitewide floating concierge launcher (self-contained; injected by page() on every page except
# /ask/ itself, which IS the full chat). Uses the same /.netlify/functions/concierge endpoint.
CHAT_LAUNCHER = """
<div id="pcs-ask-launcher">
  <button type="button" id="pcsAskBtn" aria-expanded="false" aria-controls="pcsAskPanel">\U0001F4AC Ask PCS Oahu</button>
  <div id="pcsAskPanel" role="dialog" aria-label="Ask PCS Oahu concierge" hidden>
    <div class="pcs-ask-head"><strong>Ask PCS Oahu</strong>
      <a class="pcs-ask-full" href="/ask/">Full page ↗</a>
      <button type="button" id="pcsAskClose" aria-label="Close">×</button></div>
    <div id="pcsAskLog"></div>
    <div class="pcs-ask-row">
      <input id="pcsAskQ" type="text" aria-label="Your question"
             placeholder="e.g., Does E-5 BAH cover a 3BR in Mililani?">
      <button type="button" id="pcsAskSend" class="btn">Ask</button></div>
    <p class="pcs-ask-fine">Educational answers from this site's guides — not legal, tax, or
       lending advice, and PCS Oahu isn't a brokerage.</p>
  </div>
</div>
<style>
#pcs-ask-launcher{position:fixed;right:16px;bottom:16px;z-index:9999}
#pcsAskBtn{background:#10222e;color:#fff;border:0;border-radius:999px;padding:.7rem 1.1rem;
  font-weight:700;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25);font-size:.95rem}
#pcsAskPanel{position:absolute;right:0;bottom:3.4rem;width:min(360px,calc(100vw - 32px));
  background:#fff;color:#10222e;border:2px solid #10222e;border-radius:12px;
  box-shadow:0 8px 30px rgba(0,0,0,.28);padding:.85rem}
.pcs-ask-head{display:flex;align-items:center;gap:.5rem;border-bottom:1px solid #e2e6e4;
  padding-bottom:.45rem;margin-bottom:.5rem}
.pcs-ask-head strong{flex:1}
.pcs-ask-full{font-size:.8rem;color:#1f5a54;font-weight:700;text-decoration:none}
#pcsAskClose{background:none;border:0;font-size:1.2rem;line-height:1;cursor:pointer;color:#5b6b73}
#pcsAskLog{max-height:44vh;overflow-y:auto;font-size:.92rem}
#pcsAskLog div{padding:.4rem 0;border-top:1px dotted #d8dcd9}
.pcs-ask-row{display:flex;gap:.4rem;margin-top:.5rem}
#pcsAskQ{flex:1;min-width:0;padding:.5rem .6rem;border:1px solid #b9c2c0;border-radius:8px;font-size:.92rem}
#pcsAskSend{padding:.5rem .8rem}
.pcs-ask-fine{font-size:.72rem;color:#5b6b73;margin:.5rem 0 0}
@media (prefers-color-scheme:dark){#pcsAskPanel{background:#0f1e28;color:#e8eeec}
  #pcsAskQ{background:#0b1720;color:#e8eeec;border-color:#2a3b44}}
</style>
<script>
(function(){
 var b=document.getElementById('pcsAskBtn'),p=document.getElementById('pcsAskPanel'),
     c=document.getElementById('pcsAskClose'),log=document.getElementById('pcsAskLog'),
     q=document.getElementById('pcsAskQ'),s=document.getElementById('pcsAskSend'),hist=[];
 function open(v){p.hidden=!v;b.setAttribute('aria-expanded',v?'true':'false');if(v)q.focus();}
 b.addEventListener('click',function(){open(p.hidden);});
 c.addEventListener('click',function(){open(false);});
 function add(who,text,muted){var d=document.createElement('div');
   if(muted)d.style.color='#5b6b73';
   d.innerHTML='<strong>'+who+':</strong> '+text;log.appendChild(d);log.scrollTop=log.scrollHeight;}
 function send(){var t=q.value.trim();if(!t)return;
   add('You',t.replace(/</g,'&lt;'));q.value='';s.disabled=true;
   hist.push({role:'user',content:t});
   fetch('/.netlify/functions/concierge',{method:'POST',
     headers:{'Content-Type':'application/json'},
     body:JSON.stringify({messages:hist.slice(-12)})})
   .then(function(r){return r.json()})
   .then(function(d){var a=d.reply||'The concierge is offline — see the <a href="/guides/">guides</a>.';
     hist.push({role:'assistant',content:a});add('PCS Oahu',a);s.disabled=false;})
   .catch(function(){add('PCS Oahu','Connection issue — try the <a href="/ask/">full page</a>.',1);s.disabled=false;});
 }
 s.addEventListener('click',send);
 q.addEventListener('keydown',function(e){if(e.key==='Enter')send();});
})();
</script>
"""

def page(path, title, desc, body, current="", jsonld=None, extra_head=""):
    canonical = DOMAIN + path
    launcher = "" if path == "/ask/" else CHAT_LAUNCHER
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
{launcher}
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
