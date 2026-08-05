# CLAUDE_CODE_DEPLOY.md — pcsoahu.com
Executable runbook. Single-package layout: `site/` is the ONLY directory that gets published. `gen/` (generator +
gate), the runbooks, and `indexnow-payload.json` never get published. Do not hand-edit site/
files — content changes go through `gen/` (edit, `python3 gen/build.py`, re-gate).

## 0 · Pre-flight (mandatory)
```bash
python3 gen/gate.py site
```
Must print `GATE PASSED`. If it fails, STOP — do not deploy; report the failures instead.
Sanity: `site/` should contain 47 HTML files, sitemap.xml (45 URLs), robots.txt, llms.txt,
assets/ (style.css, og-card.png, img/ with 11 photos).

## 1 · Deploy
**Primary path — Netlify** (account is connected):
```bash
netlify deploy --prod   # netlify.toml sets publish=site and functions=netlify/functions
```
Then attach the custom domain: `netlify domains:add pcsoahu.com` (or via dashboard), and let
Netlify provision HTTPS. Netlify serves `404.html` for not-found routes automatically —
verify in step 3.

**Fallback — any static host:** upload site/ contents as the document root; set the error
document to `/404.html`; force HTTPS; add a 301 from www → apex (or apex → www, but pick apex:
every canonical in the build is `https://pcsoahu.com`).

## 2 · DNS (registrar side)
Point pcsoahu.com at the host per its instructions (Netlify: apex A/ALIAS + www CNAME).
Confirm propagation before step 3: `curl -sI https://pcsoahu.com | head -5` → HTTP/2 200.

## 3 · Post-deploy verification (all must pass)
```bash
for p in / /bases/ /bases/fort-shafter.html /bah-report/ /buy/ /sell/ /on-base/ /quiz/ \
         /pcs-checklist/ /tools/ /sitemap.xml /robots.txt /llms.txt /assets/og-card.png; do
  echo "$p -> $(curl -s -o /dev/null -w '%{http_code}' https://pcsoahu.com$p)"; done
curl -s -o /dev/null -w '404 route -> %{http_code}\n' https://pcsoahu.com/does-not-exist
```
Expect 200 on every listed path and **404** (not 200, not redirect) on the last line.
Then three in-browser checks: /pcs-checklist/ saves progress after reload; /quiz/ returns three
pockets with reasoning; /tools/ calculators compute. Finally, one canonical spot check:
`curl -s https://pcsoahu.com/buy/ | grep -o '<link rel="canonical"[^>]*>'` → must be the apex URL.

## 4 · Search plumbing (same session)
1. **GSC + Bing:** add the property, verify (Netlify: DNS TXT), submit
   `https://pcsoahu.com/sitemap.xml`.
2. **Priority indexing requests in GSC, in order:** /bah-report/, /sell/, /buy/, then the seven
   /bases/ pages, /on-base/, /quiz/.
3. **IndexNow:**
```bash
KEY=$(openssl rand -hex 16)
echo $KEY > site/$KEY.txt   # redeploy this one file
# then update indexnow-payload.json: replace both REPLACE_WITH_INDEXNOW_KEY with $KEY
curl -s -X POST https://api.indexnow.org/indexnow \
  -H 'Content-Type: application/json' -d @indexnow-payload.json
```
Expect HTTP 200/202. Report the key back to the operator — it's needed for every future refresh.

## 5 · Do NOT do
- Do not submit test entries to the FormSubmit forms — form activation is a human step
  (one deliberate test per tag, listed in the operator's brief) so junk leads never hit the pipeline.
- Do not add analytics, tag managers, or third-party scripts — not in spec.
- Do not edit any HTML. If something looks wrong, stop and report.

## 6 · Report back
Deliver: deploy URL + custom-domain status, the verification table from step 3, sitemap
submission confirmation, IndexNow key + response code, and any anomaly verbatim.
