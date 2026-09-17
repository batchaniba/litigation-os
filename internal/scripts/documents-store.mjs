#!/usr/bin/env node
// ==========================================================
// Move PDF bytes to the `documents` branch so main stays small.
//
//   npm run documents:pull                # whole tree
//   npm run documents:pull -- --matter 24 # one matter folder
//   npm run documents:push                # after adding a filing (pre-commit also runs this)
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
      console.log(`OK — pushed document store ${result.commit.slice(0, 12)}.`);
    } else {
      console.log("OK — document store already matches the working tree.");
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
