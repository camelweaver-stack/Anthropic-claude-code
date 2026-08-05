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
    return page("/bah-report/2026-edition/",
        "The BAH Reality Report — August 2026 Edition (Archived) | PCS Oahu",
        "Archived August 2026 edition of the BAH Reality Report: 2026 Honolulu County BAH "
        "anchors vs dated Oahu rent bands. Current edition at /bah-report/.",
        body, "/bah-report/")

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
       "HARPTA is Hawaii's withholding on real-estate sales by non-residents — currently 7.25% "
       "of the gross sale price per the Hawaii Department of Taxation. It does not apply to "
       "Hawaii residents at closing. Service members who kept a mainland state of legal "
       "residence under SCRA are typically non-residents for HARPTA purposes even after years "
       "on island — confirm your status with a tax professional before listing."),
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
<p style="max-width:46rem">HARPTA is Hawaii's withholding law on real-estate sales by
<em>non-residents</em> — currently a 7.25% withholding on the gross sale price, per the Hawaii
Department of Taxation (verify the current rate and forms there; it's withholding against
potential tax, not the tax itself, and refunds of over-withholding run through state filings).
The part that matters for military sellers: <strong>if you're a Hawaii resident at closing,
HARPTA doesn't apply.</strong> Residency for this purpose is a tax status, not a feeling — service
members who kept a mainland state of legal residence under SCRA protections are typically
non-residents for HARPTA even after three years on island. Timing your sale relative to your
departure and your residency status is a real-money question for a tax professional, not a
listing agent.</p>
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

def household_goods():
    qas = [
      ("How does shipping household goods to Hawaii work on a PCS?",
       "A move to Oahu is an OCONUS shipment, which splits your belongings into streams booked "
       "through the Defense Personal Property System (DPS): unaccompanied baggage that ships "
       "expedited so it arrives soon after you do, your main household goods that move by sea and "
       "can take weeks to months, and anything you leave behind in non-temporary storage for the "
       "tour. You build every shipment in DPS after uploading your orders; your local "
       "transportation office and the DoD call center (833-MIL-MOVE) are the authoritative help "
       "desk for entitlements."),
      ("Does professional gear count against my weight allowance for Hawaii?",
       "No. Professional books, papers, and equipment needed for your job (PBP&E, or pro-gear) "
       "are shipped separately and do not count against your household-goods weight limit — "
       "separate and clearly mark those boxes. A spouse's professional gear can be authorized up "
       "to 500 pounds when approved. Source: Military OneSource, verified August 2026; confirm "
       "your specifics with your transportation office."),
      ("Can Hawaii's weight allowance be lower than the mainland?",
       "It can. Household-goods weight allowances are set by grade and dependency status in the "
       "Joint Travel Regulations, but selected OCONUS duty stations carry administratively reduced "
       "allowances (DTMO publishes the list), and government-furnished or partly furnished on-base "
       "housing can make a full shipment impractical even when it's allowed. Confirm your exact "
       "allowance in DPS and with your transportation office before you decide what ships."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">PCS logistics · the third shipping decision</p>
<h1>Household goods to Hawaii: the OCONUS move, in order</h1>
<p class="lede">Getting your things to Oahu isn't one shipment — it's three decisions made at once:
what flies with you as unaccompanied baggage, what crosses the Pacific by sea as household goods,
and what stays behind in storage for the tour. Book them together in DPS the week orders drop, and
plan for the weeks-to-months gap before the sea shipment lands.</p>
</div></div>
<div class="wrap">
<h2>The direct answer</h2>
<p style="max-width:46rem">A move to Oahu is an <strong>OCONUS</strong> shipment (the same category
as Alaska and overseas). In the Defense Personal Property System — <strong>DPS</strong>, where you
upload orders and create every shipment — your belongings split into streams:</p>
<ul style="max-width:46rem">
<li><strong>Unaccompanied baggage (UB).</strong> The part of your allowance shipped by an
expedited mode so it arrives soon after you do — seasonal clothing, essential kitchen items, and
gear for dependents. It is meant to bridge the gap before the main shipment.</li>
<li><strong>Household goods (HHG).</strong> The main shipment, which moves by sea and, per Military
OneSource, "can take weeks to months to be delivered." This is the one you plan the gap around.</li>
<li><strong>Non-temporary storage (NTS).</strong> What you deliberately leave behind — stored for
the duration of the tour rather than shipped to a small, expensive island market.</li>
</ul>
<div class="warn"><strong>One clock, booked once.</strong> All three streams are created in DPS
after your orders upload. Book early — Oahu summer PCS season (May–August) is the busy window, and
capacity, packing dates, and delivery slots tighten exactly when everyone needs them.</div>
<h2>What doesn't count against your weight</h2>
<p style="max-width:46rem"><strong>Pro-gear.</strong> Professional books, papers, and equipment you
need for your job (PBP&amp;E) ship separately and do <em>not</em> count against your household-goods
weight limit — separate them and mark the boxes clearly. A spouse's professional gear can be
authorized up to <strong>500 pounds</strong> when approved. That distinction matters most for
service members and spouses whose tools or reference materials are heavy.</p>
<h2>The weight-allowance reality on Oahu</h2>
<p style="max-width:46rem">Your household-goods allowance is set by <strong>pay grade and dependency
status</strong> in the Joint Travel Regulations, and DPS shows your exact figure once orders are
loaded — pull it from there rather than a forum table. Two Hawaii-specific wrinkles:</p>
<p style="max-width:46rem"><strong>OCONUS administrative reductions.</strong> Selected overseas duty
stations carry administratively reduced HHG allowances; DTMO publishes the location list, so check
whether your specific installation appears before you assume the mainland number. <strong>Furnished
housing.</strong> On-base housing that arrives furnished or partly furnished — appliances, sometimes
more — can make shipping a full household impractical even when the weight is technically allowed.
Decide what to ship <em>after</em> you know your housing plan, not before.</p>
<h2>The consumables allowance — verify, don't assume</h2>
<p style="max-width:46rem">Some remote OCONUS assignments authorize a separate <strong>consumables
allowance</strong> — up to 1,250 pounds per 12-month tour (1,875 for an 18-month tour) for suitable
consumable goods — but it applies only to duty stations on the Authorized Consumable Goods Allowance
list. Do not assume an Oahu assignment qualifies; whether it does is exactly the kind of detail your
transportation office confirms in a two-minute call. Ask rather than pack on a guess.</p>
<h2>Plan for the gap</h2>
<p style="max-width:46rem">Because HHG travels by sea, there is a real window — often weeks, sometimes
months — between wheels-down and delivery. Your UB is meant to cover the essentials in that window,
but it is deliberately light. Build a survival layer around it: an air-checked-bag kit, an inflatable
bed or two, a few kitchen basics, and the documents packet you'll need for a
rental application and <a href="/guides/school-transition.html">school enrollment</a>. This gap is also why your
<a href="/tla/">interim-housing (TLA) plan</a> and your neighborhood shortlist should be settled
before you fly — you may be living out of UB in temporary lodging while the sea shipment crosses.</p>
<h2>The Oahu mechanics</h2>
<p style="max-width:46rem"><strong>Book in DPS; call when it's not obvious.</strong> Upload orders,
create HHG + UB + any NTS/PPM shipments, and lean on the DoD personal-property call center at
<strong>833-MIL-MOVE (833-645-6683)</strong> or your installation's transportation office for
entitlement questions. For soldiers reporting to Schofield Barracks or Fort Shafter, the outbound
transportation office is at the Soldier Support Center, 673 Ayers Avenue, Bldg 750, Rm 140,
Schofield Barracks — reachable at 808-787-0868 (verified against the installation's MilitaryINSTALLATIONS
listing, August 2026; hours and contacts change, so confirm before you drive out).</p>
<p style="max-width:46rem"><strong>Personally procured moves (PPM).</strong> You can move some or all
of your goods yourself for an incentive payment, booked in DPS like any other shipment — but the
OCONUS math is different from a mainland PPM, so price it carefully with your TO. <strong>Agricultural
inspection.</strong> Hawaii enforces agricultural rules on what enters the state; ask your TO and check
the Hawaii Department of Agriculture for current restrictions rather than learning about them at the
pier.</p>
<div class="warn"><strong>Honest limits.</strong> Weight allowances, entitlements, and reimbursement
rules vary by grade, service, and the exact language on your orders, and they change. This guide is
orientation compiled from Military OneSource, Move.mil/DPS, and DTMO/JTR references and verified
August 5, 2026 — <strong>DPS and your transportation office are the authoritative source</strong> for
your move. Nothing here is a substitute for your official counseling.</div>
<p style="max-width:46rem">Two companion shipping decisions sit next to this one: the
<a href="/vehicle-shipping/">one-POV vehicle shipment and the gap-car math</a>, and the
<a href="/guides/pets-to-hawaii.html">pet quarantine clock</a> — both start on the same day orders
drop. Work the whole <a href="/pcs-checklist/">PCS timeline checklist</a> so none of the three clocks
starts late.</p>
{lead_form("HHG", "pcs-renter",
  heading="Building your shipment plan?",
  blurb="Join the list and the arrival brief pairs the household-goods, vehicle, and pet timelines "
        "against your report window, so the three shipping clocks all start on time.")}
</div>'''
    p = "/guides/household-goods.html"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article",
         "headline": "Household goods to Hawaii: the OCONUS move, in order",
         "description": "How a military OCONUS household-goods move to Oahu works — unaccompanied "
                        "baggage, the sea shipment, non-temporary storage, pro-gear, weight "
                        "allowances, and the DPS booking process.",
         "datePublished": "2026-08-05", "dateModified": "2026-08-05",
         "author": {"@type": "Organization", "name": "PCS Oahu"},
         "publisher": {"@type": "Organization", "name": "PCS Oahu"},
         "mainEntityOfPage": DOMAIN + p},
        faq_ld(qas)]}
    return p, page(p, "Shipping Household Goods to Hawaii on PCS Orders: UB, HHG, Storage | PCS Oahu",
                "How the OCONUS household-goods move to Oahu works — unaccompanied baggage that "
                "lands first, the sea shipment, storage, pro-gear, weight allowances, and DPS "
                "booking. Sourced and dated.",
                body, "/guides/", jsonld=ld)

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
         "mainEntityOfPage": DOMAIN + p},
        faq_ld(qas)]}
    return p, page(p, "Registering a Car in Hawaii on PCS Orders: Forms, Weight Tax, Inspection | PCS Oahu",
                "How military families register an imported vehicle on Oahu: the safety-inspection "
                "sequence and 30-day clock, the nonresident weight-tax exemption (CS-L(MVR)50), and "
                "the out-of-state permit (CS-L(MVR)27). Sourced and dated.",
                body, "/guides/", jsonld=ld)

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
    <h3><a href="/guides/household-goods.html">Household goods to Hawaii</a></h3>
    <p>The OCONUS move in order: unaccompanied baggage first, the sea shipment, storage, pro-gear, and the DPS booking clock.</p></div>
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
    <h3><a href="/tla/">TLA &amp; interim housing</a></h3>
    <p>The wheels-down-to-keys sequence, including the pet-quarantine timeline.</p></div>
  <div class="card"><span class="tag">Departing</span>
    <h3><a href="/sell/">PCSing out: sell or rent?</a></h3>
    <p>HARPTA, the accidental-landlord napkin, and VA seller notes.</p></div>
</div>
{lead_form("GUIDES", "pcs-renter")}
</div>'''
    return page("/guides/", "PCS Oahu Guides: Spouse Employment, Schools, TLA, Selling | PCS Oahu",
                "Process guides for the parts of a Hawaii PCS that numbers alone don't cover — "
                "spouse careers, school transitions, interim housing, and the departure decision.",
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
    }
    for fn in (spouse, school_transition, pets, household_goods, vehicle_registration):
        p, h = fn()
        out[p] = h
    return out
