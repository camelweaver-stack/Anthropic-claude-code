# Embed-Back — Wire the New Video ID Into the Site

Once a video is live on YouTube and you have its ID, the twin page on the West FW Living site needs to show the
player. The rendered pages ship with the embed **pre-built but hidden**, holding a `YOUTUBE_VIDEO_ID` placeholder,
so publishing back is a find-replace plus un-hide plus deploy — no new markup to author.

Do this step **after** the video is published and the pinned comment is posted, so a viewer who follows the site link
lands on a live video, not a placeholder.

---

## Step 1: Find the Twin Page

The page to edit is:
- Whatever path the kit's `embed-target.txt` names, if present. Use it exactly.
- Otherwise, for monthly rent reports, the convention is `rent-report/<month>.html` in the site repo.

If neither resolves cleanly, ask the user which page this video belongs to rather than editing the wrong file.

---

## Step 2: Insert the Video ID

The page contains a `.video-embed` block whose iframe/src carries the literal placeholder `YOUTUBE_VIDEO_ID`, and the
block is hidden with `display:none` until there's a real video. Two edits:

1. **Replace every `YOUTUBE_VIDEO_ID`** in the file with the real ID. There is usually more than one (the iframe src,
   a thumbnail/poster link, a "watch on YouTube" anchor), so replace **all** occurrences, not just the first.
2. **Un-hide the embed** by removing the `display:none` from the `.video-embed` element (inline style or the class
   rule — match how the page does it).

A quick way to see how many replacements you should expect:
```bash
grep -c 'YOUTUBE_VIDEO_ID' <path-to-twin-page.html>   # count before
# after the edit, this should be 0
grep -c 'display:none' <path-to-twin-page.html>        # confirm the .video-embed one is gone
```

After editing, re-grep for `YOUTUBE_VIDEO_ID` and confirm zero matches remain — a leftover placeholder means a broken
embed on a live page.

---

## Step 3: Deploy and Ping IndexNow

1. **Deploy to Netlify.** Use the repo's normal deploy path (a `git push` to the deploy branch if the site
   auto-builds, or the project's deploy command/Netlify build hook — follow whatever the site repo already does; check
   its README or `netlify.toml` if unsure).
2. **Ping IndexNow** so search engines re-crawl the updated page promptly. Use the repo's existing IndexNow submission
   method (a script or endpoint the site already uses) and submit the twin page's URL.

---

## Step 4: Confirm

Report the deployed page URL back to the user alongside the video ID, so they can eyeball the live embed if they want.
If the deploy or IndexNow ping is handled by CI after the push, say so rather than claiming it's done before it is.
