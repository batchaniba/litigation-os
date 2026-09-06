import { useMemo } from "react";
import timeline from "../data/timeline.json";
import { cases } from "../data/matters";
import { buildQueue, yourQueue } from "../../scripts/lib/next-actions.mjs";

/** Same queue as `npm run next` — ranked from timeline.json, not upcoming.json. */
export function useNextActions(horizonDays = 30) {
  return useMemo(() => {
    const queue = buildQueue(timeline, cases, { horizonDays });
    return { queue, mine: yourQueue(queue) };
  }, [horizonDays]);
}
