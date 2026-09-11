#!/usr/bin/env node
// ==========================================================
// Refresh every derived snapshot from source records.
//
//   registry.json          ← document files + label overrides
//   manifest.json          ← sha256 inventory of public/documents
//   summaries.json         ← matter JSON
//   document-index.json    ← matter JSON + registry
//   upcoming.json          ← timeline.json (upcoming: true)
//   vercel.json / slugs    ← short-links.json
//   README.md tables       ← matters + timeline + damages
//
// Usage: npm run sync:all
// ==========================================================
import { spawnSync } from "node:child_process";

const steps = [
  ["sync:registry", ["npm", "run", "sync:registry"]],
  ["sync:manifest", ["npm", "run", "sync:manifest"]],
  ["sync:summaries", ["npm", "run", "sync:summaries"]],
  ["sync:upcoming", ["npm", "run", "sync:upcoming"]],
  ["sync:short-links", ["npm", "run", "sync:short-links"]],
  ["generate:readme", ["npm", "run", "generate:readme"]],
];

for (const [label, argv] of steps) {
  const result = spawnSync(argv[0], argv.slice(1), { stdio: "inherit" });
  if (result.status !== 0) {
    console.error(`sync:all stopped at ${label}`);
    process.exit(result.status ?? 1);
  }
}
