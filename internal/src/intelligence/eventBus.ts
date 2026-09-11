import type { LitigationEvent, LitigationEventType } from "./types";

export type EventHandler = (event: LitigationEvent) => void;

const listeners = new Map<LitigationEventType | "*", Set<EventHandler>>();
const log: LitigationEvent[] = [];

export function subscribe(type: LitigationEventType | "*", handler: EventHandler): () => void {
  const bucket = listeners.get(type) ?? new Set<EventHandler>();
  bucket.add(handler);
  listeners.set(type, bucket);
  return () => {
    listeners.get(type)?.delete(handler);
  };
}

export function resetEventBus() {
  listeners.clear();
  log.length = 0;
}

export function publishedEvents(): readonly LitigationEvent[] {
  return log;
}

export function publish(event: LitigationEvent): void {
  log.push(event);
  for (const handler of listeners.get(event.type) ?? []) handler(event);
  for (const handler of listeners.get("*") ?? []) handler(event);
}

export function publishAll(events: LitigationEvent[]): void {
  for (const event of events) publish(event);
}

/** Named agents so sync-dockets stays a dispatcher, not a 4,000-line monster. */
export function registerDefaultAgents(agents: Record<string, EventHandler>): () => void {
  const unsub = Object.values(agents).map((handler) => subscribe("*", handler));
  return () => {
    for (const stop of unsub) stop();
  };
}
