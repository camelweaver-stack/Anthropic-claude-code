# PCS Oahu — pcsoahu.com

Dedicated Oahu military/PCS publisher site (WFL family, its own brand). Educational content +
email capture only; referral-first lead routing. Static site, no runtime backend.

## Layout
- `site/` — deployable static web root (24 pages incl. 404, `assets/`, `sitemap.xml`,
  `robots.txt`, `llms.txt`). **Do not hand-edit** — it is generated output.
- `gen/` — Python generator (`build.py`) + QA gate (`gate.py`). Content lives here.
- `netlify.toml` — Netlify deploy config (`publish = "site"`).
- `indexnow-payload.json` — IndexNow submission body (key is a placeholder; see deploy runbook).
- `DEPLOY_BRIEF.md` — full operator brief + human checklist.
- `CLAUDE_CODE_DEPLOY.md` — executable deploy runbook.
- `REFRESH_RUNBOOK.md` — gate-enforced data-refresh cadence.
- `PITCH_KIT.md` — BAH Reality Report link-outreach kit (fire in December).

## Build & gate (required before any deploy)
```bash
cd gen && python3 build.py && python3 gate.py   # must print GATE PASSED
```
The committed `site/` is the gate-verified output of the committed `gen/`.

See `CLAUDE_CODE_DEPLOY.md` for the full deploy + search-plumbing runbook and
`DEPLOY_BRIEF.md` for the operator/human checklist.
