import { describe, expect, it } from "vitest";
import {
  clocksToUpcomingEvents,
  isLiveClock,
  nextFromClocks,
} from "../../scripts/lib/upcoming-from-clocks.mjs";

describe("upcoming from clocks", () => {
  const clocks = {
    24: [
      {
        id: "mtd-hearing",
        date: "2026-11-20",
        kind: "hearing",
        status: "set",
        title: "MTD FAC Zoom",
        actor: "you",
      },
      {
        id: "cmc-after-mtd",
        date: null,
        kind: "cmc",
        status: "contingent",
        title: "CMC after MTD",
        actor: "you",
      },
      {
        id: "name-conform",
        date: null,
        kind: "filing",
        status: "open",
        title: "Unfiled name-conform packet",
        actor: "you",
      },
      {
        id: "vacated",
        date: "2026-09-30",
        kind: "hearing",
        status: "vacated",
        title: "Sep. 30 vacated",
        actor: "court",
      },
    ],
    1: [
      {
        id: "sol",
        date: "2026-11-01",
        date_label: "Nov. 1, 2026",
        kind: "deadline",
        status: "open",
        title: "CCP §335.1 backstop",
        actor: "you",
        source: "/documents/matter-33/incident/Arrest Report.pdf",
      },
    ],
    32: [
      {
        id: "sol-copy",
        date: "2026-11-01",
        date_label: "Nov. 1, 2026",
        kind: "deadline",
        status: "open",
        title: "CCP §335.1 backstop",
        actor: "you",
        source: "/documents/matter-33/incident/Arrest Report.pdf",
      },
    ],
  };

  it("drops vacated and contingent-undated from the live set", () => {
    expect(isLiveClock(clocks[24][0])).toBe(true);
    expect(isLiveClock(clocks[24][1])).toBe(false);
    expect(isLiveClock(clocks[24][3])).toBe(false);
  });

  it("writes dated live clocks and merges the same event across matters", () => {
    const rows = clocksToUpcomingEvents(clocks, { today: "2026-09-17" });
    expect(rows.map((r) => r.event).sort()).toEqual(["CCP §335.1 backstop", "MTD FAC Zoom"]);
    const sol = rows.find((r) => r.event === "CCP §335.1 backstop");
    expect(sol.matters).toEqual([1, 32]);
    expect(sol.date).toBe("Nov. 1, 2026");
  });

  it("keeps open undated clocks only when asked", () => {
    const datedOnly = clocksToUpcomingEvents(clocks, { today: "2026-09-17" });
    expect(datedOnly.some((r) => r.event === "Unfiled name-conform packet")).toBe(false);
    const withUndated = clocksToUpcomingEvents(clocks, { today: "2026-09-17", includeUndated: true });
    expect(withUndated.some((r) => r.event === "Unfiled name-conform packet")).toBe(true);
  });

  it("marks a past dated clock overdue on the index row without dropping it", () => {
    const { next_clock, overdue } = nextFromClocks(
      [{ id: "past", date: "2026-09-01", kind: "deadline", status: "open", title: "already due", source_dkt: null }],
      "2026-09-17",
    );
    expect(overdue).toBe(true);
    expect(next_clock.status).toBe("overdue");
    expect(next_clock.date).toBe("2026-09-01");
  });

  it("keeps private clocks off the public index and the SPA upcoming snapshot", () => {
    const rows = [
      {
        id: "pay",
        date: "2026-10-09",
        kind: "deadline",
        status: "open",
        title: "WATCH — settlement payment due",
        actor: "opposing",
        private: true,
      },
      {
        id: "cmc",
        date: "2026-12-17",
        kind: "hearing",
        status: "open",
        title: "Case Management Conference",
        actor: "you",
      },
    ];
    const { next_clock } = nextFromClocks(rows, "2026-10-28");
    expect(next_clock.id).toBe("cmc");
    const spa = clocksToUpcomingEvents({ 27: rows }, { today: "2026-10-28", excludePrivate: true });
    expect(spa.map((r) => r.event)).toEqual(["Case Management Conference"]);
    const desk = clocksToUpcomingEvents({ 27: rows }, { today: "2026-10-28" });
    expect(desk.some((r) => r.event.includes("settlement payment"))).toBe(true);
  });
});
