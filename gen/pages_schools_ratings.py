#!/usr/bin/env python3
"""West FW Living — 2026 TEA accountability ratings for the west Fort Worth corridor.

Every figure in this module comes from the Texas Education Agency's 2026 Statewide
Multi-Year Ratings spreadsheet (the authoritative per-district and per-campus file
behind TXschools.gov), cross-checked against TEA's 2026 release announcement.
Nothing here is estimated, interpolated, or carried over from a prior year.

  Source A: TEA, "TEA Releases 2026 A-F Accountability Ratings on TXschools.gov,"
            released 2026-08-14.
  Source B: TEA, 2026 Statewide Multi-Year Ratings Spreadsheet (.xlsx).
  Verified: 2026-08-16.

Scores are TEA scaled scores, 0-100. "Not Rated" campuses are omitted from tables.
"""
from common import page, lead_form, article_ld, faq_ld, _url

VERIFIED = "2026-08-16"
RELEASED = "August 14, 2026"

EN_PATH = "/schools/tea-ratings-2026.html"
ES_PATH = "/es/escuelas/calificaciones-tea-2026.html"

SRC_RELEASE = "https://tea.texas.gov/about-tea/newsroom/tea-releases-2026-f-accountability-ratings-txschoolsgov"
SRC_SYSTEM = "https://tea.texas.gov/school-and-district-leaders/accountability/academic-accountability/performance-reporting/2026-accountability-rating-system"
SRC_LOOKUP = "https://txschools.gov"

# (district, 2026 letter, 2026 score, 2025 letter, 2025 score, corridor note)
DISTRICTS = [
    ("Aledo ISD", "A", 92, "A", 92, "Aledo, much of Willow Park, parts of Hudson Oaks and unincorporated Parker County"),
    ("Brock ISD", "A", 91, "A", 90, "Brock, southwest of Weatherford off I-20"),
    ("Peaster ISD", "B", 85, "B", 87, "Peaster, north of Weatherford"),
    ("Millsap ISD", "B", 82, "B", 82, "Millsap, west of Weatherford on I-20"),
    ("Weatherford ISD", "B", 80, "C", 77, "Weatherford and parts of Hudson Oaks"),
    ("Azle ISD", "C", 78, "C", 78, "Azle, north of Lake Worth"),
    ("Fort Worth ISD", "C", 77, "C", 73, "Fort Worth proper, including Benbrook and the Ridglea/Western Hills side"),
    ("Springtown ISD", "C", 77, "C", 76, "Springtown, north Parker County"),
    ("Eagle Mt-Saginaw ISD", "C", 77, "C", 78, "Northwest Tarrant County"),
    ("White Settlement ISD", "C", 75, "C", 73, "White Settlement, just west of the I-30 / Loop 820 split"),
    ("Lake Worth ISD", "D", 69, "D", 66, "Lake Worth, north of White Settlement"),
]

# (campus, 2026 letter, 2026 score, 2025 letter, 2025 score)
ALEDO_CAMPUSES = [
    ("Aledo High School", "A", 93, "A", 93),
    ("Don R. Daniel Ninth Grade Campus", "A", 93, "A", 91),
    ("Aledo Middle School", "A", 92, "B", 89),
    ("McAnally Middle School", "A", 93, "A", 92),
    ("Stuard Elementary", "A", 93, "A", 95),
    ("Lynn McKinney Elementary", "A", 92, "A", 92),
    ("Vandagriff Elementary", "A", 91, "A", 93),
    ("Coder Elementary", "A", 91, "A", 93),
    ("Annetta Elementary", "A", 90, "B", 89),
    ("Walsh Elementary", "B", 89, "A", 94),
    ("McCall Elementary", "B", 88, "A", 93),
]

WEATHERFORD_CAMPUSES = [
    ("Weatherford High School", "B", 86, "B", 83),
    ("Tison Middle School", "B", 82, "D", 68),
    ("Hall Middle School", "C", 73, "C", 74),
    ("Martin Elementary", "B", 88, "B", 84),
    ("Austin Elementary", "B", 82, "B", 81),
    ("Ikard Elementary", "C", 74, "D", 67),
    ("Seguin Elementary", "C", 73, "C", 79),
    ("Wright Elementary", "C", 71, "C", 76),
    ("Curtis Elementary", "C", 70, "B", 85),
    ("Crockett Elementary", "D", 69, "D", 67),
]

BENBROOK_CAMPUSES = [
    ("Benbrook Middle/High School", "A", 90, "B", 85),
    ("Westpark Elementary", "A", 92, "A", 90),
    ("Benbrook Elementary", "B", 89, "A", 92),
    ("Luella Merrett Elementary", "B", 84, "B", 83),
    ("Ridglea Hills Elementary", "C", 79, "C", 75),
    ("Waverly Park Elementary", "C", 74, "B", 81),
    ("Western Hills High School", "C", 74, "D", 69),
    ("Western Hills Elementary", "C", 73, "D", 63),
]

WHITE_SETTLEMENT_CAMPUSES = [
    ("Brewer High School", "B", 82, "C", 76),
    ("Fine Arts Academy at Tannahill", "C", 77, "A", 91),
    ("Brewer Middle School", "C", 76, "C", 74),
    ("West Early Learners Academy", "C", 75, "C", 73),
    ("North Elementary", "C", 74, "B", 80),
    ("Blue Haze Elementary", "D", 61, "D", 69),
    ("Liberty Elementary", "F", 55, "D", 67),
]


def _delta(cur_l, cur_s, prev_l, prev_s):
    """Human-readable year-over-year movement."""
    if prev_l in (None, "", "None"):
        return "—"
    if cur_l != prev_l:
        arrow = "&uarr;" if cur_s > prev_s else "&darr;"
        return f"{arrow} from {prev_l} ({prev_s})"
    d = cur_s - prev_s
    if d == 0:
        return f"held {prev_l} ({prev_s})"
    return f"{'+' if d > 0 else ''}{d} pts vs {prev_s}"


def _dtable(rows, es=False):
    head = ("<tr><th>Distrito</th><th>2026</th><th>Puntaje</th><th>Cambio vs 2025</th><th>Cubre, a grandes rasgos</th></tr>"
            if es else
            "<tr><th>District</th><th>2026</th><th>Score</th><th>Change vs 2025</th><th>Roughly covers</th></tr>")
    body = "".join(
        f"<tr><td><strong>{n}</strong></td><td><span class='tag'>{l}</span></td>"
        f"<td class='money'>{s}</td><td>{_delta(l, s, pl, ps)}</td><td>{note}</td></tr>"
        for n, l, s, pl, ps, note in rows)
    return f"<table>{head}{body}</table>"


def _ctable(rows, es=False):
    head = ("<tr><th>Plantel</th><th>2026</th><th>Puntaje</th><th>Cambio vs 2025</th></tr>"
            if es else
            "<tr><th>Campus</th><th>2026</th><th>Score</th><th>Change vs 2025</th></tr>")
    body = "".join(
        f"<tr><td>{n}</td><td><span class='tag'>{l}</span></td>"
        f"<td class='money'>{s}</td><td>{_delta(l, s, pl, ps)}</td></tr>"
        for n, l, s, pl, ps in rows)
    return f"<table>{head}{body}</table>"


FAQ_EN = [
    ("When did TEA release the 2026 accountability ratings?",
     f"TEA published the 2026 A-F accountability ratings on {RELEASED} at TXschools.gov. "
     "They rated 1,202 districts and 9,105 campuses."),
    ("What rating did Aledo ISD get in 2026?",
     "Aledo ISD earned an A with a scaled score of 92, the same letter and score it earned in 2025."),
    ("Did Weatherford ISD's rating change in 2026?",
     "Yes. Weatherford ISD moved from a C (77) in 2025 to a B (80) in 2026."),
    ("Does a district's A rating mean my address is zoned to an A campus?",
     "No. District and campus ratings are separate, and attendance zones are set by the district "
     "and are address-specific. A district can hold an A while an individual campus rates lower. "
     "Verify the zoned campus for a specific address with the district before you sign or close."),
    ("Do these ratings describe the current school year?",
     "No. The 2026 ratings describe performance in the school year that just ended. They are a "
     "record of past results, not a forecast."),
]

FAQ_ES = [
    ("¿Cuándo publicó la TEA las calificaciones de 2026?",
     "La TEA publicó las calificaciones A-F de 2026 el 14 de agosto de 2026 en TXschools.gov. "
     "Calificó 1,202 distritos y 9,105 planteles."),
    ("¿Qué calificación obtuvo Aledo ISD en 2026?",
     "Aledo ISD obtuvo una A con un puntaje de 92, la misma letra y el mismo puntaje que en 2025."),
    ("¿Cambió la calificación de Weatherford ISD?",
     "Sí. Weatherford ISD pasó de C (77) en 2025 a B (80) en 2026."),
    ("Si el distrito tiene A, ¿mi dirección queda en un plantel con A?",
     "No necesariamente. Las calificaciones del distrito y del plantel son distintas, y las zonas "
     "escolares dependen de la dirección exacta. Verifica el plantel asignado con el distrito antes "
     "de firmar o cerrar."),
]


def build_en():
    body = f"""<section>
  <h2 id="short-answer">The short answer</h2>
  <p>The Texas Education Agency released its 2026 A&ndash;F accountability ratings on <strong>{RELEASED}</strong>, covering 1,202 districts and 9,105 campuses statewide (<a href="{SRC_RELEASE}" rel="nofollow">TEA release</a>). For the west Fort Worth corridor, three things actually changed:</p>
  <ul>
    <li><strong>Aledo ISD held its A</strong> &mdash; 92 for the second year running, and the highest district score in the corridor.</li>
    <li><strong>Weatherford ISD moved up a letter</strong>, from a C (77) to a <strong>B (80)</strong> &mdash; the corridor's biggest district-level change.</li>
    <li><strong>Benbrook Middle/High School moved from a B to an A</strong> (90), inside a Fort Worth ISD that improved four points but stayed a C.</li>
  </ul>
  <p class="tag">Verified {VERIFIED} against TEA's 2026 ratings data</p>
</section>

<section>
  <h2>Every corridor district, rated</h2>
  <p>Districts a west-side move realistically puts you in, ranked by 2026 score. Scores are TEA scaled scores out of 100.</p>
  {_dtable(DISTRICTS)}
  <p>Source: <a href="{SRC_SYSTEM}" rel="nofollow">TEA 2026 Statewide Multi-Year Ratings</a>. The &ldquo;roughly covers&rdquo; column is orientation only &mdash; district boundaries and attendance zones are address-specific and are set by the districts, not by city limits. Willow Park is genuinely split between Aledo ISD and Weatherford ISD, and Hudson Oaks varies by address.</p>
</section>

<section>
  <h2>Aledo ISD, campus by campus</h2>
  <p>The district most west-side buyers are actually shopping for. Every campus rated A or B in 2026, but the year-over-year column is the honest part &mdash; two elementaries slipped a letter while two campuses gained one.</p>
  {_ctable(ALEDO_CAMPUSES)}
  <p>Walsh Elementary (89) and McCall Elementary (88) both moved from an A to a B this cycle. Both remain B campuses in an A district, and a single year's movement of four to five points is a thin basis for a housing decision &mdash; but if you are buying specifically <em>because</em> of a campus, this is the number to know rather than discover later. McCall is the Willow Park&ndash;side campus; Walsh serves the Walsh community.</p>
</section>

<section>
  <h2>Weatherford ISD's move from C to B</h2>
  <p>The corridor's biggest district story. Weatherford ISD gained three points and a letter, and the campus detail shows where it came from &mdash; Tison Middle School jumped from a D (68) to a B (82).</p>
  {_ctable(WEATHERFORD_CAMPUSES)}
  <p>The spread inside the district is wide: Martin Elementary at 88 and Crockett Elementary at 69 are both Weatherford ISD. If you are looking at Hudson Oaks or Weatherford proper, the district letter is the least useful number on this page &mdash; the zoned campus is the one that matters.</p>
</section>

<section>
  <h2>Benbrook and the Fort Worth ISD side</h2>
  <p>Benbrook is served by Fort Worth ISD, which is why its schools often get read through a district-level C that does not describe them. Benbrook Middle/High School rated an <strong>A (90)</strong> in 2026, up from a B.</p>
  {_ctable(BENBROOK_CAMPUSES)}
  <p>Fort Worth ISD as a district scored 77 (a C), up from 73 in 2025. Two independent reports of the release put the district's improvement in the same place (<a href="https://www.fox4news.com/news/texas-school-ratings-2026" rel="nofollow">FOX 4</a>). For a Benbrook address, the campus rows above describe the schools far better than the district letter does.</p>
</section>

<section>
  <h2>White Settlement ISD</h2>
  <p>West of the I-30 / Loop 820 split, White Settlement ISD held a C (75). The district's range this cycle is the widest in the corridor.</p>
  {_ctable(WHITE_SETTLEMENT_CAMPUSES)}
  <p>Brewer High School gained a letter, moving to a B (82). Liberty Elementary rated an F (55), down from a D. TEA publishes campus ratings precisely so families can see this level of detail; a low rating triggers state support requirements for the campus rather than describing the children in it. If you are renting or buying into a specific White Settlement zone, look up the exact campus rather than the district.</p>
</section>

<section>
  <h2>Who this actually applies to</h2>
  <p><strong>Buyers</strong> shopping a corridor address where the school zone is part of the price &mdash; particularly in Willow Park, Hudson Oaks, Aledo and Walsh, where &ldquo;Aledo ISD&rdquo; carries a real premium. <strong>Renters</strong> comparing complexes along I-30 and I-20 whose leasing materials name a district. <strong>Families relocating</strong> into west Fort Worth who need a starting map before they can shortlist neighborhoods.</p>
  <p>It applies less cleanly than people expect. A rating describes a school year that has already ended, at a campus your address may or may not feed. It is a useful input and a poor conclusion.</p>
</section>

<section>
  <h2>What a rating does not tell you</h2>
  <p>Three limits worth holding onto:</p>
  <ul>
    <li><strong>A district letter is not a campus letter.</strong> Aledo ISD is an A district containing two B elementaries; Fort Worth ISD is a C district containing an A middle/high school in Benbrook.</li>
    <li><strong>A campus letter is not your campus.</strong> Attendance zones are drawn to the address, sometimes to the street, and districts redraw them as the corridor grows. A leasing office or listing sheet naming a district is not a zoning document.</li>
    <li><strong>A rating is a rear-view number.</strong> It reflects the year that ended, and a single cycle's four-point move is noise as often as it is signal. Two or three years of direction is the more honest read, which is why the change column above exists.</li>
  </ul>
</section>

<section>
  <h2>Next steps</h2>
  <ol>
    <li>Look up the exact address on <a href="{SRC_LOOKUP}" rel="nofollow">TXschools.gov</a>, which maps ratings to campuses and lets you search by address.</li>
    <li>Confirm the zoned campus in writing with the district itself &mdash; that is the only answer that binds.</li>
    <li>If you are renting, read <a href="/schools/willow-park-school-zones">Willow Park school zones, decoded for renters</a> before you sign; the split-district problem is real in that pocket.</li>
    <li>If you are buying, pair this with the district hubs: <a href="/schools/aledo-isd/">Aledo ISD</a>, <a href="/schools/weatherford-isd/">Weatherford ISD</a>, <a href="/schools/brock-isd/">Brock ISD</a>.</li>
  </ol>
</section>

<section>
  <h2>Sources</h2>
  <ul>
    <li>Texas Education Agency &mdash; <a href="{SRC_RELEASE}" rel="nofollow">2026 A&ndash;F accountability ratings release</a>, {RELEASED}.</li>
    <li>Texas Education Agency &mdash; <a href="{SRC_SYSTEM}" rel="nofollow">2026 Accountability Rating System</a>, including the 2026 Statewide Multi-Year Ratings spreadsheet used for every district and campus figure above.</li>
    <li>Campus and district lookup &mdash; <a href="{SRC_LOOKUP}" rel="nofollow">TXschools.gov</a>.</li>
  </ul>
  <p><strong>Verified {VERIFIED}.</strong> Ratings describe the school year that just ended and are republished by TEA annually; this page is rebuilt when the next cycle lands.</p>
</section>

<section>
  <h2>Keep reading</h2>
  <p><a href="/schools/">the schools hub</a> &middot; <a href="/neighborhoods/">neighborhoods</a> &middot; <a href="/relocate/">the relocation hub</a> &middot; <a href="/buy/">the buyer's guide</a> &middot; <a href="/guides/living-in-aledo">living in Aledo</a> &middot; <a href="/guides/living-in-walsh">living in Walsh</a></p>
  <p><a href="{_url(ES_PATH)}" hreflang="es">Lee esta p&aacute;gina en espa&ntilde;ol &mdash; Calificaciones TEA 2026</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>Want the next ratings cycle when it lands?</h2>
  <p>We rebuild this page every time TEA publishes. The early list gets a note when the corridor numbers change &mdash; no other mail.</p>
{lead_form(EN_PATH, "Send me the next update", renting=False, es=False, uid="tea")}
</section>
"""
    return page(
        path=EN_PATH,
        title="2026 TEA School Ratings: Aledo, Weatherford, Benbrook &amp; West Fort Worth",
        description=("The 2026 A-F accountability ratings for every west Fort Worth corridor district and "
                     "campus: Aledo ISD holds an A, Weatherford ISD moves to a B, Benbrook Middle/High "
                     "earns an A. Verified against TEA data."),
        h1="2026 TEA ratings for west Fort Worth schools",
        eyebrow="RELEASED AUGUST 14, 2026 &middot; EVERY CORRIDOR DISTRICT AND CAMPUS",
        lede=("TEA published this year's A&ndash;F ratings two days ago. Here is what they say about the "
              "districts and campuses a west-side move actually puts you in &mdash; and the three limits "
              "that keep a letter grade from being a housing decision."),
        crumb="<a href='/'>Home</a> / <a href='/schools/'>Schools</a> / 2026 TEA Ratings",
        verified=VERIFIED,
        es=False,
        alt_path=ES_PATH,
        body=body,
        ld=[article_ld("2026 TEA ratings for west Fort Worth schools",
                       f"https://westfwliving.com{EN_PATH}",
                       "The 2026 A-F accountability ratings for every west Fort Worth corridor district and campus.",
                       VERIFIED),
            faq_ld(FAQ_EN)],
    )


def build_es():
    body = f"""<section>
  <h2>La respuesta corta</h2>
  <p>La Agencia de Educaci&oacute;n de Texas (TEA) public&oacute; sus calificaciones A&ndash;F de 2026 el <strong>14 de agosto de 2026</strong>, cubriendo 1,202 distritos y 9,105 planteles en todo el estado (<a href="{SRC_RELEASE}" rel="nofollow">anuncio de la TEA</a>). Para el corredor oeste de Fort Worth, cambiaron tres cosas:</p>
  <ul>
    <li><strong>Aledo ISD mantuvo su A</strong> &mdash; 92 por segundo a&ntilde;o, el puntaje m&aacute;s alto del corredor.</li>
    <li><strong>Weatherford ISD subi&oacute; de letra</strong>, de C (77) a <strong>B (80)</strong>.</li>
    <li><strong>Benbrook Middle/High School pas&oacute; de B a A</strong> (90), dentro de un Fort Worth ISD que mejor&oacute; cuatro puntos pero sigue en C.</li>
  </ul>
  <p class="tag">Verificado el {VERIFIED} con los datos de la TEA</p>
</section>

<section>
  <h2>Cada distrito del corredor</h2>
  <p>Los distritos en los que realmente cae una mudanza al lado oeste, ordenados por puntaje 2026. Los puntajes son de la TEA, sobre 100.</p>
  {_dtable(DISTRICTS, es=True)}
  <p>Fuente: <a href="{SRC_SYSTEM}" rel="nofollow">TEA, calificaciones multianuales 2026</a>. La columna &ldquo;cubre&rdquo; es solo orientaci&oacute;n &mdash; los l&iacute;mites y las zonas escolares dependen de la direcci&oacute;n exacta y los fijan los distritos, no los l&iacute;mites de la ciudad. Willow Park est&aacute; dividido entre Aledo ISD y Weatherford ISD, y Hudson Oaks var&iacute;a seg&uacute;n la direcci&oacute;n.</p>
</section>

<section>
  <h2>Aledo ISD, plantel por plantel</h2>
  <p>El distrito que la mayor&iacute;a de los compradores del lado oeste busca. Todos los planteles calificaron A o B en 2026, pero la columna de cambio es la parte honesta: dos primarias bajaron una letra.</p>
  {_ctable(ALEDO_CAMPUSES, es=True)}
  <p>Walsh Elementary (89) y McCall Elementary (88) pasaron de A a B en este ciclo. Siguen siendo planteles B dentro de un distrito A, y el movimiento de un solo a&ntilde;o es una base delgada para decidir una compra &mdash; pero si compras <em>por</em> un plantel espec&iacute;fico, este es el n&uacute;mero que conviene saber antes y no despu&eacute;s.</p>
</section>

<section>
  <h2>Weatherford ISD: de C a B</h2>
  <p>La historia m&aacute;s grande del corredor. Weatherford ISD gan&oacute; tres puntos y una letra, y el detalle por plantel muestra de d&oacute;nde vino: Tison Middle School salt&oacute; de D (68) a B (82).</p>
  {_ctable(WEATHERFORD_CAMPUSES, es=True)}
  <p>La diferencia dentro del distrito es amplia: Martin Elementary con 88 y Crockett Elementary con 69 son ambos Weatherford ISD. Si miras Hudson Oaks o Weatherford, la letra del distrito es el n&uacute;mero menos &uacute;til de esta p&aacute;gina &mdash; lo que importa es el plantel asignado a tu direcci&oacute;n.</p>
</section>

<section>
  <h2>Benbrook y el lado de Fort Worth ISD</h2>
  <p>Benbrook pertenece a Fort Worth ISD, y por eso sus escuelas suelen leerse a trav&eacute;s de una C de distrito que no las describe. Benbrook Middle/High School obtuvo una <strong>A (90)</strong> en 2026.</p>
  {_ctable(BENBROOK_CAMPUSES, es=True)}
  <p>Fort Worth ISD como distrito obtuvo 77 (C), arriba de 73 en 2025. Para una direcci&oacute;n en Benbrook, las filas de arriba describen las escuelas mucho mejor que la letra del distrito.</p>
</section>

<section>
  <h2>White Settlement ISD</h2>
  <p>Al oeste de la divisi&oacute;n I-30 / Loop 820, White Settlement ISD mantuvo una C (75), con el rango m&aacute;s amplio del corredor.</p>
  {_ctable(WHITE_SETTLEMENT_CAMPUSES, es=True)}
  <p>Brewer High School subi&oacute; a B (82). Liberty Elementary obtuvo F (55). La TEA publica calificaciones por plantel precisamente para que las familias vean este nivel de detalle; una calificaci&oacute;n baja obliga al estado a dar apoyo al plantel. Si rentas o compras en una zona de White Settlement, consulta el plantel exacto, no el distrito.</p>
</section>

<section>
  <h2>A qui&eacute;n le sirve</h2>
  <p><strong>Compradores</strong> que buscan una direcci&oacute;n donde la zona escolar es parte del precio &mdash; sobre todo en Willow Park, Hudson Oaks, Aledo y Walsh. <strong>Inquilinos</strong> que comparan complejos sobre la I-30 y la I-20 cuyos folletos mencionan un distrito. <strong>Familias que se mudan</strong> al oeste de Fort Worth y necesitan un mapa inicial.</p>
</section>

<section>
  <h2>Lo que una calificaci&oacute;n no te dice</h2>
  <ul>
    <li><strong>La letra del distrito no es la del plantel.</strong> Aledo ISD es distrito A con dos primarias B; Fort Worth ISD es distrito C con una secundaria A en Benbrook.</li>
    <li><strong>La letra del plantel no es la de tu plantel.</strong> Las zonas se trazan por direcci&oacute;n, a veces por calle, y los distritos las redibujan conforme crece el corredor.</li>
    <li><strong>Es un n&uacute;mero del retrovisor.</strong> Refleja el a&ntilde;o que termin&oacute;. Dos o tres a&ntilde;os de direcci&oacute;n dicen m&aacute;s que un ciclo.</li>
  </ul>
</section>

<section>
  <h2>Pr&oacute;ximos pasos</h2>
  <ol>
    <li>Busca la direcci&oacute;n exacta en <a href="{SRC_LOOKUP}" rel="nofollow">TXschools.gov</a>.</li>
    <li>Confirma por escrito el plantel asignado con el distrito &mdash; esa es la &uacute;nica respuesta que obliga.</li>
    <li>Si rentas, lee <a href="/schools/willow-park-school-zones">las zonas escolares de Willow Park</a> antes de firmar.</li>
    <li>Si compras, usa los centros de distrito: <a href="/schools/aledo-isd/">Aledo ISD</a>, <a href="/schools/weatherford-isd/">Weatherford ISD</a>, <a href="/schools/brock-isd/">Brock ISD</a>.</li>
  </ol>
</section>

<section>
  <h2>Fuentes</h2>
  <ul>
    <li>TEA &mdash; <a href="{SRC_RELEASE}" rel="nofollow">anuncio de las calificaciones A&ndash;F 2026</a>, 14 de agosto de 2026.</li>
    <li>TEA &mdash; <a href="{SRC_SYSTEM}" rel="nofollow">Sistema de Calificaciones 2026</a>, incluida la hoja multianual usada para cada cifra.</li>
    <li>Consulta por plantel &mdash; <a href="{SRC_LOOKUP}" rel="nofollow">TXschools.gov</a>.</li>
  </ul>
  <p><strong>Verificado el {VERIFIED}.</strong></p>
</section>

<section>
  <h2>Sigue leyendo</h2>
  <p><a href="/es/escuelas/">el centro de escuelas</a> &middot; <a href="/es/relocate/">mudanza</a> &middot; <a href="/es/comprar/">comprar casa</a> &middot; <a href="/es/vecindarios/">vecindarios</a></p>
  <p><a href="{_url(EN_PATH)}" hreflang="en">Read this page in English &mdash; 2026 TEA school ratings</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>&iquest;Quieres el pr&oacute;ximo ciclo de calificaciones?</h2>
  <p>Reconstruimos esta p&aacute;gina cada vez que la TEA publica. La lista recibe un aviso cuando cambian los n&uacute;meros del corredor.</p>
{lead_form(ES_PATH, "Av&iacute;senme del pr&oacute;ximo cambio", renting=False, es=True, uid="tea")}
</section>
"""
    return page(
        path=ES_PATH,
        title="Calificaciones TEA 2026: Aledo, Weatherford, Benbrook y el Oeste de Fort Worth",
        description=("Las calificaciones A-F de 2026 para cada distrito y plantel del corredor oeste de Fort "
                     "Worth: Aledo ISD mantiene su A, Weatherford ISD sube a B, Benbrook Middle/High obtiene A."),
        h1="Calificaciones TEA 2026 para las escuelas del oeste de Fort Worth",
        eyebrow="PUBLICADAS EL 14 DE AGOSTO DE 2026 &middot; CADA DISTRITO Y PLANTEL",
        lede=("La TEA public&oacute; las calificaciones A&ndash;F de este a&ntilde;o hace dos d&iacute;as. Esto es lo que dicen "
              "sobre los distritos y planteles donde realmente cae una mudanza al lado oeste."),
        crumb="<a href='/es/'>Inicio</a> / <a href='/es/escuelas/'>Escuelas</a> / Calificaciones TEA 2026",
        verified=VERIFIED,
        es=True,
        alt_path=EN_PATH,
        body=body,
        ld=[article_ld("Calificaciones TEA 2026 para las escuelas del oeste de Fort Worth",
                       f"https://westfwliving.com{ES_PATH}",
                       "Las calificaciones A-F de 2026 para cada distrito y plantel del corredor oeste de Fort Worth.",
                       VERIFIED),
            faq_ld(FAQ_ES)],
    )


def build():
    return {EN_PATH: build_en(), ES_PATH: build_es()}
