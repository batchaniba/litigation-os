import type { MatterSummary } from "../types/portfolio";
import type { DominoResult, IntelligenceCatalog, KnowledgeGraph, SystemicScore } from "./types";
import { linkDegree } from "../utils/crossMatter";
import { mattersWithIssue } from "./queries";

export function systemicImportance(
  summaries: MatterSummary[],
  graph: KnowledgeGraph,
  catalog: IntelligenceCatalog,
): SystemicScore[] {
  const live = summaries.filter((row) => row.lifecycle === "active" || row.lifecycle === "pre_filing");
  const maxDegree = Math.max(1, ...live.map((row) => linkDegree(row.number)));
  return live
    .map((row) => {
      const degree = linkDegree(row.number);
      const issueCount = graph.edges.filter((edge) => edge.matter === row.number && edge.kind === "same_issue").length;
      const liveMotion = catalog.motions.some((motion) => motion.matter === row.number && motion.status === "live");
      const dependents = graph.edges.filter(
        (edge) => edge.kind === "authority_dependency" && (edge.from === `matter:${row.number}` || edge.to === `matter:${row.number}`),
      ).length;
      const score = Math.round(
        (degree / maxDegree) * 40 + Math.min(issueCount, 6) * 6 + (liveMotion ? 18 : 0) + Math.min(dependents, 4) * 4 + (row.phase.includes("mtd") ? 8 : 0),
      );
      const reasons = [
        degree ? `Linked to ${degree} other matter${degree === 1 ? "" : "s"}` : "Isolated docket",
        liveMotion ? "Live dispositive motion" : "No live dispositive motion",
        dependents ? `${dependents} authority-dependency edge${dependents === 1 ? "" : "s"}` : "No authority-dependency edges",
      ];
      return { matter: row.number, score: Math.min(99, score), reasons };
    })
    .sort((a, b) => b.score - a.score || a.matter - b.matter);
}

export function simulateDomino(
  hypothesis: { kind: "survives_mtd" | "theory_rejected"; matter?: number; issue?: string; authorityId?: string },
  graph: KnowledgeGraph,
  catalog: IntelligenceCatalog,
): DominoResult {
  if (hypothesis.kind === "survives_mtd" && hypothesis.matter != null) {
    const peers = graph.edges
      .filter((edge) => {
        const touches = edge.from === `matter:${hypothesis.matter}` || edge.to === `matter:${hypothesis.matter}`;
        const other = edge.from === `matter:${hypothesis.matter}` ? edge.to : edge.from;
        return touches && other.startsWith("matter:");
      })
      .map((edge) => Number((edge.from === `matter:${hypothesis.matter}` ? edge.to : edge.from).replace("matter:", "")))
      .filter((number) => Number.isInteger(number) && number !== hypothesis.matter);
    const unique = [...new Set(peers)];
    return {
      hypothesis: `Matter ${hypothesis.matter} survives the MTD`,
      effects: unique.map((matter) => ({
        matter,
        delta: "strengthened",
        impact: "HIGH" as const,
        reason: `Shares issue or authority-dependency edges with Matter ${hypothesis.matter}. A surviving theory travels.`,
      })),
    };
  }
  const issue = hypothesis.issue ?? catalog.authorities.find((row) => row.id === hypothesis.authorityId)?.issues[0];
  const matters = issue ? mattersWithIssue(graph, issue) : [];
  return {
    hypothesis: hypothesis.authorityId
      ? `Authority ${hypothesis.authorityId} is rejected or narrowed`
      : `Theory ${issue} is rejected`,
    effects: matters.map((matter) => ({
      matter,
      delta: "weakened",
      impact: "HIGH" as const,
      reason: `Matter ${matter} currently depends on ${issue}.`,
    })),
  };
}
