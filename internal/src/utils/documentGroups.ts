import type { PortfolioDocument } from "../types/portfolio";

export const DOCUMENT_GROUPS = ["Pleadings", "Motions & Briefs", "Orders & Rulings", "Discovery", "Evidence & Exhibits", "Service", "Correspondence", "Other"] as const;
export type DocumentGroup = typeof DOCUMENT_GROUPS[number];

export function documentGroup(document: PortfolioDocument): DocumentGroup {
  const value = `${document.label} ${document.path}`.toLowerCase();
  if (/complaint|petition|answer|summons|civil cover|cm-010/.test(value)) return "Pleadings";
  if (/motion|opposition|reply|demurrer|memorandum|brief|rjn|points and authorities/.test(value)) return "Motions & Briefs";
  if (/order|ruling|judgment|findings|recommendation|minute/.test(value)) return "Orders & Rulings";
  if (/discovery|interrogator|admission|production|deposition|subpoena/.test(value)) return "Discovery";
  if (/exhibit|evidence|declaration|transcript|report|record|photo|video/.test(value)) return "Evidence & Exhibits";
  if (/service|served|proof|pos-|usm-285|nar/.test(value)) return "Service";
  if (/email|letter|correspondence|meet-and-confer|notice/.test(value)) return "Correspondence";
  return "Other";
}

export function groupDocuments(documents: PortfolioDocument[] = []) {
  const grouped = new Map<DocumentGroup, PortfolioDocument[]>();
  for (const group of DOCUMENT_GROUPS) grouped.set(group, []);
  for (const document of documents) grouped.get(documentGroup(document))!.push(document);
  return [...grouped.entries()].filter(([, items]) => items.length);
}
