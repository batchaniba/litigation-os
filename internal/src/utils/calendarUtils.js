import { parseEventDatePDT } from "./dateUtils";

// A "groundable" date is exactly "[~]Month[.] D, YYYY" -- one calendar day, unambiguous.
// Anything else (month-only, ranges, "Mid-2025", etc.) is intentionally rejected here,
// even though parseEventDatePDT would happily (and sometimes wrongly) parse it --
// e.g. "Jul. 9-10, 2026" silently parses to July 9, 2010 via native Date parsing.
const GROUNDED_RE = /^~?[A-Za-z]+\.?\s+\d{1,2},\s*\d{4}$/;

export const isGroundedDate = (dateStr) => GROUNDED_RE.test(dateStr.trim());

// Returns a PDT-midnight Date, or null if the string can't be placed on one specific day.
export const groundEventDate = (dateStr) => {
  if (!isGroundedDate(dateStr)) return null;
  const d = parseEventDatePDT(dateStr);
  return isNaN(d.getTime()) ? null : d;
};

// Day key derived from the UTC fields of a PDT-midnight Date. Must use getUTC*, not
// local getters, since getPDTMidnight/parseEventDatePDT already encode the correct
// calendar day in the UTC fields (with the hour set to represent the PT offset).
export const dayKey = (date) =>
  `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, "0")}-${String(date.getUTCDate()).padStart(2, "0")}`;

// 42-cell (6x7) grid for a given year/month (month: 0-11), Sunday-first, using UTC
// arithmetic throughout so cell keys line up with dayKey() from groundEventDate().
export const buildMonthGrid = (year, month) => {
  const startWeekday = new Date(Date.UTC(year, month, 1)).getUTCDay();
  const cells = [];
  for (let i = 0; i < 42; i++) {
    const d = new Date(Date.UTC(year, month, 1 - startWeekday + i));
    cells.push({ date: d, key: dayKey(d), inMonth: d.getUTCMonth() === month });
  }
  return cells;
};

// Groups timeline entries by day key; anything ungroundable goes into a side list
// instead of being dropped or mis-placed.
export const groupEventsByDay = (timeline) => {
  const byDay = new Map();
  const ungrounded = [];
  for (const t of timeline) {
    const d = groundEventDate(t.date);
    if (!d) { ungrounded.push(t); continue; }
    const key = dayKey(d);
    if (!byDay.has(key)) byDay.set(key, []);
    byDay.get(key).push(t);
  }
  return { byDay, ungrounded };
};

// "9,6,5,11,15" -> [9,6,5,11,15]; "20" -> [20]; "All"/"All CDCR" -> all:true.
export const parseMatterNumbers = (mattersStr) => {
  const trimmed = (mattersStr || "").trim();
  if (/^all\b/i.test(trimmed)) return { all: true, numbers: [], label: trimmed };
  const numbers = trimmed.split(",").map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
  return { all: false, numbers, label: trimmed };
};
