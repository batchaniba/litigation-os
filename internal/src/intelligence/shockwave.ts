import type { IntelligenceCatalog, ShockwaveHit, ShockwaveReport } from "./types";

const HIGH_ISSUES = new Set(["qualified_immunity", "pc_290_46", "state_actor", "monell_policy", "u_visa_certification"]);

export function shockwaveFromOpinion(
  opinion: { title: string; court: string; issues: string[]; holdings?: string },
  catalog: IntelligenceCatalog,
): ShockwaveReport {
  const hits: ShockwaveHit[] = [];
  const matters = new Map<number, string[]>();
  for (const matrix of catalog.matrices) {
    for (const element of matrix.elements) {
      if (element.issue && opinion.issues.includes(element.issue)) {
        const list = matters.get(matrix.matter) ?? [];
        list.push(element.issue);
        matters.set(matrix.matter, list);
      }
    }
  }
  for (const motion of catalog.motions) {
    for (const issue of motion.issues) {
      if (opinion.issues.includes(issue)) {
        const list = matters.get(motion.matter) ?? [];
        list.push(issue);
        matters.set(motion.matter, list);
      }
    }
  }
  for (const [matter, issues] of matters) {
    const unique = [...new Set(issues)];
    const impact = unique.some((issue) => HIGH_ISSUES.has(issue)) ? "HIGH" : unique.length > 1 ? "MEDIUM" : "LOW";
    hits.push({
      matter,
      impact,
      reason: `Overlaps controlling issues: ${unique.join(", ")}.${opinion.holdings ? ` ${opinion.holdings}` : ""}`,
      documents: catalog.matrices
        .filter((matrix) => matrix.matter === matter)
        .map((matrix) => `Matter ${matter} ${matrix.claim} matrix`),
    });
  }
  hits.sort((a, b) => a.matter - b.matter);
  return {
    opinion: opinion.title,
    court: opinion.court,
    issues: opinion.issues,
    holdings: opinion.holdings,
    hits,
    propositionsToUpdate: catalog.authorities
      .filter((authority) => authority.issues.some((issue) => opinion.issues.includes(issue)))
      .map((authority) => authority.label),
  };
}
