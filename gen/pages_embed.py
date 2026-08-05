from common import *

def widget():
    """Standalone iframe widget — no site chrome, self-contained inline styles, noindex."""
    rows = "".join(
        f'<div style="display:flex;align-items:baseline;gap:.5rem;padding:.3rem 0;'
        f'border-top:1px dotted #d8dcd9"><span>{v[0]}</span>'
        f'<span style="flex:1;border-bottom:1px dotted #9aa8ae;transform:translateY(-4px)"></span>'
        f'<span style="font-weight:600;white-space:nowrap">{v[1].split(" · ")[0]}</span></div>'
        for v in POCKETS.values())
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oahu BAH vs Rent — PCS Oahu widget</title>
<meta name="description" content="Embeddable Oahu BAH-vs-rent snapshot from the BAH Reality Report.">
<meta name="robots" content="noindex">
<link rel="canonical" href="{DOMAIN}/bah-report/">
</head>
<body style="margin:0;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;
color:#10222e;background:#f7f8f6;padding:14px;line-height:1.5">
<div style="border:2px solid #10222e;border-radius:8px;padding:12px 14px;background:#fff">
<div style="font-weight:700;font-size:15px;letter-spacing:-.01em">Oahu BAH vs. actual rents</div>
<div style="color:#5b6b73;font-size:11px;margin-bottom:6px">One BAH rate covers every Oahu base
(Honolulu County MHA). Anchors, {BAH_YEAR}: E-5 w/dep <b>{BAH["e5_dep"]}</b> ·
range <b>{BAH["floor"]}–{BAH["ceiling"]}</b>. Effective {BAH["effective"]}.</div>
<div style="font-size:12px">{rows}</div>
<div style="color:#5b6b73;font-size:10px;margin-top:8px;border-top:2px solid #10222e;padding-top:6px">
First band shown per pocket; rounded, compiled mid-2026. Last refreshed: {LAST_REFRESHED}.
Full tables, sources &amp; methodology:
<a href="{DOMAIN}/bah-report/?utm_source=embed" style="color:#1f5a54;font-weight:700">
The BAH Reality Report — pcsoahu.com</a>. Equal Housing Opportunity.</div>
</div>
</body>
</html>'''

def embed_page():
    # The caption <a> lives in the HOST page's DOM (outside the iframe) so every embedding
    # site passes pcsoahu.com a real, crawlable backlink. No UTM on it (clean canonical target).
    snippet = html.escape(
        f'<iframe src="{DOMAIN}/embed/bah-widget.html" width="100%" height="620" '
        f'style="border:0;max-width:520px" loading="lazy" '
        f'title="Oahu BAH vs Rent — PCS Oahu"></iframe>\n'
        f'<p style="font-size:.8rem;margin-top:.25rem">Data: '
        f'<a href="{DOMAIN}/bah-report/">The BAH Reality Report — PCS Oahu</a></p>')
    body = f'''
<div class="hero"><div class="wrap">
<p class="eyebrow">For publishers, bloggers, and group admins</p>
<h1>Embed the BAH-vs-rent snapshot</h1>
<p class="lede">A compact, self-updating version of the BAH Reality Report for your site,
newsletter page, or group resources — free to use with the built-in attribution intact. When we
refresh the data, your embed refreshes with it.</p>
</div></div>
<div class="wrap">
<h2>The widget</h2>
<p style="max-width:44rem">Live preview:</p>
<iframe src="/embed/bah-widget.html" width="100%" height="620"
 style="border:1px solid var(--rule);border-radius:8px;max-width:520px" loading="lazy"
 title="Oahu BAH vs Rent — PCS Oahu"></iframe>
<p style="font-size:.85rem;margin-top:.4rem">Data:
  <a href="{DOMAIN}/bah-report/">The BAH Reality Report — PCS Oahu</a></p>
<h2>Copy-paste embed code</h2>
<p style="max-width:44rem"><code style="display:block;background:#fff;border:1px solid var(--rule);
border-radius:6px;padding:1rem;font-size:.85rem;overflow-x:auto;white-space:pre-wrap">{snippet}</code></p>
<h2>Terms, short version</h2>
<p style="max-width:44rem">Use it anywhere audiences find it useful — personal blogs, spouse
groups, unit resource pages, newsrooms. Keep the attribution caption — the
<a href="/bah-report/">The BAH Reality Report — PCS Oahu</a> link beneath the iframe — intact;
don't present the data as your own or strip the refresh date. For charts, custom cuts, or a quote for a story,
the <a href="/bah-report/#cite">citation block</a> on the report has what you need — and we
answer data questions from writers, free.</p>
{lead_form("EMBED", "pcs-renter",
  heading="Publishing for this audience?",
  blurb="Join the list and get the refresh notice before each edition publishes — useful if "
        "your page cites the numbers.")}
</div>'''
    return page("/embed/", "Embed the Oahu BAH-vs-Rent Widget | PCS Oahu",
                "A free embeddable snapshot of the BAH Reality Report for blogs, spouse groups, "
                "and unit resource pages — self-updating with each data refresh.",
                body, "/bah-report/")

def build():
    return {"/embed/bah-widget.html": widget(), "/embed/index.html": embed_page()}
