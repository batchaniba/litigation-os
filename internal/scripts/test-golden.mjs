#!/usr/bin/env node
// Golden-file test for damages math.
// Usage: node internal/scripts/test-golden.mjs
// Compares computed aggregates against internal/scripts/__golden__/damages.json.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GOLDEN = path.join(__dirname, "__golden__", "damages.json");

// Import the damages table (strip the import of matterIdentity)
const damagesPath = path.resolve(__dirname, "../src/data/damages.js");
let damagesSrc = fs.readFileSync(damagesPath, "utf8");
// Replace the import with a stub
damagesSrc = damagesSrc.replace(
  /import \{ withMatterIdentity \} from "[^"]+";/,
  "const withMatterIdentity = (x) => x;"
);
const tmpPath = path.join(__dirname, "__golden__", "_damages_tmp.mjs");
fs.writeFileSync(tmpPath, damagesSrc);
const { damages_table } = await import(tmpPath);
fs.unlinkSync(tmpPath);

const totals = { conservative: 0, moderate: 0, aggressive: 0 };
for (const row of damages_table) {
  totals.conservative += row.conservative;
  totals.moderate += row.moderate;
  totals.aggressive += row.aggressive;
}

const golden = JSON.parse(fs.readFileSync(GOLDEN, "utf8"));
let failed = 0;

for (const k of ["conservative", "moderate", "aggressive"]) {
  if (totals[k] !== golden.damages_totals[k]) {
    console.error(`✗ damages.${k}: got ${totals[k]}, golden has ${golden.damages_totals[k]}`);
    failed++;
  }
}
if (damages_table.length !== golden.damages_row_count) {
  console.error(`✗ row count: got ${damages_table.length}, golden has ${golden.damages_row_count}`);
  failed++;
}

if (failed) {
  console.error(`\n${failed} golden mismatch(es). If intentional, regenerate: node internal/scripts/generate-golden.mjs`);
  process.exit(1);
}
console.log(`✓ damages golden file matches (${damages_table.length} rows, totals verified)`);
