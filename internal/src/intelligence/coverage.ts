import type { ClaimElement, ClaimMatrix, IntelligenceCatalog } from "./types";

export function filledSlots(element: ClaimElement): number {
  return [element.allegation, element.evidence.length ? "e" : "", element.authority.length ? "a" : "", element.defense]
    .filter(Boolean).length;
}

export function elementCoverage(element: ClaimElement): number {
  return filledSlots(element) / 4;
}

export function claimCoverage(matrix: ClaimMatrix): number {
  if (!matrix.elements.length) return 0;
  return matrix.elements.reduce((sum, element) => sum + elementCoverage(element), 0) / matrix.elements.length;
}

export function weakestElement(elements: ClaimElement[]): ClaimElement | undefined {
  if (!elements.length) return undefined;
  return [...elements].sort((a, b) => elementCoverage(a) - elementCoverage(b) || a.label.localeCompare(b.label))[0];
}

export function matrixForMatter(catalog: IntelligenceCatalog, matter: number): ClaimMatrix[] {
  return catalog.matrices.filter((matrix) => matrix.matter === matter);
}

export function coverageReport(matrix: ClaimMatrix) {
  const weakest = weakestElement(matrix.elements);
  return {
    matter: matrix.matter,
    claim: matrix.claim,
    coverage: claimCoverage(matrix),
    weakest: weakest?.label,
    best_next_evidence: weakest?.next_evidence,
    elements: matrix.elements.map((element) => ({
      id: element.id,
      label: element.label,
      coverage: elementCoverage(element),
    })),
  };
}
