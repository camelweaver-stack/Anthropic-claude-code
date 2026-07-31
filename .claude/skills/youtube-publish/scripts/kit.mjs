// kit.mjs — read a READY_ kit folder into a normalized object, tolerant of BOTH kit conventions:
//   (a) the real West FW Living convention: title.txt + description.txt + a COMBINED tags-pinned-embed.txt
//       (tags, then ---PINNED COMMENT---, ---EMBED TARGET---, ---VIDEO FILE--- sections)
//   (b) separate files: tags.txt + pinned-comment.txt + embed-target.txt
// Separate files win if present; otherwise the combined file is parsed. This is what lets youtube-publish
// consume folders the human pipeline (and video-render/stage_kit) actually produce.

import { readFile, readdir, access } from 'node:fs/promises';
import { join, basename } from 'node:path';

async function exists(p) { try { await access(p); return true; } catch { return false; } }
async function readIf(p) { return (await exists(p)) ? await readFile(p, 'utf8') : null; }

const SECTION = /^-{2,}\s*(PINNED COMMENT|EMBED TARGET|VIDEO FILE)\s*-{2,}\s*$/i;

/** Parse the combined tags-pinned-embed.txt into its parts. */
export function parseCombined(text) {
  const key = { 'PINNED COMMENT': 'pinned', 'EMBED TARGET': 'embed', 'VIDEO FILE': 'video' };
  const buckets = { tags: [], pinned: [], embed: [], video: [] };
  let cur = 'tags';
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(SECTION);
    if (m) { cur = key[m[1].toUpperCase()]; continue; }
    buckets[cur].push(line);
  }
  const videoRaw = buckets.video.join('\n').trim();
  return {
    tags: buckets.tags.join('\n').trim(),
    pinnedComment: buckets.pinned.join('\n').trim(),
    embedTarget: buckets.embed.join('\n').trim() || null,
    // strip a trailing note like "rent-report-august-2026.mp4 (place in this folder; ...)"
    videoFile: videoRaw ? videoRaw.replace(/\s*\(.*$/s, '').trim() : null,
  };
}

/** Read and normalize a READY_ kit folder. */
export async function loadKit(dir) {
  const title = (await readIf(join(dir, 'title.txt')))?.trim() || null;
  const description = (await readIf(join(dir, 'description.txt'))) || null;

  let tags = (await readIf(join(dir, 'tags.txt')))?.trim() ?? null;
  let pinnedComment = (await readIf(join(dir, 'pinned-comment.txt')))?.trim() ?? null;
  let embedTarget = (await readIf(join(dir, 'embed-target.txt')))?.trim() || null;
  let declaredVideo = null;

  const combined = await readIf(join(dir, 'tags-pinned-embed.txt'));
  if (combined) {
    const p = parseCombined(combined);
    if (tags == null) tags = p.tags;
    if (pinnedComment == null) pinnedComment = p.pinnedComment;
    if (embedTarget == null) embedTarget = p.embedTarget;
    declaredVideo = p.videoFile;
  }

  // resolve the mp4: prefer the declared filename, else <folder-slug>.mp4, else the first .mp4
  const slug = basename(dir).replace(/^READY_/, '');
  let videoPath = null;
  const candidates = [];
  if (declaredVideo) candidates.push(declaredVideo);
  candidates.push(`${slug}.mp4`);
  for (const c of candidates) { if (await exists(join(dir, c))) { videoPath = join(dir, c); break; } }
  if (!videoPath) {
    const found = (await readdir(dir)).find(f => f.toLowerCase().endsWith('.mp4'));
    if (found) videoPath = join(dir, found);
  }

  const thumb = (await exists(join(dir, 'thumbnail.png'))) ? join(dir, 'thumbnail.png') : null;

  return {
    slug, title, description,
    tags: tags || '',
    pinnedComment: pinnedComment || '',
    embedTarget,
    videoPath, thumbnailPath: thumb,
  };
}
