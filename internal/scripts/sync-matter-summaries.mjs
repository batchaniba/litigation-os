#!/usr/bin/env node
// ==========================================================
// Build the filing-safe SPA snapshots from the single publish projection.
//
//   summaries.json          — shell list/search identity
//   document-index.json     — public filed / phone-tap PDFs only
//   publish/NN.json         — lazy matter records (same shape as D1 seed)
//
// Full prose stays in the split laptop folders. Do not glob those into Vite.
//
// Usage:
//   npm run sync:summaries           # write summaries + publish records
//   npm run sync:summaries -- --check  # exit 1 if out of date
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters, MATTERS_DIR } from "./load-matters.mjs";
import { listMatterSources } from "./lib/matter-layout.mjs";
import {
  REPO_ROOT,
  labelFromPublicPath,
  loadPhoneTapPaths,
  publishDir,
  publishMatterFromDir,
} from "./lib/publish-matter.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(MATTERS_DIR, "summaries.json");
const DOC_INDEX = path.join(MATTERS_DIR, "document-index.json");
const PUBLISH_ROOT = path.join(MATTERS_DIR, "publish");
const checkOnly = process.argv.includes("--check");

// Validate the laptop graph first (schema), then project.
loadMatters();

const phoneTapPaths = loadPhoneTapPaths(REPO_ROOT);
const sources = listMatterSources(MATTERS_DIR).filter((source) => source.layout === "split");
const publishedMatters = sources.map((source) => publishMatterFromDir(source.dir, { phoneTapPaths }));

function toSummary(published) {
  const { docket: _docket, clocks: _clocks, documents, people: _people, ...identity } = published;
  return {
    ...identity,
    evidenceCount: 0,
    documentCount: Array.isArray(documents) ? documents.length : 0,
  };
}

function toDocIndex(publishedList) {
  const entries = [];
  for (const published of publishedList) {
    for (const doc of published.documents ?? []) {
      if (!doc?.path) continue;
      entries.push({
        matter: published.number,
        label: labelFromPublicPath(doc.path),
        path: doc.path,
      });
    }
  }
  return entries;
}

const summaries = publishedMatters.map(toSummary);
const docIndex = toDocIndex(publishedMatters);
const summaryPayload = `${JSON.stringify(summaries, null, 2)}\n`;
const docPayload = `${JSON.stringify(docIndex, null, 2)}\n`;
const publishPayloads = publishedMatters.map((published) => ({
  filePath: publishDir(MATTERS_DIR, published.number),
  body: `${JSON.stringify(published, null, 2)}\n`,
}));

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
  for (const { filePath, body } of publishPayloads) {
    checkFile(filePath, body, path.relative(process.cwd(), filePath));
  }
  console.log(
    `OK — summaries.json (${summaries.length} matters), document-index.json (${docIndex.length} public docs), ` +
      `and publish/${publishedMatters.length} records are current.`,
  );
  process.exit(0);
}

fs.mkdirSync(PUBLISH_ROOT, { recursive: true });
const keep = new Set(publishPayloads.map((row) => path.basename(row.filePath)));
for (const name of fs.readdirSync(PUBLISH_ROOT)) {
  if (name.endsWith(".json") && !keep.has(name)) {
    fs.unlinkSync(path.join(PUBLISH_ROOT, name));
  }
}

fs.writeFileSync(OUT, summaryPayload);
fs.writeFileSync(DOC_INDEX, docPayload);
for (const { filePath, body } of publishPayloads) {
  fs.writeFileSync(filePath, body);
}
console.log(
  `Wrote ${path.relative(process.cwd(), OUT)} (${summaries.length} matters, ${summaryPayload.length} bytes), ` +
    `${path.relative(process.cwd(), DOC_INDEX)} (${docIndex.length} public docs, ${docPayload.length} bytes), ` +
    `and ${publishPayloads.length} publish records.`,
);
