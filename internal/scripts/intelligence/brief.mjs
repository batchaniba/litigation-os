#!/usr/bin/env node
// Text radar for the litigation intelligence OS. The UI at /intelligence is the command center.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../src/data/intelligence");
const read = (name) => JSON.parse(fs.readFileSync(path.join(dir, name), "utf8"));

const issues = read("issues.json");
const matrices = read("matrices.json");
const motions = read("motions.json");
const dependencies = read("dependencies.json");
const recap = read("recap.json");
const fingerprints = read("fingerprints.json");
const citeproof = read("citeproof.json");

const qiMatters = [...new Set([
  ...matrices.flatMap((matrix) => matrix.elements.filter((el) => el.issue === "qualified_immunity").map(() => matrix.matter)),
  ...motions.filter((row) => row.issues.includes("qualified_immunity")).map((row) => row.matter),
])].sort((a, b) => a - b);
const live = motions.filter((row) => row.status === "live");
const waiting = dependencies.filter((row) => !row.trigger.fired);

console.log("LITIGATION INTELLIGENCE — text radar");
console.log("Percentages in the UI are record coverage, not win probability.");
console.log("");
console.log(`Issue catalog: ${issues.length} doctrines.`);
console.log(`QI currently mapped onto matters: ${qiMatters.join(", ") || "(none)"}`);
console.log("Live motions:");
for (const motion of live) {
  console.log(`  Matter ${motion.matter}: ${motion.label}${motion.hearing ? ` (${motion.hearing})` : ""}`);
}
console.log("Dependency clocks waiting on a trigger:");
for (const recipe of waiting) {
  console.log(`  Matter ${recipe.matter}: ${recipe.label}`);
  console.log(`    waiting on: ${recipe.trigger.description}`);
}
console.log("RECAP / PACER gate:");
for (const row of recap) {
  const action = row.inRecap ? "retrieve (already in RECAP)" : row.strategicValue === "LOW" ? "skip" : "retrieve recommended";
  console.log(`  ${action}: ${row.label}`);
}
console.log("CiteProof overstatement flags:");
for (const [id, audit] of Object.entries(citeproof)) {
  if (audit.parentheticalOverstates) console.log(`  ${id}: ${audit.notes?.[0] ?? "parenthetical overstates"}`);
}
console.log("Defense fingerprints on file:");
for (const profile of fingerprints) {
  console.log(`  ${profile.attorney}: ${profile.leadDefense}`);
}
console.log("");
console.log("Open /intelligence for twins, war rooms, shockwaves, and the overnight brief.");
