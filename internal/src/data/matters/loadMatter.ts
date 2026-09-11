import type { Matter, MatterDocumentRef } from "../../types/portfolio";
import { resolveDocuments } from "../documents";

// Full NN.json records are code-split and loaded on demand. Do not re-export
// this module from `./index` — that barrel is the light `cases` list, and a
// static import of `resolveDocuments` would pull registry.json onto `/`.
const matterLoaders = import.meta.glob(["./*.json", "!./summaries.json", "!./document-index.json"]) as Record<
  string,
  () => Promise<{ default: Matter & { documents?: MatterDocumentRef[] } }>
>;

export function matterFileKey(number: number): string {
  return `./${String(number).padStart(2, "0")}.json`;
}

export function loadMatter(number: number): Promise<Matter> {
  const loader = matterLoaders[matterFileKey(number)];
  if (!loader) {
    return Promise.reject(new Error(`No matter JSON for number ${number}`));
  }
  return loader().then((mod) => {
    const raw = mod.default;
    const documents = resolveDocuments(raw.documents);
    const matter: Matter = {
      ...raw,
      documents,
      evidenceCount: raw.evidenceCount ?? (Array.isArray(raw.evidence) ? raw.evidence.length : 0),
      documentCount: raw.documentCount ?? documents.length,
    };
    return matter;
  });
}
