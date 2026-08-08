import { describe, expect, it } from "vitest";
import { getMatterIdentity, withMatterIdentity } from "./matterIdentity";
import { matter_damages } from "./damages";
import { lawyer_fees } from "./lawyerFees";
import { coverageForMatter } from "./coverage";
import { outcomes } from "./outcomes";
import summaries from "./matters/summaries.json";

describe("matter identity joins", () => {
  it("resolves caption/case_no/court from summaries", () => {
    const identity = getMatterIdentity(1);
    const summary = summaries.find((m) => m.number === 1);
    expect(identity).toMatchObject({
      number: 1,
      caption: summary.caption,
      case_no: summary.case_no,
      court: summary.court,
    });
  });

  it("lets row-level caption overrides win", () => {
    const joined = withMatterIdentity(
      { matter: 27, caption: "Newanforbi v. RK Logistics Group, Inc." },
      { numberKey: "matter" },
    );
    expect(joined.caption).toBe("Newanforbi v. RK Logistics Group, Inc.");
    expect(joined.case_no).toBe(getMatterIdentity(27).case_no);
  });

  it("enriches damages and fee rows without storing status copies", () => {
    for (const row of matter_damages) {
      expect(row.caption).toBeTruthy();
      expect(row.court).toBeTruthy();
      expect(row.status).toBeUndefined();
    }
    for (const row of lawyer_fees) {
      expect(row.caption).toBeTruthy();
      expect(row.caseNumber).toBeTruthy();
      expect(row.court).toBeTruthy();
      expect(row.status).toBeUndefined();
    }
  });

  it("joins coverage identity for matter 28", () => {
    const record = coverageForMatter(28);
    const summary = summaries.find((m) => m.number === 28);
    expect(record.caption).toBe(summary.caption);
    expect(record.caseNo).toBe(summary.case_no);
    expect(record.court).toBe(summary.court);
  });

  it("joins outcomes case numbers from matter identity", () => {
    const settled = outcomes.realized[0];
    const summary = summaries.find((m) => m.number === settled.matter);
    expect(settled.caption).toBe(summary.caption);
    expect(settled.case_no).toBe(summary.case_no);
    expect(settled.court).toBe(summary.court);
  });

  it("keeps shell summaries free of full status prose", () => {
    for (const matter of summaries) {
      expect(matter.status, `matter ${matter.number}`).toBeUndefined();
    }
  });
});
