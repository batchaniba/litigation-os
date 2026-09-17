#!/usr/bin/env node
// Laptop Dependabot: no GitHub Actions.
//
//   npm run deps:outdated          # report npm + pip floors vs the registries
//   npm run deps:update            # npm update (in-range lockfile only)
//
// Majors are printed, not applied. TypeScript majors stay ignored.
// See .github/WORKFLOW_NOTES.md and .github/renovate.json (Mend app, optional).
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import {
  classifyNpm,
  formatReport,
  parseRequirementsTxt,
  pipStale,
} from "./lib/deps-outdated.mjs";
import { REPO_ROOT } from "./lib/root.mjs";

const args = new Set(process.argv.slice(2));
const apply = args.has("--apply");
const skipPip = args.has("--no-pip");
const jsonOut = args.has("--json");

function npmOutdated() {
  const result = spawnSync("npm", ["outdated", "--json"], {
    cwd: REPO_ROOT,
    encoding: "utf8",
  });
  if (result.error) throw result.error;
  // npm outdated: 0 = current, 1 = stale, anything else = failure.
  if (result.status !== 0 && result.status !== 1) {
    throw new Error((result.stderr || "").trim() || `npm outdated exited ${result.status}`);
  }
  const text = (result.stdout || "").trim();
  if (!text) return {};
  try {
    return JSON.parse(text);
  } catch {
    const err = (result.stderr || "").trim() || "npm outdated returned non-JSON";
    throw new Error(err);
  }
}

function npmUpdate() {
  const result = spawnSync("npm", ["update"], {
    cwd: REPO_ROOT,
    encoding: "utf8",
    stdio: "inherit",
  });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    throw new Error(`npm update exited ${result.status}`);
  }
}

async function pipReport() {
  const reqPath = path.join(REPO_ROOT, "requirements.txt");
  let text;
  try {
    text = readFileSync(reqPath, "utf8");
  } catch {
    return { stale: [], error: "requirements.txt missing" };
  }
  const rows = parseRequirementsTxt(text);
  const latestByName = new Map();
  try {
    await Promise.all(
      rows.map(async (row) => {
        const url = `https://pypi.org/pypi/${encodeURIComponent(row.name)}/json`;
        const res = await fetch(url, { headers: { accept: "application/json" } });
        if (!res.ok) throw new Error(`PyPI ${row.name}: HTTP ${res.status}`);
        const body = await res.json();
        latestByName.set(row.name, body?.info?.version ?? "");
      }),
    );
  } catch (err) {
    return { stale: [], error: err instanceof Error ? err.message : String(err) };
  }
  return { stale: pipStale(rows, latestByName) };
}

const npm = classifyNpm(npmOutdated());
const pip = skipPip ? null : await pipReport();
const report = { npm, pip };

if (jsonOut) {
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
} else {
  process.stdout.write(formatReport(report));
}

if (apply) {
  if (!npm.inRange.length) {
    console.log("Nothing in-range to apply.");
  } else {
    npmUpdate();
  }
  process.exit(0);
}

const stale =
  npm.inRange.length +
  npm.major.length +
  (pip && !pip.error ? pip.stale.length : 0);
process.exit(stale ? 1 : 0);
