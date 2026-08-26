// Shared lifecycle helpers for Node scripts (validate, README gen, scaffold).

export const MATTER_LIFECYCLES = [
  "active",
  "pre_filing",
  "settled",
  "dismissed",
  "abandoned",
  "closed",
];

const TERMINAL = new Set(["dismissed", "abandoned", "closed"]);
// Still on the open docket -- settled included, same as isOpenLifecycle on
// the TS side. The "Active / Open" README table is keyed off this, not off
// "currently being litigated," so a settled-but-not-dismissed matter (e.g.
// Matter 22) stays in it; isSettledLifecycle below drives its own "Settled"
// summary line independently, so the row can be both.
const README_ACTIVE = new Set(["active", "pre_filing", "settled"]);

export function isTerminalLifecycle(lifecycle) {
  return TERMINAL.has(lifecycle);
}

export function isSettledLifecycle(lifecycle) {
  return lifecycle === "settled";
}

export function archivedFromLifecycle(lifecycle) {
  return isTerminalLifecycle(lifecycle);
}

/** README Active/Open vs Closed buckets -- settled matters count as open. */
export function readmeBucket(lifecycle) {
  if (README_ACTIVE.has(lifecycle)) return "active";
  return "closed";
}

export function lifecycleLabel(lifecycle) {
  return (
    {
      active: "Active",
      pre_filing: "Pre-filing",
      settled: "Settled",
      dismissed: "Dismissed",
      abandoned: "Abandoned",
      closed: "Closed",
    }[lifecycle] ?? lifecycle
  );
}
