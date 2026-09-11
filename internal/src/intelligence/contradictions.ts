import type { FactProposition, IntelligenceCatalog } from "./types";

export function detectContradictions(catalog: IntelligenceCatalog): FactProposition[] {
  return catalog.facts.filter((fact) => fact.contradicted_by.length > 0);
}

export function contradictionsForMatter(catalog: IntelligenceCatalog, matter: number): FactProposition[] {
  return detectContradictions(catalog).filter((fact) => fact.supports.includes(matter));
}

export function flagContradiction(fact: FactProposition, source: string): FactProposition {
  if (fact.contradicted_by.includes(source)) return fact;
  return { ...fact, contradicted_by: [...fact.contradicted_by, source] };
}
