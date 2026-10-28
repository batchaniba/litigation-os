import { timeline } from "../data/timeline";
import type { PublicClock, TimelineEvent } from "../types/portfolio";
import { getPDTMidnight, parseEventDatePDT } from "./dateUtils";
import { parseMatterRefs } from "./matterRefs.js";
import { dateLabelFromKey, todayKey } from "../../scripts/lib/next-actions.mjs";

// The timeline is a flat log, but every consumer wants it keyed by matter. It was
// being re-scanned per lookup, and a status label costs two lookups — so rendering
// the matters list walked all 303 events 66 times. Partition it once instead.
//
// Portfolio-wide sentinels ("All", "All CDCR") are deliberately excluded, matching
// matterRefsInclude's default of includeAll: false.
const eventsByMatter = new Map<number, TimelineEvent[]>();
for (const event of timeline) {
  const { numbers } = parseMatterRefs(event.matters);
  for (const number of numbers) {
    const bucket = eventsByMatter.get(number);
    if (bucket) bucket.push(event);
    else eventsByMatter.set(number, [event]);
  }
}

const NO_EVENTS: readonly TimelineEvent[] = Object.freeze([]);

const SKIP_RECENT =
  /^(MOOT(?:ED)?|VACATED|SUPERSEDED)\b|\bMOOTED:|\bVACATED BY|Watch for (?:an?\s+)?(?:OSC|court order)|OSC RESPONSE WINDOW|Azimov response due|EXECUTED \(unfiled\)|hard cutoff|address of record|Oct\. 1 calendar passed|confirm PACER/i;

/** Timeline events naming this matter, in timeline order. Callers must not mutate
 *  the result — it is the shared index bucket, not a copy. */
export function eventsForMatter(matterNumber: number): TimelineEvent[] {
  return (eventsByMatter.get(Number(matterNumber)) ?? NO_EVENTS) as TimelineEvent[];
}

function isLivePublicClock(clock: PublicClock | undefined): clock is PublicClock {
  if (!clock || !clock.date) return false;
  if (clock.status === "vacated" || clock.status === "satisfied") return false;
  return true;
}

function clockAsEvent(clock: PublicClock, matterNumber: number): TimelineEvent {
  return {
    date: dateLabelFromKey(clock.date) || clock.date,
    event: clock.title,
    matters: [matterNumber],
    type: (clock.kind as TimelineEvent["type"]) || "event",
    upcoming: true,
    actor: clock.actor,
  } as TimelineEvent;
}

function nextFromClocks(clocks: PublicClock[] | undefined, matterNumber: number, nowKey: string): TimelineEvent | undefined {
  const upcoming = (clocks ?? [])
    .filter(isLivePublicClock)
    .filter((clock) => clock.date >= nowKey)
    .slice()
    .sort((a, b) => {
      if (a.date !== b.date) return a.date < b.date ? -1 : 1;
      const aYou = a.actor === "you" || a.actor === "unknown" || !a.actor ? 0 : 1;
      const bYou = b.actor === "you" || b.actor === "unknown" || !b.actor ? 0 : 1;
      return aYou - bYou;
    });
  const yours = upcoming.find((c) => !c.actor || c.actor === "you" || c.actor === "unknown");
  const chosen = yours ?? upcoming[0];
  return chosen ? clockAsEvent(chosen, matterNumber) : undefined;
}

export function matterActivity(matterNumber: number, options: { clocks?: PublicClock[] } = {}) {
  const now = +getPDTMidnight();
  const nowKey = todayKey();
  let next: TimelineEvent | undefined = nextFromClocks(options.clocks, matterNumber, nowKey);
  let nextTs = next ? +parseEventDatePDT(next.date) : Infinity;
  let recent: TimelineEvent | undefined;
  let recentTs = -Infinity;

  for (const event of eventsForMatter(matterNumber)) {
    const timestamp = +parseEventDatePDT(event.date);
    if (!Number.isFinite(timestamp)) continue;
    const text = `${event.event ?? ""}`;
    if (!options.clocks && timestamp >= now && event.upcoming && timestamp < nextTs) {
      next = event;
      nextTs = timestamp;
    }
    if (timestamp <= now && timestamp > recentTs && !SKIP_RECENT.test(text)) {
      recent = event;
      recentTs = timestamp;
    }
  }
  return { next, recent };
}
