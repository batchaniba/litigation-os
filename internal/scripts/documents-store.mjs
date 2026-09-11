#!/usr/bin/env node
// ==========================================================
// Move PDF bytes to the `documents` branch so main stays small.
//
//   npm run documents:pull   # after clone, fill internal/public/documents/
//   npm run documents:push   # after adding a filing (pre-commit also runs this)
//
// See internal/docs/DOCUMENT_STORE.md.
// ==========================================================
import { pullDocuments, pushDocuments, seedDocumentsBranch } from "./lib/documents-branch.mjs";

const command = process.argv[2] ?? "";

try {
  if (command === "pull") {
    pullDocuments();
    console.log("OK — document tree restored from origin/documents.");
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
    process.exit(2);
  }
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
