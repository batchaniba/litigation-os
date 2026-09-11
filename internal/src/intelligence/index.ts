import { intelligenceCatalog } from "../data/intelligence/catalog";
import loggedEventLog from "../data/intelligence/events.json";
import { cases } from "../data/matters";
import { timeline } from "../data/timeline";
import type { MatterSummary, TimelineEvent } from "../types/portfolio";
import { diffsForMatter, diffsFromEvents } from "./argumentDiff";
import { briefingClocksFromEvents, resolveDeadlines } from "./deadlines";
import { auditCatalog } from "./citeProof";
import { enrichEvent, eventsFromTimeline } from "./classify";
import {
  COVERAGE_DISCLAIMER,
  type IntelligenceCatalog,
  type KnowledgeGraph,
  type LitigationEvent,
  type LitigationTwin,
  type OvernightBrief,
  type PendingClock,
  type WarRoom,
} from "./types";
import { coverageReport, matrixForMatter } from "./coverage";
import { publishAll, resetEventBus } from "./eventBus";
import { fingerprintForMatter } from "./fingerprints";
import { buildKnowledgeGraph } from "./graph";
import { overnightBrief } from "./overnight";
import { qiRadar } from "./queries";
import { recapAdvice } from "./recap";
import { shockwaveFromOpinion } from "./shockwave";
import { simulateDomino, systemicImportance } from "./systemic";
import { deriveTwin } from "./twin";
import { warRoomsFromEvents } from "./warRoom";

export { COVERAGE_DISCLAIMER };

export interface LitigationOS {
  catalog: IntelligenceCatalog;
  graph: KnowledgeGraph;
  events: LitigationEvent[];
  twins: LitigationTwin[];
  clocks: PendingClock[];
  warRooms: WarRoom[];
  overnight: OvernightBrief;
  disclaimer: string;
}

export interface AssembleInput {
  summaries?: MatterSummary[];
  timeline?: TimelineEvent[];
  catalog?: IntelligenceCatalog;
  /** Pre-classified feed (CourtListener log or a test fixture). */
  events?: LitigationEvent[];
  asOf?: string;
  publish?: boolean;
}

function upcomingClocks(summary: MatterSummary, events: TimelineEvent[]): PendingClock[] {
  return events
    .filter((event) => event.upcoming && Array.isArray(event.matters) && event.matters.includes(summary.number))
    .map((event, index) => ({
      id: `upcoming-${summary.number}-${index}`,
      matter: summary.number,
      label: event.event.slice(0, 180),
      status: "date_certain" as const,
      date: event.date,
      displayDate: event.date,
    }));
}

function mergeEventStreams(preferred: LitigationEvent[], fallback: LitigationEvent[]): LitigationEvent[] {
  const seenIds = new Set(preferred.map((event) => event.id));
  const seenKeys = new Set(
    preferred
      .filter((event) => event.matter != null && event.docket != null)
      .map((event) => `${event.matter}:${event.docket}:${event.type}`),
  );
  const merged = [...preferred];
  for (const event of fallback) {
    if (seenIds.has(event.id)) continue;
    const key = event.matter != null && event.docket != null ? `${event.matter}:${event.docket}:${event.type}` : null;
    if (key && seenKeys.has(key)) continue;
    seenIds.add(event.id);
    if (key) seenKeys.add(key);
    merged.push(event);
  }
  return merged;
}

export function assembleIntelligence(input: AssembleInput = {}): LitigationOS {
  const catalog = input.catalog ?? intelligenceCatalog;
  const summaries = input.summaries ?? cases;
  const log = input.timeline ?? timeline;
  const fromTimeline = eventsFromTimeline(log, catalog);
  const fromFeed =
    input.events ?? (input.timeline === undefined ? (loggedEventLog as LitigationEvent[]) : []);
  const events = mergeEventStreams(
    fromFeed.map((event) => enrichEvent(event, catalog)),
    fromTimeline,
  );
  if (input.publish) {
    resetEventBus();
    publishAll(events);
  }
  const graph = buildKnowledgeGraph(summaries, catalog);
  const dependencyClocks = resolveDeadlines(catalog, events);
  const briefingClocks = briefingClocksFromEvents(events, catalog, summaries);
  const clocks = [...dependencyClocks, ...briefingClocks];
  const twins = summaries
    .filter((row) => row.lifecycle === "active" || row.lifecycle === "pre_filing")
    .map((summary) =>
      deriveTwin(summary, catalog, events, [
        ...clocks.filter((clock) => clock.matter === summary.number),
        ...upcomingClocks(summary, log),
      ]),
    );
  const significant = events.filter(
    (event) =>
      event.type === "MOTION_FILED" || (event.type === "ORDER_ENTERED" && Boolean(event.payload?.triggerId)),
  );
  const warRooms = warRoomsFromEvents(significant.slice(0, 24), catalog);
  const overnight = overnightBrief({
    asOf: input.asOf ?? "Sep. 11, 2026",
    twins,
    events,
    catalog,
    shockwaves: [
      shockwaveFromOpinion(
        {
          title: "Watch: Ninth Circuit QI / clearly-established inquiry",
          court: "CA9",
          issues: ["qualified_immunity"],
          holdings: "Any new CA9 opinion narrowing clearly-established-law would hit the live Serrato MTD and the anticipated HOPE QI fight.",
        },
        catalog,
      ),
    ],
  });
  return {
    catalog,
    graph,
    events,
    twins,
    clocks,
    warRooms,
    overnight,
    disclaimer: COVERAGE_DISCLAIMER,
  };
}

let cached: LitigationOS | null = null;

export function getLitigationOS(): LitigationOS {
  cached ??= assembleIntelligence();
  return cached;
}

export function twinFor(matter: number, os: LitigationOS = getLitigationOS()): LitigationTwin | undefined {
  return os.twins.find((twin) => twin.matter === matter);
}

export function commandCenter(matter: number, os: LitigationOS = getLitigationOS()) {
  const twin = twinFor(matter, os);
  const matrices = matrixForMatter(os.catalog, matter);
  return {
    twin,
    matrices,
    warRooms: os.warRooms.filter((room) => room.matter === matter).slice(0, 3),
    diffs: diffsFromEvents(os.catalog, os.events, matter),
    fingerprints: fingerprintForMatter(os.catalog, matter),
    clocks: os.clocks.filter((clock) => clock.matter === matter),
    judge: os.catalog.judges.find((row) => os.graph.edges.some((edge) => edge.from === `matter:${matter}` && edge.to === `judge:${row.id}`)),
    radar: qiRadar(os.graph, os.catalog, new Set(os.twins.map((twin) => twin.matter))),
  };
}

export {
  auditCatalog,
  coverageReport,
  diffsForMatter,
  diffsFromEvents,
  fingerprintForMatter,
  matrixForMatter,
  qiRadar,
  recapAdvice,
  shockwaveFromOpinion,
  simulateDomino,
  systemicImportance,
};
