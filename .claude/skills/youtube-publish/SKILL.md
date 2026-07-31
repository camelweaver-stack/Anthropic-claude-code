---
name: youtube-publish
description: >
  Full-automation skill for publishing West FW Living videos to YouTube Studio. Use this skill whenever the user
  says "publish today's video", "upload the rent report video", "process the video queue", "publish to YouTube",
  "post the Shorts", or any similar request to get a rendered video from the queue onto the West FW Living channel.
  The skill scans the Video Upload Queue for READY_ folders, reads each video's kit files (title, description, tags,
  pinned comment), and drives YouTube Studio through the ENTIRE publish flow with a Playwright browser — including
  the video-file upload, all metadata, thumbnail, playlist, visibility, publish, and the post-publish pinned
  comment — with no human clicks. It then embeds the new video ID back into the twin page on the site and redeploys.
  The only thing the user ever does is log in ONCE (a persistent browser profile reuses that login forever after).
  Trigger this even when the user names a specific video or says "put the April rent report up" without saying
  "YouTube" — this is the path for getting West FW Living videos live.
---

# YouTube Publish Skill

## Overview — how this achieves full automation

Earlier versions of this workflow injected JavaScript into the user's open browser. That approach can never upload
the video file or handle login, because browsers forbid page scripts from touching file pickers or auth. So this
skill drives YouTube Studio with **Playwright** instead, using a **persistent browser profile**. That single change
removes both manual steps:

- **Video/thumbnail upload is automated** — Playwright sets the file input directly (`setInputFiles`), which page
  JavaScript is not allowed to do.
- **Login happens once, ever** — the persistent profile keeps the session, so every future run is hands-off. There
  is no way to safely automate a *cold* Google login (bot-detection will lock the channel), so reusing a real
  logged-in profile is both the correct and the safest design.

The heavy lifting lives in bundled scripts; your job is to orchestrate them, do the site embed-back, enforce the
publish-rate cap, and report results.

- `scripts/publish_video.mjs` — the engine: uploads, fills every field, publishes, posts+pins the comment, prints a JSON result.
- `scripts/setup_auth.mjs` — the one-time login.
- `references/youtube-studio-workflow.md` — the Playwright selector map + calibration guide (read when a run fails on a selector).
- `references/embed-back.md` — putting the video ID back into the site (you do this directly, no browser needed).

---

## One-Time Setup (first use on a machine)

Do this once. If publishing fails later with "Not logged in," the session expired — just rerun step 2.

1. **Install the browser engine** in the scripts folder:
   ```bash
   cd <skill-path>/scripts && npm install && npx playwright install chromium
   ```
2. **Log in once:**
   ```bash
   node setup_auth.mjs
   ```
   A browser opens to YouTube Studio. The user signs into the **West FW Living** brand account (handling 2FA),
   confirms the top-right avatar is that channel, then presses Enter in the terminal. The session is saved to the
   profile dir (`~/.yt-publish-profile` by default) and reused on every publish.

Tell the user this is the *only* time they touch the browser. Everything after is automated.

---

## Step 1: Discover What's Ready

Videos wait in the Video Upload Queue, one folder per video, prefixed `READY_`:

```
Video Upload Queue/READY_<slug>/
```

This lives in the user's **Google Drive** (all West FW Living assets and management are on Google Drive), synced
locally via Drive for desktop — typically under the mounted Drive (e.g. `G:\My Drive\...` on Windows). If you can't
find it, ask the user for the path once and reuse it. Process oldest first if folder names carry date stamps.
Each kit contains:

| File | What it's for |
|------|---------------|
| `<slug>.mp4` | The rendered video (the script uploads this) |
| `title.txt` | Exact title — used verbatim |
| `description.txt` | Full description; first line has the `westfwliving.com/tv.html` link; includes a CHAPTERS block |
| `tags.txt` | Comma-separated tags |
| `pinned-comment.txt` | Comment posted and pinned after publish |
| `thumbnail.png` | Optional custom thumbnail, 1280×720 |
| `embed-target.txt` | Optional — the site page to embed into (see Step 4) |

The script reads these itself; you don't need to pre-parse them. But do glance at `title.txt` and `description.txt`
so your report to the user is accurate.

---

## Step 2: Publish (one command per video)

For each `READY_` folder, within the day's rate cap (see below), run the engine:

```bash
cd <skill-path>/scripts
node publish_video.mjs --kit "<absolute path to READY_ folder>"
```

Useful flags:
- `--dry-run` — fills everything and stops **before** clicking Publish. **Use this on the very first video on a new
  machine** so the user can watch it drive Studio and confirm every field landed, before anything goes live.
- `--headless` — run without a visible window (only once you trust it; headed is the default and is more reliable).
- `--visibility unlisted|private` — override the default `public`.
- `--schedule "2026-08-01T09:00"` — schedule instead of publishing now (for calendar batches).
- `--no-comment` — skip the pinned comment (post it yourself if the script's comment step is mid-calibration).

The script prints one JSON line, e.g.:
```json
{"ok":true,"videoId":"dQw4w9WgXcQ","url":"https://youtu.be/dQw4w9WgXcQ","commentPinned":true}
```
Parse it. On `"ok":false`, read the `error` and look in the kit's `_publish_artifacts/` folder — the script
screenshots each failed step there. Then consult `references/youtube-studio-workflow.md` to fix the selector, and
rerun. **The description's tv.html link and CHAPTERS line-breaks are verified inside the script** (it re-inserts the
description line-by-line if chapters got flattened), so you don't have to check those by hand — but do report if the
JSON carries a warning about them.

---

## Step 3: Confirm the Video Is Right

After a successful publish, spot-check via the returned URL (open the watch page if in doubt):
- Title matches `title.txt`, description shows the tv.html link, and **chapters render** (the timeline is segmented).
- The comment is posted **and pinned** (`commentPinned: true`). If the script reports `commentPinned: false`, the
  YouTube comment UI shifted — post and pin it manually this once and note it in `references/` for next time.

---

## Step 4: Embed the Video Back Into the Site

You do this directly (no browser). Detail in `references/embed-back.md`; the shape:

1. Open the twin page — the path in `embed-target.txt` if present, else `rent-report/<month>-<year>.html` (e.g.
   `rent-report/august-2026.html`). The site is this same repo (camelweaver-stack/Anthropic-claude-code).
2. Replace **every** `YOUTUBE_VIDEO_ID` placeholder with the real ID — there are usually **3** (the iframe `src`
   plus `embedUrl` and `thumbnailUrl` in the JSON-LD `VideoObject` schema) — and remove `display:none` from the
   `.video-embed` div (keep its `margin`) so the player shows.
3. Deploy to Netlify (the repo's normal deploy path) and ping IndexNow so the update gets crawled.
4. Verify no `YOUTUBE_VIDEO_ID` remains (`grep` should return zero).

---

## Step 5: Mark Complete and Report

Rename the folder to drop `READY_` so it isn't picked up again:
```bash
mv "Video Upload Queue/READY_<slug>" "Video Upload Queue/<slug>"
```
Then report per video: the **video ID**, live URL, whether the comment pinned, and that the site embed is deployed.
If you scheduled instead of publishing, say when it goes live.

---

## Rate Discipline — Enforce This, Don't Just Mention It

YouTube reads a sudden flood of uploads from one channel as a spam signature, which can suppress reach or trip a
review. Because the script makes publishing effortless, **you** are the throttle:

- **Max per day: 1 full video + 2 Shorts.** Stop at the cap even if more folders are `READY_`.
- **Standard cadence: 2–3 videos/week.** Spread a backlog across days.
- If the queue exceeds the daily cap, publish up to the cap, then tell the user exactly how many remain and that
  you're stopping to protect the channel — never quietly push the whole backlog through in one run.

**Shorts** use the same kit structure with `#Shorts` appended to the title, and count against the "2 Shorts/day"
side of the cap.

### Unattended / scheduled publishing

For "publish the queue on a schedule" without a person driving each one, use the batch runner
`scripts/publish_queue.mjs` — it scans all `READY_` folders, enforces the caps above via a ledger, classifies
Shorts vs full, publishes each through `publish_video.mjs`, and logs results. A scheduler (Windows Task Scheduler,
cron, or launchd) calls it. **Full setup, and the honest limits, are in `references/scheduling.md`** — read it
before promising a schedule, because a scheduled job only runs when a machine with the queue + a logged-in browser
is powered on (the cloud sandbox behind the web/mobile app cannot do it). The runner leaves the site embed-back to a
follow-up step, writing published IDs to `pending_embed.jsonl` for later processing.

---

## First-Run Calibration — Set Expectations Honestly

YouTube Studio's DOM changes over time, and the selectors in `publish_video.mjs` are centralized (the `SEL` object)
precisely so they're easy to fix. On a brand-new machine, or if YouTube redesigns Studio, the first run may stall on
a selector. That's expected and cheap to handle:

1. Run the first video with `--dry-run` and watch it (headed).
2. If it stalls, the failing step name is in the error and a screenshot is in `_publish_artifacts/`. Open
   `references/youtube-studio-workflow.md`, update the one selector, rerun.
3. Once a dry-run completes cleanly, drop `--dry-run` and publish for real. After that, runs are turnkey.

Frame this to the user as a one-time tune-up, not a limitation — after calibration the whole queue publishes with a
single command per video.

---

## What Still Needs a Human

- **The one-time login** (`setup_auth.mjs`) — a cold automated Google login can't be done safely, so the user signs
  in once and the profile remembers it.
- **Selector calibration** on first use or after a Studio redesign — a quick one-line fix, per above.

Everything else — video upload, thumbnail, title, description, chapters, tags, playlist, audience, language,
category, visibility, publish, and the pinned comment — is fully automated.
