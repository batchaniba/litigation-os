#!/usr/bin/env node
// Idempotent public-library sync: repo documents/ → R2 (canonical bytes) + D1
// (index) + extracted-text sidecars + documents_fts.
//
//   npm run documents:sync              # dry-run (default)
//   npm run documents:sync -- --apply   # PUT missing R2 objects + D1 upserts
//
// Never deletes from R2 or D1. Private denylist files are skipped (they stay
// in R2 if already there; they are not added to the public path index or FTS).
// Does not reseed. A full `node workers/doc-api/seed.mjs` DELETE is destructive
// and is not this script.
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import {
  DOCUMENTS_ROOT,
  REPO_ROOT,
  hashFileSha256,
  walkFiles,
} from "./lib/document-store.mjs";
import { isPrivateDocument } from "./lib/private-documents.mjs";
import { isConfigured as r2IsConfigured, keyForSha256 } from "./lib/r2-client.mjs";

const apply = process.argv.includes("--apply");
const includePrivate = process.argv.includes("--include-private");

function urlFromDisk(abs) {
  const rel = path.relative(DOCUMENTS_ROOT, abs).split(path.sep).join("/");
  return `/documents/${rel}`;
}

function main() {
  if (!fs.existsSync(DOCUMENTS_ROOT)) {
    console.error("documents/ is missing — run the consolidator or npm run documents:pull");
    process.exit(1);
  }
  const pdfs = walkFiles(DOCUMENTS_ROOT).filter((p) => p.toLowerCase().endsWith(".pdf"));
  const rows = [];
  for (const abs of pdfs) {
    const docPath = urlFromDisk(abs);
    const sha256 = hashFileSha256(abs);
    const size = fs.statSync(abs).size;
    const privateDoc = isPrivateDocument({ path: docPath, sha256 });
    rows.push({
      disk: path.relative(REPO_ROOT, abs).split(path.sep).join("/"),
      path: docPath,
      sha256,
      size,
      r2_key: keyForSha256(sha256),
      private: privateDoc,
      action: privateDoc ? "skip_private" : apply ? "upload_if_missing" : "would_upload_if_missing",
    });
  }
  const publicRows = rows.filter((r) => !r.private);
  const privateRows = rows.filter((r) => r.private);

  const summary = {
    generated: new Date().toISOString(),
    apply,
    r2_configured: r2IsConfigured(),
    public: publicRows.length,
    private_skipped: privateRows.length,
    note:
      "R2 is canonical; D1 is the index. This script never DELETE/DROP. " +
      "Without R2_* it only prints the plan. Text sidecars need pdftotext. " +
      "D1 FTS: wrangler d1 execute litigation-portfolio --remote --file=workers/doc-api/schema.sql " +
      "then re-run with --apply (FTS upsert is printed as SQL, not executed here).",
  };

  if (privateRows.length && !includePrivate) {
    summary.private_paths = privateRows.map((r) => r.path);
  }

  if (apply && r2IsConfigured()) {
    const list = path.join("/tmp", `ilp-sync-${process.pid}.txt`);
    fs.writeFileSync(list, `${publicRows.map((r) => r.disk).join("\n")}\n`);
    execFileSync("node", ["internal/scripts/r2-upload.mjs", "--list", list], {
      cwd: REPO_ROOT,
      stdio: "inherit",
    });
    execFileSync("node", ["internal/scripts/r2-upload.mjs", "--index"], {
      cwd: REPO_ROOT,
      stdio: "inherit",
    });
    summary.r2 = "uploaded_or_skipped";
  } else if (apply && !r2IsConfigured()) {
    summary.r2 = "skipped_no_credentials";
    console.warn(
      "R2_* is not in the environment. Export them from ~/.config/r2/env on the laptop, then re-run with --apply.\n" +
        "D1 upserts (no DELETE):\n" +
        publicRows
          .slice(0, 3)
          .map(
            (r) =>
              `  wrangler d1 execute litigation-portfolio --remote --command "INSERT OR REPLACE INTO documents (sha256, matter_number, path, size) VALUES ('${r.sha256}', NULL, '${r.path.replaceAll("'", "''")}', ${r.size});"`,
          )
          .join("\n") +
        (publicRows.length > 3 ? `\n  …and ${publicRows.length - 3} more` : ""),
    );
  }

  summary.fts =
    "Apply workers/doc-api/schema.sql (CREATE VIRTUAL TABLE documents_fts). Path LIKE search works until text rows are upserted with R2_* + pdftotext.";

  process.stdout.write(
    `${JSON.stringify({ ...summary, sample: publicRows.slice(0, 5) }, null, 2)}\n`,
  );
  process.stdout.write(
    `${apply ? "APPLIED" : "DRY-RUN"} public=${publicRows.length} private_skipped=${privateRows.length} r2=${r2IsConfigured() ? "configured" : "unconfigured"}\n`,
  );
}

main();
