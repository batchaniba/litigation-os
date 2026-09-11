#!/usr/bin/env node
// ==========================================================
// Build light upcoming-deadline list for the SPA shell bundle.
//
// Full timeline stays in timeline.json and is only imported by
// route/search chunks that need the complete event log. The dashboard
// "what's next" queue and the shell deadline clock both read this file.
//
// Usage:
//   npm run sync:upcoming           # write upcoming.json
//   npm run sync:upcoming -- --check  # exit 1 if out of date
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.resolve(__dirname, "../src/data");
const TIMELINE = path.join(DATA_DIR, "timeline.json");
const OUT = path.join(DATA_DIR, "upcoming.json");
const checkOnly = process.argv.includes("--check");

if (!fs.existsSync(TIMELINE)) {
  console.error(`Missing ${path.relative(process.cwd(), TIMELINE)}`);
  process.exit(1);
}

const timeline = JSON.parse(fs.readFileSync(TIMELINE, "utf8"));
if (!Array.isArray(timeline)) {
  console.error("timeline.json must be an array");
  process.exit(1);
}

const upcoming = timeline.filter((event) => event?.upcoming === true);
const payload = `${JSON.stringify(upcoming, null, 2)}\n`;

if (checkOnly) {
  if (!fs.existsSync(OUT)) {
    console.error(`Missing ${path.relative(process.cwd(), OUT)} — run npm run sync:upcoming`);
    process.exit(1);
  }
  const current = fs.readFileSync(OUT, "utf8");
  if (current !== payload) {
    console.error("internal/src/data/upcoming.json is stale — run npm run sync:upcoming");
    process.exit(1);
  }
  console.log(`OK — upcoming.json is current (${upcoming.length} events).`);
  process.exit(0);
}

fs.writeFileSync(OUT, payload);
console.log(`Wrote ${path.relative(process.cwd(), OUT)} (${upcoming.length} events, ${payload.length} bytes).`);
