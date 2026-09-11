import type { MatterSummary } from "../types/portfolio";
import type { ClaimElement, IntelligenceCatalog, LitigationEvent, LitigationTwin, OpenIssue } from "./types";
import type { PendingClock } from "./types";
import { elementCoverage, matrixForMatter, weakestElement } from "./coverage";

function clamp(value: number): number {
  return Math.max(0, Math.min(1, Number(value.toFixed(2))));
}

function issueStatus(issueId: string, matter: number, catalog: IntelligenceCatalog, events: LitigationEvent[]): OpenIssue["status"] {
  const live = catalog.motions.some(
    (motion) => motion.matter === matter && motion.issues.includes(issueId) && (motion.status === "live" || motion.status === "submitted"),
  );
  if (live) return "active";
  const raised = events.some((event) => event.matter === matter && event.issues?.includes(issueId) && event.type === "MOTION_FILED");
  if (raised) return "active";
  const anticipated = catalog.motions.some(
    (motion) => motion.matter === matter && motion.issues.includes(issueId) && motion.status === "anticipated",
  );
  if (anticipated) return "anticipated";
  const onMatrix = catalog.matrices.some(
    (matrix) => matrix.matter === matter && matrix.elements.some((element) => element.issue === issueId),
  );
  return onMatrix ? "anticipated" : "dormant";
}

export function deriveTwin(
  summary: MatterSummary,
  catalog: IntelligenceCatalog,
  events: LitigationEvent[],
  clocks: PendingClock[],
): LitigationTwin {
  const matrices = catalog.matrices.filter((matrix) => matrix.matter === summary.number);
  const elements = matrices.flatMap((matrix) => matrix.elements);
  const issueIds = [...new Set(elements.map((element) => element.issue).filter((id): id is string => Boolean(id)))];
  for (const motion of catalog.motions.filter((row) => row.matter === summary.number)) {
    for (const issue of motion.issues) {
      if (!issueIds.includes(issue)) issueIds.push(issue);
    }
  }
  const open_issues: OpenIssue[] = issueIds.map((id) => ({
    id,
    status: issueStatus(id, summary.number, catalog, events),
    source: catalog.motions.find((motion) => motion.matter === summary.number && motion.issues.includes(id))?.label,
  }));
  const controlling = open_issues.filter((issue) => issue.status === "active" || issue.status === "anticipated").map((issue) => issue.id);
  const coverage = elements.length ? elements.reduce((sum, element) => sum + elementCoverage(element), 0) / elements.length : 0;
  const weak = weakestElement(elements);
  const evidenceSlots = elements.filter((element) => element.evidence.length > 0).length;
  const liveMotions = catalog.motions.filter((motion) => motion.matter === summary.number && motion.status !== "decided");
  const proceduralRisk = liveMotions.some((motion) => motion.status === "live") ? 0.45 : summary.phase.includes("mtd") ? 0.4 : 0.22;
  const discovery = summary.evidenceCount && summary.evidenceCount > 8 ? 0.89 : 0.4;

  return {
    matter: summary.number,
    stage: summary.phase,
    live_motions: liveMotions.map((motion) => ({
      id: motion.id,
      docket: motion.docket,
      label: motion.label,
      status: motion.status,
      hearing: motion.hearing,
      issues: motion.issues,
    })),
    pending_clocks: clocks.filter((clock) => clock.matter === summary.number),
    open_issues,
    evidence_coverage: clamp(elements.length ? evidenceSlots / elements.length : coverage),
    pleading_coverage: clamp(coverage),
    procedural_risk: clamp(proceduralRisk),
    discovery_leverage: clamp(discovery),
    controlling_questions: controlling,
    weakest_element: weak?.label,
    best_next_evidence: weak?.next_evidence,
  };
}

export function activateIssue(twin: LitigationTwin, issueId: string, source: string): LitigationTwin {
  const open_issues = twin.open_issues.map((issue) =>
    issue.id === issueId ? { ...issue, status: "active" as const, source } : issue,
  );
  const known = open_issues.some((issue) => issue.id === issueId);
  if (!known) open_issues.push({ id: issueId, status: "active", source });
  const live_motions = twin.live_motions.some((motion) => motion.issues.includes(issueId))
    ? twin.live_motions
    : [
        ...twin.live_motions,
        { id: `activated-${issueId}`, label: source, status: "live" as const, issues: [issueId] },
      ];
  return {
    ...twin,
    open_issues,
    live_motions,
    controlling_questions: [...new Set([...twin.controlling_questions, issueId])],
    procedural_risk: clamp(Math.max(twin.procedural_risk, 0.45)),
  };
}

export { matrixForMatter, elementCoverage };
export type { ClaimElement };
