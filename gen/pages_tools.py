from common import *

CHECKLIST = [
 ("Orders in hand (as early as possible)", [
   "Contact the gaining installation housing office — get on the on-base waitlist same week",
   "Start the Hawaii pet quarantine checklist (rabies bloodwork lead time runs months)",
   "Request school records and connect with the gaining base's school liaison officer",
   "Pull your exact 2026 BAH from the DTMO calculator for your grade and dependents",
   "Read your gaining base guide and shortlist 3 commute-real pockets",
   "Schedule the transportation office (household goods) counseling session",
 ]),
 ("90–60 days out", [
   "Book TLA-eligible lodging near your gaining base (on-base lodging first)",
   "Stage rental documents: orders, LES, references, pet records, photo ID",
   "Decide the vehicle question: ship a POV, buy on island, or one-car it",
   "If buying: get your Certificate of Eligibility and a real preapproval on gaining-station BAH",
   "Spouse: check licensure compact / expedited-license path for your profession",
   "Run candidate addresses through the HIDOE school finder before committing to a pocket",
 ]),
 ("60–30 days out", [
   "Confirm household goods pack-out dates and the unaccompanied baggage split",
   "Book flights; confirm pet direct-airport-release paperwork is complete",
   "Set a housing budget line: your BAH is for rent AND utilities",
   "Start mainland-side school health requirements (immunizations, TB clearance)",
   "If selling a mainland home: read the entitlement-restoration notes before closing",
 ]),
 ("Arrival week", [
   "In-process; attend the housing office briefing before signing anything",
   "Get on the on-base waitlist even if you plan to rent out in town",
   "Tour shortlisted pockets at your actual commute hours (0630 test)",
   "Open a local credit-union account if your bank has no island presence",
   "Enroll kids: orders, proof of address, health records, records packet",
 ]),
 ("First 30 days", [
   "Apply fast when a unit fits the band — PCS-season inventory moves in days",
   "Document TLA compliance: keep lodging receipts and housing-search evidence",
   "Hawaii driver's license / vehicle registration decisions (SCRA options apply)",
   "Walk the commute, the grocery run, and the beach day before the lease renews itself into habit",
 ]),
 ("Settling (60–90 days)", [
   "Calendar your lease-end against your projected rotation date now",
   "If buying this tour: read the condo-approval and leasehold briefs before touring",
   "Spouse: family-support-center employment workshops run heaviest in PCS season",
   "Write down what you wish you'd known — the next family in your unit needs it",
 ]),
]

def checklist_page():
    phases = []
    tid = 0
    for i, (title, items) in enumerate(CHECKLIST):
        lis = []
        for item in items:
            tid += 1
            lis.append(f'<li><input type="checkbox" id="t{tid}" data-ck>'
                       f'<label for="t{tid}">{item}</label></li>')
        phases.append(
          f'<section class="phase{" open" if i == 0 else ""}" id="ph{i}">'
          f'<button type="button" aria-expanded="{str(i==0).lower()}">{title}'
          f'<span class="count" data-count></span></button><ul>{"".join(lis)}</ul></section>')
    total = tid
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Interactive · {total} tasks · saves in your browser</p>
<h1>The Hawaii PCS timeline checklist</h1>
<p class="lede">The whole move as one working list — six phases from orders-in-hand to settled,
each task linked to the guide that explains it. Progress saves on this device. No account,
nothing uploaded.</p>
</div></div>
<div class="wrap">
<div class="progressbar" aria-hidden="true"><div id="bar"></div></div>
<p id="progressText" style="font-family:'IBM Plex Mono',monospace;font-size:.85rem"></p>
{''.join(phases)}
<p><button class="btn ghost" style="color:#1f5a54;border-color:#9db4ae" type="button" id="reset">
Reset checklist</button></p>
{lead_form("CHECKLIST", "pcs-renter",
  heading="Want the checklist as a timed brief?",
  blurb="Join the list and we'll pace these phases against your report window — the right "
        "reminders at the right distance from wheels-down.")}
</div>
<script>
(function(){{
 var KEY='pcsoahu-checklist-v1';
 var boxes=[].slice.call(document.querySelectorAll('[data-ck]'));
 var saved={{}};
 try{{saved=JSON.parse(localStorage.getItem(KEY)||'{{}}')}}catch(e){{}}
 boxes.forEach(function(b){{
   if(saved[b.id]){{b.checked=true;b.closest('li').classList.add('done')}}
   b.addEventListener('change',function(){{
     b.closest('li').classList.toggle('done',b.checked);
     saved[b.id]=b.checked;try{{localStorage.setItem(KEY,JSON.stringify(saved))}}catch(e){{}}
     paint();}});
 }});
 [].slice.call(document.querySelectorAll('.phase>button')).forEach(function(btn){{
   btn.addEventListener('click',function(){{
     var ph=btn.parentNode,open=ph.classList.toggle('open');
     btn.setAttribute('aria-expanded',open);}});
 }});
 function paint(){{
   var done=boxes.filter(function(b){{return b.checked}}).length;
   var pct=Math.round(100*done/boxes.length);
   document.getElementById('bar').style.width=pct+'%';
   document.getElementById('progressText').textContent=done+' / '+boxes.length+' tasks · '+pct+'%';
   [].slice.call(document.querySelectorAll('.phase')).forEach(function(ph){{
     var bs=[].slice.call(ph.querySelectorAll('[data-ck]'));
     var d=bs.filter(function(b){{return b.checked}}).length;
     ph.querySelector('[data-count]').textContent=d+'/'+bs.length;}});
 }}
 document.getElementById('reset').addEventListener('click',function(){{
   if(!confirm('Clear all saved progress on this device?'))return;
   boxes.forEach(function(b){{b.checked=false;b.closest('li').classList.remove('done')}});
   saved={{}};try{{localStorage.removeItem(KEY)}}catch(e){{}};paint();}});
 paint();
}})();
</script>'''
    return page("/pcs-checklist/", "The Hawaii PCS Timeline Checklist (Interactive) | PCS Oahu",
                "The whole Hawaii PCS as one interactive checklist: six phases, every task linked "
                "to its guide, progress saved on your device. Free, no account.",
                body, "/pcs-checklist/")

def tools_page():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Three calculators · nothing leaves your phone</p>
<h1>The PCS math, automated</h1>
<p class="lede">Orientation tools, not advice: rough the numbers before any conversation with a
landlord, lender, or property manager. All math runs in your browser.</p>
</div></div>
<div class="wrap">
<div class="tool"><h2 style="margin-top:0">BAH-vs-rent fit</h2>
<p>How much allowance is left after rent — remembering BAH is also meant to cover utilities.</p>
<label for="bah1">Your monthly BAH (from the DTMO calculator)</label>
<input id="bah1" type="number" inputmode="decimal" placeholder="e.g., 3663">
<label for="rent1">Asking rent for the unit</label>
<input id="rent1" type="number" inputmode="decimal" placeholder="e.g., 3200">
<output id="out1">Enter both numbers.</output></div>

<div class="tool"><h2 style="margin-top:0">Payment reality check</h2>
<p>Rough principal-and-interest on a loan amount — then add taxes, insurance, and (critically on
Oahu) the HOA fee yourself. Educational only; not a loan quote.</p>
<label for="amt2">Loan amount</label>
<input id="amt2" type="number" inputmode="decimal" placeholder="e.g., 650000">
<label for="rate2">Interest rate %</label>
<input id="rate2" type="number" step="0.01" inputmode="decimal" placeholder="e.g., 6.5">
<output id="out2">Enter amount and rate (30-year assumed).</output></div>

<div class="tool"><h2 style="margin-top:0">Rent-vs-sell napkin (departing owners)</h2>
<p>Monthly cash position if you keep the house as a rental. Every input is your data.</p>
<label for="rent3">Likely market rent</label>
<input id="rent3" type="number" inputmode="decimal" placeholder="e.g., 3400">
<label for="piti3">Your PITI + HOA</label>
<input id="piti3" type="number" inputmode="decimal" placeholder="e.g., 3100">
<label for="mgmt3">Management % of rent</label>
<input id="mgmt3" type="number" step="0.1" inputmode="decimal" placeholder="e.g., 10">
<label for="res3">Monthly vacancy + maintenance reserve</label>
<input id="res3" type="number" inputmode="decimal" placeholder="e.g., 300">
<output id="out3">Fill the four lines. Note: Hawaii GET applies to rental income — ask a tax
professional what your effective rate does to this number.</output></div>
{lead_form("TOOLS", "pcs-renter")}
</div>
<script>
(function(){{
 function n(id){{var v=parseFloat(document.getElementById(id).value);return isFinite(v)?v:null}}
 function money(x){{return (x<0?'-$':'$')+Math.abs(Math.round(x)).toLocaleString()}}
 function wire(ids,fn){{ids.forEach(function(id){{
   document.getElementById(id).addEventListener('input',fn)}})}}
 wire(['bah1','rent1'],function(){{
   var b=n('bah1'),r=n('rent1'),o=document.getElementById('out1');
   if(b==null||r==null){{o.textContent='Enter both numbers.';return}}
   var left=b-r;
   o.textContent=(left>=0?money(left)+' / month left for utilities and everything else.'
     :money(left)+' / month out of pocket before utilities.')}});
 wire(['amt2','rate2'],function(){{
   var a=n('amt2'),r=n('rate2'),o=document.getElementById('out2');
   if(a==null||r==null){{o.textContent='Enter amount and rate (30-year assumed).';return}}
   var i=r/100/12,m=360,p=i>0?a*i/(1-Math.pow(1+i,-m)):a/m;
   o.textContent='≈ '+money(p)+' / month principal & interest — before taxes, insurance, and HOA.'}});
 wire(['rent3','piti3','mgmt3','res3'],function(){{
   var r=n('rent3'),p=n('piti3'),m=n('mgmt3'),s=n('res3'),o=document.getElementById('out3');
   if([r,p,m,s].some(function(x){{return x==null}})){{return}}
   var net=r-p-(r*m/100)-s;
   o.textContent='≈ '+money(net)+' / month before GET and income tax. '+
     (net<0?'Negative cash flow is a choice some owners make for equity — make it on purpose.'
           :'Positive on paper — stress-test it against a two-month vacancy.')}});
}})();
</script>'''
    return page("/tools/", "PCS Oahu Tools: BAH-vs-Rent, Payment Check, Rent-vs-Sell | PCS Oahu",
                "Three free browser calculators for a Hawaii PCS: BAH-vs-rent fit, a payment "
                "reality check, and the departing owner's rent-vs-sell napkin. Nothing uploaded.",
                body, "/tools/")

def build():
    return {"/pcs-checklist/index.html": checklist_page(),
            "/tools/index.html": tools_page()}
