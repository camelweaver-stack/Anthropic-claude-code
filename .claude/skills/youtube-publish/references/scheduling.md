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

One-time, on the PC:
```bat
cd C:\Users\camel\<path-to-skill>\scripts
npm install & npx playwright install chromium
node setup_auth.mjs            REM log into West FW Living once
```

Create the scheduled task (run in an elevated PowerShell; adjust the queue path):
```powershell
$scripts = "C:\Users\camel\<path-to-skill>\scripts"
$queue   = "C:\Users\camel\iCloudDrive\<...>\Video Upload Queue"
$action  = New-ScheduledTaskAction -Execute "node.exe" `
  -Argument "publish_queue.mjs --queue `"$queue`" --days mon,wed,fri" -WorkingDirectory $scripts
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable
Register-ScheduledTask -TaskName "YouTube Auto-Publish" -Action $action -Trigger $trigger -Settings $settings
```

The key flag is **`-StartWhenAvailable`** ("run task as soon as possible after a scheduled start is missed"). If the
PC is off at 9am, the task fires the next time you power on. Combined with `--days mon,wed,fri`, that gives a
2–3/week cadence that survives an intermittently-on machine. `-RunOnlyIfNetworkAvailable` avoids firing offline.

**First real run:** before trusting the schedule, run it once by hand with `--dry-run` and watch it, so you can
calibrate any Studio selector that moved (see `youtube-studio-workflow.md`):
```bat
node publish_queue.mjs --queue "%QUEUE%" --dry-run
```

---

## macOS alternative (launchd)

If the worker is a Mac instead, use a `launchd` LaunchAgent with `StartCalendarInterval` (fires on next wake if
missed), calling the same `node publish_queue.mjs --queue ... --days mon,wed,fri`. Do `setup_auth.mjs` once first.

---

## What the runner does / doesn't do

- **Does:** scan READY_ folders oldest-first, classify Short (`#Shorts` in title.txt) vs full, enforce per-day caps
  via a `.publish-ledger.json`, publish each through `publish_video.mjs`, drop the `READY_` prefix on success, and
  append results to `publish_queue.log`.
- **Doesn't:** the **site embed-back** (Step 4 of SKILL.md) — that needs the site repo checked out + a deploy, which
  is environment-specific. Published IDs + their `embed-target` are written to `pending_embed.jsonl` in the queue so
  the embed-back can be run afterward (e.g., ask Claude "process pending_embed.jsonl" in a session that has the site
  repo). If you want the schedule to embed too, add a follow-up scheduled step that runs your site's deploy against
  that file.

---

## Reliability caveats to accept up front

- **Login expiry.** The saved session lasts a while but not forever; when it expires, runs fail with "Not logged in"
  and you rerun `setup_auth.mjs`. The log makes this obvious.
- **Selector drift.** A YouTube Studio redesign can break a selector; the runner logs the failure and leaves that
  folder `READY_` for a retry after you calibrate. It does **not** silently skip — check `publish_queue.log`.
- **Unlock/session on Windows.** Task Scheduler can run whether or not you're logged in, but a *headed* browser needs
  an interactive desktop session. Simplest: run the task in your user session (default) and let it run headed. Only
  move to `--headless` once calibrated and confident.
