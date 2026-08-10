import type { MatterLifecycle, MatterPhase, MatterSummary, TimelineEvent } from "../types/portfolio";
import { lifecycleLabel, isTerminalLifecycle } from "./matterLifecycle";
import { eventsForMatter, matterActivity } from "./matterTimeline";
import { getPDTMidnight, parseEventDatePDT } from "./dateUtils";

/** Max length for badges, the summary strip, search, and README cells. */
export const STATUS_LABEL_MAX = 60;

type MatterLike = Pick<
  MatterSummary,
  "number" | "status_label" | "lifecycle" | "phase" | "serviceTracking"
>;

export type StatusLabelActivity = {
  next?: TimelineEvent;
  recent?: TimelineEvent;
  /** All timeline events for the matter (past + upcoming). Optional; loaded on demand. */
  events?: TimelineEvent[];
};

const PHASE_SHORT: Partial<Record<MatterPhase, string>> = {
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

export function clampStatusLabel(label: string, max = STATUS_LABEL_MAX): string {
  const cleaned = label.replace(/\s+/g, " ").trim();
  if (cleaned.length <= max) return cleaned;
  const cut = cleaned.slice(0, max - 1);
  const word = cut.lastIndexOf(" ");
  const base = (word > 36 ? cut.slice(0, word) : cut).trim();
  return `${base.replace(/[—–,:;-]+$/, "").trim()}…`;
}

/** Compact portfolio date strings stay as authored ("Aug. 12, 2026"). */
export function compactEventDate(date: string): string {
  return date.replace(/^~/, "").replace(/\s+/g, " ").trim();
}

function eventText(event: TimelineEvent): string {
  return `${event.type ?? ""} ${event.event ?? ""}`.toLowerCase();
}

/** Score how well an upcoming event represents current case posture (not admin chores). */
export function postureEventScore(event: TimelineEvent, phase?: MatterPhase): number {
  const text = eventText(event);
  let score = 0;
  // Real calendar hearings outrank deadline rows that merely mention a hearing.
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
  // Deprioritize collateral admin deadlines that sort earlier than the posture hearing.
  if (/\b(meet-and-confer|meet and confer|adr |adr-|usps|sheriff outer|postage|continued hearing|joinder)\b/.test(text)) {
    score -= 50;
  }
  if (event.type === "deadline") score += 8;
  if (event.type === "filing") score += 12;
  return score;
}

/** Waiting postures shouldn't collapse to an old Filed/Served milestone. */
const WAITING_PHASES = new Set<MatterPhase>([
  "fr_pending",
  "district_review",
  "under_submission",
  "stayed",
  "mtd_briefing",
]);

export function pickPostureEvent(
  events: TimelineEvent[],
  phase?: MatterPhase,
  now = +getPDTMidnight(),
): TimelineEvent | undefined {
  const upcoming = events
    .map((event) => ({ event, timestamp: +parseEventDatePDT(event.date), score: postureEventScore(event, phase) }))
    .filter((item) => item.event.upcoming && Number.isFinite(item.timestamp) && item.timestamp >= now)
    .sort((a, b) => b.score - a.score || a.timestamp - b.timestamp);
  return upcoming[0]?.event;
}

function postureKind(event: TimelineEvent, phase?: MatterPhase): string {
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
  if (phase && PHASE_SHORT[phase]) return PHASE_SHORT[phase]!;
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

function cleanServedDate(value: string): string {
  // "July 30, 2026 (Josh Swindell / Authorized Agent)" → "Jul. 30, 2026"
  const cleaned = compactEventDate(value.replace(/\s*\(.*$/, "").trim());
  const match = cleaned.match(/^([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})$/);
  if (!match) return cleaned;
  const stamp = Date.parse(`${match[1]} ${match[2]}, ${match[3]}`);
  if (!Number.isFinite(stamp)) return cleaned;
  const date = new Date(stamp);
  return `${MONTH_ABBR[date.getUTCMonth()]} ${date.getUTCDate()}, ${date.getUTCFullYear()}`;
}

function recentMilestone(
  matter: MatterLike,
  events: TimelineEvent[],
  now = +getPDTMidnight(),
): string | undefined {
  // Prefer structured serviceTracking — it's the cleanest "Served {date}" source.
  const servedDates = (matter.serviceTracking ?? [])
    .filter((row) => row.served && row.dateServed)
    .map((row) => cleanServedDate(row.dateServed!))
    .filter(Boolean)
    .sort((a, b) => +parseEventDatePDT(a) - +parseEventDatePDT(b));
  if (servedDates.length) {
    return `Served ${servedDates[servedDates.length - 1]!}`;
  }

  const past = events
    .map((event) => ({ event, timestamp: +parseEventDatePDT(event.date) }))
    .filter((item) => Number.isFinite(item.timestamp) && item.timestamp <= now && !item.event.upcoming)
    .sort((a, b) => b.timestamp - a.timestamp);

  for (const { event } of past.slice(0, 16)) {
    const text = eventText(event);
    const date = compactEventDate(event.date);
    // Avoid "service deadline" / "proof-of-service" chores being read as completed service.
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

function phaseFallback(phase: MatterPhase | undefined, lifecycle: MatterLifecycle | undefined): string {
  if (phase && phase !== "terminal" && PHASE_SHORT[phase]) return PHASE_SHORT[phase]!;
  if (lifecycle) return lifecycleLabel(lifecycle);
  return phase && phase !== "terminal" ? phase.replace(/_/g, " ") : "Active";
}

/**
 * Derive a short posture label from lifecycle/phase + timeline.
 * Terminal matters intentionally stay thin — keep a `status_label` override for
 * disposition nuance ("voluntarily dismissed", dual settlement dates, etc.).
 */
export function deriveStatusLabel(matter: MatterLike, activity: StatusLabelActivity = {}): string {
  const events = activity.events ?? eventsForMatter(matter.number);
  const now = +getPDTMidnight();
  const posture = pickPostureEvent(events, matter.phase, now);
  const lifecycle = matter.lifecycle;
  const phase = matter.phase;

  if (isTerminalLifecycle(lifecycle) || phase === "terminal") {
    // Never follow leftover upcoming events on abandoned/dismissed matters.
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

  // Waiting phases (awaiting a ruling/submission) should only surface a posture
  // date when it's an actual calendared hearing tied to that ruling — an
  // unrelated contingent deadline (e.g. a statute of limitations that only
  // starts running if the case is later dismissed) shouldn't make a matter
  // that's simply waiting on a judge look like it has something scheduled.
  const usablePosture =
    posture && phase && WAITING_PHASES.has(phase) && posture.type !== "hearing" ? undefined : posture;

  const milestone = recentMilestone(matter, events, now);
  if (usablePosture) {
    const kind = postureKind(usablePosture, phase);
    const dated = `${kind} ${compactEventDate(usablePosture.date)}`;
    // Served/Filed + later CMC/hearing is the common early-litigation pattern.
    const canPairMilestone =
      Boolean(milestone) &&
      !WAITING_PHASES.has(phase!) &&
      (kind === "CMC" ||
        kind === "Hearing" ||
        kind === "Demurrer hearing" ||
        kind === "Fee waiver hearing" ||
        (phase === "responsive_deadline" && kind === "Response due"));
    if (canPairMilestone) {
      return clampStatusLabel(`${milestone} — ${dated}`);
    }
    // Prefer the posture event's own kind ("CMC", "Demurrer hearing") over the
    // broader phase word when we have a dated calendar event.
    return clampStatusLabel(`${kind} — ${compactEventDate(usablePosture.date)}`);
  }

  // Waiting / under-submission without a live posture date: keep the phase words.
  if (phase && WAITING_PHASES.has(phase)) return phaseFallback(phase, lifecycle);
  if (milestone && (phase === "service" || phase === "responsive_deadline" || phase === "screening_ifp")) {
    return clampStatusLabel(milestone);
  }
  return phaseFallback(phase, lifecycle);
}

/**
 * Prefer a hand override (`status_label`) when present; otherwise derive from
 * phase + posture-ranked timeline events so labels self-update.
 */
export function effectiveStatusLabel(matter: MatterLike, activity?: StatusLabelActivity): string {
  const override = matter.status_label?.trim();
  if (override) return clampStatusLabel(override);

  if (activity) return deriveStatusLabel(matter, activity);
  const live = matterActivity(matter.number);
  return deriveStatusLabel(matter, {
    next: live.next,
    recent: live.recent,
    events: eventsForMatter(matter.number),
  });
}

/** True when the override merely restates what derivation already produces. */
export function isRedundantStatusLabelOverride(matter: MatterLike, activity?: StatusLabelActivity): boolean {
  const override = matter.status_label?.trim();
  if (!override) return false;
  const derived = activity ? deriveStatusLabel(matter, activity) : deriveStatusLabel(matter);
  const norm = (value: string) => value.toLowerCase().replace(/[—–-]/g, "-").replace(/\s+/g, " ").trim();
  return norm(override) === norm(derived);
}
