#!/usr/bin/env node
// Public timeline projection: timeline.json (internal, full) -> timeline.public.json
// (what the SPA bundles). Drops every event whose text carries a settlement or
// demand figure, or settlement payment mechanics, then redacts addresses, phones,
// emails, vault tokens, and unique identifiers from what remains.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { sanitizePublicText, settlementLeakPatterns } from "./lib/publish-matter.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.resolve(__dirname, "../src/data");
const SRC = path.join(DATA_DIR, "timeline.json");
const OUT = path.join(DATA_DIR, "timeline.public.json");
const checkOnly = process.argv.includes("--check");

function sanitizeEvent(event) {
  if (!event || typeof event !== "object") return event;
  const out = { ...event };
  if (typeof out.event === "string") out.event = sanitizePublicText(out.event);
  if (typeof out.source === "string" && !out.source.startsWith("/documents/")) {
    out.source = sanitizePublicText(out.source);
  }
  return out;
}

export function isPublicTimelineEvent(event) {
  const hay = JSON.stringify(event ?? {});
  return !settlementLeakPatterns().some(({ re }) => re.test(hay));
}

const full = JSON.parse(fs.readFileSync(SRC, "utf8"));
const kept = full.filter(isPublicTimelineEvent).map(sanitizeEvent);
const payload = `${JSON.stringify(kept, null, 2)}\n`;

if (checkOnly) {
  const current = fs.existsSync(OUT) ? fs.readFileSync(OUT, "utf8") : "";
  if (current !== payload) {
    console.error("internal/src/data/timeline.public.json is stale — run npm run sync:public-timeline");
    process.exit(1);
  }
  console.log(`OK — timeline.public.json is current (${kept.length}/${full.length} events).`);
  process.exit(0);
}
fs.writeFileSync(OUT, payload);
console.log(`Wrote ${path.relative(process.cwd(), OUT)} (${kept.length}/${full.length} events; ${full.length - kept.length} withheld).`);
