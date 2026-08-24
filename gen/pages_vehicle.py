from common import *

def vehicle():
    qas = [
      ("Does the military ship my car to Hawaii for free?",
       "Yes — one privately owned vehicle per service member, at government expense, because "
       "Hawaii is an OCONUS station under the Joint Travel Regulations. Booking runs through "
       "PCSmyPOV (International Auto Logistics, the current Global POV Contract operator): you "
       "drop off at a Vehicle Processing Center near your losing station, the government handles "
       "the ocean freight, and you pick up at the Honolulu VPC. Second vehicles ship at your own "
       "expense through commercial carriers."),
      ("How long does it take to ship a car to Hawaii on PCS orders?",
       "The ocean leg from the West Coast is only about a week, but plan door-to-door: 30–45 "
       "days from drop-off to Honolulu pickup availability is a realistic mid-2026 window, and "
       "60+ days happens in summer PCS season and around winter holidays. Track at "
       "pcsmypov.com/Track, and once the ready notice arrives you must book a pickup "
       "appointment within 21 days."),
      ("How much does it cost to ship a second car to Hawaii?",
       "Roughly $1,000–$1,600 from West Coast ports per published carrier pricing in mid-2026, "
       "and commonly $2,000+ all-in from the East Coast once the overland leg is added. Matson "
       "and Pasha Hawaii are the two direct carriers — get current quotes from both before "
       "deciding whether the car is worth more than the invoice."),
      ("How soon must I register my car in Hawaii after it arrives?",
       "Within 10 days of the vehicle's arrival in the state. Non-residents (which includes most "
       "service members keeping a mainland state of legal residence) can keep home plates but "
       "must obtain a Hawaii permit — bring proof of ownership or registration, the shipping "
       "documents, Hawaii no-fault insurance, and the non-resident certificate Form CS-L (MVR) "
       "from your personnel office. Every vehicle also needs Hawaii's annual safety inspection."),
      ("Should I ship my car to Hawaii or buy one on the island?",
       "Run three numbers: the second-vehicle shipping invoice, the gap-car cost while you wait "
       "(airport rentals commonly run $600–$900+ a week in mid-2026), and the island's used-car "
       "premium against your car's mainland value. A paid-off reliable car usually wins by "
       "shipping; a marginal car often loses to selling mainland-side and buying from a "
       "departing PCS family on island."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The complete brief · drop-off to Hawaii plates</p>
<h1>Shipping your vehicle to Hawaii on PCS orders, end to end</h1>
<p class="lede">One POV ships free on your orders. Everything else about the process — the
booking site, the quarter-tank rule, the 30-to-60-day gap, the 10-day registration clock on
the other end — is where PCS budgets and tempers actually go. This is the whole sequence in
one place, dated mid-2026, with every step pointed at its official source.</p>
</div></div>
<div class="wrap">

<h2>First, the decision: ship, sell, or one-car it</h2>
<p style="max-width:46rem">Before any booking, decide what's actually crossing the ocean. The
government pays for <strong>one</strong> vehicle. For a second, you're a retail customer of the
ocean carriers. Three honest numbers settle it:</p>
{rates([
  ("Government-paid vehicles per member", "1 POV"),
  ("Second vehicle, West Coast port (mid-2026)", "≈ $1,000–1,600"),
  ("Second vehicle, East Coast all-in", "commonly $2,000+"),
  ("Gap rental at the airport, per week", "≈ $600–900+", True),
], "Entitlement per the Joint Travel Regulations; second-vehicle ranges per published Matson / "
   "Pasha Hawaii pricing and installation newcomer guidance, mid-2026 — get live quotes from "
   "both carriers. Rental range from public mid-2026 pricing; PCS-season availability varies.")}
<p style="max-width:46rem">The pattern that repeats every summer: families ship the reliable
paid-off car free, sell the second car mainland-side, and either go one-car (genuinely workable
near the close-in pockets and the rail line — see your <a href="/bases/">base guide</a>) or buy
the second car on island from a PCSing-out family, which is where the best island used-car deals
live. Oahu's used market carries a premium over mainland pricing; price your own car against it
before paying to float it across the Pacific.</p>

<h2>The end-to-end sequence, inbound</h2>
<h3>1 — Orders in hand: book the VPC appointment</h3>
<p style="max-width:46rem">Everything runs through <strong>PCSmyPOV</strong>, the booking,
tracking, and appointment system operated by International Auto Logistics under the current
Global POV Contract. Create the appointment at your nearest Vehicle Processing Center the week
orders drop — turn-in slots compress badly in May–August. Your transportation office (DMO/TMO/
JPPSO by service) is the authority on your specific entitlement, and some situations — shipping
from a location that isn't your losing station, separating members, alternate destinations —
need a signed counselor document first.</p>
<h3>2 — Paperwork staging</h3>
<p style="max-width:46rem">Turn-in requires a complete set of orders (with amendments), photo
ID, and proof of ownership. <strong>If there's a lien on the vehicle</strong>, you need the
lender's permission letter on bank letterhead — VIN, make, model, year, the bank's contact
information, and explicit permission to ship — and depending on destination it may need to be
notarized. Getting this letter is routinely the longest-lead item in the whole process; request
it the same day you book. Full current document list: pcsmypov.com/TurnIn.</p>
<h3>3 — Prep the vehicle</h3>
<p style="max-width:46rem">The turn-in standard: <strong>a quarter tank of fuel or less</strong>,
cleaned inside and out (Hawaii's agricultural inspection regime is why — dirt, seeds, and pests
get vehicles rejected), no unresolved fire- or electrical-related recalls, alarms disabled or
instructions provided, and personal items out. The carve-out: items required to maintain or
operate the vehicle (jack, spare, factory accessories) may ship in it if they fit in the
designed spaces. Photograph the whole car, dated, at drop-off — your condition record is your
claim evidence.</p>
<h3>4 — Turn-in at the origin VPC</h3>
<p style="max-width:46rem">West Coast members typically use the California or Washington-area
VPCs; wherever you are, PCSmyPOV assigns the nearest. Joint inspection at the counter, keys and
documents across, and you'll leave with the inspection record you'll need again at pickup.</p>
<h3>5 — The crossing, honestly timed</h3>
{rates([
  ("Ocean leg, West Coast to Honolulu", "≈ 1–2 weeks"),
  ("Realistic drop-off → pickup-ready window", "30–45 days"),
  ("Peak season / holiday backlogs", "60+ days", True),
], "Compiled from installation newcomer guidance and carrier schedules, mid-2026. Track your "
   "vehicle at pcsmypov.com/Track. Plan your arrival transportation around the long end, not "
   "the ocean leg.")}
<h3>6 — The ready notice and the 21-day clock</h3>
<p style="max-width:46rem">Do not drive to the port because tracking says "arrived" — the VPC
releases nothing until it emails the ready notice. Once it does, <strong>you have 21 days to
book a pickup appointment</strong> online. Pickup requires ID, proof of ownership, the
inspection form from turn-in, and — if anyone other than the sponsor is collecting — a power of
attorney or letter of authorization. The Honolulu VPC's location has changed over the years and
sources still disagree; confirm the current address, hours, and contact on the PCSmyPOV
Honolulu VPC page before heading anywhere with a full day planned.</p>
<h3>7 — The gap-car plan</h3>
<p style="max-width:46rem">The 30–60 day window is the expensive part nobody briefs. Options,
in rough order of cost: base shuttle/rideshare austerity near a close-in pocket; a monthly-rate
local rental (materially cheaper than airport chains — compare total cost over your realistic
window, and read the contract's extension terms since your date is a guess); or buying the
island car first and letting the shipped car be the second arrival. Whatever the plan, make it
before wheels-down — <a href="/tla/">TLA logistics</a> and a car search in the same week is the
classic arrival overload.</p>
<h3>8 — Registration: the 10-day clock</h3>
<p style="max-width:46rem">Hawaii requires registration <strong>within 10 days of the vehicle's
arrival in the state</strong>. As a non-resident service member you may keep your home-state
plates, but you still register for a Hawaii permit. Bring: proof of ownership or current
registration, the shipping documents, <strong>Hawaii no-fault insurance</strong> (mainland
policies don't automatically satisfy this — call your carrier before the ship docks), and the
<strong>Non-Resident Certificate, Form CS-L (MVR)</strong>, issued through your personnel
office against your home of record. Registration runs through the City &amp; County of
Honolulu's motor-vehicle offices and satellite city halls.</p>
<h3>9 — Safety inspection, annually</h3>
<p style="max-width:46rem">Every vehicle on Hawaii highways carries a current annual safety
inspection — gas stations and service shops island-wide perform them. Sequence note: insurance
and registration paperwork feed the inspection, so run the errands in the order listed here
and it's one afternoon, not three.</p>

<h2>Special cases</h2>
<p style="max-width:46rem"><strong>Oversize vehicles:</strong> above 20 measurement tons the
government may assess excess charges under JTR 053001 — compute yours with PCSmyPOV's formula
(L×W×H in inches ÷ 1728 ÷ 40) before assuming a lifted truck ships clean.
<strong>Motorcycles:</strong> generally shippable through the same entitlement in place of the
POV or via the carriers commercially; confirm your service's rules with the transportation
office. <strong>EVs:</strong> both major carriers move them routinely — confirm current
state-of-charge requirements when booking, and note your pocket's charging reality (the
close-in condo pockets are the hard case; see your <a href="/neighborhoods/">pocket page</a>).
<strong>Leased vehicles:</strong> the lessor's permission letter is the gating item and some
lessors refuse ocean shipment entirely — ask before you plan around it.</p>

<h2>PCSing out: the reverse run</h2>
<p style="max-width:46rem">Outbound is the same machine in reverse with two additions: your
Hawaii registration should have validity remaining at turn-in (temporary registrations are
assumed to expire 31 days after issue if undated), and lien-holder letters are mandatory again
for many destinations. If you're weighing selling the car on island instead — a departing-PCS
car sale into Oahu's premium used market is often the better trade than shipping a mid-value
vehicle east. The same three-number math from the top of this page runs in reverse, and the
<a href="/sell/">PCS-out brief</a> covers the house-sized version of the same decision.</p>

<h2>The official sources, all of them</h2>
<p style="max-width:46rem">Bookmark in this order: <strong>PCSmyPOV</strong> (booking,
turn-in and pickup document lists, tracking, VPC locations — pcsmypov.com), your
<strong>transportation office</strong> (DMO/TMO/JPPSO — entitlement authority), the
<strong>Joint Travel Regulations</strong> (the entitlement itself), <strong>Matson</strong> and
<strong>Pasha Hawaii</strong> (second-vehicle quotes — matson.com, pashahawaii.com), the
<strong>City &amp; County of Honolulu motor vehicle division</strong> (registration —
honolulu.gov), and <strong>Military OneSource</strong> (moving entitlement counseling —
militaryonesource.mil). Program details, addresses, and prices on this page were compiled
mid-2026 from these public sources and change without notice — the links above are the
authority, and this page is the map to them.</p>
{lead_form("VEHICLE", "pcs-renter",
  heading="Shipping a vehicle this cycle?",
  blurb="Join the list and the arrival brief paces the VPC booking, the lien letter, the "
        "gap-car decision, and the 10-day registration clock against your report window.")}
</div>'''
    p = "/vehicle-shipping/"
    return page(p, "Shipping Your Car to Hawaii on PCS Orders: The Complete 2026 Guide | PCS Oahu",
                "End to end: the one-POV entitlement, PCSmyPOV booking, quarter-tank prep, the "
                "real 30–60 day timeline, the gap-car math, and Hawaii's 10-day registration "
                "clock — every step sourced.",
                body, "/guides/",
                jsonld={"@context": "https://schema.org",
                        "@graph": [article_ld(p, "Shipping your vehicle to Hawaii on PCS orders",
                                              "The complete end-to-end sequence.")]})

def tla_field_notes():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Field notes · the wheels-down week, specifically</p>
<h1>TLA lodging on Oahu: where families actually bridge the gap</h1>
<p class="lede">The <a href="/tla/" style="color:#c9d6da">TLA guide</a> covers the allowance;
this page covers the beds. Options by installation, what to actually ask when booking, and the
handful of choices experienced PCS families make that first-timers learn the expensive way.</p>
</div></div>
<div class="wrap">
<h2>On-base lodging, base by base</h2>
<p style="max-width:46rem">Book on-base first: it simplifies TLA paperwork, shortens the
in-processing commute, and PCS-season demand means the good units go to whoever booked from the
mainland. Each installation runs lodging under its service's program — book through your
gaining base's official lodging page or the DoD lodging portal, and verify current operators
and pet policies at booking (both change): the JBPHH area is served by Navy and Air Force
lodging programs including the Navy Lodge; Army families at Schofield and patients/staff at
Tripler book through Army lodging; MCBH runs Marine Corps lodging aboard the base at Kaneohe
Bay. Ask every property the same four questions: kitchenette or full kitchen, pet room
availability and fee, TLA-rate documentation practice, and realistic maximum stay in PCS
season.</p>
<h2>The Waikiki option most families don't know they have</h2>
<p style="max-width:46rem">The <strong>Hale Koa Hotel</strong> — the Armed Forces Recreation
Center on Waikiki Beach — is bookable by eligible service members at rates scaled to rank, and
a PCS gap is a legitimate use. The honest trade: it's a genuine beachfront start to the tour
and the commute to every installation from Waikiki is real. Families choosing it usually front-
load house-hunting days and treat the location as the one-time perk it is.</p>
<h2>Off-base, if the waitlists are full</h2>
<p style="max-width:46rem">PCS season fills base lodging, and overflow to commercial hotels on
TLA is normal and authorized within the rules. Choose by three filters, in order:
<strong>kitchen</strong> (TLA meal treatment differs with cooking facilities — and sixty days
of restaurant eating breaks budgets independent of any allowance), <strong>location against
your gate</strong> (an airport-corridor or Ko Olina-area property near a leeward assignment
beats a cheaper Waikiki rate plus an hour of H-1), and <strong>weekly-rate flexibility</strong>
(your keys date is a guess; book what extends). Confirm the property will produce itemized
receipts in the format your finance office wants — ask before the first night, not at claim
time.</p>
<div class="note"><strong>The pet complication, again.</strong> Pet-friendly TLA-suitable rooms
are the scarcest inventory on the island in June and July. If the <a
href="/guides/pets-to-hawaii.html">quarantine timeline</a> has your animal landing with you,
book the room before the flights.</div>
<p style="max-width:46rem">Rules, rates, and eligibility on this page are orientation compiled
from public sources, mid-2026 — your installation's housing office, lodging office, and the
current Joint Travel Regulations are the authorities, and prices change seasonally.</p>
{lead_form("LODGING", "pcs-renter",
  heading="Arrival week coming up?",
  blurb="Join the list and the arrival brief includes the lodging-booking checklist paced "
        "ahead of the PCS-season crunch, timed to your report window.")}
</div>'''
    p = "/tla/field-notes.html"
    return p, page(p, "TLA Lodging on Oahu: On-Base Options, Hale Koa, Off-Base Strategy | PCS Oahu",
                "Where PCS families actually stay between wheels-down and keys: base lodging by "
                "installation, the Hale Koa option, and the three filters for off-base TLA hotels.",
                body, "/tla/",
                jsonld=article_ld(p, "TLA lodging on Oahu: field notes",
                                  "Lodging options and booking strategy for the PCS gap."))

def build():
    out = {"/vehicle-shipping/index.html": vehicle()}
    p, h = tla_field_notes()
    out[p] = h
    return out
