#!/usr/bin/env node
// Production-output credibility validator — runs INSIDE the Netlify build
// command (see netlify.toml) so it cannot be skipped during a normal deploy.
// Scans every .html file in the publish directory (the repo root — this site
// deploys its source tree as-is) against scripts/prohibited-content.json and
// exits nonzero on any hit, which FAILS the Netlify build and blocks the
// deploy. Local equivalent: the placeholder-assert gate in
// scripts/apply_standing_fixes.py reads the same config.
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SKIP_DIRS = new Set([".git", ".netlify", "node_modules", "gen", "docs",
  "editorial", "reports", "scripts"]);
const config = JSON.parse(
  fs.readFileSync(path.join(__dirname, "prohibited-content.json"), "utf8"));
const patterns = config.patterns.map(p => ({re: new RegExp(p.re, "i"), label: p.label}));

function* htmlFiles(dir) {
  for (const ent of fs.readdirSync(dir, {withFileTypes: true})) {
    if (ent.isDirectory()) {
      if (!SKIP_DIRS.has(ent.name)) yield* htmlFiles(path.join(dir, ent.name));
    } else if (ent.name.endsWith(".html")) {
      yield path.join(dir, ent.name);
    }
  }
}

let files = 0;
const violations = [];
for (const fp of htmlFiles(ROOT)) {
  files++;
  const doc = fs.readFileSync(fp, "utf8");
  for (const {re, label} of patterns) {
    const m = doc.match(re);
    if (m) violations.push(`${path.relative(ROOT, fp)}: ${label} (${JSON.stringify(m[0].slice(0, 60))})`);
  }
}

if (violations.length) {
  console.error(`\nPRODUCTION VALIDATION FAILED — prohibited content in deployable HTML (${violations.length} hit(s) across ${files} files):`);
  for (const v of violations.slice(0, 40)) console.error("  ✗ " + v);
  console.error("\nThe deploy is blocked. Remove the content (render nothing where no verified first-hand material exists) and rebuild.");
  process.exit(1);
}
console.log(`production validation OK — ${files} HTML files scanned, 0 prohibited strings.`);
