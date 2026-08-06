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
import crypto from "node:crypto";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { loadMatters, MATTERS_DIR } from "./load-matters.mjs";
import { MATTER_LIFECYCLES, archivedFromLifecycle } from "./matter-lifecycle.mjs";
import {
  MATTER_PHASES,
  MATTER_PROCEEDINGS,
  isPhaseAllowed,
} from "./matter-proceeding.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const PUBLIC_ROOT = path.join(REPO_ROOT, "internal", "public");
const DOCUMENTS_ROOT = path.join(PUBLIC_ROOT, "documents");
const DEADLINE_TIME_ZONE = "America/Los_Angeles";

const errors = [];
const warnings = [];

function fail(msg) {
  errors.push(msg);
}
function warn(msg) {
  warnings.push(msg);
}

function todayInTimeZone(timeZone) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(new Date());
  const value = Object.fromEntries(parts.map(({ type, value }) => [type, value]));
  return `${value.year}-${value.month}-${value.day}`;
}

function timelineDateKey(value) {
  const match = value.match(/^([A-Z][a-z]{2})\.\s+(\d{1,2}),\s+(\d{4})$/);
  if (!match) return null;
  const months = new Map([
    ["Jan", "01"], ["Feb", "02"], ["Mar", "03"], ["Apr", "04"],
    ["May", "05"], ["Jun", "06"], ["Jul", "07"], ["Aug", "08"],
    ["Sep", "09"], ["Oct", "10"], ["Nov", "11"], ["Dec", "12"],
  ]);
  const month = months.get(match[1]);
  return month ? `${match[3]}-${month}-${match[2].padStart(2, "0")}` : null;
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
const { insurance_coverage } = await import(pathToFileURL(path.join(REPO_ROOT, "internal/src/data/coverage.js")).href);

// ---------- matter JSON records ----------

const REQUIRED_MATTER_FIELDS = [
  ["number", "number"],
  ["caption", "string"],
  ["case_no", "string"],
  ["court", "string"],
  ["claims", "string"],
  ["status", "string"],
  ["lifecycle", "string"],
  ["proceeding", "string"],
  ["phase", "string"],
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
const LIFECYCLE_SET = new Set(MATTER_LIFECYCLES);
const PROCEEDING_SET = new Set(MATTER_PROCEEDINGS);
const PHASE_SET = new Set(MATTER_PHASES);
const TERMINAL_LIFECYCLES = new Set(["settled", "dismissed", "abandoned", "closed"]);

const seenMatterNumbers = new Set();
const matterRecords = new Map();
const referencedDocPaths = new Set();
let missingFiledCount = 0;

for (const m of cases) {
  matterRecords.set(m.number, m);
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

  if (typeof m.lifecycle === "string" && !LIFECYCLE_SET.has(m.lifecycle)) {
    fail(`${tag}: lifecycle "${m.lifecycle}" must be one of ${MATTER_LIFECYCLES.join(", ")}`);
  } else if (LIFECYCLE_SET.has(m.lifecycle)) {
    const expectedArchived = archivedFromLifecycle(m.lifecycle);
    if ("archived" in m && Boolean(m.archived) !== expectedArchived) {
      fail(
        `${tag}: archived=${Boolean(m.archived)} conflicts with lifecycle="${m.lifecycle}" ` +
          `(expected archived=${expectedArchived})`,
      );
    }
  }

  if (typeof m.proceeding === "string" && !PROCEEDING_SET.has(m.proceeding)) {
    fail(`${tag}: proceeding "${m.proceeding}" must be one of ${MATTER_PROCEEDINGS.join(", ")}`);
  }
  if (typeof m.phase === "string" && !PHASE_SET.has(m.phase)) {
    fail(`${tag}: phase "${m.phase}" must be one of ${MATTER_PHASES.join(", ")}`);
  }
  if (PROCEEDING_SET.has(m.proceeding) && PHASE_SET.has(m.phase) && !isPhaseAllowed(m.proceeding, m.phase)) {
    fail(`${tag}: phase "${m.phase}" is not allowed for proceeding "${m.proceeding}"`);
  }
  if (TERMINAL_LIFECYCLES.has(m.lifecycle) && m.phase !== "terminal") {
    fail(`${tag}: lifecycle "${m.lifecycle}" requires phase "terminal" (got "${m.phase}")`);
  }
  if (m.lifecycle === "pre_filing" && m.phase !== "pre_filing") {
    fail(`${tag}: lifecycle "pre_filing" requires phase "pre_filing" (got "${m.phase}")`);
  }
  if (m.lifecycle === "active" && m.phase === "terminal") {
    fail(`${tag}: lifecycle "active" cannot use phase "terminal"`);
  }
  if (m.lifecycle === "active" && m.phase === "pre_filing") {
    fail(`${tag}: lifecycle "active" should not use phase "pre_filing" (use lifecycle pre_filing)`);
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

const today = todayInTimeZone(DEADLINE_TIME_ZONE);
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
  if (t.upcoming === true) {
    const dateKey = typeof t.date === "string" ? timelineDateKey(t.date) : null;
    if (!dateKey) {
      fail(`${tag}: upcoming event date must use the format "Mon. D, YYYY"`);
    } else if (dateKey < today) {
      fail(`${tag}: past event is still marked upcoming (today is ${today} in ${DEADLINE_TIME_ZONE})`);
    }
  }
}

// ---------- cross-matter defendant references ----------
// If an archived matter shares a named defendant with an active matter, the
// active matter record should mention that related matter number somewhere in
// its prose (defendants, key_facts, procedural_status, or related_actions).

function relatedActionsText(m) {
  return [m.defendants, m.key_facts, m.procedural_status, m.damages, m.risk, m.caption].join(" ");
}

const GENERIC_DEFENDANT_WORDS = new Set([
  "state", "california", "county", "city", "officer", "sergeant", "deputy",
  "individual", "capacity", "official", "does", "inc", "llc", "corporation",
  "company", "services", "department", "program", "united", "district",
  "court", "superior", "director", "hearing", "dmv", "motor", "vehicle",
  "division", "board", "commission", "secretary", "warden", "sheriff",
  "police", "chief", "manager", "supervisor", "administrator", "agent",
  "parole", "probation", "corrections", "rehabilitation", "department",
  "bureau", "agency", "commissioner", "governor", "attorney", "general",
  "plaintiff", "defendant", "petitioner", "respondent", "doe", "does",
  "john", "jane", "richard", "roe", "unknown", "named", "unnamed",
  "successor", "predecessor", "assigns", "employees", "agents",
  "representatives", "successors", "predecessors", "all", "other",
  "persons", "entities", "acting", "capacity", "official", "individual",
]);

function defendantTokens(defs) {
  const text = typeof defs === "string" ? defs : "";
  const tokens = new Set();
  for (const chunk of text.split(/;|\band\b/)) {
    const trimmed = chunk.trim().replace(/^[\s.,]+|[\s.,]+$/g, "");
    // Prefer multi-word proper names (e.g. "Centerline Drivers", "FedEx Corporation")
    // and fall back to capitalized last names.
    const multi = trimmed.match(/[A-Z][a-zA-Z&]+(?:\s+[A-Z][a-zA-Z&]+)+/g) ?? [];
    for (const phrase of multi) {
      const words = phrase.split(/\s+/).filter((w) => !GENERIC_DEFENDANT_WORDS.has(w.toLowerCase()));
      if (words.length) tokens.add(words.join(" "));
    }
    const singles = trimmed.match(/[A-Z][a-zA-Z\-']{2,}/g) ?? [];
    for (const w of singles) {
      const low = w.toLowerCase();
      if (w.length < 4 || GENERIC_DEFENDANT_WORDS.has(low)) continue;
      tokens.add(w);
    }
  }
  return tokens;
}

const activeMatters = [...matterRecords.values()].filter((m) => m.lifecycle === "active");
const archivedMatters = [...matterRecords.values()].filter((m) => m.lifecycle !== "active");
const activeDefMap = new Map(activeMatters.map((m) => [m.number, defendantTokens(m.defendants)]));
const archivedDefMap = new Map(archivedMatters.map((m) => [m.number, defendantTokens(m.defendants)]));

for (const a of activeMatters) {
  const aTokens = activeDefMap.get(a.number) ?? new Set();
  for (const arc of archivedMatters) {
    const arcTokens = archivedDefMap.get(arc.number) ?? new Set();
    const shared = [...aTokens].filter((t) => arcTokens.has(t));
    if (shared.length === 0) continue;
    const haystack = relatedActionsText(a);
    if (!new RegExp(`\\bMatter ${String(arc.number).padStart(2, "0")}\\b`).test(haystack) &&
        !new RegExp(`\\b${arc.number}\\b`).test(haystack)) {
      warn(
        `Matter ${a.number} shares defendant(s) "${shared.join(", ")}" with archived Matter ${arc.number} ` +
        `but does not reference it in defendants/key_facts/procedural_status/damages/risk/caption. ` +
        `Consider adding a cross-reference to the cross-matter risk index.`,
      );
    }
  }
}

// ---------- timeline source citations ----------
// Timeline events should cite a source PDF so the record is verifiable.
const timelineWithoutSource = timeline.filter((t) => !t.source || typeof t.source !== "string" || !t.source.trim());
if (timelineWithoutSource.length) {
  warn(
    `${timelineWithoutSource.length}/${timeline.length} timeline events lack a "source" PDF citation. ` +
    `Add source paths as the audit pipeline is extended to each event.`,
  );
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

// ---------- insurance coverage ----------
// coverage.js is the source of truth for policy limits; the matter JSON carries
// a display string for its badge. These are rendered in different places, so a
// mismatch would silently show two different numbers for the same policy.

const coverageNumbers = new Set();
for (const record of insurance_coverage ?? []) {
  const { matter: n, limitsShort, perIncident, aggregate, policyNo, carrier, insureds } = record;

  if (coverageNumbers.has(n)) {
    fail(`coverage.js: duplicate entry for matter ${n}`);
  }
  coverageNumbers.add(n);

  const matterRecord = matterRecords.get(n);
  if (!matterRecord) {
    fail(`coverage.js: entry for matter ${n}, which has no matter JSON record`);
    continue;
  }
  if (matterRecord.policy_limits !== limitsShort) {
    fail(
      `coverage.js matter ${n}: limitsShort "${limitsShort}" does not match ` +
        `${matterRecord.__sourceFile} policy_limits "${matterRecord.policy_limits ?? "(unset)"}"`,
    );
  }
  if (!(Number.isFinite(perIncident) && perIncident > 0)) {
    fail(`coverage.js matter ${n}: perIncident must be a positive number`);
  }
  if (!(Number.isFinite(aggregate) && aggregate > 0)) {
    fail(`coverage.js matter ${n}: aggregate must be a positive number`);
  }
  if (Number.isFinite(perIncident) && Number.isFinite(aggregate) && perIncident > aggregate) {
    fail(`coverage.js matter ${n}: perIncident (${perIncident}) exceeds aggregate (${aggregate})`);
  }
  if (!policyNo || !carrier) {
    fail(`coverage.js matter ${n}: carrier and policyNo are required`);
  }
  if (!Array.isArray(insureds) || insureds.length === 0) {
    fail(`coverage.js matter ${n}: at least one insured must be named`);
  }
}

// A matter carrying policy_limits with no coverage.js record renders the small
// badge but never the tower — the leverage figure would be nearly invisible.
for (const m of matterRecords.values()) {
  if (m.policy_limits && !coverageNumbers.has(m.number)) {
    fail(`Matter ${m.number}: has policy_limits but no coverage.js record — add one so it renders portfolio-wide`);
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

// ---------- byte-identical duplicate documents (fail) ----------
// Two copies of the same filing inside one matter folder make the record
// ambiguous: half the links point at one copy, half at the other. Keep a
// single copy and reference that one.
const byDigest = new Map();
for (const full of onDiskDocs) {
  if (full.startsWith(formLibraryPrefix + path.sep) || full === formLibraryPrefix) continue;
  const digest = crypto.createHash("sha1").update(fs.readFileSync(full)).digest("hex");
  const key = `${path.dirname(full)}::${digest}`;
  if (!byDigest.has(key)) byDigest.set(key, []);
  byDigest.get(key).push(path.relative(PUBLIC_ROOT, full));
}
for (const copies of byDigest.values()) {
  if (copies.length > 1) {
    fail(`byte-identical duplicate document(s) in one matter folder: ${copies.join(" == ")}`);
  }
}




// ---------- cross-matter graph ----------

const crossMatter = JSON.parse(
  fs.readFileSync(path.join(REPO_ROOT, "internal/src/data/crossMatter.json"), "utf8"),
);

{
  const declaredKinds = new Set(Object.keys(crossMatter.linkKinds ?? {}));
  if (declaredKinds.size === 0) errors.push("crossMatter.json declares no link kinds.");
  for (const [kind, meta] of Object.entries(crossMatter.linkKinds ?? {})) {
    if (!meta?.label) errors.push(`crossMatter link kind ${kind} is missing a label.`);
    if (!meta?.description) errors.push(`crossMatter link kind ${kind} is missing a description.`);
  }

  const caseNumbers = new Set(cases.map((c) => c.number));
  const clusterIds = new Set();

  for (const cluster of crossMatter.clusters ?? []) {
    if (clusterIds.has(cluster.id)) errors.push(`crossMatter cluster id ${cluster.id} is duplicated.`);
    clusterIds.add(cluster.id);
    if (!cluster.label) errors.push(`crossMatter cluster ${cluster.id} is missing a label.`);
    if (!cluster.thesis || cluster.thesis.length < 80) {
      errors.push(`crossMatter cluster ${cluster.id} needs a substantive thesis.`);
    }
    if ((cluster.matters ?? []).length < 2) {
      errors.push(`crossMatter cluster ${cluster.id} must reference at least two matters.`);
    }

    const inCluster = new Set(cluster.matters ?? []);
    for (const number of cluster.matters ?? []) {
      if (!caseNumbers.has(number)) {
        errors.push(`crossMatter cluster ${cluster.id} references unknown matter ${number}.`);
      }
    }

    const linkIds = new Set();
    const linked = new Set();
    const validDirections = new Set(["mutual", "from_depends_on_to", "to_cites_from"]);
    const validSeverities = new Set(["high", "medium", "low"]);

    for (const link of cluster.links ?? []) {
      if (linkIds.has(link.id)) errors.push(`crossMatter link id ${link.id} is duplicated.`);
      linkIds.add(link.id);
      for (const endpoint of [link.from, link.to]) {
        if (!inCluster.has(endpoint)) {
          errors.push(`crossMatter link ${link.id} references matter ${endpoint} outside its cluster.`);
        }
      }
      if (link.from === link.to) errors.push(`crossMatter link ${link.id} links a matter to itself.`);
      if (!validDirections.has(link.direction)) {
        errors.push(`crossMatter link ${link.id} has invalid direction "${link.direction}".`);
      }
      if (!validSeverities.has(link.severity)) {
        errors.push(`crossMatter link ${link.id} has invalid severity "${link.severity}".`);
      }
      if (!(link.kinds ?? []).length) errors.push(`crossMatter link ${link.id} declares no kinds.`);
      for (const kind of link.kinds ?? []) {
        if (!declaredKinds.has(kind)) {
          errors.push(`crossMatter link ${link.id} uses undeclared kind "${kind}".`);
        }
      }
      if (!link.significance || link.significance.length < 60) {
        errors.push(`crossMatter link ${link.id} needs a substantive significance note.`);
      }
      if (!(link.sources ?? []).length) {
        errors.push(`crossMatter link ${link.id} cites no source filing.`);
      }
      linked.add(link.from);
      linked.add(link.to);
    }

    for (const number of cluster.matters ?? []) {
      if (!linked.has(number)) {
        errors.push(`crossMatter cluster ${cluster.id} lists matter ${number} with no documented link.`);
      }
    }

    const exposureIds = new Set();
    for (const exposure of cluster.exposures ?? []) {
      if (exposureIds.has(exposure.id)) {
        errors.push(`crossMatter exposure id ${exposure.id} is duplicated.`);
      }
      exposureIds.add(exposure.id);
      if (!exposure.remedy || exposure.remedy.length < 20) {
        errors.push(`crossMatter exposure ${exposure.id} has no actionable remedy.`);
      }
      if (!exposure.detail || exposure.detail.length < 60) {
        errors.push(`crossMatter exposure ${exposure.id} needs a substantive detail note.`);
      }
      if (!["open", "monitoring", "resolved"].includes(exposure.status)) {
        errors.push(`crossMatter exposure ${exposure.id} has invalid status "${exposure.status}".`);
      }
      if (!validSeverities.has(exposure.severity)) {
        errors.push(`crossMatter exposure ${exposure.id} has invalid severity "${exposure.severity}".`);
      }
      if (!(exposure.matters ?? []).length) {
        errors.push(`crossMatter exposure ${exposure.id} references no matters.`);
      }
      for (const number of exposure.matters ?? []) {
        if (!inCluster.has(number)) {
          errors.push(`crossMatter exposure ${exposure.id} references matter ${number} outside its cluster.`);
        }
      }
    }

    for (const item of cluster.foundation ?? []) {
      if (!item.label || !item.detail) {
        errors.push(`crossMatter foundation item ${item.id} needs a label and detail.`);
      }
      if ((item.matters ?? []).length < 2) {
        warnings.push(`crossMatter foundation item ${item.id} is shared by fewer than two matters.`);
      }
      for (const number of item.matters ?? []) {
        if (!inCluster.has(number)) {
          errors.push(`crossMatter foundation item ${item.id} references matter ${number} outside its cluster.`);
        }
      }
      if (item.document_path) {
        const full = path.join(REPO_ROOT, item.document_path.replace(/^\/+/, ""));
        if (!fs.existsSync(full)) {
          errors.push(`crossMatter foundation item ${item.id} cites a missing file ${item.document_path}.`);
        }
      }
    }

    for (const party of cluster.parties ?? []) {
      if (!party.name || !party.role) errors.push(`crossMatter cluster ${cluster.id} has a party missing name or role.`);
      const touches = [...(party.defendantIn ?? []), ...(party.factualIn ?? [])];
      if (!touches.length) {
        errors.push(`crossMatter party ${party.name} touches no matter in cluster ${cluster.id}.`);
      }
      for (const number of touches) {
        if (!inCluster.has(number)) {
          errors.push(`crossMatter party ${party.name} references matter ${number} outside its cluster.`);
        }
      }
    }
  }
}

// ---------- report ----------

console.log(
  `Checked ${cases.length} matter JSON records in ${path.relative(REPO_ROOT, MATTERS_DIR)}, ` +
    `${timeline.length} timeline entries, ` +
    `${(matter_damages ?? []).length} damages rows, ` +
    `${(lawyer_fees ?? []).length} lawyer-fee rows, ` +
    `${(outcomes.judicial_opinions ?? []).length} judicial opinions, ` +
    `${onDiskDocs.length} files under documents/, ` +
    `${(crossMatter.clusters ?? []).length} cross-matter cluster(s) with ` +
    `${(crossMatter.clusters ?? []).reduce((sum, c) => sum + (c.links ?? []).length, 0)} links.`,
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
