import type { GraphEdge, IntelligenceCatalog, KnowledgeGraph } from "./types";

export function neighbors(graph: KnowledgeGraph, nodeId: string, kind?: GraphEdge["kind"]): GraphEdge[] {
  return graph.edges.filter((edge) => (edge.from === nodeId || edge.to === nodeId) && (!kind || edge.kind === kind));
}

export function mattersWithIssue(graph: KnowledgeGraph, issueId: string): number[] {
  const target = `issue:${issueId}`;
  const matters = new Set<number>();
  for (const edge of graph.edges) {
    if (edge.kind !== "same_issue" && edge.kind !== "raises") continue;
    if (edge.to !== target && edge.from !== target) continue;
    if (typeof edge.matter === "number") matters.add(edge.matter);
  }
  return [...matters].sort((a, b) => a - b);
}

export function attorneysWhoRaised(catalog: IntelligenceCatalog, issueId: string): string[] {
  return catalog.attorneys.filter((attorney) => attorney.issues.includes(issueId)).map((attorney) => attorney.name);
}

export function authoritiesForIssue(catalog: IntelligenceCatalog, issueId: string, side?: "plaintiff" | "defense") {
  return catalog.authorities.filter((authority) => authority.issues.includes(issueId) && (!side || authority.supports === side));
}

export function adverseCiting(catalog: IntelligenceCatalog, authorityId: string) {
  const node = catalog.authorities.find((row) => row.id === authorityId);
  if (!node) return [];
  return catalog.authorities.filter((row) => row.cites.includes(authorityId) && row.supports === "defense");
}

export function counselOverlap(catalog: IntelligenceCatalog): Array<{ attorney: string; matters: number[] }> {
  return catalog.attorneys
    .filter((attorney) => attorney.matters.length > 1)
    .map((attorney) => ({ attorney: attorney.name, matters: attorney.matters }));
}

export function sharedCounsel(catalog: IntelligenceCatalog, matterA: number, matterB: number): string[] {
  return catalog.attorneys
    .filter((attorney) => attorney.matters.includes(matterA) && attorney.matters.includes(matterB))
    .map((attorney) => attorney.name);
}

export function qiRadar(graph: KnowledgeGraph, catalog: IntelligenceCatalog) {
  const matters = mattersWithIssue(graph, "qualified_immunity");
  return {
    matters,
    supporting: authoritiesForIssue(catalog, "qualified_immunity", "plaintiff"),
    adverse: authoritiesForIssue(catalog, "qualified_immunity", "defense"),
    attorneys: attorneysWhoRaised(catalog, "qualified_immunity"),
  };
}
