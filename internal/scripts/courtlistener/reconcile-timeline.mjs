#!/usr/bin/env node
// Re-run timeline reconciliation from the local ledger (no API).
// Does not promote review.json candidates into upcoming deadlines.

import path from "node:path";
import { fileURLToPath } from "node:url";

function main() {
  console.log(
    "Deadline candidates stay in internal/src/data/courtlistener/review.json until approved.\n" +
      "New docket rows enter the ledger and timeline through npm run court:sync.\n" +
      "This command does not copy review candidates into timeline.json.",
  );
}

const isCli = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isCli) main();
