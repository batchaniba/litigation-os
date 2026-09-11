import type { IntelligenceCatalog, LitigationEvent, LitigationEventType } from "./types";
import type { TimelineEvent } from "../types/portfolio";
import { parseMatterRefs } from "../utils/matterRefs.js";
import {
  classifyDocketText as classifyFromSignals,
  enrichEventRecord,
  issuesInText,
  mentionedDockets,
} from "./filingSignals.js";

export function classifyDocketText(text: string): LitigationEventType {
  return classifyFromSignals(text) as LitigationEventType;
}

export function issuesMentioned(text: string, catalog: IntelligenceCatalog): string[] {
  return issuesInText(text, catalog.issues);
}

function docketFromText(text: string, fallback?: number | null): number | undefined {
  if (fallback != null && Number.isInteger(fallback)) return fallback;
  return mentionedDockets(text)[0];
}

export function enrichEvent(event: LitigationEvent, catalog: IntelligenceCatalog): LitigationEvent {
  const body = typeof event.payload?.body === "string" ? event.payload.body : "";
  const text = [event.summary, body].filter(Boolean).join("\n");
  const docket = event.docket ?? docketFromText(text, Number(event.payload?.docket) || null);
  return enrichEventRecord({ ...event, docket }, catalog) as LitigationEvent;
}

export function eventFromTimeline(
  event: TimelineEvent,
  catalog: IntelligenceCatalog,
  index: number,
): LitigationEvent | null {
  const text = `${event.type} ${event.event}`;
  const { numbers } = parseMatterRefs(event.matters);
  const matter = numbers[0];
  let type: LitigationEventType =
    event.type === "order" ? "ORDER_ENTERED" : event.type === "deadline" ? "DEADLINE_TRIGGERED" : classifyDocketText(text);
  if (/\bunfiled\b|drafted \(unfiled\)/i.test(event.event) && type === "MOTION_FILED") type = "DOCKET_ENTRY_ADDED";
  const issues = issuesMentioned(text, catalog);
  return enrichEvent(
    {
      id: `tl-${index}-${event.date}`,
      at: event.date,
      type,
      matter,
      summary: event.event,
      issues,
      actor: event.actor,
      payload: {
        source_type: event.source_type ?? "portfolio",
        docket: event.external?.entry_number ?? null,
        body: event.event,
      },
    },
    catalog,
  );
}

export function eventsFromTimeline(timeline: TimelineEvent[], catalog: IntelligenceCatalog): LitigationEvent[] {
  return timeline.map((event, index) => eventFromTimeline(event, catalog, index)).filter((row): row is LitigationEvent => Boolean(row));
}

export function eventFromNormalizedEntry(
  entry: {
    matter: number;
    description?: string;
    body?: string;
    date_filed?: string;
    entry_number?: number | null;
    courtlistener_entry_id?: number | null;
  },
  catalog: IntelligenceCatalog,
): LitigationEvent {
  const description = entry.description ?? "";
  const body = entry.body ?? "";
  return enrichEvent(
    {
      id: `cl-${entry.matter}-${entry.courtlistener_entry_id ?? entry.entry_number ?? description.slice(0, 24)}`,
      type: classifyDocketText(`${description} ${body}`),
      at: entry.date_filed ?? "",
      matter: entry.matter,
      docket: entry.entry_number ?? undefined,
      summary: description,
      issues: issuesMentioned(`${description}\n${body}`, catalog),
      payload: { provider: "courtlistener", body },
    },
    catalog,
  );
}
