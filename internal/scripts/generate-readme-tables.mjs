#!/usr/bin/env node
// ==========================================================
// Regenerate marked README sections from portfolio data.
//
// Source of truth:
//   - internal/src/data/matters/NN.json  (matter tables + counts)
//   - internal/src/data/timeline.json    (upcoming deadlines)
//   - internal/src/data/damages.js       (damages summary + aggregates)
//
// Markers (HTML comments) in README.md delimit regenerable blocks:
//   <!-- PORTFOLIO:<NAME>:START -->
//   ...
//   <!-- PORTFOLIO:<NAME>:END -->
//
// Usage:
//   npm run generate:readme           # write README.md
//   npm run generate:readme -- --check  # exit 1 if stale
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { loadMatters } from "./load-matters.mjs";
import { lifecycleLabel, readmeBucket } from "./matter-lifecycle.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const README = path.join(REPO_ROOT, "README.md");
const checkOnly = process.argv.includes("--check");

const MONTHS = {
  jan: 0,
  january: 0,
  feb: 1,
  february: 1,
  mar: 2,
  march: 2,
  apr: 3,
  april: 3,
  may: 4,
  jun: 5,
  june: 5,
  jul: 6,
  july: 6,
  aug: 7,
  august: 7,
  sep: 8,
  sept: 8,
  september: 8,
  oct: 9,
  october: 9,
  nov: 10,
  november: 10,
  dec: 11,
  december: 11,
};

function escapeCell(value) {
  return String(value ?? "")
    .replace(/\r?\n/g, " ")
    .replace(/\|/g, "\\|")
    .trim();
}

function truncate(text, max) {
  const s = String(text ?? "").replace(/\s+/g, " ").trim();
  if (s.length <= max) return s;

  // Prefer a natural clause break before hard truncation.
  const clauseBreaks = [];
  for (const re of [/;\s+/g, /\s+[—–-]\s+/g, /\.\s+(?=[A-Z])/g]) {
    let m;
    while ((m = re.exec(s)) !== null) {
      const end = m.index + (s[m.index] === "." ? 1 : 0);
      if (end >= 48 && end <= max) clauseBreaks.push(end);
    }
  }
  if (clauseBreaks.length) {
    return s.slice(0, Math.max(...clauseBreaks)).trim();
  }

  const cut = s.slice(0, max);
  const word = cut.lastIndexOf(" ");
  return `${(word > 40 ? cut.slice(0, word) : cut).trim()}…`;
}

// A table cell wants the short posture, which is exactly what status_label is —
// so no truncation here. The narrative `status` stays out of the README tables.
function shortStatus(matter, { closed = false } = {}) {
  const label = (matter.status_label || "").replace(/\s+/g, " ").trim();
  if (closed && matter.lifecycle && matter.lifecycle !== "closed") {
    const lifecycle = lifecycleLabel(matter.lifecycle).toUpperCase();
    if (!label.toUpperCase().startsWith(lifecycle)) {
      return escapeCell(`**${lifecycle}** — ${label}`);
    }
  }
  return escapeCell(label);
}

function bucket(matter) {
  return readmeBucket(matter.lifecycle);
}

function parsePortfolioDate(dateStr) {
  const s = String(dateStr || "").trim();
  const m = s.match(/^([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})$/);
  if (!m) return null;
  const month = MONTHS[m[1].toLowerCase()];
  if (month == null) return null;
  return new Date(Date.UTC(Number(m[3]), month, Number(m[2])));
}

function money(n) {
  const rounded = Math.round(Number(n) || 0);
  return `$${rounded.toLocaleString("en-US")}`;
}

function replaceBlock(readme, name, body) {
  const start = `<!-- PORTFOLIO:${name}:START -->`;
  const end = `<!-- PORTFOLIO:${name}:END -->`;
  const startIdx = readme.indexOf(start);
  const endIdx = readme.indexOf(end);
  if (startIdx === -1 || endIdx === -1 || endIdx < startIdx) {
    throw new Error(`README.md missing markers for PORTFOLIO:${name}`);
  }
  const before = readme.slice(0, startIdx + start.length);
  const after = readme.slice(endIdx);
  const inner = body.endsWith("\n") ? body : `${body}\n`;
  return `${before}\n${inner}${after}`;
}

const cases = loadMatters();
const timeline = JSON.parse(
  fs.readFileSync(path.join(REPO_ROOT, "internal/src/data/timeline.json"), "utf8"),
);
const { damages_table } = await import(pathToFileURL(path.join(REPO_ROOT, "internal/src/data/damages.js")).href);

const active = cases.filter((m) => bucket(m) === "active");
const settled = cases.filter((m) => bucket(m) === "settled");
const closed = cases.filter((m) => bucket(m) === "closed");

const settledLabel = settled.length
  ? settled
      .map((m) => {
        const when = (m.status.match(/SETTLED\s*[—-]\s*([^;(]+)/i) || [])[1]?.trim();
        return `${m.number} — ${m.caption}${when ? `, ${when}` : ""}`;
      })
      .join("; ")
  : "none";

const overviewCounts = [
  `| Total Matters | ${cases.length} |`,
  `| Active / Open | ${active.length} |`,
  `| Settled | ${settled.length}${settled.length ? ` (Matter ${settledLabel})` : ""} |`,
  `| Dismissed / Closed / Abandoned | ${closed.length} |`,
].join("\n");

const cons = damages_table.reduce((s, r) => s + (r.conservative || 0), 0);
const mod = damages_table.reduce((s, r) => s + (r.moderate || 0), 0);
const agg = damages_table.reduce((s, r) => s + (r.aggressive || 0), 0);

const roundK = (n) => Math.round(Number(n) / 1000) * 1000;
const overviewExposure = [
  `| Aggregate Exposure (Conservative) | ~${money(roundK(cons))}+ |`,
  `| Aggregate Exposure (Moderate) | ~${money(roundK(mod))}+ |`,
  `| Aggregate Exposure (Aggressive) | ~${money(roundK(agg))}+ |`,
].join("\n");

const activeTable = [
  `| # | Caption | Case No. | Court | Type | Status |`,
  `|---|---|---|---|---|---|`,
  ...active.map(
    (m) =>
      `| ${m.number} | ${escapeCell(m.caption)} | ${escapeCell(m.case_no)} | ${escapeCell(m.court)} | ${escapeCell(m.type)} | ${shortStatus(m)} |`,
  ),
].join("\n");

const settledTable = [
  `| # | Caption | Case No. | Court | Outcome |`,
  `|---|---|---|---|---|`,
  ...settled.map(
    (m) =>
      `| ${m.number} | ${escapeCell(m.caption)} | ${escapeCell(m.case_no)} | ${escapeCell(m.court)} | ${shortStatus(m)} |`,
  ),
].join("\n");

const closedTable = [
  `| # | Caption | Case No. | Court | Disposition |`,
  `|---|---|---|---|---|`,
  ...closed.map(
    (m) =>
      `| ${m.number} | ${escapeCell(m.caption)} | ${escapeCell(m.case_no)} | ${escapeCell(m.court)} | ${shortStatus(m, { closed: true })} |`,
  ),
].join("\n");

const upcoming = timeline
  .filter((t) => t.upcoming === true)
  .map((t, i) => ({ ...t, _i: i, _d: parsePortfolioDate(t.date) }))
  .sort((a, b) => {
    if (a._d && b._d) return a._d - b._d || a._i - b._i;
    if (a._d) return -1;
    if (b._d) return 1;
    return a._i - b._i;
  });

const deadlinesTable = [
  `| Date | Matter | Event |`,
  `|---|---|---|`,
  ...upcoming.map(
    (t) => `| ${escapeCell(t.date)} | ${escapeCell(t.matters)} | ${escapeCell(truncate(t.event, 220))} |`,
  ),
].join("\n");

const damagesTable = [
  `| Category | Matters | Conservative | Moderate | Aggressive |`,
  `|---|---|---|---|---|`,
  ...damages_table.map(
    (r) =>
      `| ${escapeCell(r.category)} | ${escapeCell(r.matters)} | ${money(r.conservative)} | ${money(r.moderate)} | ${money(r.aggressive)} |`,
  ),
  `| **Portfolio Total (pre-deduplication)** | | **${money(cons)}** | **${money(mod)}** | **${money(agg)}** |`,
].join("\n");

const abandoned = closed.filter((m) => m.lifecycle === "abandoned");
const dismissed = closed.filter((m) => m.lifecycle === "dismissed");
const otherClosed = closed.filter((m) => m.lifecycle === "closed");
const closedCountNote =
  `*Of the ${closed.length} dismissed/closed/abandoned matters: ${abandoned.length} abandoned, ` +
  `${dismissed.length} dismissed, ${otherClosed.length} otherwise closed ` +
  `(structured \`lifecycle\` on each matter JSON). See [All Matters](#all-matters) below for the full disposition table. ` +
  `Pre-filing matters stay in the Active table.*`;

let readme = fs.readFileSync(README, "utf8");
const replacements = {
  OVERVIEW_COUNTS: overviewCounts,
  OVERVIEW_EXPOSURE: overviewExposure,
  CLOSED_COUNT_NOTE: closedCountNote,
  ACTIVE_MATTERS: activeTable,
  SETTLED_MATTERS: settledTable,
  CLOSED_MATTERS: closedTable,
  UPCOMING_DEADLINES: deadlinesTable,
  DAMAGES_SUMMARY: damagesTable,
};

for (const [name, body] of Object.entries(replacements)) {
  readme = replaceBlock(readme, name, body);
}

if (checkOnly) {
  const current = fs.readFileSync(README, "utf8");
  if (current !== readme) {
    console.error("README.md generated tables are stale — run npm run generate:readme");
    process.exit(1);
  }
  console.log(
    `OK — README portfolio tables are current (${active.length} active, ${settled.length} settled, ${closed.length} closed, ${upcoming.length} upcoming).`,
  );
  process.exit(0);
}

fs.writeFileSync(README, readme);
console.log(
  `Updated ${path.relative(REPO_ROOT, README)} ` +
    `(${active.length} active / ${settled.length} settled / ${closed.length} closed / ${upcoming.length} upcoming).`,
);
