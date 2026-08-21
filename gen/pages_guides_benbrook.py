#!/usr/bin/env python3
"""West FW Living — Living in Benbrook: the value-play guide (EN + ES).

Every figure on this page is reused from data the site has already published
with its own sourcing, or from the TEA 2026 accountability data verified
2026-08-16 (see gen/pages_schools_ratings.py). Nothing is newly estimated.

  Sale bands + $/sqft + days-to-contract: compiled from public listing data,
    summer 2026 — as published on /sell/benbrook and /sell/aledo.
  Rent bands: compiled from public listing platforms, May–July 2026 — as
    published on /areas/benbrook, including its platform-trend-conflict caveat.
  School ratings: TEA 2026 A–F release (2026-08-14), per-campus figures from
    the TEA Statewide Multi-Year Ratings spreadsheet, verified 2026-08-16.

  Verified (this page assembled and figures re-checked): 2026-08-20.
"""
from common import page, lead_form, article_ld, faq_ld, _url

VERIFIED = "2026-08-20"

EN_PATH = "/guides/living-in-benbrook.html"
ES_PATH = "/es/guias/vivir-en-benbrook.html"

SRC_TEA = "https://tea.texas.gov/school-and-district-leaders/accountability/academic-accountability/performance-reporting/2026-accountability-rating-system"

# (campus, 2026 letter, 2026 score, change text) — from the TEA 2026 spreadsheet.
CAMPUSES = [
    ("Westpark Elementary", "A", 92, "+2 pts vs 2025"),
    ("Benbrook Middle/High School", "A", 90, "&uarr; from B (85)"),
    ("Benbrook Elementary", "B", 89, "&darr; from A (92)"),
    ("Luella Merrett Elementary", "B", 84, "+1 pt vs 2025"),
    ("Ridglea Hills Elementary", "C", 79, "+4 pts vs 2025"),
    ("Waverly Park Elementary", "C", 74, "&darr; from B (81)"),
    ("Western Hills High School", "C", 74, "&uarr; from D (69)"),
]


def _campus_table(es=False):
    head = ("<tr><th>Plantel</th><th>2026</th><th>Puntaje</th><th>Cambio</th></tr>" if es else
            "<tr><th>Campus</th><th>2026</th><th>Score</th><th>Change vs 2025</th></tr>")
    body = "".join(
        f"<tr><td>{n}</td><td><span class='tag'>{l}</span></td>"
        f"<td class='money'>{s}</td><td>{c}</td></tr>"
        for n, l, s, c in CAMPUSES)
    return f"<table>{head}{body}</table>"


def _money_table(es=False):
    if es:
        head = "<tr><th>&nbsp;</th><th>Benbrook</th><th>Aledo</th></tr>"
        rows = [
            ("Banda t&iacute;pica de venta", "$300K&ndash;$420K", "$520K&ndash;$750K"),
            ("Por pie cuadrado, rango t&iacute;pico", "$165&ndash;$205", "$210&ndash;$260"),
            ("D&iacute;as t&iacute;picos hasta contrato", "35&ndash;65", "45&ndash;75"),
        ]
    else:
        head = "<tr><th>&nbsp;</th><th>Benbrook</th><th>Aledo</th></tr>"
        rows = [
            ("Typical sale band", "$300K&ndash;$420K", "$520K&ndash;$750K"),
            ("Per square foot, typical range", "$165&ndash;$205", "$210&ndash;$260"),
            ("Typical days to contract", "35&ndash;65", "45&ndash;75"),
        ]
    body = "".join(f"<tr><td>{a}</td><td class='money'>{b}</td><td class='money'>{c}</td></tr>"
                   for a, b, c in rows)
    return f"<table>{head}{body}</table>"


FAQ_EN = [
    ("Is Benbrook cheaper than Aledo?",
     "Substantially, by the published bands: Benbrook's typical sale band runs $300K-$420K "
     "against Aledo's $520K-$750K, and $165-$205 per square foot against $210-$260 "
     "(compiled from public listing data, summer 2026). The bands sit roughly $200K apart "
     "at the low end."),
    ("Are Benbrook's schools any good?",
     "Better than the district letter suggests. Benbrook sits in Fort Worth ISD, which rated "
     "a C (77) in TEA's 2026 cycle - but Benbrook Middle/High School rated an A (90) and "
     "Westpark Elementary an A (92). Campus ratings, not the district letter, describe the "
     "schools a Benbrook address actually feeds; verify the zoned campus for any specific "
     "address with the district."),
    ("What school district serves Benbrook?",
     "Fort Worth ISD. Note that listing sites frequently label southwest Fort Worth addresses "
     "as 'Benbrook' - the city and the school assignment are both address-specific, so verify "
     "them for any specific property before signing or closing."),
    ("Can I rent in Benbrook first to try it?",
     "Yes, and the rental-house inventory is a genuine strength: houses carry a median near "
     "$1,650, with 1-bedrooms averaging roughly $980-$1,195 (public listing platforms, "
     "May-July 2026). One caution from that compilation: major platforms currently disagree "
     "on Benbrook's rent-trend direction, so get written unit-level quotes rather than "
     "trusting market averages."),
]

FAQ_ES = [
    ("¿Benbrook es más barato que Aledo?",
     "Considerablemente, según las bandas publicadas: la banda típica de venta de Benbrook es "
     "$300K-$420K contra $520K-$750K en Aledo, y $165-$205 por pie cuadrado contra $210-$260 "
     "(compilado de listados públicos, verano 2026)."),
    ("¿Las escuelas de Benbrook son buenas?",
     "Mejores de lo que sugiere la letra del distrito. Benbrook pertenece a Fort Worth ISD, "
     "que obtuvo C (77) en el ciclo 2026 de la TEA - pero Benbrook Middle/High School obtuvo "
     "A (90) y Westpark Elementary A (92). Verifica el plantel asignado a la dirección exacta "
     "con el distrito."),
    ("¿Qué distrito escolar sirve a Benbrook?",
     "Fort Worth ISD. Ojo: los portales suelen etiquetar direcciones del suroeste de Fort "
     "Worth como 'Benbrook' - la ciudad y la asignación escolar dependen de la dirección "
     "exacta; verifícalas antes de firmar o cerrar."),
    ("¿Puedo rentar primero en Benbrook?",
     "Sí. Las casas de renta son una fortaleza real: mediana cerca de $1,650, y los "
     "departamentos de 1 recámara promedian $980-$1,195 (portales públicos, mayo-julio 2026). "
     "Los portales hoy no coinciden en la dirección de la tendencia de rentas, así que pide "
     "cotizaciones por escrito por unidad."),
]


def build_en():
    body = f"""<section>
  <h2 id="short-answer">The short answer</h2>
  <p>Benbrook is the west side's value play: a settled lake town of roughly 25,000 that delivers most of the family texture people move to the corridor for &mdash; parks, water, a real middle/high school argument &mdash; at a published price band roughly <strong>$200K below Aledo's</strong>. The schools half of that sentence got materially stronger in August 2026, when TEA rated <strong>Benbrook Middle/High School an A (90)</strong>, up from a B, inside a Fort Worth ISD whose district letter (C) keeps mispricing the address for people who stop reading at the district line.</p>
  <p class="tag">Verified {VERIFIED} &middot; price bands compiled summer 2026 &middot; ratings from TEA's 2026 release</p>
</section>

<section>
  <h2>1 &middot; The money layer</h2>
  <p>Side by side, from the bands this site publishes on its <a href="/sell/benbrook">Benbrook</a> and <a href="/sell/aledo">Aledo</a> seller pages (compiled from public listing data, summer 2026 &mdash; typical ranges for each area, not a valuation of any property):</p>
  {_money_table()}
  <p>The low ends of the two bands sit about $220K apart; the high ends, over $300K. Benbrook also moves faster to contract, which cuts both ways: less time to deliberate as a buyer, less carrying time as a seller. On the renting side &mdash; a real option here, since the town splits almost exactly half renters, half owners &mdash; 1-bedrooms average roughly $980&ndash;$1,195, 2-bedrooms $1,450&ndash;$1,560, and rental houses (the deep end of Benbrook's inventory) carry a median near $1,650 (public listing platforms, May&ndash;July 2026). One honesty note carried over from <a href="/areas/benbrook">the Benbrook area file</a>: the major platforms currently disagree on which direction Benbrook rents are moving, so treat averages as orientation and get written unit-level quotes.</p>
</section>

<section>
  <h2>2 &middot; The schools layer &mdash; where the 2026 ratings changed the argument</h2>
  <p>Benbrook's usual knock is the district letter: it sits in Fort Worth ISD, which rated a <strong>C (77)</strong> in TEA's 2026 cycle. But nobody attends a district average &mdash; they attend a campus, and the campuses a Benbrook address actually feeds look different:</p>
  {_campus_table()}
  <p>The headline is Benbrook Middle/High moving from a B to an <strong>A (90)</strong> &mdash; a rating higher than several campuses in districts whose letter grade carries a six-figure housing premium. The honest counterweights: Benbrook Elementary slipped from an A to a B this cycle, the Western Hills side of the zone map still rates C, and a single year's movement is thin evidence in either direction. Full corridor tables, and what a rating does and doesn't tell you, live in <a href="/schools/tea-ratings-2026">the 2026 TEA ratings page</a>. Two verification rules do real work here: listing sites frequently label southwest Fort Worth addresses as &ldquo;Benbrook,&rdquo; and attendance zones are drawn to the address &mdash; so confirm both the city and the zoned campus with the district before money moves.</p>
</section>

<section>
  <h2>3 &middot; The daily-life layer</h2>
  <p>The lake is the point. Benbrook Lake and Dutch Branch Park anchor the town's free recreation &mdash; fishing, camping, courts and fields &mdash; and the west side has no bigger outdoor asset. Lockheed and west-side commuters run 12&ndash;20 minutes to the plant against southwest Fort Worth traffic instead of the I-30 grind. The texture is settled rather than new-build: this is the corridor's half-owner, half-renter equilibrium town, not a master-planned growth front like <a href="/guides/living-in-walsh">Walsh</a>. For the feel of it &mdash; the rhythm, the third places &mdash; see <a href="/community/vibes/benbrook">the Benbrook vibe file</a>.</p>
</section>

<section>
  <h2>4 &middot; The decision layer</h2>
  <p><strong>Benbrook fits</strong> buyers priced out of the Aledo band who still want the family package; Lockheed and west-side workers who value the short commute; renters who want a house rather than a corridor complex; and &ldquo;scout year&rdquo; households renting the neighborhood they might buy in. <strong>Stretch to Aledo anyway</strong> if the specific thing you are buying is the district itself &mdash; Aledo ISD rated an A (92) district-wide in 2026, every campus A or B &mdash; or if resale-market depth at the family price point is the priority. The middle path exists too: <a href="/compare/benbrook-vs-white-settlement">Benbrook vs White Settlement</a> covers the next rung down, and <a href="/buy/rent-or-buy-benbrook">the Benbrook rent-or-buy math</a> runs the numbers on entering at all.</p>
  <h3>Next steps</h3>
  <ol>
    <li>Run the address, not the town: confirm city limits and the zoned campus with Fort Worth ISD for any specific property.</li>
    <li>Check the current campus ratings on <a href="/schools/tea-ratings-2026">the 2026 TEA page</a> and at TXschools.gov.</li>
    <li>Renting first? Start from <a href="/areas/benbrook">the Benbrook area file</a> and get three written quotes &mdash; the platforms disagree on trend direction right now.</li>
    <li>Buying? Pair the bands above with <a href="/calculator">the rent-vs-buy math</a>.</li>
  </ol>
</section>

<section>
  <h2>Sources</h2>
  <ul>
    <li>Sale bands, $/sqft, days-to-contract &mdash; compiled from public listing data, summer 2026, as published on <a href="/sell/benbrook">/sell/benbrook</a> and <a href="/sell/aledo">/sell/aledo</a>.</li>
    <li>Rent bands and platform-trend caveat &mdash; public listing platforms, May&ndash;July 2026, as published on <a href="/areas/benbrook">/areas/benbrook</a>.</li>
    <li>School ratings &mdash; <a href="{SRC_TEA}" rel="nofollow">TEA 2026 Accountability Rating System</a> (released 2026-08-14; per-campus figures from the Statewide Multi-Year Ratings spreadsheet, verified 2026-08-16).</li>
  </ul>
  <p><strong>Verified {VERIFIED}.</strong> Bands are typical ranges compiled from public sources, change without notice, and are not a valuation of any specific property.</p>
</section>

<section>
  <h2>Keep reading</h2>
  <p><a href="/guides/">the guide library</a> &middot; <a href="/guides/living-in-aledo">living in Aledo</a> &middot; <a href="/guides/living-in-walsh">living in Walsh</a> &middot; <a href="/neighborhoods/">the neighborhood library</a> &middot; <a href="/relocate/">the relocation hub</a></p>
  <p><a href="{_url(ES_PATH)}" hreflang="es">Lee esta p&aacute;gina en espa&ntilde;ol &mdash; Vivir en Benbrook</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>Watching the Benbrook-vs-Aledo gap?</h2>
  <p>We refresh the bands when the underlying compilations update, and the school tables every TEA cycle. The early list hears when the numbers move &mdash; no other mail.</p>
{lead_form(EN_PATH, "Tell me when the numbers move", renting=False, es=False, uid="lib")}
</section>
"""
    return page(
        path=EN_PATH,
        title="Living in Benbrook: the West Side's Value Play &mdash; Prices, Schools &amp; the Aledo Gap",
        description=("Benbrook vs Aledo by the published numbers: a $300K-$420K sale band against "
                     "$520K-$750K, an A-rated middle/high school inside a C-rated district, the lake, "
                     "and who the trade actually fits. Verified 2026-08-20."),
        h1="Living in Benbrook: the value play, by the numbers",
        eyebrow="THE DEFINITIVE GUIDE &middot; PRICES, SCHOOLS &amp; THE ALEDO GAP",
        lede=("Most of the west side's family texture at a published band roughly $200K below Aledo's "
              "&mdash; and, as of TEA's August 2026 ratings, an A-rated middle/high school inside a "
              "district whose C keeps mispricing the address."),
        crumb="<a href='/'>Home</a> / <a href='/guides/'>Guides</a> / Living in Benbrook",
        verified=VERIFIED,
        es=False,
        alt_path=ES_PATH,
        body=body,
        ld=[article_ld("Living in Benbrook: the value play, by the numbers",
                       f"https://westfwliving.com{_url(EN_PATH)}",
                       "Benbrook vs Aledo by the published numbers: prices, 2026 TEA campus ratings, and who the trade fits.",
                       VERIFIED),
            faq_ld(FAQ_EN)],
    )


def build_es():
    body = f"""<section>
  <h2>La respuesta corta</h2>
  <p>Benbrook es la jugada de valor del lado oeste: un pueblo asentado junto al lago, de unos 25,000 habitantes, que ofrece la mayor parte de la textura familiar por la que la gente se muda al corredor &mdash; parques, agua, y un argumento escolar real &mdash; con una banda de precios publicada aproximadamente <strong>$200K por debajo de la de Aledo</strong>. La mitad escolar de esa oraci&oacute;n se fortaleci&oacute; en agosto de 2026, cuando la TEA calific&oacute; a <strong>Benbrook Middle/High School con A (90)</strong>, subiendo desde B, dentro de un Fort Worth ISD cuya letra de distrito (C) sigue malinterpretando la direcci&oacute;n para quien deja de leer en la l&iacute;nea del distrito.</p>
  <p class="tag">Verificado el {VERIFIED} &middot; bandas compiladas en verano 2026 &middot; calificaciones del ciclo 2026 de la TEA</p>
</section>

<section>
  <h2>1 &middot; El dinero</h2>
  <p>Lado a lado, seg&uacute;n las bandas que este sitio publica en sus p&aacute;ginas de venta de <a href="/es/vender/benbrook">Benbrook</a> y <a href="/es/vender/aledo">Aledo</a> (compiladas de listados p&uacute;blicos, verano 2026 &mdash; rangos t&iacute;picos por zona, no una valuaci&oacute;n de ninguna propiedad):</p>
  {_money_table(es=True)}
  <p>Los extremos bajos de las dos bandas est&aacute;n a unos $220K de distancia; los altos, a m&aacute;s de $300K. Del lado de la renta &mdash; opci&oacute;n real aqu&iacute;, porque el pueblo se divide casi exactamente entre inquilinos y propietarios &mdash; los departamentos de 1 rec&aacute;mara promedian $980&ndash;$1,195, los de 2 rec&aacute;maras $1,450&ndash;$1,560, y las casas de renta (la fortaleza del inventario de Benbrook) tienen una mediana cerca de $1,650 (portales p&uacute;blicos, mayo&ndash;julio 2026). Una nota de honestidad: los portales hoy no coinciden en la direcci&oacute;n de la tendencia de rentas en Benbrook &mdash; usa los promedios como orientaci&oacute;n y pide cotizaciones por escrito por unidad.</p>
</section>

<section>
  <h2>2 &middot; Las escuelas &mdash; donde el ciclo 2026 cambi&oacute; el argumento</h2>
  <p>El reproche habitual a Benbrook es la letra del distrito: pertenece a Fort Worth ISD, que obtuvo <strong>C (77)</strong> en el ciclo 2026 de la TEA. Pero nadie asiste al promedio de un distrito &mdash; se asiste a un plantel, y los planteles que una direcci&oacute;n de Benbrook realmente alimenta se ven distintos:</p>
  {_campus_table(es=True)}
  <p>El titular es Benbrook Middle/High subiendo de B a <strong>A (90)</strong>. Los contrapesos honestos: Benbrook Elementary baj&oacute; de A a B este ciclo, el lado de Western Hills del mapa sigue en C, y el movimiento de un solo a&ntilde;o es evidencia delgada en cualquier direcci&oacute;n. Las tablas completas del corredor est&aacute;n en <a href="/es/escuelas/calificaciones-tea-2026">la p&aacute;gina de calificaciones TEA 2026</a>. Dos reglas de verificaci&oacute;n hacen el trabajo real: los portales suelen etiquetar direcciones del suroeste de Fort Worth como &ldquo;Benbrook,&rdquo; y las zonas escolares se trazan por direcci&oacute;n &mdash; confirma la ciudad y el plantel asignado con el distrito antes de mover dinero.</p>
</section>

<section>
  <h2>3 &middot; La vida diaria</h2>
  <p>El lago es el punto. Benbrook Lake y Dutch Branch Park anclan la recreaci&oacute;n gratuita del pueblo &mdash; pesca, campamento, canchas y campos &mdash; y el lado oeste no tiene un activo exterior m&aacute;s grande. Quien trabaja en Lockheed o el lado oeste maneja 12&ndash;20 minutos a la planta contra el tr&aacute;fico del suroeste de Fort Worth, en lugar de pelear la I-30. La textura es asentada, no de estreno: es el pueblo-equilibrio del corredor, mitad propietarios y mitad inquilinos, no un frente de crecimiento planeado como <a href="/es/guias/vivir-en-walsh">Walsh</a>.</p>
</section>

<section>
  <h2>4 &middot; La decisi&oacute;n</h2>
  <p><strong>Benbrook conviene</strong> a compradores fuera del alcance de la banda de Aledo que a&uacute;n quieren el paquete familiar; a trabajadores de Lockheed y el lado oeste que valoran el trayecto corto; a inquilinos que quieren casa y no complejo; y a hogares en &ldquo;a&ntilde;o de exploraci&oacute;n,&rdquo; rentando el vecindario que podr&iacute;an comprar. <strong>Estira hacia Aledo</strong> si lo que compras es espec&iacute;ficamente el distrito &mdash; Aledo ISD obtuvo A (92) en 2026, cada plantel A o B.</p>
  <h3>Pr&oacute;ximos pasos</h3>
  <ol>
    <li>Corre la direcci&oacute;n, no el pueblo: confirma l&iacute;mites de ciudad y plantel asignado con Fort Worth ISD.</li>
    <li>Revisa las calificaciones por plantel en <a href="/es/escuelas/calificaciones-tea-2026">la p&aacute;gina TEA 2026</a> y en TXschools.gov.</li>
    <li>&iquest;Rentar primero? Pide tres cotizaciones por escrito &mdash; los portales no coinciden en la tendencia ahora mismo.</li>
    <li>&iquest;Comprar? Combina las bandas de arriba con <a href="/es/calculadora">la calculadora renta-o-compra</a>.</li>
  </ol>
</section>

<section>
  <h2>Fuentes</h2>
  <ul>
    <li>Bandas de venta y $/pie&sup2; &mdash; listados p&uacute;blicos, verano 2026, como se publica en <a href="/es/vender/benbrook">/es/vender/benbrook</a> y <a href="/es/vender/aledo">/es/vender/aledo</a>.</li>
    <li>Bandas de renta y la nota de tendencia &mdash; portales p&uacute;blicos, mayo&ndash;julio 2026, como se publica en <a href="/areas/benbrook">el archivo de zona de Benbrook</a> (en ingl&eacute;s).</li>
    <li>Calificaciones escolares &mdash; <a href="{SRC_TEA}" rel="nofollow">TEA, Sistema de Calificaciones 2026</a> (publicado el 14 de agosto de 2026; verificado el 2026-08-16).</li>
  </ul>
  <p><strong>Verificado el {VERIFIED}.</strong> Las bandas son rangos t&iacute;picos compilados de fuentes p&uacute;blicas, cambian sin aviso, y no son una valuaci&oacute;n de ninguna propiedad.</p>
</section>

<section>
  <h2>Sigue leyendo</h2>
  <p><a href="/es/guias/">las gu&iacute;as</a> &middot; <a href="/es/guias/vivir-en-aledo">vivir en Aledo</a> &middot; <a href="/es/guias/vivir-en-walsh">vivir en Walsh</a> &middot; <a href="/es/escuelas/">las escuelas</a> &middot; <a href="/es/relocate/">mudanza</a></p>
  <p><a href="{_url(EN_PATH)}" hreflang="en">Read this page in English &mdash; Living in Benbrook</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>&iquest;Sigues la brecha Benbrook&ndash;Aledo?</h2>
  <p>Actualizamos las bandas cuando cambian las compilaciones, y las tablas escolares cada ciclo de la TEA. La lista se entera cuando los n&uacute;meros se mueven.</p>
{lead_form(ES_PATH, "Av&iacute;senme cuando cambien los n&uacute;meros", renting=False, es=True, uid="lib")}
</section>
"""
    return page(
        path=ES_PATH,
        title="Vivir en Benbrook: la Jugada de Valor del Oeste &mdash; Precios, Escuelas y la Brecha con Aledo",
        description=("Benbrook contra Aledo con n&uacute;meros publicados: banda de $300K-$420K contra "
                     "$520K-$750K, una secundaria con A dentro de un distrito con C, el lago, y a "
                     "qui&eacute;n le conviene el intercambio."),
        h1="Vivir en Benbrook: la jugada de valor, con n&uacute;meros",
        eyebrow="LA GU&Iacute;A DEFINITIVA &middot; PRECIOS, ESCUELAS Y LA BRECHA CON ALEDO",
        lede=("La mayor parte de la textura familiar del lado oeste con una banda publicada unos $200K "
              "por debajo de la de Aledo &mdash; y, desde el ciclo 2026 de la TEA, una secundaria con A "
              "dentro de un distrito cuya C sigue malinterpretando la direcci&oacute;n."),
        crumb="<a href='/es/'>Inicio</a> / <a href='/es/guias/'>Gu&iacute;as</a> / Vivir en Benbrook",
        verified=VERIFIED,
        es=True,
        alt_path=EN_PATH,
        body=body,
        ld=[article_ld("Vivir en Benbrook: la jugada de valor, con n&uacute;meros",
                       f"https://westfwliving.com{_url(ES_PATH)}",
                       "Benbrook contra Aledo con n&uacute;meros publicados: precios, calificaciones TEA 2026 por plantel, y a qui&eacute;n le conviene.",
                       VERIFIED),
            faq_ld(FAQ_ES)],
    )


def build():
    return {EN_PATH: build_en(), ES_PATH: build_es()}
