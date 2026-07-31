# YouTube Studio — Playwright Selector & Calibration Map

**Studio URL**: `https://studio.youtube.com`
**Channel**: West FW Living (brand account)

This file is the calibration surface for `scripts/publish_video.mjs`. The script drives Studio with Playwright and
keeps every brittle selector in one `SEL` object at the top of the file. When a run fails on a step, its error names
the step and drops a screenshot in the kit's `_publish_artifacts/`. Come here, find that step below, fix the
selector in the script's `SEL`, and rerun. This is the least stable part of the skill by nature — YouTube ships DOM
changes — so treat it as living and update it as you go.

> Why Playwright and not page-injected JavaScript: Studio is built on Polymer/web-components with lots of
> **shadow DOM**, and — more importantly — the two things that matter most (uploading the video file and staying
> logged in) are simply impossible from in-page scripts. Playwright pierces shadow DOM automatically for its
> locators and can set file inputs directly, which is the whole reason this skill can be hands-off.

---

## Full Click-Path (what the script automates)

1. Confirm session (persistent profile → already logged in as West FW Living)
2. Create → Upload videos
3. **Set the MP4 on the file input** (`setInputFiles` — no OS picker)
4. Details: title, description (+ chapter/link verify), thumbnail, playlist, audience, tags, language, category
5. Wait for processing (Publish/Done enables after ~1–3 min — the script polls, never refreshes)
6. Checks (copyright flag on original content is a false positive — advance past)
7. Visibility → Public (or scheduled) → Done/Publish
8. Read video ID from the share link
9. Watch page → post comment → pin

---

## Selector Reference (maps to the `SEL` object)

Studio selectors drift; these are current-as-of-authoring starting points. Prefer **role/label/text** locators when
a raw CSS selector breaks, because they survive redesigns better.

| Step | `SEL` key | Current selector / robust fallback |
|------|-----------|-------------------------------------|
| Open create menu | `createButton` | `#create-icon` · fallback: `page.getByRole('button', {name:/create/i})` |
| Upload menu item | `uploadMenuItem` | `tp-yt-paper-item:has-text("Upload videos")` · fallback: `getByText(/upload videos/i)` |
| Video file input | `fileInput` | `input[type="file"]` (first one in the upload dialog) |
| Title box | `titleBox` | `#title-textarea #textbox` · it's a contenteditable, not an `<input>` |
| Description box | `descBox` | `#description-textarea #textbox` · also contenteditable |
| Thumbnail input | `thumbnailInput` | `ytcp-thumbnails-compact-editor input[type="file"]` |
| Not made for kids | `notMadeForKids` | `tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]` |
| Show more | `showMore` | `#toggle-button` · fallback: `getByText(/show more/i)` |
| Tags input | `tagsInput` | `input#text-input[aria-label*="Tags" i]` |
| Next (wizard) | `nextButton` | `#next-button` |
| Public radio | `publicRadio` | `tp-yt-paper-radio-button[name="PUBLIC"]` |
| Schedule radio | `scheduleRadio` | `tp-yt-paper-radio-button[name="SCHEDULE"]` |
| Done / Publish | `doneButton` | `#done-button` |
| Share URL | `shareUrl` | `a[href*="youtu.be/"]` in the post-upload dialog |

**How to find a broken selector fast:** run `node publish_video.mjs --kit <folder> --dry-run` headed, let it stall,
open the screenshot in `_publish_artifacts/`, then in a devtools console on that page inspect the element and grab a
stable attribute (`name`, `aria-label`, `id`, visible text). Update the one `SEL` entry. Favor `getByRole`,
`getByLabel`, `getByText` in the script over deep CSS — they're far more durable.

---

## Step Notes & Known Snags

**Contenteditable fields (title/description).** These aren't inputs — you can't `.fill()` them cleanly. The script
clicks, selects-all, deletes, then types. If text ends up doubled or prepended, the select-all/delete didn't land;
add a small wait before typing.

**Description is the fragile field.** Studio can collapse blank lines on entry, which breaks the CHAPTERS block —
YouTube only renders chapters if the first timestamp is `0:00` on its own line, each chapter on its own line, ≥3
chapters. The script reads the description back, counts chapter lines against the kit, and if they were flattened it
re-enters the description line-by-line pressing Enter between lines. It also confirms the `westfwliving.com/tv.html`
link survived. If you still see a flattened block in the artifact screenshot, the re-entry path needs the field's
own key handling — check the `descBox` selector is hitting the real editable, not a wrapper.

**Processing gate.** Publish/Done stays disabled until upload processing clears (~1–3 min). The script waits on the
button becoming enabled (up to 5 min) and never refreshes — refreshing can restart the upload.

**Copyright checks.** The Checks step may flag a copyright match. West FW Living videos are 100% original frames +
synthesized narration, so it's a false positive; the script advances past it. If Studio ever *blocks* rather than
warns, that's a real change — stop and tell the user.

**Playlist / language / category dropdowns.** Their option text varies and they open as overlays. The script ticks
"Rent Reports" (creating it once if missing) via role/text locators; language and category are left as light-touch
because their option lists change — set them during calibration and pin the selectors here if they prove stable.

**Comment + pin (most fragile).** This happens on `youtube.com/watch` (not Studio) in the same logged-in context, so
it posts as the channel — required for pinning. The comment box is `#contenteditable-root`; the action menu → Pin is
a `ytd-menu-renderer`. YouTube reshuffles this UI often; if `commentPinned` comes back false, do it by hand once and
update the `postAndPin` selectors.

**Headless vs headed.** Default is headed — YouTube is more cooperative and you can watch calibration. Only switch to
`--headless` once a machine is dialed in.
