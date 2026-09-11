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
import { PAGES_DOCUMENTS_ORIGIN, vercelSpaRewrites } from "../../scripts/lib/documents-branch.mjs";

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

describe("vercelSpaRewrites", () => {
  it("proxies /documents/* to GitHub Pages ahead of the SPA fallback", () => {
    const rewrites = vercelSpaRewrites();
    expect(rewrites[0]).toEqual({
      source: "/documents/:path*",
      destination: `${PAGES_DOCUMENTS_ORIGIN}/:path*`,
    });
    expect(rewrites[1]).toEqual({ source: "/(.*)", destination: "/index.html" });
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

  it("reuses a previous hash when the path still has the same size", () => {
    const dir = mkdtempSync(path.join(tmpdir(), "doc-manifest-inc-"));
    try {
      const documents = path.join(dir, "documents");
      mkdirSync(path.join(documents, "matter-01"), { recursive: true });
      const file = path.join(documents, "matter-01", "a.pdf");
      writeFileSync(file, "A");
      const previous = {
        files: [{ path: "/documents/matter-01/a.pdf", size: 1, sha256: "deadbeef" }],
      };
      const reused = buildManifestFromDisk(documents, dir, { previous });
      expect(reused.files[0].sha256).toBe("deadbeef");
      const hashed = buildManifestFromDisk(documents, dir, { previous, rehash: true });
      expect(hashed.files[0].sha256).toBe(hashFileSha256(file));
      expect(hashed.files[0].sha256).not.toBe("deadbeef");
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  it("hashes a new path even when a previous inventory exists", () => {
    const dir = mkdtempSync(path.join(tmpdir(), "doc-manifest-new-"));
    try {
      const documents = path.join(dir, "documents");
      mkdirSync(path.join(documents, "matter-01"), { recursive: true });
      const file = path.join(documents, "matter-01", "b.pdf");
      writeFileSync(file, "%PDF-1.4\n");
      const incremental = buildManifestFromDisk(documents, dir, {
        previous: { files: [] },
      });
      expect(incremental.files[0].sha256).toBe(hashFileSha256(file));
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
