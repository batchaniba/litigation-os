#!/usr/bin/env node
// Write internal/scripts/__golden__/damages.json from the current damages table.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const GOLDEN = path.join(__dirname, "__golden__", "damages.json");
const damagesPath = path.resolve(__dirname, "../src/data/damages.js");
let damagesSrc = fs.readFileSync(damagesPath, "utf8");
damagesSrc = damagesSrc.replace(
  /import \{ withMatterIdentity \} from "[^"]+";/,
  "const withMatterIdentity = (x) => x;",
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

const payload = {
  generated: new Date().toISOString().slice(0, 10),
  damages_totals: totals,
  damages_row_count: damages_table.length,
  note: "If this test fails, the damages math or data changed. Update the golden file intentionally via: node internal/scripts/generate-golden.mjs",
};
fs.writeFileSync(GOLDEN, `${JSON.stringify(payload, null, 2)}\n`);
console.log(
  `Wrote ${path.relative(path.resolve(__dirname, "../.."), GOLDEN)} ` +
    `(${damages_table.length} rows; ${totals.conservative}/${totals.moderate}/${totals.aggressive}).`,
);
