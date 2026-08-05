from common import *

def utilities():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Setting up the house</p>
<h1>Utilities on Oahu: the honest bill preview</h1>
<p class="lede">The single budgeting fact first: Hawaii has the most expensive residential
electricity in the country — routinely two to three times mainland rates. BAH is built to cover
utilities, but only if you plan the house around them.</p>
</div></div>
<div class="wrap">
<h2>Electricity — the big line</h2>
<p style="max-width:46rem"><strong>Hawaiian Electric (HECO)</strong> serves Oahu; start service
online with your lease and ID. What drives the bill is air conditioning: an older un-insulated
house running window units can double a mainland family's usage cost, while a trade-wind-cooled
hillside unit may barely need AC at all. At showings, ask for a recent bill (landlords who track
it will tell you), check ceiling fans and window orientation, and note that many newer Ewa and
Mililani homes carry solar — ask specifically whether panels are owned, leased, or PPA-bound
and what conveys to a tenant. Current rates and start-service: hawaiianelectric.com.</p>
<h2>Water, gas, trash</h2>
<p style="max-width:46rem"><strong>Water/sewer:</strong> Honolulu Board of Water Supply
(boardofwatersupply.com) plus the city sewer charge; many rentals fold these into rent — get it
in writing either way. <strong>Gas:</strong> most Oahu homes are all-electric; where gas exists
it's Hawaii Gas (synthetic natural gas lines in town, propane elsewhere). <strong>Trash:</strong>
city collection for houses (opala.org for schedules and rules); complexes handle their own.</p>
<h2>Internet &amp; mobile</h2>
<p style="max-width:46rem">Two wireline options in most pockets: <strong>Spectrum</strong>
(cable) and <strong>Hawaiian Telcom</strong> (fiber where built out — coverage is address-by-
address, so check both before promising a work-from-home setup). Major mobile carriers all
operate; coverage dips in windward valleys and on some base interiors — ask your sponsor what
works at your actual building.</p>
{rates([
  ("Electricity", "highest residential rates in the U.S. — plan the AC question"),
  ("Water/sewer", "often folded into rent; confirm in writing"),
  ("Gas", "most homes all-electric"),
  ("Internet", "Spectrum / Hawaiian Telcom — check the exact address"),
], "Provider facts compiled from public utility information, mid-2026; rates change — verify "
   "current tariffs with each provider before budgeting.")}
{lead_form("UTILITIES", "pcs-renter")}
</div>'''
    p = "/guides/utilities.html"
    return p, page(p, "Utilities on Oahu for Military Families: HECO, Water, Internet | PCS Oahu",
        "The honest utility preview for a Hawaii PCS: the highest electric rates in the U.S., "
        "the AC question to ask at showings, water/gas/trash, and the two internet providers.",
        body, "/guides/", jsonld=article_ld(p, "Utilities on Oahu", "The bill preview."))

def healthcare():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Care on island</p>
<h1>Healthcare for arriving military families</h1>
<p class="lede">Hawaii sits in the TRICARE West footprint, anchored by Tripler Army Medical
Center — the Pacific's largest military hospital. The system works well here; the friction is
all in enrollment timing and drive times.</p>
</div></div>
<div class="wrap">
<h2>The enrollment sequence</h2>
<p style="max-width:46rem">Update DEERS the week you arrive, then transfer your TRICARE
enrollment to the new region — contract administration has changed in recent years, so use
tricare.mil for the current regional contractor and portal rather than an old bookmark.
Prime families are typically assigned care through Tripler or a base clinic depending on pocket
and service; Select families choose network providers. The practical Oahu note: primary-care
panels and pediatric specialists carry waits, so start any specialty-care transfer (referrals,
records, EFMP-tracked care) before you fly, not after.</p>
<h2>The geography of care</h2>
<p style="max-width:46rem">Tripler sits centrally on Moanalua ridge — convenient from the
close-in pockets, a genuine drive from Ewa or the windward side in traffic. Base clinics
(Schofield, MCBH, JBPHH-area) handle much routine care; civilian network hospitals include
Queen's (town), Pali Momi (Aiea), Wahiawa General, Adventist Health Castle (windward), and
Kapiolani for pediatrics/OB. If a family member has recurring appointments, put the facility
on your commute map before choosing a pocket.</p>
<h2>EFMP, dental, and the fine print</h2>
<p style="max-width:46rem">Hawaii assignments run through <a
href="/guides/sponsorship.html">EFMP/overseas-suitability screening</a> for families — clear it
early, because it can shape both orders and housing. Dental runs on its own TRICARE program with
its own enrollment; do it the same week as DEERS. Everything above is orientation from public
program information, mid-2026 — tricare.mil, your service's patient administration, and Tripler's
site are the authorities.</p>
{lead_form("HEALTHCARE", "pcs-renter")}
</div>'''
    p = "/guides/healthcare.html"
    return p, page(p, "Healthcare on Oahu for Military Families: TRICARE, Tripler, Timing | PCS Oahu",
        "The enrollment sequence, the geography of care from Tripler to the base clinics, and "
        "the EFMP and dental fine print for a Hawaii PCS.",
        body, "/guides/", jsonld=article_ld(p, "Healthcare for arriving families", "TRICARE and Tripler."))

def childcare():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The waitlist that starts before you fly</p>
<h1>Childcare on Oahu: start now, seriously</h1>
<p class="lede">Oahu childcare is the pet-quarantine of family logistics: solvable, but only by
families who start the clock at orders. On-base Child Development Center waitlists on Oahu
commonly run months — sometimes past a year for infant rooms.</p>
</div></div>
<div class="wrap">
<h2>The one website that matters</h2>
<p style="max-width:46rem"><strong>MilitaryChildCare.com</strong> is the DoD-wide request
system for CDCs, school-age care, and family childcare homes — create the account and submit
requests for your gaining installation the week orders drop. Your position is largely
request-date driven; every week of delay is a week of waitlist. Priority tiers (dual-military,
single parents, working spouses) are set by DoD policy — check your category honestly and
document it.</p>
<h2>While the list moves</h2>
<p style="max-width:46rem"><strong>Fee assistance</strong> for approved civilian providers runs
through your service's program (administered via Child Care Aware for most branches) when base
care isn't available — apply in parallel, not after. Civilian preschools and licensed homes
cluster unevenly: the family-heavy pockets (Mililani, Ewa/Kapolei, Kaneohe) carry the most
capacity and the longest civilian lists too. State licensing lookup runs through Hawaii's
Department of Human Services. And the unofficial layer every experienced family uses — base
hourly care for appointments, spouse-group co-ops, and the neighbor network — is a real reason
the <a href="/neighborhoods/">family pockets</a> rank how they do.</p>
<div class="note"><strong>Budget line, honestly.</strong> Full-time infant care on Oahu —
on-base fees are income-scaled; civilian care frequently exceeds mainland metro pricing.
If childcare is load-bearing for a two-income plan, price it before choosing between the
<a href="/quiz/">pocket options</a>, not after.</div>
{lead_form("CHILDCARE", "pcs-renter")}
</div>'''
    p = "/guides/childcare.html"
    return p, page(p, "Childcare on Oahu for Military Families: CDC Waitlists, Fee Assistance | PCS Oahu",
        "Why the childcare clock starts at orders: MilitaryChildCare.com requests, realistic "
        "waitlists, fee assistance in parallel, and the pockets with actual capacity.",
        body, "/guides/", jsonld=article_ld(p, "Childcare on Oahu", "Waitlists and fee assistance."))

def sponsorship():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Clearing up a common confusion</p>
<h1>Accompanied orders, EFMP screening, and family travel to Hawaii</h1>
<p class="lede">Families researching "command sponsorship" for Hawaii are usually asking the
right question with the wrong term — that framework governs foreign OCONUS tours. Hawaii is
OCONUS but a U.S. state, and what actually applies here is a different, shorter checklist.</p>
</div></div>
<div class="wrap">
<h2>What Hawaii actually requires</h2>
<p style="max-width:46rem"><strong>Accompanied orders:</strong> your orders must authorize
dependent travel for the government to move the family and pay with-dependent allowances —
confirm the authorization line before booking anything. <strong>EFMP / suitability
screening:</strong> most services require Exceptional Family Member Program screening (or an
overseas/remote-suitability review) for family members before a Hawaii assignment, because
specialty medical and educational capacity on island is finite. This is the step that bites
late starters — screening can shape orders themselves, so it happens at the front of the
timeline, through your medical treatment facility and personnel office. <strong>No visas, no
SOFA, no passport requirement</strong> for the family move itself — it's domestic travel with
OCONUS entitlements.</p>
<h2>What that unlocks</h2>
<p style="max-width:46rem">Accompanied status is what drives the with-dependent BAH rate (see
the <a href="/bah-report/">current anchors</a>), family <a href="/tla/">TLA</a>, full household
goods weight, and dependent enrollment in <a href="/guides/healthcare.html">TRICARE</a> and <a
href="/schools/">schools</a> on arrival. If a family member's screening flags a need Tripler's
system can't support, outcomes range from assignment adjustment to care plans — engage the
EFMP office early and in writing rather than hoping it resolves at the gate.</p>
<p style="max-width:46rem">Service policies differ in the details and change; your personnel
office, your service's EFMP program, and your orders themselves are the authorities — this
page is the map, compiled from public program information, mid-2026.</p>
{lead_form("SPONSORSHIP", "pcs-renter")}
</div>'''
    p = "/guides/sponsorship.html"
    return p, page(p, "Command Sponsorship for Hawaii? Accompanied Orders & EFMP, Explained | PCS Oahu",
        "Hawaii doesn't run foreign-OCONUS command sponsorship — what applies is accompanied "
        "orders and EFMP screening. The actual checklist, and what it unlocks.",
        body, "/guides/", jsonld=article_ld(p, "Accompanied orders and EFMP for Hawaii",
                                            "The actual Hawaii family-travel checklist."))

def data_hub():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Original research · dated, sourced, citable</p>
<h1>The PCS Oahu data desk</h1>
<p class="lede">Every number on this site traces back here: named, dated data products refreshed
on a published cadence. Free to cite with attribution; free to <a href="/embed/"
style="color:#c9d6da">embed</a>.</p>
</div></div>
<div class="wrap">
<div class="grid c2">
  <div class="card"><span class="tag">Flagship · refreshed each BAH cycle</span>
    <h3><a href="/bah-report/">The BAH Reality Report</a></h3>
    <p>Honolulu County BAH anchors vs dated rent bands across 11 pockets — where the allowance
    clears the market and where the gap opens. Current edition refreshed {LAST_REFRESHED}.</p></div>
  <div class="card"><span class="tag">Archive</span>
    <h3><a href="/bah-report/2026-edition/">August 2026 edition (archived)</a></h3>
    <p>Prior editions stay online permanently so citations never break.</p></div>
</div>
<h2>The cadence</h2>
{rates([
  ("BAH Reality Report", "each December BAH cycle + mid-year band moves"),
  ("Pocket rent bands (sitewide)", "monthly, March–August; quarterly off-season"),
  ("Market medians (buy-side pages)", "with each Honolulu Board of REALTORS® cycle we compile"),
], "The refresh date on every rates block sitewide is enforced at build time — if a page shows "
   "a date, the number was reviewed on that date.")}
<h2>In development</h2>
<p style="max-width:46rem">Two additions are planned as the dataset deepens: a <strong>Military
Rental Index</strong> (pocket-level asking-rent movement, PCS-season vs off-season) and a
<strong>BAH Purchasing Power series</strong> (what the with-dependents anchor buys or rents,
tracked edition over edition). Join the list below and you'll get each new product's first
edition before it publishes. Methodology questions and custom cuts for writers: see the <a
href="/bah-report/#cite">citation block</a>.</p>
{lead_form("DATA", "pcs-renter",
  heading="First access to new data products",
  blurb="Report editions and new index launches, in your inbox before they publish. Nothing else.")}
</div>'''
    return page("/data/", "The PCS Oahu Data Desk: Reports, Cadence, Methodology | PCS Oahu",
        "The named, dated data products behind every number on the site — the BAH Reality "
        "Report, the refresh cadence, archived editions, and what's in development.",
        body, "/bah-report/")

def my_pcs():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Your relocation headquarters · saved on this device only</p>
<h1>My PCS</h1>
<p class="lede">Everything you've built on this site in one place: your quiz match, saved
pockets, checklist progress, and calculator results. Stored in your browser — no account, no
login, nothing uploaded. One button turns it into an emailable plan.</p>
</div></div>
<div class="wrap">
<div id="dash"></div>
<h2>Turn it into a plan</h2>
<p style="max-width:46rem"><button class="btn" type="button" id="copyplan">Copy my plan</button>
<a class="btn ghost" style="color:#1f5a54;border-color:#9db4ae" id="mailplan" href="#">Email it
to myself</a></p>
<p style="max-width:46rem" class="fine" id="planNote"></p>
{lead_form("MYPCS", "pcs-renter",
  heading="Want the plan kept current?",
  blurb="Join the list and we'll pace refreshed numbers for your saved pockets against your "
        "report window — the device keeps your plan, the list keeps it accurate.")}
</div>
<script>
(function(){{
 function g(k){{try{{return JSON.parse(localStorage.getItem(k))}}catch(e){{return null}}}}
 function gs(k){{try{{return localStorage.getItem(k)}}catch(e){{return null}}}}
 var quiz=g('pcsoahu-quiz-result'), saved=g('pcsoahu-saved-pockets')||[],
     ck=g('pcsoahu-checklist-v1')||{{}}, calcs=[];
 ['bahfit','payment','rentsell','rentbuy','proceeds','closing','vaff','budget'].forEach(function(id){{
   var v=gs('pcsoahu-calc-'+id); if(v)calcs.push([id,v]);}});
 var done=Object.keys(ck).filter(function(k){{return ck[k]}}).length;
 var h='';
 h+='<h2>Pocket match</h2>'+(quiz?('<p>Your top matches: <strong>'+quiz.top.join(', ')+
   '</strong> (for '+quiz.base+'). <a href="/quiz/">Retake</a>.</p>')
   :'<p>No quiz result yet — <a href="/quiz/">take the pocket-match quiz</a> (90 seconds).</p>');
 h+='<h2>Saved pockets</h2>'+(saved.length?('<p>'+saved.map(function(s){{return '<a href="/neighborhoods/'+
   s+'.html">'+s.charAt(0).toUpperCase()+s.slice(1)+'</a>'}}).join(' · ')+'</p>')
   :'<p>None yet — every <a href="/neighborhoods/">pocket page</a> has a save button.</p>');
 h+='<h2>Checklist</h2><p>'+(done?done+' tasks complete — <a href="/pcs-checklist/">continue</a>.'
   :'Not started — <a href="/pcs-checklist/">open the six-phase checklist</a>.')+'</p>';
 h+='<h2>Calculator results</h2>'+(calcs.length?('<p>'+calcs.map(function(c){{return '<strong>'+
   c[0]+':</strong> '+c[1]}}).join('<br>')+'</p><p><a href="/tools/">Recalculate</a></p>')
   :'<p>None saved yet — results save automatically from the <a href="/tools/">tools page</a>.</p>');
 document.getElementById('dash').innerHTML=h;
 function plan(){{
   var L=['MY PCS OAHU PLAN — pcsoahu.com/my-pcs/',''];
   if(quiz)L.push('Pocket match ('+quiz.base+'): '+quiz.top.join(', '));
   if(saved.length)L.push('Saved pockets: '+saved.join(', '));
   L.push('Checklist: '+done+' tasks complete');
   calcs.forEach(function(c){{L.push(c[0]+': '+c[1])}});
   L.push('','Current data: pcsoahu.com/bah-report/ (refreshed {LAST_REFRESHED})');
   return L.join('\\n');
 }}
 document.getElementById('copyplan').addEventListener('click',function(){{
   navigator.clipboard.writeText(plan()).then(function(){{
     document.getElementById('planNote').textContent='Copied — paste it anywhere.';}});}});
 document.getElementById('mailplan').addEventListener('click',function(e){{
   e.preventDefault();
   location.href='mailto:?subject='+encodeURIComponent('My PCS Oahu plan')+
     '&body='+encodeURIComponent(plan());}});
}})();
</script>'''
    return page("/my-pcs/", "My PCS: Your Saved Oahu Relocation Plan | PCS Oahu",
        "Your quiz match, saved pockets, checklist progress, and calculator results in one "
        "place — stored on your device, no account, exportable as an emailable plan.",
        body, "/pcs-checklist/")

def ask():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Ask the field guide · answers cite their pages</p>
<h1>Ask PCS Oahu</h1>
<p class="lede">A concierge trained on this site's content: BAH math, pockets, the VA gates,
HARPTA, the pet clock. It answers from the guides and links you to them — and it will tell you
when a question needs a human professional instead.</p>
</div></div>
<div class="wrap">
<div class="tool" id="chatbox">
 <div id="log" style="min-height:8rem;font-size:.98rem"></div>
 <label for="q" style="margin-top:1rem">Your question</label>
 <input id="q" type="text" style="max-width:100%" placeholder="e.g., Does my E-5 BAH cover a 3BR in Mililani?">
 <p><button class="btn" type="button" id="send">Ask</button></p>
 <p class="fine">Educational answers from published site content — not legal, tax, lending, or
 valuation advice, and no school or safety rankings. Conversations aren't saved to your device
 or shown to anyone else.</p>
</div>
{lead_form("ASK", "pcs-renter")}
</div>
<script>
(function(){{
 var log=document.getElementById('log'),q=document.getElementById('q'),
     btn=document.getElementById('send'),hist=[];
 function add(who,text,cls){{
   var d=document.createElement('div');
   d.style.cssText='padding:.5rem 0;border-top:1px dotted #d8dcd9'+(cls?';color:#5b6b73':'');
   d.innerHTML='<strong>'+who+':</strong> '+text; log.appendChild(d);}}
 function send(){{
   var text=q.value.trim(); if(!text)return;
   add('You',text.replace(/</g,'&lt;')); q.value=''; btn.disabled=true;
   hist.push({{role:'user',content:text}});
   fetch('/.netlify/functions/concierge',{{method:'POST',
     headers:{{'Content-Type':'application/json'}},
     body:JSON.stringify({{messages:hist.slice(-12)}})}})
   .then(function(r){{return r.json()}})
   .then(function(d){{
     var a=d.reply||'Sorry — the concierge is offline right now. Everything it knows lives in '+
       'the <a href="/guides/">guides</a> and <a href="/bah-report/">the report</a>.';
     hist.push({{role:'assistant',content:a}});
     add('PCS Oahu',a); btn.disabled=false;}})
   .catch(function(){{
     add('PCS Oahu','Connection issue — try again, or go straight to the '+
       '<a href="/guides/">guides</a>.',1); btn.disabled=false;}});
 }}
 btn.addEventListener('click',send);
 q.addEventListener('keydown',function(e){{if(e.key==='Enter')send()}});
}})();
</script>'''
    return page("/ask/", "Ask PCS Oahu: The Relocation Concierge | PCS Oahu",
        "Ask questions about BAH, pockets, VA buying, HARPTA, or the PCS timeline — answers "
        "come from the site's published guides, with links, and honest limits.",
        body, "/guides/")

def build():
    out = {"/data/index.html": data_hub(), "/my-pcs/index.html": my_pcs(),
           "/ask/index.html": ask()}
    for fn in (utilities, healthcare, childcare, sponsorship):
        p, h = fn()
        out[p] = h
    return out
