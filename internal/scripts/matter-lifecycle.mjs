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
const README_ACTIVE = new Set(["active", "pre_filing"]);

export function isTerminalLifecycle(lifecycle) {
  return TERMINAL.has(lifecycle);
}

export function archivedFromLifecycle(lifecycle) {
  return isTerminalLifecycle(lifecycle);
}

/** README Active / Settled / Closed buckets. */
export function readmeBucket(lifecycle) {
  if (lifecycle === "settled") return "settled";
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
