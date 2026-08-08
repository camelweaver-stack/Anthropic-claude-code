#!/usr/bin/env python3
"""Add a self-referencing <link rel="canonical"> to any page missing one.

Every page on westfwliving.com is reachable at more than one URL (e.g. both
`/calculator` and `/calculator.html`, and `/` plus `/index.html`). Pages that
already carry a canonical tag point at their `.html` form, which is also the
form listed in sitemap.xml and the hreflang alternates. The 51 pages that were
missing a canonical are what Google reports as "Duplicate without user-selected
canonical". This script gives each of them a self-canonical in that same
`.html` form so every URL signal on the site agrees.

Idempotent: files that already contain rel="canonical" are left untouched.
The canonical line is inserted immediately before the first hreflang
<link rel="alternate"> tag (matching the placement on existing pages), or
before </head> if there is no hreflang block.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://westfwliving.com/"

canonical_re = re.compile(r'rel=["\']canonical["\']', re.I)
hreflang_re = re.compile(r'<link[^>]*rel=["\']alternate["\'][^>]*hreflang', re.I)
head_close_re = re.compile(r'</head>', re.I)

changed, skipped = [], []

for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts:
        continue
    html = path.read_text(encoding="utf-8")
    if canonical_re.search(html):
        skipped.append(path)
        continue

    rel = path.relative_to(ROOT).as_posix()
    canonical = f'<link rel="canonical" href="{BASE}{rel}">\n'

    m = hreflang_re.search(html)
    if m:
        # insert on the line before the first hreflang alternate
        line_start = html.rfind("\n", 0, m.start()) + 1
        new_html = html[:line_start] + canonical + html[line_start:]
    else:
        m = head_close_re.search(html)
        if not m:
            print(f"!! no </head> in {rel}; skipping", file=sys.stderr)
            skipped.append(path)
            continue
        line_start = html.rfind("\n", 0, m.start()) + 1
        new_html = html[:line_start] + canonical + html[line_start:]

    path.write_text(new_html, encoding="utf-8")
    changed.append((rel, f"{BASE}{rel}"))

print(f"Added canonical to {len(changed)} file(s); {len(skipped)} already had one.\n")
for rel, url in changed:
    print(f"  {rel:60s} -> {url}")
