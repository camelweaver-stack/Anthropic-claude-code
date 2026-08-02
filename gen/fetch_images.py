#!/usr/bin/env python3
"""Fetch licensed hero imagery from Wikimedia Commons with attribution manifest."""
import json, os, urllib.request, urllib.parse

UA = {"User-Agent": "WFLBot/1.0 (https://westfwliving.com; chris@westfwliving.com)"}
OK_LICENSES = ("cc by", "cc-by", "cc0", "public domain", "pd")
OUT = os.path.join(os.path.dirname(__file__), "..", "site", "assets", "img")
os.makedirs(OUT, exist_ok=True)

QUERIES = {
  "home":      ["Diamond Head Honolulu aerial", "Oahu Hawaii coastline aerial"],
  "jbphh":     ["Pearl Harbor Hawaii aerial", "Pearl Harbor USS Arizona Memorial"],
  "schofield": ["Schofield Barracks Hawaii", "Wahiawa Oahu"],
  "mcbh":      ["Kaneohe Bay Oahu", "Marine Corps Base Hawaii Kaneohe"],
  "campsmith": ["Halawa Heights Oahu", "Aiea Hawaii Pearl Harbor view"],
  "tripler":   ["Tripler Army Medical Center", "Moanalua Oahu"],
  "uscg":      ["Honolulu Harbor", "Sand Island Honolulu"],
  "shafter":   ["Fort Shafter Hawaii", "Fort Shafter Palm Circle"],
  "kailua":    ["Kailua Beach Oahu", "Lanikai Beach"],
  "mililani":  ["Mililani Hawaii", "Central Oahu"],
  "downtown":  ["Honolulu skyline", "Kakaako Honolulu"],
  "ewa":       ["Kapolei Hawaii", "Ewa Beach Oahu"],
}

def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))

def find_image(query):
    data = api({"action": "query", "format": "json", "generator": "search",
                "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6, "gsrlimit": 8,
                "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1600})
    pages = (data.get("query") or {}).get("pages") or {}
    best = None
    for p in sorted(pages.values(), key=lambda x: x.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        w, h = ii.get("width", 0), ii.get("height", 0)
        if w < 1200 or h < 600 or h > w:  # need usable landscape
            continue
        meta = ii.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName", {}).get("value") or "").lower()
        if not any(k in lic for k in OK_LICENSES):
            continue
        artist = meta.get("Artist", {}).get("value") or "Unknown"
        # strip html from artist
        import re
        artist = re.sub(r"<[^>]+>", "", artist).strip()[:80] or "Unknown"
        best = {"thumb": ii.get("thumburl") or ii.get("url"),
                "title": p.get("title", ""), "artist": artist,
                "license": meta.get("LicenseShortName", {}).get("value", ""),
                "source": ii.get("descriptionurl", "")}
        break
    return best

manifest = {}
for key, queries in QUERIES.items():
    got = None
    for q in queries:
        try:
            got = find_image(q)
        except Exception as e:
            print(f"{key}: query error {e}")
        if got:
            break
    if not got:
        print(f"{key}: NO IMAGE FOUND — skipping")
        continue
    fp = os.path.join(OUT, f"{key}.jpg")
    try:
        req = urllib.request.Request(got["thumb"], headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r, open(fp, "wb") as f:
            f.write(r.read())
        sz = os.path.getsize(fp)
        if sz < 30000:
            os.remove(fp); print(f"{key}: file too small, skipped"); continue
        manifest[key] = {"file": f"/assets/img/{key}.jpg", **{k: got[k] for k in
                         ("title", "artist", "license", "source")}}
        print(f"{key}: OK {sz//1024}KB — {got['title']} [{got['license']}] by {got['artist']}")
    except Exception as e:
        print(f"{key}: download failed {e}")

with open(os.path.join(os.path.dirname(__file__), "img_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\nManifest: {len(manifest)} images")
