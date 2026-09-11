// Normalize PACER-style civil docket numbers so we query CourtListener by
// number + court_id, never by caption.

import { COURT_OFFICES } from "./courts.mjs";

const FEDERAL_RE =
  /\b(\d):(\d{2})-(cv|cr|mc|md)-(\d{3,6})(?:-[A-Z]{2,5}(?:-[A-Z]{2,5})*)?(?:\s*\((?:PC|PS)\))?\b/i;

export function parseFederalDocket(value) {
  const text = String(value ?? "");
  const match = text.match(FEDERAL_RE);
  if (!match) return null;
  return {
    office: match[1],
    year: match[2],
    nature: match[3].toLowerCase(),
    number: match[4].padStart(5, "0"),
  };
}

export function formatDocketNumber(parsed) {
  if (!parsed) return null;
  return `${parsed.office}:${parsed.year}-${parsed.nature}-${parsed.number}`;
}

export function normalizeDocketNumber(value) {
  return formatDocketNumber(parseFederalDocket(value));
}

/** Same year/nature/number with this court's other office prefixes. Exact office first. */
export function officeVariants(parsed, courtId) {
  if (!parsed) return [];
  const offices = COURT_OFFICES[courtId] ?? [parsed.office];
  const ordered = [parsed.office, ...offices.filter((office) => office !== parsed.office)];
  const seen = new Set();
  const out = [];
  for (const office of ordered) {
    const formatted = formatDocketNumber({ ...parsed, office });
    if (!formatted || seen.has(formatted)) continue;
    seen.add(formatted);
    out.push(formatted);
  }
  return out;
}

export function hasResolvableDocketNumber(caseNo) {
  return parseFederalDocket(caseNo) != null;
}
