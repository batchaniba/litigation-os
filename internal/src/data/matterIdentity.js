// ==========================================================
// Matter identity joins.
//
// caption / case_no / court live only on matter JSON (via summaries.json).
// Analytic modules (damages, fees, outcomes, coverage) store `number` (or
// `matter`) plus their own fields — join identity here at read time.
// ==========================================================
import summaries from "./matters/summaries.json" with { type: "json" };

const byNumber = new Map(summaries.map((matter) => [matter.number, matter]));

/** Structured identity fields for a matter number, or null if unknown. */
export function getMatterIdentity(number) {
  const matter = byNumber.get(Number(number));
  if (!matter) return null;
  return {
    number: matter.number,
    caption: matter.caption,
    case_no: matter.case_no,
    court: matter.court,
    claims: matter.claims,
    type: matter.type,
  };
}

/**
 * Merge matter identity onto an analytic row.
 * Row-level `caption` (when present) wins — used for defendant-specific
 * outcomes labels (e.g. Matter 27 Randstad vs RK Logistics demands).
 */
export function withMatterIdentity(row, { numberKey = "number" } = {}) {
  const number = row?.[numberKey] ?? row?.matter;
  const identity = getMatterIdentity(number);
  if (!identity) return { ...row };

  const caseNo = row.case_no ?? row.caseNumber ?? row.caseNo ?? identity.case_no;
  return {
    ...row,
    caption: row.caption ?? identity.caption,
    case_no: caseNo,
    caseNumber: caseNo,
    caseNo,
    court: row.court ?? identity.court,
  };
}
