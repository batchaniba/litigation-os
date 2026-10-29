import { useEffect, useState } from "react";
import {
  PORTFOLIO_TZ,
  msUntilNextMidnight,
  todayKey,
} from "../../scripts/lib/next-actions.mjs";

const MAX_TIMEOUT = 2_147_483_647;

/**
 * Viewer's current civil date in America/Los_Angeles.
 * Recomputed on mount, window focus, tab visibility, and PT midnight.
 * Never reads a build-time or index `today`.
 */
export function usePortfolioToday() {
  const [today, setToday] = useState(() => todayKey(PORTFOLIO_TZ));

  useEffect(() => {
    let timeoutId;

    const refresh = () => {
      setToday((prev) => {
        const next = todayKey(PORTFOLIO_TZ);
        return next === prev ? prev : next;
      });
    };

    const armMidnight = () => {
      clearTimeout(timeoutId);
      const wait = Math.min(msUntilNextMidnight(PORTFOLIO_TZ), MAX_TIMEOUT);
      timeoutId = setTimeout(() => {
        refresh();
        armMidnight();
      }, wait);
    };

    const onWake = () => {
      refresh();
      armMidnight();
    };

    refresh();
    armMidnight();
    window.addEventListener("focus", onWake);
    document.addEventListener("visibilitychange", onWake);
    return () => {
      clearTimeout(timeoutId);
      window.removeEventListener("focus", onWake);
      document.removeEventListener("visibilitychange", onWake);
    };
  }, []);

  return today;
}
