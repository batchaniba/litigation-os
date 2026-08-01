import type { Matter, MatterSummary } from "../../types/portfolio";
import summaries from "./summaries.json";

// Light records for list/search/dashboard — keep the shell bundle small.
export const cases = summaries as MatterSummary[];

// Full NN.json records are code-split and loaded on demand.
const matterLoaders = import.meta.glob(["./*.json", "!./summaries.json"]) as Record<
  string,
  () => Promise<{ default: Matter }>
>;

export function matterFileKey(number: number): string {
  return `./${String(number).padStart(2, "0")}.json`;
}

export function loadMatter(number: number): Promise<Matter> {
  const loader = matterLoaders[matterFileKey(number)];
  if (!loader) {
    return Promise.reject(new Error(`No matter JSON for number ${number}`));
  }
  return loader().then((mod) => {
    const matter = mod.default;
    if (matter.evidenceCount == null) {
      matter.evidenceCount = Array.isArray(matter.evidence) ? matter.evidence.length : 0;
    }
    return matter;
  });
}

export function getMatterSummary(number: number): MatterSummary | undefined {
  return cases.find((matter) => matter.number === number);
}
