// Schema for internal/src/data/matters/NN.json — the canonical matter record.
// Plain-JS declarative schema (no dependency); validates shape and types.

const isStr = (v) => typeof v === "string";
const isNonEmptyStr = (v) => isStr(v) && v.trim().length > 0;
const isNum = (v) => typeof v === "number" && !Number.isNaN(v);
const isInt = (v) => Number.isInteger(v);
const isBool = (v) => typeof v === "boolean";
const isStrArray = (v) => Array.isArray(v) && v.every(isStr);
const isObj = (v) => v !== null && typeof v === "object" && !Array.isArray(v);

/** Required fields: [validator] */
const REQUIRED = {
  number: (v) => isInt(v) && v > 0,
  caption: isNonEmptyStr,
  case_no: isStr,
  court: isNonEmptyStr,
  claims: isStr,
  status: isStr,
  lifecycle: isStr,
  proceeding: isStr,
  phase: isStr,
  filed: isStr,
  judge: isStr,
  cluster: isInt,
  type: isStr,
  defendants: isStr,
  archived: isBool,
  causes: isStrArray,
  key_facts: isStr,
  procedural_status: isStr,
  damages: isStr,
  risk: isStr,
  evidence: isStrArray,
  documents: (v) =>
    Array.isArray(v) &&
    v.every((d) => isObj(d) && isStr(d.path) && d.path.startsWith("/documents/")),
};

/** Optional fields: [validator] */
const OPTIONAL = {
  status_label: isStr,
  badge: isStr,
  courtlistener: (v) =>
    isObj(v) &&
    (v.court_id === undefined || isStr(v.court_id)) &&
    (v.docket_id === undefined || isNum(v.docket_id)) &&
    (v.docket_url === undefined || isStr(v.docket_url)),
  note: isStr,
  policy_limits: isObj,
  serviceTracking: isObj,
};

/** Validate a parsed matter JSON; returns an array of human-readable issues (empty = valid). */
export function validateMatter(data) {
  const issues = [];
  if (!isObj(data)) return ["matter must be an object"];
  for (const [field, check] of Object.entries(REQUIRED)) {
    const v = data[field];
    if (v === undefined) {
      issues.push(`${field}: missing required field`);
    } else if (!check(v)) {
      issues.push(`${field}: invalid value`);
    }
  }
  for (const [field, check] of Object.entries(OPTIONAL)) {
    const v = data[field];
    if (v !== undefined && !check(v)) {
      issues.push(`${field}: invalid value`);
    }
  }
  return issues;
}
