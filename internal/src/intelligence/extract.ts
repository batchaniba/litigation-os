import type { ArgumentSnapshot, IntelligenceCatalog } from "./types";
import {
  extractAdmissions as extractAdmissionsFromText,
  extractAuthorities as extractAuthoritiesFromCatalog,
  extractFiling as extractFilingFromText,
  issuesInText,
} from "./filingSignals.js";

export function extractAuthorities(text: string, catalog: IntelligenceCatalog): string[] {
  return extractAuthoritiesFromCatalog(text, catalog.authorities);
}

export function extractAdmissions(text: string): string[] {
  return extractAdmissionsFromText(text);
}

export function extractFiling(
  text: string,
  catalog: IntelligenceCatalog,
): { issues: string[]; authorities: string[]; arguments: string[]; admissions: string[] } {
  return extractFilingFromText(text, catalog);
}

export function snapshotFromFiling(input: {
  matter: number;
  filing: string;
  date: string;
  text: string;
  docket?: number;
  catalog: IntelligenceCatalog;
}): ArgumentSnapshot {
  const extracted = extractFiling(input.text, input.catalog);
  return {
    id: `live-${input.matter}-${input.docket ?? input.date}`,
    matter: input.matter,
    filing: input.filing,
    date: input.date,
    arguments: extracted.arguments,
    authorities: extracted.authorities,
    admissions: extracted.admissions,
  };
}

export { issuesInText };
