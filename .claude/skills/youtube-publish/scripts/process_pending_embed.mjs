#!/usr/bin/env node
/**
 * process_pending_embed.mjs — run the site embed-back for videos published unattended.
 *
 * publish_queue.mjs records each published video in <queue>/pending_embed.jsonl instead of touching
 * the site (the site step needs the repo + a deploy). This script drains that file: for each entry
 * it opens the twin page in the site repo, drops the real video ID in, un-hides the player, then
 * deploys (git push → Netlify by default) and pings IndexNow. Processed entries move to
 * embedded.jsonl so re-runs are safe.
 *
 * Usage:
 *   node process_pending_embed.mjs --queue "<Video Upload Queue>" --repo "<site repo path>" \
 *       --site-url https://westfwliving.com [--indexnow-key <key>] [--deploy-cmd "npx netlify deploy --prod"] \
 *       [--dry-run] [--no-deploy]
 *
 * Defaults: deploy = git add/commit/push in --repo (Netlify auto-builds). Override with --deploy-cmd,
 * or skip with --no-deploy (edits + commit only). Nothing is pushed in --dry-run.
 */

import { readFile, writeFile, appendFile, access } from 'node:fs/promises';
import { join } from 'node:path';
import { spawn } from 'node:child_process';

const A = Object.fromEntries(process.argv.slice(2).flatMap((a, i, arr) =>
  a.startsWith('--') ? [[a.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]] : []));
const QUEUE = req('queue'), REPO = req('repo');
const SITE_URL = A['site-url'] && A['site-url'] !== true ? String(A['site-url']).replace(/\/$/, '') : null;
const INDEXNOW_KEY = A['indexnow-key'] && A['indexnow-key'] !== true ? String(A['indexnow-key']) : null;
const DEPLOY_CMD = A['deploy-cmd'] && A['deploy-cmd'] !== true ? String(A['deploy-cmd']) : null;
const DRY = !!A['dry-run'], NO_DEPLOY = !!A['no-deploy'];

const PENDING = join(QUEUE, 'pending_embed.jsonl');
const EMBEDDED = join(QUEUE, 'embedded.jsonl');
const LOG = join(QUEUE, 'embed.log');

function req(k) { const v = A[k]; if (!v || v === true) { console.error(`Missing --${k}`); process.exit(2); } return String(v); }
async function exists(p) { try { await access(p); return true; } catch { return false; } }
async function log(m) { const l = `${new Date().toISOString()}  ${m}\n`; process.stderr.write(l); await appendFile(LOG, l).catch(() => {}); }
function sh(cmd, args, cwd) {
  return new Promise((res) => { const c = spawn(cmd, args, { cwd, shell: process.platform === 'win32' }); let o = '', e = '';
    c.stdout.on('data', d => o += d); c.stderr.on('data', d => e += d); c.on('close', code => res({ code, out: o, err: e })); });
}

/** Put the video id into the twin page and un-hide the .video-embed block. Returns {changed, target, url, warn}. */
async function embedInto(entry) {
  const { videoId, embedTarget } = entry;
  if (!videoId) return { changed: false, warn: 'no videoId' };
  if (!embedTarget) return { changed: false, warn: `no embed-target for ${entry.folder} — set embed-target.txt in the kit; skipping (won't guess)` };
  const file = join(REPO, embedTarget);
  if (!(await exists(file))) return { changed: false, warn: `twin page not found: ${embedTarget}` };

  let html = await readFile(file, 'utf8');
  const before = (html.match(/YOUTUBE_VIDEO_ID/g) || []).length;
  html = html.replaceAll('YOUTUBE_VIDEO_ID', videoId);
  // un-hide: strip display:none on any segment that also mentions video-embed (inline style or CSS rule)
  html = html.replace(/([^\n{]*video-embed[^\n{]*?)display\s*:\s*none\s*;?/gi, '$1');
  html = html.replace(/(\.video-embed\s*\{[^}]*?)display\s*:\s*none\s*;?/gi, '$1');

  const leftoverId = (html.match(/YOUTUBE_VIDEO_ID/g) || []).length;
  const stillHidden = /video-embed[^\n{]*display\s*:\s*none|\.video-embed\s*\{[^}]*display\s*:\s*none/i.test(html);
  let warn = null;
  if (leftoverId) warn = `${leftoverId} YOUTUBE_VIDEO_ID placeholder(s) still present after replace`;
  if (stillHidden) warn = (warn ? warn + '; ' : '') + 'a .video-embed display:none may remain — eyeball the page';

  if (!DRY) await writeFile(file, html);
  return { changed: before > 0, target: embedTarget, url: SITE_URL ? `${SITE_URL}/${embedTarget.replace(/^\/?/, '')}` : null, warn, replaced: before };
}

async function deploy(changedTargets) {
  if (NO_DEPLOY) { await log('Skipping deploy (--no-deploy).'); return; }
  if (DRY) { await log('[dry-run] would deploy after edits.'); return; }
  if (DEPLOY_CMD) {
    await log(`Deploy: ${DEPLOY_CMD}`);
    const [cmd, ...rest] = DEPLOY_CMD.split(' ');
    const r = await sh(cmd, rest, REPO);
    await log(r.code === 0 ? 'Deploy command OK.' : `Deploy command exit ${r.code}: ${r.err.slice(-300)}`);
    return;
  }
  // default: git commit + push (Netlify auto-build)
  await sh('git', ['add', '-A'], REPO);
  const msg = `Embed published video(s): ${changedTargets.join(', ')}`;
  const c = await sh('git', ['commit', '-m', msg], REPO);
  if (c.code !== 0 && !/nothing to commit/i.test(c.out + c.err)) { await log(`git commit issue: ${(c.err || c.out).slice(-200)}`); }
  const p = await sh('git', ['push'], REPO);
  await log(p.code === 0 ? 'git push OK (Netlify will build).' : `git push exit ${p.code}: ${p.err.slice(-300)}`);
}

async function pingIndexNow(urls) {
  if (!urls.length) return;
  if (!INDEXNOW_KEY || !SITE_URL) { await log('IndexNow skipped (need --indexnow-key and --site-url).'); return; }
  if (DRY) { await log(`[dry-run] would ping IndexNow for ${urls.length} url(s).`); return; }
  const host = SITE_URL.replace(/^https?:\/\//, '');
  try {
    const resp = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ host, key: INDEXNOW_KEY, keyLocation: `${SITE_URL}/${INDEXNOW_KEY}.txt`, urlList: urls }),
    });
    await log(`IndexNow: HTTP ${resp.status} for ${urls.length} url(s).`);
  } catch (e) { await log(`IndexNow ping failed: ${e.message}`); }
}

(async () => {
  if (!(await exists(PENDING))) { await log('No pending_embed.jsonl — nothing to embed.'); return; }
  const lines = (await readFile(PENDING, 'utf8')).split('\n').filter(Boolean);
  if (!lines.length) { await log('pending_embed.jsonl is empty.'); return; }
  await log(`Processing ${lines.length} pending embed(s).${DRY ? ' [DRY-RUN]' : ''}`);

  const stillPending = [], doneTargets = [], doneUrls = [];
  for (const line of lines) {
    let entry; try { entry = JSON.parse(line); } catch { await log(`bad line skipped: ${line.slice(0, 80)}`); continue; }
    const r = await embedInto(entry);
    if (r.warn) await log(`  ! ${entry.videoId || '?'}: ${r.warn}`);
    if (r.changed && !r.warn) {
      await log(`  ✓ ${entry.videoId} → ${r.target} (${r.replaced} id refs)`);
      doneTargets.push(r.target); if (r.url) doneUrls.push(r.url);
      if (!DRY) await appendFile(EMBEDDED, JSON.stringify({ ...entry, embeddedAt: new Date().toISOString() }) + '\n');
    } else {
      stillPending.push(line); // keep it for a retry / manual fix
    }
  }

  if (doneTargets.length) { await deploy(doneTargets); await pingIndexNow(doneUrls); }
  if (!DRY) await writeFile(PENDING, stillPending.length ? stillPending.join('\n') + '\n' : '');
  await log(`Done. Embedded ${doneTargets.length}, left pending ${stillPending.length}.`);
})().catch(async e => { await log(`FATAL: ${e.stack || e.message}`); process.exit(1); });
