#!/usr/bin/env node
// ==========================================================
// Build / check the physical inventory of public/documents.
//
// Every file under internal/public/documents/ (except dotfiles) is recorded
// as { path, size, sha256 }. Data-only CI uses this in place of the 660 MB
// tree. See internal/docs/DOCUMENT_STORE.md.
//
// Usage:
//   npm run sync:manifest            # write manifest.json
//   npm run sync:manifest -- --check # exit 1 if the inventory drifted
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import {
  DOCUMENTS_ROOT,
  MANIFEST_PATH,
  REPO_ROOT,
  buildManifestFromDisk,
  loadManifest,
  manifestByPath,
  manifestPayload,
} from "./lib/document-store.mjs";

const checkOnly = process.argv.includes("--check");

if (!fs.existsSync(DOCUMENTS_ROOT)) {
  console.error(
    "documents tree missing — cannot build or check the manifest. " +
      "If this is a sparse checkout, skip this script and let validate " +
      "--skip-disk-docs read the committed manifest.",
  );
  process.exit(1);
}

const expected = buildManifestFromDisk();
const payload = manifestPayload(expected);

function summarizeDrift(onDisk) {
  const expectedByPath = manifestByPath(expected);
  const diskByPath = manifestByPath(onDisk);
  let missing = 0;
  let extra = 0;
  let changed = 0;
  for (const file of expected.files) {
    const have = diskByPath.get(file.path);
    if (!have) {
      missing += 1;
      if (missing <= 8) console.error(`  missing: ${file.path}`);
      continue;
    }
    if (have.size !== file.size || have.sha256 !== file.sha256) {
      changed += 1;
      if (changed <= 8) console.error(`  changed: ${file.path}`);
    }
  }
  for (const file of onDisk.files ?? []) {
    if (!expectedByPath.has(file.path)) {
      extra += 1;
      if (extra <= 8) console.error(`  extra: ${file.path}`);
    }
  }
  return { missing, extra, changed };
}

if (checkOnly) {
  if (!fs.existsSync(MANIFEST_PATH)) {
    console.error("Missing document manifest — run npm run sync:manifest");
    process.exit(1);
  }
  const actual = fs.readFileSync(MANIFEST_PATH, "utf8");
  if (actual !== payload) {
    console.error("Document manifest is stale — run npm run sync:manifest");
    const { missing, extra, changed } = summarizeDrift(loadManifest());
    console.error(
      `  ${changed} hash/size mismatch(es), ${missing} missing, ${extra} extra ` +
        `(disk ${expected.fileCount} files / ${expected.totalBytes} bytes).`,
    );
    process.exit(1);
  }
  console.log(
    `OK — document manifest current (${expected.fileCount} files, ${expected.totalBytes} bytes).`,
  );
  process.exit(0);
}

fs.mkdirSync(path.dirname(MANIFEST_PATH), { recursive: true });
fs.writeFileSync(MANIFEST_PATH, payload);
console.log(
  `Wrote ${path.relative(REPO_ROOT, MANIFEST_PATH)} ` +
    `(${expected.fileCount} files, ${expected.totalBytes} bytes).`,
);
