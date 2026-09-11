import type { IntelligenceCatalog, LitigationEvent, LitigationTwin, OvernightBrief, ShockwaveReport } from "./types";

export function overnightBrief(input: {
  asOf: string;
  twins: LitigationTwin[];
  events: LitigationEvent[];
  shockwaves?: ShockwaveReport[];
  catalog: IntelligenceCatalog;
}): OvernightBrief {
  const recent = input.events.filter((event) =>
    ["DOCKET_ENTRY_ADDED", "MOTION_FILED", "ORDER_ENTERED", "COUNSEL_APPEARED", "ARGUMENT_CHANGED"].includes(event.type),
  );
  const docketChanges = recent
    .filter((event) => event.matter)
    .slice(0, 12)
    .map((event) => `Matter ${event.matter}: ${event.type.replaceAll("_", " ").toLowerCase()} — ${event.summary.slice(0, 140)}`);
  const live = input.twins.filter((twin) => twin.live_motions.some((motion) => motion.status === "live"));
  const highest = live[0] ?? input.twins.find((twin) => twin.controlling_questions.length > 0);
  const plaintiffDeadlines = input.twins.flatMap((twin) =>
    twin.pending_clocks
      .filter((clock) => clock.status === "fired" || clock.status === "date_certain")
      .map((clock) => `Matter ${twin.matter}: ${clock.label} — ${clock.displayDate ?? clock.date}`),
  );
  const precedent = (input.shockwaves ?? []).flatMap((report) =>
    report.hits.map((hit) => `${report.opinion} → Matter ${hit.matter} (${hit.impact})`),
  );
  const citationNotes = input.catalog.authorities
    .filter((authority) => input.catalog.citeproof[authority.id]?.parentheticalOverstates)
    .map((authority) => `${authority.label}: parenthetical overstates the holding.`);
  return {
    asOf: input.asOf,
    docketChanges: docketChanges.length ? docketChanges : ["No new classified docket activity in this pass."],
    precedent: precedent.length ? precedent : ["No new opinion matched the portfolio issue graph in this pass."],
    citationNotes,
    plaintiffDeadlines: plaintiffDeadlines.length ? plaintiffDeadlines : ["No plaintiff-controlled dependency clocks currently carry a date certain."],
    highestPriority: highest
      ? `Matter ${highest.matter}: ${highest.live_motions[0]?.label ?? (highest.controlling_questions.join(", ") || highest.stage)}`
      : "No live dispositive motion.",
  };
}
