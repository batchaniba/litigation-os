#!/usr/bin/env node
// ============================================================
// Append newly landed document-store files to the committed manifest
// without rehashing the whole ~660 MB tree.
//
// Automation that pushes files straight to the `documents` branch (e.g. the
// RECAP brief fetcher) uses this to keep internal/src/data/documents/
// manifest.json in sync, so the documents-integrity check stays green.
//
// Usage:
//   node append-document-manifest.mjs \
//     --manifest internal/src/data/documents/manifest.json \
//     --dir /tmp/briefs/ventura-randstad \
//     --prefix /documents/counsel-briefs/ventura-randstad
//
// Every non-dotfile under --dir is recorded as
//   { path: "<prefix>/<name>", size, sha256 }
// Idempotent: existing entries with matching size+sha are left alone;
// entries whose size changed are rehashed and updated.
// ============================================================
import fs from "node:fs";
import path from "node:path";
import {
  hashFileSha256,
  loadManifest,
  manifestByPath,
  manifestPayload,
  walkFiles,
} from "./lib/document-store.mjs";

function arg(name, def = null) {
  const ix = process.argv.indexOf(`--${name}`);
  if (ix === -1 || ix + 1 >= process.argv.length) return def;
  return process.argv[ix + 1];
}

const MANIFEST = arg("manifest");
const DIR = arg("dir");
const PREFIX = arg("prefix");

if (!MANIFEST || !DIR || !PREFIX) {
  console.error("usage: append-document-manifest.mjs --manifest <path> --dir <dir> --prefix <url-prefix>");
  process.exit(2);
}
if (!PREFIX.startsWith("/documents/")) {
  console.error(`refusing prefix outside the document store: ${PREFIX}`);
  process.exit(2);
}

const manifest = loadManifest(MANIFEST);
const byPath = manifestByPath(manifest);
let added = 0;
let updated = 0;

for (const full of walkFiles(DIR)) {
  const name = path.basename(full);
  const urlPath = `${PREFIX}/${name}`;
  const size = fs.statSync(full).size;
  const prev = byPath.get(urlPath);
  if (prev && prev.size === size && prev.sha256) continue;
  const sha256 = hashFileSha256(full);
  const entry = { path: urlPath, size, sha256 };
  if (prev) {
    const ix = manifest.files.findIndex((f) => f.path === urlPath);
    manifest.files[ix] = entry;
    updated += 1;
  } else {
    manifest.files.push(entry);
    added += 1;
  }
  byPath.set(urlPath, entry);
}

manifest.files.sort((a, b) => a.path.localeCompare(b.path));
manifest.fileCount = manifest.files.length;
manifest.totalBytes = manifest.files.reduce((sum, f) => sum + f.size, 0);
fs.writeFileSync(MANIFEST, manifestPayload(manifest));
console.log(`manifest updated: +${added} added, ${updated} updated, ${manifest.fileCount} total`);
