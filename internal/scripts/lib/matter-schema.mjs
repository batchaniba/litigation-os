// Schema for internal/src/data/matters/NN.json — the canonical matter record.
// Plain-JS declarative schema (no dependency); validates shape and types.

const isStr = (v) => typeof v === "string";
const isNonEmptyStr = (v) => isStr(v) && v.trim().length > 0;
const isNum = (v) => typeof v === "number" && !Number.isNaN(v);
const isInt = (v) => Number.isInteger(v);
const isBool = (v) => typeof v === "boolean";
const isStrArray = (v) => Array.isArray(v) && v.every(isStr);

/** Field definitions: [validator, required] */
const FIELDS = {
  number: [(v) => isInt(v) && v > 0, true],
  caption: [isNonEmptyStr, true],
  case_no: [isStr, true],
  court: [isNonEmptyStr, true],
  claims: [isStr, true],
  status: [isStr, true],
  status_label: [isStr, true],
  lifecycle: [isStr, true],
  proceeding: [isStr, true],
  phase: [isStr, true],
  filed: [isStr, true],
  judge: [isStr, true],
  cluster: [isInt, true],
  type: [isStr, true],
  defendants: [isStr, true],
  archived: [isBool, true],
  badge: [isStr, true],
  causes: [isStrArray, true],
  key_facts: [isStr, true],
  procedural_status: [isStr, true],
  damages: [isStr, true],
  risk: [isStr, true],
  evidence: [isStrArray, true],
  documents: [
    (v) => Array.isArray(v) && v.every((d) => d && isStr(d.path) && d.path.startsWith("/documents/")),
    true,
  ],
};

const OPTIONAL_FIELDS = {
  courtlistener: [
    (v) =>
      v && typeof v === "object" &&
      (v.court_id === undefined || isStr(v.court_id)) &&
      (v.docket_id === undefined || isNum(v.docket_id)) &&
      (v.docket_url === undefined || isStr(v.docket_url)),
    false,
  ],
};

/** Validate a parsed matter JSON; returns an array of human-readable issues (empty = valid). */
export function validateMatter(data) {
  const issues = [];
  if (!data || typeof data !== "object") return ["matter must be an object"];
  for (const [field, [check, required]] of Object.entries({ ...FIELDS, ...OPTIONAL_FIELDS })) {
    const v = data[field];
    if (v === undefined) {
      if (required) issues.push(`${field}: missing required field`);
      continue;
    }
    if (!check(v)) issues.push(`${field}: invalid value`);
  }
  return issues;
}
