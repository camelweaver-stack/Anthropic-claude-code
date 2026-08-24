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
                        "@graph": [dataset_ld()]})

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
<h2>No, there's no DoDEA school waiting for you</h2>
<p style="max-width:46rem">If your last move was OCONUS or to a CONUS DoDEA installation, reset
that expectation now: Hawaii has zero Department of Defense-run schools. Every military-connected
child here attends a HIDOE public school, the same statewide system every civilian family uses —
see the <a href="/guides/dodea-schools.html">full explainer</a> for why, plus School Liaison
Officer contacts by service branch.</p>
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
market timing. Not sure you should buy at all this tour? Start with the
<a href="/guides/rent-vs-buy.html">rent-vs-buy framework</a> — the horizon, the BAH-purchasing-power
math, and the forced-exit risk — then read the <a href="/sell/">PCS-out guide</a> before you buy,
because the exit is part of the purchase. Numbers here are education, not advice; underwriting is between you and a
lender you choose.</p>
{lead_form("BUY", "pcs-buyer",
  heading="Thinking about buying this tour?",
  blurb="Join the list for the buyer-side refresh: entitlement math updates, condo-approval notes, "
        "and market medians as they move. First access when full service opens.")}
</div>'''
    return page("/buy/", "VA Loans on Oahu 2026: Entitlement Math, Condo Approval, Leasehold | PCS Oahu",
                "The flagship VA buyer brief for Oahu: full vs partial entitlement at island "
                "prices, the condo-approval reality at a $530K median, and the leasehold trap.",
                body, "/buy/")

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
                                   "HARPTA, rent-vs-sell math, and VA seller notes.")]})

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
one (see the <a href="/guides/dodea-schools.html">contacts by service branch</a> if you don't
already have a name and number). <strong>Before housing:</strong> run candidate addresses through
the HIDOE school finder;
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
                body, "/guides/")

def dodea_schools():
    qas = [
      ("Does Hawaii have DoDEA (Department of Defense) schools?",
       "No. The Hawaii State Department of Education is explicit on this: 'There are no DOD "
       "schools in Hawaiʻi, including those on military installations. All public schools are "
       "part of the Hawaiʻi State Department of Education.' Every military-connected child on "
       "Oahu, Kauai, or Hawaii Island attends a HIDOE public school — the same statewide system "
       "every civilian family uses. DoDEA's own domestic footprint confirms the same thing from "
       "the other direction: its Americas region runs schools in Alabama, Georgia, Kentucky, New "
       "York, North Carolina, South Carolina, Virginia, Puerto Rico, and Cuba — not Hawaii."),
      ("Why do so many incoming families assume Hawaii has DoDEA schools?",
       "Because a real subset of military moves does land on a DoDEA campus — installations like "
       "Fort Campbell, Fort Bragg, Fort Knox, West Point, and Guantanamo Bay all have "
       "Defense-run schools, and every OCONUS tour does too. Hawaii looks like it should belong "
       "in that group — bases, high military density, its own culture — but it's a U.S. state, "
       "and Hawaii is also the only state in the country with a single statewide school district. "
       "Both facts point away from a DoD-run system: state schools serve everyone, DoDEA schools "
       "don't operate here at all."),
      ("Who do I contact about Hawaii schools before I PCS in?",
       "Your service's School Liaison Officer, not a school directly and not HIDOE's general "
       "line — they exist specifically to walk incoming military families through enrollment, "
       "and which one you contact depends on your service and which installation you're assigned "
       "to. Contacts for every branch are below. HIDOE is direct about the limits of "
       "pre-arrival planning too: 'the school your child can attend will be dependent on where "
       "you will live,' so the liaison officer is who can actually orient you before you have an "
       "address."),
      ("What is Federal Impact Aid and why does it matter for military families?",
       "It's a federal program that reimburses local school districts for the property-tax "
       "revenue they lose to tax-exempt federal land — military bases chief among them — and for "
       "educating children whose parents serve in the uniformed services or work on federal "
       "property. Hawaii's Department of Education says Impact Aid statewide 'helps offset costs "
       "for school materials and resources, substitute teachers, student transportation, school "
       "utilities such as electricity, and other services,' funded specifically because of how "
       "many military-connected students the state educates. It's part of why HIDOE actively "
       "tracks and supports military-impacted schools rather than treating military enrollment as "
       "incidental."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Schools · the question every incoming family asks</p>
<h1>Does Hawaii have DoDEA schools? No — here's what that actually means</h1>
<p class="lede">If your last PCS was OCONUS, or to Fort Bragg, Fort Campbell, Fort Knox, or West
Point, you got used to Defense-run schools on or near base. Hawaii doesn't work that way. Every
military kid here attends a Hawaii public school — which is a bigger structural difference than it
sounds, and it changes what you do before you sign a lease.</p>
</div></div>
<div class="wrap">
<h2>The direct answer</h2>
<p style="max-width:46rem">Hawaii has zero DoDEA schools. The Hawaii State Department of
Education's own military-families page answers this exact question in its FAQ: <strong>"Are there
any Department of Defense (DOD) schools in Hawaiʻi? There are no DOD schools in Hawaiʻi, including
those on military installations. All public schools are part of the Hawaiʻi State Department of
Education."</strong> DoDEA's own site confirms it from the other side — its domestic (Americas)
schools sit in Alabama, Georgia, Kentucky, New York, North Carolina, South Carolina, Virginia,
Puerto Rico, and Cuba. Hawaii isn't on that list, and it isn't a gap in DoDEA's coverage — the
state's public system serves every child here, military or not.
(<a href="https://hawaiipublicschools.org/enrolling-in-school/military-families/">Hawaii DOE,
Military Families</a>; <a href="https://www.dodea.edu/about/about-dodea/dodea-schools-worldwide">DoDEA
Schools Worldwide</a>.)</p>

<h2>Who this applies to</h2>
<p style="max-width:46rem">Anyone PCSing to Oahu, Kauai (Pacific Missile Range Facility), or Hawaii
Island (Pōhakuloa) with kids — but it matters most if your prior assumption came from real
experience with a DoDEA system: OCONUS tours, or CONUS DoDEA installations like Fort Campbell,
Fort Bragg, Fort Jackson, Fort Stewart, Fort Rucker, or West Point. The adjustment isn't just
paperwork — DoDEA schools are federally operated and built around a transient military population
by design; HIDOE is a state system built for everyone, with its own calendar, culture, and process
(see the <a href="/schools/">Hawaii schools guide</a> for how the statewide-district structure and
Geographic Exceptions actually work once you have an address).</p>

<h2>Why Hawaii ended up this way</h2>
<p style="max-width:46rem">Two facts explain it, and they reinforce each other. First, Hawaii is
the only state with a single statewide public school district — there's no county or city district
line to have DoDEA carve a niche around, the way it can at a single installation inside a mainland
county system. Second, Hawaii's military-connected student population is large enough, and
geographically embedded enough across Oahu especially, that the state built its own
military-family-support infrastructure into HIDOE directly rather than a separate federal system
sitting alongside it — transition centers, a named military liaison, and School Liaison Officer
coordination by service branch, covered below.</p>

<h2>Who to actually contact — by service</h2>
<p style="max-width:46rem">HIDOE is direct about this: <strong>"the school your child can attend
will be dependent on where you will live"</strong> — there's no pre-enrollment before you have an
address. What you <em>can</em> do before then is contact your service's School Liaison Officer,
whose job is exactly this transition:</p>
{rates([
  ("Navy / Air Force / Space Force (JBPHH, PMRF)", "Cherise Yamasaki (elem.), Kimberly Meyer (middle/high) · 808-306-9247"),
  ("Army (Tripler, Shafter, Schofield, Wheeler, Pōhakuloa)", "Tamsin Keone, Jin Castiglione · 808-787-5644"),
  ("Marine Corps (MCBH, Camp Smith)", "Seon Lecher · 808-496-2019"),
  ("Coast Guard (Base Honolulu, Sand Island)", "Stacey Sawyer · 808-842-2089"),
  ("Hawaiʻi National Guard (HIARNG / HIANG)", "LTC Natalie Hayes · 808-672-1315 / CMSgt Maryann Martin · 808-789-1672", True),
], "Hawaii DOE, Military Families page (accessed August 2026) — verify current names and numbers "
   "there before calling, since liaison staffing changes.")}

<h2>What HIDOE builds in for military families</h2>
<p style="max-width:46rem">Two things worth knowing exist, beyond the liaison network. Hawaii
schools that carry a large military-connected population are formally designated
<strong>military-impacted schools</strong>, and a subset earn <strong>Purple Star</strong>
recognition for supporting incoming and transitioning military students specifically — HIDOE
publishes the current list on the same military-families page. Separately, <strong>Federal Impact
Aid</strong> reimburses Hawaii schools for the property-tax base they lose to tax-exempt federal
land (bases) and for educating children of service members and federal employees — HIDOE describes
it as helping cover "school materials and resources, substitute teachers, student transportation,
school utilities such as electricity, and other services at schools statewide." Neither of these
changes which school your child attends, but they're a useful signal that Hawaii's system is built
around military families rather than treating them as an afterthought.</p>

<h2>Next steps</h2>
<ol style="max-width:46rem">
<li><strong>Call your service's School Liaison Officer</strong> from the table above as soon as
orders are in hand — before you have an address, they can still orient you on the process and
timing.</li>
<li><strong>Don't shop schools before housing.</strong> Assignment runs through your home address,
not the installation you report to — see the <a href="/schools/">Hawaii schools guide</a> for the
HIDOE address lookup and the Geographic Exception process if you want a different school.</li>
<li><strong>Start records and health paperwork mainland-side.</strong> The <a
href="/guides/school-transition.html">school transition guide</a> covers the enrollment sequence
in order, including Hawaii's immunization and TB-clearance requirements.</li>
<li><strong>Ask your gaining installation about a transition center</strong> if your child is
changing schools mid-year — HIDOE runs these specifically to support military-connected and other
transient students.</li>
</ol>

<p style="max-width:46rem">Sourced from the Hawaii State Department of Education's Military
Families page and DoDEA's own school-location pages, verified <strong>August 22, 2026</strong>.
Liaison names and phone numbers change with staffing — confirm current contacts at the HIDOE link
above before relying on any number here.</p>
{lead_form("DODEASCHOOLS", "pcs-renter",
  heading="PCSing in with kids?",
  blurb="Join the list for the family-side brief: school-liaison updates, enrollment timing "
        "notes, and first access when full service opens.")}
</div>'''
    p = "/guides/dodea-schools.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article",
         "headline": "Does Hawaii have DoDEA schools? No — here's what that actually means",
         "description": "Hawaii has zero Department of Defense schools — every military-connected "
                        "child attends the statewide Hawaii DOE public system. What that means for "
                        "incoming families, who to contact by service branch, and how Impact Aid "
                        "and Purple Star designations fit in.",
         "datePublished": "2026-08-22", "dateModified": "2026-08-22",
         "author": {"@type": "Organization", "name": "PCS Oahu"},
         "publisher": {"@type": "Organization", "name": "PCS Oahu"},
         "mainEntityOfPage": DOMAIN + p}]}
    return p, page(p, "Does Hawaii Have DoDEA Schools? The Answer for Military Families | PCS Oahu",
                "Hawaii has no DoDEA schools — every military child attends the statewide Hawaii "
                "DOE system. School Liaison Officer contacts by service branch, why Hawaii differs "
                "from OCONUS and CONUS DoDEA installations, and how Impact Aid fits in. Sourced "
                "and dated.",
                body, "/schools/", jsonld=ld)

def onbase_waitlist():
    qas = [
      ("How do I get on the on-base housing waitlist for Oahu before I arrive?",
       "It depends on which side of the island's system your orders point at. On the Navy side "
       "(Joint Base Pearl Harbor-Hickam), start with the Housing Early Assistance Tool (HEAT) on "
       "the Navy's CNIC site — it opens your file and a Housing Service Center counselor contacts "
       "you within one business day — but know its stated limit: HEAT does not place you on a "
       "wait list and cannot improve your position on one. The waitlist itself is managed by the "
       "JBPHH Housing Service Center, which takes appointments up to 30 days before arrival. On "
       "the Army side, you apply to Island Palm Communities directly, and their posted guidelines "
       "contain the single most valuable mechanic on this page: an inbound soldier's eligibility "
       "date is backdated to the date they departed their last duty station — if they apply "
       "within 7 days of arriving. Miss that window and your date is just your application date."),
      ("Does joining an on-base housing waitlist on Oahu cost anything or commit me to living on base?",
       "No and no. Applying costs nothing on any Oahu installation, and holding a waitlist spot "
       "doesn't obligate you to accept a home — you can shop off-base pockets the whole time. The "
       "commitments start when a home is offered: under Island Palm Communities' posted "
       "guidelines, declining an adequate offer moves you to the bottom of the list with your "
       "eligibility date reset to the day you declined. So the free option is real, but understand "
       "what an offer does to it before one arrives."),
      ("Who actually runs the on-base family housing waitlists on Oahu?",
       "Family housing is privatized, so there are two layers: the private partner that owns and "
       "leases the homes, and the military housing office that manages eligibility and, on the "
       "Navy side, the waitlist itself. Per the DoD's MilitaryINSTALLATIONS directory: at JBPHH, "
       "Ohana Military Communities (a Hunt Companies partnership) manages the Navy-side homes and "
       "Hickam Communities the Air Force side, with the Navy Housing Service Center managing the "
       "waitlist; across the Army footprint (Schofield, Wheeler, Helemano, Fort Shafter, Tripler, "
       "AMR, Red Hill) it's Island Palm Communities, which runs its own two regional lists; at "
       "Marine Corps Base Hawaii it's Ohana Military Communities' Marine housing operation. "
       "Operators and terms change — the housing office at your gaining installation is always "
       "the source of record."),
      ("What determines my position on an Oahu housing waitlist?",
       "Eligibility date plus priority category, not first-come-first-served alone. Island Palm "
       "Communities' posted guidelines show the shape: position runs by eligibility date within "
       "priority categories (accompanied personnel assigned to the installation sit high; key-and-"
       "essential billets and certain medical cases move ahead), your bedroom eligibility comes "
       "from command-sponsored dependents on your orders, you can be on only one IPC regional "
       "list at a time, and an assignment requires at least twelve months remaining on your tour. "
       "On the Navy side, MilitaryINSTALLATIONS states waitlist priority is determined by local "
       "business agreements, with EFMP status potentially conferring higher priority. The rules "
       "differ by service and change over time — ask your housing office for the current written "
       "rules for your exact situation."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Renting · the free option most families set up too late</p>
<h1>The Oahu on-base housing waitlist: apply the day orders drop</h1>
<p class="lede">Every Oahu housing decision runs better with a waitlist position you're free to
use or ignore. Joining costs nothing, commits you to nothing — and on the Army side, applying
promptly can backdate your position to the day you left your last duty station. Here's how the
lists actually work, installation by installation, from the operators' own published rules.</p>
</div></div>
<div class="wrap">
<h2>The direct answer</h2>
<p style="max-width:46rem">Get on the list the day orders drop, even if you expect to live off
base. It's free, it holds while you shop <a href="/neighborhoods/">off-base pockets</a>, and
position compounds: the earlier your eligibility date, the earlier the offer. The mechanics that
follow are the parts most families learn too late — the tool that <em>doesn't</em> put you on the
list, the seven-day window that backdates your position, and what declining an offer costs.</p>

<h2>Navy side (JBPHH): HEAT starts the file — it does not hold your place</h2>
<p style="max-width:46rem">The Navy's <strong>Housing Early Assistance Tool (HEAT)</strong> is the
right first move and the most misunderstood one. Per the Navy's own CNIC housing site, HEAT lets
you start the housing process online before or after orders, and "someone from the Navy HSC will
contact you within one business day." But the same page is explicit about its limit: HEAT
<strong>"does not place you on a wait list and cannot improve your position on a housing wait
list."</strong> The waitlist itself runs through the <strong>JBPHH Housing Service Center</strong>,
which — per the DoD's MilitaryINSTALLATIONS directory — takes appointments up to 30 days before
arrival (808-474-1820/1821) and expects a DD Form 1746 application with a copy of your PCS orders
and dependency documentation. The homes themselves are run by Ohana Military Communities on the
Navy side and Hickam Communities on the Air Force side; the HSC manages the waitlist, and
priority "is determined by local Business Agreements," with EFMP families potentially entitled to
higher assignment priority.
(<a href="https://ffr.cnic.navy.mil/Navy-Housing/HEAT/">CNIC, Navy Housing — HEAT</a>;
<a href="https://installations.militaryonesource.mil/military-installation/joint-base-pearl-harbor-hickam/housing/government-housing">MilitaryINSTALLATIONS,
JBPHH housing</a>.)</p>

<h2>Army side (Island Palm Communities): the seven-day backdating rule</h2>
<p style="max-width:46rem">Island Palm Communities runs two regional lists — <strong>North</strong>
(Helemano, Schofield Barracks, Wheeler) and <strong>South</strong> (Aliamanu, Fort Shafter,
Tripler, Red Hill) — and you can be on only one at a time. The mechanic worth planning around, from
IPC's own posted waitlist guidelines: <strong>an inbound soldier's eligibility date is the date
they departed their last duty station, as long as they apply for housing within 7 days of
arrival.</strong> Apply inside that window and your position reflects your whole transit; apply
later, or from an off-post lease, and your eligibility date is simply your application date. The
same document sets the other rules families trip on: assignment requires at least twelve months
remaining on your tour, bedroom eligibility follows command-sponsored dependents on orders, and
<strong>declining an adequate offer moves you to the bottom of the list with your eligibility date
reset to the declination date</strong>. One caution on that document: the version IPC posts is
dated 2016, so treat it as the shape of the system and confirm current terms at the leasing
office before you rely on any line of it.
(<a href="https://www.islandpalmcommunities.com/">Island Palm Communities</a> and its posted
<a href="https://medialibrarycf.entrata.com/12710/MLv3/2023/08/22/012503/64e50b8fd25e7748.pdf">Guidelines
for Waitlist and Housing Assignment</a>.)</p>

<h2>Marine Corps side (MCBH): Ohana's Marine housing operation</h2>
<p style="max-width:46rem">Family housing at Marine Corps Base Hawaii runs through Ohana Military
Communities' Marine housing arm — the same Hunt Companies partnership as the Navy side, operating
separately for MCBH with communities concentrated around Kaneohe Bay and leeward Oahu. Application
runs through <a href="https://www.ohanamarinefamilyhousing.com/">Ohana's Marine family housing
site</a> and the MCBH housing office; as everywhere on this page, apply with orders in hand and
ask the office for the current written waitlist rules rather than relying on a forum thread.</p>

<h2>Who this applies to</h2>
<p style="max-width:46rem">Every inbound accompanied family, whichever way you're leaning. If
you're <strong>set on living on base</strong>, the eligibility-date mechanics above are the whole
game — apply immediately and protect your date. If you're <strong>leaning off base</strong>, the
free list position is your hedge against a brutal pocket search — many families bridge on
<a href="/tla/">TLA</a> while holding a list spot and let the better option win. If you're
<strong>undecided</strong>, the <a href="/on-base/">on-base housing guide</a> walks the
BAH-allotment trade in full: on base you spend exactly your allowance; off base, if your grade's
rate beats your pocket's band in the <a href="/bah-report/">BAH Reality Report</a>, the difference
is yours.</p>

<h2>Next steps</h2>
<ol style="max-width:46rem">
<li><strong>Orders in hand → apply the same week.</strong> Navy/Air Force: submit HEAT, then book
the HSC appointment (up to 30 days pre-arrival). Army: apply to the correct IPC regional list.
Marines: start with Ohana's Marine housing site and the MCBH housing office.</li>
<li><strong>Army families: calendar the 7-day window.</strong> Applying within 7 days of arrival
backdates your eligibility to your departure date — it's the cheapest position upgrade in the
entire system.</li>
<li><strong>Get the decline rules in writing</strong> before an offer comes. Ask: what counts as
an adequate offer, what happens to my date if I decline, and how long do I have to answer.</li>
<li><strong>Tell the office about EFMP status at application</strong> — on both the Navy and Army
sides, documented EFMP status can change priority or the type of home offered, and the review has
its own timeline.</li>
<li><strong>Run the off-base comparison in parallel.</strong> The <a href="/on-base/">on-base
guide</a> and the <a href="/neighborhoods/">pocket table</a> are the two halves of that
decision.</li>
</ol>

<p style="max-width:46rem">Compiled from the Navy's CNIC housing pages, the DoD's
MilitaryINSTALLATIONS directory, and Island Palm Communities' published guidelines, and verified
<strong>August 23, 2026</strong>. Waitlist rules, operators, and phone numbers change — the
housing office at your gaining installation is the source of record, and nothing here is a promise
of housing or a timeline.</p>
{lead_form("WAITLIST", "pcs-renter",
  heading="Working the on-vs-off decision?",
  blurb="Join the list and the arrival brief pairs the current on-base wait picture with the "
        "off-base rent bands for your gaining installation.")}
</div>'''
    p = "/guides/on-base-waitlist.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article",
         "headline": "The Oahu on-base housing waitlist: apply the day orders drop",
         "description": "How Oahu's privatized-housing waitlists actually work, installation by "
                        "installation: HEAT's real role on the Navy side, Island Palm Communities' "
                        "7-day eligibility-backdating rule on the Army side, decline consequences, "
                        "and EFMP priority — from the operators' own published rules.",
         "datePublished": "2026-08-23", "dateModified": "2026-08-23",
         "author": {"@type": "Organization", "name": "PCS Oahu"},
         "publisher": {"@type": "Organization", "name": "PCS Oahu"},
         "mainEntityOfPage": DOMAIN + p}]}
    return p, page(p, "Oahu On-Base Housing Waitlists: HEAT, the 7-Day Rule, Decline Costs | PCS Oahu",
                "How Oahu military housing waitlists really work: HEAT starts your file but holds "
                "no place, Island Palm's 7-day rule backdates Army positions to your departure "
                "date, and declining an offer resets your date. Sourced and dated.",
                body, "/bases/", jsonld=ld)

def vehicle_registration():
    qas = [
      ("How long do I have to register my car after it arrives in Hawaii?",
       "Within 30 days of the vehicle's arrival on Oahu you must obtain either a Hawaii "
       "registration or an out-of-state permit (City & County of Honolulu). The process runs "
       "through a safety inspection that initially ‘fails’ because the car has no Hawaii "
       "registration yet — that failed certificate is what lets you register, and you return to "
       "the inspection station within 30 days of that failed check for the passing sticker once "
       "you’re registered. Confirm current timelines with Honolulu’s Department of Customer "
       "Services — forms and windows change."),
      ("Do active-duty military have to pay Hawaii's vehicle weight tax?",
       "Nonresident active-duty service members and their spouses are exempt from Honolulu’s "
       "motor-vehicle weight tax when they submit a properly completed Non-Resident Certificate, "
       "Form CS-L(MVR)50, with each registration transaction (the county notes the current form is "
       "dated 04/2026). You can also keep your home-state plates instead, via the out-of-state "
       "permit, Form CS-L(MVR)27. Verify both forms’ current versions on honolulu.gov."),
      ("Where do I register a PCS vehicle on Oahu?",
       "At any Satellite City Hall (City & County of Honolulu, Department of Customer Services), "
       "with an on-base option at Joint Base Pearl Harbor-Hickam for the initial out-of-state "
       "registration. Bring your out-of-state title/registration, Hawaii insurance, orders, the "
       "failed Hawaii safety-inspection certificate, and the applicable form."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">PCS logistics · after the car lands</p>
<h1>Registering your car in Hawaii: the arrival clock</h1>
<p class="lede">Shipping the car is one process; putting Hawaii plates on it is another. There is no
one-counter, same-day path — the sequence runs insurance → a safety inspection that deliberately
‘fails’ first → registration → back for the passing sticker. Active-duty families get a real
choice and a weight-tax exemption most people don’t know about.</p>
</div></div>
<div class="wrap">
<h2>The direct answer</h2>
<p style="max-width:46rem">When your POV arrives (see <a href="/vehicle-shipping/">vehicle
shipping</a> for getting it here), the registration sequence on Oahu is:</p>
<ol style="max-width:46rem">
<li><strong>Know the deadline: 30 days.</strong> Per the City &amp; County of Honolulu, within
30 days of the vehicle's arrival on Oahu you must obtain either a Hawaii registration or an
out-of-state permit. Start the steps below the week the car lands.</li>
<li><strong>Get Hawaii auto insurance first.</strong> You need proof of Hawaii insurance to obtain
a safety inspection, and the inspection is required for every registration transaction.</li>
<li><strong>Take the car for a Hawaii safety inspection — which ‘fails.’</strong> With no Hawaii
registration yet, the station issues a <em>failed</em> certificate. That failed certificate is not
a problem; it is the document that lets you register.</li>
<li><strong>Register at a Satellite City Hall</strong> (or the Joint Base Pearl Harbor-Hickam option
for the initial out-of-state registration), choosing plates or an out-of-state permit — see below.</li>
<li><strong>Return for the passing sticker.</strong> Per the City &amp; County of Honolulu, you go
back to the inspection station within <strong>30 days</strong> of that original failed check to
complete the passing inspection once you’re registered.</li>
</ol>
<h2>The choice active-duty families have</h2>
<p style="max-width:46rem">Nonresident active-duty service members (and spouses) don’t have to
convert to Hawaii plates at all — there are two legitimate paths:</p>
<p style="max-width:46rem"><strong>Keep your home-state plates</strong> via the out-of-state permit,
<strong>Form CS-L(MVR)27</strong>. Or <strong>register in Hawaii</strong> with <strong>Form
CS-L(MVR)50</strong>, the Non-Resident Certificate, which also claims the exemption below. Both are
recognized options; pick based on your home state’s renewal cost and how long the tour runs.</p>
<div class="warn"><strong>The weight-tax exemption worth knowing.</strong> Nonresident active-duty
military and their spouses are <strong>exempt from Honolulu’s motor-vehicle weight tax</strong>
when they file a properly completed CS-L(MVR)50 with each registration transaction — the county
notes the current form is dated 04/2026. That exemption is easy to miss and it is not automatic:
the form has to be submitted every time. (You still pay the standard state registration fee and the
safety-inspection fee, which the state updated in 2025 — check the current schedule on honolulu.gov.)</div>
<h2>What to bring</h2>
<p style="max-width:46rem">Your out-of-state title and current registration, proof of Hawaii
insurance, a copy of your orders, the <em>failed</em> Hawaii safety-inspection certificate, and the
applicable form (CS-L(MVR)50 to register in Hawaii with the exemption, or CS-L(MVR)27 for the
out-of-state permit). If the car came by sea, keep the shipping paperwork from the port with the
packet — you may need it to prove arrival.</p>
<div class="warn"><strong>Honest limits.</strong> Forms, fees, inspection rules, and timelines are
set by the City &amp; County of Honolulu (Department of Customer Services) and the Hawaii Department
of Transportation, and they change — the county even versions the CS-L(MVR)50 by date. This guide is
orientation compiled from honolulu.gov and hidot.hawaii.gov and verified <strong>August 5, 2026</strong>;
confirm the current forms and fees with the county before you go, and use your installation’s
in-processing brief. Nothing here is legal or tax advice.</p>
<p style="max-width:46rem">This is the last step of the car’s PCS journey; the first is the
<a href="/vehicle-shipping/">shipment itself</a>, and the registration deadline is one of the arrival
tasks tracked on the <a href="/pcs-checklist/">PCS timeline checklist</a>. Setting up on base first?
See <a href="/on-base/">on-base housing</a>.</p>
{lead_form("VEHREG", "pcs-renter",
  heading="Working the arrival checklist?",
  blurb="Join the list and the arrival brief sequences the registration, inspection, and insurance "
        "steps against your report window so the safety-inspection clock never catches you late.")}
</div>'''
    p = "/guides/vehicle-registration.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article",
         "headline": "Registering your car in Hawaii: the arrival clock",
         "description": "How PCS families register an imported vehicle on Oahu — the safety-inspection "
                        "sequence, the 30-day clock, the nonresident-military weight-tax exemption "
                        "(Form CS-L(MVR)50), and the out-of-state permit option.",
         "datePublished": "2026-08-05", "dateModified": "2026-08-05",
         "author": {"@type": "Organization", "name": "PCS Oahu"},
         "publisher": {"@type": "Organization", "name": "PCS Oahu"},
         "mainEntityOfPage": DOMAIN + p}]}
    return p, page(p, "Registering a Car in Hawaii on PCS Orders: Forms, Weight Tax, Inspection | PCS Oahu",
                "How military families register an imported vehicle on Oahu: the safety-inspection "
                "sequence and 30-day clock, the nonresident weight-tax exemption (CS-L(MVR)50), and "
                "the out-of-state permit (CS-L(MVR)27). Sourced and dated.",
                body, "/guides/", jsonld=ld)

def rent_vs_buy():
    qas = [
      ("Should I buy a house on Oahu as a military member?",
       "There is no universal yes or no — the honest answer is a three-question framework. First, "
       "your horizon: buying rarely pays off unless you'll hold the home long enough to earn back "
       "the transaction costs, and a two-to-three-year tour is short for that. Second, purchasing "
       "power: at a June 2026 single-family median around $1,275,000 (Honolulu Board of REALTORS® "
       "data in public reports), even Oahu's top-in-the-force BAH buys a condo more realistically "
       "than a house for most grades. Third, the exit: PCS orders don't wait for the market, so "
       "the question isn't only 'can I buy' but 'what happens when I have to leave.' Run all three "
       "before a listing does the deciding for you."),
      ("Is BAH enough to buy a house on Oahu?",
       "It depends on grade and what you're buying. Every Oahu installation shares one BAH rate "
       "(Honolulu County MHA); 2026 with-dependents anchors run about $3,663 for an E-5 and $3,912 "
       "for an E-6, with a ceiling near $5,040 (DTMO 2026 tables, effective January 1, 2026). "
       "Against a $1,275,000 single-family median, that BAH points more comfortably at Oahu's "
       "$530,000-median condo market than at a house — and a VA loan's no-down-payment, no-PMI "
       "structure plus BAH being tax-free (Military OneSource) is what makes the math work at all. "
       "HOA fees and the VA condo-approval list decide whether a given condo is actually reachable."),
      ("How long do I need to stay for buying to beat renting on Oahu?",
       "Long enough to earn back what it costs to get in and out — the VA funding fee (unless "
       "you're exempt for a service-connected disability, per VA.gov), closing costs, and the "
       "selling costs on the far end. There's no single magic number, but a break-even measured in "
       "years, not months, is the honest frame, and a standard PCS tour can be shorter than that. "
       "If orders might move you before you'd clear the round-trip costs, renting and pointing the "
       "same BAH at a landlord is not the lesser choice — it's often the disciplined one."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Buying · the decision before the decision</p>
<h1>Rent or buy on Oahu with a VA loan? The honest framework</h1>
<p class="lede">Oahu hands military buyers a rare combination — the highest BAH in the force pointed
at a zero-down VA loan — and that combination makes "just buy, you're throwing money away renting"
sound obvious. On this island it isn't. Three questions decide it, and none of them is the listing
price.</p>
</div></div>
<div class="wrap">
<h2>The direct answer</h2>
<p style="max-width:46rem">Buying beats renting when you'll hold long enough to earn back the cost
of getting in and out, when your BAH actually reaches the kind of home you want at Oahu prices, and
when you can absorb the exit on someone else's timeline. Miss any one and renting the same BAH is
frequently the stronger move. Here's each question in island numbers.</p>
<h2>1 — Your horizon vs. the round-trip cost</h2>
<p style="max-width:46rem">Buying isn't free to enter or leave. On the way in there's a one-time
<strong>VA funding fee</strong> (waived if you receive — or are eligible to receive — VA
compensation for a service-connected disability, per <a href="https://www.va.gov/housing-assistance/home-loans/funding-fee-and-closing-costs/">VA.gov</a>)
plus ordinary closing costs; on the way out there are selling costs. You earn those back through
appreciation and principal paydown over <em>years</em>, not months. A standard PCS tour of two to
three years can be shorter than that break-even — so the first question isn't "can I qualify," it's
"will I hold this home long enough for the round trip to pay for itself?" If the answer is uncertain
because orders are uncertain, that uncertainty has a dollar value, and it favors renting.</p>
<h2>2 — What your BAH actually reaches here</h2>
<p style="max-width:46rem">Oahu is one BAH market — every installation draws the same Honolulu
County rate — and it's the top of the national table. But it meets some of the country's highest
prices:</p>
{rates([
  ("Oahu median single-family (June 2026)", MED_SF, True),
  ("Oahu median condo (June 2026)", MED_CONDO),
  ("BAH, E-5 with dependents (2026)", BAH["e5_dep"]),
  ("BAH, E-6 with dependents (2026)", BAH["e6_dep"]),
  ("BAH ceiling, Honolulu County (2026)", BAH["ceiling"]),
], "BAH: DTMO 2026 tables, effective January 1, 2026 (one Honolulu County MHA covers every Oahu "
   "installation). Medians: Honolulu Board of REALTORS® data as republished in public June 2026 "
   "market reports. Orientation only — verify at source; not a valuation or loan offer.")}
<p style="max-width:46rem">Two structural advantages tilt the math toward the buy side when the
horizon is right. A VA-backed purchase loan needs <strong>no down payment</strong> (up to the
appraised value) and carries <strong>no private mortgage insurance</strong>
(<a href="https://www.va.gov/housing-assistance/home-loans/loan-types/purchase-loan/">VA.gov</a>) —
so the BAH you'd otherwise hand a landlord goes straight at principal and interest. And <strong>BAH
itself is tax-free</strong> — excluded from gross income, not subject to federal or state income
tax (<a href="https://www.militaryonesource.mil/financial-legal/taxes/military-housing-allowance/">Military
OneSource</a>) — which quietly raises the housing budget's real purchasing power versus a civilian
earning the same gross. Against the medians above, that firepower reaches the <a href="/buy/">condo
market</a> far more readily than the single-family market for most grades.</p>
<h2>3 — The exit you don't control</h2>
<div class="warn"><strong>The market won't wait for your orders.</strong> The risk that separates
Oahu from a mainland duty station isn't buying — it's being <em>forced to sell or rent on a PCS
timeline</em> into a single, supply-constrained island market. If values dip the quarter your
orders drop, you sell into that dip or you become a long-distance landlord. Both are legitimate;
neither is free. Before you buy, read the departure side of this decision — the
<a href="/sell/">sell-or-rent-when-you-PCS-out guide</a> covers the accidental-landlord math, and the
<a href="/guides/harpta.html">HARPTA guide</a> covers the 7.25% withholding that comes out of an
Oahu sale at closing — because on this island the exit is part of the purchase.</div>
<h2>Who this applies to</h2>
<p style="max-width:46rem"><strong>Leaning buy</strong> if you have full VA entitlement, a
longer-than-usual tour or plans to keep the home as a rental after you leave, and a target in the
condo band your BAH comfortably covers. <strong>Leaning rent</strong> if your tour is a standard
two-to-three years with real PCS uncertainty, if partial entitlement pulls the county loan limit
back into your math, or if the only homes in reach are leasehold or unapproved condos (both covered
on the <a href="/buy/">VA-loan buyer brief</a>). Renting the same BAH while you learn the island and
watch a pocket is not a failure to build equity — it's buying flexibility, which on a PCS timeline
has real value.</p>
<h2>Next steps</h2>
<ol style="max-width:46rem">
<li><strong>Pin your horizon honestly.</strong> How firm is the tour length, and would you keep the
home as a rental if orders moved you? That answer drives everything below.</li>
<li><strong>Get a Loan Estimate, not a guess.</strong> Ask a VA-experienced lender for the funding
fee (or confirm your exemption), the closing costs, and the real monthly payment <em>including HOA
and insurance</em> before you compare it to rent.</li>
<li><strong>Check tenure and condo approval early.</strong> Confirm fee-simple vs. leasehold and
whether the project is on the VA-approved condo list — see the <a href="/buy/">buyer brief</a> —
before you fall for a price.</li>
<li><strong>Sanity-check the rent side.</strong> Compare against real asking rents for your pocket
in the <a href="/bah-report/">BAH Reality Report</a>, and remember on-base housing trades your whole
BAH for a no-maintenance, no-exit-risk option — see <a href="/on-base/">how on-base housing works</a>.</li>
</ol>
<p style="max-width:46rem">This is a framework compiled from VA.gov, Military OneSource, DTMO 2026
tables, and public Honolulu market reports, and verified <strong>August 6, 2026</strong>. Every
figure changes and every situation differs — nothing here is a valuation, a loan offer,
prequalification, or lending, legal, or tax advice. The break-even math is yours to run with a
lender and, where taxes are involved, a tax professional you choose.</p>
{lead_form("RENTBUY", "pcs-buyer",
  heading="Weighing the rent-or-buy call this tour?",
  blurb="Join the list for the buyer-side refresh: BAH-cycle updates, market medians as they move, "
        "and the rent-band changes that decide the math. First access when full service opens.")}
</div>'''
    p = "/guides/rent-vs-buy.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article",
         "headline": "Rent or buy on Oahu with a VA loan? The honest framework",
         "description": "A decision framework for military buyers weighing rent vs. buy on Oahu: the "
                        "PCS-horizon break-even, what BAH actually reaches at island prices, the "
                        "no-down-payment/no-PMI VA advantage, tax-free BAH, and the forced-exit risk.",
         "datePublished": "2026-08-06", "dateModified": "2026-08-06",
         "author": {"@type": "Organization", "name": "PCS Oahu"},
         "publisher": {"@type": "Organization", "name": "PCS Oahu"},
         "mainEntityOfPage": DOMAIN + p}]}
    return p, page(p, "Rent vs Buy on Oahu with a VA Loan: The Military Framework | PCS Oahu",
                "Should military families rent or buy on Oahu? The honest framework: the PCS break-even "
                "horizon, what BAH reaches at a $1.275M median, the no-down-payment VA advantage, "
                "tax-free BAH, and the forced-exit risk. Sourced and dated.",
                body, "/buy/", jsonld=ld)

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
  <div class="card"><span class="tag">Family</span>
    <h3><a href="/guides/dodea-schools.html">Does Hawaii have DoDEA schools?</a></h3>
    <p>No — every military kid attends the statewide Hawaii DOE system. School Liaison Officer contacts by service branch.</p></div>
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
    <h3><a href="/guides/vehicle-registration.html">Registering your car in Hawaii</a></h3>
    <p>The safety-inspection sequence and 30-day clock, the nonresident weight-tax exemption, and the out-of-state permit option.</p></div>
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
  <div class="card"><span class="tag">Arriving</span>
    <h3><a href="/guides/on-base-waitlist.html">The on-base waitlist, decoded</a></h3>
    <p>HEAT's real role, Island Palm's 7-day backdating rule, and what declining an offer costs your position.</p></div>
  <div class="card"><span class="tag">Buying</span>
    <h3><a href="/guides/rent-vs-buy.html">Rent or buy with a VA loan?</a></h3>
    <p>The honest framework: the PCS break-even horizon, what BAH reaches at island prices, and the forced-exit risk.</p></div>
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
         "mainEntityOfPage": DOMAIN + p}]}
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
    for fn in (spouse, school_transition, pets, harpta, dodea_schools, onbase_waitlist,
               vehicle_registration, rent_vs_buy):
        p, h = fn()
        out[p] = h
    return out
