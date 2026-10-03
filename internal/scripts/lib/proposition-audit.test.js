import { describe, expect, it } from "vitest";
import { auditPropositions } from "./proposition-audit.mjs";

const proposition = () => ({
  id: "example", statement: "Synthetic assertion, not a case fact.",
  factual_status: "allegation", sources: [], proof_gaps: [], objections: [],
});
describe("proposition audit", () => {
  it("does not treat an assertion as supported without sources", () => {
    const result = auditPropositions({ propositions: [proposition()] });
    expect(result.summary.needs_review).toBe(1);
    expect(result.propositions[0].issues.map((i) => i.code))
      .toEqual(["no_supporting_record", "no_supporting_authority"]);
  });
  it("retrieval alone cannot satisfy review", () => {
    const p = proposition();
    p.sources = [{ id: "a", type: "authority", role: "supports",
      locator: "synthetic:test", pinpoint: "p. 1", quote: "Synthetic passage.",
      retrieved_at: "2026-10-03" }];
    expect(auditPropositions({ propositions: [p] }).propositions[0].issues)
      .toContainEqual({ code: "source_not_reviewed", source: "a" });
  });
  it("rejects orphan objection references and duplicate propositions", () => {
    const p = proposition();
    p.objections = [{ statement: "Challenge", response: "Reply", response_source_ids: ["missing"] }];
    expect(() => auditPropositions({ propositions: [p] })).toThrow("unknown source");
    expect(() => auditPropositions({ propositions: [proposition(), proposition()] })).toThrow("duplicate");
  });
  it("keeps adverse sources visible after review", () => {
    const p = proposition();
    p.sources = [{ id: "a", type: "record", role: "opposes", locator: "synthetic:test",
      pinpoint: "p. 1", quote: "Synthetic passage.", review: {
        reviewer: "test", reviewed_at: "2026-10-03", reason: "Synthetic review",
        relationship: "supports", foundation_checked: true,
      } }];
    const issues = auditPropositions({ propositions: [p] }).propositions[0].issues;
    expect(issues).toContainEqual({ code: "relationship_mismatch", source: "a" });
    expect(issues).toContainEqual({ code: "adverse_source_present", source: null });
  });
});
