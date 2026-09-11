import type { IntelligenceCatalog, LitigationEvent, LitigationEventType } from "./types";
import type { TimelineEvent } from "../types/portfolio";
import { parseMatterRefs } from "../utils/matterRefs.js";

const MOTION = /motion to dismiss|notice of motion|rule 12|12\(b\)\(6\)|demurrer/i;
const ORDER = /\border\b|clerk.?s notice|findings?\s*(and|&)\s*recommendations?/i;
const COUNSEL = /notice of appearance|appeared for|counsel of record/i;
const SETTLED = /\bsettled\b|notice of settlement|stipulation of dismissal/i;
const TRIGGER_LANGUAGE = /within \d+ days|shall file|deadline|continued.{0,40}after/i;

export function classifyDocketText(text: string): LitigationEventType {
  if (SETTLED.test(text)) return "CASE_SETTLED";
  if (COUNSEL.test(text)) return "COUNSEL_APPEARED";
  if (MOTION.test(text)) return "MOTION_FILED";
  if (ORDER.test(text)) return "ORDER_ENTERED";
  if (TRIGGER_LANGUAGE.test(text)) return "DEADLINE_TRIGGERED";
  return "DOCKET_ENTRY_ADDED";
}

export function issuesMentioned(text: string, catalog: IntelligenceCatalog): string[] {
  const lower = text.toLowerCase();
  return catalog.issues.filter((issue) => issue.keywords.some((keyword) => lower.includes(keyword.toLowerCase()))).map((issue) => issue.id);
}

export function eventFromTimeline(
  event: TimelineEvent,
  catalog: IntelligenceCatalog,
  index: number,
): LitigationEvent | null {
  const text = `${event.type} ${event.event}`;
  const { numbers } = parseMatterRefs(event.matters);
  const matter = numbers[0];
  const type = event.type === "order" ? "ORDER_ENTERED" : event.type === "deadline" ? "DEADLINE_TRIGGERED" : classifyDocketText(text);
  const issues = issuesMentioned(text, catalog);
  return {
    id: `tl-${index}-${event.date}`,
    type,
    at: event.date,
    matter,
    summary: event.event,
    issues,
    actor: event.actor,
    payload: { source_type: event.source_type ?? "portfolio", docket: event.external?.entry_number ?? null },
  };
}

export function eventsFromTimeline(timeline: TimelineEvent[], catalog: IntelligenceCatalog): LitigationEvent[] {
  return timeline.map((event, index) => eventFromTimeline(event, catalog, index)).filter((row): row is LitigationEvent => Boolean(row));
}

export function eventFromNormalizedEntry(
  entry: {
    matter: number;
    description?: string;
    date_filed?: string;
    entry_number?: number | null;
    courtlistener_entry_id?: number | null;
  },
  catalog: IntelligenceCatalog,
): LitigationEvent {
  const description = entry.description ?? "";
  return {
    id: `cl-${entry.matter}-${entry.courtlistener_entry_id ?? entry.entry_number ?? description.slice(0, 24)}`,
    type: classifyDocketText(description),
    at: entry.date_filed ?? "",
    matter: entry.matter,
    docket: entry.entry_number ?? undefined,
    summary: description,
    issues: issuesMentioned(description, catalog),
    payload: { provider: "courtlistener" },
  };
}
