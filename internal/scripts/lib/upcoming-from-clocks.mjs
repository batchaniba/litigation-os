// Live calendar from clocks.json. timeline.json is the archive.
// Pure: no fs. Node loaders live in load-clocks.mjs; the SPA reads published clocks.
// Stored statuses live in clock-status.mjs. `overdue` is derived only.

import { dateKeyFromLabel, dateLabelFromKey } from "./next-actions.mjs";
import {
  CLOCK_RANK,
  DEAD_CLOCK_STATUS_SET,
  isClockOverdue,
  isDeadClock,
} from "./clock-status.mjs";

export {
  CLOCK_RANK,
  CLOCK_STATUSES,
  isClockOverdue,
  isDeadClock,
} from "./clock-status.mjs";
export const DEAD_CLOCK_STATUSES = DEAD_CLOCK_STATUS_SET;

export function isContingentUndated(clock) {
  return clock?.status === "contingent" && !clock?.date;
}

/** open/set, and contingent only when dated. Vacated/satisfied/legacy-closed out. */
export function isLiveClock(clock) {
  if (!clock || typeof clock !== "object") return false;
  if (isDeadClock(clock)) return false;
  if (isContingentUndated(clock)) return false;
  return true;
}

export function isDatedLiveClock(clock) {
  return isLiveClock(clock) && Boolean(clock.date);
}

function asMap(clocksByMatter) {
  if (clocksByMatter instanceof Map) return clocksByMatter;
  return new Map(
    Object.entries(clocksByMatter ?? {}).map(([key, clocks]) => [Number(key), clocks]),
  );
}

function mergeKey(clock) {
  return `${clock.date ?? ""}|${clock.title ?? ""}|${clock.source ?? ""}`;
}

function clockDateLabel(clock) {
  if (typeof clock.date_label === "string" && clock.date_label.trim()) return clock.date_label.trim();
  return dateLabelFromKey(clock.date) || "";
}

/**
 * Flatten per-matter clocks into timeline-shaped upcoming rows.
 * Same date+title+source across matters become one row with a unioned matters[].
 */
export function clocksToUpcomingEvents(clocksByMatter, options = {}) {
  const includeUndated = options.includeUndated === true;
  // Public outputs (upcoming.json, README) pass excludePrivate: clocks marked
  // private: true (e.g. confidential settlement mechanics) stay in the laptop tools.
  const excludePrivate = options.excludePrivate === true;
  const today = options.today;
  const groups = new Map();

  for (const [number, clocks] of asMap(clocksByMatter)) {
    const matter = Number(number);
    if (!Number.isInteger(matter)) continue;
    for (const clock of clocks ?? []) {
      if (!isLiveClock(clock)) continue;
      if (excludePrivate && clock.private === true) continue;
      const dated = Boolean(clock.date);
      if (!dated && !includeUndated) continue;
      const key = mergeKey(clock);
      const existing = groups.get(key);
      if (existing) {
        if (!existing.matters.includes(matter)) existing.matters.push(matter);
        if (!existing.source && clock.source) existing.source = clock.source;
        if (!existing.actor && clock.actor) existing.actor = clock.actor;
        continue;
      }
      const overdue = isClockOverdue(clock, today);
      const dateLabel = clockDateLabel(clock);
      const row = {
        date: dateLabel || (dated ? clock.date : "undated"),
        event: clock.title ?? "",
        matters: [matter],
        type: clock.kind ?? "event",
        upcoming: true,
      };
      if (clock.actor) row.actor = clock.actor;
      if (clock.source) row.source = clock.source;
      // Derived display on the generated upcoming row — not a stored clocks.json status.
      if (overdue) row.status = "overdue";
      groups.set(key, row);
    }
  }

  const events = [...groups.values()];
  for (const row of events) row.matters.sort((a, b) => a - b);
  events.sort((a, b) => {
    const da = dateKeyFromLabel(a.date) || (/\d{4}-\d{2}-\d{2}/.test(a.date) ? a.date : "9999-99-99");
    const db = dateKeyFromLabel(b.date) || (/\d{4}-\d{2}-\d{2}/.test(b.date) ? b.date : "9999-99-99");
    if (da !== db) return da < db ? -1 : 1;
    return (a.matters[0] ?? 0) - (b.matters[0] ?? 0);
  });
  return events;
}

function clockSortDate(clock) {
  return clock.date || clock.date_label || "9999-99-99";
}

export function liveClocks(clocks) {
  return (clocks ?? []).filter((c) => isLiveClock(c));
}

/** Prefer a dated live clock. Overdue is a fact on the index row, not a schema fail. */
export function nextFromClocks(clocks, today) {
  const live = liveClocks(clocks)
    .slice()
    .sort((a, b) => {
      const rank = (CLOCK_RANK[a.status] ?? 5) - (CLOCK_RANK[b.status] ?? 5);
      if (rank) return rank;
      return String(clockSortDate(a)).localeCompare(String(clockSortDate(b)));
    });
  const dated = live.find((c) => c.date);
  const chosen = dated ?? live[0] ?? null;
  if (!chosen) return { next_clock: null, overdue: false };
  const overdue = isClockOverdue(chosen, today);
  return {
    next_clock: {
      id: chosen.id,
      date: chosen.date ?? null,
      kind: chosen.kind,
      // Derived index chip only. clocks.json keeps the stored status.
      status: overdue ? "overdue" : chosen.status,
      title: chosen.title,
      source_dkt: chosen.source_dkt ?? null,
    },
    overdue,
  };
}
