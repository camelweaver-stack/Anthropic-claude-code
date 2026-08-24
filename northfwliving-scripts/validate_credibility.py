#!/usr/bin/env python3
"""Hard credibility gate for northfwliving.com production HTML.

Scans every deployable HTML file for editorial/placeholder content that must
never render publicly: fake first-hand field notes, future-visit placeholders,
editorial instructions, TODO/FIXME copy, insert-markers, and lorem ipsum.

The scan runs against VISIBLE text only (text nodes, <title>, meta
description/keywords, and img alt text) so that legitimate markup such as
`placeholder=` input attributes never trips it. Spanish body copy is handled:
`TODO:`/`FIXME:` match only in uppercase so the common Spanish word "todo:"
does not false-positive.

Exit code 0 = clean. Exit code 1 = violations found (build must fail).

Usage: validate_credibility.py [site_root]   (default: ../northfwliving)
"""
import html
import io
import os
import re
import sys
from html.parser import HTMLParser

# Patterns applied CASE-INSENSITIVELY to visible text.
PATTERNS_CI = [
    r"FIRST-?HAND",
    r"FIELD NOTE:",          # marker form; branded headings like "Latest field notes" are fine
    r"\[FIELD NOTE",
    r"FIELD PHOTO",
    r"added after an in-?person visit",
    r"\[INSERT",
    r"\[ADD PHOTO",
    r"\[TBD",
    r"\bTBD\b",
    r"\bTK\s?TK\b",
    r"lorem ipsum",
    r"PLACEHOLDER",
]

# Patterns applied CASE-SENSITIVELY (uppercase editorial markers only, so
# Spanish "todo:" / "sobre todo:" never false-positives).
PATTERNS_CS = [
    r"\bTODO:",
    r"\bFIXME\b",
    r"\bXXX\b",
]

RX_CI = [re.compile(p, re.IGNORECASE) for p in PATTERNS_CI]
RX_CS = [re.compile(p) for p in PATTERNS_CS]


class VisibleTextExtractor(HTMLParser):
    """Collects visible text plus title/meta-description/alt attribute values."""

    SKIP_TAGS = {"script", "style", "noscript"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.chunks = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        d = dict(attrs)
        if tag == "meta" and d.get("name", "").lower() in ("description", "keywords"):
            self.chunks.append(d.get("content", "") or "")
        if tag == "img":
            self.chunks.append(d.get("alt", "") or "")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth == 0:
            self.chunks.append(data)


def visible_text(html_source):
    p = VisibleTextExtractor()
    p.feed(html_source)
    return "\n".join(p.chunks)


def scan_file(path):
    src = io.open(path, encoding="utf-8", errors="replace").read()
    text = visible_text(src)
    violations = []
    for rx in RX_CI + RX_CS:
        for m in rx.finditer(text):
            ctx = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            violations.append((rx.pattern, ctx.strip()))
    return violations


def main(root):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(f"credibility validator: site root not found: {root}")
        return 2
    total = 0
    files = 0
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in sorted(filenames):
            if not name.endswith(".html"):
                continue
            files += 1
            path = os.path.join(dirpath, name)
            for pattern, ctx in scan_file(path):
                total += 1
                rel = os.path.relpath(path, root)
                print(f"VIOLATION {rel}: /{pattern}/ near: …{ctx}…")
    if total:
        print(f"credibility validator: FAIL — {total} violation(s) across {files} file(s)")
        return 1
    print(f"credibility validator: OK — {files} HTML files clean")
    return 0


if __name__ == "__main__":
    default_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "northfwliving")
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default_root))
