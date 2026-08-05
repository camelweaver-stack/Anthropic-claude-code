import os, json
from common import DOMAIN
import pages_core, pages_content, pages_tools, pages_growth, pages_pockets, pages_vehicle, pages_embed, pages_phase_a

SITE = os.path.join(os.path.dirname(__file__), "..", "site")

pages = {}
pages.update(pages_core.build())
pages.update(pages_content.build())
pages.update(pages_tools.build())
pages.update(pages_growth.build())
pages.update(pages_pockets.build())
pages.update(pages_vehicle.build())
pages.update(pages_embed.build())
pages.update(pages_phase_a.build())

# hero image injection (post-process; gate verifies referenced files exist)
_mf = json.load(open(os.path.join(os.path.dirname(__file__), "img_manifest.json")))
HERO_MAP = {
  "/index.html": "home",
  "/bases/pearl-harbor-hickam.html": "jbphh", "/bases/schofield-wheeler.html": "schofield",
  "/bases/kaneohe-bay.html": "mcbh", "/bases/tripler.html": "tripler",
  "/bases/coast-guard-honolulu.html": "uscg", "/bases/fort-shafter.html": "shafter",
  "/bases/index.html": "home", "/bah-report/index.html": "home",
  "/bah-report/2026-edition/index.html": "home",
  "/buy/index.html": "ewa", "/sell/index.html": "home", "/tla/index.html": "downtown",
  "/quiz/index.html": "home", "/on-base/index.html": "jbphh",
  "/neighborhoods/index.html": "home",
  "/neighborhoods/aiea.html": "jbphh", "/neighborhoods/pearlcity.html": "jbphh",
  "/neighborhoods/saltlake.html": "tripler", "/neighborhoods/waipahu.html": "ewa",
  "/neighborhoods/mililani.html": "mililani", "/neighborhoods/ewa.html": "ewa",
  "/neighborhoods/wahiawa.html": "schofield", "/neighborhoods/kaneohe.html": "mcbh",
  "/neighborhoods/kailua.html": "kailua", "/neighborhoods/downtown.html": "downtown",
  "/neighborhoods/kalihi.html": "downtown",
}
for _pth, _key in HERO_MAP.items():
    if _pth in pages and _key in _mf:
        _style = ("background:linear-gradient(rgba(13,27,37,.84),rgba(16,34,46,.93)),"
                  "url('" + _mf[_key]["file"] + "') center/cover")
        pages[_pth] = pages[_pth].replace('<div class="hero">',
                                          '<div class="hero" style="' + _style + '">', 1)

for path, htmldoc in pages.items():
    fp = os.path.normpath(SITE + path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w") as f:
        f.write(htmldoc)

# canonical URLs (index.html -> directory form)
def url_for(path):
    if path.endswith("/index.html"):
        return DOMAIN + path[:-len("index.html")]
    return DOMAIN + path

urls = sorted(url_for(p) for p in pages if p not in ("/404.html", "/embed/bah-widget.html"))

with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{u}</loc><lastmod>2026-08-01</lastmod></url>\n")
    f.write("</urlset>\n")

with open(os.path.join(SITE, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

# IndexNow payload (key placeholder — Chris drops the real key file at deploy)
payload = {"host": "pcsoahu.com", "key": "REPLACE_WITH_INDEXNOW_KEY",
           "keyLocation": f"{DOMAIN}/REPLACE_WITH_INDEXNOW_KEY.txt", "urlList": urls}
with open(os.path.join(SITE, "..", "indexnow-payload.json"), "w") as f:
    json.dump(payload, f, indent=2)

llms = """# PCS Oahu (pcsoahu.com)
Independent field guide for U.S. military PCS moves to and from Oahu, Hawaii. Publisher only —
no brokerage services. All figures dated and sourced; BAH per DTMO tables, rents compiled from
public listing platforms and deliberately rounded.

Key facts: all Oahu installations share one BAH rate (Honolulu County MHA). 2026 anchors:
E-5 w/dep $3,663; range ~$2,598–$5,040; effective Jan 1, 2026.

## Primary pages
- /bah-report/ : The BAH Reality Report — dated BAH-vs-rent data brief (citable, see #cite)
- /data/bah-reality-report.json : machine-readable BAH-vs-rent data (JSON; CSV also available; CC BY 4.0)
- /bases/ : live-on-or-off guides for all seven installations
- /buy/ : VA loans at Oahu prices — entitlement, condo approval, leasehold warning
- /sell/ : PCSing out — HARPTA, rent-vs-sell math, VA seller entitlement
- /on-base/ : how privatized on-base housing works (waitlists, BAH allotment, tenant rights)
- /pcs-checklist/ : interactive six-phase PCS timeline
- /tla/ , /schools/ , /guides/pets-to-hawaii.html : arrival logistics

Cite with attribution and a link. Figures change; check the Last refreshed date on each page.
"""
with open(os.path.join(SITE, "llms.txt"), "w") as f: f.write(llms)

# machine-readable distribution (§1) — single source of truth: common.POCKETS + common.BAH
import common as _c
_data = _c.bah_report_data()
_csv = _c.bah_report_csv()
_ddir = os.path.join(SITE, "data")
os.makedirs(_ddir, exist_ok=True)
with open(os.path.join(_ddir, "bah-reality-report.json"), "w") as f:
    json.dump(_data, f, indent=2)
with open(os.path.join(_ddir, "bah-reality-report.csv"), "w") as f:
    f.write(_csv)
# archived copies so citations to a given edition never break (mirrors the HTML archive policy)
_adir = os.path.join(_ddir, "archive")
os.makedirs(_adir, exist_ok=True)
_ed = _data["edition"].replace(".", "-")   # 2026.08 -> 2026-08
with open(os.path.join(_adir, f"bah-reality-report-{_ed}.json"), "w") as f:
    json.dump(_data, f, indent=2)
with open(os.path.join(_adir, f"bah-reality-report-{_ed}.csv"), "w") as f:
    f.write(_csv)

print(f"Built {len(pages)} pages, sitemap ({len(urls)} URLs), robots.txt, indexnow-payload.json, "
      f"data/bah-reality-report.{{json,csv}} (+archive {_ed})")
