import { describe, expect, it } from "vitest";
import {
  analyzeClients,
  analyzeSubjects,
  identityConfidence,
  normalizeClientName,
  splitCaseName,
} from "./counsel-dossier.mjs";

describe("splitCaseName", () => {
  it("splits plaintiff v. defendant", () => {
    expect(splitCaseName("Zorayda Mariscal v. Appfolio, Inc.")).toEqual({
      plaintiff: "Zorayda Mariscal",
      defendant: "Appfolio, Inc.",
    });
  });

  it("handles vs. and strips et al.", () => {
    expect(splitCaseName("Smith vs. Acme Corp. et al.")).toEqual({
      plaintiff: "Smith",
      defendant: "Acme Corp.",
    });
  });

  it("returns null when there is no separator", () => {
    expect(splitCaseName("In re Something")).toBeNull();
    expect(splitCaseName("")).toBeNull();
    expect(splitCaseName(null)).toBeNull();
  });
});

describe("normalizeClientName", () => {
  it("strips entity suffixes for clustering", () => {
    const a = normalizeClientName("First Advantage Background Services Corp.");
    const b = normalizeClientName("First Advantage Background Services, Inc.");
    expect(a.key).toBe(b.key);
    expect(a.key).toContain("first advantage");
  });

  it("keeps a display form", () => {
    expect(normalizeClientName("DISA Global Solutions Inc.").display).toContain("DISA");
  });
});

describe("analyzeClients", () => {
  const sample = [
    { case_name: "Boyer v. First Advantage Background Services Corp." },
    { case_name: "Bosco v. First Advantage Background Services Corp." },
    { case_name: "Zorayda Mariscal v. Appfolio, Inc." },
    { case_name: "Smith v. DISA Global Solutions Inc." },
  ];

  it("ranks repeat defendants first", () => {
    const clients = analyzeClients(sample);
    expect(clients.top_defendant.count).toBe(2);
    expect(clients.top_defendant.name).toMatch(/First Advantage/);
    expect(clients.defendants).toHaveLength(3);
    expect(clients.cases_parsed).toBe(4);
  });

  it("skips cases without a parseable name", () => {
    const clients = analyzeClients([{ case_name: "In re Mystery" }, ...sample]);
    expect(clients.cases_parsed).toBe(4);
  });

  it("handles empty input", () => {
    expect(analyzeClients([]).defendants).toEqual([]);
    expect(analyzeClients(null).top_defendant).toBeNull();
  });
});

describe("analyzeSubjects", () => {
  it("detects the screening ecosystem from CRA defendants", () => {
    const subjects = analyzeSubjects([
      { case_name: "Boyer v. First Advantage Background Services Corp." },
      { case_name: "Smith v. DISA Global Solutions Inc." },
      { case_name: "Jones v. Equifax Information Services LLC" },
    ]);
    expect(subjects.primary).toBe("fcra_background_screening");
    expect(subjects.screening_ecosystem.detected).toBe(true);
    expect(subjects.screening_ecosystem.matched_cra_clients).toEqual(
      expect.arrayContaining(["first advantage", "disa", "equifax"]),
    );
  });

  it("detects employment subjects by keyword", () => {
    const subjects = analyzeSubjects([
      { case_name: "Doe v. Acme Inc. — wrongful termination and retaliation" },
    ]);
    expect(subjects.tags.employment_discrimination).toBe(1);
  });

  it("reports no primary when nothing matches", () => {
    const subjects = analyzeSubjects([{ case_name: "Smith v. Jones" }]);
    expect(subjects.primary).toBeNull();
    expect(subjects.screening_ecosystem.detected).toBe(false);
  });
});

describe("identityConfidence", () => {
  it("marks pinned attorney IDs as verified", () => {
    expect(identityConfidence({ attorney_id: 42 }).level).toBe("verified");
  });

  it("marks missing IDs as name-based", () => {
    const c = identityConfidence({ attorney_id: null });
    expect(c.level).toBe("name-based");
    expect(c.label).toMatch(/Name-based/);
  });
});
