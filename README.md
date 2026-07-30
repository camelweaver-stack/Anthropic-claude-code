# anastasiaweaver.com

Static marketing site for **Anastasia Weaver** — free apartment locating &
real-estate services in west Fort Worth (Aledo, Willow Park, Hudson Oaks,
Benbrook, Weatherford).

## Structure

Plain HTML/CSS — no build step.

| Path | Page |
| --- | --- |
| `index.html` | Home / apartment locating |
| `second-chance.html` | Second-chance apartments |
| `rent-to-own.html` | Rent-to-own |
| `calculator.html` | Rent math calculator |
| `areas.html` | Areas served |
| `specials.html` | This month's specials |
| `complexes/*.html` | Individual community pages |
| `thanks.html` | Post-contact thank-you |
| `styles.css` | Shared styles |
| `sitemap.xml`, `robots.txt` | SEO |

## Deploying to Netlify

This repo deploys as a static site (see `netlify.toml`; publish dir = repo
root, no build command). Connect the repo to a Netlify site, then set the
custom domain to `anastasiaweaver.com`.
