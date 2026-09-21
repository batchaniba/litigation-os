import { describe, expect, it } from "vitest";
import { classifyRootEntries } from "./root-quarantine.mjs";

const ALLOWED = new Set(["package.json", "README.md"]);

function file(name, size) {
  return { name, isFile: true, size };
}

const LEDGER = {
  files: [
    { name: "1032_Opposition.pdf", size: 2956810 },
    { name: "Discharge_Review_Report.pdf", size: 757513 },
  ],
};

describe("classifyRootEntries", () => {
  it("no longer waves through arbitrary root PDFs and DOCX", () => {
    const { errors } = classifyRootEntries({
      entries: [file("SomeNewUpload.pdf", 1234), file("Draft.docx", 99)],
      allowedFiles: ALLOWED,
      quarantine: LEDGER,
    });
    expect(errors).toHaveLength(2);
    expect(errors[0]).toMatch(/stray file "SomeNewUpload\.pdf"/);
    expect(errors[0]).toMatch(/pushed to R2, not committed here/);
  });

  it("permits the known backlog without erroring", () => {
    const { errors, remaining } = classifyRootEntries({
      entries: [file("1032_Opposition.pdf", 2956810), file("Discharge_Review_Report.pdf", 757513)],
      allowedFiles: ALLOWED,
      quarantine: LEDGER,
    });
    expect(errors).toEqual([]);
    expect(remaining).toBe(2);
  });

  it("reports the backlog as a warning so it stays visible", () => {
    const { warnings } = classifyRootEntries({
      entries: [file("1032_Opposition.pdf", 2956810)],
      allowedFiles: ALLOWED,
      quarantine: LEDGER,
    });
    expect(warnings.join(" ")).toMatch(/still holds 1 quarantined document/);
    expect(warnings.join(" ")).toMatch(/documents:push/);
  });

  it("catches a different file parked under a quarantined name", () => {
    const { errors } = classifyRootEntries({
      entries: [file("1032_Opposition.pdf", 5)],
      allowedFiles: ALLOWED,
      quarantine: LEDGER,
    });
    expect(errors).toHaveLength(1);
    expect(errors[0]).toMatch(/different file is parked/);
  });

  it("nudges the ledger to shrink once a file is filed", () => {
    const { errors, warnings, remaining } = classifyRootEntries({
      entries: [],
      allowedFiles: ALLOWED,
      quarantine: LEDGER,
    });
    expect(errors).toEqual([]);
    expect(remaining).toBe(0);
    expect(warnings.join(" ")).toMatch(/lists 2 file\(s\) no longer at the repository root/);
  });

  it("fails closed when the ledger is missing", () => {
    const { errors } = classifyRootEntries({
      entries: [file("1032_Opposition.pdf", 2956810)],
      allowedFiles: ALLOWED,
      quarantine: { files: [] },
    });
    expect(errors).toHaveLength(1);
  });

  it("ignores directories, dotfiles, and the root allowlist", () => {
    const { errors, warnings } = classifyRootEntries({
      entries: [
        { name: "internal", isFile: false },
        file(".env.local", 10),
        file("package.json", 10),
      ],
      allowedFiles: ALLOWED,
      quarantine: { files: [] },
    });
    expect(errors).toEqual([]);
    expect(warnings).toEqual([]);
  });
});
