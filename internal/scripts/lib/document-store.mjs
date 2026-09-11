// Shared helpers for the document tree vs. the committed inventory.
//
// registry.json is editorial (path → label + owner).
// manifest.json is physical (path → size + sha256).
// CI data jobs can prove a cited path exists from the manifest alone.

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const REPO_ROOT = path.resolve(__dirname, "../../..");
export const PUBLIC_ROOT = path.join(REPO_ROOT, "internal", "public");
export const DOCUMENTS_ROOT = path.join(PUBLIC_ROOT, "documents");
export const MANIFEST_PATH = path.resolve(
  __dirname,
  "../../src/data/documents/manifest.json",
);
export const DOCUMENTS_URL_PREFIX = "/documents/";

/**
 * @param {{ argv?: string[], env?: NodeJS.ProcessEnv }} [opts]
 */
export function skipDiskDocs({ argv = process.argv, env = process.env } = {}) {
  if (argv.includes("--skip-disk-docs")) return true;
  const raw = env.PORTFOLIO_SKIP_DISK_DOCS;
  return raw === "1" || raw === "true";
}

/**
 * @param {{ env?: NodeJS.ProcessEnv }} [opts]
 */
export function skipViteDocumentCopy({ env = process.env } = {}) {
  return env.VITE_COPY_DOCUMENTS === "0";
}

/** @param {string} absPath @param {string} [publicRoot] */
export function publicRel(absPath, publicRoot = PUBLIC_ROOT) {
  return path.relative(publicRoot, absPath).split(path.sep).join("/");
}

/** @param {string} rel */
export function urlFromPublicRel(rel) {
  return `/${rel}`;
}

/** @param {string} urlPath @param {string} [publicRoot] */
export function diskFromUrl(urlPath, publicRoot = PUBLIC_ROOT) {
  return path.join(publicRoot, String(urlPath).replace(/^\//, ""));
}

/** @param {string} dir */
export function walkFiles(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walkFiles(full));
    else if (entry.isFile() && !entry.name.startsWith(".")) out.push(full);
  }
  return out;
}

/**
 * fs.cp / Vite public-dir filter: keep everything except the documents tree.
 * @param {string} source
 * @param {string} [publicRoot]
 */
export function copyPublicExceptDocumentsFilter(source, publicRoot = PUBLIC_ROOT) {
  const rel = path.relative(publicRoot, source);
  if (rel === "" || rel === ".") return true;
  return rel.split(path.sep)[0] !== "documents";
}

/**
 * @param {string} [filePath]
 * @returns {{ version: number, fileCount: number, totalBytes: number, files: Array<{ path: string, size: number, sha256: string }> }}
 */
export function loadManifest(filePath = MANIFEST_PATH) {
  if (!fs.existsSync(filePath)) {
    return { version: 1, fileCount: 0, totalBytes: 0, files: [] };
  }
  const raw = JSON.parse(fs.readFileSync(filePath, "utf8"));
  return {
    version: Number(raw.version) || 1,
    fileCount: Number(raw.fileCount) || 0,
    totalBytes: Number(raw.totalBytes) || 0,
    files: Array.isArray(raw.files) ? raw.files : [],
  };
}

/** @param {{ files?: Array<{ path: string }> }} manifest */
export function manifestByPath(manifest) {
  return new Map((manifest.files ?? []).map((entry) => [entry.path, entry]));
}

/** @param {string} filePath */
export function hashFileSha256(filePath) {
  const hash = crypto.createHash("sha256");
  const fd = fs.openSync(filePath, "r");
  try {
    const buf = Buffer.alloc(1024 * 1024);
    let n;
    while ((n = fs.readSync(fd, buf, 0, buf.length, null)) > 0) {
      hash.update(buf.subarray(0, n));
    }
  } finally {
    fs.closeSync(fd);
  }
  return hash.digest("hex");
}

/**
 * @param {string} [documentsRoot]
 * @param {string} [publicRoot]
 */
export function buildManifestFromDisk(
  documentsRoot = DOCUMENTS_ROOT,
  publicRoot = PUBLIC_ROOT,
) {
  const files = walkFiles(documentsRoot)
    .map((full) => {
      const rel = publicRel(full, publicRoot);
      return {
        path: urlFromPublicRel(rel),
        size: fs.statSync(full).size,
        sha256: hashFileSha256(full),
      };
    })
    .sort((a, b) => a.path.localeCompare(b.path));
  return {
    version: 1,
    fileCount: files.length,
    totalBytes: files.reduce((sum, file) => sum + file.size, 0),
    files,
  };
}

/** @param {{ version: number, fileCount: number, totalBytes: number, files: unknown[] }} manifest */
export function manifestPayload(manifest) {
  return `${JSON.stringify(manifest, null, 2)}\n`;
}
