# West FW Living — Daily Publishing Runbook

The operating procedure for the daily content cycle on westfwliving.com. One substantial,
useful, factual item per day. Utility over volume: if no topic clears the bar, materially
update an existing page instead. **Never publish filler to hit a quota.**

Bootstrapped 2026-08-16 from the PCS Oahu editorial system, adapted to WFL's publish model.
The master driver lives in Google Drive: *Daily Publishing Driver — PCS Oahu + West FW Living*
(folder "Anastasia RE — Aledo Opportunity Engine").

## Asset facts (single source of truth — do not re-derive these each run)

| Fact | Value |
| --- | --- |
| Site | https://westfwliving.com |
| Repo | github.com/camelweaver-stack/Anthropic-claude-code |
| Working branch | `claude/wfl-daily-publishing-i7lmp9` |
| Netlify project | `anastasiaweaver` |
| **Netlify siteId** | `a975e513-e8b1-46c2-9d31-1f769e103f2c` |
| Publish dir | repository root (`netlify.toml`: `publish = "."`) |
| **IndexNow key** | `f61db218770282944b56755e36b90509` |
| IndexNow keyLocation | https://westfwliving.com/f61db218770282944b56755e36b90509.txt |
| Legacy key (also served) | `ad9df71e17eb3f5d04105f21e8ec56e4` |

Deploy: Netlify deploy-site connector for the siteId above → run the returned
`npx @netlify/mcp …` command from the repo root with `--no-wait`, then poll until
`state=ready`.

## Publish model — read this before editing anything

WFL publishes the **repository root**. There is no separate `site/` directory, and the
298 pages that predate this generator are hand-authored HTML. So the model is hybrid:

- **New pages** are authored in `gen/pages_*.py` using the helpers in `gen/common.py`
  (`page()`, `lead_form()`, `article_ld()`, `faq_ld()`) and written into the tree by
  `gen/build.py`. Never hand-edit a generated page — change the module and rebuild.
- **Every page in the tree**, generated or hand-authored, is then normalized and gated by
  `scripts/apply_standing_fixes.py`. That script is **always the final build step.**

```
python3 gen/build.py                      # render new/updated pages + reciprocal hub links
python3 scripts/apply_standing_fixes.py   # FINAL STEP — normalize, rebuild sitemap, gate
```

`apply_standing_fixes.py` is idempotent: running it twice in a row changes nothing the
second time. It exits nonzero if any gate fails. **No green, no ship.**

### What the final step fixes
- **nav** — the 10-link EN spec (Specials · Best Deals · Neighborhoods · Schools · Buying ·
  Selling · Relocate · Guides · Tools · Español) and the 8-link ES spec, whose last slot is
  the English-mirror link and is preserved per page.
- **canonical** — enforced as the single correct URL form, which is **extensionless** for
  `.html` files (`/specials`, not `/specials.html`) and trailing-slash for directory index
  files. This is not a style choice: Netlify's Pretty URLs post-processing rewrites every
  rendered `<a href="x.html">` to `<a href="x">` on every deploy regardless of source, so
  extensionless is the only form that actually matches what real links resolve to. A
  `.html`-form (or otherwise non-matching) canonical is actively corrected, not left alone —
  see "Netlify platform behavior" below before changing this policy.
- **internal `<a href>` and hreflang `<link>` targets** — canonicalized to the same
  extensionless form as the pages they point to.
- **lead-form date field** — context-aware, see below.
- **sitemap.xml** — derived fresh from the files actually present on disk. The prior sitemap
  is never read; `lastmod` comes from git history. A deleted page cannot survive and a new
  page cannot be missed.

### Lead-form contexts (form-assert)
| Context | Field | EN label | ES label |
| --- | --- | --- | --- |
| Renting-associated | `lease_end` | When does your current lease end? | ¿Cuándo vence tu contrato actual? |
| Selling | `sell_timeline` | (existing seller label preserved) | (existing seller label preserved) |
| Everything else | `move_date` (optional) | When are you planning to move? (optional) | ¿Para cuándo planea mudarse? (opcional) |

**Note on the seller context:** the task spec says "renting-associated pages use `lease_end`;
all others use optional `move_date`." The 26 `sell/` and `es/vender/` pages carry a
purpose-built `sell_timeline` field ("when are you planning to sell?"), which is a strictly
better question for a seller than a move date. It is preserved as a third context rather than
flattened into `move_date`. **Flagged for the operator** — if you want the literal two-context
rule instead, delete `SELL_PREFIXES` / `SELL_FIELD` from `apply_standing_fixes.py` and rerun.

Renting classification is by path prefix + slug token, with an explicit `RENT_SLUGS`
override for renting pages whose slug carries no rent token (e.g. `quiz.html`, the
complex-vs-complex comparison guides). Keep it auditable: add to the list, don't add fuzzy
heuristics.

### Gates
`nav-assert` · `form-assert` · `canonical-assert` · `hreflang-assert` (bidirectional, resolved
by file so all three URL spellings compare equal) · `link-assert` · `sitemap-assert`.

`KNOWN_MISSING` in the script lists dead internal links that are tracked and deliberately not
auto-created, each with a reason. They report as **warnings**, never silently. Any *other* dead
link fails the gate, so a new regression can't hide behind them.

## The daily loop
1. **Review** — `find . -name '*.html' -not -path './.git/*' | wc -l`; skim the calendar.
2. **Maintain** — run `editorial/staleness-scan.md`. If a fix outranks a new page, do the fix.
3. **Select** — read the latest opportunity queue in `reports/seo/` **first** (see
   `docs/SEO_GROWTH_SYSTEM.md`), then the scored backlog in `EDITORIAL_CALENDAR.md`.
   GSC evidence outranks editorial hunch: expand demonstrated winners and push pages
   ranking 6–15 before starting fresh topics. Target mix over any ~2 weeks (tunable in
   `data/seo/config.json → allocation`): 35% expand winners / 30% improve pos-6–20 pages /
   20% new high-intent local / 10% maintain facts / 5% exploratory — publishing is
   subordinate to optimizing existing assets (2026-08-24 rebalance). Run
   `python3 scripts/seo_engine.py reinforce` weekly for the per-page action list; its
   default recommendation is *leave alone* — don't manufacture churn. Any brand-new page must
   pass the seven-question gate in the growth-system doc.
   *Change classes (post-2026-08-24 stability rule):* **Maintenance** (fact corrections,
   rent/concession updates, link fixes, technical repairs, dates updated only on real
   verification) is always allowed. **Optimization** (titles, enrichment, link reinforcement,
   cluster expansion) requires GSC evidence — cite the snapshot in the audit log. **New
   publishing** continues at the current cadence with strategic justification; do not raise
   velocity. The site needs ranking maturation more than surface area: pages at pos 10–30 are
   a live experiment — no wholesale rewrites of pages earning impressions. Keep cluster balance across
   buyers, sellers, renters, relocation, neighborhoods, schools. Never ship two
   near-duplicate pages in a row.
   *When a fresh GSC export arrives:* `python3 scripts/seo_engine.py ingest <zip>` then
   `report`; run `linkaudit` monthly. Log every meaningful SEO change with `log-event`.
4. **Research** — source hierarchy below. Record every source URL + the date verified.
5. **Produce** — author in `gen/pages_*.py`. Every page needs: direct answer up top, west
   Fort Worth corridor context (Willow Park, Hudson Oaks, Weatherford, Aledo, Benbrook, White
   Settlement, the I-30/I-20 split), who it applies to, next steps, inline sources, a
   **visible verified date**, hub-and-spoke links (link the hub **and** add a reciprocal link
   from an existing page — wire it into `RECIPROCAL` in `gen/build.py`), a page-matched CTA,
   and Article/FAQ JSON-LD.
6. **Spanish mirror** — if the page belongs to a cluster that has ES mirrors, build the ES
   twin with bidirectional hreflang and a **humanly visible** cross-language link in the body
   (not breadcrumb-anchored). Verify with a **rendered screenshot**, not grep.
7. **Validate** — re-read every number and date against its source.
8. **Build + gate** — the two commands above. `GATE PASSED` required.
9. **Deploy** — Netlify connector, siteId above, `--no-wait`, poll to `state=ready`.
10. **Verify live** — new URL 200 · a nonexistent path 404 · URL present in
    https://westfwliving.com/sitemap.xml · canonical is the apex URL · for ES mirrors,
    hreflang resolves both directions.
11. **IndexNow** — POST changed URLs to https://api.indexnow.org/indexnow with host
    `westfwliving.com` and the key above.
12. **Record** — append to `editorial/AUDIT_LOG.md`, mark the item LIVE in
    `EDITORIAL_CALENDAR.md`, commit, `git push -u origin claude/wfl-daily-publishing-i7lmp9`
    (retry with backoff). **Do not open a PR** unless asked.

## Voice — publisher mode, not brokerage
WFL is an independent field guide. Full service is "coming soon." Forbidden: agent /
brokerage / leasing / apartment-locating / consultation language, "schedule a showing,"
"work with us," "free home valuation." Email capture only. **No lender placements.** No
crime-rate or "safest neighborhood" claims. EHO + the not-a-brokerage disclaimer on every page.

## Never invent
Prices, rents, concessions, dates, hours, phone numbers, addresses, policies, quotes, reviews.
If a fact can't be confirmed from the hierarchy below, omit it or label it explicitly
(`preliminary` / `proposed` / `reported` / `unconfirmed`).

**Watch for year-conflation.** Local coverage of an annual dataset is easy to mistake for the
current cycle — on 2026-08-16 the top search result for Parker County school ratings was a
2022 article. Always confirm the edition year in the source itself before using a figure.

## Source hierarchy (highest first)
1. Texas state agencies (TEA, Comptroller, TDHCA, TDI, DPS, TxDOT)
2. County + city (Tarrant County, Parker County, Fort Worth, Weatherford, Willow Park,
   Hudson Oaks, Aledo, Benbrook, White Settlement)
3. TEA + individual ISDs (Aledo, Weatherford, Brock, Fort Worth, White Settlement, Springtown)
4. Appraisal districts (Tarrant Appraisal District, Parker County Appraisal District)
5. First-party / official operators (property owners, program administrators)
6. MLS-derived or brokerage-authorized data
7. Reputable local media (Fort Worth Report, Star-Telegram, Weatherford Democrat)
8. Other secondary sources

## Clusters (hub-and-spoke)
Buyers · Sellers · Renters · Relocation · Neighborhoods · Schools · Community · Military/BAH ·
Data & Tools. Every item must strengthen ≥1 cluster and link to its hub.

## Do NOT auto-publish — draft + flag `NEEDS REVIEW` instead
Political advocacy · individualized legal or financial advice · allegations against
identifiable people or businesses · unverified safety/crime claims · crisis/casualty/crime ·
anything touching an active legal dispute · changes to brokerage/licensing/referral/privacy/
terms/consent disclosures · paid or sponsored content · material redesigns · destructive code ·
deleting major pages · domain/DNS/billing/account changes.
For any of these: write the draft, log it `NEEDS REVIEW`, deploy nothing.

## Netlify platform behavior — read before touching internal link forms

**westfwliving.com's canonical URL form for .html pages is extensionless** (`/specials`, not
`/specials.html`). This is enforced by Netlify's Pretty URLs post-processing, which rewrites
every rendered `<a href="x.html">` to `<a href="x">` on **every deploy**, platform-side,
regardless of what the source HTML contains. `scripts/apply_standing_fixes.py`'s `url_for()` /
`canonical_path()` already encode this — don't flip it back to `.html` without re-reading
`editorial/AUDIT_LOG.md`'s 2026-08-18 entry, which documents four burned deploy attempts from
getting this backwards once already.

**Verifying a link/URL-form fix requires checking the deploy itself, not just local disk or
GitHub.** Local content and the committed GitHub branch matching what you intend to ship is
necessary but not sufficient — confirm the fix survived Netlify's post-processing by checking
**the deploy's own permalink** (`https://<deployId>--anastasiaweaver.netlify.app/...`, returned
by `get-deploy-for-site`) immediately after it reaches `state=ready`, before trusting production.
A quick isolation technique if something looks reverted: append a unique HTML comment to a file,
commit, push, deploy, and check whether the comment survived — if it did but a link/href change
in the same file did not, that's Pretty URLs, not a stale-content bug.

## Deploy-failure protocol
Preserve the prior production version. Do not repeatedly force deploys. Diagnose, record the
error in the audit log, leave a clean recovery path, make no destructive changes.
