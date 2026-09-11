import { describe, expect, it } from "vitest";
import {
  PROSE_BUDGETS,
  PROSE_FIELDS,
  PROSE_HINTS,
  docketLogIssues,
  docketLogSignals,
  proseBudgetIssues,
  wordCount,
} from "../utils/proseBudget";
import * as scriptModule from "../../scripts/prose-budget.mjs";

// Full matter records — summaries.json deliberately strips the prose fields,
// so the budgets have to be checked against the NN.json sources.
const matterModules = import.meta.glob(
  ["./matters/*.json", "!./matters/summaries.json", "!./matters/document-index.json"],
  { eager: true },
);

const matters = Object.entries(matterModules)
  .map(([path, mod]) => ({ path, matter: mod.default }))
  .sort((a, b) => a.matter.number - b.matter.number);

describe("prose length budgets", () => {
  it("loads every matter record", () => {
    expect(matters.length).toBe(39);
  });

  it("counts words without being fooled by runs of whitespace", () => {
    expect(wordCount("  one   two\n\nthree ")).toBe(3);
    expect(wordCount("")).toBe(0);
    expect(wordCount(undefined)).toBe(0);
  });

  it("flags a field over its authoring target and never invents a ceiling", () => {
    const issues = proseBudgetIssues({
      key_facts: Array.from({ length: 400 }, () => "word").join(" "),
      procedural_status: "short",
      risk: "short",
      status: "short",
    });
    expect(issues).toEqual([
      { field: "key_facts", words: 400, target: 350, level: "over-target" },
    ]);
  });

  it("carries an actionable hint for every budgeted field", () => {
    for (const field of PROSE_FIELDS) {
      expect(PROSE_HINTS[field], field).toBeTruthy();
    }
  });

  it("mirrors the script-side budgets used by the validator", () => {
    expect(scriptModule.PROSE_BUDGETS).toEqual(PROSE_BUDGETS);
    expect(scriptModule.PROSE_FIELDS).toEqual(PROSE_FIELDS);
    expect(scriptModule.PROSE_HINTS).toEqual(PROSE_HINTS);
    expect(scriptModule.wordCount("  one   two ")).toBe(wordCount("  one   two "));
    expect(typeof scriptModule.docketLogIssues).toBe("function");
    expect(typeof scriptModule.docketLogSignals).toBe("function");
  });

  it("flags dense docket-log prose and ignores short posture sentences", () => {
    const log =
      "SERVED July 24, 2026 on FedEx. COMPUTED: responsive pleading due August 24, 2026. " +
      "PUNITIVE AMOUNT REVISED — AUGUST 7, 2026: notice executed. SERVICE CONFIRMED July 31, 2026. " +
      "FILING — JULY 28, 2026 completed. ACTION ITEM: serve amended notice before August 31, 2026.";
    expect(docketLogSignals(log).score).toBeGreaterThanOrEqual(2);
    expect(docketLogIssues({ status: log, procedural_status: "Short posture." })).toHaveLength(1);

    const posture =
      "Filed July 15, 2026. Served July 24, 2026; responsive pleading due Aug. 24, 2026.";
    expect(docketLogSignals(posture).score).toBeLessThan(2);
  });
});
