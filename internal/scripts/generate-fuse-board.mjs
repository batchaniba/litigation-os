#!/usr/bin/env node
// Generate the live Fuse / Wait / Parked board from the machine index.
// The board is a *derived view* — the data lives in matter identity records,
// per-matter clocks.json (split) or timeline.json upcoming events (legacy),
// surfaced as next_clock in internal/src/data/index/matters.json.
// Run `npm run sync:index` before this so the index is current.
//
//   node internal/scripts/generate-fuse-board.mjs
//   node internal/scripts/generate-fuse-board.mjs --check
//
// Columns:
//   Fuse   — active matter with a live clock dated within the next 14 days
//            (or already overdue). A date that costs a right if missed.
//   Wait   — active matter with no fuse-grade clock; ball is elsewhere.
//   Parked — pre-filing matter; no move until a named event.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { todayKey } from "./lib/next-actions.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const INDEX_PATH = path.join(REPO_ROOT, "internal/src/data/index/matters.json");
const OUT_PATH = path.join(REPO_ROOT, "internal/docs/FUSE_BOARD.md");
const FUSE_DAYS = 14;
const checkOnly = process.argv.includes("--check");

const addDays = (key, n) => {
  const d = new Date(`${key}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};

const today = todayKey();
const horizon = addDays(today, FUSE_DAYS);
const index = JSON.parse(fs.readFileSync(INDEX_PATH, "utf8"));
const matters = index.matters ?? [];

const row = (m) => {
  const c = m.next_clock;
  const when = !c ? "no live clock" : c.date ? `${c.date}${m.overdue ? " — OVERDUE" : ""}` : "undated";
  const what = c ? c.title : "—";
  return `| M${m.number} | ${m.caption} | ${when} | ${what} |`;
};

const byDate = (a, b) => {
  if (a.overdue !== b.overdue) return a.overdue ? -1 : 1;
  const da = a.next_clock?.date ?? "9999-99-99";
  const db = b.next_clock?.date ?? "9999-99-99";
  return da.localeCompare(db) || a.number - b.number;
};

const fuse = matters
  .filter(
    (m) =>
      m.lifecycle === "active" &&
      m.next_clock?.date &&
      (m.overdue || m.next_clock.date <= horizon),
  )
  .sort(byDate);
const wait = matters
  .filter((m) => m.lifecycle === "active" && !fuse.includes(m))
  .sort(byDate);
const parked = matters.filter((m) => m.lifecycle === "pre_filing").sort((a, b) => a.number - b.number);
const terminal = matters.filter((m) =>
  ["dismissed", "abandoned", "closed", "settled"].includes(m.lifecycle),
);

const section = (title, rule, list) =>
  `## ${title}\n\n*${rule}*\n\n` +
  (list.length
    ? `| Matter | Caption | Clock | Next |\n|---|---|---|---|\n${list.map(row).join("\n")}\n`
    : "_Empty._\n");

const doc = `# Fuse Board\n\n` +
  `> Generated ${today} by \`node internal/scripts/generate-fuse-board.mjs\` — do not hand-edit.\n` +
  `> Source of truth: \`internal/src/data/index/matters.json\` (next_clock per matter).\n` +
  `> Fuse window: ${today} → ${horizon} (${FUSE_DAYS} days). ` +
  `Active: ${matters.filter((m) => m.lifecycle === "active").length}. ` +
  `Terminal (dismissed/abandoned/closed/settled): ${terminal.length} — not listed.\n\n` +
  `**Breath rule:** if it is not on Fuse, it does not get drafted tonight.\n\n` +
  section("Fuse", "A date in the next 14 days that costs a right if missed.", fuse) +
  `\n` +
  section("Wait", "Ball is on a court or a lawyer.", wait) +
  `\n` +
  section("Parked", "No move until a named event.", parked);

const next = `${doc}\n`;
if (checkOnly) {
  if (!fs.existsSync(OUT_PATH) || fs.readFileSync(OUT_PATH, "utf8") !== next) {
    console.error("internal/docs/FUSE_BOARD.md is stale — run node internal/scripts/generate-fuse-board.mjs");
    process.exit(1);
  }
  console.log("OK — FUSE_BOARD.md is current.");
  process.exit(0);
}
fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
fs.writeFileSync(OUT_PATH, next);
console.log(
  `Wrote internal/docs/FUSE_BOARD.md — Fuse: ${fuse.length}, Wait: ${wait.length}, Parked: ${parked.length}.`,
);
