#!/usr/bin/env python3
"""West FW Living — What the homestead exemption is actually worth (EN + ES).

Exemption amounts verified against the Texas Comptroller's framework and the
November 2025 constitutional amendments (Prop 13: general school exemption
$100K -> $140K, applying beginning with tax year 2025; Prop 11: additional
65+/disabled exemption $10K -> $60K). Each district's dollar figure is plain
arithmetic: exemption x that district's adopted 2025 school tax rate.

  Rate sources (all verified 2026-08-22):
    Aledo ISD        $1.1942  first-party: district news, adopted 2025-26,
                              seventh consecutive reduction (-$0.0110)
    White Settlement $1.2069  official Tarrant County truth-in-taxation DB
    Weatherford ISD  $1.0342  first-party: district news, adopted 8/26/2025
                              (M&O $0.7552 + I&S $0.2790, unchanged YoY)
    Fort Worth ISD   $1.0291  board adoption 8/26/2025; cross-checked against
                              the county Form 50-859 worksheet (M&O $0.7869)

These are tax-year 2025 adopted rates — the rates on current bills. Taxing
units adopt tax-year 2026 rates around September 2026; refresh then (see the
calendar anchor).
"""
from common import page, lead_form, article_ld, faq_ld, _url

VERIFIED = "2026-08-22"

EN_PATH = "/buy/homestead-exemption.html"
ES_PATH = "/es/comprar/exencion-homestead.html"

SRC_COMPTROLLER = "https://comptroller.texas.gov/taxes/property-tax/exemptions/"
SRC_ALEDO = "https://www.aledoisd.org/aledo-isd-news/~board/aledo-isd-news/post/aledo-isd-trustees-adopt-2025-2026-budget"
SRC_WISD = "https://www.weatherfordisd.com/apps/news/article/1958550"
SRC_FWISD = "https://www.fwisd.org/departments/budget/tax-rates/adopted-tax-rates"
SRC_TNT = "https://tarranttaxinfo.com"

# (district, corridor note, adopted 2025 rate, $140K value/yr, $200K 65+/disabled value/yr)
ROWS = [
    ("White Settlement ISD", "White Settlement", "$1.2069", "$1,690", "$2,414"),
    ("Aledo ISD", "Aledo, much of Willow Park, Walsh, parts of Hudson Oaks", "$1.1942", "$1,672", "$2,388"),
    ("Weatherford ISD", "Weatherford, parts of Hudson Oaks and Willow Park", "$1.0342", "$1,448", "$2,068"),
    ("Fort Worth ISD", "Fort Worth proper, incl. Benbrook", "$1.0291", "$1,441", "$2,058"),
]

ROWS_ES = [
    ("White Settlement ISD", "White Settlement", "$1.2069", "$1,690", "$2,414"),
    ("Aledo ISD", "Aledo, gran parte de Willow Park, Walsh, partes de Hudson Oaks", "$1.1942", "$1,672", "$2,388"),
    ("Weatherford ISD", "Weatherford, partes de Hudson Oaks y Willow Park", "$1.0342", "$1,448", "$2,068"),
    ("Fort Worth ISD", "Fort Worth, incl. Benbrook", "$1.0291", "$1,441", "$2,058"),
]


def _worth_table(es=False):
    rows = ROWS_ES if es else ROWS
    if es:
        head = ("<tr><th>Distrito</th><th>Cubre, a grandes rasgos</th><th>Tasa escolar 2025</th>"
                "<th>Valor anual ($140K)</th><th>65+/discapacidad ($200K)</th></tr>")
    else:
        head = ("<tr><th>District</th><th>Roughly covers</th><th>2025 school rate</th>"
                "<th>Worth per year ($140K)</th><th>65+/disabled ($200K)</th></tr>")
    body = "".join(
        f"<tr><td><strong>{d}</strong></td><td>{note}</td><td class='money'>{r}</td>"
        f"<td class='money'>&approx;{v}</td><td class='money'>&approx;{s}</td></tr>"
        for d, note, r, v, s in rows)
    return f"<table>{head}{body}</table>"


FAQ_EN = [
    ("How much is the Texas homestead exemption in 2026?",
     "$140,000 off your home's taxable value for school district taxes, raised from $100,000 "
     "by Proposition 13 (November 2025), applying beginning with tax year 2025. Homeowners 65+ "
     "or disabled receive an additional $60,000, for $200,000 total off school taxable value."),
    ("What is the exemption actually worth in dollars?",
     "Multiply $140,000 by your school district's tax rate. At the adopted 2025 rates it is "
     "worth roughly $1,441/year in Fort Worth ISD ($1.0291 per $100), $1,448 in Weatherford ISD "
     "($1.0342), $1,672 in Aledo ISD ($1.1942), and $1,690 in White Settlement ISD ($1.2069) - "
     "before any city, county, or other-unit exemptions."),
    ("How do I file, and does it cost anything?",
     "Filing is free. Submit Form 50-114 once to your county appraisal district - Tarrant "
     "Appraisal District for Tarrant-side addresses, Parker County Appraisal District for "
     "Parker-side. You never need to pay a third-party service to file it, and you do not "
     "reapply every year."),
    ("Does the exemption do anything besides cut the school bill?",
     "Yes - qualifying also activates the 10% appraisal cap: your homestead's taxable value "
     "cannot rise more than 10% per year regardless of market value, starting your second year "
     "with the exemption. In an appreciating corridor the cap can be worth more than the "
     "exemption itself over time."),
]

FAQ_ES = [
    ("¿De cuánto es la exención homestead de Texas en 2026?",
     "$140,000 menos del valor gravable de tu casa para los impuestos del distrito escolar, "
     "aumentada desde $100,000 por la Proposición 13 (noviembre de 2025), aplicable desde el "
     "año fiscal 2025. Los propietarios de 65+ o con discapacidad reciben $60,000 adicionales: "
     "$200,000 en total."),
    ("¿Cuánto vale en dólares?",
     "Multiplica $140,000 por la tasa de tu distrito escolar. Con las tasas adoptadas de 2025 "
     "vale aproximadamente $1,441/año en Fort Worth ISD ($1.0291 por $100), $1,448 en "
     "Weatherford ISD ($1.0342), $1,672 en Aledo ISD ($1.1942) y $1,690 en White Settlement "
     "ISD ($1.2069)."),
    ("¿Cómo se solicita y cuánto cuesta?",
     "Es gratis. Presenta el Formulario 50-114 una sola vez ante el distrito de avalúo de tu "
     "condado (Tarrant Appraisal District o Parker County Appraisal District). Nunca necesitas "
     "pagar a un tercero para presentarla, y no se renueva cada año."),
    ("¿La exención hace algo más que bajar la factura escolar?",
     "Sí: también activa el tope de avalúo del 10% - el valor gravable de tu homestead no puede "
     "subir más de 10% al año sin importar el valor de mercado, a partir de tu segundo año con "
     "la exención."),
]


def build_en():
    body = f"""<section>
  <h2 id="short-answer">The short answer</h2>
  <p>The Texas homestead exemption takes <strong>$140,000 off your home's taxable value for school district taxes</strong> &mdash; raised from $100,000 by Proposition 13 in November 2025, applying beginning with tax year 2025. On the west side that is worth roughly <strong>$1,441 to $1,690 a year</strong> depending on your school district, and homeowners 65+ or disabled get $200,000 off instead (Proposition 11's additional $60,000). It is free to claim, filed once, and it switches on a second benefit &mdash; the 10% appraisal cap &mdash; that can quietly outearn the exemption itself in a corridor appreciating like this one.</p>
  <p class="tag">Verified {VERIFIED} &middot; rates are each district's adopted 2025 rate &middot; arithmetic shown per district below</p>
</section>

<section>
  <h2>What it's worth, district by district</h2>
  <p>The exemption's dollar value is just <em>exemption &times; your school district's rate</em>. Here is that arithmetic at the adopted 2025 rates (the rates on current bills), for the districts a west-side address actually lands in:</p>
  {_worth_table()}
  <p>Three reading notes. First, the district is set by your address, not your city &mdash; Willow Park and Hudson Oaks both split between districts, and Benbrook is Fort Worth ISD (<a href="/schools/tea-ratings-2026">the 2026 ratings page</a> maps this). Second, the November 2025 increase alone &mdash; the $40,000 bump from $100K to $140K &mdash; added roughly $410&ndash;$480 a year in these districts. Third, these figures are the school-district slice only: cities, counties, and special districts levy separately and some offer their own optional exemptions &mdash; your appraisal-district record shows exactly which ones apply to your address.</p>
</section>

<section>
  <h2>How to claim it (free, once)</h2>
  <ol>
    <li><strong>File Form 50-114</strong> with your county appraisal district &mdash; Tarrant Appraisal District for Tarrant-side addresses (Benbrook, White Settlement, Fort Worth), Parker County Appraisal District for Parker-side (Aledo, Willow Park, Hudson Oaks, Weatherford). Online, free.</li>
    <li><strong>Do it the week you close.</strong> You qualify once you own and occupy the home as your principal residence &mdash; no need to wait for a new year, and if you missed it, late filing is allowed for a limited period (ask your appraisal district).</li>
    <li><strong>Never pay a &ldquo;filing service.&rdquo;</strong> Mailers offering to file it for $50&ndash;$100 sell you a free form. The districts themselves warn about these.</li>
    <li><strong>File once, keep it.</strong> No annual renewal. Update it only if you move.</li>
  </ol>
  <p>The quiet second benefit: qualifying activates the <strong>10% appraisal cap</strong> &mdash; your homestead's taxable value can't rise more than 10% a year regardless of market value, starting your second year with the exemption. <a href="/buy/property-taxes-for-buyers">The property-tax playbook</a> covers the cap, the free annual protest, and the PID/MUD layer together.</p>
</section>

<section>
  <h2>Who this applies to</h2>
  <p><strong>New buyers</strong> anywhere in the corridor &mdash; this is the first form to file after closing, and the savings above are annual, not one-time. <strong>Owners 65+ or disabled</strong> &mdash; the additional $60,000 (a $200,000 total) plus the school-tax ceiling makes this the single most valuable filing in Texas property tax. <strong>Renters running the buy math</strong> &mdash; the exemption narrows the rent-vs-buy gap; <a href="/calculator">the calculator</a> and <a href="/buy/rent-vs-buy">the rent-vs-buy engine</a> both assume you claim it.</p>
</section>

<section>
  <h2>One honest timing note</h2>
  <p>The rates above are the <strong>adopted 2025 rates</strong> &mdash; what current bills are computed on. Texas taxing units adopt their tax-year 2026 rates around September 2026, and several corridor districts have been cutting rates for years (Aledo ISD's 2025 adoption was its seventh consecutive reduction). When the 2026 rates land, the per-district arithmetic here shifts slightly; this page is refreshed each cycle.</p>
</section>

<section>
  <h2>Next steps</h2>
  <ol>
    <li>Check whether your exemption is already on file: look up your address in your appraisal district's records.</li>
    <li>Not on file? Submit Form 50-114 to the appraisal district for your county. Free.</li>
    <li>65+ or disabled? File the additional exemption at the same time.</li>
    <li>Pair it with the annual protest &mdash; <a href="/buy/property-taxes-for-buyers">the playbook</a> walks both levers.</li>
  </ol>
</section>

<section>
  <h2>Sources</h2>
  <ul>
    <li>Texas Comptroller &mdash; <a href="{SRC_COMPTROLLER}" rel="nofollow">residence homestead exemptions</a> (framework, Form 50-114).</li>
    <li>Proposition 13 &amp; 11 (November 2025) &mdash; $140,000 general school exemption applying from tax year 2025; additional 65+/disabled exemption to $60,000.</li>
    <li>Aledo ISD &mdash; <a href="{SRC_ALEDO}" rel="nofollow">2025-26 adopted rate $1.1942</a> (seventh consecutive reduction).</li>
    <li>Weatherford ISD &mdash; <a href="{SRC_WISD}" rel="nofollow">2025-26 adopted rate $1.0342</a> (M&amp;O $0.7552 + I&amp;S $0.2790).</li>
    <li>Fort Worth ISD &mdash; <a href="{SRC_FWISD}" rel="nofollow">adopted rate $1.0291</a> (board adoption 2025-08-26; cross-checked against the county Form 50-859 worksheet).</li>
    <li>White Settlement ISD &mdash; adopted rate $1.2069 per the official <a href="{SRC_TNT}" rel="nofollow">Tarrant County truth-in-taxation database</a>.</li>
  </ul>
  <p><strong>Verified {VERIFIED}.</strong> Educational only &mdash; not tax or legal advice for any specific situation; confirm your own exemptions with your appraisal district.</p>
</section>

<section>
  <h2>Keep reading</h2>
  <p><a href="/buy/">the buyer's guide</a> &middot; <a href="/buy/property-taxes-for-buyers">the property-tax playbook</a> &middot; <a href="/buy/first-time-buyer-texas">first-time buying in Texas</a> &middot; <a href="/data/property-tax">rate tables by city &amp; district</a> &middot; <a href="/guides/living-in-benbrook">living in Benbrook</a></p>
  <p><a href="{_url(ES_PATH)}" hreflang="es">Lee esta p&aacute;gina en espa&ntilde;ol &mdash; La exenci&oacute;n homestead</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>Want the 2026 rate refresh when districts adopt?</h2>
  <p>Taxing units adopt new rates around September. We redo this page's arithmetic when they land &mdash; the early list hears first, no other mail.</p>
{lead_form(EN_PATH, "Tell me when the 2026 rates land", renting=False, es=False, uid="hse")}
</section>
"""
    return page(
        path=EN_PATH,
        title="What the Texas Homestead Exemption Is Actually Worth in West Fort Worth (2026)",
        description=("The $140K school-district homestead exemption in dollars: roughly $1,441-$1,690 "
                     "a year across Aledo, Weatherford, White Settlement and Fort Worth ISDs at adopted "
                     "2025 rates - plus how to file free and the 10% cap it switches on."),
        h1="What the homestead exemption is actually worth here",
        eyebrow="THE $140K EXEMPTION, IN DOLLARS &middot; DISTRICT BY DISTRICT",
        lede=("$140,000 off school taxable value &mdash; roughly $1,441 to $1,690 a year on the west side, "
              "district depending, and double the exemption at 65+. Free to claim, filed once, and it "
              "switches on the 10% cap most owners forget."),
        crumb="<a href='/'>Home</a> / <a href='/buy/'>Buying</a> / Homestead Exemption",
        verified=VERIFIED,
        es=False,
        alt_path=ES_PATH,
        body=body,
        ld=[article_ld("What the homestead exemption is actually worth in west Fort Worth",
                       f"https://westfwliving.com{_url(EN_PATH)}",
                       "The $140K school homestead exemption converted to dollars per year for each west Fort Worth corridor district, at adopted 2025 rates.",
                       VERIFIED),
            faq_ld(FAQ_EN)],
    )


def build_es():
    body = f"""<section>
  <h2>La respuesta corta</h2>
  <p>La exenci&oacute;n homestead de Texas resta <strong>$140,000 del valor gravable de tu casa para los impuestos del distrito escolar</strong> &mdash; aumentada desde $100,000 por la Proposici&oacute;n 13 en noviembre de 2025, aplicable desde el a&ntilde;o fiscal 2025. En el lado oeste vale aproximadamente <strong>$1,441 a $1,690 al a&ntilde;o</strong> seg&uacute;n tu distrito escolar, y los propietarios de 65+ o con discapacidad restan $200,000 en total (los $60,000 adicionales de la Proposici&oacute;n 11). Es gratis, se presenta una sola vez, y activa un segundo beneficio &mdash; el tope de aval&uacute;o del 10% &mdash; que con el tiempo puede valer m&aacute;s que la propia exenci&oacute;n.</p>
  <p class="tag">Verificado el {VERIFIED} &middot; tasas adoptadas de 2025 &middot; la aritm&eacute;tica, distrito por distrito</p>
</section>

<section>
  <h2>Cu&aacute;nto vale, distrito por distrito</h2>
  <p>El valor en d&oacute;lares es simplemente <em>exenci&oacute;n &times; la tasa de tu distrito escolar</em>. Con las tasas adoptadas de 2025 (las de las facturas actuales):</p>
  {_worth_table(es=True)}
  <p>Tres notas. Primera: el distrito lo fija tu direcci&oacute;n, no tu ciudad &mdash; Willow Park y Hudson Oaks se dividen entre distritos, y Benbrook es Fort Worth ISD (<a href="/es/escuelas/calificaciones-tea-2026">el mapa est&aacute; en la p&aacute;gina de calificaciones</a>). Segunda: solo el aumento de noviembre de 2025 &mdash; de $100K a $140K &mdash; agreg&oacute; unos $410&ndash;$480 al a&ntilde;o en estos distritos. Tercera: estas cifras son solo la parte escolar; ciudades, condados y distritos especiales cobran por separado y algunos ofrecen sus propias exenciones opcionales.</p>
</section>

<section>
  <h2>C&oacute;mo reclamarla (gratis, una vez)</h2>
  <ol>
    <li><strong>Presenta el Formulario 50-114</strong> ante el distrito de aval&uacute;o de tu condado &mdash; Tarrant Appraisal District (Benbrook, White Settlement, Fort Worth) o Parker County Appraisal District (Aledo, Willow Park, Hudson Oaks, Weatherford). En l&iacute;nea y gratis.</li>
    <li><strong>Hazlo la semana en que cierres.</strong> Calificas desde que eres due&ntilde;o y ocupas la casa como residencia principal; si se te pas&oacute;, hay un plazo limitado para presentarla tarde (preg&uacute;ntale a tu distrito de aval&uacute;o).</li>
    <li><strong>Nunca pagues a un &ldquo;servicio de tr&aacute;mite.&rdquo;</strong> Las cartas que ofrecen presentarla por $50&ndash;$100 te venden un formulario gratuito.</li>
    <li><strong>Se presenta una vez.</strong> Sin renovaci&oacute;n anual; act&uacute;alizala solo si te mudas.</li>
  </ol>
  <p>El segundo beneficio silencioso: calificar activa el <strong>tope de aval&uacute;o del 10%</strong> &mdash; el valor gravable de tu homestead no puede subir m&aacute;s de 10% al a&ntilde;o sin importar el mercado, desde tu segundo a&ntilde;o con la exenci&oacute;n.</p>
</section>

<section>
  <h2>A qui&eacute;n le aplica</h2>
  <p><strong>Compradores nuevos</strong> en todo el corredor &mdash; es el primer formulario despu&eacute;s del cierre, y el ahorro es anual, no de una sola vez. <strong>Propietarios de 65+ o con discapacidad</strong> &mdash; los $60,000 adicionales m&aacute;s el tope escolar la convierten en el tr&aacute;mite m&aacute;s valioso del impuesto predial en Texas. <strong>Inquilinos haciendo la cuenta de compra</strong> &mdash; <a href="/es/calculadora">la calculadora</a> y <a href="/es/comprar/renta-o-compra">renta o compra</a> asumen que la reclamas.</p>
</section>

<section>
  <h2>Una nota honesta de calendario</h2>
  <p>Las tasas de arriba son las <strong>adoptadas para 2025</strong>. Las unidades fiscales de Texas adoptan sus tasas de 2026 alrededor de septiembre de 2026 (la adopci&oacute;n 2025 de Aledo ISD fue su s&eacute;ptima reducci&oacute;n consecutiva). Cuando lleguen las tasas de 2026, la aritm&eacute;tica cambia un poco; esta p&aacute;gina se actualiza cada ciclo.</p>
</section>

<section>
  <h2>Pr&oacute;ximos pasos</h2>
  <ol>
    <li>Revisa si tu exenci&oacute;n ya est&aacute; registrada: busca tu direcci&oacute;n en los registros de tu distrito de aval&uacute;o.</li>
    <li>&iquest;No aparece? Presenta el Formulario 50-114. Gratis.</li>
    <li>&iquest;65+ o discapacidad? Presenta la exenci&oacute;n adicional al mismo tiempo.</li>
    <li>Comb&iacute;nala con la protesta anual del aval&uacute;o.</li>
  </ol>
</section>

<section>
  <h2>Fuentes</h2>
  <ul>
    <li>Contralor&iacute;a de Texas &mdash; <a href="{SRC_COMPTROLLER}" rel="nofollow">exenciones de residencia homestead</a> (marco legal, Formulario 50-114).</li>
    <li>Proposiciones 13 y 11 (noviembre 2025) &mdash; exenci&oacute;n escolar general de $140,000 desde el a&ntilde;o fiscal 2025; adicional de 65+/discapacidad a $60,000.</li>
    <li>Aledo ISD &mdash; <a href="{SRC_ALEDO}" rel="nofollow">tasa adoptada $1.1942</a> &middot; Weatherford ISD &mdash; <a href="{SRC_WISD}" rel="nofollow">tasa adoptada $1.0342</a> &middot; Fort Worth ISD &mdash; <a href="{SRC_FWISD}" rel="nofollow">tasa adoptada $1.0291</a> &middot; White Settlement ISD &mdash; $1.2069 seg&uacute;n la <a href="{SRC_TNT}" rel="nofollow">base oficial de Tarrant County</a>.</li>
  </ul>
  <p><strong>Verificado el {VERIFIED}.</strong> Contenido educativo &mdash; no es asesor&iacute;a fiscal ni legal para ninguna situaci&oacute;n espec&iacute;fica; confirma tus exenciones con tu distrito de aval&uacute;o.</p>
</section>

<section>
  <h2>Sigue leyendo</h2>
  <p><a href="/es/comprar/">comprar casa</a> &middot; <a href="/es/comprar/primera-vivienda-texas">primera vivienda</a> &middot; <a href="/es/comprar/asistencia-enganche">ayuda con el enganche</a> &middot; <a href="/es/guias/vivir-en-benbrook">vivir en Benbrook</a></p>
  <p><a href="{_url(EN_PATH)}" hreflang="en">Read this page in English &mdash; The homestead exemption, in dollars</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>&iquest;Quieres la actualizaci&oacute;n cuando adopten las tasas de 2026?</h2>
  <p>Las unidades fiscales adoptan alrededor de septiembre. Rehacemos la aritm&eacute;tica cuando lleguen &mdash; la lista se entera primero.</p>
{lead_form(ES_PATH, "Av&iacute;senme cuando lleguen las tasas 2026", renting=False, es=True, uid="hse")}
</section>
"""
    return page(
        path=ES_PATH,
        title="La Exenci&oacute;n Homestead de Texas en D&oacute;lares: Oeste de Fort Worth (2026)",
        description=("La exenci&oacute;n escolar de $140K convertida a d&oacute;lares: unos $1,441-$1,690 al "
                     "a&ntilde;o en Aledo, Weatherford, White Settlement y Fort Worth ISD con las tasas "
                     "adoptadas de 2025 - y c&oacute;mo presentarla gratis."),
        h1="La exenci&oacute;n homestead, en d&oacute;lares",
        eyebrow="LA EXENCI&Oacute;N DE $140K &middot; DISTRITO POR DISTRITO",
        lede=("$140,000 menos del valor gravable escolar &mdash; unos $1,441 a $1,690 al a&ntilde;o en el "
              "lado oeste seg&uacute;n el distrito, y el doble de exenci&oacute;n a los 65+. Gratis, una sola "
              "vez, y activa el tope del 10% que casi todos olvidan."),
        crumb="<a href='/es/'>Inicio</a> / <a href='/es/comprar/'>Comprar</a> / Exenci&oacute;n Homestead",
        verified=VERIFIED,
        es=True,
        alt_path=EN_PATH,
        body=body,
        ld=[article_ld("La exenci&oacute;n homestead, en d&oacute;lares",
                       f"https://westfwliving.com{_url(ES_PATH)}",
                       "La exenci&oacute;n escolar de $140K convertida a d&oacute;lares anuales por distrito del corredor oeste de Fort Worth.",
                       VERIFIED),
            faq_ld(FAQ_ES)],
    )


def build():
    return {EN_PATH: build_en(), ES_PATH: build_es()}
