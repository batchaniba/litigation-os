#!/usr/bin/env node
// Build the crawler index: one small file per concern, covering every matter.
//
//   node internal/scripts/sync-machine-index.mjs
//   node internal/scripts/sync-machine-index.mjs --check
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters, MATTERS_DIR } from "./load-matters.mjs";
import { dateKeyFromLabel, todayKey } from "./lib/next-actions.mjs";
import { GRAPH_CONTRACT, loadJsonIfPresent, paddedMatterNumber } from "./lib/matter-layout.mjs";
import { matterRefsInclude } from "../src/utils/matterRefs.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const INDEX_DIR = path.join(REPO_ROOT, "internal/src/data/index");
const TIMELINE_PATH = path.join(REPO_ROOT, "internal/src/data/timeline.json");
const CROSS_PATH = path.join(REPO_ROOT, "internal/src/data/crossMatter.json");
const checkOnly = process.argv.includes("--check");

const CLOCK_RANK = {
  open: 0,
  set: 0,
  overdue: 0,
  contingent: 2,
  undated: 3,
  vacated: 9,
  satisfied: 9,
};

function clockSortDate(clock) {
  return clock.date || clock.date_label || "9999-99-99";
}

function liveClocks(clocks) {
  return clocks.filter((c) => !["vacated", "satisfied"].includes(c.status));
}

function nextFromClocks(clocks, today) {
  const live = liveClocks(clocks).slice().sort((a, b) => {
    const rank = (CLOCK_RANK[a.status] ?? 5) - (CLOCK_RANK[b.status] ?? 5);
    if (rank) return rank;
    return String(clockSortDate(a)).localeCompare(String(clockSortDate(b)));
  });
  const dated = live.find((c) => c.date);
  const chosen = dated ?? live[0] ?? null;
  if (!chosen) return { next_clock: null, overdue: false };
  const overdue = Boolean(chosen.date && chosen.date < today && chosen.status !== "contingent");
  return {
    next_clock: {
      id: chosen.id,
      date: chosen.date ?? null,
      kind: chosen.kind,
      status: overdue ? "overdue" : chosen.status,
      title: chosen.title,
      source_dkt: chosen.source_dkt ?? null,
    },
    overdue,
  };
}

function nextFromTimeline(timeline, number, today) {
  const rows = timeline.filter(
    (row) => row.upcoming === true && matterRefsInclude(row.matters, number),
  );
  const dated = rows
    .map((row) => ({ row, date: dateKeyFromLabel(row.date) }))
    .filter((x) => x.date)
    .sort((a, b) => a.date.localeCompare(b.date));
  const chosen = dated[0];
  if (!chosen) return { next_clock: null, overdue: false };
  const overdue = chosen.date < today;
  return {
    next_clock: {
      id: null,
      date: chosen.date,
      kind: chosen.row.type ?? "event",
      status: overdue ? "overdue" : "open",
      title: String(chosen.row.event ?? "").slice(0, GRAPH_CONTRACT.indexNextClockTitleChars),
      source_dkt: null,
    },
    overdue,
  };
}

function writeIfChanged(filePath, payload) {
  const next = `${JSON.stringify(payload, null, 2)}\n`;
  if (checkOnly) {
    if (!fs.existsSync(filePath) || fs.readFileSync(filePath, "utf8") !== next) {
      console.error(`${path.relative(REPO_ROOT, filePath)} is stale — run node internal/scripts/sync-machine-index.mjs`);
      return false;
    }
    return true;
  }
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, next);
  return true;
}

const matters = loadMatters();
const timeline = JSON.parse(fs.readFileSync(TIMELINE_PATH, "utf8"));
const cross = JSON.parse(fs.readFileSync(CROSS_PATH, "utf8"));
const today = todayKey();

const indexMatters = matters.map((m) => {
  const layout = m.__layout === "split" ? "split" : "legacy";
  const rel =
    layout === "split"
      ? `internal/src/data/matters/${paddedMatterNumber(m.number)}/`
      : `internal/src/data/matters/${paddedMatterNumber(m.number)}.json`;
  const clocks =
    layout === "split"
      ? loadJsonIfPresent(path.join(MATTERS_DIR, paddedMatterNumber(m.number), "clocks.json")) ?? []
      : [];
  const fromClocks = layout === "split" ? nextFromClocks(clocks, today) : { next_clock: null, overdue: false };
  const fromTimeline = nextFromTimeline(timeline, m.number, today);
  const picked = fromClocks.next_clock ? fromClocks : fromTimeline;
  const files =
    layout === "split"
      ? fs.readdirSync(path.join(MATTERS_DIR, paddedMatterNumber(m.number))).sort()
      : [`${paddedMatterNumber(m.number)}.json`];
  return {
    number: m.number,
    path: rel,
    layout,
    caption: m.caption,
    case_no: m.case_no,
    court: m.court,
    judge: m.judge,
    cluster: m.cluster,
    related: Array.isArray(m.related) ? m.related : [],
    same_incident: m.same_incident ?? null,
    lifecycle: m.lifecycle,
    proceeding: m.proceeding,
    phase: m.phase,
    next_clock: picked.next_clock,
    overdue: picked.overdue,
    last_updated: m.last_updated ?? null,
    files,
  };
});

const clusters = (cross.clusters ?? []).map((c) => ({
  id: c.id,
  label: c.label,
  matters: c.matters,
  thesis: c.thesis,
}));

const mattersOk = writeIfChanged(path.join(INDEX_DIR, "matters.json"), {
  generated: true,
  today,
  matters: indexMatters,
});
const clustersOk = writeIfChanged(path.join(INDEX_DIR, "clusters.json"), { clusters });

if (checkOnly) {
  if (!mattersOk || !clustersOk) process.exit(1);
  console.log(`OK — index/matters.json (${indexMatters.length} matters) and clusters.json are current.`);
  process.exit(0);
}

console.log(
  `Wrote index/matters.json (${indexMatters.length} matters) and index/clusters.json (${clusters.length} clusters).`,
);
