import { useMemo } from "react";
import graph from "../data/crossMatter.json";
import { cases } from "../data/matters";
import { buildQueue, nextOnYourDesk, yourQueue } from "../../scripts/lib/next-actions.mjs";
import { clocksToUpcomingEvents } from "../../scripts/lib/upcoming-from-clocks.mjs";
import { usePortfolioToday } from "./usePortfolioToday";

const publishModules = import.meta.glob("../data/matters/publish/*.json", { eager: true });

function clocksByMatterFromGlob() {
  const byMatter = new Map();
  for (const [file, mod] of Object.entries(publishModules)) {
    const match = file.match(/\/(\d{2})\.json$/);
    if (!match) continue;
    const clocks = mod?.default?.clocks;
    byMatter.set(Number(match[1]), Array.isArray(clocks) ? clocks : []);
  }
  return byMatter;
}

/** Same queue as `npm run next` — ranked from clocks.json, not timeline.json. */
export function useNextActions(horizonDays = 30) {
  const today = usePortfolioToday();
  return useMemo(() => {
    const upcoming = clocksToUpcomingEvents(clocksByMatterFromGlob(), {
      includeUndated: true,
      today,
    });
    const queue = buildQueue(upcoming, cases, {
      today,
      horizonDays,
      clusters: graph.clusters,
    });
    return { queue, mine: yourQueue(queue), nextMine: nextOnYourDesk(queue), today };
  }, [horizonDays, today]);
}
