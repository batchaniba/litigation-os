#!/usr/bin/env node
// Backfill: extracted-text sidecars for every R2 PDF.
//
//   node internal/scripts/extract-doc-text.mjs
//   node internal/scripts/extract-doc-text.mjs --list <file>   # one sha256 per line
//
// For each manifest PDF, ensures text/<first2>/<rest>.txt exists in R2 via
// lib/doc-text.mjs (poppler `pdftotext -layout`; empty sidecar = no text
// layer; only a missing sidecar means "not yet processed"). Idempotent —
// re-runs skip what exists. Never deletes from R2. Exits 1 if any file
// fails (including a missing PDF or a missing pdftotext binary).
//
// R2_* come from the environment (see lib/r2-client.mjs).
import fs from "node:fs";
import {
  getObject,
  keyForSha256,
  keyForSha256Text,
} from "./lib/r2-client.mjs";
import { ensureTextSidecar } from "./lib/doc-text.mjs";
import { MANIFEST_PATH } from "./lib/document-store.mjs";

const CONCURRENCY = 6;
const HEX64 = /^[0-9a-f]{64}$/;

async function processOne(sha256) {
  const log = { sha256, text_key: keyForSha256Text(sha256) };
  try {
    const { body } = await getObject(keyForSha256(sha256));
    log.pdf_bytes = body.length;
    log.text_status = await ensureTextSidecar(sha256, body);
    log.status = log.text_status === "skipped_no_pdftotext" ? "failed" : "ok";
    if (log.status === "failed") log.error = "pdftotext binary not installed";
  } catch (error) {
    log.status = "failed";
    log.error = String(error instanceof Error ? error.message : error).slice(0, 300);
  }
  return log;
}

async function mapLimit(items, limit, fn) {
  const out = [];
  let i = 0;
  const n = Math.min(limit, items.length) || 0;
  await Promise.all(
    Array.from({ length: n }, async () => {
      while (i < items.length) {
        const idx = i++;
        out[idx] = await fn(items[idx]);
      }
    }),
  );
  return out;
}

let shas;
if (process.argv[2] === "--list" && process.argv[3]) {
  shas = fs
    .readFileSync(process.argv[3], "utf8")
    .split("\n")
    .map((l) => l.trim().toLowerCase())
    .filter((l) => HEX64.test(l));
  if (!shas.length) {
    console.error("no valid sha256 lines in list file");
    process.exit(2);
  }
} else if (process.argv[2]) {
  console.error(
    "usage: node internal/scripts/extract-doc-text.mjs [--list <file>]",
  );
  process.exit(2);
} else {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
  shas = manifest.files
    .filter((f) => f.path.endsWith(".pdf") && HEX64.test(f.sha256))
    .map((f) => f.sha256.toLowerCase());
}

const results = await mapLimit(shas, CONCURRENCY, processOne);
let failed = 0;
for (const log of results) {
  console.log(JSON.stringify(log));
  if (log.status === "failed") failed += 1;
}
console.error(`done: ${shas.length} pdfs, ${failed} failed`);
process.exit(failed ? 1 : 0);
