#!/usr/bin/env node
// ==========================================================
// Build light matter summaries for the SPA shell bundle.
//
// Full prose (key_facts, procedural_status, damages, risk, evidence)
// stays in NN.json and is lazy-loaded on matter expand/detail.
//
// Usage:
//   npm run sync:summaries           # write summaries.json
//   npm run sync:summaries -- --check  # exit 1 if out of date
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters, MATTERS_DIR } from "./load-matters.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(MATTERS_DIR, "summaries.json");
const checkOnly = process.argv.includes("--check");

const HEAVY = new Set(["key_facts", "procedural_status", "damages", "risk", "evidence", "__sourceFile"]);

function toSummary(matter) {
  const summary = {};
  for (const [key, value] of Object.entries(matter)) {
    if (HEAVY.has(key)) continue;
    summary[key] = value;
  }
  summary.evidenceCount = Array.isArray(matter.evidence) ? matter.evidence.length : 0;
  if (Array.isArray(matter.documents)) {
    summary.documents = matter.documents.map((doc) => {
      const next = { label: doc.label, path: doc.path };
      if ("filed" in doc) next.filed = doc.filed;
      return next;
    });
  }
  return summary;
}

const summaries = loadMatters().map(toSummary);
const payload = `${JSON.stringify(summaries, null, 2)}\n`;

if (checkOnly) {
  if (!fs.existsSync(OUT)) {
    console.error(`Missing ${path.relative(process.cwd(), OUT)} — run npm run sync:summaries`);
    process.exit(1);
  }
  const current = fs.readFileSync(OUT, "utf8");
  if (current !== payload) {
    console.error("internal/src/data/matters/summaries.json is stale — run npm run sync:summaries");
    process.exit(1);
  }
  console.log(`OK — summaries.json is current (${summaries.length} matters).`);
  process.exit(0);
}

fs.writeFileSync(OUT, payload);
console.log(`Wrote ${path.relative(process.cwd(), OUT)} (${summaries.length} matters, ${payload.length} bytes).`);
