# Internal Link Graph — pcsoahu.com

Crawl of the **live production site** from `https://pcsoahu.com/`, following rendered `<a href>` links only
(no sitemap seeding). Node identity collapses Netlify's `.html`/extensionless twin forms.

- Pages crawled: **59** of 59 sitemap URLs (pre-fix universe) — **every sitemap URL is reachable from the homepage**
- Internal edges: **2386**
- Orphans (in sitemap, unreachable by links): **0**
- Maximum click depth: **4** (the per-base `/family/*` pages)
- Flagged non-page hrefs: 3 data-file links (`/data/*.json|.csv`) — all verified HTTP 200 live; not defects.

| URL | Depth | Inbound (unique pages) | Example parents |
|---|---|---|---|
| / | 0 | 58 | /ask, /bah-report, /bah-report/2026-edition |
| /ask/ | 1 | 58 | /, /bah-report, /bah-report/2026-edition |
| /bah-report/ | 1 | 58 | /, /ask, /bah-report/2026-edition |
| /bah-report/2026-edition/ | 2 | 1 | /data |
| /bases/ | 1 | 58 | /, /ask, /bah-report |
| /bases/camp-smith.html | 2 | 1 | /bases |
| /bases/coast-guard-honolulu.html | 2 | 1 | /bases |
| /bases/fort-shafter.html | 2 | 1 | /bases |
| /bases/kaneohe-bay.html | 2 | 1 | /bases |
| /bases/pearl-harbor-hickam.html | 2 | 1 | /bases |
| /bases/schofield-wheeler.html | 2 | 1 | /bases |
| /bases/tripler.html | 2 | 1 | /bases |
| /buy/ | 1 | 58 | /, /ask, /bah-report |
| /data/ | 1 | 58 | /, /ask, /bah-report |
| /embed/ | 2 | 3 | /bah-report, /bah-report/2026-edition, /data |
| /family/ | 3 | 4 | /family/childcare, /neighborhoods/downtown, /neighborhoods/kalihi |
| /family/camp-smith/ | 4 | 1 | /family |
| /family/childcare/ | 2 | 19 | /data, /family, /family/camp-smith |
| /family/fort-shafter/ | 4 | 1 | /family |
| /family/kaneohe-bay/ | 4 | 1 | /family |
| /family/pearl-harbor-hickam/ | 4 | 1 | /family |
| /family/schofield-wheeler/ | 4 | 1 | /family |
| /family/spouse-jobs/ | 4 | 7 | /family, /family/camp-smith, /family/fort-shafter |
| /family/tripler/ | 4 | 1 | /family |
| /guides/ | 1 | 58 | /, /ask, /bah-report |
| /guides/childcare.html | 2 | 1 | /guides |
| /guides/dodea-schools.html | 2 | 3 | /guides, /guides/school-transition, /schools |
| /guides/harpta.html | 1 | 58 | /, /ask, /bah-report |
| /guides/healthcare.html | 2 | 2 | /guides, /guides/sponsorship |
| /guides/household-goods.html | 2 | 1 | /guides |
| /guides/on-base-waitlist.html | 2 | 2 | /guides, /on-base |
| /guides/pets-to-hawaii.html | 2 | 3 | /guides, /guides/household-goods, /tla/field-notes |
| /guides/school-transition.html | 1 | 58 | /, /ask, /bah-report |
| /guides/sponsorship.html | 2 | 2 | /guides, /guides/healthcare |
| /guides/spouse-employment.html | 1 | 58 | /, /ask, /bah-report |
| /guides/utilities.html | 2 | 2 | /guides, /tools |
| /my-pcs/ | 1 | 58 | /, /ask, /bah-report |
| /neighborhoods/ | 1 | 58 | /, /ask, /bah-report |
| /neighborhoods/aiea.html | 2 | 11 | /bases/camp-smith, /bases/fort-shafter, /bases/pearl-harbor-hickam |
| /neighborhoods/downtown.html | 2 | 10 | /bases/coast-guard-honolulu, /bases/fort-shafter, /bases/tripler |
| /neighborhoods/ewa.html | 2 | 9 | /bases/pearl-harbor-hickam, /bases/schofield-wheeler, /family/camp-smith |
| /neighborhoods/kailua.html | 2 | 8 | /bases/kaneohe-bay, /family/camp-smith, /family/fort-shafter |
| /neighborhoods/kalihi.html | 2 | 11 | /bases/camp-smith, /bases/coast-guard-honolulu, /bases/fort-shafter |
| /neighborhoods/kaneohe.html | 2 | 8 | /bases/kaneohe-bay, /family/camp-smith, /family/fort-shafter |
| /neighborhoods/mililani.html | 2 | 9 | /bases/pearl-harbor-hickam, /bases/schofield-wheeler, /family/camp-smith |
| /neighborhoods/pearlcity.html | 2 | 10 | /bases/camp-smith, /bases/fort-shafter, /bases/pearl-harbor-hickam |
| /neighborhoods/saltlake.html | 2 | 12 | /bases/camp-smith, /bases/coast-guard-honolulu, /bases/fort-shafter |
| /neighborhoods/wahiawa.html | 2 | 8 | /bases/schofield-wheeler, /family/camp-smith, /family/fort-shafter |
| /neighborhoods/waipahu.html | 2 | 9 | /bases/pearl-harbor-hickam, /bases/schofield-wheeler, /family/camp-smith |
| /on-base/ | 1 | 58 | /, /ask, /bah-report |
| /pcs-checklist/ | 1 | 58 | /, /ask, /bah-report |
| /quiz/ | 1 | 58 | /, /ask, /bah-report |
| /schools/ | 1 | 58 | /, /ask, /bah-report |
| /sell/ | 1 | 58 | /, /ask, /bah-report |
| /tla/ | 1 | 58 | /, /ask, /bah-report |
| /tla/field-notes.html | 1 | 58 | /, /ask, /bah-report |
| /tools/ | 1 | 58 | /, /ask, /bah-report |
| /tools/commute-grid/ | 2 | 19 | /data, /family, /family/camp-smith |
| /vehicle-shipping/ | 1 | 58 | /, /ask, /bah-report |

## Findings

- **No orphan pages.** Everything in the sitemap is link-reachable; nav (11 links) + footer (~20 links) put most pages at depth 1–2.
- **Base pages have exactly one unique inbound page each (the `/bases/` hub) at depth 2.** Not an orphan condition and hub-and-spoke is the site's intended architecture, but this is the weakest layer of the graph relative to the pages' importance. Recommended (not executed — outside this audit's fix authority, which covers 0-inbound orphans only): natural contextual links from each neighborhood page to the base(s) it discusses, and reciprocal links between each `/bases/X.html` page and its `/family/X/` twin.
- **`/family/*` pages sit at depth 4 with 1 inbound each** — reachable but weak; same recommendation as above.
- The two guides restored in this audit re-enter the graph with footer (sitewide), hub-card, and in-body links (depth 1 via footer).
