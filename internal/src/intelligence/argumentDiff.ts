import type { ArgumentDiff, ArgumentSnapshot, IntelligenceCatalog, LitigationEvent } from "./types";
import { toDayKey } from "../utils/deadlineMath/format";
import { snapshotFromFiling } from "./extract";

function snapshotDateKey(date: string): string {
  try {
    return toDayKey(date);
  } catch {
    return date;
  }
}

export function diffArguments(prior: ArgumentSnapshot, current: ArgumentSnapshot): ArgumentDiff {
  const priorArgs = new Set(prior.arguments);
  const currentArgs = new Set(current.arguments);
  const added = current.arguments.filter((item) => !priorArgs.has(item));
  const abandoned = prior.arguments.filter((item) => !currentArgs.has(item));
  const kept = current.arguments.filter((item) => priorArgs.has(item));
  const priorAuth = new Set(prior.authorities);
  const currentAuth = new Set(current.authorities);
  const priorAdmit = new Set(prior.admissions);
  return {
    matter: current.matter,
    prior: prior.filing,
    current: current.filing,
    added,
    abandoned,
    modified: added.length + abandoned.length > 0 ? kept : [],
    newAuthorities: current.authorities.filter((item) => !priorAuth.has(item)),
    droppedAuthorities: prior.authorities.filter((item) => !currentAuth.has(item)),
    factualAdmissions: current.admissions.filter((item) => !priorAdmit.has(item)),
  };
}

export function diffsForMatter(snapshots: ArgumentSnapshot[], matter: number): ArgumentDiff[] {
  const ordered = snapshots
    .filter((row) => row.matter === matter)
    .sort((a, b) => snapshotDateKey(a.date).localeCompare(snapshotDateKey(b.date)));
  const diffs: ArgumentDiff[] = [];
  for (let i = 1; i < ordered.length; i += 1) diffs.push(diffArguments(ordered[i - 1], ordered[i]));
  return diffs;
}

export function liveSnapshots(events: LitigationEvent[], catalog: IntelligenceCatalog): ArgumentSnapshot[] {
  return events
    .filter((event) => event.type === "MOTION_FILED" && event.matter)
    .map((event) => {
      const text = [event.summary, typeof event.payload?.body === "string" ? event.payload.body : ""].filter(Boolean).join("\n");
      return snapshotFromFiling({
        matter: event.matter as number,
        filing: event.docket != null ? `Dkt. ${event.docket} ${event.summary.slice(0, 80)}` : event.summary.slice(0, 120),
        date: event.at,
        text,
        docket: event.docket,
        catalog,
      });
    });
}

export function diffsFromEvents(catalog: IntelligenceCatalog, events: LitigationEvent[], matter: number): ArgumentDiff[] {
  return diffsForMatter([...catalog.arguments, ...liveSnapshots(events, catalog)], matter);
}
