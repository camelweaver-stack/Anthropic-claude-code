from common import *

def bah_report():
    pocket_rows = [(v[0], v[1]) for v in POCKETS.values()]
    qas = [
      ("Do different Oahu bases pay different BAH?",
       "No. All Oahu installations sit inside one Military Housing Area — Honolulu County. BAH "
       "varies by pay grade and dependency status, never by which base you report to."),
      ("What is the 2026 BAH range on Oahu?",
       f"Per DTMO 2026 tables effective {BAH['effective']}, Honolulu County rates run from roughly "
       f"{BAH['floor']} (junior enlisted without dependents) to about {BAH['ceiling']} (senior "
       f"officers with dependents), an increase of {BAH['increase']} over 2025. Verify your exact "
       "grade at the DTMO calculator."),
      ("Does BAH cover average rent on Oahu?",
       "It depends entirely on pocket and bedroom count. Mid-2026 public listing data shows island "
       "medians around $2,700–$3,200 overall, with windward and beach-town pockets well above an "
       "E-5 allowance and several central and leeward pockets comfortably inside it."),
      ("Which Oahu neighborhoods fit an E-5 BAH with dependents?",
       f"At the 2026 with-dependents anchor of {BAH['e5_dep']}, typical 3-bedroom asking bands in "
       "Wahiawa, Waipahu, and much of Pearl City and Aiea fall inside the allowance with room for "
       "utilities. Windward pockets such as Kailua generally do not. Bands are rounded asking rents, "
       "compiled mid-2026."),
      ("Is Kailua affordable on BAH?",
       f"Kailua 3-bedroom asking bands ($4,000–$5,500, mid-2026) begin around where the E-6 "
       f"with-dependents allowance ({BAH['e6_dep']}) ends. Kaneohe prices materially lower for "
       "windward access."),
      ("Where can I download Oahu BAH-vs-rent data?",
       "The BAH Reality Report publishes machine-readable JSON and CSV at pcsoahu.com/data/, free "
       "to reuse with attribution (CC BY 4.0), refreshed each BAH cycle."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Named data brief · refreshed with the annual BAH cycle</p>
<h1>The BAH Reality Report</h1>
<p class="lede">One page, updated each BAH cycle: what the Honolulu County allowance actually is,
what Oahu pockets actually rent for, and where the gap opens. Every figure dated, sourced, and
deliberately rounded — cite it, link it, argue with it.</p>
</div></div>
<div class="wrap">
<p class="eyebrow">Edition: {BUILD_DATE} · BAH effective {BAH["effective"]}</p>
<h2>Part 1 — The allowance</h2>
<p style="max-width:46rem">One MHA covers the island. The {BAH_YEAR} cycle raised Honolulu County
rates by {BAH["increase"]}, keeping Oahu among the highest BAH markets in the force.</p>
{rates([
  ("E-5 with dependents", BAH["e5_dep"]),
  ("E-5 without dependents", BAH["e5_solo"]),
  ("E-6 with dependents", BAH["e6_dep"]),
  ("E-6 without dependents", BAH["e6_solo"]),
  ("Island floor (jr. enlisted, no dep.)", BAH["floor"]),
  ("Island ceiling (sr. officer, w/ dep.)", BAH["ceiling"], True),
], "DTMO " + BAH_YEAR + " tables, Honolulu County MHA. These are published anchors we can source; "
   "pull your exact pay grade from the DTMO BAH calculator before signing anything.")}
<h2>Part 2 — The rents</h2>
{rates(pocket_rows, RENT_SRC)}
<h2>Part 3 — Where the gap opens</h2>
<p style="max-width:46rem">Read the two ledgers together and three honest patterns emerge.</p>
<p><strong>The allowance is strongest mid-island.</strong> An E-5-with-dependents rate of
{BAH["e5_dep"]} clears typical 3-bedroom bands in Wahiawa, Waipahu, and much of Pearl City and
Aiea with room for utilities — which BAH is also meant to cover.</p>
<p><strong>The windward premium is real.</strong> Kailua 3-bedroom bands start where the E-6
allowance ends. Families set on windward living should price Kaneohe first and treat Kailua as a
deliberate splurge, not a default.</p>
<p><strong>Without-dependents rates map to condos, not houses.</strong> {BAH["e5_solo"]}–{BAH["e6_solo"]}
fits the Salt Lake, Kalihi, and downtown 1–2BR bands — the single-service-member market is a condo
market, which is why VA condo approval (see the <a href="/buy/">buying guide</a>) matters here more
than almost anywhere in the country.</p>
<p style="max-width:46rem">Running a blog, group, or unit page? <a href="/embed/">Embed the live widget</a> — it refreshes with each edition.</p>
<section id="cite"><h2>Cite this report</h2>
<p style="max-width:46rem">Journalists, bloggers, and researchers may quote or chart this report
with attribution and a link. Suggested citation:</p>
<p style="max-width:46rem;font-family:'IBM Plex Mono',monospace;font-size:.88rem;background:#fff;
border:1px solid var(--rule);border-radius:6px;padding:.8rem 1rem">PCS Oahu, "The BAH Reality
Report," {BUILD_DATE} edition, pcsoahu.com/bah-report/.</p></section>
<div class="warn"><strong>Honest limits.</strong> Rent bands are compiled from public listing
platforms and rounded on purpose; they describe asking rents, not lease outcomes, and PCS-season
scarcity moves them. This report is a compass, not a valuation.</div>
{lead_form("BAHREPORT", "pcs-renter",
  heading="Get the next edition first",
  blurb="The report refreshes with every BAH cycle and mid-year when rent bands move. Join the "
        "list and it lands in your inbox before it's published here.")}
</div>'''
    return page("/bah-report/", "The BAH Reality Report: 2026 Oahu BAH vs Actual Rents | PCS Oahu",
                "The citable data brief: 2026 Honolulu County BAH anchors vs dated rent bands by "
                "Oahu pocket — where the allowance clears the market and where the gap opens.",
                body, "/bah-report/",
                jsonld={"@context": "https://schema.org",
                        "@graph": [dataset_ld(), faq_ld(qas)]})

def bah_report_2026_archive():
    import re as _re
    live = bah_report()
    m = _re.search(r"<main>(.*)</main>", live, _re.S)
    body = ('<div class="wrap"><div class="warn" style="margin-top:1.5rem"><strong>Archived '
            'edition (August 2026).</strong> Preserved so citations never break. The current '
            'edition, refreshed with each BAH cycle, lives at '
            '<a href="/bah-report/">pcsoahu.com/bah-report/</a>.</div></div>' + m.group(1))
    arch = DOMAIN + "/bah-report/2026-edition/"
    return page("/bah-report/2026-edition/",
        "The BAH Reality Report — August 2026 Edition (Archived) | PCS Oahu",
        "Archived August 2026 edition of the BAH Reality Report: 2026 Honolulu County BAH "
        "anchors vs dated Oahu rent bands. Current edition at /bah-report/.",
        body, "/bah-report/",
        jsonld={"@context": "https://schema.org",
                "@graph": [dataset_ld(url=arch, at_id=arch + "#dataset",
                                      same_as=DOMAIN + "/bah-report/")]})

def neighborhoods():
    rows = "".join(f"<tr><td><a href='/neighborhoods/{k}.html'>{v[0]}</a></td>"
                   f"<td class='num'>{v[1]}</td></tr>" for k, v in POCKETS.items())
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Eleven pockets, one honest table</p>
<h1>Oahu neighborhoods, commute-first</h1>
<p class="lede">Mainland instinct says pick the neighborhood, then find the commute. Oahu punishes
that order of operations. Start from your gate, shortlist the pockets that survive a 0630 drive
test, then let the rent bands break the tie.</p>
</div></div>
<div class="wrap">
<h2>The pocket table</h2>
<table class="data"><thead><tr><th>Pocket</th><th>Mid-2026 rent bands</th></tr></thead>
<tbody>{rows}</tbody></table>
<p style="max-width:46rem;font-size:.9rem;color:#5b6b73">{RENT_SRC}</p>
<h2>How to read it</h2>
<p style="max-width:46rem"><strong>Central value:</strong> Wahiawa and Waipahu hold the island's
most forgiving bands. <strong>The family defaults:</strong> Mililani and Ewa/Kapolei trade newer
stock and planned-community amenities against longer drives to south-shore gates.
<strong>Close-in condos:</strong> Salt Lake, Moanalua, and Kalihi are the minutes-to-gate play for
JBPHH, Camp Smith, and Tripler. <strong>The windward premium:</strong> Kaneohe is the practical
windward option; Kailua is the deliberate one.</p>
<p style="max-width:46rem">Each <a href="/bases/">base guide</a> pairs these pockets with the
commute they actually produce. For a family decision, layer in the
<a href="/schools/">schools guide</a> — Hawaii's statewide district changes how address and school
connect.</p>
{lead_form("NEIGHBORHOODS", "pcs-renter")}
</div>'''
    return page("/neighborhoods/", "Oahu Neighborhoods for Military Families, Commute-First | PCS Oahu",
                "Eleven Oahu pockets with dated mid-2026 rent bands, organized by what matters on "
                "orders: the gate you'll drive to at 0630 for the next three years.",
                body, "/neighborhoods/")

def schools():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">One state, one district</p>
<h1>Hawaii schools for arriving military families</h1>
<p class="lede">Hawaii runs the only statewide public school district in the country. That single
fact rearranges the mainland playbook: there are no district lines to shop, attendance is set by
school-level geographic boundaries, and moving between schools runs through a formal Geographic
Exception (GE) process rather than a district transfer.</p>
</div></div>
<div class="wrap">
<h2>What actually determines your school</h2>
<p style="max-width:46rem">Your address maps to a specific home school through the Hawaii
Department of Education's school-finder boundaries. Before signing any lease or contract, run the
exact address through the HIDOE lookup — pockets can split between schools street by street, and
listing-site school labels are frequently wrong.</p>
<h2>The Geographic Exception, honestly</h2>
<p style="max-width:46rem">A GE lets you request a school other than your home school. Approval
depends on capacity and is not guaranteed; application windows matter (the main window typically
falls in early spring for the following year, with late applications handled case by case).
Military families arriving mid-cycle should contact both the home school and the desired school
directly, and loop in the school liaison officer at the gaining installation — that office exists
for exactly this.</p>
<h2>Timing notes for PCS season</h2>
<p style="max-width:46rem">Hawaii public schools start earlier than most mainland calendars —
typically late July to early August. A summer PCS that feels comfortable by mainland timing can
land after the first bell here. The Interstate Compact on Educational Opportunity for Military
Children applies in Hawaii and covers enrollment, placement, and eligibility transitions —
know it by name when you register.</p>
<div class="note"><strong>What this guide won't do.</strong> No school rankings and no
neighborhood steering — that's both house policy and fair-housing law. We map process and timing;
you weigh schools with your own visits and the state's own public data at the HIDOE site.</div>
{lead_form("SCHOOLS", "pcs-renter")}
</div>'''
    return page("/schools/", "Hawaii Schools for Military Families: The Statewide District, "
                "Explained | PCS Oahu",
                "Hawaii's one statewide school district changes the PCS playbook: home-school "
                "boundaries, Geographic Exceptions, early calendars, and the Interstate Compact.",
                body, "/schools/",
                jsonld=article_ld("/schools/", "Hawaii schools for arriving military families",
                                  "How the statewide district, GE process, and calendar work."))

def buy():
    qas = [
      ("Is there a VA loan limit on Oahu in 2026?",
       "Not if you have full entitlement — approval then rests on income, debts, and residual "
       "income, not a county cap. With partial entitlement (an active prior VA loan), the county "
       "conforming limit drives zero-down math; published 2026 figures for Hawaii cluster around "
       "$1.2M–$1.25M with a state ceiling of $1,873,675 — verify the exact Honolulu County figure "
       "on the FHFA map before running numbers."),
      ("Can I use a VA loan on an Oahu condo?",
       "Only if the specific project is on the VA's approved condo list or gets approved during "
       "escrow. On an island where the median condo ran about $530,000 in June 2026 public data "
       "versus $1,275,000 for a single-family home, condo approval is the difference between a "
       "real market and a closed one — check the list before you tour."),
      ("What is leasehold property in Hawaii?",
       "Some Hawaii listings sell the building but not the land beneath it — you lease the land "
       "for a term, pay lease rent, and face reversion or renegotiation when it ends. Leasehold "
       "prices look like bargains next to fee-simple and are the classic mainland-buyer trap. "
       "Confirm tenure on every listing before falling for a price."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The flagship buyer brief</p>
<h1>The VA loan on Oahu: entitlement math at island prices</h1>
<p class="lede">Oahu is simultaneously one of the best VA markets in the country — the highest BAH
in the force pointed at a zero-down loan — and one of the easiest places to make a six-figure
mistake. Three things decide which one you get: your entitlement, the condo approval list, and the
word "leasehold."</p>
</div></div>
<div class="wrap">
<h2>1 — Entitlement, in island numbers</h2>
<p style="max-width:46rem"><strong>Full entitlement</strong> (no active VA loan, or a prior one
restored): no loan limit applies. Zero-down at any price your income, debts, and residual income
support. On Oahu the binding constraint is the payment, not a cap.</p>
<p style="max-width:46rem"><strong>Partial entitlement</strong> (you kept a VA loan on a mainland
house): the county conforming limit re-enters the math, because lenders need the VA guaranty plus
your cash to cover 25% of the loan. Hawaii's 2026 published figures cluster around $1.2M–$1.25M
for the county limit with a statutory state ceiling of $1,873,675 — but sources differ on the
exact Honolulu number, so pull it from the FHFA county map yourself before you shop. Rough shape
of the shortfall: entitlement used on the mainland reduces the guaranty available here, and every
guaranty dollar short of 25% becomes down payment.</p>
{rates([
  ("Oahu median single-family (June 2026)", MED_SF, True),
  ("Oahu median condo (June 2026)", MED_CONDO),
  ("2026 national baseline conforming limit", "$832,750"),
  ("2026 Hawaii ceiling (statutory)", "$1,873,675"),
], "Medians: Honolulu Board of REALTORS® data as republished in public June 2026 market reports. "
   "Limits: FHFA 2026 announcements. All figures for orientation only — verify at source; "
   "not a valuation or loan offer.")}
<h2>2 — The condo reality</h2>
<p style="max-width:46rem">At a {MED_SF} single-family median, the condo market is where most Oahu
VA buying actually happens — and VA condo financing only works in projects on the VA-approved
list (or approved during your escrow, which takes time you may not have in a competitive offer).
Before touring any building: check the project on the VA condo report, ask about the association's
owner-occupancy and litigation status, and price the HOA fee into your payment — Oahu HOA fees
routinely rival mainland car payments and lenders count every dollar of them.</p>
<h2>3 — The leasehold warning</h2>
<div class="warn"><strong>Read tenure before price.</strong> Hawaii sells property two ways:
fee-simple (you own the land) and leasehold (you own the improvements and rent the land under
them until a lease expiration). Leasehold listings can price hundreds of thousands below
comparable fee-simple units — that discount is the market pricing the lease term, the lease rent,
and the reversion risk. VA financing on leasehold is possible only within strict term rules, and
resale gets harder every year the lease runs down. If a listing looks too cheap for its pocket,
tenure is the first thing to check.</div>
<h2>The honest close</h2>
<p style="max-width:46rem">BAH pointed at a mortgage builds equity in one of the country's most
supply-constrained markets; it also concentrates risk on one island, and PCS orders don't wait for
market timing — read the <a href="/sell/">PCS-out guide</a> before you buy, because the exit is
part of the purchase. Numbers here are education, not advice; underwriting is between you and a
lender you choose.</p>
{lead_form("BUY", "pcs-buyer",
  heading="Thinking about buying this tour?",
  blurb="Join the list for the buyer-side refresh: entitlement math updates, condo-approval notes, "
        "and market medians as they move. First access when full service opens.")}
</div>'''
    return page("/buy/", "VA Loans on Oahu 2026: Entitlement Math, Condo Approval, Leasehold | PCS Oahu",
                "The flagship VA buyer brief for Oahu: full vs partial entitlement at island "
                "prices, the condo-approval reality at a $530K median, and the leasehold trap.",
                body, "/buy/", jsonld=faq_ld(qas))

def sell():
    qas = [
      ("Does HARPTA apply to military sellers in Hawaii?",
       "Yes — HARPTA applies to the disposition of Hawaii real property whoever sells it. The "
       "Hawaii Department of Taxation calls it a common misperception that HARPTA doesn't apply "
       "when the seller is a Hawaii resident: it does apply, and the buyer must withhold 7.25% of "
       "the amount realized unless the seller gives the buyer Form N-289 certifying an exemption. "
       "Whether you qualify as a Hawaii resident person turns on domicile and the purpose of your "
       "presence in the State, so a mainland state of legal residence doesn't settle it by itself. "
       "See the full HARPTA guide, and confirm your status with the Department or a tax "
       "professional before listing."),
      ("Should I sell or rent my Oahu house when I PCS out?",
       "Run five lines: likely market rent, PITI plus HOA plus GET on rental income, remote "
       "property management (commonly around 8–12% of rent), an honest vacancy and maintenance "
       "reserve, and the equity a sale would free. Keeping the house bets on Oahu's supply "
       "constraint and a PCS-refreshed tenant pool; selling ends single-island risk and can "
       "capture the primary-residence capital-gains exclusion, which has special timing "
       "extensions for qualifying military moves."),
      ("What happens to my VA entitlement when I sell my Hawaii home?",
       "Selling and paying off the VA loan starts entitlement restoration for your next duty "
       "station, but restoration requires filing — it is not automatic. If a VA buyer assumes "
       "your loan instead, your entitlement stays tied up unless the buyer substitutes their "
       "own."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The other half of the cycle</p>
<h1>PCSing out: sell the house or become a landlord?</h1>
<p class="lede">Every arrival on this island is somebody else's departure. If you bought here and
the orders now point outbound, you're choosing between selling into one of the country's tightest
markets or running a rental from five time zones away. Both are legitimate. Here's the math and
the paperwork, without a listing pitch.</p>
</div></div>
<div class="wrap">
<h2>The HARPTA facts, straight</h2>
<p style="max-width:46rem">HARPTA is Hawaii's withholding law on sales of Hawaii real property —
a 7.25% withholding on the <em>amount realized</em>, per the Hawaii Department of Taxation. It's
withholding against potential tax, not the tax itself; refunds of over-withholding run through
state filings. The part that trips up military sellers: <strong>being a Hawaii resident does not
switch it off by itself.</strong> The Department names that as a common misperception — HARPTA
applies even when the seller is a resident, and the buyer must withhold unless the seller
<em>gives the buyer Form N-289</em> certifying an exemption. Residency for this purpose is a tax
status determined by domicile and the purpose of your presence in the State, so keeping a mainland
state of legal residence doesn't resolve it in either direction on its own. Timing your sale
against your residency status and the N-288B filing deadline is a real-money question for a tax
professional, not a listing agent — the mechanics are laid out in the
<a href="/guides/harpta.html">full HARPTA guide</a>.</p>
<h2>Rent-vs-sell, on one napkin</h2>
<p style="max-width:46rem">The accidental-landlord math has five lines. Run them before any
emotional attachment votes:</p>
{rates([
  ("Likely market rent for your pocket", "see the pocket table"),
  ("PITI + HOA + GET on rental income", "your actual numbers"),
  ("Property management from 5 time zones", "commonly ~8–12% of rent"),
  ("Vacancy + maintenance reserve", "budget honestly, not hopefully"),
  ("Equity you'd free by selling", "vs. the June 2026 " + MED_SF + " SF median", True),
], "Frameworks only — every line is your data, not ours. Hawaii levies General Excise Tax on "
   "rental income; management percentages vary by company. Verify everything independently.")}
<p style="max-width:46rem"><strong>The case for keeping it:</strong> Oahu's chronic supply
constraint, a tenant pool refreshed by every PCS cycle, and a mortgage possibly priced below
today's rates. <strong>The case for selling:</strong> concentrated single-island risk, the
management drag from overseas, and — if it's been your primary residence — the federal capital-gains
exclusion window (with special extensions for qualifying military moves; confirm your dates with a
tax professional before deciding).</p>
<h2>If you sell with a VA loan on the house</h2>
<p style="max-width:46rem">Selling pays off the loan and starts the path to restoring your
entitlement for the next duty station — file the restoration paperwork; it isn't automatic. If
your buyer is also VA, your loan may be assumable at its existing rate, which in a high-rate year
can be worth real money in your sale terms; assumption releases your entitlement only if the
assuming buyer substitutes their own. Know both facts before negotiating.</p>
{lead_form("SELL", "pcs-seller", context="sell",
  heading="Orders pointing off-island?",
  blurb="Join the list for the seller-side brief: market medians as they move, HARPTA and "
        "residency notes, and first access when full service opens.")}
</div>'''
    return page("/sell/", "PCSing Out of Hawaii: Sell or Rent Your Oahu Home? HARPTA, VA Sellers | PCS Oahu",
                "The departure brief: HARPTA facts for residents vs non-residents, the "
                "accidental-landlord math from five time zones, and VA seller entitlement notes.",
                body, "/sell/",
                jsonld={"@context": "https://schema.org",
                        "@graph": [article_ld("/sell/",
                                   "PCSing out: sell or rent your Oahu home?",
                                   "HARPTA, rent-vs-sell math, and VA seller notes."), faq_ld(qas)]})

def tla():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Wheels-down to keys</p>
<h1>TLA and interim housing, without the panic</h1>
<p class="lede">The gap between landing and leasing is where Oahu PCS budgets go to die — unless
you know how Temporary Lodging Allowance works here and stage the search before you fly.</p>
</div></div>
<div class="wrap">
<h2>How TLA works in Hawaii, in brief</h2>
<p style="max-width:46rem">Hawaii is an OCONUS location for lodging purposes, so inbound members
generally draw <strong>TLA</strong> (not the CONUS TLE): a per-diem-based reimbursement for
temporary lodging and meals, typically authorized in 10-day increments up to 60 days inbound,
subject to your service's rules and your commander's authorization — and conditioned on showing an
active housing search. Rates key off the Honolulu locality per diem and your family size. The
numbers change; the rules have edges. <strong>Your installation housing office and the current
Joint Travel Regulations are the authority</strong> — treat every dollar figure you read anywhere
else, including here, as orientation.</p>
<p style="max-width:46rem">Companion page: <a href="/tla/field-notes.html">the lodging field notes</a> — options by installation and the off-base booking filters.</p>
<h2>The practical sequence</h2>
<p style="max-width:46rem"><strong>Before you fly:</strong> book TLA-eligible lodging near your
gaining base (on-base lodging first — it simplifies the paperwork and the commute), stage your
rental documents (LES, orders, references, pet records), and shortlist pockets from your
<a href="/bases/">base guide</a>. <strong>Week one:</strong> in-processing, housing office
briefing, get on the on-base waitlist even if you intend to rent out in town — it's a free
option. <strong>Weeks two through four:</strong> tour your shortlist at commute hours, apply
fast when something fits the band. PCS-season inventory does not wait for deliberation.</p>
<div class="note"><strong>Pet reality.</strong> Hawaii's rabies-free status means a real
quarantine program with a direct-airport-release path that takes months of advance bloodwork.
Start the checklist the week orders drop — it is the single most common PCS-to-Hawaii timeline
mistake — and note that pet-friendly rentals and TLA lodging are both scarcer here.</div>
{lead_form("TLA", "pcs-renter",
  heading="Landing soon?",
  blurb="Join the list and get the arrival-week brief: current rent bands for your gaining base "
        "and the search-documents checklist, timed to your report window.")}
</div>'''
    return page("/tla/", "TLA in Hawaii: Interim Housing Between Wheels-Down and Keys | PCS Oahu",
                "How Temporary Lodging Allowance works for a Hawaii PCS — the 60-day shape, the "
                "practical search sequence, and the pet-quarantine timeline everyone underestimates.",
                body, "/tla/",
                jsonld=article_ld("/tla/", "TLA and interim housing on Oahu",
                                  "The wheels-down-to-keys sequence for arriving families."))

def spouse():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The second career in every PCS</p>
<h1>Spouse employment on Oahu: the honest landscape</h1>
<p class="lede">Oahu's job market is real but particular: government, healthcare, tourism, and
logistics dominate; wages often trail the cost of living; and remote work has quietly become the
strongest option many military spouses have. Here's the factual lay of the land and where the
actual programs live.</p>
</div></div>
<div class="wrap">
<h2>The structural facts</h2>
<p style="max-width:46rem">Hawaii participates in interstate licensure compacts for a growing list
of professions (nursing among them) and has expedited-licensure provisions for military spouses —
check your profession's board at the state DCCA before assuming you must re-license from scratch.
Federal hiring preference for military spouses applies at the island's large federal workforce,
and USAJOBS postings for Oahu run continuously. Mainland-remote roles keep mainland salaries
against Hawaii costs — for many households the single best financial outcome — but confirm an
employer's Hawaii work authorization and the time-zone reality (Hawaii sits 2–3 hours behind the
West Coast and observes no daylight saving).</p>
<h2>Where the real programs are</h2>
<p style="max-width:46rem">The Military Spouse Employment Partnership and SECO (Spouse Education
and Career Opportunities) counseling run force-wide; each Oahu installation's family-support
center (Military and Family Support Center at JBPHH, Army Community Service at Schofield, Marine
Corps Family Team Building at MCBH) runs employment workshops and local hiring events, heaviest
in PCS season. State workforce services through American Job Centers Hawaii are open to spouses
from day one. This page links you to the programs; it is not career advice, and every program's
current terms live on its own site.</p>
{lead_form("SPOUSE", "pcs-renter")}
</div>'''
    p = "/guides/spouse-employment.html"
    return p, page(p, "Military Spouse Employment on Oahu: Licensure, Remote Work, Programs | PCS Oahu",
                "The factual landscape for working spouses on a Hawaii PCS: licensure compacts, "
                "federal preference, remote-work realities, and where the real programs live.",
                "".join([body]), "/guides/",
                jsonld=article_ld(p, "Spouse employment on Oahu", "Licensure, remote work, programs."))

def school_transition():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Moving kids mid-stream</p>
<h1>The school transition, managed</h1>
<p class="lede">A Hawaii PCS moves kids into a new school system, an earlier calendar, and a
genuinely different culture — usually all in the same month. The logistics are manageable if you
run them in order.</p>
</div></div>
<div class="wrap">
<h2>The sequence</h2>
<p style="max-width:46rem"><strong>Orders in hand:</strong> request records from the losing school
and connect with the school liaison officer at the gaining installation — every Oahu base has
one. <strong>Before housing:</strong> run candidate addresses through the HIDOE school finder;
the address decides the home school (see the <a href="/schools/">schools guide</a> for how
Geographic Exceptions work). <strong>On arrival:</strong> enroll with orders, proof of address,
health records (Hawaii enforces its immunization and TB-clearance requirements at enrollment —
start these mainland-side), and the records packet. The Interstate Compact covers placement
continuity, extracurricular eligibility, and graduation-requirement flexibility for military
kids — cite it by name if you hit friction.</p>
<h2>The soft landing</h2>
<p style="max-width:46rem">Hawaii's school culture carries its own vocabulary and rhythms —
'ohana nights, hō'ike performances, and a local culture your kids will absorb faster than you
will. The consistent advice from families who've done it: arrive curious, join early (sports
and clubs start with the July/August calendar), and give it a full semester before judging the
fit. Anchoring the transition is also the strongest argument for choosing housing stability —
pocket first, then school process, then lease length that matches your tour.</p>
{lead_form("SCHOOLTRANSITION", "pcs-renter")}
</div>'''
    p = "/guides/school-transition.html"
    return p, page(p, "PCS School Transition to Hawaii: Records, Enrollment, the Compact | PCS Oahu",
                "The order of operations for moving kids in a Hawaii PCS: records, the HIDOE "
                "address lookup, immunization timing, and the Interstate Compact.",
                body, "/guides/",
                jsonld=article_ld(p, "The school transition, managed",
                                  "Enrollment sequence for a Hawaii PCS."))

def pets():
    qas = [
      ("Can my pet skip quarantine when we PCS to Hawaii?",
       "Usually yes — through the Direct Airport Release program — but only if every step of "
       "Hawaii's rabies-prevention checklist is completed on time: microchip, rabies vaccinations, "
       "an OIE-FAVN rabies antibody blood test through an approved lab, the mandated waiting "
       "period after passing results, and paperwork submitted before arrival. Miss a step or a "
       "date and the fallback is quarantine at the owner's expense. The Hawaii Department of "
       "Agriculture's Animal Quarantine Station publishes the authoritative checklist — start it "
       "the week orders drop."),
      ("How early should military families start the Hawaii pet process?",
       "The moment orders are in hand. The blood-test-plus-waiting-period sequence is measured in "
       "months, not weeks, and it is the single most common Hawaii PCS timeline failure. Families "
       "with a short-fuse report date should call the Animal Quarantine Station directly and loop "
       "in their transportation office about pet spots on flights."),
      ("Does the military pay to ship pets to Hawaii?",
       "Policies on pet-transportation reimbursement for PCS moves have changed in recent years "
       "and differ by service and circumstances — verify current entitlements with your "
       "transportation office and the Joint Travel Regulations rather than a forum post."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The most-missed deadline in every Hawaii PCS</p>
<h1>Pets to Hawaii: the quarantine clock starts now</h1>
<p class="lede">Hawaii is rabies-free and intends to stay that way, so bringing a dog or cat means
clearing the state's Animal Quarantine program. Done right and early, most military pets walk out
of the airport the day they land. Done late, the fallback is quarantine at your expense — and
"late" arrives faster than almost anyone expects.</p>
</div></div>
<div class="wrap">
<h2>The sequence, in order</h2>
<p style="max-width:46rem"><strong>Microchip first</strong> (the chip must precede the blood
test), <strong>rabies vaccinations</strong> per the state's two-vaccine rules, the
<strong>OIE-FAVN antibody blood test</strong> processed through an approved lab, then the
<strong>mandatory waiting period</strong> that begins only after a passing result reaches the
program — followed by health certificate, documents, and fees submitted ahead of arrival for
<strong>Direct Airport Release</strong>. Each step gates the next; the calendar math is why this
page says "the week orders drop" and means it. The Hawaii Department of Agriculture's Animal
Quarantine Station checklist is the single source of truth — print it, date it backward from
your report date, and treat every deadline as a formation time.</p>
<div class="warn"><strong>The three classic failures.</strong> Testing before the microchip
(restarts the sequence), assuming the waiting period runs from the blood draw rather than the
lab result, and booking pet cargo space last — summer PCS season and airline heat embargoes
squeeze pet capacity exactly when everyone needs it. Island Pet transport services and your
transportation office both exist for this; ask early.</div>
<h2>After wheels-down</h2>
<p style="max-width:46rem">Pet-friendly TLA lodging and rentals are both scarcer on Oahu than
mainland instinct expects — filter your <a href="/tla/">interim-housing</a> plan and your
<a href="/neighborhoods/">pocket shortlist</a> for pets from day one, and have vet records staged
in your rental-documents packet. Verify every rule, fee, and form directly with the Hawaii
Department of Agriculture — program details change, and this guide is orientation, not the
checklist itself.</p>
{lead_form("PETS", "pcs-renter",
  heading="PCSing with pets?",
  blurb="Join the list and the arrival brief includes the pet-timeline reminder sequence, dated "
        "backward from your report window.")}
</div>'''
    p = "/guides/pets-to-hawaii.html"
    return p, page(p, "Pets to Hawaii on PCS Orders: Quarantine, Direct Airport Release | PCS Oahu",
                "The Hawaii pet quarantine sequence for military moves — microchip, OIE-FAVN "
                "test, waiting period, Direct Airport Release — and the three classic failures.",
                body, "/guides/", jsonld=faq_ld(qas))

def guides_hub():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Field notes</p>
<h1>The guide shelf</h1>
<p class="lede">Everything on this site that isn't a number: process guides for the parts of a
Hawaii PCS that paperwork alone doesn't cover.</p>
</div></div>
<div class="wrap">
<div class="grid c2">
  <div class="card"><span class="tag">Family</span>
    <h3><a href="/guides/spouse-employment.html">Spouse employment on Oahu</a></h3>
    <p>Licensure compacts, federal preference, the remote-work math, and where the real programs live.</p></div>
  <div class="card"><span class="tag">Family</span>
    <h3><a href="/guides/school-transition.html">The school transition, managed</a></h3>
    <p>Records, enrollment, the early calendar, and the Interstate Compact — in the order that works.</p></div>
  <div class="card"><span class="tag">Settling</span>
    <h3><a href="/guides/utilities.html">Utilities, honestly</a></h3>
    <p>The highest electric rates in the country, the AC question, and the two internet providers.</p></div>
  <div class="card"><span class="tag">Family</span>
    <h3><a href="/guides/healthcare.html">Healthcare &amp; TRICARE</a></h3>
    <p>The enrollment sequence, the geography of care, and the EFMP fine print.</p></div>
  <div class="card"><span class="tag">Family</span>
    <h3><a href="/guides/childcare.html">Childcare: start now</a></h3>
    <p>MilitaryChildCare.com, realistic waitlists, and fee assistance in parallel.</p></div>
  <div class="card"><span class="tag">Orders</span>
    <h3><a href="/guides/sponsorship.html">Accompanied orders &amp; EFMP</a></h3>
    <p>Hawaii runs accompanied-orders and EFMP screening, not foreign-style command sponsorship.</p></div>
  <div class="card"><span class="tag">Arriving</span>
    <h3><a href="/vehicle-shipping/">Vehicle shipping, end to end</a></h3>
    <p>The one-POV entitlement, PCSmyPOV, the real timeline, the gap-car math, and the 10-day registration clock.</p></div>
  <div class="card"><span class="tag">Arriving</span>
    <h3><a href="/tla/field-notes.html">TLA lodging field notes</a></h3>
    <p>Base lodging by installation, the Hale Koa option, and the off-base filters that matter.</p></div>
  <div class="card"><span class="tag">Arriving</span>
    <h3><a href="/guides/pets-to-hawaii.html">Pets to Hawaii: the quarantine clock</a></h3>
    <p>Microchip, OIE-FAVN, the waiting period, Direct Airport Release — dated backward from your report date.</p></div>
  <div class="card"><span class="tag">Arriving</span>
    <h3><a href="/guides/household-goods.html">Household goods to Hawaii</a></h3>
    <p>The OCONUS move in three shipments — unaccompanied baggage, the sea shipment, storage, pro-gear, and DPS booking.</p></div>
  <div class="card"><span class="tag">Arriving</span>
    <h3><a href="/tla/">TLA &amp; interim housing</a></h3>
    <p>The wheels-down-to-keys sequence, including the pet-quarantine timeline.</p></div>
  <div class="card"><span class="tag">Departing</span>
    <h3><a href="/sell/">PCSing out: sell or rent?</a></h3>
    <p>HARPTA, the accidental-landlord napkin, and VA seller notes.</p></div>
  <div class="card"><span class="tag">Departing</span>
    <h3><a href="/guides/harpta.html">HARPTA, in detail</a></h3>
    <p>The 7.25% withholding on the amount realized, why residency alone doesn't exempt you, and the Form N-288B 10-working-day clock.</p></div>
</div>
{lead_form("GUIDES", "pcs-renter")}
</div>'''
    return page("/guides/", "PCS Oahu Guides: Spouse Employment, Schools, TLA, Selling | PCS Oahu",
                "Process guides for the parts of a Hawaii PCS that numbers alone don't cover — "
                "spouse careers, school transitions, interim housing, and the departure decision.",
                body, "/guides/")

def harpta():
    qas = [
      ("Does HARPTA apply to me if I'm military selling a house on Oahu?",
       "Almost certainly yes — HARPTA applies to the disposition of Hawaii real property regardless "
       "of who sells it. The Hawaii Department of Taxation is explicit that a common misperception "
       "is that HARPTA doesn't apply when the seller is a Hawaii resident: it does apply, and the "
       "buyer must withhold 7.25% of the amount realized unless the seller hands the buyer Form "
       "N-289 certifying an exemption. So the question for a military seller is never 'does HARPTA "
       "apply' — it's 'which exemption or withholding certificate do I qualify for, and did I file "
       "it in time.' Your residency status for this purpose turns on domicile and the purpose of "
       "your presence in Hawaii under TIR 97-1, which is a tax question for the Department or a tax "
       "professional, not something a duty station decides by itself."),
      ("How much is withheld under HARPTA and when is it due?",
       "The buyer withholds 7.25% of the amount realized — not of your equity, and not necessarily "
       "of the sticker price. The amount realized is generally the sales price, but it also includes "
       "the fair market value of any property you receive and any liability the buyer assumes. The "
       "buyer must send the withheld amount to the Department with Forms N-288 and N-288A by the "
       "20th day after the transfer date, which is the day the sale closes and title passes. "
       "Because it's withheld from proceeds at closing, an Oahu-sized sale can tie up a very large "
       "number for months — on a $1,275,000 sale, 7.25% is about $92,400."),
      ("Can I avoid HARPTA withholding by using the $300,000 principal-residence exemption?",
       "On Oahu, usually not. One of the three exemptions certified on Form N-289 covers property "
       "used as the seller's principal residence in the year preceding the transfer where the amount "
       "realized does not exceed $300,000. Oahu prices sit well above that threshold — the June 2026 "
       "medians were about $1,275,000 for a single-family home and $530,000 for a condo — so the "
       "$300,000 ceiling rarely reaches an Oahu sale. The lever that does tend to matter here is "
       "Form N-288B, the application for a withholding certificate, which must reach the Department "
       "no later than 10 working days before the transfer date."),
      ("Does the military capital-gains exception help with HARPTA?",
       "It can, indirectly, but the timing is the whole game. Hawaii conforms to IRC section 121, "
       "which excludes up to $250,000 of gain on a principal residence ($500,000 on a joint return) "
       "if you meet the two-of-five-year ownership and use tests. Members of the uniformed services "
       "on qualified official extended duty can elect to suspend that five-year period for up to 10 "
       "years, which is what keeps the exclusion reachable across a PCS. But an exclusion doesn't "
       "stop the withholding by itself: to eliminate the withholding you file Form N-288B, and if "
       "any gain remains after applying the exclusion, Form N-288B can't be used and the buyer "
       "withholds the full 7.25%."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Leaving Hawaii · the number that surprises outbound sellers</p>
<h1>HARPTA when you PCS out: the 7.25% withholding, Form N-289, and the 10-day clock</h1>
<p class="lede">You sell the Oahu house, you clear escrow, and 7.25% of the sale doesn't come with
you. HARPTA isn't a penalty and it isn't a tax — it's a withholding against tax you may not owe.
But it's withheld at closing, it's sized to an Oahu price, and the paperwork that reduces it has a
deadline that falls <em>before</em> your closing date, not after.</p>
</div></div>
<div class="wrap">
<h2>The direct answer</h2>
<p style="max-width:46rem">Under HARPTA — the Hawaii Real Property Tax Act, section 235-68, Hawaii
Revised Statutes — <strong>every buyer of Hawaii real property must withhold 7.25% of the amount
realized and pay it to the Hawaii Department of Taxation</strong>, unless the seller gives the buyer
a Form N-289 certifying an exemption. It is not a tax. The Department is explicit: the amount
withheld is an <em>estimated tax payment made for the seller</em>, credited against what you
actually owe when you file a Hawaii income tax return for the year of the sale. Over-withhold and
you get it back — eventually. The whole game for an outbound military seller is reducing the
withholding <em>before</em> closing rather than waiting a year to reclaim it.
(<a href="https://files.hawaii.gov/tax/legal/taxfacts/tf2025-2010-1.pdf">Hawaii DOTAX Tax Facts
2010-1, rev. April 2025</a>.)</p>

<h2>What 7.25% actually means at Oahu prices</h2>
<p style="max-width:46rem">The withholding is 7.25% of the <strong>amount realized</strong>, which
is not the same thing as your equity and not always the sticker price. Generally it's the sales
price, but the Department includes the fair market value of any property you receive and any
liability the buyer assumes. Critically, it's calculated on the <em>whole</em> amount realized —
so a seller with modest equity, or none, can still see a large sum withheld from proceeds:</p>
{rates([
  ("Oahu median single-family (June 2026)", MED_SF),
  ("HARPTA withheld on that amount realized", "≈ $92,400", True),
  ("Oahu median condo (June 2026)", MED_CONDO),
  ("HARPTA withheld on that amount realized", "≈ $38,400"),
  ("N-289 principal-residence exemption ceiling", "$300,000"),
], "Withholding rate 7.25% of the amount realized per HRS §235-68 and Hawaii DOTAX Tax Facts 2010-1 "
   "(rev. April 2025); withheld figures are arithmetic on this site's published medians, rounded, "
   "for scale only — not a quote, valuation, or tax computation. Medians: Honolulu Board of "
   "REALTORS® data as republished in public June 2026 market reports.")}
<p style="max-width:46rem">Note what the last line does to the most-cited exemption. The
principal-residence exemption on Form N-289 applies where the amount realized <strong>does not
exceed $300,000</strong> — a ceiling that sits below both Oahu medians. On this island that
exemption is largely theoretical for a typical sale, which is why Oahu sellers end up at Form
N-288B instead.</p>

<h2>Who this applies to — including the resident misperception</h2>
<div class="warn"><strong>Being a Hawaii resident does not switch HARPTA off by itself.</strong>
The Department names this as a common misperception: HARPTA <em>does</em> apply when the seller is
a Hawaii resident — the buyer simply isn't required to withhold if the seller <strong>gives the
buyer Form N-289</strong> stating that the seller is a Hawaii resident. If you don't provide the
form, the buyer must withhold even if the buyer knows you're a resident, and a buyer who fails to
withhold is personally liable for the amount. The form is the mechanism; residency alone isn't.</div>
<p style="max-width:46rem">For a service member the residency question itself is genuinely
fact-specific and worth getting right rather than assuming. The Department defines a resident
person as an individual domiciled in Hawaii <em>or</em> one who resides in the State for other than
a temporary or transitory purpose, and points to <a href="https://files.hawaii.gov/tax/legal/tir/tir97-01.pdf">TIR
97-1, "Determination of Residence Status,"</a> for how that's decided. Keeping a mainland state of
legal residence through a tour here doesn't automatically resolve it in either direction, and
neither does length of time on island. This is the one question on this page worth taking to the
Department or to a tax professional you choose before you list — the answer determines whether
you're filing an N-289 or an N-288B.</p>

<h2>The three N-289 exemptions</h2>
<p style="max-width:46rem">Withholding isn't required if the seller gives the buyer Form N-289
stating the seller's taxpayer identification number and one of the following:</p>
<ol style="max-width:46rem">
<li><strong>The seller is a Hawaii resident person.</strong> See the residency note above.</li>
<li><strong>No gain or loss is recognized</strong> under a nonrecognition provision of the Internal
Revenue Code that Hawaii conforms to, or under a U.S. treaty. Common ones: a section 1031 like-kind
exchange, transfers by gift, transfers by bequest, and transfers incident to divorce. You must
describe the transfer and summarize the law and facts supporting the claim — and if <em>any</em>
gain is recognized in a 1031 exchange, Form N-289 can't be used for it.</li>
<li><strong>Principal residence under $300,000.</strong> The property was used by the seller as a
principal residence for the year preceding the transfer <em>and</em> the amount realized does not
exceed $300,000. As shown above, this rarely reaches an Oahu sale. Note this differs from federal
FIRPTA, where the $300,000 test looks at the <em>buyer's</em> intended use.</li>
</ol>

<h2>The lever that usually matters here: Form N-288B and the 10-working-day clock</h2>
<p style="max-width:46rem">If you don't qualify for an N-289 exemption but you won't owe anywhere
near 7.25% of the sale, the instrument is <strong>Form N-288B</strong>, the Application for
Withholding Certificate, which asks the Department to reduce or eliminate the withholding up front.
It's used where the seller will realize no gain, where the gain is fully covered by the
capital-gains exclusion, or where sale proceeds are insufficient to pay the withholding in full.</p>
<div class="warn"><strong>The deadline falls before closing, and it is hard.</strong> Form N-288B
must be filed with the Department <strong>no later than 10 working days prior to the date of
transfer</strong>. The Department's own instructions state that applications filed later than that
will not be accepted and will be returned to the seller, and that it will not approve a Form N-288B
after the transfer date has passed. Working days, not calendar days — and counted backward from
closing, which means the decision to file lands in the middle of your PCS, not after it.
(<a href="https://files.hawaii.gov/tax/forms/current/n288b_i.pdf">Form N-288B instructions, rev.
2025</a>.)</div>
<p style="max-width:46rem">One trap worth stating plainly: if you're relying on the
principal-residence gain exclusion and <strong>any</strong> amount of gain remains after applying
it, Form N-288B cannot be used, and the buyer is required to withhold the full 7.25% of the amount
realized. Partial relief through N-288B is not available for a partially-excluded gain. And even
when a withholding certificate is issued, you must still file a Hawaii income tax return for the
year of the sale.</p>

<h2>The capital-gains exclusion and the military suspension</h2>
<p style="max-width:46rem">Hawaii conforms to IRC section 121, which lets a seller exclude up to
<strong>$250,000</strong> of gain on a principal residence — <strong>$500,000</strong> on a joint
return — if the seller owned the home at least two years of the five-year period ending on the sale
date, lived in it as a principal residence for at least two of those years, didn't acquire it
through a 1031 exchange in the past five years, and hasn't excluded gain on another home in the two
years before this sale.</p>
<p style="max-width:46rem">The two-of-five-year test is exactly what a PCS breaks — which is why
the military provision exists. Under the federal rules, a member of the uniformed services on
<strong>qualified official extended duty</strong> may elect to suspend that five-year period for up
to <strong>10 years</strong>. Extended duty qualifies when you're serving at a duty station at
least <strong>50 miles</strong> from the home, under a call or order to active duty for an
indefinite period or a definite period of <strong>more than 90 days</strong>
(<a href="https://www.irs.gov/publications/p523">IRS Publication 523</a>). A partial exclusion may
also be available where the sale is due to a change in workplace location, health, or an
unforeseeable event — the category most PCS-driven sales are argued under.</p>
<p style="max-width:46rem">Two cautions. The suspension is a <em>federal</em> election described in
IRS guidance; Hawaii's conformity to section 121 is stated by the Department in Tax Facts 2010-1,
but how the election applies to your Hawaii return is a question to confirm with the Department or
a tax professional rather than assume from this page. And the exclusion is about the tax — it only
touches the withholding through a timely, approved Form N-288B.</p>

<h2>Getting money back if too much was withheld</h2>
<p style="max-width:46rem">Two routes, per the Department. First, file your Hawaii income tax
return after the end of the year; the withholding is credited against the tax and the excess is
refunded. Second, if the return for the year of sale isn't available yet — the usual case for a
summer PCS-season closing — you can apply for a tentative refund on <strong>Form N-288C</strong>.
Either way you must still file a Hawaii return for the year of the sale to report the sale and any
other Hawaii income. One detail worth knowing before you ask your escrow company to fix an error:
<strong>escrow cannot apply for the refund</strong>. Once payment reaches the Department it's
credited to the seller's account, and only the seller can request it back.</p>

<h2>Next steps</h2>
<ol style="max-width:46rem">
<li><strong>Settle your residency status first.</strong> Domicile and the purpose of your presence
under TIR 97-1 decide whether you're on the N-289 path or the N-288B path. Do this before you list,
not during escrow.</li>
<li><strong>Estimate the gain, not the equity.</strong> The Department is blunt that people confuse
the two: you can have no equity and still have taxable gain, particularly after refinancing or
depreciation on a rental period. Depreciation allowed <em>or allowable</em> reduces basis whether or
not you claimed it.</li>
<li><strong>Count 10 working days backward from your target closing.</strong> If Form N-288B is your
route, that date — not closing — is your real deadline. Put it on the PCS calendar alongside the
other clocks in the <a href="/pcs-checklist/">PCS timeline checklist</a>.</li>
<li><strong>Decide sell-vs-rent with the withholding in the math.</strong> A 7.25% hold on proceeds
changes what a sale actually frees up this year. Run it against the accidental-landlord numbers in
the <a href="/sell/">sell-or-rent departure brief</a>.</li>
<li><strong>Take the return itself to a professional.</strong> Forms and current rates are on the
Department's site; its technical section is reachable at 808-587-1577, and forms by phone at
808-587-4242 or toll-free 1-800-222-3229. For deeper background the Department points to TIR
2017-01.</li>
</ol>

<h2>Sources</h2>
<ul style="max-width:46rem">
<li><a href="https://files.hawaii.gov/tax/legal/taxfacts/tf2025-2010-1.pdf">Hawaii Department of
Taxation, Tax Facts 2010-1, "Understanding HARPTA" (rev. April 2025)</a> — the 7.25% rate, amount
realized, the resident misperception, the N-289 exemptions, the 20th-day payment deadline, N-288C
refunds, and section 121 conformity.</li>
<li><a href="https://files.hawaii.gov/tax/forms/current/n288b_i.pdf">Hawaii DOTAX, Instructions for
Form N-288B (rev. 2025)</a> — the 10-working-day filing deadline and what happens to late
applications.</li>
<li><a href="https://files.hawaii.gov/tax/legal/tir/tir97-01.pdf">Hawaii DOTAX, TIR 97-1,
"Determination of Residence Status"</a> — how residency is determined.</li>
<li><a href="https://www.irs.gov/publications/p523">IRS Publication 523, "Selling Your Home"</a> —
the section 121 exclusion amounts and the uniformed-services suspension of the five-year test.</li>
</ul>
<p style="max-width:46rem">Compiled from the sources above and verified <strong>August 16, 2026</strong>.
Rates, thresholds, and forms change; the Department's published forms and Tax Facts govern, not this
page. Nothing here is tax, legal, or accounting advice, an opinion on your residency status, or a
computation of what you will owe — those are for the Department of Taxation or a tax professional
you choose.</p>
{lead_form("HARPTA", "pcs-seller", context="sell",
  heading="Selling the Oahu house on this set of orders?",
  blurb="Join the list for the seller-side brief: HARPTA and residency notes as the Department "
        "updates them, market medians as they move, and first access when full service opens.")}
</div>'''
    p = "/guides/harpta.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article",
         "headline": "HARPTA when you PCS out of Hawaii: the 7.25% withholding, Form N-289, and the 10-day clock",
         "description": "How Hawaii's HARPTA withholding works for outbound military sellers on Oahu: "
                        "7.25% of the amount realized, why residency alone doesn't exempt you, the three "
                        "Form N-289 exemptions, the Form N-288B 10-working-day deadline, and the "
                        "uniformed-services suspension of the section 121 five-year test.",
         "datePublished": "2026-08-16", "dateModified": "2026-08-16",
         "author": {"@type": "Organization", "name": "PCS Oahu"},
         "publisher": {"@type": "Organization", "name": "PCS Oahu"},
         "mainEntityOfPage": DOMAIN + p},
        faq_ld(qas)]}
    return p, page(p, "HARPTA for Military Sellers on Oahu: 7.25% Withholding, N-289, N-288B | PCS Oahu",
                "HARPTA explained for outbound military sellers on Oahu: the 7.25% withholding on the "
                "amount realized, why being a Hawaii resident doesn't exempt you without Form N-289, "
                "the $300,000 ceiling that rarely fits Oahu, and the Form N-288B 10-working-day clock.",
                body, "/sell/", jsonld=ld)

def household_goods():
    # Body sourced from gen/content/household-goods.body.html (the page's <main>), re-emitted
    # through page() so it carries the current nav, footer, identity graph, and Ask launcher.
    body = open(os.path.join(os.path.dirname(__file__), "content", "household-goods.body.html")).read()
    return page("/guides/household-goods.html",
        "Shipping Household Goods to Hawaii on PCS Orders: UB, HHG, Storage | PCS Oahu",
        "How the OCONUS household-goods move to Oahu works — unaccompanied baggage that lands "
        "first, the sea shipment, storage, pro-gear, weight allowances, and DPS booking. Sourced and dated.",
        body, "/guides/")

def build():
    out = {
        "/bah-report/index.html": bah_report(),
        "/neighborhoods/index.html": neighborhoods(),
        "/bah-report/2026-edition/index.html": bah_report_2026_archive(),
        "/schools/index.html": schools(),
        "/buy/index.html": buy(),
        "/sell/index.html": sell(),
        "/tla/index.html": tla(),
        "/guides/index.html": guides_hub(),
        "/guides/household-goods.html": household_goods(),
    }
    for fn in (spouse, school_transition, pets, harpta):
        p, h = fn()
        out[p] = h
    return out
