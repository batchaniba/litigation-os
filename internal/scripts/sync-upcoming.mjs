#!/usr/bin/env node
// ==========================================================
// Build light upcoming-deadline list for the SPA shell bundle.
//
// Live calendar is clocks.json (open/set, dated, including overdue).
// timeline.json stays the archive. CourtListener appends split events.jsonl
// and parks deadline text as proposed_clock in review.json — never clocks.json.
//
// Usage:
//   npm run sync:upcoming           # write upcoming.json
//   npm run sync:upcoming -- --check  # exit 1 if out of date
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { MATTERS_DIR } from "./load-matters.mjs";
import { loadAllClocks } from "./lib/load-clocks.mjs";
import { todayKey } from "./lib/next-actions.mjs";
import { clocksToUpcomingEvents } from "./lib/upcoming-from-clocks.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.resolve(__dirname, "../src/data");
const OUT = path.join(DATA_DIR, "upcoming.json");
const checkOnly = process.argv.includes("--check");

const upcoming = clocksToUpcomingEvents(loadAllClocks(MATTERS_DIR), { today: todayKey() });
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
