// Path → sha256 lookup for /documents/* on the R2-backed Worker.
// Index is a JSON map of portfolio paths ("/documents/matter-NN/...") to
// the 64-hex sha256 stored in manifest.json. Bytes live at
// sha256/<first2>/<rest>.pdf.

import { isPrivateDocument } from "../../../internal/scripts/lib/private-documents.mjs";

export function documentsKeyFromUrl(pathname) {
  let p = decodeURIComponent(String(pathname ?? "").split("?")[0]);
  if (!p.startsWith("/")) p = `/${p}`;
  if (p.startsWith("/documents/")) return p;
  return `/documents${p}`;
}

export function sha256ForPath(index, pathname) {
  if (!index || typeof index !== "object") return null;
  const key = documentsKeyFromUrl(pathname);
  const hit = index[key];
  if (typeof hit === "string") return hit.toLowerCase();
  if (hit && typeof hit.sha256 === "string") return hit.sha256.toLowerCase();
  return null;
}

export function contentDispositionForPath(pathname) {
  const key = documentsKeyFromUrl(pathname);
  const name = key.split("/").pop() || "document.pdf";
  return `inline; filename="${name.replaceAll('"', "")}"`;
}

export function buildPathIndex(manifestFiles) {
  const out = {};
  for (const file of manifestFiles ?? []) {
    if (!file?.path || !file?.sha256) continue;
    // Private denylist bytes stay in R2 (hash-addressed) but must not be
    // reachable via the public path index.
    if (isPrivateDocument(file)) continue;
    out[file.path] = String(file.sha256).toLowerCase();
  }
  return out;
}
