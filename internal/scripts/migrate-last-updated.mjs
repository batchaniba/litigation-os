#!/usr/bin/env node
// One-off schema migration: add "last_updated" (YYYY-MM-DD) to every matter
// identity record — the 39 legacy internal/src/data/matters/NN.json files and
// the split matter 24/matter.json. Byte-safe: inserts one line after the
// "number" key, preserving everything else verbatim. Idempotent.
//
//   node internal/scripts/migrate-last-updated.mjs [YYYY-MM-DD]
//   (defaults to today)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const MATTERS_DIR = path.join(REPO_ROOT, "internal/src/data/matters");

const arg = process.argv[2];
const stamp = arg && /^\d{4}-\d{2}-\d{2}$/.test(arg) ? arg : new Date().toISOString().slice(0, 10);

const targets = [];
for (let n = 1; n <= 40; n++) {
  const pad = String(n).padStart(2, "0");
  const legacy = path.join(MATTERS_DIR, `${pad}.json`);
  const split = path.join(MATTERS_DIR, String(n), "matter.json");
  if (fs.existsSync(split)) targets.push(split);
  else if (fs.existsSync(legacy)) targets.push(legacy);
  else console.error(`no identity record for matter ${n}`);
}

let updated = 0;
for (const file of targets) {
  const raw = fs.readFileSync(file, "utf8");
  if (raw.includes('"last_updated"')) {
    console.log(`skip (already stamped): ${path.relative(REPO_ROOT, file)}`);
    continue;
  }
  const next = raw.replace(
    /^(\s*"number"\s*:\s*\d+\s*,\s*)$/m,
    `$1\n  "last_updated": "${stamp}",`,
  );
  if (next === raw) {
    console.error(`NO NUMBER LINE — skipped: ${path.relative(REPO_ROOT, file)}`);
    continue;
  }
  fs.writeFileSync(file, next);
  updated++;
  console.log(`stamped: ${path.relative(REPO_ROOT, file)}`);
}
console.log(`done — ${updated} stamped, ${targets.length - updated} already had last_updated.`);
