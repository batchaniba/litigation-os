// Shared status-label helpers for Node scripts (validate, README gen).
// Keep in sync with internal/src/utils/statusLabel.ts.

import { lifecycleLabel, isTerminalLifecycle } from "./matter-lifecycle.mjs";

export const STATUS_LABEL_MAX = 60;

const PHASE_SHORT = {
  fr_pending: "F&R pending",
  district_review: "District Judge review",
  under_submission: "Under submission",
  stayed: "Stayed",
  default: "Default prove-up",
  demurrer: "Demurrer",
  cmc: "CMC",
  responsive_deadline: "Response pending",
  screening_ifp: "IFP / screening",
  mtd_briefing: "MTD briefing",
  service: "Service",
  pre_filing: "Pre-filing",
  hearing: "Hearing",
  petition_filed: "Petition filed",
  return_awaited: "Return awaited",
  discovery: "Discovery",
  pleadings: "Pleadings",
};

const WAITING_PHASES = new Set(["fr_pending", "district_review", "under_submission", "stayed", "mtd_briefing"]);

export function clampStatusLabel(label, max = STATUS_LABEL_MAX) {
  const cleaned = String(label ?? "").replace(/\s+/g, " ").trim();
  if (cleaned.length <= max) return cleaned;
  const cut = cleaned.slice(0, max - 1);
  const word = cut.lastIndexOf(" ");
  const base = (word > 36 ? cut.slice(0, word) : cut).trim();
  return `${base.replace(/[—–,:;-]+$/, "").trim()}…`;
}

export function compactEventDate(date) {
  return String(date ?? "").replace(/^~/, "").replace(/\s+/g, " ").trim();
}

function eventText(event) {
  return `${event?.type ?? ""} ${event?.event ?? ""}`.toLowerCase();
}

function parsePortfolioDate(dateStr) {
  const s = String(dateStr || "")
    .replace(/^~/, "")
    .replace(/\./g, "")
    .trim();
  const t = Date.parse(s);
  return Number.isFinite(t) ? t : NaN;
}

export function postureEventScore(event, phase) {
  const text = eventText(event);
  let score = 0;
  if (event.type === "hearing") score += 110;
  else if (/\b(hearing|prove-up)\b/.test(text)) score += 55;
  if (/\b(cmc|case management conference)\b/.test(text)) score += 95;
  if (/\bdemurrer hearing\b/.test(text)) score += 100;
  else if (/\bdemurrer\b/.test(text) && /\b(opposition|reply)\b/.test(text)) score += 45;
  else if (/\bdemurrer\b/.test(text)) score += 70;
  if (/\b(response due|responsive pleading|answer due|plea(?:ding)? due)\b/.test(text)) score += 85;
  if (/\b(anticipated filing|filing date|complaint filing)\b/.test(text)) score += 88;
  if (/\bfee waiver hearing\b/.test(text)) score += 80;
  if (phase === "demurrer" && event.type === "hearing" && /\bdemurrer\b/.test(text)) score += 40;
  if (phase === "demurrer" && /\b(reply|opposition)\b/.test(text) && event.type !== "hearing") score += 15;
  if (phase === "cmc" && /\bcmc\b/.test(text)) score += 20;
  if (phase === "default" && /\b(prove-up|default|cmc)\b/.test(text)) score += 20;
  if (phase === "responsive_deadline" && /\b(response due|responsive)\b/.test(text)) score += 30;
  if (phase === "pre_filing" && /\bfil(e|ing)\b/.test(text)) score += 25;
  if (/\b(meet-and-confer|meet and confer|adr |adr-|usps|sheriff outer|postage|continued hearing|joinder)\b/.test(text)) {
    score -= 50;
  }
  if (event.type === "deadline") score += 8;
  if (event.type === "filing") score += 12;
  return score;
}

export function pickPostureEvent(events, phase, now = Date.now()) {
  const upcoming = (events ?? [])
    .map((event) => ({
      event,
      timestamp: parsePortfolioDate(event.date),
      score: postureEventScore(event, phase),
    }))
    .filter((item) => item.event.upcoming && Number.isFinite(item.timestamp) && item.timestamp >= now)
    .sort((a, b) => b.score - a.score || a.timestamp - b.timestamp);
  return upcoming[0]?.event;
}

function postureKind(event, phase) {
  const text = eventText(event);
  if (/\bdefault prove-up\b/.test(text) || (phase === "default" && /\b(prove-up|cmc)\b/.test(text))) {
    return "Default prove-up";
  }
  if (/\bdemurrer hearing\b/.test(text) || (/\bdemurrer\b/.test(text) && event.type === "hearing")) {
    return "Demurrer hearing";
  }
  if (/\bfee waiver hearing\b/.test(text)) return "Fee waiver hearing";
  if (/\b(cmc|case management conference)\b/.test(text)) return "CMC";
  if (/\banticipated filing\b/.test(text)) return "Anticipated filing";
  if (/\b(response due|responsive pleading)\b/.test(text)) return "Response due";
  if (event.type === "hearing" || /\bhearing\b/.test(text)) return "Hearing";
  if (phase && PHASE_SHORT[phase]) return PHASE_SHORT[phase];
  return "Next deadline";
}

const MONTH_ABBR = [
  "Jan.",
  "Feb.",
  "Mar.",
  "Apr.",
  "May",
  "Jun.",
  "Jul.",
  "Aug.",
  "Sep.",
  "Oct.",
  "Nov.",
  "Dec.",
];

function cleanServedDate(value) {
  const cleaned = compactEventDate(String(value).replace(/\s*\(.*$/, "").trim());
  const match = cleaned.match(/^([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})$/);
  if (!match) return cleaned;
  const stamp = Date.parse(`${match[1]} ${match[2]}, ${match[3]}`);
  if (!Number.isFinite(stamp)) return cleaned;
  const date = new Date(stamp);
  return `${MONTH_ABBR[date.getUTCMonth()]} ${date.getUTCDate()}, ${date.getUTCFullYear()}`;
}

function recentMilestone(matter, events, now = Date.now()) {
  const servedDates = (matter.serviceTracking ?? [])
    .filter((row) => row.served && row.dateServed)
    .map((row) => cleanServedDate(row.dateServed))
    .filter(Boolean)
    .sort((a, b) => parsePortfolioDate(a) - parsePortfolioDate(b));
  if (servedDates.length) return `Served ${servedDates[servedDates.length - 1]}`;

  const past = (events ?? [])
    .map((event) => ({ event, timestamp: parsePortfolioDate(event.date) }))
    .filter((item) => Number.isFinite(item.timestamp) && item.timestamp <= now && !item.event.upcoming)
    .sort((a, b) => b.timestamp - a.timestamp);

  for (const { event } of past.slice(0, 16)) {
    const text = eventText(event);
    const date = compactEventDate(event.date);
    if (/\b(service deadline|proof-of-service|to be served|awaiting service)\b/.test(text)) continue;
    if (
      (/\bserved\b/.test(text) || /\bservice confirmed\b/.test(text)) &&
      !/\bnot served\b/.test(text) &&
      !/\bdeadline\b/.test(text)
    ) {
      return `Served ${date}`;
    }
    if (/\b(case filed|complaint filed|filed complaint|complaint docketed)\b/.test(text)) {
      return `Filed ${date}`;
    }
  }
  return undefined;
}

function phaseFallback(phase, lifecycle) {
  if (phase && phase !== "terminal" && PHASE_SHORT[phase]) return PHASE_SHORT[phase];
  if (lifecycle) return lifecycleLabel(lifecycle);
  return phase && phase !== "terminal" ? phase.replace(/_/g, " ") : "Active";
}

export function deriveStatusLabel(matter, events = [], now = Date.now()) {
  const posture = pickPostureEvent(events, matter.phase, now);
  const lifecycle = matter.lifecycle;
  const phase = matter.phase;

  if (isTerminalLifecycle(lifecycle) || phase === "terminal") {
    return lifecycleLabel(lifecycle);
  }

  if (lifecycle === "pre_filing" || phase === "pre_filing") {
    const filing =
      posture && /\b(anticipated filing|filing date|complaint filing|fil(e|ing))\b/.test(eventText(posture))
        ? posture
        : pickPostureEvent(
            events.filter((event) => /\b(anticipated filing|filing date|fil(e|ing))\b/.test(eventText(event))),
            phase,
            now,
          );
    if (filing) {
      return clampStatusLabel(`Pre-filing — anticipated filing ${compactEventDate(filing.date)}`);
    }
    return "Pre-filing";
  }

  const milestone = recentMilestone(matter, events, now);
  if (posture) {
    const kind = postureKind(posture, phase);
    const dated = `${kind} ${compactEventDate(posture.date)}`;
    const canPairMilestone =
      Boolean(milestone) &&
      !WAITING_PHASES.has(phase) &&
      (kind === "CMC" ||
        kind === "Hearing" ||
        kind === "Demurrer hearing" ||
        kind === "Fee waiver hearing" ||
        (phase === "responsive_deadline" && kind === "Response due"));
    if (canPairMilestone) {
      return clampStatusLabel(`${milestone} — ${dated}`);
    }
    return clampStatusLabel(`${kind} — ${compactEventDate(posture.date)}`);
  }

  if (phase && WAITING_PHASES.has(phase)) return phaseFallback(phase, lifecycle);
  if (milestone && (phase === "service" || phase === "responsive_deadline" || phase === "screening_ifp")) {
    return clampStatusLabel(milestone);
  }
  return phaseFallback(phase, lifecycle);
}

export function effectiveStatusLabel(matter, events = [], now = Date.now()) {
  const override = typeof matter.status_label === "string" ? matter.status_label.trim() : "";
  if (override) return clampStatusLabel(override);
  return deriveStatusLabel(matter, events, now);
}

export function isRedundantStatusLabelOverride(matter, events = [], now = Date.now()) {
  const override = typeof matter.status_label === "string" ? matter.status_label.trim() : "";
  if (!override) return false;
  const derived = deriveStatusLabel(matter, events, now);
  const norm = (value) => value.toLowerCase().replace(/[—–-]/g, "-").replace(/\s+/g, " ").trim();
  return norm(override) === norm(derived);
}
