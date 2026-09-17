#!/usr/bin/env node
// New PDFs in the document store need a searchable sidecar on this branch.
// Grandfathered paths (already in HEAD's manifest) are not retroactively required.
//
//   node internal/scripts/check-document-sidecars.mjs
//   node internal/scripts/check-document-sidecars.mjs --staged
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { DOCUMENTS_ROOT, loadManifest } from "./lib/document-store.mjs";

const stagedOnly = process.argv.includes("--staged");

function sidecarPaths(pdfPath) {
  const parsed = path.parse(pdfPath);
  const stem = path.join(parsed.dir, parsed.name);
  return { meta: `${stem}.meta.json`, txt: `${stem}.txt` };
}

function diskFromUrl(urlPath) {
  return path.join(DOCUMENTS_ROOT, urlPath.replace(/^\/documents\//, ""));
}

function headManifestPaths() {
  try {
    const raw = execSync("git show HEAD:internal/src/data/documents/manifest.json", {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    });
    const parsed = JSON.parse(raw);
    return new Set((parsed.files ?? []).map((f) => f.path));
  } catch {
    return new Set();
  }
}

function stagedPdfUrls() {
  const out = execSync("git diff --cached --name-only --diff-filter=A", { encoding: "utf8" });
  return out
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => /^internal\/public\/documents\/.+\.pdf$/i.test(line))
    .map((line) => `/${line.replace(/^internal\/public\//, "")}`);
}

const required = new Set();
if (stagedOnly) {
  for (const url of stagedPdfUrls()) required.add(url);
} else {
  const previous = headManifestPaths();
  const current = loadManifest();
  for (const file of current.files ?? []) {
    if (!/\.pdf$/i.test(file.path)) continue;
    if (!previous.has(file.path)) required.add(file.path);
  }
}

const errors = [];
for (const url of [...required].sort()) {
  const disk = diskFromUrl(url);
  const { meta, txt } = sidecarPaths(disk);
  if (!fs.existsSync(meta)) {
    errors.push(`${url}: missing ${path.basename(meta)} sidecar`);
  }
  if (!fs.existsSync(txt)) {
    errors.push(`${url}: missing ${path.basename(txt)} sidecar`);
  }
}

if (errors.length) {
  console.error("New PDF(s) missing machine-readable sidecars (.meta.json + .txt):");
  for (const err of errors) console.error(`  - ${err}`);
  process.exit(1);
}

if (required.size) {
  console.log(`OK — ${required.size} new PDF(s) have sidecars.`);
} else {
  console.log("OK — no new PDFs requiring sidecars.");
}
