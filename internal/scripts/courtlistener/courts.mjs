// Map portfolio court strings onto CourtListener court_id values.
// Federal RECAP/PACER is the only side this adapter binds today.

const RULES = [
  { id: "cand", test: /\bN\.?\s*D\.?\s*Cal/i },
  { id: "caed", test: /\bE\.?\s*D\.?\s*Cal/i },
  { id: "casd", test: /\bS\.?\s*D\.?\s*Cal/i },
  { id: "cacd", test: /\bC\.?\s*D\.?\s*Cal/i },
];

/** Office prefixes CourtListener uses for these districts. */
export const COURT_OFFICES = {
  cand: ["3", "4", "5"],
  caed: ["1", "2"],
  casd: ["3"],
  cacd: ["2", "5", "8"],
};

export function courtIdFromCourt(court) {
  const text = String(court ?? "");
  for (const rule of RULES) {
    if (rule.test.test(text)) return rule.id;
  }
  return null;
}

export function isFederalMatter(matter) {
  return matter?.type === "Federal" || matter?.proceeding === "federal_civil";
}
