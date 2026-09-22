#!/usr/bin/env node
// Scoped doc_kind gate. Classified files live in
// internal/src/data/index/doc-kind.json. Derived files may not assert a
// portfolio-wide matter count that disagrees with index/matters.json.
// Retired derived files are skipped for the count rule.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const CATALOG_REL = "internal/src/data/index/doc-kind.json";
const INDEX_REL = "internal/src/data/index/matters.json";
const KINDS = new Set(["derived", "runbook", "analysis"]);
const COUNT_RE = /\b(\d+)\s+(?:civil\s+)?[Mm]atters(?:\s+Portfolio)?\b/g;

const errors = [];

function fail(msg) {
  errors.push(msg);
}

function parseFrontMatter(text) {
  if (!text.startsWith("---\n") && !text.startsWith("---\r\n")) return null;
  const end = text.indexOf("\n---", 3);
  if (end < 0) return null;
  const block = text.slice(text.indexOf("\n") + 1, end);
  const out = {};
  for (const line of block.split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$/);
    if (!match) continue;
    out[match[1]] = match[2].trim().replace(/^['"]|['"]$/g, "");
  }
  return out;
}

const catalogPath = path.join(REPO_ROOT, CATALOG_REL);
if (!fs.existsSync(catalogPath)) {
  console.error(`missing ${CATALOG_REL}`);
  process.exit(1);
}

const catalog = JSON.parse(fs.readFileSync(catalogPath, "utf8"));
const index = JSON.parse(fs.readFileSync(path.join(REPO_ROOT, INDEX_REL), "utf8"));
const expectedCount = Array.isArray(index.matters) ? index.matters.length : 0;
if (!expectedCount) fail(`${INDEX_REL} has no matters[]`);

const seen = new Set();
for (const entry of catalog.docs ?? []) {
  const rel = entry.path;
  if (typeof rel !== "string" || !rel.startsWith("internal/docs/")) {
    fail(`doc-kind entry path must be under internal/docs/: ${JSON.stringify(rel)}`);
    continue;
  }
  if (seen.has(rel)) fail(`duplicate doc-kind path: ${rel}`);
  seen.add(rel);
  if (!KINDS.has(entry.doc_kind)) {
    fail(`${rel}: doc_kind "${entry.doc_kind}" must be derived | runbook | analysis`);
  }
  const abs = path.join(REPO_ROOT, rel);
  if (!fs.existsSync(abs)) {
    fail(`${rel}: classified but missing on disk`);
    continue;
  }
  const text = fs.readFileSync(abs, "utf8");
  const front = parseFrontMatter(text);
  if (front?.doc_kind && front.doc_kind !== entry.doc_kind) {
    fail(`${rel}: front matter doc_kind=${front.doc_kind} disagrees with catalog ${entry.doc_kind}`);
  }
  if (entry.doc_kind !== "derived" || entry.retired) continue;
  COUNT_RE.lastIndex = 0;
  for (const match of text.matchAll(COUNT_RE)) {
    const claimed = Number(match[1]);
    if (claimed !== expectedCount) {
      fail(
        `${rel}: derived doc claims "${match[0]}" but ${INDEX_REL} has ${expectedCount} matters`,
      );
    }
  }
}

if (errors.length) {
  console.error(`check-doc-kind: ${errors.length} error(s)`);
  for (const error of errors) console.error(`  ✗ ${error}`);
  process.exit(1);
}

console.log(
  `check-doc-kind: ${seen.size} classified docs, portfolio count ${expectedCount} — OK`,
);
