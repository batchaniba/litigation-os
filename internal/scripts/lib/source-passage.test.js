import { describe, expect, it } from "vitest";
import { verifySourcePassage, passageReviewPacket } from "./source-passage.mjs";

describe("source passage verification", () => {
  it("normalizes whitespace without changing words or case", () => {
    expect(verifySourcePassage({ quote: "The motion is denied.", text: "The motion\n is   denied." }).status).toBe("matched");
    expect(verifySourcePassage({ quote: "The motion is granted.", text: "The motion is denied." }).status).toBe("not_found");
    expect(verifySourcePassage({ quote: "the motion", text: "The motion" }).status).toBe("not_found");
  });
  it("requires a match on the selected extraction page", () => {
    const text = "First page\fSecond page";
    expect(verifySourcePassage({ quote: "Second page", text, page: 1 }).status).toBe("not_found");
    expect(verifySourcePassage({ quote: "Second page", text, page: 2 }).page_verified).toBe(true);
    expect(verifySourcePassage({ quote: "First page", text: "First page", page: 1 }).status).toBe("page_unverifiable");
  });
  it("does not silently accept omissions or bracketed substitutions", () => {
    expect(verifySourcePassage({ quote: "The ... denied.", text: "The motion is denied." }).status).toBe("not_found");
    expect(verifySourcePassage({ quote: "The [request] is denied.", text: "The motion is denied." }).status).toBe("not_found");
  });
  it("returns surrounding qualifications and every occurrence", () => {
    const result = verifySourcePassage({ quote: "Rule applies", text: "Rule applies only here. Rule applies unless waived." });
    expect(result.matches.length).toBe(2);
    expect(result.matches[0].context.includes("only here")).toBe(true);
  });
  it("rejects invalid page numbers and empty quotes", () => {
    expect(() => verifySourcePassage({ quote: "x", text: "x", page: 0 })).toThrow("page");
    expect(() => verifySourcePassage({ quote: " ", text: "x" })).toThrow("quote");
  });
  it("quotation presence never marks proposition fit as verified", () => {
    const packet = passageReviewPacket({ id: "p", statement: "Synthetic claim" },
      { id: "s", type: "authority", role: "supports", quote: "Rule", locator: "synthetic", pinpoint: "1" },
      { status: "matched", matches: [] });
    expect(packet.relationship_status).toBe("requires_substantive_review");
    expect(packet.questions.length).toBe(4);
  });
});
