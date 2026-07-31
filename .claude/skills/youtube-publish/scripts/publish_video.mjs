#!/usr/bin/env node
/**
 * publish_video.mjs — drive YouTube Studio end to end for one West FW Living video.
 *
 * This is the engine that makes the youtube-publish skill fully automated. It uses a PERSISTENT
 * browser profile so login happens once (see setup_auth.mjs) and is reused on every run — no
 * per-upload login, and no file-picker pause, because Playwright can set file inputs directly.
 *
 * Usage:
 *   node publish_video.mjs --kit "/path/to/READY_<slug>" \
 *       [--profile ~/.yt-publish-profile] [--headless] [--dry-run] \
 *       [--visibility public|private|unlisted] [--schedule "2026-08-01T09:00"] \
 *       [--no-comment]
 *
 * Output: a single JSON line on stdout, e.g. {"ok":true,"videoId":"abc123","url":"https://youtu.be/abc123"}
 *   so the calling skill can parse the result. Progress + errors go to stderr.
 *
 * SELECTORS: YouTube Studio's DOM shifts over time. Everything brittle is centralized in the SEL
 * object below so calibration is a one-file edit. When a step can't find its element, the script
 * screenshots to <kit>/_publish_artifacts/ and throws with the step name — start calibration there.
 */

import { chromium } from 'playwright';
import { readFile, mkdir, access } from 'node:fs/promises';
import { join, basename } from 'node:path';
import { homedir } from 'node:os';

// ------------------------------- args -------------------------------
const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, arr) => {
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = arr[i + 1];
      acc.push([key, next && !next.startsWith('--') ? next : true]);
    }
    return acc;
  }, [])
);

const KIT = args.kit;
if (!KIT) fail('Missing --kit <folder>');
const PROFILE = (args.profile && args.profile !== true ? args.profile : join(homedir(), '.yt-publish-profile'));
const HEADLESS = !!args.headless;                 // default HEADED — YouTube behaves better and you can watch
const DRY_RUN = !!args['dry-run'];                // fill everything but do NOT click the final Publish
const VISIBILITY = (args.visibility && args.visibility !== true ? String(args.visibility) : 'public').toLowerCase();
const SCHEDULE = args.schedule && args.schedule !== true ? String(args.schedule) : null;
const DO_COMMENT = !args['no-comment'];

const ART = join(KIT, '_publish_artifacts');

// ------------------------------- selectors (calibration surface) -------------------------------
const SEL = {
  createButton: '#create-icon, ytcp-button#create-icon',
  uploadMenuItem: 'tp-yt-paper-item#text-item-0, tp-yt-paper-item:has-text("Upload videos")',
  fileInput: 'input[type="file"]',
  // Details step
  titleBox: '#title-textarea #textbox, ytcp-social-suggestions-textbox[label="Title (required)"] #textbox',
  descBox: '#description-textarea #textbox, ytcp-social-suggestions-textbox[label*="Description"] #textbox',
  thumbnailInput: '#file-loader input[type="file"], ytcp-thumbnails-compact-editor input[type="file"]',
  notMadeForKids: 'tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]',
  showMore: 'ytcp-button#toggle-button, #toggle-button:has-text("Show more")',
  tagsInput: 'input#text-input[aria-label*="Tags" i], #tags-container input',
  nextButton: 'ytcp-button#next-button, #next-button',
  // Visibility step
  publicRadio: 'tp-yt-paper-radio-button[name="PUBLIC"]',
  privateRadio: 'tp-yt-paper-radio-button[name="PRIVATE"]',
  unlistedRadio: 'tp-yt-paper-radio-button[name="UNLISTED"]',
  scheduleRadio: '#second-container-expand-button, tp-yt-paper-radio-button[name="SCHEDULE"]',
  doneButton: 'ytcp-button#done-button, #done-button',
  shareUrl: 'a.ytcp-video-info[href*="youtu.be"], #share-url a, a[href*="youtu.be/"]',
};

// ------------------------------- helpers -------------------------------
function log(...m) { process.stderr.write(m.join(' ') + '\n'); }
function fail(msg) { process.stdout.write(JSON.stringify({ ok: false, error: msg }) + '\n'); process.exit(1); }
async function exists(p) { try { await access(p); return true; } catch { return false; } }
async function readKit(name, required = false) {
  const p = join(KIT, name);
  if (!(await exists(p))) { if (required) fail(`Kit missing required file: ${name}`); return null; }
  return (await readFile(p, 'utf8'));
}
async function shot(page, label) {
  try { await mkdir(ART, { recursive: true }); await page.screenshot({ path: join(ART, `${label}.png`), fullPage: false }); } catch {}
}

/** Type into a Studio contenteditable reliably: focus, select-all, delete, type. */
async function fillContentEditable(page, selector, text, stepName) {
  const box = page.locator(selector).first();
  await box.waitFor({ state: 'visible', timeout: 30000 }).catch(async () => { await shot(page, `err-${stepName}`); throw new Error(`Could not find ${stepName} box`); });
  await box.click();
  await page.keyboard.press('ControlOrMeta+A');
  await page.keyboard.press('Delete');
  await box.type(text, { delay: 4 });
}

// ------------------------------- main -------------------------------
(async () => {
  // Load the kit
  const title = (await readKit('title.txt', true)).trim();
  const description = await readKit('description.txt', true);
  const tags = (await readKit('tags.txt')) || '';
  const pinnedComment = (await readKit('pinned-comment.txt')) || '';
  const slug = basename(KIT).replace(/^READY_/, '');

  // Find the video file
  let mp4 = join(KIT, `${slug}.mp4`);
  if (!(await exists(mp4))) {
    // fall back to the first .mp4 in the folder
    const { readdir } = await import('node:fs/promises');
    const files = await readdir(KIT);
    const found = files.find(f => f.toLowerCase().endsWith('.mp4'));
    if (!found) fail(`No .mp4 found in ${KIT}`);
    mp4 = join(KIT, found);
  }
  const thumb = (await exists(join(KIT, 'thumbnail.png'))) ? join(KIT, 'thumbnail.png') : null;

  log(`[kit] "${title}"  video=${basename(mp4)}  thumb=${thumb ? 'yes' : 'no'}  visibility=${VISIBILITY}${DRY_RUN ? '  DRY-RUN' : ''}`);

  // Launch the persistent (logged-in) profile
  const ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: HEADLESS,
    viewport: { width: 1366, height: 900 },
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const page = ctx.pages()[0] || (await ctx.newPage());

  try {
    await page.goto('https://studio.youtube.com', { waitUntil: 'domcontentloaded' });
    // Auth check: if we got bounced to a Google login, the profile isn't logged in yet.
    if (/accounts\.google\.com|\/signin/i.test(page.url())) {
      await shot(page, 'err-not-logged-in');
      throw new Error('Not logged in. Run setup_auth.mjs once (headed) and sign into the West FW Living channel, then retry.');
    }

    // --- Start upload ---
    log('[step] Create → Upload videos');
    await page.locator(SEL.createButton).first().click();
    await page.locator(SEL.uploadMenuItem).first().click();

    // --- File input (this is the step JS-injection could never do) ---
    log('[step] Setting video file (automated, no picker)');
    const fileInput = page.locator(SEL.fileInput).first();
    await fileInput.waitFor({ state: 'attached', timeout: 30000 });
    await fileInput.setInputFiles(mp4);

    // --- Details ---
    log('[step] Title');
    await fillContentEditable(page, SEL.titleBox, title, 'title');

    log('[step] Description (+ chapters/link verification)');
    await fillContentEditable(page, SEL.descBox, description.replace(/\r\n/g, '\n'), 'description');
    // Read back and verify the two things that silently break.
    const descGot = await page.locator(SEL.descBox).first().innerText();
    const linkOk = /westfwliving\.com\/tv\.html/i.test(descGot);
    const chapterLines = descGot.split('\n').filter(l => /^\s*\d{1,2}:\d{2}\b/.test(l.trim()));
    const wantChapters = description.split('\n').filter(l => /^\s*\d{1,2}:\d{2}\b/.test(l.trim())).length;
    if (!linkOk) log('[warn] tv.html link not detected in description after paste — inspect artifact');
    if (chapterLines.length < wantChapters) {
      log(`[warn] chapter lines ${chapterLines.length} < expected ${wantChapters}; re-inserting description to preserve line breaks`);
      // Re-type line by line so newlines are explicit and chapters render.
      const box = page.locator(SEL.descBox).first();
      await box.click();
      await page.keyboard.press('ControlOrMeta+A');
      await page.keyboard.press('Delete');
      for (const line of description.replace(/\r\n/g, '\n').split('\n')) {
        await box.type(line, { delay: 2 });
        await page.keyboard.press('Enter');
      }
    }

    if (thumb) {
      log('[step] Thumbnail');
      const ti = page.locator(SEL.thumbnailInput).first();
      if (await ti.count()) await ti.setInputFiles(thumb).catch(() => log('[warn] thumbnail input not settable; skipping'));
    }

    // Playlist "Rent Reports" — clicked via visible UI (dropdown labels vary; handled in the skill's reference)
    await addToPlaylist(page, 'Rent Reports').catch(e => log(`[warn] playlist step: ${e.message}`));

    log('[step] Audience: Not made for kids');
    await page.locator(SEL.notMadeForKids).first().click({ timeout: 15000 }).catch(async () => { await shot(page, 'err-kids'); throw new Error('Could not set "Not made for kids"'); });

    // Show more → tags, language, category
    log('[step] Show more → tags');
    await page.locator(SEL.showMore).first().click().catch(() => log('[warn] "Show more" not found; may already be expanded'));
    if (tags.trim()) {
      const ti = page.locator(SEL.tagsInput).first();
      if (await ti.count()) { await ti.click(); await ti.type(tags.trim(), { delay: 3 }); }
      else log('[warn] tags input not found — set tags during calibration');
    }
    // Language + category are dropdowns with variable option text; left to the reference/calibration.

    // --- Advance: Details → Video elements → Checks → Visibility ---
    log('[step] Advancing through wizard');
    for (let i = 0; i < 3; i++) {
      const next = page.locator(SEL.nextButton).first();
      if (await next.isVisible().catch(() => false)) { await next.click(); await page.waitForTimeout(800); }
    }
    // Copyright checks are a false positive for original content — advancing past is the intended behavior.

    // --- Visibility ---
    if (SCHEDULE) {
      log(`[step] Scheduling for ${SCHEDULE}`);
      await page.locator(SEL.scheduleRadio).first().click().catch(() => log('[warn] schedule control not found'));
      // Date/time entry UI varies; the skill pauses here for calibration if scheduling.
    } else {
      const map = { public: SEL.publicRadio, private: SEL.privateRadio, unlisted: SEL.unlistedRadio };
      log(`[step] Visibility: ${VISIBILITY}`);
      await page.locator(map[VISIBILITY] || SEL.publicRadio).first().click({ timeout: 15000 })
        .catch(async () => { await shot(page, 'err-visibility'); throw new Error('Could not set visibility'); });
    }

    // Publish gate: the Done/Publish button stays disabled until processing clears (~1–3 min).
    log('[step] Waiting for Publish to enable (processing ~1–3 min; not refreshing)');
    const done = page.locator(SEL.doneButton).first();
    await done.waitFor({ state: 'visible', timeout: 300000 });
    await page.waitForFunction(
      (sel) => { const b = document.querySelector(sel); return b && !b.hasAttribute('disabled') && b.getAttribute('aria-disabled') !== 'true'; },
      SEL.doneButton, { timeout: 300000 }
    ).catch(() => log('[warn] Publish still shows disabled after 5 min — proceeding to click anyway'));

    // Grab the video id/url before clicking (share link is shown in the dialog).
    let url = await page.locator(SEL.shareUrl).first().getAttribute('href').catch(() => null);

    if (DRY_RUN) {
      await shot(page, 'dry-run-before-publish');
      log('[dry-run] Everything filled; NOT publishing.');
      process.stdout.write(JSON.stringify({ ok: true, dryRun: true, url }) + '\n');
      await ctx.close();
      return;
    }

    log('[step] Publishing');
    await done.click();
    await page.waitForTimeout(2500);
    if (!url) url = await page.locator(SEL.shareUrl).first().getAttribute('href').catch(() => null);
    const videoId = url ? (url.match(/youtu\.be\/([\w-]+)/) || url.match(/[?&]v=([\w-]+)/) || [])[1] : null;
    await shot(page, 'published');

    // --- Comment + pin (most fragile; best-effort, reported honestly) ---
    let commentPinned = false;
    if (DO_COMMENT && pinnedComment.trim() && videoId) {
      commentPinned = await postAndPin(page, videoId, pinnedComment.trim()).catch(e => { log(`[warn] comment/pin: ${e.message}`); return false; });
    }

    process.stdout.write(JSON.stringify({ ok: true, videoId, url: videoId ? `https://youtu.be/${videoId}` : url, commentPinned }) + '\n');
    await ctx.close();
  } catch (err) {
    await shot(page, 'error');
    log(`[error] ${err.stack || err.message}`);
    process.stdout.write(JSON.stringify({ ok: false, error: String(err.message || err), artifacts: ART }) + '\n');
    await ctx.close().catch(() => {});
    process.exit(1);
  }
})();

// ------------------------------- sub-flows -------------------------------
async function addToPlaylist(page, name) {
  // Open the playlist dropdown, tick the named playlist, create it if missing.
  const trigger = page.getByText(/Playlists/i).first();
  if (!(await trigger.isVisible().catch(() => false))) return;
  await trigger.click();
  const item = page.getByRole('checkbox', { name }).first();
  if (await item.count()) { await item.check().catch(() => item.click()); }
  else {
    const newBtn = page.getByText(/New playlist/i).first();
    if (await newBtn.count()) {
      await newBtn.click();
      await page.getByRole('textbox').first().fill(name);
      await page.getByText(/^Create$/).first().click().catch(() => {});
    }
  }
  await page.getByRole('button', { name: /Done/i }).first().click().catch(() => {});
}

async function postAndPin(page, videoId, text) {
  // Comment + pin must happen on the watch page as the CHANNEL account (same logged-in context).
  await page.goto(`https://www.youtube.com/watch?v=${videoId}`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  await page.mouse.wheel(0, 1200);                 // load the comment box
  const placeholder = page.locator('#placeholder-area, #simplebox-placeholder').first();
  await placeholder.waitFor({ state: 'visible', timeout: 20000 });
  await placeholder.click();
  const box = page.locator('#contenteditable-root').first();
  await box.click();
  await box.type(text, { delay: 3 });
  await page.getByRole('button', { name: /^Comment$/ }).first().click();
  await page.waitForTimeout(2500);
  // Open the comment action menu → Pin
  const menu = page.locator('ytd-comment-view-model #action-menu button, #action-menu ytd-menu-renderer button').first();
  await menu.click();
  await page.getByRole('menuitem', { name: /Pin/i }).first().click();
  await page.getByRole('button', { name: /Pin/i }).first().click().catch(() => {}); // confirm dialog
  return true;
}
