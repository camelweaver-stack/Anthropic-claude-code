#!/usr/bin/env python3
"""PCS Oahu QA gate battery. Run from anywhere: python3 gate.py [site_dir]
Exits nonzero on any failure. Ship this with the package; run before every deploy."""
import os, re, sys, glob

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "site")
DOMAIN = "https://pcsoahu.com"
FAILS = []

def fail(msg): FAILS.append(msg)

html_files = sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True))
if not html_files: fail("No HTML files found")

NAV_EXPECTED = 11
FORBIDDEN = [
    r"\bour agents?\b", r"\bour brokerage\b", r"\bour leasing\b", r"\bconsultation\b",
    r"\bschedule a (?:showing|tour|call)\b", r"\bapartment locat", r"\blist with us\b",
    r"\bwe(?:'ll| will) find you\b", r"\bhire us\b", r"\bcontact us to (?:buy|sell|rent)\b",
    r"\bfree home valuation\b", r"\bwork with (?:us|me)\b", r"\brepresent(?:ing)? you\b",
    r"crime rate", r"\bsafest neighborhood", r"\blow.crime\b",
]
CONTEXT_FIELDS = {"move_date", "sell_timeline"}

for fp in html_files:
    rel = os.path.relpath(fp, SITE)
    doc = open(fp).read()

    # embed widget: standalone iframe — its own mini-battery, then skip site chrome checks
    if rel.replace(os.sep, "/") == "embed/bah-widget.html":
        if 'name="robots" content="noindex"' not in doc: fail(f"{rel}: widget must be noindex")
        if 'rel="canonical"' not in doc: fail(f"{rel}: widget missing canonical")
        if "Equal Housing Opportunity" not in doc: fail(f"{rel}: widget missing EHO")
        if "/bah-report/?utm_source=embed" not in doc: fail(f"{rel}: widget missing attribution link")
        if "Last refreshed" not in doc: fail(f"{rel}: widget missing refresh date")
        continue

    # 1. nav count
    navm = re.search(r'<nav class="main".*?</nav>', doc, re.S)
    links = len(re.findall(r"<a ", navm.group(0))) if navm else 0
    if links != NAV_EXPECTED:
        fail(f"{rel}: nav has {links} links, expected {NAV_EXPECTED}")

    # 2. head requirements
    if '<link rel="canonical"' not in doc: fail(f"{rel}: missing canonical")
    if not re.search(r"<title>.+</title>", doc): fail(f"{rel}: missing title")
    if 'name="description"' not in doc: fail(f"{rel}: missing meta description")
    if '/assets/favicon.svg' not in doc: fail(f"{rel}: missing favicon link")
    for og in ('og:title','og:description','og:url','og:image'):
        if f'property="{og}"' not in doc: fail(f"{rel}: missing {og}")
    if 'name="twitter:card"' not in doc: fail(f"{rel}: missing twitter card")

    # 3. EHO + data disclaimer
    if "Equal Housing Opportunity" not in doc: fail(f"{rel}: missing EHO")
    if "not a real estate brokerage" not in doc: fail(f"{rel}: missing publisher disclaimer")

    # 4. hreflang must NOT exist (no second language shipped)
    if "hreflang" in doc: fail(f"{rel}: unexpected hreflang (site ships no mirror)")

    # 5. forbidden language
    low = doc.lower()
    for pat in FORBIDDEN:
        if re.search(pat, low): fail(f"{rel}: forbidden language matches /{pat}/")

    # 6. form assertions (every form on page)
    for form in re.findall(r"<form class=\"lead\".*?</form>", doc, re.S):
        if 'action="https://formsubmit.co/leads@anastasiaweaver.com"' not in form:
            fail(f"{rel}: form action wrong")
        m = re.search(r'name="_subject" value="(PCSOAHU-[A-Z]+)"', form)
        if not m: fail(f"{rel}: form missing PCSOAHU-* _subject")
        if 'name="audience" value="referral-hi-oahu-pcs"' not in form:
            fail(f"{rel}: form missing audience=referral-hi-oahu-pcs")
        if not re.search(r'name="segment" value="pcs-(renter|buyer|seller)"', form):
            fail(f"{rel}: form missing segment field")
        if not re.search(r'name="phone" type="tel" required', form):
            fail(f"{rel}: phone not required tel")
        if not re.search(r'name="email" type="email" required autocomplete="email"', form):
            fail(f"{rel}: email field wrong")
        if 'autocomplete="name"' not in form or 'autocomplete="tel"' not in form:
            fail(f"{rel}: autocomplete attrs missing")
        ctx = set(re.findall(r'name="(move_date|sell_timeline)"', form))
        if not ctx: fail(f"{rel}: form missing context field")
        if not ctx <= CONTEXT_FIELDS: fail(f"{rel}: unknown context field {ctx}")
        seg = re.search(r'name="segment" value="(pcs-\w+)"', form)
        if seg and seg.group(1) == "pcs-seller" and "sell_timeline" not in ctx:
            fail(f"{rel}: seller form must use sell_timeline")
        if seg and seg.group(1) != "pcs-seller" and "move_date" not in ctx:
            fail(f"{rel}: non-seller form must use move_date")

# 6b. freshness: any page with a rates block must show refresh date
    if 'class="rates"' in doc and "Last refreshed:" not in doc:
        fail(f"{rel}: rates block without visible refresh date")

# 6c. images: referenced /assets/img files must exist; credits present when heroes used
    for imref in re.findall(r"/assets/img/([\w.-]+\.jpg)", doc):
        if not os.path.exists(os.path.join(SITE, "assets", "img", imref)):
            fail(f"{rel}: references missing image {imref}")
    if "url('/assets/img/" in doc and "Photo credits" not in doc:
        fail(f"{rel}: hero image without credits footer")

# 7. sitemap/loc parity
sm = open(os.path.join(SITE, "sitemap.xml")).read()
locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
expected = set()
for fp in html_files:
    rel = "/" + os.path.relpath(fp, SITE).replace(os.sep, "/")
    if rel in ("/404.html", "/embed/bah-widget.html"): continue
    expected.add(DOMAIN + (rel[:-len("index.html")] if rel.endswith("/index.html") else rel))
if locs != expected:
    fail(f"sitemap parity: only-in-sitemap={sorted(locs-expected)} missing={sorted(expected-locs)}")

rep = open(os.path.join(SITE, "bah-report", "index.html")).read()
if "Cite this report" not in rep: fail("bah-report: missing cite block")
if '"@type": "Dataset"' not in rep: fail("bah-report: missing Dataset schema")

if FAILS:
    print(f"GATE FAILED — {len(FAILS)} issue(s):")
    [print("  ✗ " + f) for f in FAILS]
    sys.exit(1)
print(f"GATE PASSED — {len(html_files)} pages, {len(locs)} sitemap URLs, all assertions green.")
