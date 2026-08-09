import { afterEach, describe, expect, it, vi } from "vitest";
import { getPDTMidnight, parseEventDatePDT } from "./dateUtils";

// 2026 US transitions: DST starts Mar. 8, ends Nov. 1.
const PDT_DAY = "2026-08-08T12:00:00-07:00"; // mid-summer, UTC-7
const PST_DAY = "2026-12-10T12:00:00-08:00"; // mid-winter, UTC-8

describe("Pacific date helpers", () => {
  afterEach(() => vi.useRealTimers());

  it("anchors summer dates to UTC-7 midnight", () => {
    expect(parseEventDatePDT("Aug. 8, 2026").toISOString()).toBe("2026-08-08T07:00:00.000Z");
  });

  it("anchors winter dates to UTC-8 midnight", () => {
    expect(parseEventDatePDT("Dec. 10, 2026").toISOString()).toBe("2026-12-10T08:00:00.000Z");
  });

  it("keeps the calendar day in the UTC fields on both sides of the transition", () => {
    // calendarUtils.dayKey() reads these fields directly.
    for (const [input, day] of [["Aug. 8, 2026", 8], ["Dec. 10, 2026", 10]]) {
      expect(parseEventDatePDT(input).getUTCDate()).toBe(day);
    }
  });

  it("handles the transition days themselves", () => {
    expect(parseEventDatePDT("Nov. 1, 2026").toISOString()).toBe("2026-11-01T07:00:00.000Z"); // still PDT at midnight
    expect(parseEventDatePDT("Nov. 2, 2026").toISOString()).toBe("2026-11-02T08:00:00.000Z"); // first full PST day
    expect(parseEventDatePDT("Mar. 8, 2026").toISOString()).toBe("2026-03-08T08:00:00.000Z"); // still PST at midnight
  });

  it("treats an event dated today as today during PDT", () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date(PDT_DAY));
    expect(+parseEventDatePDT("Aug. 8, 2026")).toBe(+getPDTMidnight());
  });

  // The regression: parseEventDatePDT used to hardcode UTC-7, so during PST it
  // landed an hour before getPDTMidnight() and today's deadlines read as past —
  // dropping them from upcoming events, the deadline banner and next actions.
  it("treats an event dated today as today during PST", () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date(PST_DAY));
    expect(+parseEventDatePDT("Dec. 10, 2026")).toBe(+getPDTMidnight());
    expect(+parseEventDatePDT("Dec. 10, 2026")).toBeGreaterThanOrEqual(+getPDTMidnight());
  });

  it("strips the approximate-date marker", () => {
    expect(+parseEventDatePDT("~Dec. 10, 2026")).toBe(+parseEventDatePDT("Dec. 10, 2026"));
  });

  it("returns an Invalid Date rather than throwing on unparseable input", () => {
    expect(Number.isNaN(+parseEventDatePDT("TBD"))).toBe(true);
  });

  // Native Date parsing is loose — "Jul 9-10, 2026" becomes July 9 *2010*. That is
  // why calendarUtils.isGroundedDate() gates this function rather than trusting it;
  // pinned here so the looseness stays a known quantity.
  it("inherits native Date's loose parsing for non-exact dates", () => {
    expect(parseEventDatePDT("Jul. 9-10, 2026").getUTCFullYear()).toBe(2010);
  });

  it("resolves getPDTMidnight against Pacific time, not the host timezone", () => {
    vi.useFakeTimers();
    // 01:00 UTC on Dec. 11 is still Dec. 10 in California.
    vi.setSystemTime(new Date("2026-12-11T01:00:00Z"));
    expect(getPDTMidnight().toISOString()).toBe("2026-12-10T08:00:00.000Z");
  });
});
