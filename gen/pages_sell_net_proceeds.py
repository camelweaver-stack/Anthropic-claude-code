#!/usr/bin/env python3
"""West FW Living — the seller's net-proceeds napkin (EN + ES).

The worked example uses $450,000 because it sits inside the site's published
Willow Park typical sale band ($430K–$600K, public listing data, summer 2026).
The only hard dollar figures on the page are the two that are verifiable:

  Owner's title policy at $450,000: **$2,509**
    TDI basic premium schedule effective 2026-03-01, verified 2026-08-23:
    policies $100,001–$1,000,000 = (face − $100,000) × 0.00494 + $780
    → (450,000 − 100,000) × 0.00494 = 1,729; + 780 = 2,509.
  Transfer tax: **$0** — Texas constitutionally prohibits real-estate
    transfer taxes (Prop 1, approved 2015, in the constitution since 2016).

Everything else on the napkin is mechanics with fill-in-yourself blanks —
escrow fees, payoff, prorations, compensation — because those numbers are
negotiated or property-specific and inventing them would violate the runbook.
"""
from common import page, lead_form, article_ld, faq_ld, _url

VERIFIED = "2026-08-23"

EN_PATH = "/sell/net-proceeds.html"
ES_PATH = "/es/vender/ganancias-netas.html"

SRC_TDI = "https://tdi.texas.gov/title/titlerates2026.html"


def _napkin(es=False):
    if es:
        head = "<tr><th>Concepto</th><th>Ejemplo a $450,000</th><th>De d&oacute;nde sale</th></tr>"
        rows = [
            ("Precio de venta", "$450,000", "Tu contrato — el ejemplo est&aacute; dentro de la banda publicada de Willow Park ($430K–$600K)"),
            ("P&oacute;liza de t&iacute;tulo del comprador (owner's policy)", "&minus;$2,509", "Tarifa b&aacute;sica de TDI vigente desde 2026-03-01; por costumbre la paga el vendedor, pero es negociable en el contrato"),
            ("Impuesto de transferencia", "$0", "Texas lo proh&iacute;be constitucionalmente desde 2016"),
            ("Liquidaci&oacute;n de tu hipoteca", "&minus; tu saldo", "P&iacute;dele a tu prestamista la carta de payoff con inter&eacute;s por d&iacute;a"),
            ("Prorrateo del predial", "&minus; tu parte del a&ntilde;o", "En Texas se paga al vencido: acreditas al comprador del 1&deg; de enero a la fecha de cierre"),
            ("Cuota de cierre (escrow fee)", "&minus; seg&uacute;n la compa&ntilde;&iacute;a", "Var&iacute;a por compa&ntilde;&iacute;a de t&iacute;tulo — pide la hoja de tarifas antes de elegir"),
            ("HOA: certificado de reventa y transferencia", "&minus; seg&uacute;n tu HOA", "Pide el desglose por escrito a la administradora"),
            ("Compensaci&oacute;n de agentes", "&minus; lo que negocies", "Negociable y por escrito en tu contrato de listado — no hay tarifa fija"),
            ("Reparaciones / concesiones del periodo de opci&oacute;n", "&minus; lo que aceptes", "Sale de la negociaci&oacute;n de inspecci&oacute;n"),
        ]
    else:
        head = "<tr><th>Line item</th><th>Worked example at $450,000</th><th>Where the number comes from</th></tr>"
        rows = [
            ("Sale price", "$450,000", "Your contract — the example sits inside Willow Park's published band ($430K–$600K)"),
            ("Owner's title policy", "&minus;$2,509", "TDI's basic premium schedule effective 2026-03-01; customarily seller-paid in Texas, but negotiable in the contract"),
            ("Transfer tax", "$0", "Texas constitutionally prohibits real-estate transfer taxes (since 2016)"),
            ("Mortgage payoff", "&minus; your balance", "Order the payoff letter from your lender — it includes per-diem interest"),
            ("Property-tax proration", "&minus; your slice of the year", "Texas taxes are paid in arrears: you credit the buyer for Jan 1 through closing day"),
            ("Escrow / settlement fee", "&minus; company-specific", "Varies by title company — ask for the fee sheet before you pick one"),
            ("HOA resale certificate &amp; transfer fees", "&minus; HOA-specific", "Get the itemized list in writing from the management company"),
            ("Agent compensation", "&minus; whatever you negotiate", "Negotiable and set in writing in your listing agreement — there is no fixed rate"),
            ("Repairs / option-period concessions", "&minus; what you agree to", "Comes out of the inspection negotiation"),
        ]
    body = "".join(f"<tr><td><strong>{a}</strong></td><td class='money'>{b}</td><td>{c}</td></tr>"
                   for a, b, c in rows)
    return f"<table>{head}{body}</table>"


FAQ_EN = [
    ("How much does it cost to sell a house in Texas?",
     "Only two lines are fixed: Texas charges no transfer tax (constitutionally prohibited "
     "since 2016), and the owner's title policy follows TDI's promulgated schedule - $2,509 "
     "on a $450,000 sale under the rates effective March 1, 2026. Everything else - escrow "
     "fees, agent compensation, HOA fees, repairs - is negotiated or property-specific, which "
     "is why no honest single 'percent to sell' number exists."),
    ("Who pays for the title policy in Texas?",
     "Customarily the seller pays for the buyer's owner's policy in Texas, but it is a "
     "negotiable contract term, not a law. The premium itself is set by the Texas Department "
     "of Insurance, so it is the same at every title company - what varies by company is the "
     "escrow/settlement fee."),
    ("Does Texas have a real estate transfer tax?",
     "No. Texas voters constitutionally banned real-estate transfer taxes in 2015 (effective "
     "2016), so neither the state nor a Texas city or county can charge one."),
    ("How does the property-tax proration work at closing?",
     "Texas property taxes are paid in arrears, so at closing you credit the buyer for the "
     "portion of the year you owned the home - January 1 through closing day - computed from "
     "the most recent tax rate and value. Sell in early fall and the credit approaches "
     "three-quarters of the annual bill; the buyer then pays the full bill when it comes due."),
]

FAQ_ES = [
    ("¿Cuánto cuesta vender una casa en Texas?",
     "Solo dos renglones son fijos: Texas no cobra impuesto de transferencia (prohibido "
     "constitucionalmente desde 2016), y la póliza de título sigue la tarifa oficial de TDI - "
     "$2,509 en una venta de $450,000 con las tarifas vigentes desde el 1 de marzo de 2026. "
     "Todo lo demás se negocia o depende de la propiedad."),
    ("¿Quién paga la póliza de título en Texas?",
     "Por costumbre el vendedor paga la póliza del comprador, pero es un término negociable "
     "del contrato, no una ley. La prima la fija el Departamento de Seguros de Texas, así que "
     "es igual en cualquier compañía de título; lo que varía es la cuota de cierre."),
    ("¿Texas tiene impuesto de transferencia inmobiliaria?",
     "No. Los votantes lo prohibieron constitucionalmente en 2015 (vigente desde 2016), así "
     "que ni el estado ni una ciudad o condado de Texas pueden cobrarlo."),
    ("¿Cómo funciona el prorrateo del predial al cerrar?",
     "El predial en Texas se paga al vencido: al cerrar, acreditas al comprador la parte del "
     "año en que fuiste dueño - del 1 de enero a la fecha de cierre - calculada con la tasa y "
     "el valor más recientes."),
]


def build_en():
    body = f"""<section>
  <h2 id="short-answer">The short answer</h2>
  <p>There is no honest single &ldquo;it costs X% to sell&rdquo; number &mdash; most of a Texas seller's closing costs are negotiated, not fixed. But the napkin has exactly two hard lines, and they're both good news: <strong>Texas charges no transfer tax</strong> (constitutionally prohibited since 2016), and the owner's title policy follows a state-set schedule &mdash; <strong>$2,509 on a $450,000 sale</strong> under TDI's rates effective March 1, 2026. Everything else is a blank you fill in from documents you can demand up front. This page is the napkin.</p>
  <p class="tag">Verified {VERIFIED} &middot; title premium from TDI's 2026 schedule &middot; example price sits in Willow Park's published band</p>
</section>

<section>
  <h2>The napkin, line by line</h2>
  <p>Worked at $450,000 &mdash; inside the typical band this site publishes for <a href="/sell/willow-park">Willow Park</a> ($430K&ndash;$600K, public listing data, summer 2026), and a realistic mid-corridor number from <a href="/sell/hudson-oaks">Hudson Oaks</a> to <a href="/sell/benbrook">Benbrook</a>:</p>
  {_napkin()}
  <p>The title premium deserves one more sentence, because it's the line sellers overpay attention to and underpay attention around: the premium is <em>promulgated</em> &mdash; set by the Texas Department of Insurance, identical at every title company &mdash; computed as (price &minus; $100,000) &times; 0.00494 + $780 for homes between $100K and $1M. What varies between companies is the <strong>escrow/settlement fee</strong>, which is why the fee sheet, not the premium, is the thing to shop.</p>
</section>

<section>
  <h2>The three documents that fill in the blanks</h2>
  <ol>
    <li><strong>The payoff letter</strong> from your lender &mdash; your true balance plus per-diem interest to the closing date. Order it early; it has an expiration date.</li>
    <li><strong>The title company's fee sheet</strong> &mdash; the escrow fee and any add-ons. This is the shoppable part.</li>
    <li><strong>The HOA's resale package quote</strong> &mdash; resale certificate, transfer fees, any capital contribution billed at transfer. Get it itemized, in writing, from the management company.</li>
  </ol>
  <p>With those three plus your negotiated compensation terms, the napkin closes to a real number &mdash; before you list, not at the closing table.</p>
</section>

<section>
  <h2>Who this applies to</h2>
  <p><strong>Move-up sellers</strong> running whether the equity actually covers the next down payment &mdash; pair this with <a href="/sell/sell-before-buying">sell before you buy</a> and <a href="/sell/equity-report">the equity report</a>. <strong>Corridor owners gut-checking a listing price</strong> against what actually lands in the account &mdash; the per-city bands live on the <a href="/sell/">selling hub</a>. <strong>Anyone comparing offers</strong> &mdash; a higher price with heavy concessions can net less than a clean lower one; the napkin makes that visible.</p>
  <p>Taxes on the gain are the other half of the picture: <a href="/sell/capital-gains">capital gains, plain English</a> covers the federal exclusion most owner-occupants qualify for &mdash; and after closing, the buyer's side of the ledger starts with <a href="/buy/homestead-exemption">the homestead exemption</a> on the next house.</p>
</section>

<section>
  <h2>Next steps</h2>
  <ol>
    <li>Order the payoff letter and pull your last mortgage statement.</li>
    <li>Ask two title companies for their fee sheets (the premium is identical; the escrow fee isn't).</li>
    <li>Request the HOA resale-package quote in writing, if you have an HOA.</li>
    <li>Run your own number through the napkin above &mdash; then sanity-check the price against <a href="/sell/home-value">what's my home worth</a>.</li>
  </ol>
</section>

<section>
  <h2>Sources</h2>
  <ul>
    <li>Texas Department of Insurance &mdash; <a href="{SRC_TDI}" rel="nofollow">Basic Premium Rates for title insurance, effective 2026-03-01</a>: $780 at $100,000; (face &minus; $100,000) &times; 0.00494 + $780 for $100,001&ndash;$1,000,000. The $2,509 figure is that formula at $450,000.</li>
    <li>Transfer tax &mdash; prohibited by the Texas Constitution (statewide Proposition 1, approved 2015, effective 2016).</li>
    <li>Example price &mdash; inside the Willow Park typical sale band ($430K&ndash;$600K) published on <a href="/sell/willow-park">/sell/willow-park</a>, compiled from public listing data, summer 2026.</li>
  </ul>
  <p><strong>Verified {VERIFIED}.</strong> Educational only &mdash; not legal, tax, or financial advice for any specific transaction; your contract terms govern.</p>
</section>

<section>
  <h2>Keep reading</h2>
  <p><a href="/sell/">the selling hub</a> &middot; <a href="/sell/capital-gains">capital gains, plain English</a> &middot; <a href="/sell/sell-before-buying">sell before you buy</a> &middot; <a href="/sell/home-value">what's my home worth</a> &middot; <a href="/buy/homestead-exemption">the buyer's homestead exemption</a></p>
  <p><a href="{_url(ES_PATH)}" hreflang="es">Lee esta p&aacute;gina en espa&ntilde;ol &mdash; Las cuentas netas del cierre</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>Want the neighborhood-level bands with your napkin?</h2>
  <p>We track the corridor's sale bands as the compilations update. The early list hears when your pocket's numbers move &mdash; no other mail.</p>
{lead_form(EN_PATH, "Send me my pocket's numbers", selling=True, es=False, uid="npk")}
</section>
"""
    return page(
        path=EN_PATH,
        title="The Texas Seller's Net-Proceeds Napkin: a $450K West Fort Worth Example (2026)",
        description=("What it actually costs to sell in Texas, line by line: the $2,509 TDI title "
                     "premium at $450K, the $0 transfer tax, the tax proration, and the blanks only "
                     "your documents can fill. Worked on a Willow Park-band example."),
        h1="The seller's net-proceeds napkin",
        eyebrow="WHAT SELLING ACTUALLY COSTS &middot; A $450K WORKED EXAMPLE",
        lede=("Two lines are fixed by the state &mdash; the $2,509 title premium and the $0 transfer "
              "tax. Everything else is a blank your documents fill in. Here's the napkin, worked at a "
              "price inside Willow Park's published band."),
        crumb="<a href='/'>Home</a> / <a href='/sell/'>Selling</a> / Net Proceeds",
        verified=VERIFIED,
        es=False,
        alt_path=ES_PATH,
        body=body,
        ld=[article_ld("The seller's net-proceeds napkin",
                       f"https://westfwliving.com{_url(EN_PATH)}",
                       "Texas selling costs line by line: the TDI title premium, the zero transfer tax, prorations, and the negotiated blanks - worked at $450,000.",
                       VERIFIED),
            faq_ld(FAQ_EN)],
    )


def build_es():
    body = f"""<section>
  <h2>La respuesta corta</h2>
  <p>No existe un &ldquo;vender cuesta X%&rdquo; honesto &mdash; la mayor&iacute;a de los costos del vendedor en Texas se negocian, no son fijos. Pero la servilleta tiene exactamente dos renglones duros, y los dos son buenas noticias: <strong>Texas no cobra impuesto de transferencia</strong> (prohibido constitucionalmente desde 2016), y la p&oacute;liza de t&iacute;tulo sigue una tarifa fijada por el estado &mdash; <strong>$2,509 en una venta de $450,000</strong> con las tarifas de TDI vigentes desde el 1 de marzo de 2026. Todo lo dem&aacute;s es un espacio en blanco que llenas con documentos que puedes exigir por adelantado.</p>
  <p class="tag">Verificado el {VERIFIED} &middot; prima de t&iacute;tulo de la tarifa TDI 2026 &middot; el precio del ejemplo cae en la banda publicada de Willow Park</p>
</section>

<section>
  <h2>La servilleta, rengl&oacute;n por rengl&oacute;n</h2>
  <p>Trabajada a $450,000 &mdash; dentro de la banda t&iacute;pica que este sitio publica para <a href="/es/vender/willow-park">Willow Park</a> ($430K&ndash;$600K, listados p&uacute;blicos, verano 2026):</p>
  {_napkin(es=True)}
  <p>La prima de t&iacute;tulo merece una oraci&oacute;n m&aacute;s: es <em>promulgada</em> &mdash; la fija el Departamento de Seguros de Texas y es id&eacute;ntica en cualquier compa&ntilde;&iacute;a &mdash; calculada como (precio &minus; $100,000) &times; 0.00494 + $780 para casas entre $100K y $1M. Lo que s&iacute; var&iacute;a entre compa&ntilde;&iacute;as es la <strong>cuota de cierre</strong>; esa es la que conviene comparar.</p>
</section>

<section>
  <h2>Los tres documentos que llenan los espacios</h2>
  <ol>
    <li><strong>La carta de payoff</strong> de tu prestamista &mdash; tu saldo real m&aacute;s el inter&eacute;s por d&iacute;a hasta el cierre. P&iacute;dela temprano; tiene fecha de vencimiento.</li>
    <li><strong>La hoja de tarifas de la compa&ntilde;&iacute;a de t&iacute;tulo</strong> &mdash; la cuota de cierre y sus extras. Esta es la parte comparable.</li>
    <li><strong>La cotizaci&oacute;n del paquete de reventa del HOA</strong> &mdash; certificado, cuotas de transferencia, cualquier aportaci&oacute;n al transferir. Por escrito y desglosada.</li>
  </ol>
</section>

<section>
  <h2>A qui&eacute;n le aplica</h2>
  <p><strong>Vendedores que suben de casa</strong> comprobando si el capital cubre el siguiente enganche &mdash; combina con <a href="/es/vender/vender-antes-de-comprar">vender antes de comprar</a> y <a href="/es/vender/reporte-de-plusvalia">el reporte de plusval&iacute;a</a>. <strong>Due&ntilde;os del corredor</strong> comparando el precio de lista con lo que de verdad llega a la cuenta &mdash; las bandas por ciudad viven en <a href="/es/vender/">el centro de venta</a>. Los impuestos sobre la ganancia son la otra mitad: <a href="/es/vender/impuestos-ganancias">impuestos al vender, en espa&ntilde;ol claro</a>.</p>
</section>

<section>
  <h2>Pr&oacute;ximos pasos</h2>
  <ol>
    <li>Pide la carta de payoff y tu &uacute;ltimo estado de cuenta hipotecario.</li>
    <li>Pide hojas de tarifas a dos compa&ntilde;&iacute;as de t&iacute;tulo (la prima es igual; la cuota de cierre no).</li>
    <li>Solicita por escrito la cotizaci&oacute;n del paquete de reventa del HOA, si tienes HOA.</li>
    <li>Corre tu propio n&uacute;mero por la servilleta &mdash; y compara el precio con <a href="/es/vender/valor-de-tu-casa">el valor de tu casa</a>.</li>
  </ol>
</section>

<section>
  <h2>Fuentes</h2>
  <ul>
    <li>Departamento de Seguros de Texas (TDI) &mdash; <a href="{SRC_TDI}" rel="nofollow">tarifas b&aacute;sicas de t&iacute;tulo vigentes desde 2026-03-01</a>: $780 a $100,000; (precio &minus; $100,000) &times; 0.00494 + $780 entre $100,001 y $1,000,000. Los $2,509 son esa f&oacute;rmula a $450,000.</li>
    <li>Impuesto de transferencia &mdash; prohibido por la Constituci&oacute;n de Texas (Proposici&oacute;n 1 estatal, aprobada en 2015, vigente desde 2016).</li>
    <li>Precio del ejemplo &mdash; dentro de la banda publicada de Willow Park en <a href="/es/vender/willow-park">/es/vender/willow-park</a> (listados p&uacute;blicos, verano 2026).</li>
  </ul>
  <p><strong>Verificado el {VERIFIED}.</strong> Contenido educativo &mdash; no es asesor&iacute;a legal, fiscal ni financiera para ninguna transacci&oacute;n espec&iacute;fica; rigen los t&eacute;rminos de tu contrato.</p>
</section>

<section>
  <h2>Sigue leyendo</h2>
  <p><a href="/es/vender/">el centro de venta</a> &middot; <a href="/es/vender/impuestos-ganancias">impuestos al vender</a> &middot; <a href="/es/vender/vender-antes-de-comprar">vender antes de comprar</a> &middot; <a href="/es/comprar/exencion-homestead">la exenci&oacute;n homestead del comprador</a></p>
  <p><a href="{_url(EN_PATH)}" hreflang="en">Read this page in English &mdash; The net-proceeds napkin</a></p>
</section>

<section class="tint" style="border-radius:14px;padding:34px 28px">
  <h2>&iquest;Quiere las bandas de su zona junto con la servilleta?</h2>
  <p>Seguimos las bandas de venta del corredor conforme se actualizan las compilaciones. La lista se entera primero.</p>
{lead_form(ES_PATH, "Env&iacute;enme los n&uacute;meros de mi zona", selling=True, es=True, uid="npk")}
</section>
"""
    return page(
        path=ES_PATH,
        title="Las Cuentas Netas del Cierre: Ejemplo de $450K en el Oeste de Fort Worth (2026)",
        description=("Cu&aacute;nto cuesta vender en Texas, rengl&oacute;n por rengl&oacute;n: la prima de "
                     "t&iacute;tulo de $2,509 seg&uacute;n TDI, el impuesto de transferencia de $0, el "
                     "prorrateo del predial y los espacios que solo tus documentos llenan."),
        h1="Las cuentas netas del cierre",
        eyebrow="LO QUE VENDER CUESTA DE VERDAD &middot; EJEMPLO A $450K",
        lede=("Dos renglones los fija el estado &mdash; la prima de t&iacute;tulo de $2,509 y el impuesto "
              "de transferencia de $0. Todo lo dem&aacute;s es un espacio que llenan tus documentos. "
              "Aqu&iacute; est&aacute; la servilleta, a un precio dentro de la banda publicada de Willow Park."),
        crumb="<a href='/es/'>Inicio</a> / <a href='/es/vender/'>Vender</a> / Cuentas Netas",
        verified=VERIFIED,
        es=True,
        alt_path=EN_PATH,
        body=body,
        ld=[article_ld("Las cuentas netas del cierre",
                       f"https://westfwliving.com{_url(ES_PATH)}",
                       "Costos de venta en Texas rengl&oacute;n por rengl&oacute;n: prima TDI, cero impuesto de transferencia, prorrateos y los espacios negociados - a $450,000.",
                       VERIFIED),
            faq_ld(FAQ_ES)],
    )


def build():
    return {EN_PATH: build_en(), ES_PATH: build_es()}
