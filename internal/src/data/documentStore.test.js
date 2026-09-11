import { mkdtempSync, writeFileSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";
import { tmpdir } from "node:os";
import { describe, expect, it } from "vitest";
import {
  buildManifestFromDisk,
  copyPublicExceptDocumentsFilter,
  diskFromUrl,
  hashFileSha256,
  publicRel,
  skipDiskDocs,
  skipViteDocumentCopy,
  urlFromPublicRel,
} from "../../scripts/lib/document-store.mjs";

describe("skipDiskDocs", () => {
  it("reads the flag from argv or env", () => {
    expect(skipDiskDocs({ argv: ["node", "x"], env: {} })).toBe(false);
    expect(skipDiskDocs({ argv: ["node", "x", "--skip-disk-docs"], env: {} })).toBe(true);
    expect(skipDiskDocs({ argv: ["node"], env: { PORTFOLIO_SKIP_DISK_DOCS: "1" } })).toBe(true);
    expect(skipDiskDocs({ argv: ["node"], env: { PORTFOLIO_SKIP_DISK_DOCS: "true" } })).toBe(true);
    expect(skipDiskDocs({ argv: ["node"], env: { PORTFOLIO_SKIP_DISK_DOCS: "0" } })).toBe(false);
  });
});

describe("skipViteDocumentCopy", () => {
  it("is opt-in via VITE_COPY_DOCUMENTS=0", () => {
    expect(skipViteDocumentCopy({ env: {} })).toBe(false);
    expect(skipViteDocumentCopy({ env: { VITE_COPY_DOCUMENTS: "0" } })).toBe(true);
    expect(skipViteDocumentCopy({ env: { VITE_COPY_DOCUMENTS: "1" } })).toBe(false);
  });
});

describe("public path helpers", () => {
  it("round-trips a documents URL", () => {
    const publicRoot = "/repo/internal/public";
    const abs = path.join(publicRoot, "documents", "matter-05", "complaint.pdf");
    expect(publicRel(abs, publicRoot)).toBe("documents/matter-05/complaint.pdf");
    expect(urlFromPublicRel("documents/matter-05/complaint.pdf")).toBe(
      "/documents/matter-05/complaint.pdf",
    );
    expect(diskFromUrl("/documents/matter-05/complaint.pdf", publicRoot)).toBe(
      path.join(publicRoot, "documents", "matter-05", "complaint.pdf"),
    );
  });
});

describe("copyPublicExceptDocumentsFilter", () => {
  const publicRoot = "/repo/internal/public";

  it("keeps the public root, logos, and short-link slugs", () => {
    expect(copyPublicExceptDocumentsFilter(publicRoot, publicRoot)).toBe(true);
    expect(copyPublicExceptDocumentsFilter(path.join(publicRoot, "logo-dark.webp"), publicRoot)).toBe(
      true,
    );
    expect(copyPublicExceptDocumentsFilter(path.join(publicRoot, "fedex-consent.pdf"), publicRoot)).toBe(
      true,
    );
    expect(copyPublicExceptDocumentsFilter(path.join(publicRoot, "branding"), publicRoot)).toBe(true);
  });

  it("drops the documents tree and everything under it", () => {
    expect(copyPublicExceptDocumentsFilter(path.join(publicRoot, "documents"), publicRoot)).toBe(
      false,
    );
    expect(
      copyPublicExceptDocumentsFilter(
        path.join(publicRoot, "documents", "matter-05", "complaint.pdf"),
        publicRoot,
      ),
    ).toBe(false);
  });
});

describe("buildManifestFromDisk", () => {
  it("inventories files with size and sha256, skipping dotfiles", () => {
    const dir = mkdtempSync(path.join(tmpdir(), "doc-manifest-"));
    try {
      const documents = path.join(dir, "documents");
      mkdirSync(path.join(documents, "matter-01"), { recursive: true });
      writeFileSync(path.join(documents, "matter-01", "a.pdf"), "%PDF-1.4\n");
      writeFileSync(path.join(documents, "matter-01", ".gitkeep"), "ignore\n");
      const manifest = buildManifestFromDisk(documents, dir);
      expect(manifest.fileCount).toBe(1);
      expect(manifest.files[0].path).toBe("/documents/matter-01/a.pdf");
      expect(manifest.files[0].size).toBe("%PDF-1.4\n".length);
      expect(manifest.files[0].sha256).toBe(
        hashFileSha256(path.join(documents, "matter-01", "a.pdf")),
      );
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
