import { describe, expect, it } from "vitest";
import { DOCUMENT_GROUPS, documentGroup, groupDocuments } from "./documentGroups";

const doc = (label: string, path = "/documents/matter-05/file.pdf") => ({ label, path });

describe("documentGroup", () => {
  it("classifies each group from the label", () => {
    expect(documentGroup(doc("Original Complaint (Doc 1)"))).toBe("Pleadings");
    expect(documentGroup(doc("Opposition to Demurrer"))).toBe("Motions & Briefs");
    expect(documentGroup(doc("Screening Order Dismissing Claims"))).toBe("Orders & Rulings");
    expect(documentGroup(doc("Special Interrogatories, Set One"))).toBe("Discovery");
    expect(documentGroup(doc("Exhibit A — dash camera still"))).toBe("Evidence & Exhibits");
    expect(documentGroup(doc("Proof of Service by Mail"))).toBe("Service");
    expect(documentGroup(doc("Meet-and-confer letter to counsel"))).toBe("Correspondence");
    expect(documentGroup(doc("Scratch notes"))).toBe("Other");
  });

  it("falls back to the path when the label is uninformative", () => {
    expect(documentGroup(doc("0.Newanforbi v. CHP", "/documents/matter-32/summons.pdf"))).toBe("Pleadings");
  });

  it("resolves overlaps by group order, not by which word appears first", () => {
    // "Complaint" and "Motion" both match; Pleadings is checked first and wins.
    expect(documentGroup(doc("Motion to Amend the Complaint"))).toBe("Pleadings");
  });

  it("is case-insensitive", () => {
    expect(documentGroup(doc("PETITION FOR WRIT OF HABEAS CORPUS"))).toBe("Pleadings");
  });
});

describe("groupDocuments", () => {
  it("returns groups in the declared order, omitting empty ones", () => {
    const grouped = groupDocuments([
      doc("Meet-and-confer letter"),
      doc("Original Complaint"),
      doc("Opposition to Demurrer"),
      doc("Second Amended Complaint"),
    ]);
    expect(grouped.map(([group]) => group)).toEqual(["Pleadings", "Motions & Briefs", "Correspondence"]);
    expect(grouped[0][1]).toHaveLength(2);
  });

  it("preserves input order inside a group", () => {
    const first = doc("Complaint A");
    const second = doc("Complaint B");
    expect(groupDocuments([first, second])[0][1]).toEqual([first, second]);
  });

  it("handles an empty or omitted list", () => {
    expect(groupDocuments([])).toEqual([]);
    expect(groupDocuments()).toEqual([]);
  });

  it("only ever emits declared groups", () => {
    const grouped = groupDocuments([doc("Something unclassifiable")]);
    expect(DOCUMENT_GROUPS).toContain(grouped[0][0]);
  });
});
