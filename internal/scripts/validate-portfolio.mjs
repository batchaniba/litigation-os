#!/usr/bin/env node
// ==========================================================
// Portfolio integrity checker.
//
// Validates matter JSON records, timeline references, cross-module
// coverage (damages / lawyer fees), document path existence, orphan
// files under public/documents, and outcomes opinion paths.
// Exits non-zero if any error is found (warnings are informational).
//
// Usage: node internal/scripts/validate-portfolio.mjs
//        npm run validate
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { loadMatters, MATTERS_DIR } from "./load-matters.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const PUBLIC_ROOT = path.join(REPO_ROOT, "internal", "public");
const DOCUMENTS_ROOT = path.join(PUBLIC_ROOT, "documents");

const errors = [];
const warnings = [];

function fail(msg) {
  errors.push(msg);
}
function warn(msg) {
  warnings.push(msg);
}

function walkFiles(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walkFiles(full));
    else if (entry.isFile() && !entry.name.startsWith(".")) out.push(full);
  }
  return out;
}

const cases = loadMatters();
const timeline = JSON.parse(
  fs.readFileSync(path.join(REPO_ROOT, "internal/src/data/timeline.json"), "utf8"),
);
const { matter_damages } = await import(pathToFileURL(path.join(REPO_ROOT, "internal/src/data/damages.js")).href);
const { lawyer_fees } = await import(pathToFileURL(path.join(REPO_ROOT, "internal/src/data/lawyerFees.js")).href);
const { outcomes } = await import(pathToFileURL(path.join(REPO_ROOT, "internal/src/data/outcomes.js")).href);

// ---------- matter JSON records ----------

const REQUIRED_MATTER_FIELDS = [
  ["number", "number"],
  ["caption", "string"],
  ["case_no", "string"],
  ["court", "string"],
  ["claims", "string"],
  ["status", "string"],
  ["filed", "string"],
  ["judge", "string"],
  ["cluster", "number"],
  ["type", "string"],
  ["defendants", "string"],
  ["key_facts", "string"],
  ["procedural_status", "string"],
  ["damages", "string"],
  ["risk", "string"],
];

const seenMatterNumbers = new Set();
const referencedDocPaths = new Set();
let missingFiledCount = 0;

for (const m of cases) {
  const source = m.__sourceFile ?? "?.json";
  const tag = `Matter ${m.number ?? "<no number>"} (${m.caption ?? "<no caption>"}) [${source}]`;
  const expectedName = `${String(m.number).padStart(2, "0")}.json`;

  if (m.number == null) {
    fail(`${tag}: missing required field "number"`);
  } else {
    if (seenMatterNumbers.has(m.number)) {
      fail(`Matter number ${m.number} is used more than once`);
    }
    seenMatterNumbers.add(m.number);
    if (source !== expectedName) {
      fail(`${tag}: file should be named ${expectedName}`);
    }
  }

  for (const [field, type] of REQUIRED_MATTER_FIELDS) {
    if (!(field in m)) {
      fail(`${tag}: missing required field "${field}"`);
    } else if (typeof m[field] !== type) {
      fail(`${tag}: field "${field}" should be ${type}, got ${typeof m[field]}`);
    }
  }

  if (m.causes !== undefined && !Array.isArray(m.causes)) {
    fail(`${tag}: field "causes" should be an array`);
  }
  if (m.evidence !== undefined && !Array.isArray(m.evidence)) {
    fail(`${tag}: field "evidence" should be an array`);
  }

  if (m.serviceTracking !== undefined) {
    if (!Array.isArray(m.serviceTracking)) {
      fail(`${tag}: field "serviceTracking" should be an array`);
    } else {
      for (const [i, s] of m.serviceTracking.entries()) {
        if (typeof s.name !== "string") fail(`${tag}: serviceTracking[${i}] missing string "name"`);
        if (typeof s.served !== "boolean") fail(`${tag}: serviceTracking[${i}] "served" should be boolean`);
      }
    }
  }

  if (m.documents !== undefined) {
    if (!Array.isArray(m.documents)) {
      fail(`${tag}: field "documents" should be an array`);
    } else {
      for (const [i, d] of m.documents.entries()) {
        const dtag = `${tag}, documents[${i}]`;
        if (typeof d.label !== "string" || !d.label.trim()) {
          fail(`${dtag}: missing/empty "label"`);
        }
        if (typeof d.path !== "string" || !d.path.trim()) {
          fail(`${dtag}: missing/empty "path"`);
        } else {
          if (!d.path.startsWith("/documents/")) {
            fail(`${dtag}: path "${d.path}" should start with "/documents/"`);
          }
          const onDisk = path.join(PUBLIC_ROOT, d.path);
          if (!fs.existsSync(onDisk)) {
            fail(`${dtag}: path does not resolve to a real file: ${d.path}`);
          } else {
            referencedDocPaths.add(path.resolve(onDisk));
          }
        }
        if ("filed" in d && typeof d.filed !== "boolean") {
          fail(`${dtag}: "filed" should be boolean when present, got ${typeof d.filed}`);
        } else if (!("filed" in d)) {
          missingFiledCount += 1;
        }
      }
    }
  }
}

// JSON files on disk that are not loadable matter records
const MATTERS_DIR_ALLOWLIST = new Set(["summaries.json", "document-index.json"]);
for (const name of fs.readdirSync(MATTERS_DIR)) {
  if (!name.endsWith(".json") || MATTERS_DIR_ALLOWLIST.has(name)) continue;
  if (!/^\d{2}\.json$/.test(name)) {
    fail(`matters/${name}: filename must be NN.json (zero-padded matter number)`);
  }
}

// ---------- timeline.json ----------

for (const [i, t] of timeline.entries()) {
  const tag = `timeline[${i}] (${t.date ?? "<no date>"})`;
  if (typeof t.date !== "string" || !t.date.trim()) fail(`${tag}: missing/empty "date"`);
  if (typeof t.event !== "string" || !t.event.trim()) fail(`${tag}: missing/empty "event"`);
  if (typeof t.type !== "string" || !t.type.trim()) fail(`${tag}: missing/empty "type"`);
  if (typeof t.matters !== "string") {
    fail(`${tag}: "matters" should be a string, got ${typeof t.matters}`);
  } else if (t.matters !== "All") {
    for (const raw of t.matters.split(",")) {
      const n = Number(raw.trim());
      if (Number.isNaN(n)) {
        fail(`${tag}: "matters" contains non-numeric entry "${raw.trim()}"`);
      } else if (!seenMatterNumbers.has(n)) {
        fail(`${tag}: references matter ${n}, which does not exist in matter JSON records`);
      }
    }
  }
  if ("upcoming" in t && typeof t.upcoming !== "boolean") {
    fail(`${tag}: "upcoming" should be boolean when present`);
  }
}

// ---------- damages / lawyer fees coverage ----------

const damageNumbers = new Set((matter_damages ?? []).map((d) => d.number));
const feeNumbers = new Set((lawyer_fees ?? []).map((f) => f.number));

for (const n of seenMatterNumbers) {
  if (!damageNumbers.has(n)) {
    warn(`Matter ${n}: no entry in damages.js matter_damages[]`);
  }
  if (!feeNumbers.has(n)) {
    warn(`Matter ${n}: no entry in lawyerFees.js lawyer_fees[]`);
  }
}

for (const d of matter_damages ?? []) {
  if (!seenMatterNumbers.has(d.number)) {
    fail(`damages.js matter_damages: references matter ${d.number}, which has no JSON record`);
  }
}
for (const f of lawyer_fees ?? []) {
  if (!seenMatterNumbers.has(f.number)) {
    fail(`lawyerFees.js: references matter ${f.number}, which has no JSON record`);
  }
}

// ---------- outcomes paths ----------

function checkOutcomePath(tag, p) {
  if (typeof p !== "string" || !p.trim()) return;
  if (!p.startsWith("/documents/")) {
    fail(`${tag}: path "${p}" should start with "/documents/"`);
    return;
  }
  const onDisk = path.join(PUBLIC_ROOT, p);
  if (!fs.existsSync(onDisk)) {
    fail(`${tag}: path does not resolve to a real file: ${p}`);
  } else {
    referencedDocPaths.add(path.resolve(onDisk));
  }
}

for (const [i, op] of (outcomes.judicial_opinions ?? []).entries()) {
  const tag = `outcomes.judicial_opinions[${i}] (matter ${op.matter ?? "?"})`;
  if (op.matter != null && !seenMatterNumbers.has(op.matter)) {
    fail(`${tag}: references matter ${op.matter}, which has no JSON record`);
  }
  checkOutcomePath(`${tag}.document_path`, op.document_path);
  checkOutcomePath(`${tag}.objections_path`, op.objections_path);
  checkOutcomePath(`${tag}.nsa_path`, op.nsa_path);
}

// ---------- filed-field + orphan document summaries (warn) ----------

if (missingFiledCount > 0) {
  warn(
    `${missingFiledCount} documents[] entries omit boolean "filed" (status lives only in prose labels)`,
  );
}

const onDiskDocs = walkFiles(DOCUMENTS_ROOT).map((p) => path.resolve(p));
const formLibraryPrefix = path.resolve(path.join(DOCUMENTS_ROOT, "_form-library"));
const orphans = [];
for (const full of onDiskDocs) {
  if (full.startsWith(formLibraryPrefix + path.sep) || full === formLibraryPrefix) continue;
  if (!referencedDocPaths.has(full)) {
    orphans.push(path.relative(PUBLIC_ROOT, full));
  }
}
if (orphans.length) {
  const preview = orphans.slice(0, 15);
  warn(`${orphans.length} orphan document(s) on disk not referenced in matters/outcomes:`);
  for (const rel of preview) warn(`  - ${rel}`);
  if (orphans.length > preview.length) {
    warn(`  …and ${orphans.length - preview.length} more`);
  }
}

// ---------- report ----------

console.log(
  `Checked ${cases.length} matter JSON records in ${path.relative(REPO_ROOT, MATTERS_DIR)}, ` +
    `${timeline.length} timeline entries, ` +
    `${(matter_damages ?? []).length} damages rows, ` +
    `${(lawyer_fees ?? []).length} lawyer-fee rows, ` +
    `${(outcomes.judicial_opinions ?? []).length} judicial opinions, ` +
    `${onDiskDocs.length} files under documents/.`,
);

if (warnings.length) {
  console.log(`\n${warnings.length} warning(s):`);
  for (const w of warnings) console.log(`  ⚠ ${w}`);
}

if (errors.length) {
  console.log(`\n${errors.length} error(s):`);
  for (const e of errors) console.log(`  ✗ ${e}`);
  console.log(`\nFAILED`);
  process.exit(1);
} else {
  console.log(`\nOK — no errors.`);
}
