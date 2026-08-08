import { describe, expect, it } from "vitest";
import { documentRegistry, getRegistryEntry, resolveDocument, resolveDocuments } from "./documents";
import { loadMatter } from "./matters";

describe("document registry", () => {
  it("registers unique paths including outcomes-only opinions", () => {
    const paths = documentRegistry.map((entry) => entry.path);
    expect(new Set(paths).size).toBe(paths.length);
    expect(paths.length).toBeGreaterThan(490);
    expect(
      paths.some((p) => p.startsWith("/documents/opinions/")),
    ).toBe(true);
  });

  it("resolves bare matter refs from the registry canonical label", () => {
    const path = "/documents/matter-33/incident/Arrest Report.pdf";
    const entry = getRegistryEntry(path);
    expect(entry?.ownerMatter).toBe(33);
    expect(resolveDocument({ path, filed: false })).toEqual({
      path,
      label: entry.label,
      filed: false,
    });
  });

  it("keeps matter-level label overrides", () => {
    const path = "/documents/matter-33/incident/Arrest Report.pdf";
    const resolved = resolveDocument({
      path,
      label: "CHP Arrest-Investigation Report (CHP Form 202, RJ68845, File No. 202400898)",
    });
    expect(resolved.label).toContain("Arrest-Investigation");
    expect(resolved.label).not.toBe(getRegistryEntry(path).label);
  });

  it("loadMatter returns resolved document labels for hub matters", async () => {
    const matter = await loadMatter(33);
    expect(matter.documents?.length).toBeGreaterThan(0);
    for (const doc of matter.documents ?? []) {
      expect(doc.path).toMatch(/^\/documents\//);
      expect(doc.label.trim()).not.toBe("");
    }
    const arrest = matter.documents.find((d) => d.path.endsWith("Arrest Report.pdf"));
    expect(arrest?.label).toBe(getRegistryEntry(arrest.path).label);
  });

  it("resolveDocuments maps empty input to []", () => {
    expect(resolveDocuments(undefined)).toEqual([]);
    expect(resolveDocuments([])).toEqual([]);
  });
});
