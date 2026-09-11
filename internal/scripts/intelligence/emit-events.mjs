#!/usr/bin/env node
// Classify CourtListener entries into litigation-bus events.
// sync-dockets.mjs stays a dispatcher: it does not grow a 4,000-line agent.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const MOTION = /motion to dismiss|notice of motion|rule 12|12\(b\)\(6\)|demurrer/i;
const ORDER = /\border\b|clerk.?s notice|findings?\s*(and|&)\s*recommendations?/i;
const COUNSEL = /notice of appearance|appeared for|counsel of record/i;
const SETTLED = /\bsettled\b|notice of settlement|stipulation of dismissal/i;

export function classifyDocketText(text) {
  const body = String(text ?? "");
  if (SETTLED.test(body)) return "CASE_SETTLED";
  if (COUNSEL.test(body)) return "COUNSEL_APPEARED";
  if (MOTION.test(body)) return "MOTION_FILED";
  if (ORDER.test(body)) return "ORDER_ENTERED";
  return "DOCKET_ENTRY_ADDED";
}

export function eventFromNormalizedEntry(entry) {
  const description = entry.description ?? "";
  return {
    id: `cl-${entry.matter}-${entry.courtlistener_entry_id ?? entry.entry_number ?? "x"}`,
    type: classifyDocketText(description),
    at: entry.date_filed ?? "",
    matter: entry.matter,
    docket: entry.entry_number ?? null,
    summary: description,
    payload: { provider: "courtlistener" },
  };
}

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../src/data/intelligence");
const EVENTS_PATH = path.join(ROOT, "events.json");

export function loadEventLog() {
  if (!fs.existsSync(EVENTS_PATH)) return [];
  return JSON.parse(fs.readFileSync(EVENTS_PATH, "utf8"));
}

export function appendEventLog(events, { dryRun = false } = {}) {
  if (!events.length) return loadEventLog();
  const existing = loadEventLog();
  const seen = new Set(existing.map((row) => row.id));
  const merged = [...existing];
  for (const event of events) {
    if (seen.has(event.id)) continue;
    seen.add(event.id);
    merged.push(event);
  }
  if (!dryRun) {
    fs.mkdirSync(ROOT, { recursive: true });
    fs.writeFileSync(EVENTS_PATH, `${JSON.stringify(merged, null, 2)}\n`);
  }
  return merged;
}
