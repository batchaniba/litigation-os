import { describe, expect, it } from "vitest";
import {
  buildPathIndex,
  contentDispositionForPath,
  documentsKeyFromUrl,
  sha256ForPath,
} from "./documents.mjs";

const SHA = "a".repeat(64);

describe("documents path map", () => {
  it("normalizes encoded /documents paths", () => {
    expect(documentsKeyFromUrl("/documents/matter-26/foo.pdf")).toBe(
      "/documents/matter-26/foo.pdf",
    );
    expect(
      documentsKeyFromUrl("/documents/matter-26/Dkt%2010%20%28Filed%29.pdf"),
    ).toBe("/documents/matter-26/Dkt 10 (Filed).pdf");
  });

  it("resolves sha256 from the committed manifest map", () => {
    const index = buildPathIndex([{ path: "/documents/matter-26/foo.pdf", sha256: SHA }]);
    expect(sha256ForPath(index, "/documents/matter-26/foo.pdf")).toBe(SHA);
    expect(sha256ForPath(index, "/missing.pdf")).toBeNull();
  });

  it("a replacement at the same path points at the new sha256", () => {
    const first = "a".repeat(64);
    const redraft = "b".repeat(64);
    const index = buildPathIndex([
      { path: "/documents/matter-32/decl.pdf", sha256: first },
      { path: "/documents/matter-32/decl.pdf", sha256: redraft },
    ]);
    expect(index["/documents/matter-32/decl.pdf"]).toBe(redraft);
    expect(sha256ForPath(index, "/documents/matter-32/decl.pdf")).toBe(redraft);
  });

  it("omits the 14-path private denylist from the public path index", () => {
    const priv =
      "/documents/matter-12/reservice-packets-sep9/4_Stanislaus_Credit_Card_Authorization_Diamond.pdf";
    const index = buildPathIndex([
      { path: "/documents/matter-26/foo.pdf", sha256: SHA },
      { path: priv, sha256: "9411c895fa4f3abbde5b31ae784af5b08d22a4d6275c605f0f22c911a09e5b31" },
    ]);
    expect(index["/documents/matter-26/foo.pdf"]).toBe(SHA);
    expect(index[priv]).toBeUndefined();
  });

  it("names Content-Disposition from the court filename, not the hash", () => {
    expect(contentDispositionForPath("/documents/matter-32/ndcal/Declaration.pdf")).toBe(
      'inline; filename="Declaration.pdf"',
    );
  });
});
