import { isCourtDay, isNonCourtDay } from "./holidays";
import { addCalendarDays } from "./format";
import type { CourtKey, DayKey } from "./types";

/**
 * CCP §12 / FRCP 6(a)(1)(A): exclude the trigger day, then count `n` calendar days forward.
 * Does not itself apply weekend/holiday extension — call rollForwardAfter for that.
 */
export function addCalendarDaysAfter(trigger: DayKey, n: number): DayKey {
  if (n < 0) throw new Error("addCalendarDaysAfter expects a non-negative count");
  return addCalendarDays(trigger, n);
}

/**
 * Count `n` calendar days backward from `anchor`, excluding the anchor day (CCP §12 / §12c(a)).
 * Example: 5 calendar days before Aug. 21 → start Aug. 20 as day 1 → Aug. 16.
 */
export function subtractCalendarDaysBefore(anchor: DayKey, n: number): DayKey {
  if (n < 0) throw new Error("subtractCalendarDaysBefore expects a non-negative count");
  return addCalendarDays(anchor, -n);
}

/**
 * Count `n` court days backward from `hearing`, excluding the hearing day (CCP §12c(a)).
 * Only Monday–Friday non-holidays count.
 */
export function subtractCourtDaysBefore(hearing: DayKey, n: number, court: CourtKey): DayKey {
  if (n < 0) throw new Error("subtractCourtDaysBefore expects a non-negative count");
  let cursor = hearing;
  let remaining = n;
  while (remaining > 0) {
    cursor = addCalendarDays(cursor, -1);
    if (isCourtDay(cursor, court)) remaining -= 1;
  }
  return cursor;
}

/** Count `n` court days forward after `trigger`, excluding the trigger day. */
export function addCourtDaysAfter(trigger: DayKey, n: number, court: CourtKey): DayKey {
  if (n < 0) throw new Error("addCourtDaysAfter expects a non-negative count");
  let cursor = trigger;
  let remaining = n;
  while (remaining > 0) {
    cursor = addCalendarDays(cursor, 1);
    if (isCourtDay(cursor, court)) remaining -= 1;
  }
  return cursor;
}

/**
 * CCP §12a / FRCP 6(a)(1)(C): if the last day is a non-court day, roll forward
 * to the next court day.
 */
export function rollForwardToCourtDay(day: DayKey, court: CourtKey): { date: DayKey; rolled: boolean } {
  let cursor = day;
  let rolled = false;
  while (isNonCourtDay(cursor, court)) {
    cursor = addCalendarDays(cursor, 1);
    rolled = true;
  }
  return { date: cursor, rolled };
}

/**
 * When counting backward for service deadlines and the computed day lands on a
 * weekend/holiday, move to the preceding court day (Sac Law Library / CCP practice).
 */
export function rollBackwardToCourtDay(day: DayKey, court: CourtKey): { date: DayKey; rolled: boolean } {
  let cursor = day;
  let rolled = false;
  while (isNonCourtDay(cursor, court)) {
    cursor = addCalendarDays(cursor, -1);
    rolled = true;
  }
  return { date: cursor, rolled };
}

/**
 * FRCP 6(d): after the period expires under 6(a), add 3 calendar days for mail
 * (or clerk / other consented non-electronic service), then apply 6(a) last-day roll.
 */
export function addFrcpMailDays(periodEnd: DayKey, court: CourtKey): { date: DayKey; rolled: boolean; afterMail: DayKey } {
  const afterMail = addCalendarDays(periodEnd, 3);
  const rolled = rollForwardToCourtDay(afterMail, court);
  return { date: rolled.date, rolled: rolled.rolled || afterMail !== periodEnd, afterMail };
}

/**
 * CCP §1005(b) mail extension for moving papers: after finding the 16-court-day
 * filing/personal-service date, count further backward the mail calendar days (CCP §12c(b)).
 * If that day is a non-court day, roll to the prior court day.
 */
export function subtractMailCalendarDays(
  courtDayDeadline: DayKey,
  mailCalendarDays: number,
  court: CourtKey,
): { date: DayKey; rolled: boolean; rawDate: DayKey } {
  const rawDate = subtractCalendarDaysBefore(courtDayDeadline, mailCalendarDays);
  const rolled = rollBackwardToCourtDay(rawDate, court);
  return { date: rolled.date, rolled: rolled.rolled, rawDate };
}
