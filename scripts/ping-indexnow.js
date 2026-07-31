#!/usr/bin/env node
/*
 * IndexNow auto-ping — runs as the Netlify build command on every deploy.
 *
 * Reads the freshly-built sitemap.xml and submits every URL to IndexNow
 * (Bing, Yandex, and other participating engines). The IndexNow key file
 * lives at the site root (/<key>.txt) and is validated asynchronously by
 * IndexNow after submission.
 *
 * Safety: this must NEVER fail a deploy. Every error is caught and logged;
 * the netlify.toml command is also guarded with `|| true`.
 */
const fs = require('fs');

const KEY = 'f61db218770282944b56755e36b90509';
const HOST = 'westfwliving.com';
const ENDPOINT = 'https://api.indexnow.org/indexnow';

(async () => {
  try {
    const xml = fs.readFileSync('sitemap.xml', 'utf8');
    const urls = [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map((m) => m[1]);
    if (urls.length === 0) {
      console.log('[indexnow] sitemap.xml has no <loc> URLs — skipping ping');
      return;
    }
    // Hard timeout so a slow/unreachable IndexNow endpoint can never hang the build.
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
          host: HOST,
          key: KEY,
          keyLocation: `https://${HOST}/${KEY}.txt`,
          urlList: urls,
        }),
        signal: controller.signal,
      });
      console.log(`[indexnow] submitted ${urls.length} URLs -> HTTP ${res.status}`);
    } finally {
      clearTimeout(timer);
    }
  } catch (err) {
    console.log(`[indexnow] ping skipped (non-fatal): ${err && err.message}`);
  }
})();
