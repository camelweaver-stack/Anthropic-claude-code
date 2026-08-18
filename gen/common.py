#!/usr/bin/env python3
"""West FW Living — shared page-construction helpers.

Single source of truth for site chrome (nav, footer, disclaimer), the lead form,
and structured data. Authored pages call page(), lead_form() and faq_ld() rather
than hand-rolling HTML, so a chrome change lands everywhere at once.

WFL publishes the repository root (netlify.toml: publish = "."), so build.py
writes generated pages directly into the tree alongside the hand-authored pages
that predate this generator. `scripts/apply_standing_fixes.py` is the final,
idempotent normalization + gate pass over *every* page, generated or not.
"""

DOMAIN = "https://westfwliving.com"

# ---------------------------------------------------------------- nav (10-link spec)
NAV_EN = ("<a href='/specials.html'>Specials</a>"
          "<a href='/deals.html'>Best Deals</a>"
          "<a href='/neighborhoods/'>Neighborhoods</a>"
          "<a href='/schools/'>Schools</a>"
          "<a href='/buy/'>Buying</a>"
          "<a href='/sell/'>Selling</a>"
          "<a href='/relocate/'>Relocate</a>"
          "<a href='/guides/'>Guides</a>"
          "<a href='/tools/'>Tools</a>"
          "<a href='/es/' style='font-weight:600'>Español</a>")

# The ES nav is its own 8-link spec; the final slot is the English-mirror link and
# is rewritten per page by apply_standing_fixes.py so it points at the EN twin.
NAV_ES = ("<a href='/es/'>Inicio</a>"
          "<a href='/es/comprar/'>Comprar</a>"
          "<a href='/es/vender/'>Vender</a>"
          "<a href='/es/especiales.html'>Especiales</a>"
          "<a href='/es/segunda-oportunidad.html'>Segunda Oportunidad</a>"
          "<a href='/es/relocate/'>Mudanza</a>"
          "<a href='/es/calculadora.html'>Calculadora</a>"
          "<a href='{en}' style='font-weight:600'>English</a>")

FONTS = ("<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
         "<link href=\"https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;"
         "0,9..144,600;0,9..144,700;1,9..144,600&family=Instrument+Sans:wght@400;600&"
         "family=IBM+Plex+Mono:wght@400;600;700&display=swap\" rel=\"stylesheet\">")

DISCLAIM = (
    "West FW Living is not a real estate brokerage and does not currently offer brokerage, "
    "leasing, or apartment-locating services. All rent figures, specials, and program details "
    "are compiled from public listings and sources, change without notice, and should be "
    "verified directly with the property or program. Payment estimates are educational only — "
    "not a loan offer, prequalification, or lending advice. Drive times are typical off-peak "
    "estimates, not guarantees. School attendance zones are set by districts, are "
    "address-specific, and change; always verify with the district. Accountability ratings are "
    "published by the Texas Education Agency and describe past performance only. BAH figures "
    "are for planning only; confirm your rate with DTMO or your finance office. "
    "Equal Housing Opportunity.")

DISCLAIM_ES = (
    "West FW Living no es una correduría de bienes raíces y actualmente no ofrece servicios de "
    "correduría, arrendamiento ni de localización de apartamentos. Todas las cifras de renta, "
    "especiales y detalles de programas provienen de listados y fuentes públicas, cambian sin "
    "aviso, y deben verificarse directamente con la propiedad o el programa. Las estimaciones de "
    "pago son solo educativas — no son una oferta de préstamo, precalificación ni asesoría "
    "crediticia. Las zonas escolares las fijan los distritos, dependen de la dirección exacta y "
    "cambian; verifica siempre con el distrito. Las calificaciones de responsabilidad las publica "
    "la Agencia de Educación de Texas y describen únicamente el desempeño pasado. "
    "Igualdad de Oportunidad en la Vivienda.")

FGRID_EN = """<div class="fgrid">
    <div><h4>West FW Living</h4><p>An independent field guide to renting and buying on Fort Worth's west side — Aledo, Willow Park, Hudson Oaks, Walsh, Benbrook and the Chisholm Trail corridor. Full service is coming soon; <a href='/#list'>the early list hears first</a>.</p></div>
    <div><h4>Renting</h4><ul><li><a href='/specials.html'>This Month's Specials</a></li><li><a href='/deals.html'>Best Deals, Ranked</a></li><li><a href='/rentals/'>Browse by Feature</a></li><li><a href='/second-chance.html'>Second Chance Renting</a></li><li><a href='/rent-to-own.html'>Rent-to-Own Reality</a></li><li><a href='/areas.html'>Areas We Cover</a></li></ul></div>
    <div><h4>Explore West FW</h4><ul><li><a href='/neighborhoods/'>Neighborhoods</a></li><li><a href='/schools/'>Schools &amp; ISDs</a></li><li><a href='/compare/'>Compare Places</a></li><li><a href='/relocate/'>Relocating Here</a></li><li><a href='/move/'>Move Checklist</a></li><li><a href='/community/'>Community &amp; Local Life</a></li><li><a href='/military/'>Military &amp; BAH</a></li><li><a href='/guides/'>All Guides</a></li></ul></div>
    <div><h4>Buying</h4><ul><li><a href='/buy/'>Buy the West Side</a></li><li><a href='/calculator.html'>Rent vs. Buy Math</a></li><li><a href='/quiz.html'>Rent-or-Buy Quiz</a></li><li><a href='/es/'>En Español</a></li></ul></div>
    <div><h4>Selling</h4><ul><li><a href='/sell/'>Sell Your Home</a></li><li><a href='/sell/home-value'>What's My Home Worth</a></li><li><a href='/sell/equity-report'>The Equity Report</a></li><li><a href='/sell/sell-before-buying'>Sell Before You Buy</a></li></ul></div>
    <div><h4>Data &amp; Tools</h4><ul><li><a href='/tools/'>Renter Tools</a></li><li><a href='/data/'>Rent Data &amp; Reports</a></li><li><a href='/rent-report/august-2026.html'>Latest Rent Report</a></li><li><a href='/resources/'>Resources</a></li></ul></div>
  </div>"""

FGRID_ES = """<div class="fgrid">
    <div><h4>West FW Living</h4><p>Una guía independiente para rentar y comprar en el oeste de Fort Worth. El servicio completo llega pronto; <a href='/es/#lista'>la lista se entera primero</a>.</p></div>
    <div><h4>Rentar</h4><ul><li><a href='/es/especiales.html'>Especiales del Mes</a></li><li><a href='/deals.html'>Mejores Ofertas</a></li><li><a href='/es/segunda-oportunidad.html'>Segunda Oportunidad</a></li><li><a href='/es/semanas-gratis.html'>Semanas Gratis</a></li><li><a href='/es/romper-contrato.html'>Romper el Contrato</a></li></ul></div>
    <div><h4>Comprar</h4><ul><li><a href='/es/comprar/'>Comprar Casa</a></li><li><a href='/es/comprar/renta-o-compra.html'>Renta o Compra</a></li><li><a href='/es/comprar/primera-vivienda-texas.html'>Primera Vivienda</a></li><li><a href='/es/comprar/asistencia-enganche.html'>Ayuda con el Enganche</a></li></ul></div>
    <div><h4>Vender</h4><ul><li><a href='/es/vender/'>Vender tu Casa</a></li><li><a href='/es/vender/valor-de-tu-casa'>Valor de tu Casa</a></li><li><a href='/es/vender/reporte-de-plusvalia'>Reporte de Plusvalía</a></li></ul></div>
    <div><h4>Recursos</h4><ul><li><a href='/es/calculadora.html'>Calculadora</a></li><li><a href='/es/puntaje-credito.html'>Puntaje de Crédito</a></li><li><a href='/es/relocate/'>Mudanza</a></li><li><a href='/es/comunidad/'>Comunidad</a></li><li><a href='/'>English site</a></li></ul></div>
  </div>"""

# ---------------------------------------------------------------- lead form
# Hashed FormSubmit endpoint (privacy proxy for the destination address). The
# cleartext address must never appear in markup — apply_standing_fixes.py asserts it.
FORM_ACTION = "https://formsubmit.co/c86195fac91694c985b7fc55c96e4f77"

# Context-aware date field. Renting-associated pages ask when the lease ends;
# everything else asks an optional move date. Enforced by the form-assert gate.
FIELD_LEASE_EN = ("When does your current lease end?", "lease_end", "e.g., November 2026")
FIELD_MOVE_EN = ("When are you planning to move? (optional)", "move_date", "e.g., spring 2027")
FIELD_LEASE_ES = ("¿Cuándo vence tu contrato actual?", "lease_end", "ej., noviembre 2026")
FIELD_MOVE_ES = ("¿Para cuándo planea mudarse? (opcional)", "move_date", "ej., primavera 2027")

CONSENT_EN = ("I agree to be contacted about my inquiry by email or phone and accept the "
              "<a href=\"/privacy/\">privacy policy</a>. No spam — unsubscribe anytime.")
CONSENT_ES = ("Acepto ser contactado sobre mi consulta por correo o teléfono y acepto la "
              "<a href=\"/es/privacidad/\">política de privacidad</a>. Sin spam — cancela cuando quieras.")


def lead_form(path, heading_cta, renting=False, es=False, uid="lf"):
    """Render the hardened lead form with the context-appropriate date field."""
    label, name, ph = (FIELD_LEASE_ES if renting else FIELD_MOVE_ES) if es else \
                      (FIELD_LEASE_EN if renting else FIELD_MOVE_EN)
    consent = CONSENT_ES if es else CONSENT_EN
    thanks = f"{DOMAIN}/es/gracias.html" if es else f"{DOMAIN}/thanks.html"
    l_name, l_mail, l_phone = ("Nombre", "Correo", "Teléfono") if es else ("Name", "Email", "Phone")
    return f"""<form data-aw-hardened="2" class="lead" action="{FORM_ACTION}" method="POST"><input type="text" name="_honey" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;height:0;overflow:hidden;" aria-hidden="true"><input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_term"><input type="hidden" name="utm_content"><input type="hidden" name="referrer"><input type="hidden" name="landing_page"><input type="hidden" name="page_url"><input type="hidden" name="consent_ts">
    <input type="hidden" name="_subject" value="WFL — {path}">
    <input type="hidden" name="_next" value="{thanks}">
    <label for="{uid}name">{l_name}</label><input id="{uid}name" name="name" required autocomplete="name">
    <label for="{uid}mail">{l_mail}</label><input id="{uid}mail" name="email" type="email" required autocomplete="email">
    <label for="{uid}phone">{l_phone}</label><input id="{uid}phone" name="phone" type="tel" required>
    <label for="{uid}date">{label}</label><input id="{uid}date" name="{name}" placeholder="{ph}">
    <label class="aw-consent" style="display:flex;gap:.5rem;align-items:flex-start;font-size:.85rem;margin:.75rem 0;"><input type="checkbox" name="consent" value="agreed" required style="margin-top:.2rem;"><span>{consent}</span></label><button class="btn" type="submit">{heading_cta}</button>
  </form>"""


# ---------------------------------------------------------------- structured data
def _esc(s):
    return (s.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", " ").replace("\r", " "))


def article_ld(headline, url, description, verified, author="West FW Living"):
    """Article JSON-LD. `verified` is the visible verified date (ISO yyyy-mm-dd)."""
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            f'"@type":"Article","headline":"{_esc(headline)}","url":"{url}",'
            f'"description":"{_esc(description)}","datePublished":"{verified}",'
            f'"dateModified":"{verified}",'
            f'"author":{{"@type":"Organization","name":"{_esc(author)}"}},'
            f'"publisher":{{"@type":"Organization","name":"West FW Living"}}}}</script>')


def faq_ld(pairs):
    """FAQPage JSON-LD from [(question, answer), ...]."""
    items = ",".join(
        f'{{"@type":"Question","name":"{_esc(q)}","acceptedAnswer":'
        f'{{"@type":"Answer","text":"{_esc(a)}"}}}}' for q, a in pairs)
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            f'"@type":"FAQPage","mainEntity":[{items}]}}</script>')


UTM_SCRIPT = """<!-- aw-utm-capture --><script>
(function(){
  function qs(s){try{return new URLSearchParams(s)}catch(e){return null}}
  var K=["utm_source","utm_medium","utm_campaign","utm_term","utm_content"];
  var p=qs(location.search), store={};
  try{store=JSON.parse(sessionStorage.getItem("aw_ft")||"{}")}catch(e){}
  if(!store.landing_page){
    store.landing_page=location.pathname;
    store.referrer=document.referrer||"";
    if(p) K.forEach(function(k){var v=p.get(k); if(v) store[k]=v;});
    try{sessionStorage.setItem("aw_ft",JSON.stringify(store))}catch(e){}
  }
  document.querySelectorAll("form[data-aw-hardened]").forEach(function(f){
    K.concat(["referrer","landing_page"]).forEach(function(k){
      var el=f.querySelector('input[name="'+k+'"]');
      if(el && store[k]) el.value=store[k];
    });
    var pu=f.querySelector('input[name="page_url"]');
    if(pu) pu.value=location.pathname;
    f.addEventListener("submit",function(){
      var ts=f.querySelector('input[name="consent_ts"]');
      if(ts) ts.value=new Date().toISOString();
    });
  });
})();
</script>"""


def page(*, path, title, description, h1, eyebrow, lede, body, crumb,
         verified, es=False, alt_path=None, ld=(), extra_css=()):
    """Assemble a complete page.

    path      site-absolute path of this page, e.g. "/schools/tea-ratings-2026.html"
    alt_path  site-absolute path of the other-language twin (drives hreflang both ways)
    verified  visible "verified" date, ISO yyyy-mm-dd — rendered into the page body
    ld        iterable of JSON-LD <script> strings (use article_ld/faq_ld)
    """
    canonical = DOMAIN + path
    lang = "es" if es else "en"
    en_path = alt_path if es else path
    es_path = path if es else alt_path

    hreflang = ""
    if alt_path:
        hreflang = (f'<link rel="alternate" hreflang="en" href="{DOMAIN}{en_path}">\n'
                    f'<link rel="alternate" hreflang="es" href="{DOMAIN}{es_path}">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{en_path}">')

    nav = NAV_ES.format(en=en_path or "/") if es else NAV_EN
    brand_href = "/es/" if es else "/"
    brand_tag = "la guía del oeste de Fort Worth" if es else "the west side field guide"
    fgrid = FGRID_ES if es else FGRID_EN
    disclaim = DISCLAIM_ES if es else DISCLAIM
    css = "".join(f'<link rel="stylesheet" href="{c}">\n' for c in extra_css)
    ldblock = "\n".join(ld)

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="robots" content="max-image-preview:large">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
{FONTS}
<link rel="stylesheet" href="/styles.css">
{css}<link rel="canonical" href="{canonical}">
{hreflang}
{ldblock}
</head>
<body>
<header><div class="wrap"><div class="topbar">
  <a class='brand' href='{brand_href}'>West FW <span>Living</span><small>{brand_tag}</small></a>
  <nav>{nav}</nav>
</div></div></header>

<main><div class="wrap">
<p class="crumb">{crumb}</p>

<section class="hero hero-inner">
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</section>
{body}
</div></main>

<footer><div class="wrap">
  {fgrid}
  <p class="disclaim">{disclaim}</p>
</div></footer>
  <script src="/assets/concierge.js" defer></script>
{UTM_SCRIPT}</body>
</html>
"""
