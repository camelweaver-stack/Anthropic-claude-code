# PCS Oahu — The Family Layer. Renders ONLY from data/source/*.json (zero generated facts).
from common import *
from pages_core import BASES

_SRC = os.path.join(os.path.dirname(__file__), "..", "data", "source")
SCHOOLS = json.load(open(os.path.join(_SRC, "oahu_elementary_schools.json")))
COMMUTE = json.load(open(os.path.join(_SRC, "commute_grid.json")))
CCRATES = json.load(open(os.path.join(_SRC, "childcare_oahu_rates.json")))

# Site base slug -> the installation key used in the source data (Wheeler folds into Schofield;
# Coast Guard Honolulu has no school/commute data in this ingest, so it gets no family page in v1).
BASE_INSTALL = {
    "pearl-harbor-hickam": "JB Pearl Harbor-Hickam",
    "schofield-wheeler":   "Schofield Barracks",
    "kaneohe-bay":         "MCBH Kaneohe Bay",
    "camp-smith":          "Camp H.M. Smith",
    "tripler":             "Tripler AMC",
    "fort-shafter":        "Fort Shafter",
}
BASE_BY_SLUG = {b["slug"]: b for b in BASES}
FAMILY_BASES = [b for b in BASES if b["slug"] in BASE_INSTALL]

# pocket display name (as used in the commute grid) -> pocket slug
DISPLAY_TO_SLUG = {v[0]: k for k, v in POCKETS.items()}

SCHOOLS_SRC = f'{SCHOOLS["source"]}. Pulled {SCHOOLS["pulled"]}.'
COMMUTE_SRC = f'{COMMUTE["methodology"]} Pulled {COMMUTE["pulled"]}.'
# Verified-resolving official landing pages (deep paths rot, so we link stable roots/sections).
DOE_LOCATOR   = "https://www.hawaiipublicschools.org"                  # DOE school finder + geographic exception
DHS_CHILDCARE = "https://humanservices.hawaii.gov/bessd/child-care/"   # DHS BESSD child care licensing + finder
PATCH_URL     = "https://www.patchhawaii.org/"
PATCH_LINE    = "808-839-1988"
MCC_URL       = "https://www.militarychildcare.com/"

def _fmt(n): return f"${n:,.0f}"

def _license_note():
    return ('<p class="fine"><strong>Before you visit any provider,</strong> confirm its current '
            'license status directly with the state — licenses lapse and change. This site publishes '
            'no provider roster; use the official finders below.</p>')

# ---------- Commute Reality Grid ----------
def commute_grid_page():
    gates = sorted({k for p in COMMUTE["grid"].values() for k in p})
    head = "".join(f"<th>{g}</th>" for g in gates)
    rows = ""
    for disp, cells in COMMUTE["grid"].items():
        tds = ""
        for g in gates:
            c = cells.get(g, {})
            ff = c.get("freeflow_min")
            pk = c.get("peak_min")
            ff_s = f"{ff}" if ff is not None else "—"
            pk_s = f"{pk}" if pk is not None else "—"
            tds += f'<td><span class="v">{ff_s}</span> <span class="fine">/ {pk_s}</span></td>'
        rows += f"<tr><th>{disp}</th>{tds}</tr>"
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Tool · dated, sourced, methodology-first</p>
<h1>The Commute Reality Grid</h1>
<p class="lede">Every Oahu pocket against every installation, in drive-minutes. Oahu punishes the
mainland instinct of picking a neighborhood before checking the drive — start here. Two numbers
per cell: <strong>free-flow</strong> / <strong>typical peak</strong>.</p>
</div></div>
<div class="wrap">
<div style="overflow-x:auto">
<table class="data"><thead><tr><th>Pocket \\ Installation</th>{head}</tr></thead>
<tbody>{rows}</tbody></table>
</div>
<p class="fine">Each cell: free-flow minutes / typical-peak minutes. Peak sampling is pending, so
peak renders as an em-dash (—) until it lands — free-flow with honest methodology beats fake
precision.</p>
<div class="warn"><strong>Methodology.</strong> {COMMUTE["methodology"]} Pulled {COMMUTE["pulled"]}.
Reference points are centroids, not your address; your mileage will literally vary.</div>
<p style="max-width:46rem">Machine-readable: <a href="/data/commute-grid.json">commute-grid.json</a>
(free to reuse with attribution). See the <a href="/data/">data desk</a> for the full roster.</p>
{lead_form("COMMUTEGRID", "pcs-renter", heading="Get the peak-band update",
  blurb="When traffic-aware peak sampling lands, list members get the refreshed grid first.")}
</div>'''
    ds = {"@context": "https://schema.org", "@graph": [{
        "@type": "Dataset", "@id": DOMAIN + "/tools/commute-grid/#dataset",
        "name": "The Commute Reality Grid — Oahu pockets × installations",
        "description": "Free-flow drive minutes between 11 Oahu neighborhood pockets and 7 military "
                       "installations, via OSRM public routing, rounded to 5 minutes. Peak bands pending.",
        "url": DOMAIN + "/tools/commute-grid/", "sameAs": DOMAIN + "/data/",
        "creator": {"@id": DOMAIN + "/#org"}, "publisher": {"@id": DOMAIN + "/#org"},
        "license": LICENSE_URL, "isAccessibleForFree": True,
        "datePublished": COMMUTE["pulled"], "dateModified": COMMUTE["pulled"],
        "spatialCoverage": {"@type": "Place", "name": "Oahu, Honolulu County, Hawaii, USA"},
        "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json",
                          "contentUrl": DOMAIN + "/data/commute-grid.json"}],
        "citation": 'PCS Oahu, "The Commute Reality Grid," pcsoahu.com/tools/commute-grid/'}]}
    return page("/tools/commute-grid/",
        "The Commute Reality Grid: Oahu Pockets × Bases, in Drive-Minutes | PCS Oahu",
        "Free-flow drive times between every Oahu neighborhood pocket and every installation, "
        "dated and sourced (OSRM), rounded to 5 minutes. Methodology on-page.",
        body, "/tools/", jsonld=ds)

# ---------- The Second Paycheck Report (/family/childcare/) ----------
def second_paycheck_report():
    rows = ""
    for c in CCRATES["care_types"]:
        rows += (f'<tr><td>{c["type"]}</td><td class="num">{_fmt(c["median"])}</td>'
                 f'<td class="num">{_fmt(c["p75"])}</td><td class="num">{c["providers"]}</td></tr>')
    # calculator options from the SAME sourced figures (median monthly cost per care type)
    opts = "".join(f'<option value="{c["median"]}">{c["type"]} — {_fmt(c["median"])}/mo (median)</option>'
                   for c in CCRATES["care_types"] if c["median"] > 200)
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Named data brief · The Second Paycheck Report</p>
<h1>The Second Paycheck Report</h1>
<p class="lede">The question every dual-income family reaching Oahu actually asks: after childcare,
what does the second job really net? Here are the licensed-care costs, sourced and dated — and an
honest calculator so you can run your own number, not ours.</p>
</div></div>
<div class="wrap">
<h2>What licensed care costs on Oahu</h2>
<p style="max-width:46rem">Full-time monthly rates from the {CCRATES["product_source"]},
{CCRATES["table"]}. CCDF suggests the <strong>75th percentile</strong> as the access benchmark —
the rate that clears three-quarters of the market. Provider counts are shown so you can weigh the
smaller samples honestly.</p>
<table class="data"><thead><tr><th>Type of care</th><th class="num">Median /mo</th>
<th class="num">75th pctile /mo</th><th class="num"># providers</th></tr></thead>
<tbody>{rows}</tbody></table>
<p class="fine">Source: {CCRATES["product_source"]}. Pulled {CCRATES["pulled"]}. Rates are
full-time monthly; the study segments by care type, not single-year age bands. {CCRATES["note"]}</p>

<h2>The crossover: what the second job nets</h2>
<p style="max-width:46rem">Enter the second earner's expected <em>monthly take-home</em> and pick a
care option. This runs entirely on your device; nothing is sent anywhere. We supply the sourced
cost — you supply your wage, because a "representative Oahu wage" would be a number we made up.</p>
<div class="tool" id="spr">
  <label for="sprwage">Second earner — monthly take-home ($)</label>
  <input id="sprwage" type="number" inputmode="numeric" placeholder="e.g., 3200" style="max-width:16rem">
  <label for="sprcare" style="margin-top:.6rem">Childcare option (sourced median)</label>
  <select id="sprcare" style="max-width:100%">{opts}</select>
  <p><button class="btn" type="button" id="sprgo">Run the math</button></p>
  <div id="sprout" style="font-weight:700"></div>
  <p class="fine">One child, one care slot, full-time. Add a slot per child. Ignores commuting,
  taxes on the margin, and fee assistance — for which see the on-base and CCDF options below.</p>
</div>
<h2>Before you assume it doesn't pencil</h2>
<p style="max-width:46rem">On-base Child Development Centers use income-banded fees that can land
well below market, and CCDF/DHS fee assistance exists for eligible families. Start those in
parallel — waitlists are the constraint, not eligibility. See the base pages under
<a href="/family/">the family layer</a> for the finders.</p>
<section id="cite"><h2>Cite this report</h2>
<p style="max-width:46rem;font-family:'IBM Plex Mono',monospace;font-size:.88rem;background:#fff;
border:1px solid var(--rule);border-radius:6px;padding:.8rem 1rem">PCS Oahu, "The Second Paycheck
Report," {BUILD_DATE} edition, pcsoahu.com/family/childcare/. Cost data: {CCRATES["product_source"]}.</p></section>
<p style="max-width:46rem">Machine-readable:
<a href="/data/second-paycheck-report.json">JSON</a> ·
<a href="/data/second-paycheck-report.csv">CSV</a> — free to reuse with attribution (CC BY 4.0).</p>
{lead_form("FAMILYCARE", "pcs-renter", heading="Get the next edition first",
  blurb="The Second Paycheck Report refreshes with each PATCH market-rate study. Join the list and "
        "it lands before it publishes here.")}
</div>
<script>
(function(){{
 var w=document.getElementById('sprwage'),s=document.getElementById('sprcare'),
     b=document.getElementById('sprgo'),o=document.getElementById('sprout');
 function money(n){{return '$'+Math.round(n).toLocaleString();}}
 b.addEventListener('click',function(){{
   var wage=parseFloat(w.value||'0'),cost=parseFloat(s.value||'0');
   if(!wage){{o.textContent='Enter a monthly take-home to run the math.';return;}}
   var net=wage-cost, pct=Math.round(net/wage*100);
   o.innerHTML='After '+money(cost)+'/mo childcare, the second paycheck nets <u>'+money(net)+
     '/mo</u> ('+pct+'% of take-home). '+(net<0?'The care cost exceeds the wage at this option — '+
     'price the on-base CDC and fee assistance before deciding.':'Weigh it against the on-base CDC '+
     'and fee-assistance options, which often price lower.');
 }});
}})();
</script>'''
    ds = {"@context": "https://schema.org", "@graph": [{
        "@type": "Dataset", "@id": DOMAIN + "/family/childcare/#dataset",
        "name": "The Second Paycheck Report — Oahu licensed-childcare costs",
        "description": "Full-time monthly licensed child care rates on Oahu by care type (median and "
                       "75th percentile) from the Hawaii DHS/CCDF biennial market rate study, set "
                       "against a bring-your-own-wage crossover calculator.",
        "url": DOMAIN + "/family/childcare/", "sameAs": DOMAIN + "/data/",
        "creator": {"@id": DOMAIN + "/#org"}, "publisher": {"@id": DOMAIN + "/#org"},
        "license": LICENSE_URL, "isAccessibleForFree": True,
        "datePublished": REFRESH_ISO, "dateModified": REFRESH_ISO,
        "spatialCoverage": {"@type": "Place", "name": "Oahu, Honolulu County, Hawaii, USA"},
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": DOMAIN + "/data/second-paycheck-report.json"},
            {"@type": "DataDownload", "encodingFormat": "text/csv",
             "contentUrl": DOMAIN + "/data/second-paycheck-report.csv"}],
        "citation": 'PCS Oahu, "The Second Paycheck Report," pcsoahu.com/family/childcare/'}]}
    return page("/family/childcare/",
        "The Second Paycheck Report: Oahu Childcare Costs vs the Second Job | PCS Oahu",
        "Sourced Oahu licensed-childcare monthly costs (Hawaii DHS/CCDF market-rate study) plus a "
        "bring-your-own-wage calculator: what does the second paycheck net after care?",
        body, "/guides/", jsonld=ds)

# ---------- Per-base family pages ----------
def _schools_near(install_key, limit=12):
    ranked = sorted(SCHOOLS["schools"], key=lambda s: s["miles_to_installation"].get(install_key, 9e9))
    return ranked[:limit]

def _commute_for(install_key):
    band = {"≤10 min": [], "10–20 min": [], "20–30 min": [], "30+ min": []}
    for disp, cells in COMMUTE["grid"].items():
        ff = cells.get(install_key, {}).get("freeflow_min")
        if ff is None: continue
        k = "≤10 min" if ff <= 10 else "10–20 min" if ff <= 20 else "20–30 min" if ff <= 30 else "30+ min"
        band[k].append((disp, ff))
    return band

def family_base_page(b):
    ik = BASE_INSTALL[b["slug"]]
    schools = _schools_near(ik)
    srows = "".join(
        f'<tr><td>{s["name"]}{" · charter" if s.get("charter") else ""}</td>'
        f'<td>{s["city"]}</td><td class="num">{s["grades"]}</td>'
        f'<td class="num">{s["enrollment"]}</td></tr>' for s in schools)
    band = _commute_for(ik)
    crows = ""
    for k, items in band.items():
        if not items: continue
        pockets = ", ".join(f'<a href="/neighborhoods/{DISPLAY_TO_SLUG[d]}.html">{d}</a>'
                            for d, _ in sorted(items, key=lambda x: x[1]) if d in DISPLAY_TO_SLUG)
        crows += f'<tr><td class="num">{k}</td><td>{pockets}</td></tr>'
    cc = {c["type"]: c for c in CCRATES["care_types"]}
    ccexample = cc.get("Licensed center-based or group child care home", CCRATES["care_types"][2])
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Family layer · {b["side"]} · Honolulu County MHA</p>
<h1>{b["name"]}: the family map</h1>
<p class="lede">Schools, childcare, and the commute — the three things that decide where a family
lands around {b["short"]}. Every name and figure below is pulled from a public source with the
date shown; confirm anything address-specific before you sign.</p>
</div></div>
<div class="wrap">

<h2>Licensed childcare within reach</h2>
<p style="max-width:46rem">Oahu's licensed providers aren't published as a downloadable list, and we
won't reprint a partial one. Use the authoritative finders, then verify each provider's current
license before visiting:</p>
<ul>
  <li><a href="{DHS_CHILDCARE}" rel="nofollow">Hawaii DHS child care licensing &amp; provider finder</a> — the official source for licensed providers and license status.</li>
  <li><a href="{PATCH_URL}" rel="nofollow">PATCH</a> statewide child care referral line: <strong>{PATCH_LINE}</strong> — free referrals by town and age.</li>
  <li><a href="{MCC_URL}" rel="nofollow">MilitaryChildCare.com</a> — the on-base CDC waitlist for {b["short"]}. Waitlists are the real constraint; request the day orders drop. Income-banded fees and CCDF fee assistance can land well below market.</li>
</ul>
<p style="max-width:46rem">For what care costs and whether the second job pencils, see
<a href="/family/childcare/">The Second Paycheck Report</a> — e.g., a {ccexample["type"].lower()}
runs a median of {_fmt(ccexample["median"])}/mo ({CCRATES["product_source"].split("(")[0].strip()}).</p>
{_license_note()}

<h2>Public elementary schools near the gate</h2>
<p style="max-width:46rem">The nearest open public elementary schools to {b["short"]}, from the
federal directory. This lists <em>public</em> schools only (private/parochial to come). We do not
rank schools and we never publish attendance boundaries — <strong>your exact zoned school depends on
your address; confirm at the <a href="{DOE_LOCATOR}" rel="nofollow">DOE school finder</a> before you
sign a lease</strong>, and see the DOE Geographic Exception process for out-of-zone requests.</p>
<table class="data"><thead><tr><th>School</th><th>Town</th><th class="num">Grades</th>
<th class="num">Enrollment</th></tr></thead><tbody>{srows}</tbody></table>
<p class="fine">Source: {SCHOOLS_SRC} Ordered by proximity to the installation reference point
(internal only — distances not published). Enrollment and grade span as reported to NCES.</p>

<h2>Commute reality</h2>
<p style="max-width:46rem">Which pockets reach {b["short"]} in what free-flow time. Peak bands are
pending (shown as —). Full grid: <a href="/tools/commute-grid/">the Commute Reality Grid</a>.</p>
<table class="data"><thead><tr><th class="num">Free-flow band</th><th>Pockets</th></tr></thead>
<tbody>{crows}</tbody></table>
<p class="fine">Source: {COMMUTE_SRC}</p>

<h2>The spouse-work picture</h2>
<p style="max-width:46rem">A PCS to Oahu usually means a career interruption for the accompanying
spouse — and a set of programs built to soften it. Hawaii recognizes many out-of-state professional
licenses through military-spouse provisions; federal hiring has a spouse-preference path; and the
MSEP partner network, NAF/MWR, and the exchanges hire locally. The remote-work option is real but
runs into the time-zone math. The <a href="/family/spouse-jobs/">spouse-jobs directory</a> links
each official starting point — no placement pitch, just the doors.</p>

{lead_form("FAMILY" + b["tag"], "pcs-renter",
  heading="Bringing a family to " + b["short"] + "?",
  blurb="Join the list for the school-year and childcare refreshes for these pockets, timed to your "
        "report window. No spam. Leave anytime.")}
</div>'''
    path = f"/family/{b['slug']}/"
    return path + "index.html", page(path,
        f"{b['name']} for Families: Schools, Childcare, Commute | PCS Oahu",
        f"The family map for {b['short']}: nearest public elementary schools, licensed-childcare "
        f"finders and costs, and the commute bands by pocket. Sourced and dated.",
        body, "", jsonld=crumbs_ld(path))

# ---------- Family hub ----------
def family_hub():
    cards = "".join(
        f'<div class="card"><span class="tag">{b["side"]}</span>'
        f'<h3><a href="/family/{b["slug"]}/">{b["name"]}</a></h3>'
        f'<p>Schools, childcare finders, and commute bands for families around {b["short"]}.</p></div>'
        for b in FAMILY_BASES)
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">The family layer · sourced, dated, honest</p>
<h1>Moving a family to Oahu</h1>
<p class="lede">Schools, childcare, the commute, and the spouse-career question — mapped per
installation, every fact pulled from a public source with its date shown. We rank nothing and
publish no attendance boundaries; we point you at the official tools and tell you what care costs.</p>
</div></div>
<div class="wrap">
<div class="grid c2">
  <div class="card"><span class="tag">Data brief</span>
    <h3><a href="/family/childcare/">The Second Paycheck Report</a></h3>
    <p>Sourced Oahu childcare costs and a bring-your-own-wage crossover calculator.</p></div>
  <div class="card"><span class="tag">Tool</span>
    <h3><a href="/tools/commute-grid/">The Commute Reality Grid</a></h3>
    <p>Every pocket against every installation, in drive-minutes.</p></div>
  <div class="card"><span class="tag">Careers</span>
    <h3><a href="/family/spouse-jobs/">Spouse jobs & license portability</a></h3>
    <p>The official doors: MSEP, federal spouse preference, NAF/MWR, DCCA license recognition.</p></div>
</div>
<h2>By installation</h2>
<div class="grid c2">{cards}</div>
<p class="fine">Coast Guard Base Honolulu isn't in this release's school/commute dataset yet; its
family page follows when that data lands. Private/parochial schools and a named-employer table are
also deferred to a later cycle — v1 links the official finders rather than reprint a partial list.</p>
{lead_form("FAMILYHUB", "pcs-renter")}
</div>'''
    return page("/family/", "PCS Oahu Family Layer: Schools, Childcare, Commute, Spouse Jobs | PCS Oahu",
        "Per-installation family guides for a PCS to Oahu: nearest public schools, licensed-childcare "
        "finders and costs, commute bands, and spouse-career resources. Sourced and dated.",
        body, "/guides/")

# ---------- Spouse jobs ----------
def spouse_jobs():
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">Family layer · a directory, not a pitch</p>
<h1>Spouse jobs & license portability on Oahu</h1>
<p class="lede">A PCS shouldn't end a career. These are the official starting points for
military-spouse employment and professional-license recognition in Hawaii — linked directly,
because the live portals are always more current than any snapshot we'd reprint. No company is
recommended here; no placement service is sold.</p>
</div></div>
<div class="wrap">
<h2>Hiring paths</h2>
<ul>
  <li><a href="https://msepjobs.militaryonesource.mil" rel="nofollow">MSEP — Military Spouse Employment Partnership</a>: the partner-employer job board; filter for Oahu/Hawaii postings.</li>
  <li><a href="https://www.usajobs.gov/" rel="nofollow">Federal spouse preference (USAJOBS)</a>: the noncompetitive Military Spouse hiring authority for federal roles, including on-island DoD positions.</li>
  <li>NAF/MWR and the exchanges (AAFES/NEX/MCX) hire locally on every installation — check each installation's MWR and exchange careers pages.</li>
</ul>
<h2>Professional license recognition</h2>
<p style="max-width:46rem">Hawaii has military-spouse provisions for recognizing out-of-state
professional licenses. Rules differ by board (teaching, nursing, cosmetology, and others), so
confirm your specific license with the state before you count on it:</p>
<ul>
  <li><a href="https://cca.hawaii.gov/pvl/" rel="nofollow">Hawaii DCCA — Professional & Vocational Licensing</a>: the boards and the military-spouse recognition provisions.</li>
</ul>
<h2>The remote-work reality</h2>
<p style="max-width:46rem">Keeping a mainland remote job is the most common Oahu spouse-career play,
and it works — with the time-zone tax. Hawaii is UTC−10: a 9-to-5 Eastern job is 3 a.m. to noon
local. Roles anchored to Pacific time, or async-friendly ones, travel best. Verify your employer's
out-of-state payroll and any state-tax implications before the move.</p>
<div class="warn"><strong>No endorsements.</strong> Links are official starting points, not
recommendations. Verify eligibility, licensing, and terms with each agency or employer directly.</div>
{lead_form("SPOUSEJOBS", "pcs-renter",
  heading="Working the spouse-career problem?",
  blurb="Join the list for updates when Hawaii's license-recognition rules or the federal spouse "
        "hiring paths change.")}
</div>'''
    return page("/family/spouse-jobs/",
        "Military Spouse Jobs & License Portability on Oahu | PCS Oahu",
        "Official starting points for military-spouse employment in Hawaii: MSEP, federal spouse "
        "preference, NAF/MWR and exchanges, DCCA license recognition, and the remote-work reality.",
        body, "/guides/")

def build():
    out = {
        "/tools/commute-grid/index.html": commute_grid_page(),
        "/family/index.html": family_hub(),
        "/family/childcare/index.html": second_paycheck_report(),
        "/family/spouse-jobs/index.html": spouse_jobs(),
    }
    for b in FAMILY_BASES:
        p, h = family_base_page(b)
        out[p] = h
    return out
