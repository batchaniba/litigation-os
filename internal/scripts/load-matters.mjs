// Shared Node-side loader for matter JSON records.
// Vite uses import.meta.glob in internal/src/data/matters/index.ts;
// plain Node (validate, scaffold, index) reads the same files via fs.
//
// Two layouts, portfolio-wide:
//   legacy — internal/src/data/matters/NN.json
//   split  — internal/src/data/matters/NN/{matter,docket,clocks,...}.json
// Agents fetch the split files by path. This loader still returns the
// assembled Matter shape so the dashboard and existing scripts do not fork.
import path from "node:path";
import { fileURLToPath } from "node:url";
import { validateMatter } from "./lib/matter-schema.mjs";
import {
  legacyMatterPath,
  listMatterSources,
  loadSplitMatter,
  paddedMatterNumber,
  readJson,
} from "./lib/matter-layout.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const MATTERS_DIR = path.resolve(__dirname, "../src/data/matters");

export function loadMatters() {
  const sources = listMatterSources(MATTERS_DIR);
  const seen = new Set();
  const cases = sources.map((source) => {
    if (seen.has(source.number)) {
      throw new Error(
        `Matter ${source.number} has both ${paddedMatterNumber(source.number)}.json and a split folder — keep one layout`,
      );
    }
    seen.add(source.number);
    const matter =
      source.layout === "split"
        ? loadSplitMatter(source.dir)
        : Object.assign(readJson(source.abs), {
            __sourceFile: source.rel,
            __layout: "legacy",
          });
    const issues = validateMatter(matter);
    if (issues.length) {
      throw new Error(`matters/${source.rel} failed schema validation:\n  - ${issues.join("\n  - ")}`);
    }
    return matter;
  });

  cases.sort((a, b) => Number(a.number) - Number(b.number));
  return cases;
}

export function matterFileName(number) {
  return `${paddedMatterNumber(number)}.json`;
}

export function matterSourceRel(number, layout = "legacy") {
  return layout === "split"
    ? `${paddedMatterNumber(number)}/matter.json`
    : matterFileName(number);
}

export { legacyMatterPath, paddedMatterNumber };
