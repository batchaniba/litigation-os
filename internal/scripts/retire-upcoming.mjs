#!/usr/bin/env node
// ==========================================================
// Flip upcoming: true → false when the dated event is already
// past in America/Los_Angeles. Does not hide a genuine PAST DUE
// on purpose — it retires clocks that rolled past today so
// validate-portfolio stops failing and the desk stays current.
//
// Usage:
//   npm run retire:upcoming           # write timeline.json
//   npm run retire:upcoming -- --check  # exit 1 if any flip is needed
// Then run npm run sync:upcoming (or npm run sync:all).
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { dateKeyFromLabel, todayKey } from "./lib/next-actions.mjs";
import { writeJsonAscii } from "./lib/write-json-ascii.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TIMELINE = path.resolve(__dirname, "../src/data/timeline.json");
const checkOnly = process.argv.includes("--check");
const today = todayKey("America/Los_Angeles");

const timeline = JSON.parse(fs.readFileSync(TIMELINE, "utf8"));
if (!Array.isArray(timeline)) {
  console.error("timeline.json must be an array");
  process.exit(1);
}

const flips = [];
for (const [i, event] of timeline.entries()) {
  if (event?.upcoming !== true) continue;
  const dateKey = dateKeyFromLabel(event.date);
  if (!dateKey || dateKey >= today) continue;
  flips.push({ index: i, date: event.date, dateKey, event: String(event.event ?? "").slice(0, 96) });
  if (!checkOnly) event.upcoming = false;
}

if (flips.length === 0) {
  console.log(`OK — no past upcoming flags (today is ${today} PT).`);
  process.exit(0);
}

if (checkOnly) {
  console.error(`${flips.length} upcoming event(s) are past ${today} PT — run npm run retire:upcoming`);
  for (const row of flips) {
    console.error(`  timeline[${row.index}] ${row.date}  ${row.event}`);
  }
  process.exit(1);
}

writeJsonAscii(TIMELINE, timeline);
console.log(`Retired ${flips.length} past upcoming flag(s) (today is ${today} PT):`);
for (const row of flips) {
  console.log(`  timeline[${row.index}] ${row.date}  ${row.event}`);
}
console.log("Run npm run sync:upcoming (or npm run sync:all) next.");
