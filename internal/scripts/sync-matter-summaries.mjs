#!/usr/bin/env node
// ==========================================================
// Build light matter summaries for the SPA shell bundle.
//
// Full prose (status, key_facts, procedural_status, damages, risk, evidence)
// and document lists stay in NN.json (lazy-loaded on expand/detail).
// Document labels resolve through documents/registry.json (path is the id).
// Shell badges use status_label / effectiveStatusLabel instead of status.
// A slim document-index.json is generated for global search.
//
// Usage:
//   npm run sync:summaries           # write summaries + document-index
//   npm run sync:summaries -- --check  # exit 1 if out of date
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters, MATTERS_DIR } from "./load-matters.mjs";
import { loadRegistry, registryByPath, resolveDocumentRef } from "./lib/document-registry.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(MATTERS_DIR, "summaries.json");
const DOC_INDEX = path.join(MATTERS_DIR, "document-index.json");
const checkOnly = process.argv.includes("--check");
const registry = loadRegistry();
const registryPaths = registryByPath(registry);

const HEAVY = new Set([
  // Full procedural narrative — lazy-load with NN.json. Shell uses
  // status_label / effectiveStatusLabel instead.
  "status",
  "key_facts",
  "procedural_status",
  "damages",
  "risk",
  "evidence",
  "documents",
  "__sourceFile",
]);

function toSummary(matter) {
  const summary = {};
  for (const [key, value] of Object.entries(matter)) {
    if (HEAVY.has(key)) continue;
    summary[key] = value;
  }
  summary.evidenceCount = Array.isArray(matter.evidence) ? matter.evidence.length : 0;
  summary.documentCount = Array.isArray(matter.documents) ? matter.documents.length : 0;
  return summary;
}

function toDocIndex(matters) {
  const entries = [];
  for (const matter of matters) {
    for (const doc of matter.documents ?? []) {
      if (!doc?.path) continue;
      const resolved = resolveDocumentRef(doc, registryPaths);
      if (!resolved?.label) continue;
      entries.push({
        matter: matter.number,
        label: resolved.label,
        path: resolved.path,
      });
    }
  }
  return entries;
}

const matters = loadMatters();
const summaries = matters.map(toSummary);
const docIndex = toDocIndex(matters);
const summaryPayload = `${JSON.stringify(summaries, null, 2)}\n`;
const docPayload = `${JSON.stringify(docIndex, null, 2)}\n`;

function checkFile(filePath, expected, label) {
  if (!fs.existsSync(filePath)) {
    console.error(`Missing ${path.relative(process.cwd(), filePath)} — run npm run sync:summaries`);
    process.exit(1);
  }
  if (fs.readFileSync(filePath, "utf8") !== expected) {
    console.error(`${label} is stale — run npm run sync:summaries`);
    process.exit(1);
  }
}

if (checkOnly) {
  checkFile(OUT, summaryPayload, "internal/src/data/matters/summaries.json");
  checkFile(DOC_INDEX, docPayload, "internal/src/data/matters/document-index.json");
  console.log(
    `OK — summaries.json (${summaries.length} matters) and document-index.json (${docIndex.length} docs) are current.`,
  );
  process.exit(0);
}

fs.writeFileSync(OUT, summaryPayload);
fs.writeFileSync(DOC_INDEX, docPayload);
console.log(
  `Wrote ${path.relative(process.cwd(), OUT)} (${summaries.length} matters, ${summaryPayload.length} bytes) and ` +
    `${path.relative(process.cwd(), DOC_INDEX)} (${docIndex.length} docs, ${docPayload.length} bytes).`,
);
