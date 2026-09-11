// Paths and JSON IO for the CourtListener bridge.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { writeJsonAscii } from "../lib/write-json-ascii.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = path.resolve(__dirname, "..", "..", "..");
export const DATA_DIR = path.join(REPO_ROOT, "internal/src/data");
export const MATTERS_DIR = path.join(DATA_DIR, "matters");
export const CL_DIR = path.join(DATA_DIR, "courtlistener");
export const TIMELINE_PATH = path.join(DATA_DIR, "timeline.json");
export const REVIEW_PATH = path.join(CL_DIR, "review.json");
export const LEDGER_PATH = path.join(CL_DIR, "ledger.json");
export const SYNC_STATE_PATH = path.join(CL_DIR, "sync-state.json");

export function readJson(filePath, fallback = null) {
  if (!fs.existsSync(filePath)) return fallback;
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

export function writeJsonUtf8(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`);
}

export function emptyLedger() {
  return { version: 1, entries: [] };
}

export function emptyReview() {
  return { version: 1, candidates: [] };
}

export function emptySyncState() {
  return { version: 1, matters: {} };
}

export function loadLedger() {
  return readJson(LEDGER_PATH, emptyLedger());
}

export function loadReview() {
  return readJson(REVIEW_PATH, emptyReview());
}

export function loadSyncState() {
  return readJson(SYNC_STATE_PATH, emptySyncState());
}

export function loadTimeline() {
  return readJson(TIMELINE_PATH, []);
}

export function writeTimeline(timeline) {
  writeJsonAscii(TIMELINE_PATH, timeline);
}

export function writeLedger(ledger) {
  writeJsonUtf8(LEDGER_PATH, ledger);
}

export function writeReview(review) {
  writeJsonUtf8(REVIEW_PATH, review);
}

export function writeSyncState(state) {
  writeJsonUtf8(SYNC_STATE_PATH, state);
}

export function insertBinding(matter, binding) {
  const out = {};
  let inserted = false;
  for (const [key, value] of Object.entries(matter)) {
    if (key === "courtlistener" || key === "__sourceFile") continue;
    out[key] = value;
    if (key === "court") {
      out.courtlistener = binding;
      inserted = true;
    }
  }
  if (!inserted) out.courtlistener = binding;
  return out;
}

export function compactBinding(binding) {
  const out = {};
  for (const key of ["court_id", "docket_id", "docket_url", "alert_id"]) {
    if (binding[key] != null && binding[key] !== "") out[key] = binding[key];
  }
  return out;
}

export function writeMatterRecord(matter) {
  const number = matter.number;
  const fileName = `${String(number).padStart(2, "0")}.json`;
  const filePath = path.join(MATTERS_DIR, fileName);
  const current = JSON.parse(fs.readFileSync(filePath, "utf8"));
  const next = insertBinding(current, compactBinding(matter.courtlistener));
  writeJsonUtf8(filePath, next);
  return filePath;
}

export function bindingFromHit(hit, courtId) {
  const docketId = hit.docket_id ?? hit.id ?? null;
  const docketUrl = hit.docket_absolute_url ?? hit.absolute_url ?? (docketId ? `/docket/${docketId}/` : null);
  return compactBinding({
    court_id: hit.court_id ?? courtId,
    docket_id: docketId,
    docket_url: docketUrl,
  });
}

export function bindingsEqual(a, b) {
  return JSON.stringify(compactBinding(a ?? {})) === JSON.stringify(compactBinding(b ?? {}));
}
