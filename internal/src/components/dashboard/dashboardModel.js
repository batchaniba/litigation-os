// Pure view-model helpers for the Dashboard. Everything here is derived from
// the same queue as `npm run next` (clocks.json via useNextActions) and the
// matter summaries — no hand-maintained dates or counts.
import {
  addDaysToKey,
  daysBetween,
  isYours,
  weekStartKey,
} from "../../../scripts/lib/next-actions.mjs";

const MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
const DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function parseKey(key) {
  const [y, m, d] = String(key).split("-").map(Number);
  return { y, m, d, dow: new Date(Date.UTC(y, m - 1, d)).getUTCDay() };
}

/** "2026-11-09" → "Nov. 9" */
export function shortDate(key) {
  const { m, d } = parseKey(key);
  return `${MONTHS[m - 1]} ${d}`;
}

/** "2026-11-09" → { dow: "Mon", day: 9, label: "Mon Nov 9" } */
export function agendaDate(key) {
  const { m, d, dow } = parseKey(key);
  return { dow: DOW[dow], day: d, label: `${DOW[dow]} ${MONTHS[m - 1].replace(".", "")} ${d}` };
}

/** "Oct. 25 – 31" or "Oct. 25 – Nov. 1" */
export function weekRangeLabel(startKey) {
  const endKey = addDaysToKey(startKey, 6);
  const a = parseKey(startKey);
  const b = parseKey(endKey);
  return a.m === b.m
    ? `${MONTHS[a.m - 1]} ${a.d} – ${b.d}`
    : `${MONTHS[a.m - 1]} ${a.d} – ${MONTHS[b.m - 1]} ${b.d}`;
}

const PLAINTIFF_PREFIX = /^(?:Brendan\s+)?(?:Ngehsi\s+)?(?:Ngwa\s+)?(?:Newanforbi|Nforbi)\s+v\.\s+/i;

/** "Brendan Ngwa Nforbi v. Hertz Global Holdings, Inc." → "Hertz Global Holdings" */
export function shortCaption(caption) {
  let s = String(caption ?? "").replace(PLAINTIFF_PREFIX, "");
  s = s.replace(/,?\s+et\s+al\.?$/i, "");
  s = s.split(",")[0];
  s = s.replace(/\s+(?:Inc\.?|LLC|Corporation|Corp\.?|U\.S\.A\.,?)$/i, "").trim();
  return s || String(caption ?? "");
}

/** "USDC N.D. Cal." → "N.D. Cal."; "San Joaquin Sup. Ct." → "San Joaquin" */
export function shortCourt(court) {
  const s = String(court ?? "");
  const fed = s.match(/\b([NESC]\.D\. Cal\.)/);
  if (fed) return fed[1];
  const sup = s.match(/^([A-Z][A-Za-z ]+?) Sup(?:erior|\.)? Ct/);
  if (sup) return sup[1].trim();
  return s.split("(")[0].trim();
}

// Bookkeeping labels that help on the laptop desk view but read as noise in
// public: they say how a clock was entered, not what is due.
const META_LABEL = /^(?:IMPORTANT|DUE|FILE|WATCH|OPEN TASK|CONTINGENT|OPTIONAL|COMPUTED|DEADLINE|OUTER BOUND(?:\s*\([^)]*\))?)\s*(?:—|–|-|:)\s*/i;
const CAPTION_CUT = /\s+(?:(?:—|–|-)\s+|in\s+|for\s+)?(?:Brendan\s+)?(?:Ngehsi\s+)?(?:Ngwa\s+)?(?:Newanforbi|Nforbi)\s+v\.?\s.*$/i;
const RESTATED_DATE = /\s+(?:due|on|by)\s+(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)?\.?\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:,\s+\d{4})?/i;

// Abbreviations that end in a period mid-sentence; a period after one of
// these is not a sentence break.
const ABBR = new Set(["fed", "civ", "proc", "evid", "gov", "dkt", "no", "nos", "hon", "dept", "ct", "sup", "cal", "r", "p", "l", "v", "vs", "st", "jr", "sr", "inc", "co", "corp", "mon", "tue", "wed", "thu", "fri", "sat", "sun", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec", "a.m", "p.m", "u.s", "e.d", "n.d", "c.d", "s.d", "cf", "e.g", "i.e", "al", "ccp", "crc"]);
const COMMA_DATE = /,\s+(?:(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\.?\s+)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s+\d{4}.*$/;

function firstSentence(s) {
  const re = /([A-Za-z.)\]]+)\.\s+(?=[A-Z(])/g;
  let m;
  while ((m = re.exec(s))) {
    const word = m[1].replace(/[)\]]+$/, "").toLowerCase();
    if (m.index < 20 || ABBR.has(word) || word.length <= 2) continue;
    return s.slice(0, m.index + m[1].length);
  }
  return s;
}

/** Plain, public-safe title for a queue item: no bookkeeping tags, no caption, no restated date. */
export function shortTitle(event, max = 96) {
  let s = String(event ?? "").replace(/\s+/g, " ").trim();
  for (let i = 0; i < 4 && META_LABEL.test(s); i++) s = s.replace(META_LABEL, "");
  s = s.replace(/^Matter\s+\d+\s*(?:\([^)]*\))?\s*:?\s*/i, "");
  s = s.replace(/^(?:Deadline|Last day)\s+to\s+/i, "");
  // The verb chip already says File / Serve.
  s = s.replace(/^(?:file and serve|file|serve)\s+(?=[A-Z])/i, "");
  s = s.split(/\s*\[redacted\]/i)[0];
  s = s.split(/\s+USER REPORT\b/i)[0];
  s = s.replace(CAPTION_CUT, "");
  s = s.replace(COMMA_DATE, "");
  s = s.replace(RESTATED_DATE, "");
  // A leading ALL-CAPS phrase ("EX PARTE HEARING — …") reads as shouting.
  s = s.replace(/^([A-Z][A-Z0-9 ()§.'-]{3,}?)(\s+(?:—|–)\s+)/, (_, head, sep) => {
    const t = head.toLowerCase();
    return t.charAt(0).toUpperCase() + t.slice(1) + sep;
  });
  s = firstSentence(s);
  s = s.replace(/\s+(?:Dkt|No|Hon|Dept)\.?$/i, "");
  s = s.replace(/[\s—–:;,(-]+$/, "").trim();
  if (s.length > max) {
    const cut = s.slice(0, max);
    s = `${cut.slice(0, Math.max(cut.lastIndexOf(" "), max - 12))}…`;
  }
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Lane copy for a matter with no dated step: its status label without a stage word the lane already says. */
export function laneStatus(label) {
  return String(label ?? "").replace(/^(?:Pre-filing|Pending)\s*(?:—|–|-|:)\s*/i, "").replace(/^./, (c) => c.toUpperCase()) || "No date set";
}

/** First "h:mm a.m./p.m." in the event text, normalized. */
export function eventTime(event) {
  const m = String(event ?? "").match(/\b(\d{1,2}:\d{2})\s*(a\.?m\.?|p\.?m\.?)/i);
  if (!m) return null;
  return `${m[1]} ${m[2].toLowerCase().startsWith("a") ? "a.m." : "p.m."}`;
}

export const VERB = {
  appear: { label: "Appear", tone: "court" },
  "meet & confer": { label: "Confer", tone: "confer" },
  serve: { label: "Serve", tone: "task" },
  file: { label: "File", tone: "task" },
  prepare: { label: "Prep", tone: "task" },
};

export function verbFor(item) {
  if (!isYours(item)) return { label: "Their move", tone: "theirs" };
  return VERB[item.action] ?? { label: "Prep", tone: "task" };
}

function byDateThenMine(a, b) {
  if (a.dateKey !== b.dateKey) return a.dateKey < b.dateKey ? -1 : 1;
  const ay = isYours(a) ? 0 : 1;
  const by = isYours(b) ? 0 : 1;
  if (ay !== by) return ay - by;
  return (a.matters[0] ?? 0) - (b.matters[0] ?? 0);
}

function decorate(item, byNumber) {
  const m = byNumber.get(item.matters[0]);
  const court = m ? shortCourt(m.court) : "";
  const time = eventTime(item.event);
  return {
    ...item,
    key: `${item.dateKey}-${item.matters.join("-")}-${item.event.slice(0, 40)}`,
    matterLabel: item.matters.map((n) => `M${n}`).join(" / "),
    title: shortTitle(item.event),
    verb: verbFor(item),
    meta: [m ? shortCaption(m.caption) : null, court, time].filter(Boolean).join(" · "),
    when: agendaDate(item.dateKey),
  };
}

function relativeLabel(daysOut) {
  if (daysOut < 0) return `Past due · ${-daysOut} ${-daysOut === 1 ? "day" : "days"}`;
  if (daysOut === 0) return "Today";
  if (daysOut === 1) return "Tomorrow";
  return `In ${daysOut} days`;
}

/** Your overdue items, then yours due within 3 days. Opposing overdue is counted, not listed. */
export function needsAttention(queue, cases, limit = 5) {
  const byNumber = new Map(cases.map((c) => [Number(c.number), c]));
  const items = queue.items.filter((i) => isYours(i) && (i.urgency === "overdue" || i.urgency === "critical"));
  const sorted = [...items].sort(byDateThenMine).slice(0, limit).map((i) => ({
    ...decorate(i, byNumber),
    relative: relativeLabel(i.daysOut),
    tone: i.daysOut < 0 ? "late" : "soon",
  }));
  const overdue = items.filter((i) => i.urgency === "overdue").length;
  const soon = items.length - overdue;
  const opposingOverdue = queue.items.filter((i) => !isYours(i) && i.urgency === "overdue").length;
  return { items: sorted, overdue, soon, opposingOverdue };
}

/** Next 30 days, in date order, grouped Sunday–Saturday. */
export function agendaWeeks(queue, cases, { filter = "all", horizonDays = 30 } = {}) {
  const byNumber = new Map(cases.map((c) => [Number(c.number), c]));
  const thisWeek = weekStartKey(queue.today);
  const items = queue.items
    .filter((i) => i.daysOut >= 0 && i.daysOut <= horizonDays)
    .filter((i) => (filter === "mine" ? isYours(i) : filter === "court" ? i.action === "appear" : true))
    .sort(byDateThenMine)
    .map((i) => decorate(i, byNumber));
  const weeks = [];
  for (const item of items) {
    const start = weekStartKey(item.dateKey);
    let week = weeks.at(-1);
    if (!week || week.start !== start) {
      const offset = daysBetween(thisWeek, start) / 7;
      week = {
        start,
        label: offset === 0 ? "This week" : offset === 1 ? "Next week" : weekRangeLabel(start),
        range: offset <= 1 ? weekRangeLabel(start) : "",
        rows: [],
      };
      weeks.push(week);
    }
    week.rows.push(item);
  }
  return weeks;
}

export function agendaCounts(queue, horizonDays = 30) {
  const inWindow = queue.items.filter((i) => i.daysOut >= 0 && i.daysOut <= horizonDays);
  return {
    all: inWindow.length,
    mine: inWindow.filter(isYours).length,
    court: inWindow.filter((i) => i.action === "appear").length,
  };
}

/** 5-week strip starting this Sunday; each day lists the tones of its items. */
export function monthStrip(queue, weeksShown = 5) {
  const start = weekStartKey(queue.today);
  const byDay = new Map();
  for (const i of queue.items) {
    if (i.daysOut < 0) continue;
    const list = byDay.get(i.dateKey) ?? [];
    list.push(verbFor(i).tone);
    byDay.set(i.dateKey, list);
  }
  const days = [];
  for (let n = 0; n < weeksShown * 7; n++) {
    const key = addDaysToKey(start, n);
    const { d } = parseKey(key);
    days.push({
      key,
      label: d === 1 ? shortDate(key) : String(d),
      today: key === queue.today,
      past: key < queue.today,
      tones: (byDay.get(key) ?? []).slice(0, 3),
    });
  }
  const end = addDaysToKey(start, weeksShown * 7 - 1);
  return { days, label: `${shortDate(start)} – ${shortDate(end)}` };
}

export const LANES = [
  { key: "pre_filing", name: "Pre-filing", phases: ["pre_filing"] },
  { key: "service", name: "Service", phases: ["service"] },
  { key: "pleadings", name: "Pleadings", phases: ["pleadings", "screening_ifp"] },
  { key: "motions", name: "Motions & rulings", phases: ["mtd_briefing", "fr_pending", "under_submission", "district_review", "ruling", "traverse"] },
  { key: "hearings", name: "Discovery & hearings", phases: ["discovery", "hearing", "cmc", "trial"] },
  { key: "stayed", name: "Stayed", phases: ["stayed"] },
  { key: "settled", name: "Settled", phases: [] },
];

const OPEN = new Set(["active", "pre_filing", "settled"]);

/** Every open matter on a stage board with its next dated step (or why there is none). */
export function stageBoard(cases, queue) {
  const nextByMatter = new Map();
  for (const i of [...queue.items].sort(byDateThenMine)) {
    for (const n of i.matters) {
      const prev = nextByMatter.get(n);
      // Prefer the earliest item on your desk; fall back to theirs.
      if (!prev || (!isYours(prev) && isYours(i))) nextByMatter.set(n, i);
    }
  }
  const open = cases.filter((c) => OPEN.has(c.lifecycle) && !c.archived);
  const lanes = LANES.map((lane) => ({ ...lane, items: [] }));
  const other = { key: "other", name: "Other", phases: [], items: [] };
  for (const c of open) {
    const lane = c.lifecycle === "settled"
      ? lanes.find((l) => l.key === "settled")
      : lanes.find((l) => l.phases.includes(c.phase)) ?? other;
    const next = nextByMatter.get(Number(c.number));
    let line;
    let tone;
    if (c.lifecycle === "settled") {
      line = c.status_label || "Settled";
      tone = "normal";
    } else if (next && next.daysOut < 0 && isYours(next)) {
      line = `Past due · ${shortTitle(next.event, 34)}`;
      tone = "late";
    } else if (next && next.daysOut >= 0) {
      line = `${shortDate(next.dateKey)} · ${shortTitle(next.event, 34)}`;
      tone = isYours(next) ? "normal" : "muted";
    } else {
      line = laneStatus(c.status_label);
      tone = "undated";
    }
    lane.items.push({
      number: Number(c.number),
      name: shortCaption(c.caption),
      cluster: c.cluster,
      line,
      tone,
      sortKey: tone === "late" ? "0" : next && next.daysOut >= 0 ? `1${next.dateKey}` : "2",
    });
  }
  const all = other.items.length ? [...lanes, other] : lanes;
  for (const lane of all) lane.items.sort((a, b) => (a.sortKey < b.sortKey ? -1 : a.sortKey > b.sortKey ? 1 : a.number - b.number));
  return { lanes: all.filter((l) => l.items.length), total: open.length };
}

/** First court appearance on or after today. */
export function nextCourtDate(queue, cases) {
  const byNumber = new Map(cases.map((c) => [Number(c.number), c]));
  const hit = queue.items
    .filter((i) => i.daysOut >= 0 && i.action === "appear")
    .sort(byDateThenMine)[0];
  return hit ? decorate(hit, byNumber) : null;
}

/** Days since the last CourtListener sync, or null. */
export function syncAgeDays(lastDayKey, todayKey) {
  if (!lastDayKey || !todayKey) return null;
  return daysBetween(lastDayKey, todayKey);
}
