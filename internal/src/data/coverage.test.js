import { describe, expect, it } from "vitest";
import { insurance_coverage, coverageForMatter, headline_coverage, formatLimit } from "./coverage";

describe("insurance coverage data", () => {
  it("names every insured and keeps per-incident within the aggregate", () => {
    for (const record of insurance_coverage) {
      expect(record.insureds.length).toBeGreaterThan(0);
      expect(record.perIncident).toBeGreaterThan(0);
      expect(record.aggregate).toBeGreaterThanOrEqual(record.perIncident);
      expect(record.carrier).toBeTruthy();
      expect(record.policyNo).toBeTruthy();
    }
  });

  it("carries the HOPE / Shannon Smith tower on matter 28", () => {
    const record = coverageForMatter(28);
    expect(record).toBeDefined();
    expect(record.limitsShort).toBe("$1M / $5M");
    expect(record.perIncident).toBe(1_000_000);
    expect(record.aggregate).toBe(5_000_000);
    expect(record.insureds).toEqual(
      expect.arrayContaining(["HOPE Psychotherapy, Inc.", "Shannon Smith, LCSW"]),
    );
  });

  it("resolves a matter number given as a string", () => {
    expect(coverageForMatter("28")).toBe(coverageForMatter(28));
  });

  it("returns undefined for matters with no policy on file", () => {
    expect(coverageForMatter(12)).toBeUndefined();
  });

  it("features the largest aggregate tower portfolio-wide", () => {
    const largest = Math.max(...insurance_coverage.map((r) => r.aggregate));
    expect(headline_coverage.aggregate).toBe(largest);
  });

  it("formats limits compactly", () => {
    expect(formatLimit(1_000_000)).toBe("$1M");
    expect(formatLimit(5_000_000)).toBe("$5M");
    expect(formatLimit(1_500_000)).toBe("$1.5M");
    expect(formatLimit(250_000)).toBe("$250K");
  });

  it("keeps limitsShort consistent with the numeric limits it displays", () => {
    for (const record of insurance_coverage) {
      expect(record.limitsShort).toBe(
        `${formatLimit(record.perIncident)} / ${formatLimit(record.aggregate)}`,
      );
    }
  });
});
