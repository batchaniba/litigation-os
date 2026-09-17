#!/usr/bin/env node
// Check upcoming deadlines and emit N-day warnings.
// Usage: node internal/scripts/check-deadlines.mjs [--days=N] [--format=json|markdown]
// Exit 0: no critical deadlines. Exit 2: critical deadlines found (within 3 days).
import { MATTERS_DIR } from "./load-matters.mjs";
import { loadAllClocks } from "./lib/load-clocks.mjs";
import { dateKeyFromLabel, daysBetween, todayKey } from "./lib/next-actions.mjs";
import { clocksToUpcomingEvents } from "./lib/upcoming-from-clocks.mjs";

const args = process.argv.slice(2);
const days = parseInt(args.find((a) => a.startsWith("--days="))?.split("=")[1] || "7", 10);
const format = args.find((a) => a.startsWith("--format="))?.split("=")[1] || "markdown";

const today = todayKey();
const upcoming = clocksToUpcomingEvents(loadAllClocks(MATTERS_DIR), { today });

const warnings = [];
for (const e of upcoming) {
  if (e.type !== "deadline") continue;
  const key = dateKeyFromLabel(e.date);
  if (!key) continue;
  const daysOut = daysBetween(today, key);
  if (daysOut < 0 || daysOut > days) continue;
  warnings.push({
    date: e.date,
    daysOut,
    event: e.event,
    matters: e.matters,
    verified_at: null,
    confidence: null,
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
      console.log(`${flag} **${w.date}** (${w.daysOut}d) — ${w.event.slice(0, 120)}`);
    }
  }
}

const critical = warnings.filter((w) => w.critical);
process.exit(critical.length ? 2 : 0);
