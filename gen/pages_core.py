from common import *

def homepage():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Honolulu County MHA · BAH effective {BAH["effective"]}</p>
<h1>You have orders to Oahu. Here's the honest math.</h1>
<p class="lede">PCS Oahu is an independent field guide for service members and families reporting
to Joint Base Pearl Harbor–Hickam, Schofield Barracks, MCBH Kaneohe Bay, Camp Smith, Tripler, or
Coast Guard Base Honolulu — and for the other half of the cycle, when the orders point back out.
No hype, no kitsch. Just what housing actually costs, what your allowance actually covers, and
what to decide before wheels-down. New orders? The
<a href="/pcs-to-hawaii/">complete PCS-to-Hawaii guide</a> walks the whole move in the order the
decisions actually arrive; temporary lodging lives in the <a href="/tla/">TLA guide</a>.</p>
<p><a class="btn" href="/pcs-to-hawaii/">Start here: the PCS to Hawaii guide</a>
<a class="btn ghost" href="/bah-report/">The BAH Reality Report</a>
<a class="btn ghost" href="/pcs-checklist/">Interactive checklist</a>
<a class="btn ghost" href="/quiz/">Pocket-match quiz</a></p>
<form class="ask-hero" action="/ask/" method="get" role="search"
      style="display:flex;gap:.5rem;max-width:38rem;margin-top:.4rem">
  <input name="q" type="text" aria-label="Ask PCS Oahu a question"
         placeholder="Ask about your PCS — BAH, pockets, VA, HARPTA, the pet clock…"
         style="flex:1;min-width:0;padding:.6rem .8rem;border-radius:8px;border:1px solid var(--rule)">
  <button class="btn" type="submit">Ask PCS Oahu</button>
</form>
</div></div>
<div class="wrap">
<p class="eyebrow">The one fact that changes your search</p>
<h2>Every Oahu base pays the same BAH. The rents are not the same.</h2>
<p style="max-width:46rem">All six installations sit inside one Military Housing Area — Honolulu
County. Your allowance changes with rank and dependents, never with your gate. What changes by
gate is the rent on the other side of it, and the commute you'll live with for three years.
That gap — same allowance, very different pockets — is the whole game, and it's what every page
on this site is built to map.</p>
{rates([
  ("E-5 with dependents", BAH["e5_dep"]),
  ("E-5 without dependents", BAH["e5_solo"]),
  ("E-6 with dependents", BAH["e6_dep"]),
  ("2026 island-wide range", BAH["floor"] + " – " + BAH["ceiling"], True),
], "DTMO " + BAH_YEAR + " tables, Honolulu County MHA, effective " + BAH["effective"] +
   ". Pull your exact grade at the DTMO BAH calculator — these are anchors, not your LES.")}
<div class="grid c3">
  <div class="card"><span class="tag">Arriving</span><h3><a href="/bases/">Your base, your pockets</a></h3>
    <p>Base-by-base live-on-or-off math: commute-real neighborhoods with dated rent bands next to
    the allowance they have to fit inside.</p></div>
  <div class="card"><span class="tag">Buying</span><h3><a href="/buy/">The VA loan, Oahu edition</a></h3>
    <p>Entitlement math at Oahu price points, the condo VA-approval reality, and the leasehold
    trap that catches mainland buyers.</p></div>
  <div class="card"><span class="tag">Departing</span><h3><a href="/sell/">PCSing out: sell or rent?</a></h3>
    <p>The other half of the cycle. HARPTA facts, the accidental-landlord math, and what a VA
    seller should know before listing.</p></div>
</div>
<h2>First 30 days, mapped</h2>
<div class="grid c3">
  <div class="card"><span class="tag">Interim housing</span><h3><a href="/tla/">TLA without the panic</a></h3>
    <p>How Temporary Lodging Allowance actually works in Hawaii, and how families bridge the gap
    between wheels-down and keys.</p></div>
  <div class="card"><span class="tag">Family</span><h3><a href="/schools/">Schools, decoded</a></h3>
    <p>Hawaii runs one statewide district — which changes how school choice works. Geographic
    exceptions, calendars, and enrollment timing.</p></div>
  <div class="card"><span class="tag">Tools</span><h3><a href="/tools/">The math, automated</a></h3>
    <p>BAH-vs-rent fit, rent-vs-sell for departing owners, and a payment reality check — free,
    nothing leaves your phone.</p></div>
</div>
<h2>Make it yours</h2>
<div class="grid c3">
  <div class="card"><span class="tag">No account needed</span><h3><a href="/my-pcs/">My PCS dashboard</a></h3>
    <p>Your quiz match, saved pockets, checklist, and calculator results — on your device,
    exportable as a plan.</p></div>
  <div class="card"><span class="tag">Concierge</span><h3><a href="/ask/">Ask PCS Oahu</a></h3>
    <p>Questions answered from the guides, with links — and honest limits.</p></div>
  <div class="card"><span class="tag">Research</span><h3><a href="/data/">The data desk</a></h3>
    <p>Every named report, the refresh cadence, and what's coming next.</p></div>
</div>
{lead_form("HOME", "pcs-renter",
  heading="The arrival brief, before you arrive",
  blurb="Join the list and get the current BAH Reality Report, the rent-band refresh for your "
        "gaining base, and a heads-up timed to your report window. First access when full service "
        "opens. No spam. Leave anytime.")}
</div>'''
    # WebSite/Organization now emitted sitewide by page() (see common.identity_graph()).
    return page("/", "PCS Oahu — The Field Guide for Military Orders to Oahu",
                "Orders to Hawaii? Base-by-base BAH vs rent math, VA loans at Oahu prices, TLA, "
                "schools, and the sell-or-rent call when you PCS out. Independent and honest.",
                body, "")

BASES = [
 dict(slug="pearl-harbor-hickam", tag="JBPHH", name="Joint Base Pearl Harbor–Hickam",
   short="JBPHH", side="Leeward / central south shore",
   intro="The island's biggest installation and its worst-understood commute problem. JBPHH sits "
         "at the center of Oahu's traffic geometry: pockets ten minutes away in a vacuum are "
         "forty-five in the H-1 morning crush, and the westbound afternoon return from town is "
         "its own weather system. Choose your pocket by drive-time at 0630, not by map distance.",
   pockets=["aiea","pearlcity","saltlake","waipahu","mililani","ewa"],
   commute=[("Aiea / Halawa","10–20 min to most gates; closest true neighborhood"),
            ("Salt Lake / Moanalua","10–20 min; condo-heavy, walkable errands"),
            ("Pearl City","15–25 min; townhome and single-family mix"),
            ("Waipahu","15–30 min; most rent per dollar this close in"),
            ("Mililani","25–40 min against H-2 flow; the family-planned-community default"),
            ("Ewa Beach / Kapolei","30–60+ min in real traffic; newest housing stock, hardest drive — "
             "the Skyline rail segment serving Pearl Harbor changes this calculus for some schedules")],
   note="Sailors on sea duty and shift workers rate pockets very differently from staff hours — "
        "a Kapolei house that's a 65-minute 0700 commute can be a 25-minute drive at 0500."),
 dict(slug="schofield-wheeler", tag="SCHOFIELD", name="Schofield Barracks & Wheeler Army Airfield",
   short="Schofield", side="Central plateau",
   intro="Home of the 25th Infantry Division, up on the cooler central plateau — and the one Oahu "
         "assignment where living close is genuinely affordable. Wahiawa, directly outside the "
         "gate, carries some of the lowest rent bands on the island. The trade: you're 40–60 "
         "minutes from town beaches and nightlife, and everything runs through the H-2.",
   pockets=["wahiawa","mililani","waipahu","ewa"],
   commute=[("Wahiawa","5–15 min; oldest stock, lowest bands, walkable small-town core"),
            ("Mililani / Mililani Mauka","10–20 min; the family default, strong amenities"),
            ("Waipio / Waikele / Waipahu","20–30 min; middle path on price and drive"),
            ("Ewa Beach / Kapolei","30–50 min; newer homes, but you fight H-2 and H-1 both ways")],
   bah_note=("Schofield Barracks BAH, in practice",
     'There is no separate "Schofield Barracks BAH rate": Schofield and Wheeler draw the same '
     'Honolulu County MHA rate as every other Oahu installation, set by rank and dependency '
     'status. What makes Schofield different is what that identical rate <em>buys</em>: per the '
     'current rent bands, Wahiawa — directly outside the gate — carries some of the lowest '
     '3-bedroom bands on the island, comfortably inside the E-5 with-dependents anchor, while '
     'Mililani, the family default up the road, straddles it. Few Oahu gates put the allowance '
     'this far ahead of the close-in market. Run the island-wide picture in the '
     '<a href="/bah-report/">BAH Reality Report</a>, then pull your exact grade from the DTMO '
     'BAH calculator before you budget — the figures here are dated anchors, not your LES.'),
   note="High deployment tempo is a housing fact here, not just a duty fact: many spouses "
        "prioritize Mililani's networks and services over saving a few hundred dollars in a "
        "pocket with less support."),
 dict(slug="kaneohe-bay", tag="MCBH", name="Marine Corps Base Hawaii — Kaneohe Bay",
   short="MCBH", side="Windward",
   intro="The windward side is greener, wetter, cooler — and priced like people know it. Kaneohe "
         "and Kailua are the two real off-base options; both run above the island's typical bands, "
         "with Kailua at a hard premium. Living leeward to save money means commuting the H-3 "
         "through the mountain every day, which is beautiful exactly twice.",
   pockets=["kaneohe","kailua"],
   commute=[("Kaneohe","10–15 min; the practical choice, median rents around $3,500 overall in "
             "mid-2026 public data"),
            ("Kailua","10–20 min; premium beach-town bands — budget for it or don't window-shop it"),
            ("Leeward pockets via H-3","35–60+ min; the savings are real and so is the drive")],
   note="Windward inventory is thin. In PCS season, well-priced Kaneohe 3-bedrooms move in days. "
        "Have documents staged before you fly."),
 dict(slug="camp-smith", tag="CAMPSMITH", name="Camp H.M. Smith",
   short="Camp Smith", side="Halawa Heights",
   intro="INDOPACOM's headquarters sits above Halawa — a small installation with no family "
         "housing scale of its own, which makes the off-base decision the default decision. The "
         "good news: it's minutes from the island's most livable mid-band pockets.",
   pockets=["aiea","saltlake","pearlcity","kalihi"],
   commute=[("Aiea","5–15 min; effectively the home neighborhood"),
            ("Salt Lake / Moanalua","10–15 min; condo value close in"),
            ("Pearl City","10–20 min; more space per dollar"),
            ("Town (Kalihi to Kakaako)","15–30 min; urban living against the traffic flow")],
   note="Staff-hours schedules make this one of the few Oahu assignments where a town condo "
        "commute is genuinely reasonable."),
 dict(slug="tripler", tag="TRIPLER", name="Tripler Army Medical Center",
   short="Tripler", side="Moanalua ridge",
   intro="The pink hospital on the ridge is its own duty station with its own rhythm — shift work, "
         "on-call, and a workforce that prizes minutes-to-parking over square footage. The "
         "close-in condo pockets are the play.",
   pockets=["saltlake","aiea","kalihi","downtown"],
   commute=[("Salt Lake / Moanalua","5–15 min; the default for hospital staff"),
            ("Aiea","10–15 min; more house for the money"),
            ("Kalihi","10–15 min; lowest close-in bands on the island"),
            ("Downtown / Kakaako","15–30 min; urban option for single service members")],
   note="If you're on nights, tour your shortlist at your actual commute hours — Moanalua Freeway "
        "behavior flips completely by time of day."),
 dict(slug="fort-shafter", tag="SHAFTER", name="Fort Shafter",
   short="Fort Shafter", side="Moanalua / Kalihi uplands",
   intro="U.S. Army Pacific's headquarters is the oldest Army post on the island and the most "
         "centrally placed duty station on it — which makes this one of the few Oahu assignments "
         "where nearly every close-in pocket is a plausible commute. The decision here is less "
         "about surviving a drive and more about choosing between condo value close in and house "
         "space one valley over.",
   pockets=["saltlake","kalihi","aiea","pearlcity","downtown"],
   commute=[("Salt Lake / Moanalua","5–15 min; the staff-hours default"),
            ("Kalihi","5–15 min; lowest close-in bands on the island"),
            ("Aiea","10–20 min; more house per dollar, against lighter flow"),
            ("Pearl City","15–25 min; townhome and single-family territory"),
            ("Downtown / Kakaako","15–25 min; the urban option, reverse of the worst traffic")],
   note="Dual-military households split between Shafter and Schofield often anchor at the "
        "Waipio/Waikele midpoint — run both commutes before defaulting to either gate's "
        "neighborhood."),
 dict(slug="coast-guard-honolulu", tag="USCG", name="U.S. Coast Guard Base Honolulu",
   short="USCG Honolulu", side="Sand Island / Honolulu Harbor",
   intro="Sand Island sits inside the working harbor, which makes this the most urban housing "
         "problem on the island: town condos, town parking, town prices. The compensation is that "
         "Coast Guard members here can live the closest thing Oahu offers to a city life.",
   pockets=["kalihi","downtown","saltlake"],
   commute=[("Kalihi / Iwilei","5–15 min; the value play right outside the causeway"),
            ("Downtown / Kakaako","10–15 min; walkable urban condos at urban bands"),
            ("Salt Lake / Moanalua","10–20 min; quieter middle path")],
   note="Condo shoppers here should read the VA condo-approval section before falling for a "
        "building — town inventory is where the approval list matters most."),
]

def pcs_to_hawaii():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The master guide · orders in hand to wheels-down and beyond</p>
<h1>PCS to Hawaii: the complete Oahu move, in order</h1>
<p class="lede">Everything this site knows about a Hawaii PCS, on one page, in the order the
decisions actually arrive. Each section gives you the direct answer and hands you the full guide
— every figure on those pages is dated and sourced, and none of this is official guidance: your
orders, your transportation office, and Military OneSource govern your entitlements.</p>
<p><a class="btn" href="/pcs-checklist/">Open the interactive checklist</a>
<a class="btn ghost" href="/bah-report/">Check the BAH-vs-rent numbers</a></p>
</div></div>
<div class="wrap">
<h2>The direct answer</h2>
<p style="max-width:46rem">A Hawaii PCS is an OCONUS move wearing a domestic nametape: your
household goods travel by ship, your car needs a booking, your pet is on a months-long
rabies-program clock, and your family lands in temporary lodging before you've seen a single
rental. The families who land soft all do the same thing — they run the clocks that start the day
orders drop <em>first</em>, and leave the fun decisions (pocket, house, beach) for the
<a href="/tla/">TLA window</a> when they can see the island. This page walks that order.</p>

<h2>1 — The day orders drop</h2>
<p style="max-width:46rem">Four clocks start immediately, and none of them wait for your flight.
<strong><a href="/guides/pets-to-hawaii.html">The pet clock</a></strong> is the least forgiving:
Hawaii is rabies-free, and Direct Airport Release only works if the microchip → vaccination →
blood test → waiting period sequence is run early and in order.
<strong><a href="/guides/household-goods.html">Household goods</a></strong> move by sea in
multiple shipments — unaccompanied baggage first, the main lift later — booked through your
transportation office and DPS. <strong><a href="/vehicle-shipping/">Your one shipped
vehicle</a></strong> has its own booking and port timeline. And the
<strong><a href="/guides/on-base-waitlist.html">on-base housing waitlist</a></strong> costs
nothing to join, commits you to nothing, and on the Army side can backdate your position if you
apply promptly. Families with kids should also start
<a href="/guides/school-transition.html">records and health paperwork</a> mainland-side — Hawaii
enforces immunization and TB clearance at enrollment, and the school year starts earlier than
most mainland calendars.</p>

<h2>2 — Know your money before you shop</h2>
<p style="max-width:46rem">Two allowances shape the whole move. <strong>BAH:</strong> every Oahu
installation draws the same Honolulu County rate — set by rank and dependents, never by base —
and whether that rate covers a real pocket is the island's defining housing question. The
<a href="/bah-report/">BAH Reality Report</a> puts the current anchors next to dated rent bands,
pocket by pocket. <strong>TLA:</strong> Temporary Lodging Allowance bridges wheels-down to keys —
the <a href="/tla/">temporary-lodging guide</a> covers how the window works in practice and the
<a href="/tla/field-notes.html">lodging field notes</a> cover where people actually stay. Verify
both entitlements against your orders with your finance office and Military OneSource — this site
maps the market, not your LES.</p>

<h2>3 — Pick your gate's pockets, not a postcard</h2>
<p style="max-width:46rem">Housing search order matters here more than anywhere on the mainland:
<strong>gate → corridor → pocket → rent → drive test</strong>. The
<a href="/guides/commute-first.html">commute-first decision guide</a> walks the method, the
<a href="/neighborhoods/">pocket table</a> carries the dated rent bands, and the
<a href="/quiz/">pocket-match quiz</a> automates the first pass. Then read your installation's
own page — each pairs the allowance with the pockets people actually commute from:</p>
<ul style="max-width:46rem;columns:2;gap:2rem">
<li><a href="/bases/pearl-harbor-hickam.html">Joint Base Pearl Harbor–Hickam</a></li>
<li><a href="/bases/schofield-wheeler.html">Schofield Barracks &amp; Wheeler</a></li>
<li><a href="/bases/kaneohe-bay.html">MCBH Kaneohe Bay</a></li>
<li><a href="/bases/fort-shafter.html">Fort Shafter</a></li>
<li><a href="/bases/tripler.html">Tripler Army Medical Center</a></li>
<li><a href="/bases/camp-smith.html">Camp Smith</a></li>
<li><a href="/bases/coast-guard-honolulu.html">Coast Guard Base Honolulu</a></li>
</ul>

<h2>4 — Rent, buy, or wait for the waitlist</h2>
<p style="max-width:46rem">Three legitimate paths, one honest framework.
<strong>Renting</strong> points your BAH at the pocket that survived the commute test.
<strong>Buying</strong> can work on Oahu's VA math — no down payment, no PMI, the strongest BAH
in the force — but the <a href="/guides/rent-vs-buy.html">rent-vs-buy framework</a> and the
<a href="/buy/">VA buyer brief</a> are honest about the break-even horizon, condo approval, and
the leasehold trap. <strong>On-base</strong> trades your whole allowance for proximity and zero
landlord risk — the <a href="/on-base/">on-base guide</a> runs that ledger. Families with kids:
read the <a href="/schools/">schools guide</a> before the lease, not after — Hawaii's statewide
district ties school to address. And <a href="/guides/dodea-schools.html">no, there are no DoDEA
schools here</a>.</p>

<h2>5 — Wheels-down: the first 30 days</h2>
<p style="max-width:46rem">Land, start TLA, and run the arrival clocks: the
<a href="/guides/vehicle-registration.html">30-day vehicle registration window</a> once your car
clears the port, <a href="/guides/school-transition.html">school enrollment</a> with the records
you staged, <a href="/guides/childcare.html">childcare waitlists</a> (start these even earlier if
you can), <a href="/guides/utilities.html">utilities</a>, and
<a href="/guides/healthcare.html">TRICARE enrollment</a>. The
<a href="/pcs-checklist/">interactive checklist</a> sequences all of it into six phases and saves
progress on your device.</p>

<h2>6 — The other half of the cycle</h2>
<p style="max-width:46rem">Every arrival is somebody's departure. When your own outbound orders
come, the <a href="/sell/">sell-or-rent brief</a> runs the accidental-landlord math, and the
<a href="/guides/harpta.html">HARPTA guide</a> explains the 7.25% withholding that surprises
outbound owners — with the pre-closing paperwork clock that matters more than the rate.</p>

<h2>Verify against the source</h2>
<p style="max-width:46rem">This is an independent field guide, not an official resource.
Entitlements, weight allowances, TLA rules, and shipment rights come from your orders, your
transportation office, your finance office, and Military OneSource — the linked guides above cite
the official sources for each topic inline, with the date each fact was verified. When this page
and your orders disagree, your orders win. Page verified <strong>September 6, 2026</strong>.</p>
{lead_form("PCSHUB", "pcs-renter",
  heading="Orders in hand?",
  blurb="Join the list and the arrival brief lands before you do: current BAH-vs-rent numbers "
        "for your gaining base, the clock checklist, and a heads-up timed to your report window.")}
</div>'''
    p = "/pcs-to-hawaii/"
    return page(p, "PCS to Hawaii: The Complete Oahu Move Guide | PCS Oahu",
        "PCSing to Hawaii? The whole Oahu move in order: the four clocks that start with orders, "
        "BAH and TLA money, commute-first housing, base-by-base guides, arrival logistics, and "
        "the outbound cycle. Independent, dated, and sourced.",
        body, "/pcs-to-hawaii/",
        jsonld={"@context": "https://schema.org", "@graph": [
            {"@type": "Article",
             "headline": "PCS to Hawaii: the complete Oahu move, in order",
             "description": "The master guide to a Hawaii PCS — clocks, money, housing, arrival, "
                            "and departure — routing to every detailed guide on the site.",
             "datePublished": "2026-09-06", "dateModified": "2026-09-06",
             "author": {"@type": "Organization", "name": "PCS Oahu"},
             "publisher": {"@type": "Organization", "name": "PCS Oahu"},
             "mainEntityOfPage": DOMAIN + p}]})


def base_page(b):
    prows = [(f'<a href="/neighborhoods/{p}.html">{POCKETS[p][0]}</a>', POCKETS[p][1])
             for p in b["pockets"]]
    commute_rows = "".join(f"<tr><td>{n}</td><td>{d}</td></tr>" for n, d in b["commute"])
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">{b["side"]} · Honolulu County MHA</p>
<h1>{b["name"]}: live on or off?</h1>
<p class="lede">{b["intro"]}</p>
</div></div>
<div class="wrap">
<h2>The allowance side of the ledger</h2>
<p style="max-width:46rem">Your BAH here is the same as every other Oahu installation — one
county-wide rate set by rank and dependents. The decision is whether your grade's number covers a
pocket you can actually commute from, or whether the <a href="/on-base/">on-base waitlist</a> (contact the housing
office the day orders drop) is the better bridge.</p>
{rates([
  ("E-5 with dependents", BAH["e5_dep"]),
  ("E-6 with dependents", BAH["e6_dep"]),
  ("E-5 / E-6 without dependents", BAH["e5_solo"] + " / " + BAH["e6_solo"]),
], "DTMO " + BAH_YEAR + " Honolulu County tables, effective " + BAH["effective"] +
   ". Anchors only — pull your exact grade from the DTMO calculator.")}
{('<h2 id="bah">' + b["bah_note"][0] + '</h2><p style="max-width:46rem">' + b["bah_note"][1] + '</p>') if b.get("bah_note") else ""}
<h2>The rent side, by commute-real pocket</h2>
{rates(prows, RENT_SRC)}
<h2>Commute reality</h2>
<table class="data"><thead><tr><th>Pocket</th><th>What the drive is actually like</th></tr></thead>
<tbody>{commute_rows}</tbody></table>
<p style="max-width:46rem;font-size:.88rem;color:#5b6b73">Drive descriptions are resident-reported
orientation, not measured promises — schedules, gates, and seasons move them. Before signing, run
the route yourself at your actual report time (the
<a href="/guides/commute-first.html">commute-first guide</a> walks the method).</p>
<div class="note"><strong>Field note.</strong> {b["note"]}</div>
<div class="grid c3">
  <div class="card"><span class="tag">Next</span><h3><a href="/tla/">Land first, then look</a></h3>
    <p>TLA and interim housing while you tour pockets in person.</p></div>
  <div class="card"><span class="tag">Buying</span><h3><a href="/buy/">Could BAH carry a mortgage?</a></h3>
    <p>The VA loan at Oahu prices, without the sales pitch.</p></div>
  <div class="card"><span class="tag">Data</span><h3><a href="/bah-report/">The BAH Reality Report</a></h3>
    <p>The island-wide allowance-vs-rent picture, dated and sourced.</p></div>
</div>
{lead_form(b["tag"], "pcs-renter",
  heading="Reporting to " + b["short"] + "?",
  blurb="Join the list and we'll send the current rent-band refresh for these pockets and a "
        "heads-up timed to your report window. No spam. Leave anytime.")}
</div>'''
    path = f"/bases/{b['slug']}.html"
    return path, page(path,
        f"{b['name']} — Live On or Off Base? BAH vs Rent | PCS Oahu",
        f"Honest 2026 math for {b['short']}: Honolulu County BAH anchors vs dated rent bands in "
        f"commute-real neighborhoods, plus field notes for arriving families.",
        body, "/bases/", jsonld=article_ld(path, f"{b['name']}: live on or off base?",
                                           f"BAH vs rent math for {b['short']}."))

def bases_hub():
    cards = "".join(
        f'<div class="card"><span class="tag">{b["side"]}</span>'
        f'<h3><a href="/bases/{b["slug"]}.html">{b["name"]}</a></h3>'
        f'<p>{b["intro"][:150]}…</p></div>' for b in BASES)
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Six installations · one BAH rate · very different rents</p>
<h1>Pick your gate. We'll map the pockets.</h1>
<p class="lede">Every Oahu installation draws the same Honolulu County BAH. What differs is the
rent and the drive on the other side of each gate. Each guide below pairs your allowance anchors
with dated rent bands in the neighborhoods people at that base actually commute from.</p>
</div></div>
<div class="wrap">
<div class="grid c2">{cards}</div>
{lead_form("BASES", "pcs-renter")}
</div>'''
    return page("/bases/", "Oahu Military Bases: Live On or Off? Base-by-Base Guides | PCS Oahu",
                "Base-by-base housing guides for JBPHH, Schofield Barracks, MCBH Kaneohe Bay, Camp "
                "Smith, Tripler, and Coast Guard Base Honolulu — BAH anchors vs real rent bands.",
                body, "/bases/")

def build():
    out = {"/index.html": homepage(), "/bases/index.html": bases_hub(),
           "/pcs-to-hawaii/index.html": pcs_to_hawaii()}
    for b in BASES:
        p, h = base_page(b)
        out[p] = h
    return out
