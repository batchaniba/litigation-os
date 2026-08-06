import { isGroundedDate, groundEventDate, dayKey as calendarDayKey } from "../calendarUtils";
import type { DayKey } from "./types";

const MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."] as const;

export function toDayKey(input: DayKey | Date | string): DayKey {
  if (input instanceof Date) {
    if (Number.isNaN(input.getTime())) throw new Error("Invalid Date");
    // Prefer UTC fields when the Date was built as a PDT-midnight / UTC day key.
    return `${input.getUTCFullYear()}-${pad(input.getUTCMonth() + 1)}-${pad(input.getUTCDate())}`;
  }
  const trimmed = String(input).trim();
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) return trimmed;
  if (isGroundedDate(trimmed)) {
    const grounded = groundEventDate(trimmed);
    if (!grounded) throw new Error(`Unable to ground date: ${trimmed}`);
    return calendarDayKey(grounded);
  }
  // Accept HTML date inputs and ISO timestamps.
  const iso = trimmed.match(/^(\d{4}-\d{2}-\d{2})/);
  if (iso) return iso[1];
  const parsed = new Date(trimmed.replace(/\./g, ""));
  if (Number.isNaN(parsed.getTime())) throw new Error(`Unrecognized date: ${trimmed}`);
  return `${parsed.getFullYear()}-${pad(parsed.getMonth() + 1)}-${pad(parsed.getDate())}`;
}

export function formatPortfolioDate(day: DayKey): string {
  const [y, m, d] = day.split("-").map(Number);
  const month = MONTHS[m - 1];
  if (!month) throw new Error(`Invalid day key: ${day}`);
  return `${month} ${d}, ${y}`;
}

export function addCalendarDays(day: DayKey, delta: number): DayKey {
  const [y, m, d] = day.split("-").map(Number);
  const next = new Date(Date.UTC(y, m - 1, d + delta));
  return `${next.getUTCFullYear()}-${pad(next.getUTCMonth() + 1)}-${pad(next.getUTCDate())}`;
}

function pad(n: number): string {
  return String(n).padStart(2, "0");
}
