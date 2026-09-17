#!/usr/bin/env node
// Seed the D1 tables from repo JSON. Emits idempotent INSERT statements to
// stdout — pipe to a file, then apply:
//
//   node seed.mjs > seed.sql
//   wrangler d1 execute litigation-portfolio --remote --file=seed.sql
//
// Sources (read-only; never writes to the repo):
//   - matters: split layout internal/src/data/matters/NN/{matter,clocks}.json
//     when present, otherwise the legacy internal/src/data/matters/NN.json.
//     next_clock_* columns come from internal/src/data/index/matters.json,
//     which already folds clocks.json-over-timeline precedence.
//   - documents: internal/src/data/documents/manifest.json (files[].sha256);
//     matter_number is parsed from /documents/matter-<n>/ paths.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const MATTERS_DIR = path.join(REPO_ROOT, "internal/src/data/matters");
const INDEX_PATH = path.join(REPO_ROOT, "internal/src/data/index/matters.json");
const MANIFEST_PATH = path.join(REPO_ROOT, "internal/src/data/documents/manifest.json");

const readJSON = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const pad = (n) => String(n).padStart(2, "0");
// SQL literal: numbers bare, strings single-quoted with '' escaping, nulls NULL.
const lit = (v) =>
  v === null || v === undefined
    ? "NULL"
    : typeof v === "number" && Number.isFinite(v)
      ? String(v)
      : `'${String(v).replace(/'/g, "''")}'`;

const index = readJSON(INDEX_PATH);
const idxByNumber = new Map((index.matters ?? []).map((m) => [Number(m.number), m]));
const manifest = readJSON(MANIFEST_PATH);

// Discover matter numbers from both layouts; split wins when both exist.
const numbers = new Set();
for (const entry of fs.readdirSync(MATTERS_DIR, { withFileTypes: true })) {
  const legacy = entry.name.match(/^(\d{2})\.json$/);
  if (entry.isFile() && legacy) numbers.add(Number(legacy[1]));
  const split = entry.name.match(/^(\d{2})$/);
  if (
    entry.isDirectory() &&
    split &&
    fs.existsSync(path.join(MATTERS_DIR, entry.name, "matter.json"))
  ) {
    numbers.add(Number(split[1]));
  }
}

const out = [];
out.push("-- D1 seed — generated from repo JSON. Idempotent (OR REPLACE / DELETE+INSERT).");

for (const n of [...numbers].sort((a, b) => a - b)) {
  const p = pad(n);
  const splitDir = path.join(MATTERS_DIR, p);
  let identity;
  let clocks = [];
  if (fs.existsSync(path.join(splitDir, "matter.json"))) {
    // Split layout (preferred).
    identity = readJSON(path.join(splitDir, "matter.json"));
    const clocksPath = path.join(splitDir, "clocks.json");
    if (fs.existsSync(clocksPath)) {
      const raw = readJSON(clocksPath);
      clocks = Array.isArray(raw) ? raw : (raw.clocks ?? []);
    }
  } else {
    // Legacy single-file layout.
    identity = readJSON(path.join(MATTERS_DIR, `${p}.json`));
  }

  const idx = idxByNumber.get(n) ?? {};
  const nc = idx.next_clock ?? {};
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

  // clocks: all split rows when present; otherwise the folded index next_clock.
  out.push(`DELETE FROM clocks WHERE matter_number = ${n};`);
  const rows = clocks.length ? clocks : nc.date ? [{ title: nc.title, date: nc.date, kind: nc.kind }] : [];
  for (const c of rows) {
    if (!c || !c.date) continue;
    out.push(
      `INSERT INTO clocks (matter_number, title, date, kind) VALUES (${n}, ${lit(c.title)}, ${lit(c.date)}, ${lit(c.kind ?? null)});`,
    );
  }
}

for (const f of manifest.files ?? []) {
  if (!f || !f.sha256) continue;
  const mm = String(f.path ?? "").match(/\/matter-(\d{1,2})\//);
  out.push(
    `INSERT OR REPLACE INTO documents (sha256, matter_number, path, size) VALUES (` +
      [lit(String(f.sha256).toLowerCase()), mm ? Number(mm[1]) : "NULL", lit(f.path), lit(f.size)].join(", ") +
      `);`,
  );
}

console.log(out.join("\n"));
