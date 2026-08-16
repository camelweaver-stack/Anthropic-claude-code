#!/usr/bin/env python3
"""West FW Living — standing fixes + release gates. THE FINAL BUILD STEP.

Run after `python3 gen/build.py`, from anywhere:

    python3 scripts/apply_standing_fixes.py [--check]

Idempotent: running it twice in a row makes no changes the second time. It
normalizes every page in the tree (generated and hand-authored alike), rebuilds
the sitemap from the files actually present, and then runs the release gates.
Exits nonzero if any gate fails — no green, no ship.

  FIXES   nav (10-link EN spec / 8-link ES spec) · canonical · context-aware
          lead-form date field · sitemap derived fresh from disk
  GATES   nav-assert · form-assert · canonical-assert · hreflang-assert ·
          internal-link-assert · sitemap-assert · cleartext-endpoint-assert

--check runs the gates without writing anything.
"""
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

DOMAIN = "https://westfwliving.com"
CHECK_ONLY = "--check" in sys.argv

# Pages deliberately excluded from the sitemap (noindex via netlify.toml headers).
NOINDEX = {"thanks.html", "es/gracias.html"}

# ---------------------------------------------------------------- nav specs
NAV_EN_LINKS = [
    ("/specials", "Specials"), ("/deals", "Best Deals"),
    ("/neighborhoods/", "Neighborhoods"), ("/schools/", "Schools"),
    ("/buy/", "Buying"), ("/sell/", "Selling"), ("/relocate/", "Relocate"),
    ("/guides/", "Guides"), ("/tools/", "Tools"),
]
NAV_EN = "".join(f"<a href='{h}'>{t}</a>" for h, t in NAV_EN_LINKS) + \
         "<a href='/es/' style='font-weight:600'>Español</a>"
NAV_EN_COUNT = 10

NAV_ES_LINKS = [
    ("/es/", "Inicio"), ("/es/comprar/", "Comprar"), ("/es/vender/", "Vender"),
    ("/es/especiales", "Especiales"), ("/es/segunda-oportunidad", "Segunda Oportunidad"),
    ("/es/relocate/", "Mudanza"), ("/es/calculadora", "Calculadora"),
]
NAV_ES_HEAD = "".join(f"<a href='{h}'>{t}</a>" for h, t in NAV_ES_LINKS)
NAV_ES_COUNT = 8

# ---------------------------------------------------------------- form spec
LABEL_LEASE_EN = "When does your current lease end?"
LABEL_MOVE_EN = "When are you planning to move? (optional)"
LABEL_LEASE_ES = "¿Cuándo vence tu contrato actual?"
LABEL_MOVE_ES = "¿Para cuándo planea mudarse? (opcional)"
PH_LEASE_EN, PH_MOVE_EN = "e.g., November 2026", "e.g., spring 2027"
PH_LEASE_ES, PH_MOVE_ES = "ej., noviembre 2026", "ej., primavera 2027"

# A page is renting-associated if its path starts with one of these prefixes or
# its slug contains one of these tokens. Everything else gets the optional
# move_date field. Deliberately explicit so the classification is auditable.
RENT_PREFIXES = (
    "rentals/", "complexes/", "commutes/", "verify/", "tools/",
    "second-chance", "rent-to-own", "specials", "deals", "for-leasing-teams",
    "rent-report/", "military/",
    "es/especiales", "es/segunda-oportunidad", "es/semanas-gratis",
    "es/romper-contrato", "es/renta", "es/complejos",
)
# Renting-associated pages whose slug carries no rent token of its own.
RENT_SLUGS = (
    "quiz.html",                                             # the rent-or-buy quiz
    "guides/olympus-willow-park-vs-olympus-hudson-oaks.html",  # complex-vs-complex
)
RENT_TOKENS = (
    "rent", "lease", "apartment", "renter", "tenant", "deposit", "sublet",
    "landlord", "second-chance", "specials", "concession", "eviction",
    "renta", "inquilino", "contrato", "apartamento", "deposito", "subarriendo",
    "arriendo", "desalojo", "propietario",
)
# Slugs that contain a rent token but are decidedly not renting-side pages.
RENT_EXCLUDE = (
    "rent-vs-buy", "renta-o-compra", "rent-or-buy", "rent-to-own-programs",
    "whats-my-home-worth", "sell", "vender",
)

# Selling pages carry a purpose-built seller field (sell_timeline, "when are you
# planning to sell?") that predates this script and is a better question for a
# seller than a move date. It is preserved as a third context rather than being
# flattened into move_date; see editorial/DAILY_RUN.md.
SELL_PREFIXES = ("sell/", "es/vender/")
SELL_FIELD = "sell_timeline"

# Dead internal links that are KNOWN, TRACKED, and deliberately not auto-created.
# Creating these pages would publish a privacy/consent disclosure, which is a
# safeguarded category under editorial/DAILY_RUN.md — drafted and flagged
# NEEDS REVIEW for a human instead. Reported as warnings, never silently ignored.
KNOWN_MISSING = {
    "/privacy/": "NEEDS REVIEW — privacy disclosure is a safeguarded category; "
                 "linked from every lead-form consent checkbox. Draft awaiting human review.",
    "/es/privacidad/": "NEEDS REVIEW — Spanish mirror of the same privacy disclosure.",
}

FIXED = []
FAILS = []
WARNINGS = []


def note(msg):
    FIXED.append(msg)


def fail(msg):
    FAILS.append(msg)


def html_files():
    out = []
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "gen")]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, fn), ".").replace(os.sep, "/"))
    return sorted(out)


def url_for(rel):
    """Site-absolute URL path for a file, matching the site's existing convention:
    index.html -> directory URL with trailing slash; everything else keeps .html."""
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def is_es(rel):
    return rel == "es/index.html" or rel.startswith("es/")


def is_renting(rel):
    slug = rel.lower()
    if slug in RENT_SLUGS:
        return True
    if any(x in slug for x in RENT_EXCLUDE):
        return False
    if slug.startswith(RENT_PREFIXES):
        return True
    return any(t in slug for t in RENT_TOKENS)


def is_selling(rel, doc=""):
    return rel.lower().startswith(SELL_PREFIXES) or f'name="{SELL_FIELD}"' in doc


def context_for(rel, doc):
    """Which date field this page's lead form must carry: the site's three contexts."""
    if is_selling(rel, doc):
        return SELL_FIELD
    return "lease_end" if is_renting(rel) else "move_date"


def canonical_path(doc, rel):
    """The page's declared canonical path, if it validly resolves to this file.

    The site uses three equivalent apex spellings (/x.html, /x, and /dir/ for
    index files) and the existing sitemap matches whatever each page declares.
    We accept any spelling that maps back to this file rather than rewriting 24
    live canonicals into a different form.
    """
    m = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    if not m:
        return None
    got = m.group(1)
    if not got.startswith(DOMAIN):
        return None
    path = got[len(DOMAIN):] or "/"
    default = url_for(rel)
    accepted = {default}
    if default.endswith(".html"):
        accepted.add(default[:-5])
    if path in accepted:
        return path
    return None


# ---------------------------------------------------------------- fixes
def fix_nav(doc, rel):
    m = re.search(r"<nav>(.*?)</nav>", doc, re.S)
    if not m:
        return doc
    if is_es(rel):
        # Preserve this page's existing English-mirror target; default to the EN home.
        cur = re.findall(r"<a href='([^']+)'[^>]*>English</a>", m.group(1))
        en_target = cur[0] if cur else "/"
        want = NAV_ES_HEAD + f"<a href='{en_target}' style='font-weight:600'>English</a>"
    else:
        want = NAV_EN
    if m.group(1) == want:
        return doc
    note(f"nav       {rel}")
    return doc[: m.start()] + "<nav>" + want + "</nav>" + doc[m.end():]


def fix_canonical(doc, rel):
    want = f'<link rel="canonical" href="{DOMAIN}{url_for(rel)}">'
    m = re.search(r'<link rel="canonical"[^>]*>', doc)
    if m:
        # Only correct a canonical that does not resolve to this file; an existing
        # valid apex spelling is left exactly as-is (see canonical_path).
        if canonical_path(doc, rel) is not None:
            return doc
        note(f"canonical {rel} (corrected — did not resolve to this file)")
        return doc[: m.start()] + want + doc[m.end():]
    # Insert before the first hreflang alternate, else before </head>.
    alt = re.search(r'<link rel="alternate"', doc)
    anchor = alt.start() if alt else doc.find("</head>")
    if anchor == -1:
        fail(f"{rel}: no </head> — cannot insert canonical")
        return doc
    note(f"canonical {rel} (added)")
    return doc[:anchor] + want + "\n" + doc[anchor:]


DATE_FIELD_RE = re.compile(
    r'<label for="([^"]*)">([^<]*)</label>\s*'
    r'<input id="\1" name="(move_date|lease_end|sell_timeline)"([^>]*)>')

CONSENT_ANCHOR = '<label class="aw-consent"'


def wanted_field(rel, doc):
    """(name, label, placeholder) this page's date field must use."""
    ctx = context_for(rel, doc)
    es = is_es(rel)
    if ctx == SELL_FIELD:
        return None  # selling pages keep their existing seller field verbatim
    if ctx == "lease_end":
        return ("lease_end", LABEL_LEASE_ES if es else LABEL_LEASE_EN,
                PH_LEASE_ES if es else PH_LEASE_EN)
    return ("move_date", LABEL_MOVE_ES if es else LABEL_MOVE_EN,
            PH_MOVE_ES if es else PH_MOVE_EN)


def fix_form_field(doc, rel):
    if 'class="lead"' not in doc:
        return doc
    want = wanted_field(rel, doc)
    if want is None:
        return doc
    name, label, ph = want

    changed = [False]

    def repl(m):
        fid, cur_label, cur_name, _rest = m.groups()
        if cur_name == SELL_FIELD:
            return m.group(0)
        if cur_label == label and cur_name == name:
            return m.group(0)
        changed[0] = True
        return (f'<label for="{fid}">{label}</label>'
                f'<input id="{fid}" name="{name}" placeholder="{ph}">')

    new = DATE_FIELD_RE.sub(repl, doc)
    if changed[0]:
        note(f"form      {rel} -> {name} (normalized)")
        return new

    # No date field at all: insert one just above the consent checkbox in each form.
    if not DATE_FIELD_RE.search(new) and CONSENT_ANCHOR in new:
        fid = "sfdate"
        field = (f'<label for="{fid}">{label}</label>'
                 f'<input id="{fid}" name="{name}" placeholder="{ph}">\n      ')
        new = new.replace(CONSENT_ANCHOR, field + CONSENT_ANCHOR)
        note(f"form      {rel} -> {name} (inserted, was missing)")
    return new


def git_lastmod():
    """Last commit date per tracked file, from a single git pass."""
    out = {}
    try:
        raw = subprocess.run(
            ["git", "log", "--pretty=format:C%cd", "--date=short", "--name-only"],
            capture_output=True, text=True, check=True, timeout=120).stdout
    except Exception:
        return out
    cur = None
    for line in raw.splitlines():
        if line.startswith("C") and len(line) == 11 and line[5] == "-":
            cur = line[1:]
        elif line.strip() and cur:
            out.setdefault(line.strip(), cur)
    return out


def build_sitemap(files, docs):
    """Derive the sitemap fresh from the files actually present on disk.

    The prior sitemap is never read: the URL set is enumerated from the tree,
    each URL is the page's own declared canonical, and lastmod comes from git
    history. A deleted page cannot survive and a new page cannot be missed.
    """
    lastmod = git_lastmod()
    today = date.today().isoformat()
    rows = []
    for rel in files:
        if rel in NOINDEX:
            continue
        url = canonical_path(docs[rel], rel) or url_for(rel)
        rows.append((url, lastmod.get(rel, today)))
    rows.sort()
    body = "\n".join(
        f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{lm}</lastmod></url>" for u, lm in rows)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n"), [u for u, _ in rows]


# ---------------------------------------------------------------- gates
def gate_nav(doc, rel):
    m = re.search(r"<nav>(.*?)</nav>", doc, re.S)
    if not m:
        fail(f"{rel}: nav-assert — no <nav> block")
        return
    inner = m.group(1)
    n = len(re.findall(r"<a ", inner))
    want_n = NAV_ES_COUNT if is_es(rel) else NAV_EN_COUNT
    if n != want_n:
        fail(f"{rel}: nav-assert — {n} links, expected {want_n}")
        return
    if not is_es(rel):
        for href, text in NAV_EN_LINKS:
            if f"<a href='{href}'>{text}</a>" not in inner:
                fail(f"{rel}: nav-assert — missing nav link {text} ({href})")
        if "Español" not in inner:
            fail(f"{rel}: nav-assert — missing Español link")


def gate_form(doc, rel):
    if 'class="lead"' not in doc:
        return
    if "formsubmit.co/leads@" in doc:
        fail(f"{rel}: form-assert — cleartext FormSubmit endpoint present")
    if 'name="_honey"' not in doc:
        fail(f"{rel}: form-assert — missing honeypot")
    if 'name="consent"' not in doc:
        fail(f"{rel}: form-assert — missing consent checkbox")

    found = DATE_FIELD_RE.findall(doc)
    if not found:
        fail(f"{rel}: form-assert — lead form has no date field "
             "(move_date / lease_end / sell_timeline)")
        return

    want = wanted_field(rel, doc)
    if want is None:
        # Selling context: assert the seller field is the one present.
        for _fid, _label, name, _rest in found:
            if name != SELL_FIELD:
                fail(f"{rel}: form-assert — selling page carries {name}, expected {SELL_FIELD}")
        return

    want_name, want_label, _ph = want
    for _fid, label, name, _rest in found:
        if name != want_name:
            fail(f"{rel}: form-assert — field is {name}, expected {want_name} "
                 f"({'renting-associated' if is_renting(rel) else 'non-renting'} page)")
        elif label != want_label:
            fail(f"{rel}: form-assert — label {label!r}, expected {want_label!r}")


def gate_canonical(doc, rel):
    if not re.search(r'<link rel="canonical" href="([^"]+)"', doc):
        fail(f"{rel}: canonical-assert — missing canonical")
        return
    if canonical_path(doc, rel) is None:
        got = re.search(r'<link rel="canonical" href="([^"]+)"', doc).group(1)
        fail(f"{rel}: canonical-assert — {got} is not an apex URL resolving to {rel}")


def resolve(url):
    """Map a site-absolute URL to the file that serves it, or None.

    Netlify serves /x.html, /x and /dir/ interchangeably, and the site uses all
    three spellings, so resolution is by file rather than by string.
    """
    path = url.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return "index.html" if os.path.isfile("index.html") else None
    p = path.lstrip("/")
    for cand in (p, p + ".html", p.rstrip("/") + "/index.html", p.rstrip("/") + ".html"):
        if cand and os.path.isfile(cand):
            return cand.replace(os.sep, "/")
    return None


def gate_hreflang(docs):
    """Every declared alternate must exist and point back (bidirectional)."""
    alts = {}
    for rel, doc in docs.items():
        targets = set()
        for _lang, href in re.findall(
                r'<link rel="alternate" hreflang="(en|es)" href="([^"]+)"', doc):
            tgt = resolve(href.replace(DOMAIN, ""))
            if tgt is None:
                fail(f"{rel}: hreflang-assert — alternate {href} does not resolve to a page")
            else:
                targets.add(tgt)
        if targets:
            alts[rel] = targets
    for rel, targets in alts.items():
        for tgt in targets:
            if tgt == rel:
                continue
            if tgt not in alts:
                fail(f"{rel}: hreflang-assert — {tgt} declares no hreflang back")
            elif rel not in alts[tgt]:
                fail(f"{rel}: hreflang-assert — {tgt} does not point back to {rel}")


def gate_links(docs):
    """Every internal href must resolve to a file on disk.

    KNOWN_MISSING targets are reported as warnings rather than gate failures:
    they are tracked, flagged gaps (see editorial/AUDIT_LOG.md), and each one
    names why it cannot simply be created. Any *other* dead link fails the gate,
    so a new regression can never slip through behind them.
    """
    missing = {}
    for rel, doc in docs.items():
        for href in re.findall(r"href=[\"'](/[^\"']*)[\"']", doc):
            if resolve(href) is None:
                missing.setdefault(href.split("#")[0], set()).add(rel)
    for href, srcs in sorted(missing.items()):
        msg = (f"{href} does not resolve ({len(srcs)} page(s), "
               f"e.g. {sorted(srcs)[0]})")
        if href in KNOWN_MISSING:
            WARNINGS.append(f"link-assert (known) — {msg} — {KNOWN_MISSING[href]}")
        else:
            fail(f"link-assert — {msg}")


# ---------------------------------------------------------------- main
def main():
    files = html_files()
    docs = {}

    for rel in files:
        with open(rel, encoding="utf-8") as fh:
            orig = fh.read()
        doc = orig
        if not CHECK_ONLY:
            doc = fix_nav(doc, rel)
            doc = fix_canonical(doc, rel)
            doc = fix_form_field(doc, rel)
            if doc != orig:
                with open(rel, "w", encoding="utf-8") as fh:
                    fh.write(doc)
        docs[rel] = doc

    sitemap, present_urls = build_sitemap(files, docs)
    if not CHECK_ONLY:
        prior = ""
        if os.path.exists("sitemap.xml"):
            with open("sitemap.xml", encoding="utf-8") as fh:
                prior = fh.read()
        if prior != sitemap:
            with open("sitemap.xml", "w", encoding="utf-8") as fh:
                fh.write(sitemap)
            note(f"sitemap   rebuilt from disk ({len(present_urls)} URLs)")

    for rel, doc in docs.items():
        gate_nav(doc, rel)
        gate_form(doc, rel)
        gate_canonical(doc, rel)
    gate_hreflang(docs)
    gate_links(docs)

    # sitemap-assert: parity between the indexable file set and the derived sitemap.
    expect = {canonical_path(docs[r], r) or url_for(r) for r in files if r not in NOINDEX}
    if expect != set(present_urls):
        fail(f"sitemap-assert — parity mismatch: {expect ^ set(present_urls)}")
    if len(present_urls) != len(set(present_urls)):
        fail("sitemap-assert — duplicate URLs in derived sitemap")

    if FIXED:
        print(f"Standing fixes applied ({len(FIXED)}):")
        for f in FIXED[:60]:
            print("  " + f)
        if len(FIXED) > 60:
            print(f"  … and {len(FIXED) - 60} more")
    else:
        print("Standing fixes: nothing to change (idempotent no-op).")

    if WARNINGS:
        print(f"\nWarnings ({len(WARNINGS)}) — tracked, non-blocking:")
        for w in WARNINGS:
            print("  ! " + w)

    print(f"\nPages: {len(files)} · sitemap URLs: {len(present_urls)}")
    if FAILS:
        print(f"\nGATE FAILED — {len(FAILS)} problem(s):")
        for f in FAILS[:80]:
            print("  ✗ " + f)
        if len(FAILS) > 80:
            print(f"  … and {len(FAILS) - 80} more")
        return 1
    print("\nGATE PASSED — nav-assert, form-assert, canonical-assert, "
          "hreflang-assert, link-assert, sitemap-assert all green.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
