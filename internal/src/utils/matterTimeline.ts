import { timeline } from "../data/timeline";
import type { TimelineEvent } from "../types/portfolio";
import { getPDTMidnight, parseEventDatePDT } from "./dateUtils";
import { parseMatterRefs } from "./matterRefs.js";

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

/** Timeline events naming this matter, in timeline order. Callers must not mutate
 *  the result — it is the shared index bucket, not a copy. */
export function eventsForMatter(matterNumber: number): TimelineEvent[] {
  return (eventsByMatter.get(Number(matterNumber)) ?? NO_EVENTS) as TimelineEvent[];
}

export function matterActivity(matterNumber: number) {
  const now = +getPDTMidnight();
  let next: TimelineEvent | undefined;
  let nextTs = Infinity;
  let recent: TimelineEvent | undefined;
  let recentTs = -Infinity;

  // Two linear passes rather than map + two filters + two sorts: only the extremes
  // are ever read, so there is nothing to gain from ordering the rest.
  for (const event of eventsForMatter(matterNumber)) {
    const timestamp = +parseEventDatePDT(event.date);
    if (!Number.isFinite(timestamp)) continue;
    if (timestamp >= now && event.upcoming && timestamp < nextTs) {
      next = event;
      nextTs = timestamp;
    }
    if (timestamp <= now && timestamp > recentTs) {
      recent = event;
      recentTs = timestamp;
    }
  }
  return { next, recent };
}
