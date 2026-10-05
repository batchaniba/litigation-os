#!/usr/bin/env node
// Evidence-tied valuation sheet for one matter.
//
//   npm run valuation -- --matter 25
//   npm run valuation -- --matter 25 --json
//
// Reads internal/private/negotiation/NN.valuation.json (proof map, damages
// lines with probabilities, positions) and the walk-away from NN.jsonl.
// Exit 1 if the file is malformed or no walk-away is recorded; exit 2 on usage.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { LEDGER_DIR, parseLedger } from "./lib/negotiation.mjs";
import { computeValuation, formatValuation, validateValuation } from "./lib/valuation.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const args = process.argv.slice(2);
const i = args.indexOf("--matter");
const matter = i >= 0 ? args[i + 1] : null;
if (!matter || !/^\d{1,2}$/.test(matter)) {
  process.stderr.write("valuation: --matter NN is required\n");
  process.exit(2);
}
const nn = matter.padStart(2, "0");
const vFile = path.join(ROOT, LEDGER_DIR, `${nn}.valuation.json`);
if (!fs.existsSync(vFile)) {
  process.stderr.write(`valuation: no ${path.relative(ROOT, vFile)} yet\n`);
  process.exit(2);
}
const v = JSON.parse(fs.readFileSync(vFile, "utf8"));
const errors = validateValuation(v);
if (errors.length) {
  process.stderr.write(`valuation: ${path.relative(ROOT, vFile)} has problems:\n${errors.map((e) => `  ✗ ${e}`).join("\n")}\n`);
  process.exit(1);
}
const lFile = path.join(ROOT, LEDGER_DIR, `${nn}.jsonl`);
const ledger = fs.existsSync(lFile) ? parseLedger(fs.readFileSync(lFile, "utf8"), path.relative(ROOT, lFile)) : [];
const walk = ledger.filter((m) => m.kind === "walkaway" && (m.scope ?? "global") === "global").at(-1);
const c = computeValuation(v, { walkaway: walk?.amount ?? null });

if (args.includes("--json")) process.stdout.write(`${JSON.stringify(c, null, 2)}\n`);
else process.stdout.write(`${formatValuation(v, c)}\n`);
process.exit(c.findings.some((f) => f.level === "block") ? 1 : 0);
