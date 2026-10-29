import { describe, expect, it } from "vitest";
import {
  BLENDED_HOURLY_RATE,
  costFromHours,
  FEE_CLUSTER_DEFS,
  summarizeLawyerFees,
  withDerivedCost,
} from "./lawyerFeeMath";
import { lawyer_fees, lawyer_fees_summary } from "./lawyerFees";
import summaries from "./matters/summaries.json";

describe("lawyerFeeMath", () => {
  it("prices hours at the blended rate", () => {
    expect(BLENDED_HOURLY_RATE).toBe(280);
    expect(costFromHours({ low: 1, mid: 1.75, high: 2.5 })).toEqual({
      low: 280,
      mid: 490,
      high: 700,
    });
  });

  it("overwrites a stale cost block from hours", () => {
    const row = withDerivedCost({
      number: 41,
      hours: { low: 1, mid: 1.75, high: 2.5 },
      cost: { low: 1, mid: 2, high: 3 },
    });
    expect(row.cost).toEqual({ low: 280, mid: 490, high: 700 });
  });

  it("refuses to summarize a row whose numbered cluster is unmapped", () => {
    expect(() =>
      summarizeLawyerFees([
        {
          number: 99,
          cluster: 99,
          documentsCount: 0,
          totalPagesReal: 0,
          hours: { low: 0, mid: 0, high: 0 },
          cost: { low: 0, mid: 0, high: 0 },
        },
      ]),
    ).toThrow(/missing a fee-cluster mapping/);
  });
});

describe("lawyer_fees coverage", () => {
  const byNumber = new Map(lawyer_fees.map((row) => [row.number, row]));

  it("has a fee row for every tracked matter", () => {
    const missing = summaries.map((m) => m.number).filter((n) => !byNumber.has(n));
    expect(missing).toEqual([]);
    expect(lawyer_fees_summary.totalMatters).toBe(summaries.length);
    expect(lawyer_fees_summary.trackedMatters).toBe(summaries.length);
  });

  it("derives every exported cost from hours × blended rate", () => {
    for (const row of lawyer_fees) {
      expect(row.cost, `M${row.number}`).toEqual(costFromHours(row.hours));
      expect(row.hours.mid).toBeGreaterThanOrEqual(row.hours.low);
      expect(row.hours.high).toBeGreaterThanOrEqual(row.hours.mid);
    }
  });

  it("derives summary totals and cluster rollups from the rows", () => {
    const derived = summarizeLawyerFees(lawyer_fees, {
      analysisDate: lawyer_fees_summary.analysisDate,
      trackedMatters: summaries.length,
      methodologyNote: lawyer_fees_summary.methodology.note,
    });
    expect(lawyer_fees_summary.totalEstimatedCost).toEqual(derived.totalEstimatedCost);
    expect(lawyer_fees_summary.totalEstimatedHours).toEqual(derived.totalEstimatedHours);
    expect(lawyer_fees_summary.totalDocumentsAnalyzed).toBe(derived.totalDocumentsAnalyzed);
    expect(lawyer_fees_summary.totalPagesReal).toBe(derived.totalPagesReal);
    expect(lawyer_fees_summary.byCluster).toEqual(derived.byCluster);
  });

  it("places every fee row in exactly one fee cluster", () => {
    const clustered = Object.values(lawyer_fees_summary.byCluster).flatMap((c) => c.matters);
    expect([...clustered].sort((a, b) => a - b)).toEqual(
      lawyer_fees.map((row) => row.number).sort((a, b) => a - b),
    );
    expect(new Set(clustered).size).toBe(clustered.length);
  });

  it("maps numbered matter clusters onto the fee-tab rollups", () => {
    for (const row of lawyer_fees) {
      const def = FEE_CLUSTER_DEFS.find((d) => d.numbered.includes(row.cluster));
      expect(def, `M${row.number} cluster ${row.cluster}`).toBeTruthy();
      expect(lawyer_fees_summary.byCluster[def.id].matters).toContain(row.number);
    }
  });
});
