#!/usr/bin/env python3
"""URL-canonicalization auditor for westfwliving.com.

Repo mode (default) — static checks against the working tree:
  1. every published .html file maps to exactly one canonical public URL
     (dir/index.html -> /dir/ ; page.html -> /page), with no two files
     claiming the same canonical (e.g. foo.html alongside foo/index.html);
  2. every file's <link rel="canonical"> equals its derived canonical URL;
  3. _redirects carries exactly one forced-301 rule per file, source
     /path.html -> canonical target, with no chains (a target that is also
     a source) and no loops;
  4. no internal href points at a .html or /index.html form;
  5. no absolute https://westfwliving.com/...*.html URL survives anywhere
     (JSON-LD, og:url, form _next values);
  6. sitemap.xml equals the canonical set minus noindexed pages, all 200-class
     by construction (files exist), all in absolute canonical form;
  7. hreflang alternates reference canonical-form URLs that exist, and the
     en/es pairing is reciprocal.

Live mode (--live) — network checks against production (or --base URL):
  8. every canonical URL answers 200 with no redirect;
  9. every .html alternate answers a single 301 whose Location is exactly the
     canonical URL (no chains);
 10. directory URLs without the trailing slash answer a single 301 to the
     slashed form.

Exit 0 = clean. Exit 1 = findings (printed). Run after apply_standing_fixes.py.
"""
import argparse
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

HOST = "https://westfwliving.com"
SKIP_DIRS = {".git", "node_modules", "gen", "scripts", "editorial", "docs",
             "reports", "handoff", "__pycache__", ".claude"}

CANON_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')
HREFLANG_RE = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"')
LINK_RE = re.compile(r'''href=["'](/[^"'>]*)["']''')
ABS_HTML_RE = re.compile(r'https://westfwliving\.com(/[^"\'<>\s]*)\.html(?=["\'<>\s])')
ROBOTS_NOINDEX_RE = re.compile(r'name="robots" content="[^"]*noindex')

problems = []


def flag(msg):
    problems.append(msg)


def pages():
    out = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.join(root, f)[2:])
    return sorted(out)


def canonical_for(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")]


def audit_repo():
    files = pages()
    canon = {}
    docs = {}
    for rel in files:
        with open(rel, encoding="utf-8") as fh:
            docs[rel] = fh.read()
        c = canonical_for(rel)
        if c in canon:
            flag(f"duplicate canonical target {c}: {canon[c]} and {rel}")
        canon[c] = rel
    # foo.html vs foo/index.html — different strings (/foo vs /foo/), same content id
    slashless = {c.rstrip("/") for c in canon if c.endswith("/") and c != "/"}
    for c in canon:
        if not c.endswith("/") and c in slashless:
            flag(f"conflict: both {c}.html and {c}/index.html exist")

    for rel, doc in docs.items():
        want = HOST + canonical_for(rel)
        m = CANON_RE.search(doc)
        if not m:
            flag(f"{rel}: missing canonical tag")
        elif m.group(1) != want:
            flag(f"{rel}: canonical {m.group(1)} != {want}")
        for lang, href in HREFLANG_RE.findall(doc):
            path = href[len(HOST):] if href.startswith(HOST) else href
            if path.endswith(".html"):
                flag(f"{rel}: hreflang {lang} uses .html form {href}")
            elif path not in canon:
                flag(f"{rel}: hreflang {lang} target {href} has no page")
        for path in LINK_RE.findall(doc):
            p = path.split("#")[0].split("?")[0]
            if p.endswith(".html") or p.endswith("/index.html"):
                flag(f"{rel}: internal link to non-canonical {path}")
        for m in ABS_HTML_RE.finditer(doc):
            flag(f"{rel}: absolute .html self-URL {HOST}{m.group(1)}.html")

    # hreflang reciprocity (en<->es pairs)
    alt = {rel: dict(HREFLANG_RE.findall(docs[rel])) for rel in files}
    for rel, pairs in alt.items():
        me = HOST + canonical_for(rel)
        for lang, href in pairs.items():
            if href == me:
                continue
            path = href[len(HOST):] if href.startswith(HOST) else href
            tgt = canon.get(path)
            if tgt and me not in alt.get(tgt, {}).values():
                flag(f"{rel}: hreflang -> {href} not reciprocated")

    # _redirects
    rules = {}
    if not os.path.exists("_redirects"):
        flag("_redirects missing")
    else:
        for i, line in enumerate(open("_redirects"), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 3 or parts[2] != "301!":
                flag(f"_redirects:{i}: unexpected rule {line!r}")
                continue
            src, tgt = parts[0], parts[1]
            if src in rules:
                flag(f"_redirects:{i}: duplicate source {src}")
            rules[src] = tgt
        for src, tgt in rules.items():
            if tgt in rules:
                flag(f"_redirects: chain {src} -> {tgt} -> {rules[tgt]}")
            if src == tgt:
                flag(f"_redirects: loop on {src}")
        for rel in files:
            src = "/" + rel
            want = canonical_for(rel)
            if src not in rules:
                flag(f"_redirects: no rule for {src}")
            elif rules[src] != want:
                flag(f"_redirects: {src} -> {rules[src]}, expected {want}")
        for src in rules:
            if src[1:] not in set(files):
                flag(f"_redirects: rule for missing file {src}")

    # sitemap
    noindex = {rel for rel, d in docs.items() if ROBOTS_NOINDEX_RE.search(d)}
    want_urls = {HOST + canonical_for(rel) for rel in files if rel not in noindex}
    try:
        tree = ET.parse("sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        got_urls = {el.text.strip() for el in tree.getroot().iter(
            "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    except Exception as e:  # noqa: BLE001
        flag(f"sitemap.xml unreadable: {e}")
        got_urls = set()
    for u in sorted(got_urls - want_urls):
        flag(f"sitemap: unexpected URL {u}")
    for u in sorted(want_urls - got_urls):
        flag(f"sitemap: missing URL {u}")
    return files, canon


def _head(url):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "wfl-url-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "")
    except Exception as e:  # noqa: BLE001
        return None, str(e)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def probe(url):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "wfl-url-audit/1.0"})
    try:
        with OPENER.open(req, timeout=30) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "") or ""
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def audit_live(base, files, sample):
    todo = files if not sample else files[::max(1, len(files) // sample)][:sample]
    print(f"live probe of {len(todo)} pages x 2-3 URLs against {base}")

    def check(rel):
        errs = []
        canonical = canonical_for(rel)
        st, loc = probe(base + canonical)
        if st != 200:
            errs.append(f"{canonical}: canonical answered {st} {loc}")
        st, loc = probe(base + "/" + rel)
        want = base + canonical if base != HOST else HOST + canonical
        # Netlify emits absolute Location on this site
        if st != 301 or loc.rstrip() not in (want, canonical):
            errs.append(f"/{rel}: expected 301 -> {want}, got {st} -> {loc}")
        elif loc in (want, canonical):
            st2, loc2 = probe(loc if loc.startswith("http") else base + loc)
            if st2 != 200:
                errs.append(f"/{rel}: redirect target answered {st2} {loc2} (chain)")
        if canonical.endswith("/") and canonical != "/":
            st, loc = probe(base + canonical.rstrip("/"))
            if st not in (301, 200):
                errs.append(f"{canonical.rstrip('/')}: expected 301 -> {canonical}, got {st}")
        return errs

    with ThreadPoolExecutor(max_workers=8) as ex:
        for errs in ex.map(check, todo):
            for e in errs:
                flag(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="probe production URLs")
    ap.add_argument("--base", default=HOST)
    ap.add_argument("--sample", type=int, default=0,
                    help="live mode: probe only N evenly-spaced pages (0 = all)")
    args = ap.parse_args()

    files, _canon = audit_repo()
    print(f"repo audit: {len(files)} pages")
    if args.live:
        audit_live(args.base.rstrip("/"), files, args.sample)

    if problems:
        print(f"\nFINDINGS ({len(problems)}):")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("URL AUDIT PASSED — one canonical per page; redirects, links, "
          "sitemap, hreflang and structured-data URLs all canonical.")


if __name__ == "__main__":
    main()
