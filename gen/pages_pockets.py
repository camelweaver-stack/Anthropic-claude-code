from common import *
import pages_family as _fam

# Clean pocket->town matches for the NCES school join. The three urban pockets that resolve to
# city "Honolulu" (Salt Lake, Downtown, Kalihi) are ambiguous, so they link the DOE finder instead.
POCKET_CITY = {
    "aiea": ["Aiea"], "pearlcity": ["Pearl City"], "waipahu": ["Waipahu"],
    "mililani": ["Mililani"], "ewa": ["Ewa Beach", "Kapolei"], "wahiawa": ["Wahiawa"],
    "kaneohe": ["Kaneohe"], "kailua": ["Kailua"],
}
_CC = {c["type"]: c for c in _fam.CCRATES["care_types"]}
_CC_INFANT = _CC["Center-based infant/toddler care"]
_CC_CENTER = _CC["Licensed center-based or group child care home"]

def _family_block(key, name):
    # Schools serving this pocket (city-matched; ambiguous urban pockets link the finder instead)
    if key in POCKET_CITY:
        towns = POCKET_CITY[key]
        sc = [s for s in _fam.SCHOOLS["schools"] if s["city"] in towns]
        sc.sort(key=lambda s: -s["enrollment"])
        rows = "".join(f'<tr><td>{s["name"]}{" · charter" if s.get("charter") else ""}</td>'
                       f'<td class="num">{s["grades"]}</td><td class="num">{s["enrollment"]}</td></tr>'
                       for s in sc)
        schools = (f'<table class="data"><thead><tr><th>Public elementary school</th>'
                   f'<th class="num">Grades</th><th class="num">Enrollment</th></tr></thead>'
                   f'<tbody>{rows}</tbody></table>'
                   f'<p class="fine">Public schools in {name} from {_fam.SCHOOLS_SRC} We don\'t rank '
                   f'schools and never publish attendance boundaries — your zoned school depends on '
                   f'your address; confirm at the <a href="{_fam.DOE_LOCATOR}" rel="nofollow">DOE '
                   f'school finder</a> before you sign.</p>') if sc else ""
    else:
        schools = (f'<p style="max-width:46rem">{name} sits in urban Honolulu, where several district '
                   f'boundaries overlap — look your exact address up in the '
                   f'<a href="{_fam.DOE_LOCATOR}" rel="nofollow">DOE school finder</a> rather than trust '
                   f'a pocket-level list. The <a href="/family/">family layer</a> maps schools by gate.</p>')
    # Sourced free-flow commute to the nearest gate (single source: the Commute Reality Grid)
    grid = _fam.COMMUTE["grid"].get(name, {})
    commute = ""
    if grid:
        g, cell = min(grid.items(), key=lambda kv: kv[1]["freeflow_min"])
        commute = (f'<p style="max-width:46rem">Free-flow to the nearest installation ({g}): '
                   f'<strong>{cell["freeflow_min"]} min</strong>. This pocket\'s full row across every '
                   f'gate is in <a href="/tools/commute-grid/">the Commute Reality Grid</a>.</p>'
                   f'<p class="fine">Source: {_fam.COMMUTE_SRC}</p>')
    return f'''
<h2>For families</h2>
<h3>Schools</h3>
{schools}
<h3>Childcare</h3>
<p style="max-width:46rem">Licensed full-time care on Oahu runs roughly {_fam._fmt(_CC_CENTER["median"])}/mo
(median, licensed center or group home) to {_fam._fmt(_CC_INFANT["median"])}/mo (median, center-based
infant/toddler) — the crossover math is in <a href="/family/childcare/">The Second Paycheck Report</a>.
Find licensed providers through the <a href="{_fam.DHS_CHILDCARE}" rel="nofollow">Hawaii DHS finder</a>
or <a href="{_fam.PATCH_URL}" rel="nofollow">PATCH</a> ({_fam.PATCH_LINE}); confirm each provider's
current license before visiting.</p>
<p class="fine">Cost source: {_fam.CCRATES["product_source"]}. Pulled {_fam.CCRATES["pulled"]}.</p>
<h3>Commute, sourced</h3>
{commute}'''

# per-pocket editorial data: (tag, hero_img_key, bases[(label,drive)], story, trade, buynote)
PD = {
 "aiea": ("AIEA","jbphh",
   [("JBPHH","10–20 min"),("Camp Smith","5–15 min"),("Tripler","10–15 min"),("Fort Shafter","10–20 min")],
   "Aiea is the closest thing the south shore has to a default military neighborhood: terraced "
   "hillsides above Pearl Harbor, a mix of 1960s–80s houses and newer townhomes, and a location "
   "that puts four installations inside a twenty-minute drive. Pearlridge Center anchors the "
   "errand run, and the heights catch trade winds the flatlands don't.",
   "Stock skews older — factor renovation lottery into your tours — and hillside streets can be "
   "steep and parking-tight. Well-priced units move fast because every service shops here.",
   "Fee-simple single-family homes here trade below windward and town equivalents; a realistic "
   "first rung for VA buyers who want a house, not a unit."),
 "pearlcity": ("PEARLCITY","jbphh",
   [("JBPHH","15–25 min"),("Camp Smith","10–20 min"),("Schofield","25–35 min")],
   "Pearl City is the workhorse: townhome complexes and single-family streets stacked above the "
   "H-1 with more square footage per dollar than anything closer to the harbor. It's a "
   "long-established local community — multi-generation households, strong little-league "
   "energy, and grocery-store parking lots that know a payday weekend.",
   "The H-1 merge is the tax you pay for the space; test the drive at your real report time "
   "before signing anything uphill of the freeway.",
   "Townhome inventory here is a frequent first VA purchase — check HOA health and the "
   "project's VA approval status before touring."),
 "saltlake": ("SALTLAKE","tripler",
   [("Tripler","5–15 min"),("Fort Shafter","5–15 min"),("JBPHH","10–20 min"),("Camp Smith","10–15 min")],
   "Salt Lake and Moanalua are condo country: mid-rise towers and garden complexes around the "
   "crater with the shortest average commute footprint on the island. Hospital staff, "
   "headquarters soldiers, and single service members make up half the elevator on any given "
   "morning. Errands are walkable-adjacent; the airport is ten minutes when family visits.",
   "You're trading yard for minutes — and airport flight paths are real; open the windows at a "
   "showing and listen.",
   "The densest VA-condo decision zone on Oahu: the approved-project list and HOA fees decide "
   "more here than asking price does."),
 "waipahu": ("WAIPAHU","ewa",
   [("JBPHH","15–30 min"),("Schofield","20–30 min"),("Kapolei jobs","10–20 min")],
   "Waipahu delivers the most rent per dollar this close to the harbor: plantation-town roots, "
   "dense local neighborhoods, legendary food (start with the okazuya counters), and quick "
   "access to both the H-1 and the rail line. Families stretching a junior-enlisted allowance "
   "into three bedrooms end up here more than anywhere else on the leeward side.",
   "It's dense and working — smaller lots, busier streets, and quality varies block by block; "
   "tour in person and at night.",
   None),
 "mililani": ("MILILANI","mililani",
   [("Schofield","10–20 min"),("JBPHH","25–40 min"),("Wheeler","10–15 min")],
   "Mililani is the island's planned-community answer to the mainland suburb question: HOA-kept "
   "streets, seven rec centers with pools, top-of-plateau weather that runs cooler than the "
   "shore, and schools with waiting lists of geographic-exception requests. For Schofield "
   "families it's the default; for south-shore commuters it's the deliberate space-for-drive "
   "trade.",
   "The HOA that keeps it tidy also has opinions about your truck, your fence, and your "
   "holiday lights — read the rules before you romanticize them.",
   "One of the strongest resale stories on Oahu — the same predictability that draws renters "
   "draws the next buyer when you PCS out."),
 "ewa": ("EWA","ewa",
   [("JBPHH","30–60+ min"),("Schofield","30–50 min"),("Kapolei jobs","5–15 min")],
   "Ewa Beach and Kapolei are where Oahu builds new: master-planned subdivisions, the island's "
   "youngest housing stock, Ka Makana Ali'i mall, and a second-city job base that keeps "
   "growing. Four bedrooms and a two-car garage exist here at prices the rest of the island "
   "stopped offering years ago — which is exactly why half the base seems to live here.",
   "The H-1 eastbound at 0600 is the whole conversation. If your report time is standard "
   "staff hours, drive it once before you commit; if you're on shift work or the rail line "
   "serves your gate, the math changes completely.",
   "The center of gravity for VA purchases on Oahu — new-construction builders here know the "
   "VA process cold, and resale competition is thickest at exactly these price points."),
 "wahiawa": ("WAHIAWA","schofield",
   [("Schofield","5–15 min"),("Wheeler","5–10 min"),("JBPHH","30–45 min")],
   "Wahiawa is the last real plantation town on the plateau: walkable old core, lake views, "
   "cool nights, and the most forgiving rent bands within a coffee's drive of any gate on the "
   "island. Soldiers who want five minutes to formation and a mortgage-sized savings rate "
   "choose it on purpose.",
   "Stock is old and honest about it — inspect hard, and know that town amenities are a "
   "drive, not a stroll. What you save in rent you spend in weekend gas.",
   None),
 "kaneohe": ("KANEOHE","mcbh",
   [("MCBH","10–15 min"),("Camp Smith via H-3","25–35 min"),("Town via Pali/Like","25–40 min")],
   "Kaneohe is the practical windward choice: real neighborhoods under the Ko'olau cliffs, "
   "bay views from ordinary streets, and the closest off-base living to the Marine Corps "
   "base. It rains more and everyone gardens like it; the green is the point.",
   "Windward inventory is thin and moves in days during PCS season — have documents staged "
   "and decide your ceiling before you tour, not during.",
   "Fee-simple houses here hold value on scarcity alone; check flood maps street by street "
   "before falling for a bayside listing."),
 "kailua": ("KAILUA","kailua",
   [("MCBH","10–20 min"),("Town via Pali","25–40 min")],
   "Kailua is the deliberate splurge: one of the most photographed beaches in the country as "
   "your weekend baseline, a walkable town core, and a rental market priced like it knows all "
   "of that. Families who choose it usually rank the beach-town childhood above every other "
   "line on the budget — a legitimate call, made honestly.",
   "Bands start where an E-6 allowance ends; budget the gap on purpose or window-shop "
   "somewhere kinder. Vacation-rental pressure keeps long-term inventory scarce.",
   None),
 "downtown": ("DOWNTOWN","downtown",
   [("USCG Sand Island","10–15 min"),("Fort Shafter","15–25 min"),("Tripler","15–30 min")],
   "Downtown and Kakaako are the city option: high-rise condos, the rail line, third-wave "
   "coffee, and the only Oahu lifestyle where a car is optional. Coast Guard members and "
   "single service members at the medical and headquarters commands make it work best — "
   "against-traffic commutes and walkable everything.",
   "Parking stalls, HOA fees, and pet rules decide more than square footage here; get all "
   "three in writing before applying. Street noise is a feature of the genre.",
   "Town towers are where the VA condo-approval list matters most on the entire island — "
   "check the project before you check the view."),
 "kalihi": ("KALIHI","downtown",
   [("USCG Sand Island","5–15 min"),("Fort Shafter","5–15 min"),("Tripler","10–15 min")],
   "Kalihi holds the lowest close-in rent bands on Oahu: dense, working, unglamorous, and "
   "fifteen minutes from three installations and the airport. The food alone — old-school "
   "manapua shops to some of the island's best plate lunch — argues its case. For a single "
   "service member banking the allowance difference, it's the sharpest arbitrage on the map.",
   "Housing quality varies unit to unit more than neighborhood averages suggest — tour in "
   "person, meet the landlord, and read the lease twice.",
   None),
}

def pocket_page(key):
    tag, img, bases, story, trade, buynote = PD[key]
    name, bands = POCKETS[key]
    band_rows = [tuple(b.split(" ", 1)) for b in bands.split(" · ")]
    commute_rows = "".join(f"<tr><td>{b}</td><td class='num'>{d}</td></tr>" for b, d in bases)
    buy_html = (f'<div class="note"><strong>Buyer note.</strong> {buynote} '
                f'Full math in the <a href="/buy/">VA brief</a>.</div>') if buynote else ""
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Commute-real for: {", ".join(b for b,_ in bases)}</p>
<h1>Living in {name} on military orders</h1>
<p class="lede">{story}</p>
</div></div>
<div class="wrap">
<h2>The bands</h2>
{rates(band_rows, RENT_SRC)}
<h2>The commute picture</h2>
<table class="data"><thead><tr><th>To</th><th>Typical drive</th></tr></thead>
<tbody>{commute_rows}</tbody></table>
<h2>The honest trade</h2>
<p style="max-width:46rem">{trade}</p>
{buy_html}
{_family_block(key, name)}
<p><button class="btn ghost" style="color:#1f5a54;border-color:#9db4ae" id="savep" data-pocket="{key}">Save {name} to My PCS</button></p>
<p style="max-width:46rem">School boundaries here run street by street — check any exact address
against the HIDOE lookup before signing (the <a href="/schools/">schools guide</a> explains how
Hawaii's statewide district and Geographic Exceptions work), and see how {name} scores against
your priorities in the <a href="/quiz/">pocket-match quiz</a>.</p>
<script>
(function(){{var b=document.getElementById('savep'),k=b.getAttribute('data-pocket'),K='pcsoahu-saved-pockets';
function arr(){{try{{return JSON.parse(localStorage.getItem(K))||[]}}catch(e){{return[]}}}}
function paint(){{b.textContent=(arr().indexOf(k)>-1?'Saved to My PCS (tap to remove)':'Save {name} to My PCS')}}
b.addEventListener('click',function(){{var a=arr(),i=a.indexOf(k);
if(i>-1)a.splice(i,1);else a.push(k);
try{{localStorage.setItem(K,JSON.stringify(a))}}catch(e){{}};paint()}});paint()}})();
</script>
{lead_form(tag, "pcs-renter",
  heading="Watching " + name + "?",
  blurb="Join the list and the monthly refresh includes this pocket's bands next to your grade's "
        "allowance, timed to your report window.")}
</div>'''
    path = f"/neighborhoods/{key}.html"
    return path, page(path,
        f"Living in {name} on Military Orders: Rents, Commutes, Honest Trades | PCS Oahu",
        f"{name} for PCS families — dated rent bands, real drive times to nearby installations, "
        f"and the honest trade-offs nobody puts in a listing.",
        body, "/neighborhoods/",
        jsonld=article_ld(path, f"Living in {name} on military orders",
                          f"Rent bands, commutes, and trade-offs for {name}."))

def build():
    return dict(pocket_page(k) for k in PD)
