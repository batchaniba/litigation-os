// Shared Node helpers for the portfolio document registry.
// Path is the document id. Matter JSON stores membership + optional label/filed
// overrides; registry.json owns the canonical label (+ owning matter folder).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const REGISTRY_PATH = path.resolve(__dirname, "../../src/data/documents/registry.json");

/** @param {string} docPath */
export function ownerMatterFromPath(docPath) {
  const match = String(docPath).match(/^\/documents\/matter-(\d+)\//);
  return match ? Number(match[1]) : null;
}

/** Strip hub-matter display prefixes like "[M7] ". */
export function stripMatterPrefix(label) {
  return String(label ?? "").replace(/^\[M\d+\]\s*/i, "").trim();
}

/** Filename stem used when no matter label exists (outcomes-only paths). */
export function labelFromPath(docPath) {
  const base = path.posix.basename(String(docPath));
  return base.replace(/\.pdf$/i, "").replace(/\.docx$/i, "").trim() || base;
}

/**
 * @param {string} [filePath]
 * @returns {{ version: number, documents: Array<{ path: string, label: string, ownerMatter: number|null }> }}
 */
export function loadRegistry(filePath = REGISTRY_PATH) {
  if (!fs.existsSync(filePath)) {
    return { version: 1, documents: [] };
  }
  const raw = JSON.parse(fs.readFileSync(filePath, "utf8"));
  return {
    version: Number(raw.version) || 1,
    documents: Array.isArray(raw.documents) ? raw.documents : [],
  };
}

/** @param {{ documents?: Array<{ path: string, label: string }> }} registry */
export function registryByPath(registry) {
  return new Map((registry.documents ?? []).map((entry) => [entry.path, entry]));
}

/**
 * Resolve a matter document ref against the registry.
 * @param {{ path: string, label?: string, filed?: boolean }} ref
 * @param {Map<string, { path: string, label: string }>} byPath
 */
export function resolveDocumentRef(ref, byPath) {
  if (!ref?.path) return null;
  const entry = byPath.get(ref.path);
  const label = (typeof ref.label === "string" && ref.label.trim())
    ? ref.label.trim()
    : (entry?.label ?? labelFromPath(ref.path));
  /** @type {{ path: string, label: string, filed?: boolean }} */
  const resolved = { path: ref.path, label };
  if (typeof ref.filed === "boolean") resolved.filed = ref.filed;
  return resolved;
}

/**
 * @param {Array<{ path: string, label?: string, filed?: boolean }>|undefined} refs
 * @param {Map<string, { path: string, label: string }>} byPath
 */
export function resolveMatterDocuments(refs, byPath) {
  return (refs ?? [])
    .map((ref) => resolveDocumentRef(ref, byPath))
    .filter(Boolean);
}
