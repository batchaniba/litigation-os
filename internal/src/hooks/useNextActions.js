import { useMemo } from "react";
import upcoming from "../data/upcoming.json";
import graph from "../data/crossMatter.json";
import { cases } from "../data/matters";
import { buildQueue, yourQueue } from "../../scripts/lib/next-actions.mjs";

/** Same ranking as `npm run next`, fed from upcoming.json (the upcoming:true
 *  slice). buildQueue ignores past events, so the dashboard must not import
 *  the full timeline.json log. */
export function useNextActions(horizonDays = 30) {
  return useMemo(() => {
    const queue = buildQueue(upcoming, cases, {
      horizonDays,
      clusters: graph.clusters,
    });
    return { queue, mine: yourQueue(queue) };
  }, [horizonDays]);
}
