#!/usr/bin/env node
// ==========================================================
// Scaffold a new matter record + document folder.
//
// Usage:
//   npm run scaffold:matter -- 32 "Newanforbi v. Example Corp."
//   node internal/scripts/scaffold-matter.mjs 32 "Newanforbi v. Example Corp."
//
// Creates:
//   internal/src/data/matters/NN.json
//   internal/public/documents/matter-NN/
//
// Then fill in the JSON and add companion rows in timeline.js,
// damages.js, and lawyerFees.js (validate will warn until those exist).
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadMatters, matterFileName, MATTERS_DIR } from "./load-matters.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..", "..");

const [numberArg, ...captionParts] = process.argv.slice(2);
const number = Number(numberArg);
const caption = captionParts.join(" ").trim();

if (!Number.isInteger(number) || number < 1 || !caption) {
  console.error('Usage: npm run scaffold:matter -- <number> "<caption>"');
  console.error('Example: npm run scaffold:matter -- 32 "Newanforbi v. Example Corp."');
  process.exit(1);
}

const existing = loadMatters();
if (existing.some((m) => m.number === number)) {
  console.error(`Matter ${number} already exists (${matterFileName(number)}).`);
  process.exit(1);
}

const fileName = matterFileName(number);
const jsonPath = path.join(MATTERS_DIR, fileName);
const docsDir = path.join(
  REPO_ROOT,
  "internal/public/documents",
  `matter-${String(number).padStart(2, "0")}`,
);

const stub = {
  number,
  caption,
  case_no: "TBD",
  court: "TBD",
  claims: "TBD",
  status: "Pre-complaint / drafting",
  filed: "Not yet filed",
  judge: "TBD",
  cluster: 0,
  type: "State",
  defendants: "TBD",
  causes: [],
  key_facts: "",
  procedural_status: "",
  damages: "",
  risk: "",
  evidence: [],
  documents: [],
};

fs.writeFileSync(jsonPath, JSON.stringify(stub, null, 2) + "\n");
fs.mkdirSync(docsDir, { recursive: true });
fs.writeFileSync(
  path.join(docsDir, ".gitkeep"),
  "# Place matter PDFs here. Reference them from documents[] in the matter JSON.\n",
);

console.log(`Created ${path.relative(REPO_ROOT, jsonPath)}`);
console.log(`Created ${path.relative(REPO_ROOT, docsDir)}/`);
console.log(`
Next checklist for Matter ${number}:
  [ ] Fill key_facts, procedural_status, damages, risk, causes in ${fileName}
  [ ] Add timeline.js entries (mark upcoming deadlines with upcoming: true)
  [ ] Add damages.js matter_damages[] row (and damages_table category if needed)
  [ ] Add lawyerFees.js lawyer_fees[] row
  [ ] Update README matter inventory / deadlines if this matter is active
  [ ] Drop PDFs into ${path.relative(REPO_ROOT, docsDir)} and list them in documents[]
  [ ] npm run validate
`);
