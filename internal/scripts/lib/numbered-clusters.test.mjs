import { describe, expect, it } from "vitest";
import {
  CLUSTERS,
  clusterHeadingLine,
  collectNumberedClusterIssues,
  parseMatterRangeList,
} from "./numbered-clusters.mjs";

const CANONICAL = Object.fromEntries(CLUSTERS.map((c) => [c.n, c.label]));

/** Headings + TOC copied from the inverted README that this check exists to catch. */
const INVERTED_README = `
- [3 — Consumer Fraud / Defective Vehicle](#cluster-3--consumer-fraud--defective-vehicle-matter-12)
- [5 — Employment / Statutory Violation](#cluster-5--employment--statutory-violation-matters-22-25-26-27-29-31-36-39)

### Cluster 3 — Consumer Fraud / Defective Vehicle (Matter 12)
### Cluster 5 — Employment / Statutory Violation (Matters 22, 25, 26, 27, 29, 31, 36-40)
`;

const SAMPLE_MATTERS = [
  { number: 12, cluster: 5 },
  { number: 22, cluster: 3 },
  { number: 26, cluster: 3 },
  { number: 1, cluster: 1 },
  { number: 3, cluster: 2 },
  { number: 9, cluster: 4 },
  { number: 35, cluster: 6 },
];

function headingsFor(matters) {
  return CLUSTERS.map((c) => {
    const nums = matters.filter((m) => m.cluster === c.n).map((m) => m.number);
    return clusterHeadingLine(c.n, nums);
  }).join("\n");
}

describe("parseMatterRangeList", () => {
  it("expands en-dash and hyphen ranges", () => {
    expect(parseMatterRangeList("22, 25–27, 31, 36-39")).toEqual([
      22, 25, 26, 27, 31, 36, 37, 38, 39,
    ]);
  });
});

describe("collectNumberedClusterIssues", () => {
  it("fails the old README inversion (3 = Consumer Fraud, 5 = Employment)", () => {
    const errors = collectNumberedClusterIssues({
      matters: SAMPLE_MATTERS,
      readme: INVERTED_README,
      namedClusters: [{ id: "chp-nov2024" }, { id: "megan-law-employment" }],
    });
    expect(errors.some((e) => e.includes("README Cluster 3 heading") && e.includes(CANONICAL[3]))).toBe(
      true,
    );
    expect(errors.some((e) => e.includes("README Cluster 5 heading") && e.includes(CANONICAL[5]))).toBe(
      true,
    );
    expect(errors.some((e) => e.includes("README contents lists Cluster 3") && e.includes(CANONICAL[3]))).toBe(
      true,
    );
    expect(errors.some((e) => e.includes("README contents lists Cluster 5") && e.includes(CANONICAL[5]))).toBe(
      true,
    );
    // Matter 12 is Consumer Fraud (5); listing it under heading 3 is the inversion.
    expect(errors.some((e) => e.includes("README Cluster 3 lists matters") && e.includes("12"))).toBe(
      true,
    );
  });

  it("accepts headings generated from the canonical map and matter.cluster", () => {
    const readme = `
- [1 — ${CANONICAL[1]}](#cluster-1)
- [2 — ${CANONICAL[2]}](#cluster-2)
- [3 — ${CANONICAL[3]}](#cluster-3)
- [4 — ${CANONICAL[4]}](#cluster-4)
- [5 — ${CANONICAL[5]}](#cluster-5)
- [6 — ${CANONICAL[6]}](#cluster-6)

${headingsFor(SAMPLE_MATTERS)}
`;
    expect(
      collectNumberedClusterIssues({
        matters: SAMPLE_MATTERS,
        readme,
        namedClusters: [{ id: "chp-nov2024" }],
      }),
    ).toEqual([]);
  });

  it("fails an unknown matter.cluster id", () => {
    const errors = collectNumberedClusterIssues({
      matters: [{ number: 99, cluster: 7 }],
      readme: headingsFor(SAMPLE_MATTERS),
      namedClusters: [],
    });
    expect(errors.some((e) => e.includes("Matter 99") && e.includes("unknown numbered cluster"))).toBe(
      true,
    );
  });

  it("fails when a named-graph id is a numbered bucket", () => {
    const errors = collectNumberedClusterIssues({
      matters: SAMPLE_MATTERS,
      readme: `
- [1 — ${CANONICAL[1]}](#cluster-1)
- [2 — ${CANONICAL[2]}](#cluster-2)
- [3 — ${CANONICAL[3]}](#cluster-3)
- [4 — ${CANONICAL[4]}](#cluster-4)
- [5 — ${CANONICAL[5]}](#cluster-5)
- [6 — ${CANONICAL[6]}](#cluster-6)
${headingsFor(SAMPLE_MATTERS)}
`,
      namedClusters: [{ id: "3" }, { id: 5 }],
    });
    expect(errors.some((e) => e.includes('named cluster id "3"') && e.includes("numbered bucket"))).toBe(
      true,
    );
    expect(errors.some((e) => e.includes("named cluster id 5") && e.includes("numbered bucket"))).toBe(
      true,
    );
  });

  it("keeps Matter 12 in Consumer Fraud and Matter 26 in Employment", () => {
    expect(CANONICAL[5]).toMatch(/Consumer Fraud/);
    expect(CANONICAL[3]).toMatch(/Employment/);
    expect(clusterHeadingLine(5, [12])).toBe(
      `### Cluster 5 — ${CANONICAL[5]} (Matter 12)`,
    );
    expect(clusterHeadingLine(3, [22, 26])).toBe(
      `### Cluster 3 — ${CANONICAL[3]} (Matters 22, 26)`,
    );
  });
});
