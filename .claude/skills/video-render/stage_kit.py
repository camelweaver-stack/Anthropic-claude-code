#!/usr/bin/env python3
"""
stage_kit.py — assemble a READY_<slug>/ folder in the shape the youtube-publish skill consumes,
then move it into the Video Upload Queue. Run after build_video.py + build_v2.py.

Kit shape (the real West FW Living convention, confirmed from the live queue):
  title.txt              one line, exact title (append " #Shorts" for a Short)
  description.txt        includes the https://westfwliving.com/tv.html link and a CHAPTERS block
                         (first chapter "0:00" on its own line, >=3 chapters)
  tags-pinned-embed.txt  combined file:
                             <comma-separated tags>
                             ---PINNED COMMENT---
                             <comment to pin>
                             ---EMBED TARGET---
                             rent-report/<month>-<year>.html
                             ---VIDEO FILE---
                             <slug>.mp4 (place in this folder; thumbnail.png alongside)
  <slug>.mp4             the rendered video
  thumbnail.png          optional 1280x720 thumbnail

Separate tags.txt / pinned-comment.txt / embed-target.txt are also accepted (youtube-publish reads
either form) — but the combined file is the house convention, so prefer it.

Usage:
  python stage_kit.py --slug rent-report-september-2026 [--workdir .] [--queue "<path>"] [--copy]

--queue defaults to queue_path.txt next to this script. --copy leaves originals in place (default: move).
"""
import argparse, os, shutil, sys, re

SEP = re.compile(r"^-{2,}\s*(PINNED COMMENT|EMBED TARGET|VIDEO FILE)\s*-{2,}\s*$", re.I)

def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr); sys.exit(1)

def parse_combined(text):
    key = {"PINNED COMMENT": "pinned", "EMBED TARGET": "embed", "VIDEO FILE": "video"}
    buckets = {"tags": [], "pinned": [], "embed": [], "video": []}
    cur = "tags"
    for line in text.splitlines():
        m = SEP.match(line)
        if m:
            cur = key[m.group(1).upper()]; continue
        buckets[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in buckets.items()}

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

    queue = args.queue
    if not queue:
        qp = os.path.join(here, "queue_path.txt")
        if os.path.exists(qp):
            queue = open(qp, encoding="utf-8").read().strip()
    if not queue:
        die("No queue path. Pass --queue or create queue_path.txt (see SKILL.md one-time setup).")
    if not os.path.isdir(queue):
        die(f"Queue folder not found: {queue}")

    def wpath(name): return os.path.join(wd, name)
    mp4 = wpath(f"{slug}.mp4")

    # ---- validate BEFORE touching the queue ----
    missing = []
    for f in ("title.txt", "description.txt"):
        if not os.path.exists(wpath(f)):
            missing.append(f)
    if not os.path.exists(mp4):
        missing.append(f"{slug}.mp4")

    has_combined = os.path.exists(wpath("tags-pinned-embed.txt"))
    has_separate = os.path.exists(wpath("tags.txt")) and os.path.exists(wpath("pinned-comment.txt"))
    if not (has_combined or has_separate):
        missing.append("tags-pinned-embed.txt (or separate tags.txt + pinned-comment.txt)")
    if missing:
        die("Missing required kit file(s) in workdir: " + ", ".join(missing))

    # resolve tags/pinned/embed for validation
    if has_combined:
        parts = parse_combined(open(wpath("tags-pinned-embed.txt"), encoding="utf-8").read())
        tags, pinned, embed = parts["tags"], parts["pinned"], parts["embed"]
    else:
        tags = open(wpath("tags.txt"), encoding="utf-8").read().strip()
        pinned = open(wpath("pinned-comment.txt"), encoding="utf-8").read().strip()
        embed = (open(wpath("embed-target.txt"), encoding="utf-8").read().strip()
                 if os.path.exists(wpath("embed-target.txt")) else "")

    desc = open(wpath("description.txt"), encoding="utf-8").read()
    warnings = []
    if "westfwliving.com/tv.html" not in desc:
        warnings.append("description.txt should include the https://westfwliving.com/tv.html link")
    chapter_lines = [l for l in desc.splitlines() if re.match(r"^\s*\d{1,2}:\d{2}\b", l)]
    if not any(l.strip().startswith("0:00") for l in chapter_lines):
        warnings.append("CHAPTERS needs a '0:00' line on its own line (YouTube won't render chapters otherwise)")
    elif len(chapter_lines) < 3:
        warnings.append(f"only {len(chapter_lines)} chapter line(s); YouTube needs >=3 to show chapters")
    if not tags:
        warnings.append("no tags found")
    if not pinned:
        warnings.append("no pinned comment found")
    if not embed:
        warnings.append("no embed target found (embed-back step will skip this video until set)")

    title = open(wpath("title.txt"), encoding="utf-8").read().strip()
    is_short = "#shorts" in title.lower()

    # ---- assemble READY_ folder ----
    dest = os.path.join(queue, f"READY_{slug}")
    if os.path.exists(dest):
        die(f"Destination already exists: {dest} (refusing to overwrite)")
    os.makedirs(dest)

    op = shutil.copy2 if args.copy else shutil.move
    op(mp4, os.path.join(dest, f"{slug}.mp4"))
    for f in ("title.txt", "description.txt", "tags-pinned-embed.txt",
              "tags.txt", "pinned-comment.txt", "embed-target.txt", "thumbnail.png"):
        if os.path.exists(wpath(f)):
            op(wpath(f), os.path.join(dest, f))

    print(f"Staged {'SHORT' if is_short else 'FULL'} kit -> {dest}")
    print("  files:", ", ".join(sorted(os.listdir(dest))))
    if warnings:
        print("\nHEADS-UP (fix before publishing):")
        for w in warnings:
            print("  - " + w)
    else:
        print("  kit validates against youtube-publish's expected format ✓")
    print(f"\nGoogle Drive will sync this folder. Then run youtube-publish: \"publish today's video\".")

if __name__ == "__main__":
    main()
