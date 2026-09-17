#!/usr/bin/env node
// Split a legacy NN.json into NN/{matter,docket,clocks,parties,counsel,claims,damages,evidence,documents,events,prose}.
// Any matter, whenever it is touched. Not cluster-gated. Does not invent docket numbers.
// docket.json is pleadings. documents.json is the file inventory.
// events.jsonl is append-only after the first split.
//
//   node internal/scripts/split-matter.mjs 32
//   node internal/scripts/split-matter.mjs 32 --replace
//   node internal/scripts/split-matter.mjs --all
//   node internal/scripts/split-matter.mjs 24 --trim-docket
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { MATTERS_DIR } from "./load-matters.mjs";
import { dateKeyFromLabel } from "./lib/next-actions.mjs";
import {
  EVENTS_FILE,
  inferDocketNumber,
  paddedMatterNumber,
} from "../src/data/matters/assembleMatter.js";
import {
  isSplitMatterDir,
  legacyMatterPath,
  splitMatterDir,
  writeJson,
} from "./lib/matter-layout.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const TIMELINE_PATH = path.join(REPO_ROOT, "internal/src/data/timeline.json");

const IDENTITY_KEYS = [
  "number",
  "caption",
  "case_no",
  "former_case_no",
  "court",
  "courtlistener",
  "claims",
  "status",
  "status_label",
  "lifecycle",
  "proceeding",
  "phase",
  "filed",
  "judge",
  "judge_id",
  "cluster",
  "related",
  "same_incident",
  "type",
  "badge",
  "archived",
  "note",
  "key_facts",
  "procedural_status",
];

const CLOCK_TITLE_CHARS = 160;

function parseArgs(argv) {
  const replace = argv.includes("--replace");
  const all = argv.includes("--all");
  const trimDocket = argv.includes("--trim-docket");
  const rebuild = argv.includes("--rebuild-from-inventory");
  const number = Number(argv.find((a) => /^\d+$/.test(a)));
  return { replace, all, trimDocket, rebuild, number };
}

function guessFiler(title, filed) {
  const t = String(title ?? "").toLowerCase();
  if (/\b(defendant|respondents?|dag|ag |motion to dismiss|demurrer|reply iso)\b/.test(t)) {
    return "defendant";
  }
  if (/\b(clerk|court|order|notice resetting|reassign)/.test(t) && !/\bplaintiff/.test(t)) {
    return "court";
  }
  if (filed === false && /\b(draft|email_draft|gmail)\b/i.test(t)) return "plaintiff";
  return "plaintiff";
}

function guessDocType(title, dkt) {
  const t = String(title ?? "").toLowerCase();
  if (/\bfirst amended complaint|\bfac\b/.test(t)) return "amended_complaint";
  if (/\bcomplaint\b/.test(t) && dkt === 1) return "complaint";
  if (/\bmotion to dismiss|\bmtd\b/.test(t)) return "motion_to_dismiss";
  if (/\bopposition\b/.test(t)) return "opposition";
  if (/\breply\b/.test(t)) return "reply";
  if (/\border\b/.test(t)) return "order";
  if (/\bsummons\b/.test(t)) return "summons";
  if (/\bproof of service|\bpos\b/.test(t)) return "proof_of_service";
  if (/\bstipulation\b/.test(t)) return "stipulation";
  if (/\bgmail\b|\bemail\b/.test(t)) return "correspondence";
  return "other";
}

function packetFlag(docPath) {
  if (/4-26-cv-05953-ASK/i.test(docPath)) return "ask-packet";
  if (/3-26-cv-05953-CRB/i.test(docPath)) return "crb-packet";
  return null;
}

function oneLiner(text, max = CLOCK_TITLE_CHARS) {
  const s = String(text ?? "").replace(/\s+/g, " ").trim();
  if (!s) return "";
  if (s.length <= max) return s;
  return `${s.slice(0, max).replace(/\s+\S*$/, "")}…`;
}

function isPleadingDocument(doc) {
  const docPath = String(doc.path ?? "");
  const title = path.posix.basename(docPath).replace(/\.[^.]+$/, "");
  if (/\.(jpe?g|png|gif|webp)$/i.test(docPath)) return false;
  if (/EMAIL_DRAFT|Mailing Photo/i.test(title)) return false;
  const dkt = inferDocketNumber(docPath, title);
  if (Number.isInteger(dkt)) return true;
  if (doc.filed === true) return true;
  if (packetFlag(docPath)) return true;
  if (
    /\b(complaint|motion|opposition|order|summons|stipulation|proof of service|notice of errata|amended complaint|reply)\b/i.test(
      title,
    ) &&
    !/\bdraft\b/i.test(title)
  ) {
    return true;
  }
  return false;
}

function toInventoryRow(doc) {
  const ref = { path: doc.path };
  if (typeof doc.filed === "boolean") ref.filed = doc.filed;
  if (typeof doc.label === "string" && doc.label.trim()) ref.label = doc.label.trim();
  return ref;
}

function toDocketRow(doc) {
  const title = path.posix.basename(doc.path).replace(/\.[^.]+$/, "");
  const dkt = inferDocketNumber(doc.path, title);
  const packet = packetFlag(doc.path);
  const row = {
    dkt,
    date: null,
    filer: guessFiler(title, doc.filed),
    type: guessDocType(title, dkt),
    title,
    path: doc.path,
    filed: typeof doc.filed === "boolean" ? doc.filed : Boolean(dkt),
  };
  if (dkt === 10 && row.type === "amended_complaint") row.operative = true;
  if (packet) {
    row.packet = packet;
    if (packet === "ask-packet") {
      row.superseded_by = "crb-packet";
      row.operative = false;
    }
  }
  return row;
}

function toEvidenceRow(item, index) {
  if (typeof item !== "string") return item;
  return {
    id: `e${String(index + 1).padStart(2, "0")}`,
    label: item,
    path: null,
    what_it_proves: item,
    transcript_path: null,
  };
}

function toClocks(timeline, number) {
  return timeline
    .filter((row) => Array.isArray(row.matters) && row.matters.includes(number) && row.upcoming === true)
    .map((row, i) => {
      const date = dateKeyFromLabel(row.date);
      return {
        id: `${paddedMatterNumber(number)}-${row.type ?? "event"}-${i + 1}`,
        date,
        date_label: row.date ?? null,
        kind: row.type ?? "event",
        status: date ? "open" : "undated",
        source_dkt: inferDocketNumber(row.source ?? "", row.event ?? ""),
        title: oneLiner(row.event ?? ""),
        actor: row.actor ?? null,
        source: row.source ?? null,
      };
    });
}

function toEvents(timeline, number) {
  return timeline
    .filter((row) => Array.isArray(row.matters) && row.matters.includes(number))
    .map((row) => {
      const date = dateKeyFromLabel(row.date);
      const event = {
        ts: date ? `${date}T00:00:00-07:00` : null,
        date: row.date ?? null,
        matter: number,
        matters: row.matters,
        type: row.type ?? "event",
        title: String(row.event ?? ""),
        path: row.source ?? null,
        dkt: inferDocketNumber(row.source ?? "", row.event ?? ""),
      };
      if (row.upcoming === true) event.upcoming = true;
      if (typeof row.filed === "boolean") event.filed = row.filed;
      if (row.actor) event.actor = row.actor;
      if (row.source_type) event.source_type = row.source_type;
      if (row.external) event.external = row.external;
      return event;
    });
}

function slimMatter(raw) {
  const out = {};
  for (const key of IDENTITY_KEYS) {
    if (raw[key] !== undefined) out[key] = raw[key];
  }
  out.procedural_status =
    "Canonical chronology is clocks.json, docket.json, and events.jsonl. Do not reconstruct dates from README.";
  return out;
}

function writeSplit(number, raw, timeline, { replace }) {
  const src = legacyMatterPath(MATTERS_DIR, number);
  const dest = splitMatterDir(MATTERS_DIR, number);
  const inventory = (raw.documents ?? []).map(toInventoryRow).filter((row) => row.path);
  const docket = (raw.documents ?? []).filter(isPleadingDocument).map(toDocketRow);
  const evidence = (raw.evidence ?? []).map(toEvidenceRow);
  const clocks = toClocks(timeline, number);
  const events = toEvents(timeline, number);

  const parties = {
    defendants_label: raw.defendants ?? "",
    serviceTracking: raw.serviceTracking ?? [],
  };
  const counsel = {
    appearances: (raw.opposing_counsel ?? []).map((row) => ({
      id: null,
      name: row.name,
      firm: row.firm ?? null,
      dossier: row.dossier ?? null,
      attorney_id: row.attorney_id ?? null,
    })),
  };
  const claims = {
    summary: raw.claims ?? "",
    counts: (raw.causes ?? []).map((title, i) => ({
      id: i + 1,
      status: "live",
      theory_ids: [],
      title,
    })),
  };
  const damages = {
    narrative: raw.damages ?? "",
    risk: raw.risk ?? "",
  };
  const prose = {
    status: raw.status ?? "",
    key_facts: raw.key_facts ?? "",
    procedural_status: raw.procedural_status ?? "",
    damages: raw.damages ?? "",
    risk: raw.risk ?? "",
  };

  fs.mkdirSync(dest, { recursive: true });
  writeJson(path.join(dest, "matter.json"), slimMatter(raw));
  writeJson(path.join(dest, "docket.json"), docket);
  writeJson(path.join(dest, "documents.json"), inventory);
  writeJson(path.join(dest, "clocks.json"), clocks);
  writeJson(path.join(dest, "parties.json"), parties);
  writeJson(path.join(dest, "counsel.json"), counsel);
  writeJson(path.join(dest, "claims.json"), claims);
  writeJson(path.join(dest, "damages.json"), damages);
  writeJson(path.join(dest, "evidence.json"), evidence);
  writeJson(path.join(dest, "prose.json"), prose);
  fs.writeFileSync(
    path.join(dest, EVENTS_FILE),
    events.map((row) => JSON.stringify(row)).join("\n") + (events.length ? "\n" : ""),
  );
  if (replace && fs.existsSync(src)) fs.unlinkSync(src);
  return { dest, docket: docket.length, clocks: clocks.length, events: events.length, inventory: inventory.length };
}

function trimDocket(number) {
  const dest = splitMatterDir(MATTERS_DIR, number);
  const docketPath = path.join(dest, "docket.json");
  const inventoryPath = path.join(dest, "documents.json");
  const docket = JSON.parse(fs.readFileSync(docketPath, "utf8"));
  if (!fs.existsSync(inventoryPath)) {
    writeJson(
      inventoryPath,
      docket.map((row) => toInventoryRow(row)).filter((row) => row.path),
    );
  }
  const next = docket.filter(isPleadingDocument);
  writeJson(docketPath, next);
  return { before: docket.length, after: next.length, dest };
}

function rebuildFromInventory(number, { clocksFromEvents, keepHandClocks }) {
  const dest = splitMatterDir(MATTERS_DIR, number);
  const inventoryPath = path.join(dest, "documents.json");
  const docketPath = path.join(dest, "docket.json");
  const clocksPath = path.join(dest, "clocks.json");
  const eventsPath = path.join(dest, EVENTS_FILE);
  if (!fs.existsSync(inventoryPath)) return null;
  const inventory = JSON.parse(fs.readFileSync(inventoryPath, "utf8"));
  const docket = inventory.filter(isPleadingDocument).map(toDocketRow);
  writeJson(docketPath, docket);
  let clocks = null;
  if (clocksFromEvents && !(keepHandClocks && number === 24) && fs.existsSync(eventsPath)) {
    const events = fs
      .readFileSync(eventsPath, "utf8")
      .split(/\n/)
      .filter(Boolean)
      .map((line) => JSON.parse(line))
      .filter((row) => row.upcoming === true);
    clocks = events.map((row, i) => {
      const date = dateKeyFromLabel(row.date) || (row.ts ? String(row.ts).slice(0, 10) : null);
      return {
        id: `${paddedMatterNumber(number)}-${row.type ?? "event"}-${i + 1}`,
        date,
        date_label: row.date ?? null,
        kind: row.type ?? "event",
        status: date ? "open" : "undated",
        source_dkt: row.dkt ?? null,
        title: oneLiner(row.title ?? ""),
        actor: row.actor ?? null,
        source: row.path ?? null,
      };
    });
    writeJson(clocksPath, clocks);
  }
  return { number, docket: docket.length, clocks: clocks?.length ?? null };
}

const { number, replace, all, trimDocket: trimOnly, rebuild } = parseArgs(process.argv.slice(2));
const timeline = JSON.parse(fs.readFileSync(TIMELINE_PATH, "utf8"));

if (rebuild) {
  const numbers = fs
    .readdirSync(MATTERS_DIR, { withFileTypes: true })
    .filter((e) => e.isDirectory() && /^\d{2}$/.test(e.name))
    .map((e) => Number(e.name))
    .sort((a, b) => a - b);
  for (const n of numbers) {
    const result = rebuildFromInventory(n, { clocksFromEvents: true, keepHandClocks: true });
    if (!result) continue;
    console.log(
      `Rebuilt matter ${n}: ${result.docket} docket rows` +
        (result.clocks == null ? " (clocks kept)" : `, ${result.clocks} clocks`),
    );
  }
  process.exit(0);
}

if (trimOnly) {
  if (!Number.isInteger(number) || number < 1) {
    console.error("Usage: node internal/scripts/split-matter.mjs <number> --trim-docket");
    process.exit(1);
  }
  const result = trimDocket(number);
  console.log(
    `Trimmed docket ${number}: ${result.before} → ${result.after} pleading rows (${path.relative(process.cwd(), result.dest)})`,
  );
  process.exit(0);
}

if (all) {
  const numbers = fs
    .readdirSync(MATTERS_DIR)
    .filter((name) => /^\d{2}\.json$/.test(name))
    .map((name) => Number(name.slice(0, 2)))
    .sort((a, b) => a - b);
  if (!numbers.length) {
    console.log("No legacy NN.json files to split.");
    process.exit(0);
  }
  for (const n of numbers) {
    const src = legacyMatterPath(MATTERS_DIR, n);
    const raw = JSON.parse(fs.readFileSync(src, "utf8"));
    const result = writeSplit(n, raw, timeline, { replace: true });
    console.log(
      `Split matter ${n} → ${path.relative(process.cwd(), result.dest)} ` +
        `(${result.docket} docket, ${result.inventory} documents, ${result.clocks} clocks, ${result.events} events)`,
    );
  }
  process.exit(0);
}

if (!Number.isInteger(number) || number < 1) {
  console.error("Usage: node internal/scripts/split-matter.mjs <number|--all> [--replace] [--trim-docket]");
  process.exit(1);
}

const src = legacyMatterPath(MATTERS_DIR, number);
const dest = splitMatterDir(MATTERS_DIR, number);
if (!fs.existsSync(src)) {
  console.error(`No legacy file at ${path.relative(process.cwd(), src)}`);
  process.exit(1);
}
if (isSplitMatterDir(dest) && !replace) {
  console.error(`${path.relative(process.cwd(), dest)} already exists. Pass --replace to overwrite.`);
  process.exit(1);
}

const raw = JSON.parse(fs.readFileSync(src, "utf8"));
const result = writeSplit(number, raw, timeline, { replace });
console.log(
  `Split matter ${number} → ${path.relative(process.cwd(), result.dest)} ` +
    `(${result.docket} docket, ${result.inventory} documents, ${result.clocks} clocks, ${result.events} events)` +
    (replace ? "; removed legacy JSON" : ""),
);
