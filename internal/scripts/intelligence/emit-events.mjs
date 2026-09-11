#!/usr/bin/env node
// Classify CourtListener entries into litigation-bus events.
// sync-dockets.mjs stays a dispatcher: it does not grow a 4,000-line agent.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  classifyDocketText,
  enrichEventRecord,
  issuesInText,
} from "../../src/intelligence/filingSignals.js";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../src/data/intelligence");
const EVENTS_PATH = path.join(ROOT, "events.json");

function readJson(name, fallback) {
  const file = path.join(ROOT, name);
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

export function loadCatalogSlice() {
  return {
    issues: readJson("issues.json", []),
    authorities: readJson("authorities.json", []),
    dependencies: readJson("dependencies.json", []),
  };
}

export { classifyDocketText };

export function eventFromNormalizedEntry(entry, catalog = loadCatalogSlice()) {
  const description = entry.description ?? "";
  const body = entry.body ?? "";
  const text = `${description}\n${body}`.trim();
  return enrichEventRecord(
    {
      id: `cl-${entry.matter}-${entry.courtlistener_entry_id ?? entry.entry_number ?? "x"}`,
      type: classifyDocketText(text),
      at: entry.date_filed ?? "",
      matter: entry.matter,
      docket: entry.entry_number ?? null,
      summary: description,
      issues: issuesInText(text, catalog.issues),
      payload: { provider: "courtlistener", body },
    },
    catalog,
  );
}

export function loadEventLog() {
  if (!fs.existsSync(EVENTS_PATH)) return [];
  return JSON.parse(fs.readFileSync(EVENTS_PATH, "utf8"));
}

function bodyOf(event) {
  return typeof event?.payload?.body === "string" ? event.payload.body : "";
}

export function appendEventLog(events, { dryRun = false } = {}) {
  if (!events.length) return loadEventLog();
  const existing = loadEventLog();
  const byId = new Map(existing.map((row) => [row.id, row]));
  for (const event of events) {
    const prior = byId.get(event.id);
    if (!prior) {
      byId.set(event.id, event);
      continue;
    }
    const nextBody = bodyOf(event);
    if (nextBody && nextBody !== bodyOf(prior)) {
      byId.set(event.id, {
        ...prior,
        ...event,
        payload: { ...(prior.payload ?? {}), ...(event.payload ?? {}) },
        issues: event.issues?.length ? event.issues : prior.issues,
      });
    }
  }
  const merged = [...byId.values()];
  if (!dryRun) {
    fs.mkdirSync(ROOT, { recursive: true });
    fs.writeFileSync(EVENTS_PATH, `${JSON.stringify(merged, null, 2)}\n`);
  }
  return merged;
}
