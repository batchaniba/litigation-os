import { intelligenceCatalog } from "../data/intelligence/catalog";
import { cases } from "../data/matters";
import { timeline } from "../data/timeline";
import type { MatterSummary, TimelineEvent } from "../types/portfolio";
import { diffsForMatter } from "./argumentDiff";
import { auditCatalog } from "./citeProof";
import { eventsFromTimeline } from "./classify";
import { COVERAGE_DISCLAIMER, type IntelligenceCatalog, type KnowledgeGraph, type LitigationEvent, type LitigationTwin, type OvernightBrief, type PendingClock, type WarRoom } from "./types";
import { coverageReport, matrixForMatter } from "./coverage";
import { resolveDeadlines } from "./deadlines";
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

export function assembleIntelligence(input: AssembleInput = {}): LitigationOS {
  const catalog = input.catalog ?? intelligenceCatalog;
  const summaries = input.summaries ?? cases;
  const log = input.timeline ?? timeline;
  const events = eventsFromTimeline(log, catalog);
  if (input.publish) {
    resetEventBus();
    publishAll(events);
  }
  const graph = buildKnowledgeGraph(summaries, catalog);
  const dependencyClocks = resolveDeadlines(catalog, events);
  const twins = summaries
    .filter((row) => row.lifecycle === "active" || row.lifecycle === "pre_filing")
    .map((summary) => {
      const twin = deriveTwin(summary, catalog, events, [...dependencyClocks, ...upcomingClocks(summary, log)]);
      return twin;
    });
  const significant = events.filter(
    (event) =>
      (event.type === "MOTION_FILED" || event.type === "ORDER_ENTERED") &&
      catalog.motions.some((motion) => motion.matter === event.matter),
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
    clocks: dependencyClocks,
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
    diffs: diffsForMatter(os.catalog.arguments, matter),
    fingerprints: fingerprintForMatter(os.catalog, matter),
    clocks: os.clocks.filter((clock) => clock.matter === matter),
    judge: os.catalog.judges.find((row) => os.graph.edges.some((edge) => edge.from === `matter:${matter}` && edge.to === `judge:${row.id}`)),
    radar: qiRadar(os.graph, os.catalog),
  };
}

export {
  auditCatalog,
  coverageReport,
  diffsForMatter,
  fingerprintForMatter,
  matrixForMatter,
  qiRadar,
  recapAdvice,
  shockwaveFromOpinion,
  simulateDomino,
  systemicImportance,
};
