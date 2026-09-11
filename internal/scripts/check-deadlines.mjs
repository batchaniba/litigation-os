#!/usr/bin/env node
// Check upcoming deadlines and emit N-day warnings.
// Usage: node internal/scripts/check-deadlines.mjs [--days=N] [--format=json|markdown]
// Exit 0: no critical deadlines. Exit 2: critical deadlines found (within 3 days).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.resolve(__dirname, "../src/data");

const args = process.argv.slice(2);
const days = parseInt(args.find((a) => a.startsWith("--days="))?.split("=")[1] || "7", 10);
const format = args.find((a) => a.startsWith("--format="))?.split("=")[1] || "markdown";

const timeline = JSON.parse(fs.readFileSync(path.join(DATA_DIR, "timeline.json"), "utf8"));

const today = new Date();
today.setHours(0, 0, 0, 0);

function parseDate(s) {
  // "Sep. 14, 2026" -> Date
  const d = new Date(s.replace(/\./g, ""));
  return isNaN(d) ? null : d;
}

const warnings = [];
for (const e of timeline) {
  if (e.upcoming !== true || e.type !== "deadline") continue;
  const d = parseDate(e.date);
  if (!d) continue;
  const daysOut = Math.round((d - today) / 86400000);
  if (daysOut < 0 || daysOut > days) continue;
  warnings.push({
    date: e.date,
    daysOut,
    event: e.event,
    matters: e.matters,
    verified_at: e.verified_at || null,
    confidence: e.confidence || null,
    critical: daysOut <= 3,
  });
}

warnings.sort((a, b) => a.daysOut - b.daysOut);

if (format === "json") {
  console.log(JSON.stringify({ generated: new Date().toISOString(), days, warnings }, null, 2));
} else {
  if (!warnings.length) {
    console.log(`No deadlines in the next ${days} days.`);
  } else {
    console.log(`## Deadlines in the next ${days} days (${warnings.length})\n`);
    for (const w of warnings) {
      const flag = w.critical ? "\u26a0\ufe0f" : "\u2022";
      const verified = w.verified_at ? ` (verified ${w.verified_at})` : " (unverified)";
      console.log(`${flag} **${w.date}** (${w.daysOut}d) — ${w.event.slice(0, 120)}${verified}`);
    }
  }
}

const critical = warnings.filter((w) => w.critical);
process.exit(critical.length ? 2 : 0);
