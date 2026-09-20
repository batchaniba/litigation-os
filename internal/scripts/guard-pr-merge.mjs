#!/usr/bin/env node
// Pre-merge guardrail: flag files a PR would DELETE from its base branch.
//
// Catches the silent-drop failure class (PR #876, 2026-09-19: a Matter 41 branch
// built from a stale tree whose squash merge deleted 84 unrelated tracked files,
// including the Ray Kim dossier and the 9/18 research pulls; same class as the
// 9/18 documents-branch race). Run before tapping merge:
//
//   npm run guard:pr -- --pr 876
//
// Exit 0: no deletions vs base (safe to merge). Exit 1: deletions found —
// confirm each is intentional (name them in the PR body) or rebase the branch
// onto base and restore them before merging.
//
// Works on a plain local clone; no tokens needed (uses git only).
import { execFileSync } from "node:child_process";

const args = process.argv.slice(2);
function opt(name, fallback = null) {
  const hit = args.find((a) => a === name || a.startsWith(name + "="));
  if (!hit) return fallback;
  if (hit.includes("=")) return hit.split("=").slice(1).join("=");
  const i = args.indexOf(hit);
  return args[i + 1] ?? fallback;
}

const pr = opt("--pr") || args.find((a) => /^\d+$/.test(a));
const baseRef = opt("--base", "origin/main");
const remote = opt("--origin", "origin");

if (!pr) {
  console.error("Usage: npm run guard:pr -- --pr <number> [--base <ref>] [--origin <remote>]");
  process.exit(2);
}

function git(...gargs) {
  return execFileSync("git", gargs, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim();
}

let root;
try {
  root = git("rev-parse", "--show-toplevel");
} catch {
  console.error("guard:pr: not inside a git repository.");
  process.exit(2);
}
process.chdir(root);

// Fetch the PR head into FETCH_HEAD (no local branch created).
try {
  git("fetch", "--quiet", remote, `pull/${pr}/head`);
} catch (e) {
  console.error(`guard:pr: could not fetch pull/${pr}/head from ${remote}. ${e.message.split("\n")[0]}`);
  process.exit(2);
}
const head = git("rev-parse", "FETCH_HEAD");
let base;
try {
  base = git("rev-parse", baseRef);
} catch {
  console.error(`guard:pr: base ref ${baseRef} not found (try: git fetch ${remote}).`);
  process.exit(2);
}

// Two-dot diff: what the merge would remove from files that exist on base today.
// (Squash merges apply the branch diff onto the base tip, so anything present
// on base but absent in the head is deleted by the merge.)
const deleted = git("diff", "--name-only", "--diff-filter=D", base, head)
  .split("\n")
  .filter(Boolean);
const added = git("diff", "--name-only", "--diff-filter=A", base, head).split("\n").filter(Boolean);
const modified = git("diff", "--name-only", "--diff-filter=M", base, head).split("\n").filter(Boolean);

// Staleness signal: how far behind base the branch's merge-base is.
let behind = null;
try {
  const mb = git("merge-base", base, head);
  behind = parseInt(git("rev-list", "--count", `${mb}..${base}`), 10);
} catch { /* non-fatal */ }

console.log(`guard:pr #${pr}: base=${baseRef} (${base.slice(0, 8)}), head=${head.slice(0, 8)}`);
console.log(`  added: ${added.length}, modified: ${modified.length}, deleted vs base: ${deleted.length}`);
if (behind !== null) console.log(`  branch merge-base is ${behind} commit(s) behind base${behind > 5 ? "  <-- STALE BRANCH" : ""}`);

if (deleted.length === 0) {
  console.log("OK: PR deletes nothing from base. Safe to merge on this axis.");
  process.exit(0);
}

console.log("\nDELETED BY THIS PR (exist on base, absent in PR head):");
const byDir = new Map();
for (const f of deleted) {
  const dir = f.includes("/") ? f.slice(0, f.lastIndexOf("/")) : ".";
  if (!byDir.has(dir)) byDir.set(dir, []);
  byDir.get(dir).push(f);
}
for (const [dir, files] of [...byDir.entries()].sort()) {
  console.log(`  ${dir}/ (${files.length})`);
  for (const f of files.slice(0, 15)) console.log(`    - ${f.split("/").pop()}`);
  if (files.length > 15) console.log(`    ... and ${files.length - 15} more`);
}
console.log("\nRefusing: confirm every deletion above is intentional (name them in the PR body),");
console.log("or rebase the branch onto base and restore them, then re-run this check.");
process.exit(1);
