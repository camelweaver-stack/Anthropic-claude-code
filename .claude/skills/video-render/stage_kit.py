#!/usr/bin/env python3
"""
stage_kit.py — assemble a READY_<slug>/ folder in the exact shape the youtube-publish skill consumes,
then move it into the Video Upload Queue. Run after build_video.py + build_v2.py.

Why this exists: youtube-publish reads SEPARATE files — title.txt, description.txt, tags.txt,
pinned-comment.txt, and (optional) embed-target.txt + thumbnail.png. Producing one combined
"tags-pinned-embed.txt" (an earlier convention) would silently break the handoff. This script
validates the kit against what youtube-publish actually expects, so a bad kit is caught here, not
at upload time.

Usage:
  python stage_kit.py --slug west-fw-rent-report-august-2026 [--workdir .] [--queue "<path>"] [--copy]

--queue defaults to the path recorded in queue_path.txt next to this script (see SKILL.md setup).
--copy leaves originals in place (default is move). The MP4 and thumbnail are expected in --workdir
as <slug>.mp4 and thumbnail.png (that's where the build scripts put them).

Author the four text files in --workdir before running (Claude writes these each month):
  title.txt            one line, exact video title (append " #Shorts" for a Short)
  description.txt       first line = https://westfwliving.com/tv.html ; then blurb ; then a CHAPTERS
                        block whose first line is "0:00 ..." with each chapter on its own line
  tags.txt              comma-separated tags
  pinned-comment.txt    the comment to pin after publish
  embed-target.txt      (optional) site page to embed into, e.g. rent-report/august.html
"""
import argparse, os, shutil, sys, re

REQUIRED_TEXT = ["title.txt", "description.txt", "tags.txt", "pinned-comment.txt"]
OPTIONAL = ["embed-target.txt", "thumbnail.png"]

def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr); sys.exit(1)

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--workdir", default=os.getcwd())
    ap.add_argument("--queue", default=None)
    ap.add_argument("--copy", action="store_true")
    args = ap.parse_args()

    wd = os.path.abspath(args.workdir)
    slug = args.slug

    # Resolve the queue path
    queue = args.queue
    if not queue:
        qp = os.path.join(here, "queue_path.txt")
        if os.path.exists(qp):
            queue = open(qp, encoding="utf-8").read().strip()
    if not queue:
        die("No queue path. Pass --queue or create queue_path.txt (see SKILL.md one-time setup).")
    if not os.path.isdir(queue):
        die(f"Queue folder not found: {queue}")

    mp4 = os.path.join(wd, f"{slug}.mp4")

    # ---- validate everything BEFORE touching the queue ----
    missing = [f for f in REQUIRED_TEXT if not os.path.exists(os.path.join(wd, f))]
    if not os.path.exists(mp4):
        missing.append(f"{slug}.mp4")
    if missing:
        die("Missing required kit file(s) in workdir: " + ", ".join(missing))

    # description sanity — the two things youtube-publish specifically checks
    desc = open(os.path.join(wd, "description.txt"), encoding="utf-8").read()
    first_line = desc.splitlines()[0].strip() if desc.strip() else ""
    warnings = []
    if "westfwliving.com/tv.html" not in first_line:
        warnings.append("description.txt line 1 should be the https://westfwliving.com/tv.html link")
    chapter_lines = [l for l in desc.splitlines() if re.match(r"^\s*\d{1,2}:\d{2}\b", l)]
    if not any(l.strip().startswith("0:00") for l in chapter_lines):
        warnings.append("CHAPTERS block must start with a '0:00' line on its own line (YouTube won't render chapters otherwise)")
    elif len(chapter_lines) < 3:
        warnings.append(f"only {len(chapter_lines)} chapter line(s) found; YouTube needs >=3 to show chapters")

    title = open(os.path.join(wd, "title.txt"), encoding="utf-8").read().strip()
    is_short = "#shorts" in title.lower()

    # ---- assemble READY_ folder ----
    dest = os.path.join(queue, f"READY_{slug}")
    if os.path.exists(dest):
        die(f"Destination already exists: {dest} (refusing to overwrite)")
    os.makedirs(dest)

    op = shutil.copy2 if args.copy else shutil.move
    op(mp4, os.path.join(dest, f"{slug}.mp4"))
    for f in REQUIRED_TEXT:
        op(os.path.join(wd, f), os.path.join(dest, f))
    for f in OPTIONAL:
        src = os.path.join(wd, f)
        if os.path.exists(src):
            op(src, os.path.join(dest, f))

    print(f"Staged {'SHORT' if is_short else 'FULL'} kit -> {dest}")
    print("  files:", ", ".join(sorted(os.listdir(dest))))
    if warnings:
        print("\nHEADS-UP (fix before publishing, youtube-publish will flag these):")
        for w in warnings:
            print("  - " + w)
    else:
        print("  kit validates against youtube-publish's expected format ✓")
    print(f"\nGoogle Drive will sync this folder. Then run youtube-publish: \"publish today's video\".")

if __name__ == "__main__":
    main()
