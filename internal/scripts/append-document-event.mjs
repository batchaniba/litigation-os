#!/usr/bin/env node
// Append one events.jsonl row when a file lands in documents/matter-N/.
// Split matters only. Append-only — never rewrite the log.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { inferDocketNumber, paddedMatterNumber } from "../src/data/matters/assembleMatter.js";
import { EVENTS_FILE, isSplitMatterDir, splitMatterDir } from "./lib/matter-layout.mjs";
import { MATTERS_DIR } from "./load-matters.mjs";
import { DOCUMENTS_ROOT } from "./lib/document-store.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");

const fileArg = process.argv[2];
if (!fileArg) {
  console.error("Usage: node internal/scripts/append-document-event.mjs <path-or-url>");
  process.exit(1);
}

const url = fileArg.startsWith("/documents/")
  ? fileArg
  : `/${path.relative(path.join(REPO_ROOT, "internal/public"), path.resolve(fileArg)).split(path.sep).join("/")}`;
const match = url.match(/^\/documents\/matter-(\d+)\//);
if (!match) process.exit(0);

const number = Number(match[1]);
const dir = splitMatterDir(MATTERS_DIR, number);
if (!isSplitMatterDir(dir)) process.exit(0);

const eventsPath = path.join(dir, EVENTS_FILE);
const row = {
  ts: new Date().toISOString(),
  matter: number,
  type: "document_added",
  title: path.posix.basename(url),
  path: url,
  dkt: inferDocketNumber(url),
};
fs.appendFileSync(eventsPath, `${JSON.stringify(row)}\n`);
console.log(`Appended event to ${path.relative(process.cwd(), eventsPath)}`);
