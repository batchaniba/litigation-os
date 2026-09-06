#!/usr/bin/env node
// Point git at .githooks when this clone has a .git directory.
// npm's `prepare` script runs this after install so a fresh clone
// picks up the pre-commit sync without husky.
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
if (!fs.existsSync(path.join(repoRoot, ".git"))) process.exit(0);

execSync("git config core.hooksPath .githooks", { cwd: repoRoot, stdio: "inherit" });
