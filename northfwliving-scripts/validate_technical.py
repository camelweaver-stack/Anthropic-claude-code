#!/usr/bin/env python3
"""Technical gate for northfwliving.com production HTML.

Fails (exit 1) on structural defects that would hurt the live site:

  * missing/empty <title>
  * duplicate <title> across pages
  * missing canonical, or canonical that does not match the page's own URL
  * missing/incomplete hreflang cluster (en + es + x-default expected)
  * <html lang> attribute inconsistent with the /es/ path prefix
  * any robots noindex
  * missing meta description
  * internal links or asset references that resolve to nothing on disk
  * sitemap.xml entries with no file on disk, and indexable pages missing
    from sitemap.xml

Usage: validate_technical.py [site_root]   (default: ../northfwliving)
"""
import io
import os
import re
import sys
from urllib.parse import urlparse

DOMAIN = "https://northfwliving.com"


def page_url(root, path):
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return DOMAIN + "/" + rel


def target_exists(root, ref):
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    if not ref:
        return True
    p = os.path.join(root, ref.lstrip("/"))
    if ref.endswith("/"):
        return os.path.isfile(os.path.join(p, "index.html"))
    if os.path.isfile(p):
        return True
    # extensionless internal link -> directory index
    return os.path.isfile(os.path.join(p, "index.html"))


def main(root):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(f"technical validator: site root not found: {root}")
        return 2
    errors = []
    titles = {}
    pages = []
    for dirpath, _d, filenames in os.walk(root):
        for name in sorted(filenames):
            if name.endswith(".html"):
                pages.append(os.path.join(dirpath, name))
    for path in sorted(pages):
        rel = os.path.relpath(path, root)
        src = io.open(path, encoding="utf-8", errors="replace").read()
        head = src[: src.find("</head>")] if "</head>" in src else src

        m = re.search(r"<title>(.*?)</title>", head, re.S)
        if not m or not m.group(1).strip():
            errors.append(f"{rel}: missing or empty <title>")
        else:
            titles.setdefault(m.group(1).strip(), []).append(rel)

        if not re.search(r'<meta\s+name="description"\s+content="[^"]+"', head):
            errors.append(f"{rel}: missing meta description")

        m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', head)
        if not m:
            errors.append(f"{rel}: missing canonical")
        elif m.group(1) != page_url(root, path):
            errors.append(f"{rel}: canonical {m.group(1)} != {page_url(root, path)}")

        langs = set(re.findall(r'hreflang="([^"]+)"', head))
        if langs != {"en", "es", "x-default"}:
            errors.append(f"{rel}: hreflang cluster is {sorted(langs)}, expected en/es/x-default")

        m = re.search(r'<html\s+lang="([^"]+)"', src)
        expected_lang = "es" if rel.replace(os.sep, "/").startswith("es/") else "en"
        if not m:
            errors.append(f"{rel}: missing <html lang>")
        elif m.group(1) != expected_lang:
            errors.append(f"{rel}: lang={m.group(1)}, expected {expected_lang}")

        if re.search(r'<meta[^>]+content="[^"]*noindex', head, re.I):
            errors.append(f"{rel}: noindex present")

        for ref in re.findall(r'(?:href|src)="(/[^"]*)"', src):
            if not target_exists(root, ref):
                errors.append(f"{rel}: broken internal reference {ref}")

    for title, where in sorted(titles.items()):
        if len(where) > 1:
            errors.append(f"duplicate title {title!r}: {', '.join(where)}")

    # sitemap two-way check
    sm_path = os.path.join(root, "sitemap.xml")
    if not os.path.isfile(sm_path):
        errors.append("sitemap.xml missing")
    else:
        sm = io.open(sm_path, encoding="utf-8").read()
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sm))
        on_disk = set()
        for path in pages:
            url = page_url(root, path)
            on_disk.add(url)
            if url not in locs:
                errors.append(f"sitemap: page on disk missing from sitemap: {url}")
        for loc in sorted(locs):
            if loc not in on_disk:
                errors.append(f"sitemap: entry with no file on disk: {loc}")

    if errors:
        for e in errors:
            print("ERROR " + e)
        print(f"technical validator: FAIL — {len(errors)} error(s) across {len(pages)} pages")
        return 1
    print(f"technical validator: OK — {len(pages)} pages clean")
    return 0


if __name__ == "__main__":
    default_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "northfwliving")
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default_root))
