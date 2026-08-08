// Shared document registry — path is the document id.
// Matter JSON stores membership (+ optional label override / filed);
// resolve through these helpers before rendering or indexing.
import registry from "./documents/registry.json" with { type: "json" };
import type { DocumentRegistryEntry, MatterDocumentRef, PortfolioDocument } from "../types/portfolio";

type RegistryFile = {
  version: number;
  documents: DocumentRegistryEntry[];
};

const registryFile = registry as RegistryFile;

export const documentRegistry: DocumentRegistryEntry[] = registryFile.documents;

const byPath = new Map(documentRegistry.map((entry) => [entry.path, entry]));

export function getRegistryEntry(docPath: string): DocumentRegistryEntry | undefined {
  return byPath.get(docPath);
}

function labelFromPath(docPath: string): string {
  const base = docPath.split("/").pop() ?? docPath;
  return base.replace(/\.pdf$/i, "").replace(/\.docx$/i, "").trim() || base;
}

/** Resolve a matter document ref against the registry. */
export function resolveDocument(ref: MatterDocumentRef): PortfolioDocument {
  const entry = byPath.get(ref.path);
  const label = ref.label?.trim() || entry?.label || labelFromPath(ref.path);
  const resolved: PortfolioDocument = { path: ref.path, label };
  if (typeof ref.filed === "boolean") resolved.filed = ref.filed;
  return resolved;
}

export function resolveDocuments(refs: MatterDocumentRef[] | undefined | null): PortfolioDocument[] {
  return (refs ?? []).map(resolveDocument);
}
