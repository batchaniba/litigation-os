// ==========================================================
// Pure logic for the "what's next" queue.
//
// Reads nothing and writes nothing — callers hand in the timeline entries and
// matter summaries, so the ranking rules stay unit-testable. The CLI wrapper
// lives in internal/scripts/next-actions.mjs.
//
// Two things drive the queue:
//   1. timeline.json entries flagged `upcoming: true` (dated obligations)
//   2. active matters with no dated obligation at all (coverage gaps)
// ==========================================================

const MONTHS = new Map([
  ["jan", 1], ["january", 1],
  ["feb", 2], ["february", 2],
  ["mar", 3], ["march", 3],
  ["apr", 4], ["april", 4],
  ["may", 5],
  ["jun", 6], ["june", 6],
  ["jul", 7], ["july", 7],
  ["aug", 8], ["august", 8],
  ["sep", 9], ["sept", 9], ["september", 9],
  ["oct", 10], ["october", 10],
  ["nov", 11], ["november", 11],
  ["dec", 12], ["december", 12],
]);

// "Aug. 19, 2026" / "May 12, 2026" / "~Sep. 1, 2026" -> "2026-08-19".
// Deliberately rejects month-only ("Aug. 2025") and ranges ("Jul. 9-10, 2026"):
// those can't be placed on one day, so they can't be counted down to.
export function dateKeyFromLabel(value) {
  const match = String(value ?? "")
    .trim()
    .match(/^~?([A-Za-z]+)\.?\s+(\d{1,2}),\s*(\d{4})$/);
  if (!match) return null;
  const month = MONTHS.get(match[1].toLowerCase());
  if (!month) return null;
  const day = Number(match[2]);
  if (day < 1 || day > 31) return null;
  return `${match[3]}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

/** Today in a given IANA zone as an ISO day key. Portfolio dates are all PT. */
export function todayKey(timeZone = "America/Los_Angeles", now = new Date()) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(now);
  const value = Object.fromEntries(parts.map(({ type, value: v }) => [type, v]));
  return `${value.year}-${value.month}-${value.day}`;
}

/** Whole calendar days from `fromKey` to `toKey`; negative means already past. */
export function daysBetween(fromKey, toKey) {
  const [fy, fm, fd] = fromKey.split("-").map(Number);
  const [ty, tm, td] = toKey.split("-").map(Number);
  const MS_PER_DAY = 86_400_000;
  return Math.round((Date.UTC(ty, tm - 1, td) - Date.UTC(fy, fm - 1, fd)) / MS_PER_DAY);
}

// Who the clock actually runs against. An entry may pin this with an `actor`
// field; everything else is inferred from the event text and marked as such,
// because "the AG's reply is due" is not a task on this litigant's desk.
const OPPOSING_PATTERNS = [
  /\bAG (?:reply|response)\b/i,
  /\bRespondents?'? (?:reply|response|brief)\b/i,
  /\bresponsive pleading deadline\b/i,
  /\bdefendants?'? (?:reply|response|answer|responsive)\b/i,
  /\bopposition deadline\b.*\brespondents?\b/i,
  // CCP §430.41 demurrer meet-and-confer runs against the defendant who
  // intends to demur — not a task on this litigant's desk.
  /\bCCP\s*§?\s*430\.41\b/i,
  /\bif\s+(?:\w+\s+)+intends?\s+to\s+demur\b/i,
  /\bif\s+either\s+defendant\s+intends?\s+to\s+demur\b/i,
];
const AGENCY_PATTERNS = [
  /\bouter bound for\b/i,
  /\b(?:sheriff|clerk|court|USMS|U\.S\. Marshals)\b[^—]*\bto (?:process|issue|rule|act|serve)\b/i,
  /\bdeemed[- ]rejection\b/i,
  /\banticipated deemed\b/i,
];

const ACTIVE_LIFECYCLES = new Set(["active", "pre_filing"]);

export const ACTORS = ["you", "opposing", "agency", "court", "unknown"];
const ACTOR_ALIASES = { plaintiff: "you" };

export function inferActor(entry) {
  const raw = typeof entry?.actor === "string" ? entry.actor.toLowerCase() : null;
  const explicit = raw && (ACTOR_ALIASES[raw] ?? raw);
  if (explicit && ACTORS.includes(explicit)) {
    return { actor: explicit, actorSource: "explicit" };
  }
  const text = String(entry?.event ?? "");
  if (OPPOSING_PATTERNS.some((re) => re.test(text))) {
    return { actor: "opposing", actorSource: "inferred" };
  }
  if (AGENCY_PATTERNS.some((re) => re.test(text))) {
    return { actor: "agency", actorSource: "inferred" };
  }
  return { actor: "you", actorSource: "inferred" };
}

/** Coarse verb for the queue line — what the day actually demands. */
export function inferAction(entry) {
  const text = String(entry?.event ?? "");
  if (entry?.type === "hearing" || /\b(?:hearing|conference)\b/i.test(text)) return "appear";
  if (/\bmeet[-\s]and[-\s]confer\b/i.test(text)) return "meet & confer";
  if (/\b(?:proof[-\s]of[-\s]service|service deadline|serve)\b/i.test(text)) return "serve";
  // "Reply deadline" / "Opposition due" are filing tasks; match before the
  // generic prepare fallback (and ahead of bare "due", which also hits file).
  if (/\b(?:reply|opposition)\b/i.test(text) && /\b(?:deadline|due)\b/i.test(text)) {
    return "file";
  }
  if (/\b(?:file|filing|due|disclosures|statement|notice|claim)\b/i.test(text)) return "file";
  return "prepare";
}

/** True when at least one linked matter is still live (active / pre-filing). */
export function touchesActiveMatter(matters, byNumber) {
  if (!matters.length) return true;
  return matters.some((n) => {
    const m = byNumber.get(n);
    if (!m) return true;
    if (m.archived) return false;
    return ACTIVE_LIFECYCLES.has(m.lifecycle);
  });
}

/** Urgency band. Overdue first, then a 3/7/30-day ladder. */
export function urgencyFor(daysOut, horizonDays) {
  if (daysOut < 0) return "overdue";
  if (daysOut <= 3) return "critical";
  if (daysOut <= 7) return "soon";
  if (daysOut <= horizonDays) return "upcoming";
  return "later";
}

const URGENCY_RANK = new Map([
  ["overdue", 0],
  ["critical", 1],
  ["soon", 2],
  ["upcoming", 3],
  ["later", 4],
]);
const ACTOR_RANK = new Map([
  ["you", 0],
  ["unknown", 1],
  ["opposing", 2],
  ["agency", 2],
  ["court", 2],
]);

/**
 * @param {Array<object>} timeline  timeline.json entries
 * @param {Array<object>} summaries matters/summaries.json entries
 * @param {{ today?: string, horizonDays?: number }} [options]
 */
export function buildQueue(timeline, summaries, options = {}) {
  const today = options.today ?? todayKey();
  const horizonDays = options.horizonDays ?? 30;
  const byNumber = new Map((summaries ?? []).map((m) => [Number(m.number), m]));

  const items = [];
  const undated = [];
  const retired = [];

  for (const entry of timeline ?? []) {
    if (entry?.upcoming !== true) continue;
    const dateKey = dateKeyFromLabel(entry.date);
    const matters = (Array.isArray(entry.matters) ? entry.matters : []).map(Number);
    const shared = {
      date: entry.date,
      event: entry.event,
      type: entry.type ?? "event",
      matters,
      matterLabels: matters.map((n) => {
        const m = byNumber.get(n);
        return m ? `${n} — ${m.caption}${m.case_no ? ` (${m.case_no})` : ""}` : `${n}`;
      }),
      action: inferAction(entry),
      ...inferActor(entry),
    };

    // Abandoned / dismissed / closed matters still carrying upcoming: true are
    // data debt for validate-portfolio — not tasks. Keep them out of the queue
    // so a lapsed leave-to-amend on an abandoned case never leads PAST DUE.
    if (!touchesActiveMatter(matters, byNumber)) {
      retired.push(shared);
      continue;
    }

    // Ungroundable dates ("Dec. 2026", "Jul. 9-10, 2026") can't be ranked, but
    // dropping them silently would hide real obligations.
    if (!dateKey) {
      undated.push(shared);
      continue;
    }

    const daysOut = daysBetween(today, dateKey);
    items.push({ ...shared, dateKey, daysOut, urgency: urgencyFor(daysOut, horizonDays) });
  }

  items.sort((a, b) => {
    const byUrgency = URGENCY_RANK.get(a.urgency) - URGENCY_RANK.get(b.urgency);
    if (byUrgency !== 0) return byUrgency;
    const byActor = ACTOR_RANK.get(a.actor) - ACTOR_RANK.get(b.actor);
    if (byActor !== 0) return byActor;
    if (a.dateKey !== b.dateKey) return a.dateKey < b.dateKey ? -1 : 1;
    return (a.matters[0] ?? 0) - (b.matters[0] ?? 0);
  });

  const scheduled = new Set(items.flatMap((i) => i.matters).concat(undated.flatMap((i) => i.matters)));
  const gaps = (summaries ?? [])
    .filter((m) => (m.lifecycle === "active" || m.lifecycle === "pre_filing") && !m.archived)
    .filter((m) => !scheduled.has(Number(m.number)))
    .map((m) => ({
      number: Number(m.number),
      caption: m.caption,
      case_no: m.case_no ?? null,
      lifecycle: m.lifecycle,
      status_label: m.status_label ?? null,
    }))
    .sort((a, b) => a.number - b.number);

  return { today, horizonDays, items, undated, retired, gaps };
}

/** The short answer: overdue + everything inside the horizon that is yours. */
export function yourQueue(queue) {
  return queue.items.filter(
    (i) => i.urgency !== "later" && (i.actor === "you" || i.actor === "unknown"),
  );
}
