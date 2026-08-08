// Portfolio dates are civil dates in Pacific time — "Mar. 27, 2026" means that
// calendar day in California, regardless of where the browser is. Every date in
// here is therefore represented as the UTC instant of midnight Pacific on that
// day, which keeps the UTC fields readable as the intended calendar day (see
// dayKey() in calendarUtils.js, which depends on exactly that).
//
// The Pacific offset is not a constant: PDT is UTC-7, PST is UTC-8. It is
// derived per date rather than assumed, so comparisons stay correct across the
// November and March transitions.

// Constructed once — Intl formatter construction is expensive, and these sit in
// the status-label hot path.
const PT_FIELDS = new Intl.DateTimeFormat("en-US", {
  timeZone: "America/Los_Angeles",
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hourCycle: "h23",
});

// Calendar fields of an instant, as seen in Pacific time.
const pacificFields = (date) => {
  const fields = {};
  for (const part of PT_FIELDS.formatToParts(date)) {
    if (part.type !== "literal") fields[part.type] = Number(part.value);
  }
  return fields;
};

// Hours Pacific time runs behind UTC at a given instant: 7 in PDT, 8 in PST.
const pacificOffsetAt = (date) => {
  const f = pacificFields(date);
  const asIfUTC = Date.UTC(f.year, f.month - 1, f.day, f.hour, f.minute, f.second);
  return Math.round((date.getTime() - asIfUTC) / 3600000);
};

// The UTC instant of midnight Pacific on a given civil date. Guesses with the
// PST offset first, then re-anchors using the offset actually in force that day.
// Midnight itself is never skipped or repeated by a US transition (both happen
// at 2 a.m.), so one correction pass is always enough.
const pacificMidnight = (year, month, day) => {
  const guess = new Date(Date.UTC(year, month - 1, day, 8, 0, 0));
  return new Date(Date.UTC(year, month - 1, day, pacificOffsetAt(guess), 0, 0));
};

/** Midnight Pacific on the day `date` falls on in Pacific time. */
export const getPDTMidnight = (date = new Date()) => {
  const f = pacificFields(date);
  return pacificMidnight(f.year, f.month, f.day);
};

/**
 * Parse a timeline date string (e.g. "Mar. 27, 2026") as midnight Pacific time.
 * Strips a leading "~" (approximate date marker) before parsing. Returns an
 * Invalid Date for strings the platform cannot parse — callers filter on
 * Number.isFinite of the timestamp.
 */
export const parseEventDatePDT = (dateStr) => {
  const parsed = new Date(dateStr.replace(/^~/, "").replace(/\./g, ""));
  if (Number.isNaN(parsed.getTime())) return parsed;
  // Read back the local fields the platform parsed, then re-anchor them to
  // Pacific midnight — the string carried a calendar day, not an instant.
  return pacificMidnight(parsed.getFullYear(), parsed.getMonth() + 1, parsed.getDate());
};
