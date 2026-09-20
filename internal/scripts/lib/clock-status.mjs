// Canonical stored clock statuses. One list — validate, upcoming, seed, and
// the Worker import this file instead of restating the enum.
//
// Live clocks.json (54 rows, 2026-09-20) uses only these five. `undated` is
// unused as a stored status (two undated rows exist; they are `open` and
// `contingent` with a null date). `overdue` is derived from date + open/set.
// `retired` / `cancelled` appear in Worker comments, not in clocks.json.

export const STORED_CLOCK_STATUSES = Object.freeze([
  "open",
  "set",
  "contingent",
  "vacated",
  "satisfied",
]);

export const STORED_CLOCK_STATUS_SET = new Set(STORED_CLOCK_STATUSES);

/** Alias used by upcoming-from-clocks and older imports. Stored list only. */
export const CLOCK_STATUSES = STORED_CLOCK_STATUS_SET;

/** Obligation finished or withdrawn. Not live. */
export const DEAD_CLOCK_STATUSES = Object.freeze(["vacated", "satisfied"]);
export const DEAD_CLOCK_STATUS_SET = new Set(DEAD_CLOCK_STATUSES);

/** Open-ish stored statuses. A past date on these is overdue (derived). */
export const OPEN_CLOCK_STATUSES = Object.freeze(["open", "set"]);
export const OPEN_CLOCK_STATUS_SET = new Set(OPEN_CLOCK_STATUSES);

/**
 * Legacy D1 / comment aliases — not stored in clocks.json.
 * Mapping: withdrawn / cancelled clock → vacated (not completed).
 * Validate rejects these; Worker SQL still treats them as closed so an
 * unmigrated D1 row cannot leak onto /upcoming.
 */
export const LEGACY_CLOCK_STATUS_MAP = Object.freeze({
  retired: "vacated",
  cancelled: "vacated",
  canceled: "vacated",
});

export const CLOSED_CLOCK_STATUSES = Object.freeze([
  ...DEAD_CLOCK_STATUSES,
  ...Object.keys(LEGACY_CLOCK_STATUS_MAP),
]);

export const CLOSED_CLOCK_STATUS_SET = new Set(CLOSED_CLOCK_STATUSES);

export const CLOSED_CLOCK_SQL = `(${CLOSED_CLOCK_STATUSES.map((s) => `'${s}'`).join(",")})`;

export const CLOCK_RANK = Object.freeze({
  open: 0,
  set: 0,
  contingent: 2,
  vacated: 9,
  satisfied: 9,
});

export function isStoredClockStatus(status) {
  return STORED_CLOCK_STATUS_SET.has(status);
}

export function isDeadClockStatus(status) {
  return DEAD_CLOCK_STATUS_SET.has(status);
}

/** Closed for upcoming / fuse — canonical dead plus unmigrated legacy aliases. */
export function isClosedClockStatus(status) {
  return CLOSED_CLOCK_STATUS_SET.has(String(status ?? "open").toLowerCase());
}

export function normalizeClockStatus(status) {
  const raw = String(status ?? "open").toLowerCase();
  return LEGACY_CLOCK_STATUS_MAP[raw] ?? raw;
}

/** Derived: dated, not contingent, not closed, date before today. Never stored. */
export function isClockOverdue(clock, today) {
  if (!clock?.date || !today) return false;
  if (clock.status === "contingent") return false;
  if (isClosedClockStatus(clock.status)) return false;
  return clock.date < today;
}

export function isDeadClock(clock) {
  return isClosedClockStatus(clock?.status);
}

/**
 * Fail-closed check for a stored `clocks.json` / D1 status.
 * `overdue` is called out so the error says "derived", not just "unknown".
 */
export function clockStatusIssue(status, loc = "clocks.json") {
  const allowed = STORED_CLOCK_STATUSES.join(" | ");
  if (status == null || status === "") {
    return `${loc}: status is required (${allowed})`;
  }
  if (typeof status !== "string") {
    return `${loc}: status must be a string (${allowed})`;
  }
  if (status === "overdue") {
    return `${loc}: "overdue" is derived from date + open/set, never a stored status`;
  }
  if (!isStoredClockStatus(status)) {
    return `${loc}: unknown stored clock status "${status}" (allowed: ${allowed})`;
  }
  return null;
}

/** Validate an array of clock rows the way validate-portfolio does. */
export function validateClockRows(clocks, tag = "clocks.json") {
  if (!Array.isArray(clocks)) return [`${tag} must be an array`];
  const issues = [];
  for (const [i, row] of clocks.entries()) {
    if (row == null || typeof row !== "object") continue;
    const issue = clockStatusIssue(row.status, `${tag}[${i}]`);
    if (issue) issues.push(issue);
  }
  return issues;
}
