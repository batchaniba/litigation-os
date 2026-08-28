// Minimal PDF-file checks for validate-portfolio: size and %PDF magic.
// Node-only — no pymupdf. Empty files and text-named-.pdf both fail.
import fs from "node:fs";

export const PDF_MAGIC = "%PDF";

/** @param {Buffer|Uint8Array|string} bytes */
export function hasPdfMagic(bytes) {
  if (bytes == null) return false;
  const buf = Buffer.isBuffer(bytes) ? bytes : Buffer.from(bytes);
  return buf.length >= 4 && buf.subarray(0, 4).toString("latin1") === PDF_MAGIC;
}

/**
 * @param {string} filePath
 * @param {number} [size]
 * @returns {string|null} problem, or null if the file looks like a PDF
 */
export function pdfReadableProblem(filePath, size) {
  const n = size ?? fs.statSync(filePath).size;
  if (n === 0) return "empty file (0 bytes)";
  const fd = fs.openSync(filePath, "r");
  try {
    const buf = Buffer.alloc(5);
    const read = fs.readSync(fd, buf, 0, 5, 0);
    if (read < 4 || !hasPdfMagic(buf.subarray(0, read))) {
      return "not a PDF (missing %PDF header)";
    }
  } finally {
    fs.closeSync(fd);
  }
  return null;
}
