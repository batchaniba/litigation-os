import type { MatterLifecycle, MatterSummary } from "../types/portfolio";

export const MATTER_LIFECYCLES = [
  "active",
  "pre_filing",
  "settled",
  "dismissed",
  "abandoned",
  "closed",
] as const;

/** Still on the open docket (includes settled — same as historic !archived filter). */
const OPEN_LIFECYCLES = new Set<MatterLifecycle>(["active", "pre_filing", "settled"]);

/** Actively litigated or pending filing — excludes settled and terminal dispositions. */
const LIVE_LIFECYCLES = new Set<MatterLifecycle>(["active", "pre_filing"]);

const TERMINAL_LIFECYCLES = new Set<MatterLifecycle>(["dismissed", "abandoned", "closed"]);

export function isOpenLifecycle(lifecycle: MatterLifecycle | undefined): boolean {
  return lifecycle != null && OPEN_LIFECYCLES.has(lifecycle);
}

export function isLiveLifecycle(lifecycle: MatterLifecycle | undefined): boolean {
  return lifecycle != null && LIVE_LIFECYCLES.has(lifecycle);
}

export function isTerminalLifecycle(lifecycle: MatterLifecycle | undefined): boolean {
  return lifecycle != null && TERMINAL_LIFECYCLES.has(lifecycle);
}

/** Prefer structured lifecycle; fall back to legacy archived flag. */
export function isArchivedMatter(matter: Pick<MatterSummary, "lifecycle" | "archived">): boolean {
  if (matter.lifecycle) return isTerminalLifecycle(matter.lifecycle);
  return Boolean(matter.archived);
}

export function lifecycleLabel(lifecycle: MatterLifecycle): string {
  switch (lifecycle) {
    case "active":
      return "Active";
    case "pre_filing":
      return "Pre-filing";
    case "settled":
      return "Settled";
    case "dismissed":
      return "Dismissed";
    case "abandoned":
      return "Abandoned";
    case "closed":
      return "Closed";
    default:
      return lifecycle;
  }
}

export function archivedFromLifecycle(lifecycle: MatterLifecycle): boolean {
  return isTerminalLifecycle(lifecycle);
}
