import { timeline } from "../data/timeline";
import type { TimelineEvent } from "../types/portfolio";
import { getPDTMidnight, parseEventDatePDT } from "./dateUtils";
import { matterRefsInclude } from "./matterRefs.js";

export function eventsForMatter(matterNumber: number): TimelineEvent[] {
  return timeline.filter((event) => matterRefsInclude(event.matters, matterNumber));
}

export function matterActivity(matterNumber: number) {
  const now = +getPDTMidnight();
  const events = eventsForMatter(matterNumber).map((event) => ({ event, timestamp: +parseEventDatePDT(event.date) })).filter((item) => Number.isFinite(item.timestamp));
  const next = events.filter((item) => item.timestamp >= now && item.event.upcoming).sort((a, b) => a.timestamp - b.timestamp)[0]?.event;
  const recent = events.filter((item) => item.timestamp <= now).sort((a, b) => b.timestamp - a.timestamp)[0]?.event;
  return { next, recent };
}
