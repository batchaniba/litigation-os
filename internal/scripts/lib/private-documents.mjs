// Owner denylist: 14 paths (and every known SHA-256 of their bytes) are
// auth-only. Every other D1-registered document is public. Worker, seed,
// publish projection, path index, and the consolidator all import this so
// the set cannot drift. Newly added files default public unless they match.
//
// Source of truth: internal/src/data/documents/private-documents.json
// This module inlines the same data so the Worker bundle does not need fs.

import spec from "../../src/data/documents/private-documents.json" with { type: "json" };

const HEX64 = /^[0-9a-f]{64}$/;

function collectShas(specObj) {
  const out = new Set();
  const bags = specObj?.sha256 ?? {};
  for (const list of Object.values(bags)) {
    for (const h of list ?? []) {
      const c = String(h).toLowerCase();
      if (HEX64.test(c)) out.add(c);
    }
  }
  return out;
}

export const PRIVATE_DOCUMENT_PATHS = Object.freeze([...(spec.paths ?? [])]);
export const PRIVATE_DOCUMENT_PATH_PREFIXES = Object.freeze([
  ...(spec.path_prefixes ?? []),
]);
export const PRIVATE_DOCUMENT_SHAS = Object.freeze([...collectShas(spec)]);

const PATH_SET = new Set(PRIVATE_DOCUMENT_PATHS);
const SHA_SET = new Set(PRIVATE_DOCUMENT_SHAS);
const ALIAS_PATHS = new Set(
  (spec.same_bytes_aliases ?? []).map((a) => a?.path).filter((p) => typeof p === "string" && p && !p.endsWith("/")),
);

export function isPrivatePath(docPath) {
  const p = String(docPath ?? "");
  if (!p) return false;
  if (PATH_SET.has(p)) return true;
  if (ALIAS_PATHS.has(p)) return true;
  for (const prefix of PRIVATE_DOCUMENT_PATH_PREFIXES) {
    if (p.startsWith(prefix)) return true;
  }
  return false;
}

export function isPrivateSha(sha) {
  const c = String(sha ?? "").toLowerCase();
  return HEX64.test(c) && SHA_SET.has(c);
}

/** True when a D1 / manifest / disk row must not be served anonymously. */
export function isPrivateDocument({ path, sha256 } = {}) {
  return isPrivatePath(path) || isPrivateSha(sha256);
}

export function filterPublicDocuments(rows) {
  return (rows ?? []).filter((row) => !isPrivateDocument(row));
}
