import { describe, expect, it } from "vitest";
import spec from "../../src/data/documents/private-documents.json" with { type: "json" };
import {
  PRIVATE_DOCUMENT_PATHS,
  filterPublicDocuments,
  isPrivateDocument,
  isPrivatePath,
  isPrivateSha,
} from "./private-documents.mjs";

describe("private document denylist", () => {
  it("lists exactly 14 owner paths", () => {
    expect(PRIVATE_DOCUMENT_PATHS).toHaveLength(14);
    expect(spec.paths).toHaveLength(14);
  });

  it("blocks every hope-discovery HOPE_000 path, including a hash-suffixed copy", () => {
    expect(
      isPrivatePath(
        "/documents/matter-05/hope-discovery/HOPE_000224_Curriculum_Tracking_Audit.pdf",
      ),
    ).toBe(true);
    expect(
      isPrivatePath(
        "/documents/matter-05/hope-discovery/HOPE_000224_Curriculum_Tracking_Audit.root-aaf89e1d.pdf",
      ),
    ).toBe(true);
  });

  it("blocks both matter-12 card-authorization paths by path, and the aug31 alias by hash", () => {
    expect(
      isPrivatePath(
        "/documents/matter-12/018 Request for Sheriff Service + Fee Waiver : CC Auth — Ngwa Nforbi v. Diamond Truc.pdf",
      ),
    ).toBe(true);
    expect(
      isPrivatePath(
        "/documents/matter-12/reservice-packets-sep9/4_Stanislaus_Credit_Card_Authorization_Diamond.pdf",
      ),
    ).toBe(true);
    expect(
      isPrivateSha("9411c895fa4f3abbde5b31ae784af5b08d22a4d6275c605f0f22c911a09e5b31"),
    ).toBe(true);
    expect(
      isPrivatePath(
        "/documents/matter-12/reservice-packets-aug31/4_Stanislaus_Credit_Card_Authorization_Diamond.pdf",
      ),
    ).toBe(true);
    expect(
      isPrivatePath(
        "/documents/matter-28/HOPE Discovery (Matter 5)/1_PHCP06796815_Rdctd_131_pdf.pdf",
      ),
    ).toBe(true);
  });

  it("leaves ordinary filings public", () => {
    expect(isPrivatePath("/documents/matter-24/First Amended Complaint.pdf")).toBe(false);
    expect(isPrivateSha("a".repeat(64))).toBe(false);
    expect(
      isPrivateDocument({
        path: "/documents/matter-05/Minute Order - Demurrer Sustained WOLA (Jul 15 2026).pdf",
        sha256: "b".repeat(64),
      }),
    ).toBe(false);
  });

  it("defaults a newly added path to public unless it matches the denylist", () => {
    expect(
      isPrivateDocument({
        path: "/documents/matter-41/brand-new-filing.pdf",
        sha256: "d".repeat(64),
      }),
    ).toBe(false);
    expect(
      isPrivatePath("/documents/matter-05/hope-discovery/HOPE_000999_New_Production.pdf"),
    ).toBe(true);
  });

  it("filterPublicDocuments drops denylist rows and keeps the rest", () => {
    const rows = [
      { path: "/documents/matter-24/x.pdf", sha256: "a".repeat(64) },
      {
        path: "/documents/matter-05/hope-discovery/HOPE_000001-031_Professional_Liability_Policy.pdf",
        sha256: "9c6b98a0ccf500f2894028f6b50f5e6538d4561c8f4681e9dca45858e8e2e7cc",
      },
    ];
    expect(filterPublicDocuments(rows)).toEqual([rows[0]]);
  });
});
