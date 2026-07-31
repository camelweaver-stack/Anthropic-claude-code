# Scheduled Auto-Publish — Setup & Honest Limits

Goal: publish READY_ videos on a schedule with no manual step. The runner is `scripts/publish_queue.mjs` — it
enforces the daily cap (1 full + 2 Shorts) and a weekly cadence (publish-days), so a scheduler can call it
unattended. But scheduling has a hard requirement worth stating plainly.

## The one unavoidable truth

**A scheduled job only runs if a machine is powered on and online at that time**, with (a) the queue files present,
(b) a browser that can reach YouTube, and (c) a logged-in session. There is no way around this:

- The **managed cloud sandbox** (where Claude runs when you use the web/mobile app) **cannot** do it — its proxy
  blocks YouTube and it has none of your files.
- A **cloud VM you rent** technically can, but: iCloud Drive doesn't sync to Linux (you'd have to feed the queue via
  other storage), and Google challenges/logs-out sessions from datacenter IPs, so an unattended uploader there
  **breaks silently and needs periodic manual re-login.** Only choose this if you accept that maintenance.

The reliable path is **your own computer** (the Windows PC you already run book-upload on), which has the queue,
your browser, and your login. It doesn't need to be on 24/7 — see the "missed start" trick below.

---

## Recommended: Windows Task Scheduler (tolerates an off-most-of-the-time PC)

Everything is bundled — you edit two paths and run one installer.

One-time, on the PC:
```bat
cd <path-to-skill>\scripts
npm install & npx playwright install chromium
node setup_auth.mjs            REM log into West FW Living once
```

Then:
1. **Edit the three values** at the top of `scheduled_run.cmd` — your `QUEUE` folder, your `SITE_REPO` checkout, and
   `SITE_URL` (+ optional `INDEXNOW_KEY`). Those are the only machine-specific bits.
2. **Register the task:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File install_schedule.ps1
   ```

`scheduled_run.cmd` runs both halves in order: `publish_queue.mjs` (publish ready videos, capped) then
`process_pending_embed.mjs` (embed the new IDs into the site and deploy). The installer sets
**`-StartWhenAvailable`** ("run as soon as possible after a missed start"), so if the PC was off at 9am the task
fires next boot — that's what makes this work without an always-on machine. Days/time are set in both
`install_schedule.ps1` and the `DAYS` line of `scheduled_run.cmd`; keep them in sync (default Mon/Wed/Fri 9am).

**First real run:** before trusting the schedule, run it once by hand with `--dry-run` and watch it, so you can
calibrate any Studio selector that moved (see `youtube-studio-workflow.md`):
```bat
node publish_queue.mjs --queue "%QUEUE%" --dry-run
```
Test the whole chained task on demand with:  `Start-ScheduledTask -TaskName "West FW Living Auto-Publish"`

---

## macOS alternative (launchd)

If the worker is a Mac instead, use a `launchd` LaunchAgent with `StartCalendarInterval` (fires on next wake if
missed), calling the same `node publish_queue.mjs --queue ... --days mon,wed,fri`. Do `setup_auth.mjs` once first.

---

## What the runner does / doesn't do

- **Does:** scan READY_ folders oldest-first, classify Short (`#Shorts` in title.txt) vs full, enforce per-day caps
  via a `.publish-ledger.json`, publish each through `publish_video.mjs`, drop the `READY_` prefix on success, and
  append results to `publish_queue.log`.
- **Embed-back is now automated too**, via `process_pending_embed.mjs` (run second by `scheduled_run.cmd`). It drains
  `pending_embed.jsonl`, replaces `YOUTUBE_VIDEO_ID` in each twin page (`embed-target.txt` must be set in the kit),
  un-hides the `.video-embed` block, commits + pushes the site repo (Netlify auto-builds; override with `--deploy-cmd`),
  and pings IndexNow if you pass `--indexnow-key`. Processed entries move to `embedded.jsonl`; anything it can't safely
  edit (missing `embed-target.txt`, page not found) is left in `pending_embed.jsonl` and logged to `embed.log` for a
  manual look — it never guesses which page to edit.

---

## Reliability caveats to accept up front

- **Login expiry.** The saved session lasts a while but not forever; when it expires, runs fail with "Not logged in"
  and you rerun `setup_auth.mjs`. The log makes this obvious.
- **Selector drift.** A YouTube Studio redesign can break a selector; the runner logs the failure and leaves that
  folder `READY_` for a retry after you calibrate. It does **not** silently skip — check `publish_queue.log`.
- **Unlock/session on Windows.** Task Scheduler can run whether or not you're logged in, but a *headed* browser needs
  an interactive desktop session. Simplest: run the task in your user session (default) and let it run headed. Only
  move to `--headless` once calibrated and confident.
