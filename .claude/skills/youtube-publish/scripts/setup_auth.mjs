#!/usr/bin/env node
/**
 * setup_auth.mjs — one-time login for the youtube-publish skill.
 *
 * Opens the persistent browser profile that publish_video.mjs reuses, navigates to YouTube Studio,
 * and waits while YOU sign in to the West FW Living channel (including any 2FA). Once you're on the
 * Studio dashboard, the session cookies are saved into the profile dir, and every future publish run
 * is hands-off — no login, no picker.
 *
 * You only need to run this again if the session expires or you switch machines.
 *
 * Usage:
 *   node setup_auth.mjs [--profile ~/.yt-publish-profile]
 *
 * Then confirm in the terminal (press Enter) once you can see the Studio dashboard for the correct
 * channel. Make sure the avatar top-right is the West FW Living brand account before confirming —
 * pinning comments later requires the channel account, not a personal one.
 */

import { chromium } from 'playwright';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { createInterface } from 'node:readline';

const args = Object.fromEntries(process.argv.slice(2).flatMap((a, i, arr) =>
  a.startsWith('--') ? [[a.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]] : []));
const PROFILE = (args.profile && args.profile !== true ? args.profile : join(homedir(), '.yt-publish-profile'));

const ctx = await chromium.launchPersistentContext(PROFILE, {
  headless: false,
  viewport: { width: 1366, height: 900 },
  args: ['--disable-blink-features=AutomationControlled'],
});
const page = ctx.pages()[0] || (await ctx.newPage());
await page.goto('https://studio.youtube.com');

console.error(`\nProfile: ${PROFILE}`);
console.error('A browser window is open. Sign in to the WEST FW LIVING channel (handle 2FA if asked).');
console.error('Confirm the top-right avatar is the West FW Living brand account.');
console.error('When you can see the Studio dashboard, come back here and press Enter to save the session.\n');

await new Promise((res) => {
  const rl = createInterface({ input: process.stdin, output: process.stderr });
  rl.question('Press Enter once logged in… ', () => { rl.close(); res(); });
});

console.error('Saving session and closing. Future runs will reuse this login.');
await ctx.close();
