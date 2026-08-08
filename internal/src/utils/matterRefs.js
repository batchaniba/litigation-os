// ==========================================================
// Matter-join helpers.
//
// Timeline / damages / theories store `matters` as number[] (or a portfolio
// sentinel string: "All" / "All CDCR"). Legacy CSV strings are still accepted
// by the parser so old fixtures and half-migrated data don't crash.
// ==========================================================

/**
 * @typedef {{ all: boolean, numbers: number[], label: string }} MatterRefs
 */

/**
 * Normalize a matters field into `{ all, numbers, label }`.
 * @param {unknown} matters
 * @returns {MatterRefs}
 */
export function parseMatterRefs(matters) {
  if (Array.isArray(matters)) {
    const numbers = matters
      .map((value) => Number(value))
      .filter((n) => Number.isInteger(n) && n > 0);
    return { all: false, numbers, label: numbers.join(", ") };
  }

  const trimmed = String(matters ?? "").trim();
  if (!trimmed) return { all: false, numbers: [], label: "" };
  if (/^all\b/i.test(trimmed)) {
    return { all: true, numbers: [], label: trimmed };
  }

  const numbers = trimmed
    .split(",")
    .map((part) => Number.parseInt(part.trim(), 10))
    .filter((n) => Number.isInteger(n) && n > 0);
  return { all: false, numbers, label: numbers.join(", ") };
}

/** Display label for a matters field ("1, 2, 7" or "All"). */
export function formatMatterRefs(matters) {
  return parseMatterRefs(matters).label;
}

/**
 * Whether a matters field includes a given matter number.
 * Portfolio-wide sentinels ("All" / "All CDCR") match only when `includeAll`.
 */
export function matterRefsInclude(matters, matterNumber, { includeAll = false } = {}) {
  const parsed = parseMatterRefs(matters);
  if (parsed.all) return includeAll;
  return parsed.numbers.includes(Number(matterNumber));
}

/** @deprecated Prefer parseMatterRefs — kept for calendarUtils call sites. */
export const parseMatterNumbers = parseMatterRefs;
