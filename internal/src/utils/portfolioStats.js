import { isLiveLifecycle, isArchivedMatter } from "./matterLifecycle";

const COURT_ALIASES = [
  { match: /N\.?\s*D\.?\s*Cal/i, label: "USDC N.D. Cal." },
  { match: /E\.?\s*D\.?\s*Cal/i, label: "USDC E.D. Cal." },
  { match: /Santa Clara/i, label: "Santa Clara Sup. Ct." },
  { match: /San Joaquin/i, label: "San Joaquin Sup. Ct." },
  { match: /Alameda/i, label: "Alameda Sup. Ct." },
  { match: /Sacramento/i, label: "Sacramento Sup. Ct." },
];

/** Successor dockets keep CHP-cluster dollars live after M1/M2/M7 dismissal. */
export const SUCCESSOR_EXPOSURE_MATTERS = new Set([1, 2, 7]);
export const HISTORICAL_EXPOSURE_MATTERS = new Set([22, 27]);

export function courtLabelsFrom(court) {
  const text = String(court ?? "");
  const labels = [];
  for (const { match, label } of COURT_ALIASES) {
    if (match.test(text)) labels.push(label);
  }
  return labels;
}

export function countCourts(matters, jurisdictions) {
  const counts = Object.fromEntries((jurisdictions ?? []).map((j) => [j, 0]));
  for (const matter of matters ?? []) {
    for (const label of courtLabelsFrom(matter.court)) {
      if (counts[label] !== undefined) counts[label] += 1;
    }
  }
  return counts;
}

export function litigatingMatters(matters) {
  return (matters ?? []).filter((m) => m.lifecycle === "active");
}

export function preFilingMatters(matters) {
  return (matters ?? []).filter((m) => m.lifecycle === "pre_filing");
}

export function isActiveExposureRow(row, byNumber) {
  const nums = Array.isArray(row?.matters) ? row.matters.map(Number) : [];
  if (nums.length === 0) return true;
  if (nums.every((n) => HISTORICAL_EXPOSURE_MATTERS.has(n))) return false;
  return nums.some((n) => {
    if (SUCCESSOR_EXPOSURE_MATTERS.has(n)) return true;
    const matter = byNumber?.get?.(n);
    if (!matter) return true;
    if (HISTORICAL_EXPOSURE_MATTERS.has(n)) return false;
    if (isArchivedMatter(matter)) return false;
    return isLiveLifecycle(matter.lifecycle) || (!matter.lifecycle && !matter.archived);
  });
}

export function sumExposure(rows, key = "moderate") {
  return (rows ?? []).reduce((total, row) => total + (Number(row[key]) || 0), 0);
}
