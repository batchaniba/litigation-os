// Single source for the repo root. Honors PORTFOLIO_ROOT for testing
// write operations against a scratch copy: run any script with
//   PORTFOLIO_ROOT=/tmp/pf-test node internal/scripts/q.mjs ...
import path from "node:path";
import { fileURLToPath } from "node:url";

export const REPO_ROOT =
  process.env.PORTFOLIO_ROOT ||
  path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
