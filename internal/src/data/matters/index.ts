import type { MatterSummary } from "../../types/portfolio";
import summaries from "./summaries.json";

// Light records for list/search/dashboard — keep the shell bundle small.
// Full records: `loadMatter` in ./loadMatter.ts (not re-exported from here).
export const cases = summaries as MatterSummary[];

export function getMatterSummary(number: number): MatterSummary | undefined {
  return cases.find((matter) => matter.number === number);
}
