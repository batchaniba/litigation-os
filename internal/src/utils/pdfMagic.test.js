import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { hasPdfMagic, pdfReadableProblem } from "../../scripts/lib/pdfMagic.mjs";

describe("hasPdfMagic", () => {
  it("accepts a %PDF header", () => {
    expect(hasPdfMagic(Buffer.from("%PDF-1.7\n"))).toBe(true);
    expect(hasPdfMagic("%PDF")).toBe(true);
  });

  it("rejects empty, short, or non-PDF bytes", () => {
    expect(hasPdfMagic(Buffer.alloc(0))).toBe(false);
    expect(hasPdfMagic(Buffer.from("PDF"))).toBe(false);
    expect(hasPdfMagic(Buffer.from("SUPERIOR COURT O"))).toBe(false);
  });
});

describe("pdfReadableProblem", () => {
  it("flags empty files and text named .pdf", () => {
    const dir = mkdtempSync(path.join(tmpdir(), "pdf-magic-"));
    try {
      const empty = path.join(dir, "empty.pdf");
      writeFileSync(empty, "");
      expect(pdfReadableProblem(empty, 0)).toMatch(/empty file/);

      const text = path.join(dir, "order.pdf");
      writeFileSync(text, "SUPERIOR COURT OF CALIFORNIA\n");
      expect(pdfReadableProblem(text)).toMatch(/missing %PDF header/);

      const real = path.join(dir, "ok.pdf");
      writeFileSync(real, "%PDF-1.4\n%\xe2\xe3\xcf\xd3\n");
      expect(pdfReadableProblem(real)).toBeNull();
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
