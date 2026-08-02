from common import *

def quiz():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Five questions · scored against the current rent bands · reasoning shown</p>
<h1>The pocket-match quiz</h1>
<p class="lede">Duty station, bedrooms, budget, and what you're optimizing for — scored against
this edition's rent bands and commute realities. Top three pockets, with the why. Runs entirely
in your browser; nothing is uploaded anywhere.</p>
</div></div>
<div class="wrap">
<div class="tool" id="quizbox">
<label for="q1">1. Where do you report?</label>
<select id="q1"><option value="">Choose your installation</option>
<option value="jbphh">Joint Base Pearl Harbor–Hickam</option>
<option value="schofield">Schofield Barracks / Wheeler</option>
<option value="mcbh">MCBH Kaneohe Bay</option>
<option value="campsmith">Camp Smith</option>
<option value="tripler">Tripler AMC</option>
<option value="shafter">Fort Shafter</option>
<option value="uscg">USCG Base Honolulu</option></select>
<label for="q2">2. Bedrooms you actually need</label>
<select id="q2"><option value="">Choose</option><option value="s">1–2 (just us / roommate math)</option>
<option value="m">3 (family standard)</option><option value="l">4+ (big crew)</option></select>
<label for="q3">3. Monthly housing budget (your BAH is a good start — it covers utilities too)</label>
<select id="q3"><option value="">Choose</option><option value="1">Under $2,500</option>
<option value="2">$2,500–$3,200</option><option value="3">$3,200–$4,000</option>
<option value="4">$4,000+</option></select>
<label for="q4">4. What are you optimizing for?</label>
<select id="q4"><option value="">Choose</option>
<option value="commute">Shortest possible commute</option>
<option value="space">Most space per dollar</option>
<option value="windward">Windward / beach-town living</option>
<option value="new">Newest housing stock</option></select>
<label for="q5">5. This tour, you're most likely to…</label>
<select id="q5"><option value="">Choose</option><option value="rent">Rent</option>
<option value="buy">Seriously consider buying</option></select>
<p><button class="btn" type="button" id="go">Show my pockets</button></p>
<output id="res" style="font-family:inherit;font-weight:400"></output>
</div>
{lead_form("QUIZ", "pcs-renter",
  heading="Want your match kept current?",
  blurb="Rent bands move monthly in PCS season. Join the list and your shortlisted pockets come "
        "with the refreshed numbers, timed to your report window.")}
</div>
<script>
(function(){{
// pocket data: [name, url-slugless label, minRent(s/m/l band floor, null=rare), commute rank per base (1=best), space, windward, newness]
var P={{
 aiea:      ["Aiea","aiea",[1900,3200,3900],{{jbphh:1,campsmith:1,tripler:2,shafter:3,schofield:4,uscg:3,mcbh:5}},2,0,1],
 pearlcity: ["Pearl City","pearlcity",[2400,3000,3700],{{jbphh:2,campsmith:3,tripler:3,shafter:4,schofield:3,uscg:4,mcbh:5}},3,0,1],
 saltlake:  ["Salt Lake / Moanalua","saltlake",[1800,2900,null],{{jbphh:1,campsmith:2,tripler:1,shafter:1,schofield:5,uscg:3,mcbh:5}},1,0,1],
 waipahu:   ["Waipahu","waipahu",[2000,2700,3400],{{jbphh:2,campsmith:4,tripler:4,shafter:4,schofield:3,uscg:5,mcbh:6}},3,0,1],
 mililani:  ["Mililani","mililani",[2500,3200,4000],{{jbphh:3,campsmith:4,tripler:4,shafter:4,schofield:2,uscg:5,mcbh:6}},3,0,2],
 ewa:       ["Ewa Beach / Kapolei","ewa",[2600,3000,3800],{{jbphh:4,campsmith:5,tripler:5,shafter:5,schofield:4,uscg:6,mcbh:7}},3,0,3],
 wahiawa:   ["Wahiawa","wahiawa",[1900,2600,3300],{{jbphh:4,campsmith:5,tripler:5,shafter:5,schofield:1,uscg:6,mcbh:6}},3,0,0],
 kaneohe:   ["Kaneohe","kaneohe",[2600,3400,4300],{{jbphh:5,campsmith:4,tripler:4,shafter:4,schofield:6,uscg:5,mcbh:1}},2,1,1],
 kailua:    ["Kailua","kailua",[3200,4000,5000],{{jbphh:5,campsmith:5,tripler:5,shafter:5,schofield:6,uscg:5,mcbh:1}},1,1,1],
 downtown:  ["Downtown / Kakaako","downtown",[2000,3600,null],{{jbphh:4,campsmith:3,tripler:3,shafter:2,schofield:6,uscg:1,mcbh:5}},0,0,3],
 kalihi:    ["Kalihi","kalihi",[1500,2400,null],{{jbphh:3,campsmith:3,tripler:2,shafter:1,schofield:5,uscg:1,mcbh:5}},1,0,0]
}};
var BASEURL={{jbphh:"pearl-harbor-hickam",schofield:"schofield-wheeler",mcbh:"kaneohe-bay",
 campsmith:"camp-smith",tripler:"tripler",shafter:"fort-shafter",uscg:"coast-guard-honolulu"}};
var BUDGET={{1:2500,2:3200,3:4000,4:99999}};
var BR={{s:0,m:1,l:2}};
document.getElementById('go').addEventListener('click',function(){{
 var b=document.getElementById('q1').value,br=document.getElementById('q2').value,
     bg=document.getElementById('q3').value,pr=document.getElementById('q4').value,
     hz=document.getElementById('q5').value,res=document.getElementById('res');
 if(!b||!br||!bg||!pr||!hz){{res.textContent='Answer all five and try again.';return}}
 var cap=BUDGET[bg],bi=BR[br],scored=[];
 for(var k in P){{
  var p=P[k],rent=p[2][bi],why=[];
  if(rent===null)continue; // pocket rarely offers this size
  var s=0;
  var cr=p[3][b]; s+=(7-cr)*3; if(cr<=2)why.push('one of the closest pockets to your gate');
  if(rent<=cap){{s+=6;why.push('band floor fits your budget')}}
  else if(rent<=cap*1.1){{s+=2;why.push('tight against your budget — negotiate or size down')}}
  else s-=8;
  if(pr==='commute')s+=(7-cr)*3;
  if(pr==='space'){{s+=p[4]*3;if(p[4]>=3)why.push('strong space-per-dollar')}}
  if(pr==='windward'){{s+=p[5]*12;if(p[5])why.push('windward side')}}
  if(pr==='new'){{s+=p[6]*4;if(p[6]>=2)why.push('newest stock on the island')}}
  if(hz==='buy'&&(k==='ewa'||k==='mililani'||k==='waipahu'))
    {{s+=2;why.push('active buy-side inventory near typical VA price points')}}
  scored.push([s,p[0],why]);
 }}
 scored.sort(function(a,z){{return z[0]-a[0]}});
 var top=scored.slice(0,3),html='<h3 style="margin-top:1rem">Your three pockets</h3>';
 top.forEach(function(t,i){{
  html+='<p><strong>'+(i+1)+'. '+t[1]+'</strong> — '+(t[2].length?t[2].join('; '):'balanced fit')+'.</p>';
 }});
 html+='<p>Bands and commutes for these live on your <a href="/bases/'+BASEURL[b]+
   '.html">base guide</a> and the <a href="/neighborhoods/">pocket table</a>.'+
   (hz==='buy'?' Buying this tour? Read the <a href="/buy/">VA brief</a> before touring anything.':'')+
   '</p><p style="font-size:.85rem;color:#5b6b73">Scored against the current edition\\'s rounded '+
   'bands — a compass, not a lease decision. Verify asking rents directly.</p>';
 res.innerHTML=html;
}});
}})();
</script>'''
    return page("/quiz/", "Oahu Pocket-Match Quiz: Which Neighborhood Fits Your Orders? | PCS Oahu",
                "Five questions — duty station, bedrooms, budget, priorities — scored against "
                "current Oahu rent bands and commute realities. Top three pockets, reasoning shown.",
                body, "/neighborhoods/")

def on_base():
    qas = [
      ("How do I get on the on-base housing waitlist on Oahu?",
       "Contact the housing office at your gaining installation the day orders drop — waitlists "
       "commonly run weeks to months, position rules vary by service, and getting on the list "
       "costs nothing and forecloses nothing. You can hold a place while searching off base."),
      ("Does on-base housing take my whole BAH?",
       "Under the privatized (MHPI) model, rent is typically set at your with-dependents BAH and "
       "paid by allotment, generally with utilities handled per the program's rules. What varies "
       "— and what to ask in writing — is utility allowance policy, fees, and what happens to "
       "any gap. The program office at your installation has the current terms."),
      ("Who runs on-base family housing on Oahu?",
       "Family housing is privatized and operated by program partners by service — Island Palm "
       "Communities for Army installations, Ohana Military Communities for Navy and Marine Corps "
       "areas, and Hickam Communities on the Air Force side of JBPHH. Management arrangements "
       "change; verify the current operator and terms through your installation housing office."),
    ]
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The third option on every ledger</p>
<h1>On-base housing on Oahu: how the privatized system actually works</h1>
<p class="lede">Every live-on-or-off page on this site ends at the same fork, so here's the
on-base tine in full: who runs it, how the waitlist and money work, and the questions worth
asking in writing before you sign a lease with a housing partner — because that's what it is,
a lease.</p>
</div></div>
<div class="wrap">
<h2>The shape of the system</h2>
<p style="max-width:46rem">Oahu family housing runs on the Military Housing Privatization
Initiative: private program partners own and operate the neighborhoods under long-term
agreements. By service — <strong>Island Palm Communities</strong> across the Army footprint
(Schofield, Wheeler, Fort Shafter area, AMR), <strong>Ohana Military Communities</strong> for
Navy and Marine Corps areas, and <strong>Hickam Communities</strong> on the Air Force side of
JBPHH. Operators and terms change; the housing office at your installation is the source of
record, and this page is orientation.</p>
<h2>The money, honestly</h2>
{rates([
  ("Typical rent under MHPI", "your with-dependents BAH, by allotment"),
  ("Your negotiating leverage on rent", "none — it's set to the allowance"),
  ("What varies (ask in writing)", "utility policy, fees, pet terms, move-out"),
  ("Off-base comparison for your grade", "the pocket table on this site"),
], "Program terms per your installation's housing office and the current resident lease — "
   "verify everything there. This page is orientation, not the lease.")}
<p style="max-width:46rem">The honest trade: on base you spend exactly your allowance and buy
proximity, community, and zero landlord-shopping; off base, if your grade's number beats your
pocket's band, the difference is yours — and BAH is also meant to cover utilities either way.
Run your grade against the <a href="/neighborhoods/">pocket table</a> before deciding the
allowance question is already answered.</p>
<h2>Waitlist tactics that cost nothing</h2>
<p style="max-width:46rem">Get on the list the day orders drop — position rules vary by service
but the option is free and holds while you search off base. Ask for the current realistic wait
for your grade and bedroom count (not the brochure answer), and whether accepting or declining
an offer affects your position. Arriving families commonly bridge with <a href="/tla/">TLA</a>
while the list moves.</p>
<h2>Know your paper</h2>
<p style="max-width:46rem">The MHPI <strong>Tenant Bill of Rights</strong> applies to privatized
military housing: written lease terms, a formal dispute-resolution process, maintenance-history
disclosure, and habitability standards among them. Read the current version before signing,
document unit condition at move-in as thoroughly as you would with any civilian landlord, and
put every maintenance request in the system of record, not a text thread. None of this is
adversarial — it's the same paper discipline this site preaches for off-base leases.</p>
{lead_form("ONBASE", "pcs-renter",
  heading="Still deciding on vs. off?",
  blurb="Join the list and the arrival brief pairs the current on-base wait picture with the "
        "off-base bands for your gaining installation.")}
</div>'''
    return page("/on-base/", "On-Base Housing on Oahu: Waitlists, BAH, and the Privatized System | PCS Oahu",
                "How Oahu's privatized military housing actually works — Island Palm, Ohana, and "
                "Hickam Communities, waitlist tactics, the BAH allotment math, and tenant rights.",
                body, "/bases/", jsonld=faq_ld(qas))

def notfound():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Wrong gate</p>
<h1>That page isn't here.</h1>
<p class="lede">The address may have changed with a refresh, or the link was mistyped. Everything
on the site routes from these four:</p>
<p><a class="btn" href="/bases/">Base guides</a> <a class="btn ghost" href="/bah-report/">BAH Report</a>
<a class="btn ghost" href="/pcs-checklist/">PCS checklist</a> <a class="btn ghost" href="/tools/">Tools</a></p>
</div></div>
<div class="wrap">{lead_form("NOTFOUND", "pcs-renter")}</div>'''
    return page("/404.html", "Page Not Found | PCS Oahu",
                "That page isn't here — route back through the base guides, the BAH Reality "
                "Report, the PCS checklist, or the tools.", body, "")

def build():
    return {"/quiz/index.html": quiz(), "/on-base/index.html": on_base(),
            "/404.html": notfound()}
