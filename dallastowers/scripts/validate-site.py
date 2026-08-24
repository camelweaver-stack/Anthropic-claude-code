#!/usr/bin/env python3
"""Dallas Towers production validator. MUST pass before any deploy.

Checks:
  1. VALUE SEMANTICS — assessed/certified-roll data may never render under
     transaction-price labels. Forbidden visible phrases: "sale price", "sold for",
     "sale $/sf", "market sale price", "closed-sale", "closed sale", "recent avg"
     price patterns, and any bare "$N/sf" not qualified by "assessed".
     (Exception list below for legitimate editorial usage explaining non-disclosure.)
  2. PLACEHOLDERS — block editorial placeholders in visible content:
     FIRST-HAND FIELD NOTE, FIELD PHOTO, TODO:, FIXME:, [PLACEHOLDER, [INSERT,
     [ADD PHOTO, HOA TBD, FLOOR PLAN TBD, VERIFY HOA, VERIFY PET POLICY.
     "Not yet verified" is an intentional credibility phrase and is allowed.
     HTML comments (e.g. IDX-SLOT integration markers) are stripped before checking.
  3. INTERNAL LINKS — every internal href/src/action resolves to a file.
  4. SITEMAP — every sitemap URL has a file; parses as XML; no sitemap URL 404s locally.
  5. CANONICALS/NOINDEX — every sitemap page has a canonical and no noindex;
     404/thanks are noindexed and excluded from the sitemap.
  6. JSON-LD — every block parses; no fabricated review/rating/offer types.
  7. TITLES — no duplicate <title> across sitemap pages.
Exit 1 on any failure.
"""
import re, os, sys, json, html
from xml.etree import ElementTree

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
fails = []

def visible_text(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))

pages = [f for f in os.listdir(ROOT) if f.endswith(".html")]
site_pages = {}
for f in pages:
    site_pages[f] = open(os.path.join(ROOT, f), encoding="utf-8").read()

# --- 1. value semantics ---
ALLOWED_SALE_CONTEXTS = [
    "no sale prices exist", "texas is a non-disclosure state",
    "closed prices never enter the public record",
    "not confirmed arm", "trail market prices", "trail sale prices",
    "trail market sale prices", "do not disclose prices",
    "assessed values trail", "until closed sales exist",
    "no login walls",
]
SALE_PAT = re.compile(r"(sale price|sold for|sale \$\s*/\s*sf|market sale price|closed[- ]sale|closed sale|sold at \$|sales history|trailing average \u2248?\$)", re.I)
GENERIC_PRICE_TH = re.compile(r"<th>\s*(Price|\$/SF)\s*</th>", re.I)
BARE_PSF = re.compile(r"[·>]\s*\$[\d,]+/sf(?!\s*(assessed|·|\s*mo))", re.I)
for f, s in site_pages.items():
    vt = visible_text(s)
    for m in SALE_PAT.finditer(vt):
        ctx = vt[max(0, m.start()-160):m.end()+160].lower()
        if not any(a in ctx for a in ALLOWED_SALE_CONTEXTS):
            fails.append(f"[value-semantics] {f}: '{m.group(0)}' … {vt[max(0,m.start()-60):m.end()+60].strip()[:140]!r}")
    for m in GENERIC_PRICE_TH.finditer(s):
        fails.append(f"[value-semantics] {f}: generic table header {m.group(0)!r} \u2014 use 'Assessed value' / 'assessed $/sf' / typed transaction labels")
    # bare $/sf on cards must be qualified as assessed
    for m in re.finditer(r"·\s*\$[\d,]+/sf", vt):
        ctx = vt[max(0, m.start()-90):m.end()+30].lower()
        if "assessed" not in ctx and "/sf/mo" not in ctx:
            fails.append(f"[value-semantics] {f}: unqualified card figure {m.group(0)!r} — must read 'assessed $N/sf'")

# --- 2. placeholders ---
PLACEHOLDERS = ["FIRST-HAND FIELD NOTE","FIELD PHOTO","TODO:","FIXME:","[PLACEHOLDER","[INSERT","[ADD PHOTO","HOA TBD","FLOOR PLAN TBD","VERIFY HOA","VERIFY PET POLICY"]
for f, s in site_pages.items():
    vt = visible_text(s)
    for p in PLACEHOLDERS:
        if p in vt:
            fails.append(f"[placeholder] {f}: contains {p!r}")

# --- 3. internal links ---
files = set()
for dirpath, _, fns in os.walk(ROOT):
    for fn in fns:
        files.add(os.path.relpath(os.path.join(dirpath, fn), ROOT))
for f, s in site_pages.items():
    for m in re.finditer(r"""(?:href|src|action)=["']([^"']+)["']""", s):
        u = m.group(1)
        if re.match(r"^(https?:|mailto:|tel:|#|data:)", u): continue
        u = u.split("#")[0].split("?")[0].lstrip("/")
        if not u: continue
        if "${" in u: continue  # JS template literal
        if u in files or u + ".html" in files: continue
        fails.append(f"[link] {f}: unresolved internal ref '{m.group(1)}'")

# --- 4. sitemap ---
sm_path = os.path.join(ROOT, "sitemap.xml")
try:
    tree = ElementTree.parse(sm_path)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [e.text.strip() for e in tree.findall(".//s:loc", ns)]
except Exception as e:
    locs = []; fails.append(f"[sitemap] parse error: {e}")
sm_files = set()
for loc in locs:
    p = loc.replace("https://dallastowers.com/", "") or "index.html"
    sm_files.add(p)
    if p not in files:
        fails.append(f"[sitemap] {loc} has no file")
for excl in ("404.html", "thanks.html"):
    if excl in sm_files: fails.append(f"[sitemap] {excl} must not be in sitemap")

# --- 5. canonicals / noindex ---
for f, s in site_pages.items():
    noindex = re.search(r'name="robots"[^>]*noindex', s)
    canonical = 'rel="canonical"' in s
    if f in sm_files:
        if noindex: fails.append(f"[noindex] {f}: sitemap page carries noindex")
        if not canonical: fails.append(f"[canonical] {f}: sitemap page missing canonical")
    if f in ("404.html", "thanks.html") and not noindex:
        fails.append(f"[noindex] {f}: utility page must be noindexed")

# --- 6. JSON-LD ---
FORBIDDEN_LD = {"AggregateRating", "Review", "Offer"}
for f, s in site_pages.items():
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            obj = json.loads(m.group(1))
        except Exception as e:
            fails.append(f"[jsonld] {f}: invalid JSON-LD ({e})"); continue
        blob = json.dumps(obj)
        for t in FORBIDDEN_LD:
            if f'"@type": "{t}"' in blob or f'"@type":"{t}"' in blob:
                fails.append(f"[jsonld] {f}: fabricated-risk type {t}")

# --- 7. duplicate titles ---
titles = {}
for f, s in site_pages.items():
    if f not in sm_files: continue
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    if not m: fails.append(f"[title] {f}: missing <title>"); continue
    t = m.group(1).strip()
    if t in titles: fails.append(f"[title] duplicate: {f} == {titles[t]} ({t[:60]!r})")
    titles[t] = f

if fails:
    print(f"FAIL — {len(fails)} finding(s):")
    for x in fails: print("  " + x)
    sys.exit(1)
print(f"PASS — {len(pages)} pages, {len(locs)} sitemap URLs, {len(titles)} unique titles. All checks clean.")
