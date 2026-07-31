---
name: video-render
description: >
  Renders a complete West FW Living episode (frames + narration + MP4 + thumbnail) locally and stages it as a
  READY_<slug> folder in the Video Upload Queue, in the exact format the youtube-publish skill consumes. Use this
  skill whenever the user says "render this month's video", "render the September rent report video", "build the
  video for <page>", "make the rent report episode", or otherwise asks to produce a West FW Living video from the
  monthly data. It is the upstream companion to youtube-publish: this builds the kit, that publishes it. Trigger it
  even when the user just says "make this month's episode" without saying "render."
---

# video-render

Produces one West FW Living episode end to end — six branded frames, engineered narration, a 1080p MP4, and a
thumbnail — then stages it as `READY_<slug>/` in the Video Upload Queue for the **youtube-publish** skill to pick up.
Nothing is hand-assembled: three scripts run in order and the kit lands in the queue in the right shape.

## Pipeline (run in this order)

1. **`build_video.py`** → renders `f1.png … f6.png` (1920×1080) and `thumbnail.png` (1280×720). Fonts resolve
   relative to the skill folder with a cross-platform mono fallback, so it runs on Mac/Windows/Linux.
2. **`build_v2.py`** → the proven narration pipeline: sentence-level synthesis with engineered pauses (0.45s within
   thoughts, ~0.7s transitions, 1.2s section landings, ellipses before key numbers), loudness-normalized, then
   assembled with the frames into `<slug>.mp4`. It prints the exact per-frame durations — use them to time the
   CHAPTERS block.
3. **`stage_kit.py`** → writes/validates the kit and moves everything into `<queue>/READY_<slug>/`.

Set `RENDER_SLUG` and run from a clean work dir so intermediates and the MP4 stay together:
```bash
export RENDER_SLUG=west-fw-rent-report-september-2026
python build_video.py && python build_v2.py
# author the four kit text files (below), then:
python stage_kit.py --slug $RENDER_SLUG
```

## One-time setup

1. `pip install piper-tts pillow` and confirm `ffmpeg` is installed.
2. Download the voice once: `python -m piper.download_voices en_US-ryan-high` (build_v2.py uses `en_US-ryan-high`).
   For Spanish `/es/` twins use `es_MX-*` (or best available es_MX/es_ES) and pull the script from the `/es/` page.
3. **Record the queue path** in `queue_path.txt` next to the scripts. This MUST be the same **Google Drive** Video
   Upload Queue that youtube-publish reads (all West FW Living assets live on Google Drive; Drive for desktop mounts
   it locally, e.g. `G:\My Drive\...`). Both skills must point at this one folder. stage_kit.py reads this file when
   `--queue` isn't passed.

## Producing an episode

1. **Get this month's data.** Canonical source is `rent-report/<month>.html` in the site repo: Concession Index,
   per-community offers, 1BR bands, and the effective-rent example. Never re-render a prior script with a new date —
   every episode must carry month-specific numbers.
2. **Adapt the frames** (`build_video.py`) and **the script table** (`build_v2.py`) to the new month's numbers. Keep
   the layout and the pacing architecture; only the content changes.
3. **Run build_video.py then build_v2.py.** Note the printed frame durations.
4. **Author the kit text files** in the work dir — these are what youtube-publish reads, so the names and shapes
   matter (stage_kit.py validates them):

   | File | Contents |
   |------|----------|
   | `title.txt` | One line, exact title. Append ` #Shorts` for a Short. |
   | `description.txt` | **Line 1 = `https://westfwliving.com/tv.html`**. Then a short blurb. Then a `CHAPTERS` block whose first line is `0:00 …`, each chapter on its own line, ≥3 chapters — timed from build_v2.py's printed durations. |
   | `tags.txt` | Comma-separated tags. |
   | `pinned-comment.txt` | The comment youtube-publish will post and pin. |
   | `embed-target.txt` | *(optional)* site page to embed the video into, e.g. `rent-report/september.html`. Include it so the embed-back step knows the twin page. |

5. **Stage it:** `python stage_kit.py --slug <slug>`. It validates (flags a missing tv.html link or a broken CHAPTERS
   block *before* upload), builds `READY_<slug>/`, and moves the MP4, thumbnail, and text files in. Drive sync
   uploads the folder automatically.
6. **Report:** slug, duration, file sizes. The user then says "publish today's video" to hand off to youtube-publish.

## Quality gates (do not skip)

- **Listen-check ~10s of narration** before assembly; fix mispronunciations by respelling phonetically (e.g.
  "west F W living"). piper reads letters better spaced out.
- **Month-specific data every time** — no recycled scripts with a swapped date.
- **Chapters must be real.** YouTube only renders them if the first line is `0:00` and there are ≥3, each on its own
  line. stage_kit.py checks this, but author it right so the check passes.

## Notes on the kit format (why stage_kit.py exists)

youtube-publish reads **separate** `title.txt`, `description.txt`, `tags.txt`, `pinned-comment.txt`, and optional
`embed-target.txt` + `thumbnail.png`. An earlier convention bundled tags/pinned/embed into one file — that silently
breaks the handoff. stage_kit.py is the guardrail: it only ever writes the shape youtube-publish expects, and refuses
to overwrite an existing READY_ folder.
