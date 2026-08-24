#!/usr/bin/env python3
"""West FW Living — Working at Lockheed Martin Fort Worth: relocation hub (EN + ES).

Flagship hub of the Lockheed cluster. Answers the broad relocation question
("I'm coming to work at the plant — where should I live?") and routes into the
renter spoke (/guides/apartments-near-lockheed-martin-fort-worth), the buyer
spoke (/guides/buying-a-home-near-lockheed-martin-fort-worth), commute, family,
military and decision-support paths. Every figure is reused from published,
sourced site data: rent bands from the renter hub (public listings, July 2026),
sale bands from the sell-side files (summer 2026), TEA 2026 ratings, homestead
dollars at adopted 2025 rates. Nothing newly estimated.
"""
from common import page, lead_form, article_ld, faq_ld, _url

VERIFIED = "2026-08-24"

EN_PATH = "/relocate/working-at-lockheed-martin-fort-worth.html"
ES_PATH = "/es/relocate/trabajar-en-lockheed-martin-fort-worth.html"

# (pocket, plant drive, renting band, buying band) — all previously published.
MAP = [
    ("White Settlement", "5&ndash;12 min", "$900&ndash;$1,200 (1BR)", "$230K&ndash;$320K"),
    ("West Fort Worth (I-30 corridor)", "10&ndash;18 min", "$1,100&ndash;$1,450 (1BR)", "&mdash;"),
    ("Benbrook", "12&ndash;20 min", "$1,100&ndash;$1,400 (1BR)", "$300K&ndash;$420K"),
    ("Willow Park / Hudson Oaks", "20&ndash;30 min", "$1,150&ndash;$1,500 (1BR)", "$430K&ndash;$600K"),
    ("Aledo", "25&ndash;35 min", "$1,400&ndash;$1,900 (houses)", "$520K&ndash;$750K"),
]

MAP_ES = [
    ("White Settlement", "5&ndash;12 min", "$900&ndash;$1,200 (1 rec.)", "$230K&ndash;$320K"),
    ("Oeste de Fort Worth (corredor I-30)", "10&ndash;18 min", "$1,100&ndash;$1,450 (1 rec.)", "&mdash;"),
    ("Benbrook", "12&ndash;20 min", "$1,100&ndash;$1,400 (1 rec.)", "$300K&ndash;$420K"),
    ("Willow Park / Hudson Oaks", "20&ndash;30 min", "$1,150&ndash;$1,500 (1 rec.)", "$430K&ndash;$600K"),
    ("Aledo", "25&ndash;35 min", "$1,400&ndash;$1,900 (casas)", "$520K&ndash;$750K"),
]


def _map_table(rows, es=False):
    head = ("<tr><th>Zona</th><th>A la planta</th><th>Rentar (t&iacute;pico)</th><th>Comprar (banda)</th></tr>" if es else
            "<tr><th>Pocket</th><th>Plant drive</th><th>Renting (typical)</th><th>Buying (band)</th></tr>")
    body = "".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td>"
                   f"<td class='money'>{c}</td><td class='money'>{d}</td></tr>"
                   for a, b, c, d in rows)
    return f"<div class='table-scroll'><table>{head}{body}</table></div>"


FAQ_EN = [
    ("I'm relocating to work at Lockheed Martin Fort Worth — where should I live?",
     "Start with three questions, in order: rent or buy, how close to the plant, and which "
     "school situation. The plant is on Fort Worth's west side, so short commutes and "
     "affordable pockets point the same direction - White Settlement and west Fort Worth for "
     "the shortest drives, Benbrook for the lake and an A-rated middle/high, Willow Park/"
     "Hudson Oaks and Aledo for Parker County schools at a longer drive."),
    ("Should I rent first or buy on arrival?",
     "A scout year renting in the pocket you'd buy in is a legitimate strategy, and this "
     "year's concessions make it cheap to try. If your credit is solid and you know the "
     "pocket, buying works too - the rent-vs-buy calculator compares a 12-month all-in rent "
     "total against ownership at current published bands."),
    ("How does NAS JRB relate to the Lockheed housing search?",
     "The plant and the base share a fence line, so the housing map is nearly identical. "
     "Military households add two layers: BAH math and the jet-noise contours - both have "
     "dedicated guides on this site."),
    ("What do the commutes actually look like at shift times?",
     "Commute times are estimates and vary substantially by departure hour: very early starts "
     "generally see lighter traffic than the metro peak, while standard office hours face the "
     "full I-30/820 interchange. Drive your real route at your real report time once before "
     "signing anything."),
]

FAQ_ES = [
    ("Me mudo para trabajar en Lockheed Martin Fort Worth — ¿dónde debería vivir?",
     "Empieza con tres preguntas, en orden: rentar o comprar, qué tan cerca de la planta, y "
     "qué situación escolar. La planta está en el lado oeste de Fort Worth, así que los "
     "trayectos cortos y las zonas accesibles apuntan en la misma dirección."),
    ("¿Rentar primero o comprar al llegar?",
     "Un año de exploración rentando en la zona donde comprarías es una estrategia legítima, "
     "y las concesiones de este año lo hacen barato. Si tu crédito es sólido y conoces la "
     "zona, comprar también funciona - la calculadora renta-o-compra corre los números."),
    ("¿Qué tiene que ver NAS JRB con la búsqueda de vivienda para Lockheed?",
     "La planta y la base comparten barda, así que el mapa de vivienda es casi idéntico. Los "
     "hogares militares suman dos capas: el cálculo del BAH y los contornos de ruido de "
     "aviones - ambos con guías dedicadas en este sitio."),
]


def build_en():
    body = f"""<section>
  <h2 id="short-answer">The short answer</h2>
  <p>The plant is on Fort Worth's <strong>west side</strong>, which makes this one of the few
  big-employer relocations in DFW where the short commutes and the affordable pockets point the
  <em>same direction</em>. Your search is three decisions, in order: <strong>rent or buy</strong>,
  <strong>how close to the gate</strong>, and <strong>which schools</strong>. This page routes
  all three; the two deep guides &mdash; <a href="/guides/apartments-near-lockheed-martin-fort-worth">renting
  near the plant</a> and <a href="/guides/buying-a-home-near-lockheed-martin-fort-worth">buying near
  the plant</a> &mdash; carry the numbers.</p>
  <p class="tag">Verified {VERIFIED} &middot; all figures reused from this site's published, sourced pages</p>
</section>

<section>
  <h2>The one-table map</h2>
  {_map_table(MAP)}
  <p>Rent bands compiled from public listings (July 2026, per <a href="/guides/apartments-near-lockheed-martin-fort-worth">the
  renter's guide</a>); sale bands from the published sell-side files (summer 2026, per
  <a href="/guides/buying-a-home-near-lockheed-martin-fort-worth">the buyer's ladder</a>). Both move
  &mdash; treat them as the shape of the market, not a quote. West Fort Worth's I-30 corridor is a
  renter-volume play with little single-family inventory tracked here, hence the missing buy band.</p>
</section>

<section>
  <h2>Path one: rent near the plant</h2>
  <p>Best when you're new to the area, on a start date, or running a deliberate scout year.
  <a href="/guides/apartments-near-lockheed-martin-fort-worth">The apartments guide</a> maps every
  pocket with estimated off-peak drive times; <a href="/rentals/apartments-76108">the 76108 file</a> covers
  the closest-to-gate ZIP, and the named communities people ask about have full field files &mdash;
  <a href="/complexes/westpoint-at-scenic-vista">Westpoint at Scenic Vista</a> and
  <a href="/complexes/chapel-creek-cottages">Chapel Creek Cottages</a> on the west side.
  Need a bridge, not a lease? <a href="/guides/short-term-leases-weatherford-willow-park">Short-term
  options</a>. And check <a href="/specials">this month's verified specials</a> before touring &mdash;
  several corridor communities are running 6&ndash;8 weeks free.</p>
</section>

<section>
  <h2>Path two: buy near the plant</h2>
  <p><a href="/guides/buying-a-home-near-lockheed-martin-fort-worth">The buyer's ladder</a> runs the
  four pockets rung by rung &mdash; published bands, $/sqft, and the 2026 TEA rating attached to each.
  File <a href="/buy/homestead-exemption">the homestead exemption</a> the week you close (worth
  roughly $1,441&ndash;$1,690/yr across these districts at adopted 2025 rates), and if you're a
  veteran or transitioning from the base next door, <a href="/buy/va-loans-fort-worth">the VA-loans
  guide</a> covers the west-side specifics.</p>
</section>

<section>
  <h2>Path three: the commute decides the pocket</h2>
  <p>The hour you drive matters as much as the miles: mapping estimates for very early starts put
  even the Parker County runs well under their rush-hour worst case, while standard office hours
  face the full I-30/820 interchange &mdash; these are estimates, not measurements.
  <a href="/guides/apartments-near-lockheed-martin-fort-worth">The shift-math section of the renter's
  guide</a> works this in detail, and every tracked community has its own drive-time file (e.g.
  <a href="/commutes/westpoint-at-scenic-vista">from Westpoint</a>,
  <a href="/commutes/olympus-willow-park">from Olympus Willow Park</a>). Choosing a side of town
  from scratch? <a href="/guides/moving-to-fort-worth-which-side">Fort Worth sorts by direction</a>.</p>
</section>

<section>
  <h2>Moving with a family</h2>
  <p>Schools decide addresses out here. <a href="/schools/tea-ratings-2026">The 2026 TEA ratings
  page</a> maps every corridor district and campus; <a href="/schools/willow-park-school-zones">the
  school-zone decoder</a> shows how to verify a specific address, and the definitive guides &mdash;
  <a href="/guides/living-in-benbrook">Benbrook</a>, <a href="/guides/living-in-aledo">Aledo</a>,
  <a href="/guides/living-in-walsh">Walsh</a> &mdash; carry the neighborhood trade-offs.
  <a href="/guides/relocating-to-west-fort-worth-family-guide">The family relocation playbook</a>
  sequences the whole thing.</p>
</section>

<section>
  <h2>Military crossover</h2>
  <p>The plant shares a fence line with <strong>NAS JRB Fort Worth</strong>, so the two housing maps
  are nearly identical. <a href="/guides/apartments-near-nas-jrb-fort-worth">The NAS JRB guide</a> is
  the base-side mirror of this page; <a href="/military/bah-fort-worth">the BAH tables</a> price the
  pockets against the allowance, and <a href="/military/jrb-noise">the jet-noise map</a> is worth ten
  minutes before you pick a street on the near west side.</p>
</section>

<section>
  <h2>Decide, then move</h2>
  <p>Two finalists? <a href="/compare/">Put them side by side</a> &mdash;
  <a href="/compare/willow-park-vs-hudson-oaks">Willow Park vs Hudson Oaks</a> and
  <a href="/compare/aledo-vs-weatherford">Aledo vs Weatherford</a> settle the two most common
  corridor face-offs. Not sure of the shortlist? <a href="/where-to-live">The Where-Should-I-Live
  matcher</a> builds one from your priorities. Rent-or-buy still open?
  <a href="/calculator">Thirty seconds of math</a>. And once the decision is made,
  <a href="/move/">the interactive move checklist</a> runs the relocation itself &mdash; six phases,
  progress saved as you go.</p>
</section>

<section>
  <h2>Keep reading</h2>
  <p><a href="/guides/apartments-near-lockheed-martin-fort-worth">apartments near Lockheed Martin</a> &middot;
  <a href="/guides/buying-a-home-near-lockheed-martin-fort-worth">the buyer's ladder</a> &middot;
  <a href="/guides/apartments-near-nas-jrb-fort-worth">NAS JRB housing</a> &middot;
  <a href="/relocate/">the relocation hub</a> &middot; <a href="/move/">the move checklist</a></p>
  <p><a href="{_url(ES_PATH)}" hreflang="es">Lee esta p&aacute;gina en espa&ntilde;ol &mdash; Trabajar en Lockheed Martin Fort Worth</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>Relocating on a start date?</h2>
  <p>Tell us when you land and we'll send the current specials, the pocket map, and the school
  timeline that matches your move &mdash; before the leasing offices open. No other mail.</p>
{lead_form(EN_PATH, "Send me the relocation brief", renting=False, es=False, uid="lkr")}
</section>
"""
    return page(
        path=EN_PATH,
        title="Working at Lockheed Martin Fort Worth: Housing & Relocation Guide (2026)",
        description=("Relocating to work at Lockheed Martin Fort Worth? The west-side housing map "
                     "in one page: rent vs buy paths, pocket-by-pocket drives, schools, NAS JRB "
                     "crossover, and the decision tools - built from published, sourced data."),
        h1="Working at Lockheed Martin Fort Worth: where to live",
        eyebrow="RELOCATION HUB &middot; THE PLANT, THE POCKETS &amp; THE PATHS",
        lede=("The plant is west, the affordable pockets are west, and the good schools are west "
              "&mdash; one of DFW's few relocations where everything points the same direction. "
              "Here's the whole housing decision, organized."),
        crumb="<a href='/'>Home</a> / <a href='/relocate/'>Relocate</a> / Working at Lockheed Martin",
        verified=VERIFIED,
        es=False,
        alt_path=ES_PATH,
        body=body,
        ld=[article_ld("Working at Lockheed Martin Fort Worth: Housing & Relocation Guide",
                       f"https://westfwliving.com{_url(EN_PATH)}",
                       "The west-side housing and relocation map for Lockheed Martin Fort Worth employees: rent and buy paths, commutes, schools, and NAS JRB crossover.",
                       VERIFIED),
            faq_ld(FAQ_EN)],
    )


def build_es():
    body = f"""<section>
  <h2 id="respuesta-corta">La respuesta corta</h2>
  <p>La planta est&aacute; en el <strong>lado oeste</strong> de Fort Worth, lo que hace de esta una
  de las pocas reubicaciones de gran empleador en DFW donde los trayectos cortos y las zonas
  accesibles apuntan en la <em>misma direcci&oacute;n</em>. Tu b&uacute;squeda son tres decisiones,
  en orden: <strong>rentar o comprar</strong>, <strong>qu&eacute; tan cerca de la planta</strong> y
  <strong>qu&eacute; escuelas</strong>. Esta p&aacute;gina organiza las tres; las dos gu&iacute;as
  profundas &mdash; <a href="/es/guias/apartamentos-cerca-de-lockheed-martin-fort-worth">rentar cerca
  de la planta</a> y <a href="/es/guias/comprar-casa-cerca-de-lockheed-martin-fort-worth">comprar
  cerca de la planta</a> &mdash; llevan los n&uacute;meros.</p>
  <p class="tag">Verificado {VERIFIED} &middot; cifras reutilizadas de p&aacute;ginas publicadas y con fuente de este sitio</p>
</section>

<section>
  <h2>El mapa en una tabla</h2>
  {_map_table(MAP_ES, es=True)}
  <p>Bandas de renta compiladas de listados p&uacute;blicos (julio 2026); bandas de venta de los
  archivos de venta publicados (verano 2026). Ambas se mueven &mdash; son la forma del mercado, no
  una cotizaci&oacute;n.</p>
</section>

<section>
  <h2>Camino uno: rentar cerca de la planta</h2>
  <p>Ideal si eres nuevo en el &aacute;rea o corres un a&ntilde;o de exploraci&oacute;n.
  <a href="/es/guias/apartamentos-cerca-de-lockheed-martin-fort-worth">La gu&iacute;a de
  apartamentos</a> mapea cada zona con tiempos estimados fuera de hora pico, y
  <a href="/es/especiales">los especiales verificados de este mes</a> incluyen 6&ndash;8 semanas
  gratis en varias comunidades del corredor.</p>
</section>

<section>
  <h2>Camino dos: comprar cerca de la planta</h2>
  <p><a href="/es/guias/comprar-casa-cerca-de-lockheed-martin-fort-worth">La escalera del
  comprador</a> recorre las cuatro zonas &mdash; bandas publicadas, $/pie&sup2; y la
  calificaci&oacute;n TEA 2026 de cada distrito. Presenta
  <a href="/es/comprar/exencion-homestead">la exenci&oacute;n homestead</a> la semana que cierres
  (vale unos $1,441&ndash;$1,690 al a&ntilde;o en estos distritos con tasas adoptadas de 2025).</p>
</section>

<section>
  <h2>Familia y escuelas</h2>
  <p>Las escuelas deciden direcciones aqu&iacute;.
  <a href="/es/escuelas/calificaciones-tea-2026">Las calificaciones TEA 2026</a> mapean cada
  distrito y plantel del corredor, y las gu&iacute;as definitivas &mdash;
  <a href="/es/guias/vivir-en-benbrook">Benbrook</a>, <a href="/es/guias/vivir-en-aledo">Aledo</a>,
  <a href="/es/guias/vivir-en-walsh">Walsh</a> &mdash; llevan los trade-offs.
  <a href="/es/guias/reubicacion-familiar-oeste-fort-worth">El manual de reubicaci&oacute;n
  familiar</a> ordena todo el proceso.</p>
</section>

<section>
  <h2>Cruce militar</h2>
  <p>La planta comparte barda con <strong>NAS JRB Fort Worth</strong>, as&iacute; que los dos mapas
  de vivienda son casi id&eacute;nticos.
  <a href="/es/guias/apartamentos-cerca-de-nas-jrb-fort-worth">La gu&iacute;a de NAS JRB</a> es el
  espejo de esta p&aacute;gina del lado de la base.</p>
</section>

<section>
  <h2>Decide, y luego m&uacute;date</h2>
  <p>&iquest;Dos finalistas? <a href="/compare/">Comp&aacute;ralos lado a lado</a>.
  &iquest;Renta o compra abierta a&uacute;n? <a href="/es/calculadora">Treinta segundos de
  matem&aacute;ticas</a>. Y con la decisi&oacute;n tomada,
  <a href="/es/relocate/">el centro de reubicaci&oacute;n</a> lleva la mudanza misma.</p>
</section>

<section>
  <h2>Sigue leyendo</h2>
  <p><a href="/es/guias/apartamentos-cerca-de-lockheed-martin-fort-worth">apartamentos cerca de Lockheed Martin</a> &middot;
  <a href="/es/guias/comprar-casa-cerca-de-lockheed-martin-fort-worth">comprar casa cerca de la planta</a> &middot;
  <a href="/es/relocate/">mudanza</a> &middot; <a href="/es/comprar/">la gu&iacute;a del comprador</a></p>
  <p><a href="{_url(EN_PATH)}" hreflang="en">Read this page in English &mdash; Working at Lockheed Martin Fort Worth</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>&iquest;Te mudas con fecha de inicio?</h2>
  <p>Dinos cu&aacute;ndo llegas y te enviamos los especiales vigentes, el mapa de zonas y el
  calendario escolar que corresponde a tu mudanza. Sin otro correo.</p>
{lead_form(ES_PATH, "Env&iacute;enme el resumen de reubicaci&oacute;n", renting=False, es=True, uid="lkres")}
</section>
"""
    return page(
        path=ES_PATH,
        title="Trabajar en Lockheed Martin Fort Worth: Guía de Vivienda y Reubicación (2026)",
        description=("¿Te mudas para trabajar en Lockheed Martin Fort Worth? El mapa de vivienda "
                     "del lado oeste en una página: rentar o comprar, trayectos por zona, escuelas "
                     "y el cruce con NAS JRB - con datos publicados y con fuente."),
        h1="Trabajar en Lockheed Martin Fort Worth: dónde vivir",
        eyebrow="CENTRO DE REUBICACI&Oacute;N &middot; LA PLANTA, LAS ZONAS Y LOS CAMINOS",
        lede=("La planta está al oeste, las zonas accesibles están al oeste y las buenas "
              "escuelas están al oeste — una de las pocas reubicaciones de DFW donde todo "
              "apunta en la misma dirección. Aquí está la decisión completa, organizada."),
        crumb="<a href='/es/'>Inicio</a> / <a href='/es/relocate/'>Mudanza</a> / Trabajar en Lockheed Martin",
        verified=VERIFIED,
        es=True,
        alt_path=EN_PATH,
        body=body,
        ld=[article_ld("Trabajar en Lockheed Martin Fort Worth: Guía de Vivienda y Reubicación",
                       f"https://westfwliving.com{_url(ES_PATH)}",
                       "El mapa de vivienda y reubicación del lado oeste para empleados de Lockheed Martin Fort Worth: rentar o comprar, trayectos, escuelas y NAS JRB.",
                       VERIFIED),
            faq_ld(FAQ_ES)],
    )


def build():
    return {EN_PATH: build_en(), ES_PATH: build_es()}
