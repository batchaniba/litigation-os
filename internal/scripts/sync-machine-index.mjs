#!/usr/bin/env node
// Build the crawler index: one small file per concern, covering every matter.
//
//   node internal/scripts/sync-machine-index.mjs
//   node internal/scripts/sync-machine-index.mjs --check
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters, MATTERS_DIR } from "./load-matters.mjs";
import { todayKey } from "./lib/next-actions.mjs";
import { loadJsonIfPresent, paddedMatterNumber } from "./lib/matter-layout.mjs";
import { nextFromClocks } from "./lib/upcoming-from-clocks.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const INDEX_DIR = path.join(REPO_ROOT, "internal/src/data/index");
const CROSS_PATH = path.join(REPO_ROOT, "internal/src/data/crossMatter.json");
const checkOnly = process.argv.includes("--check");

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
  const { next_clock, overdue } = nextFromClocks(clocks, today);
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
    next_clock,
    overdue,
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
