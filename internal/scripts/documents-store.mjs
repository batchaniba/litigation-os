#!/usr/bin/env node
// ==========================================================
// Document store: R2 is live bytes; origin/documents is the cold backup.
//
//   npm run documents:pull                # whole tree (R2 if R2_* set)
//   npm run documents:pull -- --matter 24 # one matter folder
//   npm run documents:push                # after adding or replacing a filing
//
// See internal/docs/DOCUMENT_STORE.md.
// ==========================================================
import {
  DOCUMENTS_PULL_USAGE,
  parseDocumentsPullArgs,
  pullDocuments,
  pushDocuments,
  seedDocumentsBranch,
} from "./lib/documents-branch.mjs";

const command = process.argv[2] ?? "";

try {
  if (command === "pull") {
    const opts = parseDocumentsPullArgs(process.argv.slice(3));
    if (opts.help) {
      process.stdout.write(DOCUMENTS_PULL_USAGE);
      process.exit(0);
    }
    const result = await pullDocuments(opts);
    if (result.list) {
      process.stdout.write(`${result.list.join("\n")}\n`);
    } else if (result.via === "r2") {
      console.log(`OK — pulled ${result.count} files from R2.`);
    } else if (result.paths.length === 1 && result.paths[0].endsWith("/documents")) {
      console.log("OK — document tree restored from origin/documents.");
    } else {
      console.log(`OK — pulled ${result.paths.join(", ")} from origin/documents.`);
    }
  } else if (command === "push") {
    const result = pushDocuments();
    if (result.pushed) {
      console.log(`OK — pushed document store ${String(result.commit).slice(0, 12)}.`);
    } else {
      console.log("OK — origin/documents already matches the working tree.");
    }
    if (result.r2?.uploaded) {
      console.log(`OK — published ${result.r2.count} PDFs to R2 and refreshed the path index.`);
    } else if (result.r2?.reason === "r2_unconfigured") {
      console.warn(
        "R2 skipped (no R2_* in the environment). Bytes are on origin/documents until `npm run documents:push` runs with credentials, or the r2-upload workflow runs.",
      );
    }
  } else if (command === "seed") {
    const result = seedDocumentsBranch();
    if (result.created) {
      console.log(`OK — seeded origin/documents ${result.commit.slice(0, 12)}.`);
    } else {
      console.log(`OK — origin/documents already exists (${result.commit.slice(0, 12)}).`);
    }
  } else {
    console.error("Usage: node internal/scripts/documents-store.mjs <pull|push|seed>");
    console.error("       npm run documents:pull -- --help");
    process.exit(2);
  }
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
