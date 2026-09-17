// Extracted-text sidecars for R2 PDFs: text/<first2>/<rest>.txt.
//
// Written by internal/scripts/extract-doc-text.mjs (backfill) and kept in
// sync by internal/scripts/r2-upload.mjs on every push. Served to external
// models by the Worker's readDocumentText MCP tool, so agents read document
// contents as tool results instead of fetching PDF bytes over HTTP.
//
// Requires the `pdftotext` binary (poppler-utils). Extraction is best-effort:
// a missing binary skips the sidecar with a warning status rather than
// failing the caller — the documents:push path must never break on it.
import { execFile } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import { keyForSha256Text, objectExists, putObject } from "./r2-client.mjs";

const execFileAsync = promisify(execFile);

let pdftotextOk = null;
async function havePdftotext() {
  if (pdftotextOk === null) {
    try {
      await execFileAsync("pdftotext", ["-v"]);
      pdftotextOk = true;
    } catch {
      pdftotextOk = false;
    }
  }
  return pdftotextOk;
}

// Extracts text with `pdftotext -layout` (preserves the visual layout, which
// keeps pleading line numbers and tables readable). Returns the text, or null
// when pdftotext is unavailable. Throws on extraction failure (e.g. corrupt
// PDF) so the caller can log it.
export async function extractTextFromPdf(pdfBytes) {
  if (!(await havePdftotext())) return null;
  const tmp = path.join(
    os.tmpdir(),
    `doctext-${process.pid}-${Math.random().toString(36).slice(2)}.pdf`,
  );
  fs.writeFileSync(tmp, pdfBytes);
  try {
    const { stdout } = await execFileAsync("pdftotext", ["-layout", tmp, "-"], {
      maxBuffer: 256 * 1024 * 1024,
    });
    return stdout;
  } finally {
    fs.rmSync(tmp, { force: true });
  }
}

// Ensures the text sidecar exists for one PDF (idempotent: HEAD skip).
// Returns "uploaded" | "skipped_already_present" | "skipped_no_pdftotext".
// An empty sidecar means the PDF had no text layer (scanned/image-only);
// only a missing sidecar means "not yet processed".
export async function ensureTextSidecar(sha256, pdfBytes) {
  const key = keyForSha256Text(sha256);
  if (await objectExists(key)) return "skipped_already_present";
  const text = await extractTextFromPdf(pdfBytes);
  if (text === null) return "skipped_no_pdftotext";
  await putObject(key, Buffer.from(text, "utf8"), {
    contentType: "text/plain; charset=utf-8",
  });
  return "uploaded";
}
