#!/usr/bin/env node
// Fail-closed local portfolio gate. Invoked by:
//   npm run gate
//   .githooks/pre-push  →  node internal/scripts/portfolio-gate.mjs --hook
//
// Hook mode reads git's <local-ref> <local-sha> <remote-ref> <remote-sha> lines
// on stdin. Direct mode (`npm run gate`) always runs the checks.
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  checkPrerequisites,
  decideHookAction,
  GATE_STEPS,
  parsePushLines,
  shouldSkipDiskDocs,
} from "./lib/portfolio-gate-policy.mjs";
import { diskFromUrl, loadManifest } from "./lib/document-store.mjs";
import { isPrivateDocument } from "./lib/private-documents.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");

export function runPortfolioGate({
  hookMode = false,
  stdinText = "",
  env = process.env,
  nodeModulesExists,
  python3Available,
  nodeVersion = process.versions.node,
  enginesRange,
  nvmrcVersion,
  matterDirNames = [],
  diskComplete = true,
  runStep,
  log = console.log,
  logErr = console.error,
} = {}) {
  const prefix = hookMode ? "pre-push" : "portfolio-gate";

  if (hookMode) {
    const lines = parsePushLines(stdinText);
    const decision = decideHookAction({
      lines,
      skipValue: env.SKIP_PORTFOLIO_GATE,
    });
    if (decision.action === "skip") {
      return 0;
    }
    if (decision.action === "bypass") {
      logErr(`${prefix}: ${decision.reason}`);
      return 0;
    }
    if (decision.action === "refuse") {
      logErr(`${prefix}: ${decision.reason}`);
      return 1;
    }
    if (env.SKIP_PORTFOLIO_GATE) {
      logErr(`${prefix}: ${decision.reason}`);
    }
  }

  const preflight = checkPrerequisites({
    nodeModulesExists,
    python3Available,
    nodeVersion,
    enginesRange,
    nvmrcVersion,
  });
  if (!preflight.ok) {
    logErr(preflight.message);
    return 1;
  }

  if (shouldSkipDiskDocs(matterDirNames) || diskComplete === false) {
    env.PORTFOLIO_SKIP_DISK_DOCS = "1";
  }
  env.VITE_COPY_DOCUMENTS = "0";

  for (const step of GATE_STEPS) {
    log(`${prefix}: ${step.label}`);
    const status = runStep(step);
    if (status !== 0) {
      return status ?? 1;
    }
  }

  log(`${prefix}: gate passed`);
  return 0;
}

function nodeModulesPresent(root) {
  try {
    return fs.statSync(path.join(root, "node_modules")).isDirectory();
  } catch {
    return false;
  }
}

function python3Present() {
  return spawnSync("python3", ["--version"], { stdio: "ignore" }).status === 0;
}

// engines.node is the contract; .nvmrc is only quoted in the error message.
function declaredEngines(root) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8")).engines?.node;
  } catch {
    return undefined;
  }
}

function nvmrcPin(root) {
  try {
    return fs.readFileSync(path.join(root, ".nvmrc"), "utf8").trim() || undefined;
  } catch {
    return undefined;
  }
}

function listMatterDirs(root) {
  const dir = path.join(root, "documents");
  try {
    return fs
      .readdirSync(dir, { withFileTypes: true })
      .filter((entry) => entry.isDirectory() && entry.name.startsWith("matter-"))
      .map((entry) => entry.name);
  } catch {
    return [];
  }
}

/** True when every public (non-denylist) manifest PDF exists under documents/. */
export function publicDocumentsTreeComplete(root = repoRoot) {
  const documentsRoot = path.join(root, "documents");
  if (!fs.existsSync(documentsRoot)) return false;
  const expected = (loadManifest().files ?? []).filter(
    (f) => !isPrivateDocument(f) && String(f.path ?? "").toLowerCase().endsWith(".pdf"),
  );
  if (!expected.length) return false;
  return expected.every((f) => fs.existsSync(diskFromUrl(f.path)));
}

function readStdinSync() {
  if (process.stdin.isTTY) return "";
  try {
    return fs.readFileSync(0, "utf8");
  } catch {
    return "";
  }
}

function spawnStep(step) {
  const [command, ...args] = step.argv;
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    env: process.env,
    stdio: "inherit",
  });
  return result.status ?? 1;
}

function main() {
  const hookMode = process.argv.includes("--hook");
  const code = runPortfolioGate({
    hookMode,
    stdinText: hookMode ? readStdinSync() : "",
    env: process.env,
    nodeModulesExists: nodeModulesPresent(repoRoot),
    python3Available: python3Present(),
    nodeVersion: process.versions.node,
    enginesRange: declaredEngines(repoRoot),
    nvmrcVersion: nvmrcPin(repoRoot),
    matterDirNames: listMatterDirs(repoRoot),
    diskComplete: publicDocumentsTreeComplete(repoRoot),
    runStep: spawnStep,
  });
  process.exit(code);
}

const invokedDirectly =
  Boolean(process.argv[1]) && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedDirectly) {
  main();
}
