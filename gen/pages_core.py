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
what to decide before wheels-down.</p>
<p><a class="btn" href="/bah-report/">Read the BAH Reality Report</a>
<a class="btn ghost" href="/pcs-checklist/">Start the PCS checklist</a>
<a class="btn ghost" href="/quiz/">Take the pocket-match quiz</a></p>
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
{lead_form("HOME", "pcs-renter",
  heading="The arrival brief, before you arrive",
  blurb="Join the list and get the current BAH Reality Report, the rent-band refresh for your "
        "gaining base, and a heads-up timed to your report window. First access when full service "
        "opens. No spam. Leave anytime.")}
</div>'''
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "PCS Oahu",
          "url": DOMAIN, "description": "The independent field guide for military PCS moves to and from Oahu."}
    return page("/", "PCS Oahu — The Field Guide for Military Orders to Oahu",
                "Orders to Hawaii? Base-by-base BAH vs rent math, VA loans at Oahu prices, TLA, "
                "schools, and the sell-or-rent call when you PCS out. Independent and honest.",
                body, "/bases/" if False else "", jsonld=ld)

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

def base_page(b):
    prows = [(POCKETS[p][0], POCKETS[p][1]) for p in b["pockets"]]
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
<h2>The rent side, by commute-real pocket</h2>
{rates(prows, RENT_SRC)}
<h2>Commute reality</h2>
<table class="data"><thead><tr><th>Pocket</th><th>What the drive is actually like</th></tr></thead>
<tbody>{commute_rows}</tbody></table>
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
    out = {"/index.html": homepage(), "/bases/index.html": bases_hub()}
    for b in BASES:
        p, h = base_page(b)
        out[p] = h
    return out
