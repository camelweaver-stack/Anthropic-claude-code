#!/usr/bin/env node
/**
 * publish_queue.mjs — scheduled, rate-capped batch runner for the youtube-publish skill.
 *
 * Scans the Video Upload Queue for READY_ folders and publishes them via publish_video.mjs,
 * enforcing the daily cap (1 full video + 2 Shorts) and a weekly cadence (publish-days filter),
 * so a scheduler (Windows Task Scheduler / cron / launchd) can run this unattended without
 * tripping YouTube's spam signature. Keeps a ledger so re-runs on the same day don't exceed the
 * cap or double-publish.
 *
 * Usage (typically from a scheduled task):
 *   node publish_queue.mjs --queue "G:\\My Drive\\West FW Living\\Video Upload Queue" \
 *       [--days mon,wed,fri] [--max-full 1] [--max-shorts 2] [--dry-run] [--headless]
 *
 * A Short is detected by "#Shorts" in title.txt (case-insensitive). Everything else is a full video.
 * Results (and any failures needing attention) are appended to <queue>/publish_queue.log.
 * Published video IDs + their embed target are written to <queue>/pending_embed.jsonl so the site
 * embed-back step can be done afterward (that step needs the site repo + deploy, so it's not run here).
 */

import { readdir, readFile, writeFile, appendFile, rename, access, stat } from 'node:fs/promises';
import { join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';
import { spawn } from 'node:child_process';

const HERE = dirname(fileURLToPath(import.meta.url));

// ------- args -------
const A = Object.fromEntries(process.argv.slice(2).flatMap((a, i, arr) =>
  a.startsWith('--') ? [[a.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]] : []));
const QUEUE = A.queue && A.queue !== true ? A.queue : null;
if (!QUEUE) { console.error('Missing --queue "<path to Video Upload Queue>"'); process.exit(2); }
const PROFILE = A.profile && A.profile !== true ? A.profile : join(homedir(), '.yt-publish-profile');
const MAX_FULL = Number(A['max-full'] ?? 1);
const MAX_SHORTS = Number(A['max-shorts'] ?? 2);
const DRY = !!A['dry-run'];
const HEADLESS = !!A.headless;
const DAYS = A.days && A.days !== true ? String(A.days).toLowerCase().split(',').map(s => s.trim()) : null;

const LEDGER = join(QUEUE, '.publish-ledger.json');
const LOG = join(QUEUE, 'publish_queue.log');
const EMBED = join(QUEUE, 'pending_embed.jsonl');

const DOW = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
async function exists(p) { try { await access(p); return true; } catch { return false; } }
function today() { return new Date().toISOString().slice(0, 10); } // YYYY-MM-DD (local-ish; fine for a daily cap)
async function logline(msg) {
  const line = `${new Date().toISOString()}  ${msg}\n`;
  process.stderr.write(line);
  await appendFile(LOG, line).catch(() => {});
}

async function loadLedger() {
  if (!(await exists(LEDGER))) return {};
  try { return JSON.parse(await readFile(LEDGER, 'utf8')); } catch { return {}; }
}
async function saveLedger(l) { await writeFile(LEDGER, JSON.stringify(l, null, 2)).catch(() => {}); }

// Run publish_video.mjs for one folder; resolve its parsed JSON result.
function publishOne(kitPath, isShort) {
  return new Promise((resolve) => {
    const args = ['publish_video.mjs', '--kit', kitPath, '--profile', PROFILE];
    if (DRY) args.push('--dry-run');
    if (HEADLESS) args.push('--headless');
    const child = spawn(process.execPath, args, { cwd: HERE });
    let out = '', err = '';
    child.stdout.on('data', d => out += d);
    child.stderr.on('data', d => err += d);
    child.on('close', () => {
      let result = null;
      const lastJson = out.trim().split('\n').filter(Boolean).pop();
      try { result = JSON.parse(lastJson); } catch { result = { ok: false, error: `unparseable output: ${out.slice(-200)}` }; }
      resolve({ ...result, _isShort: isShort, _stderrTail: err.split('\n').slice(-4).join(' | ') });
    });
  });
}

(async () => {
  // Cadence gate
  const dow = DOW[new Date().getDay()];
  if (DAYS && !DAYS.includes(dow)) {
    await logline(`Not a publish day (today=${dow}, allowed=${DAYS.join(',')}). Nothing to do.`);
    return;
  }

  if (!(await exists(QUEUE))) { await logline(`Queue not found: ${QUEUE}`); process.exit(1); }

  // Today's counts from the ledger
  const ledger = await loadLedger();
  const day = today();
  ledger[day] = ledger[day] || { full: 0, shorts: 0, published: [] };
  let { full, shorts } = ledger[day];

  if (full >= MAX_FULL && shorts >= MAX_SHORTS) {
    await logline(`Daily cap already met (full ${full}/${MAX_FULL}, shorts ${shorts}/${MAX_SHORTS}). Stopping.`);
    return;
  }

  // Find READY_ folders, oldest first
  const entries = [];
  for (const name of await readdir(QUEUE)) {
    if (!name.startsWith('READY_')) continue;
    const p = join(QUEUE, name);
    if (!(await stat(p)).isDirectory()) continue;
    entries.push({ name, path: p });
  }
  // sort by embedded date stamp if present, else by name
  entries.sort((a, b) => a.name.localeCompare(b.name));

  if (!entries.length) { await logline('No READY_ folders in queue.'); return; }

  await logline(`Found ${entries.length} READY_ folder(s). Day caps remaining: full ${MAX_FULL - full}, shorts ${MAX_SHORTS - shorts}.${DRY ? ' [DRY-RUN]' : ''}`);

  for (const e of entries) {
    // classify short vs full
    let isShort = false;
    const titlePath = join(e.path, 'title.txt');
    if (await exists(titlePath)) isShort = /#shorts/i.test(await readFile(titlePath, 'utf8'));

    if (isShort && shorts >= MAX_SHORTS) { await logline(`Skip (shorts cap): ${e.name}`); continue; }
    if (!isShort && full >= MAX_FULL) { await logline(`Skip (full cap): ${e.name}`); continue; }

    await logline(`Publishing ${isShort ? 'SHORT' : 'FULL'}: ${e.name}`);
    const r = await publishOne(e.path, isShort);

    if (r.ok && !r.dryRun) {
      if (isShort) shorts++; else full++;
      ledger[day].full = full; ledger[day].shorts = shorts;
      ledger[day].published.push({ folder: e.name, videoId: r.videoId, url: r.url, commentPinned: r.commentPinned });
      await saveLedger(ledger);
      // record for the site embed-back step (done separately — needs the repo + deploy)
      const embedTarget = (await exists(join(e.path, 'embed-target.txt')))
        ? (await readFile(join(e.path, 'embed-target.txt'), 'utf8')).trim() : null;
      await appendFile(EMBED, JSON.stringify({ videoId: r.videoId, url: r.url, embedTarget, folder: e.name, date: day }) + '\n').catch(() => {});
      // mark complete: drop READY_
      const done = join(QUEUE, e.name.replace(/^READY_/, ''));
      await rename(e.path, done).catch(err => logline(`  (could not rename ${e.name}: ${err.message})`));
      await logline(`  ✓ ${r.videoId}  ${r.url}  pinned=${r.commentPinned}  → renamed, embed pending`);
    } else if (r.ok && r.dryRun) {
      await logline(`  ✓ DRY-RUN filled OK (not published): ${e.name}`);
    } else {
      await logline(`  ✗ FAILED: ${e.name} — ${r.error}. See ${join(e.path, '_publish_artifacts')}. stderr: ${r._stderrTail}`);
      // don't rename; leave it READY_ for a retry / manual look. Continue to next.
    }

    if (full >= MAX_FULL && shorts >= MAX_SHORTS) { await logline('Daily cap reached. Stopping.'); break; }
  }

  const p = ledger[day].published.filter(x => x.videoId);
  await logline(`Done. Published today: ${p.length} (full ${full}/${MAX_FULL}, shorts ${shorts}/${MAX_SHORTS}). ${p.length ? 'Embed-back still pending for: ' + p.map(x => x.videoId).join(', ') : ''}`);
})().catch(async e => { await logline(`FATAL: ${e.stack || e.message}`); process.exit(1); });
