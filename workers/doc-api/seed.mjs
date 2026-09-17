#!/usr/bin/env node
// Seed the D1 tables from repo JSON. Emits idempotent INSERT statements to
// stdout — pipe to a file, then apply on the laptop:
//
//   node seed.mjs > seed.sql
//   wrangler d1 execute litigation-portfolio --remote --file=schema.sql
//   wrangler d1 execute litigation-portfolio --remote --file=seed.sql
//
// Sources (read-only; never writes to the repo):
//   - matters: split layout internal/src/data/matters/NN/{matter,clocks}.json
//   - next_clock_*: soonest clock whose status is not satisfied/retired/cancelled/vacated
//   - documents_by_path: one row per manifest path (aliases keep their own row)

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const MATTERS_DIR = path.join(REPO_ROOT, "internal/src/data/matters");
const INDEX_PATH = path.join(REPO_ROOT, "internal/src/data/index/matters.json");
const MANIFEST_PATH = path.join(REPO_ROOT, "internal/src/data/documents/manifest.json");

const CLOSED_CLOCK = new Set(["satisfied", "retired", "cancelled", "canceled", "vacated"]);

const readJSON = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const pad = (n) => String(n).padStart(2, "0");
const lit = (v) =>
  v === null || v === undefined
    ? "NULL"
    : typeof v === "number" && Number.isFinite(v)
      ? String(v)
      : `'${String(v).replace(/'/g, "''")}'`;

const nextOpenClock = (clocks) => {
  const open = (clocks ?? []).filter(
    (c) => c && c.date && !CLOSED_CLOCK.has(String(c.status ?? "open").toLowerCase()),
  );
  open.sort(
    (a, b) => String(a.date).localeCompare(String(b.date)) || String(a.title ?? "").localeCompare(String(b.title ?? "")),
  );
  return open[0] ?? null;
};

const index = readJSON(INDEX_PATH);
const idxByNumber = new Map((index.matters ?? []).map((m) => [Number(m.number), m]));
const manifest = readJSON(MANIFEST_PATH);

const numbers = new Set();
for (const entry of fs.readdirSync(MATTERS_DIR, { withFileTypes: true })) {
  const legacy = entry.name.match(/^(\d{2})\.json$/);
  if (entry.isFile() && legacy) numbers.add(Number(legacy[1]));
  const split = entry.name.match(/^(\d{2})$/);
  if (
    entry.isDirectory() &&
    split &&
    fs.existsSync(path.join(splitDir(split[1]), "matter.json"))
  ) {
    numbers.add(Number(split[1]));
  }
}

function splitDir(p) {
  return path.join(MATTERS_DIR, String(p).padStart(2, "0"));
}

const out = [];
out.push("-- D1 seed — generated from repo JSON. Idempotent.");
out.push("DELETE FROM clocks;");
out.push("DELETE FROM documents_by_path;");

for (const n of [...numbers].sort((a, b) => a - b)) {
  const p = pad(n);
  const dir = path.join(MATTERS_DIR, p);
  let identity;
  let clocks = [];
  if (fs.existsSync(path.join(dir, "matter.json"))) {
    identity = readJSON(path.join(dir, "matter.json"));
    const clocksPath = path.join(dir, "clocks.json");
    if (fs.existsSync(clocksPath)) {
      const raw = readJSON(clocksPath);
      clocks = Array.isArray(raw) ? raw : (raw.clocks ?? []);
    }
  } else {
    identity = readJSON(path.join(MATTERS_DIR, `${p}.json`));
  }

  const idx = idxByNumber.get(n) ?? {};
  const computed = nextOpenClock(clocks);
  const nc = computed
    ? { title: computed.title, date: computed.date }
    : (idx.next_clock ?? {});
  out.push(
    `INSERT OR REPLACE INTO matters (number, caption, case_no, court, phase, status_label, judge, next_clock_title, next_clock_date, lifecycle) VALUES (` +
      [
        n,
        lit(identity.caption ?? idx.caption),
        lit(identity.case_no ?? idx.case_no),
        lit(identity.court ?? idx.court),
        lit(identity.phase ?? idx.phase),
        lit(identity.status_label),
        lit(identity.judge ?? idx.judge),
        lit(nc.title),
        lit(nc.date),
        lit(identity.lifecycle ?? idx.lifecycle),
      ].join(", ") +
      `);`,
  );

  for (const c of clocks) {
    if (!c || !c.date) continue;
    out.push(
      `INSERT INTO clocks (matter_number, title, date, kind, status) VALUES (${n}, ${lit(c.title)}, ${lit(c.date)}, ${lit(c.kind ?? null)}, ${lit(c.status ?? "open")});`,
    );
  }
}

for (const f of manifest.files ?? []) {
  if (!f || !f.sha256 || !f.path) continue;
  const mm = String(f.path).match(/\/matter-(\d{1,2})\//);
  const sha = String(f.sha256).toLowerCase();
  out.push(
    `INSERT OR REPLACE INTO documents_by_path (path, sha256, matter_number, size) VALUES (` +
      [lit(f.path), lit(sha), mm ? Number(mm[1]) : "NULL", lit(f.size)].join(", ") +
      `);`,
  );
  // Legacy row: last alias at this hash wins. Path lookups must use documents_by_path.
  out.push(
    `INSERT OR REPLACE INTO documents (sha256, matter_number, path, size) VALUES (` +
      [lit(sha), mm ? Number(mm[1]) : "NULL", lit(f.path), lit(f.size)].join(", ") +
      `);`,
  );
}

console.log(out.join("\n"));
