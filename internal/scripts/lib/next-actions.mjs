// ==========================================================
// Pure logic for the "what's next" queue.
//
// Reads nothing and writes nothing — callers hand in the timeline entries and
// matter summaries, so the ranking rules stay unit-testable. The CLI wrapper
// lives in internal/scripts/next-actions.mjs.
//
// Two things drive the queue:
//   1. live clocks.json rows (open/set, dated, including overdue; callers convert)
//   2. active matters with no dated obligation at all (coverage gaps)
// The converter lives in upcoming-from-clocks.mjs. buildQueue still takes
// timeline-shaped rows so fixture tests stay local.
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

const MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** "2026-11-20" -> "Nov. 20, 2026" */
export function dateLabelFromKey(key) {
  const match = String(key ?? "").match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!match) return null;
  const month = MONTH_ABBR[Number(match[2]) - 1];
  if (!month) return null;
  return `${month}. ${Number(match[3])}, ${match[1]}`;
}

export const PORTFOLIO_TZ = "America/Los_Angeles";

/** Today in a given IANA zone as an ISO day key. Portfolio dates are all PT. */
export function todayKey(timeZone = PORTFOLIO_TZ, now = new Date()) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(now);
  const value = Object.fromEntries(parts.map(({ type, value: v }) => [type, v]));
  return `${value.year}-${value.month}-${value.day}`;
}

/** Shift an ISO day key by a whole number of calendar days. */
export function addDaysToKey(key, days) {
  const [y, m, d] = String(key).split("-").map(Number);
  if (!y || !m || !d) return null;
  const shifted = new Date(Date.UTC(y, m - 1, d + Number(days)));
  return `${shifted.getUTCFullYear()}-${String(shifted.getUTCMonth() + 1).padStart(2, "0")}-${String(shifted.getUTCDate()).padStart(2, "0")}`;
}

/**
 * Milliseconds until the next civil midnight in `timeZone`.
 * Binary-searches the instant so DST fall-back (25-hour days) is covered.
 */
export function msUntilNextMidnight(timeZone = PORTFOLIO_TZ, now = new Date()) {
  const today = todayKey(timeZone, now);
  let lo = now.getTime();
  let hi = lo + 36 * 3_600_000;
  if (todayKey(timeZone, new Date(hi)) === today) hi += 12 * 3_600_000;
  while (hi - lo > 1) {
    const mid = Math.floor((lo + hi) / 2);
    if (todayKey(timeZone, new Date(mid)) === today) lo = mid;
    else hi = mid;
  }
  while (todayKey(timeZone, new Date(hi)) === today) hi += 1;
  return Math.max(1, hi - now.getTime());
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
const RETIRED_EVENT_RE =
  /^(?:VACATED|MOOTED|SUPERSEDED|SATISFIED|DONE|SETTLED)\b/i;

/** Title already marked finished — keep out of the live queue even if a clock leaked. */
export function isRetiredEventText(text) {
  return RETIRED_EVENT_RE.test(String(text ?? "").trim());
}

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
// Order matters: the head of the text names the task ("Opposition to …",
// "Joint status conference report …"), so a filing noun there beats a
// hearing or conference mentioned later in the same line.
const META_HEAD = /^(?:(?:IMPORTANT|DUE|FILE|WATCH|OPEN TASK|CONTINGENT|OPTIONAL|COMPUTED|DEADLINE)\s*(?:—|–|-|:)\s*)+/i;
const APPEAR_HEAD = /^(?:ex parte\s+)?(?:hearing|(?:initial\s+|further\s+)?case management conference|status conference|oral argument|trial)\b/i;
const FILING_NOUN = /\b(?:report|statement|brief|opposition|reply|certification|disclosures|request|motion|application|declaration|notice|answer|complaint)\b/i;

export function inferAction(entry) {
  const text = String(entry?.event ?? "");
  const head = text.replace(META_HEAD, "").split(/\s+[—–]\s+/)[0].slice(0, 90);
  if (entry?.type === "hearing" || APPEAR_HEAD.test(head)) return "appear";
  if (FILING_NOUN.test(head)) return "file";
  if (/\b(?:proof[-\s]of[-\s]service|service deadline)\b/i.test(text)) return "serve";
  if (/\bmeet[-\s]and[-\s]confer\b/i.test(text)) return "meet & confer";
  if (/\b(?:hearing|conference)\b/i.test(text)) return "appear";
  if (/\bserve\b/i.test(text)) return "serve";
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

/** Whole days remaining in the current Sunday–Saturday week (PT civil date). */
export function daysUntilSaturday(fromKey) {
  const [y, m, d] = String(fromKey).split("-").map(Number);
  if (!y || !m || !d) return 6;
  const dow = new Date(Date.UTC(y, m - 1, d)).getUTCDay(); // 0 Sun … 6 Sat
  return 6 - dow;
}

/** Sunday of the Sunday–Saturday week that contains `fromKey`. */
export function weekStartKey(fromKey) {
  const [y, m, d] = String(fromKey).split("-").map(Number);
  if (!y || !m || !d) return null;
  const dow = new Date(Date.UTC(y, m - 1, d)).getUTCDay();
  return addDaysToKey(fromKey, -dow);
}

/** Saturday of the Sunday–Saturday week that contains `fromKey`. */
export function weekEndKey(fromKey) {
  const [y, m, d] = String(fromKey).split("-").map(Number);
  if (!y || !m || !d) return null;
  const dow = new Date(Date.UTC(y, m - 1, d)).getUTCDay();
  return addDaysToKey(fromKey, 6 - dow);
}

/** True when `dateKey` falls in the Sunday–Saturday week that contains `today`. */
export function isInCurrentWeek(dateKey, today) {
  if (!dateKey || !today) return false;
  const start = weekStartKey(today);
  const end = weekEndKey(today);
  return Boolean(start && end && dateKey >= start && dateKey <= end);
}

/**
 * Exclusive list band. Overdue first, then next 3 days, then the rest of this
 * Sunday–Saturday week, then the rest of the horizon.
 *
 * Pill counts for This week / Next 30 days are inclusive — see queueBands().
 */
export function urgencyFor(daysOut, horizonDays, todayKey) {
  if (daysOut < 0) return "overdue";
  if (daysOut <= 3) return "critical";
  const weekLeft = todayKey ? daysUntilSaturday(todayKey) : 6;
  if (daysOut <= weekLeft) return "soon";
  if (daysOut <= horizonDays) return "upcoming";
  return "later";
}

export function isYours(item) {
  return item?.actor === "you" || item?.actor === "unknown";
}

function exclusiveBandKey(item) {
  if (item.urgency === "overdue") return isYours(item) ? "overdue" : "opposing_overdue";
  return item.urgency;
}

function inferTodayFromItems(items) {
  const sample = (items ?? []).find((item) => item?.dateKey && Number.isFinite(item.daysOut));
  if (!sample) return null;
  return addDaysToKey(sample.dateKey, -sample.daysOut);
}

export const QUEUE_BANDS = [
  { key: "overdue", label: "Past due" },
  { key: "opposing_overdue", label: "Opposing overdue" },
  { key: "critical", label: "Next 3 days" },
  { key: "soon", label: "This week" },
  { key: "upcoming", label: "Next 30 days" },
];

/**
 * Dashboard buckets.
 *
 * List rows are exclusive (each item once, most urgent band).
 * Pill counts for This week and Next 30 days are inclusive of nearer
 * upcoming items so "Next 3 days = 1, This week = 0" cannot happen when
 * that item still falls in the current Sunday–Saturday week.
 */
export function queueBands(items, options = {}) {
  const horizonDays = options.horizonDays ?? 30;
  const today = options.today ?? inferTodayFromItems(items);
  const mineOnly = options.mineOnly === true;
  const visible = (items ?? []).filter((item) => {
    if (item.urgency === "later") return false;
    if (mineOnly && !isYours(item)) return false;
    return true;
  });

  return QUEUE_BANDS.map((band) => {
    const exclusive = visible.filter((item) => exclusiveBandKey(item) === band.key);
    let count = exclusive.length;
    if (band.key === "soon") {
      count = visible.filter((item) => item.daysOut >= 0 && isInCurrentWeek(item.dateKey, today)).length;
    } else if (band.key === "upcoming") {
      count = visible.filter((item) => item.daysOut >= 0 && item.daysOut <= horizonDays).length;
    }
    return { key: band.key, label: band.label, items: exclusive, count };
  });
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

const PRECEDENT_KINDS = new Set(["same_statute", "same_denial_challenged"]);

/** Other matters that share a traveling statute or the same agency denial. */
export function precedentPeers(matter, clusters) {
  const peers = new Set();
  for (const cluster of clusters ?? []) {
    for (const link of cluster.links ?? []) {
      if (!(link.kinds ?? []).some((kind) => PRECEDENT_KINDS.has(kind))) continue;
      if (link.from === matter) peers.add(link.to);
      if (link.to === matter) peers.add(link.from);
    }
  }
  return [...peers].sort((a, b) => a - b);
}

/**
 * @param {Array<object>} timeline  timeline.json entries
 * @param {Array<object>} summaries matters/summaries.json entries
 * @param {{ today?: string, horizonDays?: number, clusters?: Array<object> }} [options]
 */
export function buildQueue(timeline, summaries, options = {}) {
  const today = options.today ?? todayKey();
  const horizonDays = options.horizonDays ?? 30;
  const clusters = options.clusters ?? [];
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
      source: typeof entry.source === "string" && entry.source.startsWith("/documents/")
        ? entry.source
        : null,
      verified_at: entry.verified_at ?? null,
      confidence: entry.confidence ?? null,
      source_type: entry.source_type ?? null,
      precedentPeers: [...new Set(matters.flatMap((n) => precedentPeers(n, clusters)))]
        .filter((n) => !matters.includes(n))
        .sort((a, b) => a - b),
      ...inferActor(entry),
    };

    // Abandoned / dismissed / settled / closed matters, and titles already
    // marked vacated / mooted / done, are not tasks. Keep them out of the queue
    // so a lapsed leave-to-amend on an archived case never leads PAST DUE.
    if (isRetiredEventText(shared.event) || !touchesActiveMatter(matters, byNumber)) {
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
    items.push({ ...shared, dateKey, daysOut, urgency: urgencyFor(daysOut, horizonDays, today) });
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

/** Next dated obligation on the litigant's desk that is not already overdue. */
export function nextOnYourDesk(queue) {
  return yourQueue(queue).find((i) => i.urgency !== "overdue") ?? null;
}
