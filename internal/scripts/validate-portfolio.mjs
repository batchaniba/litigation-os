#!/usr/bin/env node
// ==========================================================
// Portfolio integrity checker.
//
// Runs the checks that were previously done ad hoc, by hand, in
// individual sessions -- every documents[] path resolving to a real
// file, required fields present on each matter/timeline entry, and
// every timeline entry pointing at a matter number that actually
// exists. Exits non-zero (and prints every problem found, not just
// the first) if anything is wrong, so it can run in CI instead of
// depending on whoever happens to remember to check by hand.
//
// Usage: node internal/scripts/validate-portfolio.mjs
//        npm run validate
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const PUBLIC_ROOT = path.join(REPO_ROOT, "internal", "public");

const errors = [];
const warnings = [];

function fail(msg) {
  errors.push(msg);
}
function warn(msg) {
  warnings.push(msg);
}

const { cases } = await import(path.join(REPO_ROOT, "internal/src/data/matters.js"));
const { timeline } = await import(path.join(REPO_ROOT, "internal/src/data/timeline.js"));

// ---------- matters.js ----------

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

for (const m of cases) {
  const tag = `Matter ${m.number ?? "<no number>"} (${m.caption ?? "<no caption>"})`;

  if (m.number == null) {
    fail(`${tag}: missing required field "number"`);
  } else {
    if (seenMatterNumbers.has(m.number)) {
      fail(`Matter number ${m.number} is used more than once`);
    }
    seenMatterNumbers.add(m.number);
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
          }
        }
        if ("filed" in d && typeof d.filed !== "boolean") {
          fail(`${dtag}: "filed" should be boolean when present, got ${typeof d.filed}`);
        } else if (!("filed" in d)) {
          warn(`${dtag}: no "filed" field set (label: "${d.label}") -- status only lives in prose`);
        }
      }
    }
  }
}

// ---------- timeline.js ----------

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
        fail(`${tag}: references matter ${n}, which does not exist in matters.js`);
      }
    }
  }
  if ("upcoming" in t && typeof t.upcoming !== "boolean") {
    fail(`${tag}: "upcoming" should be boolean when present`);
  }
}

// ---------- report ----------

console.log(`Checked ${cases.length} matters, ${timeline.length} timeline entries.`);

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
