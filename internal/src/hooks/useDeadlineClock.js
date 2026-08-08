import { useState, useEffect } from "react";
import { DEFAULT_DEADLINE, CLOCK_FREEZE_UNTIL } from "../constants";
import { parseEventDatePDT } from "../utils/dateUtils";

const DEFAULT_DEADLINE_TS = +DEFAULT_DEADLINE;
const FREEZE_UNTIL_TS = +CLOCK_FREEZE_UNTIL;
const FROZEN_STATE = { label: "Palacios Federal Default — 03/28/2026", days: 0, hours: 0, mins: 0, secs: 0, urgent: false, frozen: true };
const NO_EVENTS_STATE = { label: "No upcoming deadlines", days: 0, hours: 0, mins: 0, secs: 0, urgent: false };

// Seconds only matter while the countdown is on screen. When it is collapsed the
// only thing read off this state is `urgent` (it tints the banner border), so a
// minute is plenty and the app is not re-rendering once a second for digits
// nobody can see.
const VISIBLE_INTERVAL_MS = 1000;
const HIDDEN_INTERVAL_MS = 60000;

const sameState = (a, b) =>
  a.label === b.label && a.days === b.days && a.hours === b.hours &&
  a.mins === b.mins && a.secs === b.secs && a.urgent === b.urgent && !!a.frozen === !!b.frozen;

export const useDeadlineClock = (upcomingEvents, visible = true) => {
  const [timeLeft, setTimeLeft] = useState({ label: "", days: 0, hours: 0, mins: 0, secs: 0, urgent: false, frozen: false });

  useEffect(() => {
    // Precompute event-derived values once per upcomingEvents change.
    const ev = upcomingEvents[0];
    const eventLabel = ev ? ev.date + " — " + ev.event.slice(0, 55) : null;
    const eventTargetTs = ev ? parseEventDatePDT(ev.date).getTime() + 17 * 3600 * 1000 : null;

    let cancelled = false;
    let id = null;

    const compute = (nowTs) => {
      if (nowTs < DEFAULT_DEADLINE_TS) {
        const diff = DEFAULT_DEADLINE_TS - nowTs;
        return {
          label: "Palacios Federal Default — Answer Deadline",
          days: Math.floor(diff / 86400000),
          hours: Math.floor((diff % 86400000) / 3600000),
          mins: Math.floor((diff % 3600000) / 60000),
          secs: Math.floor((diff % 60000) / 1000),
          urgent: diff < 86400000,
          frozen: false,
        };
      }
      if (nowTs < FREEZE_UNTIL_TS) return FROZEN_STATE;
      if (!ev) return NO_EVENTS_STATE;
      const diff = eventTargetTs - nowTs;
      if (diff <= 0) return { label: eventLabel, days: 0, hours: 0, mins: 0, secs: 0, urgent: true, frozen: false };
      return {
        label: eventLabel,
        days: Math.floor(diff / 86400000),
        hours: Math.floor((diff % 86400000) / 3600000),
        mins: Math.floor((diff % 3600000) / 60000),
        secs: Math.floor((diff % 60000) / 1000),
        urgent: diff < 86400000,
        frozen: false,
      };
    };

    const tick = () => {
      if (cancelled) return;
      const next = compute(Date.now());
      // Skip re-render when nothing visible changed (e.g. frozen phase, no events).
      setTimeLeft(prev => (sameState(prev, next) ? prev : next));
    };

    tick();
    id = setInterval(tick, visible ? VISIBLE_INTERVAL_MS : HIDDEN_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [upcomingEvents, visible]);

  return timeLeft;
};
