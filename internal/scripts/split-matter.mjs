#!/usr/bin/env node
// Split a legacy NN.json into NN/{matter,docket,clocks,parties,counsel,claims,damages,evidence,events,prose}.
// Portfolio-wide: any matter can be split. Does not invent docket numbers.
//
//   node internal/scripts/split-matter.mjs 24
//   node internal/scripts/split-matter.mjs 24 --replace
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { MATTERS_DIR } from "./load-matters.mjs";
import { dateKeyFromLabel } from "./lib/next-actions.mjs";
import {
  EVENTS_FILE,
  GRAPH_LIMITS,
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

function parseArgs(argv) {
  const replace = argv.includes("--replace");
  const number = Number(argv.find((a) => /^\d+$/.test(a)));
  return { replace, number };
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
        title: String(row.event ?? "").slice(0, GRAPH_LIMITS.indexNextClockTitleChars),
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
        matter: number,
        type: row.type ?? "event",
        title: String(row.event ?? ""),
        path: row.source ?? null,
        dkt: inferDocketNumber(row.source ?? "", row.event ?? ""),
      };
      if (row.upcoming === true) event.upcoming = true;
      return event;
    });
}

function slimMatter(raw) {
  const out = {};
  for (const key of IDENTITY_KEYS) {
    if (raw[key] !== undefined) out[key] = raw[key];
  }
  // First fetch stays small. Full diary lands in prose.json.
  out.procedural_status =
    "Canonical chronology is clocks.json, docket.json, and events.jsonl. Do not reconstruct dates from README.";
  if (typeof raw.key_facts === "string" && raw.key_facts.length > GRAPH_LIMITS.identityKeyFactsChars) {
    const keep = GRAPH_LIMITS.identityKeyFactsChars - 80;
    out.key_facts = `${raw.key_facts.slice(0, keep).replace(/\s+\S*$/, "")} See evidence.json and prose.json.`;
  }
  return out;
}

const { number, replace } = parseArgs(process.argv.slice(2));
if (!Number.isInteger(number) || number < 1) {
  console.error("Usage: node internal/scripts/split-matter.mjs <number> [--replace]");
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
const timeline = JSON.parse(fs.readFileSync(TIMELINE_PATH, "utf8"));

const docket = (raw.documents ?? []).map(toDocketRow);
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

if (replace) {
  fs.unlinkSync(src);
}

console.log(
  `Split matter ${number} → ${path.relative(process.cwd(), dest)} ` +
    `(${docket.length} docket rows, ${clocks.length} clocks, ${events.length} events)` +
    (replace ? "; removed legacy JSON" : ""),
);
