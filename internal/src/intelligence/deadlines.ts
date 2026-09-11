import { addCalendarDaysAfter, addCourtDaysAfter, rollBackwardToCourtDay, rollForwardToCourtDay, subtractCalendarDaysBefore, subtractCourtDaysBefore } from "../utils/deadlineMath/dayCount";
import { formatPortfolioDate, toDayKey } from "../utils/deadlineMath/format";
import { computeDeadlinesFromEvent } from "../utils/deadlineMath/recipes";
import type { CourtKey } from "../utils/deadlineMath/types";
import type { DeadlineRecipe, IntelligenceCatalog, LitigationEvent, PendingClock } from "./types";
import type { MatterSummary } from "../types/portfolio";

function courtKey(label?: string): CourtKey {
  if (label?.includes("E.D. Cal")) return "USDC E.D. Cal.";
  return "USDC N.D. Cal.";
}

function shift(
  anchor: string,
  spec: { days: number; unit: "calendar" | "court"; direction: "after" | "before"; roll?: "forward" | "backward" | "none" },
  court: CourtKey,
): { date: string; displayDate: string } {
  const start = toDayKey(anchor);
  let raw =
    spec.direction === "after"
      ? spec.unit === "court"
        ? addCourtDaysAfter(start, spec.days, court)
        : addCalendarDaysAfter(start, spec.days)
      : spec.unit === "court"
        ? subtractCourtDaysBefore(start, spec.days, court)
        : subtractCalendarDaysBefore(start, spec.days);
  if (spec.roll === "forward") raw = rollForwardToCourtDay(raw, court).date;
  if (spec.roll === "backward") raw = rollBackwardToCourtDay(raw, court).date;
  return { date: raw, displayDate: formatPortfolioDate(raw) };
}

export function fireTrigger(recipe: DeadlineRecipe, firedOn: string): DeadlineRecipe {
  return { ...recipe, trigger: { ...recipe.trigger, fired: true, firedOn } };
}

export function resolveRecipe(recipe: DeadlineRecipe): PendingClock[] {
  const court = courtKey(recipe.court);
  if (!recipe.trigger.fired || !recipe.trigger.firedOn) {
    const waiting: PendingClock[] = [
      {
        id: recipe.id,
        matter: recipe.matter,
        label: recipe.label,
        status: "waiting_on_trigger",
        date: null,
        displayDate: null,
        waitingOn: recipe.trigger.description,
      },
    ];
    for (const dependent of recipe.dependents ?? []) {
      waiting.push({
        id: dependent.id,
        matter: recipe.matter,
        label: dependent.label,
        status: "waiting_on_trigger",
        date: null,
        displayDate: null,
        waitingOn: recipe.trigger.description,
        derivedFrom: recipe.id,
      });
    }
    return waiting;
  }
  const parent = shift(recipe.trigger.firedOn, recipe.offset, court);
  const clocks: PendingClock[] = [
    {
      id: recipe.id,
      matter: recipe.matter,
      label: recipe.label,
      status: "fired",
      date: parent.date,
      displayDate: parent.displayDate,
      derivedFrom: recipe.trigger.id,
    },
  ];
  for (const dependent of recipe.dependents ?? []) {
    const child = shift(parent.date, dependent, court);
    clocks.push({
      id: dependent.id,
      matter: recipe.matter,
      label: dependent.label,
      status: "fired",
      date: child.date,
      displayDate: child.displayDate,
      derivedFrom: recipe.id,
    });
  }
  return clocks;
}

export function resolveDeadlines(catalog: IntelligenceCatalog, events: LitigationEvent[] = []): PendingClock[] {
  return catalog.dependencies.flatMap((recipe) => {
    const triggerEvent = events.find(
      (event) =>
        event.type === "ORDER_ENTERED" &&
        event.matter === recipe.matter &&
        event.payload?.triggerId === recipe.trigger.id,
    );
    const live = triggerEvent?.at ? fireTrigger(recipe, toDayKey(triggerEvent.at)) : recipe;
    return resolveRecipe(live);
  });
}

/** Opposition / reply clocks from a newly filed motion that is not already a catalogued live motion. */
export function briefingClocksFromEvents(
  events: LitigationEvent[],
  catalog: IntelligenceCatalog,
  summaries: MatterSummary[],
): PendingClock[] {
  const knownLive = new Set(
    catalog.motions.filter((motion) => motion.status === "live" && motion.docket != null).map((motion) => `${motion.matter}:${motion.docket}`),
  );
  const clocks: PendingClock[] = [];
  for (const event of events) {
    if (event.type !== "MOTION_FILED" || event.matter == null || !event.at) continue;
    if (event.docket != null && knownLive.has(`${event.matter}:${event.docket}`)) continue;
    const summary = summaries.find((row) => row.number === event.matter);
    const court = summary?.court.includes("E.D. Cal") ? "USDC E.D. Cal." : "USDC N.D. Cal.";
    const recipe = court === "USDC E.D. Cal." ? "edcal_lr230c_opposition" : "ndcal_lr7_motion_filed";
    try {
      const computed = computeDeadlinesFromEvent({ recipe, anchorDate: event.at, court });
      for (const deadline of computed.deadlines) {
        if (deadline.id === "ndcal_earliest_hearing") continue;
        clocks.push({
          id: `briefing-${event.matter}-${event.docket ?? event.id}-${deadline.id}`,
          matter: event.matter,
          label: deadline.label,
          status: "date_certain",
          date: deadline.date,
          displayDate: deadline.displayDate,
          derivedFrom: event.id,
        });
      }
    } catch {
      // Unparseable filing date — skip rather than invent a clock.
    }
  }
  return clocks;
}

export function applyOrderToDependencies(
  catalog: IntelligenceCatalog,
  matter: number,
  triggerId: string,
  filedOn: string,
): IntelligenceCatalog {
  return {
    ...catalog,
    dependencies: catalog.dependencies.map((recipe) =>
      recipe.matter === matter && recipe.trigger.id === triggerId ? fireTrigger(recipe, filedOn) : recipe,
    ),
  };
}
