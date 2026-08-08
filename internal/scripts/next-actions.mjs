#!/usr/bin/env node
// ==========================================================
// Answer "what's next on the list for me to do?" from portfolio data.
//
// Reads timeline.json (upcoming: true) + matters/summaries.json, ranks by
// urgency and by who the clock runs against, and prints a queue. Nothing is
// written to disk, so this output can never go stale the way a synced file can.
//
// Usage:
//   npm run next                  # next 30 days, your obligations first
//   npm run next -- --days 14     # tighter horizon
//   npm run next -- --all         # every upcoming entry, no horizon
//   npm run next -- --matter 20   # one matter only
//   npm run next -- --mine        # drop opposing-party / agency clocks
//   npm run next -- --json        # machine-readable
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildQueue, todayKey } from "./lib/next-actions.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.resolve(__dirname, "../src/data");
const TIMELINE = path.join(DATA_DIR, "timeline.json");
const SUMMARIES = path.join(DATA_DIR, "matters/summaries.json");

const argv = process.argv.slice(2);
const asJson = argv.includes("--json");
const showAll = argv.includes("--all");
const mineOnly = argv.includes("--mine");

function flagValue(name) {
  const index = argv.indexOf(name);
  return index === -1 ? null : argv[index + 1];
}

const horizonDays = showAll ? Number.POSITIVE_INFINITY : Number(flagValue("--days") ?? 30);
if (!Number.isFinite(horizonDays) && !showAll) {
  console.error("--days must be a number");
  process.exit(1);
}
const matterFilter = flagValue("--matter") ? Number(flagValue("--matter")) : null;

for (const file of [TIMELINE, SUMMARIES]) {
  if (!fs.existsSync(file)) {
    console.error(`Missing ${path.relative(process.cwd(), file)}`);
    process.exit(1);
  }
}

const timeline = JSON.parse(fs.readFileSync(TIMELINE, "utf8"));
const summaries = JSON.parse(fs.readFileSync(SUMMARIES, "utf8"));
const today = todayKey();
const queue = buildQueue(timeline, summaries, { today, horizonDays });

const matchesFilter = (item) => matterFilter === null || item.matters.includes(matterFilter);
const matchesActor = (item) => !mineOnly || item.actor === "you" || item.actor === "unknown";

const visible = queue.items.filter(
  (item) => item.urgency !== "later" && matchesFilter(item) && matchesActor(item),
);
const undated = queue.undated.filter((item) => matchesFilter(item) && matchesActor(item));
const gaps = matterFilter === null ? queue.gaps : queue.gaps.filter((g) => g.number === matterFilter);

if (asJson) {
  console.log(JSON.stringify({ today, horizonDays, items: visible, undated, gaps }, null, 2));
  process.exit(0);
}

const BANDS = [
  ["overdue", "PAST DUE — still flagged upcoming"],
  ["critical", "Next 3 days"],
  ["soon", "This week"],
  ["upcoming", showAll ? "Later" : `Next ${horizonDays} days`],
];

function countdown(item) {
  if (item.daysOut < 0) return `${Math.abs(item.daysOut)}d ago`;
  if (item.daysOut === 0) return "today";
  if (item.daysOut === 1) return "tomorrow";
  return `in ${item.daysOut}d`;
}

function actorNote(item) {
  if (item.actor === "you") return "";
  const label = item.actor === "opposing" ? "opposing party's clock" : "court/agency clock";
  return ` [${label}${item.actorSource === "inferred" ? ", inferred — verify" : ""}]`;
}

const horizonLabel = showAll ? "all upcoming" : `${horizonDays}-day horizon`;
console.log(`Next actions — as of ${today} (America/Los_Angeles, ${horizonLabel})`);
if (matterFilter !== null) console.log(`Filtered to Matter ${matterFilter}`);
console.log("=".repeat(72));

let printed = 0;
for (const [band, heading] of BANDS) {
  const rows = visible.filter((item) => item.urgency === band);
  if (rows.length === 0) continue;
  console.log(`\n${heading} (${rows.length})`);
  console.log("-".repeat(72));
  for (const item of rows) {
    printed += 1;
    const matters = item.matters.length ? `M${item.matters.join(", M")}` : "portfolio";
    console.log(`  ${item.date}  (${countdown(item)})  ${matters}  [${item.action}]${actorNote(item)}`);
    console.log(`    ${item.event}`);
    for (const label of item.matterLabels) console.log(`      · ${label}`);
  }
}

if (printed === 0) {
  console.log(`\nNothing dated inside the ${horizonLabel}.`);
}

if (undated.length > 0) {
  console.log(`\nUpcoming but not on one calendar day (${undated.length})`);
  console.log("-".repeat(72));
  for (const item of undated) {
    console.log(`  ${item.date}  M${item.matters.join(", M")}  [${item.action}]`);
    console.log(`    ${item.event}`);
  }
}

if (gaps.length > 0) {
  console.log(`\nActive matters with no dated next step (${gaps.length})`);
  console.log("-".repeat(72));
  for (const gap of gaps) {
    console.log(`  M${gap.number} — ${gap.caption}${gap.case_no ? ` (${gap.case_no})` : ""}`);
    if (gap.status_label) console.log(`    ${gap.status_label}`);
  }
}

console.log(
  "\nSource: internal/src/data/timeline.json (upcoming: true) + matters/summaries.json.",
);
console.log("Deadlines are as recorded in the portfolio — confirm against the docket before relying on one.");
